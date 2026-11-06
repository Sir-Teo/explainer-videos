"""Precompute every number in Part 3 of *Statistics, Built* ("The Family of Distributions").

    python -m videos.stats.stats3.compute            # everything missing (well under a minute)
    python -m videos.stats.stats3.compute --force rare

Results are cached in ``.cache/stats3/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Exact pmfs come from the
probability engine (``explainer.stats.prob``) or from scipy; every limit and identity is checked against a seeded
simulation.  The horse kicks are the Museum's (Bortkiewicz 1898); the lake and the towns are the World's.

Items:
    horsekick   Bortkiewicz's 200 corps-years against Poisson(0.61); 200 simulated corps-years
    binomial    Binomial(10, 0.3) by the engine; 40 lattice paths; mean and variance by indicators
    rare        Binomial(n, 2/n) against Poisson(2) for n = 4 ... 1000: total variation and Le Cam's bound
    waiting     the geometric (first six), memorylessness, the negative binomial; gamma-Poisson simulated
    capture     the World's lake: capture 500, recapture 400, the hypergeometric count of tagged fish; Lincoln-Petersen
                and Chapman estimates over 2,000 repetitions
    process     a Poisson process of buses (one every 10 minutes on average): gaps, waits, the inspection paradox
    normal      Binomial(n, 1/2) against de Moivre's curve; Herschel-Maxwell: rotation-invariant 2D cloud
    transforms  the CDF method on -log U; Box-Muller pairs; a product of 60 random factors (the log-normal)
    sampling    chi-square, t and F densities; the lighthouse (Cauchy) and its running mean against a normal's
    order       order statistics of 10 uniforms (Beta); the German tank estimate
    tails       the World's town sizes (Zipf), income tail; log-log least squares against the MLE (Clauset et al.)
    mgf         moment generating functions: normal, Poisson; the sum of independent Poissons
    mixtures    beta-binomial (overdispersion), gamma-Poisson = negative binomial, normal scale mixture = t
    expfam      exponential families: A'(eta) = E T checked for Bernoulli, Poisson, normal
"""

from __future__ import annotations

import math

import numpy as np
from scipy import special, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.prob import Dist, coin
from explainer.stats.world import World

