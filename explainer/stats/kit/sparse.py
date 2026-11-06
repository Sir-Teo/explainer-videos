"""statkit.sparse: sparsity, from ridge to compressed sensing (Part 32 of *Statistics, Built*).

Ridge through the SVD; the lasso and elastic net by coordinate descent along a warm-started path (glmnet's scaling,
(1/2n)||y - Xb||^2 + lam (alpha |b|_1 + (1 - alpha)/2 |b|_2^2)); the exact LARS and LARS-lasso paths (Efron, Hastie,
Johnstone & Tibshirani 2004); thresholding rules (soft, hard, SCAD, MCP) and coordinate descent for SCAD and MCP; the
group lasso; adaptive weights; K-fold CV with the one-SE rule and stability selection; Bayesian shrinkage profiles
(Laplace and horseshoe) and their Gibbs samplers for the normal-means problem; basis pursuit by linear programming,
the Donoho--Tanner phase transition and the modified Shepp--Logan phantom recovered from radial Fourier samples by
total-variation minimization (Chambolle--Pock); inference after selection (naive post-lasso, the debiased lasso,
double selection); and matrix completion by SoftImpute.  Checked in ``tests/test_stats_kit_sparse.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats

# --------------------------------------------------------------------------------------------------------- helpers


def standardize(X, y=None):
    """Centre the columns of X and scale them to unit variance (divisor n); centre y.  Returns (Xs, ys, mean, sd, ybar)."""
    X = np.asarray(X, float)
    mu, sd = X.mean(0), X.std(0)
    Xs = (X - mu) / sd
    if y is None:
        return Xs, None, mu, sd, 0.0
    y = np.asarray(y, float)
    return Xs, y - y.mean(), mu, sd, float(y.mean())


def soft(z, t):
    """Soft thresholding: sign(z)(|z| - t)_+, the lasso's rule for an orthonormal design."""
    return np.sign(z) * np.maximum(np.abs(z) - t, 0.0)


def hard(z, t):
    """Hard thresholding: z 1{|z| > t}, best subset's rule for an orthonormal design."""
    z = np.asarray(z, float)
    return z * (np.abs(z) > t)


def scad_threshold(z, lam, a: float = 3.7):
    """Fan & Li's (2001) SCAD rule for an orthonormal design: soft near 0, linear interpolation, identity beyond a lam."""
    z = np.asarray(z, float)
    az = np.abs(z)
    return np.where(az <= 2 * lam, soft(z, lam),
                    np.where(az <= a * lam, ((a - 1) * z - np.sign(z) * a * lam) / (a - 2), z))


def mcp_threshold(z, lam, gamma: float = 3.0):
    """Zhang's (2010) MCP ('firm') rule: soft(z, lam)/(1 - 1/gamma) for |z| <= gamma lam, identity beyond."""
    z = np.asarray(z, float)
    return np.where(np.abs(z) <= gamma * lam, soft(z, lam) / (1 - 1 / gamma), z)


def scad_penalty(b, lam, a: float = 3.7):
    b = np.abs(np.asarray(b, float))
    return np.where(b <= lam, lam * b, np.where(b <= a * lam, (2 * a * lam * b - b ** 2 - lam ** 2) / (2 * (a - 1)),
                                                 lam ** 2 * (a + 1) / 2))


def mcp_penalty(b, lam, gamma: float = 3.0):
    b = np.abs(np.asarray(b, float))
    return np.where(b <= gamma * lam, lam * b - b ** 2 / (2 * gamma), gamma * lam ** 2 / 2)


# --------------------------------------------------------------------------------------------------------- ridge


