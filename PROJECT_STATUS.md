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
- New Geti project: Instance Segmentation, single class `delamination`
- 5 defect images, all polygon-annotated, no "No object" samples
- Model: RF-DETR-Seg-M, CPU training, ~37 min, 200 max epochs (early stopping)
- Result: 705 MB model, OpenVINO FP16 export 66 MB, mAP@0.5 ~1% (expected — smoke test only)
- **Pipeline proven end-to-end**: upload → annotate → train → export ✔
- Next: learn Geti model evaluation + inference, then scale up to full NVL dataset

---

## Currently WIP

- [ ] Learn Geti model evaluation UI — understand metrics, confusion matrix, per-class scores
- [ ] Learn Geti inference — run predictions on new images before starting real NVL run
- [ ] Decide full defect class list for NVL (delamination + void + crack?)
- [ ] Annotate 50+ NVL images with full class schema
- [ ] First real training run on full NVL dataset

---

## Decisions Still Open

| Decision | Why it matters |
|---|---|
| Full defect class list for NVL? (delamination + void + crack?) | Everything downstream depends on this — lock it down before annotating 50+ images |
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

1. Learn Geti model evaluation UI (metrics, confusion matrix, score breakdown)
2. Learn Geti inference — run predictions on a new image
3. Lock full defect class list for NVL run
4. Annotate 50+ NVL images with polygon masks
5. First real training run — target meaningful mAP

---

## Workspace Files

| File | What it is |
|---|---|
| `TiffSplitter/TiffSplitter.py` | TIFF ? PNG/JPEG splitter tool |
| `SCOPE_AND_PROGRESS.md` | Management report � phases, timeline, challenges |
| `RESOURCES.md` | Geti reference � models, API, install commands |
| `PROJECT_STATUS.md` | This file � engineering notes |

---

| `Debug/Run081125/jobs/` | 12 failed training logs from July 24 – Aug 11 |
| `Debug/Run081226/` | First successful run artifacts, screenshots, 1 failed log |

---

*Last updated: 2026-08-12 — First clean training run done. Pipeline proven. Next: evaluation + inference learning, then full NVL dataset.*
