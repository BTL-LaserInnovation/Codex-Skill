---
name: mocha-library
description: "Find and reuse existing MFC/C++ implementations, headers, libraries, and build conventions from the local Mocha library referenced by PathMocha before creating equivalent code."
---

# Mocha Library Reference

Use this skill for MFC or C++ work when the requested behavior may already exist in the local Mocha library. Its purpose is to make Mocha a source of evidence and reuse before new code, controls, utilities, or dependencies are introduced.

## Resolve the library

1. Read `PathMocha` from the active environment. If it is absent, query the User and Machine environment-variable scopes.
2. Verify that the resolved directory contains `include`, `src`, and `all.sln`. Do not set, alter, or persist environment variables as part of ordinary reference work.
3. If the path is unavailable, report that Mocha could not be searched and continue with the target project's normal reuse-first process. Do not assume that a hard-coded path exists.

## Fast discovery

Read [the generated index](references/mocha-library.index.json) before broad exploration. It maps the Mocha solution, public-header groups, Visual C++ projects, project references, and available libraries. Read [the Mermaid diagram](references/mocha-library.mmd) when deciding which subsystem is relevant.

Refresh both artifacts after a meaningful Mocha module, public API, or dependency change by running `scripts/update-mocha-index.ps1` from this skill directory.

The generator resolves `PathMocha` at run time and does not modify the Mocha checkout. Inspect the refreshed artifact before committing it because it is a portable snapshot of the local library structure.

## Reuse-first lookup

Before designing or implementing an MFC/C++ feature, search the smallest relevant Mocha scope for the domain term, intended class/API name, and comparable control or behavior.

- Search public contracts in `<PathMocha>/include` first; then inspect the matching implementation under `<PathMocha>/src` and its `.vcxproj` file.
- Use targeted `rg` searches over headers, source files, and project files. Search the relevant indexed module before enumerating broad trees.
- For a candidate, verify its public header, ownership/lifetime expectations, MFC message or UI behavior when applicable, source/build project, and Debug/Release x64 compatibility.
- Inspect the candidate project's include paths, library directories, dependent libraries, and preprocessor definitions before proposing integration. Preserve the consuming project's established build convention.
- Reuse an existing public API, library, control, or established pattern when it meets the requirement. Do not copy an implementation into a new utility or create an equivalent control merely because it is easier to reach.

When no candidate is suitable, record the search terms and rejected candidates briefly, then implement the smallest compatible solution. A candidate is not suitable when its public contract, ownership model, platform/configuration support, licensing, or dependencies conflict with the target project.

## Boundaries

Treat the Mocha checkout as a shared reference and dependency source. Do not edit its source, binary libraries, project files, or environment setup scripts unless the user explicitly asks to change Mocha itself. Do not add a new dependency or change a target project's environment variables solely to use a candidate; identify the integration impact first.

For the observed repository layout and build details, read [Mocha layout reference](references/mocha-layout.md).
