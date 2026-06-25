---
name: local-run-doctor
description: Diagnose how to run a beginner project locally and resolve startup blockers. Use when the user says the local app will not start, asks which command to run, sees port conflicts, or needs project type detection for Next.js, Vite, Streamlit, Flask, generic Python, or static HTML projects.
skill_id: VH-05
aliases: [local-run-doctor, 로컬런닥터, 실행진단]
category: development
priority: high
version: 0.1.0
tags: [local, run, nextjs, flask, streamlit, beginners, vibe-healer]
allowed-tools:
  - Bash
  - Read
created_at: "2026-06-25"
author: GQAI X TTimes
---

# Local Run Doctor

Use this skill to identify the current project type, find the safest local run command, and explain startup blockers in beginner language.

## Workflow

1. Inspect the project root before proposing a command.
2. Run `scripts/detect_project.py --path <project>` when available.
3. Read `references/project-types.md` when the project type is unclear or mixed.
4. Read `references/local-run-troubleshooting.md` when there is a port, dependency, or command failure.
5. Return one primary command and one verification check.

## What To Inspect

- `package.json`, lockfiles, and known scripts.
- `requirements.txt`, `pyproject.toml`, `Pipfile`, and app entry files.
- `app.py`, `main.py`, `streamlit_app.py`, `src/`, `app/`, `pages/`, `index.html`.
- `.env.example` and README run instructions, if present.

## Output Rules

- If confidence is high, provide the likely command.
- If confidence is medium, explain why and ask for permission before installing dependencies.
- If confidence is low, ask for the file list or error log instead of guessing.
- Never suggest deleting lockfiles or reinstalling everything as the first step.

## Shared Beginner Response Shape

Always answer with these labels unless the user explicitly asks for a different format:

```text
Diagnosis:
Likely cause:
Do this first:
Verification:
Safety note:
```

Keep the first action small and reversible. If multiple fixes are possible, pick the safest first check and mention alternatives only after the first check.

## Safety Rules

- Do not reveal full API keys, tokens, cookies, or credentials.
- Do not delete files, reset Git history, push, deploy, or modify external services without explicit confirmation.
- Prefer read-only inspection before edits.
- Ask for the smallest missing artifact when blocked: an error log, file path, screenshot, or deployment log.
- State verification clearly so the beginner knows when the issue is resolved.
