"""The House's portfolio optimizer (Part 30): covariance estimators, the classical and robust allocations, and the
theory of what estimation error does to them.

Covariance: the sample matrix; Ledoit and Wolf's linear shrinkage toward a scaled identity (2004a) and toward constant
correlation (2004b); eigenvalue clipping at the Marchenko-Pastur edge (Laloux, Cizeau, Bouchaud and Potters 1999);
Ledoit and Wolf's analytical nonlinear shrinkage (2020).  Allocations: the global minimum-variance portfolio (and its
long-only version), mean-variance and tangency, Black-Litterman, equal risk contributions, hierarchical risk parity
(López de Prado 2016), minimum CVaR as a linear program (Rockafellar and Uryasev 2000), the growth-optimal (Kelly)
portfolio, Cover's universal portfolio for two assets, Meucci's entropy pooling and Fernholz's diversity weights.
Theory: the exact in- and out-of-sample variance of the sample minimum-variance portfolio under normal returns.

Every function takes returns as a (T x N) array of periods by assets and covariance matrices as (N x N) arrays.
"""

from __future__ import annotations

import math

import numpy as np

# ---------------------------------------------------------------------------
# Covariance
# ---------------------------------------------------------------------------


def sample_cov(R) -> np.ndarray:
    """The sample covariance (divisor T - 1)."""
    R = np.asarray(R, float)
    return np.cov(R, rowvar=False)


def lw_identity(R):
    """Ledoit and Wolf (2004a): shrink the sample covariance toward m I, m = tr(S)/N, with the estimated optimal
    intensity.  Returns (Sigma, intensity)."""
    X = np.asarray(R, float)
    X = X - X.mean(0)
    n, p = X.shape
    S = X.T @ X / n
    m = np.trace(S) / p
    d2 = np.sum((S - m * np.eye(p)) ** 2) / p
    b2 = sum(np.sum((np.outer(x, x) - S) ** 2) for x in X) / p / n ** 2
    b2 = min(b2, d2)
    k = b2 / d2 if d2 > 0 else 1.0
    return k * m * np.eye(p) + (1 - k) * S, float(k)


def lw_constcorr(R):
    """Ledoit and Wolf (2004b), `Honey, I shrunk the sample covariance matrix': shrink toward the constant-correlation
    matrix with the estimated optimal intensity.  Returns (Sigma, intensity)."""
    Y = np.asarray(R, float)
    Y = Y - Y.mean(0)
    n, p = Y.shape
    S = Y.T @ Y / n
    var = np.diag(S).copy()
    sd = np.sqrt(var)
    C = S / np.outer(sd, sd)
    rbar = (C.sum() - p) / (p * (p - 1))
    F = rbar * np.outer(sd, sd)
    np.fill_diagonal(F, var)
    Y2 = Y ** 2
    pi_mat = Y2.T @ Y2 / n - S ** 2
    pi_hat = pi_mat.sum()
    gamma_hat = np.sum((F - S) ** 2)
    rho_diag = np.trace(pi_mat)
    theta = (Y ** 3).T @ Y / n - var[:, None] * S
    np.fill_diagonal(theta, 0.0)
    rho_off = rbar * np.sum(np.outer(1 / sd, sd) * theta)
    kappa = (pi_hat - (rho_diag + rho_off)) / gamma_hat
    k = float(max(0.0, min(1.0, kappa / n)))
    return k * F + (1 - k) * S, k


def mp_edges(gamma: float, sigma2: float = 1.0):
    """The Marchenko-Pastur support [(1 - sqrt g)^2, (1 + sqrt g)^2] sigma^2 for N/T = g."""
    return sigma2 * (1 - math.sqrt(gamma)) ** 2, sigma2 * (1 + math.sqrt(gamma)) ** 2


