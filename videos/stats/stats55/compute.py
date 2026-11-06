"""Precompute every number in Part 55 of *Statistics, Built* ("The Qualifying Exam").

    OMP_NUM_THREADS=1 python -m videos.stats.stats55.compute            # everything missing (a few minutes)
    python -m videos.stats.stats55.compute --force board

Results are cached in ``.cache/stats55/<name>.json``.  Snow's Table IX and Newcomb's passage times are the Museum's;
everything else is exact arithmetic or a seeded simulation.

Items:
    bc        Problem 1: exponential maxima, Borel-Cantelli sums and exceedances
    walk      Problem 2: the walk stopped at +1, exactly; ruin probabilities
    umvue     Problem 3: the Poisson UMVUE of exp(-lambda) against the MLE and the Cramer-Rao bound
    blyth     Problem 4: Blyth's ratio in one and two dimensions
    snow      Problem 5: Snow's Table IX, the conditional test and the exact interval for the rate ratio; sizes
    lan       Problem 6: local power in the logistic location model, theory and simulation
    brackets  Problem 7: brackets for half-lines, the bracketing integral, the empirical process
    median    Problem 8: the median's influence function; Newcomb's median with its Wald interval
    fano      Problem 9: Fano's bound for sparse means against soft thresholding, by dimension
    bernstein Problem 10: matrix Bernstein for a bounded covariance, by n
    lasso     Problem 11: the lasso's oracle inequality, by n
    contract  Problem 12: posterior contraction in the sequence model, by n and prior smoothness
    board     Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import qual as Q

CACHE = Cache("stats55")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, float)):
        v = float(obj)
        return v if math.isfinite(v) else None
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def compute_bc():
    r = rng(5501)
    N = 10 ** 6
    x = r.exponential(size=N)
    ratio = Q.running_max_ratio(x)
    ns = np.unique(np.round(np.geomspace(2, N, 120)).astype(int))
    out = {"N": N, "ns": ns, "ratio": ratio[ns - 2]}
    for c in (0.8, 1.0, 1.2, 2.0):
        e = Q.exceedances(x, c)
        out[f"exc_{c}"] = {"count": len(e), "last": int(e[-1]) if len(e) else 0, "first20": e[:20],
                           "sum": float(Q.bc_partial_sums(c, N)[-1])}
    out["sum2_exact"] = math.pi ** 2 / 6 - 1
    # the exceedance times for the scatter: X_n / log n for n up to 10^4
    n = np.arange(2, 10001)
    out["scatter_n"] = n[::7]
    out["scatter_r"] = (x[1:10000] / np.log(n))[::7]
    return out


def compute_walk():
    N = 4001
    fp = Q.first_passage(N)
    ms = np.unique(np.round(np.geomspace(1, N, 80)).astype(int))
    pmf = [Q.first_passage_pmf(k) for k in range(1, 11)]
    r = rng(5502)
    # a few sample paths until T or 400 steps
    paths = []
    while len(paths) < 5:  # five paths that take a while, to show the walk's excursions below zero
        s, path = 0, [0]
        for _ in range(400):
            s += 1 if r.random() < 0.5 else -1
            path.append(s)
            if s == 1:
                break
        if len(path) >= 12:
            paths.append(path)
    return {"ms": ms, "hit": fp["hit"][ms], "tail_mean": fp["tail_mean"][ms], "e_min": fp["e_min"][ms],
            "pmf": pmf, "tail_exact": [math.comb(2 * k, k) / 4 ** k for k in (1, 10, 100, 1000)],
            "paths": paths, "ruin": Q.ruin(3, 7)}


def compute_umvue():
    lams = np.linspace(0.05, 5, 100)
    rows = {n: [Q.poisson_umvue(n, float(l)) for l in lams] for n in (5, 20)}
    out = {"lams": lams}
    for n, rs in rows.items():
        out[str(n)] = {k: [r_[k] for r_ in rs] for k in ("var_umvue", "crlb", "mle_mse", "target")}
    out["example"] = Q.poisson_umvue(10, 2.0)
    r = rng(5503)
    T = r.poisson(20.0, 200000)
    out["mc"] = {"mean": float(np.mean(0.9 ** T)), "var": float(np.var(0.9 ** T))}
    return out


def compute_blyth():
    taus = np.geomspace(0.3, 300, 80)
    return {"taus": taus, "d1": Q.blyth_ratio(taus, 1), "d2": Q.blyth_ratio(taus, 2), "d3": Q.blyth_ratio(taus, 3)}


def compute_snow():
    sv, lb = museum.SNOW[0], museum.SNOW[1]
    e1, x, e2, y = sv[1], sv[2], lb[1], lb[2]
    t = x + y
    p0 = e1 / (e1 + e2)
    z = (x - t * p0) / math.sqrt(t * p0 * (1 - p0))
    logp = float(stats.binom.logsf(x - 1, t, p0))
    # exact (Clopper-Pearson) interval for p = rho e1 / (rho e1 + e2), mapped to the rate ratio rho
    lo = stats.beta.ppf(0.025, x, t - x + 1)
    hi = stats.beta.ppf(0.975, x + 1, t - x)
    rho = lambda p: p / (1 - p) * e2 / e1  # noqa: E731
    sizes = {lam: (Q.poisson_conditional_size(lam), Q.poisson_conditional_size(lam, randomized=True)) for lam in (1, 2, 5, 10, 20, 50)}
    # a toy for the card: X = 12, Y = 4
    toy = Q.poisson_conditional_test(12, 4)
    return {"e1": e1, "x": x, "e2": e2, "y": y, "t": t, "p0": p0, "phat": x / t, "z": z, "log10p": logp / math.log(10),
            "ratio": (x / e1) / (y / e2), "ci": [rho(lo), rho(hi)], "rate1": 1e4 * x / e1, "rate2": 1e4 * y / e2,
            "sizes": {str(k): v for k, v in sizes.items()},
            "toy": {"p": toy["p"], "t": toy["t"], "c1": toy["umpu"]["c1"], "c2": toy["umpu"]["c2"], "g1": toy["umpu"]["g1"],
                    "g2": toy["umpu"]["g2"]}}


def compute_lan():
    hs = np.linspace(0, 6, 61)
    th = Q.logistic_local_powers(hs)
    r = rng(5504)
    sim_h = [0.0, 1.5, 3.0, 4.5, 6.0]
    sim = [Q.logistic_local_power_sim(h, 400, r, reps=4000) for h in sim_h]
    return {"hs": hs, **{k: th[k] for k in th}, "sim_h": sim_h, "sim": {k: [s[k] for s in sim] for k in ("score", "t", "sign")},
            "info": Q.LOGISTIC_INFO, "are_t": 9 / math.pi ** 2, "are_sign": 0.75}


def compute_brackets():
    eps = np.geomspace(0.02, 1, 60)
    N = [int(math.ceil(1 / e ** 2)) for e in eps]
    integ = Q.bracketing_integral(lambda e: np.log(np.ceil(1 / e ** 2)))
    closed = math.sqrt(2) * math.sqrt(math.pi) / 2
    r = rng(5505)
    n = 400
    u = np.sort(r.random(n))
    grid = np.linspace(0, 1, 401)
    Fn = np.searchsorted(u, grid, side="right") / n
    proc = math.sqrt(n) * (Fn - grid)
    br = Q.halfline_brackets(0.25)
    # monotone functions: log N ~ 1/eps, still integrable; Lipschitz in d dims: eps^(-d), integrable only if d < 2
    return {"eps": eps, "N": N, "integral": integ, "closed": closed, "grid": grid, "proc": proc, "n": n, "brackets": br,
            "sup": float(np.max(np.abs(proc)))}


def compute_median():
    x = museum.newcomb()
    n = len(x)
    w = Q.median_wald(x)
    mean, sd = float(x.mean()), float(x.std(ddof=1))
    clean = x[x > 0]
    r = rng(5506)
    # the IF's variance against simulation, for N(0,1) and t3
    sims = {}
    for name, draw, f0 in (("normal", lambda k: r.standard_normal(k), stats.norm.pdf(0)), ("t3", lambda k: r.standard_t(3, k), stats.t.pdf(0, 3))):
        meds = np.median(draw((4000, 66)), axis=1)
        sims[name] = {"nvar": float(66 * meds.var()), "theory": 1 / (4 * f0 ** 2)}
    grid = np.linspace(-3, 3, 241)
    return {"x": x, "n": n, "median": w["median"], "f": w["f"], "se": w["se"], "ci": [w["lo"], w["hi"]], "mean": mean,
            "se_mean": sd / math.sqrt(n), "ci_mean": [mean - 1.96 * sd / math.sqrt(n), mean + 1.96 * sd / math.sqrt(n)],
            "clean_mean": float(clean.mean()), "clean_n": len(clean), "outliers": sorted(x[x <= 0].tolist()), "sims": sims,
            "grid": grid, "if_normal": Q.median_if(grid, 0.0, stats.norm.pdf(0)), "if_mean": grid, "modern": 33.0}


def compute_fano():
    r = rng(5507)
    s, n = 10, 100
    ds = [100, 200, 500, 1000, 2000, 5000, 10000, 100000]
    rows = []
    for d in ds:
        f = Q.sparse_fano(d, s, n)
        st = max(Q.soft_threshold_risk(d, s, n, a, r, reps=200) for a in (0.3, 0.6, 1.0, 3.0))
        rows.append({"d": d, "lower": f["lower"], "rate": f["rate"], "logM": f["logM"], "soft": st})
    return {"s": s, "n": n, "rows": rows, "example": Q.sparse_fano(1000, s, n)}


def compute_bernstein():
    r = rng(5508)
    d = 50
    ns = [100, 200, 400, 800, 1600, 3200, 6400]
    rows = []
    for n in ns:
        b = Q.bounded_covariance_error(n, d, r, reps=200)
        rows.append({"n": n, "mean": b["mean"], "mean_bound": b["mean_bound"], "t": b["t"], "coverage": b["coverage"], "q95": b["q95"],
                     "mp": (1 + math.sqrt(d / n)) ** 2 - 1})
    return {"d": d, "rows": rows}


def compute_lasso():
    r = rng(5509)
    p, s = 500, 5
    ns = [100, 150, 200, 300, 500, 800]
    rows = []
    for n in ns:
        o = Q.lasso_oracle(n, p, s, r, reps=30)
        rows.append({"n": n, **{k: o[k] for k in ("lam", "pred", "pred_bound", "l1", "l1_bound", "event")}})
    return {"p": p, "s": s, "rows": rows}


def compute_contract():
    ns = np.unique(np.round(np.geomspace(10, 1e6, 40)).astype(int))
    out = {"ns": ns, "beta": 1.0}
    for a in (0.5, 1.0, 2.0):
        rs = [Q.sequence_contraction(int(n), a, 1.0) for n in ns]
        tot = np.array([x["total"] for x in rs])
        out[str(a)] = {"total": tot, "rate2": [x["rate2"] for x in rs], "bias2": [x["bias2"] for x in rs],
                       "var": [x["var"] for x in rs], "spread": [x["spread"] for x in rs],
                       "slope": float(np.polyfit(np.log(ns[20:]), np.log(tot[20:]), 1)[0]),
                       "theory": -2 * min(a, 1.0) / (1 + 2 * a)}
    return out


def compute_board():
    r = rng(5510)
    reps = 20000
    lam = 5.0
    # (a, b) the conditional test of equal Poisson rates, unrandomized and randomized, at a common rate of 5
    X = r.poisson(lam, reps)
    Y = r.poisson(lam, reps)
    rej_nr, rej_r = 0, 0
    phis = {}
    for x, y in zip(X, Y):
        t = x + y
        if t == 0:
            rej_r += r.random() < 0.05
            continue
        pv = min(1.0, 2 * min(stats.binom.cdf(x, t, 0.5), stats.binom.sf(x - 1, t, 0.5)))
        rej_nr += pv <= 0.05
        # randomized UMPU in the slice
        if t not in phis:
            phis[t] = Q.poisson_conditional_test(int(x), int(y))["umpu"]["phi"]
        rej_r += r.random() < phis[t][x]
    # (c) the median's Wald interval with a KDE plug-in, t3 data of Newcomb's size
    cov_med = 0
    m_reps = 4000
    for _ in range(m_reps):
        w = Q.median_wald(r.standard_t(3, 66))
        cov_med += w["lo"] <= 0 <= w["hi"]
    # (d) the matrix-Bernstein ball for a bounded covariance, d = 50, n = 400
    b = Q.bounded_covariance_error(400, 50, r, reps=2000)
    rows = [
        Row(55, r"conditional binomial test, \ unrandomized", r"equal Poisson rates, \ $\lambda = 5$", "size", 0.05, rej_nr / reps, reps),
        Row(55, r"UMPU test (randomized, \ Neyman structure)", r"equal Poisson rates, \ $\lambda = 5$", "size", 0.05, rej_r / reps, reps),
        Row(55, r"median $\pm$ 1.96 IF-based SE \ (KDE plug-in)", r"$t_3$ data, \ $n = 66$", "coverage", 0.95, cov_med / m_reps, m_reps),
        Row(55, r"matrix-Bernstein ball for $\Sigma$", r"Rademacher vectors, \ $d = 50$, \ $n = 400$", "coverage", 0.95, b["coverage"], 2000),
    ]
    save_rows(55, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows]}


ITEMS = {
    "bc": compute_bc, "walk": compute_walk, "umvue": compute_umvue, "blyth": compute_blyth, "snow": compute_snow,
    "lan": compute_lan, "brackets": compute_brackets, "median": compute_median, "fano": compute_fano,
    "bernstein": compute_bernstein, "lasso": compute_lasso, "contract": compute_contract, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
