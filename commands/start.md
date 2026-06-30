---
description: "Vibe Healer 트리아지 허브. 빠른 트리아지 또는 전체 헬스체크(순차 실행) 중 선택한다."
allowed-tools: [Bash, Read, AskUserQuestion]
---

# /healer:start

막혔을 때 문제를 찾아드립니다. **빠른 진단** 또는 **처음부터 끝까지 전체 점검** 중 선택하세요.

---

## 0-PRE. 플러그인 최신 버전 동기화

아래 bash를 실행해서 GitHub 최신 버전과 비교하고, 새 버전이 있으면 자동으로 업데이트한다.

```bash
HEALER_SOURCE=""

# 저장된 소스 경로 확인
if [ -f "$HOME/.claude/.healer_source_path" ]; then
  CANDIDATE=$(cat "$HOME/.claude/.healer_source_path")
  if [ -f "$CANDIDATE/.claude-plugin/plugin.json" ]; then
    HEALER_SOURCE="$CANDIDATE"
  fi
fi

# fallback: git remote URL로 후보 탐색
if [ -z "$HEALER_SOURCE" ]; then
  for dir in "$HOME"/*vibe-healer* "$HOME"/*healer* "$HOME/.claude/plugins"/*; do
    if [ -d "$dir/.git" ]; then
      REMOTE_URL=$(git -C "$dir" remote get-url origin 2>/dev/null || true)
      if echo "$REMOTE_URL" | grep -q "yongkyu4803/vibe-healer"; then
        HEALER_SOURCE="$dir"
        echo "$dir" > "$HOME/.claude/.healer_source_path"
        break
      fi
    fi
  done
fi

if [ -n "$HEALER_SOURCE" ]; then
  LOCAL_VER=$(python3 -c "import json; print(json.load(open('$HEALER_SOURCE/.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo "0.0.0")
  REMOTE_VER=$(curl -sf "https://raw.githubusercontent.com/yongkyu4803/vibe-healer/main/.claude-plugin/plugin.json" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['version'])" 2>/dev/null || echo "")

  if [ -n "$REMOTE_VER" ] && [ "$LOCAL_VER" != "$REMOTE_VER" ]; then
    echo "⬆️  새 버전 발견: $LOCAL_VER → $REMOTE_VER — 업데이트 중..."
    git -C "$HEALER_SOURCE" pull origin main --quiet && \
      bash "$HEALER_SOURCE/scripts/install_claude_code.sh" && \
      echo "✅ $REMOTE_VER 업데이트 완료" || \
      echo "⚠️  업데이트 실패. 수동: cd $HEALER_SOURCE && git pull && bash scripts/install_claude_code.sh"
  else
    echo "✅ Vibe Healer v$LOCAL_VER (최신)"
  fi
else
  echo "ℹ️  소스 경로를 찾을 수 없어 업데이트를 건너뜁니다"
fi
```

---

## 0. 환경 확인

먼저 현재 위치와 기본 환경을 확인한다.

```bash
echo "📍 작업 위치: $(pwd)" && \
echo "=== 프로젝트 타입 ===" && \
ls package.json requirements.txt pyproject.toml app.py streamlit_app.py 2>/dev/null || echo "(없음)" && \
echo "=== Git 상태 ===" && \
git status --short 2>/dev/null | head -10 || echo "Git 없음" && \
echo "=== .env 파일 ===" && \
ls -1 .env .env.local .env.development .env.production 2>/dev/null || echo "(없음)"
```

---

## 1. 모드 선택

AskUserQuestion 도구로 아래 질문을 표시한다.

**질문**: "어떻게 점검할까요?"

**선택지**:
- **A. 빠른 트리아지** — 지금 가장 급한 문제 하나만 찾아서 알려줌 (1분)
- **B. 전체 헬스체크** — 모든 영역을 처음부터 끝까지 순서대로 점검 (초보자 추천, 5분)

---

## 2-A. 빠른 트리아지 모드

A를 선택한 경우, 아래 우선순위 표를 따라 가장 먼저 해당하는 항목 **하나만** 추천하고 멈춘다.

| 우선순위 | 감지 조건 | 추천 커맨드 |
|---------|-----------|-------------|
| 1 | `.env` 있는데 `.gitignore`에 보호 없음 | `/healer:api-key-guardian` |
| 2 | Git 추적 파일에 `.env*` · `*secret*` · `*token*` 포함 | `/healer:api-key-guardian` |
| 3 | `package.json` / `requirements.txt` 없거나 프로젝트 타입 불명확 | `/healer:local-run-doctor` |
| 4 | 오류 로그·에러 메시지 존재 | `/healer:error-doctor` |
| 5 | Git 변경사항 커밋 안 됨 (파일 多) | `/healer:git-savepoint` |
| 6 | "배포 실패" / Vercel / Render 언급 | `/healer:deploy-fixer` |
| 7 | 스크린샷 첨부 또는 "화면 이상" 언급 | `/healer:ui-screenshot-reviewer` |

