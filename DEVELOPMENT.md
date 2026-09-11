# Development Guide

Instructions for setting up a development environment, building, and contributing to EchoSight.

## Table of Contents
1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Building from Source](#building-from-source)
4. [Extending EchoSight](#extending-echosight)
5. [Contributing](#contributing)

---

## Development Setup

### Prerequisites

- **Python 3.9** (exactly; 3.10+ not yet supported by OpenVINO 2024.5)
- **Git**
- **Visual Studio Code** (recommended) or any Python IDE
- ~2 GB free disk space

### Initial Setup

1. **Clone Repository**
   ```powershell
   git clone https://github.com/okachare/EchoSight.git
   cd EchoSight
   ```

2. **Create Virtual Environment**
   ```powershell
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # or Command Prompt
   # python -m venv venv
   # venv\Scripts\activate.bat
   ```

3. **Install Dependencies**
   ```powershell
   # Development install (editable mode)
   pip install -e .
   
   # Add development tools
   pip install pyinstaller pytest
   ```

4. **Verify Installation**
   ```powershell
   python src/echosight/EchoSight.py
   # Window should launch successfully
   ```

### IDE Setup (VS Code)

1. Open folder in VS Code
2. Install Python extension by Microsoft
3. Select Python interpreter:
   - Ctrl+Shift+P → "Python: Select Interpreter"
   - Choose `.venv\Scripts\python.exe`

---

## Project Structure

```
EchoSight/
├── src/echosight/
│   ├── __init__.py              # Package metadata
│   ├── EchoSight.py             # Main application entry point
│   └── requirements.txt
├── build/
│   ├── build_installer.ps1      # Build installer executable
│   ├── build_portable.ps1       # Build portable package
│   └── EchoSight.spec           # PyInstaller configuration
├── docs/
│   ├── README.md                # Project overview
│   ├── INSTALL.md               # Installation guide
│   ├── USAGE.md                 # User guide
│   └── DEVELOPMENT.md           # This file
├── .github/
│   └── workflows/
│       └── build-release.yml    # CI/CD for automated releases
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT license
├── setup.py                     # pip setup configuration
└── CHANGELOG.md                 # Version history
```

### Key Files

| File | Purpose |
|------|---------|
| `src/echosight/EchoSight.py` | Core GUI application; ~800 lines |
| `build/EchoSight.spec` | PyInstaller configuration for executable |
| `build/build_portable.ps1` | PowerShell script to build portable package |
| `setup.py` | Package metadata and pip installation config |

---

## Building from Source

### Method 1: Build Portable Package

Portable package includes bundled Python 3.9 runtime + all dependencies (no external Python needed).

```powershell
cd build
.\build_portable.ps1
```

**Output**: `dist/EchoSight/` folder
- Contains `EchoSight.exe` and bundled runtime
- Entire folder can be moved/shared as-is
- ~600 MB total size

**What the script does**:
1. Creates virtual environment with Python 3.9
2. Installs all dependencies (OpenVINO, PIL, OpenCV, etc.)
3. Runs PyInstaller to bundle Python + code + dependencies
4. Creates batch launcher (`Launch_EchoSight.bat`)
5. Packages into portable folder

### Method 2: Build Windows Installer

Creates NSIS installer for traditional installation experience.

```powershell
cd build
.\build_installer.ps1
```

**Output**: `dist/EchoSight-installer.exe`
- Traditional Windows installer wizard
- Installs to Program Files
- Creates Start Menu shortcuts
- ~800 MB total size

### Method 3: Manual Build with PyInstaller

For customized builds:

```powershell
# Install PyInstaller
pip install pyinstaller

# Build executable
cd src/echosight
pyinstaller EchoSight.spec --distpath ../../dist --buildpath ../../build

# Run the built executable
../../dist/EchoSight/EchoSight.exe
```

### Build Troubleshooting

**Issue**: "Python 3.9 not found"
```powershell
# Verify Python version
python --version

# If not 3.9.x, download and install from https://python.org
```

**Issue**: "OpenVINO module not found during build"
```powershell
# Reinstall in virtual environment
pip install --upgrade openvino==2024.5 openvino-dev==2024.5
```

**Issue**: "PyInstaller: No module named 'xxx'"
```powershell
# Ensure all dependencies installed
pip install -e .

# Rebuild
pyinstaller EchoSight.spec --clean
```

---

## Extending EchoSight

### Architecture Overview

```python
EchoSight.py
├── class RoundedButton(tk.Canvas)
│   └── Custom button widget with hover states
│
├── class ModelLoader
│   └── Discovers & loads Geti deployment structure
│
├── class InferenceEngine
│   └── Runs OpenVINO predictions in background thread
│
├── class ResultRenderer
│   └── Draws detection boxes, masks, labels on canvas
│
├── class CanvasManager
│   └── Handles zoom/pan interactions
│
└── class EchoSightApp(tk.Tk)
    └── Main application window & UI logic
```

### Common Customizations

#### 1. Add New Model Type Support

**Current**: Detection, Instance Segmentation, Anomaly

**To add**:
1. Identify output format (e.g., keypoint coordinates)
2. Add detection logic in `InferenceEngine`
3. Add rendering logic in `ResultRenderer`
4. Update model discovery in `ModelLoader`

Example:
```python
# In InferenceEngine.predict()
if task_type == "keypoint_detection":
    # Parse keypoint predictions
    keypoints = prediction_output[0]
    return {"keypoints": keypoints, "confidence": ...}

# In ResultRenderer.draw_results()
if "keypoints" in results:
    for keypoint in results["keypoints"]:
        draw_circle(x, y, radius=5)
```

#### 2. Add Image Filter/Preprocessing

Current filters: brightness, contrast, sharpness, denoise

**To add a new filter**:
1. Add slider in preprocessing popover UI
2. Implement filter function (OpenCV/PIL)
3. Integrate into preprocessing pipeline

Example:
```python
# Add to PreprocessingPipeline class
def apply_saturation(self, image, intensity):
    """Adjust color saturation."""
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1 + intensity)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

# Add slider UI (in EchoSightApp)
self.saturation_slider = ttk.Scale(...)
self.saturation_slider.config(command=lambda v: self._update_preview())
```

#### 3. Export Results to Different Formats

Current: Live display only

**To add export**:
1. Collect results during inference
2. Format for output (CSV, JSON, images)
3. Add export button to UI

Example:
```python
def export_results_csv(self, filepath):
    """Export results to CSV."""
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Frame', 'Detections', 'AvgConfidence'])
        for frame, result in self.results.items():
            writer.writerow([
                frame.name,
                len(result['objects']),
                np.mean([obj['confidence'] for obj in result['objects']])
            ])
```

#### 4. Enable GPU Inference

Current: CPU-only (via OpenVINO)

**To enable GPU**:
```python
# In InferenceEngine.__init__()
# Change from:
self.compiled_model = core.compile_model(model, "CPU")

# To:
self.compiled_model = core.compile_model(model, "GPU.0")  # NVIDIA
# or
self.compiled_model = core.compile_model(model, "GPU.1")  # Intel Arc

# Or make device configurable:
device = os.getenv("OV_DEVICE", "CPU")
self.compiled_model = core.compile_model(model, device)
```

Users can then set:
```powershell
$env:OV_DEVICE = "GPU.0"
python EchoSight.py
```

### Code Style

- **Formatting**: PEP 8 (4-space indents)
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Comments**: Docstrings for functions, inline comments for complex logic
- **Type Hints**: Recommended but not required (Python 3.9 compatible)

Example:
```python
def load_model(self, model_path: Path) -> bool:
    """
    Load OpenVINO model from deployment folder.
    
    Args:
        model_path: Path to deployment parent folder
        
    Returns:
        True if model loaded successfully, False otherwise
    """
    try:
        xml_path = model_path / "model" / "model.xml"
        if not xml_path.exists():
            return False
        # Load model logic...
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False
```

---

## Contributing

### Fork & Branch Workflow

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```powershell
   git clone https://github.com/YOUR-USERNAME/EchoSight.git
   cd EchoSight
   ```

3. **Create feature branch**:
   ```powershell
   git checkout -b feature/my-awesome-feature
   ```

4. **Make changes** and test locally:
   ```powershell
   python src/echosight/EchoSight.py
   ```

5. **Commit** with clear messages:
   ```powershell
   git add .
   git commit -m "Add feature: description of change"
   ```

6. **Push** to your fork:
   ```powershell
   git push origin feature/my-awesome-feature
   ```

7. **Open Pull Request** on GitHub:
   - Title: "Add feature: ..."
   - Description: Why this feature, how it works
   - Screenshots if UI changes

### Pull Request Guidelines

- **Scope**: One feature or bug fix per PR
- **Tests**: Manually test feature locally
- **Documentation**: Update README/USAGE if needed
- **Commits**: Squash multiple commits into 1-2 logical commits
- **Message**: Clear, descriptive commit messages

### Reporting Bugs

1. **Search** existing issues to avoid duplicates
2. **Create Issue** with:
   - Clear title ("Button crashes on click", etc.)
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System info (Windows version, Python 3.9, etc.)

### Feature Requests

1. **Check Discussions** to see if already proposed
2. **Create Discussion** or **Issue** with:
   - What feature is needed
   - Why it's useful
   - Possible implementation approach

---

## Debugging Tips

### Enable Verbose Logging

Modify `EchoSight.py` to add debug prints:

```python
# Add to EchoSightApp.__init__()
self.debug = True

# Add helper method
def debug_log(self, message):
    if self.debug:
        print(f"[DEBUG] {datetime.now().strftime('%H:%M:%S')} - {message}")

# Use in code:
self.debug_log(f"Loading model from: {path}")
self.debug_log(f"Inference time: {elapsed_ms}ms")
```

### Inspect Model Output

```python
# In InferenceEngine.predict()
print(f"Model output shape: {prediction.shape}")
print(f"Model output range: {prediction.min()}-{prediction.max()}")
print(f"Model output type: {prediction.dtype}")
```

### Performance Profiling

```powershell
# Install profiler
pip install py-spy

# Run with profiling
py-spy record -o profile.svg -- python src/echosight/EchoSight.py

# View profile
# Open profile.svg in browser
```

---

## Release Checklist

Before creating a release:

- [ ] All tests pass locally
- [ ] Increment version in `src/echosight/__init__.py`
- [ ] Update `CHANGELOG.md` with new features/fixes
- [ ] Update `README.md` if major changes
- [ ] Build and test portable package
- [ ] Build and test installer
- [ ] Test on clean Windows VM if possible
- [ ] Tag release: `git tag v1.0.0`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub Release with binaries

---

## Resources

- [OpenVINO Documentation](https://docs.openvino.ai/)
- [Tkinter Tutorial](https://docs.python.org/3.9/library/tkinter.html)
- [PyInstaller Docs](https://pyinstaller.org/)
- [Python 3.9 Docs](https://docs.python.org/3.9/)

---

Questions? Open an issue or discussion on GitHub! Happy coding! 🚀
