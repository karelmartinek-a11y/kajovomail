# Deployment

## Local stack
1. Copy `.env.example` to `.env`, fill PostgreSQL/Redis credentials, OpenAI placeholders, and run `docker compose -f infra/docker-compose.dev.yml up --build` to start the backend, workers, database, and Redis.
2. Backend migrations run through Alembic (`python -m alembic upgrade head`) and tests live in `backend/app/tests`; the stack already caches correlation IDs and worker logs.
3. For local frontend iterations, `cd web && npm run dev` talks to the backend API at `/api/v1` and WS at `/api/v1/events/ws` using HttpOnly cookies and CSRF headers.

## Production layout
- The backend stays behind the `mail.hcasc.cz` reverse proxy and exposes `/api/v1` plus `/api/v1/events/ws`. Celery workers continue to push sync/draft/offer audits to the event stream.
- Build the SPA with `cd web && npm run build`; the generated `dist/` folder contains the static bundle that references brand tokens without duplication.
- Static assets are served by the host web server (Nginx, Caddy), while `/api/v1` and `/api/v1/events/ws` are forwarded to the backend container defined in `infra/docker-compose.prod.yml`. Sessions remain server-only, and `x-csrf-token` headers stay paired with HttpOnly cookies.
- Deploy workflow injects bootstrap login credentials from GitHub: variable `KAJOVOMAIL_LOGIN_EMAIL` and secret `KAJOVOMAIL_LOGIN_PASSWORD`. Backend startup ensures this account exists and keeps the password synchronized.

## Desktop artifacts
- Desktop builds live under `desktop/scripts/*` and rely on PyInstaller (`pyinstaller --onefile --windowed --name KajovoMail main.py`). Run the scripts after installing dependencies in `desktop/pyproject.toml`; artifacts appear in `dist/` and connect to the same `mail.hcasc.cz/api/v1` backend.
- The desktop client keeps mail state in RAM, stores only the session token/CSRF pair in the OS keyring/keychain, and explicitly avoids creating any local mailbox database. Event stream updates refresh the UI via `/api/v1/events/ws`.

## Reverse proxy for mail.hcasc.cz
- `mail.hcasc.cz` should point to the node hosting both the static `web/dist` directory and the Compose backend container. Requests to `/` load the SPA and let client-side routing hit `/api/v1` and `/api/v1/events/ws` on the same origin.
- API endpoints, event stream, and OAuth callbacks (if added later) must be routed to the backend container so credentials never touch clients. Static caching headers should be conservative (short TTL) so new builds roll out quickly.
- Keep existing hostnames (`hotel.hcasc.cz`, `dagmar.hcasc.cz`, `api.hcasc.cz`) untouched; only `mail.hcasc.cz` may host KajovoMail. DNS and certificates should reflect the new static + API split.

## Observability
- Backend logs and Celery audit trails write to `/var/log/kajovomail`; event stream messages embed correlation IDs so the UI can display sync/* drafts/AI updates without polling.
- Playwright acceptance tests (`npm run test:playwright`) run against the local SPA and ensure login, navigation, Compose autosave, and search targets work before release.
- Android debug/release builds (`./gradlew assembleDebug`, `./gradlew bundleRelease`) also depend on `mail.hcasc.cz/api/v1`/`/events/ws`; treat the generated APK/AAB artifacts as production deliverables with their own release notes.
