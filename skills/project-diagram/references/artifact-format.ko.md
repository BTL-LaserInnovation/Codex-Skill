# 프로젝트 다이어그램 산출물 형식

`project-diagram.mmd`는 렌더링 가능한 개요입니다. 첫 부분에 `schemaVersion`, UTC ISO 8601 형식의 `updatedAt`, 연결된 인덱스 파일명을 담은 Mermaid 주석을 둡니다. 선택한 렌더러가 지원하는 `flowchart` 또는 `C4` 문법을 사용합니다. 보이는 모든 노드는 인덱스와 같은 안정적인 구성 요소 ID를 표시하고, 엣지는 방향과 관계/흐름 레이블을 가집니다.

`project-diagram.index.json`은 UTF-8 JSON이며 다음 구조를 사용합니다.

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

`kind`에는 project, application, service, module, library, ui, database, queue, external-system, test, other를 사용합니다. 구현 판단에 영향을 줄 때만 `status` 또는 `notes` 필드를 추가합니다. 파일 경로는 프로젝트 루트 기준이며 슬래시(`/`)로 구분하고, 추적 중인 파일 또는 문서화된 생성 파일을 가리켜야 합니다. `symbols`는 정규화된 이름, 공개 API, 경로, 리소스 ID 등 프로젝트 내에서 안정적인 식별자이며 신뢰할 수 있는 식별자가 없으면 생략합니다.

부분 지도 또는 초기 지도라면 `source.scope`에 범위(예: `solution:App.sln`, `modules:auth,billing`)를 명시하고 짧은 `notes`를 둡니다. 부분 지도를 저장소 전체 지도처럼 표시하지 않습니다.

