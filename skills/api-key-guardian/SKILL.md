---
name: api-key-guardian
description: Check beginner projects for API key exposure, unsafe .env handling, missing .gitignore protection, hardcoded secrets, public client-side secret usage, and safe environment variable patterns. Use when the user asks whether API keys are safe, whether code can be pushed to GitHub, or how to use .env files.
skill_id: VH-04
aliases: [api-key-guardian, API키가디언, 키점검]
category: security
priority: high
version: 0.1.0
tags: [security, api-key, env, gitignore, beginners, vibe-healer]
allowed-tools:
  - Bash
  - Read
created_at: "2026-06-25"
author: GQAI X TTimes
---

# API Key Guardian

Use this skill to prevent accidental credential leaks and explain safe env handling.

## Workflow

1. Run `scripts/secret_scan.py --path <project> --json` when available.
2. Inspect `.gitignore`, `.env*`, client files, server routes, and config files.
3. Mask all secrets in output.
4. Explain whether the value belongs server-side or may be public.
5. Suggest `.env.example` keys without real values.
6. Ask before editing `.gitignore`, removing files from Git, or creating templates.

## High Risk Signals

- Real secret in files under `app/`, `pages/`, `src/components/`, `public/`, or static JS.
- Private key assigned to `NEXT_PUBLIC_*`.
- `.env` or `.env.local` not ignored by Git.
- Secret appears in committed history or staged diff.

## Output Rules

- Never print complete secrets.
- Use `[REDACTED]` or masked previews only.
- Separate urgent leak risks from cleanup recommendations.

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
