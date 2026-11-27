"""Lab 22: P&G's double and its dollar, the Run it brand against a store label, gross margins and advertising across the
makers, Walmart's shares, Coca-Cola's concentrate and bottlers, P&G's volume and price, consumer prices, Hershey, Altria's
volume and price and PMI's smoke-free products, the landscape, and P&G's forecasts."""

import numpy as np

from explainer.industry.works import brand  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry22.compute import results

TITLE = "Consumer goods: the brand, the shelf and the price"
GOAL = ("Measure how far P&G's prices sit above its costs and where the gap goes; run a brand against a store label and "
        "see what cutting the advertising or the price does over eight years; compare gross margins and advertising across "
        "the makers; read the retailer's share of each maker's sales; split Coca-Cola's concentrate from its bottlers; test "
        "pricing power in P&G's volume and price and in consumer prices; follow Hershey, Altria and PMI; place the companies; "
        "and score P&G's forecasts, with this series' call.")
TASKS = [
    "With brand.Brand().run([A] * 8), try steady budgets A from $0m to $300m a year. Which maximizes eight-year value, and "
    "what share does it reach by year eight? Is the Works' brand advertising too little?",
    "With brand.Brand(decay=d), make advertising wear off faster (d = 0.4) or slower (d = 0.1). How does the gap between "
    "holding and cutting the advertising change, and why?",
    "With brand.Brand().run([100] * 8, store_price=s), lower the store label's price to $4 and raise it to $6. How do the "
    "brand's share and profit change, and what does that say about the retailer's power over the brand?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("P&G fiscal 2026: sales / cost of products, $bn; ratio", f"{h['sales']:.1f} / {h['cost']:.1f}; {h['ratio']:.2f}")
    lab.row("advertising $bn; Walmart share; top ten customers", f"{h['ads']}; {h['walmart']}%; {h['top10']}%")
    d = R["dollar"]
    lab.row("a dollar of P&G's sales, cents: making / advertising / other / operating profit / net",
            " / ".join(f"{100 * d[k]:.0f}" for k in ("make", "ads", "other", "op", "net")))

    ch = R["run"]["choices"]
    for k in ("hold", "cut", "promote"):
        rows = ch[k]["rows"]
        lab.row(f"the Works' brand, {k}: year 1 / year 8 profit $m; year 8 share; 8-year value $bn",
                f"{rows[0]['profit']:,.0f} / {rows[-1]['profit']:,.0f}; {100 * rows[-1]['share']:.0f}%; {ch[k]['npv'] / 1e3:.2f}")
    assert ch["hold"]["npv"] > ch["cut"]["npv"] and ch["cut"]["rows"][0]["profit"] > ch["hold"]["rows"][0]["profit"]

    g = R["margins"]["gm"]
    lab.row("gross margins: PMI / Coca-Cola / P&G / bottler / Mondelez",
            " / ".join(f"{100 * g[k]:.0f}%" for k in ("Philip Morris International", "Coca-Cola", "Procter & Gamble",
                                                      "Coca-Cola Consolidated", "Mondelez")))
    a = R["ads"]["share"]
    lab.row("advertising share of sales: Colgate / P&G / Coca-Cola / PepsiCo / PMI",
            " / ".join(f"{100 * a[k]:.1f}%" for k in ("Colgate-Palmolive", "Procter & Gamble", "Coca-Cola", "PepsiCo",
                                                       "Philip Morris International")))
    w = R["retailer"]["walmart"]
    lab.row("Walmart's share of sales: " + " / ".join(w), " / ".join(f"{v}%" for v in w.values()))

    b = R["bottler"]
    lab.row("Coca-Cola: concentrate share of cases / revenue; gross margin vs bottler",
            f"{b['conc_vol']}% / {b['conc_rev']}%; {100 * b['ko_gm']:.0f}% vs {100 * b['coke_gm']:.0f}%")

    p = R["pricing"]
    lab.row("P&G volume / price, FY2020-26", "; ".join(f"{y}: {v['vol']:+d}/{v['price']:+d}" for y, v in p.items()))
    hs = R["history"]["infl"]
    lab.row("consumer prices 2020-23: food at home / all / personal care",
            " / ".join(f"+{100 * hs[k]:.1f}%" for k in ("food at home", "all", "personal care")))

    e = R["extra"]
    lab.row("Hershey gross margin 2024 / 2025; price", f"{e['hsy_gm'][0]}% / {e['hsy_gm'][1]}%; +{e['hsy_price']}%")
    t = R["tobacco"]
    lab.row("Altria 2025: volume / price effects $m; margin; Marlboro share", f"{t['volfx']:,} / +{t['price']:,}; {t['margin']}%; {t['share']}%")
    lab.row("PMI smoke-free revenue, $bn: 2023 / 2025", f"{e['pm_sf'][2023] / 1e3:.1f} / {e['pm_sf'][2025] / 1e3:.1f}")

    c = R["called"]
    lab.row("P&G organic guidance: FY25 / actual; FY26 / actual; FY27; Q1",
            f"{c['g25'][0]}-{c['g25'][1]}% / {c['a25']}%; {c['g26'][0]}-{c['g26'][1]}% / {c['a26']}%; "
            f"{c['g27'][0]}-{c['g27'][1]}%; {c['q1']}%")
    lab.row("this series' call: P&G fiscal 2027 organic growth 3% or more", f"probability {100 * c['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    for k, col in (("hold", labs.GOLD), ("cut", labs.RED), ("promote", labs.BLUE)):
        rows = ch[k]["rows"]
        ax1.plot([r["year"] for r in rows], [r["profit"] for r in rows], color=col, lw=1.8, label=k)
    ax1.set_xlabel("year")
    ax1.set_ylabel("profit after advertising, $m")
    ax1.set_title("Run it (the Works)")
    ax1.legend(fontsize=7)
    names = [n for n in a if n in g]
    ax2.scatter([100 * a[n] for n in names], [100 * g[n] for n in names], color=labs.PURPLE)
    for n in names:
        ax2.annotate(n.split()[0], (100 * a[n], 100 * g[n]), fontsize=6, color=labs.MUTED)
    ax2.set_xlabel("advertising, % of sales")
    ax2.set_ylabel("gross margin, %")
    ax2.set_title("Advertising against gross margin")
    lab.fig = fig
    lab.note = ("Half the price is the brand, kept alive by advertising every year; the biggest spenders pay least per unit "
                "for it, the retailers push back, and when prices rose the brands raised theirs and most shoppers stayed.")
    _ = np
    return lab
