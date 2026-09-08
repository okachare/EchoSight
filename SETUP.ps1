#!/usr/bin/env powershell
# EchoSight Setup - Clean, Simple, Foolproof

param()

$ErrorActionPreference = "Continue"

function Exit-Pause {
    param([int]$Code = 0)
    Write-Host ""
    Read-Host "Press Enter to close"
    exit $Code
}

trap {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Exit-Pause 1
}

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EchoSight Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "[1/4] Checking Python 3.9..." -ForegroundColor Yellow

$Python = $null

try {
    $Ver = & python --version 2>&1
    if ($Ver -match "3\.9") {
        $Python = "python"
        Write-Host "  Found: $Ver" -ForegroundColor Green
    }
} catch {}

if (-not $Python) {
    $Path = "C:\Python39\python.exe"
    if (Test-Path $Path) {
        $Ver = & $Path --version 2>&1
        if ($Ver -match "3\.9") {
            $Python = $Path
            Write-Host "  Found: $Path" -ForegroundColor Green
        }
    }
}

if (-not $Python) {
    $Path = "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe"
    if (Test-Path $Path) {
        $Ver = & $Path --version 2>&1
        if ($Ver -match "3\.9") {
            $Python = $Path
            Write-Host "  Found: $Path" -ForegroundColor Green
        }
    }
}

if (-not $Python) {
    Write-Host ""
    Write-Host "ERROR: Python 3.9 not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Download Python 3.9.13:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/release/python-3913/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "During install: CHECK 'Add Python 3.9 to PATH'" -ForegroundColor Yellow
    Write-Host ""
    Exit-Pause 1
}

Write-Host ""

# Step 2: Virtual environment
Write-Host "[2/4] Setting up environment..." -ForegroundColor Yellow

$Venv = "$Root\.venv"

if (-not (Test-Path $Venv)) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Gray
    & $Python -m venv $Venv 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create venv" -ForegroundColor Red
        Exit-Pause 1
    }
}

Write-Host "  Environment ready" -ForegroundColor Green
Write-Host ""

# Step 3: Install dependencies
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow

$Activate = "$Venv\Scripts\activate.ps1"
& $Activate

Write-Host "  Installing packages..." -ForegroundColor Gray
python -m pip install -q --upgrade pip 2>$null
python -m pip install -q -e $Root 2>$null

Write-Host "  Dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 4: Create launcher
Write-Host "[4/4] Creating launcher..." -ForegroundColor Yellow

$Bat = "$Root\Launch_EchoSight.bat"

$Launcher = "@echo off`nsetlocal enabledelayedexpansion`nset `"SCRIPT_DIR=%~dp0`"`ncall `"!SCRIPT_DIR!.venv\Scripts\activate.bat`"`nif errorlevel 1 (`n    echo ERROR: Failed to activate`n    pause`n    exit /b 1`n)`npython -c `"from echosight.EchoSight import main; main()`" %*`ndeactivate 2>nul"

$Launcher | Set-Content $Bat -Encoding ASCII

if (-not (Test-Path $Bat)) {
    Write-Host "ERROR: Failed to create launcher" -ForegroundColor Red
    Exit-Pause 1
}

Write-Host "  Launcher created" -ForegroundColor Green
Write-Host ""

deactivate 2>$null

# Done
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next:" -ForegroundColor Green
Write-Host "1. Double-click: Launch_EchoSight.bat" -ForegroundColor White
Write-Host "2. Wait for GUI (first run: 1-2 min)" -ForegroundColor White
Write-Host ""

Exit-Pause 0
