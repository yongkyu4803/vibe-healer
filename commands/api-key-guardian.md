---
description: "API 키 노출, 불안전한 .env 처리, .gitignore 미보호, 하드코딩된 시크릿, 클라이언트 측 시크릿 사용을 점검한다."
allowed-tools: [Bash, Read]
---

# /healer:api-key-guardian

$ARGUMENTS

API 키와 환경 변수가 안전하게 관리되고 있는지 확인해드립니다.

## 워크플로우

1. 가능하면 `scripts/secret_scan.py --path . --json`을 실행한다.
2. `.gitignore`, `.env*`, 클라이언트 파일, 서버 라우트, 설정 파일을 검사한다.
3. 모든 시크릿 값을 마스킹한다.
4. 값이 서버 측에 있어야 하는지 공개 가능한지 설명한다.
5. 실제 값 없이 `.env.example` 키를 제안한다.
6. `.gitignore` 수정, Git에서 파일 제거, 템플릿 생성 전 확인을 받는다.

## 고위험 신호

- `app/`, `pages/`, `src/components/`, `public/`, 정적 JS 파일에 실제 시크릿 포함.
- `NEXT_PUBLIC_*`에 비공개 키 할당.
- `.env` 또는 `.env.local`이 Git에 의해 무시되지 않음.
- 커밋된 히스토리나 staged diff에 시크릿 포함.

## 출력 형식

```
Diagnosis:
Likely cause:
Do this first:
Verification:
Safety note:
```

긴급 유출 위험과 정리 권장 사항을 분리해서 출력한다.

## 안전 규칙

- 완전한 시크릿을 절대 출력하지 않는다. `[REDACTED]` 또는 마스킹된 미리보기만 사용.
- `.gitignore` 수정, Git 히스토리 재작성은 확인 후 실행한다.
