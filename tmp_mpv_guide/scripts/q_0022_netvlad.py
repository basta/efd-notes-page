# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""NetVLAD: soft vs hard assignment for q_0022."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0022_netvlad.png"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Three centres on a line for clarity
    centres = np.array([-2.5, 0.0, 2.0])
    xs = np.linspace(-4, 4, 600)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # (a) Hard assignment (VLAD) vs Soft assignment (NetVLAD) weights
    ax = axes[0]
    cmap = ["tab:blue", "tab:green", "tab:red"]
    # hard
    hard = np.zeros((len(centres), len(xs)))
    nearest = np.argmin(np.abs(xs[None, :] - centres[:, None]), axis=0)
    for k in range(len(centres)):
        hard[k] = (nearest == k).astype(float)
    for k, c in enumerate(cmap):
        ax.plot(xs, hard[k], color=c, lw=1.6, ls="--",
                label=f"VLAD hard $\\mathbf{{1}}[q(\\mathbf{{x}})={k+1}]$" if k == 0
                else None)
    # soft
    alpha = 1.5
    d2 = (xs[None, :] - centres[:, None]) ** 2
    soft = np.exp(-alpha * d2)
    soft /= soft.sum(axis=0, keepdims=True)
    for k, c in enumerate(cmap):
        ax.plot(xs, soft[k], color=c, lw=2.2,
                label=f"NetVLAD soft $a_{k+1}(\\mathbf{{x}})$  ($\\alpha={alpha:g}$)")
    for c, col in zip(centres, cmap):
        ax.axvline(c, color=col, alpha=0.4, lw=1)
        ax.text(c, 1.08, f"$\\mathbf{{c}}_{cmap.index(col)+1}$",
                ha="center", color=col, fontsize=11, fontweight="bold")
    ax.set_xlabel("descriptor coordinate $\\mathbf{x}$ (1-D)")
    ax.set_ylabel("assignment weight")
    ax.set_title("(a) Hard vs. soft assignment\n"
                 "NetVLAD replaces argmin with a differentiable softmax")
    ax.set_ylim(-0.05, 1.2)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.3)

    # (b) Effect of temperature alpha
    ax = axes[1]
    for alpha, ls in zip([0.5, 1.5, 5.0, 50.0],
                         ["-", "-", "--", ":"]):
        d2 = (xs[None, :] - centres[:, None]) ** 2
        soft = np.exp(-alpha * d2)
        soft /= soft.sum(axis=0, keepdims=True)
        ax.plot(xs, soft[1], lw=2.2, ls=ls,
                label=f"$\\alpha = {alpha:g}$"
                + (" (≈ hard)" if alpha >= 50 else ""))
    for c in centres:
        ax.axvline(c, color="black", alpha=0.3, lw=0.8)
    ax.set_xlabel("descriptor coordinate $\\mathbf{x}$ (1-D)")
    ax.set_ylabel("soft weight to centre $\\mathbf{c}_2$")
    ax.set_title("(b) Temperature $\\alpha$ controls softness\n"
                 "large $\\alpha$ → assignment becomes hard; gradients vanish")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    fig.suptitle("NetVLAD: differentiable soft assignment over a learnable codebook",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
