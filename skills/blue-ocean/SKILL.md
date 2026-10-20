---
name: blue-ocean
description: "Coordinate C++/C# project delivery, implementation, GUI design and independent QC using existing project code and libraries. Use for Blue Ocean development coordination."
---

# Blue Ocean

Coordinate the approved outcome with proportionate planning, reuse and verified evidence. Preserve project conventions and explicit user choices. Report plans, progress and results in Korean unless requested otherwise; keep code and identifiers unchanged.

## Startup and shared constraints

- At invocation start, read [updates and authority](references/update-and-authority.md): check the configured GitHub source once and distinguish upstream updates from local or ahead-of-upstream changes. Preserve newer local features. Apply an explicitly requested update within its reviewed scope without asking the same permission again; otherwise obtain the required update decision before replacing an installation. Preserve a recoverable backup and validate the candidate.
- Before choosing supporting skills, load `<ProjectRoot>/cfg/blue-ocean.preferences.json` using the same established project root. Follow saved `user`/`pm` authority and per-skill allow/deny/defer decisions. With no saved or explicit choice, obtain the choice before dependent skill use; do not invent persistence or broaden access. Read the authority reference for storage and external installation details.
- Load applicable project-local rules before planning. Capture clearly continuing instructions and genuinely repeated corrections through [local skills](references/local-skills.md), retaining scope, evidence, opt-outs and task exceptions. Reuse the [local template](templates/local-skill/SKILL.md) and [registry](templates/local-skill/references/rules.json); do not turn manuals or logs into user instructions.
- Keep every Blue Ocean role on **GPT-6.1 Sol** (`gpt-6.1-sol`). Before spawning or substantial parallel work, read [agents and resources](references/agents-and-resources.md). Verify model availability; no silent substitution. Separate independent work, sequence shared-file edits, and preserve independent QC where feasible. Simple work may combine roles with honest attribution.
- Select the first sufficient option: omit unnecessary work, reuse project code, use the language standard library, native platform capability, an installed dependency, then a small maintainable implementation. Preserve required validation, error/data-loss handling, security, accessibility, observability and tests. Search compatible existing variables before adding new ones.
- Preserve approved roadmap, design review (DR), runtime and QC gates. An evidence file, successful command or cached summary is not by itself proof of acceptance or user authorization. Continue independent authorized work while a real decision blocks another stage.

## Read the applicable workflow

These documents are conditional routes, not a startup reading checklist. Read relevant sections before the affected decision. A routine, fully specified correction can use a brief task record and relevant checks; it does not need unrelated roles, repo-wide discovery or a new ledger. This proportionality never removes applicable DR, external-integration Debug, Computer Use confirmation or independent acceptance requirements.

| Current work | Read and apply |
| --- | --- |
| Substantial implementation, architecture, feature choices, specialist handoffs | [Delivery](references/delivery.md): roles, PM synthesis, task plans, ownership and acceptance. |
| Source changes, C++/MFC reuse or new dependencies | [Implementation](references/implementation.md): Mocha search before choosing a new implementation, naming rules, native builds, library impact, Debug integration and QC. Use only affected diagram/documentation areas. |
| UI layout, controls, interactions or final real-UI verification | [GUI workflow](references/gui-workflow.md): visual proposal and user direction before implementation, WPF designer/MFC DC defaults, concrete Computer Use test plan and explicit execution scope. |
| Multi-step execution, correction loops or cross-session recovery | [Harness](references/harness.md) and [config template](templates/harness-config.json). Keep state under `cfg/blue-ocean.harness/`; use `resume` after interruption and revalidate changed inputs. Passing checks enter `verification_pending`; acceptance needs current QC/PM evidence. |
| PDF/image/manual evidence | [Manual knowledge](references/manual-knowledge.md) and [analysis template](templates/manual-analysis.json). Check `scripts/manual_cache.py status` first; reuse verified covered sections and re-read only changed, missing or uncertain evidence. |
| Windows/WSL checkout, parallel build setup, model/speed settings or tool integration changes | [Execution environment](references/execution-environment.md): actual checkout, build paths, tool availability and recovery checks. |
| Updating this skill, its routing, model or tools | [Skill evaluation](references/skill-evaluation.md) and [cases](templates/skill-evaluation-cases.json): structural checks plus representative decisions in the target client. |
| Explicit code cleanup or CI maintenance task | Maintenance section in [execution environment](references/execution-environment.md); substantiate removals and run affected validation. |

## Completion

Developers run proportionate project-native checks; external library/SDK/API integration requires actual Debug runtime evidence. QC records observed expected/actual outcomes and re-verifies failures after correction. Prepare the runnable build and concrete real-UI scenarios before requesting Computer Use execution confirmation; reuse explicit authorization for the same scope. Mark unavailable or declined checks blocked/not run, never passed. PM accepts only after required evidence or a documented authorized exception, then reports delivered scope, changed files, checks and remaining limitations.
