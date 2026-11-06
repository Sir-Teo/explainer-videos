"""Precompute every number in Part 27 of *Statistics, Built* ("Bayesian Computation").

    python -m videos.stats.stats27.compute            # everything missing (about forty minutes: the Board runs NUTS)
    python -m videos.stats.stats27.compute --force board

Results are cached in ``.cache/stats27/<name>.json``.  The eight schools and Bliss's beetles are the Museum's; the rest
are seeded simulations.

Items:
    disks       Metropolis et al.'s hard disks: a random-displacement walk with overlaps rejected
    banana      a random-walk Metropolis path on a curved two-dimensional density
    importance  importance sampling with three proposals: weights, ESS, PSIS k-hat; a tail probability
    rwm         random-walk Metropolis in 20 dimensions: acceptance and ESS against the step size (the 0.234 rule)
    gibbs       Gibbs on a correlated normal; Albert-Chib probit for Bliss's beetles, raw and centred dose
    diagnostics healthy and stuck chains: R-hat, bulk and tail ESS
    hmc         leapfrog vs Euler on an oscillator; an HMC trajectory; HMC vs RWM in 100 dimensions
    nuts        one NUTS trajectory; step-size adaptation; tree depths
    funnel      Neal's funnel and the eight schools, centred and non-centred, against the exact grid
    ppl         statkit.ppl checked against closed forms
    smc         a particle filter against the Kalman filter; tempered SMC evidence against the exact evidence
    vi          mean-field ADVI on a correlated normal and on the eight schools; CAVI for a normal sample
    laplace     Laplace against NUTS for a small and a large logistic regression
    abc         rejection ABC for a Poisson rate with sufficient and insufficient summaries
    cftp        coupling from the past for an Ising model
    board       Coverage Board rows: simulation-based coverage of four ways to compute the eight-schools posterior
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import optimize, special, stats

from explainer.ai.autodiff import Tensor
from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import bayes as B
from explainer.stats.kit import ppl as P

CACHE = Cache("stats27")
load = CACHE.load
Y8 = np.array([28.0, 8, -3, 7, -1, 1, 18, 12])
S8 = np.array([15.0, 10, 16, 11, 9, 11, 10, 18])


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


def schools_model(centred: bool, y=Y8, s=S8):
    if centred:
        def logp(p):
            return (P.normal_lpdf(p["mu"], 0.0, 5.0) + P.halfcauchy_lpdf(p["tau"], 5.0) + P.normal_lpdf(p["theta"], p["mu"], p["tau"])
                    + P.normal_lpdf(y, p["theta"], s))
        return P.Model({"mu": (1, "real"), "tau": (1, "positive"), "theta": (8, "real")}, logp)

    def logp(p):
        theta = p["mu"] + p["tau"] * p["z"]
        return (P.normal_lpdf(p["mu"], 0.0, 5.0) + P.halfcauchy_lpdf(p["tau"], 5.0) + P.normal_lpdf(p["z"], 0.0, 1.0)
                + P.normal_lpdf(y, theta, s))
    return P.Model({"mu": (1, "real"), "tau": (1, "positive"), "z": (8, "real")}, logp)


def schools_grid(y=Y8, s=S8):
    grid = np.linspace(0, 80, 8001)
    return B.hier_normal(y, s, grid, lambda t: stats.halfcauchy.logpdf(t, scale=5), mu_prior=(0.0, 5.0))


def compute_disks():
    """N disks of diameter d in the unit square (hard walls), each move a uniform displacement of up to delta."""
    g = rng(1953)
    N, d, delta = 40, 0.11, 0.06
    side = int(np.ceil(np.sqrt(N)))
    xy = np.array([[((i % side) + 0.5) / side, ((i // side) + 0.5) / side] for i in range(N)])
    start = xy.copy()
    acc, moves, snaps = 0, 0, []
    for sweep in range(400):
        for i in range(N):
            prop = xy[i] + delta * (2 * g.random(2) - 1)
            moves += 1
            if np.any(prop < d / 2) or np.any(prop > 1 - d / 2):
                continue
            dist = np.sqrt(np.sum((xy - prop) ** 2, axis=1))
            dist[i] = np.inf
            if np.all(dist >= d):
                xy[i] = prop
                acc += 1
        if sweep in (0, 5, 20, 100, 399):
            snaps.append(xy.copy())
    return nest({"N": N, "d": d, "delta": delta, "start": start, "snaps": snaps, "accept": acc / moves})


def banana_logp(x):
    a, b = 1.0, 0.5
    return -0.5 * (x[0] / 2.0) ** 2 - 0.5 * ((x[1] - b * (x[0] ** 2 - a)) / 0.6) ** 2


def compute_banana():
    r = P.rwm(banana_logp, np.array([-3.0, 3.0]), 0.6, 3000, rng(1954))
    xs, ys = np.linspace(-6, 6, 120), np.linspace(-3, 9, 120)
    X, Y = np.meshgrid(xs, ys)
    Z = np.exp(-0.5 * (X / 2.0) ** 2 - 0.5 * ((Y - 0.5 * (X ** 2 - 1)) / 0.6) ** 2)
    return nest({"path": r["draws"][:400], "draws": r["draws"], "accept": float(r["accept"].mean()), "Z": Z,
                 "x_range": [-6, 6], "y_range": [-3, 9]})


def compute_importance():
    g = rng(1949)
    n = 2000
    out = {"n": n, "props": {}}
    for name, dist in (("narrow", stats.norm(0, 0.5)), ("wide", stats.norm(0, 3)), ("t3", stats.t(3))):
        x = dist.rvs(size=n, random_state=g)
        lw = stats.norm.logpdf(x) - dist.logpdf(x)
        w = np.exp(lw - lw.max())
        w /= w.sum()
        est = float(np.sum(w * x ** 2))
        ws, k = P.psis(lw)
        out["props"][name] = {"est": est, "est_psis": float(np.sum(ws * x ** 2)), "ess": P.ess_is(w), "khat": k,
                              "max_w": float(w.max()), "x": x[:400], "w": w[:400] * n}
    # tail probability P(X > 3) for X ~ N(0, 1): naive vs the shifted proposal N(3.15, 1)
    truth = float(stats.norm.sf(3))
    x = g.normal(size=n)
    naive = float(np.mean(x > 3))
    z = g.normal(3.15, 1, n)
    lw = stats.norm.logpdf(z) - stats.norm.logpdf(z, 3.15, 1)
    iswts = np.exp(lw) * (z > 3)
    is_est = float(iswts.mean())
    reps = [(np.mean(g.normal(size=n) > 3), np.mean(np.exp(stats.norm.logpdf(zz) - stats.norm.logpdf(zz, 3.15, 1)) * (zz > 3)))
            for zz in (g.normal(3.15, 1, n) for _ in range(200))]
    reps = np.array(reps)
    out["tail"] = {"truth": truth, "naive": naive, "is": is_est, "sd_naive": float(reps[:, 0].std()), "sd_is": float(reps[:, 1].std())}
    return nest(out)


def compute_rwm():
    d = 20
    g = rng(1996)

    def lp(x):
        return -0.5 * float(x @ x)

    ells = np.array([0.3, 0.6, 1.0, 1.5, 2.0, 2.4, 3.0, 4.0, 5.5, 8.0])
    acc, ess1, ess2 = [], [], []
    traces = {}
    for ell in ells:
        r = P.rwm(lp, g.normal(size=d), ell / np.sqrt(d), 20000, g)
        dr = r["draws"][2000:]
        acc.append(float(r["accept"].mean()))
        ess1.append(P.ess_basic(dr[:, 0][None, :]) / len(dr))
        ess2.append(P.ess_basic(np.sum(dr ** 2, 1)[None, :]) / len(dr))
        if ell in (0.3, 2.4, 8.0):
            traces[f"{ell}"] = dr[:600, 0]
    return nest({"d": d, "ells": ells, "accept": acc, "ess_x1": ess1, "ess_r2": ess2, "traces": traces})


def compute_gibbs():
    g = rng(1984)
    rho = 0.95
    x = np.array([-2.5, 2.5])
    path = [x.copy()]
    pts = []
    for i in range(2000):
        x = x.copy()
        x[0] = rho * x[1] + np.sqrt(1 - rho ** 2) * g.standard_normal()
        path.append(x.copy())
        x = x.copy()
        x[1] = rho * x[0] + np.sqrt(1 - rho ** 2) * g.standard_normal()
        path.append(x.copy())
        pts.append(x.copy())
    pts = np.array(pts)
    ess = P.ess_basic(pts[:, 0][None, :])
    # Albert-Chib probit for Bliss's beetles (481 beetles)
    dose, n_, k_ = (np.asarray(a, float) for a in museum.bliss())
    xs = np.repeat(dose, n_.astype(int))
    ys = np.concatenate([np.r_[np.ones(int(k)), np.zeros(int(n - k))] for n, k in zip(n_, k_)])
    out = {}
    import statsmodels.api as sm
    for name, xv in (("raw", xs), ("centred", xs - xs.mean())):
        X = np.column_stack([np.ones(len(xv)), xv])
        dr = P.gibbs_probit(X, ys, 3000, g)[500:]
        mle = sm.Probit(ys, X).fit(disp=0)
        out[name] = {"mean": dr.mean(0), "sd": dr.std(0), "mle": mle.params, "mle_se": mle.bse,
                     "ess_slope": P.ess_basic(dr[:, 1][None, :]), "trace_slope": dr[:400, 1], "n": len(dr)}
    return nest({"rho": rho, "path": np.array(path[:61]), "ess_x1": ess, "n": len(pts), "probit": out})


def compute_diagnostics():
    g = rng(2021)

    def bimodal(x):
        return float(np.logaddexp(stats.norm.logpdf(x[0], -4, 0.6), stats.norm.logpdf(x[0], 4, 0.6)))

    stuck = np.stack([P.rwm(bimodal, np.array([s]), 0.6, 2000, g)["draws"][:, 0] for s in (-4, -4, 4, -4)])
    good = np.stack([P.rwm(bimodal, np.array([s]), 8.0, 2000, g)["draws"][:, 0] for s in (-4, 4, -4, 4)])
    out = {}
    for k, ch in (("stuck", stuck), ("good", good)):
        out[k] = {"chains": ch[:, ::4], "rhat": P.rhat(ch), "ess_bulk": P.ess_bulk(ch), "ess_tail": P.ess_tail(ch),
                  "mean": float(ch.mean())}
    return nest(out)


def compute_hmc():
    # the harmonic oscillator H = (q^2 + p^2)/2: Euler and leapfrog with eps = 0.3 for 60 steps
    eps, n = 0.3, 60
    q, p = 1.0, 0.0
    euler = [(q, p)]
    for _ in range(n):
        q, p = q + eps * p, p - eps * q
        euler.append((q, p))
    q, p = 1.0, 0.0
    lf = [(q, p)]
    for _ in range(n):
        p -= 0.5 * eps * q
        q += eps * p
        p -= 0.5 * eps * q
        lf.append((q, p))
    euler, lf = np.array(euler), np.array(lf)
    H = lambda a: 0.5 * (a[:, 0] ** 2 + a[:, 1] ** 2)  # noqa: E731
    # an HMC trajectory on a correlated 2-D normal
    rho = 0.9
    Si = np.linalg.inv(np.array([[1, rho], [rho, 1]]))

    def lp2(pp):
        x = pp["x"]
        return ((x @ Si) * x).sum() * -0.5

    m2 = P.Model({"x": (2, "real")}, lp2)
    h = P.hmc(m2, np.array([-1.5, -1.0]), 0.15, 25, 8, rng(1987), record=True)
    # 100 dimensions, scales from 0.01 to 1 (Neal 2011's example): HMC vs RWM per gradient (or density) evaluation
    d = 100
    sc = np.linspace(0.01, 1, d)

    def lp100(pp):
        x = pp["x"]
        return ((x / sc) * (x / sc)).sum() * -0.5

    m100 = P.Model({"x": (d, "real")}, lp100)
    g = rng(2011)
    hm = P.hmc(m100, g.normal(size=d) * sc, 0.013, 150, 400, g)
    dr = hm["draws"][100:]
    ess_h = P.ess_basic(dr[:, -1][None, :])
    evals_h = 300 * 150
    rw = P.rwm(lambda x: -0.5 * float(np.sum((x / sc) ** 2)), g.normal(size=d) * sc, 0.024, 60000, g)
    drw = rw["draws"][10000:]
    ess_r = P.ess_basic(drw[:, -1][None, :])
    evals_r = 50000
    return nest({"eps": eps, "euler": euler, "leapfrog": lf, "H_euler": H(euler), "H_lf": H(lf), "paths": h["paths"],
                 "accept2": float(h["accept"].mean()), "rho": rho, "hmc_accept": float(hm["accept"].mean()),
                 "rwm_accept": float(rw["accept"].mean()), "ess_hmc_per_1000": 1000 * ess_h / evals_h,
                 "ess_rwm_per_1000": 1000 * ess_r / evals_r, "ess_hmc": ess_h, "ess_rwm": ess_r,
                 "trace_hmc": dr[:200, -1], "trace_rwm": drw[::250][:200, -1]})


def compute_nuts():
    rho = 0.95
    Si = np.linalg.inv(np.array([[1, rho], [rho, 1]]))

    def lp2(pp):
        x = pp["x"]
        return ((x @ Si) * x).sum() * -0.5

    m2 = P.Model({"x": (2, "real")}, lp2)
    g = rng(2014)
    q = np.array([1.8, 1.4])
    lp, gr = m2.logp_grad(q)
    trajs = []
    for _ in range(3):
        q, lp, gr, st = P.nuts_step(m2, q, lp, gr, 0.12, np.ones(2), g, record=True)
        trajs.append({"path": np.array(st["path"]), "end": q.copy(), "depth": st["depth"], "n": st["n_leapfrog"]})
    # adaptation trace on the eight schools (non-centred)
    m = schools_model(False)
    rg = rng(2015)
    U, info, eps, inv_m, wdiv = P.nuts(m, 1000, 1000, rg)
    fit = P.sample(m, chains=4, iters=1000, warmup=1000, seed=27, delta=0.9)
    depth = np.bincount(fit.depth.ravel().astype(int), minlength=11)
    return nest({"rho": rho, "trajs": trajs, "eps_final": eps, "inv_metric": inv_m, "depth_counts": depth,
                 "mean_leapfrog": float(fit.n_leapfrog.mean()), "divergent": int(fit.divergent.sum()),
                 "rhat_tau": P.rhat(np.log(fit.draws["tau"][..., 0])), "ess_tau": P.ess_bulk(np.log(fit.draws["tau"][..., 0])),
                 "n_grad": fit.n_grad})


def compute_funnel():
    # Neal's funnel: v ~ N(0, 3^2), x_i | v ~ N(0, e^{v}) for i = 1..9 (sd e^{v/2})
    def lpc(p):
        v = p["v"]
        sd = (v * 0.5).exp()
        return P.normal_lpdf(v, 0.0, 3.0) + P.normal_lpdf(p["x"], 0.0, sd)

    def lpn(p):
        return P.normal_lpdf(p["v"], 0.0, 3.0) + P.normal_lpdf(p["z"], 0.0, 1.0)

    fc = P.sample(P.Model({"v": (1, "real"), "x": (9, "real")}, lpc), chains=2, iters=1000, warmup=1000, seed=2003)
    fn = P.sample(P.Model({"v": (1, "real"), "z": (9, "real")}, lpn), chains=2, iters=1000, warmup=1000, seed=2003)
    vc = fc.draws["v"][..., 0].ravel()
    xc = fc.draws["x"][..., 0].ravel()
    vn = fn.draws["v"][..., 0].ravel()
    xn = (fn.draws["z"][..., 0] * np.exp(fn.draws["v"][..., 0] / 2)).ravel()
    div = fc.divergent.ravel()
    funnel = {"vc": vc, "xc": xc, "div": div, "vn": vn, "xn": xn, "div_c": int(div.sum()), "div_n": int(fn.divergent.sum()),
              "q05_c": float(np.quantile(vc, 0.05)), "q05_n": float(np.quantile(vn, 0.05)), "q05_true": float(stats.norm.ppf(0.05, 0, 3))}
    # eight schools, centred (delta 0.8 and 0.99) and non-centred, against the exact grid
    h = schools_grid()
    grid = h.tau
    cdf = np.cumsum(h.post_tau * np.gradient(grid))
    cdf /= cdf[-1]
    exact = {"median": float(np.interp(0.5, cdf, grid)), "q05": float(np.interp(0.05, cdf, grid)), "q95": float(np.interp(0.95, cdf, grid))}
    lt = np.linspace(-6, 4, 200)
    dens_lt = np.interp(np.exp(lt), grid, h.post_tau) * np.exp(lt)
    res = {}
    for key, centred, delta in (("centred", True, 0.8), ("centred99", True, 0.99), ("noncentred", False, 0.9)):
        f = P.sample(schools_model(centred), chains=4, iters=1000, warmup=1000, seed=81, delta=delta)
        tau = f.draws["tau"][..., 0]
        res[key] = {"divergent": int(f.divergent.sum()), "rhat": P.rhat(np.log(tau)), "ess": P.ess_bulk(np.log(tau)),
                    "median": float(np.median(tau)), "q05": float(np.quantile(tau, 0.05)), "q95": float(np.quantile(tau, 0.95)),
                    "logtau": np.log(tau[:, ::2]).ravel(), "div_logtau": np.log(tau)[f.divergent].ravel()[:200],
                    "mu_div": f.draws["mu"][..., 0][f.divergent][:200], "n_grad": f.n_grad,
                    "step": float(f.step_size.mean())}
    return nest({"funnel": funnel, "exact": exact, "lt": lt, "dens_lt": dens_lt, "schools": res})


def compute_ppl():
    rows = []
    g = rng(2770)
    # 1. normal mean, known sigma
    y = g.normal(1.0, 2.0, 25)
    f = P.sample(P.Model({"mu": (1, "real")}, lambda p: P.normal_lpdf(p["mu"], 0.0, 3.0) + P.normal_lpdf(y, p["mu"], 2.0)),
                 chains=4, iters=1000, warmup=500, seed=1)
    m, s = B.normal_update(0.0, 3.0, y.mean(), 2.0, 25)
    d = f.draws["mu"][..., 0]
    rows.append(["normal mean, \\ posterior mean", m, float(d.mean()), float(d.std() / np.sqrt(P.ess_bulk(d)))])
    rows.append(["normal mean, \\ posterior SD", s, float(d.std()), None])
    # 2. a proportion, uniform prior, unit transform
    k, n = 14, 40
    f = P.sample(P.Model({"p": (1, "unit")}, lambda p: P.binomial_logit_lpmf(k, n, (p["p"] / (1.0 - p["p"])).log())),
                 chains=4, iters=1000, warmup=500, seed=2)
    d = f.draws["p"][..., 0]
    rows.append(["proportion, \\ 90\\% quantile", float(stats.beta.ppf(0.9, 1 + k, 1 + n - k)), float(np.quantile(d, 0.9)), None])
    # 3. a Poisson rate, gamma prior, positive transform
    x = g.poisson(3.0, 30)
    f = P.sample(P.Model({"lam": (1, "positive")}, lambda p: P.poisson_log_lpmf(x, p["lam"].log() + 0.0 * p["lam"]) +
                         (p["lam"].log() * 1.0 - p["lam"] * 1.0).sum()), chains=4, iters=1000, warmup=500, seed=3)
    d = f.draws["lam"][..., 0]
    a, b = 2.0 + x.sum(), 1.0 + len(x)
    rows.append(["Poisson rate, \\ Gamma(2, 1) prior, \\ mean", float(a / b), float(d.mean()), float(d.std() / np.sqrt(P.ess_bulk(d)))])
    # 4. eight schools tau median, against the exact grid
    h = schools_grid()
    cdf = np.cumsum(h.post_tau * np.gradient(h.tau))
    cdf /= cdf[-1]
    f = P.sample(schools_model(False), chains=4, iters=1000, warmup=1000, seed=4, delta=0.9)
    d = f.draws["tau"][..., 0]
    rows.append(["eight schools, \\ median $\\tau$", float(np.interp(0.5, cdf, h.tau)), float(np.median(d)), None])
    mean_th = (f.draws["mu"][..., 0][..., None] + f.draws["tau"][..., 0][..., None] * f.draws["z"]).reshape(-1, 8).mean(0)
    hd = h.draws(200_000, g)
    rows.append(["eight schools, \\ $E\\,\\theta_A$", float(hd["theta"][:, 0].mean()), float(mean_th[0]), None])
    return {"rows": rows}


def compute_smc():
    g = rng(1993)
    T = 60
    x = np.cumsum(g.normal(0, 0.5, T))
    y = x + g.normal(0, 1.0, T)
    k = P.kalman_local_level(y, 0.25, 1.0)
    pf = P.particle_filter(y, 1000, 0.25, 1.0, g)
    spread = {}
    for N in (50, 200, 1000):
        lls = [P.particle_filter(y, N, 0.25, 1.0, g)["loglik"] for _ in range(40)]
        spread[str(N)] = {"sd": float(np.std(lls)), "mean": float(np.mean(lls))}
    # tempered SMC evidence for polynomial degrees (Part 26's data)
    from videos.stats.stats26.compute import load as load26
    o = load26("occam")
    xs, ys = np.asarray(o["x"]), np.asarray(o["y"])
    alpha, sig = o["alpha"], o["sigma"]
    ev = []
    for deg in (1, 2, 3, 4):
        X = np.vander(xs, deg + 1, increasing=True)
        res = P.smc_tempering(lambda n, r, dd=deg: r.normal(0, 1 / np.sqrt(alpha), (n, dd + 1)),
                              lambda w, X=X: float(np.sum(stats.norm.logpdf(ys, X @ w, sig))),
                              lambda w: float(np.sum(stats.norm.logpdf(w, 0, 1 / np.sqrt(alpha)))), 2000, g)
        ev.append({"deg": deg, "smc": res["log_evidence"], "exact": B.blr_log_evidence(X, ys, alpha, sig), "phi": res["phi"]})
    return nest({"x": x, "y": y, "kalman": k["mean"], "kalman_sd": np.sqrt(k["var"]), "pf": pf["mean"],
                 "ll_kalman": k["loglik"], "ll_pf": pf["loglik"], "spread": spread, "evidence": ev})


def compute_vi():
    rho = 0.9
    S = np.array([[1, rho], [rho, 1]])
    Si = np.linalg.inv(S)

    def lp2(pp):
        x = pp["x"]
        return ((x @ Si) * x).sum() * -0.5

    v2 = P.advi(P.Model({"x": (2, "real")}, lp2), 3000, rng(2017), lr=0.02)
    # the eight schools, non-centred, ADVI vs NUTS
    m = schools_model(False)
    va = P.advi(m, 4000, rng(2018), lr=0.03, samples=8)
    khat = P.advi_psis_khat(m, va, 4000, rng(2019))
    g = rng(2020)
    U = va["mean"] + np.exp(va["log_sd"]) * g.standard_normal((20000, m.dim))
    tau_vi = np.exp(U[:, 1])
    f = P.sample(m, chains=4, iters=1000, warmup=1000, seed=5, delta=0.9)
    tau_n = f.draws["tau"][..., 0].ravel()
    # CAVI for x_i ~ N(mu, 1/lam), mu | lam ~ N(0, 1/(k0 lam)), lam ~ Gamma(a0, b0): Bishop section 10.1.3
    xs = rng(2021).normal(2.0, 1.5, 20)
    n, xb = len(xs), xs.mean()
    a0, b0, k0 = 1.0, 1.0, 0.1
    E_lam = 1.0
    path = []
    for _ in range(12):
        mu_n = (k0 * 0 + n * xb) / (k0 + n)
        prec_mu = (k0 + n) * E_lam
        a_n = a0 + (n + 1) / 2
        E_sq = np.sum((xs - mu_n) ** 2) + n / prec_mu + k0 * (mu_n ** 2 + 1 / prec_mu)
        b_n = b0 + 0.5 * E_sq
        E_lam = a_n / b_n
        path.append([mu_n, 1 / np.sqrt(prec_mu), E_lam])
    # exact marginal of mu: Student t
    kn = k0 + n
    an = a0 + n / 2
    bn = b0 + 0.5 * np.sum((xs - xb) ** 2) + 0.5 * k0 * n * xb ** 2 / kn
    sd_exact = float(np.sqrt(bn / (an * kn) * (2 * an) / (2 * an - 2)))
    return nest({"rho": rho, "mf_sd": np.exp(v2["log_sd"]), "mf_mean": v2["mean"], "elbo2": v2["elbo"][::20],
                 "tau_vi": np.quantile(tau_vi, [0.05, 0.5, 0.95]), "tau_nuts": np.quantile(tau_n, [0.05, 0.5, 0.95]),
                 "khat": khat, "elbo8": va["elbo"][::40], "logtau_vi": np.log(tau_vi[:4000]), "logtau_nuts": np.log(tau_n[::2]),
                 "cavi": path, "cavi_sd_mu": float(path[-1][1]), "exact_sd_mu": sd_exact, "xbar": float(xb)})


def compute_laplace():
    out = {}
    for name, n, seed in (("small", 20, 31), ("large", 400, 32)):
        g = rng(seed)
        x = g.normal(size=n)
        y = (g.random(n) < special.expit(0.5 + 1.5 * x)).astype(float)
        X = np.column_stack([np.ones(n), x])

        def lp(p, X=X, y=y):
            b = p["b"]
            return P.normal_lpdf(b, 0.0, 2.5) + P.bernoulli_logit_lpmf(y, Tensor(X) @ b)

        m = P.Model({"b": (2, "real")}, lp)
        f = P.sample(m, chains=4, iters=1000, warmup=500, seed=seed)
        bs = f.draws["b"][..., 1].ravel()
        neg = lambda u: -m.log_density(u)  # noqa: E731
        r = optimize.minimize(neg, np.zeros(2), method="BFGS")
        from explainer.stats.kit.mle import numerical_hessian
        H = numerical_hessian(lambda u: m.log_density(u), r.x, h=1e-4)
        cov = np.linalg.inv(-H)
        grid = np.linspace(bs.min(), bs.max(), 200)
        kde = stats.gaussian_kde(bs)(grid)
        out[name] = {"n": n, "grid": grid, "nuts": kde, "laplace": stats.norm.pdf(grid, r.x[1], np.sqrt(cov[1, 1])),
                     "mode": float(r.x[1]), "sd_lap": float(np.sqrt(cov[1, 1])), "mean_nuts": float(bs.mean()),
                     "sd_nuts": float(bs.std()), "q95_nuts": float(np.quantile(bs, 0.95)),
                     "q95_lap": float(stats.norm.ppf(0.95, r.x[1], np.sqrt(cov[1, 1])))}
    return nest(out)


def compute_abc():
    g = rng(2002)
    lam_true, n = 3.0, 15
    x = g.poisson(lam_true, n)
    a0, b0 = 2.0, 1.0
    exact = stats.gamma(a0 + x.sum(), scale=1 / (b0 + n))
    res = {}
    for name, summ, s_obs in (("mean", np.mean, x.mean()), ("median", np.median, np.median(x))):
        res[name] = {}
        for eps in (1.0, 0.3, 0.05):
            r = P.abc_rejection(lambda rg: rg.gamma(a0, 1 / b0), lambda th, rg: rg.poisson(th, n), summ, s_obs, 1000, eps, g)
            d = r["draws"]
            res[name][f"{eps}"] = {"mean": float(d.mean()), "sd": float(d.std()), "accept": r["accept_rate"],
                                   "hist": np.histogram(d, np.linspace(0, 7, 36), density=True)[0]}
    grid = np.linspace(0, 7, 200)
    return nest({"x": x, "exact_mean": float(exact.mean()), "exact_sd": float(exact.std()), "grid": grid,
                 "exact_pdf": exact.pdf(grid), "edges": np.linspace(0, 7, 36), "res": res})


def compute_cftp():
    out = {}
    for name, beta in (("warm", 0.3), ("near", 0.42)):
        r = P.cftp_ising(16, beta, rng(1996 if name == "warm" else 1997))
        out[name] = {"beta": beta, "state": r["state"], "T": r["T"], "mags": r["mags"]}
    return nest(out)


def compute_board():
    """Simulation-based coverage: draw (mu, tau, theta) from the prior (mu ~ N(0, 5^2), tau ~ half-Cauchy(5)), then
    the eight estimates with the eight schools' standard errors; compute each school's 90% interval four ways."""
    g = rng(2727)
    R = 100
    hits = {"exact": 0, "noncentred": 0, "centred": 0, "advi": 0}
    for i in range(R):
        mu = g.normal(0, 5)
        tau = abs(stats.cauchy.rvs(scale=5, random_state=g))
        theta = mu + tau * g.standard_normal(8)
        y = theta + S8 * g.standard_normal(8)
        h = schools_grid(y, S8)
        dr = h.draws(4000, g)["theta"]
        lo, hi = np.quantile(dr, [0.05, 0.95], axis=0)
        hits["exact"] += int(np.sum((lo <= theta) & (theta <= hi)))
        for key, centred in (("noncentred", False), ("centred", True)):
            f = P.sample(schools_model(centred, y, S8), chains=1, iters=400, warmup=400, seed=10_000 + i, delta=0.8)
            th = (f.draws["theta"] if centred else f.draws["mu"][..., :1] + f.draws["tau"][..., :1] * f.draws["z"]).reshape(-1, 8)
            lo, hi = np.quantile(th, [0.05, 0.95], axis=0)
            hits[key] += int(np.sum((lo <= theta) & (theta <= hi)))
        m = schools_model(False, y, S8)
        va = P.advi(m, 1500, g, lr=0.05, samples=4)
        U = va["mean"] + np.exp(va["log_sd"]) * g.standard_normal((4000, m.dim))
        th = U[:, :1] + np.exp(U[:, 1:2]) * U[:, 2:]
        lo, hi = np.quantile(th, [0.05, 0.95], axis=0)
        hits["advi"] += int(np.sum((lo <= theta) & (theta <= hi)))
    N = 8 * R
    rows = [
        Row(27, r"exact grid draws", r"eight schools, \ truths from the prior", "coverage", 0.90, hits["exact"] / N, N),
        Row(27, r"NUTS, \ non-centred", r"eight schools, \ truths from the prior", "coverage", 0.90, hits["noncentred"] / N, N),
        Row(27, r"NUTS, \ centred", r"eight schools, \ truths from the prior", "coverage", 0.90, hits["centred"] / N, N),
        Row(27, r"mean-field ADVI", r"eight schools, \ truths from the prior", "coverage", 0.90, hits["advi"] / N, N),
    ]
    save_rows(27, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "disks": compute_disks, "banana": compute_banana, "importance": compute_importance, "rwm": compute_rwm,
    "gibbs": compute_gibbs, "diagnostics": compute_diagnostics, "hmc": compute_hmc, "nuts": compute_nuts,
    "funnel": compute_funnel, "ppl": compute_ppl, "smc": compute_smc, "vi": compute_vi, "laplace": compute_laplace,
    "abc": compute_abc, "cftp": compute_cftp, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
