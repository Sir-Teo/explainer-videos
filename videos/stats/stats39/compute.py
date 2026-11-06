"""Precompute every number in Part 39 of *Statistics, Built* ("Space").

    OMP_NUM_THREADS=1 python -m videos.stats.stats39.compute            # everything missing (about half an hour)
    python -m videos.stats.stats39.compute --force board

Results are cached in ``.cache/stats39/<name>.json``.  Meuse's zinc and Snow's map are the Museum's; the pollution
field, its stations and the towns' disease counts are the World's; the rest are seeded simulations.

Items:
    meuse       log zinc: variograms (classical, robust), fitted models, ordinary and universal kriging, cross-validation
    world       the pollution field and stations: variogram, REML fits, universal kriging over the island vs the truth
    fields      three seeded Matern fields of different smoothness
    ident       infill asymptotics: estimates of range and variance scatter along a ridge; sigma^2/rho does not
    scale       exact vs Vecchia likelihoods and their cost; Vecchia on 100,000 locations
    gmrf        an SPDE lattice: sparsity, a sample, and the conditional mean from scattered observations
    areal       the World's towns: disease counts, Moran's I, raw SMRs vs BYM smoothing
    snow        Snow's deaths and pumps: nearest pumps, Ripley's L against CSR
    confound    spatial confounding: OLS vs a spatial random effect
    spacetime   separable vs Gneiting covariances; the World's daily readings
    bayesopt    Bayesian optimization of a one-dimensional function
    extra       Meuse's directional variograms and LOO z-scores; the World stations' effective sample size
    ridge_pred  kriging with covariances along and off the microergodic ridge
    blockcv     random vs spatial-block cross-validation of kriging on the World's stations
    board       Coverage Board rows
"""

from __future__ import annotations

import math
import time
from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import spatial as SP
from explainer.stats.world import World

CACHE = Cache("stats39")
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


def eff_reps(per_rep, nominal=0.9) -> int:
    v = np.var(np.asarray(per_rep, float), ddof=1) / len(per_rep)
    return int(round(nominal * (1 - nominal) / max(v, 1e-12)))


def circulant_field(nx, ny, h, sigma2, rho, nu, g):
    """A Matern field on an nx x ny grid with spacing h, by circulant embedding."""
    mx, my = 2 * nx, 2 * ny
    dx = np.minimum(np.arange(mx), mx - np.arange(mx)) * h
    dy = np.minimum(np.arange(my), my - np.arange(my)) * h
    D = np.sqrt(dx[None, :] ** 2 + dy[:, None] ** 2)
    C = SP.matern(D, sigma2, rho, nu)
    lam = np.clip(np.fft.fft2(C).real, 0, None)
    Z = g.standard_normal((my, mx)) + 1j * g.standard_normal((my, mx))
    return np.fft.fft2(np.sqrt(lam / (mx * my)) * Z).real[:ny, :nx]


