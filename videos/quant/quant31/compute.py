"""Every number in Part 31 (Risk Models, Costs and Trading Through Time), computed and cached in .cache/quant31/.

    python -m videos.quant.quant31.compute [items] [--force]

The universe is Part 29's: every coin Binance has quoted in USDT, eligible on a day with 60 days of history and a
median quote volume of at least 250,000 USDT; daily closes. Research uses 2018-2020; 2021-2025 is sealed and read once,
in ``envelope``. August 2007 is replayed on Kenneth French's daily industry portfolios.

* ``model``       a Barra-style factor model of the coins: exposures, daily cross-sectional regressions, factor
                  returns, risk forecasts and Barra's bias statistic;
* ``vasicek``     raw and Vasicek-shrunk betas, and which predicts the next quarter's beta better;
* ``law``         the fundamental law simulated: IC, breadth, the transfer coefficient, a time-varying IC;
* ``costs``       the square-root law on the coins, and a capacity curve for the calm-coin signal;
* ``gp``          Garleanu and Pedersen against myopic trading, net of quadratic costs, on a fast and a slow signal;
* ``combine``     combining signals: equal, IC-weighted and ridge, trained on 2018-19, judged on 2020;
* ``attribution`` Part 29's mined alpha split into factor and specific returns;
* ``quake``       August 2007: Khandani and Lo's contrarian strategy on the daily industries;
* ``theory``      the research chapter: the information ratio with a time-varying IC, proved, simulated, measured;
* ``envelope``    the factor-neutral calm signal, traded the Garleanu-Pedersen way, registered and opened on 2021-2025.
"""

from __future__ import annotations

import functools
import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import alphas as A, pit, riskmodel as RM

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant31")
load = pit.counted(CACHE.load, 31)
START, TRAIN_END, RESEARCH_END = 20180101, 20191231, 20201231
FACTORS = ["market", "size", "beta", "volatility", "momentum", "reversal"]
BURN = 120


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _roll(fn, x, w):
    out = np.full_like(x, np.nan)
    for t in range(w - 1, x.shape[0]):
        out[t] = fn(x[t - w + 1:t + 1], axis=0)
    return out


def _exposures(F, mask):
    """Style exposures known at the close of day t, standardised across the eligible coins."""
    ret, vol = F["ret"], F["volume"]
    size = np.log(_roll(np.nanmean, vol, 20))
    sd20 = _roll(np.nanstd, ret, 20)
    csum = np.nancumsum(np.nan_to_num(ret), axis=0)
    mom = np.full_like(ret, np.nan)
    mom[60:] = csum[54:-6] - csum[:-60]                  # days t-59 .. t-6
    rev = np.full_like(ret, np.nan)
    rev[5:] = csum[5:] - csum[:-5]                       # the last five days
    mkt = np.array([np.nanmean(np.where(mask[t], ret[t], np.nan)) for t in range(ret.shape[0])])
    beta = np.full_like(ret, np.nan)
    for t in range(60, ret.shape[0]):
        m = mkt[t - 59:t + 1]
        r = ret[t - 59:t + 1]
        mm = m - np.nanmean(m)
        beta[t] = np.nanmean((r - np.nanmean(r, 0)) * mm[:, None], 0) / np.nanvar(m)
    raw = {"size": size, "beta": beta, "volatility": sd20, "momentum": mom, "reversal": rev}
    X = np.stack([np.where(mask, 1.0, np.nan)] + [RM.standardise(raw[k], mask) for k in FACTORS[1:]], -1)
    return X, raw, mkt


@functools.lru_cache(maxsize=None)
def _panel(full: bool = False):
    from videos.quant.quant29 import compute as Q29
    if not full:
        d, names, F, fwd, mask, train, valid = Q29._research()
        return d, names, F, fwd, mask
    dates, names, G = Q29._full_grid()
    lo = int(np.searchsorted(dates, START)) - 30
    rows = np.arange(lo, len(dates))
    cols = np.arange(len(names))
    F, fwd = Q29._fields(G, rows, cols)
    m = Q29._mask(G, rows, cols)
    m[:30] = False
    return dates[rows], names, F, fwd, m


