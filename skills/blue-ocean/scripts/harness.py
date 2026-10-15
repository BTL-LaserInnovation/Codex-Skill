#!/usr/bin/env python3
"""Project-local Blue Ocean task ledger and verification gates (Python 3.10+)."""

from __future__ import annotations

import argparse
import contextlib
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


class HarnessError(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def file_hash(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def within(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise HarnessError(f"Expected a project-relative path: {relative!r}")
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or ".git" in path.relative_to(root).parts:
        raise HarnessError(f"Path leaves project or targets .git: {relative}")
    return path


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextlib.contextmanager
def exclusive_lock(path):
    # OS locks release on process death; a leftover file is not a stale lock.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise HarnessError("Another harness command owns the project lock") from error
        try:
            if path.stat().st_size == 0:
                stream.write(b"0")
                stream.flush()
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


class Harness:
    def __init__(self, root, config="cfg/blue-ocean.harness.json"):
        self.root = Path(root).resolve()
        if not self.root.is_dir():
            raise HarnessError("Project root does not exist")
        self.config_path = within(self.root, config)
        self.runtime = within(self.root, "cfg/blue-ocean.harness")
        self.state_path = self.runtime / "state.json"
        self.config = read_json(self.config_path)
        self.validate_config()
        self.config_hash = digest(self.config)
        self.state = None

    def validate_config(self):
        config = self.config
        if config.get("schema_version") != 1:
            raise HarnessError("Unsupported config schema_version")
        limits = config.get("limits", {})
        for key in ("max_attempts", "max_task_seconds", "max_parallel_tasks"):
            if type(limits.get(key)) is not int or limits[key] < 1:
                raise HarnessError(f"limits.{key} must be a positive integer")
        checks = config.get("checks")
        tasks = config.get("tasks")
        if not isinstance(checks, list) or not isinstance(tasks, list) or not tasks:
            raise HarnessError("Provide checks and a nonempty tasks list")
        self.checks = self.index(checks)
        self.tasks = self.index(tasks)
        for check in checks:
            argv = check.get("argv")
            if not isinstance(argv, list) or not argv or any(not isinstance(x, str) or not x for x in argv):
                raise HarnessError(f"{check['id']}: argv must be a nonempty string array")
            if not within(self.root, check.get("cwd", ".")).is_dir():
                raise HarnessError(f"{check['id']}: cwd does not exist")
            if type(check.get("timeout_seconds")) is not int or check["timeout_seconds"] < 1:
                raise HarnessError(f"{check['id']}: invalid timeout_seconds")
        for task in tasks:
            for key in ("scope", "acceptance", "checks", "gates"):
                if not isinstance(task.get(key), list) or not task[key]:
                    raise HarnessError(f"{task['id']}: {key} must not be empty")
            if not isinstance(task.get("owner"), str) or not task["owner"].strip():
                raise HarnessError(f"{task['id']}: owner is required")
            if any(not isinstance(x, str) or not x.strip() for x in task["acceptance"]):
                raise HarnessError(f"{task['id']}: invalid acceptance criteria")
            for scope in task["scope"]:
                path = within(self.root, scope)
                if path.is_relative_to(self.runtime):
                    raise HarnessError("Task scope must not target harness runtime files")
            if not isinstance(task.get("snapshot_exclude", []), list) or any(
                not isinstance(pattern, str) or not pattern for pattern in task.get("snapshot_exclude", [])
            ):
                raise HarnessError(f"{task['id']}: snapshot_exclude must be a string list")
            if not isinstance(task.get("depends_on"), list):
                raise HarnessError(f"{task['id']}: depends_on must be a list")
            if any(x not in self.tasks or x == task["id"] for x in task["depends_on"]):
                raise HarnessError(f"{task['id']}: unknown or self dependency")
            if any(x not in self.checks for x in task["checks"]):
                raise HarnessError(f"{task['id']}: unknown check")
            gates = self.index(task["gates"])
            if any(gate.get("stage") not in ("start", "accept") for gate in gates.values()):
                raise HarnessError(f"{task['id']}: gate stage must be start or accept")
            if not any(gate["stage"] == "accept" for gate in gates.values()):
                raise HarnessError(f"{task['id']}: an acceptance evidence gate is required")
        visiting, visited = set(), set()

        def visit(task_id):
            if task_id in visiting:
                raise HarnessError("Task dependency cycle")
            if task_id in visited:
                return
            visiting.add(task_id)
            for dependency in self.tasks[task_id]["depends_on"]:
                visit(dependency)
            visiting.remove(task_id)
            visited.add(task_id)

        for task_id in self.tasks:
            visit(task_id)

    @staticmethod
    def index(items):
        result = {}
        for item in items:
            key = item.get("id")
            if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", key) or key in result:
                raise HarnessError("IDs must be unique lowercase letters, digits and hyphens")
            result[key] = item
        return result

    def load(self):
        self.state = read_json(self.state_path)
        if self.state.get("schema_version") != 1 or self.state.get("project_root") != str(self.root):
            raise HarnessError("State schema or project root mismatch")
        if set(self.state.get("tasks", {})) != set(self.tasks):
            raise HarnessError("Task IDs changed; reconcile the plan in a new config/state project before continuing")

    def save(self, task_id, event, detail):
        self.state["updated_at"] = now()
        self.state["history"].append({"at": now(), "task": task_id, "event": event, "detail": detail})
        atomic_json(self.state_path, self.state)

    def initialize(self):
        if self.state_path.exists():
            raise HarnessError("State already exists; use status/resume, never overwrite it")
        self.state = {"schema_version": 1, "project_root": str(self.root), "tasks": {}, "history": []}
        for task_id in self.tasks:
            self.state["tasks"][task_id] = {"status": "pending", "attempts": 0, "started_at": None,
                                           "verification": None, "evidence": {}}
        self.save(None, "init", {"config_hash": self.config_hash})

    def fingerprint(self, task_id):
        files = {}
        for scope in self.tasks[task_id]["scope"]:
            source = within(self.root, scope)
            candidates = source.rglob("*") if source.is_dir() else [source]
            if not source.exists():
                files[scope] = "missing"
            for path in candidates:
                relative = path.relative_to(self.root)
                if ".git" in relative.parts or path.is_relative_to(self.runtime):
                    continue
                if any(fnmatch.fnmatchcase(relative.as_posix(), pattern)
                       for pattern in self.tasks[task_id].get("snapshot_exclude", [])):
                    continue
                if path.is_symlink() or not path.resolve().is_relative_to(self.root):
                    raise HarnessError(f"Symlinks are not supported in task scope: {relative}")
                if path.is_file():
                    files[relative.as_posix()] = file_hash(path)
        return digest({"files": files, "config": self.config_hash})

    def current(self, task_id):
        return self.state["tasks"][task_id]

    def remaining(self, task_id):
        started = self.current(task_id)["started_at"]
        elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(started)).total_seconds() if started else 0
        return self.config["limits"]["max_task_seconds"] - elapsed

    def evidence(self, task_id, stage, supplied):
        task = self.current(task_id)
        known = {gate["id"]: gate for gate in self.tasks[task_id]["gates"]}
        for value in supplied:
            gate, separator, relative = value.partition("=")
            if not separator or gate not in known or known[gate]["stage"] != stage:
                raise HarnessError(f"Expected --evidence gate-id=project-relative-file for {stage}: {value}")
            path = within(self.root, relative)
            if not path.is_file() or path.stat().st_size == 0:
                raise HarnessError(f"Missing/empty evidence: {relative}")
            task["evidence"][gate] = {"path": relative, "sha256": file_hash(path),
                                      "recorded_at": now()}
        for gate in known.values():
            if gate["stage"] != stage:
                continue
            record = task["evidence"].get(gate["id"])
            if not record:
                raise HarnessError(f"Required {stage} evidence: {gate['id']}")
            path = within(self.root, record["path"])
            if not path.is_file() or file_hash(path) != record["sha256"]:
                raise HarnessError(f"Evidence changed/missing: {gate['id']}")

    def dependencies(self, task_id):
        for dependency in self.tasks[task_id]["depends_on"]:
            record = self.current(dependency)
            if record["status"] != "complete" or record.get("accepted_fingerprint") != self.fingerprint(dependency):
                raise HarnessError(f"Dependency incomplete or changed: {dependency}; resume and revalidate it")
            self.evidence(dependency, "start", [])
            self.evidence(dependency, "accept", [])
            self.validate_verification(dependency)
            self.dependencies(dependency)

    def validate_verification(self, task_id):
        verification = self.current(task_id).get("verification")
        if not verification or not verification.get("passed") or verification["fingerprint"] != self.fingerprint(task_id):
            raise HarnessError("Verification is missing or stale; resume and reverify")
        if [check["id"] for check in verification["checks"]] != self.tasks[task_id]["checks"]:
            raise HarnessError("Required verification checks are missing")
        for check in verification["checks"]:
            path = within(self.root, check["log"])
            if check["status"] != "passed" or not path.is_file() or file_hash(path) != check["log_sha256"]:
                raise HarnessError("Verification log changed/missing; resume and reverify")

    def start(self, task_id, supplied):
        task = self.current(task_id)
        if task["status"] not in ("pending", "needs_changes"):
            raise HarnessError("start requires pending or needs_changes; use resume for interrupted work")
        self.dependencies(task_id)
        self.evidence(task_id, "start", supplied)
        if self.remaining(task_id) <= 0 or task["attempts"] >= self.config["limits"]["max_attempts"]:
            raise HarnessError("Task execution budget exhausted; PM must revise limits/plan explicitly")
        active = sum(value["status"] in ("running", "verification_pending") for key, value in self.state["tasks"].items() if key != task_id)
        if active >= self.config["limits"]["max_parallel_tasks"]:
            raise HarnessError("max_parallel_tasks reached")
        task["status"] = "running"
        task["started_at"] = task["started_at"] or now()
        task["verification"] = None
        task["evidence"] = {key: value for key, value in task["evidence"].items()
                            if any(gate["id"] == key and gate["stage"] == "start" for gate in self.tasks[task_id]["gates"])}
        self.save(task_id, "start", {"fingerprint": self.fingerprint(task_id)})

    @staticmethod
    def stop_process(process):
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, check=False)
        else:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
        if process.poll() is None:
            process.kill()
        process.wait(timeout=10)

    def run_check(self, task_id, check, attempt):
        relative = f"logs/{task_id}-{attempt}-{check['id']}.log"
        log = self.runtime / relative
        log.parent.mkdir(parents=True, exist_ok=True)
        result = {"id": check["id"], "argv": check["argv"], "cwd": check.get("cwd", "."),
                  "started_at": now(), "log": log.relative_to(self.root).as_posix()}
        timeout = min(check["timeout_seconds"], max(0.01, self.remaining(task_id)))
        with log.open("wb") as stream:
            options = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
            try:
                process = subprocess.Popen(check["argv"], cwd=within(self.root, check.get("cwd", ".")),
                                           stdout=stream, stderr=subprocess.STDOUT, shell=False, **options)
            except OSError as error:
                stream.write(str(error).encode("utf-8"))
                result.update(status="blocked", error=str(error), exit_code=None)
            else:
                self.current(task_id)["active_check"] = {"pid": process.pid, "id": check["id"], "started_at": now()}
                try:
                    self.save(task_id, "check-start", self.current(task_id)["active_check"])
                    result["exit_code"] = process.wait(timeout=timeout)
                    result["status"] = "passed" if result["exit_code"] == 0 else "failed"
                except subprocess.TimeoutExpired:
                    self.stop_process(process)
                    result.update(status="failed", error="timeout", exit_code=process.returncode)
                except BaseException:
                    self.stop_process(process)
                    self.current(task_id).pop("active_check", None)
                    self.save(task_id, "check-interrupted", {"id": check["id"]})
                    raise
                self.current(task_id).pop("active_check", None)
        result["finished_at"] = now()
        result["log_sha256"] = file_hash(log)
        return result

    def verify(self, task_id):
        task = self.current(task_id)
        if task["status"] != "running":
            raise HarnessError("verify requires running; use start/resume first")
        if task.get("active_check"):
            raise HarnessError("An interrupted check may still be active; inspect it and use resume --reason first")
        self.dependencies(task_id)
        self.evidence(task_id, "start", [])
        if task["attempts"] >= self.config["limits"]["max_attempts"] or self.remaining(task_id) <= 0:
            task.update(status="blocked", reason="Execution budget exhausted")
            self.save(task_id, "blocked", {"reason": task["reason"]})
            return False
        before = self.fingerprint(task_id)
        task["attempts"] += 1
        task["verification"] = {"fingerprint": before, "checks": [], "passed": False}
        self.save(task_id, "verify-start", {"attempt": task["attempts"]})
        for check_id in self.tasks[task_id]["checks"]:
            if self.remaining(task_id) <= 0:
                break
            result = self.run_check(task_id, self.checks[check_id], task["attempts"])
            task["verification"]["checks"].append(result)
            self.save(task_id, "check", result)
            if result["status"] != "passed":
                break
        results = task["verification"]["checks"]
        passed = (len(results) == len(self.tasks[task_id]["checks"]) and all(x["status"] == "passed" for x in results)
                  and before == self.fingerprint(task_id) and self.remaining(task_id) > 0)
        task["verification"]["passed"] = passed
        exhausted = task["attempts"] >= self.config["limits"]["max_attempts"] or self.remaining(task_id) <= 0
        task["status"] = "verification_pending" if passed else "blocked" if exhausted or any(x["status"] == "blocked" for x in results) else "needs_changes"
        self.save(task_id, "verify-end", {"status": task["status"], "passed": passed})
        return passed

    def accept(self, task_id, supplied):
        task = self.current(task_id)
        verification = task.get("verification")
        if task["status"] != "verification_pending" or not verification or not verification["passed"]:
            raise HarnessError("accept requires passing verification_pending")
        if verification["fingerprint"] != self.fingerprint(task_id):
            raise HarnessError("Inputs/config changed after verification; resume and verify again")
        self.dependencies(task_id)
        self.evidence(task_id, "start", [])
        self.evidence(task_id, "accept", supplied)
        self.validate_verification(task_id)
        task.update(status="complete", accepted_fingerprint=verification["fingerprint"])
        self.save(task_id, "accept", {"evidence": task["evidence"]})

    def resume(self, task_id, reason=None):
        task = self.current(task_id)
        before = task["status"]
        if before == "pending":
            raise HarnessError("Pending task: use start")
        active = task.get("active_check")
        if active and (not reason or not reason.strip()):
            raise HarnessError(f"Interrupted check may still be running: {active}. Inspect/stop the old check tree, then resume --reason with the recovery evidence")
        fingerprint = self.fingerprint(task_id)
        verification = task.get("verification")
        if before == "complete":
            try:
                self.dependencies(task_id)
                self.evidence(task_id, "start", [])
                self.evidence(task_id, "accept", [])
                self.validate_verification(task_id)
                valid = task.get("accepted_fingerprint") == fingerprint
            except HarnessError:
                valid = False
            if valid:
                return
        task["status"] = "needs_changes"
        task["verification"] = None
        task.pop("active_check", None)
        self.save(task_id, "resume", {"previous_status": before, "current_fingerprint": fingerprint,
                                      "previous_verification": verification, "recovery_reason": reason,
                                      "interrupted_check": active, "next_action": "Review current files, then start and verify"})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "status", "start", "verify", "accept", "block", "resume"))
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--config", default="cfg/blue-ocean.harness.json")
    parser.add_argument("--task")
    parser.add_argument("--evidence", action="append", default=[], help="gate-id=project-relative-file")
    parser.add_argument("--reason")
    args = parser.parse_args(argv)
    try:
        harness = Harness(args.project_root, args.config)
        # One writer/verifier per project, including across concurrent CLI processes.
        with exclusive_lock(harness.runtime / "ledger.lock"):
            if args.action == "init":
                harness.initialize()
            else:
                harness.load()
                if args.action != "status" and args.task not in harness.tasks:
                    raise HarnessError("Provide a known --task ID")
                if args.action == "start":
                    harness.start(args.task, args.evidence)
                elif args.action == "verify":
                    if not harness.verify(args.task):
                        print(json.dumps(harness.current(args.task), ensure_ascii=False, indent=2))
                        return 1
                elif args.action == "accept":
                    harness.accept(args.task, args.evidence)
                elif args.action == "resume":
                    harness.resume(args.task, args.reason)
                elif args.action == "block":
                    if not args.reason or not args.reason.strip():
                        raise HarnessError("block requires --reason")
                    if harness.current(args.task)["status"] == "complete":
                        raise HarnessError("Completed task: resume/revalidate before blocking")
                    harness.current(args.task).update(status="blocked", reason=args.reason)
                    harness.save(args.task, "blocked", {"reason": args.reason})
            print(json.dumps(harness.state, ensure_ascii=False, indent=2))
        return 0
    except (HarnessError, OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(f"Harness error: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Interrupted; state preserved. Review files and use resume.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
