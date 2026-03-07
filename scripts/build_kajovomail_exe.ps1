Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    throw "Virtualenv python not found: $venvPython"
}

& (Join-Path $scriptDir "prepare_brand_assets.ps1")

& $venvPython -m pip install -r (Join-Path $repoRoot "requirements.txt")
& $venvPython -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name KajovoMail `
    --icon (Join-Path $repoRoot "desktop\app\assets\kajovomail_icon.ico") `
    --add-data ((Join-Path $repoRoot "desktop\app\assets\kajovomail_icon.png") + ";desktop\app\assets") `
    (Join-Path $repoRoot "kajovomail\__main__.py")

Write-Host ""
Write-Host "Build complete:"
Write-Host (Join-Path $repoRoot "dist\KajovoMail.exe")
