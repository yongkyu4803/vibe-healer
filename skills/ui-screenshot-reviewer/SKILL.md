---
name: ui-screenshot-reviewer
description: Review screenshots for beginner-visible UI problems such as text overflow, overlapping elements, clipped buttons, navbar misalignment, inconsistent spacing, low contrast, broken mobile layouts, and visual hierarchy issues. Use when the user shares a screenshot or asks whether a page looks broken on desktop or mobile.
skill_id: VH-06
aliases: [ui-screenshot-reviewer, UI리뷰어, 화면리뷰]
category: design
priority: high
version: 0.1.0
tags: [ui, screenshot, layout, mobile, beginners, vibe-healer]
allowed-tools:
  - Read
created_at: "2026-06-25"
author: GQAI X TTimes
---

# UI Screenshot Reviewer

Use this skill to review what is visible in a screenshot, not to redesign the whole product.

## Workflow

1. Inspect the screenshot first.
2. Prioritize bugs over taste: overlap, clipping, unreadable text, alignment, contrast, broken responsive layout.
3. Mention the highest-impact visible issue first.
4. Suggest small fixes with concrete CSS or layout direction when useful.
5. Recommend verification screenshots for desktop and mobile.

## Output Rules

- Do not invent hidden behavior that is not visible.
- Do not rewrite the design system unless asked.
- Keep feedback actionable and ordered by severity.
- If screenshot quality is too low, ask for a clearer crop or viewport size.

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
