"""Lab 8: deal Student's 3,000 cards into samples of four, and see which multiplier keeps the 95% promise."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats import museum
from explainer.stats.kit import intervals
from explainer.stats.kit import random as skr

TITLE = "Student's cards: 1.96 against the t multiplier"
GOAL = ("Shuffle Macdonell's 3,000 heights forty times, deal each shuffle into 750 samples of four as Gosset did, "
        "and compare the coverage of mean +/- 1.96 s/sqrt(n) and of Student's interval with what the t distribution "
        "with 3 degrees of freedom predicts. Then check two more of the part's claims on simulated samples.")
TASKS = [
    "Deal samples of 2, 8 and 30 instead of 4. How fast does the 1.96 interval's coverage approach 95%?",
    "Replace the heights by their exponentials, np.exp((h - h.mean()) / h.std()), a skewed population. Which "
    "interval suffers, and on which side does it miss?",
    "Build the chi-squared interval for the variance (intervals.var_interval) on normal and on exponential samples "
    "of ten. Which coverage survives?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Gosset's experiment on the Museum's cards.
    cards = np.repeat(np.asarray(museum.CRIM_HEIGHT_CM), np.asarray(museum.CRIM_TABLE).sum(0))
    mu, n, shuffles = cards.mean(), 4, 40
    deals = np.concatenate([rng.permutation(cards).reshape(-1, n) for _ in range(shuffles)])  # 30,000 samples of four
    xbar, s = deals.mean(1), deals.std(1, ddof=1)
    tmult = stats.t.ppf(0.975, n - 1)
    err = np.abs(xbar - mu)
    hit_z, hit_t = err <= 1.96 * s / 2, err <= tmult * s / 2
    theory_z = 1 - 2 * stats.t.sf(1.96, n - 1)
    first = intervals.t_interval(deals[0])
    assert abs(first[1] - (xbar[0] + tmult * s[0] / 2)) < 1e-9, "the vectorized interval is statkit's t_interval"
    lab.row("cards, mean and sd (cm)", f"{len(cards)}, {mu:.2f}, {cards.std():.2f}")
    lab.row("first shuffle, 750 samples: 1.96 covers", f"{hit_z[:750].mean():.1%}   Student's {tmult:.2f} covers {hit_t[:750].mean():.1%}")
    lab.row("all 30,000 samples: 1.96 covers", f"{hit_z.mean():.1%} +/- {skr.mc_se(hit_z):.1%}   (t with 3 df predicts {theory_z:.1%})")
    lab.row("all 30,000 samples: Student's covers", f"{hit_t.mean():.1%} +/- {skr.mc_se(hit_t):.1%}   (promise 95%)")
    assert abs(hit_z.mean() - theory_z) < 0.015, "with s from four cards, 1.96 covers about 85.5%, not 95%"
    assert abs(hit_t.mean() - 0.95) < 0.012, "Student's multiplier keeps the promise"

    # 2. Fisher's geometry: mean and sd are independent for normal samples, and only for them.
    reps = 200_000
    z3, e3 = rng.standard_normal((reps, 3)), rng.exponential(size=(reps, 3))
    r_norm = np.corrcoef(z3.mean(1), z3.std(1, ddof=1))[0, 1]
    r_exp = np.corrcoef(e3.mean(1), e3.std(1, ddof=1))[0, 1]
    lab.row("corr(mean, sd), samples of 3", f"normal {r_norm:+.3f} (theory 0)   exponential {r_exp:+.3f}")
    assert abs(r_norm) < 0.012 and r_exp > 0.6, "independence of mean and sd is special to the normal"

    # 3. Bias against variance: the MSE of SS/c for normal samples of five is least at c = n + 1.
    n5 = 5
    ss = ((z5 := rng.standard_normal((reps, n5))) - z5.mean(1, keepdims=True)) ** 2
    ss = ss.sum(1)
    cs = np.array([n5 - 1, n5, n5 + 1])
    mse_sim = np.array([np.mean((ss / c - 1) ** 2) for c in cs])
    mse_th = ((n5 - 1) / cs - 1) ** 2 + 2 * (n5 - 1) / cs ** 2
    lab.row("MSE of SS/c, c = n - 1, n, n + 1 (n = 5)", "  ".join(f"{a:.3f}" for a in mse_sim) + "   (theory " + ", ".join(f"{a:.3f}" for a in mse_th) + ")")
    assert np.allclose(mse_sim, mse_th, rtol=0.04) and mse_sim[2] < mse_sim[1] < mse_sim[0], "n + 1 beats n beats n - 1"
    lab.note = ("Four cards give a standard deviation too shaky for the normal table: the ratio follows Student's t "
                "with 3 degrees of freedom, whose 97.5% point is 3.18. The unbiased divisor n - 1 is not the one "
                "with the smallest mean squared error.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ok = s > 0
    ratio = (xbar[ok] - mu) / (s[ok] / 2)
    grid = np.linspace(-6, 6, 400)
    counts, edges = np.histogram(ratio, bins=np.linspace(-6, 6, 31))  # wide bins: the heights are whole inches
    ax[0].bar(edges[:-1], counts / (len(ratio) * 0.4), width=0.4, align="edge", color=labs.BLUE, alpha=0.6,
              label="30,000 samples of four cards")
    ax[0].plot(grid, stats.norm.pdf(grid), color=labs.RED, label="normal")
    ax[0].plot(grid, stats.t.pdf(grid, 3), color=labs.GOLD, label="Student's t, 3 df")
    for m, c in ((1.96, labs.RED), (tmult, labs.GOLD)):
        ax[0].axvline(m, color=c, ls="--", lw=1)
        ax[0].axvline(-m, color=c, ls="--", lw=1)
    ax[0].set(title="(mean - true mean) / (s / sqrt(4))", xlabel="the ratio Gosset computed (dashed: 1.96 and 3.18)",
              ylabel="density", ylim=(0, 0.62))
    ax[0].legend(loc="upper left", frameon=True, facecolor=labs.BG, edgecolor=labs.GRID, framealpha=1)
    cgrid = np.linspace(3, 9, 200)
    ax[1].plot(cgrid, ((n5 - 1) / cgrid - 1) ** 2 + 2 * (n5 - 1) / cgrid ** 2, color=labs.GOLD, label="theory")
    ax[1].plot(cs, mse_sim, "o", color=labs.BLUE, label="simulated: c = 4, 5, 6")
    ax[1].axvline(n5 + 1, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title="MSE of SS/c as a variance estimate, n = 5", xlabel="divisor c", ylabel="MSE / sigma^4")
    ax[1].legend()
    lab.fig = fig
    return lab