def compute_meuse():
    m = museum.meuse()
    xy = np.column_stack([m["x"], m["y"]]) / 1000.0  # km
    z = np.log(m["zinc"])
    edges = np.linspace(0, 1.6, 16)
    v = SP.variogram(xy, z, edges)
    vr = SP.variogram(xy, z, edges, robust=True)
    fe = SP.fit_variogram(v["lag"], v["gamma"], v["n"], "exp")
    fs = SP.fit_variogram(v["lag"], v["gamma"], v["n"], "sph")
    gr = museum.meuse_grid()
    gxy = np.column_stack([gr["x"], gr["y"]]) / 1000.0
    cov = lambda d: fs["sill"] - SP.model_variogram(d, 0.0, fs["sill"], fs["range"], "sph")
    ok = SP.krige(xy, z, gxy, cov, nugget=fs["nugget"])
    sd_ = np.sqrt(m["dist"])
    # universal kriging with sqrt(distance to river): residual variogram
    X = np.column_stack([np.ones(len(z)), sd_])
    b = np.linalg.lstsq(X, z, rcond=None)[0]
    vres = SP.variogram(xy, z - X @ b, edges)
    fr = SP.fit_variogram(vres["lag"], vres["gamma"], vres["n"], "sph")
    covr = lambda d: fr["sill"] - SP.model_variogram(d, 0.0, fr["sill"], fr["range"], "sph")
    uk = SP.krige(xy, z, gxy, covr, sd_, np.sqrt(gr["dist"]), nugget=fr["nugget"])
    # leave-one-out cross-validation
    err = {"mean": [], "idw": [], "ok": [], "uk": []}
    for i in range(len(z)):
        k = np.arange(len(z)) != i
        d = np.sqrt(((xy[k] - xy[i]) ** 2).sum(1))
        err["mean"].append(z[i] - z[k].mean())
        wts = 1 / d ** 2
        err["idw"].append(z[i] - wts @ z[k] / wts.sum())
        err["ok"].append(z[i] - SP.krige(xy[k], z[k], xy[i:i + 1], cov, nugget=fs["nugget"])["pred"][0])
        err["uk"].append(z[i] - SP.krige(xy[k], z[k], xy[i:i + 1], covr, sd_[k], sd_[i:i + 1], nugget=fr["nugget"])["pred"][0])
    rmse = {k: float(np.sqrt(np.mean(np.square(v_)))) for k, v_ in err.items()}
    return nest({"x": xy[:, 0], "y": xy[:, 1], "z": z, "zinc": m["zinc"], "v": v, "vr": vr, "fe": fe, "fs": fs,
                 "vres": vres, "fr": fr, "gx": gxy[:, 0], "gy": gxy[:, 1], "ok": ok["pred"], "ok_sd": np.sqrt(ok["var"]),
                 "uk": uk["pred"], "uk_sd": np.sqrt(uk["var"]), "uk_beta": uk["beta"], "rmse": rmse, "n": len(z),
                 "river": museum.meuse_river()})


def compute_world():
    P = World().pollution
    xy = np.column_stack([P["sx"], P["sy"]])
    z, tr = P["annual"], P["s_traffic"]
    edges = np.linspace(0, 6, 16)
    X = np.column_stack([np.ones(300), tr])
    b = np.linalg.lstsq(X, z, rcond=None)[0]
    v = SP.variogram(xy, z - X @ b, edges)
    fits = {str(nu): SP.gp_fit(xy, z, tr, nu=nu, reml=True) for nu in (0.5, 1.5, 2.5)}
    ml = SP.gp_fit(xy, z, tr, nu=1.5, reml=False)
    f = fits["1.5"]
    # predict on a coarser land grid (0.2 units)
    gx, gy, land, field = P["gx"], P["gy"], P["land"], P["field"]
    sub = (np.arange(len(gy))[:, None] % 2 == 0) & (np.arange(len(gx))[None, :] % 2 == 0) & land
    Xg, Yg = np.meshgrid(gx, gy)
    pts = np.column_stack([Xg[sub], Yg[sub]])
    cov = lambda d: SP.matern(d, f["sigma2"], f["rho"], 1.5)
    k = SP.krige(xy, z, pts, cov, tr, P["traffic"][sub], nugget=f["tau2"])
    truth = field[sub]
    cover = float(np.mean(np.abs(truth - k["pred"]) <= 1.645 * np.sqrt(k["var"])))
    rmse_k = float(np.sqrt(np.mean((truth - k["pred"]) ** 2)))
    rmse_lm = float(np.sqrt(np.mean((truth - (b[0] + b[1] * P["traffic"][sub])) ** 2)))
    return nest({"sx": P["sx"], "sy": P["sy"], "z": z, "v": v, "fits": {k_: {kk: fv[kk] for kk in ("rho", "sigma2", "tau2", "beta", "ll")} for k_, fv in fits.items()},
                 "ml": {kk: ml[kk] for kk in ("rho", "sigma2", "tau2", "beta", "ll")},
                 "truth_params": {"sigma2": World.POLLUTION_SIGMA ** 2, "rho": World.POLLUTION_RANGE, "tau2": World.POLLUTION_NUGGET ** 2,
                                  "beta": [20.0, World.POLLUTION_TRAFFIC]},
                 "px": pts[:, 0], "py": pts[:, 1], "pred": k["pred"], "sd": np.sqrt(k["var"]), "truth": truth,
                 "cover": cover, "rmse_krige": rmse_k, "rmse_lm": rmse_lm, "lm_beta": b})


