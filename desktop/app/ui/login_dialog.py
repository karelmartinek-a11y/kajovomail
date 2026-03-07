import threading
from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
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
        self._assets_dir = Path(__file__).resolve().parents[1] / 'assets'
        self.setWindowTitle('KajovoMail přihlášení')
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        brand_row = QHBoxLayout()
        signace_label = QLabel()
        mark_label = QLabel()
        signace = QPixmap(str(self._assets_dir / 'kajovo_signace.png'))
        mark = QPixmap(str(self._assets_dir / 'kajovo_mark.png'))
        if not signace.isNull():
            signace_label.setPixmap(signace.scaled(20, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if not mark.isNull():
            mark_label.setPixmap(mark.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        brand_row.addWidget(signace_label)
        brand_row.addWidget(mark_label)
        brand_row.addWidget(QLabel('KajovoMail'))
        brand_row.addStretch(1)
        layout.addLayout(brand_row)

        form = QFormLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('uzivatel@hcasc.cz')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form.addRow('E-mail', self.email_input)
        form.addRow('Heslo', self.password_input)
        layout.addLayout(form)

        self.status_label = QLabel('Zadejte přihlašovací údaje pro backend KajovoMail.')
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText('Přihlásit')
        buttons.button(QDialogButtonBox.Cancel).setText('Zrušit')
        buttons.accepted.connect(self.do_login)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        floating_signace = QLabel()
        floating = QPixmap(str(self._assets_dir / 'kajovo_signace.png'))
        if not floating.isNull():
            floating_signace.setPixmap(floating.scaled(18, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        floating_signace.setAlignment(Qt.AlignLeft)
        layout.addWidget(floating_signace)

        self.setLayout(layout)

    def do_login(self) -> None:
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        if not email or not password:
            self._async_status('E-mail i heslo jsou povinné.')
            return

        self._async_status('Přihlašuji...')
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
            self._async_status('Přihlášení selhalo: ' + str(exc))

    def _async_accept(self) -> None:
        QTimer.singleShot(0, self.accept)

    def _async_status(self, message: str) -> None:
        QTimer.singleShot(0, lambda: self.status_label.setText(message))
