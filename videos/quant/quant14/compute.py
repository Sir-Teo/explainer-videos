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

from datetime import datetime, timezone

import numpy as np
from scipy.optimize import least_squares

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, pit, rough as R, sim, stochvol as sv, surface

CACHE = Cache("quant14")
load = CACHE.load
Q13 = Cache("quant13")


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


ITEMS = {"skew": compute_skew, "roughness": compute_roughness, "artefact": compute_artefact,
         "rbergomi": compute_rbergomi, "rheston": compute_rheston, "rprofile": compute_rprofile, "lift": compute_lift, "hawkes": compute_hawkes,
         "pdv": compute_pdv, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
