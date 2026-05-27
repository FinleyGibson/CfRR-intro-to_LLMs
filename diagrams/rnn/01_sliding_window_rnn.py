"""
Diagrams: Single RNN block with sliding context window.
=========================================================
Generates two nearly-identical images:
  rnn_step1.png  —  window at positions 7–10  ("or·n" → 'o')
  rnn_step2.png  —  window shifted one right   ("r·no" → 't')

Run from the repo root:
    python examples/rnn/01_sliding_window_rnn.py
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans"})

# ── data ───────────────────────────────────────────────────────────────────────
FULL_TEXT = "To be, or not to be"
WIN_LEN = 4

# ── colours ────────────────────────────────────────────────────────────────────
C_BG = "#FAFAFA"
C_NEUTRAL = "#DDDDDD"
C_WIN = "#4C72B0"  # blue  – context window
C_TARGET = "#C44E52"  # red   – target character
C_INPUT = "#55A868"  # green – input boxes
C_RNN = "#4C72B0"  # blue  – RNN block
C_OUTPUT = "#C44E52"  # red   – predicted output

# ── layout ─────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 11, 7.2
CHAR_PITCH = 0.52  # spacing between text characters
TEXT_X0 = 0.56  # x-centre of character index 0

Y_TEXT = 6.1  # text strip
Y_INPUT = 4.65  # input character boxes
Y_RNN = 3.1  # RNN block centre
Y_OUT = 1.55  # output box centre

RNN_W, RNN_H = 2.8, 0.92  # RNN block dimensions
IN_W, IN_H = 0.42, 0.54  # input box dimensions (matches text-strip cells)


def char_cx(i):
    """Centre x-coordinate of character i in the text strip."""
    return TEXT_X0 + i * CHAR_PITCH


# ── drawing helpers ────────────────────────────────────────────────────────────
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


def arrow(ax, x1, y1, x2, y2, color="#AAAAAA", lw=1.5):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw),
        zorder=1,
    )


def label(ax, x, y, s, size=11, color="#222222", weight="normal", ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=5)


# ── main diagram function ──────────────────────────────────────────────────────
def make_diagram(win_start, step_label, filename):
    win_chars = list(FULL_TEXT[win_start : win_start + WIN_LEN])
    target_char = FULL_TEXT[win_start + WIN_LEN]
    input_xs = [char_cx(win_start + i) for i in range(WIN_LEN)]
    rnn_cx = sum(input_xs) / WIN_LEN  # centred on the window

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_facecolor(C_BG)
    fig.patch.set_facecolor(C_BG)
    ax.axis("off")

    # ── title ──────────────────────────────────────────────────────────────────
    label(
        ax,
        FIG_W / 2,
        FIG_H - 0.38,
        f"{step_label}  ·  next-character prediction",
        size=14,
        weight="bold",
        color="#111111",
    )

    # ── text strip ─────────────────────────────────────────────────────────────
    for i, ch in enumerate(FULL_TEXT):
        cx = char_cx(i)
        in_win = win_start <= i < win_start + WIN_LEN
        is_tgt = i == win_start + WIN_LEN
        fc = C_WIN if in_win else (C_TARGET if is_tgt else C_NEUTRAL)
        tc = "white" if (in_win or is_tgt) else "#555555"
        rbox(ax, cx, Y_TEXT, 0.42, 0.48, fc=fc)
        label(
            ax,
            cx,
            Y_TEXT,
            "·" if ch == " " else ch,
            size=10,
            color=tc,
            weight="bold" if (in_win or is_tgt) else "normal",
        )

    # window underline + label
    bx0 = char_cx(win_start) - 0.27
    bx1 = char_cx(win_start + WIN_LEN - 1) + 0.27
    ax.plot([bx0, bx1], [Y_TEXT - 0.34, Y_TEXT - 0.34], color=C_WIN, lw=2)
    label(ax, (bx0 + bx1) / 2, Y_TEXT - 0.56, "context window", size=8.5, color=C_WIN)

    # target underline + label
    tx = char_cx(win_start + WIN_LEN)
    ax.plot([tx - 0.26, tx + 0.26], [Y_TEXT - 0.34, Y_TEXT - 0.34], color=C_TARGET, lw=2)
    label(ax, tx, Y_TEXT - 0.56, "target", size=8.5, color=C_TARGET)

    # ── input character boxes (directly below their text-strip position) ───────
    for ch, cx in zip(win_chars, input_xs):
        arrow(ax, cx, Y_TEXT - 0.68, cx, Y_INPUT + IN_H / 2 + 0.06)
        rbox(ax, cx, Y_INPUT, IN_W, IN_H, fc=C_INPUT)
        label(ax, cx, Y_INPUT, "·" if ch == " " else ch, size=12, color="white", weight="bold")

    # ── converging arrows: input boxes → top of RNN block ─────────────────────
    # Spread arrival points evenly across the top of the RNN box so the
    # arrows fan in cleanly rather than all hitting the same pixel.
    pad = 0.45
    top_xs = [
        rnn_cx - RNN_W / 2 + pad + i * (RNN_W - 2 * pad) / (WIN_LEN - 1) for i in range(WIN_LEN)
    ]
    for cx, top_cx in zip(input_xs, top_xs):
        arrow(ax, cx, Y_INPUT - IN_H / 2, top_cx, Y_RNN + RNN_H / 2 + 0.04)

    # ── RNN block ──────────────────────────────────────────────────────────────
    rbox(ax, rnn_cx, Y_RNN, RNN_W, RNN_H, fc=C_RNN)
    label(ax, rnn_cx, Y_RNN, "RNN", size=20, color="white", weight="bold")

    # ── output ─────────────────────────────────────────────────────────────────
    arrow(ax, rnn_cx, Y_RNN - RNN_H / 2, rnn_cx, Y_OUT + 0.36)
    rbox(ax, rnn_cx, Y_OUT, 0.78, 0.60, fc=C_OUTPUT)
    label(
        ax,
        rnn_cx,
        Y_OUT,
        "·" if target_char == " " else f"'{target_char}'",
        size=14,
        color="white",
        weight="bold",
    )
    label(ax, rnn_cx, Y_OUT - 0.48, "predicted next char", size=8.5, color="#888888")

    plt.savefig(filename, dpi=150, bbox_inches="tight", facecolor=C_BG)
    print(f"Saved: {filename}")
    plt.close()


# ── generate both steps ────────────────────────────────────────────────────────
# Step 1: window over "or·n"  (indices 7–10)  →  predicts 'o'
# Step 2: window over "r·no"  (indices 8–11)  →  predicts 't'
make_diagram(win_start=7, step_label="Step 1", filename="examples/rnn/rnn_step1.png")
make_diagram(win_start=8, step_label="Step 2", filename="examples/rnn/rnn_step2.png")
