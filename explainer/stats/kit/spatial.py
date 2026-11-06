"""statkit.spatial: geostatistics, areal data and point patterns (Part 39 of *Statistics, Built*).

Covariances and variograms:
    matern(d, sigma2, rho, nu)              the Matern covariance (closed forms for nu = 1/2, 3/2, 5/2)
    variogram(xy, z, edges, robust)         Matheron's (or Cressie-Hawkins') empirical semivariogram
    fit_variogram(lags, gamma, n, model)    weighted least squares (Cressie 1985) for nugget + sill * model
Prediction:
    krige(xy, z, xy0, cov, X, X0, nugget)   simple / ordinary / universal kriging (= the GP posterior), with variances
    gp_fit(xy, z, X, nu, reml)              Matern parameters by ML or REML (profiled over the mean and scale)
    vecchia_loglik(xy, z, params, m)        Vecchia's (1988) nearest-neighbour approximation to the Gaussian likelihood
    vecchia_loglik_fast(...)                the same with k-d-tree neighbours, for 10^5 points
Lattices and areas:
    gmrf_precision(nx, ny, kappa, tau)      the SPDE-style precision (kappa^2 - Laplacian)^2 on a grid, sparse
    morans_i(z, W)                          Moran's I with its permutation p-value
    icar_smooth(y, E, W, tau_u, tau_v)      Poisson disease mapping with BYM-type random effects, posterior mode
Points:
    ripley_k(xy, r, window)                 Ripley's K with border correction; L(r) = sqrt(K/pi)
    csr_envelope(n, r, window, sims)        pointwise envelopes of L under complete spatial randomness
Other:
    gneiting(h, u, ...)                     Gneiting's (2002) nonseparable space-time covariance
    expected_improvement(mu, sd, best)      the Bayesian-optimization acquisition function
"""

from __future__ import annotations

import math

import numpy as np
from scipy import linalg, optimize, sparse, special, stats
from scipy.sparse import linalg as splinalg


def dists(a, b=None):
    a = np.asarray(a, float)
    b = a if b is None else np.asarray(b, float)
    return np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1))


def matern(d, sigma2: float = 1.0, rho: float = 1.0, nu: float = 1.5) -> np.ndarray:
    """C(d) = sigma^2 2^{1-nu}/Gamma(nu) (sqrt(2 nu) d/rho)^nu K_nu(sqrt(2 nu) d/rho); nu = 1/2 is exponential, nu -> inf
    Gaussian.  Closed forms for nu = 0.5, 1.5, 2.5."""
    d = np.asarray(d, float)
    s = math.sqrt(2 * nu) * d / rho
    if nu == 0.5:
        return sigma2 * np.exp(-s)
    if nu == 1.5:
        return sigma2 * (1 + s) * np.exp(-s)
    if nu == 2.5:
        return sigma2 * (1 + s + s * s / 3) * np.exp(-s)
    with np.errstate(invalid="ignore"):
        c = sigma2 * 2 ** (1 - nu) / special.gamma(nu) * s ** nu * special.kv(nu, s)
    return np.where(d == 0, sigma2, c)


def variogram(xy, z, edges, robust: bool = False) -> dict:
    """The empirical semivariogram: half the mean squared difference of pairs in each distance bin (Matheron 1962), or
    Cressie & Hawkins' (1980) robust version (mean |dz|^{1/2})^4 / (0.457 + 0.494/N)."""
    xy, z = np.asarray(xy, float), np.asarray(z, float)
    i, j = np.triu_indices(len(z), 1)
    d = np.sqrt(((xy[i] - xy[j]) ** 2).sum(1))
    dz = z[i] - z[j]
    lags, gam, cnt = [], [], []
    for a, b in zip(edges[:-1], edges[1:]):
        k = (d >= a) & (d < b)
        n = int(k.sum())
        if n == 0:
            continue
        lags.append(float(d[k].mean()))
        if robust:
            gam.append(float(np.mean(np.sqrt(np.abs(dz[k]))) ** 4 / (0.457 + 0.494 / n) / 2))
        else:
            gam.append(float(0.5 * np.mean(dz[k] ** 2)))
        cnt.append(n)
    return {"lag": np.array(lags), "gamma": np.array(gam), "n": np.array(cnt)}


