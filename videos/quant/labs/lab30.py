"""Lab 30: the optimizer underestimates its own risk; shrinkage gives most of it back."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import portfolio

TITLE = "The minimum-variance portfolio and its broken promise"
GOAL = ("Estimate a covariance matrix from T months of K assets and build the minimum-variance portfolio. Compare "
        "the risk it promises with the risk it delivers as K/T grows, against the exact formulas, then repeat with "
        "Ledoit-Wolf shrinkage and with 1/N.")
TASKS = [
    "Add long_only=True to portfolio.gmv. Why do constraints behave like shrinkage (Jagannathan and Ma)?",
    "Swap lw_identity for lw_constcorr or lw_nonlinear. Which target suits a one-factor market?",
    "Give the assets fat-tailed returns (multivariate t). Do the exact Gaussian formulas still hold?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    T = 120
    lab = labs.Lab()
    Ks = np.array([10, 30, 60, 90, 110])
    rows = {k: [] for k in ("promised", "delivered", "theory_in", "theory_out", "lw", "equal")}
    for K in Ks:
        beta = rng.uniform(0.6, 1.4, K)
        Sigma = np.outer(beta, beta) * 0.04 ** 2 + np.diag(rng.uniform(0.04, 0.09, K) ** 2)
        w_star = portfolio.gmv(Sigma)
        v_min = w_star @ Sigma @ w_star
        sim = portfolio.gmv_sim(Sigma, T, 150, rng)
        th = portfolio.gmv_theory(int(K), T)
        lw, eq = [], np.full(K, 1 / K)
        for _ in range(25):
            R = rng.multivariate_normal(np.zeros(K), Sigma, T)
            w = portfolio.gmv(portfolio.lw_identity(R)[0])
            lw.append(w @ Sigma @ w / v_min)
        for k, v in zip(rows, (np.mean(sim["in"]), np.mean(sim["out"]), th["in"], th["out"], np.mean(lw), eq @ Sigma @ eq / v_min)):
            rows[k].append(v)
        lab.row(f"K = {K:>3} assets, T = 120", f"promised {rows['promised'][-1]:.2f}  delivered {rows['delivered'][-1]:5.2f} "
                                               f"(theory {th['out']:5.2f})   Ledoit-Wolf {rows['lw'][-1]:.2f}   1/N {rows['equal'][-1]:.2f}")
    lab.note = ("Variances relative to the true minimum. The sample optimizer promises (1 - K/T) and delivers "
                "1/(1 - K/T): the gap is the square of that ratio.")
    assert np.allclose(rows["promised"], rows["theory_in"], rtol=0.08) and np.allclose(rows["delivered"], rows["theory_out"], rtol=0.15)
    assert rows["lw"][-1] < 0.5 * rows["delivered"][-1] and rows["lw"][2] < rows["delivered"][2]

    fig, ax = labs.figure(1, size=(9.6, 4.4))
    g = np.linspace(0.02, 0.95, 100)
    ax.plot(g, 1 / (1 - g), color=labs.LOSS, label="delivered: 1 / (1 - K/T)")
    ax.plot(g, 1 - g, color=labs.GAIN, label="promised: 1 - K/T")
    ax.plot(Ks / T, rows["delivered"], "o", color=labs.LOSS)
    ax.plot(Ks / T, rows["promised"], "o", color=labs.GAIN)
    ax.plot(Ks / T, rows["lw"], "s-", color=labs.P, label="Ledoit-Wolf shrinkage, delivered")
    ax.plot(Ks / T, rows["equal"], "^--", color=labs.CASH, label="1/N")
    ax.axhline(1, color=labs.MUTED, lw=0.8)
    ax.set_yscale("log")
    ax.set(title="Variance of the minimum-variance portfolio, relative to the true minimum", xlabel="assets per observation, K/T",
           ylim=(0.05, 30))
    ax.legend(fontsize=8)
    lab.fig = fig
    return lab
