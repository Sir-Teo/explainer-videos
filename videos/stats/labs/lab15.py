"""Lab 15: judge 95% credible intervals by frequency, at a fixed truth and on average over the prior."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import bayes

TITLE = "Credible intervals on the Coverage Board"
GOAL = ("For a binomial with n = 50 and three beta priors, compute how often the 95% credible interval contains a "
        "fixed truth, exactly and by simulation; then draw the truth from the prior and check that the coverage "
        "is 95%.")
TASKS = [
    "Draw the truth from Beta(2, 18) but keep the Beta(18, 2) prior in the analysis. What is the average coverage now?",
    "Replace bayes.credible by bayes.hpd. Is the HPD interval's coverage over the prior still 95%? Is its curve against p the same?",
    "Raise n from 50 to 500 with the Beta(18, 2) prior. How large must n be before coverage at p = 0.05 passes 90%?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, reps = 50, 10_000
    priors = (("uniform Beta(1, 1)", 1.0, 1.0, labs.BLUE), ("Jeffreys Beta(1/2, 1/2)", 0.5, 0.5, labs.GREEN),
              ("confident Beta(18, 2)", 18.0, 2.0, labs.RED))
    ks = np.arange(n + 1)
    ps = np.linspace(0.005, 0.995, 199)

    def table(a, b):  # the 95% equal-tailed interval after each possible count
        return np.array([bayes.credible(stats.beta(*bayes.beta_update(a, b, k, n - k))) for k in ks])

    def exact(tab, p):  # coverage at a fixed p: a sum over the n + 1 outcomes
        p = np.atleast_1d(p)
        inside = (tab[None, :, 0] <= p[:, None]) & (p[:, None] <= tab[None, :, 1])
        return (stats.binom.pmf(ks[None, :], n, p[:, None]) * inside).sum(1)

    lab = labs.Lab()
    curves, tabs = {}, {}
    for name, a, b, _ in priors:
        tabs[name] = tab = table(a, b)
        curves[name] = exact(tab, ps)
        for p0 in (0.05, 0.9):
            x = rng.binomial(n, p0, reps)
            sim = float(np.mean((tab[x, 0] <= p0) & (p0 <= tab[x, 1])))
            ex = float(exact(tab, p0)[0])
            assert abs(sim - ex) < 4 * np.sqrt(max(ex * (1 - ex), 1e-4) / reps), "simulation agrees with the exact sum"
            lab.row(f"{name}, truth fixed at {p0}", f"exact {ex:.2%}   simulated {sim:.2%}")

    # the truth drawn from the prior the analyst uses
    name, a, b, _ = priors[2]
    p = rng.beta(a, b, reps)
    x = rng.binomial(n, p)
    hit = (tabs[name][x, 0] <= p) & (p <= tabs[name][x, 1])
    avg, se = float(hit.mean()), float(np.sqrt(0.95 * 0.05 / reps))
    lab.row(f"{name}, truth drawn from the prior", f"simulated {avg:.2%}   (theory 95.00%, Monte Carlo SE {se:.2%})")
    wrong = rng.uniform(0, 1, reps)  # the world does not follow the prior
    xw = rng.binomial(n, wrong)
    avg_wrong = float(np.mean((tabs[name][xw, 0] <= wrong) & (wrong <= tabs[name][xw, 1])))
    lab.row(f"{name}, truth drawn uniformly instead", f"simulated {avg_wrong:.2%}")
    lab.note = ("A credible interval's 95% is a statement given the data. Averaged over truths drawn from the prior "
                "it is also a frequency; at one fixed truth it can be anything, and a confident wrong prior makes it 0.")
    assert abs(avg - 0.95) < 4 * se, "calibrated on average over the prior"
    assert float(exact(tabs[name], 0.05)[0]) < 0.001, "Beta(18, 2) never covers a truth of 0.05 at n = 50"
    assert float(exact(tabs[name], 0.9)[0]) > 0.97 and avg_wrong < 0.85, "right for the truths it expects, wrong for the rest"
    assert abs(curves[priors[0][0]].mean() - 0.95) < 0.01 and abs(curves[priors[1][0]].mean() - 0.95) < 0.01

    fig, ax = labs.figure(2, size=(11, 4.2))
    for name, a, b, color in priors:
        ax[0].plot(ps, curves[name], color=color, lw=1.2, label=name)
    ax[0].axhline(0.95, color=labs.MUTED, ls="--", lw=1)
    ax[0].set(title="Coverage of the 95% credible interval at a fixed truth, n = 50", xlabel="true proportion p",
              ylabel="coverage", ylim=(-0.03, 1.03))
    ax[0].legend(loc="center left", bbox_to_anchor=(0.02, 0.62))
    grid = np.linspace(0.001, 0.999, 500)
    post = stats.beta(*bayes.beta_update(1, 1, 8, 4))
    lo, hi = bayes.credible(post)
    ax[1].plot(grid, np.ones_like(grid), color=labs.MUTED, label="prior: uniform")
    ax[1].plot(grid, post.pdf(grid), color=labs.GOLD, label="posterior Beta(9, 5)")
    ax[1].fill_between(grid, post.pdf(grid), where=(grid >= lo) & (grid <= hi), color=labs.GOLD, alpha=0.25,
                       label=f"95% credible [{lo:.2f}, {hi:.2f}]")
    ax[1].axvline(bayes.rule_of_succession(8, 12), color=labs.BLUE, ls=":", label="mean 9/14 (rule of succession)")
    ax[1].set(title="Bayes's table: 8 of 12 balls stop to the left", xlabel="position p of the hidden ball", ylabel="density",
              ylim=(0, 4.6))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
