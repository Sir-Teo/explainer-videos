"""Lab 40: a risk number is a forecast: three VaR models, backtested on a market with clusters and fat tails."""

import numpy as np

from videos.quant import labs
from videos.quant.labs.lab01 import garch
from explainer.quant.house import risk

TITLE = "Backtest a risk model"
GOAL = ("Forecast one-day 99% value at risk three ways on a simulated market with volatility clusters and heavy "
        "tails: a rolling normal, historical simulation, and filtered historical simulation. Count the "
        "exceptions, test their number and their clustering, and compare the expected shortfalls.")
TASKS = [
    "Add 'evt' to the methods (a generalized Pareto tail on GARCH residuals). Is it better at 99.9%?",
    "Scale the one-day VaR to ten days with risk.sqrt_time. When does the square-root rule fail, and in which direction?",
    "Score the forecasts with risk.fz0, the joint VaR-ES loss. Does it rank the models the same way?",
]


def run(seed=0):
    r = garch(6000, seed=seed + 5)
    alpha, start = 0.99, 1000
    out = risk.rolling_forecasts(r, alpha=alpha, window=500, start=start, methods=("normal", "hs", "fhs"))
    names = {"normal": "rolling normal", "hs": "historical simulation", "fhs": "filtered historical"}
    lab, res = labs.Lab(), {}
    for key, name in names.items():
        var, es = np.asarray(out[key]["var"]), np.asarray(out[key]["es"])
        I = risk.hits(r, var)  # forecasts are NaN before `start`; hits skips those days
        k, c = risk.kupiec(I, 1 - alpha), risk.christoffersen(I, 1 - alpha)
        res[key] = dict(var=var[start:], I=I, rate=I.mean(), p_uc=k["p_value"], p_ind=c["p_ind"], ratio=np.nanmean(es / var))
        lab.row(name, f"exceptions {I.sum():>3} of {I.size} ({100 * I.mean():.2f}%; 1% expected)   "
                      f"coverage p = {k['p_value']:.3f}   independence p = {c['p_ind']:.3f}   ES/VaR {res[key]['ratio']:.2f}")
    lab.note = ("The rolling normal fails twice: too many exceptions, and they come in clusters. Filtering by "
                "today's volatility repairs the clustering; the empirical tail repairs the count.")
    assert res["normal"]["rate"] > 0.014 and res["normal"]["p_ind"] < 0.05
    assert abs(res["fhs"]["rate"] - 0.01) < 0.005 and res["fhs"]["p_ind"] > 0.01 and res["fhs"]["ratio"] > res["normal"]["ratio"]

    realized = r[start:]
    fig, ax = labs.figure(2, size=(11, 4.2), gridspec_kw={"width_ratios": [2, 1]})
    days = np.arange(start, start + 1500)
    ax[0].plot(days, 100 * realized[:1500], color=labs.MUTED, lw=0.5)
    for key, c in (("normal", labs.LOSS), ("fhs", labs.GAIN)):
        ax[0].plot(days, -100 * res[key]["var"][:1500], color=c, lw=1.1, label=f"-VaR, {names[key]}")
        hit = np.flatnonzero(res[key]["I"][:1500])
        ax[0].plot(days[hit], 100 * realized[:1500][hit], "o", color=c, ms=3)
    ax[0].set(title="Returns, two 99% VaR forecasts and their exceptions", xlabel="day", ylabel="%", ylim=(-9, 6))
    ax[0].legend(fontsize=8, loc="upper right")
    keys = list(names)
    ax[1].bar([names[k].replace(" ", "\n") for k in keys], [100 * res[k]["rate"] for k in keys],
              color=[labs.LOSS, labs.P, labs.GAIN])
    ax[1].axhline(1.0, color=labs.INK, ls="--", lw=1)
    ax[1].set(title="Exception rate, % (1% promised)")
    ax[1].tick_params(axis="x", labelsize=8)
    lab.fig = fig
    return lab
