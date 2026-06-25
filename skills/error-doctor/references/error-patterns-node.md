# Node And Next.js Error Patterns

- `Module not found: Can't resolve`: dependency or import path missing.
- `Cannot find module`: package not installed or wrong runtime path.
- `ReferenceError: window is not defined`: browser-only code ran on server.
- `Hydration failed`: server and client rendered different output.
- `Type error:`: TypeScript contract mismatch; fix source before deployment.
- `EADDRINUSE`: port conflict.
- `NEXT_PUBLIC_`: public env var; never put private API keys here.
