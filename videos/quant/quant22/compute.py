"""Every number in Part 22 (FX, Commodities and the Basis), computed and cached in .cache/quant22/.

    python -m videos.quant.quant22.compute [items] [--force]

* ``snb``       EUR/CHF from the Fed's noon rates, 2011-2016: the 1.20 floor and 15 January 2015;
* ``cip``       covered interest parity for sterling: the Bank of England's spot and 3-month forward against dollar and
                sterling 3-month LIBOR, monthly 1986-2016, and the basis;
* ``fama``      the Fama regression for nine currencies against the dollar, monthly 1999-2025 (yen from 2002);
* ``carry``     carry portfolios (long the three highest-yielding, short the three lowest), their crash statistics,
                and each currency's skewness against its average interest differential;
* ``yen2024``   the yen and the Nikkei, June-September 2024;
* ``fxopt``     Garman-Kohlhagen, the four delta conventions and a vanna-volga smile on an illustrative EUR/USD
                market;
* ``erm``       sterling against the Deutsche mark, 1990-1993, with the ERM band; the first-generation attack model;
* ``oil``       the NYMEX WTI curve (contracts 1-4, EIA) 1986-2024: contango and backwardation, the implied
                convenience yield, a rolled front-month index against the spot, April 2020;
* ``negoil``    options near a zero price: Black-76 against Bachelier on WTI-like futures;
* ``gas``       Henry Hub's seasonal curve, its futures in September 2006 (Amaranth), European gas against American
                (IMF, monthly); a spark-spread option by Margrabe;
* ``basis``     the Treasury cash-futures basis: leveraged funds' and asset managers' futures positions (CFTC), and the
                arithmetic of the trade;
* ``inflation`` breakevens (5-year, 10-year, 5y5y), and the 5-year breakeven against the CPI inflation that followed.
"""

from __future__ import annotations

import json

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, exotics as EX, macro as M, quoting as QT, termstructure as TS

CACHE = Cache("quant22")
load = CACHE.load

THROUGH = "2025-12-31"
# currency: (FRED spot series, quoted as USD per unit?, OECD 3-month rate series)
CCY = {
    "EUR": ("DEXUSEU", True, "IR3TIB01EZM156N"),
    "JPY": ("DEXJPUS", False, "IR3TIB01JPM156N"),
    "GBP": ("DEXUSUK", True, "IR3TIB01GBM156N"),
    "CHF": ("DEXSZUS", False, "IR3TIB01CHM156N"),
    "AUD": ("DEXUSAL", True, "IR3TIB01AUM156N"),
    "CAD": ("DEXCAUS", False, "IR3TIB01CAM156N"),
    "NZD": ("DEXUSNZ", True, "IR3TIB01NZM156N"),
    "NOK": ("DEXNOUS", False, "IR3TIB01NOM156N"),
    "SEK": ("DEXSDUS", False, "IR3TIB01SEM156N"),
}
US_RATE = "IR3TIB01USM156N"


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _fy(d):
    d = np.asarray(d)
    return d // 10000 + (d // 100 % 100 - 1) / 12 + (d % 100 - 1) / 365


def _month_end(dates, values):
    """The last observation of each calendar month: (YYYYMM, value)."""
    ym = np.asarray(dates) // 100
    last = np.r_[ym[1:] != ym[:-1], True]
    return ym[last], np.asarray(values)[last]


def _month_mean(dates, values):
    ym = np.asarray(dates) // 100
    u, inv = np.unique(ym, return_inverse=True)
    s = np.bincount(inv, weights=np.asarray(values, float))
    return u, s / np.bincount(inv)


def _monthly_rate(series, start="1950-01-01"):
    d = data.fred(series, start, THROUGH)
    return np.asarray(d["date"]) // 100, np.asarray(d["value"]) / 100


def _usd_per(ccy):
    """Daily USD per unit of ``ccy`` from the Fed's noon rates."""
    sid, usd_per, _ = CCY[ccy]
    d = data.fred(sid, "1971-01-01", THROUGH)
    v = np.asarray(d["value"], float)
    return np.asarray(d["date"]), (v if usd_per else 1 / v)


