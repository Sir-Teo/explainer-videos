"""Precompute every number in Part 23 of *Statistics, Built* ("The Linear Model in Depth").

    python -m videos.stats.stats23.compute            # everything missing (several minutes)
    python -m videos.stats.stats23.compute --force board

Results are cached in ``.cache/stats23/<name>.json``.  Longley's data and Hubble's nebulae are the Museum's; families,
incomes and schools are the World's; the rest are seeded simulations.

Items:
    longley     digits from the normal equations and from QR, in single and double precision; condition numbers
    glh         the general linear hypothesis on the World's families: equal parents, and a joint value
    gls         a trend with AR(1) errors: OLS, GLS and Prais-Winsten, their spreads and interval coverage
    hc          heteroskedasticity at n = 30: classical, HC0, HC1, HC2, HC3 coverage, by leverage
    schools     one sample of 40 schools: the programme effect with iid and cluster SEs; the Moulton factor
    blp         income on age in the World: the best linear predictor, and which SEs cover it
    eiv         attenuation by noisy fathers; Hubble's nebulae by OLS, reverse regression and Deming
    qreg        quantile regression of the World's incomes on age, with sandwich and bootstrap SEs
    splines     bases, knots and cross-validation for income on age
    influence   DFBETAS and the jackknife on Hubble's nebulae
    board       Coverage Board rows
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import ols as O
from explainer.stats.kit import optim
from explainer.stats.world import World

CACHE = Cache("stats23")
load = CACHE.load
W = World()


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



def wild_cluster_boot(X, y, groups, j, b0=0.0, R=999, weights="webb", g=None):
    """Restricted CR1 bootstrap-t, using cluster sufficient statistics.

    The +1 correction prevents zero Monte Carlo p-values. It does not make
    a few-cluster bootstrap exact. Draw order matches explicit refitting.
    """
    X, y, groups = np.asarray(X, float), np.asarray(y, float), np.asarray(groups)
    if X.ndim != 2 or y.shape != (len(X),) or groups.shape != y.shape:
        raise ValueError("incompatible design, response, or group shapes")
    n, p = X.shape
    if n <= p or p < 2 or not 0 <= j < p or R < 1 or int(R) != R:
        raise ValueError("need n > p >= 2, a valid coefficient and positive integer R")
    if not np.isfinite(X).all() or not np.isfinite(y).all() or not np.isfinite(b0):
        raise ValueError("finite data and null required")
    if np.linalg.matrix_rank(X) != p:
        raise ValueError("full-rank design required")
    if weights not in ("webb", "rademacher"):
        raise ValueError("weights must be webb or rademacher")
    labels, idx = np.unique(groups, return_inverse=True)
    G = len(labels)
    if G < 2:
        raise ValueError("at least two independent clusters required")
    g = rng(0) if g is None else g
    f = O.fit(X, y)
    obs_se = np.sqrt(O.cluster_cov(f, groups)[j, j])
    if not obs_se > 0:
        raise ValueError("positive observed cluster variance required")
    t_obs = (f.coef[j] - b0) / obs_se
    er = O.fit(np.delete(X, j, axis=1), y - b0 * X[:, j]).resid
    score = np.zeros((G, p))
    gram = np.zeros((G, p, p))
    np.add.at(score, idx, X * er[:, None])
    np.add.at(gram, idx, X[:, :, None] * X[:, None, :])
    w = g.choice(O.WEBB if weights == "webb" else [-1., 1.], size=(int(R), G))
    delta = (w @ score) @ f.XtX_inv
    # Project each cluster's bootstrap score onto the coefficient's bread row.
    a = f.XtX_inv[j]
    u = w * (score @ a)[None, :] - delta @ np.einsum('gij,j->gi', gram, a).T
    variance = np.sum(u ** 2, axis=1) * G / (G - 1) * (n - 1) / (n - p)
    if np.any(variance <= 0):
        raise ValueError("degenerate bootstrap cluster variance")
    ts = delta[:, j] / np.sqrt(variance)
    extreme = int(np.count_nonzero((np.abs(ts) >= abs(t_obs)) | np.isclose(np.abs(ts), abs(t_obs), rtol=1e-12, atol=1e-12)))
    return {"t": float(t_obs), "p": (1 + extreme) / (R + 1), "t_boot": ts}


def stationary_prais_winsten(X, y, iters=20, rho_bound=0.999):
    """Iterated PW constrained to the stated stationary AR(1) model.

    Record every constrained update rather than silently taking sqrt(1-rho²)
    outside its domain. This safeguard is a numerical modelling choice.
    """
    X, y = np.asarray(X, float), np.asarray(y, float)
    b, rho, constrained = O.fit(X, y).coef, 0., 0
    for _ in range(iters):
        e = y - X @ b
        raw = float(e[1:] @ e[:-1] / (e[:-1] @ e[:-1]))
        new = float(np.clip(raw, -rho_bound, rho_bound))
        constrained += int(raw != new)
        scale = np.sqrt(1 - new ** 2)
        f = O.fit(np.vstack([scale * X[:1], X[1:] - new * X[:-1]]),
                  np.r_[scale * y[:1], y[1:] - new * y[:-1]])
        b = f.coef
        done = abs(new - rho) < 1e-10
        rho = new
        if done:
            break
    return {"fit": f, "rho": rho, "coef": b, "constrained_updates": constrained}


def qreg_score_se(X, y, tau, coef):
    """Kernel bread and empirical score meat for a possibly misspecified line.

    With a correctly specified continuous conditional quantile the meat
    simplifies to tau(1-tau) X'X. LP ties use the strict-negative convention;
    finitely many active constraints are negligible in the stated asymptotics.
    """
    X, y = np.asarray(X, float), np.asarray(y, float)
    r = y - X @ coef
    n = len(y)
    z, q = stats.norm.ppf(.975), stats.norm.ppf(tau)
    hs = n ** (-1 / 3) * z ** (2 / 3) * (1.5 * stats.norm.pdf(q) ** 2 / (2 * q ** 2 + 1)) ** (1 / 3)
    h = (stats.norm.ppf(min(tau + hs, .999)) - stats.norm.ppf(max(tau - hs, .001))) * min(np.std(r), stats.iqr(r) / 1.34)
    if not h > 0:
        raise ValueError("positive residual bandwidth required")
    D = X.T @ (X * ((abs(r) <= h) / (2 * h))[:, None])
    Di = np.linalg.inv(D)
    score = X * (tau - (r < 0))[:, None]
    return np.sqrt(np.diag(Di @ (score.T @ score) @ Di))


def training_knots(age, K):
    """Distinct interior quantile knots, fitted to training predictors only."""
    knots = np.unique(np.quantile(age, np.linspace(0, 1, K + 2)[1:-1])) if K else np.array([])
    return knots[(knots > 18) & (knots < 85)]


def precise_least_squares(X, y):
    """90-digit solution for the exact supplied binary64 inputs, not their generator."""
    import mpmath as mp
    with mp.workdps(90):
        A = mp.matrix([[mp.mpf(float(v)) for v in row] for row in X])
        c = mp.matrix([mp.mpf(float(v)) for v in y])
        return np.array([float(v) for v in mp.lu_solve(A.T * A, A.T * c)])


def compute_longley():
    X, y, names = museum.longley()
    cert = np.asarray(museum.LONGLEY_CERTIFIED)
    out = {"names": names, "certified": cert, "X": X, "y": y}
    for tag, dt in (("32", np.float32), ("64", np.float64)):
        ne = O.normal_equations(X, y, dt)
        out[f"ne{tag}"] = ne["coef"]
        out[f"ne{tag}_route"] = ne["route"]
        out[f"ne{tag}_digits"] = O.correct_digits(ne["coef"], cert)
        q = O.qr_solve(X, y, dt)
        out[f"qr{tag}"] = q
        out[f"qr{tag}_digits"] = O.correct_digits(q, cert)
    Z = X.copy()
    Z[:, 1:] = (X[:, 1:] - X[:, 1:].mean(0)) / X[:, 1:].std(0)
    ne_s = O.normal_equations(Z, y, np.float32)["coef"]
    b_s = O.qr_solve(Z, y, np.float64)
    out.update({"cond_X": float(np.linalg.cond(X)), "cond_XtX": float(np.linalg.cond(X) ** 2), "cond_rounded_gram": float(np.linalg.cond(X.T @ X)),
                "cond_scaled": float(np.linalg.cond(Z)), "corr": np.corrcoef(X[:, 1:].T),
                "ne32_scaled_digits": O.correct_digits(ne_s, b_s), "vif": O.vif(X),
                "eps32": float(np.finfo(np.float32).eps), "eps64": float(np.finfo(np.float64).eps)})
    return nest(out)


def family_sample(n, seed):
    fam = W.families
    g = rng(seed)
    i = g.choice(len(fam["child"]), n, replace=False)
    return fam["z_father"][i], fam["z_mother"][i], fam["z_child"][i]


def compute_glh():
    zf, zm, zc = family_sample(400, 2301)
    X = O.design(zf, zm)
    f = O.fit(X, zc)
    eq = O.glh(f, [[0, 1, -1]])
    joint = O.glh(f, [[0, 1, 0], [0, 0, 1]], [0.35, 0.35])
    zero = O.glh(f, [[0, 1, 0], [0, 0, 1]])
    restricted = O.fit(O.design(zf + zm), zc)  # beta_f = beta_m: one slope on the sum
    F_rss = ((restricted.rss - f.rss) / 1) / (f.rss / f.df)
    V = f.cov()[1:, 1:]
    # the 95% joint confidence ellipse for (beta_f, beta_m)
    c = 2 * stats.f.ppf(0.95, 2, f.df)
    t = np.linspace(0, 2 * np.pi, 200)
    L = np.linalg.cholesky(V)
    ell = f.coef[1:, None] + np.sqrt(c) * L @ np.vstack([np.cos(t), np.sin(t)])
    return nest({"n": 400, "coef": f.coef, "se": f.se(), "eq": eq, "joint": joint, "zero": zero, "F_rss": float(F_rss),
                 "rss": f.rss, "rss_restricted": restricted.rss, "ellipse": ell, "truth": [0.35, 0.35]})


def trend_data(n, rho, g):
    t = np.arange(n) / n
    X = O.design(t)
    e = np.empty(n)
    e[0] = g.normal() / np.sqrt(1 - rho ** 2)
    for i in range(1, n):
        e[i] = rho * e[i - 1] + g.normal()
    return X, X @ [10.0, 2.0] + e


def compute_gls():
    g = rng(1935)
    n, rho, R = 60, 0.8, 2000
    ex_X, ex_y = trend_data(n, rho, rng(35))
    Om = O.ar1_omega(n, rho)
    b_ols, b_gls, b_pw = [], [], []
    hit = {"ols": 0, "nw": 0, "pw": 0, "gls": 0}
    se_naive = []
    constrained_updates = 0
    for _ in range(R):
        X, y = trend_data(n, rho, g)
        f = O.fit(X, y)
        fg = O.gls(X, y, Om)
        pw = stationary_prais_winsten(X, y)
        b_ols.append(f.coef[1])
        b_gls.append(fg.coef[1])
        b_pw.append(pw["coef"][1])
        constrained_updates += pw["constrained_updates"]
        se_naive.append(f.se()[1])
        z = stats.t.ppf(0.975, n - 2)
        hit["ols"] += abs(f.coef[1] - 2) <= z * f.se()[1]
        hit["nw"] += abs(f.coef[1] - 2) <= z * np.sqrt(O.hac_cov(f, 6)[1, 1])
        hit["pw"] += abs(pw["coef"][1] - 2) <= z * pw["fit"].se()[1]
        hit["gls"] += abs(fg.coef[1] - 2) <= z * fg.se()[1]
    exf = O.fit(ex_X, ex_y)
    return nest({"n": n, "rho": rho, "R": R, "t": ex_X[:, 1], "y": ex_y, "ols_line": exf.coef,
                 "sd_ols": float(np.std(b_ols)), "sd_gls": float(np.std(b_gls)), "sd_pw": float(np.std(b_pw)),
                 "mean_naive_se": float(np.mean(se_naive)), "coverage": {k: v / R for k, v in hit.items()},
                 "rho_hat_example": float(exf.resid[1:] @ exf.resid[:-1] / (exf.resid[:-1] @ exf.resid[:-1])),
                 "dw_example": float(np.sum(np.diff(exf.resid)**2) / exf.rss),
                 "pw_rho_example": stationary_prais_winsten(ex_X, ex_y)["rho"],
                 "pw_constrained_updates": constrained_updates, "pw_rho_bound": .999})


def hc_data(n, g):
    x = g.lognormal(0, 0.5, n)
    y = 1 + 2 * x + x * g.normal(size=n)  # SD proportional to x: the big-x points are the noisy ones
    return O.design(x), y


def compute_hc():
    g = rng(1980)
    n, R = 30, 4000
    kinds = ["classical", "HC0", "HC1", "HC2", "HC3"]
    hit = {k: 0 for k in kinds}
    hit["wild"] = 0
    maxlev = []
    ex = hc_data(n, rng(1985))
    for r in range(R):
        X, y = hc_data(n, g)
        f = O.fit(X, y)
        maxlev.append(f.leverage.max())
        q = stats.t.ppf(0.975, f.df)
        for k in kinds:
            hit[k] += abs(f.coef[1] - 2) <= q * f.se(k)[1]
        if r < 1000:
            hit["wild"] += wild_cluster_boot(X, y, np.arange(n), 1, 2.0, R=399, weights="rademacher", g=g)["p"] > 0.05
    R_by_method = {k: (1000 if k == "wild" else R) for k in hit}
    fe = O.fit(*ex)
    return nest({"n": n, "R": R, "R_by_method": R_by_method, "coverage": {k: v / R_by_method[k] for k, v in hit.items()}, "x": ex[0][:, 1], "y": ex[1],
                 "lev": fe.leverage, "resid": fe.resid, "coef": fe.coef, "se": {k: fe.se(k)[1] for k in kinds},
                 "median_maxlev": float(np.median(maxlev)), "p_over_n": 2 / n})


def school_sample(G, g):
    s = W.schools
    pick = np.sort(g.choice(W.N_SCHOOLS, G, replace=False))
    m = np.isin(s["school"], pick)
    sch = s["school"][m]
    X = O.design(s["programme"][sch].astype(float), s["ses"][m])
    return X, s["score"][m], sch


def compute_schools():
    g = rng(2323)
    X, y, sch = school_sample(40, g)
    f = O.fit(X, y)
    V = O.cluster_cov(f, sch)
    m_bar = len(y) / 40
    rho_e = O.icc(f.resid, sch)
    rho_x = O.icc(X[:, 1], sch)
    s = W.schools
    per = [(float(y[sch == k].mean()), bool(X[sch == k, 1][0]), int(np.sum(sch == k))) for k in np.unique(sch)]
    return nest({"G": 40, "n": len(y), "coef": f.coef, "se_iid": f.se(), "se_cr1": np.sqrt(np.diag(V)),
                 "m_bar": m_bar, "rho_e": rho_e, "rho_x": rho_x, "moulton": O.moulton(m_bar, rho_x, rho_e),
                 "ratio": float(np.sqrt(V[1, 1]) / f.se()[1]), "truth": 100 * W.SCHOOL_PROGRAMME_EFFECT, "per_school": per,
                 "icc_world": O.icc(s["score"], s["school"])})


def compute_blp():
    ad = W.adult & (W.age <= 75)
    age = W.age[ad].astype(float)
    inc = W.income[ad] / 1000
    pop = O.fit(O.design(age), inc)  # the population best linear predictor: the World is finite
    ages = np.arange(18, 76)
    means = np.array([inc[age == a].mean() for a in ages])
    young = (age <= 40)
    pop_young = O.fit(O.design(age[young]), inc[young])
    g = rng(2019)
    n, R = 200, 2000
    pool = np.flatnonzero(ad)
    hit = {"classical": 0, "HC3": 0}
    ex = None
    for r in range(R):
        i = g.choice(len(age), n, replace=False)
        f = O.fit(O.design(age[i]), inc[i])
        q = stats.t.ppf(0.975, f.df)
        for k in hit:
            hit[k] += abs(f.coef[1] - pop.coef[1]) <= q * f.se(k)[1]
        if r == 0:
            ex = {"age": age[i], "inc": inc[i], "coef": f.coef, "se": f.se()[1], "se_hc3": f.se("HC3")[1]}
    del pool
    # Buja et al.'s point in its plainest form: a curved truth, x random; the line's target is the BLP (slope 0)
    gt = rng(2020)
    toy = {"classical": 0, "HC3": 0}
    for _ in range(R):
        x = gt.normal(size=100)
        yy = x ** 2 + 0.3 * gt.normal(size=100)
        f = O.fit(O.design(x), yy)
        qq = stats.t.ppf(0.975, f.df)
        for k in toy:
            toy[k] += abs(f.coef[1]) <= qq * f.se(k)[1]
    xt = rng(21).normal(size=100)
    yt = xt ** 2 + 0.3 * rng(22).normal(size=100)
    return nest({"toy": {k: v / R for k, v in toy.items()}, "toy_x": xt, "toy_y": yt, "toy_fit": O.fit(O.design(xt), yt).coef,
                 "ages": ages, "means": means, "blp": pop.coef, "blp_young": pop_young.coef, "n": n, "R": R,
                 "coverage": {k: v / R for k, v in hit.items()}, "example": ex})


def compute_eiv():
    d, v = museum.hubble()
    ols = O.fit(O.design(d), v)
    rev = O.fit(O.design(v), d)
    dem = O.deming(d, v, delta=1.0)
    # Deming with an assumed error SD ratio: velocities +-100 km/s, distances +-20%
    lam = (100 / (0.2 * d.mean())) ** 2
    dem2 = O.deming(d, v, delta=lam)
    origin = O.fit(d[:, None], v)
    # attenuation: fathers' heights measured with error (reliability 0.6)
    fam = W.families
    g = rng(1888)
    n = 500
    i = g.choice(len(fam["child"]), n, replace=False)
    zf, zc = fam["z_father"][i], fam["z_child"][i]
    true_slope = float(O.fit(O.design(fam["z_father"]), fam["z_child"]).coef[1])
    rel = 0.6
    su2 = float(np.var(fam["z_father"])) * (1 - rel) / rel
    wf = zf + np.sqrt(su2) * g.normal(size=n)
    f_true = O.fit(O.design(zf), zc)
    f_noisy = O.fit(O.design(wf), zc)
    # SIMEX (Cook & Stefanski 1994): add extra error of variance lam * su2, watch the slope fall, extrapolate to -1
    lams = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    gs = rng(1994)
    simex = [float(f_noisy.coef[1])] + [float(np.mean([O.fit(O.design(wf + np.sqrt(l * su2) * gs.normal(size=n)), zc).coef[1]
                                                       for _ in range(200)])) for l in lams[1:]]
    quad = np.polyfit(lams, simex, 2)
    return nest({"d": d, "v": v, "ols": ols.coef, "ols_se": ols.se(), "reverse_slope": float(1 / rev.coef[1]),
                 "reverse_line": [float(-rev.coef[0] / rev.coef[1]), float(1 / rev.coef[1])], "deming1": dem,
                 "deming2": dem2, "lam": lam, "origin": float(origin.coef[0]), "r": float(np.corrcoef(d, v)[0, 1]),
                 "modern_H0": 70.0, "fam_zf": zf[:200], "fam_wf": wf[:200], "fam_zc": zc[:200], "true_slope": true_slope,
                 "coef_exact": f_true.coef, "coef_noisy": f_noisy.coef, "measurement_error_variance": su2,
                 "slope_exact": float(f_true.coef[1]), "slope_noisy": float(f_noisy.coef[1]), "reliability": rel,
                 "simex_lams": lams, "simex": simex, "simex_quad": quad, "simex_est": float(np.polyval(quad, -1.0)),
                 "predicted": true_slope * rel})


def compute_qreg():
    ad = W.adult & (W.age >= 25) & (W.age <= 64)
    pool = np.flatnonzero(ad)
    g = rng(1978)
    i = g.choice(pool, 1000, replace=False)
    age, inc = W.age[i].astype(float), W.income[i] / 1000
    X = O.design(age)
    out = {"age": age[:500], "inc": inc[:500], "taus": [0.1, 0.25, 0.5, 0.75, 0.9], "fits": []}
    for tau in out["taus"]:
        b = optim.quantile_lp(X, inc, tau)["b"]
        se = qreg_score_se(X, inc, tau, b)
        boot = []
        gb = rng(int(1000 * tau))
        for _ in range(100):
            j = gb.integers(0, len(inc), len(inc))
            boot.append(optim.quantile_lp(X[j], inc[j], tau)["b"][1])
        out["fits"].append({"tau": tau, "b": b, "se": se, "boot_se": float(np.std(boot, ddof=1))})
    ols = O.fit(X, inc)
    out["ols"] = ols.coef
    out["ols_se"] = ols.se("HC3")
    ages = np.arange(25, 65)
    allage, allinc = W.age[ad].astype(float), W.income[ad] / 1000
    out["true_q"] = {str(t): [float(np.quantile(allinc[allage == a], t)) for a in ages] for t in out["taus"]}
    out["ages"] = ages
    return nest(out)


def compute_splines():
    ad = W.adult & (W.age <= 85)
    pool = np.flatnonzero(ad)
    g = rng(1946)
    i = g.choice(pool, 800, replace=False)
    age, inc = W.age[i].astype(float), np.log(W.income[i])
    grid = np.linspace(18, 85, 200)
    allage, allinc = W.age[ad].astype(float), np.log(W.income[ad])
    ages = np.arange(18, 86)
    truth = np.array([allinc[allage == a].mean() for a in ages])
    fits = {}
    for K in (1, 3, 6, 20):
        knots = training_knots(age, K)
        B = O.bspline_basis(age, knots, lo=18, hi=85)
        f = O.fit(B, inc)
        fits[str(K)] = {"knots": knots, "effective_K": len(knots), "curve": O.bspline_basis(grid, knots, lo=18, hi=85) @ f.coef}
    cv, fold_errors, effective_K = [], [], []
    folds = np.array_split(g.permutation(len(age)), 10)
    for K in range(0, 26):
        err, counts = [], []
        for te in folds:
            tr = np.setdiff1d(np.arange(len(age)), te)
            knots = training_knots(age[tr], K)
            counts.append(len(knots))
            Btr = O.bspline_basis(age[tr], knots, lo=18, hi=85)
            b = np.linalg.lstsq(Btr, inc[tr], rcond=None)[0]
            err.append(np.mean((inc[te] - O.bspline_basis(age[te], knots, lo=18, hi=85) @ b) ** 2))
        cv.append(float(np.mean(err)))
        fold_errors.append(err)
        effective_K.append(counts)
    cv_se = np.std(fold_errors, axis=1, ddof=1) / np.sqrt(len(folds))
    best_K = int(np.argmin(cv))
    oneSE_K = int(np.flatnonzero(np.asarray(cv) <= cv[best_K] + cv_se[best_K])[0])
    knots3 = training_knots(age, 3)
    basis = O.bspline_basis(grid, knots3, lo=18, hi=85)
    tp = O.truncated_power(grid, knots3)
    return nest({"age": age, "inc": inc, "grid": grid, "fits": fits, "cv": cv, "best_K": best_K, "oneSE_K": oneSE_K, "cv_se": cv_se, "fold_errors": fold_errors, "effective_K_by_fold": effective_K,
                 "basis": basis.T, "tp": tp.T, "knots3": knots3, "ages": ages, "truth": truth,
                 "cond_bs": float(np.linalg.cond(O.bspline_basis(age, knots3, lo=18, hi=85))),
                 "cond_tp": float(np.linalg.cond(O.truncated_power(age, knots3)))})


def compute_influence():
    d, v = museum.hubble()
    X = O.design(d)
    f = O.fit(X, v)
    dfb = O.dfbetas(f)
    J = O.jackknife_coefs(X, v)
    n = len(v)
    jack_se = np.sqrt((n - 1) / n * np.sum((J - J.mean(0)) ** 2, 0))
    k = int(np.argmax(np.abs(dfb[:, 1])))
    keep = np.arange(n) != k
    return nest({"dfbetas": dfb[:, 1], "leverage": f.leverage, "cooks": f.cooks, "jack_slopes": J[:, 1],
                 "jack_se": jack_se, "se": f.se(), "se_hc3": f.se("HC3"), "most": k, "slope": f.coef[1],
                 "slope_without": float(O.fit(X[keep], v[keep]).coef[1]), "cut": 2 / np.sqrt(n)})


def compute_glh_null():
    """Exact conditional Gaussian F null on one fixed World-family design."""
    g = rng(2302)
    zf, zm, _ = family_sample(400, 2301)
    X = O.design(zf, zm)
    Fs = []
    for _ in range(2000):
        y = X @ [0., .35, .35] + g.normal(size=len(X))
        Fs.append(O.glh(O.fit(X, y), [[0, 1, -1]])["F"])
    Fs = np.asarray(Fs)
    return nest({"F": Fs, "R": len(Fs), "model": "fixed family design; fresh iid N(0,1) errors under equal-parent null", "reject": float(np.mean(Fs > stats.f.ppf(.95, 1, 397))), "crit": float(stats.f.ppf(.95, 1, 397))})


def compute_kappa():
    """Correct digits against the condition number: normal equations (Cholesky) vs Householder QR, double precision,
    for designs with prescribed singular values, with and without a residual."""
    g = rng(1965)
    n, p = 50, 4
    logk = np.linspace(1, 12, 23)
    out = {"logk": logk, "ne": [], "qr": [], "qr_resid": [], "ne_failures": [], "reference": "90-digit least squares of supplied binary64 X and y"}
    for lk in logk:
        ne, qr, qrr = [], [], []
        failures = 0
        for _ in range(5):
            U = np.linalg.qr(g.normal(size=(n, p)))[0]
            V = np.linalg.qr(g.normal(size=(p, p)))[0]
            X = U @ np.diag(np.logspace(0, -lk, p)) @ V.T
            b = np.ones(p)
            y = X @ b
            ref = precise_least_squares(X, y)
            try:
                ne.append(np.median(O.correct_digits(O.normal_equations(X, y)["coef"], ref)))
            except np.linalg.LinAlgError:
                ne.append(0.)
                failures += 1
            qr.append(np.median(O.correct_digits(O.qr_solve(X, y), ref)))
            # Construct an approximately orthogonal residual; then solve the rounded inputs independently.
            r = g.normal(size=n)
            r -= U @ (U.T @ r)
            yr = y + 1e-3 * r / np.linalg.norm(r) * np.linalg.norm(y)
            qrr.append(np.median(O.correct_digits(O.qr_solve(X, yr), precise_least_squares(X, yr))))
        out["ne_failures"].append(failures)
        out["ne"].append(float(np.median(ne)))
        out["qr"].append(float(np.median(qr)))
        out["qr_resid"].append(float(np.median(qrr)))
    return nest(out)


def compute_masking():
    """Three outliers mask one another; compare single deletions with deleting the group."""
    g = rng(1980)
    x = np.concatenate([g.uniform(0, 10, 20), [15.0, 15.2, 15.4]])
    y = np.concatenate([2 + 0.5 * x[:20] + g.normal(0, 0.7, 20), [0.5, 0.7, 0.9]])
    X = O.design(x)
    f = O.fit(X, y)
    dfb = O.dfbetas(f)[:, 1]
    keep = np.arange(len(x)) < 20
    return nest({"x": x, "y": y, "coef": f.coef, "dfbetas": dfb, "coef_clean": O.fit(X[keep], y[keep]).coef,
                 "coef_drop1": O.fit(np.delete(X, 20, 0), np.delete(y, 20)).coef, "cut": 2 / np.sqrt(len(x)),
                 "cooks": f.cooks})


def compute_board():
    g = rng(2324)
    R = 1000
    truth = 100 * W.SCHOOL_PROGRAMME_EFFECT
    q = stats.norm.ppf(0.975)
    # (1, 2) 40 schools: iid vs CR1
    iid = cr = 0
    for _ in range(R):
        X, y, sch = school_sample(40, g)
        f = O.fit(X, y)
        iid += abs(f.coef[1] - truth) <= stats.t.ppf(0.975, f.df) * f.se()[1]
        cr += abs(f.coef[1] - truth) <= stats.t.ppf(0.975, 39) * np.sqrt(O.cluster_cov(f, sch)[1, 1])
    # (3, 4) 8 schools: CR1 with t(G - 1) vs the wild cluster bootstrap
    R8 = 500
    cr8 = wcb = redraws = 0
    for _ in range(R8):
        X, y, sch = school_sample(8, g)
        while X[:, 1].min() == X[:, 1].max():  # condition on both treatment arms
            redraws += 1
            X, y, sch = school_sample(8, g)
        f = O.fit(X, y)
        cr8 += abs(f.coef[1] - truth) <= stats.t.ppf(0.975, 7) * np.sqrt(O.cluster_cov(f, sch)[1, 1])
        wcb += wild_cluster_boot(X, y, sch, 1, truth, R=399, g=g)["p"] > 0.05
    # (5) the naive slope under errors in variables, reliability 0.6, n = 500
    fam = W.families
    true_slope = float(O.fit(O.design(fam["z_father"]), fam["z_child"]).coef[1])
    eiv = 0
    for _ in range(R):
        i = g.choice(len(fam["child"]), 500, replace=False)
        w = fam["z_father"][i] + np.sqrt(np.var(fam["z_father"]) * 0.4 / 0.6) * g.normal(size=500)
        f = O.fit(O.design(w), fam["z_child"][i])
        eiv += abs(f.coef[1] - true_slope) <= q * f.se()[1]
    # (6, 7) heteroskedastic, n = 30: HC0 vs HC3
    hc0 = hc3 = wild = 0
    for _ in range(R):
        X, y = hc_data(30, g)
        f = O.fit(X, y)
        tq = stats.t.ppf(0.975, f.df)
        hc0 += abs(f.coef[1] - 2) <= tq * f.se("HC0")[1]
        hc3 += abs(f.coef[1] - 2) <= tq * f.se("HC3")[1]
        wild += wild_cluster_boot(X, y, np.arange(30), 1, 2.0, R=399, weights="rademacher", g=g)["p"] > 0.05
    rows = [
        Row(23, r"iid SE, school programme", r"40 schools, \ pupils clustered", "coverage", 0.95, iid / R, R),
        Row(23, r"cluster-robust SE (CR1)", r"40 schools", "coverage", 0.95, cr / R, R),
        Row(23, r"cluster-robust SE (CR1)", r"8 schools, both arms, \ $t_7$", "coverage", 0.95, cr8 / R8, R8),
        Row(23, r"wild cluster bootstrap", r"8 schools, both arms, \ Webb weights", "coverage", 0.95, wcb / R8, R8),
        Row(23, r"naive slope, \ noisy regressor", r"reliability 0.6, \ $n = 500$", "coverage", 0.95, eiv / R, R),
        Row(23, r"HC0 SE", r"heteroskedastic, \ $n = 30$", "coverage", 0.95, hc0 / R, R),
        Row(23, r"HC3 SE", r"heteroskedastic, \ $n = 30$", "coverage", 0.95, hc3 / R, R),
        Row(23, r"wild bootstrap-$t$", r"heteroskedastic, \ $n = 30$", "coverage", 0.95, wild / R, R),
    ]
    save_rows(23, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "school8_one_arm_redraws": redraws, "school8_sampling": "conditional on both arms", "bootstrap_mc_p": "(1 + extreme) / (R + 1)"}


ITEMS = {
    "longley": compute_longley, "glh": compute_glh, "gls": compute_gls, "hc": compute_hc, "schools": compute_schools,
    "blp": compute_blp, "eiv": compute_eiv, "qreg": compute_qreg, "splines": compute_splines,
    "influence": compute_influence, "glh_null": compute_glh_null, "kappa": compute_kappa,
    "masking": compute_masking, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)


def clipped_segments(xs, ys, rectangle):
    """Intersect segments with the viewport, preserving crossings and missing breaks."""
    xmin, xmax, ymin, ymax = rectangle
    points = np.column_stack((xs, ys))
    result = []
    for start, end in zip(points[:-1], points[1:]):
        if not np.isfinite([start, end]).all():
            continue
        delta = end-start
        lo, hi = 0., 1.
        for j, lower, upper in ((0, xmin, xmax), (1, ymin, ymax)):
            if delta[j] == 0:
                if not lower <= start[j] <= upper:
                    hi = -1
                    break
            else:
                a, b = sorted(((lower-start[j])/delta[j], (upper-start[j])/delta[j]))
                lo, hi = max(lo, a), min(hi, b)
        if lo <= hi:
            result.append((start+lo*delta, start+hi*delta))
    return result