CACHE = Cache("stats3")
load = CACHE.load
W = World()


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    """Arrays inside lists and dicts as plain lists (the cache stores only top-level arrays in .npz)."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    return obj


# ---------------------------------------------------------------------------
def compute_horsekick():
    k, n = np.array(museum.HORSEKICK_K), np.array(museum.HORSEKICK_N)
    total = int(n.sum())
    lam = float((k * n).sum() / total)
    expected = total * stats.poisson.pmf(k, lam)
    expected[-1] = total * stats.poisson.sf(k[-2], lam)  # 4 or more
    chi2 = float(((n - expected) ** 2 / expected).sum())
    g = rng(1898)
    sim = g.poisson(lam, total)
    sim_counts = np.bincount(np.minimum(sim, 4), minlength=5)
    var = float(((k - lam) ** 2 * n).sum() / (total - 1))
    return {"k": k, "n": n, "total": total, "deaths": int((k * n).sum()), "lam": lam, "expected": expected,
            "chi2": chi2, "sim_counts": sim_counts, "var": var}


def compute_binomial():
    n, p = 10, 0.3
    d = coin(p, heads=1, tails=0).iid_sum(n)
    pmf = [float(d.P(k)) for k in range(n + 1)]
    assert np.allclose(pmf, stats.binom.pmf(range(n + 1), n, p))
    g = rng(1713)
    steps = g.random((40, n)) < p
    paths = np.cumsum(steps, axis=1)
    many = (g.random((20_000, n)) < p).sum(axis=1)
    # a poll: how many of 100 World adults are taller than 180 cm?
    h = W.height[W.adult]
    p180 = float((h > 180).mean())
    polls = np.array([int((W.height[W.sample(100, among=W.adult, seed=7000 + s)] > 180).sum()) for s in range(2000)])
    poll_k = np.arange(0, 41)
    poll_emp = np.bincount(polls, minlength=41)[:41] / len(polls)
    poll_pmf = stats.binom.pmf(poll_k, 100, p180)
    return {"p180": p180, "poll_k": poll_k, "poll_emp": poll_emp, "poll_pmf": poll_pmf,
            "poll_mean": float(polls.mean()), "poll_var": float(polls.var()),
            "n": n, "p": p, "pmf": pmf, "E": float(d.E()), "Var": float(d.var()), "paths": steps.astype(int),
            "ends": paths[:, -1], "sim_mean": float(many.mean()), "sim_var": float(many.var()),
            "c_10_3": math.comb(10, 3)}


def compute_rare():
    lam = 2.0
    ns = [4, 10, 50, 1000]
    ks = np.arange(0, 11)
    pois = stats.poisson.pmf(ks, lam)
    rows = []
    for n in ns:
        b = stats.binom.pmf(ks, n, lam / n)
        kk = np.arange(0, n + 1)
        tv = 0.5 * (np.abs(stats.binom.pmf(kk, n, lam / n) - stats.poisson.pmf(kk, lam)).sum() + stats.poisson.sf(n, lam))
        rows.append({"n": n, "pmf": b, "tv": float(tv), "lecam": lam ** 2 / n})
    grid = np.unique(np.round(np.geomspace(2, 2000, 60)).astype(int))
    tvs, bounds = [], []
    for n in grid:
        kk = np.arange(0, n + 1)
        tvs.append(0.5 * (np.abs(stats.binom.pmf(kk, n, lam / n) - stats.poisson.pmf(kk, lam)).sum()
                          + stats.poisson.sf(n, lam)))
        bounds.append(min(1.0, lam ** 2 / n))
    return {"lam": lam, "ks": ks, "pois": pois, "rows": nest(rows), "grid": grid, "tvs": np.array(tvs),
            "bounds": np.array(bounds)}


def compute_waiting():
    p = 1 / 6
    ks = np.arange(1, 31)
    geo = stats.geom.pmf(ks, p)
    g = rng(1654)
    waits = g.geometric(p, 50_000)
    # memorylessness: P(T > s + t | T > s) = P(T > t), s = 5, t = 3
    s_, t_ = 5, 3
    lhs = float((waits > s_ + t_).sum() / (waits > s_).sum())
    rhs = float((waits > t_).mean())
    exact = (5 / 6) ** t_
    # negative binomial: tosses to the 3rd six
    r = 3
    nb = stats.nbinom.pmf(ks - r, r, p)  # scipy counts failures
    # gamma-Poisson: Poisson with a gamma-distributed rate
    shape, scale = 2.0, 1.5
    rates = g.gamma(shape, scale, 50_000)
    counts = g.poisson(rates)
    kk = np.arange(0, 16)
    nb2 = stats.nbinom.pmf(kk, shape, 1 / (1 + scale))
    emp = np.bincount(counts, minlength=16)[:16] / len(counts)
    return {"p": p, "ks": ks, "geo": geo, "mean_wait": float(waits.mean()), "lhs": lhs, "rhs": rhs, "exact_ml": exact,
            "s": s_, "t": t_, "r": r, "nb": nb, "gp_k": kk, "gp_nb": nb2, "gp_emp": emp,
            "gp_mean": float(counts.mean()), "gp_var": float(counts.var()), "shape": shape, "scale": scale}


def compute_capture():
    N = W.lake["n_fish"]
    n1, n2 = 500, 400
    g = rng(1662)
    tagged = np.zeros(N, bool)
    tagged[g.choice(N, n1, replace=False)] = True
    second = g.choice(N, n2, replace=False)
    m = int(tagged[second].sum())
    reps = 2000
    ms = stats.hypergeom.rvs(N, n1, n2, size=reps, random_state=g)
    with np.errstate(divide="ignore"):
        lp = n1 * n2 / ms  # zero recaptures mean no finite ratio estimate, never impute one
    chap = (n1 + 1) * (n2 + 1) / (ms + 1) - 1
    kk = np.arange(0, 61)
    hyp = stats.hypergeom.pmf(kk, N, n1, n2)
    bino = stats.binom.pmf(kk, n2, n1 / N)
    return {"N": N, "n1": n1, "n2": n2, "m": m, "estimate": n1 * n2 / m, "chapman": (n1 + 1) * (n2 + 1) / (m + 1) - 1,
            "lp": lp, "chap": chap, "lp_mean": float(lp.mean()), "chap_mean": float(chap.mean()),
            "lp_sd": float(lp.std()), "kk": kk, "hyp": hyp, "bino": bino, "mean_m": n2 * n1 / N}


def compute_process():
    g = rng(1909)
    mean_gap = 10.0
    T = 600.0
    gaps = g.exponential(mean_gap, 200)
    times = np.cumsum(gaps)
    times = times[times < T]
    long_gaps = g.exponential(mean_gap, 200_000)
    arrivals = np.cumsum(long_gaps)
    pas = g.uniform(0, arrivals[-1], 20_000)
    idx = np.searchsorted(arrivals, pas)
    nxt = arrivals[idx]
    prv = np.where(idx > 0, arrivals[np.maximum(idx - 1, 0)], 0.0)
    wait = nxt - pas
    seen = nxt - prv
    counts = np.histogram(arrivals, np.arange(0, arrivals[-1], 60.0))[0]  # buses per hour
    # gamma: time to the 3rd bus
    third = g.gamma(3, mean_gap, 50_000)
    a_bus = np.cumsum(g.exponential(10.0, 30_000))
    b_bus = np.cumsum(g.exponential(15.0, 20_000))
    horizon = min(a_bus[-1], b_bus[-1])
    merged = np.sort(np.r_[a_bus[a_bus < horizon], b_bus[b_bus < horizon]])
    merged_gap = float(np.diff(merged).mean())
    room = a_bus[g.random(len(a_bus)) < 0.6]
    room_gap = float(np.diff(room).mean())
    return {"merged_gap": merged_gap, "room_gap": room_gap, "a_sample": a_bus[a_bus < 120], "b_sample": b_bus[b_bus < 120],
            "mean_gap": mean_gap, "times": times, "wait_mean": float(wait.mean()), "seen_mean": float(seen.mean()),
            "seen": seen[:4000], "gaps_sample": long_gaps[:4000], "per_hour": counts[:2000],
            "per_hour_mean": float(counts.mean()), "per_hour_var": float(counts.var()), "third": third[:20000]}


def compute_normal():
    out = []
    for n in (10, 50, 200):
        k = np.arange(0, n + 1)
        out.append({"n": n, "pmf": stats.binom.pmf(k, n, 0.5)})
    g = rng(1850)
    xy = g.normal(0, 1, (1500, 2))
    r = np.hypot(xy[:, 0], xy[:, 1])
    th = np.arctan2(xy[:, 1], xy[:, 0])
    stirling = [(n, math.factorial(n), math.sqrt(2 * math.pi * n) * (n / math.e) ** n) for n in (1, 5, 10, 20)]
    men = W.height[W.adult & W.male]
    mu, sd = float(men.mean()), float(men.std())
    within = [float((np.abs(men - mu) < k * sd).mean()) for k in (1, 2, 3)]
    rule = [float(stats.norm.cdf(k) - stats.norm.cdf(-k)) for k in (1, 2, 3)]
    return {"men_mu": mu, "men_sd": sd, "within": within, "rule": rule, "n_men": int(men.size),
            "binoms": nest(out), "xy": xy, "theta_hist": np.histogram(th, np.linspace(-np.pi, np.pi, 25))[0],
            "r_mean": float(r.mean()), "stirling": [[n, float(a), float(b), float(a / b)] for n, a, b in stirling],
            "gauss_integral": float(np.sqrt(np.pi))}


def compute_transforms():
    g = rng(1958)
    u = g.random(20_000)
    e = -np.log(u)
    u1, u2 = g.random(3000), g.random(3000)
    r = np.sqrt(-2 * np.log(u1))
    z1, z2 = r * np.cos(2 * np.pi * u2), r * np.sin(2 * np.pi * u2)
    factors = g.uniform(0.8, 1.25, (20_000, 60))
    prod = factors.prod(axis=1)
    logp = np.log(prod)
    return {"u": u[:3000], "e": e, "e_mean": float(e.mean()), "u1": u1, "u2": u2, "z1": z1, "z2": z2,
            "z_mean": float(np.mean(np.r_[z1, z2])), "z_sd": float(np.std(np.r_[z1, z2])), "prod": prod,
            "logp_mean": float(logp.mean()), "logp_sd": float(logp.std()),
            "logp_skew": float(stats.skew(logp)), "prod_skew": float(stats.skew(prod))}


def compute_sampling():
    g = rng(1908)
    xs = np.linspace(0.001, 12, 400)
    chi = {k: stats.chi2.pdf(xs, k) for k in (1, 2, 3, 5)}
    ts = np.linspace(-5, 5, 400)
    tden = {nu: stats.t.pdf(ts, nu) for nu in (1, 3, 30)}
    fx = np.linspace(0.001, 5, 400)
    fden = stats.f.pdf(fx, 5, 10)
    # chi-square as a sum of squares: 20,000 sums of 3 squared normals
    s3 = (g.normal(0, 1, (20_000, 3)) ** 2).sum(axis=1)
    # the lighthouse: 1 km offshore, beam at a uniform angle
    ang = g.uniform(-np.pi / 2, np.pi / 2, 20_000)
    pos = np.tan(ang)
    run_c = np.cumsum(pos) / np.arange(1, len(pos) + 1)
    norm = g.normal(0, 1, 20_000)
    run_n = np.cumsum(norm) / np.arange(1, len(norm) + 1)
    return {"xs": xs, "chi": nest({str(k): v for k, v in chi.items()}), "ts": ts, "tden": nest({str(k): v for k, v in tden.items()}),
            "normal": stats.norm.pdf(ts), "fx": fx, "fden": fden, "s3": s3[:20000], "s3_mean": float(s3.mean()),
            "s3_var": float(s3.var()), "pos": pos[:300], "ang": ang[:300], "run_c": run_c, "run_n": run_n}


def compute_order():
    g = rng(1943)
    n = 10
    u = np.sort(g.random((20_000, n)), axis=1)
    xs = np.linspace(0, 1, 300)
    beta = {k: stats.beta.pdf(xs, k, n + 1 - k) for k in (1, 3, 8, 10)}
    hists = {k: np.histogram(u[:, k - 1], np.linspace(0, 1, 41), density=True)[0] for k in (1, 3, 8, 10)}
    # the German tank problem: serials 1..N, N = 300; a sample of 8 serial numbers
    N_true, m = 300, 8
    serial = np.sort(g.choice(np.arange(1, N_true + 1), m, replace=False))
    est = serial.max() * (1 + 1 / m) - 1
    reps = np.array([np.max(g.choice(np.arange(1, N_true + 1), m, replace=False)) for _ in range(5000)])
    ests = reps * (1 + 1 / m) - 1
    return {"n": n, "xs": xs, "beta": nest({str(k): v for k, v in beta.items()}), "hists": nest({str(k): v for k, v in hists.items()}),
            "N": N_true, "m": m, "serial": serial, "est": float(est), "ests_mean": float(ests.mean()),
            "max_mean": float(reps.mean()), "ests_sd": float(ests.std())}


def compute_tails():
    pops = np.sort(W.towns["pop"] if "pop" in W.towns else np.bincount(W.town, minlength=200))[::-1]
    ranks = np.arange(1, len(pops) + 1)
    slope_rank, intercept_rank = np.polyfit(np.log(ranks[:150]), np.log(pops[:150]), 1)
    # Clauset-Shalizi-Newman: fitting a power law by least squares on a log-log histogram is biased
    g = rng(2009)
    alpha, xmin, n = 2.5, 1.0, 500
    ls, mle = [], []
    for _ in range(400):
        x = xmin * (1 - g.random(n)) ** (-1 / (alpha - 1))  # density ~ x^-alpha
        edges = np.logspace(0, np.log10(x.max()) + 1e-9, 25)
        h, e = np.histogram(x, edges, density=True)
        mid = np.sqrt(e[:-1] * e[1:])
        ok = h > 0
        ls.append(-np.polyfit(np.log(mid[ok]), np.log(h[ok]), 1)[0])
        mle.append(1 + n / np.log(x / xmin).sum())
    x = xmin * (1 - g.random(n)) ** (-1 / (alpha - 1))
    edges = np.logspace(0, np.log10(x.max()) + 1e-9, 25)
    h, e = np.histogram(x, edges, density=True)
    mid = np.sqrt(e[:-1] * e[1:])
    inc = np.sort(W.income[W.adult])[::-1]
    shares = {str(q): float(inc[: int(q * len(inc))].sum() / inc.sum()) for q in (0.01, 0.1, 0.2)}
    a8020 = math.log(5) / math.log(4)
    qs = np.linspace(0.01, 1, 100)
    lorenz_par = {str(a): (qs ** (1 - 1 / a)).tolist() for a in (1.16, 2.0, 3.0)}
    return {"shares": shares, "a8020": a8020, "qs": qs, "lorenz_par": lorenz_par,
            "pops": pops, "ranks": ranks, "slope_rank": float(slope_rank), "intercept_rank": float(intercept_rank), "alpha": alpha, "n": n,
            "ls": np.array(ls), "mle": np.array(mle), "ls_mean": float(np.mean(ls)), "ls_sd": float(np.std(ls)),
            "mle_mean": float(np.mean(mle)), "mle_sd": float(np.std(mle)), "ex_mid": mid[h > 0], "ex_h": h[h > 0]}


def compute_mgf():
    g = rng(1812)
    a, b = 1.5, 2.5
    s = g.poisson(a, 50_000) + g.poisson(b, 50_000)
    kk = np.arange(0, 14)
    return {"a": a, "b": b, "kk": kk, "emp": np.bincount(s, minlength=14)[:14] / len(s),
            "pois": stats.poisson.pmf(kk, a + b)}


def compute_mixtures():
    g = rng(1925)
    n = 20
    a, b = 2.0, 3.0
    p = g.beta(a, b, 50_000)
    bb = g.binomial(n, p)
    plain = g.binomial(n, a / (a + b), 50_000)
    kk = np.arange(0, n + 1)
    bb_pmf = stats.betabinom.pmf(kk, n, a, b)
    bin_pmf = stats.binom.pmf(kk, n, a / (a + b))
    # scale mixture: Z / sqrt(V/nu), V ~ chi2_nu  <=>  normal with variance nu / V
    nu = 3
    var = nu / g.chisquare(nu, 50_000)
    x = g.normal(0, np.sqrt(var))
    ts = np.linspace(-6, 6, 300)
    return {"n": n, "a": a, "b": b, "kk": kk, "bb_pmf": bb_pmf, "bin_pmf": bin_pmf,
            "bb_emp": np.bincount(bb, minlength=n + 1)[:n + 1] / len(bb), "bb_var": float(bb.var()),
            "bin_var": float(plain.var()), "mean": n * a / (a + b), "nu": nu, "t_x": x[:20000],
            "ts": ts, "tden": stats.t.pdf(ts, nu), "nden": stats.norm.pdf(ts)}


def compute_expfam():
    rows = []
    # Bernoulli: eta = log(p/(1-p)), A = log(1 + e^eta)
    for p in (0.2, 0.5, 0.9):
        eta = math.log(p / (1 - p))
        h = 1e-5
        A = lambda e: math.log1p(math.exp(e))  # noqa: E731
        rows.append(("Bernoulli", p, (A(eta + h) - A(eta - h)) / (2 * h), p))
    for lam in (0.5, 2.0, 7.0):
        eta = math.log(lam)
        h = 1e-5
        A = math.exp
        rows.append(("Poisson", lam, (A(eta + h) - A(eta - h)) / (2 * h), lam))
    return {"rows": [[r[0], r[1], r[2], r[3]] for r in rows]}


ITEMS = {
    "horsekick": compute_horsekick, "binomial": compute_binomial, "rare": compute_rare, "waiting": compute_waiting,
    "capture": compute_capture, "process": compute_process, "normal": compute_normal, "transforms": compute_transforms,
    "sampling": compute_sampling, "order": compute_order, "tails": compute_tails, "mgf": compute_mgf,
    "mixtures": compute_mixtures, "expfam": compute_expfam,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
