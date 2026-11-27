"""Every number in Part 26 of *Industry, Built* ("Property"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry26.compute        # prints the film's numbers; writes .cache/industry26/computed.json

Items:
    hook        the Federal Reserve's commercial property price index since 1990; the two falls
    run         the Run it pair: an office and a warehouse bought in 2019, refinanced in 2026 (the Works)
    bond        value as income over a rate; Realty Income's buying yield against the 10-year Treasury since 2015
    lease       the net lease, the tower lease and WeWork's mismatch
    debt        a dollar of Prologis's rent; banks' commercial property loans and delinquencies
    sectors     occupancy and margins by kind of building
    office      BXP's occupancy since 2017; the weakest offices; the model of remote work's effect
    retail      e-commerce's share; Simon's malls; Prologis's warehouses and rents
    owners      Blackstone, the REIT rule, the services firms
    extra       the intermission's series: rents of commercial buildings, construction of offices and shops, bank loans
    landscape   the companies by revenue and margin
    called      WeWork's opportunity; BXP's occupancy; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import building

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry26"

NAMES = {"PLD": ("Prologis", "industrial"), "REXR": ("Rexford", "industrial"), "EGP": ("EastGroup", "industrial"),
         "AMT": ("American Tower", "towers"), "CCI": ("Crown Castle", "towers"), "SBAC": ("SBA", "towers"),
         "EQIX": ("Equinix", "data"), "DLR": ("Digital Realty", "data"), "SPG": ("Simon", "retail"),
         "O": ("Realty Income", "retail"), "KIM": ("Kimco", "retail"), "REG": ("Regency", "retail"),
         "MAC": ("Macerich", "retail"), "FRT": ("Federal Realty", "retail"), "BXP": ("BXP", "office"),
         "VNO": ("Vornado", "office"), "SLG": ("SL Green", "office"), "KRC": ("Kilroy", "office"),
         "HPP": ("Hudson Pacific", "office"), "DEI": ("Douglas Emmett", "office"), "ARE": ("Alexandria", "office"),
         "AVB": ("AvalonBay", "homes"), "EQR": ("Equity Residential", "homes"), "MAA": ("MAA", "homes"),
         "PSA": ("Public Storage", "storage"), "EXR": ("Extra Space", "storage"), "WELL": ("Welltower", "health"),
         "VTR": ("Ventas", "health"), "BX": ("Blackstone", "manager"), "CBRE": ("CBRE", "services"),
         "JLL": ("JLL", "services"), "CWK": ("Cushman & Wakefield", "services"), "STWD": ("Starwood Property", "lender")}

SECTORS = [("warehouses", "PLD", "pld.occ"), ("malls", "SPG", "spg.occ"), ("net-leased shops", "O", "o.occ"),
           ("offices", "BXP", "bxp.occ"), ("flats", "AVB", None), ("self-storage", "PSA", None),
           ("phone towers", "AMT", None), ("data centres", "EQIX", None), ("senior housing", "WELL", None)]


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


def _q(m: str) -> float:
    """A quarter's first month as a fractional year at the quarter's middle: 2026-04 -> 2026.375."""
    return int(m[:4]) + (int(m[5:7]) + 0.5) / 12


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_property"):
        if r.get("revenue"):
            sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    f = _monthly(read("fred_property"))

    # the hook: the Fed's commercial property price index (Z.1), nominal and deflated
    cre = f["BOGZ1FL075035503Q"]
    cpi = f["CPIAUCNS"]
    idx = {_q(m): v / cre["2001-01"] * 100 for m, v in cre.items() if m >= "1990-01"}
    real = {_q(m): (v / cre["2001-01"]) / (cpi[m] / cpi["2001-01"]) * 100 for m, v in cre.items() if m >= "1990-01" and m in cpi}
    pk1 = max((m for m in cre if "2005" <= m <= "2008-12"), key=cre.get)
    lo1 = min((m for m in cre if "2008" <= m <= "2011-12"), key=cre.get)
    pk2 = max((m for m in cre if "2020" <= m <= "2024-12"), key=cre.get)
    lo2 = min((m for m in cre if m > pk2), key=cre.get)
    last = max(cre)
    R["hook"] = dict(idx=idx, real=real, pk1=pk1, lo1=lo1, pk2=pk2, lo2=lo2, last=last,
                     fall1=cre[lo1] / cre[pk1] - 1, fall2=cre[lo2] / cre[pk2] - 1, since=cre[last] / cre[lo2] - 1,
                     q={m: _q(m) for m in (pk1, lo1, pk2, lo2, last)},
                     gmv=dict(short=get("gmv.short"), long=get("gmv.long"), us=get("gmv.us")),
                     fsr_real=get("fsr.real"), fsr_cre=get("fsr.cre"))

    # Run it
    run = building.run_it()
    run["sweep_cap"] = {round(c, 4): building.value_at(10.0, c) for c in np.arange(0.035, 0.0951, 0.0025)}
    run["sweep_occ"] = {round(o, 2): building.OFFICE_2019.but(occupancy=o).noi() for o in np.arange(0.40, 1.001, 0.05)}
    run["breakeven_occ"] = building.OFFICE_2019.costs * 1e6 / (building.OFFICE_2019.sqft * building.OFFICE_2019.rent)
    run["one_point"] = {c: building.rate_move(c) for c in (0.04, 0.05, 0.075)}
    R["run"] = run

    # A bond with a roof: Realty Income's buying yield against Treasuries
    gs10 = _annual(f["GS10"])
    baa = _annual(f["BAA"])
    oy = {y: get(f"o.yield.{y}") for y in range(2015, 2026)}
    R["bond"] = dict(o_yield=oy, gs10={y: gs10[y] for y in range(2005, 2026)}, baa={y: baa[y] for y in range(2005, 2026)},
                     spread={y: oy[y] - gs10[y] for y in oy}, gs10_now=f["GS10"][max(f["GS10"])], gs10_month=max(f["GS10"]),
                     cap_avg=get("fsr.capavg"), div=get("o.divyield"))

    # the lease
    we = {y: (sec["WE"][y]["revenue"], sec["WE"][y]["profit"]) for y in sorted(sec["WE"])}
    R["lease"] = dict(props=get("o.props"), occ=get("o.occ"), term=get("o.term"), sites=get("amt.sites"),
                      we=we, we_lease=get("we.lease"), we_term=get("we.leaseterm"), we_member=get("we.member"),
                      we_tam=get("we.tam"))

    # debt: a dollar of rent; the banks
    p = sec["PLD"][2025]
    rent, rentexp = get("pld.rental") / 1e3, get("pld.rentexp") / 1e3
    R["debt"] = dict(pld=dict(rev=p["revenue"], rental=rent, rentexp=rentexp, interest=p["interest"], dep=p["depreciation"],
                              profit=p["profit"], noi=get("pld.noi") / 1e3),
                     loans={y: v for y, v in _annual(f["CREACBM027NBOG"]).items() if y >= 2005},
                     loans_now=f["CREACBM027NBOG"][max(f["CREACBM027NBOG"])], loans_month=max(f["CREACBM027NBOG"]),
                     delinq={_q(m): v for m, v in f["DRCRELEXFACBS"].items()}, delinq_last=max(f["DRCRELEXFACBS"]))
    dq = f["DRCRELEXFACBS"]
    R["debt"].update(dq_1991=max(v for m, v in dq.items() if m.startswith("1991")),
                     dq_2010=max(v for m, v in dq.items() if "2009" <= m <= "2011-12"),
                     dq_2019=dq["2019-10"], dq_now=dq[max(dq)])

    # the sectors
    rows = []
    for name, tk, occ in SECTORS:
        s = sec[tk]
        y = max(s)
        mm = [s[k]["profit"] / s[k]["revenue"] for k in s if y - 4 <= k <= y and s[k].get("profit") is not None]
        rows.append(dict(name=name, tk=tk, co=NAMES[tk][0], rev=s[y]["revenue"], margin=float(np.median(mm)),
                         occ=get(occ) if occ else None, re=s[y].get("real_estate"), assets=s[y]["assets"]))
    R["sectors"] = rows

    # offices
    occ = {y: get(f"bxp.occ.{y}") for y in range(2017, 2025)}
    occ[2025] = get("bxp.occ")
    are = {y: (sec["ARE"][y]["revenue"], sec["ARE"][y]["profit"], sec["ARE"][y].get("impairment")) for y in range(2019, 2026)}
    hpp = {y: (sec["HPP"][y]["revenue"], sec["HPP"][y]["profit"]) for y in range(2019, 2026)}
    R["office"] = dict(bxp=occ, q3=get("bxp.occ.2026q3"), leased=get("bxp.leased.2026q3"), sf=get("bxp.sf"),
                       renew=get("bxp.renew"), hpp=get("hpp.occ"), hpp_pl=hpp, slg=get("slg.occ"), are=are,
                       sqft=get("bxp.sqft"))

    # shops and sheds
    ecom = f["ECOMPCTSA"]
    mac = {y: (sec["MAC"][y]["revenue"], sec["MAC"][y]["profit"]) for y in range(2016, 2026)}
    R["retail"] = dict(ecom={_q(m): v for m, v in ecom.items()}, ecom_last=max(ecom), ecom_now=ecom[max(ecom)],
                       ecom_2019=ecom["2019-10"], ecom_2020=max(v for m, v in ecom.items() if m.startswith("2020")),
                       spg=dict(occ=get("spg.occ"), rent=get("spg.rent"), props=get("spg.props")), mac=mac,
                       pld=dict(sqft=get("pld.sqft"), occ=get("pld.occ"), change=get("pld.rentchange"), mtm=get("pld.mtm"),
                                amazon=get("pld.amazon"), yld=get("pld.yield"), margin=get("pld.margin"),
                                cap=building.implied_cap(get("pld.yield") / 100, get("pld.margin") / 100)))

    # owners and the services firms
    svc = {NAMES[tk][0]: {y: (sec[tk][y]["revenue"], sec[tk][y]["profit"] / sec[tk][y]["revenue"]) for y in range(2019, 2026)}
           for tk in ("CBRE", "JLL", "CWK")}
    R["owners"] = dict(bx=get("bx.re"), cbre=dict(rev=get("cbre.rev"), fm=get("cbre.fm"), pm=get("cbre.pm"), lease=get("cbre.lease"),
                                                    sales=get("cbre.sales"), passthrough=get("cbre.passthrough")),
                       svc=svc, reit=get("pld.reit90"), fsr_cre=get("fsr.cre"),
                       listed=sum(sec[tk][max(sec[tk])]["assets"] for tk in NAMES if NAMES[tk][1] not in ("manager", "services", "lender")) / 1e3, pld_assets=sec["PLD"][2025]["assets"],
                       cbre_assets=sec["CBRE"][2025]["assets"])

    # the intermission
    ppi = _annual(f["PCU531120531120"], need=11)
    office = _annual(f["TLOFCONS"])
    comm = _annual(f["TLCOMCONS"])
    R["extra"] = dict(ppi={y: ppi[y] / ppi[2005] for y in ppi if 2005 <= y <= 2025},
                      cpi={y: v / _annual(cpi, need=11)[2005] for y, v in _annual(cpi, need=11).items() if 2005 <= y <= 2025},
                      office={y: office[y] / 1e3 for y in office if y <= 2025}, comm={y: comm[y] / 1e3 for y in comm if y <= 2025})

    # the landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        if not sec[tk]:
            continue
        y = max(sec[tk])
        r = sec[tk][y]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in sec[tk] if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=r["revenue"], margin=float(np.median(mm)), fy=y, tk=tk))
    R["landscape"] = dict(companies=comp)

    R["called"] = dict(we_tam=get("we.tam"), we_rev=we, call=91.0, prob=0.55, q3=get("bxp.occ.2026q3"),
                       leased=get("bxp.leased.2026q3"), occ25=get("bxp.occ"), gmv=get("gmv.long"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("hook", H["pk1"], H["lo1"], round(100 * H["fall1"], 1), H["pk2"], H["lo2"], round(100 * H["fall2"], 1), H["last"],
          round(100 * H["since"], 1))
    for k in ("office", "warehouse"):
        v = R["run"][k]
        print(k, {a: round(b, 2) for a, b in v["then"].items()}, {a: round(b, 2) for a, b in v["now"].items()}, v["loan"],
              round(v["at"]["new_loan"], 1), v["at"]["binds"], round(v["at"]["gap"], 1), round(v["at"]["cash_out"], 1))
    print("breakeven occ", round(R["run"]["breakeven_occ"], 3), {k: round(v, 3) for k, v in R["run"]["one_point"].items()})
    B = R["bond"]
    print("bond", {y: (B["o_yield"][y], round(B["gs10"][y], 2), round(B["spread"][y], 2)) for y in B["o_yield"]}, B["gs10_now"], B["gs10_month"])
    print("we", R["lease"]["we"])
    D = R["debt"]
    print("debt", {k: round(v, 3) for k, v in D["pld"].items()}, round(D["loans_now"]), D["loans_month"], D["dq_1991"], D["dq_2010"],
          D["dq_2019"], D["dq_now"], D["delinq_last"])
    print("sectors", [(s["name"], s["co"], round(s["rev"], 2), round(100 * s["margin"], 1), s["occ"]) for s in R["sectors"]])
    O = R["office"]
    print("office", O["bxp"], O["q3"], "are", {y: tuple(round(x, 2) if x else x for x in v) for y, v in O["are"].items()},
          "hpp", {y: tuple(round(x, 2) for x in v) for y, v in O["hpp_pl"].items()})
    T = R["retail"]
    print("retail", T["ecom_2019"], T["ecom_2020"], T["ecom_now"], T["ecom_last"], {k: (round(v, 3) if isinstance(v, float) else v) for k, v in T["pld"].items()},
          {y: tuple(round(x, 2) for x in v) for y, v in T["mac"].items()})
    print("owners", R["owners"]["cbre"], {k: {y: (round(a, 1), round(100 * b, 1)) for y, (a, b) in v.items()} for k, v in R["owners"]["svc"].items()})
    E = R["extra"]
    print("extra", round(E["ppi"][2025], 2), round(E["cpi"][2025], 2), {y: round(E["office"][y]) for y in (2005, 2015, 2019, 2022, 2025)},
          {y: round(E["comm"][y]) for y in (2005, 2015, 2019, 2022, 2025)})
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
