"""statkit.evals (Part 64): statistics for evaluating and deploying AI systems.

Benchmarks as samples (clustered standard errors), paired comparisons and McNemar's test, the leaderboard's winner's
curse, Bradley-Terry arenas with model-based, sandwich and bootstrap intervals, Elo's order dependence, two-parameter
IRT for benchmarks, adaptive reuse of a holdout and Thresholdout, model-judged labels with prediction-powered
inference, model collapse of a Gaussian refit to its own samples, conformal factuality, green-list watermark
detection, the calibration of amortized posteriors, Tweedie denoising and the probability-flow sampler with an exact
or smoothed empirical score, and a two-sided-market A/B test."""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats

# --------------------------------------------------------------------------------------------- benchmarks


def mean_se(x) -> dict:
    """The mean of per-question scores with the iid standard error sd/sqrt(n)."""
    x = np.asarray(x, float)
    return {"mean": float(x.mean()), "se": float(x.std(ddof=1) / math.sqrt(len(x)))}


def cluster_se(x, cluster) -> dict:
    """The mean with the cluster-robust standard error (Part 23's CR1): questions sharing a passage, a template or a
    source are correlated, so sum the residuals within each cluster before squaring.
    SE^2 = G/(G - 1) * sum_c (sum_{i in c} (x_i - xbar))^2 / n^2."""
    x = np.asarray(x, float)
    cl = np.asarray(cluster)
    n = len(x)
    r = x - x.mean()
    _, inv = np.unique(cl, return_inverse=True)
    s = np.bincount(inv, weights=r)
    G = len(s)
    return {"mean": float(x.mean()), "se": float(math.sqrt(G / (G - 1) * np.sum(s ** 2)) / n), "clusters": G}


def clustered_benchmark(G: int, m: int, acc: float, tau: float, rng: np.random.Generator) -> dict:
    """A benchmark of G clusters of m questions: each cluster has a latent logit offset u_c ~ N(0, tau^2), and a
    question is answered correctly with probability expit(logit(acc) + u_c).  Returns the 0/1 scores and cluster ids."""
    u = rng.normal(0, tau, G)
    p = 1 / (1 + np.exp(-(math.log(acc / (1 - acc)) + np.repeat(u, m))))
    return {"x": (rng.random(G * m) < p).astype(float), "cluster": np.repeat(np.arange(G), m), "p": p}


def design_effect(m: int, icc: float) -> float:
    """Kish's design effect for clusters of size m with intraclass correlation icc: 1 + (m - 1) icc."""
    return 1 + (m - 1) * icc


# --------------------------------------------------------------------------------------- paired comparisons


def paired_compare(a, b, alpha: float = 0.05) -> dict:
    """Two models scored on the same questions: the difference in accuracy with the paired SE sd(a - b)/sqrt(n), and the
    unpaired SE sqrt(var a/n + var b/n) that ignores the pairing; with their (1 - alpha) intervals."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = len(a)
    d = a - b
    z = stats.norm.ppf(1 - alpha / 2)
    sp = d.std(ddof=1) / math.sqrt(n)
    su = math.sqrt(a.var(ddof=1) / n + b.var(ddof=1) / n)
    m = float(d.mean())
    return {"diff": m, "se_paired": float(sp), "se_unpaired": float(su), "paired": (m - z * sp, m + z * sp),
            "unpaired": (m - z * su, m + z * su), "corr": float(np.corrcoef(a, b)[0, 1]) if a.std() > 0 and b.std() > 0 else 0.0}


def mcnemar(a, b) -> dict:
    """McNemar's exact test: only the discordant questions carry information about which model is better; under the
    null each is equally likely to favour either model, so n10 ~ Binomial(n10 + n01, 1/2)."""
    a, b = np.asarray(a, int), np.asarray(b, int)
    n10, n01 = int(np.sum((a == 1) & (b == 0))), int(np.sum((a == 0) & (b == 1)))
    k = n10 + n01
    p = 1.0 if k == 0 else float(min(1.0, 2 * stats.binom.cdf(min(n10, n01), k, 0.5)))
    return {"n10": n10, "n01": n01, "p": p}


def correlated_pair(n: int, acc_a: float, acc_b: float, rho_latent: float, rng: np.random.Generator) -> tuple:
    """Two models' 0/1 scores on n questions whose difficulty is shared: a latent difficulty d_i ~ N(0, 1) enters both
    models' logits with weight ``rho_latent`` (on the probit scale), so their errors are positively correlated."""
    d = rng.standard_normal(n)
    e1, e2 = rng.standard_normal(n), rng.standard_normal(n)
    s = math.sqrt(1 - rho_latent ** 2)
    a = rho_latent * d + s * e1 < stats.norm.ppf(acc_a)
    b = rho_latent * d + s * e2 < stats.norm.ppf(acc_b)
    return a.astype(float), b.astype(float)