def rmt_clip(R):
    """Eigenvalue clipping of the correlation matrix (Laloux et al. 1999): eigenvalues below the Marchenko-Pastur upper
    edge (1 + sqrt(N/T))^2 are noise and are replaced by their average (the trace is kept); the covariance is rebuilt
    with the sample variances.  Returns (Sigma, number of eigenvalues kept)."""
    R = np.asarray(R, float)
    T, N = R.shape
    S = sample_cov(R)
    sd = np.sqrt(np.diag(S))
    C = S / np.outer(sd, sd)
    lam, V = np.linalg.eigh(C)
    edge = mp_edges(N / T)[1]
    noise = lam < edge
    if noise.any():
        lam = lam.copy()
        lam[noise] = lam[noise].mean()
    Cc = V @ np.diag(lam) @ V.T
    d = np.sqrt(np.diag(Cc))
    Cc = Cc / np.outer(d, d)
    return Cc * np.outer(sd, sd), int((~noise).sum())


def lw_nonlinear(R):
    """Ledoit and Wolf (2020), `Analytical nonlinear shrinkage of large-dimensional covariance matrices', for N < T:
    keep the sample eigenvectors and replace each sample eigenvalue by a kernel estimate of the oracle, built from the
    eigenvalues' density and its Hilbert transform (Epanechnikov kernel, bandwidth T^(-1/3))."""
    X = np.asarray(R, float)
    X = X - X.mean(0)
    n, p = X.shape
    n = n - 1                                     # demeaned: one degree of freedom used
    S = X.T @ X / n
    lam, U = np.linalg.eigh(S)
    lam = np.maximum(lam, 1e-12)
    c = p / n
    h = n ** (-1 / 3)
    H = h * lam                                   # one bandwidth per eigenvalue
    x = (lam[:, None] - lam[None, :]) / H[None, :]
    s5 = math.sqrt(5)
    ft = (3 / (4 * s5)) * np.mean(np.maximum(1 - x ** 2 / 5, 0) / H[None, :], axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        hf = (-3 / (10 * math.pi)) * x + (3 / (4 * s5 * math.pi)) * (1 - x ** 2 / 5) * \
            np.log(np.abs((s5 - x) / (s5 + x)))
    hf = np.where(np.isclose(np.abs(x), s5), (-3 / (10 * math.pi)) * x, hf)
    Hft = np.mean(hf / H[None, :], axis=1)
    d = lam / ((math.pi * c * lam * ft) ** 2 + (1 - c - math.pi * c * lam * Hft) ** 2)
    return U @ np.diag(d) @ U.T


# ---------------------------------------------------------------------------
# Allocations
# ---------------------------------------------------------------------------


def _gmv_long_only(S, tol: float = 1e-12, max_iter: int = 1000) -> np.ndarray:
    """min w'Sw s.t. 1'w = 1, w >= 0 by a primal active-set method (exact, finite): on the free set the equality-
    constrained optimum is S_FF^-1 1 / 1'S_FF^-1 1; step toward it until a weight hits zero; when it is reached, release
    the zero weight whose Karush-Kuhn-Tucker multiplier is most negative."""
    N = S.shape[0]
    w = np.full(N, 1 / N)
    fixed = np.zeros(N, bool)
    for _ in range(max_iter):
        F = ~fixed
        x = np.linalg.solve(S[np.ix_(F, F)], np.ones(F.sum()))
        target = np.zeros(N)
        target[F] = x / x.sum()
        p = target - w
        if np.max(np.abs(p)) < 1e-14:
            g = S @ w
            lam = g - w @ g                          # multipliers (scaled) of the zero weights
            lam[F] = 0
            i = int(np.argmin(lam))
            if lam[i] >= -tol:
                break
            fixed[i] = False
            continue
        neg = F & (p < -1e-16)
        alpha, block = 1.0, -1
        if neg.any():
            r = -w[neg] / p[neg]
            k = int(np.argmin(r))
            if r[k] < 1.0:
                alpha, block = float(r[k]), int(np.flatnonzero(neg)[k])
        w = w + alpha * p
        if block >= 0:
            w[block] = 0.0
            fixed[block] = True
        w = np.maximum(w, 0)
        w = w / w.sum()
    return w


def gmv(S, long_only: bool = False) -> np.ndarray:
    """The global minimum-variance weights (summing to one); ``long_only`` adds w >= 0 (an exact active-set solver)."""
    S = np.asarray(S, float)
    N = S.shape[0]
    w = np.linalg.solve(S, np.ones(N))
    w = w / w.sum()
    if not long_only:
        return w
    if (w >= 0).all():
        return w
    return _gmv_long_only(S)


def tangency(mu, S) -> np.ndarray:
    """The maximum-Sharpe weights Sigma^-1 mu, scaled to sum to one (mu: excess returns)."""
    w = np.linalg.solve(np.asarray(S, float), np.asarray(mu, float))
    return w / w.sum()


def mean_variance(mu, S, risk_aversion: float) -> np.ndarray:
    """argmax w'mu - (a/2) w'Sigma w, unconstrained: Sigma^-1 mu / a."""
    return np.linalg.solve(np.asarray(S, float), np.asarray(mu, float)) / risk_aversion


def frontier(mu, S, targets):
    """The fully invested mean-variance frontier: the volatility of the minimum-variance portfolio for each target
    mean (Merton 1972's A, B, C)."""
    mu = np.asarray(mu, float)
    Si = np.linalg.inv(np.asarray(S, float))
    one = np.ones(len(mu))
    A, B, C = one @ Si @ one, one @ Si @ mu, mu @ Si @ mu
    D = A * C - B ** 2
    t = np.asarray(targets, float)
    return np.sqrt(np.maximum((A * t ** 2 - 2 * B * t + C) / D, 0))


def black_litterman(S, w_mkt, delta: float, tau: float, P=None, Q=None, Omega=None):
    """Black and Litterman (1992), as He and Litterman (1999) write it: the equilibrium excess returns
    Pi = delta Sigma w_mkt, and with views P mu = Q + e, e ~ N(0, Omega), the posterior mean
    [(tau Sigma)^-1 + P' Omega^-1 P]^-1 [(tau Sigma)^-1 Pi + P' Omega^-1 Q].  Returns (Pi, posterior mean)."""
    S = np.asarray(S, float)
    pi = delta * S @ np.asarray(w_mkt, float)
    if P is None:
        return pi, pi
    P = np.atleast_2d(np.asarray(P, float))
    Q = np.atleast_1d(np.asarray(Q, float))
    if Omega is None:                              # He and Litterman's default: the views' variance under tau Sigma
        Omega = np.diag(np.diag(P @ (tau * S) @ P.T))
    A = np.linalg.inv(tau * S)
    Oi = np.linalg.inv(np.atleast_2d(Omega))
    post = np.linalg.solve(A + P.T @ Oi @ P, A @ pi + P.T @ Oi @ Q)
    return pi, post


def risk_contributions(w, S) -> np.ndarray:
    """Each asset's share of the portfolio variance: w_i (Sigma w)_i / w'Sigma w (they sum to one)."""
    w = np.asarray(w, float)
    m = np.asarray(S, float) @ w
    return w * m / (w @ m)


def erc(S, budget=None, iters: int = 500) -> np.ndarray:
    """Equal (or budgeted) risk contributions, long only, by Spinu's (2013) convex problem
    min_y (1/2) y'Sigma y - sum b_i log y_i, solved by Newton's method, then w = y / sum y."""
    S = np.asarray(S, float)
    N = S.shape[0]
    b = np.full(N, 1 / N) if budget is None else np.asarray(budget, float) / np.sum(budget)
    y = 1 / np.sqrt(np.diag(S))
    y = y / np.sqrt(y @ S @ y)
    for _ in range(iters):
        g = S @ y - b / y
        Hm = S + np.diag(b / y ** 2)
        step = np.linalg.solve(Hm, g)
        t = 1.0
        while np.any(y - t * step <= 0):
            t /= 2
        y = y - t * step
        if np.max(np.abs(g)) < 1e-12:
            break
    return y / y.sum()


def hrp(S) -> tuple[np.ndarray, list]:
    """López de Prado's (2016) hierarchical risk parity: single-linkage clustering of the correlation distance
    sqrt((1 - rho)/2), quasi-diagonal ordering, then recursive bisection, each half weighted by the inverse of its
    inverse-variance portfolio's variance.  Returns (weights, the leaf order)."""
    from scipy.cluster.hierarchy import leaves_list, linkage
    from scipy.spatial.distance import squareform
    S = np.asarray(S, float)
    sd = np.sqrt(np.diag(S))
    C = np.clip(S / np.outer(sd, sd), -1, 1)
    D = np.sqrt(np.maximum((1 - C) / 2, 0))
    np.fill_diagonal(D, 0)
    order = list(leaves_list(linkage(squareform(D, checks=False), method="single")))
    w = np.ones(len(S))

    def cvar(idx):
        sub = S[np.ix_(idx, idx)]
        iv = 1 / np.diag(sub)
        iv = iv / iv.sum()
        return iv @ sub @ iv
    stack = [order]
    while stack:
        cl = stack.pop()
        if len(cl) < 2:
            continue
        a, b = cl[:len(cl) // 2], cl[len(cl) // 2:]
        va, vb = cvar(a), cvar(b)
        alpha = 1 - va / (va + vb)
        w[a] *= alpha
        w[b] *= 1 - alpha
        stack += [a, b]
    return w / w.sum(), order


def min_cvar(scen, beta: float = 0.95, target=None, long_only: bool = True):
    """Rockafellar and Uryasev (2000): minimise CVaR_beta of the loss -scen @ w over fully invested weights (and a
    target mean if given) as one linear program in (w, alpha, u): alpha + sum u_j / ((1 - beta) J), u_j >= 0,
    u_j >= -scen_j w - alpha.  Returns (weights, VaR alpha, CVaR)."""
    from scipy.optimize import linprog
    X = np.asarray(scen, float)
    J, N = X.shape
    c = np.r_[np.zeros(N), 1.0, np.full(J, 1 / ((1 - beta) * J))]
    A_ub = np.hstack([-X, -np.ones((J, 1)), -np.eye(J)])
    b_ub = np.zeros(J)
    A_eq = [np.r_[np.ones(N), 0.0, np.zeros(J)]]
    b_eq = [1.0]
    if target is not None:
        A_ub = np.vstack([A_ub, np.r_[-X.mean(0), 0.0, np.zeros(J)]])
        b_ub = np.r_[b_ub, -target]
    bounds = [(0, None) if long_only else (None, None)] * N + [(None, None)] + [(0, None)] * J
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq, bounds=bounds, method="highs")
    w = res.x[:N]
    return w, float(res.x[N]), float(res.fun)


def cvar_of(losses, beta: float = 0.95) -> float:
    """The empirical CVaR: the mean of the worst (1 - beta) share of losses (Rockafellar-Uryasev's formula)."""
    L = np.sort(np.asarray(losses, float))
    a = np.quantile(L, beta)
    return float(a + np.mean(np.maximum(L - a, 0)) / (1 - beta))


def kelly(mu, S) -> np.ndarray:
    """The growth-optimal weights in continuous time, Sigma^-1 (mu - r) with mu excess returns: they maximise
    w'mu - w'Sigma w / 2, the expected log growth, and may be levered."""
    return np.linalg.solve(np.asarray(S, float), np.asarray(mu, float))


def universal_2(gross, grid: int = 201):
    """Cover's (1991) universal portfolio for two assets: the wealth of every constant-rebalanced mix b in [0, 1],
    and the universal portfolio's wealth, their uniform average.  ``gross``: (T x 2) gross returns.  Returns
    (b grid, wealth of each mix, universal wealth path, best mix's wealth path)."""
    X = np.asarray(gross, float)
    b = np.linspace(0, 1, grid)
    period = np.outer(X[:, 0], b) + np.outer(X[:, 1], 1 - b)          # T x grid
    paths = np.cumprod(period, axis=0)
    uni = paths.mean(axis=1)
    best = paths[:, int(np.argmax(paths[-1]))]
    return b, paths[-1], uni, best


def entropy_pooling(scen, p, views_A, views_b):
    """Meucci (2008): the scenario probabilities q closest to the prior p in relative entropy subject to the linear
    views A q = b (each row of A a function of the scenarios, e.g. a return).  The solution is q ∝ p exp(A'lambda),
    lambda minimising the convex dual log sum p exp(A'lambda) - lambda'b."""
    from scipy.optimize import minimize
    A = np.atleast_2d(np.asarray(views_A, float))
    b = np.atleast_1d(np.asarray(views_b, float))
    p = np.asarray(p, float)
    lp = np.log(p)

    def dual(lam):
        z = lp + lam @ A
        m = z.max()
        lse = m + np.log(np.exp(z - m).sum())
        q = np.exp(z - lse)
        return lse - lam @ b, A @ q - b
    res = minimize(dual, np.zeros(len(b)), jac=True, method="BFGS", options={"gtol": 1e-12, "maxiter": 1000})
    z = lp + res.x @ A
    q = np.exp(z - z.max())
    return q / q.sum()


def diversity_weights(caps, p: float = 0.5) -> np.ndarray:
    """Fernholz's diversity-weighted portfolio: market weights raised to the power p in (0, 1), renormalised."""
    m = np.asarray(caps, float)
    m = m / m.sum()
    w = m ** p
    return w / w.sum()


def turnover(W) -> float:
    """Average one-way turnover of a sequence of weight vectors (rows): half the sum of absolute changes."""
    W = np.asarray(W, float)
    return float(np.mean(0.5 * np.abs(np.diff(W, axis=0)).sum(axis=1))) if len(W) > 1 else 0.0


# ---------------------------------------------------------------------------
# Theory: the sample minimum-variance portfolio under normal returns
# ---------------------------------------------------------------------------


def gmv_theory(K: int, T: int) -> dict:
    """For T i.i.d. N(mu, Sigma) returns of K assets and the sample covariance (n = T - 1 degrees of freedom), the
    sample GMV portfolio's variance relative to the true minimum sigma^2_min (exact):
    in sample, 1'S^-1 1 relates to a chi-square with n - K + 1 degrees of freedom, so E[in-sample / sigma^2_min] =
    (n - K + 1) / n; out of sample, E[w'Sigma w / sigma^2_min] = (n - 1) / (n - K) (Kempf and Memmel 2006).  As
    K/T -> gamma these tend to 1 - gamma and 1/(1 - gamma)."""
    n = T - 1
    return {"in": (n - K + 1) / n, "out": (n - 1) / (n - K), "in_lim": 1 - K / T, "out_lim": 1 / (1 - K / T)}


def gmv_sim(Sigma, T: int, reps: int, rng) -> dict:
    """Simulated in-sample and out-of-sample variance of the sample GMV portfolio, relative to the true minimum."""
    Sigma = np.asarray(Sigma, float)
    K = Sigma.shape[0]
    L = np.linalg.cholesky(Sigma)
    one = np.ones(K)
    vmin = 1 / (one @ np.linalg.solve(Sigma, one))
    ins, outs = np.empty(reps), np.empty(reps)
    for r in range(reps):
        X = rng.standard_normal((T, K)) @ L.T
        S = np.cov(X, rowvar=False)
        w = np.linalg.solve(S, one)
        w = w / w.sum()
        ins[r] = w @ S @ w / vmin
        outs[r] = w @ Sigma @ w / vmin
    return {"in": ins, "out": outs}


__all__ = ["sample_cov", "lw_identity", "lw_constcorr", "mp_edges", "rmt_clip", "lw_nonlinear", "gmv", "tangency",
           "mean_variance", "frontier", "black_litterman", "risk_contributions", "erc", "hrp", "min_cvar", "cvar_of",
           "kelly", "universal_2", "entropy_pooling", "diversity_weights", "turnover", "gmv_theory", "gmv_sim"]
