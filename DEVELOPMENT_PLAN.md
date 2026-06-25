# Vibe Healer Plugin Development Plan

## 0. Purpose

Vibe Healer is a beginner-friendly diagnostic plugin for people building small web apps with AI coding tools. It does not try to be a magic auto-fixer. Its job is to inspect a project, explain what is wrong in plain language, propose the next safest action, and verify that the action worked.

This document is a development plan only. Do not scaffold or implement the plugin during this planning phase. Use this file as the source of truth when a later session starts actual development.

## 1. Product Definition

### Plugin Name

- Normalized plugin name: `vibe-healer`
- Display name: `Vibe Healer`
- Category: `Productivity`
- Primary audience: beginners following Season 1 and Season 2 vibe-coding lessons
- Core promise: "When a beginner gets stuck, Vibe Healer diagnoses the project and gives one safe next step."

### Beginner Experience Rule

Every skill in this plugin must answer in this shape:

```text
Diagnosis:
What I found in plain language.

Likely cause:
Why this is happening.

Do this first:
One concrete next action.

Verification:
How we will know it worked.

Safety note:
Anything dangerous, private, or irreversible.
```

The plugin must avoid overwhelming beginners with ten possible fixes at once. It can show additional options only after the first safe action is complete or rejected.

## 2. Six Skills To Build

### 2.1 `local-run-doctor`

Purpose: identify how to run the current project locally.

Beginner trigger examples:

- "로컬에서 안 켜져"
- "이 프로젝트 어떻게 실행해?"
- "npm run dev가 맞아?"
- "Flask인지 Next.js인지 모르겠어"
- "포트가 충돌하는 것 같아"

Responsibilities:

- Detect project type: Next.js, React/Vite, Streamlit, Flask, generic Python, static HTML.
- Inspect safe files: `package.json`, `requirements.txt`, `pyproject.toml`, `app.py`, `streamlit_app.py`, `.env.example`, README files.
- Identify likely run command.
- Check common port assumptions.
- Suggest one safe command to run.

Required reusable resources:

- `scripts/detect_project.py`
- `references/project-types.md`
- `references/local-run-troubleshooting.md`

Validation cases:

- Next.js app with `package.json` and `dev` script.
- Flask app with `app.py` and `requirements.txt`.
- Streamlit app with `streamlit_app.py`.
- Static HTML folder with no package manager.
- Unknown project where the skill should ask for logs instead of guessing.

### 2.2 `error-doctor`

Purpose: explain terminal, build, install, and runtime errors.

Beginner trigger examples:

- "이 에러가 뭐야?"
- "터미널 로그 보고 고쳐줘"
- "npm install이 실패했어"
- "빌드 에러가 나"
- "Python 에러 해석해줘"

Responsibilities:

- Classify error type: dependency, syntax, missing environment variable, version mismatch, path issue, port issue, permission issue.
- Extract the first meaningful error line instead of reacting to noisy logs.
- Explain the error in beginner language.
- Provide one fix attempt and one verification command.
- Preserve user changes and avoid destructive commands.

Required reusable resources:

- `scripts/classify_error.py`
- `references/error-patterns-node.md`
- `references/error-patterns-python.md`
- `references/error-response-template.md`

Validation cases:

- Next.js TypeScript compile error.
- Missing package error.
- Python `ModuleNotFoundError`.
- Port already in use error.
- Environment variable missing error.
- Long noisy log where the root cause is near the top.

### 2.3 `deploy-fixer`

Purpose: diagnose failed deployments and turn deployment logs into a safe repair plan.

Beginner trigger examples:

- "Vercel 배포가 실패했어"
- "Render에서 안 떠"
- "Streamlit 배포 로그 봐줘"
- "GitHub에는 올렸는데 사이트가 안 보여"
- "빌드는 로컬에서 되는데 배포에서 실패해"

Responsibilities:

- Distinguish local build failures from platform configuration failures.
- Diagnose Vercel, Render, and Streamlit Community Cloud basics.
- Check build command, output directory, runtime version, environment variables, package lock files.
- Explain what must be changed in platform settings versus code.
- Require confirmation before pushing, redeploying, or changing external service settings.

Required reusable resources:

- `references/deploy-vercel.md`
- `references/deploy-render.md`
- `references/deploy-streamlit.md`
- `references/deploy-log-patterns.md`

Validation cases:

- Vercel build fails because env var is missing.
- Vercel build fails because TypeScript compile fails.
- Render Flask app fails because start command is wrong.
- Streamlit app fails because dependency is missing.
- App deploys but shows a blank page due to client-side runtime error.

### 2.4 `api-key-guardian`

Purpose: prevent API key exposure and help beginners use environment variables safely.

Beginner trigger examples:

- "API 키 넣어도 안전해?"
- "이 코드에 키가 노출됐는지 봐줘"
- ".env는 어떻게 써?"
- "GitHub에 올려도 돼?"
- "프론트 코드에 OpenAI 키를 넣어도 돼?"

Responsibilities:

- Inspect `.env*`, `.gitignore`, client-side files, server-side API routes, config files.
- Detect likely secrets without printing them back.
- Mask sensitive values in all output.
- Explain client versus server boundary.
- Suggest `.env.example` shape without real secrets.
- Require confirmation before modifying `.gitignore` or adding env templates.

Required reusable resources:

- `scripts/secret_scan.py`
- `references/api-key-safety.md`
- `references/env-file-patterns.md`
- `references/client-server-boundary.md`

Validation cases:

- `.env.local` exists and `.gitignore` excludes `.env*`.
- `.env` exists but `.gitignore` does not protect it.
- API key hardcoded in a client component.
- API key hardcoded in a backend-only script.
- False positive string that looks like a key but is sample text.

### 2.5 `git-savepoint`

Purpose: help beginners create a safe checkpoint before risky edits.

Beginner trigger examples:

- "망치기 전에 저장해줘"
- "지금 상태 백업해줘"
- "커밋해도 돼?"
- "Git 상태 확인해줘"
- "되돌릴 수 있게 세이브포인트 만들어줘"

Responsibilities:

- Explain current Git state in beginner language.
- Separate tracked changes, untracked files, ignored files, and large artifacts.
- Suggest a clear commit message.
- Do not commit secrets, logs, build artifacts, or test output.
- Ask before commit and before push.
- Never run destructive commands such as `git reset --hard` unless the user explicitly asks and understands the consequence.

Required reusable resources:

- `scripts/git_status_summary.py`
- `references/git-savepoint-policy.md`
- `references/gitignore-common.md`

Validation cases:

- Clean repo.
- Modified tracked files only.
- Untracked image assets that should be committed.
- Test result artifacts that should be ignored.
- Possible secret file staged by mistake.

### 2.6 `ui-screenshot-reviewer`

Purpose: review screenshots for obvious beginner-facing UI problems.

Beginner trigger examples:

- "이 화면 이상한 곳 봐줘"
- "모바일에서 깨지는지 확인해줘"
- "버튼 위치 괜찮아?"
- "텍스트가 겹치는지 봐줘"
- "스크린샷 기준으로 디자인 리뷰해줘"

Responsibilities:

- Inspect screenshots and identify layout, spacing, contrast, overflow, alignment, and mobile issues.
- Prioritize visible user-facing problems over subjective taste.
- Suggest small, concrete fixes.
- If a local dev server is available, recommend desktop and mobile viewport checks.
- Do not redesign the whole page unless the user asks.

Required reusable resources:

- `references/ui-review-rubric.md`
- `references/responsive-checklist.md`
- `references/screenshot-report-template.md`

Validation cases:

- Desktop navbar alignment issue.
- Mobile text overflow.
- Button label clipped.
- Card grid spacing inconsistency.
- Low contrast text on image.

## 3. Proposed Plugin Structure

Use this target structure during implementation:

