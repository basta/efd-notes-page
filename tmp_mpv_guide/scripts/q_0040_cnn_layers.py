# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""CNN building blocks: layer diagram + activation functions for q_0040."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0040_cnn_layers.png"


def box(ax, x, y, w, h, text, fc="#bfdbfe"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                fc=fc, ec="black", lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(15, 6))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.0], hspace=0.4)

    # (a) Pipeline
    ax = fig.add_subplot(gs[0])
    ax.set_xlim(0, 16); ax.set_ylim(0, 4); ax.axis("off")
    blocks = [
        ("input\n224×224×3", 0.2, 2.0, "#dbeafe"),
        ("conv 11×11×96\nstride 4 + ReLU", 1.8, 2.0, "#bbf7d0"),
        ("max-pool 3×3\nstride 2", 4.0, 1.6, "#fde68a"),
        ("conv 5×5×256\n+ ReLU", 5.7, 2.0, "#bbf7d0"),
        ("max-pool", 8.0, 1.6, "#fde68a"),
        ("conv ×3\n+ ReLU", 9.4, 2.0, "#bbf7d0"),
        ("max-pool", 11.4, 1.6, "#fde68a"),
        ("FC 4096\n+ ReLU + dropout", 12.8, 2.0, "#fecaca"),
        ("softmax\n→ 1000 classes", 15.0, 1.8, "#a7f3d0"),
    ]
    prev_x = None
    for name, x, h, fc in blocks:
        w = 1.5
        y = 2 - h / 2 + 0.2
        box(ax, x, y, w, h, name, fc=fc)
        if prev_x is not None:
            ax.annotate("", xy=(x, 2), xytext=(prev_x + 1.5, 2),
                        arrowprops=dict(arrowstyle="->", lw=1.5))
        prev_x = x
    ax.set_title("(a) Canonical CNN pipeline (AlexNet-style):  "
                 "conv → ReLU → pool → … → FC → softmax",
                 fontsize=12)

    # (b) Activation functions
    ax = fig.add_subplot(gs[1])
    x = np.linspace(-4, 4, 400)
    fns = [
        ("sigmoid", 1 / (1 + np.exp(-x)), "tab:gray", "saturates → vanishing grad"),
        ("tanh", np.tanh(x), "tab:purple", "saturates → vanishing grad"),
        ("ReLU = max(0,x)", np.maximum(0, x), "tab:red",
         "non-saturating; dead neurons for x<0"),
        ("Leaky ReLU (0.1)", np.where(x > 0, x, 0.1 * x), "tab:orange",
         "small slope for x<0 — cures dead ReLU"),
        ("GELU", 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3))),
         "tab:green", "smooth ReLU-like (used in transformers)"),
    ]
    for name, y, col, note in fns:
        ax.plot(x, y, color=col, lw=2.2, label=f"{name} — {note}")
    ax.axhline(0, color="black", lw=0.5)
    ax.axvline(0, color="black", lw=0.5)
    ax.set_ylim(-1.8, 4.0)
    ax.set_xlabel("input  $x$")
    ax.set_ylabel("$\\phi(x)$")
    ax.set_title("(b) Common non-linearities — ReLU and variants enable training of deep nets")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(alpha=0.3)

    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
