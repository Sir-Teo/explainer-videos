"""statkit.hdstat: high-dimensional statistics (Part 52 of *Statistics, Built*).

Checked in ``tests/test_stats_kit_hdstat.py``:

* random-matrix laws: the Marchenko-Pastur Stieltjes transform and the density recovered from it; Wigner's semicircle;
* spiked covariance models: the BBP limit of the top eigenvalue and of the eigenvector overlap, its inversion, the
  top eigenvalue's fluctuation, and an interval for a spike;
* Tracy-Widom laws for beta = 1 and 2 by Bornemann's quadrature of Fredholm determinants; Johnstone's centring and
  scaling; Roy's largest-root test;
* the lasso: errors against the oracle rate, the irrepresentable condition, exact signed-support recovery along the
  LARS path;
* covariance estimation: banding, thresholding and Ledoit-Wolf shrinkage;
* Davis-Kahan's sin-theta bound;
* sparse PCA by diagonal thresholding; neighbourhood selection for Gaussian graphical models;
* low-rank matrices for completion.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import special

from explainer.stats.kit import sparse as SPK

# ------------------------------------------------------------------------------------------ random-matrix laws


def mp_edges(gamma: float) -> tuple:
    return (1 - math.sqrt(gamma)) ** 2, (1 + math.sqrt(gamma)) ** 2


def mp_pdf(x, gamma: float) -> np.ndarray:
    """Marchenko-Pastur density (variance 1, ratio gamma = p/n <= 1)."""
    x = np.asarray(x, float)
    a, b = mp_edges(gamma)
    out = np.zeros_like(x)
    m = (x > a) & (x < b)
    out[m] = np.sqrt((b - x[m]) * (x[m] - a)) / (2 * math.pi * gamma * x[m])
    return out


def mp_stieltjes(z, gamma: float) -> np.ndarray:
    """m(z) = int dF(x)/(x - z) for Marchenko-Pastur: the root of gamma z m^2 + (z + gamma - 1) m + 1 = 0 with
    Im m > 0 when Im z > 0 (Marchenko & Pastur 1967; Silverstein 1995)."""
    z = np.asarray(z, complex)
    A, B = gamma * z, z + gamma - 1
    disc = np.sqrt(B * B - 4 * A)
    r1, r2 = (-B + disc) / (2 * A), (-B - disc) / (2 * A)
    return np.where(r1.imag > 0, r1, r2)


def density_from_stieltjes(x, gamma: float, eta: float = 1e-6) -> np.ndarray:
    """Stieltjes inversion: f(x) = lim Im m(x + i eta) / pi."""
    return np.imag(mp_stieltjes(np.asarray(x, float) + 1j * eta, gamma)) / math.pi


def semicircle_pdf(x) -> np.ndarray:
    x = np.asarray(x, float)
    return np.where(np.abs(x) < 2, np.sqrt(np.maximum(4 - x * x, 0)) / (2 * math.pi), 0.0)


def wigner(n: int, rng: np.random.Generator) -> np.ndarray:
    """Eigenvalues of a GOE matrix scaled so the spectrum fills [-2, 2]."""
    G = rng.standard_normal((n, n))
    return np.linalg.eigvalsh((G + G.T) / math.sqrt(2 * n))


# ------------------------------------------------------------------------------------------------ spikes


def spike_eigenvalue(ell, gamma: float) -> np.ndarray:
    """Limit of the top sample eigenvalue when Sigma = I + ell v v^T (Baik, Ben Arous & Peche 2005; Baik &
    Silverstein 2006): (1 + ell)(1 + gamma/ell) above the threshold ell > sqrt(gamma), the MP edge below it."""
    ell = np.asarray(ell, float)
    edge = (1 + math.sqrt(gamma)) ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        above = (1 + ell) * (1 + gamma / ell)
    return np.where(ell > math.sqrt(gamma), above, edge)


def spike_overlap(ell, gamma: float) -> np.ndarray:
    """Limit of <v_hat, v>^2 (Paul 2007): (1 - gamma/ell^2)/(1 + gamma/ell) above the threshold, 0 below."""
    ell = np.asarray(ell, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        above = (1 - gamma / ell ** 2) / (1 + gamma / ell)
    return np.where(ell > math.sqrt(gamma), above, 0.0)


def spike_invert(lhat: float, gamma: float) -> float:
    """Solve (1 + ell)(1 + gamma/ell) = lhat for ell > sqrt(gamma); nan at or below the edge."""
    c = lhat - 1 - gamma
    d = c * c - 4 * gamma
    if d < 0 or c <= 0:
        return float("nan")
    return (c + math.sqrt(d)) / 2


def spike_sd(ell: float, gamma: float, n: int) -> float:
    """Asymptotic SD of the top sample eigenvalue above the threshold, real Gaussian data (Paul 2007; Bai & Yao
    2008): sqrt(2/n) (1 + ell) sqrt(1 - gamma/ell^2)."""
    return math.sqrt(2 / n) * (1 + ell) * math.sqrt(max(1 - gamma / ell ** 2, 0.0))


def spike_ci(lhat: float, n: int, gamma: float, level: float = 0.95) -> tuple:
    """An interval for the population spike 1 + ell, inverting the BBP map with a delta-method SE."""
    ell = spike_invert(lhat, gamma)
    if not np.isfinite(ell):
        return (float("nan"), float("nan"))
    z = special.ndtri(0.5 + level / 2)
    dpsi = 1 - gamma / ell ** 2  # d/d ell of (1 + ell)(1 + gamma/ell)
    se = spike_sd(ell, gamma, n) / dpsi
    return (1 + ell - z * se, 1 + ell + z * se)


def anderson_ci(lhat: float, n: int, level: float = 0.95) -> tuple:
    """The classical (fixed-p) interval for a simple population eigenvalue (Anderson 1963): lhat (1 +- z sqrt(2/n))."""
    z = special.ndtri(0.5 + level / 2)
    return (lhat / (1 + z * math.sqrt(2 / n)), lhat / (1 - z * math.sqrt(2 / n)))


def spiked_sample(n: int, p: int, ell: float, rng: np.random.Generator, v=None):
    """n draws from N(0, I + ell v v^T); v defaults to e_1."""
    v = np.eye(p)[0] if v is None else np.asarray(v, float) / np.linalg.norm(v)
    Z = rng.standard_normal((n, p))
    return Z + (math.sqrt(1 + ell) - 1) * np.outer(Z @ v, v)


def top_eig(X) -> tuple:
    n = X.shape[0]
    w, V = np.linalg.eigh(X.T @ X / n)
    return float(w[-1]), V[:, -1]


# ----------------------------------------------------------------------------------------------- Tracy-Widom


def _airy_kernel(x, y):
    ai_x, aip_x, _, _ = special.airy(x)
    ai_y, aip_y, _, _ = special.airy(y)
    X, Y = np.meshgrid(x, y, indexing="ij")
    num = np.outer(ai_x, aip_y) - np.outer(aip_x, ai_y)
    with np.errstate(divide="ignore", invalid="ignore"):
        K = num / (X - Y)
    d = aip_x ** 2 - x * ai_x ** 2
    K[np.diag_indices_from(K)] = d
    return K


def tracy_widom_cdf(s, beta: int = 1, m: int = 64, L: float = 14.0) -> np.ndarray:
    """F_beta(s) by Gauss-Legendre quadrature of a Fredholm determinant on (s, s + L) (Bornemann 2010):
    F_2(s) = det(I - K_Airy) and F_1(s) = det(I - K_1), K_1(x, y) = Ai((x + y)/2)/2."""
    u, w = np.polynomial.legendre.leggauss(m)
    out = []
    for s0 in np.atleast_1d(np.asarray(s, float)):
        x = s0 + (u + 1) * L / 2
        ww = w * L / 2
        sq = np.sqrt(ww)
        if beta == 2:
            K = _airy_kernel(x, x)
        elif beta == 1:
            K = 0.5 * special.airy((x[:, None] + x[None, :]) / 2)[0]
        else:
            raise ValueError("beta must be 1 or 2")
        out.append(float(np.linalg.det(np.eye(m) - sq[:, None] * K * sq[None, :])))
    return np.clip(np.array(out), 0.0, 1.0)


def tracy_widom_pdf(s, beta: int = 1, h: float = 1e-3) -> np.ndarray:
    s = np.asarray(s, float)
    return (tracy_widom_cdf(s + h, beta) - tracy_widom_cdf(s - h, beta)) / (2 * h)


def tracy_widom_quantile(q: float, beta: int = 1) -> float:
    lo, hi = -8.0, 8.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if tracy_widom_cdf(mid, beta)[0] < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def tracy_widom_moments(beta: int = 1) -> dict:
    s = np.linspace(-8, 8, 1601)
    f = tracy_widom_pdf(s, beta)
    mean = float(np.trapezoid(s * f, s))
    var = float(np.trapezoid((s - mean) ** 2 * f, s))
    return {"mean": mean, "sd": math.sqrt(var)}


def johnstone_center_scale(n: int, p: int) -> tuple:
    """For the top eigenvalue l of X^T X with X n x p standard normal (Johnstone 2001):
    (l - mu)/sigma -> TW1, mu = (sqrt(n - 1) + sqrt p)^2, sigma = (sqrt(n - 1) + sqrt p)(1/sqrt(n - 1) + 1/sqrt p)^(1/3)."""
    a, b = math.sqrt(n - 1), math.sqrt(p)
    return (a + b) ** 2, (a + b) * (1 / a + 1 / b) ** (1 / 3)


# --------------------------------------------------------------------------------------------------- lasso


def lasso_lambda(n: int, p: int, sigma: float = 1.0, c: float = 2.0) -> float:
    """The theory's choice lam = c sigma sqrt(2 log p / n) (glmnet scaling, (1/2n)||y - Xb||^2 + lam||b||_1)."""
    return c * sigma * math.sqrt(2 * math.log(p) / n) / 2


