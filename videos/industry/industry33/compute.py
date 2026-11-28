"""Every number in Part 33 of *Industry, Built* ("The Middlemen"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry33.compute        # prints the film's numbers; writes .cache/industry33/computed.json

Items:
    hook        the three drug wholesalers against the largest drug maker; a Japanese trading house
    run         the Run it distributor: stock and service, working capital, drop-shipping and routes (the Works)
    does        what a wholesaler does: the networks behind it
    returns     margins, working-capital days, and margin times turns, across distributors
    kinds       four kinds of middlemen: what each keeps of a dollar
    traffic     the intermission's series: American wholesale sales, inventories, jobs and margins
    power       buying alliances, pass-through drugs and the opioid settlements
    trading     the trading house and the crop traders
    online      the internet and the distributor: Grainger's two models
    landscape   the companies by revenue and margin
    called      Chemdex's prospectus against Ventro's shutdown; this series' call on Mitsui
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import distributor as dw

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry33"

NAMES = {"MCK": ("McKesson", "drugs"), "COR": ("Cencora", "drugs"), "CAH": ("Cardinal Health", "drugs"),
         "HSIC": ("Henry Schein", "drugs"), "OMI": ("Owens & Minor", "drugs"), "SYY": ("Sysco", "food"),
         "USFD": ("US Foods", "food"), "PFGC": ("Performance Food", "food"), "UNFI": ("UNFI", "food"),
         "CHEF": ("Chefs' Warehouse", "food"), "ARW": ("Arrow", "tech"), "AVT": ("Avnet", "tech"), "SNX": ("TD Synnex", "tech"),
         "SCSC": ("ScanSource", "tech"), "CDW": ("CDW", "tech"), "WCC": ("WESCO", "industrial"), "GWW": ("Grainger", "industrial"),
         "FAST": ("Fastenal", "industrial"), "MSM": ("MSC Industrial", "industrial"), "AIT": ("Applied Industrial", "industrial"),
         "GIC": ("Global Industrial", "industrial"), "GPC": ("Genuine Parts", "industrial"), "CNM": ("Core & Main", "industrial"),
         "WSO": ("Watsco", "industrial"), "POOL": ("Pool Corp", "industrial"), "SITE": ("SiteOne", "industrial"),
         "BG": ("Bunge", "crops"), "ADM": ("ADM", "crops"), "ANDE": ("Andersons", "crops")}


def _monthly(rows: list) -> dict:
    by: dict = collections.defaultdict(dict)
    for r in rows:
        by[r["series"]][str(r["month"])] = r["value"]
    return by


def _ym(p: str) -> float:
    return int(p[:4]) + (int(p[5:7]) - 0.5) / 12


def _fy(end: str) -> int:
    y, m = int(end[:4]), int(end[5:7])
    return y - 1 if m <= 3 else y


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_middle"):
        if r.get("revenue"):
            sec[r["ticker"]][_fy(str(r["year_end"]))] = r
    f = _monthly(read("fred_middle"))
    last = {t: max(d) for t, d in sec.items()}

    def g(t, item, y=None):
        y = last[t] if y is None else y
        return sec[t][y].get(item) if y in sec[t] else None

    # the hook
    pharma = {}
    for r in read("sec_pharma"):
        if r.get("revenue") and r["currency"] == "USD":
            t = r["ticker"]
            if t not in pharma or str(r["year_end"]) > pharma[t][0]:
                pharma[t] = (str(r["year_end"]), r["revenue"])
    top_maker = max(pharma, key=lambda t: pharma[t][1])
    fx = get("mi33.fx")
    big3 = {t: dict(rev=g(t, "revenue"), ni=g(t, "profit"), end=str(sec[t][last[t]]["year_end"])[:10]) for t in ("MCK", "COR", "CAH")}
    R["hook"] = dict(big3=big3, big3_rev=sum(v["rev"] for v in big3.values()), big3_ni=sum(v["ni"] for v in big3.values()),
                     maker=top_maker, maker_rev=pharma[top_maker][1],
                     mitsui_rev=get("mi33.rev") / fx, mitsui_ni=get("mi33.profit") / fx,
                     mck_hist={y: (sec["MCK"][y]["revenue"], sec["MCK"][y]["profit"]) for y in sorted(sec["MCK"]) if y >= 2010})

    # Run it: a distributor with McKesson's margins and payment terms
    rv, c, op = g("MCK", "revenue"), g("MCK", "cost"), g("MCK", "operating_income")
    gm = 1 - c / rv
    D = dw.Distributor(sales=get("wk33.sales") * 1e6, gm=gm, opex=gm - op / rv, lead=get("wk33.lead"), review=get("wk33.review"),
                       cv=get("wk33.cv"), loss=get("wk33.loss"), recv=g("MCK", "receivables") / rv * 365,
                       pay=g("MCK", "payables") / c * 365, wacc=get("wk33.wacc"), drop_keep=get("wk33.dropkeep"),
                       drop_gm=get("wk33.dropgm"))
    zs = [round(x, 2) for x in np.linspace(0.5, 3.5, 31)]
    best = D.best_z()
    Rt = dw.Route(cost=get("wk33.route"), drops=get("wk33.drop"), density=get("wk33.density"))
    shares = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6]
    R["run"] = dict(gm=gm, opex=D.opex, recv=D.recv, pay=D.pay, sales=D.sales, base=D.year(), by_z={z: D.year(z) for z in zs},
                    best_z=best, best=D.year(best), full=D.year(3.5), drop=D.drop_ship(), mck_inv_days=g("MCK", "inventory") / c * 365,
                    route={s: dict(stops=Rt.stops(s), cps=Rt.cost_per_stop(s), share=Rt.cost_share(s)) for s in shares},
                    route_cost=Rt.cost, route_drop=Rt.drops)

    # margins, days and returns
    marg, days = {}, {}
    for t in ("MCK", "COR", "CAH", "SYY", "USFD", "PFGC", "ARW", "AVT", "SNX", "WCC", "GWW", "FAST", "BG", "ADM"):
        rv_, c_, op_, ni_ = g(t, "revenue"), g(t, "cost"), g(t, "operating_income"), g(t, "profit")
        marg[NAMES[t][0]] = dict(gross=100 * (1 - c_ / rv_), op=100 * op_ / rv_ if op_ is not None else None, net=100 * ni_ / rv_,
                                 rev=rv_, turns=rv_ / g(t, "assets"), fy=last[t])
        inv, rec, ap = g(t, "inventory"), g(t, "receivables"), g(t, "payables")
        if inv and rec and ap:
            days[NAMES[t][0]] = dict(inv=inv / c_ * 365, rec=rec / rv_ * 365, pay=ap / c_ * 365,
                                     capital=inv + rec - ap, wc_days=inv / c_ * 365 + rec / rv_ * 365 - ap / c_ * 365)
    R["returns"] = dict(margins=marg, days=days)

    # what a wholesaler does
    R["does"] = dict(sysco=get("sy33.dcs"), usf_cust=get("us33.cust"), usf_trucks=get("us33.trucks"), usf_dcs=get("us33.dcs"),
                     gww_stocked=get("gw33.stocked"), gww_cust=get("gw33.cust"), mck_dcs=get("mk33.dcs"), mck_emp=get("mk33.emp"))

    # four kinds
    R["kinds"] = {k: marg[k] for k in ("McKesson", "Sysco", "Arrow", "Grainger", "Fastenal")}

    # the intermission
    sales = f["WHLSLRSMSA"]
    ann = collections.defaultdict(list)
    for m, v in sales.items():
        ann[int(m[:4])].append(v)
    R["traffic"] = dict(sales={y: 12 * np.mean(v) / 1e6 for y, v in ann.items() if len(v) == 12},
                        ratio={_ym(m): v for m, v in f["WHLSLRIRSA"].items()},
                        jobs={_ym(m): v for m, v in f["USWTRADE"].items() if m >= "1990-01"},
                        drugs={y: 12 * np.mean([v for m, v in f["S4242SM144SCEN"].items() if m.startswith(str(y))]) / 1e6
                               for y in range(1992, 2026)},
                        ppi_d={_ym(m): v for m, v in f["PCU423423"].items()}, ppi_n={_ym(m): v for m, v in f["PCU424424"].items()},
                        cpi={_ym(m): v for m, v in f["CPIAUCNS"].items() if m >= "2004-06"})

    # buying power and its costs
    R["power"] = dict(cvs=get("mk33.cvs"), next2=get("mk33.next2"), top10=get("mk33.top10"), wag=get("co33.wag"),
                      evernorth=get("co33.evernorth"), top5=get("co33.top5"), supp=get("co33.supp"), glp1=get("co33.glp1"),
                      opioid=get("mk33.opioid"), nosa=get("ca33.nosa"))

    # the trading house and the crop traders
    cf = {"metals and mines": get("mi33.cf.mm"), "energy": get("mi33.cf.en"), "machinery and infrastructure": get("mi33.cf.mi"),
          "chemicals": get("mi33.cf.ch"), "innovation and corporate": get("mi33.cf.ic"), "iron and steel products": get("mi33.cf.is"),
          "lifestyle (food, retail, health)": get("mi33.cf.li")}
    R["trading"] = dict(rev=get("mi33.rev"), gp=get("mi33.gp"), equity=get("mi33.equity"), div=get("mi33.div"), profit=get("mi33.profit"),
                        cf=cf, cf_total=get("mi33.cf.total"), fx=fx, bunge=marg["Bunge"], adm=marg["ADM"])

    # online
    ea_gp = get("gw33.ea.sales") - get("gw33.ea.cogs")
    R["online"] = dict(ht=dict(sales=get("gw33.ht.sales"), gm=100 * get("gw33.ht.gp") / get("gw33.ht.sales"),
                               om=100 * get("gw33.ht.op") / get("gw33.ht.sales")),
                       ea=dict(sales=get("gw33.ea.sales"), gm=100 * ea_gp / get("gw33.ea.sales"), om=100 * get("gw33.ea.op") / get("gw33.ea.sales")),
                       zoro=get("gw33.zoro"), monotaro=get("gw33.monotaro"), stocked=get("gw33.stocked"))

    # landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        if tk not in sec:
            continue
        ys = sorted(sec[tk])
        y = ys[-1]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in ys if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=sec[tk][y]["revenue"], margin=float(np.median(mm)), fy=y, tk=tk))
    comp.append(dict(name="Mitsui & Co.", group="trading", rev=get("mi33.rev") / fx, margin=get("mi33.profit") / get("mi33.rev"),
                     fy=2025, tk="MITSUI"))
    R["landscape"] = dict(companies=comp)

    R["called"] = dict(q2rev=get("cd33.q2rev"), loss=get("cd33.loss"), fc=get("mi33.fc"), fc_may=get("mi33.fc.may"),
                       h1=get("mi33.h1"), prev=get("mi33.profit"), prob=0.55)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("hook", {k: v for k, v in H.items() if k != "mck_hist"})
    U = R["run"]
    pk = lambda s: {k: (round(v / 1e6, 1) if abs(v) > 1e4 else round(v, 4)) for k, v in s.items()}  # noqa: E731
    print("run gm/opex/recv/pay", round(U["gm"], 4), round(U["opex"], 4), round(U["recv"], 1), round(U["pay"], 1), round(U["mck_inv_days"], 1))
    print("base", pk(U["base"]))
    print("best", U["best_z"], pk(U["best"]))
    print("full", pk(U["full"]))
    print("drop", pk(U["drop"]))
    print("route", {s: {k: round(v, 3) for k, v in d.items()} for s, d in U["route"].items()})
    print("margins", {k: {a: (round(b, 2) if isinstance(b, float) else b) for a, b in v.items()} for k, v in R["returns"]["margins"].items()})
    print("days", {k: {a: round(b, 1) for a, b in v.items()} for k, v in R["returns"]["days"].items()})
    T = R["traffic"]
    print("wholesale $trn", {y: round(v, 2) for y, v in T["sales"].items() if y in (1992, 2000, 2010, 2019, 2022, 2025)})
    print("drugs $bn", {y: round(v * 1e3) for y, v in T["drugs"].items() if y in (1992, 2000, 2010, 2025)})
    print("jobs", {k: v for k, v in T["jobs"].items() if int(k) in (1990, 2000, 2008, 2019, 2026) and (k % 1) < 0.1})
    print("trading", {k: v for k, v in R["trading"].items() if k not in ("bunge", "adm")})
    print("online", R["online"])
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 2), c["fy"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
