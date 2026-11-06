"""statkit.slt: statistical learning theory (Part 54 of *Statistics, Built*).

Checked in ``tests/test_stats_kit_slt.py``:

* ERM over thresholds on [0, 1] with label noise: the excess risk and the uniform deviation sup |R_n - R|, against
  VC bounds; realizable and Massart-noise fast rates;
* the VC bound and the Rademacher bound for finite classes and VC classes;
* Rademacher complexity of l2-bounded linear classes and kernel classes, exact by simulation, against B max||x|| /
  sqrt(n) and B sqrt(tr K)/n;
* AdaBoost with decision stumps: training error, test error and the margin distribution (Schapire et al. 1998);
* PAC-Bayes: McAllester's and Catoni's bounds for a Gibbs posterior over a finite class, with the kl inversion;
* uniform stability of ridge regression and its generalization gap;
* Hedge (exponential weights): regret against sqrt(T log K / 2), and online-to-batch conversion;
* surrogate losses and their psi-transforms (Bartlett, Jordan & McAuliffe 2006);
* minimum-norm least squares: the double-descent curve and benign overfitting with a spiked spectrum.
"""

from __future__ import annotations

import math

import numpy as np

# ---------------------------------------------------------------------------------------------------- ERM


def threshold_data(n: int, rng: np.random.Generator, t0: float = 0.5, eta: float = 0.1):
    """x ~ U(0, 1), y = 1{x > t0}, flipped with probability eta."""
    x = rng.random(n)
    y = (x > t0).astype(int)
    flip = rng.random(n) < eta
    return x, np.where(flip, 1 - y, y)


def threshold_risk(t, t0: float = 0.5, eta: float = 0.1):
    """True 0-1 risk of the classifier 1{x > t}: eta + (1 - 2 eta) |t - t0|."""
    return eta + (1 - 2 * eta) * np.abs(np.asarray(t, float) - t0)


def erm_threshold(x, y) -> float:
    """The empirical risk minimizer over {1{x > t}}: scan the sorted points."""
    order = np.argsort(x)
    xs, ys = x[order], y[order]
    n = len(x)
    # errors for t below all points: predict 1 everywhere -> errors = #zeros
    errs = np.concatenate([[np.sum(ys == 0)], np.sum(ys == 0) - np.cumsum(ys == 0) + np.cumsum(ys == 1)])
    i = int(np.argmin(errs))
    cuts = np.concatenate([[0.0], xs])
    return float(cuts[i]) if i < n else float(xs[-1])


def uniform_deviation_threshold(x, y, t0: float = 0.5, eta: float = 0.1, grid: int = 2001) -> float:
    """sup_t |R_n(t) - R(t)| over a fine grid of thresholds."""
    ts = np.linspace(0, 1, grid)
    order = np.argsort(x)
    xs, ys = x[order], y[order]
    k = np.searchsorted(xs, ts, side="right")
    zeros_below = np.concatenate([[0], np.cumsum(ys == 0)])[k]
    ones_below = np.concatenate([[0], np.cumsum(ys == 1)])[k]
    total_zeros = np.sum(ys == 0)
    emp = (ones_below + (total_zeros - zeros_below)) / len(x)
    return float(np.max(np.abs(emp - threshold_risk(ts, t0, eta))))


def vc_bound(n: int, d: int, delta: float = 0.05) -> float:
    """sup |R_n - R| <= sqrt(8 (d log(2 e n / d) + log(4/delta)) / n) (Vapnik's form)."""
    return math.sqrt(8 * (d * math.log(2 * math.e * n / d) + math.log(4 / delta)) / n)


def rademacher_vc_bound(n: int, d: int) -> float:
    """E sup |R_n - R| <= 2 R_n <= 2 sqrt(2 d log(e n / d) / n) (Massart's lemma plus Sauer-Shelah)."""
    return 2 * math.sqrt(2 * d * math.log(math.e * n / d) / n)


def finite_class_bound(n: int, K: int, delta: float = 0.05) -> float:
    """Hoeffding plus a union bound: sup over K classifiers of |R_n - R| <= sqrt(log(2K/delta) / (2n))."""
    return math.sqrt(math.log(2 * K / delta) / (2 * n))


# --------------------------------------------------------------------------------------------- Rademacher


def rademacher_linear(X, B: float, rng: np.random.Generator, reps: int = 2000) -> float:
    """Empirical Rademacher complexity of {x -> <w, x>: ||w|| <= B}: E (B/n) ||sum sigma_i x_i||."""
    X = np.asarray(X, float)
    n = len(X)
    s = rng.choice([-1.0, 1.0], size=(reps, n))
    return float(np.mean(B * np.linalg.norm(s @ X, axis=1) / n))


