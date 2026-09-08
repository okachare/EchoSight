#!/usr/bin/env powershell
<#
.SYNOPSIS
EchoSight Complete Setup and Build Installer

.DESCRIPTION
This master script automates the entire process:
  1. Verify Python 3.9 installation
  2. Create virtual environment
  3. Install dependencies and build tools
  4. Build standalone executable with PyInstaller
  5. Create portable zip archive
  6. Create Launch_EchoSight.bat launcher

.PARAMETER PythonPath
Full path to Python 3.9 executable (default: auto-detect)

.PARAMETER BuildPortable
Build portable archive (default: $true)

.EXAMPLE
.\SETUP_AND_BUILD.ps1
.\SETUP_AND_BUILD.ps1 -PythonPath "C:\Python39\python.exe"

.NOTES
Requirements:
  - Windows 10 or later
  - Python 3.9 (NOT 3.10+)
  - 4 GB RAM minimum
  - 3 GB disk space for build
#>

param(
    [string]$PythonPath = "",
    [bool]$BuildPortable = $true,
    [bool]$BuildInstaller = $false
)

$ErrorActionPreference = "Stop"
$WarningPreference = "Continue"

# ============================================
# COLOR DEFINITIONS
# ============================================
$ColorHeader = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorInfo = "White"

# ============================================
# UTILITY FUNCTIONS
# ============================================
function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor $ColorHeader
    Write-Host $Text -ForegroundColor $ColorHeader
    Write-Host "========================================" -ForegroundColor $ColorHeader
    Write-Host ""
}

function Write-Step {
    param(
        [string]$Step,
        [string]$Description
    )
    Write-Host "$Step $Description" -ForegroundColor $ColorWarning
}

function Write-Success {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor $ColorSuccess
}

function Write-Info {
    param([string]$Text)
    Write-Host "  $Text" -ForegroundColor $ColorInfo
}

# ============================================
# MAIN PROCESS
# ============================================
Write-Header "EchoSight Setup and Build"

# Detect Python 3.9
Write-Step "[1/6]" "Detecting Python 3.9..."

if ($PythonPath -and (Test-Path $PythonPath)) {
    $Python = $PythonPath
    Write-Success "Using provided Python: $Python"
} else {
    # Try common Python 3.9 locations
    $CommonPaths = @(
        "C:\Python39\python.exe",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python39\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe"
    )
    
    $Found = $false
    foreach ($Path in $CommonPaths) {
        if (Test-Path $Path) {
            $Python = $Path
            $Found = $true
            Write-Success "Found Python at: $Python"
            break
        }
    }
    
    if (-not $Found) {
        # Try 'python' from PATH
        try {
            $PythonVer = & python --version 2>&1
            if ($PythonVer -match "3\.9") {
                $Python = "python"
                Write-Success "Found Python in PATH: $PythonVer"
                $Found = $true
            }
        } catch {
            $Found = $false
        }
    }
    
    if (-not $Found) {
        Write-Host ""
        Write-Host "ERROR: Python 3.9 not found!" -ForegroundColor $ColorError
        Write-Host ""
        Write-Host "Please install Python 3.9 from: https://www.python.org/downloads/" -ForegroundColor $ColorWarning
        Write-Host "Download: Windows Installer (64-bit) for Python 3.9.x" -ForegroundColor $ColorWarning
        Write-Host ""
        Write-Host "During installation, CHECK: 'Add Python 3.9 to PATH'" -ForegroundColor $ColorWarning
        Write-Host ""
        exit 1
    }
}

# Verify Python version
Write-Info "Verifying Python version..."
$PythonVer = & $Python --version 2>&1
Write-Info "Version: $PythonVer"

if (-not ($PythonVer -match "3\.9")) {
    Write-Host ""
    Write-Host "WARNING: Python 3.9 is required!" -ForegroundColor $ColorWarning
    Write-Host "Current version: $PythonVer" -ForegroundColor $ColorWarning
    Write-Host "OpenVINO 2024.5 requires Python 3.9 (NOT 3.10 or 3.11+)" -ForegroundColor $ColorWarning
    Write-Host ""
    $Continue = Read-Host "Continue anyway? (y/n)"
    if ($Continue -ne "y") { exit 1 }
}

# ============================================
# SETUP ENVIRONMENT
# ============================================
Write-Step "[2/6]" "Setting up environment..."

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
Write-Info "Working directory: $Root"

# Create virtual environment
$VenvPath = "$Root\.venv"
if (Test-Path $VenvPath) {
    Write-Info "Virtual environment already exists"
} else {
    Write-Info "Creating virtual environment..."
    & $Python -m venv $VenvPath
    Write-Success "Virtual environment created"
}

# Activate virtual environment
$VenvActivate = "$VenvPath\Scripts\Activate.ps1"
Write-Info "Activating virtual environment..."
& $VenvActivate

Write-Success "Environment ready"

# ============================================
# INSTALL DEPENDENCIES
# ============================================
Write-Step "[3/6]" "Installing dependencies..."

