#!/usr/bin/env powershell
<#
.SYNOPSIS
Simple EchoSight Launcher Creator

.DESCRIPTION
Creates a working Launch_EchoSight.bat file without Python installation checks.
This is the easiest way to get started.
#>

$ErrorActionPreference = "Continue"
$WarningPreference = "SilentlyContinue"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EchoSight Setup (Simple)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

# Create the batch launcher file
$LauncherContent = @'
@echo off
REM EchoSight Launcher - Creates virtual environment and runs EchoSight
REM This file can be run from anywhere and will work correctly

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python 3.9 is not installed or not in PATH
    echo.
    echo Please install Python 3.9:
    echo   https://www.python.org/downloads/release/python-3913/
    echo.
    echo During installation, IMPORTANT:
    echo   CHECK: "Add Python 3.9 to PATH"
    echo.
    echo After installing, close this window and try again.
    echo.
    pause
    exit /b 1
)

REM Check Python version
python -c "import sys; sys.exit(0 if sys.version_info >= (3,9) and sys.version_info < (3,11) else 1)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Python version might not be 3.9
    echo.
    python --version
    echo.
    echo OpenVINO 2024.5 works best with Python 3.9
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "!CONTINUE!"=="y" exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "!SCRIPT_DIR!.venv" (
    echo Creating virtual environment...
    python -m venv "!SCRIPT_DIR!.venv"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call "!SCRIPT_DIR!.venv\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/upgrade pip and setuptools
echo Installing build tools...
python -m pip install -q --upgrade pip setuptools wheel 2>nul

REM Install project dependencies
echo Installing dependencies (this may take a minute)...
python -m pip install -q -e "!SCRIPT_DIR!" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies failed to install
    echo Attempting to continue...
    echo.
)

REM Run EchoSight
echo.
echo Starting EchoSight...
echo.
python -c "from echosight.EchoSight import main; main()" %*
set EXIT_CODE=%errorlevel%

REM Deactivate on exit
deactivate 2>nul

if %EXIT_CODE% neq 0 (
    echo.
    echo ERROR: EchoSight failed to start
    echo Exit code: %EXIT_CODE%
    echo.
    pause
    exit /b %EXIT_CODE%
)

exit /b 0
'@

# Write the launcher file
$LauncherPath = "$Root\Launch_EchoSight.bat"
Write-Host "[1/2] Creating launcher: Launch_EchoSight.bat" -ForegroundColor Yellow

try {
    Set-Content -Path $LauncherPath -Value $LauncherContent -Encoding ASCII -Force
    Write-Host "✓ Launcher created successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ FAILED to create launcher!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running PowerShell as Administrator" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Create desktop shortcut (optional)
Write-Host "[2/2] Creating shortcut..." -ForegroundColor Yellow

try {
    $Shell = New-Object -ComObject WScript.Shell
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    $ShortcutPath = "$DesktopPath\EchoSight.lnk"
    
    $Shortcut = $Shell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $LauncherPath
    $Shortcut.WorkingDirectory = $Root
    $Shortcut.IconLocation = "$Root\src\echosight\icon.ico"
    $Shortcut.Description = "EchoSight - Model Inference GUI"
    $Shortcut.Save()
    
    Write-Host "✓ Desktop shortcut created" -ForegroundColor Green
} catch {
    Write-Host "✓ Launcher created (shortcut optional, skipped)" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Double-click: Launch_EchoSight.bat" -ForegroundColor White
Write-Host "   (in folder: $Root)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. First run will take 1-2 minutes (installing dependencies)" -ForegroundColor White
Write-Host ""
Write-Host "3. The GUI window will appear" -ForegroundColor White
Write-Host ""
Write-Host "4. Load a model folder and run inference!" -ForegroundColor White
Write-Host ""

Write-Host "FILES CREATED:" -ForegroundColor Yellow
Write-Host "  ✓ Launch_EchoSight.bat (in EchoSight folder)" -ForegroundColor White
if (Test-Path "$DesktopPath\EchoSight.lnk") {
    Write-Host "  ✓ EchoSight.lnk (on Desktop)" -ForegroundColor White
}
Write-Host ""

Write-Host "TROUBLESHOOTING:" -ForegroundColor Yellow
Write-Host "  If launcher fails on first run:" -ForegroundColor White
Write-Host "  → Run: .\DIAGNOSE.ps1" -ForegroundColor Gray
Write-Host "  → Check: MANUAL_SETUP.md" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"
