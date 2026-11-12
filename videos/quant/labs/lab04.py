"""Lab 4: you cannot beat a fair game: the doubling system, and gambler's ruin."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import martingale

TITLE = "The doubling system against a fair coin"
GOAL = ("Play the doubling system ten thousand times with a finite bankroll. Count the winners, weigh the ruins, "
        "and check the expected profit against optional stopping and the gambler's-ruin formula.")
TASKS = [
    "Give the house an edge (p = 18/37 on red). How does the mean change, and gamblers_ruin(a, b, p)?",
    "Raise the bankroll from 1,023 to 65,535. Does the share of winners change the expected profit?",
    "Replace doubling by martingale.system_stakes with another betting system and repeat.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    bankroll, target, n = 1023.0, 1123.0, 10000
    final, stopped, sample = np.empty(n), np.empty(n), []
    for i in range(n):
        out = martingale.doubling(rng.random(4000) < 0.5, base=1.0, bankroll=bankroll, target=target)
        final[i], stopped[i] = out["wealth"][-1], out["stopped"]
        if i < 60:
            sample.append(out["wealth"])
    profit = final - bankroll
    won = np.mean(final >= target)
    se = profit.std(ddof=1) / np.sqrt(n)
    ruin = martingale.gamblers_ruin(int(bankroll), int(target), 0.5)
    lab = labs.Lab()
    lab.row("Reached +100", f"{100 * won:.1f}% of {n:,} players   (fair-game bound a/b = {100 * ruin:.1f}%)")
    lab.row("Mean profit", f"{profit.mean():+.2f} +- {1.96 * se:.2f}   (optional stopping: exactly 0)")
    lab.row("Median profit; worst", f"{np.median(profit):+.0f}; {profit.min():+,.0f}")
    lab.note = ("Most players win a little, a few lose everything, and the mean is zero: a bounded-bankroll "
                "strategy on a martingale is a martingale.")
    assert abs(profit.mean()) < 3 * se and abs(won - ruin) < 0.02

    fig, ax = labs.figure(2, size=(11, 4.2))
    for w in sample:
        ax[0].plot(w, color=labs.LOSS if w[-1] < bankroll else labs.GAIN, lw=0.7, alpha=0.7)
    ax[0].axhline(target, color=labs.P, ls="--", lw=0.9)
    ax[0].set(title="Sixty players doubling after every loss", xlabel="round", ylabel="wealth")
    ax[1].hist(profit, bins=60, color=labs.SPOT)
    ax[1].set_yscale("log")
    ax[1].axvline(profit.mean(), color=labs.P, ls="--")
    ax[1].set(title="Profit: many +100s, a few -1,023s, mean zero", xlabel="profit", ylabel="players (log)")
    lab.fig = fig
    return lab
