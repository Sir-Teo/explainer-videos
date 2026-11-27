"""Lab 29: the Works' lane and the rate a loaded mile needs, the trucking market, freight's units, the railway's cost by
density, the census of carriers, truckload against part-load margins, the parcel networks, the route and the Postal
Service, driverless trucks, and this series' call on Union Pacific and Norfolk Southern."""

from explainer.industry.works import freight
from videos.coursekit import labs
from videos.industry.industry29.compute import results

TITLE = "Rail, trucks and parcels: who owns the road"
GOAL = ("Price a truckload lane with an empty trip home and see why networks win; watch a trucking market with easy entry "
        "swing; compare what a ton-mile, a mile, a hundredweight and a parcel earn; compute a railway's cost by traffic "
        "density; count the trucking firms; compare part-load networks with truckload carriers; read the parcel networks "
        "and the cost of a delivery stop; read a driverless-truck company's dates; place the companies; and state a dated "
        "call on a railway merger.")
TASKS = [
    "With freight.Lane(miles=m).breakeven_head(take_back=False), shorten the lane to 250 miles and lengthen it to 1,500. "
    "Does the rate a loaded mile needed change? Now add a $300 charge for loading and unloading each way: why do short "
    "hauls cost more a mile?",
    "With freight.Market(entry=e).path(), let new trucks arrive in 2 months instead of 6, then in 12. How high does the spot "
    "rate go, how low does it fall, and for how many months after the peak is it below cost?",
    "With freight.Route(pps=k).per_package(spacing), raise the parcels a stop from 1.4 to 3 (a lockers-and-apartments "
    "route). How much does a parcel cost in the city and in the countryside? Why do parcel firms push for pick-up points?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("operating ratio 2009 / 2025: Union Pacific; BNSF; CSX; Norfolk Southern; Knight-Swift",
            "; ".join(f"{H['ors'][k][2009]:.1f}% / {H['ors'][k][2025]:.1f}%" for k in ("Union Pacific", "BNSF", "CSX", "Norfolk Southern", "Knight-Swift")))
    lab.row("active for-hire interstate trucking firms; with one truck", f"{H['carriers']:,.0f}; {H['one']:,.0f}")
    U = R["run"]
    lab.row("the Works' truck: cost a mile (before fuel + diesel)", f"${U['per_mile']:.2f} (${U['nonfuel']:.2f} + ${U['fuel_mile']:.2f})")
    lab.row("Chicago to Atlanta at $2.84: one way; home empty; with a chance of a load home",
            f"${U['out_rev'] - U['one_way']:,.0f}; ${U['empty']['profit']:,.0f}; ${U['back']['profit']:,.0f}")
    lab.row("rate a loaded mile needed, by share of miles empty", ", ".join(f"{100 * s:.0f}%: ${v:.2f}" for s, v in U["needed"].items()))
    assert U["needed"][0.5] > U["needed"][0.1] and U["back"]["profit"] > U["empty"]["profit"]
    Un = R["unit"]
    lab.row("rail cents a ton-mile; intermodal / truckload $ a mile; LTL $ a hundredweight; UPS $ a parcel",
            f"{Un['rail_tm']:.2f}; {Un['int_mile']:.2f} / {Un['tl_mile']:.2f}; {Un['ltl_cwt']:.2f}; {Un['ups']:.2f}")
    Rl = R["rail"]
    lab.row("the Works' railway: fixed $ a route mile; variable cents a ton-mile; density m; average cents; break-even m",
            f"{Rl['F']:,.0f}; {100 * Rl['v']:.2f}; {Rl['density'] / 1e6:.1f}; {100 * Rl['avg']:.2f}; {Rl['be'] / 1e6:.1f}")
    lab.row("rail prices after inflation (1981 = 1): 2001 / 2025", f"{Rl['real'][2001]:.2f} / {Rl['real'][2025]:.2f}")
    T = R["trucks"]
    lab.row("trucking firms by trucks in the fleet", ", ".join(f"{k}: {v:,.0f}" for k, v in T["sizes"]))
    c = T["cycle"]
    lab.row("the Works' market: peak rate; trough; months below cost after the peak",
            f"${max(c['rate']):.2f}; ${min(c['rate']):.2f}; {c['below']}")
    M = T["margins"]
    lab.row("operating margin 2025: Old Dominion / Saia / XPO; Knight-Swift / Schneider / Werner",
            f"{M['Old Dominion'][2025]:.1f}% / {M['Saia'][2025]:.1f}% / {M['XPO'][2025]:.1f}%; "
            f"{M['Knight-Swift'][2025]:.1f}% / {M['Schneider'][2025]:.1f}% / {M['Werner'][2025]:.1f}%")
    P = R["parcels"]
    lab.row("UPS parcels a day, revenue a parcel; FedEx", f"{P['ups_adv'] / 1e3:.1f}m, ${P['ups_rpp']:.2f}; {P['fdx_adv'] / 1e3:.1f}m, ${P['fdx_yield']:.2f}")
    D = R["door"]
    lab.row("the Works' route: $ a parcel in the city / suburb / countryside", f"{D['city']:.2f} / {D['suburb']:.2f} / {D['rural']:.2f}")
    lab.row("Postal Service: pieces an address a day 2007 / 2025; net loss $bn", f"{D['ppd'][0]} / {D['ppd'][1]}; {D['usps_loss']:.1f}")
    C = R["called"]
    lab.row("Aurora: promised launch; actual; driverless miles by September 2026; aim for end-2027",
            f"late {C['plan']}; April {C['launch']}; {C['miles']:,.0f}; {C['target']:,.0f}+ trucks")
    lab.row(f"this series' call: Union Pacific completes its purchase of Norfolk Southern by {C['line']}", f"probability {100 * C['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    r = c["rate"]
    ax1.plot(range(len(r)), r, color="#E8554E", lw=1.8, label="spot rate, $ a mile")
    ax1.axhline(c["cost"], color=labs.MUTED, lw=1.0, ls="--", label="cost")
    ax1.axvspan(*c["boom"], color=labs.GOLD, alpha=0.12, label="demand boom")
    ax1.set_xlabel("month")
    ax1.set_title("The Works' trucking market")
    ax1.legend(fontsize=7)
    cv = Rl["curve"]
    ds = [d / 1e6 for d in cv]
    ax2.plot(ds, [100 * v for v in cv.values()], color=labs.GOLD, lw=1.8, label="average cost")
    ax2.axhline(100 * Rl["rate"], color=labs.BLUE, lw=1.0, ls="--", label="revenue a ton-mile")
    ax2.set_ylim(0, 25)
    ax2.set_xlabel("ton-miles a year per route mile (millions)")
    ax2.set_ylabel("cents a ton-mile")
    ax2.set_title("The Works' railway: density")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("Every freight business is about filling the trip, and the firm with the most freight in the most places fills "
                "it best: railways own their track, truckers share the road with half a million rivals, part-load and parcel "
                "networks build buildings, and at the door density decides everything.")
    _ = freight
    return lab
