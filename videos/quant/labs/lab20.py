"""Lab 20: defaults that arrive together: the one-factor copula, the loss distribution, the tranches."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import credit

TITLE = "Correlation decides who loses: the pool and its tranches"
GOAL = ("Simulate defaults in a pool of 500 loans with one common factor, compare the loss distribution with "
        "Vasicek's large-pool formula, and see how correlation moves expected loss between the equity, mezzanine "
        "and senior tranches of the same pool.")
TASKS = [
    "Use a t copula (nu=4) at the same correlation. Which tranche notices?",
    "Compute Basel's capital with credit.basel_irb_k at PD 1%, 2% and 5%. Why is it concave in PD?",
    "At what correlation does the mezzanine tranche's expected loss peak?",
]

TRANCHES = {"equity 0-3%": (0.0, 0.03), "mezzanine 3-7%": (0.03, 0.07), "senior 7-100%": (0.07, 1.0)}


def run(seed=0):
    pd_, n, R = 0.02, 500, 0.4
    lab = labs.Lab()
    sims = {}
    for rho in (0.05, 0.30):
        counts, _ = credit.copula_defaults(n, pd_, rho, 40000, seed=seed)
        frac = counts / n
        sims[rho] = frac
        q999 = float(credit.vasicek_quantile(0.999, pd_, rho))
        lab.row(f"rho = {rho:.2f}: default rate", f"mean {100 * frac.mean():.2f}%   99.9% quantile simulated "
                                                  f"{100 * np.quantile(frac, 0.999):.1f}%, formula {100 * q999:.1f}%")
        assert abs(frac.mean() - pd_) < 0.002 and abs(np.quantile(frac, 0.999) - q999) < 0.035
    rhos = np.linspace(0.01, 0.6, 40)
    el = {name: np.array([credit.lhp_tranche_el(pd_, r, R, a, d) for r in rhos]) for name, (a, d) in TRANCHES.items()}
    for name in TRANCHES:
        lab.row(f"Expected loss, {name}", f"rho 0.05: {100 * np.interp(0.05, rhos, el[name]):6.3f}%   "
                                          f"rho 0.30: {100 * np.interp(0.30, rhos, el[name]):6.3f}%")
    lab.note = ("Correlation does not change the pool's expected loss; it moves it from the equity tranche to the "
                "senior one. That is why equity is long correlation and senior is short it.")
    assert np.all(np.diff(el["equity 0-3%"]) < 0) and np.all(np.diff(el["senior 7-100%"]) > 0)
    pool = sum(el[name] * (d - a) for name, (a, d) in TRANCHES.items())
    assert np.allclose(pool, pd_ * (1 - R), atol=2e-4), "the tranches add up to the pool"

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(0, 0.2, 81)
    x = np.linspace(0.0005, 0.2, 400)
    for rho, c in ((0.05, labs.GAIN), (0.30, labs.LOSS)):
        ax[0].hist(sims[rho], bins=bins, density=True, color=c, alpha=0.45)
        ax[0].plot(x, credit.vasicek_loss_pdf(x, pd_, rho), color=c, label=f"rho = {rho:.2f}")
    ax[0].set(title="Default rate of the pool: simulation and Vasicek", xlabel="fraction defaulted", ylim=(0, 60))
    ax[0].legend()
    for name, c in zip(TRANCHES, (labs.LOSS, labs.P, labs.SPOT)):
        ax[1].plot(rhos, 100 * el[name], color=c, label=name)
    ax[1].set_yscale("log")
    ax[1].set(title="Expected tranche loss against correlation", xlabel="asset correlation rho", ylabel="% of tranche")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
