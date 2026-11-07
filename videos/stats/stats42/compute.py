"""Precompute every number in Part 42 of *Statistics, Built* ("The Comprehensive Exam").

    OMP_NUM_THREADS=1 python -m videos.stats.stats42.compute            # everything missing (a few minutes)
    python -m videos.stats.stats42.compute --force board

Results are cached in ``.cache/stats42/<name>.json``.  The pilot survey, the trial's towns and the salt-substitute survey
are the World's (``World.ministry``); the exam problems use the Museum (Bliss, Longley, the eight schools, Old
Faithful, Newcomb, Stamey's prostate data, the prostate microarray, New York's air quality, Gehan's 6-MP trial) and
seeded simulations.

Items:
    pilot       Case 1: the pilot survey's town means, the one-way ANOVA and the intraclass correlation
    size        Case 1: sample size by formula, the design effect, towns needed against adults per town, power curves
    plan        Case 1: the plan simulated (type I error, power, coverage) and the trial run in the World
    obs         Case 2: naive, adjusted, bad controls, overlap, MI + AIPW, the robustness value
    p_mle       Problem 1: a Poisson MLE, its model-based and sandwich SEs on twelve of the World's adults
    p_irls      Problem 2: Bliss's beetles, IRLS from zero, step by step
    p_reml      Problem 3: Longley, ML against REML for the error variance, and the bias by simulation
    p_hier      Problem 4: the eight schools, p(tau | y) and the shrunken effects
    p_mcmc      Problem 5: a two-mode target, four chains badly and well tuned, R-hat and ESS
    p_ic        Problem 6: ozone polynomials by AIC and BIC; how often each picks the truth as n grows
    p_kde       Problem 7: Old Faithful's waiting times, Silverman's rule against LSCV
    p_if        Problem 8: Newcomb's light, sensitivity curves of the mean, median and Huber's estimate
    p_kkt       Problem 9: the lasso on Stamey's prostate data, the KKT check, and a wrong solution that fails it
    p_bh        Problem 10: BH by hand on twelve p-values, then on 6,033 genes
    p_conf      Problem 11: a split conformal interval for New York's ozone, by hand
    p_km        Problem 12: Kaplan-Meier for the 6-MP arm with Greenwood's variance by hand
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import causal as CA
from explainer.stats.kit import mi as MI
from explainer.stats.world import World

CACHE = Cache("stats42")
load = CACHE.load

ALPHA = 0.1  # the Board's 90% intervals


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def eff_reps(per_rep, nominal=0.9) -> int:
    v = np.var(np.asarray(per_rep, float), ddof=1) / len(per_rep)
    if v == 0:
        return len(per_rep)
    return int(round(nominal * (1 - nominal) / max(v, 1e-12)))


# ===================================================================================================== Case 1
TAU1 = World.HEALTH_PROGRAMME_EFFECT
M_TRIAL = 50  # adults measured per town at follow-up
K_ARM = 21  # towns per arm in the plan


def oneway_icc(y, group) -> dict:
    """The one-way ANOVA estimator of the intraclass correlation for equal groups of size m."""
    y, group = np.asarray(y, float), np.asarray(group)
    ks = np.unique(group)
    m = len(y) // len(ks)
    means = np.array([y[group == k].mean() for k in ks])
    msb = m * means.var(ddof=1)
    msw = sum(((y[group == k] - y[group == k].mean()) ** 2).sum() for k in ks) / (len(y) - len(ks))
    s2b = max((msb - msw) / m, 0.0)
    return {"m": m, "k": len(ks), "means": means, "msb": float(msb), "msw": float(msw), "s2b": float(s2b),
            "icc": float(s2b / (s2b + msw)), "F": float(msb / msw)}


def compute_pilot():
    W = World()
    M = W.ministry
    r = oneway_icc(M["pilot_sbp"], M["pilot_town"])
    # a bootstrap over towns for the ICC's uncertainty
    g = rng(4201)
    y, tw = M["pilot_sbp"], M["pilot_town"]
    by = [y[tw == k] for k in range(r["k"])]
    boot = []
    for _ in range(400):
        pick = g.integers(0, r["k"], r["k"])
        yy = np.concatenate([by[k] for k in pick])
        gg = np.repeat(np.arange(r["k"]), r["m"])
        boot.append(oneway_icc(yy, gg)["icc"])
    true_icc = W.TOWN_SD ** 2 / (W.TOWN_SD ** 2 + W.PERSON_SD ** 2)
    trial_icc = (W.TOWN_SD ** 2 + W.TOWN_DRIFT ** 2) / (W.TOWN_SD ** 2 + W.TOWN_DRIFT ** 2 + W.PERSON_SD ** 2)
    sd_total = float(np.std(y, ddof=1))
    return {**r, "icc_ci": np.quantile(boot, [0.05, 0.95]), "true_icc": true_icc, "trial_icc": trial_icc,
            "sd_total": sd_total, "sd_within": math.sqrt(r["msw"]), "sd_between": math.sqrt(r["s2b"]),
            "mean": float(y.mean()), "n": len(y),
            "town_means": r["means"], "example_town": by[int(np.argmax(r["means"]))][:30],
            "true_u": M["u"]}


def n_per_arm(delta, sigma, alpha=0.05, power=0.8) -> float:
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return 2 * z ** 2 * sigma ** 2 / delta ** 2


def compute_size():
    p = load("pilot")
    icc = 0.055  # the planning value: the pilot's estimate, rounded up a little for the year's drift
    sigma = 16.5
    delta = abs(TAU1)
    n_ind = n_per_arm(delta, sigma)
    rows = []
    for m in [10, 20, 30, 50, 100, 200, 500]:
        de = 1 + (m - 1) * icc
        k = n_ind * de / m
        rows.append({"m": m, "de": de, "k": k, "k_t": math.ceil(k) + 1, "people": (math.ceil(k) + 1) * m})
    ms = np.unique(np.round(np.geomspace(5, 1000, 80)))
    k_curve = n_ind * (1 + (ms - 1) * icc) / ms
    k_inf = 2 * (stats.norm.ppf(0.975) + stats.norm.ppf(0.8)) ** 2 * icc * sigma ** 2 / delta ** 2

    # power against the number of towns per arm, for m = 50, from the normal approximation on cluster means (t df)
    ks = np.arange(4, 41)
    var_mean = sigma ** 2 * (icc + (1 - icc) / M_TRIAL)
    pw = []
    for k in ks:
        se = math.sqrt(2 * var_mean / k)
        df = 2 * k - 2
        tc = stats.t.ppf(0.975, df)
        pw.append(float(stats.nct.sf(tc, df, delta / se) + stats.nct.cdf(-tc, df, delta / se)))
    # ignoring clustering: the power one would claim
    pw_naive = [float(stats.norm.sf(1.96 - delta / math.sqrt(2 * sigma ** 2 / (k * M_TRIAL)))) for k in ks]
    return {"icc": icc, "sigma": sigma, "delta": delta, "n_ind": n_ind, "rows": rows, "ms": ms, "k_curve": k_curve,
            "k_inf": k_inf, "ks": ks, "power": pw, "power_naive": pw_naive, "pilot_icc": p["icc"],
            "de50": 1 + 49 * icc}


def trial_draw(g, k_arm=K_ARM, m=M_TRIAL, tau=TAU1, pilot_m=30, towns=None, W=None):
    """One trial from the law of the World's towns: town effects u (new each draw unless ``towns`` gives the World's
    own), the pilot means (30 adults), the trial-year means (m adults, drift added), and a complete randomization."""
    k = 2 * k_arm
    if towns is None:
        u = World.TOWN_SD * g.standard_normal(k)
        drift = World.TOWN_DRIFT * g.standard_normal(k)
        base = u + World.PERSON_SD * g.standard_normal((k, pilot_m)).mean(1)
    else:
        u, drift, base = towns
    z = np.zeros(k, bool)
    z[g.permutation(k)[:k_arm]] = True
    y = (u + drift + tau * z)[:, None] + World.PERSON_SD * g.standard_normal((k, m))
    return z, base, y


def analyse_trial(z, base, y, alpha=ALPHA):
    k, m = y.shape
    ybar = y.mean(1)
    # cluster-level t
    d = ybar[z].mean() - ybar[~z].mean()
    se = math.sqrt(ybar[z].var(ddof=1) / z.sum() + ybar[~z].var(ddof=1) / (~z).sum())
    tq = stats.t.ppf(1 - alpha / 2, k - 2)
    # cluster-level ANCOVA on the pilot mean
    X = np.column_stack([np.ones(k), z, base - base.mean()])
    b, *_ = np.linalg.lstsq(X, ybar, rcond=None)
    e = ybar - X @ b
    s2 = e @ e / (k - 3)
    V = s2 * np.linalg.inv(X.T @ X)
    se_a = math.sqrt(V[1, 1])
    ta = stats.t.ppf(1 - alpha / 2, k - 3)
    # naive individual-level difference
    yi, zi = y.ravel(), np.repeat(z, m)
    dn = yi[zi].mean() - yi[~zi].mean()
    sen = math.sqrt(yi[zi].var(ddof=1) / zi.sum() + yi[~zi].var(ddof=1) / (~zi).sum())
    zq = stats.norm.ppf(1 - alpha / 2)
    return {"t": (d, se, d - tq * se, d + tq * se), "ancova": (b[1], se_a, b[1] - ta * se_a, b[1] + ta * se_a),
            "naive": (dn, sen, dn - zq * sen, dn + zq * sen)}


def compute_plan():
    g = rng(4202)
    reps = 4000
    out = {"t": [], "ancova": [], "naive": []}
    rej = {"t": [], "ancova": [], "naive": []}
    rej0 = {"t": [], "ancova": [], "naive": []}
    for _ in range(reps):
        a = analyse_trial(*trial_draw(g), alpha=0.05)
        a0 = analyse_trial(*trial_draw(g, tau=0.0), alpha=0.05)
        for key in out:
            out[key].append(a[key][0])
            rej[key].append(a[key][3] < 0)
            rej0[key].append(a0[key][3] < 0 or a0[key][2] > 0)
    power = {k: float(np.mean(v)) for k, v in rej.items()}
    size = {k: float(np.mean(v)) for k, v in rej0.items()}
    sd = {k: float(np.std(v)) for k, v in out.items()}

    # the trial run in the World: 42 of its 200 towns drawn at random, then randomized
    W = World()
    M = W.ministry
    gw = rng(4203)
    pick = np.sort(gw.choice(200, 2 * K_ARM, replace=False))
    base = np.array([M["pilot_sbp"][M["pilot_town"] == j].mean() for j in pick]) - M["mu"]
    z, base_, y = trial_draw(gw, towns=(M["u"][pick], M["drift"][pick], base))
    res = analyse_trial(z, base_, y, alpha=0.05)
    ybar = y.mean(1)
    xy = W.towns["xy"][pick]
    return {"reps": reps, "power": power, "size": size, "sd": sd, "towns": pick, "xy": xy, "all_xy": W.towns["xy"],
            "z": z, "base": base + M["mu"], "ybar": ybar + M["mu"], "result": {k: list(v) for k, v in res.items()},
            "tau": TAU1}


# ===================================================================================================== Case 2
COVS = ["age", "male", "bmi", "log_income", "told_high"]


def _design(M, cols, data=None):
    d = data or M
    return np.column_stack([np.ones(len(M["sbp"]))] + [np.asarray(d[c], float) for c in cols])


def ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    n, p = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    meat = X.T @ (X * (e ** 2)[:, None])
    V = XtXi @ meat @ XtXi * n / (n - p)
    return b, np.sqrt(np.diag(V)), e, n - p


def aipw_fit(y, t, X):
    """AIPW with a logistic propensity and linear outcome models fitted in each arm, all in X (with intercept)."""
    ps = CA.propensity(X[:, 1:], t)
    ps = np.clip(ps, 0.01, 0.99)
    b1, *_ = np.linalg.lstsq(X[t], y[t], rcond=None)
    b0, *_ = np.linalg.lstsq(X[~t], y[~t], rcond=None)
    r = CA.aipw(y, t, X @ b0, X @ b1, ps, alpha=ALPHA)
    return r, ps


def obs_analysis(M, g, m_imp=20, want_detail=False):
    """Naive, CC adjusted, MI + AIPW and the bad controls on one survey."""
    y, t = np.asarray(M["sbp"], float), np.asarray(M["uptake"], bool)
    n = len(y)
    out = {}
    naive = CA.diff_means(y, t, alpha=ALPHA)
    out["naive"] = (naive["est"], naive["se"], naive["lo"], naive["hi"])
    obs = ~np.asarray(M["income_miss"], bool)
    # complete cases, AIPW
    Xc = _design(M, COVS)[obs]
    rc, _ = aipw_fit(y[obs], t[obs], Xc)
    out["cc_aipw"] = (rc["est"], rc["se"], rc["lo"], rc["hi"])
    # multiple imputation of log income from everything else, outcome and treatment included
    li = np.where(obs, M["log_income"], np.nan)
    Z = np.column_stack([M["age"], M["male"], M["bmi"], M["told_high"], t, y, t * y])
    ests, vars_ = [], []
    ests_bad = {"collider": [], "mediator": [], "regress": []}
    for _ in range(m_imp):
        li_k = MI.impute_norm(li, Z, g, "proper")
        d = {**M, "log_income": li_k}
        X = _design(M, COVS, d)
        r, ps = aipw_fit(y, t, X)
        ests.append(r["est"])
        vars_.append(r["se"] ** 2)
        if want_detail:
            b, se, _, _ = ols(y, np.column_stack([X, t]))
            ests_bad["regress"].append((b[-1], se[-1] ** 2))
            b, se, _, _ = ols(y, np.column_stack([X, t, M["visited"]]))
            ests_bad["collider"].append((b[-2], se[-2] ** 2))
            b, se, _, _ = ols(y, np.column_stack([X, t, M["potassium"]]))
            ests_bad["mediator"].append((b[-2], se[-2] ** 2))
    rr = MI.rubin(ests, vars_, level=1 - ALPHA)
    out["mi_aipw"] = (rr["est"], rr["se"], rr["ci"][0], rr["ci"][1])
    out["fmi"] = rr["fmi"]
    if want_detail:
        for k, v in ests_bad.items():
            v = np.array(v)
            rk = MI.rubin(v[:, 0], v[:, 1], level=1 - ALPHA)
            out[k] = (rk["est"], rk["se"], rk["ci"][0], rk["ci"][1])
    return out


def compute_obs():
    W = World()
    M = dict(W.ministry)
    for k in ["male", "told_high", "uptake", "visited", "income_miss"]:
        M[k] = np.asarray(M[k], bool)
    y, t = M["sbp"], M["uptake"]
    g = rng(4204)
    res = obs_analysis(M, g, m_imp=40, want_detail=True)
    # overlap, balance and the regression for the robustness value, on one completed data set (an analyst's view)
    obs_i = ~M["income_miss"]
    Z = np.column_stack([M["age"], M["male"], M["bmi"], M["told_high"], t, y, t * y])
    li1 = MI.impute_norm(np.where(obs_i, M["log_income"], np.nan), Z, rng(4215), "proper")
    M1 = {**M, "log_income": li1}
    X = _design(M, COVS, M1)
    ps = np.clip(CA.propensity(X[:, 1:], t), 0.01, 0.99)
    w = np.where(t, 1 / ps, 1 / (1 - ps))
    names = ["age", "male", "BMI", "log income", "told high"]
    smd_raw = [CA.smd(np.asarray(M1[c], float), t) for c in COVS]
    smd_w = [CA.smd(np.asarray(M1[c], float), t, w) for c in COVS]
    # who the users are
    table = []
    for c, nm in zip(COVS, names):
        v = np.asarray(M1[c], float)
        table.append((nm, float(v[t].mean()), float(v[~t].mean())))
    # the regression's t for the robustness value, and told_high as a benchmark (partial R^2 with T and Y)
    b, se, e, dof = ols(y, np.column_stack([X, t]))
    t_stat = b[-1] / se[-1]
    rv = CA.robustness_value(t_stat, dof)
    rv_a = CA.robustness_value(t_stat, dof, alpha=0.05)
    # benchmark: told_high's partial R^2 with the outcome (given the rest) and with uptake (given the rest)
    others = [c for c in COVS if c != "told_high"]
    Xo = _design(M, others, M1)
    bt, set_, _, doft = ols(y, np.column_stack([Xo, t, M["told_high"]]))
    r2y = CA.partial_r2(bt[-1] / set_[-1], doft)
    btt, sett, _, doftt = ols(t.astype(float), np.column_stack([Xo, M["told_high"]]))
    r2d = CA.partial_r2(btt[-1] / sett[-1], doftt)
    # the true-income analysis, the World's privilege
    rt, _ = aipw_fit(y, t, _design(M, COVS))
    return {"n": len(y), "n_users": int(t.sum()), "share_users": float(t.mean()), "income_miss": float(M["income_miss"].mean()),
            "res": res, "true_aipw": (rt["est"], rt["se"], rt["lo"], rt["hi"]), "tau": World.SUBSTITUTE_EFFECT,
            "ps": ps, "t": t, "smd_raw": smd_raw, "smd_w": smd_w, "names": names, "table": table,
            "ols": (float(b[-1]), float(se[-1])), "t_stat": float(t_stat), "dof": int(dof), "rv": rv, "rv_a": rv_a,
            "bench_r2y": r2y, "bench_r2d": r2d, "y_mean_users": float(y[t].mean()), "y_mean_non": float(y[~t].mean()),
            "visited": [float(M["visited"][t].mean()), float(M["visited"][~t].mean())],
            "potassium": [float(M["potassium"][t].mean()), float(M["potassium"][~t].mean())],
            "miss_by": {"users": float(M["income_miss"][t].mean()), "non": float(M["income_miss"][~t].mean()),
                        "young": float(M["income_miss"][M["age"] < 40].mean()),
                        "old": float(M["income_miss"][M["age"] >= 60].mean())}}


# ===================================================================================================== problems
def compute_p_mle():
    W = World()
    v = W.visits["visits"]
    pool = np.flatnonzero(v >= 0)
    g = rng(4205)
    y = np.sort(v[g.choice(pool, 12, replace=False)]).astype(float)
    n = len(y)
    lam = y.mean()
    ss = float(((y - lam) ** 2).sum())
    se_model = math.sqrt(lam / n)
    se_sand = math.sqrt(ss) / n
    grid = np.linspace(0.3, max(8.0, lam * 2.5), 200)
    ll = y.sum() * np.log(grid) - n * grid
    pop = v[pool].astype(float)
    return {"y": y, "n": n, "lam": lam, "ss": ss, "se_model": se_model, "se_sand": se_sand, "grid": grid, "ll": ll,
            "sumy": float(y.sum()), "info": n / lam, "pop_mean": float(pop.mean()), "pop_var": float(pop.var()),
            "dispersion": float(pop.var() / pop.mean())}


def compute_p_irls():
    x, n, k = museum.bliss()
    p_obs = k / n
    X = np.column_stack([np.ones(len(x)), x])
    b = np.zeros(2)
    hist = []
    for it in range(8):
        eta = X @ b
        mu = 1 / (1 + np.exp(-eta))
        w = n * mu * (1 - mu)
        zz = eta + (p_obs - mu) / (mu * (1 - mu))
        XtWX = X.T @ (w[:, None] * X)
        XtWz = X.T @ (w * zz)
        ll = float(np.sum(k * np.log(mu) + (n - k) * np.log(1 - mu)))
        hist.append({"b": b.copy(), "ll": ll, "w": w, "z": zz, "XtWX": XtWX, "XtWz": XtWz})
        b = np.linalg.solve(XtWX, XtWz)
    mu = 1 / (1 + np.exp(-(X @ b)))
    ll_final = float(np.sum(k * np.log(mu) + (n - k) * np.log(1 - mu)))
    cov = np.linalg.inv(X.T @ ((n * mu * (1 - mu))[:, None] * X))
    ld50 = -b[0] / b[1]
    return {"x": x, "n": n, "k": k, "p": p_obs, "hist": hist, "b": b, "ll": ll_final, "se": np.sqrt(np.diag(cov)),
            "ld50": float(ld50), "ld50_dose": float(10 ** ld50)}


def compute_p_reml():
    D, y, names = museum.longley()
    n, p = D.shape
    b, *_ = np.linalg.lstsq(D, y, rcond=None)
    rss = float(((y - D @ b) ** 2).sum())
    s2_ml, s2_reml = rss / n, rss / (n - p)
    grid = np.linspace(0.3 * s2_ml, 4.0 * s2_reml, 300)
    ll_ml = -n / 2 * np.log(grid) - rss / (2 * grid)
    ll_reml = -(n - p) / 2 * np.log(grid) - rss / (2 * grid)
    # the bias by simulation, at sigma^2 = s2_reml with Longley's design
    g = rng(4206)
    reps = 20000
    mu = D @ b
    E = math.sqrt(s2_reml) * g.standard_normal((reps, n))
    H = D @ np.linalg.pinv(D)
    R = E - E @ H.T
    r = (R ** 2).sum(1)
    return {"n": n, "p": p, "rss": rss, "s2_ml": s2_ml, "s2_reml": s2_reml, "grid": grid, "ll_ml": ll_ml - ll_ml.max(),
            "ll_reml": ll_reml - ll_reml.max(), "sim_ml": float((r / n).mean()), "sim_reml": float((r / (n - p)).mean()),
            "true_s2": s2_reml, "ml_hist": np.histogram(r / n, bins=40, range=(0, 3 * s2_reml)),
            "reml_hist": np.histogram(r / (n - p), bins=40, range=(0, 3 * s2_reml)), "y_name": "employment"}


def compute_p_hier():
    from explainer.stats.kit import bayes as BA

    names, y, s = museum.eight_schools()
    tau = np.linspace(0.0, 30.0, 601)
    h = BA.hier_normal(y, s, tau)
    dens = np.asarray(h.post_tau)
    w = dens / dens.sum()
    mu_hat, v_mu = np.asarray(h.mu_hat), np.asarray(h.v_mu)
    # E[theta_j | y] = sum_tau p(tau|y) E[theta_j | tau, y]; E[theta_j | tau, y] uses E[mu | tau, y] = mu_hat(tau)
    th = np.zeros(len(y))
    for i in range(len(y)):
        with np.errstate(divide="ignore", invalid="ignore"):
            prec = 1 / s[i] ** 2 + np.where(tau > 0, 1 / tau ** 2, np.inf)
            m = np.where(tau > 0, (y[i] / s[i] ** 2 + mu_hat / np.maximum(tau, 1e-12) ** 2) / prec, mu_hat)
        th[i] = float((w * m).sum())
    shrink_at = {}
    for t0 in [5.0, 10.0]:
        j = int(np.argmin(np.abs(tau - t0)))
        B = s ** 2 / (s ** 2 + t0 ** 2)
        shrink_at[str(t0)] = {"B": B, "mu": float(mu_hat[j]), "theta": (1 - B) * y + B * mu_hat[j]}
    cdf = np.cumsum(w)
    return {"names": names, "y": y, "s": s, "tau": tau, "dens": dens, "theta": th, "mu_post": float((w * mu_hat).sum()),
            "tau_mean": float((w * tau).sum()), "tau_median": float(tau[np.searchsorted(cdf, 0.5)]),
            "tau_q90": float(tau[np.searchsorted(cdf, 0.9)]), "shrink": shrink_at,
            "pooled": float(np.sum(y / s ** 2) / np.sum(1 / s ** 2)), "pooled_se": float(1 / math.sqrt(np.sum(1 / s ** 2)))}


def compute_p_mcmc():
    from explainer.stats.kit import ppl as PP

    def logp(q):
        x = q[0]
        return float(np.logaddexp(-0.5 * (x + 3) ** 2, -0.5 * (x - 3) ** 2))

    starts = [-6.0, -2.0, 2.0, 6.0]
    out = {}
    for name, step, seed in [("bad", 0.4, 4207), ("good", 4.0, 4208)]:
        g = rng(seed)
        chains, acc = [], []
        for s0 in starts:
            r = PP.rwm(logp, [s0], step, 2000, g)
            chains.append(r["draws"][:, 0])
            acc.append(float(r["accept"].mean()))
        C = np.array(chains)[:, 1000:]
        out[name] = {"step": step, "trace": np.array(chains)[:, ::4], "rhat": PP.rhat(C), "ess_bulk": PP.ess_bulk(C),
                     "ess_tail": PP.ess_tail(C), "accept": float(np.mean(acc)), "means": C.mean(1),
                     "share_right": float((C > 0).mean())}
    return out


def compute_p_ic():
    A = museum.airquality()
    x, y = A["temp"], A["ozone"]
    n = len(y)
    xs = (x - x.mean()) / x.std()
    rows = []
    for d in range(1, 6):
        D = np.column_stack([xs ** j for j in range(d + 1)])
        b, *_ = np.linalg.lstsq(D, y, rcond=None)
        rss = float(((y - D @ b) ** 2).sum())
        k = d + 2  # coefficients and the variance
        ll = -n / 2 * (math.log(2 * math.pi * rss / n) + 1)
        rows.append({"d": d, "k": k, "ll": ll, "aic": -2 * ll + 2 * k, "bic": -2 * ll + k * math.log(n), "b": b})
    grid = np.linspace(x.min(), x.max(), 100)
    gs = (grid - x.mean()) / x.std()
    fits = {}
    for r in rows:
        fits[str(r["d"])] = sum(r["b"][j] * gs ** j for j in range(r["d"] + 1))
    # the selection simulation: a true quadratic, candidates 1..6
    g = rng(4209)
    ns = [20, 40, 80, 160, 320, 640, 1280, 2560]
    p_aic, p_bic, over_aic = [], [], []
    for nn in ns:
        ca = cb = oa = 0
        reps = 600
        for _ in range(reps):
            u = g.uniform(-1, 1, nn)
            yy = 1.0 + 0.5 * u + 0.6 * u ** 2 + g.standard_normal(nn)
            aics, bics = [], []
            for d in range(1, 7):
                D = np.column_stack([u ** j for j in range(d + 1)])
                b, *_ = np.linalg.lstsq(D, yy, rcond=None)
                rss = float(((yy - D @ b) ** 2).sum())
                ll = -nn / 2 * (math.log(2 * math.pi * rss / nn) + 1)
                aics.append(-2 * ll + 2 * (d + 2))
                bics.append(-2 * ll + math.log(nn) * (d + 2))
            ca += int(np.argmin(aics) == 1)
            cb += int(np.argmin(bics) == 1)
            oa += int(np.argmin(aics) > 1)
        p_aic.append(ca / reps)
        p_bic.append(cb / reps)
        over_aic.append(oa / reps)
    return {"n": n, "rows": rows, "x": x, "y": y, "grid": grid, "fits": fits, "ns": ns, "p_aic": p_aic, "p_bic": p_bic,
            "over_aic": over_aic, "chi2_tail": float(stats.chi2.sf(2, 1))}


def compute_p_kde():
    from explainer.stats.kit import smooth as SM

    _, x = museum.faithful()
    n = len(x)
    s = float(x.std(ddof=1))
    iqr = float(stats.iqr(x))
    h_s = SM.silverman_h(x)
    hs = np.linspace(1.0, 10.0, 181)
    cv = [SM.lscv(x, h) for h in hs]
    h_cv = float(hs[int(np.argmin(cv))])
    grid = np.linspace(35, 105, 300)
    return {"n": n, "s": s, "iqr": iqr, "a": min(s, iqr / 1.349), "h_s": h_s, "h_cv": h_cv, "hs": hs, "cv": cv,
            "grid": grid, "f_s": SM.kde(x, grid, h_s), "f_cv": SM.kde(x, grid, h_cv), "f_big": SM.kde(x, grid, 3 * h_s),
            "hist": np.histogram(x, bins=28, range=(40, 100), density=True), "n_fifth": n ** -0.2}


def compute_p_if():
    from explainer.stats.kit import robust as RO

    x = museum.newcomb()
    n = len(x)
    grid = np.linspace(-60, 80, 281)
    s_huber = RO.mad(x)
    est_h = lambda v: RO.m_location(v, "huber", scale=s_huber)["mu"]  # noqa: E731
    sc = {"mean": RO.sensitivity_curve(np.mean, x, grid), "median": RO.sensitivity_curve(np.median, x, grid),
          "huber": RO.sensitivity_curve(est_h, x, grid)}
    keep = x > -20
    return {"x": x, "n": n, "grid": grid, "sc": sc, "mean": float(x.mean()), "median": float(np.median(x)),
            "huber": est_h(x), "mean_clean": float(x[keep].mean()), "var": float(x.var()),
            "var_clean": float(x[keep].var()), "mad": s_huber, "outliers": x[~keep],
            "if_var_at_out": [float((v - x.mean()) ** 2 - x.var()) for v in x[~keep]]}


def compute_p_kkt():
    from explainer.stats.kit import sparse as SP

    X, y, train, names = museum.prostate()
    tr = np.asarray(train, bool)
    X, y = X[tr], y[tr]
    n = len(y)
    Xs = (X - X.mean(0)) / X.std(0)
    yc = y - y.mean()
    lam = 0.10
    b = np.asarray(SP.lasso_cd(Xs, yc, lam))
    k = SP.kkt(Xs, yc, b, lam)
    # a colleague's "solution": OLS soft-thresholded once (not a lasso solution when X is correlated)
    bo, *_ = np.linalg.lstsq(Xs, yc, rcond=None)
    bw = np.sign(bo) * np.maximum(np.abs(bo) - lam, 0)
    kw = SP.kkt(Xs, yc, bw, lam)
    return {"n": n, "names": names, "lam": lam, "b": b, "grad": k["grad"], "on_err": k["on_err"], "off_max": k["off_max"],
            "bw": bw, "grad_w": kw["grad"], "on_err_w": kw["on_err"], "off_max_w": kw["off_max"],
            "corr_max": float(np.max(np.abs(np.corrcoef(Xs.T) - np.eye(8))))}


def compute_p_bh():
    p = np.array([0.0002, 0.0011, 0.0039, 0.0082, 0.0123, 0.0217, 0.0401, 0.0458, 0.1720, 0.3010, 0.6540, 0.8820])
    m, q = len(p), 0.1
    line = q * np.arange(1, m + 1) / m
    r = None
    from explainer.stats.kit import multiple as MU

    r = MU.bh(p, q)
    bonf = int((p <= q / m).sum())
    z = np.asarray(museum.prostate_z()[1], float)
    pz = 2 * stats.norm.sf(np.abs(z))
    rz = MU.bh(pz, q)
    adj = MU.adjust(p, "bh")
    srt = np.sort(pz)[:400]
    return {"p": p, "m": m, "q": q, "line": line, "k": r["k"], "thr": r["threshold"], "bonf": bonf, "adj": adj,
            "genes": len(z), "genes_k": rz["k"], "genes_thr": rz["threshold"], "genes_bonf": int((pz <= q / len(z)).sum()),
            "genes_sorted": srt}


def compute_p_conf():
    A = museum.airquality()
    x, y = A["temp"], A["ozone"]
    g = rng(4210)
    n = len(y)
    perm = g.permutation(n)
    tr, cal, te = perm[:37], perm[37:74], perm[74:]
    D = lambda v: np.column_stack([np.ones(len(v)), v])  # noqa: E731
    b, *_ = np.linalg.lstsq(D(x[tr]), y[tr], rcond=None)
    r = np.abs(y[cal] - D(x[cal]) @ b)
    k = math.ceil((len(cal) + 1) * 0.9)
    q = float(np.sort(r)[k - 1])
    pred_te = D(x[te]) @ b
    cover = float(np.mean(np.abs(y[te] - pred_te) <= q))
    # the toy: nine calibration residuals, alpha = 0.2
    toy = np.array([2.1, 0.4, 3.3, 1.2, 5.8, 0.9, 2.7, 1.6, 4.4])
    kt = math.ceil((len(toy) + 1) * 0.8)
    qt = float(np.sort(toy)[kt - 1])
    x0 = 85.0
    return {"b": b, "x": x, "y": y, "tr": tr, "cal": cal, "te": te, "r": np.sort(r), "k": k, "q": q, "n_cal": len(cal),
            "cover": cover, "toy": toy, "kt": kt, "qt": qt, "x0": x0, "pred0": float(b[0] + b[1] * x0)}


def compute_p_km():
    from explainer.stats.kit import survival as SV

    G = museum.gehan()
    t, e, grp = G["time"], G["event"], G["group"]
    km = SV.kaplan_meier(t[grp == 1], e[grp == 1])
    km0 = SV.kaplan_meier(t[grp == 0], e[grp == 0])
    rows = []
    for i in range(len(km["t"])):
        if km["d"][i] > 0:
            rows.append({"t": float(km["t"][i]), "n": float(km["n"][i]), "d": float(km["d"][i]), "s": float(km["surv"][i]),
                         "gw": float(km["greenwood"][i]), "se": float(km["se"][i]),
                         "lo": float(km["loglog"][0][i]), "hi": float(km["loglog"][1][i])})
    lr = SV.logrank(t, e, grp)
    return {"time": t[grp == 1], "event": e[grp == 1], "time0": t[grp == 0], "event0": e[grp == 0], "rows": rows,
            "median0": SV.km_median(km0), "median1": SV.km_median(km), "logrank": {k: v for k, v in lr.items() if np.isscalar(v)}}


# ===================================================================================================== Board
def compute_board():
    rows = []
    # Case 1: the cluster trial
    g = rng(4211)
    reps = 4000
    cov = {"t": [], "ancova": [], "naive": []}
    for _ in range(reps):
        a = analyse_trial(*trial_draw(g))
        for k in cov:
            cov[k].append(a[k][2] <= TAU1 <= a[k][3])
    rows.append(Row(42, "individual-level t, cluster trial", "42 towns x 50 adults, ICC 0.054", "coverage", 0.9,
                    float(np.mean(cov["naive"])), eff_reps(cov["naive"])))
    rows.append(Row(42, "cluster-level t", "42 towns x 50 adults, ICC 0.054", "coverage", 0.9,
                    float(np.mean(cov["t"])), eff_reps(cov["t"])))
    rows.append(Row(42, "cluster-level ANCOVA on the pilot", "42 towns x 50 adults, ICC 0.054", "coverage", 0.9,
                    float(np.mean(cov["ancova"])), eff_reps(cov["ancova"])))

    # Case 2: the survey from the law of the World's adults
    W = World()
    base = W.ministry
    pool = np.flatnonzero(W.adult)
    a_all = W.age.astype(float)
    li_all = np.log(np.where(W.adult, W.income, 1.0))
    mu_li, sd_li = float(li_all[W.adult].mean()), float(li_all[W.adult].std())
    g = rng(4212)
    reps2 = 400
    cn, cc, cm, cb = [], [], [], []
    for _ in range(reps2):
        idx = g.choice(pool, World.SUBSTITUTE_N, replace=False)
        n = len(idx)
        age, male, bmi = a_all[idx], W.male[idx], W.health["bmi"][idx]
        li = li_all[idx]
        zi = (li - mu_li) / sd_li
        M = World.substitute_draw(g, age, male, bmi, zi, W.health["told_high"][idx], W.health["sbp"][idx])
        M["log_income"] = li
        t, y, visited, miss = M["uptake"], M["sbp"], M["visited"], M["income_miss"]
        told = M["told_high"]
        r = obs_analysis(M, g, m_imp=10, want_detail=False)
        tau = World.SUBSTITUTE_EFFECT
        cn.append(r["naive"][2] <= tau <= r["naive"][3])
        cc.append(r["cc_aipw"][2] <= tau <= r["cc_aipw"][3])
        cm.append(r["mi_aipw"][2] <= tau <= r["mi_aipw"][3])
        X = np.column_stack([np.ones(n), age, male, bmi, li, told])  # every income seen: the collider's bias alone
        b, se, _, dof = ols(y, np.column_stack([X, t, visited]))
        q = stats.t.ppf(1 - ALPHA / 2, dof)
        cb.append(b[-2] - q * se[-2] <= tau <= b[-2] + q * se[-2])
    st = "3,000 adults, income MAR for over a third"
    rows.append(Row(42, "naive difference in means", st, "coverage", 0.9, float(np.mean(cn)), eff_reps(cn)))
    rows.append(Row(42, "regression adjusting for a collider", st, "coverage", 0.9, float(np.mean(cb)), eff_reps(cb)))
    rows.append(Row(42, "AIPW on complete cases", st, "coverage", 0.9, float(np.mean(cc)), eff_reps(cc)))
    rows.append(Row(42, "AIPW with multiple imputation", st, "coverage", 0.9, float(np.mean(cm)), eff_reps(cm)))

    # Problem 1: the mean visits, model-based Poisson SE vs the sandwich, n = 200 from the World
    v = W.visits["visits"]
    vp = v[v >= 0].astype(float)
    mu = float(vp.mean())
    g = rng(4213)
    reps3 = 4000
    cmod, csand = [], []
    z = stats.norm.ppf(1 - ALPHA / 2)
    for _ in range(reps3):
        yy = vp[g.integers(0, len(vp), 500)]
        lam = yy.mean()
        sm = math.sqrt(lam / 500)
        ss = math.sqrt(((yy - lam) ** 2).sum()) / 500
        cmod.append(abs(lam - mu) <= z * sm)
        csand.append(abs(lam - mu) <= z * ss)
    rows.append(Row(42, "Poisson MLE, model-based SE", "the World's doctor visits, n = 500", "coverage", 0.9,
                    float(np.mean(cmod)), eff_reps(cmod)))
    rows.append(Row(42, "Poisson MLE, sandwich SE", "the World's doctor visits, n = 500", "coverage", 0.9,
                    float(np.mean(csand)), eff_reps(csand)))

    # Problem 11: split conformal for the World's pressure from age and BMI
    ad = np.flatnonzero(W.adult)
    sbp, age, bmi = W.health["sbp"], W.age.astype(float), W.health["bmi"]
    g = rng(4214)
    reps4 = 4000
    cv = []
    for _ in range(reps4):
        idx = g.choice(ad, 300, replace=False)
        tr, cal, te = idx[:200], idx[200:299], idx[299:]
        D = lambda j: np.column_stack([np.ones(len(j)), age[j], age[j] ** 2, bmi[j]])  # noqa: E731
        b, *_ = np.linalg.lstsq(D(tr), sbp[tr], rcond=None)
        r = np.abs(sbp[cal] - D(cal) @ b)
        q = np.sort(r)[math.ceil(100 * 0.9) - 1]
        cv.append(bool(abs(sbp[te][0] - (D(te) @ b)[0]) <= q))
    rows.append(Row(42, "split conformal, 99 calibration points", "the World's pressure from age and BMI", "coverage", 0.9,
                    float(np.mean(cv)), eff_reps(cv)))
    save_rows(42, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "pilot": compute_pilot, "size": compute_size, "plan": compute_plan, "obs": compute_obs,
    "p_mle": compute_p_mle, "p_irls": compute_p_irls, "p_reml": compute_p_reml, "p_hier": compute_p_hier,
    "p_mcmc": compute_p_mcmc, "p_ic": compute_p_ic, "p_kde": compute_p_kde, "p_if": compute_p_if,
    "p_kkt": compute_p_kkt, "p_bh": compute_p_bh, "p_conf": compute_p_conf, "p_km": compute_p_km,
    "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
