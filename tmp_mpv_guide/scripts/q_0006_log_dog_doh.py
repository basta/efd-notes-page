# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""LoG vs DoG vs DoH comparison for q_0006.

Two figure rows:

Top row — the three filter responses applied at the same scale to a test
image containing a bright blob and two saddle-like patterns.  The 1D
profiles of the three kernels are inset.

Bottom row — the scale-normalised response curves σ²|∇²L|, |LoG ≈ DoG|,
and σ⁴|det H| at the centre of a single blob, demonstrating that all
three peak near σ = r/√2 (but with different magnitudes/widths).
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0006_log_dog_doh.png"


def make_image(h: int = 240, w: int = 380):
    """Bright disk + one saddle-like (XOR-pattern) feature + flat region."""
    img = np.full((h, w), 200, dtype=np.uint8)
    # Bright disk on dark background — but our background is light, so use dark blob
    cv2.circle(img, (90, 120), 22, 40, -1)
    # Saddle-like: black/white quadrants meeting at (260, 120)
    cv2.rectangle(img, (220, 80), (260, 120), 30, -1)
    cv2.rectangle(img, (260, 120), (300, 160), 30, -1)
    cv2.rectangle(img, (260, 80), (300, 120), 240, -1)
    cv2.rectangle(img, (220, 120), (260, 160), 240, -1)
    img = cv2.GaussianBlur(img, (5, 5), 1.0)
    rng = np.random.default_rng(0)
    img = np.clip(img + rng.normal(0, 1.5, img.shape), 0, 255).astype(np.uint8)
    return img, (90, 120, 22), (260, 120)


def log_response(img: np.ndarray, sigma: float) -> np.ndarray:
    f = img.astype(np.float32) / 255.0
    L = cv2.GaussianBlur(f, (0, 0), sigma)
    Lxx = cv2.Sobel(L, cv2.CV_32F, 2, 0, ksize=3)
    Lyy = cv2.Sobel(L, cv2.CV_32F, 0, 2, ksize=3)
    return sigma * sigma * (Lxx + Lyy)


def dog_response(img: np.ndarray, sigma: float, k: float = np.sqrt(2)) -> np.ndarray:
    f = img.astype(np.float32) / 255.0
    L1 = cv2.GaussianBlur(f, (0, 0), sigma)
    L2 = cv2.GaussianBlur(f, (0, 0), k * sigma)
    return (L2 - L1) / (k - 1)


def doh_response(img: np.ndarray, sigma: float) -> np.ndarray:
    f = img.astype(np.float32) / 255.0
    L = cv2.GaussianBlur(f, (0, 0), sigma)
    Lxx = cv2.Sobel(L, cv2.CV_32F, 2, 0, ksize=3)
    Lyy = cv2.Sobel(L, cv2.CV_32F, 0, 2, ksize=3)
    Lxy = cv2.Sobel(L, cv2.CV_32F, 1, 1, ksize=3)
    return sigma ** 4 * (Lxx * Lyy - Lxy * Lxy)


