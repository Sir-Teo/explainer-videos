"""Every number in Part 36 of *Industry, Built* ("Software"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry36.compute        # prints the film's numbers; writes .cache/industry36/computed.json

Items:
    hook        Microsoft: revenue, the cost of a copy, the cloud, the backlog; its growth since 2009
    run         the Run it company: sales or product, a price rise, the unit economics (the Works)
    cost        where a software dollar goes, company by company
    licence     licence to subscription: Adobe's J-curve and the Works' version
    cohorts     cohorts, net retention, the backlog and billing in advance
    selling     Salesforce's sales cost and margin since 2009; growth plus margin across the industry
    traffic     the intermission's series: software investment, programmers' jobs, software prices
    platform    the platform layer: Microsoft's mix, self-serve against the field
    landscape   the companies by revenue and margin
    called      Salesforce's $50 billion target against its result; this series' call on Microsoft Cloud
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import saas as sw

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry36"

NAMES = {"MSFT": ("Microsoft", "platform"), "ORCL": ("Oracle", "platform"), "SAP": ("SAP", "apps"), "CRM": ("Salesforce", "apps"),
         "ADBE": ("Adobe", "apps"), "NOW": ("ServiceNow", "apps"), "WDAY": ("Workday", "apps"), "INTU": ("Intuit", "apps"),
         "ADSK": ("Autodesk", "design"), "CDNS": ("Cadence", "design"), "SNPS": ("Synopsys", "design"), "VEEV": ("Veeva", "apps"),
         "TYL": ("Tyler", "apps"), "HUBS": ("HubSpot", "apps"), "DOCU": ("DocuSign", "apps"), "ZM": ("Zoom", "apps"),
         "FRSH": ("Freshworks", "apps"), "BOX": ("Box", "apps"), "TEAM": ("Atlassian", "dev"), "GTLB": ("GitLab", "dev"),
         "SNOW": ("Snowflake", "data"), "DDOG": ("Datadog", "data"), "MDB": ("MongoDB", "data"), "DT": ("Dynatrace", "data"),
         "PLTR": ("Palantir", "data"), "TWLO": ("Twilio", "dev"), "NET": ("Cloudflare", "security"), "PANW": ("Palo Alto", "security"),
         "CRWD": ("CrowdStrike", "security"), "ZS": ("Zscaler", "security"), "OKTA": ("Okta", "security")}


def _monthly(rows: list) -> dict:
    by: dict = collections.defaultdict(dict)
    for r in rows:
        by[r["series"]][str(r["month"])] = r["value"]
    return by


def _ym(p: str) -> float:
    return int(p[:4]) + (int(p[5:7]) - 0.5) / 12


def _fy(end: str) -> int:
    """Fiscal years named for the calendar year in which most of them falls (a year to January 2026 is 2025)."""
    y, m = int(end[:4]), int(end[5:7])
    return y - 1 if m <= 4 else y


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    f = _monthly(read("fred_soft"))
    eur = {int(m_[:4]): v for m_, v in f["AEXUSEU"].items()}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_soft"):
        if not r.get("revenue"):
            continue
        y = _fy(str(r["year_end"]))
        if r["currency"] == "EUR":
            if y not in eur:
                continue
            r = {k: (v * eur[y] if isinstance(v, float) else v) for k, v in r.items()}
        sec[r["ticker"]][y] = r
    last = {t: max(d) for t, d in sec.items()}

    def g(t, item, y=None):
        y = last[t] if y is None else y
        return sec[t][y].get(item) if y in sec[t] else None

    # the hook
    ms = dict(rev=get("ms36.rev"), product=get("ms36.product"), service=get("ms36.service"), cost=get("ms36.cost"), rnd=get("ms36.rnd"), sm=get("ms36.sm"), cloud=get("ms36.cloud"), cloudgm=get("ms36.cloudgm"), rpo=get("ms36.rpo"), azure=get("ms36.azure"), seats=get("ms36.seats"), staff=get("ms36.staff"), pcost=get("ms36.pcost"), scost=get("ms36.scost"))
    ms["op"] = g("MSFT", "operating_income")
    ms["hist"] = {y: (sec["MSFT"][y]["revenue"], sec["MSFT"][y]["operating_income"]) for y in sorted(sec["MSFT"])}
    R["hook"] = ms

    # Run it
    W = sw.Saas(arr0=get("wk36.arr") * 1e6, gross_margin=get("wk36.gm"), churn=get("wk36.churn"), expansion=get("wk36.exp"),
                reps0=get("wk36.reps"), productivity=get("wk36.prod") * 1e6, rep_cost=get("wk36.repcost") * 1e6,
                market=get("wk36.market"), rnd0=get("wk36.rnd") * 1e6, product_scale=get("wk36.scale") * 1e6,
                product_decay=get("wk36.decay"))
    base = W.run(quarters=20)
    shares = [0.0, 0.25, 0.5, 0.75, 1.0]
    alloc = {s: W.run(extra=30e6, to_sales=s, quarters=20) for s in shares}
    price = {k: W.run(raise_at=k, quarters=20) for k in (None, 2)}
    churn_sens = {c: W.with_(churn=c).run(quarters=20)["arr"][-1] for c in (0.04, 0.08, 0.12, 0.16)}
    R["run"] = dict(churn_sens=churn_sens, company=dict(arr0=W.arr0, gm=W.gross_margin, churn=W.churn, expansion=W.expansion, reps=W.reps0,
                                 productivity=W.productivity, rep_cost=W.rep_cost, rnd=W.rnd0, ga=W.ga, ramp=W.ramp),
                    base=base, alloc=alloc, price=price, unit=W.unit_economics(), extra=30e6,
                    ltv={yrs: sum(W.gross_margin * (1 - W.churn + W.expansion) ** t / 1.1 ** t for t in range(yrs)) for yrs in (1, 3, 5, 10)},
                    cac=W.unit_economics()["sm"] / W.unit_economics()["new"])

    # where the dollar goes
    cost = {}
    for t in ("CRM", "ADBE", "NOW", "WDAY", "SNOW", "DDOG", "CRWD", "TEAM", "HUBS"):
        rv = g(t, "revenue")
        cost[NAMES[t][0]] = dict(rev=rv, cost=(g(t, "cost") or 0) / rv, rnd=(g(t, "rnd") or 0) / rv, sm=(g(t, "marketing") or 0) / rv,
                                 op=g(t, "operating_income") / rv, sbc=(g(t, "sbc") or 0) / rv, fy=last[t])
    cost["Adobe"]["rnd"] = None
    R["cost"] = dict(companies=cost, crm=dict(rev=get("cr36.rev"), sub=get("cr36.sub"), prof=get("cr36.prof"), cost=get("cr36.cost"), rnd=get("cr36.rnd"), sm=get("cr36.sm"), ga=get("cr36.ga"), restr=get("cr36.restr"), op=get("cr36.op")))

    # licence to subscription
    adh = {y: (sec["ADBE"][y]["revenue"], sec["ADBE"][y]["operating_income"]) for y in sorted(sec["ADBE"]) if y >= 2009}
    R["licence"] = dict(adobe=adh, r12=get("ad36.r12"), r13=get("ad36.r13"), sub13=get("ad36.sub13"), prod13=get("ad36.prod13"),
                        cc13=get("ad36.cc13"), arr13=get("ad36.arr13"), sub25=get("ad36.sub"), rev25=get("ad36.rev"),
                        works=sw.j_curve())

    # cohorts and the backlog
    coh = sw.cohorts(8, new=1.0, growth=0.25, churn=W.churn, expansion=W.expansion)
    R["cohorts"] = dict(matrix=coh.tolist(), nrr_works=1 - W.churn + W.expansion, snow=get("sn36.nrr"), ddog=get("dd36.nrr"),
                        snow_big=get("sn36.big"), now_big=get("nw36.big"), crm_rpo=get("cr36.rpo"), crm_crpo=get("cr36.crpo"),
                        crm_rev=get("cr36.rev"), ms_rpo=get("ms36.rpo"), or_rpo=get("or36.rpo"), or_rev=get("or36.rev"),
                        crm_def=g("CRM", "deferred"), crm_ocf=get("cr36.ocf"), crm_op=get("cr36.op"))

    # selling
    ch = {y: (sec["CRM"][y]["marketing"] / sec["CRM"][y]["revenue"], sec["CRM"][y]["operating_income"] / sec["CRM"][y]["revenue"])
          for y in sorted(sec["CRM"]) if sec["CRM"][y].get("marketing")}
    r40 = {}
    for t, (nm, grp) in NAMES.items():
        ys = sorted(sec[t])
        if len(ys) < 2 or ys[-1] - 1 not in sec[t]:
            continue
        y = ys[-1]
        gr = sec[t][y]["revenue"] / sec[t][y - 1]["revenue"] - 1
        fcf = ((sec[t][y].get("ocf") or 0) - (sec[t][y].get("capex") or 0)) / sec[t][y]["revenue"]
        r40[nm] = dict(growth=gr, fcf=fcf, op=(sec[t][y].get("operating_income") or 0) / sec[t][y]["revenue"], group=grp,
                       sbc=(sec[t][y].get("sbc") or 0) / sec[t][y]["revenue"], rev=sec[t][y]["revenue"])
    R["selling"] = dict(crm=ch, r40=r40, crm_sm=get("cr36.sm"), crm_rev=get("cr36.rev"), cw_arr=get("cw36.arr"))

    # the intermission
    gdp = f["GDP"]
    softq = f["B985RC1Q027SBEA"]
    R["traffic"] = dict(share={_ym(m_): 100 * v / gdp[m_] for m_, v in softq.items() if m_ in gdp and m_ >= "1960-01"},
                        soft={_ym(m_): v for m_, v in softq.items()},
                        jobs={_ym(m_): v for m_, v in f["CES6054150001"].items()},
                        ppi={_ym(m_): v for m_, v in f["PCU511210511210"].items()},
                        cpi={_ym(m_): 100 * v / f["CPIAUCNS"]["1997-12"] for m_, v in f["CPIAUCNS"].items() if m_ >= "1997-12"})

    # platform
    R["platform"] = dict(ms_product=get("ms36.product"), ms_service=get("ms36.service"), cloudgm=get("ms36.cloudgm"),
                         seats=get("ms36.seats"), azure=get("ms36.azure"),
                         team=dict(rev=g("TEAM", "revenue"), sm=g("TEAM", "marketing"), rnd=g("TEAM", "rnd")),
                         crm=dict(rev=get("cr36.rev"), sm=get("cr36.sm"), rnd=get("cr36.rnd")))

    # when the copy stops being free
    def hist(t, fn, y0=2015):
        out = {}
        for y in sorted(sec[t]):
            if y >= y0:
                try:
                    out[y] = fn(sec[t][y])
                except TypeError:
                    pass
        return out
    R["ai"] = dict(ms_capex=hist("MSFT", lambda r: r["capex"]), ms_gm=hist("MSFT", lambda r: 1 - r["cost"] / r["revenue"]),
                   ms_capex_share=hist("MSFT", lambda r: r["capex"] / r["revenue"]), or_capex=hist("ORCL", lambda r: r["capex"]),
                   or_capex_share=hist("ORCL", lambda r: r["capex"] / r["revenue"]),
                   or_fcf=hist("ORCL", lambda r: r["ocf"] - r["capex"]), ms_fcf=hist("MSFT", lambda r: r["ocf"] - r["capex"]),
                   cloudgm=get("ms36.cloudgm"), cloud=get("ms36.cloud"), azure=get("ms36.azure"))

    # landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        if tk not in sec:
            continue
        ys = sorted(sec[tk])
        yy = ys[-1]
        mm = [sec[tk][k]["operating_income"] / sec[tk][k]["revenue"] for k in ys if yy - 4 <= k <= yy
              and sec[tk][k].get("operating_income") is not None]
        if not mm:
            continue
        comp.append(dict(name=nm, group=grp, rev=sec[tk][yy]["revenue"], margin=float(np.median(mm)), fy=yy, tk=tk,
                         growth=r40.get(nm, {}).get("growth")))
    R["landscape"] = dict(companies=comp, eur=eur.get(2025))

    # Called it?
    crmh = {y: sec["CRM"][y]["revenue"] for y in sorted(sec["CRM"]) if y >= 2018}
    q1 = get("ms36.q1cloud")
    target = 275.0
    R["called"] = dict(crm=crmh, target_crm=get("cr36.target"), crm26=get("cr36.rev"), h1=get("cr36.h1"),
                       cloud26=get("ms36.cloud"), q1=q1, target=target, need=target / get("ms36.cloud") - 1, prob=0.55)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("hook", {k: v for k, v in H.items() if k != "hist"})
    U = R["run"]
    b = U["base"]
    print("base arr by year", [round(a / 1e6) for a in b["arr"][3::4]], "growth", [round(100 * x, 1) for x in b["growth"][3::4]],
          "opm", [round(100 * x, 1) for x in b["op_margin"][3::4]], "cash", round(b["cum_cash"] / 1e6))
    print("unit", {k: round(v, 2) for k, v in U["unit"].items()})
    for s_, r in U["alloc"].items():
        print("alloc", s_, "arr3", round(r["arr"][11] / 1e6), "arr5", round(r["arr"][-1] / 1e6), "cash5", round(r["cum_cash"] / 1e6),
              "opm5", round(100 * r["op_margin"][-1], 1), "nrr5", round(r["nrr"][-1], 3))
    for k, r in U["price"].items():
        print("price", k, round(r["arr"][-1] / 1e6), round(r["cum_cash"] / 1e6))
    print("cost", {k: {a: (round(b_, 3) if isinstance(b_, float) else b_) for a, b_ in v.items()} for k, v in R["cost"]["companies"].items()})
    L = R["licence"]
    print("adobe", {y: (round(a, 2), round(b_, 2)) for y, (a, b_) in L["adobe"].items()})
    print("j", [round(v) for v in L["works"]["licence"]], [round(v) for v in L["works"]["switched"]])
    print("cohorts", {k: v for k, v in R["cohorts"].items() if k != "matrix"})
    print("selling crm", {y: (round(100 * a), round(100 * b_)) for y, (a, b_) in R["selling"]["crm"].items()})
    print("r40", {k: (round(100 * v["growth"]), round(100 * v["fcf"]), round(100 * v["op"])) for k, v in R["selling"]["r40"].items()})
    T = R["traffic"]
    print("traffic share", round(T["share"][max(T["share"])], 2), round(T["share"][min(T["share"])], 3), "jobs", T["jobs"][max(T["jobs"])],
          "ppi", T["ppi"][max(T["ppi"])], "cpi", round(T["cpi"][max(T["cpi"])], 1))
    print("platform", R["platform"])
    print("called", R["called"])
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
