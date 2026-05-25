# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Image-to-vector retrieval: well- vs poorly-trained embedding for q_0021."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0021_embedding.png"
rng = np.random.default_rng(13)


def make_classes(spread: float):
    centres = np.array([[2.0, 2.0], [-2.0, 1.8], [0.0, -2.2], [2.5, -1.5]])
    classes = []
    for c in centres:
        classes.append(c + rng.normal(0, spread, size=(40, 2)))
    return centres, classes


def project_unit(p):
    return p / np.linalg.norm(p, axis=1, keepdims=True)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    cmap = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    titles = [("(a) Poorly-trained / no metric learning",
               "classes overlap → nearest-neighbour retrieval fails", 1.3),
              ("(b) Well-trained metric embedding",
               "tight, separated clusters → top-$k$ NN ≈ relevant matches", 0.35)]

    for ax, (title, sub, spread) in zip(axes, titles):
        _, cls = make_classes(spread)
        # Project to unit circle (ℓ2-normalise) as in cosine retrieval
        all_pts = np.vstack(cls)
        all_pts = project_unit(all_pts)
        # restore class boundaries from indices
        offset = 0
        for k, c in enumerate(cls):
            n = len(c)
            pts = all_pts[offset:offset + n]
            ax.scatter(*pts.T, s=42, color=cmap[k], alpha=0.85,
                       edgecolors="black", lw=0.3, label=f"class {k+1}")
            offset += n
        # Query: one point of class 0
        q = project_unit(np.array([[2.2, 2.1]]))[0]
        ax.scatter(*q, marker="*", s=380, color="black",
                   edgecolors="yellow", lw=1.5, zorder=5, label="query")
        # NN search radius (cosine ~ small angle)
        from matplotlib.patches import Circle
        ax.add_patch(Circle(q, 0.45, fill=False, ec="black", lw=1.5,
                            ls="--"))
        ax.set_title(f"{title}\n{sub}", fontsize=11)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect("equal")
        ax.set_xlabel("descriptor dim 1 (after $\\ell_2$ norm)")
        ax.set_ylabel("descriptor dim 2")
        ax.legend(loc="lower left", fontsize=8)
        ax.grid(alpha=0.3)

    fig.suptitle("Mapping images to a vector space: retrieval = NN search\n"
                 "metric learning makes the same NN procedure accurate",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
