"""Lab 33: bet a thousand fortunes at four Kelly fractions, and test Allais's choices against every utility."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import decision as dec

TITLE = "Kelly's fraction, Allais's choices and Good's theorem"
GOAL = ("Simulate a thousand bettors staking a fixed fraction of their wealth on a 60% coin and compare the median "
        "fortune with the growth rate g(f); then check that no utility of a million makes expected utility pick "
        "Allais's common choices, and that free information never hurts an expected-utility maximizer.")
TASKS = [
    "Bet half the Kelly fraction (f = 0.1) and twice it (f = 0.4). Compare the growth rates and the spread of the "
    "final fortunes, and say why practitioners bet a fraction of Kelly.",
    "In dec.reu, replace r(p) = p**2 by r(p) = p. Does the risk-weighted agent still show Allais's pattern, and "
    "why not?",
    "Change the coin to p = 0.52. What is the Kelly fraction now, and how many bets does the median bettor need "
    "to double her money?",
]


def run(seed=0):
    lab = labs.Lab()
    p, bets, paths = 0.6, 1000, 1000
    fractions = (0.1, 0.2, 0.4, 0.6)
    k = dec.kelly(p=p, bets=bets, paths=paths, fractions=fractions, seed=1956 + seed)
    g = lambda f: p * math.log1p(f) + (1 - p) * math.log1p(-f)  # noqa: E731
    lab.row("Kelly fraction f* = 2p - 1", f"{k['f_star']}")
    medians = {}
    for f in fractions:
        r = k["by_f"][str(f)]
        theory = bets * g(f) / math.log(10)
        step_sd = math.sqrt(p * (1 - p)) * (math.log1p(f) - math.log1p(-f))
        se = 1.2533 * step_sd * math.sqrt(bets) / math.sqrt(paths) / math.log(10)   # s.e. of a median, in log10
        medians[f] = r["median_log10"]
        lab.row(f"f = {f}: median log10 wealth", f"{r['median_log10']:+.2f}   (1000 g(f) / ln 10 = {theory:+.2f}; "
                f"log10 of the mean {r['mean_log10_of_mean']:+.1f}; below 1% of the stake: {r['ruined']})")
        assert abs(r["median_log10"] - theory) < 4 * se + 0.05, "the typical fortune grows at the rate g(f)"
    assert medians[0.2] == max(medians.values()), "the Kelly fraction has the best typical outcome"
    assert k["by_f"]["0.6"]["ruined"] > 0.95 * paths and k["by_f"]["0.6"]["mean_log10_of_mean"] > 40, \
        "at three times Kelly nearly everyone is ruined while expected wealth explodes"
    assert g(0.4) < g(0.2) / 4 and g(0.6) < 0, "growth is about zero near twice Kelly and negative beyond"

    al = dec.allais()
    lab.row("utilities of a million that give 1A and 2B under EU", f"{al['both_ok']} of {al['grid']}")
    lab.row("risk-weighted utility, r(p) = p^2, u(1M) = 0.8", "  ".join(f"{n} {v:.4f}" for n, v in al["reu"].items()))
    assert al["both_ok"] == 0, "EU(1A) - EU(1B) = EU(2A) - EU(2B) for every utility"
    for u1 in np.linspace(0, 1, 11):
        u = {0: 0.0, 1: float(u1), 5: 1.0}.get
        d1 = dec.eu(dec.ALLAIS["1A"], u) - dec.eu(dec.ALLAIS["1B"], u)
        d2 = dec.eu(dec.ALLAIS["2A"], u) - dec.eu(dec.ALLAIS["2B"], u)
        assert abs(d1 - d2) < 1e-12 and abs(d1 - (0.11 * u1 - 0.10)) < 1e-12
    assert al["reu_pattern"], "risk-weighted utility does represent the common choices"

    good = dec.good_theorem(problems=1000, seed=1967 + seed)
    lab.row("value of a free test in 1000 random problems", f"negative in {good['negative']}, positive in "
            f"{good['positive']}, smallest {round(good['min_voi'], 6) + 0.0:.6f}")
    assert good["negative"] == 0 and good["positive"] > 100, "Good's theorem"
    lab.note = ("Maximizing expected wealth says stake everything; the typical bettor is governed by the growth "
                "rate g(f), which peaks at 2p - 1 and turns negative past about twice that. Allais's common "
                "choices contradict expected utility for every utility function, not for some.")

    fig, ax = labs.figure(2, size=(11.5, 4.4))
    fs = np.array([c[0] for c in k["g_curve"]])
    ax[0].plot(fs, [bets * c[1] / math.log(10) for c in k["g_curve"]], color=labs.BLUE,
               label="theory: 1000 g(f) / ln 10")
    ax[0].plot(fractions, [medians[f] for f in fractions], "o", color=labs.GOLD, label="median of 1000 bettors")
    ax[0].axvline(k["f_star"], color=labs.GREEN, ls="--", label="f* = 2p - 1")
    ax[0].axhline(0, color=labs.MUTED, lw=1)
    ax[0].set(title="Typical growth against the fraction staked", xlabel="fraction of wealth staked, f",
              ylabel="log10 of median wealth after 1000 bets")
    ax[0].legend(loc="lower left")
    t = np.arange(0, bets, 20)
    for f, color in zip(fractions, (labs.BLUE, labs.GREEN, labs.ORANGE, labs.RED)):
        for j, path in enumerate(k["by_f"][str(f)]["sample"][:3]):
            ax[1].plot(t, path, color=color, lw=1, alpha=0.85, label=f"f = {f}" if j == 0 else None)
    ax[1].axhline(0, color=labs.MUTED, lw=1)
    ax[1].set(title="Three fortunes at each fraction", xlabel="bets placed", ylabel="log10 wealth")
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
