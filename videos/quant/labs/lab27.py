"""Lab 27: double descent: out-of-sample risk of ridge and of the interpolator, theory against simulation."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import ml

TITLE = "Double descent, and why returns need the ridge"
GOAL = ("Fit linear models with more and more parameters to 200 observations at a return-like signal-to-noise "
        "ratio. Compare the minimum-norm interpolator and ridge with the random-matrix prediction of their "
        "out-of-sample risk.")
TASKS = [
    "Raise the signal (r2 = 5). Where is the ridgeless risk now smallest: at few parameters or at many?",
    "Scan the penalty at P/N = 2. Is the optimum near s2 * gamma / r2, as the theory says?",
    "Feed ml.rff features of a nonlinear signal instead of an exactly linear one. Does the picture survive?",
]


def run(seed=0):
    N, r2, s2 = 200, 1.0, 4.0  # one part signal to four parts noise
    gammas = np.array([0.1, 0.25, 0.5, 0.75, 0.9, 1.1, 1.25, 1.5, 2.0, 3.0, 5.0])
    grid = np.concatenate([np.linspace(0.05, 0.97, 60), np.linspace(1.03, 5, 80)])
    lab = labs.Lab()
    sims = {}
    for name, lam in (("ridgeless (lam -> 0)", 1e-6), ("ridge, lam = 1", 1.0)):
        sims[name] = np.array([ml.ridge_risk_sim(N, int(g * N), lam, r2, s2, seeds=10).mean() for g in gammas])
    th = {name: np.array([ml.ridge_risk_theory(g, lam, r2, s2)["risk"] for g in gammas])
          for name, lam in (("ridgeless (lam -> 0)", 1e-6), ("ridge, lam = 1", 1.0))}
    for g in (0.5, 0.9, 1.1, 2.0, 5.0):
        i = int(np.argmin(np.abs(gammas - g)))
        lab.row(f"P/N = {g:>3}: risk", f"ridgeless {sims['ridgeless (lam -> 0)'][i]:7.2f} (theory {th['ridgeless (lam -> 0)'][i]:7.2f})   "
                                       f"ridge {sims['ridge, lam = 1'][i]:5.2f} (theory {th['ridge, lam = 1'][i]:5.2f})")
    lab.row("Risk of predicting zero", f"{r2:.2f}")
    lab.note = ("The interpolator explodes at P = N and recovers beyond it; at this signal-to-noise ratio only the "
                "regularized model ever beats predicting zero.")
    rel = np.abs(sims["ridge, lam = 1"] / th["ridge, lam = 1"] - 1)
    assert rel.max() < 0.25 and sims["ridgeless (lam -> 0)"][4] > 10 * r2 and sims["ridge, lam = 1"].min() < r2

    fig, ax = labs.figure(1, size=(9.6, 4.4))
    colors = {"ridgeless (lam -> 0)": labs.LOSS, "ridge, lam = 1": labs.GAIN}
    for name, lam in (("ridgeless (lam -> 0)", 1e-6), ("ridge, lam = 1", 1.0)):
        ax.plot(grid, [ml.ridge_risk_theory(g, lam, r2, s2)["risk"] for g in grid], color=colors[name], label=f"{name}: theory")
        ax.plot(gammas, sims[name], "o", color=colors[name], ms=5)
    ax.axhline(r2, color=labs.MUTED, ls="--", lw=1)
    ax.text(4.2, r2 * 1.12, "predict zero", color=labs.MUTED, fontsize=8)
    ax.axvline(1.0, color=labs.P, ls=":", lw=1)
    ax.set_yscale("log")
    ax.set(title="Out-of-sample risk against model size (dots: simulation, N = 200)", xlabel="parameters per observation, P/N",
           ylabel="excess risk", ylim=(0.3, 200))
    ax.legend(fontsize=8)
    lab.fig = fig
    return lab
