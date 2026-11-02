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
                                                {"n": 49}, trials=49),
           "fomc_announcement_days": pit.register("fomc_announcement_days", inspect.getsource(compute_fomc),
                                                  {"days": "scheduled FOMC decisions 1994-2020"}, trials=1),
           "shiller_oos_predictors": pit.register("shiller_oos_predictors", inspect.getsource(compute_oos),
                                                  {"predictors": 5, "oos_from": 1927}, trials=5),
           "lookahead_rotation_toy": pit.register("lookahead_rotation_toy", inspect.getsource(compute_lookahead),
                                                  {"rule": "4-week size-decile rotation"}, trials=1),
           "capm_two_pass": pit.register("capm_two_pass", inspect.getsource(compute_twopass),
                                         {"portfolios": "49 industries + 10 B/M deciles", "from": 196307}, trials=1)}
    return _json({"sealed": recs, "registered": reg, "trials": pit.trials_so_far()})


# ===========================================================================
# The expansion (November 2026): items for chapters 1-18
# ===========================================================================
def _shiller_lr_dy():
    """Monthly real log total return lr[t] (month t to t+1) and log dividend yield dy[t], as in ``overlap``."""
    t, P, D = _shiller_monthly()
    lr = np.log((P[1:] + D[:-1] / 12) / P[:-1])
    dy = np.log(D / P)[:-1]
    return t[:-1], lr, dy


def _panel_arrays():
    ind = data.ken_french_industries(49)
    R = ind["returns"]
    dates = ind["date"]
    past = np.full_like(R, np.nan)
    for t in range(12, R.shape[0]):
        past[t] = np.prod(1 + R[t - 12:t - 1], axis=0) - 1
    keep = dates >= 192801
    return R[keep], past[keep], dates[keep], ind["columns"]


# ---------------------------------------------------------------------------
def compute_ols_fwl() -> dict:
    ind = data.ken_french_industries(49)
    ff = data.ken_french_factors_monthly()
    j = ind["columns"].index("Smoke")
    m = ind["date"] >= 192701
    y = (ind["returns"][:, j] - ff["rf"])[m]
    mk, smb = ff["mkt_rf"][m], ff["smb"][m]
    full = econ.ols(y, np.column_stack([mk, smb]))
    white = econ.ols(y, np.column_stack([mk, smb]), se="white")
    ry = econ.ols(y, mk)["resid"]
    rx = econ.ols(smb, mk)["resid"]
    b2 = float(rx @ ry / (rx @ rx))
    assert abs(b2 - full["beta"][2]) < 1e-10
    alone = econ.ols(y, smb)
    rng = np.random.default_rng(1)
    pick = np.sort(rng.choice(len(y), 360, replace=False))
    return _json({"beta": full["beta"], "se_naive": full["se"], "se_white": white["se"], "fwl": b2,
                  "gap": abs(b2 - float(full["beta"][2])), "alone": float(alone["beta"][1]), "n": int(len(y)),
                  "rx": rx[pick], "ry": ry[pick], "smb": smb[pick], "y": y[pick],
                  "corr_mk_smb": float(np.corrcoef(mk, smb)[0, 1])})


# ---------------------------------------------------------------------------
def compute_hac() -> dict:
    t, lr, dy = _shiller_lr_dy()
    h = 60
    fwd = np.convolve(lr, np.ones(h), "valid")[1:]
    x = dy[: len(fwd)]
    T = len(fwd)
    reg = econ.ols(fwd, x)
    xt = x - x.mean()
    z = xt * reg["resid"]
    g0 = z @ z / T
    acf = [1.0] + [float(z[k:] @ z[:-k] / T / g0) for k in range(1, 121)]
    Ls = list(range(0, 181, 3))
    tL = [float(econ.ols(fwd, x, se="nw", lags=L)["t"][1]) for L in Ls]
    sxx = xt @ xt / T
    beta = float(reg["beta"][1])
    nu = int(round(0.4 * T ** (2 / 3)))
    s_ewc = econ.lrv(z, "ewc", nu=nu)
    t_ewc = beta / np.sqrt(s_ewc / T) * sxx
    bw = 1.3 * np.sqrt(T)
    s_fb = econ.lrv(z, "bartlett", bw=bw)
    t_fb = beta / np.sqrt(s_fb / T) * sxx
    cv_fb = econ.fixed_b_cv(bw / T, T=500, reps=20000, seed=11)
    hod = econ.hodrick_se(lr[1:], dy[: len(lr) - 1], h)
    # periodogram of the scores at the lowest frequencies, and the cosine projections EWC averages
    tt = np.arange(1, T + 1)
    lam = [float(np.sqrt(2 / T) * (np.cos(np.pi * j * (tt - 0.5) / T) @ (z - z.mean()))) for j in range(1, 61)]
    # fixed-b critical values against b, by simulation
    bs = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5]
    cvs = [econ.fixed_b_cv(b, T=500, reps=20000, seed=20 + i) for i, b in enumerate(bs)]
    poly = [1.96 + 2.9694 * b + 0.416 * b ** 2 - 0.5324 * b ** 3 for b in bs]
    return _json({"T": T, "h": h, "beta": beta, "acf": acf, "L": Ls, "t_L": tL, "t_naive": tL[0],
                  "t_nw": float(econ.ols(fwd, x, se="nw", lags=2 * h)["t"][1]),
                  "t_hh": float(econ.ols(fwd, x, se="hh", lags=h - 1)["t"][1]),
                  "t_hodrick": float(hod["t"][1]), "beta_hodrick": float(hod["beta"][1]),
                  "t_ewc": float(t_ewc), "nu": nu, "cv_ewc": float(sst.t.ppf(0.975, nu)),
                  "t_fixedb": float(t_fb), "bw_fixedb": float(bw), "cv_fixedb": cv_fb, "lam": lam,
                  "b_grid": bs, "cv_grid": cvs, "cv_poly": poly, "g0": float(g0)})


