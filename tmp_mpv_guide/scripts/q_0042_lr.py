# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Learning-rate range test + schedules for q_0042."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0042_lr.png"
rng = np.random.default_rng(71)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # (a) LR range test curve
    ax = axes[0]
    lrs = np.logspace(-6, 1, 200)
    # idealised behaviour: too small → flat loss, sweet spot, diverge
    def smoothstep(x):
        return np.where(x < 0, 0, np.where(x > 1, 1, 3 * x ** 2 - 2 * x ** 3))
    # start near 3.0, drop to ~0.3 in good region, then blow up
    log_lr = np.log10(lrs)
    descent = 3.0 - 2.5 * smoothstep((log_lr - (-5)) / 2.0)  # drops 3→0.5 between 1e-5 and 1e-3
    explode = 3.5 * smoothstep((log_lr - (-2)) / 1.0)        # explodes after 1e-2
    loss = descent + explode
    loss += rng.normal(0, 0.07, size=loss.shape)
    ax.semilogx(lrs, loss, lw=2.2, color="tab:blue")
    # Annotate regions
    ax.axvspan(1e-6, 3e-5, color="tab:gray", alpha=0.15,
               label="too small (flat loss)")
    ax.axvspan(3e-5, 1e-2, color="tab:green", alpha=0.20,
               label="sweet spot (steep descent)")
    ax.axvspan(1e-2, 10, color="tab:red", alpha=0.15,
               label="too large (diverges)")
    # Recommended rate ~ one order below where it diverges (≈ 5e-3)
    rec = 5e-3
    ax.axvline(rec, color="black", ls="--", lw=1.5)
    ax.text(rec * 1.1, 1.8, f"recommended\n$\\eta \\approx {rec:g}$",
            fontsize=10)
    ax.set_xlabel("learning rate $\\eta$  (log scale)")
    ax.set_ylabel("training loss after a few mini-batches")
    ax.set_title("(a) Learning-rate range test\nsweep $\\eta$ low→high, "
                 "pick where loss decreases fastest")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(which="both", alpha=0.3)

    # (b) LR schedules
    ax = axes[1]
    epochs = np.arange(0, 100)
    eta0 = 0.1
    step = eta0 * 0.1 ** (epochs // 30)
    expo = eta0 * np.exp(-0.04 * epochs)
    cos = 0.001 + 0.5 * (eta0 - 0.001) * (1 + np.cos(epochs / 100 * np.pi))
    warmup_cos = np.where(epochs < 5, eta0 * (epochs + 1) / 5,
                          0.001 + 0.5 * (eta0 - 0.001) *
                          (1 + np.cos((epochs - 5) / 95 * np.pi)))
    ax.plot(epochs, step, lw=2.2, label="step decay (×0.1 every 30 ep)")
    ax.plot(epochs, expo, lw=2.2, label="exponential")
    ax.plot(epochs, cos, lw=2.2, label="cosine annealing")
    ax.plot(epochs, warmup_cos, lw=2.2, ls="--",
            label="warmup → cosine")
    ax.set_yscale("log")
    ax.set_xlabel("epoch")
    ax.set_ylabel("$\\eta$  (log)")
    ax.set_title("(b) Common learning-rate schedules")
    ax.legend(fontsize=10)
    ax.grid(which="both", alpha=0.3)

    fig.suptitle("Selecting and scheduling the learning rate",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
