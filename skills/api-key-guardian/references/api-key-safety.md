# API Key Safety

Private keys must stay on the server. Browser code is visible to users.

Safe places:

- `.env.local` ignored by Git.
- Server-only API routes.
- Backend scripts not shipped to the browser.
- Deployment platform environment settings.

Unsafe places:

- Client components.
- Static HTML or JS files.
- `NEXT_PUBLIC_*` variables for private keys.
- Screenshots or logs that include full tokens.
