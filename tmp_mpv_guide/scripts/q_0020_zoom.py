# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Zoom-in retrieval: scale-aware reweighting for q_0020."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0020_zoom.png"
rng = np.random.default_rng(11)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # (a) Three candidate images with different scale-ratio distributions of matches
    ax = axes[0]
    r_dup = rng.normal(1.0, 0.07, 80)                # near-duplicate: r ~ 1
    r_zoom = rng.normal(1.8, 0.2, 40)                # zoom-in: r > 1
    r_wide = rng.normal(0.5, 0.1, 80)                # wide-angle: r < 1
    bins = np.linspace(0.2, 2.6, 50)
    ax.hist(r_dup, bins=bins, alpha=0.55, color="tab:blue",
            label=f"near-duplicate ({len(r_dup)} matches)")
    ax.hist(r_zoom, bins=bins, alpha=0.55, color="tab:green",
            label=f"zoom-in ({len(r_zoom)} matches)")
    ax.hist(r_wide, bins=bins, alpha=0.55, color="tab:red",
            label=f"wide-angle ({len(r_wide)} matches)")
    ax.axvline(1.0, color="black", lw=1.2, ls="--")
    ax.text(1.02, ax.get_ylim()[1] * 0.95, "$r=1$  (same scale)",
            fontsize=9, va="top")
    ax.set_xlabel("scale ratio  $r = \\mathrm{scale}(A_{db})/\\mathrm{scale}(A_q)$")
    ax.set_ylabel("# matches")
    ax.set_title("(a) Per-candidate scale-ratio distribution of matches\n"
                 "BoW would rank near-duplicate top (most matches)")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.3, axis="y")

    # (b) Scoring under each scheme
    ax = axes[1]
    matches = {"near-dup": r_dup, "zoom-in": r_zoom, "wide-angle": r_wide}
    colors = {"near-dup": "tab:blue", "zoom-in": "tab:green",
              "wide-angle": "tab:red"}
    schemes = {
        "standard BoW\n$g(r)=1$": lambda r: np.ones_like(r),
        "scale-aware\n$g(r)=r^2$": lambda r: r**2,
        "step (r>1)\n$g(r)=r\\cdot\\mathbb{1}[r>1]$": lambda r: r * (r > 1),
    }
    cats = list(matches)
    xs = np.arange(len(schemes))
    width = 0.25
    for i, c in enumerate(cats):
        scores = [schemes[s](matches[c]).sum() for s in schemes]
        ax.bar(xs + (i - 1) * width, scores, width,
               color=colors[c], label=c)
    ax.set_xticks(xs)
    ax.set_xticklabels(list(schemes), fontsize=9)
    ax.set_ylabel("aggregate score per candidate")
    ax.set_title("(b) Candidate scores under three vote weights\n"
                 "scale-aware schemes push the zoom-in candidate to the top")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("Zoom-in retrieval requires a scale-aware vote weight",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
