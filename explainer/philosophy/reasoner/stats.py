"""Statistical evidence, made computable (Part 16).

* p-values under the null and the alternative; the common misreadings, each refuted by simulation.
* The base-rate fallacy as a population grid; Ioannidis's positive predictive value from power, alpha and prior odds.
* A garden of forking paths: a p-hacking simulator that turns pure noise into "significant" results.
* Optional stopping: a fixed-alpha test checked after every batch under the null, against the likelihood ratio.
* Birnbaum's theorem on a toy mixture experiment: sufficiency plus conditionality give the likelihood principle.
* Lindley's paradox, computed: p < 0.05 while the Bayes factor favours the null; and the prior sensitivity of Bayes
  factors.
* Mayo's severity curves.
* Simpson's paradox on the six largest Berkeley departments (Bickel, Hammel and O'Connell 1975).
* Testing by betting: e-values, a test martingale, Ville's inequality checked by simulation, anytime validity.
* AIC and BIC (Forster and Sober 1994).
"""

from __future__ import annotations

import math
import random

import numpy as np

# ---------------------------------------------------------------------------
# Normal and t helpers (no scipy dependency)
# ---------------------------------------------------------------------------
SQRT2 = math.sqrt(2.0)


def phi(z: float) -> float:
    """Standard normal CDF."""
    return 0.5 * (1 + math.erf(z / SQRT2))


def p_two_sided(z: float) -> float:
    return 2 * (1 - phi(abs(z)))


def z_of_p(p: float) -> float:
    """Inverse of the two-sided p-value for a z statistic (bisection)."""
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if p_two_sided(mid) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the regularized incomplete beta (Numerical Recipes, 6.4)."""
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / d if abs(d) > 1e-300 else 1e300
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / d if abs(d) > 1e-300 else 1e300
        c = 1 + aa / c if abs(c) > 1e-300 else 1e300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / d if abs(d) > 1e-300 else 1e300
        c = 1 + aa / c if abs(c) > 1e-300 else 1e300
        de = d * c
        h *= de
        if abs(de - 1) < 1e-12:
            break
    return h


def betainc(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lbt) * _betacf(a, b, x) / a
    return 1 - math.exp(lbt) * _betacf(b, a, 1 - x) / b


def t_two_sided(t: float, df: float) -> float:
    """Two-sided p-value of Student's t."""
    return betainc(df / 2, 0.5, df / (df + t * t))


