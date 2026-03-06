# Security

## Principles
1. **Server-centric controls**—session tokens, OpenAI keys, and mailbox sync happen inside backend/worker layers; clients never store these secrets nor retry mail fetches independently.
2. **Audit & correlation**—every state-changing action (login/logout, AI request, offer transition, folder mutation) logs an entry with correlation ID, user, source client, and sanitized payload. Logs never include user credentials, raw AI prompt content, or attachments.
3. **Capability enforcement**—POP3 accounts are treated as read-only limited zones; their capability metadata blocks folder writes, attachments, and search beyond inbox scope.
4. **AI privacy**—requests pass through backend/app/services/ai.py which validates the schema, enforces store: false by default, and stores only sanitized structured output; standard logs only capture status, not prompt/response body.

## Runtime safeguards
- Sessions use secure cookies with CSRF protection; logout-all revokes every row in sessions for the user.
- Email sync/update workers propagate retries via Celery with idempotency checks (cursor updates, auditing) and honor capability flags.
- The React web SPA injects the server-provided CSRF token via the SessionProvider, keeps the OpenAI key server-side, and only talks to `/api/v1` + `/api/v1/events/ws` so secrets never surface in client bundle.
- Release gate script in infra/release-gate.sh rejects deployments that reference TODO/TBD placeholders, violate manifest assets, or expose OpenAI keys to clients.
- The PySide6 desktop client stores only the CSRF occurrence in the OS keyring, keeps the HttpOnly cookie alive through httpx, and caches mailbox state in-memory widgets; there is no persistent local mailbox database or log of message bodies.