@functools.lru_cache(maxsize=None)
def _fitted(full: bool = False):
    d, names, F, fwd, mask = _panel(full)
    X, raw, mkt = _exposures(F, mask)
    w = np.sqrt(np.where(mask, _roll(np.nanmean, F["volume"], 20), np.nan))
    R = np.where(mask, fwd, np.nan)
    f, u = RM.factor_returns(R, X, w)
    return d, names, F, fwd, mask, X, raw, mkt, f, u


# ---------------------------------------------------------------------------
# The factor model
# ---------------------------------------------------------------------------
def compute_model() -> dict:
    d, names, F, fwd, mask, X, raw, mkt, f, u = _fitted()
    T, N, K = X.shape
    # cross-sectional R^2 of each day's regression
    r2 = []
    for t in range(T):
        m = np.isfinite(u[t]) & np.isfinite(fwd[t])
        if m.sum() > 20:
            y = fwd[t, m]
            r2.append(1 - np.sum(u[t, m] ** 2) / np.sum((y - y.mean()) ** 2))
    # risk forecasts made at t from factor returns up to t-1, scored on the return to t+1
    Fc = RM.ewma_cov(np.where(np.isfinite(f), f, np.nan), 60)
    sv = RM.specific_var(u, 60)
    rng = np.random.default_rng(3101)
    ports = {"equal-weighted coins": [], "random long-short": [], "volatility factor": [], "single coins": []}
    for t in range(BURN, T - 1):
        m = mask[t] & np.isfinite(X[t]).all(1) & np.isfinite(sv[t - 1]) & np.isfinite(fwd[t])
        if m.sum() < 20 or not np.isfinite(Fc[t - 1]).all():
            continue
        Xt, St, Fv = X[t, m], sv[t - 1, m], Fc[t - 1]
        n = m.sum()
        books = {"equal-weighted coins": np.full(n, 1 / n),
                 "random long-short": (lambda z: z / np.abs(z).sum() * 2)(rng.standard_normal(n)),
                 "volatility factor": (lambda z: z / np.abs(z).sum() * 2)(Xt[:, 3] - Xt[:, 3].mean())}
        for k, h in books.items():
            var = float(h @ Xt @ Fv @ Xt.T @ h + np.sum(h ** 2 * St))
            ports[k].append(float(h @ fwd[t, m]) / math.sqrt(var))
        j = rng.integers(n)
        e = np.zeros(n)
        e[j] = 1
        var = float(e @ Xt @ Fv @ Xt.T @ e + St[j])
        ports["single coins"].append(float(fwd[t, m][j]) / math.sqrt(var))
    bias = {k: RM.bias_statistic(v) for k, v in ports.items()}
    ok = np.isfinite(f).all(1)
    cum = np.nancumsum(np.where(ok[:, None], f, 0.0), axis=0)
    fstats = {k: {"vol": float(np.nanstd(f[ok, i]) * math.sqrt(365)), "mean": float(np.nanmean(f[ok, i]) * 365),
                  "t": float(np.nanmean(f[ok, i]) / np.nanstd(f[ok, i]) * math.sqrt(ok.sum()))} for i, k in enumerate(FACTORS)}
    # share of a typical coin's variance that the factors explain
    fac_share = []
    for t in range(BURN, T - 1, 5):
        m = mask[t] & np.isfinite(X[t]).all(1) & np.isfinite(sv[t - 1])
        if m.sum() < 20 or not np.isfinite(Fc[t - 1]).all():
            continue
        fv = np.einsum("nk,kl,nl->n", X[t, m], Fc[t - 1], X[t, m])
        fac_share.append(float(np.median(fv / (fv + sv[t - 1, m]))))
    corr = np.corrcoef(f[ok].T)
    return _json({"factors": FACTORS, "r2_mean": float(np.mean(r2)), "r2_median": float(np.median(r2)),
                  "bias": bias, "cum": cum, "dates": d, "fstats": fstats, "fac_share": float(np.median(fac_share)),
                  "n_days": int(ok.sum()), "median_n": float(np.median(mask.sum(1)[mask.sum(1) > 0])), "corr": corr})


