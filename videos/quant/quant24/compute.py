"""Every number in Part 24 (Factors), computed and cached in .cache/quant24/.

    python -m videos.quant.quant24.compute [items] [--force]

Research uses data to December 2020 only. The sealed hold-out (January 2021 to December 2025) is read in one item,
``envelope``, after each classic factor is registered (videos/quant/SYLLABUS.md, "The Track Record").

* ``race``       a dollar in each Fama-French factor and momentum, 1963-2020; their statistics;
* ``tests``      GRS and two-pass tests of the CAPM, FF3, Carhart and FF5 on the 25 size and value portfolios;
* ``sizevalue``  SMB and HML since 1926, before and after their discovery; January;
* ``momentum``   the momentum deciles since 1927; UMD; AQR's time-series momentum by asset class; the smile;
* ``crash``      1932 and 2009; Daniel and Moskowitz's bear-market betas; Barroso and Santa-Clara's scaling;
* ``profit``     RMW and CMA; is HML redundant?; the q-factors; the dividend discount model's B/M;
* ``lowrisk``    betting against beta (AQR, US and global); portfolios sorted on variance;
* ``everywhere`` value and momentum in eight markets (AQR); carry in four asset classes; quality minus junk;
* ``valuedecade`` HML 2007-2020; the value spread since 1926; HML with current prices (AQR's HML Devil);
* ``timing``     time-series factor momentum (Ehsani and Linnainmaa); the value spread as a forecast;
* ``china``      Liu, Stambaugh and Yuan's CH-4, 2000-2020, beside the US;
* ``construct``  a toy 2 x 3 sort, step by step;
* ``envelope``   the Track Record opens: ten classic factors registered, scored on 2021-2025 once.
"""

from __future__ import annotations

import inspect
import json

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import econ as E, factors as FA, pit, track

CACHE = Cache("quant24")
load = pit.counted(CACHE.load, 24)
THROUGH = "2025-12"
END = 202012


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _cut(d, *xs, start=0, end=END):
    m = (np.asarray(d) >= start) & (np.asarray(d) <= end)
    return (np.asarray(d)[m],) + tuple(np.asarray(x)[m] for x in xs)


def _ff5():
    k = data.ken_french_monthly("F-F_Research_Data_5_Factors_2x3_CSV.zip", "ff5_monthly", THROUGH)
    r = k["returns"]
    return {"date": k["date"], "mkt": r[:, 0], "smb": r[:, 1], "hml": r[:, 2], "rmw": r[:, 3], "cma": r[:, 4],
            "rf": r[:, 5]}


def _mom():
    k = data.ken_french_monthly("F-F_Momentum_Factor_CSV.zip", "mom_monthly", THROUGH)
    return k["date"], k["returns"][:, 0]


def _strev():
    k = data.ken_french_monthly("F-F_ST_Reversal_Factor_CSV.zip", "strev_monthly", THROUGH)
    return k["date"], k["returns"][:, 0]


def _on(d_from, x, d_to):
    """``x`` (dated ``d_from``) on the dates ``d_to`` (NaN where missing)."""
    idx = {int(a): i for i, a in enumerate(d_from)}
    return np.array([x[idx[int(a)]] if int(a) in idx else np.nan for a in d_to])


def compute_race() -> dict:
    f = _ff5()
    md, mom = _mom()
    d, mkt, smb, hml, rmw, cma = _cut(f["date"], f["mkt"], f["smb"], f["hml"], f["rmw"], f["cma"])
    umd = _on(md, mom, d)
    out = {"date": d, "series": {}, "stats": {}}
    for k, x in (("MKT", mkt), ("SMB", smb), ("HML", hml), ("UMD", umd), ("RMW", rmw), ("CMA", cma)):
        out["series"][k] = FA.cumulative(x)
        out["stats"][k] = FA.stats(x)
    X = np.c_[mkt, smb, hml, umd, rmw, cma]
    out["corr"] = np.corrcoef(X.T)
    out["names"] = ["MKT", "SMB", "HML", "UMD", "RMW", "CMA"]
    return _json(out)


def _ff25():
    k = data.ken_french_monthly("25_Portfolios_5x5_CSV.zip", "ff25", THROUGH)
    return k["date"], k["returns"], k["columns"]