def winners_curse(k: int, n: int, acc: float, reps: int, rng: np.random.Generator) -> dict:
    """k models of identical true accuracy on the same n-question benchmark (independent errors): the top model's
    observed accuracy exceeds its true accuracy on average by about sd * E[max of k normals]."""
    top = rng.binomial(n, acc, size=(reps, k)).max(1) / n
    sd = math.sqrt(acc * (1 - acc) / n)
    return {"bias": float(top.mean() - acc), "sd": sd, "approx": float(sd * expected_max_normal(k))}


def expected_max_normal(k: int) -> float:
    """E[max of k iid N(0, 1)] by numerical integration."""
    f = lambda x: x * k * stats.norm.pdf(x) * stats.norm.cdf(x) ** (k - 1)  # noqa: E731
    from scipy import integrate

    return float(integrate.quad(f, -10, 10)[0])


# ----------------------------------------------------------------------------------------------- arenas


def simulate_battles(theta, n: int, rng: np.random.Generator, pairs=None) -> dict:
    """n battles between random pairs of models with Bradley-Terry strengths ``theta`` (log scale):
    P(i beats j) = expit(theta_i - theta_j).  Returns arrays i, j and y (1 if i won)."""
    theta = np.asarray(theta, float)
    K = len(theta)
    i = rng.integers(0, K, n)
    j = (i + rng.integers(1, K, n)) % K
    y = (rng.random(n) < 1 / (1 + np.exp(-(theta[i] - theta[j])))).astype(float)
    return {"i": i, "j": j, "y": y}


def bt_fit(i, j, y, K: int, ref: int = 0, iters: int = 50) -> dict:
    """Bradley-Terry by logistic regression: a battle is a row with +1 in column i and -1 in column j, the reference
    model's column dropped (its strength fixed at 0), and y the outcome.  Newton-Raphson; returns the strengths, the
    model-based SEs from the inverse Fisher information, and the sandwich SEs (Part 22)."""
    i, j, y = np.asarray(i), np.asarray(j), np.asarray(y, float)
    n = len(y)
    X = np.zeros((n, K))
    X[np.arange(n), i] += 1
    X[np.arange(n), j] -= 1
    keep = [k for k in range(K) if k != ref]
    X = X[:, keep]
    w = np.zeros(K - 1)
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w))
        g = X.T @ (y - p)
        H = (X * (p * (1 - p))[:, None]).T @ X + 1e-9 * np.eye(K - 1)
        step = np.linalg.solve(H, g)
        w += step
        if np.max(np.abs(step)) < 1e-10:
            break
    p = 1 / (1 + np.exp(-X @ w))
    H = (X * (p * (1 - p))[:, None]).T @ X
    Hi = np.linalg.inv(H)
    S = X * (y - p)[:, None]
    V = Hi @ (S.T @ S) @ Hi
    theta = np.zeros(K)
    theta[keep] = w
    se, se_sw = np.zeros(K), np.zeros(K)
    se[keep] = np.sqrt(np.diag(Hi))
    se_sw[keep] = np.sqrt(np.diag(V))
    return {"theta": theta, "se": se, "se_sandwich": se_sw}


