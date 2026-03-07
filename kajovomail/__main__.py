from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from desktop.app.main import run_desktop


def _resource_path(relative_path: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parents[1] / relative_path


def main() -> int:
    app = QApplication(sys.argv)
    icon_path = _resource_path("desktop/app/assets/kajovomail_icon.png")
    if icon_path.exists():
        icon = QIcon(str(icon_path))
        app.setWindowIcon(icon)
    window = run_desktop()
    if icon_path.exists():
        window.setWindowIcon(QIcon(str(icon_path)))
    window.showMaximized()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

