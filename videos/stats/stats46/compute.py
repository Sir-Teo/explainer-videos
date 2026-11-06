"""Precompute every number in Part 46 of *Statistics, Built* ("The Theory of Testing and Confidence").

    OMP_NUM_THREADS=1 python -m videos.stats.stats46.compute            # everything missing (a few minutes)
    python -m videos.stats.stats46.compute --force board

Results are cached in ``.cache/stats46/<name>.json``.  Old Faithful, ISIS-2, Bliss's beetles and the lady tasting tea
are the Museum's; everything else is exact arithmetic or a seeded simulation.

Items:
    bf          Behrens-Fisher: sizes of the pooled t, Welch and fiducial tests; the fiducial critical values; Old Faithful
    np          the randomized UMP one-sided binomial test and its power; the non-randomized test's size
    mlr         likelihood ratios: monotone for the binomial, not for the Cauchy location family
    umpu        the UMPU two-sided binomial test against the equal-tailed test; the generalized NP lemma as an LP
    invariance  power of the z, t and sign tests against mu / sigma
    neyman      Neyman structure for two binomials: conditional slices, unconditional sizes; ISIS-2 and the tea
    lrt         Wilks's chi-square for a Poisson rate; Chernoff's boundary mixture
    belt        Clopper-Pearson's belt for n = 20; exact coverage against Wald's
    fieller     a ratio of means: Fieller's sets against the delta method; Bliss's LD50
    fc          Feldman-Cousins intervals for b = 3 against flip-flopping; exact coverage
    simul       Scheffe, Bonferroni and closed testing (Holm, Hommel) on a worked example
    buehler     the n = 2 t interval on a recognizable subset
    evidence    Berger-Sellke bounds on P(H0 | x) by p-value
    gof         Pearson's chi-square limit; Kolmogorov-Smirnov with estimated parameters
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import optimize, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import testing as TK

CACHE = Cache("stats46")
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


def eff_reps(per_rep, nominal=0.95) -> int:
    v = np.var(np.asarray(per_rep, float), ddof=1) / len(per_rep)
    if v == 0:
        return len(per_rep)
    return int(round(nominal * (1 - nominal) / max(v, 1e-12)))


# ---------------------------------------------------------------------------------------------------------------
def compute_bf():
    g = rng(4601)
    settings = [(10, 1.0, 10, 1.0), (10, 1.0, 10, 3.0), (5, 3.0, 25, 1.0), (25, 3.0, 5, 1.0)]
    rows = []
    for n1, s1, n2, s2 in settings:
        r = TK.two_sample_sizes(n1, s1, n2, s2, 20000, g)
        rows.append({"n1": n1, "s1": s1, "n2": n2, "s2": s2, "pooled": float(r["pooled"].mean()),
                     "welch": float(r["welch"].mean()), "bf": float(r["bf"].mean())})
    phis = np.linspace(0, math.pi / 2, 31)
    curves = {}
    for n1, n2 in ((5, 25), (10, 10)):
        curves[f"{n1}_{n2}"] = [TK.bf_critical(p, n1, n2) for p in phis]
    # Old Faithful: eruption durations after short and long waits
    er, wt = museum.faithful()
    a, b = er[wt < 70], er[wt >= 70]
    v1, v2 = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    d = (b.mean() - a.mean()) / math.sqrt(v1 + v2)
    df = float(TK.welch_df(v1, v2, len(a), len(b)))
    sp = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    tp = (b.mean() - a.mean()) / math.sqrt(sp * (1 / len(a) + 1 / len(b)))
    faithful = {"n": [len(a), len(b)], "mean": [float(a.mean()), float(b.mean())], "sd": [float(a.std(ddof=1)), float(b.std(ddof=1))],
                "welch_t": float(d), "welch_df": df, "pooled_t": float(tp), "pooled_df": len(a) + len(b) - 2,
                "welch_ci": [float(b.mean() - a.mean() - stats.t.ppf(0.975, df) * math.sqrt(v1 + v2)),
                             float(b.mean() - a.mean() + stats.t.ppf(0.975, df) * math.sqrt(v1 + v2))]}
    return {"rows": rows, "phis": phis, "curves": curves, "z": float(stats.norm.ppf(0.975)),
            "t4": float(stats.t.ppf(0.975, 4)), "t24": float(stats.t.ppf(0.975, 24)), "faithful": faithful}


def compute_np():
    n, p0 = 20, 0.3
    u = TK.ump_binomial(n, p0)
    ps = np.linspace(0, 1, 201)
    nonrand = np.where(np.arange(n + 1) > u["c"], 1.0, 0.0)
    return {"n": n, "p0": p0, "c": u["c"], "gamma": u["gamma"], "phi": u["phi"], "ps": ps, "power": TK.power(u["phi"], n, ps),
            "power_nr": TK.power(nonrand, n, ps), "size_nr": float(TK.power(nonrand, n, p0)[0]),
            "size_nr2": float(TK.power(np.where(np.arange(n + 1) >= u["c"], 1.0, 0.0), n, p0)[0]),
            "pmf0": stats.binom.pmf(np.arange(n + 1), n, p0), "pmf1": stats.binom.pmf(np.arange(n + 1), n, 0.5)}


def compute_mlr():
    x = np.arange(21)
    lr_bin = stats.binom.pmf(x, 20, 0.5) / stats.binom.pmf(x, 20, 0.3)
    xs = np.linspace(-6, 8, 281)
    lr_cauchy = stats.cauchy.pdf(xs, 1) / stats.cauchy.pdf(xs, 0)
    # a one-observation Cauchy test: power of 'reject when x > c' vs the most powerful test at theta = 1
    return {"x": x, "lr_bin": lr_bin, "xs": xs, "lr_cauchy": lr_cauchy, "cauchy_max": float(xs[np.argmax(lr_cauchy)]),
            "cauchy_peak": float(lr_cauchy.max())}


def compute_umpu():
    n, p0 = 20, 0.3
    t = TK.umpu_binomial(n, p0)
    et = TK.equal_tailed_binomial(n, p0)
    ps = np.linspace(0, 1, 401)
    pw_u, pw_e = TK.power(t["phi"], n, ps), TK.power(et, n, ps)
    near = (ps > 0.2) & (ps < 0.45)
    x = np.arange(n + 1)
    f0 = stats.binom.pmf(x, n, p0)
    lp = {}
    for p1 in (0.15, 0.5):
        g = TK.generalized_np(f0, stats.binom.pmf(x, n, p1), [f0, x * f0], [0.05, 0.05 * n * p0])
        lp[str(p1)] = {"phi": g, "power": float(TK.power(g, n, p1)[0]), "umpu": float(TK.power(t["phi"], n, p1)[0])}
    return {"n": n, "p0": p0, "umpu": t, "et": et, "ps": ps, "pw_umpu": pw_u, "pw_et": pw_e,
            "et_min": float(pw_e[near].min()), "et_argmin": float(ps[near][np.argmin(pw_e[near])]), "lp": lp}


def compute_neyman():
    m, n = 8, 10
    r = TK.conditional_test(m, n, randomized=True)
    nr = TK.conditional_test(m, n, randomized=False)
    ps = np.linspace(0.02, 0.98, 49)
    slices = {}
    for t in (4, 9, 13):
        lo, hi = max(0, t - n), min(m, t)
        xs = np.arange(lo, hi + 1)
        slices[str(t)] = {"x": xs, "pmf": stats.hypergeom.pmf(xs, m + n, m, t), "phi": r["phi"][xs, t]}
    # ISIS-2: deaths given the total
    da, na = museum.ISIS2["aspirin"]
    dp, npl = museum.ISIS2["placebo"]
    T = da + dp
    hyp = stats.hypergeom(na + npl, na, T)
    p_lower = float(hyp.cdf(da))  # aspirin deaths this low or lower, given the total
    z = (da - T * na / (na + npl)) / math.sqrt(hyp.var())
    # the lady tasting tea: 8 cups, 4 milk-first; all four identified
    tea = {"p_all": 1 / math.comb(8, 4), "p_3plus": (math.comb(4, 3) * math.comb(4, 1) + 1) / math.comb(8, 4)}
    return {"m": m, "n": n, "ps": ps, "size_rand": TK.unconditional_size(r["phi"], m, n, ps),
            "size_fisher": TK.unconditional_size(nr["phi"], m, n, ps), "slices": slices,
            "isis": {"deaths": [da, dp], "n": [na, npl], "total": T, "expected": T * na / (na + npl), "p": p_lower, "z": float(z)},
            "tea": tea}


def compute_invariance():
    """Power at level 0.05 (one-sided) for normal data, n = 10, against delta = mu / sigma: the z test with sigma known
    (an upper bound), the t test (UMP among scale-invariant tests), and the sign test (exact, randomized)."""
    n = 10
    d = np.linspace(0, 1.5, 61)
    z = stats.norm.sf(stats.norm.isf(0.05) - d * math.sqrt(n))
    tc = stats.t.isf(0.05, n - 1)
    t = stats.nct.sf(tc, n - 1, d * math.sqrt(n))
    u = TK.ump_binomial(n, 0.5)
    sign = TK.power(u["phi"], n, stats.norm.cdf(d))
    return {"n": n, "delta": d, "z": z, "t": t, "sign": sign, "at05": [float(np.interp(0.5, d, z)), float(np.interp(0.5, d, t)), float(np.interp(0.5, d, sign))]}


def compute_lrt():
    g = rng(4602)
    # Wilks: Poisson rate, n = 10, lambda = 2
    n, lam = 10, 2.0
    x = g.poisson(lam, (40000, n))
    xb = x.mean(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        lr = 2 * n * np.where(xb > 0, xb * np.log(xb / lam) - (xb - lam), lam)
    q = np.quantile(lr, [0.5, 0.9, 0.95, 0.99])
    # Chernoff: H0 mu = 0 vs mu >= 0
    z = g.normal(0, 1, 200000)
    lrb = np.maximum(z, 0) ** 2
    return {"wilks_q": q, "chi2_q": stats.chi2.ppf([0.5, 0.9, 0.95, 0.99], 1), "wilks_size": float(np.mean(lr > stats.chi2.ppf(0.95, 1))),
            "lr_hist": np.histogram(lr, bins=40, range=(0, 8), density=True)[0], "chibar_crit": TK.chibar_critical(0.05),
            "chi2_crit": float(stats.chi2.ppf(0.95, 1)), "naive_size": float(np.mean(lrb > stats.chi2.ppf(0.95, 1))),
            "chibar_size": float(np.mean(lrb > TK.chibar_critical(0.05))), "zero_share": float(np.mean(lrb == 0))}


def compute_belt():
    n = 20
    iv = [TK.clopper_pearson(x, n) for x in range(n + 1)]
    w = [TK.wald_binomial(x, n) for x in range(n + 1)]
    ps = np.linspace(0.005, 0.995, 397)
    # one-sided UMA upper bounds (invert the UMP tests of p >= p0): upper limit for x
    upper = [1.0 if x == n else float(stats.beta.ppf(0.95, x + 1, n - x)) for x in range(n + 1)]
    return {"n": n, "cp": iv, "wald": w, "ps": ps, "cov_cp": TK.coverage_binomial(iv, n, ps), "cov_wald": TK.coverage_binomial(w, n, ps),
            "upper": upper, "cov_upper": TK.coverage_binomial([(0.0, u) for u in upper], n, ps)}


def _logistic(dose, n, k):
    X = np.c_[np.ones_like(dose), dose]

    def nll(b):
        eta = X @ b
        return -np.sum(k * eta - n * np.logaddexp(0, eta))

    r = optimize.minimize(nll, [-60, 34], method="BFGS")
    b = r.x
    p = 1 / (1 + np.exp(-(X @ b)))
    W = n * p * (1 - p)
    V = np.linalg.inv(X.T @ (W[:, None] * X))
    return b, V


def compute_fieller():
    g = rng(4603)
    # a ratio of two normal means: rho = alpha / beta, a ~ N(1, 1), b ~ N(beta, 1)
    out = {}
    reps = 20000
    for beta in (4.0, 2.0, 1.0, 0.5):
        a = g.normal(1.0, 1.0, reps)
        b = g.normal(beta, 1.0, reps)
        rho = 1.0 / beta
        z = stats.norm.ppf(0.975)
        se = np.sqrt(1 / b ** 2 + a ** 2 / b ** 4)
        cov_delta = np.abs(a / b - rho) <= z * se
        kinds = {"bounded": 0, "exclusive": 0, "all": 0}
        cov_f = np.zeros(reps, bool)
        for i in range(reps):
            f = TK.fieller(a[i], b[i], 1.0, 1.0)
            kinds[f["kind"]] += 1
            if f["kind"] == "bounded":
                cov_f[i] = f["lo"] <= rho <= f["hi"]
            elif f["kind"] == "exclusive":
                cov_f[i] = rho <= f["lo"] or rho >= f["hi"]
            else:
                cov_f[i] = True
        out[str(beta)] = {"delta": float(cov_delta.mean()), "fieller": float(cov_f.mean()),
                          "kinds": {k: v / reps for k, v in kinds.items()}, "cov_delta": cov_delta, "cov_f": cov_f}
    # Bliss's beetles: LD50 by Fieller and by the delta method
    dose, n, k = museum.bliss()
    b, V = _logistic(dose, n, k)
    ld = -b[0] / b[1]
    f = TK.fieller(-b[0], b[1], V[0, 0], V[1, 1], -V[0, 1])
    grad = np.array([-1 / b[1], b[0] / b[1] ** 2])
    se = math.sqrt(grad @ V @ grad)
    bliss = {"ld50": float(ld), "fieller": [f["lo"], f["hi"]], "delta": [ld - 1.96 * se, ld + 1.96 * se], "b": b, "z_slope": float(b[1] / math.sqrt(V[1, 1]))}
    return {"ratio": {k: {kk: vv for kk, vv in v.items() if kk not in ("cov_delta", "cov_f")} for k, v in out.items()},
            "bliss": bliss, "_cov": {k: {"delta": v["cov_delta"], "fieller": v["cov_f"]} for k, v in out.items()}}


def compute_fc():
    b = 3.0
    grid = np.linspace(0, 15, 1501)
    fc = TK.fc_intervals(b, 0.9, mu_grid=grid, nmax=40)
    ff = TK.flipflop_intervals(b, 0.9, nmax=40)
    mus = grid[grid <= 8 + 1e-9][::2]  # on the construction's grid, where its coverage is guaranteed
    cov_fc = TK.poisson_coverage(fc["lo"], fc["hi"], b, mus)
    cov_ff = TK.poisson_coverage(ff["lo"], ff["hi"], b, mus)
    f0 = TK.fc_intervals(0.0, 0.9, mu_grid=np.linspace(0, 15, 3001), nmax=40)
    # the classical upper limit for n = 0 at b = 3 is negative: an empty interval
    return {"b": b, "n": fc["n"][:11], "fc_lo": fc["lo"][:11], "fc_hi": fc["hi"][:11], "ff_lo": ff["lo"][:11], "ff_hi": ff["hi"][:11],
            "mus": mus, "cov_fc": cov_fc, "cov_ff": cov_ff, "ff_min": float(cov_ff.min()), "ff_argmin": float(mus[np.argmin(cov_ff)]),
            "fc_min": float(cov_fc.min()), "b0": {"lo": f0["lo"][:6], "hi": f0["hi"][:6]},
            "classical_upper_n0": float(-math.log(0.1) - b)}


def compute_simul():
    p = np.array([0.011, 0.018, 0.024, 0.04])
    bon = p <= 0.05 / len(p)
    holm = TK.holm(p)
    hommel = TK.closed_test(p, 0.05, "simes")
    ks = [1, 2, 3, 5, 10, 20]
    sch = [TK.scheffe_constant(k) for k in ks]
    bonf = [float(stats.norm.ppf(1 - 0.025 / k)) for k in ks]
    return {"p": p, "bonferroni": bon, "holm": holm, "hommel": hommel, "ks": ks, "scheffe": sch, "bonf": bonf}


def compute_buehler():
    g = rng(4604)
    k = 1 + math.sqrt(2)
    mus = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0]
    rows = [TK.t2_conditional(m, k, 200000, g) | {"mu": m} for m in mus]
    return {"k": k, "rows": rows}


def compute_evidence():
    ps = [0.1, 0.05, 0.01, 0.001]
    return {"rows": [TK.berger_sellke(p) | {"p": p} for p in ps]}


def compute_gof():
    g = rng(4605)
    # Pearson: 6 categories, n = 60, uniform null
    k, n = 6, 60
    counts = g.multinomial(n, np.full(k, 1 / k), 40000)
    X2 = np.sum((counts - n / k) ** 2 / (n / k), axis=1)
    ks20 = TK.ks_estimated(20, 40000, g)
    ks100 = TK.ks_estimated(100, 20000, g)
    return {"x2_q": np.quantile(X2, [0.5, 0.9, 0.95, 0.99]), "chi2_q": stats.chi2.ppf([0.5, 0.9, 0.95, 0.99], k - 1),
            "x2_size": float(np.mean(X2 > stats.chi2.ppf(0.95, k - 1))), "x2_hist": np.histogram(X2, bins=36, range=(0, 18), density=True)[0],
            "ks20": {k_: v for k_, v in ks20.items() if k_ != "D"}, "ks100": {k_: v for k_, v in ks100.items() if k_ != "D"},
            "D20_hist": np.histogram(ks20["D"], bins=40, range=(0, 0.4), density=True)[0]}


def compute_board():
    g = rng(4699)
    rows = []
    r = TK.two_sample_sizes(5, 3.0, 25, 1.0, 20000, g)
    for key, name in (("pooled", "pooled t test"), ("welch", "Welch's test"), ("bf", "Behrens--Fisher test")):
        rows.append(Row(46, name, "n = 5 (SD 3) vs n = 25 (SD 1)", "size", 0.05, float(r[key].mean()), len(r[key])))
    fl = load("fieller")
    cov = fl["_cov"]["0.5"]
    rows.append(Row(46, "delta-method interval for a ratio", "denominator mean 0.5, SE 1", "coverage", 0.95,
                    float(np.mean(cov["delta"])), len(cov["delta"])))
    rows.append(Row(46, "Fieller's set for a ratio", "denominator mean 0.5, SE 1", "coverage", 0.95,
                    float(np.mean(cov["fieller"])), len(cov["fieller"])))
    # flip-flopping vs Feldman-Cousins at the flip-flop's worst mu: simulate Poisson counts
    fc = load("fc")
    mu = fc["ff_argmin"]
    nobs = g.poisson(mu + fc["b"], 20000)
    full_fc = TK.fc_intervals(3.0, 0.9, mu_grid=np.linspace(0, 15, 1501), nmax=60)
    full_ff = TK.flipflop_intervals(3.0, 0.9, nmax=60)
    hit_ff = (full_ff["lo"][nobs] <= mu + 1e-12) & (mu <= full_ff["hi"][nobs] + 1e-12)
    hit_fc = (full_fc["lo"][nobs] <= mu + 1e-12) & (mu <= full_fc["hi"][nobs] + 1e-12)
    rows.append(Row(46, "flip-flopping Poisson limits", f"background 3, mu = {mu:.2f}", "coverage", 0.9, float(hit_ff.mean()), len(hit_ff)))
    rows.append(Row(46, "Feldman--Cousins limits", f"background 3, mu = {mu:.2f}", "coverage", 0.9, float(hit_fc.mean()), len(hit_fc)))
    ks = TK.ks_estimated(20, 20000, g)
    rows.append(Row(46, "KS test, estimated mean and SD", "normal data, n = 20", "size", 0.05, ks["size"], 20000))
    save_rows(46, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "bf": compute_bf, "np": compute_np, "mlr": compute_mlr, "umpu": compute_umpu, "neyman": compute_neyman, "invariance": compute_invariance, "lrt": compute_lrt,
    "belt": compute_belt, "fieller": compute_fieller, "fc": compute_fc, "simul": compute_simul, "buehler": compute_buehler,
    "evidence": compute_evidence, "gof": compute_gof, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
