$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$iconDir = Join-Path $root "src-tauri/icons"
New-Item -ItemType Directory -Force -Path $iconDir | Out-Null

$bitmap = New-Object System.Drawing.Bitmap 256, 256
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.Clear([System.Drawing.Color]::FromArgb(8, 13, 24))

$accent = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(76, 211, 226))
$dark = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(76, 211, 226)), 12
$graphics.FillEllipse($accent, 34, 34, 188, 188)
$inner = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(8, 13, 24))
$graphics.FillEllipse($inner, 48, 48, 160, 160)

$font = New-Object System.Drawing.Font("Segoe UI", 112, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$format = New-Object System.Drawing.StringFormat
$format.Alignment = [System.Drawing.StringAlignment]::Center
$format.LineAlignment = [System.Drawing.StringAlignment]::Center
$graphics.DrawString("Y", $font, $accent, (New-Object System.Drawing.RectangleF(0, 0, 256, 256)), $format)

$iconHandle = $bitmap.GetHicon()
$icon = [System.Drawing.Icon]::FromHandle($iconHandle)
$stream = [System.IO.File]::Create((Join-Path $iconDir "icon.ico"))
try { $icon.Save($stream) } finally { $stream.Dispose() }

$icon.Dispose()
$font.Dispose()
$format.Dispose()
$accent.Dispose()
$inner.Dispose()
$dark.Dispose()
$graphics.Dispose()
$bitmap.Dispose()

if (-not (Test-Path (Join-Path $iconDir "icon.ico"))) {
  throw "Windows icon generation failed."
}
Write-Host "Generated src-tauri/icons/icon.ico"
