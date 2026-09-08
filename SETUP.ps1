#!/usr/bin/env powershell
<#
.SYNOPSIS
EchoSight Setup - Single Foolproof Installer

.DESCRIPTION
One-command setup that handles everything:
  1. Checks Python 3.9 installation
  2. Creates virtual environment
  3. Installs all dependencies
  4. Creates Launch_EchoSight.bat launcher
  
That's it. Then double-click the launcher to run.

.EXAMPLE
.\SETUP.ps1
#>

param()

$ErrorActionPreference = "Continue"
$WarningPreference = "SilentlyContinue"

# Colors
$ColorHeader = "Cyan"
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "White"

function Write-Title {
    param([string]$Text)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor $ColorHeader
    Write-Host $Text -ForegroundColor $ColorHeader
    Write-Host "========================================" -ForegroundColor $ColorHeader
    Write-Host ""
}

function Write-OK {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor $ColorSuccess
}

function Write-Error-Bold {
    param([string]$Text)
    Write-Host "✗ $Text" -ForegroundColor $ColorError
}

function Write-Warn {
    param([string]$Text)
    Write-Host "⚠ $Text" -ForegroundColor $ColorWarning
}

function Write-Info {
    param([string]$Text)
    Write-Host "  $Text" -ForegroundColor $ColorInfo
}

# ============================================================
# START
# ============================================================
Write-Title "EchoSight Setup"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

# ============================================================
# STEP 1: Check Python 3.9
# ============================================================
Write-Host "[1/4] Checking Python 3.9..." -ForegroundColor $ColorWarning

$PythonFound = $false
$Python = $null

try {
    $Version = & python --version 2>&1
    if ($Version -match "3\.9") {
        $Python = "python"
        $PythonFound = $true
        Write-OK "Found Python: $Version"
    } else {
        Write-Warn "Python found but not 3.9: $Version"
    }
} catch {
    Write-Warn "Python not in PATH"
}

# If not found, try common locations
if (-not $PythonFound) {
    $Paths = @(
        "C:\Python39\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe"
    )
    
    foreach ($Path in $Paths) {
        if (Test-Path $Path) {
            try {
                $Version = & $Path --version 2>&1
                if ($Version -match "3\.9") {
                    $Python = $Path
                    $PythonFound = $true
                    Write-OK "Found Python at: $Path"
                    break
                }
            } catch {}
        }
    }
}

# If still not found, error
if (-not $PythonFound) {
    Write-Host ""
    Write-Error-Bold "Python 3.9 NOT FOUND"
    Write-Host ""
    Write-Host "REQUIRED: Python 3.9 (NOT 3.10 or 3.11+)" -ForegroundColor $ColorWarning
    Write-Host ""
    Write-Host "SOLUTION:" -ForegroundColor $ColorWarning
    Write-Host "1. Download Python 3.9:" -ForegroundColor White
    Write-Host "   https://www.python.org/downloads/release/python-3913/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Run installer and CHECK:" -ForegroundColor White
    Write-Host "   ☑ 'Add Python 3.9 to PATH'" -ForegroundColor $ColorSuccess
    Write-Host ""
    Write-Host "3. Restart PowerShell/CMD" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Run this script again:" -ForegroundColor White
    Write-Host "   .\SETUP.ps1" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# ============================================================
# STEP 2: Create Virtual Environment
# ============================================================
Write-Host "[2/4] Setting up environment..." -ForegroundColor $ColorWarning

$VenvPath = "$Root\.venv"

if (Test-Path $VenvPath) {
    Write-Info "Virtual environment already exists"
} else {
    Write-Info "Creating virtual environment..."
    & $Python -m venv $VenvPath 2>&1 | Out-Null
    
    if (-not (Test-Path $VenvPath)) {
        Write-Error-Bold "Failed to create virtual environment"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-OK "Environment ready"

# ============================================================
# STEP 3: Install Dependencies
# ============================================================
Write-Host "[3/4] Installing dependencies..." -ForegroundColor $ColorWarning

$VenvActivate = "$VenvPath\Scripts\activate.ps1"

# Activate venv
Write-Info "Activating environment..."
& $VenvActivate

Write-Info "Installing pip, setuptools, wheel..."
python -m pip install -q --upgrade pip setuptools wheel 2>$null

Write-Info "Installing EchoSight and dependencies..."
python -m pip install -q -e $Root 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Warn "Some dependencies may have failed (continuing anyway)"
}

Write-OK "Dependencies installed"

# ============================================================
# STEP 4: Create Launcher
# ============================================================
Write-Host "[4/4] Creating launcher..." -ForegroundColor $ColorWarning

$LauncherContent = @"
@echo off
REM EchoSight Launcher
REM Do not edit this file - it was generated by SETUP.ps1

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"

REM Activate virtual environment
call "!SCRIPT_DIR!.venv\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Run EchoSight
python -c "from echosight.EchoSight import main; main()" %*
set EXIT_CODE=%errorlevel%

REM Deactivate on exit
deactivate 2>nul
exit /b %EXIT_CODE%
"@

$LauncherPath = "$Root\Launch_EchoSight.bat"
Set-Content -Path $LauncherPath -Value $LauncherContent -Encoding ASCII -Force
Write-OK "Launcher created: Launch_EchoSight.bat"

# Deactivate venv
deactivate 2>$null

# ============================================================
# COMPLETE
# ============================================================
Write-Title "Setup Complete!"

Write-Host "NEXT STEPS:" -ForegroundColor $ColorSuccess
Write-Host ""
Write-Host "1. Double-click: Launch_EchoSight.bat" -ForegroundColor White
Write-Host "   Location: $Root" -ForegroundColor Gray
Write-Host ""
Write-Host "2. First run takes 1-2 minutes (one-time only)" -ForegroundColor White
Write-Host ""
Write-Host "3. The EchoSight GUI will appear" -ForegroundColor White
Write-Host ""
Write-Host "4. Load a model folder and run inference!" -ForegroundColor White
Write-Host ""

Write-Host "FILES CREATED:" -ForegroundColor $ColorSuccess
Write-Host "  ✓ .venv/                  (virtual environment)" -ForegroundColor White
Write-Host "  ✓ Launch_EchoSight.bat    (launcher)" -ForegroundColor White
Write-Host ""

Write-Host "TROUBLESHOOTING:" -ForegroundColor $ColorWarning
Write-Host "  If something goes wrong, run:" -ForegroundColor White
Write-Host "    .\DIAGNOSE.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "  For detailed help, see:" -ForegroundColor White
Write-Host "    MANUAL_SETUP.md" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
