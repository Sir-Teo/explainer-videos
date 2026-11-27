"""Lab 14: the Great Stink, bills that never fall, the last landfill in the valley, America's water needs, the regulated
water company and gearing, England's price review, a Kentucky rate case and Sabesp, the collection route, landfills and
airspace, recycling and China's ban, hazardous waste, margins, safe water around the world, and the EPA's 1989
forecast."""

import numpy as np

from explainer.industry.works import route, utility  # noqa: F401  (the tasks use them)
from videos.coursekit import labs
from videos.industry.industry14.compute import results

TITLE = "Water and waste: the route, the hole, the asset base and the bill"
GOAL = ("Count the years America's utility prices fell; price the last landfill in a valley as a rival waits for a "
        "permit; size America's water needs; build a regulated water company's bill from its asset base and see what "
        "gearing does to its owners; read England's price review; split a street between haulers; follow a landfill's "
        "airspace; watch recyclable paper fall after China's ban; compare margins; and score the EPA's 1989 forecast.")
TASKS = [
    "With route.ValleyLandfill and its play(plan, rival_year) method, find the valley's ceiling "
    "(ValleyLandfill(ceiling=...)) below which charging it, with the rival fifteen years away, is worth no more than "
    "filling fast. Then set the ceiling to $75 and find what ten years of the rival's permitting are now worth.",
    "With utility.WaterCo, find the capital spending a year that keeps the bill flat in real terms over twenty-five years. "
    "Then, with utility.equity_return, find the cost of debt at which shareholders at 70% gearing earn nothing on an asset "
    "base earning 4%.",
    "With route.Route and route.split_street, find the share of a street a hauler must serve to break even at $1.25 a "
    "stop. How does the answer change if the truck costs $1,400 a day (Route(truck_day=1400.0))? What does this say about "
    "why towns grant one hauler a whole district?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("the Great Stink: days from leave to royal assent; cost; rate", f"{h['days']:.0f}; £{h['cost']:.0f}m; {h['rate']:.0f}d for {h['years']:.0f} years")
    lab.row("years each US price index fell, 1953-2025",
            " / ".join(f"{v['name']} {v['n']}" for v in h["falls"].values()))
    assert h["falls"]["SEHG01"]["n"] == 0

    g = R["run"]["games"]
    lab.row("Run it, $m today: fill / ceiling / expand, rival in 15 years",
            " / ".join(f"{g[p + '|15']['pv']:,.0f}" for p in ("fill", "ceiling", "expand")))
    lab.row("Run it, $m today: fill / ceiling / expand, rival in 5 years",
            " / ".join(f"{g[p + '|5']['pv']:,.0f}" for p in ("fill", "ceiling", "expand")))
    lab.row("ten years of the rival's permitting; a ton of airspace (ceiling, 15 years)",
            f"${R['run']['permit_worth']:,.0f}m; ${g['ceiling|15']['per_ton']:.2f} (book: ${R['run']['depletion']:.2f})")
    assert g["ceiling|15"]["pv"] > g["fill|15"]["pv"]

    s = R["system"]
    lab.row("America's water needs over 20 years: drinking (of which pipes) / clean water",
            f"${s['dw_total']:.0f}bn (${s['dw']['dist']:.0f}bn) / ${s['cw']:.0f}bn")
    lab.row("American Water 2025: capital spending per dollar of depreciation", f"{s['awk_ratio']:.1f}")

    rg = R["regulated"]
    f0, f25 = rg["path"][0], rg["path"][-1]
    lab.row("the Works' water company: asset base and bill, year 0 and year 25 (real)",
            f"£{f0['rcv'] / 1000:.0f}bn, £{f0['bill']:.0f} -> £{f25['rcv'] / 1000:.1f}bn, £{f25['bill']:.0f}")
    lab.row("shareholders' return at 55% / 80% gearing, debt at 2% and at 5%",
            f"{100 * rg['lev_cheap'][0.55]:.1f}% / {100 * rg['lev_cheap'][0.8]:.1f}%; {100 * rg['lev_dear'][0.55]:.1f}% / {100 * rg['lev_dear'][0.8]:.1f}%")
    lab.row("England: gearing 1991 / 2009; allowances PR19 / PR24; allowed return PR19 / PR24 / CMA",
            f"{rg['gear91']:.0f}% / {rg['gear09']:.0f}%; £{rg['allow19']:.0f}bn / £{rg['allow24']:.0f}bn; "
            f"{rg['wacc19']:.2f}% / {rg['wacc24']:.2f}% / {rg['cma_wacc']:.2f}%")
    lab.row("England: average bill 2025/26; Thames Water's debt", f"£{rg['bill']:.0f}; £{rg['thames_debt']:.1f}bn")

    e = R["elsewhere"]
    lab.row("Kentucky American Water: rate base, equity share, allowed ROE", f"${e['awk']['rb']:.0f}m, {e['awk']['eq']:.2f}%, {e['awk']['roe']:.2f}%")
    lab.row("Sabesp: state's stake before / after; investment 2023 / 2024 / 2025 (R$bn)",
            f"{e['sbs']['before']:.2f}% / {e['sbs']['after']:.2f}%; " + " / ".join(f"{e['sbs']['capex'][y]:.1f}" for y in (2023, 2024, 2025)))

    c = R["collection"]
    lab.row("the Works' route: cost per stop, whole street / half / third",
            " / ".join(f"${v['cost']:.2f}" for v in c["split"].values()))
    lab.row("profit a day at the price, one / two / three haulers", " / ".join(f"${v['profit']:,.0f}" for v in c["split"].values()))
    lab.row("rubbish collection's CPI after inflation, 2025 (1984 = 1)", f"x{c['garbage_real'][2025]:.2f}")

    lf = R["landfill"]
    lab.row("US landfills 1988 / 2009; tons landfilled 1990 / 2018 (m)",
            f"{lf['count'][0]:,.0f} / {lf['count'][1]:,.0f}; {lf['tons'][1990]:.0f} / {lf['tons'][2018]:.0f}")
    lab.row("Republic's permitted airspace, 2024 -> 2025 (m cubic yards); years at 2025's pace",
            f"{lf['rsg']['start']:,.0f} -> {lf['rsg']['end']:,.0f}; {lf['rsg']['years_left']:.0f}")

    rc = R["recycling"]
    m18 = rc["msw"][2018]
    lab.row("2018: landfilled / recycled / composted / burned (% of generation)",
            " / ".join(f"{100 * m18[k] / m18['generation']:.0f}%" for k in ("landfill", "recycling", "composting", "combustion")))
    lab.row("recyclable paper index: peak (2016-18) and low (2018-20)", f"{rc['paper_peak'][0]:.0f} ({rc['paper_peak'][1]}) -> {rc['paper_low'][0]:.0f} ({rc['paper_low'][1]})")

    sp = R["returns"]["spread"]
    lab.row("net margin range 2010-2025: American States / Republic / Freeport / Delta",
            " / ".join(f"{100 * sp[t][0]:.0f}% to {100 * sp[t][1]:.0f}%" for t in ("AWR", "RSG", "FCX", "DAL")))

    w = R["world"]
    lab.row("safely managed water / sanitation, world, 2000 -> 2024",
            f"{w['SH.H2O.SMDW.ZS']['World'][0]:.0f}% -> {w['SH.H2O.SMDW.ZS']['World'][1]:.0f}%; "
            f"{w['SH.STA.SMSS.ZS']['World'][0]:.0f}% -> {w['SH.STA.SMSS.ZS']['World'][1]:.0f}%")

    cl = R["called"]
    lab.row("this series' call: water and sewerage CPI up more than 4% in 2027", f"{100 * cl['prob']:.0f}% (2026 to September: +{cl['ytd']:.1f}%)")

    fig, (ax1, ax2) = labs.figure(2)
    C = R["run"]["curve"]
    Ts = sorted(C)
    for p, col in (("fill", labs.BLUE), ("ceiling", labs.GOLD), ("expand", labs.PURPLE)):
        ax1.plot(Ts, [C[T][p] for T in Ts], color=col, lw=1.8, label=p)
    ax1.set_xlabel("years until the rival's permit")
    ax1.set_ylabel("$m today")
    ax1.set_title("The last landfill in the valley (the Works)")
    ax1.legend(fontsize=7)
    real = R["history"]["real"]
    for k, col in (("SEHG01", labs.BLUE), ("SEHG02", labs.GREEN), ("SEHF01", labs.GOLD), ("SEHA", labs.PURPLE)):
        ys = sorted(real[k])
        ax2.plot(ys, [real[k][y] for y in ys], color=col, lw=1.6, label=R["history"]["names"][k])
    ax2.set_ylabel("price after inflation (first year = 1)")
    ax2.set_title("American bills since 1953 (BLS)")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("Water and waste are networks nobody can duplicate, paid for over decades; a regulator or a scarce permit "
                "sets the return, prices follow costs up, and the steadiness belongs to whoever has not borrowed too "
                "much against it.")
    return lab
