# Geti Model Parameters & Results Guide

**Reference for:** Intel Geti™ Instance Segmentation — RF-DETR-Seg-M  
**Based on:** Smoke Test Run, 12 Aug 2026 (5 images, delamination class)  

---

## How to Read the Models Tab in Geti

After training, go to **Models** tab. Click the model row to expand. You'll see 4 sub-tabs:

| Tab | What's in it |
|---|---|
| **Model variants** | Export formats available (OpenVINO FP32, FP16, INT8) |
| **Model metrics** | All accuracy numbers + training curves — **most important tab** |
| **Training parameters** | Exact settings used to train this model |
| **Training datasets** | Which images were in training / validation / test |

---

## Model Metrics — What Each Number Means

These are the numbers that tell you how good your model is. All from the **Model metrics** tab.

### Accuracy Metrics

| Metric | What it measures | Smoke test value | Target for NVL |
|---|---|---|---|
| **mAP** | Mean Average Precision across all IoU thresholds (0.5→0.95). Overall single-number summary of model quality. | 0.6% | >50% |
| **mAP@0.5** | Precision when a prediction counts as correct if it overlaps the ground truth mask by ≥50%. Most commonly cited metric. | 1.4% | >50% |
| **mAP@0.75** | Precision with stricter ≥75% overlap required. Tests if masks are tight and accurate, not just roughly correct. | 0.0% | >30% |
| **mAR@1** | Mean Average Recall when only 1 detection is allowed per image. How often the model finds at least one defect. | 0.0% | >50% |
| **mAR@10** | Mean Average Recall allowing up to 10 detections per image. | 0.0% | >50% |
| **mAR@100** | Mean Average Recall allowing up to 100 detections per image. With small datasets this can spike misleadingly. | 40.0% | >50% |

**Plain English:**
- **mAP@0.5 = 1.4%** → the model correctly found ~1 in 70 delamination instances. Expected — only 5 training images.
- **mAR@100 = 40%** → when given 100 guesses per image, the model found 40% of real defects. Shows it has *some* signal.
- **mAP@0.75 = 0%** → predicted masks are not tight — they overlap but not precisely enough. Normal for tiny dataset.

### What "IoU" means
IoU = **Intersection over Union** — measures how much a predicted mask overlaps the ground truth mask you drew.

```
IoU = (overlap area) / (total combined area)

IoU = 1.0  → perfect match
IoU = 0.5  → 50% overlap (threshold for mAP@0.5)
IoU = 0.0  → no overlap at all
```

---

## Training Curves — What to Look For

All visible in the **Model metrics** tab, scroll down.

### Learning Rate Curve
![Learning rate drops at epoch ~20]

- Starts at 0.0001
- **Should drop** when the model stops improving (this is the LR scheduler working correctly)
- In the smoke test: LR dropped sharply around epoch 20, then flattened near 0
- **What you want:** a smooth step-down, not a flat line (flat = model never learned)

### Training Loss (bbox / total)
- Should **decrease over epochs** — if it never goes down, the model isn't learning
- If it goes down then spikes back up → overfitting or bad batch

### Training Data Time / Iteration Time
- Just tells you how fast each step ran — useful for estimating total run time
- In smoke test: ~24 seconds per training iteration on CPU

---

## Training Parameters — What Each One Does

From the **Training parameters** tab. Grouped by section.

### Learning Parameters

| Parameter | Smoke Test Value | What it does | When to change |
|---|---|---|---|
| **Maximum epochs** | 200 | Max training cycles through the dataset. Training stops early if no improvement. | Increase to 300–500 for large datasets; leave at 200 for most runs |
| **Batch size** | 4 | Images processed per training step. | Keep at 4 for CPU. GPU can handle 8–16 |
| **Early stopping — Enable** | On | Stops training automatically if val loss doesn't improve for `Patience` epochs | Always keep On |
| **Early stopping — Patience** | 15 | How many consecutive epochs of no improvement before stopping | Increase to 20–30 for larger datasets |
| **Learning rate** | 0.0001 | How fast the model adjusts weights. Too high = unstable. Too low = slow learning. | Default is fine. Don't touch unless you know what you're doing |
| **Weight decay** | 0.0001 | Regularization — penalizes large weights to prevent overfitting | Default is fine |
| **LR scheduler** | Reduce LR on loss plateau | Automatically cuts learning rate when loss stops improving | Default is correct for most cases |
| **LR linear warmup** | Off (5 warmup epochs) | Gradually increases LR at the start to stabilize early training | Turn On for large datasets (50+ images) |
| **Gradient accumulation** | Off (1 batch) | Simulates larger batch size by accumulating gradients over multiple steps | Turn On if CPU runs out of memory |