def compute_tests() -> dict:
    f = _ff5()
    md, mom = _mom()
    d25, R25, cols = _ff25()
    d = f["date"][(f["date"] >= 196307) & (f["date"] <= END)]
    R = np.array([R25[list(d25).index(int(x))] for x in d])
    rf = _on(f["date"], f["rf"], d)
    ex = R - rf[:, None]
    g = {k: _on(f["date"], f[k], d) for k in ("mkt", "smb", "hml", "rmw", "cma")}
    umd = _on(md, mom, d)
    models = {"CAPM": np.c_[g["mkt"]], "FF3": np.c_[g["mkt"], g["smb"], g["hml"]],
              "Carhart": np.c_[g["mkt"], g["smb"], g["hml"], umd],
              "FF5": np.c_[g["mkt"], g["smb"], g["hml"], g["rmw"], g["cma"]]}
    out = {"models": {}, "mean": ex.mean(0) * 12, "columns": cols, "start": int(d[0]), "end": int(d[-1])}
    for k, F in models.items():
        t = FA.model_test(ex, F)
        B = np.linalg.lstsq(np.c_[np.ones(len(F)), F], ex, rcond=None)[0][1:]
        out["models"][k] = {"grs": t["grs"], "p": t["p"], "mean_abs_alpha": t["mean_abs_alpha"], "alpha": t["alpha"],
                            "lambda": t["lambda"], "t_shanken": t["t_shanken"], "df": t["df"],
                            "pred": (B.T @ F.mean(0)) * 12}
    return _json(out)


def compute_sizevalue() -> dict:
    ff = data.ken_french_factors_monthly(THROUGH)
    d, smb, hml, mkt = _cut(ff["date"], ff["smb"], ff["hml"], ff["mkt_rf"])
    out = {"full": {"SMB": FA.stats(smb), "HML": FA.stats(hml)}, "start": int(d[0])}
    pre, post = d <= 198012, d > 198012
    out["pre1981"] = {"SMB": FA.stats(smb[pre]), "HML": FA.stats(hml[pre])}
    out["post1981"] = {"SMB": FA.stats(smb[post]), "HML": FA.stats(hml[post])}
    jan = (d % 100) == 1
    out["smb_jan"] = float(smb[jan].mean())
    out["smb_rest"] = float(smb[~jan].mean())
    out["smb_jan_post"] = float(smb[jan & post].mean())
    out["smb_rest_post"] = float(smb[~jan & post].mean())
    dec = {}
    for y0 in range(1930, 2020, 10):
        m = (d >= y0 * 100 + 1) & (d <= (y0 + 9) * 100 + 12)
        dec[str(y0)] = {"SMB": float(smb[m].mean() * 12), "HML": float(hml[m].mean() * 12)}
    out["decades"] = dec
    out["date"] = d
    out["smb_cum"] = FA.cumulative(smb)
    out["hml_cum"] = FA.cumulative(hml)
    return _json(out)


def compute_momentum() -> dict:
    k = data.ken_french_monthly("10_Portfolios_Prior_12_2_CSV.zip", "mom_deciles", THROUGH)
    ff = data.ken_french_factors_monthly(THROUGH)
    d, R = _cut(k["date"], k["returns"])
    rf = _on(ff["date"], ff["rf"], d)
    ex = R - rf[:, None]
    md, mom = _mom()
    dm, umd = _cut(md, mom)
    ts = data.aqr("Time-Series-Momentum-Factors-Monthly", "TSMOM Factors", THROUGH)
    dt, T = _cut(ts["date"], ts["values"])
    tstats = {c: FA.stats(T[:, j]) for j, c in enumerate(ts["columns"])}
    umd_t = _on(md, mom, dt)
    mkt_t = _on(ff["date"], ff["mkt_rf"], dt)
    # the smile: quarterly TSMOM against the quarterly market
    q = len(dt) // 3
    Tq = np.array([np.prod(1 + T[3 * i:3 * i + 3, 0]) - 1 for i in range(q)])
    Mq = np.array([np.prod(1 + mkt_t[3 * i:3 * i + 3]) - 1 for i in range(q)])
    c2 = np.polyfit(Mq, Tq, 2)
    y08 = (dt >= 200801) & (dt <= 200812)
    return _json({"deciles": ex.mean(0) * 12, "dec_vol": ex.std(0) * np.sqrt(12), "start": int(d[0]),
                  "umd": FA.stats(umd), "ts": tstats, "ts_cols": ts["columns"], "ts_start": int(dt[0]),
                  "corr_umd_ts": float(np.corrcoef(umd_t, T[:, 0])[0, 1]),
                  "corr_ts_mkt": float(np.corrcoef(mkt_t, T[:, 0])[0, 1]),
                  "ts_2008": float(np.prod(1 + T[y08, 0]) - 1), "mkt_2008": float(np.prod(1 + mkt_t[y08]) - 1),
                  "smile": {"m": Mq, "t": Tq, "fit": c2}, "ts_cum": FA.cumulative(T[:, 0]), "ts_date": dt})


