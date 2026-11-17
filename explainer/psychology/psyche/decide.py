"""Psyche's decisions in time: adding up evidence until it crosses a line (Part 25 of *Psychology, Built*).

A choice between two answers takes time because the evidence for each arrives noisily, a little at a time, and the
chooser must decide when it has enough.  Wald's sequential probability ratio test (1947) says when, for a
statistician; Ratcliff's diffusion model (1978) says the same for a person, in half a second.  Everything here is
closed form, a convergent series, or a stated simulation; times are in seconds.

* **Wald's test.**  :func:`sprt_bernoulli` runs it on coin flips; :func:`wald_bounds`, :func:`sprt_oc_asn` give the
  operating characteristic and average sample number (Wald's approximations, checked by simulation), and
  :func:`fixed_n` the fixed-sample test with the same error rates, so the saving can be computed.
* **The diffusion model.**  Evidence ``x(t)`` starts at ``z = w a`` between bounds 0 and ``a`` and drifts at ``v``
  with unit noise (``s`` rescales).  Closed forms: the probability of the upper bound (:func:`p_upper`) and the
  mean decision time (:func:`mean_dt`).  The first-passage densities by Navarro and Fuss's two series
  (:func:`fpt_density`), with across-trial drift variability ``sv`` integrated out exactly; conditional mean times
  by quadrature; a vectorized simulator with every across-trial variability (:func:`simulate`), and one with any
  bound that changes in time (:func:`simulate_bound`).
* **Fitting.**  :func:`fit_ddm` by maximum likelihood (``v, a, w, t0``, any of them fixable), and
  :func:`fit_conditions` for conditions that share some parameters and free others: the selective-influence test.  :func:`ez` is Wagenmakers, van der Maas
  and Grasman's EZ diffusion (2007), three summary statistics in, three parameters out.
* **Relatives.**  The linear ballistic accumulator (Brown and Heathcote 2008): densities, defective densities and
  a simulator (:func:`lba_pdf`, :func:`lba_cdf`, :func:`lba_defective`, :func:`lba_simulate`).  A race of ``n``
  diffusing accumulators whose bound is set for a fixed accuracy, which recovers Hick's logarithm
  (:func:`race_hick`).
* **The brain.**  Accumulator paths averaged by coherence, aligned to the stimulus and to the response
  (:func:`aligned_means`); a stepping model whose single trials jump, whose average ramps (:func:`stepping`).
* **Stopping.**  Logan and Cowan's independent race: :func:`stop_race` (the inhibition function from a go
  distribution and a stop process) and :func:`ssrt_integration` (the stop-signal reaction time by the integration
  method, with go omissions replaced by the maximum go time, as Verbruggen et al. 2019 recommend).
* **Confidence.**  The balance of evidence in a two-accumulator race (:func:`race_confidence`).
"""

from __future__ import annotations

import math

import numpy as np
from scipy import integrate, optimize, stats

Phi = stats.norm.cdf
phi = stats.norm.pdf


# ------------------------------------------------------------------------------------------- Wald's test
def wald_bounds(alpha: float, beta: float) -> tuple:
    """Wald's approximate log-likelihood-ratio bounds: accept H1 above ``A = log((1 - beta) / alpha)``, accept H0
    below ``B = log(beta / (1 - alpha))``."""
    return math.log((1 - beta) / alpha), math.log(beta / (1 - alpha))


def sprt_bernoulli(x, p0: float, p1: float, alpha: float = 0.05, beta: float = 0.05) -> dict:
    """Run the SPRT for ``p = p0`` against ``p = p1`` on a sequence of 0/1 observations; stops at the first bound
    crossing (or the end of the data)."""
    A, B = wald_bounds(alpha, beta)
    up, dn = math.log(p1 / p0), math.log((1 - p1) / (1 - p0))
    llr = np.cumsum(np.where(np.asarray(x) > 0, up, dn))
    path = np.concatenate([[0.0], llr])
    hit = np.nonzero((llr >= A) | (llr <= B))[0]
    if len(hit) == 0:
        return {"path": path, "n": len(llr), "decision": None, "A": A, "B": B}
    k = int(hit[0])
    return {"path": path[: k + 2], "n": k + 1, "decision": int(llr[k] >= A), "A": A, "B": B}


