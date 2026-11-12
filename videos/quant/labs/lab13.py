"""Lab 13: random volatility makes a smile; its correlation with the stock tilts it."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import bs, stochvol

TITLE = "Heston: the smile from a characteristic function"
GOAL = ("Price six-month options under Heston with the COS method for three spot-vol correlations, check one smile "
        "against a quadratic-exponential Monte Carlo, and read what rho and vol-of-vol do to the shape.")
TASKS = [
    "Set xi = 0.01 with rho = -0.7. What smile is left, and which model is that?",
    "Reprice at T = 1/52 and T = 2. Which parameter controls the short-dated skew, which the long-dated level?",
    "Swap heston_cf for bates_cf with one jump a year of -10%. How does the one-week smile change?",
]


def run(seed=0):
    F, T = 100.0, 0.5
    par = dict(v0=0.04, kappa=2.0, theta=0.04, xi=0.5)
    K = np.linspace(75, 125, 41)
    smiles = {}
    for rho in (-0.7, 0.0, 0.7):
        cf = lambda u, t, rho=rho: stochvol.heston_cf(u, t, par["v0"], par["kappa"], par["theta"], par["xi"], rho)  # noqa: E731
        smiles[rho] = stochvol.model_iv(cf, F, K, T)
    # Monte Carlo check of the rho = -0.7 smile at three strikes
    S = stochvol.heston_qe(F, par["v0"], par["kappa"], par["theta"], par["xi"], -0.7, T, 100, 200000, seed=seed)[-1]
    lab = labs.Lab()
    worst = 0.0
    for k in (85.0, 100.0, 115.0):
        cp = 1 if k >= F else -1
        payoff = np.maximum(cp * (S - k), 0)
        mc, se = payoff.mean(), payoff.std() / np.sqrt(S.size)
        iv_mc = float(bs.implied_vol(mc, F, k, T, cp=cp))
        iv_cos = float(np.interp(k, K, smiles[-0.7]))
        worst = max(worst, abs(iv_mc - iv_cos))
        lab.row(f"K = {k:.0f}: implied vol", f"COS {100 * iv_cos:.2f}%   Monte Carlo {100 * iv_mc:.2f}%  (price se {se:.3f})")
    skew = {rho: (np.interp(105, K, s) - np.interp(95, K, s)) / np.log(105 / 95) for rho, s in smiles.items()}
    lab.row("At-the-money skew d(iv)/d(log K)", "  ".join(f"rho {r:+.1f}: {v:+.3f}" for r, v in skew.items()))
    lab.note = "Negative correlation: volatility rises as the stock falls, so downside strikes cost more."
    assert worst < 0.004 and skew[-0.7] < -0.1 < 0.1 < skew[0.7] and abs(skew[0.0]) < 0.02
    assert smiles[0.0][0] > smiles[0.0][20] < smiles[0.0][-1], "zero correlation: a symmetric smile"

    fig, ax = labs.figure(2, size=(11, 4.2))
    for rho, c in ((-0.7, labs.LOSS), (0.0, labs.CASH), (0.7, labs.GAIN)):
        ax[0].plot(K, 100 * smiles[rho], color=c, label=f"rho = {rho:+.1f}")
    ax[0].axhline(20, color=labs.MUTED, ls=":", lw=1)
    ax[0].set(title="Six-month Heston smiles (xi = 0.5)", xlabel="strike", ylabel="implied vol, %")
    ax[0].legend()
    for xi, c in ((0.2, labs.CASH), (0.5, labs.Q), (0.9, labs.OPTION)):
        cf = lambda u, t, xi=xi: stochvol.heston_cf(u, t, par["v0"], par["kappa"], par["theta"], xi, -0.7)  # noqa: E731
        ax[1].plot(K, 100 * stochvol.model_iv(cf, F, K, T), color=c, label=f"xi = {xi}")
    ax[1].set(title="Vol of vol bends it (rho = -0.7)", xlabel="strike", ylabel="implied vol, %")
    ax[1].legend()
    lab.fig = fig
    return lab
