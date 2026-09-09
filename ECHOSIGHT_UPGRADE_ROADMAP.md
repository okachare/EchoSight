# EchoSight Upgrade & Enhancement Roadmap

**Document Date:** 2026-09-09
**Status:** Strategic Planning — Tier 1-4 Features
**Audience:** Principal Engineers, CSAM Data Analysts, Manufacturing Engineering

> **Context:** This roadmap consolidates recommendations from principal firmware engineers, CSAM data analysis experts, and software architects to evolve EchoSight from a standalone inference GUI into a production-grade manufacturing quality control platform integrated with SAM501 CSAM hardware and enterprise manufacturing systems.

---

## Executive Summary

EchoSight is currently a **standalone model inference GUI** with excellent preprocessing, Treeview navigation, and portability. To unlock full manufacturing value, we need three critical capabilities:

1. **Manufacturing integration**: Actionable defect classification, SPC gates, compliance audit trails
2. **CSAM-specific analysis**: Multi-frame statistics, defect geometry, temporal trends
3. **System architecture**: Real-time hardware feedback, batch processing, model deployment automation

Current state: **Production-ready for demo and research use**
Target state (Q4 2026): **Manufacturing quality control platform with SAM501 integration**

---

## TIER 1: Manufacturing Quality Control (High Impact, Do First)

### 1.1 Automated Defect Classification & SPC

**Problem:** Manufacturers need actionable GO/NO-GO decisions, not just confidence scores.

**Solution:**
- **Severity scoring** based on defect type and size (Critical/Major/Minor)
- **Automated accept/reject/hold gates** based on configurable thresholds per defect type
- **Real-time SPC charts**: control limits, trend lines, Cpk/Ppk metrics
- **Defect rate trending**: # defects per wafer/die, rolling 7-day averages
- **Alert thresholds**: Notify operator when defect rate spikes >20% above baseline

**Impact:**
- Enables integration with manufacturing control systems
- Supports compliance documentation and root cause analysis
- Operators get instant pass/fail verdict, not probability scores

**Effort:** Medium (2-3 weeks)
**Dependencies:** SQLite backend (1.2), per-type ROC curves (1.3)

---

### 1.2 Persistent Result Storage & Audit Trail

**Problem:** CSV export is great for one-off analysis but terrible for compliance and queries.

**Solution:**
- **SQLite database** (indexed, queryable, transactional) instead of CSV-only
- **Immutable audit log** with result ID, timestamp, model version, operator, hardware ID
- **Metadata storage**: inference time, GPU utilization, confidence distribution, preprocessing params
- **Query interface** for compliance: "Show me all defects >50% confidence in last 24h for batch ID XYZ"
- **Export flexibility**: still support CSV/JSON for reports, but queries come from database

**Schema outline:**
```sql
results (
  id TEXT PRIMARY KEY,
  timestamp DATETIME,
  model_version TEXT,
  operator_id TEXT,
  hardware_id TEXT,
  image_source TEXT,
  defect_type TEXT,
  confidence FLOAT,
  severity TEXT,
  batch_id TEXT,
  inferred_at_ms FLOAT,
  gpu_memory_mb INT
)

audit_log (
  id INTEGER PRIMARY KEY,
  action TEXT,
  result_id TEXT,
  before_state JSON,
  after_state JSON,
  timestamp DATETIME
)
```

**Impact:**
- Manufacturing compliance: traceable, auditable records
- Root cause analysis: correlate results with batch IDs, production timestamps
- Model comparison: query performance of v1 vs v2 across time

**Effort:** Low-Medium (1-2 weeks)
**Dependencies:** None (foundational)

---

### 1.3 Per-Defect-Type Statistics & ROC Analysis

**Problem:** Single overall confidence threshold doesn't account for different defect types having different error profiles.

