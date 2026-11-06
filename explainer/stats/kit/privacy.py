"""statkit.privacy: differential privacy and fairness (Part 63 of *Statistics, Built*).

    mechanisms: Laplace, Gaussian (classical and analytic calibration), randomized response
    accounting: basic and advanced composition, Renyi DP and zCDP for the Gaussian mechanism, conversions to (eps, delta)
    DP as hypothesis testing: trade-off curves of Laplace and Gaussian mechanisms, mu-GDP    (Dong, Roth & Su 2022)
    private inference: a noisy proportion with naive and noise-aware intervals
    the cost of privacy: central Laplace against local randomized response for a mean     (Duchi, Jordan & Wainwright 2013)
    post-processing: nonnegative, total-preserving projection of noisy counts (a TopDown toy)  (Abowd et al. 2022)
    DP gradient descent for logistic regression, with per-example clipping and zCDP accounting   (Abadi et al. 2016)
    membership inference as a likelihood-ratio test against a Gaussian-mechanism release
    fairness: group error rates, calibration by group, Chouldechova's identity, multicalibration (Hebert-Johnson et al. 2018)
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats

# ------------------------------------------------------------------------------------------------- mechanisms


def laplace_mech(value, sensitivity: float, eps: float, rng: np.random.Generator):
    return np.asarray(value, float) + rng.laplace(0, sensitivity / eps, np.shape(value))


def gaussian_sigma_classic(sensitivity: float, eps: float, delta: float) -> float:
    """Dwork & Roth's sufficient noise for (eps, delta)-DP, eps < 1: sigma = sqrt(2 log(1.25/delta)) Delta / eps."""
    return math.sqrt(2 * math.log(1.25 / delta)) * sensitivity / eps


def gaussian_delta(sigma: float, sensitivity: float, eps: float) -> float:
    """The exact delta of the Gaussian mechanism at eps (Balle & Wang 2018):
    Phi(D/(2s) - eps s/D) - e^eps Phi(-D/(2s) - eps s/D)."""
    a = sensitivity / (2 * sigma)
    b = eps * sigma / sensitivity
    return float(stats.norm.cdf(a - b) - math.exp(eps) * stats.norm.cdf(-a - b))


def gaussian_sigma_analytic(sensitivity: float, eps: float, delta: float) -> float:
    """The smallest sigma whose exact delta at eps is at most delta (the analytic Gaussian mechanism)."""
    return float(optimize.brentq(lambda s: gaussian_delta(s, sensitivity, eps) - delta, 1e-6 * sensitivity, 1e6 * sensitivity))


def randomized_response(bits, eps: float, rng: np.random.Generator) -> np.ndarray:
    """Warner's randomized response: report the true bit with probability e^eps / (1 + e^eps), else its flip."""
    bits = np.asarray(bits, int)
    keep = rng.random(len(bits)) < math.exp(eps) / (1 + math.exp(eps))
    return np.where(keep, bits, 1 - bits)


def rr_debias(reports, eps: float) -> float:
    """The unbiased estimate of the true proportion from randomized-response reports."""
    p = math.exp(eps) / (1 + math.exp(eps))
    return float((np.mean(reports) - (1 - p)) / (2 * p - 1))


# ------------------------------------------------------------------------------------------------- accounting


def basic_composition(eps: float, k: int, delta: float = 0.0) -> tuple:
    return k * eps, k * delta


def advanced_composition(eps: float, k: int, delta_slack: float, delta: float = 0.0) -> tuple:
    """Dwork, Rothblum & Vadhan: k-fold composition of (eps, delta) is (eps', k delta + delta_slack) with
    eps' = sqrt(2k log(1/delta_slack)) eps + k eps (e^eps - 1)."""
    e = math.sqrt(2 * k * math.log(1 / delta_slack)) * eps + k * eps * (math.exp(eps) - 1)
    return e, k * delta + delta_slack


def zcdp_gaussian(sensitivity: float, sigma: float) -> float:
    """rho of the Gaussian mechanism in zero-concentrated DP (Bun & Steinke 2016): Delta^2 / (2 sigma^2)."""
    return sensitivity ** 2 / (2 * sigma ** 2)


