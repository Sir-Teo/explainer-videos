"""Every number in Part 6 (Financial Econometrics), computed and cached in .cache/quant6/.

    python -m videos.quant.quant6.compute [items] [--force]

Research window: to December 2020.  Items (seeded; seconds to a few minutes):

* ``overlap``   five-year returns on the dividend yield (Shiller, monthly, overlapping): naive, Newey-West and
                Hansen-Hodrick t-statistics; and their false-rejection rates when the truth is zero (simulation);
* ``stambaugh`` the bias of predictive regressions: simulated slopes for a persistent predictor, and the annual
                dividend-yield regression 1871-2020 with Stambaugh's correction;
* ``gmm``       the consumption Euler equation (Hansen and Singleton 1982) by two-step GMM: real PCE per capita
                (FRED), the market and the T-bill (French), quarterly 1947-2020; the J test;
* ``event``     an event study of the turn of the month (Ariel 1987; Lakonishok and Smidt 1988) on daily US returns,
                before and after publication;
* ``panel``     industry momentum on French's 49 industries: pooled OLS, clustered (by month; two-way) and
                Fama-MacBeth standard errors (Petersen 2009);
* ``bootstrap`` the US market's Sharpe ratio, monthly 1926-2020: iid, Lo, block and stationary bootstrap errors;
* ``shrinkage`` 49 industry means estimated on 1927-1973, raw and shrunk, scored on 1974-2020;
* ``multiple``  the 49 industries' CAPM alphas: how many survive Bonferroni, Holm and Benjamini-Hochberg;
* ``ellipse``   the confidence ellipse of (alpha, beta) for tobacco stocks over 5, 20 and 60 years;
* ``dml``       double machine learning on a planted effect, against naive OLS;
* ``snr``       years to significance and the chance a good strategy looks bad;
* ``envelope``  seals the hold-outs this part reads and registers its tests.
"""

from __future__ import annotations

import inspect

import numpy as np
from scipy import stats as sst

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import econ, pit

CACHE = Cache("quant6")
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


def _shiller_monthly():
    s = data.shiller()
    t = s["t"]
    cpi = s["cpi"]
    P = s["price"] * cpi[-1] / cpi
    D = s["div"] * cpi[-1] / cpi
    ok = np.isfinite(P) & np.isfinite(D)
    return t[ok], P[ok], D[ok]


# ---------------------------------------------------------------------------
def compute_overlap() -> dict:
    t, P, D = _shiller_monthly()
    lr = np.log((P[1:] + D[:-1] / 12) / P[:-1])  # monthly real log total return
    dy = np.log(D / P)[:-1]
    h = 60
    fwd = np.convolve(lr, np.ones(h), "valid")[1:]  # return over months t+1 .. t+h
    x = dy[: len(fwd)]
    out = {}
    for se, lags in (("naive", 0), ("nw", 2 * h), ("hh", h - 1)):
        r = econ.ols(fwd, x, se=se, lags=lags)
        out[se] = {"beta": float(r["beta"][1]), "t": float(r["t"][1]), "r2": r["r2"]}
    # size under the null: iid normal returns, AR(1) predictor with rho = 0.99 monthly, independent
    rng = np.random.default_rng(6)
    n_sim, T = 400, 1200
    rej = {"naive": 0, "nw": 0, "hh": 0}
    for _ in range(n_sim):
        e = rng.standard_normal(T + h)
        z = np.empty(T + h)
        z[0] = 0
        v = rng.standard_normal(T + h)
        for k in range(1, T + h):
            z[k] = 0.99 * z[k - 1] + v[k]
        f = np.convolve(e, np.ones(h), "valid")[1:T + 1]
        for se, lags in (("naive", 0), ("nw", 2 * h), ("hh", h - 1)):
            if abs(econ.ols(f, z[:T], se=se, lags=lags)["t"][1]) > 1.96:
                rej[se] += 1
    return _json({"est": out, "n": int(len(fwd)), "h": h, "size": {k: v / n_sim for k, v in rej.items()},
                  "t": t[: len(fwd)], "fwd": fwd, "dy": x})


