"""statkit.optim: the algorithms behind the estimators, for Part 21 of *Statistics, Built* ("Optimization for
Statistics").

Newton's method with a backtracking line search; Fisher scoring for logistic regression; MM algorithms (Lange) for
least absolute deviations and quantile regression; the same problems as linear programs (HiGHS, through SciPy) and a
small dense simplex method that records the vertices it visits; the Neyman-Pearson lemma as a linear program;
proximal operators, ISTA and FISTA (Beck & Teboulle 2009); coordinate descent and the duality gap for the lasso;
ADMM (Boyd et al. 2011) for the lasso and the one-dimensional fused lasso; stochastic gradient with Robbins-Monro steps
and Polyak-Ruppert averaging.  Every routine returns its path, so a scene can draw it.  Checked in
``tests/test_stats_kit_optim.py``.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog


# ---------------------------------------------------------------------------------------------------------------------
# Newton's method and Fisher scoring
# ---------------------------------------------------------------------------------------------------------------------
def newton(f, grad, hess, x0, line_search: bool = True, tol: float = 1e-10, max_iter: int = 50, maximize: bool = False) -> dict:
    """Newton's method for a minimum (or a maximum with ``maximize=True``).  With ``line_search``, the step is halved
    until the objective improves (Armijo backtracking), and a non-descent Newton direction is replaced by the gradient
    direction.  Returns the path of iterates and objective values."""
    sgn = -1.0 if maximize else 1.0
    F = lambda x: sgn * f(x)  # noqa: E731
    G = lambda x: sgn * np.atleast_1d(grad(x))  # noqa: E731
    H = lambda x: sgn * np.atleast_2d(hess(x))  # noqa: E731
    x = np.atleast_1d(np.asarray(x0, float)).copy()
    path, vals = [x.copy()], [f(x)]
    for _ in range(max_iter):
        g, h = G(x), H(x)
        try:
            d = -np.linalg.solve(h, g)
        except np.linalg.LinAlgError:
            d = -g
        if line_search:
            if g @ d >= 0:  # not a descent direction (the Hessian is not positive definite here)
                d = -g
            t, f0 = 1.0, F(x)
            while F(x + t * d) > f0 + 1e-4 * t * (g @ d) and t > 1e-12:
                t /= 2
            x = x + t * d
        else:
            x = x + d
        path.append(x.copy())
        vals.append(f(x))
        if np.linalg.norm(d) < tol:
            break
    return {"x": x, "path": np.array(path), "values": np.array(vals), "iters": len(path) - 1}


def cauchy_location(x):
    """Log likelihood of a Cauchy location parameter, with its derivatives: a classic non-concave likelihood."""
    x = np.asarray(x, float)
    f = lambda t: float(-np.sum(np.log1p((x - np.atleast_1d(t)[0]) ** 2)))  # noqa: E731
    g = lambda t: np.array([np.sum(2 * (x - np.atleast_1d(t)[0]) / (1 + (x - np.atleast_1d(t)[0]) ** 2))])  # noqa: E731

    def h(t):
        u = x - np.atleast_1d(t)[0]
        return np.array([[np.sum(2 * (u ** 2 - 1) / (1 + u ** 2) ** 2)]])

    return f, g, h


def logistic_scoring(X, y, iters: int = 25, b0=None) -> dict:
    """Fisher scoring (= Newton, = IRLS for the canonical link) for logistic regression; the path and log likelihoods."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = np.zeros(X.shape[1]) if b0 is None else np.asarray(b0, float).copy()
    path, ll = [b.copy()], []
    for _ in range(iters):
        eta = X @ b
        p = 1 / (1 + np.exp(-eta))
        ll.append(float(np.sum(y * eta - np.logaddexp(0, eta))))
        W = p * (1 - p)
        step = np.linalg.solve(X.T @ (W[:, None] * X), X.T @ (y - p))
        b = b + step
        path.append(b.copy())
        if np.linalg.norm(step) < 1e-12:
            break
    eta = X @ b
    ll.append(float(np.sum(y * eta - np.logaddexp(0, eta))))
    p = 1 / (1 + np.exp(-eta))
    info = X.T @ ((p * (1 - p))[:, None] * X)
    return {"b": b, "path": np.array(path), "loglik": np.array(ll), "info": info, "se": np.sqrt(np.diag(np.linalg.inv(info)))}


# ---------------------------------------------------------------------------------------------------------------------
# Least absolute deviations and quantiles: MM, and linear programs
# ---------------------------------------------------------------------------------------------------------------------
def check_loss(r, tau: float) -> np.ndarray:
    r = np.asarray(r, float)
    return r * (tau - (r < 0))