### Intensity Mapping

| Parameter | Value | What it does |
|---|---|---|
| **Intensity mapping mode** | Unit interval scaling | Normalizes pixel values to 0–1 range for the model |
| **Maximum pixel intensity** | 255 | Max expected pixel value (correct for 8-bit PNG images) |

### Filters

These filter out annotations that are too small or too large before training.

| Parameter | Value | What it does | When to change |
|---|---|---|---|
| **Min annotation pixels** | Off (min=1) | Removes annotations smaller than N pixels | Turn On if you have noise annotations smaller than ~10px |
| **Min annotation objects** | Off (min=1) | Removes images with fewer than N annotations | Leave Off |
| **Max annotation objects** | Off (max=10000) | Removes images with more than N annotations | Leave Off |

### Augmentations

Augmentations artificially expand your dataset by creating modified versions of your images during training.

| Augmentation | Value | What it does |
|---|---|---|
| **Random zoom out** | On, prob=0.5 | Randomly shrinks the image and fills the border with black (fill=0). Helps model detect small defects |
| **IoU random crop** | On, prob=1, scale 0.3–1 | Randomly crops the image. Forces model to find defects at different scales |
| **Random affine** | Off | Would randomly rotate/translate/scale the image. Off by default |

---

## Training Datasets Tab — Understanding Your Split

From **Training datasets** tab. Shows exactly which images were in each subset.

| Subset | Purpose | Smoke test |
|---|---|---|
| **Training** | Images the model learns from | 3 images (60%) |
| **Validation** | Used during training to check if the model is improving — NOT seen by model during weight updates | 1 image (20%) |
| **Testing** | Held out completely — used only to report final mAP after training finishes | 1 image (20%) |

**Why the split matters:**
- mAP reported in Geti is measured on the **test set** — images the model has never seen
- If your test set is too small (1–2 images), the mAP number is unreliable
- With 30 images at 70/20/10: Training=21, Validation=6, Test=3 — still small but more reliable

---

## Model Variants Tab — Export Formats

| Format | Size | Use case |
|---|---|---|
| **OpenVINO FP32** | Largest | Full precision — use for accuracy testing |
| **OpenVINO FP16** | ~half size (66 MB in smoke test) | Recommended for SAM501 deployment — faster inference, negligible accuracy loss |
| **OpenVINO INT8** | Smallest | Fastest inference — slight accuracy drop, use if speed is critical |

---

## Quick Interpretation Reference — Is My Model Good?

| mAP@0.5 | Interpretation | Action |
|---|---|---|
| 0–5% | Model has not learned anything useful | Normal for <10 images. Add more data. |
| 5–30% | Model has weak signal — finds *some* defects | Add more annotated images, improve polygon quality |
| 30–60% | Usable model — finds most defects with some false positives | Fine-tune: add hard examples, correct bad annotations |
| 60–80% | Good model — reliable detection | Demo-ready range. Can show to management. |
| 80%+ | Excellent | Production-quality. |

**Smoke test (1.4% mAP@0.5):** Expected — 5 images is not enough to train. This run was only to confirm the pipeline works.  
**NVL Test Run target:** >30% with 30 images would be a solid first result. >50% would be excellent for 30 images.

---

## Smoke Test Run Summary (2026-08-12)

| Item | Value |
|---|---|
| Model | RF-DETR-Seg-M (39bcb728) |
| Trained | 12 Aug 2026, 10:38 AM |
| Architecture | RF-DETR-Seg-M (Apache 2.0) — Balance preset |
| Total model size | 705 MB |
| OpenVINO FP16 export | 66 MB |
| Dataset | 5 images — Training 3 (60%) / Validation 1 (20%) / Test 1 (20%) |
| Labels | 1 class: delamination |
| Epochs run | ~140 (early stopping from max 200) |
| mAP | 0.6% |
| mAP@0.5 | 1.4% |
| mAP@0.75 | 0.0% |
| mAR@100 | 40.0% |
| Training time | ~37 min (CPU) |
| Verdict | Pipeline smoke test ✅ — not a usable model |

---

*Created: 2026-08-12 — Based on smoke test run Train2 (Run081226)*
