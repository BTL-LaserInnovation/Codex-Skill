---
name: project-diagram
description: "Maintain a machine-readable project architecture diagram for code projects, use it to scope changes before implementation, and render it on request."
---

# Project Diagram

Use this skill when establishing, updating, reviewing, or visualizing a software project's structure. Its purpose is to preserve a compact, dependable architectural map so later work begins with the affected area rather than repeatedly reading the entire codebase.

## Diagram artifact

Keep the canonical artifact under the project root:

```text
docs/architecture/
├─ project-diagram.mmd       # human-readable Mermaid source and canonical render input
└─ project-diagram.index.json # machine-readable component, relationship, and source index
```

For an existing repository, preserve an established documentation location if it already has one. Do not store generated images as the source of truth. The Mermaid file and JSON index must agree, identify their generation/update time, and link each component to its relevant files and stable symbols. Read [the artifact format](references/artifact-format.md) when creating or materially revising either file.

Create or refresh the artifact after initial project composition, architecture changes, added or removed projects/modules, public interface changes, dependency changes, and meaningful UI or data-flow changes. Use the project's solution, manifests, build files, public interfaces, entry points, and targeted source inspection as evidence; do not infer relationships solely from filenames.

## Reference-first change workflow

Before planning or editing code:

1. Locate and read the diagram and JSON index. Identify the affected component IDs, neighbors, dependency direction, entry points, tests, and mapped source files.
2. Check whether the artifact covers the requested scope and whether recent repository changes make it stale. If it is stale, inspect only manifests, diffs, and the implicated files needed to refresh that area; do not treat a stale diagram as proof.
3. Form the implementation plan from the impacted subgraph, then read the actual target code and its direct contracts before changing it. The diagram narrows investigation; it never replaces source-level verification.
4. After the change and its validation, update the impacted nodes, edges, file/symbol mappings, relevant flows, timestamp, and change note. Remove obsolete mappings rather than leaving contradictory history.

Keep exploration proportional. A complete initial map can require broad analysis. For later work, begin with the indexed subgraph and expand only when an edge, contract, build result, or test shows that the change reaches farther.

## Visualization requests

When the user asks to see, image, export, or visualize the diagram, render the canonical Mermaid source with a deterministic Mermaid-compatible renderer. Prefer SVG for a crisp inspectable output; also produce PNG only when requested or required by the delivery surface. Save generated output under `docs/architecture/generated/` unless the project already has a documented generated-artifact location, and report the output path.

Do not redraw a technical architecture diagram with a generative image model: it can alter labels, relationships, and topology. If no compatible renderer is available, provide the Mermaid source and state the rendering limitation instead of inventing an image.

## Diagram quality

Model only information that guides implementation: deployable projects/apps, modules, shared libraries, data stores, external systems, UI boundaries, key data/control flows, and tests when they constrain a component. Collapse implementation-detail nodes that do not affect dependencies. Use stable IDs, directed labeled edges, and a small legend. Keep sensitive values, secrets, and irrelevant internal details out of both artifacts.