def quantile_mm(X, y, tau: float = 0.5, iters: int = 200, eps: float = 1e-6, b0=None) -> dict:
    """Hunter & Lange's (2000) MM algorithm for quantile regression (tau = 0.5: least absolute deviations): each step
    is a weighted least squares with weights 1 / (eps + |r|), the minimizer of a quadratic majorizer of the check loss.
    The objective never increases."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = np.linalg.lstsq(X, y, rcond=None)[0] if b0 is None else np.asarray(b0, float).copy()
    path, obj = [b.copy()], [float(np.sum(check_loss(y - X @ b, tau)))]
    for _ in range(iters):
        r = y - X @ b
        w = 1 / (eps + np.abs(r))
        # majorizer of rho_tau(r) at r_k: r^2 / (4(eps + |r_k|)) + (tau - 1/2) r + const
        A = X.T @ (w[:, None] * X)
        b = np.linalg.solve(A, X.T @ (w * y) + 2 * (tau - 0.5) * X.sum(0))
        path.append(b.copy())
        obj.append(float(np.sum(check_loss(y - X @ b, tau))))
    return {"b": b, "path": np.array(path), "objective": np.array(obj)}


def quantile_lp(X, y, tau: float = 0.5) -> dict:
    """Quantile regression (tau = 0.5: LAD) as the linear program min tau 1'u + (1 - tau) 1'v subject to
    X b + u - v = y, u, v >= 0, solved by HiGHS."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    c = np.concatenate([np.zeros(p), tau * np.ones(n), (1 - tau) * np.ones(n)])
    A = np.hstack([X, np.eye(n), -np.eye(n)])
    bounds = [(None, None)] * p + [(0, None)] * (2 * n)
    r = linprog(c, A_eq=A, b_eq=y, bounds=bounds, method="highs")
    b = r.x[:p]
    return {"b": b, "objective": float(r.fun), "basic": np.flatnonzero(np.abs(y - X @ b) < 1e-7)}


def simplex(c, A, b, max_iter: int = 50) -> dict:
    """The simplex method (Dantzig 1947) for max c'x subject to Ax <= b, x >= 0, with b >= 0 (so the origin is a
    vertex), by a dense tableau and Dantzig's rule (the most positive reduced cost enters).  Returns the vertices
    visited, so the walk round the polytope can be drawn."""
    c, A, b = np.asarray(c, float), np.asarray(A, float), np.asarray(b, float)
    m, n = A.shape
    T = np.zeros((m + 1, n + m + 1))
    T[:m, :n], T[:m, n:n + m], T[:m, -1] = A, np.eye(m), b
    T[-1, :n] = -c
    basis = list(range(n, n + m))
    path = [np.zeros(n)]
    for _ in range(max_iter):
        j = int(np.argmin(T[-1, :-1]))
        if T[-1, j] >= -1e-12:
            break
        col = T[:m, j]
        ratios = np.where(col > 1e-12, T[:m, -1] / np.where(col > 1e-12, col, 1), np.inf)
        i = int(np.argmin(ratios))
        if not np.isfinite(ratios[i]):
            raise ValueError("unbounded")
        T[i] /= T[i, j]
        for k in range(m + 1):
            if k != i:
                T[k] -= T[k, j] * T[i]
        basis[i] = j
        x = np.zeros(n + m)
        x[basis] = T[:m, -1]
        path.append(x[:n].copy())
    return {"x": path[-1], "value": float(c @ path[-1]), "path": np.array(path), "dual": T[-1, n:n + m].copy()}


