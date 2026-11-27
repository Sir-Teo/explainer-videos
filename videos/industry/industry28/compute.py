"""Every number in Part 28 of *Industry, Built* ("Airlines"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry28.compute        # prints the film's numbers; writes .cache/industry28/computed.json

Items:
    hook        real airline fares since 1963; American airlines' combined profits since 2009
    run         the Run it flight: two fares, a protection level and overbooking (the Works)
    seat        a seat-mile's revenue and cost at Delta, Southwest and Spirit; load factors
    dollar      where a dollar of Delta's costs goes
    fuel        jet fuel since 1990; Delta's fuel in 2025 and 2026; fuel efficiency
    loyalty     the card money against the airline's profit
    traffic     the intermission's series: seat-miles, load factors, passengers, airline jobs
    cheap       the low-cost and ultra-low-cost carriers' margins; Spirit's two bankruptcies
    lessors     aircraft lessors against the airlines
    landscape   the companies by revenue and margin
    called      Delta's 2026 guidance, January against October; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import airline

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry28"

NAMES = {"DAL": ("Delta", "network"), "UAL": ("United", "network"), "AAL": ("American", "network"),
         "ALK": ("Alaska", "network"), "HA": ("Hawaiian", "network"), "LUV": ("Southwest", "lowcost"),
         "JBLU": ("JetBlue", "lowcost"), "ULCC": ("Frontier", "ulcc"), "SAVE": ("Spirit", "ulcc"), "ALGT": ("Allegiant", "ulcc"),
         "SKYW": ("SkyWest", "regional"), "CPA": ("Copa", "foreign"), "LTM": ("LATAM", "foreign"), "RYAAY": ("Ryanair", "foreign"),
         "AER": ("AerCap", "lessor"), "AL": ("Air Lease", "lessor"), "SABR": ("Sabre", "systems")}
US = ("DAL", "UAL", "AAL", "LUV", "JBLU", "ALK", "ULCC", "ALGT", "HA")   # Spirit's filed net income is mis-scaled in XBRL; left out
COSTS = [("salaries", "people"), ("fuel", "fuel"), ("ancillary", "ancillary businesses and refinery"),
         ("contracted", "contracted services"), ("landing", "landing fees and rents"), ("regional", "regional carriers"),
         ("selling", "selling and commissions"), ("depreciation", "depreciation"), ("maintenance", "maintenance"),
         ("service", "passenger service"), ("profitsharing", "profit sharing"), ("rent", "aircraft rent"), ("other", "other")]


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
    for r in read("sec_air"):
        if r.get("revenue") or r.get("profit") is not None:
            sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    f = _monthly(read("fred_air"))

    # the hook: real fares and the industry's profits
    fare = _annual(f["CUUR0000SETG01"], need=11)
    cpi = _annual(f["CPIAUCNS"], need=11)
    real = {y: (fare[y] / fare[2000]) / (cpi[y] / cpi[2000]) for y in fare if y in cpi and y >= 2000}
    prof = {}
    for y in range(2009, 2026):
        v = [sec[t][y]["profit"] for t in US if y in sec[t] and sec[t][y].get("profit") is not None]
        rv = [sec[t][y]["revenue"] for t in US if y in sec[t] and sec[t][y].get("revenue")]
        prof[y] = (sum(v), sum(rv))
    R["hook"] = dict(real=real, profit=prof, total=sum(p for p, _ in prof.values()),
                     total_rev=sum(r for _, r in prof.values()))

    # Run it
    fl = airline.Flight()
    lw = fl.littlewood()
    sweep = fl.sweep_protect(step=2, top=80)
    over = fl.sweep_oversell(top=24)
    best_o = max(over, key=over.get)
    R["run"] = dict(seats=fl.seats, low=fl.low, high=fl.high, leisure=fl.leisure, business=fl.business, cost=fl.cost(),
                    miles=fl.miles, casm=fl.casm, noshow=fl.noshow, bump=fl.bump, lw=lw,
                    first=fl.sell(protect=0), high_only=fl.sell(fixed=fl.high), mid=fl.sell(fixed=199.0), protect=fl.sell(protect=lw),
                    sweep=sweep, over=over, best_over=best_o, both=fl.sell(protect=lw, oversell=best_o),
                    ratio=fl.low / fl.high)

    # what-ifs for Run it: a dearer business fare
    f600 = fl.but(high=600.0)
    R["run"]["dear"] = dict(high=600.0, lw=f600.littlewood(), res=f600.sell(protect=f600.littlewood()))

    # 2020
    pan = {NAMES[t][0]: dict(rev19=sec[t][2019]["revenue"], rev20=sec[t][2020]["revenue"], op20=sec[t][2020]["operating_income"],
                             ni20=sec[t][2020]["profit"]) for t in ("DAL", "UAL", "AAL", "LUV")}
    R["pandemic"] = dict(firms=pan, lf20=_annual(f["LOADFACTOR"])[2020], lf19=_annual(f["LOADFACTOR"])[2019], psp=get("cares.psp"),
                         enplane={y: v * 12 / 1e3 for y, v in _annual(f["ENPLANE"]).items()},
                         lf_m={m: v for m, v in f["LOADFACTOR"].items() if "2019-07" <= m <= "2021-12"})

    # a seat-mile
    R["seat"] = dict(dal=(get("dl28.trasm"), get("dl28.casm"), get("dl28.lf")), luv=(get("sw28.rasm"), get("sw28.casm"), get("sw28.lf")),
                     save=(get("spirit.trasm"), get("spirit.casm"), get("spirit.lf")), dal_asm=get("dl28.asm"), dal_rpm=get("dl28.rpm"),
                     dal_yield=get("dl28.yield"), dal_casmex=get("dl28.casmex"), luv_fare=get("sw28.fare"), luv_stage=get("sw28.stage"),
                     luv_planes=get("sw28.planes"), luv_pax=get("sw28.pax"), dal_prasm=get("dl28.prasm"),
                     luv_trips=get("sw28.trips"), luv_seats=get("sw28.seatspertrip"))

    # Delta's dollar
    total = get("dl28.cost.total")
    rev = sec["DAL"][2025]["revenue"]
    R["dollar"] = dict(items=[(name, get(f"dl28.cost.{k}") / 1e3) for k, name in COSTS], total=total / 1e3, revenue=rev,
                       profit=sec["DAL"][2025]["profit"], emp=get("dl28.emp"))

    # fuel
    jet = f["MJFUELUSGULF"]
    fa = f["CUUR0000SETG01"]
    jy = _annual(jet, need=8)
    R["fuel"] = dict(monthly={_ym(m): v for m, v in jet.items() if m >= "2000-01"}, annual=jy, last=max(jet), last_v=jet[max(jet)],
                     m26={m: v for m, v in jet.items() if m >= "2025-07"},
                     fares26={m: 100 * (v / fa[f"{int(m[:4]) - 1}{m[4:]}"] - 1) for m, v in fa.items()
                              if m >= "2026-01" and f"{int(m[:4]) - 1}{m[4:]}" in fa},
                     dal25=get("dl28.fuel"), dal24=2.57, q2=get("dl28.fuel.q2"), q3=get("dl28.fuel.q3"), q4=get("dl28.fuel.q4"),
                     hit=get("dl28.fuelhit"), gallons=get("dl28.gal"), mpg=(get("sw28.mpg.2022"), get("sw28.mpg")),
                     share=get("dl28.cost.fuel") / get("dl28.cost.total"))

    # loyalty
    R["loyalty"] = dict(amex=get("dl28.amex"), dal_profit=sec["DAL"][2025]["profit"], aal=get("aal.cobrand25"),
                        aal_profit=sec["AAL"][2025]["profit"], q3=get("dl28.loyalty.q3"),
                        skymiles=get("dl28.skymiles"))

    # traffic
    R["traffic"] = dict(lf={_ym(m): v for m, v in f["LOADFACTOR"].items()}, asm=_annual(f["ASM"]), rpm=_annual(f["RPM"]),
                        asm_m={_ym(m): v / 1e6 for m, v in f["ASM"].items()}, rpm_m={_ym(m): v / 1e6 for m, v in f["RPM"].items()},
                        enplane={y: v * 12 / 1e3 for y, v in _annual(f["ENPLANE"]).items()},
                        jobs={_ym(m): v for m, v in f["CES4348100001"].items() if m >= "2000-01"},
                        lf_annual=_annual(f["LOADFACTOR"]))

    # the cheap carriers
    marg = {NAMES[t][0]: {y: sec[t][y]["operating_income"] / sec[t][y]["revenue"] for y in range(2019, 2026)
                          if y in sec[t] and sec[t][y].get("revenue") and sec[t][y].get("operating_income") is not None}
            for t in ("DAL", "UAL", "LUV", "JBLU", "ULCC", "SAVE", "ALGT")}
    R["cheap"] = dict(margins=marg, planes=(get("spirit.planes.2024"), get("spirit.planes")), luv_lf=(get("sw28.lf.2024"), get("sw28.lf")),
                      luv_fare=(get("sw28.fare.2024"), get("sw28.fare")), luv_pax=(get("sw28.pax.2024"), get("sw28.pax")),
                      luv_q4=get("sw28.q4"))

    # lessors
    def med(t):
        ys = [y for y in sec[t] if y >= 2021 and sec[t][y].get("revenue") and sec[t][y].get("profit") is not None]
        return float(np.median([sec[t][y]["profit"] / sec[t][y]["revenue"] for y in ys]))
    R["lessors"] = dict(aer=med("AER"), al=med("AL"), dal=med("DAL"), ual=med("UAL"), luv=med("LUV"),
                        aer_rev=sec["AER"][2025]["revenue"], al_rev=sec["AL"][2025]["revenue"],
                        aer_ni=sec["AER"][2025]["profit"], dal_ni=sec["DAL"][2025]["profit"], dal_rev=sec["DAL"][2025]["revenue"])

    # landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        if not sec[tk] or tk in ("SAVE", "HA"):     # Spirit's net income is mis-scaled; Hawaiian is part of Alaska since 2024
            continue
        ys = [y for y in sec[tk] if sec[tk][y].get("revenue")]
        if not ys:
            continue
        y = max(ys)
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in ys if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=sec[tk][y]["revenue"], margin=float(np.median(mm)), fy=y, tk=tk,
                         cur=sec[tk][y].get("currency", "USD")))
    usr = [(NAMES[t][0], sec[t][2025]["revenue"]) for t in ("DAL", "UAL", "AAL", "LUV", "ALK", "JBLU", "ULCC", "ALGT")]
    R["landscape"] = dict(companies=comp, us_rev=usr, top4=sum(v for _, v in usr[:4]) / sum(v for _, v in usr))

    j26 = [v for m, v in jet.items() if m.startswith("2026")]
    R["called"] = dict(jan=(get("dl28.g.jan.lo"), get("dl28.g.jan.hi")), oct=(get("dl28.g.oct.lo"), get("dl28.g.oct.hi")),
                       pretax=get("dl28.pretax26"), hit=get("dl28.fuelhit"), line=3.00, prob=0.4,
                       jet25=jy.get(2025), jet26=float(np.mean(j26)), jet26_n=len(j26))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("real fares", {y: round(v, 2) for y, v in H["real"].items() if y in (2000, 2010, 2019, 2022, 2025)})
    print("profits", {y: round(p, 2) for y, (p, r) in H["profit"].items()}, round(H["total"], 1), round(H["total_rev"], 1))
    U = R["run"]
    for k in ("first", "high_only", "mid", "protect", "both"):
        print(k, {a: round(b, 2) for a, b in U[k].items()})
    print("lw", U["lw"], "best over", U["best_over"], "cost", U["cost"])
    print("seat", R["seat"])
    print("dollar", R["dollar"]["items"], R["dollar"]["total"], R["dollar"]["revenue"], R["dollar"]["profit"])
    F = R["fuel"]
    print("fuel", {y: round(v, 2) for y, v in F["annual"].items() if y >= 2005}, F["last"], F["last_v"], round(F["share"], 3))
    print("loyalty", R["loyalty"])
    T = R["traffic"]
    print("traffic", {y: round(v, 1) for y, v in T["lf_annual"].items()}, {y: round(v) for y, v in T["enplane"].items() if y in (2000, 2019, 2020, 2025)})
    print("cheap", {k: {y: round(100 * x, 1) for y, x in v.items()} for k, v in R["cheap"]["margins"].items()})
    print("lessors", {k: round(v, 3) for k, v in R["lessors"].items()})
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"], c["cur"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))
    print("called", R["called"])


if __name__ == "__main__":
    main()
