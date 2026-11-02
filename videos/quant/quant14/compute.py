"""Every number in Part 14 (Rough and Path-Dependent Volatility), computed and cached in .cache/quant14/.

    python -m videos.quant.quant14.compute [items] [--force]

Items (seconds to minutes each on a CPU):

* ``skew``       the Surface's at-the-money skew by maturity: a power law against Guyon and El Amrani's bounded
                 alternative;
* ``roughness``  bitcoin's daily realized variance from 5-minute returns (2024-2025): the scaling of log-RV increments
                 and the Hurst exponent, Gatheral-Jaisson-Rosenbaum style; the same estimator on fBm with known H;
* ``artefact``   the critique: a smooth volatility (H = 0.5) measured through noisy realized variance, estimated by
                 the same estimator (Cont and Das 2024);
* ``rbergomi``   rough Bergomi calibrated to the Surface (hybrid scheme, common random numbers), with the forward
                 variance curve of Part 13;
* ``rheston``    rough Heston calibrated to the Surface (fractional Adams, COS); its skew term structure;
* ``lift``       the lifted Heston's error against rough Heston as factors are added (Abi Jaber and El Euch);
* ``hawkes``     order flow as a Hawkes process, from a branching ratio of 0.5 to the critical 0.99: where roughness
                 comes from (illustration);
* ``pdv``        Guyon and Lekeufack's path-dependent volatility fitted to DVOL from bitcoin's own returns, in sample
                 (2021-2023) and out of sample (2024-2025);
* ``envelope``   registers nothing (no strategy is tested); the counter.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, pit, rough as R, sim, smile, stochvol as sv, surface

CACHE = Cache("quant14")
load = CACHE.load
Q13 = Cache("quant13")
ROOT = Path(__file__).resolve().parents[3]


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


def _quotes(min_T=2 / 365, max_T=200 / 365, max_k=0.5):
    q = surface.build(surface.DAYS[0])
    ok = (np.abs(q["k"]) < max_k) & (q["T"] > min_T) & (q["T"] < max_T)
    return {k: (np.asarray(v)[ok] if isinstance(v, np.ndarray) and len(v) == len(ok) else v) for k, v in q.items()}


def _rmse(iv, Q):
    m = np.isfinite(iv)
    return float(np.sqrt(np.average((iv[m] - Q["iv"][m]) ** 2 * 1e4, weights=Q["vega"][m])))


# ---------------------------------------------------------------------------
def compute_skew() -> dict:
    s = Q13.load("skew")
    T = np.array([r["T"] for r in s["market"]])
    y = np.abs(np.array([r["skew"] for r in s["market"]]))
    # a power law c T^-a, against Guyon and El Amrani's (2023) bounded alternative c (T + eps)^-a: the second has a
    # finite skew as T -> 0, and fits short-dated SPX skews better
    pw = least_squares(lambda p: np.log(p[0] * T ** (-p[1])) - np.log(y), [0.1, 0.5], bounds=([1e-4, 0], [10, 2]))
    sh = least_squares(lambda p: np.log(p[0] * (T + p[2]) ** (-p[1])) - np.log(y), [0.1, 0.5, 0.002],
                       bounds=([1e-4, 0, 0], [10, 3, 0.2]))
    rm = lambda r: float(np.sqrt(np.mean(r.fun ** 2)))  # noqa: E731
    Tg = np.exp(np.linspace(np.log(1 / 365), np.log(1.0), 60))
    return _json({"T": T, "skew": y, "power": {"c": pw.x[0], "a": pw.x[1], "rmse_log": rm(pw)},
                  "shifted": {"c": sh.x[0], "a": sh.x[1], "eps": sh.x[2], "rmse_log": rm(sh)},
                  "grid": Tg, "power_fit": pw.x[0] * Tg ** (-pw.x[1]), "shifted_fit": sh.x[0] * (Tg + sh.x[2]) ** (-sh.x[1]),
                  "H_implied": 0.5 - pw.x[1]})


def _daily_rv(start="2024-01", end="2025-11"):
    kl = data.binance_klines("BTCUSDT", "5m", start, end)
    t = np.asarray(kl["time"])
    c = np.asarray(kl["close"], float)
    r = np.diff(np.log(c))
    day = (t[1:] // 86400).astype(int)
    days, idx = np.unique(day, return_index=True)
    rv = np.add.reduceat(r * r, idx)
    cnt = np.diff(np.append(idx, len(r)))
    ok = cnt >= 280  # complete days only (288 five-minute returns)
    return days[ok], rv[ok] * 365


def compute_roughness() -> dict:
    days, rv = _daily_rv()
    est = R.log_rv_scaling(np.log(rv))
    # the estimator on fractional Brownian motion with known H
    checks = []
    for H in (0.05, 0.1, 0.3, 0.5):
        x = np.asarray(sim.fbm(H, len(rv), 1.0, 1, seed=int(100 * H))).ravel()
        checks.append({"H": H, "est": R.log_rv_scaling(x)["H"]})
    # a rough path and a smooth one with the same variance as bitcoin's log RV, for the picture
    lv = np.log(rv)
    sd = np.std(np.diff(lv))
    fb = {}
    for H in (est["H"], 0.5):
        x = np.asarray(sim.fbm(H, len(rv), 1.0, 1, seed=7)).ravel()
        x = (x - x.mean()) / np.std(np.diff(x)) * sd + lv.mean()
        fb[f"{H:.2f}"] = x[:len(rv)]
    return _json({"days": days, "rv": rv, "lags": est["lags"], "qs": est["qs"], "zeta": est["zeta"], "H": est["H"],
                  "m": {str(q): est[f"m_{q}"] for q in est["qs"]}, "checks": checks, "paths": fb})


def _smooth_rv(half_lives, weights, sig, n_days=700, m=288, seed=14):
    """A smooth volatility (each factor a log-OU, H = 1/2), sampled every 5 minutes; returns the daily integrated
    variance and the realized variance measured from m simulated returns a day."""
    g = np.random.default_rng(seed)
    dt = 1 / 365 / m
    N = n_days * m
    x = np.zeros(N)
    for hl, w in zip(half_lives, weights):
        k = np.log(2) / (hl / 365)
        e = np.exp(-k * dt)
        sd = sig * w * np.sqrt((1 - e * e) / (2 * k))
        z = g.standard_normal(N) * sd
        f = np.empty(N)
        f[0] = 0.0
        for i in range(1, N):  # an AR(1) recursion, exact for the OU process
            f[i] = f[i - 1] * e + z[i]
        x += f
    vol = 0.5 * np.exp(x)
    r = vol * np.sqrt(dt) * g.standard_normal(N)
    rv = (r * r).reshape(n_days, m).sum(axis=1) * 365
    iv = (vol ** 2).reshape(n_days, m).mean(axis=1)
    return iv, rv


def compute_artefact() -> dict:
    """The critique (Cont and Das 2024; Guyon and El Amrani 2023; multi-scale models before them): the estimator can be
    fooled. First, bitcoin's own weekly pattern (calm weekends) is a periodic component that lowers the estimate; we
    remove the day-of-week means. Then three smooth volatilities (H = 1/2), as variable as bitcoin's, measured through
    5-minute realized variance over 700 days: one log-OU factor (half-life 10 days), two (1 and 60 days), and one very
    fast factor (half-life 5 hours)."""
    days, rv = _daily_rv()
    lv = np.log(rv)
    dow = (days + 3) % 7
    ds = lv.copy()
    for d in range(7):
        ds[dow == d] -= lv[dow == d].mean() - lv.mean()
    out = {"btc": R.log_rv_scaling(lv)["H"], "btc_deseasonalized": R.log_rv_scaling(ds)["H"],
           "dow_mean_rv": [float(np.exp(lv[dow == d].mean())) for d in range(7)], "models": []}
    for name, hl, w, sig in (("one factor, half-life 10 days", (10,), (1.0,), 10.0),
                             ("two factors, 1 and 60 days", (1, 60), (0.8, 0.6), 6.0),
                             ("one factor, half-life 5 hours", (0.2,), (1.0,), 8.0)):
        iv, rv2 = _smooth_rv(hl, w, sig)
        out["models"].append({"name": name, "H_integrated": R.log_rv_scaling(np.log(iv))["H"],
                              "H_rv": R.log_rv_scaling(np.log(rv2))["H"], "sd_dlog": float(np.std(np.diff(np.log(rv2))))})
    return _json(out)


def _xi_curve():
    b = Q13.load("bergomi")
    e = np.asarray(b["edges"])
    fv = np.asarray(b["market_fwd_var"])

    def xi(t):
        i = np.clip(np.searchsorted(e, t, side="right") - 1, 0, len(fv) - 1)
        return fv[i]
    return xi


def _mc_iv(S, Q, n_days):
    out = np.full(len(Q["K"]), np.nan)
    for T in np.unique(Q["T"]):
        m = Q["T"] == T
        d = int(round(T * 365))
        if d > n_days:
            continue
        ST = S[d] * float(Q["F"][m][0])
        for j in np.flatnonzero(m):
            K, cp = Q["K"][j], int(Q["cp"][j])
            p = float(np.mean(np.maximum(cp * (ST - K), 0)))
            out[j] = bs.implied_vol(p, float(Q["F"][j]), K, T, 0.0, 0.0, cp)
    return out


def compute_rbergomi() -> dict:
    Q = _quotes()
    n_days = int(round(Q["T"].max() * 365))
    xi = _xi_curve()
    n_paths = 20000

    def ivs(p, seed=3):
        H, eta, rho = p
        S = R.rbergomi_paths(H, eta, rho, xi, n_days / 365, n_days, n_paths, seed=seed)
        return _mc_iv(S, Q, n_days)

    w = np.sqrt(Q["vega"] / Q["vega"].mean())

    def resid(p):
        iv = ivs(p)
        e = (iv - Q["iv"]) * 100 * w
        return np.where(np.isfinite(e), e, 20.0)

    r = least_squares(resid, [0.1, 1.5, -0.2], bounds=([0.01, 0.2, -0.95], [0.49, 5.0, 0.95]), diff_step=0.05,
                      max_nfev=40)
    iv = ivs(r.x, seed=11)  # out of sample: fresh random numbers
    Tg = np.exp(np.linspace(np.log(3 / 365), np.log(0.5), 14))
    # the model's ATM skew by maturity, on its own grid
    nd = int(round(0.5 * 365))
    S = R.rbergomi_paths(*r.x, xi, nd / 365, nd, 40000, seed=21)
    sk = []
    for T in Tg:
        d = max(1, int(round(T * 365)))
        x = S[d]
        p = [float(np.mean(np.maximum(c * (x - np.exp(k)), 0))) for k, c in ((-0.02, -1), (0.02, 1))]
        v = [bs.implied_vol(p[0], 1.0, np.exp(-0.02), d / 365, 0, 0, -1), bs.implied_vol(p[1], 1.0, np.exp(0.02), d / 365, 0, 0, 1)]
        sk.append(float((v[1] - v[0]) / 0.04))
    return _json({"params": {"H": r.x[0], "eta": r.x[1], "rho": r.x[2]}, "x": r.x, "rmse": _rmse(iv, Q),
                  "iv": iv, "skew_T": Tg, "skew": sk, "n": len(Q["K"]), "n_paths": n_paths})


def compute_rbskew() -> dict:
    """Rough Bergomi's at-the-money skew by maturity, from the fitted parameters: the slope of implied vol over
    log-moneyness -0.08..0.08 (least squares on 9 strikes), 100,000 paths, so Monte Carlo noise stays small."""
    rb = load("rbergomi")
    xi = _xi_curve()
    nd = 183
    S = R.rbergomi_paths(*rb["x"], xi, nd / 365, nd * 2, 100000, seed=31)
    ks = np.linspace(-0.08, 0.08, 9)
    Tg = np.exp(np.linspace(np.log(3 / 365), np.log(0.5), 14))
    out = []
    for T in Tg:
        i = max(1, int(round(T * 365 * 2)))
        x = S[i]
        iv = []
        for k in ks:
            c = 1 if k >= 0 else -1
            pr = float(np.mean(np.maximum(c * (x - np.exp(k)), 0)))
            iv.append(bs.implied_vol(pr, 1.0, np.exp(k), i / 730, 0, 0, c))
        iv = np.asarray(iv, float)
        ok = np.isfinite(iv)
        out.append(float(np.polyfit(ks[ok], iv[ok], 2)[1]))  # the slope at the money of a quadratic fit
    # Part 13's Heston on the same quotes (expiries up to 200 days), for a like-for-like comparison
    Q = _quotes()
    hx = Q13.load("calibrate")["fits"]["Heston"]["x"]
    hiv = np.empty(len(Q["K"]))
    for T in np.unique(Q["T"]):
        m = Q["T"] == T
        hiv[m] = sv.surface_iv("Heston", hx, float(Q["F"][m][0]), Q["K"][m], T)
    return _json({"skew_T": Tg, "skew": out, "heston_rmse_same": _rmse(hiv, Q)})


def compute_rheston() -> dict:
    Q = _quotes()
    w = np.sqrt(Q["vega"] / Q["vega"].mean())
    Ts = np.unique(Q["T"])

    def cf_for(p):
        v0, lam, theta, nu, rho, H = p
        return lambda u, T: R.rough_heston_cf(u, T, v0, lam, theta, nu, rho, H, n=80)

    def ivs(p):
        out = np.empty(len(Q["K"]))
        cf = cf_for(p)
        for T in Ts:
            m = Q["T"] == T
            F = float(Q["F"][m][0])
            with np.errstate(all="ignore"):
                pr = sv.cos_price(cf, F, Q["K"][m], T, Q["cp"][m], N=192, L=14)
            out[m] = [bs.implied_vol(a, F, k, T, 0, 0, int(c)) for a, k, c in zip(pr, Q["K"][m], Q["cp"][m])]
        return out

    def resid(p):
        e = (ivs(p) - Q["iv"]) * 100 * w
        return np.where(np.isfinite(e), e, 20.0)

    x0 = [0.2, 2.0, 0.3, 1.0, -0.2, 0.1]
    r = least_squares(resid, x0, bounds=([1e-3, 0.01, 1e-3, 0.05, -0.95, 0.02], [2, 30, 2, 5, 0.95, 0.49]),
                      max_nfev=60, x_scale="jac")
    iv = ivs(r.x)
    Tg = np.exp(np.linspace(np.log(2 / 365), np.log(1.0), 16))
    cf = cf_for(r.x)
    sk = []
    for T in Tg:
        v = sv.model_iv(cf, 1.0, np.exp(np.array([-0.02, 0.02])), T)
        sk.append(float((v[1] - v[0]) / 0.04))
    names = ("v0", "lambda", "theta", "nu", "rho", "H")
    return _json({"params": dict(zip(names, r.x)), "x": r.x, "rmse": _rmse(iv, Q), "iv": iv, "skew_T": Tg, "skew": sk,
                  "n": len(Q["K"])})


def compute_rprofile() -> dict:
    """Rough Heston with H held fixed (0.05, 0.1, 0.2), the other five re-fitted from the free fit: how much does
    the Surface care about roughness? And each fit's skew term structure."""
    Q = _quotes()
    w = np.sqrt(Q["vega"] / Q["vega"].mean())
    Ts = np.unique(Q["T"])
    best = load("rheston")["x"]

    def ivs(p):
        v0, lam, theta, nu, rho, H = p
        cf = lambda u, T: R.rough_heston_cf(u, T, v0, lam, theta, nu, rho, H, n=80)  # noqa: E731
        out = np.empty(len(Q["K"]))
        for T in Ts:
            m = Q["T"] == T
            F = float(Q["F"][m][0])
            with np.errstate(all="ignore"):
                pr = sv.cos_price(cf, F, Q["K"][m], T, Q["cp"][m], N=192, L=14)
            out[m] = [bs.implied_vol(a, F, k, T, 0, 0, int(c)) for a, k, c in zip(pr, Q["K"][m], Q["cp"][m])]
        return out

    rows = []
    Tg = np.exp(np.linspace(np.log(2 / 365), np.log(1.0), 16))
    for H in (0.05, 0.1, 0.2):
        def resid(q, H=H):
            e = (ivs(list(q) + [H]) - Q["iv"]) * 100 * w
            return np.where(np.isfinite(e), e, 20.0)
        r = least_squares(resid, best[:5], bounds=([1e-3, 0.01, 1e-3, 0.05, -0.95], [2, 30, 2, 5, 0.95]),
                          max_nfev=25, x_scale="jac")
        x = list(r.x) + [H]
        iv = ivs(x)
        cf = lambda u, T, x=x: R.rough_heston_cf(u, T, *x, n=80)  # noqa: E731
        sk = []
        for T in Tg:
            v = sv.model_iv(cf, 1.0, np.exp(np.array([-0.02, 0.02])), T)
            sk.append(float((v[1] - v[0]) / 0.04))
        by = {int(round(T * 365)): _rmse(np.where(Q["T"] == T, iv, np.nan), Q) for T in Ts}
        rows.append({"H": H, "x": x, "rmse": _rmse(iv, Q), "skew": sk, "by_expiry": by})
    ivb = ivs(best)
    by_best = {int(round(T * 365)): _rmse(np.where(Q["T"] == T, ivb, np.nan), Q) for T in Ts}
    return _json({"rows": rows, "skew_T": Tg, "best_by_expiry": by_best})


