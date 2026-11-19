"""Lab 2: tax the pit from either side, cap and floor its price, and check the answers against the formulas."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import curves as cv
from explainer.economics.agora import market as mk
from explainer.economics.island import truths

TITLE = "The scissors: who pays a tax, and what a price control costs"
GOAL = ("Run Part 1's pit with a 40-cent tax paid by the sellers and then by the buyers, and with a price cap and a "
        "price floor. Measure what buyers pay, what sellers keep, how many units trade and how much of the possible "
        "gain is made; then check the incidence and the losses against the straight-line formulas of agora.curves.")
TASKS = [
    "Make demand steeper: multiply every buyer's distance from $2.25 by three. Who bears more of the tax now, and "
    "does the pit agree with the formula's direction?",
    "Raise the cap from $2.00 to $2.15, then to $2.25. At what cap does the lottery loss vanish, and why there?",
    "Replace the learning traders with zero-intelligence ones under the cap. Their efficiency is higher than the "
    "learners'. Explain why random bids ration the scarce units better than bids that all sit at the cap.",
]


def run(seed=0):
    lab = labs.Lab()
    pit = truths(1)["pit"]
    t2 = truths(2)
    m = mk.Market(values=pit["values"], costs=pit["costs"])
    eq = m.equilibrium()
    t = t2["tax"]
    runs = 24

    def last(kind="zip", **kw):
        rs = [mk.double_auction(m, kind, periods=6, seed=1000 * seed + r, **kw)["periods"][-1] for r in range(runs)]
        return {k: float(np.nanmedian([x[k] for x in rs])) for k in ("paid", "received", "n", "efficiency")}

    s, b = last(tax=t, tax_on="sell"), last(tax=t, tax_on="buy")
    lab.row("no tax: band", f"${eq['p_lo']:.2f} to ${eq['p_hi']:.2f}, {eq['q']} units")
    lab.row("tax on sellers: buyers pay / sellers keep", f"${s['paid']:.3f} / ${s['received']:.3f}, {s['n']:.0f} units")
    lab.row("tax on buyers: buyers pay / sellers keep", f"${b['paid']:.3f} / ${b['received']:.3f}, {b['n']:.0f} units")
    assert abs(s["paid"] - b["paid"]) < 0.06 and abs(s["received"] - b["received"]) < 0.06, "who remits does not matter"
    assert s["n"] == b["n"] == eq["q"] - 1
    lost = eq["surplus"] - (s["efficiency"] * eq["surplus"])
    lab.row("deadweight loss of the tax", f"${lost:.2f} (the sixth pair's gain: ${m.v[5] - m.c[5]:.2f})")

    L = cv.Linear.from_crowd(400, 6.0, 0.5, 5.0)
    el = L.elasticity()
    tx = L.tax(t)
    share = cv.buyers_share(el["demand"], el["supply"])
    lab.row("fish market: buyers' share of a 40-cent tax", f"{100 * tx['buyers_share']:.1f}% (formula "
                                                           f"{100 * share:.1f}%)")
    assert abs(tx["buyers_share"] - share) < 1e-9

    cap, lo = t2["cap"], t2["minimum"]
    k = int((m.c <= cap).sum())
    want = m.v[m.v >= cap]
    best = (m.v[:k].sum() - m.c[:k].sum()) / eq["surplus"]
    lottery = (k * want.mean() - m.c[:k].sum()) / eq["surplus"]
    c_ = last(cap=cap)
    lab.row(f"cap at ${cap:.2f}: efficiency (best / lottery / pit)",
            f"{100 * best:.1f}% / {100 * lottery:.1f}% / {100 * c_['efficiency']:.1f}%")
    assert abs(c_["efficiency"] - lottery) < 0.05 < best - lottery, "the pit rations by lottery"
    k2 = int((m.v >= lo).sum())
    sell = m.c[m.c <= lo]
    f_ = last(minimum=lo)
    best2 = (m.v[:k2].sum() - m.c[:k2].sum()) / eq["surplus"]
    lot2 = (m.v[:k2].sum() - k2 * sell.mean()) / eq["surplus"]
    lab.row(f"floor at ${lo:.2f}: efficiency (best / lottery / pit)",
            f"{100 * best2:.1f}% / {100 * lot2:.1f}% / {100 * f_['efficiency']:.1f}%")
    assert abs(f_["efficiency"] - lot2) < 0.05
    lab.note = ("A tax falls the same way whoever remits it; a binding control loses the triangle and, when the "
                "scarce side is rationed by whoever calls first, the misallocation on top.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ratio = np.linspace(0, 4, 200)
    ax[0].plot(ratio, 1 / (1 + ratio), color=labs.ORANGE, lw=2.4)
    ax[0].scatter([abs(el["demand"]) / el["supply"]], [tx["buyers_share"]], color=labs.BLUE, zorder=3,
                  label="the Island's fish market")
    ax[0].set(title="Who bears a tax?", xlabel="|demand elasticity| / supply elasticity", ylabel="buyers' share")
    ax[0].legend()
    names = ["best", "lottery", "pit"]
    xs = np.arange(3)
    ax[1].bar(xs - 0.2, [100 * best, 100 * lottery, 100 * c_["efficiency"]], 0.4, color=labs.ORANGE, label="cap $2.00")
    ax[1].bar(xs + 0.2, [100 * best2, 100 * lot2, 100 * f_["efficiency"]], 0.4, color=labs.GREY, label="floor $2.60")
    ax[1].set_xticks(xs, names)
    ax[1].set(title="What a price control costs", ylabel="efficiency, %", ylim=(0, 105))
    ax[1].legend()
    lab.fig = fig
    return lab
