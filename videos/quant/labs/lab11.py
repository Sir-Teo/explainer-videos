"""Lab 11: gamma against theta: a straddle's day, explained term by term."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import quoting

TITLE = "Gamma against theta: explain a day's P&L"
GOAL = ("Hold a delta-hedged three-month straddle for one day. Split the P&L into gamma, theta and vega for every "
        "possible move, and find the move at which the day breaks even.")
TASKS = [
    "Let implied volatility fall one point on the same day (sig1 = 0.19). How big a move pays for that?",
    "Swap the straddle for strategies['butterfly'] or ['risk reversal']: which Greeks carry the P&L now?",
    "Use quoting.ww_band to get the no-trade band for a 5 bp cost, and count trades with hedge_with_band.",
]


def run(seed=0):
    S0, sigma, dt = 100.0, 0.20, 1 / 252
    legs = quoting.strategies(S0=S0, T=0.25)["straddle"]
    g = quoting.book_greeks(legs, S0, sigma)
    breakeven = S0 * sigma * np.sqrt(dt)
    moves = np.linspace(-4, 4, 161)
    rows = [quoting.pnl_explain(legs, S0, S0 + m, sigma, sigma, dt) for m in moves]
    hedged = {k: np.array([r[k] for r in rows]) for k in ("gamma", "theta", "actual", "delta", "unexplained")}
    net = hedged["actual"] - hedged["delta"]  # the delta-hedged book
    zero = moves[moves > 0][np.argmin(np.abs(net[moves > 0]))]
    lab = labs.Lab()
    lab.row("Straddle Greeks", f"gamma {g['gamma']:.3f}, theta {g['theta'] / 252:+.3f} a day, vega {g['vega'] / 100:.3f} a point")
    lab.row("Breakeven move S sigma sqrt(dt)", f"{breakeven:.2f}   (measured zero of the hedged P&L: {zero:.2f})")
    one = quoting.pnl_explain(legs, S0, S0 + 2.0, sigma, sigma, dt)
    lab.row("A +2 day, hedged", f"gamma {one['gamma']:+.3f}  theta {one['theta']:+.3f}  left over {one['unexplained']:+.4f}")
    lab.note = "Long gamma earns half gamma dS^2 and pays theta; they cancel when the move equals the implied daily move."
    assert abs(zero - breakeven) < 0.06 and abs(one["unexplained"]) < 0.01
    assert abs(g["theta"] / 252 + 0.5 * g["gamma"] * S0 ** 2 * sigma ** 2 * dt) < 1e-3

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(moves, hedged["gamma"], color=labs.GAIN, label="gamma: half gamma dS^2")
    ax[0].plot(moves, hedged["theta"], color=labs.LOSS, label="theta: one day of decay")
    ax[0].plot(moves, net, color=labs.INK, lw=2.2, label="delta-hedged P&L")
    for x in (-breakeven, breakeven):
        ax[0].axvline(x, color=labs.P, ls="--", lw=0.9)
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title="One day of a hedged straddle", xlabel="move in the stock", ylabel="P&L")
    ax[0].legend(fontsize=8)
    rng = np.random.default_rng(seed)
    for vol, c, name in ((0.15, labs.LOSS, "realized 15%"), (0.20, labs.CASH, "realized 20%"), (0.25, labs.GAIN, "realized 25%")):
        dS = S0 * vol * np.sqrt(dt) * rng.standard_normal(20000)
        pnl = np.interp(dS, moves, net)
        ax[1].hist(pnl, bins=np.linspace(-0.07, 0.3, 80), color=c, alpha=0.6, label=f"{name}: mean {pnl.mean():+.3f}")
    ax[1].set(title="A day's hedged P&L when realized differs from implied", xlabel="P&L")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
