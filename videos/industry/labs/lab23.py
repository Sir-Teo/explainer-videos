"""Lab 23: the Works' season bought early, late or as a base and a chase; NIKE's factories and dollar; clothing exports by
country; days of stock; Inditex's working capital and quarters; off-price against department stores; Hermès, LVMH and
Gucci; the landscape; and Inditex's margin guidance, with this series' call."""

import numpy as np

from explainer.industry.works import fashion  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry23.compute import results

TITLE = "Fashion and luxury: the guess, speed and the wait"
GOAL = ("Buy a season of a new style early, late, or as a base and a chase, and see where the profit and the markdowns go; "
        "measure the forecast's worth; read where NIKE's goods are made and where its dollar goes; compare days of stock, "
        "Inditex's working capital and quarterly margins, off-price against department stores, and luxury's margins; follow "
        "Gucci against Hermès; place the companies; and score Inditex's margin guidance, with this series' call.")
TASKS = [
    "With fashion.Season(cost_near=c).choices(), raise the cost of ordering late from $16 to $20 and $24. How much of the "
    "chase's advantage over the early order is left, and how does the best early base change? Why can the chase never do "
    "worse than ordering everything early?",
    "With fashion.Season(clearance=s), set the clearance price to $0 (the leftovers are destroyed) and to $11. How do the "
    "best early order, the shirts left for the sale and the profit change, and why?",
    "With fashion.Season(cv_far=e, cv_near=0.2), find the forecast error months ahead below which the chase earns less "
    "than 1% more than ordering everything early. What kind of clothes have forecasts that good?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("Inditex FY2025: sales EUR bn; stores; gross margin by quarter",
            f"{h['sales']:.1f}; {h['stores']:,}; " + " / ".join(f"{h['q'][q][1]}%" for q in (1, 2, 3, 4)))
    lab.row("Hermès 2025: revenue EUR bn; recurring operating margin", f"{h['rms_rev'] / 1e3:.1f}; {h['rms_margin']}%")

    u = R["run"]
    for k in ("far", "near", "chase"):
        c = u["choices"][k]
        lab.row(f"the Works' season, {k}: ordered / cleared / lost (thousand); profit $m; gross margin",
                f"{c['ordered'] / 1e3:.0f} / {c['cleared'] / 1e3:.0f} / {c['lost'] / 1e3:.1f}; {c['profit'] / 1e6:.2f}; "
                f"{100 * c['gm']:.1f}%")
    ch = u["choices"]
    assert ch["chase"]["profit"] > max(ch["far"]["profit"], ch["near"]["profit"])
    lab.row("critical ratio early / late", f"{100 * u['ratio_far']:.1f}% / {100 * u['ratio_near']:.1f}%")
    lab.row("best early order's profit by forecast error, $m",
            "; ".join(f"{100 * k:.0f}%: {v / 1e6:.2f}" for k, v in u["cv"].items()))

    m = R["made"]
    lab.row("NIKE: footwear factories / countries / makers; apparel factories / countries / makers",
            f"{m['fw_factories']:.0f} / {m['fw_countries']:.0f} / {m['fw_makers']:.0f}; "
            f"{m['ap_factories']:.0f} / {m['ap_countries']:.0f} / {m['ap_makers']:.0f}")
    lab.row("NIKE footwear by country", ", ".join(f"{k} {v:.0f}%" for k, v in m["fw"].items()))
    lab.row("clothing exports 2023, $bn", ", ".join(f"{k} {v:.0f}" for k, v in sorted(m["exp2023"].items(), key=lambda kv: -kv[1])))
    lab.row("American jobs making clothes, thousand: 1990 / 2025", f"{m['jobs90']:.0f} / {m['jobs25']:.0f}")
    d = R["dollar"]
    lab.row("a dollar of NIKE's sales, cents: product / demand creation / other / net",
            " / ".join(f"{100 * d[k]:.0f}" for k in ("make", "demand", "other", "net")))

    t = R["turns"]["days"]
    lab.row("days of stock", ", ".join(f"{k} {v:.0f}" for k, v in sorted(t.items(), key=lambda kv: kv[1])))
    f = R["fast"]
    lab.row("Inditex 31 Jan 2026, EUR bn: stock + receivables - payables = working capital",
            f"{f['inventory']:.2f} + {f['receivables']:.2f} - {f['payables']:.2f} = {f['owc']:.2f}")
    o = R["offprice"]["index"]
    lab.row("sales since the year ending early 2015 (x)", ", ".join(f"{k} {v[2026]:.2f}" for k, v in o.items()))
    p = R["prices"]
    lab.row("American prices since 1990: clothes / all items / clothes in real terms",
            f"x{p['app_x']:.2f} / x{p['all_x']:.2f} / x{p['real']:.2f}")

    lux = R["luxury"]
    lab.row("Hermès revenue EUR bn and margin, 2022-2025",
            "; ".join(f"{y}: {v / 1e3:.1f} ({100 * o_ / v:.1f}%)" for y, (v, o_) in lux["rms"].items()))
    lab.row("LVMH 2025 margin by business group",
            ", ".join(f"{k} {100 * p_ / v:.0f}%" for k, (v, p_) in lux["mc"].items()))
    g = R["fickle"]["gucci"]
    lab.row("Gucci revenue / operating income, EUR bn, 2022-2025",
            "; ".join(f"{y}: {v / 1e3:.1f} / {o_ / 1e3:.2f}" for y, (v, o_) in g.items()))

    c = R["called"]
    lab.row("Inditex guidance for 2026: band; first half; second half 2025; second half needed for 58.5%",
            f"{c['lo']:.1f}-{c['hi']:.1f}%; {c['h1']}%; {c['h2_gm25']:.1f}%; {c['need']:.1f}%")
    lab.row("this series' call: Inditex FY2026 gross margin 58.5% or more", f"probability {100 * c['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    s = fashion.Season()
    bases = np.linspace(0, 200_000, 81)
    ax1.plot(bases / 1e3, [s.chase_at(b)["profit"] / 1e6 for b in bases], color=labs.GOLD, lw=1.8, label="base and chase")
    ax1.axhline(ch["far"]["profit"] / 1e6, color=labs.MUTED, lw=1.2, ls="--", label="all early")
    ax1.axhline(ch["near"]["profit"] / 1e6, color=labs.BLUE, lw=1.2, ls=":", label="all late")
    ax1.set_xlabel("early base order, thousand shirts")
    ax1.set_ylabel("expected profit, $m")
    ax1.set_title("Run it (the Works)")
    ax1.legend(fontsize=7)
    names = sorted(t, key=t.get)
    ax2.barh(range(len(names)), [t[n] for n in names], color=labs.PURPLE)
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels(names, fontsize=6)
    ax2.set_xlabel("days of cost of sales held as stock")
    ax2.set_title("How long stock sits")
    lab.fig = fig
    lab.note = ("Clothes are ordered before anyone knows what will sell. Fast fashion guesses less by chasing the hits close "
                "to home; off-price buys everyone else's wrong guesses; luxury makes fewer than people want and never "
                "holds a sale; all of them rest on contract factories and on taste that can turn.")
    return lab
