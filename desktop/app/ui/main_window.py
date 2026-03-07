from __future__ import annotations

import json
import threading
from typing import Dict, List

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTabWidget,
    QToolBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
)

from desktop.app.events.stream_worker import EventStreamWorker
from desktop.app.models import Account, Folder, Message, Offer
from desktop.app.services.api_client import ApiClient, ApiError
from desktop.app.services.session_manager import SessionManager
from desktop.app.ui.login_dialog import LoginDialog


class KajovoMailMainWindow(QMainWindow):
    def __init__(self, api_client: ApiClient, session_manager: SessionManager) -> None:
        super().__init__()
        self.api_client = api_client
        self.session_manager = session_manager
        self.setWindowTitle("KajovoMail Desktop")
        self.setMinimumSize(1200, 800)
        self._accounts: List[Account] = []
        self._messages: Dict[str, Message] = {}
        self._folders: Dict[str, List[Folder]] = {}
        self._current_folder_id: str | None = None
        self._event_worker: EventStreamWorker | None = None
        self._editing_draft = False
        self._ai_models: List[str] = []
        self._setup_ui()
        QTimer.singleShot(100, self._run_login)

    def _setup_ui(self) -> None:
        toolbar = QToolBar("Main toolbar")
        toolbar.setMovable(False)
        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut(QKeySequence("F5"))
        refresh_action.triggered.connect(self._refresh_accounts)
        toolbar.addAction(refresh_action)
        compose_action = QAction("Compose", self)
        compose_action.setShortcut(QKeySequence("Ctrl+N"))
        compose_action.triggered.connect(lambda: self.reading_pane.setFocus())
        toolbar.addAction(compose_action)
        search_action = QAction("Search", self)
        search_action.setShortcut(QKeySequence("Ctrl+F"))
        search_action.triggered.connect(lambda: self.reader_status("Search panel ready."))
        toolbar.addAction(search_action)
        logout_action = QAction("Logout", self)
        logout_action.setShortcut(QKeySequence("Ctrl+Shift+Q"))
        logout_action.triggered.connect(self._logout)
        toolbar.addAction(logout_action)
        self.addToolBar(toolbar)

        central_split = QSplitter(Qt.Horizontal)
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_layout.addWidget(QLabel("Accounts & folders"))
        self.account_list = QListWidget()
        self.account_list.currentItemChanged.connect(self._on_account_selected)
        left_layout.addWidget(self.account_list)
        self.folder_tree = QTreeWidget()
        self.folder_tree.setHeaderHidden(True)
        self.folder_tree.itemClicked.connect(self._on_folder_clicked)
        self.folder_tree.setAcceptDrops(True)
        self.folder_tree.dragEnterEvent = self._folder_drag_enter
        self.folder_tree.dropEvent = self._folder_drop
        left_layout.addWidget(self.folder_tree)
        central_split.addWidget(left_panel)

        self.message_list = QListWidget()
        self.message_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.message_list.setDragEnabled(True)
        self.message_list.setDragDropMode(QListWidget.DragOnly)
        self.message_list.itemSelectionChanged.connect(self._display_selected_message)
        central_split.addWidget(self.message_list)

        right_main = QSplitter(Qt.Vertical)
        self.reading_pane = QTextEdit()
        self.reading_pane.setReadOnly(True)
        right_main.addWidget(self.reading_pane)
        compose_widget = QWidget()
        compose_layout = QVBoxLayout()
        compose_widget.setLayout(compose_layout)
        self.compose_recipient = QLineEdit()
        self.compose_recipient.setPlaceholderText("recipient@provider")
        self.compose_subject = QLineEdit()
        self.compose_subject.setPlaceholderText("Subject")
        self.compose_body = QTextEdit()
        send_button = QPushButton("Send multipart draft")
        send_button.clicked.connect(self._send_compose)
        compose_layout.addWidget(QLabel("Compose"))
        compose_layout.addWidget(self.compose_recipient)
        compose_layout.addWidget(self.compose_subject)
        compose_layout.addWidget(self.compose_body)
        compose_layout.addWidget(send_button)
        right_main.addWidget(compose_widget)
        central_split.addWidget(right_main)

        ai_offers_panel = QTabWidget()
        ai_panel = QWidget()
        ai_layout = QVBoxLayout()
        ai_panel.setLayout(ai_layout)
        self.ai_prompt = QTextEdit()
        ai_layout.addWidget(QLabel("AI prompt"))
        ai_layout.addWidget(self.ai_prompt)
        ai_run = QPushButton("Run AI orchestration")
        ai_run.clicked.connect(self._run_ai)
        ai_layout.addWidget(ai_run)
        self.ai_output = QTextEdit()
        self.ai_output.setReadOnly(True)
        ai_layout.addWidget(self.ai_output)
        ai_offers_panel.addTab(ai_panel, "AI console")

        offers_panel = QWidget()
        offers_layout = QVBoxLayout()
        offers_panel.setLayout(offers_layout)
        self.offer_list = QListWidget()
        self.offer_list.setSelectionMode(QListWidget.SingleSelection)
        offers_layout.addWidget(QLabel("Offers"))
        offers_layout.addWidget(self.offer_list)
        ai_offers_panel.addTab(offers_panel, "Offers")

        settings_panel = QWidget()
        settings_layout = QVBoxLayout()
        settings_panel.setLayout(settings_layout)
        settings_layout.addWidget(QLabel("OpenAI API key"))
        self.ai_api_key = QLineEdit()
        self.ai_api_key.setPlaceholderText("sk-...")
        self.ai_api_key.setEchoMode(QLineEdit.Password)
        settings_layout.addWidget(self.ai_api_key)
        settings_layout.addWidget(QLabel("Response style"))
        self.ai_style = QComboBox()
        self.ai_style.addItems(["concise", "balanced", "detailed"])
        settings_layout.addWidget(self.ai_style)
        settings_layout.addWidget(QLabel("OpenAI model"))
        self.ai_model = QComboBox()
        self.ai_model.setEditable(True)
        settings_layout.addWidget(self.ai_model)
        test_key_button = QPushButton("Test API key")
        test_key_button.clicked.connect(self._test_ai_key)
        settings_layout.addWidget(test_key_button)
        load_models_button = QPushButton("Load models")
        load_models_button.clicked.connect(self._load_ai_models)
        settings_layout.addWidget(load_models_button)
        save_settings_button = QPushButton("Save AI settings")
        save_settings_button.clicked.connect(self._save_ai_settings)
        settings_layout.addWidget(save_settings_button)
        ai_offers_panel.addTab(settings_panel, "Settings")

        central_split.addWidget(ai_offers_panel)
        central_split.setStretchFactor(1, 2)
        central_split.setStretchFactor(2, 3)
        self.setCentralWidget(central_split)

        self.status_label = QLabel("Awaiting backend connection...")
        self.statusBar().addWidget(self.status_label)

    def _run_login(self) -> None:
        dialog = LoginDialog(self.api_client, self.session_manager)
        if dialog.exec() == LoginDialog.Accepted:
            self.reader_status("Authenticated as " + (self.session_manager.current_user() or "unknown"))
            self._refresh_accounts()
            self._refresh_offers()
            self._load_ai_settings()
            self._start_event_stream()
        else:
            self.close()

    def _refresh_accounts(self) -> None:
        def task() -> None:
            try:
                accounts = self.api_client.accounts()
                QTimer.singleShot(0, lambda: self._populate_accounts(accounts))
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        threading.Thread(target=task, daemon=True).start()

    def _populate_accounts(self, accounts: List[Account]) -> None:
        self._accounts = accounts
        self.account_list.clear()
        for account in accounts:
            QListWidgetItem(f"{account.provider} ({account.email})", self.account_list)

    def _on_account_selected(self, current: QListWidgetItem | None) -> None:
        index = self.account_list.row(current) if current else -1
        if index >= 0:
            account = self._accounts[index]
            self._load_folders(account.id)

    def _load_folders(self, account_id: str) -> None:
        def task() -> None:
            try:
                folders = self.api_client.folders(account_id)
                QTimer.singleShot(0, lambda: self._populate_folders(account_id, folders))
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        threading.Thread(target=task, daemon=True).start()

    def _populate_folders(self, account_id: str, folders: List[Folder]) -> None:
        self._folders[account_id] = folders
        self.folder_tree.clear()
        for folder in folders:
            node = QTreeWidgetItem([folder.name])
            node.setData(0, Qt.UserRole, folder.id)
            self.folder_tree.addTopLevelItem(node)

    def _on_folder_clicked(self, item: QTreeWidgetItem) -> None:
        folder_id = item.data(0, Qt.UserRole)
        if folder_id:
            self._current_folder_id = folder_id
            self.reader_status(f"Fetching {item.text(0)}...")
            self._load_messages(folder_id)

    def _load_messages(self, folder_id: str) -> None:
        def task() -> None:
            try:
                messages = self.api_client.messages(folder_id)
                QTimer.singleShot(0, lambda: self._populate_messages(messages))
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        threading.Thread(target=task, daemon=True).start()

    def _populate_messages(self, messages: List[Message]) -> None:
        self.message_list.clear()
        self._messages = {message.id: message for message in messages}
        for message in messages:
            item = QListWidgetItem(f"{message.sender}: {message.subject}")
            item.setData(Qt.UserRole, message.id)
            item.setToolTip(message.snippet)
            self.message_list.addItem(item)

    def _display_selected_message(self) -> None:
        selected = self.message_list.selectedItems()
        if selected:
            message_id = selected[-1].data(Qt.UserRole)
            message = self._messages.get(message_id)
            if message:
                self.reading_pane.setPlainText(
                    f"From: {message.sender}\nSubject: {message.subject}\n\n{message.snippet}"
                )
        else:
            self.reading_pane.clear()

    def _send_compose(self) -> None:
        if self._editing_draft:
            return
        draft = {
            "to": self.compose_recipient.text(),
            "subject": self.compose_subject.text(),
            "body": self.compose_body.toPlainText(),
            "flags": ["draft"],
        }

        def task() -> None:
            try:
                self.api_client.compose(draft)
                QTimer.singleShot(0, lambda: self.reader_status("Draft sent for multipart dispatch."))
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        self._editing_draft = True
        threading.Thread(target=task, daemon=True).start()
        QTimer.singleShot(2500, self._reset_draft_flag)

    def _reset_draft_flag(self) -> None:
        self._editing_draft = False

    def _run_ai(self) -> None:
        prompt = self.ai_prompt.toPlainText().strip()
        if not prompt:
            self.reader_status("AI prompt cannot be empty.")
            return

        def task() -> None:
            try:
                response = self.api_client.ai_request(prompt)
                QTimer.singleShot(
                    0,
                    lambda: self.ai_output.setPlainText(
                        f"Summary:\n{response.summary}\n\nHTML preview:\n{response.html_preview}\n\nPolicy: {response.policy}"
                    ),
                )
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        threading.Thread(target=task, daemon=True).start()

    def _load_ai_settings(self) -> None:
        def task() -> None:
            try:
                payload = self.api_client.get_ai_settings()
                QTimer.singleShot(0, lambda: self._apply_ai_settings(payload))
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        threading.Thread(target=task, daemon=True).start()

    def _apply_ai_settings(self, payload: Dict[str, object]) -> None:
        style = str(payload.get("response_style", "balanced"))
        model = str(payload.get("model") or "")
        index = self.ai_style.findText(style)
        if index >= 0:
            self.ai_style.setCurrentIndex(index)
        self.ai_model.clear()
        if model:
            self.ai_model.addItem(model)
            self.ai_model.setCurrentText(model)
        masked = payload.get("openai_api_key_masked")
        if masked:
            self.ai_api_key.setPlaceholderText(str(masked))
        self.reader_status("AI settings loaded.")

    def _test_ai_key(self) -> None:
        key = self.ai_api_key.text().strip() or None

        def task() -> None:
            try:
                payload = self.api_client.test_openai_key(key)
                models = payload.get("models", [])
                QTimer.singleShot(0, lambda: self._apply_model_list(models))
                QTimer.singleShot(0, lambda: self.reader_status(str(payload.get("message", "Key test done"))))
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        threading.Thread(target=task, daemon=True).start()

    def _load_ai_models(self) -> None:
        def task() -> None:
            try:
                models = self.api_client.list_openai_models()
                QTimer.singleShot(0, lambda: self._apply_model_list(models))
                QTimer.singleShot(0, lambda: self.reader_status(f"Loaded {len(models)} OpenAI models."))
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        threading.Thread(target=task, daemon=True).start()

    def _apply_model_list(self, models: List[str]) -> None:
        current = self.ai_model.currentText()
        self.ai_model.clear()
        for model in models:
            self.ai_model.addItem(model)
        if current:
            self.ai_model.setCurrentText(current)
        elif models:
            self.ai_model.setCurrentIndex(0)

    def _save_ai_settings(self) -> None:
        key = self.ai_api_key.text().strip()
        style = self.ai_style.currentText().strip().lower()
        model = self.ai_model.currentText().strip()

        def task() -> None:
            try:
                self.api_client.update_ai_settings(
                    openai_api_key=key if key else None,
                    response_style=style,
                    model=model if model else None,
                )
                QTimer.singleShot(0, lambda: self.ai_api_key.clear())
                QTimer.singleShot(0, lambda: self.reader_status("AI settings saved."))
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        threading.Thread(target=task, daemon=True).start()

    def _refresh_offers(self) -> None:
        def task() -> None:
            try:
                offers = self.api_client.offers()
                QTimer.singleShot(0, lambda: self._populate_offers(offers))
            except ApiError as exc:
                QTimer.singleShot(0, lambda: self.reader_status(str(exc)))

        threading.Thread(target=task, daemon=True).start()

    def _populate_offers(self, offers: List[Offer]) -> None:
        self.offer_list.clear()
        for offer in offers:
            item = QListWidgetItem(f"[{offer.state}] {offer.title}")
            self.offer_list.addItem(item)

    def _start_event_stream(self) -> None:
        if self._event_worker:
            self._event_worker.stop()
        headers = self.api_client.cookie_header()
        self._event_worker = EventStreamWorker(self.api_client.base_url, headers or None)
        self._event_worker.event_received.connect(self._handle_event)
        self._event_worker.error.connect(lambda exc: self.reader_status("Event stream interrupted: " + str(exc)))
        self._event_worker.start()

    def _handle_event(self, raw_event: str) -> None:
        try:
            data = json.loads(raw_event)
            self.reader_status(f"Event: {data.get('type', 'update')}")
            if data.get("type") in ("folder.sync", "message.update") and self._current_folder_id:
                self._load_messages(self._current_folder_id)
        except json.JSONDecodeError:
            pass

    def _logout(self) -> None:
        def task() -> None:
            try:
                self.api_client.logout()
            except Exception:
                pass
            self.session_manager.clear()
            QTimer.singleShot(0, self.close)

        threading.Thread(target=task, daemon=True).start()

    def _folder_drag_enter(self, event) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def _folder_drop(self, event) -> None:
        target = self.folder_tree.itemAt(event.position().toPoint())
        if not target:
            return
        folder_id = target.data(0, Qt.UserRole)
        if not folder_id:
            return
        selected = [item.data(Qt.UserRole) for item in self.message_list.selectedItems()]
        action = "copy" if event.keyboardModifiers() & Qt.ControlModifier else "move"
        self.reader_status(f"{action.title()} {len(selected)} message(s) into {target.text(0)}")
        event.acceptProposedAction()

    def reader_status(self, message: str) -> None:
        self.status_label.setText(message)
