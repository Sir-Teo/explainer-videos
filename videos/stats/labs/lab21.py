"""Lab 21: solve one lasso by ISTA and by FISTA, and certify the answer with KKT and the duality gap."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import optim

TITLE = "ISTA against FISTA, with a certificate"
GOAL = ("Fit a 40-predictor lasso with correlated columns by proximal gradient with and without Nesterov's momentum, "
        "check both against their 1/k and 1/k^2 bounds, and verify the optimum by its KKT conditions and duality gap.")
TASKS = [
    "Raise the correlation rho from 0.9 to 0.99. How do the condition number and the two error curves change?",
    "Replace ISTA by coordinate descent (optim.cd_lasso) and plot its error per sweep on the same axes.",
    "Set lam = 0, where the problem is least squares. Which of the KKT rows changes, and what happens to the gap?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, p, rho, lam, iters = 100, 40, 0.9, 0.1, 400
    z = rng.standard_normal((n, p))
    X = np.empty((n, p))
    X[:, 0] = z[:, 0]
    for j in range(1, p):  # AR(1) columns: neighbours correlate at rho
        X[:, j] = rho * X[:, j - 1] + np.sqrt(1 - rho ** 2) * z[:, j]
    X = (X - X.mean(0)) / X.std(0)
    beta = np.zeros(p)
    beta[[2, 11, 25]] = (2.0, -1.5, 1.0)
    y = X @ beta + rng.standard_normal(n)
    y = y - y.mean()

    ref = optim.cd_lasso(X, y, lam, sweeps=1500)  # the reference optimum, certified below
    b_star, f_star = ref["b"], ref["objective"][-1]
    gap = optim.lasso_dual_gap(X, y, b_star, lam)["gap"]
    grad = X.T @ (y - X @ b_star) / n
    on = b_star != 0
    ista = optim.ista(X, y, lam, iters=iters)
    fista = optim.ista(X, y, lam, iters=iters, accelerate=True)
    L = ista["L"]
    eig = np.linalg.eigvalsh(X.T @ X / n)
    k = np.arange(1, iters + 1)
    d2 = float(b_star @ b_star)  # ||b_0 - b*||^2 from the start b_0 = 0
    err_i, err_f = ista["objective"][1:] - f_star, fista["objective"][1:] - f_star
    bound_i, bound_f = L * d2 / (2 * k), 2 * L * d2 / (k + 1) ** 2
    mid = optim.lasso_dual_gap(X, y, ista["path"][50], lam)["gap"]

    lab = labs.Lab()
    lab.row("condition number of X'X/n", f"{eig[-1] / eig[0]:.0f}")
    lab.row("non-zero coefficients at the optimum", f"{on.sum()} of {p}")
    lab.row("KKT on the support: max | |x_j'r/n| - lam |", f"{np.abs(np.abs(grad[on]) - lam).max():.1e}   (theory 0)")
    lab.row("KKT off the support: max |x_j'r/n|", f"{np.abs(grad[~on]).max():.4f}   (must be <= lam = {lam})")
    lab.row("duality gap at the optimum", f"{gap:.1e}")
    lab.row("ISTA after 50 steps: error, gap", f"{err_i[49]:.2e}, {mid:.2e}   (the gap bounds the error)")
    lab.row(f"error after {iters} steps: ISTA", f"{err_i[-1]:.2e}   (bound {bound_i[-1]:.2e})")
    lab.row(f"error after {iters} steps: FISTA", f"{err_f[-1]:.2e}   (bound {bound_f[-1]:.2e})")
    lab.note = ("Both methods stay under their worst-case bounds, momentum buys orders of magnitude at the same cost "
                "per step, and the duality gap certifies an answer without knowing the optimum.")
    assert 0 <= gap < 1e-9, "the reference is optimal to nine digits"
    assert np.all(np.sign(grad[on]) == np.sign(b_star[on])) and np.abs(np.abs(grad[on]) - lam).max() < 1e-6, "KKT on"
    assert np.abs(grad[~on]).max() <= lam + 1e-9, "KKT off the support"
    assert np.all(err_i <= bound_i + 1e-12) and np.all(err_f <= bound_f + 1e-12), "the 1/k and 1/k^2 bounds hold"
    assert np.all(np.diff(ista["objective"]) <= 1e-12), "ISTA is a descent method"
    assert err_f[-1] < err_i[-1] / 20, "momentum wins"
    assert mid >= err_i[49] - 1e-12, "the duality gap bounds the suboptimality"

    fig, ax = labs.figure(2, size=(11, 4.2))
    floor = 1e-14
    ax[0].loglog(k, np.maximum(err_i, floor), color=labs.BLUE, label="ISTA")
    ax[0].loglog(k, np.maximum(err_f, floor), color=labs.GOLD, label="FISTA")
    ax[0].loglog(k, bound_i, color=labs.BLUE, ls="--", lw=1, label="bound L d² / 2k")
    ax[0].loglog(k, bound_f, color=labs.GOLD, ls="--", lw=1, label="bound 2 L d² / (k+1)²")
    ax[0].set(title="Objective error against its bound", xlabel="step k", ylabel="F(b_k) − F*")
    ax[0].legend()
    idx = np.arange(p)
    ax[1].bar(idx - 0.2, beta, width=0.4, color=labs.MUTED, label="truth")
    ax[1].bar(idx + 0.2, b_star, width=0.4, color=labs.GREEN, label="lasso optimum")
    ax[1].set(title=f"The optimum: {on.sum()} of {p} coefficients are non-zero", xlabel="predictor j",
              ylabel="coefficient")
    ax[1].legend()
    lab.fig = fig
    return lab
