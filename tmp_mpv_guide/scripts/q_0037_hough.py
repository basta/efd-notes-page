# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Hough transform for line detection: edge map → (ρ,θ) accumulator → peaks."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0037_hough.png"
rng = np.random.default_rng(61)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Generate two lines + outliers
    n_per_line = 60
    n_out = 100
    # Line 1: rho=20, theta = 20 deg
    rho1, th1 = 20.0, np.deg2rad(20)
    # Line 2: rho=-15, theta = 110 deg
    rho2, th2 = -15.0, np.deg2rad(110)
    pts = []
    for rho, th, n in [(rho1, th1, n_per_line), (rho2, th2, n_per_line)]:
        n_vec = np.array([np.cos(th), np.sin(th)])
        d_vec = np.array([-np.sin(th), np.cos(th)])
        ts = rng.uniform(-40, 40, n)
        line = rho * n_vec + ts[:, None] * d_vec
        line += rng.normal(0, 0.5, size=line.shape)
        pts.append(line)
    out = rng.uniform(-50, 50, size=(n_out, 2))
    pts.append(out)
    edge = np.vstack(pts)

    # Build accumulator
    thetas = np.linspace(0, np.pi, 180, endpoint=False)
    rhos = np.linspace(-80, 80, 161)
    acc = np.zeros((len(rhos), len(thetas)))
    cos_t, sin_t = np.cos(thetas), np.sin(thetas)
    for x, y in edge:
        r = x * cos_t + y * sin_t
        for j, rv in enumerate(r):
            i = int(round((rv + 80)))
            if 0 <= i < len(rhos):
                acc[i, j] += 1

    # Find two peaks
    flat = acc.flatten()
    top_idx = np.argpartition(flat, -2)[-2:]
    peaks = [np.unravel_index(i, acc.shape) for i in top_idx]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    ax = axes[0]
    ax.scatter(*edge.T, s=8, color="black", alpha=0.6)
    ax.set_xlim(-50, 50); ax.set_ylim(-50, 50); ax.set_aspect("equal")
    ax.set_title(f"(a) Edge points: 2 true lines + {n_out} outliers")
    ax.grid(alpha=0.3)

    ax = axes[1]
    im = ax.imshow(acc, extent=[0, 180, -80, 80], origin="lower", aspect="auto",
                   cmap="hot")
    ax.set_xlabel("$\\theta$  (degrees)")
    ax.set_ylabel("$\\rho$")
    ax.set_title("(b) Hough accumulator $(\\rho, \\theta)$\n"
                 "outliers add a diffuse background, true lines form peaks")
    plt.colorbar(im, ax=ax, fraction=0.046)
    for pi, pj in peaks:
        ax.plot(np.rad2deg(thetas[pj]), rhos[pi], "o", markersize=14,
                markerfacecolor="none", markeredgecolor="cyan", lw=2)

    ax = axes[2]
    ax.scatter(*edge.T, s=8, color="tab:gray", alpha=0.5)
    # Draw detected lines
    xs = np.linspace(-50, 50, 2)
    for pi, pj in peaks:
        r, t = rhos[pi], thetas[pj]
        if abs(np.sin(t)) > 0.1:
            ys = (r - xs * np.cos(t)) / np.sin(t)
            ax.plot(xs, ys, "-", lw=2.5, color="tab:red")
        else:
            ax.axvline(r / np.cos(t), color="tab:red", lw=2.5)
    ax.set_xlim(-50, 50); ax.set_ylim(-50, 50); ax.set_aspect("equal")
    ax.set_title("(c) Detected lines (peaks → image space)")
    ax.grid(alpha=0.3)

    fig.suptitle("Hough transform: each edge point votes for a $\\rho(\\theta)$ "
                 "sinusoid; peaks = lines",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
