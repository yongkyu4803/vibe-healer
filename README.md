# Vibe Healer

막혔을 때 쓰는 응급 진단 플러그인입니다.  
로컬 실행 오류, 터미널 에러, 배포 실패, API 키 노출, Git 상태, UI 화면 문제를 진단하고 **다음 행동 하나**를 알려줍니다.

---

## 설치

### Claude Code

```bash
# 1. 레포 클론
git clone https://github.com/yongkyu4803/vibe-healer.git

# 2. 설치 스크립트 실행
bash vibe-healer/scripts/install_claude_code.sh
```

설치하면 `~/.claude/skills/healer/`에 파일이 복사되고, Claude Code를 재시작하면 바로 사용할 수 있습니다.

---

## 사용법

### 빠른 시작

```
/healer:start
```

실행하면 두 가지 모드 중 하나를 선택합니다.

- **빠른 트리아지** — 지금 가장 급한 문제 하나만 찾아서 알려줌 (1분)
- **전체 헬스체크** — 로컬 실행 → 에러 → API 키 → Git 상태를 순서대로 점검 (5분)

### 개별 스킬 직접 실행

| 명령어 | 언제 쓰나 |
|---|---|
| `/healer:error-doctor` | 터미널 에러, 빌드 실패, npm/Python 에러가 났을 때 |
| `/healer:local-run-doctor` | 로컬에서 앱이 안 켜질 때, 실행 명령을 모를 때 |
| `/healer:api-key-guardian` | API 키가 안전한지, GitHub에 올려도 되는지 확인할 때 |
| `/healer:git-savepoint` | 수정 전에 현재 상태를 저장(커밋)하고 싶을 때 |
| `/healer:deploy-fixer` | Vercel, Render, Streamlit 배포가 실패했을 때 |
| `/healer:ui-screenshot-reviewer` | 화면이 이상하게 보이는 스크린샷을 리뷰 받고 싶을 때 |

---

## 스킬 소개

### error-doctor
터미널에 붙여넣으면 에러의 원인과 첫 번째 해결책을 알려줍니다. Node.js, Next.js, Python, Flask, Streamlit의 에러 패턴을 지원합니다.

### local-run-doctor
프로젝트 타입(Next.js / Flask / Streamlit 등)을 자동으로 감지하고, 올바른 실행 명령을 찾아줍니다. 포트 충돌이나 의존성 미설치도 확인합니다.

### api-key-guardian
`.env` 파일, `.gitignore`, 소스 코드를 검사해서 API 키가 노출될 위험이 있는지 진단합니다. 키 값 자체는 절대 출력하지 않습니다.

### git-savepoint
Git 상태를 초보자 언어로 설명하고, 커밋 메시지를 제안합니다. 시크릿 파일, 빌드 결과물, 로그는 커밋에서 자동으로 제외합니다. 커밋·푸시 전에 반드시 확인을 받습니다.

### deploy-fixer
배포 로그를 분석해서 코드 문제인지 플랫폼 설정 문제인지 구분합니다. Vercel, Render, Streamlit Community Cloud를 지원합니다.

### ui-screenshot-reviewer
스크린샷을 보고 레이아웃 깨짐, 텍스트 오버플로우, 버튼 잘림, 모바일 반응형 문제를 찾아줍니다.

---

## 자동 업데이트

`/healer:start`를 실행할 때마다 GitHub의 최신 버전을 자동으로 확인합니다.

```
✅ Vibe Healer v0.1.0 (최신)
```

새 버전이 있으면 자동으로 pull 하고 재설치합니다.

```
⬆️  새 버전 발견: 0.1.0 → 0.2.0 — 업데이트 중...
✅ 0.2.0 업데이트 완료
```

---

## 원칙

- **진단 우선** — 파일을 수정하거나 명령을 실행하기 전에 먼저 진단합니다.
- **한 번에 한 단계** — 해결책을 열 가지 나열하지 않고 지금 당장 해야 할 것 하나만 알려줍니다.
- **확인 후 행동** — 커밋, 푸시, 배포, 파일 삭제는 반드시 사용자 확인을 받습니다.
- **비밀 보호** — API 키, 토큰, 패스워드 실제 값은 절대 출력하지 않습니다.

---

## 수동 업데이트

자동 업데이트가 실패했을 때는 직접 실행하세요.

```bash
cd vibe-healer
git pull
bash scripts/install_claude_code.sh
```

---

## 라이선스

MIT © GQAI X TTimes
