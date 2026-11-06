"""statkit.decision -- the risk-set explorer (Part 45 of *Statistics, Built*, "The Theory of Estimation").

* **Decision theory (Wald 1950):** every non-randomized rule of a finite problem (two states, finitely many outcomes
  and actions), its risk point, the convex risk set of the randomized rules, the lower boundary, Bayes rules as
  supporting lines, and the minimax rule with its least favourable prior from a linear programme.
* **Exact risk functions:** binomial proportions (the MLE, Beta posterior means, the constant-risk minimax rule);
  the scale family c * sum (x - xbar)^2; the absurd unbiased estimator (-1)^X of e^{-2 lambda}.
* **Exponential families as convex duality:** the cumulant A(eta), the mean map A'(eta), the Fisher information
  A''(eta) and the Legendre conjugate A*(mu) for the Bernoulli, Poisson and normal families.
* **Sufficiency:** the tank problem's estimators with exact variances (a single serial, the moment estimator, the
  Rao-Blackwellized UMVUE), and the exact law of the maximum.
* **Ancillarity:** Cox's (1958) two instruments; a uniform location family's conditional interval given the range.
* **Information inequalities:** Cramer-Rao, Bhattacharyya and Chapman-Robbins bounds against exact variances.
* **Equivariance:** the Pitman estimator of location by numerical integration.
* **Normal means:** James-Stein's exact risk from the Poisson mixture of noncentral chi-squares; Baranchik's family;
  Strawderman's proper Bayes minimax estimator; Brown's recurrence integrals and Brownian hitting probabilities.
* **Empirical Bayes:** Robbins's formula, the gamma-Poisson (negative binomial) fit and the Poisson NPMLE.

Tested in ``tests/test_stats_kit_decision.py``.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy import integrate, optimize, special, stats


# ---------------------------------------------------------------------------------------------------------------
# A finite decision problem
# ---------------------------------------------------------------------------------------------------------------
def risk_points(px, loss) -> dict:
    """All non-randomized rules for a problem with states theta_j (rows of px), outcomes x (columns of px) and actions
    a (columns of loss[j, a]).  Returns the rules (tuples: the action for each outcome) and their risk points
    R(theta_j, delta) = sum_x p(x | theta_j) L(theta_j, delta(x))."""
    px, loss = np.asarray(px, float), np.asarray(loss, float)
    nx, na = px.shape[1], loss.shape[1]
    rules = list(itertools.product(range(na), repeat=nx))
    R = np.array([[np.sum(px[j] * loss[j, list(r)]) for j in range(px.shape[0])] for r in rules])
    return {"rules": rules, "R": R}


def _cross(u, v) -> float:
    return float(u[0] * v[1] - u[1] * v[0])


def lower_boundary(R) -> np.ndarray:
    """The lower-left boundary of the convex hull of two-dimensional risk points (the admissible randomized rules),
    from the point with the smallest R_1 to the point with the smallest R_2, as hull vertices."""
    P = np.unique(np.round(np.asarray(R, float), 12), axis=0)
    P = P[np.lexsort((P[:, 1], P[:, 0]))]
    hull = []
    for p in P:  # the lower convex chain by Andrew's monotone chain
        while len(hull) >= 2 and _cross(hull[-1] - hull[-2], p - hull[-2]) <= 0:
            hull.pop()
        hull.append(p)
    H = np.array(hull)
    k = int(np.argmin(H[:, 1]))  # stop where R_2 is smallest
    return H[: k + 1]


def bayes_rule(R, prior) -> dict:
    """The Bayes rule for prior (pi, 1 - pi) on two states: the risk point minimizing pi R_1 + (1 - pi) R_2."""
    R = np.asarray(R, float)
    w = np.array([prior, 1 - prior])
    r = R @ w
    i = int(np.argmin(r))
    return {"index": i, "point": R[i], "bayes_risk": float(r[i])}


def minimax(R) -> dict:
    """The minimax randomized rule over the risk points by linear programming: minimize t subject to sum_k w_k R_jk
    <= t for each state, w in the simplex.  The dual variables are the least favourable prior."""
    R = np.asarray(R, float)
    K, J = R.shape
    c = np.r_[np.zeros(K), 1.0]
    A_ub = np.c_[R.T, -np.ones(J)]
    A_eq = np.r_[np.ones(K), 0.0][None, :]
    res = optimize.linprog(c, A_ub=A_ub, b_ub=np.zeros(J), A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * K + [(None, None)],
                           method="highs")
    w = res.x[:K]
    lf = -np.asarray(res.ineqlin.marginals)
    lf = lf / lf.sum()
    return {"value": float(res.x[-1]), "weights": w, "point": w @ R, "least_favourable": lf}


# ---------------------------------------------------------------------------------------------------------------
# Exact risk functions
# ---------------------------------------------------------------------------------------------------------------
def binomial_mse(n: int, p, a: float = 0.0, b: float = 0.0) -> np.ndarray:
    """Mean squared error of (X + a) / (n + a + b) for X ~ Bin(n, p): [n p (1 - p) + (a - (a + b) p)^2] / (n + a + b)^2.
    a = b = 0 is the MLE; a = b = sqrt(n)/2 is the minimax rule, with constant risk 1 / (4 (1 + sqrt n)^2)."""
    p = np.asarray(p, float)
    return (n * p * (1 - p) + (a - (a + b) * p) ** 2) / (n + a + b) ** 2


def binomial_bayes_risk(n: int, a: float, b: float, prior_a: float = 1.0, prior_b: float = 1.0) -> float:
    """Average of binomial_mse(n, p, a, b) over p ~ Beta(prior_a, prior_b), exactly (Beta moments)."""
    m1 = prior_a / (prior_a + prior_b)
    m2 = prior_a * (prior_a + 1) / ((prior_a + prior_b) * (prior_a + prior_b + 1))
    num = n * (m1 - m2) + a ** 2 - 2 * a * (a + b) * m1 + (a + b) ** 2 * m2
    return float(num / (n + a + b) ** 2)


def scale_mse(n: int, c) -> np.ndarray:
    """MSE / sigma^4 of c * sum (x_i - xbar)^2 for sigma^2 from n normal observations: the sum is sigma^2 chi^2_{n-1}, so
    MSE = c^2 (n - 1)(n + 1) - 2 c (n - 1) + 1, minimized at c = 1 / (n + 1)."""
    c = np.asarray(c, float)
    return c ** 2 * (n - 1) * (n + 1) - 2 * c * (n - 1) + 1


def absurd_umvue(lam) -> dict:
    """X ~ Poisson(lambda), estimating e^{-2 lambda}.  The only unbiased estimator is (-1)^X (MSE 1 - e^{-4 lambda});
    the MLE e^{-2X} and the truncation 1(X even) (which dominates it) have exact MSEs from the Poisson PGF."""
    lam = np.asarray(lam, float)
    g = np.exp(-2 * lam)
    pgf = lambda t: np.exp(lam * (np.exp(-t) - 1))  # noqa: E731  E e^{-tX}
    mse_u = 1 - np.exp(-4 * lam)
    mse_mle = pgf(4.0) - 2 * g * pgf(2.0) + g ** 2
    pe = (1 + np.exp(-2 * lam)) / 2
    mse_even = pe * (1 - 2 * g) + g ** 2
    return {"target": g, "umvue": mse_u, "mle": mse_mle, "even": mse_even}


# ---------------------------------------------------------------------------------------------------------------
# Exponential families as convex duality
# ---------------------------------------------------------------------------------------------------------------
def expfam(name: str, eta) -> dict:
    """Cumulant A(eta), mean A'(eta), variance A''(eta) and the conjugate A*(mu) = sup_eta (eta mu - A(eta)) at mu =
    A'(eta), for 'bernoulli', 'poisson' or 'normal' (unit variance)."""
    eta = np.asarray(eta, float)
    if name == "bernoulli":
        A = np.logaddexp(0, eta)
        mu = special.expit(eta)
        V = mu * (1 - mu)
        Astar = special.xlogy(mu, mu) + special.xlogy(1 - mu, 1 - mu)
    elif name == "poisson":
        A = np.exp(eta)
        mu = A
        V = A
        Astar = mu * np.log(mu) - mu
    elif name == "normal":
        A = eta ** 2 / 2
        mu = eta
        V = np.ones_like(eta)
        Astar = mu ** 2 / 2
    else:
        raise ValueError(name)
    return {"A": A, "mu": mu, "V": V, "Astar": Astar}