def bt_style_fit(i, j, y, K: int, style, ref: int = 0) -> dict:
    """Bradley-Terry with style control: P(i beats j) = expit(theta_i - theta_j + gamma . (s_i - s_j)), where ``style``
    is a (n, q) array of the battle's style differences (say, answer length).  The strengths are then compared at equal
    style.  Style must vary within each model's answers, or it is confounded with the model.  Returns theta and gamma."""
    i, j, y = np.asarray(i), np.asarray(j), np.asarray(y, float)
    n = len(y)
    X = np.zeros((n, K))
    X[np.arange(n), i] += 1
    X[np.arange(n), j] -= 1
    keep = [k for k in range(K) if k != ref]
    Z = np.column_stack([X[:, keep], np.asarray(style, float).reshape(n, -1)])
    w = logistic_fit(Z, y)
    theta = np.zeros(K)
    theta[keep] = w[: K - 1]
    return {"theta": theta, "gamma": w[K - 1:]}


def logistic_fit(X, y, iters: int = 60) -> np.ndarray:
    """Logistic regression without intercept by Newton-Raphson."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w))
        H = (X * (p * (1 - p))[:, None]).T @ X + 1e-9 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p))
        w += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return w


def bt_bootstrap(i, j, y, K: int, B: int, rng: np.random.Generator, ref: int = 0) -> np.ndarray:
    """B bootstrap refits of Bradley-Terry over resampled battles; returns a (B, K) array of strengths."""
    n = len(y)
    out = np.zeros((B, K))
    for b in range(B):
        k = rng.integers(0, n, n)
        out[b] = bt_fit(np.asarray(i)[k], np.asarray(j)[k], np.asarray(y)[k], K, ref)["theta"]
    return out


def elo(i, j, y, K: int, k_factor: float = 4.0, scale: float = 400.0) -> np.ndarray:
    """Online Elo ratings (base-10, 400-point scale), updated battle by battle in the given order."""
    r = np.zeros(K)
    for a, b, o in zip(i, j, y):
        e = 1 / (1 + 10 ** ((r[b] - r[a]) / scale))
        r[a] += k_factor * (o - e)
        r[b] -= k_factor * (o - e)
    return r - r[0]


# ------------------------------------------------------------------------------------------------- IRT


def fit_2pl(R, iters: int = 30, ridge: float = 0.01) -> dict:
    """Joint maximum likelihood for the two-parameter logistic IRT model P(R_mj = 1) = expit(a_j (theta_m - b_j)),
    with models m and items j: alternate Newton steps for each item's (a_j, b_j) and each model's theta_m, then
    standardize theta.  A small ridge keeps items that everyone (or no one) answers finite."""
    R = np.asarray(R, float)
    M, J = R.shape
    th = stats.norm.ppf((R.mean(1) * M + 0.5) / (M + 1))
    th = (th - th.mean()) / th.std()
    a = np.ones(J)
    b = -stats.norm.ppf((R.mean(0) * M + 0.5) / (M + 1))
    for _ in range(iters):
        for _ in range(2):  # items
            z = a[None, :] * (th[:, None] - b[None, :])
            p = 1 / (1 + np.exp(-z))
            r = R - p
            w = p * (1 - p)
            da = th[:, None] - b[None, :]
            ga = (r * da).sum(0) - ridge * (a - 1)
            gb = (-r * a[None, :]).sum(0) - ridge * b
            haa = (w * da ** 2).sum(0) + ridge
            hbb = (w * a[None, :] ** 2).sum(0) + ridge
            hab = (-w * a[None, :] * da).sum(0)
            det = haa * hbb - hab ** 2
            a = np.clip(a + (hbb * ga - hab * gb) / det, 0.05, 6)
            b = np.clip(b + (haa * gb - hab * ga) / det, -6, 6)
        for _ in range(2):  # models
            z = a[None, :] * (th[:, None] - b[None, :])
            p = 1 / (1 + np.exp(-z))
            g = ((R - p) * a[None, :]).sum(1) - 0.01 * th
            h = (p * (1 - p) * a[None, :] ** 2).sum(1) + 0.01
            th = th + g / h
        mu, sd = th.mean(), th.std()
        th = (th - mu) / sd
        a, b = a * sd, (b - mu) / sd
    return {"theta": th, "a": a, "b": b}


def irt_ability(r, a, b, prior_sd: float = 3.0) -> float:
    """A new model's ability from its responses r on items with known (a, b): the posterior mode under N(0, prior_sd^2)."""
    r, a, b = np.asarray(r, float), np.asarray(a, float), np.asarray(b, float)
    th = 0.0
    for _ in range(50):
        p = 1 / (1 + np.exp(-a * (th - b)))
        g = np.sum(a * (r - p)) - th / prior_sd ** 2
        h = np.sum(a ** 2 * p * (1 - p)) + 1 / prior_sd ** 2
        th += g / h
    return float(th)


