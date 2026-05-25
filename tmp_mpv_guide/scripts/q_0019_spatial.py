# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Spatial verification: tentative correspondences vs. geometrically-consistent inliers."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0019_spatial.png"
rng = np.random.default_rng(5)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Build a synthetic image pair: query (left) and db (right).
    W, H = 6.0, 4.5
    # Inlier correspondences obey a similarity transform: F = sR + t.
    theta = np.deg2rad(15)
    s = 1.15
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    t = np.array([0.3, -0.2])

    n_in = 30
    pts_q = rng.uniform([1.0, 1.0], [W - 1, H - 1], size=(n_in, 2))
    pts_db = (s * pts_q @ R.T) + t + rng.normal(0, 0.05, size=pts_q.shape)
    # offset db so its drawing sits beside the query
    offset = np.array([W + 1.5, 0.0])
    pts_db_offset = pts_db + offset

    # Outlier correspondences (random)
    n_out = 25
    out_q = rng.uniform([0.3, 0.3], [W - 0.3, H - 0.3], size=(n_out, 2))
    out_db = rng.uniform([0.3, 0.3], [W - 0.3, H - 0.3], size=(n_out, 2)) + offset

    all_q = np.vstack([pts_q, out_q])
    all_db = np.vstack([pts_db_offset, out_db])
    is_inlier = np.array([True] * n_in + [False] * n_out)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    def draw_images(ax):
        # frame the two "images"
        for x0 in (0, W + 1.5):
            ax.add_patch(plt.Rectangle((x0, 0), W, H, fc="#f3f4f6",
                                       ec="black", lw=1.2))
        ax.text(W / 2, H + 0.25, "query", ha="center", fontsize=11, fontweight="bold")
        ax.text(W + 1.5 + W / 2, H + 0.25, "database image", ha="center",
                fontsize=11, fontweight="bold")
        ax.set_xlim(-0.5, 2 * W + 2)
        ax.set_ylim(-0.5, H + 0.8)
        ax.set_aspect("equal")
        ax.axis("off")

    # (a) All tentative correspondences from BoW
    ax = axes[0]
    draw_images(ax)
    for q, d in zip(all_q, all_db):
        ax.plot([q[0], d[0]], [q[1], d[1]], color="tab:gray", lw=0.7, alpha=0.7)
    ax.scatter(*all_q.T, s=20, color="tab:blue")
    ax.scatter(*all_db.T, s=20, color="tab:orange")
    ax.set_title(f"(a) Tentative correspondences from BoW: "
                 f"{len(all_q)} pairs sharing a visual word\n"
                 "BoW similarity sums them all — inflated by repetitive/clutter matches")

    # (b) Inliers only after RANSAC-style verification
    ax = axes[1]
    draw_images(ax)
    for q, d, ok in zip(all_q, all_db, is_inlier):
        c = "tab:green" if ok else "tab:red"
        a = 0.8 if ok else 0.25
        ax.plot([q[0], d[0]], [q[1], d[1]], color=c, lw=0.9, alpha=a,
                linestyle="-" if ok else ":")
    ax.scatter(*all_q.T, s=22, color="tab:blue")
    ax.scatter(*all_db.T, s=22, color="tab:orange")
    n_inl = int(is_inlier.sum())
    ax.set_title(f"(b) After geometric verification: "
                 f"{n_inl} inliers (green) / {len(all_q) - n_inl} outliers (red dotted)\n"
                 "inlier count is the new, geometry-aware similarity")

    fig.suptitle("Spatial verification turns BoW co-occurrences into a "
                 "geometrically-consistent score", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
