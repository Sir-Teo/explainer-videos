"""Lab 16: the same price from five estimators, and how fast each one converges."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import bs, engine

TITLE = "Monte Carlo, variance reduction and Sobol: the race"
GOAL = ("Price one European call with plain Monte Carlo, antithetic pairs, a control variate, importance sampling "
        "and scrambled Sobol points. Measure each estimator's error across seeds and its rate of convergence.")
TASKS = [
    "Move the strike to 140. Which method gains most, and which loses its advantage?",
    "Price an Asian call with engine.asian_control: how correlated is the geometric control?",
    "Run engine.mlmc(0.01) and compare its cost with a single-level Euler run at the same accuracy.",
]


def sobol_call(S0, K, T, sigma, r, n, seed):
    z = engine.normals(n, 1, "sobol", seed)[:, 0]
    ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * z)
    return float(np.exp(-r * T) * np.maximum(ST - K, 0).mean())


def run(seed=0):
    S0, K, T, sigma, r = 100.0, 110.0, 1.0, 0.2, 0.03
    exact = float(bs.price(S0, K, T, sigma, r))
    ns = 2 ** np.arange(8, 16)
    methods = ["plain", "antithetic", "control", "is", "sobol"]
    rmse = {m: [] for m in methods}
    for n in ns:
        for m in methods:
            if m == "sobol":
                est = [sobol_call(S0, K, T, sigma, r, n, seed + s) for s in range(40)]
            else:
                est = [engine.mc_call(S0, K, T, sigma, r, int(n), m, seed + s)[0] for s in range(40)]
            rmse[m].append(np.sqrt(np.mean((np.array(est) - exact) ** 2)))
    slope = {m: np.polyfit(np.log(ns), np.log(rmse[m]), 1)[0] for m in methods}
    lab = labs.Lab()
    lab.row("Black-Scholes price", f"{exact:.4f}")
    names = {"plain": "plain Monte Carlo", "antithetic": "antithetic pairs", "control": "control variate (the stock)",
             "is": "importance sampling", "sobol": "scrambled Sobol"}
    for m in methods:
        lab.row(names[m], f"RMSE at n = 32,768: {rmse[m][-1]:.5f}   rate n^{slope[m]:+.2f}   "
                          f"variance cut x{(rmse['plain'][-1] / rmse[m][-1]) ** 2:,.0f}")
    lab.note = "Variance reduction changes the constant; only low-discrepancy points change the rate."
    assert all(abs(slope[m] + 0.5) < 0.12 for m in methods[:4]) and slope["sobol"] < -0.8
    assert max(rmse[m][-1] for m in ("antithetic", "control", "is")) < rmse["plain"][-1]
    assert rmse["sobol"][-1] < 0.2 * rmse["plain"][-1]

    colors = dict(zip(methods, (labs.CASH, labs.SPOT, labs.GAIN, labs.P, labs.OPTION)))
    fig, ax = labs.figure(2, size=(11, 4.2))
    for m in methods:
        ax[0].loglog(ns, rmse[m], "o-", color=colors[m], ms=3, label=f"{names[m]} ({slope[m]:+.2f})")
    ax[0].set(title="Error against the number of paths", xlabel="paths n", ylabel="RMSE over 40 seeds")
    ax[0].legend(fontsize=7.5)
    u = np.random.default_rng(seed).random((512, 2))
    from scipy.stats import qmc

    s = qmc.Sobol(2, scramble=True, seed=seed).random(512)
    ax[1].scatter(u[:, 0], u[:, 1] * 0.48, s=5, color=labs.CASH, label="pseudo-random")
    ax[1].scatter(s[:, 0], 0.52 + s[:, 1] * 0.48, s=5, color=labs.OPTION, label="Sobol")
    ax[1].set(title="512 points: random (below) and Sobol (above)", xticks=[], yticks=[])
    ax[1].grid(False)
    lab.fig = fig
    return lab
