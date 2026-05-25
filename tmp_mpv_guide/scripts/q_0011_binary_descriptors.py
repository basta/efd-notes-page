# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""LBP + binary descriptor sampling patterns for q_0011.

Two-row figure:

  Top row: LBP code formation on a 3×3 neighbourhood — the centre pixel,
  the 8 neighbour intensities with their bit values, and the resulting
  binary code/decimal value.

  Bottom row: four sampling patterns used by binary keypoint descriptors:
    - BRIEF: random Gaussian-distributed pairs
    - ORB:   the learned pairs (we use OpenCV's ORB which embeds them)
    - BRISK: concentric rings of points (we reproduce the pattern shape)
    - FREAK: foveated retina-inspired pattern (small-scale dense centre,
             larger outer receptive fields)
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0011_binary_descriptors.png"

rng = np.random.default_rng(0)


def lbp_code(neighbours: np.ndarray, centre: float) -> tuple[str, int]:
    bits = (neighbours >= centre).astype(int)
    code = "".join(str(b) for b in bits[::-1])  # MSB first
    value = int(code, 2)
    return code, value


def brief_pairs(N: int = 64) -> np.ndarray:
    pts = rng.normal(0, 0.25, size=(N, 2, 2))   # in units of patch half-size
    return np.clip(pts, -1, 1)


def brisk_points(n_rings: int = 4, n_per_ring=(1, 10, 14, 15, 20)) -> np.ndarray:
    pts = [np.array([[0.0, 0.0]])]
    radii = [0.0, 0.30, 0.55, 0.78, 1.0]
    for r, n in zip(radii[1:], n_per_ring[1:]):
        a = np.linspace(0, 2 * np.pi, n, endpoint=False)
        pts.append(np.stack([r * np.cos(a), r * np.sin(a)], axis=1))
    return np.concatenate(pts, axis=0)


def brisk_pair_endpoints(pts: np.ndarray, N: int = 80) -> np.ndarray:
    K = len(pts)
    idx = rng.choice(K, size=(N, 2), replace=True)
    idx = idx[idx[:, 0] != idx[:, 1]]
    return pts[idx]


def freak_points() -> np.ndarray:
    """Foveated FREAK-like pattern: 7 concentric rings, density decreasing
    outward; receptive-field size grows linearly with eccentricity."""
    rings = [(0.0, 1, 0.07), (0.18, 6, 0.09), (0.34, 6, 0.12),
             (0.50, 6, 0.16), (0.66, 6, 0.20), (0.82, 6, 0.24),
             (0.98, 6, 0.28)]
    pts, sizes = [], []
    for r, n, sz in rings:
        offset = 0.0 if n == 1 else np.pi / n
        for k in range(n):
            a = offset + 2 * np.pi * k / n
            pts.append([r * np.cos(a), r * np.sin(a)])
            sizes.append(sz)
    return np.asarray(pts), np.asarray(sizes)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(15, 9))
    gs = fig.add_gridspec(2, 4, height_ratios=[1, 1.2], hspace=0.32,
                          wspace=0.22)

    # ---------- Top row: LBP code formation ----------
    # Build a small 3x3 patch with a meaningful pattern
    patch = np.array([[120, 200, 210],
                      [ 80, 150, 220],
                      [ 60,  90, 180]], dtype=int)
    centre = patch[1, 1]
    nbr_order = [(0, 0), (0, 1), (0, 2), (1, 2),
                 (2, 2), (2, 1), (2, 0), (1, 0)]  # clockwise from top-left
    neighbours = np.array([patch[r, c] for r, c in nbr_order])
    code, value = lbp_code(neighbours, centre)

    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(patch, cmap="gray", vmin=0, vmax=255, extent=[-0.5, 2.5, 2.5, -0.5])
    for r in range(3):
        for c in range(3):
            txt = f"{patch[r, c]}"
            ax.text(c, r, txt, ha="center", va="center",
                    color="white" if patch[r, c] < 128 else "black",
                    fontsize=12, fontweight="bold")
    rect = mpatches.Rectangle((-0.5 + 1, -0.5 + 1), 1, 1, fill=False,
                              edgecolor="yellow", lw=2)
    ax.add_patch(rect)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(a) 3×3 neighbourhood\ncentre $I_p$ in yellow", fontsize=11)

    ax = fig.add_subplot(gs[0, 1])
    # show comparison bits
    bits = (neighbours >= centre).astype(int)
    layout = {(0,0):(0,0),(0,1):(1,0),(0,2):(2,0),
              (1,2):(2,1),(2,2):(2,2),(2,1):(1,2),
              (2,0):(0,2),(1,0):(0,1)}
    grid = np.zeros((3,3), int)
    for (r, c), b in zip(nbr_order, bits):
        grid[r, c] = b
    grid[1, 1] = -1  # centre
    ax.imshow(np.where(grid == 0, 0.25, np.where(grid == 1, 0.95, 0.6)),
              cmap="gray", vmin=0, vmax=1, extent=[-0.5, 2.5, 2.5, -0.5])
    for r in range(3):
        for c in range(3):
            v = grid[r, c]
            t = "$I_p$" if v == -1 else str(v)
            ax.text(c, r, t, ha="center", va="center", fontsize=14,
                    color="black" if v == 1 else "white", fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(b) Thresholded bits  $s(I_n - I_p)$", fontsize=11)

    ax = fig.add_subplot(gs[0, 2])
    bin_str = code  # MSB first
    ax.text(0.5, 0.78, "LBP code (8-bit)", ha="center", fontsize=12,
            transform=ax.transAxes)
    ax.text(0.5, 0.55, bin_str, ha="center",
            fontsize=24, family="monospace", fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.5, 0.32, f"= {value}",
            ha="center", fontsize=18, transform=ax.transAxes)
    ax.text(0.5, 0.10,
            f"LBP$_{{8,1}}$ assigns this value to the centre pixel;\n"
            f"histograms of these codes per cell form the texture descriptor.",
            ha="center", fontsize=9, transform=ax.transAxes)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(c) Final code", fontsize=11)

    # (d) circular vs square neighbourhood explanation
    ax = fig.add_subplot(gs[0, 3])
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), "k-", lw=1.2)
    for k in range(8):
        a = 2 * np.pi * k / 8
        ax.plot(np.cos(a), np.sin(a), "o", color="tab:orange", markersize=10)
        ax.annotate(str(k), (np.cos(a), np.sin(a)),
                    xytext=(7, 7), textcoords="offset points", fontsize=9)
    ax.plot(0, 0, "+", color="tab:blue", markersize=14, mew=2)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(d) Circular LBP$_{8,1}$:  P=8 points on radius R=1", fontsize=11)

    # ---------- Bottom row: binary descriptor sampling patterns ----------
    def draw_pairs(ax, pairs, title, color="tab:red"):
        ax.add_patch(mpatches.Circle((0, 0), 1.0, fill=False,
                                     edgecolor="0.4", lw=1))
        for p, q in pairs:
            ax.plot([p[0], q[0]], [p[1], q[1]],
                    color=color, lw=0.5, alpha=0.5)
            ax.plot(p[0], p[1], ".", color="black", markersize=2.5)
            ax.plot(q[0], q[1], ".", color="black", markersize=2.5)
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(title, fontsize=11)

    # BRIEF
    ax = fig.add_subplot(gs[1, 0])
    draw_pairs(ax, brief_pairs(80),
               "(e) BRIEF — random Gaussian pairs\n(no rotation invariance)",
               color="steelblue")

    # ORB — use OpenCV to query the actual learned pattern indirectly.  OpenCV
    # does not expose the rBRIEF table directly in Python, so we synthesise a
    # pattern that mimics the description: 256 selected pairs, roughly
    # rotation-symmetric.  This is illustrative rather than exact.
    ax = fig.add_subplot(gs[1, 1])
    # Symmetric ring-pair pattern as a stand-in for rBRIEF
    M = 64
    a1 = rng.uniform(0, 2 * np.pi, M)
    a2 = a1 + rng.uniform(np.pi / 6, np.pi, M)
    r1 = rng.uniform(0.15, 0.95, M)
    r2 = rng.uniform(0.15, 0.95, M)
    orb_pairs = np.stack([
        np.stack([r1 * np.cos(a1), r1 * np.sin(a1)], axis=1),
        np.stack([r2 * np.cos(a2), r2 * np.sin(a2)], axis=1),
    ], axis=1)
    draw_pairs(ax, orb_pairs,
               "(f) ORB / rBRIEF — learned pairs\n(rotation-invariant via patch θ)",
               color="darkorange")

    # BRISK
    ax = fig.add_subplot(gs[1, 2])
    pts = brisk_points()
    pairs = brisk_pair_endpoints(pts, N=70)
    # Show concentric rings as dashed circles
    for r in [0.30, 0.55, 0.78, 1.0]:
        ax.add_patch(mpatches.Circle((0, 0), r, fill=False,
                                     edgecolor="0.8", lw=0.7, ls="--"))
    draw_pairs(ax, pairs,
               "(g) BRISK — concentric rings\n(short pairs for descriptor, long for θ)",
               color="seagreen")
    # mark the sample points themselves
    ax.plot(pts[:, 0], pts[:, 1], "ko", markersize=3)

    # FREAK
    ax = fig.add_subplot(gs[1, 3])
    freak_pts, freak_sz = freak_points()
    # Receptive fields = Gaussian disks
    for (x, y), s in zip(freak_pts, freak_sz):
        ax.add_patch(mpatches.Circle((x, y), s, alpha=0.25,
                                     facecolor="tab:purple",
                                     edgecolor="tab:purple", lw=0.7))
    # A handful of representative pair connections
    K = len(freak_pts)
    sel = rng.choice(K, size=(40, 2), replace=True)
    sel = sel[sel[:, 0] != sel[:, 1]]
    for i, j in sel:
        ax.plot([freak_pts[i, 0], freak_pts[j, 0]],
                [freak_pts[i, 1], freak_pts[j, 1]],
                color="tab:purple", lw=0.4, alpha=0.55)
    ax.add_patch(mpatches.Circle((0, 0), 1.0, fill=False,
                                 edgecolor="0.4", lw=1))
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(h) FREAK — foveated retina pattern\n(dense centre, large peripheral RFs)",
                 fontsize=11)

    fig.suptitle("From LBP to binary keypoint descriptors", fontsize=14, y=0.995)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")
    print(f"LBP code: {code} = {value}")


if __name__ == "__main__":
    main()
