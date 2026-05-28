"""
Diagrams: RNN with Hidden State (correct representation)
==========================================================
Shows how an RNN processes one character at a time, carrying a
hidden state that encodes ALL previous context — not a fixed window.

Generates five images showing consecutive time steps:
  rnn_step1.png  —  processing 'o' (t=8);   h₇ → RNN → h₈,   predicts 't'
  rnn_step2.png  —  processing 't' (t=9);   h₈ → RNN → h₉,   predicts ' '
  rnn_step3.png  —  processing ' ' (t=10);  h₉ → RNN → h₁₀,  predicts 't'
  rnn_step4.png  —  processing 't' (t=11);  h₁₀ → RNN → h₁₁, predicts 'o'
  rnn_step5.png  —  processing 'o' (t=12);  h₁₁ → RNN → h₁₂, predicts ' '

Run from the repo root:
    python diagrams/rnn/01_rnn_with_hidden_state.py
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans"})

# ── data ───────────────────────────────────────────────────────────────────────
FULL_TEXT = "To be, or not to be"

# ── colours ────────────────────────────────────────────────────────────────────
C_BG = "#FAFAFA"
C_NEUTRAL = "#DDDDDD"  # unprocessed future characters
C_PREV = "#7BAED4"  # already-processed characters (lighter blue)
C_CURRENT = "#4C72B0"  # current input character
C_TARGET = "#C44E52"  # predicted / target character
C_INPUT = "#55A868"  # input box
C_RNN = "#4C72B0"  # RNN block
C_HIDDEN = "#DD8452"  # hidden state boxes and arrows
C_OUTPUT = "#C44E52"  # output box

# ── layout ─────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 11, 7.8
CHAR_PITCH = 0.52
TEXT_X0 = 0.56

Y_TEXT = 7.0  # text strip
Y_INPUT = 5.5  # input char box
Y_RNN = 3.7  # RNN block centre
Y_OUT = 1.9  # output box centre

RNN_W, RNN_H = 2.6, 0.92
IN_W, IN_H = 0.42, 0.54
HB_W, HB_H = 1.0, 0.60  # hidden-state box dimensions
H_GAP = 0.55  # gap between RNN edge and hidden-state box


def char_cx(i):
    """Centre x-coordinate of character i in the text strip."""
    return TEXT_X0 + i * CHAR_PITCH


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


def arrow(ax, x1, y1, x2, y2, color="#AAAAAA", lw=1.5, z=1):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw),
        zorder=z,
    )


def lbl(ax, x, y, s, size=11, color="#222222", weight="normal", ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=5)


# ── main diagram function ──────────────────────────────────────────────────────
def make_diagram(cur_pos, step_label, h_in_label, h_out_label, filename):
    """
    cur_pos     : index in FULL_TEXT of the character processed this step
    step_label  : e.g. "Step 1"
    h_in_label  : incoming hidden state label, e.g. "h₇"
    h_out_label : outgoing hidden state label, e.g. "h₈"
    """
    cur_char = FULL_TEXT[cur_pos]
    next_char = FULL_TEXT[cur_pos + 1]

    # Clamp RNN centre so hidden-state boxes stay inside the figure
    raw_cx = char_cx(cur_pos)
    min_cx = 0.3 + HB_W + H_GAP + RNN_W / 2
    max_cx = FIG_W - 0.3 - HB_W - H_GAP - RNN_W / 2
    rnn_cx = max(min_cx, min(max_cx, raw_cx))

    h_in_cx = rnn_cx - RNN_W / 2 - H_GAP - HB_W / 2
    h_out_cx = rnn_cx + RNN_W / 2 + H_GAP + HB_W / 2

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_facecolor(C_BG)
    fig.patch.set_facecolor(C_BG)
    ax.axis("off")

    # ── title ──────────────────────────────────────────────────────────────────
    lbl(
        ax,
        FIG_W / 2,
        FIG_H - 0.38,
        f"{step_label}  ·  one character in, hidden state updated",
        size=14,
        weight="bold",
        color="#111111",
    )

    # ── text strip ─────────────────────────────────────────────────────────────
    for i, ch in enumerate(FULL_TEXT):
        cx = char_cx(i)
        if i < cur_pos:
            fc, tc, bold = C_PREV, "white", False
        elif i == cur_pos:
            fc, tc, bold = C_CURRENT, "white", True
        elif i == cur_pos + 1:
            fc, tc, bold = C_TARGET, "white", True
        else:
            fc, tc, bold = C_NEUTRAL, "#555555", False

        rbox(ax, cx, Y_TEXT, 0.42, 0.48, fc=fc)
        lbl(
            ax,
            cx,
            Y_TEXT,
            "·" if ch == " " else ch,
            size=10,
            color=tc,
            weight="bold" if bold else "normal",
        )

    # "already processed" annotation over previous chars
    if cur_pos > 0:
        mid_x = (char_cx(0) + char_cx(cur_pos - 1)) / 2
        lbl(ax, mid_x, Y_TEXT - 0.56, "already processed →", size=8, color=C_PREV, ha="center")

    # current char underline + label
    ccx = char_cx(cur_pos)
    ax.plot([ccx - 0.26, ccx + 0.26], [Y_TEXT - 0.34] * 2, color=C_CURRENT, lw=2)
    lbl(ax, ccx, Y_TEXT - 0.56, "xₜ", size=8.5, color=C_CURRENT)
    lbl(ax, ccx, Y_TEXT - 0.76, "(current input)", size=7.5, color=C_CURRENT)

    # target char underline + label
    ncx = char_cx(cur_pos + 1)
    ax.plot([ncx - 0.26, ncx + 0.26], [Y_TEXT - 0.34] * 2, color=C_TARGET, lw=2)
    lbl(ax, ncx, Y_TEXT - 0.56, "target", size=8.5, color=C_TARGET)

    # ── current input char box ─────────────────────────────────────────────────
    arrow(ax, ccx, Y_TEXT - 0.68, ccx, Y_INPUT + IN_H / 2 + 0.06)
    rbox(ax, ccx, Y_INPUT, IN_W, IN_H, fc=C_INPUT)
    lbl(
        ax,
        ccx,
        Y_INPUT,
        "·" if cur_char == " " else cur_char,
        size=11,
        color="white",
        weight="bold",
    )

    # ── hidden state IN ────────────────────────────────────────────────────────
    rbox(ax, h_in_cx, Y_RNN, HB_W, HB_H, fc=C_HIDDEN)
    lbl(ax, h_in_cx, Y_RNN, h_in_label, size=11, color="white", weight="bold")
    lbl(
        ax,
        h_in_cx,
        Y_RNN - HB_H / 2 - 0.28,
        "hidden state\n(from previous step)",
        size=7.5,
        color="#888888",
        ha="center",
    )

    # arrow from h_in into RNN
    arrow(ax, h_in_cx + HB_W / 2, Y_RNN, rnn_cx - RNN_W / 2, Y_RNN, color=C_HIDDEN, lw=2.2, z=2)

    # ── RNN block ──────────────────────────────────────────────────────────────
    rbox(ax, rnn_cx, Y_RNN, RNN_W, RNN_H, fc=C_RNN)
    lbl(ax, rnn_cx, Y_RNN, "RNN", size=13, color="white", weight="bold")

    # arrow from input into RNN (with one-hot encoding in between)
    mid_y = (Y_INPUT - IN_H / 2 + Y_RNN + RNN_H / 2) / 2
    arrow(ax, ccx, Y_INPUT - IN_H / 2 - 0.06, ccx, mid_y + 0.12)
    lbl(ax, ccx, mid_y, "[0, 1, ..., 0]", size=7, color="#999999")
    arrow(ax, ccx, mid_y - 0.12, rnn_cx, Y_RNN + RNN_H / 2 + 0.06)

    # ── hidden state OUT ───────────────────────────────────────────────────────
    rbox(ax, h_out_cx, Y_RNN, HB_W, HB_H, fc=C_HIDDEN)
    lbl(ax, h_out_cx, Y_RNN, h_out_label, size=11, color="white", weight="bold")
    lbl(
        ax,
        h_out_cx,
        Y_RNN - HB_H / 2 - 0.28,
        "updated hidden state\n(encodes all context)",
        size=7.5,
        color="#888888",
        ha="center",
    )

    # arrow from RNN to h_out
    arrow(ax, rnn_cx + RNN_W / 2, Y_RNN, h_out_cx - HB_W / 2, Y_RNN, color=C_HIDDEN, lw=2.2, z=2)

    # ── output ─────────────────────────────────────────────────────────────────
    arrow(ax, rnn_cx, Y_RNN - RNN_H / 2, rnn_cx, Y_OUT + 0.36)
    rbox(ax, rnn_cx, Y_OUT, 0.82, 0.60, fc=C_OUTPUT)
    lbl(
        ax,
        rnn_cx,
        Y_OUT,
        "·" if next_char == " " else f"'{next_char}'",
        size=15,
        color="white",
        weight="bold",
    )
    lbl(ax, rnn_cx, Y_OUT - 0.48, "predicted next char", size=8, color="#888888")

    # ── save ───────────────────────────────────────────────────────────────────
    plt.savefig(f"diagrams/rnn/{filename}", dpi=150, bbox_inches="tight", facecolor=C_BG)
    print(f"Saved: diagrams/rnn/{filename}")
    plt.close()


# ── generate multiple time steps ──────────────────────────────────────────────
if __name__ == "__main__":
    # Step 1: processing 'o' at position 11 → predicts 't'
    make_diagram(
        cur_pos=11,
        step_label="Step 1",
        h_in_label="h₇",
        h_out_label="h₈",
        filename="rnn_step1.png",
    )

    # Step 2: processing 't' at position 12 → predicts ' '
    make_diagram(
        cur_pos=12,
        step_label="Step 2",
        h_in_label="h₈",
        h_out_label="h₉",
        filename="rnn_step2.png",
    )

    # Step 3: processing ' ' at position 13 → predicts 't'
    make_diagram(
        cur_pos=13,
        step_label="Step 3",
        h_in_label="h₉",
        h_out_label="h₁₀",
        filename="rnn_step3.png",
    )

    # Step 4: processing 't' at position 14 → predicts 'o'
    make_diagram(
        cur_pos=14,
        step_label="Step 4",
        h_in_label="h₁₀",
        h_out_label="h₁₁",
        filename="rnn_step4.png",
    )

    # Step 5: processing 'o' at position 15 → predicts ' '
    make_diagram(
        cur_pos=15,
        step_label="Step 5",
        h_in_label="h₁₁",
        h_out_label="h₁₂",
        filename="rnn_step5.png",
    )

    print("\nDone! Generated 5 time steps:")
    print("  • rnn_step1.png  —  shows h₇ + 'o' → RNN → h₈, predicts 't'")
    print("  • rnn_step2.png  —  shows h₈ + 't' → RNN → h₉, predicts ' '")
    print("  • rnn_step3.png  —  shows h₉ + ' ' → RNN → h₁₀, predicts 't'")
    print("  • rnn_step4.png  —  shows h₁₀ + 't' → RNN → h₁₁, predicts 'o'")
    print("  • rnn_step5.png  —  shows h₁₁ + 'o' → RNN → h₁₂, predicts ' '")