def compute_lift() -> dict:
    # the rough Heston fit with H = 0.1 from the profile: the lift is built for genuinely rough kernels
    p = next(r["x"] for r in load("rprofile")["rows"] if abs(r["H"] - 0.1) < 1e-9)
    v0, lam, theta, nu, rho, H = p
    u = np.linspace(0.2, 20, 60)
    T = 30 / 365
    ref = R.rough_heston_cf(u, T, v0, lam, theta, nu, rho, H, n=800)
    K = np.exp(np.linspace(-0.3, 0.3, 13))
    iv_ref = sv.model_iv(lambda uu, TT: R.rough_heston_cf(uu, TT, v0, lam, theta, nu, rho, H, n=400), 1.0, K, T)
    rows = []
    for N in (1, 2, 5, 10, 20, 50):
        cfN = lambda uu, TT, N=N: R.lifted_heston_cf(uu, TT, v0, lam, theta, nu, rho, H, N=N, n_steps=600)  # noqa: E731
        err = float(np.abs(cfN(u, T) - ref).max())
        iv = sv.model_iv(cfN, 1.0, K, T)
        rows.append({"N": N, "cf_err": err, "iv_err": float(np.sqrt(np.nanmean((iv - iv_ref) ** 2)) * 100)})
    return _json({"rows": rows, "T": T, "x": p, "H": H})


def compute_hawkes() -> dict:
    """Order arrivals as a Hawkes process (Part 5): each trade raises the rate of the next. As the branching ratio
    approaches one, activity clusters across all time scales; Jaisson and Rosenbaum (2016) prove that the scaling
    limit of nearly unstable Hawkes processes with heavy-tailed kernels is a rough Heston model."""
    out = {}
    T = 20000.0
    grid = np.linspace(0, T, 801)
    for n_ratio in (0.5, 0.9, 0.99):
        beta = 1.0
        alpha = n_ratio * beta
        mu = 1.0 * (1 - n_ratio)  # the same average rate, 1 a unit of time
        ev = sim.hawkes_thinning(mu, alpha, beta, T, seed=int(n_ratio * 100))
        counts = np.histogram(ev, bins=grid)[0]
        out[f"{n_ratio}"] = {"counts": counts, "n_events": len(ev)}
    out["grid"] = grid
    return _json(out)