def model_variogram(h, nugget, sill, rng_, model="exp", nu=1.5):
    h = np.asarray(h, float)
    if model == "sph":
        r = np.clip(h / rng_, 0, 1)
        g = sill * (1.5 * r - 0.5 * r ** 3)
    else:
        nu_ = {"exp": 0.5, "matern": nu}[model]
        g = sill - matern(h, sill, rng_, nu_)
    return np.where(h > 0, nugget + g, 0.0)


def fit_variogram(lags, gamma, n, model: str = "exp", nu: float = 1.5) -> dict:
    """Cressie's (1985) weighted least squares: weights N_k / gamma_model(h_k)^2."""
    lags, gamma, n = (np.asarray(a, float) for a in (lags, gamma, n))

    def loss(th):
        nug, sill, r = np.exp(th)
        g = model_variogram(lags, nug, sill, r, model, nu)
        return np.sum(n * (gamma / g - 1) ** 2)

    th0 = np.log([max(gamma[0] * 0.5, 1e-6), max(gamma.max(), 1e-6), max(lags.max() / 3, 1e-6)])
    o = optimize.minimize(loss, th0, method="Nelder-Mead", options={"maxiter": 5000, "xatol": 1e-8, "fatol": 1e-10})
    nug, sill, r = np.exp(o.x)
    return {"nugget": float(nug), "sill": float(sill), "range": float(r), "model": model}


def krige(xy, z, xy0, cov, X=None, X0=None, nugget: float = 0.0, mean: float | None = None) -> dict:
    """Kriging with covariance function ``cov(d)`` (no nugget) and measurement-error variance ``nugget``:
    simple kriging if ``mean`` is given; otherwise universal kriging on the columns of X (ordinary kriging when X is
    None: a constant).  Returns the predictions of the noise-free field at xy0, their variances, and the GLS
    coefficients.  This is the posterior mean and variance of a Gaussian process."""
    xy, xy0, z = np.asarray(xy, float), np.asarray(xy0, float), np.asarray(z, float)
    n, m = len(z), len(xy0)
    K = cov(dists(xy)) + nugget * np.eye(n)
    k0 = cov(dists(xy, xy0))  # n x m
    c00 = cov(np.zeros(1))[0]
    L = linalg.cho_factor(K, lower=True)
    if mean is not None:
        r = z - mean
        w = linalg.cho_solve(L, r)
        pred = mean + k0.T @ w
        v = c00 - np.sum(k0 * linalg.cho_solve(L, k0), 0)
        return {"pred": pred, "var": np.maximum(v, 0), "beta": np.array([mean])}
    F = np.ones((n, 1)) if X is None else np.column_stack([np.ones(n), np.asarray(X, float).reshape(n, -1)])
    F0 = np.ones((m, 1)) if X0 is None else np.column_stack([np.ones(m), np.asarray(X0, float).reshape(m, -1)])
    KiF = linalg.cho_solve(L, F)
    A = F.T @ KiF
    beta = np.linalg.solve(A, KiF.T @ z)
    r = z - F @ beta
    pred = F0 @ beta + k0.T @ linalg.cho_solve(L, r)
    Kik0 = linalg.cho_solve(L, k0)
    R = F0.T - F.T @ Kik0  # p x m
    v = c00 - np.sum(k0 * Kik0, 0) + np.sum(R * np.linalg.solve(A, R), 0)
    return {"pred": pred, "var": np.maximum(v, 0), "beta": beta, "cov_beta": np.linalg.inv(A)}


def gp_loglik(xy, z, X, rho: float, nu: float, frac: float, reml: bool = False) -> dict:
    """The Matern log-likelihood with the mean (GLS) and the overall variance profiled out; frac = sill/(sill+nugget)."""
    z = np.asarray(z, float)
    n = len(z)
    F = np.ones((n, 1)) if X is None else np.column_stack([np.ones(n), np.asarray(X, float).reshape(n, -1)])
    p = F.shape[1]
    R = frac * matern(dists(xy), 1.0, rho, nu) + (1 - frac) * np.eye(n)
    L = linalg.cho_factor(R + 1e-10 * np.eye(n), lower=True)
    logdet = 2 * np.sum(np.log(np.diag(L[0])))
    RiF = linalg.cho_solve(L, F)
    A = F.T @ RiF
    beta = np.linalg.solve(A, RiF.T @ z)
    r = z - F @ beta
    q = r @ linalg.cho_solve(L, r)
    if reml:
        s2 = q / (n - p)
        ll = -0.5 * ((n - p) * np.log(2 * np.pi * s2) + logdet + np.linalg.slogdet(A)[1] + (n - p))
    else:
        s2 = q / n
        ll = -0.5 * (n * np.log(2 * np.pi * s2) + logdet + n)
    return {"ll": float(ll), "sigma2": float(s2 * frac), "tau2": float(s2 * (1 - frac)), "beta": beta,
            "cov_beta": s2 * np.linalg.inv(A)}