def compute_snb() -> dict:
    de, eu = _usd_per("EUR")
    dc, ch = _usd_per("CHF")
    common, ie, ic = np.intersect1d(de, dc, return_indices=True)
    eurchf = eu[ie] / ch[ic]  # CHF per EUR = (USD per EUR) / (USD per CHF)
    sel = (common >= 20100101) & (common <= 20161231)
    t, v = common[sel], eurchf[sel]
    k = int(np.where(t == 20150115)[0][0])
    r = np.diff(np.log(eurchf))
    dsel = (common[1:] >= 20120101) & (common[1:] <= 20141231)
    return _json({"t": _fy(t), "dates": t, "eurchf": v, "before": float(v[k - 1]), "on": float(v[k]),
                  "move": float(v[k] / v[k - 1] - 1), "after_month": float(v[k + 20]),
                  "vol_2012_2014": float(r[dsel].std() * np.sqrt(252)), "z_move": float(np.log(v[k] / v[k - 1]) /
                                                                                       r[dsel].std()),
                  "floor_set": 20110906})


def compute_cip() -> dict:
    """Sterling against the dollar with LIBOR on both sides, as Du, Tepper and Verdelhan measure it: dollar 3-month
    LIBOR (the Fed's TED spread plus the 3-month bill, daily, act/360) and sterling 3-month LIBOR (monthly, act/365),
    against the Bank of England's spot and 3-month forward (monthly averages of daily quotes), 1986-2016."""
    s = data.boe("XUDLUSS", 1975)
    f = data.boe("XUDLDS3", 1975)
    common, i1, i2 = np.intersect1d(s["date"], f["date"], return_indices=True)
    fp = np.log(f["value"][i2] / s["value"][i1]) / 0.25  # annualised forward premium of sterling (USD per GBP)
    ym, fpm = _month_mean(common, fp)
    _, sm = _month_mean(common, s["value"][i1])
    _, fm = _month_mean(common, f["value"][i2])
    ted = data.fred("TEDRATE", "1986-01-01", "2022-01-21")
    tb = data.fred("DTB3", "1954-01-01", THROUGH)
    c2, a, b = np.intersect1d(ted["date"], tb["date"], return_indices=True)
    yu, ru = _month_mean(c2, (np.asarray(ted["value"])[a] + np.asarray(tb["value"])[b]) / 100)
    g = data.fred("LIOR3MUKM", "1970-01-01", THROUGH)
    yg, rg = np.asarray(g["date"]) // 100, np.asarray(g["value"]) / 100
    keep = np.intersect1d(np.intersect1d(ym, yu), yg)
    ia = np.searchsorted(ym, keep)
    fpk, Sk, Fk = fpm[ia], sm[ia], fm[ia]
    ruk = ru[np.searchsorted(yu, keep)] * 365 / 360  # dollar LIBOR is act/360: put both on one year
    rgk = rg[np.searchsorted(yg, keep)]
    diff = M.cc(ruk, 0.25) - M.cc(rgk, 0.25)  # what parity says the forward premium should be
    x = diff - fpk  # the basis: x = y_USD - y_GBP - ln(F/S)/tau
    t = keep // 100 + (keep % 100 - 0.5) / 12
    pre, post, cr = (keep < 200708), (keep >= 201001), (keep >= 200708) & (keep <= 200912)
    j = int(np.searchsorted(keep, 201606))
    worked = {"ym": int(keep[j]), "S": float(Sk[j]), "F": float(Fk[j]), "r_usd": float(ruk[j]), "r_gbp": float(rgk[j])}
    worked["F_parity"] = float(M.cip_forward(worked["S"], worked["r_usd"], worked["r_gbp"], 0.25))
    worked["x_bp"] = float(1e4 * x[j])
    dec = (keep % 100 == 12)
    worked["dec_post_bp"] = float(1e4 * x[post & dec].mean())
    worked["other_post_bp"] = float(1e4 * x[post & ~dec].mean())
    return _json({"t": t, "fp": fpk, "diff": diff, "x": x, "mean_pre_bp": float(1e4 * x[pre].mean()),
                  "sd_pre_bp": float(1e4 * x[pre].std()), "mean_post_bp": float(1e4 * x[post].mean()),
                  "sd_post_bp": float(1e4 * x[post].std()), "mean_crisis_bp": float(1e4 * x[cr].mean()),
                  "min_bp": float(1e4 * x.min()), "min_ym": int(keep[np.argmin(x)]), "worked": worked,
                  "corr": float(np.corrcoef(diff, fpk)[0, 1]), "start": int(keep[0]), "end": int(keep[-1])})


