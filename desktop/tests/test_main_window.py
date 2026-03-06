import pytest

from PySide6.QtWidgets import QApplication

from desktop.app.models import Account, Folder, Message, Offer
from desktop.app.ui.main_window import KajovoMailMainWindow



class DummyApiClient:
    base_url = "http://localhost:8000/api/v1"

    def __init__(self):
        self.composed = []

    def accounts(self):
        return [Account(id="1", provider="IMAP", email="test@hcasc.cz", capability="sync")]

    def folders(self, account_id: str):
        return [Folder(id="inbox", name="Inbox", account_id=account_id, is_system=True)]

    def messages(self, folder_id: str, limit: int = 50):
        return [
            Message(
                id="msg-1",
                subject="Test",
                sender="dev@hcasc.cz",
                folder_id=folder_id,
                snippet="Sample",
                flags=[],
            )
        ]

    def compose(self, draft):
        self.composed.append(draft)
        return {"status": "queued"}

    def ai_request(self, prompt: str):
        class Response:
            summary = "Summarized"
            html_preview = "<p>Preview</p>"
            policy = "store: false"

        return Response()

    def offers(self):
        return [Offer(thread_id="#1", title="Test Offer", state="draft", message_id=None)]

    def logout(self):
        return None

    def cookie_header(self):
        return ""


class DummySessionManager:
    def __init__(self):
        self.user = "test@hcasc.cz"
        self.csrf = None

    def store_csrf(self, token: str) -> None:
        self.csrf = token

    def store_current_user(self, email: str) -> None:
        self.user = email

    def clear(self) -> None:
        self.user = None

    def current_user(self) -> str | None:
        return self.user


@pytest.fixture
def qt_app():
    return QApplication.instance() or QApplication([])


def test_window_loads(qtbot, qt_app):
    api = DummyApiClient()
    session = DummySessionManager()
    window = KajovoMailMainWindow(api, session)
    window._run_login = lambda: None
    qtbot.addWidget(window)
    window.reader_status("Ready")
    assert window.status_label.text() == "Ready"
    window._accounts = api.accounts()
    window._populate_accounts(window._accounts)
    assert window.account_list.count() == 1

def test_compose_updates_status(qtbot, qt_app):
    api = DummyApiClient()
    session = DummySessionManager()
    window = KajovoMailMainWindow(api, session)
    window._run_login = lambda: None
    qtbot.addWidget(window)
    window.compose_recipient.setText("user@hcasc.cz")
    window.compose_subject.setText("Hi")
    window.compose_body.setPlainText("Hello")
    window._send_compose()
    qtbot.wait(100)
    assert api.composed
    assert "draft" in api.composed[0]["flags"]
