param(
    [string]$PythonHome = "$env:LOCALAPPDATA\Programs\Python\Python39",
    [string]$PackageRoot = "C:\GetiCSAMInstallerBuild\site",
    [string]$DeploymentSource = "$(Join-Path (Split-Path -Parent $PSScriptRoot) 'Test_Run_Detect\deployment\Detection')",
    [string]$OutputRoot = "$(Join-Path $PSScriptRoot 'portable_pyqt6')"
)

$ErrorActionPreference = "Stop"
$GuiRoot = $PSScriptRoot

Write-Host ""
Write-Host "=== EchoSight PyQt6 Portable Build ===" -ForegroundColor Cyan
Write-Host ""

# Validation
Write-Host "Validating prerequisites..." -ForegroundColor Cyan
$pyexe = Get-ChildItem -Path "$PythonHome\Scripts" -Filter "python.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pyexe) {
    throw "Python not found at: $PythonHome\Scripts`nPlease ensure Python virtual environment exists."
}
Write-Host "  * Python found: $($pyexe.FullName)" -ForegroundColor Green

if (-not (Test-Path "$PackageRoot\openvino\__init__.py")) {
    throw "OpenVINO package not found at: $PackageRoot`nPlease build OpenVINO package first."
}
Write-Host "  * OpenVINO package found: OK" -ForegroundColor Green

if (-not (Test-Path "$DeploymentSource\model")) {
    throw "Deployment model not found at: $DeploymentSource\model`nModel files missing."
}
Write-Host "  * Deployment model found: OK" -ForegroundColor Green

# Cleanup old build
if (Test-Path $OutputRoot) {
    Write-Host "Removing old build: $OutputRoot"
    Remove-Item -Recurse -Force $OutputRoot
}

