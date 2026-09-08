# Build Instructions for EchoSight

## Quick Start (Recommended)

### Windows (5 minutes)

1. **Open PowerShell** (press `Win+R`, type `powershell`, hit Enter)

2. **Navigate to EchoSight folder**:
   ```powershell
   cd C:\Path\To\EchoSight
   ```

3. **Run the setup script**:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   .\SETUP_AND_BUILD.ps1
   ```

4. **Wait for completion** (~3-5 minutes depending on internet speed)

5. **Done!** The script creates:
   - ✅ `Launch_EchoSight.bat` - Double-click to run
   - ✅ `dist/EchoSight/EchoSight.exe` - Standalone executable
   - ✅ `dist/EchoSight-portable.zip` - Portable archive for sharing

---

## What You'll Get

### After Running SETUP_AND_BUILD.ps1

| File/Folder | Purpose | Size |
|---|---|---|
| `Launch_EchoSight.bat` | Quick launcher (double-click to run) | <1 KB |
| `dist/EchoSight/` | All dependencies bundled | ~600-800 MB |
| `dist/EchoSight.exe` | Standalone executable | ~250 MB |
| `dist/EchoSight-portable.zip` | Portable archive (share via USB/email) | ~150-200 MB |

---

## How to Run

### Option 1: Double-Click Launcher (Easiest)
```
EchoSight folder → double-click Launch_EchoSight.bat
```

### Option 2: Run Directly
```
EchoSight folder → dist → EchoSight → double-click EchoSight.exe
```

### Option 3: Portable Archive
```
1. Extract EchoSight-portable.zip anywhere
2. Double-click Launch_EchoSight.bat
```

---

## Requirements

- **Windows 10 or later**
- **Python 3.9** (must be 3.9, NOT 3.10 or 3.11)
  - Download: https://www.python.org/downloads/release/python-3913/
  - During install: ✓ "Add Python 3.9 to PATH"
- **4 GB RAM** minimum
- **3 GB disk space** for build

---

## Troubleshooting

### "Python 3.9 not found"
- Install Python 3.9: https://www.python.org/downloads/release/python-3913/
- Make sure to check "Add Python 3.9 to PATH" during installation
- Restart PowerShell after installing Python

### "Permission denied" or script won't run
- Run PowerShell as Administrator
- Run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
- Then re-run: `.\SETUP_AND_BUILD.ps1`

### "OpenVINO import failed" on launch
- This is a Python 3.10+ issue
- Make sure you have Python 3.9 installed
- The script will warn you if the wrong version is detected

### EchoSight crashes immediately
- Check you're using Python 3.9
- Try running from command prompt instead: `cd dist\EchoSight && EchoSight.exe`
- Check console output for error messages

### Very slow first launch
- First run can be slow (~30 seconds)
- Subsequent launches are faster
- This is normal for OpenVINO initialization

---

## Command-Line Options

```powershell
# Use specific Python installation
.\SETUP_AND_BUILD.ps1 -PythonPath "C:\Python39\python.exe"

# Build without portable zip
.\SETUP_AND_BUILD.ps1 -BuildPortable $false

# Build installer (requires NSIS - advanced)
.\SETUP_AND_BUILD.ps1 -BuildInstaller $true
```

---

## File Structure After Build

```
EchoSight/
├── SETUP_AND_BUILD.ps1           ← Run this
├── Launch_EchoSight.bat          ← Then run this (double-click)
├── dist/
│   ├── EchoSight/                ← All bundled files
│   │   ├── EchoSight.exe         ← Executable
│   │   ├── openvino/
│   │   ├── cv2/
│   │   └── ... (all dependencies)
│   └── EchoSight-portable.zip    ← For sharing
├── src/
│   └── echosight/
│       └── EchoSight.py          ← Source code
└── build/
    ├── SETUP_AND_BUILD.ps1
    ├── build_portable.ps1
    ├── build_installer.ps1
    └── EchoSight.spec
```

---

## What SETUP_AND_BUILD.ps1 Does

1. ✅ Verifies Python 3.9 is installed
2. ✅ Creates a virtual environment (`.venv`)
3. ✅ Installs all dependencies (OpenVINO, PIL, OpenCV, etc.)
4. ✅ Builds standalone executable with PyInstaller
5. ✅ Creates `Launch_EchoSight.bat` launcher
6. ✅ Creates portable zip archive for distribution

---

## Next Steps

1. **Test the Build**:
   - Double-click `Launch_EchoSight.bat`
   - You should see the EchoSight GUI window open

2. **Load a Model**:
   - Click "Select Model Folder"
   - Navigate to a Geti export folder (contains `detection/`, `project.json`, etc.)
   - Click "Load Model"

3. **Run Inference**:
   - Click "Add Images"
   - Select PNG/JPG/TIFF files
   - Click "Run All"
   - View results

4. **Share**:
   - Send `EchoSight-portable.zip` to others
   - They can extract and run immediately (no Python installation needed!)

---

## Support

For issues or questions:
- Check [USAGE.md](USAGE.md) for full user guide
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if available
- Check [GitHub Issues](https://github.com/okachare/EchoSight/issues)
