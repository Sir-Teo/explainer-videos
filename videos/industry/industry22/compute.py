"""Every number in Part 22 of *Industry, Built* ("Consumer Goods"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry22.compute        # prints the film's numbers; writes .cache/industry22/computed.json

Items:
    hook        Procter & Gamble: sales against the cost of the products sold; advertising; Walmart
    run         the Run it decision: hold, cut the advertising, or cut the price, against a store label (the Works)
    dollar      a dollar of P&G's sales
    margins     gross margins across the makers (SEC)
    ads         P&G's advertising since 2018, and advertising against sales across the makers
    retailer    the largest customer's share of sales
    bottler     Coca-Cola's concentrate and its bottlers
    pricing     P&G's sales growth split into volume, price, mix and currency, fiscal 2020-2026
    tobacco     Altria: volume against price, and the margin
    history     consumer prices of personal care, food and tobacco against all items (FRED)
    landscape   the companies by revenue and margin
    called      P&G's organic sales guidance against outcomes; this series' call
"""

from __future__ import annotations

import collections
import datetime as dt
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import brand

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry22"

NAMES = {"PG": ("Procter & Gamble", "home"), "CL": ("Colgate-Palmolive", "home"), "KMB": ("Kimberly-Clark", "home"),
         "CLX": ("Clorox", "home"), "CHD": ("Church & Dwight", "home"), "EL": ("Estee Lauder", "home"),
         "KO": ("Coca-Cola", "drink"), "PEP": ("PepsiCo", "drink"), "KDP": ("Keurig Dr Pepper", "drink"),
         "MNST": ("Monster", "drink"), "COKE": ("Coca-Cola Consolidated", "drink"), "STZ": ("Constellation", "drink"),
         "BF-B": ("Brown-Forman", "drink"), "BUD": ("AB InBev", "drink"), "MDLZ": ("Mondelez", "food"),
         "GIS": ("General Mills", "food"), "HSY": ("Hershey", "food"), "CAG": ("Conagra", "food"), "CPB": ("Campbell's", "food"),
         "SJM": ("J.M. Smucker", "food"), "KHC": ("Kraft Heinz", "food"), "MO": ("Altria", "tobacco"),
         "PM": ("Philip Morris International", "tobacco")}


