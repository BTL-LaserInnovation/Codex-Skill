# Symbol catalog format

Use this format when creating or refreshing a catalog. Preserve an established equivalent project format if it supports the same evidence, freshness, and lookup requirements.

## Index

Store UTF-8 JSON in `docs/project-analysis/index.json`. Paths are project-root-relative with forward slashes; timestamps are ISO 8601 with an explicit offset. Never persist a machine-specific absolute project path. Use actual values obtained from the project, not the illustrative names below.

```json
{
  "schemaVersion": "1.0",
  "updatedAt": "2026-10-22T14:00:00+09:00",
  "project": {"name": "MotionApp", "root": "."},
  "coverage": {
    "status": "partial",
    "requestedScope": ["src/**"],
    "pendingFiles": ["src/Display.cpp"],
    "excluded": [{"path": "vendor/**", "reason": "Third-party source"}],
    "configurations": ["Debug|x64"],
    "limitations": ["Function-pointer targets unresolved"],
    "localsPolicy": "Parameters and locals affecting behavior, state transitions, or reuse"
  },
  "sources": [
    {"path": "src/Axis.h", "sha256": "actual-content-sha256", "owners": ["class:Motion.Axis"]},
    {"path": "src/Axis.cpp", "sha256": "actual-content-sha256", "owners": ["class:Motion.Axis"]}
  ],
  "owners": [
    {"id": "class:Motion.Axis", "qualifiedName": "Motion::Axis", "kind": "class", "catalog": "docs/project-analysis/classes/motion-axis.md"}
  ],
  "symbols": [
    {"id": "var:Motion.Axis.position", "owner": "class:Motion.Axis", "kind": "field", "qualifiedName": "Motion::Axis::position", "signature": "double position", "summary": "Current axis position", "tags": ["position", "axis", "위치"], "catalog": "docs/project-analysis/classes/motion-axis.md#var-position", "declarations": [{"path": "src/Axis.h", "line": 12}], "definitions": []},
    {"id": "fn:Motion.Axis.Move(double)", "owner": "class:Motion.Axis", "kind": "method", "qualifiedName": "Motion::Axis::Move", "signature": "bool Move(double target)", "summary": "Request an axis move", "tags": ["motion", "이동"], "catalog": "docs/project-analysis/classes/motion-axis.md#fn-move-double", "declarations": [{"path": "src/Axis.h", "line": 18}], "definitions": [{"path": "src/Axis.cpp", "line": 42}]}
  ],
  "validation": {"status": "not-run", "details": "Analysis only"}
}
```

`coverage.status` is `partial` or `complete` relative to `requestedScope`. `complete` requires every included file to have been examined and all in-scope declarations cataloged; record semantic limitations independently. `sources` holds analyzed files and the fingerprints of the bytes actually analyzed. Files awaiting analysis go in `pendingFiles`, including newly discovered files. Account for every file in the requested inventory as analyzed, pending, or excluded with a reason. Re-enumerate that inventory when refreshing; comparing existing hashes alone misses new/deleted files. Non-Git projects use the same inventory/content comparison.

Update a file's fingerprint only after reconciling all impacted symbols and relationships. If a file changes during analysis, re-read it or keep it pending rather than storing a fingerprint for bytes not analyzed. Keep unresolved relationships in owner records. A variable's `definitions` can be empty when its declaration is also its definition; explicitly describe external/declaration-only symbols in the owner record.

## IDs and locations

- Use compiler-native stable IDs if available. Otherwise form IDs from project/module, qualified owner/name, symbol kind, and canonical parameter types plus generic arity and method qualifiers needed to distinguish overloads. Include a relative source path for file-local symbols. Return types alone normally do not identify an overload; include language-specific discriminators where necessary.
- Do not use line numbers as IDs. Preserve IDs across implementation-only edits; update linked records when identity changes. Use a collision-safe owner filename and an explicit, unique HTML anchor for every symbol section.
- Store declaration and definition locations separately. Shared declarations, partial classes, templates, and configuration-dependent locations may need multiple entries with a configuration note.
- JSON paths resolve from the project root. Markdown links resolve from their containing catalog file; verify that they point to the intended source. Refresh line hints after edits and confirm the qualified symbol before acting on a link.

## Owner record

Each class or module file has this information, expressed as compact tables plus per-symbol sections where detail is needed:

1. Owner ID, qualified name, responsibility, bases/interfaces, source links, analyzed configurations, and scope limits.
2. Variable table: symbol ID/link, name, type, access, storage kind, purpose, safe initializer/default, range/unit, declaration link. Per-variable details hold lifecycle, thread/ownership constraints and known readers/writers by function ID with evidence.
3. Function table: symbol ID/link, full signature, access/qualifiers, purpose, declaration/implementation links. Per-function details hold inputs/outputs/errors, preconditions, effects, read/write variable IDs, caller/callee IDs, constraints, call examples and tests.
4. Unresolved relationships and validation status. For each unresolved edge, state the source evidence, uncertainty, and relevant configuration rather than inventing a target.

Use explicit HTML anchors such as `<a id="var-position"></a>` and `<a id="fn-move-double"></a>` so lookup links remain stable when headings change. For out-of-scope/external targets, keep a qualified name and evidence marked `external` or `not-analyzed` rather than a dangling local ID. Use `unknown` or `not-applicable` for unestablished or irrelevant semantic fields; an empty list means only that no instances were observed within the stated scope.

Keep variable → reader/writer and function → read/write entries consistent, likewise caller ↔ callee entries when both endpoints are cataloged. Qualify relationships as `observed`, `inferred`, or `unresolved`; inferred relationships include their rationale. If an edited file affects incoming relationships in unchanged files, recheck those records too.

## Proposal boundary

Index only symbols that exist in source. Keep missing-symbol proposals in the task response or a project-established proposal document, clearly separate from existing-symbol records. After approved implementation, assign real IDs/locations and update both lookup and owner records. Proposed functions must not become source declarations, stubs, lambdas, or implementations until approved.

## Completion checks

Parse the JSON; check unique owner/symbol IDs, owner membership, live source paths, valid catalog files/anchors, and references to cataloged IDs or explicitly labeled external targets. Check inventory coverage, analyzed fingerprints, changed/deleted symbols, reciprocal relationships, and representative source links against current code. Run relevant project validation for implementation changes and record the actual result; do not claim a build/test was run for catalog-only work.
