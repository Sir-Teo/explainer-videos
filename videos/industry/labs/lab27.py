"""Lab 27: the Works' shipping market and the owner's two rules, a voyage at different speeds, ZIM's freight and profits,
the fleet and the orderbook, chokepoint traffic, Frontline's earnings, the forwarders, the landscape and this series' call
on Hapag-Lloyd and ZIM."""

from explainer.industry.works import ship
from videos.coursekit import labs
from videos.industry.industry27.compute import results

TITLE = "Shipping: nearly free, and never safe"
GOAL = ("Price a ship's day from its utilization and see why the boom builds the bust; compare ordering with the market "
        "against ordering against it; find the cheapest speed for a voyage; read the container lines' freight and profits "
        "through the pandemic boom and the bust; count the ships through the world's chokepoints since 2019; read a tanker "
        "owner's earnings against its breakeven; compare the lines with the lessors and the forwarders; place the companies; "
        "and state a dated call on a merger.")
TASKS = [
    "With ship.Market(lag=l).owner(rule), shorten the delivery lag from three years to one, then lengthen it to five. How "
    "do the two rules' returns change? Why does a longer lag make following the market worse?",
    "With ship.Market(herd=h).path(), let the industry order less in booms (h = 0.1) and more (h = 0.35). How high do "
    "earnings go, how long do busts last, and what happens to the gap between the two rules?",
    "With ship.best_speed(fuel_price, ship_day=d), raise the ship's other daily cost from $40,000 to $80,000 (a dearer, newer "
    "ship) at fuel of $600. Does the cheapest speed rise or fall, and why does an expensive ship sail faster?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("ocean freight on one pair of trainers (5,000 pairs a 40-foot box): 2019 / 2022 / 2025",
            " / ".join(f"${H['per_pair'][y]:.2f}" for y in (2019, 2022, 2025)))
    lab.row("Suez Canal, March 2021: ships a day before; lowest day", f"{H['before']:.0f}; {H['low']:.0f} on {H['low_day']}")
    U = R["run"]
    for k in ("follow", "against"):
        o = U[k]
        lab.row(f"the Works' owner, {k} the market: ships; average price $m; earnings at delivery $k/day; return",
                f"{len(o['ships'])}; {o['avg_price']:.0f}; {o['avg_earn_at_delivery']:.0f}; {100 * o['ret']:+.0f}%")
    assert U["against"]["ret"] > U["follow"]["ret"]
    D = R["day"]
    lab.row("11,000-mile voyage: days / fuel t / cost $m at 20 knots; at 16 knots",
            f"{D['v20']['days']:.1f} / {D['v20']['fuel_t']:,.0f} / {D['v20']['total'] / 1e6:.2f}; "
            f"{D['v16']['days']:.1f} / {D['v16']['fuel_t']:,.0f} / {D['v16']['total'] / 1e6:.2f}")
    lab.row("cheapest speed, knots, by fuel price $/t", ", ".join(f"{p}: {v:.1f}" for p, v in D["best"].items()))
    B = R["box"]
    lab.row("world port traffic m TEU 2010 / 2024; fleet m TEU 2021 / 2025; on order", f"{B['world'][2010]:.0f} / {B['world'][2024]:.0f}; "
            f"{B['fleet21']:.0f} / {B['fleet']}; {B['order']}")
    C = R["cycle"]
    lab.row("ZIM freight per TEU, 2016-2025", ", ".join(f"{y}: {v:,.0f}" for y, v in C["rate"].items()))
    lab.row("ZIM freight per TEU, by quarter", ", ".join(f"{q}: {v:,.0f}" for q, v in C["q"].items()))
    lab.row("ZIM net income $bn 2021 / 2022 / 2023; Maersk EBIT $bn 2019 / 2022 / 2025",
            f"{C['zim'][2021][1]:.2f} / {C['zim'][2022][1]:.2f} / {C['zim'][2023][1]:.2f}; "
            f"{C['maersk'][2019][1]:.2f} / {C['maersk'][2022][1]:.2f} / {C['maersk'][2025][1]:.2f}")
    K = R["choke"]["annual"]
    for name in ("Suez Canal", "Cape of Good Hope", "Panama Canal", "Strait of Hormuz", "Malacca Strait"):
        lab.row(f"ships a day, {name}: 2019 / 2023 / 2024 / 2026", " / ".join(f"{K[name][y]:.0f}" for y in (2019, 2023, 2024, 2026)))
    T = R["tanker"]
    lab.row("Frontline VLCC $/day: breakeven; spot Q2 / Q3 2026; booked Q4; one-year charter",
            f"{T['be']:,.0f}; {T['q2']:,.0f} / {T['q3']:,.0f}; {T['q4']:,.0f}; {T['tc']:,.0f}")
    P = R["ports"]
    lab.row("net margin 2021 / 2023: Expeditors; C.H. Robinson",
            f"{100 * P['fw']['Expeditors'][2021][1]:.1f}% / {100 * P['fw']['Expeditors'][2023][1]:.1f}%; "
            f"{100 * P['fw']['C.H. Robinson'][2021][1]:.1f}% / {100 * P['fw']['C.H. Robinson'][2023][1]:.1f}%")
    cl = R["called"]
    lab.row("ZIM's 2026 adjusted EBITDA guidance, $bn", "; ".join(f"{w}: {lo}-{hi}" for w, lo, hi in cl["g"]))
    lab.row(f"this series' call: Hapag-Lloyd completes its purchase of ZIM by {cl['call']}", f"probability {100 * cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    e = U["path"]["earn"]
    ax1.plot(range(len(e)), e, color=labs.GOLD, lw=1.6, label="earnings a day, $k")
    for s in U["follow"]["ships"]:
        ax1.axvline(s["order"], color=labs.RED if hasattr(labs, "RED") else "#E8554E", lw=0.8, ls="--")
    for s in U["against"]["ships"]:
        ax1.axvline(s["order"], color=labs.BLUE, lw=0.8, ls=":")
    ax1.set_xlabel("year")
    ax1.set_title("Run it (the Works): orders, follow (dashed) and against (dotted)")
    ax1.legend(fontsize=7)
    sp = list(D["sweep"])
    ax2.plot(sp, list(D["sweep"].values()), color=labs.GOLD, lw=1.8, label="whole voyage")
    ax2.plot(sp, list(D["fuel_sweep"].values()), color=labs.BLUE, lw=1.2, ls="--", label="fuel")
    ax2.plot(sp, list(D["ship_sweep"].values()), color=labs.MUTED, lw=1.2, ls=":", label="the ship's days")
    ax2.set_xlabel("knots")
    ax2.set_ylabel("$m a voyage")
    ax2.set_title("Slow steaming")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("Big slow ships and one standard box made the voyage nearly free; a full fleet charges almost anything and a "
                "half-empty one almost nothing; everyone orders at once and the ships arrive together; and a few narrow "
                "places carry the whole system.")
    _ = ship
    return lab
