# Changelog

All notable changes to EchoSight are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-09-08

### Initial Release ✨

**First public release of EchoSight.**

#### Added
- **Core Features**
  - Standalone GUI application for running Geti OpenVINO model deployments
  - Support for Object Detection, Instance Segmentation, and Anomaly Detection models
  - Real-time model inference with background threading
  - Multi-format image import (PNG, JPG, BMP, WebP, TIFF)
  - Multi-frame TIFF support with automatic frame extraction

- **UI & Interaction**
  - Dark theme with professional high-contrast design
  - Soft-rounded button controls and customizable styling
  - Three-tab interface: Inference, Analysis, Results Review
  - Frame-by-frame navigation with Previous/Next controls
  - Canvas zoom and pan with scroll wheel and click-drag
  - Keyboard shortcuts (arrow keys, scroll navigation)

- **Image Processing**
  - Preprocessing filters: brightness, contrast, sharpness, denoising
  - Per-frame profile storage with applied-value badges
  - Scope control: apply to all frames, current frame, or selected frames
  - Original images preserved; processed copies used for inference
  - Interactive preview with zoom/pan preservation

- **Results Analysis**
  - Confidence threshold filtering (1-100%)
  - Independent annotation visibility toggles:
    - Show/hide detection boxes
    - Show/hide labels
    - Show/hide instance segmentation masks
  - Frame-by-frame confidence score display
  - Overall highest-confidence frame highlighting

- **Model Support**
  - Automatic Geti deployment structure discovery
  - Support for model.xml + model.bin architecture
  - Config.json parameter loading
  - Multi-task model detection (Detection/Segmentation/Anomaly)

- **Distribution & Installation**
  - Pre-built Windows portable package with bundled Python 3.9 runtime
  - Windows installer (.exe) for traditional installation
  - Pip-installable Python package for development
  - PyInstaller configuration for custom builds
  - Smart launcher batch script (auto-detects runtime)

- **Documentation**
  - Comprehensive README.md with features and quick start
  - Installation guide (4 methods: portable, installer, Python, custom build)
  - Detailed user guide with workflows and troubleshooting
  - Development guide for extending and contributing
  - Inline code documentation and docstrings

- **Development**
  - GitHub repository structure
  - .gitignore for Python/build artifacts
  - setup.py for pip installation
  - MIT License for open-source sharing

#### Technical Stack
- **UI Framework**: Tkinter (Python 3.9 standard library)
- **Image Processing**: OpenCV, Pillow, NumPy
- **AI Inference**: OpenVINO 2024.5
- **Build**: PyInstaller
- **Python Version**: 3.9 (exact requirement for OpenVINO 2024.5)

#### Known Limitations
- Windows only (Tkinter cross-platform possible in future)
- CPU inference only (GPU support can be enabled in code)
- Maximum TIFF file size depends on available RAM
- Model must be exported from Intel Geti platform

#### Testing
- ✓ Detection model inference verified
- ✓ Instance Segmentation model inference verified
- ✓ Anomaly Detection model inference verified
- ✓ Image preprocessing pipeline verified
- ✓ Multi-frame TIFF import verified
- ✓ Portable build and execution verified
- ✓ Installer build and execution verified

---

## Future Roadmap

### v1.1.0 (Planned)
- [ ] Export results to CSV/JSON
- [ ] Result batch download
- [ ] GPU inference support toggle
- [ ] Custom confidence threshold presets
- [ ] Model configuration editor UI

### v1.2.0 (Planned)
- [ ] Linux/macOS support
- [ ] Batch processing from command line
- [ ] REST API for remote inference
- [ ] Advanced image enhancement filters
- [ ] Model performance benchmarking

### v2.0.0 (Planned)
- [ ] Multi-model ensemble inference
- [ ] Real-time camera feed support
- [ ] Custom model training integration
- [ ] Result annotation and labeling tools
- [ ] Plug-in architecture for extensions

---

## Version History Format

```
## [Semantic Version] - YYYY-MM-DD

### Category (Added/Fixed/Changed/Removed/Deprecated/Security)

- Brief description of change
- Related issues/PRs if applicable
```

---

**Legend**:
- ✨ New feature
- 🐛 Bug fix
- 📝 Documentation
- 🔧 Configuration/Build
- ⚡ Performance improvement
- 🎨 UI/UX improvement

---

For detailed commit history, see [GitHub Commits](https://github.com/okachare/EchoSight/commits/main)

For issues and feature requests, see [GitHub Issues](https://github.com/okachare/EchoSight/issues)
