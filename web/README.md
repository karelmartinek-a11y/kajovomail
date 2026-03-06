# KajovoMail Web Client

Single-page React + TypeScript client that consumes the `/api/v1` backend and `/api/v1/events/ws` stream.

## Structure
- `src/app` holds layout primitives and route definitions.
- `src/features` mirrors the product areas (auth, mail, AI, offers, search, settings).
- `src/services` exposes shared HTTP and event-stream helpers.
- `brand/` assets are aliased via Vite for palettes, tokens, and logos without duplication.

## Local development
1. Install dependencies: `npm install`
2. Start backend (`docker compose -f infra/docker-compose.dev.yml up --build`) so `/api/v1` is reachable.
3. Launch the UI: `npm run dev`
4. The Vite proxy points to `/api/v1` and honors HttpOnly cookies.

## Production build
- `npm run build` produces optimized assets under `dist/`. See `docs/Deployment.md` for how the proxy on `mail.hcasc.cz` should host the resulting files.
