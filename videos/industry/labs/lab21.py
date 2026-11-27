"""Lab 21: Intuitive's robots and instruments, the Run it market (sell the robot or place it), the four businesses, the
FDA's roads and recalls, who pays a laboratory, the installed base and a hospital's five years, Abbott's tests, prices and
output, pulsed field ablation, the tools companies, the landscape and the device dollar, and Intuitive's forecasts."""

import numpy as np

from explainer.industry.works import medtech  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry21.compute import results

TITLE = "Medical technology: the surgeon, the hospital, the payer and the installed base"
GOAL = ("Count Intuitive's robots, operations and instruments; sell a robot or place it and find the fee that pays as well; "
        "read the four businesses in Medtronic's, GE HealthCare's, Dexcom's and Quest's accounts; count the FDA's two roads "
        "and its recalls; see who pays a laboratory, and price against volume; cost a hospital's five years with one robot; "
        "follow Abbott's tests and pulsed field ablation; compare device prices with all prices; place the tools companies; "
        "split a device dollar beside a drug dollar; and score Intuitive's forecasts, with this series' call.")
TASKS = [
    "With medtech.Market().sell(price=P) and .place(fee=f), find the robot price that maximizes the maker's value from "
    "selling and the fee that maximizes it from placing. Which earns more at its best, and how many operations does each "
    "bring?",
    "Raise the hospital's gain per operation (Market(value=V)) from $3,000 to $5,000. How do the buying threshold, the "
    "number of buyers and the fee that pays as well as selling change?",
    "With medtech.hospital_spend(ops=n), find how the cost per operation of one robot falls as a hospital does 150, 300 and "
    "500 operations a year. At what volume do instruments pass 60% of the hospital's spend?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("Intuitive 2025: operations / robots / operations a robot a year",
            f"{h['procs']:,} / {h['base']:,} / {h['per_system']:.0f}")
    lab.row("robot price, $m; instruments a procedure, $; average instruments revenue an operation",
            f"{h['price'][0]}-{h['price'][1]}; {h['ia'][0]:,}-{h['ia'][1]:,}; {h['per_op']:,.0f}")

    u = R["run"]
    s, p = u["sell"], u["place"]
    lab.row("sell at $2m: buyers / value $m / operations; threshold",
            f"{s['buyers']} / {s['value'] / 1e6:.0f} / {s['ops']:,.0f}; {s['threshold']:.0f} a year")
    lab.row("place at $1,000 an operation: takers / value $m / operations; break-even; losers",
            f"{p['takers']} / {p['value'] / 1e6:.0f} / {p['ops']:,.0f}; {p['breakeven']:.0f}; {p['losers']}")
    lab.row("the fee that pays as well as selling", f"${u['match']:,.0f}")
    lab.row("Intuitive: leased robots / paid by use (2023) / lease revenue 2023-2025, $m",
            f"{u['leased']:,} / {u['usage']:,} ({u['usage23']:,}) / " + " / ".join(f"{v:,.0f}" for v in u["lease_rev"].values()))
    assert s["threshold"] > p["breakeven"]

    k = R["kinds"]
    lab.row("Medtronic fiscal 2026, $bn: " + " / ".join(k["mdt"]), " / ".join(f"{v / 1e3:.1f}" for v in k["mdt"].values()))
    lab.row("GE HealthCare 2025, $bn: products / services", f"{k['gehc']['products'] / 1e3:.1f} / {k['gehc']['services'] / 1e3:.1f}")
    lab.row("Dexcom revenue, $bn: 2012 / 2025", f"{k['dexcom'][2012]:.2f} / {k['dexcom'][2025]:.2f}")

    f = R["fda"]
    lab.row("a year, 2021-2025: 510(k) clearances / De Novo / original PMAs", f"{f['k510_5']:,.0f} / {f['denovo_5']:.0f} / {f['pma_5']:.0f}")
    lab.row("Class I recall products: 2014 / 2017 / 2023 (events, largest)",
            f"{f['recall_c1'][2014]} / {f['recall_c1'][2017]} / {f['recall_c1'][2023]} ({f['c1_events']}, {f['c1_max']})")

    c = R["customers"]["mix"]
    lab.row("Quest payers, % of tests / % of revenue: insurers, government, clients, patients",
            "; ".join(f"{v[0]}/{v[1]}" for v in c.values()))
    pv = R["pricevol"]
    lab.row("Quest revenue per requisition / volume / organic, 2025", f"{pv[2025]['rpr']:+.1f}% / {pv[2025]['vol']:+.1f}% / "
            f"{pv[2025]['org']:+.1f}%")

    b = R["base"]
    lab.row("recurring share; GE HealthCare gross margin products / services",
            f"{b['recurring']}%; {100 * b['gehc_gm_products']:.0f}% / {100 * b['gehc_gm_services']:.0f}%")
    sp = b["spend"]
    lab.row("a hospital's five years with one robot, $m: robot / service / instruments; an operation",
            " / ".join(f"{v / 1e6:.2f}" for v in sp["parts"].values()) + f"; ${sp['per_op']:,.0f}")

    d = R["diag"]
    lab.row("Abbott COVID-19 tests, $bn: 2020 / 2022 / 2025", f"{d['covid'][2020]} / {d['covid'][2022]} / {d['covid'][2025]}")
    hs = R["history"]
    lab.row("since 1986: instrument prices / CPI / relative; output since 1972",
            f"x{hs['ppi_x']:.2f} / x{hs['cpi_x']:.2f} / x{hs['rel'][2025]:.2f}; x{hs['ip_x']:.1f}")

    bm = R["boom"]
    lab.row("Boston Scientific electrophysiology, $bn: 2023 / 2024 / 2025", " / ".join(f"{v / 1e3:.2f}" for v in bm["ep"].values()))
    lab.row("tools revenue, $bn: " + " / ".join(R["tools"]["rev"]), " / ".join(f"{v:.1f}" for v in R["tools"]["rev"].values()))

    dl = R["dollar"]
    lab.row(f"a dollar of {dl['n']} device makers' revenue, cents: making / research / everything else / profit",
            " / ".join(f"{100 * dl[k_]:.0f}" for k_ in ("make", "research", "rest", "profit")))

    cd = R["called"]
    lab.row("Intuitive's guidance: 2025 range / actual; 2026 range, narrowed",
            f"{cd['g2025'][0]}-{cd['g2025'][1]}% / {cd['a2025']}%; {cd['g2026'][0]}-{cd['g2026'][1]}%, "
            f"{cd['g2026_oct'][0]}-{cd['g2026_oct'][1]}%")
    lab.row("this series' call: 2026 da Vinci operations up 15% or more", f"probability {100 * cd['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    vols = np.array(u["volumes"])
    ax1.plot(vols, np.array(u["sell_per"]) / 1e6, color=labs.BLUE, lw=1.8, label="sell at $2m")
    ax1.plot(vols, np.array(u["place_per"]) / 1e6, color=labs.GOLD, lw=1.8, label="place, $1,000 an operation")
    ax1.axhline(0, color=labs.GREY, lw=1)
    ax1.set_xlabel("operations a year at the hospital")
    ax1.set_ylabel("maker's value per hospital, $m")
    ax1.set_title("Sell or place (the Works)")
    ax1.legend(fontsize=7)
    k510 = hs["k510"]
    yy = sorted(y for y in k510 if 1977 <= y <= 2025)
    ax2.plot(yy, [k510[y] for y in yy], color=labs.BLUE, lw=1.6)
    ax2.set_ylabel("510(k) clearances a year")
    ax2.set_title("The comparison road (openFDA)")
    lab.fig = fig
    lab.note = ("The surgeon chooses, the hospital buys, the payer sets the price; the maker earns most after the sale, from "
                "the instruments, service and tests its installed base buys again and again.")
    return lab
