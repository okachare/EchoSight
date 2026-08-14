# GeTi CSAM � Engineering Notes

**Hardware:** PVA SAM501 CSAM ? Geti installed directly on it
**Goal:** Train a defect detection model on NovaLake (NVL) scan images. Demo by end of Q3 2026.
**This workspace:** Drop logs, scripts, and run artifacts here for analysis and debugging.

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

## Currently WIP

- [x] Annotate 20 NVL images with `anomaly` polygon masks — completed 2026-08-14, approximately 39 minutes (10:32–11:11)
- [ ] NVL Test Run 01 — Mask R-CNN Swin-T training still in progress as of approximately 16:29; started 2026-08-14 at approximately 11:18
- [ ] Inference review — run predictions on unseen NVL images
- [ ] Map the temporary `anomaly` label to final defect classes (delamination, void, crack?)

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

---

## Next Steps (in order)

1. Finish NVL Test Run 01 — Mask R-CNN Swin-T, 20 images
2. Collect the Geti log, screenshots, and utilization CSVs
3. Review metrics + run inference on unseen images
4. Fine-tune: predict → review → correct → retrain loop
5. Lock additional defect classes (void, crack) and expand dataset

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

---

*Last updated: 2026-08-14 at approximately 16:29 — 20 NVL images annotated and Mask R-CNN Swin-T training still in progress. Next: collect the completed run artifacts and metrics.*
