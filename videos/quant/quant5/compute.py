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
from explainer.quant.house import pit as _pit  # noqa: E402
load = _pit.counted(CACHE.load, 5)  # the series' trial counter as of this part


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
    for n in [4, 16, 64, 256, 1024, 4096, 8192]:
        st = nmax // n
        Wn = W[::st]
        d = np.diff(Wn)
        left = float(np.sum(Wn[:-1] * d))
        mid = float(np.sum(W[st // 2::st][:n] * d))  # W at the midpoint in time of each step
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
        if n == 4000:
            # half the local time at K, by the occupation formula: (1/4 eps) * int 1{|S - K| < eps} d<S>
            eps = 0.5
            dqv = (sigma * S[:, :-1]) ** 2 * (T / n)
            half_L = np.sum((np.abs(S[:, :-1] - K) < eps) * dqv, axis=1) / (4 * eps)
            scatter = {"err": err[:600], "half_L": half_L[:600],
                       "corr": float(np.corrcoef(err, half_L)[0, 1]), "mean_half_L": float(half_L.mean())}
            one = {"S": S[0], "half_L": np.concatenate([[0.0], np.cumsum((np.abs(S[0, :-1] - K) < eps) * dqv[0])]) / (4 * eps)}
    # the theory: E[(S_T - K)^+] - (S_0 - K)^+ = E[1/2 L_T^K] = the call's time value at the money
    call = float(bs.price(S0, K, T, sigma, 0.0, 0.0, 1))
    return _json({"rows": out, "call": call, "intrinsic": max(S0 - K, 0), "scatter": scatter, "one": one})


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


# ===========================================================================
# The second pass (November 2026): constructions, proofs checked by simulation, labs and replays
# ===========================================================================
def _thin(a, k):
    a = np.asarray(a)
    idx = np.unique(np.linspace(0, len(a) - 1, k).astype(int))
    return a[idx]


def compute_construct() -> dict:
    """Donsker with three step laws (coin, uniform, skewed two-point; all mean 0, variance 1) from the same seed, at
    n = 16, 128, 4096; and Lévy's midpoint construction to level 10."""
    laws = {}
    for name in ("coin", "uniform", "skewed"):
        rng = np.random.default_rng(21)
        u = rng.random(4096)
        if name == "coin":
            x = np.where(u < 0.5, -1.0, 1.0)
        elif name == "uniform":
            x = (u - 0.5) * np.sqrt(12)
        else:
            x = np.where(u < 0.2, 2.0, -0.5)  # mean 0, variance 1, skewed
        laws[name] = {str(n): np.concatenate([[0.0], np.cumsum(x[:n])]) / np.sqrt(n) for n in (16, 128, 4096)}
    lv = sim.levy_construction(10, seed=22)
    # the bridge's variance, checked: midpoints of level 1 over 20,000 constructions, given the endpoints
    lv1 = np.array([sim.levy_construction(1, seed=s)[1] for s in range(20000)])
    mids, ends = lv1[:, 1], lv1[:, 2]
    return _json({"laws": laws, "levels": lv, "bridge_var": float(np.var(mids - ends / 2)), "bridge_theory": 0.25})


def compute_reflection() -> dict:
    """20,000 Brownian paths on 1,000 steps: the running maximum against the reflection principle, the discrete
    monitoring shift (Broadie, Glasserman and Kou 1997), the first-passage density and the arcsine law."""
    n, N = 1000, 20000
    dW, W = sim.brownian(1.0, n, N, seed=23)
    M = W.max(axis=1)
    a_grid = np.linspace(0.0, 2.5, 26)
    sim_tail = [float(np.mean(M >= a)) for a in a_grid]
    theory = [float(2 * norm.sf(a)) for a in a_grid]
    beta = 0.5826
    bgk = float(2 * norm.sf(1 + beta * np.sqrt(1 / n)))
    hit = M >= 1
    tau = np.argmax(W >= 1, axis=1)[hit] / n
    th, te = np.histogram(tau, bins=25, range=(0, 1))
    pos = (W[:, 1:] > 0).mean(axis=1)
    ph, pe = np.histogram(pos, bins=20, range=(0, 1))
    # one path that crosses 1 near the middle, and its reflection after the crossing
    i = int(np.argmin(np.abs(np.where(hit, np.argmax(W >= 1, axis=1) / n, 9) - 0.45)))
    k = int(np.argmax(W[i] >= 1))
    refl = W[i].copy()
    refl[k:] = 2 * W[i, k] - W[i, k:]
    return _json({"p_sim": float(np.mean(M >= 1)), "p_theory": float(2 * norm.sf(1)), "p_bgk": bgk,
                  "a_grid": a_grid, "tail_sim": sim_tail, "tail_theory": theory, "tau_hist": th, "tau_edges": te,
                  "n_hit": int(hit.sum()), "pos_hist": ph, "pos_edges": pe, "path": _thin(W[i], 501),
                  "refl": _thin(refl, 501), "t_cross": k / n, "N": N, "n": n,
                  "frac_extreme": float(np.mean((pos < 0.1) | (pos > 0.9))), "frac_middle": float(np.mean((pos > 0.4) & (pos < 0.6)))})


def compute_qv_live() -> dict:
    """One path at 2^12 steps: the three running variation sums at n = 16 ... 4096; the spread of the quadratic
    variation estimate against sqrt(2/n) over 4,000 paths; and Bitcoin's microstructure noise from the signature plot."""
    rng = np.random.default_rng(24)
    nmax = 2 ** 12
    dW = rng.standard_normal(nmax) * np.sqrt(1 / nmax)
    W = np.concatenate([[0.0], np.cumsum(dW)])
    run = {}
    for n in (16, 64, 256, 1024, 4096):
        d = dW.reshape(n, -1).sum(axis=1)
        run[str(n)] = {"v1": np.concatenate([[0], np.cumsum(np.abs(d))]), "v2": np.concatenate([[0], np.cumsum(d ** 2)]),
                       "v3": np.concatenate([[0], np.cumsum(np.abs(d) ** 3)])}
    ns = [16, 64, 256, 1024, 4096]
    dd, _ = sim.brownian(1.0, 4096, 4000, seed=25)
    sds = [float(np.std((dd.reshape(4000, n, -1).sum(axis=2) ** 2).sum(axis=1))) for n in ns]
    s = load("signature")
    yrs = s["years"]
    n1 = yrs * 365.25 * 1440
    rv1, rvd = s["rv_annual"][0], s["rv_annual"][-1]
    noise_var = (rv1 - rvd) * yrs / (2 * n1)
    return _json({"W": W[::4], "run": run, "ns": ns, "qv_sd": sds, "qv_sd_theory": [float(np.sqrt(2 / n)) for n in ns],
                  "noise_var": noise_var, "noise_bp": float(1e4 * np.sqrt(max(noise_var, 0))), "rv_1m": rv1,
                  "rv_1d": rvd, "n_1m": n1})


def compute_wong_zakai() -> dict:
    """dX = X dW, X_0 = 1, three ways on 20,000 shared paths: Euler-Maruyama (Itô), and the ordinary differential
    equation x' = x W'^{(n)} driven by the piecewise-linear interpolation of the same path (solved by RK4, 8 substeps
    a piece): Wong and Zakai (1965) say the ODE converges to the Stratonovich solution e^{W}."""
    N, nmax = 20000, 1024
    dW, W = sim.brownian(1.0, nmax, N, seed=26)
    rows = []
    for n in (4, 16, 64, 256, 1024):
        d = dW.reshape(N, n, -1).sum(axis=2)
        em = np.prod(1 + d, axis=1)
        x = np.ones(N)
        for k in range(n):
            s = d[:, k] / 8  # x' = x * slope over the piece, RK4 in 8 substeps
            for _ in range(8):
                k1 = x * s
                k2 = (x + k1 / 2) * s
                k3 = (x + k2 / 2) * s
                k4 = (x + k3) * s
                x = x + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        rows.append({"n": n, "ode": float(x.mean()), "ode_se": float(x.std() / np.sqrt(N)), "em": float(em.mean()),
                     "em_se": float(em.std() / np.sqrt(N))})
    t = np.linspace(0, 1, nmax + 1)
    w0 = W[0]
    return _json({"rows": rows, "strat": float(np.exp(0.5)), "ito": 1.0, "t": t[::4], "W": w0[::4],
                  "exp_w": np.exp(w0[::4]), "exp_ito": np.exp(w0[::4] - t[::4] / 2)})


def compute_lemma_column() -> dict:
    """Itô's lemma seen happening: along one Brownian path, f(t, W) = W^2 e^{-t/4} against its tangent-plane
    predictions; the misses pile up to 1/2 int f_xx dt.  With two correlated paths (rho = -0.7) and f = xy, the misses
    pile up to the covariation rho t.  GBM's volatility drag and E[W^4] on 20,000 paths."""
    n = 400
    dW, W = sim.brownian(1.0, n, 1, seed=27)
    w = W[0]
    t = np.linspace(0, 1, n + 1)
    f = w ** 2 * np.exp(-t / 4)
    pred = (-0.25 * w[:-1] ** 2 * np.exp(-t[:-1] / 4)) * (1 / n) + 2 * w[:-1] * np.exp(-t[:-1] / 4) * dW[0]
    miss = np.diff(f) - pred
    theory = 4 * (1 - np.exp(-t / 4))
    rho = -0.7
    rng = np.random.default_rng(28)
    z1, z2 = rng.standard_normal((2, n)) * np.sqrt(1 / n)
    dB = rho * z1 + np.sqrt(1 - rho ** 2) * z2
    X = np.concatenate([[0.0], np.cumsum(z1)])
    Y = np.concatenate([[0.0], np.cumsum(dB)])
    miss2 = np.diff(X * Y) - (Y[:-1] * z1 + X[:-1] * dB)
    mu, sig = 0.10, 0.40
    _, Wg = sim.brownian(1.0, 1, 20000, seed=29)
    logS = (mu - 0.5 * sig ** 2) + sig * Wg[:, -1]
    _, W4 = sim.brownian(1.0, 1, 200000, seed=30)
    return _json({"t": t, "W": w, "f": f, "cum_miss": np.concatenate([[0], np.cumsum(miss)]), "theory": theory,
                  "X": X, "Y": Y, "cum_miss2": np.concatenate([[0], np.cumsum(miss2)]), "rho": rho,
                  "mean_log": float(logS.mean()), "drag_theory": mu - 0.5 * sig ** 2, "mu": mu, "sigma": sig,
                  "log_mean": float(np.log(np.exp(logS).mean())), "EW4": float(np.mean(W4[:, -1] ** 4))})


def compute_picard() -> dict:
    """Picard iteration for dX = sin(X) dt + 0.5 cos(X) dW, X_0 = 1, on one Brownian path (1,000 steps): each iterate
    plugs the previous one into the right-hand side; the sup-distance between iterates falls like C^k / k!."""
    n = 1000
    dW, _ = sim.brownian(1.0, n, 1, seed=31)
    dW = dW[0]
    dt = 1 / n
    X = np.ones(n + 1)
    its, dist = [X.copy()], []
    for _ in range(9):
        Xn = np.concatenate([[1.0], 1.0 + np.cumsum(np.sin(X[:-1]) * dt + 0.5 * np.cos(X[:-1]) * dW)])
        dist.append(float(np.max(np.abs(Xn - X))))
        X = Xn
        its.append(X.copy())
    em = sim.euler_maruyama(lambda t, x: np.sin(x), lambda t, x: 0.5 * np.cos(x), 1.0, 1.0, dW[None])[0]
    return _json({"iterates": [x[::5] for x in its], "dist": dist, "em_gap": float(np.max(np.abs(X - em)))})


def compute_cir_mle() -> dict:
    """CIR fitted to the monthly 3-month bill rate by exact (non-central chi-square) maximum likelihood, from the
    regression estimate and four random starts; every Nelder-Mead iterate kept for the replay."""
    from scipy.stats import gamma as gamma_d

    r = load("rates")
    x = np.maximum(np.asarray(r["r"]), 1e-5)
    reg = r["cir"]
    x0s = [[reg["kappa"], reg["theta"], reg["sigma"]]]
    rng = np.random.default_rng(32)
    for _ in range(4):
        x0s.append([float(np.exp(rng.uniform(np.log(0.01), np.log(1.0)))), float(rng.uniform(0.01, 0.08)),
                    float(np.exp(rng.uniform(np.log(0.02), np.log(0.2))))])
    fits, curves = [], []
    for x0 in x0s:
        f = sim.cir_mle(x, 1 / 12, x0, maxiter=800)
        ll = [sim.cir_loglik(p, x, 1 / 12) for p in f["iterates"]]
        fits.append({k: f[k] for k in ("kappa", "theta", "sigma", "loglik", "feller")})
        curves.append(ll)
    L = max(len(c) for c in curves)
    curves = np.array([c + [c[-1]] * (L - len(c)) for c in curves])
    f0 = sim.cir_mle(x, 1 / 12, x0s[0], maxiter=800)
    its = f0["iterates"]
    ck = np.unique(np.linspace(0, len(its) - 1, 10).astype(int))
    xg = np.linspace(0.0005, 0.16, 160)

    def stat(p):
        k, th, s = p
        a = 2 * k * th / s ** 2
        return gamma_d.pdf(xg, a, scale=s ** 2 / (2 * k))
    dens = [stat(its[i]) for i in ck]
    hist, edges = np.histogram(x, bins=32, range=(0, 0.16), density=True)
    return _json({"fits": fits, "curves": curves, "ck": ck, "ck_params": [its[i] for i in ck],
                  "ck_loglik": [float(sim.cir_loglik(its[i], x, 1 / 12)) for i in ck], "xg": xg, "dens": dens,
                  "hist": hist, "edges": edges, "reg": reg, "reg_loglik": sim.cir_loglik([reg["kappa"], reg["theta"],
                                                                                           reg["sigma"]], x, 1 / 12),
                  "best": max(fits, key=lambda f: f["loglik"])})


def compute_fp_surface() -> dict:
    """The transition density p(t, x) of CIR from x_0 = 4%: with the fitted parameters (2 kappa theta / sigma^2 = 0.58:
    a wall of probability at 0) and with sigma lowered so that 2 kappa theta / sigma^2 = 2 (the density pinches to 0),
    on a grid in (t, x); checked against a histogram of 20,000 exact paths at t = 5."""
    from scipy.stats import ncx2

    r = load("rates")
    k, th, s = r["cir"]["kappa"], r["cir"]["theta"], r["cir"]["sigma"]
    x0 = 0.04
    ts = np.linspace(0.25, 10, 40)
    xs = np.linspace(0.001, 0.12, 60)

    def dens(kk, tt, ss):
        out = []
        for t in ts:
            c = ss ** 2 * (1 - np.exp(-kk * t)) / (4 * kk)
            d = 4 * kk * tt / ss ** 2
            lam = x0 * np.exp(-kk * t) / c
            out.append(ncx2.pdf(xs / c, d, lam) / c)
        return np.array(out)
    s2 = np.sqrt(kk_th := k * th)  # 2 k th / s^2 = 2
    p_fit = dens(k, th, s)
    p_two = dens(k, th, s2)
    X = sim.cir_exact(x0, k, th, s, 5.0, 60, 20000, seed=33)[:, -1]
    h, e = np.histogram(X, bins=60, range=(0, 0.12), density=True)
    c = s ** 2 * (1 - np.exp(-k * 5)) / (4 * k)
    mid = (e[:-1] + e[1:]) / 2
    exact = (ncx2.cdf(e[1:] / c, 4 * k * th / s ** 2, x0 * np.exp(-k * 5) / c)
             - ncx2.cdf(e[:-1] / c, 4 * k * th / s ** 2, x0 * np.exp(-k * 5) / c)) / np.diff(e)
    l1 = float(np.sum(np.abs(h - exact) * np.diff(e)))
    return _json({"ts": ts, "xs": xs, "p_fit": p_fit, "p_two": p_two, "nu_fit": 2 * k * th / s ** 2, "nu_two": 2.0,
                  "sigma_two": float(s2), "l1": l1, "frac_low": float(np.mean(X < 0.002)), "x0": x0, "mid": mid,
                  "hist5": h, "exact5": exact, "kk_th": kk_th})


def compute_fk_check() -> dict:
    """Feynman-Kac checked: the Vasicek 10-year zero-coupon bond from December 2020's bill rate, by Monte Carlo
    (20,000 exact paths, daily steps, trapezoid integral of r) against the closed form; and Dynkin's E[tau] = ab for
    Brownian motion leaving (-1, 2)."""
    r = load("rates")
    v = r["vasicek"]
    k, th, s = v["kappa"], v["theta"], v["sigma"]
    r0 = float(np.asarray(r["r"])[-1])
    T, n = 10.0, 2520
    X = sim.ou_exact(r0, k, th, s, T, n, 20000, seed=34)
    integ = (X[:, :-1] + X[:, 1:]).sum(axis=1) * (T / n) / 2
    disc = np.exp(-integ)
    B = (1 - np.exp(-k * T)) / k
    lnP = (th - s ** 2 / (2 * k ** 2)) * (B - T) - s ** 2 * B ** 2 / (4 * k) - B * r0
    taus = np.linspace(0.25, 30, 120)
    Bs = (1 - np.exp(-k * taus)) / k
    ys = -((th - s ** 2 / (2 * k ** 2)) * (Bs - taus) - s ** 2 * Bs ** 2 / (4 * k) - Bs * r0) / taus
    # Dynkin: exit time of BM from (-1, 2), dt = 1e-4
    rng = np.random.default_rng(35)
    m, dt = 20000, 1e-4
    w = np.zeros(m)
    tau = np.zeros(m)
    alive = np.ones(m, bool)
    steps = 0
    while alive.any() and steps < 400000:
        idx = np.flatnonzero(alive)
        w[idx] += rng.standard_normal(len(idx)) * np.sqrt(dt)
        tau[idx] += dt
        out = (w[idx] <= -1) | (w[idx] >= 2)
        alive[idx[out]] = False
        steps += 1
    return _json({"mc": float(disc.mean()), "mc_se": float(disc.std() / np.sqrt(len(disc))), "closed": float(np.exp(lnP)),
                  "mc_yield": float(-np.log(disc.mean()) / T), "closed_yield": float(-lnP / T), "r0": r0,
                  "taus": taus, "curve": ys, "y30": float(ys[-1]), "dynkin": float(tau.mean()),
                  "dynkin_se": float(tau.std() / np.sqrt(m)), "p_upper": float(np.mean(w >= 2))})


def compute_girsanov_paths() -> dict:
    """300 driftless Brownian paths and their Girsanov weights Z = exp(theta W_T - theta^2 T / 2) (theta = 1): under
    Q the same paths have drift theta.  The weighted histogram of W_T against the moved one; the effective sample size
    of 100,000 weights at T = 1, 4, 16, 64 (theta = 0.5) against e^{-theta^2 T}."""
    th = 1.0
    _, W = sim.brownian(1.0, 100, 300, seed=36)
    z = np.exp(th * W[:, -1] - th ** 2 / 2)
    big = np.random.default_rng(37).standard_normal(200000)
    wb = np.exp(th * big - th ** 2 / 2)
    edges = np.linspace(-3.5, 4.5, 41)
    h_p, _ = np.histogram(big, edges, density=True)
    h_q, _ = np.histogram(big, edges, weights=wb, density=True)
    h_m, _ = np.histogram(big + th, edges, density=True)
    ess = []
    for T in (1, 4, 16, 64):
        x = np.random.default_rng(38).standard_normal(100000) * np.sqrt(T)
        w = np.exp(0.5 * x - 0.125 * T)
        ess.append({"T": T, "ess": float(w.sum() ** 2 / (w ** 2).sum() / len(w)), "theory": float(np.exp(-0.25 * T)),
                    "mean_w": float(w.mean()), "max_share": float(w.max() / w.sum())})
    return _json({"theta": th, "W": W[:, ::2], "Z": z, "edges": edges, "h_p": h_p, "h_q": h_q, "h_moved": h_m,
                  "wmean": float((wb * big).sum() / wb.sum()), "EZ": float(wb.mean()), "ess": ess})


def compute_is_run() -> dict:
    """The deep out-of-the-money digital of the girsanov item, running estimates path by path: plain and reweighted
    (the House's is_digital), 20,000 paths each, with their standard errors."""
    S0, K, T, sig = 100.0, 160.0, 1.0, 0.2
    n = 20000
    m, se, pay = sim.is_digital(S0, K, sig, T, n, seed=9)
    z = np.random.default_rng(9).standard_normal(n)
    plain = (S0 * np.exp(-0.5 * sig ** 2 * T + sig * np.sqrt(T) * z) > K).astype(float)
    idx = np.unique(np.geomspace(20, n, 120).astype(int))
    def run(x):
        c = np.cumsum(x)
        c2 = np.cumsum(x * x)
        mu = c[idx - 1] / idx
        sd = np.sqrt(np.maximum(c2[idx - 1] / idx - mu ** 2, 0) / idx)
        return mu, sd
    pm, ps = run(plain)
    im, is_ = run(pay)
    exact = float(norm.cdf((np.log(S0 / K) - 0.5 * sig ** 2 * T) / (sig * np.sqrt(T))))
    return _json({"idx": idx, "plain": pm, "plain_se": ps, "is": im, "is_se": is_, "exact": exact, "is_mean": m,
                  "is_sd": se, "plain_mean": float(plain.mean()), "plain_sd": float(plain.std() / np.sqrt(n)),
                  "var_ratio": float(plain.var() / pay.var())})


def compute_observability() -> dict:
    """200 simulated years of one-minute GBM (sigma = 20%, mu = 8%): volatility from quadratic variation against the
    drift from the endpoint, year by year, and running through one year."""
    sig, mu, n = 0.20, 0.08, 525600
    dt = 1 / n
    rng = np.random.default_rng(39)
    shat, mhat = [], []
    for y in range(200):
        r = (mu - 0.5 * sig ** 2) * dt + sig * np.sqrt(dt) * rng.standard_normal(n)
        shat.append(float(np.sqrt(np.sum(r ** 2))))
        mhat.append(float(r.sum() + 0.5 * sig ** 2))
        if y == 0:
            days = np.arange(1, 366) * (n // 365)
            c, c2 = np.cumsum(r), np.cumsum(r ** 2)
            t = days * dt
            run_s = np.sqrt(c2[days - 1] / t)
            run_m = c[days - 1] / t + 0.5 * sig ** 2
    return _json({"sigma_hat": shat, "mu_hat": mhat, "sd_sigma": float(np.std(shat)), "sd_mu": float(np.std(mhat)),
                  "sd_sigma_theory": sig / np.sqrt(2 * n), "sd_mu_theory": sig, "run_t": t, "run_s": run_s,
                  "run_m": run_m, "sigma": sig, "mu": mu, "n": n})


def compute_hedge_rates() -> dict:
    """Martingale representation in practice: hedge errors on n = 8 ... 2,048 rebalances, five seeds of 4,000 paths:
    F = W_T^2 hedged with H = 2W (Clark-Ocone), a Black-Scholes call (S_0 = K = 100, sigma = 20%, T = 1, r = 0)
    hedged with its delta, and F = X_T^2 where X = 0.8 W + 0.6 B hedged in W alone (a second noise)."""
    from explainer.quant.house import bs as BS

    ns = [8, 32, 128, 512, 2048]
    res = {"w2": [], "call": [], "two": []}
    S0, K, sig = 100.0, 100.0, 0.2
    C0 = float(BS.price(S0, K, 1.0, sig, 0.0, 0.0, 1))
    for seed in range(5):
        rng = np.random.default_rng(40 + seed)
        N, nmax = 4000, 2048
        dW = rng.standard_normal((N, nmax)) * np.sqrt(1 / nmax)
        dB = rng.standard_normal((N, nmax)) * np.sqrt(1 / nmax)
        rw = {"w2": [], "call": [], "two": []}
        for n in ns:
            d = dW.reshape(N, n, -1).sum(axis=2)
            b = dB.reshape(N, n, -1).sum(axis=2)
            W = np.concatenate([np.zeros((N, 1)), np.cumsum(d, axis=1)], axis=1)
            X = 0.8 * W + 0.6 * np.concatenate([np.zeros((N, 1)), np.cumsum(b, axis=1)], axis=1)
            rw["w2"].append(float(np.std(W[:, -1] ** 2 - (1 + np.sum(2 * W[:, :-1] * d, axis=1)))))
            rw["two"].append(float(np.std(X[:, -1] ** 2 - (1 + np.sum(2 * 0.8 * X[:, :-1] * d, axis=1)))))
            t = np.linspace(0, 1, n + 1)
            S = S0 * np.exp(-0.5 * sig ** 2 * t + sig * W)
            tau = np.maximum(1 - t[:-1], 1e-12)
            d1 = (np.log(S[:, :-1] / K) + 0.5 * sig ** 2 * tau) / (sig * np.sqrt(tau))
            V = C0 + np.sum(norm.cdf(d1) * np.diff(S, axis=1), axis=1)
            rw["call"].append(float(np.std(np.maximum(S[:, -1] - K, 0) - V)))
        for k in res:
            res[k].append(rw[k])
    # one path for the picture: M_t = E[W_T^2 | F_t] = W_t^2 + 1 - t, and the hedge at n = 8 and 512
    rng = np.random.default_rng(45)
    dW = rng.standard_normal(2048) * np.sqrt(1 / 2048)
    W = np.concatenate([[0.0], np.cumsum(dW)])
    t = np.linspace(0, 1, 2049)
    M = W ** 2 + 1 - t
    hedges = {}
    for n in (8, 512):
        st = 2048 // n
        Wc = W[::st]
        V = np.concatenate([[1.0], 1 + np.cumsum(2 * Wc[:-1] * np.diff(Wc))])
        hedges[str(n)] = {"t": t[::st], "V": V}
    slope = {k: float(np.polyfit(np.log(ns), np.log(np.mean(res[k], axis=0)), 1)[0]) for k in res}
    return _json({"ns": ns, "sd": res, "slope": slope, "theory_w2": [float(np.sqrt(2 / n)) for n in ns],
                  "t": t[::4], "W": W[::4], "M": M[::4], "hedges": hedges, "C0": C0})


def compute_tanaka() -> dict:
    """Local time of Brownian motion at 0 by t = 1: by occupation (eps = 0.02) and by Tanaka (|W_1| - int sgn(W) dW),
    on 20,000 paths of 2,000 steps, against sqrt(2/pi); Lévy's identity (L has the law of the running maximum); and
    the smoothing of the kink on one fine path (200,000 steps)."""
    dW, W = sim.brownian(1.0, 2000, 20000, seed=46)
    Locc = sim.local_time(W, 0.0, 0.02)[:, -1]
    Ltan = np.abs(W[:, -1]) - np.sum(np.sign(W[:, :-1]) * dW, axis=1)
    M = W.max(axis=1)
    qs = np.linspace(0.02, 0.98, 49)
    rng = np.random.default_rng(47)
    n = 200000
    d = rng.standard_normal(n) * np.sqrt(1 / n)
    w = np.concatenate([[0.0], np.cumsum(d)])
    tan_one = float(np.abs(w[-1]) - np.sum(np.sign(w[:-1]) * d))
    eps_rows = [{"eps": e, "L": float(np.sum(np.abs(w[:-1]) < e) / n / (2 * e))} for e in (0.5, 0.2, 0.1, 0.05, 0.02, 0.01)]
    return _json({"mean_occ": float(Locc.mean()), "mean_tan": float(Ltan.mean()), "theory": float(np.sqrt(2 / np.pi)),
                  "E_absW": float(np.mean(np.abs(W[:, -1]))), "q_L": np.quantile(Ltan, qs), "q_M": np.quantile(M, qs),
                  "path": w[::200], "tan_one": tan_one, "eps_rows": eps_rows,
                  "L_run": sim.local_time(w, 0.0, 0.02)[::200]})


def _ts_levy(alpha=1.2, cp=1.0, cm=1.5, lam=1.0, eps=0.005, T=1.0, seed=48):
    """Jumps of a tempered-stable Lévy process (nu(dx) = c_{+/-} e^{-lam |x|} / |x|^{1 + alpha}) with |x| >= eps on
    [0, T], sampled by inverse transform on a fine grid."""
    rng = np.random.default_rng(seed)
    xs = np.geomspace(eps, 30, 4000)
    dens = np.exp(-lam * xs) / xs ** (1 + alpha)
    cdf = np.concatenate([[0], np.cumsum((dens[1:] + dens[:-1]) / 2 * np.diff(xs))])
    mass = cdf[-1]
    tot = (cp + cm) * mass
    n = rng.poisson(tot * T)
    times = np.sort(rng.uniform(0, T, n))
    sizes = np.interp(rng.random(n) * mass, cdf, xs)
    sgn = np.where(rng.random(n) < cp / (cp + cm), 1.0, -1.0)
    return times, sizes * sgn, (xs, dens, cdf)


def compute_levy_layers() -> dict:
    """The Lévy-Itô layer cake on one path: drift, Brownian part, big jumps (|x| >= 1), and the compensated small jumps
    eps <= |x| < 1 for eps = 0.3, 0.1, 0.03, 0.01; the characteristic function checked (Lévy-Khintchine); a Poisson
    clock; and the compensated compound Poisson's mean and variance on 50,000 paths."""
    alpha, cp, cm, lam = 1.2, 1.0, 1.5, 1.0
    b, sig = 0.1, 0.2
    seed = next(s for s in range(48, 400) if np.sum(np.abs(_ts_levy(alpha, cp, cm, lam, seed=s)[1]) >= 1) == 3)
    times, x, (xs, dens, cdf) = _ts_levy(alpha, cp, cm, lam, seed=seed)
    grid = np.linspace(0, 1, 1001)
    rng = np.random.default_rng(49)
    Wb = np.concatenate([[0.0], np.cumsum(rng.standard_normal(1000) * np.sqrt(1 / 1000))]) * sig

    def mean_x(lo, hi):  # int_{lo <= |x| < hi} x nu(dx)
        m = (xs >= lo) & (xs < hi)
        return float(np.trapezoid(xs[m] * dens[m], xs[m]) * (cp - cm))
    big = np.array([np.sum(x[(np.abs(x) >= 1) & (times <= g)]) for g in grid])
    small = {}
    for e in (0.3, 0.1, 0.03, 0.01, 0.005):
        sel = (np.abs(x) >= e) & (np.abs(x) < 1)
        comp = mean_x(e, 1.0)
        small[str(e)] = np.array([np.sum(x[sel & (times <= g)]) for g in grid]) - comp * grid
    # Lévy-Khintchine check on 20,000 copies of X_1 (small jumps from 0.01)
    us = np.linspace(0.25, 4, 16)
    X1 = []
    for s in range(20000):
        tt, xx, _ = _ts_levy(alpha, cp, cm, lam, seed=10000 + s)
        X1.append(np.sum(xx) - mean_x(0.005, 1.0))
    X1 = np.asarray(X1) + b + sig * np.random.default_rng(50).standard_normal(20000)
    m = xs >= 0.005
    psi = []
    for u in us:
        integrand_p = (np.exp(1j * u * xs) - 1 - 1j * u * xs * (xs < 1)) * dens
        integrand_m = (np.exp(-1j * u * xs) - 1 + 1j * u * xs * (xs < 1)) * dens
        I = cp * np.trapezoid(integrand_p[m], xs[m]) + cm * np.trapezoid(integrand_m[m], xs[m])
        psi.append(1j * u * b - 0.5 * sig ** 2 * u ** 2 + I)
    cf_th = np.exp(np.array(psi))
    cf_emp = np.array([np.mean(np.exp(1j * u * X1)) for u in us])
    # a Poisson clock (rate 6 a year) and the compensated compound Poisson
    clock = np.cumsum(np.random.default_rng(51).exponential(1 / 6, 20))
    clock = clock[clock <= 1]
    rng = np.random.default_rng(52)
    Nn = rng.poisson(6, 50000)
    Ysum = np.array([rng.normal(-0.05, 0.08, k).sum() for k in Nn])
    comp = Ysum - 6 * (-0.05)
    return _json({"grid": grid, "drift": b * grid, "brown": Wb, "big": big, "small": small, "n_jumps": int(len(x)),
                  "n_big": int(np.sum(np.abs(x) >= 1)), "us": us, "cf_th_re": cf_th.real, "cf_th_im": cf_th.imag,
                  "cf_emp_re": cf_emp.real, "cf_emp_im": cf_emp.imag, "cf_err": float(np.max(np.abs(cf_th - cf_emp))),
                  "clock": clock, "cp_mean": float(comp.mean()), "cp_var": float(comp.var()),
                  "cp_var_theory": 6 * (0.05 ** 2 + 0.08 ** 2), "n_small": {str(e): int(np.sum((np.abs(x) >= e) & (np.abs(x) < 1)))
                                                                           for e in (0.3, 0.1, 0.03, 0.01, 0.005)},
                  "comp": {str(e): mean_x(e, 1.0) for e in (0.3, 0.1, 0.03, 0.01, 0.005)}, "seed": seed, "alpha": alpha})


def compute_jump_hedge() -> dict:
    """A short at-the-money three-month call (S_0 = K = 100, sigma = 20%) delta-hedged with the Black-Scholes delta,
    n = 13 ... 4,000 rebalances a year, on 10,000 paths of GBM and of Merton's jump-diffusion (6 jumps a year, log
    sizes N(-5%, 8%^2), the same diffusion): the hedge error's spread."""
    from explainer.quant.house import bs as BS

    S0, K, T, sig = 100.0, 100.0, 0.25, 0.2
    lam, mj, sj = 6.0, -0.05, 0.08
    kbar = np.exp(mj + 0.5 * sj ** 2) - 1
    rows = []
    one = None
    for n_year in (13, 52, 252, 1000, 4000):
        n = max(int(round(n_year * T)), 2)
        dt = T / n
        out = {}
        for jumps in (False, True):
            rng = np.random.default_rng(53)
            N = 10000
            x = np.full(N, np.log(S0))
            V = np.full(N, float(BS.price(S0, K, T, sig, 0.0, 0.0, 1)))
            S = np.full(N, S0)
            trace = []
            for k in range(n):
                tau = T - k * dt
                d1 = (np.log(S / K) + 0.5 * sig ** 2 * tau) / (sig * np.sqrt(tau))
                delta = norm.cdf(d1)
                dlog = -0.5 * sig ** 2 * dt + sig * np.sqrt(dt) * rng.standard_normal(N)
                if jumps:
                    nj = rng.poisson(lam * dt, N)
                    dlog = dlog - lam * kbar * dt + mj * nj + sj * np.sqrt(nj) * rng.standard_normal(N)
                Snew = np.exp(x + dlog)
                V = V + delta * (Snew - S)
                x, S = x + dlog, Snew
                if jumps and n_year == 1000:
                    trace.append((S[0], V[0]))
            err = V - np.maximum(S - K, 0)
            out["jump" if jumps else "gbm"] = float(err.std())
            if jumps and n_year == 1000:
                one = trace
        rows.append({"n": n_year, **out})
    return _json({"rows": rows, "lam": lam, "mj": mj, "sj": sj, "sigma": sig, "T": T,
                  "slope_gbm": float(np.polyfit(np.log([r["n"] for r in rows]), np.log([r["gbm"] for r in rows]), 1)[0]),
                  "floor_ratio": rows[-1]["jump"] / rows[-1]["gbm"]})


def compute_hawkes_replay() -> dict:
    """The Bitcoin Hawkes fit, replayed: Nelder-Mead's iterates from eight random starts, the log-likelihood along each,
    and the fitted intensity at checkpoints of the first."""
    from scipy import optimize

    h = load("hawkes")
    ev = np.asarray(h["events"])
    T = h["T"]
    rng = np.random.default_rng(54)
    starts = [[float(np.exp(rng.uniform(np.log(0.02), np.log(0.5)))), float(np.exp(rng.uniform(np.log(0.05), np.log(3)))),
               float(np.exp(rng.uniform(np.log(0.1), np.log(10))))] for _ in range(8)]
    curves, finals, its0 = [], [], None
    for j, x0 in enumerate(starts):
        its = []
        res = optimize.minimize(lambda p: -sim.hawkes_loglik(np.exp(p), ev, T), np.log(x0), method="Nelder-Mead",
                                callback=lambda p: its.append(np.exp(p).tolist()),
                                options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-8})
        ll = [sim.hawkes_loglik(p, ev, T) for p in its]
        curves.append(ll)
        mu, a, b = np.exp(res.x)
        finals.append({"mu": float(mu), "alpha": float(a), "beta": float(b), "branching": float(a / b),
                       "loglik": float(-res.fun)})
        if j == 0:
            its0 = its
    L = 160
    curves = np.array([(c + [c[-1]] * L)[:L] for c in curves])
    ck = [0, 3, 8, 15, 25, 40, 60, 90, 159]
    ck = [min(c, len(its0) - 1) for c in ck]
    grid = np.linspace(0, T, 700)
    lams = [sim.hawkes_intensity(ev, *its0[c], grid) for c in ck]
    return _json({"curves": curves, "finals": finals, "ck": ck, "ck_params": [its0[c] for c in ck], "grid": grid,
                  "lams": lams, "events": ev, "T": T, "ll_poisson": h["fit"]["loglik_poisson"],
                  "spread": float(np.ptp([f["branching"] for f in finals]))})


def compute_hawkes_check() -> dict:
    """Simulation against theory: 50 Hawkes paths (mu = 0.2, alpha = 1.4, beta = 2, T = 2,000): the mean count against
    mu T / (1 - alpha / beta); thinning with its candidates, and a branching (cluster) picture."""
    counts = [len(sim.hawkes_thinning(0.2, 1.4, 2.0, 2000.0, seed=1000 + s)) for s in range(50)]
    tr = sim.hawkes_thinning_trace(0.2, 1.4, 2.0, 40.0, seed=13)
    cl = sim.hawkes_clusters(0.2, 0.7, 2.0, 60.0, seed=56)
    sizes = np.bincount(np.array([_root(cl["parent"], i) for i in range(len(cl["t"]))]))
    sizes = sizes[sizes > 0]
    return _json({"mean_count": float(np.mean(counts)), "sd_count": float(np.std(counts)),
                  "theory": 0.2 * 2000 / (1 - 0.7), "trace": tr, "clusters": cl, "mean_cluster": float(sizes.mean()),
                  "cluster_theory": 1 / (1 - 0.7), "n_clusters": int(len(sizes))})


def _root(parent, i):
    while parent[i] >= 0:
        i = parent[i]
    return i


def compute_hawkes_rescale() -> dict:
    """The time-rescaling test on the Bitcoin events: gaps of the fitted compensator against Exp(1), for the Hawkes
    fit and for a Poisson clock at the average rate (Kolmogorov-Smirnov)."""
    from scipy.stats import kstest

    h = load("hawkes")
    ev = np.asarray(h["events"])
    f = h["fit"]
    gh = np.diff(sim.hawkes_compensator(ev, f["mu"], f["alpha"], f["beta"]))
    gp = np.diff(ev) * len(ev) / h["T"]
    ph = float(kstest(gh, "expon").pvalue)
    pp = float(kstest(gp, "expon").pvalue)
    q = (np.arange(1, len(gh) + 1) - 0.5) / len(gh)
    return _json({"p_hawkes": ph, "p_poisson": pp, "qq_x": -np.log(1 - q), "qq_h": np.sort(gh), "qq_p": np.sort(gp),
                  "resc": sim.hawkes_compensator(ev, f["mu"], f["alpha"], f["beta"])})


def compute_fbm_morph() -> dict:
    """The H dial: one fixed complex Gaussian vector turned into fBM at H = 0.05 ... 0.95 by Davies-Harte; the lag-1
    increment correlation 2^{2H-1} - 1; and the expected squared-variation sums E sum |dB|^2 = n^{1-2H} on refining
    grids for H = 0.3, 0.5, 0.7 (200 paths)."""
    n = 1000
    m = 2 * n
    z = np.random.default_rng(57).standard_normal(m) + 1j * np.random.default_rng(58).standard_normal(m)
    Hs = np.round(np.arange(0.05, 0.96, 0.05), 2)
    paths = {}
    for H in Hs:
        k = np.arange(n + 1)
        g = 0.5 * (np.abs(k - 1) ** (2 * H) - 2 * np.abs(k) ** (2 * H) + np.abs(k + 1) ** (2 * H))
        row = np.concatenate([g, g[-2:0:-1]])
        lam = np.clip(np.fft.fft(row).real, 0, None)
        y = np.fft.fft(np.sqrt(lam / m) * z)[:n].real
        paths[f"{H:.2f}"] = np.concatenate([[0.0], np.cumsum(y)]) * (1 / n) ** H
    pv = {}
    ns = [16, 64, 256, 1024, 4096]
    for H in (0.3, 0.5, 0.7):
        B = sim.fbm(H, 4096, 1.0, 200, seed=59)
        pv[str(H)] = [float(np.mean(np.sum(np.diff(B[:, :: 4096 // nn], axis=1) ** 2, axis=1))) for nn in ns]
    return _json({"Hs": Hs, "paths": paths, "rho1": {f"{H:.2f}": float(2 ** (2 * H - 1) - 1) for H in Hs}, "ns": ns,
                  "pvar": pv})


def compute_cont_das() -> dict:
    """Cont and Das's caveat, computed: a smooth (H = 1/2) Ornstein-Uhlenbeck log-volatility (mean reversion one week,
    stationary sd 0.3 around 50% a year), a one-second price with i.i.d. noise (5 basis points), 500 days; daily
    realized variance from 5-minute returns; the Hurst estimate of log realized volatility against that of the true
    integrated variance."""
    from scipy.signal import lfilter

    rng = np.random.default_rng(60)
    days, spd = 500, 86400
    dt = 1 / (365 * spd)
    kap = 52.0
    sd_st = 0.3
    phi = np.exp(-kap * dt)
    innov = sd_st * np.sqrt(1 - phi ** 2)
    zi = np.array([rng.standard_normal() * sd_st * phi])
    logp = 0.0
    rv, iv, rv_clean = [], [], []
    for d in range(days):
        e = rng.standard_normal(spd) * innov
        y, zi = lfilter([1.0], [1.0, -phi], e, zi=zi)
        zi = zi * 1.0
        sig = 0.5 * np.exp(y - sd_st ** 2)
        r = sig * np.sqrt(dt) * rng.standard_normal(spd)
        p = logp + np.cumsum(r)
        logp = p[-1]
        obs = p[299::300] + rng.standard_normal(288) * 5e-4
        rv.append(np.sum(np.diff(obs) ** 2))
        rv_clean.append(np.sum(np.diff(p[299::300]) ** 2))
        iv.append(np.sum(sig ** 2) * dt)
    h_rv = sim.hurst_from_increments(0.5 * np.log(rv))
    h_clean = sim.hurst_from_increments(0.5 * np.log(rv_clean))
    h_iv = sim.hurst_from_increments(0.5 * np.log(iv))
    return _json({"H_rv": h_rv["H"], "H_rv_clean": h_clean["H"], "H_iv": h_iv["H"], "zeta_rv": h_rv["zeta"],
                  "qs": h_rv["qs"], "log_rv": 0.5 * np.log(rv), "log_iv": 0.5 * np.log(iv), "days": days})


def compute_helix() -> dict:
    """Lyons' example: X^(n)(t) = (cos n^2 t, sin n^2 t) / n on [0, 1] drives dY1 = dX1, dY2 = dX2,
    dY3 = Y1 dX2 - Y2 dX1 from 0; the path shrinks to a point, Y3(1) does not."""
    out = {}
    for n in (1, 2, 4, 8):
        t = np.linspace(0, 1, 40001)
        X1, X2 = np.cos(n ** 2 * t) / n, np.sin(n ** 2 * t) / n
        Y1, Y2 = X1 - X1[0], X2 - X2[0]
        Y3 = np.concatenate([[0], np.cumsum(Y1[:-1] * np.diff(X2) - Y2[:-1] * np.diff(X1))])
        area = sim.signature2(np.column_stack([X1[::10], X2[::10]]))["levy_area"][0, 1]
        out[str(n)] = {"t": t[::20], "Y1": Y1[::20], "Y2": Y2[::20], "Y3": Y3[::20], "sup": float(np.max(np.hypot(X1, X2))),
                       "Y3_end": float(Y3[-1]), "area": float(area)}
    return _json(out)


def compute_sig_regression() -> dict:
    """Linear regression on truncated signatures, depth 1 to 5, on 20,000 paths of two correlated GBMs (sigma = 30%,
    rho = 0.5, 64 steps, with time as a channel): targets the average of the first asset (exactly linear at depth 2),
    an Asian call on it, and the Lévy area of the pair (exactly level 2).  Ridge, penalty picked on a validation
    split; five train/test splits; baselines: the final values, and every point of the path."""
    N, n = 20000, 64
    rng = np.random.default_rng(61)
    z1 = rng.standard_normal((N, n))
    z2 = 0.5 * z1 + np.sqrt(0.75) * rng.standard_normal((N, n))
    dt = 1 / n
    t = np.linspace(0, 1, n + 1)
    S1 = np.exp(np.concatenate([np.zeros((N, 1)), np.cumsum(-0.045 * dt + 0.3 * np.sqrt(dt) * z1, 1)], 1))
    S2 = np.exp(np.concatenate([np.zeros((N, 1)), np.cumsum(-0.045 * dt + 0.3 * np.sqrt(dt) * z2, 1)], 1))
    P = np.stack([np.broadcast_to(t, (N, n + 1)), S1, S2], 2)
    avg = np.trapezoid(S1, t, axis=1)
    asian = np.maximum(avg - 1.0, 0)
    area = np.array([0.0] * N)
    d1, d2 = np.diff(S1, axis=1), np.diff(S2, axis=1)
    area = 0.5 * np.sum((S1[:, :-1] - 1) * d2 - (S2[:, :-1] - 1) * d1, axis=1)
    feats = {k: sim.signature_batch(P, k) for k in range(1, 6)}
    base = {"last": np.column_stack([S1[:, -1], S2[:, -1]]), "path": np.column_stack([S1, S2])}
    lams = 10.0 ** np.arange(-8, 2)

    def ridge_r2(F, y, split):
        idx = np.random.default_rng(split).permutation(N)
        tr, va, te = idx[:12000], idx[12000:16000], idx[16000:]
        mu, sd = F[tr].mean(0), F[tr].std(0) + 1e-12
        Z = (F - mu) / sd
        A = np.column_stack([np.ones(N), Z])
        best = None
        for lam in lams:
            I = np.eye(A.shape[1]) * lam * len(tr)
            I[0, 0] = 0
            w = np.linalg.solve(A[tr].T @ A[tr] + I, A[tr].T @ y[tr])
            e = np.mean((A[va] @ w - y[va]) ** 2)
            if best is None or e < best[0]:
                best = (e, w)
        pred = A[te] @ best[1]
        return 1 - np.mean((pred - y[te]) ** 2) / np.var(y[te]), pred, y[te]
    out = {}
    for name, y in (("average", avg), ("asian", asian), ("area", area)):
        r2 = np.array([[ridge_r2(feats[k], y, s)[0] for k in range(1, 6)] for s in range(5)])
        bl = {b: float(np.mean([ridge_r2(base[b], y, s)[0] for s in range(5)])) for b in base}
        out[name] = {"r2": r2, "r2_mean": r2.mean(0), "base": bl}
    scat = {}
    for k in range(1, 6):
        _, pr, yt = ridge_r2(feats[k], asian, 0)
        scat[str(k)] = {"pred": pr[:400], "true": yt[:400]}
    return _json({"targets": out, "scatter": scat, "n_feats": [int(feats[k].shape[1]) for k in range(1, 6)], "N": N})


def compute_wti() -> dict:
    """FRED's Cushing WTI spot price (DCOILWTICO), March-May 2020, and Black-76 against Bachelier for a one-month put
    struck at 10 as the futures price falls toward and below zero (illustrative: normal vol matched to a 100%
    lognormal vol at F = 20)."""
    f = data.fred("DCOILWTICO", start="2020-03-02", through="2020-05-29")
    d, v = f["date"], f["value"]
    i = int(np.argmin(v))
    T, K = 1 / 12, 10.0
    sig_b = 1.0
    sig_n = sig_b * 20.0
    F = np.linspace(-20, 20, 81)

    def bach(F):
        s = sig_n * np.sqrt(T)
        dd = (F - K) / s
        return (K - F) * norm.cdf(-dd) + s * norm.pdf(dd)

    def black(F):
        out = np.full(len(F), np.nan)
        m = F > 0
        s = sig_b * np.sqrt(T)
        d1 = (np.log(F[m] / K) + 0.5 * s ** 2) / s
        out[m] = K * norm.cdf(-(d1 - s)) - F[m] * norm.cdf(-d1)
        return out
    return _json({"date": d, "value": v, "min_date": int(d[i]), "min": float(v[i]), "F": F, "bach": bach(F),
                  "black": black(F), "K": K, "sig_n": sig_n})


def compute_varswap() -> dict:
    """Realized variance replicated by a delta position in 1/S and a log contract (the variance-swap identity):
    10,000 Heston paths (kappa = 2, theta = v_0 = 0.04, xi = 0.5, rho = -0.7, full truncation) at 252 and 2,520 steps,
    and with Merton jumps added (3 a year, log size N(-10%, 5%^2)): the replication error's mean and spread."""
    out = {}
    lam, mj, sj = 3.0, -0.10, 0.05
    for n in (252, 2520):
        for jumps in (False, True):
            rng = np.random.default_rng(62)
            N = 10000
            dt = 1 / n
            x = np.zeros(N)
            v = np.full(N, 0.04)
            rep = np.zeros(N)
            rv = np.zeros(N)
            trace = []
            kbar = np.exp(mj + 0.5 * sj ** 2) - 1
            for k in range(n):
                z1 = rng.standard_normal(N)
                z2 = -0.7 * z1 + np.sqrt(0.51) * rng.standard_normal(N)
                vp = np.maximum(v, 0)
                dx = -0.5 * vp * dt + np.sqrt(vp * dt) * z1
                if jumps:
                    nj = rng.poisson(lam * dt, N)
                    dx = dx - lam * kbar * dt + mj * nj + sj * np.sqrt(nj) * rng.standard_normal(N)
                v = v + 2.0 * (0.04 - vp) * dt + 0.5 * np.sqrt(vp * dt) * z2
                rep += 2 * (np.exp(dx) - 1)          # 2 dS/S
                rv += dx ** 2
                x += dx
                if n == 252:
                    trace.append((float(rv[0]), float(rep[0] - 2 * x[0])))
            err = rep - 2 * x - rv
            out[f"{n}_{'jump' if jumps else 'heston'}"] = {"mean": float(err.mean()), "sd": float(err.std()),
                                                         "rv_mean": float(rv.mean()), "trace": trace}
    # theory for the jump bias: E[2(e^J - 1 - J) - J^2] per jump, times lam
    J = np.random.default_rng(63).normal(mj, sj, 1_000_000)
    out["jump_bias_theory"] = float(lam * np.mean(2 * (np.exp(J) - 1 - J) - J ** 2))
    out["cubic_theory"] = float(lam * np.mean(J ** 3) / 3)
    return _json(out)


def _btc_daily():
    t, c = _btc("1h", "2018-01", "2020-12")
    keep = (t % 86400) == 0
    return t[keep], c[keep]


def compute_nsde() -> dict:
    """A neural SDE market generator (the House's deep.NeuralSDE: a 2-dimensional latent SDE, drift and diffusion
    MLPs of width 32, Euler on 32 steps) trained on 32-day windows of Bitcoin's daily log returns 2018-2019 by matching
    expected signatures (depth 4, lead-lag); three seeds, a fan of generated windows every 100 steps.  Resumable."""
    import torch

    from explainer.quant.house import deep

    torch.set_num_threads(1)
    t, c = _btc_daily()
    r = np.diff(np.log(c))
    yr = np.array([datetime.fromtimestamp(x, tz=timezone.utc).year for x in t[1:]])
    tr = r[yr <= 2019]
    sd = tr.std()
    L = 32
    real = np.lib.stride_tricks.sliding_window_view((tr - tr.mean()) / sd, L)
    params = {"iters": 1000, "batch": 256, "lr": 3e-3, "L": L}
    part = CACHE.partial("nsde", params)
    for seed in range(3):
        key = f"seed{seed}"
        if key in part:
            continue
        m, curve, fans = deep.train_nsde(real, L=L, iters=params["iters"], batch=params["batch"], lr=params["lr"],
                                         seed=seed, every=100, log=lambda i, l: print(f"  seed {seed} it {i} loss {l:.4f}",
                                                                                       flush=True))
        torch.save(m.parameters(), CACHE.path("nsde").with_suffix(f".seed{seed}.pt"))
        with torch.no_grad():
            gen = m.sample(2000, torch.Generator().manual_seed(77)).numpy()
        part[key] = _json({"curve": curve, "fans": {str(k): v for k, v in fans.items()}, "gen": gen})
    out = {"seeds": [part[f"seed{s}"] for s in range(3)], "real_fan": np.cumsum(real[::30][:24], axis=1),
           "mean": float(tr.mean()), "sd": float(sd), "n_windows": int(len(real))}
    part.finish()
    return _json(out)


def compute_nsde_eval() -> dict:
    """The neural SDE on the 2020 hold-out (inside the research window): signature distance, kurtosis and the
    autocorrelation of |r|, against GBM (i.i.d. normal with the 2018-2019 mean and sd) and an i.i.d. bootstrap of
    2018-2019 returns, all standardized by the training sd."""
    import torch

    from explainer.quant.house import deep

    nz = load("nsde")
    t, c = _btc_daily()
    r = np.diff(np.log(c))
    yr = np.array([datetime.fromtimestamp(x, tz=timezone.utc).year for x in t[1:]])
    tr, te = r[yr <= 2019], r[yr == 2020]
    mu, sd = nz["mean"], nz["sd"]
    L = 32
    test = np.lib.stride_tricks.sliding_window_view((te - mu) / sd, L)
    train = np.lib.stride_tricks.sliding_window_view((tr - mu) / sd, L)
    rng = np.random.default_rng(64)
    gbm = rng.standard_normal((2000, L))
    boot = rng.choice((tr - mu) / sd, (2000, L))
    T = lambda a: torch.tensor(np.asarray(a), dtype=torch.float32)  # noqa: E731
    res = {"real_2020": deep.stylized_facts(test), "train": deep.stylized_facts(train)}
    res["gbm"] = {**deep.stylized_facts(gbm), "mmd": deep.sig_mmd(T(gbm), T(test))}
    res["bootstrap"] = {**deep.stylized_facts(boot), "mmd": deep.sig_mmd(T(boot), T(test))}
    ns = []
    for s in nz["seeds"]:
        g = np.asarray(s["gen"])
        ns.append({**deep.stylized_facts(g), "mmd": deep.sig_mmd(T(g), T(test))})
    res["nsde"] = ns
    res["nsde_mmd_mean"] = float(np.mean([x["mmd"] for x in ns]))
    res["nsde_kurt_mean"] = float(np.mean([x["kurtosis"] for x in ns]))
    res["nsde_acf_mean"] = float(np.mean([x["acf_abs"][0] for x in ns]))
    res["train_vs_test_mmd"] = deep.sig_mmd(T(train), T(test))
    return _json(res)


def compute_envelope2() -> dict:
    """Registers the second pass's fitted models with the trial counter."""
    reg = {"cir_mle_dtb3": pit.register("cir_mle_dtb3", inspect.getsource(compute_cir_mle),
                                        {"data": "FRED DTB3 monthly 1954-2020", "starts": 5}, trials=1),
           "btc_nsde_generator": pit.register("btc_nsde_generator", inspect.getsource(compute_nsde),
                                              {"data": "BTCUSDT daily 2018-2019, hold-out 2020", "seeds": 3}, trials=1)}
    return _json({"registered": reg, "trials": pit.trials_so_far()})


def compute_ou_lab() -> dict:
    """The lab of chapter 6: 200 exact Vasicek (Ornstein-Uhlenbeck) paths from the January 1954 bill rate with the
    fitted parameters, monthly to 2020; the terminal spread against the stationary law N(theta, sigma^2 / 2 kappa)."""
    r = load("rates")
    v = r["vasicek"]
    x = np.asarray(r["r"])
    n = len(x) - 1
    P = sim.ou_exact(x[0], v["kappa"], v["theta"], v["sigma"], n / 12, n, 200, seed=65)
    big = sim.ou_exact(x[0], v["kappa"], v["theta"], v["sigma"], n / 12, n, 20000, seed=66)[:, -1]
    return _json({"paths": P[:, ::3], "t0": float(np.asarray(r["t"])[0]), "years": n / 12, "mean_T": float(big.mean()),
                  "sd_T": float(big.std()), "theta": v["theta"],
                  "sd_inf": float(v["sigma"] / np.sqrt(2 * v["kappa"])),
                  "mean_theory": float(v["theta"] + (x[0] - v["theta"]) * np.exp(-v["kappa"] * n / 12)),
                  "sd_theory": float(v["sigma"] * np.sqrt((1 - np.exp(-2 * v["kappa"] * n / 12)) / (2 * v["kappa"]))),
                  "frac_neg_T": float(np.mean(big < 0))})


def compute_rv_theory() -> dict:
    """The research chapter: the asymptotic theory of realized variance on simulated stochastic-volatility days
    (23,400 one-second steps).  The studentized CLT (Barndorff-Nielsen and Shephard 2002) at 5-minute to 1-second
    sampling; the bias from microstructure noise and the two-scales estimator; bipower variation and the Huang-
    Tauchen jump test with and without a jump."""
    from math import gamma, pi
    from explainer.quant.house import vol as V
    rng = np.random.default_rng(505)
    N, M = 23400, 3000
    ns = (39, 78, 390, 2340, 23400)
    s0, eta = 0.30 / np.sqrt(252), 0.6          # 30% a year; intraday vol of vol
    u = np.linspace(0, 1, N + 1)
    shape = 1 + 0.6 * (2 * u - 1) ** 2           # the U-shaped intraday pattern
    shape /= np.sqrt(np.mean(shape[:-1] ** 2))
    mu43 = 2 ** (2 / 3) * gamma(7 / 6) / gamma(0.5)
    tstats = {n: [] for n in ns}
    rel = {n: [] for n in ns}
    omega = 5e-4                                 # 5 basis points of noise on each observed log price
    sig_noise = {n: [] for n in ns}
    tsrv, rv5n, ivs, inv_iv = [], [], [], []
    ht = {"none": [], "jump": []}
    for m in range(M):
        B = np.cumsum(rng.standard_normal(N)) * np.sqrt(1 / N)
        sig = s0 * shape[:-1] * np.exp(eta * np.r_[0, B[:-1]] - 0.5 * eta ** 2 * u[:-1])
        dX = sig * rng.standard_normal(N) * np.sqrt(1 / N)
        iv = float(np.sum(sig ** 2) / N)
        ivs.append(iv)
        X = np.r_[0, np.cumsum(dX)]
        for n in ns:
            r = np.diff(X[::N // n])
            rv = float(np.sum(r ** 2))
            rq = n / 3 * float(np.sum(r ** 4))
            tstats[n].append((rv - iv) / np.sqrt(2 * rq / n))
            rel[n].append(rv / iv - 1)
        if m < 1000:
            inv_iv.append(1 / iv)
            Y = X + omega * rng.standard_normal(N + 1)
            for n in ns:
                sig_noise[n].append(float(np.sum(np.diff(Y[::N // n]) ** 2)) / iv)
            tsrv.append(V.two_scale_rv(Y, K=int(round(N ** (2 / 3) / 4))) / iv)
            rv5n.append(float(np.sum(np.diff(Y[::N // 78]) ** 2)) / iv)
        # jumps: the Huang-Tauchen ratio test on 5-minute returns, with and without one jump of 1%
        for key in ("none", "jump"):
            Xj = X.copy()
            if key == "jump":
                k = rng.integers(1, N)
                Xj[k:] += 0.01 * rng.choice([-1, 1])
            r = np.diff(Xj[::N // 78])
            rv, bv = float(np.sum(r ** 2)), V.bipower_variation(r)
            a = np.abs(r) ** (4 / 3)
            tq = 78 * mu43 ** -3 * float(np.sum(a[2:] * a[1:-1] * a[:-2])) * 78 / 76
            z = ((rv - bv) / rv) / np.sqrt((pi ** 2 / 4 + pi - 5) / 78 * max(1.0, tq / bv ** 2))
            ht[key].append(z)
    out = {"N": N, "M": M, "ns": list(ns), "omega": omega, "iv_mean": float(np.mean(ivs))}
    out["clt"] = {str(n): {"cover95": float(np.mean(np.abs(tstats[n]) < 1.96)), "sd_t": float(np.std(tstats[n])),
                           "rel_sd": float(np.std(rel[n])), "hist": np.histogram(tstats[n], 40, (-4, 4))[0]}
                  for n in ns}
    out["noise"] = {"rv_over_iv": {str(n): float(np.mean(sig_noise[n])) for n in ns},
                    "bias_theory": {str(n): float(2 * n * omega ** 2 * np.mean(inv_iv)) for n in ns},
                    "tsrv_mean": float(np.mean(tsrv)), "tsrv_sd": float(np.std(tsrv)),
                    "rv5_mean": float(np.mean(rv5n)), "rv5_sd": float(np.std(rv5n))}
    out["jumps"] = {k: {"reject": float(np.mean(np.asarray(v) > 1.645))} for k, v in ht.items()}
    return _json(out)


ITEMS2 = {"construct": compute_construct, "reflection": compute_reflection, "qv_live": compute_qv_live,
          "wong_zakai": compute_wong_zakai, "lemma_column": compute_lemma_column, "picard": compute_picard,
          "cir_mle": compute_cir_mle, "fp_surface": compute_fp_surface,
          "fk_check": compute_fk_check, "girsanov_paths": compute_girsanov_paths, "is_run": compute_is_run,
          "observability": compute_observability, "hedge_rates": compute_hedge_rates, "tanaka": compute_tanaka,
          "levy_layers": compute_levy_layers, "jump_hedge": compute_jump_hedge, "hawkes_replay": compute_hawkes_replay,
          "hawkes_check": compute_hawkes_check, "hawkes_rescale": compute_hawkes_rescale,
          "fbm_morph": compute_fbm_morph, "cont_das": compute_cont_das, "helix": compute_helix,
          "sig_regression": compute_sig_regression, "wti": compute_wti, "varswap": compute_varswap,
          "nsde": compute_nsde, "nsde_eval": compute_nsde_eval, "envelope2": compute_envelope2, "ou_lab": compute_ou_lab, "rv_theory": compute_rv_theory}


ITEMS = {"variation": compute_variation, "signature": compute_signature, "ito": compute_ito, "orders": compute_orders,
         "rates": compute_rates, "girsanov": compute_girsanov, "stoploss": compute_stoploss, "jumps": compute_jumps,
         "hawkes": compute_hawkes, "rough": compute_rough, "fbm": compute_fbm, "envelope": compute_envelope, **ITEMS2}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
