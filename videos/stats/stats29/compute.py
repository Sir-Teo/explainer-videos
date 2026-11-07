"""Precompute every number in Part 29 of *Statistics, Built* ("Smoothing").

    python -m videos.stats.stats29.compute            # everything missing (several minutes)
    python -m videos.stats.stats29.compute --force rbc

Results are cached in ``.cache/stats29/<name>.json``.  Old Faithful, the motorcycle crash and New York's air quality
are the Museum's; the rest are seeded simulations.

Items:
    faithful    Old Faithful's 272 eruptions: histograms, KDEs, bandwidth selectors, Silverman's critical bandwidths and
                mode test
    histmise    the histogram's exact MISE as a function of bin width, and its n^{-2/3} rate
    kdemise     the KDE's exact MISE (Marron & Wand 1992), its bias and variance, AMISE, and the n^{-4/5} rate
    selectors   bandwidth selectors on 300 simulated samples: normal reference, Silverman, LSCV, Sheather--Jones
    curse       Silverman's table, the empty corners of the cube, nearest-neighbour distances
    locpoly     Nadaraya--Watson vs local linear: equivalent kernels at the boundary; LOESS on the motorcycle data
    spline      smoothing splines on the motorcycle data: fits by df, the Demmler--Reinsch basis, GCV and REML
    lamsim      GCV vs REML on 300 simulated data sets: the chosen df and the resulting error
    rkhs        kernel ridge regression and its Gaussian-process reading on the motorcycle data
    wavelets    VisuShrink and SureShrink on Donoho & Johnstone's signals, against a GCV spline; the max of n normals
    gam         an additive model for New York's ozone by backfitting
    rbc         Coverage Board rows: pointwise KDE intervals at the MSE-optimal bandwidth, conventional vs robust
                bias-corrected
    shape       isotonic regression and the Grenander estimator: the cube-root rate
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import optim as Op
from explainer.stats.kit import smooth as Sm

CACHE = Cache("stats29")
load = CACHE.load

# a two-humped stand-in for Old Faithful's durations: 35% short eruptions, 65% long
GEYSER = Sm.NormalMixture([0.35, 0.65], [2.0, 4.3], [0.27, 0.42])


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


def silverman_bootstrap(x, k, B, g, grid=None):
    """Finite-bootstrap estimate; Silverman's raw test still needs calibration qualifications.

    Adding one avoids reporting an impossible zero Monte Carlo tail probability.
    This does not make the smoothed bootstrap an exact finite-sample level test.
    """
    if B < 1:
        raise ValueError("at least one bootstrap sample is required")
    result = Sm.silverman_test(x, k, B, g, grid)
    count = int(round(result["p"] * B))
    return dict(result, p=(count+1)/(B+1), exceedances=count,
                mc_se=math.sqrt((count+1)/(B+1)*(1-(count+1)/(B+1))/(B+1)),
                calibration="raw smoothed-bootstrap estimate; no Hall-York calibration")


def compute_faithful():
    e, w = museum.faithful()
    grid = np.linspace(1.0, 6.0, 401)
    hs = {"nr": Sm.normal_reference_h(e), "silverman": Sm.silverman_h(e), "sj": Sm.sheather_jones_h(e)}
    lg = np.geomspace(0.04, 1.0, 120)
    lv = [Sm.lscv(e, h) for h in lg]
    hs["lscv"] = float(lg[int(np.argmin(lv))])
    kd = {k: Sm.kde(e, grid, h) for k, h in hs.items()}
    for h in (0.05, 0.1, 0.25, 0.5, 1.0):
        kd[f"h{h:g}"] = Sm.kde(e, grid, h)
    crit = {k: Sm.critical_bandwidth(e, k, grid) for k in (1, 2, 3, 4)}
    g = rng(1981)
    tests = {k: silverman_bootstrap(e, k, 500, g, grid) for k in (1, 2, 3)}
    hist = {}
    for bw in (0.5, 0.25):
        for off in (0.0, 0.25 * bw, 0.5 * bw, 0.75 * bw):
            edges = np.arange(1.0 - off, 6.0 + bw, bw)
            hist[f"{bw:g}_{off:g}"] = {"edges": edges, "dens": Sm.histogram_density(e, edges)}
    modes = {k: Sm.count_modes(v) for k, v in kd.items()}
    return nest({"x": e, "waiting": w, "grid": grid, "h": hs, "kde": kd, "lscv_h": lg, "lscv": lv, "critical": crit,
                 "tests": tests, "hist": hist, "modes": modes,
                 "n": len(e), "short_share": float(np.mean(e < 3)), "mean": float(e.mean()), "sd": float(e.std(ddof=1))})


def compute_histmise():
    out = {"ns": [100, 1000, 10000], "hs": np.geomspace(0.02, 1.5, 120)}
    lo, hi = 0.0, 6.5
    for n in out["ns"]:
        m = []
        for h in out["hs"]:
            # average the exact MISE over bin origins (the origin matters little on average)
            vals = []
            for off in np.linspace(0, h, 6, endpoint=False):
                edges = np.arange(lo - off, hi + h, h)
                vals.append(Sm.histogram_mise(GEYSER.cdf, edges, n, GEYSER.R(0)))
            m.append(np.mean(vals))
        out[f"mise_{n}"] = m
        out[f"best_{n}"] = {"h": float(out["hs"][int(np.argmin(m))]), "mise": float(np.min(m))}
    out["amise_h"] = {n: Sm.histogram_amise_h(n, GEYSER.R(1)) for n in out["ns"]}
    ns = np.array(out["ns"], float)
    out["slope"] = float(np.polyfit(np.log(ns), np.log([out[f"best_{n}"]["mise"] for n in out["ns"]]), 1)[0])
    out["slope_h"] = float(np.polyfit(np.log(ns), np.log([out[f"best_{n}"]["h"] for n in out["ns"]]), 1)[0])
    return nest(out)


def compute_kdemise():
    hs = np.geomspace(0.02, 1.5, 200)
    out = {"hs": hs, "ns": [100, 1000, 10000]}
    R2 = GEYSER.R(2)
    RK = 1 / (2 * math.sqrt(math.pi))
    for n in out["ns"]:
        m = [GEYSER.kde_mise(h, n) for h in hs]
        out[f"mise_{n}"] = m
        out[f"amise_{n}"] = [RK / (n * h) + h ** 4 / 4 * R2 for h in hs]
        out[f"ivar_{n}"] = [RK / (n * h) for h in hs]
        out[f"ibias2_{n}"] = [h ** 4 / 4 * R2 for h in hs]
        i = int(np.argmin(m))
        out[f"best_{n}"] = {"h": float(hs[i]), "mise": float(m[i]), "amise_h": GEYSER.kde_amise_h(n)}
    ns = np.array(out["ns"], float)
    out["slope"] = float(np.polyfit(np.log(ns), np.log([out[f"best_{n}"]["mise"] for n in out["ns"]]), 1)[0])
    hb = np.array([GEYSER.kde_amise_h(int(n)) for n in ns])
    out["slope_h"] = float(np.polyfit(np.log(ns), np.log(hb), 1)[0])
    # the histogram's best MISE at the same n, for the comparison
    try:
        hm = load("histmise")
        out["hist_best"] = {n: hm[f"best_{n}"]["mise"] for n in out["ns"]}
    except Exception:
        out["hist_best"] = None
    out["efficiency"] = {k: Sm.kernel_efficiency(k) for k in ("epanechnikov", "biweight", "triangular", "gaussian", "uniform")}
    out["R2"] = R2
    # bias and variance pointwise at n = 1000 and the AMISE-optimal h, for the picture
    grid = np.linspace(0.5, 6.0, 300)
    h = GEYSER.kde_amise_h(1000)
    out["grid"] = grid
    out["f"] = GEYSER.pdf(grid)
    out["bias"] = 0.5 * h * h * GEYSER.d2(grid)
    out["sd"] = np.sqrt(GEYSER.pdf(grid) * RK / (1000 * h))
    return nest(out)


def compute_selectors():
    g = rng(1991)
    n, R = 200, 300
    hstar = GEYSER.kde_amise_h(n)
    hs = np.geomspace(0.03, 1.5, 300)
    hm = float(hs[int(np.argmin([GEYSER.kde_mise(h, n) for h in hs]))])
    grid = np.linspace(-0.5, 7.0, 600)
    lg = np.geomspace(0.03, 1.2, 80)
    res = {k: [] for k in ("nr", "silverman", "lscv", "sj")}
    ise = {k: [] for k in res}
    for _ in range(R):
        x = GEYSER.rvs(n, g)
        hh = {"nr": Sm.normal_reference_h(x), "silverman": Sm.silverman_h(x), "sj": Sm.sheather_jones_h(x),
              "lscv": float(lg[int(np.argmin([Sm.lscv(x, h) for h in lg]))])}
        f = GEYSER.pdf(grid)
        for k, h in hh.items():
            res[k].append(h / hm)
            ise[k].append(float(np.trapezoid((Sm.kde(x, grid, h) - f) ** 2, grid)))
    out = {"n": n, "R": R, "h_mise": hm, "h_amise": hstar, "mise_opt": GEYSER.kde_mise(hm, n), "ratio": res, "ise": ise}
    out["summary"] = {k: {"median": float(np.median(v)), "q10": float(np.quantile(v, 0.1)), "q90": float(np.quantile(v, 0.9)),
                          "mean_ise": float(np.mean(ise[k]))} for k, v in res.items()}
    return nest(out)


def compute_curse():
    table = {d: Sm.silverman_table(d) for d in range(1, 11)}
    vol = {d: math.pi ** (d / 2) / math.gamma(d / 2 + 1) / 2 ** d for d in range(1, 21)}
    g = rng(1961)
    nn = {}
    for d in (1, 2, 5, 10, 20, 50):
        X = g.uniform(0, 1, (1000, d))
        D = np.sqrt(((X[:200, None, :] - X[None, :, :]) ** 2).sum(-1))
        D[np.arange(200), np.arange(200)] = np.inf
        nn[d] = {"nearest": float(np.median(D.min(1))), "farthest": float(np.median(np.where(np.isfinite(D), D, 0).max(1))),
                 "ratio": float(np.median(D.min(1) / np.where(np.isfinite(D), D, 0).max(1)))}
    rates = {d: 4 / (4 + d) for d in range(1, 11)}
    return nest({"table": table, "ball": vol, "nn": nn, "rates": rates})


def compute_locpoly():
    # equivalent kernels at an interior point and at the boundary for an even design on [0, 1]
    x = np.linspace(0, 1, 101)
    h = 0.1
    ek = {}
    for deg in (0, 1):
        for t in (0.0, 0.5):
            ek[f"{deg}_{t:g}"] = Sm.local_poly(x, np.zeros_like(x), [t], h, deg)["weights"][0]
    # boundary bias for y = 2x: NW pulls towards the interior
    lin = {deg: Sm.local_poly(x, 2 * x, x, h, deg)["fit"] for deg in (0, 1)}
    # the motorcycle data
    t, a = museum.mcycle()
    tt = np.linspace(t.min(), t.max(), 300)
    nw = Sm.local_poly(t, a, tt, 2.0, 0)["fit"]
    ll = Sm.local_poly(t, a, tt, 2.0, 1)["fit"]
    lo = Sm.loess(t, a, tt, 0.2, 1, 0)
    lr = Sm.loess(t, a, tt, 0.2, 1, 3)
    # Old Faithful: waiting time after an eruption of a given length
    e, w = museum.faithful()
    ee = np.linspace(e.min(), e.max(), 200)
    fw = Sm.local_poly(e, w, ee, 0.3, 1)["fit"]
    return nest({"x": x, "h": h, "ek": ek, "lin": lin, "t": t, "a": a, "tt": tt, "nw": nw, "ll": ll, "loess": lo,
                 "loess_robust": lr, "e": e, "w": w, "ee": ee, "fw": fw})


def spline_reml(sp, lam):
    """Profile Gaussian REML including within-tie contrasts and known precision weights."""
    if lam <= 0 or len(sp.y) <= 2:
        raise ValueError("positive penalty and at least three observations required")
    rootw = np.sqrt(sp.W)
    d, U = np.linalg.eigh(sp.K/rootw[:,None]/rootw[None,:])
    v = 1 + 1/(lam*d[2:])
    z = U.T @ (rootw*sp.ybar)
    within = np.sum(sp.w*(sp.y-sp.ybar[sp.inv])**2)
    m = len(sp.y)-2
    s2 = (np.sum(z[2:]**2/v)+within)/m
    return float(.5*(np.log(v).sum()+m*np.log(s2)+m))


def compute_spline():
    t, a = museum.mcycle()
    sp = Sm.SmoothingSpline(t, a)
    tt = np.linspace(t.min(), t.max(), 400)
    fits = {}
    for df in (4, 8, 12, 25):
        lam = sp.lam_for_df(df)
        fits[str(df)] = {"lam": lam, "fit": sp.predict(lam, tt)}
    grid = np.geomspace(1e-3, 1e5, 161)
    gcv = [sp.gcv(l) for l in grid]
    dfs = [sp.df(l) for l in grid]
    lg = float(grid[int(np.argmin(gcv))])
    # Full Gaussian REML retains the replicate contrasts at tied crash times.
    spu = Sm.SmoothingSpline(sp.t, sp.ybar)
    reml = [spline_reml(sp, l) for l in grid]
    lr = float(grid[int(np.argmin(reml))])
    # the Demmler--Reinsch basis on the unique times, unit weights
    d, U = spu.eigen()
    basis = {k: U[:, k] for k in range(0, 8)}
    shrink = {"df8": 1 / (1 + spu.lam_for_df(8) * d), "df25": 1 / (1 + spu.lam_for_df(25) * d)}
    resid = a - sp.fit(lg)[sp.inv]
    return nest({"t": t, "a": a, "tt": tt, "fits": fits, "grid": grid, "gcv": gcv, "df": dfs, "lam_gcv": lg,
                 "df_gcv": sp.df(lg), "fit_gcv": sp.predict(lg, tt), "reml": reml, "lam_reml": lr, "df_reml": sp.df(lr),
                 "fit_reml": sp.predict(lr, tt), "eig": d, "basis": basis, "knots": sp.t, "shrink": shrink,
                 "sigma_gcv": float(np.sqrt(np.sum(resid ** 2) / (len(a) - sp.df(lg)))), "n_unique": len(sp.t)})


def compute_lamsim():
    g = rng(1985)
    n, R = 100, 300
    x = np.linspace(0, 1, n)
    f = np.sin(2 * np.pi * x) + 0.5 * np.cos(6 * np.pi * x) * x
    sp0 = Sm.SmoothingSpline(x, np.zeros(n))
    grid = np.geomspace(1e-9, 1e-1, 121)
    S = {l: sp0.smoother(l) for l in grid}
    dfs = {l: float(np.trace(S[l])) for l in grid}
    out = {"gcv_df": [], "reml_df": [], "gcv_mse": [], "reml_mse": [], "oracle_mse": [], "oracle_df": []}
    d, U = sp0.eigen()
    for _ in range(R):
        y = f + 0.3 * g.standard_normal(n)
        best = {"gcv": (np.inf, None), "reml": (np.inf, None), "oracle": (np.inf, None)}
        z = U.T @ y
        for l in grid:
            fit = S[l] @ y
            r = y - fit
            gv = float(np.mean(r * r) / (1 - dfs[l] / n) ** 2)
            v = 1 + 1 / (l * d[2:])
            s2 = np.sum(z[2:] ** 2 / v) / (n - 2)
            rm = 0.5 * (np.sum(np.log(v)) + (n - 2) * np.log(s2))
            mse = float(np.mean((fit - f) ** 2))
            for k, c in (("gcv", gv), ("reml", rm), ("oracle", mse)):
                if c < best[k][0]:
                    best[k] = (c, l)
        for k in ("gcv", "reml", "oracle"):
            l = best[k][1]
            out[f"{k}_df"].append(dfs[l])
            out[f"{k}_mse"].append(float(np.mean((S[l] @ y - f) ** 2)))
    out["summary"] = {k: {"df_median": float(np.median(out[f"{k}_df"])), "df_q10": float(np.quantile(out[f"{k}_df"], 0.1)),
                          "df_q90": float(np.quantile(out[f"{k}_df"], 0.9)), "mse": float(np.mean(out[f"{k}_mse"])),
                          "worst5": float(np.mean(sorted(out[f"{k}_mse"])[-15:]))} for k in ("gcv", "reml", "oracle")}
    out["n"], out["R"], out["sigma"] = n, R, 0.3
    return nest(out)


def compute_rkhs():
    t, a = museum.mcycle()
    tt = np.linspace(t.min(), t.max(), 300)
    s = (t - t.mean()) / t.std()
    ss = (tt - t.mean()) / t.std()
    fits = {}
    for ell in (0.05, 0.15, 0.5):
        for lam in (0.1, 1.0):
            kr = Sm.kernel_ridge(s, a, lam, ell, ss)
            fits[f"{ell:g}_{lam:g}"] = {"pred": kr["pred"], "df": kr["df"]}
    # the GP reading: f ~ GP(0, tau^2 k), noise sigma^2, lam = sigma^2 / tau^2; posterior mean = kernel ridge
    ell, lam = 0.15, 1.0
    K = Sm.gaussian_kernel_matrix(s, s, ell)
    Ks = Sm.gaussian_kernel_matrix(ss, s, ell)
    A = np.linalg.solve(K + lam * np.eye(len(a)), np.eye(len(a)))
    mean = Ks @ A @ a
    resid = a - K @ A @ a
    df = float(np.trace(K @ A))
    sigma2 = float(resid @ resid / (len(a) - df))
    tau2 = sigma2 / lam
    var = tau2 * (1 - np.einsum("ij,jk,ik->i", Ks, A, Ks))
    return nest({"t": t, "a": a, "tt": tt, "fits": fits, "gp_mean": mean, "gp_sd": np.sqrt(np.clip(var, 0, None)),
                 "sigma": math.sqrt(sigma2), "ell_ms": ell * t.std(), "df": df})


def compute_wavelets():
    g = rng(1994)
    n = 1024
    out = {"n": n, "signals": {}}
    for name in ("blocks", "doppler", "heavisine", "bumps"):
        f = Sm.dj_function(name, n)
        y = f + g.standard_normal(n)
        v = Sm.wavelet_denoise(y, "visu")
        s_ = Sm.wavelet_denoise(y, "sure")
        sp = Sm.SmoothingSpline(np.arange(n) / n, y)
        # the spline smoother on 1,024 points: choose df by GCV over a coarse df grid via the eigenbasis
        d, U = np.linalg.eigh(sp.K)
        d[:2] = 0
        z = U.T @ y
        best = (np.inf, None, None)
        for lam in np.geomspace(1e-14, 1e-2, 61):
            sh = 1 / (1 + lam * d)
            fit = U @ (sh * z)
            dfv = sh.sum()
            gv = np.mean((y - fit) ** 2) / (1 - dfv / n) ** 2
            if gv < best[0]:
                best = (gv, fit, dfv)
        cf = Sm.dwt(f, Sm.D4, 7)
        out["signals"][name] = {"f": f, "y": y, "visu": v["fit"], "sure": s_["fit"], "spline": best[1],
                                "mse": {"noisy": float(np.mean((y - f) ** 2)), "visu": float(np.mean((v["fit"] - f) ** 2)),
                                        "sure": float(np.mean((s_["fit"] - f) ** 2)),
                                        "spline": float(np.mean((best[1] - f) ** 2))},
                                "spline_df": float(best[2]), "kept_visu": v["kept"], "kept_sure": s_["kept"],
                                "big_coefs": int(sum(np.sum(np.abs(c) > math.sqrt(2 * math.log(n))) for c in cf[1:])),
                                "coefs_y": [c for c in Sm.dwt(y, Sm.D4, 7)[1:]], "coefs_f": [c for c in cf[1:]],
                                "thresholds_sure": s_["thresholds"]}
    mx = {}
    for m in (10, 100, 1000, 10000, 100000):
        z = np.abs(g.standard_normal((200, m))).max(1)
        mx[m] = {"median": float(np.median(z)), "q90": float(np.quantile(z, 0.9)), "bound": math.sqrt(2 * math.log(m))}
    out["max_normals"] = mx
    return nest(out)


def compute_gam():
    d = museum.airquality()
    y = np.cbrt(d["ozone"])
    X = np.column_stack([d["temp"], d["wind"], d["solar"]])
    names = ["temp", "wind", "solar"]
    lams = [Sm.SmoothingSpline(X[:, j], y).lam_for_df(4.0) for j in range(3)]
    b = Sm.backfit(X, y, lams, iters=200)
    n = len(y)
    lin = np.column_stack([np.ones(n), X])
    bl, *_ = np.linalg.lstsq(lin, y, rcond=None)
    rl = y - lin @ bl
    ra = y - b["fit"]
    tss = np.sum((y - y.mean()) ** 2)
    comps = {}
    for j, nm in enumerate(names):
        o = np.argsort(X[:, j])
        comps[nm] = {"x": X[o, j], "f": b["f"][o, j], "partial": (ra + b["f"][:, j])[o], "lin": bl[j + 1] * (X[o, j] - X[:, j].mean())}
    # 10-fold CV of the additive model vs the linear one
    g = rng(1973)
    folds = np.array_split(g.permutation(n), 10)
    e_add, e_lin = [], []
    for te in folds:
        tr = np.setdiff1d(np.arange(n), te)
        # Re-establish the stated four-df component rule on training observations only.
        fold_lams = [Sm.SmoothingSpline(X[tr, j], y[tr]).lam_for_df(4.0) for j in range(3)]
        bt = Sm.backfit(X[tr], y[tr], fold_lams, iters=200)
        if bt["iterations"] == 200:
            raise RuntimeError("additive CV fit did not converge")
        pred = np.full(len(te), bt["alpha"])
        for j in range(3):
            o = np.argsort(X[tr, j])
            # Each fitted component is a natural cubic spline, including linear extrapolation.
            knots, inverse = np.unique(X[tr, j], return_inverse=True)
            comp = np.bincount(inverse, weights=bt["f"][:, j]) / np.bincount(inverse)
            Q, R = Sm._QR(knots)
            pred += Sm.natural_spline_eval(knots, comp, np.linalg.solve(R, Q.T @ comp), X[te, j])
        e_add.extend((y[te] - pred) ** 2)
        blt, *_ = np.linalg.lstsq(lin[tr], y[tr], rcond=None)
        e_lin.extend((y[te] - lin[te] @ blt) ** 2)
    return nest({"n": n, "names": names, "comps": comps, "r2_add": float(1 - ra @ ra / tss), "r2_lin": float(1 - rl @ rl / tss),
                 "iterations": b["iterations"], "cv_add": float(np.mean(e_add)), "cv_lin": float(np.mean(e_lin)),
                 "coef_lin": bl[1:], "cv_case_add": e_add, "cv_case_lin": e_lin,
                 "cv_paired_delta": float(np.mean(np.asarray(e_add)-e_lin)),
                 "cv_paired_se": float(np.std(np.asarray(e_add)-e_lin, ddof=1)/math.sqrt(n))})


def compute_rbc():
    """A pointwise 95% interval for f(x0) at the pointwise MSE-optimal bandwidth: the conventional interval ignores the
    bias that this bandwidth deliberately leaves in; the robust bias-corrected one (Calonico, Cattaneo & Farrell 2018)
    removes it and widens to account for the correction.  x0 = 4.3, the long eruptions' mode; n = 300."""
    g = rng(2018)
    n, R, x0 = 300, 2000, 4.3
    f0, f2 = float(GEYSER.pdf(x0)), float(GEYSER.d2(x0))
    h = Sm.pointwise_mse_h(f0, f2, n)
    hit = {"conv": 0, "rbc": 0, "under": 0}
    width = {"conv": [], "rbc": [], "under": []}
    est = []
    for _ in range(R):
        x = GEYSER.rvs(n, g)
        for k, (hh, rb) in (("conv", (h, False)), ("rbc", (h, True)), ("under", (h * n ** -0.1, False))):
            lo, hi, e = Sm.kde_ci(x, x0, hh, robust=rb)
            hit[k] += lo <= f0 <= hi
            width[k].append(hi - lo)
            if k == "conv":
                est.append(e)
    rows = [
        Row(29, r"KDE interval at the MSE-optimal $h$", r"$f(4.3)$, \ the long eruptions' mode, \ $n = 300$", "coverage", 0.95,
            hit["conv"] / R, R),
        Row(29, r"undersmoothed: \ $h \cdot n^{-1/10}$", r"$f(4.3)$, \ $n = 300$", "coverage", 0.95, hit["under"] / R, R),
        Row(29, r"robust bias-corrected", r"$f(4.3)$, \ $n = 300$", "coverage", 0.95, hit["rbc"] / R, R),
    ]
    save_rows(29, rows)
    return nest({"n": n, "R": R, "x0": x0, "f0": f0, "h": h, "coverage": {k: v / R for k, v in hit.items()},
                 "width": {k: float(np.mean(v)) for k, v in width.items()}, "mean_est": float(np.mean(est)),
                 "bias_theory": 0.5 * h * h * f2, "sd_est": float(np.std(est)),
                 "rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


def compute_shape():
    g = rng(1956)
    # isotonic regression of a noisy dose-response
    x = np.linspace(0, 1, 60)
    mu = 1 / (1 + np.exp(-10 * (x - 0.5)))
    y = mu + 0.15 * g.standard_normal(60)
    iso = Op.pava(y)["fit"]
    # Grenander at x0 = 1 for exponential data: n^{1/3} scaling vs the KDE's n^{2/5}
    rates = {}
    for n in (100, 1000, 10000):
        gr, kd = [], []
        for _ in range(300 if n < 10000 else 120):
            z = g.exponential(1, n)
            gr.append(Sm.grenander_at(Sm.grenander(z), [1.0])[0] - math.exp(-1))
            kd.append(Sm.kde(z, [1.0], 1.06 * n ** -0.2)[0] - math.exp(-1))
        rates[n] = {"gren_sd": float(np.std(gr)), "gren_scaled": float(np.std(gr) * n ** (1 / 3)), "kde_sd": float(np.std(kd)),
                    "kde_scaled": float(np.std(kd) * n ** 0.4), "gren_bias": float(np.mean(gr))}
    z = g.exponential(1, 200)
    G = Sm.grenander(z)
    tt = np.linspace(0, 4, 400)
    # Chernoff's constant: n^{1/3}(fhat - f) -> |f f' / 2|^{1/3} * 2Z, Z Chernoff with SD 0.52; so SD -> 2 * 0.52 * |f f'/2|^{1/3}
    f, fp = math.exp(-1), -math.exp(-1)
    chern = 2 * 0.52 * abs(f * fp / 2) ** (1 / 3)
    return nest({"x": x, "mu": mu, "y": y, "iso": iso, "rates": rates, "z": z, "gren_t": tt, "gren": Sm.grenander_at(G, tt),
                 "gren_knots": G["knots"], "gren_density": G["density"], "chernoff_sd": chern, "n_blocks": int(len(np.unique(np.round(iso, 10))))})


ITEMS = {
    "faithful": compute_faithful, "histmise": compute_histmise, "kdemise": compute_kdemise, "selectors": compute_selectors,
    "curse": compute_curse, "locpoly": compute_locpoly, "spline": compute_spline, "lamsim": compute_lamsim,
    "rkhs": compute_rkhs, "wavelets": compute_wavelets, "gam": compute_gam, "rbc": compute_rbc, "shape": compute_shape,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