# ---------------------------------------------------------------------------
def compute_stambaugh() -> dict:
    s = data.shiller()
    t, P, D = s["t"], s["price"], s["div"]
    jan = np.isclose(t % 1, 0) & np.isfinite(P) & np.isfinite(D)
    ty, Py, Dy = t[jan], P[jan], D[jan]
    r = np.log((Py[1:] + Dy[:-1]) / Py[:-1])  # annual nominal log return (dividends over the year as reported)
    x = np.log(Dy / Py)
    reg = econ.ols(r, x[:-1])
    ar = econ.ols(x[1:], x[:-1])
    rho = float(ar["beta"][1])
    u, v = reg["resid"], ar["resid"]
    cov_uv, var_v = float(np.cov(u, v)[0, 1]), float(np.var(v, ddof=1))
    T = len(r)
    bias = econ.stambaugh_bias(rho, cov_uv, var_v, T)
    corr = cov_uv / np.sqrt(np.var(u, ddof=1) * var_v)
    sims = {}
    for TT in (50, 150):
        sims[str(TT)] = econ.simulate_predictive(TT, 0.92, -0.75, n=4000, seed=TT,
                                                 sd_u=float(np.std(u)), sd_v=float(np.std(v)))
    return _json({"beta": float(reg["beta"][1]), "t": float(reg["t"][1]), "rho": rho, "corr_uv": float(corr), "T": T,
                  "bias": bias, "beta_corrected": float(reg["beta"][1] - bias), "sims": sims,
                  "sim_rho": 0.92, "sim_corr": -0.75, "sd_u": float(np.std(u)), "sd_v": float(np.std(v))})


