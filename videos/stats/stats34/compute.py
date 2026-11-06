"""Precompute every number in Part 34 of *Statistics, Built* ("Prediction with Guarantees").

    python -m videos.stats.stats34.compute            # everything missing (ten minutes or so)
    python -m videos.stats.stats34.compute --force board

Results are cached in ``.cache/stats34/<name>.json``.  The breast cancer data (Wolberg, Street & Mangasarian 1995),
the irises and the diabetes data are the Museum's; incomes and votes are the World's; the rest are seeded
simulations, most on Friedman's (1991) test function.

Items:
    rashomon    bootstrap trees on the breast cancer data: equal accuracy, different stories
    forest      one tree, bagging, a forest on breast cancer; OOB vs test; impurity vs permutation importance
    variance    Friedman 1: a tree's variance sigma^2 and the correlation rho between trees, by mtry
    ij          a forest's infinitesimal-jackknife interval at one point, and its coverage of E f(x0) and mu(x0)
    boost       L2 boosting on Friedman 1: shrinkage nu = 0.1 vs 1
    cv          what cross-validation estimates (Bates, Hastie & Tibshirani 2024): CV vs Err_XY vs Err
    calib       breast cancer: naive Bayes, a forest, logistic; reliability; Platt, isotonic, temperature
    lemma       the quantile lemma: ranks of a new score; coverage given the calibration set ~ Beta
    split       World incomes by age: split conformal (constant width) vs CQR, coverage by age group
    jack        Barber et al.'s (2021) near-interpolation regime: naive, jackknife, jackknife+, split
    diab        CV+ with a forest on the diabetes data
    shift       covariate shift in age: unweighted vs weighted conformal
    aci         a stream with a volatility break: static split conformal vs adaptive conformal
    sets        prediction sets: APS on the irises (sepals only) and on breast cancer; class-conditional coverage
    ppi         the World's mean blood pressure from 300 clinic visits and 20,000 smartwatch guesses: classical, naive, PPI, PPI++
    interp      a forest on Friedman 1 with a twin feature: PDP, permutation importance, LOCO, Shapley at a point
    board       Coverage Board rows
"""

from __future__ import annotations

import itertools
import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import conformal as CF
from explainer.stats.kit import optim as OP
from explainer.stats.kit import ppi as PPI
from explainer.stats.world import World

CACHE = Cache("stats34")
load = CACHE.load


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


# ----------------------------------------------------------------------------------------------------------- helpers


def friedman1_mu(X):
    X = np.asarray(X, float)
    return 10 * np.sin(np.pi * X[:, 0] * X[:, 1]) + 20 * (X[:, 2] - 0.5) ** 2 + 10 * X[:, 3] + 5 * X[:, 4]


def friedman1(n, g, p=10, sigma=1.0):
    X = g.random((n, p))
    return X, friedman1_mu(X) + sigma * g.standard_normal(n)


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -40, 40)))


def logistic_fit(X, y, ridge=1e-6, iters=60):
    Z = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(Z.shape[1])
    for _ in range(iters):
        p = sigmoid(Z @ w)
        g = Z.T @ (y - p) - ridge * np.r_[0, w[1:]]
        H = Z.T @ (Z * (p * (1 - p))[:, None]) + ridge * np.diag(np.r_[0, np.ones(len(w) - 1)])
        step = np.linalg.solve(H, g)
        w += step
        if np.max(np.abs(step)) < 1e-9:
            break
    return w


def logistic_logit(w, X):
    return np.column_stack([np.ones(len(X)), X]) @ w


def gnb_logit(Xtr, ytr, X):
    """Gaussian naive Bayes' log odds of class 1: features treated as independent given the class."""
    out = np.full(len(X), math.log(ytr.mean() / (1 - ytr.mean())))
    for j in range(Xtr.shape[1]):
        for c, sgn in ((1, 1), (0, -1)):
            m, s = Xtr[ytr == c, j].mean(), Xtr[ytr == c, j].std() + 1e-9
            out += sgn * stats.norm.logpdf(X[:, j], m, s)
    return out


def standardize_pair(Xtr, *others):
    m, s = Xtr.mean(0), Xtr.std(0) + 1e-12
    return [(Xtr - m) / s] + [(o - m) / s for o in others]


def world_adults(seed, n):
    w = World()
    g = rng(seed)
    idx = np.flatnonzero(w.adult)
    take = g.choice(idx, n, replace=False)
    return w, take


def poly_age(a):
    """A cubic in age, plus a step at the retirement age (67)."""
    a = np.asarray(a, float)
    t = (a - 50) / 20
    return np.column_stack([t, t ** 2, t ** 3, (a >= 67).astype(float)])


# ----------------------------------------------------------------------------------------------------------- items


def compute_rashomon():
    """Fifty bootstrap samples of the breast cancer data; a depth-3 tree on each.  Their test accuracies are all about
    the same; the feature at the root, and the top three by importance, are not."""
    X, y, names = museum.breast_cancer()
    g = rng(34)
    perm = g.permutation(len(y))
    te, tr = perm[:169], perm[169:]
    roots, accs, tops = [], [], []
    for b in range(50):
        s = g.choice(tr, len(tr), replace=True)
        t = CF.fit_tree(X[s], y[s].astype(float), max_depth=3, min_leaf=5, rng=g)
        acc = float(np.mean((t.predict(X[te]) > 0.5) == y[te]))
        roots.append(int(t.feature[0]))
        accs.append(acc)
        tops.append([int(j) for j in np.argsort(-t.gain)[:3]])
    cnt = np.bincount(roots, minlength=X.shape[1])
    order = np.argsort(-cnt)
    # three logistic models on disjoint pairs of features, nearly the same accuracy
    pairs = [(7, 22), (27, 20), (23, 21)]
    plog = []
    for a, b in pairs:
        Xs, Xt = standardize_pair(X[tr][:, [a, b]], X[te][:, [a, b]])
        w = logistic_fit(Xs, y[tr].astype(float))
        plog.append({"features": [names[a], names[b]], "acc": float(np.mean((logistic_logit(w, Xt) > 0) == y[te])),
                     "coef": w[1:].tolist()})
    return nest({"names": names, "root_counts": cnt, "order": order[:8], "acc": accs, "acc_mean": float(np.mean(accs)),
                 "acc_sd": float(np.std(accs)), "n_distinct_roots": int((cnt > 0).sum()),
                 "distinct_top3": len({tuple(sorted(t)) for t in tops}), "pairs": plog,
                 "first_trees": [{"root": names[roots[k]], "acc": accs[k]} for k in range(6)]})


