"""statkit.ot: optimal transport for statistics (Part 61 of *Statistics, Built*).

    one-dimensional transport: the quantile coupling, W_p between samples, W_1 as the area between CDFs
    discrete transport: the assignment problem and the Kantorovich linear program, with its dual
    Gaussian W_2 in closed form (the Bures metric) and McCann's displacement interpolation
    empirical rates: W between two samples from the same law, n^{-1/d}           (Dudley 1969; Fournier & Guillin 2015)
    entropic transport by log-domain Sinkhorn and the Sinkhorn divergence        (Cuturi 2013; Genevay et al. 2019)
    transport maps: the empirical and the entropic (barycentric-projection) estimators  (Pooladian & Niles-Weed 2021)
    barycenters: quantile averaging in 1D, the Gaussian fixed point               (Agueh & Carlier 2011; Alvarez-Esteban et al. 2016)
    center-outward ranks and quantile contours, the rank energy test             (Hallin et al. 2021; Deb & Sen 2023)
    Langevin dynamics as the Wasserstein gradient flow of KL                     (Jordan, Kinderlehrer & Otto 1998)
    a toy flow-matching sampler by kernel regression                              (Lipman et al. 2023; Liu et al. 2023)
"""

from __future__ import annotations

import math

import numpy as np
from scipy import linalg, optimize, stats
from scipy.special import logsumexp

# ------------------------------------------------------------------------------------------------ one dimension


def wasserstein_1d(x, y, p: float = 1.0, grid: int = 4000) -> float:
    """W_p between the empirical laws of x and y in one dimension: (int_0^1 |F^{-1}(u) - G^{-1}(u)|^p du)^{1/p},
    exactly, by merging the two step quantile functions."""
    x, y = np.sort(np.asarray(x, float)), np.sort(np.asarray(y, float))
    n, m = len(x), len(y)
    us = np.unique(np.r_[np.arange(1, n) / n, np.arange(1, m) / m, 1.0])
    lo = np.r_[0.0, us[:-1]]
    mid = (lo + us) / 2
    qx = x[np.minimum((mid * n).astype(int), n - 1)]
    qy = y[np.minimum((mid * m).astype(int), m - 1)]
    return float(np.sum((us - lo) * np.abs(qx - qy) ** p) ** (1 / p))


