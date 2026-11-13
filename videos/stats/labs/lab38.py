"""Lab 38: simulate the Dickey-Fuller statistic and see the normal critical value fail at a unit root."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import ts

TITLE = "The unit-root test has its own distribution"
GOAL = ("Simulate 4,000 random walks of length 100 and 4,000 stationary AR(1) series, compute the t statistic of the "
        "autoregressive coefficient against its true value in each, and compare both histograms with the standard "
        "normal and with MacKinnon's Dickey-Fuller critical value.")
TASKS = [
    "Set phi to 0.95 and 0.99 in the stationary run. How large must T be before the normal approximation is usable?",
    "Regress one random walk on another, independent one (np.polyfit or ols) and count how often |t| > 1.96.",
    "Add a linear trend to the test (trend='ct') and compare the simulated 5% point with ts.df_critical(T, 0.05, 'ct').",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    T, reps, phi = 100, 4000, 0.5
    t_unit, t_stat = np.empty(reps), np.empty(reps)
    for r in range(reps):
        e = rng.standard_normal(T + 1)
        t_unit[r] = ts.adf(np.cumsum(e))["t"]  # H0: gamma = phi - 1 = 0, which is true
        x = np.empty(T + 1)
        x[0] = e[0] / np.sqrt(1 - phi ** 2)
        for i in range(1, T + 1):
            x[i] = phi * x[i - 1] + e[i]
        a = ts.adf(x)
        t_stat[r] = (a["gamma"] - (phi - 1)) / (a["gamma"] / a["t"])  # t against the true gamma = -0.5
    crit = ts.df_critical(T, 0.05, "c")
    q_unit, q_stat = np.quantile(t_unit, 0.05), np.quantile(t_stat, 0.05)
    rej_normal, rej_mack = np.mean(t_unit < -1.645), np.mean(t_unit < crit)
    rej_stat, rej_stat2 = np.mean(t_stat < -1.645), np.mean(np.abs(t_stat) > 1.96)

    lab = labs.Lab()
    lab.row("random walk: 5% point of the t statistic", f"{q_unit:.2f}   (MacKinnon {crit:.2f}, normal -1.645)")
    lab.row("random walk: mean of the t statistic", f"{t_unit.mean():.2f}   (normal theory 0)")
    lab.row("random walk: rejections at -1.645", f"{rej_normal:.1%}   (nominal 5%)")
    lab.row("random walk: rejections at MacKinnon's value", f"{rej_mack:.1%}   (nominal 5%)")
    lab.row("AR(1), phi = 0.5: 5% point of the t statistic", f"{q_stat:.2f}   (normal -1.645)")
    lab.row("AR(1), phi = 0.5: rejections at -1.645", f"{rej_stat:.1%}   (nominal 5%; the small-sample bias of phi-hat)")
    lab.row("AR(1), phi = 0.5: rejections at |t| > 1.96", f"{rej_stat2:.1%}   (nominal 5%)")
    lab.note = ("At a unit root the t statistic converges to a functional of Brownian motion, shifted well to the left "
                "of the normal: the normal cutoff rejects nearly half of all true random walks, and the Dickey-Fuller "
                "table restores the size. Away from the unit root the normal is close, apart from a "
                "small leftward shift that shrinks as T grows.")
    assert abs(q_unit - crit) < 0.12, "the simulated 5% point matches MacKinnon's"
    assert 0.40 < rej_normal < 0.51, "the normal critical value rejects about 45% of true unit roots"
    assert abs(rej_mack - 0.05) < 0.015, "MacKinnon's value has size 5%"
    assert abs(rej_stat2 - 0.05) < 0.025 and rej_stat < 0.14, "under stationarity the normal is about right"

    fig, ax = labs.figure(2, size=(11, 4.2), sharey=True)
    grid = np.linspace(-5, 4, 200)
    for a, t, name in ((ax[0], t_unit, "Random walk (phi = 1): the Dickey-Fuller law"),
                       (ax[1], t_stat, "Stationary AR(1), phi = 0.5: nearly normal")):
        a.hist(t, bins=np.linspace(-5, 4, 55), density=True, color=labs.BLUE, alpha=0.6, label="4,000 simulated t statistics")
        a.plot(grid, stats.norm.pdf(grid), color=labs.GOLD, label="standard normal")
        a.axvline(-1.645, color=labs.GOLD, ls="--", lw=1.2, label="normal 5% point, -1.645")
        a.set(title=name, xlabel="t statistic of the coefficient against its true value")
    ax[0].axvline(crit, color=labs.RED, ls="--", lw=1.2, label=f"MacKinnon 5% point, {crit:.2f}")
    ax[0].set_ylabel("density")
    ax[0].set_ylim(0, 0.72)
    ax[0].legend(loc="upper right")
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
