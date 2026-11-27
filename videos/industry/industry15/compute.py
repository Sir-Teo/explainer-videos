"""Every number in Part 15 of *Industry, Built* ("Semiconductors"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry15.compute        # prints the film's numbers; writes .cache/industry15/computed.json

Items:
    hook        Moore's 1965 doubling and its 1975 revision; TSMC's founding and its customers
    run         the Run it game: build a fab or book a foundry, at three volumes (the Works)
    making      dies on a wafer; line widths from 1961 to 1975 (Moore)
    node        TSMC's wafer revenue by node, 2023-2025 and the third quarter of 2026
    yield       yield against die size and defect density; dies per wafer; cost per good die (the Works)
    fab         TSMC's capital spending, capacity, shipments, revenue per wafer and margins
    split       TSMC's customers; Intel Foundry's losses; Nvidia's Data Center revenue
    tools       ASML's EUV monopoly; the equipment and design-software makers' revenue (SEC)
    history     US output and producer prices of semiconductors since 1967-72 (FRED); transistors per chip since 1971
    memory      world memory sales (WSTS); Micron's quarters since 2008 (SEC)
    trailing    the analog and power makers' margins (SEC); the 2021 shortage; TSMC's mature nodes
    markets     what chips go into: TSMC's platforms, Nvidia, WSTS by product
    geography   export controls and subsidies; sales by region (WSTS)
    landscape   the listed chip companies by group
    called      Moore's law against transistor counts; WSTS's Autumn 2025 forecast against 2026; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
import math
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.data.tables import table
from explainer.industry.register import get, span
from explainer.industry.works import fab

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry15"
GROUPS = {"foundry": ("TSM", "GFS", "UMC"), "integrated": ("INTC", "TXN", "ADI", "MCHP", "ON", "NXPI", "STM"),
          "fabless": ("NVDA", "AVGO", "QCOM", "AMD", "MRVL"), "memory": ("MU",),
          "equipment": ("AMAT", "LRCX", "KLAC"), "design software": ("SNPS", "CDNS"), "packaging": ("AMKR",)}


def _monthly(rows):
    d: dict = collections.defaultdict(dict)
    for r in rows:
        d[r["series"]][str(r["month"])] = r["value"]
    return d


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_annual"):
        sec[r["ticker"]][str(r["year_end"])] = r
    foreign: dict = collections.defaultdict(dict)
    for r in read("sec_foreign"):
        foreign[r["ticker"]][str(r["year_end"])] = r

    # --- hook -------------------------------------------------------------------------------------------------------------
    R["hook"] = dict(rate=get("moore.1965.rate"), target=get("moore.1965.target"), years=get("moore.1975.years"),
                     founded=get("tsm.founded"), customers=get("tsm.customers"), products=get("tsm.products"),
                     line=[(1959 + k, 2 ** k) for k in range(0, 17)])

    # --- Run it -------------------------------------------------------------------------------------------------------------
    g = fab.run_it()
    F = fab.Fab()
    ch = fab.Chip()
    vols = list(range(2_000, 50_001, 1_000))
    curve = {v: (fab.plan(v, False)["profit"], fab.plan(v, True)["profit"]) for v in vols}
    even = next((v for v in vols if curve[v][1] >= curve[v][0]), None)
    R["run"] = dict(games={f"{v}|{'own' if own else 'foundry'}": x for (v, own), x in g.items()}, curve=curve, even=even,
                    fab=dict(capex=F.capex, life=F.life, fixed=F.fixed, capacity=F.capacity, variable=F.variable),
                    chip=dict(die=ch.die_mm2, price=ch.price), foundry_price=17_000.0, d_new=0.5, d_mature=0.1,
                    wafer_cost={v: F.cost_per_wafer(v) for v in (5_000, 10_000, 20_000, 30_000, 40_000, 50_000)})

    # --- making ---------------------------------------------------------------------------------------------------------------
    R["making"] = dict(dpw100=fab.dies_per_wafer(100), dpw600=fab.dies_per_wafer(600),
                       line61=get("moore.1961.line"), line75=get("moore.1975.line"))

    # --- node -------------------------------------------------------------------------------------------------------------------
    nodes = {"3nm": (6, 18, 24), "5nm": (33, 34, 36), "7nm": (19, 17, 14), "16nm": (10, 8, 7), "28nm": (10, 7, 7),
             "40-65nm": (12, 8, 7), "90nm and older": (10, 8, 5)}     # TSMC 20-F 2025, the table summed into groups
    R["node"] = dict(share=nodes, q3={"2nm": get("tsm.q3.n2"), "3nm": get("tsm.q3.n3"), "5nm": get("tsm.q3.n5"),
                                      "7nm": get("tsm.q3.n7")})
    R["node"]["q3"]["older"] = 100 - sum(R["node"]["q3"].values())

    # --- yield --------------------------------------------------------------------------------------------------------------------
    sizes = list(range(25, 851, 25))
    R["yield"] = dict(sizes=sizes, y={d: [fab.yield_poisson(a, d) for a in sizes] for d in (0.1, 0.3, 0.5)},
                      good={d: [fab.good_dies(a, d) for a in sizes] for d in (0.1, 0.5)},
                      small=dict(dpw=fab.dies_per_wafer(100), y=fab.yield_poisson(100, 0.1), good=fab.good_dies(100, 0.1)),
                      big=dict(dpw=fab.dies_per_wafer(800), y=fab.yield_poisson(800, 0.1), good=fab.good_dies(800, 0.1)))
    R["yield"]["ratio"] = R["yield"]["small"]["good"] / R["yield"]["big"]["good"]

    # --- fab --------------------------------------------------------------------------------------------------------------------
    t = foreign["TSM"]
    capex_twd = {int(k[:4]): v["capex"] for k, v in t.items() if v.get("capex")}
    capex_twd[2025] = 1272.411
    rev_twd = {int(k[:4]): v["revenue"] for k, v in t.items() if v.get("revenue")}
    rev_twd[2025] = get("tsm.rev.2025")
    prof_twd = {int(k[:4]): v["profit"] for k, v in t.items() if v.get("profit")}
    prof_twd[2025] = 1697.604
    ship = {2023: get("tsm.ship.2023"), 2024: get("tsm.ship.2024"), 2025: get("tsm.ship.2025")}
    R["fab"] = dict(capex_twd=capex_twd, rev_twd=rev_twd, prof_twd=prof_twd, ship=ship, capacity=get("tsm.capacity"),
                    util=get("tsm.ship.2025") / get("tsm.capacity"),
                    per_wafer_usd=get("tsm.rev.2025.usd") * 1e9 / (get("tsm.ship.2025") * 1e6),
                    per_wafer_twd={y: rev_twd[y] * 1e9 / (ship[y] * 1e6) for y in ship},
                    gm={2023: get("tsm.gm.2023"), 2024: get("tsm.gm.2024"), 2025: get("tsm.gm.2025"), "3Q26": get("tsm.q3.gm")},
                    capex25=get("tsm.capex.2025.usd"), capex26=span("tsm.capex.2026"), us=get("tsm.us_invest"),
                    q3rev=get("tsm.q3.rev"), q3om=get("tsm.q3.om"), staff=get("tsm.staff"),
                    staff_hist={2023: get("tsm.staff.2023"), 2024: get("tsm.staff.2024"), 2025: get("tsm.staff")})
    R["fab"]["capex_share"] = {y: capex_twd[y] / rev_twd[y] for y in capex_twd if y in rev_twd}

    # --- split -----------------------------------------------------------------------------------------------------------------
    R["split"] = dict(top10=get("tsm.top10"), top1=get("tsm.top1"), top2=get("tsm.top2"),
                      intel_loss={2023: get("intc.foundry.loss.2023"), 2024: get("intc.foundry.loss.2024"),
                                  2025: get("intc.foundry.loss.2025")},
                      intel_ext=get("intc.foundry.ext"), intel_rev=get("intc.foundry.rev"), intel_usg=get("intc.usg.shares"),
                      nvda_dc={2024: get("nvda.dc.2024"), 2026: get("nvda.dc")}, nvda_rev=get("nvda.rev"))
    nv = sec["NVDA"]
    R["split"]["nvda"] = {int(k[:4]): (v["revenue"], v["net_income"]) for k, v in nv.items() if v.get("revenue")}

    # --- tools ----------------------------------------------------------------------------------------------------------------
    def last(tk):
        ys = sorted(k for k in sec[tk] if sec[tk][k].get("revenue"))
        return ys[-1], sec[tk][ys[-1]]
    tools = {}
    for tk in ("AMAT", "LRCX", "KLAC", "SNPS", "CDNS"):
        y, row = last(tk)
        tools[tk] = dict(year=y, revenue=row["revenue"], net=row["net_income"])
    a = foreign["ASML"]
    R["tools"] = dict(companies=tools, asml_rev=get("asml.rev"), asml_gm=get("asml.gm"), asml_units=get("asml.units"),
                      asml_euv=get("asml.euv"), asml_hist={int(k[:4]): v["revenue"] for k, v in a.items() if v.get("revenue")})

    # --- history: the intermission -------------------------------------------------------------------------------------------
    m = _monthly(read("fred_chips"))
    ip = _annual(m["IPG3344S"])
    ppi = _annual(m["PCU334413334413"])
    cpi = {int(r["year"]): r["value"] for r in read("bls_water") if r["item"] == "SA0"}   # BLS annual averages
    real_ppi = {y: (ppi[y] / ppi[1967]) / (cpi[y] / cpi[1967]) for y in ppi if y in cpi and y >= 1967}
    tr = {int(r["year"]): r["transistors"] for r in read("owid_chips")}
    R["history"] = dict(ip=ip, ip_x=ip[2025] / ip[1972], ppi=ppi, ppi_fall=1 - ppi[2025] / ppi[1967], cpi_x=cpi[2025] / cpi[1967],
                        real_ppi=real_ppi, real_fall=1 - real_ppi[2025], transistors=tr,
                        doubling=(max(tr) - min(tr)) / math.log2(tr[max(tr)] / tr[min(tr)]))

    # --- memory ------------------------------------------------------------------------------------------------------------------
    q = [r for r in read("sec_quarterly") if r["ticker"] == "MU"]
    R["memory"] = dict(wsts={2022: get("wsts.mem.2022"), 2024: get("wsts.mem.2024"), 2025: get("wsts.mem.2025"),
                             "2026f": get("wsts.mem.2026f")},
                       mu=[(str(r["quarter_end"]), r["revenue"], r["operating_income"]) for r in q])
    R["memory"]["wsts"][2023] = get("wsts.mem.2024") / 1.793     # the Autumn 2025 table's 2024 growth of 79.3%
    mu = R["memory"]["mu"]
    R["memory"]["mu_capex"] = {int(e[:4]): (r["revenue"], r["capex"]) for e, r in sec["MU"].items()
                               if r.get("revenue") and r.get("capex") and int(e[:4]) >= 2010}
    R["memory"]["mu_low"] = min(mu, key=lambda x: x[2])
    R["memory"]["mu_last"] = mu[-1]
    R["memory"]["mu_2023"] = [x for x in mu if x[0].startswith("2023")]

    # --- trailing edge -------------------------------------------------------------------------------------------------------------
    marg = {}
    for tk in ("TXN", "ADI", "MCHP", "ON", "NXPI"):
        marg[tk] = {int(k[:4]): v["net_income"] / v["revenue"] for k, v in sec[tk].items()
                    if v.get("revenue") and v.get("net_income") is not None and k >= "2015"}
    marg["STM"] = {int(k[:4]): v["profit"] / v["revenue"] for k, v in foreign["STM"].items() if v.get("revenue") and v.get("profit") is not None}
    mature = sum(v[2] for k, v in nodes.items() if k in ("28nm", "40-65nm", "90nm and older"))
    R["trailing"] = dict(margins=marg, mature=mature, analog=get("wsts.analog.2025"))

    # --- markets -------------------------------------------------------------------------------------------------------------------
    PLATS = ("hpc", "phone", "iot", "auto", "dce", "other")
    R["markets"] = dict(platform={"high-performance computing": get("tsm.q3.hpc"), "smartphones": get("tsm.q3.phone"),
                                  "internet of things": get("tsm.q3.iot"), "cars": get("tsm.q3.auto"),
                                  "consumer electronics": get("tsm.q3.dce"), "other": get("tsm.q3.other")},
                        products={"memory": get("wsts.mem.2025"), "logic": get("wsts.logic.2025"), "analog": get("wsts.analog.2025"),
                                  "micro": get("wsts.micro.2025"), "discretes, opto, sensors": get("wsts.other.2025")},
                        total25=get("wsts.2025"), nvda_dc=get("nvda.dc"), nvda_dc24=get("nvda.dc.2024"), nvda_rev=get("nvda.rev"),
                        nvda_gm=get("nvda.gm"), tsm_q3=get("tsm.q3.rev"),
                        plat_years={str(y): {k: get(f"tsm.plat.{k}.{y}") for k in PLATS} for y in (2023, 2024, 2025)})
    R["markets"]["forecast"] = dict(total=(get("wsts.2025"), get("wsts.2026f")), memory=(get("wsts.mem.2025"), get("wsts.mem.2026f")))
    R["markets"]["hpc_twd"] = {2023: get("tsm.plat.hpc.twd.2023"), 2025: get("tsm.plat.hpc.twd.2025")}
    R["markets"]["plat_years"]["3Q 2026"] = {k: get(f"tsm.q3.{k}") for k in PLATS}

    # --- geography -----------------------------------------------------------------------------------------------------------------
    fabs = table("tsm.fabs.nm")
    taiwan = {f: nm for place, d in fabs.items() if "Taiwan" in place or place == "Hsinchu" for f, nm in d.items()}
    abroad = {place: d for place, d in fabs.items() if not ("Taiwan" in place or place == "Hsinchu")}
    R["geography"] = dict(chips_tsm=get("tsm.chips_grant"), esmc=get("tsm.esmc_aid"), us=get("tsm.us_invest"),
                          intel_shares=get("intc.usg.shares"), am_growth=get("wsts.am.2026f"), h20=get("nvda.h20"),
                          fabs=fabs, fab_year=table("tsm.fabs.year"), n_fabs=sum(len(d) for d in fabs.values()),
                          n_taiwan=len(taiwan), best_taiwan=min(taiwan.values()),
                          best_abroad=min(nm for d in abroad.values() for nm in d.values()),
                          leading=sorted(f for f, nm in taiwan.items() if nm <= 3),
                          regions={k: (get(f"wsts.reg.{k}.2025"), get(f"wsts.reg.{k}.2026f")) for k in ("am", "ap", "eu", "jp")},
                          rules=[(get(k), k) for k in ("bis.2022", "bis.2023", "bis.2024", "bis.2025", "bis.2026h200",
                                                       "bis.2026remote")], h20_lic=get("nvda.h20.lic"))

    # --- landscape ------------------------------------------------------------------------------------------------------------------
    comp = []
    for gname, tks in GROUPS.items():
        for tk in tks:
            if tk in ("TSM", "UMC", "GFS", "STM"):
                rows = foreign[tk]
                ys = sorted(k for k in rows if rows[k].get("revenue"))
                ms = [rows[k]["profit"] / rows[k]["revenue"] for k in ys[-5:] if rows[k].get("profit") is not None]
                if tk == "TSM":
                    ms = ms[-4:] + [prof_twd[2025] / rev_twd[2025]]
                    rev_usd, year = get("tsm.rev.2025.usd"), "2025"
                elif tk == "UMC":
                    rev_usd, year = rows[ys[-1]]["revenue"] / 32.1, ys[-1][:4]   # NT$ at about 32 to the dollar (2024)
                else:
                    rev_usd, year = rows[ys[-1]]["revenue"], ys[-1][:4]
            else:
                rows = sec[tk]
                ys = sorted(k for k in rows if rows[k].get("revenue"))
                ms = [rows[k]["net_income"] / rows[k]["revenue"] for k in ys[-5:] if rows[k].get("net_income") is not None]
                rev_usd, year = rows[ys[-1]]["revenue"], ys[-1][:4]
            comp.append(dict(ticker=tk, group=gname, revenue=rev_usd, year=year, margin5=float(np.mean(ms))))
    R["landscape"] = dict(companies=comp, asml_rev=get("asml.rev"))

    # --- called -------------------------------------------------------------------------------------------------------------------
    R["called"] = dict(target=get("moore.1965.target"), chip75=get("moore.1975.chip"), tr=tr,
                       aut=get("wsts.aut.2026f"), aut_mem=get("wsts.aut.mem.2026f"), spring=get("wsts.2026f"),
                       q2calc=get("wsts.q2calc.2026"), h1=get("wsts.h1.2026"), q3=get("sia.q3.2026"), sep=get("sia.sep.2026"),
                       to_sep=get("wsts.h1.2026") + get("sia.q3.2026"), threshold=1800.0, prob=0.65,
                       q4_25=get("wsts.q4.2025"), q3_growth=get("sia.q3.growth") / 100, rate65=get("moore.1965.rate"))
    C = R["called"]
    C["q4_needed"] = C["threshold"] - C["to_sep"]
    C["q4_growth"] = C["q4_needed"] / C["q3"] - 1
    # the quarters of 2026: the second from the third and its growth, the first from the half-year total (derived)
    q2 = C["q3"] / (1 + C["q3_growth"])
    C["quarters"] = {"4Q 2025": C["q4_25"], "1Q 2026": C["h1"] - q2, "2Q 2026": q2, "3Q 2026": C["q3"]}
    C["start65"] = C["target"] / C["rate65"] ** 10   # ten doublings back from 1975
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("run", {k: (round(v["cost_die"], 1), round(v["profit"], 2)) for k, v in R["run"]["games"].items()}, "even", R["run"]["even"])
    print("yield", {k: round(v, 2) for k, v in R["yield"]["small"].items()}, {k: round(v, 2) for k, v in R["yield"]["big"].items()},
          round(R["yield"]["ratio"], 1))
    f = R["fab"]
    print("fab util", round(f["util"], 3), "per wafer $", round(f["per_wafer_usd"]), {y: round(v / 1000) for y, v in f["per_wafer_twd"].items()},
          "capex share", {y: round(v, 2) for y, v in f["capex_share"].items()})
    h = R["history"]
    print("history ip x", round(h["ip_x"]), "ppi fall", round(h["ppi_fall"], 3), "cpi x", round(h["cpi_x"], 1), "real fall",
          round(h["real_fall"], 4), "doubling", round(h["doubling"], 2))
    print("memory", {k: round(v, 1) for k, v in R["memory"]["wsts"].items()}, R["memory"]["mu_low"], R["memory"]["mu_last"])
    print("trailing", {k: round(100 * v.get(2025, float('nan')), 1) for k, v in R["trailing"]["margins"].items()}, R["trailing"]["mature"])
    print("tools", R["tools"]["companies"])
    print("landscape", [(c["ticker"], round(c["revenue"], 1), round(100 * c["margin5"], 1)) for c in R["landscape"]["companies"]])
    print("called", {k: v for k, v in R["called"].items() if k != "tr"})


if __name__ == "__main__":
    main()
