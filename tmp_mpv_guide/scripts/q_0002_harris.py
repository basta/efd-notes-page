# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""Harris corner detector visualisation for q_0002.

Builds a synthetic image containing a corner, an edge and a flat region,
computes the second-moment matrix M at each location, and produces a
3-panel figure:

  (a) the source image with the three probe locations marked,
  (b) the iso-contour ellipses of E(Δx, Δy) at the three probes
      (shape comes directly from the eigenvalues of M),
  (c) the full cornerness response R together with the detected
      Harris keypoints (after thresholding + non-maximum suppression).
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0002_harris.png"


def build_scene(h: int = 240, w: int = 320) -> np.ndarray:
    """Synthetic image with corner, edge, and flat regions."""
    img = np.full((h, w), 220, dtype=np.uint8)
    # Big dark square in the upper-left → its corner is a clean Harris point
    cv2.rectangle(img, (20, 20), (130, 130), 40, -1)
    # Strong horizontal edge across the middle-right
    cv2.rectangle(img, (170, 40), (300, 90), 90, -1)
    # Flat region: untouched (lower-right) — already 220
    # Gentle noise + blur
    img = cv2.GaussianBlur(img, (3, 3), 0.7)
    rng = np.random.default_rng(0)
    img = np.clip(img + rng.normal(0, 2, img.shape), 0, 255).astype(np.uint8)
    return img


def second_moment(img: np.ndarray, sigma_d: float = 1.0, sigma_i: float = 2.0):
    """Return per-pixel components A,B,C of M and the cornerness R."""
    f = img.astype(np.float32) / 255.0
    Ix = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3)
    Iy = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3)
    # Pre-smooth gradients by sigma_d (already approximated by Sobel)
    Ix = cv2.GaussianBlur(Ix, (0, 0), sigma_d)
    Iy = cv2.GaussianBlur(Iy, (0, 0), sigma_d)
    Ixx, Iyy, Ixy = Ix * Ix, Iy * Iy, Ix * Iy
    A = cv2.GaussianBlur(Ixx, (0, 0), sigma_i)
    C = cv2.GaussianBlur(Iyy, (0, 0), sigma_i)
    B = cv2.GaussianBlur(Ixy, (0, 0), sigma_i)
    k = 0.05
    R = (A * C - B * B) - k * (A + C) ** 2
    return A, B, C, R


def harris_points(R: np.ndarray, frac: float = 0.02, nms: int = 7):
    """Threshold + 3x3 NMS."""
    thr = frac * R.max()
    mask = R > thr
    dil = cv2.dilate(R, np.ones((nms, nms), np.uint8))
    mask &= R == dil
    ys, xs = np.where(mask)
    return np.stack([xs, ys], axis=1)


def ellipse_from_M(A: float, B: float, C: float):
    """Ellipse from M = [[A,B],[B,C]] — axis lengths ∝ 1/sqrt(λ)."""
    M = np.array([[A, B], [B, C]])
    w, V = np.linalg.eigh(M)        # ascending
    w = np.clip(w, 1e-8, None)
    # Iso-contour Δᵀ M Δ = const  ⇒  semi-axes = sqrt(const) / sqrt(λ)
    semis = 1.0 / np.sqrt(w)
    # Normalise so the larger ellipse fits the panel
    return semis, V


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = build_scene()
    A, B, C, R = second_moment(img)

    # Probe locations
    probes = {
        "corner": (130, 130),       # bottom-right corner of dark square
        "edge":   (235, 40),        # top edge of right rectangle
        "flat":   (260, 200),       # flat region in lower-right
    }
    colors = {"corner": "tab:green", "edge": "tab:orange", "flat": "tab:red"}

    pts = harris_points(R, frac=0.02, nms=7)

    fig = plt.figure(figsize=(15, 5.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1.2, 1.2], wspace=0.18)

    # Panel (a): image with probes
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    for name, (x, y) in probes.items():
        ax.plot(x, y, "o", color=colors[name], markersize=10,
                markeredgecolor="white", markeredgewidth=1.5)
        ax.annotate(name, xy=(x, y), xytext=(x + 8, y - 12),
                    color=colors[name], fontsize=10, fontweight="bold")
    ax.set_title("(a) Probes: corner, edge, flat")
    ax.axis("off")

    # Panel (b): three mini-plots, one ellipse per probe (each with its own scale)
    gs_b = gs[0, 1].subgridspec(1, 3, wspace=0.05)
    for i, name in enumerate(["corner", "edge", "flat"]):
        axb = fig.add_subplot(gs_b[0, i])
        x, y = probes[name]
        Mm = np.array([[A[y, x], B[y, x]], [B[y, x], C[y, x]]])
        evs = np.linalg.eigvalsh(Mm)  # ascending: λ₂, λ₁
        semis, V = ellipse_from_M(A[y, x], B[y, x], C[y, x])
        big = float(np.max(semis))
        lim = big * 1.25
        axb.set_xlim(-lim, lim)
        axb.set_ylim(-lim, lim)
        axb.set_aspect("equal")
        axb.axhline(0, color="0.85", lw=0.6)
        axb.axvline(0, color="0.85", lw=0.6)
        ang = np.degrees(np.arctan2(V[1, 0], V[0, 0]))
        e = mpatches.Ellipse((0, 0), width=2 * semis[0], height=2 * semis[1],
                             angle=ang, fill=False,
                             edgecolor=colors[name], lw=2.5)
        axb.add_patch(e)
        axb.set_title(name, color=colors[name], fontsize=11, fontweight="bold")
        axb.text(0.5, -0.12,
                 f"λ₁={evs[1]:.3g}\nλ₂={evs[0]:.3g}",
                 transform=axb.transAxes, ha="center", va="top",
                 fontsize=9, color=colors[name])
        if i == 0:
            axb.set_ylabel("Δy")
        axb.set_xlabel("Δx")
        axb.tick_params(labelsize=7)
    fig.text(gs[0, 1].get_position(fig).x0 + 0.005,
             gs[0, 1].get_position(fig).y1 + 0.005,
             "(b) iso-contour ΔᵀM Δ = 1  (own scale per probe)",
             fontsize=11)

    # Panel (c): cornerness heatmap + detected keypoints
    ax = fig.add_subplot(gs[0, 2])
    Rshow = np.sign(R) * np.log1p(1000 * np.abs(R))
    vmax = np.abs(Rshow).max()
    im = ax.imshow(Rshow, cmap="seismic", vmin=-vmax, vmax=vmax)
    ax.imshow(img, cmap="gray", alpha=0.25)
    ax.scatter(pts[:, 0], pts[:, 1], s=40, facecolors="none",
               edgecolors="lime", linewidths=1.5, label=f"{len(pts)} keypoints")
    ax.set_title("(c) Cornerness R (signed log) + Harris keypoints")
    ax.axis("off")
    ax.legend(loc="lower right", fontsize=9)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("sign(R)·log(1+|R|·1000)")

    fig.suptitle("Harris detector: structure tensor, cornerness, and keypoints",
                 fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
