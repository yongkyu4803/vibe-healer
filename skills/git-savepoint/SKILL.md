---
name: git-savepoint
description: Help beginners inspect Git status and create safe checkpoints before risky edits. Use when the user asks to save, back up, commit, push, check Git state, make a restore point, or avoid losing work. Exclude secrets, logs, build artifacts, and test outputs from commits.
skill_id: VH-02
aliases: [git-savepoint, 깃세이브포인트, 세이브포인트]
category: git
priority: high
version: 0.1.0
tags: [git, savepoint, beginners, vibe-healer]
allowed-tools:
  - Bash
  - Read
created_at: "2026-06-25"
author: GQAI X TTimes
---

# Git Savepoint

Use this skill to make Git understandable and safe for beginners.

## Workflow

1. Run `scripts/git_status_summary.py --path <repo> --json` when available.
2. Explain clean, modified, staged, untracked, ignored, and suspicious files.
3. Recommend what should be committed and what should be ignored.
4. Suggest a concise commit message.
5. Ask before running `git add`, `git commit`, or `git push`.
6. Never run destructive commands by default.

## Commit Safety Gate

Before commit, verify:

- No `.env`, key, token, credential, or secret-looking file is included.
- No build folders such as `.next/`, `dist/`, `build/`, `node_modules/` are included.
- No test output folders such as `test-results/` or reports are included unless explicitly intended.
- Large binary files are expected assets.

## Output Rules

- Explain the state in beginner language.
- Provide one proposed commit group.
- Ask for confirmation before commit or push.

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
