"""statkit.shift: robustness and distribution shift (Part 60 of *Statistics, Built*).

    Tukey's halfspace depth in the plane and the Tukey median                         (Tukey 1975)
    robust means in high dimensions: coordinatewise median, geometric median, the spectral filter
                                                               (Diakonikolas et al. 2016; Lai, Rao & Vempala 2016)
    list-decodable mean estimation by clustering                                     (Charikar, Steinhardt & Valiant 2017)
    median of means in high dimensions                                               (Lugosi & Mendelson 2019)
    importance weighting under covariate shift, effective sample size, weighted intervals
    label shift: black-box shift estimation and the EM correction        (Lipton, Wang & Smola 2018; Saerens et al. 2002)
    distributionally robust risk over chi-square and KL balls, by duality               (Duchi & Namkoong 2021)
    invariant causal prediction and anchor regression          (Peters, Buhlmann & Meinshausen 2016; Rothenhausler et al. 2021)
    transfer learning for sparse regression, the two-step Trans-Lasso                    (Li, Cai & Li 2022)
    detecting shift: MMD and classifier two-sample tests                              (Gretton et al. 2012)
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats

# ----------------------------------------------------------------------------------------------------- depth


def tukey_depth_2d(points, data, n_dirs: int = 720) -> np.ndarray:
    """Tukey's halfspace depth of each point among ``data`` in the plane: the smallest fraction of data in a closed
    halfplane containing the point, minimized over ``n_dirs`` directions (exact as n_dirs grows)."""
    P, X = np.atleast_2d(np.asarray(points, float)), np.asarray(data, float)
    th = np.linspace(0, math.pi, n_dirs, endpoint=False)
    U = np.stack([np.cos(th), np.sin(th)], 1)
    px = X @ U.T  # n x dirs
    out = np.empty(len(P))
    for i, p in enumerate(P):
        pp = p @ U.T
        above = np.mean(px >= pp[None, :] - 1e-12, axis=0)
        below = np.mean(px <= pp[None, :] + 1e-12, axis=0)
        out[i] = float(np.min(np.minimum(above, below)))
    return out


def tukey_median_2d(data, grid: int = 60) -> dict:
    """The Tukey median: the point of maximal depth, searched on a grid over the data's bounding box (the centroid of
    the deepest cells)."""
    X = np.asarray(data, float)
    lo, hi = X.min(0), X.max(0)
    gx = np.linspace(lo[0], hi[0], grid)
    gy = np.linspace(lo[1], hi[1], grid)
    G = np.array([[a, b] for a in gx for b in gy])
    D = tukey_depth_2d(G, X, 360)
    best = G[D >= D.max() - 1e-12]
    return {"median": best.mean(0), "depth": float(D.max()), "grid": G, "depth_grid": D}


# ---------------------------------------------------------------------------------------- robust means in R^d


def contaminate(n: int, d: int, eps: float, rng: np.random.Generator, value: float = 2.0) -> dict:
    """n points from N(0, I_d), of which a fraction eps is replaced by an adversary's tight cluster with every coordinate
    equal to ``value``: each coordinate's median moves by about 1.25 eps, so the coordinatewise median errs by about
    1.25 eps sqrt(d), and the mean by value * eps * sqrt(d)."""
    X = rng.standard_normal((n, d))
    k = int(round(eps * n))
    X[:k] = value + 0.1 * rng.standard_normal((k, d))
    return {"X": X, "bad": np.arange(n) < k}


def geometric_median(X, iters: int = 200, tol: float = 1e-9) -> np.ndarray:
    """Weiszfeld's algorithm."""
    X = np.asarray(X, float)
    m = np.median(X, axis=0)
    for _ in range(iters):
        d = np.linalg.norm(X - m, axis=1)
        w = 1 / np.maximum(d, 1e-12)
        mn = (w[:, None] * X).sum(0) / w.sum()
        if np.linalg.norm(mn - m) < tol:
            return mn
        m = mn
    return m