def compute_fields():
    out = {}
    for nu in (0.5, 1.5, 2.5):
        out[str(nu)] = circulant_field(60, 40, 0.1, 1.0, 1.0, nu, rng(3901))
    out["short"] = circulant_field(60, 40, 0.1, 1.0, 0.3, 1.5, rng(3901))
    return nest(out)


def compute_ident():
    g = rng(3902)
    n, reps = 300, 80
    rho0, s0 = 0.3, 1.0
    rhos, sig, micro = [], [], []
    for _ in range(reps):
        xy = g.random((n, 2))
        K = SP.matern(SP.dists(xy), s0, rho0, 0.5)
        z = np.linalg.cholesky(K + 1e-9 * np.eye(n)) @ g.standard_normal(n)
        f = SP.gp_fit(xy, z, None, nu=0.5, reml=False)
        rhos.append(f["rho"]), sig.append(f["sigma2"]), micro.append(f["sigma2"] / f["rho"])
    rhos, sig, micro = map(np.asarray, (rhos, sig, micro))
    cv = lambda a: float(np.std(a) / np.mean(a))
    return nest({"rho": rhos, "sigma2": sig, "micro": micro, "rho0": rho0, "s0": s0, "cv_rho": cv(rhos), "cv_sig": cv(sig),
                 "cv_micro": cv(micro), "micro0": s0 / rho0, "n": n, "reps": reps})


def compute_scale():
    g = rng(3903)
    times = {}
    for n in (250, 500, 1000, 2000):
        xy = g.random((n, 2))
        z = g.standard_normal(n)
        t0 = time.perf_counter()
        SP.exact_loglik(xy, z, 1.0, 0.2, 1.5, 0.1)
        times[str(n)] = time.perf_counter() - t0
    n = 2000
    xy = g.random((n, 2))
    K = SP.matern(SP.dists(xy), 1.0, 0.2, 1.5) + 0.1 * np.eye(n)
    z = np.linalg.cholesky(K) @ g.standard_normal(n)
    ex = SP.exact_loglik(xy, z, 1.0, 0.2, 1.5, 0.1)
    vc = {str(m): SP.vecchia_loglik_fast(xy, z, 1.0, 0.2, 1.5, 0.1, m) for m in (1, 3, 5, 10, 20, 30)}
    # profile over the range: exact vs Vecchia(10)
    grid = np.linspace(0.1, 0.35, 11)
    prof_ex = [SP.exact_loglik(xy, z, 1.0, r, 1.5, 0.1) for r in grid]
    prof_vc = [SP.vecchia_loglik_fast(xy, z, 1.0, r, 1.5, 0.1, 10) for r in grid]
    # 100,000 locations: the pollution field resampled at random land points
    P = World().pollution
    land = P["land"].ravel()
    Xg, Yg = np.meshgrid(P["gx"], P["gy"])
    idx = np.flatnonzero(land)
    pick = g.choice(idx, 100_000, replace=True)
    jit = g.uniform(-0.05, 0.05, (100_000, 2))
    big = np.column_stack([Xg.ravel()[pick], Yg.ravel()[pick]]) + jit
    zb = P["w"].ravel()[pick] + World.POLLUTION_NUGGET * g.standard_normal(100_000)
    t0 = time.perf_counter()
    llb = SP.vecchia_loglik_fast(big, zb, World.POLLUTION_SIGMA ** 2, World.POLLUTION_RANGE, 1.5, World.POLLUTION_NUGGET ** 2, 10)
    tb = time.perf_counter() - t0
    cubic = times["2000"] * (100_000 / 2000) ** 3
    return nest({"times": times, "exact": ex, "vecchia": vc, "grid": grid, "prof_ex": prof_ex, "prof_vc": prof_vc,
                 "big_ll": llb, "big_time": tb, "cubic_extrap_hours": cubic / 3600})


