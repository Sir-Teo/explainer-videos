"""Lab 14: measure roughness, then see what it does to the skew of short-dated options."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import bs, rough, sim

TITLE = "Rough volatility: estimate H, then price the skew"
GOAL = ("Estimate the Hurst exponent of a simulated log-volatility by the scaling of its increments, then price "
        "options under rough Bergomi (H = 0.1) and a nearly Brownian twin (H = 0.49) and compare how the at-the-money "
        "skew grows as maturity shrinks.")
TASKS = [
    "Add measurement noise to log_v (the realized-variance proxy's error). What does it do to the estimated H?",
    "Fit rough.skew_term_fit to the rough skews. Is the bounded alternative distinguishable at these maturities?",
    "Raise eta. Does the skew's exponent change, or only its level?",
]


def atm_skew(S, T, h=0.03):
    """d(implied vol)/d(log strike) at the money from terminal values S (forward 1), by central difference."""
    ivs = []
    for k in (-h, h):
        K = np.exp(k)
        cp = 1 if k > 0 else -1
        price = np.maximum(cp * (S - K), 0).mean()
        ivs.append(float(bs.implied_vol(price, 1.0, K, T, cp=cp)))
    return (ivs[1] - ivs[0]) / (2 * h)


def run(seed=0):
    lab = labs.Lab()
    est = {}
    for H in (0.1, 0.5):
        log_v = sim.fbm(H, 4000, 1.0, 20, seed=seed)
        est[H] = np.mean([rough.log_rv_scaling(x)["H"] for x in log_v])
        lab.row(f"True H = {H}: estimated", f"{est[H]:.3f}   (20 paths of 4,000 points)")
    mats = np.array([1 / 52, 1 / 24, 1 / 12, 1 / 4, 1 / 2])
    skews = {}
    for H in (0.1, 0.49):  # the hybrid scheme needs H < 1/2; 0.49 stands in for a diffusion
        n = 260
        S = rough.rbergomi_paths(H, 1.9 if H < 0.4 else 1.0, -0.9, 0.04, 0.5, n, 60000, seed=seed + 1)
        idx = np.round(mats / 0.5 * n).astype(int)
        skews[H] = np.array([atm_skew(S[i], i * 0.5 / n) for i in idx])
    slope = {H: np.polyfit(np.log(mats), np.log(-s), 1)[0] for H, s in skews.items()}
    lab.row("ATM skew, one week", f"rough {skews[0.1][0]:+.2f}   smooth {skews[0.49][0]:+.2f}")
    lab.row("Skew ~ T^a: fitted a", f"rough {slope[0.1]:+.2f} (theory H - 1/2 = -0.40)   smooth {slope[0.49]:+.2f} "
                                    f"(a diffusion's skew stays bounded as T -> 0)")
    lab.note = "Equity skews in the market grow roughly like T^-0.4 at short maturities: a diffusion cannot do that."
    assert abs(est[0.1] - 0.1) < 0.03 and abs(est[0.5] - 0.5) < 0.05
    assert -0.55 < slope[0.1] < -0.25 and abs(slope[0.49]) < 0.25

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.linspace(0, 1, 4001)
    for H, c in ((0.5, labs.CASH), (0.1, labs.Q)):
        ax[0].plot(t[:1200], sim.fbm(H, 4000, 1.0, 1, seed=seed + 3)[0][:1200], color=c, lw=0.8, label=f"H = {H}")
    ax[0].set(title="Log-volatility paths: Brownian against rough", xlabel="time")
    ax[0].legend()
    ax[1].loglog(mats * 52, -skews[0.1], "o-", color=labs.Q, label=f"rough Bergomi, slope {slope[0.1]:.2f}")
    ax[1].loglog(mats * 52, -skews[0.49], "o-", color=labs.CASH, label=f"H = 0.49, slope {slope[0.49]:.2f}")
    ax[1].set(title="At-the-money skew against maturity", xlabel="maturity, weeks", ylabel="-d(iv)/d(log K)")
    ax[1].legend()
    lab.fig = fig
    return lab
