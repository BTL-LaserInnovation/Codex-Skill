# Blue Ocean execution harness

Read this reference for persistent progress, verification gates, correction loops, or handoff across sessions. The existing roadmap owns planned scope and acceptance criteria; the harness owns observed execution state and evidence references. Link the roadmap instead of copying its narrative. Small one-step work can retain the ordinary task record without initializing a ledger.

## Ownership and boundaries

- PM approves task contracts, limits, material changes and final acceptance. The system designer maps project-native commands and affected inputs into config. Developers implement and run checks. QC independently reviews actual results and records evidence. GUI designers provide applicable DR evidence.
- The helper does not call an LLM, launch agents, install dependencies, operate the UI, commit/push, or restart Codex outside a session. The existing coordinator schedules agents. `max_parallel_tasks` caps active task records, not CPU processes/model slots. One project-wide OS lock serializes ledger commands; verification checks run sequentially.
- Successful command exit proves only that check's result. Choose assertions of actual requirements. Compilation alone cannot satisfy an external-integration Debug runtime requirement. The helper checks evidence-file presence/integrity; PM/QC assess content and authority. A self-written approval file is not user approval or independent QC.
- Preserve skill-selection preferences, DR decisions and Computer Use confirmation. Configure `start` gates for applicable DR decisions and `accept` gates for QC/PM/UI/runtime evidence. Declined/blocked tests are not passed. There is no automatic exception override: PM/user documents an accepted exception and deliberately revises the contract before applicable verification is rerun.
- For manual-dependent work, use [persistent manual knowledge](manual-knowledge.md): reuse verified sections, record the source revision and include relevant project-local manual/cache inputs or an explicit freshness/coverage check. Cached documentation is an input to verification, not evidence that product behavior passed.

## Configure a project

Python 3.10+ is required; standard library only. `scripts/harness.ps1` forwards arguments to `python` on Windows PowerShell 5.1/PowerShell 7. `scripts/harness.py` can run directly on Windows, Linux or macOS. If Python is absent, report the prerequisite and use the existing task record; do not install it implicitly.

1. Use the established solution/project root. Copy `templates/harness-config.json` to `<ProjectRoot>/cfg/blue-ocean.harness.json`. Preserve existing config/state and `blue-ocean.preferences.json`.
2. Replace example tasks, acceptance text, solution/test paths and commands with the approved contract. The template is a C# example, not platform detection. C++/MFC projects must use their own MSBuild/test/Debug smoke commands and development environment. Check executable availability first. No restore, dependency installation or external side effect is authorized by the template.
3. Each task declares a unique lowercase `id`, `owner`, project-relative literal `scope` paths, observable `acceptance`, `depends_on` IDs, ordered required `checks`, and evidence `gates` (`id`, `stage`: `start` or `accept`). At least one check and one acceptance gate are required. Keep QC and PM gates; add DR/UI/runtime gates when applicable. For logic-only work, remove the example DR gate with a recorded not-applicable reason; never fabricate approval.
4. Each check declares a unique `id`, `argv` string array, project-relative `cwd`, and positive integer `timeout_seconds`. Arguments use `shell=False`. For shell syntax, explicitly invoke the project's trusted script/interpreter; never concatenate untrusted input. Processes inherit the caller environment. Secrets belong in the existing credential/environment mechanism, never in argv/config/evidence/logs.
5. Include all affected implementation inputs in `scope`: source, headers, build/project files, shared dependencies, tests and runtime configuration. Missing paths are tracked until created; scope paths are literal, not globs. Optional `snapshot_exclude` entries are project-relative, case-sensitive fnmatch patterns for generated outputs only. The example excludes nested `bin`, `obj` and `__pycache__`; add root-level patterns if needed. Do not exclude dependency inputs. Keep review artifacts outside source scope, preferably under the runtime evidence directory. Runtime files and `.git` are always excluded. Paths cannot escape the project; symlinks inside scope are rejected.
6. Positive integer `limits`: `max_attempts` counts verification batches including interrupted attempts; `max_task_seconds` counts wall-clock seconds since first start, including waiting/downtime; `max_parallel_tasks` caps `running`/`verification_pending` tasks. These do not impose token budgets or monitor unrelated agents. Exhausted limits require an explicit PM revision, not an automatic reset.

Runtime files live under `<ProjectRoot>/cfg/blue-ocean.harness/`:

```text
state.json        # Atomic ledger, task states/results and append-only history
ledger.lock       # OS lock; its file may safely remain after exit
logs/             # Per-task/per-attempt check stdout and stderr
evidence/         # Suggested location for team-supplied review/approval records
```

