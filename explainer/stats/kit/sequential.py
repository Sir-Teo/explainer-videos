"""statkit.sequential: anytime-valid inference and adaptive experiments (Part 58 of *Statistics, Built*).

    Wald's SPRT for Bernoulli data: exact operating characteristic and stopping-time law on the lattice    (Wald 1945)
    Wald's approximations, the fixed-sample comparison, Wald's identity                                    (Wald 1947)
    estimation after a group-sequential stop                                                               (Whitehead 1986)
    test martingales, Ville's inequality, the peeking p-value                                              (Ville 1939)
    calibrators and merging of e-values                                                                    (Vovk & Wang 2021)
    universal inference: the split likelihood-ratio e-value                                               (Wasserman et al. 2020)
    normal-mixture, stitched (LIL) and betting confidence sequences                       (Robbins 1970; Howard et al. 2021;
                                                                                           Waudby-Smith & Ramdas 2024)
    e-BH                                                                                                   (Wang & Ramdas 2022)
    CUSUM and Bayesian online changepoint detection                                    (Page 1954; Adams & MacKay 2007)
    Thompson sampling, the bias of adaptively collected means, adaptively weighted AIPW
                                                                         (Thompson 1933; Nie et al. 2018; Hadad et al. 2021)
    off-policy evaluation: IPW and doubly robust policy values
"""

from __future__ import annotations

import math

import numpy as np
from scipy import special, stats

# ------------------------------------------------------------------------------------------------------- the SPRT


def sprt_bounds(alpha: float, beta: float) -> dict:
    """Wald's thresholds for the likelihood ratio: accept H1 when LR >= A = (1 - beta)/alpha, accept H0 when
    LR <= B = beta/(1 - alpha)."""
    A, B = (1 - beta) / alpha, beta / (1 - alpha)
    return {"A": A, "B": B, "logA": math.log(A), "logB": math.log(B)}


def sprt_bernoulli_exact(p: float, p0: float, p1: float, alpha: float, beta: float, n_max: int = 5000) -> dict:
    """The SPRT of p0 against p1 (p1 > p0) on Bernoulli(p) data, computed exactly.  After n trials with s successes the
    log LR is s a + (n - s) b, a = log(p1/p0), b = log((1 - p1)/(1 - p0)); the walk lives on a lattice, so the law of
    (stopping time, decision) follows by propagating the probabilities of the continuing states.  Returns the
    probability of accepting H1, the expected sample size, and the stopping-time distribution."""
    a, b = math.log(p1 / p0), math.log((1 - p1) / (1 - p0))
    th = sprt_bounds(alpha, beta)
    lo, hi = th["logB"], th["logA"]
    prob = {0: 1.0}  # continuing states after n trials: successes -> probability
    acc1 = acc0 = 0.0
    en = 0.0
    stop_n = np.zeros(n_max + 1)
    for n in range(1, n_max + 1):
        new: dict = {}
        for s, pr in prob.items():
            for ds, q in ((1, p), (0, 1 - p)):
                new[s + ds] = new.get(s + ds, 0.0) + pr * q
        prob = {}
        for s, pr in new.items():
            llr = s * a + (n - s) * b
            if llr >= hi:
                acc1 += pr
                en += n * pr
                stop_n[n] += pr
            elif llr <= lo:
                acc0 += pr
                en += n * pr
                stop_n[n] += pr
            else:
                prob[s] = pr
        if sum(prob.values()) < 1e-13:
            break
    rest = sum(prob.values())
    return {"accept_h1": acc1, "accept_h0": acc0, "asn": en + n_max * rest, "unfinished": rest, "stop_n": stop_n[: n + 1],
            "a": a, "b": b}


