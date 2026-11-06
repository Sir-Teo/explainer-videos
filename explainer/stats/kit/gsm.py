"""statkit.gsm: the Gaussian sequence model and a lower-bound workbench (Part 50 of *Statistics, Built*).

Checked in ``tests/test_stats_kit_gsm.py``:

* the Gaussian sequence model y_k = theta_k + eps z_k; Sobolev ellipsoids sum a_k^2 theta_k^2 <= C^2, a_k = k^alpha;
* Pinsker's minimax linear estimator and risk, its least favourable Gaussian prior, and Pinsker's constant;
* estimators: projection (truncation), Pinsker, blockwise James-Stein on dyadic blocks, soft and hard thresholding;
* divergences: total variation, Hellinger and Kullback-Leibler for normals and Bernoullis; Pinsker's and Le Cam's
  inequalities;
* Le Cam's two-point bound for a density at a point (a bump of height h and width w), optimized over the bump;
* Fano's bound with the Varshamov-Gilbert packing; the sparse-means rate s log(p/s);
* Assouad's hypercube bound for Hoelder regression;
* Lepski's bandwidth choice for a value at a point in white-noise regression;
* the sparse-mixture detection boundary and Donoho-Jin's higher criticism;
* a planted-clique detector by total degree.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats

# --------------------------------------------------------------------------------------------- the GSM, Pinsker


def sobolev_weights(K: int, alpha: float) -> np.ndarray:
    return np.arange(1, K + 1, dtype=float) ** alpha


def pinsker(eps: float, a, C: float) -> dict:
    """Pinsker (1980): over {sum a_k^2 theta_k^2 <= C^2} in y_k = theta_k + eps z_k, the minimax linear estimator is
    theta_hat_k = (1 - a_k/mu)_+ y_k, with mu solving eps^2 sum a_k (mu - a_k)_+ = C^2, and its maximal risk is
    eps^2 sum (1 - a_k/mu)_+; the least favourable prior is Gaussian with variances eps^2 (mu/a_k - 1)_+."""
    a = np.asarray(a, float)

    def g(mu):
        return eps ** 2 * np.sum(a * np.maximum(mu - a, 0)) - C ** 2

    lo, hi = a.min(), a.min() + 1.0
    while g(hi) < 0:
        hi *= 2
    mu = optimize.brentq(g, lo, hi)
    shrink = np.maximum(1 - a / mu, 0)
    risk = eps ** 2 * float(np.sum(shrink))
    prior_var = eps ** 2 * np.maximum(mu / a - 1, 0)
    # the Bayes risk of the Gaussian prior: sum s^2 eps^2/(s^2 + eps^2) -- equals the linear minimax risk
    bayes = float(np.sum(prior_var * eps ** 2 / (prior_var + eps ** 2)))
    return {"mu": mu, "shrink": shrink, "risk": risk, "prior_var": prior_var, "bayes": bayes, "N": int(np.sum(shrink > 0))}


def pinsker_constant(alpha: float) -> float:
    """P(alpha) = (2 alpha + 1)^(1/(2 alpha + 1)) (alpha/(alpha + 1))^(2 alpha/(2 alpha + 1))."""
    r = 1 / (2 * alpha + 1)
    return (2 * alpha + 1) ** r * (alpha / (alpha + 1)) ** (2 * alpha * r)


def pinsker_asymptotic(eps: float, alpha: float, C: float) -> float:
    """The asymptotic minimax risk P(alpha) C^(2/(2alpha+1)) eps^(4alpha/(2alpha+1))."""
    return pinsker_constant(alpha) * C ** (2 / (2 * alpha + 1)) * eps ** (4 * alpha / (2 * alpha + 1))


def hardest_theta(eps: float, a, C: float) -> np.ndarray:
    """A deterministic point on the ellipsoid with |theta_k| = sqrt of the least favourable prior variance (rescaled
    onto the boundary): a natural 'hard' truth for simulations."""
    p = pinsker(eps, a, C)
    th = np.sqrt(p["prior_var"])
    a = np.asarray(a, float)
    s = math.sqrt(np.sum(a ** 2 * th ** 2))
    return th * C / s if s > 0 else th


def est_truncation(y, N: int) -> np.ndarray:
    y = np.asarray(y, float)
    out = np.zeros_like(y)
    out[..., :N] = y[..., :N]
    return out


def est_linear(y, shrink) -> np.ndarray:
    return np.asarray(y, float) * np.asarray(shrink, float)


def dyadic_blocks(K: int) -> list:
    """Blocks {1}, {2,3}, {4..7}, ... of indices 0-based."""
    out, start, size = [], 0, 1
    while start < K:
        out.append(np.arange(start, min(start + size, K)))
        start += size
        size *= 2
    return out


def est_block_js(y, eps: float, blocks=None) -> np.ndarray:
    """Blockwise positive-part James-Stein: theta_B = (1 - eps^2 |B| / ||y_B||^2)_+ y_B on dyadic blocks (Efromovich &
    Pinsker 1984; Cai 1999), adaptive: it needs no knowledge of alpha or C."""
    y = np.atleast_2d(np.asarray(y, float))
    blocks = blocks or dyadic_blocks(y.shape[1])
    out = np.zeros_like(y)
    for B in blocks:
        s = np.sum(y[:, B] ** 2, axis=1, keepdims=True)
        out[:, B] = np.maximum(1 - eps ** 2 * len(B) / np.maximum(s, 1e-300), 0) * y[:, B]
    return out


def est_soft(y, t) -> np.ndarray:
    y = np.asarray(y, float)
    return np.sign(y) * np.maximum(np.abs(y) - t, 0)


def est_hard(y, t) -> np.ndarray:
    y = np.asarray(y, float)
    return np.where(np.abs(y) > t, y, 0.0)


# ------------------------------------------------------------------------------------------------ divergences


def tv_normal(d: float, sigma: float = 1.0) -> float:
    """TV(N(0, s^2), N(d, s^2)) = 2 Phi(|d|/(2s)) - 1."""
    return float(2 * stats.norm.cdf(abs(d) / (2 * sigma)) - 1)


def kl_normal(d: float, sigma: float = 1.0) -> float:
    return d ** 2 / (2 * sigma ** 2)


def hellinger2_normal(d: float, sigma: float = 1.0) -> float:
    """H^2 = 1 - exp(-d^2/(8 s^2)) (with H^2 = 1 - Bhattacharyya affinity)."""
    return float(1 - math.exp(-d ** 2 / (8 * sigma ** 2)))


def kl_bernoulli(p: float, q: float) -> float:
    return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))


def tv_product_normal(d: float, n: int) -> float:
    """TV between N(0,1)^n and N(d,1)^n: the same as for one observation of the mean, 2 Phi(sqrt(n) |d| / 2) - 1."""
    return tv_normal(math.sqrt(n) * d)


# ------------------------------------------------------------------------------------------------ Le Cam


def bump(x, x0: float, w: float) -> np.ndarray:
    """A smooth bump of width w at x0, peak 1: exp(1 - 1/(1 - u^2)) on |u| < 1, u = (x - x0)/w."""
    u = (np.asarray(x, float) - x0) / w
    out = np.zeros_like(u)
    m = np.abs(u) < 1
    out[m] = np.exp(1 - 1 / (1 - u[m] ** 2))
    return out


def lecam_density_point(n: int, s: float = 2.0, L: float = 1.0) -> dict:
    """Le Cam's two-point bound for estimating f(x0) over a Hoelder-s ball: f0 = U(0,1) and f1 = f0 + h b((x - x0)/w)
    - h b((x - x1)/w) (mass preserved), with h = L w^s (so f1 stays in the ball).  The squared-error risk is at least
    (h/2)^2 (1 - TV(f0^n, f1^n))/2; TV is bounded via Hellinger, n H^2 <= n chi^2.  Optimize over w."""
    from scipy import integrate

    best = {"bound": 0.0}
    c2 = integrate.quad(lambda u: bump(np.array([u]), 0.0, 1.0)[0] ** 2, -1, 1)[0]  # int b^2
    for w in np.logspace(-3, -0.4, 400):
        h = L * w ** s
        chi2 = 2 * h ** 2 * w * c2  # two bumps, f0 = 1
        H2 = min(chi2, 2.0)
        tv = min(1.0, math.sqrt(n * H2))  # TV(P^n, Q^n) <= sqrt(n chi^2)-type bound (Le Cam)
        b = (h / 2) ** 2 * (1 - tv) / 2
        if b > best["bound"]:
            best = {"bound": b, "w": w, "h": h, "tv": tv}
    best["rate"] = n ** (-2 * s / (2 * s + 1))
    return best


# ------------------------------------------------------------------------------------------------- Fano


def varshamov_gilbert(d: int, rng: np.random.Generator, trials: int = 4000) -> dict:
    """A greedy random packing of {0,1}^d with pairwise Hamming distance >= d/8 (Varshamov-Gilbert guarantees
    at least 2^(d/8) such points)."""
    pts = []
    for _ in range(trials):
        v = rng.integers(0, 2, d)
        if all(np.sum(v != p) >= d / 8 for p in pts):
            pts.append(v)
    return {"M": len(pts), "guarantee": 2 ** (d / 8), "pts": np.array(pts)}


def fano_bound(M: int, max_kl: float, delta: float) -> float:
    """Fano: if hypotheses are 2 delta apart and every KL to a centre is <= max_kl, the minimax risk is at least
    delta^2 (1 - (max_kl + log 2)/log M) (squared loss, up to the usual constants)."""
    return float(delta ** 2 * max(0.0, 1 - (max_kl + math.log(2)) / math.log(M)))


def sparse_means_rate(n: int, p: int, s: int, sigma: float = 1.0) -> float:
    """The minimax rate for s-sparse means in R^p from n observations: sigma^2 s log(e p/s) / n."""
    return sigma ** 2 * s * math.log(math.e * p / s) / n


def assouad_holder(n: int, s: float = 1.0, L: float = 1.0) -> dict:
    """Assouad's lemma for regression y = f(x) + N(0,1), x on a grid of n points in [0,1], f in a Hoelder-s ball:
    m bumps of width 1/m and height L (1/m)^s; each coordinate pair has KL = n h^2 int b^2 / m / 2.  The integrated
    squared risk is at least (m/2) (h^2 int b^2/m) (1 - TV) per... optimized over m."""
    from scipy import integrate

    c2 = integrate.quad(lambda u: bump(np.array([u]), 0.0, 1.0)[0] ** 2, -1, 1)[0] / 2  # int over the half-width-1/2 cell
    best = {"bound": 0.0}
    for m in range(1, 400):
        h = L * (1 / (2 * m)) ** s
        sep = h ** 2 * c2 / m  # squared L2 distance contributed by one bump
        kl = n * sep / 2
        tv = min(1.0, math.sqrt(kl / 2))
        b = m / 2 * sep * (1 - tv)
        if b > best["bound"]:
            best = {"bound": b, "m": m, "h": h}
    best["rate"] = n ** (-2 * s / (2 * s + 1))
    return best


# ------------------------------------------------------------------------------------------------ Lepski


def white_noise_kernel(f, x0: float, h: float, n: int, rng: np.random.Generator, reps: int = 1, grid: int = 4000):
    """The local-average estimate of f(x0) with a box kernel of half-width h in y_i = f(i/n) + N(0, 1): mean of the
    y_i with |x_i - x0| <= h.  Returns (estimates, the number of points used)."""
    x = np.arange(1, n + 1) / n
    m = np.abs(x - x0) <= h
    k = int(m.sum())
    fx = f(x[m])
    e = rng.standard_normal((reps, k))
    return (fx[None, :] + e).mean(axis=1), k


def lepski(ests: np.ndarray, sds: np.ndarray, kappa: float = 2.2) -> int:
    """Lepski's method: bandwidths ordered from smallest (largest SD) to largest.  Choose the largest index j such that
    |est_j - est_i| <= kappa sd_i for every smaller index i (the estimates at smaller bandwidths all agree)."""
    J = len(ests)
    chosen = 0
    for j in range(J):
        ok = all(abs(ests[j] - ests[i]) <= kappa * sds[i] for i in range(j))
        if ok:
            chosen = j
        else:
            break
    return chosen


# ------------------------------------------------------------------------------------------ detection, HC


def detection_boundary(beta: float) -> float:
    """Ingster (1997); Donoho & Jin (2004): rho*(beta) = beta - 1/2 on (1/2, 3/4], (1 - sqrt(1 - beta))^2 on (3/4, 1)."""
    if beta <= 0.5:
        return 0.0
    if beta <= 0.75:
        return beta - 0.5
    return (1 - math.sqrt(1 - beta)) ** 2


def higher_criticism(x, alpha0: float = 0.5) -> float:
    """Donoho & Jin's HC*: max over the smallest alpha0 n one-sided p-values of sqrt(n)(i/n - p_(i))/sqrt(p_(i)(1-p_(i)))
    (restricted to p_(i) >= 1/n)."""
    x = np.atleast_2d(np.asarray(x, float))
    n = x.shape[1]
    p = np.sort(stats.norm.sf(x), axis=1)
    i = np.arange(1, n + 1) / n
    hc = math.sqrt(n) * (i[None, :] - p) / np.sqrt(p * (1 - p))
    k = max(1, int(alpha0 * n))
    hc = np.where(p >= 1 / n, hc, -np.inf)[:, :k]
    return np.max(hc, axis=1)


def sparse_mixture(n: int, beta: float, r: float, rng: np.random.Generator, reps: int = 1) -> np.ndarray:
    """X ~ (1 - eps) N(0,1) + eps N(mu, 1), eps = n^-beta, mu = sqrt(2 r log n)."""
    eps = n ** (-beta)
    mu = math.sqrt(2 * r * math.log(n))
    z = rng.standard_normal((reps, n))
    return z + mu * (rng.random((reps, n)) < eps)


# -------------------------------------------------------------------------------------------- planted clique


def planted_clique(n: int, k: int, rng: np.random.Generator) -> np.ndarray:
    A = np.triu(rng.random((n, n)) < 0.5, 1)
    if k > 0:
        S = rng.choice(n, k, replace=False)
        A[np.ix_(S, S)] = True
        A = np.triu(A, 1)
    return A | A.T


def degree_stat(A) -> float:
    """The total-edge count, standardized under G(n, 1/2): (|E| - N/2)/sqrt(N/4), N = n(n-1)/2."""
    n = A.shape[0]
    N = n * (n - 1) / 2
    E = A.sum() / 2
    return float((E - N / 2) / math.sqrt(N / 4))


def max_degree_stat(A) -> float:
    n = A.shape[0]
    d = A.sum(axis=1)
    return float((d.max() - (n - 1) / 2) / math.sqrt((n - 1) / 4))
