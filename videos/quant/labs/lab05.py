"""Lab 5: quadratic variation piles up to T, and that is why Euler converges at one half and Milstein at one."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import sim

TITLE = "Quadratic variation, and the order of a simulation scheme"
GOAL = ("Watch the sum of squared Brownian increments settle on T as the grid is refined, then measure the strong "
        "error of Euler and Milstein on geometric Brownian motion against the exact solution on the same path.")
TASKS = [
    "Compute the sum of |dW| (first variation) on the same grids. Where does it go?",
    "Run sim.scheme_orders with sigma = 0.8. Which scheme's constant suffers more?",
    "Simulate sim.fbm(H=0.1, ...) and repeat the quadratic-variation plot. What does it do, and why?",
]


def run(seed=0):
    T = 1.0
    dW, _ = sim.brownian(T, 2 ** 14, 200, seed=seed)
    levels = 2 ** np.arange(3, 15)
    qv = np.array([[np.sum(path.reshape(n, -1).sum(1) ** 2) for n in levels] for path in dW])
    orders = sim.scheme_orders(seed=seed)
    lab = labs.Lab()
    lab.row("Quadratic variation, n = 8", f"{qv[:, 0].mean():.3f} +- {qv[:, 0].std():.3f} across paths")
    lab.row("Quadratic variation, n = 16,384", f"{qv[:, -1].mean():.3f} +- {qv[:, -1].std():.3f}   (theory: T = 1, "
                                               f"sd sqrt(2/n) = {np.sqrt(2 / levels[-1]):.3f})")
    lab.row("Strong order, Euler", f"{orders['slope_strong_euler']:.2f}   (theory 0.5)")
    lab.row("Strong order, Milstein", f"{orders['slope_strong_milstein']:.2f}   (theory 1.0)")
    lab.note = "Milstein adds the (dW^2 - dt) term that Ito's lemma says cannot be dropped."
    assert abs(qv[:, -1].mean() - T) < 0.01 and abs(qv[:, -1].std() - np.sqrt(2 / levels[-1])) < 0.004
    assert abs(orders["slope_strong_euler"] - 0.5) < 0.1 and abs(orders["slope_strong_milstein"] - 1.0) < 0.1

    fig, ax = labs.figure(2, size=(11, 4.2))
    for row in qv[:40]:
        ax[0].plot(levels, row, color=labs.SPOT, lw=0.6, alpha=0.5)
    ax[0].axhline(T, color=labs.P, ls="--")
    ax[0].set_xscale("log", base=2)
    ax[0].set(title="Sum of squared increments, 40 paths", xlabel="number of steps n", ylabel="quadratic variation")
    ns = np.asarray(orders["n"])
    ax[1].loglog(T / ns, orders["strong_euler"], "o-", color=labs.LOSS, label=f"Euler, slope {orders['slope_strong_euler']:.2f}")
    ax[1].loglog(T / ns, orders["strong_milstein"], "o-", color=labs.GAIN,
                 label=f"Milstein, slope {orders['slope_strong_milstein']:.2f}")
    ax[1].set(title="Strong error E|X_T - S_T| on GBM", xlabel="step dt", ylabel="error")
    ax[1].legend()
    lab.fig = fig
    return lab
