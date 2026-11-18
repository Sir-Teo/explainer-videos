"""Lab 1: run a double auction with traders who learn and traders who don't, and see what the rules do on their own."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import market as mk
from explainer.economics.island import truths

TITLE = "The pit: where the price comes from"
GOAL = ("Run the opening chapter's pit market many times, with traders who adjust their margins and with traders "
        "who bid at random, and measure two things each period: how far the prices stray from the competitive band, "
        "and how much of the possible gain is made.")
TASKS = [
    "Give the buyers' cards a wider spread (multiply the gaps between them by two). Do the learning traders still "
    "converge in three periods, and does the band get wider or narrower?",
    "Add a seller with a $1.00 card. Predict the new competitive quantity and band before you run it, then check "
    "the prices.",
    "Make the zero-intelligence traders' ceiling $10 instead of $5. What happens to their efficiency, and why does "
    "the ceiling matter for random sellers but not for random buyers?",
]


def run(seed=0):
    lab = labs.Lab()
    pit = truths(1)["pit"]
    m = mk.Market(values=pit["values"], costs=pit["costs"])
    eq = m.equilibrium()
    lab.row("competitive quantity and band", f"{eq['q']} units at ${eq['p_lo']:.2f} to ${eq['p_hi']:.2f}")
    lab.row("largest possible gain", f"${eq['surplus']:.2f}")
    assert eq["q"] == 6 and abs(eq["p_lo"] - 2.2) < 1e-9 and abs(eq["p_hi"] - 2.3) < 1e-9

    runs, periods = 30, 6
    out = {}
    for kind in ("zip", "zi"):
        alpha = np.zeros((runs, periods))
        eff = np.zeros((runs, periods))
        mean = np.zeros((runs, periods))
        for r in range(runs):
            res = mk.double_auction(m, kind, periods=periods, seed=1000 * seed + r)
            for k, p in enumerate(res["periods"]):
                alpha[r, k], eff[r, k], mean[r, k] = p["alpha"], p["efficiency"], p["mean"]
        out[kind] = (alpha, eff, mean)
    za, ze, zm = out["zip"]
    ia, ie, im = out["zi"]
    lab.row("learning traders: median alpha, period 1 and 6", f"{np.median(za[:, 0]):.1f}% and "
                                                                f"{np.median(za[:, -1]):.1f}%")
    lab.row("random traders: median alpha, period 1 and 6", f"{np.median(ia[:, 0]):.1f}% and "
                                                              f"{np.median(ia[:, -1]):.1f}%")
    lab.row("efficiency, last period: learning / random", f"{100 * ze[:, -1].mean():.1f}% / {100 * ie[:, -1].mean():.1f}%")
    lab.row("mean price, last period: learning traders", f"${np.median(zm[:, -1]):.3f}   (band ${eq['p_lo']:.2f} to "
                                                         f"${eq['p_hi']:.2f})")
    assert np.median(za[:, -1]) < np.median(za[:, 0]) / 2, "learning traders converge"
    assert np.median(ia[:, -1]) > 2 * np.median(za[:, -1]), "random traders do not"
    assert ie.mean() > 0.85, "but the rules alone capture most of the gain"
    assert 2.05 < np.median(zm[:, -1]) < 2.45
    lab.note = ("The rules of the double auction (no trade at a loss, the best bids and offers trade first) capture "
                "most of the possible gain even with random traders; learning is what makes the price settle.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    per = np.arange(1, periods + 1)
    for (a, e, _), color, name in ((out["zip"], labs.ORANGE, "traders who learn"),
                                   (out["zi"], labs.GREY, "zero intelligence")):
        ax[0].plot(per, np.median(a, axis=0), color=color, lw=2.2, label=name)
        ax[0].fill_between(per, np.percentile(a, 25, axis=0), np.percentile(a, 75, axis=0), color=color, alpha=0.2)
        ax[1].plot(per, 100 * e.mean(axis=0), color=color, lw=2.2, label=name)
    ax[0].set(title="How scattered are the prices? (Smith's alpha)", xlabel="period", ylabel="alpha, % of the price")
    ax[1].set(title="How much of the possible gain is made?", xlabel="period", ylabel="efficiency, %", ylim=(80, 101))
    ax[0].legend()
    lab.fig = fig
    return lab