def kernel_1d_profile(sigma: float, n: int = 81):
    """LoG, DoG, and (–DoH-flavour: Gx*Gx – we plot the LoG and DoG profile
    along x.  DoH is a 2D operator with no clean 1D analogue, so we omit it
    in the kernel inset."""
    x = np.arange(-n // 2, n // 2 + 1).astype(np.float32)
    G = np.exp(-x ** 2 / (2 * sigma ** 2)) / (np.sqrt(2 * np.pi) * sigma)
    Gpp = (x ** 2 / sigma ** 4 - 1 / sigma ** 2) * G        # ∂²G/∂x²
    LoG = sigma ** 2 * Gpp
    k = np.sqrt(2)
    G_big = np.exp(-x ** 2 / (2 * (k * sigma) ** 2)) / (np.sqrt(2 * np.pi) * k * sigma)
    DoG = (G_big - G) / (k - 1)
    return x, LoG, DoG


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img, (cx, cy, r), (sx, sy) = make_image()

    sigma_show = r / np.sqrt(2)   # matched scale for the disk
    Rlog = log_response(img, sigma_show)
    Rdog = dog_response(img, sigma_show)
    Rdoh = doh_response(img, sigma_show)

    # Scale sweep
    sigmas = np.geomspace(2.0, 40.0, 36)
    log_curve = [log_response(img, s)[cy, cx] for s in sigmas]
    dog_curve = [dog_response(img, s)[cy, cx] for s in sigmas]
    doh_curve = [doh_response(img, s)[cy, cx] for s in sigmas]
    log_curve = np.array(log_curve)
    dog_curve = np.array(dog_curve)
    doh_curve = np.array(doh_curve)

    # The disk is dark on light background ⇒ LoG/DoG are *positive* at centre
    # only when matched.  For "matched-filter" feeling we plot |·|.
    s_star_log = sigmas[int(np.argmax(np.abs(log_curve)))]
    s_star_dog = sigmas[int(np.argmax(np.abs(dog_curve)))]
    s_star_doh = sigmas[int(np.argmax(np.abs(doh_curve)))]
    s_theory = r / np.sqrt(2)
    print(f"r={r}  r/√2={s_theory:.2f}  "
          f"σ*: LoG={s_star_log:.2f}  DoG={s_star_dog:.2f}  DoH={s_star_doh:.2f}")

    # ---- Figure ----
    fig = plt.figure(figsize=(15, 8.5))
    gs = fig.add_gridspec(2, 3, hspace=0.32, wspace=0.18,
                          height_ratios=[1, 1])

    def show_response(ax, R, title, cmap="seismic"):
        v = np.percentile(np.abs(R), 99) + 1e-9
        ax.imshow(R, cmap=cmap, vmin=-v, vmax=v)
        ax.imshow(img, cmap="gray", alpha=0.2)
        # Mark probe locations
        ax.add_patch(mpatches.Circle((cx, cy), r, fill=False,
                                     edgecolor="lime", lw=1.5, ls="--"))
        ax.plot(sx, sy, "x", color="cyan", mew=2, markersize=10)
        ax.set_title(title, fontsize=11)
        ax.axis("off")

    show_response(fig.add_subplot(gs[0, 0]), Rlog,
                  f"(a) σ²·∇²L  (LoG)   σ={sigma_show:.1f}")
    show_response(fig.add_subplot(gs[0, 1]), Rdog,
                  f"(b) DoG ≈ σ²·∇²L   σ={sigma_show:.1f}")
    show_response(fig.add_subplot(gs[0, 2]), Rdoh,
                  f"(c) σ⁴·det H  (DoH)   σ={sigma_show:.1f}")

    # Inset 1D profiles of LoG and DoG (top-left axes)
    x_k, log_k, dog_k = kernel_1d_profile(sigma_show)
    ax_ins = fig.add_axes([0.06, 0.84, 0.13, 0.10])
    ax_ins.plot(x_k, log_k, "tab:blue", lw=1.5, label="LoG")
    ax_ins.plot(x_k, dog_k, "tab:orange", lw=1.2, ls="--", label="DoG")
    ax_ins.axhline(0, color="0.5", lw=0.5)
    ax_ins.set_xticks([])
    ax_ins.set_yticks([])
    ax_ins.legend(fontsize=7, loc="upper right")
    ax_ins.set_title("kernel 1D", fontsize=8)

    # Bottom row: scale-sweep curves at blob centre
    ax = fig.add_subplot(gs[1, :])
    # Normalise each curve to its peak |·| for direct comparison
    def norm(c):
        return c / max(np.abs(c).max(), 1e-9)
    ax.plot(sigmas, np.abs(norm(log_curve)), "o-", color="tab:blue", lw=2, label="|LoG|")
    ax.plot(sigmas, np.abs(norm(dog_curve)), "s--", color="tab:orange", lw=2, label="|DoG|")
    ax.plot(sigmas, np.abs(norm(doh_curve)), "^-",  color="tab:green", lw=2, label="|DoH|")
    ax.axvline(s_theory, color="0.4", ls=":", lw=1.5, label=f"r/√2 = {s_theory:.2f}")
    ax.set_xscale("log")
    ax.set_xlabel("σ  (log scale)")
    ax.set_ylabel("normalised |response| at blob centre")
    ax.set_title("(d) Scale-sweep at the blob centre — all three operators peak near σ = r/√2")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=10, loc="lower center", ncol=4)

    fig.suptitle("Three blob detectors: LoG vs DoG vs DoH",
                 fontsize=14, y=0.995)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