The helper creates state/logs, not approval files. Follow project retention rules; do not commit local state/logs/secrets by default or auto-edit `.gitignore`. Record config/state locations in the roadmap. Writes use a same-directory temporary file and replace. Malformed state is reported, never silently reset; explicitly back up and reconcile it.

## Commands

PowerShell example; replace paths and provide real review records before passing gates:

```powershell
$harnessScript = 'D:\Skills\blue-ocean\scripts\harness.ps1'
$projectRoot = 'D:\Projects\Product'
& $harnessScript init --project-root $projectRoot
& $harnessScript status --project-root $projectRoot
& $harnessScript start --project-root $projectRoot --task sample-change --evidence 'design-review=cfg/blue-ocean.harness/evidence/dr.md'
# Developer implements the approved scope using the existing workflow.
& $harnessScript verify --project-root $projectRoot --task sample-change
# QC and PM review the result and record decisions before acceptance.
& $harnessScript accept --project-root $projectRoot --task sample-change --evidence 'qc=cfg/blue-ocean.harness/evidence/qc.md' --evidence 'pm-acceptance=cfg/blue-ocean.harness/evidence/pm.md'
```

Direct equivalent: `python <SkillDir>/scripts/harness.py <action> --project-root <ProjectRoot>`. Optional `--config <relative-path>` chooses config but not ledger location: never mix separate plans against the same ledger. `--task` is required except for `init` and `status`.

| Action | Required state | Outcome |
|---|---|---|
| `init` | No ledger | Initializes tasks as `pending`; refuses overwrite |
| `status` | Existing ledger | Prints recorded state/history without fresh validation |
| `start` | `pending`, `needs_changes` | Checks dependencies/start gates, active-task cap and budget; enters `running` |
| `verify` | `running` | Runs required commands in order, recording command/cwd/times/exit/log hash; stops at first failure |
| `accept` | `verification_pending` | Requires current inputs/dependencies/logs/evidence; enters `complete` |
| `block --reason ...` | Any unfinished state | Records `blocked` and a concrete reason |
| `resume` | Any except `pending` | Reconciles work to `needs_changes`; requires review, `start` and new verification. A still-valid completed task stays complete |

Passing verification enters `verification_pending`, not `complete`. Failure/timeout enters `needs_changes`; depleted budgets enter `blocked`. Missing/unlaunchable commands enter `blocked`. Unrun checks are absent, never passed. Source/config changes during checks invalidate the batch; exclude only expected generated outputs. Timeout/handled keyboard interruption terminates the launched command tree where supported and preserves the pre-recorded attempt/logs. Use finite checks that do not detach background services.

A forced parent-process kill, machine failure or session loss may leave child checks running. Inspect the recorded `active_check` PID, start time, logs and actual process state before recovery; confirm identity before stopping any process. `resume` refuses a recorded interrupted check until `--reason` describes how the previous process tree was confirmed stopped and its outputs inspected. This acknowledgement is a manual recovery gate, not automated proof that the PID has exited. A crash between spawning and recording a child is also possible: always check for leftover builds/tests after forced termination, even without `active_check`. Never launch a duplicate verification while old work remains active.

Exit codes: `0` successful action, `1` verification did not pass, `2` invalid config/state/precondition or execution error, `130` keyboard interruption. Inspect stderr/state/logs before choosing the next step; do not repeat ineffective actions indefinitely.

## Correction and recovery

1. Route failed criteria, expected/actual behavior and logs to the owner. Correct within approved scope, then `start` and `verify`. QC reruns failed/affected checks and replaces superseded acceptance evidence. Counts/history persist.
2. At handoff, record the last check, next action, blocker and evidence in the existing task record. New sessions read that record, config and `status`, inspect current files, then use `resume`. Before relying on a stored completed task, use `resume` to check it remains current; `status` alone is not verification.
3. SHA-256 snapshots bind results to scoped file contents and the entire config. Source, criteria, commands, limits or dependency/evidence changes require revalidation. `resume` retains prior results in history, clears active verification and requires a new passing batch for unfinished/stale work. Crash recovery never fabricates a pass.
4. Task IDs cannot be silently added/removed. For a materially revised graph, explicitly archive config/state/logs using project retention rules and initialize the new plan, preserving earlier evidence and noting new budgets. Existing task contracts may change with PM decisions recorded and affected tasks reverified. Never reset/delete the ledger to evade a limit.
5. Final reports distinguish delivered work, passing checks, not-run/blocked tests, accepted exceptions and PM acceptance. Neither ledger existence nor an agent completion message proves product correctness.

## Validate harness changes

```text
python -m unittest discover -s skills/blue-ocean/scripts -p test_harness.py -v
python scripts/validate_skills.py
```

Tests use isolated projects and actual subprocesses. They do not run the sample product build, a live application or Computer Use.
