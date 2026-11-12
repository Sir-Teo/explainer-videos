"""Lab 26: the best of N backtests of nothing, and the Sharpe ratio deflated for it."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import backtest

TITLE = "The best backtest of nothing, and the deflated Sharpe ratio"
GOAL = ("Backtest N strategies with no skill for five years and keep the best. Compare its Sharpe ratio with the "
        "expected-maximum formula, then deflate a reported Sharpe of 1.5 for the number of trials behind it.")
TASKS = [
    "How many years of data would make the best of 1,000 noise strategies look like a Sharpe of 1? (backtest.min_btl)",
    "Give the returns negative skew and fat tails (skew=-1, kurt=8) in deflated_sharpe. What happens?",
    "Split one noise sample in two halves and pick the in-sample best. What is its out-of-sample rank? (backtest.cscv)",
]


def run(seed=0):
    T = 5 * 252  # five years of daily returns
    ann = np.sqrt(252)
    ns = np.array([1, 10, 100, 1000, 10000])
    sim = [ann * backtest.noise_max_sr(int(n), T, sims=1000, seed=seed).mean() for n in ns]
    theory = [ann * backtest.expected_max_sr(float(n), 1 / T) if n > 1 else 0.0 for n in ns]
    lab = labs.Lab()
    for n, s, th in zip(ns, sim, theory):
        lab.row(f"Best of {n:>6,} skill-less strategies", f"annual Sharpe {s:.2f}   (formula {th:.2f})")
    sr = 1.5 / ann
    dsr = {int(n): backtest.deflated_sharpe(sr, T, float(n), 1 / T)["dsr"] if n > 1 else backtest.psr(sr, 0.0, T) for n in ns}
    lab.row("A reported Sharpe of 1.5: P(true Sharpe > 0)", "  ".join(f"N={n:,}: {100 * v:.0f}%" for n, v in dsr.items()))
    lab.note = ("Five years, one trial: 1.5 is convincing. After a thousand trials it is what noise is expected to "
                "produce. The trial count is part of the result.")
    assert all(abs(s - th) < 0.12 for s, th in zip(sim[1:], theory[1:])) and dsr[1] > 0.99 > 0.6 > dsr[1000]

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.logspace(0.31, 5, 100)
    ax[0].semilogx(grid, [ann * backtest.expected_max_sr(float(n), 1 / T) for n in grid], color=labs.P, label="expected maximum (formula)")
    ax[0].semilogx(ns, sim, "o", color=labs.SPOT, label="simulated")
    ax[0].axhline(1.5, color=labs.LOSS, ls="--", lw=1)
    ax[0].text(1.2, 1.54, "the reported 1.5", color=labs.LOSS, fontsize=8)
    ax[0].set(title="Best annual Sharpe among N noise strategies, 5 years", xlabel="strategies tried, N", ylabel="Sharpe ratio")
    ax[0].legend(fontsize=8)
    best = ann * backtest.noise_max_sr(1000, T, sims=3000, seed=seed + 1)
    one = ann * backtest.noise_max_sr(1, T, sims=3000, seed=seed + 2)
    bins = np.linspace(-1.5, 2.5, 80)
    ax[1].hist(one, bins=bins, color=labs.CASH, alpha=0.8, label="one strategy")
    ax[1].hist(best, bins=bins, color=labs.SPOT, alpha=0.8, label="the best of 1,000")
    ax[1].axvline(1.5, color=labs.LOSS, ls="--", lw=1)
    ax[1].set(title="Sharpe ratios that pure noise produces", xlabel="annual Sharpe ratio")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
