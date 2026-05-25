# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""LoG scale selection visualisation for q_0003.

Builds a synthetic image of three dark blobs with different radii, computes
the scale-normalised LoG response σ²|∇²(G_σ * I)| over a range of σ, and
shows:

  (a) the image with the auto-selected characteristic scale drawn at each
      blob centre (the radius equals √2·σ̂, the LoG-blob relation),
  (b) the scale-normalised LoG response curve sampled at each blob centre,
      with vertical markers at the expected σ* = r/√2.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0003_log_scale.png"


def make_blob_image(h: int = 260, w: int = 520) -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    """Three dark blobs of radii 8, 18, 32 px on a bright background."""
    img = np.full((h, w), 230, dtype=np.uint8)
    blobs = [(90, 130, 8), (250, 130, 18), (430, 130, 32)]  # (cx, cy, r)
    for cx, cy, r in blobs:
        cv2.circle(img, (cx, cy), r, 30, -1)
    img = cv2.GaussianBlur(img, (5, 5), 1.0)
    rng = np.random.default_rng(0)
    img = np.clip(img + rng.normal(0, 2.0, img.shape), 0, 255).astype(np.uint8)
    return img, blobs


def scale_normalised_log(img: np.ndarray, sigma: float) -> np.ndarray:
    """σ² * (∂²/∂x² + ∂²/∂y²) of Gaussian-smoothed image, signed."""
    f = img.astype(np.float32) / 255.0
    L = cv2.GaussianBlur(f, (0, 0), sigma)
    Lxx = cv2.Sobel(L, cv2.CV_32F, 2, 0, ksize=3)
    Lyy = cv2.Sobel(L, cv2.CV_32F, 0, 2, ksize=3)
    return sigma * sigma * (Lxx + Lyy)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img, blobs = make_blob_image()

    sigmas = np.geomspace(1.0, 50.0, 40)
    # Pre-compute per-pixel max but we only need per-centre curves
    curves = {b: [] for b in blobs}
    response_volume = []
    for sigma in sigmas:
        Rn = scale_normalised_log(img, sigma)
        response_volume.append(Rn)
        for (cx, cy, r) in blobs:
            # For a *dark* blob on bright background, the LoG response at the
            # centre is positive — we take it directly.
            curves[(cx, cy, r)].append(Rn[cy, cx])
    response_volume = np.stack(response_volume, axis=0)  # (S, H, W)
    curves = {b: np.array(v) for b, v in curves.items()}

    # Pick the σ̂ that maximises the curve at each centre
    sigma_hat = {b: float(sigmas[int(np.argmax(curves[b]))]) for b in blobs}

    # ---- Figure ----
    fig = plt.figure(figsize=(13, 5.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1], wspace=0.18)

    # (a) image + selected scales
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    palette = ["tab:blue", "tab:orange", "tab:green"]
    for (cx, cy, r), col in zip(blobs, palette):
        s = sigma_hat[(cx, cy, r)]
        # The LoG of a 2D Gaussian peaks at σ = r/√2 for a disk of radius r,
        # so the natural visual circle has radius √2·σ̂.
        circ = mpatches.Circle((cx, cy), radius=np.sqrt(2) * s,
                               fill=False, edgecolor=col, lw=2.0)
        ax.add_patch(circ)
        ax.plot(cx, cy, "+", color=col, markersize=10, mew=2)
        ax.annotate(f"r={r}\nσ̂={s:.1f}", xy=(cx, cy),
                    xytext=(cx, cy + r + 18), color=col,
                    ha="center", fontsize=9, fontweight="bold")
    ax.set_title("(a) Auto-selected characteristic scale  (drawn radius = √2·σ̂)")
    ax.axis("off")

    # (b) scale-normalised LoG response curves
    ax = fig.add_subplot(gs[0, 1])
    for (cx, cy, r), col in zip(blobs, palette):
        ax.plot(sigmas, curves[(cx, cy, r)], color=col, lw=2,
                label=f"r={r} px")
        # Mark the *detected* extremum
        ax.axvline(sigma_hat[(cx, cy, r)], color=col, ls=":", lw=1.0, alpha=0.7)
        # Mark the *theoretical* peak r/√2
        ax.axvline(r / np.sqrt(2), color=col, ls="--", lw=1.0, alpha=0.5)
    ax.set_xscale("log")
    ax.set_xlabel("σ  (log scale)")
    ax.set_ylabel("σ² · ∇²L(x_c, y_c; σ)")
    ax.set_title("(b) Scale-normalised LoG response at each blob centre")
    ax.grid(alpha=0.3)
    ax.axhline(0, color="0.5", lw=0.7)
    legend_main = ax.legend(loc="upper right", fontsize=9)
    ax.add_artist(legend_main)
    handles = [
        plt.Line2D([0], [0], color="k", ls=":", label="detected σ̂"),
        plt.Line2D([0], [0], color="k", ls="--", label="theory  r/√2"),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=8)

    fig.suptitle("Scale selection via the scale-normalised Laplacian",
                 fontsize=13)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")
    for b in blobs:
        cx, cy, r = b
        print(f"  blob r={r}  σ̂={sigma_hat[b]:.2f}  expected r/√2={r/np.sqrt(2):.2f}")


if __name__ == "__main__":
    main()