def compute_gmrf():
    nx, ny = 60, 40
    kappa = math.sqrt(8) / 8.0  # range of about 8 grid steps
    Q = SP.gmrf_precision(nx, ny, kappa, tau=1.0)
    g = rng(3904)
    u = SP.gmrf_sample(Q, g)
    u = u / u.std()
    Qs = Q / (1 / np.var(SP.gmrf_sample(Q, rng(1))))  # rough rescale not needed for the mean
    obs = np.sort(g.choice(nx * ny, 150, replace=False))
    y = u[obs] + 0.3 * g.standard_normal(150)
    var_u = float(np.var(SP.gmrf_sample(Q, rng(2))))
    mu = SP.gmrf_condition(Q * var_u, obs, y, 0.09)
    nnz = int(Q.nnz)
    return nest({"nx": nx, "ny": ny, "u": u.reshape(ny, nx), "obs": obs, "y": y, "mu": mu.reshape(ny, nx), "nnz": nnz,
                 "n": nx * ny, "dense": (nx * ny) ** 2, "rmse": float(np.sqrt(np.mean((mu - u) ** 2))),
                 "pattern": np.array(Q[:60, :60].toarray() != 0, int)})


def town_neighbours(xy, k=5):
    D = SP.dists(xy)
    np.fill_diagonal(D, np.inf)
    W = np.zeros_like(D)
    nn = np.argsort(D, 1)[:, :k]
    for i in range(len(xy)):
        W[i, nn[i]] = 1
    return np.maximum(W, W.T)


def compute_areal():
    w = World()
    t = w.towns
    P = w.pollution
    xy = t["xy"]
    pop = np.bincount(w.town, minlength=len(xy)).astype(float)
    # each town's pollution: the field at its centre
    ix = np.clip(np.round((xy[:, 0] + 5.5) / 0.1).astype(int), 0, len(P["gx"]) - 1)
    iy = np.clip(np.round((xy[:, 1] + 3.8) / 0.1).astype(int), 0, len(P["gy"]) - 1)
    pol = P["field"][iy, ix]
    g = rng(3905)
    rate = 0.002  # yearly cases per resident at average pollution
    log_rr = 0.06 * (pol - pol.mean()) + 0.1 * g.standard_normal(len(xy))
    E = pop * rate
    y = g.poisson(E * np.exp(log_rr))
    smr = y / E
    W = town_neighbours(xy)
    mi = SP.morans_i(np.log((y + 0.5) / E), W, 999, rng(3906))
    sm = SP.icar_smooth(y, E, W, tau_u=8.0, tau_v=50.0)
    true_rr = np.exp(log_rr)
    err = lambda est: float(np.sqrt(np.mean((np.log(est) - np.log(true_rr)) ** 2)))
    small = pop < np.percentile(pop, 25)
    return nest({"x": xy[:, 0], "y": xy[:, 1], "pop": pop, "E": E, "cases": y, "smr": smr, "rr_smooth": sm["rr"],
                 "true_rr": true_rr, "moran": mi, "err_smr": err(np.maximum(smr, 0.05)), "err_smooth": err(sm["rr"]),
                 "range_smr_small": [float(smr[small].min()), float(smr[small].max())],
                 "range_sm_small": [float(sm["rr"][small].min()), float(sm["rr"][small].max())],
                 "W": W, "pol": pol, "n_edges": int(W.sum() / 2)})


