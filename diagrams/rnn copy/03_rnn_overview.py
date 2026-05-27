"""
Overview diagram: sliding window → one-hot encoding → unrolled RNN → prediction.

The key visual idea:
  • Text strip shows the source text with window + target highlighted
  • Input char boxes sit directly below their characters (tight spacing)
  • Fan arrows spread each char out to its own wide column
  • Each column shows a schematic one-hot vector, then an RNN cell
  • Hidden-state arrows run left→right between RNN cells
  • The final cell feeds into a softmax → predicted character

Generates: examples/rnn/rnn_overview.png
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans"})

# ── data ───────────────────────────────────────────────────────────────────────
FULL_TEXT = "To be, or not to be"
WIN_START = 7
WIN_LEN = 4
VOCAB = [" "] + list("abcdefghijklmnopqrstuvwxyz")  # 27 chars (simplified)

WIN_CHARS = list(FULL_TEXT[WIN_START : WIN_START + WIN_LEN])
TARGET_CHAR = FULL_TEXT[WIN_START + WIN_LEN]

# ── colours ────────────────────────────────────────────────────────────────────
C_BG = "#FAFAFA"
C_NEUTRAL = "#DDDDDD"
C_WIN = "#4C72B0"  # blue  – context window
C_TARGET = "#C44E52"  # red   – target character
C_INPUT = "#55A868"  # green – input char boxes
C_RNN = "#4C72B0"  # blue  – RNN cells
C_H0 = "#CCCCCC"  # grey  – initial hidden state
C_HIDDEN = "#DD8452"  # orange – hidden-state arrows
C_SOFTMAX = "#8172B2"  # purple – softmax
C_OUTPUT = "#C44E52"  # red   – output box
C_HOT = "#C44E52"  # red   – the '1' in one-hot
C_ZERO = "#E8E8E8"  # light grey – the '0's in one-hot

# ── layout ─────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 13.5, 10.5

CHAR_PITCH = 0.52
TEXT_X0 = (FIG_W - 18 * CHAR_PITCH) / 2  # centre the text strip

# Four RNN time-step columns, spread wide
COL_XS = [3.2, 5.2, 7.2, 9.2]
H0_X = 1.7

RNN_W, RNN_H = 1.3, 0.82
IN_W, IN_H = 0.42, 0.52

# Row y-centres (top → bottom)
Y_TITLE = 10.05
Y_TEXT = 9.05
Y_INPUT = 7.75  # input char boxes (tight, aligned to text)
Y_OH = 6.3  # one-hot schematics (wide, at COL_XS)
Y_RNN = 4.85  # RNN cells (wide, at COL_XS)
Y_SM = 3.4  # softmax
Y_OUT = 2.1  # output char

ROW_LBL_X = 0.6


def char_cx(i):
    return TEXT_X0 + i * CHAR_PITCH


# ── helpers ────────────────────────────────────────────────────────────────────
def rbox(ax, cx, cy, w, h, fc, ec="white", lw=1.8, z=2):
    ax.add_patch(
        mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2),
            w,
            h,
            boxstyle="round,pad=0.04",
            fc=fc,
            ec=ec,
            lw=lw,
            zorder=z,
        )
    )


def arrow(ax, x1, y1, x2, y2, color="#BBBBBB", lw=1.4, z=1):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw),
        zorder=z,
    )


def lbl(ax, x, y, s, size=10, color="#222222", weight="normal", ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=5)


def draw_onehot(ax, cx, cy, ch):
    """
    Draw a schematic  [0][ … ][1][ … ][0]  one-hot indicator.
    The centre cell (the '1') is coloured; flanking zeros and ellipses are grey.
    An index label sits below the hot cell.
    """
    idx = VOCAB.index(ch) if ch in VOCAB else -1
    cs = 0.21  # cell width & height
    gap = 0.07  # gap between cells
    items = [
        ("0", C_ZERO, "#AAAAAA"),
        ("…", "#F2F2F2", "#BBBBBB"),
        ("1", C_HOT, "white"),
        ("…", "#F2F2F2", "#BBBBBB"),
        ("0", C_ZERO, "#AAAAAA"),
    ]
    total_w = len(items) * cs + (len(items) - 1) * gap
    x0 = cx - total_w / 2

    for k, (text, fc, tc) in enumerate(items):
        ccx = x0 + k * (cs + gap) + cs / 2
        rbox(ax, ccx, cy, cs, cs * 0.88, fc=fc, lw=0.8)
        lbl(ax, ccx, cy, text, size=9, color=tc, weight="bold" if text == "1" else "normal")

    # index annotation under the hot cell
    if idx >= 0:
        hot_cx = x0 + 2 * (cs + gap) + cs / 2
        lbl(ax, hot_cx, cy - cs * 0.5 - 0.17, f"idx {idx}", size=7.5, color=C_HOT)


# ── figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_facecolor(C_BG)
fig.patch.set_facecolor(C_BG)
ax.axis("off")

# ── title ──────────────────────────────────────────────────────────────────────
lbl(
    ax,
    FIG_W / 2,
    Y_TITLE,
    "Sliding Window RNN  ·  Overview",
    size=15,
    weight="bold",
    color="#111111",
)

# ── row labels (left margin) ───────────────────────────────────────────────────
for y, text in [
    (Y_TEXT, "Source\ntext"),
    (Y_INPUT, "Input\nchars"),
    (Y_OH, "One-hot\nvector"),
    (Y_RNN, "RNN\ncell"),
    (Y_OUT, "Output"),
]:
    lbl(ax, ROW_LBL_X, y, text, size=8.5, color="#BBBBBB")

# ── text strip ─────────────────────────────────────────────────────────────────
for i, ch in enumerate(FULL_TEXT):
    cx = char_cx(i)
    in_win = WIN_START <= i < WIN_START + WIN_LEN
    is_tgt = i == WIN_START + WIN_LEN
    fc = C_WIN if in_win else (C_TARGET if is_tgt else C_NEUTRAL)
    tc = "white" if (in_win or is_tgt) else "#555555"
    rbox(ax, cx, Y_TEXT, 0.42, 0.48, fc=fc)
    lbl(
        ax,
        cx,
        Y_TEXT,
        "·" if ch == " " else ch,
        size=9.5,
        color=tc,
        weight="bold" if (in_win or is_tgt) else "normal",
    )

# window underline + label
bx0 = char_cx(WIN_START) - 0.27
bx1 = char_cx(WIN_START + WIN_LEN - 1) + 0.27
ax.plot([bx0, bx1], [Y_TEXT - 0.34, Y_TEXT - 0.34], color=C_WIN, lw=1.8)
lbl(ax, (bx0 + bx1) / 2, Y_TEXT - 0.55, "context window", size=8, color=C_WIN)

# target underline + label
tx = char_cx(WIN_START + WIN_LEN)
ax.plot([tx - 0.26, tx + 0.26], [Y_TEXT - 0.34, Y_TEXT - 0.34], color=C_TARGET, lw=1.8)
lbl(ax, tx, Y_TEXT - 0.55, "target", size=8, color=C_TARGET)

# ── input char boxes (aligned to text strip) ───────────────────────────────────
input_xs = [char_cx(WIN_START + i) for i in range(WIN_LEN)]

for ch, cx in zip(WIN_CHARS, input_xs):
    arrow(ax, cx, Y_TEXT - 0.68, cx, Y_INPUT + IN_H / 2 + 0.05)
    rbox(ax, cx, Y_INPUT, IN_W, IN_H, fc=C_INPUT)
    lbl(ax, cx, Y_INPUT, "·" if ch == " " else ch, size=11, color="white", weight="bold")

# ── fan arrows: input boxes (tight) → one-hot columns (wide) ──────────────────
# This spreading visually represents: character → one-hot vector
for src_cx, dst_cx in zip(input_xs, COL_XS):
    arrow(ax, src_cx, Y_INPUT - IN_H / 2, dst_cx, Y_OH + 0.27, color="#CCCCCC", lw=1.3)

# ── one-hot schematics (at wide column positions) ─────────────────────────────
for ch, cx in zip(WIN_CHARS, COL_XS):
    draw_onehot(ax, cx, Y_OH, ch)

# ── straight arrows: one-hot → RNN cells ──────────────────────────────────────
for cx in COL_XS:
    arrow(ax, cx, Y_OH - 0.38, cx, Y_RNN + RNN_H / 2 + 0.05)

# ── h0 (initial hidden state) ─────────────────────────────────────────────────
rbox(ax, H0_X, Y_RNN, 0.72, 0.52, fc=C_H0, lw=1.4)
lbl(ax, H0_X, Y_RNN, "h₀", size=11, color="#555555", weight="bold")

# ── RNN cells ─────────────────────────────────────────────────────────────────
for i, cx in enumerate(COL_XS):
    rbox(ax, cx, Y_RNN, RNN_W, RNN_H, fc=C_RNN)
    lbl(ax, cx, Y_RNN, "RNN", size=13, color="white", weight="bold")

    # t= label above each cell
    lbl(ax, cx, Y_RNN + RNN_H / 2 + 0.2, f"t = {i + 1}", size=8, color="#999999")

    # hidden-state label below
    lbl(ax, cx, Y_RNN - RNN_H / 2 - 0.22, f"h{i + 1}", size=8.5, color="#777777")

    # hidden-state arrow from previous cell (or h0)
    prev_x = H0_X if i == 0 else COL_XS[i - 1]
    prev_w = 0.36 if i == 0 else RNN_W / 2
    arrow(ax, prev_x + prev_w, Y_RNN, cx - RNN_W / 2, Y_RNN, color=C_HIDDEN, lw=2.2, z=2)

# ── softmax + output (from last RNN cell only) ────────────────────────────────
last_cx = COL_XS[-1]

arrow(ax, last_cx, Y_RNN - RNN_H / 2, last_cx, Y_SM + 0.29)

rbox(ax, last_cx, Y_SM, 1.4, 0.52, fc=C_SOFTMAX)
lbl(ax, last_cx - 0.8, Y_SM, "ŷ =", size=10, color="#DDDDDD")
lbl(ax, last_cx, Y_SM, "softmax", size=11, color="white", weight="bold")

arrow(ax, last_cx, Y_SM - 0.28, last_cx, Y_OUT + 0.34)

rbox(ax, last_cx, Y_OUT, 0.82, 0.60, fc=C_OUTPUT)
lbl(
    ax,
    last_cx,
    Y_OUT,
    "·" if TARGET_CHAR == " " else f"'{TARGET_CHAR}'",
    size=15,
    color="white",
    weight="bold",
)
lbl(ax, last_cx, Y_OUT - 0.48, "predicted next char", size=8, color="#888888")

# ── save ──────────────────────────────────────────────────────────────────────
OUT = "examples/rnn/rnn_overview.png"
plt.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=C_BG)
print(f"Saved: {OUT}")
plt.show()
