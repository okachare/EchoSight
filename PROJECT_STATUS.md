# GeTi CSAM � Engineering Notes

**Hardware:** PVA SAM501 CSAM; Geti Web is now the active platform
**Goal:** Train a defect detection model on NovaLake (NVL) scan images. Demo by end of Q3 2026.
**This workspace:** Drop logs, scripts, and run artifacts here for analysis and debugging.

## Platform Direction

- **Windows Geti/MSIX:** Closed as of 2026-08-19. All training, debugging, exports, metrics, and inference screenshots remain preserved as historical artifacts in `Debug/NVL_Geti_Run/`.
- **Web Geti:** Active platform going forward. New training, inference, evaluation, and deployment activities should be appended to the Web progress log below.

## Web Geti Progress Log

| Date | Activity | Status | Notes |
|---|---|---|---|
| 2026-08-19 | Web Geti model training | Complete | Model trained successfully in the Web version. Run details to be added as they are confirmed. |
| 2026-08-19 | Web Geti model inference | Complete | Inference completed successfully in the Web version. Prediction results and screenshots to be added to this log. |
| 2026-08-19 | Web Geti follow-up validation | Active | Continue recording model, dataset, metrics, sample count, and visual results here. |

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

---

## Windows Track: Closed

- [x] Annotate 20 NVL images with `anomaly` polygon masks — completed 2026-08-14, approximately 39 minutes (10:32–11:11)
- [x] NVL Test Run 01 — Mask R-CNN Swin-T training completed 2026-08-15 at 03:04 after approximately 15 hours 53 minutes; 140 epochs, 14/4/2 train/validation/test split, OpenVINO FP16 and ONNX FP16 exports created
- [x] Run artifacts — training log, copied project/model files, and resource-monitor CSVs preserved in `Debug/NVL_Geti_Run/`
- [x] Inference review attempt — completed in the Windows UI; `nvl_predict.PNG` preserved, with no visible prediction overlay for the captured sample
- [ ] Map the temporary `anomaly` label to final defect classes (delamination, void, crack?) — superseded by Web Geti work

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
- Interpretation: the model recognizes coarse anomaly regions, but the low mAP@0.75 and mAR@100 indicate imprecise mask boundaries and missed defect instances. Treat the run as a conditional go pending visual review on unseen images.
- Resource monitor: CPU averaged 45.8% and peaked at 100%; available RAM averaged 17.3 GB but briefly reached zero; disk throughput averaged 5.89 MiB/s and peaked at 132.65 MiB/s.

---

## Decisions Still Open

| Decision | Why it matters |
|---|---|
| Final meaning of temporary `anomaly` label? (delamination, void, crack?) | Determines whether the first NVL model is a generic anomaly detector or a class-specific defect model |
| How many NVL frames are useful vs noise? | Not all 66 frames per TIFF will have defects — need selection criteria |
| Will demo be live on SAM501 or separate machine? | Affects OpenVINO export target and deployment steps |
| How to include clean/"No object" images? | getitune limitation — needs investigation or workaround |

---

## Known Issues / Things to Watch

- getitune **cannot handle `"No object"` annotations in val/test split** for instance segmentation — empty bbox tensor crashes DataLoader collate. Workaround: defect-only datasets until fixed.
- Images upload directly into Geti project — no need for COCO/VOC folder structure when using Geti GUI.
- RF-DETR-Seg-M is the confirmed working architecture for this project.
- The preserved NVL configuration used early-stopping patience 10, despite the earlier planning note listing 15.

---

## Next Steps: Web Geti

1. Capture the Web Geti model name, revision, dataset size, and training configuration
2. Record Web Geti inference samples, prediction screenshots, and visual scores
3. Compare Web Geti results with the Windows baseline without mixing the two runs
4. Fine-tune: predict → review → correct → retrain loop in Web Geti
5. Lock additional defect classes (void, crack) and expand the dataset

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

---

*Last updated: 2026-08-19 — Windows Geti track closed. Web Geti is the active platform; model training and inference are complete and ongoing validation is being tracked separately.*
