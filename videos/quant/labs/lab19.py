"""Lab 19: a short-rate model prices every bond: Vasicek by formula and by simulation."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import sim, termstructure

TITLE = "One short rate, a whole yield curve"
GOAL = ("Simulate Vasicek's short rate, price zero-coupon bonds as the average of exp(-integral of r), and check "
        "them against the affine formula. Then read the curve's shapes off the model: normal, inverted, humped.")
TASKS = [
    "Switch to CIR (sim.cir_exact, termstructure.cir_zcb). What can the short rate no longer do?",
    "The long yield sits below b. Derive the gap sigma^2 / (2 a^2) and check it at T = 100.",
    "Build a termstructure.HullWhite on a bootstrapped curve and price a caplet with hw.caplet.",
]


def run(seed=0):
    a, b, sigma, r0 = 0.5, 0.04, 0.012, 0.01
    T, n, n_paths = 10.0, 2000, 20000
    r = sim.ou_exact(r0, a, b, sigma, T, n, n_paths, seed=seed)
    dt = T / n
    integral = np.cumsum(0.5 * (r[:, 1:] + r[:, :-1]) * dt, axis=1)  # trapezoid rule along each path
    lab, worst = labs.Lab(), 0.0
    for years in (1, 2, 5, 10):
        i = int(years / dt) - 1
        disc = np.exp(-integral[:, i])
        mc, se = disc.mean(), disc.std() / np.sqrt(n_paths)
        exact = float(termstructure.vasicek_zcb(r0, a, b, sigma, years))
        worst = max(worst, abs(mc - exact) / se)
        lab.row(f"{years}-year zero", f"formula {exact:.5f}   Monte Carlo {mc:.5f} +- {1.96 * se:.5f}   "
                                      f"yield {-100 * np.log(exact) / years:.2f}%")
    long_yield = b - sigma ** 2 / (2 * a ** 2)
    lab.row("Yield as T -> infinity", f"{100 * long_yield:.3f}%   (b minus the convexity term sigma^2 / 2a^2)")
    lab.note = "Under Q the bond price is the expected discount factor; the model's whole curve follows from r0."
    assert worst < 3.5

    mats = np.linspace(0.25, 30, 120)
    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.linspace(0, T, n + 1)
    for path in r[:25]:
        ax[0].plot(t, 100 * path, color=labs.SPOT, lw=0.6, alpha=0.6)
    ax[0].axhline(100 * b, color=labs.P, ls="--", lw=1)
    ax[0].set(title="Vasicek short-rate paths pulled toward b = 4%", xlabel="years", ylabel="short rate, %")
    for start, c, name in ((0.01, labs.GAIN, "r0 = 1%: normal"), (0.0385, labs.P, "r0 = 3.85%: humped"),
                           (0.07, labs.LOSS, "r0 = 7%: inverted")):
        ylds = -np.log(termstructure.vasicek_zcb(start, a, b, sigma, mats)) / mats
        ax[1].plot(mats, 100 * ylds, color=c, label=name)
    ax[1].axhline(100 * long_yield, color=labs.MUTED, ls=":", lw=1)
    ax[1].set(title="The curves the model can draw", xlabel="maturity, years", ylabel="zero yield, %")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
