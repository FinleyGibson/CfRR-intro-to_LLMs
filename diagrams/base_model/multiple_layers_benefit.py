"""
Multiple Layers: Why stacking transformer layers is powerful
=============================================================
Shows how multiple layers build increasingly abstract understanding.

Generates: diagrams/base_model/multiple_layers_benefit.png
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans"})

# ── colours ────────────────────────────────────────────────────────────────────
C_BG = "#FAFAFA"
C_EMBEDCOLOR = "#6496C8"  # blue
C_LAYER1 = "#96B464"  # green
C_LAYER2 = "#DC9C64"  # orange
C_LAYER3 = "#DC7864"  # red
C_OUTPUTCOLOR = "#B08CB4"  # purple

# ── layout ─────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 13, 11

# Left side (1 layer)
LEFT_X = 3.0
# Right side (3 layers)
RIGHT_X = 10.0

BOX_W = 3.8
BOX_H = 0.8
LAYER_H = 0.75

# y-positions
Y_TITLE = 10.3
Y_SUBTITLE_LEFT = 9.5
Y_SUBTITLE_RIGHT = 9.5
Y_INPUT = 8.3
Y_LAYER1 = 7.0
Y_LAYER2 = 5.7
Y_LAYER3 = 4.4
Y_OUTPUT = 3.0
Y_COMPARISON = 1.8

# Example text
EXAMPLE = "The cat sat on the mat"


def rbox(ax, cx, cy, w, h, fc, ec="white", lw=2.0, z=2, alpha=1.0):
    """Draw a rounded box."""
    ax.add_patch(
        mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2),
            w,
            h,
            boxstyle="round,pad=0.05",
            fc=fc,
            ec=ec,
            lw=lw,
            zorder=z,
            alpha=alpha,
        )
    )


def arrow(ax, x1, y1, x2, y2, color="#999999", lw=2.0, z=1):
    """Draw an arrow."""
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw),
        zorder=z,
    )


def lbl(ax, x, y, s, size=11, color="#222222", weight="normal", ha="center", va="center"):
    """Draw text label."""
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=5)


def multiline_lbl(ax, x, y, lines, size=9, color="#555555", ha="center"):
    """Draw multi-line annotation text."""
    for i, line in enumerate(lines):
        ax.text(x, y - i * 0.23, line, fontsize=size, color=color, ha=ha, va="center", zorder=5)


# ── figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, 11.2)
ax.set_facecolor(C_BG)
fig.patch.set_facecolor(C_BG)
ax.axis("off")

# ── title ──────────────────────────────────────────────────────────────────────
lbl(
    ax,
    FIG_W / 2,
    Y_TITLE,
    "Why Stack Multiple Transformer Layers?",
    size=16,
    weight="bold",
    color="#111111",
)

# ── left side: 1 layer ─────────────────────────────────────────────────────────
lbl(ax, LEFT_X, Y_SUBTITLE_LEFT, "1 Layer", size=13, weight="bold", color="#444444")

# input
rbox(ax, LEFT_X, Y_INPUT, BOX_W, BOX_H, fc=C_EMBEDCOLOR, lw=1.5)
lbl(ax, LEFT_X, Y_INPUT, "Input Embeddings", size=9, color="white", weight="bold")

arrow(ax, LEFT_X, Y_INPUT - BOX_H / 2 - 0.05, LEFT_X, Y_LAYER1 + LAYER_H / 2 + 0.05)

# layer 1
rbox(ax, LEFT_X, Y_LAYER1, BOX_W, LAYER_H, fc=C_LAYER1)
lbl(ax, LEFT_X, Y_LAYER1, "Layer 1", size=10, color="white", weight="bold")

multiline_lbl(
    ax,
    LEFT_X,
    Y_LAYER1 - 0.6,
    ["Surface patterns:", '"cat" near "sat"'],
    size=8,
    color="#555555",
)

arrow(ax, LEFT_X, Y_LAYER1 - LAYER_H / 2 - 0.35, LEFT_X, Y_OUTPUT + BOX_H / 2 + 0.05, lw=1.5)

# output
rbox(ax, LEFT_X, Y_OUTPUT, BOX_W, BOX_H, fc=C_OUTPUTCOLOR, lw=1.5)
lbl(ax, LEFT_X, Y_OUTPUT, "Output", size=9, color="white", weight="bold")

multiline_lbl(
    ax,
    LEFT_X,
    Y_OUTPUT - 0.6,
    ["✓ Basic relationships", "✗ Limited abstraction", "✗ Shallow understanding"],
    size=8,
    color="#555555",
)

# ── right side: 3 layers ───────────────────────────────────────────────────────
lbl(ax, RIGHT_X, Y_SUBTITLE_RIGHT, "3 Layers", size=13, weight="bold", color="#444444")

# input
rbox(ax, RIGHT_X, Y_INPUT, BOX_W, BOX_H, fc=C_EMBEDCOLOR, lw=1.5)
lbl(ax, RIGHT_X, Y_INPUT, "Input Embeddings", size=9, color="white", weight="bold")

arrow(ax, RIGHT_X, Y_INPUT - BOX_H / 2 - 0.05, RIGHT_X, Y_LAYER1 + LAYER_H / 2 + 0.05)

# layer 1
rbox(ax, RIGHT_X, Y_LAYER1, BOX_W, LAYER_H, fc=C_LAYER1)
lbl(ax, RIGHT_X, Y_LAYER1, "Layer 1", size=10, color="white", weight="bold")

multiline_lbl(
    ax,
    RIGHT_X,
    Y_LAYER1 - 0.6,
    ["Surface patterns:", '"cat" near "sat"'],
    size=8,
    color="#555555",
)

arrow(ax, RIGHT_X, Y_LAYER1 - LAYER_H / 2 - 0.35, RIGHT_X, Y_LAYER2 + LAYER_H / 2 + 0.05)

# layer 2
rbox(ax, RIGHT_X, Y_LAYER2, BOX_W, LAYER_H, fc=C_LAYER2)
lbl(ax, RIGHT_X, Y_LAYER2, "Layer 2", size=10, color="white", weight="bold")

multiline_lbl(
    ax,
    RIGHT_X,
    Y_LAYER2 - 0.6,
    ["Grammar & roles:", '"cat" is subject of "sat"'],
    size=8,
    color="#555555",
)

arrow(ax, RIGHT_X, Y_LAYER2 - LAYER_H / 2 - 0.35, RIGHT_X, Y_LAYER3 + LAYER_H / 2 + 0.05)

# layer 3
rbox(ax, RIGHT_X, Y_LAYER3, BOX_W, LAYER_H, fc=C_LAYER3)
lbl(ax, RIGHT_X, Y_LAYER3, "Layer 3", size=10, color="white", weight="bold")

multiline_lbl(
    ax,
    RIGHT_X,
    Y_LAYER3 - 0.6,
    ["Abstract meaning:", "Animal performing action on object"],
    size=8,
    color="#555555",
)

arrow(ax, RIGHT_X, Y_LAYER3 - LAYER_H / 2 - 0.35, RIGHT_X, Y_OUTPUT + BOX_H / 2 + 0.05, lw=1.5)

# output
rbox(ax, RIGHT_X, Y_OUTPUT, BOX_W, BOX_H, fc=C_OUTPUTCOLOR, lw=1.5)
lbl(ax, RIGHT_X, Y_OUTPUT, "Output", size=9, color="white", weight="bold")

multiline_lbl(
    ax,
    RIGHT_X,
    Y_OUTPUT - 0.6,
    ["✓ Rich representations", "✓ Deep understanding", "✓ Complex reasoning"],
    size=8,
    color="#555555",
)

# ── comparison box ─────────────────────────────────────────────────────────────
rbox(ax, FIG_W / 2, Y_COMPARISON, BOX_W + 6.0, 1.3, fc="#FFF9E6", ec="#DDB74C", lw=1.8, z=1)

lbl(
    ax,
    FIG_W / 2,
    Y_COMPARISON + 0.42,
    "Key Insight: Each layer builds on the previous one",
    size=10,
    weight="bold",
    color="#222222",
)

multiline_lbl(
    ax,
    FIG_W / 2,
    Y_COMPARISON - 0.05,
    [
        "Layer 1: Low-level patterns (which words are near each other)",
        "Layer 2: Mid-level structure (grammar, word roles, phrases)",
        "Layer 3+: High-level meaning (concepts, reasoning, context)",
    ],
    size=8,
    color="#444444",
)

# ── arrows showing depth ───────────────────────────────────────────────────────
# Bracket on right side showing increasing abstraction
bracket_x = RIGHT_X + BOX_W / 2 + 0.5
ax.plot([bracket_x, bracket_x + 0.3], [Y_LAYER1, Y_LAYER1], color="#666666", lw=1.5)
ax.plot([bracket_x + 0.3, bracket_x + 0.3], [Y_LAYER1, Y_LAYER3], color="#666666", lw=1.5)
ax.plot([bracket_x, bracket_x + 0.3], [Y_LAYER3, Y_LAYER3], color="#666666", lw=1.5)

lbl(
    ax,
    bracket_x + 0.85,
    (Y_LAYER1 + Y_LAYER3) / 2,
    "Increasing\nabstraction",
    size=8,
    color="#666666",
    ha="left",
)

# ── save ───────────────────────────────────────────────────────────────────────
OUT = "diagrams/base_model/multiple_layers_benefit.png"
plt.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=C_BG)
print(f"Saved: {OUT}")
plt.close()
