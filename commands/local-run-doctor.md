---
description: "로컬 프로젝트 실행 방법을 진단하고 시작 오류를 해결한다. Next.js, Vite, Streamlit, Flask, 일반 Python, 정적 HTML 프로젝트 타입 감지 지원."
allowed-tools: [Bash, Read]
---

# /vibe-healer:local-run-doctor

$ARGUMENTS

로컬에서 프로젝트가 실행되지 않을 때, 프로젝트 타입을 감지하고 가장 안전한 실행 명령을 찾아드립니다.

## 검사 항목

- `package.json`, lockfile, 스크립트
- `requirements.txt`, `pyproject.toml`, `Pipfile`, 앱 진입 파일
- `app.py`, `main.py`, `streamlit_app.py`, `src/`, `app/`, `pages/`, `index.html`
- `.env.example`, README 실행 지침

## 워크플로우

1. 프로젝트 루트를 먼저 검사한다.
2. 가능하면 `scripts/detect_project.py --path .`를 실행한다.
3. 프로젝트 타입이 불명확하면 `references/project-types.md`를 참조한다.
4. 포트, 의존성, 명령 실패가 있으면 `references/local-run-troubleshooting.md`를 참조한다.
5. 기본 명령 1개 + 검증 확인 1개를 반환한다.

## 신뢰도별 응답

- **높음**: 실행 명령을 바로 제공한다.
- **보통**: 이유를 설명하고 의존성 설치 전 허락을 구한다.
- **낮음**: 파일 목록이나 에러 로그를 요청한다. 추측하지 않는다.

## 출력 형식

```
Diagnosis:
Likely cause:
Do this first:
Verification:
Safety note:
```

## 안전 규칙

- lockfile 삭제, 전체 재설치를 첫 번째 조치로 제안하지 않는다.
- 의존성 설치 전 확인을 받는다.
