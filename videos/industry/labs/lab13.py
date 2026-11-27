"""Lab 13: Insull's load factor, a gas plant in a cold snap, the load duration curve, the screening curve, the merit
order and gas, a utility's revenue requirement, February 2021, solar's falling price and the battery that needs bad
evenings, Britain's suppliers, the world's electricity, the new load, and the government's 2005 outlook."""

import numpy as np

from explainer.industry.works import power  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry13.compute import results

TITLE = "Electricity: load, the merit order, the rate base and the storm"
GOAL = ("Compute Insull's load factors; play a gas plant through a cold snap, hedged and not; read Texas's load duration "
        "curve; draw the screening curve from EIA's costs; watch the merit order set the price; build a utility's "
        "revenue requirement; follow February 2021 hour by hour; see why more solar earns less and what a battery needs; "
        "squeeze a supplier; compare the world; and score the government's 2005 outlook.")
TASKS = [
    "With power.run_it(power.week_prices(cap=5000.0)), replay chapter 1 with a lower cap of $5,000. Which strategy now loses "
    "most, and by how much? At what share of output sold forward (power.GasPlantWeek(hedge=...)) does a plant that "
    "freezes lose nothing over the week?",
    "Using R['plants'] and power.Tech, find the cost of capital at which a new nuclear plant matches a new combined-cycle "
    "plant at a 90% capacity factor with gas at $3.85 per million Btu. Then find the gas price at which they match if "
    "capital costs 4%.",
    "With power.Utility, raise the rate base from $30bn to $40bn with sales unchanged. How much does the price of a kWh "
    "rise? How much more do shareholders earn a year? Explain, with these numbers, the Averch-Johnson incentive.",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("Insull's block (1910): load factor on customers' peaks / on the block's peak",
            f"{100 * h['lf_alone']:.1f}% / {100 * h['lf_together']:.1f}%; diversity factor {h['diversity']:.2f}")

    g = R["run"]["games"]
    lab.row("Run it, $m for the week: spot & runs / hedged & runs / spot & freezes / hedged & freezes",
            " / ".join(f"{g[k]['total']:+,.0f}" for k in ("spot, runs", "hedged, runs", "spot, freezes", "hedged, freezes")))
    assert g["hedged, freezes"]["total"] < g["spot, freezes"]["total"] < g["spot, runs"]["total"]
    lab.row("Vistra's Winter Storm Uri, pre-tax ($bn)", f"{R['run']['vst']:.1f}")

    p = R["physics"]
    lab.row("ERCOT 2025: peak / average / load factor", f"{p['peak'] / 1000:.1f} GW / {p['mean'] / 1000:.1f} GW / {100 * p['load_factor']:.0f}%")
    lab.row("ERCOT 2025: hours above 90% and 95% of the peak", f"{p['top'][0.1]:,} / {p['top'][0.05]:,}")

    pl = R["plants"]
    for k in ("ct_frame", "cc2", "nuclear", "wind", "solar"):
        t = pl["techs"][k]
        lab.row(f"{t['name']}: fixed $ a kW-year / running $ a MWh", f"{t['fixed']:,.0f} / {t['running']:.1f}")
    lab.row("a new plant at 90%: combined cycle / nuclear ($ a MWh); gas for nuclear to break even",
            f"{pl['cc_mwh_90']:.0f} / {pl['nuke_mwh_90']:.0f}; ${pl['gas_even']:.1f}")
    lab.row("capacity factors 2025: nuclear / combined cycle / coal / wind / solar / peakers",
            " / ".join(f"{100 * pl['cf'][k]['cf']:.0f}%" for k in ("nuclear", "gas_cc", "coal", "wind", "solar", "gas_ct")))

    d = R["dispatch"]
    lab.row("ERCOT price on gas, 2014-2021 (ex-Uri): $ a MWh per $ a MMBtu", f"{d['slope']:.2f} (intercept {d['icpt']:.1f})")
    lab.row("the Works' merit order: price at 35, 60, 80, 100, 106 GW", " / ".join(f"${v:,.0f}" for v in d["clears"].values()))

    u = R["utility"]
    q = u["req"]
    lab.row("the Works' utility: O&M / depreciation / tax / return = requirement ($m)",
            f"{q['om']:,.0f} / {q['depreciation']:,.0f} / {q['tax']:,.0f} / {q['return']:,.0f} = {q['total']:,.0f}; {q['cents']:.1f}c a kWh")
    lab.row("a US kWh, 2020: generation / transmission / distribution (cents)", " / ".join(f"{v:.2f}" for v in u["split"].values()))
    lab.row("Duke: approved ROEs (range); requested in N.C. 2025",
            f"{min(c[2] for c in u['cases']):.2f}%-{max(c[2] for c in u['cases']):.2f}%; {u['pending'][0][2]:.2f}%")

    t = R["texas"]
    lab.row("February 2021: largest gap, forecast less served (MW, when)", f"{t['gap_max']:,.0f} ({t['gap_when'][0]} hour {t['gap_when'][1]})")
    lab.row("February 2021: people without power; deaths; firm load shed", f"{t['people']:.1f}m; {t['deaths']:.0f}; {t['shed']:,.0f} MW")

    hi = R["history"]
    lab.row("US sales growth by decade (% a year)", " / ".join(f"{k}s {v:+.1f}" for k, v in hi["decades"].items()))

    s = R["sun"]["works"]
    st = R["storage"]["works"]
    lab.row("the Works' solar day: what a MWh of solar earns, little / much solar", f"${s['cap_lo']:.0f} / ${s['cap_hi']:.0f}")
    lab.row("a 100 MW four-hour battery: trading a year / fixed cost a year ($m); bad evenings to break even",
            f"{st['year']:.1f} / {st['fixed']:.1f}; {st['days_even']:.0f}")

    r = R["retail"]
    lab.row("Britain: suppliers 2010 / mid-2018 / 2022; failed; cost per customer",
            f"{r['s2010']:.0f} / {r['speak']:.0f} / {r['s2022']:.0f}; {r['failed']:.0f}; £{r['per']:.0f}")

    w = R["world"]
    lab.row("generation 2025 (TWh): China / US / EU / India", " / ".join(f"{w['gen'][k][2025]:,.0f}" for k in
                                                                          ("China", "United States", "European Union (27)", "India")))

    dm = R["demand"]
    lab.row("US sales growth 2024 / 2025 / 2026 to date", f"{dm['growth'][2024]:+.1f}% / {dm['growth'][2025]:+.1f}% / {dm['ytd']:+.1f}%")
    lab.row("data centres: 2014 / 2023 / 2028 projection (TWh)", f"{dm['dc14']:.0f} / {dm['dc23']:.0f} / {dm['dc28_lo']:.0f}-{dm['dc28_hi']:.0f}")

    c = R["called"]
    lab.row("AEO2005: 2025 projected / actual (billion kWh)", f"{c['proj']:,.0f} / {c['actual']:,.0f} ({c['growth_proj']:.1f}% vs {c['growth_actual']:.1f}% a year)")
    lab.row("this series' call: 2027 sales more than 1.5% above 2026", f"{100 * c['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    dur = np.array(p["duration"])
    ax1.plot(np.arange(len(dur)) * 8, dur / 1000, color=labs.BLUE, lw=1.8)
    ax1.axhline(p["peak"] / 1000, color=labs.RED, lw=1.0, ls="--")
    ax1.set_xlabel("hours of 2025, busiest first")
    ax1.set_ylabel("GW")
    ax1.set_title("ERCOT's load duration curve (EIA-930)")
    xs = np.arange(0, 101, 5)
    for k, col in (("ct_frame", labs.RED), ("cc2", labs.GOLD), ("nuclear", labs.PURPLE)):
        ax2.plot(xs, pl["techs"][k]["curve"], color=col, lw=1.8, label=pl["techs"][k]["name"])
    ax2.set_xlabel("capacity factor, %")
    ax2.set_ylabel("$ a kW a year")
    ax2.set_title("The screening curve (the Works, EIA costs)")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("Electricity is made the instant it is used, so the system is built for its peak and paid for by its "
                "average; the merit order sets the price, the rate base sets the wires' return, and scarcity pays the "
                "plants that stand ready, if they are ready.")
    return lab
