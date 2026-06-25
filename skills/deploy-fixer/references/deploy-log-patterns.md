# Deployment Log Patterns

- `Environment Variable ... not found`: configure platform env vars.
- `Module not found`: dependency missing or wrong root directory.
- `Command "build" not found`: package script missing or wrong framework.
- `No open ports detected`: start command or server binding issue.
- `Exited with status 1`: inspect lines above for the real cause.
- Blank page after deploy: collect browser console errors and runtime logs.