# ---------------------------------------------------------------------------
def compute_gmm() -> dict:
    c = data.fred("A794RX0Q048SBEA", start="1947-01-01")
    cpi = data.fred("CPIAUCSL", start="1947-01-01")
    ff = data.ken_french_factors_monthly()
    cd, cv = c["date"], c["value"]
    m = (cd >= 19470101) & (cd <= 20201001)
    cd, cv = cd[m], cv[m]
    q = (cd // 10000) * 10 + ((cd // 100) % 100 - 1) // 3 + 1  # YYYYQ
    g = cv[1:] / cv[:-1]  # gross real consumption growth, quarter to quarter
    qy = q[1:]
    # quarterly gross nominal returns from monthly, and CPI inflation over the same quarters
    fd = ff["date"]
    fq = (fd // 100) * 10 + ((fd % 100) - 1) // 3 + 1
    mk = ff["mkt_rf"] + ff["rf"]
    Rm = {k: float(np.prod(1 + mk[fq == k])) for k in np.unique(fq)}
    Rf = {k: float(np.prod(1 + ff["rf"][fq == k])) for k in np.unique(fq)}
    pd_, pv = cpi["date"], cpi["value"]
    pq = (pd_ // 10000) * 10 + ((pd_ // 100) % 100 - 1) // 3 + 1
    P = {k: float(pv[pq == k].mean()) for k in np.unique(pq)}
    rows = []
    for i, k in enumerate(qy):
        prev = q[i]
        if k in Rm and k in P and prev in P:
            infl = P[k] / P[prev]
            rows.append((g[i], Rm[k] / infl, Rf[k] / infl))
    A = np.array(rows)
    G, RM, RF = A[:, 0], A[:, 1], A[:, 2]
    # instruments known at t: constant, lagged consumption growth, lagged market return
    Z = np.column_stack([np.ones(len(G) - 1), G[:-1], RM[:-1]])
    Gt, RMt, RFt = G[1:], RM[1:], RF[1:]

    def moments(th):
        beta, gam = th
        sdf = beta * Gt ** (-gam)
        e1 = sdf * RMt - 1
        e2 = sdf * RFt - 1
        return np.column_stack([e1[:, None] * Z, e2[:, None] * Z])

    res = econ.gmm(moments, [0.99, 2.0], lags=2)
    eq = float(np.mean(RMt - RFt))
    return _json({"beta": res["theta"][0], "gamma": res["theta"][1], "se": res["se"], "J": res["J"], "df": res["df"],
                  "p_J": res["p_J"], "n": res["n"], "sd_g": float(np.std(Gt - 1)), "mean_g": float(np.mean(Gt - 1)),
                  "equity_premium_q": eq, "corr_g_rm": float(np.corrcoef(Gt, RMt)[0, 1]),
                  "hj_gamma": float(eq / np.cov(Gt - 1, RMt - RFt)[0, 1])})


# ---------------------------------------------------------------------------
def compute_event() -> dict:
    kf = data.ken_french_daily()
    d, r = pit.research(kf["date"], kf["mkt"])
    ym = d // 100
    # position of each day relative to the month's last trading day: -1 is the last day, +1 the first of the next month
    pos = np.full(len(d), 99)
    starts = np.flatnonzero(np.diff(ym)) + 1  # first trading day of each new month
    for s0 in starts:
        for k in range(-5, 5):
            j = s0 + k
            if 0 <= j < len(d):
                pos[j] = k if k < 0 else k + 1
    window = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
    out = {}
    for name, m in (("1926-1986", d < 19870101), ("1987-2020", d >= 19870101)):
        base = r[m & (pos == 99)].mean()
        ar = []
        for k in window:
            x = r[m & (pos == k)] - base
            ar.append({"k": k, "ar": float(x.mean()), "se": float(x.std(ddof=1) / np.sqrt(len(x)))})
        tom = r[m & np.isin(pos, [-1, 1, 2, 3])]
        rest = r[m & ~np.isin(pos, [-1, 1, 2, 3])]
        tt = sst.ttest_ind(tom, rest, equal_var=False)
        out[name] = {"ar": ar, "base": float(base), "tom_mean": float(tom.mean()), "rest_mean": float(rest.mean()),
                     "t": float(tt.statistic), "share_of_return": float(tom.sum() / r[m].sum()),
                     "days_share": float(len(tom) / m.sum())}
    return _json(out)


# ---------------------------------------------------------------------------
def compute_panel() -> dict:
    ind = data.ken_french_industries(49)
    R = ind["returns"]
    dates = ind["date"]
    T, N = R.shape
    past = np.full_like(R, np.nan)
    for t in range(12, T):
        past[t] = np.prod(1 + R[t - 12:t - 1], axis=0) - 1  # months t-12 .. t-2 (skip the most recent)
    keep = dates >= 192801
    Y, X = R[keep], past[keep]
    y, x = Y.ravel(), X.ravel()
    month = np.repeat(np.arange(Y.shape[0]), N)
    firm = np.tile(np.arange(N), Y.shape[0])
    ok = np.isfinite(y) & np.isfinite(x)
    out = {}
    for name, kw in (("pooled OLS", {"se": "naive"}), ("clustered by industry", {"se": "cluster", "groups": firm[ok]}),
                     ("clustered by month", {"se": "cluster", "groups": month[ok]}),
                     ("two-way clustered", {"se": "cluster2", "groups": month[ok], "groups2": firm[ok]})):
        r = econ.ols(y[ok], x[ok], **kw)
        out[name] = {"beta": float(r["beta"][1]), "se": float(r["se"][1]), "t": float(r["t"][1])}
    fm = econ.fama_macbeth(Y, X)
    out["Fama-MacBeth"] = {"beta": float(fm["beta"][1]), "se": float(fm["se"][1]), "t": float(fm["t"][1])}
    return _json({"results": out, "n_obs": int(ok.sum()), "months": int(Y.shape[0]), "industries": N})


# ---------------------------------------------------------------------------
def compute_bootstrap() -> dict:
    ff = data.ken_french_factors_monthly()
    x = ff["mkt_rf"]
    sr = lambda z: z.mean() / z.std(ddof=1)  # noqa: E731
    s = float(sr(x))
    n = len(x)
    iid = econ.sharpe_se(s, n)
    skew, kurt = float(sst.skew(x)), float(sst.kurtosis(x, fisher=False))
    mert = econ.sharpe_se(s, n, skew, kurt)
    mb = econ.moving_block_bootstrap(x, sr, block=12, B=2000, seed=1)
    stb = econ.stationary_bootstrap(x, sr, mean_block=12, B=800, seed=2)
    iidb = econ.moving_block_bootstrap(x, sr, block=1, B=2000, seed=3)
    ann = np.sqrt(12)
    return _json({"sr_m": s, "sr_a": s * ann, "n": n, "se_iid": iid * ann, "se_mertens": mert * ann,
                  "se_iid_boot": float(iidb.std()) * ann, "se_block": float(mb.std()) * ann,
                  "se_stationary": float(stb.std()) * ann, "skew": skew, "kurt": kurt,
                  "boot_block": mb * ann})


# ---------------------------------------------------------------------------
def compute_shrinkage() -> dict:
    ind = data.ken_french_industries(49)
    ff = data.ken_french_factors_monthly()
    assert np.array_equal(ind["date"], ff["date"])
    ex = ind["returns"] - ff["rf"][:, None]
    d = ind["date"]
    a = (d >= 192701) & (d <= 197312)
    b = d >= 197401
    full = np.all(np.isfinite(ex[a | b]), axis=0)
    m1 = np.nanmean(ex[a][:, full], axis=0) * 12
    s1 = np.nanstd(ex[a][:, full], axis=0, ddof=1) * np.sqrt(12) / np.sqrt(a.sum() / 12)
    m2 = np.nanmean(ex[b][:, full], axis=0) * 12
    sh = econ.shrink_means(m1, s1)
    mse_raw = float(np.mean((m1 - m2) ** 2))
    mse_sh = float(np.mean((sh["shrunk"] - m2) ** 2))
    mse_grand = float(np.mean((sh["grand"] - m2) ** 2))
    names = [c for c, f in zip(ind["columns"], full) if f]
    return _json({"names": names, "raw": m1, "shrunk": sh["shrunk"], "later": m2, "grand": sh["grand"], "tau": sh["tau"],
                  "B_mean": float(np.mean(sh["B"])), "mse_raw": mse_raw, "mse_shrunk": mse_sh, "mse_grand": mse_grand,
                  "n": int(full.sum())})


# ---------------------------------------------------------------------------
def compute_multiple() -> dict:
    ind = data.ken_french_industries(49)
    ff = data.ken_french_factors_monthly()
    ex = ind["returns"] - ff["rf"][:, None]
    mk = ff["mkt_rf"]
    alphas, ts, ps = [], [], []
    for j in range(ex.shape[1]):
        r = econ.ols(ex[:, j], mk, se="nw", lags=6)
        alphas.append(float(r["beta"][0] * 12))
        ts.append(float(r["t"][0]))
        ps.append(float(2 * sst.norm.sf(abs(r["t"][0]))))
    ps = np.array(ps)
    # 1,000 strategies that are pure noise (true alpha zero) for comparison
    rng = np.random.default_rng(8)
    noise_p = 2 * sst.norm.sf(np.abs(rng.standard_normal(1000)))
    return _json({"names": ind["columns"], "alpha": alphas, "t": ts, "p": ps,
                  "n_raw": int((ps < 0.05).sum()), "n_bonf": int(econ.bonferroni(ps).sum()),
                  "n_holm": int(econ.holm(ps).sum()), "n_bh": int(econ.benjamini_hochberg(ps).sum()),
                  "noise_raw": int((noise_p < 0.05).sum()), "noise_bh": int(econ.benjamini_hochberg(noise_p).sum()),
                  "noise_bonf": int(econ.bonferroni(noise_p).sum())})


# ---------------------------------------------------------------------------
def compute_ellipse() -> dict:
    ind = data.ken_french_industries(49)
    ff = data.ken_french_factors_monthly()
    j = ind["columns"].index("Smoke")
    ex = ind["returns"][:, j] - ff["rf"]
    out = {}
    for yrs in (5, 20, 60):
        m = ind["date"] >= (2021 - yrs) * 100 + 1
        r = econ.ols(ex[m], ff["mkt_rf"][m])
        V = r["V"].copy()
        V[0, :] *= 12
        V[:, 0] *= 12
        out[str(yrs)] = {"alpha": float(r["beta"][0] * 12), "beta": float(r["beta"][1]), "V": V}
    return _json(out)


# ---------------------------------------------------------------------------
def compute_dml() -> dict:
    rng = np.random.default_rng(12)
    n = 4000
    X = rng.uniform(-2, 2, (n, 3))
    m = np.sin(2 * X[:, 0]) + 0.5 * X[:, 1] ** 2
    g = 2 * np.sin(2 * X[:, 0]) + X[:, 1] ** 2 + 0.5 * X[:, 2]
    reps = []
    for k in range(60):
        r2 = np.random.default_rng(100 + k)
        d = m + r2.standard_normal(n)
        y = 0.3 * d + g + r2.standard_normal(n)
        res = econ.dml_plr(y, d, X, seed=k)
        reps.append((res["theta"], res["naive"]))
    reps = np.array(reps)
    return _json({"theta_true": 0.3, "dml": reps[:, 0], "naive": reps[:, 1], "dml_mean": float(reps[:, 0].mean()),
                  "naive_mean": float(reps[:, 1].mean()), "dml_sd": float(reps[:, 0].std())})


# ---------------------------------------------------------------------------
def compute_snr() -> dict:
    srs = np.linspace(0.2, 2.0, 91)
    yrs = [econ.years_to_significance(s) for s in srs]
    T = np.linspace(0.5, 30, 120)
    p_neg = {str(s): sst.norm.cdf(-s * np.sqrt(T)).tolist() for s in (0.25, 0.5, 1.0)}
    se_desk = econ.sharpe_se(1.0, 4)  # annual units, four years, Gaussian
    return _json({"sr": srs, "years": yrs, "T": T, "p_neg": p_neg, "se_desk": se_desk,
                  "y05": econ.years_to_significance(0.5), "y1": econ.years_to_significance(1.0)})


# ---------------------------------------------------------------------------
def compute_envelope() -> dict:
    recs = {}
    ind = data.ken_french_industries(49, through="2025-12")
    recs["French 49 industries"] = pit.seal("kenfrench/industries49", ind["date"] * 100 + 1, ind["returns"])
    ff = data.ken_french_factors_monthly(through="2025-12")
    recs["French factors, monthly"] = pit.seal("kenfrench/ff3_monthly", ff["date"] * 100 + 1,
                                               np.column_stack([ff["mkt_rf"], ff["smb"], ff["hml"], ff["rf"]]))
    c = data.fred("A794RX0Q048SBEA", start="1947-01-01")
    recs["Real PCE per capita (FRED)"] = pit.seal("fred/A794RX0Q048SBEA", c["date"], c["value"])
    reg = {"industry_momentum_panel": pit.register("industry_momentum_panel", inspect.getsource(compute_panel),
                                                   {"signal": "12-2 month industry return"}, trials=1),
           "turn_of_month_event": pit.register("turn_of_month_event", inspect.getsource(compute_event),
                                               {"window": "[-1, +3]"}, trials=1),
           "industry_capm_alphas": pit.register("industry_capm_alphas", inspect.getsource(compute_multiple),
                                                {"n": 49}, trials=49)}
    return _json({"sealed": recs, "registered": reg, "trials": pit.trials_so_far()})


ITEMS = {"overlap": compute_overlap, "stambaugh": compute_stambaugh, "gmm": compute_gmm, "event": compute_event,
         "panel": compute_panel, "bootstrap": compute_bootstrap, "shrinkage": compute_shrinkage,
         "multiple": compute_multiple, "ellipse": compute_ellipse, "dml": compute_dml, "snr": compute_snr,
         "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
