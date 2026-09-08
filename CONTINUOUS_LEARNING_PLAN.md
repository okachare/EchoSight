# Continuous Learning & Model Improvement Plan for Geti CSAM Anomaly Detection

**Status:** Active (Starting Week 1)  
**Baseline Model:** v1 (~37 images)  
**Target:** Production-ready model with measurable improvement and repeatable evolution workflow  
**Timeline:** Week 1 → Month 1 → Quarter 1 (Sustainable)  

---

## Executive Summary

Transform your 37-image anomaly detection model into a **production-ready, continuously-improving system** through a structured 3-month roadmap:

- **Week 1–2:** Rapid iteration to v2 (proof of concept improvement)
- **Week 3–4:** Quality focus to v3 (production-ready foundation)
- **Month 2:** Sustainable weekly retraining pipeline (v4–v8)
- **Quarter 1:** Production hardening and validated deployment

---

## Part 1: Week 1–2 Action Plan (Get to v2)

### Days 1–7: Collect New Defects from Production

**Objective:** Systematically capture 3–5 new anomalies using EchoSight + operator validation.

**Workflow:**

1. **Deploy v1 to EchoSight** (30 min)
   - Load your current model in EchoSight
   - Configure confidence threshold: **0.5** (catch all potential anomalies initially)

2. **Process Production TIFFs** (Daily, 10 min)
   - Use **TiffSplitter** to convert production TIFF frames → PNG
   - Load PNG batch into EchoSight
   - Run batch inference → Export CSV results

3. **Operator Validation** (Daily, 10–15 min)
   - Review each flagged image in EchoSight
   - Record verdict in spreadsheet:
     ```
     Image_ID | Model_Confidence | Operator_Verdict | Defect_Type | Action
     frame_001| 0.92             | YES (Real)       | Crack       | Add to v2
     frame_002| 0.78             | NO (False Alarm) | - (Normal)  | Log reason
     ```
   - Prioritize: True defects NOT in original 37 images

4. **Triage for Retraining**
   - **High Priority:** Real anomalies your model missed or NEW types
   - **Medium Priority:** Borderline cases (operator uncertain)
   - **Low Priority:** Clear false positives (document root cause)

**Checklist:**
- [ ] v1 model loaded in EchoSight
- [ ] TiffSplitter processing production TIFFs daily
- [ ] Operator validation spreadsheet created
- [ ] 3–5 high-value new images identified
- [ ] Evidence saved to `Debug/Production_Inference_Logs/`

---

### Days 8–10: Prepare & Retrain to v2

**Objective:** Add new images, retrain, and validate improvement.

**Step 1: Prepare Dataset v2** (1 hour)

```
Debug/
├── Baseline_Model_v1/                  (Preserved, frozen)
│   ├── Model_Metrics_v1.txt
│   └── EchoSight_Validation_v1.csv
│
└── Model_v2_Iteration_1/               (New iteration)
    ├── Dataset_Manifest_v2.csv         (37 original + 3–5 new)
    ├── New_Images_Rationale.txt        (Why each new image was added)
    ├── EchoSight_Validation_v1.csv     (10 held-out images, v1 scores)
    └── (Will populate with v2 results after training)
```

**Step 2: Upload & Annotate in Geti Web** (30 min)