def sprt_wald_approx(p: float, p0: float, p1: float, alpha: float, beta: float) -> dict:
    """Wald's approximations ignoring overshoot: with h solving E_p[(f1/f0)^h] = 1, the operating characteristic is
    OC = (A^h - 1)/(A^h - B^h) (the probability of accepting H0), and E N = E[log LR at stopping]/E[log LR per step]."""
    a, b = math.log(p1 / p0), math.log((1 - p1) / (1 - p0))
    th = sprt_bounds(alpha, beta)
    lA, lB = th["logA"], th["logB"]
    z = p * a + (1 - p) * b  # mean log LR per observation
    if abs(z) < 1e-12:  # h = 0: the limit
        oc = lA / (lA - lB)
        asn = -lA * lB / (p * a * a + (1 - p) * b * b)
        return {"oc": oc, "accept_h1": 1 - oc, "asn": asn, "h": 0.0}
    # solve p (p1/p0)^h + (1 - p) ((1 - p1)/(1 - p0))^h = 1 for h != 0
    f = lambda h: p * math.exp(a * h) + (1 - p) * math.exp(b * h) - 1  # noqa: E731
    from scipy.optimize import brentq

    h = brentq(f, 1e-9, 60) if z < 0 else brentq(f, -60, -1e-9)
    Ah, Bh = math.exp(h * lA), math.exp(h * lB)
    oc = (Ah - 1) / (Ah - Bh)
    asn = (oc * lB + (1 - oc) * lA) / z
    return {"oc": oc, "accept_h1": 1 - oc, "asn": asn, "h": h}


def fixed_n_binomial(p0: float, p1: float, alpha: float, beta: float) -> dict:
    """The smallest n for which the one-sided exact binomial test of p0 at level alpha has power >= 1 - beta at p1."""
    for n in range(1, 20000):
        c = int(stats.binom.isf(alpha, n, p0)) + 1  # reject when S >= c
        while c > 0 and stats.binom.sf(c - 2, n, p0) <= alpha:
            c -= 1
        if stats.binom.sf(c - 1, n, p1) >= 1 - beta:
            return {"n": n, "c": c, "size": float(stats.binom.sf(c - 1, n, p0)), "power": float(stats.binom.sf(c - 1, n, p1))}
    raise ValueError("no n found")


def sprt_simulate(x, p0: float, p1: float, alpha: float, beta: float) -> dict:
    """Run the SPRT on one stream: the log-LR path and where it stopped."""
    x = np.asarray(x, float)
    a, b = math.log(p1 / p0), math.log((1 - p1) / (1 - p0))
    th = sprt_bounds(alpha, beta)
    llr = np.cumsum(np.where(x > 0.5, a, b))
    hit = np.flatnonzero((llr >= th["logA"]) | (llr <= th["logB"]))
    n = int(hit[0]) + 1 if len(hit) else len(x)
    return {"llr": llr, "n": n, "decision": int(llr[n - 1] >= th["logA"]) if len(hit) else -1}


# ----------------------------------------------------------------------------------- estimation after stopping


def stopped_mean_bias(theta: float, bounds, n_per_look: int, reps: int, rng: np.random.Generator) -> dict:
    """A group-sequential trial on N(theta, 1) data with z-boundaries ``bounds`` at K equally spaced looks: the
    sample mean at stopping is biased (upwards when the trial stops early for efficacy)."""
    K = len(bounds)
    Z = rng.standard_normal((reps, K, n_per_look)) + theta
    sums = np.cumsum(Z.sum(2), axis=1)
    ns = n_per_look * np.arange(1, K + 1)
    z = sums / np.sqrt(ns)
    crossed = np.abs(z) >= np.asarray(bounds)[None, :]
    crossed[:, -1] = True
    k = np.argmax(crossed, axis=1)
    mean = sums[np.arange(reps), k] / ns[k]
    early = k < K - 1
    return {"mean": float(mean.mean()), "bias": float(mean.mean() - theta), "bias_early": float(mean[early].mean() - theta) if early.any() else np.nan,
            "p_early": float(early.mean()), "stop_look": np.bincount(k, minlength=K) / reps}


# ------------------------------------------------------------------------------- test martingales and Ville


def normal_lr_martingale(x, mu1: float) -> np.ndarray:
    """The likelihood ratio of N(mu1, 1) against N(0, 1): a nonnegative martingale with mean one under the null."""
    x = np.asarray(x, float)
    return np.exp(np.cumsum(mu1 * x - mu1 * mu1 / 2))


