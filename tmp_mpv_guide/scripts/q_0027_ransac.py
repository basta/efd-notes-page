# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""RANSAC: line-fitting demo + iterations-vs-inlier-ratio plot for q_0027."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0027_ransac.png"
rng = np.random.default_rng(31)


def fit_line(p, q):
    """Line through two points."""
    dx, dy = q - p
    n = np.array([-dy, dx])
    n = n / np.linalg.norm(n)
    c = -n @ p
    return n, c


def dist_to_line(pts, n, c):
    return np.abs(pts @ n + c)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Synthetic line + outliers
    true_n = np.array([0.4, 1.0]); true_n /= np.linalg.norm(true_n)
    true_c = -0.4
    n_in = 60
    t = rng.uniform(-3, 3, size=n_in)
    inliers = -true_c * true_n + t[:, None] * np.array([true_n[1], -true_n[0]])
    inliers += rng.normal(0, 0.12, size=inliers.shape)
    n_out = 80
    outliers = rng.uniform(-4, 4, size=(n_out, 2))
    pts = np.vstack([inliers, outliers])
    is_inlier_gt = np.array([True] * n_in + [False] * n_out)

    # Run a basic RANSAC
    sigma = 0.3
    best_count = -1
    best_inliers = None
    best_line = None
    for _ in range(500):
        i, j = rng.choice(len(pts), size=2, replace=False)
        n, c = fit_line(pts[i], pts[j])
        d = dist_to_line(pts, n, c)
        inl = d < sigma
        if inl.sum() > best_count:
            best_count = inl.sum()
            best_inliers = inl
            best_line = (n, c)

    fig = plt.figure(figsize=(15, 5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.1, 1.1, 1.0], wspace=0.3)

    # (a) Data with outliers
    ax = fig.add_subplot(gs[0, 0])
    ax.scatter(*pts[~is_inlier_gt].T, s=22, color="tab:gray", alpha=0.6,
               label=f"outliers ({n_out})")
    ax.scatter(*pts[is_inlier_gt].T, s=22, color="tab:blue",
               label=f"inliers (gt) ({n_in})")
    eps_gt = n_in / len(pts)
    ax.set_title(f"(a) Data: $\\varepsilon$ = {eps_gt:.0%} inliers")
    ax.set_xlim(-4.5, 4.5); ax.set_ylim(-4, 4); ax.set_aspect("equal")
    ax.legend(fontsize=9); ax.grid(alpha=0.3)

    # (b) RANSAC result
    ax = fig.add_subplot(gs[0, 1])
    n, c = best_line
    xs = np.linspace(-4.5, 4.5, 2)
    ys = -(n[0] * xs + c) / n[1]
    ax.plot(xs, ys, "k-", lw=2, label="best hypothesis")
    # Threshold band
    band = sigma / abs(n[1])
    ax.fill_between(xs, ys - band, ys + band, alpha=0.15, color="tab:green",
                    label=f"inlier band  $\\sigma={sigma}$")
    ax.scatter(*pts[~best_inliers].T, s=22, color="tab:red", alpha=0.6,
               label="rejected outliers")
    ax.scatter(*pts[best_inliers].T, s=22, color="tab:green",
               edgecolors="black", lw=0.3,
               label=f"RANSAC inliers ({best_count})")
    ax.set_title("(b) Best hypothesis after RANSAC sampling")
    ax.set_xlim(-4.5, 4.5); ax.set_ylim(-4, 4); ax.set_aspect("equal")
    ax.legend(fontsize=9); ax.grid(alpha=0.3)

    # (c) Required iterations vs inlier ratio for several m, eta=0.99
    ax = fig.add_subplot(gs[0, 2])
    eps = np.linspace(0.05, 0.95, 200)
    eta = 0.99
    for m, col in zip([2, 4, 7, 8],
                      ["tab:blue", "tab:green", "tab:orange", "tab:red"]):
        k = np.log(1 - eta) / np.log(1 - eps ** m + 1e-300)
        ax.plot(eps, k, lw=2, color=col,
                label=f"$m={m}$  (e.g., {'line' if m == 2 else 'homography' if m == 4 else 'F-mat'})")
    ax.set_yscale("log")
    ax.set_xlabel("inlier ratio  $\\varepsilon$")
    ax.set_ylabel("required iterations  $k$  (log scale)")
    ax.set_title(f"(c) $k = \\frac{{\\log(1-\\eta)}}{{\\log(1-\\varepsilon^m)}}$,  "
                 f"$\\eta = {eta}$\nblows up for low $\\varepsilon$ and large $m$")
    ax.grid(which="both", alpha=0.3)
    ax.legend(fontsize=9)

    fig.suptitle("RANSAC: hypothesise from minimal sample, "
                 "verify by inlier count", fontsize=13, y=1.02)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
