---
description: "Git 상태를 점검하고 위험한 작업 전에 안전한 커밋 체크포인트를 만든다. 시크릿, 빌드 결과물, 테스트 출력은 커밋에서 제외한다."
allowed-tools: [Bash, Read]
---

# /healer:git-savepoint

$ARGUMENTS

지금 Git 상태를 확인하고, 위험한 수정 전에 안전한 저장 지점을 만들어드립니다.

## 워크플로우

1. `git status`로 현재 상태를 확인한다.
2. 가능하면 `scripts/git_status_summary.py --path . --json`을 실행한다.
3. 추적 중인 변경, 미추적 파일, 무시 파일, 수상한 파일을 설명한다.
4. 커밋할 것과 무시할 것을 권장한다.
5. 간결한 커밋 메시지를 제안한다.
6. `git add`, `git commit`, `git push` 전에 반드시 확인을 받는다.

## 커밋 안전 게이트

커밋 전 반드시 확인:
- `.env`, 키, 토큰, 자격증명 파일이 포함되어 있지 않은가.
- `.next/`, `dist/`, `build/`, `node_modules/` 같은 빌드 폴더가 없는가.
- `test-results/`, 리포트 폴더가 없는가 (의도한 경우 제외).
- 큰 바이너리 파일이 예상된 에셋인가.

## 출력 형식

```
Diagnosis:
Likely cause:
Do this first:
Verification:
Safety note:
```

## 안전 규칙

- `git reset --hard`, `git push --force` 등 파괴적 명령은 사용자가 명시적으로 이해하고 요청한 경우에만 실행한다.
- 외부 서비스(GitHub, 원격 저장소)에 push하기 전에 확인을 받는다.
