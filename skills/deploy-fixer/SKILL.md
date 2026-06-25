---
name: deploy-fixer
description: Diagnose failed deployments for beginner projects on Vercel, Render, and Streamlit Community Cloud. Use when deployment logs fail, the site is blank after deploy, local build works but cloud build fails, env vars are missing in deployment, or platform build/start settings are unclear.
skill_id: VH-03
aliases: [deploy-fixer, 배포픽서, 배포진단]
category: devops
priority: high
version: 0.1.0
tags: [deploy, vercel, render, streamlit, beginners, vibe-healer]
allowed-tools:
  - Bash
  - Read
created_at: "2026-06-25"
author: GQAI X TTimes
---

# Deploy Fixer

Use this skill to separate code failures from platform configuration failures and guide the user through one safe deployment fix.

## Workflow

1. Ask which platform is being used if the log does not reveal it.
2. Ask for the deployment log, build settings, and framework if missing.
3. Read the platform reference: Vercel, Render, or Streamlit.
4. Identify whether the failure is local code, build command, start command, runtime version, dependency, or env configuration.
5. Explain what to change and where: codebase or platform dashboard.
6. Ask before pushing, redeploying, or changing external platform settings.

## Common Diagnosis Split

- Build fails locally too: fix code first with Error Doctor style guidance.
- Build only fails in cloud: check env vars, Node/Python version, install command, build command, root directory.
- Deploy succeeds but app crashes: inspect runtime logs and start command.
- Site is blank: check browser console, base path, client env vars, or missing assets.

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
