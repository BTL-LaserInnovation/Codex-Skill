# Mocha Layout Reference

This is a discovery aid for the live Mocha library, not a replacement for inspecting the current files. It was observed on 2026-09-23 with `PathMocha` set to `C:\Mocha\` at the Machine scope.

## Repository structure

`C:\Mocha` is a Visual Studio C++/MFC and OpenCV library repository. It contains 73 `.vcxproj` projects, 463 source/header files under `include`, 78 `.lib` files under `lib`, and 68 `.lib` files under `lib.static`.

| Path | Purpose |
| --- | --- |
| `all.sln` | Primary solution and project dependency graph. |
| `include/<Module>` | Public headers and module-facing contracts. |
| `src/<Module>` | Module implementation and Visual C++ project files. |
| `lib` | Built/import libraries used by dependent projects. |
| `lib.static` | Static libraries used by dependent projects. |
| `bin` | Runtime executables and DLL outputs. |
| `common.props` | Shared MSBuild properties, including OpenCV path macros. |
| `SetMochaEnvironmentPath` | Scripts that establish `PathMocha` and runtime PATH entries; do not run during ordinary reference work. |

Common reusable areas include `misc` (MFC controls and utilities), `xMathUtil` (coordinate/math utilities), `Shape` (drawing/CAD), `FrameGrabber` (camera acquisition and vendor plugins), `ImageProcessor` and `Vision` (image processing), `PLC`, `HSMS`, `Scanner`, `3DCloudView`, and `QMisc`.

## Build conventions observed

- Projects commonly import `$(SolutionDir)common.props` and use `$(SolutionDir)include`, `$(SolutionDir)lib`, and `$(SolutionDir)lib.static`.
- Typical configurations are Debug/Release x64, plus Debug.XP/Release.XP x64 in some projects; the observed toolset is v145, with dynamic MFC and Unicode in the `misc` project.
- A direct `.vcxproj` MSBuild invocation needs `/p:SolutionDir=C:\Mocha\` so the common property sheet and shared paths resolve. Building through `all.sln` establishes this context normally.
- `common.props` defines `OpenCVRoot`, `OpenCVInclude`, and `OpenCVLib`, defaulting OpenCVRoot to `C:\OpenCV` when it is not otherwise supplied.