def _monthly_panel(start=199901):
    """End-of-month USD per unit and the OECD 3-month rate (monthly average) for each currency, aligned."""
    yu, ru = _monthly_rate(US_RATE)
    months = yu[(yu >= start) & (yu <= 202512)]
    Q = np.full((len(months), len(CCY)), np.nan)
    R = np.full((len(months), len(CCY)), np.nan)
    for j, c in enumerate(CCY):
        d, q = _usd_per(c)
        ym, qe = _month_end(d, q)
        yr, rr = _monthly_rate(CCY[c][2])
        for i, m in enumerate(months):
            a, b = np.searchsorted(ym, m), np.searchsorted(yr, m)
            if a < len(ym) and ym[a] == m:
                Q[i, j] = qe[a]
            if b < len(yr) and yr[b] == m:
                R[i, j] = rr[b]
    return months, Q, R, ru[np.searchsorted(yu, months)]


def compute_fama() -> dict:
    months, Q, R, ru = _monthly_panel()
    out, pooled_ds, pooled_fp = {}, [], []
    for j, c in enumerate(CCY):
        ok = np.isfinite(Q[:, j]) & np.isfinite(R[:, j])
        idx = np.where(ok)[0]
        idx = idx[np.r_[True, np.diff(idx) == 1]]  # a contiguous run
        q, r, u = Q[idx, j], R[idx, j], ru[idx]
        f = M.fama_regression(q, u, r, 1 / 12, lags=3)
        s_ = -np.log(q)
        out[c] = {**f, "start": int(months[idx[0]]), "mean_diff": float(np.mean(r - u))}
        pooled_ds += list(np.diff(s_))
        pooled_fp += list((r[:-1] - u[:-1]) / 12)
    from explainer.quant.house.econ import ols
    o = ols(np.array(pooled_ds), np.array(pooled_fp), se="white")
    # an example scatter: the yen's monthly forward premium against the next month's change in the log rate
    j = list(CCY).index("AUD")
    ok = np.isfinite(Q[:, j]) & np.isfinite(R[:, j])
    q, r, u = Q[ok, j], R[ok, j], ru[ok]
    return _json({"by": out, "pooled": {"beta": float(o["beta"][1]), "se": float(o["se"][1]), "n": int(o["n"])},
                  "scatter": {"ccy": "AUD", "fp": (r[:-1] - u[:-1]) / 12, "ds": np.diff(-np.log(q))}})


def compute_carry() -> dict:
    months, Q, R, ru = _monthly_panel()
    ex = np.full((len(months) - 1, len(CCY)), np.nan)
    diff = R[:-1] - ru[:-1, None]
    for j in range(len(CCY)):
        ex[:, j] = np.log(Q[1:, j] / Q[:-1, j]) + (R[:-1, j] - ru[:-1]) / 12
    cs = M.carry_sort(ex, diff, k=3)
    ls = cs["ls"]
    ok = np.isfinite(ls)
    t = months[1:] // 100 + (months[1:] % 100 - 0.5) / 12
    st = M.crash_stats(ls[ok])
    worst = np.argsort(np.where(ok, ls, np.inf))[:5]
    per = {}
    for j, c in enumerate(CCY):
        e = ex[:, j]
        g = np.isfinite(e)
        st_c = M.crash_stats(e[g])
        per[c] = {"mean_diff": float(np.nanmean(diff[:, j])), "skew": st_c["skew"], "mean": st_c["mean"],
                  "vol": st_c["vol"]}
    # how often each currency sat in the long and short legs
    legs = {c: {"long": 0, "short": 0} for c in CCY}
    for i in range(diff.shape[0]):
        okc = np.isfinite(diff[i]) & np.isfinite(ex[i])
        if okc.sum() < 6:
            continue
        idx = np.where(okc)[0]
        order = idx[np.argsort(diff[i, idx])]
        for k_ in order[-3:]:
            legs[list(CCY)[k_]]["long"] += 1
        for k_ in order[:3]:
            legs[list(CCY)[k_]]["short"] += 1
    # the strategy scaled to 10% volatility, cumulative
    cum = np.cumsum(np.where(ok, ls, 0.0))
    return _json({"t": t, "ls": ls, "cum": cum, "long": cs["long"], "short": cs["short"], "stats": st,
                  "worst": [{"t": float(t[i]), "ym": int(months[1:][i]), "r": float(ls[i])} for i in worst],
                  "per": per, "legs": legs})