def rademacher_linear_bound(X, B: float) -> float:
    X = np.asarray(X, float)
    return float(B * math.sqrt(np.sum(X ** 2)) / len(X))


def rademacher_kernel(K, B: float, rng: np.random.Generator, reps: int = 2000) -> float:
    """{f in H: ||f||_H <= B}: E (B/n) sqrt(sigma^T K sigma) <= B sqrt(tr K) / n."""
    K = np.asarray(K, float)
    n = len(K)
    s = rng.choice([-1.0, 1.0], size=(reps, n))
    q = np.einsum("ri,ij,rj->r", s, K, s)
    return float(np.mean(B * np.sqrt(np.maximum(q, 0)) / n))


def gaussian_kernel(X, bw: float) -> np.ndarray:
    X = np.asarray(X, float)
    d2 = np.sum(X ** 2, 1)[:, None] + np.sum(X ** 2, 1)[None, :] - 2 * X @ X.T
    return np.exp(-np.maximum(d2, 0) / (2 * bw ** 2))


# --------------------------------------------------------------------------------------------------- boosting


def _best_stump(X, y, w):
    """Weighted decision stump minimizing weighted error; y in {-1, +1}."""
    best = (np.inf, 0, 0.0, 1)
    n, d = X.shape
    for j in range(d):
        order = np.argsort(X[:, j])
        xs, ys, ws = X[order, j], y[order], w[order]
        # predict +1 for x > t: error = sum_{x <= t, y = +1} w + sum_{x > t, y = -1} w
        pos_below = np.concatenate([[0.0], np.cumsum(ws * (ys > 0))])
        neg_above = np.sum(ws * (ys < 0)) - np.concatenate([[0.0], np.cumsum(ws * (ys < 0))])
        err = pos_below + neg_above
        for sign, e in ((1, err), (-1, 1 - err)):
            i = int(np.argmin(e))
            if e[i] < best[0]:
                t = -np.inf if i == 0 else (xs[i - 1] + (xs[i] if i < n else xs[i - 1] + 1)) / 2
                best = (float(e[i]), j, float(t), sign)
    return best


def stump_predict(X, j, t, sign):
    return sign * np.where(X[:, j] > t, 1.0, -1.0)


