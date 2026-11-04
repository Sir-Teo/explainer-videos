"""Every number in Part 27 (Machine Learning for Returns), computed and cached in .cache/quant27/.

    python -m videos.quant.quant27.compute [items] [--force]

Two data sets.  The market: Amit Goyal's update of the Welch-Goyal predictors, monthly, 1926-2020 for research.
The cross-section: every coin Binance has ever quoted in USDT, listed or delisted, from its public archive (a panel
with no survivorship bias), weekly features from daily candles, 2018-2020 for research; 2021-2025 is sealed and read
once, in ``envelope``.

* ``snr``        what a small R^2 is worth: timing one asset against trading many;
* ``kmz``        Kelly, Malamud and Zhou's random-feature market timing over complexity and shrinkage;
* ``nagel``      Nagel's reading: the forecast against momentum, and a world built to reverse;
* ``panel``      the coin panel: who is in it, when, and the features;
* ``zoo``        Gu, Kelly and Xiu's model zoo on the panel, tested on 2019 and 2020 with expanding refits;
* ``descent``    double descent: ridgeless random-feature regressions as the features pass the observations;
* ``autoenc``    the conditional autoencoder against PCA, K = 1 to 5;
* ``attention``  attention across coins against a network that sees one coin at a time;
* ``images``     a CNN on 20-day chart images, against momentum;
* ``sdf``        an adversarially trained SDF against a linear one;
* ``toolkit``    dollar bars, triple-barrier labels and meta-labels, fractional differencing, uniqueness weights;
* ``conformal``  split and adaptive conformal intervals;
* ``pretrained`` a pocket foundation model: pretrained on coins, tested zero-shot on stock-market volatility;
* ``envelope``   the network ensemble and the random-feature timer, registered and opened on 2021-2025.
"""

from __future__ import annotations

import functools
import json
import math
import warnings

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import backtest as B, ml as ML, pit

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant27")
load = pit.counted(CACHE.load, 27)
RESEARCH_END = 202012


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


# ---------------------------------------------------------------------------
# The market: Welch-Goyal predictors, Kelly-Malamud-Zhou standardisation
# ---------------------------------------------------------------------------
PRED_NAMES = ["dp", "dy", "ep", "de", "svar", "bm", "ntis", "tbl", "lty", "ltr", "tms", "dfy", "dfr", "infl", "mkt"]


def _timing_data(through: str = "2020-12"):
    """Fifteen predictors (the Welch-Goyal set and the lagged market return) standardised by expanding means and
    volatilities (36 months minimum), and the market's excess return divided by its trailing 12-month volatility."""
    g = data.goyal_welch(through)
    m = g["date"] >= 192601
    L = lambda k: g[k][m]  # noqa: E731
    idx, D, E = L("Index"), L("D12"), L("E12")
    rx = L("CRSP_SPvw") - L("Rfree")
    X = np.column_stack([np.log(D) - np.log(idx), np.log(D) - np.log(np.r_[np.nan, idx[:-1]]), np.log(E) - np.log(idx),
                         np.log(D) - np.log(E), L("svar"), L("b/m"), L("ntis"), L("tbl"), L("lty"), L("ltr"),
                         L("lty") - L("tbl"), L("BAA") - L("AAA"), L("corpr") - L("ltr"),
                         np.r_[np.nan, L("infl")[:-1]], rx])
    d = g["date"][m]
    first = np.flatnonzero(np.isfinite(X).all(1))[0]
    X, rx, d = X[first:], rx[first:], d[first:]
    Xs = np.full_like(X, np.nan)
    for t in range(36, len(X)):
        Xs[t] = (X[t] - X[:t + 1].mean(0)) / (X[:t + 1].std(0) + 1e-12)
    vol = np.array([rx[t - 12:t].std() if t >= 12 else np.nan for t in range(len(rx))])
    rs = rx / vol
    s0 = np.flatnonzero(np.isfinite(Xs).all(1) & np.isfinite(rs))[0]
    return {"X": Xs[s0:], "r": rs[s0:], "rx": rx[s0:], "vol": vol[s0:], "date": d[s0:]}


def compute_snr() -> dict:
    r2 = np.linspace(0.001, 0.05, 50)
    single = np.sqrt(12 * r2 / (1 - r2))                     # timing one asset, monthly R^2
    breadth = {str(n): np.sqrt(12 * n * r2 / (1 - r2)) for n in (10, 100, 1000)}   # n independent bets a month
    td = _timing_data()
    r = td["r"]
    # the in-sample R^2 of each predictor alone, 1930-2020
    rows = []
    for j, nm in enumerate(PRED_NAMES):
        x, y = td["X"][:-1, j], r[1:]
        b = np.polyfit(x, y, 1)
        rows.append({"name": nm, "r2": float(1 - np.var(y - np.polyval(b, x)) / np.var(y))})
    return _json({"r2": r2, "single": single, "breadth": breadth, "predictors": rows,
                  "sr_at_1pct": float(math.sqrt(12 * 0.01 / 0.99))})


KMZ_P = (2, 6, 12, 30, 60, 120, 300, 600, 1200, 3000, 6000, 12000)
KMZ_Z = (1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0, 1e3)


def compute_kmz() -> dict:
    td = _timing_data()
    X, r, d = td["X"], td["r"], td["date"]
    res = ML.kmz_timing(X, r, T=12, Ps=KMZ_P, zs=KMZ_Z, gamma=2.0, n_seeds=10)
    F, t0 = res["F"], res["t0"]
    rr = r[t0:]
    grid = {"sharpe": [], "r2": [], "beta": []}
    for P in KMZ_P:
        s_, q_, b_ = [], [], []
        for z in KMZ_Z:
            f = F[P][z][t0:]
            s_.append(B.sharpe(f * rr, 12))
            q_.append(1 - np.sum((rr - f) ** 2) / np.sum(rr ** 2))
            b_.append(float(np.polyfit(f, rr, 1)[0]))
        grid["sharpe"].append(s_)
        grid["r2"].append(q_)
        grid["beta"].append(b_)
    best = F[12000][1e-1][t0:]
    ym = d[t0:]
    return _json({"P": KMZ_P, "z": KMZ_Z, "c": [p / 12 for p in KMZ_P], "grid": grid, "first": int(ym[0]),
                  "last": int(ym[-1]), "n": len(rr), "sr_market": B.sharpe(rr, 12),
                  "position": best, "ym": ym, "cum": np.cumsum(best * rr), "cum_mkt": np.cumsum(rr)})


