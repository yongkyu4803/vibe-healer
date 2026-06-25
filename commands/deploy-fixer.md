---
description: "Vercel, Render, Streamlit Community Cloud 배포 실패를 진단한다. 로컬 빌드 성공인데 클라우드 빌드 실패, 빈 화면, env 누락 등을 처리한다."
allowed-tools: [Bash, Read]
---

# /healer:deploy-fixer

$ARGUMENTS

배포 로그를 붙여넣으면 코드 문제인지 플랫폼 설정 문제인지 구분해서 안전한 수정 방법을 알려드립니다.

## 워크플로우

1. 배포 플랫폼을 확인한다 (로그에 없으면 질문).
2. 배포 로그, 빌드 설정, 프레임워크 정보를 요청한다.
3. Vercel / Render / Streamlit 플랫폼별 참고 자료를 읽는다.
4. 실패 원인을 분류한다: 로컬 코드 / 빌드 명령 / 시작 명령 / 런타임 버전 / 의존성 / env 설정.
5. 코드 변경인지 플랫폼 대시보드 변경인지를 명확히 구분해서 설명한다.
6. push, redeploy, 외부 설정 변경 전 확인을 받는다.

## 일반 진단 분류

- 로컬도 빌드 실패: 코드 먼저 수정 (error-doctor 방식으로 접근).
- 클라우드만 빌드 실패: env 변수, Node/Python 버전, install 명령, 빌드 명령, 루트 디렉토리 확인.
- 배포 성공 후 앱 크래시: 런타임 로그와 시작 명령 확인.
- 빈 화면: 브라우저 콘솔, base path, 클라이언트 env 변수, 에셋 누락 확인.

## 출력 형식

```
Diagnosis:
Likely cause:
Do this first:
Verification:
Safety note:
```

## 안전 규칙

- 외부 플랫폼 설정 변경, push, redeploy는 확인 후 실행한다.
- API 키, 토큰은 절대 출력하지 않는다.