def compute_vasicek() -> dict:
    d, names, F, fwd, mask, X, raw, mkt, f, u = _fitted()
    ret = F["ret"]
    T = ret.shape[0]
    errs = {"raw": [], "shrunk": [], "one": []}
    ws = []
    ex = None
    for t0 in range(60, T - 120, 60):
        a, b = slice(t0, t0 + 60), slice(t0 + 60, t0 + 120)
        live = mask[t0:t0 + 120].all(0)
        if live.sum() < 15:
            continue
        m1, m2 = mkt[a], mkt[b]
        B1, S1, B2 = [], [], []
        for j in np.flatnonzero(live):
            y1, y2 = ret[a, j], ret[b, j]
            ok1, ok2 = np.isfinite(y1) & np.isfinite(m1), np.isfinite(y2) & np.isfinite(m2)
            if ok1.sum() < 40 or ok2.sum() < 40:
                continue
            c1 = np.polyfit(m1[ok1], y1[ok1], 1)
            res = y1[ok1] - np.polyval(c1, m1[ok1])
            se = res.std(ddof=2) / (m1[ok1].std() * math.sqrt(ok1.sum()))
            B1.append(c1[0]); S1.append(se)
            B2.append(np.polyfit(m2[ok2], y2[ok2], 1)[0])
        if len(B1) < 15:
            continue
        B1, S1, B2 = map(np.array, (B1, S1, B2))
        Bs, w = RM.vasicek(B1, S1)
        errs["raw"].append(np.mean((B1 - B2) ** 2))
        errs["shrunk"].append(np.mean((Bs - B2) ** 2))
        errs["one"].append(np.mean((1 - B2) ** 2))
        ws.append(float(np.mean(w)))
        ex = {"raw": B1, "shrunk": Bs, "next": B2}
    return _json({"mse": {k: float(np.mean(v)) for k, v in errs.items()}, "weight": float(np.mean(ws)),
                  "n_windows": len(errs["raw"]), "example": ex})


# ---------------------------------------------------------------------------
# The fundamental law, simulated
# ---------------------------------------------------------------------------
def compute_law() -> dict:
    rng = np.random.default_rng(3102)
    rows = []
    for N in (10, 50, 100, 500):
        for sd in (0.0, 0.05, 0.1):
            irs = [RM.simulate_ic_strategy(N, 1000, 0.05, sd, rng)[0] for _ in range(8)]
            rows.append({"N": N, "ic_sd": sd, "sim": float(np.mean(irs)), "formula": RM.ir_time_varying(0.05, sd, N),
                         "naive": RM.fundamental_ir(0.05, N)})
    # the transfer coefficient of a long-only constraint: correlation of long-only weights with unconstrained ones
    tcs = []
    for _ in range(200):
        z = rng.standard_normal(500)
        w_u = z - z.mean()
        w_l = np.maximum(z, 0) - np.maximum(z, 0).mean() * 0          # long the positive scores
        w_l = np.maximum(z, 0)
        w_l = w_l / w_l.sum() - 1 / 500                            # active weights against equal-weighted benchmark
        tcs.append(np.corrcoef(w_u, w_l)[0, 1])
    return _json({"rows": rows, "tc_long_only": float(np.mean(tcs))})


# ---------------------------------------------------------------------------
# Costs and capacity
# ---------------------------------------------------------------------------
def _calm_book(F, mask):
    s = -_roll(np.nanstd, F["ret"], 20)                           # calm coins long, wild ones short
    R = A.rank(np.where(mask, s, np.nan))
    W = np.zeros_like(R)
    for t in range(R.shape[0]):
        m = np.isfinite(R[t])
        if m.sum() >= 10:
            v = R[t, m] - R[t, m].mean()
            W[t, m] = v / np.abs(v).sum() * 2
    return W