def compute_forest():
    X, y, names = museum.breast_cancer()
    g = rng(341)
    yf = y.astype(float)
    # add two noise features: a continuous one and a coin
    Xn = np.column_stack([X, g.standard_normal(len(y)), g.integers(0, 2, len(y)).astype(float)])
    nm = list(names) + ["noise (continuous)", "noise (coin)"]
    perm = g.permutation(len(y))
    te, tr = perm[:169], perm[169:]
    tree = CF.fit_tree(Xn[tr], yf[tr], max_depth=30, min_leaf=1, rng=g)
    acc_tree = float(np.mean((tree.predict(Xn[te]) > 0.5) == y[te]))
    bag = CF.Forest(Xn[tr], yf[tr], B=300, mtry=Xn.shape[1], min_leaf=1, rng=g)
    rf = CF.Forest(Xn[tr], yf[tr], B=300, mtry=int(round(math.sqrt(Xn.shape[1]))), min_leaf=1, rng=g)
    Pb, Pr = bag.tree_preds(Xn[te]), rf.tree_preds(Xn[te])
    Bs = [1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200, 300]
    err_b = [float(np.mean((Pb[:B].mean(0) > 0.5) != y[te])) for B in Bs]
    err_r = [float(np.mean((Pr[:B].mean(0) > 0.5) != y[te])) for B in Bs]
    pt = rf.predict(Xn[te])
    pi = int(np.argmin(np.abs(pt - 0.83)))
    oob = rf.oob()
    oob_err = float(np.nanmean((oob > 0.5) != y[tr]))
    imp = rf.impurity_importance()
    pim = rf.permutation_importance(Xn[te], yf[te], rng=g, reps=10)
    top = np.argsort(-imp)[:8]
    return nest({"acc_tree": acc_tree, "acc_bag": 1 - err_b[-1], "acc_rf": 1 - err_r[-1], "Bs": Bs, "err_bag": err_b,
                 "err_rf": err_r, "oob_err": oob_err, "test_err": err_r[-1], "names": nm, "imp": imp, "perm": pim,
                 "top": top, "noise_imp": imp[-2:], "noise_perm": pim[-2:],
                 "noise_imp_rank": [int(np.sum(imp > imp[-2]) + 1), int(np.sum(imp > imp[-1]) + 1)],
                 "noise_perm_rank": [int(np.sum(pim > pim[-2]) + 1), int(np.sum(pim > pim[-1]) + 1)],
                 "tree_leaves": int(np.sum(tree.feature < 0)), "mtry": rf.mtry, "p": Xn.shape[1],
                 "patient_p": float(pt[pi]), "patient_y": int(y[te][pi])})


def compute_variance():
    """sigma^2(x): the variance of one tree's prediction at x (over training sets and the trees' own randomness);
    rho(x): the correlation between two trees of the same forest.  Var(forest of B) = rho sigma^2 + (1 - rho) sigma^2 / B."""
    g = rng(342)
    Xt, _ = friedman1(200, g)
    mu = friedman1_mu(Xt)
    out = {}
    R, B = 40, 40
    for mtry in (10, 5, 3, 1):
        T = np.zeros((R, B, len(Xt)))
        for r in range(R):
            X, y = friedman1(300, g)
            f = CF.Forest(X, y, B=B, mtry=mtry, min_leaf=3, rng=g)
            T[r] = f.tree_preds(Xt)
        s2 = T.reshape(R * B, -1).var(0)
        within = T.var(1).mean(0)  # E_r Var_b
        between_cov = s2 - within  # Cov between two trees of one forest = Var_r(E_b)
        rho = float(np.mean(between_cov) / np.mean(s2))
        forest_pred = T.mean(1)
        mse = float(np.mean((forest_pred - mu[None, :]) ** 2))
        bias2 = float(np.mean((forest_pred.mean(0) - mu) ** 2))
        out[str(mtry)] = {"sigma2": float(np.mean(s2)), "rho": rho, "forest_var": float(np.mean(forest_pred.var(0))),
                          "mse": mse, "bias2": bias2}
    Bgrid = [1, 2, 5, 10, 20, 50, 100, 200, 500]
    curves = {k: [v["rho"] * v["sigma2"] + (1 - v["rho"]) * v["sigma2"] / b for b in Bgrid] for k, v in out.items()}
    return nest({"by_mtry": out, "Bgrid": Bgrid, "curves": curves, "R": R, "B": B})


def _ij_rep(g, x0, B=500, n=250, subsample=None):
    X, y = friedman1(n, g)
    f = CF.Forest(X, y, B=B, mtry=3, min_leaf=5, rng=g, subsample=subsample)
    pred = float(f.predict(x0)[0])
    v = float(f.ij_variance(x0)[0])
    return pred, v


def compute_ij_sub():
    """The same, with Wager & Athey's (2018) subsampled forests: each tree on 50 of the 250 points, without
    replacement, 2,000 trees."""
    g = rng(3431)
    x0 = np.full((1, 10), 0.5)
    x0[0, :5] = [0.8, 0.8, 0.5, 0.9, 0.9]
    mu0 = float(friedman1_mu(x0)[0])
    reps = 300
    res = np.array([_ij_rep(g, x0, B=2000, subsample=50) for _ in range(reps)])
    extra = np.array([_ij_rep(g, x0, B=2000, subsample=50)[0] for _ in range(100)])
    preds, se = res[:, 0], np.sqrt(res[:, 1])
    Ef = float(np.mean(np.r_[preds, extra]))
    z = stats.norm.ppf(0.95)
    return nest({"mu0": mu0, "Ef": Ef, "bias": Ef - mu0, "sd_pred": float(np.std(np.r_[preds, extra])),
                 "mean_se": float(np.mean(se)), "cov_E": float(np.mean(np.abs(preds - Ef) <= z * se)),
                 "cov_mu": float(np.mean(np.abs(preds - mu0) <= z * se)), "reps": reps, "s": 50, "B": 2000,
                 "first": [{"pred": float(p), "se": float(s)} for p, s in zip(preds[:30], se[:30])]})


