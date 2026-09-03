# Geti CSAM Inference GUI

First offline GUI prototype for running the downloaded Geti code deployment on images and multi-frame TIFF files.

Author: Omkar Kachare

## Features

- Dark theme with high-contrast controls.
- Select the downloaded deployment parent folder; the GUI discovers the model folder.
- Import common images and multi-frame TIFF files.
- Run one image or all loaded images with a visible progress bar.
- Review every result in the Results tab.
- Adjust confidence filtering without rerunning inference.
- Scroll-wheel zoom and click-drag pan in both preview and results viewers.
- Pastel-green highlighting for the result image with the highest confidence detection.
- Select one or more result images for export, or export the complete result set.
- Export the current annotated result or all results plus CSV metadata.
- Fixed-size Analyze and Results workspaces to prevent tab switching from resizing the window.
- Background model loading, image decoding, and inference with live top-right activity status.
- One top-right spinner glyph with elapsed-time status prevents duplicate "Loading images" messages.
- Run All pulses the progress bar while each frame is actively inside model inference and reports the current frame and elapsed time.
- Activity state is explicitly closed on completion, error, or cancellation so the spinner cannot remain running after inference finishes.
- Model information panel with model name, version, task, labels, precision, size, record date, score, optimization, XAI-head status, and deployment status.

## Setup

Use a Python 3.10 or 3.11 environment for the downloaded Geti SDK package. The exported package currently pins `geti-sdk==2.6.*`, while the main project environment uses Python 3.14.

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
Launch_Geti_CSAM_GUI.bat
```

The launcher uses the compatible Python 3.9 runtime and the currently staged OpenVINO 2024.5 packages at `C:\GetiCSAMInstallerBuild\site`. It expects this GUI folder to remain inside the project under `Deployment`. The final installer will replace this temporary runtime location with bundled files.

On normal launch, the GUI automatically searches for and loads `Deployment\Test_Run_Detect`. You do not need to select that folder yourself. Use **Load Model** only when switching to a different Geti deployment folder.

You can also launch from PowerShell:

```powershell
python .\geti_csam_inference_gui.py
```

Select `Deployment/Test_Run_Detect` when using the current download. The app uses the Geti deployment wrapper from the package so its preprocessing and postprocessing remain aligned with the exported model.

The initial confidence threshold is `0.10` because the current model's sample detections are in the 10%-21% range. Raise or lower it in the Results tab to control which detections are shown; changing the threshold does not rerun inference. A model deployment does not always include the original training-image count; the GUI reports that field as unavailable rather than guessing.

The portable package intentionally keeps the complete verified inference dependency set. This is packaging compatibility, not a percentage-based inference optimization. Runtime optimization should be measured against the same model and preprocessing contract before changing it.

## Portable folder build (deferred)

To create a copy/paste package containing Python, the complete verified OpenVINO/Geti inference dependencies, the model, GUI source, and launcher:

```powershell
.\\build_portable.ps1 -OutputRoot C:\\GetiCSAMPortable
```

Copy the resulting `C:\\GetiCSAMPortable` folder to another Windows machine and double-click `Launch_Geti_CSAM_GUI.bat`. The builder intentionally preserves the full dependency set because the Geti wrapper has transitive runtime requirements; it excludes only PyInstaller build tools. It verifies the runtime, model API, GUI, launcher, and model files before reporting success.

Portable packaging is currently deferred while GUI behavior and representative model-output validation are prioritized. The build script is retained for later use.

## Current scope

This is a functional test GUI, not yet a production deployment package. It currently targets the downloaded detection deployment and CPU inference. Validate results against Geti before using it for engineering decisions.
