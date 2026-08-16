# NVL Test Run — Step-by-Step Plan

**Project:** Geti AI-Assisted Defect Detection on NovaLake  
**Run Name:** NVL Test Run  
**Planned Date:** 2026-08-16/17 (weekend)  
**Goal:** Train first real anomaly detection model on 20 NVL CSAM images and validate inference quality  

---

## Overview

| Phase | Activity | Target Outcome |
|---|---|---|
| **4a — Training** | Annotate 20 images → train Mask R-CNN Swin-T | Clean training run, mAP baseline established |
| **4b — Inference** | Review metrics → predict on new images | Confirm model detects anomalies on unseen images |
| **4c — Fine-tuning** | Correct predictions → retrain → compare mAP | Improved accuracy; repeat until demo-ready |

---

## Phase 4a — Training

### Step 1 — Create new Geti project
- Launch Geti on PVA SAM501
- Click **Create New Project**
- Task type: **Instance Segmentation**
- Project name: `NVL_TestRun_01` (or similar)
- Label: add `anomaly` only (temporary single class for this run)

### Step 2 — Upload images
- Upload all **20 NVL defect images** (PNG format from TiffSplitter)
- Do **not** include clean/good-unit images — getitune crashes when "No object" images land in val/test split
- Leave all images as **Unassigned** after upload — this means do not manually set Training/Validation/Testing on any image; Geti will auto-distribute them when training starts

### Step 3 — Annotate all 20 images ✅ Complete
- **Completed:** 2026-08-14, approximately 10:32–11:11 (39 minutes)
- **Result:** 20/20 images submitted with `anomaly` polygon annotations
- Open **Annotate** tab
- For each image:
  - Select the **Polygon tool** (left toolbar)
  - Select label: **Anomaly**
  - Trace the anomaly boundary tightly — follow the defect edge, not a loose outline
  - If an image has **multiple anomaly spots**, draw a **separate polygon for each one**
  - Click **Submit** after each image
- Work through all 20 images before starting training — do not train on partial annotations
- All 20 images should show a green checkmark (✓) in the filmstrip when done

### Step 4 — Configure training ✅ Complete
- **Training window:** 2026-08-14 11:11:40 to 2026-08-15 03:04:20 (approximately 15 hours 53 minutes)
- **Run:** Mask R-CNN Swin-T, 20 images, temporary `anomaly` label
- **Result:** completed through epoch 140; Geti then exported and evaluated PyTorch, OpenVINO FP16, and ONNX FP16 variants
- Click **Train Model**
- **Model:** Mask R-CNN Swin-T — selected as the comparison model for this run; CPU training is active
- **Advanced Settings → Data Management:**
  - Split: Training 70% / Validation 20% / Test 10% (default)
  - Expected distribution with 20 images: approximately Training=14, Validation=4, Test=2
  - Geti may round subset counts; confirm each subset has at least one image
  - Geti auto-distributes all "Unassigned" images when you open this dialog — confirm **Unassigned: 0** before proceeding, meaning Geti has placed all 20 images into subsets and none are left floating
- **Advanced Settings → Training:** configured 200 epochs, early stopping patience 10, and learning rate 0.0001
- **Device:** CPU (no GPU on SAM501)
- Click **Start**

### Step 5 — Collect training log
- **Complete:** preserved run artifacts are in `Debug/NVL_Geti_Run/`
- Training job log: `train-c8cd0980-84e1-4aea-b700-5fd185a88c3c.log`
- Model workspace: `getitune-workspace-aa5aafdc-1098-4fdc-99a2-e762d61a85e6/`
- Resource monitoring: `geti-training-utilization.csv` and `geti-training-utilization-processes.csv`

---

## Phase 4b — Inference & Verification

### Step 6 — Collect run artifacts
Before reviewing anything:
- **Complete:** training log, model workspace, copied project files, and both utilization CSVs are preserved in `Debug/NVL_Geti_Run/`
- Screenshot the training result card (model name, mAP, date, dataset size) → `Debug/RunNVL01/RunNVL01_result.PNG`
- Screenshot the Model metrics tab (all numbers visible) → `Debug/RunNVL01/RunNVL01_metrics.PNG`
- Screenshot the Training parameters tab → `Debug/RunNVL01/RunNVL01_params.PNG`
- Screenshot the Training datasets tab (split distribution) → `Debug/RunNVL01/RunNVL01_dataset.PNG`

---

### Step 7 — Read and interpret model metrics

Go to **Models** tab → click the trained model → open **Model metrics** tab.

#### 7a — Check the headline numbers

| Metric | Where to find it | What to check |
|---|---|---|
| mAP@0.5 | Top of metrics tab | Primary score — is it >20%? >30%? |
| mAP@0.75 | Top of metrics tab | Gap vs mAP@0.5 — large gap = sloppy masks |
| mAR@1 | Top of metrics tab | Is model finding any defect at all on first guess? |
| mAR@100 | Top of metrics tab | Upper bound of recall — how many defects can it find at all? |

Record all values in the Run Log table at the bottom of this document.

**NVL Test Run 01 result:** held-out test mAP=22.82%, mAP@0.5=46.53%, mAP@0.75=14.85%, mAR@1=15.71%, and mAR@100=28.57%. The model has useful coarse anomaly-localization signal, but the mAP@0.5 to mAP@0.75 drop and limited recall show that mask boundaries and missed instances need improvement.

#### 7b — Check training vs validation gap (overfitting check)

Geti shows separate scores for training and validation subsets. Compare:

