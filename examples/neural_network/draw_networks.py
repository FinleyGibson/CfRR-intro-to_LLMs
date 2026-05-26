"""draw_networks.py — generate three neural-network architecture diagrams.

Diagram 1 – simple:  2 inputs, 2 hidden layers (3 nodes), 2 outputs
Diagram 2 – deep:    2 inputs, 5 hidden layers (3 nodes), 2 outputs
Diagram 3 – wide:    4 inputs, 5 hidden layers (5 nodes), 2 outputs

Colours are read from config.json in the same directory.
Output PNGs are written to the same directory.
"""

import json
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent

H_SPACE = 1.6  # horizontal gap between layer centres (data units)
V_SPACE = 1.0  # vertical gap between node centres (data units)
RADIUS = 0.25  # node radius (data units)


def load_config(path=HERE / "config.json"):
    with open(path) as f:
        return json.load(f)


def draw_network(layer_sizes, cfg, title, save_path, show_weight_labels=False):
    """Draw a fully-connected neural network and save it to *save_path*."""
    n_layers = len(layer_sizes)
    max_nodes = max(layer_sizes)

    # ── Node positions ───────────────────────────────────────────────────────
    pos = []
    for i, n in enumerate(layer_sizes):
        ys = list(np.linspace(-(n - 1) / 2, (n - 1) / 2, n) * V_SPACE)
        pos.append([(i * H_SPACE, y) for y in ys])

    # ── Figure size (equal aspect so circles stay circular) ─────────────────
    x_pad, y_pad = 0.7, 0.6
    label_h = 0.7
    data_w = (n_layers - 1) * H_SPACE + 2 * x_pad
    data_h = (max_nodes - 1) * V_SPACE + 2 * y_pad + label_h
    scale = min(11 / data_w, 7 / data_h)  # fit within 11 × 7 inches
    fig, ax = plt.subplots(figsize=(data_w * scale, data_h * scale))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(cfg["background"])
    ax.set_facecolor(cfg["background"])
    plt.rcParams["font.family"] = cfg["font_family"]

    # ── Edges ────────────────────────────────────────────────────────────────
    for i in range(n_layers - 1):
        for x1, y1 in pos[i]:
            for x2, y2 in pos[i + 1]:
                ax.plot([x1, x2], [y1, y2], color=cfg["edge"], lw=0.7, zorder=1, alpha=0.75)

    # ── Nodes ────────────────────────────────────────────────────────────────
    node_colours = [cfg["input"]] + [cfg["hidden"]] * (n_layers - 2) + [cfg["output"]]
    for layer_pos, colour in zip(pos, node_colours):
        for x, y in layer_pos:
            ax.add_patch(
                mpatches.Circle(
                    (x, y),
                    RADIUS,
                    facecolor=colour,
                    edgecolor=cfg["node_edge"],
                    linewidth=1.5,
                    zorder=2,
                )
            )

    # ── Node labels (inputs and outputs only) ──────────────────────────────
    for j, (x, y) in enumerate(pos[0]):
        ax.text(
            x,
            y,
            f"$x_{{{j + 1}}}$",
            ha="center",
            va="center",
            fontsize=cfg["font_size_label"],
            color="white",
            fontweight="bold",
            zorder=3,
        )

    for k, (x, y) in enumerate(pos[-1]):
        ax.text(
            x,
            y,
            f"$\\hat{{y}}_{{{k + 1}}}$",
            ha="center",
            va="center",
            fontsize=cfg["font_size_label"],
            color="white",
            fontweight="bold",
            zorder=3,
        )

    # ── Individual weight labels on first-layer edges ───────────────────────
    if show_weight_labels:
        fs_w = max(5, cfg["font_size_label"] - 2)
        for layer_idx in range(n_layers - 1):
            layer_in = pos[layer_idx]
            layer_out = pos[layer_idx + 1]
            n_in_l = len(layer_in)
            for i, (x1, y1) in enumerate(layer_in):
                t = (i + 1) / (n_in_l + 1)
                for j, (x2, y2) in enumerate(layer_out):
                    xm = x1 + t * (x2 - x1)
                    ym = y1 + t * (y2 - y1)
                    ax.text(
                        xm,
                        ym,
                        f"$w_{{{j + 1},{i + 1}}}$",
                        ha="center",
                        va="center",
                        fontsize=fs_w,
                        color="#333333",
                        zorder=4,
                        bbox=dict(
                            boxstyle="round,pad=0.08",
                            facecolor="white",
                            edgecolor="none",
                            alpha=0.85,
                        ),
                    )

    # ── Weight matrix labels between layers ──────────────────────────────────
    y_max = (max_nodes - 1) / 2 * V_SPACE
    y_w = y_max + RADIUS + 0.12
    for i in range(n_layers - 1):
        x_mid = (i + 0.5) * H_SPACE
        ax.text(
            x_mid,
            y_w,
            f"$W^{{({i + 1})}}$",
            ha="center",
            va="bottom",
            fontsize=cfg["font_size_label"],
            color="#666666",
            zorder=3,
        )

    # ── Layer labels ─────────────────────────────────────────────────────────
    y_bottom = -(max_nodes - 1) / 2 * V_SPACE
    label_y = y_bottom - RADIUS - 0.25
    layer_labels = ["Input"] + ["Hidden"] * (n_layers - 2) + ["Output"]
    for i, lbl in enumerate(layer_labels):
        ax.text(
            i * H_SPACE,
            label_y,
            lbl,
            ha="center",
            va="top",
            fontsize=cfg["font_size_label"],
            color="#555555",
        )

    # ── Legend ───────────────────────────────────────────────────────────────
    legend_handles = [
        mpatches.Patch(facecolor=cfg["input"], edgecolor=cfg["node_edge"], label="Input"),
        mpatches.Patch(facecolor=cfg["hidden"], edgecolor=cfg["node_edge"], label="Hidden"),
        mpatches.Patch(facecolor=cfg["output"], edgecolor=cfg["node_edge"], label="Output"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower right",
        fontsize=cfg["font_size_legend"],
        framealpha=0.9,
        edgecolor="#CCCCCC",
    )

    # ── Axis limits ──────────────────────────────────────────────────────────
    x_max = (n_layers - 1) * H_SPACE
    ax.set_xlim(-x_pad, x_max + x_pad)
    ax.set_ylim(label_y - 0.3, y_max + RADIUS + y_pad)

    ax.set_title(title, fontsize=cfg["font_size_title"], fontweight="bold", pad=8, color="#333333")

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        save_path, bbox_inches="tight", dpi=150, facecolor=cfg["background"], edgecolor="none"
    )
    plt.close(fig)
    print(f"  ✓  {Path(save_path).name}")


def main():
    cfg = load_config()

    networks = [
        # (layer_sizes,           title,                  filename)
        ([2, 3, 3, 2], "Simple Network", "diagram_0_simple.png", False),
        ([2, 3, 3, 2], "Simple Network", "diagram_1_simple.png", True),
        ([2, 3, 3, 3, 3, 3, 2], "Deep Network", "diagram_2_deep.png", False),
        ([4, 5, 5, 5, 5, 5, 2], "Wide & Deep Network", "diagram_3_wide_deep.png", False),
    ]

    print("Generating diagrams …")
    for layer_sizes, title, filename, show_w in networks:
        draw_network(layer_sizes, cfg, title, HERE / filename, show_weight_labels=show_w)
    print("Done.")


if __name__ == "__main__":
    main()