def compute_nagel() -> dict:
    td = _timing_data()
    X, r = td["X"], td["r"]
    k = load("kmz")
    t0 = int(np.searchsorted(td["date"], k["first"]))
    f = np.asarray(k["position"])
    rr = r[t0:]
    mom12 = np.array([r[t - 12:t].mean() for t in range(t0, len(r))])
    lag1 = r[t0 - 1:-1]
    # the kernel the forecast is built from: similarities of x_{t-1} to the 12 training months
    Z = ML.rff(X, 12000, 2.0, seed=0)
    sims = []
    for t in range(t0, len(r), 12):
        tr = np.arange(t - 12, t)
        sims.append(Z[t - 1] @ Z[tr - 1].T)
    sims = np.array(sims)
    exact = np.array([ML.kernel_weights(X, t) for t in range(t0, len(r), 12)])
    # Nagel's test: the same predictors, returns from a world that reverses
    rng = np.random.default_rng(27)
    a = np.zeros(len(r))
    e = rng.standard_normal(len(r))
    for i in range(1, len(r)):
        a[i] = -0.3 * a[i - 1] + e[i]
    rev = ML.kmz_timing(X, a, T=12, Ps=(12000,), zs=(1e-1,), gamma=2.0, n_seeds=10)["F"][12000][1e-1][t0:]
    return _json({"sr_rff": B.sharpe(f * rr, 12), "sr_mom12": B.sharpe(mom12 * rr, 12), "sr_lag1": B.sharpe(lag1 * rr, 12),
                  "corr_mom12": float(np.corrcoef(f, mom12)[0, 1]), "corr_lag1": float(np.corrcoef(f, lag1)[0, 1]),
                  "sims_mean": np.abs(sims).mean(0), "exact_max": float(exact.max()),
                  "exact_median": float(np.median(exact)),
                  "rev": {"sr_rff": B.sharpe(rev * a[t0:], 12), "sr_reversal": B.sharpe(-a[t0 - 1:-1] * a[t0:], 12),
                          "corr_lag1": float(np.corrcoef(rev, a[t0 - 1:-1])[0, 1]), "phi": -0.3}})


# ---------------------------------------------------------------------------
# The cross-section: every USDT coin in Binance's archive, weekly
# ---------------------------------------------------------------------------
FEATURES = ["r1d", "r1w", "r4w", "r12w", "r26w", "vol28", "max28", "skew28", "range7", "lqv", "dqv", "amihud",
            "beta", "ivol", "age"]
MIN_QV = 2.5e5          # median daily USDT volume over the past four weeks, to enter that week's universe
HOLD = 20210101
QN = 5                  # quintile sorts: in 2018-2020 a week has only 10 to 60 liquid coins


@functools.lru_cache(maxsize=1)
def _grid():
    syms = data.binance_usdt_universe()
    ser = {}
    for s_ in syms:
        d = data.binance_daily(s_)
        if len(d["time"]) >= 30:
            ser[s_] = d
    names = sorted(ser)
    d0 = min(int(round(ser[s_]["time"][0] / 86400)) for s_ in names)
    d1 = max(int(round(ser[s_]["time"][-1] / 86400)) for s_ in names)
    n = d1 - d0 + 1
    G = {k: np.full((n, len(names)), np.nan) for k in ("close", "quote", "high", "low")}
    for j, s_ in enumerate(names):
        idx = np.round(ser[s_]["time"] / 86400).astype(int) - d0
        for k in G:
            G[k][idx, j] = ser[s_][k]
    G["close"][G["close"] <= 0] = np.nan
    return d0, names, G


def _ymd(day):
    from datetime import datetime, timezone
    return int(datetime.fromtimestamp(int(day) * 86400, timezone.utc).strftime("%Y%m%d"))


def _rank(x):
    """Each week's cross-sectional rank, scaled to [-1, 1]; a missing value is set to the median, 0 (Gu, Kelly and
    Xiu's treatment)."""
    out = np.zeros_like(x)
    for j in range(x.shape[1]):
        v = x[:, j]
        m = np.isfinite(v)
        if m.sum() > 1:
            r = stats.rankdata(v[m])
            out[m, j] = 2 * (r - 1) / (m.sum() - 1) - 1
    return out