def compute_costs() -> dict:
    d, names, F, fwd, mask, X, raw, mkt, f, u = _fitted()
    W = _calm_book(F, mask)
    adv = _roll(np.nanmean, F["volume"], 20)                       # USDT a day
    sig = _roll(np.nanstd, F["ret"], 20)
    gross = np.nansum(W * np.nan_to_num(fwd), 1)
    live = (np.abs(W).sum(1) > 0) & (np.arange(len(d)) >= BURN)
    dW = np.abs(np.diff(W, axis=0, prepend=W[:1]))
    out = []
    for aum in (1e5, 1e6, 1e7, 3e7, 1e8, 3e8, 1e9):
        q = dW * aum                                               # dollars traded per coin per day
        c = np.nansum(q * RM.sqrt_impact(q, np.where(adv > 0, adv, np.nan), sig), 1) / aum
        net = gross - c - np.nansum(dW, 1) * 5e-4                  # plus 5 bp fees per dollar traded
        r = net[live]
        out.append({"aum": aum, "sharpe": float(r.mean() / r.std(ddof=1) * math.sqrt(365)),
                    "cost_day": float(np.mean(c[live])), "gross_day": float(np.mean(gross[live]))})
    r = gross[live]
    med_adv = float(np.nanmedian(adv[mask]))
    med_sig = float(np.nanmedian(sig[mask]))
    return _json({"curve": out, "gross_sharpe": float(r.mean() / r.std(ddof=1) * math.sqrt(365)),
                  "turnover": float(np.mean(np.nansum(dW, 1)[live])), "median_adv": med_adv, "median_sigma": med_sig,
                  "cost_1m": float(RM.sqrt_impact(1e6, med_adv, med_sig))})


# ---------------------------------------------------------------------------
# Garleanu and Pedersen against myopic trading
# ---------------------------------------------------------------------------
def _signals(F, mask):
    calm = RM.standardise(-_roll(np.nanstd, F["ret"], 20), mask)
    csum = np.nancumsum(np.nan_to_num(F["ret"]), axis=0)
    rev = np.full_like(calm, np.nan)
    rev[3:] = csum[3:] - csum[:-3]
    fast = RM.standardise(-rev, mask)
    return {"slow": calm, "fast": fast}


def _phi(z, mask):
    ac = []
    for t in range(1, z.shape[0]):
        m = mask[t] & mask[t - 1] & np.isfinite(z[t]) & np.isfinite(z[t - 1])
        if m.sum() > 20:
            ac.append(np.corrcoef(z[t, m], z[t - 1, m])[0, 1])
    return float(1 - np.mean(ac))


def _ic(z, fwd, mask, idx):
    return float(A.score(A.ic_series(z, fwd, mask), idx)["ic"])


def _gp_run(z, fwd, mask, sig2, coef, gamma, lam, phi, idx, mode):
    """Holdings per coin with Sigma = diag(sig2): Markowitz x* = sum_k coef_k z_k / (gamma sig2); myopic trades to it
    each day, GP trades a fraction of the way to its aim portfolio (fast signals discounted). Returns net daily P&L."""
    T, N = z["slow"].shape
    x = np.zeros(N)
    pnl = []
    rate = RM.gp_trade_rate(gamma, lam, 0.0005) if mode == "gp" else 1.0
    for t in range(T - 1):
        m = mask[t] & np.isfinite(sig2[t]) & np.isfinite(z["slow"][t]) & np.isfinite(z["fast"][t])
        tgt = np.zeros(N)
        for k in ("slow", "fast"):
            wk = RM.gp_aim_weight(gamma, lam, 0.0005, phi[k]) if mode == "gp" else 1.0
            tgt[m] += wk * coef[k] * z[k][t, m] / (gamma * sig2[t, m])
        tgt[~m] = 0.0
        x_new = x + rate * (tgt - x)
        cost = 0.5 * lam * np.nansum(np.nan_to_num(sig2[t]) * (x_new - x) ** 2)
        gain = np.nansum(x_new * np.nan_to_num(fwd[t]))
        x = x_new
        if t in idx:
            pnl.append(gain - cost)
    return np.array(pnl)