# Create directory structure
Write-Host "Creating directory structure..."
New-Item -ItemType Directory -Force -Path `
    "$OutputRoot\runtime\Lib\site-packages",
    "$OutputRoot\runtime\DLLs",
    "$OutputRoot\deployment\Detection",
    "$OutputRoot\models" | Out-Null

# Copy Python runtime executables
Write-Host "Copying Python runtime..."
$scripts_dir = "$PythonHome\Scripts"
$dlls_to_copy = Get-ChildItem -Path $PythonHome -Filter "python*.dll" -ErrorAction SilentlyContinue
$dlls_to_copy += Get-ChildItem -Path $PythonHome -Filter "vcruntime*.dll" -ErrorAction SilentlyContinue

Copy-Item "$scripts_dir\python.exe" "$OutputRoot\runtime\python.exe" -Force
if (Test-Path "$scripts_dir\pythonw.exe") {
    Copy-Item "$scripts_dir\pythonw.exe" "$OutputRoot\runtime\pythonw.exe" -Force
}

foreach ($dll in $dlls_to_copy) {
    Copy-Item $dll.FullName "$OutputRoot\runtime" -Force
}

# Copy Python standard library (minimal set)
Write-Host "Copying Python standard library..."
$lib_dir = "$PythonHome\Lib"
if (-not (Test-Path $lib_dir)) {
    $lib_dir = (Split-Path -Parent $PythonHome) + "\Lib"
}
if (Test-Path "$lib_dir\*.py") {
    Copy-Item "$lib_dir\*.py" "$OutputRoot\runtime\Lib" -Force
}
if (Test-Path "$lib_dir\*.zip") {
    Copy-Item "$lib_dir\*.zip" "$OutputRoot\runtime\Lib" -Force -ErrorAction SilentlyContinue
}

# Copy required standard library modules
$stdlib_modules = @(
    "asyncio", "collections", "concurrent", "ctypes",
    "email", "encodings", "importlib", "json",
    "logging", "multiprocessing", "pathlib",
    "re", "sqlite3", "threading",
    "unittest", "urllib", "xml", "uuid"
)
foreach ($folder in $stdlib_modules) {
    $src = "$lib_dir\$folder"
    if (Test-Path $src) {
        Write-Host "  - $folder"
        Copy-Item $src "$OutputRoot\runtime\Lib" -Recurse -Force
    }
}

# Copy DLLs
Write-Host "Copying Windows DLLs..."
$dlls_dir = "$PythonHome\DLLs"
if (Test-Path $dlls_dir) {
    Copy-Item "$dlls_dir\*" "$OutputRoot\runtime\DLLs" -Recurse -Force -ErrorAction SilentlyContinue
}

# Copy TCL (not needed for PyQt6, but kept for compatibility)
if (Test-Path "$PythonHome\tcl") {
    Write-Host "Copying Tcl..."
    Copy-Item "$PythonHome\tcl" "$OutputRoot\runtime" -Recurse -Force -ErrorAction SilentlyContinue
}

# Copy third-party packages (CRUCIAL for standalone deployment)
Write-Host "Copying third-party packages..."
Get-ChildItem $PackageRoot -Force | Where-Object {
    $_.Name -notin @(
        "PyInstaller",
        "pyinstaller-6.22.2.dist-info",
        "pyinstaller_hooks_contrib-2026.7.dist-info",
        "_pyinstaller_hooks_contrib",
        "setuptools",
        "setuptools-*",
        "pip",
        "pip-*"
    ) -and $_.Name -notlike "*egg-info"
} | ForEach-Object {
    Write-Host "  - $($_.Name)"
    Copy-Item -Path $_.FullName -Destination "$OutputRoot\runtime\Lib\site-packages\$($_.Name)" -Recurse -Force
}

# Verify critical packages
Write-Host "Verifying critical packages..."
$critical_packages = @(
    "openvino",
    "model_api",
    "cv2",
    "numpy",
    "PIL",
    "PyQt6"
)
foreach ($pkg in $critical_packages) {
    $pkg_path = "$OutputRoot\runtime\Lib\site-packages\$pkg"
    if (-not (Test-Path "$pkg_path\__init__.py")) {
        throw "CRITICAL: Package not found: $pkg at $pkg_path"
    }
    Write-Host "  OK $pkg"
}

# Copy GUI application files
Write-Host "Copying application files..."
Copy-Item `
    "$GuiRoot\EchoSight_PyQt6.py",
    "$GuiRoot\EchoSight.py",
    "$GuiRoot\README.md" `
    -Destination $OutputRoot -Force

# Copy deployment model
Write-Host "Copying deployment model..."
Copy-Item -Path "$DeploymentSource\*" -Destination "$OutputRoot\deployment\Detection" -Recurse -Force
if (-not (Test-Path "$OutputRoot\deployment\Detection\model\model.xml")) {
    throw "CRITICAL: Model XML not found after copy"
}

# Create metadata files
Write-Host ""
Write-Host "Creating metadata and README..." -ForegroundColor Cyan

$readme_lines = @(
    "EchoSight PyQt6 Portable Distribution",
    "",
    "CONTENTS:",
    "- runtime/: Python 3.9 plus PyQt6 plus OpenVINO plus all dependencies",
    "- deployment/: Geti model deployment",
    "",
    "USAGE:",
    "Double-click Launch_EchoSight_PyQt6.bat",
    "",
    "If PyQt6 fails, try Launch_EchoSight.bat for Tkinter fallback",
    "",
    "SYSTEM REQUIREMENTS:",
    "- Windows 7 SP1 or later",
    "- 4GB RAM minimum (8GB recommended)",
    "- Optional: Intel GPU for acceleration",
    ""
)

$readme_lines | Set-Content "$OutputRoot\README_PORTABLE_PyQt6.txt"

# Create build metadata
$build_info = @{
    BuildDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    PythonVersion = "3.9"
    PyQt6Version = "6.5.0"
    OpenVINOVersion = "2024.5"
    Framework = "PyQt6"
    OutputPath = $OutputRoot
} | ConvertTo-Json

Set-Content "$OutputRoot\BUILD_INFO.json" $build_info -Encoding UTF8

# Final verification
Write-Host ""
Write-Host "=== DEPLOYMENT VERIFICATION ===" -ForegroundColor Green
Write-Host ""

$totalSize = (Get-ChildItem $OutputRoot -Recurse -File | Measure-Object Length -Sum).Sum / 1MB
Write-Host "OK Total package size: $([Math]::Round($totalSize, 1)) MB" -ForegroundColor Green

$checks = @(
    @{ Path = "$OutputRoot\runtime\python39.dll"; Name = "Python runtime" }
    @{ Path = "$OutputRoot\runtime\Lib\site-packages\PyQt6\__init__.py"; Name = "PyQt6 framework" }
    @{ Path = "$OutputRoot\runtime\Lib\site-packages\openvino\__init__.py"; Name = "OpenVINO engine" }
    @{ Path = "$OutputRoot\runtime\Lib\site-packages\cv2\__init__.py"; Name = "OpenCV" }
    @{ Path = "$OutputRoot\runtime\Lib\site-packages\numpy\__init__.py"; Name = "NumPy" }
    @{ Path = "$OutputRoot\runtime\Lib\site-packages\model_api\__init__.py"; Name = "Geti Model API" }
    @{ Path = "$OutputRoot\deployment\Detection\model\model.xml"; Name = "Model deployment" }
)

$all_ok = $true
foreach ($check in $checks) {
    if (Test-Path $check.Path) {
        Write-Host "OK $($check.Name)" -ForegroundColor Green
    } else {
        Write-Host "MISSING: $($check.Name)" -ForegroundColor Red
        $all_ok = $false
    }
}

Write-Host ""
if ($all_ok) {
    Write-Host "=== SUCCESS ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Portable package created at: $OutputRoot"
    Write-Host ""
    Write-Host "To use:"
    Write-Host "  1. Copy portable_pyqt6 folder to any Windows machine"
    Write-Host "  2. Double-click Launch_EchoSight_PyQt6.bat"
    Write-Host "  3. Select deployment model and import images"
    Write-Host ""
} else {
    Write-Host "Deployment verification failed - missing components"
}
