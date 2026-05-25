# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""KCF/DCF: target template, cyclic-shift training data, response map."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "q_0035_kcf.png"
rng = np.random.default_rng(53)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    N = 33
    # Make a target patch (Gaussian blob with a dark dot offset)
    yy, xx = np.mgrid[:N, :N]
    target = np.exp(-((xx - N // 2) ** 2 + (yy - N // 2) ** 2) / 28.0)
    target += 0.4 * np.exp(-((xx - N // 2 - 4) ** 2 + (yy - N // 2 + 3) ** 2) / 8.0)

    # Cosine window
    win = np.outer(np.hanning(N), np.hanning(N))
    target_w = target * win

    # Desired Gaussian response y (peak in centre)
    y = np.exp(-((xx - N // 2) ** 2 + (yy - N // 2) ** 2) / 12.0)

    # Closed-form MOSSE filter in Fourier
    eps = 1e-2
    X = np.fft.fft2(target_w)
    Y = np.fft.fft2(y)
    W_hat = np.conj(X) * Y / (np.conj(X) * X + eps)
    w = np.fft.ifft2(W_hat).real

    # Search window with the target shifted
    shift = (5, -3)
    search = np.zeros_like(target)
    sx, sy = shift
    rolled = np.roll(np.roll(target, sx, axis=0), sy, axis=1)
    # Add noise / background structure
    search = rolled + 0.1 * rng.standard_normal(size=target.shape)
    search_w = search * win
    Z = np.fft.fft2(search_w)
    resp = np.fft.fftshift(np.fft.ifft2(np.conj(W_hat) * Z).real)

    fig, axes = plt.subplots(1, 4, figsize=(15, 4.2))

    axes[0].imshow(target, cmap="gray")
    axes[0].set_title("(a) Target template $\\mathbf{x}$")
    axes[0].set_xticks([]); axes[0].set_yticks([])

    axes[1].imshow(np.fft.fftshift(w), cmap="seismic",
                   vmin=-abs(w).max(), vmax=abs(w).max())
    axes[1].set_title("(b) Learned filter $\\mathbf{w}$\n"
                      "(closed-form ridge regression in FFT domain)")
    axes[1].set_xticks([]); axes[1].set_yticks([])

    axes[2].imshow(search, cmap="gray")
    axes[2].set_title(f"(c) Search window $\\mathbf{{z}}$\n"
                      f"(target translated by {shift})")
    axes[2].set_xticks([]); axes[2].set_yticks([])

    im = axes[3].imshow(resp, cmap="hot")
    py, px = np.unravel_index(resp.argmax(), resp.shape)
    cy, cx = N // 2, N // 2
    axes[3].plot(px, py, "o", color="cyan", markersize=10, markeredgecolor="black")
    axes[3].set_title(f"(d) Response map (peak = new target pos)\n"
                      f"peak shift ($\\Delta y$,$\\Delta x$) = ({py-cy}, {px-cx})")
    axes[3].set_xticks([]); axes[3].set_yticks([])
    plt.colorbar(im, ax=axes[3], fraction=0.046)

    fig.suptitle("DCF/KCF: ridge-regression filter trained via FFT, "
                 "detection by cross-correlation peak", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=130, bbox_inches="tight")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
