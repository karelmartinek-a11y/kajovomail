from desktop.app.services.api_client import ApiClient
from desktop.app.services.session_manager import SessionManager
from desktop.app.ui.main_window import KajovoMailMainWindow


def run_desktop() -> KajovoMailMainWindow:
    api_base = "https://mail.hcasc.cz/api/v1"
    api_client = ApiClient(api_base)
    session_manager = SessionManager(api_client)
    session_manager.restore_csrf()
    return KajovoMailMainWindow(api_client, session_manager)
