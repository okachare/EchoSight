# EchoSight

**Model-agnostic image inference and inspection**

A standalone, portable GUI application for running Intel Geti OpenVINO model deployments on images and multi-frame TIFF files. Features real-time inference, confidence filtering, image preprocessing, and comprehensive results navigation.

![Platform: Windows](https://img.shields.io/badge/platform-Windows-blue)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-green)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)

---

## Quick Start

### Option 1: Pre-built Executable (Recommended)

1. Download the latest release from [GitHub Releases](https://github.com/okachare/EchoSight/releases)
2. Extract `EchoSight-portable.zip` or run `EchoSight-installer.exe`
3. Launch `EchoSight.exe` or double-click `Launch_EchoSight.bat`
4. Click **Load Model** and select your Geti deployment folder
5. Start analyzing!

### Option 2: Python Development Install

Requires **Python 3.9** and **pip**:

```powershell
git clone https://github.com/okachare/EchoSight.git
cd EchoSight
pip install -e .
python src/echosight/EchoSight.py
```

### Option 3: Build Your Own Executable

```powershell
cd build
.\build_portable.ps1   # Creates portable package with bundled Python
# or
.\build_installer.ps1  # Creates Windows installer
```

---

## Features

✨ **Standalone & Portable**: All dependencies bundled; runs on Windows without Python installation

🎨 **Dark Theme UI**: Professional interface with high-contrast controls and soft rounded buttons

🔍 **Smart Model Discovery**: Automatically finds `model.xml` and `config.json` in deployment folder structure

📁 **Multi-Format Import**: Supports PNG, JPG, BMP, WebP, and multi-frame TIFF files

⚡ **Real-Time Inference**: Background threading keeps UI responsive during model predictions

🎚️ **Confidence Filtering**: Adjustable 1%-100% confidence threshold for detection results

🖼️ **Image Preprocessing**: Optional brightness, contrast, sharpness, and denoising:
  - Apply to all frames, current frame, or selected frames
  - Original images preserved; preprocessed copies used for inference
  - Per-frame profile storage and preview preservation

📊 **Results Review**: Navigate frame-by-frame with Previous/Next buttons

🔬 **Annotation Controls**: Toggle detection boxes, labels, and instance masks independently

🖱️ **Interactive Canvas**: Zoom and pan detection overlays with intuitive controls

---

## System Requirements

- **OS**: Windows 10 or later
- **RAM**: Minimum 4GB (8GB+ recommended for large models)
- **Disk**: 2-3GB for portable package (includes Python 3.9 runtime)
- **GPU**: Optional (uses OpenVINO CPU inference by default)

---

## Supported Model Types

- **Object Detection** (bounding boxes)
- **Instance Segmentation** (pixel masks)
- **Anomaly Detection** (classification + heatmaps)

Models must be exported from Intel Geti with the following folder structure:

```
my-deployment/
├── Detection/              # or Instance Segmentation, Anomaly classification
│   └── model/
│       ├── model.xml
│       ├── model.bin
│       └── config.json
└── python/                 # (optional wrapper)
    └── (model_api modules)
```

---

## Usage

### Loading a Model

1. Click **Load Model** button
2. Navigate to your Geti deployment parent folder
3. EchoSight automatically discovers the model structure
4. Model loads and displays configuration

### Running Inference

1. Click **Load Images** to import PNG, JPG, BMP, WebP, or TIFF files
2. Click **Run All** to process all frames
3. Or click **Run Current** to process the active frame only
4. Watch progress in the status bar
5. Navigate results with Previous/Next buttons

### Image Preprocessing

1. Click the **gear icon** (⚙️) in the Analyze tab
2. Adjust brightness, contrast, sharpness, denoiser
3. Choose scope: **All Frames**, **Current Frame**, or **Selected Frames**
4. Click **Apply Processing**
5. Original images remain unchanged; inference uses preprocessed versions

### Results Analysis

- **Confidence Threshold**: Slide 1-100% to filter detections
- **Show Detections**: Toggle detection boxes on/off
- **Show Labels**: Toggle label text on/off
- **Show Masks**: Toggle instance segmentation masks on/off
- **Zoom/Pan**: Scroll to zoom; click-drag to pan the canvas

---

## Documentation

- **[INSTALL.md](INSTALL.md)** — Detailed installation steps and troubleshooting
- **[USAGE.md](USAGE.md)** — Complete user guide with workflows and examples
- **[DEVELOPMENT.md](DEVELOPMENT.md)** — Development setup, build instructions, and contribution guidelines

---

## Architecture

```
EchoSight.py
├── ModelLoader       → Discovers & loads Geti deployment structure
├── InferenceEngine   → Runs OpenVINO predictions in background thread
├── PreprocessingPipeline → Image filtering (brightness, contrast, etc.)
├── ResultRenderer    → Draws detection boxes, masks, labels
├── CanvasManager     → Zoom/pan controls
└── UI Components     → Tabs, buttons, progress tracking
```

---

## Troubleshooting

### "Model not found" Error
- Ensure your Geti deployment folder contains `Detection/`, `Instance Segmentation/`, or `Anomaly classification/` subfolder
- Check that `model.xml` exists in the model subfolder

### Slow Inference
- GPU inference not enabled by default (uses CPU)
- To use GPU, modify OpenVINO device in code or set environment variable

### TIFF Not Recognized
- Ensure multi-frame TIFF is valid (verify with image viewer)
- Some compressed TIFF formats may not be supported; try converting to PNG

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

---

## Citation

If you use EchoSight in your research or work, please cite:

```bibtex
@software{echosight2026,
  title={EchoSight: Model-agnostic Image Inference and Inspection},
  author={Kachare, Omkar},
  year={2026},
  url={https://github.com/okachare/EchoSight}
}
```

---

## Support

- 📧 Issues & Questions: [GitHub Issues](https://github.com/okachare/EchoSight/issues)
- 📚 Documentation: See [USAGE.md](USAGE.md) and [DEVELOPMENT.md](DEVELOPMENT.md)
- 💡 Tips & Tricks: Check [Discussions](https://github.com/okachare/EchoSight/discussions)

---

**Made with ❤️ by Omkar Kachare**
