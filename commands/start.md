---
description: "Vibe Healer 트리아지 허브. 현재 프로젝트 상태를 자동 감지해서 지금 당장 써야 할 헬러 스킬 하나를 골라준다."
allowed-tools: [Bash, Read]
---

# /vibe-healer:start

막혔을 때 어떤 헬러를 써야 할지 자동으로 찾아드립니다.

## 실행 절차

### 1. 현재 위치 출력

```bash
echo "📍 작업 위치: $(pwd)"
```

### 2. 프로젝트 상태 스캔

아래 항목을 한 번에 확인한다.

```bash
echo "=== 프로젝트 타입 ===" && \
ls package.json requirements.txt pyproject.toml app.py streamlit_app.py 2>/dev/null || echo "(없음)" && \
echo "=== Git 상태 ===" && \
git status --short 2>/dev/null | head -20 || echo "Git 없음" && \
echo "=== .env 파일 ===" && \
ls -1 .env .env.local .env.development .env.production 2>/dev/null || echo "(없음)" && \
echo "=== .gitignore에 .env 보호 여부 ===" && \
grep -l "^\.env" .gitignore 2>/dev/null || echo "(보호 없음 또는 .gitignore 없음)" && \
echo "=== 최근 오류 로그 ===" && \
ls -1t *.log npm-debug.log* .next/server/*.log 2>/dev/null | head -5 || echo "(없음)"
```

### 3. 진단 우선순위 (아래 순서로 가장 먼저 해당하는 것 하나만 추천)

| 우선순위 | 감지 조건 | 추천 커맨드 | 이유 |
|---------|-----------|-------------|------|
| 1 | `.env` 파일이 있는데 `.gitignore`에 보호 없음 | `/vibe-healer:api-key-guardian` | API 키 노출 위험이 가장 위험함 |
| 2 | Git 추적 파일에 `.env*`, `*secret*`, `*token*` 포함 | `/vibe-healer:api-key-guardian` | 커밋 직전 유출 위험 |
| 3 | `package.json` / `requirements.txt` 없음, 또는 프로젝트 타입 불명확 | `/vibe-healer:local-run-doctor` | 실행 방법부터 확인 필요 |
| 4 | 사용자가 오류 로그 또는 에러 메시지를 붙여넣었거나, `*.log` 파일 존재 | `/vibe-healer:error-doctor` | 에러 먼저 분류 |
| 5 | Git 변경사항이 있고 커밋 안 됨 (modified/untracked 파일 多) | `/vibe-healer:git-savepoint` | 위험 작업 전 체크포인트 |
| 6 | 사용자가 "배포 실패", "Vercel", "Render", "Streamlit Cloud" 언급 | `/vibe-healer:deploy-fixer` | 배포 로그 분석 필요 |
| 7 | 사용자가 스크린샷을 첨부하거나 "화면이 이상해" 언급 | `/vibe-healer:ui-screenshot-reviewer` | 화면 문제는 눈으로 봐야 함 |
| — | 위 조건 없음 | 현황만 출력 후 직접 선택 안내 | |

### 4. 결과 출력 형식

```
🩺 Vibe Healer 트리아지 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

프로젝트 현황:
  [✅ or ⬜] 프로젝트 타입 감지됨    (예: Next.js / Flask / Streamlit)
  [✅ or ⬜] .env 보안 설정됨
  [✅ or ⬜] Git 초기화됨
  [✅ or ⬜] 커밋 정리됨

⚡ 지금 당장 이걸 쓰세요:

  /vibe-healer:<스킬명>
  이유: <한 줄 이유>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
전체 도구 목록:
  /vibe-healer:local-run-doctor      — 로컬 실행이 안 될 때
  /vibe-healer:error-doctor          — 터미널 에러 해석
  /vibe-healer:api-key-guardian      — API 키·.env 안전 점검
  /vibe-healer:git-savepoint         — 커밋 전 체크포인트
  /vibe-healer:deploy-fixer          — 배포 실패 진단
  /vibe-healer:ui-screenshot-reviewer — 화면이 이상할 때
```

### 5. 안전 규칙

- 스캔 결과에서 실제 API 키 값은 절대 출력하지 않는다.
- 파일 수정, 커밋, 배포는 이 커맨드에서 직접 하지 않는다.
- 진단만 하고, 실행은 사용자가 해당 커맨드를 직접 호출하게 안내한다.
