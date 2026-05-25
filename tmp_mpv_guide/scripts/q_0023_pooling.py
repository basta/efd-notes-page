# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""SPoC / MAC / GeM pooling comparison for q_0023."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0023_pooling.png"
rng = np.random.default_rng(17)


def gem(x, p):
    return (np.mean(np.clip(x, 1e-6, None) ** p)) ** (1.0 / p)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(15, 5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.1], wspace=0.32)

    # (a) Synthetic 8×8 activation map (one channel) with an object peak
    W = 8
    xx, yy = np.meshgrid(np.arange(W), np.arange(W))
    obj = 3.0 * np.exp(-((xx - 2) ** 2 + (yy - 5) ** 2) / 1.5)
    bg = 0.4 + rng.normal(0, 0.15, size=(W, W))
    act = obj + bg
    act = np.clip(act, 0, None)

    ax = fig.add_subplot(gs[0, 0])
    im = ax.imshow(act, cmap="viridis", origin="lower")
    ax.set_title("(a) One channel of a CNN feature map\n"
                 "bright spot = object response, low background")
    ax.set_xticks([])
    ax.set_yticks([])
    plt.colorbar(im, ax=ax, fraction=0.046)

    # (b) Pooled scalar for each pooling type
    ax = fig.add_subplot(gs[0, 1])
    p_vals = [1.0, 2.0, 3.0, 5.0, 20.0]
    spoc = act.mean()
    mac = act.max()
    pooled = [gem(act, p) for p in p_vals]
    ax.plot(p_vals, pooled, "o-", color="tab:blue", lw=2, markersize=9,
            label="GeM$(p)$")
    ax.axhline(spoc, color="tab:green", ls="--", lw=2,
               label=f"SPoC (mean) = {spoc:.2f}")
    ax.axhline(mac, color="tab:red", ls="--", lw=2,
               label=f"MAC (max) = {mac:.2f}")
    ax.set_xlabel("GeM exponent $p$")
    ax.set_ylabel("pooled value")
    ax.set_xscale("log")
    ax.set_title("(b) GeM interpolates SPoC ($p=1$) ↔ MAC ($p\\to\\infty$)")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, which="both")

    # (c) GeM curves for two activations: peaky (object) vs flat (background)
    ax = fig.add_subplot(gs[0, 2])
    p_vals = np.linspace(0.5, 30, 80)
    peaky = rng.exponential(0.3, size=64)
    peaky[12] += 4.0
    flat = rng.normal(1.0, 0.15, size=64).clip(0)
    ax.plot(p_vals, [gem(peaky, p) for p in p_vals], lw=2.2,
            label="peaky channel (object)")
    ax.plot(p_vals, [gem(flat, p) for p in p_vals], lw=2.2,
            label="flat channel (background)")
    ax.set_xlabel("$p$")
    ax.set_ylabel("GeM$(p)$")
    ax.set_title("(c) GeM amplifies peaky activations as $p\\!\\uparrow$\n"
                 "background stays flat → larger separation")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    fig.suptitle("SPoC, MAC, GeM: translation-invariant global pooling of "
                 "CNN feature maps", fontsize=13, y=1.02)
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