def compute_crash() -> dict:
    ff = data.ken_french_factors_monthly(THROUGH)
    md, mom = _mom()
    d, umd = _cut(md, mom)
    mkt = _on(ff["date"], ff["mkt_rf"], d)
    rf = _on(ff["date"], ff["rf"], d)
    w = FA.cumulative(umd)
    # bear: the market's cumulative return over the previous 24 months is negative
    cm = np.log1p(mkt + rf)
    past = np.array([cm[max(0, t - 24):t].sum() if t >= 24 else np.nan for t in range(len(d))])
    bear = np.nan_to_num(past, nan=1) < 0
    rebound = bear & (mkt > 0)
    cb = FA.conditional_beta(umd, mkt, bear, rebound)
    vs = FA.vol_scaled(umd, 0.12, 6)
    ok = np.isfinite(vs)

    def window(a, b):
        m = (d >= a) & (d <= b)
        return {"date": d[m], "umd": umd[m], "mkt": mkt[m], "cum_umd": float(np.prod(1 + umd[m]) - 1),
                "cum_mkt": float(np.prod(1 + mkt[m] + rf[m]) - 1)}
    order = np.argsort(umd)[:8]
    return _json({"date": d, "cum": w, "w2009": window(200903, 200905), "w1932": window(193207, 193208),
                  "w2009_full": window(200801, 200912), "worst": [{"date": int(d[i]), "r": float(umd[i])} for i in order],
                  "cond": cb, "raw": FA.stats(umd[ok]), "scaled": FA.stats(vs[ok]), "vs": vs,
                  "raw_2009": float(np.prod(1 + umd[(d >= 200903) & (d <= 200905)]) - 1),
                  "scaled_2009": float(np.prod(1 + vs[(d >= 200903) & (d <= 200905)]) - 1),
                  "dd": FA.drawdown(umd)})


def compute_profit() -> dict:
    f = _ff5()
    d, mkt, smb, hml, rmw, cma = _cut(f["date"], f["mkt"], f["smb"], f["hml"], f["rmw"], f["cma"])
    span = FA.alpha(hml, np.c_[mkt, smb, rmw, cma])
    span3 = FA.alpha(hml, np.c_[mkt, smb])
    q = data.q_factors(THROUGH)
    dq = q["date"]
    m = dq <= END
    qs = {k: FA.stats(q[k][m]) for k in ("R_ME", "R_IA", "R_ROE", "R_EG")}
    hml_q = _on(f["date"], f["hml"], dq[m])
    qa = FA.alpha(hml_q, np.c_[q["R_MKT"][m], q["R_ME"][m], q["R_IA"][m], q["R_ROE"][m]])
    corr = {"IA_CMA": float(np.corrcoef(q["R_IA"][m], _on(f["date"], f["cma"], dq[m]))[0, 1]),
            "ROE_RMW": float(np.corrcoef(q["R_ROE"][m], _on(f["date"], f["rmw"], dq[m]))[0, 1])}
    ddm = {"base": FA.ddm_bm(0.12, 0.05, 0.09), "low_roe": FA.ddm_bm(0.08, 0.05, 0.09),
           "high_inv": FA.ddm_bm(0.12, 0.07, 0.09), "high_r": FA.ddm_bm(0.12, 0.05, 0.11)}
    return _json({"RMW": FA.stats(rmw), "CMA": FA.stats(cma), "HML": FA.stats(hml), "span": span, "span3": span3,
                  "q": qs, "q_span_hml": qa, "corr": corr, "ddm": ddm, "start": int(d[0]), "q_start": int(dq[0]),
                  "corr_hml_cma": float(np.corrcoef(hml, cma)[0, 1])})


