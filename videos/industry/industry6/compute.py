"""Every number in Part 6 of *Industry, Built* ("The Cycle"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry6.compute        # prints the film's numbers; writes .cache/industry6/computed.json

Items:
    micron      Micron's fiscal years 2009-2026 and its quarters: revenue, operating income, capital spending and
                depreciation; every peak quarter and the fall that followed
    maersk      Maersk's group revenue and operating profit, 2019-2025 (ESEF filings)
    ships       UNCTAD's ships on order against the fleet
    hogs        Chicago hog prices and US hogs slaughtered, 1880-1940 (NBER): the cycle's length and lags
    cobweb      Ezekiel's model, two paths for the screen
    fleet       the Works' shipping market with lead times of 1 to 4 years, and one long run to animate
    housing     housing starts, houses under construction and completed, months' supply, 2000-2026
    oil         West Texas crude and Exxon Mobil's capital spending
    bullwhip    retail sales against factory orders (FRED), and the Works' chain of four tiers
    leverage    operating leverage in Micron's fiscal 2023 and Maersk's 2023
    reading     capital spending against depreciation at peaks and troughs
    intel       the dated call of a peak: Intel's 2021 announcement and what followed
    base_rate   for this series' call: how far Micron's quarterly revenue fell within two years of each peak
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import cycle

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry6"


def _fred() -> dict:
    S: dict = collections.defaultdict(dict)
    for r in read("fred_cycle"):
        S[r["series"]][r["month"]] = r["value"]
    return S


def _monthly(S, sid, y0, y1):
    keys = [f"{y}-{m:02d}" for y in range(y0, y1 + 1) for m in range(1, 13)]
    return keys, np.array([S[sid].get(k, np.nan) for k in keys], dtype=float)


def _ma(x, w):
    return np.convolve(x, np.ones(w) / w, mode="same")


def _annual(rows, tic, key):
    return {int(r["year_end"][:4]) if r["year_end"][5:7] > "06" else int(r["year_end"][:4]) - 1: r[key]
            for r in rows if r["ticker"] == tic and r.get(key) is not None}


def _fy(rows, tic, key):
    """A fiscal year labelled by the calendar year it ends in (Micron's ends in late August or early September)."""
    return {int(r["year_end"][:4]): r[key] for r in rows if r["ticker"] == tic and r.get(key) is not None}


def peaks(values: list, ends: list, window: int = 4, horizon: int = 8, floor: float = 0.0) -> list[dict]:
    """Quarters higher than the ``window`` quarters on each side (the last quarter counts when it is the highest yet),
    each with the lowest quarter in the ``horizon`` quarters that followed and the fall to it."""
    out = []
    n = len(values)
    for i in range(n):
        lo, hi = max(0, i - window), min(n, i + window + 1)
        if values[i] != max(values[lo:hi]) or values[i] < floor:
            continue
        after = values[i + 1:i + 1 + horizon]
        if not after:
            out.append(dict(end=ends[i], value=values[i], low=None, low_end=None, fall=None, open=True))
            continue
        j = int(np.argmin(after))
        out.append(dict(end=ends[i], value=values[i], low=after[j], low_end=ends[i + 1 + j],
                        fall=after[j] / values[i] - 1, open=len(after) < horizon))
    return out


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec = read("sec_annual")
    q = [r for r in read("sec_quarterly") if r["ticker"] == "MU"]

    # --- Micron ------------------------------------------------------------------------------------------------------
    mu = {k: _fy(sec, "MU", k) for k in ("revenue", "operating_income", "capex", "depreciation", "inventory")}
    years = sorted(y for y in mu["revenue"] if y >= 2010)
    qe = [r["quarter_end"] for r in q]
    qv = [r["revenue"] for r in q]
    qo = [r["operating_income"] for r in q]
    pk = peaks(qv, qe, floor=2.0)
    R["micron"] = dict(years=years, revenue=[mu["revenue"][y] for y in years],
                       operating_income=[mu["operating_income"][y] for y in years],
                       capex=[mu["capex"][y] for y in years], depreciation=[mu["depreciation"][y] for y in years],
                       quarters=qe, q_revenue=qv, q_operating=qo, peaks=pk,
                       fy23=dict(revenue=mu["revenue"][2023], oi=mu["operating_income"][2023]),
                       fy26=dict(revenue=mu["revenue"][2026], oi=mu["operating_income"][2026],
                                 capex=mu["capex"][2026], dep=mu["depreciation"][2026]),
                       q4_26=dict(revenue=qv[-1], oi=qo[-1], margin=qo[-1] / qv[-1], end=qe[-1]),
                       q4_25=dict(revenue=qv[-5], end=qe[-5]))

    # --- Maersk ------------------------------------------------------------------------------------------------------
    mk = read("esef_maersk")
    R["maersk"] = dict(years=[int(r["year"]) for r in mk], revenue=[r["revenue"] for r in mk],
                       ebit=[r["ebit"] for r in mk], depreciation=[r["depreciation"] for r in mk])

    # --- ships on order --------------------------------------------------------------------------------------------
    R["ships"] = dict(book={2009: get("ships.book.2009"), 2014: get("ships.book.2014"), 2023: get("ships.book.2023"),
                            2024: get("ships.book.2024"), 2025: get("ships.book.2025")},
                      bulk2009=get("ships.book.bulk.2009"), box2025=get("ships.book.box.2025"),
                      box_delivered2024=get("ships.delivered.box.2024"))

    # --- hogs, 1880-1940 ---------------------------------------------------------------------------------------------
    S = _fred()
    keys, price = _monthly(S, "M04008US16980M275NNBR", 1880, 1940)
    _, slaughter = _monthly(S, "M01039USM566NNBR", 1880, 1940)
    lp, lq = _ma(np.log(price), 12), _ma(np.log(slaughter), 12)   # a year's average: no seasons
    dp, dq = (lp - _ma(lp, 61))[60:-60], (lq - _ma(lq, 61))[60:-60]  # against the five-year trend
    lags = list(range(-36, 37, 6))

    def corr_at(lag):  # slaughter ``lag`` months after the price
        a = dp[:len(dp) - lag] if lag >= 0 else dp[-lag:]
        b = dq[lag:] if lag >= 0 else dq[:len(dq) + lag]
        return float(np.corrcoef(a, b)[0, 1])

    def period(x):
        x = x - x.mean()
        f = np.fft.rfftfreq(len(x), 1 / 12)
        pw = np.abs(np.fft.rfft(x)) ** 2
        m = (f > 1 / 12) & (f < 1 / 1.5)
        return float(1 / f[np.argmax(pw * m)])
    ann_p = [float(np.mean(price[12 * k:12 * k + 12])) for k in range(61)]
    ann_q = [float(np.mean(slaughter[12 * k:12 * k + 12])) for k in range(61)]
    R["hogs"] = dict(years=list(range(1880, 1941)), price=ann_p, slaughter=ann_q,
                     dev_months=keys[60:-60], dev_price=dp.tolist(), dev_slaughter=dq.tolist(),
                     lags=lags, corr=[corr_at(L) for L in lags], same=corr_at(0),
                     best_lag=max((L for L in lags if L > 0), key=corr_at), best=max(corr_at(L) for L in lags if L > 0),
                     period_slaughter=period(dq), period_price=period(dp))

    # --- the cobweb (model) ------------------------------------------------------------------------------------------
    pe, qe_ = cycle.cobweb_eq(10, 1, 0, 0.8)
    p1, q1 = cycle.cobweb(10, 1, 0, 0.8, pe + 2.6, n=10)
    R["cobweb"] = dict(eq=(pe, qe_), damped=(p1.tolist(), q1.tolist()))

    # --- the Works' fleet ------------------------------------------------------------------------------------------
    runs = {L: cycle.fleet(years=60, lead=L, k=0.35) for L in (1, 2, 3, 4)}
    R["fleet"] = dict(swing={L: cycle.swing(f["rate"], 15) for L, f in runs.items()},
                      run={k: v[10:50].tolist() for k, v in runs[3].items()},
                      book_max={L: float(f["orderbook"][15:].max()) for L, f in runs.items()},
                      rates={L: f["rate"][10:50].tolist() for L, f in runs.items()})

    # --- housing ---------------------------------------------------------------------------------------------------
    H = {}
    for sid in ("HOUST", "UNDCONTSA", "COMPUTSA", "MSACSR"):
        ks, v = _monthly(S, sid, 2000, 2026)
        ok = ~np.isnan(v)
        H[sid] = dict(months=[k for k, o in zip(ks, ok) if o], values=v[ok].tolist())
    hs = dict(zip(H["HOUST"]["months"], H["HOUST"]["values"]))
    ms = dict(zip(H["MSACSR"]["months"], H["MSACSR"]["values"]))
    pk_h = max((k for k in hs if k < "2008"), key=hs.get)
    tr_h = min((k for k in hs if pk_h < k < "2012"), key=hs.get)
    pk_m = max((k for k in ms if "2005" < k < "2012"), key=ms.get)
    R["housing"] = dict(series=H, starts_peak=(pk_h, hs[pk_h]), starts_trough=(tr_h, hs[tr_h]),
                        fall=hs[tr_h] / hs[pk_h] - 1, supply_peak=(pk_m, ms[pk_m]), latest=(max(hs), hs[max(hs)]))

    # --- oil ---------------------------------------------------------------------------------------------------------
    ks, w = _monthly(S, "DCOILWTICO", 2000, 2026)
    ok = ~np.isnan(w)
    xom = _fy(sec, "XOM", "capex")
    R["oil"] = dict(months=[k for k, o in zip(ks, ok) if o], wti=w[ok].tolist(),
                    xom_years=sorted(xom), xom_capex=[xom[y] for y in sorted(xom)],
                    wti_2014_06=S["DCOILWTICO"]["2014-06"], wti_2016_02=S["DCOILWTICO"]["2016-02"])

    # --- the bullwhip ------------------------------------------------------------------------------------------------
    ks, rs = _monthly(S, "RSXFS", 1993, 2026)
    _, no = _monthly(S, "AMTMNO", 1993, 2026)
    ok = ~np.isnan(rs) & ~np.isnan(no)
    rs, no = rs[ok], no[ok]
    g_rs, g_no = np.diff(np.log(rs)), np.diff(np.log(no))
    rng = np.random.default_rng(6)
    sales = 100 + rng.normal(0, 4, 160)
    chain = cycle.bullwhip(sales, tiers=3)
    R["bullwhip"] = dict(sd_retail=float(np.std(g_rs)), sd_orders=float(np.std(g_no)),
                         ratio=float(np.std(g_no) / np.std(g_rs)), months=int(ok.sum()),
                         chain=chain[:, 20:100].tolist(), chain_sd=[float(np.std(chain[i, 20:])) for i in range(4)])

    # --- operating leverage ----------------------------------------------------------------------------------------
    m = R["micron"]
    i22, i23 = m["years"].index(2022), m["years"].index(2023)
    mk_i = R["maersk"]["years"]
    a, b = mk_i.index(2022), mk_i.index(2023)
    R["leverage"] = dict(
        micron=dict(rev=(m["revenue"][i22], m["revenue"][i23]), oi=(m["operating_income"][i22],
                    m["operating_income"][i23]), dep=(m["depreciation"][i22], m["depreciation"][i23])),
        maersk=dict(rev=(R["maersk"]["revenue"][a], R["maersk"]["revenue"][b]),
                    ebit=(R["maersk"]["ebit"][a], R["maersk"]["ebit"][b]),
                    dep=(R["maersk"]["depreciation"][a], R["maersk"]["depreciation"][b])),
        model=cycle.leverage(100.0, 80.0, fixed=30.0, variable_share=0.5))

    # --- reading where you are: capital spending against depreciation ---------------------------------------------
    intc = {k: _fy(sec, "INTC", k) for k in ("capex", "depreciation", "operating_income", "revenue")}
    xd = _fy(sec, "XOM", "depreciation")
    R["reading"] = dict(
        micron=[(y, m["capex"][k] / m["depreciation"][k]) for k, y in enumerate(m["years"])],
        intel={y: intc["capex"][y] / intc["depreciation"][y] for y in (2021, 2022, 2023, 2024, 2025)},
        exxon={y: xom[y] / xd[y] for y in (2013, 2014, 2016, 2021, 2025) if y in xd})

    # --- the dated call of a peak: Intel ---------------------------------------------------------------------------
    R["intel"] = dict(announced=get("intel.az.2021"),
                      years=list(range(2019, 2026)), capex=[intc["capex"][y] for y in range(2019, 2026)],
                      oi=[intc["operating_income"][y] for y in range(2019, 2026)],
                      revenue=[intc["revenue"][y] for y in range(2019, 2026)])

    # --- base rate for the call ------------------------------------------------------------------------------------
    closed = [p for p in pk if not p["open"] and p["fall"] is not None]
    R["base_rate"] = dict(peaks=closed, falls=[p["fall"] for p in closed],
                          hits=sum(p["fall"] <= -0.25 for p in closed), n=len(closed))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    m = R["micron"]
    print(f"Micron FY2023 revenue ${m['fy23']['revenue']:.1f}bn, operating income ${m['fy23']['oi']:.1f}bn; FY2026 "
          f"${m['fy26']['revenue']:.1f}bn and ${m['fy26']['oi']:.1f}bn; capex ${m['fy26']['capex']:.1f}bn against "
          f"depreciation ${m['fy26']['dep']:.1f}bn")
    print(f"   last quarter ({m['q4_26']['end']}): ${m['q4_26']['revenue']:.1f}bn, margin {100 * m['q4_26']['margin']:.0f}%; "
          f"a year before ${m['q4_25']['revenue']:.1f}bn")
    for p in m["peaks"]:
        f = "open" if p["fall"] is None else f"{100 * p['fall']:+.0f}% by {p['low_end']}"
        print(f"   peak {p['end']} ${p['value']:.2f}bn -> {f}")
    k = R["maersk"]
    print("Maersk " + ", ".join(f"{y}: {r:.1f}/{e:.1f}" for y, r, e in zip(k["years"], k["revenue"], k["ebit"])))
    h = R["hogs"]
    print(f"hogs: same-month r {h['same']:.2f}; slaughter follows price best at +{h['best_lag']} months (r {h['best']:.2f}); "
          f"cycle {h['period_slaughter']:.1f} years (slaughter), {h['period_price']:.1f} (price)")
    print(f"fleet swings by lead time: {R['fleet']['swing']}; orderbook peaks {R['fleet']['book_max']}")
    hs = R["housing"]
    print(f"housing starts {hs['starts_peak']} -> {hs['starts_trough']} ({100 * hs['fall']:.0f}%); months' supply peak "
          f"{hs['supply_peak']}; latest {hs['latest']}")
    o = R["oil"]
    print(f"WTI {o['wti_2014_06']:.0f} (2014-06) -> {o['wti_2016_02']:.0f} (2016-02); Exxon capex "
          + ", ".join(f"{y}: {v:.1f}" for y, v in zip(o["xom_years"], o["xom_capex"]) if y in (2013, 2014, 2016, 2021, 2025)))
    b = R["bullwhip"]
    print(f"bullwhip: sd of monthly change, retail {100 * b['sd_retail']:.2f}% vs factory orders {100 * b['sd_orders']:.2f}% "
          f"(x{b['ratio']:.1f}, {b['months']} months); chain sds {[round(x, 1) for x in b['chain_sd']]}")
    L = R["leverage"]
    print(f"leverage: Micron rev {L['micron']['rev']} oi {L['micron']['oi']}; Maersk rev {L['maersk']['rev']} ebit "
          f"{L['maersk']['ebit']} dep {L['maersk']['dep']}")
    rd = R["reading"]
    print("capex / depreciation: Micron " + ", ".join(f"{y}: {v:.1f}" for y, v in rd["micron"]) + f"; Intel {rd['intel']}; "
          f"Exxon {rd['exxon']}")
    i = R["intel"]
    print(f"Intel: ${i['announced']:.0f}bn announced March 2021; capex {i['capex']}; operating income {i['oi']}")
    br = R["base_rate"]
    print(f"base rate: {br['hits']} of {br['n']} closed peaks fell 25% or more within two years: "
          + ", ".join(f"{100 * f:.0f}%" for f in br["falls"]))


if __name__ == "__main__":
    main()
