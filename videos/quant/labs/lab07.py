"""Lab 7: fit a GARCH by maximum likelihood and race it against EWMA and a constant."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import vol

TITLE = "Fit a GARCH, then race the forecasts"
GOAL = ("Simulate a GARCH(1,1) market with known parameters, recover them by the House's quasi-maximum "
        "likelihood, and score one-day variance forecasts (GARCH, EWMA, a constant) by QLIKE out of sample.")
TASKS = [
    "Fit kind='gjr' to the same data. Is the asymmetry term distinguishable from zero? Then simulate a GJR market.",
    "Shorten the estimation sample to 500 days. How far do alpha and beta wander across seeds?",
    "Score with vol.mse instead of vol.qlike, then test the difference with vol.diebold_mariano.",
]


def simulate(n, omega, alpha, beta, seed):
    rng = np.random.default_rng(seed)
    r, h = np.empty(n), np.empty(n)
    h[0] = omega / (1 - alpha - beta)
    for t in range(n):
        r[t] = np.sqrt(h[t]) * rng.standard_normal()
        if t + 1 < n:
            h[t + 1] = omega + alpha * r[t] ** 2 + beta * h[t]
    return r, h


def run(seed=0):
    true = (2e-6, 0.08, 0.90)
    r, h = simulate(6000, *true, seed)
    split = 4000
    fit = vol.garch_fit(r[:split])
    omega, alpha, beta = fit["params"]
    garch = vol.garch_filter(fit["params"], r)[split:]
    ewma = vol.ewma(r, 0.94)[split:]
    const = np.full(len(garch), r[:split].var())
    target = r[split:] ** 2
    scores = {name: vol.qlike(f, target).mean() for name, f in (("GARCH", garch), ("EWMA 0.94", ewma),
                                                                ("constant", const))}
    oracle = vol.qlike(h[split:], target).mean()
    lab = labs.Lab()
    lab.row("True alpha, beta", f"{true[1]:.3f}, {true[2]:.3f}")
    lab.row("Fitted alpha, beta", f"{alpha:.3f}, {beta:.3f}   (persistence {fit['persistence']:.3f})")
    for name, s in scores.items():
        lab.row(f"QLIKE out of sample, {name}", f"{s:.4f}")
    lab.row("QLIKE, the true variance", f"{oracle:.4f}")
    lab.note = "QLIKE is minimized in expectation by the true conditional variance; nothing beats the oracle."
    assert abs(alpha - true[1]) < 0.03 and abs(beta - true[2]) < 0.04
    assert oracle <= scores["GARCH"] + 0.005 and scores["GARCH"] < scores["EWMA 0.94"] < scores["constant"]

    fig, ax = labs.figure(2, size=(11, 4.2), gridspec_kw={"width_ratios": [2, 1]})
    days = np.arange(split, split + 600)
    ann = lambda v: 100 * np.sqrt(252 * v)  # noqa: E731
    ax[0].plot(days, ann(h[split:split + 600]), color=labs.INK, lw=1.2, label="true")
    ax[0].plot(days, ann(garch[:600]), color=labs.Q, label="GARCH fit")
    ax[0].plot(days, ann(ewma[:600]), color=labs.REALIZED, lw=1.1, label="EWMA")
    ax[0].set(title="Volatility forecasts out of sample (annualized, %)", xlabel="day")
    ax[0].legend(ncols=3)
    names = list(scores) + ["truth"]
    ax[1].bar(names, list(scores.values()) + [oracle], color=[labs.Q, labs.REALIZED, labs.CASH, labs.INK])
    ax[1].set(title="QLIKE (lower is better)", ylim=(oracle - 0.05, max(scores.values()) + 0.02))
    ax[1].tick_params(axis="x", labelsize=8)
    lab.fig = fig
    return lab