def filter_mean(X, eps: float, max_iter: int = 200) -> dict:
    """A simple spectral filter (in the spirit of Diakonikolas et al. 2016): while the top eigenvalue of the empirical
    covariance exceeds 1 + C eps log(1/eps), project on its eigenvector and remove the points whose projections are
    the most extreme (a random fraction scaled by their squared deviation).  Returns the filtered mean."""
    X = np.asarray(X, float)
    keep = np.ones(len(X), bool)
    rounds = 0
    for _ in range(max_iter):
        Y = X[keep]
        thr = (1 + math.sqrt(X.shape[1] / len(Y))) ** 2 + 2 * eps * math.log(1 / eps)  # the clean spectrum's edge, plus slack
        mu = Y.mean(0)
        C = np.cov(Y.T)
        w, V = np.linalg.eigh(C)
        if w[-1] <= thr:
            break
        v = V[:, -1]
        proj = (Y - mu) @ v
        s = proj ** 2
        # remove the points with the largest squared projections, about half an eps fraction per round
        k = max(1, int(0.5 * eps * len(Y)))
        idx = np.flatnonzero(keep)
        keep[idx[np.argsort(-s)[:k]]] = False
        rounds += 1
    return {"mean": X[keep].mean(0), "kept": keep, "rounds": rounds}


def robust_mean_errors(n: int, d: int, eps: float, rng: np.random.Generator, value: float = 2.0) -> dict:
    """The error ||mu_hat - 0|| of the sample mean, coordinatewise median, geometric median and filter on one
    contaminated sample."""
    c = contaminate(n, d, eps, rng, value)
    X = c["X"]
    f = filter_mean(X, eps)
    return {"mean": float(np.linalg.norm(X.mean(0))), "coord_median": float(np.linalg.norm(np.median(X, 0))),
            "geo_median": float(np.linalg.norm(geometric_median(X))), "filter": float(np.linalg.norm(f["mean"])),
            "removed_bad": float(np.mean(~f["kept"][c["bad"]])) if c["bad"].any() else 0.0,
            "removed_good": float(np.mean(~f["kept"][~c["bad"]])), "oracle": float(np.linalg.norm(X[~c["bad"]].mean(0)))}


def list_decode(X, alpha: float, rng: np.random.Generator, restarts: int = 5) -> np.ndarray:
    """List-decodable mean estimation when only a fraction alpha of the points are inliers: output a short list of
    candidate means (k-means with k = ceil(1/alpha) centres, best of several restarts); one of them is near the
    inliers' mean."""
    X = np.asarray(X, float)
    k = int(math.ceil(1 / alpha))
    best, cost = None, np.inf
    for _ in range(restarts):
        C = X[rng.choice(len(X), k, replace=False)]
        for _ in range(100):
            lab = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(2), 1)
            Cn = np.array([X[lab == j].mean(0) if np.any(lab == j) else C[j] for j in range(k)])
            if np.allclose(Cn, C):
                break
            C = Cn
        cst = float(((X - C[lab]) ** 2).sum())
        if cst < cost:
            best, cost = C, cst
    return best


def median_of_means(X, k: int, rng: np.random.Generator) -> np.ndarray:
    """Split into k blocks, average each, and take the geometric median of the block means (Minsker; Lugosi &
    Mendelson): sub-Gaussian deviations with only two moments."""
    X = np.asarray(X, float)
    o = rng.permutation(len(X))
    blocks = np.array_split(o, k)
    M = np.array([X[b].mean(0) for b in blocks])
    return geometric_median(M)


# ---------------------------------------------------------------------------------------------- covariate shift


def kish_ess(w) -> float:
    """Kish's effective sample size (sum w)^2 / sum w^2."""
    w = np.asarray(w, float)
    return float(w.sum() ** 2 / np.sum(w * w))


def weighted_mean_ci(y, w, alpha: float = 0.05) -> dict:
    """Self-normalized importance-weighted mean and its delta-method interval."""
    y, w = np.asarray(y, float), np.asarray(w, float)
    W = w / w.sum()
    m = float(np.sum(W * y))
    se = float(math.sqrt(np.sum(W * W * (y - m) ** 2)))
    z = stats.norm.isf(alpha / 2)
    return {"mean": m, "lo": m - z * se, "hi": m + z * se, "se": se, "ess": kish_ess(w)}


def logistic_density_ratio(Xs, Xt, lam: float = 1e-3, iters: int = 50) -> callable:
    """Estimate w(x) = p_target(x)/p_source(x) by a logistic classifier of target against source (with an intercept),
    w = (n_s/n_t) exp(eta(x)).  Returns a function of new x."""
    Xs, Xt = np.atleast_2d(Xs), np.atleast_2d(Xt)
    Z = np.vstack([Xs, Xt])
    Z1 = np.column_stack([np.ones(len(Z)), Z])
    y = np.r_[np.zeros(len(Xs)), np.ones(len(Xt))]
    b = np.zeros(Z1.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(Z1 @ b)))
        g = Z1.T @ (y - p) - lam * np.r_[0, b[1:]]
        H = (Z1 * (p * (1 - p))[:, None]).T @ Z1 + lam * np.diag(np.r_[0, np.ones(len(b) - 1)])
        step = np.linalg.solve(H, g)
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    ratio = len(Xs) / len(Xt)
    return lambda X: ratio * np.exp(np.column_stack([np.ones(len(np.atleast_2d(X))), np.atleast_2d(X)]) @ b)


