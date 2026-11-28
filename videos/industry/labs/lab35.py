"""Lab 35: the Works' hotel by rate, season, brand, channel and members' discount; the owner's return; a management
contract's fees; the hotel brands' and owners' returns on assets; the online agents' take; Carnival's dollar; a night at
roulette against the Strip's hold; and this series' call."""

from explainer.industry.works import hotel
from videos.coursekit import labs
from videos.industry.industry35.compute import results

TITLE = "Travel and hotels: a name on someone else's building"
GOAL = ("Fill a hotel for a year: find the rate that earns the most, then price month by month; split its dollar between the "
        "staff, the brand, the agents, the bank and the owner; compare branded and independent; test a members' discount; "
        "put the hotel under a management contract; compare the brands' and owners' returns; read the agents' and a cruise "
        "line's accounts; play roulette two thousand times; and state a dated call.")
TASKS = [
    "With hotel.Hotel(elasticity=e).best_flat(), make demand less sensitive to price (elasticity 1.2 instead of 1.5). What "
    "rate now earns the most, how full is the hotel, and why does a less price-sensitive market favour higher rates?",
    "With hotel.Hotel(branded=False, lift=L).best_monthly(), find the demand advantage the brand must bring (lift) for the "
    "branded hotel to earn the same as the independent one. Is the brand worth 10% of room revenue if it brings less?",
    "With hotel.roulette(spins=n), let the players stay for 50, 100 and 200 spins. How does the house's share of the chips "
    "bought change, and why, when the edge on each bet never moves?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("Marriott: rooms; owned or leased hotels; share of rooms", f"{H['rooms']:,}; {H['own_props']}; {100 * H['own_share']:.1f}%")
    lab.row("Marriott's revenue: reimbursed costs; fees; own hotels; total", f"${H['reimb']:.1f}bn; ${H['fees']:.1f}bn; ${H['owned']:.1f}bn; ${H['rev']:.1f}bn")
    U = R["run"]
    for k, lbl in (("flat", "one rate all year"), ("monthly", "a rate for each month"), ("indep", "independent, monthly rates")):
        y = U[k]
        lab.row(f"the Works' hotel, {lbl}: occupancy; rate; profit before interest",
                f"{100 * y['occupancy']:.1f}%; ${y['adr']:.0f}; ${y['ebitda'] / 1e6:.2f}m")
    M = U["monthly"]
    assert M["ebitda"] >= U["flat"]["ebitda"] > U["indep"]["ebitda"]
    lab.row("monthly rates, $", ", ".join(f"{r:.0f}" for r in M["rates"]))
    lab.row("the owner's cash after interest; a year on equity", f"${M['cash'] / 1e6:.2f}m; {100 * M['yield_']:.1f}%")
    lab.row("members' discount 0 / 5 / 10%: profit", " / ".join(f"${U['discount'][d]['ebitda'] / 1e6:.2f}m" for d in (0.0, 0.05, 0.1)))
    S = R["contract"]["split"]
    lab.row("under a management contract: base fee; incentive fee; priority return", f"${S['base_fee'] / 1e6:.2f}m; ${S['inc_fee'] / 1e6:.2f}m; ${S['prior'] / 1e6:.2f}m")
    L = R["light"]["roa"]
    lab.row("operating income on assets, five-year median", "; ".join(f"{k}: {v['roa']:.1f}%" for k, v in sorted(L.items(), key=lambda kv: -(kv[1]['roa'] or 0)) if v["roa"]))
    A = R["agents"]
    lab.row("Booking: gross bookings; revenue; take; marketing", f"${A['bk']['gb']:.0f}bn; ${A['bk']['rev']:.1f}bn; {100 * A['bk']['rev'] / A['bk']['gb']:.1f}%; ${A['bk']['mkt']:.1f}bn")
    lab.row("Airbnb: gross bookings; revenue; take", f"${A['ab']['gbv']:.1f}bn; ${A['ab']['rev']:.1f}bn; {100 * A['ab']['rev'] / A['ab']['gbv']:.1f}%")
    Cr = R["cruise"]
    lab.row("Carnival: tickets; on board; operating income; deposits; debt", f"${Cr['ticket']:.1f}bn; ${Cr['onboard']:.1f}bn; ${Cr['op']:.1f}bn; ${Cr['deposits']:.1f}bn; ${Cr['debt']:.1f}bn")
    Rl = R["casino"]["roulette"]
    lab.row("roulette: edge; bet per $500 of chips; hold on chips bought", f"{100 * Rl['edge']:.2f}%; ${Rl['wagered'] / Rl['players']:,.0f}; {100 * Rl['hold']:.1f}%")
    lab.row("the Strip in 2025: gaming win; table hold; slot hold", f"${R['casino']['strip']:.2f}bn; {R['casino']['tablepct']}%; {R['casino']['slotpct']}%")
    C = R["called"]
    lab.row("this series' call: Booking at least 1,400 million room nights in 2027",
            f"2026 on pace for about {C['est26']:,.0f}m; needs {100 * C['need']:.1f}% in 2027; probability {100 * C['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    B = U["by_rate"]
    ax1.plot(list(B), [y["ebitda"] / 1e6 for y in B.values()], color=labs.GOLD, lw=1.8, label="profit before interest, $m")
    ax1.plot(list(B), [3 * y["occupancy"] for y in B.values()], color=labs.BLUE, lw=1.4, ls="--", label="occupancy (x3)")
    ax1.set_xlabel("one rate all year, $")
    ax1.set_title("The Works' hotel by its rate")
    ax1.legend(fontsize=8)
    hist, edges = Rl["hist"], Rl["edges"]
    mids = [(edges[i] + edges[i + 1]) / 2 for i in range(len(hist))]
    ax2.bar(mids, hist, width=40, color=[labs.GREEN if x > 0 else labs.RED for x in mids])
    ax2.set_xlabel("a player's result, $")
    ax2.set_title("2,000 evenings at roulette")
    lab.fig = fig
    lab.note = ("A hotel sells nights that cannot be stored, so it prices to fill; the brand is paid first on revenue and the "
                "owner last; the agents, the ships, the casinos and the parks each earn on a different part of the trip.")
    _ = hotel
    return lab
