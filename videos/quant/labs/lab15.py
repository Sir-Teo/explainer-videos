"""Lab 15: a barrier watched once a day, and a snowball note priced by simulation."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import bs, exotics

TITLE = "Barriers, and what a snowball buyer has sold"
GOAL = ("Price a down-and-out call three ways (closed form, daily-monitored Monte Carlo, closed form with the "
        "Broadie-Glasserman-Kou shift), then value a snowball note across volatilities and spot levels.")
TASKS = [
    "Monitor weekly instead of daily. Does the shifted-barrier formula still match the simulation?",
    "Find the snowball's fair coupon with exotics.fair_coupon at 15%, 20% and 25% volatility.",
    "Value the note at S = 0.80 with knocked_in=True against knocked_in=False. What is the barrier worth?",
]


def run(seed=0):
    S0, K, H, T, sigma, n = 100.0, 100.0, 90.0, 0.5, 0.25, 126
    paths = exotics.gbm_paths(S0, sigma, T, n, 200000, seed=seed)
    alive = paths.min(axis=0) > H
    payoff = np.where(alive, np.maximum(paths[-1] - K, 0), 0.0)
    mc, se = payoff.mean(), payoff.std() / np.sqrt(payoff.size)
    cont = float(exotics.down_out_call(S0, K, H, T, sigma))
    shifted = float(exotics.down_out_call(S0, K, exotics.bgk_barrier(H, S0, sigma, T / n), T, sigma))
    lab = labs.Lab()
    lab.row("Vanilla call", f"{bs.price(S0, K, T, sigma):.3f}")
    lab.row("Down-and-out, continuous barrier", f"{cont:.3f}")
    lab.row("Down-and-out, watched daily (MC)", f"{mc:.3f} +- {1.96 * se:.3f}")
    lab.row("Continuous formula, barrier shifted", f"{shifted:.3f}   (barrier {exotics.bgk_barrier(H, S0, sigma, T / n):.2f})")
    vols = np.array([0.10, 0.15, 0.20, 0.25, 0.30, 0.40])
    note = np.array([exotics.snowball_price(v, n_paths=20000, seed=seed) for v in vols])
    lab.row("Snowball note value by volatility", "  ".join(f"{v:.0%}: {x:.3f}" for v, x in zip(vols, note)))
    lab.note = "The note falls as volatility rises: the buyer has sold a down-and-in put and is paid a coupon for it."
    assert abs(mc - shifted) < 3 * se + 0.01 and mc - cont > 5 * se, "daily monitoring knocks out less often"
    assert np.all(np.diff(note) < 0)

    fig, ax = labs.figure(2, size=(11, 4.2))
    spots = np.linspace(86, 125, 200)
    ax[0].plot(spots, bs.price(spots, K, T, sigma), color=labs.CASH, label="vanilla call")
    ax[0].plot(spots, exotics.down_out_call(spots, K, H, T, sigma), color=labs.OPTION, label="down-and-out at 90")
    ax[0].axvline(H, color=labs.LOSS, ls="--", lw=0.9)
    ax[0].plot(S0, mc, "o", color=labs.P, label="daily-monitored MC")
    ax[0].set(title="A barrier removes value near it", xlabel="spot", ylabel="price")
    ax[0].legend(fontsize=8)
    ax[1].plot(100 * vols, note, "o-", color=labs.OPTION)
    ax[1].axhline(1.0, color=labs.MUTED, ls=":", lw=1)
    ax[1].set(title="Snowball (15% coupon, 103/75 barriers) against volatility", xlabel="volatility, %",
              ylabel="value per 1 of notional")
    lab.fig = fig
    return lab
