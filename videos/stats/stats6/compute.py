"""Precompute every number in Part 6 of *Statistics, Built* ("The Laws of Averages").

    python -m videos.stats.stats6.compute            # everything missing (about a minute)
    python -m videos.stats.stats6.compute --force n30

Results are cached in ``.cache/stats6/<name>.json``; scenes call ``load(name)``.  Galton's ox, Bernoulli's urn and the
Port Pirie sea levels are the Museum's; incomes and heights are the World's; everything else is a seeded simulation or
an exact calculation (the convolution powers use Part 2's ``prob.Dist`` in exact fractions).

Items:
    ox           Galton's 787 guesses: the percentile table, the ogive, a normal with Galton's probable error, and a
                 simulated crowd (independent errors vs a shared bias)
    markov       Markov and Chebyshev against the World's incomes and heights; Jensen for log income
    bernoulli    Bernoulli's 25,550 against Chebyshev, Hoeffding, the normal approximation and the exact binomial
    paths        running means of coin tosses: 40 paths of 4,000; the funnel; how many paths stray late
    lopsided     convolution powers of a lopsided law on {0, ..., 5}: exact pmfs, standardized, sup-distance to normal
    board        the Galton board: 12 rows, 600 balls; counts against the binomial
    mgf          n log M(t / sqrt n) -> t^2 / 2 for a centred exponential and for the lopsided law
    demoivre     P(S >= 60) for 100 fair tosses: exact, normal, with continuity correction
    n30          the World's incomes: means of n for n = 5 ... 1,000: sup-distance to normal, t-interval coverage;
                 the same for heights; Berry-Esseen for a lognormal
    delta        the delta method: sqrt of Poisson, arcsine of a binomial share, log of a mean
    slutsky      t-statistics with s for sigma: World heights, World incomes (n = 10, 30, 100)
    cauchy       running means of Cauchy and normal draws; a Pareto(1.5) mean
    hoeffding    exact tail of a binomial share against Hoeffding, Chebyshev and the CLT
    maxima       maxima of exponentials (Gumbel), of uniforms (reversed Weibull), of Paretos (Frechet)
    portpirie    GEV fit to Port Pirie's annual maxima (maximum likelihood), return levels, a profile of the 100-year level
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy import optimize, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.prob import Dist
from explainer.stats.world import World

CACHE = Cache("stats6")
load = CACHE.load
W = World()

LOPSIDED = {0: Fraction(1, 2), 1: Fraction(1, 5), 2: Fraction(1, 20), 3: Fraction(1, 50), 4: Fraction(1, 50),
            5: Fraction(21, 100)}


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, Fraction):
        return float(obj)
    return obj


def compute_ox():
    deg = np.asarray(museum.OX_DEGREES, float)
    est = np.asarray(museum.OX_ESTIMATES, float)
    med = float(np.interp(50, deg, est))
    q1, q3 = float(np.interp(25, deg, est)), float(np.interp(75, deg, est))
    pe = (q3 - q1) / 2  # Galton's probable error
    sd = pe / stats.norm.ppf(0.75)
    normal = med + sd * stats.norm.ppf(deg / 100)
    # a simulated crowd: each guess = truth + independent error (sd 75 lb) + a shared bias of +20 lb
    g = rng(1907)
    ns = np.unique(np.round(np.logspace(0, 3, 40)).astype(int))
    reps = 2000
    indep, shared = [], []
    for n in ns:
        e = g.normal(0, 75, (reps, n)).mean(1)
        indep.append(float(np.sqrt(np.mean(e ** 2))))
        shared.append(float(np.sqrt(np.mean((e + 20) ** 2))))
    return nest({"deg": deg, "est": est, "median": med, "q1": q1, "q3": q3, "pe": pe, "sd": sd, "normal": normal,
                 "truth": museum.OX_TRUTH, "mean": museum.OX_MEAN, "n": museum.OX_N,
                 "err_pct": 100 * (med - museum.OX_TRUTH) / museum.OX_TRUTH,
                 "crowd_ns": ns, "crowd_indep": indep, "crowd_shared": shared})


def compute_markov():
    y = W.income[W.adult]
    h = W.height[W.adult]
    mu = float(y.mean())
    a = np.arange(1, 11)
    frac = [float(np.mean(y >= k * mu)) for k in a]
    ks = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 4.0])
    ch_h = [float(np.mean(np.abs(h - h.mean()) >= k * h.std())) for k in ks]
    ch_y = [float(np.mean(np.abs(y - mu) >= k * y.std())) for k in ks]
    # the income density for the picture (thousands), with the tail beyond 3 * mean shaded
    ed = np.linspace(0, 300, 121)
    hist = np.histogram(y / 1000, ed, density=True)[0]
    return nest({"mu": mu, "sd": float(y.std()), "a": a, "frac": frac, "markov": 1 / a, "ks": ks, "cheb": 1 / ks ** 2,
                 "cheb_height": ch_h, "cheb_income": ch_y, "edges": ed, "hist": hist,
                 "elog": float(np.log(y).mean()), "logE": float(np.log(mu)), "gmean": float(np.exp(np.log(y).mean())),
                 "h_mu": float(h.mean()), "h_sd": float(h.std())})


def exact_n(p, eps, delta, lo, hi):
    """The smallest n in [lo, hi] from which P(|S/n - p| <= eps) >= 1 - delta holds for every larger n in range."""
    ns = np.arange(lo, hi + 1)
    ok = []
    for n in ns:
        k_lo, k_hi = int(np.ceil(n * (p - eps) - 1e-9)), int(np.floor(n * (p + eps) + 1e-9))
        ok.append(stats.binom.cdf(k_hi, n, p) - stats.binom.cdf(k_lo - 1, n, p) >= 1 - delta)
    ok = np.asarray(ok)
    bad = np.where(~ok)[0]
    return int(ns[bad[-1] + 1]) if len(bad) else int(lo), int(ns[np.argmax(ok)])


def compute_bernoulli():
    b = museum.BERNOULLI
    p, eps = b["p"], b["eps"]
    delta = 1 / (b["odds"] + 1)
    cheb = p * (1 - p) / (eps ** 2 * delta)
    hoef = np.log(2 / delta) / (2 * eps ** 2)
    z = stats.norm.ppf(1 - delta / 2)
    norm = z ** 2 * p * (1 - p) / eps ** 2
    ex_all, ex_first = exact_n(p, eps, delta, 5000, 8000)
    return {"bernoulli": b["n"], "chebyshev": float(np.ceil(cheb)), "hoeffding": float(np.ceil(hoef)),
            "normal": float(np.ceil(norm)), "exact": ex_all, "exact_first": ex_first, "delta": delta, "z": float(z)}


def compute_paths():
    g = rng(6)
    n = 4000
    x = g.random((40, n)) < 0.5
    means = np.cumsum(x, 1) / np.arange(1, n + 1)
    idx = np.unique(np.round(np.logspace(0, np.log10(n), 160)).astype(int)) - 1
    # strong-law flavour: of 2,000 paths of 20,000, the share that leave 0.5 +/- 0.02 after step m
    many = (g.random((2000, 20000)) < 0.5).cumsum(1) / np.arange(1, 20001)
    dev = np.abs(many - 0.5) > 0.02
    ms = np.array([100, 500, 1000, 2000, 5000, 10000])
    late = [float(dev[:, m:].any(1).mean()) for m in ms]
    at = [float(dev[:, m - 1].mean()) for m in ms]
    return nest({"steps": idx + 1, "means": means[:, idx], "ms": ms, "late": late, "at": at})


def compute_lopsided():
    d = Dist(LOPSIDED)
    mu, var = d.E(), d.var()
    out = {"mu": mu, "var": var, "skew": float(d.E(lambda x: (x - mu) ** 3)) / float(var) ** 1.5,
           "ns": [1, 2, 3, 5, 10, 30], "pmf": {}, "sup": {}}
    s = Dist({0: Fraction(1)})
    cur = 0
    for n in [1, 2, 3, 5, 10, 30]:
        while cur < n:
            s = s + d
            cur += 1
        ks = np.array(s.support(), float)
        ps = np.array([float(s.P(lambda v, k=k: v == k)) for k in s.support()])
        z = (ks - n * float(mu)) / np.sqrt(n * float(var))
        F = np.cumsum(ps)
        sup = float(np.max(np.abs(F - stats.norm.cdf((ks + 0.5 - n * float(mu)) / np.sqrt(n * float(var))))))
        out["pmf"][str(n)] = {"k": ks, "p": ps, "z": z}
        out["sup"][str(n)] = sup
    return nest(out)


def compute_board():
    g = rng(1873)  # Galton's quincunx, first shown 1873-4
    rows, balls = 12, 600
    bits = (g.random((balls, rows)) < 0.5).astype(int)
    k = bits.sum(1)
    counts = np.bincount(k, minlength=rows + 1)
    expected = balls * stats.binom.pmf(np.arange(rows + 1), rows, 0.5)
    return nest({"rows": rows, "balls": balls, "bits": bits[:40], "k": k, "counts": counts, "expected": expected})


def compute_mgf():
    ts = np.linspace(-2.5, 2.5, 101)
    out = {"t": ts, "target": ts ** 2 / 2, "exp": {}, "lop": {}}
    # centred, standardized exponential: M(t) = e^{-t} / (1 - t), t < 1
    for n in (1, 2, 5, 20, 100):
        u = ts / np.sqrt(n)
        with np.errstate(invalid="ignore", divide="ignore"):
            v = np.where(u < 1, n * (-u - np.log1p(-u)), np.nan)
        out["exp"][str(n)] = v
    d = LOPSIDED
    mu = float(sum(k * float(p) for k, p in d.items()))
    sd = np.sqrt(float(sum((k - mu) ** 2 * float(p) for k, p in d.items())))
    for n in (1, 2, 5, 20, 100):
        u = ts / np.sqrt(n)
        M = sum(float(p) * np.exp(u * (k - mu) / sd) for k, p in d.items())
        out["lop"][str(n)] = n * np.log(M)
    return nest(out)


def compute_demoivre():
    n, p = 100, 0.5
    exact = float(stats.binom.sf(59, n, p))
    mu, sd = n * p, np.sqrt(n * p * (1 - p))
    plain = float(stats.norm.sf((60 - mu) / sd))
    cc = float(stats.norm.sf((59.5 - mu) / sd))
    k = np.arange(30, 71)
    return nest({"exact": exact, "plain": plain, "cc": cc, "k": k, "pmf": stats.binom.pmf(k, n, p), "mu": mu, "sd": sd,
                 "exact_eq": float(stats.binom.pmf(50, n, p)), "approx_eq": float(stats.norm.pdf(0) / sd)})


def mean_sims(pop, ns, reps, g):
    out = {}
    mu, sd = float(pop.mean()), float(pop.std())
    for n in ns:
        idx = g.integers(0, len(pop), (reps, n))
        x = pop[idx]
        m = x.mean(1)
        s = x.std(1, ddof=1)
        z = np.sort((m - mu) / (sd / np.sqrt(n)))
        sup = float(np.max(np.abs(np.arange(1, reps + 1) / reps - stats.norm.cdf(z))))
        t = (m - mu) / (s / np.sqrt(n))
        q = stats.t.ppf(0.975, n - 1)
        cover = float(np.mean(np.abs(t) <= q))
        lo, hi = float(np.mean(t < -q)), float(np.mean(t > q))
        out[str(n)] = {"sup": sup, "cover": cover, "miss_lo": lo, "miss_hi": hi,
                       "hist": np.histogram((m - mu) / (sd / np.sqrt(n)), np.linspace(-4, 4, 61), density=True)[0],
                       "skew_m": float(stats.skew(m))}
    return out


def compute_n30():
    g = rng(30)
    y = W.income[W.adult]
    h = W.height[W.adult]
    ns = [5, 10, 30, 100, 300, 1000]
    inc = mean_sims(y, ns, 20000, g)
    hgt = mean_sims(h, ns, 20000, g)
    # a lognormal with the World's body (sigma 0.55): finite third moment, Berry-Esseen applies
    s = 0.55
    ln = np.exp(s * g.standard_normal(2_000_000))
    lnm = mean_sims(ln, ns, 20000, g)
    mu, sd = ln.mean(), ln.std()
    rho = np.mean(np.abs(ln - mu) ** 3)
    be = [float(0.4748 * rho / (sd ** 3 * np.sqrt(n))) for n in ns]
    return nest({"ns": ns, "income": inc, "height": hgt, "lognormal": lnm, "be": be, "be_ratio": float(rho / sd ** 3),
                 "skew_income": float(stats.skew(y)), "skew_ln": float(stats.skew(ln)),
                 "top_share": float(np.sort(y)[-len(y) // 100:].sum() / y.sum()), "edges": np.linspace(-4, 4, 61)})


def compute_delta():
    lams = np.array([0.5, 1, 2, 4, 8, 16, 32, 64])
    var_sqrt, var_raw = [], []
    for lam in lams:
        k = np.arange(0, int(lam + 40 * np.sqrt(lam) + 40))
        p = stats.poisson.pmf(k, lam)
        e = np.sum(np.sqrt(k) * p)
        var_sqrt.append(float(np.sum(k * p) - e ** 2))
        var_raw.append(float(lam))
    n = 50
    ps = np.linspace(0.02, 0.98, 25)
    var_asin, var_share = [], []
    for pp in ps:
        k = np.arange(n + 1)
        w = stats.binom.pmf(k, n, pp)
        a = np.arcsin(np.sqrt(k / n))
        var_asin.append(float(np.sum(a ** 2 * w) - np.sum(a * w) ** 2))
        var_share.append(float(pp * (1 - pp) / n))
    # log of a mean of 50 World heights: delta says sd(log xbar) = sd / (mu sqrt n)
    g = rng(61)
    h = W.height[W.adult]
    m = h[g.integers(0, len(h), (20000, 50))].mean(1)
    return nest({"lams": lams, "var_sqrt": var_sqrt, "var_raw": var_raw, "n": n, "ps": ps, "var_asin": var_asin,
                 "var_share": var_share, "asin_target": 1 / (4 * n), "log_sd_sim": float(np.log(m).std()),
                 "log_sd_delta": float(h.std() / (h.mean() * np.sqrt(50)))})


def compute_slutsky():
    g = rng(62)
    h = W.height[W.adult]
    y = W.income[W.adult]
    out = {"edges": np.linspace(-5, 5, 81)}
    for name, pop in (("height", h), ("income", y)):
        mu = pop.mean()
        for n in (10, 30, 100):
            x = pop[g.integers(0, len(pop), (20000, n))]
            t = (x.mean(1) - mu) / (x.std(1, ddof=1) / np.sqrt(n))
            out[f"{name}_{n}"] = {"hist": np.histogram(t, out["edges"], density=True)[0],
                                  "cover": float(np.mean(np.abs(t) <= stats.t.ppf(0.975, n - 1))),
                                  "mean_t": float(t.mean())}
    return nest(out)


def compute_cauchy():
    g = rng(1853)  # Cauchy's 1853 note on the law
    n = 10000
    c = g.standard_cauchy((6, n))
    z = g.standard_normal((6, n))
    p = (1 - g.random((6, n))) ** (-1 / 1.5)  # Pareto, alpha 1.5, minimum 1: mean 3, infinite variance
    idx = np.unique(np.round(np.logspace(0, 4, 200)).astype(int)) - 1
    rm = lambda a: (np.cumsum(a, 1) / np.arange(1, n + 1))[:, idx]  # noqa: E731
    # the mean of n Cauchys is Cauchy: quantiles of the mean of 1, 10, 100 draws
    qs = {str(k): np.quantile(g.standard_cauchy((20000, k)).mean(1), [0.25, 0.5, 0.75]) for k in (1, 10, 100)}
    return nest({"steps": idx + 1, "cauchy": rm(c), "normal": rm(z), "pareto": rm(p), "pareto_mean": 3.0, "iqr": qs})


def compute_hoeffding():
    p, eps = 0.6, 0.05
    ns = np.arange(20, 1001, 10)
    exact, hoef, cheb, clt = [], [], [], []
    for n in ns:
        k = np.arange(n + 1)
        exact.append(float(stats.binom.pmf(k, n, p)[np.abs(k / n - p) >= eps - 1e-12].sum()))  # P(|share - p| >= eps)
        hoef.append(float(min(1, 2 * np.exp(-2 * n * eps ** 2))))
        cheb.append(float(min(1, p * (1 - p) / (n * eps ** 2))))
        clt.append(float(2 * stats.norm.sf(eps * np.sqrt(n / (p * (1 - p))))))
    # a check by simulation at n = 200
    g = rng(63)
    sim = float(np.mean(np.abs(g.binomial(200, p, 200000) / 200 - p) > eps - 1e-12))
    return nest({"p": p, "eps": eps, "ns": ns, "exact": exact, "hoeffding": hoef, "chebyshev": cheb, "clt": clt,
                 "sim200": sim})


def compute_maxima():
    g = rng(1928)  # Fisher and Tippett
    out = {}
    xs = np.linspace(-3, 6, 181)
    out["gumbel_x"] = xs
    out["gumbel"] = np.exp(-xs - np.exp(-xs))
    for n in (10, 100, 1000):
        m = g.exponential(size=(20000, n)).max(1) - np.log(n)
        out[f"exp_{n}"] = np.histogram(m, np.linspace(-3, 6, 46), density=True)[0]
        u = n * (1 - g.random((20000, n)).max(1))  # n (1 - max U) -> Exp(1): the reversed Weibull, shape 1
        out[f"unif_{n}"] = np.histogram(u, np.linspace(0, 5, 41), density=True)[0]
        pa = g.pareto(2.0, (20000, n)) + 1  # Pareto alpha 2: max / sqrt(n) -> Frechet(2)
        out[f"par_{n}"] = np.histogram(pa.max(1) / np.sqrt(n), np.linspace(0, 6, 49), density=True)[0]
    out["exp_edges"] = np.linspace(-3, 6, 46)
    out["unif_edges"] = np.linspace(0, 5, 41)
    out["par_edges"] = np.linspace(0, 6, 49)
    ux = np.linspace(0, 5, 101)
    out["unif_x"], out["unif_pdf"] = ux, np.exp(-ux)
    fx = np.linspace(0.05, 6, 120)
    out["frechet_x"], out["frechet_pdf"] = fx, 2 * fx ** -3 * np.exp(-fx ** -2)
    return nest(out)


def gev_nll(theta, x):
    mu, logs, xi = theta
    s = np.exp(logs)
    z = (x - mu) / s
    if abs(xi) < 1e-8:
        return float(len(x) * logs + np.sum(z) + np.sum(np.exp(-z)))
    t = 1 + xi * z
    if np.any(t <= 0):
        return 1e10
    return float(len(x) * logs + (1 + 1 / xi) * np.sum(np.log(t)) + np.sum(t ** (-1 / xi)))


def return_level(mu, s, xi, T):
    yp = -np.log(1 - 1 / T)
    return mu - s / xi * (1 - yp ** (-xi)) if abs(xi) > 1e-8 else mu - s * np.log(yp)


def compute_portpirie():
    x = np.asarray(museum.PORTPIRIE, float)
    years = np.asarray(museum.PORTPIRIE_YEARS)
    r = optimize.minimize(gev_nll, [x.mean(), np.log(x.std()), 0.0], args=(x,), method="Nelder-Mead",
                          options={"xatol": 1e-10, "fatol": 1e-10, "maxiter": 20000})
    mu, logs, xi = r.x
    s = float(np.exp(logs))
    Ts = np.array([2, 5, 10, 20, 50, 100, 200, 500, 1000, 10000])
    rl = [float(return_level(mu, s, xi, T)) for T in Ts]
    # profile log-likelihood for the 100-year level: reparametrize mu by z100
    T = 100
    yp = -np.log(1 - 1 / T)
    zs = np.linspace(4.4, 5.4, 61)
    prof = []
    for z in zs:
        def nll(th, z=z):
            ls, xx = th
            ss = np.exp(ls)
            m = z + ss / xx * (1 - yp ** (-xx)) if abs(xx) > 1e-8 else z + ss * np.log(yp)
            return gev_nll([m, ls, xx], x)
        best = min((optimize.minimize(nll, [logs, x0], method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-9})
                    for x0 in (-0.2, -0.05, 0.1)), key=lambda o: o.fun)
        prof.append(-float(best.fun))
    prof = np.asarray(prof)
    cut = prof.max() - stats.chi2.ppf(0.95, 1) / 2
    above = prof >= cut
    i0, i1 = np.argmax(above), len(above) - 1 - np.argmax(above[::-1])
    lo = float(np.interp(cut, [prof[i0 - 1], prof[i0]], [zs[i0 - 1], zs[i0]]))
    hi = float(np.interp(cut, [prof[i1 + 1], prof[i1]], [zs[i1 + 1], zs[i1]]))
    # empirical return periods (Gringorten-free, simple Weibull plotting positions)
    srt = np.sort(x)
    emp_T = 1 / (1 - np.arange(1, len(x) + 1) / (len(x) + 1))
    return nest({"x": x, "years": years, "mu": float(mu), "sigma": s, "xi": float(xi), "nll": float(r.fun), "Ts": Ts,
                 "rl": rl, "zs": zs, "prof": prof, "ci100": [lo, hi], "cut": float(cut),
                 "sorted": srt, "emp_T": emp_T, "max": float(x.max()), "max_year": int(years[np.argmax(x)])})


ITEMS = {
    "ox": compute_ox, "markov": compute_markov, "bernoulli": compute_bernoulli, "paths": compute_paths,
    "lopsided": compute_lopsided, "board": compute_board, "mgf": compute_mgf, "demoivre": compute_demoivre,
    "n30": compute_n30, "delta": compute_delta, "slutsky": compute_slutsky, "cauchy": compute_cauchy,
    "hoeffding": compute_hoeffding, "maxima": compute_maxima, "portpirie": compute_portpirie,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
