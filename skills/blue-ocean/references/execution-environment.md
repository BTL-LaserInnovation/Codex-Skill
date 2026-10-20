# Execution environment and maintenance

Read the applicable section when configuring workers, diagnosing environment failures, changing Codex integrations, or performing requested maintenance. Record observations in the existing task/roadmap; do not create another mandatory ledger.

## Windows, WSL and worktrees

- Before a worker edits or builds, establish its actual repository root, branch/worktree and shell. Use `git rev-parse --show-toplevel` and `git status --short` where available. Resolve Windows versus WSL paths in that environment; never assume a task title or inherited working directory identifies the checkout.
- Follow the existing solution-to-project mapping and project-native toolchain. Locate MSBuild/Visual Studio or dotnet and the required Debug/Release/platform configuration before starting a build. Keep intermediate/output paths separate for simultaneous builds that would otherwise overwrite the same files. If isolation is impractical, sequence those builds.
- A worktree does not automatically inherit uncommitted files, ignored configuration, installed dependencies or environment variables. Check only prerequisites needed by the assigned task. Preserve local edits and credentials; do not copy secrets or install prerequisites implicitly.
- After an app update or reconnect, inspect the actual sandbox/tool error and checkout before retrying. Distinguish an unavailable executable, permission failure or disconnected environment from a product defect. Use an allowed narrower action or the supported escalation path. Report an approval-review rejection and its reason; do not repeat the same rejected operation or weaken permissions to bypass it.
- At handoff record the checkout, target/configuration, last observed result and next action. For harness work, use [resume and revalidation](harness.md) before trusting old checks.

## Models, speed and integration compatibility

- Preserve `gpt-6.1-sol` for every Blue Ocean role. Check the actual client/workspace model availability when configuring agents, scripts or scheduled work; a model named in a prompt is not evidence that it ran. Report unavailable or unverified assignments accurately.
- GPT-5.5 retired from Codex with ChatGPT sign-in on October 14, 2026; that retirement did not apply to API-key sessions. Check affected saved model selectors when migrating an existing configuration rather than rewriting unrelated settings.
- Ultrafast is an optional client/plan capability for GPT-6.1 Sol. Check current official availability and usage terms before recommending or enabling it. Keep the selected model and reasoning appropriate to the task; never claim the mode is active based on instructions alone. Respect the user's existing choice and authorization for settings or spending changes.
- When updating a custom Codex integration, inspect the commands and runtime it actually uses. `codex mcp-server` and `codex-mcp-server` were removed on September 5, 2026. The documented app server replacement is experimental; review its current contract before a migration and do not describe it as production-supported. This removal does not remove support for connecting Codex to external MCP servers. No migration is needed if the integration does not use those removed commands.

## Requested code cleanup and CI work

- Bound the requested area and observable behavior before removing code or changing CI. Reuse existing repository evidence and affected builds/tests; do not extend ordinary feature work into an unsolicited cleanup campaign.
- For C++/MFC, inspect message maps, resource IDs, exported/ABI symbols, dynamic loading and configuration paths. For C#, consider reflection, XAML bindings, serialization and public contracts. A text search with no matches alone does not prove code is unused.
- Record evidence and uncertainty for each removal candidate, preserve intentionally dormant recovery/compatibility paths, and leave unsupported candidates pending. Keep changes reviewable and verify affected Debug/runtime behavior or CI jobs. Do not equate a smaller diff or faster CI with preserved behavior.

## Official sources

Checked October 21, 2026. Availability may change; recheck before changing a client or integration.

- [ChatGPT & Codex changelog](https://learn.chatgpt.com/docs/changelog): model retirement, Ultrafast, Windows sandbox/worktree fixes and removed MCP-server commands.
- [Maintaining software with the GPT-6 family](https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family): evidence-based maintenance examples, not a mandate to remove code.