def _h_for(p, p0, p1):
    """The nonzero root h of p (p1/p0)^h + (1-p) ((1-p1)/(1-p0))^h = 1 (Wald's operating characteristic)."""
    up, dn = math.log(p1 / p0), math.log((1 - p1) / (1 - p0))
    f = lambda h: p * math.exp(h * up) + (1 - p) * math.exp(h * dn) - 1
    mean = p * up + (1 - p) * dn
    if abs(mean) < 1e-12:
        return 0.0
    # h has the opposite sign to the mean increment
    lo, hi = (1e-9, 50.0) if mean < 0 else (-50.0, -1e-9)
    return optimize.brentq(f, lo, hi)


def sprt_oc_asn(p, p0: float, p1: float, alpha: float = 0.05, beta: float = 0.05) -> tuple:
    """Wald's approximations to P(accept H0 | p) and the average sample number E[N | p]."""
    A, B = wald_bounds(alpha, beta)
    up, dn = math.log(p1 / p0), math.log((1 - p1) / (1 - p0))
    mean = p * up + (1 - p) * dn
    h = _h_for(p, p0, p1)
    if h == 0.0:
        oc = A / (A - B)
        var = p * up ** 2 + (1 - p) * dn ** 2
        return oc, -A * B / var
    eA, eB = math.exp(h * A), math.exp(h * B)
    oc = (eA - 1) / (eA - eB)
    asn = (oc * B + (1 - oc) * A) / mean
    return oc, asn


def fixed_n(p0: float, p1: float, alpha: float = 0.05, beta: float = 0.05) -> int:
    """The smallest fixed sample size whose one-sided exact binomial test of p0 against p1 has size <= alpha and
    power >= 1 - beta."""
    for n in range(1, 5000):
        c = int(stats.binom.ppf(1 - alpha, n, p0)) + 1  # reject when successes >= c
        while c > 0 and stats.binom.sf(c - 2, n, p0) <= alpha:
            c -= 1
        if stats.binom.sf(c - 1, n, p0) <= alpha and stats.binom.sf(c - 1, n, p1) >= 1 - beta:
            return n
    raise ValueError("no n below 5000")


def sprt_simulate(p: float, p0: float, p1: float, alpha: float = 0.05, beta: float = 0.05, reps: int = 20000,
                  seed: int = 0, max_n: int = 2000) -> dict:
    """Monte Carlo operating characteristic and sample-number distribution of the Bernoulli SPRT."""
    rng = np.random.default_rng(seed)
    A, B = wald_bounds(alpha, beta)
    up, dn = math.log(p1 / p0), math.log((1 - p1) / (1 - p0))
    x = np.zeros(reps)
    n = np.zeros(reps, int)
    done = np.zeros(reps, bool)
    acc1 = np.zeros(reps, bool)
    for k in range(1, max_n + 1):
        live = ~done
        if not live.any():
            break
        step = np.where(rng.random(live.sum()) < p, up, dn)
        x[live] += step
        hit1 = live.copy()
        hit1[live] = x[live] >= A
        hit0 = live.copy()
        hit0[live] = x[live] <= B
        n[hit1 | hit0] = k
        acc1[hit1] = True
        done |= hit1 | hit0
    return {"accept_h1": acc1.mean(), "n": n, "mean_n": n.mean()}


# ------------------------------------------------------------------------------------------- the diffusion model
def p_upper(v, a, w=0.5, s: float = 1.0):
    """Probability that diffusion with drift v, unit-s noise, from w*a, reaches a before 0."""
    v, a, w = np.broadcast_arrays(np.asarray(v, float), np.asarray(a, float), np.asarray(w, float))
    k = 2 * v / s ** 2
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        out = np.where(np.abs(v) < 1e-10, w, -np.expm1(-k * a * w) / -np.expm1(-k * a))
    return out[()] if out.ndim == 0 else out