def compute_ij():
    g = rng(343)
    x0 = np.full((1, 10), 0.5)
    x0[0, :5] = [0.8, 0.8, 0.5, 0.9, 0.9]  # a peak of the surface: the forest under-reaches it
    mu0 = float(friedman1_mu(x0)[0])
    reps = 300
    res = np.array([_ij_rep(g, x0) for _ in range(reps)])
    preds, vs = res[:, 0], res[:, 1]
    # E f(x0), from the replications themselves plus 200 more
    extra = np.array([_ij_rep(g, x0)[0] for _ in range(200)])
    Ef = float(np.mean(np.r_[preds, extra]))
    z = stats.norm.ppf(0.95)
    se = np.sqrt(vs)
    cov_E = float(np.mean(np.abs(preds - Ef) <= z * se))
    cov_mu = float(np.mean(np.abs(preds - mu0) <= z * se))
    return nest({"x0": x0[0], "mu0": mu0, "Ef": Ef, "bias": Ef - mu0, "sd_pred": float(np.std(np.r_[preds, extra])),
                 "mean_se": float(np.mean(se)), "cov_E": cov_E, "cov_mu": cov_mu, "reps": reps,
                 "first": [{"pred": float(p), "se": float(s)} for p, s in zip(preds[:30], se[:30])]})


def compute_boost():
    g = rng(344)
    X, y = friedman1(400, g)
    Xt, yt = friedman1(3000, g)
    out = {}
    for nu in (1.0, 0.1):
        r = CF.l2_boost(X, y, M=600, nu=nu, depth=2, min_leaf=5, Xtest=Xt, ytest=yt)
        out[str(nu)] = {"train": r["train"], "test": r["test"], "best_m": int(np.argmin(r["test"]) + 1),
                        "best": float(np.min(r["test"])), "final": float(r["test"][-1])}
    rf = CF.Forest(X, y, B=300, mtry=3, min_leaf=3, rng=g)
    rf_mse = float(np.mean((rf.predict(Xt) - yt) ** 2))
    # stagewise on one variable: the first few fits of the additive model to x4 (the linear term) in 1-D
    x = np.linspace(0, 1, 120)
    yy = 10 * x + 2 * np.sin(6 * x)
    stage = []
    F = np.full_like(x, yy.mean())
    Xs = x[:, None]
    for m in range(12):
        t = CF.fit_tree(Xs, yy - F, max_depth=1, min_leaf=3)
        F = F + 0.3 * t.predict(Xs)
        stage.append(F.copy())
    return nest({"by_nu": out, "rf_mse": rf_mse, "noise_var": 1.0, "stage_x": x, "stage_y": yy, "stages": stage})


def compute_cv():
    """Bates, Hastie & Tibshirani (2024): with OLS on n = 100, p = 20, sigma = 1, Gaussian X, the conditional error
    Err_XY = sigma^2 + ||beta_hat - beta||^2 is known exactly.  How well does 10-fold CV track it, compared with how
    well it tracks Err = E Err_XY?"""
    g = rng(345)
    n, p, reps = 100, 20, 1000
    beta = np.zeros(p)
    beta[:5] = 1.0
    cvs, errs, ses, nested_cover = [], [], [], []
    for _ in range(reps):
        X = g.standard_normal((n, p))
        y = X @ beta + g.standard_normal(n)
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        errs.append(1 + float(np.sum((b - beta) ** 2)))
        folds = g.permutation(np.arange(n) % 10)
        e = np.zeros(n)
        for k in range(10):
            m = folds == k
            bk = np.linalg.lstsq(X[~m], y[~m], rcond=None)[0]
            e[m] = (y[m] - X[m] @ bk) ** 2
        cvs.append(e.mean())
        ses.append(e.std(ddof=1) / math.sqrt(n))
    cvs, errs, ses = map(np.array, (cvs, errs, ses))
    Err = 1 + p / (n - p - 1)  # E ||b - beta||^2 = sigma^2 tr (X'X)^{-1}, E tr = p / (n - p - 1)
    z = stats.norm.ppf(0.95)
    cover_xy = float(np.mean(np.abs(cvs - errs) <= z * ses))
    cover_err = float(np.mean(np.abs(cvs - Err) <= z * ses))
    sd_cv = float(np.std(cvs))
    return nest({"n": n, "p": p, "reps": reps, "cv": cvs[:300], "err_xy": errs[:300], "Err": Err,
                 "corr": float(np.corrcoef(cvs, errs)[0, 1]), "mean_cv": float(cvs.mean()),
                 "sd_cv": sd_cv, "sd_errxy": float(np.std(errs)), "mean_se": float(ses.mean()),
                 "se_ratio": float(sd_cv / ses.mean()), "cover_xy": cover_xy, "cover_err": cover_err})


def compute_calib():
    X, y, names = museum.breast_cancer()
    yf = y.astype(float)
    g = rng(346)
    pooled = {k: ([], []) for k in ("nb", "nb_platt", "nb_iso", "nb_temp", "rf", "rf_iso")}
    eces = {k: [] for k in pooled}
    briers = {k: [] for k in pooled}
    temps = []
    for s in range(40):
        perm = g.permutation(len(y))
        tr, ca, te = perm[:300], perm[300:435], perm[435:]
        Xs, Xc, Xt = standardize_pair(X[tr], X[ca], X[te])
        zc, zt = gnb_logit(Xs, y[tr], Xc), gnb_logit(Xs, y[tr], Xt)
        p = {"nb": sigmoid(zt)}
        a, b = CF.platt(zc, yf[ca])
        p["nb_platt"] = sigmoid(a + b * zt)
        ss, fit = CF.isotonic(zc, yf[ca])
        p["nb_iso"] = np.interp(zt, ss, fit)
        T = CF.temperature(zc, yf[ca])
        temps.append(T)
        p["nb_temp"] = sigmoid(zt / T)
        rf = CF.Forest(X[tr], yf[tr], B=150, mtry=5, min_leaf=1, rng=g)
        pc, pt = rf.predict(X[ca]), rf.predict(X[te])
        p["rf"] = pt
        ss, fit = CF.isotonic(pc, yf[ca])
        p["rf_iso"] = np.interp(pt, ss, fit)
        for k, v in p.items():
            pooled[k][0].extend(v.tolist())
            pooled[k][1].extend(yf[te].tolist())
            eces[k].append(CF.reliability(v, yf[te], 10)["ece"])
            briers[k].append(float(np.mean((v - yf[te]) ** 2)))
    rel = {k: CF.reliability(np.array(v[0]), np.array(v[1]), 10) for k, v in pooled.items()}
    acc = {k: float(np.mean((np.array(v[0]) > 0.5) == np.array(v[1]))) for k, v in pooled.items()}
    hist = {k: np.histogram(np.array(v[0]), bins=10, range=(0, 1))[0] for k, v in pooled.items()}
    return nest({"rel": rel, "ece": {k: float(np.mean(v)) for k, v in eces.items()},
                 "brier": {k: float(np.mean(v)) for k, v in briers.items()}, "acc": acc, "hist": hist,
                 "T": float(np.median(temps)), "splits": 40})


