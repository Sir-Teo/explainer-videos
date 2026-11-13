"""Lab 59: check two exact proportional-regime predictions: the ridgeless risk curve and AMP's state evolution."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import amp

TITLE = "Double descent and state evolution, theory against simulation"
GOAL = ("Fit minimum-norm least squares with p/n from 0.5 to 4 and compare its excess risk with the limiting "
        "formula, peak included; then run approximate message passing for the lasso on one random problem and "
        "compare its noise level at every iteration with the scalar recursion of state evolution.")
TASKS = [
    "Add the penalty lam = gamma/snr to ridge_sim's list at every gamma and overlay amp.optimal_ridge_risk. Where has the peak gone?",
    "Lower delta = n/p from 0.5 to 0.2 at eps = 0.05. Does state evolution still reach a small fixed point, and does AMP follow it?",
    "Replace the Gaussian matrix A by random signs divided by sqrt(n). State evolution was proved for Gaussian entries: does AMP still track it?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. ridgeless least squares: excess risk E||b - beta||^2 at ratio gamma = p/n, signal ||beta||^2 = 4, noise 1
    n, snr = 160, 4.0
    gammas = np.array([0.5, 0.8, 1.25, 2.0, 4.0])
    reps = [8, 14, 10, 2, 2]  # most where the risk is most variable, near p = n
    sim = np.array([amp.ridge_sim(n, g, snr, [0.0], r, rng)[0] for g, r in zip(gammas, reps)])
    theory = amp.ridgeless_risk(gammas, snr)
    for g, s, t in zip(gammas, sim, theory):
        lab.row(f"min-norm risk at p/n = {g:g}", f"{s:.2f}   limit {t:.2f}")
    opt_sim = amp.ridge_sim(n, 0.5, snr, [0.5 / snr], 10, rng)[0]
    opt = amp.optimal_ridge_risk(0.5, snr)
    lab.row("ridge at the optimal penalty, p/n = 0.5", f"{opt_sim:.3f}   limit {opt:.3f}")

    # 2. AMP for the lasso against state evolution: n = 1500, p = 3000, 5% of the signal is +-1
    nn, p, eps, sigma2, theta = 1500, 3000, 0.05, 0.01, 1.5
    A = rng.standard_normal((nn, p)) / np.sqrt(nn)
    x0 = np.zeros(p)
    x0[rng.choice(p, int(eps * p), replace=False)] = rng.choice([-1.0, 1.0], int(eps * p))
    y = A @ x0 + np.sqrt(sigma2) * rng.standard_normal(nn)
    fit = amp.amp_lasso(A, y, theta, iters=20)
    tau2 = np.array(fit["tau"]) ** 2
    se = amp.state_evolution(nn / p, eps, sigma2, theta, iters=20)
    mse = np.mean((fit["x"] - x0) ** 2)
    mse_se = (nn / p) * (se[-1] - sigma2)
    for t in (1, 3, 10):
        lab.row(f"AMP noise level tau^2 at iteration {t}", f"{tau2[t]:.4f}   state evolution {se[t]:.4f}")
    lab.row("mean squared error after 20 iterations", f"{mse:.4f}   state evolution's fixed point {mse_se:.4f}")
    lab.note = ("With p proportional to n the risk has an exact limit, infinite at p = n and falling again beyond it, "
                "and a p-dimensional algorithm is tracked by a one-dimensional recursion, constants included.")
    assert np.all(np.abs(sim / theory - 1) < 0.3), "the ridgeless risk matches its limit on both sides of the peak"
    assert sim[1] > 2.5 * sim[0] and sim[2] > 1.3 * sim[3], "double descent: up toward p = n, then down beyond it"
    assert abs(opt_sim / opt - 1) < 0.3 and opt_sim < sim[0], "the optimal ridge penalty beats least squares"
    assert np.max(np.abs(tau2[:12] / se[:12] - 1)) < 0.2, "AMP follows state evolution iteration by iteration"
    assert abs(mse / mse_se - 1) < 0.3, "and ends at its fixed point"

    fig, ax = labs.figure(2, size=(11, 4.2))
    lo, hi = np.linspace(0.05, 0.97, 200), np.linspace(1.03, 5, 300)
    for k, g in enumerate((lo, hi)):
        ax[0].plot(g, amp.ridgeless_risk(g, snr), color=labs.GOLD, label="limit: min-norm least squares" if k == 0 else None)
    gg = np.linspace(0.05, 5, 200)
    ax[0].plot(gg, [amp.optimal_ridge_risk(g, snr) for g in gg], color=labs.GREEN, label="limit: ridge at the optimal penalty")
    ax[0].plot(gammas, sim, "o", color=labs.BLUE, label=f"simulated min-norm, n = {n}")
    ax[0].axvline(1, color=labs.MUTED, ls="--", lw=1)
    ax[0].set(title="Double descent: excess risk against p/n", xlabel="p/n", ylabel="excess risk", ylim=(0, 10))
    ax[0].legend(loc="upper right")
    it = np.arange(len(se))
    ax[1].plot(it, se, color=labs.GOLD, label="state evolution (scalar recursion)")
    ax[1].plot(it[:len(tau2)], tau2, "o", color=labs.BLUE, ms=4, label=f"AMP on one {nn} x {p} problem")
    ax[1].axhline(sigma2, color=labs.MUTED, ls="--", lw=1, label="noise variance, the floor")
    ax[1].set(title="AMP for the lasso: effective noise by iteration", xlabel="iteration t", ylabel="tau_t squared (log scale)", yscale="log")
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
