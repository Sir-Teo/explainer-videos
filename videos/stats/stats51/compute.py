"""Precompute every number in Part 51 of *Statistics, Built* ("High-Dimensional Probability").

    OMP_NUM_THREADS=1 python -m videos.stats.stats51.compute            # everything missing (a few minutes)
    python -m videos.stats.stats51.compute --force board

Results are cached in ``.cache/stats51/<name>.json``.  The Wisconsin breast cancer data are the Museum's; everything
else is exact arithmetic or a seeded simulation.

Items:
    hook      the equatorial band's mass by n; the half-width holding 95%; the coordinate's law for n = 3, 10, 100, 1000
    shells    norms of Gaussian vectors by n; inner products and angles of random directions
    jl        Johnson-Lindenstrauss: distortion of 200 points in R^5000 by projection dimension k
    tails     Hoeffding, Bernstein and Chernoff against the exact binomial tail, p = 0.5 and p = 0.02
    orlicz    empirical psi_2 and psi_1 norms of common laws
    lipschitz the maximum of n Gaussians: mean, SD and tail against Gaussian concentration
    matrices  extreme singular values against sqrt(n) +- sqrt(p); covariance error by n; Marchenko-Pastur
    bernstein matrix Bernstein against simulation
    compare   Slepian: the expected maximum of exchangeable Gaussians by correlation; Sudakov
    chaining  Brownian motion's grid maximum against the union bound and Dudley's integral; an ellipsoid
    widths    Gaussian widths of the l1 and l2 balls by p; the l1 descent cone's width against its statistical dimension
    statdim   the l1 phase transition: basis-pursuit success against the statistical dimension
    cancer    the breast-cancer correlation spectrum against Marchenko-Pastur; shuffled columns
    board     Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats, special, optimize

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import hdp as HK
from explainer.stats.kit import sparse as SPK

CACHE = Cache("stats51")
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
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def psi_norm_empirical(x, which=2):
    """Empirical Orlicz norm solved in the log domain, without overflowing sums."""
    x = np.abs(np.asarray(x, float))
    if np.max(x) == 0:
        return 0.
    f = lambda t: special.logsumexp((x/t)**which)-math.log(len(x))-math.log(2)
    return float(optimize.brentq(f, 1e-6*float(np.max(x)), 10*float(np.max(x))+1))


def chernoff_binomial(t, n, p):
    """Inclusive Bernoulli upper-tail bound, including q=1 and degenerate laws."""
    t = np.atleast_1d(np.asarray(t, float))
    if n < 1 or not 0 <= p <= 1 or np.any(t < 0):
        raise ValueError("n>=1, p in [0,1], t>=0 required")
    q = p + t
    if p in (0, 1):
        return (t == 0).astype(float)
    z = np.clip(q, 0, 1)
    kl = special.xlogy(z, z / p) + special.xlogy(1-z, (1-z)/(1-p))
    return np.where(q > 1, 0., np.exp(-n*kl))


def binomial_mean_tail(t, n, p):
    # Define the floating-point event literally; do not shift a lattice threshold by 1e-9.
    k = np.arange(n+1)
    return np.array([stats.binom.pmf(k, n, p)[k/n-p >= v].sum()
                     for v in np.atleast_1d(t)])


def jl_dimension_confidence(N, eps, alpha=0.05):
    """Squared distances, all pairs, probability >=1-alpha, 0<eps<=1."""
    if N < 2 or not 0 < eps <= 1 or not 0 < alpha < 1:
        raise ValueError("N>=2, eps in (0,1], alpha in (0,1) required")
    return math.ceil(8 / eps**2 * math.log(N*(N-1)/alpha))


def l1_polar_distance_squared(g, s):
    """Exact per-draw min_tau>=0 dist^2(g,tau partial||x||_1), positive support."""
    g = np.atleast_2d(np.asarray(g, float))
    p = g.shape[1]
    if not 1 <= s <= p:
        raise ValueError("1<=s<=p required")
    v = np.sort(np.abs(g[:, s:]), axis=1)[:, ::-1]
    sums = np.column_stack([np.zeros(len(g)), np.cumsum(v, axis=1)])
    tau = np.maximum((g[:, :s].sum(axis=1)[:, None]+sums)/(s+np.arange(p-s+1)), 0)
    upper = np.column_stack([np.full(len(g), np.inf), v])
    lower = np.column_stack([v, np.zeros(len(g))])
    valid = (tau <= upper) & (tau >= lower)
    if not np.all(valid.any(axis=1)):
        raise ArithmeticError("No active-set solution for polar projection")
    t = tau[np.arange(len(g)), valid.argmax(axis=1)]
    return ((g[:, :s]-t[:, None])**2).sum(axis=1) + (np.maximum(np.abs(g[:, s:])-t[:, None], 0)**2).sum(axis=1)


def checked_basis_pursuit(A, y):
    """Fail visibly on LP failure; numerical errors are not statistical failures."""
    p = A.shape[1]
    fit = optimize.linprog(np.ones(2*p), A_eq=np.hstack([A,-A]), b_eq=y,
                           bounds=(0,None), method="highs")
    if not fit.success:
        raise RuntimeError(f"Basis-pursuit solver failed: {fit.message}")
    x = fit.x[:p]-fit.x[p:]
    if np.linalg.norm(A@x-y, np.inf) > 1e-6*max(1, np.linalg.norm(y, np.inf)):
        raise ArithmeticError("Basis-pursuit feasibility check failed")
    return x


def interval_halfwidths(m, n=200, alpha=.05):
    m = np.asarray(m, float)
    v = m*(1-m)*n/(n-1)  # unbiased sample variance
    return (1.96*np.sqrt(m*(1-m)/n),
            np.full_like(m, math.sqrt(math.log(2/alpha)/(2*n))),
            np.sqrt(2*v*math.log(4/alpha)/n)+7*math.log(4/alpha)/(3*(n-1)))


# ---------------------------------------------------------------------------------------------------------------
def compute_hook():
    ns = [3, 10, 100, 1000, 10000]
    out = {"ns": ns, "band01": [HK.sphere_band_mass(0.1, n) for n in ns], "half95": [HK.sphere_band_for(0.95, n) for n in ns]}
    x = np.linspace(-1, 1, 801)
    out["x"] = x
    out["pdf"] = {str(n): HK.sphere_coordinate_pdf(x, n) for n in (3, 10, 100, 1000)}
    r = rng(5101)
    out["sample"] = HK.sample_sphere(1000, 300, r)[:, 0]
    return out


def compute_shells():
    r = rng(5102)
    ns = [2, 10, 100, 1000, 10000]
    rows = []
    for n in ns:
        g = np.linalg.norm(r.standard_normal((3000, n)), axis=1)
        m = HK.norm_chi_moments(n)
        u = HK.sample_sphere(n, 3000, r)
        v = HK.sample_sphere(n, 3000, r)
        ip = np.sum(u * v, axis=1)
        rows.append({"n": n, "mean": float(g.mean()), "sd": float(g.std()), "chi_mean": m["mean"], "chi_sd": m["sd"],
                     "ip_sd": float(ip.std()), "angle_sd_deg": float(np.degrees(np.arccos(np.clip(ip, -1, 1))).std())})
    th = np.linspace(0, math.pi, 361)
    return {"rows": rows, "theta": th, "angle_pdf": {str(n): HK.angle_pdf(th, n) for n in (3, 10, 100, 1000)}}


def compute_jl():
    r = rng(5103)
    N, d = 200, 5000
    X = r.standard_normal((N, d))
    X[:100] += 0.3 * r.standard_normal((1, d))  # two loose clusters
    ks = [10, 25, 50, 100, 250, 500, 1000, 2000]
    rows = []
    for k in ks:
        res = HK.jl_distortion(X, k, r)
        rat = res["ratios"]
        rows.append({"k": k, "max_dev": res["max_dev"], "q01": float(np.quantile(rat, 0.01)), "q99": float(np.quantile(rat, 0.99)),
                     "within10": float(np.mean(np.abs(rat - 1) <= 0.1)), "theory": math.sqrt(8 * math.log(N) / k)})
    return {"N": N, "d": d, "rows": rows, "metric": "squared distance ratio", "alpha": .05, "k_needed_30": jl_dimension_confidence(N, 0.3), "k_needed_10": jl_dimension_confidence(N, 0.1)}


def compute_tails():
    n = 200
    out = {"n": n}
    for p in (0.5, 0.02):
        t = np.unique(np.r_[np.linspace(0.002, 0.25 if p == 0.5 else 0.08, 80), .1 if p == .5 else .04])
        out[str(p)] = {"t": t, "exact": binomial_mean_tail(t, n, p), "hoeffding": HK.hoeffding_tail(t, n),
                       "bernstein": HK.bernstein_tail(t, n, p * (1 - p), 1.0), "chernoff": chernoff_binomial(t, n, p)}
    return out


def compute_orlicz():
    r = rng(5104)
    N = 400000
    laws = {"normal": r.standard_normal(N), "rademacher": r.choice([-1.0, 1.0], N), "uniform": r.uniform(-math.sqrt(3), math.sqrt(3), N),
            "laplace": r.laplace(scale=1 / math.sqrt(2), size=N), "exponential": r.exponential(size=N) - 1}
    rows = []
    for k, x in laws.items():
        rows.append({"law": k, "psi2": psi_norm_empirical(x[:200000], 2) if k not in ("laplace", "exponential") else None,
                     "psi1": psi_norm_empirical(x[:200000], 1)})
    return {"rows": rows, "normal_psi2": HK.psi2_norm_normal(), "rad_psi2": HK.psi2_norm_bounded(1.0)}


def compute_lipschitz():
    r = rng(5105)
    ns = [10, 100, 1000, 10000]
    rows = []
    for n in ns:
        reps = 4000 if n <= 1000 else 1000
        m = np.max(r.standard_normal((reps, n)), axis=1)
        rows.append({"n": n, "mean": float(m.mean()), "sd": float(m.std()), "exact_mean": HK.expected_max_gaussians(n),
                     "sqrt2log": math.sqrt(2 * math.log(n))})
    m = np.max(r.standard_normal((20000, 1000)), axis=1)
    t = np.linspace(0, 3, 61)
    tail = [float(np.mean(m - HK.expected_max_gaussians(1000) >= s)) for s in t]
    nrm = np.linalg.norm(r.standard_normal((20000, 1000)), axis=1)
    tailn = [float(np.mean(nrm - HK.norm_chi_moments(1000)["mean"] >= s)) for s in t]
    return {"rows": rows, "t": t, "tail_max": tail, "tail_norm": tailn, "bound": HK.gaussian_concentration(t),
            "center_max": HK.expected_max_gaussians(1000), "center_norm": HK.norm_chi_moments(1000)["mean"], "tail_reps": len(m), "var_max": float(m.var()), "var_norm": float(nrm.var())}


def compute_matrices():
    r = rng(5106)
    n = 400
    ps = [10, 25, 50, 100, 200, 300, 400]
    rows = []
    for p in ps:
        s = HK.singular_extremes(n, p, r, reps=20)
        rows.append({"p": p, **s})
    cov = []
    p = 100
    for nn in (100, 200, 400, 800, 1600, 3200):
        cov.append({"n": nn, "err": HK.covariance_error(nn, p, r, reps=15), "limit": HK.covariance_error_limit(nn, p), "sqrt": math.sqrt(p / nn)})
    X = r.standard_normal((2000, 500))
    ev = np.linalg.eigvalsh(X.T @ X / 2000)
    x = np.linspace(0.1, 2.6, 400)
    edges = np.linspace(0.1, 2.6, 51)
    counts, _ = np.histogram(ev, bins=edges)
    h = counts / (len(ev)*np.diff(edges))
    return {"n": n, "rows": rows, "cov": cov, "cov_p": p, "mp_x": x, "mp_pdf": HK.marchenko_pastur_pdf(x, 0.25), "edges": edges, "hist": h,
            "ev_min": float(ev.min()), "ev_max": float(ev.max())}


def compute_bernstein():
    r = rng(5107)
    p = 50
    rows = []
    for n in (100, 200, 400, 800, 1600, 3200):
        m = HK.matrix_bernstein_rank_one(n, p, r, reps=40)
        rows.append({"n": n, **m, "mp": HK.covariance_error_limit(n, p)})
    return {"p": p, "rows": rows}


def compute_compare():
    r = rng(5108)
    n = 1000
    rhos = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]
    vals = [HK.exchangeable_max(n, rho, r, reps=3000) if rho < 1 else 0.0 for rho in rhos]
    theory = [math.sqrt(1 - rho) * HK.expected_max_gaussians(n) for rho in rhos]
    return {"n": n, "rhos": rhos, "sim": vals, "theory": theory, "sudakov": HK.sudakov_lower(1.0, n), "emax": HK.expected_max_gaussians(n)}


def compute_chaining():
    r = rng(5112)
    Ns = [10, 30, 100, 300, 1000, 3000, 10000]
    walk = [HK.walk_max(N, r, reps=4000) for N in Ns]
    union = [HK.union_bound_max(N+1) for N in Ns]
    dudley = [HK.dudley_brownian(1 / math.sqrt(N)) for N in Ns]
    # Talagrand's ellipsoid a_k = 1/sqrt(k): E sup ~ sqrt(log p); Dudley's integral ~ log p
    ps = [10, 100, 1000, 10000]
    ell = []
    for p in ps:
        a = 1 / np.sqrt(np.arange(1, p + 1))
        g = r.standard_normal((2000, p))
        sup = float(np.mean(np.sqrt(np.sum((a * g) ** 2, axis=1))))
        ell.append({"p": p, "sup": sup, "sqrt_log": math.sqrt(np.sum(a ** 2)), "log": float(np.log(p))})
    return {"Ns": Ns, "walk": walk, "union": union, "dudley": dudley, "limit": math.sqrt(2 / math.pi), "dudley_inf": HK.dudley_brownian(0.0),
            "ell": ell}


def compute_widths():
    ps = [10, 30, 100, 300, 1000, 3000, 10000]
    l1 = [HK.gaussian_width_l1_ball(p) for p in ps]
    l2 = [HK.gaussian_width_l2_ball(p) for p in ps]
    r = rng(5113)
    # Statistical dimension E min, distinguished from the inf E upper bound.
    p = 100
    cone = []
    for s in (1, 2, 5, 10, 20, 40):
        best = l1_polar_distance_squared(r.standard_normal((10000, p)), s)
        cone.append({"s": s, "dist2": float(best.mean()), "delta": HK.stat_dim_l1(s,p),
                     "mcse": float(best.std(ddof=1)/math.sqrt(len(best))), "reps": len(best)})
    return {"ps": ps, "l1": l1, "l2": l2, "sqrt2log": [math.sqrt(2 * math.log(2 * p)) for p in ps], "p": p, "cone": cone}


def compute_statdim():
    r = rng(5109)
    p = 100
    ss = [2, 5, 10, 20, 30, 40]
    ms = list(range(5, 100, 5))
    grid = []
    for s in ss:
        for m in ms:
            ok = 0
            reps = 20
            for _ in range(reps):
                A = r.standard_normal((m, p))
                x = np.zeros(p)
                x[r.choice(p, s, replace=False)] = r.standard_normal(s)
                xh = checked_basis_pursuit(A, A @ x)
                ok += np.linalg.norm(xh - x) <= 1e-4 * max(1, np.linalg.norm(x))
            rate = ok/reps
            grid.append({"s": s, "m": m, "success": rate, "successes": int(ok), "reps": reps,
                         "mcse": math.sqrt(rate*(1-rate)/reps), "solver_failures": 0})
    curve_s = np.arange(1, 60)
    curve = [HK.stat_dim_l1(int(s), p) for s in curve_s]
    return {"p": p, "grid": grid, "curve_s": curve_s, "curve": curve, "ss": ss, "ms": ms}


def compute_cancer():
    X, y, names = museum.breast_cancer()
    X = np.asarray(X, float)
    n, p = X.shape
    Z = (X - X.mean(axis=0)) / X.std(axis=0)
    ev = np.sort(np.linalg.eigvalsh(Z.T @ Z / n))[::-1]
    r = rng(5110)
    Zs = np.column_stack([r.permutation(Z[:, j]) for j in range(p)])
    evs = np.sort(np.linalg.eigvalsh(Zs.T @ Zs / n))[::-1]
    B = 399
    null_top = []
    for _ in range(B):
        perm = np.column_stack([r.permutation(Z[:,j]) for j in range(p)])
        null_top.append(float(np.linalg.eigvalsh(perm.T@perm/n)[-1]))
    # Global independence null: conditional column permutations preserve each margin.
    threshold = float(np.quantile(null_top, .95, method="higher"))
    perm_p = (1+np.sum(np.asarray(null_top)>=ev[0]))/(B+1)
    g = p / (n-1)  # centered Gaussian reference; not an exact null for these margins
    a, b = (1 - math.sqrt(g)) ** 2, (1 + math.sqrt(g)) ** 2
    return {"n": n, "p": p, "gamma": g, "ev": ev, "ev_shuffled": evs, "mp_lo": a, "mp_hi": b, "above": int(np.sum(ev > b)),
            "permutations": B, "null_top": null_top, "top_pvalue": float(perm_p), "top_threshold95": threshold, "above_permutation_max": int(np.sum(ev>threshold)), "share_top": float(ev[0] / ev.sum()), "share_top5": float(ev[:5].sum() / ev.sum())}


def compute_board():
    """Intervals from a concentration bound instead of a CLT, for a Bernoulli mean: the Wald interval (broken for rare
    events), Hoeffding's (honest and conservative), and the empirical Bernstein interval (Maurer & Pontil 2009)."""
    r = rng(5111)
    rows = []
    exact_coverage = []
    n, reps = 200, 20000
    for p in (0.02, 0.5):
        x = r.random((reps, n)) < p
        m = x.mean(axis=1)
        widths = interval_halfwidths(m, n)
        cw, ch, cb = [float(np.mean(np.abs(m-p)<=w)) for w in widths]
        k = np.arange(n+1)
        exact = [float(stats.binom.pmf(k,n,p)[np.abs(k/n-p)<=w].sum())
                 for w in interval_halfwidths(k/n,n)]
        exact_coverage.extend(exact)
        st = rf"Bernoulli($p = {p}$), \ $n = {n}$"
        rows.append(Row(51, r"Wald interval", st, "coverage", 0.95, float(cw), reps, mc_se=math.sqrt(cw*(1-cw)/(reps-1))))
        rows.append(Row(51, r"Hoeffding interval", st, "coverage", 0.95, float(ch), reps, mc_se=math.sqrt(ch*(1-ch)/(reps-1))))
        rows.append(Row(51, r"empirical Bernstein interval", st, "coverage", 0.95, float(cb), reps, mc_se=math.sqrt(cb*(1-cb)/(reps-1))))
    save_rows(51, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows], "exact_coverage": exact_coverage, "hoef_half": math.sqrt(math.log(2 / 0.05) / (2 * n))}


ITEMS = {
    "hook": compute_hook, "shells": compute_shells, "jl": compute_jl, "tails": compute_tails, "orlicz": compute_orlicz,
    "lipschitz": compute_lipschitz, "matrices": compute_matrices, "bernstein": compute_bernstein, "compare": compute_compare,
    "chaining": compute_chaining, "widths": compute_widths, "statdim": compute_statdim, "cancer": compute_cancer, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
