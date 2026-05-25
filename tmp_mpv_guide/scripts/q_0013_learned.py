# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""Conceptual visualisations for learned detectors (q_0013).

We illustrate two ideas WITHOUT requiring PyTorch or pretrained networks:

  (A) Homographic adaptation (SuperPoint training-label generation):
      take an unlabelled image, apply many random homographies, detect
      keypoints in each warped view with a classical base detector (FAST
      = our stand-in for MagicPoint), warp the detections back to the
      original image, and accumulate a heatmap.  Local maxima of the
      heatmap are the pseudo-ground-truth keypoints.

  (B) R2D2's repeatability × reliability:  on a synthetic image with both
      a unique landmark (text) and a repetitive grid (low descriptor
      reliability), we plot a (handcrafted) repeatability map, a
      reliability map, and their product.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0013_learned.png"


# ----------------- A. Homographic adaptation ----------------------------
def make_scene_A(h: int = 280, w: int = 420) -> np.ndarray:
    img = np.full((h, w), 230, dtype=np.uint8)
    cv2.rectangle(img, (40, 40), (180, 160), 50, -1)
    cv2.rectangle(img, (220, 60), (380, 140), 110, -1)
    cv2.circle(img, (90, 220), 30, 70, -1)
    cv2.line(img, (260, 180), (380, 240), 30, 4)
    cv2.putText(img, "S P", (40, 240), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, 20, 3)
    img = cv2.GaussianBlur(img, (3, 3), 0.7)
    return img


def random_homography(h: int, w: int, rng: np.random.Generator,
                      strength: float = 0.18) -> np.ndarray:
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    pert = rng.uniform(-strength, strength, size=(4, 2))
    dst = src.copy()
    dst[:, 0] += pert[:, 0] * w
    dst[:, 1] += pert[:, 1] * h
    return cv2.getPerspectiveTransform(src, dst.astype(np.float32))


def homographic_adaptation(img: np.ndarray, n_warps: int = 40,
                            t_fast: int = 30) -> tuple[np.ndarray, list[tuple], list[np.ndarray]]:
    """Apply n_warps random homographies, run FAST on each warp, warp
    detections back, and aggregate into a heatmap."""
    h, w = img.shape
    rng = np.random.default_rng(0)
    fast = cv2.FastFeatureDetector_create(threshold=t_fast,
                                          nonmaxSuppression=True)
    heat = np.zeros((h, w), dtype=np.float32)
    sample_warps = []
    sample_pts = []
    for i in range(n_warps):
        H = random_homography(h, w, rng)
        warped = cv2.warpPerspective(img, H, (w, h), borderValue=240)
        kps = fast.detect(warped, None)
        if not kps:
            continue
        pts_w = np.array([k.pt for k in kps], dtype=np.float32).reshape(-1, 1, 2)
        Hinv = np.linalg.inv(H)
        pts_o = cv2.perspectiveTransform(pts_w, Hinv).reshape(-1, 2)
        # Accumulate (with a small Gaussian splat per point)
        for x, y in pts_o:
            xi, yi = int(round(x)), int(round(y))
            if 0 <= xi < w and 0 <= yi < h:
                heat[yi, xi] += 1
        if i < 4:
            sample_warps.append(warped)
            sample_pts.append(pts_o)
    heat_smooth = cv2.GaussianBlur(heat, (0, 0), 2.5)
    return heat_smooth, sample_warps, sample_pts


def nms_peaks(heat: np.ndarray, radius: int = 5, k: int = 40):
    """Return the top-k local maxima of `heat`."""
    dil = cv2.dilate(heat, np.ones((radius, radius), np.uint8))
    mask = (heat == dil) & (heat > 0.05 * heat.max())
    ys, xs = np.where(mask)
    vals = heat[ys, xs]
    order = np.argsort(-vals)[:k]
    return np.stack([xs[order], ys[order]], axis=1)


# ----------------- B. R2D2's R·D --------------------------------------
def make_scene_B(h: int = 280, w: int = 420) -> np.ndarray:
    img = np.full((h, w), 230, dtype=np.uint8)
    # Repetitive grid in left half (high repeatability but low reliability!)
    for x in range(20, 200, 22):
        for y in range(30, 250, 22):
            cv2.rectangle(img, (x, y), (x + 12, y + 12), 60, -1)
    # Unique landmark in right half: text
    cv2.putText(img, "R2D2", (230, 110), cv2.FONT_HERSHEY_SIMPLEX,
                1.6, 30, 4)
    cv2.rectangle(img, (230, 140), (390, 240), 110, 2)
    cv2.circle(img, (310, 190), 22, 60, -1)
    img = cv2.GaussianBlur(img, (3, 3), 0.7)
    return img


def repeatability_map(img: np.ndarray) -> np.ndarray:
    """Hand-crafted proxy: high where image has strong local gradient."""
    f = img.astype(np.float32) / 255.0
    Lx = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3)
    Ly = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3)
    g = np.sqrt(Lx ** 2 + Ly ** 2)
    g = cv2.GaussianBlur(g, (0, 0), 2.0)
    return g / (g.max() + 1e-9)


