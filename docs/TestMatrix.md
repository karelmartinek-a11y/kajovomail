# Test Matrix

| Layer | Focus | Frequency | Tooling |
| --- | --- | --- | --- |
| Config | Validate .env load and capability flags | CI + local | pytest backend/tests/test_config.py |
| Health | /api/v1/health/*, readiness, DB reachability | Every push | pytest backend/tests/test_health.py |
| Auth | Login/logout/logout-all, session rotation, password change | Every push | pytest backend/tests/test_auth.py |
| Mail Sync | IMAP/POP3 capability routing, sync cursor updates, retries | Nightly/manual | Celery task tests + integration harness (GreenMail or mocked provider) |
| Search | Query syntax, pagination, virtual folders | Integration | pytest backend/tests/test_search.py (placeholder for future) |
| AI | Structured output validation, privacy rules, store=false default | Every push | pytest backend/tests/test_ai.py (checks schema + privacy metadata) |
| Offers | Thread-linked state transitions, audit logs, WebSocket events | Every push | pytest backend/tests/test_offers.py |
| Web UI | Login, navigation, compose autosave, search, event stream hints | Every push | Playwright `web/tests/e2e.spec.ts` (`npm run test:playwright`) |
| Desktop UI | Desktop layout, session handling, compose/drafts, AI/offers panels | Every push | pytest-qt + `desktop/tests/test_main_window.py` |
| Android UI | Login/login form, accounts navigation, compose/drafts, AI/offers flows | Every push | Compose UI test `android/src/androidTest/java/cz/kajovomail/LoginScreenTest.kt` + unit view model coverage |
| Docs & Release | Manifest integrity, OpenAPI coverage, no TODO | Release gate | infra/release-gate.sh + documentation review |