def mean_dt(v, a, w=0.5, s: float = 1.0):
    """Mean decision time (both bounds), E[T] = (a P_upper - z) / v; z (a - z) / s^2 when v = 0."""
    v, a, w = np.broadcast_arrays(np.asarray(v, float), np.asarray(a, float), np.asarray(w, float))
    z = w * a
    with np.errstate(invalid="ignore", divide="ignore"):
        out = np.where(np.abs(v) < 1e-10, z * (a - z) / s ** 2, (a * p_upper(v, a, w, s) - z) / np.where(
            np.abs(v) < 1e-10, 1.0, v))
    return out[()] if out.ndim == 0 else out


def _std_lower(u, w, terms: int = 12):
    """Density of the first passage at 0 for zero drift, unit bound, start w, at standardized time u = t / a^2.
    Navarro and Fuss (2009): the small-time series for u < 1, the large-time series otherwise."""
    u = np.asarray(u, float)
    out = np.zeros_like(u)
    small = (u > 0) & (u < 1.0)
    if small.any():
        us = u[small]
        k = np.arange(-terms, terms + 1)[:, None]
        r = w + 2 * k
        out[small] = (r * np.exp(-r ** 2 / (2 * us))).sum(0) / np.sqrt(2 * np.pi * us ** 3)
    large = u >= 1.0
    if large.any():
        ul = u[large]
        k = np.arange(1, 4 * terms + 1)[:, None]
        out[large] = np.pi * (k * np.exp(-k ** 2 * np.pi ** 2 * ul / 2) * np.sin(k * np.pi * w)).sum(0)
    return np.maximum(out, 0.0)


def fpt_density(t, v: float, a: float, w: float = 0.5, bound: str = "upper", sv: float = 0.0, s: float = 1.0):
    """Defective density of reaching ``bound`` at decision time t (> 0).  ``sv`` is the standard deviation of the
    drift across trials, integrated out in closed form (as in Blurton, Kesselmeier and Gondan 2012)."""
    t = np.asarray(t, float)
    v, a, sv = v / s, a / s, sv / s
    if bound == "upper":
        v, w = -v, 1 - w
    pos = t > 0
    out = np.zeros_like(t)
    tt = t[pos]
    g = _std_lower(tt / a ** 2, w) / a ** 2
    one = 1 + sv ** 2 * tt
    out[pos] = g * np.exp((sv ** 2 * a ** 2 * w ** 2 - 2 * a * v * w - v ** 2 * tt) / (2 * one)) / np.sqrt(one)
    return out[()] if out.ndim == 0 else out


def rt_density(rt, v, a, w=0.5, t0=0.3, bound="upper", sv=0.0, st=0.0, s=1.0):
    """Density of the response time rt = t0 + decision time; ``st`` spreads t0 uniformly over [t0, t0 + st]."""
    rt = np.asarray(rt, float)
    if st <= 0:
        return fpt_density(rt - t0, v, a, w, bound, sv, s)
    nodes, weights = np.polynomial.legendre.leggauss(16)
    shift = t0 + st * (nodes + 1) / 2
    vals = np.array([fpt_density(rt - u, v, a, w, bound, sv, s) for u in shift])
    return (weights[:, None] * vals).sum(0) / 2 if vals.ndim > 1 else (weights * vals).sum() / 2


def cond_mean_dt(v, a, w=0.5, bound="upper", sv=0.0, s=1.0) -> float:
    """Mean decision time given the bound reached, by quadrature of the density."""
    f = lambda t: fpt_density(t, v, a, w, bound, sv, s)
    tmax = 20 * a ** 2 / s ** 2 + 5
    m0 = integrate.quad(lambda t: float(f(t)), 0, tmax, limit=400)[0]
    m1 = integrate.quad(lambda t: t * float(f(t)), 0, tmax, limit=400)[0]
    return m1 / m0


