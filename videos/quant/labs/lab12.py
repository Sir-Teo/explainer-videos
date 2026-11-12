"""Lab 12: a smile in five numbers, the density inside it, and the shape that cannot exist."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import smile, volsurface

TITLE = "Fit a smile, read its density, break it"
GOAL = ("Fit raw SVI to noisy quotes of a skewed one-month smile, differentiate the call prices twice to get the "
        "risk-neutral density, then steepen the wings until Gatheral's g goes negative: a butterfly arbitrage.")
TASKS = [
    "Compute the SVIX with smile.svix2 and compare it with the at-the-money implied variance.",
    "Flip rho to +0.6 (a call skew). Where does the density's mass move?",
    "Find the largest b for which the smile stays arbitrage-free at this rho and s.",
]


def g_of(p, k):
    w = smile.svi_total_variance(k, p["a"], p["b"], p["rho"], p["m"], p["s"])
    h = k[1] - k[0]
    dw, d2w = np.gradient(w, h), np.gradient(np.gradient(w, h), h)
    return volsurface.g_function(k, w, dw, d2w)


def run(seed=0):
    T, F = 1 / 12, 100.0
    true = dict(a=0.002, b=0.012, rho=-0.6, m=0.0, s=0.08)
    rng = np.random.default_rng(seed)
    k_q = np.linspace(-0.25, 0.2, 19)
    iv_q = smile.svi_iv(true, k_q, T) + rng.normal(0, 0.003, k_q.size)  # quotes with 0.3 vol points of noise
    fit = smile.fit_svi(k_q, iv_q ** 2 * T)
    k = np.linspace(-0.45, 0.45, 901)
    K = np.linspace(60, 140, 801)
    dens = smile.risk_neutral_density(fit, F, T, K)
    mass = float(np.sum(dens) * (K[1] - K[0]))
    mean = float(np.sum(K * dens) * (K[1] - K[0]) / mass)
    bad = dict(fit, b=0.16, s=0.004)  # wings near Lee's bound, a kink at the money
    g_fit, g_bad = g_of(fit, k), g_of(bad, k)
    rmse = np.sqrt(np.mean((smile.svi_iv(fit, k_q, T) - smile.svi_iv(true, k_q, T)) ** 2))
    lab = labs.Lab()
    lab.row("Fitted (a, b, rho, m, s)", ", ".join(f"{fit[x]:.4f}" for x in "a b rho m s".split()))
    lab.row("Fit error against the true smile", f"{100 * rmse:.2f} vol points (quote noise 0.30)")
    lab.row("Density: mass, mean", f"{mass:.4f}, {mean:.2f}   (should be 1 and the forward, 100)")
    lab.row("min g, fitted smile", f"{g_fit.min():+.3f}   (no butterfly arbitrage)")
    lab.row("min g, steepened smile", f"{g_bad.min():+.3f}   (negative: a butterfly with negative price)")
    lab.note = "The density is the second strike-derivative of the call price (Breeden-Litzenberger)."
    assert rmse < 0.004 and abs(mass - 1) < 0.01 and abs(mean - F) < 0.2 and g_fit.min() > 0 > g_bad.min()

    fig, ax = labs.figure(3, size=(12, 3.9))
    ax[0].plot(k_q, 100 * iv_q, "o", color=labs.IMPLIED, ms=4, label="quotes")
    ax[0].plot(k, 100 * smile.svi_iv(fit, k, T), color=labs.Q, label="SVI fit")
    ax[0].set(title="The smile", xlabel="log-moneyness k", ylabel="implied vol, %", xlim=(-0.3, 0.25), ylim=(10, 50))
    ax[0].legend()
    ax[1].fill_between(K, dens, color=labs.Q, alpha=0.35)
    ax[1].plot(K, dens, color=labs.Q)
    lognormal = np.exp(-(np.log(K / F) + 0.5 * fit["a"]) ** 2 / (2 * smile.svi_iv(fit, 0.0, T) ** 2 * T))
    lognormal /= np.sum(lognormal) * (K[1] - K[0])
    ax[1].plot(K, lognormal, color=labs.MUTED, ls="--", label="lognormal at ATM vol")
    ax[1].set(title="The density the smile implies", xlabel="strike", xlim=(75, 120))
    ax[1].legend(fontsize=8)
    ax[2].plot(k, g_fit, color=labs.GAIN, label="fitted")
    ax[2].plot(k, g_bad, color=labs.LOSS, label="steepened")
    ax[2].axhline(0, color=labs.MUTED, lw=0.8)
    ax[2].set(title="Gatheral's g: negative means arbitrage", xlabel="log-moneyness k", ylim=(-3, 3), xlim=(-0.2, 0.2))
    ax[2].legend(fontsize=8)
    lab.fig = fig
    return lab
