# Development delivery

## Roles and ownership

Establish these roles for substantial work:

| Role | Responsibility |
| --- | --- |
| Project manager (PM) | Scope, acceptance criteria, brainstorming brief/synthesis, roadmap approval, assignment, integration and final report. Owns forecasts and replanning under [PM control](pm-control.md). |
| System designer | Architecture, interfaces, dependencies, roadmap, existing-code inventory, supporting-skill selection and roadmap alignment. |
| GUI designer | Existing-screen audit, visual/interaction design, user review and implementation handoff under [GUI workflow](gui-workflow.md). |
| Software developer | Reuse-based implementation, integration and evidence under [implementation conventions](implementation.md). |
| QC | Independent review, acceptance checks and reproducible findings. |
| Typing specialist | Concretely specified repetitive edits and code-rule application; returns changes to the issuing agent for review. |

Assign a responsible agent for each role. Simple work or resource limits may combine roles with honest attribution; preserve QC independence whenever feasible. Follow [model and resource allocation](agents-and-resources.md) and the [PM work-order/reporting contract](pm-control.md) for dispatch.

## Typing-specialist work orders

PM, system designer, GUI designer, developer and QC may issue orders within the approved roadmap. The PM coordinates priority and file ownership; the developer retains code correctness and integration responsibility.

- An order names the issuer, target files/symbols, exact change or deterministic transformation, applicable code/local-rule IDs and exceptions, a useful example if needed, and completion checks. Resolve behavioral and design choices before dispatch.
- Suitable work includes repeated declarations/event wiring, approved template expansion, formatting, naming rules and specified document updates. Restrict bulk edits to named files/symbols; preserve generated/public/ABI-bound and approved exceptions.
- The typing specialist does not invent behavior, architecture, dependencies, UI direction or refactoring. Return ambiguous/conflicting items to the issuer; continue independent clear items. Brainstorming participation is limited to implementation-rule feasibility.
- Queue shared-file orders, re-read current content, use an established formatter/generator when suitable, inspect the diff and run assigned checks.
- Return the order reference, changed files, applied rules, results and unresolved items. The issuer reviews the diff; the developer runs integration checks. QC retains independent final verification, including when QC issued the correction. The typing specialist never self-accepts the feature.

## PM-led specialist brainstorming

Before committing to a feature/problem/improvement direction, gather role-specific ideas. A fully specified routine change can use brief role comments.

1. **Brief:** PM shares outcome, current behavior/reference locations, constraints, acceptance criteria and open decisions. Request ideas before implementation.
2. **Independent proposals:** Relevant specialists first assess the item independently: system design covers architecture/reuse/dependencies; GUI covers workflow/visuals/accessibility and a DR proposal; development covers feasibility/effort/performance and a representative sample; QC covers failures/regressions/testability. Omit unrelated fields with a reason. Separate agents may work in parallel within resource limits; combined-role assessments must not be described as independent reviews.
3. **Compare:** Each returns an idea, benefit, evidence, tradeoffs/effort, dependencies and validation method, separating facts from assumptions. PM compares against acceptance, user value, compatibility, reuse, effort, risk and verification cost; merges compatible ideas and records conflicts, rejected/deferred ideas and reasons. Resolve only gaps that affect the decision.
4. **Handoff:** Keep the brief, proposals, chosen direction, assumptions and validation owners in the existing roadmap/task plan. System designer turns the synthesis into sequenced tasks. Preserve user-fixed requirements and applicable user decisions; revisit affected choices when requirements or evidence change.

## Operating workflow

1. **Frame:** Apply [startup and authority](update-and-authority.md) and applicable [local rules](../localrule/local-skills.md). Define objective, constraints, acceptance and language/platform; resolve material open decisions and complete the relevant brainstorming.
2. **Plan:** Inventory comparable screens, controls, helpers, styles/assets, symbols, data flows and referenced libraries. Classify candidates as reuse, adaptation or replacement with evidence. Record deliverables, ordering, owners, dependencies, risks and verification. Assign available supporting skills within saved authority, recording role, purpose and prerequisites.
3. **Recommend new-project skills:** Before roadmap approval, recommend the smallest useful set from approved local/public catalogs. For each candidate give source, purpose/role, benefit, prerequisites/access, dependency/privacy/security impact, compatibility and a local/no-install alternative. Label already available, recommended to install or not recommended; record user allow/deny/defer decisions. Unavailable capabilities follow [external installation](update-and-authority.md#external-skill-installation-workflow); recommendation alone authorizes no download or connection.
4. **Approve and dispatch:** PM approves the roadmap and uses [PM control](pm-control.md) for bounded assignments, historical estimates, allowances, reports and forecasts. A GUI designer/developer task plan identifies affected components, existing references, approach, reuse and validation; the system designer checks alignment. UI tasks require the [user-confirmed visual handoff](gui-workflow.md#ui-proposal-and-user-confirmation-before-implementation) before implementation.
5. **Implement:** Developers follow [reuse, naming, sample-first and Debug conventions](implementation.md); repetitive specified edits use the work orders above. Use the approved GUI handoff, report feasibility issues and apply the [GUI review checkpoints](gui-workflow.md#design-handoff-and-review) before the next affected stage.
6. **Review and correct:** System designer checks roadmap alignment; GUI designer checks approved design; QC reviews intermediate/final results. Distinguish defects from suggestions. A blocking finding records criterion, severity, expected/actual result, reproduction/evidence and owner. Correct within scope, run affected checks and obtain QC re-verification, or record a PM/user-authorized exception with remaining risk.
7. **Verify and accept:** After implementation/build checks, prepare and execute the authorized [Computer Use plan](gui-workflow.md#user-confirmed-computer-use-verification) when applicable. Record skipped/blocked/not-applicable checks explicitly. PM accepts against original criteria only after required QC evidence or authorized exceptions.
8. **Close:** Report scope, changed files/components, validation/outcomes, deviations and open risks/follow-ups. Close estimate-versus-actual history under [PM control](pm-control.md).

## Persistent execution harness

For multi-step execution, correction loops or cross-session work, apply the [harness contract](harness.md) and [config template](../templates/harness-config.json). That reference owns setup, commands, gates, limits and recovery; link the roadmap rather than duplicating it. Simple one-step work needs no new ledger. Preserve existing preferences and state; use `resume` before relying on interrupted/stored results.