# ---------------------------------------------------------------------------
def compute_har_size() -> dict:
    """Null rejection rates of five t-tests for a predictive regression of h-period overlapping returns on an AR(1)
    predictor, T = 600, 3,000 worlds per cell."""
    T, reps = 600, 3000
    L_rot = int(np.floor(0.75 * T ** (1 / 3)))
    bw_fb = 1.3 * np.sqrt(T)
    cv_fb = econ.fixed_b_cv(bw_fb / T, T=T, reps=20000, seed=31)
    nu = int(round(0.4 * T ** (2 / 3)))
    cv_ewc = float(sst.t.ppf(0.975, nu))
    tt = np.arange(1, T + 1)
    C = np.array([np.sqrt(2 / T) * np.cos(np.pi * j * (tt - 0.5) / T) for j in range(1, nu + 1)])
    nfft = 1 << int(np.ceil(np.log2(2 * T)))
    k = np.arange(1, T)

    def bart(ac, bw):
        w = np.clip(1 - k / bw, 0, None)
        return ac[:, 0] + 2 * ac[:, 1:] @ w

    part = CACHE.partial("har_size", {"T": T, "reps": reps, "v": 1})
    out = {}
    for rho in (0.0, 0.9, 0.95, 0.99):
        for h in (1, 12, 60):
            key = f"{rho}|{h}"
            if key not in part:
                rng = np.random.default_rng(int(1000 * rho) + h)
                rej = np.zeros(5)
                for s in range(0, reps, 500):
                    n = min(500, reps - s)
                    v = rng.standard_normal((n, T + 200))
                    x = np.zeros_like(v)
                    for t in range(1, T + 200):
                        x[:, t] = rho * x[:, t - 1] + v[:, t]
                    x = x[:, 200:]
                    e = rng.standard_normal((n, T + h))
                    cs = np.cumsum(e, axis=1)
                    y = cs[:, h:] - cs[:, :-h] if h > 1 else e[:, 1:T + 1]
                    y = y[:, :T]
                    xt = x - x.mean(1, keepdims=True)
                    yt = y - y.mean(1, keepdims=True)
                    sxx = (xt * xt).sum(1)
                    b = (xt * yt).sum(1) / sxx
                    u = yt - b[:, None] * xt
                    z = xt * u
                    F = np.fft.rfft(z, nfft, axis=1)
                    ac = np.fft.irfft(F * np.conj(F), nfft, axis=1)[:, :T] / T
                    se = lambda S: np.sqrt(S * T) / sxx  # noqa: E731
                    s_naive = np.sqrt((u * u).sum(1) / (T - 2) / sxx)
                    t_ = [b / s_naive, b / se(bart(ac, L_rot + 1)), b / se(bart(ac, max(h - 1, 0) + 1)),
                          b / se(bart(ac, bw_fb)), b / se(((z - z.mean(1, keepdims=True)) @ C.T) ** 2 @ np.ones(nu) / nu)]
                    cvs = [1.96, 1.96, 1.96, cv_fb, cv_ewc]
                    rej += [np.sum(np.abs(a) > c) for a, c in zip(t_, cvs)]
                part[key] = (rej / reps).tolist()
            out[key] = part[key]
    names = ["naive", f"NW, L = {L_rot}", "NW, L = h - 1", "NW, b fixed, cv", "EWC"]
    return _json({"T": T, "reps": reps, "names": names, "rate": out, "L_rot": L_rot, "bw_fb": bw_fb, "cv_fb": cv_fb,
                  "nu": nu, "cv_ewc": cv_ewc})


# ---------------------------------------------------------------------------
def compute_petersen() -> dict:
    """Petersen's (2009) simulation: 500 firms x 10 years, a firm effect and/or a time effect in both the regressor
    and the residual; each standard error's average against the true sampling spread of the slope."""
    F, Tn, reps = 500, 10, 1000
    designs = {"none": (0, 0, 0, 0), "firm 50%": (0.5, 0.5, 0, 0), "time 50%": (0, 0, 0.5, 0.5),
               "firm 25% + time 25%": (0.25, 0.25, 0.25, 0.25), "firm 75%": (0.75, 0.75, 0, 0)}
    firm = np.repeat(np.arange(F), Tn)
    year = np.tile(np.arange(Tn), F)
    checkpoints = [10, 20, 50, 100, 200, 500, 1000]
    out = {}
    for di, (name, (fx, fu, tx, tu)) in enumerate(designs.items()):
        rng = np.random.default_rng(900 + di)
        b_ols, b_fm, ses = [], [], {k: [] for k in ("OLS", "firm", "time", "two-way", "FM")}
        for _ in range(reps):
            def comp(f, t_):
                return (np.sqrt(f) * rng.standard_normal(F)[firm] + np.sqrt(t_) * rng.standard_normal(Tn)[year]
                        + np.sqrt(1 - f - t_) * rng.standard_normal(F * Tn))
            x = comp(fx, tx)
            u = 2 * comp(fu, tu)
            y = x + u
            X = np.column_stack([np.ones(F * Tn), x])
            XtXi = np.linalg.inv(X.T @ X)
            b = XtXi @ X.T @ y
            e = y - X @ b
            sc = X * e[:, None]

            def cl(g, G):
                s = np.column_stack([np.bincount(g, sc[:, 0], G), np.bincount(g, sc[:, 1], G)])
                return XtXi @ (s.T @ s) @ XtXi
            Vf, Vt = cl(firm, F), cl(year, Tn)
            Vw = XtXi @ (sc.T @ sc) @ XtXi
            ses["OLS"].append(np.sqrt((e @ e) / (F * Tn - 2) * XtXi[1, 1]))
            ses["firm"].append(np.sqrt(Vf[1, 1]))
            ses["time"].append(np.sqrt(Vt[1, 1]))
            ses["two-way"].append(np.sqrt(max(Vf[1, 1] + Vt[1, 1] - Vw[1, 1], 1e-12)))
            xs, ys = x.reshape(F, Tn), y.reshape(F, Tn)
            xc = xs - xs.mean(0)
            sl = (xc * (ys - ys.mean(0))).sum(0) / (xc * xc).sum(0)
            b_fm.append(sl.mean())
            ses["FM"].append(sl.std(ddof=1) / np.sqrt(Tn))
            b_ols.append(b[1])
        b_ols, b_fm = np.array(b_ols), np.array(b_fm)
        ratios = {}
        paths = {}
        for k, v in ses.items():
            v = np.array(v)
            ref = b_fm if k == "FM" else b_ols
            ratios[k] = float(v.mean() / ref.std(ddof=1))
            paths[k] = [float(v[:c].mean() / ref[:c].std(ddof=1)) for c in checkpoints]
        out[name] = {"ratio": ratios, "path": paths, "sd_ols": float(b_ols.std(ddof=1))}
    return _json({"designs": out, "order": list(designs), "checkpoints": checkpoints, "firms": F, "years": Tn,
                  "reps": reps})


