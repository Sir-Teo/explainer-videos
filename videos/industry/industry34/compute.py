"""Every number in Part 34 of *Industry, Built* ("Restaurants and Franchising"), from the Register, the Filing Room and the
Works.

    python -m videos.industry.industry34.compute        # prints the film's numbers; writes .cache/industry34/computed.json

Items:
    hook        McDonald's: whose sales, whose revenue, whose profit
    run         the Run it store as a franchisee, then the franchisor's fee (the Works)
    unit        one restaurant's dollar at McDonald's company stores, Chipotle and Darden
    contract    the franchise contract: rents, royalties, terms and property
    split       franchisors against operators: margins and capital
    system      the system: Domino's dough, digital orders, delivery
    traffic     the intermission's series: restaurant sales, menu prices, jobs and wages
    delivery    DoorDash: orders, take and profit
    abroad      master franchisees and the global systems
    landscape   the companies by revenue and margin
    called      DoorDash's prospectus against its results; this series' call on McDonald's 50,000 restaurants
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import franchise as fw

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry34"

NAMES = {"MCD": ("McDonald's", "franchisor"), "YUM": ("Yum! Brands", "franchisor"), "QSR": ("Restaurant Brands", "franchisor"),
         "DPZ": ("Domino's", "franchisor"), "WING": ("Wingstop", "franchisor"), "WEN": ("Wendy's", "franchisor"),
         "PZZA": ("Papa John's", "franchisor"), "JACK": ("Jack in the Box", "franchisor"), "DIN": ("Dine Brands", "franchisor"),
         "CMG": ("Chipotle", "operator"), "SBUX": ("Starbucks", "operator"), "SHAK": ("Shake Shack", "operator"),
         "SG": ("Sweetgreen", "operator"), "CAVA": ("Cava", "operator"), "BROS": ("Dutch Bros", "operator"),
         "PTLO": ("Portillo's", "operator"), "LOCO": ("El Pollo Loco", "operator"), "DNUT": ("Krispy Kreme", "operator"),
         "DRI": ("Darden", "full"), "TXRH": ("Texas Roadhouse", "full"), "EAT": ("Brinker", "full"), "CAKE": ("Cheesecake Factory", "full"),
         "BLMN": ("Bloomin' Brands", "full"), "CBRL": ("Cracker Barrel", "full"), "FWRG": ("First Watch", "full"),
         "ARCO": ("Arcos Dorados", "master"), "YUMC": ("Yum China", "master"), "DASH": ("DoorDash", "delivery")}


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
    for r in read("sec_rest"):
        if r.get("revenue"):
            sec[r["ticker"]][_fy(str(r["year_end"]))] = r
    f = _monthly(read("fred_rest"))
    last = {t: max(d) for t, d in sec.items()}

    def g(t, item, y=None):
        y = last[t] if y is None else y
        return sec[t][y].get(item) if y in sec[t] else None

    # the hook
    R["hook"] = dict(rev=g("MCD", "revenue"), op=g("MCD", "operating_income"), ni=g("MCD", "profit"), frsales=get("md34.frsales"),
                     rents=get("md34.rents"), royal=get("md34.royal"), frrev=get("md34.frrev"), cosales=get("md34.cosales"),
                     rest=get("md34.rest"), fr=get("md34.fr"),
                     hist={y: (sec["MCD"][y]["revenue"], sec["MCD"][y]["operating_income"]) for y in sorted(sec["MCD"]) if y >= 2010})

    # Run it
    us_fr = get("md34.us") * get("md34.fr") / 100
    auv = get("md34.frsales.us") * 1e9 / us_fr
    take = (get("md34.rents") + get("md34.royal")) / get("md34.frsales")
    S = fw.Store(sales=auv, food=get("md34.food") / get("md34.cosales"), labour=get("md34.payroll") / get("md34.cosales"),
                 labour_fixed=get("wk34.fixed"), fees=take, ad=get("wk34.ad"), other=get("wk34.other"),
                 delivery=get("wk34.delivery"), commission=get("wk34.commission"), invest=get("wk34.invest") * 1e6)
    F = fw.Franchisor(store=S, pool=get("wk34.pool"), patience=get("wk34.patience"),
                      cost_share=1 - get("md34.frmargin") / get("md34.frrev"))
    takes = [float(round(x, 3)) for x in np.linspace(0.06, 0.18, 25)]
    R["run"] = dict(auv=auv, take=take, base=S.year(), store=dict(food=S.food, labour=S.labour, ad=S.ad, other=S.other,
                    delivery=S.delivery, commission=S.commission, invest=S.invest, fixed=S.labour_fixed),
                    drop10=S.year(0.9 * auv), wage20=S.with_(wage=1.2).year(), apps30=S.with_(delivery=0.30).year(),
                    fee15=S.with_(fees=0.15).year(),
                    by_sales={float(round(x, 2)): S.year(x * auv)["profit"] for x in np.linspace(0.8, 1.2, 17)},
                    franchisor={t: F.run(t) for t in takes}, cost_share=F.cost_share, pool=F.pool, patience=F.patience)

    # one restaurant's dollar
    cs = get("md34.cosales")
    cmg_rev = get("cm34.rev")
    dr = get("dr34.sales")
    R["unit"] = {"McDonald's company stores": dict(food=get("md34.food") / cs, labour=get("md34.payroll") / cs,
                                                    occupancy=get("md34.occ") / cs, margin=get("md34.comargin") / cs),
                 "Chipotle": dict(food=get("cm34.food") / cmg_rev, labour=get("cm34.labor") / cmg_rev,
                                  occupancy=(get("cm34.occ") + get("cm34.other")) / cmg_rev,
                                  margin=1 - (get("cm34.food") + get("cm34.labor") + get("cm34.occ") + get("cm34.other")) / cmg_rev),
                 "Darden": dict(food=get("dr34.food") / dr, labour=get("dr34.labor") / dr, occupancy=get("dr34.rexp") / dr,
                                margin=1 - (get("dr34.food") + get("dr34.labor") + get("dr34.rexp")) / dr)}
    R["unit_extra"] = dict(cmg_ars=get("cm34.ars"), cmg_units=get("cm34.units"), auv=auv, wing_auv=get("wg34.auv"))

    # the contract
    R["contract"] = dict(rents=get("md34.rents"), royal=get("md34.royal"), conv=get("md34.conv"), frsales=get("md34.frsales"),
                         term=get("md34.term"), land=get("md34.land"), bldg=get("md34.bldg"), wing_roy=get("wg34.royalty"),
                         wing_ad=get("wg34.ad"), arco_roy=get("ar34.royalty"), take=take,
                         rent_share=get("md34.rents") / (get("md34.rents") + get("md34.royal")))

    # franchisors against operators
    marg = {}
    for t in ("MCD", "YUM", "WING", "DPZ", "QSR", "WEN", "CMG", "SBUX", "DRI", "TXRH", "CAKE", "SHAK"):
        marg[NAMES[t][0]] = dict(op=100 * g(t, "operating_income") / g(t, "revenue"), rev=g(t, "revenue"),
                                 turns=g(t, "revenue") / g(t, "assets"), capex=100 * (g(t, "capex") or 0) / g(t, "revenue"),
                                 group=NAMES[t][1])
    R["split"] = dict(margins=marg, fr_margin=get("md34.frmargin") / get("md34.frrev"), co_margin=get("md34.comargin") / get("md34.cosales"),
                      frmargin=get("md34.frmargin"), comargin=get("md34.comargin"))

    # the system
    R["system"] = dict(supply=get("dp34.supply"), dpz_rev=g("DPZ", "revenue"), dpz_royal=get("dp34.royal"), scinc=get("dp34.scinc"),
                       dpz_units=get("dp34.units"), digital=get("wg34.digital"), delivery=get("md34.delivery"), wing_coc=get("wg34.coc"))

    # the intermission
    rs = f["RSFSDP"]
    ann = collections.defaultdict(list)
    for m_, v in rs.items():
        ann[int(m_[:4])].append(v)
    fafh, fah, cpi = f["CUUR0000SEFV"], f["CUUR0000SAF11"], f["CPIAUCNS"]
    b0 = "2019-12"
    gro = collections.defaultdict(list)
    for r in read("fred_grocery"):
        if r["series"] == "RSGCS":
            gro[int(str(r["month"])[:4])].append(r["value"])
    R["traffic"] = dict(sales={y: 12 * np.mean(v) / 1e3 for y, v in ann.items() if len(v) == 12},
                        grocery={y: 12 * np.mean(v) / 1e3 for y, v in gro.items() if len(v) == 12},
                        fafh={_ym(m_): 100 * v / fafh[b0] for m_, v in fafh.items() if m_ >= "2015-01"},
                        fah={_ym(m_): 100 * v / fah[b0] for m_, v in fah.items() if m_ >= "2015-01"},
                        cpi={_ym(m_): 100 * v / cpi[b0] for m_, v in cpi.items() if m_ >= "2015-01"},
                        jobs={_ym(m_): v for m_, v in f["CES7072200001"].items() if m_ >= "1990-01"},
                        ahe={_ym(m_): v for m_, v in f["CES7000000003"].items()},
                        minwage={_ym(m_): v for m_, v in f["FEDMINNFRWG"].items() if m_ >= "2006-01"})

    # delivery
    R["delivery"] = dict(gov=get("da34.gov"), orders=get("da34.orders"), nrm=get("da34.nrm"), rev=g("DASH", "revenue"),
                         ni={y: sec["DASH"][y]["profit"] for y in sorted(sec["DASH"])},
                         revs={y: sec["DASH"][y]["revenue"] for y in sorted(sec["DASH"])})

    # abroad
    R["abroad"] = dict(arco_units=get("ar34.units"), arco_roy=get("ar34.royalty"), arco_rev=g("ARCO", "revenue"),
                       yumc_rev=g("YUMC", "revenue"), yum_units=get("ym34.units"), yum_fr=get("ym34.fr"), mcd_rest=get("md34.rest"),
                       dpz_units=get("dp34.units"))

    # landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        if tk not in sec:
            continue
        ys = sorted(sec[tk])
        y = ys[-1]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in ys if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=sec[tk][y]["revenue"], margin=float(np.median(mm)), fy=y, tk=tk))
    R["landscape"] = dict(companies=comp)

    rest = {2023: get("md34.rest23"), 2024: get("md34.rest24"), 2025: get("md34.rest")}
    end26 = get("md34.rest") + get("md34.net26")
    R["called"] = dict(loss19=get("da34.loss19"), ni=R["delivery"]["ni"], revs=R["delivery"]["revs"], target=get("md34.target"),
                       rest=rest, end26=end26, need27=get("md34.target") - end26, net26=get("md34.net26"), prob=0.25)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("hook", {k: v for k, v in H.items() if k != "hist"})
    U = R["run"]
    pk = lambda s: {k: (round(v / 1e3) if abs(v) > 1e3 else round(v, 3)) for k, v in s.items()}  # noqa: E731
    print("run auv/take", round(U["auv"] / 1e6, 3), round(U["take"], 4), U["store"])
    for k in ("base", "drop10", "wage20", "apps30", "fee15"):
        print(k, pk(U[k]))
    print("franchisor", {t: (round(r["rate"], 2), round(r["stores"][-1]), round(r["last"] / 1e6), round(r["total"] / 1e6), round(r["franchisee"]["payback"], 1))
                         for t, r in U["franchisor"].items()}, round(U["cost_share"], 3))
    print("unit", {k: {a: round(100 * b, 1) for a, b in v.items()} for k, v in R["unit"].items()})
    print("contract", R["contract"])
    print("split", {k: {a: (round(b, 2) if isinstance(b, float) else b) for a, b in v.items()} for k, v in R["split"]["margins"].items()},
          round(R["split"]["fr_margin"], 3), round(R["split"]["co_margin"], 3))
    print("system", R["system"])
    T = R["traffic"]
    print("sales $bn", {y: round(v) for y, v in T["sales"].items() if y in (1992, 2000, 2010, 2019, 2020, 2025)})
    print("prices", round(T["fafh"][max(T["fafh"])], 1), round(T["fah"][max(T["fah"])], 1), round(T["cpi"][max(T["cpi"])], 1))
    print("jobs", T["jobs"][max(T["jobs"])], "ahe", {k: v for k, v in T["ahe"].items() if k in (min(T["ahe"]), max(T["ahe"]))}, "min", T["minwage"][max(T["minwage"])])
    print("delivery", R["delivery"])
    print("abroad", R["abroad"])
    print("called", {k: v for k, v in R["called"].items() if k not in ("ni", "revs")})
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