# -------------------------------------------------------------------------------------------------- label shift


def bbse_weights(pred_src, y_src, pred_tgt, K: int) -> dict:
    """Black-box shift estimation (Lipton, Wang & Smola 2018): with C[i, j] = P_source(predict i, label j) and
    mu[i] = P_target(predict i), the class weights w = q(y)/p(y) solve C w = mu.  Returns w and the implied target
    class proportions."""
    pred_src, y_src, pred_tgt = (np.asarray(a, int) for a in (pred_src, y_src, pred_tgt))
    C = np.zeros((K, K))
    for i, j in zip(pred_src, y_src):
        C[i, j] += 1
    C /= len(y_src)
    mu = np.bincount(pred_tgt, minlength=K) / len(pred_tgt)
    w = np.linalg.lstsq(C, mu, rcond=None)[0]
    w = np.maximum(w, 0)
    p_src = np.bincount(y_src, minlength=K) / len(y_src)
    q = w * p_src
    q = q / q.sum()
    return {"w": w, "q": q, "C": C, "mu": mu}


def em_label_shift(probs_tgt, p_src, iters: int = 200) -> dict:
    """Saerens, Latinne & Decaestecker's (2002) EM: re-weight the source-calibrated posteriors by q/p and update the
    target priors q as the average reweighted posterior, to a fixed point."""
    P = np.asarray(probs_tgt, float)
    p = np.asarray(p_src, float)
    q = p.copy()
    for _ in range(iters):
        R = P * (q / p)[None, :]
        R /= R.sum(1, keepdims=True)
        qn = R.mean(0)
        if np.max(np.abs(qn - q)) < 1e-12:
            q = qn
            break
        q = qn
    return {"q": q, "posterior": R}


# -------------------------------------------------------------------------------------------------------- DRO


def dro_chi2(losses, rho: float) -> float:
    """sup E_Q[loss] over Q with chi-square divergence D(Q || P_n) <= rho/2... in the Duchi-Namkoong form
    {Q: (1/2) E_P[(dQ/dP - 1)^2] <= rho}: computed exactly by its dual over the weights (a convex program on the
    simplex), which for small rho equals mean + sqrt(2 rho var)."""
    l = np.asarray(losses, float)
    n = len(l)
    # maximize sum q_i l_i s.t. sum q = 1, q >= 0, (n/2) sum (q_i - 1/n)^2 <= rho
    m, s = l.mean(), l.std()
    if s == 0:
        return float(m)
    # without the nonnegativity constraint the maximizer is q = 1/n + c (l - m), c = sqrt(2 rho / (n * sum (l-m)^2/ n ... ))
    c = math.sqrt(2 * rho / n) / (s * math.sqrt(n))
    q = 1 / n + c * (l - m)
    if np.all(q >= 0):
        return float(np.sum(q * l))
    # otherwise solve the small convex program
    cons = [{"type": "eq", "fun": lambda q: q.sum() - 1}, {"type": "ineq", "fun": lambda q: rho - 0.5 * n * np.sum((q - 1 / n) ** 2)}]
    r = optimize.minimize(lambda q: -q @ l, np.full(n, 1 / n), constraints=cons, bounds=[(0, 1)] * n, method="SLSQP")
    return float(r.x @ l)


def dro_kl(losses, rho: float) -> float:
    """sup E_Q[loss] over KL(Q || P_n) <= rho, by its dual inf_{lam > 0} lam log E exp(loss/lam) + lam rho."""
    l = np.asarray(losses, float)

    def dual(t):
        lam = math.exp(t)
        mx = l.max()
        return lam * (math.log(np.mean(np.exp((l - mx) / lam))) + mx / lam) + lam * rho
    r = optimize.minimize_scalar(dual, bounds=(-8, 8), method="bounded")
    return float(r.fun)


# --------------------------------------------------------------------------------------------------- invariance


def anchor_regression(X, y, A, gamma: float) -> np.ndarray:
    """Anchor regression (Rothenhausler, Meinshausen, Buhlmann & Peters 2021): least squares after the transform
    W = I - (1 - sqrt(gamma)) P_A, with P_A the projection onto the anchors' column space.  gamma = 1 is OLS,
    gamma -> infinity approaches instrumental-variable regression, gamma = 0 partials the anchors out."""
    X, y, A = np.asarray(X, float), np.asarray(y, float), np.atleast_2d(np.asarray(A, float))
    if A.shape[0] != len(y):
        A = A.T
    P = A @ np.linalg.pinv(A)
    W = np.eye(len(y)) - (1 - math.sqrt(gamma)) * P
    return np.linalg.lstsq(W @ X, W @ y, rcond=None)[0]


