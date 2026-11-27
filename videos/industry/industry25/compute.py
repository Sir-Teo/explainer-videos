"""Every number in Part 25 of *Industry, Built* ("Homes"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry25.compute        # prints the film's numbers; writes .cache/industry25/computed.json

Items:
    hook        house prices against all prices since 1987; the mortgage payment on a median new house, 2021 and 2026
    run         the Run it decision: own the lot or option it, through a boom or a bust (the Works)
    builder     D.R. Horton, Lennar and NVR: closings, prices, margins, incentives, land owned against controlled
    supply      housing starts since 1959; months' supply
    prices      house prices against construction inputs and consumer prices since 2000; price against income
    mortgage    the 30-year rate since 1971; the payment on a median new house each year; Fannie Mae; the lock-in
    rent        rents against prices; homeownership; Invitation Homes
    trade       the brokers and portals, the home-improvement stores and the factory-built homes (SEC)
    landscape   the companies by revenue and margin
    called      D.R. Horton's guidance against outcomes; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import builder

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry25"

NAMES = {"DHI": ("D.R. Horton", "builder"), "LEN": ("Lennar", "builder"), "PHM": ("PulteGroup", "builder"),
         "NVR": ("NVR", "builder"), "TOL": ("Toll Brothers", "builder"), "KBH": ("KB Home", "builder"),
         "MTH": ("Meritage", "builder"), "CCS": ("Century Communities", "builder"), "MHO": ("M/I Homes", "builder"),
         "DFH": ("Dream Finders", "builder"), "LGIH": ("LGI Homes", "builder"), "CVCO": ("Cavco", "factory"),
         "SKY": ("Champion Homes", "factory"), "BLDR": ("Builders FirstSource", "supply"), "HD": ("Home Depot", "supply"),
         "LOW": ("Lowe's", "supply"), "UWMC": ("UWM", "mortgage"), "Z": ("Zillow", "broker"), "COMP": ("Compass", "broker"),
         "OPEN": ("Opendoor", "broker"), "INVH": ("Invitation Homes", "landlord")}


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


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_homes"):
        if r.get("revenue"):
            sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    f = _monthly(read("fred_homes"))

    cpi = _annual(f["CPIAUCNS"], need=11)  # the BLS published no October 2025 CPI
    cs = _annual(f["CSUSHPINSA"], need=9)
    real = {y: (cs[y] / cs[1987]) / (cpi[y] / cpi[1987]) for y in cs if y in cpi and y >= 1987}
    rate = f["MORTGAGE30US"]
    price = f["MSPNHSUS"]
    m21, m26 = "2021-01", max(m for m in price if m in rate)
    pay = {m: builder.payment(0.9 * price[m], rate[m] / 100) for m in (m21, m26)}
    R["hook"] = dict(real=real, peak06=max((y for y in real if y <= 2010), key=real.get), m21=m21, m26=m26,
                     price={m21: price[m21], m26: price[m26]}, rate={m21: rate[m21], m26: rate[m26]}, pay=pay,
                     rate_now=rate[max(rate)], rate_month=max(rate))

    d = builder.LandDeal()
    sweep = {round(p, 2): (builder.LandDeal(p_bust=p).expected("own"), builder.LandDeal(p_bust=p).expected("option"))
             for p in np.arange(0, 1.01, 0.05)}
    R["run"] = dict(table=d.table(), breakeven=d.breakeven_bust(), sweep=sweep, price=d.price, lot=d.lot, build=d.build,
                    overhead=d.overhead, years=d.years, carry=d.carry, escalator=d.escalator, deposit=d.deposit,
                    boom=d.boom, bust=d.bust, p_bust=d.p_bust, sale={s: d.sale(s) for s in ("boom", "bust")},
                    margin_now=(d.price - d.lot - d.build - d.overhead * d.price) / d.price)

    R["builder"] = dict(dhi=dict(rev=get("dhi.rev"), closed=get("dhi.closed"), price=get("dhi.price"), gm=get("dhi.gm"),
                                 gm_prev=get("dhi.gm.prev"), pretax=get("dhi.pretax"), owned=get("dhi.owned"),
                                 controlled=get("dhi.controlled"), owned25=get("dhi.owned.2025"),
                                 controlled25=get("dhi.controlled.2025"), unsold=get("dhi.unsold")),
                        len=dict(deliveries=get("len.deliveries"), price={2023: get("len.price.2023"), 2024: get("len.price.2024"),
                                                                           2025: get("len.price")},
                                 gm=(get("len.gm.prev"), get("len.gm")), incent=(get("len.incent.prev"), get("len.incent")),
                                 incent_pct=get("len.incent.pct"), controlled=(get("len.controlled.prev"), get("len.controlled")),
                                 walked=get("len.walked"), writeoff=get("len.writeoff")),
                        nvr=dict(lots=get("nvr.lots"), deposits=get("nvr.deposits"), price=get("nvr.price"),
                                 settle=get("nvr.settle"), gm=get("nvr.gm"),
                                 per_lot=get("nvr.deposits") * 1e3 / get("nvr.lots")))

    starts = _annual(f["HOUST"])
    R["supply"] = dict(starts={y: v for y, v in starts.items() if y <= 2025}, peak=max((y for y in starts if y <= 2010), key=starts.get),
                       low=min((y for y in starts if 2005 <= y <= 2015), key=starts.get),
                       supply=_annual(f["MSACSR"]), sales=_annual(f["HSN1F"]))

    ppi = _annual(f["WPUIP2311001"], need=11)
    base = 2000
    R["prices"] = dict(cs={y: cs[y] / cs[base] for y in cs if base <= y <= 2025}, ppi={y: ppi[y] / ppi[base] for y in ppi if base <= y <= 2025},
                       cpi={y: cpi[y] / cpi[base] for y in cpi if base <= y <= 2025}, base=base)
    mspus = _annual(f["MSPUS"], need=3)
    inc = {int(m[:4]): v for m, v in f["MEHOINUSA646N"].items()}
    R["prices"]["ratio"] = {y: mspus[y] / inc[y] for y in inc if y in mspus and y >= 1984}

    rate_y = _annual(rate)
    newp = _annual(price)
    payy = {y: builder.payment(0.9 * newp[y], rate_y[y] / 100) * 12 / inc[y] for y in inc if y in rate_y and y in newp and y >= 1984}
    debt = {int(m[:4]): v for m, v in f["HHMSDODNS"].items() if m.endswith("-10") or m.endswith("-04")}
    R["mortgage"] = dict(rate={y: v for y, v in rate_y.items() if y <= 2025}, pay_share=payy, book=get("fnm.book"), share=get("fnm.share"),
                         debt_total=get("fnm.debt"), lock=get("fnm.lock"), orig=(get("fnm.orig.2025"), get("fnm.orig.2026")),
                         refi=(get("fnm.refi.2025"), get("fnm.refi.2026")),
                         hh_debt=f["HHMSDODNS"][max(f["HHMSDODNS"])] / 1e6, hh_debt_q=max(f["HHMSDODNS"]),
                         rate_2026={m: v for m, v in rate.items() if m >= "2025-01"})
    rent = _annual(f["CUSR0000SEHA"], need=11)
    R["extra"] = dict(months=_annual(f["MSACSR"]), newp={y: v for y, v in _annual(price).items() if y <= 2025},
                      delinq=_annual(f["DRSFRMACBS"], need=4),
                      loan=0.9 * price[m26], bal5={k: builder.balance(0.9 * price[m26], k / 100, 60) for k in (2.735, 7.328)},
                      bfs={y: (sec["BLDR"][y]["revenue"], sec["BLDR"][y]["profit"] / sec["BLDR"][y]["revenue"]) for y in sorted(sec["BLDR"]) if y >= 2019},
                      uwm={y: (sec["UWMC"][y]["revenue"], sec["UWMC"][y]["profit"] / sec["UWMC"][y]["revenue"]) for y in sorted(sec["UWMC"]) if y >= 2021})
    R["rent"] = dict(rent={y: rent[y] / rent[base] for y in rent if base <= y <= 2025}, own=_annual(f["RHORUSQ156N"], need=4),
                     vacancy=_annual(f["RRVRUSQ156N"], need=4), invh=get("invh.homes"))

    R["trade"] = {NAMES[tk][0]: {y: (sec[tk][y]["revenue"], sec[tk][y]["profit"] / sec[tk][y]["revenue"] if sec[tk][y].get("profit") is not None else None)
                                 for y in sorted(sec[tk]) if y >= 2018} for tk in ("Z", "COMP", "OPEN", "HD", "LOW", "CVCO", "SKY", "INVH")}
    R["trade"]["nar"] = get("comp.anywhere")

    comp = []
    for tk, (nm, grp) in NAMES.items():
        if not sec[tk]:
            continue
        y = max(sec[tk])
        r = sec[tk][y]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in sec[tk] if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=r["revenue"], margin=float(np.median(mm)), fy=y, tk=tk))
    R["landscape"] = dict(companies=comp)

    R["called"] = dict(g26_rev=(get("dhi.g26.rev.lo"), get("dhi.g26.rev.hi")), g26_homes=(get("dhi.g26.homes.lo"), get("dhi.g26.homes.hi")),
                       a26=(get("dhi.rev"), get("dhi.closed")), a25=get("dhi.closed.2025"),
                       g27_rev=(get("dhi.g27.rev.lo"), get("dhi.g27.rev.hi")), g27_homes=(get("dhi.g27.homes.lo"), get("dhi.g27.homes.hi")),
                       orders_q4=get("dhi.orders.q4"), call=81500, prob=0.60, fnm=(get("fnm.orig.2025"), get("fnm.orig.2026")))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("hook", H["m21"], H["m26"], H["price"], H["rate"], {k: round(v) for k, v in H["pay"].items()}, "peak", H["peak06"],
          round(H["real"][H["peak06"]], 2), round(H["real"][2025], 2), H["rate_now"], H["rate_month"])
    print("run", {k: {a: round(b, 2) for a, b in v.items()} for k, v in R["run"]["table"].items()}, round(R["run"]["breakeven"], 3),
          round(R["run"]["margin_now"], 3))
    S = R["supply"]
    print("starts", S["peak"], round(S["starts"][S["peak"]]), S["low"], round(S["starts"][S["low"]]), round(S["starts"][2025]),
          {y: round(v) for y, v in S["starts"].items() if y in (1972, 1986, 2005, 2009, 2021)})
    P = R["prices"]
    print("prices 2025", round(P["cs"][2025], 2), round(P["ppi"][2025], 2), round(P["cpi"][2025], 2), "ratio", {y: round(v, 2) for y, v in P["ratio"].items() if y in (1984, 2000, 2006, 2012, 2020, 2022, 2024, 2025)})
    M = R["mortgage"]
    print("pay share", {y: round(100 * v, 1) for y, v in M["pay_share"].items() if y in (1984, 1990, 2000, 2006, 2012, 2020, 2021, 2023, 2024, 2025)},
          "hh debt", round(M["hh_debt"], 2), M["hh_debt_q"])
    print("rent", round(R["rent"]["rent"][2025], 2), {y: round(v, 1) for y, v in R["rent"]["own"].items() if y in (1965, 1980, 2004, 2016, 2020, 2025)})
    print("trade", {k: {y: (round(a, 2), round(100 * b, 1) if b is not None else None) for y, (a, b) in v.items() if y >= 2021} for k, v in R["trade"].items() if k != "nar"})
    print("landscape", [(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]])


if __name__ == "__main__":
    main()