def legendre(A, eta_grid, mu) -> np.ndarray:
    """A*(mu) = sup_eta (eta mu - A(eta)) numerically over a grid (for checking the closed forms)."""
    eta_grid = np.asarray(eta_grid, float)
    Ag = A(eta_grid)
    return np.max(np.asarray(mu, float)[:, None] * eta_grid[None, :] - Ag[None, :], axis=1)


# ---------------------------------------------------------------------------------------------------------------
# Sufficiency: the tank problem
# ---------------------------------------------------------------------------------------------------------------
def tank_max_pmf(N: int, k: int) -> tuple:
    """P(M = m) = C(m - 1, k - 1) / C(N, k) for the largest of k serials drawn without replacement from 1..N."""
    m = np.arange(k, N + 1)
    logp = special.gammaln(m) - special.gammaln(k) - special.gammaln(m - k + 1) - (
        special.gammaln(N + 1) - special.gammaln(k + 1) - special.gammaln(N - k + 1))
    return m, np.exp(logp)


def tank_estimators(N: int, k: int) -> dict:
    """Exact standard deviations of three unbiased estimators of N from k serials without replacement:
    2 X_1 - 1 (one serial), 2 Xbar - 1 (the moment estimator) and M (k + 1)/k - 1 (its Rao-Blackwellization, the UMVUE),
    with the UMVUE's SD computed both by the formula and from the exact law of M."""
    s2 = (N ** 2 - 1) / 12  # variance of one serial
    sd_one = 2 * math.sqrt(s2)
    sd_mom = 2 * math.sqrt(s2 / k * (N - k) / (N - 1))
    sd_umvue = math.sqrt((N - k) * (N + 1) / (k * (k + 2)))
    m, p = tank_max_pmf(N, k)
    est = m * (k + 1) / k - 1
    mean = float(np.sum(p * est))
    sd_exact = float(np.sqrt(np.sum(p * (est - mean) ** 2)))
    return {"one": sd_one, "mom": sd_mom, "umvue": sd_umvue, "umvue_exact": sd_exact, "umvue_mean": mean}


