# GeTi CSAM — Engineering Notes

**Hardware:** PVA SAM501 CSAM ? Geti installed directly on it
**Goal:** Train a defect detection model on NovaLake (NVL) scan images. Demo by end of Q3 2026.
**This workspace:** Drop logs, scripts, and run artifacts here for analysis and debugging.

---

## What's Done

**~2026-07-14 — Tool selection**
- Picked Intel Geti after reviewing docs + full GitHub repo
- Two modes: GUI app (what we're using on SAM501) and `getitune` Python library
- Key capability for us: tiling pipeline for large scan images, OpenVINO export for edge inference
- Supported dataset formats: COCO, YOLO, Pascal VOC, Datumaro native

**~2026-07-21 — Geti on SAM501**
- Installed and running on PVA SAM501. Launches fine.
- Using Windows app version (MSIX). No Ultralytics YOLO models but not needed yet.

**~2026-07-28 — NVL data collected**
- CSAM scans of NovaLake samples done on SAM501
- Raw output: multi-frame `.TIFF` files

**~2026-08-04 — TiffSplitter built**
- CSAM outputs `.TIFF`, Geti needs individual images ? built `TiffSplitter`
- GUI tool (tkinter), supports PNG/JPEG/BMP/WEBP export, configurable JPEG quality, progress bar
- Lives at `TiffSplitter/TiffSplitter.py`

**2026-08-11 — Image integrity check**
- Ran quantitative analysis on `ARL_Test.TIFF` vs splitter output
- Source: 8-bit, palette mode (`P`), 66 frames, 517x281px
- All 66 PNG and 66 JPEG files generated correctly, no missing frames
- **PNG chosen as training format** — lossless, preserves palette, no compression artefacts
- JPEG also fine (quality 95) but PNG is cleaner for defect boundaries

**2026-08-11 — Workspace + GitHub set up**
- Repo: https://github.com/okachare/GeTi_CSAM_PVA (private)
- Branch: `main`

---

## Currently WIP

- [ ] Dataset folder organization — need COCO/VOC structure for Geti auto-detection
- [ ] Defect class schema — not locked yet (voids? delamination? cracks? all three?)
- [ ] Annotation in Geti UI — started but blocked on class schema
- [ ] First training run — attempts being made, no clean run yet
- [ ] Logs — need to be dropped into this workspace for debugging

---

## Decisions Still Open

| Decision | Why it matters |
|---|---|
| Detection (bbox) vs Segmentation (mask)? | Affects model choice, annotation effort, and output format |
| What defect classes to label? | Everything downstream depends on this — lock it down ASAP |
| Which frames are useful vs noise? | Not all 66 frames per TIFF will have defects |

---

## Known Issues / Things to Watch

- TIFF splitter converts palette (`P`) mode to `RGB` for JPEG — minor mean shift (~20 pts) due to palette expansion + JPEG compression. Acceptable at quality 95.
- Dataset not yet in Geti-compatible folder structure — training will fail until this is fixed.
- Defect classes must be agreed before annotating more images — rework is expensive.

---

## Next Steps (in order)

1. Lock defect class list
2. Organize PNGs into COCO or VOC folder structure
3. Drop Geti training logs into workspace ? debug current runs
4. Complete annotation pass in Geti UI
5. Get first clean training run through

---

## Workspace Files

| File | What it is |
|---|---|
| `TiffSplitter/TiffSplitter.py` | TIFF ? PNG/JPEG splitter tool |
| `SCOPE_AND_PROGRESS.md` | Management report — phases, timeline, challenges |
| `RESOURCES.md` | Geti reference — models, API, install commands |
| `PROJECT_STATUS.md` | This file — engineering notes |

---

*Last updated: 2026-08-11 17:00 — Image integrity confirmed. PNG format chosen. Dataset org and annotation WIP. Defect classes not yet locked.*