**결과 출력 형식 (A 모드)**:

```
🩺 Vibe Healer — 빠른 트리아지
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ 지금 바로 이걸 실행하세요:

  /healer:<스킬명>
  이유: <한 줄 이유>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 2-B. 전체 헬스체크 모드 (순차 실행 하네스)

B를 선택한 경우, 아래 **5단계를 순서대로 모두 실행**한다.
각 단계 시작 전에 현재 단계 번호와 이름을 출력하고, 완료 후 결과를 요약한다.

---

### ▶ STEP 1 / 5 — 로컬 실행 진단

```
🚀 [1/5] 로컬 실행 진단 중...
```

아래를 순서대로 실행한다.

```bash
# 프로젝트 타입 감지
echo "--- 프로젝트 타입 ---" && \
([ -f package.json ] && cat package.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('Node.js:', d.get('name','?'), '| scripts:', list(d.get('scripts',{}).keys())[:5])" 2>/dev/null) || \
([ -f requirements.txt ] && echo "Python (requirements.txt)") || \
([ -f pyproject.toml ] && echo "Python (pyproject.toml)") || \
([ -f streamlit_app.py ] || [ -f app.py ] && echo "Python 앱") || \
echo "프로젝트 타입 불명확"
```

```bash
# Node.js 버전 & 의존성 상태
echo "--- Node.js 환경 ---" && \
node --version 2>/dev/null || echo "Node.js 없음" && \
([ -f package.json ] && ls node_modules 2>/dev/null | wc -l | xargs echo "node_modules 패키지 수:" || echo "node_modules 없음 (npm install 필요)") && \
echo "" && \
# Python 환경
echo "--- Python 환경 ---" && \
python3 --version 2>/dev/null || echo "Python3 없음" && \
([ -f requirements.txt ] && pip3 show -q flask fastapi streamlit 2>/dev/null | head -3 || echo "(Python 패키지 설치 상태 불명)")
```

```bash
# 실행 명령 추론
echo "--- 실행 방법 추론 ---" && \
([ -f package.json ] && python3 -c "
import json
d = json.load(open('package.json'))
scripts = d.get('scripts', {})
dev = scripts.get('dev') or scripts.get('start') or scripts.get('serve')
print('추천 명령:', 'npm run dev' if 'dev' in scripts else 'npm start' if 'start' in scripts else '확인 필요')
" 2>/dev/null) || \
([ -f streamlit_app.py ] && echo "추천 명령: streamlit run streamlit_app.py") || \
([ -f app.py ] && echo "추천 명령: python3 app.py") || \
echo "실행 명령 자동 감지 실패 — 직접 확인 필요"
```

결과를 아래 형식으로 요약한다:

```
✅ [1/5 완료] 로컬 실행 진단
  프로젝트 타입: <감지 결과>
  의존성 상태: <정상 / 미설치>
  추천 실행 명령: <명령어>
  ⚠️ 문제: <있으면 표시, 없으면 "이상 없음">
```

---

### ▶ STEP 2 / 5 — 에러 로그 분석

```
🔍 [2/5] 에러 로그 분석 중...
```

```bash
# 최근 로그 파일 확인
echo "--- 로그 파일 ---" && \
ls -1t *.log npm-debug.log* yarn-error.log .next/server/*.log 2>/dev/null | head -5 || echo "(로그 파일 없음)" && \
echo "" && \
# npm-debug 로그 마지막 20줄
([ -f npm-debug.log ] && echo "--- npm-debug.log 마지막 20줄 ---" && tail -20 npm-debug.log) || true && \
# .next 빌드 에러
([ -d .next ] && ls .next/server/ 2>/dev/null | grep "\.log" | head -3 || true)
```

```bash
# TypeScript 에러 확인
([ -f tsconfig.json ] && command -v npx >/dev/null && echo "--- TypeScript 타입 체크 ---" && npx tsc --noEmit 2>&1 | head -20 || echo "(TypeScript 없음)") && \
# Python traceback 패턴 검색
(find . -name "*.log" -newer package.json 2>/dev/null | head -3 | xargs grep -l "Traceback\|Error\|Exception" 2>/dev/null | head -3 || true)
```

결과를 아래 형식으로 요약한다:

```
✅ [2/5 완료] 에러 로그 분석
  로그 파일: <있음/없음>
  주요 에러 패턴: <있으면 표시, 없으면 "이상 없음">
  ⚠️ 문제: <있으면 표시, 없으면 "이상 없음">
```

---

### ▶ STEP 3 / 5 — API 키 보안 점검

```
🔑 [3/5] API 키 보안 점검 중...
```

```bash
# .env 파일 존재 & gitignore 보호 여부
echo "--- .env 파일 ---" && \
ls -1 .env .env.local .env.development .env.production .env.example 2>/dev/null || echo "(없음)" && \
echo "" && \
echo "--- .gitignore .env 보호 ---" && \
([ -f .gitignore ] && grep "\.env" .gitignore || echo "⚠️ .gitignore에 .env 보호 없음!")
```

```bash
# Git 추적 중인 민감 파일 탐지
echo "--- Git 추적 중인 민감 파일 ---" && \
git ls-files 2>/dev/null | grep -iE "\.env$|secret|token|password|credential|api.?key" | grep -v ".example" || echo "(없음 — 안전)" && \
echo "" && \
# 코드 내 하드코딩 패턴 탐지 (키 값은 출력하지 않음)
echo "--- 하드코딩 패턴 탐지 ---" && \
grep -rn --include="*.js" --include="*.ts" --include="*.py" \
  -E "(api_key|apiKey|API_KEY|secret|token|password)\s*=\s*['\"][a-zA-Z0-9_\-]{10,}" \
  . 2>/dev/null | grep -v "\.example\|test\|mock\|your_\|<" | \
  sed 's/=.*/= [REDACTED]/' | head -5 || echo "(없음 — 안전)"
```

결과를 아래 형식으로 요약한다:

```
✅ [3/5 완료] API 키 보안
  .env 파일: <있음/없음>
  .gitignore 보호: <✅ 있음 / ⚠️ 없음>
  하드코딩 패턴: <감지됨/없음>
  ⚠️ 문제: <있으면 표시, 없으면 "이상 없음">
```

> 실제 키 값은 절대 출력하지 않는다.

---

### ▶ STEP 4 / 5 — Git 상태 점검

```
💾 [4/5] Git 상태 점검 중...
```

```bash
# Git 초기화 여부
echo "--- Git 상태 ---" && \
git status --short 2>/dev/null | head -20 || echo "⚠️ Git 미초기화" && \
echo "" && \
# 마지막 커밋
echo "--- 마지막 커밋 ---" && \
git log --oneline -3 2>/dev/null || echo "(커밋 없음)" && \
echo "" && \
# 원격 연결
echo "--- 원격 저장소 ---" && \
git remote -v 2>/dev/null || echo "(원격 없음 — GitHub 미연결)"
```

```bash
# 커밋 안 된 파일 수
echo "--- 미커밋 파일 수 ---" && \
MODIFIED=$(git status --short 2>/dev/null | wc -l | xargs) && \
echo "변경된 파일: ${MODIFIED}개" && \
if [ "${MODIFIED:-0}" -gt 10 ]; then
  echo "⚠️ 변경사항이 많습니다 — /healer:git-savepoint로 체크포인트를 만드세요"
fi
```

결과를 아래 형식으로 요약한다:

```
✅ [4/5 완료] Git 상태
  Git 초기화: <✅/⚠️>
  미커밋 파일: <N개>
  원격 연결: <✅ 있음 / ⚠️ 없음>
  ⚠️ 문제: <있으면 표시, 없으면 "이상 없음">
```

---

### ▶ STEP 5 / 5 — 전체 요약 & 다음 단계

```
📊 [5/5] 전체 요약 생성 중...
```

앞서 나온 1~4단계 결과를 종합해서 아래 형식으로 최종 보고서를 출력한다.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🩺 Vibe Healer — 전체 헬스체크 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [1/5] 로컬 실행    ✅ or ⚠️  <한 줄 요약>
  [2/5] 에러 분석    ✅ or ⚠️  <한 줄 요약>
  [3/5] API 키 보안  ✅ or ⚠️  <한 줄 요약>
  [4/5] Git 상태     ✅ or ⚠️  <한 줄 요약>

⚠️ 발견된 문제 (<N>개):
  1. <문제 설명> → 해결: /healer:<스킬명>
  2. <문제 설명> → 해결: /healer:<스킬명>

✅ 이상 없는 영역: <영역명>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 지금 바로 할 일 (우선순위 순):
  1. /healer:<가장 급한 스킬>
  2. /healer:<두 번째>
  (없으면: "모든 영역 이상 없음 🎉")
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 안전 규칙

- API 키, 패스워드, 토큰 실제 값은 절대 출력하지 않는다.
- 파일 수정, 커밋, 배포는 이 커맨드에서 직접 하지 않는다.
- 각 단계는 **읽기 전용 진단**만 수행한다.
