# Project Scope & Progress Report
**Project:** Geti AI-Assisted Defect Detection on NovaLake Product
**Tool:** Intel Geti™ on PVA SAM501 Confocal Scanning Acoustic Microscope (CSAM)
**Owner:** Omkar
**Project Start:** July 14, 2026
**Target Deadline:** End of Q3 2026 (September 30, 2026)
**Report Last Updated:** 2026-08-12

---

## Executive Summary

This project evaluates Intel Geti™ — an end-to-end Vision AI platform — as a tool for automated defect detection in acoustic microscopy scans of the **NovaLake product**. The work encompasses the full AI model development lifecycle: tool research and qualification, custom data pipeline engineering, dataset preparation, model training, iterative debugging, and deployment for live inference on the PVA SAM501 CSAM tool.

The end goal is a live demonstration showing Geti's ability to identify and classify defects (such as voids, delamination, and cracks) directly from CSAM scan images — reducing reliance on manual inspection and establishing a repeatable AI-assisted quality workflow for NovaLake.

---

## Objective

> **Demo Geti's defect detection capability on NovaLake product scans by end of Q3 2026.**

A successful demo will show:
- Geti trained on real NovaLake CSAM images
- Model correctly identifying and localizing defects
- Inference running on the PVA SAM501 hardware
- Quantitative results (accuracy, detection rate) presented to management

---

## Scope of Work

| Phase | Description | Status |
|---|---|---|
| 1. Research & Setup | Literature review, tool evaluation, installation | ✅ Complete |
| 2. Data Collection | Acquire and organize NovaLake CSAM scan images | 🟡 WIP |
| 3. Annotation | Label defects in images using Geti's annotation tools | 🟡 WIP |
| 4. Model Training | Train initial defect detection model in Geti | 🟡 WIP |
| 5. Debugging & Analysis | Review training logs, diagnose issues, improve dataset | ✅ Complete |
| 6. Fine-tuning | Iterate on model with improved labels/data/hyperparameters | ⬜ Not Started |
| 7. Results Analysis | Evaluate final model metrics; prepare demo materials | ⬜ Not Started |
| 8. Demo | Present live defect detection on NovaLake scans to management | ⬜ Not Started |

---

## Timeline

```
Q3 2026 (Jul – Sep)
│
├── Jul 14, 2026 ─── Project kicked off
│
├── Jul 14–Aug 11 ── Research, tool evaluation, installation, data pipeline
│                    TiffSplitter built, images collected & verified
│
├── Aug 11, 2026 ─── Training logs collected & analysed. Root cause identified:
│                    "No object" images in val split → empty bbox crash.
│
├── Aug 12, 2026 ─── Root cause fixed. First clean training run completed.
│                    RF-DETR-Seg-M, 5 images, 1% mAP (smoke test).
│                    Pipeline proven end-to-end. OpenVINO FP16 export: 66 MB.
│
├── Aug 2026 ─────── [NOW] Model evaluation & inference learning → scale up dataset
│                              ↑ Currently here
├── Sep 2026 ─────── Fine-tuning, results analysis, demo preparation
│
└── Sep 30, 2026 ── DEMO DEADLINE
```

---

## Detailed Progress Log

### Phase 1 — Research & Setup
**Status:** ✅ Complete
**Duration:** 2026-07-14 – 2026-08-11

| Task | Status | Date | Notes |
|---|---|---|---|
| Identify suitable AI tool for CSAM analysis | ✅ Done | 2026-07-14 | Evaluated Intel Geti™ — selected for its no-code training UI, OpenVINO-optimized inference, and tiling support for large images |
| Review Geti documentation | ✅ Done | 2026-07-14 | Full user guide reviewed: docs.geti.intel.com |
| Review Geti GitHub repository | ✅ Done | 2026-07-14 | Full repo review: architecture, supported models, dataset formats, deployment pipeline |
| Understand Geti architecture and capabilities | ✅ Done | 2026-07-14 | Identified optimal task types (detection/segmentation) and tiling pipeline for high-res CSAM scans |
| Install Geti on CSAM hardware | ✅ Done | ~2026-07-21 | Successfully deployed on PVA SAM501; application launches and is operational |
| Set up analysis workspace and version control | ✅ Done | 2026-08-11 | GitHub repo created (private), workspace linked as debug/analysis interface |

### Phase 2 — Data Collection
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Define defect classes to detect | 🟡 WIP | 2026-08-12 | Starting with `delamination` only for smoke test; additional classes (void, crack) to be added for full NVL run |
| Perform initial CSAM scans of NovaLake samples | ✅ Done | ~2026-07-28 | NVL CSAM images captured on PVA SAM501 |
| Collect sufficient images for training (target: 50–200+) | ✅ Done | ~2026-07-28 | Dataset in hand and ready for processing |
| Convert CSAM .tiff output to PNG for Geti input | ✅ Done | ~2026-08-04 | Custom TiffSplitter tool engineered: GUI app with multi-format export, quality controls, and batch frame splitting |
| Verify TiffSplitter output integrity | ✅ Done | 2026-08-11 | Quantitative analysis performed: 8-bit source, 66 frames (517×281px), all outputs validated. PNG selected — lossless compression preserves acoustic scan contrast critical for defect detection |
| Organize images into dataset folder structure | ✅ Done | 2026-08-12 | Images uploaded directly into Geti project — Geti manages internal dataset structure |

### Phase 3 — Annotation
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Choose annotation type (bounding box vs. segmentation mask) | ✅ Done | 2026-08-12 | **Instance Segmentation (polygon masks)** selected — better captures irregular defect shapes |
| Annotate images in Geti UI | 🟡 WIP | 2026-08-12 | 5 images annotated for smoke test; full NVL dataset annotation pending |
| Review annotation quality | 🟡 WIP | 2026-08-12 | Smoke test annotations confirmed valid; full quality review pending for NVL dataset |

