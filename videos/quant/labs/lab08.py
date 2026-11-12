"""Lab 8: how much to bet: Kelly's fraction, half of it and twice it."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import control

TITLE = "How much to bet: Kelly, half Kelly, double Kelly"
GOAL = ("A coin pays even money and lands heads 55% of the time. Compute the growth rate of every fixed "
        "fraction, simulate a thousand bets at four of them, and see why nobody bets full Kelly on an estimate.")
TASKS = [
    "You only think p = 0.55; the truth is 0.52. What is full Kelly's growth rate now? Half Kelly's?",
    "Use control.merton_fraction for a stock with 6% excess return and 18% volatility at gamma = 1, 2, 5.",
    "Cap wealth (cap=100) as in the Haghani-Dewey experiment. How many paths reach the cap at each fraction?",
]


def run(seed=0):
    p, n_bets, n_paths = 0.55, 1000, 4000
    f_star = control.kelly_binary(p)
    names = {"half Kelly": 0.5 * f_star, "Kelly": f_star, "double Kelly": 2 * f_star, "triple Kelly": 3 * f_star}
    rng = np.random.default_rng(seed)
    wins = rng.random((n_paths, n_bets)) < p
    lab = labs.Lab()
    lab.row("Kelly fraction f* = 2p - 1", f"{f_star:.2f}")
    paths = {}
    for name, f in names.items():
        logw = np.cumsum(np.where(wins, np.log1p(f), np.log1p(-f)), axis=1)
        paths[name] = logw
        g = control.growth_binary(f, p)
        lab.row(name, f"f = {f:.2f}   growth {100 * g:+.3f}% a bet   median wealth x{np.exp(np.median(logw[:, -1])):,.3g}"
                      f"   paths below start {100 * np.mean(logw[:, -1] < 0):.0f}%")
        se = 1.25 * np.sqrt(p * (1 - p) * n_bets / n_paths) * np.log((1 + f) / (1 - f))
        assert abs(np.median(logw[:, -1]) - n_bets * g) < 4 * se, "the median path grows at the Kelly growth rate"
    lab.note = ("Double Kelly grows at about zero; beyond it the median path goes broke. Half Kelly keeps three "
                "quarters of the growth for half the risk.")
    g = {k: control.growth_binary(f, p) for k, f in names.items()}
    assert abs(g["double Kelly"]) < 5e-4 and g["triple Kelly"] < 0 and abs(g["half Kelly"] / g["Kelly"] - 0.75) < 0.01

    fig, ax = labs.figure(2, size=(11, 4.2))
    f = np.linspace(0, 0.33, 300)
    ax[0].plot(f, 100 * control.growth_binary(f, p), color=labs.P)
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    colors = dict(zip(names, (labs.GAIN, labs.P, labs.IMPLIED, labs.LOSS)))
    for name, ff in names.items():
        ax[0].plot(ff, 100 * control.growth_binary(ff, p), "o", color=colors[name])
        ax[0].annotate(name, (ff, 100 * control.growth_binary(ff, p)), textcoords="offset points", xytext=(4, 6),
                       color=colors[name], fontsize=9)
    ax[0].set(title="Growth rate per bet against the fraction staked", xlabel="fraction of wealth bet", ylabel="% a bet")
    t = np.arange(1, n_bets + 1)
    for name in names:
        q = np.percentile(paths[name], [10, 50, 90], axis=0) / np.log(10)
        ax[1].fill_between(t, q[0], q[2], color=colors[name], alpha=0.12, lw=0)
        ax[1].plot(t, q[1], color=colors[name], label=name)
    ax[1].set(title="Wealth over 1,000 bets: median and 10-90% band", xlabel="bet", ylabel="log10 wealth")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
