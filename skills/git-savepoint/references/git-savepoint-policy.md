# Git Savepoint Policy

Allowed without confirmation:

- `git status --short`
- `git diff --stat`
- `git branch --show-current`
- `git log -1 --oneline`

Require confirmation:

- `git add`
- `git commit`
- `git push`
- editing `.gitignore`

Do not run unless explicitly requested with clear understanding:

- `git reset --hard`
- `git clean -fd`
- `git checkout -- <file>`
- force push
