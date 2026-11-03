# Agent models and resource scheduling

## Resource-aware parallel execution

Use available authorized agents/processes for independent work that removes a real bottleneck. Do not create a fixed agent count or parallelize dependent work.

- Before substantial parallel work, inspect agent slots, logical CPU count, CPU/memory pressure and build/test topology. Keep the interactive desktop responsive unless the user requests dedicated maximum utilization.
- Parallelize independent reconnaissance, isolated components, test suites or reviews. Sequence architecture decisions, shared-file edits, migrations and dependent builds; isolate build outputs where needed.
- Fit agent/build concurrency to capacity; reduce it for memory pressure, instability or poor responsiveness. Monitor running work and stop/scale down redundant, blocked, failed or resource-starved work while preserving capacity for integration, verification and cleanup.
- Use existing tools and account limits; new API keys, paid workloads or external-service connections require separate user authorization.
- Record material concurrency/resource choices and validation owners in the roadmap. Apply [PM control](pm-control.md) for bounded work orders, reporting, token allowances and forecasts, including nested and typing work.

## Role-based agent models

Use **GPT-6.1 Sol** (`gpt-6.1-sol`) for the PM only and **GPT-6.1 Terra** (`gpt-6.1-terra`) for all other Blue Ocean roles, including designers, developers, typing, QC, reconnaissance, build and test workers. Reuse this allocation without asking each time.

- Explicitly select the role's model when spawning. Follow the tool's model-override/context requirements and provide a self-contained handoff when a fresh context is required. With inheritance only, verify the parent's model before claiming compliance.
- A required model being unavailable leaves that assignment pending; do not silently substitute. An already-running session cannot be declared switched by a prompt. Explain any necessary client switch/new session.
- Record role/effective model in the task assignment and mark unknown values unverified. Change the allocation only on explicit user instruction.

## Context and handoff

Use the [delivery roles](delivery.md#roles-and-ownership) and PM work orders for ownership. Give each worker its bounded goal, necessary files/excerpts, constraints, expected resources and completion signal. Reuse unchanged file references and prior summaries. Completion returns changes, validation, blockers and owner decisions; keep shared-file edits sequential and QC independent where feasible.