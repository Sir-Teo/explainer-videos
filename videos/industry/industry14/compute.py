"""Every number in Part 14 of *Industry, Built* ("Water and Waste"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry14.compute        # prints the film's numbers; writes .cache/industry14/computed.json

Items:
    hook        the Great Stink (Hansard, 1858); how often each US utility price index has fallen, 1953-2025 (BLS)
    run         the Run it game: the Valley landfill priced three ways, with a rival's permit fifteen or five years away
    system      water as a system: America's twenty-year needs (EPA's surveys); capital spending against depreciation at
                the listed water companies (SEC)
    regulated   the Works' water company: the asset base, the allowed revenue, the bill; gearing and the shareholders'
                return; England's privatization and PR24 (the Water Commission, the CMA); Thames Water
    elsewhere   American Water's rate cases and plan; Sabesp's privatization and investment; Veolia
    collection  the Works' route: cost per stop against the share of a street; the second truck; the price of collection
                (BLS) and Waste Management's revenue by line
    landfill    the landfill: the 1991 rule; America's landfills, 1988 and 2009 (EPA); tons landfilled since 1960 (EPA);
                tipping fees (EPA); Waste Management's landfill lives; Republic's airspace
    history     seventy-two years of American utility prices against all prices (BLS)
    recycling   where America's rubbish went, 1960-2018 (EPA); recyclable paper prices and China's ban (BLS via FRED);
                Republic's recycled commodity price
    hazard      the regulated wastes: Clean Harbors and Waste Management's medical waste (SEC)
    returns     operating margins year by year: waste and water companies against the cyclicals of earlier parts (SEC)
    world       safely managed water and sanitation by country, 2000 and 2024 (WHO/UNICEF via the World Bank)
    landscape   the listed water and waste companies by group
    called      the EPA's 1989 forecast against what followed; this series' call on the 2027 water price
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get, span
from explainer.industry.works import route, utility

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry14"
WASTE = ("WM", "RSG", "WCN", "CWST", "CLH")
WATER = ("AWK", "WTRG", "AWR", "CWT", "HTO")
CYCLICAL = ("XOM", "NUE", "DOW", "MU", "FCX", "DAL")


def _cpi() -> dict:
    s: dict = collections.defaultdict(dict)
    for r in read("bls_water"):
        s[r["item"]][int(r["year"])] = r["value"]
    return s


def _monthly(rows):
    d: dict = collections.defaultdict(dict)
    for r in rows:
        d[r["series"]][str(r["month"])] = r["value"]
    return d


def _sec() -> dict:
    out: dict = collections.defaultdict(dict)
    for r in read("sec_annual"):
        if str(r["year_end"])[5:7] in ("12", "01") or r["ticker"] in ("MU",):
            out[r["ticker"]][int(str(r["year_end"])[:4])] = r
    return out


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    cpi = _cpi()
    sec = _sec()

    # --- hook -----------------------------------------------------------------------------------------------------------
    def falls(item, y0=1953, y1=2025):
        s = cpi[item]
        return [y for y in range(max(y0, min(s)) + 1, y1 + 1) if y in s and y - 1 in s and s[y] < s[y - 1]]
    names = {"SEHG01": "water and sewerage", "SEHG02": "rubbish collection", "SEHF01": "electricity",
             "SEHF02": "piped gas", "SEHA": "rent", "SA0": "all prices"}
    R["hook"] = dict(cost=get("stink.cost"), rate=get("stink.rate"), years=get("stink.years"), days=get("stink.days"),
                     tideway=get("tideway.licence"),
                     falls={k: dict(name=names[k], n=len(falls(k)), years=falls(k), start=max(1953, min(cpi[k])))
                            for k in names})

    # --- Run it ---------------------------------------------------------------------------------------------------------
    lf = route.ValleyLandfill()
    g = route.run_it(lf)
    R["run"] = dict(games={f"{p}|{y}": dict(pv=v["pv"], full=v["full"], per_ton=v["per_ton"],
                                            fee=[r["fee"] for r in v["rows"][:40]],
                                            left=[r["left"] for r in v["rows"][:40]],
                                            tons=[r["tons"] for r in v["rows"][:40]])
                           for (p, y), v in g.items()},
                    params=dict(airspace=lf.airspace, cost=lf.cost, region=lf.region, neighbours=lf.neighbours,
                                rival_fee=lf.rival_fee, ceiling=lf.ceiling, rate=lf.rate, expansion=lf.expansion,
                                expansion_cost=lf.expansion_cost, expansion_year=lf.expansion_year),
                    curve={T: {p: lf.play(p, T)["pv"] for p in ("fill", "ceiling", "expand")} for T in range(0, 26)},
                    depletion=get("wm.depletion"))
    R["run"]["permit_worth"] = R["run"]["games"]["ceiling|15"]["pv"] - R["run"]["games"]["ceiling|5"]["pv"]

    # --- system ---------------------------------------------------------------------------------------------------------
    dw = {k: get(f"epa.dw.{k}") for k in ("dist", "treat", "storage", "source")}
    capdep = {}
    for t in ("AWK",):
        capdep[t] = {y: (r["capex"], r["depreciation"]) for y, r in sec[t].items()
                     if r.get("capex") and r.get("depreciation") and y >= 2009}
    R["system"] = dict(dw=dw, dw_total=get("epa.dw.need"), cw=get("epa.cw.need"), potw=get("epa.potw"),
                       potw_pop=get("epa.potw_pop"), pws=get("epa.pws"), lead=get("epa.dw.lead"),
                       capdep=capdep, mains=get("awk.mains"),
                       awk_ratio=capdep["AWK"][2025][0] / capdep["AWK"][2025][1])

    # --- regulated: the Works' water company --------------------------------------------------------------------------
    w = utility.WaterCo()
    path, co = [], w
    for t in range(26):
        y = co.year()
        path.append(dict(t=t, rcv=co.rcv, revenue=y["revenue"], bill=y["bill"], ret=y["ret"], dep=y["dep"]))
        co = utility.WaterCo(rcv=y["next_rcv"] / 1.02, real_wacc=w.real_wacc, run_off=w.run_off, opex=w.opex,
                             capex=w.capex, customers=w.customers)     # real terms: strip the indexation
    gears = [0.0, 0.2, 0.4, 0.55, 0.6, 0.7, 0.8]
    R["regulated"] = dict(path=path, first=path[0], wacc=w.real_wacc, run_off=w.run_off, opex=w.opex, capex=w.capex,
                          customers=w.customers,
                          lev_cheap={gg: utility.equity_return(0.04, gg, 0.02) for gg in gears},
                          lev_dear={gg: utility.equity_return(0.04, gg, 0.05) for gg in gears},
                          gear91=get("iwc.gear.1991"), gear09=get("iwc.gear.2009"), roe=get("iwc.roe"),
                          wacc19=get("iwc.wacc19"), wacc24=get("iwc.wacc24"), wacc_bill=get("iwc.wacc_bill"),
                          bill=get("iwc.bill"), enh=get("iwc.enh"), equity=span("iwc.equity"),
                          thames_debt=get("iwc.thames.debt"), thames_penalty=get("iwc.thames.penalty"),
                          thames_customers=get("thames.customers"),
                          allow24=get("cma.allow.pr24"), allow19=get("cma.allow.pr19"), bill_rise=get("cma.bill_rise"),
                          cma_wacc=get("cma.wacc"), cma_roe=get("cma.roe"), cma_debt=get("cma.debt"),
                          wascs=get("iwc.wascs"), listed=get("iwc.listed"), wocs=(get("iwc.wocs.1989"), get("iwc.wocs.2025")))

    # --- elsewhere ------------------------------------------------------------------------------------------------------
    R["elsewhere"] = dict(awk=dict(people=get("awk.people"), states=get("awk.states"), capex10=span("awk.capex10"),
                                   roe=get("awk.ky.roe"), rb=get("awk.ky.rb"), eq=get("awk.ky.eq"),
                                   rev={y: r["revenue"] for y, r in sec["AWK"].items() if y >= 2009}),
                          sbs=dict(before=get("sbs.state.before"), after=get("sbs.state.after"), water=get("sbs.water"),
                                   sewer=get("sbs.sewer"), plan=get("sbs.plan"), target=get("sbs.target"),
                                   capex={y: get(f"sbs.capex.{y}") for y in (2023, 2024, 2025)}),
                          veo=dict(rev=get("veo.rev.2024"), ebit=get("veo.ebit.2024")))

    # --- collection ---------------------------------------------------------------------------------------------------
    rt = route.Route()
    shares = [s / 100 for s in range(10, 101, 5)]
    price = rt.cost_per_stop(1.0) * 1.25
    split = route.split_street(rt, price, shares=(1.0, 0.5, 1 / 3))
    a = cpi["SA0"]
    gb = cpi["SEHG02"]
    m = _monthly(read("fred_waste"))
    ppi = {k: v for k, v in m["PCU562111562111"].items()}
    ppi_y = collections.defaultdict(list)
    for k, v in ppi.items():
        ppi_y[int(k[:4])].append(v)
    R["collection"] = dict(curve=[(s, rt.cost_per_stop(s)) for s in shares], price=price,
                           split={str(round(k, 3)): v for k, v in split.items()},
                           stops_full=rt.stops_per_day(1.0), truck_day=rt.truck_day,
                           garbage_real={y: gb[y] / gb[1984] / (a[y] / a[1984]) for y in sorted(gb) if y >= 1984},
                           ppi={y: float(np.mean(v)) for y, v in ppi_y.items() if len(v) == 12},
                           wm={k: get(f"wm.rev.{k}") for k in ("commercial", "industrial", "residential", "collection",
                                                                "landfill", "landfill_gross", "transfer", "recycling",
                                                                "energy", "health", "total")})

    # --- landfill -------------------------------------------------------------------------------------------------------
    msw = {int(r["year"]): r for r in read("epa_msw")}
    R["landfill"] = dict(liner=get("cfr.liner"), clay=get("cfr.clay"), leachate=get("cfr.leachate"),
                         postclosure=get("cfr.postclosure"),
                         count=(get("epa.landfills.1988"), get("epa.landfills.2009")),
                         tons={y: msw[y]["landfill"] / 1000 for y in sorted(msw)},
                         tip={y: get(f"epa.tip.{y}") for y in (1982, 1985, 1995, 2013)},
                         wm_life={k: get(f"wm.life.{k}") for k in ("0_5", "6_10", "11_20", "21_40", "41")},
                         wm_landfills=get("wm.landfills"), wm_avg=get("wm.life_avg"), wm_transfer=get("wm.transfer"),
                         wm_tons=get("wm.tons"), depletion=get("wm.depletion"),
                         rsg=dict(start=get("rsg.air.2024"), end=get("rsg.air.2025"), used=get("rsg.air.used"),
                                  permits=get("rsg.air.permits"), acq=get("rsg.air.acq"), total=get("rsg.air.total"),
                                  landfills=get("rsg.landfills"), internal=get("rsg.internal")))
    R["landfill"]["rsg"]["years_left"] = R["landfill"]["rsg"]["total"] / R["landfill"]["rsg"]["used"]
    R["landfill"]["per_landfill"] = (msw[1988]["landfill"] / get("epa.landfills.1988"),
                                     msw[2009]["landfill"] / get("epa.landfills.2009"))

    # --- history: the intermission ------------------------------------------------------------------------------------
    real = {}
    for k in ("SEHG01", "SEHG02", "SEHF01", "SEHF02", "SEHA"):
        s = cpi[k]
        y0 = max(1953, min(s))
        real[k] = {y: (s[y] / s[y0]) / (a[y] / a[y0]) for y in sorted(s) if y >= y0}
    R["history"] = dict(real=real, names=names, water_x=cpi["SEHG01"][2025] / cpi["SEHG01"][1953],
                        all_x=a[2025] / a[1953])

    # --- recycling --------------------------------------------------------------------------------------------------------
    paper = m["WPU0912"]
    R["recycling"] = dict(
        msw={y: dict(landfill=msw[y]["landfill"] / 1000, recycling=(msw[y]["recycling"] or 0) / 1000,
                     composting=(msw[y]["composting"] or 0) / 1000, combustion=(msw[y]["combustion_total"] or 0) / 1000,
                     food=(msw[y]["food_other"] or 0) / 1000, generation=msw[y]["generation"] / 1000,
                     lb=msw[y]["lb_per_person_day"]) for y in sorted(msw)},
        paper={k: v for k, v in sorted(paper.items()) if k >= "2010-01"},
        ban=get("wm18.china"), rsg=(get("rsg.recy.2024"), get("rsg.recy.2025")), sens=get("rsg.recy.sens"),
        epa89=dict(tons=get("epa89.tons"), tons2000=get("epa89.tons2000"), landfilled=get("epa89.landfilled"),
                   recycled=get("epa89.recycled")))
    p17 = [v for k, v in paper.items() if k.startswith("2017")]
    p19 = [v for k, v in paper.items() if k.startswith("2019")]
    R["recycling"]["paper_drop"] = 1 - np.mean(p19) / np.mean(p17)
    R["recycling"]["paper_peak"] = max((v, k) for k, v in paper.items() if "2016-01" <= k <= "2018-06")
    R["recycling"]["paper_low"] = min((v, k) for k, v in paper.items() if "2018-01" <= k <= "2020-12")

    # --- hazard -----------------------------------------------------------------------------------------------------------
    R["hazard"] = dict(clh={y: (r["revenue"], r["operating_income"]) for y, r in sec["CLH"].items() if y >= 2009},
                       wm_health=get("wm.rev.health"))

    # --- returns ----------------------------------------------------------------------------------------------------------
    def margins(t):
        return {y: r["net_income"] / r["revenue"] for y, r in sec[t].items()
                if 2010 <= y <= 2025 and r.get("revenue") and r.get("net_income") is not None}
    mg = {t: margins(t) for t in WASTE + WATER + CYCLICAL if t in sec}
    R["returns"] = dict(margins=mg, spread={t: (min(v.values()), max(v.values()), float(np.std(list(v.values()))))
                                            for t, v in mg.items() if v})

    # --- world ------------------------------------------------------------------------------------------------------------
    wb = collections.defaultdict(dict)
    for r in read("wb_water"):
        wb[(r["indicator"], r["country"])][int(r["year"])] = r["value"]
    keep = ["World", "United States", "United Kingdom", "Japan", "France", "China", "Brazil", "Mexico", "India",
            "South Africa", "Bangladesh", "Nigeria", "Ethiopia", "Sub-Saharan Africa"]
    R["world"] = {ind: {c: (wb[(ind, c)].get(2000), wb[(ind, c)].get(2024)) for c in keep if (ind, c) in wb}
                  for ind in ("SH.H2O.SMDW.ZS", "SH.STA.SMSS.ZS")}

    # --- landscape --------------------------------------------------------------------------------------------------------
    comp = []
    for t in WASTE + WATER:
        if t not in sec:
            continue
        yrs = sorted(y for y in sec[t] if sec[t][y].get("revenue"))
        last = yrs[-1]
        m5 = [sec[t][y]["net_income"] / sec[t][y]["revenue"] for y in yrs[-5:]
              if sec[t][y].get("net_income") is not None]
        comp.append(dict(ticker=t, group="waste" if t in WASTE else "water", year=last,
                         revenue=sec[t][last]["revenue"], margin5=float(np.mean(m5)),
                         capex=sec[t][last].get("capex"), dep=sec[t][last].get("depreciation")))
    R["landscape"] = dict(companies=comp, veolia=get("veo.rev.2024"), sabesp_people=get("sbs.water"))

    # --- called -----------------------------------------------------------------------------------------------------------
    w26 = cpi["SEHG01"]
    growth = {y: 100 * (w26[y] / w26[y - 1] - 1) for y in range(1954, 2026) if y in w26 and y - 1 in w26}
    R["called"] = dict(full=get("epa89.full"), count=(get("epa.landfills.1988"), get("epa.landfills.2009")),
                       tons88=msw[1988]["landfill"] / 1000, tons18=msw[2018]["landfill"] / 1000,
                       life=get("wm.life_avg"), rsg_years=R["landfill"]["rsg"]["years_left"],
                       growth=growth, mean10=float(np.mean([growth[y] for y in range(2016, 2026)])),
                       below4=[y for y in range(2016, 2026) if growth[y] < 4.0], prob=0.70,
                       ytd=get("bls.water.ytd2026"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    h = R["hook"]
    print("hook", {k: (v["name"], v["n"], v["start"]) for k, v in h["falls"].items()}, h["days"])
    print("run", {k: (round(v["pv"]), v["full"], round(v["per_ton"], 2)) for k, v in R["run"]["games"].items()},
          "permit worth", round(R["run"]["permit_worth"]))
    s = R["system"]
    print("system", s["dw"], "awk capex/dep 2025", round(s["awk_ratio"], 2))
    rg = R["regulated"]
    print("regulated first year", {k: round(v, 1) for k, v in rg["first"].items()}, "rcv25", round(rg["path"][-1]["rcv"]),
          "bill25", round(rg["path"][-1]["bill"]))
    print("leverage cheap", {k: round(100 * v, 1) for k, v in rg["lev_cheap"].items()},
          "dear", {k: round(100 * v, 1) for k, v in rg["lev_dear"].items()})
    c = R["collection"]
    print("collection", [(s, round(v, 2)) for s, v in c["curve"][::3]], "price", round(c["price"], 2),
          {k: round(v["profit"]) for k, v in c["split"].items()},
          "garbage real 2025", round(c["garbage_real"][2025], 2))
    lf = R["landfill"]
    print("landfill per site (kt)", [round(x) for x in lf["per_landfill"]], "rsg years", round(lf["rsg"]["years_left"]),
          "tons", {y: round(v) for y, v in lf["tons"].items() if y % 10 == 0 or y == 2018})
    hi = R["history"]
    print("history real 2025", {k: round(v[2025], 2) for k, v in hi["real"].items()}, round(hi["water_x"], 1),
          round(hi["all_x"], 1))
    rc = R["recycling"]
    print("recycling 2018", {k: round(v, 1) for k, v in rc["msw"][2018].items()}, "paper drop", round(rc["paper_drop"], 3),
          rc["paper_peak"], rc["paper_low"])
    print("returns spread", {t: tuple(round(100 * x, 1) for x in v) for t, v in R["returns"]["spread"].items()})
    print("world sanitation 2024", {k: v[1] for k, v in R["world"]["SH.STA.SMSS.ZS"].items()})
    print("landscape", [(x["ticker"], round(x["revenue"], 2), round(100 * x["margin5"], 1)) for x in R["landscape"]["companies"]])
    cl = R["called"]
    print("called", {k: (round(v, 2) if isinstance(v, float) else v) for k, v in cl.items() if k != "growth"})


if __name__ == "__main__":
    main()