**Solution:**
- **Separate confidence histograms** per defect type (Delamination, Void, Crack)
- **ROC curves** showing trade-off between sensitivity (catch rate) and false positive rate
- **Confusion matrix** automatically generated when ground truth available
- **Recommended thresholds** to achieve target sensitivity/specificity (e.g., "99% void detection")
- **Comparison mode**: side-by-side ROC for model v1 vs v2

**Visualization:**
- Per-type histogram with cumulative distribution
- ROC curve plot (interactive: hover to see threshold and metrics)
- Threshold recommendation table: "Set confidence >65% to achieve 98% sensitivity for Delamination"

**Impact:**
- Data-driven threshold selection replaces guesswork
- Different defect types can have different gates (high sensitivity for critical voids, lower for minor scratches)
- Supports A/B model comparison with statistical rigor

**Effort:** Low-Medium (1-2 weeks)
**Dependencies:** SQLite backend (1.2)

---

## TIER 2: CSAM Data Analysis (High Value, Do Early)

### 2.1 Multi-Frame Statistical Aggregation

**Problem:** CSAM produces multi-frame stacks; treating each frame independently misses depth/consistency information and increases false positives.

**Solution:**
- **Frame-by-frame confidence distribution**: histogram across all N frames
- **Aggregated statistics**: max/mean/min/std-dev confidence, count of frames with detection
- **Best/worst frame identification** with visual indicators
- **Defect consistency scoring**: "Defect appears in 8/10 frames → high confidence"; "1/10 frames → likely false positive"
- **Heatmap overlay**: shows defect location frequency across all frames
- **3D profile reconstruction hint**: suggests likely 3D defect geometry based on frame distribution

**Display in Results Tab:**
- New "Stack Analysis" section when TIFF is loaded
- Frame histogram + consistency score
- Heatmap thumbnail showing defect distribution across Z-axis

**Impact:**
- Dramatically reduces false positives (single-frame noise is flagged)
- Enables 3D defect profile understanding
- Operators gain intuition: "Real defects are consistent across frames"

**Effort:** Medium (2-3 weeks)
**Dependencies:** TIFF import handler (already exists), numpy visualization

---

### 2.2 Defect Geometry Quantification

**Problem:** Defect *size* is often more critical than presence for manufacturing decisions.

**Solution:**
- **Auto-compute from Instance Segmentation masks**:
  - Area (pixel count → microns² using configurable scan resolution)
  - Perimeter and aspect ratio
  - Centroid (X, Y in scan coordinates)
  - Distance to die edge (important for electromigration)
  - Overlap with critical regions (power delivery, signal paths)
  
- **Geometric anomaly detection**: flag detections that are impossibly large or have wrong shape
- **Location-based risk stratification**: "Void at die edge is higher risk than center"
- **Structured storage**: persist geometry features in SQLite for querying

**Configuration UI:**
- Scan resolution (µm/pixel) input field
- Critical region definition (polygon mask)
- Geometric thresholds (min/max area, aspect ratio limits)

**Filters in Results Tab:**
- "Show me all voids >100µm²"
- "Show defects in power delivery region only"
- "Sort by area descending"

**Impact:**
- Enables size-based yield loss correlation: "Voids >150µm² correlate with 5% yield loss"
- Supports location-based risk models
- Automatic filtering removes geometrically nonsensical detections

**Effort:** Low-Medium (1-2 weeks)
**Dependencies:** Mask handling (already exists)

---

### 2.3 Temporal Trend Analysis & Model Drift Detection

**Problem:** Manufacturing quality is dynamic; need to catch model degradation or process changes early.

**Solution:**
- **Line chart**: defect rate vs time (rolling 7-day average)
- **Anomaly detection**: alert when defect rate spikes >20% above rolling baseline
- **Model confidence tracking**: alert when avg confidence drops >15% (sign of model drift)
- **Model age indicator**: "v2 deployed 14 days ago, recommend retraining"
- **Side-by-side comparison**: run v1 and v2 in parallel on same incoming images, compare performance
- **Statistical significance test**: "Is improvement real or noise?" (t-test, p-value)

