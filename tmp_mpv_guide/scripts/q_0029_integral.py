# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Integral image: four-corner inclusion–exclusion + speed comparison for q_0029."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0029_integral.png"
rng = np.random.default_rng(37)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(15, 5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.05], wspace=0.32)

    # (a) Original image
    H, W = 8, 8
    img = rng.integers(0, 10, size=(H, W))
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(img, cmap="Greys", vmin=0, vmax=12)
    for i in range(H):
        for j in range(W):
            ax.text(j, i, int(img[i, j]), ha="center", va="center",
                    fontsize=9, color="tab:red")
    # Highlight rectangle R: rows 2..5, cols 1..4
    y1, y2 = 2, 5
    x1, x2 = 1, 4
    ax.add_patch(Rectangle((x1 - 0.5, y1 - 0.5), x2 - x1 + 1, y2 - y1 + 1,
                           fill=False, ec="tab:green", lw=2.5))
    region_sum = int(img[y1:y2 + 1, x1:x2 + 1].sum())
    ax.set_title(f"(a) Image $I$.  Want sum over R (green):  $\\Sigma_R = {region_sum}$")
    ax.set_xticks([]); ax.set_yticks([])

    # (b) Integral image with the four corners highlighted
    S = np.cumsum(np.cumsum(img, axis=0), axis=1)
    ax = fig.add_subplot(gs[0, 1])
    ax.imshow(S, cmap="Blues")
    for i in range(H):
        for j in range(W):
            ax.text(j, i, int(S[i, j]), ha="center", va="center",
                    fontsize=8, color="black")
    # Mark the four lookup points  A = (x1-1, y1-1), B = (x2, y1-1),
    # C = (x1-1, y2), D = (x2, y2)
    corners = [(x1 - 1, y1 - 1, "A", "tab:red"),
               (x2,     y1 - 1, "B", "tab:orange"),
               (x1 - 1, y2,     "C", "tab:purple"),
               (x2,     y2,     "D", "tab:green")]
    for cx, cy, lbl, col in corners:
        if cx >= 0 and cy >= 0:
            ax.add_patch(Rectangle((cx - 0.5, cy - 0.5), 1, 1,
                                   fill=False, ec=col, lw=2.5))
            ax.text(cx + 0.4, cy - 0.55, lbl,
                    fontsize=12, color=col, fontweight="bold")
    A = S[y1 - 1, x1 - 1] if (x1 > 0 and y1 > 0) else 0
    B = S[y1 - 1, x2] if y1 > 0 else 0
    C = S[y2, x1 - 1] if x1 > 0 else 0
    D = S[y2, x2]
    ax.set_title(f"(b) Integral image $S$.  Four corners (A,B,C,D)")
    ax.set_xticks([]); ax.set_yticks([])

    # (c) Inclusion-exclusion formula + speed comparison
    ax = fig.add_subplot(gs[0, 2])
    ax.axis("off")
    ax.text(0.5, 0.95,
            "$\\Sigma_R = D - B - C + A$\n"
            f"      $= {D} - {B} - {C} + {A} = {D - B - C + A}$",
            ha="center", va="top", fontsize=14,
            transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#fef3c7", ec="black", pad=0.5))
    # Speed-up curve
    pixels = np.array([4, 8, 16, 32, 64, 128, 256])
    naive = pixels ** 2     # rectangle pixels = patch_size^2
    integral = np.full_like(naive, 4)  # always 4 lookups
    ax_in = fig.add_axes([0.78, 0.18, 0.18, 0.55])
    ax_in.loglog(pixels, naive, "o-", color="tab:red",
                 label="naïve  $O(N_p)$")
    ax_in.loglog(pixels, integral, "s-", color="tab:green",
                 label="integral  $O(1)$ (= 4)")
    ax_in.set_xlabel("patch side", fontsize=9)
    ax_in.set_ylabel("ops / window", fontsize=9)
    ax_in.set_title("speed per window", fontsize=10)
    ax_in.tick_params(labelsize=8)
    ax_in.legend(fontsize=8, loc="upper left")
    ax_in.grid(which="both", alpha=0.3)

    fig.suptitle("Integral image: rectangle-sum (and variance) in constant time",
                 fontsize=13, y=1.02)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
