---
name: error-doctor
description: Diagnose terminal logs, build failures, install errors, runtime errors, TypeScript errors, Python tracebacks, missing packages, missing env vars, and port conflicts. Use when the user pastes an error log or says an npm, Next.js, Python, Flask, Streamlit, or build command failed.
skill_id: VH-01
aliases: [error-doctor, 에러닥터, 에러진단]
category: debugging
priority: high
version: 0.1.0
tags: [debugging, errors, nodejs, python, beginners, vibe-healer]
allowed-tools:
  - Bash
  - Read
created_at: "2026-06-25"
author: GQAI X TTimes
---

# Error Doctor

Use this skill to turn noisy logs into one clear diagnosis and a safe first fix.

## Workflow

1. Ask for the exact log if the user only describes the problem vaguely.
2. Run `scripts/classify_error.py` on pasted logs or saved log files when available.
3. Read Node or Python pattern references based on the detected stack.
4. Identify the first meaningful error, not the last noisy line.
5. Give one fix attempt and one verification command.

## Classification Priority

1. Secret or credential exposure risk.
2. Missing environment variable.
3. Syntax or compile error.
4. Missing dependency.
5. Runtime path/import error.
6. Version mismatch.
7. Port conflict.
8. Permission error.
9. Unknown: ask for more context.

## Output Rules

- Quote only the short relevant error line.
- Explain the cause without blaming the user.
- Do not recommend broad reinstall, cache clearing, or reset commands as the first action.
- Ask before editing files.

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