def neyman_pearson_lp(p0, p1, alpha: float) -> dict:
    """The most powerful level-alpha test on a finite sample space as a linear program (Dantzig & Wald 1951): choose
    phi(x) in [0, 1] to maximize sum phi p1 subject to sum phi p0 <= alpha.  The solution rejects where the likelihood
    ratio p1/p0 is largest, randomizing at one boundary point; the multiplier of the size constraint is the critical
    ratio k."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    r = linprog(-p1, A_ub=p0[None, :], b_ub=[alpha], bounds=[(0, 1)] * len(p0), method="highs")
    k = float(-r.ineqlin.marginals[0])
    return {"phi": r.x, "power": float(-r.fun), "size": float(p0 @ r.x), "k": k}


# ---------------------------------------------------------------------------------------------------------------------
# The lasso: proximal gradient, coordinate descent, duality, ADMM
# ---------------------------------------------------------------------------------------------------------------------
def prox_l1(v, t):
    """The proximal operator of t||.||_1: soft thresholding."""
    v = np.asarray(v, float)
    return np.sign(v) * np.maximum(np.abs(v) - t, 0.0)


def lasso_objective(X, y, b, lam: float) -> float:
    n = len(y)
    r = y - X @ b
    return float(r @ r / (2 * n) + lam * np.sum(np.abs(b)))


def ista(X, y, lam: float, iters: int = 500, accelerate: bool = False, b0=None) -> dict:
    """Proximal gradient for the lasso (1/2n)||y - Xb||^2 + lam||b||_1, step 1/L with L the largest eigenvalue of
    X'X/n.  ``accelerate=True`` is FISTA (Beck & Teboulle 2009): objective error O(1/k^2) instead of O(1/k)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    L = float(np.linalg.eigvalsh(X.T @ X / n).max())
    b = np.zeros(p) if b0 is None else np.asarray(b0, float).copy()
    z, t = b.copy(), 1.0
    obj, path = [lasso_objective(X, y, b, lam)], [b.copy()]
    for _ in range(iters):
        point = z if accelerate else b
        g = X.T @ (X @ point - y) / n
        b_new = prox_l1(point - g / L, lam / L)
        if accelerate:
            t_new = (1 + np.sqrt(1 + 4 * t * t)) / 2
            z = b_new + (t - 1) / t_new * (b_new - b)
            t = t_new
        b = b_new
        obj.append(lasso_objective(X, y, b, lam))
        path.append(b.copy())
    return {"b": b, "objective": np.array(obj), "path": np.array(path), "L": L}


def cd_lasso(X, y, lam: float, sweeps: int = 100, b0=None) -> dict:
    """Cyclic coordinate descent for the lasso: each coordinate's exact minimizer is a soft threshold of its partial
    residual correlation.  Records the objective after every coordinate update and every iterate."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    b = np.zeros(p) if b0 is None else np.asarray(b0, float).copy()
    r = y - X @ b
    col2 = (X ** 2).sum(0) / n
    obj, path = [lasso_objective(X, y, b, lam)], [b.copy()]
    for _ in range(sweeps):
        for j in range(p):
            r += X[:, j] * b[j]
            bj = prox_l1(X[:, j] @ r / n, lam) / col2[j]
            r -= X[:, j] * bj
            b[j] = bj
            obj.append(lasso_objective(X, y, b, lam))
            path.append(b.copy())
    return {"b": b, "objective": np.array(obj), "path": np.array(path)}


def lasso_dual_gap(X, y, b, lam: float) -> dict:
    """The lasso's dual: max_theta (1/2n)(||y||^2 - ||y - n theta||^2) subject to ||X'theta||_inf <= lam.  A feasible
    theta is the scaled residual; the gap primal - dual bounds the suboptimality of b."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n = len(y)
    r = (y - X @ b) / n
    s = min(1.0, lam / max(1e-15, float(np.abs(X.T @ r).max())))
    theta = s * r
    dual = float((y @ y - np.sum((y - n * theta) ** 2)) / (2 * n))
    primal = lasso_objective(X, y, b, lam)
    return {"primal": primal, "dual": dual, "gap": primal - dual, "theta": theta}