def compute_lemma():
    g = rng(347)
    n, alpha = 19, 0.1
    scores = np.sort(np.abs(g.standard_normal(n)) * 10).round(1)
    k = math.ceil((n + 1) * (1 - alpha))
    # the exact coverage given a calibration set is F(q), distributed Beta(k, n + 1 - k)
    out = {}
    for nn in (19, 99, 999):
        kk = math.ceil((nn + 1) * (1 - alpha))
        bd = stats.beta(kk, nn + 1 - kk)
        xs = np.linspace(0.6, 1.0, 401)
        out[str(nn)] = {"k": kk, "mean": kk / (nn + 1), "q05": float(bd.ppf(0.05)), "q95": float(bd.ppf(0.95)),
                        "xs": xs, "pdf": bd.pdf(xs)}
    # simulation check of marginal coverage with n = 19
    hits = []
    for _ in range(20000):
        s = np.abs(g.standard_normal(n + 1))
        q = np.sort(s[:n])[k - 1]
        hits.append(s[n] <= q)
    # a uniform-rank demonstration: where the new score lands among the n + 1
    ranks = np.bincount([int(np.sum(np.abs(g.standard_normal(n)) < abs(g.standard_normal()))) for _ in range(4000)],
                        minlength=n + 1)
    return nest({"n": n, "alpha": alpha, "scores": scores, "k": k, "q": float(scores[k - 1]), "beta": out,
                 "sim_cover": float(np.mean(hits)), "exact": k / (n + 1), "ranks": ranks})


def _income_split(g, n_tr=1000, n_ca=1000, n_te=20000, method="both"):
    w = World()
    idx = np.flatnonzero(w.adult)
    take = g.choice(idx, n_tr + n_ca + n_te, replace=False)
    a = w.age[take].astype(float)
    y = w.income[take] / 1000.0
    tr, ca, te = slice(0, n_tr), slice(n_tr, n_tr + n_ca), slice(n_tr + n_ca, None)
    Z = np.column_stack([np.ones(len(a)), poly_age(a)])
    b = np.linalg.lstsq(Z[tr], y[tr], rcond=None)[0]
    m = Z @ b
    sc = CF.split_conformal(m[ca], y[ca], m[te], 0.1)
    out = {"a": a[te], "y": y[te], "m": m[te], "sc": sc}
    if method == "both":
        blo = OP.quantile_lp(Z[tr], y[tr], 0.05)["b"]
        bhi = OP.quantile_lp(Z[tr], y[tr], 0.95)["b"]
        lo, hi = Z @ blo, Z @ bhi
        out["cqr"] = CF.cqr(lo[ca], hi[ca], y[ca], lo[te], hi[te], 0.1)
        out["qr"] = {"lo": lo[te], "hi": hi[te]}
    return out


def compute_split():
    g = rng(348)
    r = _income_split(g)
    a, y = r["a"], r["y"]
    groups = [(18, 25), (25, 35), (35, 45), (45, 55), (55, 67), (67, 100)]
    by = []
    for lo, hi in groups:
        k = (a >= lo) & (a < hi)
        by.append({"group": f"{lo}-{hi - 1}", "n": int(k.sum()),
                   "split": float(np.mean((y[k] >= r["sc"]["lo"][k]) & (y[k] <= r["sc"]["hi"][k]))),
                   "cqr": float(np.mean((y[k] >= r["cqr"]["lo"][k]) & (y[k] <= r["cqr"]["hi"][k]))),
                   "qr": float(np.mean((y[k] >= r["qr"]["lo"][k]) & (y[k] <= r["qr"]["hi"][k]))),
                   "w_split": float(np.mean(r["sc"]["hi"][k] - r["sc"]["lo"][k])),
                   "w_cqr": float(np.mean(r["cqr"]["hi"][k] - r["cqr"]["lo"][k]))})
    ag = np.arange(18, 96)
    Zg = np.column_stack([np.ones(len(ag)), poly_age(ag)])
    o = np.argsort(a)
    # plotting curves: centre, split band, CQR band, on a grid of ages
    def at_age(v):
        return np.array([np.mean(v[a == x]) if np.any(a == x) else np.nan for x in ag])
    show = g.choice(len(a), 1500, replace=False)
    return nest({"ages": ag, "m": at_age(r["m"]), "q": r["sc"]["q"], "cqr_q": r["cqr"]["q"],
                 "cqr_lo": at_age(r["cqr"]["lo"]), "cqr_hi": at_age(r["cqr"]["hi"]),
                 "pts_a": a[show], "pts_y": np.minimum(y[show], 250.0),
                 "cover_split": float(np.mean((y >= r["sc"]["lo"]) & (y <= r["sc"]["hi"]))),
                 "cover_cqr": float(np.mean((y >= r["cqr"]["lo"]) & (y <= r["cqr"]["hi"]))),
                 "cover_qr": float(np.mean((y >= r["qr"]["lo"]) & (y <= r["qr"]["hi"]))),
                 "width_split": float(np.mean(r["sc"]["hi"] - r["sc"]["lo"])),
                 "width_cqr": float(np.mean(r["cqr"]["hi"] - r["cqr"]["lo"])), "by_group": by})


def _minnorm(Xtr, ytr, Xev):
    return Xev @ (np.linalg.pinv(Xtr) @ ytr)