def w1_cdf_area(x, y) -> float:
    """W_1 in one dimension as the area between the two empirical CDFs (equal to wasserstein_1d with p = 1)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    z = np.sort(np.r_[x, y])
    F = np.searchsorted(np.sort(x), z[:-1], side="right") / len(x)
    G = np.searchsorted(np.sort(y), z[:-1], side="right") / len(y)
    return float(np.sum(np.abs(F - G) * np.diff(z)))


def quantile_coupling(x, y) -> np.ndarray:
    """For equal sample sizes, the monotone (optimal for any convex cost) pairing: the i-th smallest x with the i-th
    smallest y.  Returns index pairs (i, j)."""
    ox, oy = np.argsort(x), np.argsort(y)
    return np.column_stack([ox, oy])


# ---------------------------------------------------------------------------------------------- discrete transport


def cost_matrix(X, Y, p: float = 2.0) -> np.ndarray:
    X, Y = np.atleast_2d(np.asarray(X, float)), np.atleast_2d(np.asarray(Y, float))
    if X.shape[0] == 1 and X.shape[1] > 1 and Y.shape[0] > 1 and Y.shape[1] == 1:
        X = X.T
    D = np.sqrt(np.maximum(((X[:, None, :] - Y[None, :, :]) ** 2).sum(-1), 0))
    return D ** p


def assignment(X, Y, p: float = 2.0) -> dict:
    """Optimal transport between two equal-size point clouds with uniform weights: a permutation, by the Hungarian
    algorithm.  Returns the permutation and W_p."""
    C = cost_matrix(X, Y, p)
    r, c = optimize.linear_sum_assignment(C)
    return {"perm": c, "cost": float(C[r, c].mean()), "W": float(C[r, c].mean() ** (1 / p))}


def kantorovich_lp(a, b, C) -> dict:
    """The Kantorovich problem min <P, C> over couplings of a and b, as a linear program (HiGHS), with the dual
    potentials (f, g) such that f_i + g_j <= C_ij, and sum a f + sum b g = the optimal cost."""
    a, b, C = np.asarray(a, float), np.asarray(b, float), np.asarray(C, float)
    n, m = C.shape
    A_eq = np.zeros((n + m, n * m))
    for i in range(n):
        A_eq[i, i * m:(i + 1) * m] = 1
    for j in range(m):
        A_eq[n + j, j::m] = 1
    res = optimize.linprog(C.ravel(), A_eq=A_eq[:-1], b_eq=np.r_[a, b][:-1], bounds=(0, None), method="highs")
    P = res.x.reshape(n, m)
    duals = np.r_[res.eqlin.marginals, 0.0]
    return {"P": P, "cost": float(res.fun), "f": duals[:n], "g": duals[n:]}


# ------------------------------------------------------------------------------------------------------ Gaussians


def sqrtm_psd(S) -> np.ndarray:
    w, V = np.linalg.eigh((np.asarray(S, float) + np.asarray(S, float).T) / 2)
    return (V * np.sqrt(np.maximum(w, 0))) @ V.T


def gaussian_w2(m1, S1, m2, S2) -> float:
    """W_2 between N(m1, S1) and N(m2, S2): |m1 - m2|^2 + tr(S1 + S2 - 2 (S1^{1/2} S2 S1^{1/2})^{1/2})."""
    m1, m2 = np.atleast_1d(m1).astype(float), np.atleast_1d(m2).astype(float)
    S1, S2 = np.atleast_2d(S1).astype(float), np.atleast_2d(S2).astype(float)
    r = sqrtm_psd(S1)
    b = np.trace(S1 + S2 - 2 * sqrtm_psd(r @ S2 @ r))
    return float(math.sqrt(max(np.sum((m1 - m2) ** 2) + b, 0)))


def gaussian_map(S1, S2) -> np.ndarray:
    """The optimal (Brenier) map between centred Gaussians, x -> A x with A = S1^{-1/2}(S1^{1/2} S2 S1^{1/2})^{1/2} S1^{-1/2}."""
    r = sqrtm_psd(S1)
    ri = np.linalg.inv(r)
    return ri @ sqrtm_psd(r @ S2 @ r) @ ri


def displacement(X, Y, perm, t: float) -> np.ndarray:
    """McCann's interpolation between two matched clouds: (1 - t) x_i + t y_{perm(i)}."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    return (1 - t) * X + t * Y[perm]


# ------------------------------------------------------------------------------------------------- empirical rates


def empirical_rate(d: int, ns, reps: int, rng: np.random.Generator, p: float = 1.0) -> dict:
    """E W_p between two independent samples of size n from the uniform law on [0, 1]^d, by exact assignment; its
    slope against n on a log-log scale is about -1/d for d >= 3 (and -1/2 for d = 1)."""
    out = []
    for n in ns:
        v = []
        for _ in range(reps):
            v.append(assignment(rng.random((n, d)), rng.random((n, d)), p)["W"])
        out.append(float(np.mean(v)))
    slope = float(np.polyfit(np.log(ns), np.log(out), 1)[0])
    return {"ns": list(ns), "W": out, "slope": slope}


# -------------------------------------------------------------------------------------------------------- Sinkhorn


