# Continuous Learning & Model Improvement Roadmap

**Status:** Approved for execution | **Date:** 2026-09-08 | **Baseline:** 37-image Anomaly Detection Model v1  
**Owner:** Omkar Kachare, 11943102  
**Timeline:** Week 1–2 (v2), Week 3–4 (v3), Month 1+ (Sustainable Loop), Quarter 1 (Production Ready)  

---

## Executive Summary

Your 37-image anomaly detection model (v1) is a proof-of-concept. This roadmap describes how to evolve it to production-ready status through systematic continuous learning:

- **v1 → v2 (Week 1–2):** Add 3–5 new defects from production, retrain, validate improvement
- **v2 → v3 (Week 3–4):** Expand normal-image baseline (10–20 diverse examples), increase defect diversity (≥3 types), enable augmentation
- **v3 → v4–v8 (Month 1+):** Weekly retraining loop with 5–10 new images/week, sustainable pipeline
- **v5+ (Quarter 1):** Production deployment with monitored continuous learning

**Key Metrics to Track:**
- Dataset size: 37 → 55 → 70 → 100+ images
- Test F1 Score: 77% (v1) → 81% (v2) → 86% (v3) → 88%+ (v4+)
- False-alarm rate: <10% in production (measured weekly)
- Defect types covered: 1 → 2 → 3+ distinct types

---

## Phase 1: Week 1–2 Rapid Iteration (v1 → v2)

### Objective
Prove that adding production data improves the model measurably. Establish baseline metrics and validation procedures.

### Daily Workflow (Days 1–7)
1. **Production capture** (10–20 min/day):
   - Run TiffSplitter on new production TIFF files
   - Load PNGs into EchoSight, run batch inference
   - Operator validates each flagged image: "Real defect or false alarm?"

2. **Data triage**:
   - High priority: True positives NOT in original 37 (new defect examples)
   - Medium priority: Borderline cases (40–70% confidence)
   - Low priority: False alarms (document root cause)

3. **Collection target**: 3–5 NEW, high-value defect images

### Retraining (Days 8–10)
1. **Prepare dataset v2** (37 original + 3–5 new)
2. **Upload to Geti Web** (new images only)
3. **Annotate** as "Normal" or "Anomaly"
4. **Verify split** (70/15/15 train/val/test)
5. **Retrain** model v2 in Geti Web
6. **Export & test** in EchoSight on 10 held-out images
7. **Document** side-by-side v1 vs v2 metrics

### Evidence Folder
```
Debug/Model_v2_Iteration_1/
├── New_Images_Rationale.txt       (Why each was added)
├── Dataset_Manifest_v2.csv        (37 + 3–5 new)
├── Training_Config_v2.txt         (Task, split, augmentation)
├── Training_Job_ID.txt            (Geti job ID, timestamps)
├── Model_Metrics_v2.txt           (Precision, Recall, F1, test size)
├── Model_v1_vs_v2_Comparison.txt (Side-by-side metrics, % improvement)
└── EchoSight_Validation_v2.csv   (10 held-out images, confidence scores)
```

### Success Criteria
- v2 trains successfully
- v2 F1 > v1 F1 (even by 1–2%)
- EchoSight validation shows improvement (higher confidence on known defects, fewer false alarms)
- All evidence saved and dated

---

## Phase 2: Week 3–4 Quality Focus (v2 → v3)

### Objective
Build a robust baseline by diversifying data and improving annotation quality. Target production deployment readiness.

### Key Actions

**1. Expand Normal-Image Baseline (Critical for False-Alarm Reduction)**
- Collect 10–15 diverse "reference" images:
  - Different brightness levels
  - Different texture patterns
  - Different sample conditions/orientations
  - Different acquisition dates/instruments (if applicable)
- **Goal:** Reduce false alarms from process variation

**2. Increase Defect Diversity (Critical for Generalization)**
- Target ≥3 distinct defect types (or size/severity clusters)
- Collect examples of each type with different:
  - Sizes/severity levels
  - Visual patterns
  - Locations on sample
- **Goal:** Teach model meaningful boundaries