def compute_lowrisk() -> dict:
    bab = data.aqr("Betting-Against-Beta-Equity-Factors-Monthly", "BAB Factors", THROUGH)
    d, B = _cut(bab["date"], bab["values"])
    us = B[:, bab["columns"].index("USA")]
    gl = B[:, bab["columns"].index("Global")]
    ok_gl = np.isfinite(gl)
    var = data.ken_french_sorts("VAR", THROUGH)
    resv = data.ken_french_sorts("RESVAR", THROUGH)
    ff = data.ken_french_factors_monthly(THROUGH)
    out = {"bab_us": FA.stats(us[np.isfinite(us)]), "bab_global": FA.stats(gl[ok_gl]),
           "bab_us_start": int(d[np.isfinite(us)][0]), "bab_gl_start": int(d[ok_gl][0]),
           "bab_cum": FA.cumulative(us), "bab_date": d}
    for nm, k in (("var", var), ("resvar", resv)):
        dv, R = _cut(k["date"], k["returns"])
        q = [k["columns"].index(c) for c in ("Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20")]
        rf = _on(ff["date"], ff["rf"], dv)
        ex = R[:, q] - rf[:, None]
        mk = _on(ff["date"], ff["mkt_rf"], dv)
        betas = [float(np.polyfit(mk, ex[:, j], 1)[0]) for j in range(5)]
        out[nm] = {"mean": ex.mean(0) * 12, "vol": ex.std(0) * np.sqrt(12),
                   "sharpe": ex.mean(0) / ex.std(0) * np.sqrt(12), "beta": betas, "start": int(dv[0]),
                   "lmh": FA.stats(ex[:, 0] - ex[:, 4])}
    return _json(out)


def compute_everywhere() -> dict:
    v = data.aqr("Value-and-Momentum-Everywhere-Factors-Monthly", "VME Factors", THROUGH)
    d, V = _cut(v["date"], v["values"])
    mk = {"US stocks": "US90", "UK stocks": "UK90", "Europe stocks": "ROE90", "Japan stocks": "JP90",
          "equity indices": "EQ", "currencies": "FX", "bonds": "FI", "commodities": "COM"}
    out = {"markets": {}, "start": int(d[0])}
    for nm, s in mk.items():
        a = V[:, v["columns"].index(f"VALLS_VME_{s}")]
        b = V[:, v["columns"].index(f"MOMLS_VME_{s}")]
        ok = np.isfinite(a) & np.isfinite(b)
        c = 0.5 * a[ok] + 0.5 * b[ok]
        out["markets"][nm] = {"val": FA.stats(a[ok]), "mom": FA.stats(b[ok]), "combo": FA.stats(c),
                              "corr": float(np.corrcoef(a[ok], b[ok])[0, 1]), "start": int(d[ok][0])}
    a, b = V[:, v["columns"].index("VAL")], V[:, v["columns"].index("MOM")]
    ok = np.isfinite(a) & np.isfinite(b)
    out["global"] = {"val": FA.stats(a[ok]), "mom": FA.stats(b[ok]), "combo": FA.stats(0.5 * a[ok] + 0.5 * b[ok]),
                     "corr": float(np.corrcoef(a[ok], b[ok])[0, 1]), "cum_val": FA.cumulative(a[ok]),
                     "cum_mom": FA.cumulative(b[ok]), "cum_combo": FA.cumulative(0.5 * a[ok] + 0.5 * b[ok]),
                     "date": d[ok]}
    c = data.aqr("Century-of-Factor-Premia-Monthly", "Century of Factor Premia", THROUGH)
    dc, C = _cut(c["date"], c["values"])
    carry = {}
    for nm in ("Equity indices Carry", "Fixed income Carry", "Currencies Carry", "Commodities Carry"):
        x = C[:, c["columns"].index(nm)]
        ok = np.isfinite(x)
        carry[nm.replace(" Carry", "")] = dict(FA.stats(x[ok]), start=int(dc[ok][0]))
    out["carry"] = carry
    qmj = data.aqr("Quality-Minus-Junk-Factors-Monthly", "QMJ Factors", THROUGH)
    dq, Q = _cut(qmj["date"], qmj["values"])
    us = Q[:, qmj["columns"].index("USA")]
    ok = np.isfinite(us)
    ff = data.ken_french_factors_monthly(THROUGH)
    mk_q = _on(ff["date"], ff["mkt_rf"], dq[ok])
    out["qmj"] = dict(FA.stats(us[ok]), start=int(dq[ok][0]), beta=float(np.polyfit(mk_q, us[ok], 1)[0]))
    return _json(out)


