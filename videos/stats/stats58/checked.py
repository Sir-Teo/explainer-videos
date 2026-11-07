"""Audited Part 58 calculations; legacy teaching helpers remain available.

Betting inversion uses conservative continuum cells, not candidate points.
Logged propensities condition on the auxiliary Monte Carlo draws before action.
"""
from __future__ import annotations
import math
import numpy as np
from scipy import stats
from explainer.stats.kit.sequential import *  # noqa: F403
from explainer.stats.kit import causal as CA

def mcse(values):
    a = np.asarray(values, float)
    return float(a.std(ddof=1) / math.sqrt(len(a)))

def sprt_bernoulli_exact(p: float, p0: float, p1: float, alpha: float, beta: float, n_max: int = 5000) -> dict:
    """The SPRT of p0 against p1 (p1 > p0) on Bernoulli(p) data, propagated on its lattice with a certified truncation remainder.  After n trials with s successes the
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
    lower = en + n * rest
    # From any continuing state, a block of k successes or l failures exits.
    # Geometric blocks bound the remaining mean by block length / block probability.
    k, l = math.ceil((hi-lo)/a)+1, math.ceil((hi-lo)/abs(b))+1
    escape = min(k/p**k if p else math.inf, l/(1-p)**l if p < 1 else math.inf)
    upper = lower + rest * escape
    return {"asn_lower": lower, "asn_upper": upper,
            "accept_h1_upper": acc1 + rest, "accept_h0_upper": acc0 + rest,
            "accept_h1": acc1, "accept_h0": acc0, "asn": (lower + upper) / 2, "unfinished": rest, "stop_n": stop_n[: n + 1],
            "a": a, "b": b}

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
    signed = z[np.arange(reps), k]
    positive, negative = early & (signed > 0), early & (signed < 0)
    return {"reps": reps, "bias_mcse": mcse(mean),
            "bias_early_positive": float(mean[positive].mean()-theta) if positive.any() else np.nan,
            "bias_early_negative": float(mean[negative].mean()-theta) if negative.any() else np.nan,
            "p_early_positive": float(positive.mean()), "p_early_negative": float(negative.mean()),
            "mean": float(mean.mean()), "bias": float(mean.mean() - theta), "bias_early": float(mean[early].mean() - theta) if early.any() else np.nan,
            "p_early": float(early.mean()), "stop_look": np.bincount(k, minlength=K) / reps}

def peeking_curve(ns, alpha, reps, rng):
    ns = np.asarray(ns, int)
    total = np.zeros(len(ns), int)
    crit = stats.norm.isf(alpha/2)
    for start in range(0, reps, 256):
        X = rng.standard_normal((min(256, reps-start), int(ns.max())))
        run = np.maximum.accumulate(np.abs(np.cumsum(X, 1)/np.sqrt(np.arange(1, ns.max()+1))) >= crit, axis=1)
        total += run[:, ns-1].sum(0)
    return total/reps

def ville_check(n, mu1, alpha, reps, rng):
    counts = np.zeros(3, int)
    for start in range(0, reps, 256):
        X = rng.standard_normal((min(256, reps-start), n))
        logM = np.cumsum(mu1*X-mu1*mu1/2, 1)
        z = np.cumsum(X, 1)/np.sqrt(np.arange(1, n+1))
        crit = stats.norm.isf(alpha/2)
        counts += [np.sum(logM.max(1) >= math.log(1/alpha)),
                   np.sum(np.abs(z).max(1) >= crit),
                   np.sum(np.abs(z[:, -1]) >= crit)]
    out = dict(zip(("ville", "peek", "end_only"), counts/reps))
    return out | {"reps": reps, "mcse": {k: math.sqrt(v*(1-v)/reps) for k,v in out.items()}}

def split_lrt_normal_mean(x, rng: np.random.Generator) -> float:
    """Universal inference (Wasserman, Ramdas & Balakrishnan 2020) for H0: mu = 0 in N(mu, sigma^2), sigma unknown:
    fit (mu, sigma) on half D0, and divide the D1-likelihood at that fit by the D1-likelihood maximized over the null
    (mu = 0, sigma free).  The ratio is an e-value: E_H0 <= 1."""
    x = np.asarray(x, float)
    o = rng.permutation(len(x))
    d0, d1 = x[o[: len(x) // 2]], x[o[len(x) // 2:]]
    mu, sd = d0.mean(), d0.std() + 1e-12
    s0 = math.sqrt(np.mean(d1 ** 2))
    if s0 == 0:
        return 0.0  # null likelihood supremum is infinite
    num = stats.norm.logpdf(d1, mu, sd).sum()
    den = stats.norm.logpdf(d1, 0, s0).sum()
    return float(math.exp(num - den))

def betting_cs(x, alpha, grid=None, c=0.5):
    """Outer running-intersection CS for conditional common mean in [0,1].

    Kplus(m) decreases and Kminus(m) increases in m. On [a,b],
    (Kplus(b)+Kminus(a))/2 is a LOWER wealth bound. Excluding only
    cells whose bound crossed 1/alpha preserves continuum coverage.
    This predictable plug-in rule is not claimed to be LIL optimal.
    """
    x = np.asarray(x, float)
    grid = np.linspace(0, 1, 1001) if grid is None else np.asarray(grid, float)
    if not (0 < alpha < 1 and 0 < c < 1 and len(grid) >= 2
            and grid[0] == 0 and grid[-1] == 1 and np.all(np.diff(grid) > 0)
            and np.all((x >= 0) & (x <= 1))):
        raise ValueError("need bounded observations, 0<alpha,c<1 and increasing endpoint-inclusive grid")
    t = np.arange(1, len(x)+1)
    mu = np.r_[0.5, (0.5+np.cumsum(x)[:-1])/t[1:]]
    var = np.r_[0.25, (0.25+np.cumsum((x[:-1]-mu[:-1])**2))/t[1:]]
    lam = np.sqrt(2*math.log(2/alpha)/(var*t*np.log(t+1)))
    cp = np.divide(c, grid, out=np.full_like(grid, np.inf), where=grid>0)
    cm = np.divide(c, 1-grid, out=np.full_like(grid, np.inf), where=grid<1)
    lp, lm = np.zeros(len(grid)), np.zeros(len(grid))
    alive = np.ones(len(grid)-1, bool)
    lo, hi = np.full(len(x), np.nan), np.full(len(x), np.nan)
    for i, value in enumerate(x):
        lp += np.log1p(np.minimum(lam[i], cp)*(value-grid))
        lm += np.log1p(-np.minimum(lam[i], cm)*(value-grid))
        lower = np.logaddexp(lp[1:], lm[:-1])-math.log(2)
        alive &= lower < math.log(1/alpha)
        idx = np.flatnonzero(alive)
        if len(idx):
            lo[i], hi[i] = grid[idx[0]], grid[idx[-1]+1]
    return {"lo": lo, "hi": hi, "cell_width_max": float(np.diff(grid).max()),
            "inversion": "conservative continuum-cell outer hull"}

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
    return {"uniform": always / reps, "final": final / reps,
            "uniform_mcse": math.sqrt(always/reps*(1-always/reps)/reps),
            "final_mcse": math.sqrt(final/reps*(1-final/reps)/reps),
            "reps": reps}

def cusum_arl(mu: float, mu0: float, mu1: float, h: float, reps: int, rng: np.random.Generator, t_max: int = 200_000) -> dict:
    """Average run length to alarm when the data are N(mu, 1) from the start (mu = mu0: the false-alarm ARL)."""
    out = np.empty(reps)
    censored = 0
    for r in range(reps):
        w, t = 0.0, 0
        while t < t_max:
            chunk = rng.standard_normal(min(4096, t_max-t)) + mu
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
        censored += int(t >= t_max and hit < 0)
        out[r] = t
    return {"mean": float(out.mean()), "mcse": mcse(out), "censored": censored,
            "t_max": t_max, "run_lengths": out, "scope": "restricted mean to t_max; full ARL only if tail negligible"}

def thompson_bernoulli(means, T: int, rng: np.random.Generator, floor: float = 0.0, n_mc: int = 200) -> dict:
    """Thompson sampling with Beta(1, 1) priors on K Bernoulli arms.  The action actually uses frequencies from
    n_mc posterior draws and floored at ``floor`` (renormalized), so they are known for the inference that follows."""
    means = np.asarray(means, float)
    K = len(means)
    if not (0 <= floor <= 1/K and n_mc >= 1):
        raise ValueError("floor must be in [0,1/K] and n_mc positive")
    a, b = np.ones(K), np.ones(K)
    arms = np.empty(T, int)
    ys = np.empty(T)
    probs = np.empty((T, K))
    for t in range(T):
        draws = rng.beta(a[None, :], b[None, :], (n_mc, K))
        e = np.bincount(np.argmax(draws, 1), minlength=K) / n_mc
        if floor > 0:
            e = floor + (1-K*floor)*e
        k = rng.choice(K, p=e)
        y = float(rng.random() < means[k])
        arms[t], ys[t], probs[t] = k, y, e
        a[k] += y
        b[k] += 1 - y
    return {"arm": arms, "y": ys, "e": probs, "n_mc": n_mc,
            "policy": "finite-MC probability matching; auxiliary draws before action",
            "floor": floor}

def crossing_probs(bounds, info=None, drift=0.0, nodes=160):
    """Brownian first-crossing probabilities by smooth continuation quadrature.

    Integrate on each look's continuation interval rather than rounding a moving
    boundary to a fixed grid. Infinite boundaries use an eight-SD tail cutoff.
    """
    from scipy.special import roots_legendre

    bounds = np.asarray(bounds, float)
    times = np.arange(1, len(bounds) + 1) / len(bounds) if info is None else np.asarray(info, float)
    u, weight = roots_legendre(nodes)
    previous_t, previous_x, mass = 0.0, None, None
    out = []
    for boundary, t in zip(bounds, times):
        dt = t - previous_t
        sd = math.sqrt(dt)
        edge = boundary * math.sqrt(t)
        limit = edge if np.isfinite(edge) else 8 * math.sqrt(t) + abs(drift) * t
        x, weights = limit * u, limit * weight
        if mass is None:
            out.append(float(stats.norm.sf((edge - drift * dt) / sd)
                             + stats.norm.cdf((-edge - drift * dt) / sd)))
            density = stats.norm.pdf(x, drift * dt, sd)
        else:
            center = previous_x + drift * dt
            out.append(float(mass @ (stats.norm.sf((edge - center) / sd)
                                     + stats.norm.cdf((-edge - center) / sd))))
            density = stats.norm.pdf(x[:, None], center[None, :], sd) @ mass
        mass = density * weights
        previous_x, previous_t = x, t
    return np.asarray(out)

def sequential_boundaries(K=5, alpha=0.05, nodes=160):
    from scipy.optimize import brentq

    times = np.arange(1, K + 1) / K
    poc = brentq(lambda c: crossing_probs([c] * K, nodes=nodes).sum() - alpha, 1.5, 4, xtol=1e-10)
    obf_constant = brentq(lambda c: crossing_probs(c / np.sqrt(times), nodes=nodes).sum() - alpha,
                         1.5, 4, xtol=1e-10)
    spending = CA.spending(times, alpha)
    increments = np.diff(np.r_[0.0, spending])
    ld = []
    for k in range(K):
        ld.append(brentq(lambda c: crossing_probs(ld + [c], times[:k + 1], nodes=nodes)[-1] - increments[k],
                         0.5, 12, xtol=1e-10))
    return poc, obf_constant / np.sqrt(times), np.asarray(ld)

