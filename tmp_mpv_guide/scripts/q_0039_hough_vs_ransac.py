# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Hough vs RANSAC: applicability map (param dim × inlier ratio × instances)."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0039_hough_vs_ransac.png"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # (a) RANSAC iterations vs inlier ratio for various m
    ax = axes[0]
    eps = np.linspace(0.05, 0.95, 200)
    eta = 0.99
    for m, col in zip([2, 3, 4, 7, 8],
                      ["tab:blue", "tab:cyan", "tab:green",
                       "tab:orange", "tab:red"]):
        k = np.log(1 - eta) / np.log(1 - eps ** m + 1e-300)
        ax.plot(eps, k, lw=2, color=col,
                label=f"RANSAC  $m={m}$")
    # Hough cost: ~ N * Q (independent of eps)
    N = 1000
    Q = 180
    ax.axhline(N * Q / 1000, color="black", ls="--", lw=2,
               label=f"Hough  $N \\cdot Q / 1000$ (≈ {N * Q // 1000})")
    ax.set_yscale("log")
    ax.set_xlabel("inlier ratio  $\\varepsilon$")
    ax.set_ylabel("cost  (RANSAC iters  /  Hough votes scaled)  [log]")
    ax.set_title("(a) Cost scaling\n"
                 "Hough flat in $\\varepsilon$; RANSAC explodes as $\\varepsilon\\!\\downarrow$ or $m\\!\\uparrow$")
    ax.legend(fontsize=9)
    ax.grid(which="both", alpha=0.3)

    # (b) Strengths matrix
    ax = axes[1]
    ax.axis("off")
    rows = ["param dim ≤ 3",
            "param dim ≥ 6",
            "very low $\\varepsilon$ (<10%)",
            "moderate $\\varepsilon$ (>30%)",
            "many instances",
            "single instance",
            "needs ANN/grid quantisation",
            "continuous parameters"]
    table = [
        ["★★★", "★"],     # low-dim
        ["—",   "★★★"],   # high-dim
        ["★★★", "★"],     # low eps
        ["★★",  "★★★"],   # moderate eps
        ["★★★", "★"],     # many instances
        ["★★",  "★★★"],   # single instance
        ["always", "no"], # discretisation
        ["binned", "★★★"],# continuous
    ]
    table = np.array(table)
    cmap_table = {"★★★": "#bbf7d0", "★★": "#fde68a",
                  "★": "#fecaca", "—": "#e5e7eb",
                  "always": "#fde68a", "no": "#bbf7d0",
                  "binned": "#fecaca"}
    ax.set_xlim(0, 3); ax.set_ylim(0, len(rows) + 1)
    ax.text(1.0, len(rows) + 0.5, "Hough", ha="center", fontsize=13,
            fontweight="bold")
    ax.text(2.0, len(rows) + 0.5, "RANSAC", ha="center", fontsize=13,
            fontweight="bold")
    for i, row_name in enumerate(rows):
        y = len(rows) - i - 0.5
        ax.text(0.05, y, row_name, va="center", fontsize=10)
        for j, val in enumerate(table[i]):
            ax.add_patch(plt.Rectangle((0.6 + j * 0.95, y - 0.4), 0.85, 0.8,
                                       fc=cmap_table[val], ec="black"))
            ax.text(0.6 + j * 0.95 + 0.425, y, val, ha="center", va="center",
                    fontsize=11, fontweight="bold")
    ax.set_title("(b) When each method shines")

    fig.suptitle("Hough vs. RANSAC: complementary robust fitters",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
