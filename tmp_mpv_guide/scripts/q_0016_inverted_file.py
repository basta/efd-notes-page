# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Inverted-file structure diagram + memory comparison for q_0016."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0016_inverted_file.png"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(15, 5.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.25)

    # (a) Inverted file schematic
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    # Vocabulary column on the left
    words = ["w₁", "w₂", "w₃", "w₄", "w₅"]
    for i, w in enumerate(words):
        y = 6 - i * 1.1
        ax.add_patch(FancyBboxPatch((0.2, y - 0.35), 1.0, 0.7,
                                    boxstyle="round,pad=0.02",
                                    fc="#bde0fe", ec="black"))
        ax.text(0.7, y, w, ha="center", va="center", fontsize=11, fontweight="bold")
        ax.text(0.7, y + 0.55, "" if i else "vocabulary", ha="center",
                fontsize=9, color="black")
    # Posting lists
    rng = np.random.default_rng(2)
    list_lens = [4, 2, 5, 1, 3]
    for i, n in enumerate(list_lens):
        y = 6 - i * 1.1
        ids = sorted(rng.choice(np.arange(1, 99), size=n, replace=False))
        tfs = rng.integers(1, 5, size=n)
        for j, (im_id, tf) in enumerate(zip(ids, tfs)):
            x = 1.7 + j * 1.4
            ax.add_patch(FancyBboxPatch((x, y - 0.3), 1.15, 0.6,
                                        boxstyle="round,pad=0.02",
                                        fc="#fef9c3", ec="black"))
            ax.text(x + 0.55, y, f"({im_id},{tf})", ha="center", va="center",
                    fontsize=9)
        # arrow from word
        ax.annotate("", xy=(1.7, y), xytext=(1.25, y),
                    arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(0.7, 6.7, "vocabulary", ha="center", fontsize=10, fontweight="bold")
    ax.text(4.5, 6.7, "posting lists $L_k$: (image-id, tf)", ha="center",
            fontsize=10, fontweight="bold")
    ax.set_title("(a) Inverted-file structure\nquery visits only posting lists "
                 "of query's visual words", fontsize=11)

    # (b) Memory: dense vs inverted-file as K grows
    ax = fig.add_subplot(gs[0, 1])
    K = np.logspace(2, 7, 100)
    M = 1e6  # images
    F_total = 1e9  # total features (independent of K)
    dense_bytes = M * K * 4  # float32 per cell
    if_bytes = F_total * (4 + 2) + K * 8  # (id+tf) per posting + index pointers
    ax.loglog(K, dense_bytes / 1e9, "-", lw=2.2, color="tab:red",
              label=f"dense:  $M \\times K \\times 4$  (M={M:.0e})")
    ax.loglog(K, if_bytes / 1e9, "-", lw=2.2, color="tab:green",
              label=f"inv. file:  $F_{{total}}(6) + 8K$  ($F_{{total}}={F_total:.0e}$)")
    ax.axvspan(64, 256, alpha=0.1, color="orange",
               label="small-K regime (dense+ANN)")
    ax.axvspan(1e5, 1e7, alpha=0.1, color="green",
               label="large-K regime (inverted file)")
    ax.set_xlabel("codebook size $K$")
    ax.set_ylabel("memory  [GB]")
    ax.set_title("(b) Memory: dense storage vs. inverted file\n"
                 "inverted-file memory ≈ flat in $K$ (dominated by $F_{total}$)")
    ax.grid(which="both", alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)

    fig.suptitle("Inverted-file structure & memory analysis for BoW retrieval",
                 fontsize=13, y=1.02)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
