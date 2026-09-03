# NVL Test Run — Step-by-Step Plan

**Project:** Geti AI-Assisted Defect Detection on NovaLake  
**Run Name:** NVL Test Run  
**Planned Date:** 2026-08-16/17 (weekend; completed)
**Goal:** Train first real anomaly detection model on 20 NVL CSAM images and validate inference quality  

> **Platform update (2026-08-19):** The Windows Geti/MSIX workflow is closed and retained for historical reference. The Web Geti workflow is now the active path. Append new training, inference, metrics, and fine-tuning results to the Web Geti sections and do not mix them with the Windows run metrics.

---

## Overview

| Phase | Activity | Target Outcome |
|---|---|---|
| **4a — Training** | Annotate 20 images → train Mask R-CNN Swin-T | Clean training run, mAP baseline established |
| **4b — Inference** | Review metrics → predict on new images | Confirm model detects anomalies on unseen images |
| **4c — Web initial run** | Train, test, and infer in Web Geti | Baseline Web model and first live predictions |
| **4d — Web task comparison** | Compare instance segmentation, bounding-box detection, and anomaly detection on the same 20-image set | Select the best task/model combination for NVL |
| **4e — Web fine-tuning** | Improve the selected model with additional data | Demo-ready accuracy and deployment path |
| **4f — Local GUI deployment** | Load exported model → open multi-frame TIFF → run offline inference | Repeatable WIP inference with visible and exportable results |

---

## Phase 4a — Windows Training (Closed)

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

## Windows Track — Closed

The Windows Geti training run, metrics review, inference attempt, logs, exports, and screenshots are complete historical artifacts. The Windows inference screenshot is preserved at `Debug/NVL_Geti_Run/New folder/Inference Run/nvl_predict.PNG`.

## Web Geti Track — Active

### Web Geti Initial Run

| Activity | Status | Date | Notes |
|---|---|---|---|
| Project and dataset | ✅ Complete | 2026-08-18 | `NVL-S-28C`, Instance Segmentation, 24 images uploaded, two labels visible. |
| Model training | ✅ Complete | 2026-08-18 | `MaskRCNN-EfficientNetB2B` Speed architecture; Versions 1 and 2 created. |
| Dataset split | ✅ Complete | 2026-08-18 | Training 50%, Validation 29%, Testing 21%. |
| Model test | ✅ Complete | 2026-08-18 | Version 2, OpenVINO FP16, 24 images, score 24. |
| Live inference | ✅ Complete | 2026-08-18 | Visible masks included `Delamination` and `Inclusion/Void` predictions. |
| Later model test | ✅ Complete | 2026-08-18 | Version 5, OpenVINO FP16, 25 images, score 78. |
| Result collection | ✅ Complete | 2026-08-25 | Evidence confirms Version 5 OpenVINO FP16 test score 78 on 25 images and visible live-prediction masks; results remain directional because the dataset is small. |

### Web Geti Evidence Inventory

Screenshots are preserved in `Debug/NVL_Geti_WB_Run/`:

| Evidence | Confirmed detail |
|---|---|
| Dataset view | 24 uploaded images in project `NVL-S-28C`; `Upload media`, `Export/Import`, and `Annotate interactively` controls visible |
| Jobs view | Training job for `NVL-S-28C`; data preparation complete, model training and evaluation/inference shown in the job lifecycle |
| Models view | `MaskRCNN-EfficientNetB2B` Speed architecture; Version 2 active at 9% score and Version 1 at 48% score |
| Model variants | OpenVINO FP32 52.79 MB, OpenVINO FP16 27.36 MB, INT8 optimization available; XAI-head FP32 variant also listed |
| Training datasets | Training 50%, Validation 29%, Testing 21% |
| Tests view | Version 2 test: OpenVINO FP16, 24 images, score 24; later Version 5 test: OpenVINO FP16, 25 images, score 78 |
| Live prediction | Upload-based live prediction with visible `Delamination` and `Inclusion/Void` masks and confidence values; captured project score 72% |

## Phase 4d — Web Geti Model Comparison Study

### Objective

