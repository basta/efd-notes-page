# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Recall@k surrogate: sigmoid approximations to step functions for q_0025."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0025_recall_surrogate.png"
rng = np.random.default_rng(23)


def sigmoid(x, tau):
    return 1.0 / (1.0 + np.exp(-x / tau))


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # (a) Sigmoid approximations of step at various temperatures
    ax = axes[0]
    x = np.linspace(-3, 3, 400)
    step = (x > 0).astype(float)
    ax.plot(x, step, color="black", lw=2.5, ls="--", label="step  $\\mathbf{1}[x>0]$")
    for tau, col in zip([0.1, 0.3, 1.0], ["tab:red", "tab:green", "tab:blue"]):
        ax.plot(x, sigmoid(x, tau), lw=2.2, color=col,
                label=f"$\\sigma_{{\\tau={tau}}}(x)$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("indicator value")
    ax.set_title("(a) Sigmoid temperature trade-off\n"
                 "small $\\tau$: tight approx, weak gradient\n"
                 "large $\\tau$: loose approx, strong gradient")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    # (b) Smooth rank of one positive given negatives
    ax = axes[1]
    s_pos = 0.6
    s_neg = rng.normal(0.4, 0.35, size=300)
    bins = np.linspace(-1, 2, 50)
    ax.hist(s_neg, bins=bins, color="tab:gray", alpha=0.7,
            label=f"negative similarities ({len(s_neg)})")
    ax.axvline(s_pos, color="tab:red", lw=2.5, label=f"positive  $s_i = {s_pos}$")
    true_rank = 1 + int(np.sum(s_neg > s_pos))
    smooth_ranks = {tau: 1 + sigmoid(s_neg - s_pos, tau).sum() for tau in [0.05, 0.2, 1.0]}
    txt = f"true rank = {true_rank}\n"
    txt += "\n".join([f"$\\widehat{{\\mathrm{{rank}}}}\\,(\\tau={t})$ = {r:.1f}"
                      for t, r in smooth_ranks.items()])
    ax.text(0.97, 0.97, txt, transform=ax.transAxes, ha="right", va="top",
            fontsize=10,
            bbox=dict(boxstyle="round", fc="white", ec="black"))
    ax.set_xlabel("similarity score $s$")
    ax.set_ylabel("count")
    ax.set_title("(b) Smooth rank of a positive\n"
                 "$\\widehat{\\mathrm{rank}}(i) = 1 + \\sum_{j} \\sigma_\\tau(s_j - s_i)$")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(alpha=0.3, axis="y")

    # (c) recall@k vs surrogate over training
    ax = axes[2]
    epochs = np.arange(0, 60)
    true_recall = 0.2 + 0.7 * (1 - np.exp(-epochs / 18))
    # surrogate (small tau): close, lags slightly behind
    surr_sm = true_recall - 0.04 * np.exp(-epochs / 25)
    # surrogate (large tau): optimistic, smoother gradient
    surr_lg = true_recall + 0.07 - 0.05 * np.exp(-epochs / 25)
    ax.plot(epochs, true_recall, color="black", lw=2.5, label="true recall@k")
    ax.plot(epochs, surr_sm, color="tab:blue", lw=2, ls="--",
            label="surrogate, small $\\tau$ (tight, slow)")
    ax.plot(epochs, surr_lg, color="tab:red", lw=2, ls="--",
            label="surrogate, large $\\tau$ (loose, fast)")
    ax.set_xlabel("training epoch")
    ax.set_ylabel("recall@k  /  $\\widehat{\\mathrm{recall@k}}$")
    ax.set_title("(c) Training dynamics:  $\\tau$ trades approximation vs. gradient")
    ax.set_ylim(0.1, 1.0)
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(alpha=0.3)

    fig.suptitle("Making recall@k differentiable via sigmoid smoothing",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
