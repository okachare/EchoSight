# EchoSight

Model-agnostic image inference and inspection.

Portable standalone GUI application for running Geti OpenVINO model deployments on images and multi-frame TIFF files.

**Author:** Omkar Kachare

---

## Quick Start

### Installation (Windows)

1. **Download and build** the portable installer:
   ```powershell
   cd Deployment\EchoSight_Inference_GUI
   .\build_installer.ps1
   ```

2. **Copy the executable**:
   - Find the built folder at `dist\EchoSight\`
   - Copy the entire `EchoSight` folder to any location on your system
   - No additional installation or Python required

3. **Launch**:
   - Double-click `EchoSight.exe` to start the application
   - The GUI launches maximized for a full-screen working view

4. **Load your model**:
   - Click **Load Model** button
   - Select your Geti deployment parent folder (the folder containing `Detection/`, `Instance Segmentation/`, or `Anomaly classification/` subdirectory)
   - EchoSight automatically discovers and loads the model

---

## Features

- **Standalone portable**: All dependencies bundled; runs on Windows without Python installation
- **Dark theme with high-contrast controls**: Professional UI with soft rounded button corners
- **Model discovery**: Automatically finds model.xml and config.json in the deployment folder structure
- **Multi-format import**: Common images (PNG, JPG, BMP, WebP) and multi-frame TIFF files
- **Real-time model inference**: Background threading keeps UI responsive; progress updates shown for each frame
- **Confidence filtering**: Adjustable 1%-100% confidence threshold for detection results
- **Image preprocessing**: Optional brightness, contrast, sharpness, and denoiser adjustments
  - Apply to all frames, current frame, or selected frames
  - Original images remain preserved
  - Per-frame profile storage and preview preservation
- **Results review**: Navigate results with Previous/Next, zoom and pan detection overlays
- **Annotation visibility**: Toggle detection boxes, labels, and instance masks independently
- **Export**: Save results as annotated images, CSV, or JSON for downstream analysis

---

## Usage Workflow

1. **Load Model**: Click `Load Model` → Select deployment folder → Confirm
2. **Import Images**: Click `Import Images` → Select image files or TIFF sequences → Confirm
3. **Configure (Optional)**: Click the gear icon in preview corner → Adjust preprocessing sliders → Click `Apply Processing`
4. **Run Inference**: Click `Run Current` for single frame or `Run All` for batch processing
5. **Review Results**: Navigate frames with Previous/Next, adjust confidence filter, toggle annotations
6. **Export**: Click `Export` to save results as annotated images, CSV, or JSON

---

## System Requirements

- **Windows 7 or later** (64-bit)
- **2 GB RAM minimum** (4 GB+ recommended)
- **500 MB disk space** for application folder
- **GPU optional**: OpenVINO CPU inference is bundled; GPU support requires separate installation

---

## Build Requirements (Developer)

If rebuilding the installer from source:

- Python 3.9+
- PowerShell 5.1+
- Dependencies listed in `requirements.txt`:
  - Pillow >= 10.0
  - NumPy >= 1.26
  - OpenCV >= 4.10
  - OpenVINO == 2024.5
  - OpenVINO Model API == 0.2.5

To build:
```powershell
cd Deployment\EchoSight_Inference_GUI
.\build_installer.ps1
```

The script automatically installs all dependencies, builds the standalone executable, and outputs the portable folder.

---

## Supported Model Types

EchoSight works with any Geti OpenVINO deployment, including:
- **Detection**: Bounding box detection (YOLOv8, MobileNetV2-ATSS, etc.)
- **Instance Segmentation**: Pixel-level masks (MaskRCNN, etc.)
- **Anomaly Detection**: Anomaly classification with confidence scores

---

## Troubleshooting

**"Model load failed"**
- Verify the selected folder contains a valid Geti deployment (should have `Detection/`, `Instance Segmentation/`, or `Anomaly classification/` subdirectory)
- Check that `model.xml` and `config.json` are present in the model folder

**"No images loaded"**
- Supported formats: PNG, JPG, JPEG, BMP, TIFF, WebP
- Multi-frame TIFFs are automatically split into separate frames for processing

**"GPU not detected"**
- EchoSight uses CPU inference by default (bundled OpenVINO)
- GPU inference requires separate OpenVINO GPU plugin installation

---

## License

This application is provided as-is for research and development purposes.

- Run one image or all loaded images with a visible progress bar.
- Review every result in the Results tab.
- Results list rows show each frame's highest detection/anomaly score on the right; the highest-scoring frame is highlighted in pastel green.
- Toggle result labels on or off while retaining boxes or segmentation overlays.
- Toggle annotations independently from labels to inspect the unmarked source image or geometry without text.
- Adjust confidence filtering without rerunning inference.
- Set confidence from 1% to 100% using the percentage scale.
- Scroll-wheel zoom and click-drag pan in both preview and results viewers.
- Pastel-green highlighting for the result image with the highest confidence detection.
- Select one or more result images for export, or export the complete result set.
- Export the current annotated result or all results plus CSV metadata.
- Fixed-size Analyze and Results workspaces to prevent tab switching from resizing the window.
- Background model loading, image decoding, and inference with live top-right activity status.
- One top-right spinner glyph with elapsed-time status prevents duplicate "Loading images" messages.
- Run All pulses the progress bar while each frame is actively inside model inference and reports the current frame and elapsed time.
- Progress uses a determinate, smoothly eased fill from imported/inferred frame count instead of an indeterminate animation.
- Activity state is explicitly closed on completion, error, or cancellation so the spinner cannot remain running after inference finishes.
- Detection labels are measured and clamped to the image bounds so long labels remain fully visible.
- Model information uses wrapped rows sized to display the complete deployment summary without requiring scrolling.
- Run All, Run Current, and Cancel use distinct pastel colors with outlined controls; the selected Analyze or Results tab is visually emphasized.
- Action buttons use soft rounded edges with consistent hover, pressed, outline, and disabled states for a cohesive EchoSight surface.
- Model information panel with model name, version, task, labels, precision, size, record date, score, optimization, XAI-head status, and deployment status.

## Setup

Use the compatible Python 3.9 environment for the downloaded legacy Geti SDK package. The launcher uses staged OpenVINO 2024.5 packages; the main project environment uses Python 3.14 and is not compatible with this deployment wrapper.

From this folder:

```powershell
python -m pip install -r requirements.txt
```

The app discovers the downloaded package under:

```text
Deployment/Test_Run_Detect/deployment/Detection/model/
Deployment/Test_Run_Detect/deployment/Detection/python/
```

## Run

For a double-click launch from Windows Explorer, open:

```text
Launch_EchoSight.bat
```

The launcher uses the compatible Python 3.9 runtime and the currently staged OpenVINO 2024.5 packages at `C:\GetiCSAMInstallerBuild\site`. It expects this GUI folder to remain inside the project under `Deployment`. The final installer will replace this temporary runtime location with bundled files.

On normal launch, the GUI automatically searches for and loads `Deployment\Test_Run_Detect`. You do not need to select that folder yourself. Use **Load Model** only when switching to a different Geti deployment folder.

You can also launch from PowerShell:

```powershell
python .\EchoSight.py
```

Select `Deployment/Test_Run_Detect` when using the current download. The app uses the Geti deployment wrapper from the package so its preprocessing and postprocessing remain aligned with the exported model.

The initial confidence threshold is `10%` because the current model's sample detections are in the 10%-21% range. Raise or lower it in the Results tab to control which detections are shown; changing the threshold does not rerun inference. A model deployment does not always include the original training-image count; the GUI reports that field as unavailable rather than guessing.

The renderer accepts Geti detection, instance-segmentation, and anomaly result structures. Detection boxes remain supported through `objects` or array fields; instance masks are overlaid when the prediction exposes a `masks` array; anomaly models use `pred_mask`, `pred_label`, and `pred_score`. Labels can be hidden for unobstructed visual review without removing the underlying result data or export details.

The current `Deployment/Test_Run_Instance_Segmentation` package is actually an `AnomalyDetection` export under `deployment/Anomaly classification`. Its exported `config.json` has an empty task type, so the GUI normalizes that legacy metadata from `AnomalyDetection` to classification while preserving the anomaly mask output.

The portable package intentionally keeps the complete verified inference dependency set. This is packaging compatibility, not a percentage-based inference optimization. Runtime optimization should be measured against the same model and preprocessing contract before changing it.

## Portable folder build (deferred)

To create a copy/paste package containing Python, the complete verified OpenVINO/Geti inference dependencies, the model, GUI source, and launcher:

```powershell
.\\build_portable.ps1 -OutputRoot C:\\GetiCSAMPortable
```

Copy the resulting `C:\\GetiCSAMPortable` folder to another Windows machine and double-click `Launch_EchoSight.bat`. The builder intentionally preserves the full dependency set because the Geti wrapper has transitive runtime requirements; it excludes only PyInstaller build tools. It verifies the runtime, model API, GUI, launcher, and model files before reporting success.

Portable packaging is currently deferred while GUI behavior and representative model-output validation are prioritized. The build script is retained for later use.

## Current scope

This is a functional test GUI, not yet a production deployment package. It currently targets the downloaded detection deployment and CPU inference. Validate results against Geti before using it for engineering decisions.