def compute_gp() -> dict:
    d, names, F, fwd, mask, X, raw, mkt, f, u = _fitted()
    z = _signals(F, mask)
    idx_tr = np.flatnonzero((d >= START) & (d <= TRAIN_END) & (np.arange(len(d)) >= BURN))
    idx_all = set(np.flatnonzero((d >= START) & (d <= RESEARCH_END) & (np.arange(len(d)) >= BURN)).tolist())
    phi = {k: _phi(z[k], mask) for k in z}
    sig = _roll(np.nanstd, F["ret"], 60)
    sig2 = sig ** 2
    # each signal's expected return per unit of score: IC x volatility (Grinold's alpha = IC x sigma x z)
    coef = {k: _ic(z[k], fwd, mask, idx_tr) * float(np.nanmedian(sig[mask])) for k in z}
    gamma = 1.0
    out = []
    for lam in (0.0, 0.5, 2.0, 8.0, 32.0):
        row = {"lam": lam}
        for mode in ("myopic", "gp"):
            p = _gp_run(z, fwd, mask, sig2, coef, gamma, max(lam, 1e-9), phi, idx_all, mode)
            row[mode] = float(p.mean() / p.std(ddof=1) * math.sqrt(365))
            row[mode + "_mean"] = float(p.mean() * 365)
        row["rate"] = RM.gp_trade_rate(gamma, max(lam, 1e-9), 0.0005)
        row["w_fast"] = RM.gp_aim_weight(gamma, max(lam, 1e-9), 0.0005, phi["fast"])
        row["w_slow"] = RM.gp_aim_weight(gamma, max(lam, 1e-9), 0.0005, phi["slow"])
        out.append(row)
    return _json({"phi": phi, "coef": coef, "rows": out, "half_life": {k: math.log(0.5) / math.log(1 - v) for k, v in
                                                                           phi.items()}})


# ---------------------------------------------------------------------------
# Combining signals
# ---------------------------------------------------------------------------
def compute_combine() -> dict:
    d, names, F, fwd, mask, X, raw, mkt, f, u = _fitted()
    sigs = {k: X[..., i] for i, k in enumerate(FACTORS) if k != "market"}
    sigs["mined"] = RM.standardise(A.evaluate(("ts_mean", ("ts_min", ("div", ("field", "vwap"), ("field", "high")), 5), 20), F),
                                   mask)
    tr = np.flatnonzero((d >= START) & (d <= TRAIN_END) & (np.arange(len(d)) >= BURN))
    va = np.flatnonzero((d > TRAIN_END) & (d <= RESEARCH_END))
    ic = {k: A.score(A.ic_series(v, fwd, mask), tr)["ic"] for k, v in sigs.items()}
    ic_v = {k: A.score(A.ic_series(v, fwd, mask), va)["ic"] for k, v in sigs.items()}
    keys = list(sigs)
    Z = np.stack([np.nan_to_num(sigs[k]) for k in keys], -1)
    # ridge regression of the next-day return on the signals, pooled over the training days
    Xs = Z[tr][mask[tr]]
    ys = np.nan_to_num(fwd[tr][mask[tr]])
    out = {}
    for lam in (0.0, 1e2, 1e4, 1e6):
        b = np.linalg.solve(Xs.T @ Xs + lam * np.eye(len(keys)), Xs.T @ ys)
        comb = Z @ b
        out[f"ridge {lam:g}"] = {"w": b / np.abs(b).sum(), "train": A.score(A.ic_series(comb, fwd, mask), tr)["ic"],
                                 "valid": A.score(A.ic_series(comb, fwd, mask), va)["ic"]}
    sgn = np.array([np.sign(ic[k]) for k in keys])
    for name, w in (("equal", sgn / len(keys)), ("IC-weighted", np.array([ic[k] for k in keys]))):
        comb = Z @ w
        out[name] = {"w": w / np.abs(w).sum(), "train": A.score(A.ic_series(comb, fwd, mask), tr)["ic"],
                     "valid": A.score(A.ic_series(comb, fwd, mask), va)["ic"]}
    C = np.corrcoef(np.stack([A.ic_series(sigs[k], fwd, mask)[tr] for k in keys]))
    return _json({"keys": keys, "ic_train": ic, "ic_valid": ic_v, "combos": out, "ic_corr": C})