Determine whether NVL defect detection is better served by **instance segmentation** or **object detection**, and identify the strongest practical architecture available in Web Geti. The comparison must answer three questions:

1. Which task localizes the defect most accurately: a mask or a bounding box?
2. Which architecture gives the best detection quality on the same NVL images?
3. Which model gives the best balance of quality, inference speed, model size, and deployment suitability on the SAM501 or target host?

This is a controlled benchmark, not a production training run. Do not mix its results with the Windows baseline or the existing 24/25-image Web runs.

### Storage budget and retention rules

The project has approximately **2 TB of available storage**. Apply these rules to every Web run:

- Keep one canonical copy of the 20-image benchmark and its manifest: 14 bad annotated images plus 6 good unannotated images.
- Do not duplicate the same source images into every run folder.
- Keep screenshots for configuration, metrics, representative good/partial/fail predictions, and the final decision; discard redundant captures.
- Preserve job logs and compact metric summaries for every candidate.
- Keep the selected deployment export and record the sizes of other variants before removing them.
- Prefer FP16 for routine inference experiments; retain FP32 or INT8 only when the comparison requires it.
- Record storage usage before and after each comparison run.
- Do not delete historical Windows artifacts without an explicit project decision.

**Required storage record:** run folder size, source dataset size, annotation size, model/export sizes, and remaining free space.

### Evaluation evidence organization

Store all model-comparison results under `Debug/Evaluation/`. Create one folder per candidate model and keep screenshots, prediction outputs, and evaluation notes together:

```text
Debug/Evaluation/
├── Instance_Segmentation/
├── BoundingBox_Detection/
└── Anomaly_Detection/
```

Use stable filenames so results can be compared and found later:

- `01_project_setup.png`
- `02_dataset_split.png`
- `03_training_complete.png`
- `04_model_details.png`
- `05_test_metrics.png`
- `06_prediction_01.png`
- `07_prediction_02.png`
- `08_resource_usage.png`
- `evaluation_notes.md`

If Web Geti requires a substitute architecture, use the actual model name for the folder and record the substitution in `evaluation_notes.md`. Keep only representative prediction screenshots rather than multiple identical captures.

### Experimental design

| Item | Decision |
|---|---|
| Dataset | 20 NVL images: 14 bad/defect-positive images plus 6 good units |
| Image set | Same 20 source images for every candidate; retain stable image IDs |
| Labels | `Delamination` and `Inclusion/Void`, using the current Web taxonomy |
| Segmentation annotation | One polygon per defect instance |
| Detection annotation | One bounding box per defect instance, derived from the same polygons |
| Split | One frozen split reused for every run; target 12 training / 4 validation / 4 testing, stratified by bad/good where possible |
| Training device | Same device for every run |
| Input preprocessing | Same image format, resolution, tiling, and augmentation policy where configurable |
| Training budget | Same maximum epochs and early-stopping policy where configurable |
| Model selection | Select the best checkpoint using validation results only; evaluate once on the frozen test split |
| Repeats | One controlled run per candidate initially; repeat only the finalist if run-to-run variance matters |
| Storage budget | Approximately 2 TB total; retain canonical artifacts and avoid duplicate exports |

Twenty images are a feasibility benchmark and are too small for a production accuracy claim. Leave the 6 good units unannotated; they provide negative/background examples for false-positive evaluation. Report results as directional evidence for model/task selection.

### Selected task shortlist

Evaluate these three task types in Web Geti. Record the exact architecture/model selected for each task after confirming what the Web UI offers:

| Candidate | Task | Intended role | Selection rationale |
|---|---|---|---|
| A | Instance Segmentation | Boundary-accurate defect localization | Best fit for irregular delamination, voids, and cracks; separates individual defect instances |
| B | Object Detection, bounding box | Fast localization baseline | **Selected:** MobileNet; tests whether rectangular boxes are sufficient and practical for deployment |
| C | Anomaly Detection | Normal-versus-abnormal screening | Uses good units as normal examples and tests sensitivity to unknown or unlabeled defect patterns |

For Candidate A, record the selected segmentation backbone. Candidate B is fixed as **MobileNet bounding-box detection**. Do not silently substitute a task or model; record the exact Web Geti MobileNet variant and version.

