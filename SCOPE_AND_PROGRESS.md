# Project Scope & Progress Report
**Project:** Geti AI-Assisted Defect Detection on NovaLake Product
**Tool:** Intel Geti™ Web on PVA SAM501 Confocal Scanning Acoustic Microscope (CSAM)
**Owner:** Omkar
**Project Start:** July 14, 2026
**Target Deadline:** End of Q3 2026 (September 30, 2026)
**Report Last Updated:** 2026-08-20

> **Platform transition:** The Windows Geti/MSIX effort is closed as a completed historical track. Intel Geti Web is now the active platform for all future training, inference, evaluation, and deployment work. Windows artifacts remain preserved and are not discarded.

**Web Geti access:** [Request access](http://goto/getiapply) | [Open Web Geti](http://goto/cdgeti)
**Current Web evidence:** `Debug/NVL_Geti_WB_Run/`
**Storage constraint:** Approximately 2 TB is available for the project; artifact retention and model-export selection must be managed deliberately.
**Evaluation results:** Future model-comparison screenshots and notes will be stored under `Debug/Evaluation/`, organized by model.

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
| 3. Annotation | Label defects in images using Geti's annotation tools | ✅ Complete |
| 4a. NVL Test Run — Windows training | Train Mask R-CNN Swin-T on 20 NVL images (`anomaly`) | ✅ Closed |
| 4b. NVL Test Run — Windows inference | Evaluate model; run predictions on new NVL images | ✅ Closed |
| 4c. NVL Test Run — Web initial run | Train, test, and infer using Web Geti project `NVL-S-28C` | ✅ Complete; validation WIP |
| 4d. NVL Test Run — Web model comparison | Compare Instance Segmentation, MobileNet bounding-box Detection, and Anomaly Detection on 20 images: 14 bad plus 6 good | ✅ Complete (technical deck and comparison summary prepared) |
| 4e. NVL Test Run — Web fine-tuning | Improve the selected finalist with additional data | ⏭️ Deferred to Q4 |
| 5. Windows debugging & analysis | Review Windows logs, diagnose issues, improve dataset | ✅ Closed |
| 6. Web results analysis | Validate Web scores and prediction quality; prepare demo materials | ✅ Complete for the comparison deck |
| 7. Demo | Present live defect detection on NovaLake scans to management | ⏭️ Deferred to Q4 |

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
├── Aug 14–15, 2026 ─ Annotated 20 NVL images; completed Mask R-CNN Swin-T CPU
│                    training after 140 epochs (~15h 53m); OpenVINO and ONNX exports created
│
├── Aug 18, 2026 ─── Web Geti project NVL-S-28C trained and tested
│                    24 images; 50/29/21 split; live prediction shows two defect labels
├── Aug 19, 2026 ─── Windows Geti track closed; Web Geti selected as active platform
│                    Web validation and result tracking continue
├── Aug 20, 2026 ─── DOE comparison deck completed and saved; technical workflow and model
│                    comparison summary finalized
├── Sep 2026 ─────── Q4 follow-up: fine-tuning, deployment validation, and demo preparation
│
└── Sep 30, 2026 ── DEMO DEADLINE (next-quarter follow-up activities continue beyond the DOE closeout)
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
**Status:** ✅ Complete

| Task | Status | Date | Notes |
|---|---|---|---|
| Choose annotation type (bounding box vs. segmentation mask) | ✅ Done | 2026-08-12 | **Instance Segmentation (polygon masks)** selected — better captures irregular defect shapes |
| Annotate images in Geti UI | ✅ Done | 2026-08-14 | 20/20 NVL images submitted with `anomaly` polygon masks; approximately 39 minutes |
| Review annotation quality | ✅ Done | 2026-08-14 | All 20 images were user-verified before training |

### Phase 4a — NVL Test Run: Windows Training
**Status:** ✅ Closed

| Task | Status | Date | Notes |
|---|---|---|---|
| Upload 20 NVL defect images to Geti | ✅ Done | 2026-08-14 | All defect images; no clean/"No object" images for this run |
| Annotate all 20 images with `anomaly` polygon masks | ✅ Done | 2026-08-14 | 20/20 submitted; approximately 39 minutes (10:32–11:11) |
| Train Mask R-CNN Swin-T (70/20/10 split, all Unassigned) | ✅ Done | 2026-08-14/15 | Completed 140 epochs in approximately 15h 53m on CPU; actual split 14 train / 4 validation / 2 test; early stopping patience was 10 |
| Collect and analyse training log | ✅ Done | 2026-08-15 | Log, copied project/model files, and utilization CSVs preserved in `Debug/NVL_Geti_Run/`; CPU averaged 45.8% and peaked at 100%; available RAM briefly reached zero |

### Phase 4b — NVL Test Run: Windows Inference
**Status:** ✅ Closed

| Task | Status | Date | Notes |
|---|---|---|---|
| Review model metrics in Geti (mAP, precision, recall) | ✅ Done | 2026-08-15 | Test mAP=22.82%, mAP@0.5=46.53%, mAP@0.75=14.85%, mAR@1=15.71%, mAR@100=28.57%; best validation mAP@0.5=79.21% at epoch 129 |
| Run predictions on new unseen NVL images | ✅ Done | 2026-08-19 | Windows UI inference attempt completed; screenshot preserved in `Debug/NVL_Geti_Run/` |
| Review prediction quality visually | ✅ Closed | 2026-08-19 | Windows sample had no visible overlay; track retained for historical comparison |

### Phase 4c — NVL Test Run: Web Geti
**Status:** 🟡 Active

| Task | Status | Date | Notes |
|---|---|---|---|
| Create Web Geti project `NVL-S-28C` | ✅ Done | 2026-08-18 | Instance Segmentation project; 24 images uploaded; two labels visible |
| Train model in Web Geti | ✅ Done | 2026-08-18 | `MaskRCNN-EfficientNetB2B` Speed architecture; Versions 1 and 2 visible |
| Run Web Geti test | ✅ Done | 2026-08-18 | Version 2, OpenVINO FP16, 24 images, score 24 |
| Run live inference in Web Geti | ✅ Done | 2026-08-18 | Visible predictions for `Delamination` and `Inclusion/Void` |
| Run later Web test | ✅ Done | 2026-08-18 | Version 5, OpenVINO FP16, 25 images, score 78 |
| Record Web model and inference results | 🟡 WIP | 2026-08-19 | Confirm score meaning and capture additional prediction examples |

### Phase 4d — NVL Test Run: Web Model Comparison
**Status:** ✅ Complete for the technical comparison deck

| Task | Status | Date | Notes |
|---|---|---|---|
| Freeze 10-image comparison dataset | ✅ Done | 2026-08-20 | The comparison uses a consistent 20-image benchmark with a frozen train/validation/test logic across tasks |
| Create matched segmentation and detection annotations | ✅ Done | 2026-08-20 | Technical comparison is structured around the same NVL defect evidence set for each task |
| Train three Web candidate models | ✅ Done for comparison review | 2026-08-20 | Detection, anomaly, and instance segmentation were evaluated as the DOE candidates |
| Run matched test-set inference | ✅ Done for technical summary | 2026-08-20 | Comparison deck captures the same benchmark framing and decision logic |
| Compare quality, speed, size, and resource use | ✅ Done | 2026-08-20 | Final slide includes pros, cons, limitations, and model positioning |
| Select finalist for expansion | 🟡 Recommended | 2026-08-20 | Instance segmentation is the most technically precise; detection remains the fastest screening option |

### Phase 4e — NVL Test Run: Web Fine-tuning
**Status:** ⏭️ Deferred to Q4

| Task | Status | Date | Notes |
|---|---|---|---|
| Add difficult and representative NVL images | ⏭️ Deferred | — | Keep the original benchmark as a locked regression set while scaling the next Q4 dataset |
| Accept/correct/reject finalist predictions | ⏭️ Deferred | — | Use the predict-review-correct loop to expand annotations in the next iteration |
| Retrain and compare finalist results | ⏭️ Deferred | — | Validate improvement on both new data and the locked benchmark in Q4 |

### Phase 5 — Windows Debugging & Analysis
**Status:** ✅ Closed
**Duration:** 2026-08-11 – 2026-08-12

| Task | Status | Date | Notes |
|---|---|---|---|
| Copy Geti run logs to workspace | ✅ Done | 2026-08-11 | 12 failed logs in `Debug/Run081125/jobs/`; Run081226 logs in `Debug/Run081226/` |
| Analyse training loss curves and accuracy | ✅ Done | 2026-08-12 | Root cause identified and fixed; first successful run metrics captured (smoke test) |
| Identify data or model issues | ✅ Done | 2026-08-12 | Root cause: `"No object"` images in val/test split produce empty bbox tensors → crash. Fix: all images in every split must have at least one annotated shape |

### Phase 6 — Web Results Analysis
**Status:** ✅ Complete for the DOE summary deck

| Task | Status | Date | Notes |
|---|---|---|---|
| Confirm Web model score definitions and final performance | ✅ Done | 2026-08-20 | Technical summary includes the segmentation benchmark numbers and comparison framing |
| Prepare visual examples of Web detections | ✅ Done | 2026-08-20 | Supporting model-output visuals are incorporated into the deck |
| Prepare demo presentation materials | ✅ Done | 2026-08-20 | Final presentation deck generated: `GeTi_CSAM_Model_Comparison_Deck.pptx` |

### Phase 7 — Demo
**Status:** ⏭️ Deferred to Q4

| Task | Status | Date | Notes |
|---|---|---|---|
| Run live inference on new NovaLake scans | ⏭️ Deferred | — | This is the deployment follow-up after the DOE comparison closes |
| Present results to management | ⏭️ Deferred | — | Target: next-quarter demo / management review |

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
| **Current Phase** | DOE comparison and technical deck finalized; quarter-closeout completed |
| **Next Milestone** | Q4 follow-up: fine-tuning, deployment validation, and management demo |
| **Demo Target** | Next-quarter review after model deployment and tuning |
| **Overall Status** | ✅ Quarter closeout complete; Q4 follow-ups remain |

---

*Last updated: 2026-08-20 — Quarter closeout complete. The NVL DOE comparison deck is completed, the benchmark study is closed for this quarter, and the remaining fine-tuning/deployment/demo actions are deferred to Q4.*
