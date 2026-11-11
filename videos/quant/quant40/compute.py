"""Every number in Part 40 (Measuring Risk), computed and cached in .cache/quant40/.

    python -m videos.quant.quant40.compute [items] [--force]

Data: Kenneth French's daily US market return (July 1926 to December 2020, the research window; the hold-out is not
opened) with its size and value factors, and his 49 value-weighted industries, daily, to 2020. Models: Gaussian,
Student-t, historical simulation, RiskMetrics, filtered historical simulation, GJR-GARCH with a generalised Pareto tail,
CAViaR and a quantile network; backtests, extreme-value fits, copulas, reverse stress tests and the rearrangement
algorithm.

* ``var3``      VaR and ES three ways on a $100m market position at the end of 2007 and in October 2008;
* ``sqrt``      the square-root-of-time rule against overlapping 10-day returns, overall and by decade;
* ``coherent``  two independent bonds: VaR that is not subadditive, ES that is;
* ``backtest``  six one-day forecasters, 1928-2020: exceedances, Kupiec, Christoffersen, the traffic light, Z2;
* ``evt``       the generalised Pareto tail of daily losses, Hill's estimator, and EVT quantiles beyond the data;
* ``depend``    correlation and tail dependence between industries, in calm and in crashes, against copulas;
* ``stress``    historical scenarios and the most plausible scenario for a given loss on a three-factor portfolio;
* ``ra``        the rearrangement algorithm's worst-case VaR for sums of Pareto losses;
* ``learned``   CAViaR and a quantile network, trained to 1990 and tested 1991-2020, against filtered HS;
* ``liq``       liquidity-adjusted VaR and FRTB's liquidity horizons, for an illustrative book;
* ``research``  elicitability: the level-set counterexample, the FZ0 score's minimum, forecasters ranked by FZ0, and
                the power of Kupiec's and Acerbi-Szekely's tests when only the tail beyond VaR is wrong.
"""

from __future__ import annotations

import json
import math
import warnings

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import pit
from explainer.quant.house import risk as R

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant40")
load = pit.counted(CACHE.load, 40)
THROUGH = "2020-12-31"


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _mkt():
    k = data.ken_french_daily(through=THROUGH)
    return k["date"], k["mkt"], k


def compute_var3() -> dict:
    d, r, _ = _mkt()
    out = {}
    for tag, day in (("2007", 20071231), ("2008", 20081015)):
        i = int(np.searchsorted(d, day))
        w = r[i - 500:i]
        nv, ne = R.var_es_normal(w.mean(), w.std(ddof=1))
        hv, he = R.var_es_hist(w)
        nu, loc, sc = stats.t.fit(w)
        tv, te = R.var_es_t(loc, sc, nu)
        rng = np.random.default_rng(40)
        sim = stats.t.rvs(nu, loc=loc, scale=sc, size=200_000, random_state=rng)
        mv, me = R.var_es_hist(sim)
        sig = R.ewma_sigma(r[:i + 1])[i]
        ev, ee = R.var_es_normal(0.0, sig)
        out[tag] = {"day": int(d[i]), "normal": (nv, ne), "hs": (hv, he), "t": (tv, te), "mc": (mv, me), "nu": nu,
                    "ewma": (ev, ee), "sig_ann": sig * math.sqrt(252), "next": float(r[i])}
    return _json(out)


def compute_sqrt() -> dict:
    d, r, _ = _mkt()
    res = R.sqrt_time(r)
    dec = []
    for y0 in range(1930, 2020, 10):
        s = (d >= y0 * 10000) & (d < (y0 + 10) * 10000)
        dec.append({"decade": y0, **R.sqrt_time(r[s])})
    z = stats.norm.ppf(0.99)
    return _json({**res, "decades": dec, "gauss_check": z * math.sqrt(10)})


def compute_coherent() -> dict:
    p, loss = 0.04, 100.0
    # each bond: lose 100 with probability 4%; 95% VaR of each is 0
    single = {"var": 0.0, "es": (p * loss) / 0.05}
    # two independent bonds: P(one or more) = 1 - 0.96^2 = 7.84%
    probs = {0: (1 - p) ** 2, 100: 2 * p * (1 - p), 200: p ** 2}
    xs = np.array(sorted(probs))
    ps = np.array([probs[x] for x in xs])
    c = np.cumsum(ps)
    k = int(np.searchsorted(c, 0.95 - 1e-12))
    var = float(xs[k])
    tail = (c[k] - 0.95) * var + float(np.sum(xs[k + 1:] * ps[k + 1:]))
    both = {"var": var, "es": tail / 0.05, "p_any": 1 - (1 - p) ** 2}
    return _json({"p": p, "loss": loss, "single": single, "both": both})


