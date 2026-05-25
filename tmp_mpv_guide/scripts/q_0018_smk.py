# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Selective Match Kernel: non-linear gating f(u)=sign(u)|u|^alpha for q_0018."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0018_smk.png"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    u = np.linspace(-1, 1, 401)
    alphas = [1.0, 2.0, 3.0, 5.0]
    colors = ["tab:gray", "tab:blue", "tab:green", "tab:red"]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # (a) f(u) for various alpha
    ax = axes[0]
    for a, c in zip(alphas, colors):
        ax.plot(u, np.sign(u) * np.abs(u) ** a,
                color=c, lw=2.2, label=f"$\\alpha = {a:g}$" + ("  (linear)" if a == 1 else ""))
    ax.axhline(0, color="black", lw=0.5)
    ax.axvline(0, color="black", lw=0.5)
    ax.set_xlabel("residual dot product  $u = \\mathbf{r}(\\mathbf{x})^\\top \\mathbf{r}(\\mathbf{y})$")
    ax.set_ylabel("vote contribution  $f(u)$")
    ax.set_title("(a) Selectivity function  $f(u) = \\operatorname{sign}(u)\\,|u|^\\alpha$\n"
                 "$\\alpha > 1$  suppresses weak matches, amplifies strong ones")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    # (b) Contributions of a mixture of matches (strong + many weak)
    ax = axes[1]
    rng = np.random.default_rng(7)
    weak = rng.normal(0.0, 0.15, size=200)  # many noisy matches
    strong = np.array([0.85, 0.78, 0.92, 0.7])  # a few genuine
    matches = np.concatenate([weak, strong])
    labels = ["weak/noisy"] * len(weak) + ["strong/genuine"] * len(strong)
    totals = {}
    for a in alphas:
        f = np.sign(matches) * np.abs(matches) ** a
        totals[a] = {
            "weak": float(np.abs(f[: len(weak)]).sum()),
            "strong": float(np.abs(f[len(weak):]).sum()),
        }
    xs = np.arange(len(alphas))
    width = 0.4
    weak_bars = [totals[a]["weak"] for a in alphas]
    strong_bars = [totals[a]["strong"] for a in alphas]
    ax.bar(xs - width / 2, weak_bars, width, color="tab:gray",
           label=f"sum |f| over {len(weak)} weak matches")
    ax.bar(xs + width / 2, strong_bars, width, color="tab:green",
           label=f"sum |f| over {len(strong)} strong matches")
    for x, (w, s) in enumerate(zip(weak_bars, strong_bars)):
        ratio = s / w if w > 0 else float("inf")
        ax.text(x, max(w, s) + 0.05, f"S:W = {ratio:.1f}",
                ha="center", fontsize=10, fontweight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels([f"$\\alpha={a:g}$" for a in alphas])
    ax.set_ylabel("$\\sum |f(u)|$")
    ax.set_title("(b) Strong-vs-weak match accumulation\n"
                 "larger $\\alpha$ → strong matches dominate the score")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("Selective Match Kernel: non-linear gating amplifies "
                 "genuine matches", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