**3. Annotation Consistency Check**
- Spot-check 10% of the 37-image v1 dataset
- Verify labels are correct (no mislabeled images)
- Document findings in annotation QC report

**4. Data Augmentation Setup (Geti Training Config)**
- Brightness/Contrast: ±10%
- Rotation: ±30° (if sample orientation varies randomly)
- Gaussian Noise: σ = 0.03
- **Skip:** Crop, pad, JPEG compression (alters acoustic signals)

### Dataset v3 Composition
```
Total: ~55 images
├── Anomalies: 35–40 images (3+ defect types, diverse sizes)
├── Normals: 15–20 images (diverse acquisition conditions)
└── Ambiguous: ~5 borderline cases (for decision boundary learning)
```

### Retraining v3
1. Upload new images to Geti Web
2. Annotate all new images
3. Verify split, confirm augmentation settings
4. Retrain with augmentation enabled
5. Optimize inference threshold (test 0.5–0.9, find best balance)
6. Compare v1 vs v2 vs v3 metrics

### Success Criteria
- Defect diversity documented (≥3 types with examples)
- Normal-image baseline expanded (10–20 diverse examples)
- v3 F1 improvement over v2 (target: +2–3%)
- False-alarm rate in production <5% (at optimized threshold)

---

## Phase 3: Month 1+ Sustainable Loop (v3 → v4–v8)

### Objective
Establish repeatable weekly retraining pipeline. Scale dataset to 80+ images by end of Month 1.

### Weekly Routine (Every Friday)
**Time commitment: ~2 hours active + 1–2 hours automatic training**

1. **Collect new defects** (5–10 min/day × 5 days = 50 min total)
   - Daily EchoSight validation (10–20 min)
   - Triage high-value images
   - Target: 5–10 new images/week

2. **Prepare dataset** (20 min)
   - Create new dataset folder with manifest
   - Organize new images with rationale

3. **Upload & annotate** (15 min)
   - Upload new images to Geti Web
   - Label all images

4. **Retrain** (30 min setup + 1–2 hrs auto)
   - Verify split, confirm augmentation
   - Retrain model v_N+1

5. **Validate & document** (40 min)
   - Export v_N+1, test in EchoSight
   - Compare metrics to v_N
   - Update metrics dashboard
   - Record lessons learned

### Monthly Milestones

| Milestone | Timeline | Dataset Size | Defect Types | Metrics Target | Production Status |
|-----------|----------|--------------|--------------|---|---|
| **Month 1, Week 1** | End of Week 4 (v4) | 68 images | 3+ types | F1 = 88% | On track |
| **Month 1, End** | End of Week 8 (v8) | 80–100 images | 3+ types | F1 = 89%+ | Readiness review |
| **Month 2, Mid** | Week 12 (v12) | 100–120 images | 4+ types | F1 = 90%+ | Pre-production tests |
| **Quarter 1, End** | Week 12+ (v12+) | 120+ images | 5+ types | F1 = 91%+ | **Live deployment** |

### Weekly Summary Template
```
Week N Summary (2026-09-15)
────────────────────────────
New Images Collected: [X] anomalies, [Y] normals
Defect Types: [List 3+ types]
Model Retrained: v_N → v_N+1
Metrics Trend: F1 = X% → Y% (change: ±Z%)
Production Feedback: [False alarms, missed defects, new phenomena]
Action Items: [Next week's focus]
Evidence Location: Debug/Week_N_Summary.txt
```

---

## Phase 4: Quarter 1 Production Hardening (v5+)

### Objective
Finalize training dataset, validate model reliability, deploy to production with continuous monitoring.

### Readiness Checklist

**Dataset (100–120 images):**
- [ ] ≥5 defect types represented
- [ ] Representative severity range for each type
- [ ] Class balance: At least 2:1 ratio anomalies:normals
- [ ] ≥30 diverse normal/reference images
- [ ] Manifest frozen and versioned

**Model Validation:**
- [ ] Test Precision ≥92%
- [ ] Test Recall ≥88%
- [ ] F1 Score ≥90%
- [ ] False-alarm rate <5% at optimized threshold
- [ ] Visual review of all 50+ test predictions (no obvious misclassifications)

