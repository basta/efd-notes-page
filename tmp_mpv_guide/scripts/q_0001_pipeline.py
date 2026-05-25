# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""Wide-baseline matching pipeline figure for q_0001.

Generates a synthetic scene, warps it by a known homography, runs the full
SIFT-based pipeline, and saves a 4-panel figure illustrating detection,
description, matching (with outliers) and RANSAC verification.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0001_pipeline.png"
rng = np.random.default_rng(0)


def make_scene(h: int = 360, w: int = 480) -> np.ndarray:
    """Build a synthetic textured image with shapes and noise."""
    img = np.full((h, w), 235, dtype=np.uint8)
    # Background gradient
    yy, xx = np.mgrid[0:h, 0:w]
    img = (200 + 30 * np.sin(xx / 40.0) + 20 * np.cos(yy / 30.0)).astype(np.uint8)
    # Random rectangles
    for _ in range(8):
        x0, y0 = rng.integers(0, w - 80), rng.integers(0, h - 60)
        x1, y1 = x0 + rng.integers(30, 80), y0 + rng.integers(20, 60)
        color = int(rng.integers(20, 200))
        cv2.rectangle(img, (x0, y0), (x1, y1), color, -1)
    # Random circles
    for _ in range(10):
        cx, cy = rng.integers(20, w - 20), rng.integers(20, h - 20)
        r = int(rng.integers(8, 28))
        color = int(rng.integers(0, 255))
        cv2.circle(img, (cx, cy), r, color, -1)
    # Text for distinctive features
    cv2.putText(img, "WIDE BASELINE", (40, 60), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, 30, 3)
    cv2.putText(img, "scene", (180, 260), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, 80, 4)
    # A little blur + noise for realism
    img = cv2.GaussianBlur(img, (3, 3), 0.7)
    img = np.clip(img + rng.normal(0, 3, img.shape), 0, 255).astype(np.uint8)
    return img


def warp(img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Warp the image with a strong but invertible homography."""
    h, w = img.shape
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    # Aggressive perspective + scale + rotation
    dst = np.float32([[40, 30], [w - 20, 60], [w - 80, h - 30], [10, h - 60]])
    H = cv2.getPerspectiveTransform(src, dst)
    # Slight in-plane rotation about centre
    R = cv2.getRotationMatrix2D((w / 2, h / 2), 18, 0.85)
    R3 = np.vstack([R, [0, 0, 1]])
    H = R3 @ H
    warped = cv2.warpPerspective(img, H, (w, h), borderValue=240)
    return warped, H


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img1 = make_scene()
    img2, _H = warp(img1)

    sift = cv2.SIFT_create(nfeatures=400, contrastThreshold=0.03)
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # KNN matching + Lowe ratio test
    bf = cv2.BFMatcher(cv2.NORM_L2)
    knn = bf.knnMatch(des1, des2, k=2)
    tentative = [m for m, n in knn if m.distance < 0.85 * n.distance]

    # RANSAC homography verification
    src_pts = np.float32([kp1[m.queryIdx].pt for m in tentative]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in tentative]).reshape(-1, 1, 2)
    H_est, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 4.0)
    mask = mask.ravel().astype(bool)
    inliers = [m for m, ok in zip(tentative, mask) if ok]

    print(f"kp1={len(kp1)} kp2={len(kp2)} tentative={len(tentative)} "
          f"inliers={int(mask.sum())}")

    # ---- Figure ----
    fig = plt.figure(figsize=(13, 9))
    gs = fig.add_gridspec(2, 2, hspace=0.18, wspace=0.08)

    # Panel 1: Detection
    ax = fig.add_subplot(gs[0, 0])
    img1_kp = cv2.drawKeypoints(
        cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR), kp1, None,
        color=(0, 180, 255),
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
    )
    ax.imshow(cv2.cvtColor(img1_kp, cv2.COLOR_BGR2RGB))
    ax.set_title(f"1. Detection — {len(kp1)} SIFT keypoints (scale & orientation)")
    ax.axis("off")

    # Panel 2: Description (a single patch + descriptor histogram grid)
    ax = fig.add_subplot(gs[0, 1])
    # pick the strongest keypoint
    strongest = max(range(len(kp1)), key=lambda i: kp1[i].response)
    kp = kp1[strongest]
    desc = des1[strongest]
    cx, cy = int(kp.pt[0]), int(kp.pt[1])
    s = max(12, int(6 * kp.size))
    x0, y0 = max(0, cx - s), max(0, cy - s)
    x1, y1 = min(img1.shape[1], cx + s), min(img1.shape[0], cy + s)
    patch = img1[y0:y1, x0:x1]
    # Compose: patch on the left, 4x4 histogram grid on the right
    combined = np.ones((128, 128 + 12 + 128), dtype=np.uint8) * 255
    p_resized = cv2.resize(patch, (128, 128))
    combined[:, :128] = p_resized
    grid = np.ones((128, 128, 3), dtype=np.uint8) * 255
    cell = 32
    d = desc.reshape(4, 4, 8)
    d = d / (d.max() + 1e-6)
    for gy in range(4):
        for gx in range(4):
            cx_, cy_ = gx * cell + cell // 2, gy * cell + cell // 2
            hist = d[gy, gx]
            for b in range(8):
                ang = b * np.pi / 4
                L = hist[b] * (cell // 2 - 2)
                ex = int(cx_ + L * np.cos(ang))
                ey = int(cy_ - L * np.sin(ang))
                cv2.line(grid, (cx_, cy_), (ex, ey), (0, 60, 180), 1)
            cv2.rectangle(grid, (gx * cell, gy * cell),
                          ((gx + 1) * cell, (gy + 1) * cell), (200, 200, 200), 1)
    combined_rgb = cv2.cvtColor(combined, cv2.COLOR_GRAY2RGB)
    combined_rgb[:, 128 + 12:] = grid
    # Draw an arrow between them
    ax.imshow(combined_rgb)
    ax.annotate("", xy=(128 + 12, 64), xytext=(128, 64),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.text(64, 138, "normalised patch", ha="center", fontsize=9)
    ax.text(128 + 12 + 64, 138, "4×4 × 8 SIFT histogram", ha="center", fontsize=9)
    ax.set_title("2. Description — patch normalisation + gradient histograms")
    ax.axis("off")

    # Panel 3: Tentative matches
    ax = fig.add_subplot(gs[1, 0])
    tent_img = cv2.drawMatches(
        img1, kp1, img2, kp2, tentative, None,
        matchColor=(255, 150, 0), singlePointColor=(180, 180, 180),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    ax.imshow(cv2.cvtColor(tent_img, cv2.COLOR_BGR2RGB))
    ax.set_title(f"3. Matching — {len(tentative)} tentative correspondences "
                 f"(ratio test, includes outliers)")
    ax.axis("off")

    # Panel 4: Verified inliers
    ax = fig.add_subplot(gs[1, 1])
    in_img = cv2.drawMatches(
        img1, kp1, img2, kp2, inliers, None,
        matchColor=(0, 200, 0), singlePointColor=(180, 180, 180),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    ax.imshow(cv2.cvtColor(in_img, cv2.COLOR_BGR2RGB))
    ax.set_title(f"4. Geometric verification — {len(inliers)} RANSAC inliers")
    ax.axis("off")

    fig.suptitle("Wide-baseline matching pipeline", fontsize=14, y=0.995)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