# ---------------------------------------------------------------------------
def compute_panel_fe() -> dict:
    Y, X, dates, _ = _panel_arrays()
    T, N = Y.shape
    month = np.repeat(np.arange(T), N)
    y, x = Y.ravel(), X.ravel()
    ok = np.isfinite(y) & np.isfinite(x)
    wb = econ.within_between(y, x, month)
    mx = np.array([np.nanmean(np.where(np.isfinite(Y[t]) & np.isfinite(X[t]), X[t], np.nan)) for t in range(T)])
    my = np.array([np.nanmean(np.where(np.isfinite(Y[t]) & np.isfinite(X[t]), Y[t], np.nan)) for t in range(T)])
    yd, xd = y - my[month], x - mx[month]
    fe = econ.ols(yd[ok], xd[ok], const=False, se="cluster", groups=month[ok])
    fm = econ.fama_macbeth(Y, X)
    fm_nw = econ.fama_macbeth(Y, X, nw_lags=6)
    sl = fm["slopes"][:, 1]
    disp = np.array([np.nansum(np.where(np.isfinite(Y[t]), (X[t] - mx[t]) ** 2, np.nan)) for t in range(T)])
    w = disp / disp.sum()
    between = econ.ols(my, mx, se="nw", lags=6)
    # three months for the picture: a calm, a middling and a turbulent cross-section, with different means
    order = np.argsort(disp)
    picks = [int(order[int(0.2 * T)]), int(order[int(0.6 * T)]), int(order[int(0.97 * T)])]
    ex = []
    for t in picks:
        m = np.isfinite(Y[t]) & np.isfinite(X[t])
        ex.append({"date": int(dates[t]), "x": X[t][m], "y": Y[t][m], "slope": float(sl[t])})
    return _json({"within": wb["within"], "between": wb["between"], "pooled": wb["pooled"], "w_within": wb["w_within"],
                  "t_within_cluster": float(fe["t"][0]), "fm_weighted": float(np.sum(w * sl)),
                  "fm": float(sl.mean()), "fm_t": float(fm["t"][1]), "fm_t_nw": float(fm_nw["t"][1]),
                  "share_positive": float(np.mean(sl > 0)), "t_between_nw": float(between["t"][1]),
                  "slopes": sl, "weights": w, "dates": dates, "examples": ex, "mx": mx, "my": my, "T": int(T),
                  "Y": np.nan_to_num(Y, nan=-9.0), "X": np.nan_to_num(X, nan=-9.0)})


# ---------------------------------------------------------------------------
def compute_twopass() -> dict:
    ind = data.ken_french_industries(49)
    bm = data.ken_french_sorts("BE-ME")
    ff = data.ken_french_factors_monthly()
    assert np.array_equal(ind["date"], ff["date"]) and np.array_equal(bm["date"], ff["date"])
    m = (ff["date"] >= 196307) & (ff["date"] <= 202012)
    dec = [bm["columns"].index(c) for c in ["Lo 10", "2-Dec", "3-Dec", "4-Dec", "5-Dec", "6-Dec", "7-Dec", "8-Dec",
                                           "9-Dec", "Hi 10"]]
    R = np.column_stack([ind["returns"][m], bm["returns"][m][:, dec]]) - ff["rf"][m][:, None]
    keep = np.all(np.isfinite(R), axis=0)
    names = [c for c, k in zip(list(ind["columns"]) + [f"B/M {i}" for i in range(1, 11)], keep) if k]
    R = R[:, keep]
    f = ff["mkt_rf"][m]
    tp = econ.two_pass(R, f)
    g = econ.grs(R, f)
    return _json({"names": names, "N": int(R.shape[1]), "T": int(R.shape[0]), "betas": tp["betas"][:, 0],
                  "mean": tp["mean_returns"], "lambda": tp["lambda"], "t_fm": tp["t_fm"], "t_shanken": tp["t_shanken"],
                  "se_fm": tp["se_fm"], "se_shanken": tp["se_shanken"], "mkt_mean": float(f.mean()),
                  "mkt_t": float(f.mean() / f.std(ddof=1) * np.sqrt(len(f))), "grs_F": g["F"], "grs_p": g["p"],
                  "grs_df": list(g["df"]), "shanken_c": tp["shanken_c"]})


# ---------------------------------------------------------------------------
def compute_stambaugh_cloud() -> dict:
    s = CACHE.load("stambaugh")
    rho, corr, sd_u, sd_v = s["sim_rho"], s["sim_corr"], s["sd_u"], s["sd_v"]
    L = np.linalg.cholesky(np.array([[sd_u ** 2, corr * sd_u * sd_v], [corr * sd_u * sd_v, sd_v ** 2]]))
    out = {}
    for T in (50, 75, 100, 150):
        rng = np.random.default_rng(700 + T)
        n = 4000
        E = rng.standard_normal((n, T + 201, 2)) @ L.T
        x = np.zeros((n, T + 201))
        for t in range(1, T + 201):
            x[:, t] = rho * x[:, t - 1] + E[:, t, 1]
        x = x[:, 200:]
        r = E[:, 201:, 0]
        xl, xn = x[:, :-1], x[:, 1:]
        xc = xl - xl.mean(1, keepdims=True)
        b = (xc * (r - r.mean(1, keepdims=True))).sum(1) / (xc * xc).sum(1)
        rh = (xc * (xn - xn.mean(1, keepdims=True))).sum(1) / (xc * xc).sum(1)
        slope = float(np.polyfit(rh - rho, b, 1)[0])
        out[str(T)] = {"drho": (rh - rho)[:1500], "dbeta": b[:1500], "mean_drho": float((rh - rho).mean()),
                       "mean_dbeta": float(b.mean()), "slope": slope,
                       "kendall": float(-(1 + 3 * rho) / T), "formula": float(corr * sd_u / sd_v * -(1 + 3 * rho) / T)}
    return _json({"rho": rho, "corr": corr, "phi": corr * sd_u / sd_v, "T": out})


def compute_ivx() -> dict:
    s = data.shiller()
    t, P, D = s["t"], s["price"], s["div"]
    jan = np.isclose(t % 1, 0) & np.isfinite(P) & np.isfinite(D)
    Py, Dy = P[jan], D[jan]
    r = np.log((Py[1:] + Dy[:-1]) / Py[:-1])
    x = np.log(Dy / Py)
    ra = np.append(r, 0.0)
    aug_a = econ.augmented_predictive(ra, x)
    ivx_a = econ.ivx(ra, x)
    ols_a = econ.ols(r, x[:-1])
    tm, lr, dy = _shiller_lr_dy()
    rm = np.append(lr[1:], 0.0)
    xm = dy[: len(rm)]
    aug_m = econ.augmented_predictive(rm, xm)
    ivx_m = econ.ivx(rm, xm)
    ols_m = econ.ols(lr[1:], xm[:-1])
    post = tm[: len(rm)] >= 1952
    ivx_post = econ.ivx(rm[post], xm[post])
    ols_post = econ.ols(rm[post][:-1], xm[post][:-1])
    return _json({"annual": {"ols": float(ols_a["beta"][1]), "ols_t": float(ols_a["t"][1]), "aug": aug_a, "ivx": ivx_a},
                  "monthly": {"ols": float(ols_m["beta"][1]), "ols_t": float(ols_m["t"][1]), "aug": aug_m, "ivx": ivx_m},
                  "monthly_post1952": {"ols": float(ols_post["beta"][1]), "ols_t": float(ols_post["t"][1]),
                                       "ivx": ivx_post}})


