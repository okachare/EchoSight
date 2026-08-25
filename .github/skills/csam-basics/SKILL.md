---
name: csam-basics
description: "Use for CSAM fundamentals, acoustic microscopy, CSAM scan images, multi-frame TIFF data, image quality, defect appearance, annotations, and choosing Geti task types."
---

# CSAM Basics

Use this skill when an operator needs the domain foundation before preparing data or debugging Geti.

## What CSAM Is

Confocal Scanning Acoustic Microscopy (CSAM) uses acoustic signals to inspect internal interfaces and structures in a sample. The output is an image of acoustic contrast, not a conventional optical photograph. Brightness, texture, boundaries, reflections, and process-related variation can all affect how a defect appears.

CSAM images may originate from different instruments, products, samples, and acquisition workflows. Ask the operator for the relevant hardware and sample context rather than assuming a specific product.

## Image Data Basics

- CSAM acquisition can produce multi-frame TIFF files rather than one standalone image per inspection view.
- A TIFF may contain many frames. Record the source frame count, dimensions, and image mode for each dataset.
- Geti works with individual image files, so multi-frame TIFF data must be split before upload.
- PNG is the preferred training format for this project because it is lossless and preserves acoustic contrast and defect boundaries.
- JPEG can be used when needed, but compression artifacts may affect subtle defect edges. The project splitter supports configurable JPEG quality.
- Keep source TIFF identity, frame number, dimensions, and sample identity whenever possible so annotations and predictions remain traceable.

## Defect Concepts

Defect terminology and label taxonomy are product- and process-dependent. Ask the operator for the approved labels and definitions before annotating. Do not invent, merge, or reinterpret physical defect classes without explicit project-owner approval.

## Annotation Fundamentals

For Instance Segmentation:

- Use one polygon per individual defect instance.
- Trace the visible defect boundary tightly without including unnecessary background.
- Use the correct approved class label.
- Submit every completed image and confirm its completion state.
- Review subtle boundaries, low-contrast regions, and images with multiple defects.
- Keep good-unit images unannotated when they are being used as negative examples for a supported workflow.

For Object Detection:

- Use one bounding box per defect instance.
- Derive the box from the same ground truth used for the segmentation polygon.
- Boxes are faster to annotate but do not preserve exact defect geometry.

For Anomaly Detection:

- Good units define the normal baseline.
- The model flags deviations rather than assigning a known defect class.
- Brightness, texture, orientation, and process drift can create false alarms.

## Choosing a Geti Task

| Task | Best use | Main trade-off |
|---|---|---|
| Instance Segmentation | Engineering review, defect shape, area, and boundary | Highest annotation and compute effort |
| Object Detection | Fast screening and approximate localization | Coarse geometry |
| Anomaly Detection | Unknown-defect alerting and prioritization | Higher false-alarm risk and weaker class interpretation |

The project recommendation is Instance Segmentation for engineering review, Detection for rapid screening, and Anomaly Detection as an alerting layer.

## Image Review Questions

Before upload, ask:

1. Is this the correct sample and frame?
2. Is the image readable, complete, and not corrupted?
3. Is the defect visible in acoustic contrast rather than only in an external reference image?
4. Is this a defect-positive image or a normal/reference unit?
5. Which approved product taxonomy label applies, and how many separate instances are present?
6. Is the image representative, difficult, low contrast, or ambiguous?

## Interpretation Guardrails

- A small dataset can prove that the pipeline works but cannot establish production accuracy.
- Web Geti displayed score values and Windows mAP values must not be treated as equivalent unless their definitions are confirmed.
- Visual review is required alongside metrics because a score does not show mask tightness, missed instances, or false positives.
- Preserve the original image, converted image, annotation decision, and model evidence for reproducibility.
