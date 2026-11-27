"""Lab 25: the Works' land deal, owned against optioned, one house's payment in 2021 and 2026, the builders' lots and
margins, starts, sales and months' supply, prices against costs and incomes, the payment's share of income, renters and
owners, the brokers, the stores and the lender, the landscape and this series' call on D.R. Horton."""

from explainer.industry.works import builder
from videos.coursekit import labs
from videos.industry.industry25.compute import results

TITLE = "Homes: the house, the land and the loan"
GOAL = ("Bet on land three years ahead by owning it or holding an option on it, and find the chance of a bust at which "
        "the two cross; split the rise in one house's monthly payment into price and rate; read the largest builders' "
        "lots, margins and incentives; compare house prices with building costs and incomes; follow the thirty-year rate "
        "and the payment's share of income; read the brokers', lenders' and stores' margins; place the companies; and "
        "state a dated call on America's largest builder.")
TASKS = [
    "With builder.LandDeal(bust=b).table(), deepen the bust from -15% to -25% and soften it to -5%. How do the owned and "
    "optioned profits in the bad case change, and where does breakeven_bust() move? Why does the option's worst case not "
    "change at all?",
    "With builder.LandDeal(escalator=e), let the land banker ask 8% a year instead of 12%, then 16%. At what escalator "
    "does owning beat optioning on expected profit per home at a 40% chance of a bust? Per dollar tied up?",
    "With builder.payment(principal, rate), find the rate at which a $352k loan costs the same $1,301 a month as the "
    "January 2021 loan. Then find the price at which a 7.3% loan costs $1,301. Which is the larger change, and what does "
    "that say about how rates and prices adjust?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("median new house, price / rate / payment with 10% down: Jan 2021; Oct 2026",
            f"${h['price'][h['m21']] / 1e3:.1f}k / {h['rate'][h['m21']]:.2f}% / ${h['pay'][h['m21']]:,.0f}; "
            f"${h['price'][h['m26']] / 1e3:.1f}k / {h['rate'][h['m26']]:.2f}% / ${h['pay'][h['m26']]:,.0f}")
    split = builder.payment(0.9 * h["price"][h["m26"]], h["rate"][h["m21"]] / 100)
    lab.row("2026 loan at the 2021 rate: payment; rise from price / from rate",
            f"${split:,.0f}; ${split - h['pay'][h['m21']]:,.0f} / ${h['pay'][h['m26']] - split:,.0f}")
    assert h["pay"][h["m26"]] - split > split - h["pay"][h["m21"]]
    lab.row("real house prices (1987 = 1): 2006 peak; 2025", f"{h['real'][h['peak06']]:.2f}; {h['real'][2025]:.2f}")

    t = R["run"]["table"]
    for how in ("own", "option"):
        v = t[how]
        lab.row(f"the Works' land deal, {how}: profit boom / bust / expected, $k; capital; return",
                f"{v['boom']:+.1f} / {v['bust']:+.1f} / {v['expected']:+.1f}; {v['capital']:.0f}; {100 * v['return']:.0f}%")
    lab.row("chance of a bust at which owning and optioning earn the same per home", f"{100 * R['run']['breakeven']:.1f}%")
    assert t["option"]["return"] > t["own"]["return"]

    D, L, N = R["builder"]["dhi"], R["builder"]["len"], R["builder"]["nvr"]
    lab.row("D.R. Horton FY2026: revenue $bn; homes; average price $k; gross margin (prior); pretax margin",
            f"{D['rev']}; {D['closed']:,}; {D['price']}; {D['gm']}% ({D['gm_prev']}%); {D['pretax']}%")
    tot = D["owned"] + D["controlled"]
    lab.row("D.R. Horton lots: owned / controlled; owned share; years of closings owned / all",
            f"{D['owned']:,.0f} / {D['controlled']:,.0f}; {100 * D['owned'] / tot:.0f}%; "
            f"{D['owned'] / D['closed']:.1f} / {tot / D['closed']:.1f}")
    lab.row("Lennar FY2025: deliveries; price $k (2023, 2024, 2025); gross margin; incentive $k a home; options share",
            f"{L['deliveries']:,}; {L['price'][2023]}, {L['price'][2024]}, {L['price'][2025]}; {L['gm'][0]}% to {L['gm'][1]}%; "
            f"{L['incent'][0]} to {L['incent'][1]}; {L['controlled'][0]}% to {L['controlled'][1]}%")
    lab.row("Lennar walked away from homesites; deposits written off $m; per lot $k",
            f"{L['walked']:,.0f}; {L['writeoff']}; {1e3 * L['writeoff'] / L['walked']:.1f}")
    lab.row("NVR: lots under purchase agreements; deposits $m; per lot $k", f"{N['lots']:,.0f}; {N['deposits']}; {N['per_lot']:.1f}")

    S, P = R["supply"], R["prices"]
    lab.row("housing starts: peak; low; 2025", f"{S['peak']}: {S['starts'][S['peak']] / 1e3:.2f}m; {S['low']}: "
            f"{S['starts'][S['low']] / 1e3:.2f}m; {S['starts'][2025] / 1e3:.2f}m")
    lab.row("since 2000: house prices / materials / consumer prices",
            f"x{P['cs'][2025]:.2f} / x{P['ppi'][2025]:.2f} / x{P['cpi'][2025]:.2f}")
    lab.row("median price over median household income: 1984; 2025", f"{P['ratio'][1984]:.2f}; {P['ratio'][2025]:.2f}")
    M = R["mortgage"]
    lab.row("payment on the median new house over median income: 1984 / 2020 / 2025",
            " / ".join(f"{100 * M['pay_share'][y]:.0f}%" for y in (1984, 2020, 2025)))
    r_ = R["rent"]
    lab.row("homeownership 2004 / 2025; rental vacancy 2009 / 2025; rents since 2000",
            f"{r_['own'][2004]:.1f}% / {r_['own'][2025]:.1f}%; {r_['vacancy'][2009]:.1f}% / {r_['vacancy'][2025]:.1f}%; "
            f"x{r_['rent'][2025]:.2f}")
    T = R["trade"]
    lab.row("net margin 2025: Zillow / Compass / Opendoor / Home Depot (FY to Jan 2026)",
            f"{100 * T['Zillow'][2025][1]:+.1f}% / {100 * T['Compass'][2025][1]:+.1f}% / {100 * T['Opendoor'][2025][1]:+.1f}% / "
            f"{100 * T['Home Depot'][2026][1]:+.1f}%")
    for c in sorted(R["landscape"]["companies"], key=lambda c: -c["margin"])[:5]:
        lab.row(f"landscape: {c['name']} ({c['group']}), FY{c['fy']}", f"${c['rev']:.1f}bn; median margin {100 * c['margin']:.1f}%")
    cl = R["called"]
    lab.row(f"this series' call: D.R. Horton closes fewer than {cl['call']:,} homes in fiscal 2027",
            f"probability {100 * cl['prob']:.0f}% (guidance {cl['g27_homes'][0]:,}-{cl['g27_homes'][1]:,})")

    fig, (ax1, ax2) = labs.figure(2)
    sw = R["run"]["sweep"]
    ps = [100 * p for p in sw]
    ax1.plot(ps, [v[0] for v in sw.values()], color=labs.GOLD, lw=1.8, label="own the lot")
    ax1.plot(ps, [v[1] for v in sw.values()], color=labs.BLUE, lw=1.8, label="option the lot")
    ax1.axhline(0, color=labs.MUTED, lw=0.8)
    ax1.set_xlabel("chance of a bust, %")
    ax1.set_ylabel("expected profit per home, $k")
    ax1.set_title("Run it (the Works)")
    ax1.legend(fontsize=7)
    ys = sorted(M["pay_share"])
    ax2.plot(ys, [100 * M["pay_share"][y] for y in ys], color=labs.GOLD, lw=1.6, label="payment over income, %")
    ax2.plot(ys, [M["rate"].get(y, float("nan")) for y in ys], color=labs.BLUE, lw=1.2, ls="--", label="30-year rate, %")
    ax2.set_title("The loan")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("What a buyer can pay is what a buyer can borrow; house prices have outrun building costs, and the gap is "
                "land and permission; builders bet on both years ahead and now hold most of their land as options; when "
                "rates rise their incentives pay down the buyer's rate out of their margins; the people in between keep "
                "little.")
    return lab