def simulate(v, a, w=0.5, t0=0.3, n=2000, seed=0, sv=0.0, sw=0.0, st=0.0, s=1.0, dt=0.001, max_t=6.0):
    """Euler simulation of n diffusion trials with across-trial variability in drift (normal, sd ``sv``), start
    (uniform, width ``sw`` as a share of a) and non-decision time (uniform, width ``st``).  Returns response times,
    whether the upper bound was reached, and (for trials that never finish by ``max_t``) NaN."""
    rng = np.random.default_rng(seed)
    vv = v + sv * rng.standard_normal(n)
    x = a * (w + sw * (rng.random(n) - 0.5))
    tt = t0 + st * rng.random(n)
    rt = np.full(n, np.nan)
    up = np.zeros(n, bool)
    live = np.ones(n, bool)
    sd = s * math.sqrt(dt)
    for k in range(1, int(max_t / dt) + 1):
        idx = np.nonzero(live)[0]
        if len(idx) == 0:
            break
        x[idx] += vv[idx] * dt + sd * rng.standard_normal(len(idx))
        hit_u = x[idx] >= a
        hit_l = x[idx] <= 0
        fin = idx[hit_u | hit_l]
        rt[fin] = k * dt + tt[fin]
        up[idx[hit_u]] = True
        live[fin] = False
    return rt, up


def simulate_bound(v, bound_fn, t0=0.3, n=2000, seed=0, sv=0.0, s=1.0, dt=0.001, max_t=6.0):
    """Diffusion from 0 between symmetric bounds +-bound_fn(t) (an urgency signal or collapsing bound)."""
    rng = np.random.default_rng(seed)
    vv = v + sv * rng.standard_normal(n)
    x = np.zeros(n)
    rt = np.full(n, np.nan)
    up = np.zeros(n, bool)
    live = np.ones(n, bool)
    sd = s * math.sqrt(dt)
    for k in range(1, int(max_t / dt) + 1):
        idx = np.nonzero(live)[0]
        if len(idx) == 0:
            break
        b = bound_fn(k * dt)
        x[idx] += vv[idx] * dt + sd * rng.standard_normal(len(idx))
        hu = x[idx] >= b
        hl = x[idx] <= -b
        fin = idx[hu | hl]
        rt[fin] = k * dt + t0
        up[idx[hu]] = True
        live[fin] = False
    return rt, up


# ------------------------------------------------------------------------------------------- fitting
PARAMS = ("v", "a", "w", "t0")


def neg_loglik(params, rt, up, sv: float = 0.0, eps: float = 1e-10) -> float:
    """-log likelihood of response times ``rt`` (seconds) and upper-bound responses ``up`` under (v, a, w, t0)."""
    v, a, w, t0 = params
    if a <= 0.05 or not (0.05 < w < 0.95) or t0 < 0 or t0 >= np.min(rt):
        return 1e12
    d = np.where(up, rt_density(rt, v, a, w, t0, "upper", sv), rt_density(rt, v, a, w, t0, "lower", sv))
    return float(-np.sum(np.log(np.maximum(d, eps))))


def fit_ddm(rt, up, fix: dict | None = None, start=None) -> dict:
    """Maximum-likelihood diffusion fit to one condition (times in seconds, ``up`` = upper-bound response).
    ``fix`` holds parameters to keep fixed, e.g. ``{"w": 0.5}`` for accuracy-coded data."""
    rt, up = np.asarray(rt, float), np.asarray(up, bool)
    fix = dict(fix or {})
    if start is None:
        e = ez(min(max(np.mean(up), 0.55), 0.99), np.var(rt), np.mean(rt), s=1.0)
        start = {"v": e["v"], "a": e["a"], "w": 0.5, "t0": max(0.05, min(e["t0"], 0.9 * rt.min()))}
    free = [p for p in PARAMS if p not in fix]

    def full(x):
        d = dict(fix)
        d.update(zip(free, x))
        return [d[p] for p in PARAMS]

    res = optimize.minimize(lambda x: neg_loglik(full(x), rt, up), [start[p] for p in free], method="Nelder-Mead",
                            options={"xatol": 1e-4, "fatol": 1e-4, "maxiter": 4000})
    out = dict(zip(PARAMS, map(float, full(res.x))))
    out.update(nll=float(res.fun), n=len(rt), k=len(free))
    return out


