# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""BoW histogram, idf weights, and similarity for q_0015."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0015_bow.png"
rng = np.random.default_rng(0)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K = 60
    # Simulate two images sharing some visual words plus generic ones.
    h_A = np.zeros(K, dtype=int)
    h_B = np.zeros(K, dtype=int)
    # Generic words shared by everyone (low idf): words 0-9
    h_A[0:10] = rng.integers(2, 8, size=10)
    h_B[0:10] = rng.integers(2, 8, size=10)
    # Distinctive shared words (rare): 30-37
    for k in range(30, 38):
        c = rng.integers(1, 4)
        h_A[k] = c
        h_B[k] = c + rng.integers(-1, 2)
    h_A = np.clip(h_A, 0, None)
    h_B = np.clip(h_B, 0, None)
    # Sprinkle a few non-shared words
    for k in rng.choice(np.arange(10, 30), size=5, replace=False):
        h_A[k] = rng.integers(1, 3)
    for k in rng.choice(np.arange(40, 60), size=5, replace=False):
        h_B[k] = rng.integers(1, 3)

    # idf: low for generic words (appear in most images), high for distinctive
    M = 1000
    M_k = np.full(K, 50)
    M_k[0:10] = 900  # generic
    M_k[30:38] = 20  # distinctive
    M_k[10:30] = 200
    M_k[38:] = 250
    w = np.log(M / M_k)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    ax = axes[0]
    ks = np.arange(K)
    ax.bar(ks, h_A, color="tab:blue", alpha=0.7, label="image A")
    ax.bar(ks, -h_B, color="tab:orange", alpha=0.7, label="image B")
    ax.axhline(0, color="black", lw=0.7)
    ax.set_xlabel("visual word index $k$")
    ax.set_ylabel("term frequency $h_k$")
    ax.set_title("(a) Sparse BoW term-frequency histograms\n(mirrored: A above, B below)")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1]
    ax.bar(ks, w, color="tab:green", edgecolor="black", lw=0.3)
    ax.set_xlabel("visual word index $k$")
    ax.set_ylabel("$w_k = \\log(M/M_k)$")
    ax.set_title("(b) idf weights\nlow for generic, high for rare words")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[2]
    contrib = w**2 * h_A * h_B
    colors = ["tab:red" if M_k[k] > 500 else "tab:green" for k in ks]
    ax.bar(ks, contrib, color=colors, edgecolor="black", lw=0.3)
    ax.set_xlabel("visual word index $k$")
    ax.set_ylabel("$w_k^2 \\, h_{A,k} \\, h_{B,k}$")
    ax.set_title(f"(c) Per-word contribution to dot-product\n"
                 f"green = distinctive (drive $s$), red = generic (~0)")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("Bag-of-Words: sparse histograms, idf weighting, "
                 "and idf-weighted similarity", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
