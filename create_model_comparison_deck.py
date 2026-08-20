from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.dml.color import RGBColor
from PIL import Image

root = Path(r"\\datagrovera.ra.intel.com\QR_MD6_QRE\Users\Omkar_RA_Datagrove\Work\Dev\GeTi CSAM")
output_path = root / "GeTi_CSAM_Model_Comparison_Deck.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(18, 46, 77)
BLUE = RGBColor(16, 87, 174)
GREY = RGBColor(74, 85, 96)
LIGHT = RGBColor(244, 247, 250)
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(39, 174, 96)
ORANGE = RGBColor(230, 126, 34)
RED = RGBColor(192, 57, 43)


def add_background(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = LIGHT


def add_title(slide, title, subtitle=None):
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9.5), Inches(0.7))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.alignment = PP_ALIGN.LEFT
    run = p.runs[0]
    run.font.name = 'Aptos'
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = NAVY

    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.83), Inches(10.5), Inches(0.35))
        tf2 = sub_box.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = subtitle
        p2.alignment = PP_ALIGN.LEFT
        run2 = p2.runs[0]
        run2.font.name = 'Aptos'
        run2.font.size = Pt(10)
        run2.font.color.rgb = GREY


def add_footer(slide, text):
    footer = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(12.2), Inches(0.25))
    tf = footer.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.RIGHT
    r = p.runs[0]
    r.font.name = 'Aptos'
    r.font.size = Pt(8.5)
    r.font.color.rgb = GREY


def add_left_text(slide, title, bullets, left=0.55, top=1.25, width=6.3, height=5.1, color=WHITE, border=BLUE):
    box = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.color.rgb = border
    box.line.width = Pt(1.0)

    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.08)
    tf.margin_bottom = Inches(0.08)

    p = tf.paragraphs[0]
    p.text = title
    p.alignment = PP_ALIGN.LEFT
    p.runs[0].font.name = 'Aptos'
    p.runs[0].font.size = Pt(15)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = BLUE

    for line in bullets:
        p2 = tf.add_paragraph()
        p2.text = line
        p2.level = 0
        p2.bullet = True
        p2.alignment = PP_ALIGN.LEFT
        p2.runs[0].font.name = 'Aptos'
        p2.runs[0].font.size = Pt(11)
        p2.runs[0].font.color.rgb = NAVY
        p2.space_after = Pt(4)


def add_image_with_ratio(slide, image_path, left, top, max_width, max_height):
    p = Path(image_path)
    if not p.exists():
        return
    try:
        with Image.open(p) as img:
            width, height = img.size
    except Exception:
        return

    ratio = min(max_width / width, max_height / height)
    draw_w = width * ratio
    draw_h = height * ratio
    slide.shapes.add_picture(str(p), Inches(left), Inches(top), Inches(draw_w), Inches(draw_h))


def add_metric_boxes(slide):
    add_metric_box(slide, Inches(0.6), Inches(1.15), Inches(1.9), Inches(0.9), 'Benchmark', '20', GREEN)
    add_metric_box(slide, Inches(2.7), Inches(1.15), Inches(1.9), Inches(0.9), 'Bad', '14', ORANGE)
    add_metric_box(slide, Inches(4.8), Inches(1.15), Inches(1.9), Inches(0.9), 'Good', '6', BLUE)
    add_metric_box(slide, Inches(6.9), Inches(1.15), Inches(2.2), Inches(0.9), 'Segm.', 'mAP 22.82%', RED)
    add_metric_box(slide, Inches(9.35), Inches(1.15), Inches(2.1), Inches(0.9), 'Web', '24→78', GREEN)