def fit_conditions(data: dict, free: tuple, fix: dict | None = None) -> dict:
    """Fit several conditions at once.  ``data`` maps a condition to (rt, up); parameters in ``free`` take one
    value per condition, the others (not in ``fix``) one value overall.  Returns the parameters by condition, the
    total -log likelihood, the number of parameters and the AIC."""
    fix = dict(fix or {})
    conds = list(data)
    singles = [fit_ddm(*data[c], fix=fix) for c in conds]
    x0, layout = [], []
    for p in PARAMS:
        if p in fix:
            continue
        if p in free:
            for k in range(len(conds)):
                layout.append((p, k))
                x0.append(singles[k][p])
        else:
            layout.append((p, None))
            x0.append(float(np.mean([s_[p] for s_ in singles])))
    if "t0" not in free and "t0" not in fix:  # a shared t0 must sit below every condition's fastest time
        j = [i for i, (p, k) in enumerate(layout) if p == "t0"][0]
        x0[j] = min(x0[j], 0.95 * min(np.min(data[c][0]) for c in conds))

    def unpack(x):
        par = [dict(fix) for _ in conds]
        for (p, k), val in zip(layout, x):
            for j in (range(len(conds)) if k is None else [k]):
                par[j][p] = val
        return par

    def nll(x):
        return sum(neg_loglik([pp[p] for p in PARAMS], *data[c]) for pp, c in zip(unpack(x), conds))

    res = optimize.minimize(nll, x0, method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-4,
                                                                      "fatol": 1e-4, "adaptive": True})
    par = unpack(res.x)
    return {"params": {c: {k: float(v) for k, v in pp.items()} for pp, c in zip(par, conds)}, "nll": float(res.fun),
            "k": len(x0), "aic": 2 * float(res.fun) + 2 * len(x0)}


def ez(pc: float, vrt: float, mrt: float, s: float = 0.1) -> dict:
    """EZ diffusion (Wagenmakers, van der Maas and Grasman 2007): proportion correct, variance and mean of correct
    RTs (seconds) to drift, boundary separation and non-decision time; ``s`` is the noise scale (0.1 by
    convention there; 1 here elsewhere)."""
    pc = min(max(pc, 1e-3), 1 - 1e-3)
    if abs(pc - 0.5) < 1e-9:
        pc += 1e-4
    L = math.log(pc / (1 - pc))
    x = L * (L * pc ** 2 - L * pc + pc - 0.5) / vrt
    v = math.copysign(1, pc - 0.5) * s * x ** 0.25
    a = s ** 2 * L / v
    y = -v * a / s ** 2
    mdt = (a / (2 * v)) * (1 - math.exp(y)) / (1 + math.exp(y))
    return {"v": v, "a": a, "t0": mrt - mdt}


# ------------------------------------------------------------------------------------------- the LBA
def lba_cdf(t, v, A, b, s=1.0):
    """P(a single linear ballistic accumulator has reached b by time t): start ~ U(0, A), rate ~ N(v, s)."""
    t = np.maximum(np.asarray(t, float), 1e-12)
    z1, z2 = (b - A - t * v) / (t * s), (b - t * v) / (t * s)
    return np.clip(1 + (b - A - t * v) / A * Phi(z1) - (b - t * v) / A * Phi(z2) + t * s / A * phi(z1)
                   - t * s / A * phi(z2), 0, 1)


def lba_pdf(t, v, A, b, s=1.0):
    t = np.maximum(np.asarray(t, float), 1e-12)
    z1, z2 = (b - A - t * v) / (t * s), (b - t * v) / (t * s)
    return np.maximum((-v * Phi(z1) + s * phi(z1) + v * Phi(z2) - s * phi(z2)) / A, 0)


def lba_defective(t, i, vs, A, b, s=1.0, t0=0.0):
    """Density that accumulator i wins at response time t (others not yet finished)."""
    d = np.asarray(t, float) - t0
    out = lba_pdf(d, vs[i], A, b, s)
    for j, vj in enumerate(vs):
        if j != i:
            out = out * (1 - lba_cdf(d, vj, A, b, s))
    return np.where(d > 0, out, 0.0)


def lba_simulate(vs, A, b, s=1.0, t0=0.2, n=5000, seed=0):
    """Simulate the LBA race; accumulators with negative rates never finish."""
    rng = np.random.default_rng(seed)
    vs = np.asarray(vs, float)
    k = rng.random((n, len(vs))) * A
    d = vs + s * rng.standard_normal((n, len(vs)))
    with np.errstate(divide="ignore"):
        tt = np.where(d > 0, (b - k) / d, np.inf)
    win = tt.argmin(1)
    rt = tt.min(1) + t0
    ok = np.isfinite(rt)
    return rt[ok], win[ok]


