"""Lab 2: one path, four leverages: who is liquidated, where, and what is left."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import funding, paths

TITLE = "Margin, leverage and the liquidation price"
GOAL = ("Open the same long at 2x, 3x, 5x and 10x on one simulated path with a crash; let the House's margin "
        "account mark it to market bar by bar, and check the closed-form liquidation price and probability.")
TASKS = [
    "Make it a short (qty = -1) and move the crash to a squeeze. Which side has the bounded loss?",
    "Charge funding of 0.01% a bar (funding=np.full(n, 1e-4)): how much sooner does 10x go?",
    "Plot funding.liquidation_probability against leverage for 5, 20 and 60 days.",
]


def run(seed=0):
    n, sigma = 240, 0.035  # hourly bars over ten days; daily volatility 3.5%
    t, S = paths.gbm(100.0, 0.0, sigma * np.sqrt(365), 10 / 365, n, 1, seed=seed + 2)
    p = S[0].copy()
    p[150:] *= np.linspace(1.0, 0.72, 16).tolist() + [0.72] * (n + 1 - 166)  # an illustrative 28% slide
    lab, m = labs.Lab(), 0.005
    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(p, color=labs.SPOT)
    colors = [labs.GAIN, labs.P, labs.IMPLIED, labs.LOSS]
    for lev, c in zip((2, 3, 5, 10), colors):
        acct = funding.margin_account(p, qty=1.0, leverage=lev, maintenance=m)
        liq_px = funding.liquidation_price(p[0], lev, m)
        i = acct["liquidated_at"]
        ax[0].axhline(liq_px, color=c, lw=0.9, ls="--")
        ax[0].text(n, liq_px, f" {lev}x", color=c, va="center", fontsize=9)
        ax[1].plot(acct["equity"] / acct["initial_margin"], color=c, label=f"{lev}x")
        if i is None:
            lab.row(f"{lev}x", f"liquidation price {liq_px:6.2f}   survives; equity x{acct['left'] / acct['initial_margin']:.2f}")
            assert p.min() >= liq_px * (1 - 1e-9)
        else:
            ax[0].plot(i, p[i], "x", color=c, ms=8)
            lab.row(f"{lev}x", f"liquidation price {liq_px:6.2f}   liquidated at bar {i} (price {p[i]:.2f}); "
                               f"left {100 * acct['left'] / acct['initial_margin']:+.1f}% of margin")
            assert p[i] < liq_px <= p[:i].min() + 1e-9, "liquidated at the first bar below the liquidation price"
    prob = funding.liquidation_probability(np.array([2, 3, 5, 10]), 10, sigma, m)
    lab.row("P(liquidated in 10 days)", "  ".join(f"{lev}x {100 * q:.1f}%" for lev, q in zip((2, 3, 5, 10), prob)))
    lab.note = "Driftless Brownian log price, reflection principle. Leverage chooses the distance to the barrier."
    ax[0].set(title="One path, four liquidation prices", xlabel="hour", ylabel="price")
    ax[1].axhline(0, color=labs.MUTED, lw=0.8)
    ax[1].set(title="Equity as a multiple of the margin posted", xlabel="hour")
    ax[1].legend(ncols=4)
    lab.fig = fig
    return lab