def zcdp_to_dp(rho: float, delta: float) -> float:
    """rho-zCDP implies (rho + 2 sqrt(rho log(1/delta)), delta)-DP."""
    return rho + 2 * math.sqrt(rho * math.log(1 / delta))


def rdp_gaussian_eps(sensitivity: float, sigma: float, k: int, delta: float, alphas=None) -> float:
    """Renyi DP accounting (Mironov 2017) for k Gaussian mechanisms: RDP(alpha) = k alpha Delta^2 / (2 sigma^2), and
    eps = min over alpha of RDP(alpha) + log(1/delta)/(alpha - 1)."""
    alphas = np.linspace(1.01, 512, 20000) if alphas is None else np.asarray(alphas, float)
    r = k * alphas * sensitivity ** 2 / (2 * sigma ** 2)
    return float(np.min(r + math.log(1 / delta) / (alphas - 1)))


# ----------------------------------------------------------------------------------------- hypothesis testing


def tradeoff_gaussian(alpha, mu: float) -> np.ndarray:
    """The trade-off curve of mu-GDP: the smallest type II error at type I error alpha, Phi(Phi^{-1}(1 - alpha) - mu)."""
    a = np.clip(np.asarray(alpha, float), 1e-12, 1 - 1e-12)
    return stats.norm.cdf(stats.norm.ppf(1 - a) - mu)


def tradeoff_eps_delta(alpha, eps: float, delta: float = 0.0) -> np.ndarray:
    """The trade-off curve of (eps, delta)-DP (Wasserman & Zhou; Kairouz et al.):
    max(0, 1 - delta - e^eps alpha, e^{-eps}(1 - delta - alpha))."""
    a = np.asarray(alpha, float)
    return np.maximum.reduce([np.zeros_like(a), 1 - delta - math.exp(eps) * a, math.exp(-eps) * (1 - delta - a)])


def tradeoff_laplace(alpha, eps: float) -> np.ndarray:
    """The exact trade-off curve of the Laplace mechanism with sensitivity 1 and scale 1/eps (two neighbouring
    values 0 and 1): the Neyman-Pearson tests threshold the output."""
    a = np.clip(np.asarray(alpha, float), 1e-12, 1 - 1e-12)
    b = 1 / eps
    # under H0 the output is Laplace(0, b); under H1 Laplace(1, b); reject for large values: threshold t with P0(X > t) = a
    t = np.where(a < 0.5, -b * np.log(2 * a), b * np.log(2 * (1 - a)))
    return np.where(t >= 1, 1 - 0.5 * np.exp(-(t - 1) / b), 0.5 * np.exp((t - 1) / b))


def gdp_mu_gaussian(sensitivity: float, sigma: float) -> float:
    return sensitivity / sigma


# ---------------------------------------------------------------------------------------- private inference


def private_proportion(x, eps: float, rng: np.random.Generator, alpha: float = 0.05) -> dict:
    """Release a count of a binary attribute with Laplace noise (sensitivity 1), and form two intervals for the
    proportion: the naive Wald interval that treats the noisy proportion as exact data, and the noise-aware one that
    adds the Laplace variance 2 b^2 / n^2."""
    x = np.asarray(x, int)
    n = len(x)
    b = 1 / eps
    noisy = x.sum() + rng.laplace(0, b)
    p = min(max(noisy / n, 0.0), 1.0)
    z = stats.norm.ppf(1 - alpha / 2)
    se_naive = math.sqrt(max(p * (1 - p), 1e-12) / n)
    se_aware = math.sqrt(max(p * (1 - p), 1e-12) / n + 2 * b * b / (n * n))
    return {"p": p, "naive": (p - z * se_naive, p + z * se_naive), "aware": (p - z * se_aware, p + z * se_aware)}


