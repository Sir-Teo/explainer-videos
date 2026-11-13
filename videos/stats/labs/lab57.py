"""Lab 57: break the t-interval with the Bahadur-Savage mixture, and check the quantile lemma on the same data."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import dfree

TITLE = "No interval for the mean, an exact one for the next draw"
GOAL = ("On the mixture (1 - eps) N(0, 1) + eps at 3/eps, whose mean is 3 for every eps, measure the 95% t-interval's "
        "coverage of the mean against the Bahadur-Savage bound, and split conformal's coverage of the next draw "
        "against k/(n + 1) and the Beta law of coverage given the calibration set.")
TASKS = [
    "Raise n from 50 to 500 at eps = 0.003. Does the t-interval recover? Then shrink eps to 0.0003 and see the bound return.",
    "Replace the mean by the median: cover the mixture's median with the order-statistic interval of Part 16 and check that its coverage does not depend on eps.",
    "Call dfree.quantile_lemma_coverage(8, 0.1). Why does k = 9 with 8 calibration scores make the conformal interval the whole line, and what is the smallest n that gives a finite one?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, alpha, shift = 50, 0.05, 3.0
    lab = labs.Lab()

    # 1. the t-interval for the mean: simulation against the bound
    eps = np.array([0.3, 0.1, 0.03, 0.01, 0.003, 0.001])
    sim = np.array([dfree.bahadur_savage_sim(n, e, rng, shift=shift, reps=6000) for e in eps])
    upper = np.array([dfree.bahadur_savage_coverage(n, e, shift=shift)["upper"] for e in eps])
    for e, s, u in zip(eps, sim, upper):
        lab.row(f"t-interval covers the mean, eps = {e:g}", f"{s:.1%}   bound 1 - (1 - eps)^n = {u:.1%}")

    # 2. split conformal for the next draw from the same mixture: 10 points fix the centre, 40 calibrate
    n_fit, n_cal, reps, e0 = 10, 40, 20000, 0.003
    x = rng.standard_normal((reps, n + 1))
    x[rng.random((reps, n + 1)) < e0] = shift / e0
    centre = np.median(x[:, :n_fit], axis=1, keepdims=True)
    scores = np.abs(x[:, n_fit:n] - centre)
    lemma = dfree.quantile_lemma_coverage(n_cal, alpha)
    q = np.sort(scores, axis=1)[:, lemma["k"] - 1]
    conformal = np.mean(np.abs(x[:, n] - centre[:, 0]) <= q)
    lab.row("split conformal covers the next draw, eps = 0.003", f"{conformal:.1%}   lemma k/(n + 1) = {lemma['k']}/{n_cal + 1} = {lemma['exact']:.1%}")

    # 3. coverage given the calibration set: Beta(k, n + 1 - k), here for |N(0, 1)| scores
    law = dfree.conformal_coverage_law(100, 0.1)
    cal = np.sort(np.abs(rng.standard_normal((4000, 100))), axis=1)[:, law["a"] - 1]
    given = 2 * stats.norm.cdf(cal) - 1
    lab.row("coverage given 100 calibration scores: mean", f"{given.mean():.1%}   Beta({law['a']}, {law['b']}) mean {law['mean']:.1%}")
    lab.row("its 5% quantile", f"{np.quantile(given, 0.05):.1%}   Beta {law['q05']:.1%}")
    lab.note = ("A rare far value carries the mean where no sample of fifty finds it, so the t-interval's coverage falls "
                "with eps; the next draw's rank among the calibration scores is uniform whatever the law, so conformal "
                "coverage is k/(n + 1), on average over calibration sets.")
    assert np.all(sim <= upper + 0.02), "coverage never exceeds the Bahadur-Savage bound"
    assert sim[0] > 0.9 and sim[4] < 0.2 and sim[5] < 0.09 and abs(sim[4] - upper[4]) < 0.03, "the t-interval collapses as eps falls"
    assert abs(conformal - lemma["exact"]) < 0.008, "the quantile lemma's exact coverage"
    assert abs(given.mean() - law["mean"]) < 0.004 and abs(np.quantile(given, 0.05) - law["q05"]) < 0.008, "the Beta law"

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(eps, upper, color=labs.GOLD, label="Bahadur-Savage bound")
    ax[0].plot(eps, sim, "o", color=labs.RED, label="t-interval for the mean (simulated)")
    ax[0].axhline(0.95, color=labs.MUTED, ls="--", lw=1)
    ax[0].plot([e0], [conformal], "s", color=labs.GREEN, label="split conformal for the next draw")
    ax[0].set(title="n = 50, every mixture has mean 3", xlabel="eps, the weight of the far value (log scale)",
              ylabel="coverage", xscale="log", ylim=(0, 1.02))
    ax[0].legend(loc="lower right")
    grid = np.linspace(0.78, 0.98, 300)
    ax[1].hist(given, bins=40, density=True, color=labs.BLUE, alpha=0.6, label="4,000 calibration sets")
    ax[1].plot(grid, stats.beta.pdf(grid, law["a"], law["b"]), color=labs.GOLD, label=f"Beta({law['a']}, {law['b']})")
    ax[1].axvline(0.9, color=labs.MUTED, ls="--", lw=1, label="nominal 90%")
    ax[1].set(title="Coverage given the calibration set, n = 100, alpha = 0.1", xlabel="coverage of the next draw", ylabel="density")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
