# Client Server Boundary

Next.js examples:

- Server route: `app/api/*/route.ts` can use private env vars.
- Server component: can use private env vars if not serialized to client.
- Client component with `use client`: do not read private env vars.
- `NEXT_PUBLIC_*`: bundled into browser; safe only for public IDs and URLs.

When in doubt, move the API call into a server route.