def compute_jack():
    """Barber, Candès, Ramdas & Tibshirani (2021), their Figure: least squares (minimum-norm past p = n) with n = 100;
    the naive jackknife fails near p = n, jackknife+ never drops below 1 - 2 alpha (and in practice holds 1 - alpha)."""
    g = rng(349)
    n, alpha, reps, ntest = 100, 0.1, 60, 1
    ps = [20, 50, 80, 90, 100, 110, 150, 200]
    res = {}
    for p in ps:
        cov = {k: [] for k in ("naive", "jack", "jplus", "split")}
        wid = {k: [] for k in cov}
        for _ in range(reps):
            beta = g.standard_normal(p) / math.sqrt(p) * math.sqrt(10)
            X = g.standard_normal((n + ntest, p))
            y = X @ beta + g.standard_normal(n + ntest)
            Xtr, ytr, Xt, yt = X[:n], y[:n], X[n:], y[n:]
            full = _minnorm(Xtr, ytr, np.vstack([Xtr, Xt]))
            fit_in, ft = full[:n], full[n:]
            # naive: in-sample residuals
            q = CF.conformal_quantile(np.abs(ytr - fit_in), alpha)
            cov["naive"].append(float(np.abs(yt[0] - ft[0]) <= q))
            wid["naive"].append(2 * q)
            # jackknife and jackknife+
            loo_r, loo_t = np.zeros(n), np.zeros(n)
            for i in range(n):
                m = np.ones(n, bool)
                m[i] = False
                pr = _minnorm(Xtr[m], ytr[m], np.vstack([Xtr[i:i + 1], Xt]))
                loo_r[i] = abs(ytr[i] - pr[0])
                loo_t[i] = pr[1]
            qj = CF.conformal_quantile(loo_r, alpha)
            cov["jack"].append(float(abs(yt[0] - ft[0]) <= qj))
            wid["jack"].append(2 * qj)
            kq = math.ceil((n + 1) * (1 - alpha))
            lo = -np.sort(-(loo_t - loo_r))[kq - 1]
            hi = np.sort(loo_t + loo_r)[kq - 1]
            cov["jplus"].append(float(lo <= yt[0] <= hi))
            wid["jplus"].append(hi - lo)
            # split: half to fit, half to calibrate
            h = n // 2
            pr = _minnorm(Xtr[:h], ytr[:h], np.vstack([Xtr[h:], Xt]))
            qs = CF.conformal_quantile(np.abs(ytr[h:] - pr[:-1]), alpha)
            cov["split"].append(float(abs(yt[0] - pr[-1]) <= qs))
            wid["split"].append(2 * qs)
        res[str(p)] = {k: {"cover": float(np.mean(cov[k])), "width": float(np.median(wid[k]))} for k in cov}
    return nest({"n": n, "ps": ps, "reps": reps, "res": res})


def compute_diab():
    X, y, names = museum.diabetes()
    g = rng(350)
    def fp(Xtr, ytr, Xev):
        return CF.Forest(Xtr, ytr, B=100, mtry=3, min_leaf=5, rng=g).predict(Xev)
    covs, wids, sc_cov, sc_wid = [], [], [], []
    for s in range(10):
        perm = g.permutation(len(y))
        te, tr = perm[:88], perm[88:]
        r = CF.jackknife_plus(fp, X[tr], y[tr], X[te], 0.1, K=10, rng=g)
        covs.append(float(np.mean((y[te] >= r["lo"]) & (y[te] <= r["hi"]))))
        wids.append(float(np.mean(r["hi"] - r["lo"])))
        h = len(tr) // 2
        pr = fp(X[tr[:h]], y[tr[:h]], np.vstack([X[tr[h:]], X[te]]))
        sc = CF.split_conformal(pr[:len(tr) - h], y[tr[h:]], pr[len(tr) - h:], 0.1)
        sc_cov.append(float(np.mean((y[te] >= sc["lo"]) & (y[te] <= sc["hi"]))))
        sc_wid.append(float(np.mean(sc["hi"] - sc["lo"])))
        if s == 0:
            first = {"lo": r["lo"][:12], "hi": r["hi"][:12], "y": y[te][:12]}
    return nest({"cvplus_cover": float(np.mean(covs)), "cvplus_width": float(np.mean(wids)),
                 "split_cover": float(np.mean(sc_cov)), "split_width": float(np.mean(sc_wid)), "first": first,
                 "y_sd": float(np.std(y)), "splits": 10})


def _shift_rep(g, w_all, n_tr=1000, n_ca=1000, n_te=2000):
    """Calibration from all adults; test from adults reweighted towards mid-career by w(age)."""
    w, idx, wt = w_all
    take = g.choice(idx, n_tr + n_ca, replace=False)
    te = g.choice(idx, n_te, replace=True, p=wt / wt.sum())
    a = w.age.astype(float)
    y = w.income / 1000.0
    Z = lambda ii: np.column_stack([np.ones(len(ii)), poly_age(a[ii])])
    tr, ca = take[:n_tr], take[n_tr:]
    b = np.linalg.lstsq(Z(tr), y[tr], rcond=None)[0]
    rc = np.abs(y[ca] - Z(ca) @ b)
    rt = np.abs(y[te] - Z(te) @ b)
    q = CF.conformal_quantile(rc, 0.1)
    unw = float(np.mean(rt <= q))
    lr = lambda ii: shift_weight(a[ii])
    wc = lr(ca)
    # the weighted quantile depends on the test point's own weight: compute per distinct test age
    hits = []
    cache = {}
    for i in te:
        ai = int(a[i])
        if ai not in cache:
            cache[ai] = CF.weighted_quantile_conformal(rc, wc, float(shift_weight(np.array([ai]))[0]), 0.1)
        hits.append(abs(y[i] - Z(np.array([i])) @ b)[0] <= cache[ai])
    return unw, float(np.mean(hits)), q, float(np.median(list(cache.values())))


def shift_weight(age):
    """The likelihood ratio of the test population to the calibration population: tilted towards ages 40-60."""
    age = np.asarray(age, float)
    return np.exp(-0.5 * ((age - 50) / 7.0) ** 2) / 0.25 + 0.05


def compute_shift():
    g = rng(351)
    w = World()
    idx = np.flatnonzero(w.adult)
    wt = shift_weight(w.age[idx])
    reps = 200
    res = np.array([_shift_rep(g, (w, idx, wt))[:4] for _ in range(reps)])
    ages = np.arange(18, 96)
    pop = np.bincount(w.age[idx], minlength=100)[18:96].astype(float)
    shifted = pop * shift_weight(ages)
    return nest({"unweighted": float(res[:, 0].mean()), "weighted": float(res[:, 1].mean()), "q": float(res[:, 2].mean()),
                 "qw": float(res[:, 3].mean()), "reps": reps, "ages": ages, "pop": pop / pop.sum(),
                 "shifted": shifted / shifted.sum()})


