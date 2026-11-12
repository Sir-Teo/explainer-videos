"""Lab 25: three hundred candidate factors, thirty real: who gets through each hurdle."""

import numpy as np
from scipy.stats import norm

from videos.quant import labs
from explainer.quant.house import econ, zoo

TITLE = "Three hundred factors, thirty real: four hurdles"
GOAL = ("Draw t-statistics for 300 factors of which 30 have a real premium. Apply the classical 1.96, Bonferroni, "
        "Benjamini-Hochberg and empirical-Bayes shrinkage, and count true and false discoveries under each.")
TASKS = [
    "Publish only t > 2 and rerun eb_shrink on the survivors. How wrong is the shrinkage factor?",
    "Make the null t-statistics correlated (a common market factor). Does BH still control the FDR?",
    "Lower the share of real factors to 3%. What does 1.96 deliver now?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    M, real = 300, 30
    truth = np.zeros(M, bool)
    truth[:real] = True
    lab = labs.Lab()
    fdp = {"t > 1.96": [], "Bonferroni": [], "Benjamini-Hochberg 5%": []}
    power = {k: [] for k in fdp}
    for rep in range(400):
        theta = np.where(truth, rng.normal(3.5, 1.0, M), 0.0)
        t = theta + rng.standard_normal(M)
        p = 2 * norm.sf(np.abs(t))
        rules = {"t > 1.96": np.abs(t) > 1.96, "Bonferroni": np.abs(t) > zoo.bonferroni_t(M),
                 "Benjamini-Hochberg 5%": econ.benjamini_hochberg(p, 0.05)}
        for k, rej in rules.items():
            fdp[k].append(np.sum(rej & ~truth) / max(rej.sum(), 1))
            power[k].append(np.sum(rej & truth) / real)
    for k in fdp:
        lab.row(k, f"false discovery rate {100 * np.mean(fdp[k]):4.1f}%   real factors found {100 * np.mean(power[k]):4.1f}%")
    eb = zoo.eb_shrink(t)
    best = zoo.noise_max_t(M - real, sims=2000, seed=seed, absolute=True)
    lab.row("Bonferroni hurdle for 300 tests", f"|t| > {zoo.bonferroni_t(M):.2f}")
    lab.row("Best |t| among 270 pure-noise factors", f"{best['mean']:.2f} on average")
    lab.row("Empirical-Bayes shrinkage of every t", f"x{eb['shrink']:.2f}")
    lab.note = "The 1.96 hurdle was built for one test. BH keeps the share of false discoveries near 5% without Bonferroni's loss of power."
    assert np.mean(fdp["t > 1.96"]) > 0.25 and np.mean(fdp["Bonferroni"]) < 0.01
    assert 0.03 < np.mean(fdp["Benjamini-Hochberg 5%"]) < 0.06 and np.mean(power["Benjamini-Hochberg 5%"]) > np.mean(power["Bonferroni"])

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(-4, 8, 61)
    ax[0].hist(t[~truth], bins=bins, color=labs.CASH, label="270 with no premium")
    ax[0].hist(t[truth], bins=bins, color=labs.GAIN, label="30 real")
    for x, c, name in ((1.96, labs.LOSS, "1.96"), (zoo.bonferroni_t(M), labs.P, "Bonferroni")):
        ax[0].axvline(x, color=c, ls="--", lw=1)
        ax[0].text(x + 0.05, ax[0].get_ylim()[1] * 0.92, name, color=c, fontsize=8)
    ax[0].set(title="One draw of 300 t-statistics", xlabel="t")
    ax[0].legend(fontsize=8)
    names = list(fdp)
    x = np.arange(3)
    ax[1].bar(x - 0.2, [100 * np.mean(fdp[k]) for k in names], 0.4, color=labs.LOSS, label="false discovery rate")
    ax[1].bar(x + 0.2, [100 * np.mean(power[k]) for k in names], 0.4, color=labs.GAIN, label="real factors found")
    ax[1].set_xticks(x, ["t > 1.96", "Bonferroni", "BH 5%"])
    ax[1].set(title="What each hurdle delivers (400 draws)", ylabel="%")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
