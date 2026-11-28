"""Lab 33: the Works' distributor by safety stock, payment terms and drop-shipping; delivery cost by local share;
distributors' margins, working-capital days and margin times turns; a trading house's income; and this series' call."""

from explainer.industry.works import distributor
from videos.coursekit import labs
from videos.industry.industry33.compute import results

TITLE = "The middlemen: a penny a dollar, turned fast"
GOAL = ("Run a distributor for a year: split its dollar, find the money its suppliers' credit lends it, choose the safety "
        "stock that pays best, and compare holding stock with drop-shipping; see why density favours a few firms; compare "
        "real distributors' margins and payment days; take a trading house's profit apart; and state a dated call.")
TASKS = [
    "With distributor.Distributor(pay=p).year(), shorten the days the distributor takes to pay its makers from 56 to 30. How "
    "much money must it now find, and what does that cost it a year at 8%?",
    "With distributor.Distributor(lead=L).best_z() and .stock_days(), double the maker's lead time. How many more days of "
    "stock does the best policy hold, and how much profit is lost?",
    "With distributor.Route().cost_per_stop(s), find the local share at which a rival's delivery cost is one cent per dollar "
    "higher than yours at 40%, with $5,000 of goods a stop. Is that enough to drive it out of a market with a 1.5% margin?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("the three drug wholesalers: revenue; profit; cents a dollar", f"${H['big3_rev']:.0f}bn; ${H['big3_ni']:.1f}bn; {100 * H['big3_ni'] / H['big3_rev']:.1f}")
    lab.row("the largest drug maker in the extract", f"{H['maker']}: ${H['maker_rev']:.0f}bn")
    U = R["run"]
    b, bz, f, d = U["base"], U["best"], U["full"], U["drop"]
    lab.row("the Works' distributor: kept a dollar; costs; operating profit", f"{100 * U['gm']:.1f}c; {100 * U['opex']:.1f}c; {100 * (U['gm'] - U['opex']):.1f}c")
    lab.row("stock / receivables / payables / money needed", f"${b['inventory'] / 1e6:.0f}m / ${b['receivables'] / 1e6:.0f}m / ${b['payables'] / 1e6:.0f}m / ${b['capital'] / 1e6:.0f}m")
    lab.row("profit at 97.7% / best / every line filled", f"${b['profit'] / 1e6:.0f}m / ${bz['profit'] / 1e6:.0f}m ({100 * bz['fill']:.1f}%) / ${f['profit'] / 1e6:.0f}m")
    lab.row("drop-ship instead: sales; profit", f"${d['sales'] / 1e9:.2f}bn; ${d['profit'] / 1e6:.0f}m")
    assert bz["profit"] > b["profit"] > d["profit"] and b["capital"] < 0
    lab.row("cost a stop at 10% / 40% of a town's pharmacies", f"${U['route'][0.1]['cps']:.1f} / ${U['route'][0.4]['cps']:.1f}")
    M = R["returns"]["margins"]
    lab.row("net margin x turns = return on assets", "; ".join(f"{k}: {M[k]['net']:.1f} x {M[k]['turns']:.2f} = {M[k]['net'] * M[k]['turns']:.1f}%"
                                                         for k in ("McKesson", "Sysco", "Arrow", "Grainger", "Fastenal")))
    D = R["returns"]["days"]
    lab.row("net days of money tied up", "; ".join(f"{k}: {v['wc_days']:+.0f}" for k, v in D.items()))
    T = R["trading"]
    lab.row("Mitsui: revenue; gross profit; equity-method profit; profit (yen)", f"{T['rev']:,.0f}bn; {T['gp']:,.0f}bn; {T['equity']:.0f}bn; {T['profit']:.0f}bn")
    C = R["called"]
    lab.row(f"this series' call: Mitsui's profit for the year to March 2027 at least ¥{C['fc']:,.0f}bn", f"probability {100 * C['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    Z = U["by_z"]
    ax1.plot([s["stock_days"] for s in Z.values()], [s["profit"] / 1e6 for s in Z.values()], color=labs.GOLD, lw=1.8)
    ax1.axhline(0, color=labs.MUTED, lw=0.8)
    ax1.set_xlabel("days of stock")
    ax1.set_ylabel("$m a year")
    ax1.set_title("The Works' distributor: profit by stock")
    Rt = U["route"]
    ax2.plot([100 * s for s in Rt], [v["cps"] for v in Rt.values()], color=labs.BLUE, lw=1.8)
    ax2.set_xlabel("share of a town's pharmacies served, %")
    ax2.set_ylabel("$ a stop")
    ax2.set_title("Density: the cost of a delivery")
    lab.fig = fig
    lab.note = ("A distributor keeps a few cents of each dollar, but suppliers' credit funds its stock; it sells availability, so "
                "it stocks for nearly every order but not every last one; and density lets the biggest local player deliver "
                "for less.")
    _ = distributor
    return lab
