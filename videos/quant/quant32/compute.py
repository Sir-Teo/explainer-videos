"""Every number in Part 32 (Systematic Macro and Alternative Premia), computed and cached in .cache/quant32/.

    python -m videos.quant.quant32.compute [items] [--force]

The House's macro panel: 23 US-listed ETFs across equities, bonds, credit, commodities and currencies (Yahoo's
dividend-adjusted closes), daily excess returns over 3-month T-bills (FRED DTB3), 2006-2020 for research, 2021-2025
sealed. Long histories come from Kenneth French (daily US market, 1926-), FRED's 10-year yield (1962-), Cboe's PUT
index (1991-) and AQR's Century of Factor Premia (as published, through 2020).

* ``panel``       the ETFs, their classes and their research-years statistics;
* ``trend``       time-series momentum on the panel: lookbacks, sizing, asset classes, 2008, the quarterly smile; AQR's
                  TSMOM series 1985-2020;
* ``voltarget``   each asset raw against volatility-targeted: Sharpe ratio, drawdown, skewness;
* ``riskparity``  inverse-volatility risk parity against 60/40 and the market; leverage; the stock-bond correlation
                  1962-2020 from the market and a 10-year bond built from yields;
* ``styles``      value, momentum, carry and defensive across asset classes, 1926-2020 (AQR);
* ``shortvol``    selling puts (Cboe PUT) against the market, 2007-2020;
* ``calendar``    the turn of the month, 1926-2020; overnight against intraday in SPY, 1993-2020;
* ``theory``      the research chapter: the linear trend rule's exact P&L identity, its skewness, its mean;
* ``envelope``    the trend book and the risk-parity book, registered and opened on 2021-2025.
"""

from __future__ import annotations

import functools
import inspect
import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import pit, systematic as SY

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant32")
load = pit.counted(CACHE.load, 32)
RESEARCH_END = 20201231
CLASSES = {
    "equities": ["SPY", "EFA", "EEM", "IWM", "VNQ"],
    "bonds": ["TLT", "IEF", "TIP"],
    "credit": ["LQD", "HYG"],
    "commodities": ["GLD", "SLV", "DBC", "USO", "UNG", "DBA"],
    "currencies": ["UUP", "FXE", "FXY", "FXA", "FXC", "FXF", "FXB"],
}
SYMS = [s for v in CLASSES.values() for s in v]
GROUP = [g for g, v in CLASSES.items() for _ in v]
TARGET = 0.10


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


@functools.lru_cache(maxsize=None)
def _panel_full():
    """Daily excess simple returns of the ETFs on SPY's calendar, 2006-2025 (NaN before a fund's first day)."""
    spy = data.yahoo_total("SPY")
    dates = spy["date"]
    R = np.full((len(dates), len(SYMS)), np.nan)
    for j, s in enumerate(SYMS):
        d = data.yahoo_total(s)
        px = dict(zip(d["date"].tolist(), d["adj"].tolist()))
        p = np.array([px.get(int(x), np.nan) for x in dates])
        R[1:, j] = p[1:] / p[:-1] - 1
    tb = data.fred("DTB3", start="2006-01-01")
    rf = dict(zip(tb["date"].tolist(), tb["value"].tolist()))
    last, rfd = 0.0, np.zeros(len(dates))
    for i, x in enumerate(dates):
        last = rf.get(int(x), last)
        rfd[i] = last / 100 / 252
    return dates, R - rfd[:, None], rfd


def _panel():
    d, R, rf = _panel_full()
    m = d <= RESEARCH_END
    return d[m], R[m], rf[m]


def _stats(r, ann=252):
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    return {"mean": float(r.mean() * ann), "vol": float(r.std(ddof=1) * math.sqrt(ann)), "sharpe": SY.sharpe(r, ann),
            "maxdd": SY.max_drawdown(r), "skew": SY.skewness(r)}


def _monthly(dates, r):
    """Compound daily simple returns into calendar months: (YYYYMM, returns)."""
    d = np.asarray(dates) // 100
    out_d, out_r = [], []
    for m in np.unique(d):
        x = np.asarray(r)[d == m]
        x = x[np.isfinite(x)]
        if len(x):
            out_d.append(int(m))
            out_r.append(float(np.prod(1 + x) - 1))
    return np.array(out_d), np.array(out_r)


