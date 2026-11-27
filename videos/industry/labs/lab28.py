"""Lab 28: the Works' flight sold four ways, Littlewood's rule and overbooking, seat-mile arithmetic and break-even loads,
Delta's costs and fuel, 2020, the card money, the lessors, the landscape and this series' call on jet fuel."""

from explainer.industry.works import airline
from videos.coursekit import labs
from videos.industry.industry28.compute import results

TITLE = "Airlines: perishable seats, fixed costs"
GOAL = ("Sell one flight four ways and see the profit come from which seats go to whom; find Littlewood's protection level "
        "and the best overbooking; turn seat-mile revenue and cost into the load an airline needs to break even; read where "
        "Delta's dollar goes, what fuel did to its 2026, and what 2020 did to the whole industry; weigh the card money "
        "against the profit; compare the lessors with the airlines; place the companies; and state a dated call on fuel.")
TASKS = [
    "With airline.Flight(business=b), make business demand smaller (b = 25) and larger (b = 60). How does Littlewood's "
    "protection level change, and how does the profit of protecting compare with selling first come, first served?",
    "With airline.Flight(bump=x).sweep_oversell(), raise the payment to a bumped traveller from $900 to $3,000, and lower "
    "the no-show rate from 8% to 3% with Flight(noshow=0.03). How many extra seats should the airline sell in each case?",
    "With airline.breakeven_load(fare, casm, miles), find the load a 1,000-mile flight needs at 16 cents a seat-mile and an "
    "average fare of $190, then at $150. What happens to the break-even load when the cheap carriers cut fares by a fifth?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("American airline fares after inflation (2000 = 1): 2010 / 2019 / 2025",
            " / ".join(f"{H['real'][y]:.2f}" for y in (2010, 2019, 2025)))
    lab.row("nine listed American airlines, net income 2009-2025, $bn; per dollar of revenue",
            f"{H['total']:.1f}; {100 * H['total'] / H['total_rev']:.1f} cents")
    U = R["run"]
    for k, name in (("first", "first come, low fare"), ("high_only", "one fare of $429"), ("protect", f"hold back {U['lw']}"),
                    ("both", f"hold back {U['lw']}, oversell {U['best_over']}")):
        o = U[k]
        lab.row(f"the Works' flight, {name}: sold; average fare; bumped; profit",
                f"{o['sold']:.0f}; ${o['fare']:.0f}; {o['bumped']:.2f}; ${o['profit']:,.0f}")
    assert U["both"]["profit"] > U["protect"]["profit"] > 0 > U["first"]["profit"] > U["high_only"]["profit"]
    lab.row("Littlewood's level by business fare ($429 / $600)", f"{U['lw']} / {U['dear']['lw']}")
    S = R["seat"]
    for name, (rev, cost, lf) in (("Delta", S["dal"]), ("Southwest", S["luv"]), ("Spirit", S["save"])):
        be = cost / (rev / (lf / 100))
        lab.row(f"{name}, 2025: TRASM / CASM cents; load; break-even load",
                f"{rev:.2f} / {cost:.2f}; {lf:.1f}%; {100 * be:.0f}%")
    D = R["dollar"]
    lab.row("Delta 2025: costs $bn; people; fuel; revenue; net income",
            f"{D['total']:.1f}; {100 * D['items'][0][1] / D['total']:.0f}%; {100 * D['items'][1][1] / D['total']:.0f}%; "
            f"{D['revenue']:.1f}; {D['profit']:.2f}")
    P = R["pandemic"]
    for name, v in P["firms"].items():
        lab.row(f"{name}: revenue 2019 / 2020 $bn; operating income 2020", f"{v['rev19']:.1f} / {v['rev20']:.1f}; {v['op20']:.1f}")
    lab.row("load factor April 2020; passengers 2019 / 2020 (m); CARES Act payroll support $bn",
            f"{P['lf_m']['2020-04']:.0f}%; {P['enplane'][2019]:.0f} / {P['enplane'][2020]:.0f}; {P['psp']:.0f}")
    F = R["fuel"]
    lab.row("jet fuel $/gal, US Gulf Coast: 2020 / 2022 / 2025 / 2026 so far",
            f"{F['annual'][2020]:.2f} / {F['annual'][2022]:.2f} / {F['annual'][2025]:.2f} / {F['annual'][2026]:.2f}")
    lab.row("Delta all-in fuel $/gal: 2025; expected Q2 / Q3 / Q4 2026", f"{F['dal25']:.2f}; {F['q2']:.2f} / {F['q3']:.2f} / {F['q4']:.2f}")
    lab.row("American fares, change on a year before, 2026", ", ".join(f"{m[5:]}: {v:+.0f}%" for m, v in F["fares26"].items()))
    L = R["loyalty"]
    lab.row("card money against net income, 2025, $bn: Delta; American",
            f"{L['amex']:.1f} vs {L['dal_profit']:.2f}; {L['aal']:.1f} vs {L['aal_profit']:.2f}")
    Ls = R["lessors"]
    lab.row("median net margin 2021-2025: AerCap / Air Lease / Delta / United / Southwest",
            " / ".join(f"{100 * Ls[k]:.1f}%" for k in ("aer", "al", "dal", "ual", "luv")))
    lab.row("the four largest American airlines' share of eight's revenue, 2025", f"{100 * R['landscape']['top4']:.0f}%")
    C = R["called"]
    lab.row("Delta's 2026 EPS guidance: January; October", f"${C['jan'][0]:.2f}-{C['jan'][1]:.2f}; ${C['oct'][0]:.2f}-{C['oct'][1]:.2f}")
    lab.row(f"this series' call: Gulf Coast jet fuel averages more than ${C['line']:.2f} a gallon over 2027",
            f"probability {100 * C['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    sw = U["sweep"]
    ax1.plot(list(sw), [v / 1e3 for v in sw.values()], color=labs.GOLD, lw=1.8, label="revenue per flight, $k")
    ax1.axhline(U["cost"] / 1e3, color="#E8554E", lw=1.0, ls="--", label="the flight's cost")
    ax1.axvline(U["lw"], color=labs.BLUE, lw=1.0, ls=":", label=f"Littlewood: {U['lw']}")
    ax1.set_xlabel("seats held back for business travellers")
    ax1.set_title("Run it (the Works): holding seats back")
    ax1.legend(fontsize=7)
    m = P["lf_m"]
    ax2.bar(range(len(m)), list(m.values()), color=[("#E8554E" if v < 60 else labs.BLUE) for v in m.values()])
    ax2.set_xticks(range(0, len(m), 6))
    ax2.set_xticklabels(list(m)[::6], fontsize=7)
    ax2.set_ylabel("load factor, %")
    ax2.set_title("2020: the planes emptied")
    lab.fig = fig
    lab.note = ("A seat perishes at departure and the flight's cost is fixed, so the profit is in which seat goes to whom; "
                "competition keeps the margin on a seat-mile thin; fuel is set by wars; the cost cannot be cut when the "
                "passengers vanish; the banks pay Delta and American more for miles than either earns; and the lessors keep more.")
    _ = airline
    return lab
