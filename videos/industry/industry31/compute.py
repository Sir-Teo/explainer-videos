"""Every number in Part 31 of *Industry, Built* ("Grocery and Mass Retail"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry31.compute        # prints the film's numbers; writes .cache/industry31/computed.json

Items:
    hook        Walmart's size and what it keeps; Costco's fees against its profit
    run         the Run it store: a year on a two per cent margin, priced and staffed (the Works)
    dollar      where a dollar at the till goes; gross and operating margins across the retailers
    turns       inventory days against payables days: the suppliers' float; margin times turns
    formats     supermarket, supercentre, club and dollar store: stores, space and sales
    club        Costco's membership economics
    traffic     the intermission's series: grocery sales, food prices, grocery jobs, e-commerce's share
    buy         buying power: suppliers' dependence on Walmart (Part 22's figures)
    merger      Kroger and Albertsons, blocked
    online      Kroger's automated warehouses; Amazon against Walmart
    landscape   the companies by revenue and margin
    called      Kroger's Ocado bet; this series' call on Costco's members
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import store

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry31"

NAMES = {"WMT": ("Walmart", "mass"), "COST": ("Costco", "club"), "KR": ("Kroger", "grocer"), "ACI": ("Albertsons", "grocer"),
         "TGT": ("Target", "mass"), "DG": ("Dollar General", "dollar"), "DLTR": ("Dollar Tree", "dollar"), "BJ": ("BJ's", "club"),
         "SFM": ("Sprouts", "grocer"), "WMK": ("Weis", "grocer"), "IMKTA": ("Ingles", "grocer"), "GO": ("Grocery Outlet", "grocer"),
         "CASY": ("Casey's", "convenience"), "FIVE": ("Five Below", "dollar"), "OLLI": ("Ollie's", "dollar"),
         "PSMT": ("PriceSmart", "club"), "VLGEA": ("Village", "grocer"), "NGVC": ("Natural Grocers", "grocer"),
         "AMZN": ("Amazon", "online")}


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


def _fy(end: str) -> int:
    """Fiscal year label: a year ending in January to March belongs to the previous calendar year."""
    y, m = int(end[:4]), int(end[5:7])
    return y - 1 if m <= 3 else y


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_grocery"):
        if r.get("revenue"):
            sec[r["ticker"]][_fy(str(r["year_end"]))] = r
    f = _monthly(read("fred_grocery"))
    last = {t: max(d) for t, d in sec.items()}

    def g(t, item, y=None):
        y = last[t] if y is None else y
        return sec[t][y].get(item) if y in sec[t] else None

    # the hook
    R["hook"] = dict(wmt_rev=g("WMT", "revenue"), wmt_ni=g("WMT", "profit"), assoc=get("wm31.assoc"),
                     cost_rev=g("COST", "revenue"), cost_ni=g("COST", "profit"), fees=get("co31.fees"),
                     wmt_hist={y: (sec["WMT"][y]["revenue"], sec["WMT"][y]["profit"]) for y in range(2010, last["WMT"] + 1) if y in sec["WMT"]})

    # Run it: the store
    S = store.Store(sales=get("wk31.sales") * 1e6, gm=1 - g("KR", "cost") / g("KR", "revenue"), labour=get("wk31.labour"),
                    occupancy=get("wk31.occupancy"), other=get("wk31.other"), elasticity=get("wk31.elasticity"))
    prices = [round(x, 3) for x in np.linspace(0.94, 1.06, 25)]
    staff = [round(x, 2) for x in np.linspace(0.75, 1.25, 21)]
    R["run"] = dict(base=S.year(), gm=S.gm, labour=S.labour, occupancy=S.occupancy, other=S.other, elasticity=S.elasticity,
                    sales=S.sales, by_price={p: S.year(p)["profit"] for p in prices}, by_staff={s: S.year(s=s)["profit"] for s in staff},
                    cut1=S.year(0.99), cut1_need=S.breakeven_volume(0.01), cut2_need=S.breakeven_volume(0.02),
                    staff80=S.year(s=0.8), staff120=S.year(s=1.2), best_price=S.best_price(),
                    drops={d: S.sales * (1 - d) * (S.gm - S.other) - S.sales * (S.labour + S.occupancy) for d in (0.0, 0.05, 0.1, 0.15)})

    # the dollar and margins
    marg = {}
    for t in ("COST", "WMT", "KR", "ACI", "TGT", "DG", "SFM", "BJ", "DLTR"):
        rv, c, op, ni = g(t, "revenue"), g(t, "cost"), g(t, "operating_income"), g(t, "profit")
        marg[NAMES[t][0]] = dict(gross=100 * (1 - c / rv) if c else None, op=100 * op / rv if op is not None else None,
                                 net=100 * ni / rv if ni is not None else None, rev=rv, fy=last[t])
    R["dollar"] = dict(wmt=dict(gp=get("wm31.gp"), opex=get("wm31.opex"), op=get("wm31.op"), sales=get("wm31.sales")), margins=marg)

    # turns and the float
    fl = {}
    for t in ("WMT", "COST", "TGT", "DG", "ACI", "AMZN"):
        inv, ap, c = g(t, "inventory"), g(t, "payables"), g(t, "cost")
        if inv and ap and c:
            fl[NAMES[t][0]] = store.float_days(inv, ap, c)
    roa = {NAMES[t][0]: dict(margin=100 * g(t, "profit") / g(t, "revenue"), turns=g(t, "revenue") / g(t, "assets"))
           for t in ("COST", "WMT", "KR", "TGT", "DG") if g(t, "assets")}
    R["turns"] = dict(float=fl, roa=roa)

    # formats
    R["formats"] = dict(wmt_us=(get("wm31.us.units"), get("wm31.us.sales"), get("wm31.us.sqft")),
                        cost=(get("co31.wh"), get("co31.sales"), get("co31.wh") * get("co31.sqft") / 1e6),
                        kr=(get("kr31.stores"), g("KR", "revenue")), aci=(get("aci31.stores"), g("ACI", "revenue")),
                        dg=(get("dg31.stores"), g("DG", "revenue")))

    # the club
    R["club"] = dict(fees=get("co31.fees"), members=(get("co31.members24"), get("co31.members25"), get("co31.members")),
                     renew=get("co31.renew"), renew_ww=get("co31.renew.ww"), ni=g("COST", "profit"), op=g("COST", "operating_income"),
                     sales=get("co31.sales"), gross=g("COST", "revenue") - g("COST", "cost"),
                     merch_margin=100 * (get("co31.sales") - g("COST", "cost")) / get("co31.sales"),
                     fees_hist={y: None for y in ()})

    # traffic
    groc = _annual(f["RSGCS"], need=12)
    food = _annual(f["CUUR0000SAF11"], need=11)
    cpi = _annual(f["CPIAUCNS"], need=11)
    R["traffic"] = dict(grocery={y: 12 * v / 1e3 for y, v in groc.items()},
                        food={_ym(m): v / f["CUUR0000SAF11"]["2019-12"] * 100 for m, v in f["CUUR0000SAF11"].items() if m >= "2015-01"},
                        cpi={_ym(m): v / f["CPIAUCNS"]["2019-12"] * 100 for m, v in f["CPIAUCNS"].items() if m >= "2015-01"},
                        food_a=food, cpi_a=cpi,
                        jobs={_ym(m): v for m, v in f["CES4244500001"].items() if m >= "2000-01"},
                        ecom={int(m[:4]) + (int(m[5:7]) - 1) / 12: v for m, v in f["ECOMPCTSA"].items()},
                        retail={_ym(m): v for m, v in f["USTRADE"].items() if m >= "2000-01"})

    # online: Amazon against Walmart
    R["online"] = dict(amzn={y: sec["AMZN"][y]["revenue"] for y in range(2015, last["AMZN"] + 1)},
                       wmt={y: sec["WMT"][y]["revenue"] for y in range(2015, last["WMT"] + 1)}, ocado=get("kr31.ocado"))

    # landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        ys = sorted(sec[tk])
        y = ys[-1]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in ys if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=sec[tk][y]["revenue"], margin=float(np.median(mm)), fy=y, tk=tk))
    R["landscape"] = dict(companies=comp)

    R["called"] = dict(line=87.0, prob=0.55, members=R["club"]["members"])
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("hook", {k: v for k, v in R["hook"].items() if k != "wmt_hist"})
    U = R["run"]
    print("run base", {k: round(v, 3) for k, v in U["base"].items()}, round(U["gm"], 4), U["cut1_need"], U["cut2_need"], U["best_price"])
    print("by price", {k: round(v / 1e6, 3) for k, v in U["by_price"].items()})
    print("by staff", {k: round(v / 1e6, 3) for k, v in U["by_staff"].items()})
    print("margins", {k: {a: (round(b, 1) if isinstance(b, float) else b) for a, b in v.items()} for k, v in R["dollar"]["margins"].items()})
    print("float", {k: {a: round(b, 1) for a, b in v.items()} for k, v in R["turns"]["float"].items()})
    print("roa", {k: {a: round(b, 2) for a, b in v.items()} for k, v in R["turns"]["roa"].items()})
    print("formats", R["formats"])
    print("club", {k: v for k, v in R["club"].items() if k != "fees_hist"})
    T = R["traffic"]
    print("grocery $bn", {y: round(v) for y, v in T["grocery"].items() if y in (2000, 2010, 2019, 2020, 2025)})
    print("food/cpi", {y: round(T["food_a"][y] / T["food_a"][2019], 3) for y in (2020, 2021, 2022, 2023, 2024, 2025)},
          {y: round(T["cpi_a"][y] / T["cpi_a"][2019], 3) for y in (2022, 2025)})
    print("ecom last", max(T["ecom"]), T["ecom"][max(T["ecom"])], "jobs last", T["jobs"][max(T["jobs"])])
    print("online", {y: (round(R["online"]["amzn"][y]), round(R["online"]["wmt"].get(y, 0))) for y in range(2019, 2026)})
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