def oracle_rate(n: int, p: int, s: int, sigma: float = 1.0) -> float:
    """sigma sqrt(s log p / n): the l2 rate the lasso attains under restricted eigenvalues."""
    return sigma * math.sqrt(s * math.log(p) / n)


def irrepresentable(X, S, signs) -> float:
    """||X_{S^c}^T X_S (X_S^T X_S)^{-1} sign(beta_S)||_inf; the lasso can recover the signed support only if < 1
    (Zhao & Yu 2006; Wainwright 2009)."""
    X = np.asarray(X, float)
    S = np.asarray(S)
    Sc = np.setdiff1d(np.arange(X.shape[1]), S)
    v = X[:, Sc].T @ X[:, S] @ np.linalg.solve(X[:, S].T @ X[:, S], np.asarray(signs, float))
    return float(np.max(np.abs(v)))


def signed_support_on_path(X, y, beta) -> bool:
    """Does any point on the exact lasso path (LARS-lasso) have exactly the signed support of beta?"""
    path = SPK.lars(X, y, lasso=True)
    target = np.sign(beta)
    for b in np.asarray(path["coefs"]):
        if np.array_equal(np.sign(np.round(b, 12)), target):
            return True
    return False


# --------------------------------------------------------------------------------------------- covariances


def ar1_cov(p: int, rho: float) -> np.ndarray:
    i = np.arange(p)
    return rho ** np.abs(i[:, None] - i[None, :])


