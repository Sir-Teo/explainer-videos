"""Every number in Part 30 (Portfolio Construction), computed and cached in .cache/quant30/.

    python -m videos.quant.quant30.compute [items] [--force]

The universe: Kenneth French's 49 value-weighted industry portfolios, monthly (complete from July 1969) and daily;
the risk-free rate from the Fama-French monthly factors. Research uses data to December 2020; 2021-2025 is sealed and
read once, in ``envelope``.

* ``universe``    the panel's size, and the industries' market capitalisations at the end of 2020;
* ``michaud``     error maximisation: estimated frontiers and what the estimated portfolios really deliver;
* ``rolling``     every rule, rebalanced monthly on trailing windows, 1980-2020: 1/N, the sample rules, the shrunk ones,
                  risk parity, HRP;
* ``spectrum``    the correlation spectrum of daily industry returns against Marchenko and Pastur;
* ``shrink``      the estimators' errors, and the shrinkage intensities through time;
* ``constraints`` Jagannathan and Ma: the long-only constraint as shrinkage;
* ``bl``          Black-Litterman on the industries: equilibrium returns, one view, the posterior;
* ``riskparity``  inverse volatility, equal risk contributions and HRP on 2011-2020;
* ``cvar``        minimum CVaR as a linear program against minimum variance;
* ``growth``      Kelly on the market; Cover's universal portfolio on two industries; Fernholz's diversity weights;
* ``views``       Meucci's entropy pooling on the industries' monthly scenarios;
* ``e2e``         an end-to-end portfolio network trained on the Sharpe ratio;
* ``theory``      the research chapter: the sample minimum-variance portfolio's risk, in and out of sample;
* ``envelope``    shrunk minimum variance, HRP and 1/N, registered and opened on 2021-2025.
"""

from __future__ import annotations

import functools
import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import pit, portfolio as P

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant30")
load = pit.counted(CACHE.load, 30)
START = 197001
RESEARCH_END = 202012
EVAL_START = 198001
WINDOWS = (60, 120)


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


@functools.lru_cache(maxsize=None)
def _monthly(through: str = "2020-12"):
    ind = data.ken_french_industries(49, through=through)
    ff = data.ken_french_factors_monthly(through=through)
    d = ind["date"]
    m = d >= START
    rf = dict(zip(ff["date"], ff["rf"]))
    R = ind["returns"][m]
    return d[m], list(ind["columns"]), R, np.array([rf[x] for x in d[m]])


@functools.lru_cache(maxsize=None)
def _caps():
    n = data.ken_french_block("49_Industry_Portfolios_CSV.zip", "  Number of Firms in Portfolios", "industries49_nfirms",
                              202012)
    s = data.ken_french_block("49_Industry_Portfolios_CSV.zip", "  Average Firm Size", "industries49_size", 202012)
    return n["date"], n["values"] * s["values"]          # $ millions, the start of each month


def compute_universe() -> dict:
    d, cols, R, rf = _monthly()
    cd, caps = _caps()
    last = caps[-1]
    w = last / np.nansum(last)
    order = np.argsort(-w)
    return _json({"n_months": len(d), "first": int(d[0]), "last": int(d[-1]), "columns": cols, "cap_w": w,
                  "top": [cols[i] for i in order[:5]], "top_w": w[order[:5]], "mean": R.mean(0) * 12,
                  "vol": R.std(0) * math.sqrt(12), "rf": rf.mean() * 12})


