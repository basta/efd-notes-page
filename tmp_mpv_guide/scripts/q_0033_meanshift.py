# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Mean-shift in 1D: iteration trace + density estimate for q_0033."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0033_meanshift.png"


def mean_shift_uniform(data, x0, h, tol=1e-5, max_iter=50):
    trace = [x0]
    x = x0
    for _ in range(max_iter):
        mask = np.abs(data - x) <= h
        if mask.sum() == 0:
            break
        new = data[mask].mean()
        trace.append(new)
        if abs(new - x) < tol:
            break
        x = new
    return np.array(trace)


def kde_uniform(data, xs, h):
    return np.array([(np.abs(data - x) <= h).sum() for x in xs]) / (len(data) * 2 * h)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = np.array([1.0, 2.0, 3.0, 7.0, 8.0])
    h = 2.0

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # (a) Density estimate + two starting points + traces
    ax = axes[0]
    xs = np.linspace(-1, 11, 400)
    f = kde_uniform(data, xs, h)
    ax.plot(xs, f, color="tab:blue", lw=2, label=f"KDE  ($h={h}$, uniform)")
    ax.fill_between(xs, 0, f, alpha=0.15, color="tab:blue")
    for d in data:
        ax.axvline(d, color="black", alpha=0.6, lw=1)
    ax.scatter(data, np.zeros_like(data), s=100, marker="^", color="black",
               zorder=5, label="data points")

    for x0, col in [(2.5, "tab:red"), (6.0, "tab:green")]:
        trace = mean_shift_uniform(data, x0, h)
        ax.plot(trace, np.full_like(trace, 0.02 if col == "tab:red" else 0.05),
                "o-", color=col, lw=2, markersize=8,
                label=f"trace from $x^{{(0)}}={x0}$  → $x={trace[-1]:.2f}$")
        # arrow showing first shift
        ax.annotate("", xy=(trace[1], 0.02 if col == "tab:red" else 0.05),
                    xytext=(trace[0], 0.02 if col == "tab:red" else 0.05),
                    arrowprops=dict(arrowstyle="->", color=col, lw=2))
    ax.set_xlabel("$x$")
    ax.set_ylabel("density estimate  $\\hat f(x)$")
    ax.set_title(f"(a) Mean-shift on 1-D toy data, $h={h}$\n"
                 "two starts converge to the two modes ($x = 2$, $x = 7.5$)")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(alpha=0.3)

    # (b) Effect of bandwidth h: number of modes
    ax = axes[1]
    h_vals = np.linspace(0.5, 5.0, 60)
    n_modes = []
    for hv in h_vals:
        xs = np.linspace(-1, 11, 600)
        f = kde_uniform(data, xs, hv)
        peaks = ((f[1:-1] > f[:-2]) & (f[1:-1] > f[2:])).sum()
        n_modes.append(max(peaks, 1) if f.max() > 0 else 0)
    ax.plot(h_vals, n_modes, "o-", color="tab:purple", lw=2)
    ax.axvline(2.0, ls="--", color="tab:red", lw=1.5,
               label="$h = 2$ → 2 modes")
    ax.axvline(5.0, ls="--", color="tab:green", lw=1.5,
               label="$h \\geq 5$ → 1 mode (merges)")
    ax.set_xlabel("bandwidth $h$")
    ax.set_ylabel("# modes found")
    ax.set_title("(b) Bandwidth $h$ controls density smoothing & mode count")
    ax.legend(fontsize=10)
    ax.set_yticks([0, 1, 2, 3])
    ax.grid(alpha=0.3)

    fig.suptitle("Mean-shift: gradient-ascent on a kernel density estimate",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
