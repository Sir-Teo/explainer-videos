"""Lab 6: measure how fast the bell arrives for sums of exponentials, and watch Cauchy means refuse to settle."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import limits

TITLE = "The speed of the central limit theorem, and where it stops"
GOAL = ("Compute the exact distance between the law of a standardized sum of n exponentials and the normal, set it "
        "against the Berry-Esseen bound and the skewness-over-root-n rule, then average Cauchy draws and see the "
        "spread of the mean not shrink at all.")
TASKS = [
    "Replace the exponential by a Bernoulli(0.1) sum (limits.bernoulli_sum_atoms, limits.kolmogorov_lattice). Does "
    "the distance still fall like 1/sqrt(n), and with what constant?",
    "Replace the Cauchy by a Pareto with tail index 1.5 (rng.pareto(1.5) + 1, mean 3). Do the quartiles of the mean "
    "shrink, and at what rate in n?",
    "Use the n = 30 sums to check the delta method: compare the simulated sd of log(mean) with 1/sqrt(30).",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. The speed, exactly: a sum of n Exp(1) is gamma(n), so sup |F_n - Phi| needs no simulation.
    ns = np.array([1, 2, 5, 10, 30, 100, 300, 1000])
    z = np.linspace(-6, 8, 7001)
    rho = limits.third_abs_moment("exponential")  # E|X - 1|^3 = 12/e - 2
    exact = np.array([limits.kolmogorov(limits.exponential_sum_cdf(int(n)), stats.norm.cdf, z) for n in ns])
    bound = np.array([limits.berry_esseen(rho, int(n)) for n in ns])
    rule = 2 / (6 * np.sqrt(2 * np.pi * ns))  # skewness / (6 sqrt(2 pi n)): the first Edgeworth term at z = 0
    reps = 20_000
    sums = (rng.exponential(size=(reps, 30)).sum(1) - 30) / np.sqrt(30)
    ecdf_gap = np.max(np.abs(np.searchsorted(np.sort(sums), z, side="right") / reps - stats.norm.cdf(z)))
    for n, d, b in zip(ns, exact, bound):
        if n in (1, 30, 1000):
            lab.row(f"n = {n}: sup|F_n - Phi|", f"{d:.4f}   Berry-Esseen bound {b:.4f}   skewness rule {2 / (6 * np.sqrt(2 * np.pi * n)):.4f}")
    lab.row("n = 30, simulated (20,000 sums)", f"{ecdf_gap:.4f}   (exact {exact[4]:.4f})")
    assert np.all(exact <= bound), "Berry-Esseen is a guarantee at every n"
    assert np.all(np.diff(exact) < 0), "the distance falls as n grows"
    assert abs(exact[-1] / rule[-1] - 1) < 0.05, "for large n the distance is skewness / (6 sqrt(2 pi n))"
    assert abs(ecdf_gap - exact[4]) < 0.02, "the simulation agrees with the exact law"

    # 2. Where it stops: the mean of n Cauchy draws is Cauchy again, quartiles at -1 and +1 for every n.
    cauchy = rng.standard_cauchy(size=(reps, 100))
    normal = rng.standard_normal(size=(reps, 100))
    q_c, q_n = {}, {}
    for n in (1, 10, 100):
        q_c[n] = np.diff(np.quantile(cauchy[:, :n].mean(1), [0.25, 0.75]))[0] / 2
        q_n[n] = np.diff(np.quantile(normal[:, :n].mean(1), [0.25, 0.75]))[0] / 2
        lab.row(f"half the interquartile range of the mean, n = {n}",
                f"Cauchy {q_c[n]:.3f} (theory 1)   normal {q_n[n]:.3f} (theory {0.6745 / np.sqrt(n):.3f})")
        assert abs(q_c[n] - 1) < 0.08, "averaging Cauchy draws buys nothing"
        assert abs(q_n[n] * np.sqrt(n) / 0.6745 - 1) < 0.08, "normal means shrink like 1/sqrt(n)"
    lab.note = ("With a finite third moment the bell arrives at rate 1/sqrt(n), far inside the Berry-Esseen guarantee "
                "and at the size the skewness predicts; with no mean at all, the average of a hundred draws is as "
                "wild as one draw.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].loglog(ns, bound, color=labs.RED, label="Berry-Esseen bound")
    ax[0].loglog(ns, exact, "o-", color=labs.PURPLE, label="exact sup|F_n - Phi|")
    ax[0].loglog(ns, rule, "--", color=labs.MUTED, label="skewness / (6 sqrt(2 pi n))")
    ax[0].plot([30], [ecdf_gap], "s", color=labs.GREEN, label="simulated, n = 30")
    ax[0].set(title="Sums of n exponentials: distance from the normal", xlabel="n", ylabel="largest gap between the CDFs")
    ax[0].legend()
    steps = np.arange(1, 5001)
    for i in range(5):
        ax[1].plot(steps, np.cumsum(rng.standard_cauchy(5000)) / steps, color=labs.RED, lw=1, alpha=0.8,
                   label="Cauchy" if i == 0 else None)
        ax[1].plot(steps, np.cumsum(rng.standard_normal(5000)) / steps, color=labs.BLUE, lw=1, alpha=0.8,
                   label="normal" if i == 0 else None)
    ax[1].set(title="Running means of five sequences each", xlabel="number of draws", ylabel="mean so far",
              xscale="log", ylim=(-6, 6))
    ax[1].legend()
    lab.fig = fig
    return lab
