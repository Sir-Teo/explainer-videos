"""Lab 32: trend following is a long straddle: an exact identity, its skew, and when it pays."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import systematic

TITLE = "Why trend following has positive skew"
GOAL = ("Run the linear trend rule (hold what the market has done so far this month) on a random walk. Check the "
        "identity P = (S^2 - Q)/2, the skewness it implies, and the mean profit once returns are autocorrelated.")
TASKS = [
    "Lengthen the block from one month to one year. What happens to the skewness of yearly P&L built from months?",
    "Make the autocorrelation negative (-0.05). Who is on the other side of the trend follower now?",
    "Add volatility targeting with systematic.vol_target and compare the left tails.",
]


def ar1(n, rho, seed):
    rng = np.random.default_rng(seed)
    e = rng.normal(0, 0.01 * np.sqrt(1 - rho ** 2), n)
    r = np.empty(n)
    r[0] = e[0]
    for t in range(1, n):
        r[t] = rho * r[t - 1] + e[t]
    return r


def run(seed=0):
    n = 21
    walk = ar1(21 * 20000, 0.0, seed)
    S, Q, P = systematic.linear_trend_blocks(walk, n)
    skew = systematic.skewness(P)
    lab = labs.Lab()
    lab.row("Identity P = (S^2 - Q)/2", f"largest error {np.abs(P - (S ** 2 - Q) / 2).max():.1e}")
    lab.row("Random walk: mean monthly P&L", f"{1e4 * P.mean():+.3f} x 1e-4 (se {1e4 * P.std() / np.sqrt(P.size):.3f})")
    lab.row("Random walk: skewness of P&L", f"{skew:.2f}   (theory {systematic.trend_skew_theory(n):.2f})")
    lab.row("Share of months that lose", f"{100 * np.mean(P < 0):.0f}%")
    rho = 0.05
    trend = ar1(21 * 20000, rho, seed + 1)
    _, _, P2 = systematic.linear_trend_blocks(trend, n)
    acov = np.concatenate([[1e-4], 1e-4 * rho ** np.arange(1, n)])
    lab.row("Autocorrelation 0.05: mean P&L", f"{1e4 * P2.mean():+.3f} x 1e-4 (theory {1e4 * systematic.trend_mean_theory(acov, n):+.3f})")
    lab.note = ("The rule loses small in most months and wins big in a few: it buys realized variance of the "
                "month's return and pays the daily variance for it, like a straddle bought with daily hedges.")
    assert np.abs(P - (S ** 2 - Q) / 2).max() < 1e-12 and abs(P.mean()) < 4 * P.std() / np.sqrt(P.size)
    assert abs(skew - systematic.trend_skew_theory(n)) < 0.25 and np.mean(P < 0) > 0.55
    assert abs(P2.mean() - systematic.trend_mean_theory(acov, n)) < 4 * P2.std() / np.sqrt(P2.size)

    fig, ax = labs.figure(2, size=(11, 4.2))
    pick = np.random.default_rng(seed).choice(P.size, 3000, replace=False)
    ax[0].scatter(100 * S[pick], 1e4 * P[pick], s=4, color=labs.SPOT, alpha=0.5)
    s = np.linspace(-0.16, 0.16, 100)
    ax[0].plot(100 * s, 1e4 * (s ** 2 - n * 1e-4) / 2, color=labs.P, label="(S^2 - E[Q]) / 2: a straddle's payoff")
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title="The trend rule's month against the market's month", xlabel="market return in the month, %",
              ylabel="trend P&L (x 1e-4)")
    ax[0].legend(fontsize=8)
    bins = np.linspace(-15, 60, 90)
    ax[1].hist(1e4 * P, bins=bins, color=labs.CASH, alpha=0.8, label=f"random walk (skew {skew:.1f})")
    ax[1].hist(1e4 * P2, bins=bins, color=labs.GAIN, alpha=0.6, label="autocorrelation 0.05")
    ax[1].set_yscale("log")
    ax[1].set(title="Monthly trend P&L: many small losses, a long right tail", xlabel="P&L (x 1e-4)")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
