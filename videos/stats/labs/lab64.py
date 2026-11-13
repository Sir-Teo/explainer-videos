"""Lab 64: put honest error bars on a clustered benchmark, then refit a Gaussian to its own samples."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import evals

TITLE = "Benchmarks are samples; a model fed its own output forgets"
GOAL = ("Write 1,500 benchmarks of 200 passages with 10 questions each, and compare the coverage of the usual "
        "standard error with the cluster-robust one. Then fit a normal law to 20 draws, sample 20 new draws from "
        "the fit, refit, and repeat: after t refits the expected variance should be ((n - 1)/n)^t.")
TASKS = [
    "Set the passage effect tau to 0. What are the design effect and the two coverages now?",
    "Score a second model on the same questions with evals.correlated_pair and compare evals.paired_compare's "
    "paired and unpaired intervals for the difference.",
    "Call evals.gaussian_collapse with accumulate=True, so each refit keeps all earlier samples. Does the variance "
    "still drift to zero?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a clustered benchmark: 200 passages of 10 questions, a random passage effect on the logit scale
    G, m, base, tau, reps = 200, 10, 0.8, 1.0, 1500
    z, w = np.polynomial.hermite_e.hermegauss(80)
    pz = 1 / (1 + np.exp(-(math.log(base / (1 - base)) + tau * z)))
    truth = float(w @ pz / w.sum())  # the population accuracy, by quadrature
    icc = float((w @ pz ** 2 / w.sum() - truth ** 2) / (truth * (1 - truth)))
    deff = evals.design_effect(m, icc)
    score, se_i, se_c = np.zeros(reps), np.zeros(reps), np.zeros(reps)
    for r in range(reps):
        b = evals.clustered_benchmark(G, m, base, tau, rng)
        score[r], se_i[r] = evals.mean_se(b["x"])["mean"], evals.mean_se(b["x"])["se"]
        se_c[r] = evals.cluster_se(b["x"], b["cluster"])["se"]
    cov_i = float(np.mean(np.abs(score - truth) <= 1.96 * se_i))
    cov_c = float(np.mean(np.abs(score - truth) <= 1.96 * se_c))
    lab.row("population accuracy (baseline 0.8 on the logit scale)", f"{truth:.4f}   mean score {score.mean():.4f}")
    lab.row("sd of the score across benchmarks", f"{score.std(ddof=1):.4f}   iid SE {se_i.mean():.4f}   cluster SE {se_c.mean():.4f}")
    lab.row("design effect 1 + (m - 1) ICC", f"{deff:.2f}   (cluster SE / iid SE)^2 = {np.mean(se_c ** 2) / np.mean(se_i ** 2):.2f}")
    lab.row("95% interval covers the population accuracy", f"iid {cov_i:.1%}   cluster-robust {cov_c:.1%}")
    assert abs(score.mean() - truth) < 0.003, "the score is unbiased for the population accuracy"
    assert abs(np.mean(se_c ** 2) / np.mean(se_i ** 2) / deff - 1) < 0.1, "CR1 recovers the design effect"
    assert cov_i < 0.85 and abs(cov_c - 0.95) < 0.025, "only the cluster-robust interval keeps its promise"

    # 2. model collapse: a Gaussian refitted to n of its own samples, generation after generation
    n, T, runs = 20, 60, 400
    col = evals.gaussian_collapse(n, T, runs, rng)
    # the kit's path at index t is the variance after t refits to the model's own samples (index 0 is the start, 1)
    paths, fits = col["paths"][:, 1:], np.arange(1, T + 1)
    theory = col["expected"][1:]
    drift = float(np.mean(np.log(paths[:, -1])) / fits[-1])
    lab.row("mean fitted variance after 10 refits", f"{paths[:, 9].mean():.3f}   (theory (19/20)^10 = {theory[9]:.3f})")
    lab.row("drift of log variance per refit", f"{drift:.4f}   (theory E log(chi2_19 / 20) = {col['drift']:.4f})")
    lab.row(f"runs with variance below 0.01 after {fits[-1]} refits", f"{np.mean(paths[:, -1] < 0.01):.0%}")
    assert fits[9] == 10 and abs(theory[9] - (19 / 20) ** 10) < 1e-12 and abs(paths[:, 9].mean() / theory[9] - 1) < 0.25, "the mean variance follows ((n - 1)/n)^t"
    assert abs(drift - col["drift"]) < 0.006 and col["drift"] < math.log(19 / 20), "the log variance drifts down, faster than the mean"
    lab.note = ("Questions that share a passage carry less information than their number suggests, and each refit to "
                "one's own samples loses a little variance that is never given back.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.linspace(truth - 0.09, truth + 0.09, 200)
    ax[0].hist(score, bins=45, density=True, color=labs.BLUE, alpha=0.6, label=f"{reps:,} benchmark scores")
    for se, color, name in ((se_i.mean(), labs.RED, "iid SE"), (se_c.mean(), labs.GREEN, "cluster-robust SE")):
        ax[0].plot(grid, np.exp(-0.5 * ((grid - truth) / se) ** 2) / (se * math.sqrt(2 * math.pi)), color=color,
                   label=f"normal with the {name}")
    ax[0].set(title="2,000 questions in 200 passages: which SE matches?", xlabel="benchmark accuracy", ylabel="density")
    ax[0].legend()
    t = fits
    for path in paths[:25]:
        ax[1].plot(t, path, color=labs.GREY, lw=0.7, alpha=0.5)
    ax[1].plot([], [], color=labs.GREY, lw=0.7, label="25 single runs")
    ax[1].plot(t, paths.mean(0), color=labs.BLUE, label=f"mean of {runs} runs")
    ax[1].plot(t, theory, color=labs.GOLD, ls="--", label="((n - 1)/n)^t")
    ax[1].plot(t, np.exp(col["drift"] * t), color=labs.RED, ls=":", label="typical run: exp(t E log(chi2/n))")
    ax[1].set(yscale="log", title="A Gaussian refitted to 20 of its own samples", xlabel="number of refits t to its own samples",
              ylabel="fitted variance (log scale)")
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
