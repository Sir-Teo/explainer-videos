"""Every number in Part 29 of *Industry, Built* ("Rail, Trucks and Parcels"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry29.compute        # prints the film's numbers; writes .cache/industry29/computed.json

Items:
    hook        the Staggers Act's finding; the railways' operating ratios since 2009 against the truckers'; half a million carriers
    run         the Run it lane: a truck to Atlanta and the trip home (the Works)
    unit        what a mile, a hundredweight and a package earn: intermodal, truckload, LTL, parcels
    rail        a railway's cost per ton-mile by density (the Works, calibrated to Union Pacific); the four railways
    trucks      the census of carriers by size; truckload margins; truckload prices; the Works' capacity cycle
    ltl         Old Dominion against Yellow; LTL against truckload margins
    traffic     the intermission's series: carloads, intermodal, truck tonnage, freight jobs, e-commerce
    parcels     UPS and FedEx: volume, revenue per package, margins; Amazon; hubs
    door        the cost of a stop (the Works); the Postal Service
    landscape   the companies by revenue and margin
    called      Aurora's driverless forecasts; the Staggers Act; this series' call on Union Pacific and Norfolk Southern
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import freight

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry29"

NAMES = {"UNP": ("Union Pacific", "rail"), "BNSF": ("BNSF", "rail"), "CSX": ("CSX", "rail"), "NSC": ("Norfolk Southern", "rail"),
         "CP": ("CPKC", "rail"), "UPS": ("UPS", "parcel"), "FDX": ("FedEx", "parcel"), "ZTO": ("ZTO Express", "parcel"),
         "JBHT": ("J.B. Hunt", "intermodal"), "HUBG": ("Hub Group", "intermodal"), "KNX": ("Knight-Swift", "truckload"),
         "SNDR": ("Schneider", "truckload"), "WERN": ("Werner", "truckload"), "HTLD": ("Heartland", "truckload"),
         "MRTN": ("Marten", "truckload"), "ODFL": ("Old Dominion", "ltl"), "SAIA": ("Saia", "ltl"), "XPO": ("XPO", "ltl"),
         "ARCB": ("ArcBest", "ltl"), "TFII": ("TFI International", "ltl"), "RXO": ("RXO", "broker"), "LSTR": ("Landstar", "broker"),
         "GXO": ("GXO", "logistics"), "YELL": ("Yellow", "ltl"), "AUR": ("Aurora", "driverless")}
RAIL = ("UNP", "BNSF", "CSX", "NSC")
TL = ("KNX", "SNDR", "WERN", "HTLD")
LTL = ("ODFL", "SAIA", "XPO")


def _monthly(rows: list) -> dict:
    by: dict = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        by[r["series"]][str(r["month"])].append(r["value"])
    return {s: {m: float(np.mean(v)) for m, v in d.items()} for s, d in by.items()}


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


def _ym(p: str) -> float:
    return int(p[:4]) + (int(p[5:7]) - 0.5) / 12


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_freight"):
        if r.get("revenue"):
            y = int(str(r["year_end"])[:4])
            if str(r["year_end"])[5:7] in ("01", "02"):      # none here, kept for fiscal years ending early in a year
                y -= 1
            sec[r["ticker"]][y] = r
    f = _monthly(read("fred_freight"))

    def opr(t, y):
        r = sec[t].get(y)
        return 100 * (1 - r["operating_income"] / r["revenue"]) if r and r.get("operating_income") is not None else None

    # the hook
    ors = {NAMES[t][0]: {y: opr(t, y) for y in range(2009, 2026) if opr(t, y) is not None} for t in RAIL + ("KNX", "WERN")}
    R["hook"] = dict(ors=ors, unp=get("up29.or"), knx=get("kx29.or"), carriers=get("fm29.total"), one=get("fm29.one"))

    # Run it: the lane
    diesel = _annual(f["GASDESW"], need=12)
    truck = freight.Truck(nonfuel=get("wk29.nonfuel"), mpg=get("wk29.mpg"), diesel=diesel[2025])
    lane = freight.Lane(head=get("jb29.tl.rpl") / get("jb29.tl.haul"), back=get("wk29.back"), p_back=get("wk29.pback"),
                        wait_days=get("wk29.wait"), day_cost=get("wk29.day"), truck=truck)
    one_way = lane.miles * truck.per_mile()
    shares = [0.5, 0.4, 0.3, 0.2, get("kx29.empty") / 100, 0.1]
    d26 = [v for m, v in f["GASDESW"].items() if m.startswith("2026")]
    R["run"] = dict(diesel=diesel[2025], diesel26=float(np.mean(d26)), diesel26_n=len(d26), nonfuel=truck.nonfuel, fuel_mile=truck.diesel / truck.mpg, per_mile=truck.per_mile(),
                    miles=lane.miles, head=lane.head, out_rev=lane.head * lane.miles, one_way=one_way,
                    empty=lane.trip(False), back=lane.trip(True), be_empty=lane.breakeven_head(False),
                    be_back=lane.breakeven_head(True), needed={s: lane.needed(s) for s in shares},
                    knx_empty=get("kx29.empty"), back_rate=lane.back, p_back=lane.p_back, wait=lane.wait_days,
                    day_cost=lane.day_cost, back_cost=lane.miles * truck.per_mile(),
                    knx_rev_mile=get("kx29.rev") * 1e6 / (get("kx29.tractors") * get("kx29.miles")))

    # the unit
    R["unit"] = dict(int_mile=get("jb29.int.rpl") / get("jb29.int.haul"), tl_mile=get("jb29.tl.rpl") / get("jb29.tl.haul"),
                     int_rpl=get("jb29.int.rpl"), int_haul=get("jb29.int.haul"), tl_rpl=get("jb29.tl.rpl"), tl_haul=get("jb29.tl.haul"),
                     ltl_cwt=get("od29.cwt"), ltl_wps=get("od29.wps"), ltl_rps=get("od29.rps"), ltl_haul=get("od29.haul"),
                     ups=get("ups29.us.rpp"), fdx=get("fdx29.ground"), usps=get("usps29.pkgrev") / get("usps29.pkgvol"),
                     rail_tm=100 * get("up29.freightrev") / get("up29.rtm"))

    # the railway
    rw = freight.Railway(opex=get("up29.or") / 100 * sec["UNP"][2025]["revenue"] * 1e9, route=get("up29.route"),
                         rtm=get("up29.rtm") * 1e9, rate=get("up29.freightrev") / get("up29.rtm"), fixed=get("wk29.fixed"))
    dens = list(np.round(np.geomspace(0.5e6, 30e6, 60), -3))
    R["rail"] = dict(F=rw.F(), v=rw.v(), density=rw.density(), rate=rw.rate, avg=rw.avg_cost(rw.density()),
                     be=rw.breakeven_density(), curve={d: float(rw.avg_cost(d)) for d in dens}, at1=float(rw.avg_cost(1e6)),
                     route=get("up29.route"), rtm=get("up29.rtm"), emp=get("up29.emp"),
                     ors={NAMES[t][0]: ors[NAMES[t][0]] for t in RAIL},
                     ppi_rail={_ym(m): v for m, v in f["PCU482111482111"].items() if m >= "1980-01"},
                     cpi={_ym(m): v for m, v in f["CPIAUCNS"].items() if m >= "1980-01"})
    pr, cp = _annual(f["PCU482111482111"]), _annual(f["CPIAUCNS"], need=11)
    R["rail"]["real"] = {y: (pr[y] / pr[1981]) / (cp[y] / cp[1981]) for y in pr if y in cp and y >= 1981}

    # trucks
    sizes = [("1", get("fm29.one")), ("2-5", get("fm29.k2_5")), ("6-10", get("fm29.k6_10")), ("11-100", get("fm29.k11_100")),
             ("101-1,000", get("fm29.k101_1000")), ("over 1,000", get("fm29.k1000"))]
    mk = freight.Market()
    mp = mk.path()
    tlm = {NAMES[t][0]: {y: 100 * sec[t][y]["operating_income"] / sec[t][y]["revenue"] for y in range(2015, 2026)
                         if y in sec[t] and sec[t][y].get("operating_income") is not None} for t in TL + LTL}
    R["trucks"] = dict(sizes=sizes, total=get("fm29.total"), zero=get("fm29.zero"),
                       ppi_tl={_ym(m): v for m, v in f["PCU484121484121"].items()},
                       ppi_tl_a=_annual(f["PCU484121484121"]),
                       jobs={_ym(m): v for m, v in f["CES4348400001"].items()}, margins=tlm,
                       cycle=dict(rate=list(mp["rate"]), capacity=list(mp["capacity"]), demand=list(mp["demand"]), cost=mk.cost,
                                  boom=(mk.boom_start, mk.boom_start + mk.boom_len), entry=mk.entry,
                                  below=int((mp["rate"][int(np.argmax(mp["rate"])):] < mk.cost).sum())),
                       knx=dict(revpt=get("kx29.revpt"), miles=get("kx29.miles"), empty=get("kx29.empty"), op=get("kx29.or"),
                                tractors=get("kx29.tractors")), jb_carriers=get("jb29.carriers"))
    a = R["trucks"]["ppi_tl_a"]
    R["trucks"]["ppi_peak"] = max((y for y in a if 2019 <= y <= 2025), key=a.get)

    # LTL
    R["ltl"] = dict(odfl_or=get("od29.or"), sc=get("od29.sc"), spd=get("od29.spd"), yell_emp=get("yell29.emp"),
                    yell={y: opr("YELL", y) for y in range(2013, 2023) if opr("YELL", y) is not None},
                    odfl={y: opr("ODFL", y) for y in range(2013, 2026) if opr("ODFL", y) is not None},
                    ppi_ltl={_ym(m): v for m, v in f["PCU484122484122"].items()},
                    ppi_tl={_ym(m): v for m, v in f["PCU484121484121"].items()})

    # traffic
    def yoy(s, base, last):
        return {y: v for y, v in _annual(f[s]).items() if base <= y <= last}
    R["traffic"] = dict(carloads={_ym(m): v / 1e3 for m, v in f["RAILFRTCARLOADSD11"].items()},
                        intermodal={_ym(m): v / 1e3 for m, v in f["RAILFRTINTERMODALD11"].items()},
                        tonnage={_ym(m): v for m, v in f["TRUCKD11"].items()},
                        jobs={k: {_ym(m): v for m, v in f[s].items() if m >= "2000-01"} for k, s in
                              (("truck", "CES4348400001"), ("rail", "CES4348200001"), ("couriers", "CES4349200001"))},
                        ecom={int(m[:4]) + (int(m[5:7]) - 1) / 12: v / 1e3 for m, v in f["ECOMSA"].items()},
                        car_a=yoy("RAILFRTCARLOADSD11", 2000, 2025), int_a=yoy("RAILFRTINTERMODALD11", 2000, 2025))

    # parcels
    pm = {NAMES[t][0]: {y: 100 * sec[t][y]["operating_income"] / sec[t][y]["revenue"] for y in range(2015, 2027)
                        if y in sec[t] and sec[t][y].get("operating_income") is not None} for t in ("UPS", "FDX")}
    R["parcels"] = dict(ups_adv=get("ups29.adv"), ups_rpp=get("ups29.rpp"), ups_us_adv=get("ups29.us.adv"),
                        ups_us_rpp=get("ups29.us.rpp"), fdx_adv=get("fdx29.adv"), fdx_yield=get("fdx29.yield"),
                        fdx_ground=get("fdx29.ground"), amazon=get("ups29.amazon"), buildings=get("ups29.buildings"),
                        positions=get("ups29.positions"), hourly=get("ups29.hourly"), margins=pm,
                        ups_rev={y: sec["UPS"][y]["revenue"] for y in range(2015, 2026) if y in sec["UPS"]},
                        fdx_rev={y: sec["FDX"][y]["revenue"] for y in range(2015, 2027) if y in sec["FDX"]},
                        lanes={n: freight.lanes(n) for n in (5, 10, 20, 40)},
                        ups_day_rev=get("ups29.us.adv") * 1e3 * get("ups29.us.rpp"))

    # the door
    ro = freight.Route(hour=get("wk29.hour"), dwell=get("wk29.dwell"), speed=get("wk29.speed"), pps=get("wk29.pps"))
    sp = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
    R["door"] = dict(hour=ro.hour, hours=ro.hours, dwell=ro.dwell, speed=ro.speed, pps=ro.pps,
                     curve={s: float(ro.per_package(s)) for s in sp}, stops={s: float(ro.stops(s)) for s in sp},
                     city=float(ro.per_package(0.05)), suburb=float(ro.per_package(0.3)), rural=float(ro.per_package(2.0)),
                     usps_rev=get("usps29.rev"), usps_loss=get("usps29.loss"), usps_pkgrev=get("usps29.pkgrev"),
                     usps_pkgvol=get("usps29.pkgvol"), usps_fcm=get("usps29.fcm"), ppd=(get("usps29.ppd07"), get("usps29.ppd")),
                     dp=get("usps29.dp"), career=get("usps29.career"))

    # landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        if tk in ("YELL", "AUR") or not sec[tk]:
            continue
        ys = sorted(sec[tk])
        y = ys[-1]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in ys if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=sec[tk][y]["revenue"], margin=float(np.median(mm)), fy=y, tk=tk,
                         cur=sec[tk][y].get("currency", "USD")))
    R["landscape"] = dict(companies=comp)

    # called
    R["called"] = dict(plan=get("aur29.plan"), launch=get("aur29.launch"), miles=get("aur29.miles"), target=get("aur29.target"),
                       price=get("up29.merger"), line="2027-12-31", prob=0.4, aur_rev=sec["AUR"][2025]["revenue"],
                       aur_loss=sec["AUR"][2025]["operating_income"])
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("ORs", {k: {y: round(v, 1) for y, v in d.items() if y in (2009, 2015, 2019, 2023, 2025)} for k, d in H["ors"].items()})
    U = R["run"]
    print("run", {k: (round(v, 2) if isinstance(v, float) else v) for k, v in U.items() if not isinstance(v, dict)})
    print("run trips", {k: round(v, 2) for k, v in U["empty"].items()}, {k: round(v, 2) for k, v in U["back"].items()})
    print("needed", {k: round(v, 2) for k, v in U["needed"].items()})
    print("unit", {k: round(v, 2) for k, v in R["unit"].items()})
    Rl = R["rail"]
    print("rail", round(Rl["F"]), round(100 * Rl["v"], 2), round(Rl["density"] / 1e6, 2), round(100 * Rl["avg"], 2),
          round(100 * Rl["rate"], 2), round(Rl["be"] / 1e6, 2), round(100 * Rl["at1"], 2))
    print("real rail rates", {y: round(v, 2) for y, v in Rl["real"].items() if y in (1981, 1990, 2000, 2004, 2010, 2020, 2025)})
    T = R["trucks"]
    print("sizes", T["sizes"], "ppi tl", {y: round(v, 1) for y, v in T["ppi_tl_a"].items() if y >= 2018}, T["ppi_peak"])
    print("tl margins", {k: {y: round(v, 1) for y, v in d.items() if y >= 2019} for k, d in T["margins"].items()})
    c = T["cycle"]
    print("cycle", round(max(c["rate"]), 2), int(np.argmax(c["rate"])), round(min(c["rate"]), 2), int(np.argmin(c["rate"])), c["below"])
    L = R["ltl"]
    print("ltl", {y: round(v, 1) for y, v in L["odfl"].items()}, {y: round(v, 1) for y, v in L["yell"].items()})
    Tr = R["traffic"]
    print("traffic", {y: round(v) for y, v in Tr["car_a"].items() if y in (2000, 2006, 2019, 2025)},
          {y: round(v) for y, v in Tr["int_a"].items() if y in (2000, 2006, 2019, 2025)})
    P = R["parcels"]
    print("parcels", {k: {y: round(v, 1) for y, v in d.items()} for k, d in P["margins"].items()}, P["lanes"])
    print("ups rev", {y: round(v, 1) for y, v in P["ups_rev"].items()}, "fdx rev", {y: round(v, 1) for y, v in P["fdx_rev"].items()})
    D = R["door"]
    print("door", round(D["city"], 2), round(D["suburb"], 2), round(D["rural"], 2), {s: round(v) for s, v in D["stops"].items()})
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"], c["cur"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))
    print("called", R["called"])


if __name__ == "__main__":
    main()