```text
vibe-healer/
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   ├── local-run-doctor/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   ├── scripts/detect_project.py
│   │   └── references/
│   ├── error-doctor/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   ├── scripts/classify_error.py
│   │   └── references/
│   ├── deploy-fixer/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/
│   ├── api-key-guardian/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   ├── scripts/secret_scan.py
│   │   └── references/
│   ├── git-savepoint/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   ├── scripts/git_status_summary.py
│   │   └── references/
│   └── ui-screenshot-reviewer/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
└── scripts/
    └── validate_vibe_healer.py
```

Do not add extra README, changelog, or installation guide files inside individual skill folders. Keep each skill focused on `SKILL.md`, needed scripts, needed references, and optional `agents/openai.yaml`.

## 4. Shared Safety Rules

These rules apply to all six skills:

- Do not reveal API keys or tokens. Mask secrets as `sk-...last4` or `[REDACTED]`.
- Do not run destructive Git commands automatically.
- Do not delete files automatically.
- Do not push, deploy, send messages, or change external services without user confirmation.
- Prefer diagnosis before edits.
- When unsure, ask for the smallest missing artifact: exact error log, file path, or screenshot.
- Give one primary next step before listing alternatives.
- Always include a verification step.

## 5. Phase Plan

### Phase 0 - Scope Lock

Goal: confirm the plugin should include exactly these six skills and no implementation beyond the planned structure.

Tasks:

- Confirm target name: `vibe-healer`.
- Confirm target development location. Recommended default: `~/plugins/vibe-healer`.
- Confirm marketplace type. Recommended default: personal marketplace.
- Confirm that this is a Codex plugin first, not a Claude Code-only plugin.
- Confirm that all six skills are in scope for v1.

Exit criteria:

- The six skills listed in this document are accepted.
- No seventh skill is added to v1.
- The target path and marketplace decision are recorded in the implementation session notes.

Validation:

- Human review only.
- The implementation session must repeat the final scope before scaffolding.

### Phase 1 - Plugin Scaffold

Goal: create a valid plugin shell with marketplace-ready metadata.

Tasks:

- Use the plugin scaffold flow to create `vibe-healer`.
- Create `.codex-plugin/plugin.json`.
- Add `skills/` and `scripts/` folders.
- Add personal marketplace entry only if the implementation session explicitly chooses marketplace-backed development.
- Validate the plugin shell before adding skill content.

Expected manifest direction:

```json
{
  "name": "vibe-healer",
  "version": "0.1.0",
  "description": "Beginner-friendly project diagnosis plugin for local run issues, errors, deployment, API key safety, Git savepoints, and screenshot UI review."
}
```

Exit criteria:

- Plugin folder exists.
- `.codex-plugin/plugin.json` exists.
- Plugin manifest has no placeholder text.
- Marketplace entry, if created, includes installation policy, authentication policy, and category.

Validation:

- Run plugin validation script from the plugin creator workflow.
- Run `git status` or equivalent to confirm only intended files were created.

### Phase 2 - Shared Reference Design

Goal: define shared beginner language, safety policy, and output templates before writing individual skills.

Tasks:

- Draft shared response style in each skill or a small shared reference if the plugin system supports cross-skill references cleanly.
- Define "one next step" answer format.
- Define severity labels:
  - `safe`: read-only or local verification.
  - `careful`: file edits, package installs, environment changes.
  - `confirm`: commit, push, deploy, delete, external send.
  - `blocked`: missing artifact or user approval required.
- Define common validation language.

Exit criteria:

- All six skills use the same answer shape.
- All six skills include safety boundaries in their `SKILL.md`.
- No skill asks beginners to perform multiple unrelated steps at once.

Validation:

- Review each `SKILL.md` trigger description.
- Confirm each description says when to use the skill.
- Confirm each body stays concise and points to references for details.

### Phase 3 - Build MVP Skills

Goal: implement the three highest-value beginner skills first.

MVP skills:

1. `local-run-doctor`
2. `error-doctor`
3. `api-key-guardian`

Tasks:

- Create each skill with `SKILL.md`, `agents/openai.yaml`, scripts, and references.
- Keep `SKILL.md` under 500 lines.
- Put detailed error patterns and safety details in `references/`.
- Implement deterministic scripts only where useful:
  - `detect_project.py`
  - `classify_error.py`
  - `secret_scan.py`

Exit criteria:

- The three MVP skills validate individually.
- Each script can run with `--help` or a sample fixture.
- Each skill has at least five trigger examples covered by the description or body.

Validation:

- Run skill quick validation for each skill.
- Run representative script tests.
- Test with one Next.js sample, one Flask sample, and one Streamlit sample.
- Confirm secret scanning never prints full secrets.

### Phase 4 - Build Workflow Skills

Goal: add deployment and Git checkpoint support.

Skills:

1. `deploy-fixer`
2. `git-savepoint`

Tasks:

- Create deployment references for Vercel, Render, and Streamlit.
- Create Git savepoint policy reference.
- Implement `git_status_summary.py`.
- Define approval gates for commit and push.
- Define artifact exclusion rules for logs, test output, build folders, and secrets.

Exit criteria:

- `deploy-fixer` can classify deployment logs by platform.
- `git-savepoint` can summarize working tree state without making changes.
- Both skills ask before external or irreversible actions.

Validation:

- Run quick validation.
- Test with sample deployment logs.
- Test with clean, dirty, untracked, and suspicious-secret Git states.
- Confirm no destructive command appears in default workflow.

### Phase 5 - Build Visual Review Skill

Goal: add screenshot-based beginner UI review.

Skill:

- `ui-screenshot-reviewer`

Tasks:

- Create UI review rubric.
- Create responsive checklist.
- Create screenshot report template.
- Include guidance for desktop and mobile viewport review.
- Keep recommendations concrete and small.

Exit criteria:

- The skill can review a screenshot without needing repository access.
- The skill can distinguish visible layout bugs from subjective redesign preferences.
- The skill can recommend verification screenshots.

Validation:

- Test on three screenshots:
  - desktop navbar alignment issue.
  - mobile text overflow.
  - card grid spacing issue.
- Confirm the output starts with the highest-impact visible problem.

### Phase 6 - Integrated Healer Flow

Goal: make the six skills feel like one plugin, even though each skill has its own trigger.

Tasks:

- Define a recommended triage order:
  1. `git-savepoint` if risky edits are expected.
  2. `local-run-doctor` if the project does not run.
  3. `error-doctor` if there is a log.
  4. `api-key-guardian` if API keys or `.env` are involved.
  5. `deploy-fixer` if the issue appears only after deployment.
  6. `ui-screenshot-reviewer` if the app runs but looks wrong.
- Add cross-skill handoff guidance in each skill body.
- Define a `healer diagnosis summary` response format that can combine results from multiple skills.

Exit criteria:

- A beginner can say "힐러 실행해줘" and receive a clear first diagnosis path.
- The handoff between skills does not duplicate long explanations.
- The plugin never claims to fix something it has not verified.

Validation:

- Run an end-to-end scenario:
  - Dirty Git state.
  - Next.js app fails build.
  - `.env.local` exists.
  - User wants deploy help.
- Expected behavior:
  - Recommend savepoint first.
  - Diagnose build error second.
  - Check env safety third.
  - Only then discuss deployment.

### Phase 7 - Full Validation And Forward Testing

Goal: verify that the plugin works for real beginner situations and does not overreach.

Validation matrix:

| Area | Minimum test | Pass condition |
| --- | --- | --- |
| Plugin manifest | Plugin validator | No schema or placeholder errors |
| Skill metadata | Quick validation for all six skills | Valid frontmatter and naming |
| Scripts | Run each script with fixtures | Deterministic output and no crashes |
| Secrets | Scan files with fake keys | Keys are detected and masked |
| Git safety | Dirty repo fixture | No accidental commit/push/delete |
| Error logs | Node/Python fixtures | Correct root-cause classification |
| Deployment | Vercel/Render/Streamlit logs | Correct platform-specific advice |
| UI review | Desktop/mobile screenshots | Finds visible layout issues |
| Beginner output | Manual review | Uses plain language and one next step |

