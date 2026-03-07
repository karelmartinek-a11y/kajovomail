import sys

from PySide6.QtWidgets import QApplication

from desktop.app.main import run_desktop

if __name__ == "__main__":
    # Desktop client is always wired to the production backend; no runtime overrides allowed.
    app = QApplication(sys.argv)
    window = run_desktop()
    window.showMaximized()
    sys.exit(app.exec())
