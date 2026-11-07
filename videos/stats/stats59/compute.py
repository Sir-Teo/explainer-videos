"""Precompute every number in Part 59 of *Statistics, Built* ("High-Dimensional Asymptotics").

    OMP_NUM_THREADS=1 python -m videos.stats.stats59.compute            # everything missing (several minutes)
    python -m videos.stats.stats59.compute --force board

Results are cached in ``.cache/stats59/<name>.json``.  The Wisconsin breast cancer design is the Museum's; everything
else is exact arithmetic (quadrature, root finding) or a seeded simulation.

Items:
    hook      one logistic fit at n = 2,000, p = 400: estimated against true coefficients, and the Sur-Candes slope
    lrt       the LRT for null coefficients at kappa = 0.2: classical against rescaled p-values
    table     the Sur-Candes solution (alpha, sigma, lambda, factor) by kappa and signal strength; the MLE's existence
    mp        sample-covariance eigenvalues against the Marchenko-Pastur law
    free      a Wigner matrix plus a +-1 diagonal against the free convolution
    ridge     exact ridge risk by penalty, and ridgeless double descent, against simulation
    robust    OLS against LAD in high dimensions with Laplace errors
    amp       AMP iterates against state evolution, the cobweb, and the Donoho-Tanner curve
    bayes     Bayes-optimal AMP (the replica prediction) against the lasso, by undersampling ratio
    rf        random-features ridge regression: test error by the number of features
    real      the breast cancer design with simulated logistic outcomes: inflation on a real design
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
from . import checked as M

CACHE = Cache("stats59")
load = CACHE.load

KAPPA, GAMMA2 = 0.2, 5.0


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


def _design_beta(n: int, p: int, r: np.random.Generator):
    """Sur & Candes's setting: X with i.i.d. N(0, 1/n) entries, an eighth of the coefficients +b, an eighth -b, the rest
    zero, b chosen so that Var(x'beta) = gamma^2 = 5."""
    beta = np.zeros(p)
    k = p // 8
    beta[:k], beta[k:2 * k] = 1.0, -1.0
    beta *= math.sqrt(GAMMA2 * n / np.sum(beta ** 2))
    X = r.standard_normal((n, p)) / math.sqrt(n)
    return X, beta


def compute_hook():
    r = rng(5901)
    n, p = 2000, 400
    X, beta = _design_beta(n, p, r)
    y = (r.random(n) < 1 / (1 + np.exp(-(X @ beta)))).astype(float)
    b, _, ok = M.logistic_mle(X, y)
    if not ok:raise RuntimeError("hook finite MLE failed")
    sc = M.sur_candes(KAPPA, math.sqrt(GAMMA2))
    nz = beta != 0
    slope = float(np.sum(b[nz] * beta[nz]) / np.sum(beta[nz] ** 2))
    # classical standard errors from the inverse Fisher information, against the spread of the null coordinates
    p_hat = 1 / (1 + np.exp(-(X @ b)))
    H = (X * (p_hat * (1 - p_hat))[:, None]).T @ X
    se_classical = np.sqrt(np.diag(np.linalg.inv(H)))
    return {"n": n, "p": p, "beta": beta, "beta_hat": b, "ok": ok, "slope": slope, "alpha": sc["alpha"], "sigma": sc["sigma"],
            "lam": sc["lam"], "factor": sc["factor"], "sd_null": float(np.std(b[~nz])), "se_classical_null": float(np.mean(se_classical[~nz])),
            "b_val": float(beta[0])}


def compute_lrt():
    r = rng(5902)
    n, p = 1000, 200
    reps = 500
    llr = []
    failures = 0
    for _ in range(reps):
        X, beta = _design_beta(n, p, r)
        y = (r.random(n) < 1 / (1 + np.exp(-(X @ beta)))).astype(float)
        out = M.lrt_one(X, y, p - 1)  # the last coefficient is a null
        if out["ok"]:
            llr.append(out["llr2"])
        else:
            failures += 1
    llr = np.asarray(llr)
    sc = M.sur_candes(p / n, math.sqrt(GAMMA2))
    p_classic = stats.chi2.sf(llr, 1)
    p_rescaled = stats.chi2.sf(llr / sc["factor"], 1)
    return {"n": n, "p": p, "reps": len(llr), "attempts": reps, "failed_finite_fits": failures,
            "size_classic_mcse": math.sqrt(np.mean(p_classic<.05)*(1-np.mean(p_classic<.05))/len(llr)),
            "size_rescaled_mcse": math.sqrt(np.mean(p_rescaled<.05)*(1-np.mean(p_rescaled<.05))/len(llr)), "factor": sc["factor"], "llr": llr, "p_classic": p_classic, "p_rescaled": p_rescaled,
            "size_classic": float(np.mean(p_classic < 0.05)), "size_rescaled": float(np.mean(p_rescaled < 0.05)),
            "size_classic_01": float(np.mean(p_classic < 0.01)), "size_rescaled_01": float(np.mean(p_rescaled < 0.01)),
            "mean_llr": float(np.mean(llr))}


def compute_table():
    rows = []
    for g2 in (1.0, 5.0):
        prev = None
        for k in (0.05, 0.1, 0.15, 0.2, 0.25, 0.3):
            s = M.sur_candes(k, math.sqrt(g2), x0=prev)
            if s["ok"]:
                prev = (s["alpha"], s["sigma"], s["lam"])
            rows.append({"gamma2": g2, "kappa": k, **s})
    null = [{"kappa": k, **M.sur_candes(k, 0.0)} for k in (0.05, 0.1, 0.2, 0.3, 0.4)]
    exist = [{"gamma": g, "kappa_max": M.mle_exists_boundary(g)} for g in (0.0, 1.0, math.sqrt(5), 4.0, 8.0)]
    return {"rows": rows, "null": null, "exist": exist}


def compute_mp():
    r = rng(5903)
    n, p = 2000, 1000
    X = r.standard_normal((n, p))
    ev = np.linalg.eigvalsh(X.T @ X / n)
    xs = np.linspace(0.0, 3.2, 161)
    return {"n": n, "p": p, "gamma": p / n, "ev": ev, "xs": xs, "dens": M.mp_density(xs, p / n), "min": float(ev.min()), "max": float(ev.max()),
            "edges": [(1 - math.sqrt(p / n)) ** 2, (1 + math.sqrt(p / n)) ** 2]}


def compute_free():
    r = rng(5904)
    N = 1500
    s2 = 0.25
    G = r.standard_normal((N, N))
    W = (G + G.T) / math.sqrt(2 * N) * math.sqrt(s2)
    D = np.diag(r.choice([-1.0, 1.0], N))
    ev = np.linalg.eigvalsh(W + D)
    xs = np.linspace(-2.2, 2.2, 221)
    audit = M.free_semicircle_plus_pm1(xs, s2, eta=2e-3, return_audit=True)
    dens = audit["density"]
    semicircle = lambda x: np.sqrt(np.maximum(4*s2-x*x,0))/(2*math.pi*s2)
    naive = .5*(semicircle(xs-1)+semicircle(xs+1))
    return {"N": N, "s2": s2, "ev": ev, "xs": xs, "dens": dens, "naive": naive, "stieltjes_audit": audit, "naive_scope": "ordinary convolution of the actual semicircle and +/-1 laws"}


def compute_ridge():
    r = rng(5905)
    snr = 4.0
    lams = np.geomspace(0.01, 3.0, 40)
    out = {"snr": snr, "lams": lams}
    for g in (0.5, 2.0):
        th = M.ridge_risk(lams, g, snr)
        sim_l = lams[::6]
        sim = M.ridge_sim(400, g, snr, sim_l, 20, r, return_draws=True)
        out[str(g)] = {"bias": th["bias"], "var": th["var"], "risk": th["risk"], "sim_l": sim_l, "sim": sim["mean"], "sim_audit": sim, "opt_lam": g / snr,
                       "opt_risk": M.optimal_ridge_risk(g, snr)}
    gs = np.r_[np.linspace(0.05, 0.95, 19), np.linspace(1.05, 4.0, 30)]
    out["gammas"] = gs
    out["ridgeless"] = M.ridgeless_risk(gs, snr)
    out["opt_curve"] = [M.optimal_ridge_risk(g, snr) for g in gs]
    sim_g = [0.25, 0.5, 0.75, 0.9, 1.1, 1.5, 2.0, 3.0, 4.0]
    out["sim_g"] = sim_g
    out["sim_ridgeless_audit"] = [M.ridge_sim(300,g,snr,[0.],12,r,return_draws=True) for g in sim_g]
    out["sim_ridgeless"] = [float(d["mean"][0]) for d in out["sim_ridgeless_audit"]]
    out["null_risk"] = snr  # predicting zero: E(x'beta)^2 = ||beta||^2
    return out


def compute_robust():
    r = rng(5906)
    kappas = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    n = 400
    res = []
    for k in kappas:
        p = int(k * n)
        eo, el = [], []
        for _ in range(12):
            X = r.standard_normal((n, p))
            e = r.laplace(0, 1 / math.sqrt(2), n)  # unit variance
            bo = np.linalg.lstsq(X, e, rcond=None)[0]
            bl = M.lad_fit(X, e)
            eo.append(np.sum(bo ** 2))
            el.append(np.sum(bl ** 2))
        res.append({"kappa": k, "ols": float(np.mean(eo)), "lad": float(np.mean(el)), "ols_exact": p / (n - p - 1), "ols_mcse": M.mcse(eo), "lad_mcse": M.mcse(el), "ols_draws": eo, "lad_draws": el})
    return {"n": n, "rows": res}


def compute_amp():
    r = rng(5907)
    n, p = 1000, 2000
    delta, eps, sigma2, theta = n / p, 0.1, 0.01, 1.5
    x0 = np.zeros(p)
    idx = r.choice(p, int(eps * p), replace=False)
    x0[idx] = r.choice([-1.0, 1.0], len(idx))
    A = r.standard_normal((n, p)) / math.sqrt(n)
    y = A @ x0 + math.sqrt(sigma2) * r.standard_normal(n)
    a = M.amp_lasso(A, y, theta, 25)
    se = M.state_evolution(delta, eps, sigma2, theta, 25)
    grid = np.linspace(0.0, 0.25, 101)
    smap = [sigma2 + M._bg_mse(math.sqrt(t2), theta * math.sqrt(t2), eps) / delta if t2 > 0 else sigma2 for t2 in grid]
    mse_amp = [float(np.mean((x - x0) ** 2)) for x in a["path"]]
    deltas = np.linspace(0.05, 0.95, 37)
    return {"n": n, "p": p, "delta": delta, "eps": eps, "sigma2": sigma2, "theta": theta, "tau2_amp": np.asarray(a["tau"]) ** 2,
            "tau2_se": se, "grid": grid, "smap": smap, "mse_amp": mse_amp, "deltas": deltas, "dt": M.minimax_threshold_curve(deltas)}


def compute_bayes():
    eps, sigma2 = 0.1, 1e-4
    deltas = np.round(np.arange(0.10, 0.61, 0.025), 3)
    rows = []
    for d in deltas:
        t2 = M.bayes_state_evolution(float(d), eps, sigma2, 300)[-1]
        b = M.bayes_mmse(math.sqrt(t2), eps)
        las = M.lasso_se_mse(float(d), eps, sigma2)
        rows.append({"delta": float(d), "bayes": b, "lasso": las["mse"], "theta": las["theta"]})
    from scipy.optimize import brentq
    dt = brentq(lambda d: float(M.minimax_threshold_curve([d])[0])*d-eps,.01,.99)  # rho * delta = eps on the DT curve
    return {"eps": eps, "sigma2": sigma2, "rows": rows, "dt_delta": dt, "scope": "uninformative-initialized Bayes-denoising AMP fixed point, not globally optimized replica MMSE; lasso threshold grid, nonzero measurement noise"}


def compute_rf():
    r = rng(5908)
    n, d = 300, 30
    Ns = [10, 30, 60, 100, 150, 200, 250, 280, 300, 320, 350, 400, 500, 700, 1000, 1500, 2500]
    audit = M.random_features_experiment(n,d,Ns,[0.,1e-3],6,r)
    err0,err1 = audit["mean"]
    return {"n": n, "d": d, "Ns": Ns, "ridgeless": err0, "ridge": err1, "audit": audit}


def compute_real():
    """The Wisconsin biopsies' 30 standardized features as the design (strongly correlated), logistic outcomes simulated
    from a known beta with every coordinate +-1 and Var(x'beta) = 5; n = 150 per fit (kappa = 0.2).  Inflation is
    measured on held-out biopsies as the slope of the fitted linear predictor x'beta_hat on the true x'beta, which is
    well defined even when the correlated coordinates are not."""
    X, y, names = museum.breast_cancer()
    Z = (X - X.mean(0)) / X.std(0)
    r = rng(5909)
    n_sub, p = 150, Z.shape[1]
    reps = 200
    g2 = GAMMA2
    slopes = []
    failures = 0
    for _ in range(reps):
        o = r.permutation(len(Z))
        idx, ho = o[:n_sub], o[n_sub:]
        Xs, Xh = Z[idx] / math.sqrt(n_sub), Z[ho] / math.sqrt(n_sub)
        beta = r.choice([-1.0, 1.0], p)
        beta *= math.sqrt(g2 / np.var(Xs @ beta))
        ys = (r.random(n_sub) < 1 / (1 + np.exp(-(Xs @ beta)))).astype(float)
        b, _, ok = M.logistic_mle(Xs, ys)
        if not ok or not np.all(np.isfinite(b)):
            failures += 1
            continue
        eh, et = Xh @ b, Xh @ beta
        slopes.append(float(np.sum(eh * et) / np.sum(et * et)))
    sc = M.sur_candes(p / n_sub, math.sqrt(g2))
    return {"n": n_sub, "p": p, "kappa": p / n_sub, "gamma2": g2, "reps": len(slopes), "slope_mean": float(np.mean(slopes)),
            "slope_q": [float(np.quantile(slopes, q)) for q in (0.1, 0.5, 0.9)], "alpha_theory": sc["alpha"], "slopes": slopes, "attempts": reps, "failed_finite_fits": failures, "slope_mean_mcse": M.mcse(slopes),
            "scope": "fixed empirical design, random subsampling/beta/outcomes; conditional on finite converged MLE; not a calibration theorem for non-Gaussian predictors"}


def compute_board():
    d = load("lrt")
    rows = [Row(59, r"LRT with the $\chi^2_1$ approximation", r"logistic, \ $p/n = 0.2$, \ $\gamma^2 = 5$", "size", 0.05, d["size_classic"], d["reps"], mc_se=d["size_classic_mcse"]),
            Row(59, r"LRT rescaled by $\kappa\sigma_\star^2/\lambda_\star$", r"logistic, \ $p/n = 0.2$, \ $\gamma^2 = 5$", "size", 0.05, d["size_rescaled"], d["reps"], mc_se=d["size_rescaled_mcse"])]
    save_rows(59, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows]}


ITEMS = {
    "hook": compute_hook, "lrt": compute_lrt, "table": compute_table, "mp": compute_mp, "free": compute_free,
    "ridge": compute_ridge, "robust": compute_robust, "amp": compute_amp, "bayes": compute_bayes, "rf": compute_rf,
    "real": compute_real, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