def gp_fit(xy, z, X=None, nu: float = 1.5, reml: bool = True) -> dict:
    """Matern range and nugget fraction by maximizing the profiled (RE)ML; sigma^2, tau^2 and beta in closed form."""
    D = dists(xy)
    scale = float(np.median(D[D > 0]))

    def nll(th):
        rho, frac = np.exp(th[0]) * scale, 1 / (1 + np.exp(-th[1]))
        return -gp_loglik(xy, z, X, rho, nu, frac, reml)["ll"]

    best = None
    for r0 in (-2.0, -1.0, 0.0):
        for f0 in (0.0, 2.0):
            o = optimize.minimize(nll, [r0, f0], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-8})
            if best is None or o.fun < best.fun:
                best = o
    rho, frac = float(np.exp(best.x[0]) * scale), float(1 / (1 + np.exp(-best.x[1])))
    out = gp_loglik(xy, z, X, rho, nu, frac, reml)
    out.update(rho=rho, frac=frac, nu=nu)
    return out


def vecchia_loglik(xy, z, sigma2: float, rho: float, nu: float, tau2: float, m: int = 10, mean: float = 0.0) -> float:
    """Vecchia's (1988) approximation: order the points (here by the sum of coordinates), and replace each conditional
    density p(z_i | z_1..z_{i-1}) by p(z_i | its m nearest previous neighbours).  O(n m^3) instead of O(n^3)."""
    xy, z = np.asarray(xy, float), np.asarray(z, float) - mean
    o = np.argsort(xy[:, 0] + xy[:, 1])
    xy, z = xy[o], z[o]
    ll = 0.0
    for i in range(len(z)):
        if i == 0:
            v = sigma2 + tau2
            ll += -0.5 * (np.log(2 * np.pi * v) + z[0] ** 2 / v)
            continue
        d = np.sqrt(((xy[:i] - xy[i]) ** 2).sum(1))
        nb = np.argsort(d)[:m]
        C = matern(dists(xy[nb]), sigma2, rho, nu) + tau2 * np.eye(len(nb))
        c = matern(d[nb], sigma2, rho, nu)
        w = np.linalg.solve(C, c)
        mu = w @ z[nb]
        v = sigma2 + tau2 - c @ w
        ll += -0.5 * (np.log(2 * np.pi * v) + (z[i] - mu) ** 2 / v)
    return float(ll)


def vecchia_loglik_fast(xy, z, sigma2: float, rho: float, nu: float, tau2: float, m: int = 10, mean: float = 0.0) -> float:
    """Vecchia's approximation with neighbours found by a k-d tree: for each point (in coordinate order) the m nearest
    among the 4m nearest overall that come earlier.  Scales to 10^5 points."""
    from scipy.spatial import cKDTree

    xy, z = np.asarray(xy, float), np.asarray(z, float) - mean
    o = np.argsort(xy[:, 0] + xy[:, 1])
    xy, z = xy[o], z[o]
    n = len(z)
    _, nbrs = cKDTree(xy).query(xy, k=min(4 * m + 1, n))
    ll = 0.0
    for i in range(n):
        nb = nbrs[i][nbrs[i] < i][:m]
        if len(nb) == 0:
            v = sigma2 + tau2
            ll += -0.5 * (np.log(2 * np.pi * v) + z[i] ** 2 / v)
            continue
        C = matern(dists(xy[nb]), sigma2, rho, nu) + tau2 * np.eye(len(nb))
        c = matern(np.sqrt(((xy[nb] - xy[i]) ** 2).sum(1)), sigma2, rho, nu)
        w = np.linalg.solve(C, c)
        v = sigma2 + tau2 - c @ w
        ll += -0.5 * (np.log(2 * np.pi * v) + (z[i] - w @ z[nb]) ** 2 / v)
    return float(ll)


