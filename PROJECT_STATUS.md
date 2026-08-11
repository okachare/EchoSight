# GeTi CSAM Project — Status & Progress

## What This Project Is
Using **Intel Geti** (an end-to-end Vision AI platform) to build a computer vision model for analyzing images from a **Confocal Scanning Acoustic Microscope (CSAM)**.

**Hardware:** PVA SAM501 CSAM tool with Intel Geti installed directly on it.

CSAM is a non-destructive inspection tool used in semiconductor packaging. It generates grayscale acoustic scan images to reveal internal defects such as:
- Voids (air gaps in adhesive/underfill)
- Delamination (layer separation)
- Cracks
- Die attach defects

The goal is to automate defect detection/classification using Geti's training and inference pipeline.

## Workspace Role
This workspace (`GeTi CSAM/`) acts as the **interface and debug hub** between the developer and the CSAM tool:
- Run logs, Geti logs, and run artifacts from the SAM501 are dropped here for analysis
- All debugging, log review, and iteration decisions happen here
- No runs yet — will be updated as scans are performed

---

## Current Stage

**Stage: Active — Data, Annotation, Training & Debugging all WIP**

- [x] Identified tool: Intel Geti (open-edge-platform)
- [x] Reviewed Geti documentation and GitHub repository
- [x] Understood Geti architecture and usage modes
- [x] Hardware confirmed: PVA SAM501 CSAM tool, Geti installed and launching successfully
- [x] Workspace set up as debug/analysis interface
- [x] NVL CSAM images collected
- [x] Custom TIFF→JPEG conversion script written (CSAM output → Geti input)
- [x] TiffSplitter script moved into workspace (`TiffSplitter/TiffSplitter.py`) and pushed to GitHub
- [x] Image integrity verified: ARL_Test.TIFF (66 frames, 8-bit, 517×281px) — all 66 PNG and JPEG outputs confirmed valid
- [x] Decision: use **PNG** for Geti training (lossless, preserves palette exactly)
- [ ] Organize images into dataset folder structure (WIP)
- [ ] Define specific defect classes / annotation schema
- [ ] Annotate images in Geti (WIP)
- [ ] First clean training run completed (WIP)
- [ ] Geti logs / run artifacts dropped into workspace
- [ ] Analyse training results
- [ ] Fine-tune model
- [ ] Export and deploy model

---

## Completed Steps

### 2026-08-11 — Repository Familiarization
- Read full Geti GitHub repo: https://github.com/open-edge-platform/geti
- Read full Geti documentation: https://docs.geti.intel.com/docs/user-guide/getting-started/introduction
- Understood both usage modes (GUI app + Python library `getitune`)
- Identified tiling pipeline as important feature for large CSAM images
- Identified relevant CV tasks: **Object Detection** and/or **Semantic Segmentation**
- Confirmed dataset formats supported: COCO, YOLO, Pascal VOC, Datumaro native

### 2026-08-11 — Active Work Begun
- NVL CSAM images collected on PVA SAM501
- Custom script written to convert CSAM `.tiff` outputs → `.jpeg` for Geti ingestion
- Dataset organization in progress (images not yet sorted into folder structure)
- Annotation started in Geti UI (defect class schema still to be finalized)
- Training runs being attempted in Geti
- Debugging phase begun — logs not yet dropped into workspace

---

## Decisions Pending
- [ ] Which CV task to use? (detection with bounding boxes vs segmentation with masks)
- [ ] What defect classes will we label?
- [ ] Do we have labeled data already, or start from scratch?
- [ ] Deployment target: local Windows machine, server, or edge?
- [ ] Which Geti usage mode: GUI app or Python `getitune` library?

---

## Next Actions
1. Perform first scan run on the SAM501
2. Drop Geti logs and run artifacts into this workspace
3. Answer the pending decisions above (defect classes, CV task type)
4. Create Geti project and begin annotation

---

## Documents in This Workspace
| File | Purpose |
|---|---|
| [SCOPE_AND_PROGRESS.md](./SCOPE_AND_PROGRESS.md) | Management-facing project scope, phase tracker, challenges, roadblocks |
| [RESOURCES.md](./RESOURCES.md) | Technical reference — Geti architecture, models, API, install options |
| [PROJECT_STATUS.md](./PROJECT_STATUS.md) | Technical working log — detailed step-by-step progress |

---

*Last updated: 2026-08-11 16:30 — Image integrity confirmed. 66-frame TIFF splits cleanly to PNG/JPEG. PNG chosen as training format. Dataset organization next.*