def _pdv_data():
    kl = data.binance_klines("BTCUSDT", "1d", "2018-01", "2025-11")
    t = np.asarray(kl["time"])
    c = np.asarray(kl["close"], float)
    r = np.diff(np.log(c))
    days = (t[1:] // 86400).astype(int)
    dv = data.deribit_dvol("2021-04", "2025-11", resolution=86400)
    td = (np.asarray(dv["time"]) // 86400).astype(int)
    v = np.asarray(dv["close"], float) / 100
    pos = {d: i for i, d in enumerate(td)}
    vol = np.array([v[pos[d]] if d in pos else np.nan for d in days])  # DVOL's close on day d, with day d's return
    return days, r, vol


def compute_pdv() -> dict:
    days, r, vol = _pdv_data()
    split = datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp() // 86400
    have = np.isfinite(vol)
    first = int(np.argmax(have))
    train = have & (days < split)
    test = have & (days >= split)
    look = 1000
    # fit on 2021-2023 only: kernel shapes and betas
    vv = np.where(have, vol, np.nan)

    def design(p):
        R1, R2 = R.pdv_features(r, 1 / 365, p[0], p[1], p[2], p[3], lookback=look)
        return np.column_stack([np.ones_like(R1), R1, np.sqrt(np.maximum(R2, 0))])

    def resid(p):
        X = design(p)[train]
        b, *_ = np.linalg.lstsq(X, vv[train], rcond=None)
        return X @ b - vv[train]

    fit = least_squares(resid, [1.5, 0.02, 1.5, 0.05], bounds=([1.01, 1e-4, 1.01, 1e-4], [5, 1.0, 5, 1.0]))
    X = design(fit.x)
    b, *_ = np.linalg.lstsq(X[train], vv[train], rcond=None)
    pred = X @ b

    def r2(m):
        y = vv[m]
        return float(1 - np.sum((pred[m] - y) ** 2) / np.sum((y - y.mean()) ** 2))

    # a baseline: implied = a + b * realized over the past 30 days
    rv30 = np.sqrt(np.convolve(r * r, np.ones(30), "full")[: len(r)] / 30 * 365)
    Xb = np.column_stack([np.ones_like(rv30), rv30])
    bb, *_ = np.linalg.lstsq(Xb[train], vv[train], rcond=None)
    pb = Xb @ bb

    def r2b(m):
        y = vv[m]
        return float(1 - np.sum((pb[m] - y) ** 2) / np.sum((y - y.mean()) ** 2))

    tau = np.linspace(0, 200 / 365, 201)
    contrib = {"trend": float(np.std(b[1] * X[have, 1])), "activity": float(np.std(b[2] * X[have, 2]))}
    return _json({"contrib": contrib, "days": days[first:], "vol": vol[first:], "pred": pred[first:], "base": pb[first:],
                  "alpha1": fit.x[0], "delta1": fit.x[1], "alpha2": fit.x[2], "delta2": fit.x[3], "beta": b,
                  "r2_train": r2(train), "r2_test": r2(test), "r2_base_train": r2b(train), "r2_base_test": r2b(test),
                  "split_day": split, "tau": tau, "K1": R.tspl_kernel(tau, fit.x[0], fit.x[1]),
                  "K2": R.tspl_kernel(tau, fit.x[2], fit.x[3])})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": {}}



# =========================================================================== the expansion (hook + 18 chapters)
def _weekly_days():
    man = json.loads((ROOT / "videos/quant/data/manifest.json").read_text())
    days = sorted({k.split("/")[4] for k in man if k.startswith("deribit/trades/BTC/option")})
    return [d for d in days if "2024-01-01" <= d <= "2025-12-31"]


def _atm_skews(Q, kmax=0.3, min_q=8):
    """The at-the-money skew of each expiry: an SVI fit through the quotes with |k| < kmax (at least ``min_q`` of
    them), differentiated at k = 0. Returns rows (T, skew, trades, ATM vol)."""
    rows = []
    for T in np.unique(Q["T"]):
        if T < 1.5 / 365 or T > 1.0:
            continue
        m = (Q["T"] == T) & (np.abs(Q["k"]) < kmax)
        if m.sum() < min_q:
            continue
        p = smile.fit_svi(Q["k"][m], Q["iv"][m] ** 2 * T, weights=Q["vega"][m])

        def sig(k, p=p, T=T):
            return np.sqrt(max(float(smile.svi_total_variance(k, p["a"], p["b"], p["rho"], p["m"], p["s"])), 1e-12) / T)
        rows.append((float(T), float((sig(0.01) - sig(-0.01)) / 0.02), int(Q["n"][m].sum()), sig(0.0)))
    return rows


def compute_skew_weekly() -> dict:
    """The Surface's at-the-money skew term structure on every weekly Deribit day of 2024-2025: per week, a power law
    against Guyon and El Amrani's bounded form, expiries weighted by their trades."""
    days = _weekly_days()
    part = CACHE.partial("skew_weekly", {"days": days, "kmax": 0.3, "min_q": 8})
    for d in days:
        if d in part:
            continue
        try:
            rows = _atm_skews(surface.build(d))
        except Exception as e:  # noqa: BLE001  a day without usable quotes
            part[d] = {"skip": str(e)[:80]}
            continue
        rows = [r for r in rows if abs(r[1]) > 1e-3 and np.isfinite(r[1])]
        if len(rows) < 5:
            part[d] = {"skip": "fewer than 5 expiries"}
            continue
        T, sk, n, atm = (np.array(c) for c in zip(*rows))
        f = R.skew_term_fit(T, sk, weights=n)
        part[d] = _json({"T": T, "skew": sk, "n": n, "atm": atm, "a": f["power"]["a"], "c": f["power"]["c"],
                         "rm_p": f["power"]["rmse_log"], "rm_s": f["shifted"]["rmse_log"], "eps": f["shifted"]["eps"],
                         "a_s": f["shifted"]["a"], "c_s": f["shifted"]["c"]})
        print("  ", d, f"a={f['power']['a']:.2f}", flush=True)
    weeks = [dict(day=d, **part[d]) for d in days if "skip" not in part[d]]
    a = np.array([w["a"] for w in weeks])
    better = np.array([w["rm_s"] < w["rm_p"] - 0.01 for w in weeks])
    eps = np.array([365 * w["eps"] for w in weeks])
    out = {"weeks": weeks, "n_weeks": len(weeks), "a_median": float(np.median(a)), "a_q": np.percentile(a, [25, 75]),
           "share_mid": float(np.mean((a >= 0.3) & (a <= 0.7))), "H_median": float(0.5 - np.median(a)),
           "bounded_share": float(better.mean()), "eps_median_days": float(np.median(eps[better])) if better.any() else 0.0,
           "rmse_median": float(np.median([w["rm_p"] for w in weeks])), "skipped": [d for d in days if "skip" in part[d]]}
    part.finish()
    return _json(out)


def _model_skew(cf, Tg):
    out = []
    for T in Tg:
        v = sv.model_iv(cf, 1.0, np.exp(np.array([-0.02, 0.02])), T)
        out.append(float((v[1] - v[0]) / 0.04))
    return np.array(out)


def _local_slope(T, sk, lo, hi):
    T, sk = np.asarray(T), np.abs(np.asarray(sk))
    m = (T >= lo / 365 - 1e-9) & (T <= hi / 365 + 1e-9) & (sk > 1e-6)
    return float(-np.polyfit(np.log(T[m]), np.log(sk[m]), 1)[0])


def compute_skew_models() -> dict:
    """The at-the-money skew by maturity in classical and rough models (Part 13's Heston and Bates fits, a pure jump
    model with Bates' jumps, rough Bergomi, rough Heston at H = 0.1), with each curve's local power-law exponent at the
    short end (2-14 days) and the long end (60-365 days); and the first-order (in vol of vol) skew formula for rough
    Bergomi, psi(T) = rho eta sqrt(2H) T^{H - 1/2} / (2 (H + 1/2)(H + 3/2)), against its Monte Carlo skew."""
    fits = Q13.load("calibrate")["fits"]
    hx, bx = fits["Heston"]["x"], fits["Bates"]["x"]
    Tg = np.exp(np.linspace(np.log(2 / 365), np.log(1.0), 18))
    cf_h = lambda u, T: sv.heston_cf(u, T, *hx)  # noqa: E731
    cf_b = lambda u, T: sv.bates_cf(u, T, *bx)  # noqa: E731
    cf_m = lambda u, T: sv.bs_cf(u, T, float(np.sqrt(bx[0]))) * sv.merton_jump_cf(u, T, *bx[5:])  # noqa: E731
    pr = next(r for r in load("rprofile")["rows"] if abs(r["H"] - 0.1) < 1e-9)
    cf_r = lambda u, T: R.rough_heston_cf(u, T, *pr["x"], n=120)  # noqa: E731
    out = {"T": Tg}
    for name, cf in (("Heston", cf_h), ("Bates", cf_b), ("jumps", cf_m), ("rough Heston", cf_r)):
        with np.errstate(all="ignore"):
            sk = _model_skew(cf, Tg)
        out[name] = {"skew": sk, "short": _local_slope(Tg, sk, 2, 14), "long": _local_slope(Tg, sk, 60, 365)}
    rb, rs = load("rbergomi"), load("rbskew")
    H, eta, rho = rb["x"]
    T2 = np.asarray(rs["skew_T"])
    out["rBergomi"] = {"T": T2, "skew": np.asarray(rs["skew"]), "short": _local_slope(T2, rs["skew"], 2, 14),
                       "long": _local_slope(T2, rs["skew"], 60, 183)}
    out["formula"] = {"T": T2, "skew": rho * eta * np.sqrt(2 * H) * T2 ** (H - 0.5) / (2 * (H + 0.5) * (H + 1.5))}
    s = load("skew")
    out["market"] = {"T": s["T"], "skew": s["skew"], "short": _local_slope(s["T"], s["skew"], 2, 16),
                     "long": _local_slope(s["T"], s["skew"], 50, 365)}
    out["ratio_formula_mc"] = float(np.median(np.abs(out["formula"]["skew"]) / np.abs(out["rBergomi"]["skew"])))
    return _json(out)


def _daily_rv_2018():
    kl = data.binance_klines("BTCUSDT", "1m", "2018-01", "2020-12")
    t = np.asarray(kl["time"])[::5]
    c = np.asarray(kl["close"], float)[::5]
    r = np.diff(np.log(c))
    gap = np.diff(t) > 301  # a missing minute bar breaks the 5-minute grid: drop those returns
    r[gap] = 0.0
    day = (t[1:] // 86400).astype(int)
    days, idx = np.unique(day, return_index=True)
    rv = np.add.reduceat(r * r, idx)
    cnt = np.add.reduceat((~gap).astype(int), idx)
    ok = (cnt >= 280) & (rv > 0)
    return days[ok], rv[ok] * 365


def _deseason(days, lv):
    dow = (np.asarray(days) + 3) % 7
    ds = lv.copy()
    for d in range(7):
        ds[dow == d] -= lv[dow == d].mean() - lv.mean()
    return ds


def compute_roughness_2018() -> dict:
    """Bitcoin's roughness in an earlier era: 5-minute returns from Binance's 1-minute bars, 2018-2020."""
    days, rv = _daily_rv_2018()
    lv = np.log(rv)
    est = R.log_rv_scaling(lv)
    return _json({"days": days, "rv": rv, "H": est["H"], "zeta": est["zeta"], "qs": est["qs"], "lags": est["lags"],
                  "m": {str(q): est[f"m_{q}"] for q in est["qs"]}, "H_deseasonalized": R.log_rv_scaling(_deseason(days, lv))["H"],
                  "n": len(lv)})


def _forecast_era(lv, H, D, L=250, start=500, refit=20):
    """Out-of-sample forecasts of log RV D days ahead from an expanding window: refit every ``refit`` days on all
    data whose target is already known. HAR (Corsi), AR(1), last value, and the rough forecast (GJR weights) with an
    affine calibration. Returns the test targets and each model's predictions."""
    n = len(lv)
    y = np.full(n, np.nan)
    y[: n - D] = lv[D:]
    X_har = np.full((n, 4), np.nan)
    for i in range(21, n):
        X_har[i] = [1, lv[i], lv[i - 4: i + 1].mean(), lv[i - 21: i + 1].mean()]
    X_ar = np.column_stack([np.ones(n), lv])
    rf = R.rfsv_predict(lv, H, D, window=L)
    X_rf = np.column_stack([np.ones(n), rf])
    test = np.arange(max(start, L), n - D)
    preds = {k: np.full(n, np.nan) for k in ("HAR", "AR(1)", "last value", "rough")}
    b = {}
    for i in test:
        if (i - test[0]) % refit == 0:
            tr = np.arange(max(L, 21), i - D + 1)
            for k, X in (("HAR", X_har), ("AR(1)", X_ar), ("rough", X_rf)):
                b[k], *_ = np.linalg.lstsq(X[tr], y[tr], rcond=None)
        preds["HAR"][i] = X_har[i] @ b["HAR"]
        preds["AR(1)"][i] = X_ar[i] @ b["AR(1)"]
        preds["rough"][i] = X_rf[i] @ b["rough"]
        preds["last value"][i] = lv[i]
    return y, test, preds


def compute_rfsv_forecast() -> dict:
    """The rough forecast of log variance (Gatheral, Jaisson and Rosenbaum 2018, section 5) against HAR, AR(1) and
    the last value, at 1, 5 and 20 days, expanding-window out of sample on two eras of bitcoin."""
    eras = {"2018-2020": load("roughness_2018"), "2024-2025": load("roughness")}
    out = {}
    for name, r in eras.items():
        lv = np.log(np.asarray(r["rv"]))
        H = float(r["H"])
        start = 500 if len(lv) > 900 else 400
        res = {"H": H, "n": len(lv), "start": start}
        for D in (1, 5, 20):
            y, test, P = _forecast_era(lv, H, D, start=start)
            sst = np.sum((y[test] - y[test].mean()) ** 2)
            r2 = {k: float(1 - np.sum((p[test] - y[test]) ** 2) / sst) for k, p in P.items()}
            blocks = np.array_split(test, 4)
            band = {k: [float(1 - np.sum((p[bk] - y[bk]) ** 2) / np.sum((y[bk] - y[bk].mean()) ** 2)) for bk in blocks]
                    for k, p in P.items()}
            res[str(D)] = {"r2": r2, "blocks": band, "n_test": len(test)}
            if D == 5:
                res["series"] = {"i": test, "y": y[test], "rough": P["rough"][test], "HAR": P["HAR"][test]}
        out[name] = res
    wins = {f"{e}/{D}": max(("HAR", "rough"), key=lambda k: out[e][str(D)]["r2"][k]) for e in out for D in (1, 5, 20)}
    out["rough_wins"] = sum(v == "rough" for v in wins.values())
    out["wins"] = wins
    out["weights"] = {str(D): R.rfsv_weights(eras["2024-2025"]["H"], D, 60) for D in (1, 5, 20)}
    return _json(out)


def compute_rb_replay() -> dict:
    """The rough Bergomi calibration of ``rbergomi`` replayed: every evaluation recorded (parameters and error),
    on three random-number seeds with 10,000 paths each (the headline fit used 20,000), each re-priced on fresh
    paths."""
    Q = _quotes()
    n_days = int(round(Q["T"].max() * 365))
    xi = _xi_curve()
    w = np.sqrt(Q["vega"] / Q["vega"].mean())
    P = 10000
    part = CACHE.partial("rb_replay", {"paths": P, "nfev": 25})
    for seed in (3, 4, 5):
        if str(seed) in part:
            continue
        trace = []

        def ivs(p, s):
            return _mc_iv(R.rbergomi_paths(*p, xi, n_days / 365, n_days, P, seed=s), Q, n_days)

        def resid(p, seed=seed):
            iv = ivs(p, seed)
            e = (iv - Q["iv"]) * 100 * w
            trace.append({"x": list(p), "rmse": _rmse(iv, Q), "iv": iv})
            return np.where(np.isfinite(e), e, 20.0)

        r = least_squares(resid, [0.1, 1.5, -0.2], bounds=([0.01, 0.2, -0.95], [0.49, 5.0, 0.95]), diff_step=0.05,
                          max_nfev=25)
        best, keep = np.inf, []
        for i, t in enumerate(trace):
            if t["rmse"] < best:
                best = t["rmse"]
                keep.append({"eval": i, "x": t["x"], "rmse": t["rmse"], "iv": t["iv"]})
        part[str(seed)] = _json({"x": r.x, "fit_rmse": float(min(t["rmse"] for t in trace)),
                           "oos_rmse": _rmse(ivs(r.x, 11), Q), "curve": [t["rmse"] for t in trace], "best": keep,
                           "n_eval": len(trace)})
        print("   seed", seed, r.x, flush=True)
    out = {"seeds": {s: part[s] for s in ("3", "4", "5")}, "T": Q["T"], "k": Q["k"], "iv": Q["iv"], "paths": P}
    Hs = [part[s]["x"][0] for s in ("3", "4", "5")]
    out["H_range"] = [min(Hs), max(Hs)]
    part.finish()
    return _json(out)


def _riemann_rbergomi(H, eta, rho, xi, T, n, P, seed):
    t, Y, dW = R.volterra_riemann(H, T, n, P, seed=seed)
    v = xi(t)[None, :] * np.exp(eta * Y - 0.5 * eta ** 2 * t[None, :] ** (2 * H))
    dt = T / n
    dB = rho * dW + np.sqrt(1 - rho ** 2) * np.random.default_rng(seed + 1).standard_normal((P, n)) * np.sqrt(dt)
    x = np.cumsum(np.sqrt(v[:, :-1]) * dB - 0.5 * v[:, :-1] * dt, axis=1)
    return np.exp(x[:, -1])


def compute_hybrid_check() -> dict:
    """The hybrid scheme against the naive left-point Riemann sum: the variance of the Volterra process at t = 1
    (exactly t^{2H}), the cost against a Cholesky factorisation, and the price bias in rough Bergomi."""
    import time
    from scipy.linalg import cholesky
    rows = []
    for H in (0.05, 0.1, 0.3):
        S, v = R.rbergomi_paths(H, 1.0, 0.0, 1.0, 1.0, 100, 20000, seed=1, return_v=True)
        hyb = float((np.log(v[-1]) + 0.5).var())
        _, Y, _ = R.volterra_riemann(H, 1.0, 100, 20000, seed=2)
        rows.append({"H": H, "hybrid": hyb, "riemann": float(Y[:, -1].var()), "exact": 1.0})
    tim = []
    for n in (500, 2000, 4000):
        t0 = time.perf_counter()
        R.rbergomi_paths(0.1, 1.0, 0.0, 1.0, 1.0, n, 1000, seed=0)
        th = time.perf_counter() - t0
        k = np.arange(1, n + 1)
        C = 0.5 * (k[:, None] ** 0.2 + k[None, :] ** 0.2 - np.abs(k[:, None] - k[None, :]) ** 0.2)
        t0 = time.perf_counter()
        L = cholesky(C, lower=True)
        _ = L @ np.random.default_rng(0).standard_normal((n, 1000))
        tc = time.perf_counter() - t0
        tim.append({"n": n, "hybrid": th, "cholesky": tc})
    rb = load("rbergomi")
    H, eta, rho = rb["x"]
    xi = _xi_curve()
    T, n, P = 30 / 365, 120, 40000
    Sh = R.rbergomi_paths(H, eta, rho, xi, T, n, P, seed=5)[-1]
    Sr = _riemann_rbergomi(H, eta, rho, xi, T, n, P, 5)
    iv = {}
    for name, ST in (("hybrid", Sh), ("riemann", Sr)):
        p = float(np.mean(np.maximum(ST - 1.0, 0)))
        iv[name] = float(bs.implied_vol(p, 1.0, 1.0, T, 0, 0, 1))
    return _json({"var": rows, "timing": tim, "atm30": iv, "params": rb["x"]})


def _adams_trace(u, T, alpha, lam, rho, nu, n):
    """The fractional Adams scheme of ``rough.frac_riccati`` with its predictor recorded at every step."""
    from scipy.special import gamma as Gm
    u = np.atleast_1d(np.asarray(u, complex))
    dt = T / n
    F = lambda h: -0.5 * (u * u + 1j * u) + (1j * rho * nu * u - lam) * h + 0.5 * nu * nu * h * h  # noqa: E731
    h = np.zeros((len(u), n + 1), complex)
    hp_all = np.zeros_like(h)
    Fh = np.zeros_like(h)
    Fh[:, 0] = F(h[:, 0])
    j = np.arange(n + 1)
    for k in range(n):
        jj = j[: k + 1]
        bw = dt ** alpha / Gm(alpha + 1) * ((k + 1 - jj) ** alpha - (k - jj) ** alpha)
        hp = Fh[:, : k + 1] @ bw
        aw = np.empty(k + 1)
        aw[0] = k ** (alpha + 1) - (k - alpha) * (k + 1) ** alpha
        if k >= 1:
            j1 = jj[1:]
            aw[1:] = (k - j1 + 2) ** (alpha + 1) + (k - j1) ** (alpha + 1) - 2 * (k - j1 + 1) ** (alpha + 1)
        aw *= dt ** alpha / Gm(alpha + 2)
        h[:, k + 1] = Fh[:, : k + 1] @ aw + dt ** alpha / Gm(alpha + 2) * F(hp)
        hp_all[:, k + 1] = hp
        Fh[:, k + 1] = F(h[:, k + 1])
    return h, hp_all


def compute_adams_conv() -> dict:
    """The fractional Adams scheme's convergence (max error of the characteristic function over u in [0.5, 15],
    T = 30 days, H = 0.1, against 1,600 steps), its agreement with Heston's closed form at H = 1/2, the solution traced
    step by step for the picture, and |phi(u, T)| over (u, T) for H = 1/2 and H = 0.1."""
    import time
    v0, lam, th, nu, rho = 0.25, 2.0, 0.26, 1.0, -0.3
    u = np.linspace(0.5, 15, 30)
    T = 30 / 365
    ref = R.rough_heston_cf(u, T, v0, lam, th, nu, rho, 0.1, n=1600)
    conv = []
    for n in (25, 50, 100, 200, 400, 800):
        t0 = time.perf_counter()
        c = R.rough_heston_cf(u, T, v0, lam, th, nu, rho, 0.1, n=n)
        conv.append({"n": n, "err": float(np.abs(c - ref).max()), "sec": time.perf_counter() - t0})
    e = np.array([c["err"] for c in conv])
    order = float(-np.polyfit(np.log([c["n"] for c in conv]), np.log(e), 1)[0])
    hest = float(np.abs(R.rough_heston_cf(u, T, v0, lam, th, nu, rho, 0.5, n=200)
                        - sv.heston_cf(u, T, v0, lam, th, nu, rho)).max())
    h, hp = _adams_trace(np.arange(1, 11), T, 0.6, lam, rho, nu, 40)
    ug = np.linspace(0, 25, 36)
    Tg = np.exp(np.linspace(np.log(2 / 365), np.log(1.0), 20))
    surf = {}
    for H in (0.5, 0.1):
        surf[str(H)] = [np.abs(R.rough_heston_cf(ug, TT, v0, lam, th, nu, rho, H, n=120)) for TT in Tg]
    return _json({"conv": conv, "order": order, "heston_err": hest, "params": [v0, lam, th, nu, rho],
                  "trace_re": h.real, "trace_im": h.imag, "pred_re": hp.real, "pred_im": hp.imag, "trace_T": T,
                  "u_grid": ug, "T_grid": Tg, "absphi": surf})


def _rh_ivs(Q, p):
    Ts = np.unique(Q["T"])
    v0, lam, theta, nu, rho, H = p
    cf = lambda u, T: R.rough_heston_cf(u, T, v0, lam, theta, nu, rho, H, n=80)  # noqa: E731
    out = np.empty(len(Q["K"]))
    for T in Ts:
        m = Q["T"] == T
        F = float(Q["F"][m][0])
        with np.errstate(all="ignore"):
            pr = sv.cos_price(cf, F, Q["K"][m], T, Q["cp"][m], N=192, L=14)
        out[m] = [bs.implied_vol(a, F, k, T, 0, 0, int(c)) for a, k, c in zip(pr, Q["K"][m], Q["cp"][m])]
    return out


def compute_rh_profile9() -> dict:
    """Rough Heston's error on the Surface with H held at nine values from 0.05 to 0.5 (the other five re-fitted,
    warm-started from the neighbouring H), and the error by expiry: how much the Surface cares about roughness.
    The fits at 0.05, 0.1 and 0.2 are ``rprofile``'s."""
    Q = _quotes()
    w = np.sqrt(Q["vega"] / Q["vega"].mean())
    Ts = np.unique(Q["T"])
    prof = load("rprofile")
    have = {r["H"]: r for r in prof["rows"]}
    Hs = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]
    part = CACHE.partial("rh_profile9", {"Hs": Hs, "nfev": 20})
    rows = []
    for H in Hs:
        key = f"{H}"
        if any(abs(H - h) < 1e-9 for h in have):
            r = next(v for h, v in have.items() if abs(H - h) < 1e-9)
            rows.append({"H": H, "x": r["x"], "rmse": r["rmse"], "by_expiry": r["by_expiry"], "from": "rprofile"})
            continue
        if key not in part:
            near = min(rows, key=lambda r: abs(r["H"] - H))["x"][:5]

            def resid(q, H=H):
                e = (_rh_ivs(Q, list(q) + [H]) - Q["iv"]) * 100 * w
                return np.where(np.isfinite(e), e, 20.0)
            r = least_squares(resid, near, bounds=([1e-3, 0.01, 1e-3, 0.05, -0.95], [2, 30, 2, 5, 0.95]),
                              max_nfev=20, x_scale="jac")
            x = list(r.x) + [H]
            iv = _rh_ivs(Q, x)
            part[key] = {"x": x, "rmse": _rmse(iv, Q),
                         "by_expiry": {int(round(T * 365)): _rmse(np.where(Q["T"] == T, iv, np.nan), Q) for T in Ts}}
            print("   H", H, part[key]["rmse"], flush=True)
        rows.append({"H": H, **part[key], "from": "new"})
    rh = load("rheston")
    out = {"rows": rows, "free": {"H": rh["params"]["H"], "rmse": rh["rmse"], "by_expiry": prof["best_by_expiry"]}}
    best = min(rows, key=lambda r: r["rmse"])
    out["best_H"] = best["H"]
    part.finish()
    return _json(out)


def compute_hawkes_sweep() -> dict:
    """Order flow as a Hawkes process with a power-law (Lomax) kernel, simulated by branching: the roughness
    estimator applied to the log of activity in fixed bins as the branching ratio approaches one, three seeds each;
    and tail exponents alpha = 0.6, 0.75, 0.9 at n = 0.9999 (the theory's limit is H = alpha - 1/2)."""
    T, b = 4e6, 200.0
    lags = (1, 2, 3, 5, 7, 10, 15, 20, 30, 50)
    bins = np.arange(0, T + 1, b)

    def est(n, alpha, seed):
        ev = sim.hawkes_branching_powerlaw(1.0 * (1 - n), n, alpha, 1.0, T, seed=seed)
        cnt = np.histogram(ev, bins)[0].astype(float)
        return R.log_rv_scaling(np.log(np.maximum(cnt, 1)), lags=lags)["H"], cnt, len(ev)

    sweep = []
    keep = None
    for n in (0.5, 0.9, 0.99, 0.999, 0.9999):
        Hs = []
        for s in range(3):
            H, cnt, ne = est(n, 0.6, s)
            Hs.append(H)
            if n == 0.9999 and s == 0:
                keep = cnt
        sweep.append({"n": n, "H": Hs})
    tails = []
    for alpha in (0.6, 0.75, 0.9):
        tails.append({"alpha": alpha, "H": [est(0.9999, alpha, s)[0] for s in range(3)], "theory": alpha - 0.5})
    ev, par, gen = sim.hawkes_branching_powerlaw(0.02, 0.9, 0.6, 1.0, 400.0, seed=7, return_tree=True)
    return _json({"sweep": sweep, "tails": tails, "counts_9999": keep[:20000], "bin": b,
                  "tree": {"t": ev, "parent": par, "gen": gen}})


def compute_lift_paths() -> dict:
    """One rough Heston variance path, driven by the same Brownian increments, under lifts with N = 1, 5, 20 and 50
    factors and under a fine Volterra Euler scheme with the exact kernel (cell-averaged): the pathwise distance."""
    p = load("lift")["x"]
    v0, lam, theta, nu, rho, H = p
    a = H + 0.5
    from scipy.special import gamma as Gm
    T, n, P = 0.25, 500, 200
    dt = T / n
    dW = np.random.default_rng(9).standard_normal((P, n)) * np.sqrt(dt)
    m = np.arange(1, n + 1)
    Kc = ((m * dt) ** a - ((m - 1) * dt) ** a) / (Gm(a + 1) * dt)
    V = np.empty((P, n + 1))
    V[:, 0] = v0
    inc = np.zeros((P, n))
    for k in range(1, n + 1):
        vp = np.maximum(V[:, k - 1], 0)
        inc[:, k - 1] = lam * (theta - vp) * dt + nu * np.sqrt(vp) * dW[:, k - 1]
        V[:, k] = v0 + inc[:, :k] @ Kc[:k][::-1]
    rows, paths = [], {"exact": V[0, ::2]}
    for N in (1, 5, 20, 50, 200):
        VN = R.lifted_heston_paths(v0, lam, theta, nu, H, N, T, n, dW)
        d = float(np.sqrt(np.mean((VN - V) ** 2)) / np.std(V))
        rows.append({"N": N, "dist": d})
        paths[str(N)] = VN[0, ::2]
    return _json({"rows": rows, "paths": paths, "t": np.linspace(0, T, n + 1)[::2], "x": p})


def compute_bias_map() -> dict:
    """The roughness estimator's bias map: a fractional Ornstein-Uhlenbeck log-volatility with true H from 0.05 to
    0.5 and mean-reversion half-lives from none to 5 hours, simulated every 5 minutes for 700 days and as variable
    as bitcoin's (s.d. of daily changes in log vol 0.3), measured through 5-minute realized variance exactly as
    bitcoin was: the estimate on each cell (4 seeds), and the straightness of the q = 2 scaling line."""
    n_days, m = 700, 288
    N = n_days * m
    dt = 1 / 365 / m
    Hs = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
    hls = [None, 60, 20, 7, 3, 1, 0.5, 0.2]
    part = CACHE.partial("bias_map", {"Hs": Hs, "hls": [h or 0 for h in hls], "seeds": 4})

    def straight(lv):
        e = R.log_rv_scaling(lv)
        ln, lm = np.log(e["lags"]), np.log(e["m_2.0"])
        return float(np.sqrt(np.mean((lm - np.polyval(np.polyfit(ln, lm, 1), ln)) ** 2))), e["H"]

    for H in Hs:
        for hl in hls:
            key = f"{H}/{hl}"
            if key in part:
                continue
            est, est_i, st = [], [], []
            for seed in range(4):
                x = R.fou_paths(H, None if hl is None else hl / 365, N, dt, seed=seed)
                x = x / np.std(np.diff(x.reshape(n_days, m).mean(1))) * 0.3
                vol = 0.5 * np.exp(x)
                r = vol * np.sqrt(dt) * np.random.default_rng(100 + seed).standard_normal(N)
                rv = (r * r).reshape(n_days, m).sum(1)
                s, h = straight(np.log(rv))
                est.append(h)
                st.append(s)
                est_i.append(R.log_rv_scaling(np.log((vol ** 2).reshape(n_days, m).mean(1)))["H"])
            part[key] = {"H_rv": est, "H_int": est_i, "straight": st}
        print("   H", H, flush=True)
    btc = load("roughness")
    lvb = np.log(np.asarray(btc["rv"]))
    sb, _ = straight(lvb)
    grid = [[part[f"{H}/{hl}"] for hl in hls] for H in Hs]
    out = {"Hs": Hs, "half_lives": [h if h is not None else 0 for h in hls],
           "mean": [[float(np.mean(c["H_rv"])) for c in row] for row in grid],
           "sd": [[float(np.std(c["H_rv"])) for c in row] for row in grid],
           "integrated": [[float(np.mean(c["H_int"])) for c in row] for row in grid],
           "straight": [[float(np.mean(c["straight"])) for c in row] for row in grid],
           "btc_straight": sb, "btc_H": btc["H"]}
    part.finish()
    return _json(out)


def _b2f_paths(p, xi, T, n, P, seed):
    """A two-factor Bergomi model with one driver: X_t = int (eta1 e^{-k1 (t - s)} + eta2 e^{-k2 (t - s)}) dW_s,
    v_t = xi0(t) exp(X_t - Var X_t / 2); the compensator is the discrete scheme's own variance, so E v = xi0 exactly."""
    k1, k2, e1, e2, rho = p
    g = np.random.default_rng(seed)
    dt = T / n
    dW = g.standard_normal((P, n)) * np.sqrt(dt)
    dP = g.standard_normal((P, n)) * np.sqrt(dt)
    a1, a2 = np.exp(-k1 * dt), np.exp(-k2 * dt)
    h1, h2 = np.exp(-k1 * dt / 2), np.exp(-k2 * dt / 2)
    m = np.arange(n)
    gk = e1 * np.exp(-k1 * dt * (m + 0.5)) + e2 * np.exp(-k2 * dt * (m + 0.5))
    var = np.concatenate([[0.0], np.cumsum(gk ** 2) * dt])
    t = np.linspace(0, T, n + 1)
    xv = xi(t)
    Y1 = np.zeros(P)
    Y2 = np.zeros(P)
    lnS = np.zeros(P)
    S = np.empty((n + 1, P))
    S[0] = 1.0
    v = np.full(P, xv[0])
    for k in range(n):
        lnS += np.sqrt(v) * (rho * dW[:, k] + np.sqrt(1 - rho * rho) * dP[:, k]) - 0.5 * v * dt
        Y1 = a1 * Y1 + h1 * dW[:, k]
        Y2 = a2 * Y2 + h2 * dW[:, k]
        v = xv[k + 1] * np.exp(e1 * Y1 + e2 * Y2 - 0.5 * var[k + 1])
        S[k + 1] = np.exp(lnS)
    return S


def compute_bergomi2f() -> dict:
    """A two-factor (exponential-kernel, Markovian) Bergomi model on the same 175 quotes as rough Bergomi, with
    Part 13's variance curve: (k1, k2, eta1, eta2, rho) by least squares on 20,000 paths with common random numbers,
    the evaluations recorded, then re-priced on fresh paths; its skew term structure."""
    Q = _quotes()
    n_days = int(round(Q["T"].max() * 365))
    xi = _xi_curve()
    w = np.sqrt(Q["vega"] / Q["vega"].mean())
    P = 20000
    trace = []

    def ivs(p, seed):
        S = _b2f_paths(p, xi, n_days / 365, n_days * 2, P, seed)
        return _mc_iv(S[::2], Q, n_days)

    def resid(p):
        iv = ivs(p, 3)
        trace.append({"x": list(p), "rmse": _rmse(iv, Q)})
        e = (iv - Q["iv"]) * 100 * w
        return np.where(np.isfinite(e), e, 20.0)

    r = least_squares(resid, [40.0, 1.0, 2.0, 1.0, -0.4], bounds=([5, 0.05, 0.05, 0.05, -0.95], [300, 10, 8, 6, 0.95]),
                      diff_step=0.05, max_nfev=30, x_scale=[30, 1, 1, 1, 0.3])
    iv = ivs(r.x, 11)
    nd = 183
    S = _b2f_paths(r.x, xi, nd / 365, nd * 2, 40000, 21)
    Tg = np.exp(np.linspace(np.log(3 / 365), np.log(0.5), 14))
    sk = []
    ks = np.linspace(-0.08, 0.08, 9)
    for T in Tg:
        x = S[max(1, int(round(T * 730)))]
        TT = max(1, int(round(T * 730))) / 730
        v = np.array([bs.implied_vol(float(np.mean(np.maximum((1 if k >= 0 else -1) * (x - np.exp(k)), 0))), 1.0,
                                     np.exp(k), TT, 0, 0, 1 if k >= 0 else -1) for k in ks])
        ok = np.isfinite(v)
        sk.append(float(np.polyfit(ks[ok], v[ok], 2)[1]))
    best, keep = np.inf, []
    for i, t in enumerate(trace):
        if t["rmse"] < best:
            best = t["rmse"]
            keep.append({"eval": i, **t})
    k1, k2 = r.x[0], r.x[1]
    return _json({"x": r.x, "rmse": _rmse(iv, Q), "fit_rmse": best, "curve": [t["rmse"] for t in trace], "best": keep,
                  "half_lives_days": [365 * np.log(2) / k1, 365 * np.log(2) / k2], "skew_T": Tg, "skew": sk,
                  "iv": iv, "rbergomi_rmse": load("rbergomi")["rmse"]})


def compute_pdv_replay() -> dict:
    """Guyon and Lekeufack's fit on bitcoin (``pdv``) replayed: the kernel shapes at every evaluation of the least
    squares (betas by OLS inside), thinned to the improvements."""
    days, r, vol = _pdv_data()
    split = load("pdv")["split_day"]
    have = np.isfinite(vol)
    train = have & (days < split)
    vv = np.where(have, vol, np.nan)
    trace = []

    def resid(p):
        R1, R2 = R.pdv_features(r, 1 / 365, *p, lookback=1000)
        X = np.column_stack([np.ones_like(R1), R1, np.sqrt(np.maximum(R2, 0))])[train]
        b, *_ = np.linalg.lstsq(X, vv[train], rcond=None)
        e = X @ b - vv[train]
        trace.append({"x": list(p), "r2": float(1 - np.sum(e * e) / np.sum((vv[train] - vv[train].mean()) ** 2)),
                      "mse": float(np.mean(e * e))})
        return e

    least_squares(resid, [1.5, 0.02, 1.5, 0.05], bounds=([1.01, 1e-4, 1.01, 1e-4], [5, 1.0, 5, 1.0]))
    tau = np.linspace(0, 200 / 365, 101)
    best, keep = np.inf, []
    for i, t in enumerate(trace):
        if t["mse"] < best - 1e-9:
            best = t["mse"]
            keep.append({"eval": i, **t, "K1": R.tspl_kernel(tau, t["x"][0], t["x"][1]),
                         "K2": R.tspl_kernel(tau, t["x"][2], t["x"][3])})
    return _json({"curve": [t["mse"] for t in trace], "r2_curve": [t["r2"] for t in trace], "best": keep, "tau": tau})


def compute_pdv4() -> dict:
    """The 4-factor Markovian PDV on bitcoin: each kernel a convex mix of two exponentials, so R1 and R2 are two
    exponential moving averages each; (lam_{1,0}, lam_{1,1}, theta_1, lam_{2,0}, lam_{2,1}, theta_2) by least squares,
    betas by OLS, fitted on 2021-2023 and tested on 2024-2025 like ``pdv``."""
    days, r, vol = _pdv_data()
    p0 = load("pdv")
    split = p0["split_day"]
    have = np.isfinite(vol)
    train, test = have & (days < split), have & (days >= split)
    vv = np.where(have, vol, np.nan)
    dt = 1 / 365

    def design(p):
        R1 = R.pdv4_features(r, dt, p[0], p[1], p[2], power=1)
        R2 = R.pdv4_features(r, dt, p[3], p[4], p[5], power=2)
        return np.column_stack([np.ones_like(R1), R1, np.sqrt(np.maximum(R2, 0))])

    def resid(p):
        X = design(p)[train]
        b, *_ = np.linalg.lstsq(X, vv[train], rcond=None)
        return X @ b - vv[train]

    f = least_squares(resid, [50.0, 10.0, 0.3, 50.0, 5.0, 0.5],
                      bounds=([1, 0.05, 0, 1, 0.05, 0], [500, 100, 1, 500, 100, 1]), x_scale=[50, 5, 0.3, 50, 5, 0.3])
    X = design(f.x)
    b, *_ = np.linalg.lstsq(X[train], vv[train], rcond=None)
    pred = X @ b

    def r2(m):
        y = vv[m]
        return float(1 - np.sum((pred[m] - y) ** 2) / np.sum((y - y.mean()) ** 2))
    return _json({"x": f.x, "beta": b, "r2_train": r2(train), "r2_test": r2(test), "tspl_train": p0["r2_train"],
                  "tspl_test": p0["r2_test"], "half_lives_days": [365 * np.log(2) / f.x[i] for i in (0, 1, 3, 4)]})


def _spx_data():
    kf = data.ken_french_daily("2025-12-31")
    d = kf["date"]
    r = np.log1p(kf["mkt"])
    vx = data.fred("VIXCLS", "1990-01-02", "2025-12-31")
    vix = dict(zip(vx["date"].tolist(), (vx["value"] / 100).tolist()))
    m = d >= 19860101
    d, r = d[m], r[m]
    return d, r, np.array([vix.get(int(x), np.nan) for x in d])


def compute_pdv_spx() -> dict:
    """Guyon and Lekeufack's PDV where they fitted it: the VIX from the US market's own daily returns (Ken French's
    value-weighted market, a stand-in for the S&P 500), fitted 2000-2018 and tested 2019-2025, the evaluations
    recorded; the crisis days."""
    d, r, vol = _spx_data()
    have = np.isfinite(vol)
    train = have & (d >= 20000101) & (d < 20190101)
    test = have & (d >= 20190101)
    dt = 1 / 252
    trace = []

    def design(p):
        R1, R2 = R.pdv_features(r, dt, *p, lookback=1000)
        return np.column_stack([np.ones_like(R1), R1, np.sqrt(np.maximum(R2, 0))])

    def resid(p):
        X = design(p)[train]
        b, *_ = np.linalg.lstsq(X, vol[train], rcond=None)
        e = X @ b - vol[train]
        trace.append({"x": list(p), "mse": float(np.mean(e * e))})
        return e

    lo = [1.001, 1e-4, 1.001, 1e-4]
    f = least_squares(resid, [1.5, 0.02, 1.5, 0.05], bounds=(lo, [5, 1.0, 5, 1.0]))
    X = design(f.x)
    b, *_ = np.linalg.lstsq(X[train], vol[train], rcond=None)
    pred = X @ b
    rv = np.sqrt(np.convolve(r * r, np.ones(21), "full")[: len(r)] / 21 * 252)
    Xb = np.column_stack([np.ones_like(rv), rv])
    bb, *_ = np.linalg.lstsq(Xb[train], vol[train], rcond=None)
    base = Xb @ bb

    def r2(m, p):
        y = vol[m]
        return float(1 - np.sum((p[m] - y) ** 2) / np.sum((y - y.mean()) ** 2))
    days = {}
    for D in (20080929, 20081120, 20100520, 20150824, 20180205, 20200316, 20240802, 20240805, 20240806):
        k = int(np.where(d == D)[0][0])
        days[str(D)] = {"vix": vol[k], "pdv": pred[k], "base": base[k]}
    keep = have & (d >= 19900101)
    best, kk = np.inf, []
    for i, t in enumerate(trace):
        if t["mse"] < best - 1e-12:
            best = t["mse"]
            kk.append({"eval": i, **t})
    contrib = {"trend": float(np.std(b[1] * X[have, 1])), "activity": float(np.std(b[2] * X[have, 2]))}
    return _json({"x": f.x, "beta": b, "at_bound": bool(f.x[0] < lo[0] + 1e-3 or f.x[2] < lo[2] + 1e-3),
                  "r2_train": r2(train, pred), "r2_test": r2(test, pred), "r2_base_train": r2(train, base),
                  "r2_base_test": r2(test, base), "contrib": contrib, "days": days, "date": d[keep], "vix": vol[keep],
                  "pred": pred[keep], "curve": [t["mse"] for t in trace], "best": kk})


def compute_crisis_aug2024() -> dict:
    """5 August 2024: the VIX and its PDV prediction; DVOL hour by hour; bitcoin's realized volatility day by day and
    its PDV prediction; the Surface's skew term structure the week before and the week after."""
    ps = load("pdv_spx")
    dv = data.deribit_dvol("2024-07", "2024-08", resolution=3600)
    t = np.asarray(dv["time"])
    lo, hi = datetime(2024, 7, 29, tzinfo=timezone.utc).timestamp(), datetime(2024, 8, 10, tzinfo=timezone.utc).timestamp()
    m = (t >= lo) & (t < hi)
    days, rv = _daily_rv()
    d0, d1 = int(lo // 86400), int(hi // 86400)
    sel = (days >= d0) & (days < d1)
    p = load("pdv")
    pd_ = np.asarray(p["days"])
    btc = {}
    for D in range(d0, d1):
        k = np.where(pd_ == D)[0]
        if len(k):
            btc[str(D)] = {"dvol": p["vol"][int(k[0])], "pdv": p["pred"][int(k[0])]}
    sw = {w["day"]: w for w in load("skew_weekly")["weeks"]}
    nk = data.fred("NIKKEI225", "1949-05-01", "2025-12-31")
    k = int(np.where(nk["date"] == 20240805)[0][0])
    nikkei = float(nk["value"][k] / nk["value"][k - 1] - 1)
    return _json({"nikkei_0805": nikkei, "vix_days": ps["days"], "dvol_t": t[m], "dvol_close": np.asarray(dv["close"])[m],
                  "dvol_high": np.asarray(dv["high"])[m], "btc_rv_days": days[sel], "btc_rv": np.sqrt(rv[sel]),
                  "btc_pdv": btc, "skew_before": sw.get("2024-07-31"), "skew_after": sw.get("2024-08-07")})


def _zumbach(lnS, w=20, step=5):
    """The weak Zumbach effect: the correlation of past squared trend with future realized variance (forward)
    against that of past realized variance with future squared trend (backward), windows of ``w`` days."""
    lnS = np.atleast_2d(lnS)
    r = np.diff(lnS, axis=1)
    f, bk = [], []
    for t in range(w, r.shape[1] - w + 1, step):
        Rp = r[:, t - w: t].sum(1)
        RVp = (r[:, t - w: t] ** 2).sum(1)
        Rf = r[:, t: t + w].sum(1)
        RVf = (r[:, t: t + w] ** 2).sum(1)
        f.append(np.column_stack([Rp ** 2, RVf]))
        bk.append(np.column_stack([RVp, Rf ** 2]))
    f, bk = np.concatenate(f), np.concatenate(bk)
    return float(np.corrcoef(f.T)[0, 1]), float(np.corrcoef(bk.T)[0, 1])


def compute_qrh_sim() -> dict:
    """The quadratic rough Heston model with Gatheral, Jusselin and Rosenbaum's (2020) calibrated parameters
    (alpha = 0.51, lambda = 1.2, a = 0.384, b = 0.095, c = 0.0025, Z0 = 0.1; eta = 1, not among the calibrated
    six), lifted to 10 factors, daily steps for a year: paths for the picture, and the weak Zumbach effect measured on
    the paths, on rough Bergomi (no feedback) and on the US market 1990-2025."""
    alpha, lam, a, b, c, Z0, eta = 0.51, 1.2, 0.384, 0.095, 0.0025, 0.1, 1.0
    H = alpha - 0.5
    S, V, Z = R.qrh_paths(a, b, c, lam, lam * eta, H, Z0, 1.0, 252, 10000, N=10, seed=3, theta0=0.0)
    fq, bq = _zumbach(np.log(S))
    rb = load("rbergomi")
    Sr = R.rbergomi_paths(*rb["x"], 0.04, 1.0, 252, 10000, seed=4)
    fr, br = _zumbach(np.log(Sr.T))
    d, r, _ = _spx_data()
    m = d >= 19900101
    fs, bs_ = _zumbach(np.cumsum(r[m])[None, :])
    return _json({"params": {"alpha": alpha, "lambda": lam, "a": a, "b": b, "c": c, "Z0": Z0, "eta": eta},
                  "paths": {"S": S[:4, ::2], "V": V[:4, ::2], "Z": Z[:4, ::2]}, "t": np.linspace(0, 1, 253)[::2],
                  "vol_mean": float(np.sqrt(V).mean()), "zumbach": {"qRH": [fq, bq], "rBergomi": [fr, br],
                                                                    "market": [fs, bs_]}})


def compute_joint_bounds() -> dict:
    """A martingale-transport illustration in the spirit of Guyon's joint calibration: the lowest and highest price
    any martingale consistent with the Surface's 51-day and 107-day smiles allows for a forward-start claim
    |log(S2 / S1)|, by entropic martingale transport (Part 9's House code, both signs, with its trace) and by linear
    programming; rough Bergomi's value of the same claim sits inside."""
    from explainer.quant.house import arbitrage as A
    Q = surface.build(surface.DAYS[0])
    exps = sorted(np.unique(Q["T"]))
    T1 = min(exps, key=lambda T: abs(T - 51 / 365))
    T2 = min(exps, key=lambda T: abs(T - 107 / 365))
    marg = []
    for T, n in ((T1, 60), (T2, 80)):
        m = (Q["T"] == T) & (np.abs(Q["k"]) < 0.6)
        p = smile.fit_svi(Q["k"][m], Q["iv"][m] ** 2 * T, weights=Q["vega"][m])
        sd = np.sqrt(p["a"] + p["b"] * 0.3)
        Kg = np.linspace(np.exp(-4 * max(sd, 0.25)), np.exp(3 * max(sd, 0.25)), 400)
        q = smile.risk_neutral_density(p, 1.0, T, Kg)
        q /= q.sum()
        cdf = np.cumsum(q)
        edges = np.interp(np.linspace(0, 1, n + 1), cdf, Kg)
        xs = 0.5 * (edges[1:] + edges[:-1])
        ws = np.diff(np.interp(edges, Kg, cdf))
        ws = np.maximum(ws, 1e-12)
        ws /= ws.sum()
        marg.append((xs, ws))
    (x, mu), (y, nu) = marg
    y = A.convex_order_fix(x, mu, y, nu)
    cost = lambda s, t: abs(np.log(t / s))  # noqa: E731
    out = {"T1": T1, "T2": T2, "x": x, "mu": mu, "y": y, "nu": nu}
    for name, sign in (("upper", -1.0), ("lower", 1.0)):
        e = A.entropic_mot(x, mu, y, nu, cost, eps=0.005, iters=2000, sign=sign, log_every=20, newton=5)
        out[name] = {"value": e["value"], "trace": e["trace"]}
    try:
        lp = A.mot_bounds(x, mu, y, nu, cost)
        out["lp"] = {"lower": lp["lower"], "upper": lp["upper"]}
    except ValueError as err:
        out["lp"] = {"error": str(err)}
    rb = load("rbergomi")
    xi = _xi_curve()
    n2 = int(round(T2 * 365))
    S = R.rbergomi_paths(*rb["x"], xi, n2 / 365, n2, 40000, seed=13)
    n1 = int(round(T1 * 365))
    out["rbergomi"] = float(np.mean(np.abs(np.log(S[n2] / S[n1]))))
    out["independent"] = float(np.sum(mu[:, None] * nu[None, :] * np.abs(np.log(y[None, :] / x[:, None]))))
    return _json(out)


def compute_sigvol() -> dict:
    """A signature volatility model (Cuchiero, Gazzani and Svaluto-Ferro 2023) on the Surface: sigma_t is linear in
    the depth-3 signature of (t, W_t), so log S_T is quadratic in the parameters; the 15 weights and rho by least
    squares on 10,000 simulated paths (common random numbers, evaluations recorded), re-priced on a fresh set."""
    Q = _quotes()
    w = np.sqrt(Q["vega"] / Q["vega"].mean())
    Ts = np.unique(Q["T"])
    spd = 4
    idx = [int(round(T * 365 * spd)) for T in Ts]
    n = max(idx)
    dt = 1 / 365 / spd
    P = 10000
    sets = {}
    for seed in (1, 2):
        sets[seed], words = R.sigvol_features(idx, n, dt, P, depth=3, seed=seed)
    d = len(words)

    def ivs(p, seed):
        ell, rho = np.asarray(p[:d]), float(p[d])
        out = np.full(len(Q["K"]), np.nan)
        for T, i in zip(Ts, idx):
            f = sets[seed][i]
            ST = np.exp(R.sigvol_logS(ell, rho, f["AW"], f["AP"], f["B"]))
            ST = ST / ST.mean()   # the sample martingale correction
            m = Q["T"] == T
            for j in np.flatnonzero(m):
                K = Q["K"][j] / Q["F"][j]
                cp = int(Q["cp"][j])
                out[j] = bs.implied_vol(float(np.mean(np.maximum(cp * (ST - K), 0))), 1.0, K, T, 0, 0, cp)
        return out

    trace = []

    def resid(p):
        iv = ivs(p, 1)
        trace.append({"x": list(p), "rmse": _rmse(iv, Q)})
        e = (iv - Q["iv"]) * 100 * w
        return np.where(np.isfinite(e), e, 20.0)

    x0 = np.zeros(d + 1)
    x0[0] = 0.48
    x0[d] = -0.3
    lo = np.r_[np.full(d, -30.0), -0.95]
    hi = np.r_[np.full(d, 30.0), 0.95]
    lo[0] = 0.05
    r = least_squares(resid, x0, bounds=(lo, hi), max_nfev=60, diff_step=1e-3)
    iv_in, iv_out = ivs(r.x, 1), ivs(r.x, 2)
    best, keep = np.inf, []
    for i, t in enumerate(trace):
        if t["rmse"] < best - 1e-6:
            best = t["rmse"]
            keep.append({"eval": i, "x": t["x"], "rmse": t["rmse"], "iv": ivs(t["x"], 1)})
    # one path's signature and volatility, for the picture
    g = np.random.default_rng(5)
    m_ = 200
    dtp = 0.5 / m_
    Wp = np.concatenate([[0], np.cumsum(g.standard_normal(m_) * np.sqrt(dtp))])
    tp = np.linspace(0, 0.5, m_ + 1)
    sig = [np.r_[1.0, np.zeros(d - 1)]]
    L1, L2, L3 = np.zeros(2), np.zeros((2, 2)), np.zeros((2, 2, 2))
    for k in range(m_):
        D = np.array([dtp, Wp[k + 1] - Wp[k]])
        DD = np.outer(D, D)
        L3 = L3 + np.einsum("ij,k->ijk", L2, D) + np.einsum("i,jk->ijk", L1, DD) / 2 + np.einsum("ij,k->ijk", DD, D) / 6
        L2 = L2 + np.outer(L1, D) + DD / 2
        L1 = L1 + D
        row = [1.0]
        for wd in words[1:]:
            row.append(L1[wd[0]] if len(wd) == 1 else L2[wd] if len(wd) == 2 else L3[wd])
        sig.append(np.array(row))
    sig = np.array(sig)
    return _json({"x": r.x, "words": ["".join("tW"[i] for i in wd) for wd in words], "rmse_in": _rmse(iv_in, Q),
                  "rmse_out": _rmse(iv_out, Q), "curve": [t["rmse"] for t in trace], "best": keep, "paths": P,
                  "iv": iv_out, "path": {"t": tp, "W": Wp, "sig": sig, "vol": sig @ r.x[:d]},
                  "rbergomi_rmse": load("rbergomi")["rmse"]})


def compute_calib_speed() -> dict:
    """The wall time of one evaluation of each model on the Surface's 175 quotes, on this (shared) machine: rough
    Bergomi by Monte Carlo (20,000 paths), rough Heston by Adams and COS, the lifted Heston (N = 20) by its Riccati
    system and COS, the signature model, and Part 17's neural surrogate (from its own cache)."""
    import time
    Q = _quotes()
    n_days = int(round(Q["T"].max() * 365))
    xi = _xi_curve()
    Ts = np.unique(Q["T"])

    def med(f, k=3):
        ts = []
        for _ in range(k):
            t0 = time.perf_counter()
            f()
            ts.append(time.perf_counter() - t0)
        return float(np.median(ts))
    rb = load("rbergomi")["x"]
    px = next(r for r in load("rprofile")["rows"] if abs(r["H"] - 0.1) < 1e-9)["x"]
    t_rb = med(lambda: _mc_iv(R.rbergomi_paths(*rb, xi, n_days / 365, n_days, 20000, seed=3), Q, n_days))
    t_rh = med(lambda: _rh_ivs(Q, px))

    def lifted():
        for T in Ts:
            m = Q["T"] == T
            F = float(Q["F"][m][0])
            cf = lambda u, TT: R.lifted_heston_cf(u, TT, *px, N=20, n_steps=100)  # noqa: E731
            sv.cos_price(cf, F, Q["K"][m], T, Q["cp"][m], N=192, L=14)
    t_lh = med(lifted)
    c17 = Cache("quant17").load("calib")
    return _json({"rBergomi MC": t_rb, "rough Heston": t_rh, "lifted Heston": t_lh,
                  "neural (Part 17)": c17["t_net_surface"], "rBergomi MC (Part 17)": c17["t_mc_surface"]})

ITEMS = {"skew": compute_skew, "roughness": compute_roughness, "artefact": compute_artefact,
         "rbergomi": compute_rbergomi, "rbskew": compute_rbskew, "rheston": compute_rheston, "rprofile": compute_rprofile, "lift": compute_lift, "hawkes": compute_hawkes,
         "pdv": compute_pdv, "envelope": compute_envelope,
         "skew_weekly": compute_skew_weekly, "skew_models": compute_skew_models, "roughness_2018": compute_roughness_2018,
         "rfsv_forecast": compute_rfsv_forecast, "rb_replay": compute_rb_replay, "hybrid_check": compute_hybrid_check,
         "adams_conv": compute_adams_conv, "rh_profile9": compute_rh_profile9, "hawkes_sweep": compute_hawkes_sweep,
         "lift_paths": compute_lift_paths, "bias_map": compute_bias_map, "bergomi2f": compute_bergomi2f,
         "pdv_replay": compute_pdv_replay, "pdv4": compute_pdv4, "pdv_spx": compute_pdv_spx,
         "crisis_aug2024": compute_crisis_aug2024, "qrh_sim": compute_qrh_sim, "joint_bounds": compute_joint_bounds,
         "sigvol": compute_sigvol, "calib_speed": compute_calib_speed}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