def race_hick(ns=(1, 2, 4, 8), target: float = 0.9, v_correct: float = 2.0, seed: int = 0, n: int = 4000,
              dt: float = 0.002) -> dict:
    """A race of n independent diffusing accumulators (drift v_correct for the right one, 0 for the others, unit
    noise, start 0, a common bound b).  For each n the bound is raised until the right accumulator wins with
    probability ``target``; the mean decision time then grows with log n (Hick's law, recovered).  For n = 1 the
    bound is the n = 2 one (a simple reaction)."""
    out = {"n": list(ns), "b": [], "mean_dt": [], "acc": []}

    def run(m, b, seed_):
        rng = np.random.default_rng(seed_)
        x = np.zeros((n, m))
        drift = np.zeros(m)
        drift[0] = v_correct
        t = np.full(n, np.nan)
        win = np.full(n, -1)
        live = np.ones(n, bool)
        for k in range(1, 20000):
            idx = np.nonzero(live)[0]
            if not len(idx):
                break
            x[idx] += drift * dt + math.sqrt(dt) * rng.standard_normal((len(idx), m))
            hit = x[idx].max(1) >= b
            fin = idx[hit]
            t[fin] = k * dt
            win[fin] = x[fin].argmax(1)
            live[fin] = False
        return np.nanmean(t), np.mean(win == 0)

    b2 = None
    for m in ns:
        if m == 1:
            continue
        lo, hi = 0.05, 6.0
        for _ in range(22):
            mid = (lo + hi) / 2
            acc = run(m, mid, seed)[1]
            lo, hi = (mid, hi) if acc < target else (lo, mid)
        b = (lo + hi) / 2
        mt, acc = run(m, b, seed + 1)
        out["b"].append(b)
        out["mean_dt"].append(mt)
        out["acc"].append(acc)
        if m == 2:
            b2 = b
    if 1 in ns:
        mt, acc = run(1, b2, seed + 1)
        i = list(ns).index(1)
        out["b"].insert(i, b2)
        out["mean_dt"].insert(i, mt)
        out["acc"].insert(i, acc)
    return {k: np.array(v) for k, v in out.items()}


# ------------------------------------------------------------------------------------------- the brain
def aligned_means(vs, a: float = 1.0, t0: float = 0.0, n: int = 600, seed: int = 0, dt: float = 0.005,
                  pre: float = 0.4, post: float = 0.8):
    """Mean accumulated evidence for each drift, over trials that end at the upper bound (the choice the neuron
    favours).  Aligned to the stimulus (0 .. post s), with what follows each decision left out, as recordings leave
    out activity after the choice; and aligned to the response (-pre .. 0 s): Roitman and Shadlen 2002's two
    views."""
    rng = np.random.default_rng(seed)
    ts = np.arange(0, post + 1e-9, dt)
    tr = np.arange(-pre, 1e-9, dt)
    stim, resp = [], []
    for v in vs:
        T = int(6 / dt)
        x = np.zeros((n, T + 1))
        x[:, 0] = a / 2
        inc = v * dt + math.sqrt(dt) * rng.standard_normal((n, T))
        x[:, 1:] = a / 2 + np.cumsum(inc, 1)
        out_u = x >= a
        out_l = x <= 0
        first = np.where((out_u | out_l).any(1), (out_u | out_l).argmax(1), T)
        upper = out_u[np.arange(n), first]
        xs = x.copy()
        for i in range(n):  # freeze at the bound after it is reached
            xs[i, first[i]:] = a if upper[i] else 0
        keep = upper
        S = x[keep][:, : len(ts)].copy()
        S[np.arange(len(ts))[None, :] >= first[keep][:, None]] = np.nan  # leave out what follows each decision
        alive = np.isfinite(S).sum(0)
        with np.errstate(invalid="ignore"), __import__("warnings").catch_warnings():
            __import__("warnings").simplefilter("ignore", RuntimeWarning)
            m = np.nanmean(S, 0)
        m[alive < 0.25 * len(S)] = np.nan  # stop where fewer than a quarter of the trials are still deciding
        stim.append(m)
        R = np.array([xs[i, max(0, first[i] - len(tr) + 1): first[i] + 1] for i in np.nonzero(keep)[0]
                      if first[i] >= len(tr) - 1])
        resp.append(R.mean(0) if len(R) else np.full(len(tr), np.nan))
    return {"t_stim": ts, "stim": np.array(stim), "t_resp": tr, "resp": np.array(resp)}