# ---------------------------------------------------------------------------
# Attribution of Part 29's mined alpha
# ---------------------------------------------------------------------------
def compute_attribution() -> dict:
    d, names, F, fwd, mask, X, raw, mkt, f, u = _fitted()
    s = A.evaluate(("ts_mean", ("ts_min", ("div", ("field", "vwap"), ("field", "high")), 5), 20), F)
    R = A.rank(np.where(mask, s, np.nan))
    fac, spec, tot = [], [], []
    for t in range(BURN, len(d) - 1):
        m = np.isfinite(R[t]) & np.isfinite(X[t]).all(1) & np.isfinite(u[t])
        if m.sum() < 20 or not np.isfinite(f[t]).all():
            continue
        h = np.zeros(len(names))
        v = R[t, m] - R[t, m].mean()
        h[m] = v / np.abs(v).sum() * 2
        hx = h[m] @ X[t, m]
        fac.append(hx * f[t])
        spec.append(float(h[m] @ u[t, m]))
        tot.append(float(h[m] @ fwd[t, m]))
    fac, spec, tot = np.array(fac), np.array(spec), np.array(tot)
    mean_fac = fac.mean(0) * 365
    var_tot = tot.var()
    return _json({"factors": FACTORS, "mean_total": float(tot.mean() * 365), "mean_factor": mean_fac,
                  "mean_specific": float(spec.mean() * 365), "var_share_factor": float(np.var(fac.sum(1)) / var_tot),
                  "sharpe_total": float(tot.mean() / tot.std() * math.sqrt(365)),
                  "sharpe_specific": float(spec.mean() / spec.std() * math.sqrt(365)),
                  "cum_total": np.cumsum(tot), "cum_specific": np.cumsum(spec), "cum_factor": np.cumsum(fac.sum(1))})


# ---------------------------------------------------------------------------
# August 2007
# ---------------------------------------------------------------------------
def compute_quake() -> dict:
    dd = data.ken_french_industries_daily(49, through="2020-12-31")
    D, R = dd["date"], np.nan_to_num(dd["returns"])
    m = D >= 19900101
    D, R = D[m], R[m]
    mk = R.mean(1)
    W = -(R - mk[:, None]) / R.shape[1]                         # Khandani and Lo's contrarian weights
    W = W / np.abs(W).sum(1, keepdims=True)
    pnl = np.r_[np.nan, np.sum(W[:-1] * R[1:], 1)]
    k = (D >= 20070701) & (D <= 20070831)
    days = D[k]
    cum = np.nancumsum(pnl[k])
    aug = {int(x): float(p) for x, p in zip(D[k], pnl[k]) if 20070806 <= x <= 20070810}
    sd = np.nanstd(pnl[(D >= 20060101) & (D < 20070701)])
    yr = (D >= 19970101) & (D <= 20070630)
    return _json({"days": days, "cum": cum, "aug": aug, "sd_before": float(sd),
                  "sharpe_1997_2007": float(np.nanmean(pnl[yr]) / np.nanstd(pnl[yr]) * math.sqrt(252))})