def compute_snow():
    s = museum.snow_map()
    d, p = s["deaths"], s["pumps"]
    D = SP.dists(d, p["xy"])
    nearest = np.argmin(D, 1)
    counts = np.bincount(nearest, minlength=len(p["label"]))
    broad = p["label"].index("Broad St")
    window = (float(d[:, 0].min()) - 0.5, float(d[:, 0].max()) + 0.5, float(d[:, 1].min()) - 0.5, float(d[:, 1].max()) + 0.5)
    r = np.linspace(0.1, 3.0, 30)
    k = SP.ripley_k(d, r, window)
    env = SP.csr_envelope(len(d), r, window, 199, rng(3907))
    dist_broad = D[:, broad]
    return nest({"deaths": d, "pumps": p["xy"], "labels": p["label"], "counts": counts, "broad": broad,
                 "share_broad": float(counts[broad] / len(d)), "r": r, "L": k["L"] - r, "lo": env["lo"], "hi": env["hi"],
                 "window": window, "median_dist_broad": float(np.median(dist_broad)), "n": len(d)})


def compute_confound():
    g = rng(3908)
    reps = 60
    est = {"ols": [], "spatial": []}
    for _ in range(reps):
        n = 250
        xy = g.random((n, 2))
        K = SP.matern(SP.dists(xy), 1.0, 0.3, 1.5)
        L = np.linalg.cholesky(K + 1e-9 * np.eye(n))
        a, b = L @ g.standard_normal(n), L @ g.standard_normal(n)
        x = a
        wsp = 0.8 * a + 0.6 * b  # an unmeasured spatial confounder, correlated with x
        y = 1.0 * x + 1.0 * wsp + 0.3 * g.standard_normal(n)
        X = np.column_stack([np.ones(n), x])
        est["ols"].append(np.linalg.lstsq(X, y, rcond=None)[0][1])
        est["spatial"].append(SP.gp_fit(xy, y, x, nu=1.5, reml=True)["beta"][1])
    # a case where the spatial effect is independent of x: both unbiased
    est2 = {"ols": [], "spatial": []}
    for _ in range(reps):
        n = 250
        xy = g.random((n, 2))
        K = SP.matern(SP.dists(xy), 1.0, 0.3, 1.5)
        L = np.linalg.cholesky(K + 1e-9 * np.eye(n))
        x, wsp = L @ g.standard_normal(n), L @ g.standard_normal(n)
        y = 1.0 * x + wsp + 0.3 * g.standard_normal(n)
        X = np.column_stack([np.ones(n), x])
        est2["ols"].append(np.linalg.lstsq(X, y, rcond=None)[0][1])
        est2["spatial"].append(SP.gp_fit(xy, y, x, nu=1.5, reml=True)["beta"][1])
    s = lambda v: {"mean": float(np.mean(v)), "sd": float(np.std(v))}
    return nest({"confounded": {k: s(v) for k, v in est.items()}, "independent": {k: s(v) for k, v in est2.items()},
                 "truth": 1.0, "ols_bias_theory": 0.8, "reps": reps})


def compute_spacetime():
    h = np.linspace(0, 3, 61)
    u = np.linspace(0, 3, 61)
    H, U = np.meshgrid(h, u)
    sep = SP.gneiting(H, U, beta=0.0)
    nonsep = SP.gneiting(H, U, beta=1.0)
    P = World().pollution
    daily = P["daily"]
    anom = daily - daily.mean(0, keepdims=True)
    station_mean = daily.mean(1)
    acf = [1.0] + [float(np.corrcoef(station_mean[:-k], station_mean[k:])[0, 1]) for k in range(1, 15)]
    # spatial correlation of daily anomalies against distance
    xy = np.column_stack([P["sx"], P["sy"]])
    D = SP.dists(xy)
    C = np.corrcoef(anom.T)
    iu = np.triu_indices(300, 1)
    bins = np.linspace(0, 8, 9)
    sc = [float(C[iu][(D[iu] >= a) & (D[iu] < b)].mean()) for a, b in zip(bins[:-1], bins[1:])]
    return nest({"h": h, "u": u, "sep": sep, "nonsep": nonsep, "acf": acf, "bins": bins, "space_corr": sc,
                 "weather": P["weather"], "share_weather": float(4 / (4 + 2.25))})


