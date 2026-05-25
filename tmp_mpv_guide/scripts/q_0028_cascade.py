# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""TLD-style cascade rejection diagram for q_0028."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0028_cascade.png"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # (a) Cascade funnel
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    stages = [
        ("All windows\n$\\sim10^5$–$10^6$", 9.0, "#bfdbfe", "very cheap"),
        ("Variance filter\n(integral images)", 4.5, "#bbf7d0", "$O(1)$ per window"),
        ("Ensemble (Random Ferns)\npixel comparisons + LUTs", 1.0, "#fef3c7", "fast"),
        ("Nearest-Neighbour (NCC)\nvs. stored exemplars", 0.05, "#fecaca", "expensive"),
    ]
    n0 = 1e6
    for i, (name, frac, fc, cost) in enumerate(stages):
        y = 5.4 - i * 1.3
        width = 0.6 + 6.5 * (frac / n0 if i else 1.0) ** 0.25
        cx = 5.0
        ax.add_patch(FancyBboxPatch((cx - width / 2, y - 0.45),
                                    width, 0.9,
                                    boxstyle="round,pad=0.03",
                                    fc=fc, ec="black", lw=1.3))
        ax.text(cx, y, name, ha="center", va="center", fontsize=10)
        ax.text(cx + width / 2 + 0.2, y, f"$\\approx${int(frac):,}\n({cost})",
                ha="left", va="center", fontsize=9)
        if i + 1 < len(stages):
            ax.annotate("", xy=(cx, y - 0.6), xytext=(cx, y - 0.5),
                        arrowprops=dict(arrowstyle="->", lw=1.5))
            keep = stages[i + 1][1] / max(frac, 1)
            ax.text(cx - 0.05, y - 0.75, f"keep {keep:.1%}",
                    ha="right", va="center", fontsize=9, color="tab:red")
    ax.set_title("(a) Cascade funnel: cheap filters first, "
                 "expensive verification on tiny survivor set")

    # (b) Per-stage cost
    ax = axes[1]
    surv = [1e6, 5e5, 50, 5]
    cost = [1, 4, 50, 5000]  # nominal relative cost per evaluation
    total = [s * c for s, c in zip(surv, cost)]
    labels = ["all\nwindows", "after\nvariance", "after\nferns", "after\nNN"]
    width = 0.4
    xs = np.arange(len(labels))
    bars1 = ax.bar(xs - width / 2, surv, width, color="tab:blue",
                   edgecolor="black", label="# windows reaching stage")
    bars2 = ax.bar(xs + width / 2, total, width, color="tab:red",
                   edgecolor="black", label="total cost  (#wins × per-window cost)")
    for x, n, t in zip(xs, surv, total):
        ax.text(x - width / 2, n * 1.4, f"{n:.0e}", ha="center", fontsize=9)
        ax.text(x + width / 2, t * 1.4, f"{t:.0e}", ha="center", fontsize=9)
    ax.set_yscale("log")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.set_ylabel("count  /  cost  (log)")
    ax.set_title("(b) Why the cascade is fast\n"
                 "expensive stages only see ~50 survivors → bounded total cost")
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(alpha=0.3, axis="y", which="both")

    fig.suptitle("Sliding-window object detection with a coarse-to-fine cascade",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
