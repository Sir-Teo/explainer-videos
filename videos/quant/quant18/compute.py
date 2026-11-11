"""Every number in Part 18 (Money, Bonds and the Curve), computed and cached in .cache/quant18/.

    python -m videos.quant.quant18.compute [items] [--force]

Items (seconds to a few minutes each on a CPU):

* ``policy``     the Fed's administered rates and the market rate between them, 2007-2025 (FRED): target range,
                 interest on reserves, the overnight reverse repo rate, effective fed funds, SOFR; reserves, the
                 balance sheet and the reverse repo facility's take-up;
* ``taylor``     Taylor's (1993) rule against the funds rate, quarterly 1987-2025 (GDP deflator and CBO's potential);
* ``bonds``      a bond's price, yield, duration and convexity: the desk question's numbers and price-yield curves;
* ``curve_day``  Treasury's par yields on two days, bootstrapped to zero and forward curves, fitted by Svensson, and
                 compared with the Fed's own (GSW) curve;
* ``morph``      the GSW zero curve at every month end, 1972-2025 (the morph and the 3D surface);
* ``pca``        principal components of daily curve changes, 1986-2025 and decade by decade;
* ``swaps``      swap spreads (FRED's swap rates minus Treasury yields), 2000-2016, and when they turned negative;
* ``futures``    the 10-year note future's deliverable basket (December 2025): conversion factors, the cheapest to
                 deliver and how it switches as yields move;
* ``sofr``       SOFR compounded in arrears against the rate known at the start, 2018-2025;
* ``term``       expectations versus term premium: Campbell-Shiller and Fama-Bliss regressions, and the
                 Adrian-Crump-Moench term premium re-estimated on the GSW curve against the NY Fed's series;
* ``fomc``       the 2-year yield on FOMC days, 1994-2020, and how far down the curve the news travels;
* ``immunize``   Redington's immunization: matched present value and duration, under parallel and twisting moves;
* ``fly``        a PCA-neutral 2s5s10s butterfly: weights fitted before 2021, a pre-registered mean-reversion rule,
                 and its sealed 2021-2025 hold-out (one trial);
* ``ldi``        a leveraged LDI pool selling into its own price impact (the September 2022 gilt spiral);
* ``svb``        Silicon Valley Bank's held-to-maturity book from its 10-K (EDGAR) and the curve's move in 2022;
* ``envelope``   the trial counter after this part's one registration.
"""

from __future__ import annotations

import inspect
import json

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import pit, rates as R

CACHE = Cache("quant18")
load = pit.counted(CACHE.load, 18, items=("fly",))


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _fred(s, a="1950-01-01", b="2025-12-31"):
    f = data.fred(s, a, b)
    return f["date"], f["value"]


