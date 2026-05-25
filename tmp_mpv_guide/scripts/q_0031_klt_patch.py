# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""KLT patch suitability under horizontal camera motion for q_0031."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0031_klt_patch.png"


def gradient(p):
    Ix = np.zeros_like(p)
    Iy = np.zeros_like(p)
    Ix[:, 1:-1] = (p[:, 2:] - p[:, :-2]) / 2.0
    Iy[1:-1, :] = (p[2:, :] - p[:-2, :]) / 2.0
    return Ix, Iy


def structure_tensor(patch):
    Ix, Iy = gradient(patch.astype(float))
    H = np.array([[(Ix * Ix).sum(), (Ix * Iy).sum()],
                  [(Ix * Iy).sum(), (Iy * Iy).sum()]])
    return H


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Three synthetic 21x21 patches
    N = 21
    flat = np.full((N, N), 0.5)
    flat += np.random.default_rng(0).normal(0, 0.01, size=flat.shape)
    edge = np.zeros((N, N))
    edge[:, N // 2:] = 1.0  # vertical edge
    corner = np.zeros((N, N))
    corner[N // 2:, :N // 2] = 1.0
    corner[:N // 2, N // 2:] = 1.0  # L-shaped corner

    patches = [("Flat region", flat),
               ("Vertical edge", edge),
               ("L-shaped corner (suitable)", corner)]

    fig, axes = plt.subplots(2, 3, figsize=(13, 7),
                             gridspec_kw=dict(height_ratios=[1.0, 0.7]))

    for k, (name, p) in enumerate(patches):
        ax = axes[0, k]
        ax.imshow(p, cmap="gray", vmin=0, vmax=1)
        H = structure_tensor(p)
        eigs = np.sort(np.linalg.eigvalsh(H))[::-1]
        cond = "well-cond." if eigs[1] / max(eigs[0], 1e-9) > 0.05 \
            else "singular / ill-cond."
        ax.set_title(f"{name}\n$\\lambda_1$={eigs[0]:.2f}, "
                     f"$\\lambda_2$={eigs[1]:.2f}   ({cond})", fontsize=11)
        ax.set_xticks([]); ax.set_yticks([])
        # Bottom row: eigenvalue bar
        ax2 = axes[1, k]
        ax2.bar(["$\\lambda_1$", "$\\lambda_2$"], eigs,
                color=["tab:red", "tab:orange"],
                edgecolor="black")
        ax2.set_ylim(0, max([np.linalg.eigvalsh(structure_tensor(q))[-1]
                             for _, q in patches]) * 1.15)
        ax2.set_ylabel("eigenvalue")
        ax2.grid(alpha=0.3, axis="y")
        verdict = {"Flat region": "NOT suitable (no gradients)",
                   "Vertical edge": "NOT suitable\n(aperture: $p_2$ unobservable)",
                   "L-shaped corner (suitable)":
                       "SUITABLE\n(both $\\lambda$'s large)"}[name]
        ax2.set_title(verdict, fontsize=10, color="tab:green"
                      if "SUIT" in verdict else "tab:red")

    fig.suptitle("KLT patch selection: structure-tensor eigenvalues determine "
                 "suitability\n(even with purely horizontal motion, "
                 "standard KLT needs both $\\lambda$'s > 0)",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
