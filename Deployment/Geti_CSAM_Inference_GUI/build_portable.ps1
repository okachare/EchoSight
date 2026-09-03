param(
    [string]$PythonHome = "$env:LOCALAPPDATA\Programs\Python\Python39",
    [string]$PackageRoot = "C:\GetiCSAMInstallerBuild\site",
    [string]$DeploymentSource = "$(Join-Path (Split-Path -Parent $PSScriptRoot) 'Test_Run_Detect\deployment\Detection')",
    [string]$OutputRoot = "$(Join-Path $PSScriptRoot 'portable')"
)

$ErrorActionPreference = "Stop"
$GuiRoot = $PSScriptRoot

if (-not (Test-Path "$PythonHome\pythonw.exe")) {
    throw "Python 3.9 was not found at $PythonHome"
}
if (-not (Test-Path "$PackageRoot\openvino\__init__.py")) {
    throw "The compatible OpenVINO package directory was not found at $PackageRoot"
}
if (-not (Test-Path "$DeploymentSource\model")) {
    throw "The deployment model directory was not found at $DeploymentSource\model"
}

if (Test-Path $OutputRoot) {
    Remove-Item -Recurse -Force $OutputRoot
}
New-Item -ItemType Directory -Force -Path "$OutputRoot\runtime\Lib\site-packages", "$OutputRoot\deployment\Detection" | Out-Null

Copy-Item "$PythonHome\pythonw.exe", "$PythonHome\python.exe", "$PythonHome\python39.dll", "$PythonHome\python3.dll", "$PythonHome\vcruntime140.dll", "$PythonHome\vcruntime140_1.dll" "$OutputRoot\runtime" -Force
Copy-Item "$PythonHome\Lib\*.py" "$OutputRoot\runtime\Lib" -Force
Copy-Item "$PythonHome\Lib\*.zip" "$OutputRoot\runtime\Lib" -Force -ErrorAction SilentlyContinue
foreach ($folder in @("asyncio", "collections", "concurrent", "ctypes", "email", "encodings", "importlib", "json", "logging", "multiprocessing", "pathlib", "re", "sqlite3", "tkinter", "unittest", "urllib", "xml")) {
    if (Test-Path "$PythonHome\Lib\$folder") {
        Copy-Item "$PythonHome\Lib\$folder" "$OutputRoot\runtime\Lib" -Recurse -Force
    }
}
Copy-Item "$PythonHome\DLLs\*" "$OutputRoot\runtime\DLLs" -Recurse -Force
Copy-Item "$PythonHome\tcl" "$OutputRoot\runtime" -Recurse -Force
Write-Host "Copying complete verified inference package set"
Get-ChildItem $PackageRoot -Force | Where-Object { $_.Name -notin @("PyInstaller", "pyinstaller-6.22.2.dist-info", "pyinstaller_hooks_contrib-2026.7.dist-info", "_pyinstaller_hooks_contrib") } | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination "$OutputRoot\runtime\Lib\site-packages\$($_.Name)" -Recurse -Force
}
if (-not (Test-Path "$OutputRoot\runtime\Lib\site-packages\openvino\__init__.py")) { throw "OpenVINO was not copied" }
if (-not (Test-Path "$OutputRoot\runtime\Lib\site-packages\model_api\__init__.py")) { throw "Geti model API was not copied" }
Copy-Item "$GuiRoot\geti_csam_inference_gui.py", "$GuiRoot\Launch_Geti_CSAM_GUI.bat", "$GuiRoot\README.md" $OutputRoot -Force
Copy-Item -Path "$DeploymentSource\*" -Destination "$OutputRoot\deployment\Detection" -Recurse -Force
if (-not (Test-Path "$OutputRoot\deployment\Detection\model\model.xml")) { throw "Model XML was not copied" }

@"
Geti CSAM Inference GUI - portable folder

Double-click Launch_Geti_CSAM_GUI.bat.
This folder contains the Python runtime, OpenVINO dependencies, Geti wrapper, and model deployment.
It can be copied to another Windows machine with no separate Python or OpenVINO installation.
"@ | Set-Content "$OutputRoot\README_PORTABLE.txt" -Encoding ASCII

Write-Host "Portable GUI created: $OutputRoot"
Write-Host "Folder size: $('{0:N0}' -f ((Get-ChildItem $OutputRoot -Recurse -File | Measure-Object Length -Sum).Sum / 1MB)) MB"