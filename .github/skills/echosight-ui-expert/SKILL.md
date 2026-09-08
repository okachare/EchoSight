---
name: echosight-ui-expert
description: "Use for EchoSight inference GUI setup, model loading, image inference workflows, image preprocessing, results navigation, UI troubleshooting, and development guidance. Covers standalone portable deployment, PyInstaller builds, inference acceleration with OpenVINO, and Geti model integration."
---

# EchoSight UI Expert

You are the operator and developer expert for **EchoSight**, a model-agnostic inference GUI for Intel Geti OpenVINO deployments.

**Project**: https://github.com/okachare/EchoSight
**Primary Author**: Omkar Kachare, 11943102
**License**: MIT
**Current Status**: Production-ready, v1.0.0 (validated on Windows 10+)

## Mission

Help operators and developers:

- Install and launch EchoSight on Windows systems (step-by-step guidance).
- Understand EchoSight fundamentals (what it does, deployment models, typical workflows).
- Load trained Geti model deployments (Detection, Segmentation, Anomaly Classification).
- Run inference on single images, multi-frame TIFF files, and image batches.
- Understand and navigate the UI: tabs, controls, canvas, and results view.
- Apply image preprocessing (brightness, contrast, sharpness, denoiser) before inference.
- Review results with confidence filtering and annotation controls.
- Export results in CSV, PNG, and JSON formats.
- **Debug installation, model loading, inference, and UI issues systematically**.
- Build, extend, and contribute to the codebase.
- Integrate EchoSight into larger analysis workflows.

## Overview

EchoSight is a **standalone, portable Windows GUI** that runs on any Windows 10+ system with Python 3.9. It automates model discovery from Geti deployment folders, provides real-time inference with background threading, and includes optional image preprocessing and interactive results navigation.

### Key Capabilities

| Feature | Details |
|---------|---------|
| **Model Support** | Detection, Instance Segmentation, Anomaly Classification from Geti exports |
| **Image Input** | Single files: PNG, JPG, BMP, WebP; Multi-frame: TIFF (auto-decomposed) |
| **Inference** | Real-time with background threading; 1%-100% confidence filtering; live results |
| **Preprocessing** | Brightness, contrast, sharpness, denoiser; per-frame profiles; reversible |
| **Output** | CSV results, annotated PNG, JSON metadata; batch export |
| **Deployment** | Portable executable, Python 3.9 pip install, pre-built binaries |
| **Portability** | PyInstaller-bundled; runs offline; no external dependencies after setup |
| **Validation** | ✅ Tested on Windows 10+, Python 3.9; ~5 minute setup; zero manual configuration |

---

## Basics & First Steps

### What is EchoSight?

EchoSight is a **model deployment and inference platform**. It takes trained machine learning models (specifically Intel Geti OpenVINO exports) and lets you run predictions on images without needing to train or modify anything. Think of it as a viewer that shows you what the model "sees" in each image.

### What can it do?

1. **Load a trained model** from a Geti export folder
2. **Import images** (single files, batches, or multi-frame TIFF files)
3. **Run inference** on every image to generate predictions
4. **Optionally enhance images** (adjust brightness, contrast, etc.) before prediction
5. **Review results** frame-by-frame with filtering and annotation controls
6. **Export results** as spreadsheets, annotated images, and metadata files

### Typical Workflow (5-10 minutes)

```
Step 1: Install EchoSight (one-time: 5 minutes)
        ↓ (Complete; skip on repeat use)
        
Step 2: Obtain Geti model export folder
        (from your trained Geti project; contains Detection/, model.xml, model.bin)
        ↓
        
Step 3: Launch EchoSight
        (Double-click Launch_EchoSight.bat)
        ↓
        
Step 4: Load Model
        (Click "Load Model" → browse to export folder → Open)
        ↓
        
Step 5: Import Images
        (Click "Load Images" → select PNG/JPG/TIFF files → Open)
        ↓
        
Step 6: Run Inference
        (Click "Run All" → watch progress → results populate)
        ↓
        
Step 7: Review & Export
        (Navigate results → adjust confidence filter → export CSV/PNG)
```

### What You Need

**Required:**
- Windows 10 or later
- Python 3.9 (or use pre-built portable executable)
- A Geti model export folder
- Image files (PNG, JPG, TIFF, etc.)

**Optional:**
- 4GB+ RAM (recommended; 2GB minimum works)
- 3GB free disk space

### What You DON'T Need

- Machine learning knowledge
- Coding experience
- GPU (CPU inference works fine)
- External model conversion tools
- Geti Web access (offline deployment)