def sinkhorn(a, b, C, eps: float, iters: int = 2000, tol: float = 1e-10) -> dict:
    """Entropic OT min <P, C> - eps H(P) by log-domain Sinkhorn: alternating the dual updates
    f = -eps log sum_j b_j exp((g_j - C_ij)/eps), and the same for g.  Returns the plan, the transport cost <P, C>,
    the entropic objective, the dual potentials and the marginal error per iteration.  The linear rate worsens as
    eps shrinks (at eps well below the typical cost it can need more than ``iters`` sweeps), so the loop may stop at
    the cap: ``converged`` says whether the last marginal error is below ``tol``."""
    a, b, C = np.asarray(a, float), np.asarray(b, float), np.asarray(C, float)
    la, lb = np.log(a), np.log(b)
    f, g = np.zeros(len(a)), np.zeros(len(b))
    errs = []
    for _ in range(iters):
        f = -eps * logsumexp((g[None, :] - C) / eps + lb[None, :], axis=1)
        g = -eps * logsumexp((f[:, None] - C) / eps + la[:, None], axis=0)
        logP = (f[:, None] + g[None, :] - C) / eps + la[:, None] + lb[None, :]
        P = np.exp(logP)
        err = float(np.abs(P.sum(1) - a).sum())
        errs.append(err)
        if err < tol:
            break
    obj = float(np.sum(a * f) + np.sum(b * g))
    return {"P": P, "cost": float(np.sum(P * C)), "obj": obj, "f": f, "g": g, "errs": errs, "iters": len(errs),
            "converged": bool(errs[-1] < tol)}


def sinkhorn_divergence(X, Y, eps: float, p: float = 2.0) -> float:
    """Genevay et al.'s debiased S_eps(mu, nu) = OT_eps(mu, nu) - (OT_eps(mu, mu) + OT_eps(nu, nu))/2, with the
    entropic objective, for uniform empirical measures."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    a, b = np.full(len(X), 1 / len(X)), np.full(len(Y), 1 / len(Y))

    def ot(U, V, u, v):
        return sinkhorn(u, v, cost_matrix(U, V, p), eps, 3000, 1e-9)["obj"]
    return float(ot(X, Y, a, b) - 0.5 * ot(X, X, a, a) - 0.5 * ot(Y, Y, b, b))


# -------------------------------------------------------------------------------------------------- transport maps


def entropic_map(X, Y, eps: float):
    """Pooladian & Niles-Weed's entropic map estimator: the barycentric projection of the entropic plan,
    T(x) = sum_j y_j exp((g_j - |x - y_j|^2/2)/eps) / sum_j exp(...), extended to new x through the potential g."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    n, m = len(X), len(Y)
    C = cost_matrix(X, Y, 2) / 2
    s = sinkhorn(np.full(n, 1 / n), np.full(m, 1 / m), C, eps, 3000, 1e-9)
    g = s["g"]

    def T(Z):
        Z = np.atleast_2d(np.asarray(Z, float))
        Cz = cost_matrix(Z, Y, 2) / 2
        L = (g[None, :] - Cz) / eps
        W = np.exp(L - L.max(1, keepdims=True))
        W /= W.sum(1, keepdims=True)
        return W @ Y
    return T


# ---------------------------------------------------------------------------------------------------- barycenters


def barycenter_1d(samples, weights=None, grid: int = 400) -> np.ndarray:
    """The W_2 barycenter of one-dimensional laws: average the quantile functions.  Returns the barycenter's
    quantiles at the midpoints of ``grid`` equal cells of (0, 1)."""
    k = len(samples)
    w = np.full(k, 1 / k) if weights is None else np.asarray(weights, float)
    u = (np.arange(grid) + 0.5) / grid
    Q = np.array([np.quantile(np.asarray(s, float), u) for s in samples])
    return w @ Q


def gaussian_barycenter(covs, weights=None, iters: int = 200, tol: float = 1e-12) -> np.ndarray:
    """The W_2 barycenter of centred Gaussians: the fixed point S = sum_k w_k (S^{1/2} S_k S^{1/2})^{1/2}, by
    Alvarez-Esteban et al.'s iteration S <- S^{-1/2} (sum_k w_k (S^{1/2} S_k S^{1/2})^{1/2})^2 S^{-1/2}."""
    covs = [np.atleast_2d(np.asarray(c, float)) for c in covs]
    k = len(covs)
    w = np.full(k, 1 / k) if weights is None else np.asarray(weights, float)
    S = sum(wi * c for wi, c in zip(w, covs))
    for _ in range(iters):
        r = sqrtm_psd(S)
        ri = np.linalg.inv(r)
        M = sum(wi * sqrtm_psd(r @ c @ r) for wi, c in zip(w, covs))
        Sn = ri @ M @ M @ ri
        if np.max(np.abs(Sn - S)) < tol:
            S = Sn
            break
        S = Sn
    return (S + S.T) / 2


