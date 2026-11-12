"""Lab 22: carry: the forward curve of a commodity, the roll, and the currency that pays more."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import macro

TITLE = "Carry: the forward curve and what the roll pays"
GOAL = ("Build a commodity's forward curve from financing, storage and convenience yield; hold the front "
        "contract and roll it for a year while the spot goes nowhere; then run a carry trade across simulated "
        "currencies whose forwards obey covered parity and whose spots ignore uncovered parity.")
TASKS = [
    "Set storage to 30% a year with nowhere left to put the oil. What does the front contract do near expiry?",
    "Make uncovered parity hold (drift = interest differential). What happens to the carry trade's Sharpe ratio?",
    "Add a crash: once every five years the high-yield currencies fall 10% together. Recompute crash_stats.",
]


def run(seed=0):
    S, r, storage = 80.0, 0.04, 0.03
    T = np.arange(0, 25) / 12
    lab = labs.Lab()
    curves = {}
    for name, y in (("contango (convenience 0%)", 0.0), ("flat (7%)", 0.07), ("backwardation (15%)", 0.15)):
        F = macro.carry_forward(S, T, r, storage, y)
        curves[name] = F
        implied = round(float(macro.implied_convenience(F[1], F[2], 1 / 12, r, storage)), 12)
        roll = np.prod(np.full(12, S / F[1])) - 1  # buy the one-month future, it converges to an unchanged spot
        lab.row(name, f"12-month future {F[12]:.2f}   implied convenience {100 * implied + 0.0:.1f}%   "
                      f"rolling the front for a year: {100 * roll:+.1f}%")
        assert abs(implied - y) < 1e-9 and abs(roll - (np.exp(y - r - storage) - 1)) < 1e-9

    # ten currencies: interest differentials persist, spot changes are noise (uncovered parity fails)
    rng = np.random.default_rng(seed)
    months, n = 360, 10
    diff = np.zeros((months, n))
    diff[0] = rng.normal(0, 0.03, n)
    for t in range(1, months):
        diff[t] = 0.98 * diff[t - 1] + rng.normal(0, 0.03 * np.sqrt(1 - 0.98 ** 2), n)
    spot_change = rng.normal(0, 0.10 / np.sqrt(12), (months, n))
    excess = diff / 12 + spot_change  # the forward discount earned, plus the spot move
    carry = macro.carry_sort(excess, diff, k=3)
    stats = macro.crash_stats(carry["ls"], per_year=12)
    lab.row("Carry trade, 3 high against 3 low", f"mean {100 * stats['mean']:.1f}% a year, volatility "
                                                 f"{100 * stats['vol']:.1f}%, Sharpe {stats['sharpe']:.2f}")
    lab.note = ("Carry is what you earn if prices do not move. Whether it is a premium or a forecast error is the "
                "question the part asks; here the spot was built to ignore the differential.")
    assert stats["sharpe"] > 0.4

    fig, ax = labs.figure(2, size=(11, 4.2))
    for (name, F), c in zip(curves.items(), (labs.LOSS, labs.CASH, labs.GAIN)):
        ax[0].plot(12 * T, F, "o-", ms=3, color=c, label=name)
    ax[0].axhline(S, color=labs.MUTED, ls=":", lw=1)
    ax[0].set(title="Forward curves from one spot price", xlabel="months to delivery", ylabel="futures price")
    ax[0].legend(fontsize=8)
    ax[1].plot(np.arange(months) / 12, np.cumsum(carry["ls"]), color=labs.P, label="carry: long high, short low")
    ax[1].plot(np.arange(months) / 12, np.cumsum(excess.mean(1)), color=labs.CASH, label="all currencies, equal weight")
    ax[1].set(title="Simulated currency carry", xlabel="years", ylabel="cumulative return")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