Write-Info "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel -q
Write-Success "Build tools upgraded"

Write-Info "Installing project dependencies..."
python -m pip install -e . -q
Write-Success "Project dependencies installed"

Write-Info "Installing PyInstaller..."
python -m pip install pyinstaller -q
Write-Success "PyInstaller installed"

# ============================================
# BUILD EXECUTABLE
# ============================================
Write-Step "[4/6]" "Building standalone executable..."

# Change to build directory
Set-Location "$Root\build"
$SpecFile = "$Root\build\EchoSight.spec"

Write-Info "Running PyInstaller with: $SpecFile"
python -m PyInstaller "$SpecFile" --noconfirm --clean

if (-not (Test-Path "$Root\dist\EchoSight\EchoSight.exe")) {
    Write-Host ""
    Write-Host "ERROR: Build failed - EchoSight.exe not created!" -ForegroundColor $ColorError
    exit 1
}

Write-Success "Executable created: dist\EchoSight\EchoSight.exe"

# ============================================
# CREATE LAUNCHER
# ============================================
Write-Step "[5/6]" "Creating launcher script..."

$LauncherContent = @'
@echo off
REM EchoSight Launcher
REM Runs EchoSight.exe from the same directory

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Run EchoSight.exe
if exist "!SCRIPT_DIR!dist\EchoSight\EchoSight.exe" (
    start "" "!SCRIPT_DIR!dist\EchoSight\EchoSight.exe"
) else (
    echo Error: EchoSight.exe not found at !SCRIPT_DIR!dist\EchoSight\
    echo Please run SETUP_AND_BUILD.ps1 first to build the executable.
    pause
    exit /b 1
)
'@

$LauncherPath = "$Root\Launch_EchoSight.bat"
Set-Content -Path $LauncherPath -Value $LauncherContent -Encoding ASCII
Write-Success "Launcher created: Launch_EchoSight.bat"

# ============================================
# CREATE PORTABLE ZIP
# ============================================
if ($BuildPortable) {
    Write-Step "[6/6]" "Creating portable archive..."
    
    $PortableDir = "$Root\EchoSight-Portable"
    $ZipFile = "$Root\dist\EchoSight-portable.zip"
    
    # Clean old portable
    if (Test-Path $PortableDir) {
        Remove-Item $PortableDir -Recurse -Force
    }
    if (Test-Path $ZipFile) {
        Remove-Item $ZipFile -Force
    }
    
    # Create portable structure
    New-Item $PortableDir -ItemType Directory -Force | Out-Null
    Copy-Item "$Root\dist\EchoSight" "$PortableDir\EchoSight" -Recurse
    Copy-Item "$Root\Launch_EchoSight.bat" "$PortableDir\" -Force
    Copy-Item "$Root\README.md" "$PortableDir\" -Force
    
    Write-Info "Compressing archive..."
    Compress-Archive -Path "$PortableDir\*" -DestinationPath $ZipFile -Force
    
    if (Test-Path $ZipFile) {
        $ZipSize = [math]::Round((Get-Item $ZipFile).Length / 1MB, 2)
        Write-Success "Portable archive created: $ZipFile ($ZipSize MB)"
    }
} else {
    Write-Info "Skipping portable archive (use -BuildPortable \$true to create)"
}

# ============================================
# COMPLETION
# ============================================
Write-Header "Build Complete!"

Write-Host ""
Write-Host "QUICK START:" -ForegroundColor $ColorSuccess
Write-Host ""
Write-Host "  Option 1 - Run directly:"
Write-Host "    Double-click: Launch_EchoSight.bat" -ForegroundColor $ColorInfo
Write-Host ""
Write-Host "  Option 2 - Use portable archive:"
Write-Host "    Extract: EchoSight-portable.zip" -ForegroundColor $ColorInfo
Write-Host "    Run: Launch_EchoSight.bat" -ForegroundColor $ColorInfo
Write-Host ""
Write-Host "BUILD ARTIFACTS:" -ForegroundColor $ColorSuccess
Write-Host ""
Write-Host "  Executable:  $Root\dist\EchoSight\EchoSight.exe" -ForegroundColor $ColorInfo
Write-Host "  Launcher:    $Root\Launch_EchoSight.bat" -ForegroundColor $ColorInfo

if (Test-Path "$Root\dist\EchoSight-portable.zip") {
    Write-Host "  Archive:     $Root\dist\EchoSight-portable.zip" -ForegroundColor $ColorInfo
}

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor $ColorSuccess
Write-Host ""
Write-Host "  1. Test by running Launch_EchoSight.bat" -ForegroundColor $ColorInfo
Write-Host "  2. Open a model folder (detection/segmentation/anomaly)" -ForegroundColor $ColorInfo
Write-Host "  3. Load images and run inference" -ForegroundColor $ColorInfo
Write-Host ""

# Deactivate virtual environment
deactivate 2>$null

Write-Host "Done!" -ForegroundColor $ColorSuccess
Write-Host ""