1. Open Geti Web → Your project → Media → Upload
2. Select only NEW images (don't re-upload original 37)
3. Annotate each new image:
   - Label as "Normal" (if reference/baseline)
   - Label as "Anomaly" (if defect present)
4. Confirm all images submitted and labeled
5. Screenshot dataset panel

**Step 3: Verify Split Before Training** (15 min)

- [ ] All new images submitted and labeled
- [ ] Original 37-image baseline preserved (not re-annotated)
- [ ] Split visible in Geti: Train %, Validation %, Test % (no empty subsets)
- [ ] Operator confirms readiness

**Step 4: Retrain v2 in Geti Web** (30 min setup + 1–2 hours auto)

1. Geti Web → Models → Train or Create Model
2. Configure:
   - **Task:** Anomaly Detection
   - **Model architecture:** Same as v1 (for direct comparison)
   - **Augmentation:** Disabled for v2 (baseline only)
3. Record Job ID and start time
4. Wait for training (~1–2 hours, background)
5. Capture training completion notification

**Step 5: Test v2 in EchoSight** (1 hour)

1. Export v2 model from Geti Web (OpenVINO format)
2. Load into EchoSight
3. Test on same 10 held-out images used for v1:
   - 5 normal images → Expected low confidence
   - 5 anomaly images → Expected high confidence
4. Compare v1 vs v2 confidence scores
5. Save results to `Debug/Model_v2_Iteration_1/EchoSight_Validation_v2.csv`

**Step 6: Document Improvement** (30 min)

Create comparison table:

```
Metric          | Model v1 (37 images) | Model v2 (37+N images) | Change
Test Precision  | 85%                  | 88%                    | +3%
Test Recall     | 71%                  | 75%                    | +4%
F1 Score        | 77%                  | 81%                    | +4%
Test Set Size   | 7 images             | 10 images              | +3
```

Save to: `Debug/Model_v1_vs_v2_Comparison.txt`

**Evidence Checklist:**
- [ ] Dataset v2 manifest with new image rationale
- [ ] Geti screenshot (image count, split breakdown)
- [ ] Training job ID and timestamps
- [ ] EchoSight validation CSV (v1 vs v2 confidence scores)
- [ ] Metrics comparison table
- [ ] Observation notes (Did v2 improve? Which images got better/worse predictions?)

**Success Criteria:**
- v2 trains successfully without errors
- v2 shows measurable improvement in at least one metric (precision, recall, or F1)
- No retraining failures
- Evidence reproducible and dated

---

## Part 2: Week 3–4 Quality Focus (Build Dataset v3)

### Objective: Create a Robust Foundation for Production

**Key Actions:**

#### 1. Expand Normal/Reference Baseline (Critical for Reducing False Alarms)

**Why:** At 37 images, you likely have class imbalance. Diverse normal images reduce false alarms from process variation.

**Collect 10–15 diverse normal images:**
- Different brightness levels
- Different texture patterns
- Different sample orientations
- Different acquisition dates/instruments (if applicable)
- Different environmental conditions

**Document each:** Reason added, expected value

#### 2. Increase Defect Diversity (Generalization)

**Target:** ≥3 distinct defect types with multiple examples each

Actively seek anomalies that differ:
- Different size/severity
- Different location/orientation
- Different root cause (if product allows)

**Track in manifest:**
```
Image_ID | Defect_Type | Defect_Size | Severity | Num_Similar_Examples | Rationale
img_001  | Crack       | 2mm         | High     | 3                    | Corner location
img_015  | Delamination| 5mm         | Medium   | 2                    | Edge boundary
img_032  | Void        | 1mm         | Low      | 1                    | Rare type, needs expansion
```

#### 3. Annotation Consistency Verification

- Spot-check 10% of dataset for correct labels
- All "Normal" images should have zero marked anomalies
- All "Anomaly" images correctly labeled
- Document any corrections
- Screenshot evidence

---

### Week 3–4 Retraining: v3 with Augmentation

**Dataset:** 35 anomalies + 15–20 normals = 50–55 total images

**Training Configuration:**

```
Task:                    Anomaly Detection
Augmentation Enabled:    YES
├─ Brightness/Contrast:  ±10% brightness, ±15% contrast
├─ Rotation:             ±30° (IF sample orientation varies randomly)
├─ Noise:                σ = 0.03 (CSAM-safe Gaussian noise)
└─ DO NOT USE:           Crop/Pad (destroys acoustic field-of-view)

Epochs:                  [Match v1 setting]
Early Stopping:          Patience = 3–5 epochs (prevent overfitting)
Batch Size:              4–8 (small dataset)
```

**Steps:**

1. Upload new images to Geti Web (15 min)
2. Annotate: "Normal" or "Anomaly" (5 min)
3. Verify split: 70% train, 15% val, 15% test (5 min)
4. Enable augmentation in training settings
5. Start training (30 min setup + 1–2 hours)
6. Export v3 → Load in EchoSight (30 min)
7. Test on 10 held-out images (30 min)
8. Compare v1 vs v2 vs v3 metrics (30 min)
9. **Optimize inference threshold:**
   - Try confidence thresholds: 0.5, 0.6, 0.7, 0.8, 0.9
   - Record: At which threshold do you get best precision/recall tradeoff?
   - Example: "At 0.75, we catch all real defects + only 1 false alarm per 20 normals"
   - Document optimal threshold for production

**Expected Improvement:**
- v3 F1 should improve by 3–5% over v2
- False-alarm rate should decrease (more normals in training)
- Generalization should improve (defect diversity)

**Evidence Folder:**
```
Debug/Model_v3_Week_3/
├── Dataset_Manifest_v3.csv
├── Defect_Diversity_Summary.txt      (3+ types with examples)
├── Normal_Baseline_Curation.txt      (Why each normal image)
├── Annotation_Consistency_Check.txt  (10% reviewed, errors found: 0)
├── Training_Augmentation_Settings.txt
├── Training_Log_v3.txt               (Job ID, epochs, early stop patience)
├── Model_Metrics_v3.txt
├── v1_v2_v3_Comparison.txt           (3-row table: precision, recall, F1)
├── Threshold_Optimization.txt        (Tested 0.5–0.9, optimal = 0.75)
└── EchoSight_Validation_v3.csv       (Same 10 held-out images, v3 scores)
```

---

## Part 3: Month 2+ Sustainable Weekly Loop

### Weekly Retraining Routine (Fridays)

**Time Investment:** ~2 hours active + 1–2 hours automatic training

**Cycle:**

```
Friday Morning:
├─ Collect (15 min)      → 5–10 new images from production
├─ Upload (15 min)       → Batch to Geti Web
├─ Annotate (5 min)      → Label as "Normal" or "Anomaly"
├─ Retrain (30 min)      → Kick off training job
└─ Auto training         → 1–2 hours (background)

Friday Afternoon:
├─ Validate (30 min)     → Test in EchoSight on 10 held-out images
├─ Document (10 min)     → Update metrics dashboard
└─ Evidence (10 min)     → Save to Debug/ folder
```

### Dataset Growth Milestones

| Milestone | Week | Target Size | Anomalies | Normals | Defect Types | F1_Target | False_Alarms |
|-----------|------|-------------|-----------|---------|--------------|-----------|--------------|
| v2 | 1–2 | 42 | 27 | 15 | 1–2 | 81% | <10% |
| v3 | 3–4 | 55 | 35 | 20 | ≥3 | 86% | <5% |
| v4 | 5 | 68 | 43 | 25 | ≥3 | 88% | <3% |
| v5 | 6 | 82 | 52 | 30 | ≥3–4 | 90% | <3% |
| v6–v8 | 7–8 | 100–120 | 65–80 | 35–40 | ≥5 | 92%+ | <2% |

### Monthly Check-In (End of Each Month)

**Month 1 Success Criteria:**
- [ ] Dataset = 65–80 images
- [ ] ≥3 distinct defect types represented
- [ ] F1 score ≥ 85%
- [ ] False-alarm rate in production < 10%
- [ ] Weekly retraining is routine

**Month 2 Success Criteria:**
- [ ] Dataset = 80–100+ images
- [ ] F1 score ≥ 88%
- [ ] False-alarm rate < 5%
- [ ] Production readiness review initiated
- [ ] Operator confidence in model is high

---

## Part 4: Accuracy Improvement Strategies

### Priority 1: Normal Baseline Expansion (Week 3, Low Effort → High Impact)

**Action:** Collect 10–15 diverse reference/normal images  
**Impact:** Immediate reduction in false alarms  
**How:** Different brightness, textures, orientations, acquisition conditions

### Priority 2: Defect Diversity (Week 3–4, Low Effort → High Impact)

**Action:** Ensure ≥3 distinct defect types in dataset  
**Impact:** Model generalizes to new defect patterns  
**How:** Actively seek different sizes, severities, locations, root causes

### Priority 3: Data Augmentation (Week 3, Low Effort → Medium Impact)

**In Geti Training:**
- Brightness/Contrast: ±10% brightness, ±15% contrast (CSAM-safe)
- Rotation: ±30° (if sample orientation random)
- Noise: σ = 0.03 (Gaussian, acoustic-safe)

### Priority 4: Threshold Optimization (Week 3, Very Low Effort → Medium Impact)

**After v3 training, test thresholds 0.5–0.9 in EchoSight:**
- High threshold (0.9) = fewer false alarms, miss some defects
- Low threshold (0.5) = catch more defects, more false alarms
- **Goal:** Find sweet spot (e.g., 0.75)

### Priority 5: Borderline Case Collection (Ongoing, Medium Effort → High Impact)

**Collect images that are hard to judge:**
- Low defect contrast
- Partially-visible defects
- Defects near tolerance boundaries
- Defects unlike any in original 37

**Why:** These teach the model meaningful decision boundaries

### Priority 6: Training Parameter Tuning (Optional, Medium Effort → Low-Medium Impact)

**Focus on:**
- Early Stopping (prevent overfitting with small datasets)
- Learning Rate (if metrics plateau, try 50% lower)
- Batch Size (4–8 for 37–60 images)

---

## Part 5: Tools Integration

### TiffSplitter for Batch Collection

**Weekly Workflow:**
```powershell
# Convert production TIFF → PNG batch
python TiffSplitter.py `
  --input "C:\Production\NewTIFFs\sample_2025_01_15.tif" `
  --output "C:\Production\Extracted_PNGs\" `
  --format png `
  --quality 95

# Verify output: frame count, naming, dimensions
# Move verified PNGs to C:\Production\Staging_For_EchoSight\[YYYY_MM_DD]\
```

### EchoSight for Validation & Active Learning

**Daily Validation Routine:**
1. Load new PNG batch from TiffSplitter
2. Run inference (batch mode, threshold 0.5 initially)
3. Export CSV results
4. Operator reviews each flagged image
5. Triage: High-value images → Staging for retraining

### Geti Web for Retraining

**Weekly Friday Cycle:**
1. Upload new images (15 min)
2. Annotate (5 min)
3. Verify split (5 min)
4. Configure training (5 min)
5. Start training (1–2 hours auto)
6. Export for deployment

---

## Part 6: Evidence Organization

```
Debug/
├── Baseline_Model_v1/
│   ├── Model_Metrics_v1.txt
│   ├── EchoSight_Validation_v1.csv
│   └── Known_Limitations.md
│
├── Model_v2_Iteration_1/
│   ├── Dataset_Manifest_v2.csv
│   ├── New_Images_Rationale.txt
│   ├── Model_v1_vs_v2_Comparison.txt
│   ├── EchoSight_Validation_v2.csv
│   └── Training_Log_v2.txt
│
├── Model_v3_Week_3/
│   ├── Dataset_Manifest_v3.csv
│   ├── Defect_Diversity_Summary.txt
│   ├── Annotation_Consistency_Check.txt
│   ├── Training_Augmentation_Settings.txt
│   ├── v1_v2_v3_Comparison.txt
│   ├── Threshold_Optimization.txt
│   └── EchoSight_Validation_v3.csv
│
├── Model_v4–v8_etc/
│   └── (Same structure per iteration)
│
├── Production_Inference_Logs/
│   ├── Weekly_Summary.txt
│   ├── Production_Inference_Log_[Date].csv
│   ├── High_Value_Images_For_Retraining/
│   └── False_Alarms_Analysis.txt
│
├── Retraining_Logs/
│   ├── Retrain_Log_2025_01_15.txt
│   └── ...
│
├── Defect_Taxonomy.md              (Define defect types)
├── Continuous_Learning_Plan.md    (This document, updated quarterly)
└── Metrics_Dashboard.xlsx          (Weekly tracking: v1 → v8 trend)
```

---

## Part 7: Weekly Metrics Tracking Dashboard

**File:** `Debug/Metrics_Dashboard.xlsx`

| Week | Date | Model | Dataset | Anomalies | Normals | Precision | Recall | F1 | Threshold | False_Alarms | Status |
|------|------|-------|---------|-----------|---------|-----------|--------|-----|-----------|--------------|--------|
| 1 | Jan 15 | v1 | 37 | 22 | 15 | 85% | 71% | 77% | 0.50 | N/A | ✅ Baseline |
| 2 | Jan 22 | v2 | 42 | 27 | 15 | 88% | 75% | 81% | 0.55 | <10% | ✅ Complete |
| 3 | Jan 29 | v3 | 55 | 35 | 20 | 90% | 82% | 86% | 0.70 | <5% | ✅ Complete |
| 4 | Feb 5 | v4 | 68 | 43 | 25 | 91% | 85% | 88% | 0.75 | <3% | ⏳ Ongoing |

---

## Part 8: Quick Start Checklists

### Daily Operator Checklist (EchoSight Validation)

```
☐ Date & Time: _____
☐ TiffSplitter: _____ frames → _____ PNGs processed
☐ EchoSight inference: _____ images tested
☐ Anomalies flagged: _____ (confidence > 0.5)
☐ Operator review:
  ☐ True positives (add to training): _____
  ☐ False positives (false alarms): _____
  ☐ Borderline/uncertain: _____
☐ High-value images saved to: Debug/Production_Inference_Logs/High_Value_Images/
☐ Production validation spreadsheet updated
☐ Evidence archived with date
```

### Weekly Retraining Checklist (Friday)

```
☐ Dataset readiness:
  ☐ New images collected: _____ images
  ☐ Defect diversity documented: _____ types
  ☐ Annotation consistency reviewed
  ☐ Split verified: Train ___%, Val ___%, Test ___%
☐ Training config:
  ☐ Augmentation: Brightness/Contrast ±10%, Rotation ±30°, Noise σ=0.03
  ☐ Early stopping: Patience = 3–5 epochs
  ☐ Epochs: Match v1 setting
☐ Training execution:
  ☐ Job started in Geti Web
  ☐ Job ID recorded: _____
  ☐ Start time: _____
☐ Post-training:
  ☐ Model exported (OpenVINO FP16)
  ☐ Tested in EchoSight on 10 held-out images
  ☐ Metrics captured: Precision __%, Recall __%, F1 __%
  ☐ Comparison to v_N done
  ☐ Threshold optimization: Tested 0.5–0.9, optimal = _____
☐ Documentation:
  ☐ Metrics dashboard updated
  ☐ Evidence folder organized
  ☐ Next week's action items identified
```

---

## Next Steps (Starting Today)

✅ **Today (Day 1):**
- [ ] Capture v1 baseline metrics
- [ ] Test v1 in EchoSight on 10 held-out images
- [ ] Process first production TIFF with TiffSplitter
- [ ] Create operator validation spreadsheet

✅ **This Week (Days 2–7):**
- [ ] Daily: Run EchoSight inference + operator validation (~10 min)
- [ ] Collect 3–5 high-value new anomalies
- [ ] Document each with rationale

✅ **Next Friday (Day 8–10):**
- [ ] Upload new images to Geti Web
- [ ] Retrain v2
- [ ] Validate and compare metrics
- [ ] Save evidence folder

**Timeline to Production:** 12 weeks (3 months) from today

---

**Document Status:** Active | **Last Updated:** 2026-09-08 | **Owner:** Omkar Kachare