def compute_panel() -> dict:
    d, R, rf = _panel()
    rows = {}
    for j, s in enumerate(SYMS):
        st = _stats(R[:, j])
        st["first"] = int(d[np.isfinite(R[:, j])][0])
        st["group"] = GROUP[j]
        rows[s] = st
    C = np.ma.corrcoef(np.ma.masked_invalid(R[d >= 20080101]).T).filled(np.nan)
    return _json({"syms": SYMS, "classes": CLASSES, "rows": rows, "corr": C, "n_days": int(len(d)),
                  "first": int(d[0]), "last": int(d[-1])})


# ---------------------------------------------------------------------------
# Trend
# ---------------------------------------------------------------------------
CONFIGS = [(lb, rule) for lb in (21, 63, 252) for rule in ("sign", "linear")]


def _trend_book(d, R, lookback=252, rule="sign", cols=None):
    cols = list(range(R.shape[1])) if cols is None else cols
    X = R[:, cols]
    vol = SY.ewma_vol(X)
    W = SY.tsmom_positions(X, vol, d, lookback=lookback, target=0.40, rule=rule)
    return SY.book(X, W, scale_to=TARGET), W


def compute_trend() -> dict:
    d, R, rf = _panel()
    live = d >= 20070201
    configs = {}
    for lb, rule in CONFIGS:
        p, _ = _trend_book(d, R, lb, rule)
        configs[f"{lb}/{rule}"] = _stats(p[live])
    p, W = _trend_book(d, R, 252, "sign")
    spy = R[:, SYMS.index("SPY")]
    groups = {}
    for g, v in CLASSES.items():
        pg, _ = _trend_book(d, R, 252, "sign", [SYMS.index(s) for s in v])
        groups[g] = _stats(pg[live])
    # 60/40 for comparison
    ief = R[:, SYMS.index("IEF")]
    sixty = 0.6 * spy + 0.4 * ief
    ok = live & np.isfinite(p) & np.isfinite(spy) & np.isfinite(sixty)
    md, mp = _monthly(d[ok], p[ok])
    _, ms = _monthly(d[ok], spy[ok])
    _, m64 = _monthly(d[ok], sixty[ok])
    # quarterly smile
    q = (md // 100) * 10 + ((md % 100) - 1) // 3
    qs, qt = [], []
    for k in np.unique(q):
        qs.append(float(np.prod(1 + ms[q == k]) - 1))
        qt.append(float(np.prod(1 + mp[q == k]) - 1))
    qs, qt = np.array(qs), np.array(qt)
    fit = np.polyfit(qs, qt, 2)
    yr = lambda r, y: float(np.prod(1 + r[(md // 100) == y]) - 1)  # noqa: E731
    cum = {"trend": np.cumprod(1 + mp) - 1, "spy": np.cumprod(1 + ms) - 1, "6040": np.cumprod(1 + m64) - 1}
    # AQR's TSMOM as published, 1985-2020
    ts = data.aqr("Time-Series-Momentum-Factors-Monthly", "TSMOM Factors", "2025-12")
    m = ts["date"] <= 202012
    tsm = ts["values"][m, 0]
    aqr = {"sharpe": float(np.nanmean(tsm) / np.nanstd(tsm) * math.sqrt(12)), "first": int(ts["date"][0]),
           "y2008": float(np.prod(1 + tsm[(ts["date"][m] // 100) == 2008]) - 1)}
    # long and short share, and gross exposure through time
    gross = np.nanmean(np.abs(W[live]).sum(1))
    return _json({"configs": configs, "main": _stats(p[live]), "groups": groups, "spy": _stats(spy[live]),
                  "sixty": _stats(sixty[live]), "corr_spy": float(np.corrcoef(mp, ms)[0, 1]),
                  "y2008": {"trend": yr(mp, 2008), "spy": yr(ms, 2008), "6040": yr(m64, 2008)},
                  "smile": {"m": qs, "t": qt, "fit": fit}, "months": md, "cum": cum, "aqr": aqr,
                  "gross": float(gross), "n_trials": len(CONFIGS)})


# ---------------------------------------------------------------------------
# Volatility targeting
# ---------------------------------------------------------------------------
def compute_voltarget() -> dict:
    d, R, rf = _panel()
    live = d >= 20070201
    rows = {}
    for j, s in enumerate(SYMS):
        r = R[:, j]
        x, e = SY.vol_target(r, TARGET)
        ok = live & np.isfinite(x) & np.isfinite(r)
        _, mr = _monthly(d[ok], r[ok])
        _, mx = _monthly(d[ok], x[ok])
        rows[s] = {"raw": _stats(r[ok]), "vt": _stats(x[ok]), "skew_m_raw": SY.skewness(mr),
                   "skew_m_vt": SY.skewness(mx), "exp_min": float(np.nanmin(e[ok])), "exp_max": float(np.nanmax(e[ok])),
                   "group": GROUP[j]}
    better = sum(rows[s]["vt"]["sharpe"] > rows[s]["raw"]["sharpe"] for s in SYMS)
    dd_better = sum(rows[s]["vt"]["maxdd"] > rows[s]["raw"]["maxdd"] for s in SYMS)
    spy = R[:, SYMS.index("SPY")]
    x, e = SY.vol_target(spy, 0.15)
    ok = live & np.isfinite(x)
    return _json({"rows": rows, "better": int(better), "dd_better": int(dd_better), "n": len(SYMS),
                  "spy_path": {"dates": d[ok][::5], "exposure": e[ok][::5],
                               "vol": SY.ewma_vol(spy)[ok][::5]}})


# ---------------------------------------------------------------------------
# Risk parity
# ---------------------------------------------------------------------------
RP_COLS = ["SPY", "EFA", "EEM", "TLT", "IEF", "TIP", "LQD", "HYG", "GLD", "DBC"]
RP_GROUP = ["equities"] * 3 + ["bonds"] * 3 + ["credit"] * 2 + ["commodities"] * 2


def _rp(d, R):
    cols = [SYMS.index(s) for s in RP_COLS]
    return SY.risk_parity(R[:, cols], d, RP_GROUP, target=TARGET)


def _bond_from_yield(y, dur_years=10.0):
    """Daily total return of a constant-maturity 10-year par bond from its yield (percent): carry plus price change,
    with the modified duration of a par bond at that yield."""
    y = np.asarray(y, float) / 100
    out = np.full(len(y), np.nan)
    for t in range(1, len(y)):
        c = y[t - 1]
        D = (1 - (1 + c / 2) ** (-2 * dur_years)) / c if c > 0 else dur_years
        out[t] = c / 252 - D * (y[t] - y[t - 1])
    return out


def compute_riskparity() -> dict:
    d, R, rf = _panel()
    pnl, lev, W = _rp(d, R)
    live = d >= 20070201
    spy = R[:, SYMS.index("SPY")]
    sixty = 0.6 * spy + 0.4 * R[:, SYMS.index("IEF")]
    ok = live & np.isfinite(pnl) & np.isfinite(spy) & np.isfinite(sixty)
    md, mrp = _monthly(d[ok], pnl[ok])
    _, ms = _monthly(d[ok], spy[ok])
    _, m64 = _monthly(d[ok], sixty[ok])
    ends = np.flatnonzero(np.isfinite(lev))
    gw = {}
    for g in set(RP_GROUP):
        idx = [i for i, x in enumerate(RP_GROUP) if x == g]
        gw[g] = float(np.nanmean(np.abs(W[ends][:, idx]).sum(1)))
    # risk shares by group (average over rebalances)
    shares = {g: [] for g in set(RP_GROUP)}
    cols = [SYMS.index(s) for s in RP_COLS]
    for t in ends[::3]:
        X = R[t - 251:t + 1][:, cols]
        ok = np.isfinite(X).all(0)
        w = np.where(ok, W[t], 0.0)
        C = np.cov(np.nan_to_num(X).T)
        tot = w @ C @ w
        rc = w * (C @ w) / tot
        for g in shares:
            shares[g].append(float(sum(rc[i] for i, x in enumerate(RP_GROUP) if x == g)))
    # the stock-bond correlation, 1962-2020: the market against a 10-year bond built from yields, monthly
    kf = data.ken_french_daily(through="2020-12-31")
    y10 = data.fred("DGS10", start="1962-01-01", through="2020-12-31")
    yd = dict(zip(y10["date"].tolist(), y10["value"].tolist()))
    dd = kf["date"][kf["date"] >= 19620102]
    mk = kf["mkt"][kf["date"] >= 19620102] if "mkt" in kf else None
    yy, last = [], None
    for x in dd:
        last = yd.get(int(x), last)
        yy.append(last)
    br = _bond_from_yield(np.array(yy, float))
    mdm, mm = _monthly(dd[1:], mk[1:])
    _, mb = _monthly(dd[1:], br[1:])
    rc36 = np.full(len(mm), np.nan)
    for i in range(35, len(mm)):
        rc36[i] = np.corrcoef(mm[i - 35:i + 1], mb[i - 35:i + 1])[0, 1]
    dec = {}
    for y0 in range(1960, 2020, 10):
        k = (mdm // 100 >= y0) & (mdm // 100 < y0 + 10)
        dec[str(y0)] = float(np.corrcoef(mm[k], mb[k])[0, 1])
    return _json({"rp": _stats(pnl[live]), "spy": _stats(spy[live]), "sixty": _stats(sixty[live]),
                  "lev_mean": float(np.nanmean(lev)), "lev_max": float(np.nanmax(lev)), "lev_min": float(np.nanmin(lev)),
                  "lev_path": {"dates": d[ends], "lev": lev[ends]}, "group_gross": gw,
                  "risk_share": {g: float(np.mean(v)) for g, v in shares.items()},
                  "y2008": {"rp": float(np.prod(1 + mrp[md // 100 == 2008]) - 1),
                            "spy": float(np.prod(1 + ms[md // 100 == 2008]) - 1),
                            "6040": float(np.prod(1 + m64[md // 100 == 2008]) - 1)},
                  "cum": {"rp": np.cumprod(1 + mrp) - 1, "6040": np.cumprod(1 + m64) - 1}, "months": md,
                  "sb": {"months": mdm, "rc36": rc36, "decades": dec,
                         "bond_stats": _stats(mb, 12), "mkt_stats": _stats(mm, 12)}})


# ---------------------------------------------------------------------------
# Styles across asset classes (AQR, as published)
# ---------------------------------------------------------------------------
def compute_styles() -> dict:
    c = data.aqr("Century-of-Factor-Premia-Monthly", "Century of Factor Premia", "2025-12")
    m = c["date"] <= 202012
    cols = c["columns"]
    V = c["values"][m]
    dts = c["date"][m]
    pick = {k: cols.index(f"All asset classes {k}") for k in ("Value", "Momentum", "Carry", "Defensive", "Multi-style")}
    out = {}
    for k, j in pick.items():
        x = V[:, j]
        ok = np.isfinite(x)
        out[k] = {"sharpe": float(np.mean(x[ok]) / np.std(x[ok]) * math.sqrt(12)), "first": int(dts[ok][0]),
                  "mean": float(np.mean(x[ok]) * 12), "vol": float(np.std(x[ok]) * math.sqrt(12))}
    keys = ["Value", "Momentum", "Carry", "Defensive"]
    X = np.column_stack([V[:, pick[k]] for k in keys])
    ok = np.isfinite(X).all(1)
    C = np.corrcoef(X[ok].T)
    carry = {}
    for a in ("Equity indices", "Fixed income", "Currencies", "Commodities"):
        j = cols.index(f"{a} Carry")
        x = V[:, j]
        okk = np.isfinite(x)
        carry[a] = {"sharpe": float(np.mean(x[okk]) / np.std(x[okk]) * math.sqrt(12)), "first": int(dts[okk][0])}
    # worst calendar years of the multi-style book, and the market's return in them
    ms = V[:, pick["Multi-style"]]
    mkt = V[:, cols.index("Equity indices Market")]
    yrs = np.unique(dts // 100)
    yr_ms = {int(y): float(np.prod(1 + np.nan_to_num(ms[dts // 100 == y])) - 1) for y in yrs}
    yr_mk = {int(y): float(np.prod(1 + np.nan_to_num(mkt[dts // 100 == y])) - 1) for y in yrs}
    worst_mkt = sorted(yr_mk, key=yr_mk.get)[:6]
    return _json({"styles": out, "corr": C, "keys": keys, "carry": carry,
                  "crises": [{"year": y, "mkt": yr_mk[y], "styles": yr_ms[y]} for y in worst_mkt],
                  "cum": {k: np.nancumsum(np.log1p(np.nan_to_num(V[:, pick[k]]))) for k in keys + ["Multi-style"]},
                  "dates": dts})


# ---------------------------------------------------------------------------
# Selling insurance
# ---------------------------------------------------------------------------
def compute_shortvol() -> dict:
    put = data.cboe_index("PUT")
    kf = data.ken_french_daily(through="2020-12-31")
    m = (put["date"] >= 20070101) & (put["date"] <= RESEARCH_END)      # daily from 2007; sparse before
    pd_, pc = put["date"][m], put["close"][m]
    # month-end levels of PUT
    mon = pd_ // 100
    ends = np.r_[np.flatnonzero(mon[1:] != mon[:-1]), len(mon) - 1]
    pm, pv = mon[ends], pc[ends]
    put_r = pv[1:] / pv[:-1] - 1
    months = pm[1:]
    km, kr = _monthly(kf["date"], kf["mkt"])
    kd = dict(zip(km.tolist(), kr.tolist()))
    mkt = np.array([kd.get(int(x), np.nan) for x in months])
    rf = dict(zip(*_monthly(kf["date"], kf["rf"])))
    rfm = np.array([rf.get(int(x), 0.0) for x in months])
    ok = np.isfinite(mkt)
    pe, me = put_r[ok] - rfm[ok], mkt[ok] - rfm[ok]
    beta = float(np.cov(pe, me)[0, 1] / np.var(me))
    ev = {}
    for name, a, b in (("2008", 200809, 200811), ("2020", 202002, 202003)):
        k = (months >= a) & (months <= b)
        ev[name] = {"put": float(np.prod(1 + put_r[k]) - 1), "mkt": float(np.prod(1 + mkt[k]) - 1)}
    return _json({"put": _stats(pe, 12), "mkt": _stats(me, 12), "beta": beta,
                  "alpha": float((pe.mean() - beta * me.mean()) * 12), "events": ev, "months": months[ok],
                  "cum": {"put": np.cumprod(1 + put_r[ok]) - 1, "mkt": np.cumprod(1 + mkt[ok]) - 1}})


# ---------------------------------------------------------------------------
# Calendar effects
# ---------------------------------------------------------------------------
def compute_calendar() -> dict:
    kf = data.ken_french_daily(through="2020-12-31")
    d, r = kf["date"], kf["mkt_rf"]
    mon = d // 100
    last = np.r_[mon[1:] != mon[:-1], True]
    first_idx = np.r_[0, np.flatnonzero(mon[1:] != mon[:-1]) + 1]
    tom = np.zeros(len(d), bool)
    tom[last] = True
    for k in range(3):
        idx = first_idx + k
        tom[idx[idx < len(d)]] = True
    by = {}
    for a, b in ((1926, 1962), (1963, 1990), (1991, 2020)):
        k = (d // 10000 >= a) & (d // 10000 <= b)
        by[f"{a}-{b}"] = {"tom": float(r[k & tom].mean() * 1e4), "rest": float(r[k & ~tom].mean() * 1e4),
                          "share_days": float((k & tom).sum() / k.sum()),
                          "share_return": float(r[k & tom].sum() / r[k].sum())}
    # overnight and intraday, SPY 1993-2020
    s = data.yahoo_total("SPY", start="1993-01-29")
    m = s["date"] <= RESEARCH_END
    dd, adj, op, cl = s["date"][m], s["adj"][m], s["open"][m], s["close"][m]
    f = adj / cl                                   # adjustment factor of each day
    over = (op[1:] * f[1:]) / (cl[:-1] * f[:-1]) - 1
    intra = cl[1:] / op[1:] - 1
    yrs = dd[1:] // 10000
    return _json({"tom": by, "over": _stats(over), "intra": _stats(intra),
                  "cum": {"dates": dd[1:][::5], "over": (np.cumprod(1 + over) - 1)[::5],
                          "intra": (np.cumprod(1 + intra) - 1)[::5]},
                  "n_days": int(len(over)), "first": int(dd[0])})


# ---------------------------------------------------------------------------
# Research: the trend identity
# ---------------------------------------------------------------------------
def compute_theory() -> dict:
    rng = np.random.default_rng(3201)
    sims = []
    for n in (2, 3, 5, 10, 21, 63, 126, 252):
        k = max(2000, 400000 // n)
        r = rng.standard_normal(n * k)
        S, Q, P = SY.linear_trend_blocks(r, n)
        z = P - P.mean()
        sims.append({"n": n, "skew": float(np.mean(z ** 3) / np.mean(z ** 2) ** 1.5), "theory": SY.trend_skew_theory(n),
                     "mean": float(P.mean()), "var": float(P.var()), "var_theory": n * (n - 1) / 2, "win": float(np.mean(P > 0)),
                     "identity_err": float(np.max(np.abs(P - (S ** 2 - Q) / 2)))})
    # fat tails and volatility clustering: a GARCH(1,1) with t(5) shocks
    gs = []
    for n in (21, 63):
        k = 4000
        T = n * k
        h, x = np.empty(T), np.empty(T)
        v = 1.0
        e = rng.standard_t(5, T) / math.sqrt(5 / 3)
        for t in range(T):
            v = 0.05 + 0.10 * (x[t - 1] ** 2 if t else 1.0) + 0.85 * v
            x[t] = math.sqrt(v) * e[t]
        S, Q, P = SY.linear_trend_blocks(x, n)
        chunks = [SY.skewness(c) for c in np.array_split(P, 8)]
        gs.append({"n": n, "skew_median": float(np.median(chunks)), "theory": SY.trend_skew_theory(n),
                   "win": float(np.mean(P > 0))})
    # the ETF panel, research years: returns standardised by the prior day's EWMA volatility, blocks of 21 and 63
    d, R, rf = _panel()
    vol = SY.ewma_vol(R)
    Z = R[1:] / (vol[:-1] / math.sqrt(252))
    data_rows = []
    for n in (21, 63):
        Ps, Ss, Qs, means, preds = [], [], [], [], []
        for j in range(len(SYMS)):
            z = Z[:, j]
            z = z[np.isfinite(z)]
            if len(z) < 5 * n:
                continue
            S, Q, P = SY.linear_trend_blocks(z, n)
            Ps.append(P); Ss.append(S); Qs.append(Q)
            ac = SY.autocov(z, n)
            means.append(float(P.mean()))
            preds.append(SY.trend_mean_theory(ac, n))
        P = np.concatenate(Ps)
        zP = P - P.mean()
        data_rows.append({"n": n, "skew": float(np.mean(zP ** 3) / np.mean(zP ** 2) ** 1.5),
                          "theory": SY.trend_skew_theory(n), "blocks": int(len(P)), "win": float(np.mean(P > 0)),
                          "mean": float(np.mean(means)), "pred": float(np.mean(preds)),
                          "corr_mean_pred": float(np.corrcoef(means, preds)[0, 1])})
    # one asset's smile: SPY's 63-day blocks, P against S
    z = Z[:, SYMS.index("SPY")]
    z = z[np.isfinite(z)]
    S, Q, P = SY.linear_trend_blocks(z, 63)
    # the TSMOM book (sign rule) monthly skew against the linear rule's
    p, _ = _trend_book(d, R, 252, "sign")
    _, mp = _monthly(d[d >= 20070201], p[d >= 20070201])
    return _json({"sims": sims, "garch": gs, "data": data_rows, "spy": {"S": S, "Q": Q, "P": P},
                  "tsmom_monthly_skew": SY.skewness(mp)})


# ---------------------------------------------------------------------------
# The envelope
# ---------------------------------------------------------------------------
TREND = "trend_part32"
RP = "riskparity_part32"


def compute_envelope() -> dict:
    from explainer.quant.house import track
    t = load("trend")
    code_t = inspect.getsource(SY.tsmom_positions) + inspect.getsource(SY.book) + inspect.getsource(_trend_book)
    pit.register(TREND, code_t, {"universe": "23 ETFs, five classes", "signal": "sign of the 252-day excess return",
                                 "sizing": "40%/ex-ante EWMA vol (com 60) per asset, book scaled to 10%",
                                 "rebalance": "monthly"}, trials=int(t["n_trials"]))
    code_r = inspect.getsource(SY.risk_parity) + inspect.getsource(_rp)
    pit.register(RP, code_r, {"universe": ", ".join(RP_COLS), "rule": "inverse vol within class, equal risk across, "
                              "levered to 10% on a 252-day covariance, cap 4x", "rebalance": "monthly"}, trials=2)
    d, R, rf = _panel_full()
    pit.open_envelope(TREND, "yahoo/etf_panel_excess", d, np.where(np.isfinite(R), np.round(R, 10), -999.0))
    pit.open_envelope(RP, "yahoo/etf_panel_excess", d, np.where(np.isfinite(R), np.round(R, 10), -999.0))
    res, hold = d <= RESEARCH_END, d > RESEARCH_END
    live = d >= 20070201
    p_t, _ = _trend_book(d, R, 252, "sign")
    p_r, lev, W = _rp(d, R)
    spy = R[:, SYMS.index("SPY")]
    sixty = 0.6 * spy + 0.4 * R[:, SYMS.index("IEF")]
    out = {}
    for k, p in (("trend", p_t), ("rp", p_r), ("spy", spy), ("6040", sixty)):
        mr_d, mr = _monthly(d[res & live], p[res & live])
        mh_d, mh = _monthly(d[hold], p[hold])
        out[k] = {"res": _stats(p[res & live]), "hold": _stats(p[hold]), "hold_months": mh_d, "hold_m": mh,
                  "cum_hold": np.cumprod(1 + mh) - 1,
                  "y2022": float(np.prod(1 + mh[mh_d // 100 == 2022]) - 1)}
        if k in ("trend", "rp"):
            name = TREND if k == "trend" else RP
            out[k]["row"] = track.record(name, 32, mr, mh, 0.0, note=("TSMOM on 23 ETFs" if k == "trend" else
                                                                     "inverse-vol risk parity on 10 ETFs") +
                                         ", excess of T-bills, before costs")
    # 2022: the stock-bond correlation, daily, in the sealed years
    h = hold & np.isfinite(spy) & np.isfinite(R[:, SYMS.index("TLT")])
    yrs = {}
    for y in range(2021, 2026):
        k = h & (d // 10000 == y)
        yrs[str(y)] = float(np.corrcoef(spy[k], R[k, SYMS.index("TLT")])[0, 1])
    k = res & live & np.isfinite(spy) & np.isfinite(R[:, SYMS.index("TLT")])
    sb_res = float(np.corrcoef(spy[k], R[k, SYMS.index("TLT")])[0, 1])
    # the trend book's 2022 by asset class
    by = {}
    for g, v in CLASSES.items():
        pg, _ = _trend_book(d, R, 252, "sign", [SYMS.index(s) for s in v])
        mhd, mh = _monthly(d[hold], pg[hold])
        by[g] = float(np.prod(1 + mh[mhd // 100 == 2022]) - 1)
    lev_hold = lev[hold & np.isfinite(lev)]
    return _json({"trials": pit.trials_so_far(), "n_trials": {"trend": int(t["n_trials"]), "rp": 2}, "books": out,
                  "sb_corr": {"research": sb_res, "years": yrs}, "trend_2022_by_class": by,
                  "rp_lev_hold": {"mean": float(np.mean(lev_hold)), "min": float(np.min(lev_hold))}})


ITEMS = {"panel": compute_panel, "trend": compute_trend, "voltarget": compute_voltarget,
         "riskparity": compute_riskparity, "styles": compute_styles, "shortvol": compute_shortvol,
         "calendar": compute_calendar, "theory": compute_theory, "envelope": compute_envelope}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
