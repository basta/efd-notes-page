# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""MSER visualisation for q_0007.

Three-panel figure:

  (a) input image at four different thresholds, showing the upper-level
      sets as binary masks.  A region with a clear intensity plateau (a
      "blob") is highlighted to follow across thresholds.
  (b) area A(t) of two example regions vs threshold t — one MSER (flat
      plateau ⇒ A is nearly constant ⇒ stability is a local minimum) and
      one non-MSER (A drops rapidly).
  (c) MSERs detected by OpenCV, each approximated by its moment ellipse.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0007_mser.png"


def make_image(h: int = 280, w: int = 380) -> np.ndarray:
    """Bright background with: a bright disk (very stable MSER), a sloped
    intensity bump (poor stability), and an oriented bright ellipse."""
    img = np.full((h, w), 30, dtype=np.uint8)
    # A flat bright disk (very stable)
    cv2.circle(img, (90, 140), 35, 220, -1)
    # A faded bump created by Gaussian smoothing of a small disk
    bump = np.zeros((h, w), dtype=np.float32)
    cv2.circle(bump, (220, 80), 14, 200, -1)
    bump = cv2.GaussianBlur(bump, (0, 0), 18.0)
    img = np.maximum(img.astype(np.float32), bump).astype(np.uint8)
    # An oriented bright ellipse (also reasonably stable)
    cv2.ellipse(img, (290, 200), (45, 18), 35, 0, 360, 230, -1)
    # Light noise
    rng = np.random.default_rng(0)
    img = np.clip(img + rng.normal(0, 2.0, img.shape), 0, 255).astype(np.uint8)
    return img


def trace_region(mask_t: np.ndarray, point: tuple[int, int]) -> np.ndarray:
    """Return the binary connected component of `mask_t` that contains `point`,
    or an empty mask if the point is not in `mask_t`."""
    h, w = mask_t.shape
    if mask_t[point[1], point[0]] == 0:
        return np.zeros_like(mask_t)
    n_lab, labels = cv2.connectedComponents(mask_t.astype(np.uint8))
    lab = labels[point[1], point[0]]
    return (labels == lab).astype(np.uint8)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = make_image()

    # Seed points: flat disk and the bump
    seed_disk = (90, 140)
    seed_bump = (220, 80)

    # Sweep thresholds for the bright-on-dark direction
    ts = np.arange(40, 230, 4)
    A_disk, A_bump = [], []
    for t in ts:
        mt = (img >= t).astype(np.uint8)
        A_disk.append(int(trace_region(mt, seed_disk).sum()))
        A_bump.append(int(trace_region(mt, seed_bump).sum()))
    A_disk = np.array(A_disk, dtype=float)
    A_bump = np.array(A_bump, dtype=float)

    # MSER detection via OpenCV
    mser = cv2.MSER_create(delta=4, min_area=80, max_area=5000)
    regions, _ = mser.detectRegions(img)
    # Bright-on-dark ⇒ also run on inverted to be safe (here disk is bright)
    # OpenCV detects both ER+/- already; we just use what it returns.
    # Convert each region to a moment ellipse
    ellipses = []
    for pts in regions:
        if len(pts) < 30:
            continue
        m = cv2.moments(np.array(pts).reshape(-1, 1, 2).astype(np.float32))
        if m["m00"] == 0:
            continue
        cx = m["m10"] / m["m00"]
        cy = m["m01"] / m["m00"]
        mu20 = m["mu20"] / m["m00"]
        mu02 = m["mu02"] / m["m00"]
        mu11 = m["mu11"] / m["m00"]
        cov = np.array([[mu20, mu11], [mu11, mu02]])
        wcov, Vcov = np.linalg.eigh(cov)
        wcov = np.clip(wcov, 1e-6, None)
        semi = 2.0 * np.sqrt(wcov)  # 2σ ellipse
        ang = np.degrees(np.arctan2(Vcov[1, 1], Vcov[0, 1]))
        ellipses.append(((cx, cy), (2 * semi[1], 2 * semi[0]), ang))
    # Deduplicate: keep ellipses whose centres are >5 px apart
    dedup = []
    for c, s, a in ellipses:
        if all(np.hypot(c[0] - cc[0], c[1] - cc[1]) > 6 for cc, _, _ in dedup):
            dedup.append((c, s, a))
    ellipses = dedup
    print(f"MSER regions: {len(regions)}, deduped ellipses: {len(ellipses)}")

    # ---- Figure ----
    fig = plt.figure(figsize=(15, 9))
    gs = fig.add_gridspec(2, 4, height_ratios=[1, 1.2], hspace=0.22)

    # (a) four thresholded level sets
    show_ts = [80, 130, 180, 215]
    for i, t in enumerate(show_ts):
        ax = fig.add_subplot(gs[0, i])
        mask = (img >= t).astype(np.uint8) * 255
        overlay = np.stack([img] * 3, axis=-1)
        red = np.array([220, 60, 60], dtype=np.uint8)
        overlay[mask > 0] = (0.55 * overlay[mask > 0] + 0.45 * red).astype(np.uint8)
        ax.imshow(overlay)
        ax.set_title(f"t = {t}", fontsize=11)
        ax.axis("off")
    fig.text(0.5, 0.93, "(a) Upper-level sets  Sₜ⁺ = {x : I(x) ≥ t}  for four thresholds",
             ha="center", fontsize=12)

    # (b) area curve + (c) MSER ellipses
    ax_b = fig.add_subplot(gs[1, :2])
    ax_b.plot(ts, A_disk, "o-", color="tab:blue", lw=2,
              label=f"flat disk seed {seed_disk}")
    ax_b.plot(ts, A_bump, "s-", color="tab:orange", lw=2,
              label=f"Gaussian bump seed {seed_bump}")
    ax_b.set_xlabel("threshold t")
    ax_b.set_ylabel("|R(t)|  (area in pixels)")
    ax_b.set_title("(b) A(t): the flat disk has a long plateau ⇒ MSER; "
                   "the bump shrinks smoothly ⇒ not stable")
    ax_b.grid(alpha=0.3)
    ax_b.legend(fontsize=10)

    ax_c = fig.add_subplot(gs[1, 2:])
    ax_c.imshow(img, cmap="gray")
    for c, sz, ang in ellipses:
        e = mpatches.Ellipse(c, width=sz[0], height=sz[1], angle=ang,
                             fill=False, edgecolor="yellow", lw=1.5)
        ax_c.add_patch(e)
    ax_c.set_title(f"(c) Detected MSERs (moment ellipses, 2σ).  count = {len(ellipses)}")
    ax_c.axis("off")

    fig.suptitle("Maximally Stable Extremal Regions (MSER)",
                 fontsize=14, y=0.995)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
