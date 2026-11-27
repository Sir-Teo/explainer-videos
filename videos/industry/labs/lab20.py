"""Lab 20: Lipitor's fall, the Run it decision over Phase III, the phases and the funnel, success by phase and by
disease, the cost of one approved drug, research shares, the Works' drug and its cliff, the FDA's generic prices,
approvals, drug prices and output, Keytruda and Pfizer, Medicare's negotiation, tirzepatide and Lilly's factories, the
biotech companies, the landscape and the dollar, and Lilly's forecasts."""

import numpy as np

from explainer.industry.works import pharma  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry20.compute import results

TITLE = "Pharmaceuticals: the odds, the cost of a medicine and the patent cliff"
GOAL = ("Follow Lipitor through its cliff; decide whether to pay for Phase III and value the option to stop; follow a "
        "hundred candidates through the phases with BIO's odds; work out what one approved drug costs, out of pocket and "
        "with the waiting counted; value a drug's life before and after its date; read the FDA's generic prices; compare "
        "drug prices and output with the rest of the economy; read the companies of a few products, Medicare's first "
        "negotiation and Lilly's boom; place the biotech and generics companies; split a dollar of revenue; and score "
        "Lilly's forecasts, with this series' call.")
TASKS = [
    "With pharma.cost_per_approval(phases), lower Phase II's success rate from 0.289 to 0.20 and raise it to 0.40. How "
    "much does the cost per approved drug change, out of pocket and capitalized? Which phase's odds matter most?",
    "With pharma.Option(small=pharma.Drug(peak=P)), find the small market's peak sales P above which going on pays even "
    "when the market is small, so that the option to stop is worth nothing. How does the option's value change as p_big "
    "rises from 0.1 to 0.9?",
    "With pharma.Drug(exclusivity=E), find the drug's value at launch for 8, 10, 12 and 14 years of exclusivity. How much "
    "is each extra year of protection worth, and how does that compare with the capitalized cost per approval?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lip = h["lipitor"]
    lab.row("Lipitor, $m: 2010 / 2011 / 2012; fall in 2012", f"{lip[2010]:,} / {lip[2011]:,} / {lip[2012]:,}; "
            f"{100 * h['lip_fall']:.1f}%")
    lab.row("tirzepatide, $bn: 2024 / 2025; share of Lilly's 2025 revenue", f"{h['tirz'][2024]:.1f} / {h['tirz'][2025]:.1f}; "
            f"{h['lly_share']}%")

    u = R["run"]
    lab.row("Run it, $m: go on if big / if small; commit / flexible / option",
            f"{u['big']:,.0f} / {u['small']:,.0f}; {u['commit']:,.0f} / {u['flexible']:,.0f} / {u['option']:,.0f}")
    assert u["flexible"] >= u["commit"]

    o = R["odds"]
    lab.row("phase success, %: I / II / III / review", " / ".join(f"{100 * q:.1f}" for *_, q in pharma.PHASES))
    lab.row("of 100 entering Phase I: reach II / III / review / approved",
            " / ".join(f"{100 * p:.0f}" for p in o["reach"][1:]))
    lab.row("likelihood of approval, %: " + " / ".join(o["areas"]), " / ".join(f"{v:.1f}" for v in o["areas"].values()))

    c = R["cost"]
    lab.row("cost, $m: per candidate / per approval / capitalized; years", f"{c['spend']:.0f} / {c['per_approval']:,.0f} / "
            f"{c['capitalized']:,.0f}; {c['years']:.1f}")
    pp = R["pipeline"]
    lab.row("candidates per approval entering: " + " / ".join(pp), " / ".join(f"{v:.1f}" for v in pp.values()))
    rd = R["rnd"]["share"]
    lab.row("research, % of revenue: Regeneron / Merck / Pfizer / Teva",
            " / ".join(f"{100 * rd[k]:.0f}" for k in ("Regeneron", "Merck", "Pfizer", "Teva")))
    t = R["rd_total"]
    lab.row("research of the companies measured, 2025: $bn / share of revenue", f"{t['total']:.1f} / {100 * t['total'] / t['rev']:.0f}%")

    d = R["drug"]
    lab.row("the Works' drug: value at launch $m; share earned before the cliff",
            f"{d['npv']:,.0f}; {100 * R['drug_split']['before']:.0f}%")

    cl = R["cliff"]
    lab.row("generic price below the brand's, %: 1 / 2 / 4 / 6+ makers; median generic price, % of brand",
            " / ".join(str(v) for v in cl["fda"].values()) + f"; {cl['median']}")
    lab.row("generic approvals, 2021-2024", " / ".join(str(v) for v in R["generics"].values()))
    lab.row("novel drugs approved, 2021-2025", " / ".join(str(v) for v in R["approvals"].values()))

    p = R["prices"]
    lab.row("since 1982: drug producer prices / CPI / relative", f"x{p['ppi_x']:.2f} / x{p['cpi_x']:.2f} / x{p['rel'][2025]:.2f}")
    ip = R["output"]["ip"]
    lab.row("medicine output (1972 = 1): 2007 / 2019 / 2025", f"{ip[2007]:.2f} / {ip[2019]:.2f} / {ip[2025]:.2f}")

    pf = R["pfizer"]
    lab.row("Pfizer revenue, $bn: 2019 / 2021 / 2022 / 2023", " / ".join(f"{pf[y]:.1f}" for y in (2019, 2021, 2022, 2023)))
    m = R["medicare"]
    lab.row("Medicare's first ten: users (m) / saving $bn / % of net spending", f"{m['users']} / {m['saving']} / {m['pct']}%")

    b = R["build"]
    lab.row("Lilly capex, $bn: 2023 / 2024 / 2025; inventories 2023 / 2025",
            " / ".join(f"{v:.1f}" for v in b["capex"].values()) + f"; {b['inventory'][2023]:.1f} / {b['inventory'][2025]:.1f}")

    bt = R["biotech"]
    lab.row("Moderna revenue, $bn: 2019 / 2022 / 2025", " / ".join(f"{bt['mrna'][y]:.2f}" for y in (2019, 2022, 2025)))
    lab.row("median margin 2021-2025: Vertex / Regeneron / Amgen / Gilead",
            " / ".join(f"{100 * bt['margins'][k]:.0f}%" for k in ("Vertex", "Regeneron", "Amgen", "Gilead")))

    dl = R["dollar"]
    lab.row(f"a dollar of {dl['n']} companies' revenue, cents: making / research / everything else / profit",
            " / ".join(f"{100 * dl[k]:.0f}" for k in ("make", "research", "rest", "profit")))

    cd = R["called"]
    lab.row("Lilly's guidance: 2025 range / actual; 2026 range, raised", f"{cd['g2025'][0]:.0f}-{cd['g2025'][1]:.0f} / "
            f"{cd['a2025']:.1f}; {cd['g2026'][0]:.0f}-{cd['g2026'][1]:.0f}, {cd['g2026_oct'][0]:.0f}-{cd['g2026_oct'][1]:.0f}")
    lab.row("this series' call: Lilly's 2026 revenue at least $92.0bn", f"probability {100 * cd['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    s = d["sales"]
    ax1.bar(range(1, len(s) + 1), s, color=[labs.PURPLE if t < 12 else labs.GREY for t in range(len(s))])
    ax1.set_xlabel("year after launch")
    ax1.set_ylabel("sales, $m")
    ax1.set_title("A drug's life (the Works)")
    rates = np.linspace(0.15, 0.45, 13)
    per = []
    for q2 in rates:
        ph = list(pharma.PHASES)
        ph[1] = (ph[1][0], ph[1][1], ph[1][2], float(q2))
        per.append(pharma.cost_per_approval(tuple(ph))["capitalized"] / 1e3)
    ax2.plot(100 * rates, per, color=labs.GOLD, lw=1.8)
    ax2.axvline(28.9, color=labs.GREY, ls="--", lw=1)
    ax2.set_xlabel("Phase II success rate, %")
    ax2.set_ylabel("capitalized cost per approval, $bn")
    ax2.set_title("The great filter sets the cost")
    lab.fig = fig
    lab.note = ("Most candidates fail, mostly in Phase II, so each approved medicine carries about a dozen failures and a "
                "decade of waiting; while it is protected its price pays for them, and when copies arrive it falls to near "
                "the cost of making it.")
    return lab
