"""Precompute every number in Part 30 of *Statistics, Built* ("Robust Statistics").

    python -m videos.stats.stats30.compute            # everything missing (a few minutes)
    python -m videos.stats.stats30.compute --force board

Results are cached in ``.cache/stats30/<name>.json``.  Newcomb's light, the copper in flour, the CYG OB1 stars and
Hawkins, Bradu & Kass's data are the Museum's; the women's heights are the World's; the rest are seeded simulations.

Items:
    tukey       Tukey's (1960) duel: mean deviation vs standard deviation under the contaminated normal
    newcomb     Newcomb's 66 passage times: every location estimate, its interval, with and without the outliers
    are         Pitman ARE of Wilcoxon to t across distributions; the 0.864 bound; normal scores
    influence   sensitivity curves on Newcomb's data and theoretical influence functions
    breakdown   Newcomb's data with m points replaced by gross errors, m = 0 .. 40
    huber       Huber's k(eps), minimax variances, and the variance of Huber's estimate across k and eps
    scale       the copper data: classical and robust scale; the normal efficiencies of MAD, Qn and Sn
    regression  the CYG OB1 stars: OLS, Huber M, LMS, LTS and MM
    mcd         Hawkins--Bradu--Kass: classical vs MCD distances; masking and swamping
    mom         Pareto(2.2) means: the sample mean, trimmed mean, median of means and Catoni's estimator
    princeton   a small Princeton Robustness Study: seven location estimates on five distributions, n = 20
    corrupt     the stars with m main-sequence stars replaced by bad leverage points: OLS, LTS and MM slopes
    board       Coverage Board rows: t vs Hodges--Lehmann intervals for the World's women's mean height, clean and
                contaminated
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import integrate, stats, optimize

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import robust as R
from explainer.stats.world import World

CACHE = Cache("stats30")
load = CACHE.load
LIGHT_TRUE = 33.02  # the modern value of the speed of light on Newcomb's scale (Stigler 1977)


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


def sn_scale(x):
    """Rousseeuw-Croux Sn with low outer and high inner medians, including finite corrections.

    Matches the definition in robustbase's qn_sn.c and qnsn.R; the generic kit's
    averaged even-sample medians define a different finite-sample statistic.
    """
    x=np.asarray(x,float);n=len(x)
    if n<2:return 0. if n==1 else float("nan")
    inner=np.partition(np.abs(x[:,None]-x[None,:]),n//2,axis=1)[:,n//2]
    value=np.partition(inner,(n-1)//2)[(n-1)//2]
    correction=([.743,1.851,.954,1.351,.993,1.198,1.005,1.131][n-2]
                if n<=9 else n/(n-.9) if n%2 else 1.)
    return float(1.1926*correction*value)


def hl_interval(x,level=.95):
    """Exact continuous-symmetry signed-rank reference, for all sample sizes used here.

    Rounded historical data contain ties, so their nominal reference is not an
    exact tie-adjusted confidence guarantee. Too-small samples need infinite bounds.
    """
    x=np.asarray(x,float)
    if not len(x) or not 0<level<1:raise ValueError("nonempty sample and level in (0,1) required")
    cdf=np.cumsum(R.signed_rank_null(len(x)))
    k=int(np.searchsorted(cdf,(1-level)/2,side="right"))
    if k==0:return -math.inf,math.inf
    w=np.sort(R.walsh_averages(x))
    return float(w[k-1]),float(w[len(w)-k])


def catoni_with_bound(x,delta,variance):
    """Two-sided Catoni tuning with a supplied variance upper bound.

    The elementary exponential inequalities give error at most
    sqrt(2 v log(2/delta)/(n-2 log(2/delta))) with probability at least 1-delta.
    """
    x=np.asarray(x,float);n=len(x);L=math.log(2/delta)
    if not 0<delta<1 or not np.isfinite(variance) or variance<=0 or n<=2*L:
        raise ValueError("positive variance bound and n > 2 log(2/delta) required")
    alpha=math.sqrt(2*L*(n-2*L)/(n*n*variance))
    def equation(theta):
        u=alpha*(x-theta)
        return np.sum(np.sign(u)*np.log1p(np.abs(u)+u*u/2))
    return float(optimize.brentq(equation,x.min()-1,x.max()+1))


def tukey_efficiency(e):
    s2=1+8*e;m4=3+240*e;delta=math.sqrt(2/math.pi)*(1+2*e)
    return ((m4/s2**2-1)/4)/(s2/delta**2-1)


def compute_tukey():
    """ARE of the mean absolute deviation to the standard deviation as estimates of scale, F = (1 - e) N(0, 1) + e
    N(0, 9): [Var(s)/E(s)^2] / [Var(d)/E(d)^2] asymptotically = ((mu4/sigma^4 - 1)/4) / (sigma^2/delta^2 - 1)."""
    eps = np.concatenate([np.linspace(0, 0.01, 41), np.linspace(0.012, 0.1, 45)])
    are = []
    for e in eps:
        s2 = (1 - e) + 9 * e
        m4 = 3 * (1 - e) + 3 * 81 * e
        dl = math.sqrt(2 / math.pi) * ((1 - e) + 3 * e)
        are.append(((m4 / s2 ** 2 - 1) / 4) / (s2 / dl ** 2 - 1))
    are = np.array(are)
    cross = float(optimize.brentq(lambda e:tukey_efficiency(e)-1,0,.01))
    # a simulation check at e = 0.01, n = 100
    g = rng(1960)
    sd, md = [], []
    for _ in range(4000):
        k = g.random(100) < 0.01
        x = np.where(k, 3 * g.standard_normal(100), g.standard_normal(100))
        sd.append(x.std(ddof=1))
        md.append(np.mean(np.abs(x - x.mean())))
    sim = (np.var(sd) / np.mean(sd) ** 2) / (np.var(md) / np.mean(md) ** 2)
    return nest({"eps": eps, "are": are, "cross": cross, "are0": float(are[0]), "sim_001": float(sim),
                 "are_001": float(np.interp(0.01, eps, are)), "are_005": float(np.interp(0.05, eps, are))})


def _estimates(x):
    t = stats.t.ppf(0.975, len(x) - 1)
    m, s = x.mean(), x.std(ddof=1)
    out = {"mean": {"est": m, "lo": m - t * s / math.sqrt(len(x)), "hi": m + t * s / math.sqrt(len(x))}}
    xs = np.sort(x)
    n = len(x)
    # the distribution-free interval for the median from binomial order statistics
    k = int(stats.binom.ppf(0.025, n, 0.5))
    out["median"] = {"est": float(np.median(x)), "lo": float(xs[k - 1]), "hi": float(xs[n - k])}
    lo, hi = hl_interval(x)
    out["hl"] = {"est": R.hodges_lehmann(x), "lo": lo, "hi": hi}
    for a in (0.1, 0.2):
        out[f"trim{int(100 * a)}"] = {"est": R.trimmed_mean(x, a)}
    out["huber"] = {"est": R.m_location(x, "huber")["mu"]}
    out["biweight"] = {"est": R.m_location(x, "biweight")["mu"]}
    return out


def compute_newcomb():
    x = museum.newcomb()
    clean = x[x > 0]
    return nest({"x": x, "n": len(x), "all": _estimates(x), "clean": _estimates(clean), "true": LIGHT_TRUE,
                 "sd": float(x.std(ddof=1)), "sd_clean": float(clean.std(ddof=1)), "mad": R.mad(x), "qn": R.qn_scale(x),
                 "outliers": sorted(x[x <= 0].tolist())})


def compute_are():
    rows = []

    def add(name, pdf, var, lim=60.0):
        rows.append({"name": name, "are": R.wilcoxon_are(pdf, var, lim)})

    add("normal", stats.norm.pdf, 1)
    add("logistic", stats.logistic.pdf, math.pi ** 2 / 3)
    add("Laplace", stats.laplace.pdf, 2)
    for nu in (3, 5, 10):
        add(f"t_{nu}", lambda t, nu=nu: stats.t.pdf(t, nu), nu / (nu - 2))
    for e in (0.01, 0.05, 0.1):
        add(f"contam_{e:g}", lambda t, e=e: (1 - e) * stats.norm.pdf(t) + e * stats.norm.pdf(t, 0, 3), (1 - e) + 9 * e)
    add("uniform", lambda t: 0.5 if abs(t) <= 1 else 0.0, 1 / 3, lim=1.0)
    f = lambda t: 3 / (20 * math.sqrt(5)) * (5 - t * t) if abs(t) <= math.sqrt(5) else 0.0
    add("parabola", f, 1.0, lim=math.sqrt(5))
    # normal scores vs t (Chernoff & Savage): ARE >= 1, = 1 at the normal; e.g. at the logistic and t3
    def ns_are(pdf, cdf, var, lim=40):
        # efficacy of the normal-scores test: (int phi'' ... ) use ARE = var * (int (d/dx Phi^{-1}(F(x))) f(x) dx)^2
        g = lambda t: pdf(t) ** 2 / stats.norm.pdf(stats.norm.ppf(min(max(cdf(t), 1e-15), 1 - 1e-15)))
        return float(var * integrate.quad(g, -lim, lim, limit=400)[0] ** 2)

    ns = {"normal": ns_are(stats.norm.pdf, stats.norm.cdf, 1), "logistic": ns_are(stats.logistic.pdf, stats.logistic.cdf, math.pi ** 2 / 3),
          "t_3": ns_are(lambda t: stats.t.pdf(t, 3), lambda t: stats.t.cdf(t, 3), 3), "uniform": float("inf")}
    return nest({"rows": rows, "bound": 108 / 125, "normal_scores": ns})


def compute_influence():
    x = museum.newcomb()
    clean = x[x > 0]
    grid = np.linspace(-60, 90, 301)
    est = {"mean": np.mean, "median": np.median, "trim10": lambda z: R.trimmed_mean(z, 0.1), "hl": R.hodges_lehmann,
           "huber": lambda z: R.m_location(z, "huber")["mu"], "biweight": lambda z: R.m_location(z, "biweight")["mu"]}
    sc = {k: R.sensitivity_curve(f, clean, grid) for k, f in est.items()}
    z = np.linspace(-5, 5, 401)
    theo = {"mean": R.influence_mean(z), "median": R.influence_median(z), "huber": R.influence_huber(z),
            "trim10": R.influence_trimmed(z, 0.1),
            "biweight": R.psi_biweight(z) / integrate.quad(lambda t: (1 - (t / 4.685) ** 2) * (1 - 5 * (t / 4.685) ** 2) * stats.norm.pdf(t),
                                                           -4.685, 4.685)[0]}
    gross = {k: (len(x) and float(np.max(np.abs(v)))) for k, v in theo.items() if k != "mean"}
    return nest({"grid": grid, "sc": sc, "z": z, "theo": theo, "gross": gross, "clean": clean})


def compute_breakdown():
    x = np.sort(museum.newcomb()[museum.newcomb() > 0])
    n = len(x)
    ms = list(range(0, 41))
    est = {"mean": np.mean, "median": np.median, "trim10": lambda z: R.trimmed_mean(z, 0.1),
           "trim20": lambda z: R.trimmed_mean(z, 0.2), "hl": R.hodges_lehmann, "huber": lambda z: R.m_location(z, "huber")["mu"]}
    out = {k: [] for k in est}
    for m in ms:
        y = x.copy()
        if m:
            y[-m:] = 1000.0
        for k, f in est.items():
            out[k].append(float(f(y)))
    bd = {k: R.empirical_breakdown(f, x) for k, f in est.items()}
    return nest({"n": n, "ms": ms, "est": out, "bd": bd, "theory": {"mean": 0, "median": 0.5, "trim10": 0.1, "trim20": 0.2,
                                                                       "hl": 1 - 1 / math.sqrt(2), "huber": 0.5}})


def compute_huber():
    eps = [0.001, 0.01, 0.02, 0.05, 0.1, 0.2]
    ks = {e: R.huber_k(e) for e in eps}
    vmin = {e: R.huber_minimax_variance(e) for e in eps}
    # V(psi_k, F) at F = (1 - e) N(0, 1) + e N(0, 10^2) as k varies, for three e
    kgrid = np.linspace(0.2, 4.0, 60)
    curves = {}
    for e in (0.0, 0.05, 0.1):
        pdf = lambda t, e=e: (1 - e) * stats.norm.pdf(t) + e * stats.norm.pdf(t, 0, 10)
        curves[f"{e:g}"] = [R.m_asymptotic_variance(lambda t, k=k: R.psi_huber(t, k), pdf, lim=80) for k in kgrid]
    # the mean and median at the same distributions
    ref = {}
    for e in (0.0, 0.05, 0.1):
        var = (1 - e) + 100 * e
        f0 = (1 - e) * stats.norm.pdf(0) + e * stats.norm.pdf(0, 0, 10)
        ref[f"{e:g}"] = {"mean": var, "median": 1 / (4 * f0 * f0)}
    eff = {"huber": 1 / R.m_asymptotic_variance(lambda t: R.psi_huber(t, 1.345), stats.norm.pdf),
           "biweight": 1 / R.m_asymptotic_variance(lambda t: R.psi_biweight(t, 4.685), stats.norm.pdf, lim=8.0),
           "median": 2 / math.pi}
    return nest({"eps": eps, "k": ks, "vmin": vmin, "kgrid": kgrid, "curves": curves, "ref": ref, "eff": eff})


def compute_scale():
    x = museum.chem()
    out = {"x": x, "n": len(x), "mean": float(x.mean()), "sd": float(x.std(ddof=1)), "median": float(np.median(x)),
           "mad": R.mad(x), "iqr": float(stats.iqr(x) / 1.349), "qn": R.qn_scale(x), "sn": sn_scale(x),
           "huber": R.m_location(x, "huber")["mu"], "hl": R.hodges_lehmann(x), "clean_mean": float(np.mean(x[x < 10])),
           "clean_sd": float(np.std(x[x < 10], ddof=1))}
    g = rng(1993)
    sims = {k: [] for k in ("sd", "mad", "qn", "sn", "iqr")}
    for _ in range(3000):
        z = g.standard_normal(100)
        sims["sd"].append(z.std(ddof=1))
        sims["mad"].append(R.mad(z))
        sims["qn"].append(R.qn_scale(z))
        sims["sn"].append(sn_scale(z))
        sims["iqr"].append(stats.iqr(z) / 1.349)
    v0 = np.var(np.log(sims["sd"]))
    out["eff"] = {k: float(v0 / np.var(np.log(v))) for k, v in sims.items()}
    out["breakdown"] = {"sd": 0.0, "iqr": 0.25, "mad": 0.5, "qn": 0.5, "sn": 0.5}
    return nest(out)


def compute_regression():
    xs, ys = museum.stars_cyg()
    X = np.column_stack([np.ones(len(xs)), xs])
    ols = np.linalg.lstsq(X, ys, rcond=None)[0]
    g = rng(1984)
    L = R.lts(X, ys, rng=g)
    M = R.mm_regression(X, ys, rng=g)
    H = R.irls_huber_regression(X, ys)
    S = R.lms(X, ys, n_sub=4000, rng=g)
    r_ols = ys - X @ ols
    s_ols = math.sqrt(r_ols @ r_ols / (len(ys) - 2))
    return nest({"x": xs, "y": ys, "ols": ols, "huber": H["coef"], "lms": S["coef"], "lts": L["coef"], "lts_rw": L["coef_rw"],
                 "mm": M["coef"], "mm_scale": M["scale"], "mm_weights": M["weights"], "lts_std": L["std_resid"],
                 "lts_outliers": L["outliers"], "ols_std": r_ols / s_ols, "giants": [10, 19, 29, 33]})


def compute_mcd():
    X, y = museum.hbk()
    m = R.mcd(X, rng=rng(1999))
    cut = m["cutoff"]
    return nest({"classical": m["classical"], "robust": m["distances"], "cutoff": cut, "outliers": m["outliers"],
                 "classical_flagged": np.where(m["classical"] > cut)[0], "X": X,
                 "loc": m["location"], "loc_classical": X.mean(0), "scatter": m["scatter"], "scatter_classical": np.cov(X.T)})


def compute_mom():
    g = rng(1983)
    a = 2.2
    mu = 1 / (a - 1)  # numpy's pareto is Lomax: mean 1/(a - 1)
    n, R_ = 500, 4000
    errs = {k: [] for k in ("mean", "trim5", "mom", "catoni")}
    for _ in range(R_):
        z = g.pareto(a, n)
        errs["mean"].append(abs(z.mean() - mu))
        errs["trim5"].append(abs(R.trimmed_mean(z, 0.05) - mu))
        errs["mom"].append(abs(R.median_of_means(z, 20, g) - mu))
        errs["catoni"].append(abs(catoni_with_bound(z, 0.001, a/((a-1)**2*(a-2))) - mu))
    qs = (0.5, 0.9, 0.99, 0.999)
    out = {k: {f"{q:g}": float(np.quantile(v, q)) for q in qs} for k, v in errs.items()}
    out["bias"] = {}
    return nest({"n": n, "R": R_, "alpha": a, "mu": mu, "variance_bound": a/((a-1)**2*(a-2)), "catoni_tuning": "known variance, two-sided delta=0.001", "q": out, "k": 20, "delta_k": float(math.exp(-20 / 8))})


def compute_board():
    W = World()
    pop = W.height[W.adult & ~W.male]
    mu = float(pop.mean())
    g = rng(2030)
    n, reps = 30, 2000
    res = {}
    for scen in ("clean", "sym", "inch"):
        hit = {"t": 0, "hl": 0}
        wid = {"t": [], "hl": []}
        for _ in range(reps):
            x = g.choice(pop, n, replace=False)
            if scen == "sym":
                x = x + np.where(g.random(n) < 0.10, g.normal(0, 40, n), 0.0)
            elif scen == "inch":
                x = np.where(g.random(n) < 0.10, x / 2.54, x)
            t = stats.t.ppf(0.975, n - 1)
            m, s = x.mean(), x.std(ddof=1) / math.sqrt(n)
            hit["t"] += m - t * s <= mu <= m + t * s
            wid["t"].append(2 * t * s)
            lo, hi = hl_interval(x)
            hit["hl"] += lo <= mu <= hi
            wid["hl"].append(hi - lo)
        res[scen] = {k: {"cover": v / reps, "width": float(np.mean(wid[k]))} for k, v in hit.items()}
    # a common practice: reject points beyond 3 MAD from the median, then use the t interval
    g2 = rng(2031)
    rej = {}
    for scen in ("clean", "sym", "inch"):
        hit, wid, dropped = 0, [], []
        for _ in range(reps):
            x = g2.choice(pop, n, replace=False)
            if scen == "sym":
                x = x + np.where(g2.random(n) < 0.10, g2.normal(0, 40, n), 0.0)
            elif scen == "inch":
                x = np.where(g2.random(n) < 0.10, x / 2.54, x)
            keep = np.abs(x - np.median(x)) <= 3 * R.mad(x)
            y = x[keep]
            t = stats.t.ppf(0.975, len(y) - 1)
            m, s = y.mean(), y.std(ddof=1) / math.sqrt(len(y))
            hit += m - t * s <= mu <= m + t * s
            wid.append(2 * t * s)
            dropped.append(n - keep.sum())
        rej[scen] = {"cover": hit / reps, "width": float(np.mean(wid)), "dropped": float(np.mean(dropped))}
    lab = {"clean": r"clean, \ $n = 30$", "sym": r"10\% gross errors $\pm N(0, 40^2)$", "inch": r"10\% recorded in inches"}
    rows = []
    for scen in ("clean", "sym", "inch"):
        rows.append(Row(30, r"$t$ interval for the mean", lab[scen], "coverage", 0.95, res[scen]["t"]["cover"], reps))
        rows.append(Row(30, r"Hodges--Lehmann interval", lab[scen], "coverage", 0.95, res[scen]["hl"]["cover"], reps))
    save_rows(30, rows)
    return nest({"mu": mu, "n": n, "reps": reps, "res": res, "reject": rej, "rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


def compute_princeton():
    """A small Princeton Robustness Study (Andrews et al. 1972): n = 20, 10,000 samples from each distribution; the
    variance of each location estimate relative to the best of them on that distribution (efficiency)."""
    g = rng(1972)
    n, R_ = 20, 10000
    dists = {
        "normal": lambda: g.standard_normal((R_, n)),
        "t3": lambda: g.standard_t(3, (R_, n)),
        "contam10": lambda: np.where(g.random((R_, n)) < 0.1, 3 * g.standard_normal((R_, n)), g.standard_normal((R_, n))),
        "slash": lambda: g.standard_normal((R_, n)) / g.random((R_, n)),
        "cauchy": lambda: g.standard_cauchy((R_, n)),
    }
    est = {"mean": lambda x: x.mean(), "median": lambda x: np.median(x), "trim10": lambda x: R.trimmed_mean(x, 0.1),
           "trim25": lambda x: R.trimmed_mean(x, 0.25), "hl": R.hodges_lehmann,
           "huber": lambda x: R.m_location(x, "huber")["mu"], "biweight": lambda x: R.m_location(x, "biweight")["mu"]}
    var = {}
    for dn, f in dists.items():
        X = f()
        var[dn] = {k: float(np.mean(np.array([e(row) for row in X]) ** 2)) for k, e in est.items()}
    eff = {dn: {k: min(var[dn].values()) / var[dn][k] for k in est} for dn in dists}
    # A finite Monte Carlo average cannot estimate an infinite second moment.
    # The sample mean has infinite MSE under slash and Cauchy distributions.
    for dn in ("slash","cauchy"):eff[dn]["mean"]=0.
    worst = {k: min(eff[dn][k] for dn in dists) for k in est}
    return nest({"n": n, "R": R_, "var": var, "eff": eff, "worst": worst, "infinite_mse": ["slash.mean","cauchy.mean"], "scope": "MSE ratios among seven estimators and five simulated distributions; not a global minimax bound"})


def compute_corrupt():
    """Replace m of the 43 main-sequence stars by bad leverage points (cool and bright, like the giants), m = 0 .. 20,
    and refit by OLS, LTS (reweighted) and MM."""
    xs, ys = museum.stars_cyg()
    giants = [10, 19, 29, 33]
    ms_idx = np.array([k for k in range(len(xs)) if k not in giants])
    g = rng(1987)
    order = g.permutation(ms_idx)
    out = {"ms": list(range(0, 21)), "ols": [], "lts": [], "mm": []}
    for m in out["ms"]:
        x, y = xs.copy(), ys.copy()
        bad = order[:m]
        x[bad] = 3.45 + 0.03 * g.standard_normal(m)
        y[bad] = 6.1 + 0.1 * g.standard_normal(m)
        X = np.column_stack([np.ones(len(x)), x])
        out["ols"].append(float(np.linalg.lstsq(X, y, rcond=None)[0][1]))
        out["lts"].append(float(R.lts(X, y, rng=rng(100 + m))["coef_rw"][1]))
        out["mm"].append(float(R.mm_regression(X, y, rng=rng(200 + m))["coef"][1]))
    out["n"] = len(xs)
    return nest(out)


ITEMS = {
    "tukey": compute_tukey, "newcomb": compute_newcomb, "are": compute_are, "influence": compute_influence,
    "breakdown": compute_breakdown, "huber": compute_huber, "scale": compute_scale, "regression": compute_regression,
    "mcd": compute_mcd, "mom": compute_mom, "board": compute_board, "princeton": compute_princeton, "corrupt": compute_corrupt,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
