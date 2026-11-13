"""Lab 40: estimate a survival probability from censored lifetimes three ways, and check Greenwood's variance."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import survival

TITLE = "Kaplan-Meier against the two easy mistakes"
GOAL = ("Simulate 1,000 studies of 100 exponential lifetimes (mean 10) with independent uniform censoring, and estimate "
        "S(8) by Kaplan-Meier, by dropping the censored, and by counting the censored as deaths; then compare "
        "Greenwood's standard error with the spread of the Kaplan-Meier estimates and check the log-log interval.")
TASKS = [
    "Shorten follow-up (censoring uniform on 0 to 12). Which estimator moves, and what happens to Greenwood's SE?",
    "Make censoring informative: censor the frailest early (c = 0.5 * t for half of those with t < 5). Does Kaplan-Meier survive?",
    "Set n = 20 and compare the coverage of the plain interval (km['plain']) with the log-log interval at S(12).",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, reps, mean, cmax, t0 = 100, 1000, 10.0, 25.0, 8.0
    truth = float(np.exp(-t0 / mean))
    km_hat, se_hat, dropped, as_deaths, covered = (np.empty(reps) for _ in range(5))
    for r in range(reps):
        t, c = rng.exponential(mean, n), rng.uniform(0, cmax, n)
        time, event = np.minimum(t, c), t <= c
        km = survival.kaplan_meier(time, event)
        km_hat[r] = survival.km_at(km, t0)
        se_hat[r] = survival.step_at(t0, km["t"], km["se"], left=0.0)
        lo = survival.step_at(t0, km["t"], km["loglog"][0], left=1.0)
        hi = survival.step_at(t0, km["t"], km["loglog"][1], left=1.0)
        covered[r] = lo <= truth <= hi
        dropped[r] = np.mean(time[event] > t0)  # only the patients whose death was seen
        as_deaths[r] = np.mean(time > t0)  # a censored patient is counted as dead at the censoring time
    censored = (mean / cmax) * (1 - np.exp(-cmax / mean))  # P(C < T) = E exp(-C / mean) for these laws

    lab = labs.Lab()
    lab.row("true S(8)", f"{truth:.3f}")
    lab.row("Kaplan-Meier, mean of 1,000", f"{km_hat.mean():.3f}")
    lab.row("censored dropped", f"{dropped.mean():.3f}")
    lab.row("censored counted as deaths", f"{as_deaths.mean():.3f}")
    lab.row("sd of the KM estimates", f"{km_hat.std(ddof=1):.4f}   (mean Greenwood SE {se_hat.mean():.4f})")
    lab.row("95% log-log interval covers", f"{covered.mean():.1%}")
    lab.row("share censored", f"{censored:.0%}")
    lab.note = ("A censored patient is known to have survived up to the censoring time: Kaplan-Meier uses exactly that "
                "and is unbiased, while both shortcuts throw it away and are biased downward.")
    assert abs(km_hat.mean() - truth) < 0.008, "Kaplan-Meier is (nearly) unbiased under independent censoring"
    assert dropped.mean() < truth - 0.10 and as_deaths.mean() < truth - 0.08, "both shortcuts are biased downward"
    assert abs(se_hat.mean() / km_hat.std(ddof=1) - 1) < 0.08, "Greenwood's SE matches the spread"
    assert abs(covered.mean() - 0.95) < 0.025, "the log-log interval covers"

    # one study for the picture
    t, c = rng.exponential(mean, n), rng.uniform(0, cmax, n)
    time, event = np.minimum(t, c), t <= c
    km = survival.kaplan_meier(time, event)
    grid = np.linspace(0, 20, 400)
    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].fill_between(grid, survival.step_at(grid, km["t"], km["loglog"][0]), survival.step_at(grid, km["t"], km["loglog"][1]),
                       step="post", color=labs.GOLD, alpha=0.2, label="95% log-log band")
    ax[0].step(grid, survival.km_at(km, grid), where="post", color=labs.GOLD, label="Kaplan-Meier")
    ax[0].plot(grid, np.exp(-grid / mean), color=labs.MUTED, ls="--", label="truth")
    ax[0].step(grid, [np.mean(time[event] > g) for g in grid], where="post", color=labs.RED, lw=1.3, label="censored dropped")
    ax[0].step(grid, [np.mean(time > g) for g in grid], where="post", color=labs.ORANGE, lw=1.3, label="censored as deaths")
    cens = time[~event]
    ax[0].plot(cens[cens < 20], survival.km_at(km, cens[cens < 20]), "|", color=labs.GOLD, ms=7)
    ax[0].set(title="One study of 100 patients (ticks: censored)", xlabel="time", ylabel="estimated S(t)", xlim=(0, 20), ylim=(0, 1.02))
    ax[0].legend()
    bins = np.arange(0.095, 0.66, 0.02)  # two percentage points wide, centred on multiples of 1/n
    for x, color, name in ((km_hat, labs.GOLD, "Kaplan-Meier"), (dropped, labs.RED, "censored dropped"),
                           (as_deaths, labs.ORANGE, "censored as deaths")):
        ax[1].hist(x, bins=bins, color=color, alpha=0.6, label=name)
    ax[1].axvline(truth, color=labs.INK, ls="--", lw=1.2, label=f"true S(8) = {truth:.3f}")
    ax[1].set(title="Estimates of S(8) over 1,000 studies", xlabel="estimate", ylabel="studies")
    ax[1].legend()
    lab.fig = fig
    return lab
