from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "GeTi_CSAM_Project_Flow_Infographic.png"

BG = "#F6F3EC"
INK = "#17232C"
MUTED = "#5C6870"
TEAL = "#087E8B"
GREEN = "#2A9D61"
BLUE = "#276FBF"
AMBER = "#E09F3E"
RED = "#C44536"
LIGHT_RED = "#F2C4BC"
LIGHT_TEAL = "#B9E2DF"
LIGHT_BLUE = "#C8DCF4"
LIGHT_GREEN = "#BFE3C9"
LIGHT_AMBER = "#F4D8A7"


def add_flow(ax, x1, y1, x2, y2, width, color, alpha=0.72, zorder=1):
    curve = (x2 - x1) * 0.42
    points = [
        (x1, y1 + width / 2),
        (x1 + curve, y1 + width / 2),
        (x2 - curve, y2 + width / 2),
        (x2, y2 + width / 2),
        (x2, y2 - width / 2),
        (x2 - curve, y2 - width / 2),
        (x1 + curve, y1 - width / 2),
        (x1, y1 - width / 2),
    ]
    ax.add_patch(Polygon(points, closed=True, facecolor=color, edgecolor="none", alpha=alpha, zorder=zorder))


def add_node(ax, x, y, title, detail, color, width=1.22, height=0.62, text_color=INK):
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.025,rounding_size=0.06",
        linewidth=1.5,
        edgecolor=color,
        facecolor="white",
        zorder=4,
    )
    ax.add_patch(box)
    ax.text(x, y + 0.08, title, ha="center", va="center", fontsize=9.2, fontweight="bold", color=text_color, zorder=5)
    ax.text(x, y - 0.13, detail, ha="center", va="center", fontsize=7.1, color=MUTED, zorder=5)


def add_callout(ax, x, y, title, body, color, width=2.25, height=0.74):
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.025,rounding_size=0.05",
        linewidth=1.2,
        edgecolor=color,
        facecolor="white",
        zorder=6,
    )
    ax.add_patch(box)
    ax.text(x - width / 2 + 0.12, y + 0.17, title, ha="left", va="center", fontsize=8.6, fontweight="bold", color=color, zorder=7)
    ax.text(x - width / 2 + 0.12, y - 0.08, body, ha="left", va="center", fontsize=7.2, color=INK, zorder=7)