### Phase 4 — Model Training
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Create Geti project with defect labels | ✅ Done | 2026-08-12 | New project created: Instance Segmentation, single class `delamination` |
| Select model architecture | ✅ Done | 2026-08-12 | **RF-DETR-Seg-M** selected — balanced speed/accuracy, OpenVINO-optimized |
| Run first training job | ✅ Done | 2026-08-12 | First clean run completed — 5 images, CPU, ~37 min, 705 MB model, OpenVINO FP16 export 66 MB |
| Review training metrics | 🟡 WIP | 2026-08-12 | Smoke test mAP@0.5: ~1% — expected with 5 images; meaningful metrics require full NVL dataset |

### Phase 5 — Debugging & Analysis
**Status:** ✅ Complete
**Duration:** 2026-08-11 – 2026-08-12

| Task | Status | Date | Notes |
|---|---|---|---|
| Copy Geti run logs to workspace | ✅ Done | 2026-08-11 | 12 failed logs in `Debug/Run081125/jobs/`; Run081226 logs in `Debug/Run081226/` |
| Analyse training loss curves and accuracy | ✅ Done | 2026-08-12 | Root cause identified and fixed; first successful run metrics captured (smoke test) |
| Identify data or model issues | ✅ Done | 2026-08-12 | Root cause: `"No object"` images in val/test split produce empty bbox tensors → crash. Fix: all images in every split must have at least one annotated shape |

### Phase 6 — Fine-tuning
**Status:** ⬜ Not Started

| Task | Status | Date | Notes |
|---|---|---|---|
| Improve annotations or add more data | ⬜ Pending | — | |
| Adjust model/hyperparameters | ⬜ Pending | — | |
| Re-train and compare metrics | ⬜ Pending | — | |

### Phase 7 — Results Analysis
**Status:** ⬜ Not Started

| Task | Status | Date | Notes |
|---|---|---|---|
| Document final model performance | ⬜ Pending | — | |
| Prepare visual examples of detections | ⬜ Pending | — | |
| Prepare demo presentation materials | ⬜ Pending | — | |

### Phase 8 — Demo
**Status:** ⬜ Not Started

| Task | Status | Date | Notes |
|---|---|---|---|
| Run live inference on new NovaLake scans | ⬜ Pending | — | |
| Present results to management | ⬜ Pending | — | Target: Sep 30, 2026 |

---

## Challenges & Decisions

### Open Decisions
| # | Decision Needed | Impact |
|---|---|---|
| 1 | What defect classes to include beyond `delamination` for full NVL run? (voids, cracks?) | Defines annotation scope and label schema for Phase 3 rework |
| 2 | How many labeled images can we collect before Q3 end? | Determines model quality ceiling — target 50–200+ |
| 3 | Will demo be live on SAM501 or on a separate machine? | Affects export/deployment approach |
| 4 | How to correctly include "No object" / clean images in training? | Needs investigation — current workaround is defect-only dataset |

### Challenges Faced
| # | Date | Challenge | Resolution |
|---|---|---|---|
| 1 | 2026-07-24 – 2026-08-12 | 13 training runs failed with `ValueError: Boxes batch must have 4 coordinates` — getitune cannot handle `"No object"` annotations in the val/test split for instance segmentation; empty bbox tensors fail internal validation | **Resolved 2026-08-12** — new project with defect-only images; all images in every split have at least one polygon mask; first clean run completed |

### Current Roadblocks
| # | Roadblock | Severity | Action Required |
|---|---|---|---|
| 1 | **Smoke test mAP ~1%** — 5-image dataset too small for meaningful accuracy | 🟡 Medium — expected; does not block progress | Scale up to 50+ annotated NVL images for real training run |
| 2 | **"No object" / clean images cannot currently be used** — getitune crashes when empty-annotation images land in val/test split | 🟡 Medium — workaround in place | Investigate if getitune has a fix/config for this; or keep negative examples out until resolved |

---

## Key Resources

| Resource | Link |
|---|---|
| Intel Geti Documentation | https://docs.geti.intel.com |
| Geti GitHub Repository | https://github.com/open-edge-platform/geti |
| getitune Python Library (PyPI) | https://pypi.org/project/getitune/ |
| Geti Installation Guide | https://docs.geti.intel.com/docs/user-guide/getting-started/installation/installation-guide |
| Detailed Resources File | [RESOURCES.md](./RESOURCES.md) |
| Technical Status Log | [PROJECT_STATUS.md](./PROJECT_STATUS.md) |

---

## Summary for Management

| Item | Detail |
|---|---|
| **Project Goal** | Demonstrate AI-based defect detection on NovaLake CSAM scans |
| **Tool** | Intel Geti™ (open-source, Apache 2.0) |
| **Hardware** | PVA SAM501 CSAM tool |
| **Current Phase** | Phases 3–4 — Smoke test complete; learning model evaluation & inference; scaling up to full NVL dataset |
| **Next Milestone** | Learn Geti model evaluation + inference → annotate 50+ NVL images → first real training run |
| **Demo Target** | September 30, 2026 |
| **Overall Status** | 🟡 On Track |

---

*Last updated: 2026-08-12 — First successful training run completed. RF-DETR-Seg-M, 5 defect images (delamination), CPU, ~37 min, mAP@0.5 ~1% (smoke test). OpenVINO FP16 export generated (66 MB). Pipeline proven end-to-end. Next: learn model evaluation & inference in Geti, then scale up to full NVL dataset.*
