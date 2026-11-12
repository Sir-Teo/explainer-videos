"""Lab 43: two thousand funds, twenty years: how many of the winners were lucky?"""

import numpy as np
from scipy.stats import norm

from videos.quant import labs
from explainer.quant.house import skill

TITLE = "Skill or luck? Counting the funds with real alpha"
GOAL = ("Simulate two thousand funds of which three in four have no skill, most of the rest lose their fees and "
        "one in a hundred has real alpha. From the t-statistics alone, estimate the share with no skill (Storey) "
        "and split the significant funds into the skilled and the lucky (Barras, Scaillet and Wermers).")
TASKS = [
    "Shorten the record from 20 years to 5. How many truly skilled funds are still found?",
    "Make the funds' residuals correlated (they hold the same stocks). Is Storey's estimate still conservative?",
    "With skill.beat_prob: what is the chance a skill-less fund costing 1% beats the index over 10 years?",
]


def run(seed=0):
    shares, alphas = (0.75, 0.24, 0.01), (0.0, -0.032, 0.038)
    pop = skill.fund_population(m=2000, shares=shares, alphas=alphas, te=0.05, months=240, seed=seed)
    out = skill.bsw(pop["p"], pop["t"])
    truth = np.bincount(pop["group"], minlength=3) / len(pop["group"])
    winners = pop["t"] > norm.ppf(0.9)  # significant in the right tail at 10% each side
    lucky = np.mean(pop["group"][winners] != 2)
    lab = labs.Lab()
    lab.row("True shares: no skill / unskilled / skilled", " / ".join(f"{100 * s:.1f}%" for s in truth))
    lab.row("Storey's estimate of the no-skill share", f"{100 * out['pi0']:.1f}%")
    lab.row("Significant on the right", f"{100 * out['right']:.1f}% of funds, of which luck is expected to be "
                                        f"{100 * out['luck']:.1f}%: estimated skilled {100 * out['plus']:.1f}%")
    lab.row("Significant on the left", f"{100 * out['left']:.1f}% of funds: estimated unskilled {100 * out['minus']:.1f}%")
    lab.row("Of the right-tail winners, truly unskilled", f"{100 * lucky:.0f}%")
    lab.row("A no-skill fund costing 1%, 5% tracking error", "beats the index with probability "
            + ", ".join(f"{100 * skill.beat_prob(0.01, 0.05, y):.0f}% over {y} y" for y in (1, 10, 30)))
    lab.note = ("Most funds that look skilled are the lucky tail of a large population with none. The estimate "
                "of the no-skill share errs on the high side: Storey's count can only be inflated.")
    assert out["pi0"] >= truth[0] - 0.03 and abs(out["plus"] - truth[2]) < 0.02 and abs(out["minus"] - truth[1]) < 0.05
    assert lucky > 0.5

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(-7, 6, 66)
    for g, c, name in ((0, labs.CASH, "no skill"), (1, labs.LOSS, "lose their costs"), (2, labs.GAIN, "skilled")):
        ax[0].hist(pop["t"][pop["group"] == g], bins=bins, color=c, alpha=0.8, label=name)
    ax[0].axvline(norm.ppf(0.9), color=labs.P, ls="--", lw=1)
    ax[0].set(title="t-statistics of 2,000 funds' alphas, by their true type", xlabel="t")
    ax[0].legend(fontsize=8)
    ax[1].hist(pop["p"], bins=20, color=labs.SPOT)
    ax[1].axhline(out["pi0"] * len(pop["p"]) / 20, color=labs.P, ls="--", label=f"Storey: {100 * out['pi0']:.0f}% are nulls")
    ax[1].set(title="p-values: flat where only the skill-less live", xlabel="p-value")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
