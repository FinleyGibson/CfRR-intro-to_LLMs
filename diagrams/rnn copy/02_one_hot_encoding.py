"""
Diagrams: One-Hot Character Encoding
======================================
Generates two images:

  one_hot_simple.png   —  tiny a/b/c/d example to show the principle
  one_hot_encoding.png —  the actual window chars from the Shakespeare example

Run from the repo root:
    python examples/rnn/02_one_hot_encoding.py
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans"})

# ── colours ────────────────────────────────────────────────────────────────────
C_BG = "#FAFAFA"
C_HOT = "#C44E52"  # the '1' cell
C_ZERO = "#EEEEEE"  # '0' cells
C_UNKNOWN = "#F4CCA0"  # chars outside the vocabulary
C_CHAR = "#4C72B0"  # left-hand character label


# ── helpers ────────────────────────────────────────────────────────────────────
def rbox(ax, cx, cy, w, h, fc, ec="white", lw=1.5, z=2):
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


def label(ax, x, y, s, size=10, color="#222222", weight="normal", ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=5)


def one_hot(ch, vocab):
    vec = [0] * len(vocab)
    if ch in vocab:
        vec[vocab.index(ch)] = 1
    return vec


# ── diagram function ───────────────────────────────────────────────────────────
def make_diagram(
    vocab,
    chars,
    filename,
    title,
    subtitle,
    cell_w=0.50,
    cell_h=0.62,
    num_size=11,
    char_label_size=14,
):
    """
    vocab       : list of strings — the full vocabulary (column headers)
    chars       : list of (char, display_label) tuples — rows to draw
    filename    : output path
    title       : main title string
    subtitle    : smaller subtitle string
    cell_w/h    : grid cell dimensions in figure-inches
    num_size    : font size for the 0/1 values in cells
    char_label_size : font size for the character label boxes
    """
    n_vocab = len(vocab)
    n_chars = len(chars)

    margin_l = 1.9  # left margin for character labels
    margin_r = 0.3  # right margin
    margin_t = 1.7  # top margin (title + subtitle + header)
    margin_b = 0.85  # bottom margin (dimension arrow + label)

    fig_w = margin_l + n_vocab * cell_w + margin_r
    fig_h = margin_t + n_chars * cell_h + margin_b

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.set_facecolor(C_BG)
    fig.patch.set_facecolor(C_BG)
    ax.axis("off")

    # ── title & subtitle ───────────────────────────────────────────────────────
    label(ax, fig_w / 2, fig_h - 0.38, title, size=15, weight="bold", color="#111111")
    label(ax, fig_w / 2, fig_h - 0.76, subtitle, size=9, color="#888888")

    # ── vocabulary header ──────────────────────────────────────────────────────
    y_header = fig_h - margin_t + cell_h * 0.3

    label(ax, margin_l / 2, y_header, "Char", size=9, color="#999999", weight="bold")

    for j, ch in enumerate(vocab):
        cx = margin_l + j * cell_w + cell_w / 2
        disp = "·" if ch == " " else ch
        label(ax, cx, y_header, disp, size=9, color="#333333", weight="bold")

    ax.plot(
        [margin_l - 0.1, margin_l + n_vocab * cell_w + 0.1],
        [y_header - cell_h * 0.42, y_header - cell_h * 0.42],
        color="#CCCCCC",
        lw=1.0,
    )

    # ── grid rows ──────────────────────────────────────────────────────────────
    for i, (ch, display) in enumerate(chars):
        row_cy = y_header - cell_h * (i + 1)
        vec = one_hot(ch, vocab)
        in_vocab = ch in vocab

        # character label box
        rbox(ax, margin_l / 2, row_cy, margin_l * 0.78, cell_h * 0.72, fc=C_CHAR)
        label(ax, margin_l / 2, row_cy, display, size=char_label_size, color="white", weight="bold")

        # arrow → grid
        ax.annotate(
            "",
            xy=(margin_l - 0.06, row_cy),
            xytext=(margin_l / 2 + margin_l * 0.39 + 0.05, row_cy),
            arrowprops=dict(arrowstyle="-|>", color="#BBBBBB", lw=1.3),
            zorder=3,
        )

        # grid cells
        for j, val in enumerate(vec):
            cx = margin_l + j * cell_w + cell_w / 2
            if not in_vocab:
                fc, cell_txt, tc = C_UNKNOWN, "?", "#AA6600"
            elif val == 1:
                fc, cell_txt, tc = C_HOT, "1", "white"
            else:
                fc, cell_txt, tc = C_ZERO, "0", "#BBBBBB"

            rbox(ax, cx, row_cy, cell_w - 0.06, cell_h * 0.72, fc=fc)
            label(
                ax,
                cx,
                row_cy,
                cell_txt,
                size=num_size,
                color=tc,
                weight="bold" if val == 1 else "normal",
            )

        # hot-cell index annotation
        if in_vocab:
            hot_j = vocab.index(ch)
            hot_cx = margin_l + hot_j * cell_w + cell_w / 2
            label(ax, hot_cx, row_cy - cell_h * 0.44, f"index {hot_j}", size=7.5, color=C_HOT)
        else:
            label(
                ax,
                margin_l + n_vocab * cell_w + 0.15,
                row_cy,
                "not in simplified vocab",
                size=8,
                color="#CC8800",
                ha="left",
            )

    # ── dimension arrow ────────────────────────────────────────────────────────
    bot_y = y_header - cell_h * (n_chars + 0.15)
    ax.annotate(
        "",
        xy=(margin_l + n_vocab * cell_w + 0.05, bot_y - 0.15),
        xytext=(margin_l - 0.05, bot_y - 0.15),
        arrowprops=dict(arrowstyle="<->", color="#AAAAAA", lw=1.3),
        zorder=3,
    )
    label(
        ax,
        margin_l + n_vocab * cell_w / 2,
        bot_y - 0.42,
        f"{n_vocab}-dimensional vector  (one element = 1, all others = 0)",
        size=9,
        color="#888888",
    )

    plt.savefig(filename, dpi=150, bbox_inches="tight", facecolor=C_BG)
    print(f"Saved: {filename}")
    plt.close()


# ── Diagram 1: simple a/b/c/d principle diagram ────────────────────────────────
make_diagram(
    vocab=["a", "b", "c", "d"],
    chars=[("a", "'a'"), ("b", "'b'"), ("c", "'c'"), ("d", "'d'")],
    filename="examples/rnn/one_hot_simple.png",
    title="One-Hot Encoding  ·  The Principle",
    subtitle="Each character maps to a vector with exactly one '1' at its vocabulary index",
    cell_w=1.1,
    cell_h=0.82,
    num_size=16,
    char_label_size=16,
)

# ── Diagram 2: Shakespeare window chars (simplified vocab) ─────────────────────
make_diagram(
    vocab=[" "] + list("abcdefghijklmnopqrstuvwxyz"),
    chars=[("b", "'b'"), ("e", "'e'"), (",", "','"), (" ", "' '")],
    filename="examples/rnn/one_hot_encoding.png",
    title="One-Hot Encoding  ·  Shakespeare Example",
    subtitle="Vocabulary: space + a–z  (27 chars · simplified; real vocab includes uppercase & punctuation)",
    cell_w=0.50,
    cell_h=0.62,
    num_size=8.5,
    char_label_size=14,
)
