# Agent models and resource scheduling

Command and template paths are relative to the installed Blue Ocean skill root. Read only the sections relevant to the current task.

## Resource-aware parallel execution

When a task has independent, materially time-consuming work, use available and authorized LLM agents and local processes to finish it as quickly as the PC can safely support. The objective is high useful utilization, not a fixed agent count or artificial parallelism.

- Before scheduling substantial parallel work, inspect the practical limits: available agent slots, logical CPU count, current CPU and memory pressure, and the project build/test topology. Keep the interactive desktop responsive by default; use the whole machine only when the user explicitly requests dedicated maximum utilization.
- Split only independent work such as codebase reconnaissance, isolated component implementation, separate test suites, or independent reviews. Sequence architecture decisions, shared-file edits, migrations, and dependent build steps.
- Use all available authorized agent slots when their work removes a real bottleneck. Size local build/test parallelism to the remaining CPU and memory capacity, then reduce concurrency if the system becomes memory-bound, unstable, or materially less responsive.
- Prefer the already available model/agent tools. Do not create API keys, start a paid LLM/API workload, connect a new external service, or bypass account limits without the user's separate authorization.
- Give every worker a bounded goal, relevant context, resource expectation, and completion signal. Reuse completed summaries instead of repeatedly sending the same repository context.
- Monitor running workers and local processes. Stop or scale down redundant, blocked, failed, or resource-starved work; preserve enough capacity to collect results, run verification, and complete cleanup.
- Record the selected concurrency, role assignments, resource constraints, and validation ownership in the roadmap whenever parallel execution materially affects delivery.
## Unified agent model

Use **GPT-6.1 Sol** (`gpt-6.1-sol`) for every Blue Ocean agent: PM, system designer, GUI designer, software developer, typing specialist, QC, and any additional reconnaissance, build, test, or review workers. Roles differ in responsibility, not model capability. Do not ask the user to choose models on each task or assign a cheaper model to repetitive work.

- The PM retains scope, acceptance criteria, roadmap approval, task decomposition, integration, and final acceptance. Specialist agents retain their domain responsibilities. Give each worker one bounded goal, necessary files and constraints, and a completion summary covering changes, validation, blockers, and decisions for the responsible owner.
- When creating a subagent, explicitly select `gpt-6.1-sol` where the tool supports model selection. When it only supports inheritance, verify the parent uses that model before claiming compliance. Do not claim an already-running session has changed models; explain any required client-side switch or new session.
- If `gpt-6.1-sol` is unavailable, report the constraint and leave the affected assignment pending rather than silently substituting another model. A different allocation requires an explicit user instruction.
- Record each agent's role and effective model in the roadmap's task-assignment record; mark unverified model information as unverified. Change this allocation only when the user requests it.
