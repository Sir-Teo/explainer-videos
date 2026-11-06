"""statkit.qual: the PhD problem bank of Part 55 (the qualifying exam).

Each function computes, exactly where it can, the numbers one of the twelve problems needs:

    exponential maxima and Borel-Cantelli sums             (Problem 1, Part 43)
    the simple random walk stopped at +1                   (Problem 2, Part 44)
    the Poisson UMVUE of exp(-lambda)                      (Problem 3, Part 45)
    Blyth's ratio for normal means in d dimensions         (Problem 4, Part 45)
    the conditional test of two Poisson rates              (Problem 5, Part 46)
    local power in the logistic location model             (Problem 6, Part 47)
    brackets for half-lines and the bracketing integral    (Problem 7, Part 48)
    the median's influence function, Wald intervals        (Problem 8, Part 49)
    Fano's bound for sparse normal means                   (Problem 9, Part 50)
    matrix Bernstein for a bounded covariance              (Problem 10, Part 51)
    the lasso's oracle inequality                          (Problem 11, Part 52)
    the posterior's contraction in the sequence model      (Problem 12, Part 53)
"""

from __future__ import annotations

import math

import numpy as np
from scipy import special, stats

# ------------------------------------------------------------------------------------- 1. Borel-Cantelli


def bc_partial_sums(c: float, N: int) -> np.ndarray:
    """Partial sums of P(X_n > c log n) = n^(-c) for X_n ~ Exp(1), n = 2..N: finite iff c > 1."""
    n = np.arange(2, N + 1, dtype=float)
    return np.cumsum(n ** (-c))


def exceedances(x, c: float) -> np.ndarray:
    """Indices n (from 2) at which X_n > c log n."""
    x = np.asarray(x, float)
    n = np.arange(1, len(x) + 1)
    hit = (n >= 2) & (x > c * np.log(np.maximum(n, 2)))
    return n[hit]


def running_max_ratio(x) -> np.ndarray:
    """max_{i <= n} X_i / log n, n >= 2 (the first entry is for n = 2)."""
    m = np.maximum.accumulate(np.asarray(x, float))
    n = np.arange(1, len(m) + 1)
    return (m / np.log(np.maximum(n, 2)))[1:]


# ------------------------------------------------------------------------------- 2. optional stopping


def first_passage(N: int) -> dict:
    """The simple random walk from 0 stopped at T = inf{n: S_n = 1}, computed exactly by dynamic programming up to
    step N: P(T <= m), E[S_m; T > m] (= -P(T <= m), since E S_{T ^ m} = 0) and E[T ^ m]."""
    off = N + 1
    p = np.zeros(2 * N + 3)
    p[off] = 1.0  # mass on {T > m, S_m = k}
    hit = np.zeros(N + 1)
    tail_mean = np.zeros(N + 1)
    e_min = np.zeros(N + 1)
    acc = 0.0
    alive = 1.0
    for m in range(1, N + 1):
        q = np.zeros_like(p)
        q[1:] += 0.5 * p[:-1]
        q[:-1] += 0.5 * p[1:]
        acc += alive  # E[T ^ m] = sum_{j < m} P(T > j)
        hit[m] = hit[m - 1] + q[off + 1]
        q[off + 1] = 0.0
        p = q
        alive = float(p.sum())
        ks = np.arange(len(p)) - off
        tail_mean[m] = float((ks * p).sum())
        e_min[m] = acc
    return {"hit": hit, "tail_mean": tail_mean, "e_min": e_min}


def first_passage_pmf(k: int) -> float:
    """P(T = 2k - 1) = C_{k-1} / 2^(2k-1), C the Catalan numbers."""
    return float(math.exp(special.gammaln(2 * k - 1) - special.gammaln(k) - special.gammaln(k + 1) - (2 * k - 1) * math.log(2)))


def ruin(a: int, b: int) -> dict:
    """The walk from 0 stopped at -a or b: P(hit b) = a/(a + b) and E T = ab (Wald's identities)."""
    return {"p_b": a / (a + b), "ET": a * b}


# ---------------------------------------------------------------------------------------------- 3. UMVUE


def poisson_umvue(n: int, lam: float) -> dict:
    """The UMVUE ((n - 1)/n)^T of exp(-lambda), T = sum X_i ~ Poisson(n lambda): its exact variance
    exp(-2 lambda)(exp(lambda/n) - 1), the Cramer-Rao bound lambda exp(-2 lambda)/n, and the MLE exp(-T/n)'s bias and
    MSE, all by the Poisson generating function."""
    g = math.exp(-lam)
    var_u = math.exp(-2 * lam) * (math.exp(lam / n) - 1)
    crlb = lam * math.exp(-2 * lam) / n
    m1 = math.exp(n * lam * (math.exp(-1 / n) - 1))
    m2 = math.exp(n * lam * (math.exp(-2 / n) - 1))
    return {"target": g, "var_umvue": var_u, "crlb": crlb, "mle_bias": m1 - g, "mle_mse": m2 - 2 * g * m1 + g * g}