def compute_backtest() -> dict:
    d, r, _ = _mkt()
    f = R.rolling_forecasts(r, 0.99, refit=1250)
    start = 500
    out = {"methods": {}, "years": [int(x) for x in np.unique(d[start:] // 10000)]}
    for m, v in f.items():
        I = R.hits(r, v["var"])
        ku = R.kupiec(I, 0.01)
        ch = R.christoffersen(I, 0.01)
        z2 = R.acerbi_szekely_z2(r, v["var"], v["es"])
        yrs = d[start:] // 10000
        per_year = [int(I[yrs == y].sum()) for y in out["years"]]
        zones = [R.traffic_light(x) for x in per_year]
        out["methods"][m] = {"rate": ku["rate"], "x": ku["x"], "T": ku["T"], "kupiec_p": ku["p_value"],
                             "ind_p": ch["p_ind"], "cc_p": ch["p_cc"], "p11": ch["p11"], "z2": z2,
                             "per_year": per_year, "red": zones.count("red"), "yellow": zones.count("yellow")}
    # Z2's null distribution for this sample size, by simulation: correct forecasts of iid normal and t(4) losses
    rng = np.random.default_rng(99)
    T = int(out["methods"]["normal"]["T"])
    crit = {}
    for name, draw, ve in (("normal", lambda n: rng.standard_normal(n), R.var_es_normal(0.0, 1.0, 0.99)),
                           ("t4", lambda n: stats.t.rvs(4, size=n, random_state=rng), R.var_es_t(0.0, 1.0, 4.0, 0.99))):
        zs = [R.acerbi_szekely_z2(draw(T), np.full(T, ve[0]), np.full(T, ve[1])) for _ in range(400)]
        crit[name] = {"q95": float(np.quantile(zs, 0.95)), "q999": float(np.quantile(zs, 0.999))}
    out["z2_crit"] = crit
    # 2008 in detail, for the picture
    s = (d >= 20080101) & (d <= 20091231)
    out["y2008"] = {"d": d[s], "r": r[s], "normal": f["normal"]["var"][s], "gjr": f["gjr_fhs"]["var"][s],
                    "hs": f["hs"]["var"][s]}
    return _json(out)


def compute_evt() -> dict:
    d, r, _ = _mkt()
    L = -r
    u = float(np.quantile(L, 0.95))
    exc = L[L > u] - u
    xi, beta = R.gpd_fit(exc)
    n, nu_ = len(L), int((L > u).sum())
    rows = []
    for a in (0.99, 0.995, 0.999, 0.9999):
        ev = R.evt_var_es(u, xi, beta, n, nu_, a)
        hs = R.var_es_hist(r, a)
        nr = R.var_es_normal(r.mean(), r.std(ddof=1), a)
        rows.append({"alpha": a, "evt": ev, "hs": hs, "normal": nr})
    ks = np.array([25, 50, 100, 200, 400, 800, 1600])
    hill = R.hill_series(L, ks)
    # the empirical and fitted survival of the exceedances, for the picture
    ys = np.sort(exc)
    emp = 1 - np.arange(1, len(ys) + 1) / (len(ys) + 1)
    fit = (1 + xi * ys / beta) ** (-1 / xi)
    idx = np.unique(np.geomspace(1, len(ys), 120).astype(int) - 1)
    worst = int(np.argmax(L))
    return _json({"u": u, "xi": xi, "beta": beta, "n": n, "n_u": nu_, "rows": rows, "hill_k": ks, "hill": hill,
                  "surv": {"x": ys[idx] + u, "emp": emp[idx], "fit": fit[idx]}, "worst": float(L[worst]),
                  "worst_day": int(d[worst]), "kurt": float(stats.kurtosis(r)), "mu": float(r.mean()),
                  "sd": float(r.std(ddof=1)), "z_worst": float((L[worst] + r.mean()) / r.std(ddof=1)),
                  "log10_p_worst": float(stats.norm.logsf((L[worst] + r.mean()) / r.std(ddof=1)) / math.log(10))})


def compute_depend() -> dict:
    k = data.ken_french_industries_daily(49, through=THROUGH)
    d, X, cols = k["date"], k["returns"], k["columns"]
    _, m, _ = _mkt()
    ok = np.isfinite(X).all(1)
    pairs = [("Banks", "Insur"), ("Oil", "Mines"), ("Softw", "Chips"), ("Food", "Banks")]
    dd, mm = _mkt()[0], m
    mk = dict(zip(dd.tolist(), mm.tolist()))
    mkt = np.array([mk.get(int(x), np.nan) for x in d])
    bad = mkt <= np.nanquantile(mkt[ok], 0.05)
    rows = []
    for a, b in pairs:
        if a not in cols or b not in cols:
            continue
        x, y = X[:, cols.index(a)], X[:, cols.index(b)]
        s = ok & np.isfinite(x) & np.isfinite(y)
        rho = float(np.corrcoef(x[s], y[s])[0, 1])
        rho_bad = float(np.corrcoef(x[s & bad], y[s & bad])[0, 1])
        rho_calm = float(np.corrcoef(x[s & ~bad], y[s & ~bad])[0, 1])
        td = {str(q): R.tail_dependence(x[s], y[s], q) for q in (0.05, 0.01)}
        # what a Gaussian copula with the same correlation implies at the same levels
        g = {}
        for q in (0.05, 0.01):
            zq = stats.norm.ppf(q)
            g[str(q)] = float(stats.multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]]).cdf([zq, zq]) / q)
        rows.append({"a": a, "b": b, "rho": rho, "rho_bad": rho_bad, "rho_calm": rho_calm, "emp": td, "gauss": g,
                     "t4": R.t_copula_lambda(rho, 4.0)})
    # the average pairwise correlation of all 49 industries, by market state
    Z = X[ok]
    C_all = np.corrcoef(Z.T)
    C_bad = np.corrcoef(Z[bad[ok]].T)
    iu = np.triu_indices(Z.shape[1], 1)
    return _json({"pairs": rows, "avg_all": float(np.nanmean(C_all[iu])), "avg_bad": float(np.nanmean(C_bad[iu])),
                  "n_days": int(ok.sum())})


