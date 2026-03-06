import os
import sys

from PySide6.QtWidgets import QApplication

from desktop.app.main import run_desktop

if __name__ == "__main__":
    os.environ.setdefault("KAJOVOMAIL_API_BASE", "http://localhost:8000/api/v1")
    app = QApplication(sys.argv)
    window = run_desktop()
    window.showMaximized()
    sys.exit(app.exec())
