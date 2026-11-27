"""Every number in Part 12 of *Industry, Built* ("Chemicals"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry12.compute        # prints the film's numbers; writes .cache/industry12/computed.json

Items:
    hook        Haber and Bosch; world ammonia since 1950 (USGS) and people since 1900 (OWID); nitrogen per hectare
    run         the Run it game: a cracker built in 2012 in Texas on ethane or in Europe on naphtha, played through
                2013-2026 with the IMF's gas and oil prices (the Works); EIA on the build-out and INEOS in Antwerp
    cracker     EIA's yields for ethane and naphtha; the Works' cost of a tonne of ethylene, piece by piece
    feedstock   US ethane production and exports since 1981 (EIA); gas in three markets; ethylene's cost by site since 2000
    cycle       US chemical capacity utilization since 1948; petrochemical and resin prices; commodity makers' profits
    fertilizer  Haber's arithmetic and CF's gas per ton; ammonia's gas cost in the US and Europe; USGS ammonia prices;
                the producers; potash
    gases       Linde's and Air Products' contracts and margins; the Works' gas plant; industrial gas prices
    specialty   paint and cleaning against commodities: margins and prices
    europe      gas in Europe and America since 2019; Germany's and the EU's chemical output (Eurostat); CF's UK closures
    plastics    world plastics production since 1950; what became of plastic waste in 2019 (OECD via OWID)
    harm        Bhopal (1984); PFAS (EPA 2024; 3M and Chemours, 2023)
    landscape   the listed companies by group
    called      EIA's 2005 outlook against 2025; this series' call on German chemical output in 2027
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import cracker

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry12"


def _series(rows, key="series"):
    d: dict = collections.defaultdict(dict)
    for r in rows:
        d[r[key]][str(r["month"])] = r["value"]
    return d


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        if v is not None:
            by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    F = _series(read("fred_chem"))
    E = _series(read("eia_ngl"))
    U: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("usgs_heavy"):
        U[r["material"]][r["item"]][int(r["year"])] = r["value"]
    O: dict = collections.defaultdict(dict)
    for r in read("owid_chem"):
        O[(r["series"], r["column"])][int(r["year"])] = r["value"]
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_annual"):
        sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    ifrs: dict = collections.defaultdict(dict)
    for r in read("sec_ifrs"):
        ifrs[r["ticker"]][int(str(r["year_end"])[:4])] = r
    eu_chem: dict = collections.defaultdict(dict)
    for r in read("eurostat_chem"):
        eu_chem[r["geo"]][str(r["month"])] = r["value"]

    # --- hook ---------------------------------------------------------------------------------------------------------
    wn = dict(U["nitrogen"]["world_production"])
    wn[2025] = get("usgs.n.world.2025") * 1000
    pop = O[("population", "population_historical")]
    nha = O[("nitrogen-fertilizer-application-per-hectare-of-cropland",
             "nutrient_nitrogen_n__total__00003102__use_per_area_of_cropland__005159__kilograms_per_hectare")]
    R["hook"] = dict(patent=get("haber.patent"), prize=get("haber.prize"), bosch=get("bosch.prize"), bosch_year=get("bosch.1913"),
                     world_n=wn, n1950=wn[1950] / 1e6, n2025=wn[2025] / 1e6, pop={y: pop[y] / 1e9 for y in pop if y >= 1900},
                     pop1908=float(np.interp(1908, sorted(pop), [pop[k] for k in sorted(pop)])) / 1e9,
                     pop_last=pop[max(pop)] / 1e9, pop_year=max(pop), n_ha=nha, haber=cracker.haber(1.0))

    # --- gas and oil, annual --------------------------------------------------------------------------------------------
    us, eu, asia, br = (_annual(F[k], 9) for k in ("PNGASUSUSDM", "PNGASEUUSDM", "PNGASJPUSDM", "POILBREUSDM"))
    years = [y for y in range(2000, 2027) if all(y in d for d in (us, eu, asia, br))]
    cu_all = _annual(F["CAPUTLG325S"], 9)
    mk = {y: cracker.markup_from_utilization(cu_all[y]) for y in years if y in cu_all}
    years = [y for y in years if y in mk]
    hist = cracker.play(years, None, br, {"US": us, "EU": eu, "Asia": asia}, markup=mk)
    R["prices"] = dict(us=us, eu=eu, asia=asia, brent=br, years=years,
                       us_m={m: v for m, v in F["PNGASUSUSDM"].items() if m >= "2019-01"},
                       eu_m={m: v for m, v in F["PNGASEUUSDM"].items() if m >= "2019-01"})

    # --- run it ---------------------------------------------------------------------------------------------------------
    run_years = [y for y in years if y >= 2013]
    t_m = {y: hist["Texas, ethane"]["margin"][y] for y in run_years}
    e_m = {y: hist["Europe, naphtha"]["margin"][y] for y in run_years}
    cap = cracker.Cracker("ethane").capacity
    fixed = cracker.Cracker("ethane").fixed
    capex = cracker.Cracker("ethane").capex
    cum_t = np.cumsum([t_m[y] * cap - fixed for y in run_years])
    cum_e = np.cumsum([e_m[y] * cap - fixed for y in run_years])
    payback = next((y for y, c in zip(run_years, cum_t) if c >= capex), None)
    R["run"] = dict(years=run_years, texas=t_m, europe=e_m, markup={y: mk[y] for y in run_years},
                    bohlen=get("dow.bohlen"), cum_texas=list(cum_t), cum_europe=list(cum_e), capex=capex,
                    capacity=cap, fixed=fixed, payback=payback, price={y: hist["price"][y] for y in run_years},
                    cost_t={y: hist["Texas, ethane"]["cost"][y] for y in run_years},
                    cost_e={y: hist["Europe, naphtha"]["cost"][y] for y in run_years},
                    cap13=get("eia.ethylene.cap.2013"), cap20=get("eia.ethylene.cap.2020"), ineos=get("eia.ineos.antwerp"))

    # --- the tree: US chemical sales by segment, 2022 Economic Census ---------------------------------------------------
    seg = {"3251": "basic chemicals", "3252": "plastics, rubber and fibres", "3253": "fertilizers and farm chemicals",
           "3254": "medicines", "3255": "paints and adhesives", "3256": "soaps, cleaners and cosmetics", "3259": "other"}
    sales: dict = collections.defaultdict(float)
    for r in read("census_conc_2022"):
        code = str(r["code"])
        if len(code) == 6 and code[:4] in seg:
            sales[seg[code[:4]]] += r["sales_k"] / 1e6
    R["tree"] = dict(sales=dict(sales), total=sum(sales.values()), petro=next(r["sales_k"] / 1e6 for r in read("census_conc_2022")
                                                                             if str(r["code"]) == "325110"))

    # --- the cracker ----------------------------------------------------------------------------------------------------
    y_last = years[-1]
    R["cracker"] = dict(yields=cracker.YIELDS, year=y_last,
                        ethane=cracker.Cracker("ethane").breakdown(us[y_last], br[y_last]),
                        naphtha=cracker.Cracker("naphtha").breakdown(eu[y_last], br[y_last]),
                        assumptions=dict(fee=cracker.ETHANE_FEE, bbl=cracker.NAPHTHA_BBL_PER_T, ratio=cracker.NAPHTHA_TO_CRUDE,
                                         premium=cracker.COPRODUCT_PREMIUM, energy=cracker.ENERGY, other=cracker.OTHER_CASH))

    # --- feedstock ------------------------------------------------------------------------------------------------------
    eth = _annual(E["PET.M_EPLLEA_FPF_NUS_MBBLD.M"], 12)
    eth_m = E["PET.M_EPLLEA_FPF_NUS_MBBLD.M"]
    exp_m = E["PET.M_EPLLEA_EEX_NUS-Z00_2.M"]
    R["feedstock"] = dict(ethane=eth, ethane_first=eth_m[min(eth_m)], ethane_first_m=min(eth_m), ethane_last=eth_m[max(eth_m)],
                          ethane_last_m=max(eth_m), exports_first=exp_m[min(exp_m)], exports_first_m=min(exp_m),
                          exports_last=exp_m[max(exp_m)], exports_last_m=max(exp_m),
                          exports=_annual(exp_m, 12),
                          cost={s: hist[s]["cost"] for s in ("Texas, ethane", "Europe, naphtha", "Asia, naphtha")},
                          gap={y: hist["Europe, naphtha"]["cost"][y] - hist["Texas, ethane"]["cost"][y] for y in years})

    # --- the cycle ------------------------------------------------------------------------------------------------------
    cu = _annual(F["CAPUTLG325S"])
    nets = {t: {y: sec[t][y]["net_income"] for y in sorted(sec[t]) if 2014 <= y <= 2025 and sec[t][y]["net_income"] is not None}
            for t in ("DOW", "LYB", "WLK", "OLN", "LIN", "SHW")}
    R["cycle"] = dict(cap_util=cu, petro=_annual(F["PCU325110325110"]), resins=_annual(F["PCU325211325211"]), nets=nets)

    # --- fertilizer ------------------------------------------------------------------------------------------------------
    per_ton = get("cf.gas.2025") / (get("cf.ammonia.2025") / 1000)       # MMBtu per short ton of ammonia
    nh3_cost = {"US": {y: us[y] * per_ton for y in years}, "EU": {y: eu[y] * per_ton for y in years}}
    R["fertilizer"] = dict(per_ton=per_ton, cost=nh3_cost, price={y: get(f"usgs.n.price.{y}") for y in range(2021, 2026)},
                           producers={k: get(f"usgs.n.{k}.2025") for k in ("china", "india", "russia", "us")},
                           world=get("usgs.n.world.2025"), us_plants=get("usgs.n.us.plants"), fert=get("usgs.n.us.fert"),
                           gulf=get("usgs.n.us.gulf"), cf_gascost=get("cf.gascost.2025"),
                           potash={k: get(f"usgs.potash.{k}.2025") for k in ("canada", "russia", "china", "belarus")},
                           potash_world=get("usgs.potash.world.2025"), potash_canada=get("usgs.potash.us.canada"),
                           potash_imports=get("usgs.potash.us.imports.2025"), potash_us=get("usgs.potash.us.prod.2025"),
                           us_n=U["nitrogen"]["production"], cf_uk=get("cf.uk"), ppi_n=_annual(F["PCU325311325311"]))

    # --- the companies ---------------------------------------------------------------------------------------------------
    def comp(t, upto=2025):
        if t in ifrs and t not in sec:
            d = {y: {"revenue": ifrs[t][y]["revenue"], "net_income": ifrs[t][y]["profit"]} for y in ifrs[t]}
        else:
            d = sec[t]
        ys = [y for y in d if y <= upto and d[y]["revenue"] and d[y]["net_income"] is not None]
        y = max(ys)
        m5 = [d[k]["net_income"] / d[k]["revenue"] for k in range(y - 4, y + 1)
              if k in d and d[k]["revenue"] and d[k]["net_income"] is not None]
        return dict(ticker=t, year=y, revenue=d[y]["revenue"], net=d[y]["net_income"], margin5=float(np.mean(m5)), n5=len(m5),
                    margin=d[y]["net_income"] / d[y]["revenue"])
    groups = {"commodity": ("DOW", "LYB", "WLK", "OLN", "HUN", "EMN", "CE"), "industrial gases": ("LIN", "APD"),
              "fertilizer": ("CF", "MOS", "ICL"), "specialty": ("SHW", "PPG", "ECL", "IFF", "DD", "CC")}
    land = []
    for g, ts in groups.items():
        for t in ts:
            c = comp(t)
            c["group"] = g
            land.append(c)
    L = {c["ticker"]: c for c in land}
    R["landscape"] = dict(companies=land)
    gp = cracker.GasPlant()
    R["gases"] = dict(linde=get("linde.onsite"), linde_lo=10, linde_hi=20, apd_lo=15, apd_hi=20, lin=L["LIN"], apd=L["APD"],
                      dow=L["DOW"], plant=dict(capex=gp.capex, years=gp.years, fee=gp.fee, minimum=gp.minimum,
                                               cash_full=gp.cash(1.0), cash_half=gp.cash(0.5), cash_zero=gp.cash(0.0),
                                               npv_full=gp.npv([1.0] * gp.years), npv_weak=gp.npv([0.5] * gp.years)),
                      ppi_gases=_annual(F["PCU325120325120"]), ppi_petro=_annual(F["PCU325110325110"]))
    R["specialty"] = dict(shw=L["SHW"], ecl=L["ECL"], ppg=L["PPG"], iff=L["IFF"], dow=L["DOW"], lyb=L["LYB"],
                          ppi_paint=_annual(F["PCU325510325510"]), ppi_petro=_annual(F["PCU325110325110"]))

    # --- Europe -----------------------------------------------------------------------------------------------------------
    de, eu27 = eu_chem["DE"], eu_chem["EU27_2020"]
    de_a, eu_a = _annual(de, 9), _annual(eu27, 9)
    R["europe"] = dict(de=de, eu=eu27, de_a=de_a, eu_a=eu_a, de21=de_a[2021], de_last=de[max(de)], de_last_m=max(de),
                       fall=1 - de[max(de)] / de_a[2021], eu_fall=1 - eu27[max(eu27)] / eu_a[2021],
                       gas_eu=R["prices"]["eu_m"], gas_us=R["prices"]["us_m"], cf_uk=get("cf.uk"))

    # --- plastics ------------------------------------------------------------------------------------------------------
    pp = O[("global-plastics-production", "plastic_production")]
    fate = {k: O[("plastic-fate", k)].get(2019) for k in ("value_recycled", "value_incinerated", "littered_mismanaged_combined",
                                                         "value_landfilled")}
    tot = sum(fate.values())
    fy = sorted(O[("plastic-fate", "value_recycled")])
    fate_years = {k: {y: O[("plastic-fate", k)][y] / 1e6 for y in fy} for k in ("value_recycled", "value_incinerated",
                                                                               "littered_mismanaged_combined", "value_landfilled")}
    R["plastics"] = dict(production={y: v / 1e6 for y, v in pp.items()}, p1950=pp[1950] / 1e6, p_last=pp[max(pp)] / 1e6,
                         fate_years=fate_years, per_person=pp[max(pp)] / pop[max(pp)] if max(pp) in pop else None,
                         p_year=max(pp), fate={k: v / 1e6 for k, v in fate.items()}, recycled_share=fate["value_recycled"] / tot,
                         total_waste=tot / 1e6)

    # --- harm ----------------------------------------------------------------------------------------------------------
    R["harm"] = dict(deaths=get("bhopal.deaths"), settlement=get("bhopal.settlement"), mmm=get("mmm.pfas"), mmm_lo=10.5,
                     cc=get("cc.pfas"), mcl=get("epa.pfas.mcl"))

    # --- called it? ---------------------------------------------------------------------------------------------------
    lng = {int(r["year"]): r["mmcf"] for r in read("eia_gas") if r["series"] == "N9133US2"}
    ip = _annual(F["IPG325S"])
    usn = U["nitrogen"]["production"]
    n25 = get("usgs.n.us.2025") * 1000
    R["called"] = dict(lng_proj=get("aeo05.lng.2025"), lng_2003=get("aeo05.lng.2003"), lng_exports_2025=lng[2025] / 1e6,
                       chem_proj=get("aeo05.bulkchem"), ag_proj=get("aeo05.agchem"),
                       chem_actual=100 * ((ip[2025] / ip[2003]) ** (1 / 22) - 1),
                       n_actual=100 * ((n25 / usn[2003]) ** (1 / 22) - 1), n2003=usn[2003] / 1e6, n2025=n25 / 1e6,
                       de21=de_a[2021], threshold=0.8 * de_a[2021], de25=de_a[2025], de26=de_a.get(2026),
                       de26_months=sum(1 for m in de if m.startswith("2026")), prob=0.75)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    h = R["hook"]
    print(f"ammonia: {h['n1950']:.1f} Mt N (1950) -> {h['n2025']:.0f} (2025); people {h['pop1908']:.2f}bn (1908) -> "
          f"{h['pop_last']:.2f}bn ({h['pop_year']}); N per ha {min(h['n_ha'])} {h['n_ha'][min(h['n_ha'])]} -> {max(h['n_ha'])} "
          f"{h['n_ha'][max(h['n_ha'])]}; haber {h['haber']}")
    r = R["run"]
    print("run: texas margins", {y: round(v) for y, v in r["texas"].items()}, "europe", {y: round(v) for y, v in r["europe"].items()})
    print("cum texas", round(r["cum_texas"][-1]), "europe", round(r["cum_europe"][-1]), "payback", r["payback"])
    c = R["cracker"]
    print("cracker", c["year"], {k: round(v) for k, v in c["ethane"].items()}, {k: round(v) for k, v in c["naphtha"].items()})
    f = R["feedstock"]
    print(f"ethane {f['ethane_first']} ({f['ethane_first_m']}) -> {f['ethane_last']} ({f['ethane_last_m']}); exports "
          f"{f['exports_first']} -> {f['exports_last']}; gap", {y: round(v) for y, v in f["gap"].items() if y % 3 == 0 or y >= 2022})
    cy = R["cycle"]
    print("cap util", {y: round(v) for y, v in cy["cap_util"].items() if y % 10 == 0 or y >= 2020})
    print("nets", {k: {y: round(v, 2) for y, v in d.items() if y >= 2019} for k, d in cy["nets"].items()})
    fe = R["fertilizer"]
    print(f"NH3 gas per ton {fe['per_ton']:.1f}; cost US/EU 2022 {fe['cost']['US'][2022]:.0f}/{fe['cost']['EU'][2022]:.0f}; "
          f"2026 {fe['cost']['US'].get(2026, 0):.0f}/{fe['cost']['EU'].get(2026, 0):.0f}; price {fe['price']}")
    g = R["gases"]
    print("gases", {k: (round(v['revenue'], 1), round(100 * v['margin5'], 1)) for k, v in (('LIN', g['lin']), ('APD', g['apd']), ('DOW', g['dow']))},
          g["plant"])
    s = R["specialty"]
    print("specialty", {k: (round(v['revenue'], 1), round(100 * v['margin5'], 1)) for k, v in s.items() if isinstance(v, dict) and 'revenue' in v})
    e = R["europe"]
    print(f"DE chem 2021 {e['de21']:.1f} -> {e['de_last']} ({e['de_last_m']}): -{100 * e['fall']:.0f}%; EU -{100 * e['eu_fall']:.0f}%")
    p = R["plastics"]
    print(f"plastics {p['p1950']:.0f} -> {p['p_last']:.0f} Mt ({p['p_year']}); recycled {100 * p['recycled_share']:.0f}% of {p['total_waste']:.0f} Mt")
    print("landscape", [(c_['ticker'], c_['group'], round(c_['revenue'], 1), round(100 * c_['margin5'], 1)) for c_ in R['landscape']['companies']])
    print("called", R["called"])


if __name__ == "__main__":
    main()
