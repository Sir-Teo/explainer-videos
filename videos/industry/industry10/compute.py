"""Every number in Part 10 of *Industry, Built* ("Farming and Food"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry10.compute        # prints the film's numbers; writes .cache/industry10/computed.json

Items:
    hook        wheat yields in Mexico, India, Pakistan and the world since 1961 (FAO via Our World in Data); Borlaug
    dollar      USDA ERS's food dollar, 2007-2025: the farm share and the thirteen industry groups
    acre        an acre of corn, soybeans and wheat: ERS's costs and returns, 1996-2025
    run         the Run it game: three real corn seasons (2012, 2014, 2020), a forward sale and storage
    treadmill   Cochrane's treadmill (the Works), US maize yields, the real price of maize, the number of farms
    bread       a bushel to a loaf: the wheat in a pound of white bread against its price
    chain       the margin ladder: profit as a share of revenue, from the corn acre to the supermarket
    inputs      fertilizer per acre, the nitrogen fertilizer price index, and the input makers' accounts
    traders     ADM and Bunge (SEC) and Cargill (annual report)
    futures     the price of maize, month by month, since 1992
    meat        the packers' concentration, Tyson's and Pilgrim's margins, the price of beef
    income      US net farm income since 1910 in today's dollars, and government payments
    land        farm real estate in today's dollars, and the return on farm assets from income and from capital gains
    cocoa       the price of cocoa, the ICCO's crops, and the chocolate makers' margins
    rice        the world price of rice around India's export ban
    calories    food supply per person (FAO via Our World in Data), against The Population Bomb
    call        this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import farm

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry10"


def _series(rows, key="series"):
    d: dict = collections.defaultdict(dict)
    for r in rows:
        d[r[key]][r["month"]] = r["value"]
    return d


def _annual(monthly: dict) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        if v is not None:
            by[int(m[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) == 12}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    F = _series(read("fred_food"))
    cpi = F["CPIAUCSL"]
    cpi_last = max(cpi)

    def real(m, v):
        return v * cpi[cpi_last] / cpi[m]

    # --- the hook: Borlaug's wheat ------------------------------------------------------------------------------------
    ow: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("owid_ag"):
        ow[r["series"]][r["entity"]][int(r["year"])] = r["value"]
    wy = ow["wheat-yields"]
    R["hook"] = dict(wheat={e: dict(sorted(wy[e].items())) for e in ("Mexico", "India", "Pakistan", "World", "United States")},
                     prize=get("borlaug.prize"), mexico=get("borlaug.mexico"), india=get("borlaug.india"),
                     born=get("borlaug.born"))
    for e in ("Mexico", "India", "Pakistan", "World"):
        R["hook"][f"{e}_x"] = wy[e][max(wy[e])] / wy[e][1961]

    # --- the food dollar --------------------------------------------------------------------------------------------
    fd = [r for r in read("ers_food_dollar") if r["model"] == "agfeds"]
    share = collections.defaultdict(dict)
    groups: dict = collections.defaultdict(dict)
    spend = {}
    for r in fd:
        y = int(r["year"])
        if r["series"] == "Marketing bill" and r["category"] == "Farm share" and r["unit"] == "cents":
            share[r["channel"]][y] = r["value"]
        if r["series"] == "Industry group bill" and r["unit"] == "cents":
            groups[(r["channel"], y)][r["category"]] = r["value"]
        if r["series"] == "Industry group total" and r["unit"] == "usd_m" and r["channel"] == "All":
            spend[y] = r["value"] / 1000
    last = max(share["All"])
    R["dollar"] = dict(year=last, farm=share["All"][last], home=share["Food-at-home"][last],
                       away=share["Food-away-from-home"][last], series={k: dict(sorted(v.items())) for k, v in share.items()},
                       groups=dict(sorted(groups[("All", last)].items(), key=lambda kv: -kv[1])),
                       groups_home=dict(sorted(groups[("Food-at-home", last)].items(), key=lambda kv: -kv[1])),
                       spend=spend[last], spend_series=dict(sorted(spend.items())))

    # --- an acre ---------------------------------------------------------------------------------------------------
    cr: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("ers_costs"):
        cr[r["crop"]][int(r["year"])][r["item"]] = r["value"]
    c25 = cr["corn"][2025]
    op_items = ["Seed", "Fertilizer", "Chemicals", "Custom services", "Fuel, lube, and electricity", "Repairs",
                "Interest on operating capital", "Purchased irrigation water"]
    oh_items = ["Hired labor", "Opportunity cost of unpaid labor", "Capital recovery of machinery and equipment",
                "Opportunity cost of land", "Taxes and insurance", "General farm overhead"]
    acre = farm.Acre("corn", c25["Yield"], c25["Total, operating costs"], c25["Total, allocated overhead"],
                     land=c25["Opportunity cost of land"])
    net = {crop: {y: d.get("Value of production less total costs listed") for y, d in sorted(v.items())}
           for crop, v in cr.items()}
    netop = {crop: {y: d.get("Value of production less operating costs") for y, d in sorted(v.items())}
             for crop, v in cr.items()}
    R["acre"] = dict(year=2025, yield_bu=c25["Yield"], price=c25["Price"], revenue=c25["Total, gross value of production"],
                     operating={k: c25[k] for k in op_items if k in c25}, overhead={k: c25[k] for k in oh_items if k in c25},
                     op_total=c25["Total, operating costs"], oh_total=c25["Total, allocated overhead"],
                     cost=c25["Total, costs listed"], net=c25["Value of production less total costs listed"],
                     net_op=c25["Value of production less operating costs"], size=c25["Enterprise size"],
                     breakeven=acre.breakeven_price(), breakeven_op=acre.breakeven_price(True),
                     land_residual=acre.land_residual(c25["Price"]), land=c25["Opportunity cost of land"],
                     net_series=net, netop_series=netop,
                     losing_years={crop: sum(1 for v in s.values() if v is not None and v < 0) for crop, s in net.items()},
                     n_years={crop: len(s) for crop, s in net.items()},
                     yields={y: d["Yield"] for y, d in sorted(cr["corn"].items())},
                     fert={y: d["Fertilizer"] for y, d in sorted(cr["corn"].items())},
                     seed={y: d["Seed"] for y, d in sorted(cr["corn"].items())},
                     prices={y: d["Price"] for y, d in sorted(cr["corn"].items())})

    # --- Run it: three seasons --------------------------------------------------------------------------------------
    mz = F["PMAIZMTUSDM"]
    seasons = []
    for y in (2012, 2014, 2020):
        d = cr["corn"][y]
        past = np.array([[yy, cr["corn"][yy]["Yield"]] for yy in range(y - 10, y)])
        b, a = np.polyfit(past[:, 0], past[:, 1], 1)
        expected = float(b * y + a)
        ph = d["Price"]
        pp = ph * mz[f"{y}-04"] / mz[f"{y}-10"]
        pl = ph * mz[f"{y + 1}-06"] / mz[f"{y}-10"]
        outs = {}
        for h in (0.0, 0.5, 1.0):
            for s_ in (0.0, 1.0):
                rev = farm.sell(expected, d["Yield"], pp, ph, pl, hedge=h, store=s_)
                outs[f"h{int(100 * h)}_s{int(s_)}"] = rev - d["Total, costs listed"]
        seasons.append(dict(year=y, expected=expected, actual=d["Yield"], plant=pp, harvest=ph, later=pl,
                            cost=d["Total, costs listed"], outcomes=outs))
    totals = {k: sum(s["outcomes"][k] for s in seasons) for k in seasons[0]["outcomes"]}
    R["run"] = dict(seasons=seasons, totals=totals, best=max(totals, key=totals.get), worst=min(totals, key=totals.get),
                    carry=0.04, months=8)

    # --- the treadmill --------------------------------------------------------------------------------------------------
    T = farm.treadmill()
    mya = _annual(mz)
    # the BLS published no CPI for October 2025 (the federal shutdown): average the months it did publish
    real_mz = {y: farm.per_bushel(v, "corn") * cpi[cpi_last] /
               np.mean([cpi[f"{y}-{m:02d}"] for m in range(1, 13) if f"{y}-{m:02d}" in cpi])
               for y, v in mya.items()}
    R["treadmill"] = dict(model={k: v.tolist() for k, v in T.items()}, us_maize=dict(sorted(ow["maize-yields"]["United States"].items())),
                          real_maize=dict(sorted(real_mz.items())), cpi_month=cpi_last,
                          farms_1935=get("ers.farms.1935"), farms_2025=get("nass.farms.2025") / 1000,
                          acres_1935=get("ers.acres.1935"), acres_2025=get("nass.acres.2025"))
    um = R["treadmill"]["us_maize"]
    R["treadmill"]["maize_x"] = um[max(um)] / um[1961]
    R["treadmill"]["before"] = float(np.mean([v for y, v in um.items() if 1866 <= y <= 1935]))
    R["treadmill"]["maize_x30"] = um[max(um)] / R["treadmill"]["before"]
    R["treadmill"]["maize_last"] = (max(um), um[max(um)])

    # --- a bushel to a loaf ---------------------------------------------------------------------------------------------
    wh = F["PWHEAMTUSDM"]
    br = F["APU0000702111"]
    months = sorted(set(wh) & set(br))
    loaf = {m: farm.per_bushel(wh[m], "wheat") / get("kswheat.loaves") for m in months}
    lm = months[-1]
    R["bread"] = dict(month=lm, wheat_bu=farm.per_bushel(wh[lm], "wheat"), wheat_loaf=loaf[lm], bread=br[lm],
                      share=loaf[lm] / br[lm], months=months, loaf=[loaf[m] for m in months], price=[br[m] for m in months],
                      peak=max(months, key=lambda m: loaf[m]), flour=get("kswheat.flour"), loaves=get("kswheat.loaves"))
    R["bread"]["peak_share"] = loaf[R["bread"]["peak"]] / br[R["bread"]["peak"]]

    # --- the companies ------------------------------------------------------------------------------------------------
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_annual"):
        sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    names = {"CTVA": ("Corteva", "seed and crop chemicals"), "DE": ("Deere", "machinery"), "CF": ("CF Industries", "nitrogen fertilizer"),
             "MOS": ("Mosaic", "phosphate and potash"), "ADM": ("ADM", "grain trading and processing"),
             "BG": ("Bunge", "grain trading and processing"), "TSN": ("Tyson Foods", "meat"), "PPC": ("Pilgrim's Pride", "chicken"),
             "HRL": ("Hormel", "meat and brands"), "PEP": ("PepsiCo", "snacks and drinks"), "MDLZ": ("Mondelez", "chocolate and biscuits"),
             "GIS": ("General Mills", "cereal and baking"), "KHC": ("Kraft Heinz", "packaged food"), "HSY": ("Hershey", "chocolate"),
             "KR": ("Kroger", "supermarkets"), "WMT": ("Walmart", "supermarkets and general retail"), "COST": ("Costco", "warehouse clubs")}

    def latest(t, upto=2025):
        ys = [y for y in sec[t] if y <= upto and sec[t][y]["revenue"] and sec[t][y]["net_income"] is not None]
        y = max(ys)
        return y, sec[t][y]["revenue"], sec[t][y]["net_income"]

    def avg_margin(t, y0=2021, y1=2025):
        vals = [sec[t][y]["net_income"] / sec[t][y]["revenue"] for y in range(y0, y1 + 1)
                if y in sec[t] and sec[t][y]["revenue"] and sec[t][y]["net_income"] is not None]
        return float(np.mean(vals)), len(vals)
    ladder = []
    for t, (n, what) in names.items():
        y, rev, ni = latest(t)
        m5, k = avg_margin(t)
        ladder.append(dict(ticker=t, name=n, what=what, year=y, revenue=rev, net=ni, margin=ni / rev, margin5=m5, years5=k))
    corn_m = [netop for netop in []]
    del corn_m
    corn5 = [cr["corn"][y]["Value of production less total costs listed"] / cr["corn"][y]["Total, gross value of production"]
             for y in range(2021, 2026)]
    R["chain"] = dict(companies=sorted(ladder, key=lambda q: q["margin5"]), corn=c25["Value of production less total costs listed"] /
                      c25["Total, gross value of production"], corn5=float(np.mean(corn5)))

    # --- inputs -------------------------------------------------------------------------------------------------------
    ppi = F["PCU325311325311"]
    R["inputs"] = dict(fert=R["acre"]["fert"], seed=R["acre"]["seed"], ppi={m: v for m, v in sorted(ppi.items()) if m >= "2000"},
                       cf={y: (sec["CF"][y]["revenue"], sec["CF"][y]["net_income"]) for y in range(2015, 2026) if y in sec["CF"]},
                       ctva={y: (sec["CTVA"][y]["revenue"], sec["CTVA"][y]["net_income"]) for y in range(2019, 2026) if y in sec["CTVA"]},
                       de={y: (sec["DE"][y]["revenue"], sec["DE"][y]["net_income"]) for y in range(2015, 2026) if y in sec["DE"]})
    R["inputs"]["ppi_peak"] = max(R["inputs"]["ppi"], key=R["inputs"]["ppi"].get)

    # --- the traders ---------------------------------------------------------------------------------------------------
    R["traders"] = dict(adm={y: (sec["ADM"][y]["revenue"], sec["ADM"][y]["net_income"]) for y in sorted(sec["ADM"]) if y >= 2010},
                        bg={y: (sec["BG"][y]["revenue"], sec["BG"][y]["net_income"]) for y in sorted(sec["BG"])},
                        cargill=get("cargill.revenue.2025"))
    adm = R["traders"]["adm"]
    R["traders"]["adm_margin"] = float(np.mean([n / r for y, (r, n) in adm.items() if y >= 2016]))

    # the soybean crush: what a tonne of beans is worth as meal and oil, less the beans (the exchange's standard yields)
    sm, so, sb = F["PSMEAUSDM"], F["PSOILUSDM"], F["PSOYBUSDM"]  # meal, oil, beans
    cm = sorted(set(sm) & set(so) & set(sb))
    fo, fm = get("cme.crush.oil") / 60, get("cme.crush.meal") / 60
    crush = {m: fm * sm[m] + fo * so[m] - sb[m] for m in cm}
    R["traders"]["crush"] = dict(months=cm, margin=[crush[m] for m in cm], oil=fo, meal=fm,
                                 avg=float(np.mean(list(crush.values()))), last=crush[cm[-1]], last_month=cm[-1],
                                 neg=sum(1 for v in crush.values() if v < 0) / len(crush))

    # --- futures: maize month by month ------------------------------------------------------------------------------------
    R["futures"] = dict(months=sorted(mz), bu=[farm.per_bushel(mz[m], "corn") for m in sorted(mz)])

    # --- meat -------------------------------------------------------------------------------------------------------------
    R["meat"] = dict(cr4=get("ers.beef.cr4"), cr4_1980=get("ers.beef.cr4.1980"),
                     tsn={y: (sec["TSN"][y]["revenue"], sec["TSN"][y]["net_income"]) for y in sorted(sec["TSN"]) if y >= 2012},
                     ppc={y: (sec["PPC"][y]["revenue"], sec["PPC"][y]["net_income"]) for y in sorted(sec["PPC"]) if y >= 2012},
                     beef={m: v for m, v in sorted(F["PBEEFUSDM"].items())},
                     ground_beef={m: v for m, v in sorted(F["APU0000703112"].items()) if m >= "2000"})

    # --- farm income and the state -----------------------------------------------------------------------------------
    fi: dict = collections.defaultdict(dict)
    defl = {}
    for r in read("ers_farm_income"):
        rate = r["variable"].startswith(("Rate of return", "Net farm income ratio"))
        fi[r["variable"]][int(r["year"])] = r["value_kusd"] if rate else r["value_kusd"] / 1e6
        if r["gdp_deflator"]:
            defl[int(r["year"])] = r["gdp_deflator"]
    nfi = fi["Net farm income"]
    gov = fi["Value of government payments, total"]
    # ERS's GDP deflator starts in 1929, so the real series do too
    R["income"] = dict(nominal=dict(sorted(nfi.items())), real={y: v * 100 / defl[y] for y, v in sorted(nfi.items()) if y in defl},
                       gov_real={y: v * 100 / defl[y] for y, v in sorted(gov.items()) if y in defl},
                       gov_share={y: gov[y] / nfi[y] for y in sorted(gov) if nfi.get(y, 0) > 0})
    inc = R["income"]
    R["income"].update(peak=max(inc["real"], key=inc["real"].get), y2026=nfi[2026], gov2026=gov[2026], gov2025=gov[2025],
                       y2025=nfi[2025], y2022=nfi[2022], y1910=nfi[1910])
    re_ = fi["Dec. 31 value of real estate assets, excl. operator dwellings"]
    ret: dict = {}
    for k in ("current income", "capital gains", "total"):
        ret[k] = fi[f"Rate of return on farm assets, {k}"]
    R["land"] = dict(real={y: v * 100 / defl[y] for y, v in sorted(re_.items()) if y in defl}, nominal=dict(sorted(re_.items())),
                     ret_income=dict(sorted(ret["current income"].items())), ret_gains=dict(sorted(ret["capital gains"].items())),
                     rent=dict(sorted(fi["Net rent, nonoperator landlords, incl. capital consumption"].items())))
    ri = R["land"]["ret_income"]
    rg = R["land"]["ret_gains"]
    R["land"]["avg_income"] = float(np.mean([v for y, v in ri.items() if y >= 1990]))
    R["land"]["avg_gains"] = float(np.mean([v for y, v in rg.items() if y >= 1990]))
    R["land"]["acre_value"] = re_[2025] * 1e9 / (get("nass.land.2025") * 1e6)

    # --- cocoa, rice, calories ----------------------------------------------------------------------------------------
    co = F["PCOCOUSDM"]
    R["cocoa"] = dict(months=sorted(co), price=[co[m] for m in sorted(co)], peak=max(co, key=co.get), peak_val=max(co.values()),
                      last=co[max(co)], last_month=max(co), y2022=_annual(co)[2022],
                      civ=get("icco.civ.2023"), gha=get("icco.gha.2023"), world=get("icco.world.2023"),
                      civ24=get("icco.civ.2024"), gha24=get("icco.gha.2024"), world24=get("icco.world.2024"),
                      hsy={y: (sec["HSY"][y]["revenue"], sec["HSY"][y]["net_income"]) for y in range(2019, 2026)},
                      mdlz={y: (sec["MDLZ"][y]["revenue"], sec["MDLZ"][y]["net_income"]) for y in range(2019, 2026)})
    R["cocoa"]["share"] = (R["cocoa"]["civ"] + R["cocoa"]["gha"]) / R["cocoa"]["world"]
    rc = F["PRICENPQUSDM"]
    R["rice"] = dict(months=sorted(rc), price=[rc[m] for m in sorted(rc)], before=rc["2023-06"], peak=max((m for m in rc if "2023" <= m <= "2024-12"), key=rc.get),
                     ban=get("india.rice.ban"), last=rc[max(rc)], last_month=max(rc))
    R["rice"]["peak_val"] = rc[R["rice"]["peak"]]
    cal = ow["daily-per-capita-caloric-supply"]
    R["calories"] = {e: {y: v for y, v in sorted(cal[e].items()) if y >= 1961}
                     for e in ("World", "India", "China", "Africa", "United States") if e in cal}

    # --- the call ---------------------------------------------------------------------------------------------------
    fs = R["dollar"]["series"]["All"]
    R["call"] = dict(threshold=13.0, prob=0.70, last=fs[last], since2016=(min(v for y, v in fs.items() if y >= 2016),
                                                                         max(v for y, v in fs.items() if y >= 2016)),
                     due="2027-12")
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    h = R["hook"]
    print("wheat yields x since 1961:", {k: round(h[f'{k}_x'], 1) for k in ("Mexico", "India", "Pakistan", "World")})
    d = R["dollar"]
    print(f"food dollar {d['year']}: farm {d['farm']} (home {d['home']}, away {d['away']}); spend ${d['spend']:.0f}bn; groups {d['groups']}")
    a = R["acre"]
    print(f"corn acre 2025: revenue {a['revenue']}, operating {a['op_total']}, overhead {a['oh_total']}, net {a['net']}, "
          f"breakeven ${a['breakeven']:.2f} (operating ${a['breakeven_op']:.2f}); losing years {a['losing_years']} of {a['n_years']}")
    for s in R["run"]["seasons"]:
        print(s["year"], f"expected {s['expected']:.0f} actual {s['actual']:.0f} plant {s['plant']:.2f} harvest {s['harvest']:.2f} "
              f"later {s['later']:.2f}", {k: round(v) for k, v in s["outcomes"].items()})
    print("run totals", {k: round(v) for k, v in R["run"]["totals"].items()})
    t = R["treadmill"]
    print(f"US maize x{t['maize_x']:.1f} since 1961; real maize {[(y, round(v, 2)) for y, v in t['real_maize'].items() if y % 5 == 0]}")
    b = R["bread"]
    print(f"bread {b['month']}: wheat ${b['wheat_bu']:.2f}/bu, {100 * b['wheat_loaf']:.1f}c a loaf, bread ${b['bread']:.2f} "
          f"({100 * b['share']:.1f}%); peak {b['peak']} {100 * b['peak_share']:.1f}%")
    print("ladder:", [(c["name"], round(100 * c["margin5"], 1)) for c in R["chain"]["companies"]], "corn", round(100 * R["chain"]["corn5"], 1))
    i = R["income"]
    print(f"net farm income 2022 {i['y2022']:.1f}, 2025 {i['y2025']:.1f}, 2026F {i['y2026']:.1f}; gov 2025 {i['gov2025']:.1f}, 2026 {i['gov2026']:.1f}; real peak {i['peak']}")
    l_ = R["land"]
    print(f"land: real estate 2025 ${l_['nominal'][2025]:.0f}bn = ${l_['acre_value']:.0f}/acre; returns since 1990: income {l_['avg_income']:.2f}%, gains {l_['avg_gains']:.2f}%")
    c = R["cocoa"]
    print(f"cocoa peak {c['peak']} ${c['peak_val']:.0f}, last ${c['last']:.0f}; CIV+GHA {100 * c['share']:.0f}%")
    rc = R["rice"]
    print(f"rice before ${rc['before']:.0f}, peak {rc['peak']} ${rc['peak_val']:.0f}, last ${rc['last']:.0f}")
    print("calories:", {e: (min(v), v[min(v)], max(v), v[max(v)]) for e, v in R["calories"].items()})
    print("call", R["call"])


if __name__ == "__main__":
    main()