# ---------------------------------------------------------------------------
# Research: the information ratio with a time-varying IC
# ---------------------------------------------------------------------------
def compute_theory() -> dict:
    rng = np.random.default_rng(3103)
    sims = []
    for N in (20, 50, 100, 200, 500, 1000):
        for sd in (0.03, 0.08):
            irs = [RM.simulate_ic_strategy(N, 1500, 0.04, sd, rng)[0] for _ in range(6)]
            sims.append({"N": N, "ic_sd": sd, "sim": float(np.mean(irs)), "sim_sd": float(np.std(irs)),
                         "formula": RM.ir_time_varying(0.04, sd, N), "naive": RM.fundamental_ir(0.04, N),
                         "limit": 0.04 / sd})
    # the coins: each signal's IC mean and standard deviation, the average breadth, and its realised long-short Sharpe
    d, names, F, fwd, mask, X, raw, mkt, f, u = _fitted()
    idx = np.flatnonzero((d >= START) & (d <= RESEARCH_END) & (np.arange(len(d)) >= BURN))
    sigs = {k: X[..., i] for i, k in enumerate(FACTORS) if k != "market"}
    sigs["mined"] = RM.standardise(A.evaluate(("ts_mean", ("ts_min", ("div", ("field", "vwap"), ("field", "high")), 5), 20), F),
                                   mask)
    rows = []
    for k, z in sigs.items():
        ic = A.ic_series(z, fwd, mask)[idx]
        ok = np.isfinite(ic)
        mu, sd = float(ic[ok].mean()), float(ic[ok].std(ddof=1))
        n = float(np.mean(mask[idx][ok].sum(1)))
        ls = A.ls_returns(z, fwd, mask)[idx]
        ls = ls[np.isfinite(ls)]
        sr = float(abs(ls.mean()) / ls.std(ddof=1))
        Rk = A.rank(np.where(mask, z, np.nan))
        pe = []
        for t in idx:
            mm = np.isfinite(Rk[t]) & np.isfinite(fwd[t])
            if mm.sum() >= 10:
                ww = Rk[t, mm] - Rk[t, mm].mean()
                pe.append(np.corrcoef(ww, fwd[t, mm])[0, 1])
        pe = np.array(pe)
        disp = np.array([np.nanstd(np.where(mask[t], fwd[t], np.nan)) for t in idx])
        okd = ok & np.isfinite(disp)
        p_ = ic[okd] * disp[okd]
        rows.append({"signal": k, "ic": mu, "ic_sd": sd, "N": n, "naive": abs(mu) * math.sqrt(n),
                     "formula": abs(RM.ir_time_varying(mu, sd, int(n))), "realised": sr,
                     "noise_sd": math.sqrt((1 - mu ** 2) / n),
                     "with_dispersion": float(abs(p_.mean()) / p_.std(ddof=1)),
                     "disp_cv": float(disp[okd].std() / disp[okd].mean()),
                     "corr_ic_disp": float(np.corrcoef(np.abs(ic[okd]), disp[okd])[0, 1]),
                     "pearson": float(pe.mean()), "pearson_sd": float(pe.std(ddof=1)),
                     "pearson_ir": float(abs(pe.mean()) / pe.std(ddof=1))})
    r_all = fwd[idx][mask[idx]]
    r_all = r_all[np.isfinite(r_all)]
    from scipy.stats import kurtosis
    return _json({"sims": sims, "coins": rows, "kurtosis": float(kurtosis(r_all))})


STRATEGY = "gp_calm_reversal_part31"
LAM_REG = 8.0