def unbiased_poly_degree(n: int) -> int:
    """E_p g(X) for X ~ Bin(n, p) is a polynomial in p of degree <= n; 1/p is not, so no unbiased estimator exists."""
    return n


# ---------------------------------------------------------------------------------------------- 4. Blyth


def blyth_ratio(tau, d: int = 1) -> np.ndarray:
    """Blyth's method for X ~ N(theta, I_d) under squared loss, with the unnormalized priors exp(-|theta|^2 / 2 tau^2):
    the Bayes-risk gap of X over the Bayes rule, times the prior's total mass, divided by its mass near 0 (which tends
    to a constant): (d / (1 + tau^2)) (2 pi tau^2)^(d/2).  It tends to 0 for d = 1 (X admissible) and not for d >= 2."""
    t = np.asarray(tau, float)
    return d / (1 + t ** 2) * (2 * math.pi * t ** 2) ** (d / 2)


# ------------------------------------------------------------------------------------ 5. Neyman structure


def poisson_conditional_test(x: int, y: int, alpha: float = 0.05) -> dict:
    """X ~ Poisson(l1), Y ~ Poisson(l2), test l1 = l2 against l1 != l2.  Given T = X + Y = t, X ~ Bin(t, 1/2) whatever
    the common rate: the UMPU test is the two-sided binomial test in that slice (randomized on its boundary).  Returns
    the conditional two-sided p-value (doubling the smaller tail) and the slice's UMPU test."""
    from explainer.stats.kit.testing import umpu_binomial

    t = x + y
    lo = stats.binom.cdf(x, t, 0.5)
    hi = stats.binom.sf(x - 1, t, 0.5)
    return {"t": t, "p": float(min(1.0, 2 * min(lo, hi))), "umpu": umpu_binomial(t, 0.5, alpha)}


def poisson_conditional_size(lam: float, alpha: float = 0.05, randomized: bool = False, tmax: int | None = None) -> float:
    """The unconditional size of the conditional test of equal Poisson rates at a common rate lam: an average over
    T ~ Poisson(2 lam) of each slice's size.  Exactly alpha when randomized (Neyman structure); below it when not."""
    from explainer.stats.kit.testing import umpu_binomial

    tmax = tmax or int(2 * lam + 12 * math.sqrt(2 * lam + 1) + 10)
    size = 0.0
    for t in range(tmax + 1):
        wt = stats.poisson.pmf(t, 2 * lam)
        if t == 0:
            size += wt * (alpha if randomized else 0.0)
            continue
        if randomized:
            size += wt * alpha
            continue
        xs = np.arange(t + 1)
        f = stats.binom.pmf(xs, t, 0.5)
        pv = np.minimum(1.0, 2 * np.minimum(stats.binom.cdf(xs, t, 0.5), stats.binom.sf(xs - 1, t, 0.5)))
        size += wt * float(f[pv <= alpha].sum())
    return float(size)


# --------------------------------------------------------------------------------------------- 6. LAN


LOGISTIC_INFO = 1.0 / 3.0


def logistic_local_powers(h, alpha: float = 0.05) -> dict:
    """Local power at theta = h / sqrt n in the logistic location model, one-sided level alpha: the score (efficient)
    test with information 1/3, the t-test (variance pi^2 / 3) and the sign test (2 f(0) = 1/2)."""
    h = np.asarray(h, float)
    z = stats.norm.ppf(1 - alpha)
    return {"score": stats.norm.sf(z - h * math.sqrt(LOGISTIC_INFO)), "t": stats.norm.sf(z - h * math.sqrt(3) / math.pi),
            "sign": stats.norm.sf(z - h * 0.5)}


def logistic_local_power_sim(h: float, n: int, rng: np.random.Generator, reps: int = 4000, alpha: float = 0.05) -> dict:
    """Simulated power of the three tests at theta = h / sqrt n, with n logistic observations."""
    z = stats.norm.ppf(1 - alpha)
    X = rng.logistic(h / math.sqrt(n), 1.0, size=(reps, n))
    score = np.tanh(X / 2).sum(axis=1) / math.sqrt(n * LOGISTIC_INFO)
    tt = X.mean(axis=1) / (X.std(axis=1, ddof=1) / math.sqrt(n))
    sg = (np.sign(X).sum(axis=1)) / math.sqrt(n)
    return {"score": float(np.mean(score > z)), "t": float(np.mean(tt > z)), "sign": float(np.mean(sg > z))}