def compute_bayesopt():
    f = lambda x: np.sin(3 * x) + 0.3 * x ** 2 - 0.2 * x
    grid = np.linspace(-2, 2, 401)
    xs = list(np.array([-1.6, 0.1, 1.7]))
    steps = []
    for it in range(8):
        X = np.array(xs)[:, None]
        yv = f(np.array(xs))
        mu0 = yv.mean()
        cov = lambda d: SP.matern(d, 1.0, 0.6, 2.5)
        k = SP.krige(X, yv - mu0, grid[:, None], cov, nugget=1e-6, mean=0.0)
        mu, sd = k["pred"] + mu0, np.sqrt(k["var"])
        ei = SP.expected_improvement(mu, sd, yv.min())
        nxt = float(grid[np.argmax(ei)])
        steps.append({"x": list(xs), "y": list(yv), "mu": mu, "sd": sd, "ei": ei, "next": nxt})
        xs.append(nxt)
    true_min = float(grid[np.argmin(f(grid))])
    return nest({"grid": grid, "f": f(grid), "steps": steps, "true_min": true_min, "found": float(xs[int(np.argmin(f(np.array(xs))))]),
                 "f_min": float(f(grid).min())})


def compute_blockcv():
    """Random 10-fold CV vs spatial-block CV for kriging the World's stations, and the error at far-from-data sites."""
    P = World().pollution
    xy = np.column_stack([P["sx"], P["sy"]])
    z, tr = P["annual"], P["s_traffic"]
    f = SP.gp_fit(xy, z, tr, nu=1.5, reml=True)
    cov = lambda d: SP.matern(d, f["sigma2"], f["rho"], 1.5)
    g = rng(3910)

    def run(folds):
        err, zs = np.zeros(300), np.zeros(300)
        for k in np.unique(folds):
            te = folds == k
            kr = SP.krige(xy[~te], z[~te], xy[te], cov, tr[~te], tr[te], nugget=f["tau2"])
            err[te] = z[te] - kr["pred"]
            zs[te] = err[te] / np.sqrt(kr["var"] + f["tau2"])
        nn = np.array([np.min(np.sqrt(((xy[folds != folds[i]] - xy[i]) ** 2).sum(1))) for i in range(300)])
        return {"rmse": float(np.sqrt(np.mean(err ** 2))), "cover": float(np.mean(np.abs(zs) <= 1.645)), "nn": float(np.median(nn))}

    rand = run(g.permutation(np.arange(300) % 10))
    bx = np.digitize(xy[:, 0], np.quantile(xy[:, 0], [1 / 3, 2 / 3]))
    by = np.digitize(xy[:, 1], np.quantile(xy[:, 1], [1 / 3, 2 / 3]))
    block = run(bx * 3 + by)
    # the island's land nodes: distance to the nearest station
    Xg, Yg = np.meshgrid(P["gx"], P["gy"])
    land = np.column_stack([Xg[P["land"]], Yg[P["land"]]])[::7]
    from scipy.spatial import cKDTree
    dl = cKDTree(xy).query(land)[0]
    return nest({"random": rand, "block": block, "land_nn_median": float(np.median(dl)), "station_nn_median": float(np.median(cKDTree(xy).query(xy, 2)[0][:, 1]))})


