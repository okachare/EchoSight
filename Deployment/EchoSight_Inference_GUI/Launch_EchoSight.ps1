#!/usr/bin/env powershell
<#
.SYNOPSIS
    EchoSight PyQt6/Tkinter Launcher (works with network paths)
.DESCRIPTION
    Smart launcher that:
    - Works with UNC network paths
    - Tries PyQt6 version first
    - Falls back to Tkinter if PyQt6 unavailable
    - Activates .venv automatically
#>

param(
    [switch]$TkinterOnly = $false,
    [switch]$PyQt6Only = $false
)

$ErrorActionPreference = "Stop"

# Get the directory this script is in
$GuiDir = $PSScriptRoot
if (-not $GuiDir) {
    $GuiDir = Split-Path -Parent $MyInvocation.MyCommandPath
}
if (-not $GuiDir) {
    $GuiDir = Get-Location
}

$RootDir = Split-Path -Parent (Split-Path -Parent $GuiDir)
$VenvPath = Join-Path $RootDir ".venv"

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "EchoSight Launcher" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "GUI Dir: $GuiDir" -ForegroundColor Gray
Write-Host "Root Dir: $RootDir" -ForegroundColor Gray
Write-Host "Venv: $VenvPath" -ForegroundColor Gray
Write-Host ""

# Activate venv
if (Test-Path (Join-Path $VenvPath "Scripts\Activate.ps1")) {
    Write-Host "Activating .venv..." -ForegroundColor Green
    & (Join-Path $VenvPath "Scripts\Activate.ps1")
    $PythonExe = Join-Path $VenvPath "Scripts\python.exe"
} else {
    Write-Host "WARNING: .venv not found, using system Python" -ForegroundColor Yellow
    $PythonExe = "python.exe"
}

Write-Host "Python: $PythonExe" -ForegroundColor Green
Write-Host ""

# Try PyQt6 unless Tkinter-only is specified
if (-not $TkinterOnly) {
    Write-Host "Attempting to start PyQt6 version..." -ForegroundColor Cyan
    
    $PyQt6App = Join-Path $GuiDir "EchoSight_PyQt6.py"
    
    if (Test-Path $PyQt6App) {
        try {
            Write-Host "Launching: $PyQt6App" -ForegroundColor Green
            Write-Host ""
            & $PythonExe $PyQt6App
            
            # If it exits successfully, we're done
            exit $LASTEXITCODE
        } catch {
            Write-Host "ERROR: PyQt6 failed: $_" -ForegroundColor Red
            Write-Host ""
            Write-Host "Attempting Tkinter fallback..." -ForegroundColor Yellow
        }
    }
}

# Fall back to Tkinter
Write-Host "Attempting to start Tkinter version..." -ForegroundColor Cyan

$TkinterApp = Join-Path $GuiDir "EchoSight.py"

if (Test-Path $TkinterApp) {
    try {
        Write-Host "Launching: $TkinterApp" -ForegroundColor Green
        Write-Host ""
        & $PythonExe $TkinterApp
        
        exit $LASTEXITCODE
    } catch {
        Write-Host "ERROR: Tkinter version also failed: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Troubleshooting:" -ForegroundColor Yellow
        Write-Host "1. Verify Python is installed: python --version"
        Write-Host "2. Verify dependencies: pip list | findstr -i pyqt"
        Write-Host "3. Install missing: pip install -r requirements.txt"
        exit 1
    }
} else {
    Write-Host "ERROR: EchoSight.py not found at $TkinterApp" -ForegroundColor Red
    exit 1
}
