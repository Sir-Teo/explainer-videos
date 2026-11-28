"""Lab 34: the Works' franchised restaurant for a year, its fees, wages and delivery orders; the franchisor's ten-year
profit by its take; McDonald's revenue by type and its two margins; franchisors against operators; DoorDash's losses
and profits; and this series' call on McDonald's restaurant count."""

from explainer.industry.works import franchise
from videos.coursekit import labs
from videos.industry.industry34.compute import results

TITLE = "Restaurants: who owns the store, and who keeps the dollar"
GOAL = ("Run a franchised restaurant for a year: split its dollar, find its payback, and see what a fall in sales, a wage "
        "rise and more delivery orders do to it; then sit on the franchisor's side and choose the fee that earns the most "
        "over ten years; compare McDonald's franchised and company-run margins; set franchisors against operators; read "
        "DoorDash's path from losses to profit; and state a dated call.")
TASKS = [
    "With franchise.Store().year(sales=S) (labour partly fixed), find the sales at which the franchisee's payback on $1.5m "
    "reaches seven years, at the film's costs and fees. How far below the normal $4.0m is that?",
    "With franchise.Store(wage=w).year(), find the wage rise that halves the franchisee's profit. If menu prices then rise "
    "to bring in exactly the extra labour cost, the fees, the advertising fund and the apps still take their shares of the "
    "new revenue: how much of the lost profit comes back?",
    "With franchise.Franchisor(patience=p).sweep(takes), make would-be franchisees more patient (seven years instead of "
    "five). Where does the franchisor's best take move, and what does that say about why a strong brand can charge more?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("McDonald's: restaurants; franchised share", f"{H['rest']:,}; {H['fr']}%")
    lab.row("McDonald's revenue: rents; royalties; its own restaurants; total", f"${H['rents']:.1f}bn; ${H['royal']:.1f}bn; ${H['cosales']:.1f}bn; ${H['rev']:.1f}bn")
    lab.row("franchisees' sales, not McDonald's revenue", f"${H['frsales']:.1f}bn")
    U = R["run"]
    b = U["base"]
    lab.row("the Works' restaurant: sales; take", f"${U['auv'] / 1e6:.2f}m; {100 * U['take']:.1f}%")
    lab.row("food / labour / fees / ads / other / apps / profit, $k",
            " / ".join(f"{b[k] / 1e3:.0f}" for k in ("food", "labour", "fees", "ad", "other", "apps", "profit")))
    lab.row("profit per dollar; payback on $1.5m", f"{100 * b['margin']:.1f}c; {b['payback']:.1f} years")
    for k, lbl in (("drop10", "sales 10% lower"), ("wage20", "wages 20% higher"), ("apps30", "twice the delivery orders"),
                   ("fee15", "a 15% take")):
        lab.row(f"profit with {lbl}", f"${U[k]['profit'] / 1e3:.0f}k ({100 * U[k]['margin']:.1f}c)")
    assert U["wage20"]["profit"] < U["drop10"]["profit"] < b["profit"]
    fr = U["franchisor"]
    best = max(fr, key=lambda t: fr[t]["total"])
    lab.row("the franchisor's best take over ten years; its profit", f"{100 * best:.1f}%; ${fr[best]['total'] / 1e9:.1f}bn")
    Sp = R["split"]
    lab.row("McDonald's margin on franchised sales against its own restaurants", f"{100 * Sp['fr_margin']:.0f}c against {100 * Sp['co_margin']:.0f}c a dollar")
    M = Sp["margins"]
    lab.row("operating income per dollar of revenue",
            "; ".join(f"{k}: {v['op']:.0f}c" for k, v in sorted(M.items(), key=lambda kv: -kv[1]["op"])))
    D = R["delivery"]
    lab.row("DoorDash: orders; value; revenue", f"{D['orders'] / 1e3:.2f}bn; ${D['gov']:.0f}bn; ${D['rev']:.1f}bn")
    lab.row("DoorDash's net income, $bn", ", ".join(f"{y}: {v:+.2f}" for y, v in D["ni"].items()))
    C = R["called"]
    lab.row(f"this series' call: McDonald's at least {C['target']:,} restaurants at the end of 2027",
            f"needs {C['need27']:,} net in 2027 after about {C['net26']:,} in 2026; probability {100 * C['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    bs = U["by_sales"]
    ax1.plot([100 * s for s in bs], [v / 1e3 for v in bs.values()], color=labs.GOLD, lw=1.8)
    ax1.axhline(0, color=labs.MUTED, lw=0.8)
    ax1.set_xlabel("sales against normal, %")
    ax1.set_ylabel("$ thousand a year")
    ax1.set_title("The franchisee's profit by sales")
    ax2.plot([100 * t for t in fr], [v["total"] / 1e9 for v in fr.values()], color=labs.BLUE, lw=1.8)
    ax2.axvline(100 * U["take"], color=labs.MUTED, lw=0.8, ls="--")
    ax2.set_xlabel("rent and royalties, % of sales")
    ax2.set_ylabel("$bn over ten years")
    ax2.set_title("The franchisor's profit by its take")
    lab.fig = fig
    lab.note = ("A franchisor sells the right to run its system and rents the building, so it keeps most of what it is paid; "
                "the franchisee carries the food, the crew and the leverage of a thin margin. Charge too much and fewer people "
                "open stores; this series' assumptions put the best take near the one McDonald's charges.")
    _ = franchise
    return lab
