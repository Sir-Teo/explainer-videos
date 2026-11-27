"""Lab 18: two makers of airliners and their year, the Run it duel, how an airliner is made, a programme's learning curve
and valley of cash, program accounting, why only two, launch aid, engines sold for their servicing, the suppliers, the
order book and the lessors, defence and the world's budgets, the landscape, and Boeing's first-delivery forecasts."""

import numpy as np

from explainer.industry.works import aircraft  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry18.compute import results

TITLE = "Aerospace and defence: the learning curve, two makers and the money after the sale"
GOAL = ("Measure the two airframers' 2025 and Boeing's losses; play the duel between a new airliner and new engines and "
        "see a few points of fuel flip it; trace a programme's learning curve and valley of cash; see what program "
        "accounting defers; price a newcomer against incumbents far down their curves; find who pays when a launch-aid "
        "programme flops; value an engine sold below cost; compare margins along the chain; read the defence budgets; and "
        "score Boeing's first-delivery forecasts, with this series' call.")
TASKS = [
    "With aircraft.Duel(options=aircraft.variant(new_gain=g, re_gain=0.14)), find the smallest fuel saving g for a new "
    "airliner at which building one becomes the better reply to a rival who re-engines. Is the game then still a dilemma?",
    "With aircraft.Programme(learning=L), find the learning rate L at which the programme's value today is zero. How many "
    "aircraft would it have to build at that rate (try years=40) before its cumulative cash turned positive?",
    "With aircraft.Engine(price=p), find the sale price at which the engine just pays back over 25 years at 8%. How much "
    "lower could the price go if the engine flew 4,000 hours a year instead of 3,000?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("2025 deliveries: Airbus / Boeing; Airbus backlog", f"{h['ab']} / {h['ba']}; {h['ab_backlog']:,}")
    ni = R["accounting"]["ni"]
    lab.row("Boeing net income, $bn: 2018 / 2019-2024 in all / 2025",
            f"{ni[2018]:.1f} / {sum(ni[y] for y in range(2019, 2025)):.1f} / {ni[2025]:.1f}")

    u = R["run"]
    t, a = u["table"], u["alt"]
    lab.row("the duel, $bn each (you, rival): new/new; new/re; re/re",
            f"{t['new|new'][0]:.1f}, {t['new|new'][1]:.1f}; {t['new|reengine'][0]:.1f}, {t['new|reengine'][1]:.1f}; "
            f"{t['reengine|reengine'][0]:.1f}, {t['reengine|reengine'][1]:.1f}")
    lab.row("equilibrium; with a 23% / 13% leap", f"{u['eq']}; {u['alt_eq']} (new/re {a['new|reengine'][0]:.1f})")
    assert u["eq"] == [("reengine", "reengine")] and u["alt_eq"] == [("new", "new")]

    m = R["making"]
    lab.row("2025 deliveries by model: 737 / 787 / A320 family / A220", f"{m['ba']['737']} / {m['ba']['787']} / "
            f"{m['ab']['a320']} / {m['ab']['a220']}")
    lab.row("737 rate a month: end of 2025 / 2026; A320 target", f"{m['rate737']} / {m['rate47']}; {m['rate320']}")

    p = R["programme"]
    lab.row("the Works' programme: unit cost of the 1st / 2nd / 1,000th ($m); crosses the price at",
            f"{p['unit'][1]:.0f} / {p['unit'][2]:.0f} / {p['unit'][1000]:.0f}; the {p['cross']:.0f}th")
    lab.row("trough ($bn); break-even (year, aircraft); value at 8% ($bn); with 90% learning",
            f"{p['trough']:.1f}; year {p['be']['year']}, {p['be']['units']:,.0f}; {p['npv']:.1f}; {p['slow']:.1f}")

    ac = R["accounting"]
    lab.row("program accounting: average cost over 1,500 ($m); 777X deferred production costs, Sept 2026 ($bn)",
            f"{ac['avg']:.0f}; {ac['dpc'] / 1e3:.1f}")
    lab.row("accounting quantities: 737 / 787 / 777X (777X firm orders)",
            f"{ac['aq']['737']:,} / {ac['aq']['787']:,} / {ac['aq']['777x']} ({ac['undel']['777x']})")
    lab.row("Commercial Airplanes, loss from operations ($bn): 2023 / 2024 / 2025 / 2026 9M",
            f"{ac['bca'][2023] / 1e3:.1f} / {ac['bca'][2024] / 1e3:.1f} / {ac['bca'][2025] / 1e3:.1f} / {ac['q9'] / 1e3:.1f}")

    tw = R["two"]
    lab.row("Airbus share of deliveries; years of orders: Airbus / Boeing",
            f"{100 * tw['share_ab']:.1f}%; {tw['ab_years']:.1f} / {tw['ba_years']:.1f}")
    lab.row("newcomer's value ($bn) at a price of $110m / $100m / $80m",
            f"{tw['entrant'][110]:.1f} / {tw['entrant'][100]:.1f} / {tw['entrant'][80]:.1f}")

    ai = R["aid"]
    lab.row("launch aid: the hit's trough without / with ($bn); the flop's unrepaid loan ($bn)",
            f"{ai['hit']['trough']:.1f} / {ai['hit']['trough_aid']:.1f}; {ai['loan'] - ai['flop']['repaid']:.1f}")
    lab.row("WTO countermeasures, $bn a year: DS316 / DS353", f"{ai['ds316'] / 1e3:.1f} / {ai['ds353'] / 1e3:.1f}")

    e = R["engines"]
    lab.row("GE commercial engines: equipment / services / profit ($bn); engines delivered",
            f"{e['equipment'] / 1e3:.1f} / {e['services'] / 1e3:.1f} / {e['profit'] / 1e3:.1f}; {e['engines']:,}")
    lab.row("the Works' engine: value ($m); payback year; servicing share",
            f"{e['life']['value']:.2f}; {e['life']['payback_years']}; {100 * e['life']['service_share']:.0f}%")

    s = R["suppliers"]["avg"]
    lab.row("average net margins 2015-2025: TransDigm / HEICO / Boeing / Spirit (to 2024)",
            f"{100 * s['TDG']:.1f}% / {100 * s['HEI']:.1f}% / {100 * s['BA']:.1f}% / {100 * s['SPR']:.1f}%")
    le = R["lessors"]
    lab.row("AerCap: aircraft owned / on order; 2025 sale gain ($m)", f"{le['owned']:,} / {le['order']}; {le['gain']}")

    d = R["defence"]
    lab.row("Lockheed: US government / cost-reimbursable / F-35 share of sales", f"{d['usg']}% / {d['costplus']}% / {d['f35']}%")
    lab.row("US defence spending, $bn in 2025 prices: 1987 / 1998 / 2010 / 2025",
            " / ".join(f"{d['real'][y]:,.0f}" for y in (1987, 1998, 2010, 2025)))
    b = R["budgets"]
    lab.row("SIPRI 2025, $bn (2024 prices): US / China / Russia; world", f"{b['top']['United States of America']:.0f} / "
            f"{b['top']['China']:.0f} / {b['top']['Russia']:.0f}; {b['world'][2025] / 1e3:,.0f}")

    c = R["called"]
    lab.row("Boeing's first-delivery targets: 787, 777X (target -> outcome)",
            f"{c['t787'][0]} -> {c['t787'][1]}; {c['t777x'][0]} -> {c['t777x'][1]} (expected)")
    lab.row("this series' call: first 777-9 delivered by the end of 2027", f"probability {100 * c['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    for cum, col, lab_ in ((p["cum"], labs.GREEN, "82% learning"), (p["cum_slow"], labs.RED, "90% learning")):
        ys = sorted(cum)
        ax1.plot(ys, [cum[y] for y in ys], color=col, lw=1.8, label=lab_)
    ax1.axhline(0, color="grey", lw=0.8)
    ax1.set_xlabel("year of the programme")
    ax1.set_ylabel("cumulative cash, $bn")
    ax1.set_title("The valley of cash (the Works)")
    ax1.legend(fontsize=7)
    cum = e["cum"]
    ys = sorted(cum)
    ax2.plot(ys, [cum[y] for y in ys], color=labs.PURPLE, lw=1.8)
    ax2.axhline(0, color="grey", lw=0.8)
    ax2.set_xlabel("years in service")
    ax2.set_ylabel("value to its maker, $m (discounted)")
    ax2.set_title("An engine sold below cost (the Works)")
    lab.fig = fig
    lab.note = ("A new airliner pays back only after about a thousand aircraft, once the learning curve has brought each "
                "one's cost below its price, so the two makers far down their curves face no third; and engines and many "
                "parts are sold for the decades of servicing that follow, where much of the money is made.")
    _ = np  # the tasks use numpy for their searches
    return lab