def compute_extra():
    """Directional variograms of Meuse's log zinc; Meuse universal-kriging LOO z-scores; the World stations' n_eff."""
    m = museum.meuse()
    xy = np.column_stack([m["x"], m["y"]]) / 1000.0
    z = np.log(m["zinc"])
    sd_ = np.sqrt(m["dist"])
    X = np.column_stack([np.ones(len(z)), sd_])
    i, j = np.triu_indices(len(z), 1)
    dv = xy[j] - xy[i]
    d = np.sqrt((dv ** 2).sum(1))
    ang = np.degrees(np.arctan2(dv[:, 0], dv[:, 1])) % 180  # azimuth from north
    edges = np.linspace(0, 1.6, 11)
    out = {}
    for a in (0, 45, 90, 135):
        diff = np.minimum(np.abs(ang - a), 180 - np.abs(ang - a))
        k = diff <= 22.5
        lag, gam = [], []
        for lo, hi in zip(edges[:-1], edges[1:]):
            kk = k & (d >= lo) & (d < hi)
            if kk.sum() >= 20:
                lag.append(float(d[kk].mean()))
                gam.append(float(0.5 * np.mean((z[i][kk] - z[j][kk]) ** 2)))
        out[str(a)] = {"lag": lag, "gamma": gam}
    # universal kriging LOO z-scores with the residual spherical model
    b = np.linalg.lstsq(X, z, rcond=None)[0]
    vres = SP.variogram(xy, z - X @ b, np.linspace(0, 1.6, 16))
    fr = SP.fit_variogram(vres["lag"], vres["gamma"], vres["n"], "sph")
    covr = lambda h: fr["sill"] - SP.model_variogram(h, 0.0, fr["sill"], fr["range"], "sph")
    zs = []
    for t in range(len(z)):
        k = np.arange(len(z)) != t
        kr = SP.krige(xy[k], z[k], xy[t:t + 1], covr, sd_[k], sd_[t:t + 1], nugget=fr["nugget"])
        zs.append(float((z[t] - kr["pred"][0]) / np.sqrt(kr["var"][0] + fr["nugget"])))
    zs = np.asarray(zs)
    # World: effective sample size of the 300 stations' mean
    P = World().pollution
    sxy = np.column_stack([P["sx"], P["sy"]])
    C = SP.matern(SP.dists(sxy), World.POLLUTION_SIGMA ** 2, World.POLLUTION_RANGE, 1.5) + World.POLLUTION_NUGGET ** 2 * np.eye(300)
    var_mean = float(C.sum() / 300 ** 2)
    tot = World.POLLUTION_SIGMA ** 2 + World.POLLUTION_NUGGET ** 2
    return nest({"dir": out, "z": zs, "cover90": float(np.mean(np.abs(zs) <= 1.645)), "mean_z2": float(np.mean(zs ** 2)),
                 "n_eff": tot / var_mean, "se_naive": math.sqrt(tot / 300), "se_true": math.sqrt(var_mean)})


def compute_ridge_pred():
    """Kriging the World's field with covariances along and off Zhang's ridge (nu = 3/2: sigma^2 / rho^3 fixed)."""
    P = World().pollution
    xy = np.column_stack([P["sx"], P["sy"]])
    z, tr = P["annual"], P["s_traffic"]
    gx, gy, land, field = P["gx"], P["gy"], P["land"], P["field"]
    sub = (np.arange(len(gy))[:, None] % 2 == 0) & (np.arange(len(gx))[None, :] % 2 == 0) & land
    Xg, Yg = np.meshgrid(gx, gy)
    pts = np.column_stack([Xg[sub], Yg[sub]])
    truth = field[sub]
    s2, r0, t2 = World.POLLUTION_SIGMA ** 2, World.POLLUTION_RANGE, World.POLLUTION_NUGGET ** 2
    out = []
    for name, s, r in (("true", s2, r0), ("ridge: range x2, variance x8", 8 * s2, 2 * r0), ("ridge: range x0.7", s2 * 0.343, 0.7 * r0),
                       ("off: range x2 only", s2, 2 * r0), ("off: range x0.5 only", s2, 0.5 * r0)):
        cov = lambda h, s=s, r=r: SP.matern(h, s, r, 1.5)
        k = SP.krige(xy, z, pts, cov, tr, P["traffic"][sub], nugget=t2)
        out.append({"name": name, "sigma2": s, "rho": r, "rmse": float(np.sqrt(np.mean((truth - k["pred"]) ** 2))),
                    "cover": float(np.mean(np.abs(truth - k["pred"]) <= 1.645 * np.sqrt(k["var"]))),
                    "mean_sd": float(np.mean(np.sqrt(k["var"])))})
    return nest({"rows": out})