# ---------------------------------------------------------------------------
def compute_oos() -> dict:
    s = data.shiller()
    t, cpi = s["t"], s["cpi"]
    P = s["price"] * cpi[-1] / cpi
    D = s["div"] * cpi[-1] / cpi
    E = s["earn"] * cpi[-1] / cpi
    lr = np.log((P[1:] + D[:-1] / 12) / P[:-1])
    n = len(lr)
    infl = np.full(len(t), np.nan)
    infl[12:] = np.log(cpi[12:] / cpi[:-12])
    preds = {"dividend yield": np.log(D / P), "earnings yield": np.log(E / P), "CAPE": np.log(s["cape"]),
             "10-year yield": s["gs10"] / 100, "inflation": infl}
    start = int(np.searchsorted(t, 1927.0))
    S2 = float((np.nanmean(lr) / np.nanstd(lr)) ** 2)
    out = {}
    for name, xv in preds.items():
        x = xv[:n]
        ok = np.isfinite(x) & np.isfinite(lr)
        ins = econ.ols(lr[ok], x[ok], se="nw", lags=12)
        o = econ.oos_r2(lr, x, start)
        c = econ.oos_r2(lr, x, start, ct=True)
        out[name] = {"r2_is": ins["r2"], "t_is": float(ins["t"][1]), "beta_is": float(ins["beta"][1]),
                     "r2_os": o["r2_os"], "r2_os_ct": c["r2_os"], "dsse": o["dsse"][::3], "dsse_ct": c["dsse"][::3]}
    # the dividend yield's slope as a real-time forecaster saw it, once a year, with a Newey-West band
    x = preds["dividend yield"][:n]
    path = []
    for k in range(start, n, 12):
        r_ = econ.ols(lr[:k], x[:k], se="nw", lags=12)
        path.append((float(t[k]), float(r_["beta"][1]), float(r_["se"][1])))
    o = econ.oos_r2(lr, x, start)
    yrs = t[start:n]
    at = {str(y): float(o["dsse"][int(np.searchsorted(yrs, y)) - 1]) for y in (1990, 2000)}
    return _json({"predictors": out, "t": yrs[::3], "start": float(t[start]), "S2": S2, "slope_path": path,
                  "dsse_at": at, "dsse_end": float(o["dsse"][-1]), "n_oos": int(n - start)})


# ---------------------------------------------------------------------------
def compute_mle() -> dict:
    kf = data.ken_french_daily()
    d, r = pit.research(kf["date"], kf["mkt"])
    x = 100 * r
    nll = lambda th: -sst.t.logpdf(x, 2 + np.exp(th[2]), th[0], np.exp(th[1]))  # noqa: E731
    m = econ.mle(nll, [0.0, np.log(1.6), np.log(25.0)], steps=60)
    th = m["theta"]
    nu, sc = 2 + np.exp(th[2]), np.exp(th[1])
    Jac = np.diag([1.0, sc, np.exp(th[2])])  # d(mu, sigma, nu) / d(theta)
    Hi = np.linalg.inv(m["H"])
    V_naive = Jac @ Hi @ Jac.T
    V_sand = Jac @ Hi @ m["J"] @ Hi @ Jac.T
    # scores per observation; with volatility clustering they are serially dependent, so J needs a long-run variance
    eps = 1e-5 * np.maximum(1.0, np.abs(th))
    sc_ = np.column_stack([(nll(th + e) - nll(th - e)) / (2 * e.max()) for e in np.eye(3) * eps])
    J_hac = econ.lrv(sc_, "bartlett", bw=250) * len(x)
    V_hac = Jac @ Hi @ J_hac @ Hi @ Jac.T
    path = np.column_stack([m["path"][:, 0], np.exp(m["path"][:, 1]), 2 + np.exp(m["path"][:, 2])])
    nus = np.linspace(2.2, 6.0, 44)
    scs = np.linspace(0.45, 1.05, 44)
    ll_max = -float(np.sum(nll(th)))
    grid = np.array([[-float(np.sum(nll([th[0], np.log(s_), np.log(v_ - 2)]))) - ll_max for v_ in nus] for s_ in scs])
    ks = sst.kurtosis(x, fisher=False)
    return _json({"n": int(len(x)), "first": int(d[0]), "last": int(d[-1]), "mu": float(th[0]), "scale": float(sc),
                  "nu": float(nu), "path": path, "nll_path": m["nll"], "se_naive": np.sqrt(np.diag(V_naive)),
                  "se_sandwich": np.sqrt(np.diag(V_sand)), "V_naive": V_naive[1:, 1:], "V_sandwich": V_sand[1:, 1:],
                  "se_hac": np.sqrt(np.diag(V_hac)), "V_hac": V_hac[1:, 1:],
                  "grid_nu": nus, "grid_scale": scs, "grid_ll": grid, "kurtosis": float(ks),
                  "normal_ll_gap": float(-np.sum(sst.norm.logpdf(x, x.mean(), x.std())) - np.sum(nll(th)))})


# ---------------------------------------------------------------------------
def compute_gmm_toy() -> dict:
    rng = np.random.default_rng(66)
    n = 50
    x1 = rng.normal(1.0, 1.0, n)
    x2 = rng.normal(1.0, 2.0, n)
    mom = lambda th: np.column_stack([x1 - th[0], x2 - th[0]])  # noqa: E731
    res = econ.gmm(mom, [0.0], lags=0)
    G = mom(res["theta"])
    S = np.cov(G.T, bias=True)
    W = np.linalg.inv(S)
    return _json({"m1": float(x1.mean()), "m2": float(x2.mean()), "step1": float((x1.mean() + x2.mean()) / 2),
                  "theta": float(res["theta"][0]), "se": float(res["se"][0]), "J": res["J"], "p_J": res["p_J"],
                  "S": S, "W": W, "n": n})