def irt_accuracy(theta: float, a, b) -> float:
    """The predicted accuracy over all items of a model with ability theta."""
    return float(np.mean(1 / (1 + np.exp(-np.asarray(a) * (theta - np.asarray(b))))))


# ------------------------------------------------------------------------------------- adaptive holdout reuse


def thresholdout(train_val: float, hold_val: float, T: float, sigma: float, rng: np.random.Generator) -> float:
    """Dwork et al.'s (2015) Thresholdout: answer a query with the training value unless it differs from the holdout
    value by more than a noisy threshold, and then with the holdout value plus Laplace noise."""
    if abs(train_val - hold_val) > T + rng.laplace(0, 2 * sigma):
        return float(hold_val + rng.laplace(0, sigma))
    return float(train_val)


def adaptive_overfit(n: int, d: int, ks, rng: np.random.Generator, method: str = "reuse", T: float = 0.04,
                     sigma: float = 0.01) -> dict:
    """Dwork et al.'s (2015) experiment: labels are pure noise, so every classifier has true accuracy 1/2.  The analyst
    computes each feature's correlation with the label on the training set, asks the holdout for the same correlations
    (exactly, ``reuse``, or through Thresholdout), keeps the features where both agree in sign and are large, and builds
    a classifier from the top k.  Returns its reported holdout accuracy and its accuracy on fresh data, for each k."""
    Xt, Xh, Xf = rng.standard_normal((n, d)), rng.standard_normal((n, d)), rng.standard_normal((n, d))
    yt, yh, yf = rng.choice([-1, 1], n), rng.choice([-1, 1], n), rng.choice([-1, 1], n)
    ct, ch = Xt.T @ yt / n, Xh.T @ yh / n
    thr = 1.0 / math.sqrt(n)
    if method == "reuse":
        ans = ch
    else:
        ans = np.array([thresholdout(a, b, T, sigma, rng) for a, b in zip(ct, ch)])
    ok = (np.sign(ct) == np.sign(ans)) & (np.abs(ct) > thr) & (np.abs(ans) > thr)
    order = np.argsort(-np.abs(ct) * ok)
    out = {"k": list(ks), "holdout": [], "fresh": []}
    for k in ks:
        sel = order[:k]
        sel = sel[ok[sel]]
        w = np.zeros(d)
        w[sel] = np.sign(ct[sel])
        acc_h = float(np.mean(np.sign(Xh @ w + 1e-12) == yh))
        if method != "reuse":
            acc_t = float(np.mean(np.sign(Xt @ w + 1e-12) == yt))
            acc_h = thresholdout(acc_t, acc_h, T, sigma, rng)
        out["holdout"].append(acc_h)
        out["fresh"].append(float(np.mean(np.sign(Xf @ w + 1e-12) == yf)))
    return out


