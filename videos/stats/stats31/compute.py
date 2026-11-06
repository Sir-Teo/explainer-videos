"""Precompute every number in Part 31 of *Statistics, Built* ("Multivariate Analysis").

    python -m videos.stats.stats31.compute            # everything missing (a few minutes)
    python -m videos.stats.stats31.compute --force board

Results are cached in ``.cache/stats31/<name>.json``.  The European road distances, the irises, the 24 tests, the
savings data and the arrests are the Museum's; the towns are the World's; the rest are seeded simulations.

Items:
    towns       the World's towns: road distances through a road network, and the map classical MDS rebuilds
    euro        Europe from 210 road distances
    mahal       Mahalanobis distances for the versicolor irises, against chi^2_4
    wishart     Bartlett's decomposition checked; sample-covariance eigenvalues against the truth
    hotelling   versicolor vs virginica: T^2 and its union-intersection direction; MANOVA on all three species
    pca         principal components of the US arrests (standardized) and of the irises
    fa          maximum-likelihood factor analysis of the 24 tests: k = 1..5, the LR tests, varimax loadings
    cca         canonical correlations: demography vs the economy in 50 countries
    lda         Fisher's discriminant, LDA and QDA on the irises
    cluster     k-means (with its path) and Gaussian mixtures on the irises; BIC for k = 1..6
    glasso      the graphical lasso on the 24 tests along a path of lambda
    board       Coverage Board rows: T^2 with chi^2 vs F calibration, and Bai--Saranadasa, as p/n grows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import sparse, stats
from scipy.sparse.csgraph import shortest_path

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import multi as M
from explainer.stats.world import World

CACHE = Cache("stats31")
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


def compute_towns():
    """Roads join each town to its 4 nearest neighbours; each road is 10-30% longer than the straight line (it winds);
    the road distance is the shortest path.  Classical MDS on those distances, aligned to the truth by Procrustes."""
    W = World()
    xy = W.towns["xy"]
    g = rng(1952)
    n = len(xy)
    E = np.sqrt(((xy[:, None] - xy[None]) ** 2).sum(-1))
    rows, cols, vals = [], [], []
    for i in range(n):
        for j in np.argsort(E[i])[1:5]:
            w = E[i, j] * g.uniform(1.1, 1.3)
            rows += [i, j]
            cols += [j, i]
            vals += [w, w]
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(n, n))
    D = shortest_path(A, directed=False)
    mds = M.classical_mds(D)
    pr = M.procrustes(xy, mds["X"])
    mds_e = M.classical_mds(E)
    edges = sorted({(min(i, j), max(i, j)) for i, j in zip(rows, cols)})
    return nest({"xy": xy, "region": W.towns["region"], "weight": W.towns["weight"], "fitted": pr["fitted"], "rmse": pr["rmse"],
                 "scale": pr["scale"], "eig": mds["eigenvalues"][:10], "explained": mds["explained"],
                 "negative_share": mds["negative_share"], "edges": edges, "detour": float(np.median((D / np.where(E > 0, E, 1))[E > 0])),
                 "exact_rmse": M.procrustes(xy, mds_e["X"])["rmse"], "n": n, "pairs": n * (n - 1) // 2})


def compute_euro():
    names, D = museum.eurodist()
    r = M.classical_mds(D)
    X = r["X"].copy()
    # orient as on a map: Stockholm north (y up), Lisbon west (x left)
    iS, iL = names.index("Stockholm"), names.index("Lisbon")
    if X[iS, 1] < X[:, 1].mean():
        X[:, 1] *= -1
    if X[iL, 0] > X[:, 0].mean():
        X[:, 0] *= -1
    # where the road distances disagree most with the 2-D map
    Dm = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    iu = np.triu_indices(len(D), 1)
    err = (Dm - D)[iu]
    k = np.argsort(-np.abs(err))[:3]
    worst = [(names[iu[0][j]], names[iu[1][j]], float(D[iu][j]), float(Dm[iu][j])) for j in k]
    return nest({"names": names, "X": X, "eig": r["eigenvalues"], "explained": r["explained"], "negative_share": r["negative_share"],
                 "worst": worst, "stress": float(np.sqrt(np.sum(err ** 2) / np.sum(D[iu] ** 2)))})


def compute_mahal():
    X, y, names = museum.iris()
    V = X[y == 1]
    d2 = M.mahalanobis(V, V.mean(0), np.cov(V.T)) ** 2
    q = stats.chi2.ppf((np.arange(1, len(d2) + 1) - 0.5) / len(d2), 4)
    e2 = np.sum((V - V.mean(0)) ** 2, 1)
    two = V[:, [2, 3]]
    return nest({"d2": np.sort(d2), "q": q, "eucl": e2, "maha": d2, "two": two, "mean2": two.mean(0), "cov2": np.cov(two.T),
                 "far_eucl": int(np.argmax(e2)), "far_maha": int(np.argmax(d2)), "cut": float(stats.chi2.ppf(0.975, 4))})


def compute_wishart():
    g = rng(1928)
    S = np.array([[2.0, 0.8, 0.0], [0.8, 1.0, 0.3], [0.0, 0.3, 0.5]])
    df = 10
    Ws = np.array([M.wishart_bartlett(S, df, g) for _ in range(20000)])
    mean = Ws.mean(0) / df
    var11 = float(Ws[:, 0, 0].var())
    th11 = 2 * df * S[0, 0] ** 2
    var12 = float(Ws[:, 0, 1].var())
    th12 = df * (S[0, 1] ** 2 + S[0, 0] * S[1, 1])
    # eigenvalue spread: Sigma = I_p, p = 50, n = 100
    p, n = 50, 100
    Z = g.standard_normal((n, p))
    ev = np.linalg.eigvalsh(np.cov(Z.T))
    gam = p / n
    a, b = (1 - math.sqrt(gam)) ** 2, (1 + math.sqrt(gam)) ** 2
    xs = np.linspace(a, b, 200)
    mp = np.sqrt((b - xs) * (xs - a)) / (2 * math.pi * gam * xs)
    return nest({"S": S, "df": df, "mean": mean, "var11": var11, "th11": th11, "var12": var12, "th12": th12, "ev": ev,
                 "mp_x": xs, "mp_y": mp, "mp_ab": [a, b], "p": p, "n": n})


def compute_hotelling():
    X, y, names = museum.iris()
    h = M.hotelling_two(X[y == 1], X[y == 2])
    t_uni = [float(stats.ttest_ind(X[y == 1][:, j], X[y == 2][:, j]).statistic) for j in range(4)]
    a = h["direction"] / np.linalg.norm(h["direction"])
    proj = {"versicolor": X[y == 1] @ a, "virginica": X[y == 2] @ a}
    tmax = float(stats.ttest_ind(proj["versicolor"], proj["virginica"]).statistic)
    mv = M.manova(X, y)
    return nest({"T2": h["T2"], "F": h["F"], "df": h["df"], "p": h["p"], "t_uni": t_uni, "direction": a, "tmax": tmax,
                 "proj": proj, "manova": {k: mv[k] for k in ("wilks", "pillai", "hotelling_lawley", "roy", "wilks_F", "wilks_df", "eigen")}})


def compute_pca():
    states, A, names = museum.usarrests()
    p = M.pca(A, standardize=True)
    X, y, inames = museum.iris()
    q = M.pca(X)
    qs = M.pca(X, standardize=True)
    return nest({"states": states, "names": names, "scores": p["scores"], "loadings": p["loadings"], "var": p["variances"],
                 "explained": p["explained"], "iris_scores": q["scores"], "iris_explained": q["explained"],
                 "iris_loadings": q["loadings"], "iris_std_explained": qs["explained"], "y": y})


def compute_fa():
    names, R, n = museum.harman74()
    fits = {}
    for k in range(1, 6):
        f = M.factor_ml(R, k, n)
        fits[k] = {"chi2": f["chi2"], "df": f["df"], "p": f["p"], "heywood": f["heywood"]}
    f4 = M.factor_ml(R, 4, n)
    v = M.varimax(f4["loadings"])
    L = v["loadings"]
    # orient each factor positively, order as in Harman: verbal, spatial, speed, memory by largest loading
    L = L * np.sign(L.sum(0))[None, :]
    ev = np.sort(np.linalg.eigvalsh(R))[::-1]
    pc = M.pca(np.linalg.cholesky(R).T * math.sqrt(n - 1) + 0)  # not used for data; eigen only
    del pc
    return nest({"names": names, "fits": fits, "loadings_raw": f4["loadings"], "loadings": L, "uniqueness": f4["uniqueness"],
                 "communality": f4["communality"], "eig": ev, "n": n})


def compute_cca():
    countries, L, cols = museum.lifecycle()
    X, Y = L[:, [1, 2]], L[:, [0, 3, 4]]
    r = M.cca(X, Y)
    # principal angles
    ang = np.degrees(np.arccos(np.clip(r["r"], -1, 1)))
    corrX = np.corrcoef(np.column_stack([X, r["u"]]).T)[:2, 2:]
    corrY = np.corrcoef(np.column_stack([Y, r["v"]]).T)[:3, 3:]
    return nest({"countries": countries, "r": r["r"], "tests": r["tests"], "u": r["u"], "v": r["v"], "angles": ang,
                 "structX": corrX, "structY": corrY, "xnames": ["pop15", "pop75"], "ynames": ["sr", "dpi", "ddpi"]})


def compute_lda():
    X, y, names = museum.iris()
    f = M.lda_fit(X, y)
    proj = X @ f["directions"]
    train_lda = float(np.mean(M.lda_predict(f, X) != y))
    q = M.qda_fit(X, y)
    train_qda = float(np.mean(M.qda_predict(q, X) != y))
    # a two-variable picture: petal length and width, LDA boundaries on a grid
    X2 = X[:, [2, 3]]
    f2 = M.lda_fit(X2, y)
    q2 = M.qda_fit(X2, y)
    gx, gy = np.meshgrid(np.linspace(0.5, 7.5, 141), np.linspace(-0.2, 2.8, 61))
    G = np.column_stack([gx.ravel(), gy.ravel()])
    return nest({"proj": proj, "y": y, "eigen": f["eigen"], "share": f["eigen"][:2] / np.sum(f["eigen"][:2]),
                 "train_lda": train_lda, "train_qda": train_qda, "loo_lda": M.loo_error(X, y, "lda"),
                 "loo_qda": M.loo_error(X, y, "qda"), "grid_x": gx[0], "grid_y": gy[:, 0],
                 "lda2": M.lda_predict(f2, G).reshape(gx.shape), "qda2": M.qda_predict(q2, G).reshape(gx.shape),
                 "loo2_lda": M.loo_error(X2, y, "lda"), "loo2_qda": M.loo_error(X2, y, "qda"), "X2": X2,
                 "directions": f["directions"]})


def compute_cluster():
    X, y, names = museum.iris()
    X2 = X[:, [2, 3]]
    g = rng(1967)
    km2 = M.kmeans(X2, 3, rng(5), n_init=1)
    km = M.kmeans(X, 3, g)
    gm = M.gmm_em(X, 3, g)
    bic = {k: M.gmm_em(X, k, rng(100 + k))["bic"] for k in range(1, 7)}
    wss = {k: M.kmeans(X, k, rng(200 + k))["wss"] for k in range(1, 9)}
    return nest({"X2": X2, "y": y, "path": km2["path"], "labels2": km2["labels"], "ari_km": M.adjusted_rand(km["labels"], y),
                 "ari_gmm": M.adjusted_rand(gm["labels"], y), "bic": bic, "wss": wss, "gmm_labels": gm["labels"],
                 "km_labels": km["labels"], "gmm_means2": gm["means"][:, [2, 3]], "gmm_covs2": gm["covs"][:, [2, 3]][:, :, [2, 3]]})


def compute_lloyd():
    """Lloyd's algorithm on petal length and width from a deliberately poor start: two centres among the setosas."""
    X, y, names = museum.iris()
    X2 = X[:, [2, 3]]
    C = np.array([[1.3, 0.2], [1.7, 0.4], [6.6, 2.3]])
    cents, labs, wss = [C.copy()], [], []
    for _ in range(30):
        L = np.argmin(((X2[:, None, :] - C[None]) ** 2).sum(-1), 1)
        labs.append(L)
        wss.append(float(((X2 - C[L]) ** 2).sum()))
        Cn = np.array([X2[L == j].mean(0) for j in range(3)])
        if np.allclose(Cn, C):
            break
        C = Cn
        cents.append(C.copy())
    return nest({"X2": X2, "y": y, "centres": np.array(cents), "labels": np.array(labs), "wss": wss,
                 "ari": M.adjusted_rand(labs[-1], y)})


