# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""Orientation assignment visualisation for q_0005.

Pipeline:
  1. Take a textured patch with a clear dominant direction.
  2. Compute gradients, weight by a Gaussian (σ = 1.5·σ_keypoint).
  3. Build a 36-bin orientation histogram.
  4. Smooth + parabolic peak refinement.
  5. Rotate the patch by -θ̂ to a canonical orientation.

Figure: 4 panels — original patch with gradient quiver, Gaussian weight,
the orientation histogram (polar + linear with peaks), and the canonically
rotated patch.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0005_orientation.png"


def make_patch(N: int = 80) -> np.ndarray:
    """A patch with a single dominant gradient direction (≈ 35°).

    We use a smoothed step edge whose normal is at 35°, so gradients
    point consistently in one direction (no 180°-flip ambiguity).
    """
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32) - N / 2
    theta = np.deg2rad(35.0)
    # Signed distance along the gradient direction
    d = xx * np.cos(theta) + yy * np.sin(theta)
    # Sigmoid step (bright on one side, dark on the other)
    patch = 30 + 200 / (1 + np.exp(-d / 3.0))
    # Add a weaker secondary edge for visual realism
    theta2 = np.deg2rad(35.0 + 60)
    d2 = xx * np.cos(theta2) + yy * np.sin(theta2)
    patch += 20 / (1 + np.exp(-d2 / 4.0)) - 10
    rng = np.random.default_rng(0)
    patch = patch + rng.normal(0, 2.5, patch.shape)
    return np.clip(patch, 0, 255).astype(np.uint8)


def gradients(patch: np.ndarray, sigma_smooth: float = 1.0):
    L = cv2.GaussianBlur(patch.astype(np.float32), (0, 0), sigma_smooth)
    Lx = cv2.Sobel(L, cv2.CV_32F, 1, 0, ksize=3)
    Ly = cv2.Sobel(L, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(Lx * Lx + Ly * Ly)
    ang = (np.arctan2(Ly, Lx) + 2 * np.pi) % (2 * np.pi)  # in [0, 2π)
    return Lx, Ly, mag, ang


def orientation_histogram(mag: np.ndarray, ang: np.ndarray,
                          sigma_window: float, n_bins: int = 36):
    h, w = mag.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) - h / 2
    g = np.exp(-(xx ** 2 + yy ** 2) / (2 * sigma_window ** 2))
    g[xx ** 2 + yy ** 2 > (3 * sigma_window) ** 2] = 0
    weighted = mag * g
    # Bilinear contribution to the two nearest bins
    bin_w = 2 * np.pi / n_bins
    f_idx = ang / bin_w
    lo = np.floor(f_idx).astype(int) % n_bins
    hi = (lo + 1) % n_bins
    frac = f_idx - np.floor(f_idx)
    hist = np.zeros(n_bins, dtype=np.float64)
    np.add.at(hist, lo.ravel(), ((1 - frac) * weighted).ravel())
    np.add.at(hist, hi.ravel(), (frac * weighted).ravel())
    # Smooth the histogram (3-tap moving average, circular)
    kernel = np.array([1, 1, 1]) / 3.0
    hist_s = np.zeros_like(hist)
    for k, c in enumerate(kernel):
        hist_s += c * np.roll(hist, k - 1)
    return hist_s, g


def find_peaks(hist: np.ndarray, frac: float = 0.8):
    """Return (bin_center_rad, height) for the dominant peak plus any
    other peak at least `frac` of the dominant magnitude."""
    n = len(hist)
    bin_w = 2 * np.pi / n
    max_h = hist.max()
    peaks = []
    for i in range(n):
        if hist[i] >= hist[(i - 1) % n] and hist[i] >= hist[(i + 1) % n] \
                and hist[i] >= frac * max_h:
            # Parabolic refinement
            a, b, c = hist[(i - 1) % n], hist[i], hist[(i + 1) % n]
            denom = (a - 2 * b + c)
            offset = 0.5 * (a - c) / denom if abs(denom) > 1e-12 else 0.0
            theta = (i + offset) * bin_w
            peaks.append((theta % (2 * np.pi), float(b)))
    # Sort by height
    peaks.sort(key=lambda t: -t[1])
    return peaks


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    N = 80
    patch = make_patch(N)
    sigma_kp = 4.0          # nominal keypoint scale
    sigma_w = 1.5 * sigma_kp
    Lx, Ly, mag, ang = gradients(patch)
    hist, gauss_w = orientation_histogram(mag, ang, sigma_w)
    peaks = find_peaks(hist, frac=0.8)
    theta_hat = peaks[0][0]
    print(f"true 35° vs detected {np.rad2deg(theta_hat):.2f}°, "
          f"#peaks = {len(peaks)}")

    # Rotate the patch to canonical orientation
    M = cv2.getRotationMatrix2D((N / 2, N / 2),
                                np.rad2deg(theta_hat), 1.0)
    rotated = cv2.warpAffine(patch, M, (N, N),
                             borderValue=int(patch.mean()))

    # ---- Figure ----
    fig = plt.figure(figsize=(15, 4.2))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1.4, 1], wspace=0.25)

    # (a) patch + gradient quiver + Gaussian weight circle
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(patch, cmap="gray")
    step = 5
    yy, xx = np.mgrid[0:N:step, 0:N:step]
    sub_mag = mag[::step, ::step]
    scale = 1.5 / max(sub_mag.max(), 1e-6)
    ax.quiver(xx, yy,
              Lx[::step, ::step] * scale, -Ly[::step, ::step] * scale,
              color="tab:orange", scale=1, scale_units="xy", width=0.005)
    ang_circle = np.linspace(0, 2 * np.pi, 100)
    ax.plot(N / 2 + sigma_w * np.cos(ang_circle),
            N / 2 + sigma_w * np.sin(ang_circle),
            color="cyan", ls="--", lw=1.2)
    ax.set_title("(a) Patch + gradients\n(dashed: σ_w=1.5σ window)")
    ax.axis("off")

    # (b) Gaussian weight × magnitude
    ax = fig.add_subplot(gs[0, 1])
    ax.imshow(mag * gauss_w, cmap="magma")
    ax.set_title("(b) Weighted gradient magnitude\n(Gaussian-windowed |∇L|)")
    ax.axis("off")

    # (c) Orientation histogram (polar)
    ax = fig.add_subplot(gs[0, 2], projection="polar")
    n_bins = len(hist)
    centers = (np.arange(n_bins) + 0.5) * 2 * np.pi / n_bins
    width = 2 * np.pi / n_bins
    ax.bar(centers, hist, width=width * 0.9,
           color="steelblue", edgecolor="white", linewidth=0.5)
    # mark peaks
    for theta, h in peaks:
        ax.plot([theta, theta], [0, h * 1.05],
                color="red", lw=2)
        ax.annotate(f"{np.rad2deg(theta):.1f}°",
                    xy=(theta, h), xytext=(theta, h * 1.18),
                    color="red", ha="center", fontsize=9, fontweight="bold")
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    ax.set_yticklabels([])
    ax.set_title(f"(c) Orientation histogram (36 bins)\n"
                 f"dominant peak at {np.rad2deg(theta_hat):.1f}°", pad=20)

    # (d) Rotated patch
    ax = fig.add_subplot(gs[0, 3])
    ax.imshow(rotated, cmap="gray")
    ax.set_title("(d) Patch rotated by −θ̂\n(canonical orientation)")
    ax.axis("off")

    fig.suptitle("Orientation estimation by gradient-histogram (SIFT-style)",
                 fontsize=13)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
