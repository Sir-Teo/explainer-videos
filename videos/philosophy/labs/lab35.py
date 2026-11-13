"""Lab 35: feed a utility monster under three views, and find the noise at which calculating acts loses to a rule."""

import math

import numpy as np
from scipy.stats import norm

from videos.coursekit import labs
from explainer.philosophy.reasoner import ethics

TITLE = "The utility monster, and rules against calculation"
GOAL = ("Split 100 units between a utility monster and ten ordinary people under the utilitarian sum, a "
        "prioritarian sum and maximin, and check each split against its closed form; then compare an act "
        "utilitarian who misjudges promise cases with a rule follower and a two-level thinker, against the exact "
        "formula; and see moral uncertainty's verdict flip with the normalization.")
TASKS = [
    "Give the monster k = 100. What share does each view give it, and which view's share does not depend on "
    "the total at all?",
    "In ethics.two_level, raise the two-level thinker's bar (threshold) from 2 to 4, then lower it to 0.5. "
    "Where does each version stop beating the rule?",
    "In ethics.moral_uncertainty, set the credences to (0.2, 0.8). Which normalizations still say push?",
]


def act_value(noise, bias=0.0, bar=0.0, mu=-1.0):
    """Exact mean gain per case of breaking a promise when the estimate D + bias + noise * e exceeds the bar,
    D ~ N(mu, 1): E[D 1{Z > bar}] with Z ~ N(mu + bias, 1 + noise^2) and Cov(D, Z) = 1."""
    sd = math.sqrt(1 + noise ** 2)
    z = (mu + bias - bar) / sd
    return mu * norm.cdf(z) + norm.pdf(z) / sd


def run(seed=0):
    lab = labs.Lab()
    n, total = 10, 100
    closed = {  # the monster's share: equate marginal welfare on both sides of the split
        "utilitarian": lambda k: k ** 2 / (k ** 2 + n),
        "prioritarian": lambda k: k ** (2 / 3) / (k ** (2 / 3) + n),
        "maximin": lambda k: 1 / (1 + n * k ** 2),
    }
    for k in (1.0, 3.0, 10.0):
        m = ethics.utility_monster(total=total, k=k)
        got = {name: m["best"][name]["monster"] for name in closed}
        lab.row(f"k = {k:g}: units to the monster (sum, priority, maximin)",
                "  ".join(f"{got[name]:.1f}" for name in closed) + "   (closed forms "
                + "  ".join(f"{total * closed[name](k):.1f}" for name in closed) + ")")
        for name in closed:
            assert abs(got[name] - total * closed[name](k)) < 0.02, (name, k)
        assert abs(m["utilitarian_exact"] - total * closed["utilitarian"](k)) < 1e-3
    ten = ethics.utility_monster(k=10.0)["best"]
    assert ten["utilitarian"]["monster"] > 90 and ten["maximin"]["monster"] < 0.2, "the sum feeds it, maximin starves it"

    tl = ethics.two_level(n=200000, seed=1981 + seed)
    noises = np.array(tl["noises"])
    worst = 0.0
    for bias in (0.0, 0.5):
        c = tl["curves"][str(bias)]
        worst = max(worst, np.max(np.abs(np.array(c["act"]) - [act_value(s, bias) for s in noises])),
                    np.max(np.abs(np.array(c["two_level"]) - [act_value(s, bias, tl["threshold"]) for s in noises])))
    honest, selfish = tl["curves"]["0.0"], tl["curves"]["0.5"]
    lab.row("a perfect act utilitarian's gain per promise case", f"{tl['ideal']:.4f}   (exact {act_value(0):.4f})")
    lab.row("act utilitarian falls below the rule at noise", f"{honest['act_below_rule_at']} unbiased, "
            f"{selfish['act_below_rule_at']} self-serving   (film: 0.9, 0.5)")
    lab.row("largest gap between simulation and formula", f"{worst:.4f}")
    two_at = dict(zip(tl["noises"], honest["two_level"]))
    lab.row("two-level thinker at noise 1.5", f"{two_at[1.5]:+.4f}   (the rule: 0)")
    assert abs(tl["ideal"] - act_value(0)) < 0.004 and worst < 0.006, "the simulation matches the closed form"
    assert honest["act_below_rule_at"] in (0.9, 1.0) and selfish["act_below_rule_at"] in (0.5, 0.6)
    assert all(v > 0 for s, v in two_at.items() if s <= 1.5), "the high bar keeps the two-level thinker ahead"

    mu = ethics.moral_uncertainty()
    two = {k: v["choice"] for k, v in mu["two"]["results"].items()}
    three = {k: v["choice"] for k, v in mu["three"]["results"].items()}
    lab.row("footbridge, credence 0.6 / 0.4: raw, range, variance", f"{two['raw']}; {two['range']}; {two['variance']}")
    lab.row("with a warning shout added: the three methods; a vote", f"{three['raw']} every time; {three['plurality']}")
    assert two["raw"] == "do nothing" and two["range"] == two["variance"] == "push", "the verdict flips"
    assert {three[k] for k in ("raw", "range", "variance")} == {"shout a warning"} and three["plurality"] == "push"
    lab.note = ("The sum gives the monster k^2/(k^2 + n) of everything; priority and maximin give it less for the "
                "same reason they give the worse off more. Calculating each case beats a rule only while the "
                "estimates are accurate and unbiased; a high bar for exceptions keeps most of the gain.")

    fig, ax = labs.figure(2, size=(11.5, 4.4))
    ks = np.logspace(0, 2, 80)
    for name, color in (("utilitarian", labs.RED), ("prioritarian", labs.GOLD), ("maximin", labs.BLUE)):
        ax[0].plot(ks, [100 * closed[name](k) for k in ks], color=color, label=name)
        ax[0].plot([1, 3, 10], [ethics.utility_monster(k=k)["best"][name]["monster"] for k in (1.0, 3.0, 10.0)], "o",
                   color=color, ms=5)
    ax[0].set(title="The monster's share of 100 units, ten others", xlabel="the monster's efficiency k",
              ylabel="units given to the monster", xscale="log")
    ax[0].legend(loc="upper left")
    ax[1].plot(noises, honest["act"], "o", ms=3, color=labs.BLUE, label="act utilitarian, unbiased")
    ax[1].plot(noises, selfish["act"], "o", ms=3, color=labs.RED, label="act utilitarian, self-serving")
    ax[1].plot(noises, honest["two_level"], "o", ms=3, color=labs.GREEN, label="two-level thinker")
    for bias, bar, color in ((0.0, 0.0, labs.BLUE), (0.5, 0.0, labs.RED), (0.0, tl["threshold"], labs.GREEN)):
        ax[1].plot(noises, [act_value(s, bias, bar) for s in noises], color=color, lw=1)
    ax[1].axhline(0, color=labs.MUTED, ls="--", label="always keep the promise")
    ax[1].set(title="Gain per promise case (lines: exact)", xlabel="noise in the estimate of the gain",
              ylabel="mean value against keeping every promise")
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