# ------------------------------------------------------------------------------------- center-outward ranks


def spherical_grid(n: int, rng: np.random.Generator | None = None, n_rad: int | None = None) -> np.ndarray:
    """Hallin et al.'s regular grid in the unit disc: n_R radii (j/(n_R + 1)) times n_S equally spaced directions,
    with n_R n_S = n (plus the origin when n is odd).  The angles are rotated by a fixed offset."""
    if n_rad is None:
        n_rad = int(round(math.sqrt(n / (2 * math.pi)) * 1.0)) or 1
    n_s = n // n_rad
    pts = []
    off = 0.1234
    for j in range(1, n_rad + 1):
        r = j / (n_rad + 1)
        th = 2 * math.pi * (np.arange(n_s) + off) / n_s
        pts.append(np.column_stack([r * np.cos(th), r * np.sin(th)]))
    G = np.vstack(pts)
    while len(G) < n:
        G = np.vstack([G, np.zeros((1, 2))])
    return G[:n]


def center_outward(X, grid=None) -> dict:
    """Center-outward ranks and signs (Chernozhukov, Galichon, Hallin & Henry 2017; Hallin, del Barrio,
    Cuesta-Albertos & Matran 2021): the optimal assignment of the n data points to a regular grid in the unit disc.
    A point's center-outward rank is the radius of its grid point, its sign the grid point's direction."""
    X = np.asarray(X, float)
    G = spherical_grid(len(X)) if grid is None else np.asarray(grid, float)
    C = cost_matrix(X, G, 2)
    r, c = optimize.linear_sum_assignment(C)
    F = np.empty_like(G)
    F[r] = G[c]
    return {"F": F, "rank": np.linalg.norm(F, axis=1), "grid": G}


def energy_distance(X, Y) -> float:
    """The energy statistic 2E|X - Y| - E|X - X'| - E|Y - Y'| for two samples (V-statistic form)."""
    X, Y = np.atleast_2d(X), np.atleast_2d(Y)
    dxy = cost_matrix(X, Y, 1).mean()
    dxx = cost_matrix(X, X, 1).mean()
    dyy = cost_matrix(Y, Y, 1).mean()
    return float(2 * dxy - dxx - dyy)


def rank_energy_test(X, Y, rng: np.random.Generator, perms: int = 200, ref=None) -> dict:
    """Deb & Sen's rank energy test: transport the pooled sample to a fixed reference set (Halton points in the unit
    square), then compute the energy distance between the two groups' ranks.  The ranks of the pooled sample are a
    fixed set under H0, so the permutation null is exactly distribution-free."""
    X, Y = np.atleast_2d(X), np.atleast_2d(Y)
    Z = np.vstack([X, Y])
    N, n = len(Z), len(X)
    if ref is None:
        ref = stats.qmc.Halton(d=Z.shape[1], scramble=False).random(N + 1)[1:]
    C = cost_matrix(Z, ref, 2)
    r, c = optimize.linear_sum_assignment(C)
    R = np.empty_like(ref)
    R[r] = ref[c]
    obs = energy_distance(R[:n], R[n:])
    cnt = 0
    for _ in range(perms):
        o = rng.permutation(N)
        cnt += energy_distance(R[o[:n]], R[o[n:]]) >= obs - 1e-12
    return {"stat": obs, "p": (1 + cnt) / (1 + perms)}


def hotelling_two_sample(X, Y) -> dict:
    """Hotelling's two-sample T^2 with pooled covariance and its exact F p-value (under normality)."""
    X, Y = np.atleast_2d(X), np.atleast_2d(Y)
    n, m, d = len(X), len(Y), X.shape[1]
    S = ((n - 1) * np.cov(X.T) + (m - 1) * np.cov(Y.T)) / (n + m - 2)
    diff = X.mean(0) - Y.mean(0)
    T2 = float(n * m / (n + m) * diff @ np.linalg.solve(np.atleast_2d(S), diff))
    F = T2 * (n + m - d - 1) / (d * (n + m - 2))
    return {"T2": T2, "p": float(stats.f.sf(F, d, n + m - d - 1))}


