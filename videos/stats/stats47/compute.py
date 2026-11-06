"""Precompute every number in Part 47 of *Statistics, Built* ("Asymptotic Statistics").

    OMP_NUM_THREADS=1 python -m videos.stats.stats47.compute            # everything missing (a few minutes)
    python -m videos.stats.stats47.compute --force board

Results are cached in ``.cache/stats47/<name>.json``.  Newcomb's light and Old Faithful are the Museum's; everything
else is exact arithmetic or a seeded simulation.

Items:
    hook        Hodges's estimator: exact scaled risk over theta and over local h, for n = 25 ... 10^6
    delta       the delta method for log xbar; the second-order case
    mest        Huber's M-estimator: the sandwich variance against simulation, clean and contaminated; Newcomb
    quantile    the Bahadur remainder's RMS by n
    influence   influence functions of the mean, median, Huber and trimmed means; the delta method for the variance
    ustat       Gini's mean difference: exact, first-order and simulated variances; a degenerate kernel's limit
    ranks       Wilcoxon against t: power at local alternatives under three error laws; Pitman AREs
    lan         Cauchy local log-likelihood ratios against LAN
    contig      local power from Le Cam's third lemma against simulation
    hajek       the local risk of Hodges's estimator; the limit laws at h; the LAM bound
    bahadur     exact Bahadur slopes of the sign and z tests; the ratio against Pitman's 2/pi
    bootstrap   coverage of percentile, basic, bootstrap-t and BCa intervals; one-sided errors by n
    saddle      Daniels's saddlepoint and Lugannani-Rice for a mean of exponentials
    nonreg      the uniform maximum: the bootstrap's atom and the m-out-of-n repair
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import asymptotics as AK
from explainer.stats.kit import bootstrap as BK
from explainer.stats.kit import robust as RK

CACHE = Cache("stats47")
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


# ---------------------------------------------------------------------------------------------------------------
def compute_hook():
    th = np.linspace(-0.6, 0.6, 481)
    out = {"theta": th}
    for n in (25, 100, 1000, 10000):
        out[f"r{n}"] = AK.hodges_risk(th, n)
    h = np.linspace(0, 45, 1801)
    peaks = {}
    for n in (100, 10 ** 4, 10 ** 6):
        r = AK.hodges_local(h, n)
        out[f"h{n}"] = r
        peaks[str(n)] = {"max": float(r.max()), "at": float(h[np.argmax(r)]), "n14": n ** 0.25}
    out["h"] = h
    out["peaks"] = peaks
    out["at0"] = {str(n): float(AK.hodges_risk(0.0, n)) for n in (25, 100, 1000, 10000)}
    return out


def compute_delta():
    """The delta method: sqrt n (log xbar - log mu) for Exp(1) data against N(0, 1); and the second-order case
    g(x) = x^2 at mu = 0, where n xbar^2 -> chi^2_1."""
    g = rng(4710)
    rows = []
    edges = np.linspace(-4, 4, 41)
    hists = {}
    for n in (5, 20, 200):
        x = g.exponential(1.0, (40000, n)).mean(1)
        z = math.sqrt(n) * np.log(x)
        rows.append({"n": n, "mean": float(z.mean()), "sd": float(z.std()), "skew": float(stats.skew(z)),
                     "ks": float(stats.kstest(z, "norm").statistic)})
        hists[str(n)] = np.histogram(z, bins=edges, density=True)[0]
    y = g.normal(0, 1, (40000, 50)).mean(1)
    q = 50 * y ** 2
    return {"rows": rows, "edges": edges, "hists": hists, "second_q": np.quantile(q, [0.5, 0.9, 0.95]),
            "chi2_q": stats.chi2.ppf([0.5, 0.9, 0.95], 1)}


def compute_mest():
    g = rng(4701)
    n, reps = 50, 4000
    psi = lambda u: RK.psi_huber(u, 1.345)  # noqa: E731
    out = {}
    for name, draw, pdf in (("normal", lambda s: g.normal(0, 1, s), stats.norm.pdf),
                            ("contaminated", lambda s: np.where(g.random(s) < 0.1, g.normal(0, 5, s), g.normal(0, 1, s)),
                             lambda t: 0.9 * stats.norm.pdf(t) + 0.1 * stats.norm.pdf(t, 0, 5))):
        x = draw((reps, n))
        hub = np.array([RK.m_location(r, "huber", scale=1.0)["mu"] for r in x])
        mean = x.mean(1)
        V = RK.m_asymptotic_variance(psi, pdf)
        out[name] = {"sim_huber": float(n * hub.var()), "sandwich": V, "sim_mean": float(n * mean.var()),
                     "mean_theory": 1.0 if name == "normal" else 0.9 + 0.1 * 25}
    # Newcomb's light: Huber with a sandwich SE against the mean
    x = museum.newcomb()
    s = RK.mad(x)
    fit = RK.m_location(x, "huber")
    u = (x - fit["mu"]) / s
    p = RK.psi_huber(u, 1.345)
    dp = (np.abs(u) <= 1.345).astype(float)
    se = s * math.sqrt(np.mean(p ** 2) / np.mean(dp) ** 2 / len(x))
    out["newcomb"] = {"n": len(x), "mean": float(x.mean()), "se_mean": float(x.std(ddof=1) / math.sqrt(len(x))),
                      "huber": fit["mu"], "se_huber": se, "median": float(np.median(x)), "min": float(x.min())}
    return out


def compute_quantile():
    g = rng(4702)
    rows = []
    for n in (50, 200, 1000, 5000):
        r = AK.bahadur_remainder(n, 2000 if n < 5000 else 800, g)
        rows.append({"n": n, "rms": r["rms_rem"], "sd": r["sd_full"], "theory": r["theory_sd"]})
    return {"rows": rows}


def compute_influence():
    z = np.linspace(-4, 4, 161)
    out = {"z": z, "mean": RK.influence_mean(z), "median": RK.influence_median(z), "huber": RK.influence_huber(z),
           "trimmed": RK.influence_trimmed(z, 0.1)}
    # the functional delta method for the variance: IF(x) = (x - mu)^2 - sigma^2, so Var(s^2) ~ (mu4 - sigma^4)/n
    g = rng(4703)
    n = 40
    for name, draw, mu4 in (("normal", lambda s: g.normal(0, 1, s), 3.0), ("t5", lambda s: g.standard_t(5, s) / math.sqrt(5 / 3), 9.0)):
        x = draw((20000, n))
        s2 = x.var(1, ddof=1)
        out[f"var_{name}"] = {"sim": float(n * s2.var()), "delta": mu4 - 1}
    return out


def compute_ustat():
    g = rng(4704)
    rows = []
    for n in (10, 20, 50):
        gv = AK.gini_variance(n)
        x = g.normal(0, 1, (4000, n))
        us = np.array([AK.u_statistic(r, lambda a, b: np.abs(a - b)) for r in x])
        rows.append({"n": n, "exact": gv["var"], "first": gv["first_order"], "sim": float(us.var())})
    # degenerate kernel h(x, y) = x y with E X = 0: n U -> chi^2_1 - 1
    n = 200
    x = g.normal(0, 1, (20000, n))
    s1, s2 = x.sum(1), (x ** 2).sum(1)
    U = (s1 ** 2 - s2) / (n * (n - 1))
    nU = n * U
    edges = np.linspace(-1.5, 6, 46)
    hist = np.histogram(nU, bins=edges, density=True)[0]
    return {"rows": rows, "zeta1": AK.gini_variance(20)["zeta1"], "zeta2": AK.gini_variance(20)["zeta2"],
            "deg_edges": edges, "deg_hist": hist, "deg_mean": float(nU.mean()), "deg_var": float(nU.var())}


def compute_ranks():
    g = rng(4705)
    n, reps = 30, 8000
    laws = {"normal": (lambda s: g.normal(0, 1, s), 1.0), "Laplace": (lambda s: g.laplace(0, 1 / math.sqrt(2), s), 1.0),
            "t3": (lambda s: g.standard_t(3, s) / math.sqrt(3), 1.0)}
    hs = [0.0, 1.0, 2.0, 3.0]
    out = {"n": n, "hs": hs, "laws": {}}
    for name, (draw, _) in laws.items():
        pw_t, pw_w = [], []
        for h in hs:
            x = draw((reps, n)) + h / math.sqrt(n)
            t = x.mean(1) / (x.std(1, ddof=1) / math.sqrt(n))
            pw_t.append(float(np.mean(t > stats.t.ppf(0.95, n - 1))))
            r = stats.rankdata(np.abs(x), axis=1)
            W = np.sum(r * (x > 0), axis=1)
            mu, var = n * (n + 1) / 4, n * (n + 1) * (2 * n + 1) / 24
            pw_w.append(float(np.mean((W - mu) / math.sqrt(var) > stats.norm.ppf(0.95))))
        out["laws"][name] = {"t": pw_t, "wilcoxon": pw_w}
    out["are"] = {"normal": AK.pitman_are("wilcoxon_normal"), "Laplace": AK.pitman_are("wilcoxon_laplace"),
                  "t3": RK.wilcoxon_are(lambda u: stats.t.pdf(u * math.sqrt(3), 3) * math.sqrt(3), 1.0),
                  "min": AK.pitman_are("wilcoxon_min")}
    return out


def compute_lan():
    g = rng(4706)
    out = {}
    for n in (25, 400):
        r = AK.cauchy_local_llr(n, 1.5, 20000, g)
        out[str(n)] = {"mean": r["mean"], "var": r["var"], "hist": np.histogram(r["llr"], bins=50, range=(-5, 3), density=True)[0]}
    out["lan_mean"], out["lan_var"] = -1.5 ** 2 * 0.5 / 2, 1.5 ** 2 * 0.5
    out["edges"] = np.linspace(-5, 3, 51)
    return out


def compute_contig():
    g = rng(4707)
    n, reps = 100, 20000
    hs = np.linspace(0, 4, 9)
    sim_t, sim_s = [], []
    for h in hs:
        x = g.normal(h / math.sqrt(n), 1, (reps, n))
        t = x.mean(1) / (x.std(1, ddof=1) / math.sqrt(n))
        sim_t.append(float(np.mean(t > stats.norm.ppf(0.95))))
        k = (x > 0).sum(1)
        sim_s.append(float(np.mean((k - n / 2) / math.sqrt(n / 4) > stats.norm.ppf(0.95))))
    hh = np.linspace(0, 4, 81)
    return {"n": n, "hs": hs, "sim_t": sim_t, "sim_sign": sim_s, "hh": hh, "lp_t": AK.local_power(hh, 1.0),
            "lp_sign": AK.local_power(hh, 2 / math.pi)}


def compute_hajek():
    h = np.linspace(-12, 12, 961)
    out = {"h": h}
    for n in (10 ** 2, 10 ** 4, 10 ** 6, 10 ** 8):
        out[f"n{n}"] = AK.hodges_local(np.abs(h), n)
    cs = [1, 2, 4, 8]
    sup = {}
    for n in (10 ** 2, 10 ** 4, 10 ** 6, 10 ** 8):
        r = out[f"n{n}"]
        sup[str(n)] = [float(r[np.abs(h) <= c].max()) for c in cs]
    out["cs"], out["sup"] = cs, sup
    return out


def compute_bahadur():
    th = np.linspace(0.01, 2.5, 120)
    p = stats.norm.cdf(th)
    slope_sign = 2 * (p * np.log(2 * p) + (1 - p) * np.log(2 * (1 - p)))
    slope_z = th ** 2
    return {"theta": th, "sign": slope_sign, "z": slope_z, "ratio": slope_sign / slope_z, "pitman": 2 / math.pi}


def _coverage(draw, true, n, reps, B, g, alpha=0.1):
    hits = {"percentile": [], "basic": [], "t": [], "bca": [], "normal": []}
    lo_miss = {k: [] for k in hits}
    for _ in range(reps):
        x = draw(n)
        m = x.mean()
        idx = g.integers(0, n, (B, n))
        reps_ = x[idx].mean(1)
        jack = (x.sum() - x) / (n - 1)
        cis = {"percentile": BK.percentile_ci(reps_, alpha), "basic": BK.basic_ci(reps_, m, alpha),
               "bca": BK.bca_ci(reps_, m, jack, alpha)[0]}
        xb = x[idx]
        tt = (xb.mean(1) - m) / (xb.std(1, ddof=1) / math.sqrt(n))
        q1, q2 = np.quantile(tt, [alpha / 2, 1 - alpha / 2])
        se = x.std(ddof=1) / math.sqrt(n)
        cis["t"] = (m - q2 * se, m - q1 * se)
        tq = stats.t.ppf(1 - alpha / 2, n - 1)
        cis["normal"] = (m - tq * se, m + tq * se)
        for k, (a, b) in cis.items():
            hits[k].append(a <= true <= b)
            lo_miss[k].append(true < a)
    return {k: float(np.mean(v)) for k, v in hits.items()}, {k: float(np.mean(v)) for k, v in lo_miss.items()}, hits


def compute_bootstrap():
    g = rng(4708)
    rows = []
    for n in (10, 20, 40, 80):
        cov, low, _ = _coverage(lambda m: g.exponential(1.0, m), 1.0, n, 1500, 999, g)
        rows.append({"n": n, "cov": cov, "low": low})
    return {"rows": rows}


def compute_saddle():
    n = 5
    x = np.linspace(0.1, 3.0, 291)
    d = AK.mean_exp_density(x, n)
    xt = np.linspace(1.05, 3.0, 40)
    t = AK.lugannani_rice(xt, n)
    rel = {k: (np.abs(np.asarray(v) / t["exact"] - 1)).tolist() for k, v in t.items() if k != "exact"}
    return {"n": n, "x": x, "exact": d["exact"], "normal": d["normal"], "edgeworth": d["edgeworth"], "saddle": d["saddle"],
            "saddle_ratio": float((d["saddle"] / d["exact"])[0]), "xt": xt, "tail_exact": t["exact"], "tail_normal": t["normal"],
            "tail_lr": t["lr"], "rel": rel, "at2": {k: float(np.interp(2.0, xt, v)) for k, v in (("exact", t["exact"]),
                                                                                                 ("normal", t["normal"]), ("lr", t["lr"]))}}


def compute_nonreg():
    g = rng(4709)
    a = AK.uniform_max_bootstrap(200, 20000, g)
    b = AK.uniform_max_bootstrap(2000, 20000, g, m=40)
    edges = np.linspace(0, 5, 26)
    return {"n": 200, "atom": a["atom0"], "theory_atom": a["theory_atom"], "limit_atom": 1 - math.exp(-1),
            "hist_boot": np.histogram(a["stat"], bins=edges, density=True)[0], "hist_m": np.histogram(b["stat"], bins=edges, density=True)[0],
            "edges": edges, "ks_boot": a["ks_exp"], "ks_m": b["ks_exp"], "atom_m": b["atom0"]}


def compute_board():
    g = rng(4799)
    rows = []
    cov, low, hits = _coverage(lambda m: g.exponential(1.0, m), 1.0, 20, 2000, 999, g)
    for k, name in (("normal", "Student $t$ interval"), ("percentile", "percentile bootstrap"), ("t", "bootstrap-$t$"), ("bca", "BCa")):
        rows.append(Row(47, name + " for a mean", "Exp(1) data, n = 20", "coverage", 0.9, cov[k], len(hits[k])))
    # the uniform maximum: a percentile interval for theta from the ordinary bootstrap, and from m-out-of-n
    reps, n, B = 2000, 200, 999
    hit_b, hit_m = [], []
    for _ in range(reps):
        x = g.random(n)
        M = x.max()
        sb = n * (M - x[g.integers(0, n, (B, n))].max(1))
        m = 40
        sm = m * (M - x[g.integers(0, n, (B, m))].max(1))
        # interval for theta = 1 from the pivot n(theta - M) ~ law of sb: theta in [M + q05/n, M + q95/n]
        qb = np.quantile(sb, [0.05, 0.95])
        qm = np.quantile(sm, [0.05, 0.95])
        hit_b.append(M + qb[0] / n <= 1 <= M + qb[1] / n)
        hit_m.append(M + qm[0] / n <= 1 <= M + qm[1] / n)
    rows.append(Row(47, "bootstrap interval for a uniform maximum", "U(0, theta), n = 200", "coverage", 0.9, float(np.mean(hit_b)), reps))
    rows.append(Row(47, "m-out-of-n bootstrap (m = 40)", "U(0, theta), n = 200", "coverage", 0.9, float(np.mean(hit_m)), reps))
    save_rows(47, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "hook": compute_hook, "delta": compute_delta, "mest": compute_mest, "quantile": compute_quantile, "influence": compute_influence,
    "ustat": compute_ustat, "ranks": compute_ranks, "lan": compute_lan, "contig": compute_contig, "hajek": compute_hajek,
    "bahadur": compute_bahadur, "bootstrap": compute_bootstrap, "saddle": compute_saddle, "nonreg": compute_nonreg,
    "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
