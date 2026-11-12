"""Lab 6: a persistent predictor with no power still looks like one (Stambaugh's bias)."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import econ

TITLE = "A predictive regression that predicts nothing"
GOAL = ("Regress returns on a persistent predictor whose true slope is zero, five thousand times. Measure the "
        "bias of the slope and how often a nominal 5% t-test rejects, against Stambaugh's formula.")
TASKS = [
    "Set corr_uv = 0. Where does the bias go, and why does the dividend yield not have that luxury?",
    "Let T grow from 60 to 240 to 960 months. Does the bias fall like 1/T?",
    "Apply econ.ivx to one simulated sample and compare its t-statistic with OLS.",
]


def run(seed=0):
    T, rho, corr = 120, 0.98, -0.95
    slopes = econ.simulate_predictive(T, rho, corr, beta=0.0, n=5000, seed=seed)
    theory = econ.stambaugh_bias(rho, cov_uv=corr, var_v=1.0, T=T)
    # the same experiment by hand for the t-statistics
    rng = np.random.default_rng(seed + 1)
    tstats = np.empty(2000)
    for i in range(2000):
        v = rng.standard_normal(T + 1)
        u = corr * v + np.sqrt(1 - corr ** 2) * rng.standard_normal(T + 1)
        x = np.zeros(T + 1)
        for t in range(T):
            x[t + 1] = rho * x[t] + v[t + 1]
        fit = econ.ols(u[1:], x[:-1])
        tstats[i] = fit["t"][1]
    reject = np.mean(np.abs(tstats) > 1.96)
    lab = labs.Lab()
    lab.row("True slope", "0")
    lab.row("Mean estimated slope", f"{slopes.mean():+.4f}   (Stambaugh's formula {theory:+.4f})")
    lab.row("Nominal 5% test rejects", f"{100 * reject:.1f}% of samples")
    lab.note = "Ten years of monthly data, a predictor as persistent as the dividend yield, shocks correlated -0.95."
    assert abs(slopes.mean() - theory) < 0.3 * abs(theory) and reject > 0.08

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].hist(slopes, bins=70, color=labs.SPOT)
    ax[0].axvline(0, color=labs.MUTED, lw=1)
    ax[0].axvline(slopes.mean(), color=labs.P, ls="--", label="mean estimate")
    ax[0].axvline(theory, color=labs.LOSS, ls=":", label="Stambaugh's bias")
    ax[0].set(title="Estimated slope when the truth is zero", xlabel="slope")
    ax[0].legend()
    grid = np.linspace(-4, 6, 200)
    ax[1].hist(tstats, bins=60, density=True, color=labs.SPOT)
    ax[1].plot(grid, np.exp(-grid ** 2 / 2) / np.sqrt(2 * np.pi), color=labs.P, label="standard normal")
    ax[1].set(title=f"t-statistics: {100 * reject:.0f}% beyond 1.96", xlabel="t")
    ax[1].legend()
    lab.fig = fig
    return lab