def mean_mse_central_local(n: int, eps: float, reps: int, rng: np.random.Generator, p: float = 0.3) -> dict:
    """The mean of n bits under central DP (Laplace on the sum) and local DP (randomized response per person):
    the central error is p(1-p)/n + 2/(n eps)^2, the local roughly p(1-p)/n + e^eps/(n (e^eps - 1)^2)."""
    ec, el = [], []
    for _ in range(reps):
        x = (rng.random(n) < p).astype(int)
        ec.append((x.sum() + rng.laplace(0, 1 / eps)) / n - p)
        el.append(rr_debias(randomized_response(x, eps, rng), eps) - p)
    return {"central": float(np.mean(np.square(ec))), "local": float(np.mean(np.square(el)))}


# ------------------------------------------------------------------------------------------- post-processing


def nonneg_total_projection(noisy, total: float) -> np.ndarray:
    """The least-squares projection of noisy counts onto {c >= 0, sum c = total}: c_i = max(noisy_i - lam, 0) with lam
    chosen so the sum matches (a water-filling), as in the TopDown algorithm's nonnegativity post-processing."""
    v = np.asarray(noisy, float)
    lo, hi = v.min() - total - 1, v.max() + 1
    for _ in range(200):
        lam = (lo + hi) / 2
        s = np.maximum(v - lam, 0).sum()
        if s > total:
            lo = lam
        else:
            hi = lam
    return np.maximum(v - (lo + hi) / 2, 0)


# ------------------------------------------------------------------------------------------------- DP-SGD


def dp_logistic_gd(X, y, rho: float, steps: int, clip: float, lr: float, rng: np.random.Generator, ridge: float = 1e-3) -> dict:
    """Noisy full-batch gradient descent for logistic regression: clip each example's gradient to norm ``clip``,
    sum, add Gaussian noise, and divide by n.  With the sum's sensitivity ``clip``, each step with noise sigma is
    clip^2/(2 sigma^2)-zCDP; splitting the budget rho over the steps gives sigma = clip sqrt(steps / (2 rho)).
    rho = inf gives the non-private, clipped gradient descent."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, d = X.shape
    w = np.zeros(d)
    sigma = 0.0 if not math.isfinite(rho) else clip * math.sqrt(steps / (2 * rho))
    for _ in range(steps):
        p = 1 / (1 + np.exp(-X @ w))
        G = (p - y)[:, None] * X
        norms = np.maximum(np.linalg.norm(G, axis=1) / clip, 1.0)
        g = (G / norms[:, None]).sum(0) + sigma * rng.standard_normal(d)
        w -= lr * (g / n + ridge * w)
    return {"w": w, "sigma": sigma}


# ----------------------------------------------------------------------------------------- membership inference


def membership_attack_roc(n: int, sigma: float, reps: int, rng: np.random.Generator, grid=None) -> dict:
    """Release the mean of n values in [0, 1] plus Gaussian noise; the attacker tests whether the target's value 1
    was included (H1) or replaced by 0 (H0).  The release shifts by 1/n, so the best test is a threshold and its
    trade-off curve is mu-GDP with mu = (1/n)/sigma.  Returns the empirical ROC from simulated releases."""
    base = rng.random((reps, n - 1)).sum(1)
    r0 = (base + 0.0) / n + sigma * rng.standard_normal(reps)
    r1 = (base + 1.0) / n + sigma * rng.standard_normal(reps)
    # the attacker knows the other n - 1 values: centre each release by them (the worst case for privacy)
    s0, s1 = r0 - base / n, r1 - base / n
    grid = np.linspace(-4 * sigma, 1 / n + 4 * sigma, 200) if grid is None else grid
    fpr = np.array([np.mean(s0 > t) for t in grid])
    tpr = np.array([np.mean(s1 > t) for t in grid])
    return {"fpr": fpr, "tpr": tpr, "mu": (1 / n) / sigma}


# ------------------------------------------------------------------------------------------------- fairness


def group_rates(score, y, group, threshold) -> dict:
    """For each group: the fraction labelled high risk, the false positive rate (high among y = 0), the false
    negative rate (low among y = 1), the positive predictive value, and the base rate."""
    score, y, group = np.asarray(score, float), np.asarray(y, int), np.asarray(group)
    out = {}
    for g in np.unique(group):
        m = group == g
        hi = score[m] >= threshold
        yy = y[m]
        out[str(g)] = {"n": int(m.sum()), "base": float(yy.mean()), "high": float(hi.mean()),
                       "fpr": float(hi[yy == 0].mean()), "fnr": float((~hi)[yy == 1].mean()),
                       "ppv": float(yy[hi].mean()) if hi.any() else float("nan")}
    return out


def calibration_by_group(score, y, group, bins) -> dict:
    """The observed outcome rate within each score bin, by group."""
    score, y, group = np.asarray(score, float), np.asarray(y, int), np.asarray(group)
    out = {}
    for g in np.unique(group):
        m = group == g
        rates, counts = [], []
        for lo, hi in zip(bins[:-1], bins[1:]):
            k = m & (score >= lo) & (score < hi)
            rates.append(float(y[k].mean()) if k.any() else float("nan"))
            counts.append(int(k.sum()))
        out[str(g)] = {"rate": rates, "n": counts}
    return out


def chouldechova_fpr(base: float, ppv: float, fnr: float) -> float:
    """Chouldechova's (2017) identity: FPR = p/(1 - p) (1 - PPV)/PPV (1 - FNR)."""
    return base / (1 - base) * (1 - ppv) / ppv * (1 - fnr)


