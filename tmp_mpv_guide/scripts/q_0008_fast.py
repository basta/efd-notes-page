# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""FAST detector visualisation for q_0008.

We illustrate the segment test on a corner, an edge and a flat probe.
For each probe:

  - draw a zoom-in of the local patch with the Bresenham-3 circle of 16
    pixels overlaid, colour-coded by classification:
      red    pixel ≥ I_p + t  ("brighter")
      blue   pixel ≤ I_p − t  ("darker")
      grey   neither
  - display the longest contiguous arc length of "brighter" or "darker"
    pixels and whether it meets the FAST-N threshold.

Right panel: the test image with all OpenCV-FAST keypoints overlaid.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0008_fast.png"

# Bresenham-3 circle: 16 pixel offsets (Rosten & Drummond ordering)
BRES = np.array([
    (0, -3), (1, -3), (2, -2), (3, -1),
    (3, 0), (3, 1), (2, 2), (1, 3),
    (0, 3), (-1, 3), (-2, 2), (-3, 1),
    (-3, 0), (-3, -1), (-2, -2), (-1, -3),
], dtype=int)


def longest_arc(mask: np.ndarray) -> int:
    """Longest run of True values on the circular boolean array."""
    n = len(mask)
    if mask.all():
        return n
    if not mask.any():
        return 0
    best = cur = 0
    # Double the array to handle circular wrap
    for v in np.concatenate([mask, mask]):
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return min(best, n)


def classify(img: np.ndarray, cx: int, cy: int, t: int = 20, N: int = 9) -> dict:
    Ip = int(img[cy, cx])
    intens = [int(img[cy + dy, cx + dx]) for dx, dy in BRES]
    brighter = np.array([v > Ip + t for v in intens])
    darker = np.array([v < Ip - t for v in intens])
    arc_b = longest_arc(brighter)
    arc_d = longest_arc(darker)
    return dict(Ip=Ip, intens=intens, brighter=brighter,
                darker=darker, arc_b=arc_b, arc_d=arc_d, N=N,
                is_corner=max(arc_b, arc_d) >= N)


def make_image(h: int = 240, w: int = 360) -> np.ndarray:
    img = np.full((h, w), 220, dtype=np.uint8)
    cv2.rectangle(img, (30, 40), (140, 140), 40, -1)   # dark square (corners!)
    cv2.rectangle(img, (180, 50), (320, 100), 100, -1)  # bar (edges)
    cv2.circle(img, (240, 180), 25, 60, -1)              # disk
    img = cv2.GaussianBlur(img, (3, 3), 0.7)
    rng = np.random.default_rng(0)
    img = np.clip(img + rng.normal(0, 1.5, img.shape), 0, 255).astype(np.uint8)
    return img


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = make_image()
    probes = {
        "corner": (140, 140),  # bottom-right of dark square
        "edge":   (250, 50),   # top edge of the bar
        "flat":   (60, 200),   # flat bright area
    }

    fig = plt.figure(figsize=(15, 6))
    gs = fig.add_gridspec(2, 4, width_ratios=[1, 1, 1, 1.2],
                          hspace=0.35, wspace=0.25)

    for i, name in enumerate(["corner", "edge", "flat"]):
        cx, cy = probes[name]
        info = classify(img, cx, cy, t=20)
        # Zoom-in patch
        s = 10
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(img[cy - s:cy + s + 1, cx - s:cx + s + 1],
                  cmap="gray", vmin=0, vmax=255,
                  extent=[-s - 0.5, s + 0.5, s + 0.5, -s - 0.5])
        # Draw the 16 circle pixels
        for k, (dx, dy) in enumerate(BRES):
            if info["brighter"][k]:
                col = "red"
            elif info["darker"][k]:
                col = "blue"
            else:
                col = "0.6"
            ax.plot(dx, dy, "o", color=col, markersize=11,
                    markeredgecolor="white", markeredgewidth=1.0)
            ax.text(dx, dy, str(k + 1), fontsize=6, ha="center",
                    va="center", color="white", fontweight="bold")
        # Centre marker
        ax.plot(0, 0, "+", color="yellow", markersize=12, mew=2)
        # Bresenham guide circle
        ang = np.linspace(0, 2 * np.pi, 100)
        ax.plot(3 * np.cos(ang), 3 * np.sin(ang), "y--", lw=0.7)
        ok = "✓ corner" if info["is_corner"] else "✗ not corner"
        ax.set_title(f"{name}\nI_p={info['Ip']}  "
                     f"arc_b={info['arc_b']}  arc_d={info['arc_d']}\n"
                     f"(N={info['N']})  {ok}",
                     fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])

    # Bar plot showing the per-pixel intensity profile around the circle
    ax_b = fig.add_subplot(gs[1, :3])
    width = 0.27
    xs = np.arange(16) + 1
    for j, (name, col) in enumerate(zip(["corner", "edge", "flat"],
                                         ["tab:green", "tab:orange", "tab:red"])):
        cx, cy = probes[name]
        info = classify(img, cx, cy, t=20)
        ax_b.bar(xs + (j - 1) * width,
                 [v - info["Ip"] for v in info["intens"]],
                 width=width, color=col, label=name)
        # Threshold bands per probe — drawn once on top
    info_c = classify(img, *probes["corner"], t=20)
    ax_b.axhline(20, color="0.3", ls="--", lw=1, label="±t (t = 20)")
    ax_b.axhline(-20, color="0.3", ls="--", lw=1)
    ax_b.axhline(0, color="black", lw=0.7)
    ax_b.set_xlabel("circle index 1…16")
    ax_b.set_ylabel("I_x − I_p")
    ax_b.set_xticks(xs)
    ax_b.set_title("Intensity difference of each circle pixel relative to I_p")
    ax_b.grid(alpha=0.3, axis="y")
    ax_b.legend(fontsize=9, loc="upper right")

    # FAST detections on the whole image
    ax_d = fig.add_subplot(gs[:, 3])
    fast = cv2.FastFeatureDetector_create(threshold=25, nonmaxSuppression=True)
    kps = fast.detect(img, None)
    img_kp = cv2.drawKeypoints(
        cv2.cvtColor(img, cv2.COLOR_GRAY2BGR), kps, None, color=(0, 200, 0),
    )
    ax_d.imshow(cv2.cvtColor(img_kp, cv2.COLOR_BGR2RGB))
    for name, (px, py) in probes.items():
        ax_d.plot(px, py, "o", markersize=12,
                  markerfacecolor="none", markeredgecolor="cyan",
                  markeredgewidth=2)
        ax_d.annotate(name, (px, py), xytext=(8, -8),
                      textcoords="offset points",
                      color="cyan", fontsize=10, fontweight="bold")
    ax_d.set_title(f"FAST keypoints (t=25, NMS).  count = {len(kps)}")
    ax_d.axis("off")

    fig.suptitle("FAST detector: 16-pixel Bresenham circle segment test",
                 fontsize=14, y=0.99)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")
    for n in ["corner", "edge", "flat"]:
        info = classify(img, *probes[n], t=20)
        print(f"  {n:6s} Ip={info['Ip']:3d}  arc_b={info['arc_b']:2d}  "
              f"arc_d={info['arc_d']:2d}  → corner={info['is_corner']}")


if __name__ == "__main__":
    main()
