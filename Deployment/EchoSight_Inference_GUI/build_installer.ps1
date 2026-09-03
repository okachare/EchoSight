param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EchoSight Portable Installer Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify Python
Write-Host "[1/5] Verifying Python environment..." -ForegroundColor Yellow
$PythonVer = & $Python --version 2>&1
Write-Host "      Using: $PythonVer" -ForegroundColor Green

# Step 2: Install dependencies
Write-Host "[2/5] Installing dependencies..." -ForegroundColor Yellow
& $Python -m pip install --upgrade pip setuptools wheel
& $Python -m pip install -r .\requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Failed to install requirements" }
Write-Host "      Dependencies installed" -ForegroundColor Green

# Step 3: Install PyInstaller
Write-Host "[3/5] Installing PyInstaller..." -ForegroundColor Yellow
& $Python -m pip install pyinstaller
if ($LASTEXITCODE -ne 0) { throw "Failed to install PyInstaller" }
Write-Host "      PyInstaller installed" -ForegroundColor Green

# Step 4: Verify EchoSight.py syntax
Write-Host "[4/5] Verifying EchoSight.py syntax..." -ForegroundColor Yellow
& $Python -m py_compile .\EchoSight.py
if ($LASTEXITCODE -ne 0) { throw "EchoSight.py has syntax errors" }
Write-Host "      Syntax verified" -ForegroundColor Green

# Step 5: Build executable
Write-Host "[5/5] Building standalone EchoSight executable..." -ForegroundColor Yellow
& $Python -m PyInstaller --noconfirm --clean --windowed --onedir .\EchoSight.spec
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed" }
Write-Host "      Build complete" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Executable location: $Root\dist\EchoSight\EchoSight.exe" -ForegroundColor Green
Write-Host ""
Write-Host "Installation instructions:" -ForegroundColor Yellow
Write-Host "  1. Copy the entire 'dist\EchoSight' folder to your target location" -ForegroundColor White
Write-Host "  2. Double-click EchoSight.exe to launch" -ForegroundColor White
Write-Host "  3. Use 'Load Model' button to select your Geti deployment folder" -ForegroundColor White
Write-Host ""
Write-Host "All required libraries and dependencies are bundled in the executable." -ForegroundColor Green
Write-Host "No additional installation required on target system." -ForegroundColor Green