### Step-by-step execution plan

#### Step 1 - Freeze the benchmark question

**Objective:** Prevent the comparison from changing while runs are in progress.

- Confirm the question is: segmentation versus detection, then architecture selection.
- Confirm the two current labels: `Delamination` and `Inclusion/Void`.
- Record Web Geti project name, Web version, user, date, and available compute device.
- Create a run folder: `Debug/NVL_Geti_WB_Run/Model_Comparison_01/`.
- Create a run register with one row for each candidate.

**Expected result:** A signed-off experiment definition before images are selected.

#### Step 2 - Select and freeze the 20-image dataset

**Objective:** Ensure every model sees exactly the same evidence.

- Select 14 representative bad/defect-positive NVL images and 6 representative good units.
- Include obvious defects, subtle defects, both defect labels where possible, and at least one difficult/low-contrast case.
- Record each image filename, source TIFF/frame, label presence, image dimensions, and defect count.
- Do not replace images after the first model starts.
- Keep a separate copy or manifest of the 20-image set, including a `sample_type` field with `bad` or `good`.

**Expected result:** `nvl_model_comparison_20_images.csv` or equivalent manifest.

#### Step 3 - Create matched annotations

**Objective:** Give segmentation and detection models equivalent ground truth while preserving good units as negative examples.

- For each defect instance, draw a tight polygon for the segmentation task.
- Generate or draw a bounding box enclosing the same instance for the detection task.
- Preserve the same class name and instance count in both task datasets.
- Leave good-unit images unannotated; do not create a `Good` class or draw a shape around the whole unit.
- Review all 14 bad images twice: once for label correctness and once for geometry correctness. Confirm all 6 good units contain no target defect annotation.
- Record any image with ambiguous ground truth and exclude it from the primary score only by documented rule.

**Expected result:** Two matched annotation sets with identical image IDs, classes, and instance counts.

#### Step 4 - Create the three Web Geti projects or task configurations

**Objective:** Keep task and architecture differences isolated.

- Create or configure the segmentation project for Candidate A.
- Create or configure the segmentation project for Candidate B.
- Create or configure the detection project for Candidate C.
- Use identical project metadata and label names where Web Geti permits it.
- Verify that the selected architecture is available before uploading/training.
- Capture screenshots of task type, labels, architecture, device, and training settings.

**Expected result:** Three reproducible Web configurations with no accidental cross-task settings.

#### Step 5 - Apply the same frozen split

**Objective:** Make validation and test results comparable within each task.

- Use the same image IDs in Training, Validation, and Testing for all three candidates.
- Target 6/3/3 for the 12-image study, subject to Web Geti minimum and split constraints.
- If Web Geti forces a different split, use that exact split for all candidates and record it.
- Never compare one model with a different test image set.
- Confirm no images are missing, duplicated, or accidentally reassigned.

**Expected result:** A split table mapping every image ID to the same subset across all runs.

#### Step 6 - Train Candidate A

**Objective:** Establish the accuracy-oriented segmentation reference.

- Select the Swin-based segmentation candidate if available.
- Use the frozen dataset, labels, split, device, and training budget.
- Start training and record job ID, start/end time, epochs, early stopping, and failures.
- Save model version, exported variants, model size, and training screenshots.

**Expected result:** One completed Swin segmentation model with validation and test results.

#### Step 7 - Train Candidate B

**Objective:** Compare the current Web baseline against the Swin segmentation model.

- Select `MaskRCNN-EfficientNetB2B` or its confirmed Web equivalent.
- Repeat the exact data, split, device, and training settings.
- Record all job, model, export, timing, and metric details.

**Expected result:** One completed EfficientNet-based segmentation model evaluated on the same images.

#### Step 8 - Train Candidate B: MobileNet Detection

**Objective:** Establish the MobileNet bounding-box detection baseline.

- Select the available MobileNet detector in Web Geti.
- Use the matched bounding-box annotations, not polygons.
- Repeat the same split, device, and training budget.
- Record model size, export variants, training time, and inference timing.

**Expected result:** One completed MobileNet detection model evaluated on the same images.