def compute_aci():
    g = rng(352)
    T = 3000
    sig = np.where((np.arange(T) >= 1000) & (np.arange(T) < 2000), 3.0, 1.0)
    scores = np.abs(sig * g.standard_normal(T))
    static_q = CF.conformal_quantile(scores[:300], 0.1)
    st = (scores[300:] > static_q).astype(float)
    r = CF.aci(scores, 0.1, gamma=0.01, window=300, warm=300)
    def roll(e, w=100):
        c = np.convolve(e, np.ones(w) / w, mode="valid")
        return c
    step = 10
    rs, ra = roll(1 - st), roll(1 - r["err"])
    return nest({"T": T, "static_q": static_q, "static_cover": float(1 - st.mean()), "aci_cover": float(1 - r["err"].mean()),
                 "static_mid": float(1 - st[700:1700].mean()), "aci_mid": float(1 - r["err"][700:1700].mean()),
                 "roll_t": np.arange(300 + 99, T)[::step], "roll_static": rs[::step], "roll_aci": ra[::step],
                 "thr_t": np.arange(300, T)[::step], "thr": np.minimum(r["threshold"], 12)[::step],
                 "alpha_t": r["alpha_t"][::step], "scores_t": np.arange(T)[::5], "scores": scores[::5]})


def _qda_probs(Xtr, ytr, X):
    cls = np.unique(ytr)
    L = []
    for c in cls:
        m, S = Xtr[ytr == c].mean(0), np.cov(Xtr[ytr == c].T)
        L.append(stats.multivariate_normal(m, S).logpdf(X) + math.log(np.mean(ytr == c)))
    L = np.array(L).T
    L -= L.max(1, keepdims=True)
    P = np.exp(L)
    return P / P.sum(1, keepdims=True)


def compute_sets():
    X, y, names = museum.iris()
    Xs = X[:, :2]  # sepals only: versicolor and virginica overlap
    g = rng(353)
    cover, sizes, cls_cov, mond_cov, acc = [], [], [[] for _ in range(3)], [[] for _ in range(3)], []
    size_by_class = [[] for _ in range(3)]
    example = None
    for s in range(300):
        perm = g.permutation(150)
        tr, ca, te = perm[:60], perm[60:105], perm[105:]
        Pc, Pt = _qda_probs(Xs[tr], y[tr], Xs[ca]), _qda_probs(Xs[tr], y[tr], Xs[te])
        sc = CF.aps_scores(Pc, y[ca], g)
        q = CF.conformal_quantile(sc, 0.1)
        S = CF.aps_sets(Pt, q, g)
        hit = np.array([y[te][i] in S[i] for i in range(len(te))])
        sz = np.array([len(v) for v in S])
        cover.append(hit.mean())
        sizes.extend(sz.tolist())
        acc.append(np.mean(Pt.argmax(1) == y[te]))
        # class-conditional (Mondrian) sets
        qs = CF.mondrian_quantiles(sc, y[ca], 0.1)
        for c in range(3):
            k = y[te] == c
            if k.any():
                cls_cov[c].append(hit[k].mean())
                size_by_class[c].extend(sz[k].tolist())
                # Mondrian: class c is in the set if its own score is within its own quantile
                hm = []
                for i in np.flatnonzero(k):
                    pr = Pt[i]
                    o = np.argsort(-pr)
                    cs = np.cumsum(pr[o])
                    r = int(np.flatnonzero(o == c)[0])
                    u = g.random()
                    hm.append(cs[r] - (1 - u) * pr[o][r] <= qs[c])
                mond_cov[c].append(np.mean(hm))
        if example is None:
            example = {"P": Pt[:8], "y": y[te][:8], "sets": [list(map(int, v)) for v in S[:8]], "q": q}
    sz = np.bincount(sizes, minlength=4)
    # breast cancer: binary sets from a logistic model on three features
    Xb, yb, nb = museum.breast_cancer()
    feats = [27, 20, 21]
    bc_sizes, bc_cov, bc_cov_cls = [], [], [[], []]
    for s in range(200):
        perm = g.permutation(len(yb))
        tr, ca, te = perm[:250], perm[250:400], perm[400:]
        A, Bc, Ct = standardize_pair(Xb[tr][:, feats], Xb[ca][:, feats], Xb[te][:, feats])
        wv = logistic_fit(A, yb[tr].astype(float), ridge=1e-3)
        pc, pt = sigmoid(logistic_logit(wv, Bc)), sigmoid(logistic_logit(wv, Ct))
        Pc, Pt = np.column_stack([1 - pc, pc]), np.column_stack([1 - pt, pt])
        # simple score 1 - p(true class) (Vovk's 'inverse probability')
        sc = 1 - Pc[np.arange(len(ca)), yb[ca]]
        q = CF.conformal_quantile(sc, 0.05)
        S = [[c for c in (0, 1) if 1 - Pt[i, c] <= q] for i in range(len(te))]
        hit = np.array([yb[te][i] in S[i] for i in range(len(te))])
        bc_cov.append(hit.mean())
        bc_sizes.extend(len(v) for v in S)
        for c in (0, 1):
            bc_cov_cls[c].append(hit[yb[te] == c].mean())
    return nest({"cover": float(np.mean(cover)), "size_counts": sz, "mean_size": float(np.mean(sizes)),
                 "acc": float(np.mean(acc)), "class_cover": [float(np.mean(v)) for v in cls_cov],
                 "mondrian_cover": [float(np.mean(v)) for v in mond_cov],
                 "class_size": [float(np.mean(v)) for v in size_by_class], "example": example,
                 "species": ["setosa", "versicolor", "virginica"],
                 "bc_cover": float(np.mean(bc_cov)), "bc_sizes": np.bincount(bc_sizes, minlength=3),
                 "bc_class_cover": [float(np.mean(v)) for v in bc_cov_cls], "bc_features": [nb[j] for j in feats]})


_PPI = {}


def _ppi_setup():
    """The question: the island's mean systolic blood pressure.  A label is a clinic visit (three cuff readings,
    averaged); a guess is a cuffless smartwatch's estimate, a forest on age, sex, BMI and the watch's own pulse-wave
    signal (pressure plus noise of SD 9), trained on 2,000 of the watch's early users, all aged 18-50.  A forest cannot
    extrapolate: for pressures above any it saw it repeats the highest it knows, so it under-reads the old and the
    hypertensive, and the guesses are biased low for the island."""
    if _PPI:
        return _PPI["setup"]
    w = World()
    g = rng(354)
    adults = np.flatnonzero(w.adult)
    h = w.health
    y_all = np.nanmean(h["sbp_read"], axis=1)
    pulse = h["sbp"] + 9.0 * rng(3540).standard_normal(w.n)  # the watch's pulse-wave signal: pressure plus noise
    feats = lambda ii: np.column_stack([w.age[ii].astype(float), (~w.male[ii]).astype(float), h["bmi"][ii], pulse[ii]])
    young = adults[(w.age[adults] >= 18) & (w.age[adults] <= 50)]
    tr = g.choice(young, 2000, replace=False)
    rf = CF.Forest(feats(tr), y_all[tr], B=60, mtry=3, min_leaf=10, rng=g)
    pool = g.choice(adults, 200_000, replace=False)  # the island as the study sees it
    f_pool = rf.predict(feats(pool))
    truth = float(y_all[adults].mean())
    _PPI["setup"] = (pool, y_all[pool], f_pool, truth)
    return _PPI["setup"]


