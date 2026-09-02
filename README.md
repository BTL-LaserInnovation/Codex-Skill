# Codex Skill Hub

팀원이 재사용 가능한 Codex 스킬을 제안하고 검토·배포하는 공동 저장소입니다.

## 저장소 구조

- `skills/<skill-name>/SKILL.md`: 배포 가능한 스킬. 폴더명과 YAML `name`은 같아야 합니다.
- `skills/<skill-name>/agents/openai.yaml`: 필요한 경우에만 두는 UI 메타데이터입니다.
- `templates/skill-template/`: 새 스킬을 만들 때 복사하는 최소 템플릿입니다.
- `scripts/validate_skills.py`: 모든 스킬의 기본 구조를 검사합니다.

## 스킬 추가 방법

1. 저장소를 fork하고 작업 브랜치를 만듭니다.
2. `templates/skill-template`을 `skills/<소문자-하이픈-이름>`으로 복사합니다.
3. `SKILL.md`의 YAML 메타데이터와 작업 지침을 작성합니다. 지침에는 역할, 적용 조건, 실제 제약만 담고 일반적인 Codex 사용법은 중복하지 않습니다.
4. `python scripts/validate_skills.py`를 실행합니다.
5. Pull Request를 열고, 목적·적용 예시·검증 결과를 작성합니다. 검토가 승인된 뒤에만 `master`에 병합합니다.

## 운영 권장 설정

저장소 관리자는 GitHub Settings에서 다음을 설정합니다.

- `master` 브랜치에 직접 푸시를 금지하고 Pull Request를 필수화합니다.
- 병합 전 `Validate skills` 상태 검사를 필수화합니다.
- 최소 1명의 승인과 최신 `master` 재검증을 요구합니다.
- 필요한 경우 CODEOWNERS 또는 팀별 리뷰어를 지정합니다.

스킬은 저장소에서 검토되는 원본입니다. 각 사용자는 승인된 버전을 자신의 Codex skills 디렉터리에 설치하거나, 조직의 배포 절차를 통해 동기화합니다.
