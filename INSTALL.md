# Installation Guide

Three methods to install and run EchoSight. Choose the option that works best for your use case.

## Method 1: Pre-built Portable (Easiest) 🎯

**Best for:** Users who want to get started immediately without Python.

### Requirements
- Windows 10 or later
- ~2-3 GB free disk space
- No Python installation needed

### Steps

1. **Download Release**
   - Go to [GitHub Releases](https://github.com/okachare/EchoSight/releases)
   - Download `EchoSight-portable.zip` (latest version)

2. **Extract Archive**
   ```powershell
   # Extract to any location (e.g., C:\Applications\)
   Expand-Archive -Path EchoSight-portable.zip -DestinationPath C:\Applications\
   ```

3. **Launch Application**
   - Option A: Double-click `Launch_EchoSight.bat`
   - Option B: Double-click `EchoSight.exe`
   - Window launches maximized, ready to use

4. **Load Your First Model**
   - Click **Load Model** button
   - Navigate to your Geti deployment folder
   - Click **Open** when `model.xml` folder is visible
   - Wait for model to load (30-60 seconds first time)

---

## Method 2: Windows Installer 📦

**Best for:** Users who prefer a traditional installer experience.

### Requirements
- Windows 10 or later
- ~2-3 GB disk space

### Steps

1. **Download Release**
   - Go to [GitHub Releases](https://github.com/okachare/EchoSight/releases)
   - Download `EchoSight-installer.exe`

2. **Run Installer**
   - Double-click `EchoSight-installer.exe`
   - Follow the installation wizard
   - Select installation folder (default: `C:\Program Files\EchoSight\`)

3. **Launch Application**
   - Desktop shortcut or Start Menu → "EchoSight"
   - Or run `Launch_EchoSight.bat` from installation folder

4. **Load Your First Model**
   - Same as Method 1, step 4

---

## Method 3: Python Development Install 🐍

**Best for:** Developers who want to modify or extend EchoSight.

### Requirements
- Windows 10 or later
- **Python 3.9** (exactly; 3.10+ not yet supported by OpenVINO 2024.5)
- Git
- ~1 GB free disk space

### Prerequisites

1. **Install Python 3.9**
   - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ **Important**: Check "Add Python to PATH" during installation

2. **Verify Python Installation**
   ```powershell
   python --version
   # Should output: Python 3.9.x
   ```

3. **Install Git** (if not already installed)
   - Download from [git-scm.com](https://git-scm.com/)

### Installation Steps

1. **Clone Repository**
   ```powershell
   git clone https://github.com/okachare/EchoSight.git
   cd EchoSight
   ```

2. **Create Virtual Environment** (recommended)
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**
   ```powershell
   pip install -e .
   # or manually:
   # pip install -r src/echosight/requirements.txt
   ```

4. **Run Application**
   ```powershell
   python src/echosight/EchoSight.py
   ```

5. **Build Executable** (optional)
   ```powershell
   cd build
   .\build_portable.ps1
   # Creates dist\EchoSight\ folder with bundled runtime
   ```

---

## Method 4: Build Your Own Executable 🔨

**Best for:** Advanced users who want to customize the build or create an installer for distribution.

### Requirements
- Python 3.9
- PyInstaller (automatically installed)
- ~5 GB free disk space (for build artifacts)

### Steps

1. **Clone Repository**
   ```powershell
   git clone https://github.com/okachare/EchoSight.git
   cd EchoSight
   ```

2. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Build Dependencies**
   ```powershell
   pip install -e .
   pip install pyinstaller
   ```

4. **Run Build Script**
   
   **Portable Build** (includes Python runtime):
   ```powershell
   cd build
   .\build_portable.ps1
   # Output: dist\EchoSight\ (entire folder with runtime)
   ```

   **Installer Build** (for distribution):
   ```powershell
   cd build
   .\build_installer.ps1
   # Output: dist\EchoSight-installer.exe
   ```

5. **Verify Build**
   ```powershell
   .\dist\EchoSight\EchoSight.exe
   # or
   .\dist\EchoSight.exe
   ```

---

## Troubleshooting

### "Python 3.9 not found"
```powershell
# Check your Python version
python --version

# If using Python 3.10+, downgrade to 3.9
# See: https://www.python.org/downloads/
```

### "OpenVINO module not found"
```powershell
# Ensure OpenVINO 2024.5 is installed
pip install openvino==2024.5 openvino-dev==2024.5

# If using pre-built, this is already included
```

### Application Crashes on Launch
- Ensure Windows Defender/antivirus doesn't block the executable
- Try running as Administrator (right-click → Run as Administrator)
- Check that your deployment model structure is valid (see [USAGE.md](USAGE.md))

### "Model not found" after loading
- Verify your Geti deployment contains `Detection/`, `Instance Segmentation/`, or `Anomaly classification/` folder
- Ensure `model.xml` and `model.bin` exist in the model subfolder
- Try re-selecting the deployment folder

### Slow First Load
- First inference after loading a model takes 30-60 seconds (OpenVINO compilation)
- Subsequent inferences are much faster
- GPU inference not enabled by default; uses CPU

### TIFF File Issues
- Some compressed TIFF formats may not be supported
- Convert to PNG using:
  ```powershell
  # Using ImageMagick (if installed)
  magick convert input.tiff output.png
  ```

---

## Uninstall

### Portable / Extracted Folder
- Simply delete the extracted folder
- No system registry changes

### Installed via Installer
- Windows Start Menu → Settings → Apps → Apps & Features
- Find "EchoSight" → Click → Uninstall
- Or run `Uninstall.exe` in the installation folder

### Python Development Install
```powershell
cd EchoSight
pip uninstall echosight
# or remove the cloned folder
```

---

## Next Steps

1. **Load your first model** — See [USAGE.md](USAGE.md)
2. **Explore preprocessing features** — Image filters and enhancement
3. **Review results** — Navigate frame-by-frame with Previous/Next
4. **Report issues** — [GitHub Issues](https://github.com/okachare/EchoSight/issues)

---

Need help? Check [USAGE.md](USAGE.md) for detailed workflows or open an issue on GitHub.
