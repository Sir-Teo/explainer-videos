"""Lab 31: the Works' store by price, staff and sales; the break-even volume for a price cut; retailers' margins; days of
stock, payables and the float; margin times turns; formats; Costco's members and fees; and this series' call."""

from explainer.industry.works import store
from videos.coursekit import labs
from videos.industry.industry31.compute import results

TITLE = "Grocery and mass retail: pennies, turned fast"
GOAL = ("Run a supermarket for a year and see how little room its rivals leave on price, staff and sales; split a dollar at "
        "the till; compute how suppliers fund a retailer's stock and how margin times turns makes a return; compare formats "
        "by sales per store and per square foot; take a warehouse club's profit apart into goods and fees; place the "
        "companies; and state a dated call.")
TASKS = [
    "With store.Store(elasticity=e).best_price(), make shoppers less sensitive to price (e = -4) and more (e = -8). How does "
    "the most profitable price move, and what gross margin would a store need for today's price to be the best one?",
    "With store.Store().breakeven_volume(cut), find the volume needed for cuts of 0.5%, 1%, 2% and 3%. Why does each extra "
    "point of price cut need more volume than the last?",
    "With store.float_days(inventory, payables, cogs), suppose Walmart took ten days longer to sell its goods. How much "
    "more cash would it need to find, and why do retailers fight to sell faster?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("Walmart: revenue; net profit; cents a dollar", f"${H['wmt_rev']:.0f}bn; ${H['wmt_ni']:.1f}bn; {100 * H['wmt_ni'] / H['wmt_rev']:.1f}")
    lab.row("Costco: membership fees; net profit", f"${H['fees']:.1f}bn; ${H['cost_ni']:.1f}bn")
    U = R["run"]
    lab.row("the Works' store: profit; cents a dollar", f"${U['base']['profit'] / 1e6:.2f}m; {100 * U['base']['margin']:.1f}")
    lab.row("profit by price level", ", ".join(f"{100 * (p - 1):+.0f}%: ${v / 1e6:.2f}m" for p, v in U["by_price"].items() if abs(round(100 * (p - 1)) - 100 * (p - 1)) < 1e-9 and round(100 * (p - 1)) % 2 == 0))
    lab.row("extra volume needed for a 1% / 2% price cut", f"{100 * U['cut1_need']:.1f}% / {100 * U['cut2_need']:.1f}%")
    lab.row("profit with staff hours -20% / +20%", f"${U['staff80']['profit'] / 1e6:.2f}m / ${U['staff120']['profit'] / 1e6:.2f}m")
    lab.row("profit if sales fall 0 / 5 / 10 / 15%", " / ".join(f"${v / 1e6:.2f}m" for v in U["drops"].values()))
    assert U["cut1_need"] > 0.05 and U["staff80"]["profit"] < U["base"]["profit"]
    M = R["dollar"]["margins"]
    lab.row("gross / net margin, latest year", "; ".join(f"{k}: {v['gross']:.0f}% / {v['net']:.1f}%" for k, v in M.items()))
    F = R["turns"]["float"]
    lab.row("days of stock / days payable / suppliers fund $bn", "; ".join(f"{k}: {v['inv_days']:.0f} / {v['pay_days']:.0f} / {v['funded']:+.1f}" for k, v in F.items()))
    Ro = R["turns"]["roa"]
    lab.row("return on assets = margin x turns", "; ".join(f"{k}: {v['margin']:.1f} x {v['turns']:.2f} = {v['margin'] * v['turns']:.1f}%" for k, v in Ro.items()))
    C = R["club"]
    lab.row("Costco: paid members 2024 / 2025 / 2026; renewal US & Canada", f"{C['members'][0]} / {C['members'][1]} / {C['members'][2]}m; {C['renew']}%")
    Cl = R["called"]
    lab.row(f"this series' call: Costco reports more than {Cl['line']:.0f} million paid members at the end of fiscal 2027", f"probability {100 * Cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    bp = U["by_price"]
    ax1.plot([100 * (p - 1) for p in bp], [v / 1e6 for v in bp.values()], color=labs.GOLD, lw=1.8)
    ax1.set_xlabel("prices against rivals, %")
    ax1.set_ylabel("$m a year")
    ax1.set_title("The Works' store: profit by price")
    bs = U["by_staff"]
    ax2.plot([100 * (s - 1) for s in bs], [v / 1e6 for v in bs.values()], color=labs.BLUE, lw=1.8)
    ax2.axhline(0, color=labs.MUTED, lw=0.8)
    ax2.set_xlabel("staff hours against normal, %")
    ax2.set_title("The Works' store: profit by staffing")
    lab.fig = fig
    lab.note = ("Rivals set a grocer's thin margin; fast-turning stock paid for later lets suppliers fund it; scale spreads the "
                "lorries and buyers over thousands of stores; the club charges at the door; and the market is the town.")
    _ = store
    return lab
