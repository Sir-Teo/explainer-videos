"""Precompute every number in Part 43 of *Statistics, Built* ("Measure-Theoretic Probability").

    OMP_NUM_THREADS=1 python -m videos.stats.stats43.compute            # everything missing (a few minutes)
    python -m videos.stats.stats43.compute --force board

Results are cached in ``.cache/stats43/<name>.json``.  Bortkiewicz's horse kicks, Bernoulli's urn, Port Pirie's sea
levels and the DAX are the Museum's; everything else is exact arithmetic or a seeded simulation.

Items:
    cantor      the Cantor set's measure, the Cantor function (a singular law)
    digits      Borel's binary digits of a uniform; the quantile transform pushing Lebesgue measure to any law
    integral    the escaping bump, the typewriter sequence, X_n = n with probability 1/n, uniform integrability
    fubini      the double array whose iterated sums disagree
    runs        Erdos-Renyi: the longest run of heads in n tosses against log2 n
    series      the random harmonic series and its p = 0.4 cousin; Kolmogorov's 0-1 law
    slln        running means for exponential and Cauchy draws; Etemadi's geometric subsequence
    weak        a binomial and a normal: Kolmogorov, Levy, Wasserstein, the Prokhorov bracket; tightness lost
    horse       Bortkiewicz's horse kicks, the Poisson fit, Le Cam's bound
    cf          characteristic functions, inversion, Levy's tail bound; Heyde's lognormal family with equal moments
    lindeberg   a Lindeberg array and one where a single summand keeps three quarters of the variance
    rates       the lab: exact Kolmogorov and Wasserstein distances of standardized sums against Berry-Esseen and Stein
    stable      symmetric Pareto sums normalized by n^(1/alpha) against the stable limit; the DAX's tails and sums
    ld          Bernoulli's urn: exact tails, the CLT, Chernoff/Cramer; the rate function
    extremes    exact distances of normalized maxima from their limits; Port Pirie's GEV
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import special, stats, optimize
from scipy.integrate import quad

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import limits as LI

CACHE = Cache("stats43")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def histogram_density(values, bins, range):
    """Unconditional density on a finite viewport; omitted tails are not renormalized."""
    values=np.asarray(values,float)
    counts,edges=np.histogram(values,bins=bins,range=range)
    return counts/(len(values)*np.diff(edges)),edges


def normal_lattice_distances(atoms, probabilities):
    """Finite lattice versus standard normal; extrema and quantile cells, no spatial grid."""
    atoms, probabilities = np.asarray(atoms, float), np.asarray(probabilities, float)
    probabilities = probabilities / probabilities.sum()
    right = np.cumsum(probabilities); right[-1] = 1.
    left = np.r_[0., right[:-1]]
    def levy_ok(e):
        return max(np.max(right-stats.norm.cdf(atoms+e)), np.max(stats.norm.cdf(atoms-e)-left)) <= e
    lo, hi = 0., 1.
    for _ in range(55):
        mid = (lo+hi)/2
        if levy_ok(mid): hi=mid
        else: lo=mid
    levy = hi
    def outside(e):
        mass = np.maximum(0., np.minimum(right, stats.norm.cdf(atoms+e))-np.maximum(left, stats.norm.cdf(atoms-e)))
        return 1.-mass.sum()
    lo, hi = 0., 1.
    for _ in range(55):
        mid = (lo+hi)/2
        if outside(mid)<=mid: hi=mid
        else: lo=mid
    # Integrate |atom - Phi^-1(u)| analytically over each quantile cell.
    middle = np.clip(stats.norm.cdf(atoms), left, right)
    pdf_left, pdf_middle, pdf_right = [stats.norm.pdf(stats.norm.ppf(v)) for v in (left,middle,right)]
    wasserstein = np.sum(atoms*(2*middle-left-right)+2*pdf_middle-pdf_left-pdf_right)
    return dict(levy=float(levy), ky_fan=float(hi), wasserstein=float(wasserstein))


def aggregate_returns(returns, width):
    """Nonoverlapping complete blocks; discard the final incomplete block."""
    returns = np.asarray(returns, float)
    return returns[:len(returns)//width*width].reshape(-1,width).sum(1)


def urn_tail(n):
    """P(|K/n - 3/5| >= 1/50); exact rational event boundaries avoid float ceilings."""
    n = np.asarray(n, dtype=np.int64)
    return stats.binom.cdf((29*n)//50,n,.6) + stats.binom.sf((31*n+49)//50-1,n,.6)


def urn_sizes(target):
    lower_rate, upper_rate = LI.bernoulli_rate(.58,.6), LI.bernoulli_rate(.62,.6)
    guaranteed = math.ceil(math.log(2/target)/min(lower_rate,upper_rate))
    ns = np.arange(1,guaranteed+1)
    probabilities = urn_tail(ns)
    first = int(ns[np.flatnonzero(probabilities<=target)[0]])
    safe = int(ns[np.flatnonzero(probabilities>target)[-1]]+1)
    return dict(first_admissible=first, safe_from=safe, checked_through=guaranteed,
                boundary='inclusive |K/n - 3/5| >= 1/50, integer arithmetic',
                all_later_certificate='Exact check through Chernoff threshold; monotone Chernoff envelope thereafter')


def maximum_distance(kind, n, alpha=2.):
    """Continuous supremum with scalar optimization; exact-power CDFs from the kit."""
    if kind in ('exponential','uniform','pareto'):
        def gap(t):
            finite = math.exp(n*math.log1p(-t/n)) if t<n else 0.
            return math.exp(-t)-finite
        result=optimize.minimize_scalar(lambda t:-gap(t),bounds=(0.,min(float(n),40.)),method='bounded',options={'xatol':1e-12})
        return float(-result.fun)
    grid=np.linspace(-8,15,12001)
    gap=np.abs(LI.max_cdf(kind,n,grid)-LI.max_limit(kind,grid))
    local=np.flatnonzero((gap[1:-1]>=gap[:-2]) & (gap[1:-1]>=gap[2:]))+1
    answer=float(gap.max())
    for i in local:
        if gap[i]<1e-10:continue
        result=optimize.minimize_scalar(lambda x:-abs(float(LI.max_cdf(kind,n,x)-LI.max_limit(kind,x))),bounds=(grid[i-1],grid[i+1]),method='bounded')
        answer=max(answer,float(-result.fun))
    return answer


def compute_cantor():
    x = np.linspace(0, 1, 3001)
    return {"x": x, "c": LI.cantor_function(x), "measure": [(2 / 3) ** k for k in range(9)],
            "points": [2 ** k for k in range(9)]}


def compute_digits():
    g = rng(4301)
    u = g.random(20_000)
    d = LI.binary_digits(u, 10)
    run = np.mean(d[:, :3].sum(1) == 3)
    e = -np.log1p(-u)  # the quantile transform of Exp(1)
    h, edges = histogram_density(e, bins=40, range=(0, 6))
    return {"share": d.mean(0), "corr01": float(np.corrcoef(d[:, 0], d[:, 1])[0, 1]), "three_heads": float(run),
            "u_example": float(u[0]), "digits_example": d[0], "exp_hist": h, "exp_edges": edges}


def compute_integral():
    ns = [1, 2, 4, 8, 16, 32]
    # typewriter: the n-th indicator of [j/2^k, (j+1)/2^k) for n = 2^k + j; its L1 norm 2^-k -> 0, but every point is
    # covered once in each block, so f_n(x) -> 0 for no x
    blocks = []
    for k in range(5):
        for j in range(2 ** k):
            blocks.append((k, j, j / 2 ** k, (j + 1) / 2 ** k))
    # X_n = n with probability 1/n: E X_n = 1 for all n, X_n -> 0 in probability; sup E[X 1(X > K)] = 1 for all K
    return {"ns": ns, "bump_integral": [1.0] * len(ns), "typewriter": blocks, "ui_tail": [1.0, 1.0, 1.0]}


def compute_fubini():
    m = 6
    a = np.zeros((m, m))
    for i in range(m):
        a[i, i] = 1.0
        if i + 1 < m:
            a[i, i + 1] = -1.0
    return {"a": a, "row_sums": [1.0 if i == m - 1 else 0.0 for i in range(m)], "col_first": 1.0}


def compute_runs():
    g = rng(4302)
    ns = [2 ** k for k in range(4, 21, 2)]
    out = []
    for n in ns:
        L = []
        for _ in range(200 if n < 2 ** 18 else 40):
            x = g.random(n) < 0.5
            # the longest run of ones
            d = np.diff(np.concatenate([[0], x.astype(int), [0]]))
            starts, ends = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
            L.append(int((ends - starts).max()) if len(starts) else 0)
        out.append({"n": n, "mean": float(np.mean(L)), "lo": float(np.quantile(L, 0.1)), "hi": float(np.quantile(L, 0.9)),
                    "log2": math.log2(n), "reps": len(L), "mc_se": float(np.std(L,ddof=1)/np.sqrt(len(L)))})
    return {"rows": out}


def compute_series():
    g = rng(4303)
    p1 = LI.random_series(1.0, 5000, 12, g)
    p4 = LI.random_series(0.4, 5000, 12, g)
    big = LI.random_series(1.0, 100_000, 400, g)
    tail = np.abs(big[:, -1] - big[:, 49_999])
    return {"p1": p1[:, ::10], "p4": p4[:, ::10], "k": np.arange(1, 5001)[::10], "tail_mean": float(tail.mean()),
            "limit_sd": float(big[:, -1].std()), "var_limit": float(np.pi ** 2 / 6),
            "sum_var_p1": float(np.pi ** 2 / 6)}


def compute_slln():
    g = rng(4304)
    n = 20_000
    k = np.arange(1, n + 1)
    e = np.cumsum(g.exponential(1.0, (6, n)), axis=1) / k
    c = np.cumsum(g.standard_cauchy((6, n)), axis=1) / k
    idx = np.unique(np.round(np.geomspace(1, n, 300)).astype(int)) - 1
    sub = np.unique(np.floor(1.3 ** np.arange(0, 40)).astype(int))
    sub = sub[sub <= n]
    return {"k": k[idx], "exp": e[:, idx], "cauchy": c[:, idx], "sub": sub, "exp_sub": e[0, sub - 1]}


def compute_weak():
    x = np.linspace(-6, 6, 60_001)
    rows = []
    for n in (4, 10, 40, 160):
        b = LI.bernoulli_sum_atoms(n, 0.5)
        F = LI.lattice_cdf(b["atoms"], b["probs"])
        Q = LI.lattice_ppf(b["atoms"], b["probs"])
        k = LI.kolmogorov_lattice(b["atoms"], b["probs"], stats.norm.cdf)
        pb = normal_lattice_distances(b["atoms"], b["probs"])
        rows.append({"n": n, "kolmogorov": k["d"], "at": k["x"], "levy": pb["levy"], "ky_fan": pb["ky_fan"],
                     "wasserstein": pb["wasserstein"]})
    b = LI.bernoulli_sum_atoms(10, 0.5)
    # the Levy square at the worst point, for the picture
    grid = np.linspace(-3.5, 3.5, 701)
    Fb = LI.lattice_cdf(b["atoms"], b["probs"])
    # tightness lost: N(0, n^2) has CDFs converging to 1/2 everywhere, a 'law' with no mass
    return {"rows": rows, "atoms10": b["atoms"], "probs10": b["probs"], "grid": grid, "F10": Fb(grid),
            "k10": LI.kolmogorov_lattice(b["atoms"], b["probs"], stats.norm.cdf), "levy10": rows[1]["levy"]}


def compute_horse():
    k = np.array(museum.HORSEKICK_K)
    nk = np.array(museum.HORSEKICK_N)
    N = int(nk.sum())
    lam = float((k * nk).sum() / N)
    exp_ = N * stats.poisson.pmf(k, lam)
    exp_[-1] = N * stats.poisson.sf(k[-2], lam)
    pooled_obs = np.r_[nk[:2],nk[2:].sum()]
    pooled_expected = np.r_[exp_[:2],exp_[2:].sum()]
    chi2 = float(((pooled_obs-pooled_expected)**2/pooled_expected).sum())
    tv = [{"n": n, "tv": LI.tv_binomial_poisson(n, lam / n), "bound": n * (lam / n) ** 2} for n in (5, 20, 100, 500, 2000)]
    return {"k": k, "obs": nk, "N": N, "lam": lam, "expected": exp_, "chi2": chi2, "p": float(stats.chi2.sf(chi2,1)), "gof": dict(categories=["0","1","2+"],observed=pooled_obs,expected=pooled_expected,df=1,reference="approximate pooled chi-square; lambda estimated"),
            "tv": tv, "deaths": int((k * nk).sum())}


def compute_cf():
    t = np.linspace(-10, 10, 401)
    # the sum of two uniforms on (-1, 1): phi = (sin t / t)^2, the triangular density
    phi = lambda s: np.sinc(np.asarray(s) / np.pi) ** 2  # noqa: E731
    x = np.linspace(-2.5, 2.5, 101)
    f = LI.cf_invert_density(phi, x, T=200.0, m=200_001)
    tri = np.maximum(0, 1 - np.abs(x) / 2) / 2
    g = rng(4305)
    sample = g.uniform(-1, 1, (2, 4000)).sum(0)
    emp = LI.cf_empirical(sample, t)
    # Levy's tail bound for the Cauchy, u = 1: P(|X| > 2) <= 0.43...
    tb = {u: (LI.levy_tail_bound(lambda s: np.exp(-np.abs(s)), u), float(2 * stats.cauchy.sf(2 / u))) for u in (0.5, 1.0, 2.0)}
    # Heyde (1963): f(x)(1 + a sin(2 pi log x)) has the lognormal's moments for |a| <= 1
    xs = np.linspace(0.01, 6, 600)
    ln = stats.lognorm.pdf(xs, 1.0)
    alt = ln * (1 + 0.8 * np.sin(2 * np.pi * np.log(xs)))
    moments = []
    for r in range(1, 5):
        lgrid = np.linspace(-14, 14, 400_001)
        base = np.exp(r * lgrid) * stats.norm.pdf(lgrid)
        m0 = float(np.trapezoid(base, lgrid))
        m1 = float(np.trapezoid(base * (1 + 0.8 * np.sin(2 * np.pi * lgrid)), lgrid))
        moments.append((r, m0, m1))
    return {"t": t, "phi": phi(t), "emp_re": np.real(emp), "x": x, "f": f, "tri": tri, "tail": tb, "xs": xs, "ln": ln,
            "alt": alt, "moments": moments}


def compute_lindeberg():
    g = rng(4306)
    reps = 200_000
    out = {}
    # (a) equal uniforms: Lindeberg holds
    n = 20
    s = g.uniform(-1, 1, (reps, n)).sum(1) / math.sqrt(n / 3)
    out["equal"] = {"ks": float(stats.kstest(s, "norm").statistic), "hist": histogram_density(s, bins=60, range=(-4, 4))[0]}
    # (b) Rademacher steps with Var X_k = 4^k: the last carries three quarters of the variance
    k = np.arange(1, n + 1)
    sd = 2.0 ** k
    signs = g.choice([-1.0, 1.0], (reps, n))
    t = (signs * sd).sum(1) / math.sqrt((sd ** 2).sum())
    out["dominant"] = {"ks": float(stats.kstest(t, "norm").statistic), "hist": histogram_density(t, bins=60, range=(-4, 4))[0],
                       "share_last": float(sd[-1] ** 2 / (sd ** 2).sum())}
    edges = np.linspace(-4, 4, 61)
    out["mid"] = (edges[:-1] + edges[1:]) / 2
    # the Lindeberg quantity L_n(eps) for each array at eps = 0.5
    out["L_equal"] = 0.0  # |X_k| <= 1 < 0.5 sqrt(n/3) once n >= 12: the truncated sum is zero
    s2 = (sd ** 2).sum()
    out["L_dominant"] = float(np.sum(np.where(sd > 0.5 * math.sqrt(s2), sd ** 2, 0.0)) / s2)
    return out


def compute_rates():
    ns = [2 ** k for k in range(0, 11)]
    x = np.linspace(-10, 40, 120_001)
    rows = {}
    for kind in ("bernoulli", "bernoulli01", "exponential", "poisson"):
        rho = LI.third_abs_moment("bernoulli", 0.1) if kind == "bernoulli01" else LI.third_abs_moment(kind)
        kd, wd = [], []
        for n in ns:
            if kind in ("bernoulli", "bernoulli01"):
                p = 0.1 if kind == "bernoulli01" else 0.5
                b = LI.bernoulli_sum_atoms(n, p)
                kd.append(LI.kolmogorov_lattice(b["atoms"], b["probs"], stats.norm.cdf)["d"])
                wd.append(normal_lattice_distances(b["atoms"],b["probs"])["wasserstein"])
            elif kind == "poisson":
                b = LI.poisson_sum_atoms(n, 1.0)
                kd.append(LI.kolmogorov_lattice(b["atoms"], b["probs"], stats.norm.cdf)["d"])
                wd.append(normal_lattice_distances(b["atoms"],b["probs"])["wasserstein"])
            else:
                F = LI.exponential_sum_cdf(n)
                kd.append(LI.kolmogorov(F, stats.norm.cdf, x))
                wd.append(LI.wasserstein1(F, stats.norm.cdf, x))
        slope = float(np.polyfit(np.log(ns[4:]), np.log(kd[4:]), 1)[0])
        rows[kind] = {"rho": rho, "kolmogorov": kd, "wasserstein": wd, "be": [LI.berry_esseen(rho, n) for n in ns],
                      "stein": [LI.stein_wasserstein(rho, n) for n in ns], "slope": slope,
                      "ratio_be": float(np.max(np.array(kd) / np.array([LI.berry_esseen(rho, n) for n in ns])))}
    # the exponential's distance at n = 30, the folklore threshold
    k30 = LI.kolmogorov(LI.exponential_sum_cdf(30), stats.norm.cdf, x)
    return {"ns": ns, "rows": rows, "k30": k30, "be30": LI.berry_esseen(LI.third_abs_moment("exponential"), 30)}


def compute_stable():
    g = rng(4307)
    alpha = 1.5
    c = float(special.gamma(1 - alpha) * math.cos(math.pi * alpha / 2))  # the limit's chf exp(-c |t|^alpha)
    out = {"alpha": alpha, "c": c, "rows": []}
    t = np.array([0.25, 0.5, 1.0, 2.0])
    for n in (10, 100, 1000):
        reps = 20_000
        x = (1 - g.random((reps, n))) ** (-1 / alpha) * g.choice([-1.0, 1.0], (reps, n))
        s = x.sum(1) / n ** (1 / alpha)
        emp = np.real(LI.cf_empirical(s, t))
        out["rows"].append({"n": n, "emp": emp, "limit": np.exp(-c * t ** alpha), "q90": float(np.quantile(np.abs(s), 0.9))})
    z = LI.stable_sample(alpha, 0.0, 200_000, g) * c ** (1 / alpha)
    out["limit_q90"] = float(np.quantile(np.abs(z), 0.9))
    # the DAX
    D = museum.eustock()["DAX"]
    r = np.diff(np.log(D))
    out["dax_n"] = len(r)
    out["dax_hill"] = {str(k): LI.hill(r - r.mean(), k) for k in (25, 50, 100)}
    out["dax_kurt"] = float(stats.kurtosis(r))
    ks = []
    for m in (1, 5, 20):
        s = aggregate_returns(r-r.mean(),m)
        zz = (s - s.mean()) / s.std()
        ks.append({"m": m, "n": len(zz), "ks": float(stats.kstest(zz, "norm").statistic), "kurt": float(stats.kurtosis(zz))})
    out["dax_sums"] = ks
    zr = (r - r.mean()) / r.std()
    out["dax_hist"] = histogram_density(zr, bins=60, range=(-6, 6))[0]
    out["dax_tail"] = float(np.mean(np.abs(zr) > 4))
    out["normal_tail"] = float(2 * stats.norm.sf(4))
    return out


def compute_ld():
    p, eps = museum.BERNOULLI["p"], museum.BERNOULLI["eps"]
    target = 1 / (museum.BERNOULLI["odds"] + 1)
    ns = np.unique(np.round(np.geomspace(100, 30000, 60)).astype(int))
    exact, clt, chern = [], [], []
    Ihi, Ilo = LI.bernoulli_rate(p + eps, p), LI.bernoulli_rate(p - eps, p)
    for n in ns:
        exact.append(float(urn_tail(n)))
        clt.append(float(2 * stats.norm.sf(eps * math.sqrt(n / (p * (1 - p))))))
        chern.append(float(math.exp(-n * Ihi) + math.exp(-n * Ilo)))

    def first(v):
        v = np.asarray(v)
        i = np.flatnonzero(v <= target)
        return int(ns[i[0]]) if len(i) else None

    sizes=urn_sizes(target)
    n_exact=sizes["safe_from"]
    a = np.linspace(0.01, 0.99, 197)
    rate = [LI.bernoulli_rate(v, p) for v in a]
    return {"p": p, "eps": eps, "target": target, "ns": ns, "exact": exact, "clt": clt, "chernoff": chern,
            "n_bernoulli": museum.BERNOULLI["n"], "n_exact": n_exact, "size_certificate": sizes,
            "n_clt": int(math.ceil((stats.norm.isf(target / 2) / eps) ** 2 * p * (1 - p))),
            "n_chernoff": int(math.ceil(math.log(2 / target) / min(Ihi, Ilo))), "I_hi": Ihi, "I_lo": Ilo,
            "a": a, "rate": rate, "quad": [(v - p) ** 2 / (2 * p * (1 - p)) for v in a]}


def compute_extremes():
    x = np.linspace(-3, 8, 4401)
    rows = {}
    for kind in ("exponential", "uniform", "normal"):
        xx = np.linspace(-6, 0, 2401) if kind == "uniform" else x
        rows[kind] = [{"n": n, "d": maximum_distance(kind,n)} for n in (10, 100, 1000, 10_000, 100_000)]
    xp = np.linspace(0.02, 20, 4000)
    rows["pareto"] = [{"n": n, "d": maximum_distance("pareto",n)} for n in (10, 100, 1000, 10_000, 100_000)]
    # curves for the picture: exponential and normal maxima at n = 10 and 1000 against the Gumbel
    g = np.linspace(-3, 6, 300)
    curves = {f"{k}_{n}": LI.max_cdf(k, n, g) for k in ("exponential", "normal") for n in (10, 1000)}
    pp = np.array(museum.PORTPIRIE)
    c, loc, scale = stats.genextreme.fit(pp)
    xi = -c
    rl = float(stats.genextreme.isf(0.01, c, loc, scale))
    gum = stats.gumbel_r.fit(pp)
    return {"rows": rows, "g": g, "curves": curves, "gumbel": LI.gev_cdf(g, 0.0), "pp": pp, "pp_years": museum.PORTPIRIE_YEARS,
            "xi": float(xi), "loc": float(loc), "scale": float(scale), "rl100": rl, "gumbel_fit": [float(v) for v in gum],
            "rl100_gumbel": float(stats.gumbel_r.isf(0.01, *gum)), "pp_max": float(pp.max())}


def compute_board():
    rows = []
    z = stats.norm.ppf(0.95)
    specs = [("uniform", 10, "t interval for a mean", "Uniform(0, 1), n = 10"),
             ("exponential", 10, "t interval for a mean", "Exp(1), n = 10"),
             ("exponential", 100, "t interval for a mean", "Exp(1), n = 100"),
             ("exponential", 1000, "t interval for a mean", "Exp(1), n = 1,000"),
             ("pareto25", 100, "t interval for a mean", "Pareto, alpha = 2.5 (finite variance), n = 100"),
             ("pareto15", 1000, "t interval for a mean", "Pareto, alpha = 1.5 (infinite variance), n = 1,000")]
    g = rng(4310)
    for kind, n, method, setting in specs:
        reps = 20_000 if n < 1000 else 10_000
        cov = np.zeros(reps, bool)
        for i in range(0, reps, 1000):
            m = min(1000, reps - i)
            if kind == "uniform":
                x, mu = g.random((m, n)), 0.5
            elif kind == "exponential":
                x, mu = g.exponential(1.0, (m, n)), 1.0
            elif kind == "pareto25":
                x, mu = (1 - g.random((m, n))) ** (-1 / 2.5), 2.5 / 1.5
            else:
                x, mu = (1 - g.random((m, n))) ** (-1 / 1.5), 1.5 / 0.5
            xb, s = x.mean(1), x.std(1, ddof=1)
            q = stats.t.ppf(0.95, n - 1)
            cov[i:i + m] = np.abs(xb - mu) <= q * s / math.sqrt(n)
        rows.append(Row(43, method, setting, "coverage", 0.9, float(cov.mean()), reps, mc_se=float(cov.std(ddof=1)/np.sqrt(reps))))
    save_rows(43, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "z": float(z)}


ITEMS = {
    "cantor": compute_cantor, "digits": compute_digits, "integral": compute_integral, "fubini": compute_fubini,
    "runs": compute_runs, "series": compute_series, "slln": compute_slln, "weak": compute_weak, "horse": compute_horse,
    "cf": compute_cf, "lindeberg": compute_lindeberg, "rates": compute_rates, "stable": compute_stable, "ld": compute_ld,
    "extremes": compute_extremes, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
