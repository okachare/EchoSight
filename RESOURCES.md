# Geti — Resources & Reference

## Official Links
| Resource | URL |
|---|---|
| Documentation | https://docs.geti.intel.com/docs/user-guide/getting-started/introduction |
| GitHub Repository | https://github.com/open-edge-platform/geti |
| getitune (PyPI) | https://pypi.org/project/getitune/ |
| Quick Start Guide | https://docs.geti.intel.com/docs/user-guide/quick-start/training-your-first-model |
| Installation Guide | https://docs.geti.intel.com/docs/user-guide/getting-started/installation/installation-guide |
| getitune Library Docs | https://docs.geti.intel.com/docs/user-guide/library/get-started/intro |

---

## Installation Options (Windows)

### Option 1 — Windows MSIX App (Simplest, Recommended to Start)
Download and double-click the `.msix` installer:
- CPU-only: https://storage.geti.intel.com/geti/packages/3.0.0/geti-cpu-3.0.0.msix
- Intel XPU: https://storage.geti.intel.com/geti/packages/3.0.0/geti-xpu-3.0.0.msix
- NVIDIA CUDA: https://storage.geti.intel.com/geti/packages/3.0.0/geti-cuda-3.0.0.msix

> Note: Windows MSIX does NOT include Ultralytics YOLO models (AGPL licensing). For most CSAM use cases this is fine.

### Option 2 — PowerShell Install Script (Builds from Source)
```powershell
irm https://raw.githubusercontent.com/open-edge-platform/geti/develop/install.ps1 | iex
```
Or with options:
```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/open-edge-platform/geti/develop/install.ps1))) -Yes -WorkDir C:\geti
```

### Option 3 — Docker (Requires WSL2 + Ubuntu 24+)
```bash
docker pull ghcr.io/open-edge-platform/geti-cpu
docker tag ghcr.io/open-edge-platform/geti-cpu:latest geti-cpu:latest
just run-image --accelerator cpu
```

### System Requirements
| Component | Minimum |
|---|---|
| CPU | 8 threads |
| RAM | 16 GB |
| Disk | 40 GB free |
| GPU | Optional (Intel XPU or NVIDIA) |

After installation, access the app at: **https://localhost:7860**

---

## Geti Repository Structure

```
geti/
├── library/               ← getitune Python package (training engine)
│   └── src/getitune/
│       └── recipe/        ← YAML recipes per task
│           ├── classification/
│           ├── detection/
│           ├── instance_segmentation/
│           ├── semantic_segmentation/
│           └── keypoint_detection/
├── application/
│   ├── backend/           ← FastAPI server (Python 3.13)
│   │   └── app/
│   │       ├── api/routers/    ← REST endpoints
│   │       ├── services/       ← business logic
│   │       ├── repositories/   ← data access (SQLite)
│   │       └── execution/      ← training/export jobs (runs out-of-process)
│   ├── ui/                ← React 19 + TypeScript frontend
│   └── docs/              ← install.md, upgrade.md, api.md
└── skills/                ← agent skill definitions
    ├── library/           ← getitune-training, preparing-datasets, exporting, etc.
    └── application/       ← geti-using-the-pipeline, backend-dev, ui-dev
```

---

## Supported CV Tasks & Models

### Classification (whole image → label)
| Model | Notes |
|---|---|
| EfficientNet B0 / B3 | Good baseline, fast |
| ViT Tiny | Vision Transformer |
| DINOv2 Small | Self-supervised, strong features |
| MobileNet V3 Large | Lightweight edge deployment |
| YOLO26 N/S/M/L/X | Latest YOLO for classification |

### Object Detection (bounding boxes)
| Model | Notes |
|---|---|
| YOLOX Tiny/S/L/X | Fast, good for small objects |
| RF-DETR N/S/M/L | Transformer-based, high accuracy |
| D-FINE M/L/X | Strong detection baseline |
| YOLO11/12/26 variants | Latest generation YOLO |
| MobileNetV2 ATSS/SSD | Lightweight |

### Instance Segmentation (per-defect masks)
| Model | Notes |
|---|---|
| Mask-RCNN R50 / SwinT / EffNetB2 | Classic + modern backbones |
| RTMDet Tiny | Fast instance segmentation |
| RF-DETR-Seg N/S/M/L/XL | High accuracy |
| YOLO11/26-Seg | Latest YOLO segmentation |

### Semantic Segmentation (pixel-level class map)
| Model | Notes |
|---|---|
| DINOv2 | Best features, slower |
| LiteHRNet S/18/X | Lightweight, real-time |
| SegNeXt T/S/B | Strong balanced option |
| YOLO26 Sem | Fast semantic seg |

> **Tiling (`_tile` suffix recipes)**: Automatically splits large images into overlapping tiles for training and inference. **Critical for high-resolution CSAM images.**

---

## Dataset Formats Supported

| Format | Detection Marker |
|---|---|
| COCO | `annotations/` directory with JSON files |
| YOLO (Ultralytics) | `data.yaml` file |
| Pascal VOC | `JPEGImages/`, `Annotations/`, `ImageSets/` directories |
| Datumaro (native) | `metadata.json` + `data.parquet` at root |
| Zip archives | Automatically extracted on import |

**Recommendation for CSAM project**: Use **COCO format** — most annotation tools (CVAT, LabelMe, Roboflow) export to it, and it handles complex polygon/bbox annotations well.

---

## Core Python API (getitune library)

```python
from getitune.engine import create_engine
from getitune.utils import list_models
from getitune.types import ExportFormat, ExportPrecision

# 1. Discover available models
all_models = list_models()
detection_models = list_models(task="DETECTION")

# 2. Train
engine = create_engine(
    model="yolox_s",              # model name or recipe .yaml path
    data="/path/to/dataset",      # dataset root (format auto-detected)
    work_dir="./csam_workspace",
    device="auto",                # auto / cpu / gpu / xpu
)
engine.train(max_epochs=50)
engine.test()                     # evaluate on test split

# 3. Export to OpenVINO IR (for deployment)
ov_path = engine.export()         # returns .xml path

# 4. Load exported model and quantize (INT8, faster inference)
ov_engine = create_engine(model=ov_path, data="/path/to/dataset")
ov_engine.optimize()              # NNCF post-training quantization
ov_engine.test()

# 5. Run inference / predict
predictions = ov_engine.predict()
```

---

## Application REST API Flow (when using the GUI)

```
POST   /api/projects                          ← create project (task + labels)
POST   /api/projects/<id>/dataset/media       ← upload CSAM images
POST   /api/projects/<id>/dataset/media/<id>/annotations  ← add annotations
POST   /api/staged_datasets                   ← OR: import existing dataset archive
POST   /api/jobs  { type: "train" }           ← start async training job
GET    /api/jobs/<id>                         ← poll job status
POST   /api/jobs  { type: "quantize" }        ← optional INT8 quantization
POST   /api/sources                           ← define input source
POST   /api/sinks                             ← define output sink
PATCH  /api/projects/<id>/pipeline           ← wire source → model → sink
POST   /api/projects/<id>/pipeline:enable    ← start live inference
GET    /api/projects/<id>/pipeline/metrics   ← latency, throughput
```

---

## Ecosystem Tools Used Internally
| Tool | Role |
|---|---|
| OpenVINO | Model optimization and deployment |
| NNCF | INT8 post-training quantization |
| Datumaro | Dataset format detection and conversion |
| PyTorch Lightning | Training backend |
| SQLite | Backend database (projects, media, models) |
| FastAPI | REST API server |

---

*Last updated: 2026-08-11*
