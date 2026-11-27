"""Every number in Part 23 of *Industry, Built* ("Fashion and Luxury"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry23.compute        # prints the film's numbers; writes .cache/industry23/computed.json

Items:
    hook        Inditex's four quarters of gross margin; its sales and stores; Hermès's margin
    run         the Run it decision: buy the season early and far, late and near, or a base and a chase (the Works)
    curve       the season's demand curve and the three orders on it (the Works)
    dollar      a dollar of NIKE's sales
    made        where clothes are made: NIKE's factories, exports by country (UN Comtrade), America's sewing jobs (FRED)
    prices      the price of clothes in America against all prices since 1990 (FRED)
    fast        Inditex: concepts, inventory, working capital, the first half of 2026
    turns       days of inventory across the companies (SEC; Inditex)
    offprice    TJX against the department stores (SEC); TJX's model
    brands      NIKE's channels and margin; Lululemon; Levi's
    luxury      Hermès since 2022; LVMH's business groups; Coach and Kate Spade
    fickle      Gucci against Hermès; Coach, Kate Spade and Michael Kors
    landscape   the companies by revenue and margin
    called      Inditex's gross margin guidance; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np
from scipy.stats import lognorm

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import fashion

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry23"

NAMES = {"NKE": ("NIKE", "sport"), "LULU": ("Lululemon", "sport"), "UAA": ("Under Armour", "sport"),
         "DECK": ("Deckers (HOKA, UGG)", "sport"), "ONON": ("On", "sport"), "COLM": ("Columbia", "sport"),
         "VFC": ("VF (The North Face, Vans)", "brand"), "PVH": ("PVH (Calvin Klein, Tommy Hilfiger)", "brand"),
         "RL": ("Ralph Lauren", "brand"), "LEVI": ("Levi Strauss", "brand"), "BIRK": ("Birkenstock", "brand"),
         "TPR": ("Tapestry (Coach)", "luxury"), "CPRI": ("Capri (Michael Kors)", "luxury"),
         "GAP": ("Gap", "store"), "ANF": ("Abercrombie & Fitch", "store"), "AEO": ("American Eagle", "store"),
         "URBN": ("Urban Outfitters", "store"), "SIG": ("Signet", "store"), "TJX": ("TJX", "off"), "ROST": ("Ross", "off"),
         "BURL": ("Burlington", "off"), "M": ("Macy's", "dept"), "KSS": ("Kohl's", "dept")}


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_fashion"):
        # keyed by the calendar year the fiscal year ends in; most retailers' years end in late January
        if r.get("revenue"):
            sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    fred: dict = collections.defaultdict(dict)
    for r in read("fred_fashion"):
        fred[r["series"]][str(r["month"])] = r["value"]
    eur, chf = _annual(fred["EXUSEU"])[2025], _annual(fred["EXSZUS"])[2025]

    R["hook"] = dict(q={q: (get(f"itx.q{q}.sales"), get(f"itx.q{q}.gm")) for q in (1, 2, 3, 4)}, sales=get("itx.sales"),
                     gm=get("itx.gm"), stores=get("itx.stores"), markets=get("itx.markets"), rms_margin=get("rms.roi_margin"),
                     rms_rev=get("rms.rev.2025"), nke_factories=get("nke.fw.factories") + get("nke.ap.factories"))

    s = fashion.Season()
    ch = s.choices()
    R["run"] = dict(choices=ch, price=s.price, clearance=s.clearance, mean=s.mean, cv_far=s.cv_far, cv_near=s.cv_near,
                    cost_far=s.cost_far, cost_near=s.cost_near, ratio_far=s.ratio(s.cost_far),
                    ratio_near=s.ratio(s.cost_near),
                    cv={c: fashion.Season(cv_far=c).far()["profit"] for c in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)})
    sf = s.sigmas()[0]
    dist = lognorm(s=sf, scale=np.exp(s.mu0()))
    xs = np.linspace(2_000, 300_000, 150)
    R["curve"] = dict(x=xs.tolist(), pdf=(dist.pdf(xs) * 1e5).tolist(), far=ch["far"]["ordered"],
                      p_short=float(dist.sf(ch["far"]["ordered"])), p_below_mean=float(dist.cdf(s.mean)),
                      median=float(dist.median()), p10=float(dist.ppf(0.1)), p90=float(dist.ppf(0.9)))

    n26 = sec["NKE"][2026]
    rev = n26["revenue"]
    gm = get("nke.gm.2026") / 100
    R["dollar"] = dict(make=1 - gm, demand=get("nke.demand") / rev, net=n26["profit"] / rev, rev=rev, cost=n26["cost"],
                       other=gm - get("nke.demand") / rev - n26["profit"] / rev)

    trade: dict = collections.defaultdict(lambda: collections.defaultdict(float))
    for r in read("comtrade_apparel"):
        trade[r["reporter"]][int(r["year"])] += r["exports_usd_bn"]
    apparel_jobs = _annual(fred["CES3231500001"])
    R["made"] = dict(fw={"Vietnam": get("nke.fw.vn"), "Indonesia": get("nke.fw.id"), "China": get("nke.fw.cn")},
                     ap={"Vietnam": get("nke.ap.vn"), "Cambodia": get("nke.ap.kh"), "China": get("nke.ap.cn")},
                     fw_factories=get("nke.fw.factories"), fw_countries=get("nke.fw.countries"), fw_makers=get("nke.fw.makers"),
                     fw_top4=get("nke.fw.top4"), ap_factories=get("nke.ap.factories"), ap_countries=get("nke.ap.countries"),
                     ap_makers=get("nke.ap.makers"), tier2=get("nke.tier2"),
                     exports={k: dict(v) for k, v in trade.items()},
                     exp2023={k: v[2023] for k, v in trade.items() if 2023 in v},
                     jobs={y: v for y, v in apparel_jobs.items() if y >= 1990}, jobs90=apparel_jobs[1990],
                     jobs25=apparel_jobs[2025])

    cpi = _annual(fred["CPIAUCNS"], need=11)  # the BLS published no October 2025 CPI
    app = _annual(fred["CPIAPPNS"], need=11)
    R["prices"] = dict(app={y: app[y] / app[1990] for y in app if y >= 1990}, all={y: cpi[y] / cpi[1990] for y in cpi if y >= 1990},
                       real=app[2025] / app[1990] / (cpi[2025] / cpi[1990]), app_x=app[2025] / app[1990],
                       all_x=cpi[2025] / cpi[1990])

    R["fast"] = dict(concepts={k: get(f"itx.concept.{k}") for k in ("zara", "bershka", "stradivarius", "pullbear", "massimo", "oysho")},
                     inventory=get("itx.inventory"), payables=get("itx.payables"), receivables=get("itx.receivables"),
                     owc=get("itx.owc"), cost=get("itx.cost"), days=fashion.inventory_days(get("itx.inventory"), get("itx.cost")),
                     ebit=get("itx.ebit"), ebit_margin=get("itx.ebit_margin"), net=get("itx.net"),
                     h1=(get("itx.h1.sales"), get("itx.h1.gm")), h1_prev=(get("itx.h1.sales_prev"), get("itx.h1.gm_prev")),
                     space=get("itx.space"))

    days = {"Inditex": R["fast"]["days"], "NIKE": fashion.inventory_days(get("nke.inventory"), n26["cost"])}
    for tk in ("TJX", "ROST", "BURL", "URBN", "AEO", "DECK", "ANF", "KSS", "M", "LULU", "RL", "TPR", "LEVI"):
        r = sec[tk][max(sec[tk])]
        days[NAMES[tk][0]] = fashion.inventory_days(r["inventory"], r["cost"])
    R["turns"] = dict(days=days)

    def idx(tk, base=2015):
        return {y: sec[tk][y]["revenue"] / sec[tk][base]["revenue"] for y in sorted(sec[tk]) if y >= base}

    R["offprice"] = dict(index={"TJX": idx("TJX"), "Ross": idx("ROST"), "Burlington": idx("BURL"), "Macy's": idx("M"),
                                "Kohl's": idx("KSS")},
                         rev={k: (sec[tk][2015]["revenue"], sec[tk][2026]["revenue"]) for k, tk in
                              (("TJX", "TJX"), ("Ross", "ROST"), ("Burlington", "BURL"), ("Macy's", "M"), ("Kohl's", "KSS"))},
                         sales=get("tjx.sales"), stores=get("tjx.stores"), potential=get("tjx.potential"),
                         vendors=get("tjx.vendors"), lo=get("tjx.below.lo"), hi=get("tjx.below.hi"), pretax=get("tjx.pretax"),
                         cost=get("tjx.cost"))

    R["brands"] = dict(channel={y: (get(f"nke.wholesale.{y}"), get(f"nke.direct.{y}")) for y in (2024, 2025, 2026)},
                       gm={y: get(f"nke.gm.{y}") for y in (2024, 2025, 2026)}, nke_rev={y: sec["NKE"][y]["revenue"] for y in sorted(sec["NKE"]) if y >= 2015},
                       lulu=(get("lulu.gm.prev"), get("lulu.gm")), lulu_taiwan=get("lulu.taiwan"), lulu_china=get("lulu.china"),
                       levi_dtc=get("levi.dtc"), levi_top10=get("levi.top10"), ieepa=get("nke.ieepa"),
                       footwear=get("nke.footwear"), apparel=get("nke.apparel"), demand=get("nke.demand"), us=get("nke.us"),
                       lulu_rev={y: sec["LULU"][y]["revenue"] for y in sorted(sec["LULU"]) if y >= 2015},
                       on_rev={y: sec["ONON"][y]["revenue"] / chf for y in sorted(sec["ONON"])},
                       deck_rev={y: sec["DECK"][y]["revenue"] for y in sorted(sec["DECK"]) if y >= 2015})

    mc = {k: (get(f"mc.rev.{k}"), get(f"mc.pro.{k}")) for k in ("fashion", "watches", "perfume", "wines", "retail")}
    R["luxury"] = dict(rms={y: (get(f"rms.rev.{y}"), get(f"rms.roi.{y}")) for y in (2022, 2023, 2024, 2025)},
                       gross=get("rms.gross"), leather=get("rms.leather"), leather_g=get("rms.leather.g"),
                       workshops=get("rms.workshops"), inhouse=get("rms.inhouse"), france=get("rms.france"), staff=get("rms.staff"),
                       mc=mc, mc_rev=get("mc.rev"), mc_pro=get("mc.pro"), mc_brands=get("mc.brands"),
                       coach=get("tpr.coach"), coach_bags=get("tpr.coach.bags"), coach_gm=get("tpr.coach.gm"),
                       kate_gm=get("tpr.kate.gm"))

    R["fickle"] = dict(gucci={y: (get(f"ker.gucci.{y}"), get(f"ker.gucci.roi.{y}")) for y in (2022, 2023, 2024, 2025)},
                       gucci_retail=get("ker.gucci.retail"), gucci_margin=get("ker.gucci.margin"), kering=get("ker.rev"),
                       coach={2024: get("tpr.coach.2024"), 2025: get("tpr.coach.2025"), 2026: get("tpr.coach")},
                       kate=(get("tpr.kate.2024"), get("tpr.kate")), mk=(get("cpri.mk.2024"), get("cpri.mk")),
                       versace=get("cpri.versace"))

    comp = []
    for tk, (nm, grp) in NAMES.items():
        y = max(sec[tk])
        r = sec[tk][y]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in sec[tk] if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        fx = 1 / chf if r["currency"] == "CHF" else eur if r["currency"] == "EUR" else 1.0
        comp.append(dict(name=nm, group=grp, rev=r["revenue"] * fx, margin=float(np.median(mm)), fy=y, tk=tk))
    for nm, grp, rv, net in (("Inditex (Zara)", "store", get("itx.sales"), get("itx.net")),
                             ("Hermès", "luxury", get("rms.rev.2025") / 1e3, get("rms.net")),
                             ("LVMH", "luxury", get("mc.rev"), get("mc.net")),
                             ("Kering (Gucci)", "luxury", get("ker.rev"), get("ker.net"))):
        # European houses report in euros: one year (2025) only, at the year's average dollar rate
        comp.append(dict(name=nm, group=grp, rev=rv * eur, margin=net / rv, fy=2025, tk=nm, europe=True))
    R["landscape"] = dict(companies=comp, eur=eur, chf=chf)

    g = get("itx.gm")
    q = {k: (get(f"itx.q{k}.sales"), get(f"itx.q{k}.gm")) for k in (1, 2, 3, 4)}
    h2_sales25 = q[3][0] + q[4][0]
    h2_gm25 = (q[3][0] * q[3][1] + q[4][0] * q[4][1]) / h2_sales25
    growth = get("itx.h1.sales") / get("itx.h1.sales_prev")
    h2_sales26 = h2_sales25 / 1e3 * growth  # this series' assumption: the second half grows as the first did
    h1s, h1g = get("itx.h1.sales"), get("itx.h1.gm")
    call = 58.5
    need = (call * (h1s + h2_sales26) - h1g * h1s) / h2_sales26
    R["called"] = dict(base=g, lo=g - 0.5, hi=g + 0.5, h1=h1g, h1_prev=get("itx.h1.gm_prev"), call=call, prob=0.55,
                       q=[q[k][1] for k in (1, 2, 3, 4)], h2_gm25=h2_gm25, need=need, growth=growth - 1)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("hook", R["hook"])
    for k, v in R["run"]["choices"].items():
        print("run", k, {a: round(b, 3) for a, b in v.items()})
    print("cv", {k: round(v / 1e6, 3) for k, v in R["run"]["cv"].items()})
    print("curve", {k: (round(v, 3) if isinstance(v, float) else None) for k, v in R["curve"].items() if not isinstance(v, list)})
    print("dollar", {k: round(100 * v, 1) for k, v in R["dollar"].items() if k not in ("rev", "cost")})
    M = R["made"]
    print("made 2023", {k: round(v, 1) for k, v in M["exp2023"].items()}, round(M["jobs90"]), round(M["jobs25"]))
    print("china", {y: round(v, 1) for y, v in sorted(M["exports"]["China"].items())})
    print("prices", round(R["prices"]["real"], 3), round(R["prices"]["app_x"], 3), round(R["prices"]["all_x"], 3))
    print("fast", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in R["fast"].items()})
    print("turns", {k: round(v) for k, v in sorted(R["turns"]["days"].items(), key=lambda kv: kv[1])})
    print("offprice", {k: round(v[2026], 2) for k, v in R["offprice"]["index"].items()}, R["offprice"]["rev"])
    print("landscape", [(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]])
    print("lux", {k: (round(v[0]), round(v[1]), round(100 * v[1] / v[0], 1)) for k, v in R["luxury"]["mc"].items()})
    print("called", R["called"])


if __name__ == "__main__":
    main()
