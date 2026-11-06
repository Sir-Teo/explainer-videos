"""Precompute every number in Part 61 of *Statistics, Built* ("Optimal Transport in Statistics").

    OMP_NUM_THREADS=1 python -m videos.stats.stats61.compute            # everything missing (a few minutes)
    python -m videos.stats.stats61.compute --force board

Results are cached in ``.cache/stats61/<name>.json``.  NHANES and Old Faithful are the Museum's; everything else is
exact arithmetic or a seeded simulation.

Items:
    hook      Monge's earthworks in one dimension: the monotone map between two piles, and its cost against a crossing plan
    lp        a small discrete problem: the Kantorovich plan by LP with its dual potentials, and Sinkhorn's plans
    quantile  NHANES BMI, men against women: W1 as the area between CDFs, W2 and its mean/spread decomposition
    geodesic  Old Faithful (standardized) against a Gaussian cloud: the optimal matching and displacement interpolation
    rates     E W between two samples from the uniform cube against n, for d = 1, 2, 3, 5, 10
    sinkhorn  Sinkhorn's convergence and bias as epsilon shrinks; the Sinkhorn divergence's dimension-free rate
    maps      estimating a Brenier map between Gaussians: the empirical and the entropic estimators against n
    bary      NHANES systolic pressure by age group: the W2 barycenter against the mixture; a Gaussian barycenter
    ranks     center-outward ranks and quantile contours of Old Faithful, against Mahalanobis ellipses
    tests     sizes and power of Hotelling's T^2 and the rank energy test under bivariate Cauchy data
    langevin  Langevin particles against the exact Wasserstein gradient flow of KL for a Gaussian target
    flow      a toy flow-matching sampler from a Gaussian to Old Faithful: independent against OT pairing
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
from explainer.stats.kit import ot as O

CACHE = Cache("stats61")
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


def _nhanes():
    d = museum.nhanes()
    sbp = np.nanmean(np.column_stack([d["sbp1"], d["sbp2"], d["sbp3"]]), axis=1)
    ok = np.isfinite(sbp) & np.isfinite(d["bmi"]) & np.isfinite(d["age"]) & np.isfinite(d["sex"])
    return {k: d[k][ok] for k in ("age", "sex", "bmi")} | {"sbp": sbp[ok]}


def _faithful_std():
    e, w = museum.faithful()
    X = np.column_stack([e, w])
    return (X - X.mean(0)) / X.std(0)


def _kde(v, xs, h=None):
    v = np.asarray(v, float)
    h = h or 1.06 * v.std() * len(v) ** -0.2
    return np.exp(-0.5 * ((xs[:, None] - v[None]) / h) ** 2).sum(1) / (len(v) * h * math.sqrt(2 * math.pi))


def compute_hook():
    xs = np.linspace(0, 10, 401)
    f = stats.norm.pdf(xs, 3, 1)
    g = 0.5 * stats.norm.pdf(xs, 6, 0.7) + 0.5 * stats.norm.pdf(xs, 8, 0.5)
    F = stats.norm.cdf(xs, 3, 1)
    G = 0.5 * stats.norm.cdf(xs, 6, 0.7) + 0.5 * stats.norm.cdf(xs, 8, 0.5)
    u = (np.arange(40) + 0.5) / 40
    src = stats.norm.ppf(u, 3, 1)
    tgt = np.interp(u, G, xs)
    w1_mono = float(np.mean(np.abs(tgt - src)))
    w2_mono = float(math.sqrt(np.mean((tgt - src) ** 2)))
    # a crossing plan: pair the leftmost earth with the rightmost hole
    w1_cross = float(np.mean(np.abs(tgt[::-1] - src)))
    w2_cross = float(math.sqrt(np.mean((tgt[::-1] - src) ** 2)))
    T = np.interp(F, G, xs)  # the monotone map G^{-1}(F(x))
    return {"xs": xs, "f": f, "g": g, "src": src, "tgt": tgt, "T": T, "w1": w1_mono, "w2": w2_mono, "w1_cross": w1_cross,
            "w2_cross": w2_cross}


def compute_lp():
    r = rng(6101)
    X = r.standard_normal((6, 2)) * 0.8
    Y = r.standard_normal((7, 2)) * 0.8 + np.array([2.5, 0.5])
    a = r.dirichlet(np.full(6, 4.0))
    b = r.dirichlet(np.full(7, 4.0))
    C = O.cost_matrix(X, Y, 2)
    lp = O.kantorovich_lp(a, b, C)
    sk = {}
    for eps in (2.0, 0.5, 0.1):
        s = O.sinkhorn(a, b, C, eps, 20000, 1e-12)
        sk[f"{eps:g}"] = {"P": s["P"], "cost": s["cost"], "obj": s["obj"], "iters": s["iters"]}
    nz = int(np.sum(lp["P"] > 1e-9))
    slack = lp["f"][:, None] + lp["g"][None, :] - C
    return {"X": X, "Y": Y, "a": a, "b": b, "C": C, "P": lp["P"], "cost": lp["cost"], "f": lp["f"], "g": lp["g"],
            "dual": float(a @ lp["f"] + b @ lp["g"]), "nonzero": nz, "max_slack": float(slack.max()), "sinkhorn": sk}


def compute_quantile():
    f = _nhanes()
    m, w = f["bmi"][f["sex"] == 1], f["bmi"][f["sex"] == 2]
    w1 = O.wasserstein_1d(m, w, 1)
    w2 = O.wasserstein_1d(m, w, 2)
    u = (np.arange(199) + 1) / 200
    qm, qw = np.quantile(m, u), np.quantile(w, u)
    xs = np.linspace(14, 60, 300)
    Fm = np.searchsorted(np.sort(m), xs, side="right") / len(m)
    Fw = np.searchsorted(np.sort(w), xs, side="right") / len(w)
    # W2^2 = (mean difference)^2 + (sd difference)^2 + 2 sd_m sd_w (1 - corr of the quantile functions)
    um = (np.arange(4000) + 0.5) / 4000
    Qm, Qw = np.quantile(m, um), np.quantile(w, um)
    rho = float(np.corrcoef(Qm, Qw)[0, 1])
    return {"n_m": len(m), "n_w": len(w), "mean_m": float(m.mean()), "mean_w": float(w.mean()), "sd_m": float(m.std()),
            "sd_w": float(w.std()), "w1": w1, "w2": w2, "w1_area": O.w1_cdf_area(m, w), "u": u, "qm": qm, "qw": qw, "xs": xs,
            "Fm": Fm, "Fw": Fw, "rho": rho, "shape_term": float(2 * m.std() * w.std() * (1 - rho))}


def compute_geodesic():
    r = rng(6102)
    Y = _faithful_std()
    n = len(Y)
    X = r.standard_normal((n, 2)) * 0.6 + np.array([-2.5, 2.5])
    a = O.assignment(X, Y, 2)
    rand = r.permutation(n)
    cost_rand = float(np.mean(np.sum((X - Y[rand]) ** 2, 1)))
    # mixture interpolation for contrast: the densities averaged, (1 - t) mu + t nu, sampled at t = 1/2
    return {"X": X, "Y": Y, "perm": a["perm"], "W2": a["W"], "cost": a["cost"], "cost_rand": cost_rand, "n": n}


def compute_rates():
    r = rng(6103)
    out = {}
    ns1 = [25, 50, 100, 200, 400, 800, 1600]
    v = []
    for n in ns1:
        v.append(float(np.mean([O.wasserstein_1d(r.random(n), r.random(n), 1) for _ in range(40)])))
    out["d1"] = {"ns": ns1, "W": v, "slope": float(np.polyfit(np.log(ns1), np.log(v), 1)[0])}
    ns = [25, 50, 100, 200, 400, 800]
    for d in (2, 3, 5, 10):
        out[f"d{d}"] = O.empirical_rate(d, ns, 8, r, 1)
    return out


def compute_sinkhorn():
    r = rng(6104)
    n = 60
    X = r.standard_normal((n, 2))
    Y = r.standard_normal((n, 2)) * np.array([1.5, 0.5]) + np.array([2.0, 1.0])
    a = np.full(n, 1 / n)
    C = O.cost_matrix(X, Y, 2)
    exact = O.assignment(X, Y, 2)["cost"]
    rows = []
    traces = {}
    for eps in (3.0, 1.0, 0.3, 0.1, 0.03):
        s = O.sinkhorn(a, a, C, eps, 50000, 1e-9)
        rows.append({"eps": eps, "cost": s["cost"], "obj": s["obj"], "iters": s["iters"], "entropy_plan": float(-np.sum(s["P"] * np.log(s["P"] + 1e-300)))})
        if eps in (1.0, 0.1):
            traces[f"{eps:g}"] = s["errs"][:4000]
    # sample complexity: two independent samples from N(0, I_5); W2^2 against the Sinkhorn divergence at eps = 1
    d, ns, reps = 5, [25, 50, 100, 200, 400], 6
    w2, sd = [], []
    for m in ns:
        a1, a2 = [], []
        for _ in range(reps):
            U, V = r.standard_normal((m, d)), r.standard_normal((m, d))
            a1.append(O.assignment(U, V, 2)["cost"])
            a2.append(O.sinkhorn_divergence(U, V, 1.0))
        w2.append(float(np.mean(a1)))
        sd.append(float(np.mean(a2)))
    return {"n": n, "exact": exact, "rows": rows, "traces": traces, "d": d, "ns": ns, "w2sq": w2, "sdiv": sd,
            "slope_w2": float(np.polyfit(np.log(ns), np.log(w2), 1)[0]), "slope_sd": float(np.polyfit(np.log(ns), np.log(sd), 1)[0])}


def compute_maps():
    r = rng(6105)
    Sig = np.array([[3.0, 1.0], [1.0, 1.0]])
    A = O.gaussian_map(np.eye(2), Sig)
    L = np.linalg.cholesky(Sig)
    ns = [50, 100, 200, 400, 800]
    Z = r.standard_normal((500, 2))
    Ttrue = Z @ A.T
    out = {"ns": ns, "emp": [], "ent": [], "A": A}
    for n in ns:
        e1, e2 = [], []
        for _ in range(4):
            X = r.standard_normal((n, 2))
            Y = r.standard_normal((n, 2)) @ L.T
            perm = O.assignment(X, Y, 2)["perm"]
            # the empirical map extended by the nearest source point
            nn = np.argmin(O.cost_matrix(Z, X, 2), axis=1)
            e1.append(float(np.mean(np.sum((Y[perm][nn] - Ttrue) ** 2, 1))))
            T = O.entropic_map(X, Y, 0.5 * n ** (-1 / 3))
            e2.append(float(np.mean(np.sum((T(Z) - Ttrue) ** 2, 1))))
        out["emp"].append(float(np.mean(e1)))
        out["ent"].append(float(np.mean(e2)))
    out["slope_emp"] = float(np.polyfit(np.log(ns), np.log(out["emp"]), 1)[0])
    out["slope_ent"] = float(np.polyfit(np.log(ns), np.log(out["ent"]), 1)[0])
    return out


def compute_bary():
    f = _nhanes()
    groups = [(18, 40), (40, 60), (60, 81)]
    samples = [f["sbp"][(f["age"] >= a) & (f["age"] < c)] for a, c in groups]
    xs = np.linspace(80, 200, 400)
    dens = [_kde(s, xs, 4.0) for s in samples]
    wts = np.array([len(s) for s in samples], float)
    wts /= wts.sum()
    mix = sum(w * dd for w, dd in zip(wts, dens))
    q = O.barycenter_1d(samples, wts, 2000)
    bary = _kde(q, xs, 4.0)
    means = [float(s.mean()) for s in samples]
    sds = [float(s.std()) for s in samples]
    # Gaussian barycenter of two covariances, and its check against the closed form for commuting matrices
    Sb = O.gaussian_barycenter([np.diag([1.0, 4.0]), np.diag([4.0, 1.0])])
    mix_sd = float(math.sqrt(np.sum(wts * (np.array(sds) ** 2 + np.array(means) ** 2)) - np.sum(wts * np.array(means)) ** 2))
    return {"groups": [f"{a}--{c - 1}" for a, c in groups], "ns": [len(s) for s in samples], "xs": xs, "dens": dens, "mix": mix,
            "bary": bary, "means": means, "sds": sds, "bary_mean": float(q.mean()), "bary_sd": float(q.std()), "mix_sd": mix_sd,
            "wts": wts, "gauss_bary": Sb}


def compute_ranks():
    X = _faithful_std()
    n = len(X)
    G = O.spherical_grid(n, n_rad=6)
    co = O.center_outward(X, G)
    F = co["F"]
    rad = np.linalg.norm(F, axis=1)
    levels = sorted(set(np.round(rad, 6)) - {0.0})
    contours = {}
    for lev in levels:
        idx = np.flatnonzero(np.abs(rad - lev) < 1e-6)
        ang = np.arctan2(F[idx, 1], F[idx, 0])
        contours[f"{lev:.4f}"] = X[idx[np.argsort(ang)]]
    # Mahalanobis ellipses with the same probability content as each rank level under normality: chi^2_2 quantiles
    S = np.cov(X.T)
    ell = {}
    th = np.linspace(0, 2 * math.pi, 200)
    Lc = np.linalg.cholesky(S)
    for lev in levels:
        rr = math.sqrt(stats.chi2.ppf(lev, 2))
        ell[f"{lev:.4f}"] = (np.column_stack([np.cos(th), np.sin(th)]) * rr) @ Lc.T + X.mean(0)
    # the center-outward median: the points assigned nearest the origin
    inner = X[np.argsort(rad)[:2]].mean(0)
    return {"X": X, "F": F, "levels": levels, "contours": contours, "ellipses": ell, "median": inner, "n": n}


def compute_tests():
    r = rng(6106)
    reps, n = 1000, 40
    out = {"reps": reps, "n": n}
    rh = rr = 0
    for _ in range(reps):
        X, Y = r.standard_cauchy((n, 2)), r.standard_cauchy((n, 2))
        rh += O.hotelling_two_sample(X, Y)["p"] < 0.05
        rr += O.rank_energy_test(X, Y, r, 199)["p"] < 0.05
    out["size_hot"], out["size_rank"] = rh / reps, rr / reps
    ph = pr = 0
    preps = 300
    for _ in range(preps):
        X, Y = r.standard_cauchy((n, 2)), r.standard_cauchy((n, 2)) + 1.0
        ph += O.hotelling_two_sample(X, Y)["p"] < 0.05
        pr += O.rank_energy_test(X, Y, r, 199)["p"] < 0.05
    out["preps"], out["pow_hot"], out["pow_rank"] = preps, ph / preps, pr / preps
    return out


def compute_langevin():
    r = rng(6107)
    Sig = np.array([[1.0, 0.8], [0.8, 1.0]])
    Si = np.linalg.inv(Sig)
    m0, S0 = np.array([4.0, -3.0]), 0.2 * np.eye(2)
    X0 = r.multivariate_normal(m0, S0, 600)
    h, steps, every = 0.02, 300, 15
    snaps = O.langevin(lambda X: -X @ Si.T, X0, h, steps, r, every)
    ts = [k * h * every for k in range(len(snaps))]
    exact = O.fokker_planck_gaussian(m0, S0, np.zeros(2), Sig, ts)
    kl_exact = [O.gaussian_kl(m, S, np.zeros(2), Sig) for m, S in exact]
    w2_exact = [O.gaussian_w2(m, S, np.zeros(2), Sig) for m, S in exact]
    kl_emp = [O.gaussian_kl(Z.mean(0), np.cov(Z.T), np.zeros(2), Sig) for Z in snaps]
    rate = float(1 / np.linalg.eigvalsh(Sig).max())
    return {"snaps": [Z[:300] for Z in snaps], "ts": ts, "kl_exact": kl_exact, "kl_emp": kl_emp, "w2_exact": w2_exact,
            "h": h, "rate": rate, "Sig": Sig}


def compute_flow():
    r = rng(6108)
    Y = _faithful_std()
    n = len(Y)
    X0 = r.standard_normal((n, 2))
    out = {"n": n}
    Zs = [r.standard_normal((n, 2)) for _ in range(5)]
    for pair in ("independent", "ot"):
        v = O.flow_matching_fit(X0, Y if pair == "ot" else Y[r.permutation(n)], r, 0.3, 20, pair)
        res = {}
        for steps in (1, 2, 5, 20):
            res[str(steps)] = float(np.mean([O.assignment(O.integrate_flow(v, Z, steps)[-1], Y, 2)["W"] for Z in Zs]))
        snaps = O.integrate_flow(v, Zs[0], 20)
        out[pair] = {"W": res, "snaps": [s for s in snaps[::4]] + [snaps[-1]], "one_step": O.integrate_flow(v, Zs[0], 1)[-1]}
        # straightness: displacement over path length, averaged over particles
        P = np.array(snaps)
        length = np.sum(np.linalg.norm(np.diff(P, axis=0), axis=2), axis=0)
        disp = np.linalg.norm(P[-1] - P[0], axis=1)
        out[pair]["straight"] = float(np.mean(disp / np.maximum(length, 1e-12)))
    out["Y"] = Y
    out["W_noise"] = float(np.mean([O.assignment(Z, Y, 2)["W"] for Z in Zs]))
    return out


def compute_board():
    t = load("tests")
    rows = [Row(61, r"Hotelling's $T^2$, \ two samples", r"bivariate Cauchy, \ $n = m = 40$", "size", 0.05, t["size_hot"], t["reps"]),
            Row(61, r"rank energy test (OT ranks)", r"bivariate Cauchy, \ $n = m = 40$", "size", 0.05, t["size_rank"], t["reps"])]
    save_rows(61, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows]}


ITEMS = {
    "hook": compute_hook, "lp": compute_lp, "quantile": compute_quantile, "geodesic": compute_geodesic, "rates": compute_rates,
    "sinkhorn": compute_sinkhorn, "maps": compute_maps, "bary": compute_bary, "ranks": compute_ranks, "tests": compute_tests,
    "langevin": compute_langevin, "flow": compute_flow, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
