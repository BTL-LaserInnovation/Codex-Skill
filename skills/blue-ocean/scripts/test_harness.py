"""Behavioral regression tests using isolated projects and real child commands."""

import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).with_name("harness.py")
spec = importlib.util.spec_from_file_location("blue_ocean_harness", SCRIPT)
harness_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness_module)


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="blue-ocean-harness-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        (self.root / "cfg").mkdir()
        (self.root / "src").mkdir()
        (self.root / "src/input.txt").write_text("input", encoding="utf-8")
        self.config = {
            "schema_version": 1,
            "limits": {"max_attempts": 3, "max_task_seconds": 60, "max_parallel_tasks": 1},
            "checks": [{"id": "smoke", "argv": [sys.executable, "-c", "print('verified')"],
                        "cwd": ".", "timeout_seconds": 5}],
            "tasks": [{"id": "first", "owner": "developer", "scope": ["src"],
                       "acceptance": ["Smoke behavior verified"], "depends_on": [], "checks": ["smoke"],
                       "gates": [{"id": "dr", "stage": "start"}, {"id": "qc", "stage": "accept"},
                                 {"id": "pm", "stage": "accept"}]}],
        }
        self.write_config()
        self.evidence_dir = self.root / "cfg/blue-ocean.harness/evidence"
        self.evidence_dir.mkdir(parents=True)
        for name in ("dr", "qc", "pm"):
            (self.evidence_dir / f"{name}.md").write_text(f"Reviewed: {name}", encoding="utf-8")
        self.invoke("init")

    def write_config(self):
        (self.root / "cfg/blue-ocean.harness.json").write_text(json.dumps(self.config), encoding="utf-8")

    def invoke(self, action, *extra, expected=0, task="first"):
        args = [action, "--project-root", str(self.root)]
        if action not in ("init", "status"):
            args += ["--task", task]
        args += list(extra)
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = harness_module.main(args)
        self.assertEqual(code, expected, errors.getvalue() + output.getvalue())
        return output.getvalue(), errors.getvalue()

    def evidence(self, *gates):
        return [value for gate in gates for value in ("--evidence", f"{gate}=cfg/blue-ocean.harness/evidence/{gate}.md")]

    def start(self, task="first"):
        self.invoke("start", *self.evidence("dr"), task=task)

    def accept(self, task="first"):
        self.invoke("accept", *self.evidence("qc", "pm"), task=task)

    def state(self, task="first"):
        state = json.loads((self.root / "cfg/blue-ocean.harness/state.json").read_text(encoding="utf-8"))
        return state["tasks"][task]

    def add_second(self, dependencies):
        second = copy.deepcopy(self.config["tasks"][0])
        second.update(id="second", depends_on=dependencies)
        self.config["tasks"].append(second)
        self.write_config()
        # Set up a fresh isolated graph; production init refuses an existing ledger.
        (self.root / "cfg/blue-ocean.harness/state.json").unlink()
        self.invoke("init")

    def test_complete_requires_start_verification_and_all_evidence(self):
        self.invoke("start", expected=2)
        self.start()
        self.invoke("accept", *self.evidence("qc", "pm"), expected=2)
        self.invoke("verify")
        self.assertEqual(self.state()["status"], "verification_pending")
        self.invoke("accept", *self.evidence("qc"), expected=2)
        self.accept()
        self.assertEqual(self.state()["status"], "complete")
        self.invoke("resume")
        self.assertEqual(self.state()["status"], "complete")

    def test_failure_correction_and_retry_budget(self):
        self.config["checks"][0]["argv"] = [sys.executable, "-c", "from pathlib import Path; raise SystemExit(0 if Path('src/fix').exists() else 4)"]
        self.write_config()
        self.start()
        self.invoke("verify", expected=1)
        self.assertEqual(self.state()["status"], "needs_changes")
        (self.root / "src/fix").touch()
        self.start()
        self.invoke("verify")
        self.accept()
        self.assertEqual(self.state()["attempts"], 2)

    def test_exhaustion_stops_automatic_retries(self):
        self.config["limits"]["max_attempts"] = 1
        self.config["checks"][0]["argv"] = [sys.executable, "-c", "raise SystemExit(7)"]
        self.write_config()
        self.start()
        self.invoke("verify", expected=1)
        self.assertEqual(self.state()["status"], "blocked")
        self.invoke("resume")
        self.invoke("start", *self.evidence("dr"), expected=2)
        self.assertEqual(self.state()["attempts"], 1)

    def test_input_or_config_changes_invalidate_verification(self):
        self.start()
        self.invoke("verify")
        (self.root / "src/input.txt").write_text("changed", encoding="utf-8")
        self.invoke("accept", *self.evidence("qc", "pm"), expected=2)
        self.invoke("resume")
        self.start()
        self.invoke("verify")
        self.config["tasks"][0]["acceptance"].append("New criterion")
        self.write_config()
        self.invoke("accept", *self.evidence("qc", "pm"), expected=2)

    def test_log_and_approval_integrity(self):
        self.start()
        self.invoke("verify")
        log = self.root / self.state()["verification"]["checks"][0]["log"]
        log.write_text("replacement", encoding="utf-8")
        self.invoke("accept", *self.evidence("qc", "pm"), expected=2)
        self.invoke("resume")
        self.start()
        self.invoke("verify")
        (self.evidence_dir / "dr.md").write_text("changed decision", encoding="utf-8")
        self.invoke("accept", *self.evidence("qc", "pm"), expected=2)

    def test_completed_task_reopens_when_evidence_disappears(self):
        self.start()
        self.invoke("verify")
        self.accept()
        (self.evidence_dir / "qc.md").unlink()
        self.invoke("resume")
        self.assertEqual(self.state()["status"], "needs_changes")

    def test_dependencies_require_current_completion(self):
        self.add_second(["first"])
        self.invoke("start", *self.evidence("dr"), task="second", expected=2)
        self.start()
        self.invoke("verify")
        self.accept()
        self.start("second")
        (self.root / "src/input.txt").write_text("dependency changed", encoding="utf-8")
        self.invoke("verify", task="second", expected=2)

    def test_active_task_limit_and_block_reason(self):
        self.add_second([])
        self.start()
        self.invoke("start", *self.evidence("dr"), task="second", expected=2)
        self.invoke("block", expected=2)
        self.invoke("block", "--reason", "Waiting for endpoint")
        self.start("second")

    def test_timeout_and_missing_executable(self):
        self.config["checks"][0].update(argv=[sys.executable, "-c", "import time; time.sleep(30)"], timeout_seconds=1)
        self.write_config()
        self.start()
        self.invoke("verify", expected=1)
        self.assertEqual(self.state()["verification"]["checks"][0]["error"], "timeout")
        self.config["checks"][0]["argv"] = ["blue-ocean-nonexistent-executable"]
        self.write_config()
        self.start()
        self.invoke("verify", expected=1)
        self.assertEqual(self.state()["status"], "blocked")

    def test_mutation_during_verification_is_not_a_pass(self):
        self.config["checks"][0]["argv"] = [sys.executable, "-c", "from pathlib import Path; Path('src/input.txt').write_text('mutated')"]
        self.write_config()
        self.start()
        self.invoke("verify", expected=1)
        self.assertFalse(self.state()["verification"]["passed"])

    def test_generated_outputs_can_be_excluded(self):
        self.config["tasks"][0]["snapshot_exclude"] = ["src/obj/**"]
        self.config["checks"][0]["argv"] = [sys.executable, "-c", "from pathlib import Path; Path('src/obj').mkdir(exist_ok=True); Path('src/obj/generated').write_text('output')"]
        self.write_config()
        self.start()
        self.invoke("verify")
        self.accept()

    def test_resume_preserves_attempts_and_requires_reverification(self):
        self.start()
        self.invoke("verify")
        self.invoke("resume")
        self.assertEqual(self.state()["status"], "needs_changes")
        self.assertEqual(self.state()["attempts"], 1)
        self.invoke("accept", *self.evidence("qc", "pm"), expected=2)
        self.start()
        self.invoke("verify")
        self.accept()

    def test_wall_clock_budget_remains_exhausted_after_resume(self):
        self.start()
        path = self.root / "cfg/blue-ocean.harness/state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["tasks"]["first"]["started_at"] = "2000-01-01T00:00:00+00:00"
        path.write_text(json.dumps(state), encoding="utf-8")
        self.invoke("verify", expected=1)
        self.assertEqual(self.state()["status"], "blocked")
        self.invoke("resume")
        self.invoke("start", *self.evidence("dr"), expected=2)

    def test_init_and_corrupt_state_never_overwrite_existing_data(self):
        self.invoke("init", expected=2)
        path = self.root / "cfg/blue-ocean.harness/state.json"
        path.write_text("invalid-json", encoding="utf-8")
        self.invoke("status", expected=2)
        self.assertEqual(path.read_text(encoding="utf-8"), "invalid-json")

    def test_invalid_paths_cycles_and_empty_checks(self):
        self.config["tasks"][0]["scope"] = ["../outside"]
        self.write_config()
        self.invoke("status", expected=2)
        self.config["tasks"][0]["scope"] = ["src"]
        self.config["tasks"][0]["checks"] = []
        self.write_config()
        self.invoke("status", expected=2)
        self.config["tasks"][0]["checks"] = ["smoke"]
        self.add_second(["first"])
        self.config["tasks"][0]["depends_on"] = ["second"]
        self.write_config()
        self.invoke("status", expected=2)

    def test_os_lock_excludes_second_cli_writer(self):
        instance = harness_module.Harness(self.root)
        with harness_module.exclusive_lock(instance.runtime / "ledger.lock"):
            result = subprocess.run([sys.executable, str(SCRIPT), "start", "--project-root", str(self.root),
                                     "--task", "first", *self.evidence("dr")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("lock", result.stderr)
        self.assertEqual(self.state()["status"], "pending")

    def test_forced_parent_exit_requires_explicit_child_recovery(self):
        self.config["checks"][0].update(argv=[sys.executable, "-c", "import time; time.sleep(2)"], timeout_seconds=5)
        self.write_config()
        self.start()
        process = subprocess.Popen([sys.executable, str(SCRIPT), "verify", "--project-root", str(self.root),
                                    "--task", "first"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline and not self.state().get("active_check"):
                time.sleep(0.02)
            self.assertIsNotNone(self.state().get("active_check"))
            process.kill()
            process.wait(timeout=5)
            self.invoke("verify", expected=2)
            self.invoke("resume", expected=2)
            # The test child exits naturally; do not interfere with unrelated PIDs.
            time.sleep(2.1)
            self.invoke("resume", "--reason", "Confirmed bounded test child exited; inspected outputs")
            self.assertEqual(self.state()["status"], "needs_changes")
            self.assertEqual(self.state()["attempts"], 1)
            self.assertNotIn("active_check", self.state())
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)

    @unittest.skipUnless(os.name == "nt", "Windows PowerShell wrapper")
    def test_powershell_wrapper_forwards_arguments_and_exit_codes(self):
        wrapper = SCRIPT.with_suffix(".ps1")
        result = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(wrapper),
                                 "status", "--project-root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("pending", result.stdout)
        result = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(wrapper),
                                 "accept", "--project-root", str(self.root), "--task", "first"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