@functools.lru_cache(maxsize=1)
def _panel():
    d0, names, G = _grid()
    C, Q, H, L = G["close"], G["quote"], G["high"], G["low"]
    lc = np.log(C)
    dr = np.vstack([np.full((1, C.shape[1]), np.nan), np.diff(lc, axis=0)])
    first = np.array([np.flatnonzero(np.isfinite(C[:, j]))[0] for j in range(C.shape[1])])
    btc = names.index("BTCUSDT")
    n = C.shape[0]
    sundays = [t for t in range(200, n - 1) if (d0 + t) % 7 == 3]      # 1970-01-04 was a Sunday: day % 7 == 3
    rows = {k: [] for k in ("date", "coin", "X", "y", "ret", "qv", "delisted")}
    for t in sundays:
        ok = np.isfinite(C[t]) & (first <= t - 60)
        med_qv = np.nanmedian(Q[t - 27:t + 1], axis=0)
        ok &= med_qv >= MIN_QV
        js = np.flatnonzero(ok)
        if len(js) < 10:
            continue
        w = lambda a, b: lc[t - a, js] - lc[t - b, js]  # noqa: E731
        win = dr[t - 27:t + 1][:, js]
        f = {"r1d": dr[t, js], "r1w": w(0, 7), "r4w": w(7, 28), "r12w": w(28, 84), "r26w": w(84, 182),
             "vol28": np.nanstd(win, axis=0), "max28": np.nanmax(win, axis=0), "skew28": stats.skew(win, axis=0,
                                                                                                   nan_policy="omit"),
             "range7": np.nanmean(np.log(H[t - 6:t + 1, js] / L[t - 6:t + 1, js]), axis=0),
             "lqv": np.log(np.nanmean(Q[t - 27:t + 1, js], axis=0)),
             "dqv": np.log(np.nanmean(Q[t - 6:t + 1, js], axis=0) / np.nanmean(Q[t - 27:t + 1, js], axis=0)),
             "amihud": np.log(np.nanmean(np.abs(win) / np.maximum(Q[t - 27:t + 1, js], 1.0), axis=0) + 1e-14),
             "age": np.log(t - first[js] + 1.0)}
        xb = dr[t - 83:t + 1, btc]
        Y = dr[t - 83:t + 1][:, js]
        mb = np.isfinite(xb)
        beta = np.full(len(js), np.nan)
        ivol = np.full(len(js), np.nan)
        for k in range(len(js)):
            m = mb & np.isfinite(Y[:, k])
            if m.sum() >= 30:
                b = np.polyfit(xb[m], Y[m, k], 1)
                beta[k] = b[0]
                ivol[k] = np.std(Y[m, k] - np.polyval(b, xb[m]))
        f["beta"], f["ivol"] = beta, ivol
        X = np.column_stack([f[k] for k in FEATURES])
        # next week's return: to the close seven days on, or to the last close before a coin stopped trading
        fut = C[t + 1:t + 8, js]
        last = np.array([fut[np.flatnonzero(np.isfinite(fut[:, k]))[-1], k] if np.isfinite(fut[:, k]).any()
                         else C[t, js[k]] for k in range(len(js))])
        y = np.log(last / C[t, js])
        rows["date"].append(np.full(len(js), _ymd(d0 + t)))
        rows["coin"].append(js)
        rows["X"].append(_rank(X))
        rows["y"].append(y)
        rows["ret"].append(np.exp(y) - 1)
        rows["qv"].append(med_qv[js])
        rows["delisted"].append(~np.isfinite(C[min(t + 7, n - 1), js]))
    P = {k: np.concatenate(v) for k, v in rows.items()}
    P["names"] = names
    return P