**Dashboard widgets:**
- Defect rate trend chart (with confidence band)
- Model performance comparison cards
- Alert panel showing recent anomalies
- Model version timeline

**Impact:**
- Early warning system: "Retraining recommended"
- Supports quick rollback decision: "Performance degraded → switch to backup model"
- Enables data-driven model promotion: "v2 is statistically better → deploy as primary"

**Effort:** Medium (2-3 weeks)
**Dependencies:** SQLite backend (1.2), time-series visualization library

---

## TIER 3: System Integration & Workflow (Medium-High Value)

### 3.1 Hardware Integration & Real-Time Feedback Loop

**Problem:** Current workflow is manual: scan → export TIFF → run EchoSight → record result. Manufacturing needs semi-autonomous closed loop.

**Solution:**
- **SAM501 USB/Ethernet integration**: auto-poll for new scan files
- **Automatic inference triggering**: detect new TIFF → queue for processing
- **Push results back to SAM501**: write pass/fail and defect coordinates to scan metadata
- **Operator dashboard**: live queue depth, processing latency, throughput (images/min)
- **Bottleneck detection**: queue backup → model too slow or preprocessing inefficient
- **Hardware health monitoring**: GPU temperature, memory usage, inference latency trends

**SAM501 Integration Points:**
```
SAM501 CSAM
    ↓ (USB/Ethernet: poll every 2s)
    ├→ Detect new TIFF: /sam501/scans/batch_123/image_04.tiff
    ├→ Queue to EchoSight inference worker
    ├→ Run inference
    └→ Write results: /sam501/scans/batch_123/image_04.results.json
        {
          "pass_fail": "PASS",
          "defects": [
            {"type": "Void", "x": 240, "y": 180, "confidence": 0.89}
          ]
        }
```

**Impact:**
- Enables continuous scanning while previous frame processes
- Feedback loop accelerates root cause diagnosis (tool offset? contamination? new batch?)
- Throughput monitoring identifies hardware upgrade needs

**Effort:** High (4-5 weeks)
**Dependencies:** SAM501 API documentation, USB driver testing

---

### 3.2 Batch Processing & Throughput Optimization

**Problem:** Manufacturing operates at 1000s of scans/day; per-image GUI interaction is untenable.

**Solution:**
- **Job queue interface**: submit 100-1000 images for batch inference
- **GPU batching**: process N images simultaneously (2-5x faster than sequential)
- **Inference time tracking**: ms/image breakdown (preprocessing, inference, rendering)
- **Throughput dashboard**: current rate, ETA, historical performance
- **Configurable batch size**: auto-tune based on GPU VRAM
- **Progress export**: CSV log of batch processing with per-image stats

**Batch submission UI:**
```
Batch Configuration:
├─ Input folder: /data/scans/batch_001/
├─ Batch size: 16 images/GPU batch
├─ Output folder: /results/batch_001/
├─ Model: v2_FP16
├─ Threshold: 0.65
└─ [Start Processing]
    Progress: 156/1000 images (15% complete)
    Rate: 18.2 img/min
    ETA: 47 minutes
```

**Impact:**
- Targets manufacturing KPI: 500 dies/hour inspection
- GPU utilization monitoring informs hardware decisions
- Removes manual per-image bottleneck

**Effort:** Low-Medium (1-2 weeks)
**Dependencies:** Worker thread pool (partially implemented)

---

### 3.3 Automated Model A/B Testing & Deployment

**Problem:** Current workflow requires manual model swapping and restart; production needs blue/green testing.