def _euler_moments():
    c = data.fred("A794RX0Q048SBEA", start="1947-01-01")
    cpi = data.fred("CPIAUCSL", start="1947-01-01")
    ff = data.ken_french_factors_monthly()
    cd, cv = c["date"], c["value"]
    m = (cd >= 19470101) & (cd <= 20201001)
    cd, cv = cd[m], cv[m]
    q = (cd // 10000) * 10 + ((cd // 100) % 100 - 1) // 3 + 1
    g = cv[1:] / cv[:-1]
    qy = q[1:]
    fd = ff["date"]
    fq = (fd // 100) * 10 + ((fd % 100) - 1) // 3 + 1
    mk = ff["mkt_rf"] + ff["rf"]
    Rm = {k: float(np.prod(1 + mk[fq == k])) for k in np.unique(fq)}
    Rf = {k: float(np.prod(1 + ff["rf"][fq == k])) for k in np.unique(fq)}
    pd_, pv = cpi["date"], cpi["value"]
    pq = (pd_ // 10000) * 10 + ((pd_ // 100) % 100 - 1) // 3 + 1
    Pq = {k: float(pv[pq == k].mean()) for k in np.unique(pq)}
    rows = []
    for i, k in enumerate(qy):
        prev = q[i]
        if k in Rm and k in Pq and prev in Pq:
            infl = Pq[k] / Pq[prev]
            rows.append((g[i], Rm[k] / infl, Rf[k] / infl))
    A = np.array(rows)
    return A[:, 0], A[:, 1], A[:, 2]


def _euler_fn(G, RM, RF):
    Z = np.column_stack([np.ones(len(G) - 1), G[:-1], RM[:-1]])
    Gt, RMt, RFt = G[1:], RM[1:], RF[1:]

    def moments(th):
        sdf = th[0] * Gt ** (-th[1])
        return np.column_stack([(sdf * RMt - 1)[:, None] * Z, (sdf * RFt - 1)[:, None] * Z])
    return moments


def compute_gmm_surface() -> dict:
    from scipy import optimize
    G, RM, RF = _euler_moments()
    mom = _euler_fn(G, RM, RF)
    est = CACHE.load("gmm")
    th = np.array([est["beta"], est["gamma"]])
    Gm = mom(th)
    n = len(Gm)
    Gc = Gm - Gm.mean(0)
    S = Gc.T @ Gc / n
    for l_ in (1, 2):
        C = Gc[l_:].T @ Gc[:-l_] / n
        S += (1 - l_ / 3) * (C + C.T)
    W = np.linalg.inv(S)
    J = lambda t: n * float(mom(t).mean(0) @ W @ mom(t).mean(0))  # noqa: E731
    bs = np.linspace(0.96, 1.04, 61)
    gs = np.linspace(-10, 40, 61)
    grid = np.array([[J([b, g_]) for b in bs] for g_ in gs])
    path = [[0.975, 32.0]]
    optimize.minimize(J, path[0], method="Nelder-Mead", callback=lambda xk: path.append(list(xk)),
                      options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 400})
    return _json({"beta": bs, "gamma": gs, "J": grid, "path": path, "J_min": J(th), "theta": th,
                  "ridge": [float(gs[int(np.argmin(grid[:, i]))]) for i in range(len(bs))]})


def compute_gmm_mc() -> dict:
    """400 economies in which the consumption Euler equation holds exactly (power utility, beta = 1, gamma = 2,
    lognormal consumption growth and market returns with the data's volatilities and correlation), each as long as
    our sample; two-step GMM with the same moments and instruments."""
    est = CACHE.load("gmm")
    G, RM, RF = _euler_moments()
    n = len(G)
    sg = float(np.std(np.log(G)))
    sm = float(np.std(np.log(RM)))
    rgm = float(np.corrcoef(np.log(G), np.log(RM))[0, 1])
    mug = float(np.mean(np.log(G)))
    beta0, gam0 = 1.0, 2.0
    rf = -np.log(beta0) + gam0 * mug - 0.5 * gam0 ** 2 * sg ** 2
    covgm = rgm * sg * sm
    mum = -np.log(beta0) + gam0 * mug - 0.5 * (sm ** 2 - 2 * gam0 * covgm + gam0 ** 2 * sg ** 2)
    L = np.linalg.cholesky([[sg ** 2, covgm], [covgm, sm ** 2]])
    part = CACHE.partial("gmm_mc", {"n": n, "beta": beta0, "gamma": gam0, "v": 1})
    for k in range(400):
        if str(k) in part:
            continue
        rng = np.random.default_rng(5000 + k)
        e = rng.standard_normal((n, 2)) @ L.T
        Gs = np.exp(mug + e[:, 0])
        RMs = np.exp(mum + e[:, 1])
        RFs = np.full(n, np.exp(rf))
        mom = _euler_fn(Gs, RMs, RFs)
        try:
            res = econ.gmm(mom, [0.99, 2.0], lags=2)
            part[str(k)] = [float(res["theta"][0]), float(res["theta"][1]), float(res["se"][1]), res["J"], res["p_J"]]
        except np.linalg.LinAlgError:
            part[str(k)] = [np.nan] * 5
    A = np.array([part[str(k)] for k in range(400)], float)
    ok = np.all(np.isfinite(A), axis=1)
    A = A[ok]
    g_hat = A[:, 1]
    cover = float(np.mean(np.abs(g_hat - gam0) < 1.96 * A[:, 2]))
    return _json({"gamma_true": gam0, "beta_true": beta0, "gamma_hat": g_hat, "beta_hat": A[:, 0],
                  "J": A[:, 3], "rej_J": float(np.mean(A[:, 4] < 0.05)), "cover_gamma": cover,
                  "q": np.quantile(g_hat, [0.05, 0.25, 0.5, 0.75, 0.95]), "sd": float(np.std(g_hat)),
                  "n": n, "n_ok": int(ok.sum()), "real_J": est["J"]})


# ---------------------------------------------------------------------------
def _fomc_dates():
    import hashlib
    import html as _html
    import json as _json_mod
    import re

    from videos.quant.quant6 import fomc_dates as F
    dates = list(F.DATES)
    frozen = _json_mod.dumps(dates, separators=(",", ":")).encode()
    assert hashlib.sha256(frozen).hexdigest() == F.SHA256
    data._check("fed/fomc_scheduled/1994-2020", frozen, F.SOURCE.format(year="<YYYY>"))
    mon = {m[:3]: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                           "September", "October", "November", "December"], 1)}
    pages = [data.DATA / "fed" / f"fomchistorical{y}.htm" for y in range(1994, 2021)]
    if all(p.exists() for p in pages):  # re-derive from the Fed's pages and insist on the transcription
        got = []
        for y, p in zip(range(1994, 2021), pages):
            t = re.sub(r"<script.*?</script>", "", p.read_text("utf-8", "replace"), flags=re.S)
            ys = set()
            for line in _html.unescape(re.sub(r"<[^>]+>", "\n", t)).split("\n"):
                mm = re.match(rf"^([A-Za-z]+)(?:/([A-Za-z]+))? (\d+)(?:-(?:([A-Za-z]+) )?(\d+))?\s+Meeting\s*-\s*{y}$",
                              line.strip())
                if mm:
                    ys.add(y * 10000 + mon[(mm.group(4) or mm.group(2) or mm.group(1))[:3]] * 100
                           + int(mm.group(5) or mm.group(3)))
            ys = sorted(ys)
            got += [d for i, d in enumerate(ys) if not (i + 1 < len(ys) and ys[i + 1] - d <= 3)]
        assert got == dates, "the Fed's pages and fomc_dates.py disagree"
    return np.array(dates)