# -------------------------------------------------------------------------------------- labels from models


def judged_labels(truth, sens: float, spec: float, rng: np.random.Generator) -> np.ndarray:
    """A judge's labels of true 0/1 correctness, with sensitivity P(judge 1 | 1) and specificity P(judge 0 | 0)."""
    t = np.asarray(truth, int)
    u = rng.random(len(t))
    return np.where(t == 1, u < sens, u >= spec).astype(float)


def ppi_mean_ci(y_lab, f_lab, f_unlab, alpha: float = 0.05) -> dict:
    """Prediction-powered inference for a mean (Angelopoulos et al. 2023): the judge's mean on N unlabelled items, plus
    the rectifier, the mean of (human - judge) on n labelled ones; the variance adds the two parts."""
    y_lab, f_lab, f_unlab = (np.asarray(v, float) for v in (y_lab, f_lab, f_unlab))
    n, N = len(y_lab), len(f_unlab)
    rect = y_lab - f_lab
    est = f_unlab.mean() + rect.mean()
    se = math.sqrt(f_unlab.var(ddof=1) / N + rect.var(ddof=1) / n)
    z = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(est), "se": float(se), "ci": (float(est - z * se), float(est + z * se))}


def wald_ci(x, alpha: float = 0.05) -> dict:
    x = np.asarray(x, float)
    m, se = x.mean(), x.std(ddof=1) / math.sqrt(len(x))
    z = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(m), "se": float(se), "ci": (float(m - z * se), float(m + z * se))}


# ------------------------------------------------------------------------------------------- model collapse


def gaussian_collapse(n: int, T: int, reps: int, rng: np.random.Generator, accumulate: bool = False) -> dict:
    """Shumailov et al.'s (2024) model collapse in its simplest form: fit N(mu, sigma^2) by maximum likelihood to n
    samples, draw n new samples from the fit, refit, and repeat T times.  With replacement, E[sigma_t^2] =
    ((n - 1)/n)^t and log sigma_t^2 is a random walk with negative drift, so sigma_t -> 0 almost surely.  With
    ``accumulate`` the new samples are added to all earlier ones (Gerstgrasser et al. 2024), and the variance stays
    put.  Returns the sigma^2 paths (reps x (T + 1))."""
    paths = np.zeros((reps, T + 1))
    for r in range(reps):
        x = rng.standard_normal(n)
        pool = x.copy()
        mu, s2 = x.mean(), x.var()
        paths[r, 0] = 1.0
        for t in range(1, T + 1):
            new = mu + math.sqrt(s2) * rng.standard_normal(n)
            if accumulate:
                pool = np.concatenate([pool, new])
                mu, s2 = pool.mean(), pool.var()
            else:
                mu, s2 = new.mean(), new.var()
            paths[r, t] = s2
    return {"paths": paths, "expected": ((n - 1) / n) ** np.arange(T + 1),
            "drift": float(stats.chi2(n - 1).expect(lambda v: np.log(v / n)))}


# --------------------------------------------------------------------------------------- conformal factuality


def conformal_factuality(cal_scores, cal_true, test_scores, alpha: float) -> dict:
    """Mohri & Hashimoto's (2024) conformal factuality: each response is a list of claims with confidence scores and
    (on calibration data) true/false labels.  A response is safe at threshold t if every claim scoring above t is
    true; the smallest such t is the largest score of a false claim.  The conformal quantile of those thresholds over
    calibration responses gives a t at which a new response, filtered to claims above t, is entirely true with
    probability at least 1 - alpha."""
    need = np.array([max([s for s, c in zip(sc, tr) if not c], default=-np.inf) for sc, tr in zip(cal_scores, cal_true)])
    n = len(need)
    k = math.ceil((n + 1) * (1 - alpha))
    t = np.inf if k > n else float(np.sort(need)[k - 1])
    kept = [[s > t for s in sc] for sc in test_scores]
    return {"threshold": t, "kept": kept}


