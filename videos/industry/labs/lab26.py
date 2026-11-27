"""Lab 26: the Works' office and warehouse in 2019 and 2026 and the lender's three tests, one point of rate, Realty
Income's buying yield against the Treasury, income against occupancy, WeWork, a dollar of Prologis's rent, banks' loans
and delinquencies, the sectors, BXP's offices, e-commerce and the warehouses, the owners and the services firms, the
landscape and this series' call on BXP."""

from explainer.industry.works import building
from videos.coursekit import labs
from videos.industry.industry26.compute import results

TITLE = "Property: income over a rate"
GOAL = ("Value a building as its income over a rate and see how far a point of rate moves it; follow an office and a "
        "warehouse bought in 2019 to the day their loans fall due; find what a lender will lend by its three tests; read "
        "what a landlord buys and at what yield; compare kinds of building by margin and occupancy; read the offices' "
        "decline and the warehouses' rise in the filings; place the owners, managers and services firms; and state a "
        "dated call on America's largest office landlord.")
TASKS = [
    "With building.OFFICE_2026.but(cap=c).value() and building.refinance(...), lower the cap rate from 7.5% to 6% and "
    "raise it to 9%. How do the value, the new loan and the gap to the $130m loan change? Which of the lender's three "
    "tests binds in each case, and why does the debt-yield test not depend on the rate at all?",
    "With building.OFFICE_2019.but(occupancy=s), find the share let at which the office earns $5m, half its 2019 income. "
    "Then halve its running costs to $4.5m: where is the break-even now? What does this say about why offices with "
    "long-term tenants paying their own costs (net leases) are safer?",
    "With building.dev_margin(y, cap), Prologis's 6.7% stabilized yield is worth a 25.4% margin at a 5.34% cap rate. At "
    "what cap rate does the margin vanish? If cap rates rose a point while the building was under construction, what "
    "would the margin be?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("Fed commercial property price index (2001 = 100): 2007 peak / 2009 low; 2023 peak / 2025 low",
            f"{H['idx'][H['q'][H['pk1']]]:.0f} / {H['idx'][H['q'][H['lo1']]]:.0f} ({100 * H['fall1']:+.0f}%); "
            f"{H['idx'][H['q'][H['pk2']]]:.0f} / {H['idx'][H['q'][H['lo2']]]:.0f} ({100 * H['fall2']:+.0f}%)")
    for k in ("office", "warehouse"):
        v = R["run"][k]
        t0, t1, at = v["then"], v["now"], v["at"]
        lab.row(f"the Works' {k}: income $m 2019 / 2026; value $m 2019 / 2026; loan $m",
                f"{t0['noi']:.2f} / {t1['noi']:.2f}; {t0['value']:.1f} / {t1['value']:.1f}; {v['loan']:.1f}")
        lab.row(f"the Works' {k} refinanced at 7%: new loan $m ({at['binds']}); gap; cash out",
                f"{at['new_loan']:.1f}; {at['gap']:.1f}; {at['cash_out']:.1f}")
    off = R["run"]["office"]["at"]
    assert off["gap"] > 100 and R["run"]["warehouse"]["at"]["cash_out"] > 0
    lab.row("one point of rate: change in value at 4% / 5% / 7.5%",
            " / ".join(f"{100 * v:+.1f}%" for v in R["run"]["one_point"].values()))
    lab.row("break-even occupancy of the Works' office (2019 rent and costs)", f"{100 * R['run']['breakeven_occ']:.0f}%")

    B = R["bond"]
    lab.row("Realty Income's buying yield / 10-year Treasury / gap: 2015, 2021, 2025",
            "; ".join(f"{y}: {B['o_yield'][y]:.1f}% / {B['gs10'][y]:.2f}% / {B['spread'][y]:.1f}" for y in (2015, 2021, 2025)))
    L = R["lease"]
    lab.row("WeWork: lease obligations $bn; lease years left; member commitment, months",
            f"{L['we_lease']}; {L['we_term']}; {L['we_member']}")
    lab.row("WeWork net income $bn, 2019-2022", ", ".join(f"{y}: {v[1]:+.2f}" for y, v in L["we"].items()))
    D = R["debt"]
    lab.row("Prologis 2025: running costs / income per dollar of rent; income over interest",
            f"{100 * D['pld']['rentexp'] / D['pld']['rental']:.0f}c / {100 * D['pld']['noi'] / D['pld']['rental']:.0f}c; "
            f"{D['pld']['noi'] / D['pld']['interest']:.1f}x")
    lab.row("banks' commercial property loans $tn (latest); delinquency 1991 / 2010 / 2019 / latest",
            f"{D['loans_now'] / 1e3:.2f} ({D['loans_month']}); {D['dq_1991']} / {D['dq_2010']} / {D['dq_2019']} / {D['dq_now']}")
    for s in R["sectors"]:
        lab.row(f"sector: {s['name']} ({s['co']})", f"median margin {100 * s['margin']:.1f}%"
                + (f"; {s['occ']:.1f}% let" if s["occ"] else ""))
    O = R["office"]
    lab.row("BXP occupancy 2019 / 2025 / Sept 2026; leased Sept 2026", f"{O['bxp'][2019]} / {O['bxp'][2025]} / {O['q3']}; {O['leased']}")
    T = R["retail"]
    lab.row("e-commerce share: end 2019 / 2020 peak / latest", f"{T['ecom_2019']}% / {T['ecom_2020']}% / {T['ecom_now']}%")
    lab.row("Prologis: renewals; mark-to-market; development yield / margin / implied cap",
            f"+{T['pld']['change']}%; {T['pld']['mtm']}%; {T['pld']['yld']}% / {T['pld']['margin']}% / {100 * T['pld']['cap']:.2f}%")
    W = R["owners"]
    lab.row("Blackstone real estate $bn; listed owners' assets $tn; US commercial property $tn",
            f"{W['bx']}; {W['listed']:.2f}; {W['fsr_cre'] / 1e3:.1f}")
    cl = R["called"]
    lab.row(f"this series' call: BXP occupancy {cl['call']}% or more at 31 December 2027", f"probability {100 * cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    S = R["run"]["sweep_cap"]
    ax1.plot([100 * k for k in S], list(S.values()), color=labs.GOLD, lw=1.8, label="value of $10m a year")
    ax1.set_xlabel("capitalization rate, %")
    ax1.set_ylabel("$m")
    ax1.set_title("Income over a rate (the Works)")
    ax1.legend(fontsize=7)
    ys = sorted(B["o_yield"])
    ax2.plot(ys, [B["o_yield"][y] for y in ys], color=labs.GOLD, lw=1.6, label="Realty Income's buying yield")
    ax2.plot(ys, [B["gs10"][y] for y in ys], color=labs.BLUE, lw=1.2, ls="--", label="10-year Treasury")
    ax2.set_ylabel("% a year")
    ax2.set_title("What a landlord pays for rent")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("A building is worth its income over a rate; its income moves more than its rent because its costs are "
                "fixed; the rate moves with the whole market for money; the lease is the asset; and when income and rate "
                "both move against a building, its loan decides who loses.")
    _ = building
    return lab
