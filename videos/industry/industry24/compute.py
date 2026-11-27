"""Every number in Part 24 of *Industry, Built* ("Construction"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry24.compute        # prints the film's numbers; writes .cache/industry24/computed.json

Items:
    hook        the Empire State Building; California's high-speed railway, 2008 against 2026
    run         the Run it decision: five tenders at three markups against four rivals (the Works)
    curse       the winner's estimate against everyone's (the Works)
    cash        a contractor's cash and profit when its order book stops growing (the Works)
    dollar      construction's value added and pay (BEA); spending by type (Census); margins along the chain (SEC)
    productivity real value added per worker and prices since 1970, construction against manufacturing (BEA, BLS)
    spending    construction spending by type since 2002 (Census)
    mega        megaprojects' overruns (Flyvbjerg) and the high-speed railway
    carillion   the collapse of Carillion (NAO)
    contracts   Fluor's contract mix and charges; Quanta's backlog
    concession  Ferrovial: building against owning the road
    landscape   the companies by revenue and margin
    called      the railway's dates against the reference class; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np
from scipy.stats import norm

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import contractor

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry24"

NAMES = {"PWR": ("Quanta Services", "trade"), "EME": ("EMCOR", "trade"), "MTZ": ("MasTec", "trade"),
         "FIX": ("Comfort Systems", "trade"), "DY": ("Dycom", "trade"), "PRIM": ("Primoris", "trade"),
         "MYRG": ("MYR Group", "trade"), "APG": ("APi Group", "trade"), "FLR": ("Fluor", "general"),
         "GVA": ("Granite", "general"), "TPC": ("Tutor Perini", "general"), "STRL": ("Sterling", "general"),
         "AGX": ("Argan", "general"), "ROAD": ("Construction Partners", "general"), "J": ("Jacobs", "engineer"),
         "ACM": ("AECOM", "engineer"), "KBR": ("KBR", "engineer"), "TTEK": ("Tetra Tech", "engineer"),
         "VMC": ("Vulcan Materials", "materials"), "MLM": ("Martin Marietta", "materials"), "CRH": ("CRH", "materials"),
         "EXP": ("Eagle Materials", "materials"), "HRI": ("Herc", "rental"), "URI": ("United Rentals", "rental"),
         "FER": ("Ferrovial", "concession")}


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for name in ("sec_construction", "sec_mach"):
        for r in read(name):
            if r["ticker"] in NAMES and r.get("revenue"):
                sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    fred: dict = collections.defaultdict(dict)
    for r in read("fred_construction"):
        fred[r["series"]][str(r["month"])] = r["value"]
    bea: dict = collections.defaultdict(dict)
    for r in read("bea_long"):
        bea[(r["measure"], r["industry"])][int(r["year"])] = r["index_2017"]
    for r in read("fred_fashion"):
        if r["series"] == "EXUSEU":
            fred["EXUSEU"][str(r["month"])] = r["value"]
    eur = _annual(fred["EXUSEU"])[2025]

    R["hook"] = dict(days=get("esb.days"), stories=get("esb.stories"), hours=get("esb.hours"), floors=get("esb.floors"),
                     sqft=get("esb.sqft"), hsr08=get("hsr08.cost"), phase1=get("hsr26.phase1"), full=get("hsr26.full"),
                     mb=get("hsr26.mb"), mb_done=get("hsr26.mb.done"), p1_done=get("hsr26.phase1.done"))

    t = contractor.Tender()
    ch = t.choices()
    R["run"] = dict(choices={f"{m:.2f}": v for m, v in ch.items()}, cost=t.cost, sd=t.sd, rivals=t.rivals,
                    rival_markup=t.rival_markup, best=t.best(),
                    curve={f"{m:.2f}": t.bid(m) for m in np.round(np.arange(0, 0.205, 0.01), 2)})
    e = np.linspace(-0.2, 0.2, 161)
    b = 1.08 * (1 + e) * t.cost
    pw = t._win(b)
    dens = norm.pdf(e / t.sd) / t.sd
    won = dens * pw
    won = won / (won.sum() * (e[1] - e[0]))
    R["curse"] = dict(e=e.tolist(), all=dens.tolist(), won=won.tolist(), mean_won=t.bid(0.08)["est_if_won"])

    starts = [1] * 24 + [0] * 12
    cp = contractor.cash_path(starts)
    R["cash"] = dict(cash=cp["cash"].tolist(), profit=cp["profit"].tolist(), months=cp["months"], stop=24,
                     peak=int(np.argmax(cp["cash"][:40])), receive_lag=2, pay_lag=3, retention=0.05, margin=0.03)

    va = {r["sector"]: r for r in read("bea_va_2025")}
    con = va["Construction"]
    ttl = _annual(fred["TTLCONS"])
    R["dollar"] = dict(va=con["va_musd"] / 1e6, pct=con["pct_gdp"], comp=con["comp_pct"], gos=con["gos_pct"],
                       all_comp=va["All industries (GDP)"]["comp_pct"], spend=ttl[2025] / 1e6)

    jobs = {k: _annual(fred[s]) for k, s in (("construction", "USCONS"), ("manufacturing", "MANEMP"), ("all", "PAYEMS"))}
    base = 1970
    per = {k: {y: (bea[("quantity", k)][y] / jobs[k][y]) / (bea[("quantity", k)][base] / jobs[k][base])
               for y in range(base, 2026) if y in jobs[k]} for k in jobs}
    price = {k: {y: bea[("price", k)][y] / bea[("price", k)][base] for y in range(base, 2026)} for k in jobs}
    R["productivity"] = dict(per=per, price=price, base=base, jobs={k: (jobs[k][base], jobs[k][2025]) for k in jobs},
                             real={k: bea[("quantity", k)][2025] / bea[("quantity", k)][base] for k in jobs},
                             peak_year=max(per["construction"], key=per["construction"].get))
    cpi = _annual(fred["CPIAUCNS"], need=11)
    ppi = _annual(fred["WPUSI012011"], need=11)
    lumber = {m: v for m, v in fred["WPU081"].items() if m >= "2019-01"}
    R["materials"] = dict(ppi={y: ppi[y] / ppi[2019] for y in ppi if y >= 2015}, cpi={y: cpi[y] / cpi[2019] for y in cpi if y >= 2015},
                          lumber=lumber, lumber_peak=max(lumber, key=lumber.get))

    cats = {"residential": "TLRESCONS", "nonresidential": "TLNRESCONS", "public": "TLPBLCONS", "manufacturing": "PRMFGCONS",
            "highway": "TLHWYCONS", "power": "TLPWRCONS", "office": "TLOFCONS", "commercial": "TLCOMCONS", "total": "TTLCONS"}
    R["spending"] = {k: {y: v / 1e3 for y, v in _annual(fred[s], need=9).items() if y >= 2002} for k, s in cats.items()}

    R["mega"] = dict(share=get("fly.share"), rail=get("fly.rail"), rail_demand=get("fly.rail.demand"), road=get("fly.road"),
                     overruns={k: get(f"fly.over.{k}") for k in ("suez", "scot", "sydney", "nhs", "bigdig", "denver",
                                                                 "brooklyn", "channel", "jubilee", "greatbelt")},
                     hsr08=get("hsr08.cost"), bond=get("hsr08.bond"), phase1=get("hsr26.phase1"), full=get("hsr26.full"),
                     mb=get("hsr26.mb"), mb_done=get("hsr26.mb.done"), p1_done=get("hsr26.phase1.done"),
                     spent=get("hsr26.spent"))
    R["carillion"] = dict(staff=get("nao.staff"), contracts=get("nao.contracts"), revenue=get("nao.revenue"),
                          warn1=get("nao.warn1"), warn2=get("nao.warn2"), cash=get("nao.cash"), pension=get("nao.pension"),
                          paydays=get("nao.paydays"))
    reimb, lump = get("flr.reimb"), get("flr.lump")
    R["contracts"] = dict(reimb=reimb, lump=lump, share=reimb / (reimb + lump),
                          share24=get("flr.reimb.2024") / (get("flr.reimb.2024") + get("flr.lump.2024")),
                          adj=get("flr.adj"), santos=get("flr.santos"), lossbook=get("flr.lossbook"),
                          pwr_backlog=(get("pwr.backlog.2025"), get("pwr.backlog")), pwr_q3=(get("pwr.q3.prev"), get("pwr.q3")),
                          tpc={y: sec["TPC"][y]["profit"] / sec["TPC"][y]["revenue"] for y in sorted(sec["TPC"]) if y >= 2019})
    R["concession"] = dict(con=(get("fer.con.rev"), get("fer.con.op")), hwy=(get("fer.hwy.rev"), get("fer.hwy.op")),
                           e407=(get("fer.407.rev"), get("fer.407.net")), stake=get("fer.407.stake"), buy=get("fer.407.buy"),
                           book=get("fer.book"), public=get("fer.public"))

    comp = []
    for tk, (nm, grp) in NAMES.items():
        if not sec[tk]:
            continue
        y = max(sec[tk])
        r = sec[tk][y]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in sec[tk] if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        fx = eur if r["currency"] == "EUR" else 1.0
        comp.append(dict(name=nm, group=grp, rev=r["revenue"] * fx, margin=float(np.median(mm)), fy=y, tk=tk))
    R["landscape"] = dict(companies=comp, eur=eur)
    g = collections.defaultdict(list)
    for c in comp:
        g[c["group"]].append(c["margin"])
    R["chain"] = {k: float(np.median(v)) for k, v in g.items()}

    R["called"] = dict(mb_done=get("hsr26.mb.done"), call_year=2034, prob=0.70, share=get("fly.share"), rail=get("fly.rail"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("hook", R["hook"])
    for k, v in R["run"]["choices"].items():
        print("run", k, {a: round(b, 3) for a, b in v.items()})
    print("best", {a: round(b, 3) for a, b in R["run"]["best"].items()})
    c = R["cash"]
    print("cash peak", c["peak"], round(c["cash"][c["peak"]], 1), "at +8", round(c["cash"][c["peak"] + 8], 1),
          "profit", round(c["profit"][c["peak"]], 1), round(c["profit"][c["peak"] + 8], 1), "end", round(c["cash"][-1], 1))
    print("dollar", R["dollar"])
    P = R["productivity"]
    print("per worker 2025", {k: round(v[2025], 2) for k, v in P["per"].items()}, "peak", P["peak_year"],
          "price", {k: round(v[2025], 2) for k, v in P["price"].items()}, "jobs", P["jobs"], "real", P["real"])
    print("materials", {y: round(v, 2) for y, v in R["materials"]["ppi"].items()}, R["materials"]["lumber_peak"])
    print("spending", {k: (round(v.get(2019, 0)), round(v.get(2025, 0))) for k, v in R["spending"].items()})
    print("chain", {k: round(100 * v, 1) for k, v in R["chain"].items()})
    print("landscape", [(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]])
    print("contracts", {k: v for k, v in R["contracts"].items() if k != "tpc"}, {y: round(100 * v, 1) for y, v in R["contracts"]["tpc"].items()})
    print("concession", R["concession"])


if __name__ == "__main__":
    main()
