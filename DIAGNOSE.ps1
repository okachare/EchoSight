#!/usr/bin/env powershell
<#
.SYNOPSIS
Diagnose EchoSight setup issues

.DESCRIPTION
Checks Python installation, dependencies, and environment
#>

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EchoSight Diagnostic Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installations
Write-Host "[1] Checking Python installations..." -ForegroundColor Yellow
Write-Host ""

$PythonLocations = @(
    "python",
    "python3",
    "python3.9",
    "C:\Python39\python.exe",
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python39\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe"
)

$Found = $false
foreach ($Path in $PythonLocations) {
    try {
        $Version = & $Path --version 2>&1
        Write-Host "✓ Found: $Path" -ForegroundColor Green
        Write-Host "  Version: $Version" -ForegroundColor Green
        if ($Version -match "3\.9") {
            Write-Host "  Status: COMPATIBLE WITH OPENVINO 2024.5" -ForegroundColor Green
            $Found = $true
        } else {
            Write-Host "  Status: Not Python 3.9 (need 3.9 specifically)" -ForegroundColor Yellow
        }
    } catch {
        # Silently skip not found
    }
}

if (-not $Found) {
    Write-Host ""
    Write-Host "⚠ NO Python 3.9 FOUND!" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""

# Check PATH
Write-Host "[2] Python in PATH..." -ForegroundColor Yellow
$Paths = $env:PATH -split ";"
$PythonInPath = $Paths | Where-Object { $_ -match "Python|python" }
if ($PythonInPath) {
    Write-Host "✓ Python paths found in PATH:" -ForegroundColor Green
    foreach ($p in $PythonInPath) {
        Write-Host "  $p" -ForegroundColor Green
    }
} else {
    Write-Host "✗ No Python paths in PATH" -ForegroundColor Yellow
}

Write-Host ""

# Check pip
Write-Host "[3] Checking pip..." -ForegroundColor Yellow
try {
    $PipVersion = & python -m pip --version 2>&1
    Write-Host "✓ pip found: $PipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip not found or not working" -ForegroundColor Red
}

Write-Host ""

# Check disk space
Write-Host "[4] Checking disk space..." -ForegroundColor Yellow
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Drive = ($Root | Split-Path -Qualifier).TrimEnd(':')
$Volume = Get-Volume -DriveLetter $Drive
$FreeGB = [math]::Round($Volume.SizeRemaining / 1GB, 2)
$TotalGB = [math]::Round($Volume.Size / 1GB, 2)

Write-Host "Drive: $Drive" -ForegroundColor Green
Write-Host "Free space: $FreeGB GB / $TotalGB GB" -ForegroundColor Green

if ($FreeGB -lt 5) {
    Write-Host "⚠ Warning: Less than 5GB free space (need ~3GB for build)" -ForegroundColor Yellow
} else {
    Write-Host "✓ Sufficient disk space" -ForegroundColor Green
}

Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($Found) {
    Write-Host "✓ Python 3.9 is installed and ready" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next: Run .\SETUP_AND_BUILD.ps1" -ForegroundColor Green
} else {
    Write-Host "✗ Python 3.9 is NOT installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUTION:" -ForegroundColor Yellow
    Write-Host "1. Download Python 3.9:" -ForegroundColor White
    Write-Host "   https://www.python.org/downloads/release/python-3913/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Install and IMPORTANT:" -ForegroundColor White
    Write-Host "   ✓ Check: 'Add Python 3.9 to PATH'" -ForegroundColor Green
    Write-Host ""
    Write-Host "3. Restart PowerShell" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Run: .\DIAGNOSE.ps1 (to verify)" -ForegroundColor White
    Write-Host ""
    Write-Host "5. Then run: .\SETUP_AND_BUILD.ps1" -ForegroundColor White
}

Write-Host ""
