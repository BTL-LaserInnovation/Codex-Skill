---
name: blue-ocean
description: "Coordinate a multi-agent C++ or C# software project from PM direction through architecture, implementation, quality verification, and final reporting."
---

# Blue Ocean

Use this skill for software-development work that benefits from a clear, multi-agent delivery process. It covers C++, C#, and other requested platforms; it does not prescribe a framework or alter the user's product requirements.

## Roles and ownership

Establish these roles before beginning substantial work:

- **Project manager (PM):** clarifies the requested outcome, defines scope and acceptance criteria, chooses the delivery direction, approves the roadmap, assigns work, and delivers the final report.
- **System designer:** turns the PM direction into an implementable roadmap: architecture, interfaces, dependencies, milestones, risks, and validation strategy. Searches the approved skill catalog or available local skills for work-relevant capabilities, selects the minimum suitable skills, and assigns their use to the GUI designer and software developer. Tracks whether implementation remains aligned with the roadmap.
- **GUI designer:** defines user flows, screen layouts, component states, visual hierarchy, and interaction rules for user-facing software. Produces an implementable handoff that is consistent with the system design and records usability or accessibility requirements that affect implementation.
- **Software developer:** implements the approved work in the requested language and reports completed work, tests, and blockers.
- **Program review and verification QC:** independently reviews changes against the roadmap and acceptance criteria, performs or requests proportionate validation, and records defects or release risks.

Assign one responsible agent per role. An agent may fill more than one role only when resources are limited; preserve QC independence whenever feasible.

## Operating workflow

1. The PM converts the request into a concise objective, constraints, acceptance criteria, and language/platform decision. Identify missing decisions that materially affect scope before implementation.
2. The system designer writes a roadmap with deliverables, ordering, owners, dependencies, technical decisions, risks, and verification points. It searches the approved skill catalog or available local skills for each specialist task, records the selected skill, intended user, purpose, and any prerequisite, then assigns the skill to the GUI designer or software developer as applicable. For user-facing features, include user-review checkpoints in the roadmap and have the GUI designer supply the user flow and screen/design handoff before the relevant implementation is assigned. Keep these artifacts in the project when the task has persistent files; otherwise present them in the working response.
3. The PM reviews the roadmap, resolves scope conflicts, and assigns the approved work to the relevant agents. Do not begin out-of-scope implementation merely because it appears useful.
4. Before implementation, the GUI designer and software developer each prepare a task plan covering the affected components or screens, existing-code references, implementation approach, and validation. The system designer confirms that plan against the roadmap before the assigned work proceeds.
5. Developers implement their assigned items and run relevant builds, tests, or checks. For GUI work, they use the approved design handoff and report feasibility issues or design deviations promptly rather than silently changing the design. At each planned GUI review checkpoint, the GUI designer presents the current screen, prototype, or implementation to the user, captures feedback and confirmation, and updates the handoff before the next affected implementation stage.
6. The system designer checks roadmap alignment at meaningful milestones. The GUI designer reviews implemented screens against the approved interaction and visual requirements. QC reviews intermediate results as well as the final change, logs findings with severity and reproducible evidence, and routes defects back to the owner.
7. When QC does not pass a check, record the failed criterion, evidence, owner, and required correction. The responsible GUI designer or developer supplements and reworks the affected result, then reruns the relevant validation. QC re-verifies the failed criterion and repeats this correction loop until it passes or the PM/user accepts a documented exception.
8. Obtain PM acceptance against the original criteria after all required QC checks pass or accepted exceptions are recorded.
9. The PM produces a final report containing delivered scope, files or components changed, validation performed and outcomes, open risks or follow-ups, and any intentional deviations.

## Coordination rules

- Use parallel work only for independent tasks. Keep architectural decisions and shared-file edits sequenced to prevent conflicts.
- Treat the approved roadmap as the source of truth. Update it when the PM accepts a material scope, design, or schedule change.
- The system designer may assign an already available, project-relevant skill to the GUI designer or software developer. Assignments grant use of the skill for the named task; they do not grant external-service access, new credentials, or permission to install dependencies.
- The system designer provides each assigned GUI designer and software developer with the appropriate available tools: relevant skills, project-native build and test commands, design-system resources, and the locations of applicable existing code. This does not bypass authorization required for external services, credentials, or new dependencies.
- For coding-development work, the system designer checks whether the Superpowers skill is available and may assign it to the software developer when its workflow is relevant. Use it as a supporting reference; the approved roadmap, project conventions, and acceptance criteria remain authoritative. If Superpowers is unavailable, continue with the project's existing tools and practices rather than treating its installation as implicit.
- Before assigning implementation guidance, the system designer searches the existing codebase for comparable screens, components, functions, variables, and data flows, and recommends the relevant references to the responsible agent.
- If the requester identifies reference code or a reference project, inspect its structure and how its functions are used, then use that evidence when defining the implementation plan and compatibility guidance.
- Direct GUI and software work to follow the established project conventions as closely as possible, including architecture, naming, formatting, control flow, error handling, and project-native tools. Deviations require a recorded technical reason and system-designer confirmation.
- Do not add variables without a demonstrated need. Before introducing one, search for an existing value that safely serves the same purpose; reuse it when its scope, lifetime, and meaning are compatible, even if its name differs. Do not reuse a value when that would obscure its meaning or create unsafe coupling.
- When no suitable approved skill exists, the system designer reports the gap and proposes a skill or creation task to the PM. Obtain PM/user authorization before installing a skill, connecting an external service, or introducing a material dependency.
- Record a skill assignment in the roadmap with its target role and purpose so QC can verify that its constraints were followed.
- Treat an approved GUI handoff as the source of truth for screens and interactions. Changes that affect user flow, layout, component behavior, or accessibility require GUI-designer review and PM acceptance when they alter scope.
- Keep user GUI-review feedback and confirmations with the design handoff. A material unresolved user decision blocks the affected GUI stage until the user or PM provides direction.
- For C++ and C#, choose the project-native build and test commands when present. Do not introduce a new build system or dependencies without user authorization.
- QC must distinguish verified defects from suggestions. A release-blocking finding needs evidence, expected versus actual behavior, and a clear owner.
- A failed QC check is not complete until QC records a passing re-verification or the PM/user accepts a documented exception with its remaining risk.
- Unless the user requests another language, present roadmap summaries, task plans, GUI-review notes, QC findings, progress reports, and final results in Korean. Keep source code, commands, paths, API names, and other identifiers unchanged, and explain them in Korean where clarification is needed.
- If a required decision, credential, external service, or acceptance criterion is unavailable, report the blocker to the PM/user with the smallest decision needed to continue.