def admm_lasso(X, y, lam: float, rho: float = 1.0, iters: int = 300) -> dict:
    """ADMM for the lasso: split b = z; a ridge-like b-update, a soft-threshold z-update, a running dual u."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    A = X.T @ X / n + rho * np.eye(p)
    Xty = X.T @ y / n
    z = np.zeros(p)
    u = np.zeros(p)
    obj, rp, rd = [], [], []
    for _ in range(iters):
        b = np.linalg.solve(A, Xty + rho * (z - u))
        z_old = z
        z = prox_l1(b + u, lam / rho)
        u = u + b - z
        obj.append(lasso_objective(X, y, z, lam))
        rp.append(float(np.linalg.norm(b - z)))
        rd.append(float(rho * np.linalg.norm(z - z_old)))
    return {"b": z, "objective": np.array(obj), "primal_res": np.array(rp), "dual_res": np.array(rd)}


def fused_lasso_admm(y, lam: float, rho: float = 1.0, iters: int = 500) -> dict:
    """The one-dimensional fused lasso (total-variation denoising) min (1/2)||y - b||^2 + lam sum |b_i - b_{i-1}| by
    ADMM with the split z = Db (D the first-difference matrix)."""
    y = np.asarray(y, float)
    n = len(y)
    D = np.diff(np.eye(n), axis=0)
    M = np.eye(n) + rho * D.T @ D
    z = np.zeros(n - 1)
    u = np.zeros(n - 1)
    obj, rp = [], []
    for _ in range(iters):
        b = np.linalg.solve(M, y + rho * D.T @ (z - u))
        Db = D @ b
        z = prox_l1(Db + u, lam / rho)
        u = u + Db - z
        obj.append(float(0.5 * np.sum((y - b) ** 2) + lam * np.sum(np.abs(np.diff(b)))))
        rp.append(float(np.linalg.norm(Db - z)))
    return {"b": b, "objective": np.array(obj), "primal_res": np.array(rp)}


# ---------------------------------------------------------------------------------------------------------------------
# Stochastic gradient
# ---------------------------------------------------------------------------------------------------------------------
def sgd_logistic(X, y, step0: float = 1.0, power: float = 0.6, b0=None, average: bool = True) -> dict:
    """One pass of stochastic gradient ascent for logistic regression, one observation per step, with Robbins-Monro
    steps step0 / k^power (1/2 < power <= 1), and the Polyak-Ruppert average of the iterates."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    b = np.zeros(p) if b0 is None else np.asarray(b0, float).copy()
    avg = np.zeros(p)
    path, apath = np.empty((n, p)), np.empty((n, p))
    for k in range(n):
        x = X[k]
        g = (y[k] - 1 / (1 + np.exp(-x @ b))) * x
        b = b + step0 / (k + 1) ** power * g
        avg += (b - avg) / (k + 1)
        path[k], apath[k] = b, avg
    return {"b": b, "avg": avg, "path": path, "avg_path": apath}


def robbins_monro_quantile(x, tau: float = 0.5, step0: float = 1.0, power: float = 1.0, theta0: float = 0.0) -> dict:
    """Robbins & Monro (1951): find the root of E[1{X <= theta}] - tau, one observation at a time."""
    th = theta0
    path = np.empty(len(x))
    for k, v in enumerate(np.asarray(x, float)):
        th -= step0 / (k + 1) ** power * ((v <= th) - tau)
        path[k] = th
    return {"theta": th, "path": path}


# ---------------------------------------------------------------------------------------------------------------------
# Isotonic regression and Bradley-Terry
# ---------------------------------------------------------------------------------------------------------------------
def pava(y, w=None) -> dict:
    """The pool-adjacent-violators algorithm: the non-decreasing fit minimizing sum w_i (y_i - f_i)^2, the KKT
    solution of least squares under the order constraints f_1 <= ... <= f_n.  Returns the fit and the blocks pooled."""
    y = np.asarray(y, float)
    w = np.ones(len(y)) if w is None else np.asarray(w, float)
    blocks = []  # [value, weight, start, end]
    for i, (v, wi) in enumerate(zip(y, w)):
        blocks.append([v, wi, i, i])
        while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
            v2, w2, s2, _ = blocks.pop(-2)
            v1, w1, _, e1 = blocks.pop(-1)
            blocks.append([(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2, s2, e1])
    fit = np.empty(len(y))
    for v, _, s, e in blocks:
        fit[s:e + 1] = v
    return {"fit": fit, "blocks": [(int(s), int(e)) for _, _, s, e in blocks]}


def bradley_terry_mm(wins, iters: int = 200) -> dict:
    """Hunter's (2004) MM algorithm for the Bradley-Terry model P(i beats j) = g_i / (g_i + g_j): with W_i the total
    wins of i and n_ij the games between i and j, iterate g_i <- W_i / sum_j n_ij / (g_i + g_j), then normalize.  The
    log likelihood never decreases.  ``wins[i, j]`` counts i's wins over j."""
    wins = np.asarray(wins, float)
    n = wins + wins.T
    W = wins.sum(1)
    g = np.ones(len(W))
    path, ll = [g.copy()], []

    def loglik(g):
        P = g[:, None] / (g[:, None] + g[None, :])
        with np.errstate(divide="ignore"):
            return float(np.sum(wins * np.log(np.where(wins > 0, P, 1.0))))

    ll.append(loglik(g))
    for _ in range(iters):
        denom = (n / (g[:, None] + g[None, :])).sum(1)
        g = W / denom
        g = g / np.exp(np.mean(np.log(g)))
        path.append(g.copy())
        ll.append(loglik(g))
    return {"g": g, "path": np.array(path), "loglik": np.array(ll)}
