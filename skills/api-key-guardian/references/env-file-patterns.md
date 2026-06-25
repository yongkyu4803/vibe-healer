# Env File Patterns

Recommended `.gitignore` lines:

```text
.env
.env.*
!.env.example
```

Recommended `.env.example` style:

```text
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
NEXT_PUBLIC_SITE_URL=
```

Never copy real values into `.env.example`.