def exact_loglik(xy, z, sigma2, rho, nu, tau2, mean=0.0) -> float:
    z = np.asarray(z, float) - mean
    K = matern(dists(xy), sigma2, rho, nu) + tau2 * np.eye(len(z))
    L = linalg.cho_factor(K, lower=True)
    return float(-0.5 * (len(z) * np.log(2 * np.pi) + 2 * np.sum(np.log(np.diag(L[0]))) + z @ linalg.cho_solve(L, z)))


def gmrf_precision(nx: int, ny: int, kappa: float, tau: float = 1.0):
    """The precision of the SPDE (kappa^2 - Delta) u = W on an nx x ny grid with unit spacing (Lindgren, Rue &
    Lindstrom 2011, alpha = 2): Q = tau (K^T K), K = kappa^2 I + the 5-point negative Laplacian (free boundary).  A
    Gauss-Markov approximation to a Matern field with nu = 1, range about sqrt(8)/kappa; sparse."""
    n = nx * ny
    idx = np.arange(n).reshape(ny, nx)
    rows, cols, vals = [], [], []
    deg = np.zeros(n)
    for di, dj in ((0, 1), (1, 0)):
        a = idx[: ny - di, : nx - dj].ravel()
        b = idx[di:, dj:].ravel()
        rows += [a, b]
        cols += [b, a]
        vals += [-np.ones(len(a)), -np.ones(len(a))]
        np.add.at(deg, a, 1)
        np.add.at(deg, b, 1)
    Lap = sparse.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)).tocsr()
    Lap = Lap + sparse.diags(deg)
    Km = sparse.identity(n) * kappa ** 2 + Lap
    return (tau * (Km.T @ Km)).tocsc()


def gmrf_sample(Q, rng: np.random.Generator) -> np.ndarray:
    """A draw from N(0, Q^{-1}) via a dense Cholesky of Q (adequate for grids of a few thousand nodes)."""
    L = np.linalg.cholesky(Q.toarray())
    return linalg.solve_triangular(L.T, rng.standard_normal(Q.shape[0]), lower=False)


def gmrf_condition(Q, obs_idx, y, noise: float):
    """The posterior mean of a GMRF observed with Gaussian noise at some nodes: (Q + A'A/noise) mu = A'y/noise,
    solved sparsely."""
    n = Q.shape[0]
    A = sparse.coo_matrix((np.ones(len(obs_idx)), (np.arange(len(obs_idx)), obs_idx)), shape=(len(obs_idx), n)).tocsr()
    P = (Q + A.T @ A / noise).tocsc()
    return splinalg.spsolve(P, A.T @ np.asarray(y, float) / noise)


def morans_i(z, W, perms: int = 999, rng: np.random.Generator | None = None) -> dict:
    """Moran's (1950) I = (n / S0) (z - zbar)' W (z - zbar) / sum (z - zbar)^2, with a permutation p-value."""
    z = np.asarray(z, float)
    W = np.asarray(W, float)
    n = len(z)
    S0 = W.sum()

    def I(v):
        e = v - v.mean()
        return n / S0 * (e @ W @ e) / (e @ e)

    obs = I(z)
    rng = rng or np.random.default_rng(0)
    null = np.array([I(rng.permutation(z)) for _ in range(perms)])
    return {"I": float(obs), "E": -1 / (n - 1), "p": float((1 + np.sum(null >= obs)) / (perms + 1)), "null_sd": float(null.std())}


