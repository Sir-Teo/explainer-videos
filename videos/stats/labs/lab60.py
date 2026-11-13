"""Lab 60: plant a cluster in high-dimensional data, then shift the covariates, and see which estimates survive."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import shift

TITLE = "A planted cluster, and a shifted population"
GOAL = ("Replace 10% of n = 2,000 Gaussian points in d dimensions by a tight cluster and measure the error of the "
        "mean, the coordinatewise median, the geometric median and the spectral filter as d grows. Then estimate a "
        "target population's mean from a source sample whose covariate is shifted, with and without importance "
        "weights, and compare Kish's effective sample size with its formula.")
TASKS = [
    "Move the planted cluster from 2 to 0.5 in every coordinate (value=0.5). Which estimators still notice it, and does the filter still remove it?",
    "Raise the covariate shift from 0.7 to 2. What happens to the effective sample size, and to the weighted interval's coverage?",
    "Estimate the weights with shift.logistic_density_ratio from the source x and 2,000 unlabelled target draws, in place of the true ratio. How much coverage is lost?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. contamination: n points from N(0, I_d), a fraction eps replaced by a cluster at (2, ..., 2)
    n, eps, value = 2000, 0.1, 2.0
    dims = np.array([10, 25, 50, 100])
    errs = [shift.robust_mean_errors(n, int(d), eps, rng, value) for d in dims]
    names = ("mean", "coord_median", "geo_median", "filter", "oracle")
    E = {k: np.array([e[k] for e in errs]) for k in names}
    med_shift = stats.norm.ppf(1 / (2 * (1 - eps)))  # the median of (1 - eps) N(0, 1) + eps at +infinity
    lab.row("error of the mean, d = 100", f"{E['mean'][-1]:.2f}   theory eps x 2 x sqrt(d) = {eps * value * 10:.2f}")
    lab.row("error of the coordinatewise median, d = 100", f"{E['coord_median'][-1]:.2f}   theory {med_shift:.3f} x sqrt(d) = {med_shift * 10:.2f}")
    lab.row("error of the geometric median, d = 100", f"{E['geo_median'][-1]:.2f}")
    lab.row("error of the spectral filter, d = 100", f"{E['filter'][-1]:.2f}   clean points' mean {E['oracle'][-1]:.2f}   sqrt(d/n) = {np.sqrt(100 / n):.2f}")
    lab.row("filter removed", f"{errs[-1]['removed_bad']:.0%} of the planted points, {errs[-1]['removed_good']:.1%} of the clean ones")

    # 2. covariate shift: source x ~ N(0, 1), target x ~ N(0.7, 1), y = 2 + x + noise in both
    m, delta, reps = 600, 0.7, 400
    target = 2 + delta
    plain, weighted, ess, cover_p, cover_w = (np.empty(reps) for _ in range(5))
    z = stats.norm.isf(0.025)
    for r in range(reps):
        x = rng.standard_normal(m)
        y = 2 + x + rng.standard_normal(m)
        w = np.exp(delta * x - delta ** 2 / 2)  # the density ratio N(delta, 1) / N(0, 1)
        ci = shift.weighted_mean_ci(y, w)
        plain[r], weighted[r], ess[r] = y.mean(), ci["mean"], ci["ess"]
        cover_p[r] = abs(y.mean() - target) <= z * y.std(ddof=1) / np.sqrt(m)
        cover_w[r] = ci["lo"] <= target <= ci["hi"]
    ess_theory = m / np.exp(delta ** 2)  # n / E w^2
    lab.row("unweighted source mean", f"{plain.mean():.3f}   target {target:.3f}   95% interval covers {cover_p.mean():.1%}")
    lab.row("importance-weighted mean", f"{weighted.mean():.3f}   95% interval covers {cover_w.mean():.1%}")
    lab.row("Kish effective sample size", f"{ess.mean():.0f} of {m}   theory n / E w^2 = {ess_theory:.0f}")
    lab.row("sd of the weighted mean / sd of the unweighted", f"{weighted.std() / plain.std():.2f}")
    lab.note = ("A planted tenth moves the mean and both medians by an amount that grows like the square root of the "
                "dimension, while the filter stays at the clean sample's error; reweighting removes the bias of a "
                "shifted sample and pays for it in effective sample size.")
    assert abs(E["mean"][-1] / (eps * value * 10) - 1) < 0.15, "the mean moves by eps x value x sqrt(d)"
    assert abs(E["coord_median"][-1] / (med_shift * 10) - 1) < 0.2, "each coordinate's median absorbs the planted mass"
    assert E["coord_median"][-1] > 2 * E["coord_median"][0] and E["geo_median"][-1] > 2 * E["geo_median"][0], "medians grow with d"
    assert np.all(E["filter"] < 2 * E["oracle"] + 0.05) and E["filter"][-1] < 0.35 * E["coord_median"][-1], "the filter tracks the oracle"
    assert errs[-1]["removed_bad"] > 0.9
    assert cover_p.mean() < 0.02 and abs(weighted.mean() - target) < 0.02, "weights remove the bias"
    assert cover_w.mean() > 0.89 and abs(ess.mean() / ess_theory - 1) < 0.1 and weighted.std() > plain.std(), "at the price of variance"

    fig, ax = labs.figure(2, size=(11, 4.2))
    for k, color, label in (("mean", labs.RED, "mean"), ("coord_median", labs.ORANGE, "coordinatewise median"),
                            ("geo_median", labs.PURPLE, "geometric median"), ("filter", labs.GREEN, "spectral filter"),
                            ("oracle", labs.GREY, "mean of the clean points")):
        ax[0].plot(dims, E[k], marker="o", color=color, ms=4, label=label, ls="--" if k == "oracle" else "-")
    ax[0].set(title="10% planted at (2, ..., 2): error of the estimated centre", xlabel="dimension d (log scale)",
              ylabel="distance from the true mean (log scale)", xscale="log", yscale="log")
    ax[0].legend(loc="center right")
    bins = np.linspace(1.8, 3.0, 61)
    ax[1].hist(plain, bins=bins, density=True, color=labs.RED, alpha=0.6, label=f"unweighted: covers {cover_p.mean():.0%}")
    ax[1].hist(weighted, bins=bins, density=True, color=labs.GREEN, alpha=0.6, label=f"weighted: covers {cover_w.mean():.0%}")
    ax[1].axvline(target, color=labs.GOLD, label="target mean")
    ax[1].set(title=f"Covariate shift of {delta}: {reps} source samples of {m}", xlabel="estimated target mean", ylabel="density")
    ax[1].legend(loc="upper center")
    lab.fig = fig
    return lab