def ville_check(n: int, mu1: float, alpha: float, reps: int, rng: np.random.Generator) -> dict:
    """Under N(0, 1) data, P(sup_t M_t >= 1/alpha) <= alpha (Ville); the fixed-n z-test checked after every
    observation rejects far more often."""
    X = rng.standard_normal((reps, n))
    logM = np.cumsum(mu1 * X - mu1 * mu1 / 2, axis=1)
    ville = float(np.mean(logM.max(1) >= math.log(1 / alpha)))
    z = np.cumsum(X, 1) / np.sqrt(np.arange(1, n + 1))
    crit = stats.norm.isf(alpha / 2)
    peek = float(np.mean(np.abs(z).max(1) >= crit))
    return {"ville": ville, "peek": peek, "end_only": float(np.mean(np.abs(z[:, -1]) >= crit))}


def peeking_curve(ns, alpha: float, reps: int, rng: np.random.Generator) -> np.ndarray:
    """P(the two-sided z-test rejects at some look t <= n, looking after every observation), for each n in ns."""
    n_max = int(max(ns))
    X = rng.standard_normal((reps, n_max))
    z = np.abs(np.cumsum(X, 1) / np.sqrt(np.arange(1, n_max + 1)))
    crit = stats.norm.isf(alpha / 2)
    run = np.maximum.accumulate(z >= crit, axis=1)
    return np.array([run[:, int(n) - 1].mean() for n in ns])


# --------------------------------------------------------------------------------------------------- e-values


def calibrate_p_to_e(p, kappa: float = 0.5):
    """Vovk & Wang's calibrator e = kappa p^(kappa - 1): integrates to one over p in [0, 1], so a valid p-value becomes
    an e-value."""
    p = np.asarray(p, float)
    return kappa * p ** (kappa - 1)


def calibrate_e_to_p(e):
    """Markov's inequality: p = min(1, 1/e) is a valid p-value for any e-value."""
    return np.minimum(1.0, 1.0 / np.asarray(e, float))


def merge_e(es, how: str = "mean"):
    """The arithmetic mean of e-values is an e-value under any dependence; the product is one for independent
    (or sequentially valid) e-values."""
    es = np.asarray(es, float)
    return float(es.mean()) if how == "mean" else float(np.prod(es))


def ebh(e, alpha: float) -> dict:
    """e-BH (Wang & Ramdas 2022): reject the k* largest e-values, k* = max{k: e_(k) >= m/(alpha k)}.  Controls the
    FDR at alpha under arbitrary dependence."""
    e = np.asarray(e, float)
    m = len(e)
    o = np.argsort(-e)
    ks = np.arange(1, m + 1)
    ok = np.flatnonzero(e[o] >= m / (alpha * ks))
    k = int(ok.max()) + 1 if len(ok) else 0
    rej = np.zeros(m, bool)
    rej[o[:k]] = True
    return {"k": k, "reject": rej}


