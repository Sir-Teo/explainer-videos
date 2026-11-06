"""Precompute every number in Part 48 of *Statistics, Built* ("Empirical Processes").

    OMP_NUM_THREADS=1 python -m videos.stats.stats48.compute            # everything missing (a few minutes)
    python -m videos.stats.stats48.compute --force board

Results are cached in ``.cache/stats48/<name>.json``.  Old Faithful and Newcomb's light are the Museum's; everything
else is exact arithmetic or a seeded simulation.

Items:
    hook      KS statistics at n = 5, 20, 100 against Kolmogorov's law; empirical-process paths and a bridge
    gc        E sup |F_n - F| by n; the exact Rademacher average of half-lines; one sequence's sup over n
    vc        growth functions by brute force: half-lines, intervals, half-planes, rectangles; Sauer-Shelah
    entropy   greedy covers of half-lines (L2) and of Lipschitz functions (sup); brackets
    chain     a Brownian path on dyadic nets; E max over the level-k net; the union bound; the chaining bound
    donsker   exact KS quantiles against Kolmogorov's; Old Faithful's ECDF with a 95% band
    conc      the tail of n D_n - E n D_n against Bousquet, McDiarmid and DKW; a low-variance class
    delta     the quantile process and the Kaplan-Meier process: pointwise SDs against the delta method
    zest      mean absolute deviation about an estimated centre: naive and correct variances; Newcomb
    rates     Chernoff's distribution; the Grenander estimator at a point, n^(1/3)
    erm       threshold classifiers: the uniform deviation, ERM's excess risk and the VC bound
    bands     coverage of 95% KS bands: Kolmogorov, exact, DKW, bootstrap, multiplier
    ksest     the estimated-parameter empirical process (Durbin); sizes; Newcomb's normality
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
from explainer.stats.kit import empirical as EK
from explainer.stats.kit import smooth as SK
from explainer.stats.kit import survival as SV

CACHE = Cache("stats48")
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


def hist(v, edges):
    h, _ = np.histogram(v, bins=edges, density=True)
    return h


# ---------------------------------------------------------------------------------------------------------------
def compute_hook():
    r = rng(4801)
    edges = np.linspace(0, 2.4, 49)
    out = {"edges": edges}
    for n in (5, 20, 100):
        d = math.sqrt(n) * EK.ks_stats_uniform(r.random((20000, n)))
        out[str(n)] = {"hist": hist(d, edges), "q95": float(np.quantile(d, 0.95)), "mean": float(d.mean()),
                       "exact95": float(stats.kstwo.ppf(0.95, n) * math.sqrt(n))}
    u = np.linspace(0.01, 2.4, 240)
    out["u"] = u
    out["dens"] = EK.kolmogorov_density(u)
    out["k95"] = EK.kolmogorov_quantile(0.95)
    out["kmean"] = math.sqrt(math.pi / 2) * math.log(2)
    grid = np.linspace(0, 1, 401)
    paths = {}
    for n in (20, 200, 5000):
        paths[str(n)] = EK.empirical_process(r.random(n), lambda v: v, grid)
    out["grid"] = grid
    out["paths"] = paths
    out["bridge"] = EK.brownian_bridge(400, r)[0]
    return out


def compute_gc():
    r = rng(4802)
    ns = [10, 20, 50, 100, 200, 500, 1000, 2000]
    ed, rad = [], []
    for n in ns:
        reps = 20000 if n <= 200 else 4000
        ed.append(float(EK.ks_stats_uniform(r.random((reps, n))).mean()))
        rad.append(EK.rademacher_halflines(n))
    # one sequence: sup |F_n - F| along n = 1 .. 5000, for three seeds
    seqs = {}
    checkpoints = np.unique(np.round(np.logspace(0, np.log10(5000), 120)).astype(int))
    for s in range(3):
        x = rng(4900 + s).random(5000)
        seqs[str(s)] = [EK.ks_stat(x[:k], lambda v: v) for k in checkpoints]
    return {"ns": ns, "ed": ed, "rad": rad, "two_rad": [2 * v for v in rad], "kmean": math.sqrt(math.pi / 2) * math.log(2),
            "checkpoints": checkpoints, "seqs": seqs}


def compute_vc():
    r = rng(4803)
    rows = []
    for n in range(1, 11):
        pts = r.standard_normal((n, 2))
        rect = max(EK.dichotomies_rectangles(r.standard_normal((n, 2))) for _ in range(6))
        rows.append({"n": n, "halflines": EK.dichotomies_halflines(r.random(n)), "intervals": EK.dichotomies_intervals(r.random(n)),
                     "halfplanes": EK.dichotomies_halfplanes(pts), "rect": rect, "all": 2 ** n,
                     "ss1": EK.sauer_shelah(n, 1), "ss2": EK.sauer_shelah(n, 2), "ss3": EK.sauer_shelah(n, 3), "ss4": EK.sauer_shelah(n, 4)})
    diamond = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]], float)
    three = np.array([[0, 0], [1, 0], [0.4, 0.9]], float)
    four = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
    return {"rows": rows, "diamond_rect": EK.dichotomies_rectangles(diamond), "three_hp": EK.dichotomies_halfplanes(three),
            "four_hp": EK.dichotomies_halfplanes(four)}


def compute_entropy():
    grid = np.linspace(0, 1, 801)
    halflines = (grid[None, :] <= grid[:, None]).astype(float)
    eps = [0.4, 0.3, 0.2, 0.15, 0.1, 0.07, 0.05]
    hl = [EK.greedy_cover(halflines, e) for e in eps]
    br = [EK.bracketing_halflines(e) for e in eps]
    f = EK.lipschitz_paths(61, 20000, rng(4804))
    eps_l = [0.3, 0.25, 0.2, 0.15, 0.12, 0.1, 0.08]
    lip = [EK.greedy_cover(f, e, "sup") for e in eps_l]
    return {"eps": eps, "hl": hl, "hl_log": [math.log(v) for v in hl], "br": br, "eps_l": eps_l, "lip": lip,
            "lip_log": [math.log(v) for v in lip]}


def compute_chain():
    r = rng(4805)
    m = 2 ** 12
    t = np.linspace(0, 1, m + 1)
    w = np.concatenate([[0.0], np.cumsum(r.standard_normal(m) / math.sqrt(m))])
    ks = list(range(0, 11))
    emax = [EK.bm_sup_on_grid(k, rng(4810 + k), reps=4000, fine=12) for k in ks]
    c = EK.chaining_bound_bm(40)
    partial = np.cumsum(c["terms"]).tolist()
    union = [math.sqrt(2 * math.log(2 ** k + 1)) for k in ks]
    dud = math.sqrt(2) * math.sqrt(math.pi) / 2  # int_0^1 sqrt(log 1/eps^2) d eps
    return {"t": t[::8], "w": w[::8], "ks": ks, "emax": emax, "exact": c["exact"], "terms": c["terms"], "partial": partial,
            "bound": c["bound"], "union": union, "dudley": dud}


def compute_donsker():
    rows = []
    k95 = EK.kolmogorov_quantile(0.95)
    for n in (5, 10, 20, 50, 100, 1000):
        rows.append({"n": n, "exact": float(stats.kstwo.ppf(0.95, n) * math.sqrt(n)), "kolm": k95,
                     "size_kolm": float(stats.kstwo.sf(k95 / math.sqrt(n), n))})
    _, wait = museum.faithful()
    x = np.sort(np.asarray(wait, float))
    n = len(x)
    c = k95 / math.sqrt(n)
    g = np.linspace(40, 100, 601)
    fn = np.searchsorted(x, g, side="right") / n
    # a normal fit is visibly wrong: D against the fitted normal
    d_norm = EK.ks_stat(x, lambda v: stats.norm.cdf((v - x.mean()) / x.std(ddof=1)))
    return {"rows": rows, "k95": k95, "n": n, "grid": g, "fn": fn, "lo": np.clip(fn - c, 0, 1), "hi": np.clip(fn + c, 0, 1),
            "half": c, "fit": stats.norm.cdf((g - x.mean()) / x.std(ddof=1)), "d_norm": d_norm, "mean": float(x.mean()),
            "sd": float(x.std(ddof=1))}


def compute_conc():
    r = rng(4806)
    n = 100
    u = r.random((40000, n))
    Z = EK.ks_stats_uniform(u) * n
    ez = float(Z.mean())
    ts = np.linspace(0, 16, 81)
    sim = [float(np.mean(Z - ez >= t)) for t in ts]
    bous = EK.bousquet_tail(ts, n, 0.25, ez)
    mcd = np.exp(-2 * ts ** 2 / n)
    dkw = np.minimum(2 * np.exp(-2 * ((ez + ts) / math.sqrt(n)) ** 2), 1)
    # a low-variance class: half-lines with t <= q
    q = 0.02
    us = np.sort(u, axis=1)
    i = np.arange(1, n + 1)
    fn_left = (i - 1) / n
    ok = us <= q
    dev = np.maximum(np.where(ok, np.abs(i / n - us), 0), np.where(ok, np.abs(us - fn_left), 0)).max(axis=1)
    dev = np.maximum(dev, np.abs(np.mean(u <= q, axis=1) - q))
    Zq = dev * n
    ezq = float(Zq.mean())
    sim95 = float(np.quantile(Zq - ezq, 0.95))

    def inv(f):
        lo, hi = 0.0, 100.0
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if f(mid) > 0.05:
                lo = mid
            else:
                hi = mid
        return hi

    b95 = inv(lambda t: EK.bousquet_tail(t, n, q * (1 - q), ezq)[0])
    m95 = inv(lambda t: math.exp(-2 * t ** 2 / n))
    full = {"sim95": float(np.quantile(Z - ez, 0.95)), "b95": inv(lambda t: EK.bousquet_tail(t, n, 0.25, ez)[0]), "m95": m95}
    return {"n": n, "ez": ez, "ts": ts, "sim": sim, "bous": bous, "mcd": mcd, "dkw": dkw, "q": q, "ezq": ezq,
            "low": {"sim95": sim95, "b95": b95, "m95": m95}, "full": full}


def compute_delta():
    r = rng(4807)
    n = 200
    ps = np.array([0.1, 0.25, 0.5, 0.75, 0.9])
    x = np.sort(r.exponential(size=(20000, n)), axis=1)
    k = np.ceil(n * ps).astype(int) - 1
    Q = -np.log(1 - ps)
    sd_sim = np.sqrt(n) * np.std(x[:, k] - Q[None, :], axis=0)
    sd_th = np.sqrt(ps / (1 - ps))
    # the quantile process on a grid, one path, and its limit -B(p)/f(Q(p))
    pg = np.linspace(0.02, 0.95, 200)
    kg = np.ceil(n * pg).astype(int) - 1
    path = math.sqrt(n) * (x[0, kg] + np.log(1 - pg))
    # Kaplan-Meier: Exp(1) times, Exp(0.5) censoring
    tt = np.array([0.25, 0.5, 1.0, 1.5, 2.0])
    km_vals = []
    for _ in range(3000):
        T = r.exponential(size=n)
        C = r.exponential(scale=2.0, size=n)
        obs, ev = np.minimum(T, C), (T <= C).astype(int)
        km = SV.kaplan_meier(obs, ev)
        km_vals.append(SV.km_at(km, tt))
    km_vals = np.array(km_vals)
    km_sd = np.sqrt(n) * np.std(km_vals - np.exp(-tt)[None, :], axis=0)
    km_th = np.sqrt(np.exp(-2 * tt) * (np.exp(1.5 * tt) - 1) / 1.5)
    return {"n": n, "ps": ps, "sd_sim": sd_sim, "sd_th": sd_th, "pg": pg, "path": path, "band": 1.96 * np.sqrt(pg / (1 - pg)),
            "tt": tt, "km_sd": km_sd, "km_th": km_th, "km_reps": 3000}


def mad_ifs(x):
    x = np.asarray(x, float)
    n = len(x)
    out = {}
    for name, c in (("mean", x.mean()), ("median", np.median(x))):
        th = float(np.mean(np.abs(x - c)))
        naive = np.abs(x - c) - th
        slope = 2 * np.mean(x <= c) - 1
        # about the mean the centre's influence x - c enters with the slope 2F(c) - 1; about the median the slope is 0
        corr = naive + slope * (x - c) if name == "mean" else naive
        out[name] = {"theta": th, "se_naive": float(naive.std() / math.sqrt(n)), "se": float(corr.std() / math.sqrt(n)),
                     "slope": float(slope)}
    return out


def compute_zest():
    d = EK.mad_exponential()
    r = rng(4808)
    n = 200
    x = r.exponential(size=(20000, n))
    est_mean = np.mean(np.abs(x - x.mean(axis=1, keepdims=True)), axis=1)
    est_known = np.mean(np.abs(x - 1.0), axis=1)
    est_med = np.mean(np.abs(x - np.median(x, axis=1, keepdims=True)), axis=1)
    est_med_known = np.mean(np.abs(x - math.log(2)), axis=1)
    sim = {"mean_est": float(n * est_mean.var()), "mean_known": float(n * est_known.var()),
           "median_est": float(n * est_med.var()), "median_known": float(n * est_med_known.var())}
    nc = museum.newcomb()
    nw = mad_ifs(nc)
    # bootstrap SE of the MAD about the mean, for Newcomb
    rb = rng(4809)
    idx = rb.integers(0, len(nc), size=(4000, len(nc)))
    xb = np.asarray(nc, float)[idx]
    boot = np.mean(np.abs(xb - xb.mean(axis=1, keepdims=True)), axis=1)
    nw["mean"]["se_boot"] = float(boot.std())
    return {"exact": d, "sim": sim, "n": n, "newcomb": nw, "nc_n": len(nc)}


def compute_rates():
    r = rng(4810)
    z = EK.chernoff_draws(r, reps=6000, half=2.5, m=3000)
    edges = np.linspace(-1.6, 1.6, 41)
    f0, fp = math.exp(-1), -math.exp(-1)
    const = EK.grenander_constant(f0, fp)
    rows = []
    errs = {}
    for n, reps in ((100, 3000), (1000, 2000), (10000, 600)):
        e = []
        for _ in range(reps):
            g = SK.grenander(r.exponential(size=n))
            e.append(float(SK.grenander_at(g, 1.0)[0]) - f0)
        e = np.array(e) * n ** (1 / 3)
        errs[str(n)] = e
        rows.append({"n": n, "sd": float(e.std()), "mean": float(e.mean()), "reps": reps})
    return {"edges": edges, "z_hist": hist(z, edges), "z_sd": float(z.std()), "z_sd_ref": EK.CHERNOFF_SD, "const": const,
            "pred_sd": const * EK.CHERNOFF_SD, "rows": rows, "e_edges": np.linspace(-1.2, 1.2, 41),
            "e_hist": hist(errs["1000"], np.linspace(-1.2, 1.2, 41)), "z_scaled_x": (edges[:-1] + edges[1:]) / 2 * const}


def compute_erm():
    r = rng(4811)
    ns = [20, 50, 100, 200, 500, 1000, 2000]
    t0, flip = 0.3, 0.2

    def risk(t):
        return flip + (1 - 2 * flip) * np.abs(t - t0)

    sup, exc, bound = [], [], []
    for n in ns:
        reps = 2000 if n <= 500 else 600
        s_, e_ = [], []
        for _ in range(reps):
            x = np.sort(r.random(n))
            y = (x > t0).astype(int) ^ (r.random(n) < flip).astype(int)
            # classifier 1{x > t}: empirical risk at thresholds between points
            cand = np.concatenate([[0.0], x])
            # errors: for t = cand[k], points <= t are predicted 0, > t predicted 1
            err0 = np.concatenate([[0], np.cumsum(y)])  # misclassified among predicted 0: y = 1
            err1 = np.concatenate([[np.sum(1 - y)], np.sum(1 - y) - np.cumsum(1 - y)])
            emp = (err0 + err1) / n
            k = int(np.argmin(emp))
            e_.append(risk(cand[k]) - flip)
            # the uniform deviation over thresholds, at the candidates and just below each point
            s_.append(float(np.max(np.abs(emp - risk(cand)))))
        sup.append(float(np.mean(s_)))
        exc.append(float(np.mean(e_)))
        bound.append(2 * 2 * math.sqrt(2 * math.log(2 * (n + 1)) / n))
    return {"ns": ns, "sup": sup, "exc": exc, "bound": bound, "two_sup": [2 * v for v in sup]}


def band_coverage(n, reps, seed):
    r = rng(seed)
    q = EK.ks_band_quantiles(n)
    hit = {k: [] for k in ("kolmogorov", "exact", "dkw", "bootstrap", "multiplier")}
    for _ in range(reps):
        x = r.standard_normal(n)
        d = EK.ks_stat(x, stats.norm.cdf)
        for k in ("kolmogorov", "exact", "dkw"):
            hit[k].append(d <= q[k])
        hit["bootstrap"].append(d <= EK.bootstrap_ks_quantile(x, r, B=499))
        hit["multiplier"].append(d <= EK.multiplier_ks_quantile(x, r, B=499))
    return {k: float(np.mean(v)) for k, v in hit.items()} | {"q": q}


def compute_bands():
    out = {"20": band_coverage(20, 2000, 4812), "100": band_coverage(100, 1000, 4813), "reps": {"20": 2000, "100": 1000}}
    _, wait = museum.faithful()
    x = np.sort(np.asarray(wait, float))
    r = rng(4814)
    out["faithful"] = {"n": len(x), "kolm": EK.kolmogorov_quantile(0.95) / math.sqrt(len(x)),
                       "boot": EK.bootstrap_ks_quantile(x, r, B=1999), "mult": EK.multiplier_ks_quantile(x, r, B=1999),
                       "dkw": EK.ks_band_quantiles(len(x))["dkw"], "exact": EK.ks_band_quantiles(len(x))["exact"]}
    return out


def compute_ksest():
    r = rng(4815)
    n = 100
    z = r.standard_normal((20000, n))
    m = z.mean(axis=1, keepdims=True)
    s = z.std(axis=1, ddof=1, keepdims=True)
    zg = np.linspace(-3, 3, 61)
    fn = (z[:, :, None] <= zg[None, None, :]).mean(axis=1)
    fhat = stats.norm.cdf((zg[None, :] - m) / s)
    var_sim = n * np.var(fn - fhat, axis=0)
    var_dur = EK.durbin_variance_normal(zg)
    var_bridge = stats.norm.cdf(zg) * (1 - stats.norm.cdf(zg))
    # the null law of D with estimated parameters is parameter-free: one table serves all
    Dn = EK.ks_estimated_normal_rows(r.standard_normal((40000, 20)))
    crit_est = float(np.quantile(Dn, 0.95))
    crit_kolm = float(stats.kstwo.ppf(0.95, 20))
    # exponential with estimated rate
    xe = r.exponential(size=(40000, 50))
    ue = 1 - np.exp(-xe / xe.mean(axis=1, keepdims=True))
    De = EK.ks_stats_uniform(ue)
    crit_kolm50 = float(stats.kstwo.ppf(0.95, 50))
    size_exp_naive = float(np.mean(De > crit_kolm50))
    size_norm_naive = float(np.mean(Dn > crit_kolm))
    # Newcomb: normality by parametric bootstrap, with and without the two outliers
    nc = np.asarray(museum.newcomb(), float)
    full = EK.parametric_bootstrap_ks(nc, rng(4816), B=9999)
    trimmed = EK.parametric_bootstrap_ks(nc[nc > 0], rng(4817), B=9999)
    full["naive_p"] = float(stats.kstwo.sf(full["D"], len(nc)))
    trimmed["naive_p"] = float(stats.kstwo.sf(trimmed["D"], int(np.sum(nc > 0))))
    xe1 = np.linspace(0, 5, 101)
    return {"zg": zg, "var_sim": var_sim, "var_dur": var_dur, "var_bridge": var_bridge, "crit_est": crit_est, "crit_kolm": crit_kolm,
            "size_norm_naive": size_norm_naive, "size_exp_naive": size_exp_naive, "crit_exp": float(np.quantile(De, 0.95)),
            "crit_kolm50": crit_kolm50, "newcomb": full, "newcomb_trim": trimmed, "nc_n": len(nc), "nc_trim_n": int(np.sum(nc > 0)),
            "xe": xe1, "var_exp": EK.durbin_variance_exponential(xe1), "var_exp_bridge": (1 - np.exp(-xe1)) * np.exp(-xe1)}


def compute_board():
    rows = []
    b20 = band_coverage(20, 2000, 4820)
    names = {"kolmogorov": "KS band from Kolmogorov's limit", "exact": "KS band, exact finite-n quantile", "dkw": "DKW band (Massart's constant)",
             "bootstrap": "KS band by the bootstrap", "multiplier": "KS band by the multiplier bootstrap"}
    for k, name in names.items():
        rows.append(Row(48, name, "N(0, 1) data, n = 20", "coverage", 0.95, b20[k], 2000))
    # size of the KS test of exponentiality with an estimated rate, Kolmogorov's table vs a parametric bootstrap
    r = rng(4821)
    reps, n, B = 2000, 30, 199
    crit = float(stats.kstwo.ppf(0.95, n))
    rej_naive, rej_pb = [], []
    for _ in range(reps):
        x = r.exponential(scale=3.0, size=n)
        d = EK.ks_stats_uniform((1 - np.exp(-x / x.mean()))[None, :])[0]
        rej_naive.append(d > crit)
        xb = r.exponential(scale=x.mean(), size=(B, n))
        db = EK.ks_stats_uniform(1 - np.exp(-xb / xb.mean(axis=1, keepdims=True)))
        rej_pb.append((1 + np.sum(db >= d)) / (B + 1) <= 0.05)
    rows.append(Row(48, "KS test, estimated rate, Kolmogorov's table", "exponential data, n = 30", "size", 0.05, float(np.mean(rej_naive)), reps))
    rows.append(Row(48, "KS test, estimated rate, parametric bootstrap", "exponential data, n = 30", "size", 0.05, float(np.mean(rej_pb)), reps))
    save_rows(48, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "hook": compute_hook, "gc": compute_gc, "vc": compute_vc, "entropy": compute_entropy, "chain": compute_chain,
    "donsker": compute_donsker, "conc": compute_conc, "delta": compute_delta, "zest": compute_zest, "rates": compute_rates,
    "erm": compute_erm, "bands": compute_bands, "ksest": compute_ksest, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