def rao_blackwell_one(m: int, k: int) -> float:
    """E[2 X_1 - 1 | M = m]: given the maximum, X_1 is m with probability 1/k and otherwise uniform on 1..m-1, so the
    conditional mean is 2 [m/k + (1 - 1/k) m/2] - 1 = m (k + 1)/k - 1, the UMVUE."""
    e = m / k + (1 - 1 / k) * m / 2
    return 2 * e - 1


# ---------------------------------------------------------------------------------------------------------------
# Ancillarity
# ---------------------------------------------------------------------------------------------------------------
def cox_instruments(s_precise: float = 1.0, s_rough: float = 10.0, level: float = 0.9) -> dict:
    """Cox (1958): a fair coin picks an instrument with SD s_precise or s_rough.  The unconditional interval x +- c
    with average coverage `level`, its conditional coverages, and the conditional intervals' half-widths."""
    f = lambda c: 0.5 * (2 * stats.norm.cdf(c / s_precise) - 1) + 0.5 * (2 * stats.norm.cdf(c / s_rough) - 1) - level  # noqa: E731
    c = optimize.brentq(f, 1e-6, 100 * s_rough)
    z = stats.norm.ppf(0.5 + level / 2)
    return {"c": c, "cover_precise": float(2 * stats.norm.cdf(c / s_precise) - 1),
            "cover_rough": float(2 * stats.norm.cdf(c / s_rough) - 1),
            "half_precise": z * s_precise, "half_rough": z * s_rough, "z": z}


def uniform_location_interval(x, level: float = 0.9) -> tuple:
    """X_i ~ U(theta - 1/2, theta + 1/2).  Given the order statistics, theta is uniform (under a flat prior, and for
    the equivariant interval exactly) on [max - 1/2, min + 1/2]; the conditional interval is its central `level`."""
    x = np.asarray(x, float)
    lo, hi = x.max() - 0.5, x.min() + 0.5
    mid, half = (lo + hi) / 2, level * (hi - lo) / 2
    return mid - half, mid + half