def icp(X, y, env, alpha: float = 0.05) -> dict:
    """Invariant causal prediction (Peters, Buhlmann & Meinshausen 2016) for few predictors: for every subset S, test
    whether the residuals of y on X_S have the same mean and variance in every environment (ANOVA F and Levene's
    test, Bonferroni-combined); the estimate is the intersection of all accepted subsets."""
    X, y, env = np.asarray(X, float), np.asarray(y, float), np.asarray(env)
    n, p = X.shape
    from itertools import combinations

    accepted = []
    pvals = {}
    for k in range(p + 1):
        for S in combinations(range(p), k):
            Z = np.column_stack([np.ones(n)] + [X[:, j] for j in S])
            b = np.linalg.lstsq(Z, y, rcond=None)[0]
            r = y - Z @ b
            groups = [r[env == e] for e in np.unique(env)]
            p1 = stats.f_oneway(*groups).pvalue
            p2 = stats.levene(*groups).pvalue
            pv = min(1.0, 2 * min(p1, p2))
            pvals[S] = pv
            if pv > alpha:
                accepted.append(set(S))
    est = set.intersection(*accepted) if accepted else set()
    return {"estimate": sorted(est), "accepted": [sorted(a) for a in accepted], "pvals": {str(k): v for k, v in pvals.items()}}


# ------------------------------------------------------------------------------------------------------ transfer


def trans_lasso(Xs, ys, Xt, yt, lam_w: float | None = None, lam_d: float | None = None) -> dict:
    """The oracle Trans-Lasso of Li, Cai & Li (2022): (1) a lasso on the pooled source and target data estimates
    a coefficient w close to both; (2) a lasso of the target's residuals y_t - X_t w on X_t estimates the sparse
    difference.  Returns the transfer estimate w + delta, and the target-only and pooled lassos for comparison, with
    the theory's penalties sqrt(2 log p / n) (unit noise) unless given."""
    from .sparse import lasso_cd

    Xs, ys, Xt, yt = (np.asarray(a, float) for a in (Xs, ys, Xt, yt))
    p = Xt.shape[1]
    Xp, yp = np.vstack([Xs, Xt]), np.r_[ys, yt]
    lw = lam_w if lam_w is not None else math.sqrt(2 * math.log(p) / len(yp))
    ld = lam_d if lam_d is not None else math.sqrt(2 * math.log(p) / len(yt))
    w = lasso_cd(Xp, yp, lw)
    d = lasso_cd(Xt, yt - Xt @ w, ld)
    return {"transfer": w + d, "pooled": w, "target": lasso_cd(Xt, yt, ld)}


# ------------------------------------------------------------------------------------------------ detecting shift


def mmd2(X, Y, bw: float | None = None) -> float:
    """The unbiased squared MMD with a Gaussian kernel (median heuristic bandwidth)."""
    X, Y = np.atleast_2d(X), np.atleast_2d(Y)
    Z = np.vstack([X, Y])
    D = ((Z[:, None, :] - Z[None]) ** 2).sum(2)
    if bw is None:
        bw = math.sqrt(np.median(D[np.triu_indices(len(Z), 1)]) / 2)
    K = np.exp(-D / (2 * bw * bw))
    n, m = len(X), len(Y)
    Kxx, Kyy, Kxy = K[:n, :n], K[n:, n:], K[:n, n:]
    return float((Kxx.sum() - np.trace(Kxx)) / (n * (n - 1)) + (Kyy.sum() - np.trace(Kyy)) / (m * (m - 1)) - 2 * Kxy.mean())


def mmd_test(X, Y, rng: np.random.Generator, perms: int = 300) -> dict:
    """A permutation test of P = Q with the MMD statistic."""
    X, Y = np.atleast_2d(X), np.atleast_2d(Y)
    obs = mmd2(X, Y)
    Z = np.vstack([X, Y])
    n = len(X)
    null = []
    for _ in range(perms):
        o = rng.permutation(len(Z))
        null.append(mmd2(Z[o[:n]], Z[o[n:]]))
    null = np.asarray(null)
    return {"mmd2": obs, "p": float((1 + np.sum(null >= obs)) / (1 + perms)), "null": null}
