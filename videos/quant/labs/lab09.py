"""Lab 9: no arbitrage as a linear program: state prices, an arbitrage found, and a price interval."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import arbitrage

TITLE = "No arbitrage is a linear program"
GOAL = ("Three states, two traded assets: find the state prices the fundamental theorem promises, break a price "
        "and let the solver hand you the arbitrage, then bound a call the market cannot replicate.")
TASKS = [
    "Add the call itself as a third asset at a price inside the interval. What happens to the interval of a put?",
    "Price the call outside its interval and call arbitrage.ftap again: read the arbitrage portfolio it returns.",
    "Go to four states with three assets. How many dimensions does the set of state-price vectors have?",
]


def run(seed=0):
    # rows: assets (bond, stock); columns: states (down, flat, up)
    D = np.array([[1.0, 1.0, 1.0], [80.0, 100.0, 125.0]])
    p = np.array([0.98, 100.0])
    call = np.maximum(D[1] - 100.0, 0.0)
    ok = arbitrage.ftap(D, p)
    bounds = arbitrage.superhedge(D, p, call)
    bad = arbitrage.ftap(D, np.array([0.98, 128.0]))  # a stock dearer than its best outcome, discounted
    lab = labs.Lab()
    lab.row("No arbitrage at (0.98, 100)?", f"{ok['no_arbitrage']}   one set of state prices: {np.round(ok['psi'], 3)}")
    lab.row("Call struck at 100: price interval", f"[{bounds['lower']:.2f}, {bounds['upper']:.2f}]")
    lab.row("Cheapest super-hedge", f"{bounds['theta_up'][0]:+.2f} bonds, {bounds['theta_up'][1]:+.3f} shares")
    lab.row("Stock at 128?", f"no arbitrage: {bad['no_arbitrage']}; portfolio {np.round(bad['theta'], 4)} costs "
                             f"{bad['cost']:+.3f}, pays {np.round(bad['payoff'], 3)}")
    lab.note = "Incomplete market: every price inside the interval is consistent with some risk-neutral measure."
    assert ok["no_arbitrage"] and np.allclose(D @ ok["psi"], p) and (ok["psi"] > 0).all()
    assert not bad["no_arbitrage"] and bad["cost"] <= 1e-9 and (bad["payoff"] >= -1e-9).all()
    assert bounds["lower"] < bounds["upper"]

    # every risk-neutral measure: psi = (a, b, c) > 0 with a + b + c = 0.98 and 80a + 100b + 125c = 100
    c = np.linspace(0, 1, 400)
    b = (100 - 80 * 0.98 - 45 * c) / 20
    a = 0.98 - b - c
    keep = (a > 0) & (b > 0)
    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(c[keep], a[keep], color=labs.LOSS, label="down")
    ax[0].plot(c[keep], b[keep], color=labs.CASH, label="flat")
    ax[0].plot(c[keep], c[keep], color=labs.GAIN, label="up")
    ax[0].set(title="Every state-price vector the two assets allow", xlabel="state price of 'up'", ylabel="state price")
    ax[0].legend()
    price = 25 * c[keep]
    ax[1].plot(c[keep], price, color=labs.Q)
    for y, name in ((bounds["lower"], "sub-hedge"), (bounds["upper"], "super-hedge")):
        ax[1].axhline(y, color=labs.P, ls="--", lw=1)
        ax[1].text(c[keep][0], y, f" {name} {y:.2f}", color=labs.P, va="bottom", fontsize=9)
    ax[1].set(title="The call's price under each of them", xlabel="state price of 'up'", ylabel="call price")
    assert abs(price.min() - bounds["lower"]) < 0.1 and abs(price.max() - bounds["upper"]) < 0.1
    lab.fig = fig
    return lab
