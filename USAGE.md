# User Guide

Complete workflows and reference for using EchoSight.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Loading Models](#loading-models)
3. [Running Inference](#running-inference)
4. [Image Preprocessing](#image-preprocessing)
5. [Results Navigation](#results-navigation)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Launch EchoSight

**Option 1: Pre-built**
- Double-click `Launch_EchoSight.bat` or `EchoSight.exe`

**Option 2: From Python**
```powershell
python src/echosight/EchoSight.py
```

The application launches in a maximized dark-themed window.

### UI Layout

```
┌─────────────────────────────────────────────────┐
│  EchoSight - Model-agnostic Image Inference   │
├────────┬────────────────────────────────────────┤
│        │  [Load Model] [Load Images] [Settings] │
│        │                                        │
│ Tabs   │  ┌──────────────────────────────────┐ │
│ ─────  │  │                                  │ │
│ Infer  │  │      Canvas (Model Output)       │ │
│        │  │   (Detections, Masks, Labels)   │ │
│ Analyze│  │                                  │ │
│        │  └──────────────────────────────────┘ │
│ Review │  Frame: 1 / 10  [◀ ▶]  Progress: 45% │
│        │                                        │
│        │  Results: [Best Frame Score: 0.92]   │
│        │                                        │
│        │  [< Run All >] [< Run Current >]       │
└────────┴────────────────────────────────────────┘
```

### Keyboard Shortcuts
- **Arrow Left/Right** — Navigate previous/next frame
- **Scroll Wheel** — Zoom in/out on canvas
- **Click & Drag** — Pan zoomed view

---

## Loading Models

### Model Format Requirements

EchoSight supports models exported from **Intel Geti** with this folder structure:

```
my-geti-deployment/
├── Detection/                    (or Instance Segmentation / Anomaly classification)
│   └── model/
│       ├── model.xml            ← Required
│       ├── model.bin            ← Required
│       ├── config.json          ← Recommended
│       └── model.onnx           (optional)
└── python/                       (optional model_api wrapper)
    └── ...
```

### Load a Model

1. Click **Load Model** button (top toolbar)
2. File browser opens → Navigate to your deployment folder
3. Select the **parent folder** containing `Detection/`, `Instance Segmentation/`, or `Anomaly classification/` subfolder
4. Click **Open**
5. EchoSight scans and loads the model (shows progress)

### What Happens During Load

- Model structure is validated
- `model.xml` and `model.bin` are located
- Task type is detected (Detection, Segmentation, or Anomaly)
- OpenVINO model is compiled (first load may take 30-60 seconds)
- Status bar shows: "✓ Model loaded: Detection"

### Supported Model Types

| Type | Indicator | Output |
|------|-----------|--------|
| **Object Detection** | `Detection/` | Bounding boxes + confidence scores |
| **Instance Segmentation** | `Instance Segmentation/` | Pixel masks + class labels |
| **Anomaly Detection** | `Anomaly classification/` | Heatmap + anomaly score |

---

## Running Inference

### Load Images

1. Click **Load Images** button
2. File browser opens → Select images or TIFF files
3. Supported formats: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tif`, `.tiff`, `.webp`
4. For multi-frame TIFF: All frames are imported automatically
5. Click **Open** to load

### Run Inference

**Option 1: Infer All Frames**
```
Click [< Run All >] button
```
- Processes every loaded image/frame
- Background thread keeps UI responsive
- Progress bar updates in real-time
- Results populated as frames complete

**Option 2: Infer Current Frame**
```
Click [< Run Current >] button
```
- Processes only the active frame (shown in canvas)
- Useful for testing on single images
- Much faster than full batch

### Monitoring Progress

- **Status bar** shows frame count and progress percentage
- **Canvas** updates in real-time as frames complete
- **Results panel** populates with frame scores
- **Cancel button** appears during processing (stops remaining frames)

### What Gets Processed

- **Input**: Current image + any active preprocessing filters
- **Output**: Detection boxes, masks, labels, confidence scores
- **Original images**: Remain unchanged; only processed copies used for inference

---

## Image Preprocessing

### Overview

Preprocessing allows you to enhance or adjust images before inference:
- **Brightness** — Lighten/darken images
- **Contrast** — Increase/decrease visual separation
- **Sharpness** — Enhance or blur edges
- **Denoiser** — Reduce noise artifacts

### Access Preprocessing

1. Click the **Analyze** tab
2. Click the **gear icon** (⚙️) in the lower right
3. Preprocessing popover opens

### Adjust Filters

Each slider controls a filter:

```
Brightness: [◄─●────────►] Default (0)    Applied: OFF
             -100    0    +100

Contrast:   [◄────●──────►] Default (0)    Applied: OFF
             -50     0     +50

Sharpness:  [◄──●────────►] Default (0)    Applied: OFF
             -100    0    +100

Denoiser:   [◄────────●──►] Default (0)    Applied: OFF
             Low          High
```

### Apply to Specific Scope

Choose where preprocessing applies:

| Scope | Behavior |
|-------|----------|
| **All Frames** | Apply to every loaded frame |
| **Current Frame** | Apply only to visible frame |
| **Selected Frames** | Apply to highlighted results (if multiple selected) |

### Apply Processing

1. Adjust slider values
2. Select scope (All / Current / Selected)
3. Click **Apply Processing**
4. Canvas updates with filtered image
5. Status shows: "Processing applied to X frames"

### Reverting Changes

- **Reset Current**: Revert active frame to original
- **Reset All**: Clear all preprocessing, reload originals
- Zoom/pan position is preserved during filter adjustments

### Preview Behavior

- Canvas shows live preview as you adjust sliders
- Slider movement updates display in real-time
- Original image remains in memory unchanged
- Only processed copy is used for inference

---

## Results Navigation

### Frame Navigation

Use Previous/Next controls to review results:

```
Frame: [3] / 10    [◀ ▶]
```

- Click **◀** to go to previous frame
- Click **▶** to go to next frame
- Or press **Arrow Left/Right** on keyboard
- Current frame displays in canvas

### Confidence Filtering

Adjust threshold to filter detections by confidence:

```
Confidence Threshold: [◄───●─────►] 60%
                       1%   50%  100%
```

- Drag slider to set minimum confidence (1-100%)
- Detections below threshold are hidden
- Useful for reducing false positives

### Annotation Visibility

Toggle detection elements independently:

| Control | Effect |
|---------|--------|
| **Show Detections** ✓ | Toggles bounding boxes on/off |
| **Show Labels** ✓ | Toggles text labels on/off |
| **Show Masks** ✓ | Toggles instance segmentation masks on/off |

Example:
```
☑ Show Detections
☐ Show Labels
☑ Show Masks
```

### Results Panel

The Results section shows frame scores:

```
Results
──────────────────────────
Frame 1:    0.92  ← Highest score on frame
Frame 2:    0.78
Frame 3:    0.45
Frame 4:    0.91  ← ← Overall best frame highlighted
Frame 5:    0.55
```

- **Right-aligned score** = highest detection confidence on that frame
- **Bold/highlighted** = overall best frame across all results
- Useful for identifying key frames

### Canvas Controls

**Zoom**
- Scroll wheel up → Zoom in
- Scroll wheel down → Zoom out
- Double-click → Reset to fit window

**Pan**
- Click and drag → Move around zoomed image
- Arrow keys → Fine-tune position (if zoomed)

---

## Troubleshooting

### Common Issues

#### Model Won't Load
**Symptom**: "Model not found" or "Invalid model structure"

**Solution**:
1. Verify folder structure:
   ```
   your-deployment/
   ├── Detection/              ← Check this folder exists
   │   └── model/
   │       └── model.xml       ← Check this file exists
   ```
2. Ensure you select the **parent folder**, not the `model/` subfolder
3. For custom exports, verify `model.xml` and `model.bin` are in `model/` subdirectory

#### Slow Inference (First Run)
**Symptom**: First inference takes 60+ seconds

**Solution**: 
- This is normal; OpenVINO compiles the model on first run
- Subsequent inferences are 5-20x faster
- Be patient and let it complete
- GPU inference not enabled by default

#### TIFF Files Not Loading
**Symptom**: Multi-frame TIFF shows error

**Solution**:
1. Verify TIFF is valid with another image viewer
2. Try converting to PNG:
   ```powershell
   # Using Python + Pillow
   python -c "from PIL import Image; Image.open('file.tiff').save('file.png')"
   ```
3. Some compressed TIFF formats may not be supported

#### No Detections Shown
**Symptom**: Model runs but canvas shows blank image

**Possible Causes**:
1. Confidence threshold too high → Lower to 1%
2. Detection boxes hidden → Enable "Show Detections" checkbox
3. Model has no detections on image (low/zero confidence)
4. Check model output format matches detection boxes (not segmentation)

#### Application Crashes
**Symptom**: Unexpected crash or freeze

**Steps to Debug**:
1. Try running as Administrator
2. Disable antivirus temporarily (may block model files)
3. Ensure model folder not on network drive (use local path)
4. Check Event Viewer for error details
5. Open GitHub Issues with error message

### Getting Help

- 📖 Check [README.md](README.md) and [INSTALL.md](INSTALL.md)
- 🐛 Report bugs on [GitHub Issues](https://github.com/okachare/EchoSight/issues)
- 💬 Ask questions on [GitHub Discussions](https://github.com/okachare/EchoSight/discussions)
- 📧 Contact: Submit issue with screenshot/error log

---

## Tips & Best Practices

### Model Selection
- Ensure model is compatible with your image type (e.g., thermal vs. optical)
- Test with a small batch before full analysis
- Note model accuracy requirements before processing large datasets

### Image Preprocessing
- Start with subtle adjustments (±10-20%)
- Test on a few frames before applying to all
- Save results before processing further

### Performance
- Preprocess on disk-local folders (not network drives)
- Use "Run Current" to test before "Run All"
- Close other applications if inference is slow

### Results Export
- Screenshot canvas for individual results
- Export full result set by saving CSV (when available)
- Use confidence threshold to focus on high-confidence detections

---

## Keyboard Shortcuts Summary

| Key | Action |
|-----|--------|
| **←** Arrow | Previous frame |
| **→** Arrow | Next frame |
| **Scroll ↑** | Zoom in |
| **Scroll ↓** | Zoom out |
| **Drag** | Pan (when zoomed) |

---

Done! Start exploring your models with EchoSight. 🚀
