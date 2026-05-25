# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""VLAD: residual aggregation visualisation for q_0017."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0017_vlad.png"
rng = np.random.default_rng(3)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # 3 cluster centres in 2D
    centres = np.array([[-3.0, 1.5], [2.5, 2.0], [0.5, -2.5]])
    K, D = centres.shape
    # Generate descriptors around each centre
    pts = []
    asg = []
    for k, c in enumerate(centres):
        n = rng.integers(7, 14)
        spread = rng.normal(0, 0.9, size=(n, 2))
        pts.append(c + spread)
        asg.extend([k] * n)
    pts = np.vstack(pts)
    asg = np.array(asg)

    # Per-cluster residual sums
    v = np.zeros((K, D))
    for k in range(K):
        v[k] = (pts[asg == k] - centres[k]).sum(axis=0)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    cmap = ["tab:blue", "tab:orange", "tab:green"]

    # (a) Descriptors + centres + assignments
    ax = axes[0]
    for k in range(K):
        ax.scatter(*pts[asg == k].T, s=42, color=cmap[k], alpha=0.85,
                   edgecolors="black", lw=0.4, label=f"cluster {k+1}")
        ax.scatter(*centres[k], marker="X", s=220, color=cmap[k],
                   edgecolors="black", lw=1.5)
    ax.set_title("(a) Local descriptors quantised to nearest centroid\n"
                 "(X = centroid $\\mathbf{c}_k$)")
    ax.set_xlabel("descriptor dim 1")
    ax.set_ylabel("descriptor dim 2")
    ax.legend(loc="upper right", fontsize=9)
    ax.axis("equal")
    ax.grid(alpha=0.3)

    # (b) Residual vectors from each point to its centre
    ax = axes[1]
    for k in range(K):
        sub = pts[asg == k]
        for p in sub:
            ax.annotate("", xy=p, xytext=centres[k],
                        arrowprops=dict(arrowstyle="->", color=cmap[k], alpha=0.7, lw=1.2))
        ax.scatter(*sub.T, s=25, color=cmap[k])
        ax.scatter(*centres[k], marker="X", s=220, color=cmap[k],
                   edgecolors="black", lw=1.5)
    ax.set_title("(b) Residual vectors  $\\mathbf{r}(\\mathbf{x}) = \\mathbf{x} - \\mathbf{c}_k$\n"
                 "(arrows from centroid to each descriptor)")
    ax.set_xlabel("descriptor dim 1")
    ax.set_ylabel("descriptor dim 2")
    ax.axis("equal")
    ax.grid(alpha=0.3)

    # (c) Per-cluster sum-of-residuals as the VLAD sub-vectors
    ax = axes[2]
    for k in range(K):
        ax.scatter(*centres[k], marker="X", s=220, color=cmap[k],
                   edgecolors="black", lw=1.5)
        ax.annotate("", xy=centres[k] + v[k], xytext=centres[k],
                    arrowprops=dict(arrowstyle="->", color=cmap[k], lw=3))
        ax.text(*(centres[k] + v[k] / 2 + np.array([0.1, 0.3])),
                f"$\\mathbf{{V}}_{k+1}$", fontsize=13, color=cmap[k],
                fontweight="bold")
    ax.set_title("(c) Aggregated residual sums per cluster\n"
                 "$\\mathbf{V}_k = \\sum_{i:q(\\mathbf{x}_i)=k} (\\mathbf{x}_i-\\mathbf{c}_k)$  "
                 "→ concat → VLAD vector")
    ax.set_xlabel("descriptor dim 1")
    ax.set_ylabel("descriptor dim 2")
    ax.axis("equal")
    ax.grid(alpha=0.3)

    fig.suptitle("VLAD: aggregating first-order residual statistics per visual word",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
