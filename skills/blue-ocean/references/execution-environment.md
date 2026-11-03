# Execution environment and maintenance

Read the relevant section when configuring workers, diagnosing environment failures, changing integrations or performing requested maintenance. Keep observations in the existing task/roadmap.

## Windows, WSL and worktrees

- Before editing/building, establish the actual repository root, branch/worktree and shell, using `git rev-parse --show-toplevel` and `git status --short` where available. Resolve Windows/WSL paths in that environment.
- Locate the native MSBuild/Visual Studio/dotnet toolchain and required Debug/Release/platform configuration. Isolate intermediate/output paths for simultaneous builds, or sequence them.
- Worktrees do not inherit uncommitted files, ignored configuration, dependencies or environment variables automatically. Check task prerequisites and preserve local edits/credentials; do not copy secrets or install prerequisites implicitly.
- After an update/reconnect, inspect the actual checkout and tool/sandbox error before retrying. Separate environment failures from product defects. Use a permitted narrower action or supported escalation; report approval-review rejection and its reason without repeating/bypassing it.
- At handoff record checkout, target/configuration, last result and next action. For persistent work, use [harness recovery](harness.md) before trusting stored checks.

## Model settings and integration compatibility

- Apply [role models](agents-and-resources.md#role-based-agent-models) when configuring agents, scripts or scheduled work. Verify actual client/workspace support and effective settings; a prompt alone does not prove activation.
- Before recommending/enabling a speed mode or changing an integration, check current official documentation, availability, usage terms and the actual commands/runtime involved. Preserve user choices and authorization for settings/spending changes.
- Migrate only affected selectors/commands after checking the replacement's supported contract. Do not rewrite unrelated settings or treat an experimental feature as production-supported.

## Requested code cleanup and CI work

- Bound the requested area and observable behavior before removal or CI changes. Use existing evidence and affected checks; do not add unsolicited cleanup to feature work.
- For C++/MFC inspect message maps, resource IDs, exports/ABI, dynamic loading and configuration; for C# include reflection, XAML bindings, serialization and public contracts. No text-search matches alone does not prove unused code.
- Record removal evidence/uncertainty, preserve intentional recovery/compatibility paths and leave unsupported candidates pending. Verify affected Debug/runtime behavior or CI jobs; smaller code/faster CI does not establish behavioral preservation.