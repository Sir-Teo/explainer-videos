"""Every number in Part 5 (Stochastic Calculus), computed and cached in .cache/quant5/.

    python -m videos.quant.quant5.compute [items] [--force]

Research window: to December 2020.  Items (seeded; seconds to a few minutes):

* ``variation``  Brownian motion's variations on finer and finer grids: the sum of |dW| grows without bound, the sum
                 of dW^2 settles at T, the sum of |dW|^3 vanishes;
* ``signature``  Bitcoin's realized variance in 2020 against the sampling interval (1 minute to 1 day): the
                 volatility signature plot (Andersen, Bollerslev, Diebold and Labys 2000);
* ``ito``        the integral of W dW by left points (Itô) and midpoints (Stratonovich) on refining grids;
* ``orders``     strong and weak errors of Euler and Milstein on GBM;
* ``rates``      the 3-month Treasury bill, 1954-2020 (FRED DTB3): Vasicek (OU) and CIR fitted by regression;
                 simulated paths from both;
* ``girsanov``   a deep out-of-the-money digital by Monte Carlo, plain and with the drift shifted by Girsanov
                 (importance sampling): the variance ratio;
* ``stoploss``   the stop-loss start-gain hedge (Carr and Jarrow 1990): its error against the local time at the
                 strike, on finer and finer rebalancing;
* ``jumps``      Bitcoin's hourly returns 2018-2020: jumps flagged against bipower variation; Merton paths;
* ``hawkes``     a Hawkes process fitted to the times of Bitcoin's large hourly moves (2018-2020): the branching ratio;
* ``rough``      the Hurst exponent of Bitcoin's log realized volatility (daily, from 5-minute returns, 2019-2020),
                 against simulated fBM;
* ``fbm``        fractional Brownian paths at H = 0.1, 0.5, 0.9 for the pictures;
* ``envelope``   registers this part's tests (trial counter).
"""

from __future__ import annotations

import inspect
from datetime import datetime, timezone

import numpy as np
from scipy.stats import norm

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, pit, sim

CACHE = Cache("quant5")
load = CACHE.load


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


def _btc(interval, start, end):
    b = data.binance_klines("BTCUSDT", interval, start, end)
    t = np.asarray(b["time"], float)
    return t, np.asarray(b["close"], float)


