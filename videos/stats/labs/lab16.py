"""Lab 16: bootstrap Efron's law schools, then break the bootstrap on the maximum of a uniform sample."""

import numpy as np

from videos.coursekit import labs
from explainer.stats import museum
from explainer.stats.kit import bootstrap as bs

TITLE = "The bootstrap, where it works and where it fails"
GOAL = ("Resample the 15 law schools to get the standard error of their correlation without a normal model, then "
        "resample 50 draws from Uniform(0, 1) and watch the bootstrap of the maximum pile up on one value, so that "
        "the percentile interval never covers.")
TASKS = [
    "Replace the correlation by Spearman's (ranks.spearman). Is its bootstrap standard error larger or smaller?",
    "Resample m = 10 of the n = 50 uniform draws and compare m(max - max*) with n(1 - max): does the spike shrink?",
    "Change the statistic from the maximum to the median. Does the percentile interval's coverage recover?",
]


def corr(x, y):
    return np.corrcoef(x, y)[0, 1]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the law schools: bootstrap and jackknife standard errors of r
    lsat, gpa = np.array(museum.LAW_LSAT, float), np.array(museum.LAW_GPA, float)
    r = corr(lsat, gpa)
    reps = bs.bootstrap((lsat, gpa), corr, 4000, rng)
    se_boot = reps.std(ddof=1)
    jack = bs.jackknife((lsat, gpa), corr)
    se_normal = (1 - r ** 2) / np.sqrt(len(lsat) - 3)
    lo, hi = bs.percentile_ci(reps)
    lab.row("law schools: r", f"{r:.3f}")
    lab.row("SE of r: normal formula / jackknife / bootstrap", f"{se_normal:.3f} / {jack['se']:.3f} / {se_boot:.3f}")
    lab.row("95% percentile interval for r", f"[{lo:.3f}, {hi:.3f}]")
    assert abs(r - 0.776) < 0.001 and abs(jack["se"] - 0.143) < 0.001, "the film's numbers"
    assert 0.122 < se_boot < 0.148 and se_boot > se_normal, "the bootstrap SE is near 0.135, above the normal formula"

    # 2. the maximum of n uniforms: the spike, and the coverage of two intervals
    n, B, R = 50, 400, 600
    spike_theory = 1 - (1 - 1 / n) ** n
    spikes, cover_max, cover_mean = [], 0, 0
    for _ in range(R):
        x = rng.uniform(0, 1, n)
        xb = x[bs.resample_indices(n, B, rng)]
        mx = xb.max(1)
        spikes.append(np.mean(mx == x.max()))
        a, b = bs.percentile_ci(mx)
        cover_max += a <= 1.0 <= b
        a, b = bs.percentile_ci(xb.mean(1))
        cover_mean += a <= 0.5 <= b
    spike = float(np.mean(spikes))
    lab.row("P*(resampled max = sample max), n = 50", f"{spike:.3f}   (theory {spike_theory:.3f}, limit {1 - np.exp(-1):.3f})")
    lab.row("percentile interval covers: the mean", f"{cover_mean / R:.1%}   (nominal 95%)")
    lab.row("percentile interval covers: the maximum", f"{cover_max / R:.1%}   (nominal 95%)")
    assert abs(spike - spike_theory) < 0.01, "the spike is 1 - (1 - 1/n)^n"
    assert cover_max == 0, "every resampled maximum is below theta"
    assert 0.90 < cover_mean / R < 0.975, "the same interval works for the mean"
    lab.note = ("For a smooth statistic (a correlation, a mean) the resamples imitate the sampling distribution; for "
                "the maximum about 63% of them repeat the sample's own maximum, and the percentile interval never "
                "reaches the truth.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].hist(reps, bins=50, color=labs.BLUE, alpha=0.7)
    ax[0].axvline(r, color=labs.GOLD, label=f"r = {r:.3f}")
    ax[0].axvline(lo, color=labs.MUTED, ls="--", label="2.5% and 97.5% points")
    ax[0].axvline(hi, color=labs.MUTED, ls="--")
    ax[0].set(title=f"Law schools: 4,000 resampled correlations (SE {se_boot:.3f})", xlabel="r*", ylabel="resamples")
    ax[0].legend(loc="center left")
    x = rng.uniform(0, 1, n)
    real = n * (1 - rng.uniform(0, 1, (4000, n)).max(1))
    boot = n * (x.max() - x[bs.resample_indices(n, 4000, rng)].max(1))
    bins = np.linspace(0, 6, 49)
    ax[1].hist(real, bins=bins, density=True, color=labs.GREEN, alpha=0.55, label="real world: n(θ − max)")
    ax[1].hist(boot, bins=bins, density=True, color=labs.RED, alpha=0.55, label="bootstrap world: n(max − max*)")
    ax[1].plot(bins, np.exp(-bins), color=labs.INK, lw=1.2, label="Exponential(1) limit")
    ax[1].set(title="The maximum of 50 uniforms: a spike at zero", xlabel="scaled shortfall", ylabel="density",
              ylim=(0, 3))
    ax[1].legend()
    lab.fig = fig
    return lab
