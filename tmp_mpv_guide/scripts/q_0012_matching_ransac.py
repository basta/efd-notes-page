# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""Descriptor matching + RANSAC visualisation for q_0012.

Builds a wide-baseline pair, computes SIFT correspondences, and shows:

  (a) histogram of d₁/d₂ ratios for every NN match, with the τ = 0.8 line
      and the distribution split into "true matches" (inliers under the
      ground-truth homography) and "false matches" (outliers).  This is the
      classical Lowe-ratio diagnostic.

  (b) inlier count vs RANSAC iteration for a hand-rolled homography
      RANSAC, plus the theoretical 95%-confidence horizon

      k* = log(1−η) / log(1 − ε^m)

      drawn as a vertical line.

  (c) the matched pair with inliers (green) and rejected outliers (red).
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0012_matching_ransac.png"


def make_scene(h: int = 360, w: int = 480, seed: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w]
    img = (200 + 30 * np.sin(xx / 40.0) + 20 * np.cos(yy / 30.0)).astype(np.uint8)
    for _ in range(10):
        x0, y0 = rng.integers(0, w - 80), rng.integers(0, h - 60)
        cv2.rectangle(img,
                      (int(x0), int(y0)),
                      (int(x0 + rng.integers(30, 80)), int(y0 + rng.integers(20, 60))),
                      int(rng.integers(20, 200)), -1)
    for _ in range(15):
        cv2.circle(img, (int(rng.integers(20, w - 20)), int(rng.integers(20, h - 20))),
                   int(rng.integers(6, 28)), int(rng.integers(0, 255)), -1)
    cv2.putText(img, "MATCHING", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 30, 3)
    img = cv2.GaussianBlur(img, (3, 3), 0.7)
    img = np.clip(img + rng.normal(0, 3, img.shape), 0, 255).astype(np.uint8)
    return img


def warp(img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h, w = img.shape
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst = np.float32([[40, 30], [w - 30, 60], [w - 70, h - 30], [10, h - 60]])
    H = cv2.getPerspectiveTransform(src, dst)
    R = cv2.getRotationMatrix2D((w / 2, h / 2), 22, 0.85)
    H = np.vstack([R, [0, 0, 1]]) @ H
    return cv2.warpPerspective(img, H, (w, h), borderValue=240), H


def transfer_error(H: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    """Symmetric transfer error |H·p1 − p2|."""
    P1 = np.hstack([p1, np.ones((len(p1), 1))])
    Pp = (H @ P1.T).T
    Pp = Pp[:, :2] / (Pp[:, 2:] + 1e-12)
    return np.linalg.norm(Pp - p2, axis=1)


def ransac_homography(src: np.ndarray, dst: np.ndarray, thresh: float = 4.0,
                      max_iter: int = 800, eta: float = 0.99):
    n = len(src)
    best_inl = np.zeros(n, dtype=bool)
    best_count = 0
    best_H = None
    rng = np.random.default_rng(42)
    history = []
    for it in range(max_iter):
        idx = rng.choice(n, size=4, replace=False)
        try:
            H = cv2.getPerspectiveTransform(src[idx].astype(np.float32),
                                            dst[idx].astype(np.float32))
        except cv2.error:
            history.append(best_count)
            continue
        err = transfer_error(H, src, dst)
        inl = err < thresh
        c = int(inl.sum())
        if c > best_count:
            best_count = c
            best_inl = inl
            best_H = H
        history.append(best_count)
    return best_H, best_inl, np.array(history)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img1 = make_scene()
    img2, gt_H = warp(img1)

    sift = cv2.SIFT_create(nfeatures=600, contrastThreshold=0.025)
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # KNN matches (k=2) for the ratio test
    bf = cv2.BFMatcher(cv2.NORM_L2)
    knn = bf.knnMatch(des1.astype(np.float32), des2.astype(np.float32), k=2)
    ratios = np.array([m.distance / max(n.distance, 1e-6) for m, n in knn])
    pts1 = np.array([kp1[m.queryIdx].pt for m, _ in knn])
    pts2 = np.array([kp2[m.trainIdx].pt for m, _ in knn])

    # Ground-truth inliers under gt_H, used to colour the ratio histogram
    err = transfer_error(gt_H, pts1, pts2)
    is_true = err < 3.0

    # All matches (no ratio filter) -- already too noisy for RANSAC.
    # Apply ratio=0.85 to get a noisy set:
    keep = ratios < 0.85
    src_pts = pts1[keep]
    dst_pts = pts2[keep]
    # Run our RANSAC
    best_H, inl_mask, history = ransac_homography(src_pts, dst_pts,
                                                   thresh=4.0, max_iter=800)
    eps = inl_mask.mean()
    eta = 0.99
    m = 4
    k_theory = int(np.ceil(np.log(1 - eta) / np.log(1 - eps ** m)))
    print(f"matches kept by ratio<0.85: {len(src_pts)}  "
          f"RANSAC inliers: {int(inl_mask.sum())}  "
          f"ε={eps:.3f}  k*={k_theory}")

    # ---- Figure ----
    fig = plt.figure(figsize=(15, 9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.1], hspace=0.32, wspace=0.18)

    # (a) ratio histogram
    ax = fig.add_subplot(gs[0, 0])
    bins = np.linspace(0, 1, 40)
    ax.hist(ratios[is_true], bins=bins, color="tab:green", alpha=0.7,
            label=f"true (gt-consistent)  n={int(is_true.sum())}")
    ax.hist(ratios[~is_true], bins=bins, color="tab:red", alpha=0.7,
            label=f"false  n={int((~is_true).sum())}")
    ax.axvline(0.8, color="black", ls="--", lw=1.5, label="τ = 0.8")
    ax.set_xlabel("Lowe ratio  d₁ / d₂")
    ax.set_ylabel("count")
    ax.set_title("(a) Lowe-ratio distribution: true vs false matches")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, axis="y")

    # (b) RANSAC inlier history
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(np.arange(1, len(history) + 1), history,
            color="tab:blue", lw=1.8)
    ax.axhline(int(inl_mask.sum()), color="tab:green", ls="--",
               label=f"final inliers = {int(inl_mask.sum())}")
    ax.axvline(k_theory, color="tab:orange", ls=":", lw=2,
               label=f"k* (99%, ε={eps:.2f}) = {k_theory}")
    ax.set_xlabel("RANSAC iteration")
    ax.set_ylabel("best inlier count")
    ax.set_title("(b) RANSAC convergence: best-so-far inlier count")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    # (c) matches visualisation
    ax = fig.add_subplot(gs[1, :])
    canvas = np.concatenate([cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR),
                             cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)], axis=1)
    offset = img1.shape[1]
    # Draw outliers (red) first, then inliers (green) on top
    for (p1, p2), ok in zip(zip(src_pts, dst_pts), inl_mask):
        col = (0, 200, 0) if ok else (40, 40, 230)
        cv2.line(canvas,
                 (int(p1[0]), int(p1[1])),
                 (int(p2[0]) + offset, int(p2[1])),
                 col, 1)
        cv2.circle(canvas, (int(p1[0]), int(p1[1])), 2, col, -1)
        cv2.circle(canvas, (int(p2[0]) + offset, int(p2[1])), 2, col, -1)
    ax.imshow(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
    ax.set_title(f"(c) Putative matches: green = RANSAC inliers ({int(inl_mask.sum())}), "
                 f"red = outliers ({int((~inl_mask).sum())})")
    ax.axis("off")

    fig.suptitle("Descriptor matching, ratio test, and RANSAC verification",
                 fontsize=14, y=0.995)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
