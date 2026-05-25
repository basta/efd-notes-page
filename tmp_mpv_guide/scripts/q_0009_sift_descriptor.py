# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""SIFT descriptor construction for q_0009.

Shows the four stages of building a 4×4×8 = 128-d SIFT descriptor from a
canonicalised 16×16 patch:

  (a) normalised patch with grid overlay (4×4 spatial cells)
  (b) gradient field (quiver) modulated by Gaussian weight
  (c) per-cell orientation histograms drawn as 8-bin "stars"
  (d) the final 128-d vector before and after L2 + clip + L2 normalisation
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0009_sift_descriptor.png"

PATCH = 16
CELL = 4
NBIN = 8


def make_patch() -> np.ndarray:
    """16x16 patch with a diagonal edge + small dot — distinctive content."""
    yy, xx = np.mgrid[0:PATCH, 0:PATCH].astype(np.float32) - PATCH / 2
    # Diagonal step edge
    d = xx * np.cos(np.deg2rad(30)) + yy * np.sin(np.deg2rad(30))
    img = 60 + 180 / (1 + np.exp(-d / 1.2))
    # Small bright dot top-right quadrant
    img += 60 * np.exp(-((xx - 4) ** 2 + (yy + 4) ** 2) / (1.5 ** 2))
    rng = np.random.default_rng(0)
    img = np.clip(img + rng.normal(0, 1.5, img.shape), 0, 255).astype(np.uint8)
    return img


def gradients(patch: np.ndarray):
    f = patch.astype(np.float32)
    Lx = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3)
    Ly = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(Lx ** 2 + Ly ** 2)
    ang = (np.arctan2(Ly, Lx) + 2 * np.pi) % (2 * np.pi)
    return Lx, Ly, mag, ang


