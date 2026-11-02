"""Every number in Part 12 (The Volatility Surface), computed and cached in .cache/quant12/.

    python -m videos.quant.quant12.compute [items] [--force]

Items (seconds to a few minutes on a CPU; about 45 CPU-minutes in all):

* ``surface``    the Surface (10 December 2025): quotes, per-expiry SVI, an SSVI fit, Gatheral's g on each, and the
                 next day's quotes for the sticky-strike / sticky-delta test;
* ``localvol``   Dupire's local volatility from the SSVI fit, and the forward smile it implies (Monte Carlo);
* ``varswap``    the variance-swap strike from the 30-day strip against at-the-money vol; our VIX on the Surface
                 against DVOL;
* ``history``    weekly surfaces from Deribit trades, January 2024 to November 2025: SSVI fits, the 30-day variance
                 swap rate, and the realized variance that followed (the variance risk premium); the SVIX bound;
* ``history_ext`` the same, every Wednesday from 7 April 2021 to 26 November 2025, with each week's fit, its quotes,
                 DVOL at the same hour, the trailing and following realized variance and the risk-neutral moments;
* ``volmageddon`` the VIX around 5 February 2018 (FRED);
* ``vae``        a variational autoencoder over the weekly surfaces (an implied-vol grid), 2-d latent, five seeds;
* ``termskew``, ``dynamics``   the term structure and skew through time; stickiness, the skew-stickiness ratio, PCA;
* ``arbitrage``  Vogt's SVI and its negative butterfly; calendar crossings; Lee's moments on the Surface;
* ``svi_replay``, ``ssvi_replay``  the fits replayed from several starts; the jump-wings table; SSVI's bound;
* ``bbf``, ``dk_tree``  local against implied skew; a Derman-Kani implied tree on the Surface;
* ``gyongy``     Heston paths: E[v_T | S_T] against Dupire from Heston's own prices;
* ``lv_mc``      local-vol Monte Carlo on the Surface: repricing, convergence, forward smiles, the smile under a spot move;
* ``trunc``, ``replication``, ``vixcomp``  the strip truncated; variance swaps replicated on real BTC; the VIX recipe,
                 our index against DVOL, the VIX since 1990 and its term structure;
* ``vrp_pnl``, ``spx_vrp``, ``rn_moments``  the premium's P&L and a predictability regression; the S&P 500 since 1990;
                 risk-neutral skewness and kurtosis;
* ``vx_etp``     the VIX futures curve 2017-18 (Cboe), a short-term futures index and a -1x note rebuilt;
* ``gamma_toy``  dealer gamma in a simulated day (labelled simulated);
* ``neural_surface``, ``operator_net``  an arbitrage-penalised network on the Surface; one network for all weeks;
* ``envelope``   registers nothing (no strategy is tested); the counter.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, paths, pit, smile, surface, volsurface as V

CACHE = Cache("quant12")
load = CACHE.load

KGRID = np.linspace(-0.4, 0.4, 17)
TGRID = np.array([7, 14, 30, 60, 90, 180]) / 365


def _json(x):
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x


def _fit_day(q):
    w = q["iv"] ** 2 * q["T"]
    ok = (np.abs(q["k"]) < 0.6) & (q["T"] > 2 / 365)
    fit = V.fit_ssvi(q["k"][ok], q["T"][ok], w[ok], weights=q["vega"][ok])
    return fit, ok


def _ssvi_iv(fit, k, T):
    th = V.theta_at(fit, T)
    return np.sqrt(V.ssvi_w(k, th, fit["rho"], fit["eta"], fit["gamma"]) / T)


# ---------------------------------------------------------------------------
def compute_surface() -> dict:
    q = surface.build(surface.DAYS[0])
    q1 = surface.build(surface.DAYS[1])
    fit, ok = _fit_day(q)
    model_iv = _ssvi_iv(fit, q["k"], q["T"])
    rmse_ssvi = surface.vega_rmse(model_iv[ok], q, ok)
    per = []
    for e in q["expiries"]:
        m = np.array([x == e["expiry"] for x in q["expiry"]])
        if m.sum() < 6:
            continue
        T = e["T"]
        p = smile.fit_svi(q["k"][m], q["iv"][m] ** 2 * T, weights=q["vega"][m])
        kk = np.linspace(-1.0, 1.0, 201)
        f = lambda k, t, p=p: smile.svi_total_variance(k, p["a"], p["b"], p["rho"], p["m"], p["s"])  # noqa: E731
        w, dw, d2w, _ = V.numeric_derivs(f, kk, T)
        per.append({"expiry": e["expiry"], "T": T, "n": int(m.sum()), "svi": p, "g_min": float(V.g_function(kk, w, dw, d2w).min()),
                    "k": q["k"][m], "iv": q["iv"][m], "F": e["F"]})
    # sticky strike vs sticky delta: predict day 2's vols from day 1's smile, holding strike or moneyness fixed
    errs = {"sticky strike": [], "sticky moneyness": []}
    S0, S1 = q["S"], q1["S"]
    for i in range(len(q1["k"])):
        T1 = q1["T"][i]
        K = q1["K"][i]
        F1 = q1["F"][i]
        if T1 < 5 / 365:
            continue
        # day-1 forward of the same horizon, approximately: scale by spot
        F0 = F1 * S0 / S1
        errs["sticky strike"].append(float(_ssvi_iv(fit, np.log(K / F0), T1 + 1 / 365)) - q1["iv"][i])
        errs["sticky moneyness"].append(float(_ssvi_iv(fit, np.log(K / F1), T1 + 1 / 365)) - q1["iv"][i])
    rm = {k: float(np.sqrt(np.mean(np.square(v))) * 100) for k, v in errs.items()}
    gk = np.linspace(-1, 1, 201)
    g_ssvi = [float(V.g_function(gk, *V.numeric_derivs(lambda k, t, th=th: V.ssvi_w(k, th, fit["rho"], fit["eta"], fit["gamma"]),
                                                         gk, 0.5)[:3]).min()) for th in fit["theta"]]
    return _json({"S": q["S"], "S_next": S1, "ssvi": fit, "rmse_ssvi": rmse_ssvi, "per": per, "n_quotes": int(len(q["k"])),
                  "sticky_rmse": rm, "g_ssvi_min": float(min(g_ssvi)), "K": q["K"], "T": q["T"], "k": q["k"], "iv": q["iv"],
                  "grid_k": KGRID, "grid_T": TGRID,
                  "grid_iv": np.array([[float(_ssvi_iv(fit, k, T)) for k in KGRID] for T in TGRID])})


def compute_localvol() -> dict:
    s = load("surface")
    fit = s["ssvi"]
    f = lambda k, T: V.ssvi_surface_w(fit, k, T)  # noqa: E731
    ks = np.linspace(-0.4, 0.4, 41)
    Ts = np.array([7, 14, 30, 60, 90, 180]) / 365
    lv = np.zeros((len(Ts), len(ks)))
    for i, T in enumerate(Ts):
        w, dw, d2w, dT = V.numeric_derivs(f, ks, T, h=2e-3, hT=2e-3)
        lv[i] = np.sqrt(np.maximum(V.dupire_local_var(ks, w, dw, d2w, dT), 1e-6))
    # forward smile under local vol: Monte Carlo of dS/S = sigma_loc(log S/F, t) dW, a 30-day option starting in 60 days
    # (the House's simulator, shared with Part 13's comparison of models)
    steps1, steps2 = 60, 30
    X = V.local_vol_paths(fit, steps1 + steps2, 40000, seed=7)
    x, x_start = X[-1], X[steps1]
    Rk = np.linspace(-0.25, 0.25, 11)
    ret = np.exp(x - x_start)
    T2 = steps2 / 365
    fwd_iv = []
    for k in Rk:  # out-of-the-money options, as quoted
        cp = 1 if k >= 0 else -1
        c = np.mean(np.maximum(cp * (ret - np.exp(k)), 0))
        fwd_iv.append(float(bs.implied_vol(c, 1.0, np.exp(k), T2, 0.0, 0.0, cp)))
    today_iv = [float(_ssvi_iv(fit, k, T2)) for k in Rk]
    return _json({"k": ks, "T": Ts, "lv": lv, "fwd_k": Rk, "fwd_iv": fwd_iv, "spot_iv_30d": today_iv,
                  "fwd_skew": float(fwd_iv[3] - fwd_iv[7]), "spot_skew": float(today_iv[3] - today_iv[7])})


def compute_varswap() -> dict:
    s = load("surface")
    fit = s["ssvi"]
    S = s["S"]
    out = {}
    T = 30 / 365
    F = S  # the 30-day forward, close to spot on this day (Part 9's basis is a few percent a year)
    K = np.linspace(0.3 * F, 2.5 * F, 2201)
    iv = _ssvi_iv(fit, np.log(K / F), T)
    otm = np.where(K < F, bs.price(F, K, T, iv, cp=-1), bs.price(F, K, T, iv, cp=1))
    kvar = V.var_swap_strike(K, otm, F, T)
    atm = float(_ssvi_iv(fit, 0.0, T))
    # the VIX recipe on strikes like Deribit's (every 1,000 or 2,000 dollars), interpolated to 30 days
    Kd = np.arange(round(0.5 * F, -3), round(1.6 * F, -3) + 1, 2000.0)
    vixs = []
    for TT in (21 / 365, 42 / 365):
        ivd = _ssvi_iv(fit, np.log(Kd / F), TT)
        vixs.append((TT, V.vix(Kd, bs.price(F, Kd, TT, ivd, cp=1), bs.price(F, Kd, TT, ivd, cp=-1), F, TT)))
    (T1, v1), (T2, v2) = vixs
    w30 = ((T2 - T) / (T2 - T1)) * T1 * v1 ** 2 + ((T - T1) / (T2 - T1)) * T2 * v2 ** 2
    our_vix = float(np.sqrt(w30 / T))
    dv = data.deribit_dvol("2025-12", "2025-12")
    ref = datetime(2025, 12, 10, 8, tzinfo=timezone.utc).timestamp()
    dvol = float(dv["close"][np.argmin(np.abs(np.asarray(dv["time"]) - ref))]) / 100
    weights = 1 / K ** 2
    out.update({"K": K, "weights": weights / weights.max(), "otm": otm, "kvar": float(np.sqrt(kvar)), "atm": atm,
                "our_vix": our_vix, "dvol": dvol, "F": F})
    return _json(out)


def _realized_after(ts, days=30):
    kl = data.binance_klines("BTCUSDT", "1h", "2024-01", "2025-12")
    t = np.asarray(kl["time"]) + 3600
    c = np.asarray(kl["close"])
    i = int(np.searchsorted(t, ts))
    j = i + days * 24
    if j >= len(c):
        return np.nan
    r = np.diff(np.log(c[i:j + 1]))
    return float(np.sum(r * r) * 365 / days)


def compute_history() -> dict:
    d = date(2024, 1, 3)
    rows = []
    while d <= date(2025, 11, 26):
        try:
            q = surface.build(d.isoformat())
            fit, ok = _fit_day(q)
            F = q["S"]
            T = 30 / 365
            K = np.linspace(0.3 * F, 2.5 * F, 1101)
            iv = _ssvi_iv(fit, np.log(K / F), T)
            otm = np.where(K < F, bs.price(F, K, T, iv, cp=-1), bs.price(F, K, T, iv, cp=1))
            kvar = V.var_swap_strike(K, otm, F, T)
            ref = datetime(d.year, d.month, d.day, 8, tzinfo=timezone.utc).timestamp()
            rv = _realized_after(ref)
            grid = np.array([[float(_ssvi_iv(fit, k, T_)) for k in KGRID] for T_ in TGRID])
            # Martin's SVIX: the lower bound on the expected return over 30 days, (risk-neutral variance of R)/R_f
            Kq = np.linspace(0.2 * F, 3.0 * F, 2801)
            ivq = _ssvi_iv(fit, np.log(Kq / F), T)
            otmq = np.where(Kq < F, bs.price(F, Kq, T, ivq, cp=-1), bs.price(F, Kq, T, ivq, cp=1))
            svix2 = float(2 / (T * F ** 2) * np.trapezoid(otmq, Kq))
            rows.append({"day": d.isoformat(), "S": F, "kvar": kvar, "rv": rv, "atm": float(_ssvi_iv(fit, 0.0, T)),
                         "skew": float(_ssvi_iv(fit, -0.1, T) - _ssvi_iv(fit, 0.1, T)), "grid": grid, "rmse": fit["rmse"],
                         "svix2": svix2, "n": int(ok.sum())})
        except Exception as e:  # a day without enough quotes is skipped, and said so
            rows.append({"day": d.isoformat(), "error": str(e)[:200]})
        d += timedelta(days=7)
    good = [r for r in rows if "kvar" in r]
    kv = np.array([r["kvar"] for r in good])
    rv = np.array([r["rv"] for r in good])
    m = np.isfinite(rv)
    vrp = kv[m] - rv[m]
    # weekly observations of 30-day windows overlap by about four: Newey-West with 4 lags
    mean = float(vrp.mean())
    dc = vrp - mean
    v = dc @ dc / len(dc)
    for L in range(1, 5):
        v += 2 * (1 - L / 5) * (dc[L:] @ dc[:-L]) / len(dc)
    t_nw = float(mean / np.sqrt(v / len(dc)))
    return _json({"rows": good, "skipped": [r["day"] for r in rows if "error" in r], "n": len(good),
                  "vrp_mean": mean, "vrp_t": t_nw, "share_positive": float((vrp > 0).mean()),
                  "kvar_vol_mean": float(np.sqrt(kv[m]).mean()), "rv_vol_mean": float(np.sqrt(rv[m]).mean()),
                  "svix_bound_mean": float(np.mean([r["svix2"] for r in good]) ), "grid_k": KGRID, "grid_T": TGRID})


def compute_volmageddon() -> dict:
    v = data.fred("VIXCLS", "2017-06-01", "2018-06-30")
    dd, x = np.asarray(v["date"]), np.asarray(v["value"])
    ok = np.isfinite(x)
    i = int(np.where(dd == 20180205)[0][0])
    return _json({"date": dd[ok], "vix": x[ok], "before": float(x[i - 1]), "after": float(x[i]),
                  "jump": float(x[i] / x[i - 1] - 1), "min_2017": float(np.nanmin(x[(dd >= 20170601) & (dd < 20180101)]))})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": {}}




# ===========================================================================
# The expansion (November 2026): the weekly history from April 2021, and every new chapter's numbers
# ===========================================================================
WEEK0, WEEK1 = date(2021, 4, 7), date(2025, 11, 26)
T30 = 30 / 365
_KL = {}


def _btc_hourly():
    if not _KL:
        kl = data.binance_klines("BTCUSDT", "1h", "2021-03", "2025-12")
        _KL["t"] = np.asarray(kl["time"]) + 3600  # candle close times
        _KL["c"] = np.asarray(kl["close"])
    return _KL["t"], _KL["c"]


def _ref(day: str) -> float:
    d = date.fromisoformat(day)
    return datetime(d.year, d.month, d.day, 8, tzinfo=timezone.utc).timestamp()


def _hourly_path(day: str, days=30, before=False):
    t, c = _btc_hourly()
    i = int(np.searchsorted(t, _ref(day)))
    a, b = (i - days * 24, i) if before else (i, i + days * 24)
    if a < 0 or b >= len(c):
        return None
    return c[a:b + 1]


def _strip(fit, F, T, lo=0.2, hi=3.0, n=2801):
    K = np.linspace(lo * F, hi * F, n)
    iv = _ssvi_iv(fit, np.log(K / F), T)
    return K, np.where(K < F, bs.price(F, K, T, iv, cp=-1), bs.price(F, K, T, iv, cp=1))


def compute_history_ext() -> dict:
    """Every Wednesday, 7 April 2021 to 26 November 2025: the surface from that morning's Deribit trades, its SSVI fit,
    the 30-day strip's variance strike, moments and SVIX, DVOL at 08:00 UTC, and Bitcoin's realized variance over the
    30 days before and after (hourly)."""
    part = CACHE.partial("history_ext", {"v": 2, "start": WEEK0.isoformat(), "end": WEEK1.isoformat()})
    dv = data.deribit_dvol("2021-04", "2025-12")
    dvt, dvc = np.asarray(dv["time"]), np.asarray(dv["close"]) / 100
    d = WEEK0
    while d <= WEEK1:
        day = d.isoformat()
        if day not in part:
            try:
                q = surface.build(day)
                fit, ok = _fit_day(q)
                F = q["S"]
                K, otm = _strip(fit, F, T30)
                kvar = V.var_swap_strike(K, otm, F, T30)
                after, before = _hourly_path(day), _hourly_path(day, before=True)
                rv = float(np.sum(np.diff(np.log(after)) ** 2) / T30) if after is not None else None
                rvt = float(np.sum(np.diff(np.log(before)) ** 2) / T30) if before is not None else None
                ret = float(np.log(after[-1] / after[0])) if after is not None else None
                grid = np.array([[float(_ssvi_iv(fit, k, T_)) for k in KGRID] for T_ in TGRID])
                ref = _ref(day)
                j = int(np.argmin(np.abs(dvt - ref)))
                mom = V.rn_moments(K, otm, F, T30)
                kq, Tq, ivq, vq = (np.asarray(q[x])[ok] for x in ("k", "T", "iv", "vega"))
                part[day] = _json({"day": day, "S": F, "fit": {x: fit[x] for x in ("rho", "eta", "gamma", "theta", "T", "rmse")},
                             "kvar": kvar, "rv": rv, "rv_trail": rvt, "ret30": ret, "grid": grid,
                             "atm": float(_ssvi_iv(fit, 0.0, T30)),
                             "skew": float(_ssvi_iv(fit, -0.1, T30) - _ssvi_iv(fit, 0.1, T30)),
                             "svix2": float(2 / (T30 * F ** 2) * np.trapezoid(otm, K)),
                             "dvol": float(dvc[j]) if abs(dvt[j] - ref) < 7200 else None, "mom": mom, "n": int(ok.sum()),
                             "q": np.round(np.vstack([kq, Tq, ivq, vq]), 5)})
            except Exception as e:  # a day without enough quotes is skipped, and said so
                part[day] = {"day": day, "error": str(e)[:200]}
            print(f"  history_ext {day}: {'skipped' if 'error' in part[day] else part[day]['n']}", flush=True)
        d += timedelta(days=7)
    rows = [part[x] for x in sorted(part.done)]
    good = [r for r in rows if "error" not in r]
    return _json({"rows": good, "skipped": [r["day"] for r in rows if "error" in r], "n": len(good),
                  "grid_k": KGRID, "grid_T": TGRID})


def _weeks():
    return load("history_ext")["rows"]


def _nw_t(x, lags=4):
    x = np.asarray(x, float)
    dc = x - x.mean()
    v = dc @ dc / len(dc)
    for L in range(1, lags + 1):
        v += 2 * (1 - L / (lags + 1)) * (dc[L:] @ dc[:-L]) / len(dc)
    return float(x.mean() / np.sqrt(v / len(dc)))


def _nw_reg(x, y, lags=4):
    """OLS of y on (1, x) with Newey-West standard errors: slope, its t, R^2."""
    X = np.column_stack([np.ones_like(x), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    res = y - X @ b
    XtX = np.linalg.inv(X.T @ X)
    u = X * res[:, None]
    S = u.T @ u
    for L in range(1, lags + 1):
        G = u[L:].T @ u[:-L]
        S += (1 - L / (lags + 1)) * (G + G.T)
    cov = XtX @ S @ XtX
    return {"slope": float(b[1]), "t": float(b[1] / np.sqrt(cov[1, 1])), "r2": float(1 - res.var() / y.var()),
            "n": int(len(y))}


def _year(day):
    d = date.fromisoformat(day)
    return d.year + (d.timetuple().tm_yday - 1) / 365


# ---------------------------------------------------------------------------
def _gram_charlier(g1, g2, s, ks):
    """Implied vols of a Gram-Charlier density for the standardized log return (skewness g1, excess kurtosis g2,
    total vol s), priced by quadrature and inverted, with the first-order Backus-Foresi-Wu line."""
    x = np.linspace(-9, 9, 6001)
    ph = np.exp(-x * x / 2) / np.sqrt(2 * np.pi)
    q = ph * (1 + g1 / 6 * (x ** 3 - 3 * x) + g2 / 24 * (x ** 4 - 6 * x * x + 3))
    q = np.maximum(q, 0)
    q /= np.trapezoid(q, x)
    mu = -np.log(np.trapezoid(np.exp(s * x) * q, x))
    ST = np.exp(mu + s * x)
    iv, bfw = [], []
    for k in ks:
        K = np.exp(k)
        cp = 1 if k >= 0 else -1
        pr = np.trapezoid(np.maximum(cp * (ST - K), 0) * q, x)
        iv.append(float(bs.implied_vol(pr, 1.0, K, 1.0, 0.0, 0.0, cp)))
        d = -k / s
        bfw.append(float(s * (1 - g1 / 6 * d + g2 / 24 * (d * d - 1))))
    return np.array(iv), np.array(bfw), x, q


def compute_termskew() -> dict:
    rows = _weeks()
    G = np.array([r["grid"] for r in rows])  # (weeks, 6 maturities, 17 strikes)
    j0 = len(KGRID) // 2
    atm = G[:, :, j0]
    skew = np.array([r["skew"] for r in rows])
    S = np.array([r["S"] for r in rows])
    yrs = np.array([r["day"][:4] for r in rows])
    by_year = {y: {"call_skew": float((skew[yrs == y] < 0).mean()), "atm30": float(atm[yrs == y, 2].mean()),
                   "n": int((yrs == y).sum())} for y in sorted(set(yrs))}
    # the Gram-Charlier smiles: a 30-day option at 50% vol
    s = 0.5 * np.sqrt(T30)
    ks = np.linspace(-0.3, 0.3, 25)
    gc = {"k": ks, "s": s, "g1": np.linspace(-1.0, 1.0, 9), "g2": np.linspace(0.0, 2.0, 5)}
    gc["iv_g1"], gc["bfw_g1"], gc["dens_g1"] = [], [], []
    for g1 in gc["g1"]:
        iv, bf, x, q = _gram_charlier(g1, 0.0, s, ks)
        gc["iv_g1"].append(iv / np.sqrt(T30))
        gc["bfw_g1"].append(bf / np.sqrt(T30))
        gc["dens_g1"].append(q[::50])
    gc["iv_g2"], gc["dens_g2"] = [], []
    for g2 in gc["g2"]:
        iv, bf, x, q = _gram_charlier(0.0, g2, s, ks)
        gc["iv_g2"].append(iv / np.sqrt(T30))
        gc["dens_g2"].append(q[::50])
    gc["x"] = x[::50]
    return _json({"days": [r["day"] for r in rows], "t": [_year(r["day"]) for r in rows], "atm": atm, "skew": skew,
                  "mean_atm": atm.mean(0), "inv_7_180": float((atm[:, 0] > atm[:, 5]).mean()),
                  "inv_30_90": float((atm[:, 2] > atm[:, 4]).mean()), "call_skew": float((skew < 0).mean()),
                  "mean_skew": float(skew.mean()),
                  "corr_skew_ret": float(np.corrcoef(skew[1:], np.diff(np.log(S)))[0, 1]), "by_year": by_year,
                  "n": len(rows), "gc": gc, "tenors": TGRID * 365})


def compute_dynamics() -> dict:
    rows = _weeks()
    s = load("surface")
    G = np.array([r["grid"] for r in rows])
    S = np.array([r["S"] for r in rows])
    kg = KGRID
    j0 = len(kg) // 2
    inner = np.abs(kg) <= 0.2
    e_m, e_s = [], []
    for i in range(len(rows) - 1):
        g0, g1 = G[i, 2], G[i + 1, 2]
        sh = np.log(S[i + 1] / S[i])
        pred_strike = np.interp(kg + sh, kg, g0)  # a fixed strike K: tomorrow's k is today's k minus the move
        e_m.append(np.sqrt(np.mean((g0[inner] - g1[inner]) ** 2)))
        e_s.append(np.sqrt(np.mean((pred_strike[inner] - g1[inner]) ** 2)))
    e_m, e_s = np.array(e_m) * 100, np.array(e_s) * 100
    sk = (G[:, 2, j0 + 1] - G[:, 2, j0 - 1]) / (kg[j0 + 1] - kg[j0 - 1])  # d sigma / dk at the money, 30 days
    ssr = V.skew_stickiness(np.diff(np.log(S)), np.diff(G[:, 2, j0]), sk[:-1])
    X = np.diff(np.log(G.reshape(len(G), -1)), axis=0)
    pca = V.surface_pca(X)
    comp = pca["components"][:3].reshape(3, len(TGRID), len(kg))
    sd = pca["scores"][:, :3].std(0)
    # quoting on the Surface: the 30-day 25-delta strikes and the risk reversal and butterfly
    fit = s["ssvi"]
    a = float(_ssvi_iv(fit, 0.0, T30))
    w = a * a * T30
    k25c = 0.674 * np.sqrt(w) + w / 2
    k25p = -0.674 * np.sqrt(w) + w / 2
    for _ in range(20):  # solve N(d1) = 0.25 and N(d1) = 0.75 with the smile's own vols
        wc = float(_ssvi_iv(fit, k25c, T30)) ** 2 * T30
        wp = float(_ssvi_iv(fit, k25p, T30)) ** 2 * T30
        k25c = 0.674 * np.sqrt(wc) + wc / 2
        k25p = -0.674 * np.sqrt(wp) + wp / 2
    sc, sp = float(_ssvi_iv(fit, k25c, T30)), float(_ssvi_iv(fit, k25p, T30))
    skew30 = float((_ssvi_iv(fit, 0.01, T30) - _ssvi_iv(fit, -0.01, T30)) / 0.02)
    return _json({"sticky_m": e_m, "sticky_s": e_s, "sticky_m_mean": float(e_m.mean()), "sticky_s_mean": float(e_s.mean()),
                  "strike_better": float((e_s < e_m).mean()), "n_pairs": len(e_m), "ssr": ssr,
                  "explained": pca["explained"][:6], "comp": comp, "score_sd": sd,
                  "pc1_by_T": comp[0].mean(1), "pc3_30d": comp[2, 2], "days": [r["day"] for r in rows],
                  "atm30": a, "k25c": k25c, "k25p": k25p, "s25c": sc, "s25p": sp, "rr25": sc - sp,
                  "bf25": 0.5 * (sc + sp) - a, "skew30": skew30})


def compute_arbitrage() -> dict:
    from explainer.quant.house import arbitrage as A

    # Vogt's smile (Gatheral and Jacquier 2014, Example 3.1): raw SVI at T = 1
    a, b, rho, m, sg = -0.0410, 0.1331, 0.3060, 0.3586, 0.4153
    kk = np.linspace(-1.5, 1.5, 3001)
    f = lambda kq, t: smile.svi_total_variance(kq, a, b, rho, m, sg)  # noqa: E731
    w, dw, d2w, _ = V.numeric_derivs(f, kk, 1.0)
    g = V.g_function(kk, w, dw, d2w)
    dm = -kk / np.sqrt(w) - np.sqrt(w) / 2
    dens = g / np.sqrt(2 * np.pi * w) * np.exp(-dm ** 2 / 2) / np.exp(kk)  # in strike, F = 1: q(K) dK
    neg = kk[g < 0]
    # a butterfly around the worst strike: three calls K - h, K, K + h (F = 1, T = 1)
    K2 = float(np.exp(kk[np.argmin(g)]))
    C = lambda K: float(bs.price(1.0, K, 1.0, np.sqrt(f(np.log(K), 1.0)), cp=1))  # noqa: E731
    flies = []
    for h in (0.05, 0.1, 0.2, 0.3, 0.4):
        flies.append((h, C(K2 - h) - 2 * C(K2) + C(K2 + h)))
    hb, fly = min(flies, key=lambda x: x[1])
    # the Surface: Lee's wings per expiry, calendar crossings between consecutive SVI slices, Part 9's checker
    s = load("surface")
    per = s["per"]
    lee = []
    for p in per:
        q = p["svi"]
        bl, br = q["b"] * (1 - q["rho"]), q["b"] * (1 + q["rho"])
        lee.append({"expiry": p["expiry"], "days": p["T"] * 365, "beta_L": bl, "beta_R": br,
                    "p_R": float(V.lee_moment(br)), "q_L": float(V.lee_moment(bl))})
    kc = np.linspace(-1, 1, 401)
    cross = []
    for p0, p1 in zip(per, per[1:]):
        w0 = smile.svi_total_variance(kc, *(p0["svi"][x] for x in ("a", "b", "rho", "m", "s")))
        w1 = smile.svi_total_variance(kc, *(p1["svi"][x] for x in ("a", "b", "rho", "m", "s")))
        bad = kc[w1 < w0]
        cross.append({"pair": [p0["expiry"], p1["expiry"]], "n_bad": int(len(bad)),
                      "k_range": [float(bad.min()), float(bad.max())] if len(bad) else None})
    viol = 0
    for p in per:
        F = p["F"]
        Kg = F * np.exp(np.linspace(-0.8, 0.8, 161))
        Cg = smile.call_prices(p["svi"], F, p["T"], Kg)
        chk = A.static_checks(Kg, Cg, F, tol=1e-9 * F)
        viol += sum(len(chk[x]) for x in ("monotone", "slope", "butterfly", "lower", "upper"))
    pair_plot = max(range(len(cross)), key=lambda i: cross[i]["n_bad"])
    p0, p1 = per[pair_plot], per[pair_plot + 1]
    return _json({"vogt": {"a": a, "b": b, "rho": rho, "m": m, "s": sg}, "k": kk[::10], "g": g[::10], "w": w[::10],
                  "dens": dens[::10], "g_min": float(g.min()), "k_min": float(kk[np.argmin(g)]),
                  "neg": [float(neg.min()), float(neg.max())], "neg_mass": float(np.trapezoid(np.minimum(dens * np.exp(kk), 0), kk)),
                  "fly": fly, "fly_h": hb, "fly_K": K2, "flies": flies, "lee": lee, "cross": cross,
                  "cross_pair": pair_plot, "cross_k": kc,
                  "cross_w0": smile.svi_total_variance(kc, *(p0["svi"][x] for x in ("a", "b", "rho", "m", "s"))),
                  "cross_w1": smile.svi_total_variance(kc, *(p1["svi"][x] for x in ("a", "b", "rho", "m", "s"))),
                  "violations": viol, "n_expiries": len(per)})


def _sub(n, m=40):
    """At most m indices out of n, always including the first and the last."""
    return sorted(set(np.linspace(0, n - 1, min(n, m)).round().astype(int).tolist()))


def compute_svi_replay() -> dict:
    from scipy import optimize

    s = load("surface")
    per = [p for p in s["per"] if p["expiry"] == "2026-01-30"][0]
    k, iv, T = np.asarray(per["k"]), np.asarray(per["iv"]), per["T"]
    w = iv ** 2 * T
    lo = [-w.max(), 1e-6, -0.999, -1.0, 1e-3]
    hi = [w.max() * 2, 2.0 / (1 + 0.999), 0.999, 1.0, 2.0]
    runs = []
    for seed in range(6):
        g = np.random.default_rng(seed)
        p0 = [max(w.min() * 0.5, 1e-4) * g.uniform(0.2, 2), g.uniform(0.02, 0.3), g.uniform(-0.8, 0.8),
              g.uniform(-0.3, 0.3), g.uniform(0.05, 0.6)]
        path, rm = [], []

        def resid(p):
            path.append(np.array(p, float))
            rm.append(float(np.sqrt(np.mean((np.sqrt(np.maximum(smile.svi_total_variance(k, *p), 1e-12) / T) - iv) ** 2)) * 100))
            return smile.svi_total_variance(k, *p) - w
        r = optimize.least_squares(resid, p0, bounds=(lo, hi), max_nfev=4000)
        keep = _sub(len(path))
        runs.append({"p0": p0, "p": r.x, "nfev": int(r.nfev), "rmse": rm, "path": np.array(path)[keep], "path_i": keep,
                     "first": rm[0], "final": rm[-1]})
    best = min(runs, key=lambda x: x["final"])
    table = []
    for p in s["per"]:
        jw = V.svi_jw(p["svi"], p["T"])
        table.append({"expiry": p["expiry"], "days": p["T"] * 365, "n": p["n"], **{x: jw[x] for x in jw},
                      "g_min": p["g_min"], "rmse": float(np.sqrt(np.mean((smile.svi_iv(p["svi"], np.asarray(p["k"]), p["T"])
                                                                            - np.asarray(p["iv"])) ** 2)) * 100)})
    bp = dict(zip(("a", "b", "rho", "m", "s"), best["p"]))
    return _json({"k": k, "iv": iv, "T": T, "expiry": per["expiry"], "runs": runs, "best": bp,
                  "best_rmse": best["final"], "jw_best": V.svi_jw(bp, T), "table": table,
                  "nfev": [r_["nfev"] for r_ in runs], "first": [r_["first"] for r_ in runs],
                  "final": [r_["final"] for r_ in runs], "spread": float(np.ptp([r_["p"] for r_ in runs], axis=0).max())})


def compute_ssvi_replay() -> dict:
    s = load("surface")
    q = surface.build(surface.DAYS[0])
    k, T, iv, vg = (np.asarray(q[x]) for x in ("k", "T", "iv", "vega"))
    ok = (np.abs(k) < 0.6) & (T > 2 / 365)
    k, T, iv, vg = k[ok], T[ok], iv[ok], vg[ok]
    w = iv ** 2 * T
    runs = []
    base = V.fit_ssvi_path(k, T, w, weights=vg)
    x_default = None
    for seed in range(5):
        if seed == 0:
            r = base
        else:
            g = np.random.default_rng(seed)
            nT = len(np.unique(T))
            x0 = np.concatenate([[g.uniform(-1.5, 1.0), g.uniform(-1.0, 1.0), g.uniform(-2, 2)],
                                 np.log(np.full(nT, g.uniform(0.002, 0.03)))])
            r = V.fit_ssvi_path(k, T, w, weights=vg, x0=x0)
        Ts = r["T"]

        def vrmse(pv):
            th = pv[3:][np.searchsorted(Ts, T)]
            m = np.sqrt(V.ssvi_w(k, th, pv[0], pv[1], pv[2]) / T)
            return float(np.sqrt(np.sum(vg * (m - iv) ** 2) / np.sum(vg)) * 100)
        loss = [vrmse(pv) for pv in r["path"]]
        keep = _sub(len(loss), 30)
        runs.append({"loss": loss, "frames": r["path"][keep], "frames_i": keep, "final": loss[-1], "nfev": r["nfev"],
                     "rho": r["rho"], "eta": r["eta"], "gamma": r["gamma"]})
    fit = s["ssvi"]
    per_rmse = []
    for p in s["per"]:
        kp, ivp = np.asarray(p["k"]), np.asarray(p["iv"])
        m = np.abs(kp) < 0.6
        a = float(np.sqrt(np.mean((smile.svi_iv(p["svi"], kp[m], p["T"]) - ivp[m]) ** 2)) * 100)
        b_ = float(np.sqrt(np.mean((_ssvi_iv(fit, kp[m], p["T"]) - ivp[m]) ** 2)) * 100)
        per_rmse.append({"expiry": p["expiry"], "days": p["T"] * 365, "svi": a, "ssvi": b_})
    bound = V.ssvi_butterfly_bound(fit)
    th = np.asarray(fit["theta"])
    return _json({"runs": runs, "Ts": base["T"], "k": k, "T": T, "iv": iv, "fit": {x: fit[x] for x in ("rho", "eta", "gamma")},
                  "theta": th, "rmse": s["rmse_ssvi"], "bound": bound, "theta_min": float(th.min()),
                  "eta_rho": float(fit["eta"] * (1 + abs(fit["rho"]))), "per_rmse": per_rmse,
                  "n_par_ssvi": 3 + len(th), "n_par_svi": 5 * len(s["per"]), "g_min": s["g_ssvi_min"],
                  "finals": [r_["final"] for r_ in runs]})


def compute_bbf() -> dict:
    s = load("surface")
    lv = load("localvol")
    lk, LT, LL = np.asarray(lv["k"]), np.asarray(lv["T"]), np.asarray(lv["lv"])
    fit = s["ssvi"]
    j = int(np.argmin(np.abs(lk)))
    out = []
    for i, T_ in enumerate(LT):
        dl = (LL[i, j + 1] - LL[i, j - 1]) / (lk[j + 1] - lk[j - 1])
        di = float((_ssvi_iv(fit, 0.02, T_) - _ssvi_iv(fit, -0.02, T_)) / 0.04)
        out.append({"days": T_ * 365, "local": float(dl), "implied": di, "ratio": float(dl / di)})
    # the implied and local surfaces on one grid, for the 3D picture
    ks = np.linspace(-0.4, 0.4, 21)
    Ts = np.linspace(7, 180, 16) / 365
    f = lambda kq, T: V.ssvi_surface_w(fit, kq, T)  # noqa: E731
    imp = np.array([[float(_ssvi_iv(fit, kq, T)) for kq in ks] for T in Ts])
    loc = np.zeros_like(imp)
    for i, T in enumerate(Ts):
        w, dw, d2w, dT = V.numeric_derivs(f, ks, T, h=2e-3, hT=2e-3)
        loc[i] = np.sqrt(np.maximum(V.dupire_local_var(ks, w, dw, d2w, dT), 1e-6))
    gk = np.linspace(-0.6, 0.6, 121)
    lab = {}
    for days in (7, 30, 90):
        T = days / 365
        w, dw, d2w, dT = V.numeric_derivs(f, gk, T, h=2e-3, hT=2e-3)
        g = V.g_function(gk, w, dw, d2w)
        lab[str(days)] = {"g_min": float(g.min()), "loc_atm": float(np.sqrt(V.dupire_local_var(0.0, *(x[60] for x in (w, dw, d2w, dT))))),
                          "imp_atm": float(_ssvi_iv(fit, 0.0, T))}
    return _json({"rows": out, "ratios": [r["ratio"] for r in out], "ks": ks, "Ts": Ts, "imp": imp, "loc": loc,
                  "lab": lab})


def compute_dk_tree() -> dict:
    from explainer.quant.house import trees

    fit = load("surface")["ssvi"]
    iv = lambda K, t: float(np.sqrt(V.ssvi_surface_w(fit, np.log(K), t) / t))  # noqa: E731
    T, N = 0.25, 40
    tr = trees.derman_kani(1.0, T, N, iv)
    kk = np.linspace(-0.3, 0.3, 13)
    pt = trees.tree_price(tr, np.exp(kk))
    ivt = np.array([bs.implied_vol(p, 1.0, np.exp(x), T, 0.0, 0.0, 1) for p, x in zip(pt, kk)])
    tgt = np.array([iv(np.exp(x), T) for x in kk])
    # node local vols against Dupire's at the same place, mid-tree
    lvf = V.local_vol_fn(fit)
    n_mid = N // 2
    S_mid = np.asarray(tr["nodes"][n_mid])
    lv_tree = np.asarray(tr["local_vol"][n_mid])
    x_mid = np.log(S_mid)  # node i of level n branches with local vol lv[n][i]
    lv_dup = np.array([float(lvf(np.array([x]), (n_mid + 0.5) * tr["dt"])[0]) for x in x_mid])
    m = np.abs(x_mid) < 0.25
    small = trees.derman_kani(1.0, T, 6, iv)  # a six-step tree to draw
    return _json({"nodes": tr["nodes"], "lv": tr["local_vol"], "p": tr["p"], "fixes": tr["fixes"], "N": N, "T": T,
                  "k": kk, "iv_tree": ivt, "iv_surface": tgt, "err_volpts": (ivt - tgt) * 100,
                  "max_err": float(np.max(np.abs(ivt - tgt)[np.abs(kk) <= 0.2]) * 100),
                  "x_mid": x_mid[m], "lv_tree_mid": lv_tree[m], "lv_dupire_mid": lv_dup[m],
                  "lv_gap": float(np.median(np.abs(lv_tree[m] - lv_dup[m])) * 100),
                  "small": {"nodes": small["nodes"], "p": small["p"], "lv": small["local_vol"]}})


HESTON = {"v0": 0.25, "kappa": 3.0, "theta": 0.30, "xi": 1.2, "rho": -0.3}


def compute_gyongy() -> dict:
    from explainer.quant.house import stochvol as SV

    p = HESTON
    T = 0.25
    cf = lambda u, t: SV.heston_cf(u, t, p["v0"], p["kappa"], p["theta"], p["xi"], p["rho"])  # noqa: E731
    ks = np.linspace(-0.5, 0.5, 21)

    def w_of(k, t):
        return SV.model_iv(cf, 1.0, np.exp(np.atleast_1d(k)), t) ** 2 * t
    h, hT = 0.02, 0.005
    dup = []
    for kq in ks:
        w0 = w_of(kq, T)[0]
        wp, wm = w_of(kq + h, T)[0], w_of(kq - h, T)[0]
        wt1, wt0 = w_of(kq, T + hT)[0], w_of(kq, T - hT)[0]
        lvar = V.dupire_local_var(kq, w0, (wp - wm) / (2 * h), (wp - 2 * w0 + wm) / h ** 2, (wt1 - wt0) / (2 * hT))
        dup.append(float(np.sqrt(max(lvar, 1e-8))))
    S, vs = SV.heston_qe(1.0, p["v0"], p["kappa"], p["theta"], p["xi"], p["rho"], T, 90, 100000, seed=1, return_v=True)
    x, v = np.log(S[-1]), vs[-1]
    cond = np.sqrt(V.conditional_variance(x, v, ks, width=0.025))
    g = np.random.default_rng(2)
    pick = g.choice(len(x), 1500, replace=False)
    fan = np.log(S[::3, :40]).T
    vfan = vs[::3, :40].T
    ok = np.isfinite(cond)
    return _json({"params": p, "T": T, "k": ks, "dupire": dup, "cond": cond, "gap": np.abs(np.array(dup) - cond),
                  "max_gap": float(np.nanmax(np.abs(np.array(dup)[ok] - cond[ok])) * 100),
                  "cloud_x": x[pick], "cloud_v": v[pick], "fan_x": fan, "fan_v": vfan, "n_paths": 100000, "steps": 90,
                  "implied": np.sqrt(w_of(ks, T) / T)})


def _mc_iv(x, T, ks):
    """Implied vols of out-of-the-money options on simulated log prices x (forward 1)."""
    S = np.exp(x)
    out = []
    for k in ks:
        cp = 1 if k >= 0 else -1
        c = np.mean(np.maximum(cp * (S - np.exp(k)), 0))
        out.append(float(bs.implied_vol(c, 1.0, np.exp(k), T, 0.0, 0.0, cp)))
    return np.array(out)


def compute_lv_mc() -> dict:
    """Local-volatility Monte Carlo on the Surface (40,000 paths, 120 days): repricing of the quotes, the convergence of
    one smile with the number of paths, forward 30-day smiles starting 0-90 days out, and the smile after a spot move
    (Berestycki-Busca-Florent's average of local vol along the line)."""
    s = load("surface")
    fit = s["ssvi"]
    X = V.local_vol_paths(fit, 120, 40000, seed=7)
    ks = np.linspace(-0.3, 0.3, 13)
    K_, T_, iv_, k_ = (np.asarray(s[x]) for x in ("K", "T", "iv", "k"))
    rep = []
    for e in s["per"]:
        days = int(round(e["T"] * 365))
        if days < 7 or days > 120:
            continue
        m = (np.abs(k_ - 0) < 0.6) & (np.abs(T_ - e["T"]) < 1e-9)
        xT = X[days]
        mc_q = _mc_iv(xT, days / 365, k_[m])
        ssvi_q = np.asarray(_ssvi_iv(fit, k_[m], e["T"]))
        ok = np.isfinite(mc_q)
        rep.append({"expiry": e["expiry"], "days": days, "k": k_[m], "quote": iv_[m], "mc": mc_q, "ssvi": ssvi_q,
                    "rmse_quote": float(np.sqrt(np.mean((mc_q[ok] - iv_[m][ok]) ** 2)) * 100),
                    "rmse_ssvi": float(np.sqrt(np.mean((mc_q[ok] - ssvi_q[ok]) ** 2)) * 100),
                    "smile_k": ks, "smile_mc": _mc_iv(xT, days / 365, ks),
                    "smile_ssvi": np.asarray(_ssvi_iv(fit, ks, days / 365))})
    conv = {}
    d51 = 51
    for n in (500, 2000, 8000, 40000):
        conv[str(n)] = _mc_iv(X[d51, :n], d51 / 365, ks)
    fwd = {}
    for start in (0, 15, 30, 60, 90):
        r = X[start + 30] - X[start]
        fwd[str(start)] = _mc_iv(r, T30, ks)
    i_m, i_p = int(np.argmin(np.abs(ks + 0.1))), int(np.argmin(np.abs(ks - 0.1)))
    skews = {k_s: float(v[i_m] - v[i_p]) for k_s, v in fwd.items()}
    # the smile after a spot move, under local vol (BBF: the harmonic mean of local vol between spot and strike at
    # mid-life) and under the two sticky rules
    lvf = V.local_vol_fn(fit)
    shifts = np.linspace(-0.08, 0.08, 9)
    kk = np.linspace(-0.3, 0.3, 25)  # strikes, as log(K/F0)
    tm = 15 / 365
    u = np.linspace(-1.0, 1.0, 801)
    lu = lvf(u, tm)

    def bbf(x0, xk):
        if abs(xk - x0) < 1e-6:
            return float(np.interp(x0, u, lu))
        g = np.linspace(x0, xk, 101)
        return float(1 / np.mean(1 / np.interp(g, u, lu)))
    today = np.array([bbf(0.0, x) for x in kk])
    move = {"lv": [], "strike": [], "moneyness": []}
    atm = {"lv": [], "strike": [], "moneyness": []}
    sm = np.asarray(_ssvi_iv(fit, kk, T30))
    for sh in shifts:
        lvs_ = np.array([bbf(sh, x) for x in kk])
        move["lv"].append(lvs_)
        move["strike"].append(sm)  # a fixed strike keeps its vol
        move["moneyness"].append(np.asarray(_ssvi_iv(fit, kk - sh, T30)))
        atm["lv"].append(bbf(sh, sh))
        atm["strike"].append(float(_ssvi_iv(fit, sh, T30)))
        atm["moneyness"].append(float(_ssvi_iv(fit, 0.0, T30)))
    sk_bbf = (today[kk.tolist().index(min(kk, key=lambda z: abs(z - 0.05)))] - today[kk.tolist().index(min(kk, key=lambda z: abs(z + 0.05)))]) / 0.1
    slope_lv = float(np.polyfit(shifts, atm["lv"], 1)[0])
    return _json({"rep": rep, "rmse_quote": [r["rmse_quote"] for r in rep], "rmse_ssvi": [r["rmse_ssvi"] for r in rep],
                  "conv": conv, "ks": ks, "conv_ssvi": np.asarray(_ssvi_iv(fit, ks, d51 / 365)), "fwd": fwd,
                  "fwd_skew": skews, "today30": np.asarray(_ssvi_iv(fit, ks, T30)),
                  "today_skew": float(_ssvi_iv(fit, -0.1, T30) - _ssvi_iv(fit, 0.1, T30)),
                  "shifts": shifts, "kk": kk, "move": move, "atm": atm, "bbf_today": today,
                  "R_lv": slope_lv / float(sk_bbf), "skew_bbf": float(sk_bbf), "slope_lv": slope_lv})


def compute_trunc() -> dict:
    s = load("surface")
    fit, F = s["ssvi"], s["S"]
    out = []
    for xw in (0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.65, 0.8, 1.0, 1.2):
        K = np.linspace(F * np.exp(-xw), F * np.exp(xw), 2001)
        iv = _ssvi_iv(fit, np.log(K / F), T30)
        otm = np.where(K < F, bs.price(F, K, T30, iv, cp=-1), bs.price(F, K, T30, iv, cp=1))
        out.append((xw, float(np.sqrt(V.var_swap_strike(K, otm, F, T30)))))
    full = load("varswap")["kvar"]
    x20 = [v for x, v in out if x == 0.2][0]
    # the jump term: 2(e^J - 1 - J) - J^2 for a single jump
    J = np.linspace(-0.4, 0.4, 81)
    return _json({"rows": out, "full": full, "share_beyond_20": float(1 - x20 ** 2 / full ** 2), "J": J,
                  "jump_gap": 2 * (np.exp(J) - 1 - J) - J ** 2})


def compute_replication() -> dict:
    """Variance swaps on real Bitcoin months: each week's 30-day strip bought at its fitted price, then the hourly
    (and daily) delta hedge along Binance's hourly BTCUSDT; and the strip restricted to a Deribit-like strike grid."""
    rows = [r for r in _weeks() if r["rv"] is not None]
    out = []
    for r in rows:
        fit, F = r["fit"], r["S"]
        path = _hourly_path(r["day"])
        K, otm = _strip(fit, F, T30, 0.3, 2.5, 1101)
        hr = V.strip_replication(K, otm, F, T30, path)
        dy = V.strip_replication(K, otm, F, T30, path[::24])
        # a listed grid: strikes every 2.5% of the forward (rounded to $1,000) within the 30-day quotes' range
        Kd = np.unique(np.round(F * np.exp(np.arange(-0.5, 0.5001, 0.025)) / 1000) * 1000)
        ivd = _ssvi_iv(fit, np.log(Kd / F), T30)
        otmd = np.where(Kd < F, bs.price(F, Kd, T30, ivd, cp=-1), bs.price(F, Kd, T30, ivd, cp=1))
        kd = V.var_swap_strike(Kd, otmd, F, T30)
        out.append({"day": r["day"], "kvar": hr["kvar"], "rv": hr["rv"], "rep_h": hr["replicated"], "err_h": hr["error"],
                    "rep_d": dy["replicated"], "rv_d": dy["rv"], "kvar_listed": kd})
    kv = np.array([o["kvar"] for o in out])
    rv = np.array([o["rv"] for o in out])
    eh = np.array([o["err_h"] for o in out])
    rd = np.array([o["rep_d"] for o in out])
    kl = np.array([o["kvar_listed"] for o in out])
    # the replayed week: the one whose hourly error is the median
    i = int(np.argsort(np.abs(eh))[len(eh) // 2])
    r = rows[i]
    path = _hourly_path(r["day"])
    F = r["S"]
    K, otm = _strip(r["fit"], F, T30, 0.3, 2.5, 1101)
    q = 2 / T30 * np.gradient(K) / K ** 2
    strip_val = np.array([float(np.sum(q * np.where(K < F, np.maximum(K - S_, 0), np.maximum(S_ - K, 0)))) for S_ in path])
    hedge_cum = np.concatenate([[0], np.cumsum(2 / T30 * (1 / path[:-1] - 1 / F) * np.diff(path))])
    rv_cum = np.concatenate([[0], np.cumsum(np.diff(np.log(path)) ** 2) / T30])
    conv = V.vol_swap_convexity(rv)
    return _json({"days": [o["day"] for o in out], "kvar": kv, "rv": rv, "err_h": eh, "rep_d": rd, "kvar_listed": kl,
                  "n": len(out), "corr_h": float(np.corrcoef(kv + eh + (rv - kv), rv)[0, 1]),
                  "err_h_mean": float(eh.mean()), "err_h_sd": float(eh.std()), "err_h_maxabs": float(np.abs(eh).max()),
                  "worst_day": out[int(np.argmax(np.abs(eh)))]["day"],
                  "daily_vs_hourly_sd": float(np.std(rd - rv)), "rv_mean": float(rv.mean()),
                  "listed_gap_volpts": float(np.mean(np.sqrt(kv) - np.sqrt(kl)) * 100),
                  "convexity": conv, "replay": {"day": r["day"], "S": path, "strip": strip_val, "hedge": hedge_cum,
                                                  "rv": rv_cum, "kvar": out[i]["kvar"], "F": F}})


def compute_vixcomp() -> dict:
    s = load("surface")
    fit = s["ssvi"]
    exps = {e["expiry"]: e for e in s["per"]}
    pair = []
    q0 = surface.build(surface.DAYS[0])
    for ex in ("2025-12-26", "2026-01-30"):
        e = exps[ex]
        F, T = e["F"], e["T"]
        m = np.array([x == ex for x in q0["expiry"]])
        Kq = np.unique(np.asarray(q0["K"])[m])
        Kq = Kq[(Kq > 0.4 * F) & (Kq < 2.0 * F)]
        iv = _ssvi_iv(fit, np.log(Kq / F), T)
        C, P = bs.price(F, Kq, T, iv, cp=1), bs.price(F, Kq, T, iv, cp=-1)
        sig = V.vix(Kq, C, P, F, T)
        o = np.argsort(Kq)
        Kq, C, P = Kq[o], C[o], P[o]
        i0 = int(np.searchsorted(Kq, F, side="right") - 1)
        Q = np.where(Kq < Kq[i0], P, C)
        Q[i0] = 0.5 * (P[i0] + C[i0])
        dK = np.gradient(Kq)
        contrib = 2 / T * dK / Kq ** 2 * Q
        pair.append({"expiry": ex, "T": T, "F": F, "K": Kq, "contrib": contrib, "K0": float(Kq[i0]), "sigma": sig,
                     "corr": float((F / Kq[i0] - 1) ** 2 / T), "n": int(len(Kq))})
    our = V.vix_30d(pair[0]["T"], pair[0]["sigma"], pair[1]["T"], pair[1]["sigma"])
    dvol = load("varswap")["dvol"]
    rows = [r for r in _weeks() if r["dvol"] is not None]
    ours = np.sqrt([r["kvar"] for r in rows])
    dv = np.array([r["dvol"] for r in rows])
    v = data.fred("VIXCLS", "1990-01-02", "2025-12-31")
    vd, vx = np.asarray(v["date"]), np.asarray(v["value"])
    v3 = data.fred("VXVCLS", "2007-12-04", "2025-12-31")
    d3, x3 = np.asarray(v3["date"]), np.asarray(v3["value"])
    ch = vx[1:] / vx[:-1] - 1
    top = np.argsort(ch)[-5:][::-1]
    common, ia, ib = np.intersect1d(vd, d3, return_indices=True)
    ratio = vx[ia] / x3[ib]
    snap = {str(d): float(ratio[common == d][0]) for d in (20180202, 20180205, 20200316, 20240805) if (common == d).any()}
    wk = np.arange(0, len(vd), 5)
    return _json({"pair": pair, "our_vix": our, "dvol": dvol, "days": [r["day"] for r in rows], "ours": ours, "dvol_w": dv,
                  "mean_ours": float(ours.mean()), "mean_dvol": float(dv.mean()), "corr": float(np.corrcoef(ours, dv)[0, 1]),
                  "gap_mean": float((ours - dv).mean() * 100), "gap_sd": float((ours - dv).std() * 100), "n_weeks": len(rows),
                  "vix_d": vd[wk], "vix_x": vx[wk], "vix_max": float(vx.max()), "vix_max_d": int(vd[np.argmax(vx)]),
                  "top": [(int(vd[i + 1]), float(vx[i]), float(vx[i + 1]), float(ch[i])) for i in top],
                  "ts_d": common[::5], "ts_ratio": ratio[::5], "contango": float((ratio < 1).mean()), "ts_snap": snap,
                  "ts_start": int(common[0])})


def compute_vrp_pnl() -> dict:
    rows = [r for r in _weeks() if r["rv"] is not None and r["rv_trail"] is not None]
    kv = np.array([r["kvar"] for r in rows])
    rv = np.array([r["rv"] for r in rows])
    pnl = kv - rv
    days = [r["day"] for r in rows]
    run_mean, run_t = [], []
    for i in range(len(pnl)):
        run_mean.append(float(pnl[:i + 1].mean()))
        run_t.append(_nw_t(pnl[:i + 1]) if i >= 10 else float("nan"))
    cum = np.cumsum(pnl)
    dd = cum - np.maximum.accumulate(cum)
    ret = np.array([r["ret30"] for r in rows])
    x = kv - np.array([r["rv_trail"] for r in rows])
    late = np.array([d >= "2024-01-01" for d in days])
    yrs = np.array([d[:4] for d in days])
    by_year = {y: {"implied": float(np.sqrt(kv[yrs == y]).mean()), "realized": float(np.sqrt(rv[yrs == y]).mean()),
                   "positive": float((pnl[yrs == y] > 0).mean()), "n": int((yrs == y).sum())} for y in sorted(set(yrs))}
    sk = float(((pnl - pnl.mean()) ** 3).mean() / pnl.std() ** 3)
    return _json({"days": days, "kvar": kv, "rv": rv, "pnl": pnl, "run_mean": run_mean, "run_t": run_t, "cum": cum,
                  "dd": dd, "max_dd": float(dd.min()), "n": len(rows), "mean": float(pnl.mean()), "t": _nw_t(pnl),
                  "share_pos": float((pnl > 0).mean()), "skew": sk, "worst": float(pnl.min()),
                  "worst_day": days[int(np.argmin(pnl))], "best": float(pnl.max()), "best_day": days[int(np.argmax(pnl))],
                  "implied_mean": float(np.sqrt(kv).mean()), "realized_mean": float(np.sqrt(rv).mean()),
                  "btz": _nw_reg(x, ret), "btz_late": _nw_reg(x[late], ret[late]), "by_year": by_year,
                  "t_late": _nw_t(pnl[late]), "share_late": float((pnl[late] > 0).mean())})


def compute_spx_vrp() -> dict:
    v = data.fred("VIXCLS", "1990-01-02", "2025-12-31")
    vix = dict(zip(np.asarray(v["date"]).tolist(), np.asarray(v["value"]).tolist()))
    g = data.yahoo_daily("^GSPC", "1990-01-01", "2025-11-30")
    d, c = np.asarray(g["date"]), np.asarray(g["close"])
    r = np.diff(np.log(c))
    vv, rr, dd = [], [], []
    for i in range(len(d) - 22):
        if d[i] in vix:
            rr.append(np.sum(r[i:i + 21] ** 2) * 252 / 21)
            vv.append(vix[d[i]] ** 2 / 1e4)
            dd.append(int(d[i]))
    vv, rr, dd = np.array(vv), np.array(rr), np.array(dd)
    prem = vv - rr
    mo = np.arange(0, len(dd), 21)
    return _json({"n": len(dd), "start": int(dd[0]), "end": int(dd[-1]), "vix_mean": float(np.sqrt(vv).mean()),
                  "rv_mean": float(np.sqrt(rr).mean()), "share_pos": float((prem > 0).mean()),
                  "worst": float(prem.min()), "worst_day": int(dd[np.argmin(prem)]), "t": _nw_t(prem[::21], lags=1),
                  "d": dd[mo], "vix": np.sqrt(vv[mo]), "rv": np.sqrt(rr[mo])})


def compute_rn_moments() -> dict:
    rows = [r for r in _weeks()]
    sk = np.array([r["mom"]["skew"] for r in rows])
    ku = np.array([r["mom"]["kurt"] for r in rows])
    va = np.array([r["mom"]["var"] for r in rows])
    ret = np.array([r["ret30"] if r["ret30"] is not None else np.nan for r in rows])
    ok = np.isfinite(ret)
    svix = np.array([r["svix2"] for r in rows])
    # the three strips on the Surface, 30 days: weights times option prices, for log variance, SVIX and skewness
    s = load("surface")
    F = s["S"]
    K, otm = _strip(s["ssvi"], F, T30, 0.4, 2.2, 721)
    x = np.log(K / F)
    strips = {"logvar": 2 / K ** 2 * otm, "svix": 2 / F ** 2 * otm * np.ones_like(K), "cubic": (6 * x - 3 * x * x) / K ** 2 * otm}
    strips = {k_: (v_ / np.abs(v_).max()).tolist() for k_, v_ in strips.items()}
    m0 = V.rn_moments(K, otm, F, T30)
    return _json({"days": [r["day"] for r in rows], "skew": sk, "kurt": ku, "var": va, "share_pos_skew": float((sk > 0).mean()),
                  "mean_skew": float(sk.mean()), "mean_kurt": float(ku.mean()),
                  "corr_ret": float(np.corrcoef(sk[ok], ret[ok])[0, 1]),
                  "corr_skew_rr": float(np.corrcoef(sk, [r["skew"] for r in rows])[0, 1]),
                  "svix_mean": float(np.mean(svix)), "svix_late": float(np.mean(svix[[r["day"] >= "2024" for r in rows]])),
                  "K": K / F, "strips": strips, "surface_mom": m0})


VX_EXPIRIES = ("2017-05-17", "2017-06-21", "2017-07-19", "2017-08-16", "2017-09-20", "2017-10-18", "2017-11-15",
               "2017-12-20", "2018-01-17", "2018-02-14", "2018-03-21", "2018-04-18")


def compute_vx_etp() -> dict:
    """VIX futures settlements (Cboe), June 2017 to March 2018: the curve, a short-term futures index rebuilt by its
    published roll rule, a -1x daily note on it, and the close-of-day futures its hedger had to buy."""
    settle = {}
    for e in VX_EXPIRIES:
        d = data.cboe_vx(e)
        settle[int(e.replace("-", ""))] = dict(zip(np.asarray(d["date"]).tolist(), np.asarray(d["settle"]).tolist()))
    exps = sorted(settle)
    days = sorted(d for d in set().union(*[set(v) for v in settle.values()]) if 20170601 <= d <= 20180320)
    days = [d for d in days if sum(1 for e in exps if e > d and d in settle[e]) >= 2]
    ix = V.vx_index(days, settle, exps)
    note = V.inverse_note(ix["ret"])
    i5 = days.index(20180205)
    idec = max(i for i, d in enumerate(days) if d <= 20171229)
    slope, curve = [], []
    for d in days:
        fut = [e for e in exps if e > d and d in settle[e]]
        slope.append(settle[fut[1]][d] / settle[fut[0]][d] - 1)
        curve.append([(_ymd_days(e) - _ymd_days(d), settle[e][d]) for e in fut[:7]])
    vix = data.fred("VIXCLS", "2017-06-01", "2018-06-30")
    vxd = dict(zip(np.asarray(vix["date"]).tolist(), np.asarray(vix["value"]).tolist()))
    flow = V.rebalance_flow(-1.0, ix["ret"], note[:-1])  # per dollar of note at the start
    e1, e2 = 20180214, 20180321
    return _json({"days": days, "t": [_ymd_year(d) for d in days], "level": ix["level"], "ret": ix["ret"], "w1": ix["w1"],
                  "note": note, "slope": slope, "curve": curve, "vix": [vxd.get(d) for d in days],
                  "feb5_ret": float(ix["ret"][i5 - 1]), "note_feb5": float(note[i5] / note[i5 - 1] - 1),
                  "note_jun_dec": float(note[idec] - 1), "note_peak": float(note[:i5].max()),
                  "note_peak_day": days[int(np.argmax(note[:i5]))], "contango": float((np.array(slope) > 0).mean()),
                  "median_slope": float(np.median(slope)), "flow": flow, "flow_feb5": float(flow[i5 - 1] / note[i5 - 1]),
                  "front": [settle[e1][20180202], settle[e1][20180205]], "second": [settle[e2][20180202], settle[e2][20180205]],
                  "front_jump": float(settle[e1][20180205] / settle[e1][20180202] - 1),
                  "second_jump": float(settle[e2][20180205] / settle[e2][20180202] - 1), "i_feb5": i5})


def _ymd_days(d):
    d = int(d)
    return date(d // 10000, (d // 100) % 100, d % 100).toordinal()


def _ymd_year(d):
    d = int(d)
    x = date(d // 10000, (d // 100) % 100, d % 100)
    return x.year + (x.timetuple().tm_yday - 1) / 365


def compute_gamma_toy() -> dict:
    """Simulated (the generating model: Gaussian minute shocks, a dealer gamma k fed back through linear impact, half the
    hedge left for the last 30 minutes): realized vol and the intraday-momentum slope against k, five seeds."""
    ks = np.linspace(-0.6, 0.6, 13)
    vol, slope = [], []
    for seed in range(5):
        eps = 0.001 * np.random.default_rng(seed).standard_normal((2000, 390))
        base = V.gamma_day(eps, 0.0)["rest"].std()
        vs, ss = [], []
        for k in ks:
            o = V.gamma_day(eps, k)
            vs.append(float(o["rest"].std() / base))
            ss.append(float(np.polyfit(o["rest"], o["last"], 1)[0]))
        vol.append(vs)
        slope.append(ss)
    eps = 0.001 * np.random.default_rng(11).standard_normal((300, 390))
    lo, hi = V.gamma_day(eps, 0.5), V.gamma_day(eps, -0.5)
    return _json({"k": ks, "vol": vol, "slope": slope, "demo_long": np.cumsum(lo["r"][7]), "demo_short": np.cumsum(hi["r"][7]),
                  "demo_eps": np.cumsum(eps[7]), "scatter_long": [lo["rest"], lo["last"]],
                  "scatter_short": [hi["rest"], hi["last"]],
                  "slope_long": float(np.polyfit(lo["rest"], lo["last"], 1)[0]),
                  "slope_short": float(np.polyfit(hi["rest"], hi["last"], 1)[0]),
                  "vol_short": float(np.mean([v[1] for v in vol])), "vol_long": float(np.mean([v[-2] for v in vol])),
                  "k_short": float(ks[1]), "k_long": float(ks[-2])})


# ---------------------------------------------------------------------------
def _vae_train(X, seed, steps=3000, every=100, show=None):
    import torch
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Z = torch.tensor((X - mu) / sd, dtype=torch.float32)
    n_in, n_lat = Z.shape[1], 2
    enc = torch.nn.Sequential(torch.nn.Linear(n_in, 64), torch.nn.Tanh(), torch.nn.Linear(64, 2 * n_lat))
    dec = torch.nn.Sequential(torch.nn.Linear(n_lat, 64), torch.nn.Tanh(), torch.nn.Linear(64, n_in))
    opt = torch.optim.Adam(list(enc.parameters()) + list(dec.parameters()), lr=3e-3)
    loss_h, ck = [], []
    for it in range(steps + 1):
        e = enc(Z)
        m_, lv = e[:, :n_lat], e[:, n_lat:]
        z = m_ + torch.exp(0.5 * lv) * torch.randn_like(m_)
        rec = dec(z)
        kl = -0.5 * torch.mean(torch.sum(1 + lv - m_ ** 2 - torch.exp(lv), 1))
        loss = torch.mean((rec - Z) ** 2) + 0.01 * kl
        if it % every == 0:
            with torch.no_grad():
                mm = enc(Z)[:, :n_lat]
                r_ = dec(mm).numpy()
                err = float(np.sqrt(np.mean((np.exp(r_ * sd + mu) - np.exp(X)) ** 2)) * 100)
                loss_h.append(err)
                if show is not None:
                    ck.append(np.exp(r_[show] * sd + mu))
        if it == steps:
            break
        opt.zero_grad()
        loss.backward()
        opt.step()
    return enc, dec, mu, sd, loss_h, ck


def compute_vae() -> dict:
    import torch
    rows = _weeks()
    X = np.array([np.asarray(r["grid"]).ravel() for r in rows])
    X = np.log(np.clip(X, 0.05, 5.0))
    days = [r["day"] for r in rows]
    show = days.index(min(days, key=lambda d: abs(_year(d) - _year("2022-11-09"))))
    losses, recons = [], []
    for seed in range(5):
        enc, dec, mu, sd, lh, ck = _vae_train(X, seed, show=show)
        losses.append(lh)
        recons.append(lh[-1])
        if seed == 0:
            enc0, dec0, mu0, sd0, ck0 = enc, dec, mu, sd, ck
    with torch.no_grad():
        m_ = enc0(torch.tensor((X - mu0) / sd0, dtype=torch.float32))[:, :2].numpy()
        recon = dec0(torch.tensor(m_)).numpy()
        err = float(np.sqrt(np.mean((np.exp(recon * sd0 + mu0) - np.exp(X)) ** 2)) * 100)
        walk = {}
        for name, axis in (("z1", 0), ("z2", 1)):
            outs = []
            for v_ in np.linspace(-2, 2, 5):
                z = np.zeros((1, 2))
                z[0, axis] = v_
                outs.append(np.exp(dec0(torch.tensor(z, dtype=torch.float32)).numpy()[0] * sd0 + mu0).reshape(len(TGRID), len(KGRID)))
            walk[name] = np.array(outs)
    # the equal-size baseline: two principal components of the (standardized) log grids
    Zs = (X - mu0) / sd0
    U, S_, Vt = np.linalg.svd(Zs - Zs.mean(0), full_matrices=False)
    rec2 = (U[:, :2] * S_[:2]) @ Vt[:2] + Zs.mean(0)
    pca_err = float(np.sqrt(np.mean((np.exp(rec2 * sd0 + mu0) - np.exp(X)) ** 2)) * 100)
    atm = np.array([np.asarray(r["grid"])[2, len(KGRID) // 2] for r in rows])
    skew = np.array([r["skew"] for r in rows])
    c1 = [float(np.corrcoef(m_[:, j], atm)[0, 1]) for j in range(2)]
    c2 = [float(np.corrcoef(m_[:, j], skew)[0, 1]) for j in range(2)]
    return _json({"latent": m_, "recon_rmse_volpts": err, "walk": walk, "corr_atm": c1, "corr_skew": c2, "days": days,
                  "atm": atm, "skew": skew, "losses": losses, "recon_seeds": recons, "ck_steps": list(range(0, 3001, 100)),
                  "ck_show": ck0, "show_day": days[show], "show_true": np.exp(X[show]), "pca2_rmse": pca_err,
                  "n": len(rows), "enc_mu": mu0, "enc_sd": sd0})


def compute_neural_surface() -> dict:
    """The penalised network (Ackerer et al. 2020) and the same network unpenalised on the Surface: 80% of the
    quotes to train, 20% held out, three splits/seeds; SSVI fitted on the same training quotes as the baseline."""
    import torch
    from explainer.quant.house import deep
    torch.set_num_threads(1)
    q = surface.build(surface.DAYS[0])
    k, T, iv, vg = (np.asarray(q[x]) for x in ("k", "T", "iv", "vega"))
    ok = (np.abs(k) < 0.6) & (T > 2 / 365)
    k, T, iv, vg = k[ok], T[ok], iv[ok], vg[ok]
    part = CACHE.partial("neural_surface", {"v": 1, "steps": 3000})
    gk = np.linspace(-0.6, 0.6, 25)
    gT = np.linspace(3 / 365, 0.8, 12)
    for seed in range(3):
        tr = np.random.default_rng(seed).random(len(k)) >= 0.2
        for pen in (1.0, 0.0):
            key = f"{seed}_{pen:g}"
            if key in part:
                continue
            r = deep.train_surface_net(k, T, iv, penalty=pen, seed=seed, steps=3000, every=100, train=tr,
                                       grid=(gk, gT), log=print if seed == 0 else None)
            keep = {x: r[x] for x in ("step", "train", "test", "pen", "g_neg", "train_rmse", "test_rmse", "g_viol",
                                      "cal_viol", "secs")}
            keep["test_vw"] = float(np.sqrt(np.sum(vg[~tr] * (r["pred"][~tr] - iv[~tr]) ** 2) / np.sum(vg[~tr])) * 100)
            if seed == 0:
                keep["surf"] = r["surf"]
                keep["g_flags"] = r["g_flags"]
            fit = V.fit_ssvi(k[tr], T[tr], iv[tr] ** 2 * T[tr], weights=vg[tr])
            pr = _ssvi_iv(fit, k, T)
            keep["ssvi_test"] = float(np.sqrt(np.mean((pr[~tr] - iv[~tr]) ** 2)) * 100)
            keep["ssvi_test_vw"] = float(np.sqrt(np.sum(vg[~tr] * (pr[~tr] - iv[~tr]) ** 2) / np.sum(vg[~tr])) * 100)
            keep["ssvi_train"] = float(np.sqrt(np.mean((pr[tr] - iv[tr]) ** 2)) * 100)
            keep["train_mask"] = tr.astype(int)
            part[key] = _json(keep)
    R = {key: part[key] for key in part.done}
    pen = [R[f"{s_}_1"] for s_ in range(3)]
    raw = [R[f"{s_}_0"] for s_ in range(3)]
    return _json({"runs": R, "k": k, "T": T, "iv": iv, "gk": gk, "gT": gT,
                  "colloc_k": np.tile(np.linspace(-1, 1, 41), 30), "colloc_T": np.repeat(np.linspace(3 / 365, 0.8, 30), 41),
                  "pen_test": [r_["test_rmse"] for r_ in pen], "raw_test": [r_["test_rmse"] for r_ in raw],
                  "ssvi_test": [r_["ssvi_test"] for r_ in pen], "pen_test_vw": [r_["test_vw"] for r_ in pen],
                  "ssvi_test_vw": [r_["ssvi_test_vw"] for r_ in pen], "pen_g": [r_["g_viol"] for r_ in pen],
                  "raw_g": [r_["g_viol"] for r_ in raw], "pen_cal": [r_["cal_viol"] for r_ in pen],
                  "raw_cal": [r_["cal_viol"] for r_ in raw], "secs": [r_["secs"] for r_ in pen + raw]})


def compute_operator_net() -> dict:
    """One network for every week (the frontier's "one model for all days", in miniature): implied vol as a function of
    (k, sqrt T) and the week's two VAE coordinates, trained on the quotes of the first 80% of weeks, scored on the
    last 20% against the VAE's own decoded grid (the same two numbers) and SSVI fitted to each held-out week itself."""
    import torch
    from explainer.quant.house import deep
    from scipy.interpolate import RegularGridInterpolator
    torch.set_num_threads(1)
    rows = _weeks()
    vae = load("vae")
    Z = np.asarray(vae["latent"])
    n = len(rows)
    cut = int(0.8 * n)
    Q = [np.asarray(r["q"]) for r in rows]
    wk = np.concatenate([np.full(q.shape[1], i) for i, q in enumerate(Q)])
    A = np.concatenate(Q, axis=1)
    k, T, iv = A[0], A[1], A[2]
    zz = Z[wk]
    tr = wk < cut
    part = CACHE.partial("operator_net", {"v": 1})
    for seed in range(3):
        key = str(seed)
        if key in part:
            continue
        torch.manual_seed(seed)
        mlp = deep._mlp(4, 64, 3, act=torch.nn.Tanh)
        c0 = float(np.log(np.exp(0.6) - 1))
        f32 = lambda a: torch.tensor(np.asarray(a, float), dtype=torch.float32)  # noqa: E731
        X = f32(np.column_stack([k, np.sqrt(T), zz]))
        y = f32(iv)
        opt = torch.optim.Adam(mlp.parameters(), lr=2e-3)
        g = np.random.default_rng(seed)
        idx_tr = np.nonzero(tr)[0]
        hist = []
        for it in range(4001):
            b = torch.tensor(g.choice(idx_tr, 2048))
            pred = torch.nn.functional.softplus(mlp(X[b])[:, 0] + c0)
            loss = ((pred - y[b]) ** 2).mean()
            if it % 200 == 0:
                with torch.no_grad():
                    p_all = torch.nn.functional.softplus(mlp(X)[:, 0] + c0).numpy()
                hist.append((it, float(np.sqrt(np.mean((p_all[tr] - iv[tr]) ** 2)) * 100),
                             float(np.sqrt(np.mean((p_all[~tr] - iv[~tr]) ** 2)) * 100)))
            opt.zero_grad()
            loss.backward()
            opt.step()
        part[key] = {"hist": hist, "test": hist[-1][2], "train": hist[-1][1]}
    # baselines on the held-out weeks
    dec_err, ssvi_err = [], []
    import torch as _t
    for i in range(cut, n):
        q = Q[i]
        ssvi_err.append(np.asarray(_ssvi_iv(rows[i]["fit"], q[0], q[1])) - q[2])
    ssvi_rmse = float(np.sqrt(np.mean(np.concatenate(ssvi_err) ** 2)) * 100)
    # the VAE decoder at the same two numbers (the decoder is retrained here exactly as in ``vae``, seed 0)
    X = np.log(np.clip(np.array([np.asarray(r["grid"]).ravel() for r in rows]), 0.05, 5.0))
    enc, dec, mu, sd, _, _ = _vae_train(X, 0)
    with _t.no_grad():
        D = np.exp(dec(_t.tensor(Z, dtype=_t.float32)).numpy() * sd + mu)
    for i in range(cut, n):
        q = Q[i]
        f = RegularGridInterpolator((TGRID, KGRID), D[i].reshape(len(TGRID), len(KGRID)), bounds_error=False, fill_value=None)
        dec_err.append(f(np.column_stack([np.clip(q[1], TGRID[0], TGRID[-1]), np.clip(q[0], KGRID[0], KGRID[-1])])) - q[2])
    dec_rmse = float(np.sqrt(np.mean(np.concatenate(dec_err) ** 2)) * 100)
    R = [part[str(s_)] for s_ in range(3)]
    return _json({"runs": R, "test": [r_["test"] for r_ in R], "train": [r_["train"] for r_ in R], "ssvi_rmse": ssvi_rmse,
                  "dec_rmse": dec_rmse, "n_weeks": n, "n_train_weeks": cut, "n_quotes": int(len(k)),
                  "first_test_day": rows[cut]["day"]})


ITEMS = {"surface": compute_surface, "localvol": compute_localvol, "varswap": compute_varswap,
         "history": compute_history, "history_ext": compute_history_ext, "volmageddon": compute_volmageddon,
         "termskew": compute_termskew, "dynamics": compute_dynamics, "arbitrage": compute_arbitrage,
         "svi_replay": compute_svi_replay, "ssvi_replay": compute_ssvi_replay, "bbf": compute_bbf,
         "dk_tree": compute_dk_tree, "gyongy": compute_gyongy, "lv_mc": compute_lv_mc, "trunc": compute_trunc,
         "replication": compute_replication, "vixcomp": compute_vixcomp, "vrp_pnl": compute_vrp_pnl,
         "spx_vrp": compute_spx_vrp, "rn_moments": compute_rn_moments, "vx_etp": compute_vx_etp,
         "gamma_toy": compute_gamma_toy, "vae": compute_vae, "neural_surface": compute_neural_surface,
         "operator_net": compute_operator_net, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