def band(S, k: int) -> np.ndarray:
    """Banding (Bickel & Levina 2008a): keep entries with |i - j| <= k."""
    S = np.asarray(S, float)
    i = np.arange(S.shape[0])
    return S * (np.abs(i[:, None] - i[None, :]) <= k)


def threshold(S, t: float) -> np.ndarray:
    """Hard thresholding of off-diagonal entries (Bickel & Levina 2008b)."""
    S = np.asarray(S, float)
    T = S * (np.abs(S) >= t)
    T[np.diag_indices_from(T)] = np.diag(S)
    return T


def ledoit_wolf(X) -> tuple:
    """Ledoit & Wolf's (2004) shrinkage towards mu I: returns (Sigma_hat, intensity)."""
    X = np.asarray(X, float)
    n, p = X.shape
    Xc = X - X.mean(0)
    S = Xc.T @ Xc / n
    mu = np.trace(S) / p
    d2 = np.sum((S - mu * np.eye(p)) ** 2) / p
    b2 = sum(np.sum((np.outer(x, x) - S) ** 2) for x in Xc) / (n * n * p)
    b2 = min(b2, d2)
    rho = b2 / d2 if d2 > 0 else 0.0
    return rho * mu * np.eye(p) + (1 - rho) * S, float(rho)


def op_norm(A) -> float:
    return float(np.linalg.norm(np.asarray(A, float), 2))


# ------------------------------------------------------------------------------------------ perturbation


def sin_theta(u, v) -> float:
    u, v = np.asarray(u, float), np.asarray(v, float)
    c = abs(u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return math.sqrt(max(1 - c * c, 0.0))


def davis_kahan(E_norm: float, gap: float) -> float:
    """The Yu-Wang-Samworth (2015) form: sin theta <= 2 ||E||_op / gap, capped at 1."""
    return min(1.0, 2 * E_norm / gap)


# ------------------------------------------------------------------------------------- sparse PCA, graphs


def diagonal_thresholding(X, k: int) -> np.ndarray:
    """Johnstone & Lu (2009): PCA on the k coordinates with the largest sample variances."""
    X = np.asarray(X, float)
    n, p = X.shape
    var = (X ** 2).mean(0)
    idx = np.argsort(var)[-k:]
    S = X[:, idx].T @ X[:, idx] / n
    w, V = np.linalg.eigh(S)
    v = np.zeros(p)
    v[idx] = V[:, -1]
    return v


def sparse_spike_sample(n: int, p: int, k: int, ell: float, rng: np.random.Generator):
    v = np.zeros(p)
    v[:k] = 1 / math.sqrt(k)
    return spiked_sample(n, p, ell, rng, v=v), v


def neighbourhood_selection(X, lam: float, rule: str = "and") -> np.ndarray:
    """Meinshausen & Buhlmann (2006): regress each variable on the others by the lasso; edge if selected
    (both ways for 'and', either for 'or')."""
    X = np.asarray(X, float)
    X = (X - X.mean(0)) / X.std(0)
    n, p = X.shape
    B = np.zeros((p, p), bool)
    for j in range(p):
        others = np.delete(np.arange(p), j)
        b = SPK.lasso_cd(X[:, others], X[:, j], lam)
        B[j, others] = b != 0
    return (B & B.T) if rule == "and" else (B | B.T)


def chain_precision(p: int, a: float = 0.4) -> np.ndarray:
    """A tridiagonal precision matrix: the chain graph."""
    Q = np.eye(p)
    for i in range(p - 1):
        Q[i, i + 1] = Q[i + 1, i] = a
    return Q


# ------------------------------------------------------------------------------------------------ low rank


def low_rank(n1: int, n2: int, r: int, rng: np.random.Generator) -> np.ndarray:
    U = rng.standard_normal((n1, r))
    V = rng.standard_normal((n2, r))
    return U @ V.T / math.sqrt(r)
