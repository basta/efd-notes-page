# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "opencv-python",
#   "matplotlib",
# ]
# ///
"""Affine shape adaptation visualisation for q_0004.

Builds an image with a strongly anisotropic blob (an elongated, rotated
ellipse of darker intensity on a bright background). Starting from an
isotropic circular window, iteratively:
  1. compute the second-moment matrix M of image gradients inside the
     current elliptical window,
  2. update the window shape to U_{k+1} = M^{-1/2} U_k,
until the eigenvalue ratio of M falls below 1 + eps.

We display:
  (a) the image with iteration ellipses (0..K) drawn at the blob centre,
      colour-coded from blue (initial circle) to red (converged ellipse),
      and overlay the *true* ellipse for reference.
  (b) the eigenvalue ratio λ_max / λ_min of M as a function of iteration,
      converging to ~1 (isotropic).
"""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0004_affine_adapt.png"


# --- ground-truth anisotropic blob ----------------------------------------
H, W = 280, 360
CX, CY = W // 2, H // 2
TRUE_SEMIS = (55.0, 18.0)   # major, minor semi-axis (px)
TRUE_THETA = np.deg2rad(28)  # rotation of major axis


def make_image() -> np.ndarray:
    img = np.full((H, W), 230, dtype=np.uint8)
    cv2.ellipse(img, (CX, CY),
                (int(TRUE_SEMIS[0]), int(TRUE_SEMIS[1])),
                float(np.rad2deg(TRUE_THETA)),
                0, 360, 30, -1)
    img = cv2.GaussianBlur(img, (7, 7), 1.5)
    rng = np.random.default_rng(0)
    img = np.clip(img + rng.normal(0, 1.5, img.shape), 0, 255).astype(np.uint8)
    return img


# --- second-moment matrix inside an elliptical window ---------------------
def second_moment_in_window(Ix: np.ndarray, Iy: np.ndarray,
                            U: np.ndarray, cx: int, cy: int,
                            radius: float = 1.0) -> np.ndarray:
    """Weighted sum of [[Ix^2, Ix Iy],[Ix Iy, Iy^2]] inside the ellipse
    {x : (x - c)^T (U U^T)^{-1} (x - c) <= radius^2 }, with a Gaussian
    weight matched to the ellipse."""
    h, w = Ix.shape
    # Build pixel coords centred at (cx, cy)
    yy, xx = np.mgrid[0:h, 0:w]
    dx = (xx - cx).astype(np.float32)
    dy = (yy - cy).astype(np.float32)
    # Whitened coordinates  z = U^{-1} (x - c)
    Uinv = np.linalg.inv(U)
    zx = Uinv[0, 0] * dx + Uinv[0, 1] * dy
    zy = Uinv[1, 0] * dx + Uinv[1, 1] * dy
    r2 = zx * zx + zy * zy
    # Gaussian weight in whitened space
    sigma = radius
    w_mask = np.exp(-0.5 * r2 / (sigma * sigma))
    w_mask[r2 > (3.0 * sigma) ** 2] = 0.0
    A = float(np.sum(w_mask * Ix * Ix))
    B = float(np.sum(w_mask * Ix * Iy))
    C = float(np.sum(w_mask * Iy * Iy))
    s = float(np.sum(w_mask)) + 1e-12
    return np.array([[A, B], [B, C]]) / s


def msqrt_inv(M: np.ndarray) -> np.ndarray:
    """M^{-1/2} via eigen-decomposition (M is symmetric PD)."""
    w, V = np.linalg.eigh(M)
    w = np.clip(w, 1e-10, None)
    return V @ np.diag(1.0 / np.sqrt(w)) @ V.T


