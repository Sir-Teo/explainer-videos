"""Every number in Part 33 (Statistical Arbitrage), computed and cached in .cache/quant33/.

    python -m videos.quant.quant33.compute [items] [--force]

The universe is Kenneth French's 49 daily US industry portfolios (research through 2020; 2021-2025 sealed), with his
size deciles for lead-lag, Cboe's VIX for liquidity, and Binance's BTC and ETH for a hedge ratio that moves.

* ``pairs``     the distance method (Gatev, Goetzmann and Rouwenhorst) on the industries, 1964-2020, by decade;
* ``coint``     Engle-Granger on every pair of industries, year by year: how many pass, how many still pass a year
                later, their half-lives;
* ``pca``       Avellaneda and Lee's residual s-scores on the industries, 1995-2020, with the configurations compared;
* ``kalman``    BTC against ETH: rolling OLS and Kalman hedge ratios, and the spreads they make;
* ``lomac``     the Lo-MacKinlay decomposition of contrarian profits for size deciles and industries;
* ``nagel``     the contrarian's monthly return against the VIX (Nagel 2012);
* ``deep``      a small network trained on residual paths against the s-score rule;
* ``theory``    the research chapter: the optimal band for an OU spread, its universal curve, simulations, the data;
* ``envelope``  the residual s-score book, registered and opened on 2021-2025.
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
from explainer.quant.house import pit, statarb as SA, systematic as SY, vol as V

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant33")
load = pit.counted(CACHE.load, 33)
RESEARCH_END = 20201231
COST = 5e-4      # 5 bp per dollar traded, each side


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


@functools.lru_cache(maxsize=None)
def _ind(full: bool = False):
    d = data.ken_french_industries_daily(49, through="2025-12-31" if full else "2020-12-31")
    return d["date"], d["returns"], d["columns"]


def _stats(r, ann=252):
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    return {"mean": float(r.mean() * ann), "vol": float(r.std(ddof=1) * math.sqrt(ann)), "sharpe": SY.sharpe(r, ann),
            "maxdd": SY.max_drawdown(r), "n": int(len(r))}


# ---------------------------------------------------------------------------
# Pairs by distance
# ---------------------------------------------------------------------------
def compute_pairs() -> dict:
    d, R, cols = _ind()
    m = d >= 19630101
    d, R = d[m], R[m]
    ok = np.isfinite(R).all(0)
    R = R[:, ok]
    names = [c for c, o in zip(cols, ok) if o]
    halves = sorted(set((d // 10000) * 10 + ((d // 100) % 100 > 6)))
    idx = {h: np.flatnonzero((d // 10000) * 10 + ((d // 100) % 100 > 6) == h) for h in halves}
    daily = np.full(len(d), np.nan)
    trips, opened, examples = [], [], None
    for k in range(2, len(halves)):
        form = np.r_[idx[halves[k - 2]], idx[halves[k - 1]]]
        trade = idx[halves[k]]
        P = SA.norm_prices(R[form])
        prs = SA.distance_pairs(P, top=20)
        rets = []
        nt = 0
        for i, j, sd in prs:
            rr, tr = SA.trade_pair(R[trade, i], R[trade, j], sd)
            rets.append(rr)
            nt += tr
        daily[trade] = np.mean(rets, 0)
        trips.append(nt / len(prs))
        opened.append(np.mean([np.any(r != 0) for r in rets]))
        if halves[k] == 20081:
            i, j, sd = prs[0]
            examples = {"pair": [names[i], names[j]], "sd": sd, "pi": SA.norm_prices(R[trade, i][:, None])[:, 0],
                        "pj": SA.norm_prices(R[trade, j][:, None])[:, 0], "dates": d[trade]}
    live = np.isfinite(daily)
    dec = {}
    for y0 in range(1960, 2020, 10):
        k = live & (d // 10000 >= y0) & (d // 10000 < y0 + 10)
        if k.sum() > 100:
            dec[str(y0)] = _stats(daily[k])
    # with costs: 4 one-way trades per round trip on two legs; approximate the annual cost from round trips
    cost_year = float(np.mean(trips) * 2 * 2 * COST * 2)
    return _json({"all": _stats(daily[live]), "decades": dec, "trips": float(np.mean(trips)),
                  "opened": float(np.mean(opened)), "cost_year": cost_year, "example": examples,
                  "cum": np.cumsum(np.nan_to_num(daily[live]))[::10], "dates": d[live][::10], "n_ind": len(names)})


# ---------------------------------------------------------------------------
# Cointegration, year by year
# ---------------------------------------------------------------------------
def compute_coint() -> dict:
    d, R, cols = _ind()
    m = d >= 19900101
    d, R = d[m], R[m]
    ok = np.isfinite(R).all(0)
    R = R[:, ok]
    L = np.log(SA.norm_prices(R))
    yrs = list(range(1991, 2021))
    N = R.shape[1]
    pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    rng = np.random.default_rng(3301)
    sample = [pairs[k] for k in rng.choice(len(pairs), size=300, replace=False)]
    passed = {}
    frac, hl = [], []
    for y in yrs:
        k = d // 10000 == y
        s = set()
        for i, j in sample:
            eg = V.engle_granger(L[k, i], L[k, j])
            if eg["cointegrated_5pct"]:
                s.add((i, j))
                f = SA.ou_fit(eg["resid"])
                if np.isfinite(f["half_life"]):
                    hl.append(f["half_life"])
        passed[y] = s
        frac.append(len(s) / len(sample))
    persist = []
    for y in yrs[:-1]:
        if passed[y]:
            persist.append(len(passed[y] & passed[y + 1]) / len(passed[y]))
    # the same test on independent random walks of the same length: the false-positive rate
    fp = []
    for _ in range(300):
        a = np.cumsum(rng.standard_normal(252))
        b = np.cumsum(rng.standard_normal(252))
        fp.append(V.engle_granger(a, b)["cointegrated_5pct"])
    return _json({"years": yrs, "frac": frac, "persist": float(np.mean(persist)), "persist_series": persist,
                  "half_life_median": float(np.median(hl)), "half_lives": np.array(hl)[:2000],
                  "false_positive": float(np.mean(fp)), "n_pairs": len(sample)})


# ---------------------------------------------------------------------------
# Avellaneda-Lee residuals
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def _curve():
    cs = np.linspace(0.0, 3.0, 31)
    return cs, SA.band_curve(cs)


def _residual_book(d, R, n_fac=5, window=60, bands=(1.25, 0.5, 0.75), start=19940101, refit=21, return_scores=False,
                   return_gross=False):
    """Daily: correlation-PCA on the trailing 252 days (refit every ``refit`` days), the top ``n_fac`` eigenportfolios;
    each industry's last ``window`` days regressed on them; the cumulative residual's s-score; open long below
    -bands[0], short above +bands[0], close long above -bands[1], short below +bands[2]. P&L: the position times the
    next day's residual return, equal dollar risk per open position, gross one; costs per dollar traded."""
    T, N = R.shape
    i0 = int(np.searchsorted(d, start))
    pos = np.zeros(N)
    pnl = np.full(T, np.nan)
    gross_pnl = np.full(T, np.nan)
    turn = np.zeros(T)
    S_all = np.full((T, N), np.nan) if return_scores else None
    E = None
    for t in range(max(i0, 252), T - 1):
        if E is None or (t - i0) % refit == 0:
            X = R[t - 251:t + 1]
            mu, sd = X.mean(0), X.std(0)
            Z = (X - mu) / sd
            C = np.corrcoef(Z.T)
            w, v = np.linalg.eigh(C)
            E = v[:, ::-1][:, :n_fac] / sd[:, None]          # eigenportfolio weights on returns
        F = R[t - window + 1:t + 1] @ E                       # factor returns
        A = np.column_stack([np.ones(window), F])
        B, *_ = np.linalg.lstsq(A, R[t - window + 1:t + 1], rcond=None)
        U = R[t - window + 1:t + 1] - A @ B                   # residuals, window x N
        Xc = np.cumsum(U, 0)
        s = np.full(N, np.nan)
        band_j = np.full(N, np.nan)
        for j in range(N):
            f = SA.ou_fit(Xc[:, j])
            if np.isfinite(f["kappa"]) and f["s_eq"] > 0 and f["half_life"] < window / 2:
                s[j] = (Xc[-1, j] - f["theta"]) / f["s_eq"]
                if bands == "theory":
                    # the research chapter's band: m*/s_eq from the universal curve at c/s_eq, with the round trip
                    # costing 2 sides x 5 bp x (1 + the hedge's gross), in the residual's units
                    c_rt = 2 * COST * (1 + float(np.abs(E @ B[1:, j]).sum()))
                    cs, ms = _curve()
                    band_j[j] = float(np.interp(c_rt / f["s_eq"], cs, ms))
        if return_scores:
            S_all[t] = s
        new = pos.copy()
        for j in range(N):
            if bands == "theory":
                if not np.isfinite(s[j]):
                    new[j] = 0
                elif pos[j] == 0 and abs(s[j]) > band_j[j]:
                    new[j] = -np.sign(s[j])
                elif pos[j] != 0 and s[j] * pos[j] >= 0:
                    new[j] = 0
                continue
            if not np.isfinite(s[j]):
                new[j] = 0
            elif pos[j] == 0 and s[j] < -bands[0]:
                new[j] = 1
            elif pos[j] == 0 and s[j] > bands[0]:
                new[j] = -1
            elif pos[j] == 1 and s[j] > -bands[1]:
                new[j] = 0
            elif pos[j] == -1 and s[j] < bands[2]:
                new[j] = 0
        g = np.abs(new).sum()
        turn[t] = np.abs(new - pos).sum() / max(g, 1)
        pos = new
        if g > 0:
            # next day's residual return of each industry against today's factor loadings
            f1 = R[t + 1] @ E
            u1 = R[t + 1] - (B[0] + f1 @ B[1:])
            gross_pnl[t + 1] = float(np.sum(pos * u1) / g)
            pnl[t + 1] = gross_pnl[t + 1] - 2 * COST * turn[t]
        else:
            pnl[t + 1] = 0.0
            gross_pnl[t + 1] = 0.0
    if return_gross:
        return pnl, turn, gross_pnl
    return (pnl, turn, S_all) if return_scores else (pnl, turn)


