"""Lab 24: the Works' tender and the winner's curse, five tenders, a contractor's cash, construction spending, output per
worker and prices since 1970, margins along the chain, Fluor's contracts, Carillion, megaprojects, Ferrovial's two
margins, Quanta, the landscape and this series' call on California's railway."""

import numpy as np

from explainer.industry.works import contractor  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry24.compute import results

TITLE = "Construction: the bid, the cash and the missing productivity"
GOAL = ("Bid for jobs against rivals and see why the winner is usually the one who guessed lowest; follow a contractor's "
        "cash when its order book stops growing; measure construction's output per worker and prices against "
        "manufacturing since 1970; read margins along the chain from contractor to quarry; read Fluor's contract mix, "
        "Carillion's collapse and the record of megaprojects; compare building a road with owning it; place the "
        "companies; and state a dated call on California's railway.")
TASKS = [
    "With contractor.Tender(sd=s).best(), make estimates more accurate (s = 0.02) and less (s = 0.10). How do the best "
    "markup, the chance of winning and the margin on work won change? At s = 0.10, is any markup profitable while the "
    "rivals still add only 8%, and what does that say about rivals who underprice their uncertainty?",
    "With contractor.Tender(rivals=n), raise the number of rivals from 4 to 9. What happens to the margin a winner keeps "
    "at an 8% markup, and to the best markup? Why do crowded tenders hurt more?",
    "With contractor.cash_path(starts, pay_lag=p), set pay_lag to 1 (paying suppliers before being paid). How do the "
    "cash peak and the fall after the order book stops change? What does this say about growing on suppliers' money?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("Empire State Building: days from groundbreaking to opening; storeys a week", f"{h['days']}; {h['stories']}")
    lab.row("California HSR, $bn: 2008 plan; 2026 Phase 1 (cheaper route / as designed); Merced-Bakersfield",
            f"{h['hsr08']}; {h['phase1']} / {h['full']}; {h['mb']} (done {h['mb_done']})")

    for k, v in R["run"]["choices"].items():
        lab.row(f"the Works' tender, add {100 * float(k):.0f}%: wins of five / profit $m / margin on work won / winner's estimate",
                f"{v['wins']:.2f} / {v['profit']:+.2f} / {100 * v['margin']:+.1f}% / {100 * v['est_if_won']:+.1f}%")
    b = R["run"]["best"]
    lab.row("best markup; win rate; margin", f"{100 * b['markup']:.1f}%; {100 * b['win']:.0f}%; {100 * b['margin']:.1f}%")
    assert b["margin"] < b["markup"] / 3

    c = R["cash"]
    p = c["peak"]
    lab.row("order book that stops at month 24: cash at peak / 8 months later; profit at peak / 8 months later, $m",
            f"{c['cash'][p]:.0f} / {c['cash'][p + 8]:.0f}; {c['profit'][p]:.0f} / {c['profit'][p + 8]:.0f}")

    d = R["dollar"]
    lab.row("2025: construction spending $tn; value added $tn; share paid to employees (economy)",
            f"{d['spend']:.2f}; {d['va']:.2f}; {d['comp']}% ({d['all_comp']}%)")
    pr = R["productivity"]
    lab.row("real output per worker since 1970: construction / manufacturing / economy",
            " / ".join(f"x{pr['per'][k][2025]:.2f}" for k in ("construction", "manufacturing", "all")))
    lab.row("prices since 1970: construction / manufacturing / economy",
            " / ".join(f"x{pr['price'][k][2025]:.1f}" for k in ("construction", "manufacturing", "all")))
    lab.row("median net margin by group", ", ".join(f"{k} {100 * v:.1f}%" for k, v in sorted(R["chain"].items(), key=lambda kv: kv[1])))
    ct = R["contracts"]
    lab.row("Fluor backlog reimbursable share, end 2024 / end 2025", f"{100 * ct['share24']:.0f}% / {100 * ct['share']:.0f}%")
    k_ = R["carillion"]
    lab.row("Carillion: provisions £m (July, Sept 2017); cash lost 2017 £m; staff; UK public contracts",
            f"{k_['warn1']:.0f}, {k_['warn2']:.0f}; {k_['cash']:.0f}; {k_['staff']:,.0f}; {k_['contracts']:.0f}")
    m = R["mega"]
    lab.row("megaprojects: share over budget; rail overrun / demand shortfall; roads overrun",
            f"{m['share']}%; {m['rail']}% / {m['rail_demand']}%; {m['road']}%")
    f = R["concession"]
    lab.row("Ferrovial 2025 operating margin: construction / toll roads",
            f"{100 * f['con'][1] / f['con'][0]:.1f}% / {100 * f['hwy'][1] / f['hwy'][0]:.1f}%")
    lab.row("Quanta: backlog $bn end 2025 / Sept 2026; quarterly revenue Q3 2025 / Q3 2026",
            f"{ct['pwr_backlog'][0]} / {ct['pwr_backlog'][1]}; {ct['pwr_q3'][0]} / {ct['pwr_q3'][1]}")
    cl = R["called"]
    lab.row(f"this series' call: no fare-paying passengers Merced-Bakersfield before 1 January {cl['call_year']}",
            f"probability {100 * cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    cur = R["run"]["curve"]
    xs = [100 * float(k) for k in cur]
    ax1.plot(xs, [v["profit"] for v in cur.values()], color=labs.GOLD, lw=1.8, label="profit per tender, $m")
    ax1.plot(xs, [v["win"] for v in cur.values()], color=labs.BLUE, lw=1.2, ls="--", label="chance of winning")
    ax1.axhline(0, color=labs.MUTED, lw=0.8)
    ax1.set_xlabel("markup on your estimate, %")
    ax1.set_title("Run it (the Works)")
    ax1.legend(fontsize=7)
    for k, col in (("construction", labs.GOLD), ("manufacturing", labs.BLUE), ("all", labs.MUTED)):
        s = pr["per"][k]
        ax2.plot(list(s), list(s.values()), color=col, lw=1.6, label=k)
    ax2.set_yscale("log")
    ax2.set_ylabel("real output per worker, 1970 = 1")
    ax2.set_title("Output per worker")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("The lowest bid usually comes from the lowest estimate, so builders keep a few cents of each dollar; fixed "
                "prices put the estimate's error on the builder; other people's cash flatters a growing contractor; output "
                "per worker has fallen since 1970; the money is with whoever owns the quarry, the crane or the road.")
    _ = np
    return lab