def ellipse_patch_from_U(U: np.ndarray, scale: float, **kw) -> mpatches.Ellipse:
    """U is the affine shape such that ellipse = {U z : ||z|| <= 1}, scaled."""
    # Use SVD of U: U = R diag(s) R'.  Semi-axes are scale * s.
    Uw, Sw, _ = np.linalg.svd(U)
    semis = scale * Sw
    ang = np.degrees(np.arctan2(Uw[1, 0], Uw[0, 0]))
    return mpatches.Ellipse((CX, CY), width=2 * semis[0], height=2 * semis[1],
                            angle=ang, fill=False, lw=2, **kw)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = make_image()
    f = img.astype(np.float32) / 255.0
    f = cv2.GaussianBlur(f, (0, 0), 1.0)  # σ_D
    Ix = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3)
    Iy = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3)

    # Iterate: U_0 = (initial isotropic radius) * I
    init_r = 30.0
    U = init_r * np.eye(2)

    history_U = [U.copy()]
    history_ratio = []

    for it in range(8):
        M = second_moment_in_window(Ix, Iy, U, CX, CY, radius=1.0)
        w_eig = np.linalg.eigvalsh(M)
        w_eig = np.clip(w_eig, 1e-12, None)
        ratio = float(w_eig.max() / w_eig.min())
        history_ratio.append(ratio)
        # Shape update.  Normalize trace so the *overall scale* of the window
        # is preserved; only its shape changes.
        Tinv = msqrt_inv(M)
        # Compose update: new U = Tinv @ U, then renormalise so det(U) is fixed
        new_U = Tinv @ U
        # Renormalise so det(new_U) == det(U)
        det_ratio = np.linalg.det(U) / np.linalg.det(new_U)
        new_U = new_U * np.sqrt(abs(det_ratio))
        history_U.append(new_U.copy())
        U = new_U
        if abs(ratio - 1.0) < 0.02:
            break

    # Final M for the converged shape
    M_final = second_moment_in_window(Ix, Iy, U, CX, CY, radius=1.0)
    history_ratio.append(float(np.linalg.eigvalsh(M_final).max()
                               / max(np.linalg.eigvalsh(M_final).min(), 1e-12)))

    print(f"converged in {len(history_U) - 1} iterations, "
          f"final λ_max/λ_min = {history_ratio[-1]:.3f}")

    # ---- Figure ----
    fig = plt.figure(figsize=(13, 5.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.4, 1], wspace=0.18)

    # (a) image + iteration ellipses
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    # Ground-truth ellipse (dashed white)
    true_e = mpatches.Ellipse(
        (CX, CY), width=2 * TRUE_SEMIS[0], height=2 * TRUE_SEMIS[1],
        angle=np.rad2deg(TRUE_THETA),
        fill=False, edgecolor="white", lw=2.0, ls="--", label="true blob")
    ax.add_patch(true_e)
    cmap = plt.get_cmap("viridis")
    K = len(history_U)
    for k, Uk in enumerate(history_U):
        col = cmap(k / max(K - 1, 1))
        e = ellipse_patch_from_U(Uk, scale=1.0, edgecolor=col,
                                 label=(f"iter {k}" if k in (0, K - 1) else None))
        ax.add_patch(e)
    ax.plot(CX, CY, "+", color="red", markersize=12, mew=2.5)
    ax.set_title(f"(a) Affine shape adaptation: initial circle → converged "
                 f"ellipse  ({K-1} iters)")
    ax.axis("off")
    ax.legend(loc="upper right", fontsize=9)

    # (b) eigenvalue ratio convergence
    ax = fig.add_subplot(gs[0, 1])
    its = np.arange(len(history_ratio))
    ax.plot(its, history_ratio, "o-", color="tab:blue", lw=2, markersize=7)
    ax.axhline(1.0, color="0.5", ls="--", lw=1, label="isotropic (=1)")
    ax.set_xlabel("iteration")
    ax.set_ylabel(r"$\lambda_{\max}/\lambda_{\min}$ of  $M$")
    ax.set_title("(b) Convergence of the eigenvalue ratio of M")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)
    # annotate each point
    for it, r in zip(its, history_ratio):
        ax.annotate(f"{r:.2f}", (it, r),
                    textcoords="offset points", xytext=(6, 6), fontsize=8)

    fig.suptitle("Affine shape adaptation (Harris-/Hessian-Affine)", fontsize=13)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