Forward-test prompts:

```text
Use $local-run-doctor at /path/to/vibe-healer/skills/local-run-doctor to help me run this project locally.
```

```text
Use $error-doctor at /path/to/vibe-healer/skills/error-doctor to explain this terminal error and give me the first fix to try.
```

```text
Use $api-key-guardian at /path/to/vibe-healer/skills/api-key-guardian to check whether this project is safe to push to GitHub.
```

```text
Use $deploy-fixer at /path/to/vibe-healer/skills/deploy-fixer to diagnose this Vercel deployment log.
```

```text
Use $git-savepoint at /path/to/vibe-healer/skills/git-savepoint to create a safe checkpoint plan for this repo.
```

```text
Use $ui-screenshot-reviewer at /path/to/vibe-healer/skills/ui-screenshot-reviewer to review this screenshot for beginner-visible UI problems.
```

Exit criteria:

- Each forward test produces useful output without hidden context.
- Failures are converted into reference updates or SKILL.md trigger improvements.
- All validation commands are recorded in the implementation session notes.

### Phase 8 - Documentation For Site Card

Goal: prepare content for the `/skills` catalog after the plugin is implemented and validated.

Tasks:

- Add a new catalog item only after plugin validation passes.
- Card title: `Vibe Healer`
- Type: `plugin`
- Card description:
  - "초보자가 프로젝트 실행, 에러, 배포, API 키, Git 상태, UI 화면에서 막혔을 때 현재 상태를 진단하고 다음 행동을 한 단계씩 안내하는 응급 진단 플러그인입니다."
- Tags:
  - `Beginner`
  - `Debugging`
  - `Deploy`
  - `API Safety`
  - `Git`
- Image theme:
  - Pencil sketch on warm paper.
  - A project diagnosis desk with terminal logs, API key lockbox, Git checkpoint card, deployment chart, and UI screenshot notes.

Exit criteria:

- The site card links to a detail page.
- The detail page clearly says whether the plugin is Codex-ready, Claude Code-only, or experimental.
- The detail page includes "what it does not do" safety boundaries.

Validation:

- Run `npm run build` in the site repo after adding the card.
- Check `/skills` and `/skills/vibe-healer` screenshots.

## 6. Implementation Session Checklist

When development starts in a later session, use this checklist:

```text
1. Re-read this document.
2. Confirm target path and marketplace choice.
3. Scaffold vibe-healer plugin.
4. Validate empty plugin shell.
5. Build Phase 2 shared rules.
6. Build Phase 3 MVP skills.
7. Validate MVP.
8. Build Phase 4 workflow skills.
9. Validate workflow skills.
10. Build Phase 5 screenshot skill.
11. Validate screenshot skill.
12. Run Phase 6 integrated scenario.
13. Run Phase 7 full validation matrix.
14. Only after validation, update the site catalog card.
```

## 7. Definition Of Done

Vibe Healer v1 is done only when all items below are true:

- Plugin validates.
- All six skill folders validate.
- All scripts run on sample fixtures.
- All six skills have beginner-friendly trigger descriptions.
- All skills use the shared answer shape.
- Secrets are masked in every output.
- Destructive actions require explicit confirmation.
- Each skill has at least three realistic validation cases.
- The integrated triage flow is tested.
- Site card and detail page are added only after plugin validation.

## 8. Recommended First Development Prompt

Use this prompt in the next implementation session:

```text
VIBE_HEALER_PLUGIN_DEVELOPMENT_PLAN.md를 읽고 Phase 0부터 시작해줘.
이번 세션에서는 먼저 플러그인 스캐폴드와 Phase 2 shared rules까지만 구현하고,
각 단계마다 검증 결과를 보여줘. 실제 스킬 6개 구현은 내가 승인하면 다음 단계로 진행해줘.
```