def compute_glasso():
    names, R, n = museum.harman74()
    lams = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    path = {}
    for lam in lams:
        gl = M.graphical_lasso(R, lam)
        T = gl["precision"]
        d = np.sqrt(np.diag(T))
        pc = -T / np.outer(d, d)
        path[f"{lam:g}"] = {"edges": gl["edges"], "pcor": pc}
    pc_full = M.partial_correlations(R)
    iu = np.triu_indices(24, 1)
    return nest({"names": names, "lams": lams, "path": path, "pcor_full": pc_full, "corr_mean": float(np.mean(R[iu])),
                 "pcor_small": float(np.mean(np.abs(pc_full[iu]) < 0.1))})


def compute_board():
    g = rng(2008)
    n = 50
    reps = 2000
    res = {}
    for p in (2, 10, 25, 40):
        r_chi, r_f, r_bs = 0, 0, 0
        for _ in range(reps):
            X = g.standard_normal((n, p))
            Y = g.standard_normal((n, p))
            h = M.hotelling_two(X, Y)
            r_chi += h["p_chi2"] < 0.05
            r_f += h["p"] < 0.05
            r_bs += M.bai_saranadasa(X, Y)["p"] < 0.05
        res[p] = {"chi2": r_chi / reps, "F": r_f / reps, "bs": r_bs / reps}
    # power with a spread-out shift: delta = 0.25 in every coordinate, p = 40
    pw = {}
    for p in (10, 25, 40, 90):
        a_f, a_bs = 0, 0
        for _ in range(500):
            X = g.standard_normal((n, p)) + 0.15
            Y = g.standard_normal((n, p))
            if p < 2 * n - 2:
                a_f += M.hotelling_two(X, Y)["p"] < 0.05
            a_bs += M.bai_saranadasa(X, Y)["p"] < 0.05
        pw[p] = {"F": a_f / 500 if p < 2 * n - 2 else None, "bs": a_bs / 500}
    rows = [Row(31, r"$T^2$ with a $\chi^2_p$ calibration", rf"two samples of {n}, \ $p = {p}$", "size", 0.05, res[p]["chi2"], reps)
            for p in (2, 25)]
    rows.append(Row(31, r"$T^2$ with a $\chi^2_p$ calibration", rf"two samples of {n}, \ $p = 40$", "size", 0.05, res[40]["chi2"], reps))
    rows.append(Row(31, r"$T^2$ with the exact $F$", rf"two samples of {n}, \ $p = 40$", "size", 0.05, res[40]["F"], reps))
    rows.append(Row(31, r"Bai--Saranadasa", rf"two samples of {n}, \ $p = 40$", "size", 0.05, res[40]["bs"], reps))
    save_rows(31, rows)
    return nest({"n": n, "reps": reps, "res": res, "power": pw,
                 "rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


ITEMS = {
    "towns": compute_towns, "euro": compute_euro, "mahal": compute_mahal, "wishart": compute_wishart,
    "hotelling": compute_hotelling, "pca": compute_pca, "fa": compute_fa, "cca": compute_cca, "lda": compute_lda,
    "cluster": compute_cluster, "lloyd": compute_lloyd, "glasso": compute_glasso, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