def icar_smooth(y, E, W, tau_u: float, tau_v: float, iters: int = 50) -> dict:
    """Disease mapping in the spirit of Besag, York & Mollie (1991): y_i ~ Poisson(E_i exp(eta_i)), eta = mu + u + v with
    u an intrinsic CAR (precision tau_u (D - W)) and v iid (precision tau_v).  Returns the posterior mode of the
    relative risks exp(eta) for given precisions, by Newton's method on (mu, eta) with eta's prior precision
    tau_u (D - W) + tau_v I combined approximately: here we use the precision P = (tau_u^{-1}(D - W + eps I)^{-1} +
    tau_v^{-1} I)^{-1} for eta - mu."""
    y, E = np.asarray(y, float), np.asarray(E, float)
    W = np.asarray(W, float)
    n = len(y)
    Dm = np.diag(W.sum(1))
    Cu = np.linalg.inv(tau_u * (Dm - W + 1e-3 * np.eye(n)))
    P = np.linalg.inv(Cu + np.eye(n) / tau_v)
    eta = np.log((y + 0.5) / E)
    mu = float(np.log(y.sum() / E.sum()))
    for _ in range(iters):
        lam = E * np.exp(eta)
        g = (y - lam) - P @ (eta - mu)
        H = np.diag(lam) + P
        step = np.linalg.solve(H, g)
        eta = eta + step
        mu = float(np.sum(P @ eta) / np.sum(P))
        if np.max(np.abs(step)) < 1e-10:
            break
    return {"rr": np.exp(eta), "mu": mu, "sd": np.sqrt(np.diag(np.linalg.inv(np.diag(E * np.exp(eta)) + P)))}


def ripley_k(xy, r, window) -> dict:
    """Ripley's (1976) K with border correction: for each r, count pairs closer than r among points at least r from
    the window's edge; window = (x0, x1, y0, y1).  L(r) = sqrt(K/pi) equals r under complete spatial randomness."""
    xy = np.asarray(xy, float)
    x0, x1, y0, y1 = window
    A = (x1 - x0) * (y1 - y0)
    n = len(xy)
    lam = n / A
    D = dists(xy)
    np.fill_diagonal(D, np.inf)
    b = np.minimum.reduce([xy[:, 0] - x0, x1 - xy[:, 0], xy[:, 1] - y0, y1 - xy[:, 1]])
    K = []
    for rr in np.asarray(r, float):
        keep = b >= rr
        if keep.sum() == 0:
            K.append(np.nan)
            continue
        K.append(np.sum(D[keep] < rr) / (lam * keep.sum()))
    K = np.array(K)
    return {"r": np.asarray(r, float), "K": K, "L": np.sqrt(K / np.pi)}


def csr_envelope(n: int, r, window, sims: int, rng: np.random.Generator) -> dict:
    """Pointwise min/max and 2.5/97.5% envelopes of L(r) - r over ``sims`` CSR patterns of n points."""
    x0, x1, y0, y1 = window
    Ls = []
    for _ in range(sims):
        pts = np.column_stack([rng.uniform(x0, x1, n), rng.uniform(y0, y1, n)])
        Ls.append(ripley_k(pts, r, window)["L"] - np.asarray(r, float))
    Ls = np.array(Ls)
    return {"lo": np.nanpercentile(Ls, 2.5, 0), "hi": np.nanpercentile(Ls, 97.5, 0), "min": np.nanmin(Ls, 0),
            "max": np.nanmax(Ls, 0)}


def gneiting(h, u, sigma2: float = 1.0, a: float = 1.0, c: float = 1.0, alpha: float = 1.0, beta: float = 1.0,
             gamma: float = 0.5, delta: float = 1.0, d: int = 2) -> np.ndarray:
    """Gneiting's (2002) space-time covariance: sigma^2 / psi(u^2)^{delta + beta d/2} exp(-c h^{2 gamma} /
    psi(u^2)^{beta gamma}), psi(t) = a t^alpha + 1.  beta in [0, 1] is the space-time interaction: beta = 0 gives the
    separable product of a temporal and a spatial covariance."""
    h, u = np.asarray(h, float), np.asarray(u, float)
    psi = a * np.abs(u) ** (2 * alpha) + 1
    return sigma2 / psi ** (delta + beta * d / 2) * np.exp(-c * h ** (2 * gamma) / psi ** (beta * gamma))


def expected_improvement(mu, sd, best: float) -> np.ndarray:
    """EI for minimization: E[max(best - f, 0)] under f ~ N(mu, sd^2)."""
    mu, sd = np.asarray(mu, float), np.maximum(np.asarray(sd, float), 1e-12)
    z = (best - mu) / sd
    return (best - mu) * stats.norm.cdf(z) + sd * stats.norm.pdf(z)
