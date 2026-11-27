"""Every number in Part 16 of *Industry, Built* ("Electronics"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry16.compute        # prints the film's numbers; writes .cache/industry16/computed.json

Items:
    hook        Shih's smile (1992); Hon Hai's revenue and what it kept; Apple's products and services margins
    run         the Run it game: a brand's order that needs a new plant (the Works)
    dollar      a device's price split between parts, assembler and brand (the Works)
    contract    the assemblers' margins since 2010 (SEC) and Hon Hai's; turnkey against consigned; Hon Hai's returns
    honhai      Hon Hai's revenue by product, its largest customer and its servers subgroup
    brand       Apple's products and services; Apple's profit against Hon Hai's
    components  the component makers' margins: connectors, glass, displays, packaging (SEC)
    history     the prices of televisions, computers and smartphones (BLS); US output of computers (FRED)
    pc          Intel's PC chips against HP's and Dell's PC businesses
    servers     US imports of servers and processing units by country (UN Comtrade); Hon Hai's cloud revenue
    cluster     where Hon Hai's plants are (non-current assets by country); US electronics employment (BLS via FRED)
    tariffs     US imports of phones and laptops by country, 2015-2025 (UN Comtrade); the Section 301 notices
    landscape   the listed electronics companies by group
    called      the Commerce Secretary's 2025 forecast; this series' call on India's share of US smartphone imports
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import device

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry16"
GROUPS = {"brand": ("AAPL", "DELL", "HPQ", "LOGI", "SONY"),
          "assembler": ("HONHAI", "JBL", "FLEX", "SANM", "CLS", "PLXS", "BHE", "SMCI"),
          "components": ("APH", "TEL", "GLW", "LPL", "ASX")}
ASSEMBLERS = ("JBL", "FLEX", "SANM", "PLXS", "BHE", "CLS")
COMPONENTS = ("APH", "TEL", "GLW")


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
    """The calendar year a fiscal year mostly falls in (a year ending in January belongs to the year before)."""
    y, m = int(end[:4]), int(end[5:7])
    return y - 1 if m <= 3 else y


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_annual"):
        if r.get("revenue") and r["revenue"] > 0:   # Plexus's XBRL revenue for 2011-2014 is not its total revenue (negative)
            sec[r["ticker"]][str(r["year_end"])] = r
    foreign: dict = collections.defaultdict(dict)
    for r in read("sec_foreign"):
        foreign[r["ticker"]][str(r["year_end"])] = r
    fred = _series(read("fred_elec"))
    fx = {k: {int(m[:4]): v for m, v in fred[k].items()} for k in ("AEXTAUS", "AEXJPUS", "AEXKOUS")}
    twd25 = fx["AEXTAUS"][2025]

    def margin_by_year(tk):
        out = {}
        for end, r in sec[tk].items():
            if r.get("net_income") is not None:
                out[_fy(end)] = r["net_income"] / r["revenue"]
        return out

    # --- hook -------------------------------------------------------------------------------------------------------------
    hh_rev, hh_ni, hh_op = get("hh.rev"), get("hh.ni"), get("hh.op")
    R["hook"] = dict(shih=get("shih.year"), hh_rev_twd=hh_rev, hh_rev_usd=hh_rev / twd25, hh_ni_usd=hh_ni / twd25,
                     hh_kept=hh_ni / hh_rev, hh_op=hh_op / hh_rev, twd=twd25,
                     aapl_gm_products=get("aapl.gm.products"), aapl_gm_services=get("aapl.gm.services"))

    # --- run it -----------------------------------------------------------------------------------------------------------
    ps = [round(p, 2) for p in np.linspace(0, 1, 21)]
    curve = {p: {plan: device.play(plan, p)["expected"] / 1e6 for plan in device.PLANS} for p in ps}
    games = {plan: device.play(plan, 0.5) for plan in device.PLANS}
    cross = next(p for p in ps if curve[p]["abroad"] > curve[p]["build"])
    o, a = device.Offer(), device.Assembler()
    R["run"] = dict(curve=curve, plans=device.PLANS,
                    games={k: dict(no=v["no_renewal"] / 1e6, yes=v["renewal"] / 1e6, exp=v["expected"] / 1e6,
                                   even=v["break_even_p"], flows=[f / 1e6 for f in v["flows"]]) for k, v in games.items()},
                    cross=cross, units=o.units, fee=o.fee, years=o.years, renewal=o.renewal, plant=a.plant / 1e6,
                    labour=a.labour, other=a.other, fixed=a.fixed / 1e6, rate=o.rate)
    half = device.play("build", 0.0, a=device.Assembler(plant=a.plant / 2))
    R["run"]["tooling"] = dict(no=half["no_renewal"] / 1e6, yes=half["renewal"] / 1e6, plant=a.plant / 2e6)

    # --- the dollar ---------------------------------------------------------------------------------------------------------
    d = device.Device()
    cheap = device.Device(price=300.0, bom=210.0, fee=12.0, brand_costs=60.0)
    R["dollar"] = dict(price=d.price, split=d.split(), bom=d.bom, fee=d.fee,
                       cheap=dict(price=cheap.price, split=cheap.split(), bom=cheap.bom, fee=cheap.fee, brand_costs=cheap.brand_costs))

    # --- contract manufacturing -------------------------------------------------------------------------------------------
    margins = {tk: {y: m for y, m in margin_by_year(tk).items() if 2010 <= y <= 2025} for tk in ASSEMBLERS}
    margins["HONHAI"] = {2024: get("hh.ni.2024") / get("hh.rev.2024"), 2025: hh_ni / hh_rev}
    t, c = device.Assembler(turnkey=True).year(20e6), device.Assembler(turnkey=False).year(20e6)
    latest = {}
    for tk in ASSEMBLERS:
        end = max(sec[tk])
        latest[tk] = dict(year=_fy(end), revenue=sec[tk][end]["revenue"], ni=sec[tk][end]["net_income"])
    R["contract"] = dict(margins=margins, turnkey=t, consigned=c, latest=latest,
                         hh_turnover=hh_rev / get("hh.assets"), hh_leverage=get("hh.assets") / get("hh.equity"),
                         hh_roe=hh_ni / get("hh.equity"), hh_rd=get("hh.rd") / hh_rev, hh_gm=get("hh.gp") / hh_rev,
                         hh_inv_days=get("hh.inventory") / (hh_rev - get("hh.gp")) * 365,
                         flex_staff=get("flex.staff"), flex_china=get("flex.china"), jbl_a=get("jbl.custa"),
                         flex_regions={k: get(f"flex.staff.{k}") for k in ("am", "asia", "eu")})

    # --- Hon Hai ----------------------------------------------------------------------------------------------------------
    prod = {k: (get(f"hh.prod.{k}.2024"), get(f"hh.prod.{k}")) for k in ("sce", "cloud", "computing", "components")}
    R["honhai"] = dict(prod=prod, client_e=(get("hh.client_e.2024") / get("hh.rev.2024"), get("hh.client_e") / hh_rev),
                       fii_margin=get("hh.fii.op") / get("hh.fii.rev"), op_margin=hh_op / hh_rev,
                       parent_margin=get("hh.parent.op") / get("hh.parent.rev"), fii_rev=get("hh.fii.rev"),
                       parent_rev=get("hh.parent.rev"),
                       loc={k: get(f"hh.loc.{k}") for k in ("us", "sg", "ie", "cn", "tw", "jp", "in", "other")},
                       op_margin24=get("hh.op.2024") / get("hh.rev.2024"), rev24=get("hh.rev.2024"), rev25=hh_rev)

    # --- the brand ----------------------------------------------------------------------------------------------------------
    aapl = sec["AAPL"]
    a26 = aapl[max(aapl)]
    R["brand"] = dict(rev=a26["revenue"], ni=a26["net_income"], gp_products=get("aapl.gp.products"),
                      gp_services=get("aapl.gp.services"), gm_products=get("aapl.gm.products"),
                      gm_services=get("aapl.gm.services"), iphone=get("apple.iphone_sales.fy2026"),
                      services=get("apple.services_sales.fy2026"), staff=get("aapl.staff"),
                      hh_ni_usd=hh_ni / twd25, hh_rev_usd=hh_rev / twd25,
                      margins={tk: margin_by_year(tk) for tk in ("AAPL", "DELL", "HPQ", "LOGI")},
                      gm_hist={"products": {2024: get("aapl.gm.products.2024"), 2025: get("aapl.gm.products.2025"), 2026: get("aapl.gm.products")},
                               "services": {2024: get("aapl.gm.services.2024"), 2025: get("aapl.gm.services.2025"), 2026: get("aapl.gm.services")}})

    # --- components ---------------------------------------------------------------------------------------------------------
    comp = {tk: {y: m for y, m in margin_by_year(tk).items() if 2012 <= y <= 2025} for tk in COMPONENTS}
    for tk in ("LPL", "ASX"):
        comp[tk] = {int(e[:4]): r["profit"] / r["revenue"] for e, r in foreign[tk].items() if r.get("profit") is not None
                    and 2012 <= int(e[:4]) <= 2025}
    R["components"] = dict(margins=comp)

    # --- history: prices -----------------------------------------------------------------------------------------------------
    cpi: dict = collections.defaultdict(dict)
    for r in read("bls_elec"):
        cpi[r["item"]][int(r["year"])] = r["value"]
    tv, allc = cpi["SERA01"], cpi["SA0"]
    real_tv = {y: (tv[y] / allc[y]) / (tv[1951] / allc[1951]) for y in tv if y in allc}
    comp_p = cpi["SEEE01"]
    R["history"] = dict(tv=tv, all=allc, real_tv=real_tv, tv_fall=1 - tv[2025] / tv[1951], real_tv_fall=1 - real_tv[2025],
                        cpi_x=allc[2025] / allc[1951], computers=comp_p, comp_fall=1 - comp_p[2025] / comp_p[1998],
                        phones=cpi["SSEE041"], phone_first=min(cpi["SSEE041"]),
                        phone_fall=1 - cpi["SSEE041"][2025] / cpi["SSEE041"][min(cpi["SSEE041"])],
                        ip_comp=_annual(fred["IPG3341S"]))

    # --- the PC ---------------------------------------------------------------------------------------------------------------
    R["pc"] = dict(intel={y: (get(f"intc.ccg.{y}"), get(f"intc.ccg.op.{y}")) for y in (2023, 2024, 2025)},
                   hp={y: (get(f"hpq.ps.{y}"), get(f"hpq.ps.op.{y}")) for y in (2023, 2024, 2025)},
                   dell={y: (get(f"dell.csg.{y}"), get(f"dell.csg.op.{y}")) for y in (2024, 2025, 2026)},
                   hp_print=(get("hpq.print"), get("hpq.print.op")), hp_supplies=get("hpq.supplies"))

    # --- trade: Comtrade -----------------------------------------------------------------------------------------------------
    trade: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    units: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("comtrade_us"):
        hs = str(int(r["hs"]))
        key = "phones" if hs in ("851712", "851713") else {"847130": "laptops", "847150": "servers", "852872": "tvs"}[hs]
        y = int(r["year"])
        trade[key][r["partner"]][y] = trade[key][r["partner"]].get(y, 0.0) + float(r["imports_usd_bn"])
        if r.get("qty"):
            units[key][r["partner"]][y] = units[key][r["partner"]].get(y, 0.0) + float(r["qty"]) / 1e6
    trade = {k: {p: dict(v) for p, v in d_.items()} for k, d_ in trade.items()}
    units = {k: {p: dict(v) for p, v in d_.items()} for k, d_ in units.items()}
    R["servers"] = dict(imports=trade["servers"], cloud=(get("hh.prod.cloud.2024"), get("hh.prod.cloud")),
                        sce=(get("hh.prod.sce.2024"), get("hh.prod.sce")), fii_margin=get("hh.fii.op") / get("hh.fii.rev"),
                        smci={_fy(e): r["revenue"] for e, r in sec["SMCI"].items()},
                        cls={_fy(e): r["revenue"] for e, r in sec["CLS"].items()},
                        dell_ai={y: get(f"dell.ai.{y}") for y in (2024, 2025, 2026)}, dell_isg=(get("dell.isg.2026"), get("dell.isg.op.2026")),
                        dell_csg=(get("dell.csg.2026"), get("dell.csg.op.2026")),
                        margins={tk: margin_by_year(tk) for tk in ("CLS", "SMCI")})

    # --- the cluster ----------------------------------------------------------------------------------------------------------
    nca = {k: (get(f"hh.nca.{k}.2024"), get(f"hh.nca.{k}")) for k in ("cn", "vn", "us", "in", "tw", "mx", "other")}
    jobs = _annual(fred["CEU3133400001"])
    R["cluster"] = dict(nca=nca, jobs=jobs, jobs_peak=max(jobs.values()), jobs_peak_year=max(jobs, key=jobs.get),
                        mexico={k: (trade[k]["Mexico"][2017], trade[k]["Mexico"][2025]) for k in ("servers", "laptops", "tvs", "phones")})
    R["components"]["memory_share"] = (get("bom.memory_share.2025"), get("bom.memory_share.2026"))
    R["components"]["bom_rise"] = get("bom.rise.18pro")

    # --- tariffs ---------------------------------------------------------------------------------------------------------------
    share = {k: {y: trade[k]["China"].get(y, 0) / trade[k]["World"][y] for y in trade[k]["World"]} for k in ("phones", "laptops")}
    R["tariffs"] = dict(phones=trade["phones"], laptops=trade["laptops"], tvs=trade["tvs"], china_share=share, units=units,
                        unit_value={k: {y: trade[k]["World"][y] * 1e3 / units[k]["World"][y] for y in units[k]["World"] if units[k]["World"][y]}
                                    for k in ("phones", "laptops")},
                        r2018=get("ustr.2018"), share_rule=get("ustr.2019.share"), r2019=get("ustr.2019.rate"))

    # --- landscape ---------------------------------------------------------------------------------------------------------------
    comps = []
    for g, tks in GROUPS.items():
        for tk in tks:
            if tk == "HONHAI":
                comps.append(dict(ticker=tk, group=g, revenue=hh_rev / twd25, year="2025",
                                  margin=float(np.mean([get("hh.ni.2024") / get("hh.rev.2024"), hh_ni / hh_rev]))))
                continue
            if tk in ("SONY", "LPL", "ASX"):
                rows = foreign[tk]
                end = max(e for e in rows if rows[e].get("revenue"))
                rate = {"SONY": fx["AEXJPUS"], "LPL": fx["AEXKOUS"], "ASX": fx["AEXTAUS"]}[tk]
                y = int(end[:4]) - (1 if tk == "SONY" else 0)   # Sony's year ends in March
                rev = rows[end]["revenue"] / rate[y]
                ms = [rows[e]["profit"] / rows[e]["revenue"] for e in sorted(rows)[-5:] if rows[e].get("profit") is not None]
                comps.append(dict(ticker=tk, group=g, revenue=rev, margin=float(np.mean(ms)), year=end[:4]))
                continue
            rows = sec[tk]
            ends = sorted(rows)
            ms = [rows[e]["net_income"] / rows[e]["revenue"] for e in ends[-5:] if rows[e].get("net_income") is not None]
            comps.append(dict(ticker=tk, group=g, revenue=rows[ends[-1]]["revenue"], margin=float(np.mean(ms)), year=ends[-1][:4]))
    six = sum(latest[tk]["revenue"] for tk in ASSEMBLERS)
    R["landscape"] = dict(companies=comps, six=six, hh_usd=hh_rev / twd25)

    # --- called ------------------------------------------------------------------------------------------------------------------
    mon: dict = collections.defaultdict(dict)
    for r in read("comtrade_us_m"):
        if str(int(r["hs"])) == "851713":
            mon[r["partner"]][str(r["month"])] = float(r["imports_usd_bn"])
    months26 = sorted(m for m in mon["World"] if m.startswith("2026"))
    ytd = {p: sum(mon[p].get(m, 0) for m in months26) for p in ("World", "China", "India", "Vietnam")}
    last4_25 = {p: sum(mon[p].get(f"2025-{k:02d}", 0) for k in (9, 10, 11, 12)) for p in ("World", "China", "India")}
    # if September-December 2026 repeats September-December 2025
    proj = {p: ytd[p] + last4_25[p] for p in ("World", "China", "India")}
    R["called"] = dict(lutnick=get("lutnick.2025"), phones=trade["phones"], monthly=dict(mon), months26=months26,
                       ytd=ytd, ytd_share=ytd["India"] / ytd["World"], last4_25=last4_25, proj=proj,
                       proj_share=proj["India"] / proj["World"], threshold=0.5, prob=0.55,
                       jobs24=jobs.get(2024), jobs25=jobs.get(2025))
    W4 = last4_25["World"]
    R["called"]["need"] = (0.5 * (ytd["World"] + W4) - ytd["India"]) / W4
    R["called"]["last_autumn"] = last4_25["India"] / W4
    R["called"]["curve"] = {round(x, 2): (ytd["India"] + x * W4) / (ytd["World"] + W4) for x in np.linspace(0.1, 0.7, 13)}
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    h = R["hook"]
    print("hook", {k: round(v, 4) for k, v in h.items()})
    print("run", {k: (round(v["no"]), round(v["yes"]), round(v["exp"]), v["even"]) for k, v in R["run"]["games"].items()}, "cross", R["run"]["cross"])
    print("dollar", R["dollar"]["split"])
    c = R["contract"]
    print("contract", {tk: round(100 * c["margins"][tk].get(2025, float("nan")), 1) for tk in c["margins"]},
          "turnover", round(c["hh_turnover"], 2), "lev", round(c["hh_leverage"], 2), "roe", round(c["hh_roe"], 3),
          "rd", round(c["hh_rd"], 4), "inv days", round(c["hh_inv_days"]))
    print("honhai", R["honhai"]["prod"], [round(x, 3) for x in R["honhai"]["client_e"]], round(R["honhai"]["fii_margin"], 4))
    b = R["brand"]
    print("brand", round(b["rev"], 1), round(b["ni"], 1), "hh ni usd", round(b["hh_ni_usd"], 2))
    print("components", {k: round(100 * v.get(2024, float("nan")), 1) for k, v in R["components"]["margins"].items()})
    hs = R["history"]
    print("history tv fall", round(hs["tv_fall"], 4), "real", round(hs["real_tv_fall"], 4), "cpi x", round(hs["cpi_x"], 1),
          "computers fall", round(hs["comp_fall"], 3), "phones fall", round(hs["phone_fall"], 3))
    print("pc", R["pc"])
    print("servers", {p: round(v.get(2025, 0), 1) for p, v in R["servers"]["imports"].items()})
    print("cluster", R["cluster"]["nca"], round(R["cluster"]["jobs_peak"]), R["cluster"]["jobs_peak_year"], round(R["cluster"]["jobs"].get(2025, 0)))
    print("tariffs china share", {k: {y: round(v, 2) for y, v in s.items()} for k, s in R["tariffs"]["china_share"].items()})
    print("landscape", [(x["ticker"], round(x["revenue"], 1), round(100 * x["margin"], 1), x["year"]) for x in R["landscape"]["companies"]])
    cl = R["called"]
    print("called", cl["months26"][-1], {k: round(v, 1) for k, v in cl["ytd"].items()}, round(cl["ytd_share"], 3),
          {k: round(v, 1) for k, v in cl["proj"].items()}, round(cl["proj_share"], 3))


if __name__ == "__main__":
    main()
