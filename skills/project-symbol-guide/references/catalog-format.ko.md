# 심볼 목록 형식

목록 생성·갱신 시 사용합니다. 같은 근거·최신성·검색 요건을 충족하는 프로젝트 기존 형식이 있다면 유지합니다.

## 색인

`docs/project-analysis/index.json`에 UTF-8 JSON으로 저장합니다. 경로는 프로젝트 루트 기준이며 `/`로 구분합니다. 시각은 시간대가 명시된 ISO 8601입니다. 특정 컴퓨터의 절대 프로젝트 경로를 저장하지 않습니다. 아래 예시 이름 대신 실제 프로젝트에서 확인한 값을 사용합니다.

```json
{
  "schemaVersion": "1.0",
  "updatedAt": "2026-10-22T14:00:00+09:00",
  "project": {"name": "MotionApp", "root": "."},
  "coverage": {
    "status": "partial",
    "requestedScope": ["src/**"],
    "pendingFiles": ["src/Display.cpp"],
    "excluded": [{"path": "vendor/**", "reason": "외부 라이브러리 소스"}],
    "configurations": ["Debug|x64"],
    "limitations": ["함수 포인터 호출 대상 미해결"],
    "localsPolicy": "동작·상태 전이·재사용에 영향을 주는 매개변수와 지역 변수"
  },
  "sources": [
    {"path": "src/Axis.h", "sha256": "actual-content-sha256", "owners": ["class:Motion.Axis"]},
    {"path": "src/Axis.cpp", "sha256": "actual-content-sha256", "owners": ["class:Motion.Axis"]}
  ],
  "owners": [
    {"id": "class:Motion.Axis", "qualifiedName": "Motion::Axis", "kind": "class", "catalog": "docs/project-analysis/classes/motion-axis.md"}
  ],
  "symbols": [
    {"id": "var:Motion.Axis.position", "owner": "class:Motion.Axis", "kind": "field", "qualifiedName": "Motion::Axis::position", "signature": "double position", "summary": "현재 축 위치", "tags": ["position", "axis", "위치"], "catalog": "docs/project-analysis/classes/motion-axis.md#var-position", "declarations": [{"path": "src/Axis.h", "line": 12}], "definitions": []},
    {"id": "fn:Motion.Axis.Move(double)", "owner": "class:Motion.Axis", "kind": "method", "qualifiedName": "Motion::Axis::Move", "signature": "bool Move(double target)", "summary": "축 이동 요청", "tags": ["motion", "이동"], "catalog": "docs/project-analysis/classes/motion-axis.md#fn-move-double", "declarations": [{"path": "src/Axis.h", "line": 18}], "definitions": [{"path": "src/Axis.cpp", "line": 42}]}
  ],
  "validation": {"status": "not-run", "details": "분석만 수행"}
}
```

`coverage.status`는 `requestedScope` 기준 `partial` 또는 `complete`입니다. 포함 파일을 모두 조사하고 범위 내 선언을 전부 목록화해야 `complete`로 표시하며 의미 해석의 한계는 별도 기록합니다. `sources`에는 분석한 파일과 실제 분석한 바이트의 지문을 저장합니다. 새로 발견한 파일을 포함하여 미분석 파일은 `pendingFiles`에 넣습니다. 요청 범위의 모든 파일을 분석·대기·이유 있는 제외 중 하나로 설명해야 합니다. 갱신 시 파일 목록을 다시 열거합니다. 기존 해시 비교만으로는 새 파일·삭제 파일을 놓칩니다. Git이 없는 프로젝트도 동일하게 목록·내용 비교를 사용합니다.

파일 지문은 영향받는 모든 심볼과 관계를 정합화한 뒤 갱신합니다. 분석 도중 파일이 바뀌면 다시 읽거나 대기로 남기며, 분석하지 않은 바이트의 지문을 저장하지 않습니다. 미해결 관계는 소유자 문서에 기록합니다. 변수 선언이 곧 정의이면 `definitions`는 빈 배열일 수 있습니다. 외부 심볼이나 선언만 확인한 심볼은 소유자 문서에 명시합니다.

## ID와 위치