**Solution:**
- **A/B test UI**: route N% of incoming images to model v1, rest to v2
- **Real-time comparison**: accuracy metrics side-by-side (confidence, defect count, latency)
- **One-click promotion**: "v2 is 5% better → deploy as primary"
- **Model versioning**: tie predictions to exact model hash (guarantees reproducibility)
- **Automatic rollback**: if model v3 crashes, instant switch back to v2
- **Canary deployment**: start at 5% traffic, gradually increase to 100%

**Model management UI:**
```
Active Model: v2_FP16 (Primary)
├─ Performance: 87% accuracy, avg confidence 0.72, 45ms/image
├─ Deployed: 2026-09-05 (4 days ago)
├─ Predictions: 12,400 images processed

Available Models:
├─ v1_FP16 (Previous): 84% accuracy, can rollback instantly
└─ v3_INT8 (Testing):
    ├─ A/B Status: 10% traffic
    ├─ Performance: 89% accuracy, avg confidence 0.74, 32ms/image
    ├─ [Promote to 50% traffic] [Rollback] [Promote to Primary]
```

**Impact:**
- Production-style deployment without downtime
- Data-driven model promotion reduces regression risk
- Instant rollback capability if needed

**Effort:** High (3-4 weeks)
**Dependencies:** Model versioning, metrics tracking (1.2), worker threading

---

## TIER 4: Software Engineering Excellence (Medium Value)

### 4.1 Model Inference Profiling & Performance Tuning

**Solution:**
- Per-layer timing breakdown (identify slow ops)
- GPU memory tracking
- Automatic optimization suggestions (quantization, pruning, batch size tuning)
- Generate performance report
- Hardware purchase justification: "RTX 4070 sufficient vs 4090"

**Effort:** Low (1 week)

---

### 4.2 Reproducibility & Experiment Tracking

**Solution:**
- Result fingerprinting: given same image + model → guarantee identical predictions
- Preprocessing param storage with results
- Full provenance export: model version, training data, date
- Regulatory compliance documentation

**Effort:** Low-Medium (1-2 weeks)

---

### 4.3 REST API for Manufacturing Systems Integration

**Solution:**
- HTTP endpoint for image submission
- Async job interface
- Webhook notifications
- MES/ERP system integration
- Enables SAP → EchoSight → shopfloor automation

**Effort:** High (3-4 weeks, defer to Q4)

---

## Priority Matrix & Phased Roadmap

### Effort vs Impact

| Feature | Manufacturing Impact | CSAM-Specific | Effort | **Priority** |
|---------|---------------------|--------------|--------|------------|
| Severity + SPC + Gates (1.1) | 🟢🟢🟢 Critical | High | Medium | **TIER 1A** |
| SQLite + Audit Trail (1.2) | 🟢🟢🟢 Critical | High | Low-Medium | **TIER 1A** |
| Per-defect ROC + Thresholds (1.3) | 🟢🟢 High | Critical | Low | **TIER 1B** |
| Multi-frame aggregation (2.1) | 🟢🟢 High | 🟢🟢🟢 Critical | Medium | **TIER 2A** |
| Defect geometry (2.2) | 🟢🟢 High | 🟢🟢 High | Low-Medium | **TIER 2A** |
| Temporal trending (2.3) | 🟢 Medium | Medium | Medium | **TIER 2B** |
| SAM501 integration (3.1) | 🟢🟢 High | 🟢🟢 High | **High** | **DEFER** |
| Batch processing (3.2) | 🟢 Medium | Medium | Low-Medium | **PARALLEL** |
| A/B testing (3.3) | 🟢 Medium | Medium | **High** | **Q4 2026** |
| Profiling (4.1) | Low | Low | Low | **DEFER** |
| Reproducibility (4.2) | 🟢 Medium | Medium | Low | **DEFER** |
| REST API (4.3) | Medium | Low | **High** | **Q4 2026** |

---

## Recommended Implementation Schedule

### **Week 1-2 (Foundation Layer)**
**Goal:** Manufacturing-grade backend infrastructure