#### Step 9 - Run the frozen test set

**Objective:** Produce comparable evidence without changing the models.

- Run each candidate on the same two test images, or the same Web-enforced test set.
- Use the same model variant where possible; record FP32, FP16, or INT8 explicitly.
- Save annotated outputs with a consistent naming scheme, for example:
  - `A_swin_seg_test_01.png`
  - `B_efficientnet_seg_test_01.png`
  - `C_mobilenet_det_test_01.png`
- Do not correct or submit test predictions back into training.

**Expected result:** A side-by-side prediction set for all candidates.

#### Step 10 - Collect quality metrics

**Objective:** Score each model using metrics appropriate to its task.

For segmentation, record:

- mask mAP or the closest Web Geti mask metric
- mAP@0.5 and mAP@0.75 if available
- mask recall / mAR if available
- per-label results for `Delamination` and `Inclusion/Void`
- false positives, missed instances, and mask-boundary quality

For detection, record:

- bounding-box mAP or the closest Web Geti detection metric
- mAP@0.5 and mAP@0.75 if available
- precision, recall, and per-label results
- false positives, missed instances, and box tightness

Do not place a mask mAP and box mAP in one ranking column as though they were identical measurements. Use task-specific quality first, then compare operational usefulness.

#### Step 11 - Measure practical performance

**Objective:** Select a model that can run reliably, not only one with the highest score.

Record for every candidate:

- model architecture and version
- model format and precision: FP32, FP16, or INT8
- model size in MB
- storage used by the run and remaining free space
- training duration
- average inference latency per image
- throughput, if Web Geti reports it
- CPU/RAM utilization, if available
- export/deployment availability
- number of manual corrections required per image

**Expected result:** A quality-versus-cost profile for all three candidates.

#### Step 12 - Perform blinded visual review

**Objective:** Add engineering judgment to the small numerical sample.

- Have the reviewer inspect outputs using image IDs, not candidate names, where practical.
- For each output score localization, class correctness, completeness, boundary/box quality, and false positives on a 0-2 scale.
- Use the same reviewer and rubric for all candidates.
- Record `PASS`, `PARTIAL`, or `FAIL` per image and per candidate.

**Expected result:** A visual score that explains cases where the headline metric is misleading.

#### Step 13 - Select the finalist

**Objective:** Make an explicit model choice for the next NVL iteration.

Use this decision order:

1. Reject candidates with unstable training, invalid exports, or unusable inference.
2. Prefer the candidate with the best task-appropriate test quality and lowest false-negative rate.
3. Use visual boundary quality to break ties between segmentation candidates.
4. Use latency, size, and resource use to break ties between practical deployment options.
5. Select segmentation when boundary shape matters operationally; select detection when localization is sufficient and speed is materially better.

The finalist is a recommendation for the next run, not a production qualification. Twelve bad images do not support a final accuracy claim or clean-image false-positive measurement.

#### Step 14 - Expand and fine-tune the finalist

**Objective:** Confirm that the selected model generalizes beyond the 12-image benchmark.

- Add new NVL images, especially examples corresponding to missed defects and false positives.
- Keep the original 12-image set as a locked regression set.
- Annotate and review the new images using the finalist task.
- Retrain the finalist in Web Geti.
- Compare the expanded-run results against the locked 12-image regression results.

**Expected result:** A better-supported Web model recommendation and a documented path toward the management demo.

### Completed comparison outcome

The updated management deck is the completed comparison record for this phase. It concludes that Detection is the fastest and simplest screening option, Anomaly Detection is best suited to alerting and prioritization, and Instance Segmentation is the recommended engineering-review path because it preserves defect shape and boundary information. The deck records the segmentation baseline as mAP 22.82%, mAP@0.5 46.53%, mAP@0.75 14.85%, with a best validation checkpoint of mAP 28.59% and mAP@0.5 79.21%.

| Candidate | Completed decision | Intended use | Remaining Q4 validation |
|---|---|---|---|
| Detection | Retain as fast-screening option | Rapid triage and localization | Measure task-specific detection quality and latency on expanded data |
| Anomaly Detection | Retain as alerting option | Unknown-defect screening and prioritization | Increase good-unit diversity and calibrate false-alarm threshold |
| Instance Segmentation | Recommended finalist | Engineering review and defect geometry | Fine-tune boundary quality and validate deployment on new NVL scans |