def t_test(a: np.ndarray, b: np.ndarray) -> float:
    """Student's two-sample t-test (pooled variance), two-sided p."""
    na, nb = len(a), len(b)
    sp = ((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2)
    t = (a.mean() - b.mean()) / math.sqrt(sp * (1 / na + 1 / nb))
    return t_two_sided(t, na + nb - 2)


def z_test(x: np.ndarray, sigma: float = 1.0) -> float:
    """Two-sided p-value for H0: mean 0, known sigma."""
    return p_two_sided(float(x.mean()) / (sigma / math.sqrt(len(x))))


# ---------------------------------------------------------------------------
# Three schools on one data set
# ---------------------------------------------------------------------------
def three_schools(heads: int = 60, n: int = 100, alt: float = 0.6, alpha: float = 0.05) -> dict:
    """60 heads in 100 tosses: is the coin fair? Fisher: the exact two-sided p-value. Neyman and Pearson: the
    level-alpha rejection region (exact binomial, symmetric), whether the data fall in it, and the power against
    p = alt. Bayes (Jeffreys): H0: p = 1/2 against H1: p uniform, the Bayes factor and the posterior of H0 at even
    prior odds."""
    from math import comb
    pmf = [comb(n, k) / 2 ** n for k in range(n + 1)]
    dev = abs(heads - n / 2)
    p_fisher = sum(pmf[k] for k in range(n + 1) if abs(k - n / 2) >= dev)
    # smallest c with P(|X - n/2| >= c) <= alpha
    c = next(c for c in range(0, n // 2 + 1) if sum(pmf[k] for k in range(n + 1) if abs(k - n / 2) >= c) <= alpha)
    size = sum(pmf[k] for k in range(n + 1) if abs(k - n / 2) >= c)
    power = sum(comb(n, k) * alt ** k * (1 - alt) ** (n - k) for k in range(n + 1) if abs(k - n / 2) >= c)
    bf01 = pmf[heads] * (n + 1)      # marginal under uniform prior is 1/(n+1)
    return {"heads": heads, "n": n, "p_fisher": p_fisher, "critical": c, "reject_below": int(n / 2 - c),
            "reject_above": int(n / 2 + c), "size": size, "reject": dev >= c, "power": power, "alt": alt,
            "bf01": bf01, "post_null": bf01 / (1 + bf01)}


def sellke_bound(p: float) -> float:
    """Sellke, Bayarri and Berger (2001): for p < 1/e, the Bayes factor in favour of the null is at least
    -e p ln p, under any reasonable alternative."""
    return -math.e * p * math.log(p)


# ---------------------------------------------------------------------------
# p-values and their misreadings
# ---------------------------------------------------------------------------
def p_distribution(n: int = 20, effect: float = 0.5, sims: int = 100000, seed: int = 1925) -> dict:
    """p-values of a z-test (n per study) under the null (effect 0) and under an alternative: uniform under the null,
    piled near 0 under the alternative. Histograms on 20 bins of [0, 1]."""
    rng = np.random.default_rng(seed)
    se = 1 / math.sqrt(n)
    z0 = rng.normal(0, 1, sims)
    z1 = rng.normal(effect / se, 1, sims)
    p0 = np.array([p_two_sided(z) for z in z0])
    p1 = np.array([p_two_sided(z) for z in z1])
    bins = np.linspace(0, 1, 21)
    return {"n": n, "effect": effect, "null_hist": np.histogram(p0, bins)[0].tolist(),
            "alt_hist": np.histogram(p1, bins)[0].tolist(), "null_below_05": float((p0 < 0.05).mean()),
            "power": float((p1 < 0.05).mean()), "sims": sims}


def misreadings(seed: int = 2016) -> dict:
    """Each common misreading of p (Greenland et al. 2016; the ASA statement), refuted by a simulation:

    1. 'p is the probability the null is true': among studies with p in [0.04, 0.05], the share of true nulls
       depends on the prior share of nulls (here 50% and 90%), and is far from 0.05.
    2. 'p > 0.05 means no effect': with a real effect and low power, most studies give p > 0.05.
    3. 'a smaller p means a bigger effect': a tiny effect in a huge sample gives a smaller p than a large effect in a
       small one.
    4. 'p = 0.05 means a 5% chance of a false positive': the false discovery rate among significant results depends
       on the base rate and power (see ppv).
    5. 'p is the probability the result is due to chance': under the null, p is uniform, whatever 'chance' means.
    6. 'two studies, p = 0.03 and p = 0.07, disagree': their estimates can be nearly identical.
    """
    rng = np.random.default_rng(seed)
    out = {}
    n, effect, sims = 25, 0.4, 200000
    se = 1 / math.sqrt(n)
    for share_null in (0.5, 0.9):
        null = rng.random(sims) < share_null
        z = rng.normal(np.where(null, 0.0, effect / se), 1.0)
        p = 2 * (1 - 0.5 * (1 + np.vectorize(math.erf)(np.abs(z) / SQRT2)))
        band = (p > 0.04) & (p < 0.05)
        out[f"null_given_p_near_05_{int(share_null * 100)}"] = float(null[band].mean())
    # 2. low power
    z = rng.normal(0.2 / (1 / math.sqrt(20)), 1.0, 50000)
    p = 2 * (1 - 0.5 * (1 + np.vectorize(math.erf)(np.abs(z) / SQRT2)))
    out["real_effect_p_above_05"] = float((p > 0.05).mean())
    # 3. effect size vs p
    out["tiny_effect_huge_n"] = {"effect": 0.02, "n": 100000, "p": p_two_sided(0.02 * math.sqrt(100000))}
    out["big_effect_small_n"] = {"effect": 0.8, "n": 10, "p": p_two_sided(0.8 * math.sqrt(10))}
    # 6. two studies
    se6 = 0.1
    out["two_studies"] = {"est_a": 2.17 * se6, "p_a": p_two_sided(2.17), "est_b": 1.81 * se6,
                          "p_b": p_two_sided(1.81), "se": se6,
                          "diff_p": p_two_sided((2.17 - 1.81) * se6 / (se6 * math.sqrt(2)))}
    return out


def ci_coverage(n: int = 20, reps: int = 100, mu: float = 0.0, seed: int = 1937) -> dict:
    """Neyman's confidence intervals (1937): 95% intervals xbar +/- 1.96 / sqrt(n) from ``reps`` samples; how many
    cover the true mean. The '95%' belongs to the procedure; each interval either covers or not."""
    rng = np.random.default_rng(seed)
    half = 1.959964 / math.sqrt(n)
    rows = []
    for _ in range(reps):
        xb = float(rng.normal(mu, 1, n).mean())
        rows.append({"lo": xb - half, "hi": xb + half, "covers": xb - half <= mu <= xb + half})
    big = rng.normal(mu, 1 / math.sqrt(n), 100000)
    return {"n": n, "reps": reps, "intervals": rows, "covered": sum(r["covers"] for r in rows),
            "long_run": float((np.abs(big - mu) <= half).mean())}


def winners_curse(effect: float = 0.2, ns=(20, 50, 100, 400), sims: int = 40000, seed: int = 2014) -> dict:
    """Gelman and Carlin (2014): type S (sign) and type M (magnitude) errors. Two groups of n with a true standardized
    difference ``effect``; among results with p < 0.05, the average exaggeration |estimate| / effect and the share
    with the wrong sign, for several sample sizes (powers)."""
    rng = np.random.default_rng(seed)
    out = []
    for n in ns:
        se = math.sqrt(2 / n)
        est = rng.normal(effect, se, sims)
        sig = np.abs(est / se) > 1.959964
        out.append({"n": n, "power": float(sig.mean()), "exaggeration": float(np.abs(est[sig]).mean() / effect),
                    "wrong_sign": float((est[sig] < 0).mean())})
    return {"effect": effect, "rows": out}


# ---------------------------------------------------------------------------
# Base rates and positive predictive value
# ---------------------------------------------------------------------------
def base_rate(prevalence: float = 0.01, sensitivity: float = 0.9, false_positive: float = 0.09,
              population: int = 1000) -> dict:
    """A screening test on a population: counts of true and false positives, and the positive predictive value."""
    sick = round(population * prevalence)
    healthy = population - sick
    tp = round(sick * sensitivity)
    fp = round(healthy * false_positive)
    return {"population": population, "sick": sick, "healthy": healthy, "tp": tp, "fn": sick - tp, "fp": fp,
            "tn": healthy - fp, "ppv": tp / (tp + fp),
            "ppv_exact": prevalence * sensitivity / (prevalence * sensitivity + (1 - prevalence) * false_positive)}


def ppv(power: float, alpha: float, prior_odds: float, bias: float = 0.0) -> float:
    """Ioannidis (2005): the probability that a 'significant' finding is true, with pre-study odds R, and bias u
    (the share of analyses that would not have been significant but are reported as such)."""
    R, b, u = prior_odds, 1 - power, bias
    num = (1 - b) * R + u * b * R
    den = R + alpha - b * R + u - u * alpha + u * b * R
    return num / den


def ioannidis_table() -> list[dict]:
    """Ioannidis's Table 4, recomputed: practical examples of PPV."""
    rows = [("adequately powered RCT, little bias, 1:1 pre-study odds", 0.80, 1.0, 0.10),
            ("confirmatory meta-analysis of good-quality RCTs", 0.95, 2.0, 0.30),
            ("meta-analysis of small inconclusive studies", 0.80, 1 / 3, 0.40),
            ("underpowered, well-performed phase I/II RCT", 0.20, 1 / 5, 0.20),
            ("underpowered, poorly performed phase I/II RCT", 0.20, 1 / 5, 0.80),
            ("adequately powered exploratory epidemiological study", 0.80, 1 / 10, 0.30),
            ("underpowered exploratory epidemiological study", 0.20, 1 / 10, 0.30),
            ("discovery-oriented exploratory research, massive testing", 0.20, 1 / 1000, 0.80)]
    return [{"what": w, "power": pw, "odds": R, "bias": u, "ppv": ppv(pw, 0.05, R, u)} for w, pw, R, u in rows]


# ---------------------------------------------------------------------------
# The garden of forking paths
# ---------------------------------------------------------------------------
def garden(studies: int = 4000, n: int = 20, seed: int = 2011) -> dict:
    """Simmons, Nelson and Simonsohn (2011), in miniature. Every study is pure noise: two conditions of n subjects,
    two correlated outcome measures (r = 0.5), and each subject's gender. The researcher may (a) report either
    outcome or their average; (b) if not yet significant, add 10 more per condition and test again; (c) use gender: test within
    men and within women, or control for it; (d) drop the most extreme observation. Student's t throughout. Share
    of studies with some p < 0.05, for each freedom alone and all together."""
    rng = np.random.default_rng(seed)
    cov = np.array([[1, 0.5], [0.5, 1]])

    def tests(A, B, ga, gb, flags):
        outs = [(A[:, 0], B[:, 0])]
        if flags["a"]:
            outs += [(A[:, 1], B[:, 1]), (A.mean(axis=1), B.mean(axis=1))]
        ps = []
        for a, b in outs:
            ps.append(t_test(a, b))
            if flags["c"]:
                for g in (0, 1):
                    sa, sb = a[ga == g], b[gb == g]
                    if len(sa) > 2 and len(sb) > 2:
                        ps.append(t_test(sa, sb))
                # control for gender: remove each gender's mean
                ya, yb = a.copy(), b.copy()
                for g in (0, 1):
                    mu = np.concatenate([a[ga == g], b[gb == g]]).mean()
                    ya[ga == g] -= mu
                    yb[gb == g] -= mu
                ps.append(t_test(ya, yb))
            if flags["d"]:
                y = np.concatenate([a, b])
                k = int(np.argmax(np.abs(y - y.mean())))
                ps.append(t_test(np.delete(a, k), b) if k < len(a) else t_test(a, np.delete(b, k - len(a))))
        return min(ps)

    def one(flags):
        A = rng.multivariate_normal([0, 0], cov, n + 10)
        B = rng.multivariate_normal([0, 0], cov, n + 10)
        ga, gb = rng.integers(0, 2, n + 10), rng.integers(0, 2, n + 10)
        p = tests(A[:n], B[:n], ga[:n], gb[:n], flags)
        if p < 0.05:
            return True
        if flags["b"]:
            return bool(tests(A, B, ga, gb, flags) < 0.05)
        return False

    combos = [("none", {}), ("two outcomes", {"a": 1}), ("+ 10 more per group", {"b": 1}),
              ("gender: subgroups, or control", {"c": 1}), ("drop an outlier", {"d": 1}),
              ("all four", {"a": 1, "b": 1, "c": 1, "d": 1})]
    out = []
    for name, f in combos:
        flags = {k: bool(f.get(k)) for k in "abcd"}
        hits = sum(bool(one(flags)) for _ in range(studies))
        out.append({"freedom": name, "rate": hits / studies})
    return {"studies": studies, "n": n, "rows": out}


def garden_paths(seed: int = 0, n: int = 20) -> dict:
    """One pure-noise data set, every path through the garden: outcome (DV1, DV2, their mean) x sample (20 or 30
    per condition) x gender (all, men only, women only, controlled) x outliers (keep, drop the most extreme): 48
    analyses, 48 p-values."""
    rng = np.random.default_rng(seed)
    cov = np.array([[1, 0.5], [0.5, 1]])
    A = rng.multivariate_normal([0, 0], cov, n + 10)
    B = rng.multivariate_normal([0, 0], cov, n + 10)
    ga, gb = rng.integers(0, 2, n + 10), rng.integers(0, 2, n + 10)
    paths = []
    for oi, oname in enumerate(("DV1", "DV2", "mean")):
        for m in (n, n + 10):
            a0 = A[:m, oi] if oi < 2 else A[:m].mean(axis=1)
            b0 = B[:m, oi] if oi < 2 else B[:m].mean(axis=1)
            xa, xb = ga[:m], gb[:m]
            for gname in ("all", "men", "women", "controlled"):
                if gname == "all":
                    a, b = a0, b0
                elif gname in ("men", "women"):
                    g = 0 if gname == "men" else 1
                    a, b = a0[xa == g], b0[xb == g]
                else:
                    a, b = a0.copy(), b0.copy()
                    for g in (0, 1):
                        mu = np.concatenate([a0[xa == g], b0[xb == g]]).mean()
                        a[xa == g] -= mu
                        b[xb == g] -= mu
                for drop in (False, True):
                    aa, bb = a, b
                    if drop:
                        y = np.concatenate([a, b])
                        k = int(np.argmax(np.abs(y - y.mean())))
                        aa, bb = (np.delete(a, k), b) if k < len(a) else (a, np.delete(b, k - len(a)))
                    paths.append({"outcome": oname, "n": m, "gender": gname, "drop": drop,
                                  "p": t_test(aa, bb)})
    return {"seed": seed, "paths": paths, "default_p": paths[0]["p"],
            "significant": sum(q["p"] < 0.05 for q in paths), "min_p": min(q["p"] for q in paths)}


# ---------------------------------------------------------------------------
# Optional stopping
# ---------------------------------------------------------------------------
def optional_stopping(runs: int = 2000, max_n: int = 1000, check_every: int = 10, seed: int = 1961) -> dict:
    """Under the null (mean 0, sd 1), test after every ``check_every`` observations and stop at the first p < 0.05.
    The share of runs that ever 'reject' grows with the number of looks (toward 1, by the law of the iterated
    logarithm). One p-value path is kept for drawing. A likelihood-ratio stopper (stop when LR(mu = 0.3 : mu = 0)
    reaches 10) checked at the same looks errs at most 1 time in 10, however long it looks (Ville; Royall)."""
    rng = np.random.default_rng(seed)
    looks = list(range(check_every, max_n + 1, check_every))
    ever = np.zeros(len(looks))
    path = None
    lr_at_stop = []
    lr_paths_ge_10 = 0
    for r in range(runs):
        x = rng.normal(0, 1, max_n)
        cs = np.cumsum(x)
        rejected = False
        first = None
        ps = []
        for j, m in enumerate(looks):
            z = cs[m - 1] / math.sqrt(m)
            p = p_two_sided(z)
            ps.append(p)
            if p < 0.05 and not rejected:
                rejected = True
                first = m
                ever[j:] += 1
                mu = 0.3
                lr_at_stop.append(math.exp(mu * cs[m - 1] - m * mu * mu / 2))
        if not rejected:
            m = max_n
            lr_at_stop.append(math.exp(0.3 * cs[m - 1] - m * 0.09 / 2))
        if path is None and rejected and first >= 400:
            path = ps
        # a likelihood-ratio stopper: stop when LR(0.3 : 0) >= 10, at any look
        lr = np.exp(0.3 * cs[np.array(looks) - 1] - np.array(looks) * 0.09 / 2)
        lr_paths_ge_10 += bool((lr >= 10).any())
    return {"looks": looks, "ever_rejected": (ever / runs).tolist(), "final": float(ever[-1] / runs),
            "path": path, "runs": runs, "lr_ever_10": lr_paths_ge_10 / runs}


# ---------------------------------------------------------------------------
# Birnbaum's theorem on a toy experiment
# ---------------------------------------------------------------------------
def birnbaum() -> dict:
    """Two experiments about theta in {theta0, theta1}. E1: binomial, 12 tosses, record the number of heads.
    E2: negative binomial, toss until the 3rd tail, record the number of tosses. Outcomes x1 = '9 heads in 12' and
    x2 = '12 tosses to the 3rd tail' have proportional likelihoods in theta. The mixture E* (flip a fair coin to
    choose E1 or E2) has a statistic T that maps (E1, x1) and (E2, x2) to the same point; T is sufficient.
    Sufficiency: Ev(E*, (E1, x1)) = Ev(E*, (E2, x2)). Conditionality: Ev(E*, (Ej, xj)) = Ev(Ej, xj). So
    Ev(E1, x1) = Ev(E2, x2): the likelihood principle. The one-sided p-values for theta = 1/2 differ."""
    from math import comb
    thetas = [0.5, 0.75]
    l1 = [comb(12, 9) * t ** 9 * (1 - t) ** 3 for t in thetas]
    l2 = [comb(11, 2) * t ** 9 * (1 - t) ** 3 for t in thetas]
    # p-values for H0: theta = 1/2 against theta > 1/2
    p_binom = sum(comb(12, k) for k in range(9, 13)) / 2 ** 12
    # negative binomial: P(N >= 12) where N = tosses to the 3rd tail, p(tail) = 1/2
    p_negbin = 1 - sum(comb(n - 1, 2) * 0.5 ** n for n in range(3, 12))
    return {"likelihoods_E1": l1, "likelihoods_E2": l2, "ratio_E1": l1[1] / l1[0], "ratio_E2": l2[1] / l2[0],
            "proportional": abs(l1[1] / l1[0] - l2[1] / l2[0]) < 1e-12, "p_binomial": p_binom,
            "p_negative_binomial": p_negbin}


# ---------------------------------------------------------------------------
# Lindley's paradox and Bayes factors
# ---------------------------------------------------------------------------
def bf01_normal(z: float, n: int, tau: float = 1.0, sigma: float = 1.0) -> float:
    """Bayes factor for H0: mu = 0 against H1: mu ~ N(0, tau^2), from xbar with known sigma; z = xbar / (sigma /
    sqrt n). BF01 = sqrt(1 + n tau^2 / sigma^2) * exp(-z^2/2 * n tau^2 / (sigma^2 + n tau^2))."""
    r = n * tau ** 2 / sigma ** 2
    return math.sqrt(1 + r) * math.exp(-0.5 * z * z * r / (1 + r))


def lindley(z: float = 2.0, ns=(10, 100, 1000, 10_000, 100_000, 1_000_000)) -> dict:
    """Hold z = 2 (two-sided p = 0.0455) fixed and let n grow: the Bayes factor swings to favour the null."""
    rows = [{"n": n, "p": p_two_sided(z), "bf01": bf01_normal(z, n),
             "post_null": bf01_normal(z, n) / (1 + bf01_normal(z, n))} for n in ns]
    return {"z": z, "rows": rows}


def prior_sensitivity(z: float = 2.0, n: int = 100, taus=(0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 50)) -> dict:
    """The same data, Bayes factors under priors of different width: the evidence 'for' H1 depends on the prior.
    Includes the most favourable alternative (a point mass at the MLE), bounding BF10 by exp(z^2/2)."""
    rows = [{"tau": t, "bf01": bf01_normal(z, n, t)} for t in taus]
    return {"z": z, "n": n, "rows": rows, "max_bf10": math.exp(z * z / 2),
            "min_bf01_normal": min(r["bf01"] for r in rows)}


# ---------------------------------------------------------------------------
# Severity
# ---------------------------------------------------------------------------
def severity(xbar: float = 0.4, sigma: float = 1.0, n: int = 25, mus=None) -> dict:
    """Mayo and Spanos: after observing xbar (sigma known, n), the severity with which 'mu > mu1' passes is
    P(Xbar <= xbar; mu = mu1). Curves for two observed results: one significant, one not."""
    mus = mus if mus is not None else [round(-0.2 + 0.02 * k, 2) for k in range(51)]
    se = sigma / math.sqrt(n)
    out = {}
    for name, xb in (("significant", xbar), ("not significant", 0.2)):
        out[name] = {"xbar": xb, "z": xb / se, "p_one_sided": 1 - phi(xb / se),
                     "sev_greater": [phi((xb - m) / se) for m in mus],
                     "sev_less": [1 - phi((xb - m) / se) for m in mus]}
    return {"mus": mus, "se": se, "n": n, **out}


# ---------------------------------------------------------------------------
# Simpson's paradox: Berkeley 1973, the six largest departments
# ---------------------------------------------------------------------------
BERKELEY = {  # department: (men applied, men admitted, women applied, women admitted); Bickel et al. (1975)
    "A": (825, 512, 108, 89), "B": (560, 353, 25, 17), "C": (325, 120, 593, 202),
    "D": (417, 138, 375, 131), "E": (191, 53, 393, 94), "F": (373, 22, 341, 24),
}


def simpson() -> dict:
    rows = []
    M = Ma = W = Wa = 0
    for k, (m, ma, w, wa) in BERKELEY.items():
        rows.append({"dept": k, "men": m, "men_rate": ma / m, "women": w, "women_rate": wa / w,
                     "women_higher": wa / w > ma / m})
        M, Ma, W, Wa = M + m, Ma + ma, W + w, Wa + wa
    return {"rows": rows, "men_rate": Ma / M, "women_rate": Wa / W, "men": M, "women": W,
            "depts_women_higher": sum(r["women_higher"] for r in rows)}


# ---------------------------------------------------------------------------
# Testing by betting
# ---------------------------------------------------------------------------
def betting(n: int = 400, p_true: float = 0.6, runs: int = 4000, seed: int = 1939, lam: float = 0.2) -> dict:
    """Test H0: a coin is fair, by betting. Each round you stake a fraction lam of your wealth on heads at even
    odds, so wealth multiplies by (1 + lam) on heads and (1 - lam) on tails: a nonnegative martingale under H0
    (a test martingale), starting at 1. Ville's inequality: P(sup_t W_t >= 1/alpha) <= alpha under H0. Checked by
    simulation; and one wealth path under H0 and under the alternative p_true."""
    rng = np.random.default_rng(seed)

    def path(p):
        x = rng.random(n) < p
        return np.cumprod(np.where(x, 1 + lam, 1 - lam))
    null_paths = np.array([path(0.5) for _ in range(runs)])
    sup = null_paths.max(axis=1)
    ville = {str(a): float((sup >= 1 / a).mean()) for a in (0.2, 0.1, 0.05, 0.01)}
    alt = [path(p_true) for _ in range(runs // 4)]
    alt_hit = float(np.mean([np.any(a >= 20) for a in alt]))
    first = [int(np.argmax(a >= 20)) + 1 for a in alt if np.any(a >= 20)]
    return {"n": n, "lam": lam, "ville": ville, "null_path": path(0.5).tolist()[::2],
            "alt_path": path(p_true).tolist()[::2], "p_true": p_true, "alt_reach_20": alt_hit,
            "median_time_to_20": float(np.median(first)) if first else None, "runs": runs}


def ville_bound_check(alphas=(0.2, 0.1, 0.05, 0.01), **kw) -> bool:
    b = betting(**kw)
    return all(b["ville"][str(a)] <= a + 0.01 for a in alphas)


# ---------------------------------------------------------------------------
# A/B testing: peeking, and an always-valid alternative
# ---------------------------------------------------------------------------
def ab_peeking(runs: int = 2000, visitors: int = 5000, check_every: int = 100, seed: int = 2017) -> dict:
    """An A/B test with no real difference (both arms convert at 10%). A team peeks after every batch and stops at
    p < 0.05: the false positive rate. The same team using a betting e-process (reject when wealth >= 20) keeps it
    below 5%, at any peeking schedule."""
    rng = np.random.default_rng(seed)
    looks = list(range(check_every, visitors + 1, check_every))
    peek_fp = 0
    e_fp = 0
    for _ in range(runs):
        a = rng.random(visitors) < 0.10
        b = rng.random(visitors) < 0.10
        ca, cb = np.cumsum(a), np.cumsum(b)
        hit = False
        for m in looks:
            pa, pb = ca[m - 1] / m, cb[m - 1] / m
            pp = (ca[m - 1] + cb[m - 1]) / (2 * m)
            se = math.sqrt(max(pp * (1 - pp) * 2 / m, 1e-12))
            if p_two_sided((pa - pb) / se) < 0.05:
                hit = True
                break
        peek_fp += hit
        # e-process on the discordant pairs: under H0 each discordant pair is a fair coin
        w, lam = 1.0, 0.1
        for i in range(visitors):
            if a[i] != b[i]:
                w *= (1 + lam) if a[i] else (1 - lam)
                if w >= 20:
                    e_fp += 1
                    break
    return {"runs": runs, "visitors": visitors, "looks": len(looks), "peeking_fp": peek_fp / runs,
            "e_process_fp": e_fp / runs}


# ---------------------------------------------------------------------------
# AIC and BIC
# ---------------------------------------------------------------------------
def aic_bic(n_train: int = 30, n_test: int = 10000, noise: float = 0.5, seed: int = 1994, max_deg: int = 7,
            reps: int = 300) -> dict:
    """Forster and Sober (1994): AIC estimates predictive accuracy. For a cubic truth with noise, fit polynomials
    of each degree and compare: AIC's choice, BIC's choice, and the degree with the best expected out-of-sample
    log-likelihood, over ``reps`` training sets."""
    rng = np.random.default_rng(seed)
    pick_aic = np.zeros(max_deg + 1, int)
    pick_bic = np.zeros(max_deg + 1, int)
    test_ll = np.zeros(max_deg + 1)
    aic_est = np.zeros(max_deg + 1)
    train_ll = np.zeros(max_deg + 1)

    def f(x):
        return 0.5 * x - 1.2 * x ** 3

    xt = rng.uniform(-1.5, 1.5, n_test)
    yt = f(xt) + rng.normal(0, noise, n_test)
    for _ in range(reps):
        x = rng.uniform(-1.5, 1.5, n_train)
        y = f(x) + rng.normal(0, noise, n_train)
        aics, bics = [], []
        for k in range(max_deg + 1):
            c = np.polyfit(x, y, k)
            rss = float(((np.polyval(c, x) - y) ** 2).sum())
            s2 = rss / n_train
            ll = -n_train / 2 * (math.log(2 * math.pi * s2) + 1)
            params = k + 2
            aics.append(-2 * ll + 2 * params)
            aic_est[k] += (ll - params) / n_train
            train_ll[k] += ll / n_train
            bics.append(-2 * ll + params * math.log(n_train))
            r = np.polyval(c, xt) - yt
            test_ll[k] += float(-0.5 * np.mean(r ** 2) / s2 - 0.5 * math.log(2 * math.pi * s2))
        pick_aic[int(np.argmin(aics))] += 1
        pick_bic[int(np.argmin(bics))] += 1
    test_ll /= reps
    aic_est /= reps
    train_ll /= reps
    return {"degrees": list(range(max_deg + 1)), "aic_picks": pick_aic.tolist(), "bic_picks": pick_bic.tolist(),
            "test_loglik": test_ll.tolist(), "aic_estimate": aic_est.tolist(), "train_loglik": train_ll.tolist(), "best_predictive": int(np.argmax(test_ll)), "true_degree": 3,
            "reps": reps, "n": n_train}


def collins(n_couples: float = 12e6) -> dict:
    """People v. Collins (1968): the prosecution multiplied six 'independent' frequencies to reach 1 in 12 million.
    The California Supreme Court's appendix asked the right question: given that at least one couple in the area
    fits, how likely is it that another does too? With N couples and match probability p, the count is binomial;
    P(at least 2 | at least 1) = (1 - P0 - P1) / (1 - P0)."""
    traits = [("partly yellow car", 10), ("man with moustache", 4), ("woman with ponytail", 10),
              ("woman with blond hair", 3), ("man with beard", 10), ("interracial couple in car", 1000)]
    denom = 1
    for _, d in traits:
        denom *= d
    p = 1 / denom

    def another(N):
        p0 = math.exp(N * math.log1p(-p))
        p1 = N * p * math.exp((N - 1) * math.log1p(-p))
        return (1 - p0 - p1) / (1 - p0)
    curve = [[N / 1e6, another(N)] for N in [k * 1e6 for k in range(1, 61)]]
    return {"traits": traits, "denominator": denom, "N": n_couples, "another": another(n_couples), "curve": curve,
            "poisson_limit": (1 - 2 / math.e) / (1 - 1 / math.e)}
