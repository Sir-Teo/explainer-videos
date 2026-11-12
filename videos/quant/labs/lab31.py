"""Lab 31: the fundamental law, when the IC moves, and what size does to a strategy."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import riskmodel

TITLE = "From IC to information ratio to capacity"
GOAL = ("Simulate a long-short book with a small information coefficient across N stocks. Check the fundamental "
        "law, see it fail when the IC varies from day to day, then charge square-root impact and find the size "
        "at which the strategy earns the most dollars.")
TASKS = [
    "Double the turnover. What happens to capacity, and to the Sharpe ratio at capacity?",
    "Set the transfer coefficient to 0.4 (a long-only book). How many stocks buy the lost IR back?",
    "Use riskmodel.gp_trade_rate: how fast should you trade toward the target when costs are quadratic?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    ic, T = 0.02, 2000
    Ns = np.array([50, 200, 800, 3200])
    lab = labs.Lab()
    sim = {0.0: [], 0.04: []}
    for N in Ns:
        for sd in sim:
            ir, _ = riskmodel.simulate_ic_strategy(int(N), T, ic, sd, rng)
            sim[sd].append(ir * np.sqrt(252))
        law = riskmodel.fundamental_ir(ic, N) * np.sqrt(252)
        tv = riskmodel.ir_time_varying(ic, 0.04, int(N)) * np.sqrt(252)
        lab.row(f"N = {N:>4} stocks", f"IC sqrt(N): {law:5.2f}   simulated {sim[0.0][-1]:5.2f}   |   IC with sd 0.04: "
                                      f"formula {tv:5.2f}, simulated {sim[0.04][-1]:5.2f}")
    assert all(abs(s - riskmodel.fundamental_ir(ic, n) * np.sqrt(252)) < 0.25 * s + 0.5 for s, n in zip(sim[0.0], Ns))
    assert sim[0.04][-1] < 0.5 * sim[0.0][-1], "a varying IC caps the information ratio at E[IC]/sd(IC)"

    # capacity: gross alpha 6% a year on capital, the book turns over 20x a year, impact Y sigma sqrt(Q/ADV)
    gross, turnover, sigma_d, adv_total = 0.06, 20.0, 0.02, 2e10
    aum = np.logspace(7, 10.5, 200)
    daily_trade = aum * turnover / 252
    cost = turnover * riskmodel.sqrt_impact(daily_trade, adv_total, sigma_d)
    net = gross - cost
    dollars = net * aum
    i = int(np.argmax(dollars))
    j = int(np.argmin(np.abs(net)))
    lab.row("Capacity (most dollars earned)", f"AUM ${aum[i] / 1e9:.2f}bn: net {100 * net[i]:.1f}% a year, ${dollars[i] / 1e6:.0f}m")
    lab.row("Alpha gone", f"AUM ${aum[j] / 1e9:.2f}bn")
    lab.note = ("With square-root impact, costs grow like the square root of size: dollars peak where costs take "
                "two thirds of the gross alpha, long before the alpha is gone.")
    assert abs(net[i] / gross - 1 / 3) < 0.03

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.logspace(1.5, 3.6, 60)
    ax[0].loglog(grid, [riskmodel.fundamental_ir(ic, n) * np.sqrt(252) for n in grid], color=labs.P, label="IC sqrt(N)")
    ax[0].loglog(grid, [riskmodel.ir_time_varying(ic, 0.04, int(n)) * np.sqrt(252) for n in grid], color=labs.LOSS,
                 label="IC varies: E[IC]/sqrt(sd^2 + 1/N)")
    ax[0].loglog(Ns, sim[0.0], "o", color=labs.P)
    ax[0].loglog(Ns, sim[0.04], "o", color=labs.LOSS)
    ax[0].set(title="Annual information ratio against breadth (IC = 0.02)", xlabel="stocks, N")
    ax[0].legend(fontsize=8)
    ax[1].semilogx(aum / 1e9, 100 * net, color=labs.SPOT, label="net return, % a year")
    ax2 = ax[1].twinx()
    ax2.semilogx(aum / 1e9, dollars / 1e6, color=labs.GAIN, label="dollars earned, $m")
    ax2.grid(False)
    ax2.set_ylim(0, None)
    ax[1].axvline(aum[i] / 1e9, color=labs.P, ls="--", lw=1)
    ax[1].set(title="Size against return: capacity", xlabel="assets under management, $bn", ylim=(0, 6.2))
    ax[1].legend(loc="upper left", fontsize=8)
    ax2.legend(loc="upper right", fontsize=8)
    lab.fig = fig
    return lab