def compute_valuedecade() -> dict:
    ff = data.ken_french_factors_monthly(THROUGH)
    d, hml = _cut(ff["date"], ff["hml"])
    m = d >= 200701
    dd = FA.drawdown(hml[m])
    bm = data.ken_french_block("Portfolios_Formed_on_BE-ME_CSV.zip", "Sum of BE / Sum of ME", "bm_sum_annual",
                               2020)
    yr = bm["date"]
    hi, lo = bm["values"][:, bm["columns"].index("Hi 30")], bm["values"][:, bm["columns"].index("Lo 30")]
    spread = FA.value_spread(hi, lo)
    dev = data.aqr("The-Devil-in-HMLs-Details-Factors-Monthly", "HML Devil", THROUGH)
    dv, D = _cut(dev["date"], dev["values"])
    us = D[:, dev["columns"].index("USA")]
    mm = dv >= 200701
    hml_on = _on(ff["date"], ff["hml"], dv[mm])
    return _json({"date": d[m], "cum": FA.cumulative(hml[m]), "dd": dd, "stats_0720": FA.stats(hml[m]),
                  "stats_2606": FA.stats(hml[d < 200701]), "years": yr, "spread": spread,
                  "spread_pct": float((spread[-1] > spread).mean()),
                  "devil_0720": FA.stats(us[mm]), "ff_0720_same": FA.stats(hml_on),
                  "devil_cum": FA.cumulative(us[mm]), "devil_date": dv[mm]})


def compute_timing() -> dict:
    f = _ff5()
    md, mom = _mom()
    sd, st = _strev()
    d = f["date"][(f["date"] >= 196307) & (f["date"] <= END)]
    names = ["SMB", "HML", "RMW", "CMA", "UMD", "STREV"]
    F = np.c_[_on(f["date"], f["smb"], d), _on(f["date"], f["hml"], d), _on(f["date"], f["rmw"], d),
              _on(f["date"], f["cma"], d), _on(md, mom, d), _on(sd, st, d)]
    fm = FA.factor_momentum(F, 12)
    ok = np.isfinite(fm["r"])
    tsm = FA.stats(fm["r"][ok])
    ew = FA.stats(fm["ew"][ok])
    umd = F[ok, 4]
    a = FA.alpha(umd, np.c_[fm["r"][ok]])
    # the value spread as a forecast of next year's HML (annual, 1927-2020)
    ff = data.ken_french_factors_monthly(THROUGH)
    bm = data.ken_french_block("Portfolios_Formed_on_BE-ME_CSV.zip", "Sum of BE / Sum of ME", "bm_sum_annual", 2020)
    yr = bm["date"]
    sp = FA.value_spread(bm["values"][:, bm["columns"].index("Hi 30")], bm["values"][:, bm["columns"].index("Lo 30")])
    hy = {}
    for y in range(1927, 2021):
        m = (ff["date"] >= y * 100 + 1) & (ff["date"] <= y * 100 + 12)
        hy[y] = float(np.prod(1 + ff["hml"][m]) - 1)
    xs = [sp[list(yr).index(y - 1)] for y in range(1927, 2021) if (y - 1) in yr]
    ys = [hy[y] for y in range(1927, 2021) if (y - 1) in yr]
    o = E.ols(np.array(ys), np.array(xs), se="nw", lags=2)
    return _json({"names": names, "tsfm": tsm, "ew": ew, "long_share": fm["long_share"], "umd_on_tsfm": a,
                  "cum_tsfm": FA.cumulative(fm["r"][ok]), "cum_ew": FA.cumulative(fm["ew"][ok]), "date": d[ok],
                  "spread_x": xs, "hml_y": ys, "slope": float(o["beta"][1]), "slope_t": float(o["beta"][1] / o["se"][1]),
                  "r2": float(o.get("r2", np.nan))})


def compute_china() -> dict:
    c = data.ch4()
    d = c["date"]
    m = d <= END
    out = {k: FA.stats(c[k][m]) for k in ("mktrf", "SMB", "VMG", "PMO")}
    out["start"], out["end"] = int(d[m][0]), int(d[m][-1])
    f = _ff5()
    us = {k: FA.stats(_on(f["date"], f[k], d[m])) for k in ("mkt", "smb", "hml")}
    out["us"] = us
    out["corr"] = np.corrcoef(np.c_[c["mktrf"][m], c["SMB"][m], c["VMG"][m], c["PMO"][m]].T)
    out["cum"] = {k: FA.cumulative(c[k][m]) for k in ("SMB", "VMG", "PMO")}
    out["date"] = d[m]
    return _json(out)


