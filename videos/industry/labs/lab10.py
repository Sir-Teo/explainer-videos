"""Lab 10: the food dollar, an acre's arithmetic, a forward sale, Cochrane's treadmill, the margin ladder and the
land."""

import numpy as np

from explainer.industry.works import farm
from videos.coursekit import labs
from videos.industry.industry10.compute import results

TITLE = "Farming and food: price takers, the treadmill, the chain's margins and the land"
GOAL = ("Split a US food dollar by industry; read an acre of corn's costs and returns and its break-even prices; play "
        "three real seasons with a forward sale and storage; run Cochrane's treadmill; line up the chain's profit "
        "margins from fertilizer to supermarket; and see why farmland, not farming, has kept the gains.")
TASKS = [
    "Run farm.treadmill with a demand elasticity of -0.2 and then -1.0 (keeping a 12% gain). How far does the price fall "
    "in each case, and what are the early adopters' and the laggards' profits at the end? Which kind of product, food or "
    "a luxury, is more like each case?",
    "Replay the three seasons (R['run']['seasons']) with a storage cost of 2 cents and then 8 cents a bushel a month "
    "(farm.sell(..., carry=...)). Does the best strategy over the three years change?",
    "From the ERS extract (explainer.industry.data.fetch.read('ers_costs')), compute the 2025 break-even price over all "
    "costs for soybeans and wheat, and compare each with its harvest price. Which crop covered its costs?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("wheat yield since 1961: Mexico / India / Pakistan / world",
            " / ".join(f"x{h[k + '_x']:.1f}" for k in ("Mexico", "India", "Pakistan", "World")))
    d = R["dollar"]
    lab.row(f"US food dollar, {d['year']}: farm share (all / at home / away), cents",
            f"{d['farm']:.1f} / {d['home']:.1f} / {d['away']:.1f}")
    top = list(d["groups"].items())[:4]
    lab.row("the four largest industry groups, cents", ", ".join(f"{k} {v:.1f}" for k, v in top))
    lab.row("work done on farms (crops + livestock), cents", f"{d['groups']['Crops'] + d['groups']['Livestock']:.1f}")

    a = R["acre"]
    acre = farm.Acre("corn", a["yield_bu"], a["op_total"], a["oh_total"], land=a["land"])
    # ERS's own net includes the silage credit and its yield and price are rounded: they agree to a few dollars
    assert abs(acre.net(a["price"]) - a["net"]) < 6
    lab.row(f"corn acre {a['year']}: revenue / operating / overhead / net, $",
            f"{a['revenue']:.0f} / {a['op_total']:.0f} / {a['oh_total']:.0f} / {a['net']:+.0f}")
    lab.row("corn break-even a bushel: cash costs / all costs / price", f"${a['breakeven_op']:.2f} / ${a['breakeven']:.2f} / "
            f"${a['price']:.2f}")
    lab.row("years below zero over all costs: corn / soybeans / wheat",
            " / ".join(f"{a['losing_years'][c]} of {a['n_years'][c]}" for c in ("corn", "soybeans", "wheat")))

    for s in R["run"]["seasons"]:
        lab.row(f"season {s['year']}: expected / actual yield; plant / harvest / June price",
                f"{s['expected']:.0f} / {s['actual']:.0f} bu; ${s['plant']:.2f} / ${s['harvest']:.2f} / ${s['later']:.2f}")
    lab.row("three seasons, profit an acre: no hedge, store / half hedged / all hedged",
            f"${R['run']['totals']['h0_s1']:+.0f} / ${R['run']['totals']['h50_s0']:+.0f} / ${R['run']['totals']['h100_s0']:+.0f}")

    t = farm.treadmill()
    lab.row("treadmill (12% gain, elasticity -0.4): price at the end / adopter / laggard profit",
            f"x{t['price'][-1] / t['price'][0]:.2f} / {100 * t['adopter'][-1]:+.1f}% / {100 * t['laggard'][-1]:+.1f}%")
    tr = R["treadmill"]
    lab.row("US corn yield, 2025 against 1866-1935; farms 1935 / 2025", f"x{tr['maize_x30']:.1f}; {tr['farms_1935']:.2f}m / "
            f"{tr['farms_2025']:.2f}m")
    b = R["bread"]
    lab.row(f"wheat in a 1-lb loaf, {b['month']}: cents / loaf price / share",
            f"{100 * b['wheat_loaf']:.1f} / ${b['bread']:.2f} / {100 * b['share']:.0f}%")
    c = R["traders"]["crush"]
    lab.row("soybean crush margin (world prices), average since 1992 / latest, $ a tonne", f"{c['avg']:.0f} / {c['last']:.0f}")
    lab.row("ADM's profit per dollar of sales, 2016-2025 average", f"{100 * R['traders']['adm_margin']:.1f}%")
    for co in R["chain"]["companies"]:
        if co["ticker"] in ("CF", "DE", "PEP", "HSY", "TSN", "KR"):
            lab.row(f"{co['name']}: profit per dollar, 2021-2025 average", f"{100 * co['margin5']:.1f}%")
    i = R["income"]
    lab.row("net farm income 2022 / 2025 / 2026 forecast, $bn", f"{i['y2022']:.0f} / {i['y2025']:.0f} / {i['y2026']:.0f}")
    lab.row("government payments 2025 / 2026 forecast, $bn", f"{i['gov2025']:.1f} / {i['gov2026']:.1f}")
    l_ = R["land"]
    lab.row("return on farm assets since 1990: from income / from land values", f"{l_['avg_income']:.1f}% / {l_['avg_gains']:.1f}%")
    lab.row("this series' call: 2026 farm share above 2025's", f"{100 * R['call']['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot(t["years"], t["price"] / t["price"][0], color=labs.GOLD, lw=1.8, label="price")
    ax1.plot(t["years"], t["share"], color=labs.GREY, lw=1.2, ls="--", label="share adopted")
    ax1.plot(t["years"], t["adopter"], color=labs.BLUE, lw=1.6, label="adopter's margin")
    ax1.plot(t["years"], t["laggard"], color=labs.RED, lw=1.6, label="laggard's margin")
    ax1.axhline(0, color="k", lw=0.6)
    ax1.set_xlabel("year")
    ax1.set_title("Cochrane's treadmill (the Works)")
    ax1.legend(fontsize=7)
    ys = sorted(l_["ret_income"])
    ax2.bar(ys, [l_["ret_income"][y] for y in ys], color=labs.GOLD, width=0.8, label="from farming")
    ax2.bar(ys, [l_["ret_gains"].get(y, 0) for y in ys], bottom=[max(l_["ret_income"][y], 0) if l_["ret_gains"].get(y, 0) >= 0
                                                                 else 0 for y in ys],
            color=labs.BLUE, width=0.8, label="from land values")
    ax2.axhline(0, color="k", lw=0.6)
    ax2.set_ylabel("% a year")
    ax2.set_title("Return on US farm assets (USDA ERS)")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("Farmers take the price; new methods lower it and pass the gain to eaters; the money stays where things "
                "are hard to copy; and the land keeps the good years.")
    return lab
