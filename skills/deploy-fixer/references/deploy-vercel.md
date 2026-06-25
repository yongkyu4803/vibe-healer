# Vercel Deployment Checks

Check in this order:

1. Framework preset and root directory.
2. Install command and package manager lockfile.
3. Build command, usually `npm run build` for Next.js.
4. Required environment variables in Vercel Project Settings.
5. Node version if native packages or old dependencies are involved.
6. TypeScript and ESLint failures; Vercel treats them as build blockers.
7. Runtime logs if build succeeds but app crashes.

Do not tell beginners to disable TypeScript or lint checks as the first fix.