def multicalibrate(pred, y, groups, alpha: float = 0.01, n_bins: int = 10, max_iter: int = 500, min_n: int = 30) -> dict:
    """Hebert-Johnson, Kim, Reingold & Rothblum's (2018) multicalibration by iterative patching: while some
    (group, prediction-bin) cell has |mean(y - pred)| > alpha and at least ``min_n`` members, shift that cell's
    predictions by its mean residual.  ``groups`` is a list of boolean masks.  Returns the patched predictions, the
    history of the largest violation, and the patches, (group index, bin, shift), to replay on new data."""
    f = np.clip(np.asarray(pred, float).copy(), 0, 1)
    y = np.asarray(y, float)
    hist, patches = [], []
    for _ in range(max_iter):
        bins = np.minimum((f * n_bins).astype(int), n_bins - 1)
        worst, cell = 0.0, None
        for gi, g in enumerate(groups):
            for b in range(n_bins):
                m = g & (bins == b)
                if m.sum() < min_n:
                    continue
                r = float(np.mean(y[m] - f[m]))
                if abs(r) > abs(worst):
                    worst, cell = r, (gi, b)
        hist.append(abs(worst))
        if abs(worst) <= alpha or cell is None:
            break
        m = groups[cell[0]] & (bins == cell[1])
        f[m] = np.clip(f[m] + worst, 0, 1)
        patches.append((cell[0], cell[1], worst))
    return {"pred": f, "history": hist, "patches": patches}


def apply_patches(pred, groups, patches, n_bins: int = 10) -> np.ndarray:
    """Replay multicalibration patches on new data, in order."""
    f = np.clip(np.asarray(pred, float).copy(), 0, 1)
    for gi, b, shift in patches:
        bins = np.minimum((f * n_bins).astype(int), n_bins - 1)
        m = groups[gi] & (bins == b)
        f[m] = np.clip(f[m] + shift, 0, 1)
    return f


def max_calibration_gap(pred, y, groups, n_bins: int = 10, min_n: int = 30) -> float:
    pred, y = np.asarray(pred, float), np.asarray(y, float)
    bins = np.minimum((pred * n_bins).astype(int), n_bins - 1)
    worst = 0.0
    for g in groups:
        for b in range(n_bins):
            m = g & (bins == b)
            if m.sum() >= min_n:
                worst = max(worst, abs(float(np.mean(y[m] - pred[m]))))
    return worst


def weighted_calibration_gap(pred, y, groups, n_bins: int = 5, min_n: int = 100) -> float:
    """The size-weighted mean |mean(y - pred)| over (group, bin) cells with at least ``min_n`` members."""
    pred, y = np.asarray(pred, float), np.asarray(y, float)
    bins = np.minimum((pred * n_bins).astype(int), n_bins - 1)
    tot = w = 0.0
    for g in groups:
        for b in range(n_bins):
            m = g & (bins == b)
            if m.sum() >= min_n:
                tot += m.sum() * abs(float(np.mean(y[m] - pred[m])))
                w += m.sum()
    return tot / w if w else float("nan")