def stepping(n: int = 400, rate: float = 2.0, lo: float = 0.2, hi: float = 0.9, dt: float = 0.005, post=0.8,
             seed: int = 0):
    """Single trials that jump once, from ``lo`` to ``hi``, at an exponential time (rate per second): each trial
    steps, the average ramps (Latimer et al. 2015's point)."""
    rng = np.random.default_rng(seed)
    ts = np.arange(0, post + 1e-9, dt)
    jump = rng.exponential(1 / rate, n)
    trials = np.where(ts[None, :] >= jump[:, None], hi, lo)
    return {"t": ts, "trials": trials, "mean": trials.mean(0), "jump": jump}


# ------------------------------------------------------------------------------------------- stopping
def stop_race(go_rt, ssds, ssrt: float, ssrt_sd: float = 0.0, seed: int = 0) -> dict:
    """Logan and Cowan's independent race: on a stop trial with delay ssd the response escapes when the go time
    is shorter than ssd + the stop time.  ``go_rt`` is a sample of go times; the stop time is ssrt (+ normal
    noise).  Returns P(respond | ssd) and the mean signal-respond RT at each delay."""
    rng = np.random.default_rng(seed)
    go = np.asarray(go_rt, float)
    p, srrt = [], []
    for d in ssds:
        stop = ssrt + ssrt_sd * rng.standard_normal(len(go))
        esc = go < d + stop
        p.append(esc.mean())
        srrt.append(go[esc].mean() if esc.any() else np.nan)
    return {"ssd": np.asarray(ssds, float), "p_respond": np.array(p), "srrt": np.array(srrt)}


def ssrt_integration(go_rt, ssd: float, p_respond: float, go_omissions: float = 0.0) -> float:
    """The integration method: the go-time quantile at P(respond | ssd), minus ssd.  Go omissions are counted as
    responses at the slowest go time (Verbruggen et al. 2019)."""
    go = np.sort(np.asarray(go_rt, float))
    n_om = int(round(go_omissions * len(go) / max(1e-12, 1 - go_omissions)))
    go = np.concatenate([go, np.full(n_om, go[-1])])
    k = max(0, min(len(go) - 1, int(math.ceil(p_respond * len(go))) - 1))
    return float(go[k] - ssd)


def ssrt_mean(go_rt, mean_ssd: float) -> float:
    """The mean method (valid only when P(respond) is near one half): mean go RT minus mean SSD."""
    return float(np.mean(go_rt) - mean_ssd)


# ------------------------------------------------------------------------------------------- confidence
def race_confidence(v_correct, v_error: float = 0.0, b: float = 1.0, n: int = 4000, seed: int = 0,
                    dt: float = 0.002) -> dict:
    """A race of two diffusing accumulators from 0 to b, each held at or above 0 (evidence counts cannot go
    negative); confidence is the balance of evidence (winner minus loser) at the decision, between 0 and b.  For
    each drift: accuracy, and mean confidence on correct and error trials (Vickers 1979's balance of evidence)."""
    rng = np.random.default_rng(seed)
    acc, cc, ce, rt = [], [], [], []
    for v in np.atleast_1d(v_correct):
        x = np.zeros((n, 2))
        drift = np.array([v, v_error])
        conf = np.full(n, np.nan)
        win = np.full(n, -1)
        t = np.full(n, np.nan)
        live = np.ones(n, bool)
        for k in range(1, 20000):
            idx = np.nonzero(live)[0]
            if not len(idx):
                break
            x[idx] = np.maximum(x[idx] + drift * dt + math.sqrt(dt) * rng.standard_normal((len(idx), 2)), 0.0)
            hit = x[idx].max(1) >= b
            fin = idx[hit]
            win[fin] = x[fin].argmax(1)
            conf[fin] = np.minimum(np.abs(x[fin, 0] - x[fin, 1]), b)
            t[fin] = k * dt
            live[fin] = False
        ok = win == 0
        acc.append(ok.mean())
        cc.append(conf[ok].mean())
        ce.append(conf[(win == 1)].mean() if (win == 1).any() else np.nan)
        rt.append(np.nanmean(t))
    return {"v": np.atleast_1d(np.asarray(v_correct, float)), "acc": np.array(acc), "conf_correct": np.array(cc),
            "conf_error": np.array(ce), "mean_dt": np.array(rt)}


