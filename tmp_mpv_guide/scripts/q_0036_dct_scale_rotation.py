# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""DCT tracker scale/rotation extensions: scale pyramid + multi-rotation."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0036_dct_scale_rotation.png"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(15, 5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.1, 1.1, 1.0], wspace=0.3)

    # (a) Scale pyramid
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    scales = np.linspace(0.7, 1.4, 7)
    for i, s in enumerate(scales):
        w = 0.8 * s
        x = 1.0 + i * 1.15
        y = 3.0 - w / 2
        col = "tab:red" if abs(s - 1.0) < 1e-3 else "tab:blue"
        ax.add_patch(Rectangle((x, y), w, w, fill=False, ec=col,
                               lw=2.2 if abs(s - 1.0) < 1e-3 else 1.0))
        ax.text(x + w / 2, y - 0.35, f"$s={s:.2f}$",
                ha="center", fontsize=9)
    # Response curve over scales
    resp = np.exp(-((scales - 1.05) ** 2) / 0.04)
    ax2 = ax.inset_axes([0.07, 0.66, 0.86, 0.27])
    ax2.plot(scales, resp, "o-", color="tab:purple", lw=2)
    pi = resp.argmax()
    ax2.plot(scales[pi], resp[pi], "*", color="tab:red", markersize=14)
    ax2.set_xlabel("scale", fontsize=8); ax2.set_ylabel("response", fontsize=8)
    ax2.tick_params(labelsize=8)
    ax2.set_title("DSST 1-D scale filter peak", fontsize=9)
    ax.set_title("(a) Scale search: crop patches at multiple $s$,\n"
                 "pick the one with peak filter response", fontsize=10)

    # (b) Multi-rotation search
    ax = fig.add_subplot(gs[0, 1])
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.set_aspect("equal"); ax.axis("off")
    centre = np.array([0, 0])
    angles = np.linspace(-30, 30, 7)
    resp_r = np.exp(-((angles - 10) ** 2) / 80)
    for ang, r in zip(angles, resp_r):
        a = np.deg2rad(ang)
        R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        sq = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]]) * 1.5
        sq_r = sq @ R.T
        col = "tab:red" if abs(ang - angles[resp_r.argmax()]) < 1e-3 \
            else "tab:gray"
        lw = 2.5 if col == "tab:red" else 1.0
        ax.plot(sq_r[:, 0], sq_r[:, 1], color=col, lw=lw, alpha=0.9)
    ax2 = ax.inset_axes([0.65, 0.0, 0.35, 0.3])
    ax2.plot(angles, resp_r, "o-", color="tab:purple", lw=2)
    ax2.plot(angles[resp_r.argmax()], resp_r.max(), "*", color="tab:red",
             markersize=12)
    ax2.set_xlabel("$\\theta$ (deg)", fontsize=8)
    ax2.set_ylabel("response", fontsize=8)
    ax2.tick_params(labelsize=7)
    ax.set_title("(b) Multi-rotation search: filter evaluated\n"
                 "on rotated patches, best $\\theta$ chosen", fontsize=10)

    # (c) Why cyclic shifts model translation but not rotation
    ax = fig.add_subplot(gs[0, 2])
    ax.set_xlim(0, 6); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.2, 4.0), 2.5, 1.6,
                                boxstyle="round,pad=0.03",
                                fc="#bbf7d0", ec="black", lw=1.2))
    ax.text(1.45, 4.8,
            "Translation\ncyclic shift\n= circulant matrix\n→ diagonal in FFT",
            ha="center", va="center", fontsize=9)
    ax.add_patch(FancyBboxPatch((3.2, 4.0), 2.6, 1.6,
                                boxstyle="round,pad=0.03",
                                fc="#fecaca", ec="black", lw=1.2))
    ax.text(4.5, 4.8,
            "Rotation\nnot a cyclic shift\n→ no circulant\n→ requires extra search",
            ha="center", va="center", fontsize=9)
    ax.add_patch(FancyBboxPatch((0.2, 1.6), 5.6, 1.6,
                                boxstyle="round,pad=0.03",
                                fc="#fef3c7", ec="black", lw=1.2))
    ax.text(3.0, 2.4,
            "Workarounds:\n"
            "(i) sample multiple $\\theta$ around current estimate\n"
            "(ii) rotation-invariant features (e.g., colour names)\n"
            "(iii) slow implicit adaptation via online model update",
            ha="center", va="center", fontsize=9)
    ax.set_title("(c) Why rotation is harder than scale for DCF",
                 fontsize=10)

    fig.suptitle("DCT/KCF extensions: scale via multi-scale / DSST, "
                 "rotation via explicit search or robust features",
                 fontsize=13, y=1.02)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
