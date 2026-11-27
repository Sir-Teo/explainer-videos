"""Every number in Part 11 of *Industry, Built* ("Heavy Materials"), from the Register, the transcribed tables, the
Filing Room and the Works.

    python -m videos.industry.industry11.compute        # prints the film's numbers; writes .cache/industry11/computed.json

Items:
    hook        Bessemer's 1856 paper; the world's tonnages; what a kilogram of each material costs, beside bananas
    run         the Run it game: an integrated mill through an eight-quarter glut (the Works), and what if every mill ran full
    routes      steel two ways: a blast furnace's recipe (Cleveland-Cliffs) against a minimill's (Nucor), CO2 by route,
                electric-furnace shares by country
    tonne       a ton of steel's price against its metal: Nucor's price and scrap cost, 2018-2025; Cliffs' price and margin;
                the real price of steel since 1939 (BLS PPI over the CPI) and its unit value since 1900 (USGS)
    mustrun     a plant that must run: Nucor's utilization since 2003, US iron and steel capacity utilization since 1972,
                profits of Nucor, US Steel and Cleveland-Cliffs, and the Works' mills' cost curves
    minimills   disruption from below: the US electric-furnace share, Nucor against US Steel since 2010
    glut        China's share of world steel since 1992, its exports against home use, the tariffs
    cement      the world's cement, the US price and plants, concentration, the kiln's market (the Works), the cartel
    aluminium   electricity in solid form: IAI's energy and production, China's share, the Gulf's 2026 fall and the price,
                the US smelters and the tariff premium
    packaging   boxes, cans and bottles: the companies, prices and concentration
    aggregates  the quarry: tonnage, the real price of stone since 1900, Vulcan's ton, reserves
    carbon      CO2 from steel and cement, the chemistry of the kiln and of hydrogen, CBAM
    landscape   the listed companies (SEC), the largest steelmakers (worldsteel)
    called      worldsteel's October forecasts for China against outcomes; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.data.tables import table
from explainer.industry.register import get
from explainer.industry.works import mill

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry11"
LB_PER_KG = 2.20462
SHORT_TON_KG = 907.185


def _series(rows, key="series"):
    d: dict = collections.defaultdict(dict)
    for r in rows:
        d[r[key]][r["month"]] = r["value"]
    return d


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        if v is not None:
            by[int(m[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    F = _series(read("fred_heavy"))
    M = _series(read("fred_metals"))
    cpi = _annual(F["CPIAUCSL"], need=9)
    cpi_last = F["CPIAUCSL"][max(F["CPIAUCSL"])]
    U: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("usgs_heavy"):
        U[r["material"]][r["item"]][int(r["year"])] = r["value"]
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_annual"):
        sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    ifrs: dict = collections.defaultdict(dict)
    for r in read("sec_ifrs"):
        ifrs[r["ticker"]][int(str(r["year_end"])[:4])] = r
    W, CH = table("worldsteel.world"), table("worldsteel.china")

    # --- hook ---------------------------------------------------------------------------------------------------------
    alu = M["PALUMUSDM"]
    alu_m = max(alu)
    banana_m = max(F["APU0000711211"])
    per_kg = {"crushed stone": get("usgs.stone.us.price.2025") / 1000, "cement": get("usgs.cement.us.price.2025") / 1000,
              "steel": get("clf.hrc.2025") / SHORT_TON_KG, "aluminium": alu[alu_m] / 1000,
              "bananas": F["APU0000711211"][banana_m] * LB_PER_KG}
    R["hook"] = dict(year=1856, carbon=get("bessemer.carbon"), cwt=get("bessemer.charge"), minutes=get("bessemer.minutes"),
                     kg_charge=get("bessemer.charge") * 50.8, steel=W[2025], steel_1950=W[1950], cement=get("usgs.cement.world.2025"),
                     aluminium=get("usgs.alu.world.2025") / 1000, per_kg=per_kg, alu_month=alu_m, banana_month=banana_m,
                     steel_pc=get("ws.asu_pc.world.2025"), ratio_cement_steel=get("usgs.cement.world.2025") / W[2025])

    # --- run it -------------------------------------------------------------------------------------------------------
    games = {s: mill.glut(strategy=s) for s in ("price", "output", "bank")}
    allp = mill.industry_glut()
    games_all = {s: mill.glut(strategy=s, prices=allp) for s in ("price", "output", "bank")}
    R["run"] = dict(prices=mill.GLUT_PRICE, orders=mill.GLUT_ORDERS, games=games, all_prices=allp, games_all=games_all,
                    mill=dict(capacity=mill.INTEGRATED.capacity, fixed=mill.INTEGRATED.fixed,
                              variable=mill.INTEGRATED.variable, min_rate=mill.INTEGRATED.min_rate,
                              idle=mill.INTEGRATED.idle, restart=mill.INTEGRATED.restart),
                    breakeven=mill.INTEGRATED.breakeven_price(1.0), discount=mill.SPOT_DISCOUNT,
                    clf_idled=get("clf.idled.2025"))

    # --- steel two ways -----------------------------------------------------------------------------------------------
    R["routes"] = dict(pellets=get("clf.pellets"), coke=get("clf.coke"), coal=get("clf.coke") * get("clf.coal_per_coke"),
                       scrap_bof=get("clf.scrap.bof"), scrap_eaf=get("nucor.scrap.per_ton"),
                       co2={"bfbof": get("ws.co2.bfbof"), "drieaf": get("ws.co2.drieaf"), "scrapeaf": get("ws.co2.scrapeaf")},
                       eaf={k: get(f"ws.eaf.{k}.2025") for k in ("world", "china", "us", "eu", "india", "japan", "korea",
                                                                  "turkiye")},
                       us_integrated=get("usgs.steel.us.integrated"), us_minimills=get("usgs.steel.us.minimills"),
                       us_minimill_cos=get("usgs.steel.us.minimill_cos"))

    # --- the ton and the dollar ---------------------------------------------------------------------------------------
    price, scrap = table("nucor.mill_price"), table("nucor.scrap")
    gross_to_short = 2000 / 2240
    metal = {y: get("nucor.scrap.per_ton") * scrap[y] * gross_to_short for y in price}
    ppi = _annual(F["WPU1017"])
    real = {y: ppi[y] / cpi[y] for y in ppi if y in cpi}
    base = real[max(real)]
    real = {y: v / base for y, v in real.items()}
    uv = {y: U["steel"]["unit_value_98"][y] for y in U["steel"]["unit_value_98"]}
    R["tonne"] = dict(price=price, scrap=scrap, metal=metal, spread={y: price[y] - metal[y] for y in price},
                      p25=get("nucor.price.2025"), s25=get("nucor.scrap.2025"), m25=metal[2025],
                      clf_asp=get("clf.asp.2025"), clf_margin=get("clf.margin.2025"), hrc=get("clf.hrc.2025"),
                      hrc24=get("clf.hrc.2024"), real_ppi=real, real_unit_value_98=uv,
                      nue_net=sec["NUE"][2025]["net_income"], clf_net=sec["CLF"][2025]["net_income"])

    # --- a plant that must run ----------------------------------------------------------------------------------------
    cu = _annual(F["CAPUTLG3311A2S"])
    nets = {t: {y: sec[t][y]["net_income"] for y in sorted(sec[t]) if 2008 <= y <= 2025 and sec[t][y]["net_income"] is not None}
            for t in ("NUE", "X", "CLF", "STLD")}
    rates = np.linspace(0.4, 1.0, 61)
    curves = {k: [m_.unit_cost(r_) for r_ in rates] for k, m_ in (("integrated", mill.INTEGRATED), ("minimill", mill.MINIMILL))}
    R["mustrun"] = dict(nucor_util=table("nucor.utilization"), cap_util=cu, nets=nets, rates=list(rates), curves=curves,
                        int_fixed_share=mill.INTEGRATED.fixed / mill.INTEGRATED.capacity /
                        (mill.INTEGRATED.fixed / mill.INTEGRATED.capacity + mill.INTEGRATED.variable),
                        mini_fixed_share=mill.MINIMILL.fixed / mill.MINIMILL.capacity /
                        (mill.MINIMILL.fixed / mill.MINIMILL.capacity + mill.MINIMILL.variable))

    # --- minimills ----------------------------------------------------------------------------------------------------
    rev = {t: {y: sec[t][y]["revenue"] for y in sorted(sec[t]) if 2010 <= y <= 2025 and sec[t][y]["revenue"]}
           for t in ("NUE", "X")}
    cum = {t: float(sum(v for y, v in nets[t].items() if 2010 <= y <= 2024)) for t in ("NUE", "X")}
    R["minimills"] = dict(eaf_share=table("worldsteel.eaf_share"), us_eaf=table("worldsteel.us_eaf"),
                          us_total=table("worldsteel.us_total"), revenue=rev, cum_net=cum,
                          darlington=get("nucor.darlington"), crawfordsville=get("nucor.crawfordsville"))

    # --- the glut ------------------------------------------------------------------------------------------------------
    share = {y: CH[y] / W[y] for y in CH if y in W}
    R["glut"] = dict(world=W, china=CH, share=share, share_1995=CH[1995] / W[1995], share_2025=CH[2025] / W[2025],
                     asu=table("worldsteel.china_asu"), exports21=get("ws.exports.china.2021"),
                     exports25=get("ws.exports.china.2025"), us_crude=get("ws.crude.us.2025"),
                     countries={k: get(f"ws.crude.{k}.2025") for k in ("china", "india", "us", "japan", "russia", "korea",
                                                                     "turkiye", "germany", "brazil", "iran")},
                     tariff25=get("usgs.steel.tariff.march2025"), tariff50=get("usgs.steel.tariff.june2025"),
                     eu_imports=get("ws.imports.eu.2025"),
                     asu_pc={k: get(f"ws.asu_pc.{k}.2025") for k in ("world", "china", "us", "india")})

    # --- cement --------------------------------------------------------------------------------------------------------
    conc = {r["code"]: r for r in read("census_conc_2022")}

    def cr4(code):
        return conc[code]["cr4"], conc[code]["firms"]
    kilns = [mill.Kiln("A", 0.0, 95.0), mill.Kiln("B", 300.0, 95.0)]
    xs = list(np.linspace(-150, 450, 121))
    mk = mill.market(kilns, xs, haul=0.12)
    cuv = {y: U["cement"]["unit_value_98"][y] for y in U["cement"]["unit_value_98"]}
    R["cement"] = dict(world=get("usgs.cement.world.2025"), china=get("usgs.cement.china.2025"),
                       india=get("usgs.cement.india.2025"), us=get("usgs.cement.us.2025"), vietnam=get("usgs.cement.vietnam.2025"),
                       plants=get("usgs.cement.us.plants"), price=get("usgs.cement.us.price.2025"),
                       price21=get("usgs.cement.us.price.2021"), value=get("usgs.cement.us.value.2025"),
                       readymix=get("usgs.cement.us.readymix"), imports=get("usgs.cement.us.imports.2025"),
                       cr4_cement=cr4("327310"), cr4_readymix=cr4("327320"), cr4_steel=cr4("331110"),
                       cr4_limestone=cr4("212312"), cr4_gravel=cr4("212321"),
                       market=dict(x=xs, winner=[r_["winner"] for r_ in mk], cost=[r_["cost"] for r_ in mk],
                                   price=[r_["price"] for r_ in mk], kilns=[(k.name, k.x, k.cost) for k in kilns], haul=0.12),
                       radius_eu=get("eu.cement.price.uk") * 0.5 / get("eu.cement.haul"),
                       haul_eu=get("eu.cement.haul"), price_uk=get("eu.cement.price.uk"),
                       cartel=dict(start=get("eu.cement.start"), decision=get("eu.cement.decision"),
                                   parties=get("eu.cement.parties"), fine=get("eu.cement.fine"), cut=get("eu.cement.cut")),
                       real_unit_value_98=cuv, calcination=mill.calcination_co2(),
                       ppi=_annual(F["PCU327310327310"]), ppi_rm=_annual(F["PCU327320327320"]))

    # --- aluminium -----------------------------------------------------------------------------------------------------
    prod = table("iai.production")
    gcc = table("iai.gcc_monthly")
    alu_a = _annual(alu)
    lme25 = alu_a[2025]
    sp = mill.smelter_power(500_000, table("iai.energy_world")[2025])
    R["aluminium"] = dict(energy=table("iai.energy_world"), energy25=table("iai.energy_2025"), smelter=sp,
                          production=prod, china_share={y: prod["China"][y] / prod["World"][y] for y in prod["China"]},
                          gcc_monthly=gcc, gcc_base=float(np.mean([gcc[f"2025-{m:02d}"] for m in range(1, 13)])),
                          gcc_low=min(gcc.values()), gcc_share25=prod["GCC"][2025] / prod["World"][2025],
                          price={m: v for m, v in alu.items() if m >= "2024-01"}, lme25=lme25,
                          us_price25=get("usgs.alu.us.price.2025"), us_price24=get("usgs.alu.us.price.2024"),
                          lme25_c=lme25 / 1000 / LB_PER_KG * 100, lme24_c=alu_a[2024] / 1000 / LB_PER_KG * 100,
                          us_primary=U["aluminum"]["production"], us_primary25=get("usgs.alu.us.primary.2025"),
                          smelters=get("usgs.alu.us.smelters"), power_share=get("alcoa.power_share"),
                          tariff=get("usgs.alu.tariff.june2025"), cr4=cr4("331313"),
                          uses=dict(transport=get("usgs.alu.us.transport"), packaging=get("usgs.alu.us.packaging")))

    # --- packaging -----------------------------------------------------------------------------------------------------
    def comp(t, upto=2025):
        ys = [y for y in sec[t] if y <= upto and sec[t][y]["revenue"] and sec[t][y]["net_income"] is not None]
        y = max(ys)
        m5 = [sec[t][k]["net_income"] / sec[t][k]["revenue"] for k in range(y - 4, y + 1)
              if k in sec[t] and sec[t][k]["revenue"] and sec[t][k]["net_income"] is not None]
        om = [sec[t][k]["operating_income"] / sec[t][k]["revenue"] for k in range(y - 4, y + 1)
              if k in sec[t] and sec[t][k]["revenue"] and sec[t][k]["operating_income"] is not None]
        return dict(ticker=t, year=y, revenue=sec[t][y]["revenue"], net=sec[t][y]["net_income"],
                    margin5=float(np.mean(m5)), op5=float(np.mean(om)) if om else None, n5=len(m5))
    R["packaging"] = dict(companies={t: comp(t) for t in ("IP", "SW", "PKG", "BALL", "CCK", "OI")},
                          cr4_box=cr4("322211"), cr4_glass=cr4("327213"), cr4_cans=cr4("332431"),
                          cr4_board=cr4("322130"),
                          ppi={k: _annual(F[k]) for k in ("PCU322211322211", "PCU327213327213", "PCU332431332431")},
                          ip_paper=_annual(F["IPG3221S"]))

    # --- aggregates -----------------------------------------------------------------------------------------------------
    st = U["crushed_stone"]
    stone_real = {y: st["unit_value"][y] / cpi.get(y, np.nan) * cpi_last for y in st["unit_value"] if y in cpi}
    mcs = {2022: 14.31, 2023: 15.86, 2024: 17.50, 2025: get("usgs.stone.us.price.2025")}
    for y, v in mcs.items():
        if y in cpi:
            stone_real[y] = v / cpi[y] * cpi_last
    steel_real = {y: U["steel"]["unit_value"][y] / cpi[y] * cpi_last for y in U["steel"]["unit_value"] if y in cpi}
    R["aggregates"] = dict(tonnes=get("usgs.stone.us.2025"), value=get("usgs.stone.us.value.2025"),
                           quarries=get("usgs.stone.us.quarries"), price=get("usgs.stone.us.price.2025"),
                           aggregate=get("usgs.stone.us.aggregate"), to_cement=get("usgs.stone.us.cement"),
                           stone_real=stone_real, steel_real=steel_real, mcs_prices=mcs,
                           vmc=dict(shipments=get("vmc.shipments.2025"), price=get("vmc.price.2025"), gp=get("vmc.gp.2025"),
                                    cashgp=get("vmc.cashgp.2025"), reserves=get("vmc.reserves"), truck=get("vmc.truck"),
                                    years=get("vmc.reserves") * 1000 / get("vmc.shipments.2025")),
                           mlm_crh=get("mlm.crh.2024"), production=st["production"],
                           ppi_stone=_annual(F["WPU1321"]), ppi_steel=ppi)

    # --- carbon --------------------------------------------------------------------------------------------------------
    co2: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("owid_co2"):
        co2[r["series"]][r["entity"]][int(r["year"])] = r["value"]
    cem_w = co2["annual-co2-cement"]["World"]
    tot_w = co2["annual-co2-emissions-per-country"]["World"]
    yl = max(y for y in cem_w if y in tot_w)
    h2 = {p: mill.hydrogen_cost(p) for p in (2.0, 5.0)}
    R["carbon"] = dict(steel_avg=get("ws.ghg.avg.2024"), steel_total=get("ws.ghg.total.2024"),
                       steel_share=(7.0, 8.0), cement_co2=cem_w[yl] / 1e9, total_co2=tot_w[yl] / 1e9,
                       cement_share=cem_w[yl] / tot_w[yl], year=yl,
                       cement_series={y: v / 1e9 for y, v in cem_w.items() if y >= 1950},
                       china_cement=co2["annual-co2-cement"]["China"].get(yl, 0) / 1e9,
                       calcination=mill.calcination_co2(), h2_kg=mill.hydrogen_per_tonne_iron() * 1000,
                       co2_chem=mill.carbon_per_tonne_iron(), h2=h2, blended=get("usgs.cement.us.blended"),
                       capex=get("ws.capex.facilities"), scrap_avoids=get("ws.scrap.avoids.co2"),
                       cbam=get("eu.cbam.start"))

    # --- landscape -----------------------------------------------------------------------------------------------------
    groups = {"steel": ("NUE", "STLD", "CLF", "CMC"), "cement and aggregates": ("CRH", "AMRZ", "VMC", "MLM", "EXP"),
              "aluminium": ("AA", "CENX"), "packaging": ("IP", "SW", "PKG", "BALL", "CCK", "OI")}
    land = []
    for g, ts in groups.items():
        for t in ts:
            c = comp(t)
            c["group"] = g
            land.append(c)
    for t in ("MT", "CX"):
        ys = [y for y in ifrs[t] if ifrs[t][y]["revenue"] and ifrs[t][y]["profit"] is not None]
        y = max(ys)
        m5 = [ifrs[t][k]["profit"] / ifrs[t][k]["revenue"] for k in range(y - 4, y + 1) if k in ys]
        land.append(dict(ticker=t, year=y, revenue=ifrs[t][y]["revenue"], net=ifrs[t][y]["profit"],
                         margin5=float(np.mean(m5)), n5=len(m5), group="steel" if t == "MT" else "cement and aggregates"))
    comps = ("baowu", "arcelormittal", "nippon", "ansteel", "hbis", "shagang", "jianlong", "posco", "delong", "tata",
             "jsw", "shougang", "jfe", "nucor", "cliffs", "stld")
    R["landscape"] = dict(companies=land,
                          steelmakers=[(k, get(f"ws.company.{k}.2025")) for k in comps],
                          sro27=get("ws.sro.china.2027"), construction=_annual(F["TTLCONS"], need=9))

    # --- called it? ----------------------------------------------------------------------------------------------------
    sro = table("worldsteel.sro_china")
    asu = table("worldsteel.china_asu")
    actual = {y: 100 * (asu[y] / asu[y - 1] - 1) for y in asu if y - 1 in asu}
    rows = []
    for made, f in sorted(sro.items()):
        nxt = made + 1
        rows.append(dict(made=made, year=nxt, forecast=f["next"], actual=actual.get(nxt)))
    R["called"] = dict(rows=rows, same=[dict(made=m_, forecast=f["same"], actual=actual.get(m_)) for m_, f in sorted(sro.items())],
                       actual=actual, f26=get("ws.sro.china.2026"), ytd=get("ws.prod.china.jan_oct.change"),
                       ytd_mt=get("ws.prod.china.jan_oct.2026"), prob=0.7)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    h = R["hook"]
    print("per kg:", {k: round(v, 3) for k, v in h["per_kg"].items()}, h["alu_month"], h["banana_month"])
    print(f"steel {h['steel']} Mt, cement {h['cement']} Mt (x{h['ratio_cement_steel']:.1f}), aluminium {h['aluminium']} Mt")
    r_ = R["run"]
    print("run:", {s: round(g["total"]) for s, g in r_["games"].items()}, "all-push", {s: round(g["total"]) for s, g in r_["games_all"].items()},
          [round(p) for p in r_["all_prices"]], "breakeven", round(r_["breakeven"]))
    t = R["tonne"]
    print("tonne:", {y: (t["price"][y], round(t["metal"][y]), round(t["spread"][y])) for y in t["price"]}, "NUE net", t["nue_net"], "CLF", t["clf_net"])
    print("real PPI:", {y: round(v, 2) for y, v in t["real_ppi"].items() if y % 10 == 0 or y >= 2020})
    m_ = R["mustrun"]
    print("cap util:", {y: round(v) for y, v in m_["cap_util"].items() if y % 5 == 0 or y >= 2020})
    print("nets:", {k: {y: round(v, 2) for y, v in d.items() if y >= 2014} for k, d in m_["nets"].items()})
    print("fixed share at full: integrated", round(m_["int_fixed_share"], 2), "minimill", round(m_["mini_fixed_share"], 2))
    mm = R["minimills"]
    print("revenue NUE/X:", {y: (round(mm["revenue"]["NUE"].get(y, 0), 1), round(mm["revenue"]["X"].get(y, 0), 1)) for y in (2010, 2015, 2020, 2024)},
          "cum net 2010-2024", {k: round(v, 1) for k, v in mm["cum_net"].items()})
    g = R["glut"]
    print(f"China share 1995 {g['share_1995']:.2f}, 2025 {g['share_2025']:.2f}; exports 2021 {g['exports21']} -> 2025 {g['exports25']}")
    c = R["cement"]
    print("cement:", c["world"], c["china"], c["india"], c["us"], "price", c["price"], "cr4", c["cr4_cement"], c["cr4_readymix"],
          "radius_eu", round(c["radius_eu"]), "calcination", round(c["calcination"], 3))
    a = R["aluminium"]
    print("alu:", "china share", {y: round(v, 2) for y, v in a["china_share"].items() if y % 5 == 0 or y == 2025},
          "gcc base", round(a["gcc_base"]), "low", a["gcc_low"], "lme25", round(a["lme25"]), "c/lb", round(a["lme25_c"], 1),
          "us", a["us_price25"], "smelter", a["smelter"])
    print("price 2026:", {k: round(v) for k, v in a["price"].items() if k >= "2025-10"})
    p = R["packaging"]
    print("packaging:", {k: (round(v["revenue"], 1), round(100 * v["margin5"], 1)) for k, v in p["companies"].items()},
          p["cr4_box"], p["cr4_glass"], p["cr4_cans"])
    ag = R["aggregates"]
    print("stone real:", {y: round(v, 2) for y, v in ag["stone_real"].items() if y % 20 == 0 or y >= 2020},
          "vmc years", round(ag["vmc"]["years"]))
    print("steel real:", {y: round(v) for y, v in ag["steel_real"].items() if y % 20 == 0 or y >= 2010})
    cb = R["carbon"]
    print(f"carbon: cement {cb['cement_co2']:.2f} Gt of {cb['total_co2']:.1f} ({100 * cb['cement_share']:.1f}%) in {cb['year']}; "
          f"calcination {cb['calcination']:.2f}; H2 {cb['h2_kg']:.1f} kg; {cb['h2']}")
    print("landscape:", [(c_["ticker"], c_["group"], round(c_["revenue"], 1), round(100 * c_["margin5"], 1)) for c_ in R["landscape"]["companies"]])
    print("called:", R["called"]["rows"], R["called"]["actual"])


if __name__ == "__main__":
    main()
