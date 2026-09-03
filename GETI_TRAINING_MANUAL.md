# Geti Instance Segmentation — Training Manual

**Tool:** Intel Geti™ v3.0 on PVA SAM501  
**Task type:** Instance Segmentation  
**Model family:** RF-DETR-Seg (getitune backend, PyTorch Lightning)  
**Author:** Omkar | **Project:** GeTi CSAM NVL Defect Detection  

**Current deployment note (2026-09-03):** The local inference prototype supports the staged `MobileNetV2-ATSS` Detection deployment and the `Test_Run_Instance_Segmentation` package. The latter is technically an `AnomalyDetection` export with blank task metadata; Python 3.9/OpenVINO 2024.5 loading, inference, and mask rendering passed with an `Anomaly` score of 78.3%. See `Deployment/Geti_CSAM_Inference_GUI/README.md` for operator instructions.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [How to Navigate the Geti Models Tab](#2-how-to-navigate-the-geti-models-tab)
3. [Understanding Accuracy Metrics](#3-understanding-accuracy-metrics)
4. [Reading Training Curves](#4-reading-training-curves)
5. [Training Parameters Reference](#5-training-parameters-reference)
6. [Data Augmentation Explained](#6-data-augmentation-explained)
7. [Dataset Splits — Training / Validation / Test](#7-dataset-splits--training--validation--test)
8. [Model Export Formats](#8-model-export-formats)
9. [Common Problems and How to Fix Them](#9-common-problems-and-how-to-fix-them)
10. [Quick Decision Guide](#10-quick-decision-guide)

---

## 1. Core Concepts

### What is Instance Segmentation?
Instance segmentation means the model draws a **pixel-level mask** around each individual defect it finds — not just a bounding box, but the exact shape.

```
Detection (bounding box):         Instance Segmentation (mask):
┌─────────────────┐               ░░░▓▓▓▓▓▓░░░░░░
│                 │               ░▓▓▓▓▓▓▓▓▓▓░░░░
│   [DELAMINATION]│               ░░▓▓▓▓▓▓▓░░░░░░
│                 │               ░░░░▓▓▓▓░░░░░░░
└─────────────────┘               ░░░░░░░░░░░░░░░

A rectangle around the defect.    The exact defect boundary traced.
```

Why segmentation for CSAM? Delamination has irregular shapes — a bounding box wastes area and makes the model less accurate. A polygon mask tells the model exactly what delamination looks like, not just where it approximately is.

---

### What is IoU (Intersection over Union)?
IoU measures how well a predicted mask overlaps the ground truth mask you drew during annotation.

```
Ground truth mask (what you drew):   ████████
Predicted mask (what the model drew):    ████████

Overlap:                                 █████
Union (total area covered):          ████████████

IoU = Overlap / Union = 5 / 12 = 0.42
```

| IoU value | Meaning |
|---|---|
| 1.0 | Perfect — predicted mask exactly matches what you drew |
| 0.5 | 50% overlap — threshold used for mAP@0.5 |
| 0.75 | 75% overlap — threshold used for mAP@0.75 (stricter) |
| 0.0 | No overlap — completely wrong prediction |

**Example:**
- You annotated a delamination at the top-left of a die image
- The model predicts a mask in roughly the same area but slightly shifted
- If the overlap is 60%, it counts as a correct detection for mAP@0.5 but not for mAP@0.75

---

### What is Precision vs Recall?

These two metrics always trade off against each other.

```
PRECISION — "when the model says there's a defect, is it right?"

   Model predictions:  [DEFECT] [DEFECT] [DEFECT] [DEFECT] [DEFECT]
   Actually defects:   [  ✓   ] [  ✓   ] [  ✗   ] [  ✓   ] [  ✗   ]

   Precision = 3 correct / 5 predictions = 60%
   (2 false alarms out of 5 flags)


RECALL — "of all the real defects, how many did the model find?"

   Real defects in images:  [DEFECT] [DEFECT] [DEFECT] [DEFECT] [DEFECT]
   Model found:             [  ✓   ] [  ✗   ] [  ✓   ] [  ✗   ] [  ✓   ]

   Recall = 3 found / 5 real = 60%
   (missed 2 real defects)
```

**For defect detection:**
- **High recall is more important than high precision** — missing a real delamination (false negative) is worse than a false alarm that a human can dismiss
- Target: Recall > 70%, then improve Precision

---

### What is mAP?
mAP = **Mean Average Precision** — the standard single-number score for detection/segmentation models.

It combines precision and recall across all confidence thresholds and IoU thresholds into one number.

```
mAP@0.5   = Average Precision measured at IoU threshold 0.50
mAP@0.75  = Average Precision measured at IoU threshold 0.75
mAP       = Average of mAP@0.5, mAP@0.55, mAP@0.60 ... mAP@0.95
            (COCO standard — strictest, hardest to achieve)
```

Higher is always better. 100% = perfect model. 0% = useless.

---

## 2. How to Navigate the Geti Models Tab

After training completes, go to **Models** tab in your project. Click any model row to expand it.

```
Models tab layout:
┌──────────────────────────────────────────────────────────┐
│  RF-DETR-Seg-M  |  delamination  |  mAP 0.6%  | 12 Aug  │
│                                                          │
│  ┌──────────────┬────────────────┬──────────────────┐    │
│  │Model variants│ Model metrics  │Training parameters│   │
│  │              │ Training datasets                  │    │
│  └──────────────┴────────────────┴──────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

| Tab | What you'll find |
|---|---|
| **Model variants** | Export buttons for OpenVINO FP32 / FP16 / INT8 formats |
| **Model metrics** | mAP numbers + all training curves — **go here first** |
| **Training parameters** | Exact copy of all settings used — useful for reproducing a run |
| **Training datasets** | Which images were assigned to training / validation / test |

---

## 3. Understanding Accuracy Metrics

### The Main Metrics

| Metric | Full name | What it tests |
|---|---|---|
| **mAP** | Mean Average Precision (COCO) | Overall quality, averaged across IoU 0.5–0.95 |
| **mAP@0.5** | mAP at IoU ≥ 0.50 | "Is the model finding defects in roughly the right place?" |
| **mAP@0.75** | mAP at IoU ≥ 0.75 | "Are the mask shapes tight and accurate?" |
| **mAR@1** | Mean Average Recall, max 1 detection/image | "Does the model find at least one defect per image?" |
| **mAR@10** | Mean Average Recall, max 10 detections/image | "Does the model find most defects when given 10 guesses?" |
| **mAR@100** | Mean Average Recall, max 100 detections/image | "Can the model find defects at all, given many guesses?" |

### What the Numbers Tell You in Practice

**Example A — Good model:**
```
mAP@0.5  = 68%   ← finds most defects in roughly the right place ✓
mAP@0.75 = 41%   ← mask shapes are reasonably tight ✓
mAR@1    = 71%   ← finds a defect in 71% of images on first guess ✓
```

**Example B — Model found signal but masks are sloppy:**
```
mAP@0.5  = 55%   ← ok at rough location ✓
mAP@0.75 = 8%    ← masks are loose — big gap between @0.5 and @0.75 ⚠
mAR@1    = 60%   ← finds defects ok ✓
Fix: tighten polygon annotations, add more examples
```

**Example C — Model is guessing randomly:**
```
mAP@0.5  = 2%    ← not finding defects ✗
mAP@0.75 = 0%    ✗
mAR@100  = 15%   ← even with 100 guesses, misses 85% of defects ✗
Fix: add more annotated images (need 20+ minimum)
```

**Example D — Overfitting (memorized training data, can't generalize):**
```
Training mAP  = 91%   ← performs great on images it was trained on
Validation mAP = 12%  ← performs poorly on images it hasn't seen ← bad
Fix: add more diverse training data; increase augmentation
```

### Quick mAP@0.5 Quality Table

| mAP@0.5 | Model quality | Recommended action |
|---|---|---|
| 0–5% | No learning — not useful | Normal for <10 images. Add more annotated data. |
| 5–20% | Weak signal | Add data; check annotation quality (tight polygons?) |
| 20–40% | Detects some defects | Usable for testing inference. Fine-tune with more data. |
| 40–60% | Solid baseline | Demo-capable. Improve with more data + fine-tuning. |
| 60–80% | Good model | Strong performance. Ready for management demo. |
| 80%+ | Excellent | Production quality for this dataset size. |

---

## 4. Reading Training Curves

All curves are in **Model metrics** tab, scroll below the numbers.

### Learning Rate Curve — "How fast is the model learning?"

```
LR
0.0001 ─────────────┐
                    │ (scheduler cuts LR when loss plateaus)
0.00003             └──────────┐
                              │
0.00001                        └──────────────── (converged)
       0         50         100        150  epoch
```

**Healthy pattern:** LR starts at max, then steps down 1–2 times during training  
**Bad pattern:** LR stays flat and never drops → model never converged, learning rate too low  
**Bad pattern:** LR drops immediately at epoch 1 → learning rate too high, model unstable  

### Training Loss Curve — "Is the model getting better?"

```
Loss
2.0 ─┐
     └──┐
        └───┐
            └────┐
                 └─────────────────── (converged ~0.3)
    0         50         100       150  epoch
```

**Healthy pattern:** Loss decreases smoothly, then flattens  
**Bad pattern:** Loss bounces up and down without decreasing → batch size too small or LR too high  
**Bad pattern:** Loss decreases then suddenly spikes → a bad batch of images or annotation error  

### Validation Loss vs Training Loss — "Is the model overfitting?"

```
Loss
     Training loss ──── (goes down nicely)
     Validation loss ── (goes down then comes back up!)
                                   ↑
                              overfitting starts here
```

If validation loss starts **increasing** while training loss keeps decreasing: the model has memorized the training images and can't generalize. Fix: add more diverse images.

---

## 5. Training Parameters Reference

### Learning Parameters

| Parameter | Default | What it does | When to change |
|---|---|---|---|
| **Maximum epochs** | 200 | Maximum number of full passes through the training dataset. Training stops early via early stopping if no improvement is seen. | Increase to 300–500 for large datasets (100+ images). Leave at 200 for most runs. |
| **Batch size** | 4 | Number of images processed together in each training step. Larger = more stable gradients but needs more memory. | Keep at 4 for CPU. Use 8–16 on GPU. Never exceed available RAM. |
| **Early stopping — Enable** | On | Automatically stops training if the validation loss doesn't improve for `Patience` consecutive epochs. Prevents wasted time. | Always keep On. |
| **Early stopping — Patience** | 15 | How many epochs of no improvement before training stops. | Increase to 20–30 for large datasets where improvement is slow. |
| **Learning rate** | 0.0001 | Controls how aggressively the model updates its weights each step. Too high = unstable/diverging loss. Too low = very slow or no learning. | **Do not change** unless you know what you're doing. Default is well-tuned for RF-DETR. |
| **Weight decay** | 0.0001 | L2 regularization — penalizes large weight values to prevent overfitting. Acts as a gentle brake on the model. | Default is fine. Increase to 0.001 if you see severe overfitting on a small dataset. |

### LR Scheduler

| Parameter | Default | What it does |
|---|---|---|
| **LR scheduler** | Reduce LR on loss plateau | Automatically reduces learning rate when validation loss stops improving. The LR curve drop you see around epoch 20–40 is this scheduler firing. |
| **LR linear warmup** | Off (5 warmup epochs) | Gradually increases LR from 0 to the target at the start of training. Stabilizes early training on large datasets. Turn On for 50+ images. |

### Gradient Accumulation

| Parameter | Default | What it does |
|---|---|---|
| **Gradient accumulation** | Off (1 batch) | Simulates a larger batch size by accumulating gradients over multiple steps before updating weights. Useful when batch size is forced small by memory. Example: accumulate=4 with batch=4 simulates batch=16. |

---

### Intensity Mapping

| Parameter | Default | What it does |
|---|---|---|
| **Intensity mapping mode** | Unit interval scaling | Normalizes all pixel values to the 0–1 range before feeding into the model. Required for consistent training. |
| **Maximum pixel intensity** | 255 | Maximum expected pixel value. 255 is correct for 8-bit images (all our PNG exports from TiffSplitter). If you ever use 16-bit images, change to 65535. |

---

### Annotation Filters

These filter out annotations before training — useful for removing noise.

| Parameter | Default | What it does | Example when to use |
|---|---|---|---|
| **Min annotation pixels** | Off (min=1) | Drops any annotation mask smaller than N pixels. | Set to 50 if you accidentally annotated tiny noise artifacts (< 50px) |
| **Min annotation objects** | Off (min=1) | Drops images that have fewer than N annotations. | Leave Off — don't exclude any images |
| **Max annotation objects** | Off (max=10000) | Drops images that have more than N annotations. | Leave Off |

---

## 6. Data Augmentation Explained

Augmentations create modified copies of your images during training to artificially increase dataset diversity. The model trains on both the original and augmented versions.

**Why it matters for us:** We have a small dataset (30 images for NVL run). Without augmentation, the model sees the same images over and over and memorizes them rather than learning general delamination features.

### Random Zoom Out
```
Original image:                  After zoom out:
┌─────────────────────┐          ┌─────────────────────┐
│                     │          │░░░░░░░░░░░░░░░░░░░░░│
│   [delamination]    │    →     │░░  [delamination] ░░│
│                     │          │░░░░░░░░░░░░░░░░░░░░░│
└─────────────────────┘          └─────────────────────┘
                                   (black border added)
```
- **Setting:** On, probability=0.5, fill=0 (black), side range 1–4
- **Effect:** Randomly shrinks image and pads with black. Teaches the model to detect delamination at different scales and positions within a frame.
- **Probability 0.5:** Applied to 50% of images per epoch.

### IoU Random Crop
```
Original image:                  After crop:
┌─────────────────────┐          ┌──────────┐
│                     │          │          │
│   [delamination]    │    →     │[delam..] │  (random sub-region)
│                     │          │          │
└─────────────────────┘          └──────────┘
```
- **Setting:** On, probability=1.0, min scale 0.3, max scale 1.0
- **Effect:** Randomly crops a portion of the image (between 30% and 100% of original size). Forces model to find defects at different zoom levels.
- **IoU constraint:** Crop is only accepted if it still contains at least some of the annotated defect (uses IoU check to avoid cropping out all annotations).
- **Probability 1.0:** Applied to every image every epoch.

### Random Affine
```
Original image:                  After affine:
┌─────────────────────┐          ┌─────────────────────┐
│   [delamination]    │    →     │  [delamination]     │
│                     │          │  (rotated 8°,        │
└─────────────────────┘          │   shifted slightly) │
                                 └─────────────────────┘
```
- **Setting:** Off by default (rotation ±10°, h-translation ±0.1, scale 0.5–1.5)
- **Effect:** Randomly rotates, translates, and scales the image.
- **When to turn On:** If your CSAM images are always perfectly aligned (same orientation), the model might overfit to orientation. Turning this on forces rotation invariance. Recommended once you have 50+ images.

---

## 7. Dataset Splits — Training / Validation / Test

### What each subset does

```
All annotated images
        │
        ├── Training set (70%)   → Model LEARNS from these images
        │                           Weights are updated based on training loss
        │
        ├── Validation set (20%) → Used DURING training to check progress
        │                           Weights are NOT updated from these
        │                           Early stopping watches validation loss
        │
        └── Test set (10%)       → Used ONLY at the end to report final mAP
                                    Model has never seen these during training
                                    This is the mAP number Geti reports
```

### Why this separation matters

**The problem with testing on training data:**
Imagine you study 10 specific exam questions, then get tested on those same 10 questions. You'd score 100% but learn nothing. The model does the same — if you tested on training data, the mAP would be artificially inflated.

The **test set** is the model's "exam on new material" — it tells you how well the model performs on images it has never seen, which is what matters for real-world use.

### How Geti auto-assigns images

1. Leave all images as **Unassigned** when uploading
2. Set split ratios in Advanced Settings → Data Management (default 70/20/10)
3. Geti randomly distributes images to subsets when training starts
4. Geti reports: "Found X unassigned items — redistributed according to split ratios"

### Minimum requirements

| Dataset size | Training | Validation | Test | Notes |
|---|---|---|---|---|
| 5 images | 3 | 1 | 1 | Smoke test only. mAP unreliable. |
| 10 images | 7 | 2 | 1 | Very small. Expect mAP variance. |
| 30 images | 21 | 6 | 3 | First real run. mAP starts being meaningful. |
| 50+ images | 35+ | 10+ | 5+ | Reliable mAP. Fine-tuning becomes effective. |
| 100+ images | 70+ | 20+ | 10+ | Good model territory. |

### ⚠️ Known getitune limitation
**"No object" / clean images (images with no defect annotations) cannot be in the validation or test set.** getitune's collate function crashes with `ValueError: Boxes batch must have 4 coordinates` when it encounters an empty annotation batch during validation. Workaround: use defect-only images until this is fixed upstream.

---

## 8. Model Export Formats

After training, Geti exports the model to **OpenVINO** format — Intel's inference optimization framework. Three precision levels:

| Format | Size | Speed | Accuracy | Use case |
|---|---|---|---|---|
| **OpenVINO FP32** | Largest (~2× FP16) | Slowest | Reference (full precision) | Accuracy testing / debugging |
| **OpenVINO FP16** | Medium (~66 MB in smoke test) | Fast | Negligible loss vs FP32 | **Recommended for SAM501 deployment** |
| **OpenVINO INT8** | Smallest | Fastest | Small accuracy drop (~1–3%) | Use if inference speed is critical |

**For our use case:** OpenVINO FP16 is the right choice. The SAM501 runs on Intel hardware — OpenVINO is optimized for it. FP16 is standard practice for edge deployment.

### What OpenVINO does
Standard PyTorch model → OpenVINO conversion:
- Removes Python overhead
- Optimizes the compute graph for Intel CPUs/iGPUs
- 2–5× faster inference than raw PyTorch on the same hardware

---

## 9. Common Problems and How to Fix Them

### Problem: Training crashes with `ValueError: Boxes batch must have 4 coordinates`

**Cause:** One or more images in the validation or test subset have no annotations (empty bbox tensor).
This happens when:
- A "No object" / clean image lands in val or test
- An image was partially annotated (label assigned but no polygon drawn)

**Fix:**
- Remove all clean/unannotated images from the dataset
- Ensure every image has at least one submitted polygon annotation (green checkmark in filmstrip)
- Retry training

---

### Problem: mAP is 0–5% after training

**Possible causes and fixes:**

| Cause | How to identify | Fix |
|---|---|---|
| Too few images | Dataset < 10 images | Add more annotated images (target 30+) |
| All images in test set look different from training | Big gap between training and val/test mAP | Add more diverse training images |
| Sloppy polygon annotations | Masks are very loose, don't trace defect edges | Re-annotate with tighter polygons |
| Training crashed early | Log shows early stopping at epoch 5–10 | Check for annotation issues; increase patience |

---

### Problem: mAP@0.5 is ok but mAP@0.75 is near 0%

**Cause:** Model is finding defects in roughly the right location but the predicted mask shapes are loose — they don't tightly match the ground truth.

**Fix:** Re-annotate with tighter polygons. The gap between @0.5 and @0.75 directly reflects annotation tightness.

```
Good annotation:       Sloppy annotation:
  ▓▓▓                    ████████
 ▓▓▓▓▓                  ██▓▓▓████
▓▓▓▓▓▓▓                 ██▓▓▓████   ← lots of non-defect area included
 ▓▓▓▓▓                  ████████
  ▓▓▓
```

---

### Problem: Training loss goes down but validation loss goes up (overfitting)

**Cause:** Model memorized training images instead of learning general delamination features.

**Fix:**
1. Add more training images (most effective)
2. Enable Random Affine augmentation
3. Increase weight decay from 0.0001 to 0.001
4. Reduce max epochs (let early stopping work)

---

### Problem: Geti says "validation subset is empty, no unassigned items to redistribute"

**Cause:** With 3 images and 70/20/10 split, Geti can't populate all 3 subsets (need at least 1 per subset = minimum 3 images, but with one already pre-assigned to training the remaining 2 can only fill one more subset).

**Fix:** Add at least 1 more annotated image (minimum 4 total for a 3-way split).

---

## 10. Quick Decision Guide

### "How many images do I need?"

```
Objective                        Minimum images
─────────────────────────────────────────────────
Confirm pipeline works           5 (smoke test)
First real accuracy reading      30
Demo-ready model                 50–100
Production-quality model         200+
```

### "My mAP is low — what do I do first?"

```
mAP < 5%?
  → Add more images. Nothing else matters yet.

mAP 5–30%, mAP@0.5 >> mAP@0.75?
  → Tighten your polygon annotations.

mAP 5–30%, training mAP >> val mAP?
  → Overfitting. Add more diverse images + enable affine augmentation.

mAP 30–50%?
  → Fine-tune: use predict-review-correct loop to expand dataset faster.
    Add hard examples (images where model is wrong).

mAP > 50%?
  → You have a usable model. Demo it, collect feedback, iterate.
```

### "Which model variant should I pick?"

```
Starting out / smoke test     → RF-DETR-Seg-M (Balance)
Want better accuracy, patient → RF-DETR-Seg-L (same model, larger)
Need fastest inference        → RF-DETR-Seg-S (smaller, faster, less accurate)
Don't use XL on CPU           → Too slow without GPU (hours per run)
```

### "Should I retrain or fine-tune?"

```
Changed annotation schema (new labels, different polygon style)  → Retrain from scratch
Added 10+ new images to existing project                         → Retrain (Geti auto-includes)
Want to compare architectures (M vs L)                           → Two separate training runs
Predictions look good but mAP is low                             → Fine-tune (accept/correct predictions → retrain)
```

---

## Appendix A — Run Records

### Smoke Test Run (2026-08-12)

| Item | Value |
|---|---|
| Run folder | `Debug/Run081226/` |
| Model | RF-DETR-Seg-M |
| Model ID | 39bcb728 |
| Trained | 12 Aug 2026, 10:38 AM |
| Dataset | 5 images — Training 3 (60%) / Validation 1 (20%) / Test 1 (20%) |
| Labels | 1 class: `delamination` |
| Epochs run | ~140 (early stopping, max 200) |
| Training time | ~37 min (CPU) |
| Model size | 705 MB |
| OpenVINO FP16 export | 66 MB |
| mAP | 0.6% |
| mAP@0.5 | 1.4% |
| mAP@0.75 | 0.0% |
| mAR@100 | 40.0% |
| Verdict | Pipeline smoke test ✅ — not a usable model |
| Key finding | "No object" images in val/test split crash getitune. All images must have ≥1 polygon annotation. |

### NVL Test Run 01 (completed 2026-08-14/15)

| Item | Actual value |
|---|---|
| Run folder | `Debug/NVL_Geti_Run/` |
| Model | Mask R-CNN Swin-T |
| Dataset | 20 NVL defect images, all `anomaly`-annotated |
| Labels | 1 temporary class: `anomaly` |
| Split | Training=14, Validation=4, Test=2 |
| Training time | Approximately 15 hours 53 minutes on CPU; 140 epochs |
| mAP@0.5 | 46.53% held-out test result |
| Results | Directional historical baseline; OpenVINO FP16 and ONNX FP16 exports preserved |

---

*Created: 2026-08-12; last updated: 2026-09-03 | Based on Smoke Test Run, NVL Test Run 01 artifacts, Web Geti evidence, local deployment validation, and getitune training logs*
