---
name: geti-setup-helper
description: "Use for Geti CSAM pre-work, Web Geti access, project setup, TIFF-to-image conversion, TiffSplitter, dataset readiness, labels, annotations, splits, RTC/readiness checks, evidence capture, and starting a reliable Geti run."
---

# Geti Setup Helper

Use this skill before an operator creates or starts a Geti CSAM training run. The goal is to prevent avoidable upload, annotation, split, access, and reproducibility failures.

## Access and Application Links

- Geti access request: `http://goto/getiapply`
- Web Geti application: `http://goto/cdgeti`
- Current active platform: Intel Geti Web
- Project owner and primary agent author: Omkar Kachare, 11943102

If access fails, capture the browser message and confirm the operator is signed in to the required Intel environment. Do not guess permissions or bypass authentication.

## Pre-Work Sequence

Complete these checks in order:

1. Confirm the sample, product, scan date, and operator.
2. Confirm Geti Web access using the links above.
3. Identify the source TIFF file and preserve its original location and filename.
4. Inspect TIFF frame count, image mode, dimensions, and readability.
5. Split multi-frame TIFF data into individual PNG or JPEG images with `TiffSplitter`.
6. Review converted outputs for missing frames, corruption, wrong orientation, and unusable contrast.
7. Select representative defect-positive and good-unit images without changing the set after training begins.
8. Decide and document the taxonomy before annotation. Current Web labels are `Delamination` and `Inclusion/Void`.
9. Choose the Geti task: Instance Segmentation for engineering review, Detection for screening, or Anomaly Detection for normal-versus-abnormal alerting.
10. Prepare the manifest and evidence folder before uploading.
11. Create the Web project and confirm task type, labels, model family, and settings.
12. Upload a small smoke sample first when the workflow or operator is new.
13. Annotate, review, and submit every image before training.
14. Confirm split membership and verify no unintended empty subset exists.
15. Capture the pre-run checklist and start the run only after readiness is complete.

## TiffSplitter

The project tool is `TiffSplitter/TiffSplitter.py`.

Use it to convert multi-frame CSAM TIFF output into individual image files. Prefer PNG for training because it is lossless. Use JPEG only when a smaller file is required, and record the quality setting.

After conversion, verify:

- Expected frame count equals generated output count.
- Files open successfully.
- Image dimensions are consistent or documented.
- Image mode is preserved or intentionally converted.
- Naming retains source/sample/frame traceability.
- No duplicate, missing, blank, or accidentally overwritten outputs exist.

Do not delete source TIFF files. Avoid duplicating the full dataset unnecessarily because the project has an approximately 2 TB storage constraint.

## Dataset and Annotation Readiness

For each image, record at minimum:

- Stable image ID and filename.
- Source TIFF and frame number when known.
- Product/sample identity.
- Good or defect-positive status.
- Image dimensions and conversion format.
- Defect label and instance count.
- Ambiguity or exclusion notes.

For Instance Segmentation:

- Draw one polygon per defect instance.
- Use tight, consistent boundaries.
- Submit all images and confirm completion.
- Review subtle, low-contrast, and multi-instance examples twice.

For Detection:

- Draw one bounding box per defect instance.
- Use the same class and instance count as the segmentation ground truth when comparing tasks.

For Anomaly Detection:

- Use diverse good-unit examples as the normal baseline.
- Record expected false-alarm conditions such as brightness, texture, orientation, and process variation.

## Split Readiness

Before training:

- Confirm the intended train/validation/test percentages or image IDs.
- Confirm every required subset has images.
- Confirm no image is missing, duplicated, or accidentally assigned.
- Treat clean or `No object` images carefully. The legacy Windows `getitune` path crashed when empty annotations landed in validation or test. Verify the Web workflow before using clean images for formal scoring.
- Keep a frozen benchmark and manifest for model comparisons.

## RTC / Readiness Check

Use this as the pre-run readiness checklist. Interpret RTC as the documented readiness/technical-control check for the run; if the local organization uses a different RTC meaning or form, follow that process and record the reference.

- [ ] Access confirmed.
- [ ] Source TIFF preserved.
- [ ] Frame conversion completed and output count verified.
- [ ] Image quality and dimensions reviewed.
- [ ] Dataset manifest created.
- [ ] Labels approved.
- [ ] Task type selected.
- [ ] Annotation rules agreed.
- [ ] All required annotations submitted and reviewed.
- [ ] Split verified.
- [ ] Project/model settings captured.
- [ ] Storage location and evidence folder selected.
- [ ] Training impact understood and operator approval obtained.

Do not start training while a readiness item is unknown. Resolve it or explicitly record it as an accepted risk.

## Evidence to Capture

Save concise, representative evidence under the relevant `Debug/` folder:

- Project setup and task type.
- Labels and annotation examples.
- Dataset count and split.
- Training configuration and completion.
- Model version and export precision.
- Test metrics and their definition.
- Representative good, partial, and failed predictions.
- Resource use, latency, and model size when available.
- Error logs and the final decision.

Prefer OpenVINO FP16 for routine Intel edge-inference experiments. Retain FP32 or INT8 only when needed for comparison or deployment qualification.

## Common Setup Failures

| Symptom | Likely cause | First check |
|---|---|---|
| Cannot access Web Geti | Access or authentication issue | Open the access page and application link; capture exact message |
| Wrong number of images after conversion | TIFF frame or splitter issue | Compare source frame count with generated files |
| Images look compressed or boundaries are unclear | JPEG compression | Reconvert to PNG or increase JPEG quality |
| Training crashes with empty boxes | Empty annotation in validation/test | Check labels and split membership; legacy workaround is defect-only data |
| Model learns poorly | Too few, ambiguous, or inconsistent examples | Review labels, boundaries, class balance, and representative coverage |
| Predictions are invisible or weak | Wrong model/version, threshold, or poor generalization | Confirm model variant, test image, confidence threshold, and visual evidence |

## Completion Criteria

A setup is complete only when the operator can identify the source data, reproduce the conversion, open the Web project, explain the labels and task, show the split, and point to the saved pre-run evidence. A training job starting is not by itself proof that setup was successful.
