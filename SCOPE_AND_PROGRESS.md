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
| 2. Data Collection | Acquire and organize NovaLake CSAM scan images | ✅ Complete |
| 3. Annotation | Label defects in images using Geti's annotation tools | 🟡 WIP |
| 4a. NVL Test Run — Training | Train RF-DETR-Seg-M on 20 NVL images (`anomaly`) | ⬜ Planned |
| 4b. NVL Test Run — Inference | Evaluate model; run predictions on new NVL images | ⬜ Planned |
| 4c. NVL Test Run — Fine-tuning | Iterate: improve annotations, add data, retrain | ⬜ Planned |
| 5. Debugging & Analysis | Review training logs, diagnose issues, improve dataset | ✅ Complete |
| 6. Results Analysis | Evaluate final model metrics; prepare demo materials | ⬜ Not Started |
| 7. Demo | Present live defect detection on NovaLake scans to management | ⬜ Not Started |

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
├── Aug 16–17, 2026 ─ **NVL Test Run** — 20 NVL images, temporary `anomaly` class
│                    Training → Inference → Fine-tuning
│
├── Aug 2026 ─────── [NOW] Annotating 20 NVL images → NVL Test Run start
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
**Status:** ✅ Complete
**Duration:** 2026-07-28 – 2026-08-12

| Task | Status | Date | Notes |
|---|---|---|---|
| Define defect classes to detect | 🟡 WIP | 2026-08-14 | Using temporary `anomaly` label for first real run; map to final classes (delamination, void, crack) later |
| Perform initial CSAM scans of NovaLake samples | ✅ Done | ~2026-07-28 | NVL CSAM images captured on PVA SAM501 |
| Collect sufficient images for training (target: 50–200+) | ✅ Done | 2026-08-12 | 20 NVL images selected from the collected and organised dataset; ready for annotation |
| Convert CSAM .tiff output to PNG for Geti input | ✅ Done | ~2026-08-04 | Custom TiffSplitter tool engineered: GUI app with multi-format export, quality controls, and batch frame splitting |
| Verify TiffSplitter output integrity | ✅ Done | 2026-08-11 | Quantitative analysis performed: 8-bit source, 66 frames (517×281px), all outputs validated. PNG selected — lossless compression preserves acoustic scan contrast critical for defect detection |
| Organize images into dataset folder structure | ✅ Done | 2026-08-12 | Images upload directly into Geti project — no external folder structure needed |

### Phase 3 — Annotation
**Status:** 🟡 WIP

| Task | Status | Date | Notes |
|---|---|---|---|
| Choose annotation type (bounding box vs. segmentation mask) | ✅ Done | 2026-08-12 | **Instance Segmentation (polygon masks)** selected — better captures irregular defect shapes |
| Annotate images in Geti UI | 🟡 WIP | 2026-08-12 | 5 images annotated for smoke test; full NVL dataset annotation pending |
| Review annotation quality | 🟡 WIP | 2026-08-12 | Smoke test annotations confirmed valid; full quality review pending for NVL dataset |

### Phase 4a — NVL Test Run: Training
**Status:** ⬜ Planned (weekend 2026-08-16/17)

| Task | Status | Date | Notes |
|---|---|---|---|
| Upload 20 NVL defect images to Geti | ⬜ Pending | — | All defect images; no clean/"No object" images for this run |
| Annotate all 20 images with `anomaly` polygon masks | ✅ Done | 2026-08-14 | 20/20 submitted; approximately 39 minutes (10:32–11:11) |
| Train Mask R-CNN Swin-T (70/20/10 split, all Unassigned) | 🟡 WIP | 2026-08-14 | Started approximately 11:18; batch size 4, 200 epochs, early stopping, CPU; utilization monitoring active |
| Collect and analyse training log | ⬜ Pending | — | Drop log into `Debug/RunNVL01/` |

### Phase 4b — NVL Test Run: Inference
**Status:** ⬜ Planned

| Task | Status | Date | Notes |
|---|---|---|---|
| Review model metrics in Geti (mAP, precision, recall) | ⬜ Pending | — | Baseline performance on 20-image dataset |
| Run predictions on new unseen NVL images | ⬜ Pending | — | Use Geti Annotate → Predict on images not in training set |
| Review prediction quality visually | ⬜ Pending | — | Are masks landing on real anomalies? Any false positives? |

### Phase 4c — NVL Test Run: Fine-tuning
**Status:** ⬜ Planned

| Task | Status | Date | Notes |
|---|---|---|---|
| Accept/correct/reject Geti predictions to expand dataset | ⬜ Pending | — | Use predict-review-correct loop to build annotations faster |
| Add more NVL images if mAP is low | ⬜ Pending | — | Target 50–100+ annotated images for meaningful accuracy |
| Retrain and compare mAP vs baseline | ⬜ Pending | — | Iterate until model quality is demo-ready |

### Phase 5 — Debugging & Analysis
**Status:** ✅ Complete
**Duration:** 2026-08-11 – 2026-08-12

| Task | Status | Date | Notes |
|---|---|---|---|
| Copy Geti run logs to workspace | ✅ Done | 2026-08-11 | 12 failed logs in `Debug/Run081125/jobs/`; Run081226 logs in `Debug/Run081226/` |
| Analyse training loss curves and accuracy | ✅ Done | 2026-08-12 | Root cause identified and fixed; first successful run metrics captured (smoke test) |
| Identify data or model issues | ✅ Done | 2026-08-12 | Root cause: `"No object"` images in val/test split produce empty bbox tensors → crash. Fix: all images in every split must have at least one annotated shape |

### Phase 6 — Results Analysis
**Status:** ⬜ Not Started

| Task | Status | Date | Notes |
|---|---|---|---|
| Document final model performance | ⬜ Pending | — | |
| Prepare visual examples of detections | ⬜ Pending | — | |
| Prepare demo presentation materials | ⬜ Pending | — | |

### Phase 7 — Demo
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
| 1 | What defect classes does the temporary `anomaly` label represent? (delamination, voids, cracks?) | Defines annotation scope and label schema for the next iteration |
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
| **Current Phase** | Phase 3 annotation + Phase 4a NVL Test Run (Training) — planned for weekend 2026-08-16/17 |
| **Next Milestone** | NVL Test Run Training complete → Inference review |
| **Demo Target** | September 30, 2026 |
| **Overall Status** | 🟡 On Track |

---

*Last updated: 2026-08-14 — Annotation complete for 20 NVL images using temporary `anomaly` label (approximately 39 minutes, 10:32–11:11). Next: NVL Test Run training.*