def compute_fomc() -> dict:
    kf = data.ken_french_daily()
    m = (kf["date"] >= 19940101) & (kf["date"] <= 20201231)
    d, r = kf["date"][m], kf["mkt_rf"][m]
    fd = _fomc_dates()
    assert np.isin(fd, d).all(), "an FOMC date is not a trading day"
    ev = np.isin(d, fd)
    allp = econ.event_mean_test(r, ev)
    sub = {}
    for name, mm in (("1994-2010", d < 20110101), ("2011-2020", d >= 20110101), ("1994-2011", d < 20120101)):
        sub[name] = econ.event_mean_test(r[mm], ev[mm])
    pl = econ.placebo_means(r, int(ev.sum()), reps=10000, exclude=ev, seed=61)
    p_placebo = float(np.mean(pl >= r[ev].mean()))
    # event-time paths of cumulative abnormal return (constant-mean model), tau = -5 .. +5
    mu = r[~ev].mean()
    idx = np.flatnonzero(ev)
    W = 5
    paths = np.array([np.cumsum(r[i - W:i + W + 1] - mu) - np.sum(r[i - W:i] - mu) for i in idx if W <= i < len(r) - W])
    car = paths.mean(0)
    se_cs = paths.std(0, ddof=1) / np.sqrt(len(paths))
    # the running mean and its band as events are added (tau = 0 abnormal return)
    ar0 = r[idx] - mu
    run = [(k, float(ar0[:k].mean()), float(ar0[:k].std(ddof=1) / np.sqrt(k))) for k in
           (5, 10, 20, 40, 80, 120, 160, len(ar0))]
    share = float(r[ev].sum() / r.sum())
    # same-date clustering, simulated: 100 firms announcing on one day share an industry shock the market model
    # does not remove; the naive standard error assumes they are independent
    rng = np.random.default_rng(62)
    sims, naive = [], []
    for _ in range(4000):
        ar = 0.015 * rng.standard_normal() + 0.02 * rng.standard_normal(100)
        sims.append(ar.mean())
        naive.append(ar.std(ddof=1) / 10)
    pick = idx[np.linspace(0, len(idx) - 1, 40).astype(int)]
    return _json({"all": allp, "sub": sub, "placebo": pl[::5], "p_placebo": p_placebo, "n_days": int(len(r)),
                  "share_of_return": share, "share_of_days": float(ev.mean()), "car": car, "se_cs": se_cs,
                  "paths": paths[np.linspace(0, len(paths) - 1, 40).astype(int)], "run": run,
                  "pick_dates": d[pick], "pick_idx": pick, "cluster_true": float(np.std(sims)),
                  "cluster_naive": float(np.mean(naive)), "n_events": int(ev.sum()), "first": int(fd[0]),
                  "last": int(fd[-1])})


