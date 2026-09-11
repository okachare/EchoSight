# EchoSight Setup Guide

## One-Command Setup

That's it. Just run this:

```powershell
cd C:\Path\To\EchoSight
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\SETUP.ps1
```

The script does everything:
- ✅ Checks Python 3.9
- ✅ Creates virtual environment
- ✅ Installs dependencies
- ✅ Creates `Launch_EchoSight.bat` launcher

## Then Run

Double-click **`Launch_EchoSight.bat`** in the EchoSight folder.

That's it! 🎉

---

## Requirements

- **Windows 10+**
- **Python 3.9** — [Download here](https://www.python.org/downloads/release/python-3913/)
  - ⚠️ During install: Check "Add Python 3.9 to PATH"
  - Not 3.10, not 3.11 — must be 3.9
- **4 GB RAM** minimum
- **3 GB disk space**

---

## If Setup Fails

Run the diagnostic tool:

```powershell
.\DIAGNOSE.ps1
```

For manual step-by-step setup, see **MANUAL_SETUP.md**.

---

## What Gets Created

```
EchoSight/
├── SETUP.ps1                    ← Run this once
├── Launch_EchoSight.bat         ← Run this to start EchoSight
├── .venv/                       ← Virtual environment (auto-created)
└── ... (rest of files)
```

---

## How to Use EchoSight

1. Double-click `Launch_EchoSight.bat`
2. Click "Select Model Folder"
3. Choose a Geti model deployment folder
4. Click "Load Model"
5. Click "Add Images"
6. Click "Run All" or "Run Current"
7. Review results

See **USAGE.md** for full documentation.

---

## Pre-Built Binaries (No Python Needed)

If you don't want to install Python, pre-built portable packages are available at:

https://github.com/okachare/EchoSight/releases

Download `EchoSight-portable.zip`, extract, and double-click `Launch_EchoSight.bat`.
