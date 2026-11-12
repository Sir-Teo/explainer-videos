"""Lab 10: manufacture a call from stock and cash, and see what the manufacturer earns."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import bs, hedge, paths

TITLE = "Manufacture an option by delta hedging"
GOAL = ("Sell a three-month call at 20% implied volatility and delta-hedge it on ten thousand paths: first when "
        "the stock really moves at 20%, then when it moves at 25%, then with fewer and fewer rebalances.")
TASKS = [
    "Hedge once a day but charge 10 bp per trade (cost=0.001). How much of the premium do costs eat?",
    "Price at bs.leland_vol(0.20, 0.002, 1/252) instead of 20%: does the mean P&L return to zero?",
    "Give the stock a drift of 30% a year. Does the hedged P&L care? Does the unhedged one?",
]


def run(seed=0):
    S0, K, T, iv, n, n_paths = 100.0, 100.0, 0.25, 0.20, 252, 10000
    premium = bs.price(S0, K, T, iv)
    lab = labs.Lab()
    lab.row("Black-Scholes premium", f"{premium:.3f}")
    out = {}
    for realized in (0.20, 0.25):
        t, S = paths.gbm(S0, 0.08, realized, T, n, n_paths, seed=seed)
        res = hedge.delta_hedge(t, S, K, T, iv, position=-1)
        out[realized] = res["pnl"]
        unhedged = premium - np.maximum(S[:, -1] - K, 0)
        lab.row(f"Realized {realized:.0%}: hedged P&L", f"mean {res['pnl'].mean():+.3f}, sd {res['pnl'].std():.3f}   "
                                                         f"(unhedged sd {unhedged.std():.2f})")
    vega = bs.greeks(S0, K, T, iv)["vega"]
    lab.row("Vega x (20% - 25%)", f"{vega * (0.20 - 0.25):+.3f}   (the first-order loss from selling vol too cheap)")
    sds = {}
    t, S = paths.gbm(S0, 0.08, 0.20, T, n, n_paths, seed=seed + 1)
    for every in (1, 4, 16, 63):
        sds[n // every] = hedge.delta_hedge(t, S, K, T, iv, position=-1, hedge_every=every)["pnl"].std()
    lab.row("Hedging error sd by rebalances", "  ".join(f"{k}: {v:.3f}" for k, v in sds.items()))
    lab.note = "The hedger earns half gamma times (implied variance - realized variance); the error shrinks like 1/sqrt(N)."
    assert abs(out[0.20].mean()) < 0.05 and out[0.20].std() < 0.2 * premium
    assert abs(out[0.25].mean() - vega * (0.20 - 0.25)) < 0.12
    slope = np.polyfit(np.log(list(sds)), np.log(list(sds.values())), 1)[0]
    assert abs(slope + 0.5) < 0.08, "sd of the hedging error scales like N^(-1/2)"

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(-3.5, 1.5, 90)
    ax[0].hist(out[0.20], bins=bins, color=labs.GAIN, alpha=0.75, label="realized 20% = implied")
    ax[0].hist(out[0.25], bins=bins, color=labs.LOSS, alpha=0.75, label="realized 25%")
    ax[0].axvline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title="Seller's hedged P&L, daily rebalancing", xlabel=f"P&L (premium {premium:.2f})")
    ax[0].legend()
    N = np.array(list(sds))
    ax[1].loglog(N, list(sds.values()), "o-", color=labs.P, label=f"measured, slope {slope:.2f}")
    ax[1].loglog(N, sds[252] * np.sqrt(252 / N), color=labs.MUTED, ls="--", label="1/sqrt(N)")
    ax[1].set(title="Hedging error against the number of rebalances", xlabel="rebalances in three months", ylabel="sd of P&L")
    ax[1].legend()
    lab.fig = fig
    return lab