# ------------------------------------------------------------------------------------------ 7. bracketing


def halfline_brackets(eps: float) -> np.ndarray:
    """For P = Uniform[0, 1], the points t_j = j eps^2 giving brackets [1{x <= t_(j-1)}, 1{x <= t_j}] of L2(P) size eps."""
    m = int(math.ceil(1 / eps ** 2))
    return np.minimum(np.arange(m + 1) * eps ** 2, 1.0)


def bracketing_integral(log_n, upper: float = 1.0, grid: int = 20000) -> float:
    """int_0^upper sqrt(log N_[](eps)) d eps, by the midpoint rule (log_n a function of eps)."""
    e = (np.arange(grid) + 0.5) * upper / grid
    return float(np.sum(np.sqrt(np.maximum(0.0, log_n(e)))) * upper / grid)


# -------------------------------------------------------------------------------- 8. the median's influence


def median_if(x, m: float, f_m: float) -> np.ndarray:
    """The influence function of the median: (1/2 - 1{x <= m}) / f(m); its variance is 1 / (4 f(m)^2)."""
    return (0.5 - (np.asarray(x, float) <= m)) / f_m


def median_wald(x, level: float = 0.95) -> dict:
    """A Wald interval for the median with the plug-in variance 1/(4 n f_hat(m)^2), f_hat a Gaussian KDE with
    Silverman's bandwidth."""
    x = np.asarray(x, float)
    n = len(x)
    m = float(np.median(x))
    s = min(np.std(x, ddof=1), (np.quantile(x, 0.75) - np.quantile(x, 0.25)) / 1.349)
    bw = 0.9 * s * n ** (-0.2)
    f = float(np.mean(stats.norm.pdf((m - x) / bw)) / bw)
    se = 1 / (2 * f * math.sqrt(n))
    z = stats.norm.ppf(0.5 + level / 2)
    return {"median": m, "f": f, "se": se, "lo": m - z * se, "hi": m + z * se}


# --------------------------------------------------------------------------------------------- 9. Fano


def sparse_fano(d: int, s: int, n: int, sigma: float = 1.0) -> dict:
    """Fano's lower bound for s-sparse means in R^d from n observations N(theta, sigma^2 I / n).  The sparse
    Varshamov-Gilbert lemma (Rigollet & Huetter, Lemma 4.14; needs s <= d/8) gives M binary vectors with s ones, pairwise
    Hamming distance >= s/2 and log M >= (s/8) log(1 + d/(2s)).  Scaled by delta they are >= delta sqrt(s/2) apart, and
    every KL between them is <= n ||theta - theta'||^2 / (2 sigma^2) <= n s delta^2 / sigma^2.  Fano: the minimax risk is at
    least (s delta^2 / 8)(1 - (n s delta^2 / sigma^2 + log 2)/log M); maximized over delta, (log M - log 2)^2 sigma^2 /
    (32 n log M).  Against the rate sigma^2 s log(e d / s) / n."""
    logM = s / 8 * math.log(1 + d / (2 * s))
    if logM <= math.log(2):
        lower, delta2 = 0.0, 0.0
    else:
        delta2 = sigma ** 2 * (logM - math.log(2)) / (2 * n * s)
        lower = (logM - math.log(2)) ** 2 * sigma ** 2 / (32 * n * logM)
    return {"logM": logM, "delta2": delta2, "kl": n * s * delta2 / sigma ** 2, "lower": lower,
            "rate": sigma ** 2 * s * math.log(math.e * d / s) / n}


def soft_threshold_risk(d: int, s: int, n: int, signal: float, rng: np.random.Generator, reps: int = 400,
                        sigma: float = 1.0) -> float:
    """Simulated risk of soft thresholding at sigma sqrt(2 log(d/s) / n) for an s-sparse mean with entries signal."""
    lam = sigma * math.sqrt(2 * math.log(d / s) / n)
    th = np.zeros(d)
    th[:s] = signal
    Y = th + sigma / math.sqrt(n) * rng.standard_normal((reps, d))
    est = np.sign(Y) * np.maximum(np.abs(Y) - lam, 0)
    return float(np.mean(np.sum((est - th) ** 2, axis=1)))


# ------------------------------------------------------------------------------------- 10. matrix Bernstein


