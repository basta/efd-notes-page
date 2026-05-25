# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "matplotlib",
# ]
# ///
"""Precision@k / Recall@k / AP / mAP visualisation for q_0014.

We use the toy ranking from the lecture (10 results, relevant at ranks
1, 3, 5, 7, 9) for the first two panels, and three different query
rankings for the mAP demonstration in the third panel.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0014_map.png"


def pr_at_k(rel: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return arrays precision@k and recall@k for k = 1..N."""
    cum = np.cumsum(rel)
    ks = np.arange(1, len(rel) + 1)
    R = rel.sum()
    return cum / ks, cum / R


def average_precision(rel: np.ndarray) -> float:
    """AP = mean of precision at the positions where rel == 1."""
    p, _ = pr_at_k(rel)
    R = rel.sum()
    return float((p * rel).sum() / R)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # Toy ranking from the lecture
    rel_toy = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    P, Rc = pr_at_k(rel_toy)
    ap = average_precision(rel_toy)
    print(f"toy AP = {ap:.4f}")

    # Two extra rankings for the mAP panel
    rel_good = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
    rel_bad  = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    ap_good = average_precision(rel_good)
    ap_bad  = average_precision(rel_bad)
    mAP = np.mean([ap, ap_good, ap_bad])
    print(f"AP_good={ap_good:.4f}  AP_toy={ap:.4f}  AP_bad={ap_bad:.4f}  mAP={mAP:.4f}")

    fig = plt.figure(figsize=(15, 5.5))
    gs = fig.add_gridspec(1, 3, wspace=0.30)

    # (a) Bar chart of relevance + precision@k & recall@k overlaid
    ax = fig.add_subplot(gs[0, 0])
    ks = np.arange(1, len(rel_toy) + 1)
    colors = ["tab:green" if r else "tab:red" for r in rel_toy]
    ax.bar(ks, np.ones_like(ks), color=colors,
           edgecolor="black", lw=0.5)
    for i, r in enumerate(rel_toy):
        ax.text(i + 1, 0.5, "✓" if r else "✗",
                ha="center", va="center",
                fontsize=14, fontweight="bold",
                color="white")
    ax2 = ax.twinx()
    ax2.plot(ks, P, "o-", color="tab:blue", label="precision@k")
    ax2.plot(ks, Rc, "s-", color="tab:purple", label="recall@k")
    ax2.set_ylim(0, 1.05)
    ax2.set_ylabel("value")
    ax2.legend(loc="lower right", fontsize=10)
    ax.set_yticks([])
    ax.set_xticks(ks)
    ax.set_xlabel("rank k")
    ax.set_title("(a) Ranked list (toy):  ✓ = relevant, ✗ = not relevant\n"
                 "precision@k & recall@k vs k")

    # (b) Precision-recall curve with AP as the shaded area
    ax = fig.add_subplot(gs[0, 1])
    # Add origin and final points for nice envelope
    P_plot = np.concatenate([[1.0], P])
    R_plot = np.concatenate([[0.0], Rc])
    ax.plot(R_plot, P_plot, "o-", color="tab:blue", lw=2, markersize=7)
    # Highlight precision points at recall jumps (where relevant images sit)
    jumps = rel_toy.astype(bool)
    ax.scatter(Rc[jumps], P[jumps], color="tab:green", zorder=5,
               s=80, edgecolors="black",
               label="precision at each relevant hit")
    # Annotate
    for i, (rr, pp) in enumerate(zip(Rc[jumps], P[jumps])):
        ax.annotate(f"{pp:.2f}", (rr, pp),
                    xytext=(6, 6), textcoords="offset points", fontsize=9)
    # Shade area under PR curve (= AP for this discrete formula, by step)
    ax.fill_between(R_plot, 0, P_plot, step="post",
                    alpha=0.18, color="tab:blue",
                    label=f"AP = {ap:.3f}  (mean of green dots)")
    ax.set_xlabel("recall")
    ax.set_ylabel("precision")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.05)
    ax.set_title("(b) Precision–Recall curve;\n"
                 "AP = average of precision at recall jumps")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left", fontsize=10)

    # (c) mAP across three queries
    ax = fig.add_subplot(gs[0, 2])
    qs = ["query A (good)\n[1 1 1 1 1 0 0 0 0 0]",
          "query B (toy)\n[1 0 1 0 1 0 1 0 1 0]",
          "query C (bad)\n[0 0 0 0 0 1 1 1 1 1]"]
    aps = [ap_good, ap, ap_bad]
    xs = np.arange(3)
    bars = ax.bar(xs, aps, color=["tab:green", "tab:blue", "tab:red"],
                  edgecolor="black")
    for x, a in zip(xs, aps):
        ax.text(x, a + 0.02, f"AP={a:.3f}", ha="center", fontsize=11)
    ax.axhline(mAP, color="black", ls="--", lw=1.5,
               label=f"mAP = {mAP:.3f}")
    ax.set_xticks(xs)
    ax.set_xticklabels(qs, fontsize=9)
    ax.set_ylabel("Average Precision")
    ax.set_ylim(0, 1.15)
    ax.set_title("(c) Per-query AP → mAP")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("Precision@k, Recall@k, Average Precision, and mAP",
                 fontsize=13, y=1.02)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