```
Healthy (generalizing well):      Overfitting:
  Training mAP:   65%               Training mAP:   88%
  Validation mAP: 58%    ✓          Validation mAP: 21%    ✗ — big gap
  Gap: 7% — acceptable              Gap: 67% — model memorized training data
```

**If gap > 20%:** Model is overfitting. Fix = add more diverse images before retraining.  
**If both are low:** Model hasn't learned enough. Fix = add more images.  
**If both are reasonable:** Proceed to inference.

#### 7c — Read the training curves

Scroll down in the metrics tab to see the curves:

- **Loss curve:** Should go down smoothly then flatten. If it never dropped → model didn't learn.
- **LR curve:** Should step down 1–2 times. If it stayed flat → scheduler never fired (loss may have plateaued immediately).
- **Training time:** Note how many epochs ran before early stopping fired. If it stopped at epoch 15–20 → patience too low or learning rate issue.

Screenshot the curves → `Debug/RunNVL01/RunNVL01_curves.PNG`

---

### Step 8 — Run predictions on unseen images (visual verification)

This is the most important step — numbers alone don't tell the full story.

#### 8a — Select test images
- Pick **5 images that were NOT in the training set** — these should be new NVL scans
- Include a mix: some with obvious anomalies, some with subtle anomalies, optionally 1 clean image
- Save them locally first so you can compare prediction vs reality side-by-side

#### 8b — Run predictions in Geti
- Go to **Annotate** tab in your project
- Upload the 5 test images
- For each image, click **Predict** (the auto-annotate button, usually a sparkle/wand icon)
- Geti runs the trained model and overlays predicted masks on the image
- Do **not** Submit yet — just observe

#### 8c — Evaluate each prediction visually

For each image, ask these questions and record your observations:

| Question | Good sign | Bad sign |
|---|---|---|
| Is the mask on an actual anomaly area? | Yes — mask matches the defect | No — mask is on a clean region (false positive) |
| Does the mask shape match the defect boundary? | Tight polygon around the defect | Loose blob covering non-defect area |
| Are all visible anomaly spots detected? | Yes | Some defects missed (false negative) |
| Is the confidence score reasonable? | >50% for real defects | <30% on obvious defects = weak model |
| Any predictions on completely wrong areas? | None | Masks appearing on wire bonds, edges, etc. |

Screenshot each prediction (before accepting/rejecting) → `Debug/RunNVL01/Predict_img01.PNG` etc.

#### 8d — Score your visual inspection

After reviewing all 5 images, summarize:

```
Example scoring:
  Image 1: 2 defects present → model found 2 ✓, 0 false positives ✓  → PASS
  Image 2: 1 defect present  → model found 1 ✓, 1 false positive ✗   → PARTIAL
  Image 3: 3 defects present → model found 1 ✓, missed 2 ✗           → FAIL
  Image 4: 0 defects present → model found 0 ✓                       → PASS
  Image 5: 2 defects present → model found 2 ✓, 0 false positives ✓  → PASS

  Visual score: 3 PASS / 1 PARTIAL / 1 FAIL → acceptable for first run
```

Record your visual score in the Run Log.

---

### Step 9 — Make a go/no-go decision

Based on metrics + visual inspection, decide what to do next:

| Result | Decision | Action |
|---|---|---|
| mAP@0.5 >30%, visuals look reasonable | **Go** — proceed to fine-tuning | Accept/correct predictions, add to dataset, retrain |
| mAP@0.5 10–30%, visuals show some signal | **Conditional go** — more data needed | Annotate 20 more images, retrain, compare |
| mAP@0.5 <10%, visuals show random predictions | **No-go** — investigate | Check annotation quality; review training curves; consider tighter polygons |
| Large train/val gap (>20%) | **Overfit** | Add diverse images before retraining; don't fine-tune yet |

---

## Phase 4c — Fine-tuning

### Step 10 — Accept / correct / reject predictions
For each predicted image from Step 8:
- **Accept** predictions that look correct — mask matches the real anomaly
- **Correct** predictions that are close but need adjustment — reshape the polygon to tighten it
- **Reject** predictions that are completely wrong — removes them so the model doesn't learn bad examples
- Click **Submit** — accepted/corrected images are added back into the training dataset and will be included in the next training run

### Step 11 — Add more images if needed
If mAP@0.5 is below ~30% after the first run:
- Annotate additional NVL images (target: work toward 50–100 total)
- Use the predict-review-correct loop to annotate faster — Geti pre-fills the masks, you just verify and correct
- Aim to add images that show defect types the model currently misses (hard examples)

### Step 12 — Retrain and compare
- Repeat Steps 4–9 for each new training run
- Save each run into a new folder: `Debug/RunNVL02/`, `Debug/RunNVL03/`, etc.
- Record mAP@0.5 and visual score per run in the Run Log table below
- Stop iterating when mAP@0.5 >50% and visual inspection passes consistently

---

## Run Log

| Run | Date | Images | Model | mAP@0.5 | Train/Val gap | Visual score | Notes |
|---|---|---|---|---|---|---|---|
| Smoke Test | 2026-08-12 | 5 (delamination only) | RF-DETR-Seg-M | ~1% | — | N/A | Pipeline smoke test — not a real model |
| NVL Test Run 01 | 2026-08-14/15 | 20 (anomaly only; 14/4/2 split) | Mask R-CNN Swin-T | 46.53% | Validation mAP@0.5 peaked at 79.21%; test result is lower, but based on only 2 test images | Pending | Completed after 140 epochs in ~15h 53m; test mAP=22.82%, mAP@0.75=14.85%, mAR@1=15.71%, mAR@100=28.57%; best validation mAP=28.59% at epoch 129; OpenVINO and ONNX exports created |

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