# ------------------------------------------------------------------------------------------- value and attention
def addm(v_left: float, v_right: float, d: float = 0.4, theta: float = 0.3, sigma: float = 1.0, bound: float = 1.0,
         n: int = 4000, seed: int = 0, dt: float = 0.002, fix_mean: float = 0.4, max_t: float = 8.0) -> dict:
    """Krajbich, Armel and Rangel's (2010) attentional drift-diffusion model.  The relative decision value moves at
    d (v_left - theta v_right) while the left item is looked at, and d (theta v_left - v_right) while the right
    one is; looks alternate, each lasting an exponential time (mean ``fix_mean`` s, at least 0.1 s), starting on a
    random side.  Returns, per trial, the choice (True = left), the time, and how much longer the left item was
    looked at than the right."""
    rng = np.random.default_rng(seed)
    choice = np.zeros(n, bool)
    rt = np.full(n, np.nan)
    adv = np.zeros(n)
    last_left = np.zeros(n, bool)
    for i in range(n):
        x, t, left = 0.0, 0.0, bool(rng.random() < 0.5)
        tl = tr = 0.0
        while abs(x) < bound and t < max_t:
            dur = max(0.1, rng.exponential(fix_mean))
            steps = int(dur / dt)
            mu = d * (v_left - theta * v_right) if left else d * (theta * v_left - v_right)
            inc = mu * dt + sigma * math.sqrt(dt) * rng.standard_normal(steps)
            path = x + np.cumsum(inc)
            hit = np.nonzero(np.abs(path) >= bound)[0]
            k = int(hit[0]) + 1 if len(hit) else steps
            x = float(path[k - 1])
            t += k * dt
            if left:
                tl += k * dt
            else:
                tr += k * dt
            if len(hit):
                last_left[i] = left
                break
            left = not left
        choice[i], rt[i], adv[i] = x > 0, t, tl - tr
    return {"choice_left": choice, "rt": rt, "left_advantage": adv, "last_left": last_left}


def retest(n_people: int = 120, trials=(20, 50, 100, 200, 500), mu_v: float = 1.5, sd_v: float = 0.25,
           a: float = 1.2, t0: float = 0.3, seed: int = 0) -> dict:
    """How reliable is a fitted drift?  Simulated people with a true drift each (normal, mean ``mu_v``, sd ``sd_v``)
    are tested twice, with a given number of trials per session; EZ diffusion estimates the drift each time, and
    the correlation between sessions is the test-retest reliability."""
    rng = np.random.default_rng(seed)
    true_v = mu_v + sd_v * rng.standard_normal(n_people)
    rs = []
    for m in trials:
        est = np.zeros((2, n_people))
        for s_ in range(2):
            for i, v in enumerate(true_v):
                rt, up = simulate(v, a, 0.5, t0, n=m, seed=int(rng.integers(1 << 30)), dt=0.002)
                ok = np.isfinite(rt)
                rt, up = rt[ok], up[ok]
                pc = min(max(up.mean(), 0.5 + 0.5 / m), 1 - 0.5 / m)
                vr = np.var(rt[up]) if up.sum() > 2 else np.var(rt)
                est[s_, i] = ez(pc, vr, np.mean(rt[up]) if up.any() else np.mean(rt), s=1.0)["v"]
        rs.append(float(np.corrcoef(est[0], est[1])[0, 1]))
    return {"trials": np.array(trials), "r": np.array(rs), "true_v": true_v}
