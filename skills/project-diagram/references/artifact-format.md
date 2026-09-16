# Project diagram artifact format

`project-diagram.mmd` is the renderable overview. Start it with a Mermaid comment carrying `schemaVersion`, `updatedAt` (UTC ISO 8601), and the matching index filename. Use `flowchart` or `C4` syntax supported by the chosen renderer. Each visible node must show the same stable component ID used in the index; edges are directed and labelled with the relationship or flow.

`project-diagram.index.json` is UTF-8 JSON with this shape:

```json
{
  "schemaVersion": "1.0",
  "updatedAt": "2026-09-17T00:00:00Z",
  "source": { "diagram": "project-diagram.mmd", "scope": "repository-root" },
  "components": [
    {
      "id": "web-api",
      "name": "Web API",
      "kind": "service",
      "files": ["src/WebApi/WebApi.csproj", "src/WebApi/Program.cs"],
      "symbols": ["WebApi.Program"],
      "responsibilities": ["HTTP entry point"],
      "tests": ["tests/WebApi.Tests/WebApi.Tests.csproj"]
    }
  ],
  "relationships": [
    {
      "from": "web-api",
      "to": "domain",
      "kind": "uses",
      "label": "application commands",
      "evidence": ["src/WebApi/WebApi.csproj"]
    }
  ],
  "flows": [
    {
      "id": "submit-order",
      "kind": "control",
      "steps": ["web-api", "application", "domain", "order-store"]
    }
  ],
  "changeNote": "Added order submission flow."
}
```

Allowed `kind` values are project, application, service, module, library, ui, database, queue, external-system, test, and other. Add a `status` or `notes` field only when it changes implementation decisions. File paths are project-root-relative, slash-separated, and must point to a tracked file or a documented generated file. `symbols` should be qualified names, exported APIs, routes, resource IDs, or another stable project-native identifier; omit them when none is reliable.

For a partial or early map, make incompleteness explicit with `source.scope` (for example `solution:App.sln` or `modules:auth,billing`) and a short `notes` value. Never silently present a partial map as the whole repository.

