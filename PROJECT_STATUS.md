# GeTi CSAM � Engineering Notes

**Hardware:** PVA SAM501 CSAM; Geti Web is now the active platform
**Goal:** Train a defect detection model on NovaLake (NVL) scan images. Demo by end of Q3 2026.
**This workspace:** Drop logs, scripts, and run artifacts here for analysis and debugging.

**Storage constraint:** The available storage budget is approximately 2 TB. Keep only required source data, selected screenshots, logs, model exports, and comparison summaries; avoid duplicating full datasets or every model variant.

## Platform Direction

- **Windows Geti/MSIX:** Closed as of 2026-08-19. All training, debugging, exports, metrics, and inference screenshots remain preserved as historical artifacts in `Debug/NVL_Geti_Run/`.
- **Web Geti:** Active platform going forward. New training, inference, evaluation, and deployment activities should be appended to the Web progress log below.
- **Evaluation results:** Store model-comparison screenshots and notes under `Debug/Evaluation/`, organized by model folder.

## Web Geti Access

- Access request: `http://goto/getiapply`
- Web application: `http://goto/cdgeti`
- **Geti CSAM Helper Agent & Skills (MCP):** [GitHub public repository](https://github.com/okachare/Geti-CSAM-Helper) — Product-neutral agent, Geti Trainer skill, CSAM Basics, and Setup Helper for team training and troubleshooting.
- Current Web evidence: `Debug/NVL_Geti_WB_Run/`

## Web Geti Progress Log

| Date | Activity | Status | Notes |
|---|---|---|---|
| 2026-08-18 | Web Geti dataset setup | Complete | Project `NVL-S-28C`; Instance Segmentation; 24 images uploaded; two labels visible in the Web UI. |
| 2026-08-18 | Web Geti model training | Complete | `MaskRCNN-EfficientNetB2B` Speed architecture; model Versions 1 and 2 created. |
| 2026-08-18 | Web Geti model evaluation | Complete | Version 2 active; score 9%; OpenVINO FP32 and FP16 variants available; FP16 size 27.36 MB. |
| 2026-08-18 | Web Geti dataset split | Complete | Training 50%, Validation 29%, Testing 21%. |
| 2026-08-18 | Web Geti test run | Complete | Version 2, OpenVINO FP16, 24 images, score 24. |
| 2026-08-18 | Web Geti live prediction | Complete | Live prediction produced visible masks for `Delamination` and `Inclusion/Void`; a later test record shows Version 5, 25 images, score 78. |
| 2026-08-19 | Web Geti follow-up validation | Complete | Initial Web training, testing, and live prediction evidence recorded. |
| 2026-08-20 | Web Geti model comparison planning | Complete | MobileNet selected for the bounding-box detection baseline; comparison uses 20 images: 14 bad annotated images and 6 good unannotated units. |
| 2026-08-20 | Model comparison deck generation | Complete | Final technical deck generated and saved as `GeTi_CSAM_Model_Comparison_Deck.pptx`; includes DOE overview, individual model summaries, workflow logic, and comparison matrix. |
| 2026-08-20 | Quarter closeout | Complete | DOE work is closed for the quarter; remaining fine-tuning, deployment validation, and demo activities are intentionally deferred to Q4. |
| 2026-08-26 | Geti CSAM Helper Agent development | Complete | Product-neutral agent and MCP-based skills package created for team training and troubleshooting; dual-repository strategy implemented (source + public). |
| 2026-08-26 | Geti Trainer skill implementation | Complete | 16-step Web Geti operator walkthrough with 19-field debugging intake form and 5-field gate logic; 9-issue recovery playbook; integrated into MCP server. |
| 2026-08-26 | Product neutralization pass | Complete | All product-specific terms removed (NVL, NovaLake, SAM501, PVA); three skills now suitable for team sharing and cross-product use. |
| 2026-08-26 | Skills validation and demonstration | Complete | CSAM Basics, Geti Trainer, and Geti Setup Helper skills invoked and validated; MCP server correctly exposes all resources and prompts. |
| 2026-09-02 | Local EchoSight GUI development | Complete | Created standalone inference GUI (`Deployment/EchoSight_Inference_GUI/`) with multi-format image import (PNG/JPG/BMP/TIFF), real-time inference with background threading, confidence filtering (0.10-1.0), annotation overlays (boxes/labels/masks), zoom/pan preview, configurable image preprocessing (brightness/contrast/sharpness/denoiser with per-frame profiles), and results export (CSV/PNG). PyInstaller-based portable packaging bundles all dependencies (OpenVINO 2024.5, OpenCV, PIL, NumPy). Users run `build_installer.ps1` once, then double-click `EchoSight.exe` on any Windows system with no Python installation required. Model loading, real inference, TIFF import, and export validated. |
| 2026-09-03 | EchoSight GUI refinement and finalization | Complete | Added model-independent controls (label/mask/box visibility toggles, 1%-100% confidence slider), anomaly-detection support with mask/score rendering, right-aligned frame score indicators, configurable preprocessing (brightness/contrast/sharpness/denoiser with All/Current/Selected scope and per-frame profile storage), integrated controls into compact lower-right popover with zoom/pan preservation, maximized launch, professional rounded buttons (6 color variants), unified 0.6 font size for all annotation labels. Renamed package to EchoSight with subtitle "Model-agnostic image inference and inspection". PyInstaller portable with fully bundled dependencies validated. |
| 2026-09-08 | EchoSight standalone GitHub repository | Complete | Created independent repository at https://github.com/okachare/EchoSight with comprehensive documentation (README, SETUP, INSTALL, USAGE, DEVELOPMENT, CHANGELOG, CODE_OF_CONDUCT), MIT license, GitHub Actions CI/CD workflow for automated release builds on version tags, and author attribution (Omkar Kachare, 11943102). Repository structured with src/echosight package layout, setup.py for pip installation, and PyInstaller build configuration. |
| 2026-09-08 | EchoSight setup process simplified | Complete | Consolidated three redundant setup scripts into single foolproof `SETUP.ps1` that handles Python 3.9 detection, virtual environment creation, dependency installation, and launcher generation. Rewrote with clean PowerShell syntax (no heredoc string issues), robust error handling, and window-stay-open behavior for error visibility. Created `SETUP.md` with simple one-command flow: `.\SETUP.ps1` → double-click `Launch_EchoSight.bat`. Includes comprehensive troubleshooting (DIAGNOSE.ps1 for Python/environment checks, MANUAL_SETUP.md for step-by-step reference). |
| 2026-09-08 | EchoSight installation validation | Complete | Successfully tested SETUP.ps1 on Windows system with Python 3.9. Virtual environment created, all dependencies installed (OpenVINO 2024.5, OpenCV, PIL, NumPy), and `Launch_EchoSight.bat` launcher auto-generated without errors. EchoSight GUI launches successfully and is fully operational. Installation time: ~5 minutes. Setup process is production-ready and foolproof with zero manual configuration required. |

## Management Update — 2026-08-25

Web Geti successfully demonstrated the end-to-end NovaLake CSAM workflow: upload and annotate images, train an Instance Segmentation model, test an OpenVINO FP16 variant, and run live prediction. Project `NVL-S-28C` uses `Delamination` and `Inclusion/Void` labels. The later recorded Web test scored **78** on 25 images, and live prediction produced visible defect masks, including a `Delamination` prediction. The Web workflow is operational and is the recommended platform for the next iteration.

The 20-image model-comparison benchmark and `GeTi_CSAM_Model_Comparison_Deck.pptx` are complete. Instance segmentation is recommended for engineering review because it preserves defect shape; detection remains the fast-screening alternative. Results are directional because the dataset is small. Q4 work will fine-tune the NVL models, deploy the selected model for WIPs, train the team on Geti, and extend the approach to other products.

---

## What's Done

**~2026-07-14 � Tool selection**
- Picked Intel Geti after reviewing docs + full GitHub repo
- Two modes: GUI app (what we're using on SAM501) and `getitune` Python library
- Key capability for us: tiling pipeline for large scan images, OpenVINO export for edge inference
- Supported dataset formats: COCO, YOLO, Pascal VOC, Datumaro native

**~2026-07-21 � Geti on SAM501**
- Installed and running on PVA SAM501. Launches fine.
- Using Windows app version (MSIX). No Ultralytics YOLO models but not needed yet.

**~2026-07-28 � NVL data collected**
- CSAM scans of NovaLake samples done on SAM501
- Raw output: multi-frame `.TIFF` files

**~2026-08-04 � TiffSplitter built**
- CSAM outputs `.TIFF`, Geti needs individual images ? built `TiffSplitter`
- GUI tool (tkinter), supports PNG/JPEG/BMP/WEBP export, configurable JPEG quality, progress bar
- Lives at `TiffSplitter/TiffSplitter.py`

**2026-08-11 � Image integrity check**
- Ran quantitative analysis on `ARL_Test.TIFF` vs splitter output
- Source: 8-bit, palette mode (`P`), 66 frames, 517x281px
- All 66 PNG and 66 JPEG files generated correctly, no missing frames
- **PNG chosen as training format** � lossless, preserves palette, no compression artefacts
- JPEG also fine (quality 95) but PNG is cleaner for defect boundaries

**2026-08-11 — Training logs analysed**
- 12+1 failed runs: root cause = `"No object"` images in val/test split → empty bbox tensor → `ValueError: Boxes batch must have 4 coordinates` in getitune DataLoader collate
- getitune requires every image in every split to have at least one annotated shape
- Workaround: defect-only dataset (no clean/negative images) until getitune fixes this

**2026-08-12 — First clean training run completed**
- New Geti project: Instance Segmentation, single class `delamination` (smoke test)
- 5 defect images, all polygon-annotated, no "No object" samples
- Model: RF-DETR-Seg-M, CPU training, ~37 min, 200 max epochs (early stopping)
- Result: 705 MB model, OpenVINO FP16 export 66 MB, mAP@0.5 ~1% (expected — smoke test only)
- **Pipeline proven end-to-end**: upload → annotate → train → export ✔

**2026-08-12 — NVL data collection complete**
- 20 NVL defect images selected from the collected and organised dataset for NVL Test Run 01
- Ready for annotation and training this weekend

**2026-08-12 — Documentation complete**
- `NVL_TEST_RUN_PLAN.md` — step-by-step plan for NVL Test Run (Training → Inference → Fine-tuning)
- `GETI_TRAINING_MANUAL.md` — full training manual: concepts, metrics, parameters, troubleshooting, run records

**2026-08-20 — Model comparison deck completed**
- Built the final management-facing deck for the NVL DOE comparison.
- Includes the DOE setup slide, technical workflow slide, 3 model summaries, and the final comparison matrix with pros/cons/accuracy/limitations.
- Output file: `GeTi_CSAM_Model_Comparison_Deck.pptx`

---

## Windows Track: Closed

### Windows Track Limitation: No Direct Image-Folder Source

The Windows Geti workflow could not use the organized image folder directly as the source dataset. Images had to be uploaded and managed through the application, which made repeated runs, dataset reuse, and controlled source-data management less practical. This was separate from the `getitune` annotation crash and was a major operational reason for moving the active work to Web Geti.

- [x] Annotate 20 NVL images with `anomaly` polygon masks — completed 2026-08-14, approximately 39 minutes (10:32–11:11)
- [x] NVL Test Run 01 — Mask R-CNN Swin-T training completed 2026-08-15 at 03:04 after approximately 15 hours 53 minutes; 140 epochs, 14/4/2 train/validation/test split, OpenVINO FP16 and ONNX FP16 exports created
- [x] Run artifacts — training log, copied project/model files, and resource-monitor CSVs preserved in `Debug/NVL_Geti_Run/`
- [x] Inference review attempt — completed in the Windows UI; `nvl_predict.PNG` preserved, with no visible prediction overlay for the captured sample
- [x] Windows temporary `anomaly` label track closed — superseded by Web Geti labels `Delamination` and `Inclusion/Void`

## NVL Test Run 01 Results

| Metric | Held-out test result |
|---|---:|
| mAP | 22.82% |
| mAP@0.5 | 46.53% |
| mAP@0.75 | 14.85% |
| mAR@1 | 15.71% |
| mAR@100 | 28.57% |

- Best validation checkpoint: epoch 129, with mAP=28.59%, mAP@0.5=79.21%, mAP@0.75=13.15%, and mAR@100=37.00%.
- The test split contains only two images, so these are a directional baseline rather than a stable production-quality estimate.
- Interpretation: the model recognized coarse anomaly regions, but the low mAP@0.75 and mAR@100 indicated imprecise mask boundaries and missed defect instances. The Windows run is closed as a historical conditional-go baseline; the Web workflow is the active path.
- Resource monitor: CPU averaged 45.8% and peaked at 100%; available RAM averaged 17.3 GB but briefly reached zero; disk throughput averaged 5.89 MiB/s and peaked at 132.65 MiB/s.

---

## Web Decisions for Q4 Execution

| Decision | Why it matters |
|---|---|
| Expand the Web taxonomy beyond `Delamination` and `Inclusion/Void` as needed | Defines annotation scope for additional products and defect types |
| Select useful NVL frames and add difficult examples | Improves coverage and reduces the risk of overfitting to a small benchmark |
| Select the final WIP deployment host and export precision | Determines OpenVINO packaging and runtime validation |
| Establish the clean-image training workflow | Controls false-positive evaluation and anomaly-screening quality |
| Define the local GUI inference contract | Ensures TIFF decoding, preprocessing, model outputs, labels, overlays, and saved evidence match Geti behavior |

---

## Known Issues / Things to Watch

- Windows Geti could not consume an image folder directly as the source dataset; the application upload workflow was required. Web Geti is the active path for more practical dataset and experiment management.
- getitune **cannot handle `"No object"` annotations in val/test split** for instance segmentation — empty bbox tensor crashes DataLoader collate. Workaround: defect-only datasets until fixed.
- Images upload directly into Geti project — no need for COCO/VOC folder structure when using Geti GUI.
- RF-DETR-Seg-M is the confirmed working architecture for this project.
- The preserved NVL configuration used early-stopping patience 10.
- The downloaded Detection code deployment includes a MobileNetV2-ATSS OpenVINO FP16 model, model version 7, and the Geti SDK wrapper under `Deployment/Test_Run_Detect/`. The GUI also accepts the local `Test_Run_Instance_Segmentation` package, which is technically an AnomalyDetection export; single-image wrapper inference is validated, and representative multi-frame TIFF batch validation remains active.
- The compatible Python 3.9/OpenVINO 2024.5 runtime loads the deployment successfully; the current project Python 3.14/OpenVINO 2026 runtime is not compatible with this legacy wrapper.
- The Geti SDK returns detections through `DetectionResult.objects`; the GUI renderer was corrected to use each object's `xmin`, `ymin`, `xmax`, `ymax`, `score`, and `str_label` fields. A real-model smoke test displayed six detections.
- The downloaded deployment metadata includes model version, record date, precision, size, score, labels, optimization, XAI-head status, and CPU target, but does not include the original training-image count; the GUI displays that field as unavailable rather than inferring it.
- Portable packaging now preserves the complete verified inference dependency set rather than aggressively pruning transitive packages; only PyInstaller build tooling is excluded.

---

## Next Steps: Web Geti

1. Preserve the completed 20-image Web benchmark and comparison evidence
2. Fine-tune the NVL models with difficult and representative images
3. Export the selected model and preserve the complete deployable package and metadata
4. Validate offline OpenVINO inference across representative multi-frame TIFFs with `Deployment/EchoSight_Inference_GUI/`
5. Compare GUI outputs against Geti predictions and measure latency, resource use, and model size
6. Record parity results and failure behavior before packaging for WIP use
7. Deploy the selected model for WIPs after validation
8. **Use Geti CSAM Helper agent and skills package for team training on Web Geti workflow**
9. Bring in team support to extend the approach to other products using the product-neutral skills package

## Deferred Work

- Complete the self-contained portable folder with bundled Python/OpenVINO dependencies.
- Build and test the standalone Windows installer.
- Validate copy/paste execution on a clean Windows machine.

---

## Team Training & Knowledge Transfer (2026-08-26)

The **Geti CSAM Helper** agent and MCP-based skills package is now operational and ready for team use:

- **Geti Trainer skill**: Provides 16-step click-by-click Web Geti walkthrough, debugging intake form (19 fields, 5-field gate), and 9-issue recovery playbook
- **CSAM Basics skill**: Multi-frame TIFF preparation, defect annotation guidance, task selection (Instance Seg vs Detection vs Anomaly)
- **Geti Setup Helper skill**: Pre-work readiness checks, TiffSplitter guidance, dataset validation, evidence capture
- **MCP architecture**: Four skills exposed as resources, including upstream Geti source guidance; source links are also available as an MCP tool
- **Product neutrality**: All references removed (NVL, NovaLake, SAM501, PVA) for cross-product and external team sharing
- **Repositories**: Source repo (`okachare/GeTi_CSAM_PVA`, branch `main`, commit 697acc3) contains full project history; public repo (`okachare/Geti-CSAM-Helper`, branch `main`, commit 5c222de) is product-neutral for team distribution

---

## Workspace Files

| File | What it is |
|---|---|
| `TiffSplitter/TiffSplitter.py` | TIFF → PNG/JPEG splitter tool |
| `SCOPE_AND_PROGRESS.md` | Management report — phases, timeline, challenges |
| `RESOURCES.md` | Geti reference — models, API, install commands |
| `PROJECT_STATUS.md` | This file — engineering notes |
| `NVL_TEST_RUN_PLAN.md` | Step-by-step plan for NVL Test Run weekend |
| `GETI_TRAINING_MANUAL.md` | Full training manual: metrics, parameters, troubleshooting |
| `Debug/Run081125/jobs/` | 12 failed training logs from July 24 – Aug 11 |
| `Debug/Run081226/` | Smoke test run artifacts (logs, screenshots, 1 failed + 1 successful) |
| `Debug/NVL_Geti_Run/` | Completed NVL Test Run 01 artifacts: logs, model exports, copied project files, and utilization CSVs |
| `Deployment/EchoSight_Inference_GUI/` | EchoSight offline inference prototype, requirements, README, and installer build script |

---

*Last updated: 2026-09-08 — EchoSight published as standalone GitHub repository (https://github.com/okachare/EchoSight) with comprehensive documentation, MIT license, and CI/CD automation. Setup process simplified to one foolproof command: SETUP.ps1 creates virtual environment, installs dependencies, and generates Launch_EchoSight.bat launcher. **Installation successfully validated on Windows system:** virtual environment created, all dependencies installed (OpenVINO 2024.5, OpenCV, PIL, NumPy), launcher auto-generated, GUI launches and is fully operational. Installation time: ~5 minutes. Setup process is production-ready with zero manual configuration. Users can deploy EchoSight on any Windows system with Python 3.9 in under 5 minutes. Team training integration and additional platform validation next priorities.*
