"""Lab 17: what memory does to the mean of a series, and to the regression of one random walk on another."""

import numpy as np
from scipy import signal, stats

from videos.coursekit import labs
from explainer.stats.kit import ts

TITLE = "Statistics on series that remember"
GOAL = ("Simulate an AR(1) with rho = 0.7 four thousand times and compare the spread of its mean with the iid formula "
        "and with (1 + rho)/(1 - rho); then regress two thousand independent random walks on one another, in levels "
        "and in differences, and count the 'significant' slopes.")
TASKS = [
    "Set rho = -0.5. Is the iid interval now too narrow or too wide, and what is the effective sample size?",
    "Replace the random walks by AR(1) series with phi = 0.9. How much of the spurious significance remains?",
    "Use ts.block_bootstrap_means with blocks of 10 on one AR(1) series and compare its SE with the three in the table.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the mean of an AR(1): n observations are worth n (1 - rho)/(1 + rho)
    n, reps, rho = 100, 4000, 0.7
    e = rng.standard_normal((reps, n + 200))
    x = signal.lfilter([1.0], [1.0, -rho], e, axis=1)[:, 200:]  # x_t = rho x_{t-1} + e_t, after a burn-in
    means = x.mean(1)
    sd_true = means.std(ddof=1)
    se_iid = x.std(axis=1, ddof=1) / np.sqrt(n)
    se_nw = np.array([ts.newey_west_se(row) for row in x[:1000]])
    k = np.arange(1, n)
    inflation_n = 1 + 2 * np.sum((1 - k / n) * rho ** k)  # exact for n = 100; tends to (1 + rho)/(1 - rho)
    sd_theory = np.sqrt(inflation_n / (1 - rho ** 2) / n)
    tcrit = stats.t.ppf(0.975, n - 1)
    cover_iid = np.mean(np.abs(means) < tcrit * se_iid)
    cover_nw = np.mean(np.abs(means[:1000]) < 1.96 * se_nw)
    ratio = (sd_true / np.sqrt(np.mean(se_iid ** 2))) ** 2
    lab.row("AR(1), rho = 0.7, n = 100: sd of the mean", f"{sd_true:.3f}   (theory {sd_theory:.3f})")
    lab.row("mean SE: iid formula / Newey-West", f"{se_iid.mean():.3f} / {se_nw.mean():.3f}")
    lab.row("variance inflation over the iid formula", f"{ratio:.2f}   ((1 + rho)/(1 - rho) = {(1 + rho) / (1 - rho):.2f}; "
            f"n_eff = {ts.ar1_neff(n, rho):.1f})")
    lab.row("95% interval covers: iid t / Newey-West", f"{cover_iid:.1%} / {cover_nw:.1%}")
    assert abs(sd_true / sd_theory - 1) < 0.05, "the spread of the mean follows the autocovariances"
    assert 4.3 < ratio < 7.0, "the iid variance is too small by about (1 + rho)/(1 - rho)"
    assert 0.50 < cover_iid < 0.66 and cover_iid + 0.12 < cover_nw < 0.93, "iid breaks; HAC repairs part of it"

    # 2. spurious regression: independent random walks
    m, pairs = 100, 2000
    a = np.array([ts.random_walk(m, rng) for _ in range(pairs)])
    b = np.array([ts.random_walk(m, rng) for _ in range(pairs)])

    def slope_t(u, v):
        u, v = u - u.mean(1, keepdims=True), v - v.mean(1, keepdims=True)
        r = (u * v).sum(1) / np.sqrt((u * u).sum(1) * (v * v).sum(1))
        return r * np.sqrt((u.shape[1] - 2) / (1 - r * r)), r

    t_lev, r_lev = slope_t(a, b)
    t_dif, _ = slope_t(np.diff(a, axis=1), np.diff(b, axis=1))
    rej_lev = np.mean(np.abs(t_lev) > stats.t.ppf(0.975, m - 2))
    rej_dif = np.mean(np.abs(t_dif) > stats.t.ppf(0.975, m - 3))
    lab.row("two independent walks, n = 100: slope 'significant'", f"levels {rej_lev:.1%}   differences {rej_dif:.1%}   (nominal 5%)")
    lab.row("share of pairs with |r| > 0.5 in levels", f"{np.mean(np.abs(r_lev) > 0.5):.1%}")
    assert rej_lev > 0.68, "three quarters of unrelated walks look related"
    assert 0.03 < rej_dif < 0.075, "differencing restores the test's size"
    lab.note = ("Positive autocorrelation leaves the mean unbiased but makes 100 observations worth about 18, and two "
                "unrelated random walks pass a slope test three times in four; differencing brings the test back to 5%.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.linspace(-1.3, 1.3, 200)
    ax[0].hist(means, bins=60, density=True, color=labs.BLUE, alpha=0.6, label="4,000 means of an AR(1)")
    ax[0].plot(grid, stats.norm.pdf(grid, 0, se_iid.mean()), color=labs.RED, label="normal with the iid SE")
    ax[0].plot(grid, stats.norm.pdf(grid, 0, sd_theory), color=labs.GREEN, label="normal with the true sd")
    ax[0].set(title="The mean of 100 remembered observations", xlabel="sample mean (truth 0)", ylabel="density")
    ax[0].legend(loc="upper left")
    bins = np.linspace(-30, 30, 61)
    ax[1].hist(np.clip(t_lev, -30, 30), bins=bins, density=True, color=labs.RED, alpha=0.6, label=f"levels: {rej_lev:.0%} beyond ±2")
    ax[1].hist(t_dif, bins=bins, density=True, color=labs.GREEN, alpha=0.6, label=f"differences: {rej_dif:.0%} beyond ±2")
    ax[1].axvline(-1.98, color=labs.MUTED, ls="--")
    ax[1].axvline(1.98, color=labs.MUTED, ls="--")
    ax[1].set(title="Slope t statistics for two independent random walks", xlabel="t (clipped at ±30)", ylabel="density")
    ax[1].legend()
    lab.fig = fig
    return lab