# ---------------------------------------------------------------------------
def compute_lookahead() -> dict:
    """A toy of F-Squared's error (illustrative): each week, hold the size deciles whose past four weeks were
    positive (else cash); honestly, and with the signal applied one week early."""
    s = data.ken_french_size_daily()
    m = (s["date"] >= 20010101) & (s["date"] <= 20081231)
    d, R = s["date"][m], s["deciles"][m]
    import datetime as dt
    wk = np.array([dt.date(x // 10000, (x // 100) % 100, x % 100).isocalendar()[:2] for x in d])
    key = wk[:, 0] * 100 + wk[:, 1]
    weeks, inv = np.unique(key, return_inverse=True)
    Wr = np.array([np.prod(1 + R[inv == i], axis=0) - 1 for i in range(len(weeks))])
    lw = np.log1p(Wr)
    cs = np.vstack([np.zeros(10), np.cumsum(lw, axis=0)])
    mom = np.full_like(lw, np.nan)
    for i in range(4, len(lw) + 1):
        mom[i - 1] = cs[i] - cs[i - 4]  # weeks i-4 .. i-1 (0-based i-1 is the last week included)
    honest, early, bh = [1.0], [1.0], [1.0]
    for i in range(5, len(lw)):
        sig_h = mom[i - 1] > 0     # known at the start of week i
        sig_e = mom[i] > 0         # includes week i itself: the one-week look-ahead
        rh = Wr[i][sig_h].mean() if sig_h.any() else 0.0
        re_ = Wr[i][sig_e].mean() if sig_e.any() else 0.0
        honest.append(honest[-1] * (1 + rh))
        early.append(early[-1] * (1 + re_))
        bh.append(bh[-1] * (1 + Wr[i].mean()))
    yrs = len(honest) / 52.18
    ann = lambda c: c[-1] ** (1 / yrs) - 1  # noqa: E731
    return _json({"honest": honest, "early": early, "hold": bh, "weeks": int(len(honest)),
                  "first": int(d[0]), "last": int(d[-1]), "ann_honest": ann(honest), "ann_early": ann(early),
                  "ann_hold": ann(bh), "multiple_honest": honest[-1], "multiple_early": early[-1],
                  "inflation": float((early[-1] - 1) / (honest[-1] - 1) - 1) if honest[-1] > 1 else None})


# ---------------------------------------------------------------------------
def compute_boot_demo() -> dict:
    ff = data.ken_french_factors_monthly()
    x = ff["mkt_rf"]
    sr = lambda z: z.mean() / z.std(ddof=1)  # noqa: E731
    ann = np.sqrt(12)
    st = econ.stationary_bootstrap(x, sr, mean_block=12, B=800, seed=2) * ann
    iid = econ.moving_block_bootstrap(x, sr, block=1, B=800, seed=3) * ann
    idx = econ.stationary_indices(len(x), 12, B=3, seed=4)
    return _json({"x": x, "stationary": st, "iid": iid, "se_st": float(st.std()), "se_iid": float(iid.std()),
                  "idx": idx, "sr": float(sr(x) * ann), "dates": ff["date"]})


def compute_boot_coverage() -> dict:
    """1,000 simulated monthly markets of 1,134 months: AR(1) returns (phi = 0.1) with GARCH(1,1) shocks, true
    monthly Sharpe 0.125; the nominal 95% interval (estimate +/- 1.96 bootstrap se) from iid, moving-block (12) and
    stationary (12) bootstraps, B = 400; how often each covers the truth."""
    n, B, P = 1134, 400, 1000
    phi, om, al, be = 0.1, 0.02, 0.08, 0.9
    sd_u = np.sqrt(1.0 / (1 - phi ** 2))
    sr_true = 0.125
    mu = sr_true * sd_u
    part = CACHE.partial("boot_coverage", {"n": n, "B": B, "P": P, "v": 1})
    nb = int(np.ceil(n / 12))
    for chunk in range(0, P, 50):
        key = str(chunk)
        if key in part:
            continue
        res = []
        for pth in range(chunk, chunk + 50):
            rng = np.random.default_rng(10_000 + pth)
            h, e_prev, r = 1.0, 0.0, np.empty(n + 200)
            z = rng.standard_normal(n + 200)
            u_prev = 0.0
            for t in range(n + 200):
                h = om + al * e_prev ** 2 + be * h
                e_prev = np.sqrt(h) * z[t]
                u_prev = phi * u_prev + e_prev
                r[t] = u_prev
            x = mu + r[200:]
            s_hat = x.mean() / x.std(ddof=1)
            row = [s_hat]
            for method in ("iid", "block", "stationary"):
                if method == "iid":
                    idx = rng.integers(0, n, (B, n))
                elif method == "block":
                    st = rng.integers(0, n - 12 + 1, (B, nb))
                    idx = (st[:, :, None] + np.arange(12)).reshape(B, -1)[:, :n]
                else:
                    idx = econ.stationary_indices(n, 12, B=B, seed=int(rng.integers(1 << 31)))
                xb = x[idx]
                sb = xb.mean(1) / xb.std(1, ddof=1)
                row.append(float(sb.std()))
            res.append(row)
        part[key] = res
    A = np.array([row for c in range(0, P, 50) for row in part[str(c)]])
    true_sd = float(A[:, 0].std())
    cover = {m: float(np.mean(np.abs(A[:, 0] - sr_true) < 1.96 * A[:, i + 1]))
             for i, m in enumerate(("iid", "block", "stationary"))}
    se_mean = {m: float(A[:, i + 1].mean()) for i, m in enumerate(("iid", "block", "stationary"))}
    return _json({"cover": cover, "se_mean": se_mean, "true_sd": true_sd, "paths": P, "B": B, "n": n,
                  "sr_true": sr_true, "phi": phi, "garch": [om, al, be]})


# ---------------------------------------------------------------------------
def compute_gibbs() -> dict:
    sh = CACHE.load("shrinkage")
    ind = data.ken_french_industries(49)
    ff = data.ken_french_factors_monthly()
    ex = ind["returns"] - ff["rf"][:, None]
    d = ind["date"]
    a = (d >= 192701) & (d <= 197312)
    full = [c in sh["names"] for c in ind["columns"]]
    s1 = np.nanstd(ex[a][:, full], axis=0, ddof=1) * np.sqrt(12) / np.sqrt(a.sum() / 12)
    raw, later = np.asarray(sh["raw"]), np.asarray(sh["later"])
    g = econ.gibbs_hierarchical(raw, s1, draws=5000, chains=4, seed=0)
    post = g["alpha_post"]
    return _json({"mu": g["mu"][:, ::10], "tau": g["tau"][:, ::10], "tau_all": np.sort(g["tau"].ravel())[::20],
                  "tau_median": float(np.median(g["tau"])), "tau_q90": float(np.quantile(g["tau"], 0.9)),
                  "post": post, "raw": raw, "later": later, "se": s1, "mse_raw": float(np.mean((raw - later) ** 2)),
                  "mse_post": float(np.mean((post - later) ** 2)), "mse_eb": sh["mse_shrunk"],
                  "shrink_frac": float(1 - np.std(post) / np.std(raw)), "names": sh["names"]})


# ---------------------------------------------------------------------------
def compute_fdr_sim() -> dict:
    m, m1, yrs, sr = 1000, 50, 20, 0.5
    out = {k: {"true": [], "false": [], "fdp": []} for k in ("raw", "Bonferroni", "Holm", "BH")}
    for seed in range(200):
        rng = np.random.default_rng(3000 + seed)
        t = rng.standard_normal(m)
        t[:m1] += sr * np.sqrt(yrs)
        p = 2 * sst.norm.sf(np.abs(t))
        for k, rej in (("raw", p < 0.05), ("Bonferroni", econ.bonferroni(p)), ("Holm", econ.holm(p)),
                       ("BH", econ.benjamini_hochberg(p))):
            tr, fa = int(rej[:m1].sum()), int(rej[m1:].sum())
            out[k]["true"].append(tr)
            out[k]["false"].append(fa)
            out[k]["fdp"].append(fa / max(tr + fa, 1))
    summ = {k: {"true": float(np.mean(v["true"])), "false": float(np.mean(v["false"])), "fdr": float(np.mean(v["fdp"])),
                "fwer": float(np.mean(np.array(v["false"]) > 0)), "true_q": np.quantile(v["true"], [0.1, 0.9]),
                "false_q": np.quantile(v["false"], [0.1, 0.9])} for k, v in out.items()}
    rng = np.random.default_rng(3000)
    t = rng.standard_normal(m)
    t[:m1] += sr * np.sqrt(yrs)
    return _json({"summary": summ, "runs": out, "p_example": 2 * sst.norm.sf(np.abs(t)), "m": m, "m1": m1,
                  "years": yrs, "sr": sr})


# ---------------------------------------------------------------------------
def compute_designs() -> dict:
    out = {}
    # instruments: weak and strong first stages; truth 0.5, a confounder pushes OLS up
    for name, pi in (("weak", 0.07), ("strong", 0.35)):
        b_iv, b_ols, F = [], [], []
        for s in range(200):
            rng = np.random.default_rng(4000 + s)
            n = 1000
            u, z = rng.standard_normal(n), rng.standard_normal(n)
            x = pi * z + u + rng.standard_normal(n)
            y = 0.5 * x + u + rng.standard_normal(n)
            r = econ.iv_2sls(y, x, z)
            b_iv.append(r["beta"])
            F.append(r["F"])
            b_ols.append(float(econ.ols(y, x)["beta"][1]))
        out[name] = {"iv": b_iv, "ols": b_ols, "F": float(np.median(F)), "iv_median": float(np.median(b_iv)),
                     "ols_mean": float(np.mean(b_ols)), "iv_iqr": np.quantile(b_iv, [0.25, 0.75])}
    # staggered adoption: three cohorts treated in periods 2, 5 and 8 of 10, effects growing 0.3 a period
    T, coh_list = 10, [2, 5, 8]
    tw, cs, truth = [], [], []
    for s in range(200):
        rng = np.random.default_rng(4500 + s)
        coh = np.repeat(coh_list, 20).astype(float)
        tt = np.arange(T)
        D = (tt[None, :] >= coh[:, None]).astype(float)
        eff = np.where(D > 0, 0.3 * (tt[None, :] - coh[:, None] + 1), 0.0)
        Y = rng.standard_normal((60, 1)) + 0.1 * tt[None, :] + rng.standard_normal((1, T)) * 0.2 + eff \
            + 0.3 * rng.standard_normal((60, T))
        tw.append(econ.twfe(Y, D)["beta"])
        c = econ.did_cs(Y, coh)
        cs.append(c["att"])
        cells = [(g, t) for g, t, _, _ in c["cells"]]
        truth.append(float(np.mean([0.3 * (t - g + 1) for g, t in cells])))
        if s == 0:
            W = econ.twfe(Y, D)["weights"]
            wcell = [[float(W[coh == g, t].sum()) for t in range(T)] for g in coh_list]
    out["staggered"] = {"twfe": tw, "cs": cs, "truth": float(np.mean(truth)), "weights": wcell, "cohorts": coh_list,
                        "T": T, "true_all": float(np.mean([0.3 * (t - g + 1) for g in coh_list for t in range(g, T)])),
                        "twfe_mean": float(np.mean(tw)), "cs_mean": float(np.mean(cs))}
    # regression discontinuity at a rank cutoff: rank 1,000 (last of the Russell 1000) vs 1,001 (first of the 2000);
    # planted: +2 points in the outcome for stocks just inside the Russell 2000, a relation that curves differently on
    # the two sides (so a wide window is biased)
    bws = [25, 50, 75, 100, 150, 200, 300]
    est = {str(b): [] for b in bws}
    for s in range(200):
        rng = np.random.default_rng(4800 + s)
        rank = rng.integers(500, 1501, 2000)
        xr = (rank - 1000.5) / 100
        y = 1.0 + 0.8 * xr - 0.6 * xr ** 2 + 1.2 * xr ** 2 * (rank > 1000) + 2.0 * (rank > 1000) \
            + 3.0 * rng.standard_normal(len(xr))
        for b in bws:
            est[str(b)].append(econ.rd_local_linear(xr, y, 0.0, b / 100)["jump"])
        if s == 0:
            ex = {"x": xr, "y": y, "fits": {str(b): econ.rd_local_linear(xr, y, 0.0, b / 100) for b in bws}}
    out["rd"] = {"bw": bws, "mean": [float(np.mean(est[str(b)])) for b in bws],
                 "sd": [float(np.std(est[str(b)])) for b in bws], "truth": 2.0,
                 "rmse": [float(np.sqrt(np.mean((np.array(est[str(b)]) - 2.0) ** 2))) for b in bws], "example": ex}
    # the two-by-two: one seeded example
    rng = np.random.default_rng(3)
    tt = np.arange(-6, 7)
    ctrl = 1.0 + 0.08 * tt + 0.05 * rng.standard_normal(len(tt))
    trt = 1.4 + 0.08 * tt + np.where(tt >= 0, 0.35, 0) + 0.05 * rng.standard_normal(len(tt))
    out["did"] = {"t": tt, "ctrl": ctrl, "trt": trt, "est": econ.did_2x2(trt[tt >= 0], trt[tt < 0], ctrl[tt >= 0],
                                                                        ctrl[tt < 0]), "truth": 0.35}
    return _json(out)


# ---------------------------------------------------------------------------
def _plugin_plr(y, d, X, lam, folds=5, seed=0, iters=8):
    """The naive (non-orthogonal) plug-in: learn g by ridge on y - theta d, then theta from d's correlation with what
    is left; regularisation bias in g leaks straight into theta."""
    rng = np.random.default_rng(seed)
    fold = rng.permutation(len(y)) % folds
    th = 0.0
    for _ in range(iters):
        gh = np.empty(len(y))
        for k in range(folds):
            tr, te = fold != k, fold == k
            gh[te] = econ.ridge_fit_predict(X[tr], (y - th * d)[tr], X[te], lam)
        th = float(d @ (y - gh) / (d @ d))
    return th


def compute_dml_lambda() -> dict:
    lams = list(10.0 ** np.linspace(-2, 4, 13))
    rows = []
    part = CACHE.partial("dml_lambda", {"lams": lams, "v": 1})
    for s in range(5):
        if str(s) in part:
            continue
        rng = np.random.default_rng(1200 + s)
        n = 2000
        X = rng.uniform(-2, 2, (n, 3))
        m = np.sin(2 * X[:, 0]) + 0.5 * X[:, 1] ** 2
        g = 2 * np.sin(2 * X[:, 0]) + X[:, 1] ** 2 + 0.5 * X[:, 2]
        d = m + rng.standard_normal(n)
        y = 0.3 * d + g + rng.standard_normal(n)
        res = []
        fold = np.random.default_rng(s).permutation(n) % 5
        for lam in lams:
            dm = econ.dml_plr(y, d, X, lam=lam, seed=s)
            pl = _plugin_plr(y, d, X, lam, seed=s)
            em, el = [], []
            for k in range(5):
                tr, te = fold != k, fold == k
                em.append(np.mean((d[te] - econ.ridge_fit_predict(X[tr], d[tr], X[te], lam)) ** 2))
                el.append(np.mean((y[te] - econ.ridge_fit_predict(X[tr], y[tr], X[te], lam)) ** 2))
            res.append([dm["theta"], pl, float(np.mean(em)), float(np.mean(el))])
        part[str(s)] = res
    A = np.array([part[str(s)] for s in range(5)])  # seeds x lams x 4
    return _json({"lams": lams, "dml": A[:, :, 0], "plugin": A[:, :, 1], "mse_m": A[:, :, 2], "mse_l": A[:, :, 3],
                  "theta": 0.3})


def compute_dml_demo() -> dict:
    """One sample of the planted partially linear world (n = 600) for the picture: the raw (d, y) cloud, and the
    cross-fitted residual cloud, with their slopes."""
    rng = np.random.default_rng(1300)
    n = 600
    X = rng.uniform(-2, 2, (n, 3))
    m = np.sin(2 * X[:, 0]) + 0.5 * X[:, 1] ** 2
    g = 2 * np.sin(2 * X[:, 0]) + X[:, 1] ** 2 + 0.5 * X[:, 2]
    d = m + rng.standard_normal(n)
    y = 0.3 * d + g + rng.standard_normal(n)
    fold = np.random.default_rng(7).permutation(n) % 5
    ry, rd = np.empty(n), np.empty(n)
    for k in range(5):
        tr, te = fold != k, fold == k
        ry[te] = y[te] - econ.ridge_fit_predict(X[tr], y[tr], X[te])
        rd[te] = d[te] - econ.ridge_fit_predict(X[tr], d[tr], X[te])
    return _json({"d": d, "y": y, "x1": X[:, 0], "rd": rd, "ry": ry, "fold": fold,
                  "slope_raw": float(econ.ols(y, d)["beta"][1]), "slope_res": float(rd @ ry / (rd @ rd))})


# ---------------------------------------------------------------------------
def compute_ellipse_path() -> dict:
    ind = data.ken_french_industries(49)
    ff = data.ken_french_factors_monthly()
    j = ind["columns"].index("Smoke")
    ex = ind["returns"][:, j] - ff["rf"]
    m0 = int(np.searchsorted(ind["date"], 196101))
    out = []
    for end in range(m0 + 12, len(ex) + 1, 3):
        r = econ.ols(ex[m0:end], ff["mkt_rf"][m0:end])
        V = r["V"].copy()
        V[0, :] *= 12
        V[:, 0] *= 12
        out.append({"months": end - m0, "date": int(ind["date"][end - 1]), "alpha": float(r["beta"][0] * 12),
                    "beta": float(r["beta"][1]), "V": V})
    return _json({"path": out})


ITEMS = {"overlap": compute_overlap, "stambaugh": compute_stambaugh, "gmm": compute_gmm, "event": compute_event,
         "panel": compute_panel, "bootstrap": compute_bootstrap, "shrinkage": compute_shrinkage,
         "multiple": compute_multiple, "ellipse": compute_ellipse, "dml": compute_dml, "snr": compute_snr,
         "envelope": compute_envelope, "ols_fwl": compute_ols_fwl, "hac": compute_hac, "har_size": compute_har_size,
         "petersen": compute_petersen, "panel_fe": compute_panel_fe, "twopass": compute_twopass,
         "stambaugh_cloud": compute_stambaugh_cloud, "ivx": compute_ivx, "oos": compute_oos, "mle": compute_mle,
         "gmm_toy": compute_gmm_toy, "gmm_surface": compute_gmm_surface, "gmm_mc": compute_gmm_mc,
         "fomc": compute_fomc, "lookahead": compute_lookahead, "boot_demo": compute_boot_demo,
         "boot_coverage": compute_boot_coverage, "gibbs": compute_gibbs, "fdr_sim": compute_fdr_sim,
         "designs": compute_designs, "dml_lambda": compute_dml_lambda, "ellipse_path": compute_ellipse_path,
         "dml_demo": compute_dml_demo}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