def _ppi_rep(g, setup, n=300, N=20_000):
    pool, y, f, truth = setup
    k = g.permutation(len(pool))
    lab, unl = k[:n], k[n:n + N]
    c = PPI.classical_mean(y[lab])
    nv = PPI.naive_mean(f[unl])
    pp = PPI.ppi_mean(y[lab], f[lab], f[unl], lam=1.0)
    p2 = PPI.ppi_mean(y[lab], f[lab], f[unl], lam=None)
    return c, nv, pp, p2


def compute_ppi():
    setup = _ppi_setup()
    pool, y, f, truth = setup
    g = rng(355)
    c, nv, pp, p2 = _ppi_rep(g, setup)
    reps = np.array([[x["se"] for x in _ppi_rep(g, setup)] for _ in range(300)])
    n_equiv = 300 * float(np.mean(reps[:, 0]) / np.mean(reps[:, 3])) ** 2
    # a loose strap: the same guesses plus noise of SD 25.  PPI with lam = 1 is now worse than the labels alone;
    # PPI++ turns lam down and is never worse.
    gb = rng(3550)
    bad = (pool, y, f + 25.0 * gb.standard_normal(len(f)), truth)
    rb = []
    for _ in range(300):
        o = _ppi_rep(g, bad)
        rb.append([o[0]["se"], o[2]["se"], o[3]["se"], o[3]["lam"]])
    rb = np.array(rb).mean(0)
    # the guesses' bias by age band, on the pool
    w = World()
    ag = w.age[pool]
    bands = [(18, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 100)]
    by_age = [{"band": f"{a}-{b - 1}", "y": float(y[(ag >= a) & (ag < b)].mean()), "f": float(f[(ag >= a) & (ag < b)].mean())}
              for a, b in bands]
    show = g.choice(len(pool), 600, replace=False)
    return nest({"bad_se": rb[:3], "bad_lam": rb[3], "by_age": by_age, "pts_f": f[show], "pts_y": y[show],
                 "pts_age": ag[show], "truth": truth, "mean_f": float(f.mean()), "classical": c, "naive": nv, "ppi": pp, "ppi2": p2,
                 "n": 300, "N": 20_000, "mean_se": reps.mean(0), "n_equiv": n_equiv,
                 "corr_fy": float(np.corrcoef(f, y)[0, 1]), "sd_y": float(np.std(y)),
                 "sd_resid": float(np.std(y - f)), "bias": float(np.mean(f - y))})


def compute_interp():
    g = rng(356)
    n = 500
    X, y = friedman1(n, g)
    # a twin of x1 (correlation about 0.95)
    twin = np.clip(X[:, 0] + 0.07 * g.standard_normal(n), 0, 1)
    X2 = np.column_stack([X, twin])
    Xt, yt = friedman1(1000, g)
    Xt2 = np.column_stack([Xt, np.clip(Xt[:, 0] + 0.07 * g.standard_normal(1000), 0, 1)])
    rf = CF.Forest(X2, y, B=200, mtry=4, min_leaf=3, rng=g)
    base = float(np.mean((rf.predict(Xt2) - yt) ** 2))
    perm = rf.permutation_importance(Xt2, yt, rng=g, reps=5)
    loco = []
    for j in range(X2.shape[1]):
        k = np.arange(X2.shape[1]) != j
        f = CF.Forest(X2[:, k], y, B=120, mtry=4, min_leaf=3, rng=g)
        loco.append(float(np.mean((f.predict(Xt2[:, k]) - yt) ** 2) - base))
    # partial dependence for x1, x3, x4
    grid = np.linspace(0.02, 0.98, 25)
    bg = Xt2[:300]
    pdp = {}
    for j in (0, 2, 3, 4):
        vals = []
        for v in grid:
            Z = bg.copy()
            Z[:, j] = v
            if j == 0:
                Z[:, 10] = v  # move the twin with it, as a sensible PDP of the pair would not; see narration
            vals.append(float(rf.predict(Z).mean()))
        pdp[str(j)] = vals
    # the truth's partial dependence (average of mu over the others)
    tpdp = {}
    for j in (0, 2, 3, 4):
        vals = []
        for v in grid:
            Z = bg[:, :10].copy()
            Z[:, j] = v
            vals.append(float(friedman1_mu(Z).mean()))
        tpdp[str(j)] = vals
    # exact interventional Shapley values at one point, over the first five features (others at background)
    x = np.array([[0.8, 0.7, 0.1, 0.9, 0.5, 0.3, 0.6, 0.2, 0.4, 0.5, 0.8]])
    feats = [0, 1, 2, 3, 4]
    bgs = Xt2[:120]
    vcache = {}
    def value(S):
        S = tuple(sorted(S))
        if S not in vcache:
            Z = bgs.copy()
            for j in S:
                Z[:, j] = x[0, j]
            vcache[S] = float(rf.predict(Z).mean())
        return vcache[S]
    m = len(feats)
    phi = []
    for j in feats:
        others = [k for k in feats if k != j]
        tot = 0.0
        for r in range(m):
            for S in itertools.combinations(others, r):
                wgt = math.factorial(r) * math.factorial(m - r - 1) / math.factorial(m)
                tot += wgt * (value(S + (j,)) - value(S))
        phi.append(tot)
    v0 = value(())
    vall = value(tuple(feats))
    return nest({"base_mse": base, "perm": perm, "loco": loco, "grid": grid, "pdp": pdp, "true_pdp": tpdp,
                 "x": x[0], "phi": phi, "v0": v0, "vall": vall, "pred_x": float(rf.predict(x)[0]),
                 "mu_x": float(friedman1_mu(x[:, :10])[0]), "names": [f"x_{{{k + 1}}}" for k in range(10)] + ["x_1'"]})


# ----------------------------------------------------------------------------------------------------------- board


def eff_reps(per_rep, nominal=0.9) -> int:
    """For a coverage averaged over many test points in each replication, the number of independent hits whose
    binomial SE matches the actual SE of the mean (from the spread across replications), so that the Board's
    three-SE verdict is judged against the real Monte Carlo error."""
    v = np.var(np.asarray(per_rep, float), ddof=1) / len(per_rep)
    return int(round(nominal * (1 - nominal) / max(v, 1e-12)))