def compute_yen2024() -> dict:
    d, q = _usd_per("JPY")
    jpy = 1 / q  # yen per dollar
    sel = (d >= 20240601) & (d <= 20240930)
    n = data.fred("NIKKEI225", "1949-05-01", THROUGH)
    nd, nv = np.asarray(n["date"]), np.asarray(n["value"])
    ns = (nd >= 20240601) & (nd <= 20240930)
    k = int(np.argmax(jpy[sel]))
    a5 = int(np.where(nd == 20240805)[0][0])
    return _json({"t": _fy(d[sel]), "dates": d[sel], "usdjpy": jpy[sel], "peak": {"date": int(d[sel][k]),
                                                                              "v": float(jpy[sel][k])},
                  "aug5": float(jpy[d == 20240805][0]), "nikkei_t": _fy(nd[ns]), "nikkei": nv[ns],
                  "nikkei_aug5": float(nv[a5] / nv[a5 - 1] - 1), "nikkei_aug6": float(nv[a5 + 1] / nv[a5] - 1)})


def compute_fxopt() -> dict:
    """An illustrative EUR/USD market (labelled as such on screen): spot 1.10, USD 4.3%, EUR 2.0%, three months,
    ATM 7.5%, 25-delta risk reversal -0.6, butterfly 0.25."""
    S, T, rd, rf = 1.10, 0.25, 0.043, 0.020
    atm, rr, bf = 0.075, -0.006, 0.0025
    F = S * np.exp((rd - rf) * T)
    q = M.smile_quotes(atm, rr, bf)
    Katm = M.atm_dns_strike(F, T, atm)
    K25c = M.strike_from_delta(S, T, q["25c"], rd, rf, 0.25, 1, "forward")
    K25p = M.strike_from_delta(S, T, q["25p"], rd, rf, -0.25, -1, "forward")
    Ks = np.linspace(K25p * 0.96, K25c * 1.04, 41)
    vv = QT.vanna_volga(Ks, F, T, [K25p, Katm, K25c], [q["25p"], atm, q["25c"]], atm)
    deltas = {k: float(M.fx_delta(S, K25c, T, q["25c"], rd, rf, 1, k)) for k in ("spot", "forward", "spot_pa",
                                                                               "forward_pa")}
    gk = float(M.garman_kohlhagen(S, Katm, T, atm, rd, rf, 1))
    g = bs.greeks(S, Katm, T, atm, rd, rf, 1)
    # a premium-adjusted pair (USD/JPY-like: S = 150, rd = JPY 0.5%, rf = USD 4.3%, vol 10%)
    S2, rd2, rf2, v2 = 150.0, 0.005, 0.043, 0.10
    k_pa = M.strike_from_delta(S2, T, v2, rd2, rf2, 0.25, 1, "forward_pa")
    k_np = M.strike_from_delta(S2, T, v2, rd2, rf2, 0.25, 1, "forward")
    # the premium-adjusted call delta as a function of strike: it is not monotone
    F2 = S2 * np.exp((rd2 - rf2) * T)
    kk = F2 * np.exp(np.linspace(-0.5, 0.5, 101))
    dpa = M.fx_delta(S2, kk, T, v2, rd2, rf2, 1, "forward_pa")
    dnp = M.fx_delta(S2, kk, T, v2, rd2, rf2, 1, "forward")
    return _json({"S": S, "T": T, "rd": rd, "rf": rf, "F": F, "quotes": q, "rr": rr, "bf": bf,
                  "K": {"25p": K25p, "atm": Katm, "25c": K25c}, "Ks": Ks, "vv": vv, "deltas": deltas,
                  "gk_atm": gk, "gk_pips": gk * 1e4, "vega_atm": float(g["vega"]) / 100,
                  "pa": {"S": S2, "F": F2, "K_pa": k_pa, "K_np": k_np, "kk": kk, "dpa": dpa, "dnp": dnp},
                  "atmf": F})


