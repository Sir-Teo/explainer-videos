"""Lab 3: keep a bakery's books, watch a profitable firm run out of cash, and take six real companies apart."""

import numpy as np

from videos.coursekit import labs
from explainer.industry.register import get
from explainer.industry.works import firm
from videos.industry.industry3.compute import results

TITLE = "The accounts: double entry, cash against profit, and the Du Pont identity"
GOAL = ("Post the bakery's first entries and check that the books balance after each one; run the generic firm for a "
        "year and reconcile its three statements; grow it until it runs out of cash; then rebuild six real companies' "
        "returns on equity as margin times speed times borrowing, and Delta's operating income from its seat miles.")
TASKS = [
    "Give the cafes 10 days to pay instead of 60 in the growing bakery. In which year, if any, does it run out of "
    "cash now? What if the miller gives it 60 days?",
    "Costco's fees were $5.9bn of its $11.7bn operating income. If it cut its membership fee by a fifth and kept every "
    "member, by how much would operating income fall, and what return on equity would the Du Pont identity then give?",
    "Delta's revenue per seat mile was 21.26 cents and its cost 19.31. By how much would fuel (3.29 cents) have to rise "
    "to wipe out its operating income, all else equal? What price per gallon is that, at $2.30 a gallon?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    # 1. Double entry: the books balance after every post
    B = R["bakery"]
    assert all(abs(e["assets"] - e["liabilities"] - e["equity"]) < 1e-9 for e in B["entries"])
    lab.row("bakery: entries posted / profit so far", f"{len(B['entries'])} / ${B['profit']:,.0f}")

    # 2. A year from operations: the three statements reconcile
    y = R["bakery_year"]
    lab.row("bakery's year: sales, net profit, cash from operations",
            f"${y['income']['revenue']:,.0f}, ${y['income']['net']:,.0f}, ${y['cash']['operating']:,.0f}")
    r = y["ratios"]
    assert abs(r["roe"] - firm.dupont(r["net_margin"], r["turnover"], r["leverage"])) < 1e-12

    # 3. Growing too fast: profitable every year, out of cash
    g = R["growth"]
    first_negative = next(x["year"] for x in g if x["cash"] < 0)
    lab.row("growing bakery: profit in year 5 / cash runs out in year", f"${g[-1]['profit']:,.0f} / {first_negative}")
    assert all(x["profit"] > 0 for x in g)

    # 4. Six companies: return on equity as margin x speed x borrowing
    S = R["six"]
    for k in ("cost", "msft", "jpm", "lly"):
        d = S[k]
        assert abs(d["roe"] - d["ni"] / d["equity"]) < 1e-9
        lab.row(f"{d['name']}: margin x speed x borrowing = ROE",
                f"{100 * d['net_margin']:.1f}% x {d['turnover']:.2f} x {d['leverage']:.1f} = {100 * d['roe']:.0f}%")

    # 5. Costco: paid before it pays
    c = R["costco"]
    lab.row("Costco: days of stock / days to pay suppliers", f"{c['inventory_days']:.0f} / {c['payable_days']:.0f}")
    assert c["payable_days"] > c["inventory_days"]

    # 6. Delta: the seat-mile margin rebuilds operating income
    d = R["delta"]
    lab.row("Delta: margin per seat mile x seat miles", f"{d['margin']:.2f}c x {get('dal.asm') / 1e3:,.0f}bn = "
            f"${d['check']:.2f}bn (reported ${get('dal.oi'):.2f}bn)")

    # 7. Microsoft: profit against free cash
    m = R["cash"]["msft"]
    lab.row("Microsoft FY2026: net income / free cash", f"${m['ni']:.1f}bn / ${m['fcf']:.1f}bn")

    fig, (ax1, ax2) = labs.figure(2)
    yrs = [x["year"] for x in g]
    ax1.plot(yrs, [x["profit"] / 1e3 for x in g], marker="o", color=labs.GREEN, label="profit")
    ax1.plot(yrs, [x["cash"] / 1e3 for x in g], marker="o", color=labs.RED, label="cash in the bank")
    ax1.axhline(0, color=labs.GREY, lw=0.8)
    ax1.set_xlabel("year")
    ax1.set_ylabel("$ thousands")
    ax1.set_title("The growing bakery: profitable and out of cash")
    ax1.legend(fontsize=8)
    t = np.geomspace(0.02, 6, 100)
    for roa in (0.01, 0.03, 0.1, 0.3):
        ax2.plot(t, roa / t, color=labs.GREY, lw=0.7, ls="--")
    for k, dd in S.items():
        ax2.scatter(dd["turnover"], dd["net_margin"], s=40)
        ax2.annotate(dd["name"], (dd["turnover"], dd["net_margin"]), fontsize=7, xytext=(3, 3),
                     textcoords="offset points")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlim(0.02, 6)
    ax2.set_ylim(0.008, 0.8)
    ax2.set_xlabel("sales per $ of assets")
    ax2.set_ylabel("net profit per $ of sales")
    ax2.set_title("Margin against speed; dashed: equal return on assets")
    lab.fig = fig
    lab.note = ("The statements always reconcile because they are three views of one set of double entries. Profit "
                "and cash part when customers pay late, stock piles up or equipment is bought; borrowing multiplies "
                "the return on assets into the return on equity, for better and worse.")
    return lab
