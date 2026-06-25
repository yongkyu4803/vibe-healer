---
description: "터미널 로그, 빌드 실패, 런타임 에러, TypeScript 에러, Python traceback, 패키지 오류를 진단하고 첫 번째 수정 방법을 알려준다."
allowed-tools: [Bash, Read]
---

# /vibe-healer:error-doctor

$ARGUMENTS

에러 로그를 붙여넣으면 원인을 분류하고 가장 안전한 첫 번째 수정 방법을 알려드립니다.

## 분류 우선순위

1. 시크릿·API 키 노출 위험
2. 환경 변수 누락
3. 문법·컴파일 에러
4. 패키지 누락
5. 런타임 경로·import 에러
6. 버전 불일치
7. 포트 충돌
8. 권한 에러
9. 불명확 → 더 많은 컨텍스트 요청

## 워크플로우

1. 로그가 없으면 정확한 로그를 요청한다.
2. 가능하면 `scripts/classify_error.py`를 실행한다.
3. 프레임워크(Node/Python)에 맞는 패턴 파일을 참조한다.
4. 노이즈 줄의 마지막이 아닌 **첫 번째 의미 있는 에러 줄**을 찾는다.
5. 수정 방법 1개 + 검증 명령어 1개를 제시한다.

## 출력 형식

```
Diagnosis:
Likely cause:
Do this first:
Verification:
Safety note:
```

## 안전 규칙

- API 키, 토큰, 쿠키는 절대 출력하지 않는다.
- 파일 삭제, Git reset, 배포는 명시적 확인 없이 하지 않는다.
- 수정 전 읽기 전용 점검을 먼저 제안한다.