# ---------------------------------------------------------------------------------------------------------------
# Information inequalities
# ---------------------------------------------------------------------------------------------------------------
def bhattacharyya_theta2(theta, n: int) -> dict:
    """Estimating theta^2 from n N(theta, 1) observations: the UMVUE xbar^2 - 1/n has variance 4 theta^2/n + 2/n^2; the
    Cramer-Rao bound is 4 theta^2/n; the second-order Bhattacharyya bound adds g''^2 / J_22 = 4 / (2 n^2) and is
    attained."""
    theta = np.asarray(theta, float)
    return {"var_umvue": 4 * theta ** 2 / n + 2 / n ** 2, "cr": 4 * theta ** 2 / n,
            "bhatt2": 4 * theta ** 2 / n + 4 / (2 * n ** 2)}


def chapman_robbins_uniform(n: int, theta: float = 1.0) -> dict:
    """X_i ~ U(0, theta): no Fisher information exists (the support moves), but the Chapman-Robbins bound
    sup_{t<1} theta^2 (1 - t)^2 / (t^{-n} - 1) holds; against it, the UMVUE (n + 1)/n max has variance
    theta^2 / (n (n + 2))."""
    obj = lambda t: -((1 - t) ** 2 / (t ** (-n) - 1.0))  # noqa: E731
    r = optimize.minimize_scalar(obj, bounds=(1e-9, 1 - 1e-9), method="bounded", options={"xatol": 1e-12})
    return {"bound": float(-r.fun * theta ** 2), "t": float(r.x), "var_umvue": theta ** 2 / (n * (n + 2))}


# ---------------------------------------------------------------------------------------------------------------
# Equivariance
# ---------------------------------------------------------------------------------------------------------------
def pitman_location(x, logf, width: float = 30.0, m: int = 4001) -> float:
    """The Pitman estimator int t prod f(x_i - t) dt / int prod f(x_i - t) dt: the minimum-risk location-equivariant
    estimator under squared error, and the generalized Bayes rule for a flat prior.  A grid centred at the median."""
    x = np.asarray(x, float)
    c = float(np.median(x))
    t = np.linspace(c - width / 2, c + width / 2, m)
    lp = np.sum(logf(x[None, :] - t[:, None]), axis=1)
    w = np.exp(lp - lp.max())
    return float(np.sum(t * w) / np.sum(w))


def pitman_uniform(x) -> float:
    """For U(theta - 1/2, theta + 1/2) the Pitman estimator is the midrange."""
    x = np.asarray(x, float)
    return float((x.max() + x.min()) / 2)


# ---------------------------------------------------------------------------------------------------------------
# Normal means
# ---------------------------------------------------------------------------------------------------------------
def js_risk(p: int, norm2, terms: int = 400) -> np.ndarray:
    """Exact risk of James-Stein (1 - (p - 2)/|x|^2) x for x ~ N_p(theta, I): p - (p - 2)^2 E[1 / (p - 2 + 2K)],
    K ~ Poisson(|theta|^2 / 2) (|x|^2 is a Poisson mixture of central chi-squares with p + 2K degrees of freedom)."""
    lam = np.atleast_1d(np.asarray(norm2, float)) / 2
    k = np.arange(terms)
    w = stats.poisson.pmf(k[None, :], lam[:, None])
    e = np.sum(w / (p - 2 + 2 * k[None, :]), axis=1)
    return p - (p - 2) ** 2 * e


def sure(x, g, h: float = 1e-5) -> float:
    """Stein's unbiased risk estimate for delta(x) = x + g(x) with x ~ N_p(theta, I): p + |g|^2 + 2 div g (by central
    differences)."""
    x = np.asarray(x, float)
    gx = np.asarray(g(x), float)
    div = 0.0
    for i in range(len(x)):
        e = np.zeros_like(x)
        e[i] = h
        div += (g(x + e)[i] - g(x - e)[i]) / (2 * h)
    return float(len(x) + gx @ gx + 2 * div)


def baranchik(x, r) -> np.ndarray:
    """Baranchik's (1970) family (1 - r(|x|^2) (p - 2) / |x|^2) x: minimax for p >= 3 when r is nondecreasing with
    0 <= r <= 2."""
    x = np.asarray(x, float)
    s = np.sum(x ** 2, axis=-1, keepdims=True)
    p = x.shape[-1]
    return (1 - r(s) * (p - 2) / s) * x