def compute_erm() -> dict:
    d = data.boe("XUDLDMS", 1975)
    dates, v = np.asarray(d["date"]), np.asarray(d["value"])
    sel = (dates >= 19900101) & (dates <= 19931231)
    k = int(np.where(dates == 19920916)[0][0])
    a = M.attack_model(peg=1.0, d0=0.5, mu=0.05, alpha=2.0, T=14.0)
    return _json({"t": _fy(dates[sel]), "dmgbp": v[sel], "central": 2.95, "floor": 2.7780, "ceiling": 3.1320,
                  "entry": 19901008, "sep15": float(v[k - 1]), "sep16": float(v[k]), "sep17": float(v[k + 1]),
                  "oct30": float(v[dates == 19921030][0]) if np.any(dates == 19921030) else None,
                  "min_after": float(v[(dates > 19920916) & (dates <= 19931231)].min()), "attack": a})


def _oil():
    c = [data.eia_daily(f"RCLC{i}") for i in (1, 2, 3, 4)]
    d = c[0]["date"]
    for x in c[1:]:
        d = np.intersect1d(d, x["date"])
    P = np.stack([x["value"][np.searchsorted(x["date"], d)] for x in c], 1)
    return d, P


def compute_oil() -> dict:
    d, P = _oil()
    sel = d >= 19860101
    d, P = d[sel], P[sel]
    tb = data.fred("DTB3", "1954-01-01", THROUGH)
    r = np.interp(_fy(d), _fy(np.asarray(tb["date"])), np.asarray(tb["value"]) / 100)
    slope = np.log(P[:, 3] / P[:, 0]) / 0.25  # annualised, contracts 1 to 4 (about three months)
    ok = P[:, 0] > 0
    cy = np.where(ok, M.implied_convenience(np.where(ok, P[:, 0], 1), P[:, 1], 1 / 12, r), np.nan)
    contango = np.mean(P[ok, 1] > P[ok, 0])
    ro = M.rolled_front(d, P[:, 0], P[:, 1], roll_offset=5)
    rr = np.nan_to_num(ro["r"])
    idx = np.cumprod(1 + rr)
    spot = P[:, 0] / P[0, 0]
    y = d // 10000
    yrs = np.unique(y)
    ann = []
    for yy in yrs:
        m = y == yy
        if m.sum() < 200:
            continue
        ann.append({"y": int(yy), "futures": float(np.prod(1 + rr[m]) - 1),
                    "spot": float(P[m, 0][-1] / P[m, 0][0] - 1)})
    # snapshots of the curve
    snaps = {}
    for lab, dd in (("2008-07-03", 20080703), ("2008-12-19", 20081219), ("2014-06-20", 20140620),
                    ("2016-02-11", 20160211), ("2020-04-17", 20200417), ("2020-04-20", 20200420),
                    ("2020-04-21", 20200421), ("2022-03-08", 20220308)):
        j = int(np.searchsorted(d, dd))
        snaps[lab] = {"date": int(d[j]), "P": P[j]}
    t = _fy(d)
    step = slice(None, None, 5)
    yrs_tot = (t[-1] - t[0])
    return _json({"t": t[step], "c1": P[step, 0], "slope": slope[step], "cy": cy[step], "contango_share": float(contango),
                  "index": idx[step], "spot": spot[step], "annual": ann, "snaps": snaps,
                  "cagr_index": float(idx[-1] ** (1 / yrs_tot) - 1), "cagr_spot": float(spot[-1] ** (1 / yrs_tot) - 1),
                  "april": {"dates": d[(d >= 20200401) & (d <= 20200430)],
                            "P": P[(d >= 20200401) & (d <= 20200430)]}})


