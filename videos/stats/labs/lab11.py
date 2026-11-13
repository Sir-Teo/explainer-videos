"""Lab 11: compute the exact coverage of the Wald, Wilson and Clopper-Pearson intervals, and check it by simulation."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import intervals as iv

TITLE = "The sawtooth: exact coverage of intervals for a proportion"
GOAL = ("Sum the binomial probabilities of the outcomes whose interval contains the true p, for three intervals, "
        "and confirm one point of each curve by drawing ten thousand samples.")
TASKS = [
    "Add iv.jeffreys and iv.agresti_coull to the curves at n = 50. Which of them dips below 93%, and where?",
    "Set alpha = 0.01. Does the Wald interval's shortfall at p = 0.05 grow or shrink?",
    "Find the smallest n at which the Wald interval's exact coverage at p = 0.1 stays above 94% for every larger n up to 2,000.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    methods = (("Wald", iv.wald, labs.RED), ("Wilson", iv.wilson, labs.BLUE), ("Clopper-Pearson", iv.clopper_pearson, labs.GREEN))

    # Brown, Cai and DasGupta's example: one more observation
    c591, c592 = float(iv.binom_coverage(iv.wald, 591, 0.005)[0]), float(iv.binom_coverage(iv.wald, 592, 0.005)[0])
    lab.row("Wald, p = 0.005: n = 591, n = 592", f"{c591:.1%}, {c592:.1%}   (the film: 94.5%, 79.2%)")
    assert abs(c591 - 0.945) < 0.001 and abs(c592 - 0.792) < 0.001, "the 591/592 example"

    # coverage against p at n = 50, exactly, and at one p by simulation
    n, p0, reps = 50, 0.05, 10_000
    ps = np.linspace(0.005, 0.995, 397)
    curves = {name: iv.binom_coverage(f, n, ps) for name, f, _ in methods}
    x = rng.binomial(n, p0, reps)
    for name, f, _ in methods:
        table = np.array([f(k, n) for k in range(n + 1)])
        sim = float(np.mean((table[x, 0] <= p0) & (p0 <= table[x, 1])))
        exact = float(iv.binom_coverage(f, n, p0)[0])
        se = np.sqrt(exact * (1 - exact) / reps)
        lab.row(f"{name}, n = 50, p = 0.05", f"exact {exact:.2%}   simulated {sim:.2%}   "
                                             f"grid mean {curves[name].mean():.1%}   grid minimum {curves[name].min():.1%}")
        assert abs(sim - exact) < 4 * se + 1e-9, f"{name}: the simulation agrees with the exact sum"
    assert curves["Clopper-Pearson"].min() >= 0.95, "Clopper-Pearson keeps Neyman's promise at every p"
    assert curves["Wald"].mean() < 0.92 and curves["Wald"].min() < 0.5, "Wald is far below 95% near 0 and 1"
    assert abs(curves["Wilson"].mean() - 0.95) < 0.01 and curves["Wilson"].min() < 0.95, "Wilson: 95% on average, not everywhere"

    # coverage against n at p = 0.2
    ns = np.arange(10, 101)
    saw = {name: np.array([iv.binom_coverage(f, int(m), 0.2)[0] for m in ns]) for name, f, _ in methods}
    lab.row("Wald, p = 0.2, n = 10..100", f"from {saw['Wald'].min():.1%} to {saw['Wald'].max():.1%}   (the film: 81.5% to 95.4%)")
    assert abs(saw["Wald"].min() - 0.815) < 0.001 and abs(saw["Wald"].max() - 0.954) < 0.001
    assert np.sum(np.diff(saw["Wald"]) < -0.01) >= 5, "coverage does not rise steadily with n: it has teeth"
    lab.note = ("Coverage is a sum over n + 1 outcomes, so it jumps whenever p crosses an interval's end: Wald breaks "
                "the promise, Wilson keeps it on average, Clopper-Pearson keeps it everywhere and pays in width.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for name, _, color in methods:
        ax[0].plot(ps, curves[name], color=color, lw=1.1, label=name)
        ax[1].plot(ns, saw[name], color=color, lw=1.3, marker="o", ms=2.5, label=name)
    for a in ax:
        a.axhline(0.95, color=labs.MUTED, ls="--", lw=1)
    ax[0].set(title="Exact coverage against p, n = 50", xlabel="true proportion p", ylabel="coverage", ylim=(0.8, 1.003))
    ax[1].set(title="Exact coverage against n, p = 0.2", xlabel="sample size n", ylim=(0.8, 1.003))
    ax[0].legend(loc="lower center")
    lab.fig = fig
    return lab
