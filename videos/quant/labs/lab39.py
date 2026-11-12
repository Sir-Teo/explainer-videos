"""Lab 39: what a liquidity provider in a constant-product pool loses, and what fees must repay."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import defi, paths

TITLE = "An AMM's liquidity provider: loss versus rebalancing"
GOAL = ("Run a constant-product pool against a simulated market for a year, with arbitrageurs trading it to the "
        "market price every block. Compare the provider's loss with the closed form sigma^2/8 per unit time, with "
        "impermanent loss, and with the fees a 0.3% pool collects from the same arbitrage.")
TASKS = [
    "Lengthen the block from 12 seconds to 10 minutes. Who gets the difference?",
    "Concentrate the liquidity (L, pa, pb in defi.arb_pool) around the price. What scales, and by how much?",
    "Find the volume of uninformed trades that makes a 0.3% pool break even at 80% volatility.",
]


def run(seed=0):
    sigma, T, n = 0.8, 1.0, 100000
    t, S = paths.gbm(1.0, 0.0, sigma, T, n, 1, seed=seed)
    p = S[0]
    free = defi.arb_pool(p, fee=0.0, k=1.0)
    lvr = float(free["lvr"][-1])  # the pool's outputs are cumulative, one entry per block
    V0 = float(defi.cpmm_value(1.0, p[0]))
    theory = sigma ** 2 / 8 * np.mean(defi.cpmm_value(1.0, p)) * T
    il = float(defi.impermanent_loss(p[-1] / p[0]))
    fee = defi.arb_pool(p, fee=0.003, k=1.0)
    fees, lvr_fee = float(fee["fees"][-1]), float(fee["lvr"][-1])
    lab = labs.Lab()
    lab.row("Price moved by a factor", f"{p[-1] / p[0]:.2f}: impermanent loss {100 * il:.2f}% of holding")
    lab.row("Loss versus rebalancing, no fee", f"{100 * lvr / V0:.2f}% of the pool   (sigma^2/8 x time: {100 * theory / V0:.2f}%)")
    lab.row("With a 0.3% fee", f"arbitrageurs trade in {100 * fee['p_trade']:.1f}% of blocks; fees collected "
                               f"{100 * fees / V0:.2f}% against a loss of {100 * lvr_fee / V0:.2f}%")
    lab.note = ("Impermanent loss depends on where the price ends; loss versus rebalancing accrues every block "
                "whether or not it comes back. It is the price of quoting stale prices to arbitrageurs.")
    assert abs(lvr - theory) < 0.05 * theory and 0 < fees < lvr_fee <= lvr * 1.02

    fig, ax = labs.figure(2, size=(11, 4.2))
    r = np.linspace(0.2, 5, 300)
    ax[0].plot(r, 100 * defi.impermanent_loss(r), color=labs.LOSS)
    ax[0].plot(p[-1] / p[0], 100 * il, "o", color=labs.P)
    ax[0].set_xscale("log")
    ax[0].set(title="Impermanent loss against the price ratio", xlabel="final price / initial price", ylabel="% against holding")
    step = n // 1000
    ax[1].plot(t[::step], 100 * free["lvr"][::step] / V0, color=labs.LOSS, label="loss versus rebalancing (no fee)")
    ax[1].plot(t, 100 * sigma ** 2 / 8 * np.cumsum(defi.cpmm_value(1.0, p)) * (T / n) / V0, color=labs.P, ls="--",
               label="integral of sigma^2/8 x pool value")
    ax[1].plot(t[::step], 100 * fee["fees"][::step] / V0, color=labs.GAIN, label="fees at 0.3% (arbitrage only)")
    ax[1].set(title="A year in the pool, in % of its starting value", xlabel="years")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
