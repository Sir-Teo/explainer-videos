"""Every number in Part 30 of *Industry, Built* ("Telecoms"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry30.compute        # prints the film's numbers; writes .cache/industry30/computed.json

Items:
    hook        the carriers' revenue against the companies whose services run over them; phone prices after inflation
    run         the Run it spectrum auction: bid for every block you value, or for fewer (the Works)
    sub         a subscriber: what she pays, how long she stays, what she is worth (the Works)
    net         the network and what it costs to build: capital spending against revenue
    spectrum    the C-band auction; EchoStar's sales to AT&T and SpaceX
    towers      American Tower's sites and margins; a tower's return by tenants (the Works)
    traffic     the intermission's series: phone prices, telecom jobs, revenue stacks
    three       three national networks: T-Mobile's rise, churn and ARPA side by side
    home        broadband at home: cable's losses, fibre and fixed wireless
    landscape   the companies by revenue and margin
    called      DISH's promise of a fourth network; this series' call on cable broadband
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import telco

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry30"

NAMES = {"VZ": ("Verizon", "wireless"), "T": ("AT&T", "wireless"), "TMUS": ("T-Mobile", "wireless"), "CMCSA": ("Comcast", "cable"),
         "CHTR": ("Charter", "cable"), "CABO": ("Cable One", "cable"), "LUMN": ("Lumen", "wireline"), "FYBR": ("Frontier", "wireline"),
         "TDS": ("TDS", "wireline"), "SATS": ("EchoStar", "satellite"), "AMT": ("American Tower", "towers"),
         "CCI": ("Crown Castle", "towers"), "SBAC": ("SBA", "towers"), "VOD": ("Vodafone", "foreign"), "TEF": ("Telefónica", "foreign"),
         "AMX": ("América Móvil", "foreign"), "CHT": ("Chunghwa", "foreign"), "SKM": ("SK Telecom", "foreign"), "KT": ("KT", "foreign"),
         "TU": ("Telus", "foreign"), "BCE": ("BCE", "foreign"), "RCI": ("Rogers", "foreign"), "TIGO": ("Millicom", "foreign"),
         "LBTYA": ("Liberty Global", "foreign"), "ERIC": ("Ericsson", "equipment"), "NOK": ("Nokia", "equipment"),
         "IRDM": ("Iridium", "satellite"), "VSAT": ("Viasat", "satellite"), "GOOGL": ("Alphabet", "over"), "META": ("Meta", "over"),
         "NFLX": ("Netflix", "over")}


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
    for r in read("sec_tel"):
        if r.get("revenue"):
            sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    f = _monthly(read("fred_tel"))

    def rev(t, y):
        return sec[t][y]["revenue"] if y in sec[t] else None

    # the hook
    carriers = {y: sum(rev(t, y) for t in ("VZ", "T")) for y in range(2015, 2026)}
    over = {y: sum(rev(t, y) for t in ("GOOGL", "META", "NFLX")) for y in range(2015, 2026)}
    tel = _annual(f["CUUR0000SEED"], need=11)
    cpi = _annual(f["CPIAUCNS"], need=11)
    real = {y: (tel[y] / tel[1998]) / (cpi[y] / cpi[1998]) for y in tel if y in cpi and y >= 1998}
    carriers3 = {y: sum(rev(t, y) for t in ("VZ", "T", "TMUS")) for y in range(2015, 2026)}
    marg = {NAMES[t][0]: 100 * sec[t][2025]["operating_income"] / rev(t, 2025) for t in ("META", "GOOGL", "NFLX", "VZ", "TMUS", "T")}
    R["hook"] = dict(margins=marg, carriers=carriers, carriers3=carriers3, over=over, real=real, nominal={y: tel[y] / tel[1998] for y in tel if y >= 1998})

    # Run it: the auction
    A = telco.Auction()
    runs = {k: A.run(cap=k) for k in (1, 2, 3, 4)}
    def demand(p):
        return [sum(1 for v in vals if v >= p - 1e-12) for vals in A.values]
    R["run"] = dict(values=[list(v) for v in A.values], names=list(A.names), supply=A.supply, runs=runs,
                    clock={p: demand(p) for p in (3.0, 4.0, 5.0, 6.0, 6.5, 6.75)})

    # the subscriber
    S = telco.Subscriber(arpa=get("vz30.arpa"), churn=get("vz30.churn") / 100, margin=get("wk30.margin"), cac=get("wk30.cac"))
    churns = [0.006, 0.008, get("vz30.churn") / 100, 0.012, 0.015, 0.02, 0.03]
    R["sub"] = dict(arpa=S.arpa, churn=S.churn, months=S.months(), life=S.lifetime(), margin=S.margin, cac=S.cac,
                    by_churn={c: S.but(churn=c).lifetime() for c in churns}, cpa=get("vz30.cpa"),
                    tm_arpa=get("tm30.arpa"), tm_churn=get("tm30.churn"), att_churn=get("att30.churn"),
                    accounts=get("vz30.accounts"))

    # the network: capital spending
    capex = {}
    for t in ("VZ", "T", "TMUS", "CHTR", "CMCSA", "GOOGL", "META"):
        c = sec[t][2025].get("capex") if 2025 in sec[t] else None
        if t == "VZ":
            c = get("vz30.capex")
        capex[NAMES[t][0]] = (c, rev(t, 2025))
    R["net"] = dict(capex=capex, three=sum(capex[k][0] for k in ("Verizon", "AT&T", "T-Mobile")), vz_rev=rev("VZ", 2025),
                    nflx=(sec["NFLX"][2025].get("capex"), rev("NFLX", 2025)), asts=(sec["ASTS"][2025].get("capex"), rev("ASTS", 2025)),
                    irdm=rev("IRDM", 2025))

    # spectrum
    R["spectrum"] = dict(vz=get("vz30.cband"), att=get("att30.cband"), att_echo=get("att30.echostar"), spacex=get("ech30.spacex"),
                         sats_op=sec["SATS"][2025]["operating_income"], sats_rev=rev("SATS", 2025))

    # towers
    Tw = telco.Tower(build=get("wk30.tower"), opex=1e6 * get("amt30.us.opex") / get("amt30.us.sites"), rent=get("wk30.rent"))
    amt_m = {y: 100 * sec["AMT"][y]["operating_income"] / rev("AMT", y) for y in range(2015, 2026) if y in sec["AMT"]}
    R["towers"] = dict(sites=get("amt30.sites"), us_sites=get("amt30.us.sites"), us_rev=get("amt30.us.rev"), us_opex=get("amt30.us.opex"),
                       us_profit=get("amt30.us.profit"), per_site=1e6 * get("amt30.us.rev") / get("amt30.us.sites"),
                       opex_site=Tw.opex, churn=get("amt30.churn"), rent=Tw.rent, build=Tw.build,
                       by_tenants={n: dict(cash=Tw.cash(n), yld=Tw.yield_(n), margin=Tw.margin(n)) for n in (1, 2, 3, 4)},
                       implied=1e6 * get("amt30.us.rev") / get("amt30.us.sites") / Tw.rent, amt_margin=amt_m,
                       vz_margin={y: 100 * sec["VZ"][y]["operating_income"] / rev("VZ", y) for y in range(2015, 2026)})

    # traffic
    R["traffic"] = dict(tel={_ym(m): v for m, v in f["CUUR0000SEED"].items()},
                        cpi={_ym(m): v / f["CPIAUCNS"]["1997-12"] * 100 for m, v in f["CPIAUCNS"].items() if m >= "1997-12"},
                        jobs={_ym(m): v for m, v in f["CES5051700001"].items()},
                        rev={NAMES[t][0]: {y: rev(t, y) for y in range(2015, 2026) if rev(t, y)} for t in ("VZ", "T", "TMUS", "CMCSA", "CHTR")},
                        lumen={y: rev("LUMN", y) for y in (2015, 2019, 2022, 2025)})
    J = R["traffic"]["jobs"]
    R["traffic"]["jobs_peak"] = max(J, key=J.get)

    # three networks
    R["three"] = dict(tm_rev={y: rev("TMUS", y) for y in range(2015, 2026)}, customers=get("tm30.customers"),
                      table=[("Verizon", get("vz30.churn"), get("vz30.arpa")), ("AT&T", get("att30.churn"), None),
                             ("T-Mobile", get("tm30.churn"), get("tm30.arpa"))],
                      margins={NAMES[t][0]: {y: 100 * sec[t][y]["operating_income"] / rev(t, y) for y in range(2015, 2026)
                                             if y in sec[t] and sec[t][y].get("operating_income") is not None} for t in ("VZ", "T", "TMUS")})

    # broadband at home
    R["home"] = dict(comcast=get("cm30.broadband"), charter=get("ch30.internet"), charter_mobile=get("ch30.mobile"),
                     vz_fwa=get("vz30.fwa"), att_fiber=get("att30.fiber"), att_aia=get("att30.aia"), vz_fios=get("vz30.fios"),
                     changes=[("Comcast broadband", -711), ("Charter internet", 29680 - 30083), ("Verizon fixed wireless", 693),
                              ("AT&T Internet Air", 875), ("Charter mobile lines", 11766 - 9858)])

    # what runs over: the equipment makers
    R["over"] = dict(rev25={NAMES[t][0]: rev(t, 2025) for t in ("GOOGL", "META", "VZ", "T", "TMUS", "NFLX")}, equip={t: {y: rev(t, y) for y in range(2015, 2026) if rev(t, y)} for t in ("ERIC", "NOK")})

    # landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        if tk in ("GOOGL", "META", "NFLX", "KT", "SKM", "AMX", "CHT", "ERIC", "LBTYA") or not sec[tk]:
            continue
        ys = sorted(sec[tk])
        y = ys[-1]
        if y < 2024:
            continue
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in ys if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=sec[tk][y]["revenue"], margin=float(np.median(mm)), fy=y, tk=tk,
                         cur=sec[tk][y].get("currency", "USD")))
    R["landscape"] = dict(companies=comp, vod={y: rev("VOD", y) for y in (2016, 2019, 2022, 2025)})

    R["called"] = dict(promise=get("dish30.promise"), cm=get("cm30.broadband"), prob=0.8, cm24=411, cm25=711)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("carriers", {y: round(v, 1) for y, v in H["carriers"].items()}, "over", {y: round(v, 1) for y, v in H["over"].items()})
    print("real phone prices", {y: round(v, 2) for y, v in H["real"].items() if y in (1998, 2005, 2010, 2015, 2020, 2025)},
          "nominal", {y: round(v, 2) for y, v in H["nominal"].items() if y in (2010, 2025)})
    for k, r in R["run"]["runs"].items():
        print("auction cap", k, r["price"], r["won"], [round(x, 2) for x in r["surplus"]], r["revenue"], r["unsold"])
    S = R["sub"]
    print("sub", round(S["months"], 1), round(S["life"]), {c: round(v) for c, v in S["by_churn"].items()})
    print("capex", {k: (round(v[0], 1), round(v[1], 1), round(100 * v[0] / v[1], 1)) for k, v in R["net"]["capex"].items()}, round(R["net"]["three"], 1))
    print("spectrum", R["spectrum"])
    T = R["towers"]
    print("towers", round(T["per_site"]), round(T["opex_site"]), round(T["implied"], 2), {n: (round(v["yld"], 3), round(v["margin"], 3)) for n, v in T["by_tenants"].items()})
    print("amt margins", {y: round(v, 1) for y, v in T["amt_margin"].items()})
    print("jobs peak", R["traffic"]["jobs_peak"], R["traffic"]["jobs"][R["traffic"]["jobs_peak"]], R["traffic"]["jobs"][max(R["traffic"]["jobs"])])
    print("three", {k: {y: round(v, 1) for y, v in d.items()} for k, d in R["three"]["margins"].items()})
    print("tmus rev", {y: round(v, 1) for y, v in R["three"]["tm_rev"].items()})
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"], c["cur"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