def compute_stress() -> dict:
    d, r, k = _mkt()
    F = np.column_stack([k["mkt_rf"], k["smb"], k["hml"]])
    w = np.array([1.0, 0.5, 0.5])            # a $100m market position with half as much in each of SMB and HML
    s = d >= 19900101
    S = np.cov(F[s].T)
    scen = []
    for name, day in (("19 Oct 1987", 19871019), ("15 Oct 2008", 20081015), ("16 Mar 2020", 20200316)):
        i = int(np.searchsorted(d, day))
        x = F[i]
        loss = -float(w @ x) * 100
        dist = float(math.sqrt(x @ np.linalg.solve(S, x)))
        scen.append({"name": name, "day": int(d[i]), "x": x, "loss_m": loss, "mahal": dist})
    rev = []
    for L in (5.0, 10.0, 20.0):
        o = R.reverse_stress(w, S, L / 100)
        rev.append({"loss_m": L, "x": o["x"], "distance": o["distance"]})
    sd = float(math.sqrt(w @ S @ w))
    return _json({"w": w, "scen": scen, "rev": rev, "sd_daily": sd})


def compute_ra() -> dict:
    rows = []
    for theta in (3.0, 2.0, 1.5):
        rows.append({"theta": theta, **R.worst_var_pareto(theta, 3, 0.99, N=1000)})
    return _json({"rows": rows, "d": 3, "alpha": 0.99})


def _features(r):
    sig = R.ewma_sigma(r)
    a1 = np.r_[np.nan, np.abs(r[:-1])]
    m5 = np.r_[[np.nan] * 5, np.convolve(np.abs(r), np.ones(5) / 5, "valid")[:-1]]
    m22 = np.r_[[np.nan] * 22, np.convolve(np.abs(r), np.ones(22) / 22, "valid")[:-1]]
    neg = np.r_[np.nan, np.minimum(r[:-1], 0)]
    return np.column_stack([sig, a1, m5, m22, neg])


