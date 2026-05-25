# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Training dynamics: SGD trajectory + dropout illustration for q_0041."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0041_training.png"
rng = np.random.default_rng(67)


def loss(w):
    """Banana-like non-convex loss."""
    x, y = w[..., 0], w[..., 1]
    return (1 - x) ** 2 + 50 * (y - x ** 2) ** 2 / 100.0


def grad(w):
    x, y = w
    dx = -2 * (1 - x) - 4 * x * 50 / 100.0 * (y - x ** 2)
    dy = 2 * 50 / 100.0 * (y - x ** 2)
    return np.array([dx, dy])


def trajectory(lr, n=80, momentum=0.0, start=np.array([-1.0, 1.0])):
    w = start.copy()
    v = np.zeros(2)
    traj = [w.copy()]
    for _ in range(n):
        g = grad(w)
        v = momentum * v - lr * g
        w = w + v
        if np.linalg.norm(w) > 5:
            break
        traj.append(w.copy())
    return np.array(traj)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # (a) SGD on a 2-D loss: three learning rates
    ax = axes[0]
    xx, yy = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-0.5, 2.5, 200))
    Z = loss(np.stack([xx, yy], axis=-1))
    ax.contour(xx, yy, Z, levels=np.logspace(-2, 1.5, 20), colors="black",
               linewidths=0.5, alpha=0.4)
    ax.contourf(xx, yy, Z, levels=np.logspace(-2, 1.5, 30), cmap="viridis",
                alpha=0.4)
    for lr, label, col in [(0.02, "η = 0.02 (slow)", "tab:blue"),
                           (0.08, "η = 0.08 (good)", "tab:green"),
                           (0.20, "η = 0.20 (diverge)", "tab:red")]:
        tr = trajectory(lr, n=120)
        ax.plot(tr[:, 0], tr[:, 1], "o-", lw=1.4, color=col,
                markersize=4, label=label)
    ax.plot(1, 1, "*", color="gold", markersize=22, markeredgecolor="black",
            zorder=5, label="optimum (1,1)")
    ax.set_xlabel("$w_1$"); ax.set_ylabel("$w_2$")
    ax.set_title("(a) SGD trajectory on a non-convex loss\n"
                 "learning rate $\\eta$ controls speed vs stability")
    ax.legend(fontsize=9)

    # (b) Dropout illustration
    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    layer_x = [1, 4, 7]
    layer_n = [4, 6, 4]
    layer_names = ["input", "hidden\n(p=0.5)", "hidden"]
    nodes = []
    for x, n, name in zip(layer_x, layer_n, layer_names):
        y_vals = np.linspace(1, 5, n)
        col_nodes = []
        for j, y in enumerate(y_vals):
            dropped = (x == 4 and rng.random() < 0.5)
            col = "lightgray" if dropped else "tab:blue"
            ax.add_patch(Circle((x, y), 0.22, fc=col, ec="black"))
            if dropped:
                ax.plot([x - 0.3, x + 0.3], [y - 0.3, y + 0.3],
                        color="tab:red", lw=2)
                ax.plot([x - 0.3, x + 0.3], [y + 0.3, y - 0.3],
                        color="tab:red", lw=2)
            col_nodes.append((x, y, dropped))
        nodes.append(col_nodes)
        ax.text(x, 5.6, name, ha="center", fontsize=10, fontweight="bold")
    # Edges (only from non-dropped)
    for li in range(len(layer_x) - 1):
        for x1, y1, drop1 in nodes[li]:
            for x2, y2, drop2 in nodes[li + 1]:
                if drop1 or drop2:
                    continue
                ax.plot([x1, x2], [y1, y2], color="black", alpha=0.3, lw=0.6)
    ax.set_title("(b) Dropout: random subset of units zeroed each iteration\n"
                 "→ ensemble of thinned subnetworks at test time")

    # (c) BatchNorm: training loss curves with/without
    ax = axes[2]
    epochs = np.arange(0, 60)
    without = 2.5 * np.exp(-epochs / 35) + 0.4
    with_bn = 2.5 * np.exp(-epochs / 10) + 0.2
    ax.plot(epochs, without, lw=2.4, color="tab:red", label="no BatchNorm  (η = 0.01)")
    ax.plot(epochs, with_bn, lw=2.4, color="tab:green", label="with BatchNorm  (η = 0.1)")
    ax.fill_between(epochs, 0, 0.4, alpha=0.1, color="tab:green")
    ax.set_xlabel("epoch")
    ax.set_ylabel("training loss")
    ax.set_title("(c) Batch normalisation enables higher $\\eta$\n→ ~10× fewer epochs")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    fig.suptitle("Training deep CNNs: SGD with learning-rate tuning, "
                 "dropout, and batch normalisation",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
