---
name: blue-ocean
description: "Coordinate a multi-agent C++ or C# software project from PM direction through architecture, implementation, quality verification, and final reporting."
---

# Blue Ocean

Use this skill for software-development work that benefits from a clear, multi-agent delivery process. It covers C++, C#, and other requested platforms; it does not prescribe a framework or alter the user's product requirements.

## Roles and ownership

Establish these roles before beginning substantial work:

- **Project manager (PM):** clarifies the requested outcome, defines scope and acceptance criteria, chooses the delivery direction, approves the roadmap, assigns work, and delivers the final report.
- **System designer:** turns the PM direction into an implementable roadmap: architecture, interfaces, dependencies, milestones, risks, and validation strategy. Tracks whether implementation remains aligned with the roadmap.
- **Software developer:** implements the approved work in the requested language and reports completed work, tests, and blockers.
- **Program review and verification QC:** independently reviews changes against the roadmap and acceptance criteria, performs or requests proportionate validation, and records defects or release risks.

Assign one responsible agent per role. An agent may fill more than one role only when resources are limited; preserve QC independence whenever feasible.

## Operating workflow

1. The PM converts the request into a concise objective, constraints, acceptance criteria, and language/platform decision. Identify missing decisions that materially affect scope before implementation.
2. The system designer writes a roadmap with deliverables, ordering, owners, dependencies, technical decisions, risks, and verification points. Keep it in a project artifact when the task has persistent files; otherwise present it in the working response.
3. The PM reviews the roadmap, resolves scope conflicts, and assigns the approved work to the relevant agents. Do not begin out-of-scope implementation merely because it appears useful.
4. Developers implement their assigned items and run relevant builds, tests, or checks. Report deviations from the roadmap promptly rather than silently changing the design.
5. The system designer checks roadmap alignment at meaningful milestones. QC reviews intermediate results as well as the final change, logs findings with severity and reproducible evidence, and routes defects back to the owner.
6. Resolve verified defects, repeat only the checks affected by the correction, and obtain PM acceptance against the original criteria.
7. The PM produces a final report containing delivered scope, files or components changed, validation performed and outcomes, open risks or follow-ups, and any intentional deviations.

## Coordination rules

- Use parallel work only for independent tasks. Keep architectural decisions and shared-file edits sequenced to prevent conflicts.
- Treat the approved roadmap as the source of truth. Update it when the PM accepts a material scope, design, or schedule change.
- For C++ and C#, choose the project-native build and test commands when present. Do not introduce a new build system or dependencies without user authorization.
- QC must distinguish verified defects from suggestions. A release-blocking finding needs evidence, expected versus actual behavior, and a clear owner.
- If a required decision, credential, external service, or acceptance criterion is unavailable, report the blocker to the PM/user with the smallest decision needed to continue.
