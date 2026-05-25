# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""AdaBoost: stump→strong classifier + cascade trade-off for q_0030."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0030_adaboost.png"
rng = np.random.default_rng(41)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # (a) Toy AdaBoost: combine 3 stumps in 2-D
    ax = axes[0]
    n = 200
    X = rng.normal(0, 1, size=(n, 2))
    y = ((X[:, 0] ** 2 + X[:, 1] ** 2) > 1.2).astype(int) * 2 - 1
    # Three axis-aligned stumps with weights
    stumps = [
        (0, +1.1, +1.0, 0.7),  # x[0] > 1.1 → +1
        (0, -1.1, -1.0, 0.7),  # x[0] < -1.1 → +1
        (1, +1.1, +1.0, 0.7),  # x[1] > 1.1 → +1
    ]
    grid = np.linspace(-3, 3, 200)
    gx, gy = np.meshgrid(grid, grid)
    Xg = np.stack([gx.ravel(), gy.ravel()], axis=1)
    score = np.zeros(len(Xg))
    for d, thr, sign, w in stumps:
        pred = np.where(sign * (Xg[:, d] - thr) > 0, 1, -1)
        score += w * pred
    score = score.reshape(gx.shape)
    ax.contourf(gx, gy, score, levels=20, cmap="RdBu_r", alpha=0.6)
    ax.contour(gx, gy, score, levels=[0], colors="black", linewidths=2)
    ax.scatter(*X[y == 1].T, s=18, color="tab:red", edgecolors="black", lw=0.3,
               label="object")
    ax.scatter(*X[y == -1].T, s=18, color="tab:blue", edgecolors="black", lw=0.3,
               label="background")
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect("equal")
    ax.set_title("(a) Strong classifier from 3 weak stumps\n"
                 "(weighted vote → curved decision boundary)")
    ax.legend(loc="lower left", fontsize=10)
    ax.grid(alpha=0.3)

    # (b) Cascade FPR & survival — illustrates why few-feature early stages help
    ax = axes[1]
    n_stages = 20
    # each stage: tdr 0.995, fpr 0.5  (Viola-Jones style)
    tdr, fpr = 0.995, 0.5
    stages = np.arange(1, n_stages + 1)
    cum_tdr = tdr ** stages
    cum_fpr = fpr ** stages
    ax.plot(stages, cum_tdr, "o-", color="tab:green", lw=2,
            label=f"cumulative detection rate  ({tdr}^k)")
    ax.plot(stages, cum_fpr, "s-", color="tab:red", lw=2,
            label=f"cumulative false-positive rate  ({fpr}^k)")
    ax.set_yscale("log")
    ax.set_xlabel("cascade stage  $k$")
    ax.set_ylabel("rate (log)")
    ax.set_title("(b) Cascade lets per-stage rates be loose\n"
                 "tiny FPR ($\\leq10^{-6}$) achieved by stacking many cheap stages")
    ax.axhline(1e-6, color="black", ls="--", lw=1, alpha=0.6)
    ax.text(n_stages - 0.5, 1.3e-6, "target FPR $10^{-6}$",
            ha="right", fontsize=9)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=10)

    fig.suptitle("AdaBoost in sliding-window detectors: "
                 "feature selection + cascade", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