def compute_negoil() -> dict:
    """WTI-like options near zero: a future at $10 with Black vol 150% has a Bachelier (normal) vol of about $15; the
    Black model cannot price a future below zero, the normal model prices strikes at and below zero."""
    F, T = 10.0, 1 / 12
    Ks = np.linspace(1, 20, 39)
    black_vol = 1.5
    prices = bs.black(F, Ks, T, black_vol, 1.0, -1)
    from scipy.optimize import brentq
    normal_vols = np.array([brentq(lambda v: TS.bachelier(F, float(k), T, v, 1.0, -1) - float(p), 1e-6, 500.0,
                                   xtol=1e-12) for p, k in zip(prices, Ks)])
    sn = float(normal_vols[np.argmin(np.abs(Ks - F))])
    Fs = np.linspace(-10, 20, 61)
    put0 = np.array([TS.bachelier(f, 0.0, T, sn, 1.0, -1) for f in Fs])  # a put struck at zero, normal model
    put_negK = float(TS.bachelier(F, -5.0, T, sn, 1.0, -1))
    # what Black says a $1 future's at-the-money put is worth with the same normal vol ($15): its vol must be 1500%
    return _json({"F": F, "T": T, "Ks": Ks, "black_vol": black_vol, "normal_vols": normal_vols, "sn_atm": sn,
                  "Fs": Fs, "put0": put0, "put_negK": put_negK,
                  "black_needed_at_1": float(sn / 1.0)})


def compute_gas() -> dict:
    hh = data.fred("MHHNGSP", "1997-01-01", THROUGH)
    hd, hv = np.asarray(hh["date"]), np.asarray(hh["value"])
    eu = data.fred("PNGASEUUSDM", "1992-01-01", THROUGH)
    ed, ev = np.asarray(eu["date"]), np.asarray(eu["value"])
    # seasonality of the curve: contracts 1-4 on mid-month days, averaged by the month of contract 1's delivery
    c = [data.eia_daily(f"RNGC{i}", "ng") for i in (1, 2, 3, 4)]
    d = c[0]["date"]
    for x in c[1:]:
        d = np.intersect1d(d, x["date"])
    P = np.stack([x["value"][np.searchsorted(x["date"], d)] for x in c], 1)
    sel = (d >= 20060801) & (d <= 20061031)
    # month-of-year profile of the monthly Henry Hub spot, relative to each year's mean (2010-2025)
    m = (hd >= 20100101)
    yy, mm = hd[m] // 10000, hd[m] // 100 % 100
    rel = np.array([hv[m][i] / hv[m][yy == yy[i]].mean() for i in range(m.sum())])
    prof = np.array([rel[mm == k].mean() for k in range(1, 13)])
    # spark spread option (Margrabe): the right to burn gas into power, illustrative
    hr = 7.0
    power, gas = 42.0, 6.0
    mg = EX.margrabe(power, hr * gas, 0.5, 0.45, 0.40, 0.6)
    intrinsic = max(power - hr * gas, 0.0)
    rhos = np.linspace(-0.5, 0.95, 30)
    mg_rho = np.array([EX.margrabe(power, hr * gas, 0.5, 0.45, 0.40, float(r_)) for r_ in rhos])
    return _json({"hh_t": _fy(hd), "hh": hv, "eu_t": _fy(ed), "eu": ev, "profile": prof,
                  "amaranth": {"t": _fy(d[sel]), "dates": d[sel], "P": P[sel]},
                  "eu_peak": {"t": float(_fy(ed[np.argmax(ev)])), "v": float(ev.max()), "date": int(ed[np.argmax(ev)])},
                  "hh_same": float(hv[np.searchsorted(hd, ed[np.argmax(ev)])]),
                  "spark": {"power": power, "gas": gas, "hr": hr, "value": mg, "intrinsic": intrinsic, "rhos": rhos,
                            "by_rho": mg_rho}})