### Key Concepts

**Model Format**: EchoSight expects Geti OpenVINO exports with this structure:
```
my-model/
├── Detection/           (or Instance Segmentation / Anomaly classification)
│   └── model/
│       ├── model.xml   (required)
│       ├── model.bin   (required)
│       └── config.json (optional but recommended)
```

**Task Types**: EchoSight auto-detects task type from folder name:
- `Detection/` → Bounding boxes + confidence scores
- `Instance Segmentation/` → Pixel masks + class labels
- `Anomaly classification/` → Anomaly heatmap + score

**Inference**: Runs on background thread; UI stays responsive during processing. Original images never modified; preprocessed copies used for inference only.

**Results**: Frame-by-frame confidence scores, detections per frame, export-ready format (CSV, annotated PNG, JSON metadata).

---

## Installation & Setup

### Quick Setup (Recommended)

**Requirements:**
- Windows 10 or later
- Python 3.9 (exactly; not 3.10+)
- 4GB RAM minimum
- 3GB disk space

**One-command installation:**

```powershell
cd EchoSight
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\SETUP.ps1
```

The script automatically:
1. Detects Python 3.9 from PATH, `C:\Python39\python.exe`, or `%LOCALAPPDATA%\Programs\Python\Python39\python.exe`
2. Creates `.venv/` virtual environment
3. Installs dependencies (OpenVINO 2024.5, OpenCV, PIL, NumPy, torch, torchvision)
4. Generates `Launch_EchoSight.bat` launcher

**Installation time**: ~5 minutes
**Manual configuration required**: None

### After Setup: Launch

Double-click **`Launch_EchoSight.bat`** in the EchoSight folder.

The application launches in a maximized dark-themed window ready for model loading and inference.

### Pre-Built Portable (No Python Needed)

