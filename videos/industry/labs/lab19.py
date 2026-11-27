"""Lab 19: Otis's two businesses, the Run it tender, what Caterpillar and Deere sell, the capital-goods cycle, the
installed base, dealers, lenders and rental, book-to-bill and Caterpillar's profit bridge, machinery output and jobs,
robots, China's excavators, the conglomerates' separations, the landscape, and the IFR's forecasts."""

import numpy as np

from explainer.industry.works import machine  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry19.compute import results

TITLE = "Machinery: the installed base, the tender and the capital-goods cycle"
GOAL = ("Measure Otis's factory against its service business; play the tender and find the attach rate at which makers "
        "fight for the sale; read Caterpillar's and Deere's segments; follow equipment investment and machinery orders "
        "through the cycle; see an installed base steady a model maker; read the dealers, lenders and rental fleets; read "
        "a backlog and a profit bridge; compare machinery output with jobs; count robots by country; follow China's "
        "excavator exports; and score the IFR's forecasts, with this series' call.")
TASKS = [
    "With machine.Tender(service=s), find the smallest value of servicing s at which cutting the price beats holding "
    "against a rival who holds (the attach rate at 1). How does machine.attach_threshold change as the cut bid falls?",
    "With machine.Maker(life=L), find how the service share of profit in the mature years changes as machines last 10, 15 "
    "and 25 years. What does a longer-lived machine do to the maker's steadiness?",
    "Using the chapter's IFR figures, find the growth rate the IFR's forecast of 806,000 installations in 2029 implies "
    "from 2025's 600,000, and compare it with China's growth from 2011 to 2025.",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("Otis 2025, $m: new equipment sales / profit; service sales / profit",
            f"{h['ne_sales']:,} / {h['ne_op']:,}; {h['sv_sales']:,} / {h['sv_op']:,}")
    lab.row("Caterpillar backlog, $bn: end 2024 / end 2025 / September 2026", " / ".join(f"{v:.1f}" for v in h["backlog"]))

    u = R["run"]
    t = u["table"]
    lab.row("the tender, $m (you, rival): hold/hold; cut/hold; cut/cut",
            f"{t['hold|hold'][0]:.0f}, {t['hold|hold'][1]:.0f}; {t['cut|hold'][0]:.0f}, {t['cut|hold'][1]:.0f}; "
            f"{t['cut|cut'][0]:.0f}, {t['cut|cut'][1]:.0f}")
    lab.row("equilibrium; at a 30% attach rate; attach threshold", f"{u['eq']}; {u['low_eq']}; {100 * u['threshold']:.0f}%")
    assert u["eq"] == [("cut", "cut")]

    m = R["making"]
    lab.row("Caterpillar segments, $bn: " + " / ".join(m["cat"]), " / ".join(f"{v[0]:.1f}" for v in m["cat"].values()))
    lab.row("Deere: revenue / financial products, $bn", f"{m['de_rev']:.1f} / {m['de_fin']:.1f}")

    c = R["cycle"]
    lab.row("equipment investment, % of GDP: 1979 / 2009 / 2025",
            " / ".join(f"{100 * c['eq_share'][y]:.1f}" for y in (1979, 2009, 2025)))
    lab.row("2009: machinery orders / shipments; Caterpillar 2012-16 / 2019-20",
            f"{100 * c['orders_fall']:.0f}% / {100 * c['ships_fall']:.0f}%; {100 * c['cat_fall']:.0f}% / {100 * c['cat_fall20']:.0f}%")

    b = R["base"]
    lab.row("the Works' maker: service share of revenue / profit; worst year new / service",
            f"{100 * b['svc_rev_share']:.0f}% / {100 * b['svc_profit_share']:.0f}%; {100 * b['new_sw']['worst_fall']:.0f}% / "
            f"{100 * b['svc_sw']['worst_fall']:.0f}%")

    d = R["dealers"]
    lab.row("dealers: Caterpillar / Deere locations; United Rentals units / OEC $bn / locations",
            f"{d['cat']} / {d['de']:,}; {d['uri']['units']:,} / {d['uri']['oec']:.1f} / {d['uri']['loc']:,}")
    bk = R["backlog"]
    lab.row("Caterpillar operating profit bridge, $bn: 2024 / volume / price / costs / 2025",
            f"{bk['op24']:.2f} / {bk['volume']:+.2f} / {bk['price'] / 1e3:+.2f} / {bk['mfg']:+.2f} / {bk['op25']:.2f}")
    lab.row("machinery book-to-bill, 2009 / 2025", f"{bk['btb'][2009]:.2f} / {bk['btb'][2025]:.2f}")

    hi = R["history"]
    lab.row("1990 -> 2025: machinery output / jobs; farm machinery prices / CPI since 1947",
            f"x{hi['ip'][2025]:.2f} / x{hi['jobs'][2025]:.2f}; x{hi['farm_x']:.1f} / x{hi['cpi_x']:.1f}")

    rb = R["robots"]
    lab.row("robots installed in 2025, thousands: world / China / US / Japan",
            " / ".join(f"{rb['inst'][k][2025] / 1e3:.0f}" for k in ("World", "China", "United States", "Japan")))
    lab.row("robot density per 10,000: " + " / ".join(rb["density"]), " / ".join(f"{v:,}" for v in rb["density"].values()))

    ch = R["china"]["excavators"]
    lab.row("excavator exports, $bn: China 2015 / 2025; Japan 2025", f"{ch['China'][2015]:.1f} / {ch['China'][2025]:.1f}; "
            f"{ch['Japan'][2025]:.1f}")

    cl = R["called"]
    lab.row("IFR forecasts: 2022 / actual; 2024 / actual; 2026 forecast",
            f"{cl['fc2022']:,} / {cl['act2022']:,}; {cl['fc2024']:,} / {cl['act2024']:,.0f}; {cl['fc2026']:,}")
    lab.row("this series' call: 2026 installations below the IFR's forecast", f"probability {100 * cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    rows = b["rows"]
    ys = [r["year"] for r in rows]
    ax1.plot(ys, [r["new_rev"] for r in rows], color=labs.GOLD, lw=1.8, label="new machines")
    ax1.plot(ys, [r["svc_rev"] for r in rows], color=labs.GREEN, lw=1.8, label="parts and service")
    ax1.set_xlabel("year")
    ax1.set_ylabel("revenue, $m")
    ax1.set_title("The installed base (the Works)")
    ax1.legend(fontsize=7)
    for k, col in (("China", labs.RED), ("Japan", labs.BLUE), ("South Korea", labs.PURPLE), ("Germany", labs.TEAL)):
        e = ch[k]
        yy = sorted(e)
        ax2.plot(yy, [e[y] for y in yy], color=col, lw=1.6, label=k)
    ax2.set_ylabel("excavator exports, $bn")
    ax2.set_title("China's excavators (UN Comtrade)")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("Every machine sold joins an installed base that needs parts and service for years, at margins the factory "
                "never sees, and steadier than new sales; when the servicing is worth enough, makers fight at the sale and "
                "machines go cheap.")
    _ = np  # the tasks use numpy for their searches
    return lab