- **1.2 SQLite Backend**: Set up database, migration scripts, query interface
- **1.1 SPC Gates**: Implement severity scoring, threshold configuration
- **Parallel:** Start documentation of CSAM requirements

**Deliverable:** Database schema finalized, SPC UI mockup

### **Week 2-3 (Data Science Layer)**
**Goal:** CSAM-specific insights

- **1.3 ROC Curves**: Per-type histogram, threshold recommendations
- **2.1 Multi-frame Aggregation**: Frame consistency scoring, heatmap visualization
- **2.2 Defect Geometry**: Area/perimeter calculation, critical region flagging

**Deliverable:** Can recommend confident thresholds per defect type; understand frame-level consistency

### **Week 3-4 (Operational Layer)**
**Goal:** Trend analysis and optimization

- **2.3 Temporal Trending**: Defect rate charts, model drift detection
- **3.2 Batch Processing**: Job queue, throughput monitoring
- **Testing:** Validate on representative dataset (100+ images)

**Deliverable:** Batch inference mode operational; early warning system functional

### **Week 4-5 (Integration Preparation)**
**Goal:** Hardware readiness

- **3.1 SAM501 Integration**: USB polling, result write-back, operator dashboard
- **Performance profiling**: Identify bottlenecks before hardware commitment

**Deliverable:** Prototype SAM501 integration; performance baseline established

### **Week 5-6 (Polish & Release)**
**Goal:** Production readiness

- **3.3 A/B Testing Framework**: Model versioning, canary deployment
- **Comprehensive testing**: edge cases, failure modes, recovery
- **Documentation**: operator manual, API docs, troubleshooting guide

**Deliverable:** v1.0 Manufacturing Edition ready for pilot deployment

---

## Resource Requirements

### Personnel
- **1x Lead Software Engineer** (full-time, weeks 1-6)
- **0.5x Data Scientist** (for ROC/stats work, weeks 2-4)
- **0.5x Manufacturing Engineer** (for requirements validation, weeks 1-6)
- **0.5x DevOps/QA** (for testing, deployment, weeks 4-6)

### Hardware
- **GPU test system** (RTX 4070 or equivalent) for profiling and batch size tuning
- **SAM501 access** for integration testing (weeks 4-5)

### External Dependencies
- SAM501 API documentation / hardware team coordination
- MES/ERP system API docs (if pursuing REST API in Q4)

---

## Success Metrics

| Metric | Current | Target (Q4 2026) |
|--------|---------|-----------------|
| **Throughput** | N/A (GUI-based) | 500+ images/hour |
| **Defect classification** | Binary (detected/not) | Multi-type with severity |
| **Audit trail** | CSV export only | SQLite with immutable log |
| **Model robustness** | Single version | Versioned with A/B testing |
| **CSAM awareness** | Per-image only | Multi-frame consistency |
| **Hardware integration** | Manual file handling | Auto-polling SAM501 |
| **Operator experience** | Spreadsheet review | Dashboard with alerts |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| SAM501 API unavailability | Defer 3.1 to Q4; implement file-based fallback first |
| GPU memory constraints | Profile early (4.1); enable batch size auto-tuning |
| Model versioning complexity | Start with simple directory structure + hash tracking |
| Scope creep on REST API | Defer to Q4; focus on batch processing first |
| Database migration issues | Automated migration scripts + rollback plan tested early |

---

## References & Related Documents

- **EchoSight GitHub:** https://github.com/okachare/EchoSight
- **Geti CSAM Helper Agent:** https://github.com/okachare/Geti-CSAM-Helper
- **CONTINUOUS_LEARNING_PLAN.md:** 3-month model improvement roadmap
- **PROJECT_STATUS.md:** Current Q3 status and deliverables
- **SCOPE_AND_PROGRESS.md:** Full project history and phase tracking

---

**Next Steps:** Review with team, prioritize based on manufacturing timeline, allocate resources for Week 1-2 foundation work.
