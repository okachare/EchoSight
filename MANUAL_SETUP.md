# Quick Manual Setup (Step-by-Step)

## The Problem

You likely **don't have Python 3.9 installed**, which is required for OpenVINO 2024.5.

## The Solution (5 Steps)

### Step 1: Install Python 3.9

1. Go to: https://www.python.org/downloads/release/python-3913/
2. Download: **Windows installer (64-bit)** → `python-3.9.13-amd64.exe`
3. Run the installer
4. **IMPORTANT**: During installation:
   - ☑ Check the box: **"Add Python 3.9 to PATH"**
   - Click Install
   - Wait for completion

5. **Close everything and restart PowerShell** (this is critical!)

---

### Step 2: Verify Python Installation

Open a **NEW PowerShell window** and run:

```powershell
python --version
```

**Expected output**: `Python 3.9.13` (or similar 3.9.x)

If you see an error, Python wasn't added to PATH. **Reinstall** and make sure to check "Add Python 3.9 to PATH".

---

### Step 3: Create the Launcher Script

Copy this exactly into a file named **`Launch_EchoSight.bat`** in your EchoSight folder:

```batch
@echo off
REM EchoSight Launcher
REM Creates virtual environment and runs EchoSight

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Create virtual environment if it doesn't exist
if not exist "!SCRIPT_DIR!.venv" (
    echo Creating virtual environment...
    python -m venv "!SCRIPT_DIR!.venv"
)

REM Activate virtual environment
call "!SCRIPT_DIR!.venv\Scripts\activate.bat"

REM Install/upgrade dependencies silently
python -m pip install -q --upgrade pip setuptools wheel 2>nul
python -m pip install -q -e "!SCRIPT_DIR!" 2>nul

REM Run EchoSight
python -c "from echosight.EchoSight import main; main()" %*

REM Deactivate on exit
deactivate
pause
```

**How to create the file:**
1. Open Notepad
2. Paste the code above
3. File → Save As
4. Name: `Launch_EchoSight.bat`
5. Save in your **EchoSight folder** (where you see setup.py)
6. Important: Choose **All Files** type, NOT `.txt`

---

### Step 4: Test the Launcher

1. In your EchoSight folder, double-click **`Launch_EchoSight.bat`**
2. You should see a command window open with messages like:
   ```
   Creating virtual environment...
   Collecting pip...
   Installing collected packages...
   ```
3. Wait for it to finish and the GUI should appear

**First run takes 1-2 minutes.** Subsequent runs are faster.

---

### Step 5: Run Normally

After the first run:
- Double-click `Launch_EchoSight.bat` to run EchoSight anytime
- A command window will open, then the GUI appears
- Close the GUI to exit (command window closes automatically)

---

## Troubleshooting

### "Python 3.9 not found" or "python command not found"

**Solution:**
1. **Uninstall** current Python
2. **Restart computer**
3. Download Python 3.9.13 installer again
4. Run installer
5. **CRITICAL**: Check ☑ "Add Python 3.9 to PATH"
6. Restart PowerShell
7. Verify: `python --version`

---

### Launcher doesn't work or closes immediately

1. Try running from Command Prompt instead:
   ```cmd
   cd C:\Path\To\EchoSight
   Launch_EchoSight.bat
   ```
2. Look at error messages (don't let window close)
3. Take a screenshot of any errors

---

### "ModuleNotFoundError" when starting

Run this in PowerShell to see what's missing:
```powershell
cd C:\Path\To\EchoSight
.\.venv\Scripts\activate.ps1
python -c "import openvino; import cv2; import PIL; print('OK')"
```

If you see `OK`, everything is fine.

---

### Very slow first run (2-3 minutes)

**This is normal!** The first run:
- Creates virtual environment
- Installs dependencies
- Initializes OpenVINO

Subsequent runs are much faster (~30 seconds).

---

## Folder Structure After Setup

```
EchoSight/
├── Launch_EchoSight.bat          ← Double-click this!
├── setup.py
├── .venv/                         ← Virtual environment (auto-created)
├── src/
│   └── echosight/
│       └── EchoSight.py
├── build/
├── ... (other files)
```

---

## Quick Start

1. Double-click `Launch_EchoSight.bat`
2. GUI window opens
3. Click "Select Model Folder"
4. Navigate to a Geti model export folder
5. Click "Load Model"
6. Click "Add Images"
7. Select PNG/JPG/TIFF files
8. Click "Run All"

---

## If You Still Have Issues

Run the diagnostic script:

```powershell
cd C:\Path\To\EchoSight
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\DIAGNOSE.ps1
```

Copy the output and share it - this will tell us exactly what's wrong.

---

## Alternative: Pre-Built Binaries

If you want the pre-built executable (no Python install needed):

1. Go to: https://github.com/okachare/EchoSight/releases
2. Download: `EchoSight-portable.zip` (if available)
3. Extract anywhere
4. Double-click `Launch_EchoSight.bat`

This contains everything bundled (Python included!), no installation needed.
