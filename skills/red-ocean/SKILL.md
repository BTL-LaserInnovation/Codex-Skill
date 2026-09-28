---
name: red-ocean
description: "Use for creating or changing C#/.NET applications and headless libraries in Windows Visual Studio. Follow existing code style, compatibility, and verification; apply designer and responsiveness rules only to WinForms UI work; coordinate five agents by default unless the user forbids subagents."
---

# Red Ocean — C#/.NET Development

## Scope and precedence

- Apply to designing, implementing, changing, and reviewing C#/.NET applications and class libraries, including libraries without any UI, in **Microsoft Visual Studio on Windows only**. Use Visual Studio as the development environment for editing code, building, and debugging. When UI is needed, use WinForms and the Visual Studio designer. Do not switch to Visual Studio Code, Rider, or another UI framework. If Visual Studio is inaccessible, identify IDE work that cannot be performed or verified and do not report it as complete.
- Use this skill independently, without depending on another skill's instructions or role workflow. Follow the current user's instructions, explicit solution configuration and established project patterns, then this skill's defaults. The responsible agent resolves and records real conflicts, giving priority to the user's instructions.
- Before work, inspect `.sln`/`.csproj`, `TargetFramework`, `LangVersion`, `Nullable`, `.editorconfig`, `Directory.Build.*`, analyzers, NuGet conventions, build/test configurations, and relevant implementations. Inspect UI/designer patterns when UI exists. Match the existing syntax, naming, indentation, whitespace, braces, file organization, exception handling, and event style. Do not reformat or rename untouched code wholesale.
- For a new project, consider the latest stable, released, supported .NET LTS at the time of work. For a WinForms app, set a Windows target framework and `UseWindowsForms`. Do not force WinForms references or a Windows target framework on a headless library that does not need them. Preserve an existing project's framework and language version unless the task requires a change. Use future LTS releases such as .NET 12 or 14 only after verifying their actual release, support, and tooling compatibility. Explain and seek necessary approval before framework upgrades, preview features, or new packages.
- Do not add XML documentation comments (`///`). Explain non-obvious reasons in ordinary comments (`//` or `/* */`). Preserve existing comments unless the change makes them inaccurate.

## Work mode, roles, and models

- **Use subagents by default.** Work alone without creating any only when the user explicitly says not to use subagents for the task. If the user gives no subagent instruction, or explicitly requests subagents, assign the five distinct roles below to separate agents. Do not reverse an explicit user choice during the task.
- In solo mode, one agent owns scope, design, UI review when applicable, implementation, self-verification, and the final decision. Do not claim an independent QC review. Report required user decisions or Visual Studio access limits honestly.
- In multiagent mode only, select the models below at `High` reasoning level when starting the agents. Do not claim an already running agent switched models. If a model or slot is unavailable, report the constraint to the user instead of silently substituting or claiming five-agent participation.

| Role | Model | Responsibility |
| --- | --- | --- |
| Project manager (PM) | GPT-6 Sol High | Scope, acceptance criteria, priorities, assignments, conflict resolution, final review and completion decision |
| System designer | GPT-6 Sol High | Existing architecture and reuse candidates, interfaces, impact, work boundaries, verification plan, precise developer instructions |
| GUI designer | GPT-5.6 Terra High | For UI work, review WinForms screens, designer editing, options, and events; for headless libraries, review public API usability without inventing UI deliverables and mark UI checks not applicable |
| Software developer | GPT-5.6 Terra High | Reuse-first implementation, builds and runtime evidence, blockers and results |
| Program review and verification QC | GPT-5.6 Terra High | Independent review against criteria, reproducible defects and unverified areas, re-verification |

In multiagent mode, follow this sequence:

1. Have the PM define the objective and acceptance criteria. Have the system designer map affected code, reuse paths, file/interface ownership, and verification. Higher-tier agents must specify input files, behavior, edge cases, and required evidence so execution agents need not guess.
2. Share decisions in short handoffs. For UI work, GUI designer and developer agree on designer-managed UI versus runtime logic. Skip designer steps when there is no UI. Sequence architecture decisions and shared-file edits.
3. Run materially time-consuming independent reconnaissance, implementation, and verification in parallel when slots, CPU, memory, and build topology allow. Do not create shared-file edit conflicts or parallelize dependent steps for appearance's sake. PM integrates outcomes and assigns missing validation.
4. QC reports a pass or an evidence-backed finding to PM. On a finding, PM confirms the issue, discusses the fix with the system designer, reassigns work, and has QC re-verify. Even after QC passes, PM checks the original acceptance criteria and decides whether work is complete.

## Implementation and dependencies