**Deployment:**
- [ ] OpenVINO FP16 export tested
- [ ] Inference latency measured (<100 ms/image target)
- [ ] Rollback procedure documented
- [ ] Operator training completed
- [ ] Weekly retraining procedure documented (who, when, how)
- [ ] Escalation path defined (contact name, email, phone)

---

## Accuracy Improvement Strategies (Priority Order)

| Priority | Strategy | Effort | Impact | Timeline |
|----------|----------|--------|--------|----------|
| **1** | Expand normal/reference baseline | Low | High ↓ false alarms | Week 3–4 (v3) |
| **2** | Increase defect diversity (≥3 types) | Low | High ↑ generalization | Week 3–4 (v3) |
| **3** | Data augmentation (brightness, rotation, noise) | Low | Medium ↑ robustness | Week 3–4 (v3) |
| **4** | Threshold optimization (0.5–0.9 range) | Very Low | Medium ↑ precision/recall balance | After each retrain |
| **5** | Collect borderline/ambiguous cases | Medium | High (decision boundaries) | Ongoing (Month 1+) |
| **6** | Hyperparameter tuning (learning rate, batch size) | Medium | Low-Medium | If plateau detected |

---

## Tools & Integration

### TiffSplitter (Weekly Production Image Collection)
```powershell
cd C:\Dev\TiffSplitter
python TiffSplitter.py `
  --input "C:\Production\NewTIFFs\sample_2025_01_15.tif" `
  --output "C:\Production\Extracted_PNGs\" `
  --format png `
  --quality 95
```

### EchoSight (Daily Validation Loop)
1. Load PNGs from TiffSplitter output
2. Run batch inference (EchoSight → Run All)
3. Export CSV results
4. Operator reviews each flagged image
5. Save high-value images to `Debug/Production_Inference_Logs/High_Value_Images/`

### Geti Web (Weekly Retraining)
1. Upload new images
2. Annotate as "Normal" or "Anomaly"
3. Verify split
4. Configure augmentation (brightness/contrast/rotation/noise)
5. Retrain model
6. Export OpenVINO FP16

---

## Metrics Dashboard (Weekly Tracking)

**File:** `Debug/Metrics_Dashboard.xlsx`

| Week | Date | Model | Dataset | Anomalies | Normals | Precision | Recall | F1 | Threshold | False_Alarms | Status |
|------|------|-------|---------|-----------|---------|-----------|--------|-----|-----------|--------------|--------|
| 1 | Jan 15 | v1 | 37 | 22 | 15 | 85% | 71% | 77% | 0.50 | 2/50 | ✅ Complete |
| 2 | Jan 22 | v2 | 42 | 27 | 15 | 88% | 75% | 81% | 0.55 | 2/50 | ✅ Complete |
| 3 | Jan 29 | v3 | 55 | 35 | 20 | 90% | 82% | 86% | 0.70 | 1/50 | ✅ Complete |
| 4 | Feb 5 | v4 | 68 | 43 | 25 | 91% | 85% | 88% | 0.75 | 1/60 | ✅ Complete |
| 5 | Feb 12 | v5 | 82 | 52 | 30 | 93% | 87% | 90% | 0.75 | 1/70 | ⏳ In Progress |

**Tracking Formula:**
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

**Red Flags:**
- Metric decline (v_N+1 < v_N) → Check annotation errors, class imbalance
- No improvement after 2 weeks → Check defect diversity, threshold tuning
- False-alarm surge → Check for process drift, need new normal examples

---

## Evidence Organization

```
Debug/
├── Baseline_Model_v1/
│   ├── Model_Metrics.txt
│   ├── EchoSight_Validation_v1.csv
│   └── Known_Limitations.md
│
├── Model_v2–v8_etc/
│   └── [Same structure for each iteration]
│
├── Production_Inference_Logs/
│   ├── Week_1_Summary.txt
│   ├── High_Value_Images_For_Retraining/
│   ├── False_Positives_Analysis/
│   └── Production_TIFF_Archive/
│
├── Retraining_Logs/
│   ├── Retrain_Log_2025_01_15_15_30_45.txt
│   └── ...
│
├── Defect_Taxonomy.md            (Approved labels + definitions)
├── Metrics_Dashboard.xlsx         (Weekly tracking v1 → v8+)
└── Production_Deployment_Guide.md (Final model, threshold, latency)
```

