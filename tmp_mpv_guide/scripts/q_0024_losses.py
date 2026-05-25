# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Contrastive & Triplet losses + margin + hard negatives for q_0024."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0024_losses.png"
rng = np.random.default_rng(19)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # (a) Contrastive loss curves
    ax = axes[0]
    D = np.linspace(0, 2.5, 400)
    m = 1.0
    L_pos = 0.5 * D ** 2
    L_neg = 0.5 * np.clip(m - D, 0, None) ** 2
    ax.plot(D, L_pos, lw=2.4, color="tab:blue",
            label=r"positive:  $\frac{1}{2}D^2$")
    ax.plot(D, L_neg, lw=2.4, color="tab:red",
            label=fr"negative:  $\frac{{1}}{{2}}\max(0,\,m-D)^2$  ($m={m}$)")
    ax.axvline(m, color="black", ls="--", lw=1.2)
    ax.text(m + 0.02, 0.5, "$D = m$", fontsize=10)
    ax.set_xlabel("distance $D = \\|\\mathbf{X}_i - \\mathbf{X}_j\\|$")
    ax.set_ylabel("loss")
    ax.set_title("(a) Contrastive loss\nnegatives beyond margin are 'easy' → 0 gradient")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    # (b) Triplet hinge loss surface
    ax = axes[1]
    Dap, Dan = np.meshgrid(np.linspace(0, 2.0, 200), np.linspace(0, 2.5, 200))
    L = np.clip(Dap - Dan + m, 0, None)
    im = ax.imshow(L, extent=[0, 2.0, 0, 2.5], origin="lower",
                   cmap="YlOrRd", aspect="auto")
    ax.plot([0, 2], [m, 2 + m], color="black", lw=2)
    ax.text(1.0, 1.05 + m, "$D_{an} = D_{ap} + m$",
            color="black", fontsize=10, rotation=22)
    ax.set_xlabel("anchor–positive distance  $D_{ap}$")
    ax.set_ylabel("anchor–negative distance  $D_{an}$")
    ax.set_title(f"(b) Triplet loss $\\max(0, D_{{ap}} - D_{{an}} + m)$\n"
                 f"zero above the line (margin satisfied)")
    plt.colorbar(im, ax=ax, fraction=0.046)

    # (c) Hard vs easy negatives in 2D embedding
    ax = axes[2]
    anchor = np.array([0.0, 0.0])
    positive = np.array([0.2, 0.15])
    # Many easy negatives (far away)
    easy = rng.normal(0, 1.0, size=(40, 2))
    easy = easy / np.linalg.norm(easy, axis=1, keepdims=True) * \
           rng.uniform(1.5, 2.5, size=(40, 1))
    # A few hard negatives (close to anchor)
    hard = rng.normal(0, 0.4, size=(5, 2))
    hard = hard / np.linalg.norm(hard, axis=1, keepdims=True) * \
           rng.uniform(0.5, 0.9, size=(5, 1))
    ax.add_patch(Circle(anchor, m, fill=False, ec="black", ls="--", lw=1.5))
    ax.scatter(*anchor, marker="*", s=400, color="black",
               edgecolors="yellow", lw=1.5, zorder=5, label="anchor")
    ax.scatter(*positive, marker="P", s=200, color="tab:blue",
               edgecolors="black", lw=0.8, zorder=4, label="positive")
    ax.scatter(*hard.T, s=110, color="tab:red", edgecolors="black",
               lw=0.5, label=f"hard negatives ({len(hard)})")
    ax.scatter(*easy.T, s=35, color="tab:gray", alpha=0.5,
               label=f"easy negatives ({len(easy)})")
    ax.text(m * 0.7, m * 0.7, "margin", fontsize=10)
    ax.set_xlim(-2.8, 2.8)
    ax.set_ylim(-2.8, 2.8)
    ax.set_aspect("equal")
    ax.set_xlabel("descriptor dim 1")
    ax.set_ylabel("descriptor dim 2")
    ax.set_title("(c) Hard negatives lie inside the margin\n"
                 "only they give a non-zero gradient — must be mined")
    ax.legend(loc="lower left", fontsize=9)
    ax.grid(alpha=0.3)

    fig.suptitle("Contrastive & Triplet losses with margin; hard-negative mining",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