def add_metric_box(slide, left, top, width, height, label, value, color):
    box = slide.shapes.add_shape(1, left, top, width, height)
    box.fill.solid(); box.fill.fore_color.rgb = color; box.line.color.rgb = color
    tf = box.text_frame
    tf.margin_left = Inches(0.05); tf.margin_right = Inches(0.05); tf.margin_top = Inches(0.04); tf.margin_bottom = Inches(0.04)
    p = tf.paragraphs[0]
    p.text = label
    p.alignment = PP_ALIGN.CENTER
    p.runs[0].font.name = 'Aptos'; p.runs[0].font.size = Pt(9); p.runs[0].font.bold = True; p.runs[0].font.color.rgb = WHITE
    p2 = tf.add_paragraph(); p2.text = value; p2.alignment = PP_ALIGN.CENTER; p2.runs[0].font.name = 'Aptos'; p2.runs[0].font.size = Pt(15); p2.runs[0].font.bold = True; p2.runs[0].font.color.rgb = WHITE


def add_process_flow_slide(title, subtitle, bullets):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_title(slide, title, subtitle)
    add_footer(slide, 'Technical workflow: benchmark freeze → annotation → training → evaluation → selection')

    add_left_text(slide, 'Technical flow', bullets, left=0.55, top=1.5, width=5.8, height=4.2)

    boxes = [
        ('Dataset freeze', 7.15, 1.8, 1.5, 0.9, BLUE),
        ('Annotation', 8.95, 1.8, 1.5, 0.9, GREEN),
        ('Training', 10.75, 1.8, 1.5, 0.9, ORANGE),
        ('Evaluation', 7.9, 3.4, 1.8, 0.9, RED),
        ('Decision', 9.9, 3.4, 2.0, 0.9, NAVY),
    ]

    for label, left, top, width, height, color in boxes:
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        box.fill.solid(); box.fill.fore_color.rgb = color; box.line.color.rgb = NAVY; box.line.width = Pt(1.0)
        tf = box.text_frame; tf.word_wrap = True; tf.margin_left = Inches(0.08); tf.margin_right = Inches(0.08)
        p = tf.paragraphs[0]; p.text = label; p.alignment = PP_ALIGN.CENTER; p.runs[0].font.name = 'Aptos'; p.runs[0].font.size = Pt(9); p.runs[0].font.bold = True; p.runs[0].font.color.rgb = WHITE

    connectors = [
        (7.15 + 1.5, 2.25, 8.95, 2.25),
        (8.95 + 1.5, 2.25, 10.75, 2.25),
        (7.9 + 1.8, 3.85, 9.9, 3.85),
        (9.9 + 2.0, 3.85, 11.9, 3.85),
    ]
    for x1, y1, x2, y2 in connectors:
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        line.line.color.rgb = NAVY
        line.line.width = Pt(1.0)
        line.line.end_arrowhead = True

    image_candidates = [
        root / 'Debug' / 'Evaluation' / 'Detection only' / 'All_Models.png',
        root / 'Debug' / 'Evaluation' / 'Instance Segmentation' / 'All_Models.png',
        root / 'Debug' / 'Evaluation' / 'Anomaly only' / 'All_Models.png',
    ]
    for img in image_candidates:
        if img.exists():
            add_image_with_ratio(slide, img, 7.1, 4.65, 5.5, 1.7)
            break


# Overview slide
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_title(slide, 'GeTi CSAM NVL DOE', 'Defect detection experiment: setup, run plan, and model selection criteria')
add_footer(slide, 'Benchmark: 20 NVL images, same frozen evaluation basis across all 3 model families')
add_metric_boxes(slide)

add_left_text(slide, 'DOE objective', [
    'Compare 3 model families on the same NVL CSAM dataset.',
    'Answer which task is best for screening, localization, and engineering review.',
    'Quantify trade-offs in accuracy, speed, complexity, and deployment fit.'
], left=0.55, top=1.9, width=3.7, height=2.5)

add_left_text(slide, 'Run setup', [
    'Dataset: 20 NVL images = 14 defect-positive + 6 good units.',
    'Labels: Delamination and Inclusion/Void under the current Web Geti taxonomy.',
    'Design: one frozen split reused across all tasks; equal data and evaluation basis.',
    'Device: same training environment and same run constraints for each candidate.'
], left=4.6, top=1.9, width=3.7, height=2.5)

