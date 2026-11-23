"""Lab 4: price one more unit, fit Wright's law to solar, break even on a seat map and clear America's power stack."""

import numpy as np

from videos.coursekit import labs
from explainer.industry.works import stack as st
from videos.industry.industry4.compute import HOURS, avail, demand, results

TITLE = "The cost curve: marginal cost, utilization, learning and the merit order"
GOAL = ("Take the order below average cost and check the profit; price a megawatt-hour from new plants at every "
        "utilization; fit Wright's law to fifty years of solar prices; rebuild Delta's break-even load factor; and "
        "clear the US power fleet against a day's demand to see which plant sets the price.")
TASKS = [
    "Lower the cost of capital in the plant costs from 7% to 4% (CRF_RATE in the part's compute.py) and recompute a "
    "new reactor's megawatt-hour at 91% utilization. How much of its gap to combined-cycle gas closes?",
    "Fit Wright's law to solar prices from 2010 to 2025 only. Is the learning rate higher or lower than over 2000 to "
    "2025, and what else besides learning could explain the difference?",
    "Raise the gas price in the Stack from $3.85 to $6.00 per million Btu. What is the price at 4 am and at the "
    "evening peak now, and how much more does a nuclear plant keep on each megawatt-hour?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    # 1. The order below average cost: what it changes is what counts
    P = R["plant"]
    gain = P["offer_units"] * (P["offer_price"] - P["variable"])
    assert abs(P["profit_after"] - P["profit"] - gain) < 1e-6 and P["offer_price"] < P["avg_cost"]
    lab.row("the order at $60 against $90 average cost: profit before / after",
            f"${P['profit'] / 1e6:.1f}m / ${P['profit_after'] / 1e6:.1f}m (average cost now ${P['avg_cost_after']:.2f})")

    # 2. A megawatt-hour's cost falls as the plant runs more: fixed cost spread over 8,760 u hours
    L = R["lcoe"]["techs"]
    for k in ("nuclear", "cc2", "solar"):
        t = L[k]
        us = sorted(t["per_mwh"])
        assert all(t["per_mwh"][a] > t["per_mwh"][b] for a, b in zip(us, us[1:]))
        u = t["actual_cf"]
        check = t["fixed_kw_yr"] * 1000 / (HOURS * u) + t["variable"]
        assert abs(check - t["actual"]) < 1e-9
        lab.row(f"{t['name']}: $/MWh at 25% / 95% / as run ({100 * u:.0f}%)",
                f"${t['per_mwh'][0.25]:.0f} / ${t['per_mwh'][0.95]:.0f} / ${t['actual']:.0f}")

    # 3. Wright's law on solar: price against cumulative capacity, 2000-2025
    S = R["solar"]
    yrs = S["years"]
    x = np.log([S["capacity"][y] for y in yrs])
    y = np.log([S["price"][y] for y in yrs])
    slope, icept = np.polyfit(x, y, 1)
    lr = 1 - 2 ** slope
    assert abs(lr - S["fit"]["learning_rate"]) < 1e-6 and 0.2 < lr < 0.4
    lab.row("solar: learning rate per doubling (fit, 2000-2025) / doublings / R^2",
            f"{100 * lr:.1f}% / {S['doublings']:.1f} / {S['fit']['r2']:.2f}")

    # 4. Delta's break-even load factor from its seat-mile statistics
    Q = R["seats"]
    be = Q["casm"] / (Q["trasm"] / Q["load"])
    assert abs(be - Q["break_even"]) < 1e-12 and be < Q["load"]
    points = (Q["load"] - be) * 100
    lab.row("Delta: break-even load factor / flown / points of cushion x $bn a point",
            f"{100 * be:.1f}% / {100 * Q['load']:.0f}% / {points:.1f} x ${Q['per_point']:.2f}bn = "
            f"${points * Q['per_point']:.2f}bn (operating income ${Q['oi']:.2f}bn)")

    # 5. Operating leverage: the hotel and the agency, and Delta in 2020
    F = R["leverage"]["firms"]
    for k in ("hotel", "agency"):
        f = F[k]
        dol = st.operating_leverage(f["fixed"], f["var_share"], 1.0, 100)  # $100m of sales at a price of $1
        assert abs(dol - f["dol"]) < 1e-9
    C = R["leverage"]["covid"]
    lab.row("operating leverage: hotel / agency; Delta 2020 revenue and cost change",
            f"{F['hotel']['dol']:.0f} / {F['agency']['dol']:.0f}; {100 * (C['rev'][1] / C['rev'][0] - 1):.0f}% and "
            f"{100 * (C['cost'][1] / C['cost'][0] - 1):.0f}%")

    # 6. The Stack: the marginal plant sets the price, hour by hour
    B = R["fleet"]["blocks"]
    hours = np.arange(0, 24.01, 0.5)
    prices = []
    for h in hours:
        blocks = [st.Block(b["key"], avail(b["key"], b["gw"], h), b["mc"]) for b in B]
        prices.append(st.clear(blocks, demand(h))["price"])
    peak, trough = int(np.argmax([demand(h) for h in hours])), int(np.argmin([demand(h) for h in hours]))
    assert prices[peak] > prices[trough]
    lab.row("the illustrative day: price low / high / hours at the peakers' price",
            f"${min(prices):.1f} / ${max(prices):.1f} / {0.5 * sum(p >= 46 for p in prices):.1f} h")

    fig, (ax1, ax2) = labs.figure(2)
    cap = [S["capacity"][y] for y in yrs]
    ax1.scatter(cap, [S["price"][y] for y in yrs], color=labs.GOLD, s=18, label="module price, 2000-2025")
    xx = np.geomspace(min(cap), max(cap), 50)
    ax1.plot(xx, np.exp(icept) * xx ** slope, color=labs.GREY, lw=1.2, label=f"Wright's law, {100 * lr:.0f}% a doubling")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("world solar capacity built so far (GW)")
    ax1.set_ylabel("module price ($ per watt, 2025 dollars)")
    ax1.set_title("Solar's learning curve")
    ax1.legend(fontsize=8)
    left = 0.0
    for b in B:
        ax2.bar(left, min(b["mc"], 80), width=b["gw"], align="edge", alpha=0.85, label=b["name"])
        left += b["gw"]
    for h, ls in ((4.0, ":"), (18.0, "--")):
        ax2.axvline(demand(h), color=labs.GREY, ls=ls, lw=1.2)
        ax2.text(demand(h), 70, f"{h:.0f}h", fontsize=7)
    ax2.set_xlabel("installed capacity, cheapest to run first (GW)")
    ax2.set_ylabel("cost of one more MWh ($)")
    ax2.set_title("The US Stack, 2025 (oil cut at $80)")
    ax2.legend(fontsize=6, ncol=2)
    lab.fig = fig
    lab.note = ("Decisions turn on the cost of one more unit; a plant's cost per unit falls with utilization, scale "
                "and experience; and in a market the last unit needed sets the price for everyone, which is how "
                "plants with low running costs pay for themselves.")
    return lab
