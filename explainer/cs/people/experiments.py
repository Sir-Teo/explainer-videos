"""Controlled experiments (Part 44): the two-proportion z-test, power and sample size, the peeking problem, an
always-valid sequential test (mixture SPRT, Johari et al. 2017), CUPED variance reduction (Deng et al. 2013), false
discovery rates, sample-ratio mismatch, Simpson's paradox, and bandits against fixed A/B splits."""

from __future__ import annotations

import math
import random

import numpy as np


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def z_test(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    p = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se if se else 0.0
    return z, 2 * (1 - phi(abs(z)))


def sample_size(p, lift, alpha=0.05, power=0.8):
    """Per arm, for a relative lift on a base rate p: n = (z_{1-a/2} + z_{power})^2 * 2 p(1-p) / delta^2, which is
    about 16 sigma^2 / delta^2 at alpha 0.05 and power 0.8 (since (1.96 + 0.84)^2 * 2 = 15.7)."""
    za, zb = 1.959964, 0.841621
    d = p * lift
    exact = (za + zb) ** 2 * 2 * p * (1 - p) / d ** 2
    rule = 16 * p * (1 - p) / d ** 2
    return {"p": p, "lift": lift, "delta": d, "n_per_arm": exact, "rule_16": rule}


def power_sim(p=0.05, lift=0.05, n=None, trials=2000, seed=0):
    rng = np.random.default_rng(seed)
    n = int(n or sample_size(p, lift)["n_per_arm"])
    a = rng.binomial(n, p, trials)
    b = rng.binomial(n, p * (1 + lift), trials)
    hits = sum(1 for x1, x2 in zip(a, b) if z_test(x1, n, x2, n)[1] < 0.05)
    return {"n": n, "power": hits / trials}


def peeking(days=30, per_day=1000, p=0.05, trials=2000, seed=1):
    """A/A tests (no real difference) checked every day, stopping at the first p < 0.05: the false-positive rate
    climbs far above 5%.  Also returns a few p-value paths for drawing."""
    rng = np.random.default_rng(seed)
    a = rng.binomial(per_day, p, (trials, days)).cumsum(axis=1)
    b = rng.binomial(per_day, p, (trials, days)).cumsum(axis=1)
    stopped = np.zeros(trials, bool)
    fpr_by_day = []
    paths = []
    for d in range(days):
        n = per_day * (d + 1)
        pp = (a[:, d] + b[:, d]) / (2 * n)
        se = np.sqrt(pp * (1 - pp) * 2 / n)
        z = (b[:, d] - a[:, d]) / n / se
        pv = 2 * (1 - 0.5 * (1 + np.vectorize(math.erf)(np.abs(z) / math.sqrt(2))))
        stopped |= pv < 0.05
        fpr_by_day.append(float(stopped.mean()))
        paths.append(pv[:6].tolist())
    final_only = float(((lambda pv: pv < 0.05)(pv)).mean())
    return {"days": days, "per_day": per_day, "fpr_peeking": fpr_by_day, "fpr_final_only": final_only,
            "paths": [list(x) for x in zip(*paths)]}


def msprt(days=30, per_day=1000, p=0.05, lift=0.0, tau2=None, alpha=0.05, trials=2000, seed=2):
    """Mixture sequential probability ratio test for a difference in means (normal approximation, Johari et al.):
    with a N(0, tau^2) mixture over effects, the likelihood ratio after n per arm is
    sqrt(V/(V + n tau^2)) exp(n^2 tau^2 d^2 / (2 V (V + n tau^2))), with V = 2 p(1-p) the variance of one paired
    difference and d the observed difference.  Rejecting when it exceeds 1/alpha is valid however often one looks."""
    rng = np.random.default_rng(seed)
    V = 2 * p * (1 - p)
    tau2 = tau2 if tau2 is not None else (p * 0.05) ** 2
    a = rng.binomial(per_day, p, (trials, days)).cumsum(axis=1)
    b = rng.binomial(per_day, p * (1 + lift), (trials, days)).cumsum(axis=1)
    rejected = np.zeros(trials, bool)
    when = np.full(trials, -1)
    for dd in range(days):
        n = per_day * (dd + 1)
        d = (b[:, dd] - a[:, dd]) / n
        lr = np.sqrt(V / (V + n * tau2)) * np.exp(n * n * tau2 * d * d / (2 * V * (V + n * tau2)))
        new = (lr > 1 / alpha) & ~rejected
        when[new] = dd + 1
        rejected |= new
    return {"lift": lift, "rejected": float(rejected.mean()),
            "median_day": float(np.median(when[when > 0])) if (when > 0).any() else None}


def cuped(n=20_000, rho=0.7, effect=0.02, trials=400, seed=3):
    """Each user has a pre-period metric X correlated rho with the in-experiment metric Y.  The CUPED estimator
    Y - theta (X - mean X), theta = cov(X, Y)/var(X), has variance (1 - rho^2) times the plain one."""
    rng = np.random.default_rng(seed)
    plain, adj = [], []
    for _ in range(trials):
        x = rng.normal(0, 1, 2 * n)
        y = rho * x + math.sqrt(1 - rho * rho) * rng.normal(0, 1, 2 * n)
        t = np.r_[np.zeros(n), np.ones(n)].astype(bool)
        y = y + effect * t
        plain.append(y[t].mean() - y[~t].mean())
        theta = np.cov(x, y)[0, 1] / x.var()
        ya = y - theta * (x - x.mean())
        adj.append(ya[t].mean() - ya[~t].mean())
    vp, va = float(np.var(plain)), float(np.var(adj))
    return {"rho": rho, "var_plain": vp, "var_cuped": va, "ratio": va / vp, "theory": 1 - rho * rho,
            "ci_plain": 1.96 * math.sqrt(vp), "ci_cuped": 1.96 * math.sqrt(va), "effect": effect}


def many_metrics(k=20, alpha=0.05, trials=5000, true_effects=0, seed=4):
    """k metrics, none really moved: the chance that at least one shows p < alpha, against Benjamini–Hochberg."""
    rng = np.random.default_rng(seed)
    any_naive = any_bh = 0
    for _ in range(trials):
        pv = rng.uniform(size=k)
        if (pv < alpha).any():
            any_naive += 1
        s = np.sort(pv)
        ok = s <= alpha * np.arange(1, k + 1) / k
        if ok.any():
            any_bh += 1
    return {"k": k, "naive": any_naive / trials, "theory": 1 - (1 - alpha) ** k, "bh": any_bh / trials}


def srm(n_a=50_000, n_b=49_000):
    """Sample-ratio mismatch: a 50/50 split that delivered these counts, by a chi-squared test with one degree of
    freedom."""
    n = n_a + n_b
    e = n / 2
    chi2 = (n_a - e) ** 2 / e + (n_b - e) ** 2 / e
    p = 2 * (1 - phi(math.sqrt(chi2)))
    return {"a": n_a, "b": n_b, "chi2": chi2, "p": p}


def simpson():
    """A redesign that wins on desktop and on mobile but loses overall, because the new version's traffic was mostly
    mobile, where everyone converts less (illustrative counts)."""
    data = {"old": {"desktop": (400, 4000), "mobile": (60, 2000)},
            "new": {"desktop": (90, 800), "mobile": (300, 5200)}}
    out = {}
    for v, segs in data.items():
        tot_x = sum(x for x, _ in segs.values())
        tot_n = sum(n for _, n in segs.values())
        out[v] = {s: x / n for s, (x, n) in segs.items()} | {"overall": tot_x / tot_n}
    return {"data": data, "rates": out}


def bandit(p=(0.050, 0.055), n=100_000, trials=200, seed=5):
    """Thompson sampling against a 50/50 split for the same traffic: conversions lost (regret) and how precisely each
    measures the difference."""
    rng = np.random.default_rng(seed)
    reg_ab, reg_ts, est_ab, est_ts = [], [], [], []
    best = max(p)
    for _ in range(trials):
        xa = rng.binomial(n // 2, p[0])
        xb = rng.binomial(n // 2, p[1])
        reg_ab.append(n * best - (xa + xb))
        est_ab.append(xb / (n // 2) - xa / (n // 2))
        s = np.ones(2)
        f = np.ones(2)
        pulls = np.zeros(2)
        wins = 0
        for _ in range(n // 500):            # update in batches of 500 visitors, as deployed systems do
            th = rng.beta(s, f, (500, 2))
            arm = th.argmax(axis=1)
            for k in (0, 1):
                m = int((arm == k).sum())
                w = rng.binomial(m, p[k])
                s[k] += w
                f[k] += m - w
                pulls[k] += m
                wins += w
        reg_ts.append(n * best - wins)
        est_ts.append((s[1] - 1) / max(1, pulls[1]) - (s[0] - 1) / max(1, pulls[0]))
    return {"p": p, "n": n, "regret_ab": float(np.mean(reg_ab)), "regret_ts": float(np.mean(reg_ts)),
            "sd_ab": float(np.std(est_ab)), "sd_ts": float(np.std(est_ts)), "true_diff": p[1] - p[0]}


def interference(buyers=10_000, supply=3_000, q=(0.30, 0.36), trials=200, seed=6):
    """A marketplace with limited supply: treatment makes buyers keener, but every item a treated buyer takes is one
    a control buyer cannot.  The A/B difference (half treated) against the true effect of launching to everyone
    (all treated against none)."""
    rng = np.random.default_rng(seed)

    def run(frac):
        treated = rng.random(buyers) < frac
        want = rng.random(buyers) < np.where(treated, q[1], q[0])
        order = rng.permutation(buyers)
        got = np.zeros(buyers, bool)
        left = supply
        for i in order:
            if left == 0:
                break
            if want[i]:
                got[i] = True
                left -= 1
        return treated, got
    ab, glob = [], []
    for _ in range(trials):
        t, g = run(0.5)
        ab.append(g[t].mean() - g[~t].mean())
        _, g1 = run(1.0)
        _, g0 = run(0.0)
        glob.append(g1.mean() - g0.mean())
    return {"buyers": buyers, "supply": supply, "q": q, "ab_estimate": float(np.mean(ab)),
            "true_global": float(np.mean(glob)), "unconstrained": q[1] - q[0]}


def randomized_response(true_rate=0.2, ns=(100, 1_000, 10_000, 100_000), p_truth=0.75, trials=400, seed=7):
    """Warner's randomized response (1965), the simplest local differential privacy: each person answers truthfully
    with probability p_truth and otherwise flips a fair coin.  Any one answer is deniable (epsilon = ln of the odds
    ratio), but the population rate is recovered as (observed - (1 - p)/2) / p, with more noise."""
    rng = np.random.default_rng(seed)
    eps = math.log((p_truth + (1 - p_truth) / 2) / ((1 - p_truth) / 2))
    rows = []
    for n in ns:
        errs_rr, errs_plain = [], []
        for _ in range(trials):
            truth = rng.random(n) < true_rate
            honest = rng.random(n) < p_truth
            coin = rng.random(n) < 0.5
            ans = np.where(honest, truth, coin)
            est = (ans.mean() - (1 - p_truth) / 2) / p_truth
            errs_rr.append(abs(est - true_rate))
            errs_plain.append(abs(truth.mean() - true_rate))
        rows.append({"n": n, "err_private": float(np.mean(errs_rr)), "err_plain": float(np.mean(errs_plain))})
    return {"true_rate": true_rate, "p_truth": p_truth, "epsilon": eps, "rows": rows}
