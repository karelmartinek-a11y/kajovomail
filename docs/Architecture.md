# Architecture

## Overview
KajovoMail is a server-centric system where FastAPI backend services expose a single /api/v1 surface plus /api/v1/events/ws. Clients (web, desktop, Android) only talk to the API, never call OpenAI directly, and never persist mailbox data locally.

## Web client
- The `web/` project is a React + TypeScript SPA that consumes `/api/v1` and `/api/v1/events/ws`, applies brand tokens from `brand/ui-tokens/tokens.json` at runtime, and renders server-driven data in adaptive layouts.
- A centralized SessionProvider maintains authenticated state, loads the CSRF token, and attaches it to `axios` requests while surfacing HttpOnly cookie-managed sessions to every route.
- Playwright acceptance tests (`web/tests/e2e.spec.ts`) simulate login, navigation, Compose autosaves, and server search before each release to keep the UI aligned with backend structures.

## Bounded contexts
- **Auth / Users & Preferences** manage login, session tokens, JWT cookies, and user-scoped settings (including AI personalization).
- **Accounts & Credentials** manage IMAP/POP3/SMTP credentials, capability discovery, connection verification, and retryable metadata. POP3 accounts are flagged as limited and expose only inbox listings, while IMAP accounts keep full folder trees.
- **Mailbox Sync / Folders / Messages** synchronize with providers via Celery workers, maintain folder trees (default/system favorites vs. user folders), thread messages by RFC headers, and expose paging/virtual views (Unread, Flagged, With Attachments).
- **Drafts & Compose / Send** provide autosave drafts, compose/reply/reply-all/forward flows, HTML sanitization, and deterministic multipart/alternative MIME with text/plain + text/html payloads.
- **Search / AI Orchestration** provide policy-driven search syntax (AND, OR, NOT, quoted phrases) and orchestrate OpenAI Responses API calls on the server, storing structured metadata, plain text, HTML, preview, and optional persistence flag reset to store: false by default.
- **Offers / Audit & Security / Notifications & Events** expose offer workflows tied to threads/messages, audit log entries with correlation IDs, and a WebSocket event stream for live updates.

## Layers
1. Clients consume /api/v1 + events/WS through secure cookie auth and CSRF-protected mutate routes.
2. API routers include health, accounts, folders, messages, drafts, search, AI, offers, and events, all wired behind a unified api_router.
3. Services implement dependency-injected DB sessions, structured logging, correlation IDs, and capability-aware behavior.
4. PostgreSQL stores accounts, folders, messages, attachments, drafts, AI requests, offers, and audit logs while Redis drives Celery queues and temporary search state.
5. Celery workers execute sync_account, generate_ai_response, refresh_offer_status, and event broadcasts with retry policies documented in docs/TestMatrix.md.
6. Release gate scripts ensure no TODOs, manifest assets, OpenAPI coverage, and capability compliance before deployment.

## Android client
- Native Kotlin + Jetpack Compose stacks share the same API surface as the web/desktop clients. Navigation routes cover login, accounts/folders, messages/detail, compose, AI workflows, offers, and settings.
- Session CSRF tokens get stored in `EncryptedSharedPreferences`, event stream updates land via HTTP/WebSockets, and mail payloads stay in memory so no local mailbox DB is created.
## Desktop client
- The PySide6-based desktop app mirrors the web panels: accounts/folders on the left, message list in the middle, reading/compose center-right, and the AI/Offers column on the far right.
- All desktop actions (multi-select move/copy, compose, AI orchestration, offers auditing) call `/api/v1` or `/api/v1/events/ws`; mail state is kept in RAM widgets and never stored on disk, fulfilling the "no local mailbox DB" requirement.