def compute_board():
    rows = []
    g = rng(360)
    # split conformal on incomes: marginal coverage over fresh calibration sets
    reps = 300
    sc, cq = [], []
    for _ in range(reps):
        r = _income_split(g, n_tr=500, n_ca=500, n_te=2000)
        sc.append(np.mean((r["y"] >= r["sc"]["lo"]) & (r["y"] <= r["sc"]["hi"])))
        cq.append(np.mean((r["y"] >= r["cqr"]["lo"]) & (r["y"] <= r["cqr"]["hi"])))
    # per-rep coverage averages over 2000 test points; the board's reps count test draws as one per rep
    rows.append(Row(34, r"split conformal, \ 90\%", r"World incomes, \ cubic in age, \ $n_{\rm cal} = 500$", "coverage",
                    0.9, float(np.mean(sc)), eff_reps(sc)))
    rows.append(Row(34, r"CQR, \ 90\%", r"World incomes, \ cubic in age, \ $n_{\rm cal} = 500$", "coverage", 0.9,
                    float(np.mean(cq)), eff_reps(cq)))
    # Barber's regime: p = n = 100
    j = compute_jack_board(g)
    rows.append(Row(34, r"in-sample residuals, \ 90\%", r"least squares, \ $p = n = 100$", "coverage", 0.9,
                    j["naive"], j["reps"]))
    rows.append(Row(34, r"jackknife+, \ 90\%", r"least squares, \ $p = n = 100$", "coverage", 0.9, j["jplus"], j["reps"]))
    # shift
    w = World()
    idx = np.flatnonzero(w.adult)
    wt = shift_weight(w.age[idx])
    res = np.array([_shift_rep(g, (w, idx, wt), n_te=400)[:2] for _ in range(reps)])
    rows.append(Row(34, r"split conformal, \ unweighted", r"test ages shifted to 40--60", "coverage", 0.9,
                    float(res[:, 0].mean()), eff_reps(res[:, 0])))
    rows.append(Row(34, r"weighted conformal, \ 90\%", r"test ages shifted to 40--60", "coverage", 0.9,
                    float(res[:, 1].mean()), eff_reps(res[:, 1])))
    # PPI
    setup = _ppi_setup()
    truth = setup[3]
    reps_p = 1000
    hits = np.zeros(4)
    for _ in range(reps_p):
        out = _ppi_rep(g, setup)
        hits += [o["lo"] <= truth <= o["hi"] for o in out]
    hits /= reps_p
    rows.append(Row(34, r"classical, \ 300 clinic visits", r"World blood pressure, \ 90\%", "coverage", 0.9, float(hits[0]), reps_p))
    rows.append(Row(34, r"watch guesses as data", r"World blood pressure, \ 20,000 guesses", "coverage", 0.9, float(hits[1]), reps_p))
    rows.append(Row(34, r"prediction-powered", r"World blood pressure, \ 90\%", "coverage", 0.9, float(hits[2]), reps_p))
    rows.append(Row(34, r"PPI++ \ (tuned $\lambda$)", r"World blood pressure, \ 90\%", "coverage", 0.9, float(hits[3]), reps_p))
    # forest IJ
    ij = load("ij")
    rows.append(Row(34, r"forest IJ, \ bootstrap, \ for $\mathrm{E}\,\hat f(x_0)$", r"Friedman 1, \ $n = 250$, \ 500 trees", "coverage", 0.9,
                    ij["cov_E"], ij["reps"]))
    ijs = load("ij_sub")
    rows.append(Row(34, r"forest IJ, \ subsampled, \ for $\mathrm{E}\,\hat f(x_0)$", r"Friedman 1, \ $s = 50$ of $250$", "coverage", 0.9,
                    ijs["cov_E"], ijs["reps"]))
    rows.append(Row(34, r"forest IJ, \ subsampled, \ for $\mu(x_0)$", r"Friedman 1, \ at a peak", "coverage", 0.9, ijs["cov_mu"],
                    ijs["reps"]))
    cv = load("cv")
    rows.append(Row(34, r"naive 10-fold CV interval, \ 90\%", r"least squares, \ $n = 100$, \ $p = 20$: \ for Err", "coverage",
                    0.9, cv["cover_err"], cv["reps"]))
    save_rows(34, rows)
    return nest({"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "ppi_hits": hits,
                 "split": float(np.mean(sc)), "cqr": float(np.mean(cq)), "jack": j,
                 "shift": res.mean(0)})


def compute_jack_board(g, reps=300):
    n, p, alpha = 100, 100, 0.1
    nv, jp = [], []
    for _ in range(reps):
        beta = g.standard_normal(p) / math.sqrt(p) * math.sqrt(10)
        X = g.standard_normal((n + 1, p))
        y = X @ beta + g.standard_normal(n + 1)
        Xtr, ytr, Xt, yt = X[:n], y[:n], X[n:], y[n:]
        full = _minnorm(Xtr, ytr, np.vstack([Xtr, Xt]))
        q = CF.conformal_quantile(np.abs(ytr - full[:n]), alpha)
        nv.append(float(abs(yt[0] - full[n]) <= q))
        loo_r, loo_t = np.zeros(n), np.zeros(n)
        for i in range(n):
            m = np.ones(n, bool)
            m[i] = False
            pr = _minnorm(Xtr[m], ytr[m], np.vstack([Xtr[i:i + 1], Xt]))
            loo_r[i], loo_t[i] = abs(ytr[i] - pr[0]), pr[1]
        kq = math.ceil((n + 1) * (1 - alpha))
        lo = -np.sort(-(loo_t - loo_r))[kq - 1]
        hi = np.sort(loo_t + loo_r)[kq - 1]
        jp.append(float(lo <= yt[0] <= hi))
    return {"naive": float(np.mean(nv)), "jplus": float(np.mean(jp)), "reps": reps}


ITEMS = {
    "rashomon": compute_rashomon, "forest": compute_forest, "variance": compute_variance, "ij": compute_ij,
    "ij_sub": compute_ij_sub,
    "boost": compute_boost, "cv": compute_cv, "calib": compute_calib, "lemma": compute_lemma, "split": compute_split,
    "jack": compute_jack, "diab": compute_diab, "shift": compute_shift, "aci": compute_aci, "sets": compute_sets,
    "ppi": compute_ppi, "interp": compute_interp, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
