@echo off
if "%VIRTUAL_ENV%" == "" (
  echo Activate virtualenv before building.
  exit /b 1
)
pyinstaller --onefile --windowed --name KajovoMail main.py
