"""Lab 9: grade and rock, a mine's cash and the option to wait, the cost curve, the supercycle, and the Simon-Ehrlich
wager re-run over every decade since 1900."""

import numpy as np

from explainer.industry.register import get, span
from explainer.industry.works import mine
from videos.coursekit import labs
from videos.industry.industry9.compute import results

TITLE = "Mining and metals: grade, cost, the option to wait, the state and the long cycle"
GOAL = ("Move rock for a tonne of copper at falling grades; run the Works' model mine through its cash flows, break-even "
        "and the option to wait; set four real operations on the copper cost curve; follow Escondida's grade into its "
        "output; read the supercycle in prices and the miners' profits; measure how concentrated critical minerals are; "
        "and re-run Simon and Ehrlich's wager for every ten-year window since 1900.")
TASKS = [
    "Give the Works' model deposit a grade of 0.4% and then 0.7% (mine.Mine(..., grade=...)). How do its first-year "
    "cash cost and break-even price move, and at what copper price would building now beat waiting a year in each case "
    "(mine.wait_value over a grid of prices)?",
    "Re-run Simon and Ehrlich's wager with five-year and twenty-year windows (mine.bet_windows(..., length=5) and "
    "length=20) on the same five metals. Does Ehrlich's share of wins rise or fall with the length of the bet, and why "
    "might it?",
    "From the monthly copper series, find the share of months since 1992 in which copper's real price was above its "
    "September 2026 level. Is today's price high by the standard of the last thirty years, and by the standard of the "
    "century in the intermission?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    E = R["esc"]
    lab.row("Escondida: holes drilled / found on hole / first estimate (Mt at 1.3-1.5%)",
            f"{E['holes']} / 6 / {E['first_estimate']}")
    lab.row("Escondida, year to June 2025: copper / unit cost / EBITDA",
            f"{E['output']:,} kt / ${E['unit_cost']:.2f} a lb / ${E['ebitda']:.1f}bn")
    lo, hi = span("esc.output.2026")
    lab.row("Escondida: feed grade 2025 -> 2026; output guidance 2026; outlook FY27-31",
            f"{E['grade25']:.2f}% -> {E['grade26']:.2f}%; {lo:,.0f}-{hi:,.0f} kt; "
            f"{span('esc.medium')[0]:,.0f}-{span('esc.medium')[1]:,.0f} kt")

    G = R["grade"]
    for g, ore, tot in zip(G["grades"], G["rock"], G["rock_strip"]):
        lab.row(f"rock for one tonne of copper at {g:g}% (ore / with a 2:1 strip)", f"{ore:,.0f} t / {tot:,.0f} t")
    assert abs(mine.rock_per_tonne(1.0, 0.85, 2.0) - G["rock_strip"][2]) < 1e-9

    RR = R["run"]
    M = mine.Mine("Model deposit", ore_mt=600, grade=0.5, mill_mtpa=40, capex=3000)
    assert abs(M.breakeven() - RR["breakeven"]) < 1e-9
    lab.row("Works' model deposit: copper in year one / cash cost first and last year",
            f"{RR['copper']:.0f} kt / ${RR['cost0']:.2f} -> ${RR['cost_end']:.2f}")
    lab.row("Works' model deposit: break-even copper price (8%)", f"${RR['breakeven']:.2f} a pound")
    lab.row("Run it at $4.50: build now (mean, share losing) / wait a year / sell",
            f"${RR['now_mean']:,.0f}m, {100 * RR['now_loss']:.0f}% / ${RR['wait_mean']:,.0f}m / ${RR['sell']:,.0f}m")
    W = R["wait"]
    lab.row("option to wait: building now beats waiting above", f"${W['cross']:.2f} ({W['cross_ratio']:.2f} x break-even)")
    T = R["take"]
    lab.row("the state's share of the model mine's profit (4% royalty, 27% tax)", f"{100 * T['state_share']:.0f}%")

    for name, c, x0, x1 in R["curve"]["points"]:
        lab.row(f"cost curve: {name}", f"${c:.2f} a lb, {x1 - x0:,.0f} kt")
    Wh = R["where"]
    lab.row("China's share of copper mined / refined (2025)",
            f"{100 * Wh['china_mine_share']:.0f}% / {100 * Wh['china_share']:.0f}%")
    lab.row("world copper reserves / years of 2025 mining",
            f"{get('usgs.cu.reserves'):,.0f} Mt / {get('usgs.cu.reserves') / (Wh['world_mine'] / 1000):.0f}")

    I_ = R["iron"]
    lab.row("iron ore: distinct monthly prices a year, before 2008 / after 2009",
            f"{I_['before']:.1f} / {I_['after']:.1f}")
    B = R["boom"]
    lab.row("2002 -> 2011 price multiple: copper / iron ore", f"x{B['cu_rise']:.1f} / x{B['fe_rise']:.1f}")
    Mn = B["miners"]
    lab.row("the bust: Vale 2015 / BHP FY2016 / Rio 2015 profit",
            f"${Mn['VALE'][2015]['profit']:+.1f}bn / ${Mn['BHP'][2016]['profit']:+.1f}bn / ${Mn['RIO'][2015]['profit']:+.1f}bn")
    L = R["lithium"]
    lab.row("lithium carbonate 2021 / 2022 / 2025 (real, $ a tonne)",
            f"{L['price'][2021]:,} / {L['price'][2022]:,} / {L['price'][2025]:,}")
    Au = R["gold"]
    lab.row("gold 2025 / Newmont revenue and net income 2025",
            f"${Au['price'][2025]:,} an oz / ${Au['nem_revenue'][2025]:.1f}bn, ${Au['nem_net'][2025]:.1f}bn")

    Bt = R["bet"]
    lab.row("Simon-Ehrlich basket, 1980 -> 1990, real (USGS yearly values) / the cheque",
            f"${Bt['basket_real']:,.0f} of $1,000 / ${Bt['cheque']:.2f}")
    lab.row(f"ten-year windows {Bt['first']}-{Bt['last'] + 10}: Ehrlich wins",
            f"{Bt['ehrlich']} of {Bt['n']} ({100 * Bt['ehrlich_share']:.0f}%)")
    C = R["call"]
    lab.row("this series' call: Escondida below 1,100 kt in the year to June 2027", f"{100 * C['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    cur = W["curve"]
    ps = [c["price"] for c in cur]
    ax1.plot(ps, [c["now"] / 1000 for c in cur], color=labs.GOLD, lw=1.8, label="build now")
    ax1.plot(ps, [c["wait"] / 1000 for c in cur], color=labs.BLUE, lw=1.8, label="keep the right to build")
    ax1.axhline(0, color=labs.GREY, lw=0.8)
    ax1.axvline(W["breakeven"], color=labs.GREY, ls="--", lw=0.8)
    ax1.axvline(W["cross"], color=labs.RED, ls="--", lw=0.8)
    ax1.set_xlabel("copper price, $ a pound")
    ax1.set_ylabel("value today, $bn")
    ax1.set_title("The option to wait (the Works' model deposit)")
    ax1.legend(fontsize=7)
    ys = [y for y, _ in Bt["windows"]]
    rs = np.array([r for _, r in Bt["windows"]])
    ax2.bar(ys, rs - 1, bottom=1, color=[labs.RED if r > 1 else labs.BLUE for r in rs], width=0.9)
    ax2.axhline(1, color="k", lw=0.8)
    ax2.axvline(1980, color=labs.GREY, ls="--", lw=0.8)
    ax2.set_xlabel("first year of the ten-year window")
    ax2.set_ylabel("basket at the end / at the start (real)")
    ax2.set_title("Simon and Ehrlich's bet, every decade")
    lab.fig = fig
    lab.note = ("A mine is a long bet on a price nobody knows, made on rock whose grade only falls; the price swings in "
                "long cycles around a level that barely moves, and the state takes its share throughout.")
    return lab