def claim_responses(m: int, n_claims: int, p_true: float, signal: float, rng: np.random.Generator) -> tuple:
    """m responses of n_claims claims each; each claim is true with probability p_true, and its confidence score is
    signal * (true) + N(0, 1)."""
    tr = rng.random((m, n_claims)) < p_true
    sc = signal * tr + rng.standard_normal((m, n_claims))
    return [list(r) for r in sc], [list(r) for r in tr]


# ------------------------------------------------------------------------------------------------ watermarks


def green_prob(gamma: float, delta: float) -> float:
    """Kirchenbauer et al.'s (2023) soft watermark on a high-entropy token: a fraction gamma of the vocabulary, chosen
    by hashing the previous token, has delta added to its logits, so a uniform next-token distribution becomes green
    with probability gamma e^delta / (gamma e^delta + 1 - gamma)."""
    return gamma * math.exp(delta) / (gamma * math.exp(delta) + 1 - gamma)


def watermark_z(green: int, T: int, gamma: float) -> float:
    """The detector's z statistic: (green - gamma T) / sqrt(T gamma (1 - gamma)), standard normal for human text."""
    return (green - gamma * T) / math.sqrt(T * gamma * (1 - gamma))


def watermark_power(T: int, gamma: float, delta: float, z_thr: float, entropy_frac: float = 1.0, edit_frac: float = 0.0) -> float:
    """Exact detection power for T tokens: each token is green with probability gamma (a low-entropy or edited token)
    or green_prob (a high-entropy watermarked token); a fraction ``entropy_frac`` of tokens are high-entropy and a
    fraction ``edit_frac`` have been rewritten.  The green count is Binomial(T, q); power is P(z > z_thr)."""
    q_w = green_prob(gamma, delta)
    q = (1 - edit_frac) * (entropy_frac * q_w + (1 - entropy_frac) * gamma) + edit_frac * gamma
    need = math.ceil(gamma * T + z_thr * math.sqrt(T * gamma * (1 - gamma)) + 1e-9)
    return float(stats.binom.sf(need - 1, T, q))


# --------------------------------------------------------------------------------- simulation-based inference


def amortized_posterior_coverage(n_sim: int, p_feat: int, level: float, reps: int, rng: np.random.Generator,
                                 heldout: bool = False, n_obs: int = 10) -> float:
    """An amortized Gaussian posterior for a normal mean: theta ~ N(0, 1), x = n_obs draws from N(theta, 1).  The
    approximation regresses theta on p_feat polynomial features of the sample mean, fitted on n_sim simulations, and
    reports the regression mean with the residual variance as the posterior.  With in-sample residuals an overfitted
    regression is overconfident (Hermans et al. 2022); with residuals from held-out simulations it is calibrated.
    Returns the frequentist coverage of the central ``level`` credible interval over reps fresh (theta, x)."""
    def feats(xbar):
        return np.column_stack([xbar ** k for k in range(p_feat + 1)])

    th = rng.standard_normal(n_sim)
    xb = th + rng.standard_normal(n_sim) / math.sqrt(n_obs)
    F = feats(xb / 2)
    beta, *_ = np.linalg.lstsq(F, th, rcond=None)
    if heldout:
        th2 = rng.standard_normal(n_sim)
        xb2 = th2 + rng.standard_normal(n_sim) / math.sqrt(n_obs)
        s2 = float(np.mean((th2 - feats(xb2 / 2) @ beta) ** 2))
    else:
        s2 = float(np.sum((th - F @ beta) ** 2) / n_sim)
    z = stats.norm.ppf(0.5 + level / 2)
    t0 = rng.standard_normal(reps)
    x0 = t0 + rng.standard_normal(reps) / math.sqrt(n_obs)
    m0 = feats(x0 / 2) @ beta
    return float(np.mean(np.abs(t0 - m0) <= z * math.sqrt(s2)))