def _weekly(d, v, start=20070101):
    """Every Wednesday's (or the last earlier) value from a daily series."""
    import datetime as dt
    d = np.asarray(d)
    v = np.asarray(v, float)
    out_d, out_v = [], []
    t = dt.date(start // 10000, start // 100 % 100, start % 100)
    end = dt.date(2025, 12, 31)
    while t <= end:
        k = t.year * 10000 + t.month * 100 + t.day
        i = np.searchsorted(d, k, side="right") - 1
        if i >= 0 and d[i] >= k - 7:
            out_d.append(k)
            out_v.append(v[i])
        t += dt.timedelta(days=7)
    return np.array(out_d), np.array(out_v)


def _frac_year(d):
    d = np.asarray(d)
    return d // 10000 + (d // 100 % 100 - 1) / 12 + (d % 100 - 1) / 365


# ---------------------------------------------------------------------------
def compute_policy() -> dict:
    out = {}
    for s in ("DFEDTARU", "DFEDTARL", "DFF", "IOER", "IORB", "RRPONTSYAWARD", "SOFR"):
        d, v = _fred(s, "2007-01-01")
        wd, wv = _weekly(d, v)
        out[s] = {"t": _frac_year(wd), "v": wv}
    # the pre-2008 target was a single number: DFEDTAR (through 2008-12-15)
    d, v = _fred("DFEDTAR", "2007-01-01", "2008-12-15")
    wd, wv = _weekly(d, v)
    out["DFEDTAR"] = {"t": _frac_year(wd), "v": wv}
    for s in ("WRESBAL", "WALCL", "RRPONTSYD"):
        d, v = _fred(s, "2007-01-01")
        wd, wv = _weekly(d, v)
        out[s] = {"t": _frac_year(wd), "v": wv / (1e3 if s != "RRPONTSYD" else 1)}  # billions of dollars
    # the floor: spread of fed funds to interest on reserves, by reserves (weekly, 2009-2025)
    ffd, ffv = _fred("DFF", "2008-10-01")
    iod = np.r_[_fred("IOER", "2008-10-09")[0], _fred("IORB", "2021-07-29")[0]]
    iov = np.r_[_fred("IOER", "2008-10-09")[1], _fred("IORB", "2021-07-29")[1]]
    rd, rv = _fred("WRESBAL", "2009-01-01")
    pts = []
    for k, res in zip(rd, rv):
        i, j = np.searchsorted(ffd, k, side="right") - 1, np.searchsorted(iod, k, side="right") - 1
        if i >= 0 and j >= 0:
            pts.append((k, res / 1e3, (ffv[i] - iov[j]) * 100))
    p = np.array(pts)
    out["floor"] = {"t": _frac_year(p[:, 0]), "reserves": p[:, 1], "spread_bp": p[:, 2]}
    peak = int(np.argmax(out["WALCL"]["v"]))
    out["walcl_peak"] = {"t": out["WALCL"]["t"][peak], "bn": out["WALCL"]["v"][peak]}
    out["walcl_end"] = float(out["WALCL"]["v"][-1])
    out["rrp_peak"] = {"t": out["RRPONTSYD"]["t"][int(np.argmax(out["RRPONTSYD"]["v"]))],
                       "bn": float(np.max(out["RRPONTSYD"]["v"]))}
    rd_, rv_ = _fred("RRPONTSYD", "2007-01-01")
    k = int(np.argmax(rv_))
    out["rrp_daily_max"] = {"date": int(rd_[k]), "bn": float(rv_[k])}

    def at(series, day, scale):
        d_, v_ = _fred(series, "2007-01-01")
        return float(v_[np.searchsorted(d_, day, side="right") - 1] / scale)
    out["qt"] = {k_: {"walcl": at("WALCL", day, 1e6), "reserves": at("WRESBAL", day, 1e6),
                      "rrp": at("RRPONTSYD", day, 1e3)} for k_, day in (("peak", 20220413), ("end", 20251126))}
    return _json(out)


def compute_taylor() -> dict:
    gd, g = _fred("GDPC1", "1985-01-01")
    pd_, p = _fred("GDPPOT", "1985-01-01")
    dd, defl = _fred("GDPDEF", "1985-01-01")
    cd, core = _fred("PCEPILFE", "1985-01-01")
    fd, ff = _fred("FEDFUNDS", "1985-01-01")
    q = gd[gd >= 19870101]
    rows = []
    for k in q:
        i = np.searchsorted(dd, k)
        if i < 4 or np.searchsorted(pd_, k) >= len(pd_):
            continue
        infl = 100 * (defl[i] / defl[i - 4] - 1)
        gap = 100 * (g[np.searchsorted(gd, k)] / p[np.searchsorted(pd_, k)] - 1)
        # core PCE, year over year, at the quarter's last month
        m_end = k + 200  # first month of quarter + 2 months
        j = np.searchsorted(cd, m_end)
        if j >= len(cd) or j < 12:
            continue
        cpi = 100 * (core[j] / core[j - 12] - 1)
        mm = (fd >= k) & (fd < k + 300)
        if mm.sum() < 3:
            continue
        rows.append((k, infl, gap, cpi, ff[mm].mean()))
    a = np.array(rows)
    rule = R.taylor_rule(a[:, 1], a[:, 2])
    rule_core = R.taylor_rule(a[:, 3], a[:, 2])
    t = _frac_year(a[:, 0].astype(int))
    dev = a[:, 4] - rule
    # the widest gaps, by episode
    worst = int(np.argmin(dev))
    return _json({"t": t, "inflation": a[:, 1], "gap": a[:, 2], "core_pce": a[:, 3], "ff": a[:, 4], "rule": rule,
                  "rule_core": rule_core, "worst": {"t": t[worst], "ff": a[worst, 4], "rule": rule[worst]},
                  "dev_2003_05": float(dev[(t >= 2003) & (t < 2006)].mean()),
                  "dev_2021_22": float(dev[(t >= 2021) & (t < 2023)].mean()),
                  "corr_1987_2007": float(np.corrcoef(a[t < 2008, 4], rule[t < 2008])[0, 1])})


def compute_bonds() -> dict:
    z = R.bond_risk(0.0, 0.04, 10, freq=1)
    ys = np.linspace(0.0, 0.12, 121)
    curves = {}
    for T in (2, 10, 30):
        P = np.array([R.bond_price(0.04, y, T) for y in ys])
        rk = R.bond_risk(0.04, 0.04, T)
        tang = rk["price"] * (1 - rk["modified"] * (ys - 0.04))
        quad = tang + rk["price"] * 0.5 * rk["convexity"] * (ys - 0.04) ** 2
        curves[str(T)] = {"P": P, "tangent": tang, "quad": quad, **rk}
    # the 3D surface: price of a 4% bond over yield and maturity
    Ts = np.arange(1, 31)
    surf = np.array([[R.bond_price(0.04, y, T) for y in ys[::4]] for T in Ts])
    # a 100 bp move, three ways, on the 30-year
    r30 = curves["30"]
    move = {}
    for dy in (-0.01, 0.01):
        exact = R.bond_price(0.04, 0.04 + dy, 30) - 100
        move[f"{dy:+.2f}"] = {"exact": exact, "duration": -r30["modified"] * dy * 100,
                              "with_convexity": (-r30["modified"] * dy + 0.5 * r30["convexity"] * dy ** 2) * 100}
    return _json({"zero10": z, "y": ys, "curves": curves, "surf_T": Ts, "surf_y": ys[::4], "surf": surf,
                  "move30": move, "zero10_up1bp": R.bond_price(0.0, 0.0401, 10, freq=1) - z["price"]})


def _gsw_day(g, day):
    i = int(np.searchsorted(g["date"], day))
    b, t = g["beta"][i].copy(), g["tau"][i].copy()
    if np.isnan(t[1]) or np.isnan(b[3]):
        b[3], t[1] = 0.0, 1.0
    return b, t


def compute_curve_day() -> dict:
    g = data.gsw()
    out = {}
    for day in (20230308, 20251231):
        P = data.treasury_par(day // 10000)
        i = int(np.searchsorted(P["date"], day))
        ok = ~np.isnan(P["y"][i])
        T, y = P["tenor"][ok], P["y"][i][ok] / 100
        c = R.bootstrap_par(T, y)
        s = np.linspace(0.1, 30, 300)
        zero = c.zero(s)
        fwd = c.inst_fwd(s)
        f = R.fit_nss(c.t, c.z * 100)
        b, tt = _gsw_day(g, day)
        out[str(day)] = {"tenor": T, "par": y, "nodes_t": c.t, "nodes_z": c.z, "s": s, "zero": zero, "fwd": fwd,
                         "nss": {"beta": f["beta"], "tau": f["tau"], "rmse_bp": 100 * f["rmse"],
                                 "y": R.nss(s, f["beta"], f["tau"]) / 100},
                         "gsw": R.nss(s, b, tt) / 100, "gsw_beta": b, "gsw_tau": tt,
                         "reprice_max_bp": max(abs(c.par(Ti) - yi) for Ti, yi in zip(T, y) if Ti > 1) * 1e4,
                         "spread_2s10s_bp": 100 * (P["y"][i][list(P["tenor"]).index(10.0)]
                                                  - P["y"][i][list(P["tenor"]).index(2.0)])}
    return _json(out)


def compute_morph() -> dict:
    g = data.gsw("1972-01-01")
    m = g["date"] // 100
    idx = np.where(np.r_[m[1:] != m[:-1], True])[0]
    Y = g["y"][idx]
    t = _frac_year(g["date"][idx])
    eras = {}
    for name, day in [("1981 peak", 19810930), ("1993", 19931029), ("2000 inversion", 20000531),
                      ("2008", 20081231), ("2012 low", 20120731), ("2019", 20190830), ("2020 lows", 20200731),
                      ("2023 inversion", 20230630), ("2025", 20251231)]:
        k = int(np.searchsorted(g["date"], day, side="right") - 1)
        eras[name] = {"date": int(g["date"][k]), "y": g["y"][k]}
    s = g["y"][:, 9] - g["y"][:, 1]
    inv = s < 0
    return _json({"t": t, "Y": Y, "eras": eras, "y10_max": {"t": float(t[np.nanargmax(Y[:, 9])]),
                                                           "y": float(np.nanmax(Y[:, 9]))},
                  "y10_min": {"t": float(t[np.nanargmin(Y[:, 9])]), "y": float(np.nanmin(Y[:, 9]))},
                  "inverted_share": float(inv.mean())})


def compute_pca() -> dict:
    g = data.gsw("1985-12-01")
    mats = [1, 2, 3, 5, 7, 10, 15, 20, 30]
    Y = g["y"][:, [m - 1 for m in mats]]
    ok = ~np.isnan(Y).any(1)
    d, Y = g["date"][ok], Y[ok]
    dy = np.diff(Y, axis=0) * 100  # bp
    gap = (d[1:] - d[:-1]) < 10000  # consecutive rows (all are)
    dy = dy[gap]
    full = R.curve_pca(dy)
    dec = {}
    for a, b in [(1986, 1995), (1996, 2005), (2006, 2015), (2016, 2025)]:
        sel = (d[1:][gap] // 10000 >= a) & (d[1:][gap] // 10000 <= b)
        p = R.curve_pca(dy[sel])
        dec[f"{a}-{b}"] = {"share": p["share"][:3], "loadings": p["loadings"][:3],
                           "sd_bp": np.sqrt(p["var"][:3])}
    # a 3D view: cumulative level and slope scores over time
    sc = full["scores"][:, :3]
    return _json({"mats": mats, "share": full["share"], "loadings": full["loadings"][:3], "dec": dec,
                  "sd_bp": np.sqrt(full["var"][:3]), "n_days": int(len(dy)),
                  "t": _frac_year(d[1:][gap])[::5], "cum": np.cumsum(sc, axis=0)[::5],
                  "example_day": {"date": int(d[1:][gap][int(np.argmax(np.abs(dy[:, 5])))]),
                                  "dy": dy[int(np.argmax(np.abs(dy[:, 5])))]}})


def compute_swaps() -> dict:
    out = {}
    for m in (2, 5, 10, 30):
        sd, sv = _fred(f"DSWP{m}", "2000-07-03", "2016-10-28")
        td, tv = _fred(f"DGS{m}", "2000-07-03", "2016-10-28")
        com, i, j = np.intersect1d(sd, td, return_indices=True)
        spr = (sv[i] - tv[j]) * 100
        wd, wv = _weekly(com, spr, 20000705)
        neg = spr < 0
        # the first day after which the spread was negative on most days of the following year
        first = None
        for k in range(len(com)):
            if neg[k] and neg[k:k + 250].mean() > 0.8:
                first = int(com[k])
                break
        out[str(m)] = {"t": _frac_year(wd), "bp": wv, "first_negative": first,
                       "last_bp": float(spr[-1]), "mean_2001_2007": float(spr[(com < 20080101)].mean())}
    return _json(out)


def _coupon_dates(maturity: int, start: int):
    """Semiannual coupon dates of a note maturing on ``maturity`` (YYYYMMDD), from the last one before ``start``."""
    import datetime as dt
    m = dt.date(maturity // 10000, maturity // 100 % 100, maturity % 100)
    s = dt.date(start // 10000, start // 100 % 100, start % 100)
    out = []
    k = 0
    while True:
        y, mo = divmod((m.year * 12 + m.month - 1) - 6 * k, 12)
        day = min(m.day, [31, 29 if (y % 4 == 0 and (y % 100 or y % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30,
                          31, 30, 31][mo])
        d = dt.date(y, mo + 1, day)
        out.append(d)
        if d <= s:
            break
        k += 1
    return sorted(out), s


def compute_futures() -> dict:
    """The December 2025 10-year note future (TYZ5): every note with 6.5 to 10 years left on 1 December 2025 and an
    original term of at most 10 years.  Each priced off the GSW curve of 28 November 2025 (cash flows discounted at
    the zero curve, clean = full - accrued), its CBOT factor from the House; the futures price that makes the
    cheapest one's basis zero, ignoring carry and the delivery options."""
    import datetime as dt
    notes = data.treasury_auctions("Note")
    start, lo, hi = 20251201, 20320601, 20351201
    seen, deliv = set(), []
    first_issue = {}
    for r in notes:
        first_issue.setdefault(r["cusip"], r["issue"])
    for r in notes:
        if r["cusip"] in seen or not (lo <= r["maturity"] <= hi):
            continue
        orig = (r["maturity"] - first_issue[r["cusip"]]) / 10000
        if orig > 10.05 or first_issue[r["cusip"]] > 20251128:
            continue
        seen.add(r["cusip"])
        deliv.append(r)
    g = data.gsw("2025-11-01")
    b, tau = _gsw_day(g, 20251128)
    sdt = dt.date(2025, 12, 1)
    rows = []
    for r in sorted(deliv, key=lambda q: q["maturity"]):
        dates, s = _coupon_dates(r["maturity"], start)
        prev, fut = dates[0], [d for d in dates if d > s]
        t = np.array([(d - sdt).days / 365.25 for d in fut])
        cf = np.full(len(t), r["coupon"] / 2)
        cf[-1] += 100
        acc = r["coupon"] / 2 * (s - prev).days / (fut[0] - prev).days
        rows.append({"cusip": r["cusip"], "coupon": r["coupon"], "maturity": r["maturity"], "t": t, "cf": cf,
                     "accrued": acc})
    for q in rows:
        m = (q["maturity"] // 10000 - 2025) * 12 + (q["maturity"] // 100 % 100 - 12)
        if q["maturity"] % 100 < 1:
            m -= 1
        q["years"], q["months"] = divmod(m, 12)
        q["cf_factor"] = R.conversion_factor(q["coupon"] / 100, q["years"], q["months"])
    shifts = np.arange(-400, 401, 10)
    table = []
    for sh in shifts:
        prices = []
        for q in rows:
            z = R.nss(q["t"], b, tau) / 100 + sh * 1e-4
            prices.append(float(np.sum(q["cf"] * np.exp(-z * q["t"]))) - q["accrued"])
        prices = np.array(prices)
        ratio = prices / np.array([q["cf_factor"] for q in rows])
        k = int(np.argmin(ratio))
        F = ratio[k]
        basis = prices - F * np.array([q["cf_factor"] for q in rows])
        y10 = float(R.nss(np.array([10.0]), b, tau)[0] + sh / 100)
        table.append({"shift": int(sh), "F": F, "ctd": k, "basis": basis, "y10": y10})
    base = table[list(shifts).index(0)]
    return _json({"notes": [{k: v for k, v in q.items() if k not in ("t", "cf")} for q in rows], "table": table,
                  "shifts": shifts, "base_ctd": rows[base["ctd"]]["cusip"], "base_F": base["F"],
                  "switch": [int(table[i]["shift"]) for i in range(1, len(table))
                             if table[i]["ctd"] != table[i - 1]["ctd"]]})


def compute_sofr() -> dict:
    import datetime as dt
    d, v = _fred("SOFR", "2018-04-01")
    bd, bv = _fred("DTB3", "2018-04-01")
    dates = [dt.date(k // 10000, k // 100 % 100, k % 100) for k in d]
    days = np.array([(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)] + [1])
    rows = []
    for i, s in enumerate(dates):
        end = s + dt.timedelta(days=91)
        j = i
        while j < len(dates) and dates[j] < end:
            j += 1
        if j >= len(dates):
            break
        r = R.compound_in_arrears(v[i:j] / 100, days[i:j])
        k = np.searchsorted(bd, d[i], side="right") - 1
        rows.append((d[i], v[i], 100 * r, bv[k]))
    a = np.array(rows)
    wd, _ = _weekly(a[:, 0].astype(int), a[:, 1], 20180404)
    sel = np.isin(a[:, 0].astype(int), wd)
    hike = (a[:, 0] >= 20220301) & (a[:, 0] < 20230801)
    return _json({"t": _frac_year(a[sel, 0].astype(int)), "sofr": a[sel, 1], "arrears": a[sel, 2], "bill": a[sel, 3],
                  "gap_hikes_bp": float(np.mean(a[hike, 2] - a[hike, 1]) * 100),
                  "gap_all_bp": float(np.mean(a[:, 2] - a[:, 1]) * 100),
                  "sep2019": {"max": float(v[(d >= 20190910) & (d <= 20190930)].max()),
                              "day": int(d[(d >= 20190910) & (d <= 20190930)][np.argmax(v[(d >= 20190910) &
                                                                                            (d <= 20190930)])])}})


def _monthly_logp(g, n_months=121, start=None):
    m = g["date"] // 100
    idx = np.where(np.r_[m[1:] != m[:-1], True])[0]
    if start:
        idx = idx[g["date"][idx] >= start]
    n = np.arange(1, n_months + 1)
    lp = []
    for i in idx:
        b, t = g["beta"][i].copy(), g["tau"][i].copy()
        if np.isnan(t[1]) or np.isnan(b[3]):
            b[3], t[1] = 0.0, 1.0
        lp.append(-R.nss(n / 12, b, t) / 100 * n / 12)
    return g["date"][idx], np.array(lp)


def compute_term() -> dict:
    g = data.gsw()
    md, lp = _monthly_logp(g)
    n = np.arange(1, lp.shape[1] + 1)
    Y = -lp / n * 1200  # percent a year
    # Campbell-Shiller (1991): y(n-1, t+1) - y(n, t) on the slope (y(n) - y(1)) / (n - 1); 1 under expectations
    cs = {}
    for nn in (12, 24, 36, 60, 120):
        lhs = Y[1:, nn - 2] - Y[:-1, nn - 1]
        x = (Y[:-1, nn - 1] - Y[:-1, 0]) / (nn - 1)
        X = np.c_[np.ones(len(x)), x]
        coef = np.linalg.lstsq(X, lhs, rcond=None)[0]
        e = lhs - X @ coef
        V = np.linalg.inv(X.T @ X) * (e @ e) / (len(x) - 2)
        cs[str(nn)] = {"b": float(coef[1]), "se": float(np.sqrt(V[1, 1]))}
    # Fama-Bliss (1987): one-year excess return of an n-year bond on the forward-spot spread; annual, overlapping
    fb = {}
    for ny in (2, 3, 4, 5):
        nm = 12 * ny
        rx = (lp[12:, nm - 13] - lp[:-12, nm - 1]) + lp[:-12, 11]  # log return minus the 1-year yield
        fwd = lp[:-12, nm - 13] - lp[:-12, nm - 1]  # forward rate from n-1 to n years (log)
        x = fwd + lp[:-12, 11]
        X = np.c_[np.ones(len(x)), x]
        coef = np.linalg.lstsq(X, rx, rcond=None)[0]
        e = rx - X @ coef
        # Newey-West with 12 lags (overlapping annual returns)
        Xe = X * e[:, None]
        S = Xe.T @ Xe
        for L in range(1, 13):
            w = 1 - L / 13
            G = Xe[L:].T @ Xe[:-L]
            S += w * (G + G.T)
        XX = np.linalg.inv(X.T @ X)
        V = XX @ S @ XX
        fb[str(ny)] = {"b": float(coef[1]), "se": float(np.sqrt(V[1, 1])),
                       "r2": float(1 - e.var() / rx.var())}
    # ACM re-estimated
    acm = R.acm_decompose(lp, K=5, rx_mats=np.arange(6, 121, 6), pc_from=3)
    ny = data.acm()
    tp_ours = acm["tp"][:, 119] * 100
    y_ours = acm["y"][:, 119] * 100
    rn_ours = acm["rny"][:, 119] * 100
    com, i, j = np.intersect1d(md // 100, ny["date"] // 100, return_indices=True)
    return _json({"cs": cs, "fb": fb, "t": _frac_year(md), "y10": y_ours, "tp10": tp_ours, "rn10": rn_ours,
                  "ny_tp10": ny["tp"][:, 9], "ny_t": _frac_year(ny["date"]),
                  "corr": float(np.corrcoef(tp_ours[i], ny["tp"][j, 9])[0, 1]),
                  "mad": float(np.mean(np.abs(tp_ours[i] - ny["tp"][j, 9]))),
                  "fit_rmse_bp": acm["fit_rmse"] * 1e4,
                  "end": {"ours": float(tp_ours[-1]), "ny": float(ny["tp"][-1, 9]), "y": float(y_ours[-1])},
                  "since_cut": {k_: {"y": float(y_ours[np.where(md // 100 == ym)[0][0]]),
                                     "rn": float(rn_ours[np.where(md // 100 == ym)[0][0]]),
                                     "tp": float(tp_ours[np.where(md // 100 == ym)[0][0]])}
                                for k_, ym in (("2024-08", 202408), ("2025-12", 202512))},
                  "tp_1981": float(tp_ours[np.where(md // 100 == 198109)[0][0]]),
                  "tp_min": {"t": float(_frac_year(md)[int(np.argmin(tp_ours))]), "v": float(np.min(tp_ours))}})


def compute_fomc() -> dict:
    from videos.quant.quant6.compute import _fomc_dates
    fom = set(int(x) for x in _fomc_dates())
    g = data.gsw("1993-12-01", "2020-12-31")
    d = g["date"]
    y2 = g["y"][:, 1]
    # instantaneous forward 10 years ahead, from the fitted parameters
    f10 = []
    for i in range(len(d)):
        b, t = g["beta"][i].copy(), g["tau"][i].copy()
        if np.isnan(t[1]) or np.isnan(b[3]):
            b[3], t[1] = 0.0, 1.0
        c = R.Curve(np.linspace(0.25, 30, 120), R.nss(np.linspace(0.25, 30, 120), b, t) / 100)
        f10.append(float(c.inst_fwd(np.array([10.0]))[0]) * 100)
    f10 = np.array(f10)
    dy2 = np.diff(y2) * 100
    df10 = np.diff(f10) * 100
    dd = d[1:]
    isf = np.array([k in fom for k in dd])
    sel = dd >= 19940101
    a, b_ = dy2[sel & isf], dy2[sel & ~isf]
    X = np.c_[np.ones(isf[sel].sum()), dy2[sel & isf]]
    coef = np.linalg.lstsq(X, df10[sel & isf], rcond=None)[0]
    e = df10[sel & isf] - X @ coef
    se = float(np.sqrt((np.linalg.inv(X.T @ X) * (e @ e) / (len(e) - 2))[1, 1]))
    big = np.argsort(-np.abs(a))[:6]
    a, b_ = a[np.isfinite(a)], b_[np.isfinite(b_)]
    return _json({"n_fomc": int(isf[sel].sum()), "sd_fomc": float(a.std()), "sd_other": float(b_.std()),
                  "fomc_dy2": a, "other_dy2": b_[::7], "beta_f10": float(coef[1]), "se_f10": se,
                  "fomc_df10": df10[sel & isf],
                  "biggest": [{"date": int(dd[sel & isf][k]), "dy2": float(a[k])} for k in big]})


def compute_immunize() -> dict:
    y0 = 0.04
    L_T = 15.0
    L = 100 * np.exp(-y0 * L_T)
    T1, T2 = 5.0, 30.0
    # zeros: PV and duration match -> weights in value; duration of a zero is its maturity (continuous)
    w2 = (L_T - T1) / (T2 - T1)
    v1, v2 = L * (1 - w2), L * w2
    n1, n2 = v1 / np.exp(-y0 * T1), v2 / np.exp(-y0 * T2)

    def surplus(curve_fn):
        return float(n1 * np.exp(-curve_fn(T1) * T1) + n2 * np.exp(-curve_fn(T2) * T2)
                     - 100 * np.exp(-curve_fn(L_T) * L_T))
    shifts = np.linspace(-0.03, 0.03, 61)
    par = np.array([surplus(lambda t, s=s: y0 + s) for s in shifts])
    # a twist: short rates up, long rates down, pivot at 15 years
    twist = np.array([surplus(lambda t, s=s: y0 + s * (L_T - t) / 10) for s in shifts])
    S = np.linspace(-0.03, 0.03, 25)
    Tw = np.linspace(-0.02, 0.02, 25)
    surf = np.array([[surplus(lambda t, a=a, b=b: y0 + a + b * (L_T - t) / 10) for a in S] for b in Tw])
    conv_a = (n1 * np.exp(-y0 * T1) * T1 ** 2 + n2 * np.exp(-y0 * T2) * T2 ** 2) / L
    return _json({"L": L, "v1": v1, "v2": v2, "w2": w2, "shifts": shifts, "par": par, "twist": twist,
                  "S": S, "Tw": Tw, "surf": surf, "convexity_assets": conv_a, "convexity_liab": L_T ** 2,
                  "twist_loss_100bp": float(twist[list(np.round(shifts, 4)).index(0.01)])})


# ---------------------------------------------------------------------------
# The one strategy this part tests: a PCA-neutral butterfly, registered before its hold-out is opened
# ---------------------------------------------------------------------------
FLY_RULE = {"legs": [2, 5, 10], "weights_fit": "PCA of daily GSW changes 1990-2020, level and slope neutral",
            "signal": "z = (fly - 250-day mean) / 250-day sd", "enter": "|z| > 1, against the sign",
            "exit": "z crosses 0", "cost_bp": 0.5, "unit": "fly in bp of yield, belly DV01 = 1"}


def _fly_series():
    g = data.gsw("1989-01-01")
    Y = g["y"][:, [1, 4, 9]] * 100
    d = g["date"]
    train = (d >= 19900101) & (d < 20210101)
    mats = [1, 2, 3, 5, 7, 10, 15, 20, 30]
    full = g["y"][:, [m - 1 for m in mats]] * 100
    ok = ~np.isnan(full).any(1)
    p = R.curve_pca(np.diff(full[train & ok], axis=0))
    w = R.fly_weights(p["loadings"], [1, 3, 5])
    return d, Y @ w, w, p


def _fly_pnl(F, cost_bp):
    F = np.asarray(F, float)
    n = len(F)
    pos = np.zeros(n)
    z = np.full(n, np.nan)
    for i in range(250, n):
        win = F[i - 250:i]
        z[i] = (F[i] - win.mean()) / win.std()
        prev = pos[i - 1]
        if prev == 0 and abs(z[i]) > 1:
            pos[i] = -np.sign(z[i])
        elif prev != 0 and np.sign(z[i]) != np.sign(-prev):
            pos[i] = 0
        else:
            pos[i] = prev
    # a position of +1 gains when the fly rises; it is short (-1) after the fly was unusually high
    pnl = np.r_[0.0, pos[:-1] * np.diff(F)]
    pnl -= cost_bp * np.abs(np.diff(np.r_[0.0, pos]))
    return pos, z, pnl


def compute_fly() -> dict:
    d, F, w, p = _fly_series()
    reg = pit.register("pca_fly_2s5s10s", inspect.getsource(_fly_pnl) + inspect.getsource(_fly_series),
                       FLY_RULE, trials=1)
    ins = d < 20210101
    pos, z, pnl = _fly_pnl(F, FLY_RULE["cost_bp"])
    hd, hv = pit.open_envelope("pca_fly_2s5s10s", "gsw_fly_2s5s10s", d, F)
    gross = pnl + FLY_RULE["cost_bp"] * np.abs(np.diff(np.r_[0.0, pos]))  # what the costs took

    def stats(x):
        x = x[np.isfinite(x)]
        sd = x.std()
        return {"mean_bp_yr": float(x.mean() * 252), "sd_bp_yr": float(sd * np.sqrt(252)),
                "sharpe": float(x.mean() / sd * np.sqrt(252)) if sd > 0 else 0.0, "days": int(len(x))}
    # half-life of the fly (AR(1) on daily levels), in and out of sample
    def half_life(x):  # the Fed's file leaves one day blank: use the pairs where both days are known
        ok = np.isfinite(x[:-1]) & np.isfinite(x[1:])
        b = np.polyfit(x[:-1][ok], x[1:][ok], 1)[0]
        return float(np.log(0.5) / np.log(b)) if 0 < b < 1 else float("inf")
    return _json({"weights": w, "share": p["share"][:3], "t": _frac_year(d)[::3], "F": F[::3], "z": z[::3],
                  "pos": pos[::3], "cum": np.nancumsum(pnl)[::3], "in": stats(pnl[(d >= 19910101) & ins]),
                  "out": stats(pnl[~ins]), "gross_in": stats(gross[(d >= 19910101) & ins]),
                  "gross_out": stats(gross[~ins]), "trades_in": int(np.sum(np.abs(np.diff(pos[ins])) > 0)),
                  "trades_out": int(np.sum(np.abs(np.diff(pos[~ins])) > 0)), "hl_in": half_life(F[ins]), "hl_out": half_life(F[~ins]),
                  "holdout_first": int(hd[0]), "holdout_last": int(hd[-1]), "registered": reg,
                  "trials": pit.trials_so_far(), "rule": FLY_RULE})


def compute_ldi() -> dict:
    impacts = [0.0, 0.5, 1.0, 1.5, 2.0]
    runs = {str(k): R.ldi_spiral(50, impact_bp_per_pct=k) for k in impacts}
    shocks = np.arange(10, 151, 10)
    kk = np.linspace(0, 2.0, 21)
    surf = np.array([[R.ldi_spiral(s, impact_bp_per_pct=k)["dy_bp"][-1] for s in shocks] for k in kk])
    return _json({"runs": runs, "shocks": shocks, "impacts": kk, "surf": surf,
                  "published": {"y30_rise_bp_3days": 130, "boe_bought_bn": 19.3, "conventional_bn": 12.1,
                                "index_linked_bn": 7.2, "start": "2022-09-28", "end": "2022-10-14"}})


def compute_svb() -> dict:
    C = ("HeldToMaturitySecurities", "HeldToMaturitySecuritiesFairValue",
         "HeldToMaturitySecuritiesAccumulatedUnrecognizedHoldingLoss", "StockholdersEquity", "Deposits", "Assets",
         "AvailableForSaleSecuritiesDebtSecurities")
    f = data.sec_facts(719739, C, "2023-03-31")

    def val(c, end):
        r = [x for x in f["facts"][c] if x["end"] == end and x["form"] == "10-K"]
        return r[-1]["val"] / 1e9 if r else None
    facts = {c: {e: val(c, e) for e in ("2020-12-31", "2021-12-31", "2022-12-31")} for c in C}
    g = data.gsw("2020-12-01", "2023-03-10")
    D6 = 6.2
    y6 = g["y"][:, 5]
    i0 = int(np.searchsorted(g["date"], 20211231, side="right") - 1)
    i1 = int(np.searchsorted(g["date"], 20221230, side="right") - 1)
    dy = (y6[i1] - y6[i0]) / 100
    htm = facts["HeldToMaturitySecurities"]["2022-12-31"]
    est = htm * D6 * dy
    # a daily mark of a 6.2-year book bought at the end of 2021
    m = g["date"] >= 20211231
    mark = htm * D6 * (y6[m] - y6[i0]) / 100
    return _json({"facts": facts, "duration": D6, "dy6_2022_pct": dy * 100, "est_loss": est,
                  "t": _frac_year(g["date"][m]), "mark": mark, "y6": y6[m],
                  "review": {"assets_bn": 212, "outflow_mar9_bn": 40, "expected_mar10_bn": 100,
                             "uninsured_share": 94, "htm_share_of_securities": 78, "afs_sold_bn": 21,
                             "afs_loss_bn": 1.8, "deposit_base_share_run": 85}})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": {"pca_fly_2s5s10s": load("fly")["registered"]}}


def _sign_changes(v, tol=1e-9):
    v = np.asarray(v, float)
    v = v[np.abs(v) > tol * np.abs(v).max()]
    return int(np.sum(np.sign(v[1:]) != np.sign(v[:-1])))


def _tp_share(C, order):
    """The share of the order-r minors with increasing row and column indices that are positive."""
    from itertools import combinations
    n = len(C)
    pos = tot = 0
    for rows in combinations(range(n), order):
        for cols in combinations(range(n), order):
            tot += 1
            pos += np.linalg.det(C[np.ix_(rows, cols)]) > 0
    return pos / tot


def compute_oscillation_theory() -> dict:
    """The research chapter: why level, slope and curvature.  If the covariance of yield changes, with maturities in
    order, is an oscillation matrix (totally nonnegative, some power totally positive), Gantmacher and Krein's theorem
    makes the k-th eigenvector change sign exactly k - 1 times, whatever the economics.  Checked on smooth random
    kernels against unordered random correlation matrices; then on the Treasury curve's daily changes (GSW,
    1986-2025): the minors' signs and the eigenvectors' sign changes, for yields and for forward rates."""
    rng = np.random.default_rng(1818)
    sims = {"ordered": np.zeros((3, 4), int), "unordered": np.zeros((3, 4), int)}
    M = 2000
    for _ in range(M):
        m = np.sort(rng.uniform(0.25, 30, 9))
        ell = rng.uniform(3, 40)
        C = np.exp(-((m[:, None] - m[None, :]) / ell) ** 2) + 1e-9 * np.eye(9)   # a Gaussian kernel: totally positive
        w, V = np.linalg.eigh(C)
        V = V[:, ::-1]
        for k in range(3):
            sims["ordered"][k, min(_sign_changes(V[:, k]), 3)] += 1
        A = rng.standard_normal((9, 3))
        Cu = A @ A.T + np.diag(rng.uniform(0.05, 0.3, 9))   # a three-factor covariance with no ordering
        d = np.sqrt(np.diag(Cu))
        Cu = Cu / d[:, None] / d[None, :]
        w, V = np.linalg.eigh(Cu)
        V = V[:, ::-1]
        for k in range(3):
            sims["unordered"][k, min(_sign_changes(V[:, k]), 3)] += 1
    out = {"M": M, "sims": {k: v.tolist() for k, v in sims.items()}}
    # the exponential (Markov) correlation, rho^|i - j|: eigenvectors are discrete sinusoids
    n = 9
    rho = 0.9
    Cx = rho ** np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
    w, V = np.linalg.eigh(Cx)
    V = V[:, ::-1] * np.sign(V[:, ::-1][0])
    out["markov"] = {"rho": rho, "vec": V[:, :4].T, "share": (w[::-1] / w.sum())[:4],
                     "changes": [_sign_changes(V[:, k]) for k in range(4)]}
    # the Treasury curve
    g = data.gsw("1985-12-01")
    mats = [1, 2, 3, 5, 7, 10, 15, 20, 30]
    Y = g["y"][:, [m - 1 for m in mats]]
    ok = ~np.isnan(Y).any(1)
    Y = Y[ok]
    dy = np.diff(Y, axis=0) * 100
    C = np.cov(dy.T)
    Cr = np.corrcoef(dy.T)
    w, V = np.linalg.eigh(C)
    V = V[:, ::-1]
    V = V * np.sign(V[0])
    # forward rates between the same maturities: f(m_{i-1}, m_i)
    yy = Y
    mm = np.array(mats, float)
    F = np.column_stack([yy[:, 0]] + [(mm[i] * yy[:, i] - mm[i - 1] * yy[:, i - 1]) / (mm[i] - mm[i - 1])
                                      for i in range(1, len(mats))])
    df = np.diff(F, axis=0) * 100
    Cf = np.cov(df.T)
    wf, Vf = np.linalg.eigh(Cf)
    Vf = Vf[:, ::-1]
    Vf = Vf * np.sign(Vf[0])
    out["treasury"] = {"mats": mats, "n_days": int(len(dy)), "share": (w[::-1] / w.sum())[:5], "vec": V[:, :5].T,
                       "changes": [_sign_changes(V[:, k]) for k in range(5)],
                       "tp2": _tp_share(Cr, 2), "tp3": _tp_share(Cr, 3), "corr": Cr,
                       "fwd_share": (wf[::-1] / wf.sum())[:5], "fwd_vec": Vf[:, :5].T,
                       "fwd_changes": [_sign_changes(Vf[:, k]) for k in range(5)],
                       "fwd_tp2": _tp_share(np.corrcoef(df.T), 2), "fwd_tp3": _tp_share(np.corrcoef(df.T), 3),
                       "fwd_corr": np.corrcoef(df.T)}
    return _json(out)


ITEMS = {"oscillation_theory": compute_oscillation_theory, "policy": compute_policy, "taylor": compute_taylor, "bonds": compute_bonds, "curve_day": compute_curve_day,
         "morph": compute_morph, "pca": compute_pca, "swaps": compute_swaps, "futures": compute_futures,
         "sofr": compute_sofr, "term": compute_term, "fomc": compute_fomc, "immunize": compute_immunize,
         "fly": compute_fly, "ldi": compute_ldi, "svb": compute_svb, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