---

## Quick Reference Checklists

### Daily Operator (EchoSight Validation)
- [ ] Date: _____
- [ ] Time spent: _____ min
- [ ] TIFF processed via TiffSplitter: _____ PNGs generated
- [ ] EchoSight inference run: _____ images
- [ ] Anomalies flagged: _____ (>0.5 confidence)
- [ ] True positives (new): _____ images
- [ ] False positives: _____ images
- [ ] High-value images saved: Debug/Production_Inference_Logs/High_Value_Images/

### Weekly Retraining (Friday Before Training)
- [ ] New images collected: _____ images
- [ ] Dataset manifest created: Dataset_Manifest_v_N.csv
- [ ] Defect diversity documented: _____ types
- [ ] New images uploaded & labeled in Geti
- [ ] Split verified: Train ___%, Val ___%, Test ___% (no empty subsets)
- [ ] Augmentation enabled: Brightness/Contrast ±10%, Rotation ±30°, Noise σ=0.03
- [ ] Training started: Job ID = _____
- [ ] Expected completion: _____

### After Training (Metrics Comparison)
- [ ] Model v_N+1 exported (OpenVINO FP16)
- [ ] Metrics captured: Precision ___%, Recall ___%, F1 ___%, Test size _____
- [ ] v_N+1 tested in EchoSight (10 held-out images)
- [ ] Improvement observed: Yes/No/Partial
- [ ] Threshold optimized: ___ (tried 0.5–0.9)
- [ ] Evidence saved to Debug/Model_v_N+1/
- [ ] Metrics dashboard updated
- [ ] Next week's action items identified

---

## FAQ & Troubleshooting

**Q: How do I know when to retrain?**  
A: Retrain when: (1) 3–5+ new valuable defects collected (weekly recommended), (2) False-alarm rate increasing, (3) Operator reports new defect type missed, (4) After 4+ weeks if plateau detected. Don't retrain after every single image.

**Q: My metrics went down after adding new images. What happened?**  
A: Likely causes: (1) Annotation errors in new images, (2) Class imbalance shifted, (3) Small test set variance (try again). Fix: Spot-check annotations, rebalance classes, collect more data.

**Q: How do I know if I have enough data?**  
A: Good signs: (1) Metrics plateau after 2–3 weeks, (2) False-alarm rate stable, (3) Operator confidence high. Consider 80–100 images a solid starting point for production. 120+ gives high confidence.

**Q: Should I keep all model versions?**  
A: No. Keep: (1) v1 (baseline), (2) v3 (first quality gate), (3) Latest (v_N). Archive older versions to storage. Keep evidence (metrics, validation results) for all versions in `Debug/`.

---

## Success Criteria (End of Quarter 1)

✅ Dataset: 120+ images with 5+ defect types  
✅ Model: F1 ≥90%, Precision ≥92%, Recall ≥88%  
✅ False-alarm rate: <5% in production  
✅ Deployment: Live model with documented rollback procedure  
✅ Operations: Weekly retraining routine established and automated  
✅ Team: Operator trained on continuous learning workflow  
✅ Evidence: Complete audit trail from v1 → v8+ with all metrics and decisions documented  

---

## Next Immediate Actions (This Week)

1. **Today:** Capture baseline v1 metrics, validate in EchoSight
2. **This week:** Start daily production image collection (TiffSplitter + EchoSight)
3. **Days 8–10:** Prepare dataset v2, retrain, validate improvement
4. **Week 3:** Expand normal baseline, increase defect diversity
5. **Week 4:** Retrain v3, optimize threshold, move to weekly sustainable loop

**Owner:** Omkar Kachare  
**Reviewed:** 2026-09-08  
**Status:** Approved for execution  
