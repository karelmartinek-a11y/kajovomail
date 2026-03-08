# Repository Guidelines

## Project Structure & Module Organization
- `backend/` hosts the FastAPI monolith (bounded contexts under `app/api`, `app/services`, `app/workers`) plus migrations, env templates, and acceptance/integration tests. Keep API schemas in `app/schemas`, reusable models in `app/models`, and feature folders aligned with prompts (auth, mail sync, AI orchestration, offers).
- Clients live in parallel roots: `web/` (browser SPA), `desktop/` (native shell), `android/` (mobile UI). Reuse shared assets from `brand/` (logos, palette, tokens) and central docs.
- `infra/` defines deployment manifests (`docker-compose.dev.yml`, `docker-compose.prod.yml`, `release-gate.sh`), while `.github/workflows/` orchestrates CI/CD. Support scripts such as `scripts/` seed data or diagnostics. Preview API surfaces in `docs/openapi.json` and keep product details in `docs/KajovoMailZadaniFinal.md`.
- Update `docs/Architecture.md`, `docs/Security.md`, `docs/Deployment.md`, and `docs/TestMatrix.md` whenever architectural or operational decisions change; they summarize the live backend design.
- `desktop/` now hosts the PySide6/Qt6 client with its session bindings, event stream worker, compose/browse layout, and build scripts; refer to `desktop/README.md` for run/build guidance and the `desktop/scripts/*` helpers for packaging.
- `android/` is the Kotlin + Jetpack Compose client. Keep Gradle files/README synced with `docs/` and ensure Compose UI + view model tests run before pushing (`./gradlew` commands).

## Build, Test, and Development Commands
- `docker compose -f infra/docker-compose.dev.yml up --build` boots backend, Postgres, Redis, worker queue, and event stream. Use `docker compose -f infra/docker-compose.dev.yml down --volumes` between runs to reset data.
- `cd backend && uvicorn backend.app.main:app --reload --reload-dir backend --host 0.0.0.0 --port 8000` runs the API against local env vars sourced from `.env.example`.
- `cd backend && pytest app/tests` executes unit, integration, and connector tests (GreenMail harness) referenced in `docs/TestMatrix.md`.
- `cd backend && alembic upgrade head` keeps the migration graph in sync after schema changes.

## Coding Style & Naming Conventions
- Python follows 4-space indentation, PEP 8 layout, consistent typing, and dataclasses for DTOs. Keep routers/test files in snake_case under feature folders (`api/v1/auth_router.py`, `services/mail_sync/*`).
- Use Markdown with sentence-case headers and ~100-character lines. JSON assets use two-space indentation and no trailing commas.

## Testing Guidelines
- Arrange tests in `backend/tests` and `backend/app/tests` using descriptive fixtures (`auth_client`, `imap_mock`). Name files like `test_<feature>_succeeds.py` and target auth/session, syncing, AI orchestration, offers, and error states.
- Integration suites spin up GreenMail or comparable SMTP/IMAP/POP3 services in containers; document any required images and capabilities in `docs/TestMatrix.md`.

## Commit & Pull Request Guidelines
- Use focused, imperative commit titles (e.g., `feat: add sync retry guard`). Mention modules impacted (`backend`, `infra`, `docs`) and cite relevant prompts or docs.
- PRs must explain how the change satisfies `docs/KajovoMailZadaniFinal.md`, list commands/tests run, note migrations or env updates, and include any supporting artifacts (logs, screenshots, OpenAPI diffs).

## Security & Configuration Tips
- Never commit secrets. Populate `.env` locally from `.env.example`; production secrets live in secure stores referenced in `docs/Security.md`. Audit logs record state changes but avoid logging raw credentials.
- The production hostname is `mail.hcasc.cz`; ensure infra manifests and DNS changes leave `hotel.hcasc.cz`, `dagmar.hcasc.cz`, and `api.hcasc.cz` untouched.
- OpenAI/SMTP keys belong to server-side settings only. Admin endpoints manage them, and clients receive only derived tokens or masked configurations.

## Communication
- Při práci v tomto repozitáři komunikuj s uživatelem česky.
