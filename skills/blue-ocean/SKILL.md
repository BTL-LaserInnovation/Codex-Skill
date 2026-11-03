---
name: blue-ocean
description: "Coordinate C++/C# project delivery, implementation, GUI design and independent QC using existing project code and libraries. Use for Blue Ocean development coordination."
---

# Blue Ocean

Deliver the approved outcome using existing project conventions and code. Report plans, progress and results in Korean unless requested otherwise; preserve code and identifiers.

## Startup and shared constraints

- At invocation start, follow [updates and authority](references/update-and-authority.md): check the configured upstream once, preserve local features, and apply only an authorized update.
- Before selecting supporting skills, load `<ProjectRoot>/cfg/blue-ocean.preferences.json` and follow its authority and per-skill decisions. With no saved or explicit choice, obtain the choice before dependent skill use.
- Actively use an installed `project-symbol-guide` for project analysis and implementation under its standing authorization; follow later restrictions and the [symbol-guide workflow](references/implementation.md#project-symbol-guide). This does not authorize other skills or new project functions.
- Load applicable project-local rules before planning. Keep rules and supporting resources under `<ProjectRoot>/localrule/`; use [local skills](localrule/local-skills.md) for continuing instructions, repeated corrections and migration. Preserve project rules during shared skill updates.
- Use **GPT-6.1 Sol** (`gpt-6.1-sol`) for the PM only and **GPT-6.1 Terra** (`gpt-6.1-terra`) for every other Blue Ocean agent. Follow [agents and resources](references/agents-and-resources.md) before spawning or substantial parallel work; do not silently substitute models.
- For every UI change, including small corrections, present a visual proposal and obtain explicit user confirmation before implementation. Apply the [UI confirmation gate](references/gui-workflow.md#ui-proposal-and-user-confirmation-before-implementation); PM approval does not replace user confirmation.
- Choose the first sufficient option: omit unnecessary work, reuse project code, use the language standard library, native platform capability, an installed dependency, then a small maintainable implementation. Preserve required validation, error/data-loss handling, security, accessibility, observability and tests.

## Read the applicable workflow

Read only the relevant sections before the affected decision. A fully specified routine correction can use a brief task record and affected checks without unrelated roles, repo-wide discovery or a new ledger. This never removes applicable design review (DR), Debug runtime, Computer Use confirmation or independent acceptance requirements. Reference commands and templates are relative to the installed skill root.

| Current work | Read and apply |
| --- | --- |
| Substantial implementation, architecture, feature choices or specialist handoffs | [Delivery](references/delivery.md): roles, brainstorming, roadmap, ownership and acceptance. |
| Work orders, progress, token estimates or completion forecasts | [PM control](references/pm-control.md): reporting, historical calibration, allowances and dependency-aware finish windows. |
| Project analysis, source changes, C++/MFC reuse or dependencies | [Implementation](references/implementation.md): symbols, Mocha, naming, layout, sample-first logic and Debug integration. |
| UI design, controls, interactions or real-UI verification | [GUI workflow](references/gui-workflow.md): proposal confirmation, handoff, platform conventions and Computer Use execution. |
| Multi-step execution, correction loops or cross-session recovery | [Harness](references/harness.md): persistent state, verification, limits and recovery. |
| PDF/image/manual evidence | [Manual knowledge](references/manual-knowledge.md): check cache status first; reuse verified covered sections. |
| Windows/WSL checkout, parallel builds, model settings, integrations or requested code/CI cleanup | [Execution environment](references/execution-environment.md). |
| Changes to this skill, routing, models or tools | [Skill evaluation](references/skill-evaluation.md) and [cases](templates/skill-evaluation-cases.json). |

## Completion

Developers run affected project-native checks; QC records expected/actual results and re-verifies corrections. Mark unavailable or declined checks blocked/not run. PM accepts only with current required evidence or a documented authorized exception, then reports delivered scope, changed files, checks and remaining limitations.