def reliability_map(img: np.ndarray) -> np.ndarray:
    """Hand-crafted proxy: minimum local L2 distance to a shifted copy of
    the image over a dense range of shifts.  Repetitive regions find a
    shift that matches their content (small min ⇒ low reliability); a
    unique landmark cannot be matched by any nearby shift (large min ⇒
    high reliability).  We sample shifts at unit step in [−32, 32].
    """
    f = cv2.GaussianBlur(img.astype(np.float32), (0, 0), 1.2)
    win_sigma = 5.0
    best = np.full_like(f, 1e12)
    # Wide and dense shift grid so the grid period is sure to be hit
    for dx in range(-30, 31, 2):
        for dy in range(-30, 31, 2):
            if abs(dx) + abs(dy) < 8:
                continue
            shifted = np.roll(np.roll(f, dy, axis=0), dx, axis=1)
            diff = (f - shifted) ** 2
            diff = cv2.GaussianBlur(diff, (0, 0), win_sigma)
            best = np.minimum(best, diff)
    rel = best / (best.max() + 1e-9)
    # Zero out very flat regions (no gradient → undefined uniqueness)
    grad = repeatability_map(img)
    rel = rel * (grad > 0.05).astype(np.float32)
    rel = cv2.GaussianBlur(rel, (0, 0), 2.0)
    rel = rel / (rel.max() + 1e-9)
    return rel


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # ----- A. Homographic adaptation -----
    img_A = make_scene_A()
    heat, sample_warps, sample_pts = homographic_adaptation(img_A, n_warps=40)
    pseudo_kps = nms_peaks(heat, radius=7, k=40)

    # ----- B. R · D -----
    img_B = make_scene_B()
    R = repeatability_map(img_B)
    D = reliability_map(img_B)
    S = R * D
    # Pick top-k from S and from R alone — show the difference
    k = 30
    pts_RonlyR = nms_peaks(R, radius=8, k=k)
    pts_RD = nms_peaks(S, radius=8, k=k)

    # ---- Figure ----
    fig = plt.figure(figsize=(15, 9.5))
    gs = fig.add_gridspec(2, 4, hspace=0.32, wspace=0.15,
                          height_ratios=[1, 1])

    # Top row: SuperPoint homographic adaptation
    fig.text(0.04, 0.93,
             "(A) SuperPoint-style homographic adaptation",
             fontsize=13, fontweight="bold")
    # show 3 sample warps with detections
    for i in range(3):
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(sample_warps[i], cmap="gray")
        ax.plot(sample_pts[i][:, 0], sample_pts[i][:, 1], "o",
                color="tab:orange", markersize=3)
        ax.set_title(f"warped view {i + 1}\n({len(sample_pts[i])} FAST kps)",
                     fontsize=10)
        ax.axis("off")

    # 4th panel: aggregated heatmap on original image + pseudo-GT
    ax = fig.add_subplot(gs[0, 3])
    ax.imshow(img_A, cmap="gray")
    ax.imshow(heat, cmap="hot", alpha=0.55)
    ax.plot(pseudo_kps[:, 0], pseudo_kps[:, 1], "o",
            markerfacecolor="none", markeredgecolor="lime",
            markeredgewidth=1.6, markersize=8)
    ax.set_title(f"aggregated heatmap on original\n"
                 f"→ {len(pseudo_kps)} pseudo-GT keypoints",
                 fontsize=10)
    ax.axis("off")

    # Bottom row: R · D
    fig.text(0.04, 0.46,
             "(B) R2D2: separate repeatability (R) and reliability (D)",
             fontsize=13, fontweight="bold")
    ax = fig.add_subplot(gs[1, 0])
    ax.imshow(img_B, cmap="gray")
    ax.imshow(R, cmap="viridis", alpha=0.55)
    ax.set_title("R — repeatability\n(high on any strong edge/corner)",
                 fontsize=10)
    ax.axis("off")

    ax = fig.add_subplot(gs[1, 1])
    ax.imshow(img_B, cmap="gray")
    ax.imshow(D, cmap="viridis", alpha=0.55)
    ax.set_title("D — reliability\n(low where patches repeat nearby)",
                 fontsize=10)
    ax.axis("off")

    ax = fig.add_subplot(gs[1, 2])
    ax.imshow(img_B, cmap="gray")
    ax.imshow(S, cmap="viridis", alpha=0.55)
    ax.set_title("S = R · D\n(used for keypoint selection)",
                 fontsize=10)
    ax.axis("off")

    ax = fig.add_subplot(gs[1, 3])
    ax.imshow(img_B, cmap="gray")
    ax.plot(pts_RonlyR[:, 0], pts_RonlyR[:, 1], "o",
            markerfacecolor="none", markeredgecolor="tomato",
            markeredgewidth=1.5, markersize=8, label="top-k from R only")
    ax.plot(pts_RD[:, 0], pts_RD[:, 1], "x",
            color="lime", markersize=8, mew=2, label="top-k from R·D")
    ax.set_title("kp selection: R-only floods the repetitive\n"
                 "grid; R·D picks unique landmarks",
                 fontsize=10)
    ax.axis("off")
    ax.legend(fontsize=8, loc="upper right",
              facecolor="white", framealpha=0.85)

    fig.suptitle("Loss-driven label generation for learned detectors",
                 fontsize=14, y=0.995)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")
    print(f"pseudo-GT kps from {40} warps: {len(pseudo_kps)}")
    print(f"R-only top-k centred on grid: "
          f"{int((pts_RonlyR[:, 0] < 220).sum())}/{k};  "
          f"R·D top-k on grid: "
          f"{int((pts_RD[:, 0] < 220).sum())}/{k}")


if __name__ == "__main__":
    main()
