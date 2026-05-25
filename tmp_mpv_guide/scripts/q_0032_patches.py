# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Suitable vs unsuitable tracking patches: SSD landscape & aperture for q_0032."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0032_patches.png"
rng = np.random.default_rng(43)


def ssd_landscape(patch, search):
    """SSD of patch vs every shift in `search` (zero-padded windowed)."""
    ps = patch.shape[0]
    half = ps // 2
    H, W = search.shape
    out = np.full((H, W), np.nan)
    for yy in range(half, H - half):
        for xx in range(half, W - half):
            w = search[yy - half:yy + half + 1, xx - half:xx + half + 1]
            out[yy, xx] = ((w - patch) ** 2).sum()
    return out


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    N = 11
    # 1. Flat patch  →  ambiguous everywhere
    flat = np.full((N, N), 0.5) + rng.normal(0, 0.01, size=(N, N))
    # 2. Vertical edge  →  ambiguity along vertical direction
    edge = np.zeros((N, N))
    edge[:, N // 2:] = 1.0
    # 3. Corner (L)  →  single sharp minimum
    corner = np.zeros((N, N))
    corner[N // 2:, :N // 2] = 1.0
    corner[:N // 2, N // 2:] = 1.0

    patches = [("Flat\n(SSD ≈ flat — no info)", flat),
               ("Edge\n(SSD valley along edge — aperture)", edge),
               ("Corner\n(unique sharp SSD minimum)", corner)]

    fig, axes = plt.subplots(2, 3, figsize=(13, 8),
                             gridspec_kw=dict(height_ratios=[1, 1.3]))

    # Build a fake search image for each: bigger patch with the same structure
    Ns = 41
    search_flat = np.full((Ns, Ns), 0.5) + rng.normal(0, 0.01, size=(Ns, Ns))
    search_edge = np.zeros((Ns, Ns)); search_edge[:, Ns // 2:] = 1.0
    search_corner = np.zeros((Ns, Ns))
    search_corner[Ns // 2:, :Ns // 2] = 1.0
    search_corner[:Ns // 2, Ns // 2:] = 1.0
    searches = [search_flat, search_edge, search_corner]

    for k, ((name, p), s) in enumerate(zip(patches, searches)):
        axes[0, k].imshow(p, cmap="gray", vmin=0, vmax=1)
        axes[0, k].set_title(name, fontsize=11)
        axes[0, k].set_xticks([]); axes[0, k].set_yticks([])

        ssd = ssd_landscape(p, s)
        im = axes[1, k].imshow(ssd, cmap="viridis")
        axes[1, k].set_title("SSD cost surface (lower = better)", fontsize=10)
        axes[1, k].set_xticks([]); axes[1, k].set_yticks([])
        plt.colorbar(im, ax=axes[1, k], fraction=0.046)

    fig.suptitle("Tracking patch suitability: corner has a unique SSD minimum; "
                 "flat/edge patches are ambiguous", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
