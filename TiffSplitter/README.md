# TIFF Splitter (Offline Windows EXE)

This tool splits a multi-page TIFF (`.tif` / `.tiff`) into separate single-image files.

## Features
- Desktop GUI (no command line needed)
- Select input TIFF file
- Select output folder
- Choose output format: PNG, JPEG, BMP, TIFF, WEBP
- Optional JPEG quality control
- Progress and completion status

## Build a standalone EXE (on a build machine)

### 1) Prerequisites
- Windows
- Python 3.10+ installed on the build machine

### 2) Build
From the project folder, run in an already-open PowerShell window:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1
```

If you want the window to stay open when launching directly, use:

```powershell
powershell -NoExit -ExecutionPolicy Bypass -File .\build_exe.ps1
```

This generates:
- `dist\TiffSplitter.exe`

## Run on offline target machine
1. Copy `dist\TiffSplitter.exe` to the offline machine.
2. Double-click `TiffSplitter.exe`.
3. Select TIFF input, output folder, output format, then click **Split TIFF**.

No Python installation is required on the target machine.

## Notes
- For maximum quality, use PNG or TIFF output.
- For smaller files, use JPEG and lower quality values.
- Very large TIFF files can take longer to process.
