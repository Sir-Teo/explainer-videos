"""Lab 16: peek at a p-value and at a bettor's wealth under a true null, and compare the false alarms."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import stats as St

TITLE = "Optional stopping breaks the p-value and not the bet"
GOAL = ("Under a true null, test after every ten observations and stop at the first p < 0.05: the Reasoner counts "
        "how often that ever happens in 100 looks. Then test a fair coin by betting, and check Ville's inequality: "
        "wealth ever reaches 1/alpha in at most a share alpha of runs. Birnbaum's two coin experiments are computed "
        "beside them.")
TASKS = [
    "Change check_every from 10 to 1 and to 100. How does the share of runs that ever reject depend on the number "
    "of looks, and what is it with a single look?",
    "Bet a fraction lam = 0.5 instead of 0.2 on the 60% coin. Compare the share of runs reaching 20 with the "
    "Kelly growth rate p ln(1 + lam) + (1 - p) ln(1 - lam).",
    "In St.birnbaum's setting, compute both p-values for 10 heads and 2 tails (stop at the 2nd tail). Do the "
    "verdicts at the 5% level still disagree?",
]


def run(seed=0):
    lab = labs.Lab()
    stop = St.optional_stopping(runs=2000, max_n=1000, check_every=10, seed=seed)
    looks = np.arange(1, len(stop["looks"]) + 1)
    ever = np.array(stop["ever_rejected"])
    assert abs(ever[0] - 0.05) < 0.02, "one look: the nominal 5%"
    assert ever[-1] > 0.25 and np.all(np.diff(ever) >= 0), "a hundred looks: far above 5%"
    assert stop["lr_ever_10"] <= 0.10 + 0.01, "a likelihood ratio reaches 10 in at most 1 run in 10"
    lab.row("false rejections, 1 look", f"{ever[0]:.3f}   (theory 0.050)")
    lab.row("false rejections, 10 looks", f"{ever[9]:.3f}")
    lab.row("false rejections, 100 looks", f"{ever[-1]:.3f}   (the film: about 0.35)")
    lab.row("likelihood ratio ever reaches 10, 100 looks", f"{stop['lr_ever_10']:.3f}   (bound 0.100)")

    bet = St.betting(n=400, p_true=0.6, runs=4000, seed=seed, lam=0.2)
    alphas = [0.2, 0.1, 0.05, 0.01]
    ville = [bet["ville"][str(a)] for a in alphas]
    for a, v in zip(alphas, ville):
        assert v <= a + 0.015, "Ville's inequality"
        lab.row(f"fair coin: wealth ever reaches {1 / a:g}", f"{v:.3f}   (bound {a:.2f})")
    assert bet["alt_reach_20"] > 0.85, "the bet has power against a 60% coin"
    lab.row("60% coin: wealth reaches 20 within 400 tosses", f"{bet['alt_reach_20']:.3f}   median toss {bet['median_time_to_20']:.0f}")

    b = St.birnbaum()
    assert b["proportional"] and b["p_binomial"] > 0.05 > b["p_negative_binomial"], "same likelihood, two verdicts"
    lab.row("9 heads, 3 tails: likelihood ratio 0.75 vs 0.5", f"{b['ratio_E1']:.2f} (12 tosses)   {b['ratio_E2']:.2f} (to the 3rd tail)")
    lab.row("9 heads, 3 tails: one-sided p", f"{b['p_binomial']:.3f} (12 tosses)   {b['p_negative_binomial']:.3f} (to the 3rd tail)")
    lab.note = ("A p-value is valid for the one look that was planned: peeking a hundred times turns 5% into about "
                "a third. A bettor's wealth is a test martingale, so its guarantee holds at every look at once.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(looks, ever, color=labs.RED, label="stop at the first p < 0.05")
    ax[0].axhline(0.05, color=labs.MUTED, ls="--", lw=1, label="nominal 5%")
    ax[0].axhline(stop["lr_ever_10"], color=labs.GREEN, label="likelihood ratio ever reaches 10 (bound 10%)")
    ax[0].set(title="Under a true null: runs that ever 'reject'", xlabel="number of looks (one every 10 observations)",
              ylabel="share of 2,000 runs", ylim=(0, max(0.45, ever[-1] * 1.25)))
    ax[0].legend(loc="upper left")
    t = np.arange(1, len(bet["null_path"]) + 1) * 2
    ax[1].semilogy(t, bet["null_path"], color=labs.BLUE, label="one fair coin")
    ax[1].semilogy(t, bet["alt_path"], color=labs.GOLD, label="one 60% coin")
    ax[1].axhline(20, color=labs.RED, ls="--", lw=1, label="wealth 20: evidence at the 5% level")
    ax[1].axhline(1, color=labs.MUTED, lw=0.8)
    ax[1].set(title="Betting a fifth of your wealth on heads", xlabel="tosses", ylabel="wealth (start: 1)")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