add_left_text(slide, 'What we are testing', [
    'Detection = fast defect presence + bounding-box localization.',
    'Anomaly = abnormality screening when defect taxonomy is incomplete.',
    'Segmentation = pixel-level masks for geometry and engineering detail.'
], left=8.65, top=1.9, width=3.7, height=2.5)

add_left_text(slide, 'Experiment flow', [
    '1) Freeze the benchmark and image set.',
    '2) Run matched training for each model family.',
    '3) Evaluate on the same test split and compare metrics.',
    '4) Select the best task for deployment and technical follow-up.'
], left=0.6, top=4.75, width=11.9, height=1.6)

# right-side image area
image_path = root / 'Debug' / 'Evaluation' / 'Detection only' / 'All_Models.png'
if not image_path.exists():
    image_path = root / 'Debug' / 'Evaluation' / 'Instance Segmentation' / 'All_Models.png'
if not image_path.exists():
    image_path = root / 'Debug' / 'Evaluation' / 'Anomaly only' / 'All_Models.png'
if image_path.exists():
    add_image_with_ratio(slide, image_path, 4.8, 5.8, 3.6, 1.2)

# Technical workflow slide
add_process_flow_slide(
    'Technical workflow',
    'Benchmark freeze → annotation → training → evaluation → decision',
    [
        'Dataset freeze: fix the 20-image NVL benchmark and keep the split constant across all model families.',
        'Annotation: apply consistent polygon or box labels so each model sees the same defect truth.',
        'Training: keep training budget, preprocess, and device conditions matched for fair comparison.',
        'Evaluation: compare metrics on the same test split and review false positives, miss rate, and boundary quality.',
        'Decision: choose the deployment model based on precision, speed, explainability, and operational fit.'
    ]
)

# Generic model slide function

def add_model_slide(title, subtitle, definition, bullets, image_path):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_title(slide, title, subtitle)
    add_footer(slide, 'Technical definition and model assessment based on the NVL benchmark')

    add_left_text(slide, 'Definition', [
        definition,
        'Operational meaning: why this task exists and when it matters.'
    ], left=0.55, top=1.4, width=6.2, height=1.7)

    add_left_text(slide, 'Objective / parameters / results / improvements', bullets, left=0.55, top=3.1, width=6.2, height=3.2)

    if image_path.exists():
        add_image_with_ratio(slide, image_path, 7.1, 1.8, 5.5, 4.4)


# Detection slide
add_model_slide(
    'Detection Model',
    'Bounding-box localization for rapid defect screening',
    'Detection defines a defect as a localized object: a bounding box identifies the region of interest without tracing the exact boundary.',
    [
        'Objective: identify whether a defect is present and roughly where it is located.',
        'Parameters: box-level localization, lighter annotation burden, faster training and inference.',
        'Results: strong for first-pass review and obvious defects; weaker on irregular boundaries and exact sizing.',
        'Improvement: add low-contrast and edge-case images; tune confidence thresholds; use as a front-end filter to segmentation.'
    ],
    root / 'Debug' / 'Evaluation' / 'Detection only' / 'Results.png'
)

# Anomaly slide
add_model_slide(
    'Anomaly Model',
    'Normal-vs-abnormal screening for deviations',
    'Anomaly detection learns the normal pattern and flags anything that deviates from it. It is useful when the defect taxonomy is incomplete or when unknown patterns may appear.',
    [
        'Objective: catch abnormal scan behavior before the defect is explicitly labeled.',
        'Parameters: trained against good-unit baselines; sensitive to brightness, texture, and process drift.',
        'Results: useful for screening and prioritization; higher false alarm risk than explicit defect models.',
        'Improvement: increase good-unit diversity; calibrate thresholds; combine with a downstream detection or segmentation pass.'
    ],
    root / 'Debug' / 'Evaluation' / 'Anomaly only' / 'Results_explain.png'
)

