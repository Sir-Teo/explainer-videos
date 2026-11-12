"""Lab 33: trade a mean-reverting spread: fit it, choose the band, and check the cube-root law."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import sim, statarb

TITLE = "The optimal band for a mean-reverting spread"
GOAL = ("Simulate an Ornstein-Uhlenbeck spread, recover its speed and equilibrium width by regression, and find "
        "the entry band that maximizes profit per unit time for a given round-trip cost, by formula and by "
        "simulation. Then shrink the cost and watch the band shrink like its cube root.")
TASKS = [
    "Estimate kappa from only 250 observations, 200 times. How biased is it, and what does that do to the band?",
    "Let the spread's mean drift slowly (a random walk in theta). What does the fixed band earn now?",
    "Trade at grid prices (book_at_bands=False) with dt = 1/252. How much does discrete monitoring add?",
]


def run(seed=0):
    kappa, sigma = 12.0, 0.35  # a half-life of about three weeks
    s_eq = sigma / np.sqrt(2 * kappa)
    x = sim.ou_exact(0.0, kappa, 0.0, sigma, 20.0, 5040, 1, seed=seed)[0]
    fit = statarb.ou_fit(x, dt=20.0 / 5040)
    cost = 0.2 * s_eq  # a round trip costs a fifth of the spread's equilibrium sd
    m_star, rate_star = statarb.optimal_band(kappa, sigma, cost)
    bands = np.linspace(0.3, 2.6, 10) * s_eq
    theory = np.array([statarb.band_rate(m, kappa, sigma, cost) for m in bands])
    simulated = np.array([statarb.simulate_band(m, kappa, sigma, cost, T=150.0, dt=1e-4, seed=seed)["rate"] for m in bands])
    lab = labs.Lab()
    lab.row("True kappa, equilibrium sd", f"{kappa:.1f}, {s_eq:.4f}   half-life {252 * np.log(2) / kappa:.0f} days")
    lab.row("Fitted from 20 years of days", f"{fit['kappa']:.1f}, {fit['s_eq']:.4f}")
    lab.row("Optimal band at cost 0.2 sd", f"enter at {m_star / s_eq:.2f} sd; profit rate {rate_star:.3f} a year per unit")
    costs = np.array([0.4, 0.2, 0.1, 0.05, 0.025, 0.0125]) * s_eq
    m_c = np.array([statarb.optimal_band(kappa, sigma, c)[0] for c in costs])
    slope = np.polyfit(np.log(costs[2:]), np.log(m_c[2:]), 1)[0]
    lab.row("Band against cost: fitted exponent", f"{slope:.2f}   (small-cost law: 1/3)")
    lab.note = "Halving the cost does not halve the band: m*/s_eq ~ (3c/s_eq)^(1/3)."
    assert abs(fit["kappa"] - kappa) < 4 and abs(fit["s_eq"] - s_eq) < 0.1 * s_eq
    assert np.abs(simulated - theory).max() < 0.08 * rate_star + 0.02 and 0.27 < slope < 0.42

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.arange(600) / 252
    ax[0].plot(t, x[:600] / s_eq, color=labs.SPOT, lw=0.9)
    for y in (m_star / s_eq, -m_star / s_eq):
        ax[0].axhline(y, color=labs.P, ls="--", lw=1)
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title="The spread and the optimal band", xlabel="years", ylabel="spread, in equilibrium sd")
    ax[1].plot(bands / s_eq, theory, color=labs.P, label="renewal-reward formula")
    ax[1].plot(bands / s_eq, simulated, "o", color=labs.SPOT, ms=4, label="simulated, 150 years")
    ax[1].axvline(m_star / s_eq, color=labs.P, ls=":", lw=1)
    ax[1].axhline(0, color=labs.MUTED, lw=0.8)
    ax[1].set(title="Profit per year against the entry band", xlabel="entry band, in equilibrium sd")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
