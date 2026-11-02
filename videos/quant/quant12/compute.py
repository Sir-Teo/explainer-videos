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
                part[day] = {"day": day, "S": F, "fit": {x: fit[x] for x in ("rho", "eta", "gamma", "theta", "T", "rmse")},
                             "kvar": kvar, "rv": rv, "rv_trail": rvt, "ret30": ret, "grid": grid,
                             "atm": float(_ssvi_iv(fit, 0.0, T30)),
                             "skew": float(_ssvi_iv(fit, -0.1, T30) - _ssvi_iv(fit, 0.1, T30)),
                             "svix2": float(2 / (T30 * F ** 2) * np.trapezoid(otm, K)),
                             "dvol": float(dvc[j]) if abs(dvt[j] - ref) < 7200 else None, "mom": mom, "n": int(ok.sum()),
                             "q": np.round(np.vstack([kq, Tq, ivq, vq]), 5)}
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
