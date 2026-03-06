#!/bin/bash
set -euo pipefail
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "Activate virtualenv before building."
  exit 1
fi
pyinstaller --onefile --windowed --name KajovoMail main.py