def board_field(g, n, nt, nu, rho, tau2=0.1):
    xy = g.random((n + nt, 2))
    x = xy[:, 0] + np.sin(3 * xy[:, 1])
    K = SP.matern(SP.dists(xy), 1.0, rho, nu)
    w = np.linalg.cholesky(K + 1e-9 * np.eye(n + nt)) @ g.standard_normal(n + nt)
    y = x + w + math.sqrt(tau2) * g.standard_normal(n + nt)
    return xy[:n], y[:n], x[:n], xy[n:], (w + x)[n:], x[n:]


def compute_board():
    g = rng(3909)
    reps = 250
    ct, cr, cm, bo, bg = [], [], [], [], []
    for _ in range(reps):
        xy, y, x, xt, ft, x_t = board_field(g, 200, 50, 2.5, 0.2)
        cov = lambda d: SP.matern(d, 1.0, 0.2, 2.5)
        k = SP.krige(xy, y, xt, cov, x, x_t, nugget=0.1)
        ct.append(np.mean(np.abs(ft - k["pred"]) <= 1.645 * np.sqrt(k["var"])))
        f = SP.gp_fit(xy, y, x, nu=2.5, reml=True)
        cv = lambda d: SP.matern(d, f["sigma2"], f["rho"], 2.5)
        k = SP.krige(xy, y, xt, cv, x, x_t, nugget=f["tau2"])
        cr.append(np.mean(np.abs(ft - k["pred"]) <= 1.645 * np.sqrt(k["var"])))
        f5 = SP.gp_fit(xy, y, x, nu=0.5, reml=True)
        cv = lambda d: SP.matern(d, f5["sigma2"], f5["rho"], 0.5)
        k = SP.krige(xy, y, xt, cv, x, x_t, nugget=f5["tau2"])
        cm.append(np.mean(np.abs(ft - k["pred"]) <= 1.645 * np.sqrt(k["var"])))
        X = np.column_stack([np.ones(200), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        se = math.sqrt(e @ e / 198 * np.linalg.inv(X.T @ X)[1, 1])
        bo.append(abs(b[1] - 1) <= 1.645 * se)
        bg.append(abs(f["beta"][1] - 1) <= 1.645 * math.sqrt(f["cov_beta"][1, 1]))
    rows = [
        Row(39, r"kriging 90\% PI, \ true covariance", r"Mat\'ern $\nu = 5/2$ fields, \ $n = 200$", "coverage", 0.9,
            float(np.mean(ct)), eff_reps(ct)),
        Row(39, r"kriging PI, \ REML plug-in", r"Mat\'ern $\nu = 5/2$ fields, \ $n = 200$", "coverage", 0.9,
            float(np.mean(cr)), eff_reps(cr)),
        Row(39, r"kriging PI, \ exponential fitted", r"Mat\'ern $\nu = 5/2$ fields, \ $n = 200$", "coverage", 0.9,
            float(np.mean(cm)), eff_reps(cm)),
        Row(39, r"OLS CI for a covariate", r"spatially correlated errors, \ $n = 200$", "coverage", 0.9,
            float(np.mean(bo)), reps),
        Row(39, r"GLS (REML) CI for the covariate", r"spatially correlated errors, \ $n = 200$", "coverage", 0.9,
            float(np.mean(bg)), reps),
    ]
    save_rows(39, rows)
    return nest({"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


ITEMS = {
    "meuse": compute_meuse, "world": compute_world, "fields": compute_fields, "ident": compute_ident,
    "scale": compute_scale, "gmrf": compute_gmrf, "areal": compute_areal, "snow": compute_snow,
    "confound": compute_confound, "blockcv": compute_blockcv, "extra": compute_extra, "ridge_pred": compute_ridge_pred, "spacetime": compute_spacetime, "bayesopt": compute_bayesopt, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
