---
name: project-symbol-guide
description: "Analyze a code project's variables and functions by class, maintain source-linked symbol references, and recommend existing symbols for the current task before adding missing ones. Use for project analysis, symbol catalog maintenance, and reuse-oriented implementation; new project functions require user permission."
---

# Project Symbol Guide

Build a reusable map of what a project already provides. Keep the analysis in the target project so later sessions can find, verify, and reuse it. The Korean display name is **프로젝트 심볼 가이드**; “머지프로젝트” suggests merging projects and does not describe symbol analysis.

## Scope and persistent references

Resolve the target project from the user's request and working directory. Read its applicable instructions, manifests, and existing analysis artifacts. Use an existing architecture map to narrow the relevant modules when available; this skill does not require another skill or a particular language/toolchain.

Default storage, unless the project has an established location:

```text
docs/project-analysis/
  index.json           # scope, source fingerprints, owners, symbol lookup
  classes/<owner>.md   # class variables, functions, and evidence
  modules/<owner>.md   # free functions, globals, and module-level symbols
```

Read [the catalog format](references/catalog-format.md) when creating or updating these artifacts. Store project-specific analysis in the project, never in the installed skill. Do not copy source bodies or secret values into the catalog.

For an initial project-wide analysis, enumerate first-party source files and build configurations, then analyze classes and module symbols across that scope. A task-specific request can start with the affected modules. Explicitly record covered, pending, and excluded files and parser/configuration limits. An incomplete scan is partial even when all discovered candidates have been documented. Do not present a name-only regex scan as semantic analysis.

## Analyze classes, variables, and functions

Use available compiler/language-server/AST information for symbol resolution. Targeted `rg` searches and direct source reading are valid fallbacks; label uncertain edges rather than guessing. Inspect declarations, implementations, and relevant usages together, including split/partial classes, inheritance, overloads, templates/generics, and conditional compilation where present.

For each class, record its qualified name, responsibility, bases/interfaces, source locations, and related modules. Distinguish declared members from inherited members and link to the declaring class.

For each variable/property/field needed to understand or implement behavior, record:

- Qualified owner/name, type, visibility, instance/static/constant kind, and declaration location.
- Purpose, initializer/default when safe, valid range/unit, and lifecycle/ownership or thread requirements when evidenced.
- Known readers and writers, distinguishing a direct write from an indirect or unresolved mutation; link the relevant functions and evidence.

Inventory all declared member variables in the covered classes. Include parameters and local variables under their function when they materially affect behavior, state transitions, or reuse; state this local-variable coverage rule in the catalog. Include relevant global/module variables under their module.

For each function/method, record:

- Qualified name and full signature, visibility, static/virtual/async qualifiers as applicable, declaration and implementation locations.
- Purpose, inputs, outputs, error behavior, preconditions, state changes, side effects, and ownership/thread constraints when evidenced.
- Known callers/callees and variables read/written, with source evidence and unresolved relationships explicitly marked.
- Reuse conditions, existing call examples and tests when available. Distinguish declaration-only/external functions from verified implementations.

Inventory all declared functions in covered classes/modules, including constructors, destructors, accessors, and overloads. Keep behavioral detail proportional to its importance. For relationships, a list with no discovered edges means “none observed in this scope,” not proof that none exist. Dynamic dispatch, reflection, events, macros, aliases, and pointer calls may require unresolved entries.

## Refresh before recommending

On each invocation, read the existing index first. Compare the recorded source-file inventory and content fingerprints with current files, including uncommitted changes and relevant untracked source files. A matching Git commit alone does not prove freshness. If comparison is unavailable, re-read sources used for the current decision and report the remaining coverage limitation.

Refresh changed, added, deleted, and renamed files plus affected owners and incoming/outgoing references. Recheck dependent records when a signature, type, inheritance, or state contract changes. Remove dead lookup entries and broken links; preserve a rename mapping only when useful and verified. Preserve unaffected records and project-authored notes. Update evidence locations after edits, and never advance a file's analyzed fingerprint until its affected records have been reconciled.

Update the catalog after authorized code changes and relevant validation. Record analysis and validation status separately: a catalog can match source even when the build has failed. Updates occur during skill execution; do not claim background watching or automatic synchronization between sessions.

## Recommend symbols for the current task

Translate the requested behavior into responsibilities, state, inputs, and outputs. Search the catalog by purpose, aliases, types, owner, signature, and usage, then verify promising candidates against current source and direct contracts. Expand to related modules, base classes, module-level symbols, and already available dependencies/libraries when the initial scope has no fit.

Recommend the smallest useful set of variables and functions. For each candidate, show its stable ID, qualified name/signature, clickable source location, reason it fits, and relevant access/lifetime/thread/dependency constraints. Explain how the variable and function work together when they form a reuse path. Rank by behavioral fit and compatibility, not name similarity. Reject inaccessible or incompatible candidates with a brief reason. Do not suggest weakening encapsulation or duplicating stored state merely to reuse a private member.

When nothing suitable exists, report the searched scope/terms, relevant rejected candidates, and remaining unknowns. An unavailable dependency or unresolved parser result is a search limitation, not proof that a symbol is absent.

## Missing symbols and permission for new functions

An analysis or recommendation request authorizes catalog updates, not project implementation. In analysis-only work, describe missing symbols as proposals. When implementation is requested, add a necessary missing variable after the reuse search, following project conventions for owner, type, initialization, lifecycle, and access. No separate variable-creation approval is required within that authorized implementation scope. Do not add unused speculative state.

**Creating any new project function requires user permission before writing its declaration or body to project source.** This includes methods, helpers, local functions, new overloads, constructors/destructors, accessors, callbacks/lambdas, and generated function-bearing code. Renaming a planned helper or delegating generation does not bypass this boundary. Ordinary edits within an existing function follow the user's implementation scope; materially replacing its public contract should be presented for approval.

Before asking, complete the search and prepare a concrete proposal containing:

- Why existing variables/functions cannot satisfy the task, including search evidence.
- Proposed owner, target file, full signature, purpose, inputs/outputs, side effects, and intended callers.
- Required variables/dependencies, validation plan, and the exact set of new functions covered by the request.

Ask explicitly to approve those functions, explaining that the user's function-creation rule in this skill requires it and linking to this `SKILL.md`. A signature in the chat proposal is allowed; do not add function stubs or bodies to project files while awaiting approval. Continue independent analysis/catalog work. Silence is not approval. A prior explicit instruction to create the identified function or a prior approval covering the proposed function set suffices; a broad feature request alone does not. Ask again only if the approved set or contract materially expands. After approval, implement and validate, then update the function and variable references together. If a variable change needs a new constructor/accessor/helper, wait for that function's approval before the dependent edit.

## Report

Give the catalog location, analyzed scope/freshness and important gaps, then the task-relevant candidates or missing-symbol proposal. Distinguish existing symbols, approved changes, and proposals. For code changes, summarize validation and update both sides of variable/function relationships. Do not claim a complete project analysis when coverage is partial.
