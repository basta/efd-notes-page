# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Two-stage vs single-stage detection pipelines + focal loss for q_0043."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0043_detection.png"


def box(ax, x, y, w, h, text, fc="#bfdbfe"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03",
                                fc=fc, ec="black", lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)


def arr(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.3))


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(15, 6.5))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0], hspace=0.35,
                          wspace=0.18)

    # (a) Two-stage detector (Faster R-CNN-like)
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    box(ax, 0.2, 1.5, 1.4, 1.0, "image", "#dbeafe")
    box(ax, 2.0, 1.5, 1.6, 1.0, "CNN backbone\n(feature map)", "#bbf7d0")
    box(ax, 4.0, 2.5, 1.7, 0.9, "RPN\n(objectness +\nanchor reg.)", "#fde68a")
    box(ax, 4.0, 0.6, 1.7, 0.9, "shared\nfeature map", "#bbf7d0")
    box(ax, 6.1, 1.5, 1.5, 1.0, "RoI pool\n/ RoI align", "#fecaca")
    box(ax, 7.9, 2.4, 1.9, 0.8, "softmax  (C+1 classes)", "#a7f3d0")
    box(ax, 7.9, 1.0, 1.9, 0.8, "box regressor  (4×C)", "#a7f3d0")
    arr(ax, 1.6, 2.0, 2.0, 2.0)
    arr(ax, 3.6, 2.0, 4.0, 2.9)
    arr(ax, 3.6, 2.0, 4.0, 1.0)
    arr(ax, 5.7, 2.9, 6.1, 2.1)
    arr(ax, 5.7, 1.0, 6.1, 1.9)
    arr(ax, 7.6, 2.0, 7.9, 2.8)
    arr(ax, 7.6, 2.0, 7.9, 1.4)
    ax.set_title("(a) Two-stage (Faster R-CNN): "
                 "RPN proposes, head classifies & refines", fontsize=11)

    # (b) Single-stage detector (YOLO-like)
    ax = fig.add_subplot(gs[0, 1])
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    box(ax, 0.2, 1.5, 1.4, 1.0, "image", "#dbeafe")
    box(ax, 2.0, 1.5, 2.0, 1.0, "CNN backbone\n+ detection head", "#bbf7d0")
    box(ax, 4.4, 1.5, 2.4, 1.0,
        "dense output tensor\n$S \\times S \\times (B\\cdot5 + C)$", "#fde68a")
    box(ax, 7.2, 2.4, 2.6, 0.8, "per-cell class probabilities", "#a7f3d0")
    box(ax, 7.2, 1.0, 2.6, 0.8, "per-cell box (x,y,w,h,conf)", "#a7f3d0")
    arr(ax, 1.6, 2.0, 2.0, 2.0)
    arr(ax, 4.0, 2.0, 4.4, 2.0)
    arr(ax, 6.8, 2.0, 7.2, 2.8)
    arr(ax, 6.8, 2.0, 7.2, 1.4)
    ax.set_title("(b) Single-stage (YOLO): one forward pass → "
                 "dense per-cell predictions", fontsize=11)

    # (c) IoU illustration
    ax = fig.add_subplot(gs[1, 0])
    ax.set_xlim(-1, 6); ax.set_ylim(-1, 5); ax.set_aspect("equal"); ax.axis("off")
    gt = (0.5, 0.5, 3.0, 3.0)  # x, y, w, h
    pr = (1.5, 1.0, 3.0, 3.0)
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((gt[0], gt[1]), gt[2], gt[3],
                           fill=False, ec="tab:green", lw=2.5, label="ground truth"))
    ax.add_patch(Rectangle((pr[0], pr[1]), pr[2], pr[3],
                           fill=False, ec="tab:blue", lw=2.5,
                           ls="--", label="prediction"))
    ix0, iy0 = max(gt[0], pr[0]), max(gt[1], pr[1])
    ix1, iy1 = min(gt[0] + gt[2], pr[0] + pr[2]), min(gt[1] + gt[3], pr[1] + pr[3])
    ax.add_patch(Rectangle((ix0, iy0), ix1 - ix0, iy1 - iy0,
                           fc="tab:orange", alpha=0.4, ec="black", lw=1,
                           label="intersection"))
    iw, ih = ix1 - ix0, iy1 - iy0
    inter = iw * ih
    union = gt[2] * gt[3] + pr[2] * pr[3] - inter
    iou = inter / union
    ax.text(2.5, -0.4, f"IoU = {inter:.1f} / {union:.1f} = {iou:.2f}",
            ha="center", fontsize=12)
    ax.set_title("(c) Intersection-over-Union (IoU)\nused for matching & mAP",
                 fontsize=11)
    ax.legend(loc="upper right", fontsize=9)

    # (d) Focal loss curves
    ax = fig.add_subplot(gs[1, 1])
    pt = np.linspace(0.01, 1, 200)
    ce = -np.log(pt)
    for g, col in zip([0, 0.5, 1, 2, 5],
                      ["tab:gray", "tab:purple", "tab:blue",
                       "tab:green", "tab:red"]):
        fl = -(1 - pt) ** g * np.log(pt)
        ax.plot(pt, fl, color=col, lw=2,
                label=f"$\\gamma = {g}$" + ("  (= CE)" if g == 0 else ""))
    ax.set_xlabel("$p_t$  (predicted prob. of true class)")
    ax.set_ylabel("loss")
    ax.set_title("(d) Focal loss $-(1-p_t)^\\gamma \\log p_t$\n"
                 "down-weights easy examples (large $p_t$)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    fig.suptitle("Object detection: two-stage vs single-stage architectures, "
                 "evaluated with IoU/mAP", fontsize=13, y=1.005)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