# ---------------------------------------------------------------------------
# Error maximisation (Michaud 1989)
# ---------------------------------------------------------------------------
def compute_michaud(reps: int = 300) -> dict:
    d, cols, R, rf = _monthly()
    X = R - rf[:, None]
    mu, S = X.mean(0), np.cov(X, rowvar=False)
    rng = np.random.default_rng(3001)
    L = np.linalg.cholesky(S)
    targets = np.linspace(0.004, 0.016, 25)
    true_f = P.frontier(mu, S, targets)
    out = {}
    for T in (60, 240):
        est_f, real_pts, corr_err, maxw, res_pts = [], [], [], [], []

        def target_w(m_hat, S_hat, t=0.01):
            Si = np.linalg.inv(S_hat)
            one = np.ones(len(m_hat))
            A, B, C = one @ Si @ one, one @ Si @ m_hat, m_hat @ Si @ m_hat
            lam, gam = (C - t * B) / (A * C - B ** 2), (t * A - B) / (A * C - B ** 2)
            return Si @ (lam * one + gam * m_hat)
        for r in range(reps):
            Y = mu + rng.standard_normal((T, len(mu))) @ L.T
            m_hat, S_hat = Y.mean(0), np.cov(Y, rowvar=False)
            if r < 100:                                   # Michaud's resampled efficiency: average over resamples
                ws = []
                for _ in range(30):
                    Z = m_hat + rng.standard_normal((T, len(mu))) @ np.linalg.cholesky(S_hat).T
                    ws.append(target_w(Z.mean(0), np.cov(Z, rowvar=False)))
                wr = np.mean(ws, 0)
                res_pts.append([math.sqrt(wr @ S @ wr), wr @ mu])
            if r < 12:
                est_f.append(P.frontier(m_hat, S_hat, targets))
            # the estimated portfolio at a 1% a month target, judged under the truth
            Si = np.linalg.inv(S_hat)
            one = np.ones(len(mu))
            A, B, C = one @ Si @ one, one @ Si @ m_hat, m_hat @ Si @ m_hat
            t = 0.01
            lam, gam = (C - t * B) / (A * C - B ** 2), (t * A - B) / (A * C - B ** 2)
            wt = Si @ (lam * one + gam * m_hat)
            real_pts.append([math.sqrt(wt @ S @ wt), wt @ mu, math.sqrt(wt @ S_hat @ wt), wt @ m_hat])
            corr_err.append(np.corrcoef(wt, m_hat - mu)[0, 1])
            maxw.append(np.abs(wt).max())
        out[str(T)] = {"est": est_f, "pts": real_pts, "corr_err": float(np.mean(corr_err)),
                       "maxw_median": float(np.median(maxw)), "resampled": res_pts}
    # Best and Grauer's sensitivity: raise one industry's expected return by 1% a year
    i_s = cols.index("Softw")
    w0 = P.tangency(mu, S)
    shock = math.sqrt(S[i_s, i_s] / 60)                   # one standard error of a five-year mean
    mu1 = mu.copy()
    mu1[i_s] += shock
    w1 = P.tangency(mu1, S)
    sens = {"industry": "Softw", "dw_l1": float(np.abs(w1 - w0).sum()), "dw_self": float(w1[i_s] - w0[i_s]),
            "gross0": float(np.abs(w0).sum()), "shock_year": float(shock * 12), "w0_self": float(w0[i_s])}
    return _json({"targets": targets, "true": true_f, "sims": out, "reps": reps, "sens": sens,
                  "true_min_vol": float(1 / math.sqrt(np.ones(49) @ np.linalg.solve(S, np.ones(49))))})


# ---------------------------------------------------------------------------
# Rolling rules, 1980-2020
# ---------------------------------------------------------------------------
def _rules():
    def ew(Y):
        return np.full(Y.shape[1], 1 / Y.shape[1])

    def iv(Y):
        v = 1 / Y.var(0)
        return v / v.sum()

    def tan(Y):
        w = P.tangency(Y.mean(0), P.sample_cov(Y))
        return w if np.isfinite(w).all() else ew(Y)
    return {
        "1/N": ew,
        "inverse volatility": iv,
        "sample tangency": tan,
        "sample GMV": lambda Y: P.gmv(P.sample_cov(Y)),
        "long-only GMV": lambda Y: P.gmv(P.sample_cov(Y), long_only=True),
        "LW identity GMV": lambda Y: P.gmv(P.lw_identity(Y)[0]),
        "LW const-corr GMV": lambda Y: P.gmv(P.lw_constcorr(Y)[0]),
        "RMT-clipped GMV": lambda Y: P.gmv(P.rmt_clip(Y)[0]),
        "nonlinear GMV": lambda Y: P.gmv(P.lw_nonlinear(Y)),
        "ERC": lambda Y: P.erc(P.sample_cov(Y)),
        "HRP": lambda Y: P.hrp(P.sample_cov(Y))[0],
    }


def _run(d, R, rf, rule, W, start):
    """Rebalance at each month-end from ``start`` on the trailing W months (excess returns); hold one month."""
    X = R - rf[:, None]
    idx = np.flatnonzero(d >= start)
    rets, weights, pred = [], [], []
    for t in idx:
        if t < W:
            continue
        Y = X[t - W:t]
        w = rule(Y)
        weights.append(w)
        rets.append(float(w @ X[t]))
        pred.append(float(w @ np.cov(Y, rowvar=False) @ w))
    return np.array(rets), np.array(weights), np.array(pred), d[idx[idx >= W]]


def _stats(r):
    return {"sharpe": float(r.mean() / r.std(ddof=1) * math.sqrt(12)), "vol": float(r.std(ddof=1) * math.sqrt(12)),
            "mean": float(r.mean() * 12)}


