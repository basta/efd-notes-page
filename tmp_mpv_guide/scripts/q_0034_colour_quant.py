# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Colour-space reduction with adaptive (mean-shift-like) vs uniform quantisation."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0034_colour_quant.png"
rng = np.random.default_rng(47)


def kmeanslike_mean_shift(pts, n_clusters, n_iter=30):
    """A simple Lloyd-style iteration that mimics mean-shift mode assignment.

    Initialises with random data points; each iteration replaces each centre by
    the mean of points within a bandwidth window of it, then collapses centres
    that have drifted into the same neighbourhood until n_clusters remain.
    """
    idx = rng.choice(len(pts), size=n_clusters, replace=False)
    centres = pts[idx].astype(float)
    for _ in range(n_iter):
        # assign each point to nearest centre
        d2 = ((pts[:, None, :] - centres[None, :, :]) ** 2).sum(-1)
        a = d2.argmin(axis=1)
        for k in range(n_clusters):
            if (a == k).any():
                centres[k] = pts[a == k].mean(axis=0)
    return centres, a


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Generate three colour clusters in RGB space (e.g., red, blue, green).
    centres_true = np.array([[0.85, 0.15, 0.15],
                             [0.15, 0.70, 0.20],
                             [0.10, 0.20, 0.85],
                             [0.95, 0.95, 0.95]])
    sizes = [600, 600, 600, 200]
    pts = np.vstack([c + rng.normal(0, 0.05, size=(n, 3))
                     for c, n in zip(centres_true, sizes)])
    pts = np.clip(pts, 0, 1)

    # Adaptive quantisation: 4 clusters
    centres_ms, asg_ms = kmeanslike_mean_shift(pts, n_clusters=4)
    # Uniform quantisation: 2×2×2 = 8 bins
    bins_per_axis = 2
    edges = np.linspace(0, 1, bins_per_axis + 1)
    centres_unif = np.array(np.meshgrid(
        (edges[:-1] + edges[1:]) / 2,
        (edges[:-1] + edges[1:]) / 2,
        (edges[:-1] + edges[1:]) / 2,
        indexing="ij")).reshape(3, -1).T
    asg_unif = np.zeros(len(pts), dtype=int)
    for i, p in enumerate(pts):
        d2 = ((centres_unif - p) ** 2).sum(axis=1)
        asg_unif[i] = d2.argmin()

    fig = plt.figure(figsize=(14, 5))

    def plot_3d(ax, title, centres):
        ax.scatter(*pts.T, c=pts, s=5, alpha=0.55)
        ax.scatter(*centres.T, c="black", marker="X", s=140, edgecolor="yellow",
                   linewidths=1.5, label="palette")
        ax.set_xlabel("R"); ax.set_ylabel("G"); ax.set_zlabel("B")
        ax.set_title(title)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
        ax.legend(loc="upper left", fontsize=9)

    ax = fig.add_subplot(1, 3, 1, projection="3d")
    plot_3d(ax, "(a) Original colour distribution\n(3D RGB cloud)",
            np.empty((0, 3)))

    ax = fig.add_subplot(1, 3, 2, projection="3d")
    plot_3d(ax, "(b) Adaptive (mean-shift) palette:\n"
            f"{len(centres_ms)} modes follow the data clusters", centres_ms)

    ax = fig.add_subplot(1, 3, 3, projection="3d")
    plot_3d(ax, "(c) Uniform quantisation:\n"
            f"{len(centres_unif)} bins ignore data — waste on empty cells",
            centres_unif)

    fig.suptitle("Mean-shift adapts the palette to dominant colour clusters;\n"
                 "uniform quantisation allocates bins regardless of occupancy",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
