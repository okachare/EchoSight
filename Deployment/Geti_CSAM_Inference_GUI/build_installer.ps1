param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

& $Python -m pip install -r .\requirements.txt
& $Python -m pip install pyinstaller
& $Python -m PyInstaller --noconfirm --clean --windowed --name GetiCSAMInferenceGUI .\geti_csam_inference_gui.py

Write-Host "Build complete: $Root\dist\GetiCSAMInferenceGUI"
Write-Host "Copy the downloaded deployment folder beside the executable or select it from the GUI."