The deck does not provide comparable per-candidate latency, resource, or task-specific metric values. Those measurements remain Q4 execution items and are intentionally not represented as completed results.

### Comparison table template for Q4 measurements

| Candidate | Task | Architecture | Version | Train/Val/Test IDs | Test quality metric | Per-label result | Visual score | Model size | Precision | Avg latency | Training time | Evaluation folder | Decision |
|---|---|---|---|---|---|---|---|---:|---|---:|---:|---|
| A | Segmentation | Swin-based | Q4 | Locked benchmark plus expanded NVL set | Task-specific metric | Per-label results | Visual review | Record | FP16 preferred | Record | Record | `Debug/Evaluation/Instance_Segmentation/` | Finalist validation |
| B | Segmentation | EfficientNetB2B | Q4 | Locked benchmark plus expanded NVL set | Task-specific metric | Per-label results | Visual review | Record | FP16 preferred | Record | Record | `Debug/Evaluation/Instance_Segmentation/` | Engineering comparison |
| C | Detection | MobileNet or confirmed Web equivalent | Q4 | Locked benchmark plus expanded NVL set | Box metric | Per-label results | Visual review | Record | FP16 preferred | Record | Record | `Debug/Evaluation/Detection only/` | Screening comparison |

### Evaluation result template

For each candidate, record:

```text
Candidate:
Task:
Architecture and model version:
Web Geti project:
Dataset manifest:
Split:
Training settings:
Model variant/precision:
Test metric and definition:
Delamination result:
Inclusion/Void result:
False positives:
Missed instances:
Visual score:
Model size:
Average latency:
Training duration:
Export/deployment status:
Decision: continue / reject / finalist
Notes:
```

## Phase 4b — Windows Inference & Verification (Closed)

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

## Phase 4e — Web Fine-tuning

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
- Repeat the selected Web task/model workflow for each new training run
- Save each comparison or fine-tuning run under `Debug/NVL_Geti_WB_Run/`
- Record mAP@0.5 and visual score per run in the Run Log table below
- Stop iterating when mAP@0.5 >50% and visual inspection passes consistently

## Phase 4f — Local Inference GUI Deployment

This phase is active for GUI behavior and output validation. Portable packaging and the standalone installer are deferred until the inference workflow is stable.

### Step 13 — Export and preserve the deployable model

- Export the selected Geti model in the chosen OpenVINO precision, initially FP16 for Intel hardware experiments.
- Preserve the complete model package, including `.xml`, `.bin`, label mapping, task type, model/version, precision, and preprocessing notes.
- Do not treat a checkpoint alone as the deployment package.

### Step 14 — Implement TIFF ingestion and inference

- Open the original `.tif` or `.tiff` without overwriting it.
- Decode multi-frame TIFFs into addressable frames while retaining source filename and frame number.
- Match the training input mode, bit depth, scaling, resizing, and tiling behavior.
- Run the OpenVINO model on each frame and apply the correct task-specific postprocessing: classification labels, detection boxes, or instance-segmentation masks.

### Step 15 — Build and validate the GUI

- Provide model selection, TIFF selection, frame navigation, confidence controls, and result export.
- Display the original frame with overlays and show label, confidence, frame number, and inference time.
- Compare the same frames in the GUI and Geti Web, recording agreement, missed defects, false positives, latency, resource use, and model size.
- Package for Windows only after representative positive, negative, and multi-frame tests pass. **Deferred.**

### Deployment acceptance checklist

- [ ] Complete OpenVINO model package and metadata preserved.
- [ ] Multi-frame TIFF opens and frame count matches the source.
- [ ] GUI preprocessing matches the Geti training/inference contract.
- [ ] Labels and confidence values map correctly.
- [ ] Segmentation masks or detection boxes render at the correct coordinates.
- [ ] Results can be saved with source/frame traceability.
- [ ] GUI output agrees with Geti on representative validation frames.
- [ ] Latency, memory, model size, and failure behavior are recorded.

