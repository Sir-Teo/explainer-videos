"""Every number in Part 19 of *Industry, Built* ("Machinery"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry19.compute        # prints the film's numbers; writes .cache/industry19/computed.json

Items:
    hook        Otis's two businesses; Caterpillar's backlog; the world's robots
    run         the Run it tender: cut the machine's price to win the fleet, or hold it (the Works)
    making      Caterpillar's segments and Deere's product lines
    cycle       machinery orders and shipments, equipment investment, capacity use (FRED); Caterpillar's sales
    base        Otis's segments; the Works' maker with its installed base
    dealers     Caterpillar's and Deere's dealers and lenders; United Rentals
    backlog     Caterpillar's backlog, price realization and tariffs
    history     machinery output against jobs, and farm machinery's price against all prices (FRED)
    robots      robot installations by country and density (IFR); automation makers' margins
    china       excavator and robot exports by country (UN Comtrade)
    split       the conglomerates' separations
    landscape   the companies by revenue and margin
    called      the IFR's forecasts against the outcomes; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import machine

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry19"


def _series(rows):
    d: dict = collections.defaultdict(dict)
    for r in rows:
        d[r["series"]][str(r["month"])] = r["value"]
    return d


def _annual(monthly: dict, need: int = 12, how=np.mean) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(how(v)) for y, v in by.items() if len(v) >= need}


def _fy(end: str) -> int:
    y, m = int(end[:4]), int(end[5:7])
    return y - 1 if m <= 3 else y


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_mach"):
        if r.get("revenue") and r["revenue"] > 0:
            sec[r["ticker"]][str(r["year_end"])] = r
    fred = _series(read("fred_mach"))

    def margins(tk, start=2010):
        return {_fy(e): r["profit"] / r["revenue"] for e, r in sec[tk].items() if r.get("profit") is not None and _fy(e) >= start}

    def revenue(tk):
        return {_fy(e): r["revenue"] for e, r in sec[tk].items()}

    # --- hook -------------------------------------------------------------------------------------------------------------
    R["hook"] = dict(ne23=get("otis.ne.sales.2023"), sv23=get("otis.sv.sales.2023"), ne_sales=get("otis.ne.sales"), ne_op=get("otis.ne.op"), sv_sales=get("otis.sv.sales"),
                     sv_op=get("otis.sv.op"), units=get("otis.units"), backlog=(get("cat.backlog.2024"), get("cat.backlog"),
                                                                                get("catq.backlog")),
                     robots=get("ifr.stock"))

    # --- run it -----------------------------------------------------------------------------------------------------------
    t = machine.Tender()
    lo = machine.Tender(attach=0.3)
    R["run"] = dict(table={f"{a}|{b}": list(v) for (a, b), v in t.table().items()}, eq=t.equilibria(),
                    low={f"{a}|{b}": list(v) for (a, b), v in lo.table().items()}, low_eq=lo.equilibria(),
                    fleet=t.fleet, cost=t.cost, hold=t.hold, cut=t.cut, service=t.service, low_attach=lo.attach,
                    floor=t.floor_price(), threshold=machine.attach_threshold(t))

    # --- making -----------------------------------------------------------------------------------------------------------
    R["making"] = dict(cat={"Construction Industries": (get("cat.ci.sales"), get("cat.ci.profit")),
                            "Resource Industries": (get("cat.ri.sales"), get("cat.ri.profit")),
                            "Power & Energy": (get("cat.pe.sales"), None),
                            "Financial Products": (get("cat.fp.rev"), None)},
                       cat_rev=get("cat.rev"), cat_op=get("cat.op"), de_rev=get("de.rev"), de_fin=get("de.fin"),
                       founded=get("cat.founded"), deere_since=get("de.since"))

    # --- the capital-goods cycle ------------------------------------------------------------------------------------------
    orders = _annual(fred["A33SNO"], how=np.sum)
    ships = _annual(fred["A33SVS"], how=np.sum)
    core = _annual(fred["NEWORDER"], how=np.sum)
    eq = _annual(fred["Y033RC1Q027SBEA"], need=4)
    gdp = _annual(fred["GDP"], need=4)
    cap = _annual(fred["CAPUTLG333S"])
    cat_rev = revenue("CAT")
    R["cycle"] = dict(eq_level=eq, orders={y: v / 1e3 for y, v in orders.items()}, ships={y: v / 1e3 for y, v in ships.items()},
                      core={y: v / 1e3 for y, v in core.items()}, eq_share={y: eq[y] / gdp[y] for y in eq if y in gdp},
                      cap=cap, cat_rev=cat_rev, core_fall=(core[2009] / core[2008] - 1),
                      cat_fall=(cat_rev[2016] / cat_rev[2012] - 1), cat_fall20=(cat_rev[2020] / cat_rev[2019] - 1),
                      orders_fall=(orders[2009] / orders[2008] - 1), ships_fall=(ships[2009] / ships[2008] - 1))

    # --- the installed base -----------------------------------------------------------------------------------------------
    mk = machine.Maker()
    demand = machine.cycle_demand()
    rows = mk.run(demand)
    tail = rows[15:]
    R["base"] = dict(otis={"New Equipment": (get("otis.ne.sales"), get("otis.ne.op")),
                           "Service": (get("otis.sv.sales"), get("otis.sv.op"))},
                     sv_share=get("otis.sv.share"), units=get("otis.units"), china=get("otis.china"),
                     rows=[{k: float(v) for k, v in r.items()} for r in rows],
                     new_sw=machine.swings(rows, "new_rev"), svc_sw=machine.swings(rows, "svc_rev"),
                     svc_rev_share=sum(r["svc_rev"] for r in tail) / sum(r["svc_rev"] + r["new_rev"] for r in tail),
                     svc_profit_share=sum(r["svc_profit"] for r in tail) / sum(r["svc_profit"] + r["new_profit"] for r in tail),
                     life=mk.life, service_rate=mk.service_rate, new_margin=mk.new_margin, service_margin=mk.service_margin,
                     lifetime=mk.service_rate * mk.life, per_unit=get("otis.sv.sales") * 1e6 / (get("otis.units") * 1e6))

    # --- dealers, lenders and rental --------------------------------------------------------------------------------------
    R["dealers"] = dict(cat=get("cat.dealers"), de=get("de.dealers"), cat_fp=get("cat.fp.rev"), de_fin=get("de.fin"),
                        de_rev=get("de.rev"), cat_rev=get("cat.rev"), dealer_inv=get("cat.dealer.inv"),
                        uri=dict(rev=get("uri.rev"), oec=get("uri.oec"), units=get("uri.units"), loc=get("uri.locations"),
                                 age=get("uri.age"),
                                 share=get("uri.share"), margin=margins("URI", 2015)))

    # --- the backlog ------------------------------------------------------------------------------------------------------
    btb = {y: orders[y] / ships[y] for y in orders if y in ships}
    R["backlog"] = dict(cat=(get("cat.backlog.2024"), get("cat.backlog"), get("catq.backlog")), price=get("cat.price"),
                        op24=get("cat.op.2024"), op25=get("cat.op"), volume=get("cat.volume"), mfg=get("cat.mfg"), btb=btb,
                        pe=get("cat.pe.sales"), q3=get("catq.sales"), ieepa=get("catq.ieepa"), tariff=get("catq.tariff2026"),
                        rev=get("cat.rev"), pe24=get("cat.pe.2024"), pe_q3=get("catq.pe"), outlook=get("cat.outlook"),
                        outlook_q3=get("catq.outlook"))

    # --- history ------------------------------------------------------------------------------------------------------------
    ip = _annual(fred["IPG333S"])
    jobs = _annual(fred["CES3133300001"])
    farm = _annual(fred["PCU333111333111"])
    cpi = _annual(fred["CPIAUCNS"], need=11)  # the BLS published no October 2025 CPI
    R["history"] = dict(ip={y: ip[y] / ip[1990] for y in ip if y >= 1990}, jobs={y: jobs[y] / jobs[1990] for y in jobs},
                        jobs_abs=jobs, farm_rel={y: (farm[y] / cpi[y]) / (farm[1947] / cpi[1947]) for y in farm if y in cpi and y >= 1947},
                        farm_x=farm[2025] / farm[1947], cpi_x=cpi[2025] / cpi[1947])

    # --- robots ---------------------------------------------------------------------------------------------------------------
    rob: dict = collections.defaultdict(dict)
    for r in read("owid_robots"):
        rob[r["entity"]][int(r["year"])] = r["robots_installed"]
    for k, v in (("China", get("ifr.china")), ("United States", get("ifr.us")), ("Japan", get("ifr.japan")),
                 ("South Korea", get("ifr.korea")), ("Germany", get("ifr.germany")), ("World", get("ifr.inst"))):
        rob[k][2025] = v
    R["robots"] = dict(inst={k: dict(v) for k, v in rob.items()}, stock=get("ifr.stock"), china_dom=get("ifr.china.dom"),
                       dom_hist={"about 2013-2022": get("ifr.china.dom.past"), "2023": get("ifr.china.dom.2023"),
                                 "2024": get("ifr.china.dom.2024"), "2025": get("ifr.china.dom")},
                       density={"South Korea": get("ifr.d.kr"), "Singapore": get("ifr.d.sg"), "Germany": get("ifr.d.de"),
                                "Japan": get("ifr.d.jp"), "United States": get("ifr.d.us"), "EU-27": get("ifr.d.eu"),
                                "China": get("ifr.d.cn")},
                       fc2026=get("ifr.fc2026"), fc2029=get("ifr.fc2029"),
                       auto={tk: margins(tk, 2015) for tk in ("ROK", "EMR", "HON")})

    # --- China ----------------------------------------------------------------------------------------------------------------
    ex: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("comtrade_mach"):
        ex[str(int(r["hs"]))][r["reporter"]][int(r["year"])] = (r["exports_usd_bn"], r["qty"])
    R["china"] = dict(excavators={k: {y: v[0] for y, v in d.items()} for k, d in ex["842952"].items()},
                      excavator_units={k: {y: v[1] for y, v in d.items()} for k, d in ex["842952"].items()},
                      robots={k: {y: v[0] for y, v in d.items()} for k, d in ex["847950"].items()})

    # --- the conglomerates come apart -------------------------------------------------------------------------------------------
    R["split"] = dict(events=[("GE HealthCare", "2023-01-03", "GE"), ("Solventum", "2024-04-01", "3M"),
                              ("GE Vernova", "2024-04-02", "GE"), ("Solstice", "2025-10-30", "Honeywell"),
                              ("Honeywell Aerospace", "2026-06-29", "Honeywell")],
                      years=dict(ge_hc=get("ge.hc"), ge_v=get("ge.vernova"), mmm=get("mmm.solventum"),
                                 sol=get("hon.solstice"), hon=get("hon.aero")),
                      margins={tk: margins(tk, 2015) for tk in ("HON", "MMM", "ITW", "PH")},
                      gev=revenue("GEV"), gev_m=margins("GEV", 2022))

    # --- landscape ------------------------------------------------------------------------------------------------------------
    groups = {"CAT": ("Caterpillar", "construction"), "DE": ("Deere", "farm"), "CNH": ("CNH", "farm"), "AGCO": ("AGCO", "farm"),
              "CMI": ("Cummins", "components"), "OTIS": ("Otis", "buildings"), "CARR": ("Carrier", "buildings"),
              "TT": ("Trane", "buildings"), "JCI": ("Johnson Controls", "buildings"), "ROK": ("Rockwell", "automation"),
              "EMR": ("Emerson", "automation"), "HON": ("Honeywell", "conglomerate"), "ITW": ("Illinois Tool Works", "conglomerate"),
              "PH": ("Parker Hannifin", "components"), "ETN": ("Eaton", "components"), "DOV": ("Dover", "conglomerate"),
              "URI": ("United Rentals", "rental"), "TEX": ("Terex", "construction"), "OSK": ("Oshkosh", "construction"),
              "MMM": ("3M", "conglomerate"), "GEV": ("GE Vernova", "components"), "IR": ("Ingersoll Rand", "components"),
              "XYL": ("Xylem", "components")}
    comp = []
    for tk, (name, grp) in groups.items():
        r = sec[tk][max(sec[tk])]
        m5 = [v for y, v in margins(tk, 2021).items() if 2021 <= y <= 2025]
        comp.append(dict(name=name, group=grp, rev=r["revenue"], margin=float(np.median(m5)) if m5 else r["profit"] / r["revenue"],
                         year=str(_fy(max(sec[tk])))))
    R["steady"] = {tk: margins(tk, 2010) for tk in ("ITW", "CAT", "TEX")}
    R["deere"] = revenue("DE")
    R["components"] = {tk: (sec[tk][max(sec[tk])]["revenue"], float(np.median([v for y, v in margins(tk, 2021).items() if 2021 <= y <= 2025])))
                       for tk in ("CMI", "ETN", "PH")}
    R["landscape"] = dict(companies=comp, q3=get("catq.sales"), backlog=get("catq.backlog"), hon=get("hon.aero"))

    # --- called -------------------------------------------------------------------------------------------------------------------
    world = R["robots"]["inst"]["World"]
    R["called"] = dict(fc2022=get("ifr.fc2022"), act2022=get("ifr.act2022"), fc2024=get("ifr.fc2024"), act2024=world.get(2024),
                       act2023=get("ifr.act2023"), act2025=get("ifr.inst"), implied2025=(get("ifr.fc2022") * 1.05 ** 3,
                                                                                         get("ifr.fc2022") * 1.09 ** 3),
                       fc2026=get("ifr.fc2026"), prob=0.55)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("hook", R["hook"])
    print("run", R["run"]["table"], R["run"]["eq"], R["run"]["low_eq"], round(R["run"]["threshold"], 2))
    c = R["cycle"]
    print("cycle", round(c["orders_fall"], 3), round(c["ships_fall"], 3), round(c["cat_fall"], 3), round(c["cat_fall20"], 3),
          {y: round(100 * v, 2) for y, v in c["eq_share"].items() if y in (1950, 1980, 2000, 2009, 2025)})
    b = R["base"]
    print("base", b["new_sw"], b["svc_sw"], round(b["svc_rev_share"], 3), round(b["svc_profit_share"], 3))
    h = R["history"]
    print("history", round(h["ip"][2025], 2), round(h["jobs"][2025], 2), round(h["farm_rel"][2025], 2), round(h["farm_x"], 1), round(h["cpi_x"], 1))
    print("robots", {k: v.get(2025) for k, v in R["robots"]["inst"].items()})
    ch = R["china"]
    print("china", {k: (v.get(2015), v.get(2025)) for k, v in ch["excavators"].items()})
    print("landscape", [(x["name"], round(x["rev"], 1), round(100 * x["margin"], 1)) for x in R["landscape"]["companies"]])
    print("called", R["called"])


if __name__ == "__main__":
    main()