def split_lrt_normal_mean(x, rng: np.random.Generator) -> float:
    """Universal inference (Wasserman, Ramdas & Balakrishnan 2020) for H0: mu = 0 in N(mu, sigma^2), sigma unknown:
    fit (mu, sigma) on half D0, and divide the D1-likelihood at that fit by the D1-likelihood maximized over the null
    (mu = 0, sigma free).  The ratio is an e-value: E_H0 <= 1."""
    x = np.asarray(x, float)
    o = rng.permutation(len(x))
    d0, d1 = x[o[: len(x) // 2]], x[o[len(x) // 2:]]
    mu, sd = d0.mean(), d0.std() + 1e-12
    s0 = math.sqrt(np.mean(d1 ** 2)) + 1e-12
    num = stats.norm.logpdf(d1, mu, sd).sum()
    den = stats.norm.logpdf(d1, 0, s0).sum()
    return float(math.exp(min(700.0, num - den)))


# ------------------------------------------------------------------------------------- confidence sequences


def normal_mixture_cs(xbar, t, alpha: float, tau2: float = 1.0, sigma: float = 1.0):
    """Robbins's normal mixture: mixing exp(lam S_t - lam^2 t/2) over lam ~ N(0, tau2) gives the martingale
    (1 + t tau2)^(-1/2) exp(tau2 S_t^2/(2(1 + t tau2))); Ville turns it into the time-uniform two-sided CS
    |xbar_t - mu| <= sigma sqrt((1 + t tau2)(log(1 + t tau2) + 2 log(1/alpha)))/(t sqrt(tau2))."""
    t = np.asarray(t, float)
    w = sigma * np.sqrt((1 + t * tau2) * (np.log(1 + t * tau2) + 2 * math.log(1 / alpha))) / (t * math.sqrt(tau2))
    return np.asarray(xbar) - w, np.asarray(xbar) + w


def stitched_boundary(t, alpha: float, two_sided: bool = False):
    """Howard, Ramdas, McAuliffe & Sekhon (2021, eq. 11): for sums of independent zero-mean 1-sub-Gaussian
    increments, P(exists t >= 1: S_t >= 1.7 sqrt(t (log log(2t) + 0.72 log(5.2/alpha)))) <= alpha: the LIL rate.
    Two-sided (their eq. 2, a confidence sequence for the mean): 5.2 becomes 10.4."""
    t = np.asarray(t, float)
    c = 10.4 if two_sided else 5.2
    return 1.7 * np.sqrt(t * (np.log(np.log(2 * t)) + 0.72 * math.log(c / alpha)))


def hoeffding_fixed(xbar, t, alpha: float):
    """Hoeffding's interval for [0, 1] data at a fixed n: xbar +- sqrt(log(2/alpha)/(2n)).  Valid at one n only."""
    t = np.asarray(t, float)
    w = np.sqrt(math.log(2 / alpha) / (2 * t))
    return np.asarray(xbar) - w, np.asarray(xbar) + w


def hoeffding_union(xbar, t, alpha: float):
    """Hoeffding made time-uniform by a union bound with alpha_t = alpha 6/(pi^2 t^2): valid, but wider by a log t."""
    t = np.asarray(t, float)
    at = alpha * 6 / (math.pi ** 2 * t ** 2)
    w = np.sqrt(np.log(2 / at) / (2 * t))
    return np.asarray(xbar) - w, np.asarray(xbar) + w


def betting_cs(x, alpha: float, grid=None, c: float = 0.5) -> dict:
    """The hedged betting confidence sequence of Waudby-Smith & Ramdas (2024) for the mean of [0, 1] data.  For each
    candidate m, two gamblers bet on X_t > m and X_t < m with predictable bets lam_t (the aGRAPA-like plug-in
    lam_t = sqrt(2 log(2/alpha)/(t_hat var_hat_{t-1} log(t + 1))), truncated at c/m and c/(1 - m)); m leaves the set when
    the average of their capitals reaches 1/alpha.  The running intersection is reported."""
    x = np.asarray(x, float)
    T = len(x)
    grid = np.linspace(0.001, 0.999, 999) if grid is None else np.asarray(grid, float)
    # predictable plug-in mean and variance
    cs = np.cumsum(x)
    cs2 = np.cumsum((x - 0) ** 2)
    t = np.arange(1, T + 1)
    mu_hat = np.r_[0.5, (0.5 + cs[:-1]) / (t[:-1] + 1)]
    var_hat = np.r_[0.25, (0.25 + np.cumsum((x[:-1] - mu_hat[:-1]) ** 2)) / (t[:-1] + 1)]
    lam = np.sqrt(2 * math.log(2 / alpha) / (var_hat * t * np.log(t + 1)))
    logKp = np.zeros(len(grid))
    logKm = np.zeros(len(grid))
    lo, hi = np.zeros(T), np.zeros(T)
    alive = np.ones(len(grid), bool)
    for i in range(T):
        lp = np.minimum(lam[i], c / grid)
        lm = np.minimum(lam[i], c / (1 - grid))
        logKp += np.log1p(lp * (x[i] - grid))
        logKm += np.log1p(-lm * (x[i] - grid))
        K = 0.5 * (np.exp(np.minimum(logKp, 700)) + np.exp(np.minimum(logKm, 700)))
        alive &= K < 1 / alpha
        idx = np.flatnonzero(alive)
        lo[i], hi[i] = (grid[idx[0]], grid[idx[-1]]) if len(idx) else (np.nan, np.nan)
    del cs2
    return {"lo": lo, "hi": hi}


def cs_coverage(make_cs, sampler, T: int, reps: int, mu: float, rng: np.random.Generator, t_min: int = 1) -> dict:
    """Time-uniform coverage: the fraction of streams whose interval contains mu at every t in [t_min, T], and the
    coverage at the final time alone."""
    always = final = 0
    for _ in range(reps):
        x = sampler(rng, T)
        lo, hi = make_cs(x)
        ok = ((lo <= mu) & (mu <= hi))[t_min - 1:]
        always += bool(ok.all())
        final += bool(ok[-1])
    return {"uniform": always / reps, "final": final / reps}


# ------------------------------------------------------------------------------------------ change detection


def cusum(x, mu0: float, mu1: float, h: float) -> dict:
    """Page's CUSUM for a shift in a normal mean from mu0 to mu1 (unit variance): W_t = max(0, W_{t-1} + log LR_t);
    alarm when W_t >= h."""
    x = np.asarray(x, float)
    inc = (mu1 - mu0) * (x - (mu0 + mu1) / 2)
    W = np.zeros(len(x))
    w = 0.0
    alarm = -1
    for i, v in enumerate(inc):
        w = max(0.0, w + v)
        W[i] = w
        if alarm < 0 and w >= h:
            alarm = i
    return {"W": W, "alarm": alarm}


def cusum_arl(mu: float, mu0: float, mu1: float, h: float, reps: int, rng: np.random.Generator, t_max: int = 200_000) -> float:
    """Average run length to alarm when the data are N(mu, 1) from the start (mu = mu0: the false-alarm ARL)."""
    out = np.empty(reps)
    for r in range(reps):
        w, t = 0.0, 0
        while t < t_max:
            chunk = rng.standard_normal(4096) + mu
            inc = (mu1 - mu0) * (chunk - (mu0 + mu1) / 2)
            hit = -1
            for i, v in enumerate(inc):
                w = max(0.0, w + v)
                if w >= h:
                    hit = i
                    break
            if hit >= 0:
                t += hit + 1
                break
            t += len(chunk)
        out[r] = t
    return float(out.mean())


def bocpd_normal(x, hazard: float, mu0: float = 0.0, kappa0: float = 1.0, sigma: float = 1.0) -> np.ndarray:
    """Adams & MacKay's Bayesian online changepoint detection for a normal mean with known sigma and a N(mu0,
    sigma^2/kappa0) prior on each segment's mean: the posterior over the run length, R[t, r]."""
    x = np.asarray(x, float)
    T = len(x)
    R = np.zeros((T + 1, T + 1))
    R[0, 0] = 1.0
    mu = np.array([mu0])
    kap = np.array([kappa0])
    for t in range(T):
        pred_sd = sigma * np.sqrt(1 + 1 / kap)
        pi = stats.norm.pdf(x[t], mu, pred_sd)
        growth = R[t, : t + 1] * pi * (1 - hazard)
        cp = np.sum(R[t, : t + 1] * pi * hazard)
        R[t + 1, 1: t + 2] = growth
        R[t + 1, 0] = cp
        R[t + 1] /= R[t + 1].sum()
        mu_new = (kap * mu + x[t]) / (kap + 1)
        mu = np.r_[mu0, mu_new]
        kap = np.r_[kappa0, kap + 1]
    return R


# ----------------------------------------------------------------------------------------- adaptive experiments


def thompson_bernoulli(means, T: int, rng: np.random.Generator, floor: float = 0.0, n_mc: int = 200) -> dict:
    """Thompson sampling with Beta(1, 1) priors on K Bernoulli arms.  Assignment probabilities e_t(k) are estimated by
    n_mc posterior draws and floored at ``floor`` (renormalized), so they are known for the inference that follows."""
    means = np.asarray(means, float)
    K = len(means)
    a, b = np.ones(K), np.ones(K)
    arms = np.empty(T, int)
    ys = np.empty(T)
    probs = np.empty((T, K))
    for t in range(T):
        draws = rng.beta(a[None, :], b[None, :], (n_mc, K))
        e = np.bincount(np.argmax(draws, 1), minlength=K) / n_mc
        if floor > 0:
            e = np.maximum(e, floor)
            e = e / e.sum()
        k = rng.choice(K, p=e)
        y = float(rng.random() < means[k])
        arms[t], ys[t], probs[t] = k, y, e
        a[k] += y
        b[k] += 1 - y
    return {"arm": arms, "y": ys, "e": probs}


def aipw_scores(arm, y, e, K: int) -> np.ndarray:
    """Per-step AIPW scores Gamma_t(k) = m_{t-1}(k) + 1{A_t = k}(Y_t - m_{t-1}(k))/e_t(k), with m_{t-1} the running
    arm mean (predictable)."""
    arm, y, e = np.asarray(arm), np.asarray(y, float), np.asarray(e, float)
    T = len(arm)
    G = np.zeros((T, K))
    s, n = np.zeros(K), np.zeros(K)
    for t in range(T):
        m = np.where(n > 0, s / np.maximum(n, 1), 0.5)
        G[t] = m
        k = arm[t]
        G[t, k] += (y[t] - m[k]) / e[t, k]
        s[k] += y[t]
        n[k] += 1
    return G


def arm_estimates(arm, y, e, K: int, alpha: float = 0.05) -> dict:
    """Three estimates of each arm's mean after an adaptive experiment: the sample mean with its naive interval;
    the unweighted AIPW mean; and Hadad et al.'s adaptively weighted AIPW with variance-stabilizing weights
    h_t = sqrt(e_t(k)), whose studentized statistic is asymptotically normal."""
    G = aipw_scores(arm, y, e, K)
    e = np.asarray(e, float)
    z = stats.norm.isf(alpha / 2)
    out = {}
    for k in range(K):
        m = np.asarray(arm) == k
        nk = m.sum()
        mean = float(np.mean(np.asarray(y)[m])) if nk else np.nan
        se = math.sqrt(max(mean * (1 - mean), 1e-12) / max(nk, 1))
        h = np.sqrt(e[:, k])
        Q = float(np.sum(h * G[:, k]) / h.sum())
        se_w = float(math.sqrt(np.sum(h ** 2 * (G[:, k] - Q) ** 2)) / h.sum())
        out[k] = {"n": int(nk), "naive": mean, "naive_lo": mean - z * se, "naive_hi": mean + z * se,
                  "aipw": float(G[:, k].mean()), "aw": Q, "aw_lo": Q - z * se_w, "aw_hi": Q + z * se_w}
    return out


def policy_value(y, arm, e, target_probs, mhat=None) -> dict:
    """Off-policy evaluation of a target policy pi from logged data (A_t, Y_t) with logging probabilities e_t:
    IPW = mean(pi(A_t) Y_t / e_t(A_t)); doubly robust = mean(sum_k pi(k) m(k) + pi(A_t)(Y_t - m(A_t))/e_t(A_t))."""
    y, arm = np.asarray(y, float), np.asarray(arm)
    e, P = np.asarray(e, float), np.asarray(target_probs, float)
    T = len(y)
    w = P[np.arange(T), arm] / e[np.arange(T), arm]
    ipw = w * y
    out = {"ipw": float(ipw.mean()), "ipw_se": float(ipw.std(ddof=1) / math.sqrt(T))}
    if mhat is not None:
        M = np.asarray(mhat, float)
        M = np.broadcast_to(M, P.shape)
        dr = np.sum(P * M, 1) + w * (y - M[np.arange(T), arm])
        out |= {"dr": float(dr.mean()), "dr_se": float(dr.std(ddof=1) / math.sqrt(T))}
    return out


def lil_rate(t):
    """sqrt(2 t log log t): the law of the iterated logarithm's envelope, for comparison with boundaries."""
    t = np.asarray(t, float)
    return np.sqrt(2 * t * np.log(np.log(np.maximum(t, 3))))


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("math", "np", "special", "stats", "annotations")]