def compute_rolling() -> dict:
    d, cols, R, rf = _monthly()
    out = {}
    for W in WINDOWS:
        res = {}
        for name, rule in _rules().items():
            r, Wt, pred, dd = _run(d, R, rf, rule, W, EVAL_START)
            st = _stats(r)
            st["turnover"] = P.turnover(Wt)
            st["gross"] = float(np.mean(np.abs(Wt).sum(1)))
            st["max_w"] = float(np.mean(np.abs(Wt).max(1)))
            st["pred_vol"] = float(np.sqrt(np.mean(pred)) * math.sqrt(12))
            res[name] = st
        out[str(W)] = res
    return _json({"windows": list(WINDOWS), "rules": list(_rules()), "res": out, "start": EVAL_START,
                  "n_configs": len(WINDOWS) * len(_rules())})


# ---------------------------------------------------------------------------
# The spectrum
# ---------------------------------------------------------------------------
def compute_spectrum() -> dict:
    dd = data.ken_french_industries_daily(49, through="2020-12-31")
    m = dd["date"] >= 19700101
    D, R = dd["date"][m], np.nan_to_num(dd["returns"][m])
    out = {}
    for y in (2019, 2008):
        k = (D // 10000) == y
        Y = R[k]
        C = np.corrcoef(Y, rowvar=False)
        lam = np.sort(np.linalg.eigvalsh(C))[::-1]
        T, N = Y.shape
        a, b = P.mp_edges(N / T)
        rng = np.random.default_rng(3002)
        Z = np.column_stack([rng.permutation(Y[:, j]) for j in range(N)])
        lz = np.sort(np.linalg.eigvalsh(np.corrcoef(Z, rowvar=False)))[::-1]
        # the market mode removed: eigenvalues of the residual correlation after the first component
        lam_, V = np.linalg.eigh(C)
        v1, v2 = V[:, -1], V[:, -2]
        v1 = v1 * np.sign(v1.sum())
        o2 = np.argsort(v2)
        out[str(y)] = {"lam": lam, "shuffled": lz, "T": T, "N": N, "edge": [a, b], "n_above": int((lam > b).sum()),
                       "share1": float(lam[0] / N), "v1": v1, "v2_low": [dd["columns"][i] for i in o2[:4]],
                       "v2_high": [dd["columns"][i] for i in o2[-4:]]}
    # the largest eigenvalue's share through time, rolling one year
    years = list(range(1971, 2021))
    share = []
    for y in years:
        k = (D // 10000) == y
        lam = np.linalg.eigvalsh(np.corrcoef(R[k], rowvar=False))
        share.append(float(lam.max() / R.shape[1]))
    return _json({"years": out, "share_years": years, "share": share})


# ---------------------------------------------------------------------------
# Shrinkage: errors and intensities
# ---------------------------------------------------------------------------
def compute_shrink() -> dict:
    d, cols, R, rf = _monthly()
    X = R - rf[:, None]
    # the estimators against a known truth: the full-sample covariance, simulated windows
    S0 = np.cov(X, rowvar=False)
    L = np.linalg.cholesky(S0)
    rng = np.random.default_rng(3003)
    one = np.ones(49)
    vmin = 1 / (one @ np.linalg.solve(S0, one))
    est = {"sample": P.sample_cov, "LW identity": lambda Y: P.lw_identity(Y)[0],
           "LW const-corr": lambda Y: P.lw_constcorr(Y)[0], "RMT clipped": lambda Y: P.rmt_clip(Y)[0],
           "nonlinear": P.lw_nonlinear}
    sims = {}
    for T in (60, 120, 240):
        errs = {k: [] for k in est}
        gmvv = {k: [] for k in est}
        for _ in range(100):
            Y = rng.standard_normal((T, 49)) @ L.T
            for k, f in est.items():
                E = f(Y)
                errs[k].append(np.linalg.norm(E - S0) / np.linalg.norm(S0))
                w = P.gmv(E)
                gmvv[k].append(w @ S0 @ w / vmin)
        sims[str(T)] = {k: {"err": float(np.mean(errs[k])), "gmv": float(np.mean(gmvv[k]))} for k in est}
    # one simulated ten-year window: the eigenvalues each estimator assigns, against the truth and the oracle
    Y = rng.standard_normal((120, 49)) @ L.T
    Ssm = np.cov(Y, rowvar=False)
    lam_s, U = np.linalg.eigh(Ssm)
    eig = {"true": np.sort(np.linalg.eigvalsh(S0))[::-1], "sample": lam_s[::-1],
           "oracle": np.array([u @ S0 @ u for u in U.T])[::-1],
           "LW const-corr": np.array([u @ P.lw_constcorr(Y)[0] @ u for u in U.T])[::-1],
           "nonlinear": np.array([u @ P.lw_nonlinear(Y) @ u for u in U.T])[::-1]}
    # intensities through time on the real data, 120-month windows
    dates, k_id, k_cc = [], [], []
    for t in range(120, len(d), 12):
        Y = X[t - 120:t]
        dates.append(int(d[t]))
        k_id.append(P.lw_identity(Y)[1])
        k_cc.append(P.lw_constcorr(Y)[1])
    return _json({"sims": sims, "estimators": list(est), "dates": dates, "k_identity": k_id, "k_constcorr": k_cc,
                  "eig": eig})


# ---------------------------------------------------------------------------
# Factor-model covariances and shrunk means (studied after the envelope was registered; not part of its count)
# ---------------------------------------------------------------------------
def _pca_cov(Y, k):
    S = np.cov(Y, rowvar=False)
    lam, V = np.linalg.eigh(S)
    lam, V = lam[::-1], V[:, ::-1]
    B = V[:, :k] * np.sqrt(lam[:k])
    D = np.diag(np.maximum(np.diag(S - B @ B.T), 1e-8))
    return B @ B.T + D


def _index_cov(Y):
    m = Y.mean(1)
    var_m = m.var(ddof=1)
    beta = np.array([np.cov(Y[:, i], m)[0, 1] / var_m for i in range(Y.shape[1])])
    resid = Y - np.outer(m, beta)
    return np.outer(beta, beta) * var_m + np.diag(resid.var(0, ddof=1))


def _bayes_stein(Y):
    """Jorion (1986): shrink each sample mean toward the minimum-variance portfolio's mean."""
    T, N = Y.shape
    mu = Y.mean(0)
    S = np.cov(Y, rowvar=False)
    Si = np.linalg.inv(S)
    one = np.ones(N)
    mu0 = (one @ Si @ mu) / (one @ Si @ one)
    d = mu - mu0
    phi = (N + 2) / ((N + 2) + T * d @ Si @ d)
    return (1 - phi) * mu + phi * mu0, float(phi)


def compute_factor() -> dict:
    d, cols, R, rf = _monthly()
    rules = {"single index": lambda Y: P.gmv(_index_cov(Y)), "1 PCA factor": lambda Y: P.gmv(_pca_cov(Y, 1)),
             "3 PCA factors": lambda Y: P.gmv(_pca_cov(Y, 3)), "5 PCA factors": lambda Y: P.gmv(_pca_cov(Y, 5)),
             "sample tangency": lambda Y: P.tangency(Y.mean(0), P.lw_constcorr(Y)[0]),
             "Bayes-Stein tangency": lambda Y: P.tangency(_bayes_stein(Y)[0], P.lw_constcorr(Y)[0])}
    out = {}
    for name, rule in rules.items():
        r, Wt, pred, dd = _run(d, R, rf, rule, 120, EVAL_START)
        st = _stats(r)
        st["turnover"] = P.turnover(Wt)
        st["gross"] = float(np.mean(np.abs(Wt).sum(1)))
        st["pred_vol"] = float(np.sqrt(np.mean(pred)) * math.sqrt(12))
        out[name] = st
    X = R - rf[:, None]
    phis = [_bayes_stein(X[t - 120:t])[1] for t in range(120, len(X), 12)]
    return _json({"res": out, "phi_mean": float(np.mean(phis)), "phi_min": float(np.min(phis)),
                  "phi_max": float(np.max(phis))})


# ---------------------------------------------------------------------------
# Constraints as shrinkage (Jagannathan and Ma 2003)
# ---------------------------------------------------------------------------
def compute_constraints() -> dict:
    d, cols, R, rf = _monthly()
    X = R - rf[:, None]
    Y = X[-120:]
    S = np.cov(Y, rowvar=False)
    w_u = P.gmv(S)
    w_l = P.gmv(S, long_only=True)
    g = 2 * w_l @ S @ w_l
    lam = 2 * S @ w_l - g                                  # KKT multipliers of w >= 0 (zero where w > 0)
    lam = np.where(w_l > 1e-6, 0.0, np.maximum(lam, 0))
    S_jm = S - 0.5 * (np.outer(lam, np.ones(49)) + np.outer(np.ones(49), lam))
    w_jm = P.gmv(S_jm)
    return _json({"columns": cols, "w_unc": w_u, "w_long": w_l, "w_jm": w_jm, "lam": lam,
                  "n_pos": int((w_l > 1e-6).sum()), "short_sum": float(-w_u[w_u < 0].sum()),
                  "jm_match": float(np.abs(w_jm - w_l).max())})


# ---------------------------------------------------------------------------
# Black-Litterman
# ---------------------------------------------------------------------------
def compute_bl() -> dict:
    d, cols, R, rf = _monthly()
    X = R - rf[:, None]
    Y = X[-120:]
    S = np.cov(Y, rowvar=False)
    cd, caps = _caps()
    w_m = caps[-1] / np.nansum(caps[-1])
    mkt = Y @ w_m
    delta = float(mkt.mean() / mkt.var(ddof=1))
    tau = 1 / 120
    i_s, i_u = cols.index("Softw"), cols.index("Util")
    Pm = np.zeros((1, 49))
    Pm[0, i_s], Pm[0, i_u] = 1, -1
    Q = np.array([0.03 / 12])                             # a view: software beats utilities by 3% a year
    pi, post = P.black_litterman(S, w_m, delta, tau, Pm, Q)
    w_post = np.linalg.solve(S, post) / delta
    w_eq = np.linalg.solve(S, pi) / delta
    w_samp = np.linalg.solve(S, Y.mean(0)) / delta
    sweep = []
    base = float((Pm @ (tau * S) @ Pm.T)[0, 0])
    for c in np.logspace(-2, 2, 21):
        _, pc = P.black_litterman(S, w_m, delta, tau, Pm, Q, np.array([[base * c]]))
        sweep.append([float(c), float((pc[i_s] - pc[i_u]) * 12)])
    return _json({"columns": cols, "w_mkt": w_m, "delta": delta, "tau": tau, "pi": pi * 12, "post": post * 12,
                  "sweep": sweep,
                  "w_post": w_post, "w_eq": w_eq, "w_sample": w_samp, "view": ["Softw", "Util", 0.03],
                  "sample_mean": Y.mean(0) * 12, "gross_sample": float(np.abs(w_samp).sum()),
                  "gross_post": float(np.abs(w_post).sum())})


# ---------------------------------------------------------------------------
# Risk parity and HRP
# ---------------------------------------------------------------------------
def compute_riskparity() -> dict:
    d, cols, R, rf = _monthly()
    X = R - rf[:, None]
    Y = X[-120:]
    S = np.cov(Y, rowvar=False)
    ws = {"1/N": np.full(49, 1 / 49), "inverse volatility": (1 / np.sqrt(np.diag(S))) / (1 / np.sqrt(np.diag(S))).sum(),
          "ERC": P.erc(S), "GMV": P.gmv(S), "HRP": P.hrp(S)[0]}
    rc = {k: P.risk_contributions(w, S) for k, w in ws.items()}
    order = P.hrp(S)[1]
    from scipy.cluster.hierarchy import linkage
    from scipy.spatial.distance import squareform
    sd = np.sqrt(np.diag(S))
    C = S / np.outer(sd, sd)
    Z = linkage(squareform(np.sqrt(np.maximum((1 - C) / 2, 0)), checks=False), method="single")
    return _json({"columns": cols, "weights": ws, "rc": rc, "order": order, "linkage": Z, "corr": C,
                  "vol": {k: float(math.sqrt(w @ S @ w * 12)) for k, w in ws.items()}})


# ---------------------------------------------------------------------------
# CVaR
# ---------------------------------------------------------------------------
def compute_cvar() -> dict:
    d, cols, R, rf = _monthly()
    X = R - rf[:, None]
    S = np.cov(X, rowvar=False)
    w_mv = P.gmv(S, long_only=True)
    w_cv, var95, cv95 = P.min_cvar(X, 0.95)
    out = {}
    for k, w in (("min variance", w_mv), ("min CVaR", w_cv)):
        r = X @ w
        out[k] = {"vol": float(r.std(ddof=1) * math.sqrt(12)), "cvar": P.cvar_of(-r, 0.95), "worst": float(r.min()),
                  "w": w, "r": r, "n_held": int((w > 1e-4).sum())}
    # out of sample, rolling 120 months
    oos = {}
    for k, f in (("min variance", lambda Y: P.gmv(np.cov(Y, rowvar=False), long_only=True)),
                 ("min CVaR", lambda Y: P.min_cvar(Y, 0.95)[0])):
        r, Wt, _, _ = _run(d, R, rf, f, 120, EVAL_START)
        oos[k] = {"vol": float(r.std(ddof=1) * math.sqrt(12)), "cvar": P.cvar_of(-r, 0.95), "worst": float(r.min())}
    return _json({"columns": cols, "in": out, "oos": oos, "J": len(X)})


# ---------------------------------------------------------------------------
# Growth: Kelly, Cover, Fernholz
# ---------------------------------------------------------------------------
def compute_growth() -> dict:
    d, cols, R, rf = _monthly()
    ff = data.ken_french_factors_monthly(through="2020-12")
    mk = {a: b for a, b in zip(ff["date"], ff["mkt_rf"])}
    m = np.array([mk[x] for x in d])
    mu, s2 = m.mean() * 12, m.var(ddof=1) * 12
    f_star = mu / s2
    fs = np.linspace(0, 4, 81)
    g_th = rf.mean() * 12 + fs * mu - fs ** 2 * s2 / 2
    g_emp = [float(np.mean(np.log1p(rf + f * m))) * 12 if np.all(1 + rf + f * m > 0) else float("nan") for f in fs]
    # Cover's universal portfolio on two industries, monthly 1970-2020
    a, b = cols.index("Gold"), cols.index("Util")
    G = 1 + R[:, [a, b]]
    bgrid, wealth, uni, best = P.universal_2(G)
    # Fernholz: diversity-weighted (p = 0.5) against cap-weighted, monthly, caps at the start of each month
    cd, caps = _caps()
    cmap = {x: i for i, x in enumerate(cd)}
    rel, dates = [], []
    for t, x in enumerate(d):
        c = caps[cmap[x]]
        if not np.isfinite(c).all():
            continue
        wm = c / c.sum()
        wd = P.diversity_weights(c, 0.5)
        rel.append([float(wm @ R[t]), float(wd @ R[t])])
        dates.append(int(x))
    rel = np.array(rel)
    return _json({"kelly": f_star, "mu": mu, "s2": s2, "fs": fs, "g_theory": g_th, "g_emp": g_emp,
                  "cover": {"pair": [cols[a], cols[b]], "b": bgrid, "wealth": wealth, "uni": uni, "best": best,
                            "n": len(G), "b_best": float(bgrid[int(np.argmax(wealth))]),
                            "bound": len(G) + 1},
                  "spt": {"dates": dates, "cum_mkt": np.cumsum(np.log1p(rel[:, 0])),
                          "cum_div": np.cumsum(np.log1p(rel[:, 1])),
                          "excess": float((np.log1p(rel[:, 1]) - np.log1p(rel[:, 0])).mean() * 12)}})


# ---------------------------------------------------------------------------
# Entropy pooling
# ---------------------------------------------------------------------------
def compute_views() -> dict:
    d, cols, R, rf = _monthly()
    X = R - rf[:, None]
    J = len(X)
    p = np.full(J, 1 / J)
    i_b = cols.index("Banks")
    view = -0.03
    q = P.entropy_pooling(X, p, X[:, i_b][None, :], [view])
    ens = float(np.exp(-np.sum(q * np.log(q))))
    post = q @ X
    prior = p @ X
    Sq = (X - post).T @ np.diag(q) @ (X - post)
    w_prior = P.gmv(np.cov(X, rowvar=False), long_only=True)
    w_post = P.gmv(Sq, long_only=True)
    top_t = np.argsort(-q)[:5]
    cd, caps = _caps()
    cmap = {x: i for i, x in enumerate(cd)}
    wm = np.array([caps[cmap[x]] / np.nansum(caps[cmap[x]]) for x in d])
    mkt = np.nansum(wm * X, 1)
    m0, v0 = mkt.mean(), mkt.var()
    q2 = P.entropy_pooling(X, p, ((mkt - m0) ** 2)[None, :], [4 * v0])
    ens2 = float(np.exp(-np.sum(q2 * np.log(q2))))
    S_prior = np.cov(X, rowvar=False)
    Sq2 = (X - q2 @ X).T @ np.diag(q2) @ (X - q2 @ X)
    cor = lambda M: (M / np.sqrt(np.outer(np.diag(M), np.diag(M))))[np.triu_indices(49, 1)].mean()
    vol_view = {"ens": ens2, "corr_prior": float(cor(S_prior)), "corr_post": float(cor(Sq2)),
                "vol_prior": float(math.sqrt(v0 * 12)), "vol_post": float(math.sqrt(q2 @ (mkt - m0) ** 2 * 12))}
    return _json({"columns": cols, "view": ["Banks", view], "q": q, "dates": d, "ens": ens, "J": J,
                  "prior": prior * 12, "post": post * 12, "top_dates": d[top_t], "top_q": q[top_t],
                  "w_prior": w_prior, "w_post": w_post, "vol_view": vol_view})


# ---------------------------------------------------------------------------
# End-to-end
# ---------------------------------------------------------------------------
def compute_e2e(epochs: int = 300) -> dict:
    import torch
    import torch.nn as nn
    torch.manual_seed(30)
    torch.set_num_threads(2)
    d, cols, R, rf = _monthly()
    X = R - rf[:, None]
    T, N = X.shape

    def feats(t):
        past = X[t - 12:t]
        return np.stack([past.mean(0) * 12, past.std(0) * math.sqrt(12), X[t - 1], X[t - 60:t].mean(0) * 12], -1)
    ts = np.arange(60, T)
    F = np.stack([feats(t) for t in ts])                       # (months, N, 4)
    F = (F - F.mean((0, 1))) / F.std((0, 1))
    Yn = X[ts]
    tr = d[ts] < 200601
    va = ~tr

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.f = nn.Sequential(nn.Linear(4, 16), nn.Tanh(), nn.Linear(16, 1))

        def forward(self, x):
            return torch.softmax(self.f(x).squeeze(-1), dim=-1)    # long-only weights summing to one
    net = Net()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2, weight_decay=1e-4)
    Ft, Yt = torch.tensor(F, dtype=torch.float32), torch.tensor(Yn, dtype=torch.float32)
    hist = []
    for ep in range(epochs):
        w = net(Ft[tr])
        r = (w * Yt[tr]).sum(-1)
        loss = -r.mean() / r.std() * math.sqrt(12)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if ep % 10 == 0 or ep == epochs - 1:
            with torch.no_grad():
                rv = (net(Ft[va]) * Yt[va]).sum(-1)
                hist.append({"ep": ep, "train": float(-loss), "valid": float(rv.mean() / rv.std() * math.sqrt(12))})
    with torch.no_grad():
        W = net(Ft).numpy()
    r_e2e = (W * Yn).sum(-1)
    # two-step: predict each industry's next return by its trailing 12-month mean (the network's first input),
    # then a long-only mean-variance portfolio on the shrunk covariance
    r_two, r_ew = [], []
    for k, t in enumerate(ts):
        Yw = X[t - 60:t]
        S = P.lw_constcorr(Yw)[0]
        mu = X[t - 12:t].mean(0)
        w = np.maximum(np.linalg.solve(S, mu), 0)
        w = w / w.sum() if w.sum() > 0 else np.full(N, 1 / N)
        r_two.append(float(w @ X[t]))
        r_ew.append(float(X[t].mean()))
    r_two, r_ew = np.array(r_two), np.array(r_ew)
    sh = lambda r: float(r.mean() / r.std(ddof=1) * math.sqrt(12))
    return _json({"hist": hist, "train": {"e2e": sh(r_e2e[tr]), "two": sh(r_two[tr]), "ew": sh(r_ew[tr])},
                  "valid": {"e2e": sh(r_e2e[va]), "two": sh(r_two[va]), "ew": sh(r_ew[va])},
                  "max_w_valid": float(W[va].max(1).mean()), "eff_n_valid": float(np.mean(1 / (W[va] ** 2).sum(1)))})


# ---------------------------------------------------------------------------
# Research: the sample GMV portfolio's risk
# ---------------------------------------------------------------------------
def compute_theory() -> dict:
    d, cols, R, rf = _monthly()
    X = R - rf[:, None]
    S0 = np.cov(X, rowvar=False)
    rng = np.random.default_rng(3004)
    sims = {}
    for T in (60, 80, 120, 240, 600):
        s = P.gmv_sim(S0, T, 1000, rng)
        th = P.gmv_theory(49, T)
        sims[str(T)] = {"in": float(s["in"].mean()), "out": float(s["out"].mean()), "in_th": th["in"],
                        "out_th": th["out"], "in_lim": th["in_lim"], "out_lim": th["out_lim"],
                        "hist_in": np.histogram(s["in"], bins=30, range=(0, 2))[0],
                        "hist_out": np.histogram(s["out"], bins=30, range=(0, 6))[0]}
    # the data: predicted (in-sample) against realised (next 12 months) variance of the sample GMV, rolling
    data_rows, lw_rows = [], []
    for W in (60, 80, 120, 240):
        pl, rl_ = [], []
        for t in range(W, len(X) - 12, 12):
            if d[t] < EVAL_START:
                continue
            Y = X[t - W:t]
            S = P.lw_constcorr(Y)[0]
            w = P.gmv(S)
            pl.append(w @ S @ w)
            rl_.append(np.var(X[t:t + 12] @ w, ddof=1))
        lw_rows.append({"W": W, "ratio": float(np.mean(rl_) / np.mean(pl))})
        pred, real = [], []
        for t in range(W, len(X) - 12, 12):
            if d[t] < EVAL_START:
                continue
            Y = X[t - W:t]
            S = np.cov(Y, rowvar=False)
            w = P.gmv(S)
            pred.append(w @ S @ w)
            real.append(np.var(X[t:t + 12] @ w, ddof=1))
        th = P.gmv_theory(49, W)
        data_rows.append({"W": W, "ratio": float(np.mean(real) / np.mean(pred)), "theory": th["out"] / th["in"],
                          "pred_vol": float(math.sqrt(np.mean(pred) * 12)), "real_vol": float(math.sqrt(np.mean(real) * 12))})
    return _json({"sims": sims, "data": data_rows, "lw": lw_rows, "K": 49})


# ---------------------------------------------------------------------------
# The envelope
# ---------------------------------------------------------------------------
STRATS = {"lw_gmv_part30": ("LW const-corr GMV", 120), "hrp_part30": ("HRP", 120), "equal_weight_part30": ("1/N", 120)}


def compute_envelope() -> dict:
    import inspect
    from explainer.quant.house import track
    roll = load("rolling")
    n_trials = roll["n_configs"]
    code = inspect.getsource(_run) + inspect.getsource(_rules) + inspect.getsource(P.lw_constcorr) + \
        inspect.getsource(P.gmv) + inspect.getsource(P.hrp)
    for s, (rule, W) in STRATS.items():
        pit.register(s, code + s, {"rule": rule, "window_months": W, "rebalance": "monthly",
                                   "universe": "French 49 industries, value-weighted"},
                     trials=n_trials if s != "equal_weight_part30" else 1)
    ind = data.ken_french_industries(49, through="2025-12")
    ff = data.ken_french_factors_monthly(through="2025-12")
    out = {}
    for s in STRATS:
        pit.open_envelope(s, "kenfrench/industries49", ind["date"] * 100 + 1, ind["returns"])
        pit.open_envelope(s, "kenfrench/ff3_monthly", ff["date"] * 100 + 1,
                          np.column_stack([ff["mkt_rf"], ff["smb"], ff["hml"], ff["rf"]]))
    d_all = ind["date"]
    m = d_all >= START
    rfm = dict(zip(ff["date"], ff["rf"]))
    D, R = d_all[m], ind["returns"][m]
    rf = np.array([rfm[x] for x in D])
    rules = _rules()
    cost = 0.001                                       # 10 bp per dollar traded, one way
    for s, (rule, W) in STRATS.items():
        r, Wt, _, dd = _run(D, R, rf, rules[rule], W, EVAL_START)
        to = 0.5 * np.r_[0.0, np.abs(np.diff(Wt, axis=0)).sum(1)]
        res = dd <= RESEARCH_END
        hold = dd > RESEARCH_END
        cost_year = float(np.mean(2 * to[res]) * cost * 12)
        row = track.record(s, 30, r[res], r[hold], cost_year,
                           note=f"{rule}, {W}-month window, monthly; cost 10 bp a dollar traded on measured turnover")
        out[s] = {"rule": rule, "row": row, "cum_hold": np.cumsum(np.log1p(r[hold] + rf[np.isin(D, dd[hold])])),
                  "cum_res": np.cumsum(np.log1p(r[res] + rf[np.isin(D, dd[res])])), "res_dates": dd[res],
                  "hold_dates": dd[hold], "vol_hold": float(r[hold].std(ddof=1) * math.sqrt(12)),
                  "vol_res": float(r[res].std(ddof=1) * math.sqrt(12)), "turnover": float(np.mean(to[res]))}
    # the Sharpe-ratio difference between 1/N and each optimizer on the hold-out, with its standard error
    # (Jobson-Korkie with Memmel's correction, monthly)
    diffs = {}
    hr = {}
    for s_, (rule, W) in STRATS.items():
        r, _, _, dd = _run(D, R, rf, rules[rule], W, EVAL_START)
        hr[s_] = r[dd > RESEARCH_END]
    for s_ in ("lw_gmv_part30", "hrp_part30"):
        a, b = hr["equal_weight_part30"], hr[s_]
        T_ = len(a)
        sa, sb = a.mean() / a.std(ddof=1), b.mean() / b.std(ddof=1)
        rho = np.corrcoef(a, b)[0, 1]
        var = (2 - 2 * rho + 0.5 * (sa ** 2 + sb ** 2 - 2 * sa * sb * rho ** 2)) / T_
        diffs[s_] = {"diff": float((sa - sb) * math.sqrt(12)), "se": float(math.sqrt(var) * math.sqrt(12)),
                     "rho": float(rho)}
    # a descriptive check on the opened years: did they reward the industries that had been volatile?
    hold = D > RESEARCH_END
    prior = (D <= RESEARCH_END) & (D >= 201101)
    ann = np.nanmean(R[hold], 0) * 12
    vol = np.nanstd(R[prior], 0) * math.sqrt(12)
    top = np.argsort(-ann)[:4]
    return _json({"trials": pit.trials_so_far(), "n_trials": n_trials, "strats": out,
                  "vol_return_corr": float(np.corrcoef(ann, vol)[0, 1]), "diffs": diffs,
                  "top_hold": [ind["columns"][i] for i in top]})


ITEMS = {"universe": compute_universe, "michaud": compute_michaud, "rolling": compute_rolling,
         "spectrum": compute_spectrum, "shrink": compute_shrink, "constraints": compute_constraints, "bl": compute_bl,
         "riskparity": compute_riskparity, "cvar": compute_cvar, "growth": compute_growth, "views": compute_views,
         "e2e": compute_e2e, "theory": compute_theory, "envelope": compute_envelope, "factor": compute_factor}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
