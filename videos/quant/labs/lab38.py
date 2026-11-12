"""Lab 38: the market maker's spread as the price of being sniped, and quotes that lean on inventory."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import making

TITLE = "The speed race sets the spread"
GOAL = ("A liquidity provider earns the half-spread from investors and loses to snipers whenever the value jumps "
        "before it can cancel. Simulate its profit across spreads, find the zero-profit spread, compare it with "
        "Budish, Cramton and Shim's formula, then replace the continuous book with batch auctions.")
TASKS = [
    "Go from 5 to 50 fast traders. Does the equilibrium spread change? Does anyone's total profit?",
    "Double the rate of investor arrivals. Who gains: investors, the provider or the snipers?",
    "Use making.glft to quote with inventory: by how much should a maker long 5 units shade both quotes?",
]


def run(seed=0):
    lam_invest, lam_jump, J, N, T = 10.0, 2.0, 1.0, 5, 4000.0
    s_star = making.bcs_spread(lam_invest, lam_jump, J)
    halves = np.linspace(0.05, 0.4, 15)
    lp = np.array([making.bcs_simulate(h, lam_invest, lam_jump, J, N, T, seed=seed)["lp"] for h in halves])
    sn = np.array([making.bcs_simulate(h, lam_invest, lam_jump, J, N, T, seed=seed)["sniper"] for h in halves])
    zero = float(np.interp(0.0, lp - sn, halves))  # the provider is indifferent between quoting and sniping
    batch = making.bcs_simulate(0.02, lam_invest, lam_jump, J, N, T, seed=seed, batch=0.1)
    lab = labs.Lab()
    lab.row("Equilibrium half-spread, formula", f"{s_star:.4f}   (lam_jump J / (lam_invest + lam_jump))")
    lab.row("Where quoting pays what sniping pays", f"{zero:.4f}   (simulated, {N} equally fast firms)")
    eq = making.bcs_simulate(s_star, lam_invest, lam_jump, J, N, T, seed=seed)
    lab.row("At equilibrium: per unit time", f"provider {eq['lp']:+.3f}, each sniper {eq['sniper']:+.3f}; investors pay "
                                             f"{lam_invest * s_star:.3f}")
    lab.row("Batch auctions, half-spread 0.02", f"provider {batch['lp']:+.3f}, each sniper {batch['sniper']:+.3f}")
    g = making.glft(A=10.0, k=5.0, sigma=0.5, gamma=0.5)
    lab.row("GLFT quotes", f"half-spread {g['half_spread']:.3f} at zero inventory; shade by {g['skew']:.3f} per unit held")
    lab.note = ("Investors pay the spread; the spread pays for the arms race. With batch auctions a stale quote "
                "is never hit, so the sniping tax and most of the spread disappear.")
    assert abs(zero - s_star) < 0.02 and abs(eq["lp"] - eq["sniper"]) < 0.08 and abs(batch["sniper"]) < 1e-9

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(halves, lp, "o-", color=labs.GAIN, ms=4, label="liquidity provider")
    ax[0].plot(halves, sn, "o-", color=labs.LOSS, ms=4, label="each sniper")
    ax[0].axvline(s_star, color=labs.P, ls="--", lw=1)
    ax[0].text(s_star + 0.005, ax[0].get_ylim()[0] + 0.1, "formula", color=labs.P, fontsize=8)
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title="Profit per unit time against the quoted half-spread", xlabel="half-spread")
    ax[0].legend(fontsize=8)
    q = np.arange(-8, 9)
    ax[1].plot(q, g["half_spread"] - g["skew"] * q, "o-", color=labs.LOSS, ms=4, label="ask distance")
    ax[1].plot(q, -(g["half_spread"] + g["skew"] * q), "o-", color=labs.GAIN, ms=4, label="bid distance")
    ax[1].axhline(0, color=labs.MUTED, lw=0.8)
    ax[1].set(title="Optimal quotes lean against inventory (GLFT)", xlabel="inventory", ylabel="quote minus fair value")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
