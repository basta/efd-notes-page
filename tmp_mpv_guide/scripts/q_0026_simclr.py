# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""SimCLR: pipeline + collapse without negatives for q_0026."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0026_simclr.png"
rng = np.random.default_rng(29)


def box(ax, x, y, w, h, text, fc="#fde68a"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                fc=fc, ec="black", lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(15, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1.0], wspace=0.2)

    # (a) Pipeline diagram
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    # Original image
    box(ax, 0.2, 2.7, 1.4, 1.0, "input  $\\mathbf{x}$", fc="#bfdbfe")
    # Two augmentations
    box(ax, 2.0, 4.4, 1.2, 0.7, "aug $t_1$", fc="#fef3c7")
    box(ax, 2.0, 1.3, 1.2, 0.7, "aug $t_2$", fc="#fef3c7")
    # Views
    box(ax, 3.6, 4.3, 1.2, 0.9, "$\\tilde{\\mathbf{x}}_i$", fc="#bfdbfe")
    box(ax, 3.6, 1.2, 1.2, 0.9, "$\\tilde{\\mathbf{x}}_j$", fc="#bfdbfe")
    # Encoders
    box(ax, 5.2, 4.3, 1.2, 0.9, "encoder $f$\n(shared)", fc="#a7f3d0")
    box(ax, 5.2, 1.2, 1.2, 0.9, "encoder $f$\n(shared)", fc="#a7f3d0")
    # Representations h
    box(ax, 6.8, 4.4, 0.9, 0.7, "$\\mathbf{h}_i$", fc="#bfdbfe")
    box(ax, 6.8, 1.3, 0.9, 0.7, "$\\mathbf{h}_j$", fc="#bfdbfe")
    ax.text(7.25, 3.2, "kept for\ndownstream",
            ha="center", fontsize=9, color="tab:green", fontweight="bold")
    # Projection head
    box(ax, 8.1, 4.3, 1.1, 0.9, "head $g$\n(MLP)", fc="#fecaca")
    box(ax, 8.1, 1.2, 1.1, 0.9, "head $g$\n(MLP)", fc="#fecaca")
    # Embeddings z
    box(ax, 9.4, 4.4, 0.5, 0.7, "$\\mathbf{z}_i$", fc="#bfdbfe")
    box(ax, 9.4, 1.3, 0.5, 0.7, "$\\mathbf{z}_j$", fc="#bfdbfe")
    ax.text(9.65, 3.2, "NT-Xent\nloss\n(discarded\nafter\ntraining)",
            ha="center", fontsize=8, color="tab:red")
    # Arrows
    def arr(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.2))
    arr(1.6, 3.4, 2.0, 4.7); arr(1.6, 3.0, 2.0, 1.7)
    arr(3.2, 4.7, 3.6, 4.7); arr(3.2, 1.7, 3.6, 1.7)
    arr(4.8, 4.7, 5.2, 4.7); arr(4.8, 1.7, 5.2, 1.7)
    arr(6.4, 4.7, 6.8, 4.7); arr(6.4, 1.7, 6.8, 1.7)
    arr(7.7, 4.7, 8.1, 4.7); arr(7.7, 1.7, 8.1, 1.7)
    arr(9.2, 4.7, 9.4, 4.7); arr(9.2, 1.7, 9.4, 1.7)
    # Maximise similarity (positive pair), push negatives apart
    ax.annotate("", xy=(9.6, 4.0), xytext=(9.6, 2.1),
                arrowprops=dict(arrowstyle="<->", color="tab:green", lw=2))
    ax.text(9.95, 3.0, "pull\ntogether",
            color="tab:green", fontsize=9, fontweight="bold")
    ax.set_title("(a) SimCLR pipeline: two augmented views, "
                 "shared encoder, disposable projection head")

    # (b) Collapse vs healthy embedding
    ax = fig.add_subplot(gs[0, 1])
    # Healthy: distinct clusters on unit circle
    angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    cmap = plt.cm.tab10(np.linspace(0, 1, 6))
    for i, a in enumerate(angles):
        c = np.array([np.cos(a), np.sin(a)])
        pts = c + rng.normal(0, 0.08, size=(15, 2))
        ax.scatter(*pts.T, s=30, color=cmap[i], edgecolors="black", lw=0.3,
                   alpha=0.9)
    # Collapsed: all near one point
    coll_centre = np.array([2.6, 0.0])
    coll = coll_centre + rng.normal(0, 0.05, size=(90, 2))
    ax.scatter(*coll.T, s=30, color="tab:gray", edgecolors="black", lw=0.3,
               alpha=0.7)
    ax.set_xlim(-1.8, 3.2)
    ax.set_ylim(-1.8, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0, -1.55, "with negatives\n(NT-Xent)", ha="center", fontsize=10,
            fontweight="bold", color="black")
    ax.text(2.6, -1.55, "positive-only\n→ collapse", ha="center", fontsize=10,
            fontweight="bold", color="tab:red")
    ax.set_title("(b) Negatives prevent representation collapse\n"
                 "(without them all embeddings → a single point)")

    fig.suptitle("SimCLR: contrastive instance discrimination & "
                 "the need for negatives", fontsize=13, y=1.02)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
