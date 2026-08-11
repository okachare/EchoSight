# Project Scope & Progress Report
**Project:** Geti AI-Assisted Defect Detection on NovaLake Product
**Tool:** Intel Geti™ on PVA SAM501 Confocal Scanning Acoustic Microscope (CSAM)
**Owner:** Omkar
**Target Deadline:** End of Q3 2026 (September 30, 2026)
**Report Last Updated:** 2026-08-11

---

## Executive Summary

This project evaluates Intel Geti™ — an end-to-end Vision AI platform — as a tool for automated defect detection in acoustic microscopy scans of the **NovaLake product**. The end goal is a live demonstration showing Geti's ability to identify and classify defects (such as voids, delamination, and cracks) directly from CSAM scan images, reducing reliance on manual inspection.

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
├── Jul 2026 ─── Research, tool evaluation, installation
│
├── Aug 2026 ─── [NOW] Data collection, annotation, first training run
│                       ↑ Currently here
├── Sep 2026 ─── Fine-tuning, results analysis, demo preparation
│
└── Sep 30, 2026 ─── DEMO DEADLINE
```

---

## Detailed Progress Log

### Phase 1 — Research & Setup
**Status:** 🟡 In Progress
**Duration:** 2026-08-11 → ongoing

| Task | Status | Date | Notes |
|---|---|---|---|
| Identify suitable AI tool for CSAM analysis | ✅ Done | 2026-08-11 | Selected Intel Geti™ |
| Review Geti documentation | ✅ Done | 2026-08-11 | Docs: docs.geti.intel.com |
| Review Geti GitHub repository | ✅ Done | 2026-08-11 | github.com/open-edge-platform/geti |
| Understand Geti architecture and capabilities | ✅ Done | 2026-08-11 | Both GUI and Python library modes understood |
| Install Geti on CSAM hardware | ✅ Done | 2026-08-11 | Running on PVA SAM501, launches successfully |
| Set up analysis workspace | ✅ Done | 2026-08-11 | This workspace acts as debug/analysis interface |

### Phase 2 — Data Collection
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Define defect classes to detect | ⬜ Pending | — | e.g. void, delamination, crack |
| Perform initial CSAM scans of NovaLake samples | ✅ Done | 2026-08-11 | NVL CSAM images collected |
| Collect sufficient images for training (target: 50–200+) | ✅ Done | 2026-08-11 | Images in hand |
| Convert CSAM .tiff output to JPEG for Geti input | ✅ Done | 2026-08-11 | Custom script written and working |
| Organize images into dataset folder structure | 🟡 WIP | 2026-08-11 | Organization in progress |

### Phase 3 — Annotation
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Choose annotation type (bounding box vs. segmentation mask) | ⬜ Pending | — | Decision still needed |
| Annotate images in Geti UI | 🟡 WIP | 2026-08-11 | Annotation in progress |
| Review annotation quality | ⬜ Pending | — | |

### Phase 4 — Model Training
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Create Geti project with defect labels | 🟡 WIP | 2026-08-11 | In progress alongside annotation |
| Select model architecture | ⬜ Pending | — | Likely YOLOX or RF-DETR for detection |
| Run first training job | 🟡 WIP | 2026-08-11 | Training runs being attempted |
| Review training metrics | ⬜ Pending | — | Awaiting stable run completion |

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
| **Current Phase** | Phases 2–5 — Data collection, annotation, training, debugging (all WIP) |
| **Next Milestone** | Logs dropped into workspace; first clean training run completed |
| **Demo Target** | September 30, 2026 |
| **Overall Status** | 🟡 On Track |

---

*Last updated: 2026-08-11 — NVL CSAM images collected. Custom TIFF→JPEG conversion script written. Data organization, annotation, model training, and debugging all WIP. Geti running on PVA SAM501. Awaiting first run logs to be dropped into workspace.*