def compute_construct() -> dict:
    rng = np.random.default_rng(24)
    n = 40
    size = np.exp(rng.normal(0, 1.4, n))
    bm = np.exp(rng.normal(-0.4, 0.6, n))
    nyse = rng.random(n) < 0.45
    ret = 0.01 + 0.004 * np.log(bm) - 0.002 * np.log(size) + rng.normal(0, 0.05, n)
    t = FA.two_by_three(size, bm, nyse, ret, size)
    return _json({"size": size, "bm": bm, "nyse": nyse, "ret": ret, **t})


# ---------------------------------------------------------------------------
# The Track Record opens
# ---------------------------------------------------------------------------
COSTS = {"MKT": 0.0005, "SMB": 0.01, "HML": 0.01, "UMD": 0.03, "RMW": 0.01, "CMA": 0.01, "BAB": 0.015,
         "QMJ": 0.01, "TSMOM": 0.01, "VALMOM": 0.015}  # the House's placeholder cost model, per year, until Part 26
RULE = {"definition": "as published: Fama-French (2015) 2x3 factors and UMD (Ken French library); BAB, QMJ, TSMOM "
                      "and the 50/50 value-momentum mix of VAL and MOM (AQR data sets); no parameters chosen here",
        "research": "first month available to 2020-12", "holdout": "2021-01 to 2025-12"}


def _classic():
    f = _ff5()
    md, mom = _mom()
    bab = data.aqr("Betting-Against-Beta-Equity-Factors-Monthly", "BAB Factors", THROUGH)
    qmj = data.aqr("Quality-Minus-Junk-Factors-Monthly", "QMJ Factors", THROUGH)
    ts = data.aqr("Time-Series-Momentum-Factors-Monthly", "TSMOM Factors", THROUGH)
    vme = data.aqr("Value-and-Momentum-Everywhere-Factors-Monthly", "VME Factors", THROUGH)
    vm = 0.5 * vme["values"][:, vme["columns"].index("VAL")] + 0.5 * vme["values"][:, vme["columns"].index("MOM")]
    return {"MKT": (f["date"], f["mkt"]), "SMB": (f["date"], f["smb"]), "HML": (f["date"], f["hml"]),
            "UMD": (md, mom), "RMW": (f["date"], f["rmw"]), "CMA": (f["date"], f["cma"]),
            "BAB": (bab["date"], bab["values"][:, bab["columns"].index("USA")]),
            "QMJ": (qmj["date"], qmj["values"][:, qmj["columns"].index("USA")]),
            "TSMOM": (ts["date"], ts["values"][:, 0]), "VALMOM": (vme["date"], vm)}


