# KajovoMail Desktop

A native PySide6 Qt 6 application for Windows and macOS. The UI communicates solely with the `/api/v1` surface and `/api/v1/events/ws` stream exposed by the backend, relies on HttpOnly cookies, and keeps mailbox data entirely in RAM so no local database ever stores mail.

## Running locally
1. Create a virtual environment (Python 3.12+). `python -m venv .venv`.
2. Install deps: `.venv\Scripts\pip install -e .` (Windows) or `./.venv/bin/pip install -e .` (macOS). This installs PySide6, httpx, websockets, keyring, and dotenv support.
3. Ensure `KAJOVOMAIL_API_BASE` environment variable points to the backend (e.g., `http://localhost:8000/api/v1`).
4. Launch: `.venv\Scripts\python main.py` (Windows) or `./.venv/bin/python main.py` (macOS).

## Desktop architecture
- Layout: accounts/folders panel (left), message list (center), reading+compose split (right), AI/offers stack (rightmost), and a toolbar with Refresh/Compose/Search/Logout actions.
- The event stream (`/events/ws`) runs in its own thread via `websockets` and pushes sync/draft/offer updates to the UI.
- Session cookies are preserved by httpx, and credentials/CSRF tokens are mirrored in the OS keyring for secure storage; plain text mail bodies remain in RAM only.

## Building
- Windows: `pyinstaller --onefile --name KajovoMail desktop/app/main.py`. Run inside the activated virtualenv and keep `dist/KajovoMail.exe` for distribution.
- macOS: identical command builds a `.app` bundle when executed on macOS hosts. Use `--windowed` for GUI-only shims if desired.
- Build scripts: `scripts/build_windows.bat` and `scripts/build_macos.sh` (create if needed) wrap these commands and place artifacts under `dist/`.
- Always test builds by running the created executable to verify secure session handling and event stream connectivity.

## Security & storage
- Session tokens never leave the OS keyring; only the backend sets HttpOnly cookies, and httpx forwards them automatically.
- Mail data (messages, folders, drafts, AI output) is cached in-memory widgets; nothing is persisted to disk, meeting the "no local mailbox DB" requirement.
- Admin data such as offers or AI prompts remain on the backend, and clients refresh via WebSocket events to keep displays current.