# Segmentation slide
add_model_slide(
    'Instance Segmentation Model',
    'Pixel-level mask generation for defect geometry',
    'Instance segmentation assigns a mask to each individual defect. This captures the exact shape, size, and boundary, which is critical when defect geometry drives severity and root-cause interpretation.',
    [
        'Objective: localize every defect instance at pixel level and preserve defect morphology.',
        'Parameters: mask-based training, higher annotation effort, greater computational cost, better localization precision.',
        'Results: best technical precision; NVL baseline mAP 22.82%, mAP@0.5 46.53%, mAP@0.75 14.85%, best validation checkpoint mAP 28.59%, mAP@0.5 79.21%.',
        'Improvement: improve annotation consistency on subtle boundaries; add challenging multi-instance and low-contrast examples; refine threshold tuning.'
    ],
    root / 'Debug' / 'Evaluation' / 'Instance Segmentation' / 'Results.png'
)

# Final comparison slide
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_title(slide, 'Model Comparison Summary', 'Pros, cons, accuracy, and technical limitations')
add_footer(slide, 'Technical benchmark: same 20-image NVL set; same frozen split logic; task-specific training settings')

# three-column technical comparison
add_left_text(slide, 'Detection', [
    'Pros: fastest, simplest, easiest to explain and deploy.',
    'Best for operational triage and rapid screening.',
    'Lower annotation effort and faster iteration cycles.',
    'Cons: coarse localization and weak defect-shape precision.',
    'Accuracy/limitations: useful for rough defect presence detection, not precise sizing or mask fidelity.',
    'Run view: good front-end screening model, but not the final technical judge.'
], left=0.55, top=1.35, width=3.8, height=4.9, color=WHITE, border=BLUE)

add_left_text(slide, 'Anomaly', [
    'Pros: strong for outlier detection and unknown defect discovery.',
    'Useful when defect taxonomy is incomplete or changing.',
    'Good as alerting layer and review-prioritization tool.',
    'Cons: higher false alarm rate and weaker object-level localization.',
    'Accuracy/limitations: excellent for abnormality screening, weaker for class definition and boundary accuracy.',
    'Run view: best for flags and prioritization, not for final defect certification.'
], left=4.65, top=1.35, width=3.8, height=4.9, color=WHITE, border=BLUE)

add_left_text(slide, 'Instance Segmentation', [
    'Pros: highest technical precision and best defect geometry understanding.',
    'Captures exact shape, area, and boundary quality.',
    'Strongest for engineering review and defect-root-cause analysis.',
    'Cons: highest annotation burden and computational complexity.',
    'Accuracy/limitations: strongest technical model, but still limited by small benchmark size and annotation quality.',
    'Run view: NVL baseline mAP 22.82%, mAP@0.5 46.53%, mAP@0.75 14.85%; best validation checkpoint mAP 28.59%, mAP@0.5 79.21%.'
], left=8.75, top=1.35, width=3.8, height=4.9, color=WHITE, border=BLUE)

# final recommendation summary under the columns
summary = slide.shapes.add_shape(1, Inches(0.8), Inches(6.35), Inches(11.7), Inches(0.7))
summary.fill.solid(); summary.fill.fore_color.rgb = NAVY; summary.line.color.rgb = NAVY
stf = summary.text_frame
stf.margin_left = Inches(0.12); stf.margin_right = Inches(0.12)
p = stf.paragraphs[0]
p.text = 'Recommendation: use detection for fast screening, anomaly for alerting, and instance segmentation for the final engineering-quality assessment.'
p.alignment = PP_ALIGN.CENTER
p.runs[0].font.name = 'Aptos'; p.runs[0].font.size = Pt(12); p.runs[0].font.bold = True; p.runs[0].font.color.rgb = WHITE

prs.save(output_path)
print(f'Created presentation: {output_path}')