def main():
    fig, ax = plt.subplots(figsize=(18, 10.2), dpi=180)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12.7)
    ax.set_ylim(0, 8.4)
    ax.axis("off")

    ax.text(0.25, 8.02, "GeTi CSAM project flow", fontsize=25, fontweight="bold", color=INK)
    ax.text(0.27, 7.68, "How the NovaLake defect-detection effort moved from setup, through failed paths and recovery, to successful Web validation", fontsize=10.5, color=MUTED)

    dates = ["Jul 14", "Jul 24", "Aug 04", "Aug 11", "Aug 12", "Aug 14-15", "Aug 18", "Aug 19", "Aug 20", "Aug 25", "Q4"]
    xs = [0.7, 1.75, 2.8, 3.85, 4.9, 5.95, 7.0, 8.05, 9.1, 10.15, 11.55]
    for x, date in zip(xs, dates):
        ax.plot([x, x], [1.0, 7.25], color="#D8D1C3", linewidth=0.8, zorder=0)
        ax.text(x, 0.72, date, ha="center", va="center", fontsize=8.5, fontweight="bold", color=MUTED)
    ax.text(6.15, 0.42, "TIME AXIS", ha="center", fontsize=8, fontweight="bold", color=MUTED, alpha=0.8)

    # Main successful flow uses a dedicated lane below the event cards.
    flow_y = 5.0
    add_flow(ax, xs[0], flow_y, xs[2], flow_y, 0.32, TEAL)
    add_flow(ax, xs[2], flow_y, xs[3], flow_y, 0.32, TEAL)
    add_flow(ax, xs[3], flow_y, xs[4], flow_y, 0.32, GREEN)
    add_flow(ax, xs[4], flow_y, xs[5], flow_y, 0.32, GREEN)
    add_flow(ax, xs[5], flow_y, xs[6], flow_y, 0.32, BLUE)
    add_flow(ax, xs[6], flow_y, xs[7], flow_y, 0.32, BLUE)
    add_flow(ax, xs[7], flow_y, xs[8], flow_y, 0.32, BLUE)
    add_flow(ax, xs[8], flow_y, xs[9], flow_y, 0.32, GREEN)
    add_flow(ax, xs[9], flow_y, xs[10], flow_y, 0.32, GREEN)
    for x in xs:
        ax.plot([x, x], [5.68, flow_y + 0.17], color="#9BA9AD", linewidth=1.0, zorder=2)

    # Failed legacy branch and recovery diversion.
    add_flow(ax, xs[3], 4.82, xs[3] + 0.45, 3.7, 0.42, RED, alpha=0.78)
    add_flow(ax, xs[3] + 0.45, 3.7, xs[4], 4.15, 0.42, RED, alpha=0.78)
    add_flow(ax, xs[4], 4.15, xs[5], 4.82, 0.42, AMBER, alpha=0.76)

    # Web comparison branches converge into a recommendation.
    add_flow(ax, xs[6], 4.72, xs[8], 3.35, 0.22, BLUE, alpha=0.55)
    add_flow(ax, xs[6], 4.98, xs[8], 3.35, 0.22, AMBER, alpha=0.55)
    add_flow(ax, xs[6], 5.24, xs[8], 3.35, 0.22, TEAL, alpha=0.55)
    add_flow(ax, xs[8], 3.35, xs[9], 3.35, 0.38, GREEN)
    add_flow(ax, xs[9], 3.35, xs[10], 3.35, 0.38, GREEN)

    # Nodes.
    add_node(ax, xs[0], 6.0, "Project kickoff", "Geti selected", TEAL)
    add_node(ax, xs[2], 6.0, "Data pipeline", "TIFF -> PNG", TEAL)
    add_node(ax, xs[3], 6.0, "Training path", "Geti + getitune", BLUE)
    add_node(ax, xs[4], 6.0, "Smoke test", "5 images; ~1% mAP", GREEN)
    add_node(ax, xs[5], 6.0, "NVL baseline", "20 images; exports", BLUE)
    add_node(ax, xs[6], 6.3, "Web Geti", "NVL-S-28C", BLUE)
    add_node(ax, xs[7], 6.3, "Live prediction", "visible masks", BLUE)
    add_node(ax, xs[8], 6.3, "DOE comparison", "3 task families", TEAL)
    add_node(ax, xs[9], 6.3, "Result", "test score 78", GREEN)
    add_node(ax, xs[10], 6.3, "Q4 execution", "fine-tune + deploy", GREEN)

    add_node(ax, 4.3, 3.7, "13 failed runs", "empty boxes crash", RED, width=1.45, height=0.7)
    add_node(ax, 5.0, 4.15, "Diversion", "defect-only data", AMBER, width=1.35, height=0.62)
    add_node(ax, 7.95, 3.35, "Model roles", "screen / alert / review", TEAL, width=1.55, height=0.7)

    # Evidence callouts.
    add_callout(ax, 1.75, 2.05, "What did not work", "Clean / 'No object' images\ncaused validation crashes", RED)
    add_callout(ax, 4.15, 1.48, "What changed", "Switched to defect-only\ndata and a clean run", AMBER)
    add_callout(ax, 7.25, 1.62, "Successful Web result", "OpenVINO FP16 test: 78\n25 images; masks visible", GREEN)
    add_callout(ax, 10.3, 1.62, "Decision", "Instance segmentation for\nengineering review", TEAL)

    # Legend.
    legend_rows = [
        (7.35, [(TEAL, "progress / platform"), (GREEN, "successful result"), (RED, "failed path")]),
        (7.08, [(AMBER, "workaround / diversion"), (BLUE, "model or Web activity")]),
    ]
    for legend_y, legend in legend_rows:
        x = 7.1
        for color, label in legend:
            ax.add_patch(plt.Rectangle((x, legend_y - 0.08), 0.16, 0.16, facecolor=color, edgecolor="none", zorder=8))
            ax.text(x + 0.22, legend_y, label, va="center", fontsize=7.5, color=MUTED)
            x += 1.45

    ax.text(0.28, 0.12, "Evidence basis: project documentation, preserved Web Geti screenshots, and the updated model-comparison deck. Scores are directional because the benchmark is small.", fontsize=7.2, color=MUTED)
    fig.savefig(OUTPUT, facecolor=BG, bbox_inches="tight", pad_inches=0.18)
    print(f"Created infographic: {OUTPUT}")


if __name__ == "__main__":
    main()