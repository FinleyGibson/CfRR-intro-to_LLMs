"""
Single Layer Transformer: Detailed view of one transformer layer
================================================================
Shows what happens inside a single transformer layer with attention and feed-forward.

Generates: diagrams/base_model/single_layer_transformer.png
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
C_OUTPUTCOLOR = "#B08CB4"  # purple

# ── layout ─────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 12, 11.5
BOX_W = 4.5
BOX_H = 0.9
LAYER_BOX_H = 1.1

# y-positions (top to bottom)
Y_TITLE = 10.8
Y_INPUT = 9.3
Y_TOKEN = 8.0
Y_EMBED = 6.6
Y_LAYER_TITLE = 5.6
Y_ATTN = 4.3
Y_FFN = 2.6
Y_OUTPUT = 1.0
Y_NOTE = -0.2

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
ax.set_ylim(-0.8, 11.5)
ax.set_facecolor(C_BG)
fig.patch.set_facecolor(C_BG)
ax.axis("off")

# ── title ──────────────────────────────────────────────────────────────────────
lbl(ax, CX, Y_TITLE, "Single Transformer Layer", size=16, weight="bold", color="#111111")

# ── input text ─────────────────────────────────────────────────────────────────
rbox(ax, CX, Y_INPUT, BOX_W, BOX_H, fc=C_TOKENCOLOR + "33", lw=1.5)
lbl(ax, CX, Y_INPUT + 0.18, "Input Text", size=10, weight="normal", color="#555555")
lbl(ax, CX, Y_INPUT - 0.18, '"The cat sat"', size=11, weight="normal", color="#222222")

# ── tokenization ───────────────────────────────────────────────────────────────
arrow(ax, CX, Y_INPUT - BOX_H / 2 - 0.1, CX, Y_TOKEN + BOX_H / 2 + 0.1)

rbox(ax, CX, Y_TOKEN, BOX_W, BOX_H, fc=C_TOKENCOLOR)
lbl(ax, CX, Y_TOKEN + 0.25, "Tokenization", size=11, weight="bold", color="white")
lbl(ax, CX, Y_TOKEN - 0.05, "Text → Token IDs", size=9, color="white")
lbl(ax, CX, Y_TOKEN - 0.28, "[464, 3797, 3332]", size=8, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_TOKEN + 0.1,
    ["Split text into", "machine-readable", "pieces"],
    size=8.5,
)

# ── embeddings ─────────────────────────────────────────────────────────────────
arrow(ax, CX, Y_TOKEN - BOX_H / 2 - 0.1, CX, Y_EMBED + BOX_H / 2 + 0.1)

rbox(ax, CX, Y_EMBED, BOX_W, BOX_H, fc=C_EMBEDCOLOR)
lbl(ax, CX, Y_EMBED + 0.25, "Embeddings", size=11, weight="bold", color="white")
lbl(ax, CX, Y_EMBED - 0.05, "Token IDs → Vectors", size=9, color="white")
lbl(ax, CX, Y_EMBED - 0.28, "Each token = 768 numbers", size=8, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_EMBED + 0.1,
    ["Convert to vectors", "that capture meaning"],
    size=8.5,
)

# ── transformer layer box (background) ─────────────────────────────────────────
layer_top = Y_LAYER_TITLE + 0.3
layer_bottom = Y_FFN - LAYER_BOX_H / 2 - 0.15
layer_height = layer_top - layer_bottom

rbox(
    ax,
    CX,
    (layer_top + layer_bottom) / 2,
    BOX_W + 0.6,
    layer_height,
    fc="#F5F5F5",
    ec="#CCCCCC",
    lw=1.5,
    z=0,
)

lbl(ax, CX, Y_LAYER_TITLE, "Transformer Layer", size=10, weight="bold", color="#666666")

# ── attention mechanism ────────────────────────────────────────────────────────
arrow(ax, CX, Y_EMBED - BOX_H / 2 - 0.05, CX, Y_ATTN + LAYER_BOX_H / 2 + 0.05)

rbox(ax, CX, Y_ATTN, BOX_W, LAYER_BOX_H, fc=C_ATTNCOLOR)
lbl(ax, CX, Y_ATTN + 0.32, "Attention", size=11, weight="bold", color="white")
lbl(ax, CX, Y_ATTN + 0.05, "Words look at each other", size=9, color="white")
lbl(ax, CX, Y_ATTN - 0.22, '"sat" attends to "cat"', size=8.5, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_ATTN + 0.2,
    ["Each word considers", "all other words", "Finds relevant context"],
    size=8.5,
)

# ── feed-forward network ───────────────────────────────────────────────────────
arrow(ax, CX, Y_ATTN - LAYER_BOX_H / 2 - 0.05, CX, Y_FFN + LAYER_BOX_H / 2 + 0.05)

rbox(ax, CX, Y_FFN, BOX_W, LAYER_BOX_H, fc=C_NNCOLOR)
lbl(ax, CX, Y_FFN + 0.32, "Feed-Forward Network", size=11, weight="bold", color="white")
lbl(ax, CX, Y_FFN + 0.05, "Process each word independently", size=9, color="white")
lbl(ax, CX, Y_FFN - 0.22, "Transform & refine", size=8.5, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_FFN + 0.2,
    ["Deep neural network", "Applied to each word", "Uses attention output"],
    size=8.5,
)

# ── output ─────────────────────────────────────────────────────────────────────
arrow(ax, CX, Y_FFN - LAYER_BOX_H / 2 - 0.05, CX, Y_OUTPUT + BOX_H / 2 + 0.05)

rbox(ax, CX, Y_OUTPUT, BOX_W, BOX_H, fc=C_OUTPUTCOLOR)
lbl(ax, CX, Y_OUTPUT + 0.20, "Output Embeddings", size=11, weight="bold", color="white")
lbl(ax, CX, Y_OUTPUT - 0.20, "Updated 3 vectors", size=9, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_OUTPUT,
    ["Context-aware", "representations"],
    size=8.5,
)

# ── note box ───────────────────────────────────────────────────────────────────
rbox(ax, CX, Y_NOTE, BOX_W + 4.0, 0.85, fc="#E8F4F8", ec="#5B9BD5", lw=1.5, z=1)
lbl(
    ax,
    CX,
    Y_NOTE + 0.20,
    "One layer adds context from nearby words and processes patterns.",
    size=9,
    weight="bold",
    color="#222222",
)
lbl(
    ax,
    CX,
    Y_NOTE - 0.15,
    "Real transformers stack many layers to build deeper understanding.",
    size=8.5,
    weight="normal",
    color="#444444",
)

# ── save ───────────────────────────────────────────────────────────────────────
OUT = "diagrams/base_model/single_layer_transformer.png"
plt.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=C_BG)
print(f"Saved: {OUT}")
plt.close()
