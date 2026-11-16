"""Lab 37: inequity aversion and the ultimatum game, a tournament of repeated prisoner's dilemma strategies, public
goods with and without punishment, Hamilton's rule, and a divorce classifier scored in and out of sample."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import social as S

TITLE = "Bonds and Bargains"
GOAL = ("Compute an inequity-averse responder's threshold and a proposer's best offer; run a round-robin of repeated "
        "prisoner's dilemma strategies with and without noise; simulate a public-goods game with and without "
        "punishment; and fit a divorce classifier to a small sample and score it on the couples it was fitted to and "
        "on couples it has not seen.")
TASKS = [
    "Make every responder selfish (alpha = 0 for all). What is the proposer's best offer now, and why does that make "
    "the real offers informative?",
    "Raise the tournament's noise to 10%. Which strategies gain and which lose, and why do forgiving strategies "
    "benefit from noise?",
    "Grow the divorce sample from 56 couples to 500, with the same 30 variables. How do in-sample and leave-one-out "
    "accuracy change, and why?",
]


def run(seed=0):
    out = labs.Lab()

    for a in (0.0, 0.5, 1.0, 2.0):
        out.row(f"responder with alpha {a}: smallest share accepted", f"{float(S.fs_threshold(a)):.3f}")
    alphas = np.r_[np.zeros(30), np.linspace(0.3, 1.5, 70)]
    u = S.ultimatum(alphas)
    out.row("proposer facing Psyche's responders: best offer and expected share",
            f"{u['best']:.2f}; {u['payoff'].max():.2f}")
    assert 0.3 <= u["best"] <= 0.45

    for nz in (0.0, 0.05):
        r = S.ipd_tournament(noise=nz, seed=seed + 37)
        order = np.argsort(-r["score"])
        out.row(f"tournament, noise {nz}: top three", ", ".join(f"{r['strategies'][k]} {r['score'][k]:.2f}"
                                                                for k in order[:3]))

    plain = S.public_goods(seed=seed + 37)
    punish = S.public_goods(punishment=True, seed=seed + 37)
    out.row("public goods: contribution in rounds 1 and 10, without and with punishment",
            f"{plain[0]:.2f} -> {plain[-1]:.2f}; {punish[0]:.2f} -> {punish[-1]:.2f}")
    assert punish[-1] > plain[0] > plain[-1]

    for rel, name in ((0.5, "full sibling"), (0.125, "first cousin")):
        out.row(f"Hamilton's rule, {name}: B/C needed", f"> {1 / rel:.0f}")

    rs = [S.overfit_divorce(seed=seed + s) for s in range(100)]
    out.row("divorce classifier, 56 couples, 30 variables: in-sample; leave-one-out; base rate",
            f"{np.mean([x['insample'] for x in rs]):.2f}; {np.mean([x['loo'] for x in rs]):.2f}; "
            f"{np.mean([x['base'] for x in rs]):.2f}")

    out.note = ("A selfish proposer facing inequity-averse responders offers about what real proposers do; which "
                "strategy wins a tournament depends on the field and on noise; punishment holds up contributions that "
                "otherwise decay; and a model fitted to as many variables as there are couples looks accurate only "
                "on those couples.")

    fig, ax = labs.figure(3, size=(13, 4.0))
    ax[0].plot(u["offers"], u["accept"], color=labs.BLUE, label="P(accept)")
    ax[0].plot(u["offers"], u["payoff"], color=labs.GREEN, label="expected share")
    ax[0].axvline(u["best"], color=labs.GOLD, ls="--")
    ax[0].set(title="The proposer's problem", xlabel="offer (share)")
    ax[0].legend(fontsize=8)
    ax[1].plot(np.arange(1, 11), plain, "o-", color=labs.BLUE, label="no punishment")
    ax[1].plot(np.arange(1, 11), punish, "o-", color=labs.GREEN, label="punishment")
    ax[1].set(title="Public goods", xlabel="round", ylabel="mean contribution")
    ax[1].legend(fontsize=8)
    ax[2].hist([x["insample"] for x in rs], bins=15, color=labs.RED, alpha=0.7, label="in sample")
    ax[2].hist([x["loo"] for x in rs], bins=15, color=labs.BLUE, alpha=0.7, label="leave-one-out")
    ax[2].set(title="Divorce prediction", xlabel="accuracy")
    ax[2].legend(fontsize=8)
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