# -------------------------------------------------------------------------------------------------- gradient flows


def langevin(grad_logp, X0, h: float, steps: int, rng: np.random.Generator, every: int = 1) -> list:
    """Unadjusted Langevin: X <- X + h grad log p(X) + sqrt(2h) Z, for a cloud of particles; returns snapshots."""
    X = np.asarray(X0, float).copy()
    snaps = [X.copy()]
    for k in range(1, steps + 1):
        X = X + h * grad_logp(X) + math.sqrt(2 * h) * rng.standard_normal(X.shape)
        if k % every == 0:
            snaps.append(X.copy())
    return snaps


def gaussian_kl(m1, S1, m2, S2) -> float:
    """KL(N(m1, S1) || N(m2, S2))."""
    m1, m2 = np.atleast_1d(m1).astype(float), np.atleast_1d(m2).astype(float)
    S1, S2 = np.atleast_2d(S1).astype(float), np.atleast_2d(S2).astype(float)
    d = len(m1)
    S2i = np.linalg.inv(S2)
    dm = m2 - m1
    return float(0.5 * (np.trace(S2i @ S1) + dm @ S2i @ dm - d + np.log(np.linalg.det(S2) / np.linalg.det(S1))))


def fokker_planck_gaussian(m0, S0, mu, Sig, ts) -> list:
    """The exact law of the Langevin diffusion dX = -Sig^{-1}(X - mu) dt + sqrt 2 dW from N(m0, S0): Gaussian with
    m(t) = mu + e^{-At}(m0 - mu), S(t) = e^{-At} S0 e^{-At} + Sig - e^{-At} Sig e^{-At}, A = Sig^{-1}.  This is the
    Wasserstein gradient flow of KL(. || N(mu, Sig)) (Jordan, Kinderlehrer & Otto)."""
    A = np.linalg.inv(np.atleast_2d(Sig))
    out = []
    for t in ts:
        E = linalg.expm(-A * t)
        m = mu + E @ (np.asarray(m0, float) - mu)
        S = E @ S0 @ E.T + Sig - E @ Sig @ E.T
        out.append((m, S))
    return out


# ------------------------------------------------------------------------------------------------- flow matching


def flow_matching_fit(X0, X1, rng: np.random.Generator, bw: float = 0.25, n_t: int = 20, pair: str = "independent"):
    """A toy conditional flow-matching model: along straight paths x_t = (1 - t) x0 + t x1 the velocity is x1 - x0;
    regress it on (x_t, t) by Nadaraya-Watson.  ``pair`` = "independent" pairs at random (Lipman et al.; Liu et al.),
    "ot" pairs by optimal assignment (Tong et al.; Pooladian et al.), which straightens the paths.  Returns the
    velocity field v(x, t)."""
    X0, X1 = np.asarray(X0, float), np.asarray(X1, float)
    if pair == "ot":
        X1 = X1[assignment(X0, X1, 2)["perm"]]
    ts = (np.arange(n_t) + 0.5) / n_t
    P, V, T = [], [], []
    for t in ts:
        P.append((1 - t) * X0 + t * X1)
        V.append(X1 - X0)
        T.append(np.full(len(X0), t))
    P, V, T = np.vstack(P), np.vstack(V), np.concatenate(T)

    def v(x, t):
        x = np.atleast_2d(x)
        d2 = ((x[:, None, :] - P[None]) ** 2).sum(-1) + ((t - T[None, :]) / 0.1) ** 2 * bw * bw
        L = -d2 / (2 * bw * bw)
        W = np.exp(L - L.max(1, keepdims=True))
        W /= W.sum(1, keepdims=True)
        return W @ V
    return v


def integrate_flow(v, X0, steps: int = 20) -> list:
    """Euler steps of dx/dt = v(x, t) from t = 0 to 1, the velocity read at the start of each step; returns the
    snapshots."""
    X = np.asarray(X0, float).copy()
    snaps = [X.copy()]
    for k in range(steps):
        X = X + v(X, k / steps) / steps
        snaps.append(X.copy())
    return snaps