def compute_learned() -> dict:
    d, r, _ = _mkt()
    tau = 0.01
    split = int(np.searchsorted(d, 19910101))
    cv = R.caviar_fit(r[:split], tau)
    q_cav = R.caviar_path(r, cv["beta"], float(np.quantile(r[:250], tau)))
    X = _features(r)
    ok = np.isfinite(X).all(1)
    tr = np.arange(len(r)) < split
    pred = R.quantile_mlp(X[ok & tr], r[ok & tr], tau, hidden=16, epochs=40, seed=1)
    q_mlp = np.full(len(r), np.nan)
    q_mlp[ok] = pred(X[ok])
    f = R.rolling_forecasts(r, 0.99, refit=1250, methods=("gjr_fhs", "hs"))
    test = np.arange(len(r)) >= split
    out = {"split": int(d[split]), "beta": cv["beta"], "models": {}}
    for name, q in (("caviar", q_cav), ("network", q_mlp), ("gjr_fhs", -f["gjr_fhs"]["var"]), ("hs", -f["hs"]["var"])):
        s = test & np.isfinite(q)
        I = (r[s] < q[s]).astype(int)
        ku = R.kupiec(I, tau)
        ch = R.christoffersen(I, tau)
        out["models"][name] = {"pinball": float(np.mean(R.pinball(q[s], r[s], tau))) * 1e4, "rate": ku["rate"],
                               "kupiec_p": ku["p_value"], "ind_p": ch["p_ind"]}
    s = (d >= 20080101) & (d <= 20091231)
    out["y2008"] = {"d": d[s], "r": r[s], "caviar": q_cav[s], "network": q_mlp[s], "gjr": -f["gjr_fhs"]["var"][s]}
    # Diebold-Mariano: the network against GJR-FHS, on the pinball loss
    from explainer.quant.house import vol as V
    s = test & np.isfinite(q_mlp) & np.isfinite(f["gjr_fhs"]["var"])
    la = R.pinball(q_mlp[s], r[s], tau)
    lb = R.pinball(-f["gjr_fhs"]["var"][s], r[s], tau)
    lc = R.pinball(q_cav[s], r[s], tau)
    out["dm_net_vs_gjr"] = V.diebold_mariano(la, lb, lags=5)
    out["dm_cav_vs_gjr"] = V.diebold_mariano(lc, lb, lags=5)
    return _json(out)


def compute_liq() -> dict:
    d, r, _ = _mkt()
    s = d >= 20100101
    v, e = R.var_es_hist(r[s], 0.99)
    pos = 100.0                                  # $m
    spread_mu, spread_sd = 0.0010, 0.0005        # an illustrative 10 bp spread with a 5 bp standard deviation
    lvar = pos * (v + 0.5 * (spread_mu + 2.33 * spread_sd))
    # FRTB: 97.5% ES over a 10-day base, scaled by sqrt(LH/10) per liquidity horizon bucket
    e975 = R.var_es_hist(r[s], 0.975)[1] * math.sqrt(10)
    hz = [(10, "large-cap equity, major currencies and rates"), (20, "small-cap equity, other currencies"),
          (40, "sovereign credit, large-cap equity volatility"), (60, "corporate credit, small-cap volatility"),
          (120, "other credit spreads and the rest")]
    return _json({"var1": v, "es1": e, "pos": pos, "lvar": lvar, "var_m": pos * v, "spread_mu": spread_mu,
                  "spread_sd": spread_sd, "es975_10d": e975,
                  "horizons": [{"lh": lh, "what": w_, "es": e975 * math.sqrt(lh / 10) * pos} for lh, w_ in hz]})