def ridge_svd(X, y, lams) -> dict:
    """Ridge through the SVD X = U D V': b(lam) = V diag(d/(d^2 + lam)) U'y.  Each principal direction is shrunk by
    d_j^2/(d_j^2 + lam); the effective degrees of freedom are their sum.  (Objective ||y - Xb||^2 + lam ||b||^2.)"""
    X, y = np.asarray(X, float), np.asarray(y, float)
    U, d, Vt = np.linalg.svd(X, full_matrices=False)
    uy = U.T @ y
    coefs, dfs, shrink = [], [], []
    for lam in np.atleast_1d(lams):
        f = d ** 2 / (d ** 2 + lam)
        coefs.append(Vt.T @ (f / d * uy))
        dfs.append(float(f.sum()))
        shrink.append(f)
    return {"coefs": np.array(coefs), "df": np.array(dfs), "shrink": np.array(shrink), "d": d, "lams": np.atleast_1d(lams)}


# --------------------------------------------------------------------------------------------- lasso and elastic net


def lasso_cd(X, y, lam: float, alpha: float = 1.0, weights=None, b0=None, max_sweeps: int = 5000,
             tol: float = 1e-10) -> np.ndarray:
    """Coordinate descent for (1/2n)||y - Xb||^2 + lam sum_j w_j (alpha |b_j| + (1 - alpha) b_j^2 / 2) (glmnet's
    scaling; centre y and X first).  ``weights`` gives the adaptive lasso (Zou 2006); alpha < 1 the elastic net (Zou &
    Hastie 2005).  Uses an active-set strategy: full sweeps until the support settles, then sweeps of the support."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    w = np.ones(p) if weights is None else np.asarray(weights, float)
    b = np.zeros(p) if b0 is None else np.asarray(b0, float).copy()
    r = y - X @ b
    col2 = (X ** 2).sum(0) / n
    l1, l2 = lam * alpha * w, lam * (1 - alpha) * w

    def sweep(idx):
        delta = 0.0
        for j in idx:
            if not np.isfinite(l1[j]):
                if b[j] != 0:
                    r[:] += X[:, j] * b[j]
                    b[j] = 0.0
                continue
            old = b[j]
            z = X[:, j] @ r / n + col2[j] * old
            new = soft(z, l1[j]) / (col2[j] + l2[j])
            if new != old:
                r[:] -= X[:, j] * (new - old)
                b[j] = new
                delta = max(delta, abs(new - old))
        return delta

    for _ in range(max_sweeps):
        d = sweep(range(p))
        if d < tol:
            break
        for _ in range(max_sweeps):
            act = np.flatnonzero(b)
            if sweep(act) < tol:
                break
    return b


def lam_max(X, y, alpha: float = 1.0) -> float:
    """The smallest lam at which every lasso coefficient is zero: max_j |x_j'y| / (n alpha)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    return float(np.max(np.abs(X.T @ y)) / (len(y) * alpha))


def lasso_path(X, y, lams=None, nlam: int = 100, eps: float = 1e-3, alpha: float = 1.0, weights=None) -> dict:
    """The warm-started path on a decreasing log grid from lam_max to eps lam_max (or ``lams``)."""
    if lams is None:
        lm = lam_max(X, y, alpha)
        lams = lm * np.logspace(0, np.log10(eps), nlam)
    lams = np.asarray(lams, float)
    out, b = [], None
    for lam in lams:
        b = lasso_cd(X, y, lam, alpha=alpha, weights=weights, b0=b)
        out.append(b.copy())
    B = np.array(out)
    return {"lams": lams, "coefs": B, "df": (np.abs(B) > 0).sum(1)}


def kkt(X, y, b, lam) -> dict:
    """Lasso optimality: x_j'(y - Xb)/n = lam sign(b_j) on the support and |x_j'(y - Xb)/n| <= lam off it."""
    X, y, b = np.asarray(X, float), np.asarray(y, float), np.asarray(b, float)
    g = X.T @ (y - X @ b) / len(y)
    on = b != 0
    return {"grad": g, "on_err": float(np.max(np.abs(g[on] - lam * np.sign(b[on])), initial=0.0)),
            "off_max": float(np.max(np.abs(g[~on]), initial=0.0))}


