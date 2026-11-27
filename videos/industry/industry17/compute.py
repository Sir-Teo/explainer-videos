"""Every number in Part 17 of *Industry, Built* ("Automobiles"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry17.compute        # prints the film's numbers; writes .cache/industry17/computed.json

Items:
    hook        the carmakers' net margins in 2024 and 2025 (SEC, annual reports); Ford's moving line, 1913-14;
                the electric share of new cars (IEA) and China's car exports (UN Comtrade)
    run         the Run it game: two plants, demand 30% below plan, hold the price or discount (the Works)
    making      the 2022 Economic Census of car assembly; the plant's hours per car (the Works); Toyota's 30,000 parts
    dollar      where a new car's dollar goes: dealer (AutoNation), materials and payroll (Census), the maker's margin
    scale       R&D and profit per vehicle against volume (filings); the platform's cost per car (the Works)
    plant       the plant's profit against utilization (the Works); US capacity utilization since 1948 (FRED); the
                newcomers' plants; a launch in three worlds
    lean        dealers' months of supply since 1993 (FRED); what a chip costs against what it stops (Census)
    suppliers   the suppliers' and carmakers' margins (SEC); assemblers, parts makers and dealers (Census)
    history     the price of a new car, a used car and a repair against all prices since 1947; US sales (FRED)
    dealers     AutoNation's revenue and gross profit by line; the dealers in the Census
    finance     the finance arms' profits (GM, Ford, Toyota, Honda); a loan and a lease (the Works); loan rates (FRED)
    profit      where the profit is: trucks, commercial, luxury, motorcycles (filings)
    ev          battery pack costs (DOE); the electric share by region (IEA); the losses and write-downs (filings)
    china       car exports by country (UN Comtrade); China's sales, plans and tariffs (CAAM, gov.cn, USTR, the EU)
    labour      employment (BLS via FRED); the 2023 strike and contract (GM)
    landscape   the carmakers by revenue and margin, latest year
    called      Tesla's 2016 plan, the EIA's 2017 outlook and China's plans against the outcomes; this series' call
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
from explainer.industry.works import auto

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry17"
SUPPLIERS = ("BWA", "APTV", "LEA", "ALV", "GT", "MGA")
DEALERS = ("AN", "LAD", "PAG", "KMX", "CVNA")
MAKERS = ("GM", "F", "TSLA", "TM", "HMC", "STLA", "RACE")


def _series(rows):
    d: dict = collections.defaultdict(dict)
    for r in rows:
        d[r["series"]][str(r["month"])] = r["value"]
    return d


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


def _fy(end: str) -> int:
    """The calendar year a fiscal year mostly falls in (a year ending in March belongs to the year before)."""
    y, m = int(end[:4]), int(end[5:7])
    return y - 1 if m <= 3 else y


def _logit_fit(years, shares):
    """Least-squares line through the log-odds of a share: the logistic curve that fits it, with a 100% ceiling."""
    x = np.array(years, float)
    z = np.log(np.array(shares) / (100 - np.array(shares)))
    b, a = np.polyfit(x, z, 1)
    return a, b


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_auto"):
        if r.get("revenue") and r["revenue"] > 0:
            sec[r["ticker"]][str(r["year_end"])] = r
    fred = _series(read("fred_auto"))
    fx = {k: {int(m[:4]): v for m, v in fred[k].items()} for k in ("AEXUSEU", "AEXJPUS", "AEXCHUS")}
    eur, jpy, cny = fx["AEXUSEU"][2025], fx["AEXJPUS"][2025], fx["AEXCHUS"][2025]
    ev: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("owid_ev"):
        ev[r["series"]][r["entity"]][int(r["year"])] = r["value"]
    cars: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("comtrade_cars"):
        cars[str(int(r["hs"]))][r["reporter"]][int(r["year"])] = r["exports_usd_bn"]
    census = {str(r["code"]): r for r in read("census_auto") if r["table"] == "basic"}
    mats = {str(r["code"]): (r["name"], r["receipts"]) for r in read("census_auto") if r["table"] == "materials"}

    def margin(tk, end):
        r = sec[tk][end]
        return r["profit"] / r["revenue"] if r.get("profit") is not None else None

    def margins(tk, start=2012):
        return {_fy(e): margin(tk, e) for e in sec[tk] if margin(tk, e) is not None and _fy(e) >= start}

    # --- hook -------------------------------------------------------------------------------------------------------------
    hook_m = {}
    for tk in ("GM", "F", "STLA", "TSLA"):
        m = margins(tk)
        hook_m[tk] = (m[2024], m[2025])
    hook_m["TM"] = (margins("TM")[2024], get("tm.ni") / get("tm.rev"))
    hook_m["HMC"] = (get("hmc.ni.prev") / get("hmc.rev.prev"), get("hmc.ni") / get("hmc.rev"))
    hook_m["VW"] = (12_394 / 324_656, get("vw.eat") / get("vw.rev"))
    hook_m["BYD"] = (get("byd.profit.2024") / 777_102.455, get("byd.profit") / get("byd.rev"))
    R["hook"] = dict(margins=hook_m, ford=dict(year=get("ford.line.year"), magneto=(get("ford.magneto.before"),
                     get("ford.magneto.after")), chassis=(get("ford.chassis.before"), get("ford.chassis.rope"),
                     get("ford.chassis.line"))),
                     ev_world=ev["ev_sales_share"]["World"], china_exports=cars["8703"]["China"],
                     koromo=get("toyota.koromo"))

    # --- run it: the showroom duel -----------------------------------------------------------------------------------------
    d, plant = auto.Duel(), auto.Plant()
    game = auto.run_it(d)
    dem = {(a, b): d.demand(d.list_price - (d.discount if a == "discount" else 0),
                            d.list_price - (d.discount if b == "discount" else 0))
           for a in ("hold", "discount") for b in ("hold", "discount")}
    R["run"] = dict(table={f"{a}|{b}": [v / 1e6 for v in vals] for (a, b), vals in game["table"].items()},
                    demand={f"{a}|{b}": v for (a, b), v in dem.items()}, equilibria=game["equilibria"],
                    both_cut=game["both_cut"] / 1e6, price=d.list_price, discount=d.discount, plan=d.base,
                    weak=d.state * d.base, own=d.own, cross=d.cross, capacity=plant.capacity(2),
                    shift_cap=plant.shift_capacity, margin=plant.margin, variable=plant.variable,
                    shift_cost=plant.shift_cost / 1e6, fixed=plant.fixed / 1e6, be=plant.break_even(2),
                    be_share=plant.break_even(2) / plant.capacity(2))

    # --- how a car is made ---------------------------------------------------------------------------------------------------
    a = census["336110"]
    R["making"] = dict(firms=a["firms"], plants=a["establishments"], shipments=a["receipts"] / 1e6,
                       employees=a["employees"], payroll=a["payroll"] / 1e6, materials=a["materials"] / 1e6,
                       hours=plant.hours_per_car(), parts=get("toyota.parts"), tsla=get("tsla.prod.2025"),
                       rivn_cap=get("rivn.capacity"), people=2000, line_hours=1800,
                       us_assemblies=_annual(fred["MVAAUTLTTS"]))

    # --- the dollar ------------------------------------------------------------------------------------------------------------
    dealer = get("an.gp.new") / get("an.rev.new")
    mat_share, pay_share = a["materials"] / a["receipts"], a["payroll"] / a["receipts"]
    maker = 1 - dealer
    split = {"dealer": dealer, "materials": maker * mat_share, "payroll": maker * pay_share,
             "rest": maker * (1 - mat_share - pay_share)}
    total = mats["00772000"][1]
    named = {c: (n, v) for c, (n, v) in mats.items() if c not in ("00772000", "00970099") and v}
    R["dollar"] = dict(price=get("an.new.price"), split=split, mat_share=mat_share, pay_share=pay_share,
                       gmna=get("gm.gmna.ebit") / get("gm.gmna.rev"), blue=get("f.blue.ebit") / get("f.blue.rev"),
                       materials={n: v / 1e6 for c, (n, v) in sorted(named.items(), key=lambda kv: -kv[1][1])},
                       materials_total=total / 1e6, other=mats["00970099"][1] / 1e6)

    # --- scale ------------------------------------------------------------------------------------------------------------------
    tm25 = sec["TM"]["2025-03-31"]
    # Toyota: R&D of fiscal 2025 (the latest in its tagged filings) over that year's units; profit of fiscal 2026
    vol = {"Toyota": (get("tm.units") * 1e3, tm25["rnd"] * 1e9 / fx["AEXJPUS"][2024] * get("tm.units") / get("tm.units.prev"),
                      get("tm.ni") * 1e9 / jpy),
           "Volkswagen": (get("vw.units") * 1e3, 0.067 * get("vw.rev") * 1e6 * eur, get("vw.eat") * 1e6 * eur),
           "BYD": (get("byd.nev") * 1e6, get("byd.rnd") * 1e9 / cny, get("byd.profit") * 1e6 / cny),
           "GM": (get("gm.world.sales") * 1e3, get("gm.rnd") * 1e9, sec["GM"]["2025-12-31"]["profit"] * 1e9),
           "Ford": ((get("f.blue.wholesale") + get("f.e.wholesale") + get("f.pro.wholesale")) * 1e3,
                    sec["F"]["2025-12-31"]["rnd"] * 1e9, sec["F"]["2025-12-31"]["profit"] * 1e9),
           "Tesla": (get("tsla.deliv.2025") * 1e6, sec["TSLA"]["2025-12-31"]["rnd"] * 1e9,
                     sec["TSLA"]["2025-12-31"]["profit"] * 1e9),
           "Rivian": (get("rivn.deliv"), sec["RIVN"]["2025-12-31"]["rnd"] * 1e9, sec["RIVN"]["2025-12-31"]["profit"] * 1e9),
           "Lucid": (get("lcid.deliv"), sec["LCID"]["2025-12-31"]["rnd"] * 1e9, sec["LCID"]["2025-12-31"]["profit"] * 1e9),
           "Ferrari": (get("race.ship"), sec["RACE"]["2025-12-31"]["rnd"] * 1e9 * eur,
                       sec["RACE"]["2025-12-31"]["profit"] * 1e9 * eur)}
    pl = auto.Platform()
    R["scale"] = dict(points={k: dict(units=u, rnd=r_, profit=p, rnd_per=r_ / u, profit_per=p / u)
                              for k, (u, r_, p) in vol.items()},
                      platform=dict(eng=pl.engineering / 1e9, years=pl.years,
                                    curve={v: pl.per_car(v) for v in (50e3, 100e3, 200e3, 500e3, 1e6, 2e6)}),
                      stla_ship=get("stla.ship"), merger=get("stla.merger"), tm_rnd_year="fiscal 2025")

    # --- the plant ----------------------------------------------------------------------------------------------------------------
    util = _annual(fred["CAPUTLG3361T3S"])
    monthly_util = {m: v for m, v in fred["CAPUTLG3361T3S"].items()}
    lowest = min(monthly_util, key=monthly_util.get)
    curve = {round(u, 2): plant.year(u * plant.capacity(2), 2)["profit"] / 1e6 for u in np.linspace(0.3, 1.0, 15)}
    L = auto.launch()
    R["plant"] = dict(curve=curve, be=plant.break_even(2), be_share=plant.break_even(2) / plant.capacity(2),
                      util=util, low_month=lowest, low=monthly_util[lowest],
                      avg=float(np.mean([v for y, v in util.items() if 1948 <= y <= 2025])),
                      rivian=(get("rivn.prod"), get("rivn.capacity")), lucid=(get("lcid.prod"), get("lcid.capacity")),
                      launch={k: {kk: (vv / 1e6 if kk in ("locked", "respond") else vv) for kk, vv in v.items()}
                              for k, v in L["by_state"].items()},
                      launch_e=(L["locked"] / 1e6, L["respond"] / 1e6))

    # --- lean -----------------------------------------------------------------------------------------------------------------------
    supply = {m: v for m, v in fred["AISRSA"].items()}
    low_s = min(supply, key=supply.get)
    chips = mats["33441310"][1]
    R["lean"] = dict(supply=supply, low_month=low_s, low=supply[low_s], s2019=_annual(fred["AISRSA"])[2019],
                     s2025=_annual(fred["AISRSA"])[2025], chips=chips / 1e6, chips_share=chips / total,
                     inv_days={tk: {_fy(e): r["inventory"] / r["revenue"] * 365 for e, r in sec[tk].items()
                                    if r.get("inventory") and _fy(e) >= 2015} for tk in ("GM", "F", "TM", "TSLA")})

    # --- suppliers ------------------------------------------------------------------------------------------------------------------
    sup = {tk: margins(tk, 2015) for tk in SUPPLIERS}
    mk = {tk: margins(tk, 2015) for tk in ("GM", "F", "TM")}
    parts = census["3363"]
    R["suppliers"] = dict(margins=sup, makers=mk,
                          avg={tk: float(np.mean([v for y, v in m.items() if 2015 <= y <= 2025])) for tk, m in {**sup, **mk}.items()},
                          revenue={tk: sec[tk][max(sec[tk])]["revenue"] for tk in SUPPLIERS},
                          census=dict(assembly=(a["firms"], a["employees"], a["receipts"] / 1e6),
                                      parts=(parts["firms"], parts["employees"], parts["receipts"] / 1e6),
                                      bodies=(census["3362"]["firms"], census["3362"]["employees"], census["3362"]["receipts"] / 1e6),
                                      branches={str(c): (census[c]["name"], census[c]["receipts"] / 1e6, census[c]["employees"])
                                                for c in ("33631", "33632", "33633", "33634", "33635", "33636", "33637", "33639")}))

    # --- history: prices and sales ---------------------------------------------------------------------------------------------------
    # the BLS priced new cars, used cars and repairs only in some months of each year before 1953 (and repairs until 1964)
    cpi_new, cpi_used, cpi_rep, cpi_all = (_annual(fred[s], need=4) for s in ("CUUR0000SETA01", "CUUR0000SETA02",
                                                                              "CUUR0000SETD", "CPIAUCNS"))
    base = 1948
    rel = {k: {y: (s[y] / cpi_all[y]) / (s[min(s) if min(s) > base else base] / cpi_all[min(s) if min(s) > base else base])
               for y in s if y in cpi_all and y >= base} for k, s in (("new", cpi_new), ("repair", cpi_rep))}
    rel["used"] = {y: (cpi_used[y] / cpi_all[y]) / (cpi_used[1953] / cpi_all[1953]) for y in cpi_used if y in cpi_all and y >= 1953}
    sales = _annual(fred["TOTALSA"])
    R["history"] = dict(rel=rel, sales=sales, new_x=cpi_new[2025] / cpi_new[base], all_x=cpi_all[2025] / cpi_all[base],
                        rep_x=cpi_rep[2025] / cpi_rep[base], used_2021=(cpi_used[2022] / cpi_used[2020] - 1),
                        sales_peak=max(sales, key=sales.get), sales_low=min((y for y in sales if y < 2026), key=sales.get),
                        monthly_sales=fred["TOTALSA"])

    # --- dealers --------------------------------------------------------------------------------------------------------------------
    lines = ("new", "used", "fi", "ps")
    rev = {k: get(f"an.rev.{k}") for k in lines}
    gp = {k: get(f"an.gp.{k}") for k in lines}
    nd = census["441110"]
    R["dealers"] = dict(rev=rev, gp=gp, rev_share={k: v / sum(rev.values()) for k, v in rev.items()},
                        gp_share={k: v / sum(gp.values()) for k, v in gp.items()},
                        margin={k: gp[k] / rev[k] for k in lines}, per_car={2023: get("an.new.gp.2023"),
                        2024: get("an.new.gp.2024"), 2025: get("an.new.gp")}, fi_per=get("an.fi.per"),
                        units=get("an.new.units"), price=get("an.new.price"),
                        census=dict(firms=nd["firms"], stores=nd["establishments"], sales=nd["receipts"] / 1e6,
                                    staff=nd["employees"], payroll=nd["payroll"] / 1e6),
                        margins={tk: margins(tk, 2015) for tk in DEALERS})

    # --- the finance arm -------------------------------------------------------------------------------------------------------------
    gm_total = get("gm.gmna.ebit")
    rate = {m: v for m, v in fred["TERMCBAUTO48NS"].items()}
    last_rate = rate[max(rate)]
    price = get("an.new.price")
    R["finance"] = dict(gmf=get("gm.gmf.ebt"), gmna=gm_total, gmf_rev=get("gm.gmf.rev"), credit=get("f.credit.ebt"),
                        blue=get("f.blue.ebit"), pro=get("f.pro.ebit"), model_e=get("f.e.ebit"),
                        tm=(get("tm.fs.op"), get("tm.auto.op"), get("tm.op")),
                        hmc=(get("hmc.fs.op"), get("hmc.auto.op"), get("hmc.moto.op")), rate=rate,
                        last_rate=(max(rate), last_rate), price=price,
                        loan=auto.payment(price * 0.9, last_rate / 100, 60),
                        lease=auto.lease(price, price * 0.58, last_rate / 100, 36),
                        loan36=auto.payment(price, last_rate / 100, 36))

    # --- where the profit is ----------------------------------------------------------------------------------------------------------
    R["profit"] = dict(us=dict(cars=get("us.cars"), trucks=get("us.trucks"), crossovers=get("us.crossovers"),
                               total=get("us.industry")),
                       gm_us=dict(cars=get("gm.us.cars"), trucks=get("gm.us.trucks"), crossovers=get("gm.us.crossovers")),
                       ford={k: (get(f"f.{k}.wholesale"), get(f"f.{k}.rev"), get(f"f.{k}.ebit")) for k in ("blue", "e", "pro")},
                       ferrari=dict(units=get("race.ship"), op=sec["RACE"]["2025-12-31"]["operating_income"],
                                    rev=sec["RACE"]["2025-12-31"]["revenue"], eur=eur),
                       toyota=dict(units=get("tm.units") * 1e3, op=get("tm.auto.op"), jpy=fx["AEXJPUS"][2025]),
                       honda=dict(moto=(get("hmc.moto.units"), get("hmc.moto.rev"), get("hmc.moto.op")),
                                  auto=(get("hmc.auto.units"), get("hmc.auto.rev"), get("hmc.auto.op"))),
                       gmna_per=get("gm.gmna.ebit") * 1e6 / (get("gm.gmna.wholesale") * 1e3))

    # --- the electric car -------------------------------------------------------------------------------------------------------------
    pack = table("doe.pack.2023usd")
    shares = {e: dict(ev["ev_sales_share"][e]) for e in ("World", "China", "Europe", "United States", "Norway", "India", "Japan")}
    R["ev"] = dict(pack=pack, pack_fall=1 - pack[2023] / pack[2008], shares=shares,
                   model_e=dict(units=(get("f.e.wholesale.2024"), get("f.e.wholesale")),
                                ebit=(get("f.e.ebit.2024"), get("f.e.ebit")),
                                per=(get("f.e.ebit.2024") * 1e3 / get("f.e.wholesale.2024"),
                                     get("f.e.ebit") * 1e3 / get("f.e.wholesale"))),
                   writedowns={"Ford": get("f.ev_impairment") / 1e3, "GM": get("gm.ev_charges"),
                               "Stellantis": get("stla.charges") * eur},
                   battery=dict(kwh=75, cost=auto.battery(75, pack[2023]), cost2008=auto.battery(75, pack[2008]),
                                parity=auto.parity_per_kwh(75, 6_000), ice=6_000),
                   tsla_gm=get("tsla.auto.gm"), credits=get("tsla.credits"), stock=dict(ev["ev_stock"]["World"]),
                   sales=dict(ev["ev_sales"]["World"]))

    # --- China ------------------------------------------------------------------------------------------------------------------------
    R["china"] = dict(exports={k: dict(v) for k, v in cars["8703"].items()}, bev={k: dict(v) for k, v in cars["870380"].items()},
                      total=get("caam.2025.total"), nev=get("caam.2025.nev"), share=get("caam.2025.nev") / get("caam.2025.total"),
                      export=get("caam.2025.export"), nev_export=get("caam.2025.nev_export"),
                      byd=dict(nev=get("byd.nev"), export=get("byd.export"), rev=get("byd.rev") / cny / 1e3,
                               margin=get("byd.profit") / get("byd.rev")),
                      gm_share=(get("gm.china.share.2023"), get("gm.china.share")), ustr=get("ustr.ev"),
                      eu={k: get(f"eu.cvd.{k}") for k in ("byd", "geely", "saic", "tesla", "other")})

    # --- labour --------------------------------------------------------------------------------------------------------------------------
    jobs = _annual(fred["CES3133600101"])
    wage = (1 + get("uaw.wage.ratify") / 100) * (1 + get("uaw.wage.yearly") / 100) ** 3 * (1 + get("uaw.wage.last") / 100) - 1
    R["labour"] = dict(jobs=jobs, peak=max(jobs, key=jobs.get), low=min(jobs, key=jobs.get), wage=wage,
                       steps=[get("uaw.wage.ratify"), get("uaw.wage.yearly"), get("uaw.wage.yearly"),
                              get("uaw.wage.yearly"), get("uaw.wage.last")],
                       strike=(get("gm.strike.ebit"), get("gm.strike.ni")), bonus=get("uaw.bonus"),
                       gm_union=get("gm.union.us"), ford_uaw=get("f.uaw"),
                       census=(a["employees"], census["3363"]["employees"], census["441110"]["employees"]))

    # --- landscape -------------------------------------------------------------------------------------------------------------------------
    comp = [dict(name="Toyota", group="volume", rev=get("tm.rev") / jpy, margin=get("tm.ni") / get("tm.rev"), units=get("tm.units") / 1e3, year="FY2026"),
            dict(name="Volkswagen", group="volume", rev=get("vw.rev") * eur / 1e3, margin=get("vw.eat") / get("vw.rev"), units=get("vw.units") / 1e3, year="2025"),
            dict(name="Stellantis", group="volume", rev=get("stla.rev") * eur, margin=get("stla.loss") / get("stla.rev"), units=get("stla.ship") / 1e3, year="2025"),
            dict(name="Honda", group="volume", rev=get("hmc.rev") / jpy, margin=get("hmc.ni") / get("hmc.rev"), units=get("hmc.auto.units") / 1e3, year="FY2026"),
            dict(name="BYD", group="china", rev=get("byd.rev") / cny / 1e3, margin=get("byd.profit") / get("byd.rev"), units=get("byd.nev"), year="2025")]
    for tk, name, group, units in (("GM", "GM", "volume", get("gm.world.sales") / 1e3),
                                   ("F", "Ford", "volume", (get("f.blue.wholesale") + get("f.e.wholesale") + get("f.pro.wholesale")) / 1e3),
                                   ("TSLA", "Tesla", "electric", get("tsla.deliv.2025")),
                                   ("RIVN", "Rivian", "electric", get("rivn.deliv") / 1e6),
                                   ("LCID", "Lucid", "electric", get("lcid.deliv") / 1e6)):
        r = sec[tk]["2025-12-31"]
        comp.append(dict(name=name, group=group, rev=r["revenue"], margin=r["profit"] / r["revenue"], units=units, year="2025"))
    r = sec["RACE"]["2025-12-31"]
    comp.append(dict(name="Ferrari", group="premium", rev=r["revenue"] * eur, margin=r["profit"] / r["revenue"],
                     units=get("race.ship") / 1e6, year="2025"))
    for tk, name in (("NIO", "NIO"), ("LI", "Li Auto"), ("XPEV", "XPeng")):
        e = max(sec[tk])
        r = sec[tk][e]
        comp.append(dict(name=name, group="china", rev=r["revenue"] / fx["AEXCHUS"][int(e[:4])], margin=r["profit"] / r["revenue"],
                         units=None, year=e[:4]))
    for tk, name in (("MGA", "Magna"), ("APTV", "Aptiv"), ("LEA", "Lear"), ("BWA", "BorgWarner"), ("ALV", "Autoliv"),
                     ("GT", "Goodyear"), ("AN", "AutoNation"), ("LAD", "Lithia"), ("PAG", "Penske"), ("KMX", "CarMax"),
                     ("CVNA", "Carvana")):
        e = max(sec[tk])
        r = sec[tk][e]
        comp.append(dict(name=name, group="supplier" if tk in SUPPLIERS else "dealer", rev=r["revenue"],
                         margin=r["profit"] / r["revenue"], units=None, year=str(_fy(e))))
    R["landscape"] = dict(companies=comp, fx=dict(eur=eur, jpy=jpy, cny=cny))

    # --- called ---------------------------------------------------------------------------------------------------------------------------
    aeo: dict = collections.defaultdict(dict)
    for r in read("eia_aeo17"):
        aeo[r["series"]][int(r["year"])] = r["thousands"]
    aeo_share = {y: (aeo["electric"][y] + aeo["plugin_hybrid"][y]) / (aeo["cars"][y] + aeo["light_trucks"][y]) * 100
                 for y in aeo["cars"]}
    us = shares["United States"]
    w = shares["World"]
    yrs = [y for y in range(2021, 2026)]
    a_, b_ = _logit_fit(yrs, [w[y] for y in yrs])
    proj = {y: 100 / (1 + np.exp(-(a_ + b_ * y))) for y in range(2021, 2029)}
    R["called"] = dict(tesla=dict(plan=get("tsla.plan.units"), p2018=get("tsla.prod.2018"), p2020=get("tsla.prod.2020"),
                                  p2025=get("tsla.prod.2025")),
                       aeo=aeo_share, us=us, cn_plan=dict(nev2020=get("cn.plan17.nev2020"), share2025=get("cn.plan17.share2025"),
                                                         share2025_2020plan=get("cn.plan20.share2025"),
                                                         nev2020_actual=get("caam.2020.nev"),
                                                         share2020_actual=get("caam.2020.nev") / get("caam.2020.total") * 100,
                                                         share2025_actual=get("caam.2025.nev") / get("caam.2025.total") * 100),
                       world=w, fit=(a_, b_), proj=proj, threshold=float(round(proj[2026])), prob=0.65)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("hook", {k: (round(100 * a, 1), round(100 * b, 1)) for k, (a, b) in R["hook"]["margins"].items()})
    print("run", R["run"]["table"], R["run"]["equilibria"], round(R["run"]["both_cut"]), round(R["run"]["be"]))
    m = R["making"]
    print("making", m["firms"], m["plants"], round(m["shipments"]), m["employees"], round(m["payroll"], 1), round(m["hours"], 1))
    print("dollar", {k: round(v, 4) for k, v in R["dollar"]["split"].items()}, round(R["dollar"]["gmna"], 3),
          list(R["dollar"]["materials"].items())[:6])
    print("scale", {k: (round(v["units"]), round(v["rnd_per"]), round(v["profit_per"])) for k, v in R["scale"]["points"].items()})
    p = R["plant"]
    print("plant", round(p["be_share"], 3), p["low_month"], round(p["low"], 1), round(p["avg"], 1), p["launch"], p["launch_e"])
    ln = R["lean"]
    print("lean", ln["low_month"], ln["low"], round(ln["s2019"], 2), round(ln["s2025"], 2), round(ln["chips"], 2), round(ln["chips_share"], 4),
          {k: round(v.get(2025, 0)) for k, v in ln["inv_days"].items()})
    print("suppliers avg", {k: round(100 * v, 1) for k, v in R["suppliers"]["avg"].items()})
    h = R["history"]
    print("history", round(h["new_x"], 2), round(h["all_x"], 2), round(h["rep_x"], 2), round(h["rel"]["new"][2025], 3),
          round(h["rel"]["repair"][2025], 3), round(h["used_2021"], 3), h["sales_peak"], h["sales_low"])
    dl = R["dealers"]
    print("dealers", {k: round(v, 3) for k, v in dl["gp_share"].items()}, {k: round(v, 3) for k, v in dl["margin"].items()}, dl["census"])
    f = R["finance"]
    print("finance", f["gmf"], f["credit"], f["tm"], f["hmc"], f["last_rate"], round(f["loan"]), round(f["lease"]))
    pr = R["profit"]
    print("profit ferrari per car", round(pr["ferrari"]["op"] * 1e9 / pr["ferrari"]["units"]), "toyota per car yen",
          round(pr["toyota"]["op"] * 1e9 / pr["toyota"]["units"]), "gmna", round(pr["gmna_per"]))
    e = R["ev"]
    print("ev", round(e["pack_fall"], 3), {k: (v.get(2020), v.get(2025)) for k, v in e["shares"].items()}, e["model_e"]["per"],
          e["writedowns"], e["battery"])
    c = R["china"]
    print("china", {k: (v.get(2015), v.get(2020), v.get(2025)) for k, v in c["exports"].items()}, round(c["share"], 3), c["byd"])
    lb = R["labour"]
    print("labour", lb["peak"], round(lb["jobs"][lb["peak"]]), lb["low"], round(lb["jobs"][lb["low"]]), round(lb["wage"], 4))
    print("landscape", [(x["name"], round(x["rev"], 1), round(100 * x["margin"], 1)) for x in R["landscape"]["companies"]])
    cl = R["called"]
    print("called", cl["tesla"], {y: round(v, 1) for y, v in cl["aeo"].items() if y in (2020, 2025)}, {y: cl["us"].get(y) for y in (2020, 2025)},
          cl["cn_plan"], {y: round(v, 1) for y, v in cl["proj"].items()})


if __name__ == "__main__":
    main()
