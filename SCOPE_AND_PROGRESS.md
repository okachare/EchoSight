# Project Scope & Progress Report
**Project:** Geti AI-Assisted Defect Detection on NovaLake Product
**Tool:** Intel Geti™ on PVA SAM501 Confocal Scanning Acoustic Microscope (CSAM)
**Owner:** Omkar
**Project Start:** July 14, 2026
**Target Deadline:** End of Q3 2026 (September 30, 2026)
**Report Last Updated:** 2026-08-11

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
| 5. Debugging & Analysis | Review training logs, diagnose issues, improve dataset | 🟡 WIP |
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
├── Aug 2026 ─────── [NOW] Dataset organization, annotation, first training runs
│                              ↑ Currently here
├── Sep 2026 ─────── Fine-tuning, results analysis, demo preparation
│
└── Sep 30, 2026 ── DEMO DEADLINE
```

---

## Detailed Progress Log

### Phase 1 — Research & Setup
**Status:** 🟡 In Progress
**Duration:** 2026-08-11

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
| Define defect classes to detect | ⬜ Pending | — | e.g. void, delamination, crack — must be finalized before annotation proceeds |
| Perform initial CSAM scans of NovaLake samples | ✅ Done | ~2026-07-28 | NVL CSAM images captured on PVA SAM501 |
| Collect sufficient images for training (target: 50–200+) | ✅ Done | ~2026-07-28 | Dataset in hand and ready for processing |
| Convert CSAM .tiff output to PNG for Geti input | ✅ Done | ~2026-08-04 | Custom TiffSplitter tool engineered: GUI app with multi-format export, quality controls, and batch frame splitting |
| Verify TiffSplitter output integrity | ✅ Done | 2026-08-11 | Quantitative analysis performed: 8-bit source, 66 frames (517×281px), all outputs validated. PNG selected — lossless compression preserves acoustic scan contrast critical for defect detection |
| Organize images into dataset folder structure | 🟡 WIP | 2026-08-11 | Structuring into Geti-compatible format (COCO/VOC) |

### Phase 3 — Annotation
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Choose annotation type (bounding box vs. segmentation mask) | ⬜ Pending | — | Impacts model architecture choice and annotation effort — decision pending |
| Annotate images in Geti UI | 🟡 WIP | 2026-08-11 | Labeling underway using Geti’s built-in annotation tools |
| Review annotation quality | ⬜ Pending | — | Quality review gates training start |

### Phase 4 — Model Training
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Create Geti project with defect labels | 🟡 WIP | 2026-08-11 | Project created in Geti; label schema being refined alongside annotation |
| Select model architecture | ⬜ Pending | — | Candidates: YOLOX-S (speed) or RF-DETR (accuracy) — decision after annotation type confirmed |
| Run first training job | 🟡 WIP | 2026-08-11 | Initial training runs attempted on PVA SAM501 |
| Review training metrics | ⬜ Pending | — | Awaiting first stable run to complete |

### Phase 5 — Debugging & Analysis
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Copy Geti run logs to workspace | ⬜ Pending | — | Logs not yet dropped into workspace |
| Analyse training loss curves and accuracy | ⬜ Pending | — | Awaiting logs |
| Identify data or model issues | ⬜ Pending | — | Awaiting logs |

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
| 1 | What defect classes should be labeled? (voids, delamination, cracks, other?) | Defines the entire annotation and model scope |
| 2 | Detection (bounding boxes) or Segmentation (pixel masks)? | Affects model choice and annotation effort |
| 3 | How many labeled images can we collect before Q3 end? | Determines model quality ceiling |
| 4 | Will demo be live on SAM501 or on a separate machine? | Affects export/deployment approach |

### Challenges Faced
| # | Date | Challenge | Resolution |
|---|---|---|---|
| — | — | None yet — project just started | — |

### Current Roadblocks
| # | Roadblock | Severity | Action Required |
|---|---|---|---|
| — | None currently | — | — |

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
| **Current Phase** | Phases 2–5 — Data pipeline built, annotation and training active, debugging underway |
| **Next Milestone** | Logs dropped into workspace; first clean training run completed |
| **Demo Target** | September 30, 2026 |
| **Overall Status** | 🟡 On Track |

---

*Last updated: 2026-08-11 — Image integrity verified. TiffSplitter output cleared for Geti (PNG format recommended). Dataset organization next.*