- 가능하면 컴파일러 고유의 안정적 ID를 사용합니다. 없으면 프로젝트/모듈, 소유자와 한정 이름, 심볼 종류, 정규화한 매개변수 자료형, 제네릭 차수, 오버로드 구분에 필요한 메서드 속성으로 구성합니다. 파일 내부 심볼은 상대 소스 경로를 포함합니다. 일반적으로 반환형만으로 오버로드를 식별하지 않으며 언어별 추가 구분자가 필요하면 포함합니다.
- 줄 번호를 ID로 쓰지 않습니다. 구현만 수정되면 ID를 유지하고 심볼 정체성이 바뀌면 연결 항목을 갱신합니다. 소유자 파일명 충돌을 피하고 각 심볼에 고유한 HTML 앵커를 둡니다.
- 선언 위치와 정의 위치를 따로 저장합니다. 공유 선언, partial 클래스, 템플릿, 구성별 위치는 여러 항목과 구성 설명이 필요할 수 있습니다.
- JSON 경로는 프로젝트 루트 기준입니다. Markdown 링크는 해당 문서 기준으로 계산하고 실제 소스에 연결되는지 확인합니다. 편집 후 줄 번호를 갱신하며 링크를 따라 행동하기 전 한정 심볼을 확인합니다.

## 소유자 문서

클래스 또는 모듈 파일에는 간결한 표와 필요한 심볼별 상세 절로 다음을 기록합니다.

1. 소유자 ID, 한정 이름, 책임, 기반 클래스/인터페이스, 소스 링크, 분석한 구성, 범위 한계.
2. 변수 표: 심볼 ID/링크, 이름, 자료형, 접근 범위, 저장 종류, 용도, 안전한 초기값/기본값, 범위·단위, 선언 링크. 개별 상세에는 수명, 스레드·소유권 제약, 함수 ID로 연결한 확인된 읽기/쓰기 함수와 근거를 둡니다.
3. 함수 표: 심볼 ID/링크, 전체 서명, 접근 범위/속성, 용도, 선언·구현 링크. 개별 상세에는 입력/출력/오류, 사전 조건, 효과, 읽기/쓰기 변수 ID, 호출자/피호출자 ID, 제약, 호출 예, 테스트를 둡니다.
4. 미해결 관계와 검증 상태. 각 미해결 관계는 대상을 지어내지 말고 소스 근거, 불확실성, 관련 구성을 기록합니다.

`<a id="var-position"></a>`, `<a id="fn-move-double"></a>` 같은 명시적 HTML 앵커로 제목이 바뀌어도 링크를 유지합니다. 범위 밖/외부 대상은 연결되지 않는 내부 ID 대신 한정 이름과 근거에 `external` 또는 `not-analyzed` 표시를 붙입니다. 확인하지 못했거나 무관한 의미 필드는 `unknown` 또는 `not-applicable`로 표시합니다. 빈 배열은 명시한 범위에서 관찰되지 않았다는 의미만 가집니다.

변수 → 읽기/쓰기 함수와 함수 → 읽기/쓰기 변수의 양방향 항목을 일치시킵니다. 양쪽이 목록화된 호출자 ↔ 피호출자도 동일합니다. 관계는 `observed`, `inferred`, `unresolved`로 구분하고 추론한 관계에는 이유를 남깁니다. 편집 파일이 변경되지 않은 파일의 역참조에도 영향을 주면 해당 기록도 확인합니다.

## 제안 경계

실제 소스에 존재하는 심볼만 색인에 등록합니다. 없는 심볼 제안은 현재 응답 또는 프로젝트의 기존 제안 문서에 두고 기존 심볼과 분리합니다. 승인 후 구현했을 때 실제 ID·위치로 등록하고 색인과 소유자 문서를 함께 갱신합니다. 제안한 함수는 승인 전 소스의 선언, 함수 틀, 람다, 구현으로 만들지 않습니다.

## 완료 확인

JSON 구문, 소유자/심볼 ID 고유성, 소유자 연결, 실제 소스 경로, 문서·앵커, 목록 내 ID 또는 외부로 명시한 대상의 참조를 확인합니다. 범위 내 파일 목록, 분석 지문, 변경·삭제 심볼, 양방향 관계, 대표 소스 링크를 현재 코드와 대조합니다. 구현 변경에는 관련 프로젝트 검증을 수행하고 실제 결과를 기록합니다. 목록만 수정했다면 빌드·테스트를 수행했다고 보고하지 않습니다.