def adaboost(X, y, T: int, Xte=None, yte=None) -> dict:
    """Freund & Schapire's AdaBoost with stumps. Returns train/test error by round and the normalized margins
    y f(x) / sum |alpha| on the training set at selected rounds."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n = len(y)
    w = np.full(n, 1 / n)
    F = np.zeros(n)
    Fte = None if Xte is None else np.zeros(len(yte))
    alphas, tr, te, margins = [], [], [], {}
    for t in range(1, T + 1):
        e, j, thr, sign = _best_stump(X, y, w)
        e = min(max(e, 1e-10), 1 - 1e-10)
        a = 0.5 * math.log((1 - e) / e)
        h = stump_predict(X, j, thr, sign)
        F += a * h
        alphas.append(a)
        w = w * np.exp(-a * y * h)
        w /= w.sum()
        tr.append(float(np.mean(np.sign(F) != y)))
        if Xte is not None:
            Fte += a * stump_predict(Xte, j, thr, sign)
            te.append(float(np.mean(np.sign(Fte) != yte)))
        if t in (5, 50, 500, T):
            margins[t] = (y * F / np.sum(np.abs(alphas))).tolist()
    return {"train": tr, "test": te, "margins": margins}


# ---------------------------------------------------------------------------------------------------- PAC-Bayes


def kl_bernoulli(q: float, p: float) -> float:
    q = min(max(q, 1e-12), 1 - 1e-12)
    p = min(max(p, 1e-12), 1 - 1e-12)
    return q * math.log(q / p) + (1 - q) * math.log((1 - q) / (1 - p))


def kl_inverse(q: float, c: float) -> float:
    """The largest p >= q with kl(q || p) <= c, by bisection."""
    lo, hi = q, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if kl_bernoulli(q, mid) > c:
            hi = mid
        else:
            lo = mid
    return lo


def pac_bayes_bounds(emp_risk_post: float, kl_post_prior: float, n: int, delta: float = 0.05) -> dict:
    """For a posterior rho and prior pi over classifiers, with probability 1 - delta for all rho:
    McAllester (Maurer's form): R(rho) <= R_n(rho) + sqrt((KL + log(2 sqrt n / delta)) / (2n));
    Seeger/Langford: kl(R_n(rho) || R(rho)) <= (KL + log(2 sqrt n / delta)) / n."""
    c = (kl_post_prior + math.log(2 * math.sqrt(n) / delta)) / n
    return {"mcallester": emp_risk_post + math.sqrt(c / 2), "kl": kl_inverse(emp_risk_post, c)}


def gibbs_posterior(emp_risks, lam: float, prior=None) -> np.ndarray:
    """rho(h) propto pi(h) exp(-lam n R_n(h)) (lam on the scale of n R_n)."""
    r = np.asarray(emp_risks, float)
    pi = np.full(len(r), 1 / len(r)) if prior is None else np.asarray(prior, float)
    lw = np.log(pi) - lam * r
    w = np.exp(lw - lw.max())
    return w / w.sum()


def kl_discrete(rho, pi) -> float:
    rho, pi = np.asarray(rho, float), np.asarray(pi, float)
    m = rho > 0
    return float(np.sum(rho[m] * np.log(rho[m] / pi[m])))


# --------------------------------------------------------------------------------------------------- stability


def ridge_fit(X, y, lam: float):
    n, p = X.shape
    return np.linalg.solve(X.T @ X / n + lam * np.eye(p), X.T @ y / n)


def ridge_stability(X, y, lam: float, B: float = 1.0) -> dict:
    """Replace-one stability of ridge with squared loss, computed by refitting, against the bound
    beta <= 2 L^2 R^2 / (lam n) (Bousquet & Elisseeff 2002) with R = max ||x|| and L a Lipschitz constant of the
    loss on the relevant range."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n = len(y)
    w = ridge_fit(X, y, lam)
    diffs = []
    for i in range(0, n, max(1, n // 20)):
        Xi, yi = X.copy(), y.copy()
        j = (i + n // 2) % n  # replace point i by another point with its label flipped: a genuinely different sample
        Xi[i], yi[i] = X[j], -y[j]
        wi = ridge_fit(Xi, yi, lam)
        diffs.append(float(np.max(np.abs(X @ (w - wi)))))
    R = float(np.max(np.linalg.norm(X, axis=1)))
    return {"stability": float(np.max(diffs)), "bound": 4 * B * R ** 2 / (lam * n)}


def sgd_divergence(X, y, steps: int, lr: float, rng: np.random.Generator, reps: int = 20) -> dict:
    """Uniform stability of SGD for logistic regression (Hardt, Recht & Singer 2016): run SGD on two samples that
    differ in one point, with the same index sequence, and record ||w_t - w'_t||.  With ||x|| <= 1 the loss is
    1-Lipschitz and 1/4-smooth, so for lr <= 8 the expected divergence is at most (2/n) * sum of the step sizes."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    paths = np.zeros(steps)
    for _ in range(reps):
        i0 = int(rng.integers(n))
        X2, y2 = X.copy(), y.copy()
        z = rng.standard_normal(p)
        X2[i0] = z / max(1.0, float(np.linalg.norm(z)))
        y2[i0] = -y[i0]
        w, w2 = np.zeros(p), np.zeros(p)
        idx = rng.integers(n, size=steps)
        for t, i in enumerate(idx):
            m = y[i] * (X[i] @ w)
            w = w + lr * y[i] * X[i] / (1 + math.exp(m))
            m2 = y2[i] * (X2[i] @ w2)
            w2 = w2 + lr * y2[i] * X2[i] / (1 + math.exp(m2))
            paths[t] += float(np.linalg.norm(w - w2))
    paths /= reps
    return {"divergence": paths, "bound": 2 * lr * np.arange(1, steps + 1) / n}


# --------------------------------------------------------------------------------------------- online learning


def hedge(losses, eta: float) -> dict:
    """Exponential weights over K experts; losses (T, K) in [0, 1]. Returns the cumulative regret path."""
    L = np.asarray(losses, float)
    T, K = L.shape
    cum = np.zeros(K)
    alg = 0.0
    regret = []
    for t in range(T):
        w = np.exp(-eta * (cum - cum.min()))
        w /= w.sum()
        alg += float(w @ L[t])
        cum += L[t]
        regret.append(alg - float(cum.min()))
    return {"regret": np.asarray(regret)}


def hedge_bound(T: int, K: int) -> float:
    return math.sqrt(T * math.log(K) / 2)


def bandit(means, T: int, algo: str, rng: np.random.Generator, eps: float = 0.1) -> np.ndarray:
    """Pseudo-regret path of a Bernoulli bandit run with 'ucb' (UCB1, Auer et al. 2002), 'exp3' (tuned for
    gains in [0, 1]) or 'greedy' (epsilon-greedy with fixed epsilon)."""
    mu = np.asarray(means, float)
    K = len(mu)
    best = mu.max()
    cnt, sm = np.zeros(K), np.zeros(K)
    logw = np.zeros(K)
    gamma = min(1.0, math.sqrt(K * math.log(K) / ((math.e - 1) * T)))
    reg = np.zeros(T)
    tot = 0.0
    for t in range(T):
        if algo == "ucb":
            k = t if t < K else int(np.argmax(sm / cnt + np.sqrt(2 * math.log(t + 1) / cnt)))
        elif algo == "greedy":
            k = t if t < K else (int(rng.integers(K)) if rng.random() < eps else int(np.argmax(sm / cnt)))
        elif algo == "exp3":
            w = np.exp(logw - logw.max())
            pr = (1 - gamma) * w / w.sum() + gamma / K
            k = int(rng.choice(K, p=pr))
        else:
            raise ValueError(algo)
        g = float(rng.random() < mu[k])
        cnt[k] += 1
        sm[k] += g
        if algo == "exp3":
            logw[k] += gamma * g / (pr[k] * K)
        tot += best - mu[k]
        reg[t] = tot
    return reg


def lai_robbins(means, T) -> np.ndarray:
    """Lai & Robbins's asymptotic lower bound on the regret: sum over suboptimal arms of Delta_k / KL(mu_k, mu*) log T."""
    mu = np.asarray(means, float)
    b = mu.max()
    c = sum((b - m) / kl_bernoulli(m, b) for m in mu if m < b)
    return c * np.log(np.asarray(T, float))


# ---------------------------------------------------------------------------------------------------- surrogates


def psi_transform(theta, loss: str) -> np.ndarray:
    """Bartlett, Jordan & McAuliffe's psi: excess 0-1 risk theta forces excess surrogate risk >= psi(theta)."""
    th = np.asarray(theta, float)
    if loss == "hinge":
        return np.abs(th)
    if loss == "squared":
        return th ** 2
    if loss == "exponential":
        return 1 - np.sqrt(1 - th ** 2)
    if loss == "logistic":
        a, b = (1 + th) / 2, (1 - th) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            v = np.log(2) + np.where(a > 0, a * np.log(np.maximum(a, 1e-300)), 0) + np.where(b > 0, b * np.log(np.maximum(b, 1e-300)), 0)
        return v / np.log(2)
    raise ValueError(loss)


# ------------------------------------------------------------------------------------------------ interpolation


def min_norm_risk(n: int, p: int, rng: np.random.Generator, snr_beta: float = 1.0, sigma: float = 0.5,
                  reps: int = 20, p_total: int | None = None) -> float:
    """Test risk of min-norm least squares using the first p of p_total isotropic features (the misspecified
    double-descent model of Belkin, Hsu & Xu 2020 / Hastie et al. 2022): y = x^T beta + noise, beta spread evenly."""
    P = p_total or max(p, 2 * n)
    beta = np.full(P, snr_beta / math.sqrt(P))
    out = []
    for _ in range(reps):
        X = rng.standard_normal((n, P))
        y = X @ beta + sigma * rng.standard_normal(n)
        b = np.linalg.pinv(X[:, :p]) @ y
        # E (x^T beta - x_p^T b)^2 = ||beta_p - b||^2 + ||beta_rest||^2 (isotropic x)
        out.append(float(np.sum((beta[:p] - b) ** 2) + np.sum(beta[p:] ** 2)))
    return float(np.mean(out))


def benign_risk(n: int, rng: np.random.Generator, k: int = 5, p_tail: int = 20000, tail_var: float = 0.0005, sigma: float = 0.5,
                reps: int = 10) -> dict:
    """Benign overfitting (Bartlett, Long, Lugosi & Tsigler 2020): k strong directions carrying the signal plus p_tail
    weak ones with total variance p_tail * tail_var. Min-norm interpolation; returns its train error (0), test excess
    risk, and the noise level."""
    out = []
    for _ in range(reps):
        Xs = rng.standard_normal((n, k))
        Xt = math.sqrt(tail_var) * rng.standard_normal((n, p_tail))
        X = np.hstack([Xs, Xt])
        beta = np.concatenate([np.ones(k), np.zeros(p_tail)])
        y = X @ beta + sigma * rng.standard_normal(n)
        b = np.linalg.pinv(X) @ y
        d = beta - b
        ex = float(np.sum(d[:k] ** 2) + tail_var * np.sum(d[k:] ** 2))
        out.append(ex)
    return {"excess": float(np.mean(out)), "noise": sigma ** 2}