PCA_CONFIGS = [(nf, w, b) for nf in (3, 5) for w in (30, 60) for b in ((1.25, 0.5, 0.75), (1.0, 0.25, 0.25))] + \
    [(5, 60, "theory")]
REGISTERED = (5, 60, "theory")     # the research chapter's band, at the House's costs; added after the eight AL-band rules, so charged all nine


def compute_pca() -> dict:
    d, R, cols = _ind()
    m = d >= 19900101
    d, R = d[m], R[m]
    ok = np.isfinite(R).all(0)
    R = R[:, ok]
    out = {}
    main = None
    gross_main = None
    al = None
    for nf, w, b in PCA_CONFIGS:
        pnl, turn, gross = _residual_book(d, R, nf, w, b, return_gross=True)
        k = np.isfinite(pnl)
        key = f"{nf}f/{w}d/{b if isinstance(b, str) else b[0]}"
        out[key] = _stats(pnl[k])
        out[key]["turnover"] = float(np.mean(turn[k]))
        out[key]["gross"] = _stats(gross[k])
        if (nf, w, b) == REGISTERED:
            main, gross_main = pnl, gross
        if (nf, w, b) == (5, 60, (1.25, 0.5, 0.75)):
            al = {"net": _stats(pnl[k]), "gross": _stats(gross[k]), "cum": np.cumsum(pnl[k])[::5],
                  "cum_gross": np.cumsum(gross[k])[::5]}
    k = np.isfinite(main)
    per = {}
    for a, b_ in ((1994, 2002), (2003, 2010), (2011, 2020)):
        kk = k & (d // 10000 >= a) & (d // 10000 <= b_)
        per[f"{a}-{b_}"] = _stats(main[kk])
    perg = {}
    for a, b_ in ((1994, 2002), (2003, 2010), (2011, 2020)):
        kk = k & (d // 10000 >= a) & (d // 10000 <= b_)
        perg[f"{a}-{b_}"] = _stats(gross_main[kk])
    return _json({"configs": out, "main": _stats(main[k]), "main_gross": _stats(gross_main[k]), "periods": per,
                  "periods_gross": perg, "al": al, "n_trials": len(PCA_CONFIGS), "cum": np.cumsum(main[k])[::5],
                  "cum_gross": np.cumsum(gross_main[k])[::5], "dates": d[k][::5], "curve": list(map(list, _curve()))})


# ---------------------------------------------------------------------------
# A hedge ratio that moves: BTC and ETH
# ---------------------------------------------------------------------------
def compute_kalman() -> dict:
    def series(sym):
        b = data.binance_daily(sym)
        t = np.asarray(b["time"])
        day = np.array([int(np.datetime64(int(x), "s").astype("datetime64[D]").astype(str).replace("-", "")) for x in t])
        return dict(zip(day.tolist(), np.log(np.asarray(b["close"], float)).tolist()))
    bt, et = series("BTCUSDT"), series("ETHUSDT")
    days = sorted(k for k in set(bt) & set(et) if 20180101 <= k <= RESEARCH_END)
    y = np.array([et[k] for k in days])
    x = np.array([bt[k] for k in days])
    a, b = SA.kalman_beta(y, x, q=1e-5, r=2e-3)
    roll = np.full(len(y), np.nan)
    for t in range(60, len(y)):
        roll[t] = np.polyfit(x[t - 60:t], y[t - 60:t], 1)[0]
    static = np.polyfit(x, y, 1)
    s_static = y - np.polyval(static, x)
    s_kal = y - (np.r_[np.nan, a[:-1]] + np.r_[np.nan, b[:-1]] * x)   # one-step-ahead: yesterday's estimate
    ok = np.isfinite(s_kal)
    adf_static = V.adf(s_static, 1)["t"]
    adf_kal = V.adf(s_kal[ok], 1)["t"]
    return _json({"days": days, "beta_kalman": b, "beta_roll": roll, "beta_static": float(static[0]),
                  "spread_static": s_static, "spread_kalman": s_kal, "adf_static": float(adf_static),
                  "adf_kalman": float(adf_kal), "hl_static": SA.ou_fit(s_static)["half_life"],
                  "hl_kalman": SA.ou_fit(s_kal[ok])["half_life"]})


# ---------------------------------------------------------------------------
# Lo-MacKinlay and Nagel
# ---------------------------------------------------------------------------
def _weekly(d, R):
    wk = (np.asarray(d) // 100) * 10 + 0
    out = []
    # ISO-ish weeks: group by consecutive Fridays: use 5-day blocks
    n = len(d) // 5
    for k in range(n):
        out.append(np.prod(1 + R[5 * k:5 * k + 5], 0) - 1)
    return np.array(out)


def compute_lomac() -> dict:
    s = data.ken_french_size_daily(through="2020-12-31")
    m = s["date"] >= 19630101
    Wz = _weekly(s["date"][m], s["deciles"][m])
    d, R, cols = _ind()
    m2 = d >= 19630101
    ok = np.isfinite(R[m2]).all(0)
    Wi = _weekly(d[m2], R[m2][:, ok])
    out = {"size": SA.lo_mackinlay(Wz), "industries": SA.lo_mackinlay(Wi)}
    # the lead-lag: correlation of large-cap returns last week with small-cap returns this week, and the reverse
    out["lead"] = {"large_to_small": float(np.corrcoef(Wz[:-1, 9], Wz[1:, 0])[0, 1]),
                   "small_to_large": float(np.corrcoef(Wz[:-1, 0], Wz[1:, 9])[0, 1]),
                   "small_own": float(np.corrcoef(Wz[:-1, 0], Wz[1:, 0])[0, 1]),
                   "large_own": float(np.corrcoef(Wz[:-1, 9], Wz[1:, 9])[0, 1])}
    # by era for the size deciles
    dd = s["date"][m][::5][:len(Wz)]
    era = {}
    for a, b in ((1963, 1990), (1991, 2020)):
        k = (dd // 10000 >= a) & (dd // 10000 <= b)
        era[f"{a}-{b}"] = SA.lo_mackinlay(Wz[k])
    out["size_era"] = era
    return _json(out)


def compute_nagel() -> dict:
    d, R, cols = _ind()
    m = d >= 19900101
    d, R = d[m], R[m]
    ok = np.isfinite(R).all(0)
    R = R[:, ok]
    N = R.shape[1]
    w = -(R[:-1] - R[:-1].mean(1, keepdims=True))
    w = w / np.abs(w).sum(1, keepdims=True)
    pi = np.r_[np.nan, np.sum(w * R[1:], 1)]
    md = d // 100
    months = np.unique(md)
    mr = np.array([np.nansum(pi[md == k]) for k in months])
    vix = data.cboe_index("VIX", through="2020-12-31")
    vm = {}
    for dt, v in zip(vix["date"], vix["close"]):
        vm[int(dt) // 100] = float(v)                  # the month's last close
    lag = np.array([vm.get(int(k - 1 if k % 100 != 1 else k - 89), np.nan) for k in months])
    ok2 = np.isfinite(lag)
    X = np.column_stack([np.ones(ok2.sum()), lag[ok2]])
    beta, *_ = np.linalg.lstsq(X, mr[ok2], rcond=None)
    res = mr[ok2] - X @ beta
    se = math.sqrt(res.var(ddof=2) / (np.var(lag[ok2]) * ok2.sum()))
    q = np.quantile(lag[ok2], [0.2, 0.8])
    return _json({"slope": float(beta[1]), "t": float(beta[1] / se), "low": float(mr[ok2][lag[ok2] <= q[0]].mean()),
                  "high": float(mr[ok2][lag[ok2] >= q[1]].mean()), "q": q, "months": months[ok2], "ret": mr[ok2],
                  "vix": lag[ok2], "sharpe": float(np.nanmean(mr) / np.nanstd(mr) * math.sqrt(12))})


# ---------------------------------------------------------------------------
# A small network on residual paths
# ---------------------------------------------------------------------------
def compute_deep() -> dict:
    from explainer.quant.house import ml
    d, R, cols = _ind()
    m = d >= 19900101
    d, R = d[m], R[m]
    ok = np.isfinite(R).all(0)
    R = R[:, ok]
    T, N = R.shape
    # residuals against 5 PCA factors re-estimated every 21 days on the trailing year (as in pca)
    U = np.full((T, N), np.nan)
    E = None
    for t in range(252, T):
        if E is None or t % 21 == 0:
            X = R[t - 252:t]
            sd = X.std(0)
            w, v = np.linalg.eigh(np.corrcoef(((X - X.mean(0)) / sd).T))
            E = v[:, ::-1][:, :5] / sd[:, None]
            F = X @ E
            A = np.column_stack([np.ones(252), F])
            B, *_ = np.linalg.lstsq(A, X, rcond=None)
        f = R[t] @ E
        U[t] = R[t] - (B[0] + f @ B[1:])
    L = 30
    Xs, ys, ds = [], [], []
    for t in range(252 + L, T - 1):
        path = np.cumsum(U[t - L + 1:t + 1], 0)            # L x N
        path = path - path[-1]                              # relative to today
        sd = U[t - L + 1:t + 1].std(0)
        Xs.append((path / sd).T)
        ys.append(U[t + 1] / sd)
        ds.append(np.full(N, d[t]))
    Xs, ys, ds = np.concatenate(Xs), np.concatenate(ys), np.concatenate(ds)
    tr, va, te = ds <= 20121231, (ds > 20121231) & (ds <= 20161231), ds > 20161231
    net = ml.MLPEnsemble(hidden=(32, 16), seeds=(0, 1, 2), epochs=30, lr=1e-3, l1=1e-5, batch=2048)
    net.fit(Xs[tr], np.clip(ys[tr], -5, 5), Xs[va], np.clip(ys[va], -5, 5))
    p = net.predict(Xs[te])
    # weights proportional to the prediction, demeaned each day, gross one; P&L in residual-sd units times sd ignored:
    # trade the industries' residual returns directly
    days = np.unique(ds[te])
    pn, ps = [], []
    sc_net, sc_turn, sc_gross = _residual_book(d, R, return_gross=True)
    prev = np.zeros(N)
    pnet, turns = [], []
    for k, dd in enumerate(days):
        sel = ds[te] == dd
        pr = p[sel] - p[sel].mean()
        t = int(np.searchsorted(d, dd))
        u1 = U[t + 1] if t + 1 < T else np.full(N, np.nan)
        if np.abs(pr).sum() > 0 and np.isfinite(u1).all():
            w = pr / np.abs(pr).sum()
            pn.append(float(np.sum(w * u1)))
            tv = float(np.abs(w - prev).sum())
            turns.append(tv)
            pnet.append(pn[-1] - 2 * COST * tv)
            prev = w
            ps.append(sc_gross[t + 1] if np.isfinite(sc_gross[t + 1]) else 0.0)
    pn, ps, pnet = np.array(pn), np.array(ps), np.array(pnet)
    ic = float(np.corrcoef(p, ys[te])[0, 1])
    lin = np.corrcoef(Xs[te][:, -2], ys[te])[0, 1]
    return _json({"net": _stats(pn), "net_after_costs": _stats(pnet), "turnover": float(np.mean(turns)),
                  "sscore": _stats(ps), "ic": ic, "n_train": int(tr.sum()),
                  "corr_with_reversal": float(np.corrcoef(p, -Xs[te][:, 0])[0, 1]), "lag1_corr": float(lin)})


# ---------------------------------------------------------------------------
# Research: the optimal band
# ---------------------------------------------------------------------------
def compute_theory() -> dict:
    k, s = 1.0, math.sqrt(2.0)        # kappa 1, s_eq 1: everything in units of s_eq and 1/kappa
    costs = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0]
    curve_ = []
    for c in costs:
        m, R = SA.optimal_band(k, s, c)
        curve_.append({"c": c, "m": m, "R": R})
    ms = np.linspace(0.05, 2.5, 60)
    rates = {str(c): [SA.band_rate(m, k, s, c) if m > c else np.nan for m in ms] for c in (0.1, 0.3, 0.5)}
    times = {"to_mean": [SA.ou_time_to_mean(m, k, s) for m in ms], "to_band": [SA.ou_time_to_band(m, k, s) for m in ms]}
    sims = []
    for c in (0.1, 0.3, 0.5):
        m_star = [x for x in curve_ if x["c"] == c][0]["m"]
        for m in (0.5 * m_star, m_star, 1.6 * m_star):
            seed = int(100 * c + 10 * m)
            r = SA.simulate_band(m, k, s, c, T=4000, dt=0.0005, seed=seed)
            r4 = SA.simulate_band(m, k, s, c, T=4000, dt=0.002, seed=seed)
            # discrete monitoring detects hits late, by O(sqrt dt): extrapolate the two step sizes to dt -> 0
            sims.append({"c": c, "m": m, "theory": SA.band_rate(m, k, s, c), "sim": r["rate"], "sim_coarse": r4["rate"],
                         "sim_extrap": 2 * r["rate"] - r4["rate"], "trades": r["trades"]})
    # first-passage check by brute force
    rng = np.random.default_rng(3302)
    dt = 0.001
    b = math.exp(-k * dt)
    sd = s * math.sqrt((1 - b * b) / (2 * k))
    fp = []
    for m in (0.5, 1.0, 1.5):
        ts = []
        for _ in range(300):
            x, t = -m, 0
            while x < 0:
                x = b * x + sd * rng.standard_normal()
                t += 1
            ts.append(t * dt)
        fp.append({"m": m, "theory": SA.ou_time_to_mean(m, k, s), "sim": float(np.mean(ts)),
                   "se": float(np.std(ts) / math.sqrt(len(ts)))})
    return _json({"curve": curve_, "ms": ms, "rates": rates, "times": times, "sims": sims, "fp": fp,
                  "frictionless": s * math.sqrt(k / math.pi)})


# ---------------------------------------------------------------------------
# The envelope
# ---------------------------------------------------------------------------
STRATEGY = "residual_sscore_part33"


def compute_envelope() -> dict:
    from explainer.quant.house import track
    p = load("pca")
    code = inspect.getsource(_residual_book) + inspect.getsource(SA.ou_fit)
    pit.register(STRATEGY, code, {"universe": "Ken French 49 industries, daily", "factors": "5 correlation-PCA "
                                  "eigenportfolios, trailing 252 days, refit every 21", "window": 60,
                                  "bands": "the research chapter's optimal band at each residual's cost and s_eq; exit at the mean",
                                  "cost": "5 bp per dollar"},
                 trials=int(p["n_trials"]))
    d, R, cols = _ind(True)
    pit.open_envelope(STRATEGY, "kenfrench/industries49_daily", d, np.where(np.isfinite(R), np.round(R, 8), -99.0))
    m = d >= 19900101
    d, R = d[m], R[m]
    ok = np.isfinite(R).all(0)
    R = R[:, ok]
    nf, w, b = REGISTERED
    pnl, turn, gross = _residual_book(d, R, nf, w, b, return_gross=True)
    res = np.isfinite(pnl) & (d <= RESEARCH_END)
    hold = np.isfinite(pnl) & (d > RESEARCH_END)
    md = d // 100

    def monthly(mask):
        ks = np.unique(md[mask])
        return ks, np.array([np.sum(pnl[mask & (md == k)]) for k in ks])
    rm_d, rm = monthly(res)
    hm_d, hm = monthly(hold)
    row = track.record(STRATEGY, 33, rm, hm, 0.0, note="Avellaneda-Lee residual s-scores on the 49 industries, research-chapter band, net of 5 bp")
    years = {str(y): _stats(pnl[hold & (d // 10000 == y)]) for y in range(2021, 2026)}
    return _json({"trials": pit.trials_so_far(), "n_trials": int(p["n_trials"]), "res": _stats(pnl[res]),
                  "hold": _stats(pnl[hold]), "res_gross": _stats(gross[res]), "hold_gross": _stats(gross[hold]), "row": row, "years": years, "cum_hold": np.cumsum(pnl[hold]),
                  "hold_dates": d[hold], "turn_hold": float(np.mean(turn[hold]))})


def compute_smallc() -> dict:
    """The small-cost law: m*/s_eq -> (3c/s_eq)^(1/3), checked against the exact optimum (kappa = 1, s_eq = 1)."""
    k, sig = 1.0, math.sqrt(2.0)
    rows = []
    for c in (0.0005, 0.002, 0.01, 0.05, 0.1, 0.3):
        m, r = SA.optimal_band(k, sig, c)
        rows.append({"c": c, "m": m, "law": (3 * c) ** (1 / 3), "ratio": m / (3 * c) ** (1 / 3), "rate": r})
    return _json({"rows": rows})


ITEMS = {"pairs": compute_pairs, "coint": compute_coint, "pca": compute_pca, "kalman": compute_kalman,
         "lomac": compute_lomac, "nagel": compute_nagel, "deep": compute_deep, "theory": compute_theory,
         "envelope": compute_envelope, "smallc": compute_smallc}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
