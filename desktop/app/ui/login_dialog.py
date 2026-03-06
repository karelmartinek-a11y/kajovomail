import threading

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QFormLayout,
    QVBoxLayout,
)

from desktop.app.services.api_client import ApiClient, ApiError
from desktop.app.services.session_manager import SessionManager

class LoginDialog(QDialog):
    def __init__(self, api_client: ApiClient, session_manager: SessionManager) -> None:
        super().__init__()
        self.api_client = api_client
        self.session_manager = session_manager
        self.setWindowTitle('KajovoMail login')
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        form = QFormLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('user@hcasc.cz')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form.addRow('Email', self.email_input)
        form.addRow('Password', self.password_input)
        layout.addLayout(form)

        self.status_label = QLabel('Provide credentials to reach the server-centric backend.')
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText('Login')
        buttons.accepted.connect(self.do_login)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def do_login(self) -> None:
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        if not email or not password:
            self._async_status('Both email and password are required.')
            return

        self._async_status('Logging in...')
        threading.Thread(target=self._login_worker, args=(email, password), daemon=True).start()

    def _login_worker(self, email: str, password: str) -> None:
        try:
            result = self.api_client.login(email, password)
            csrf = result.get('csrfToken')
            if csrf:
                self.session_manager.store_csrf(csrf)
            self.session_manager.store_current_user(email)
            self._async_accept()
        except ApiError as exc:
            self._async_status(str(exc))
        except Exception as exc:  # pragma: no cover
            self._async_status('Authentication failed: ' + str(exc))

    def _async_accept(self) -> None:
        QTimer.singleShot(0, self.accept)

    def _async_status(self, message: str) -> None:
        QTimer.singleShot(0, lambda: self.status_label.setText(message))
