"""Cache behavior tests with opaque source bytes, not PDF/OCR accuracy tests."""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from harness import HarnessError, exclusive_lock, file_hash
from manual_cache import ManualCache


class ManualCacheTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="blue-ocean-manual-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = self.root / "manual.pdf"
        self.source.write_bytes(b"opaque source revision 1")
        self.cache = ManualCache(self.root)
        self.analysis_path = self.root / "reviewed.json"
        self.analysis = {
            "schema_version": 1, "source_sha256": file_hash(self.source), "analysis_revision": 1,
            "title": "Controller manual", "document_version": "1.0", "analysis_method": "fixture-reviewed",
            "summary": "Controller connections and alarms.", "units_total": 2, "reviewed_units": [1, 2],
            "limitations": [], "sections": [
                {"id": "connection", "title": "Controller connections", "unit": 1,
                 "locator": "PDF physical page 1, connector table", "keywords": ["연결", "COM1"],
                 "confidence": "verified", "content": "COM1: value 24 V. 이 값은 테스트용 근거입니다."},
                {"id": "alarm", "title": "Alarm ALM-042", "unit": 2,
                 "locator": "PDF physical page 2, alarm table", "keywords": ["에러", "ALM-042"],
                 "confidence": "verified", "content": "ALM-042: example alarm description."},
            ],
        }

    def store(self, analysis=None, source=None):
        value = self.analysis if analysis is None else analysis
        self.analysis_path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return self.cache.store(source or self.source, self.analysis_path)

    def test_first_read_store_then_targeted_search_and_reuse(self):
        missing = self.cache.status(self.source)
        self.assertEqual(missing["status"], "missing")
        stored = self.store()
        self.assertEqual(stored["status"], "ready")
        self.assertTrue(stored["reusable"])
        summary = (self.root / stored["summary"]).read_text(encoding="utf-8")
        self.assertIn("sections/connection.md", summary)
        result = self.cache.search("연결")
        self.assertEqual(result["matches"][0]["unit"], 1)
        self.assertEqual(result["matches"][0]["locator"], self.analysis["sections"][0]["locator"])
        self.assertIn("24 V", (self.root / result["matches"][0]["path"]).read_text(encoding="utf-8"))
        with mock.patch.object(self.cache, "store", side_effect=AssertionError("No reanalysis allowed")):
            self.assertEqual(self.cache.status(self.source)["generation"], stored["generation"])

    def test_identical_store_is_idempotent_even_when_json_key_order_changes(self):
        first = self.store()
        index_before = self.cache.index_path.stat().st_mtime_ns
        summary_before = (self.root / first["summary"]).stat().st_mtime_ns
        reordered = dict(reversed(list(self.analysis.items())))
        second = self.store(reordered)
        self.assertEqual(first["generation"], second["generation"])
        self.assertEqual(self.cache.index_path.stat().st_mtime_ns, index_before)
        self.assertEqual((self.root / first["summary"]).stat().st_mtime_ns, summary_before)

    def test_relative_input_paths_resolve_against_project_root(self):
        self.analysis_path.write_text(json.dumps(self.analysis), encoding="utf-8")
        result = self.cache.store("manual.pdf", "reviewed.json")
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["source"], "manual.pdf")

    def test_same_bytes_at_different_paths_reuse_without_reading_original_again(self):
        stored = self.store()
        alias = self.root / "renamed-image.jpeg"
        alias.write_bytes(self.source.read_bytes())
        self.assertEqual(self.cache.status(alias)["generation"], stored["generation"])
        result = self.cache.search("alm-042", source=alias)
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["matches"][0]["source"], "renamed-image.jpeg")
        self.assertEqual(self.store(source=alias)["generation"], stored["generation"])

    def test_changed_bytes_with_same_size_and_mtime_are_stale(self):
        stored = self.store()
        source_stat = self.source.stat()
        self.source.write_bytes(b"opaque source revision 2")
        os.utime(self.source, ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns))
        status = self.cache.status(self.source)
        self.assertEqual(status["status"], "stale")
        self.assertFalse(status["reusable"])
        result = self.cache.search("COM1")
        self.assertEqual(result["matches"], [])
        self.assertEqual(result["skipped"][0]["status"], "stale")
        self.assertTrue((self.root / stored["summary"]).exists())
        with self.assertRaises(HarnessError):
            self.store()
        self.analysis["source_sha256"] = file_hash(self.source)
        refreshed = self.store()
        self.assertNotEqual(refreshed["generation"], stored["generation"])
        self.assertTrue((self.root / stored["summary"]).exists())

    def test_partial_coverage_incrementally_extends_existing_knowledge(self):
        partial = copy.deepcopy(self.analysis)
        partial.update(reviewed_units=[1], limitations=["Page 2 not analyzed"], sections=partial["sections"][:1])
        first = self.store(partial)
        self.assertEqual(first["status"], "partial")
        self.assertEqual(self.cache.search("COM1")["matches"][0]["status"], "partial")
        self.assertEqual(self.cache.search("ALM-042")["matches"], [])
        self.analysis["analysis_revision"] = 2
        completed = self.store()
        self.assertEqual(completed["status"], "ready")
        self.assertTrue((self.root / first["analysis"]).exists())
        self.assertEqual(len(self.cache.search("ALM-042")["matches"]), 1)

    def test_unknown_page_total_or_uncertainty_never_claims_ready(self):
        self.analysis["units_total"] = None
        self.assertEqual(self.store()["status"], "partial")
        self.analysis["units_total"] = 2
        self.analysis["analysis_revision"] += 1
        self.analysis["sections"][0]["confidence"] = "uncertain"
        self.assertEqual(self.store()["status"], "partial")

    def test_new_partial_correction_supersedes_old_ready_analysis_for_all_aliases(self):
        old = self.store()
        alias = self.root / "alias.jpg"
        alias.write_bytes(self.source.read_bytes())
        self.store(source=alias)
        correction = copy.deepcopy(self.analysis)
        correction["analysis_revision"] = 2
        correction["sections"][0].update(confidence="uncertain", content="COM1 value withdrawn pending review")
        correction["limitations"] = ["Earlier COM1 value withdrawn"]
        updated = self.store(correction, alias)
        self.assertEqual(updated["status"], "partial")
        self.assertEqual(self.cache.status(self.source)["generation"], updated["generation"])
        self.assertNotEqual(old["generation"], updated["generation"])
        self.assertEqual(self.cache.search("24 V")["matches"], [])
        for source in (None, self.source, alias):
            matches = self.cache.search("withdrawn", source=source)["matches"]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["confidence"], "uncertain")
        with self.assertRaises(HarnessError):
            self.store(self.analysis)

    def test_corrupted_artifacts_are_rejected_and_analysis_can_recover_them(self):
        stored = self.store()
        target = self.root / stored["generation"] / "sections/connection.md"
        target.write_text("corrupted", encoding="utf-8")
        with self.assertRaises(HarnessError):
            self.cache.status(self.source)
        with self.assertRaises(HarnessError):
            self.store()
        self.assertEqual(target.read_text(encoding="utf-8"), "corrupted")
        self.analysis["analysis_revision"] += 1
        recovered = self.store()
        self.assertEqual(recovered["status"], "ready")
        self.assertNotEqual(recovered["generation"], stored["generation"])

    def test_unavailable_source_is_not_fresh_but_archive_remains(self):
        stored = self.store()
        self.source.unlink()
        with self.assertRaises(HarnessError):
            self.cache.status(self.source)
        result = self.cache.search("COM1")
        self.assertEqual(result["matches"], [])
        self.assertEqual(result["skipped"][0]["status"], "source_unavailable")
        self.assertTrue((self.root / stored["summary"]).is_file())

    def test_source_change_during_publication_does_not_publish_index(self):
        original_hash = file_hash
        source_calls = 0

        def changing_hash(path):
            nonlocal source_calls
            if Path(path) == self.source:
                source_calls += 1
                if source_calls == 2:
                    self.source.write_bytes(b"changed during publication")
            return original_hash(path)

        with mock.patch("manual_cache.file_hash", side_effect=changing_hash):
            with self.assertRaises(HarnessError):
                self.store()
        self.assertFalse(self.cache.index_path.exists())
        self.assertEqual(list(self.cache.cache.glob(".manual-*")), [])

    def test_invalid_analysis_and_section_path_traversal_are_rejected(self):
        for changes in ({"source_sha256": "wrong"}, {"reviewed_units": [1, 1]}, {"reviewed_units": [3]},
                        {"sections": []}, {"units_total": 0}):
            invalid = {**self.analysis, **changes}
            with self.assertRaises(HarnessError):
                self.store(invalid)
        invalid = copy.deepcopy(self.analysis)
        invalid["sections"][0]["id"] = "../../outside"
        with self.assertRaises(HarnessError):
            self.store(invalid)

    def test_custom_cache_and_external_read_only_manual(self):
        self.cache = ManualCache(self.root, "knowledge/manuals")
        with tempfile.TemporaryDirectory(prefix="external-manual-") as folder:
            external = Path(folder) / "controller.png"
            original = b"opaque external image bytes"
            external.write_bytes(original)
            self.analysis["source_sha256"] = file_hash(external)
            stored = self.store(source=external)
            self.assertTrue(stored["generation"].startswith("knowledge/manuals/"))
            self.assertEqual(external.read_bytes(), original)
            self.assertEqual(len(self.cache.search("COM1")["matches"]), 1)

    def test_malformed_index_is_not_overwritten(self):
        self.cache.cache.mkdir(parents=True)
        self.cache.index_path.write_text("bad-json", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.store()
        self.assertEqual(self.cache.index_path.read_text(encoding="utf-8"), "bad-json")

    def test_cli_exit_codes_and_cache_lock(self):
        script = Path(__file__).with_name("manual_cache.py")
        args = [sys.executable, "-B", str(script), "status", "--project-root", str(self.root), "--source", "manual.pdf"]
        missing = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(missing.returncode, 1, missing.stderr)
        with exclusive_lock(self.cache.cache / "cache.lock"):
            blocked = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(blocked.returncode, 2)
        self.assertIn("lock", blocked.stderr)
        self.store()
        ready = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(ready.returncode, 0, ready.stderr)

    def test_search_limit_and_invalid_cache_paths(self):
        self.store()
        self.assertEqual(len(self.cache.search("example", limit=1)["matches"]), 1)
        with self.assertRaises(HarnessError):
            self.cache.search("", limit=1)
        with self.assertRaises(HarnessError):
            self.cache.search("COM1", limit=0)
        with self.assertRaises(HarnessError):
            ManualCache(self.root, "../outside")
        with self.assertRaises(HarnessError):
            ManualCache(self.root, ".")


if __name__ == "__main__":
    unittest.main()
