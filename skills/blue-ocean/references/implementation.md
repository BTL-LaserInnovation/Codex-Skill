# Reuse, implementation and QC conventions

## Project symbol guide

For project analysis, implementation planning and source changes, actively use an installed `project-symbol-guide` under its [standing authorization](update-and-authority.md). Read that skill before choosing variables/functions. If absent or later restricted, use targeted source searches and record the limitation; installation is not implied.

- Verify the existing index against current source, including uncommitted changes, and refresh affected classes/modules. A small change needs no full-project catalog.
- Recommend compatible existing symbols with source locations, signatures, purpose and relevant state/access/lifetime/thread constraints. Record the selected reuse path and gaps alongside architecture/Mocha evidence.
- If no symbol fits, report search scope, rejected candidates and unknowns. Before declaring/defining a new project function, follow the symbol guide's separate permission rule; reuse approval covering the identified function. Skill-use authorization alone is insufficient. Apply its variable rules to necessary new values.
- After authorized changes and validation, refresh affected symbol records and relationships. Distinguish source freshness from validation and report partial coverage.

## Mocha library reference for MFC and C++

Before choosing a new MFC/C++ control, utility, library or implementation, check availability and saved permission for `mocha-library`. When permitted, use it to resolve `PathMocha`, consult the generated index/relevant diagram, search public headers and implementation, and inspect the candidate's build contract before assigning code.

- Record search terms, index/diagram area, candidates and selected reuse path. Explain why no candidate fits before choosing a new implementation.
- Consume a compatible API/library through its existing contract instead of copying shared Mocha code into the target project.
- State Debug/Release, x64, dependency and deployment impact for headers, `.lib` files, `common.props` and runtime binaries.
- Preserve Mocha source, binaries, project files and `PathMocha` setup during unrelated target-project work. If unavailable, denied or deferred, record the limitation and continue ordinary reuse-first work.

## Dependencies and open-source components

Search repository code, project/package manifests, resources and build configuration before adding a utility, control, asset or dependency. Prefer a compatible existing item; a visual effect alone does not justify a new library.

For MFC/C#, compatible open-source controls/libraries are recommended reuse options. Use upstream as-is when suitable, adapting through established wrappers/styles/events. A fork or material upstream edit needs its reason, maintenance plan and upgrade impact.

Before introduction, compare viable candidates by requirements and visual fit, license, maintenance/release/issue activity, documentation, package/build integration, Debug/Release and x86/x64 support, deployment dependencies, security/performance and adaptation effort. Explain rejected alternatives when only one fits. Material product choices require PM/user selection; record purpose, selected version/commit, license notices, approval and validation in the roadmap.

For C#, prefer verified compatible NuGet packages, pin the version and inspect metadata/transitive dependencies. Preserve existing package management; record ID/source/license/framework and dependency changes. Verify restore, build and actual Debug runtime behavior. Do not silently upgrade or replace packages in unrelated work.

## Solution-based project layout

When a `.sln` exists, its directory is the project root. For new/unstructured projects, use:

| Path | Contents |
| --- | --- |
| `bin/` | Executables and runnable outputs |
| `cfg/` | Parameters and runtime configuration |
| `data/` | Shared-memory structures, structure headers and memory declarations |
| `lib/`, `include/` | External library binaries and headers |
| `src/<ProjectName>/` | Internal independent/shared projects |
| `<SolutionName>.sln` | One or more solutions mapping projects under `src/` |

Record solution-to-project mapping; avoid duplicating shared code. Use established reference/include/library/output conventions and relative paths where possible. Preserve an existing different layout unless restructuring is explicitly approved. Parallel root-level code/dependency folders require a recorded reason and PM/user approval.

## Implementation planning and naming

- Inspect user-specified reference projects and how their functions are used. Recommend existing screens, components, symbols and data flows to the assigned developer; link relevant files/excerpts instead of repeatedly copying unchanged context.
- Preserve architecture, formatting, control flow, error handling and project-native tools. Record technical deviations and obtain system-designer confirmation. Provide the assigned skills, code/design references and build/test commands through the [delivery handoff](delivery.md); skill access/installation follows [authority](update-and-authority.md).
- If an available, permitted Superpowers skill fits the development task, the system designer may assign it as a supporting reference. Its absence does not imply installation; the roadmap and project conventions remain authoritative.
- Use the [GUI workflow](gui-workflow.md) for visual baseline, proposal confirmation, component reuse, handoff, construction and visual QC.
- Before adding a variable, reuse an existing value only when scope, lifetime and meaning safely match; avoid ambiguous coupling.
- For every new/modified C++/C# variable or field, use a project-approved type prefix plus a meaningful name, with `m_` for members and `g_` for global/file-scope variables before the type prefix. Examples: `nItemCount`, `dMeasuredDistance`, `strStatusMessage`, `m_nRetryCount`, `g_dDefaultScale`. Apply to parameters and loops (`nIndex`, `nRowIndex`); a type alone or one letter is insufficient.
- The system designer records the prefix table and approved exceptions before implementation; developers and QC use the same baseline. Typical prefixes: `b` bool, `n` int, `d` double, `f` float, `str` strings, `p` pointers, `arr` arrays. Preserve domain meaning in the suffix.
- Check naming in affected declarations without mass-renaming untouched legacy code. Document technical exceptions for generated code, public/ABI-bound names, external callbacks, fixed project conventions and narrowly scoped mathematical notation.

## Sample-first logic and Debug integration

Use project-native C++/C# build/test commands. A new build system or dependency requires user authorization.

For logic-heavy changes, isolate the smallest behavior/interface slice, implement a minimal sample or focused unit/characterization test, and run representative success/failure inputs. Record the result and correct failures before expanding into broader code, one verified slice at a time.

For every external library/SDK/API integration:

1. Record version, required configuration, credential/endpoint assumptions and native build target.
2. Build Debug and confirm dependency loading/linking.
3. Run the actual program or minimal in-project smoke path with debug symbols and useful logs.
4. Exercise applicable initialization, primary calls, returned data/state, callbacks, timeout/cancellation, error handling and cleanup.
5. Inspect exceptions/assertions, return codes/logs, thread/UI affinity, ownership and shutdown.
6. For external-state dependencies, test at least one invalid configuration or unavailable-service path.
7. Record reproducible steps, environment, expected/actual results and evidence.

Compilation/linking alone cannot complete integration; require actual Debug success or a documented PM/user exception with remaining risk. Review and correction ownership follow [delivery](delivery.md#operating-workflow).