def _split(P, test_year):
    """Expanding window: train on every week before the last 26 of the years before ``test_year``, validate on those
    26, test on ``test_year``; each label ends inside its own period."""
    d = P["date"]
    test = (d >= test_year * 10000) & (d < (test_year + 1) * 10000 - 7)   # labels end within the year
    pre = np.unique(d[d < test_year * 10000 - 7])
    cut = pre[-26] if len(pre) > 40 else pre[len(pre) * 3 // 4]
    tr = d < cut
    va = (d >= cut) & (d < test_year * 10000 - 7)
    return tr, va, test


def _winsor(y, q=0.01):
    lo, hi = np.quantile(y, [q, 1 - q])
    return np.clip(y, lo, hi)


def compute_panel() -> dict:
    P = _panel()
    d = P["date"]
    weeks = np.unique(d)
    count = np.array([np.sum(d == w) for w in weeks])
    res = d < 20201231
    d0, names, G = _grid()
    ever = np.unique(P["coin"][res])
    gone = [names[j] for j in ever if not np.isfinite(G["close"][-1, j])]
    # seal the hold-out: weekly next-week returns of every coin in the universe, 2021 on
    M = np.full((len(weeks), len(names)), -999.0)
    for k, w in enumerate(weeks):
        m = d == w
        M[k, P["coin"][m]] = np.round(P["ret"][m], 10)
    seal = pit.seal("binance/usdt_weekly_panel", weeks, M)
    return _json({"weeks": weeks, "count": count, "n_coins": len(names), "n_research": int(len(ever)),
                  "n_research_gone": len(gone), "gone_examples": gone[:12], "features": FEATURES,
                  "obs_research": int(res.sum()), "first_week": int(weeks[0]), "seal": seal,
                  "delisted_weeks": int(P["delisted"][res].sum())})


ZOO = ["OLS", "OLS-3", "ENet", "PCR", "PLS", "GBRT", "NN1", "NN2", "NN3"]


def _fit_zoo(name, X, y, Xv, yv, seed=0):
    if name == "OLS":
        return ML.ols(X, y)
    if name == "OLS-3":
        cols = [FEATURES.index(k) for k in ("r4w", "lqv", "vol28")]
        f = ML.ols(X[:, cols], y)
        return lambda Z: f(Z[:, cols])
    if name in ("ENet", "PCR", "PLS"):
        grid = {"ENet": [1e-4, 3e-4, 1e-3, 3e-3, 1e-2], "PCR": [1, 2, 3, 5, 8, 12], "PLS": [1, 2, 3, 5, 8]}[name]
        fn = {"ENet": lambda a: ML.enet(X, y, a), "PCR": lambda k: ML.pcr(X, y, k), "PLS": lambda k: ML.pls(X, y, k)}
        fits = [fn[name](a) for a in grid]
        k = int(np.argmin([np.mean((yv - f(Xv)) ** 2) for f in fits]))
        return fits[k]
    if name == "GBRT":
        g = ML.GBMRegressor(n_trees=400, depth=2, lr=0.03, min_leaf=50, subsample=0.7, seed=seed).fit(
            X, y, Xv, yv, early_stop=40)
        return g.predict
    hidden = {"NN1": (32,), "NN2": (32, 16), "NN3": (32, 16, 8)}[name]
    m = ML.MLPEnsemble(hidden=hidden, seeds=tuple(range(seed, seed + 5)), epochs=60, lr=1e-3, l1=1e-5).fit(X, y, Xv, yv)
    return m.predict


def compute_zoo() -> dict:
    P = _panel()
    out = {m: {"y": [], "f": [], "d": [], "qv": [], "ret": []} for m in ZOO}
    imp = {}
    for year in (2019, 2020):
        tr, va, te = _split(P, year)
        X, y = P["X"][tr], _winsor(P["y"][tr])
        Xv, yv = P["X"][va], _winsor(P["y"][va])
        for m in ZOO:
            f = _fit_zoo(m, X, y, Xv, yv)
            out[m]["f"].append(f(P["X"][te]))
            out[m]["y"].append(P["y"][te])
            out[m]["d"].append(P["date"][te])
            out[m]["qv"].append(P["qv"][te])
            out[m]["ret"].append(P["ret"][te])
            if year == 2020 and m in ("NN3", "GBRT", "OLS"):
                base = ML.r2_oos(y, f(X))
                imp[m] = {}
                for j, k in enumerate(FEATURES):
                    Z = X.copy()
                    Z[:, j] = 0.0
                    imp[m][k] = base - ML.r2_oos(y, f(Z))
    rows = {}
    for m in ZOO:
        f, y = np.concatenate(out[m]["f"]), np.concatenate(out[m]["y"])
        d, qv, ret = np.concatenate(out[m]["d"]), np.concatenate(out[m]["qv"]), np.concatenate(out[m]["ret"])
        ew = ML.decile_spread(d, f, ret, q=QN)
        vw = ML.decile_spread(d, f, ret, q=QN, weights=qv)
        rows[m] = {"r2": ML.r2_oos(y, f), "sr_ew": B.sharpe(ew["ls"], 52), "sr_vw": B.sharpe(vw["ls"], 52),
                   "mean_ew": float(ew["ls"].mean() * 52), "mean_vw": float(vw["ls"].mean() * 52),
                   "cum_ew": np.cumsum(np.log1p(np.clip(ew["ls"], -0.99, None))), "weeks": ew["date"],
                   "liq_split": _liq_split(d, f, ret, qv)}
    return _json({"rows": rows, "models": ZOO, "importance": imp, "features": FEATURES})


def _liq_split(d, f, ret, qv):
    """Avramov, Cheng and Metzker's question: where does the edge live? The tercile spread among the more and the
    less liquid half of each week's coins."""
    out = {}
    for half in ("liquid", "illiquid"):
        dd, ff, rr = [], [], []
        for w in np.unique(d):
            m = d == w
            med = np.median(qv[m])
            k = m & ((qv >= med) if half == "liquid" else (qv < med))
            dd.append(d[k])
            ff.append(f[k])
            rr.append(ret[k])
        s = ML.decile_spread(np.concatenate(dd), np.concatenate(ff), np.concatenate(rr), q=3)
        out[half] = B.sharpe(s["ls"], 52)
    return out


def compute_descent() -> dict:
    """Double descent in the cross-section: ridgeless regressions of next-week returns on P random features of the
    15 characteristics, fitted on N = 1,000 coin-weeks of 2018-19 and tested on 2020, as P passes N."""
    P = _panel()
    d = P["date"]
    tr, te = np.flatnonzero(d < 20200101), np.flatnonzero((d >= 20200101) & (d < 20201224))
    rng = np.random.default_rng(27)
    N = 1000
    Ps = [10, 30, 100, 300, 600, 900, 1000, 1100, 1500, 3000, 10000, 30000]
    res = {str(z): [] for z in (1e-8, 1e-2)}
    for z in (1e-8, 1e-2):
        for p_ in Ps:
            r2s = []
            for s in range(5):
                idx = rng.choice(tr, N, replace=False)
                Z = ML.rff(P["X"][np.r_[idx, te]], p_, gamma=0.5, seed=100 + s)
                y = _winsor(P["y"][idx])
                b = ML.ridge_dual(Z[:N], y - y.mean(), z)
                f = Z[N:] @ b + y.mean()
                r2s.append(ML.r2_oos(P["y"][te], f))
            res[str(z)].append(float(np.median(r2s)))
    return _json({"P": Ps, "N": N, "r2": res, "c": [p_ / N for p_ in Ps]})


def _weekly_panels(P, mask):
    out = []
    for w in np.unique(P["date"][mask]):
        m = mask & (P["date"] == w)
        out.append((P["X"][m].astype(np.float32), _winsor(P["y"][m], 0.02).astype(np.float32), w, np.flatnonzero(m)))
    return out


def compute_autoenc() -> dict:
    P = _panel()
    d = P["date"]
    trm, vam, tem = d < 20190701, (d >= 20190701) & (d < 20191224), (d >= 20200101) & (d < 20201224)
    tr, va, te = _weekly_panels(P, trm), _weekly_panels(P, vam), _weekly_panels(P, tem)
    rows = []
    for hidden, nm in (((), "linear betas"), ((32,), "CA1"), ((32, 16), "CA2")):
        for K in (1, 2, 3, 4, 5):
            m = ML.CondAutoencoder(K=K, hidden=hidden, epochs=80, lr=3e-3, seed=0).fit(
                [(Z, r) for Z, r, _, _ in tr], [(Z, r) for Z, r, _, _ in va])
            lam = np.mean([m.factors(Z, r) for Z, r, _, _ in tr + va], axis=0)
            num_t = num_p = den = 0.0
            for Z, r, _, idx in te:
                rr = P["y"][idx]
                num_t += np.sum((rr - m.fitted(Z, rr.astype(np.float32))) ** 2)
                num_p += np.sum((rr - m.predict(Z, lam)) ** 2)
                den += np.sum(rr ** 2)
            rows.append({"model": nm, "K": K, "total": 1 - num_t / den, "pred": 1 - num_p / den})
    return _json({"rows": rows})


def compute_attention() -> dict:
    P = _panel()
    d = P["date"]
    trm, vam, tem = d < 20190701, (d >= 20190701) & (d < 20191224), (d >= 20200101) & (d < 20201224)
    tr, va, te = _weekly_panels(P, trm), _weekly_panels(P, vam), _weekly_panels(P, tem)
    out = {}
    att = CA_ex = None
    for nm in ("attention", "pointwise"):
        preds = []
        for seed in range(3):
            if nm == "attention":
                m = ML.CrossAttention(d_model=32, heads=4, layers=1, epochs=40, lr=1e-3, seed=seed).fit(
                    [(Z, r) for Z, r, _, _ in tr], [(Z, r) for Z, r, _, _ in va])
                preds.append(np.concatenate([m.predict(Z) for Z, _, _, _ in te]))
                if seed == 0:
                    Z, _, w, idx = te[len(te) // 2]
                    att, CA_ex = m.attention(Z), {"week": int(w), "coins": [P["names"][P["coin"][i]] for i in idx]}
            else:
                Xtr = np.concatenate([Z for Z, _, _, _ in tr])
                ytr = np.concatenate([r for _, r, _, _ in tr])
                Xva = np.concatenate([Z for Z, _, _, _ in va])
                yva = np.concatenate([r for _, r, _, _ in va])
                m = ML.MLPEnsemble(hidden=(32, 16), seeds=(seed,), epochs=60).fit(Xtr, ytr, Xva, yva)
                preds.append(np.concatenate([m.predict(Z) for Z, _, _, _ in te]))
        f = np.mean(preds, axis=0)
        idx = np.concatenate([i for _, _, _, i in te])
        ew = ML.decile_spread(P["date"][idx], f, P["ret"][idx], q=QN)
        out[nm] = {"r2": ML.r2_oos(P["y"][idx], f), "sr_ew": B.sharpe(ew["ls"], 52)}
    # how concentrated is attention? the share of each row's weight on its own top 5
    top = np.sort(att, axis=1)[:, ::-1][:, :5].sum(1)
    return _json({"rows": out, "attention": att, "example": CA_ex, "top5_share": float(top.mean()),
                  "n_assets": att.shape[0]})


def compute_images() -> dict:
    d0, names, G = _grid()
    C, Q, H, L = G["close"], G["quote"], G["high"], G["low"]
    O = np.vstack([C[:1], C[:-1]])          # daily open = previous close (the archive's open is the same to rounding)
    P = _panel()
    imgs, ys, dates, mom, js_ = [], [], [], [], []
    for w in np.unique(P["date"][P["date"] < 20201224]):
        from datetime import datetime, timezone
        t = int(datetime.strptime(str(w), "%Y%m%d").replace(tzinfo=timezone.utc).timestamp() // 86400) - d0
        m = P["date"] == w
        for j in P["coin"][m]:
            seg = C[t - 19:t + 1, j]
            if not np.isfinite(seg).all() or not np.isfinite(C[min(t + 5, len(C) - 1), j]):
                continue
            imgs.append(ML.chart_images(O[:, j], H[:, j], L[:, j], C[:, j], np.nan_to_num(Q[:, j]), t, 20, 32))
            ys.append(float(C[t + 5, j] > C[t, j]))
            dates.append(w)
            mom.append(C[t, j] / C[t - 19, j] - 1)
            js_.append(j)
    imgs, ys, dates, mom = np.array(imgs), np.array(ys), np.array(dates), np.array(mom)
    tr, va, te = dates < 20190701, (dates >= 20190701) & (dates < 20191224), dates >= 20200101
    probs = []
    for seed in range(3):
        cnn = ML.ChartCNN(epochs=12, seed=seed).fit(imgs[tr], ys[tr], imgs[va], ys[va])
        probs.append(cnn.predict_proba(imgs[te]))
    p = np.mean(probs, axis=0)
    acc = float(np.mean((p > 0.5) == ys[te]))
    acc_mom = float(np.mean((mom[te] > 0) == ys[te]))
    base = float(max(ys[te].mean(), 1 - ys[te].mean()))
    # a weekly long-short by the CNN's probability, five-day returns
    r5 = np.array([C[int(datetime.strptime(str(w), "%Y%m%d").replace(tzinfo=timezone.utc).timestamp() // 86400) - d0 + 5, j]
                   / C[int(datetime.strptime(str(w), "%Y%m%d").replace(tzinfo=timezone.utc).timestamp() // 86400) - d0, j] - 1
                   for w, j in zip(dates[te], np.array(js_)[te])])
    ls = ML.decile_spread(dates[te], p, r5, q=5)
    lm = ML.decile_spread(dates[te], mom[te], r5, q=5)
    corr = float(stats.spearmanr(p, mom[te])[0])
    ex = {"up": imgs[te][int(np.argmax(p))], "down": imgs[te][int(np.argmin(p))]}
    return _json({"n_train": int(tr.sum()), "n_test": int(te.sum()), "acc": acc, "acc_mom": acc_mom, "base": base,
                  "sr_cnn": B.sharpe(ls["ls"], 52), "sr_mom": B.sharpe(lm["ls"], 52), "corr_mom": corr,
                  "example_up": ex["up"], "example_down": ex["down"]})


def compute_sdf() -> dict:
    P = _panel()
    d = P["date"]
    trm, tem = d < 20200101, (d >= 20200101) & (d < 20201224)
    tr, te = _weekly_panels(P, trm), _weekly_panels(P, tem)
    out = {}
    rets = []
    for seed in range(3):
        m = ML.AdversarialSDF(hidden=(32, 16), n_moments=4, epochs=40, lr=1e-3, seed=seed, rounds=3).fit(
            [(Z, r) for Z, r, _, _ in tr])
        rets.append([float(np.sum(m.weights(Z) * P["ret"][idx])) for Z, _, _, idx in te])
    sdf_r = np.mean(rets, axis=0)
    # the linear SDF: weights linear in characteristics, b from the managed portfolios' mean-variance solution
    Xm = np.array([Z.T @ r / len(r) for Z, r, _, _ in tr])
    b = np.linalg.solve(np.cov(Xm.T) + 1e-4 * np.eye(Xm.shape[1]), Xm.mean(0))
    lin = []
    for Z, _, _, idx in te:
        w = Z @ b
        w = w / (np.abs(w).sum() + 1e-12)
        lin.append(float(np.sum(w * P["ret"][idx])))
    ew = [float(P["ret"][idx].mean()) for _, _, _, idx in te]
    return _json({"sr_adv": B.sharpe(sdf_r, 52), "sr_lin": B.sharpe(lin, 52), "sr_ew": B.sharpe(ew, 52),
                  "cum_adv": np.cumsum(sdf_r), "cum_lin": np.cumsum(lin), "weeks": [w for _, _, w, _ in te],
                  "corr": float(np.corrcoef(sdf_r, lin)[0, 1])})


def compute_toolkit() -> dict:
    out = {}
    b = data.binance_klines("BTCUSDT", "1h", "2018-01", "2020-12")
    t, c, v = b["time"], b["close"], b["volume"] * b["close"]
    day = (t // 86400).astype(int)
    last = np.r_[np.diff(day) != 0, True]
    tb = np.diff(np.log(c[last]))
    thr = v.sum() / last.sum()                     # one dollar bar a day on average
    db = ML.dollar_bars(t, c, v, thr)
    dbr = np.diff(np.log(db["close"]))
    for k, r in (("time", tb), ("dollar", dbr)):
        z = (r - r.mean()) / r.std()
        out[k] = {"n": int(len(r)), "kurt": float(stats.kurtosis(r)), "jb": float(stats.jarque_bera(r)[0]),
                  "ac_sq": float(np.corrcoef(r[:-1] ** 2, r[1:] ** 2)[0, 1]), "hist": np.histogram(z, 60, (-6, 6))[0]}
    per_day = np.bincount((db["t"] // 86400).astype(int) - day[0])
    out["bars_per_day"] = {"min": int(per_day.min()), "max": int(per_day.max()), "series": per_day}
    # fractional differencing of the log price, 2018-2020
    lp = np.log(c[last])
    ds = np.round(np.arange(0, 1.01, 0.1), 2)
    adf, cor = [], []
    for dd in ds:
        x = ML.fracdiff(lp, dd, 1e-3) if dd > 0 else lp
        m = np.isfinite(x)
        adf.append(ML.adf_t(x[m]))
        cor.append(float(np.corrcoef(x[m], lp[m])[0, 1]))
    out["fracdiff"] = {"d": ds, "adf": adf, "corr": cor, "crit": -2.86}
    # triple-barrier labels and meta-labelling on BTC daily: the primary bet is 20-day momentum's sign
    cd = c[last]
    r1 = np.diff(np.log(cd), prepend=np.nan)
    vol = np.array([np.nanstd(r1[max(1, i - 20):i + 1]) for i in range(len(cd))])
    tbl = ML.triple_barrier(cd, vol * np.sqrt(10), horizon=10, up=1.0, down=1.0)
    side = np.sign(np.r_[np.full(20, np.nan), cd[20:] / cd[:-20] - 1])
    ok = np.isfinite(side) & (np.arange(len(cd)) < len(cd) - 10)
    hit = (tbl["label"] == side).astype(float)
    feats = np.column_stack([vol, r1, np.r_[np.nan, cd[1:] / cd[:-1]], side])
    feats = np.nan_to_num(feats)
    n = len(cd)
    trn, tst = ok & (np.arange(n) < n * 2 // 3), ok & (np.arange(n) >= n * 2 // 3)
    clf = __import__("explainer.quant.house.credit", fromlist=["GBM"]).GBM(n_trees=150, depth=2, lr=0.05, min_leaf=20,
                                                                         seed=0).fit(feats[trn], hit[trn])
    pr = clf.predict_proba(feats[tst])
    take = pr > 0.5
    fwd = np.array([np.log(cd[tbl["end"][i]] / cd[i]) for i in range(n)])
    prim = side[tst] * fwd[tst]
    meta = np.where(take, side[tst] * fwd[tst], 0.0)
    out["meta"] = {"precision_primary": float(hit[tst].mean()), "precision_meta": float(hit[tst][take].mean()),
                   "taken": float(take.mean()), "mean_primary": float(prim.mean()), "mean_meta": float(meta.mean()),
                   "sd_primary": float(prim.std()), "sd_meta": float(meta.std())}
    u = ML.uniqueness_weights(np.arange(n - 10), tbl["end"][:n - 10], n)
    out["uniqueness"] = {"mean": float(u.mean()), "n": int(len(u)), "effective": float(u.sum())}
    return _json(out)


def compute_conformal() -> dict:
    P = _panel()
    d = P["date"]
    tr, va, te = _split(P, 2020)
    cal = va
    f = _fit_zoo("NN2", P["X"][tr], _winsor(P["y"][tr]), P["X"][va], _winsor(P["y"][va]))
    out = {}
    for a in (0.1, 0.2):
        q = ML.split_conformal(P["y"][cal] - f(P["X"][cal]), a)
        cover = np.abs(P["y"][te] - f(P["X"][te])) <= q
        weekly = [float(cover[d[te] == w].mean()) for w in np.unique(d[te])]
        out[str(a)] = {"q": q, "cover": float(cover.mean()), "weekly": weekly}
    out["weeks"] = np.unique(d[te])
    # adaptive conformal on BTC's daily return, 2018-2020, forecast = 0
    b = data.binance_klines("BTCUSDT", "1d", "2018-01", "2020-12")
    r = np.diff(np.log(b["close"]))
    aci = ML.adaptive_conformal(r, alpha=0.1, gamma=0.01, window=120)
    stat = ML.split_conformal(r[:120], 0.1)
    st_cov = (np.abs(r[120:]) <= stat).astype(float)
    roll = lambda x: np.convolve(x, np.ones(60) / 60, mode="valid")  # noqa: E731
    out["btc"] = {"q_aci": aci["q"][120:], "cover_aci": float(np.nanmean(aci["cover"][120:])), "q_static": stat,
                  "cover_static": float(st_cov.mean()), "roll_aci": roll(aci["cover"][120:]), "roll_static": roll(st_cov),
                  "r": r[120:], "t": b["time"][1:][120:]}
    return _json(out)


def compute_pretrained() -> dict:
    """A pocket foundation model: one small network trained on the volatility histories of every coin, 2018-2020,
    then used zero-shot on stock-market ETFs it never saw, against EWMA and a HAR model fitted to each ETF."""
    torch = ML._torch()
    d0, names, G = _grid()
    C = G["close"]
    lr = np.diff(np.log(C), axis=0)
    end = 20201231
    from datetime import datetime, timezone
    tend = int(datetime(2020, 12, 31, tzinfo=timezone.utc).timestamp() // 86400) - d0
    L = 60

    def windows(r):
        a = np.log(np.abs(r) + 1e-4)
        X, Y = [], []
        for i in range(L, len(a) - 1):
            w = a[i - L:i]
            if np.isfinite(w).all() and np.isfinite(a[i]):
                mu = w.mean()
                X.append(w - mu)
                Y.append(a[i] - mu)
        return np.array(X, np.float32), np.array(Y, np.float32)
    Xs, Ys = [], []
    for j in range(C.shape[1]):
        X, Y = windows(lr[:tend, j])
        if len(X):
            Xs.append(X[::3])
            Ys.append(Y[::3])
    X, Y = np.concatenate(Xs), np.concatenate(Ys)
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(X))
    X, Y = X[perm][:200_000], Y[perm][:200_000]
    nv = len(X) // 10
    net = ML.MLPEnsemble(hidden=(64, 32), seeds=(0, 1, 2), epochs=30, lr=1e-3, l1=0.0, batch=1024).fit(
        X[nv:], Y[nv:], X[:nv], Y[:nv])
    out = {"n_windows": int(len(X)), "n_coins": len(Xs), "etfs": {}}
    for sym in ("SPY", "QQQ", "EEM", "GLD", "XLE"):
        b = data.yahoo_bars(sym)
        r = np.diff(np.log(b["adjclose"]))
        Xe, Ye = windows(r)
        f_net = net.predict(Xe)
        a = np.log(np.abs(r) + 1e-4)
        # EWMA of |r| in logs, and HAR (1, 5, 22-day averages) fitted on the ETF's own first half
        ew = np.array([np.log(np.sqrt(np.mean(r[max(0, i - 60):i] ** 2 * 0.94 ** np.arange(min(i, 60))[::-1]) /
                                        np.mean(0.94 ** np.arange(min(i, 60)))) + 1e-4) for i in range(L, len(a) - 1)])
        mu = np.array([a[i - L:i].mean() for i in range(L, len(a) - 1)])
        ewc = ew - mu
        h1 = np.array([a[i - 1] for i in range(L, len(a) - 1)]) - mu
        h5 = np.array([a[i - 5:i].mean() for i in range(L, len(a) - 1)]) - mu
        h22 = np.array([a[i - 22:i].mean() for i in range(L, len(a) - 1)]) - mu
        H = np.column_stack([np.ones(len(h1)), h1, h5, h22])
        half = len(H) // 2
        bh = np.linalg.lstsq(H[:half], Ye[:half], rcond=None)[0]
        f_har = H @ bh
        # E log|r| lies below log(sigma) (by 0.64 for a normal): EWMA gets the same fitted offset HAR's intercept gives it
        f_ew = ewc + np.mean(Ye[:half] - ewc[:half])
        sl = slice(half, None)
        mse = lambda f: float(np.mean((Ye[sl] - f[sl]) ** 2))  # noqa: E731
        out["etfs"][sym] = {"net": mse(f_net), "ewma": mse(f_ew), "har": mse(f_har), "zero": mse(np.zeros(len(Ye))),
                            "n_test": int(len(Ye) - half), "first_test": int(b["date"][L + 1 + half])}
    return _json(out)


def _monthly_compound(dates, r):
    """Weekly returns (dates YYYYMMDD) compounded into calendar months."""
    ym = np.asarray(dates) // 100
    out_ym, out = [], []
    for m in np.unique(ym):
        out_ym.append(int(m))
        out.append(float(np.prod(1 + np.asarray(r)[ym == m]) - 1))
    return np.array(out_ym), np.array(out)


def _turnover_cost(d, f, qv, bps=10.0):
    """Annual cost of the value-weighted quintile long-short at ``bps`` per unit of one-way turnover."""
    prev, tot, n = None, 0.0, 0
    for w in np.unique(d):
        m = d == w
        k = np.argsort(np.argsort(f[m])) * QN // m.sum()
        wt = np.zeros(m.sum())
        hi, lo = k == QN - 1, k == 0
        wt[hi] = qv[m][hi] / qv[m][hi].sum()
        wt[lo] = -qv[m][lo] / qv[m][lo].sum()
        cur = dict(zip(np.flatnonzero(m), wt))
        if prev is not None:
            keys = set(prev) | set(cur)
            tot += sum(abs(cur.get(k_, 0) - prev.get(k_, 0)) for k_ in keys)
            n += 1
        prev = {P_: v for P_, v in cur.items()}
    return 52 * (tot / max(n, 1)) * bps * 1e-4


def compute_envelope() -> dict:
    import inspect

    from explainer.quant.house import track
    P = _panel()
    d = P["date"]
    out = {}
    # --- the network ensemble on coins: fitted on 2018-2020, opened on 2021-2025
    code = inspect.getsource(_panel) + inspect.getsource(ML.MLPEnsemble) + inspect.getsource(_fit_zoo)
    n_trials = len(ZOO) + 5 + 6 + 5            # the zoo, plus the tuning grids of ENet, PCR and PLS
    pit.register("nn3_coin_ls_part27", code, {"model": "NN3 (32-16-8), 5 seeds", "train": "2018-01..2020-06",
                                              "validate": "2020-07..2020-12", "portfolio": "quintile long-short, weekly, "
                                              "weighted by 28-day median dollar volume", "universe": f"median volume >= {MIN_QV}"},
                 trials=n_trials)
    weeks = np.unique(d)
    M = np.full((len(weeks), len(P["names"])), -999.0)
    for k, w in enumerate(weeks):
        m = d == w
        M[k, P["coin"][m]] = np.round(P["ret"][m], 10)
    pit.open_envelope("nn3_coin_ls_part27", "binance/usdt_weekly_panel", weeks, M)
    tr, va = d < 20200701, (d >= 20200701) & (d < 20201224)
    f = _fit_zoo("NN3", P["X"][tr], _winsor(P["y"][tr]), P["X"][va], _winsor(P["y"][va]))
    hold = d >= HOLD
    fh = f(P["X"][hold])
    vw = ML.decile_spread(d[hold], fh, P["ret"][hold], q=QN, weights=P["qv"][hold])
    ew = ML.decile_spread(d[hold], fh, P["ret"][hold], q=QN)
    z = load("zoo")["rows"]["NN3"]
    cost = _turnover_cost(d[hold], fh, P["qv"][hold])
    ym_r, mr = _monthly_compound(*_zoo_research_vw(P))
    ym_h, mh = _monthly_compound(vw["date"], vw["ls"])
    row = track.record("nn3_coin_ls_part27", 27, mr, mh, cost, note="value-weighted quintile long-short, weekly")
    out["nn3"] = {"row": row, "sr_vw": B.sharpe(vw["ls"], 52), "sr_ew": B.sharpe(ew["ls"], 52), "cost": cost,
                  "r2": ML.r2_oos(P["y"][hold], fh), "weeks": vw["date"], "cum_vw": np.cumsum(np.log1p(np.clip(vw["ls"], -0.99, None))),
                  "research_sr_vw": z["sr_vw"], "first": int(vw["date"][0]), "last": int(vw["date"][-1])}
    # --- the random-feature timer: opened on the Welch-Goyal predictors of 2021-2025
    pit.register("kmz_timer_part27", inspect.getsource(ML.kmz_timing) + inspect.getsource(ML.rff) +
                 inspect.getsource(_timing_data), {"P": 12000, "z": 0.1, "T": 12, "gamma": 2.0, "seeds": 10,
                                                   "scale": "10% a year in research"}, trials=len(KMZ_P) * len(KMZ_Z))
    g = data.goyal_welch("2025-12")
    cols = [k for k in g if k != "date"]
    V = np.column_stack([np.nan_to_num(g[k], nan=-999) for k in cols])
    pit.open_envelope("kmz_timer_part27", "goyal/welch_goyal_monthly", g["date"] * 100 + 1, V)
    td = _timing_data("2025-12")
    X, r, rx, vol, dd = td["X"], td["r"], td["rx"], td["vol"], td["date"]
    t_h = int(np.searchsorted(dd, 202101))
    fc = ML.kmz_timing(X, r, T=12, Ps=(12000,), zs=(0.1,), gamma=2.0, n_seeds=10, start=t_h)["F"][12000][0.1]
    kres = load("kmz")
    t0 = int(np.searchsorted(dd, kres["first"]))
    f_res = np.asarray(kres["position"])
    strat_res = f_res * r[t0:t_h]
    scale = 0.10 / (np.std(strat_res) * math.sqrt(12))
    strat_h = scale * fc[t_h:] * r[t_h:]
    rowk = track.record("kmz_timer_part27", 27, scale * strat_res, strat_h, 0.001, note="RFF ridge, P = 12000, z = 0.1")
    out["kmz"] = {"row": rowk, "sr_hold": B.sharpe(strat_h, 12), "sr_mkt_hold": B.sharpe(r[t_h:], 12),
                  "ym": dd[t_h:], "cum": np.cumsum(strat_h), "first": int(dd[t_h]), "last": int(dd[-1])}
    out["trials"] = pit.trials_so_far()
    return _json(out)


def _zoo_research_preds(P, f):
    d = P["date"]
    m = (d >= 20200101) & (d < 20201224)
    return d[m], f(P["X"][m]), P["ret"][m]


def _zoo_research_vw(P):
    """The NN3 strategy's research-window weekly returns: the zoo's expanding 2019 and 2020 tests, value-weighted."""
    out_d, out_r = [], []
    for year in (2019, 2020):
        tr, va, te = _split(P, year)
        f = _fit_zoo("NN3", P["X"][tr], _winsor(P["y"][tr]), P["X"][va], _winsor(P["y"][va]))
        s = ML.decile_spread(P["date"][te], f(P["X"][te]), P["ret"][te], q=QN, weights=P["qv"][te])
        out_d.append(s["date"])
        out_r.append(s["ls"])
    return np.concatenate(out_d), np.concatenate(out_r)


ITEMS = {"snr": compute_snr, "kmz": compute_kmz, "nagel": compute_nagel, "panel": compute_panel, "zoo": compute_zoo,
         "descent": compute_descent, "autoenc": compute_autoenc, "attention": compute_attention, "images": compute_images,
         "sdf": compute_sdf, "toolkit": compute_toolkit, "conformal": compute_conformal, "pretrained": compute_pretrained,
         "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