def sift_descriptor(patch: np.ndarray):
    """Hand-rolled SIFT-style descriptor with trilinear interpolation."""
    Lx, Ly, mag, ang = gradients(patch)
    # Gaussian weight, σ = patch_width / 2 = 8
    yy, xx = np.mgrid[0:PATCH, 0:PATCH].astype(np.float32) - PATCH / 2 + 0.5
    g = np.exp(-(xx ** 2 + yy ** 2) / (2 * (PATCH / 2.0) ** 2))
    w = mag * g

    # Spatial cell index ∈ [0, 3]
    cell_x = (np.arange(PATCH) // CELL).astype(np.int32)
    cell_y = (np.arange(PATCH) // CELL).astype(np.int32)
    bin_w = 2 * np.pi / NBIN

    descriptor = np.zeros((4, 4, NBIN), dtype=np.float64)
    for v in range(PATCH):
        for u in range(PATCH):
            cx, cy = cell_x[u], cell_y[v]
            f_idx = ang[v, u] / bin_w
            b0 = int(np.floor(f_idx)) % NBIN
            b1 = (b0 + 1) % NBIN
            frac = f_idx - np.floor(f_idx)
            descriptor[cy, cx, b0] += (1 - frac) * w[v, u]
            descriptor[cy, cx, b1] += frac * w[v, u]
    return descriptor, Lx, Ly, mag, g


def normalise_sift(d128: np.ndarray) -> np.ndarray:
    v = d128.copy()
    n = np.linalg.norm(v) + 1e-12
    v = v / n
    v = np.clip(v, 0, 0.2)
    n = np.linalg.norm(v) + 1e-12
    v = v / n
    return v


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    patch = make_patch()
    desc, Lx, Ly, mag, gauss = sift_descriptor(patch)
    desc_flat = desc.flatten()
    desc_norm = normalise_sift(desc_flat)

    # ---- Figure ----
    fig = plt.figure(figsize=(15, 9.5))
    gs = fig.add_gridspec(2, 3,
                          height_ratios=[1, 1],
                          width_ratios=[1, 1, 1.05],
                          hspace=0.28, wspace=0.18)

    # (a) normalised patch + 4×4 grid
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(patch, cmap="gray", extent=[0, PATCH, PATCH, 0])
    for k in range(0, PATCH + 1, CELL):
        ax.axvline(k, color="cyan", lw=0.8)
        ax.axhline(k, color="cyan", lw=0.8)
    ax.set_title("(a) 16×16 normalised patch  (4×4 spatial cells)")
    ax.set_xticks(np.arange(0, PATCH + 1, CELL))
    ax.set_yticks(np.arange(0, PATCH + 1, CELL))

    # (b) gradient field weighted by Gaussian
    ax = fig.add_subplot(gs[0, 1])
    ax.imshow(mag * gauss, cmap="magma", extent=[0, PATCH, PATCH, 0])
    yy, xx = np.mgrid[0:PATCH, 0:PATCH] + 0.5
    sc = 0.04
    ax.quiver(xx, yy, Lx * gauss * sc, -Ly * gauss * sc,
              color="cyan", scale=1, scale_units="xy", width=0.005)
    for k in range(0, PATCH + 1, CELL):
        ax.axvline(k, color="white", lw=0.6, alpha=0.5)
        ax.axhline(k, color="white", lw=0.6, alpha=0.5)
    ax.set_title("(b) Gradients × Gaussian weight (σ = patch/2)")
    ax.set_xticks([]); ax.set_yticks([])

    # (c) 4×4 grid of orientation histograms drawn as 8-spoke "stars"
    ax = fig.add_subplot(gs[0, 2])
    ax.imshow(patch, cmap="gray", alpha=0.45, extent=[0, PATCH, PATCH, 0])
    dmax = desc.max() + 1e-9
    for gy in range(4):
        for gx in range(4):
            cx_, cy_ = gx * CELL + CELL / 2, gy * CELL + CELL / 2
            for b in range(NBIN):
                ang = b * 2 * np.pi / NBIN
                L = desc[gy, gx, b] / dmax * (CELL / 2 - 0.3)
                ex = cx_ + L * np.cos(ang)
                ey = cy_ - L * np.sin(ang)  # image y axis flipped
                ax.plot([cx_, ex], [cy_, ey], color="tab:orange", lw=1.5)
    for k in range(0, PATCH + 1, CELL):
        ax.axvline(k, color="cyan", lw=0.6)
        ax.axhline(k, color="cyan", lw=0.6)
    ax.set_title("(c) Per-cell 8-bin orientation histogram (4×4 cells)")
    ax.set_xticks([]); ax.set_yticks([])

    # (d) 128-d vector before / after normalisation
    ax = fig.add_subplot(gs[1, :])
    idx = np.arange(128)
    raw_norm = desc_flat / (np.linalg.norm(desc_flat) + 1e-12)
    ax.bar(idx - 0.2, raw_norm, width=0.4, color="steelblue",
           label="after L2 only")
    ax.bar(idx + 0.2, desc_norm, width=0.4, color="tomato",
           label="after L2 → clip(0.2) → L2")
    # Cell boundaries
    for c in range(1, 16):
        ax.axvline(c * NBIN - 0.5, color="0.7", lw=0.5)
    ax.axhline(0.2, color="0.4", ls="--", lw=1, label="clip threshold 0.2")
    ax.set_xlim(-1, 128)
    ax.set_ylim(0, max(raw_norm.max(), desc_norm.max()) * 1.1)
    ax.set_xlabel("descriptor dimension (16 cells × 8 bins = 128)")
    ax.set_ylabel("value")
    ax.set_title("(d) 128-d SIFT vector before / after clipping and re-normalisation")
    ax.legend(loc="upper right", fontsize=10)

    fig.suptitle("Construction of the SIFT descriptor", fontsize=14, y=0.995)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")
    print(f"||raw||={np.linalg.norm(desc_flat):.2f}  "
          f"#clipped={int((raw_norm > 0.2).sum())}  "
          f"||final||={np.linalg.norm(desc_norm):.4f}")


if __name__ == "__main__":
    main()