def compute_envelope() -> dict:
    code = inspect.getsource(_classic) + json.dumps(RULE, sort_keys=True)
    rows = {}
    for k, (d, x) in _classic().items():
        ok = np.isfinite(x)
        d, x = np.asarray(d)[ok], np.asarray(x)[ok]
        strat = f"classic_{k.lower()}_part24"
        pit.register(strat, code, dict(RULE, factor=k, cost_per_year=COSTS[k]), trials=1)
        stamp = d * 100 + 28
        hd, hx = pit.open_envelope(strat, f"factors/{k.lower()}_monthly", stamp, x)
        res = x[d <= END]
        hx = hx[hd <= 20251231]
        row = track.record(strat, 24, res, hx, COSTS[k], note=RULE["definition"])
        rows[k] = dict(row, research_start=int(d[0]), holdout_months=int(len(hx)),
                       holdout_cum=FA.cumulative(hx), holdout_dates=(hd[hd <= 20251231] // 100))
    return _json({"rows": rows, "trials": pit.trials_so_far(), "costs": COSTS})


def compute_momentum_decomposition() -> dict:
    """The research chapter: where momentum profits come from (Lo and MacKinlay 1990; Jegadeesh and Titman 1993;
    Conrad and Kaul 1998; Lewellen 2002).  The weighted relative-strength strategy w_i = (x_i - xbar)/N, x the formation
    return, earns pi = sum_i w_i r_i; in sample moments, exactly,
    E[pi] = (N - 1)/N^2 sum_i Cov(x_i, r_i)  -  1/N^2 sum_{i != j} Cov(x_j, r_i)  +  1/N sum_i (mu_x,i - mu_x)(mu_i - mu):
    own persistence, minus lead-lag across assets, plus the dispersion of means.  On Ken French's 49 industries,
    monthly 1927-2020, for a one-month and a twelve-month (skip one) formation, with a block-bootstrap standard error;
    and on a simulated factor model where the parts are known."""
    d = data.ken_french_industries(49, through="2020-12")
    R = np.asarray(d["returns"], float)          # already decimal
    ok = ~np.isnan(R).any(0)                      # the 40 industries with a full history from July 1926
    R = R[:, ok]
    T, N = R.shape

    def decompose(X, Y):
        # X: formation returns, Y: holding returns, aligned rows
        n = X.shape[1]
        w = (X - X.mean(1, keepdims=True)) / n
        pi = (w * Y).sum(1)
        mx, my = X.mean(0), Y.mean(0)
        Xc, Yc = X - mx, Y - my
        C = Xc.T @ Yc / len(X)                     # C[j, i] = Cov(x_j, r_i), sample (1/T)
        own = (n - 1) / n ** 2 * np.trace(C)
        cross = -(C.sum() - np.trace(C)) / n ** 2
        disp = float(np.mean((mx - mx.mean()) * (my - my.mean())))
        scale = float(1 / np.mean(0.5 * np.abs(w).sum(1)))   # to a $1-long, $1-short strategy
        return {"mean": float(pi.mean()), "own": float(own), "cross": float(cross), "disp": disp,
                "check": float(pi.mean() - (own + cross + disp)), "pi": pi, "scale": scale}

    out = {"N": int(N), "T": int(T), "first": int(d["date"][0]), "last": int(d["date"][-1]), "results": {}}
    rng = np.random.default_rng(2424)
    for name, k, skip in (("1-month", 1, 0), ("12-1", 12, 1)):
        X = np.stack([np.log1p(R[t - k - skip: t - skip]).sum(0) for t in range(k + skip, T)])
        Y = R[k + skip:]
        res = decompose(X, Y)
        # block bootstrap (blocks of 24 months) for the mean profit and each component
        bs = {"mean": [], "own": [], "cross": [], "disp": []}
        n_ = len(Y)
        for _ in range(400):
            starts = rng.integers(0, n_ - 24, n_ // 24 + 1)
            idx = np.concatenate([np.arange(s_, s_ + 24) for s_ in starts])[:n_]
            r_ = decompose(X[idx], Y[idx])
            for key in bs:
                bs[key].append(r_[key])
        res["se"] = {key: float(np.std(v)) for key, v in bs.items()}
        pi = res.pop("pi")
        res["annual_mean"] = float(12 * pi.mean() * res["scale"])
        res["sharpe"] = float(np.sqrt(12) * pi.mean() / pi.std())
        out["results"][name] = res
    # a simulated check: one factor with an AR(1) idiosyncratic part, so the own part is known to be positive and the
    # lead-lag part zero, plus a dispersion of means
    n, T2 = 30, 200000
    mu = np.linspace(-0.002, 0.004, n)
    f = rng.standard_normal(T2) * 0.04
    e = np.zeros((T2, n))
    phi = 0.1
    z = rng.standard_normal((T2, n)) * 0.05
    for t in range(1, T2):
        e[t] = phi * e[t - 1] + z[t]
    Rs = mu + f[:, None] + e
    sim = decompose(Rs[:-1], Rs[1:])
    sim.pop("pi")
    sim_theory = {"own": (n - 1) / n ** 2 * n * phi * 0.05 ** 2 / (1 - phi ** 2), "cross": 0.0,
                  "disp": float(np.mean((mu - mu.mean()) ** 2))}
    out["sim"] = {"estimate": sim, "theory": sim_theory, "phi": phi, "n": n, "T": T2}
    return _json(out)


ITEMS = {"momentum_decomposition": compute_momentum_decomposition, "race": compute_race, "tests": compute_tests, "sizevalue": compute_sizevalue, "momentum": compute_momentum,
         "crash": compute_crash, "profit": compute_profit, "lowrisk": compute_lowrisk,
         "everywhere": compute_everywhere, "valuedecade": compute_valuedecade, "timing": compute_timing,
         "china": compute_china, "construct": compute_construct, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