# ------------------------------------------------------------------------------------- diffusion and Tweedie


def mixture_score(y, sigma: float, mus, s: float, w) -> np.ndarray:
    """The score d/dy log p_sigma(y) of a one-dimensional Gaussian mixture sum_k w_k N(mu_k, s^2) convolved with
    N(0, sigma^2).  With s = 0 and the training points as mus, it is the exact score of the noised empirical law."""
    y = np.asarray(y, float)[:, None]
    mus, w = np.asarray(mus, float)[None, :], np.asarray(w, float)[None, :]
    v = s ** 2 + sigma ** 2
    logp = np.log(w) - 0.5 * (y - mus) ** 2 / v
    r = np.exp(logp - logp.max(1, keepdims=True))
    r /= r.sum(1, keepdims=True)
    return np.sum(r * (mus - y) / v, axis=1)


def tweedie(y, sigma: float, score) -> np.ndarray:
    """Tweedie's formula (Part 25): E[x | y] = y + sigma^2 * score(y) for y = x + N(0, sigma^2)."""
    return np.asarray(y, float) + sigma ** 2 * np.asarray(score, float)


def probability_flow(score_fn, sigmas, n: int, rng: np.random.Generator) -> np.ndarray:
    """Samples by the probability-flow ODE of the variance-exploding diffusion, dx/dsigma = -sigma score(x, sigma),
    integrated by Heun's method from sigmas[0] (large) down to sigmas[-1], starting from N(0, sigmas[0]^2)."""
    x = sigmas[0] * rng.standard_normal(n)
    for s0, s1 in zip(sigmas[:-1], sigmas[1:]):
        d0 = -s0 * score_fn(x, s0)
        xe = x + (s1 - s0) * d0
        d1 = -s1 * score_fn(xe, s1)
        x = x + (s1 - s0) * 0.5 * (d0 + d1)
    return x


# ------------------------------------------------------------------------------------- deployment experiments


def market_purchases(t, supply: int, base: float, lift: float, rng: np.random.Generator) -> np.ndarray:
    """One market: buyer k wants an item with probability base * (1 + lift * t_k); if more want one than there are
    items, the ``supply`` items go to wanting buyers drawn in proportion to their weights.  Returns who bought."""
    t = np.asarray(t, float)
    wgt = base * (1 + lift * t)
    want = np.flatnonzero(rng.random(len(t)) < np.minimum(wgt, 1))
    if len(want) > supply:
        want = rng.choice(want, supply, replace=False, p=wgt[want] / wgt[want].sum())
    got = np.zeros(len(t))
    got[want] = 1
    return got


def market_ab(n_buyers: int, supply: int, base: float, lift: float, p_treat: float, rng: np.random.Generator) -> dict:
    """A two-sided market with shared supply: the naive A/B difference in purchase rates with a fraction p_treat
    treated, against the global effect of treating everyone versus no one.  Treated buyers take items from control
    buyers, so the naive difference overstates the global effect when supply binds."""
    t = (rng.random(n_buyers) < p_treat).astype(float)
    g = market_purchases(t, supply, base, lift, rng)
    naive = float(g[t == 1].mean() - g[t == 0].mean())
    glob = float(market_purchases(np.ones(n_buyers), supply, base, lift, rng).mean()
                 - market_purchases(np.zeros(n_buyers), supply, base, lift, rng).mean())
    return {"naive": naive, "global": glob}


def market_randomized(n_markets: int, n_buyers: int, supply: int, base: float, lift: float, rng: np.random.Generator) -> float:
    """Randomize whole markets (half treated entirely): the difference in mean purchase rates estimates the global
    effect without interference between arms."""
    z = rng.permutation(np.repeat([0, 1], n_markets // 2))
    rates = np.array([market_purchases(np.full(n_buyers, float(k)), supply, base, lift, rng).mean() for k in z])
    return float(rates[z == 1].mean() - rates[z == 0].mean())