def compute_research() -> dict:
    # 1. level sets: two distributions with the same VaR (or ES) and their mixture
    mixV = R.mixture_var_es([0.0, 2.0], [0.995, 0.005], [0.0, 2.0, 5.0], [0.991, 0.004, 0.005], 0.5, 0.99)
    mixE = R.mixture_var_es([1.0], [1.0], [0.0, 2.0], [0.95, 0.05], 0.5, 0.9)
    # 2. the FZ0 expected score on a grid, for a Student-t(4) return scaled to 1% daily volatility
    nu = 4.0
    sc = 0.01 / math.sqrt(nu / (nu - 2))
    tau = 0.025
    rng = np.random.default_rng(4040)
    y = stats.t.rvs(nu, scale=sc, size=400_000, random_state=rng)
    v_true = float(stats.t.ppf(tau, nu) * sc)
    q = stats.t.ppf(tau, nu)
    e_true = float(-sc * (nu + q ** 2) / (nu - 1) * stats.t.pdf(q, nu) / tau)
    vs = v_true * np.linspace(0.6, 1.4, 41)
    es = e_true * np.linspace(0.6, 1.4, 41)
    G = np.array([[float(np.mean(R.fz0(vv, ee, y, tau))) if ee < vv else np.nan for vv in vs] for ee in es])
    i, j = np.unravel_index(np.nanargmin(G), G.shape)
    # 3. forecasters ranked by FZ0 at 97.5%, 1931-2020
    d, r, _ = _mkt()
    f = R.rolling_forecasts(r, 0.975, refit=1250)
    s = np.ones(len(r), bool)
    for m in f:
        s &= np.isfinite(f[m]["var"])
    rank = []
    for m, v in f.items():
        L = R.fz0(-v["var"][s], -v["es"][s], r[s], tau)
        I = R.hits(r[s], v["var"][s])
        rank.append({"method": m, "fz0": float(np.mean(L)), "rate": float(I.mean()),
                     "z2": R.acerbi_szekely_z2(r[s], v["var"][s], v["es"][s], 0.975)})
    rank.sort(key=lambda x: x["fz0"])
    from explainer.quant.house import vol as V
    best = rank[0]["method"]
    dm = {}
    for m in f:
        if m == best:
            continue
        la = R.fz0(-f[m]["var"][s], -f[m]["es"][s], r[s], tau)
        lb = R.fz0(-f[best]["var"][s], -f[best]["es"][s], r[s], tau)
        dm[m] = V.diebold_mariano(la, lb, lags=5)
    # 4. power when only the tail beyond VaR is wrong: true t(3), forecast a normal with the same 99% VaR
    nu3 = 3.0
    s3 = 1.0 / math.sqrt(nu3 / (nu3 - 2))
    var_true = -stats.t.ppf(0.01, nu3) * s3
    sd_n = var_true / stats.norm.ppf(0.99)
    v_n, e_n = R.var_es_normal(0.0, sd_n, 0.99)
    q3 = stats.t.ppf(0.01, nu3)
    e_true3 = s3 * (nu3 + q3 ** 2) / (nu3 - 1) * stats.t.pdf(q3, nu3) / 0.01
    rej_k, rej_z = 0, 0
    reps, T = 2000, 1000
    rng = np.random.default_rng(7)
    # the 5% critical value of Z2 for T days, simulated under the null (a correct normal forecast)
    z0 = [R.acerbi_szekely_z2(rng.standard_normal(T) * sd_n, np.full(T, v_n), np.full(T, e_n)) for _ in range(4000)]
    crit = float(np.quantile(z0, 0.95))
    for _ in range(reps):
        x = stats.t.rvs(nu3, scale=s3, size=T, random_state=rng)
        I = (-x > v_n).astype(int)
        if R.kupiec(I, 0.01)["p_value"] < 0.05:
            rej_k += 1
        z2 = R.acerbi_szekely_z2(x, np.full(T, v_n), np.full(T, e_n))
        if z2 > crit:
            rej_z += 1
    return _json({"mixV": mixV, "mixE": mixE, "fz": {"vs": vs, "es": es, "G": G, "v_true": v_true, "e_true": e_true,
                                                     "v_hat": float(vs[j]), "e_hat": float(es[i]), "tau": tau},
                  "rank": rank, "dm": dm, "best": best,
                  "power": {"var": v_n, "es_normal": e_n, "es_true": e_true3, "kupiec": rej_k / reps, "z2": rej_z / reps,
                            "T": T, "crit": crit}})


def compute_options() -> dict:
    """A delta-hedged short straddle (100 calls and 100 puts at the money, one month, 20% vol, spot 100, hedged):
    one-day 99% VaR by delta-normal, delta-gamma Monte Carlo and full revaluation."""
    from explainer.quant.house import bs
    S, K, T, sig = 100.0, 100.0, 21 / 252, 0.20
    n_opt = 1000.0
    g_c, g_p = bs.greeks(S, K, T, sig, cp=1), bs.greeks(S, K, T, sig, cp=-1)
    delta = -n_opt * (float(g_c["delta"]) + float(g_p["delta"]))
    gamma = -n_opt * (float(g_c["gamma"]) + float(g_p["gamma"]))
    hedge = -delta                                   # shares held to flatten the delta
    v0 = -n_opt * (float(bs.price(S, K, T, sig, cp=1)) + float(bs.price(S, K, T, sig, cp=-1)))
    rng = np.random.default_rng(1)
    sd = sig / math.sqrt(252)
    z = rng.standard_normal(200_000)
    S1 = S * np.exp(sd * z - 0.5 * sd ** 2)
    T1 = T - 1 / 252
    v1 = -n_opt * (bs.price(S1, K, T1, sig, cp=1) + bs.price(S1, K, T1, sig, cp=-1))
    pnl_full = (v1 - v0) + hedge * (S1 - S)
    dS = S1 - S
    pnl_dg = (delta + hedge) * dS + 0.5 * gamma * dS ** 2
    dn = abs(delta + hedge) * S * sd * stats.norm.ppf(0.99)
    full = R.var_es_hist(pnl_full, 0.99)
    dg = R.var_es_hist(pnl_dg, 0.99)
    # with a volatility shock: implied vol up 5 points with the 1% worst spot moves
    v1s = -n_opt * (bs.price(S1, K, T1, sig + 0.05, cp=1) + bs.price(S1, K, T1, sig + 0.05, cp=-1))
    pnl_vs = (v1s - v0) + hedge * (S1 - S)
    return _json({"delta_normal": dn, "delta_gamma": dg, "full": full, "vol_shock": R.var_es_hist(pnl_vs, 0.99),
                  "gamma": gamma, "premium": -v0, "n": n_opt})


