"""
Transformer Components: How the pieces fit together
====================================================
Shows the flow from text → tokenization → embeddings → transformer layers → output.

Generates: diagrams/base_model/transformer_components.png
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans"})

# ── colours ────────────────────────────────────────────────────────────────────
C_BG = "#FAFAFA"
C_TOKENCOLOR = "#B08CB4"  # purple
C_EMBEDCOLOR = "#6496C8"  # blue
C_ATTNCOLOR = "#96B464"  # green
C_NNCOLOR = "#DC7864"  # red/orange

# ── layout ─────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 12, 11
BOX_W = 4.5
BOX_H = 1.0
TRANSFORMER_H = 2.8

# y-positions (top to bottom)
Y_TITLE = 10.3
Y_INPUT = 8.8
Y_TOKEN = 7.3
Y_EMBED = 5.5
Y_TRANSFORMER = 3.2
Y_OUTPUT = 1.0
Y_INSIGHT = -0.5

# x-positions
CX = FIG_W / 2  # center column
ANNOT_X = CX + 3.2  # annotation column


def rbox(ax, cx, cy, w, h, fc, ec="white", lw=2.0, z=2):
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


def multiline_lbl(ax, x, y, lines, size=9, color="#555555", ha="left"):
    """Draw multi-line annotation text."""
    for i, line in enumerate(lines):
        ax.text(x, y - i * 0.22, line, fontsize=size, color=color, ha=ha, va="center", zorder=5)


# ── figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(-1.2, 11)
ax.set_facecolor(C_BG)
fig.patch.set_facecolor(C_BG)
ax.axis("off")

# ── title ──────────────────────────────────────────────────────────────────────
lbl(ax, CX, Y_TITLE, "How a Transformer Works", size=16, weight="bold", color="#111111")

# ── input text ─────────────────────────────────────────────────────────────────
rbox(ax, CX, Y_INPUT, BOX_W, BOX_H, fc=C_TOKENCOLOR + "33", lw=1.5)
lbl(ax, CX, Y_INPUT + 0.18, "Input Text", size=10, weight="normal", color="#555555")
lbl(ax, CX, Y_INPUT - 0.18, '"The cat sat"', size=11, weight="normal", color="#222222")

# ── 1. tokenization ────────────────────────────────────────────────────────────
arrow(ax, CX, Y_INPUT - BOX_H / 2 - 0.1, CX, Y_TOKEN + BOX_H / 2 + 0.1)

rbox(ax, CX, Y_TOKEN, BOX_W, BOX_H, fc=C_TOKENCOLOR)
lbl(ax, CX, Y_TOKEN + 0.25, "1. Tokenization", size=12, weight="bold", color="white")
lbl(ax, CX, Y_TOKEN - 0.05, "Text → Token IDs", size=9, color="white")
lbl(ax, CX, Y_TOKEN - 0.28, "[464, 3797, 3332]", size=8, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_TOKEN + 0.15,
    ["Split text into", "machine-readable", "pieces"],
    size=8.5,
)

# ── 2. embeddings ──────────────────────────────────────────────────────────────
arrow(ax, CX, Y_TOKEN - BOX_H / 2 - 0.1, CX, Y_EMBED + BOX_H / 2 + 0.1)

rbox(ax, CX, Y_EMBED, BOX_W, BOX_H, fc=C_EMBEDCOLOR)
lbl(ax, CX, Y_EMBED + 0.25, "2. Embeddings", size=12, weight="bold", color="white")
lbl(ax, CX, Y_EMBED - 0.05, "Token IDs → Vectors", size=9, color="white")
lbl(ax, CX, Y_EMBED - 0.28, "Each token = 768 numbers", size=8, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_EMBED + 0.15,
    ["Convert to vectors", "that capture meaning", '("cat" ≈ "dog")'],
    size=8.5,
)

# ── 3. transformer layers ──────────────────────────────────────────────────────
arrow(ax, CX, Y_EMBED - BOX_H / 2 - 0.1, CX, Y_TRANSFORMER + TRANSFORMER_H / 2 + 0.1)

rbox(ax, CX, Y_TRANSFORMER, BOX_W, TRANSFORMER_H, fc=C_ATTNCOLOR)
lbl(ax, CX, Y_TRANSFORMER + 1.0, "3. Transformer Layers", size=12, weight="bold", color="white")

# attention part
lbl(ax, CX, Y_TRANSFORMER + 0.48, "Attention:", size=10, weight="bold", color="white")
lbl(ax, CX, Y_TRANSFORMER + 0.22, "Focus on relevant words", size=8.5, color="white")
lbl(ax, CX, Y_TRANSFORMER + 0.00, '"sat" looks at "cat"', size=8, color="white")

# neural network part
lbl(ax, CX, Y_TRANSFORMER - 0.36, "Neural Network:", size=10, weight="bold", color="white")
lbl(ax, CX, Y_TRANSFORMER - 0.58, "Transform patterns", size=8.5, color="white")
lbl(ax, CX, Y_TRANSFORMER - 0.80, "Process the information", size=8, color="white")

lbl(ax, CX, Y_TRANSFORMER - 1.15, "(Repeat 24 times)", size=7.5, color="white", weight="normal")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_TRANSFORMER + 0.4,
    ["Each layer:", "1. Attention finds", "   context", "2. Neural nets", "   process it"],
    size=8.5,
)

# ── 4. output ──────────────────────────────────────────────────────────────────
arrow(ax, CX, Y_TRANSFORMER - TRANSFORMER_H / 2 - 0.1, CX, Y_OUTPUT + BOX_H / 2 + 0.1)

rbox(ax, CX, Y_OUTPUT, BOX_W, BOX_H, fc=C_NNCOLOR)
lbl(ax, CX, Y_OUTPUT + 0.25, "4. Predict Next Token", size=12, weight="bold", color="white")
lbl(ax, CX, Y_OUTPUT - 0.05, "Vectors → Probabilities", size=9, color="white")
lbl(ax, CX, Y_OUTPUT - 0.28, '"on" (65%), "down" (20%), ...', size=8, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_OUTPUT + 0.15,
    ["Convert back to", "token predictions"],
    size=8.5,
)

# ── key insight box ────────────────────────────────────────────────────────────
rbox(ax, CX, Y_INSIGHT, BOX_W + 4.5, 0.95, fc="#FFF9E6", ec="#DDB74C", lw=1.8, z=1)
lbl(
    ax,
    CX,
    Y_INSIGHT + 0.22,
    "Key Idea: These 4 components work together to predict the next word.",
    size=9,
    weight="bold",
    color="#222222",
)
lbl(
    ax,
    CX,
    Y_INSIGHT - 0.15,
    "During training, all the weights learn to make this prediction more accurate.",
    size=8.5,
    weight="normal",
    color="#444444",
)

# ── flow annotation (left side) ────────────────────────────────────────────────
flow_x = 0.7
arrow(
    ax,
    flow_x,
    Y_INPUT - 0.3,
    flow_x,
    Y_OUTPUT + 0.3,
    color="#5B9BD5",
    lw=2.5,
    z=0,
)

lbl(
    ax,
    flow_x - 0.25,
    (Y_INPUT + Y_OUTPUT) / 2,
    "Information\nflows\nthrough\neach stage",
    size=8,
    color="#5B9BD5",
    ha="right",
)

# ── save ───────────────────────────────────────────────────────────────────────
OUT = "diagrams/base_model/transformer_components.png"
plt.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=C_BG)
print(f"Saved: {OUT}")
plt.close()
