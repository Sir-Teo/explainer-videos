"""Lab 12: Haber's arithmetic, a cracker's cost on ethane and on naphtha, the shale advantage, the commodity cycle,
ammonia's gas cost, the gas plant's contract, paint against petrochemicals, Europe's output, plastics and their fate,
and the government's 2005 outlook."""

import numpy as np

from explainer.industry.works import cracker  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry12.compute import results

TITLE = "Chemicals: the cracker, the molecule, the contract and the bill"
GOAL = ("Do Haber's arithmetic; price a tonne of ethylene from ethane and from naphtha, piece by piece; follow the shale "
        "advantage and the Run it cracker's cash; read the commodity cycle in capacity, prices and profits; turn gas "
        "prices into the cost of ammonia; see why a gas plant's contract steadies its cash; compare paint with "
        "petrochemicals; measure Europe's fall in output; and score the government's outlook of 2005.")
TASKS = [
    "With cracker.Cracker('ethane') and cracker.Cracker('naphtha'), find the American gas price at which an ethane "
    "cracker's cash cost equals a naphtha cracker's in Europe at today's European gas and Brent (R['prices']). How far is "
    "that from Henry Hub's history? Repeat with Brent at $50 and at $100.",
    "Change cracker.COPRODUCT_PREMIUM from 1.1 to 0.8 and to 1.4 and rerun the cost breakdown for both feeds. Which "
    "feedstock's cost moves more, and why? What does that say about a naphtha cracker's exposure to propylene and "
    "aromatics prices?",
    "Using R['fertilizer']['per_ton'] and the IMF's monthly gas prices (R['prices']['us_m'] and ['eu_m']), compute the "
    "monthly gas cost of a ton of ammonia in America and Europe since 2019. In how many months did Europe's gas cost "
    "exceed the USGS's annual Gulf price for that year (R['fertilizer']['price'])?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("world ammonia, Mt of N: 1950 / 2025", f"{h['n1950']:.1f} / {h['n2025']:.0f}")
    lab.row("Haber: hydrogen per tonne of N2; ammonia per tonne of N2", f"{h['haber']['hydrogen']:.3f} t / {h['haber']['ammonia']:.3f} t")
    lab.row("nitrogen on a hectare of cropland, kg: first / latest year",
            f"{h['n_ha'][min(h['n_ha'])]:.1f} ({min(h['n_ha'])}) / {h['n_ha'][max(h['n_ha'])]:.1f} ({max(h['n_ha'])})")

    g = R["run"]
    lab.row("Run it: Texas margin a tonne, 2013 / 2016 / latest", f"${g['texas'][2013]:,.0f} / ${g['texas'][2016]:,.0f} / "
            f"${g['texas'][g['years'][-1]]:,.0f}")
    lab.row("Run it: cash since 2013, Texas / Europe ($m); paid back by", f"{g['cum_texas'][-1]:,.0f} / {g['cum_europe'][-1]:,.0f}; "
            f"{g['payback']}")
    assert g["cum_texas"][-1] > g["capex"] > g["cum_europe"][-1]

    c = R["cracker"]
    for f in ("ethane", "naphtha"):
        b = c[f]
        lab.row(f"a tonne of ethylene from {f}, {c['year']}: feed / by-products / fuel / other = cost",
                f"${b['feed']:,.0f} / -${b['credits']:,.0f} / ${b['fuel']:,.0f} / ${b['other']:,.0f} = ${b['cost']:,.0f}")
    lab.row("ethylene yield: ethane / naphtha", f"{100 * c['yields']['ethane']['ethylene']:.0f}% / "
            f"{100 * c['yields']['naphtha']['ethylene']:.0f}%")

    f = R["feedstock"]
    lab.row("US ethane output, kb/d: first month / latest", f"{f['ethane_first']:,.0f} ({f['ethane_first_m']}) / "
            f"{f['ethane_last']:,.0f} ({f['ethane_last_m']})")
    lab.row("US ethane exports, kb/d: first month / latest", f"{f['exports_first']:,.0f} ({f['exports_first_m']}) / "
            f"{f['exports_last']:,.0f} ({f['exports_last_m']})")
    early = [y for y in f["gap"] if y <= 2005]
    late = [y for y in f["gap"] if y >= 2010]
    lab.row("Europe's naphtha cost less Texas's ethane cost, average ($ a tonne): to 2005 / from 2010",
            f"{np.mean([f['gap'][y] for y in early]):+,.0f} / {np.mean([f['gap'][y] for y in late]):+,.0f}")

    cy = R["cycle"]
    cu = cy["cap_util"]
    lab.row("US chemical capacity utilization: lowest year / 2021 / 2025", f"{min(cu, key=cu.get)} ({min(cu.values()):.0f}%) / "
            f"{cu[2021]:.0f}% / {cu[2025]:.0f}%")
    t21 = sum(cy["nets"][t][2021] for t in ("DOW", "LYB", "WLK", "OLN"))
    t25 = sum(cy["nets"][t][2025] for t in ("DOW", "LYB", "WLK", "OLN"))
    lab.row("Dow + LyondellBasell + Westlake + Olin net income, 2021 / 2025 ($bn)", f"{t21:.1f} / {t25:.1f}")

    fe = R["fertilizer"]
    lab.row("CF: MMBtu of gas per ton of ammonia", f"{fe['per_ton']:.1f}")
    lab.row("gas in a ton of ammonia, 2022: US / EU; Gulf price", f"${fe['cost']['US'][2022]:,.0f} / ${fe['cost']['EU'][2022]:,.0f}; "
            f"${fe['price'][2022]:,.0f}")
    lab.row("ammonia 2025, Mt N: China / India / Russia / US / world",
            " / ".join(f"{fe['producers'][k] / 1000:.0f}" for k in ("china", "india", "russia", "us")) + f" / {fe['world'] / 1000:.0f}")

    gs = R["gases"]
    p = gs["plant"]
    lab.row("gas plant's cash when the customer takes 100% / 50% / 0% ($m)", f"{p['cash_full']:.1f} / {p['cash_half']:.1f} / "
            f"{p['cash_zero']:.1f}")
    lab.row("five-year net margin: Linde / Air Products / Dow", f"{100 * gs['lin']['margin5']:.1f}% / {100 * gs['apd']['margin5']:.1f}% / "
            f"{100 * gs['dow']['margin5']:.1f}%")

    s = R["specialty"]
    lab.row("five-year net margin: Sherwin-Williams / Ecolab / PPG / IFF", " / ".join(f"{100 * s[k]['margin5']:.1f}%"
                                                                                     for k in ("shw", "ecl", "ppg", "iff")))

    e = R["europe"]
    lab.row(f"chemical output vs 2021, latest ({e['de_last_m']}): Germany / EU", f"-{100 * e['fall']:.0f}% / -{100 * e['eu_fall']:.0f}%")

    pl = R["plastics"]
    lab.row(f"plastics: {pl['p1950']:.0f} Mt (1950) to {pl['p_last']:.0f} Mt ({pl['p_year']}); recycled share of waste",
            f"{100 * pl['recycled_share']:.0f}% of {pl['total_waste']:.0f} Mt")

    cl = R["called"]
    lab.row("AEO2005 vs outcome: LNG 2025 (Tcf)", f"imports {cl['lng_proj']:.1f} projected; exports {cl['lng_exports_2025']:.1f} actual")
    lab.row("AEO2005 vs outcome: farm chemicals / ammonia growth", f"{cl['ag_proj']:.1f}% vs {cl['n_actual']:.1f}% a year")
    lab.row("AEO2005 vs outcome: bulk chemicals / basic chemicals", f"{cl['chem_proj']:.1f}% vs {cl['basic_actual']:.2f}% a year")
    lab.row("this series' call: Germany's 2027 chemical output below 79.8", f"{100 * cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    ys = sorted(f["cost"]["Texas, ethane"])
    ax1.plot(ys, [f["cost"]["Texas, ethane"][y] for y in ys], color=labs.GOLD, lw=1.8,
             label="Texas, ethane")
    ax1.plot(ys, [f["cost"]["Europe, naphtha"][y] for y in ys], color=labs.BLUE, lw=1.8, label="Europe, naphtha")
    ax1.set_ylabel("$ a tonne of ethylene")
    ax1.set_title("A cracker's cash cost by site (the Works)")
    ax1.legend(fontsize=7)
    ys2 = sorted(fe["cost"]["US"])
    ax2.plot(ys2, [fe["cost"]["US"][y] for y in ys2], color=labs.RED, lw=1.6, label="US gas")
    ax2.plot(ys2, [fe["cost"]["EU"][y] for y in ys2], color=labs.BLUE, lw=1.6, label="European gas")
    ax2.set_ylabel("$ a short ton of ammonia")
    ax2.set_title("The gas in a ton of ammonia")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("At the root of the tree the feedstock is most of the cost and the cheapest molecules win; commodity "
                "profits swing with the build cycle; contracts and brands steady the money further along; and the "
                "bill for harm comes decades after the profit.")
    return lab