- Choose the smallest change that meets the requirement. Search existing project code, helpers, SDK wrappers, and relevant UI controls first; then consider .NET standard library and applicable platform capabilities. Do not add unneeded features, layers, interfaces, or packages.
- Before adding a third-party package, present the need, in-project and built-in alternatives, candidate/version, license, transitive dependencies, deployment, and maintenance impact to the user, and obtain approval for the direction. In multiagent mode, PM coordinates this decision. Do not install or add it beforehand.
- Use only APIs available for the target framework and language version. Explain impacts on existing public APIs, serialized formats, and native ABI before changing them. Where nullable analysis is enabled, express nullability in types and fix warning causes. Use `!` or warning suppressions only for proven local exceptions and explain why in an ordinary comment.
- Define ownership and cleanup for owned `IDisposable`/`IAsyncDisposable` objects, event subscriptions, timers, streams, camera/native handles. Do not dispose borrowed shared objects without an ownership contract. Validate external input and SDK results at boundaries; do not swallow exceptions or leave empty `catch` blocks. Use the project's existing user-message and diagnostic-logging patterns appropriately.
- When a library needs asynchronous APIs, use `Task`/`Task<T>` and appropriate `CancellationToken` support; define error and cancellation behavior. Do not indiscriminately wrap a library's synchronous API in `Task.Run`. Define ownership and synchronization of shared mutable state and document thread-safety assumptions for exposed APIs.
- Use `async void` only for event handlers. Observe asynchronous exceptions and avoid deadlocks caused by synchronous waits.

## For WinForms UI work only: Visual Studio designer contract

Do not apply this section or the following UI responsiveness section, or require UI deliverables, for any task without UI.

- Add and edit forms, `UserControl` instances, control layouts, and designer-supported property/event wiring **through the Visual Studio designer**. Do not manually insert runtime UI creation, layout, or event wiring into designer-managed `.Designer.cs`/`.resx` sections. Use code for UI creation or wiring only after confirming that the designer cannot represent that specific case; report why and which portion becomes non-editable in the designer.
- Prefer visually designable `UserControl` for composed reusable UI. Use code-based UI only for the necessary portion when custom drawing or another requirement cannot be configured in the designer. Constructors, property setters, and `Load` must not depend on devices, networking, long-running work, runtime-only services, or modal UI at design time.
- Put public custom options of each `UserControl` or custom UI in **one project-defined options category** (for example `Coffee Options`), and custom events in **one separate events category** (for example `Coffee Events`). Reuse established category names when present. Apply `Category` and meaningful `Description` metadata to each member. Expose custom events as standard .NET events that can be created and edited in the designer's **Events tab**.
- Only when an established pattern or concrete need calls for a grouped options object, expose a public expandable options object. Apply `ExpandableObjectConverter` to the options type, `DesignerSerializationVisibility.Content` to the property, and suitable `Browsable`/default/serialization behavior. Remember that `DefaultValue` metadata does not initialize the runtime value; use `ShouldSerializeX`/`ResetX` where appropriate. For simple properties, a shared category provides grouping. Verify values persist after saving.
- Actually open the designer, add the control, edit options, wire custom events, save, close, reopen, and check runtime behavior. If the Visual Studio designer is unavailable, do not substitute arbitrary `.Designer.cs` edits for supported UI work: report the blocked UI task and unverified criteria to the user and, in multiagent mode, to PM. If a modern .NET designer extension is essential, do not copy a .NET Framework-only designer example without verifying the target Visual Studio/.NET combination.

## UI responsiveness and work lifetime

- Never run long I/O, synchronous device calls, CPU-heavy calculations, waits, locks, `.Result`, or `.Wait()` on the UI thread. Use real asynchronous I/O APIs with `await` where available. Run CPU work or long synchronous SDK calls on a suitable worker only after checking the device's threading constraints. Do not wrap all work indiscriminately in `Task.Run`.
- For work started by UI event handlers, handle cancellation, timeouts, exceptions, duplicate activation, and restoration of UI state. Define the lifetime of long-running operations and cancel them when the owning form/control closes or is disposed.
- Do not access WinForms controls directly from background work. On .NET 9 or later, consider `Control.InvokeAsync` first when it fits the existing project; otherwise use a UI-thread dispatch approach supported by the target framework. Keep callbacks brief, handle controls already closed or disposed, and limit progress update frequency.
- Check clicking, scrolling, moving, and closing the window during real work, including error and cancellation paths. Do not claim an impossible absolute zero-latency guarantee; repair observed freezes or bottlenecks and recheck.

## Verification and completion report

- Build the exact target solution/configuration (Debug/Release) and platform (such as x64), and leave no new compiler, nullable, or analyzer warnings in changed projects. Report pre-existing baseline warnings separately. Verify changed pure logic on success and failure boundaries with the project's existing test approach. For external SDK, camera, or networking changes, run the actual Debug path when possible and exercise initialization, normal use, failure, cancellation/shutdown, and cleanup.
- For UI changes, verify designer opening, editing, saving, reopening, and runtime behavior in Visual Studio. A CI/CLI build alone does not prove designer behavior or UI responsiveness. Do not mark untested criteria as passed when Windows, tools, or hardware are unavailable.
- In solo mode, the responsible agent checks changed files, reuse evidence, actual test outcomes, unverified areas, and risks, then reports the final result. In multiagent mode, each owner sends that evidence to PM and QC. QC distinguishes verified defects from suggestions; PM checks all acceptance criteria and QC re-verification before completion.