def bounded_covariance_error(n: int, d: int, rng: np.random.Generator, reps: int = 200, delta: float = 0.05) -> dict:
    """x_i with independent Rademacher coordinates scaled to have covariance I_d, ||x||^2 = d: S = (1/n) sum x x^T - I.
    Matrix Bernstein with L = d / n (one summand's norm, since ||x x^T - I|| <= d - 1 < d) and v = (d - 1)/n gives
    P(||S|| >= t) <= 2 d exp(-(t^2/2)/(v + L t/3)); the t making this delta, the expected-norm bound, and the
    simulated mean and coverage of the ball ||S|| <= t."""
    vals = []
    for _ in range(reps):
        X = rng.choice([-1.0, 1.0], size=(n, d))
        S = X.T @ X / n - np.eye(d)
        vals.append(float(np.max(np.abs(np.linalg.eigvalsh(S)))))
    vals = np.asarray(vals)
    v, L = (d - 1) / n, d / n
    c = math.log(2 * d / delta)
    t = (L * c / 3 + math.sqrt((L * c / 3) ** 2 + 2 * v * c))
    mean_bound = math.sqrt(2 * v * math.log(2 * d)) + L * math.log(2 * d) / 3
    return {"mean": float(vals.mean()), "mean_bound": mean_bound, "t": t, "coverage": float(np.mean(vals <= t)),
            "q95": float(np.quantile(vals, 1 - delta)), "vals": vals}


# ------------------------------------------------------------------------------------------- 11. the lasso


def lasso_cd(X, y, lam: float, iters: int = 400, tol: float = 1e-8) -> np.ndarray:
    """(1/2n)||y - X b||^2 + lam ||b||_1 by cyclic coordinate descent (columns of X with squared norm n)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    b = np.zeros(p)
    r = y.copy()
    cn = (X ** 2).sum(axis=0) / n
    for _ in range(iters):
        mx = 0.0
        for j in range(p):
            old = b[j]
            z = X[:, j] @ r / n + cn[j] * old
            new = np.sign(z) * max(abs(z) - lam, 0.0) / cn[j]
            if new != old:
                r -= X[:, j] * (new - old)
                b[j] = new
                mx = max(mx, abs(new - old))
        if mx < tol:
            break
    return b


def lasso_oracle(n: int, p: int, s: int, rng: np.random.Generator, reps: int = 50, sigma: float = 1.0,
                 delta: float = 0.05) -> dict:
    """Gaussian design with unit-variance independent columns, beta with s entries of 1: the lasso at
    lam = 2 sigma sqrt(2 log(2p/delta) / n) (so that the event below has probability about 1 - delta) and its prediction error ||X(b - beta)||^2 / n against the oracle inequality's
    9 s lam^2 / phi^2 (with the compatibility constant phi^2 taken as 1/2), the l1 error against 12 s lam / phi^2,
    and how often the event ||X^T eps / n||_inf <= lam / 2 held."""
    lam = 2 * sigma * math.sqrt(2 * math.log(2 * p / delta) / n)
    pred, l1, event = [], [], []
    for _ in range(reps):
        X = rng.standard_normal((n, p))
        beta = np.zeros(p)
        beta[:s] = 1.0
        eps = sigma * rng.standard_normal(n)
        y = X @ beta + eps
        b = lasso_cd(X, y, lam)
        pred.append(float(np.sum((X @ (b - beta)) ** 2) / n))
        l1.append(float(np.sum(np.abs(b - beta))))
        event.append(bool(np.max(np.abs(X.T @ eps / n)) <= lam / 2))
    phi2 = 0.5
    return {"lam": lam, "pred": float(np.mean(pred)), "pred_bound": 9 * s * lam ** 2 / phi2, "l1": float(np.mean(l1)),
            "l1_bound": 12 * s * lam / phi2, "event": float(np.mean(event)), "ols_pred": sigma ** 2 * p / n if p < n else None}


# ------------------------------------------------------------------------------------ 12. contraction


def sequence_contraction(n: int, alpha: float, beta: float, K: int = 100000) -> dict:
    """Y_k = theta_k + Z_k / sqrt n, prior theta_k ~ N(0, k^(-1-2 alpha)), truth theta_k = k^(-1/2-beta) (in every
    Sobolev ball of smoothness < beta).  The posterior's expected squared distance from the truth, E Pi(||theta -
    theta0||^2 | Y) = bias^2 + variance + posterior spread, computed exactly, and the rate n^(-2 min(alpha, beta)/(1 +
    2 alpha))."""
    k = np.arange(1, K + 1, dtype=float)
    lam = k ** (-1 - 2 * alpha)
    th = k ** (-0.5 - beta)
    w = n * lam / (1 + n * lam)
    b2 = float(np.sum((1 - w) ** 2 * th ** 2))
    v = float(np.sum(w ** 2) / n)
    spread = float(np.sum(lam / (1 + n * lam)))
    return {"bias2": b2, "var": v, "spread": spread, "total": b2 + v + spread,
            "rate2": n ** (-2 * min(alpha, beta) / (1 + 2 * alpha))}
