"""Precompute every number in Part 32 of *Statistics, Built* ("Sparsity").

    python -m videos.stats.stats32.compute            # everything missing (a few minutes)
    python -m videos.stats.stats32.compute --force board

Results are cached in ``.cache/stats32/<name>.json``.  The diabetes data are the Museum's (Efron et al. 2004); the
phantom is Shepp and Logan's; the rest are seeded simulations.

Items:
    phantom     the Shepp--Logan phantom from 22 radial lines of Fourier samples: min-energy vs TV recovery
    lines       recovery error against the number of radial lines
    ridge       ridge on the diabetes data: the SVD shrinkage factors, the trace, effective df
    lars        LARS and the lasso path on the diabetes data, knot by knot, with the order of entry
    zoo         elastic net on correlated predictors; lasso / adaptive / MCP support recovery; a fused-lasso signal
    cv          the 64-term quadratic diabetes model: CV curve, lam_min, the one-SE rule; stability selection
    bayes       shrinkage profiles (soft, Laplace mean, horseshoe mean); Gibbs on a sparse normal-means problem
    cs          basis pursuit vs least norm on a spike train; the empirical phase transition and Donoho--Tanner's curve
    infer       naive post-lasso, debiased lasso, single and double selection: estimates and intervals
    mc          matrix completion by SoftImpute along a path of lambda
    board       Coverage Board rows: naive post-lasso vs debiased lasso; single vs double selection
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import optim as O
from explainer.stats.kit import sparse as SP

CACHE = Cache("stats32")
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


NICE = {"age": "age", "sex": "sex", "bmi": "BMI", "bp": "blood pressure", "tc": "total cholesterol", "ldl": "LDL",
        "hdl": "HDL", "tch": "TC/HDL", "ltg": "log triglycerides", "glu": "glucose"}


def diabetes_std():
    X, y, names = museum.diabetes()
    Xs, ys, mu, sd, ybar = SP.standardize(X, y)
    return Xs, ys, names


def quadratic(X, names):
    """The LARS paper's 64-term model: 10 main effects, 45 interactions, 9 squares (no square for sex), formed from the
    standardized main effects so that products are not proxies for the main effects."""
    X = (X - X.mean(0)) / X.std(0)
    cols, labs = [X[:, j] for j in range(10)], list(names)
    for i in range(10):
        for j in range(i + 1, 10):
            cols.append(X[:, i] * X[:, j])
            labs.append(f"{names[i]}:{names[j]}")
    for i in range(10):
        if names[i] != "sex":
            cols.append(X[:, i] ** 2)
            labs.append(f"{names[i]}^2")
    return np.column_stack(cols), labs


N_PH = 128


def compute_phantom():
    img = SP.shepp_logan(N_PH)
    mask = SP.radial_mask(N_PH, 22)
    F = np.fft.fft2(img, norm="ortho")
    y = np.where(mask, F, 0)
    me = SP.min_energy(y, mask)
    rec = SP.tv_recover(y, mask, iters=4000, record=(20, 100, 400, 1500, 4000))
    err = lambda a: float(np.linalg.norm(a - img) / np.linalg.norm(img))  # noqa: E731
    shifted = np.fft.fftshift(mask)
    return nest({"N": N_PH, "truth": img, "mask": shifted.astype(int), "fraction": float(mask.mean()), "min_energy": me,
                 "tv": rec["x"], "snaps": {k: v for k, v in rec["snaps"].items()},
                 "err_me": err(me), "err_tv": err(rec["x"]), "err_snaps": {k: err(v) for k, v in rec["snaps"].items()},
                 "tv_truth": SP.tv(img), "tv_me": SP.tv(me), "tv_rec": SP.tv(rec["x"]),
                 "nonzero_grad": float(np.mean(np.abs(np.diff(img, axis=1)) > 1e-9))})


def compute_lines():
    img = SP.shepp_logan(N_PH)
    F = np.fft.fft2(img, norm="ortho")
    out = []
    for L in (4, 8, 12, 16, 22, 30):
        mask = SP.radial_mask(N_PH, L)
        y = np.where(mask, F, 0)
        me = SP.min_energy(y, mask)
        rec = SP.tv_recover(y, mask, iters=3000)["x"]
        e = lambda a: float(np.linalg.norm(a - img) / np.linalg.norm(img))  # noqa: E731
        out.append({"lines": L, "fraction": float(mask.mean()), "err_me": e(me), "err_tv": e(rec),
                    "rec": rec if L in (8, 12) else None})
    return nest({"rows": out})


def compute_ridge():
    Xs, ys, names = diabetes_std()
    n = len(ys)
    lams = np.logspace(-2, 5, 120)
    r = SP.ridge_svd(Xs, ys, lams)
    ols = np.linalg.lstsq(Xs, ys, rcond=None)[0]
    # the prior view: lam = sigma^2 / tau^2
    resid = ys - Xs @ ols
    s2 = float(resid @ resid / (n - 11))
    return nest({"names": [NICE[v] for v in names], "lams": lams, "coefs": r["coefs"], "df": r["df"], "d": r["d"],
                 "ols": ols, "sigma2": s2, "shrink_at": {"10": (r["d"] ** 2 / (r["d"] ** 2 + 10.0)),
                                                         "1000": (r["d"] ** 2 / (r["d"] ** 2 + 1000.0))},
                 "cond": float(r["d"][0] / r["d"][-1]), "corr_tc_ldl": float(np.corrcoef(Xs[:, 4], Xs[:, 5])[0, 1])})


def compute_lars():
    Xs, ys, names = diabetes_std()
    n = len(ys)
    Xn = Xs / math.sqrt(n)
    La = SP.lars(Xn, ys, lasso=True)
    Lr = SP.lars(Xn, ys, lasso=False)
    B = np.asarray(La["coefs"])
    l1 = np.abs(B).sum(1)
    # unstandardized-to-'per SD' coefficients for display: b on unit-norm columns -> per SD of x is b / sqrt(n)
    return nest({"names": [NICE[v] for v in names], "lams": La["lams"], "coefs": B, "l1": l1, "s": l1 / l1[-1],
                 "actions": La["actions"], "active": La["active"], "lars_coefs": Lr["coefs"],
                 "lars_s": np.abs(np.asarray(Lr["coefs"])).sum(1) / np.abs(np.asarray(Lr["coefs"])).sum(1)[-1],
                 "lars_actions": Lr["actions"], "ols": B[-1]})


def compute_zoo():
    g = rng(2005)
    # (1) three nearly identical predictors: the lasso picks one, the elastic net shares
    n = 100
    z = g.standard_normal(n)
    X = np.column_stack([z + 0.2 * g.standard_normal(n) for _ in range(3)] + [g.standard_normal(n) for _ in range(3)])
    y = 2.0 * z + g.standard_normal(n)
    Xs, ys, *_ = SP.standardize(X, y)
    lm = SP.lam_max(Xs, ys)
    lams = lm * np.logspace(0, -2.5, 60)
    las = SP.lasso_path(Xs, ys, lams=lams)["coefs"]
    en = SP.lasso_path(Xs, ys, lams=lams / 0.5, alpha=0.5)["coefs"]
    # (2) support recovery across penalties: n = 100, p = 200, s = 8, correlated design
    reps, n2, p2, s2 = 200, 100, 200, 8
    rho = 0.5
    C = rho ** np.abs(np.subtract.outer(np.arange(p2), np.arange(p2)))
    Lc = np.linalg.cholesky(C)
    beta = np.zeros(p2)
    supp = np.arange(0, 80, 10)
    beta[supp] = [1.0, -1.0, 0.8, -0.8, 0.6, -0.6, 0.5, -0.5]
    stats_ = {k: {"tp": 0.0, "fp": 0.0, "exact": 0, "err": 0.0} for k in ("lasso", "adaptive", "mcp", "scad")}
    lam = 1.1 * math.sqrt(2 * math.log(p2) / n2)
    for _ in range(reps):
        Xr = g.standard_normal((n2, p2)) @ Lc.T
        yr = Xr @ beta + g.standard_normal(n2)
        Xr, yr, *_ = SP.standardize(Xr, yr)
        bt = beta * Xr.std(0) if False else beta
        b_l = SP.lasso_cd(Xr, yr, lam)
        b_init = SP.lasso_cd(Xr, yr, lam / 2)
        w = 1.0 / np.maximum(np.abs(b_init), 1e-8)
        w = np.where(np.abs(b_init) > 0, w, np.inf)
        b_a = SP.lasso_cd(Xr, yr, lam / 4, weights=w * np.mean(np.abs(b_init[b_init != 0])) if np.any(b_init) else w)
        b_m = SP.ncv_cd(Xr, yr, lam, "mcp", b0=b_l)
        b_s = SP.ncv_cd(Xr, yr, lam, "scad", b0=b_l)
        for k, b in (("lasso", b_l), ("adaptive", b_a), ("mcp", b_m), ("scad", b_s)):
            sel = np.flatnonzero(b)
            tp = len(np.intersect1d(sel, supp))
            stats_[k]["tp"] += tp / reps
            stats_[k]["fp"] += (len(sel) - tp) / reps
            stats_[k]["exact"] += int(tp == s2 and len(sel) == s2)
            stats_[k]["err"] += float(np.sum((b - bt) ** 2)) / reps
    for k in stats_:
        stats_[k]["exact"] /= reps
    # (3) fused lasso on a piecewise-constant signal
    m = 200
    truth = np.zeros(m)
    truth[40:80], truth[110:120], truth[150:190] = 2.0, -1.5, 1.0
    yy = truth + 0.6 * g.standard_normal(m)
    fl = O.fused_lasso_admm(yy, 3.0, rho=1.0, iters=3000)
    fit = np.asarray(fl["b"] if isinstance(fl, dict) and "b" in fl else fl["x"])
    return nest({"lams": lams, "lasso": las, "enet": en, "corr": float(np.corrcoef(X[:, 0], X[:, 1])[0, 1]),
                 "support": stats_, "lam_support": lam, "reps": reps, "fused": {"y": yy, "truth": truth, "fit": fit,
                 "rmse_fit": float(np.sqrt(np.mean((fit - truth) ** 2))),
                 "rmse_raw": float(np.sqrt(np.mean((yy - truth) ** 2)))}})


def compute_cv():
    X, y, names = museum.diabetes()
    Q, labs = quadratic(X, names)
    Qs, ys, *_ = SP.standardize(Q, y)
    lm = SP.lam_max(Qs, ys)
    lams = lm * np.logspace(0, -2.5, 60)
    cv = SP.cv_lasso(Qs, ys, lams, K=10, rng=rng(1))
    path = SP.lasso_path(Qs, ys, lams=lams)
    nz_min = int(np.sum(path["coefs"][cv["i_min"]] != 0))
    nz_1se = int(np.sum(path["coefs"][cv["i_1se"]] != 0))
    sel_1se = [labs[j] for j in np.flatnonzero(path["coefs"][cv["i_1se"]])]
    stab = SP.stability_selection(Q, y, lams[:40:3], B=60, rng=rng(2))
    top = np.argsort(-stab.max(0))[:12]
    return nest({"labels": labs, "lams": lams, "cv": cv["cv"], "se": cv["se"], "i_min": cv["i_min"], "i_1se": cv["i_1se"],
                 "lam_min": cv["lam_min"], "lam_1se": cv["lam_1se"], "nz_min": nz_min, "nz_1se": nz_1se,
                 "sel_1se": sel_1se, "df": path["df"], "stab_lams": lams[:40:3], "stab": stab[:, top],
                 "stab_labels": [labs[j] for j in top], "stab_max": stab.max(0)[top], "n_stable": int(np.sum(stab.max(0) >= 0.8)),
                 "stable": [labs[j] for j in np.flatnonzero(stab.max(0) >= 0.8)]})


def compute_bayes():
    ys = np.linspace(-6, 6, 241)
    lam = 1.0
    prof = {"y": ys, "soft": SP.soft(ys, lam), "hard": SP.hard(ys, math.sqrt(2) * lam),
            "laplace_mean": SP.laplace_posterior_mean(ys, lam), "horseshoe": SP.horseshoe_posterior_mean(ys, 0.1),
            "ridge": ys / (1 + 1.0)}
    g = rng(2010)
    p = 200
    theta = np.zeros(p)
    theta[:10] = 5.0
    y = theta + g.standard_normal(p)
    hs = SP.horseshoe_gibbs(y, iters=6000, burn=1000, rng=g)
    bl = SP.bayes_lasso_gibbs(y, 1.0, iters=6000, burn=1000, rng=g)
    lu = math.sqrt(2 * math.log(p))
    st = SP.soft(y, lu)
    mse = lambda a: float(np.sum((a - theta) ** 2))  # noqa: E731
    return nest({"profile": prof, "y": y, "theta": theta, "hs": hs["mean"], "bl": bl["mean"], "soft": st, "lam_u": lu,
                 "tau_mean": float(np.mean(hs["tau"])), "sse": {"mle": mse(y), "soft": mse(st), "bayes_lasso": mse(bl["mean"]),
                                                               "horseshoe": mse(hs["mean"])},
                 "bl_min_abs": float(np.min(np.abs(bl["mean"]))), "hs_null_mean": float(np.mean(np.abs(hs["mean"][10:])))})


def compute_cs():
    g = rng(2006)
    p, n, s = 200, 60, 10
    x = np.zeros(p)
    x[g.choice(p, s, replace=False)] = g.choice([-1.0, 1.0], s) * (1 + g.random(s))
    A = g.standard_normal((n, p)) / math.sqrt(n)
    yv = A @ x
    bp = SP.basis_pursuit(A, yv)
    ln = np.linalg.pinv(A) @ yv
    deltas = np.round(np.linspace(0.1, 0.9, 9), 2)
    rhos = np.round(np.linspace(0.05, 0.95, 19), 3)
    grid = SP.phase_grid(100, deltas, rhos, 20, g)
    dd = np.linspace(0.02, 0.98, 60)
    return nest({"p": p, "n": n, "s": s, "x": x, "bp": bp, "ln": ln, "err_bp": float(np.max(np.abs(bp - x))),
                 "err_ln": float(np.linalg.norm(ln - x) / np.linalg.norm(x)), "deltas": deltas, "rhos": rhos,
                 "grid": grid, "curve_d": dd, "curve_r": SP.phase_curve(dd), "rho_half": float(SP.phase_curve([0.5])[0])})


def _sim_lasso(g, n, p, beta):
    X = g.standard_normal((n, p))
    y = X @ beta + g.standard_normal(n)
    return X - X.mean(0), y - y.mean()


def compute_infer():
    """One illustrative data set for the inference chapter."""
    g = rng(2014)
    n, p = 100, 200
    beta = np.zeros(p)
    beta[:6] = [1.0, 1.0, 0.5, 0.5, 0.25, 0.25]
    X, y = _sim_lasso(g, n, p, beta)
    lam = math.sqrt(2 * math.log(p) / n)
    b = SP.lasso_cd(X, y, lam)
    sel = np.flatnonzero(b)
    naive = SP.ols_ci(X, y, sel)
    deb = [SP.debiased_lasso(X, y, j, lam) for j in range(8)]
    return nest({"beta": beta[:8], "lam": lam, "lasso": b[:8], "selected": sel, "naive": naive, "deb": deb})


def compute_board():
    g = rng(2024)
    reps = 1000
    n, p = 100, 200
    beta = np.zeros(p)
    beta[:6] = [1.0, 1.0, 0.5, 0.5, 0.25, 0.25]
    lam = math.sqrt(2 * math.log(p) / n)  # the noise level sigma = 1 is known to the analyst
    j, j0 = 4, 50  # a weak coefficient (0.25) and a null one
    pooled_hit, pooled_n, fp_hit, fp_n = 0, 0, 0, 0
    naive_cov_sel, naive_sel, naive_w = 0, 0, 0.0
    naive_b, deb_b, deb0_b = [], [], []
    deb_cov, deb0_cov, deb_w = 0, 0, 0.0
    for _ in range(reps):
        X, y = _sim_lasso(g, n, p, beta)
        b = SP.lasso_cd(X, y, lam)
        sel = np.flatnonzero(b)
        if len(sel):
            r = SP.ols_ci(X, y, sel)
            hit = (r["lo"] <= beta[sel]) & (beta[sel] <= r["hi"])
            pooled_hit += int(hit.sum())
            pooled_n += len(sel)
            null = beta[sel] == 0
            fp_hit += int(hit[null].sum())
            fp_n += int(null.sum())
            if j in sel:
                k = int(np.flatnonzero(sel == j)[0])
                naive_sel += 1
                naive_cov_sel += bool(hit[k])
                naive_w += r["hi"][k] - r["lo"][k]
                naive_b.append(r["b"][k])
        d = SP.debiased_lasso(X, y, j, lam)
        deb_cov += d["lo"] <= beta[j] <= d["hi"]
        deb_w += d["hi"] - d["lo"]
        deb_b.append(d["b"])
        d0 = SP.debiased_lasso(X, y, j0, lam)
        deb0_cov += d0["lo"] <= 0.0 <= d0["hi"]
        deb0_b.append(d0["b"])
    # treatment effects: single vs double selection (Belloni, Chernozhukov & Hansen 2014)
    reps2 = 1000
    n2, p2 = 100, 100
    alpha = 0.5
    gam = np.zeros(p2)
    gam[:5] = 0.6
    bet = np.zeros(p2)
    bet[:5] = 0.2
    lam2 = 1.1 * math.sqrt(2 * math.log(p2) / n2)  # BCH's plug-in level with the noise SD (1) known
    ss_cov, ds_cov, ss_b, ds_b, ss_k, ds_k = 0, 0, [], [], [], []
    for _ in range(reps2):
        X = g.standard_normal((n2, p2))
        d_ = X @ gam + g.standard_normal(n2)
        y_ = alpha * d_ + X @ bet + g.standard_normal(n2)
        s1 = SP.single_selection(y_, d_, X, lam2)
        s2 = SP.double_selection(y_, d_, X, lam2, lam2)
        ss_cov += s1["lo"] <= alpha <= s1["hi"]
        ds_cov += s2["lo"] <= alpha <= s2["hi"]
        ss_b.append(s1["b"])
        ds_b.append(s2["b"])
        ss_k.append(s1["n_selected"])
        ds_k.append(s2["n_selected"])
    rows = [
        Row(32, r"naive post-lasso CIs, \ every selected $x_j$", rf"$n = {n}$, $p = {p}$, \ 6 true effects", "coverage",
            0.95, pooled_hit / pooled_n, pooled_n),
        Row(32, r"debiased lasso CI", rf"$n = {n}$, $p = {p}$, \ $\beta_j = 0.25$", "coverage", 0.95, deb_cov / reps, reps),
        Row(32, r"debiased lasso CI", rf"$n = {n}$, $p = {p}$, \ $\beta_j = 0$", "coverage", 0.95, deb0_cov / reps, reps),
        Row(32, r"single selection, \ treatment effect", rf"$n = {n2}$, $p = {p2}$, \ 5 confounders", "coverage", 0.95,
            ss_cov / reps2, reps2),
        Row(32, r"double selection, \ treatment effect", rf"$n = {n2}$, $p = {p2}$, \ 5 confounders", "coverage", 0.95,
            ds_cov / reps2, reps2),
    ]
    save_rows(32, rows)
    return nest({"reps": reps, "lam": lam, "j": j, "beta_j": beta[j], "pooled": pooled_hit / pooled_n, "pooled_n": pooled_n,
                 "per_rep_selected": pooled_n / reps, "fp_cov": fp_hit / max(fp_n, 1), "fp_n": fp_n,
                 "naive_sel": naive_sel, "naive_cov_sel": naive_cov_sel / max(naive_sel, 1),
                 "naive_width": naive_w / max(naive_sel, 1), "naive_mean": float(np.mean(naive_b)),
                 "deb_cov": deb_cov / reps, "deb_width": deb_w / reps, "deb_mean": float(np.mean(deb_b)), "deb0_cov": deb0_cov / reps,
                 "deb_draws": deb_b, "naive_draws": naive_b, "deb0_draws": deb0_b,
                 "ss_cov": ss_cov / reps2, "ds_cov": ds_cov / reps2, "ss_mean": float(np.mean(ss_b)), "ds_mean": float(np.mean(ds_b)),
                 "ss_sd": float(np.std(ss_b)), "ds_sd": float(np.std(ds_b)), "ss_k": float(np.mean(ss_k)), "ds_k": float(np.mean(ds_k)),
                 "alpha": alpha, "rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


def compute_mc():
    g = rng(2009)
    m, k, r = 120, 90, 4
    U, V = g.standard_normal((m, r)), g.standard_normal((k, r))
    M = U @ V.T
    noisy = M + 0.5 * g.standard_normal(M.shape)
    obs = g.random(M.shape) < 0.3
    lams = np.array([60.0, 40, 25, 15, 10, 6, 3, 1])
    out, Z = [], None
    for lam in lams:
        res = SP.soft_impute(noisy, obs, lam, iters=500, Z0=Z)
        Z = res["Z"]
        out.append({"lam": float(lam), "rank": res["rank"],
                    "test": float(np.linalg.norm((Z - M)[~obs]) / np.linalg.norm(M[~obs])),
                    "train": float(np.linalg.norm((Z - noisy)[obs]) / np.linalg.norm(noisy[obs]))})
    best = min(out, key=lambda o: o["test"])
    res = SP.soft_impute(noisy, obs, best["lam"], iters=500)
    sv = np.linalg.svd(M, compute_uv=False)[:10]
    return nest({"m": m, "k": k, "r": r, "frac": float(obs.mean()), "path": out, "best": best,
                 "truth_block": M[:24, :18], "obs_block": np.where(obs, noisy, np.nan)[:24, :18],
                 "fit_block": res["Z"][:24, :18], "sv_truth": sv, "sv_fit": res["d"][:10]})


ITEMS = {
    "phantom": compute_phantom, "lines": compute_lines, "ridge": compute_ridge, "lars": compute_lars, "zoo": compute_zoo,
    "cv": compute_cv, "bayes": compute_bayes, "cs": compute_cs, "infer": compute_infer, "mc": compute_mc,
    "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