### Prototype status — 2026-09-02

- GUI workspace created at `Deployment/Geti_CSAM_Inference_GUI/`; staged deployment preserved at `Deployment/Test_Run_Detect/`.
- First Tkinter prototype includes model discovery, image/TIFF import, progress reporting, Results review, confidence filtering, and export.
- The downloaded package is a Detection deployment: `MobileNetV2-ATSS OpenVINO FP16`, CPU target, model version 7.
- The downloaded wrapper is validated with Python 3.9, OpenVINO 2024.5, and `openvino-model-api==0.2.5`; the project Python 3.14/OpenVINO 2026 environment is not compatible with this legacy package.
- Prediction rendering was corrected on 2026-09-02 to use the Geti SDK `DetectionResult.objects` schema; a real model smoke test now displays six detections with confidence values and bounding boxes.
- GUI review improvements are complete: wheel zoom and drag pan, initial confidence threshold 0.10, pastel-green highest-confidence result highlighting, and selected/all result export.
- GUI responsiveness improvements are complete: fixed Analyze/Results dimensions, worker-thread model loading/image decoding/inference, top-right activity animation, and explicit current-frame status for Run All.
- The activity indicator was refined on 2026-09-02 to one spinner glyph; duplicate loading messages were removed, and the progress bar now pulses during the active model call before returning to batch progress.
- TIFF import now reports the current source frame and total frame count; results-panel updates are guarded and worker references are cleared after successful completion.
- UI display fixes are complete: detection labels are measured/clamped to image bounds, Run All uses a smooth determinate fill, and the model information panel displays wrapped metadata without requiring scrolling.
- The GUI review controls now support hiding labels, percentage confidence filtering from 1% to 100%, and model-independent detection/instance-segmentation rendering. Run All, Run Current, and Cancel have distinct outlined pastel styles, and the selected tab is emphasized.
- Activity cleanup now uses an explicit completion event for success, error, and cancellation paths. The complete runtime dependency set remains intentionally preserved; no arbitrary percentage optimization is applied without measuring output parity and latency.
- Portable folder assembly and standalone installer creation are on the backburner until GUI inference and representative TIFF output validation are complete.
- The model summary displays verified deployment metadata including version, labels, precision, size, record date, score, optimization, XAI-head status, and status. The downloaded deployment does not contain the original training-image count, so that value is reported as unavailable.

---

## Run Log

| Run | Date | Images | Model | mAP@0.5 | Train/Val gap | Visual score | Notes |
|---|---|---|---|---|---|---|---|
| Smoke Test | 2026-08-12 | 5 (delamination only) | RF-DETR-Seg-M | ~1% | — | N/A | Pipeline smoke test — not a real model |
| NVL Test Run 01 | 2026-08-14/15 | 20 (anomaly only; 14/4/2 split) | Mask R-CNN Swin-T | 46.53% | Validation mAP@0.5 peaked at 79.21%; test result is lower, but based on only 2 test images | Historical visual review incomplete | Completed after 140 epochs in ~15h 53m; test mAP=22.82%, mAP@0.75=14.85%, mAR@1=15.71%, mAR@100=28.57%; best validation mAP=28.59% at epoch 129; OpenVINO and ONNX exports created |
| Web Geti initial run | 2026-08-18 | 24/25 | MaskRCNN-EfficientNetB2B Speed, OpenVINO FP16 | 78 displayed test score | Earlier test score 24 on 24 images; project/live evidence displayed 69%/72% | Visible masks | Project `NVL-S-28C`; labels `Delamination` and `Inclusion/Void`; later test used Version 5 and 25 images |
| Local GUI smoke test | 2026-09-02 | 1 image | MobileNetV2-ATSS, OpenVINO FP16, model version 7 | Not applicable | Six detections rendered from the Geti SDK wrapper | Single-image smoke validation | Python 3.9/OpenVINO 2024.5; representative multi-frame TIFF parity and latency measurements remain open |

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

*Created: 2026-08-12; last updated: 2026-09-02 — Windows run is historical, Web Geti is active, and local GUI multi-frame validation is in progress.*