def _fy(end: str) -> int:
    d = dt.date.fromisoformat(str(end)[:10])
    return d.year - 1 if d.month == 1 and d.day <= 7 else d.year


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_consumer"):
        # a revenue below the cost of sales is a narrower tag (General Mills tags a part of its sales as Revenues)
        if r.get("revenue") and r["revenue"] > 0 and not (r.get("cost") and r["cost"] > r["revenue"]):
            sec[r["ticker"]][_fy(r["year_end"])] = r
    fred: dict = collections.defaultdict(dict)
    for r in read("fred_consumer"):
        fred[r["series"]][str(r["month"])] = r["value"]

    def margins(tk, start=2021, end=2025):
        return {y: r["profit"] / r["revenue"] for y, r in sec[tk].items() if r.get("profit") is not None and start <= y <= end}

    pg26 = sec["PG"][2026]
    R["hook"] = dict(sales=get("pg.sales"), cost=pg26["cost"], ratio=pg26["revenue"] / pg26["cost"], ads=get("pg.ads.2026"),
                     walmart=get("pg.walmart"), gm=get("pg.gm"), top10=get("pg.top10"))

    b = brand.Brand()
    ch = b.choices()
    R["run"] = dict(choices={k: dict(npv=v["npv"], rows=v["rows"]) for k, v in ch.items()}, units=b.units, price=b.price,
                    store=b.store_price, cost=b.unit_cost, ads=b.ads, decay=b.decay, target=b.target)

    sales = pg26["revenue"]
    gm, opm = get("pg.gm") / 100, get("pg.opm") / 100
    R["dollar"] = dict(make=1 - gm, ads=get("pg.ads.2026") / sales, other=gm - get("pg.ads.2026") / sales - opm, op=opm,
                       net=pg26["profit"] / sales, rnd=get("pg.rnd") / sales)

    gms = {}
    for tk in ("KO", "PM", "CL", "MNST", "PEP", "PG", "BF-B", "CHD", "CLX", "COKE", "KMB", "HSY", "GIS", "MDLZ"):
        r = sec[tk][max(sec[tk])]
        if r.get("cost"):
            gms[NAMES[tk][0]] = 1 - r["cost"] / r["revenue"]
    R["margins"] = dict(gm=gms)

    ads = {y: get(f"pg.ads.{y}") for y in range(2018, 2027)}
    pgs = {y: get(f"pg.sales.{y}") / 1e3 for y in range(2020, 2025)}
    pgs.update({y: sec["PG"][y]["revenue"] for y in (2025, 2026)})
    adshare = {}
    for tk in ("CL", "PG", "CHD", "KO", "CLX", "BF-B", "STZ", "MNST", "HSY", "KMB", "MDLZ", "GIS", "PEP", "PM"):
        r = sec[tk][max(sec[tk])]
        if r.get("advertising"):
            adshare[NAMES[tk][0]] = r["advertising"] / r["revenue"]
    R["ads"] = dict(pg=ads, pg_sales=pgs, share=adshare, pg_share={y: ads[y] / pgs[y] for y in pgs})

    R["retailer"] = dict(walmart={"Clorox": get("clx.walmart"), "Church & Dwight": get("chd.walmart"),
                                  "General Mills": get("gis.walmart"), "Procter & Gamble": get("pg.walmart"),
                                  "Kimberly-Clark": get("kmb.walmart"), "Colgate-Palmolive": get("cl.walmart")},
                         mclane=get("hsy.mclane"), top10=get("pg.top10"))

    ko, coke = sec["KO"][2025], sec["COKE"][2025]
    R["bottler"] = dict(cases=get("ko.cases"), conc_rev=get("ko.conc.rev"), conc_vol=get("ko.conc.vol"),
                        coke_share=get("ko.coke.share"), ko_gm=1 - ko["cost"] / ko["revenue"],
                        coke_gm=1 - coke["cost"] / coke["revenue"], ko_margin=ko["profit"] / ko["revenue"],
                        coke_margin=coke["profit"] / coke["revenue"], ko_rev=ko["revenue"], coke_rev=coke["revenue"])

    keys = ("vol", "fx", "price", "mix", "other", "net")
    R["pricing"] = {y: {k: get(f"pg.drv.{y}.{k}") for k in keys} for y in range(2020, 2027)}

    R["growth"] = dict(seg={n: (get(f"pg.seg.{k}"), get(f"pg.seg.{k}.g")) for k, n in
                            (("beauty", "Beauty"), ("grooming", "Grooming"), ("health", "Health Care"),
                             ("fabric", "Fabric & Home Care"), ("baby", "Baby, Feminine & Family Care"))},
                       colgate_em=get("cl.abroad"))
    R["tobacco"] = dict(vol=get("mo.vol"), fall=get("mo.vol.fall"), price=get("mo.price"), volfx=get("mo.volfx"),
                        margin=get("mo.margin"), share=get("mo.share"), discount=get("mo.discount"))

    cpi = _annual(fred["CPIAUCNS"], need=11)  # the BLS published no October 2025 CPI
    ser = {"personal care": _annual(fred["CUUR0000SAG1"], need=11), "food at home": _annual(fred["CUUR0000SAF11"], need=11),
           "tobacco": _annual(fred["CUUR0000SEGA"], need=11)}
    base = 1990
    R["history"] = dict(rel={k: {y: (v[y] / v[base]) / (cpi[y] / cpi[base]) for y in v if y in cpi and y >= base}
                             for k, v in ser.items()}, base=base,
                        x={k: v[2025] / v[base] for k, v in ser.items()}, cpi_x=cpi[2025] / cpi[base],
                        infl={k: v[2023] / v[2020] - 1 for k, v in dict(ser, all=cpi).items()})

    comp = []
    for tk, (nm, grp) in NAMES.items():
        if not sec[tk] or max(sec[tk]) < 2025:  # Kraft Heinz and Smucker tag no total revenue in recent years
            continue
        r = sec[tk][max(sec[tk])]
        mm = list(margins(tk).values())
        comp.append(dict(name=nm, group=grp, rev=r["revenue"], margin=float(np.median(mm)) if mm else r["profit"] / r["revenue"],
                         fy=max(sec[tk])))
    R["landscape"] = dict(companies=comp)

    R["extra"] = dict(hsy_gm=(get("hsy.gm.2024"), get("hsy.gm.2025")), hsy_price=get("hsy.price"), gis_trade=get("gis.trade"),
                      gis_vol=get("gis.vol"), chd_top4=get("chd.top4"),
                      pm_sf={y: get(f"pm.sf.{y}") for y in (2023, 2024, 2025)}, pm_total=sec["PM"][2025]["revenue"],
                      pm_markets=get("pm.markets"), mnst={y: sec["MNST"][y]["revenue"] for y in sorted(sec["MNST"]) if y >= 2012},
                      mnst_gm=1 - sec["MNST"][2025]["cost"] / sec["MNST"][2025]["revenue"],
                      servings_day=get("ko.cases") * 1e9 * 24 / 365,
                      profit_serving=100 * sec["KO"][2025]["profit"] * 1e9 / (get("ko.cases") * 1e9 * 24),
                      pg_seg_share={n: get(f"pg.segshare.{k}") for k, n in
                                    (("fabric", "Fabric & Home Care"), ("baby", "Baby, Feminine & Family Care"),
                                     ("beauty", "Beauty"), ("health", "Health Care"), ("grooming", "Grooming"))}, rnd=get("pg.rnd"), ads=get("pg.ads.2026"))
    R["called"] = dict(g25=(get("pg.guide25.lo"), get("pg.guide25.hi")), a25=get("pg.organic.2025"), g26=(get("pg.guide26.lo"), get("pg.guide26.hi")), a26=get("pg.organic"),
                       g27=(get("pg.guide27.lo"), get("pg.guide27.hi")), q1=get("pg.q1fy27"), prob=0.40)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("hook", R["hook"])
    for k, v in R["run"]["choices"].items():
        print("run", k, round(v["npv"]), [round(r["profit"]) for r in v["rows"]], round(100 * v["rows"][-1]["share"], 1))
    print("dollar", {k: round(100 * v, 1) for k, v in R["dollar"].items()})
    print("gm", {k: round(100 * v) for k, v in R["margins"]["gm"].items()})
    print("ads", R["ads"]["pg"], {k: round(100 * v, 1) for k, v in R["ads"]["share"].items()})
    print("bottler", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in R["bottler"].items()})
    print("pricing", R["pricing"])
    h = R["history"]
    print("history x", {k: round(v, 2) for k, v in h["x"].items()}, round(h["cpi_x"], 2), "2020-23", {k: round(100 * v, 1) for k, v in h["infl"].items()})
    print("landscape", [(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]])
    print("called", R["called"])


if __name__ == "__main__":
    main()
