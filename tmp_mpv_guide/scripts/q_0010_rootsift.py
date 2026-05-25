# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""RootSIFT vs SIFT for q_0010.

Two-part visualisation:

  (a) The transform itself: take one SIFT descriptor, show its L1-normalised
      histogram, the element-wise √ histogram, and confirm that Euclidean
      distance after √ ≡ Hellinger distance before √.

  (b) Matching-quality comparison.  We synthesise a wide-baseline pair from
      a textured scene (the same trick as q_0001), compute SIFT and RootSIFT
      descriptors, run the Lowe ratio test, and verify via RANSAC how many
      *correct* matches each descriptor produces at multiple ratio
      thresholds.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0010_rootsift.png"


def root_sift(des: np.ndarray) -> np.ndarray:
    """L1-normalise then element-wise √."""
    eps = 1e-12
    d = des / (des.sum(axis=1, keepdims=True) + eps)
    return np.sqrt(d)


def hellinger(x: np.ndarray, y: np.ndarray) -> float:
    """For 2 L1-normalised histograms."""
    return float(np.sqrt(2 - 2 * np.sum(np.sqrt(x * y))))


# Wide-baseline synthetic scene (re-used pattern from q_0001)
def make_scene(h: int = 360, w: int = 480, seed: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w]
    img = (200 + 30 * np.sin(xx / 40.0) + 20 * np.cos(yy / 30.0)).astype(np.uint8)
    for _ in range(10):
        x0, y0 = rng.integers(0, w - 80), rng.integers(0, h - 60)
        x1, y1 = x0 + rng.integers(30, 80), y0 + rng.integers(20, 60)
        cv2.rectangle(img, (x0, y0), (x1, y1), int(rng.integers(20, 200)), -1)
    for _ in range(15):
        cv2.circle(img, (int(rng.integers(20, w - 20)), int(rng.integers(20, h - 20))),
                   int(rng.integers(6, 28)), int(rng.integers(0, 255)), -1)
    cv2.putText(img, "ROOT-SIFT", (40, 60), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, 30, 3)
    img = cv2.GaussianBlur(img, (3, 3), 0.7)
    img = np.clip(img + rng.normal(0, 3, img.shape), 0, 255).astype(np.uint8)
    return img


def warp(img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h, w = img.shape
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst = np.float32([[40, 30], [w - 30, 60], [w - 70, h - 30], [10, h - 60]])
    H = cv2.getPerspectiveTransform(src, dst)
    R = cv2.getRotationMatrix2D((w / 2, h / 2), 22, 0.82)
    H = np.vstack([R, [0, 0, 1]]) @ H
    return cv2.warpPerspective(img, H, (w, h), borderValue=240), H


def evaluate(descriptors, kp1, kp2, ratios, gt_H):
    """For each ratio threshold, run KNN + ratio + RANSAC and count inliers."""
    des1, des2 = descriptors
    bf = cv2.BFMatcher(cv2.NORM_L2)
    knn = bf.knnMatch(des1.astype(np.float32), des2.astype(np.float32), k=2)
    out = {}
    for r in ratios:
        good = [m for m, n in knn if m.distance < r * n.distance]
        if len(good) < 8:
            out[r] = (0, len(good))
            continue
        src = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
        n_in = int(mask.sum()) if mask is not None else 0
        out[r] = (n_in, len(good))
    return out


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img1 = make_scene()
    img2, gt_H = warp(img1)

    sift = cv2.SIFT_create(nfeatures=600, contrastThreshold=0.025)
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    # Standard OpenCV SIFT returns L2-normalised int8-scaled vectors; rescale
    des1 = des1.astype(np.float32)
    des2 = des2.astype(np.float32)
    rdes1 = root_sift(des1)
    rdes2 = root_sift(des2)

    ratios = [0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    res_sift = evaluate((des1, des2), kp1, kp2, ratios, gt_H)
    res_root = evaluate((rdes1, rdes2), kp1, kp2, ratios, gt_H)
    print("ratio  SIFT(inl/tent)   RootSIFT(inl/tent)")
    for r in ratios:
        a = res_sift[r]; b = res_root[r]
        print(f"  {r:.2f}   {a[0]:3d}/{a[1]:3d}        {b[0]:3d}/{b[1]:3d}")

    # ---- Figure ----
    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2], hspace=0.3, wspace=0.18)

    # (a) One SIFT vs its RootSIFT
    # Pick the strongest descriptor (largest sum)
    idx = int(np.argmax(des1.sum(axis=1)))
    d = des1[idx]
    d_l1 = d / d.sum()
    d_root = np.sqrt(d_l1)
    ax = fig.add_subplot(gs[0, 0])
    ax.bar(np.arange(128), d_l1, color="steelblue", width=1.0)
    ax.set_title("(a) Standard SIFT (L1-normalised) — heavy-tailed bins")
    ax.set_xlabel("descriptor dim (0…127)")
    ax.set_ylabel("value")
    ax.set_xlim(-1, 128)

    ax = fig.add_subplot(gs[0, 1])
    ax.bar(np.arange(128), d_root, color="tomato", width=1.0)
    ax.set_title("(b) RootSIFT = √(L1-SIFT) — flatter dynamic range")
    ax.set_xlabel("descriptor dim (0…127)")
    ax.set_ylabel("value")
    ax.set_xlim(-1, 128)

    # Sanity-check the Hellinger equivalence
    # Build a second descriptor for comparison (a slightly different one)
    idx2 = (idx + 7) % len(des1)
    e = des1[idx2]
    e_l1 = e / e.sum()
    hell = hellinger(d_l1, e_l1)
    euc_root = float(np.linalg.norm(np.sqrt(d_l1) - np.sqrt(e_l1)))
    print(f"Hellinger(SIFT₁, SIFT₂) = {hell:.5f}")
    print(f"||RootSIFT₁ − RootSIFT₂||₂ = {euc_root:.5f}  (should match Hellinger)")

    # (c) Bar plot of RANSAC inliers per ratio
    ax = fig.add_subplot(gs[1, :])
    xs = np.arange(len(ratios))
    width = 0.38
    sift_in = [res_sift[r][0] for r in ratios]
    root_in = [res_root[r][0] for r in ratios]
    ax.bar(xs - width / 2, sift_in, width=width, color="steelblue", label="SIFT")
    ax.bar(xs + width / 2, root_in, width=width, color="tomato", label="RootSIFT")
    for i, (s, r) in enumerate(zip(sift_in, root_in)):
        ax.text(i - width / 2, s + 1, str(s), ha="center", fontsize=9)
        ax.text(i + width / 2, r + 1, str(r), ha="center", fontsize=9)
    ax.set_xticks(xs)
    ax.set_xticklabels([f"{r:.2f}" for r in ratios])
    ax.set_xlabel("Lowe ratio threshold")
    ax.set_ylabel("RANSAC inlier matches")
    ax.set_title("(c) Wide-baseline match quality: RANSAC inliers vs ratio threshold")
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3, axis="y")
    # annotate the Hellinger sanity check
    ax.text(0.99, 0.95,
            f"sanity:  Hellinger(SIFTᵢ,SIFTⱼ) = {hell:.4f}\n"
            f"           ‖RootSIFTᵢ−RootSIFTⱼ‖ = {euc_root:.4f}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, family="monospace",
            bbox=dict(facecolor="white", edgecolor="0.7", boxstyle="round,pad=0.3"))

    fig.suptitle("SIFT → RootSIFT: a free upgrade via L1+√", fontsize=14, y=0.995)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