def compute_basis() -> dict:
    face = {"042601": 200_000, "044601": 100_000, "043602": 100_000, "020601": 100_000}
    names = {"042601": "2-year", "044601": "5-year", "043602": "10-year", "020601": "bond"}
    tot_lev, tot_am, dates = None, None, None
    by = {}
    for code, fv in face.items():
        x = data.cftc_tff(code)
        lev = (x["lev_money_positions_long"] - x["lev_money_positions_short"]) * fv / 1e9
        am = (x["asset_mgr_positions_long"] - x["asset_mgr_positions_short"]) * fv / 1e9
        if dates is None:
            dates, tot_lev, tot_am = x["date"], lev.copy(), am.copy()
        else:
            common, i1, i2 = np.intersect1d(dates, x["date"], return_indices=True)
            dates, tot_lev, tot_am = common, tot_lev[i1] + lev[i2], tot_am[i1] + am[i2]
        by[names[code]] = {"last_lev": float(lev[-1]), "last_am": float(am[-1])}
    t = _fy(dates)
    k20 = (dates >= 20200201) & (dates <= 20200430)
    feb = int(np.where(dates <= 20200225)[0][-1])
    apr = int(np.where(dates <= 20200331)[0][-1])
    # the arithmetic of one trade, illustrative: buy a cheapest-to-deliver note, sell the future, finance in repo
    cash_clean, accrued0, cf, fut, days, cpn = 98.50, 0.40, 0.8850, 110.90, 90, 0.04
    dirty = cash_clean + accrued0
    accrued_T = accrued0 + cpn * 100 * days / 365
    ir = M.implied_repo(dirty, fut, cf, accrued_T, days)
    gb = M.gross_basis(cash_clean, fut, cf)
    return _json({"t": t, "lev": tot_lev, "am": tot_am, "by": by, "lev_feb2020": float(tot_lev[feb]),
                  "lev_mar2020": float(tot_lev[apr]), "lev_min": float(tot_lev.min()),
                  "lev_min_t": float(t[np.argmin(tot_lev)]), "lev_last": float(tot_lev[-1]),
                  "am_last": float(tot_am[-1]),
                  "trade": {"clean": cash_clean, "dirty": dirty, "cf": cf, "fut": fut, "days": days, "cpn": cpn,
                            "implied_repo": float(ir), "gross_basis": float(gb), "accrued_T": accrued_T,
                            "invoice": float(M.invoice_price(fut, cf, accrued_T))}})


def compute_inflation() -> dict:
    b5 = data.fred("T5YIE", "2003-01-02", THROUGH)
    b10 = data.fred("T10YIE", "2003-01-02", THROUGH)
    f55 = data.fred("T5YIFR", "2003-01-02", THROUGH)
    cpi = data.fred("CPIAUCSL", "1947-01-01", THROUGH)
    cd, cv = np.asarray(cpi["date"]), np.asarray(cpi["value"])
    d5, v5 = np.asarray(b5["date"]), np.asarray(b5["value"]) / 100
    ym, b5m = _month_mean(d5, v5)
    real, starts = [], []
    for i, m in enumerate(ym):
        ri = M.realised_inflation(cd, cv, int(m) * 100 + 1, 5)
        if np.isfinite(ri):
            real.append(ri)
            starts.append(i)
    starts = np.array(starts)
    gap = b5m[starts] - np.array(real)
    t = ym // 100 + (ym % 100 - 0.5) / 12
    k = int(np.argmin(v5))
    k2 = int(np.argmax(v5))
    yoy = cv[12:] / cv[:-12] - 1
    return _json({"t5": _fy(d5)[::3], "b5": v5[::3], "t10": _fy(np.asarray(b10["date"]))[::3],
                  "b10": (np.asarray(b10["value"]) / 100)[::3], "t55": _fy(np.asarray(f55["date"]))[::3],
                  "f55": (np.asarray(f55["value"]) / 100)[::3], "tm": t, "b5m": b5m, "real_t": t[starts],
                  "real": np.array(real), "gap_mean": float(gap.mean()), "gap_sd": float(gap.std()),
                  "min": {"date": int(d5[k]), "v": float(v5[k])}, "max": {"date": int(d5[k2]), "v": float(v5[k2])},
                  "cpi_t": _fy(cd[12:]), "cpi_yoy": yoy, "cpi_peak": float(yoy[cd[12:] >= 20210101].max()),
                  "f55_mean": float(np.mean(np.asarray(f55["value"]))) / 100})


ITEMS = {"snb": compute_snb, "cip": compute_cip, "fama": compute_fama, "carry": compute_carry,
         "yen2024": compute_yen2024, "fxopt": compute_fxopt, "erm": compute_erm, "oil": compute_oil,
         "negoil": compute_negoil, "gas": compute_gas, "basis": compute_basis, "inflation": compute_inflation}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