def lars(X, y, lasso: bool = True, max_steps: int | None = None) -> dict:
    """Least angle regression (Efron, Hastie, Johnstone & Tibshirani 2004), exactly, on centred y and centred,
    standardized X.  With ``lasso=True`` a coefficient that crosses zero is dropped (the LARS-lasso modification), and
    the path is the lasso's for the objective (1/2)||y - Xb||^2 + lam ||b||_1, lam = the current maximal |correlation|.
    Returns the knots: lam, coefficients, the action ('+j' / '-j') and the active set."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    beta = np.zeros(p)
    mu = np.zeros(n)
    c = X.T @ y
    C = float(np.max(np.abs(c)))
    active = [int(np.argmax(np.abs(c)))]
    lams, coefs, actions, sets = [C], [beta.copy()], [f"+{active[0]}"], [list(active)]
    steps = 0
    max_steps = max_steps or 8 * p
    while steps < max_steps:
        steps += 1
        A = np.array(active)
        s = np.sign(c[A])
        XA = X[:, A] * s
        G = XA.T @ XA
        Gi1 = np.linalg.solve(G, np.ones(len(A)))
        AA = 1.0 / math.sqrt(float(Gi1.sum()))
        w = AA * Gi1
        u = XA @ w
        a = X.T @ u
        inactive = [j for j in range(p) if j not in active]
        gam, nxt = C / AA, None
        if len(A) >= min(n - 1, p):
            inactive = []
        for j in inactive:
            for g_ in ((C - c[j]) / (AA - a[j]), (C + c[j]) / (AA + a[j])):
                if 1e-12 < g_ < gam:
                    gam, nxt = g_, j
        drop = None
        if lasso:
            d = s * w
            with np.errstate(divide="ignore", invalid="ignore"):
                gt = -beta[A] / d
            for k, g_ in enumerate(gt):
                if 1e-12 < g_ < gam:
                    gam, drop, nxt = g_, int(A[k]), None
        mu = mu + gam * u
        beta[A] = beta[A] + gam * s * w
        C = C - gam * AA
        c = X.T @ (y - mu)
        if drop is not None:
            beta[drop] = 0.0
            active.remove(drop)
            actions.append(f"-{drop}")
        elif nxt is not None:
            active.append(nxt)
            actions.append(f"+{nxt}")
        else:
            actions.append("end")
        lams.append(max(C, 0.0))
        coefs.append(beta.copy())
        sets.append(list(active))
        if nxt is None and drop is None:
            break
    return {"lams": np.array(lams), "coefs": np.array(coefs), "actions": actions, "active": sets}


def group_lasso(X, y, groups, lam: float, max_sweeps: int = 2000, tol: float = 1e-10) -> np.ndarray:
    """Yuan & Lin's (2006) group lasso, (1/2n)||y - Xb||^2 + lam sum_g sqrt(p_g) ||b_g||_2, by block coordinate descent
    with each group orthonormalized (X_g'X_g/n = I); coefficients returned on the original scale."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    groups = np.asarray(groups)
    labs = list(dict.fromkeys(groups.tolist()))
    Q, R = {}, {}
    for g in labs:
        idx = np.flatnonzero(groups == g)
        q, r = np.linalg.qr(X[:, idx])
        Q[g], R[g] = q * math.sqrt(n), r / math.sqrt(n)
    th = {g: np.zeros(len(np.flatnonzero(groups == g))) for g in labs}
    res = y.copy()
    for _ in range(max_sweeps):
        delta = 0.0
        for g in labs:
            z = Q[g].T @ res / n + th[g]
            nz = np.linalg.norm(z)
            t = lam * math.sqrt(len(z))
            new = (1 - t / nz) * z if nz > t else np.zeros_like(z)
            diff = new - th[g]
            if np.any(diff):
                res -= Q[g] @ diff
                th[g] = new
                delta = max(delta, float(np.max(np.abs(diff))))
        if delta < tol:
            break
    b = np.zeros(p)
    for g in labs:
        idx = np.flatnonzero(groups == g)
        b[idx] = np.linalg.solve(R[g], th[g])
    return b


def ncv_cd(X, y, lam: float, penalty: str = "mcp", gamma: float | None = None, b0=None, max_sweeps: int = 5000,
           tol: float = 1e-10) -> np.ndarray:
    """Coordinate descent for SCAD or MCP (Breheny & Huang 2011) on standardized columns (x_j'x_j/n = 1): each update
    applies the univariate thresholding rule to the partial-residual correlation."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    g = gamma if gamma is not None else (3.7 if penalty == "scad" else 3.0)
    rule = (lambda z: scad_threshold(z, lam, g)) if penalty == "scad" else (lambda z: mcp_threshold(z, lam, g))
    b = np.zeros(p) if b0 is None else np.asarray(b0, float).copy()
    r = y - X @ b
    for _ in range(max_sweeps):
        delta = 0.0
        for j in range(p):
            z = X[:, j] @ r / n + b[j]
            new = float(rule(z))
            if new != b[j]:
                r -= X[:, j] * (new - b[j])
                delta = max(delta, abs(new - b[j]))
                b[j] = new
        if delta < tol:
            break
    return b


# --------------------------------------------------------------------------------------------- choosing lambda


def cv_lasso(X, y, lams, K: int = 10, rng=None, alpha: float = 1.0) -> dict:
    """K-fold CV along a common lam grid (centring within folds); the minimizer and the one-SE rule's lam."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n = len(y)
    rng = rng or np.random.default_rng(0)
    folds = rng.permutation(np.arange(n) % K)
    err = np.zeros((K, len(lams)))
    for k in range(K):
        tr, te = folds != k, folds == k
        mx, my = X[tr].mean(0), y[tr].mean()
        path = lasso_path(X[tr] - mx, y[tr] - my, lams=lams, alpha=alpha)["coefs"]
        pred = (X[te] - mx) @ path.T + my
        err[k] = ((y[te][:, None] - pred) ** 2).mean(0)
    m, se = err.mean(0), err.std(0, ddof=1) / math.sqrt(K)
    i = int(np.argmin(m))
    j = int(np.min(np.flatnonzero(m <= m[i] + se[i])))
    return {"lams": np.asarray(lams), "cv": m, "se": se, "i_min": i, "i_1se": j, "lam_min": float(lams[i]),
            "lam_1se": float(lams[j])}


def stability_selection(X, y, lams, B: int = 100, rng=None) -> np.ndarray:
    """Meinshausen & Bühlmann (2010): the share of half-subsamples in which each variable is selected, for each lam
    (rows lam, columns variables)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n = len(y)
    rng = rng or np.random.default_rng(0)
    freq = np.zeros((len(lams), X.shape[1]))
    for _ in range(B):
        idx = rng.choice(n, n // 2, replace=False)
        Xs, ys = X[idx] - X[idx].mean(0), y[idx] - y[idx].mean()
        Xs = Xs / Xs.std(0)
        path = lasso_path(Xs, ys, lams=lams)["coefs"]
        freq += path != 0
    return freq / B


# ------------------------------------------------------------------------------------------------ Bayesian sparsity


def laplace_posterior_mean(y, lam: float, sigma: float = 1.0):
    """E(theta | y) for y ~ N(theta, sigma^2), theta ~ Laplace(rate lam): never exactly zero, unlike its mode (the soft
    threshold).  In closed form through normal tail probabilities."""
    y = np.asarray(y, float)
    s = sigma
    a, b = y - lam * s * s, y + lam * s * s
    # posterior is a two-piece mixture of truncated normals N(a, s^2) on (0, inf) and N(b, s^2) on (-inf, 0)
    la = stats.norm.logcdf(a / s) + lam * lam * s * s / 2 - lam * y
    lb = stats.norm.logcdf(-b / s) + lam * lam * s * s / 2 + lam * y
    m = np.maximum(la, lb)
    wa, wb = np.exp(la - m), np.exp(lb - m)
    ma = a + s * np.exp(stats.norm.logpdf(a / s) - stats.norm.logcdf(a / s))
    mb = b - s * np.exp(stats.norm.logpdf(b / s) - stats.norm.logcdf(-b / s))
    return (wa * ma + wb * mb) / (wa + wb)


def horseshoe_posterior_mean(y, tau: float, sigma: float = 1.0, ngrid: int = 4000):
    """E(theta | y) under Carvalho, Polson & Scott's (2010) horseshoe, theta | lam ~ N(0, lam^2 tau^2), lam ~ C+(0, 1),
    with tau fixed: y (1 - E(kappa | y)), kappa = 1/(1 + lam^2 tau^2), by quadrature over kappa."""
    y = np.atleast_1d(np.asarray(y, float))
    k = (np.arange(ngrid) + 0.5) / ngrid
    # prior density of kappa for lam ~ C+ and given tau (Carvalho et al. 2010, eq. 4)
    t2 = tau * tau
    prior = 1.0 / (math.pi * tau) * k ** -0.5 * (1 - k) ** -0.5 / (1 + (t2 - 1) * k)
    out = []
    for yi in y:
        like = np.sqrt(k) * np.exp(-k * yi * yi / (2 * sigma * sigma))
        w = prior * like
        out.append(yi * (1 - np.sum(k * w) / np.sum(w)))
    return np.array(out)


def horseshoe_gibbs(y, sigma: float = 1.0, iters: int = 4000, burn: int = 1000, rng=None) -> dict:
    """The horseshoe for the normal-means problem y_i ~ N(theta_i, sigma^2), with half-Cauchy local and global scales,
    by Makalic & Schmidt's (2016) inverse-gamma auxiliaries.  Returns posterior means and the draws of tau."""
    y = np.asarray(y, float)
    p = len(y)
    rng = rng or np.random.default_rng(0)
    lam2, nu, tau2, xi = np.ones(p), np.ones(p), 1.0, 1.0
    s2 = sigma * sigma
    keep, taus = np.zeros(p), []

    def invgamma(shape, scale):
        return scale / rng.gamma(shape, 1.0, size=np.shape(scale))

    for t in range(iters):
        v = 1.0 / (1.0 / s2 + 1.0 / (lam2 * tau2))
        theta = rng.normal(v * y / s2, np.sqrt(v))
        lam2 = invgamma(1.0, 1.0 / nu + theta ** 2 / (2 * tau2))
        nu = invgamma(1.0, 1.0 + 1.0 / lam2)
        tau2 = float(invgamma((p + 1) / 2, 1.0 / xi + np.sum(theta ** 2 / lam2) / 2))
        xi = float(invgamma(1.0, 1.0 + 1.0 / tau2))
        if t >= burn:
            keep += theta
            taus.append(math.sqrt(tau2))
    return {"mean": keep / (iters - burn), "tau": np.array(taus)}


def bayes_lasso_gibbs(y, lam: float, sigma: float = 1.0, iters: int = 4000, burn: int = 1000, rng=None) -> dict:
    """Park & Casella's (2008) Bayesian lasso for the normal-means problem (Laplace prior with rate lam / sigma
    written as a scale mixture of normals): posterior means, never exactly zero."""
    y = np.asarray(y, float)
    p = len(y)
    rng = rng or np.random.default_rng(0)
    s2 = sigma * sigma
    inv_t2 = np.ones(p)
    keep = np.zeros(p)
    for t in range(iters):
        v = 1.0 / (1.0 / s2 + inv_t2 / s2)
        theta = rng.normal(v * y / s2, np.sqrt(v))
        mu = np.sqrt(lam * lam * s2 / np.maximum(theta ** 2, 1e-300))
        inv_t2 = rng.wald(mu, lam * lam)
        if t >= burn:
            keep += theta
    return {"mean": keep / (iters - burn)}


# --------------------------------------------------------------------------------------------- compressed sensing


def basis_pursuit(A, y) -> np.ndarray:
    """min ||x||_1 subject to A x = y, as the linear program min 1'(u + v), A(u - v) = y, u, v >= 0 (HiGHS)."""
    A, y = np.asarray(A, float), np.asarray(y, float)
    n, p = A.shape
    res = optimize.linprog(np.ones(2 * p), A_eq=np.hstack([A, -A]), b_eq=y, bounds=(0, None), method="highs")
    return res.x[:p] - res.x[p:]


def phase_curve(deltas) -> np.ndarray:
    """The asymptotic ell-1 phase transition rho(delta) for sign-symmetric signals (Donoho & Tanner 2009; in the form
    of Donoho, Maleki & Montanari 2009): recovery succeeds w.h.p. when s/n < rho(n/p)."""
    z = np.linspace(1e-4, 8, 8000)
    phi, Phi = stats.norm.pdf(z), stats.norm.cdf(-z)
    psi = (1 + z * z) * Phi - z * phi
    out = []
    for d in np.atleast_1d(deltas):
        r = (1 - 2 / d * psi) / (1 + z * z - 2 * psi)
        out.append(float(np.max(r)))
    return np.array(out)


def phase_grid(p: int, deltas, rhos, reps: int, rng) -> np.ndarray:
    """Empirical success rates of basis pursuit with Gaussian A (n x p), n = delta p, s = rho n, random-sign spikes;
    success means ||x_hat - x||_inf < 1e-4."""
    out = np.zeros((len(rhos), len(deltas)))
    for j, d in enumerate(deltas):
        n = max(2, int(round(d * p)))
        for i, r in enumerate(rhos):
            s = max(1, int(round(r * n)))
            ok = 0
            for _ in range(reps):
                A = rng.standard_normal((n, p)) / math.sqrt(n)
                x = np.zeros(p)
                x[rng.choice(p, s, replace=False)] = rng.choice([-1.0, 1.0], s)
                xh = basis_pursuit(A, A @ x)
                ok += np.max(np.abs(xh - x)) < 1e-4
            out[i, j] = ok / reps
    return out


SHEPP_LOGAN = [  # modified Shepp-Logan (Toft 1996): intensity, semi-axes a, b, centre x0, y0, angle (degrees)
    (1.0, .69, .92, 0, 0, 0), (-.8, .6624, .8740, 0, -.0184, 0), (-.2, .1100, .3100, .22, 0, -18),
    (-.2, .1600, .4100, -.22, 0, 18), (.1, .2100, .2500, 0, .35, 0), (.1, .0460, .0460, 0, .1, 0),
    (.1, .0460, .0460, 0, -.1, 0), (.1, .0460, .0230, -.08, -.605, 0), (.1, .0230, .0230, 0, -.606, 0),
    (.1, .0230, .0460, .06, -.605, 0)]


def shepp_logan(N: int = 128) -> np.ndarray:
    """Shepp & Logan's (1974) head phantom, in Toft's higher-contrast form, on an N x N grid of [-1, 1]^2 (row 0 at
    the top)."""
    t = (np.arange(N) + 0.5) / N * 2 - 1
    xx, yy = np.meshgrid(t, -t)
    img = np.zeros((N, N))
    for A, a, b, x0, y0, ang in SHEPP_LOGAN:
        th = math.radians(ang)
        xr = (xx - x0) * math.cos(th) + (yy - y0) * math.sin(th)
        yr = -(xx - x0) * math.sin(th) + (yy - y0) * math.cos(th)
        img[(xr / a) ** 2 + (yr / b) ** 2 <= 1] += A
    return img


def radial_mask(N: int, lines: int) -> np.ndarray:
    """A boolean k-space mask (unshifted FFT layout) of ``lines`` lines through the origin at equally spaced angles,
    made conjugate-symmetric so that real images stay real."""
    M = np.zeros((N, N), bool)
    c = N // 2
    for k in range(lines):
        th = math.pi * k / lines
        for r in np.linspace(-N, N, 4 * N):
            i, j = int(round(c + r * math.sin(th))), int(round(c + r * math.cos(th)))
            if 0 <= i < N and 0 <= j < N:
                M[i, j] = True
    M = np.fft.ifftshift(M)
    Ms = M | np.roll(np.flip(M), 1, axis=(0, 1))
    return Ms


def _grad(x):
    gx = np.zeros_like(x)
    gy = np.zeros_like(x)
    gx[:, :-1] = x[:, 1:] - x[:, :-1]
    gy[:-1, :] = x[1:, :] - x[:-1, :]
    return gx, gy


def _div(px, py):
    d = np.zeros_like(px)
    d[:, 0] = px[:, 0]
    d[:, 1:-1] = px[:, 1:-1] - px[:, :-2]
    d[:, -1] = -px[:, -2]
    e = np.zeros_like(py)
    e[0, :] = py[0, :]
    e[1:-1, :] = py[1:-1, :] - py[:-2, :]
    e[-1, :] = -py[-2, :]
    return d + e


def tv(x) -> float:
    gx, gy = _grad(x)
    return float(np.sum(np.sqrt(gx ** 2 + gy ** 2)))


def min_energy(y, mask) -> np.ndarray:
    """The minimum-energy (zero-filled) reconstruction: the inverse FFT with the unmeasured frequencies set to 0."""
    return np.real(np.fft.ifft2(np.where(mask, y, 0), norm="ortho"))


def tv_recover(y, mask, iters: int = 3000, record=()) -> dict:
    """min TV(x) subject to the measured Fourier coefficients F x = y on ``mask`` (Candès, Romberg & Tao 2006), by
    Chambolle & Pock's (2011) primal-dual algorithm; the constraint enters through exact projection (F is unitary).
    ``record`` lists iterations whose iterates are returned."""
    x = min_energy(y, mask)
    xb = x.copy()
    px, py = np.zeros_like(x), np.zeros_like(x)
    tau = sigma = 0.99 / math.sqrt(8)
    snaps = {}
    for k in range(1, iters + 1):
        gx, gy = _grad(xb)
        px, py = px + sigma * gx, py + sigma * gy
        nrm = np.maximum(1.0, np.sqrt(px ** 2 + py ** 2))
        px, py = px / nrm, py / nrm
        xn = x + tau * _div(px, py)
        F = np.fft.fft2(xn, norm="ortho")
        F[mask] = y[mask]
        xn = np.real(np.fft.ifft2(F, norm="ortho"))
        xb = 2 * xn - x
        x = xn
        if k in record:
            snaps[k] = x.copy()
    return {"x": x, "snaps": snaps}


# ---------------------------------------------------------------------------------------- inference after selection


def ols_ci(X, y, cols, level: float = 0.95) -> dict:
    """OLS on the chosen columns (with an intercept), with t-intervals: what naive post-selection inference reports."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n = len(y)
    Z = np.column_stack([np.ones(n), X[:, cols]])
    b, *_ = np.linalg.lstsq(Z, y, rcond=None)
    r = y - Z @ b
    df = n - Z.shape[1]
    s2 = float(r @ r / df)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(Z.T @ Z)))
    q = stats.t.ppf(0.5 + level / 2, df)
    return {"b": b[1:], "se": se[1:], "lo": b[1:] - q * se[1:], "hi": b[1:] + q * se[1:]}


def debiased_lasso(X, y, j: int, lam: float, lam_node: float | None = None, level: float = 0.95) -> dict:
    """Zhang & Zhang (2014) and van de Geer, Bühlmann, Ritov & Dezeure (2014): one-step correction of the lasso for
    coordinate j, b_j + theta_j' X'(y - X b)/n, with theta_j from a nodewise lasso of x_j on the other columns.  Its
    standard error is sigma_hat sqrt(theta_j' Sigma_hat theta_j / n), sigma_hat from the lasso residuals.  X centred,
    y centred."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    b = lasso_cd(X, y, lam)
    others = np.r_[0:j, j + 1:p]
    ln = lam_node if lam_node is not None else lam
    g = lasso_cd(X[:, others], X[:, j], ln)
    resid_j = X[:, j] - X[:, others] @ g
    tau2 = float(resid_j @ resid_j / n + ln * np.sum(np.abs(g)))
    theta = np.zeros(p)
    theta[j] = 1.0
    theta[others] = -g
    theta /= tau2
    r = y - X @ b
    bd = float(b[j] + theta @ X.T @ r / n)
    s = int(np.sum(b != 0))
    sigma = math.sqrt(float(r @ r) / max(n - s, 1))
    Sig = X.T @ X / n
    se = sigma * math.sqrt(float(theta @ Sig @ theta) / n)
    q = stats.norm.ppf(0.5 + level / 2)
    return {"b": bd, "se": se, "lo": bd - q * se, "hi": bd + q * se, "lasso": b, "sigma": sigma}


def double_selection(y, d, X, lam_y: float, lam_d: float, level: float = 0.95) -> dict:
    """Belloni, Chernozhukov & Hansen (2014): select controls by a lasso of y on X and a lasso of d on X; regress y on
    d and the union by OLS; report the t-interval for d's coefficient."""
    y, d, X = np.asarray(y, float), np.asarray(d, float), np.asarray(X, float)
    Xc = X - X.mean(0)
    sy = np.flatnonzero(lasso_cd(Xc, y - y.mean(), lam_y))
    sd = np.flatnonzero(lasso_cd(Xc, d - d.mean(), lam_d))
    U = np.union1d(sy, sd)
    r = ols_ci(np.column_stack([d, X]), y, np.r_[0, U + 1].astype(int), level)
    return {"b": float(r["b"][0]), "lo": float(r["lo"][0]), "hi": float(r["hi"][0]), "n_selected": len(U)}


def single_selection(y, d, X, lam: float, level: float = 0.95) -> dict:
    """The naive alternative: a lasso of y on (d, X) with d unpenalized, then OLS of y on d and the selected controls."""
    y, d, X = np.asarray(y, float), np.asarray(d, float), np.asarray(X, float)
    Z = np.column_stack([d, X])
    Zc = Z - Z.mean(0)
    w = np.ones(Z.shape[1])
    w[0] = 0.0
    b = lasso_cd(Zc, y - y.mean(), lam, weights=w)
    S = np.flatnonzero(b[1:])
    r = ols_ci(Z, y, np.r_[0, S + 1].astype(int), level)
    return {"b": float(r["b"][0]), "lo": float(r["lo"][0]), "hi": float(r["hi"][0]), "n_selected": len(S)}


# --------------------------------------------------------------------------------------------- matrix completion


def soft_impute(M, observed, lam: float, iters: int = 300, Z0=None) -> dict:
    """Mazumder, Hastie & Tibshirani's (2010) SoftImpute: repeat Z <- S_lam(P_obs(M) + P_obs^perp(Z)), where S_lam
    soft-thresholds the singular values; the fixed point minimizes (1/2)||P_obs(M - Z)||_F^2 + lam ||Z||_*."""
    M = np.asarray(M, float)
    obs = np.asarray(observed, bool)
    Z = np.zeros_like(M) if Z0 is None else np.asarray(Z0, float).copy()
    for _ in range(iters):
        W = np.where(obs, M, Z)
        U, d, Vt = np.linalg.svd(W, full_matrices=False)
        d = np.maximum(d - lam, 0.0)
        Zn = (U * d) @ Vt
        if np.linalg.norm(Zn - Z) <= 1e-7 * max(1.0, np.linalg.norm(Z)):
            Z = Zn
            break
        Z = Zn
    return {"Z": Z, "rank": int(np.sum(d > 0)), "d": d}