# ---------------------------------------------------------------------------
def compute_variation() -> dict:
    rng = np.random.default_rng(1)
    nmax = 2 ** 16
    dW = rng.standard_normal(nmax) * np.sqrt(1.0 / nmax)
    ns = [2 ** k for k in range(2, 17)]
    v1, v2, v3 = [], [], []
    for n in ns:
        d = dW.reshape(n, nmax // n).sum(axis=1)
        v1.append(float(np.abs(d).sum()))
        v2.append(float((d ** 2).sum()))
        v3.append(float((np.abs(d) ** 3).sum()))
    W = np.concatenate([[0.0], np.cumsum(dW)])
    return _json({"n": ns, "v1": v1, "v2": v2, "v3": v3, "W": W[:: nmax // 1024]})


# ---------------------------------------------------------------------------
def compute_signature() -> dict:
    """Realized variance of 2020 (one calendar year, so the sum is already annual) from returns sampled every m minutes
    across the whole year, averaged over up to 30 starting offsets (subsampling, Zhang, Mykland and Ait-Sahalia 2005)."""
    t, c = _btc("1m", "2020-01", "2020-12")
    lc = np.log(c)
    years = (t[-1] - t[0]) / (365.25 * 86400)
    mins, rvs = [], []
    for m in (1, 2, 5, 10, 15, 30, 60, 120, 240, 480, 1440):
        offs = np.unique(np.linspace(0, m - 1, min(m, 30)).astype(int))
        rv = np.mean([np.sum(np.diff(lc[o::m]) ** 2) for o in offs]) / years
        mins.append(m)
        rvs.append(float(rv))
    return _json({"minutes": mins, "rv_annual": rvs, "vol_annual": list(np.sqrt(rvs)), "years": float(years)})


# ---------------------------------------------------------------------------
def compute_ito() -> dict:
    rng = np.random.default_rng(3)
    nmax = 2 ** 14
    dW = rng.standard_normal(nmax) * np.sqrt(1.0 / nmax)
    W = np.concatenate([[0.0], np.cumsum(dW)])
    WT = W[-1]
    rows = []
    for n in [4, 16, 64, 256, 1024, 4096, 16384]:
        Wn = W[:: nmax // n]
        d = np.diff(Wn)
        left = float(np.sum(Wn[:-1] * d))
        mid = float(np.sum(0.5 * (Wn[:-1] + Wn[1:]) * d))
        rows.append({"n": n, "ito": left, "strat": mid})
    return _json({"rows": rows, "WT": float(WT), "ito_limit": float((WT ** 2 - 1) / 2), "strat_limit": float(WT ** 2 / 2),
                  "W": W[:: nmax // 512]})


# ---------------------------------------------------------------------------
def compute_orders() -> dict:
    return _json(sim.scheme_orders(n_paths=20000))


# ---------------------------------------------------------------------------
def compute_rates() -> dict:
    f = data.fred("DTB3", start="1954-01-01", through="2025-12-31")
    d, v = pit.research(f["date"], f["value"])
    ym = d // 100
    months = np.unique(ym)
    r = np.array([v[ym == m].mean() for m in months]) / 100
    t = months // 100 + (months % 100 - 0.5) / 12
    dt = 1 / 12
    # Vasicek: r_{t+dt} = a + b r_t + e  =>  kappa = -ln b / dt, theta = a / (1 - b)
    x, y = r[:-1], r[1:]
    b, a = np.polyfit(x, y, 1)
    res = y - (a + b * x)
    kappa = -np.log(b) / dt
    theta = a / (1 - b)
    sigma = res.std() * np.sqrt(2 * kappa / (1 - b ** 2))
    # CIR: divide by sqrt(r) so the residuals have constant variance
    m = x > 1e-4
    sx = np.sqrt(x[m])
    A = np.column_stack([1 / sx, sx])
    coef, *_ = np.linalg.lstsq(A, y[m] / sx, rcond=None)
    res_c = y[m] / sx - A @ coef
    bc = coef[1]
    kc = -np.log(bc) / dt
    thc = coef[0] / (1 - bc)
    sc = res_c.std() / np.sqrt(dt)
    ou = sim.ou_exact(r[0], kappa, theta, sigma, len(r) / 12, len(r) - 1, 3, seed=5)
    ci = sim.cir_exact(r[0], kc, thc, sc, len(r) / 12, len(r) - 1, 3, seed=5)
    return _json({"t": t, "r": r, "vasicek": {"kappa": kappa, "theta": theta, "sigma": sigma, "half_life": np.log(2) / kappa},
                  "cir": {"kappa": kc, "theta": thc, "sigma": sc, "feller": 2 * kc * thc / sc ** 2},
                  "ou_paths": ou, "cir_paths": ci, "frac_neg_ou": float(np.mean(sim.ou_exact(r[0], kappa, theta, sigma,
                                                                                                 len(r) / 12, len(r) - 1,
                                                                                                 2000, seed=6) < 0))})


# ---------------------------------------------------------------------------
def compute_girsanov() -> dict:
    S0, K, T, sigma, r = 100.0, 160.0, 1.0, 0.2, 0.0
    exact = float(np.exp(-r * T) * norm.cdf(bs.d1_d2(S0, K, T, sigma, r)[1]))
    rng = np.random.default_rng(9)
    n = 20000
    Z = rng.standard_normal(n)
    plain = (S0 * np.exp(-0.5 * sigma ** 2 * T + sigma * np.sqrt(T) * Z) > K).astype(float)
    # shift the Brownian drift by theta so the mean path ends at K; reweight by the likelihood ratio
    theta = (np.log(K / S0) + 0.5 * sigma ** 2 * T) / (sigma * T)
    Zs = Z + theta * np.sqrt(T)
    w = np.exp(-theta * np.sqrt(T) * Zs + 0.5 * theta ** 2 * T)
    shifted = (S0 * np.exp(-0.5 * sigma ** 2 * T + sigma * np.sqrt(T) * Zs) > K) * w
    return _json({"exact": exact, "plain_mean": plain.mean(), "plain_se": plain.std() / np.sqrt(n),
                  "is_mean": shifted.mean(), "is_se": shifted.std() / np.sqrt(n), "n": n, "theta": theta,
                  "var_ratio": float(plain.var() / shifted.var()), "hits_plain": int(plain.sum()),
                  "hits_is": int((shifted > 0).sum()), "S_plain": (S0 * np.exp(-0.5 * sigma ** 2 * T + sigma * np.sqrt(T) * Z[:400])),
                  "S_is": (S0 * np.exp(-0.5 * sigma ** 2 * T + sigma * np.sqrt(T) * Zs[:400])), "w_is": w[:400]})


# ---------------------------------------------------------------------------
def compute_stoploss() -> dict:
    """Hold one share whenever S > K, none otherwise (Carr and Jarrow 1990), r = 0, rebalanced on a grid of n steps.
    Terminal hedge value V_T = max(S_0 - K, 0) + sum 1{S_k > K}(S_{k+1} - S_k); the error against (S_T - K)^+ is minus
    the local-time term, which does not vanish as the grid is refined."""
    S0, K, T, sigma = 100.0, 100.0, 1.0, 0.2
    n_paths = 4000
    out = []
    for n in (13, 52, 252, 1000, 4000):
        dW, W = sim.brownian(T, n, n_paths, seed=11)
        tt = np.linspace(0, T, n + 1)
        S = S0 * np.exp(-0.5 * sigma ** 2 * tt + sigma * W)
        hold = (S[:, :-1] > K).astype(float)
        V = max(S0 - K, 0) + np.sum(hold * np.diff(S, axis=1), axis=1)
        err = (np.maximum(S[:, -1] - K, 0) - V)
        out.append({"n": n, "mean_err": float(err.mean()), "sd_err": float(err.std())})
    # the theory: E[(S_T - K)^+] - (S_0 - K)^+ = E[1/2 L_T^K] = the call's time value at the money
    call = float(bs.price(S0, K, T, sigma, 0.0, 0.0, 1))
    return _json({"rows": out, "call": call, "intrinsic": max(S0 - K, 0)})


# ---------------------------------------------------------------------------
def compute_jumps() -> dict:
    t, c = _btc("1h", "2018-01", "2020-12")
    r = np.diff(np.log(c))
    tt = t[1:]
    # local scale: bipower variation over the previous 7 days (robust to jumps), known before the hour
    w = 24 * 7
    absr = np.abs(r)
    bp = np.full(len(r), np.nan)
    prod = absr[1:] * absr[:-1]
    cs = np.concatenate([[0.0], np.cumsum(prod)])
    for i in range(w + 1, len(r)):
        bp[i] = (np.pi / 2) * (cs[i - 1] - cs[i - 1 - w]) / w
    z = r / np.sqrt(bp)
    flag = np.abs(z) > 5
    years = np.array([datetime.fromtimestamp(x, tz=timezone.utc).year for x in tt])
    per_year = {int(y): int(flag[years == y].sum()) for y in (2018, 2019, 2020)}
    share = float(np.nansum(r[flag] ** 2) / np.nansum(r ** 2))
    gauss_expected = float(2 * norm.sf(5) * np.isfinite(z).sum())
    paths = sim.merton_jumps(1.0, 0.0, 0.5, 6.0, -0.05, 0.08, 1.0, 365, 6, seed=12)
    return _json({"per_year": per_year, "n_jumps": int(flag.sum()), "n_hours": int(np.isfinite(z).sum()),
                  "share_of_variance": share, "gauss_expected": gauss_expected,
                  "z_hist": np.histogram(np.clip(z[np.isfinite(z)], -12, 12), np.linspace(-12, 12, 97))[0],
                  "z_edges": np.linspace(-12, 12, 97), "merton_paths": paths,
                  "t_flags": tt[flag], "r_flags": r[flag]})


# ---------------------------------------------------------------------------
def compute_hawkes() -> dict:
    t, c = _btc("1h", "2018-01", "2020-12")
    r = np.diff(np.log(c))
    tt = (t[1:] - t[1]) / 86400.0  # days
    w = 24 * 30
    sd = np.full(len(r), np.nan)
    cs = np.concatenate([[0.0], np.cumsum(r ** 2)])
    for i in range(w, len(r)):
        sd[i] = np.sqrt((cs[i] - cs[i - w]) / w)
    big = np.abs(r) > 4 * sd
    ev = tt[big]
    T = float(tt[-1])
    fit = sim.hawkes_fit(ev, T, x0=[len(ev) / T * 0.5, 0.5, 1.0])
    grid = np.linspace(0, T, 2000)
    lam = sim.hawkes_intensity(ev, fit["mu"], fit["alpha"], fit["beta"], grid)
    simev = sim.hawkes_thinning(0.2, 1.4, 2.0, 200.0, seed=13)
    sgrid = np.linspace(0, 200, 1500)
    slam = sim.hawkes_intensity(simev, 0.2, 1.4, 2.0, sgrid)
    return _json({"fit": fit, "events": ev, "T": T, "grid": grid, "lam": lam, "start": 20180101,
                  "sim_events": simev, "sim_grid": sgrid, "sim_lam": slam,
                  "half_life_hours": float(np.log(2) / fit["beta"] * 24)})


# ---------------------------------------------------------------------------
def compute_rough() -> dict:
    t, c = _btc("1m", "2019-01", "2020-12")
    day = (t // 86400).astype(int)
    lc = np.log(c)
    days, rv = [], []
    for dd in np.unique(day):
        x = lc[day == dd][::5]
        if len(x) > 200:
            days.append(dd)
            rv.append(np.sum(np.diff(x) ** 2))
    lv = 0.5 * np.log(np.asarray(rv))
    h = sim.hurst_from_increments(lv)
    fb = {}
    for H in (0.1, 0.5):
        B = sim.fbm(H, len(lv) - 1, n_paths=1, seed=14)[0]
        fb[str(H)] = sim.hurst_from_increments(B)["H"]
    return _json({"days": np.asarray(days) * 86400, "log_vol": lv, "hurst": h, "fbm_check": fb,
                  "n_days": int(len(lv))})


# ---------------------------------------------------------------------------
def compute_fbm() -> dict:
    out = {}
    for H in (0.1, 0.5, 0.9):
        out[str(H)] = sim.fbm(H, 1000, n_paths=1, seed=15)[0]
    return _json(out)


# ---------------------------------------------------------------------------
def compute_envelope() -> dict:
    reg = {"btc_hawkes_large_moves": pit.register("btc_hawkes_large_moves", inspect.getsource(compute_hawkes),
                                                  {"threshold": "4 x 30-day rolling sd", "data": "BTCUSDT 1h 2018-2020"},
                                                  trials=1),
           "btc_rough_hurst": pit.register("btc_rough_hurst", inspect.getsource(compute_rough),
                                           {"rv": "5-minute, daily", "data": "BTCUSDT 1m 2019-2020"}, trials=1)}
    return _json({"registered": reg, "trials": pit.trials_so_far()})


ITEMS = {"variation": compute_variation, "signature": compute_signature, "ito": compute_ito, "orders": compute_orders,
         "rates": compute_rates, "girsanov": compute_girsanov, "stoploss": compute_stoploss, "jumps": compute_jumps,
         "hawkes": compute_hawkes, "rough": compute_rough, "fbm": compute_fbm, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
