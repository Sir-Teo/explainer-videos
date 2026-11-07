"""Precompute every number in Part 19 of *Statistics, Built* ("Learning from Data").

    python -m videos.stats.stats19.compute            # everything missing (a few minutes)
    python -m videos.stats.stats19.compute --force board

Results are cached in ``.cache/stats19/<name>.json``.  The *Federalist* word counts are the Museum's (from Project
Gutenberg); the vote and incomes are the World's survey block; everything else is a seeded simulation.

Items:
    rates       word rates per 1,000 for Hamilton, Madison and the disputed papers; 'upon' paper by paper
    poly        training vs test error for polynomials of degree 1-14 on a known curve
    biasvar     k-NN at a point: bias^2, variance and noise across k, by simulation, against the formulas
    cv          10-fold CV of k for k-NN with SEs, the one-SE rule, against the true test error
    curse       nearest-neighbour distances and k-NN error as irrelevant dimensions are added
    nbvslr      Federalist: Poisson naive Bayes vs ridge logistic regression, leave-one-out over the 65 known papers,
                and learning curves
    tree        a CART tree for the World's vote from income and age, cost-complexity pruned by CV
    lasso       a sparse regression: lasso and ridge paths, CV over lambda
    metrics     logistic vote model on held-out adults: confusion, ROC, PR, calibration
    decided     the 12 disputed papers: naive Bayes log odds and word contributions; logistic probabilities
    leakage     feature selection outside vs inside the CV loop on pure noise
    reuse       a reused holdout: 1,000 random classifiers on 1,000 random labels; the best one, and the vote of the
                better half (Blum & Hardt 2015)
    nested      the optimism of the CV minimum for k-NN, against nested CV and the true test error
    cp          Mallows' Cp for the polynomials: training error plus the optimism 2 sigma^2 (d + 1) / n, against test error
    coverhart   1-NN and k-NN against the Bayes error for two normal classes, as n grows (Cover & Hart 1967)
    robust      the disputed papers' naive Bayes verdicts with the strongest words removed
    costs       the metrics model's expected cost per adult against the threshold, for three cost ratios
    board       Coverage Board row: the naive CV interval for test error
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import glm as G
from explainer.stats.kit import learn as L
from explainer.stats.world import World

CACHE = Cache("stats19")
load = CACHE.load
W = World()
R_BOARD = 2_000
MARKERS = ["upon", "whilst", "while", "enough", "although", "by", "on", "there", "to", "also", "an", "of"]


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
    return obj


def fed_matrix(words=None):
    d = museum.federalist()
    words = words or d["function_words"] + d["extra_words"]
    P = d["papers"]
    C = np.array([[p["counts"][w] for w in words] for p in P], float)
    n = np.array([p["n_words"] for p in P], float)
    a = np.array([p["author"] for p in P])
    no = np.array([p["no"] for p in P])
    return words, C, n, a, no


def truth_curve(x):
    return np.sin(2 * np.pi * x) + 0.5 * x


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


def knn_population_risk(x, y, k, noise=.09):
    """Exact squared-error risk for our curve, uniform X in [0,1], and distinct training x.

    In one dimension, the k-neighbour window changes at (x_i+x_{i+k})/2.
    Integrate the squared difference on each constant-prediction interval.
    """
    order = np.argsort(x)
    x, y = np.asarray(x, float)[order], np.asarray(y, float)[order]
    if not 1 <= k <= len(x) or len(np.unique(x)) != len(x):
        raise ValueError('Require distinct training inputs and 1 <= k <= n')
    cuts = np.r_[0., (x[:-k]+x[k:])/2, 1.] if k < len(x) else np.array([0., 1.])
    if np.any(np.diff(cuts) < 0):
        raise ValueError('Training inputs must lie in [0,1]')
    pred = np.convolve(y, np.ones(k)/k, mode='valid')
    omega = 2*np.pi
    primitive = -np.cos(omega*cuts)/omega + cuts**2/4
    primitive2 = (cuts/2 - np.sin(2*omega*cuts)/(4*omega)
                  - cuts*np.cos(omega*cuts)/omega + np.sin(omega*cuts)/omega**2
                  + cuts**3/12)
    return float(noise + np.sum(np.diff(primitive2)-2*pred*np.diff(primitive)+pred**2*np.diff(cuts)))


def threshold_pr_curve(scores, labels):
    """Evaluate only complete score-tie groups, including the full-recall endpoint."""
    scores, labels = np.asarray(scores), np.asarray(labels)
    order = np.argsort(-scores, kind='stable')
    ends = np.r_[np.flatnonzero(np.diff(scores[order]) != 0), len(scores)-1]
    tp = np.cumsum(labels[order])[ends]
    return np.r_[1., tp/(ends+1)], np.r_[0., tp/labels.sum()]


def compute_rates():
    words, C, n, a, no = fed_matrix()
    out = {}
    for au in ("HAMILTON", "MADISON", "DISPUTED"):
        k = a == au
        out[au] = {w: 1000 * C[k, words.index(w)].sum() / n[k].sum() for w in MARKERS}
    j = words.index("upon")
    per = {au: (1000 * C[a == au, j] / n[a == au]).tolist() for au in ("HAMILTON", "MADISON", "DISPUTED")}
    zero = {au: int(np.sum(C[a == au, j] == 0)) for au in ("HAMILTON", "MADISON", "DISPUTED")}
    return nest({"rates": out, "upon": per, "upon_zero": zero, "n_papers": {au: int(np.sum(a == au)) for au in set(a)}})


def compute_poly():
    g = rng(19)
    x = np.sort(g.uniform(0, 1, 30))
    y = truth_curve(x) + g.normal(0, 0.3, 30)
    xt = g.uniform(0, 1, 5000)
    yt = truth_curve(xt) + g.normal(0, 0.3, 5000)
    tr, te = [], []
    fits = {}
    for d in range(1, 15):
        c = np.polyfit(x, y, d)
        tr.append(float(np.mean((np.polyval(c, x) - y) ** 2)))
        te.append(float(np.mean((np.polyval(c, xt) - yt) ** 2)))
        if d in (1, 3, 5, 12):
            grid = np.linspace(0, 1, 200)
            fits[d] = np.polyval(c, grid)
    return nest({"x": x, "y": y, "train": tr, "test": te, "fits": fits, "grid": np.linspace(0, 1, 200), "noise": 0.09})


def compute_biasvar():
    g = rng(1992)
    n, sig, x0 = 100, 0.3, 0.25
    ks = [1, 2, 3, 5, 8, 12, 20, 30, 50]
    preds = {k: [] for k in ks}
    for _ in range(3000):
        x = g.uniform(0, 1, n)
        y = truth_curve(x) + g.normal(0, sig, n)
        order = np.argsort(np.abs(x - x0))
        for k in ks:
            preds[k].append(y[order[:k]].mean())
    f0 = truth_curve(x0)
    bias2 = [float((np.mean(preds[k]) - f0) ** 2) for k in ks]
    var = [float(np.var(preds[k])) for k in ks]
    return nest({"ks": ks, "bias2": bias2, "var": var, "noise": sig ** 2, "var_formula": [sig ** 2 / k for k in ks],
                 "total": [b + v + sig ** 2 for b, v in zip(bias2, var)], "x0": x0})


def compute_cv():
    g = rng(10)
    n = 100
    x = g.uniform(0, 1, n)
    y = truth_curve(x) + g.normal(0, 0.3, n)
    xt = g.uniform(0, 1, 4000)
    yt = truth_curve(xt) + g.normal(0, 0.3, 4000)
    ks = list(range(1, 41))
    means, ses, test = [], [], []
    for k in ks:
        r = L.cv_score(lambda a, b, c: L.knn_predict(a, b, c, k), x[:, None], y, 10, rng(100))
        means.append(r["mean"])
        ses.append(r["se"])
        test.append(float(np.mean((L.knn_predict(x[:, None], y, xt[:, None], k) - yt) ** 2)))
    best, simple = L.one_se_rule(means[::-1], ses[::-1])  # simplest = largest k
    best_k, simple_k = ks[::-1][best], ks[::-1][simple]
    return nest({"ks": ks, "cv": means, "se": ses, "test": test, "best_k": best_k, "one_se_k": simple_k,
                 "test_best": test[ks.index(best_k)], "test_one_se": test[ks.index(simple_k)], "test_min": min(test),
                 "test_argmin": ks[int(np.argmin(test))]})


def compute_curse():
    g = rng(1961)
    dims = [1, 2, 5, 10, 20, 50, 100]
    nn_ratio, err = [], []
    for p in dims:
        X = g.uniform(0, 1, (500, p))
        d = np.sqrt(((X[:1] - X[1:]) ** 2).sum(1))
        nn_ratio.append(float(d.min() / d.mean()))
        # one signal dimension, p - 1 irrelevant ones
        Xt = g.uniform(0, 1, (500, p))
        y = truth_curve(X[:, 0]) + g.normal(0, 0.3, 500)
        yt = truth_curve(Xt[:, 0]) + g.normal(0, 0.3, 500)
        err.append(float(np.mean((L.knn_predict(X, y, Xt, 10) - yt) ** 2)))
    side = [0.1 ** (1 / p) for p in dims]  # edge of a cube holding 10% of the unit cube
    return nest({"dims": dims, "nn_ratio": nn_ratio, "err": err, "side": side})


def lr_features(C, n):
    return 1000 * C / n[:, None]


def compute_nbvslr():
    words, C, n, a, no = fed_matrix()
    known = (a == "HAMILTON") | (a == "MADISON")
    Ck, nk, yk = C[known], n[known], (a[known] == "MADISON").astype(int)
    m = len(yk)
    nb_pred, lr_pred = [], []
    for i in range(m):
        tr = np.arange(m) != i
        nb = L.PoissonNB().fit(Ck[tr], nk[tr], yk[tr])
        nb_pred.append(float(nb.log_odds(Ck[i:i + 1], nk[i:i + 1])[0] > 0))
        Xr = lr_features(Ck, nk)
        mu, sd = Xr[tr].mean(0), Xr[tr].std(0) + 1e-9
        b = L.logistic_ridge((Xr[tr] - mu) / sd, yk[tr], lam=5.0)
        lr_pred.append(float(L.logistic_predict(b, ((Xr[i] - mu) / sd)[None, :])[0] > 0.5))
    nb_err = float(np.mean(np.array(nb_pred) != yk))
    lr_err = float(np.mean(np.array(lr_pred) != yk))
    # learning curves: train on n_train random known papers (balanced as far as possible), test on the rest
    g = rng(2002)
    sizes = [6, 10, 16, 24, 34, 44, 54]
    curves = {"nb": [], "lr": []}
    for s in sizes:
        e_nb, e_lr = [], []
        for _ in range(200):
            idx_m, idx_h = np.flatnonzero(yk == 1), np.flatnonzero(yk == 0)
            nm = max(2, int(round(s * 14 / 65)))
            tr = np.r_[g.choice(idx_m, min(nm, 12), replace=False), g.choice(idx_h, s - min(nm, 12), replace=False)]
            te = np.setdiff1d(np.arange(m), tr)
            nb = L.PoissonNB().fit(Ck[tr], nk[tr], yk[tr])
            e_nb.append(np.mean((nb.log_odds(Ck[te], nk[te]) > 0) != yk[te]))
            Xr = lr_features(Ck, nk)
            mu, sd = Xr[tr].mean(0), Xr[tr].std(0) + 1e-9
            b = L.logistic_ridge((Xr[tr] - mu) / sd, yk[tr], lam=5.0)
            e_lr.append(np.mean((L.logistic_predict(b, (Xr[te] - mu) / sd) > 0.5) != yk[te]))
        curves["nb"].append(float(np.mean(e_nb)))
        curves["lr"].append(float(np.mean(e_lr)))
    return nest({"nb_err": nb_err, "lr_err": lr_err, "m": m, "sizes": sizes, "curves": curves, "n_words": len(words)})


def compute_tree():
    A = W.adult
    idx = W.sample(3000, among=A, seed=1984)
    inc = W.income[idx] / 1000
    age = W.age[idx].astype(float)
    v = W.survey["vote_blue"][idx].astype(float)
    X = np.column_stack([np.log10(inc), age])
    g = rng(1984)
    tr, te = np.arange(2000), np.arange(2000, 3000)
    big = L.grow_tree(X[tr], v[tr], max_depth=6, min_leaf=20, classify=True)
    n_leaves_full = len(L.leaves(big))
    sizes = list(range(1, min(n_leaves_full, 24) + 1))
    folds = L.kfold(2000, 10, g)
    cv = np.zeros(len(sizes))
    for f in folds:
        trf = np.setdiff1d(tr, f)
        t = L.grow_tree(X[trf], v[trf], max_depth=6, min_leaf=20, classify=True)
        for j, s in enumerate(sizes):
            pr = L.tree_predict(L.prune_to(t, s), X[f])
            cv[j] += np.sum((pr > 0.5) != v[f])
    cv = cv / 2000
    best = sizes[int(np.argmin(cv))]
    pruned = L.prune_to(big, best)
    test_err = float(np.mean((L.tree_predict(pruned, X[te]) > 0.5) != v[te]))
    test_full = float(np.mean((L.tree_predict(big, X[te]) > 0.5) != v[te]))

    def dump(node):
        if node.leaf:
            return {"value": node.value, "n": node.n}
        return {"feature": node.feature, "threshold": node.threshold, "value": node.value, "n": node.n,
                "left": dump(node.left), "right": dump(node.right)}

    small = L.prune_to(big, 4)
    return nest({"sizes": sizes, "cv": cv, "best": best, "pruned_leaves": len(L.leaves(pruned)),
                 "test_pruned": test_err, "test_full": test_full,
                 "n_leaves_full": n_leaves_full, "small": dump(small), "pruned": dump(pruned), "base": float(v[te].mean()),
                 "sample_x": X[:600], "sample_v": v[:600]})


def compute_lasso():
    g = rng(1996)
    n, p = 100, 20
    beta = np.zeros(p)
    beta[[0, 3, 7]] = [3.0, -2.0, 1.5]
    X = g.normal(size=(n, p))
    X = X + 0.3 * X[:, [0]]  # mild correlation
    Xs, mu, sd = L.standardize(X)
    y = X @ beta + g.normal(0, 2.0, n)
    yc = y - y.mean()
    lam_max = float(np.max(np.abs(Xs.T @ yc)) / n)
    lams = lam_max * np.logspace(0, -2.5, 60)
    path = L.lasso_path(Xs, yc, lams)
    # Per-observation ridge objective: SSE/(2n) + lambda*||b||^2/2.
    rl = np.logspace(3, -1, 60)/n
    rpath = np.array([L.ridge(Xs, yc, n*l) for l in rl])
    folds = L.kfold(n, 10, rng(7))
    cvm = []
    cvs = []
    for lam in lams:
        errs = []
        for f in folds:
            tr = np.setdiff1d(np.arange(n), f)
            Xt, m_, s_ = L.standardize(X[tr])
            yt = y[tr] - y[tr].mean()
            b = L.lasso(Xt, yt, lam)
            pr = ((X[f] - m_) / s_) @ b + y[tr].mean()
            errs.append(np.mean((y[f] - pr) ** 2))
        cvm.append(float(np.mean(errs)))
        cvs.append(float(np.std(errs, ddof=1) / np.sqrt(10)))
    best, simple = L.one_se_rule(cvm, cvs)  # lams decreasing = complexity increasing
    ols = np.linalg.lstsq(Xs, yc, rcond=None)[0]
    return nest({"n": n, "lams": lams, "path": path, "ridge_lams": rl, "ridge_path": rpath, "cv": cvm, "cv_se": cvs, "best": best,
                 "one_se": simple, "b_best": path[best], "b_one_se": path[simple], "true": beta * sd, "ols": ols,
                 "nz_best": int(np.count_nonzero(path[best])), "nz_one_se": int(np.count_nonzero(path[simple]))})


def compute_metrics():
    A = W.adult
    idx = W.sample(6000, among=A, seed=2006)
    inc = np.log10(W.income[idx] / 1000)
    age = W.age[idx].astype(float)
    v = W.survey["vote_blue"][idx].astype(float)
    X = np.column_stack([inc, (age - 45) / 15, ((age - 45) / 15) ** 2])
    tr, te = np.arange(4000), np.arange(4000, 6000)
    b = L.logistic_ridge(X[tr], v[tr], 0.0)
    p = L.logistic_predict(b, X[te])
    conf = L.confusion(v[te], p > 0.5)
    conf3 = L.confusion(v[te], p > 0.35)
    fpr, tpr = [], []
    ths = np.linspace(1, 0, 101)
    for t in ths:
        c = L.confusion(v[te], p >= t)
        fpr.append(c["fp"] / max(1, c["fp"] + c["tn"]))
        tpr.append(c["tp"] / max(1, c["tp"] + c["fn"]))
    prec, rec = threshold_pr_curve(p, v[te])
    cal = G.calibration(p, v[te], bins=10)
    return nest({"b": b, "conf": conf, "conf35": conf3, "fpr": fpr, "tpr": tpr, "auc": L.auc(p, v[te]), "prec": prec,
                 "rec": rec, "base": float(v[te].mean()), "calibration": cal, "brier": G.brier(p, v[te])})


def compute_costs():
    A = W.adult
    idx = W.sample(6000, among=A, seed=2006)  # the same adults and model as ``metrics``
    inc = np.log10(W.income[idx] / 1000)
    age = W.age[idx].astype(float)
    v = W.survey["vote_blue"][idx].astype(float)
    X = np.column_stack([inc, (age - 45) / 15, ((age - 45) / 15) ** 2])
    tr, te = np.arange(4000), np.arange(4000, 6000)
    b = L.logistic_ridge(X[tr], v[tr], 0.0)
    p = L.logistic_predict(b, X[te])
    ths = np.round(np.linspace(0.05, 0.95, 91), 3)
    out = {}
    for c in (1, 2, 5):  # a missed Blue voter costs c; a wasted call on a Red voter costs 1
        cost = [float((c * np.sum((p < t) & (v[te] == 1)) + np.sum((p >= t) & (v[te] == 0))) / len(te)) for t in ths]
        j = int(np.argmin(cost))
        out[str(c)] = {"cost": cost, "best_t": float(ths[j]), "theory_t": 1 / (1 + c), "best_cost": cost[j],
                       "call_none": float(c * v[te].mean()), "call_all": float(1 - v[te].mean())}
    return nest({"ths": ths, "runs": out})


def compute_decided():
    words, C, n, a, no = fed_matrix()
    known = (a == "HAMILTON") | (a == "MADISON")
    yk = (a[known] == "MADISON").astype(int)
    nb = L.PoissonNB().fit(C[known], n[known], yk)
    disp = a == "DISPUTED"
    lo = nb.log_odds(C[disp], n[disp])
    contrib = np.array([nb.contributions(C[i], n[i]) for i in np.flatnonzero(disp)])
    top = np.argsort(-np.abs(contrib.sum(0)))[:8]
    Xr = lr_features(C, n)
    mu, sd = Xr[known].mean(0), Xr[known].std(0) + 1e-9
    b = L.logistic_ridge((Xr[known] - mu) / sd, yk, lam=5.0)
    pl = L.logistic_predict(b, (Xr[disp] - mu) / sd)
    lo_known = nb.log_odds(C[known], n[known])
    return nest({"papers": no[disp], "log_odds": lo, "log10_odds": lo / np.log(10), "lr_prob": pl,
                 "top_words": [words[j] for j in top], "top_contrib": contrib.sum(0)[top] / disp.sum(),
                 "known_log10": lo_known / np.log(10), "known_y": yk, "known_no": no[known],
                 "joint": {"papers": no[a == "JOINT"], "log10": nb.log_odds(C[a == "JOINT"], n[a == "JOINT"]) / np.log(10)}})


def compute_leakage():
    g = rng(2010)
    n, p, k = 60, 2000, 20
    reps = 100
    wrong, right = [], []
    for _ in range(reps):
        X = g.normal(size=(n, p))
        y = (g.random(n) < 0.5).astype(int)

        def top_feats(Xa, ya):
            c = np.abs([np.corrcoef(Xa[:, j], ya)[0, 1] for j in range(p)])
            return np.argsort(-c)[:k]

        sel = top_feats(X, y)
        folds = L.kfold(n, 5, g)
        e_w = e_r = 0
        for f in folds:
            tr = np.setdiff1d(np.arange(n), f)
            pr = L.knn_predict(X[tr][:, sel], y[tr], X[f][:, sel], 5, classify=True)
            e_w += np.sum(pr != y[f])
            s2 = top_feats(X[tr], y[tr])
            pr2 = L.knn_predict(X[tr][:, s2], y[tr], X[f][:, s2], 5, classify=True)
            e_r += np.sum(pr2 != y[f])
        wrong.append(e_w / n)
        right.append(e_r / n)
    return nest({"wrong": float(np.mean(wrong)), "right": float(np.mean(right)), "n": n, "p": p, "k": k,
                 "wrong_all": wrong, "right_all": right})


def compute_reuse():
    g = rng(2015)
    n, m = 1000, 1000
    y = g.integers(0, 2, n)  # holdout labels: coin flips, so every rule is truly 50% accurate
    P = g.integers(0, 2, (m, n))
    acc = (P == y).mean(1)
    best = float(acc.max())
    good = acc > 0.5
    vote = ((P[good].mean(0)) > 0.5).astype(int)
    vote_acc = float((vote == y).mean())
    yf = g.integers(0, 2, n)  # fresh labels: the truth
    vote_fresh = float((vote == yf).mean())
    curve = []
    for mm in [1, 10, 30, 100, 300, 1000]:
        a = acc[:mm]
        gg = a > 0.5
        v = ((P[:mm][gg].mean(0)) > 0.5).astype(int) if gg.any() else P[0]
        curve.append({"m": mm, "best": float(a.max()), "vote": float((v == y).mean()), "fresh": float((v == yf).mean())})
    return nest({"n": n, "m": m, "acc": acc, "best": best, "n_good": int(good.sum()), "vote_acc": vote_acc,
                 "vote_fresh": vote_fresh, "curve": curve})


def compute_nested():
    g = rng(2023)
    ks = [1, 2, 3, 5, 8, 12, 17, 25, 35]
    reps = 200
    mins, trues, nesteds = [], [], []
    # Retain the original RNG schedule for the training samples. Risk below is exact.
    xt = g.uniform(0, 1, 4000)
    _ = truth_curve(xt) + g.normal(0, 0.3, 4000)

    def tune(x, y, seed):
        cvs = [L.cv_score(lambda a, b, c, k=k: L.knn_predict(a, b, c, k), x[:, None], y, 5, rng(seed))["mean"] for k in ks]
        j = int(np.argmin(cvs))
        return ks[j], cvs[j]

    for r in range(reps):
        x = g.uniform(0, 1, 100)
        y = truth_curve(x) + g.normal(0, 0.3, 100)
        k, m = tune(x, y, 10_000 + r)
        mins.append(m)
        trues.append(knn_population_risk(x, y, k))
        outer = L.kfold(100, 5, rng(20_000 + r))
        e = 0.0
        for f in outer:
            tr = np.setdiff1d(np.arange(100), f)
            kk, _ = tune(x[tr], y[tr], 30_000 + r)
            e += float(np.sum((L.knn_predict(x[tr][:, None], y[tr], x[f][:, None], kk) - y[f]) ** 2))
        nesteds.append(e / 100)
    return nest({"ks": ks, "reps": reps, "min_cv": float(np.mean(mins)), "true": float(np.mean(trues)),
                 "nested": float(np.mean(nesteds)), "mins": mins, "trues": trues, "nesteds": nesteds})


def compute_cp():
    d = load("poly")
    n, s2 = len(d["x"]), d["noise"]
    deg = np.arange(1, 15)
    cp = np.asarray(d["train"]) + 2 * s2 * (deg + 1) / n
    x = np.asarray(d['x'])
    signal = truth_curve(x)
    fixed_risk = []
    for degree in deg:
        Q, _ = np.linalg.qr(np.polynomial.legendre.legvander(2*x-1, degree))
        bias = signal-Q@(Q.T@signal)
        fixed_risk.append(np.mean(bias**2)+s2*(1+(degree+1)/n))
    return nest({"deg": deg, "cp": cp, "train": d["train"], "test": d["test"], "n": n, "sigma2": s2,
                 "fixed_design_expected_risk": fixed_risk,
                 "cp_best": int(deg[np.argmin(cp)]), "test_best": int(deg[np.argmin(d["test"])])})


def compute_coverhart():
    from scipy.stats import norm
    g = rng(1967)
    delta = 1.5
    bayes = float(norm.cdf(-delta / 2))
    xs = np.linspace(-6, 7.5, 6001)
    f0, f1 = norm.pdf(xs), norm.pdf(xs, delta)
    eta = f1 / (f0 + f1)
    px = 0.5 * (f0 + f1)
    nn_limit = float(np.sum(2 * eta * (1 - eta) * px) * (xs[1] - xs[0]))
    ns = [10, 30, 100, 300, 1000, 3000]
    reps = 20
    e1, ek = [], []
    yt = g.integers(0, 2, 12_000)
    xt = g.normal(delta * yt, 1.0)
    bayes_test = float(np.mean((xt > delta / 2).astype(int) != yt))  # the Bayes rule on this same test set
    for n in ns:
        a, b = [], []
        k = max(1, int(round(np.sqrt(n))))
        for _ in range(reps):
            y = g.integers(0, 2, n)
            x = g.normal(delta * y, 1.0)
            a.append(float(np.mean(L.knn_predict(x[:, None], y, xt[:, None], 1, classify=True) != yt)))
            b.append(float(np.mean(L.knn_predict(x[:, None], y, xt[:, None], k | 1, classify=True) != yt)))
        e1.append(float(np.mean(a)))
        ek.append(float(np.mean(b)))
    return nest({"delta": delta, "bayes": bayes, "nn_limit": nn_limit, "bound": 2 * bayes * (1 - bayes), "ns": ns, "bayes_test": bayes_test,
                 "err1": e1, "errk": ek})


def compute_robust():
    words, C, n, a, no = fed_matrix()
    known = (a == "HAMILTON") | (a == "MADISON")
    yk = (a[known] == "MADISON").astype(int)
    disp = a == "DISPUTED"
    out = {}
    drops = {"all words": [], "without upon": ["upon"], "without upon, whilst, there": ["upon", "whilst", "there"]}
    for name, drop in drops.items():
        keep = np.array([w not in drop for w in words])
        nb = L.PoissonNB().fit(C[known][:, keep], n[known], yk)
        lo = nb.log_odds(C[disp][:, keep], n[disp]) / np.log(10)
        loo = 0
        for i in range(known.sum()):
            m = np.ones(known.sum(), bool)
            m[i] = False
            nb_i = L.PoissonNB().fit(C[known][m][:, keep], n[known][m], yk[m])
            loo += int((nb_i.log_odds(C[known][i:i + 1, keep], n[known][i:i + 1])[0] > 0) != yk[i])
        out[name] = {"log10": lo, "n_madison": int((lo > 0).sum()), "loo_errors": loo, "dropped": drop}
    return nest({"papers": no[disp], "runs": out, "n_words": len(words)})


def compute_board():
    g = rng(19_000)
    hits = 0
    widths = []
    # Preserve the original training draws without a noisy finite reference test set.
    xt = g.uniform(0, 1, 20_000)
    _ = truth_curve(xt) + g.normal(0, 0.3, 20_000)
    for _ in range(R_BOARD):
        x = g.uniform(0, 1, 100)
        y = truth_curve(x) + g.normal(0, 0.3, 100)
        r = L.cv_score(lambda a, b, c: L.knn_predict(a, b, c, 10), x[:, None], y, 10, g)
        lo, hi = r["mean"] - 1.96 * r["se"], r["mean"] + 1.96 * r["se"]
        err = knn_population_risk(x, y, 10)
        hits += lo <= err <= hi
        widths.append(hi - lo)
    rows = [Row(19, r"10-fold CV $\pm$ 1.96 SE", r"$k$-NN test error, \ $n = 100$", "coverage", 0.95, hits / R_BOARD, R_BOARD)]
    save_rows(19, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "mean_width": float(np.mean(widths))}


ITEMS = {
    "rates": compute_rates, "poly": compute_poly, "biasvar": compute_biasvar, "cv": compute_cv, "curse": compute_curse,
    "nbvslr": compute_nbvslr, "tree": compute_tree, "lasso": compute_lasso, "metrics": compute_metrics,
    "decided": compute_decided, "leakage": compute_leakage, "reuse": compute_reuse, "nested": compute_nested, "cp": compute_cp, "coverhart": compute_coverhart, "robust": compute_robust, "costs": compute_costs, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