def compute_extra() -> dict:
    """The GPD shape across thresholds; a portfolio's VaR under Gaussian and t copulas with the same marginals; Euler
    contributions to ES for the three-factor portfolio."""
    d, r, k = _mkt()
    L = -r
    sweep = []
    for q in (0.90, 0.925, 0.95, 0.975, 0.99):
        u = float(np.quantile(L, q))
        xi, beta = R.gpd_fit(L[L > u] - u)
        sweep.append({"q": q, "u": u, "xi": xi, "n_u": int((L > u).sum())})
    rng = np.random.default_rng(40)
    n, rho, nu_m = 400_000, 0.8, 3.0
    C = np.linalg.cholesky([[1, rho], [rho, 1]])
    Z = rng.standard_normal((n, 2)) @ C.T
    W = np.sqrt(4.0 / rng.chisquare(4.0, n))[:, None]
    U_g = stats.norm.cdf(Z)
    U_t = stats.t.cdf(Z * W, 4.0)
    marg = lambda U: stats.t.ppf(U, nu_m) * 0.01 / math.sqrt(nu_m / (nu_m - 2))  # noqa: E731
    out_c = {}
    for nm, U in (("gauss", U_g), ("t4", U_t)):
        X = marg(U)
        out_c[nm] = {"var": R.var_es_hist(X.sum(1), 0.99), "var999": R.var_es_hist(X.sum(1), 0.999)}
    F = np.column_stack([k["mkt_rf"], k["smb"], k["hml"]])[d >= 19900101]
    w = np.array([1.0, 0.5, 0.5])
    P = F @ w
    v, e = R.var_es_hist(P, 0.975)
    tail = -P >= v
    contrib = (-(F[tail] * w).mean(0))
    # the worst ten-day windows, non-overlapping
    r10 = np.convolve(r, np.ones(10), "valid")
    order = np.argsort(r10)
    worst10, used = [], []
    for i in order:
        if all(abs(i - j) > 30 for j in used):
            used.append(int(i))
            worst10.append({"start": int(d[i]), "end": int(d[i + 9]), "ret": float(r10[i])})
        if len(worst10) == 5:
            break
    one_day = R.var_es_hist(r, 0.99)[0]
    # other tails: Bitcoin (2017-2020) and the US market's own left and right tails
    b = data.binance_daily("BTCUSDT", "2017-08", "2020-12")
    rb = np.diff(np.log(np.asarray(b["close"], float)))
    tails = {}
    for nm, x in (("us_left", -r), ("us_right", r), ("btc_left", -rb), ("btc_right", rb)):
        u = float(np.quantile(x, 0.95))
        xi, _ = R.gpd_fit(x[x > u] - u)
        tails[nm] = {"xi": xi, "n": int(len(x)), "hill100": float(R.hill_series(x, [min(100, len(x) // 20)])[0])}
    return _json({"tails": tails, "worst10": worst10, "var1": one_day, "sweep": sweep, "copula": out_c, "rho": rho, "euler": {"es": e, "contrib": contrib,
                                                                         "share": contrib / contrib.sum(),
                                                                         "sd_share": (w * (np.cov(F.T) @ w)) / (w @ np.cov(F.T) @ w)}})


ITEMS = {"var3": compute_var3, "sqrt": compute_sqrt, "coherent": compute_coherent, "backtest": compute_backtest,
         "evt": compute_evt, "depend": compute_depend, "stress": compute_stress, "ra": compute_ra,
         "learned": compute_learned, "liq": compute_liq, "research": compute_research, "options": compute_options,
         "extra": compute_extra}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