def strawderman_shrink(s, p: int, a: float = 0.5) -> np.ndarray:
    """Strawderman's (1971) prior: theta | lam ~ N(0, (1/lam - 1) I), lam having density (1 - a) lam^{-a} on (0, 1].
    The posterior mean is (1 - E[lam | x]) x, with E[lam | x] = int_0^1 lam^{p/2 - a + 1} e^{-lam s/2} /
    int_0^1 lam^{p/2 - a} e^{-lam s/2}, s = |x|^2.  Proper for a < 1; minimax for p >= 5 and 3 - p/2 <= a < 1."""
    s = np.maximum(np.asarray(s, float), 1e-12)
    k = p / 2 - a
    lnum = special.gammaln(k + 2) + np.log(special.gammainc(k + 2, s / 2)) - (k + 2) * np.log(s / 2)
    lden = special.gammaln(k + 1) + np.log(special.gammainc(k + 1, s / 2)) - (k + 1) * np.log(s / 2)
    return np.exp(lnum - lden)


def brown_integral(p: int, R) -> np.ndarray:
    """int_1^R r^{1 - p} dr: Brown's (1971) condition for the flat-prior generalized Bayes rule (x itself) to be
    admissible is that this diverges, which happens exactly when p <= 2, exactly when Brownian motion is recurrent."""
    R = np.asarray(R, float)
    if p == 2:
        return np.log(R)
    return (R ** (2 - p) - 1) / (2 - p)


def bm_hit_ball(p: int, rho: float, R) -> np.ndarray:
    """P(p-dimensional Brownian motion from radius rho hits the unit ball before radius R): log(R/rho)/log R for p = 2,
    (rho^{2-p} - R^{2-p}) / (1 - R^{2-p}) for p >= 3, (R - rho)/(R - 1) for p = 1."""
    R = np.asarray(R, float)
    if p == 1:
        return (R - rho) / (R - 1)
    if p == 2:
        return np.log(R / rho) / np.log(R)
    return (rho ** (2 - p) - R ** (2 - p)) / (1 - R ** (2 - p))


# ---------------------------------------------------------------------------------------------------------------
# Empirical Bayes for Poisson counts
# ---------------------------------------------------------------------------------------------------------------
def robbins(counts) -> np.ndarray:
    """Robbins's (1956) estimate of E(theta | x) = (x + 1) f(x + 1) / f(x) from the frequencies f(0), f(1), ...
    (the last value, with no f(x + 1), is nan)."""
    f = np.asarray(counts, float)
    out = np.full(len(f), np.nan)
    out[:-1] = (np.arange(len(f) - 1) + 1) * f[1:] / f[:-1]
    return out


def gamma_poisson(counts) -> dict:
    """Fit theta ~ Gamma(shape nu, scale s) by maximum likelihood of the negative-binomial marginal; the posterior mean
    is (x + nu) s / (1 + s)."""
    f = np.asarray(counts, float)
    x = np.arange(len(f))

    def nll(par):
        nu, s = np.exp(par)
        lp = special.gammaln(x + nu) - special.gammaln(nu) - special.gammaln(x + 1) + x * np.log(s / (1 + s)) - nu * np.log1p(s)
        return -np.sum(f * lp)

    r = optimize.minimize(nll, [0.0, np.log(max(np.sum(f * x) / f.sum(), 1e-3))], method="Nelder-Mead",
                          options={"xatol": 1e-10, "fatol": 1e-10, "maxiter": 20000})
    nu, s = np.exp(r.x)
    return {"nu": float(nu), "scale": float(s), "post_mean": (x + nu) * s / (1 + s), "loglik": float(-r.fun)}


def poisson_npmle(counts, grid=None, iters: int = 20000, tol: float = 1e-12) -> dict:
    """The Kiefer-Wolfowitz NPMLE of the mixing law g for Poisson counts on a grid, by EM; its posterior means."""
    f = np.asarray(counts, float)
    x = np.arange(len(f))
    grid = np.linspace(1e-3, max(len(f), 2), 400) if grid is None else np.asarray(grid, float)
    L = stats.poisson.pmf(x[:, None], grid[None, :])
    w = np.full(len(grid), 1 / len(grid))
    old = -np.inf
    for _ in range(iters):
        m = L @ w
        w = w * ((f / m) @ L) / f.sum()
        ll = float(np.sum(f * np.log(L @ w)))
        if ll - old < tol:
            break
        old = ll
    m = L @ w
    return {"grid": grid, "w": w, "post_mean": (L * w) @ grid / m, "loglik": ll}
