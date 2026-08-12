# NVL Test Run — Step-by-Step Plan

**Project:** Geti AI-Assisted Defect Detection on NovaLake  
**Run Name:** NVL Test Run  
**Planned Date:** 2026-08-16/17 (weekend)  
**Goal:** Train first real delamination detection model on 30 NVL CSAM images and validate inference quality  

---

## Overview

| Phase | Activity | Target Outcome |
|---|---|---|
| **4a — Training** | Annotate 30 images → train RF-DETR-Seg-M | Clean training run, mAP baseline established |
| **4b — Inference** | Review metrics → predict on new images | Confirm model detects delamination on unseen images |
| **4c — Fine-tuning** | Correct predictions → retrain → compare mAP | Improved accuracy; repeat until demo-ready |

---

## Phase 4a — Training

### Step 1 — Create new Geti project
- Launch Geti on PVA SAM501
- Click **Create New Project**
- Task type: **Instance Segmentation**
- Project name: `NVL_TestRun_01` (or similar)
- Label: add `delamination` only (single class for this run)

### Step 2 — Upload images
- Upload all **30 NVL defect images** (PNG format from TiffSplitter)
- Do **not** include clean/good-unit images — getitune crashes when "No object" images land in val/test split
- Leave all images as **Unassigned** after upload

### Step 3 — Annotate all 30 images
- Open **Annotate** tab
- For each image:
  - Select the **Polygon tool** (left toolbar)
  - Select label: **Delamination**
  - Trace the delamination boundary tightly — follow the defect edge, not a loose outline
  - If an image has **multiple delamination spots**, draw a **separate polygon for each one**
  - Click **Submit** after each image
- Work through all 30 images before starting training — do not train on partial annotations
- All 30 images should show a green checkmark (✓) in the filmstrip when done

### Step 4 — Configure training
- Click **Train Model**
- **Model:** RF-DETR-Seg-M (Balance preset) — do not use XL for this run (CPU is too slow)
- **Advanced Settings → Data Management:**
  - Split: Training 70% / Validation 20% / Test 10% (default)
  - Expected distribution with 30 images: Training=21, Validation=6, Test=3
  - Confirm **Unassigned: 0** before proceeding — all images must be assigned
- **Advanced Settings → Training:** leave all defaults (200 epochs, early stopping patience 15, LR 0.0001)
- **Device:** CPU (no GPU on SAM501)
- Click **Start**

### Step 5 — Collect training log
- After training completes (or fails), copy the log file from Geti's jobs folder
- Save into: `Debug/RunNVL01/jobs/`
- Save a screenshot of the training result card as `RunNVL01_result.PNG`
- Drop both into the workspace for analysis

---

## Phase 4b — Inference

### Step 6 — Review model metrics in Geti
In the **Models** tab, open the trained model and check:
- **mAP@0.5** — primary accuracy metric; target >50% for a useful model
- **mAP@0.75** — stricter overlap threshold; useful for tight mask quality
- **Precision** — of all predictions, how many were actually delamination?
- **Recall** — of all real delamination instances, how many did the model find?
- **Per-subset scores** — check if val/test scores are close to training scores (large gap = overfitting)

### Step 7 — Run predictions on new images
- Go to **Annotate** tab
- Upload **2–3 new NVL images** that were NOT in the training set
- Click **Predict** on each image
- Geti will overlay predicted masks using the trained model
- Assess:
  - Are masks landing on actual delamination?
  - Are there obvious false positives (mask on clean area)?
  - Are real defects being missed (false negatives)?
- Screenshot results and save to `Debug/RunNVL01/`

---

## Phase 4c — Fine-tuning

### Step 8 — Accept / correct / reject predictions
For each predicted image:
- **Accept** predictions that look correct
- **Correct** predictions that are close but need adjustment (reshape polygon)
- **Reject** predictions that are completely wrong
- Submit — accepted/corrected images are added back into the training dataset

### Step 9 — Add more images if needed
If mAP@0.5 is below ~30% after the first run:
- Annotate additional NVL images (target: work toward 50–100 total)
- Use the predict-review-correct loop to annotate faster (Geti pre-fills, you just verify)
- Re-train and compare mAP vs the previous run

### Step 10 — Retrain and compare
- Repeat Steps 4–9 until model quality is acceptable for demo
- Log each training run into a new `Debug/RunNVL0X/` folder
- Record mAP@0.5 per run in the table below

---

## Run Log

| Run | Date | Images | Model | mAP@0.5 | Notes |
|---|---|---|---|---|---|
| Smoke Test | 2026-08-12 | 5 (delamination only) | RF-DETR-Seg-M | ~1% | Pipeline smoke test — not a real model |
| NVL Test Run 01 | — | 30 (delamination only) | RF-DETR-Seg-M | — | Planned weekend 2026-08-16/17 |

---

## Key Rules (learned from debugging)

| Rule | Why |
|---|---|
| All images must have at least one polygon annotation | "No object" / empty-annotation images in val/test crash getitune with `ValueError: Boxes batch must have 4 coordinates` |
| Leave all images as "Unassigned" | Geti auto-fills training/val/test subsets; manual assignment risks leaving a subset empty |
| Need minimum 3 annotated images per split | Geti requires Training ≥ 1, Validation ≥ 1, Test ≥ 1 — minimum 3 images total |
| Draw one polygon per defect instance | Don't merge multiple defects into one shape — each instance should be separate |
| Annotate all images before training | Partial annotation leads to inconsistent dataset splits |

---

*Created: 2026-08-12 — Plan for NVL Test Run weekend 2026-08-16/17*