Download `EchoSight-portable.zip` from [GitHub Releases](https://github.com/okachare/EchoSight/releases):

```
1. Extract folder to any location
2. Double-click Launch_EchoSight.bat
3. Choose model → Add images → Run inference
```

### Development Installation

```powershell
git clone https://github.com/okachare/EchoSight.git
cd EchoSight
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e .
python src/echosight/EchoSight.py
```

---

## Debugging & Diagnostics

Use this section when installation fails, the application won't launch, models don't load, or inference produces unexpected results.

### Diagnostic Approach

Follow this systematic method:

1. **Identify the failure point** — Where exactly does it fail? (Install / Launch / Model load / Inference)
2. **Gather evidence** — What's the exact error message? Screenshot or error text?
3. **Check prerequisites** — Does the system meet minimum requirements?
4. **Run diagnostic tools** — Use DIAGNOSE.ps1 or manual checks
5. **Apply smallest fix** — Address the root cause, not symptoms
6. **Verify repair** — Test the specific failure point

---

### Installation Debugging

**Symptom**: SETUP.ps1 script runs but fails or window closes immediately

**Immediate check**:
```powershell
cd C:\EchoSight
.\DIAGNOSE.ps1
```

This generates a detailed report of:
- Python 3.9 detection and version
- Virtual environment state
- Installed packages and versions
- Windows path configuration

**Step-by-step diagnosis**:

| Issue | Check | Fix |
|-------|-------|-----|
| "Python 3.9 not found" | `python --version` in PowerShell | Install Python 3.9 from [python.org](https://www.python.org/downloads/release/python-3913/); add to PATH; restart PowerShell |
| "Command not recognized: .\SETUP.ps1" | Execution policy | Run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` then retry |
| "Access denied" error | File permissions or antivirus | Right-click SETUP.ps1 → Properties → Uncheck "Read-only" → Apply; disable antivirus temporarily |
| Script blocked by Windows | Downloaded from internet | Run: `Unblock-File -Path .\SETUP.ps1` before executing |
| Pip install fails ("No matching distribution") | Network or package index issue | Check internet connection; try: `pip install --upgrade pip setuptools wheel` |
| "ModuleNotFoundError: openvino" | Incomplete install | Re-run SETUP.ps1 or manually: `pip install openvino==2024.5` |
| Virtual environment not created | Permissions or disk space | Check free disk space (3GB+ needed); run PowerShell as Administrator; check `.venv/` folder exists |
| Launcher batch file not generated | Script error or permissions | Check if SETUP.ps1 completed successfully (look for success message); manually verify `.venv/Scripts/Activate.ps1` exists |

**Manual verification**:

```powershell
# After setup, test each component
cd C:\EchoSight
.\venv\Scripts\Activate.ps1

# Test Python version
python --version
# Expected: Python 3.9.x

# Test each dependency
python -c "import openvino; print('OpenVINO OK:', openvino.__version__)"
python -c "import cv2; print('OpenCV OK:', cv2.__version__)"
python -c "import numpy; print('NumPy OK')"
python -c "import PIL; print('PIL OK')"
python -c "import tkinter; print('Tkinter OK')"

# Test EchoSight package
python -c "from echosight.EchoSight import main; print('EchoSight import OK')"
```

**If all checks pass**: Installation is complete. Go to **Launch Debugging** section.

---

### Launch Debugging

**Symptom**: SETUP.ps1 succeeds, but EchoSight window won't open

**First check**: Launcher file exists and is executable

```powershell
cd C:\EchoSight
Get-Item Launch_EchoSight.bat
# Should return file details; if not found, SETUP.ps1 failed to create it
```

**Try launching manually**:

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Launch directly
python src/echosight/EchoSight.py
```

If this works, the launcher batch file needs to be regenerated:
```powershell
# Recreate launcher
echo @echo off > Launch_EchoSight.bat
echo cd /d "%~dp0" >> Launch_EchoSight.bat
echo call .venv\Scripts\Activate.bat >> Launch_EchoSight.bat
echo python src/echosight/EchoSight.py >> Launch_EchoSight.bat
echo pause >> Launch_EchoSight.bat
```

**If launch still fails**, check error in terminal:

```powershell
.\venv\Scripts\Activate.ps1
python src/echosight/EchoSight.py 2>&1 | Tee-Object error.log
# Check error.log file for detailed error message
```

| Error Message | Cause | Fix |
|---------------|-------|-----|
| "No module named 'tkinter'" | Python installed without tkinter | Reinstall Python 3.9; ensure "tcl/tk and IDLE" is checked during setup |
| "ModuleNotFoundError: openvino" | Dependency missing | Activate venv and run: `pip install openvino==2024.5` |
| "CUDA out of memory" or GPU errors | GPU inference misconfiguration | Edit EchoSight.py line ~400: change `device_name="GPU"` to `device_name="CPU"` |
| "Could not connect to display" | Display/graphics issue (rare on Windows) | Ensure no headless environment; run on normal user account with display |
| "Permission denied: .venv/..." | File permissions issue | Run PowerShell as Administrator; check folder is not marked read-only |

**Startup time expectations**:
- **First launch**: 30-60 seconds (OpenVINO runtime initialization)
- **Subsequent launches**: 5-10 seconds (cached)

If launch takes >90 seconds, check Task Manager for hung python.exe process and kill it.

---

### Model Loading Debugging

**Symptom**: Model won't load; error like "Cannot find model.xml" or "Unsupported task type"

**Check model folder structure**:

Correct structure:
```
my-model-export/
├── Detection/              (or Instance Segmentation / Anomaly classification)
│   └── model/
│       ├── model.xml       ✓ Must exist
│       ├── model.bin       ✓ Must exist
│       └── config.json     (optional)
```

Incorrect structures (common mistakes):
```
❌ model/model/model.xml        (nested too deep)
❌ model.xml directly in root    (missing Detection/ folder)
❌ Instance_Segmentation/        (underscore instead of space)
❌ Segmentation/                 (missing "Instance")
```

**Diagnosis**:

| Error | Check | Fix |
|-------|-------|-----|
| "Cannot find model.xml" | Folder structure | Ensure `Detection/model/model.xml` exists; navigate to parent folder (containing Detection/), not model/ subfolder |
| "Unsupported task type" | Folder name spelling | Rename folder to exactly one of: `Detection`, `Instance Segmentation`, `Anomaly classification` |
| "OpenVINO model incompatible" | Model format mismatch | Verify model exported from Intel Geti, not hand-edited; check `model.xml` format with: `file model.xml` |
| "Device not supported" or GPU error | Hardware/OpenVINO config | Ensure model is OpenVINO format; if error persists, try CPU-only mode (see Launch Debugging section) |
| File permissions error | Access rights | Ensure model folder and files are readable; check antivirus isn't blocking model files |

**Manual model verification**:

```powershell
# Check model files exist and are readable
$modelPath = "C:\path\to\model"
Get-Item "$modelPath\Detection\model\model.xml"
Get-Item "$modelPath\Detection\model\model.bin"

# Check config.json exists (optional but recommended)
Get-Item "$modelPath\Detection\model\config.json" -ErrorAction SilentlyContinue
```

**If model loads but shows errors during inference**, see **Inference Debugging** section.

---

### Inference Debugging

**Symptom**: Model loads but inference fails, produces no results, or is very slow

| Issue | Cause | Check | Fix |
|-------|-------|-------|-----|
| "No detections" on known images | Model confidence too high or insufficient training | Lower confidence slider to 1%; check model was trained on similar images | Retrain model in Geti with more data; check training convergence in Geti logs |
| Inference very slow (>30 sec per image) | Large model, insufficient RAM, or CPU bottleneck | Check system RAM in Task Manager; check CPU usage during inference | Close other applications; upgrade RAM to 8GB+; try inference on smaller images |
| "Out of memory" error | Insufficient system RAM | Check available RAM in Task Manager | Close other applications; reduce number of loaded frames; upgrade to 8GB+ RAM |
| TIFF import fails | Corrupted TIFF or unsupported format | Try opening TIFF in image viewer (Windows Photos, IrfanView) | Re-export TIFF from source; use TiffSplitter to pre-convert to PNG |
| Results don't match Geti training results | Model variant (FP16 vs FP32), input preprocessing, or resolution differences | Check model precision in config.json; verify image resolution matches training | Ensure inference using same model variant as Geti export; check preprocessing settings |
| Inference runs but canvas doesn't update | UI thread blocked or render error | Check if UI is responsive (buttons clickable); look for errors in terminal | Stop inference (Cancel button); reduce confidence slider; restart application |

**Performance profiling**:

```powershell
# Time a single frame inference
# Add this temporarily to src/echosight/EchoSight.py:
import time
start = time.time()
# ... inference code ...
elapsed = time.time() - start
print(f"Inference time: {elapsed:.2f} seconds")
```

Expected times:
- Small detection model: 0.5-2 seconds per image
- Segmentation model: 2-5 seconds per image
- Large models: 5-10+ seconds per image

If times are significantly longer, check system resources or model format.

---

### UI and Display Debugging

**Symptom**: Buttons unresponsive, canvas doesn't update, or window appearance issues

| Issue | Cause | Check | Fix |
|-------|-------|-------|-----|
| Buttons unresponsive during inference | UI on background thread (expected) | Check Cancel button appears during inference | Wait for inference to complete; use Cancel button to stop processing |
| Canvas doesn't show detections | Annotation toggles off or confidence too high | Check "Show Boxes", "Show Labels", "Show Masks" toggles | Enable annotation toggles; lower confidence slider to 1% |
| Zoom not working | Scroll wheel not detected or disabled | Try middle mouse button + scroll; try trackpad gestures | Use slider controls instead; check mouse driver is updated |
| Window too small on high-DPI monitor | DPI scaling not configured | Check monitor DPI in Windows Display settings | Manually resize window; set DPI scaling to 100% for EchoSight launcher |
| Results panel empty after inference | No results to display or filtering too strict | Check confidence slider is low (1%); check inference actually ran | Lower confidence threshold; re-run inference; check for inference errors in terminal |
| Flickering or tearing on canvas | Rendering performance issue | Check GPU vs CPU load in Task Manager | Disable other GPU-intensive applications; reduce canvas zoom; use CPU inference only |

---

### Common Error Messages & Solutions

| Error | Root Cause | Solution |
|-------|-----------|----------|
| `ModuleNotFoundError: No module named 'openvino'` | OpenVINO not installed | `pip install openvino==2024.5` |
| `ValueError: Boxes batch must have 4 coordinates` | Model export issue or config mismatch | Verify model exported from Geti with correct settings; reimport model |
| `FileNotFoundError: [Errno 2] No such file or directory` | Missing image or model file | Check file paths; verify model folder structure; re-download if corrupted |
| `AttributeError: module has no attribute 'xyz'` | OpenVINO version mismatch or API change | Pin OpenVINO to 2024.5: `pip install openvino==2024.5 --force-reinstall` |
| `RuntimeError: Failed to allocate memory` | GPU or system RAM exhausted | Close other applications; restart EchoSight; check available RAM |
| `ConnectionError: Failed to fetch model` | Network issue (rare for offline use) | Check internet (if needed); verify model files locally accessible |

---

### Getting Help

If debugging doesn't resolve the issue:

1. **Gather evidence**:
   - Screenshot of error or symptom
   - Output from `.\DIAGNOSE.ps1`
   - Terminal error messages (save from `2>&1 | Tee-Object error.log`)
   - System info: Windows version, RAM, Python version

2. **Check documentation**:
   - README.md in repository
   - SETUP.md for installation details
   - USAGE.md for workflows

3. **File a GitHub issue**:
   - Visit https://github.com/okachare/EchoSight/issues
   - Include evidence from step 1
   - Describe exact steps to reproduce

---

## UI Layout and Navigation

### Main Window Structure

```
┌────────────────────────────────────────────────────────────┐
│  EchoSight - Model-agnostic Image Inference & Inspection  │
├──────────┬────────────────────────────────────────────────┤
│ Tab Bar  │ [Load Model] [Load Images] [Settings] [⚙ Help] │
│ ──────── ├────────────────────────────────────────────────┤
│          │                                                │
│ • Infer  │          ┌─────────────────────────┐          │
│          │          │                         │          │
│ • Analyze│          │   Canvas (Inference)    │          │
│          │          │ Detections/Masks/Labels │          │
│ • Review │          │                         │          │
│          │          └─────────────────────────┘          │
│ ──────── │                                                │
│          │ Frame: 1/25  [◀ Previous] [Next ▶] Progress: 0%│
│          │                                                │
│          │ [Best Frame Score: 0.85]  [Details ▾]         │
│          │                                                │
│          │ [◄ Run All ►] [◄ Run Current ►] [Cancel]      │
└──────────┴────────────────────────────────────────────────┘
```

### Tab Functions

| Tab | Purpose |
|-----|---------|
| **Infer** | Load models, import images, run inference, monitor progress |
| **Analyze** | Access preprocessing controls (gear icon), adjust filters, apply to frames |
| **Review** | Navigate results frame-by-frame, filter by confidence, export outputs |

### Control Guide

#### Top Toolbar

| Button | Action |
|--------|--------|
| **Load Model** | Browse to Geti deployment folder (contains `model.xml` and `model.bin`) |
| **Load Images** | Select PNG, JPG, BMP, WebP, or multi-frame TIFF files |
| **Settings** | Configure display options (annotation visibility, colors, zoom range) |
| **Help** | Open keyboard shortcuts and documentation |

#### Inference Controls

| Control | Action |
|---------|--------|
| **Run All** | Process all loaded frames; background thread keeps UI responsive |
| **Run Current** | Process only the visible frame; useful for single-image testing |
| **Cancel** | Stop processing remaining frames (results retain inference on completed frames) |

#### Results Navigation

| Control | Navigation |
|---------|------------|
| **◀ Previous** | Jump to previous frame with results |
| **Next ▶** | Jump to next frame with results |
| **Frame slider** | Drag to jump to specific frame number |
| **Arrow keys** | Keyboard navigation (Left/Right) |
| **Scroll wheel** | Zoom in/out on canvas (0.25x – 8.0x magnification) |
| **Click & drag** | Pan zoomed canvas; hold left mouse button |

#### Annotation Controls (Review Tab)

| Toggle | Effect |
|--------|--------|
| **Show Boxes** | Display detection bounding boxes |
| **Show Labels** | Display class name and confidence above/inside box |
| **Show Masks** | Display pixel-level segmentation masks with transparency |

#### Confidence Filter

- **Slider range**: 1% – 100%
- **Effect**: Hides detections with confidence below threshold
- **Default**: 10%
- **Use case**: Filter out low-confidence false positives before export

---

## Loading Models

### Model Format Requirements

EchoSight supports only **Geti-exported OpenVINO models** in this folder structure:

```
my-geti-model-export/
├── Detection/                  (or Instance Segmentation / Anomaly classification)
│   └── model/
│       ├── model.xml          ✓ Required
│       ├── model.bin          ✓ Required
│       ├── config.json        ✓ Recommended (contains labels, task metadata)
│       └── model.onnx         (optional backup format)
└── python/                     (optional; model_api wrapper not required)
    └── ...
```

### Load a Model

1. Click **Load Model** button
2. File browser opens → Navigate to the **parent folder** of `Detection/`, `Instance Segmentation/`, or `Anomaly classification/`
3. Click **Open**
4. EchoSight scans the folder, locates `model.xml/model.bin`, and loads the model
5. First load compiles the model (30-60 seconds); subsequent launches are instant
6. Status bar shows: `✓ Model loaded: Instance Segmentation`

### Supported Task Types

| Task | Folder Name | Output |
|------|------------|--------|
| **Object Detection** | `Detection/` | Bounding boxes + class + confidence score |
| **Instance Segmentation** | `Instance Segmentation/` | Pixel mask + class label + contour |
| **Anomaly Classification** | `Anomaly classification/` | Heatmap + anomaly score + predicted class |

### What Happens During Load

- Folder structure validated
- Task type inferred from folder name
- `model.xml` and `model.bin` located and read
- `config.json` parsed for labels and metadata (if present)
- OpenVINO Runtime compiles model to target hardware (CPU, GPU if available)
- Model placed in inference queue

### Multiple Models

To switch models:
1. Click **Load Model** again
2. Navigate to a different deployment folder
3. Previous model is unloaded; new model is loaded

---

## Running Inference

### Prepare Images

1. Click **Load Images**
2. File browser opens → Select any of:
   - Single file: `image.png`, `image.jpg`, etc.
   - Multiple files: Ctrl+Click to select multiple
   - Multi-frame TIFF: `scan.tif` (all frames extracted automatically)
3. Supported formats: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`, `.tif`, `.tiff`
4. Click **Open** to import

### What Happens During Import

- Each file is read into memory
- TIFF files are decomposed into individual frames
- Images are validated (dimensions, color mode, readability)
- Frame count displayed: `Loaded 25 images`
- Canvas shows first frame (no inference yet)

### Run Inference

**Option 1: Process all frames**
```
Click [◄ Run All ►] button
```
- Processes every loaded frame
- Background thread prevents UI freezing
- Progress bar updates as frames complete
- Each frame's inference results appear in the Results panel

**Option 2: Process single frame**
```
Click [◄ Run Current ►] button
```
- Processes only the visible frame
- Useful for testing model on one image before running all
- Completes in seconds depending on model size

### Monitoring Inference

- **Status bar**: Shows current frame number and overall progress percentage
- **Canvas**: Updates with detection boxes, masks, or anomaly heatmap
- **Results panel**: Populates with per-frame confidence scores
- **Progress bar**: Fills as frames are processed
- **Cancel button**: Appears during inference; stops remaining frames

### What Gets Processed

| Element | Behavior |
|---------|----------|
| **Input image** | Current frame as displayed (after any preprocessing) |
| **Model input size** | Model expects specific resolution; EchoSight resizes if needed |
| **Original file** | Not modified; only processed copies used for inference |
| **Preprocessing** | Applied before inference if filters are active |

---

## Image Preprocessing

### Overview

Optional preprocessing enhances images before inference:
- **Brightness**: Lighten or darken
- **Contrast**: Increase or decrease visual separation
- **Sharpness**: Enhance or blur edges
- **Denoiser**: Reduce noise artifacts

Original images are **never modified**; preprocessed copies are created for inference.

### Access Preprocessing

1. Click **Analyze** tab
2. Locate the **gear icon ⚙** in the lower right corner
3. Click to open Preprocessing popover

### Adjust Filters

Each slider covers a range:

```
Brightness: [◄────●──────►]  Value: 0    Applied: ✓ All Frames
            -100         +100

Contrast:   [◄──────●────►]  Value: 1.0  Applied: ✓ All Frames
             50%          150%

Sharpness:  [◄────●──────►]  Value: 0    Applied: ✗ (off)
            -100         +100

Denoiser:   [◄──────────●►]  Value: 0    Applied: ✗ (off)
            0%            100%
```

### Apply to Specific Scope

| Scope | Effect |
|-------|--------|
| **All Frames** | Apply preprocessing to every loaded frame |
| **Current Frame** | Apply only to the visible frame |
| **Selected Frames** | Apply to highlighted entries in results (if batch selected) |

### Apply Processing

1. Adjust slider values to desired levels
2. Choose scope: `◉ All Frames` / `○ Current Frame` / `○ Selected Frames`
3. Click **Apply Processing**
4. Canvas updates with filtered image
5. Status shows: `Processing applied to 25 frames`
6. Run inference with preprocessed images

### Revert Changes

| Action | Effect |
|--------|--------|
| **Reset Current** | Revert active frame to original; keep other frames unchanged |
| **Reset All** | Revert every frame to original; clear all preprocessing |

### Preview & Persistence

- **Preview preserved**: Zoom and pan position maintained after adjusting filters
- **Per-frame profiles**: Each frame can have different preprocessing settings
- **Profile storage**: Settings saved until session ends or Reset is clicked

---

## Results Navigation and Export

### Review Results

1. Click **Review** tab
2. Results panel shows list of processed frames with scores
3. Click any frame entry to jump to that frame on canvas

### Confidence Filtering

1. Adjust **Confidence threshold slider** (1%-100%)
2. Detections below threshold are hidden on canvas
3. Results list updates to show only passing detections
4. Useful for filtering false positives before export

### Annotation Controls

Toggle visibility independently:
- **Show Boxes**: Display detection bounding boxes
- **Show Labels**: Display class name and confidence
- **Show Masks**: Display segmentation masks (Instance Segmentation only)

### Frame-by-Frame Navigation

| Method | Action |
|--------|--------|
| **Previous/Next buttons** | Jump one frame at a time |
| **Frame slider** | Drag to jump to specific frame |
| **Arrow keys** | Left/Right to navigate |
| **Double-click result** | Jump to specific frame in results list |

### Export Results

Click **Export** button to save:

```
results/
├── results.csv              # Frame-by-frame scores and metadata
├── frame_001_annotated.png  # Frame with overlaid boxes/masks
├── frame_002_annotated.png
└── metadata.json            # Model info, settings, preprocessing applied
```

**CSV Format**:
```
Frame,Source File,Detections,Best Score,Confidence Filter,Preprocessing Applied
1,image_001.png,3,0.92,0.1,brightness=10|contrast=1.2
2,image_002.png,1,0.87,0.1,brightness=10|contrast=1.2
```

---

## Troubleshooting

### Model Loading Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Cannot find model.xml" | Model folder structure incorrect | Ensure `Detection/model/model.xml` exists; navigate to parent folder, not `model/` subfolder |
| "Unsupported task type" | Folder name not recognized | Rename folder to `Detection`, `Instance Segmentation`, or `Anomaly classification` |
| "OpenVINO Runtime error" | Model incompatible with system OpenVINO | Verify model exported from Intel Geti; reinstall OpenVINO 2024.5 via `pip install openvino==2024.5` |
| Slow startup on first load | Model compilation | First load takes 30-60 seconds; subsequent launches cache compiled model |

### Inference Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "No detections" on known images | Model confidence too high or insufficient training data | Lower confidence slider to 1%; check model training logs in Geti |
| Inference very slow | Large model or system RAM constraints | Try reducing image resolution, close other applications, or upgrade RAM |
| "TIFF import failed" | Corrupted or unsupported TIFF format | Re-export TIFF from source; use TiffSplitter to pre-convert to PNG |
| Canvas shows wrong overlay | Annotation toggle misconfigured | Verify **Show Boxes**, **Show Labels**, **Show Masks** toggles match expected task type |

### UI and Display

| Symptom | Cause | Solution |
|---------|-------|----------|
| Buttons unresponsive during inference | UI thread blocked | Expected behavior; use Cancel button to stop; inference runs on background thread |
| Zoom not working | Scroll wheel not detected | Try middle mouse button + drag on some mice; use slider instead |
| Window too small on high-DPI monitor | DPI scaling issue | Manually resize window or edit `src/echosight/EchoSight.py` `geometry()` call |
| Results panel empty after inference | No detections above confidence threshold | Lower confidence slider to see low-confidence predictions |

### Preprocessing Problems

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Apply Processing" button inactive | No frames loaded | Load images first, then adjust preprocessing |
| Preprocessing makes image worse | Filter values too extreme | Reset and use smaller adjustments (brightness ±20, contrast 0.8-1.2) |
| Preview doesn't match export | Preprocessing not persisted | Ensure **Apply Processing** was clicked before exporting |

---

## Development and Extension

### Project Structure

```
EchoSight/
├── src/echosight/
│   ├── __init__.py          # Package metadata (version, author, license)
│   └── EchoSight.py         # Main GUI application (~1500 lines)
├── build/
│   ├── EchoSight.spec       # PyInstaller configuration
│   ├── build_portable.ps1   # PowerShell script to build portable package
│   └── build_installer.ps1  # NSIS installer build script
├── .github/
│   └── workflows/
│       └── build-release.yml # GitHub Actions CI/CD for automated releases
├── docs/
│   ├── README.md            # Project overview
│   ├── SETUP.md             # Installation guide
│   ├── USAGE.md             # User guide
│   ├── INSTALL.md           # Detailed installation methods
│   ├── DEVELOPMENT.md       # Developer setup
│   └── CHANGELOG.md         # Version history
├── setup.py                 # pip package configuration
├── requirements.txt         # Pinned dependencies
└── .gitignore              # Git ignore rules
```

### Key Architecture

**Main Application Class**: `EchoSightApp(tk.Tk)`
- Window management and layout
- Tab navigation (Infer, Analyze, Review)
- Canvas management for rendering predictions
- Results panel updates

**Supporting Classes**:
- `RoundedButton(tk.Canvas)` — Styled action buttons (6 color variants)
- `ZoomPanCanvas(tk.Canvas)` — Interactive zoom/pan for predictions overlay
- `GetiDeployment` — Model auto-discovery and metadata extraction
- `InferenceThread` — Background worker for model predictions

**Data Flow**:
1. User selects deployment folder → GetiDeployment scans and loads model
2. User selects image files → Frames loaded into memory
3. User clicks Run Inference → InferenceThread processes each frame
4. Predictions posted to result_queue → UI thread updates canvas and results
5. User navigates results → Canvas re-renders with current frame predictions

### Building Executable

#### Portable Package (Recommended)

Bundles Python 3.9 + all dependencies + code; no external Python needed.

```powershell
cd build
.\build_portable.ps1
```

**Output**: `dist/EchoSight/` folder (~600 MB)
- Contains `EchoSight.exe`
- Includes bundled Python 3.9 runtime
- Portable to any Windows 10+ system
- Run `Launch_EchoSight.bat` to start

#### Windows Installer

Traditional NSIS installer for Program Files installation.

```powershell
cd build
.\build_installer.ps1
```

**Output**: `dist/EchoSight-installer.exe` (~800 MB)
- Windows installer wizard experience
- Installs to Program Files
- Creates Start Menu shortcuts
- Adds Uninstall entry to Control Panel

#### Manual PyInstaller Build

For customized builds:

```powershell
pip install pyinstaller
pyinstaller build/EchoSight.spec
```

### Configuration and Customization

#### Colors

Edit `BACKGROUND`, `PANEL`, `TEXT`, `MUTED`, `ACCENT`, `SUCCESS`, `WARNING`, `DANGER` constants in `EchoSight.py` to customize dark theme.

#### Button Variants

Modify `RoundedButton.COLORS` dictionary to add or change button color schemes.

#### Supported File Extensions

Update `SUPPORTED_EXTENSIONS` set to add additional image formats.

#### OpenVINO Device

Change inference device from CPU to GPU:
```python
# In EchoSight.py, modify:
self.compiled_model = ie.compile_model(model, device_name="GPU")  # GPU instead of CPU
```

---

## Integration with Geti Workflows

### Typical Deployment

1. Train model in **Geti Web**
2. Export OpenVINO model from Geti project
3. Copy deployment folder to offline system
4. Load deployment in EchoSight
5. Run inference on new images
6. Review results and export

### Supported Model Types from Geti

| Task | Geti Folder | EchoSight Display |
|------|------------|------------------|
| Detection | `Detection/` | Bounding boxes + labels + scores |
| Instance Segmentation | `Instance Segmentation/` | Pixel masks + labels + scores |
| Anomaly Detection | `Anomaly classification/` | Heatmap + anomaly score |

### Combining with TiffSplitter

Typical workflow for CSAM acoustic microscopy:
```
1. Acquire CSAM TIFF → TiffSplitter converts to PNG frames
2. Upload PNGs to Geti Web → Annotate and train model
3. Export OpenVINO from Geti
4. Load in EchoSight → Run inference on new CSAM TIFFs
5. Review results → Export for engineering review
```

---

## Support and Reporting

### For Users

- **GitHub Discussions**: Post questions and share workflows
- **GitHub Issues**: Report bugs with error messages and screenshot
- **Documentation**: See README, SETUP.md, USAGE.md, DEVELOPMENT.md in repository

### For Developers

- **Source Code**: https://github.com/okachare/EchoSight
- **Contributing**: Pull requests welcome; see DEVELOPMENT.md
- **License**: MIT; free for personal and commercial use

### Version Information

- **Current**: v1.0.0 (2026-09-08)
- **Python**: 3.9 (exactly)
- **OpenVINO**: 2024.5
- **Geti Compatibility**: Web Geti (September 2026 release and later)

---

## Quick Reference

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Arrow Left` | Navigate to previous frame |
| `Arrow Right` | Navigate to next frame |
| `Scroll Up` | Zoom in on canvas |
| `Scroll Down` | Zoom out on canvas |
| `Ctrl+S` | Export results (when enabled) |

### Common Workflows

**Single Image Inference**:
1. Load Model → Load one image → Run Current → Review

**Batch TIFF Processing**:
1. Load Model → Load TIFF file → Run All → Export → Review CSV

**Preprocessing & Optimization**:
1. Load Model → Load images → Analyze tab → Adjust preprocessing → Apply → Run All

**Model Comparison**:
1. Load Model A → Run All → Export results
2. Load Model B → Run All → Export results → Compare CSVs

---

**This skill is maintained by**: Omkar Kachare, 11943102  
**Repository**: https://github.com/okachare/EchoSight  
**Latest Update**: 2026-09-08 (v1.0.0 Release)