def compute_envelope() -> dict:
    import inspect
    from explainer.quant.house import track
    g = load("gp")
    n_trials = 2 * len(g["rows"])                              # every cost level and mode compared in ``gp``
    code = inspect.getsource(_gp_run) + inspect.getsource(_signals) + inspect.getsource(RM.gp_trade_rate) + \
        inspect.getsource(RM.gp_aim_weight)
    pit.register(STRATEGY, code, {"signals": "calm (-20d vol) and 3-day reversal, standardised",
                                  "rule": "Garleanu-Pedersen aim portfolio, gamma 1, lambda 8, rho 0.0005",
                                  "parameters": "phi and coefficients fixed on 2018-2020",
                                  "cost": "quadratic (lambda/2) sigma^2 dx^2 inside the P&L"}, trials=n_trials)
    d, names, F, fwd, mask = _panel(True)
    fin = np.isfinite(fwd)
    pit.open_envelope(STRATEGY, "binance/usdt_daily_returns", d, np.where(fin, np.round(fwd, 8), -999.0))
    z = _signals(F, mask)
    sig2 = _roll(np.nanstd, F["ret"], 60) ** 2
    idx_res = set(np.flatnonzero((d >= START) & (d <= RESEARCH_END) & (np.arange(len(d)) >= BURN)).tolist())
    idx_hold = set(np.flatnonzero(d > RESEARCH_END).tolist())
    out = {}
    for mode in ("gp", "myopic"):
        p_res = _gp_run(z, fwd, mask, sig2, g["coef"], 1.0, LAM_REG, g["phi"], idx_res, mode)
        p_hold = _gp_run(z, fwd, mask, sig2, g["coef"], 1.0, LAM_REG, g["phi"], idx_hold, mode)
        out[mode] = {"sr_res": float(p_res.mean() / p_res.std(ddof=1) * math.sqrt(365)),
                     "sr_hold": float(p_hold.mean() / p_hold.std(ddof=1) * math.sqrt(365)),
                     "cum_hold": np.cumsum(p_hold) / (p_res.std(ddof=1) * math.sqrt(365)) * 0.10}
        if mode == "gp":
            dd_res = np.array(sorted(idx_res))
            dd_hold = np.array(sorted(idx_hold))
            dd_hold = dd_hold[dd_hold < len(d) - 1]

            sc = 0.10 / (p_res.std(ddof=1) * math.sqrt(365))
            mr = np.array([np.sum(p_res[d[dd_res[:len(p_res)]] // 100 == k]) * sc for k in np.unique(d[dd_res[:len(p_res)]] // 100)])
            mh = np.array([np.sum(p_hold[d[dd_hold[:len(p_hold)]] // 100 == k]) * sc for k in np.unique(d[dd_hold[:len(p_hold)]] // 100)])
            row = track.record(STRATEGY, 31, mr, mh, 0.0, note="GP-traded calm and reversal signals on Binance coins, "
                               "net of the quadratic cost model, scaled to 10% research volatility")
            out["row"] = row
            out["hold_dates"] = d[dd_hold[:len(p_hold)]]
    # diagnosis of the registered rule's sealed-years P&L (not a new strategy): which coins drove it
    diag = _diagnose(z, fwd, mask, sig2, g["coef"], 1.0, LAM_REG, g["phi"], idx_hold, names)
    return _json({"trials": pit.trials_so_far(), "n_trials": n_trials, "res": out, "lam": LAM_REG, "diag": diag})


def _diagnose(z, fwd, mask, sig2, coef, gamma, lam, phi, idx, names):
    """Replay the registered GP rule and split its daily P&L by coin: those whose 60-day volatility fell below 0.5%
    (frozen listings and stablecoins, where 1/sigma^2 explodes) and the rest; and count the affected days."""
    T, N = z["slow"].shape
    x = np.zeros(N)
    rate = RM.gp_trade_rate(gamma, lam, 0.0005)
    p_low, p_rest, bad_days = [], [], 0
    low_names = set()
    for t in range(T - 1):
        m = mask[t] & np.isfinite(sig2[t]) & np.isfinite(z["slow"][t]) & np.isfinite(z["fast"][t])
        tgt = np.zeros(N)
        for k in ("slow", "fast"):
            tgt[m] += RM.gp_aim_weight(gamma, lam, 0.0005, phi[k]) * coef[k] * z[k][t, m] / (gamma * sig2[t, m])
        tgt[~m] = 0.0
        x_new = x + rate * (tgt - x)
        cost = 0.5 * lam * np.nan_to_num(sig2[t]) * (x_new - x) ** 2
        gain = x_new * np.nan_to_num(fwd[t]) - cost
        x = x_new
        if t in idx:
            low = m & (sig2[t] < 0.005 ** 2)
            for j in np.flatnonzero(low):
                low_names.add(names[j])
            p_low.append(float(np.nansum(np.where(low, gain, 0.0))))
            p_rest.append(float(np.nansum(np.where(low, 0.0, gain))))
            bad_days += int(low.any())
    p_low, p_rest = np.array(p_low), np.array(p_rest)
    tot = p_low + p_rest
    return {"low_vol_coins": sorted(low_names), "days_affected": bad_days, "n_days": int(len(tot)),
            "var_share_low": float(np.var(p_low) / np.var(tot)) if np.var(tot) > 0 else float("nan"),
            "sr_total": float(tot.mean() / tot.std(ddof=1) * math.sqrt(365)),
            "sr_rest": float(p_rest.mean() / p_rest.std(ddof=1) * math.sqrt(365))}


ITEMS = {"model": compute_model, "vasicek": compute_vasicek, "law": compute_law, "costs": compute_costs,
         "gp": compute_gp, "combine": compute_combine, "attribution": compute_attribution, "quake": compute_quake,
         "theory": compute_theory, "envelope": compute_envelope}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
