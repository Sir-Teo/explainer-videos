"""Lab 48: test Doob's heuristic, the symmetrization bound, and what estimating parameters does to Kolmogorov-Smirnov."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import empirical

TITLE = "The empirical process: Kolmogorov's law, symmetrization, and estimated parameters"
GOAL = ("Simulate sqrt(n) sup|F_n - F| for n = 5, 20, 100 against the exact finite-n law and the Brownian bridge's "
        "(Kolmogorov's) limit; check E sup|F_n - F| against twice the exact Rademacher average of half-lines; then fit "
        "a normal's mean and SD and compare the process's variance with Durbin's formula.")
TASKS = [
    "Replace the uniform data by Exp(1) data with its true CDF. Why do the three percentiles not change?",
    "Fit only the mean (keep the SD known). Derive the new pointwise variance and check it against the simulation.",
    "For exponential data with an estimated rate use empirical.durbin_variance_exponential, and find the naive KS test's size at n = 50.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    k95 = empirical.kolmogorov_quantile(0.95)

    # 1. Doob's heuristic: sqrt(n) D_n has the law of sup |Brownian bridge| in the limit.
    reps, sims = 20_000, {}
    for n in (5, 20, 100):
        d = np.sqrt(n) * empirical.ks_stats_uniform(rng.random((reps, n)))
        exact = np.sqrt(n) * empirical.ks_band_quantiles(n)["exact"]
        sims[n] = d
        lab.row(f"n = {n}: 95th percentile of sqrt(n) D_n", f"{np.quantile(d, 0.95):.3f}   exact {exact:.3f}   Kolmogorov's limit {k95:.3f}")
        lab.row(f"n = {n}: size of the test that uses the limit", f"{np.mean(d > k95):.1%}   (nominal 5%)")
        assert abs(np.quantile(d, 0.95) - exact) < 0.03, "the simulation matches the exact finite-n law"
        assert exact < k95, "the limit's critical value is conservative at every finite n"
    grid = np.linspace(0.3, 2.2, 96)
    gap = np.max(np.abs(np.mean(sims[100][:, None] <= grid[None, :], axis=0) - empirical.kolmogorov_cdf(grid)))
    bridge = np.max(np.abs(empirical.brownian_bridge(2000, rng, reps=4000)), axis=1)
    lab.row("sup |Brownian bridge|, simulated: 95th percentile", f"{np.quantile(bridge, 0.95):.3f}   (Kolmogorov {k95:.3f})")
    assert gap < 0.04 and abs(np.quantile(bridge, 0.95) - k95) < 0.06, "Doob's heuristic"

    # 2. Symmetrization: E sup |F_n - F| <= 2 R_n, with R_n exact for half-lines.
    for n in (20, 100):
        ed, two_r = sims[n].mean() / np.sqrt(n), 2 * empirical.rademacher_halflines(n)
        lab.row(f"n = {n}: E D_n against 2 R_n", f"{ed:.4f} <= {two_r:.4f}")
        assert ed < two_r, "symmetrization"
    limit = np.sqrt(np.pi / 2) * np.log(2)
    lab.row("sqrt(n) E D_n at n = 100", f"{sims[100].mean():.3f}   (limit sqrt(pi/2) log 2 = {limit:.3f})")
    assert abs(sims[100].mean() - limit) < 0.03

    # 3. Estimated parameters: sqrt(n)(F_n(x) - Phi((x - xbar)/s)) has Durbin's variance, far below F(1 - F).
    n, reps = 200, 20_000
    x = rng.standard_normal((reps, n))
    m, s = x.mean(axis=1, keepdims=True), x.std(axis=1, ddof=1, keepdims=True)
    zs = np.array([-1.5, -0.75, 0.0, 0.75, 1.5])
    var_est = np.array([n * np.var(np.mean(x <= m + z * s, axis=1)) for z in zs])
    var_known = np.array([n * np.var(np.mean(x <= z, axis=1)) for z in zs])
    durbin, binom = empirical.durbin_variance_normal(zs), stats.norm.cdf(zs) * stats.norm.sf(zs)
    lab.row("variance at z = 0: parameters known", f"{var_known[2]:.4f}   (theory {binom[2]:.4f})")
    lab.row("variance at z = 0: mean and SD estimated", f"{var_est[2]:.4f}   (Durbin {durbin[2]:.4f})")
    assert np.all(np.abs(var_est - durbin) < 0.008) and np.all(np.abs(var_known - binom) < 0.012), "Durbin's variance"
    d20 = empirical.ks_estimated_normal_rows(rng.standard_normal((40_000, 20)))
    table = empirical.ks_band_quantiles(20)["exact"]
    lab.row("KS with estimated mean and SD, n = 20: 95% point", f"{np.quantile(d20, 0.95):.3f}   (Kolmogorov's table {table:.3f})")
    lab.row("size of the naive test at nominal 5%", f"{np.mean(d20 > table):.3%}")
    assert abs(np.quantile(d20, 0.95) - 0.192) < 0.006 and np.mean(d20 > table) < 0.002, "the table is far too wide"
    lab.note = ("The scaled largest gap follows the Brownian bridge's law, twice the Rademacher average bounds its mean, "
                "and fitting the parameters shrinks the process so much that Kolmogorov's table almost never rejects.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    t = np.linspace(0.25, 2.2, 300)
    for n, color in ((5, labs.BLUE), (100, labs.GREEN)):
        ax[0].hist(sims[n], bins=60, range=(0.25, 2.2), density=True, histtype="step", lw=1.4, color=color, label=f"sqrt(n) D_n, n = {n}")
    ax[0].plot(t, empirical.kolmogorov_density(t), color=labs.GOLD, label="sup |Brownian bridge| (Kolmogorov)")
    ax[0].axvline(k95, color=labs.RED, ls="--", lw=1, label=f"95% point {k95:.3f}")
    ax[0].set(title="Doob's heuristic: the largest gap, scaled", xlabel="sqrt(n) sup |F_n - F|", ylabel="density")
    ax[0].legend()
    z = np.linspace(-3, 3, 241)
    ax[1].plot(z, stats.norm.cdf(z) * stats.norm.sf(z), color=labs.BLUE, label="parameters known: F(1 - F)")
    ax[1].plot(z, empirical.durbin_variance_normal(z), color=labs.GOLD, label="mean and SD estimated: Durbin")
    ax[1].scatter(zs, var_known, color=labs.BLUE, s=26, zorder=3)
    ax[1].scatter(zs, var_est, color=labs.GOLD, s=26, zorder=3, label="simulated, n = 200")
    ax[1].set(title="Pointwise variance of the empirical process", xlabel="z = (x - mean) / SD", ylabel="variance", ylim=(0, 0.34))
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
