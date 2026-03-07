Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

$sourceLogo = Join-Path $repoRoot "brand\logo\exports\mark\png\kajovo-mail_mark_512.png"
$desktopAssetsDir = Join-Path $repoRoot "desktop\app\assets"
$webPublicDir = Join-Path $repoRoot "web\public"
$desktopPng = Join-Path $desktopAssetsDir "kajovomail_icon.png"
$desktopIco = Join-Path $desktopAssetsDir "kajovomail_icon.ico"
$webPng = Join-Path $webPublicDir "favicon.png"
$webIco = Join-Path $webPublicDir "favicon.ico"

New-Item -ItemType Directory -Force -Path $desktopAssetsDir | Out-Null
New-Item -ItemType Directory -Force -Path $webPublicDir | Out-Null

if (-not (Test-Path $sourceLogo)) {
    throw "Logo not found: $sourceLogo"
}

Copy-Item -Path $sourceLogo -Destination $desktopPng -Force
Copy-Item -Path $sourceLogo -Destination $webPng -Force

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class NativeMethods {
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern bool DestroyIcon(IntPtr handle);
}
"@

function Convert-PngToIco {
    param(
        [Parameter(Mandatory = $true)][string]$InputPath,
        [Parameter(Mandatory = $true)][string]$OutputPath
    )

    $bitmap = New-Object System.Drawing.Bitmap($InputPath)
    try {
        $hIcon = $bitmap.GetHicon()
        try {
            $icon = [System.Drawing.Icon]::FromHandle($hIcon)
            try {
                $stream = [System.IO.File]::Open($OutputPath, [System.IO.FileMode]::Create)
                try {
                    $icon.Save($stream)
                }
                finally {
                    $stream.Dispose()
                }
            }
            finally {
                $icon.Dispose()
            }
        }
        finally {
            [NativeMethods]::DestroyIcon($hIcon) | Out-Null
        }
    }
    finally {
        $bitmap.Dispose()
    }
}

Convert-PngToIco -InputPath $sourceLogo -OutputPath $desktopIco
Copy-Item -Path $desktopIco -Destination $webIco -Force

Write-Host "Brand assets prepared:"
Write-Host " - $desktopPng"
Write-Host " - $desktopIco"
Write-Host " - $webPng"
Write-Host " - $webIco"
