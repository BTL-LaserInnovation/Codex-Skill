# Mocha 레이아웃 참고

이 문서는 현재 Mocha 파일을 직접 검사하는 것을 대신하지 않는 탐색 보조 자료입니다. 2026-09-23에 Machine 범위의 `PathMocha=C:\Mocha\` 환경 변수에서 관찰했습니다.

## 저장소 구조

`C:\Mocha`는 Visual Studio C++/MFC와 OpenCV 기반 라이브러리 저장소입니다. `include` 아래에 소스/헤더 463개, `.vcxproj` 73개, `lib`의 `.lib` 78개, `lib.static`의 `.lib` 68개가 있습니다.

| 경로 | 용도 |
| --- | --- |
| `all.sln` | 주 솔루션 및 프로젝트 의존성 그래프 |
| `include/<Module>` | 공용 헤더와 모듈 외부 계약 |
| `src/<Module>` | 모듈 구현과 Visual C++ 프로젝트 파일 |
| `lib` | 종속 프로젝트가 사용하는 빌드/임포트 라이브러리 |
| `lib.static` | 종속 프로젝트가 사용하는 정적 라이브러리 |
| `bin` | 실행 파일과 DLL 런타임 출력 |
| `common.props` | OpenCV 경로 매크로를 포함한 공용 MSBuild 속성 |
| `SetMochaEnvironmentPath` | `PathMocha`와 런타임 PATH를 설정하는 스크립트. 일반 참조 작업에서 실행하지 않음 |

주요 재사용 영역은 MFC 컨트롤/유틸리티의 `misc`, 좌표/수학 유틸리티의 `xMathUtil`, 도면/CAD의 `Shape`, 카메라 및 벤더 플러그인의 `FrameGrabber`, 영상 처리의 `ImageProcessor`와 `Vision`, 그리고 `PLC`, `HSMS`, `Scanner`, `3DCloudView`, `QMisc`입니다.

## 확인된 빌드 규칙

- 프로젝트는 보통 `$(SolutionDir)common.props`를 import하고 `$(SolutionDir)include`, `$(SolutionDir)lib`, `$(SolutionDir)lib.static`을 사용합니다.
- 일반 구성은 Debug/Release x64이며, 일부 프로젝트에는 Debug.XP/Release.XP x64가 있습니다. 확인한 `misc` 프로젝트는 v145, 동적 MFC, Unicode를 사용합니다.
- `.vcxproj`를 직접 MSBuild로 빌드할 때 `common.props`와 공용 경로를 해석하려면 `/p:SolutionDir=C:\Mocha\`가 필요합니다. `all.sln`을 통해 빌드하면 이 문맥이 보통 설정됩니다.
- `common.props`는 `OpenCVRoot`, `OpenCVInclude`, `OpenCVLib`를 정의하며 별도 값이 없으면 `OpenCVRoot`는 `C:\OpenCV`를 기본값으로 사용합니다.
