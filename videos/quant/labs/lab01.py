"""Lab 1: two markets with the same volatility, one Gaussian and one with clusters and heavy tails."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import stats

TITLE = "Is it a random walk, and is it Gaussian?"
GOAL = ("Simulate a Gaussian walk and a GARCH market with the same variance; run the House's variance-ratio test, "
        "tail estimator and autocorrelations on both.")
TASKS = [
    "Add momentum: r[t] += 0.1 * r[t-1]. Which statistic moves, and which test rejects?",
    "Raise alpha + beta from 0.97 to 0.995. What happens to the Hill estimate and to z against z*?",
    "Aggregate both series to 20-day returns (stats.aggregate) and recompute the excess kurtosis.",
]


def garch(n, omega=3e-6, alpha=0.09, beta=0.88, nu=6.0, seed=0):
    """GARCH(1,1) returns with Student-t shocks scaled to unit variance."""
    rng = np.random.default_rng(seed)
    z = rng.standard_t(nu, n) * np.sqrt((nu - 2) / nu)
    r, h = np.empty(n), omega / (1 - alpha - beta)
    for t in range(n):
        r[t] = np.sqrt(h) * z[t]
        h = omega + alpha * r[t] ** 2 + beta * h
    return r


def run(seed=0):
    n = 6000
    real = garch(n, seed=seed)
    walk = np.random.default_rng(seed + 1).normal(0, real.std(), n)
    lab = labs.Lab()
    out = {}
    for name, r in (("Gaussian walk", walk), ("GARCH market", real)):
        vr = stats.variance_ratio(r, 5)
        out[name] = dict(vr=vr, kurt=stats.excess_kurtosis(r), hill=stats.hill(r), ac1=stats.autocorr(r, 1)[0],
                         ac2=stats.autocorr(r ** 2, np.arange(1, 21)))
        lab.row(name, f"VR(5) {vr['vr']:.3f}  z {vr['z']:+.2f}  z* {vr['z_star']:+.2f}   excess kurtosis "
                      f"{out[name]['kurt']:.1f}   Hill alpha {out[name]['hill']:.1f}")
    lab.note = ("Both are fair games (VR near 1). Only the robust z* is a valid test for the GARCH market: its "
                "variance is predictable, its direction is not.")
    g, w = out["GARCH market"], out["Gaussian walk"]
    lab.row("Autocorrelation at lag 1", f"returns: walk {w['ac1']:+.3f}, GARCH {g['ac1']:+.3f}   squared returns: walk "
                                        f"{w['ac2'][0]:+.3f}, GARCH {g['ac2'][0]:+.3f}")
    assert abs(w["vr"]["z"]) < 3 and abs(g["vr"]["z_star"]) < 3, "neither series has predictable returns"
    assert g["kurt"] > 1 > abs(w["kurt"]) and g["ac2"][0] > 0.1 > abs(w["ac2"][0])

    fig, ax = labs.figure(3, size=(11.5, 3.9))
    for a, r, c, name in ((ax[0], walk, labs.CASH, "Gaussian walk"), (ax[1], real, labs.SPOT, "GARCH market")):
        a.plot(100 * r, color=c, lw=0.5)
        a.set(title=name, xlabel="day", ylabel="return, %", ylim=(-9, 9))
    lags = np.arange(1, 21)
    ax[2].bar(lags - 0.2, w["ac2"], 0.4, color=labs.CASH, label="walk")
    ax[2].bar(lags + 0.2, g["ac2"], 0.4, color=labs.SPOT, label="GARCH")
    ax[2].set(title="Autocorrelation of squared returns", xlabel="lag, days")
    ax[2].legend()
    lab.fig = fig
    return lab
