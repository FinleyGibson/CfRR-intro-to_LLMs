"""
LLM Recipe Generation Workflow
================================
Shows the pipeline from user request to final recipe output.

Generates: documents/harnessing/workflow-diagram.png
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans"})

# ── colours ────────────────────────────────────────────────────────────────────
C_BG = "#FAFAFA"
C_REQUEST = "#B08CB4"    # purple
C_PLANNING = "#6496C8"   # blue
C_EXECUTOR = "#96B464"   # green
C_MEMORY = "#DC7864"     # red/orange
C_OUTPUT = "#E8B44C"     # yellow/gold

# ── layout ─────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 10, 12
BOX_W = 5.5
BOX_H = 1.2

# y-positions (top to bottom)
Y_TITLE = 11.2
Y_REQUEST = 9.5
Y_PLANNING = 7.5
Y_EXECUTOR = 5.5
Y_MEMORY = 3.5
Y_OUTPUT = 1.5

# x-position
CX = FIG_W / 2  # center column
ANNOT_X = CX + 3.5  # annotation column


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


def arrow(ax, x1, y1, x2, y2, color="#999999", lw=2.5, z=1):
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
ax.set_ylim(0.5, 12)
ax.set_facecolor(C_BG)
fig.patch.set_facecolor(C_BG)
ax.axis("off")

# ── title ──────────────────────────────────────────────────────────────────────
lbl(ax, CX, Y_TITLE, "LLM Recipe Generation Workflow", size=20, weight="bold", color="#111111")

# ── 1. user request ────────────────────────────────────────────────────────────
rbox(ax, CX, Y_REQUEST, BOX_W, BOX_H, fc=C_REQUEST)
lbl(ax, CX, Y_REQUEST, "User Request (LLM)", size=16, weight="bold", color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_REQUEST + 0.1,
    ["Initial input", "requesting recipe"],
    size=13,
)

# ── 2. planning / decomposition ────────────────────────────────────────────────
arrow(ax, CX, Y_REQUEST - BOX_H / 2 - 0.15, CX, Y_PLANNING + BOX_H / 2 + 0.15)

rbox(ax, CX, Y_PLANNING, BOX_W, BOX_H, fc=C_PLANNING)
lbl(ax, CX, Y_PLANNING + 0.3, "1. Planning / Decomposition", size=16, weight="bold", color="white")
lbl(ax, CX, Y_PLANNING - 0.05, "→ Ingredients", size=14, color="white")
lbl(ax, CX, Y_PLANNING - 0.30, "→ Ordered Steps", size=14, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_PLANNING + 0.1,
    ["Break down request", "into components"],
    size=13,
)

# ── 3. step executor loop ──────────────────────────────────────────────────────
arrow(ax, CX, Y_PLANNING - BOX_H / 2 - 0.15, CX, Y_EXECUTOR + BOX_H / 2 + 0.15)

rbox(ax, CX, Y_EXECUTOR, BOX_W, BOX_H, fc=C_EXECUTOR)
lbl(ax, CX, Y_EXECUTOR + 0.25, "2. Step Executor Loop", size=16, weight="bold", color="white")
lbl(ax, CX, Y_EXECUTOR - 0.15, "(LLM runs each step alone)", size=14, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_EXECUTOR + 0.1,
    ["Process each", "step individually"],
    size=13,
)

# ── 4. context memory update ───────────────────────────────────────────────────
arrow(ax, CX, Y_EXECUTOR - BOX_H / 2 - 0.15, CX, Y_MEMORY + BOX_H / 2 + 0.15)

rbox(ax, CX, Y_MEMORY, BOX_W, BOX_H, fc=C_MEMORY)
lbl(ax, CX, Y_MEMORY + 0.25, "3. Context Memory Update", size=16, weight="bold", color="white")
lbl(ax, CX, Y_MEMORY - 0.15, "(previous steps accumulated)", size=14, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_MEMORY + 0.1,
    ["Accumulate results", "in memory"],
    size=13,
)

# ── 5. final output ────────────────────────────────────────────────────────────
arrow(ax, CX, Y_MEMORY - BOX_H / 2 - 0.15, CX, Y_OUTPUT + BOX_H / 2 + 0.15)

rbox(ax, CX, Y_OUTPUT, BOX_W, BOX_H, fc=C_OUTPUT)
lbl(ax, CX, Y_OUTPUT + 0.25, "Final Structured Recipe", size=16, weight="bold", color="white")
lbl(ax, CX, Y_OUTPUT - 0.15, "+ step-by-step instructions", size=14, color="white")

multiline_lbl(
    ax,
    ANNOT_X,
    Y_OUTPUT + 0.1,
    ["Complete recipe", "with instructions"],
    size=13,
)

# ── flow annotation (left side) ────────────────────────────────────────────────
flow_x = 0.8
arrow(
    ax,
    flow_x,
    Y_REQUEST - 0.4,
    flow_x,
    Y_OUTPUT + 0.4,
    color="#5B9BD5",
    lw=3.0,
    z=0,
)

lbl(
    ax,
    flow_x - 0.35,
    (Y_REQUEST + Y_OUTPUT) / 2,
    "Pipeline\nflow",
    size=13,
    color="#5B9BD5",
    ha="right",
    weight="bold",
)

# ── save ───────────────────────────────────────────────────────────────────────
OUT = "documents/harnessing/workflow-diagram.png"
plt.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=C_BG)
print(f"Saved: {OUT}")
plt.close()
