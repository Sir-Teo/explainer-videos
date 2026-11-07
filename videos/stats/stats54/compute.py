"""Precompute every number in Part 54 of *Statistics, Built* ("Statistical Learning Theory").

    OMP_NUM_THREADS=1 python -m videos.stats.stats54.compute            # everything missing (a few minutes)
    python -m videos.stats.stats54.compute --force board

Results are cached in ``.cache/stats54/<name>.json``.  The Wisconsin breast cancer data are the Museum's; everything
else is exact arithmetic or a seeded simulation.

Items:
    shatter   dichotomies of n random points by half-planes against 2^n and the Sauer-Shelah bound
    erm       ERM over thresholds: excess risk and the uniform deviation by n and noise, against VC and Rademacher bounds
    rademacher Rademacher complexity of linear and kernel classes against their trace bounds
    boosting  AdaBoost with stumps on the breast cancer data: training and test error, margins by round
    pacbayes  a Gibbs posterior over 101 thresholds: empirical and true risk, KL, McAllester and kl bounds by temperature
    stability bounded ridge: sampled replacement loss changes and signed generalization gaps by lambda
    sgd       SGD on logistic regression: parameter divergence on neighbouring samples against Hardt-Recht-Singer
    bandits   UCB1, EXP3 and epsilon-greedy on five Bernoulli arms against Lai-Robbins
    online    Hedge over 50 experts: regret against sqrt(T log K / 2); online-to-batch
    surrogate psi-transforms of hinge, logistic, exponential and squared losses
    interp    double descent for min-norm least squares; benign overfitting by n
    board     Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import empirical as EK
from explainer.stats.kit import slt as SL
from . import checked as CK

CACHE = Cache("stats54")
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


def compute_shatter():
    r = rng(5401)
    rows = []
    for n in range(1, 10):
        pts = r.standard_normal((n, 2))
        rows.append({"n": n, "dich": EK.dichotomies_halfplanes(pts), "all": 2 ** n, "sauer": EK.sauer_shelah(n, 3)})
    four = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    return {"rows": rows, "four_square": EK.dichotomies_halfplanes(four)}


def compute_erm():
    r = rng(5402)
    ns = [25, 50, 100, 200, 400, 800, 1600]
    out = {}
    for eta in (0.0, 0.1, 0.4):
        ex, dev, ex_se, dev_se = [], [], [], []
        for n in ns:
            e, d = [], []
            for _ in range(200):
                x, y = SL.threshold_data(n, r, eta=eta)
                t = CK.erm_threshold(x, y)
                e.append(float(SL.threshold_risk(t, eta=eta) - eta))
                d.append(CK.uniform_deviation_threshold(x, y, eta=eta))
            ex.append(float(np.mean(e)))
            dev.append(float(np.mean(d)))
            ex_se.append(CK.mcse(e)); dev_se.append(CK.mcse(d))
        out[str(eta)] = {"excess": ex, "dev": dev, "excess_mcse": ex_se, "dev_mcse": dev_se}
    return {"ns": ns, "by_eta": out, "vc": [SL.vc_bound(n, 1) for n in ns], "rad": [SL.rademacher_vc_bound(n, 1) for n in ns]}


def compute_rademacher():
    r = rng(5403)
    ns = [25, 50, 100, 200, 400, 800]
    lin, linb, ker, kerb, lse, kse = [], [], [], [], [], []
    for n in ns:
        X = r.standard_normal((n, 10)) / math.sqrt(10)
        signs = r.choice([-1., 1.], size=(2000, n))
        vals = np.linalg.norm(signs @ X, axis=1) / n
        lin.append(float(vals.mean())); lse.append(CK.mcse(vals))
        linb.append(SL.rademacher_linear_bound(X, 1.0))
        K = SL.gaussian_kernel(X, 0.5)
        signs = r.choice([-1., 1.], size=(2000, n))
        vals = np.sqrt(np.maximum(np.einsum("ri,ij,rj->r", signs, K, signs), 0)) / n
        ker.append(float(vals.mean())); kse.append(CK.mcse(vals))
        kerb.append(math.sqrt(np.trace(K)) / n)
    return {"ns": ns, "linear": lin, "linear_bound": linb, "kernel": ker, "kernel_bound": kerb, "linear_mcse": lse, "kernel_mcse": kse, "sign_draws": 2000}


def compute_boosting():
    X, y, names = museum.breast_cancer()
    X = np.asarray(X, float)
    y = np.where(np.asarray(y) == np.unique(y)[0], -1.0, 1.0)
    r = rng(5404)
    idx = r.permutation(len(y))
    tr, te = idx[:340], idx[340:]
    mu, sd = X[tr].mean(0), X[tr].std(0)
    Z = (X - mu) / sd
    out = CK.adaboost(Z[tr], y[tr], 400, Z[te], y[te])
    marg = {k: np.sort(v) for k, v in out["margins"].items()}
    return {"n_train": len(tr), "n_test": len(te), "train": out["train"], "test": out["test"], "margins": marg,
            "weighted_errors": out["weighted_errors"], "alphas": out["alphas"],
            "tie_rule": "zero ensemble score predicts +1; cuts never split equal features",
            "zero_round": int(next((i + 1 for i, e in enumerate(out["train"]) if e == 0), -1))}


def compute_pacbayes():
    r = rng(5405)
    n = 500
    eta = 0.15
    grid = np.linspace(0, 1, 101)
    x, y = SL.threshold_data(n, r, eta=eta)
    emp = np.array([np.mean((x > t).astype(int) != y) for t in grid])
    true = SL.threshold_risk(grid, eta=eta)
    rows = []
    for lam in (1, 5, 20, 50, 100, 200, 500, 1000, 3000):
        rho = SL.gibbs_posterior(n * emp, lam / n)
        kl = SL.kl_discrete(rho, np.full(101, 1 / 101))
        er = float(rho @ emp)
        b = SL.pac_bayes_bounds(er, kl, n)
        b["kl"] = CK.kl_inverse(er, (kl + math.log(2 * math.sqrt(n) / .05)) / n)
        rows.append({"lam": lam, "emp": er, "true": float(rho @ true), "kl": kl, "mcallester": b["mcallester"], "kl_bound": b["kl"]})
    best = int(np.argmin(emp))
    return {"n": n, "eta": eta, "rows": rows, "erm_emp": float(emp[best]), "erm_true": float(true[best]),
            "union": float(emp[best] + SL.finite_class_bound(n, 101))}


def compute_stability():
    """Bounded design: sampled replacement LOSS changes, not the uniform supremum."""
    r = rng(5406)
    n, p, reps = 200, 50, 10
    lams = [.001, .01, .03, .1, .3, 1., 3.]
    beta = np.ones(p) / math.sqrt(p)
    def data(m):
        X = r.standard_normal((m, p))
        X /= np.maximum(1., np.linalg.norm(X, axis=1))[:, None]
        y = .5 * (X @ beta) + .5 * r.uniform(-1, 1, m)
        return X, y
    rows = []
    for lam in lams:
        probes, gaps = [], []
        for _ in range(reps):
            X, y = data(n)
            Xt, yt = data(2000)
            w = SL.ridge_fit(X, y, lam)
            loss = (yt - Xt @ w)**2
            gaps.append(float(loss.mean() - np.mean((y - X @ w)**2)))
            diffs = []
            for i in range(0, n, n // 20):
                Xi, yi = X.copy(), y.copy()
                xr, yr = data(1)
                Xi[i], yi[i] = xr[0], yr[0]
                wi = SL.ridge_fit(Xi, yi, lam)
                diffs.append(float(np.max(np.abs(loss - (yt - Xt @ wi)**2))))
            probes.append(max(diffs))
        # Half-squared loss gradient <= 1+1/sqrt(lambda), ||w||<=1/sqrt(lambda).
        # For full squared loss the conservative replacement bound is 4L_half^2/(lambda*n).
        uniform_bound = 4 * (1 + 1 / math.sqrt(lam))**2 / (lam * n)
        rows.append(dict(lam=lam, stability=float(np.mean(probes)), gap=float(np.mean(gaps)),
                         stability_mcse=CK.mcse(probes), gap_mcse=CK.mcse(gaps),
                         sampled_loss_changes=probes, gaps=gaps, uniform_bound=uniform_bound))
    return dict(n=n, p=p, reps=reps, rows=rows, x_radius=1., y_bound=1.,
                scope="20 sampled neighbours and 2000 validation points per dataset; diagnostic, not uniform stability")


def compute_sgd():
    r = rng(5410)
    n, p, steps = 200, 10, 2000
    X = r.standard_normal((n, p))
    X /= np.maximum(1, np.linalg.norm(X, axis=1))[:, None]
    y = np.sign(X @ (np.ones(p) / math.sqrt(p)) + 0.3 * r.standard_normal(n))
    out = {"n": n, "p": p, "steps": steps}
    for lr in (0.2, 1.0):
        d = CK.sgd_divergence(X, y, steps, lr, r, reps=40)
        out[str(lr)] = {"div": d["divergence"][9::10], "bound": d["bound"][9::10],
                        "mcse": d["mcse"][9::10], "paths": d["paths"][:, 9::10],
                        "changed_visits": d["changed_visits"][:, 9::10]}
    out["t"] = list(range(10, steps + 1, 10))
    return out


def compute_bandits():
    r = rng(5411)
    mu, T, reps = [0.7, 0.5, 0.45, 0.4, 0.3], 50000, 10
    ts = np.unique(np.round(np.geomspace(10, T, 80)).astype(int))
    out = {"mu": mu, "T": T, "ts": ts}
    for a in ("ucb", "exp3", "greedy"):
        paths = np.array([SL.bandit(mu, T, a, r)[ts - 1] for _ in range(reps)])
        out[a] = paths.mean(0)
        out[a + "_mcse"] = paths.std(0, ddof=1) / math.sqrt(reps)
        out[a + "_paths"] = paths
    out["lai"] = SL.lai_robbins(mu, ts)
    return out


def compute_online():
    r = rng(5407)
    T, K = 5000, 50
    L = r.random((T, K))
    L[:, 7] = np.clip(L[:, 7] - 0.1, 0, 1)  # one expert slightly better
    eta = math.sqrt(8 * math.log(K) / T)
    h = SL.hedge(L, eta)
    ts = np.unique(np.round(np.geomspace(10, T, 60)).astype(int))
    reg = h["regret"][ts - 1]
    bound = [math.log(K) / eta + eta * int(t) / 8 for t in ts]  # the fixed-eta bound; it equals sqrt(T log K / 2) at T
    return {"T": T, "K": K, "ts": ts, "regret": reg, "bound": bound, "final": float(h["regret"][-1]), "final_bound": SL.hedge_bound(T, K),
            "scope": "deterministic mixture loss, not realized random expert losses",
            "expected_advantage": .095}


def compute_surrogate():
    th = np.linspace(0, 1, 101)
    return {"theta": th, **{k: SL.psi_transform(th, k) for k in ("hinge", "logistic", "exponential", "squared")}}


def compute_interp():
    r = rng(5408)
    n = 100
    ps = [10, 25, 50, 70, 85, 92, 97, 100, 103, 110, 130, 160, 200, 300, 500, 1000]
    samples = [[SL.min_norm_risk(n, p, r, reps=1, p_total=1000) for _ in range(12)] for p in ps]
    risk = np.mean(samples, axis=1)
    analytic = [CK.expected_min_norm_risk(n, p) for p in ps]
    benign = [{"n": m, **CK.benign_risk(m, r, reps=4)} for m in (50, 100, 200, 400)]
    short = CK.benign_risk(200, r, p_tail=400, tail_var=0.025, reps=4)
    return {"n": n, "ps": ps, "risk": risk, "samples": samples, "median": np.median(samples, axis=1),
            "expected_excess": analytic, "infinite_expected_at": [n-1, n, n+1],
            "risk_scope": "latent excess prediction risk; excludes new-response noise .25; 12 finite draws",
            "benign": benign, "short_tail": short}


def compute_board():
    """Intervals for the true error of a selected classifier: pick the best of K = 1000 random classifiers on n = 200
    training points (each with true error 0.5 - small), then (a) the naive Wald interval around its training error,
    (b) Hoeffding plus a union bound over K, (c) a Wald interval on a fresh holdout of 200."""
    r = rng(5409)
    n, K, reps = 200, 1000, 2000
    true = 0.5 - 0.02 * r.random(K)  # true errors, all near one half
    cov = {"naive": 0, "union": 0, "holdout": 0}
    for _ in range(reps):
        errs = r.random((K, n)) < true[:, None]
        tr = errs.mean(axis=1)
        k = int(np.argmin(tr))
        p = tr[k]
        se = math.sqrt(p * (1 - p) / n)
        cov["naive"] += (p - 1.96 * se) <= true[k] <= (p + 1.96 * se)
        h = SL.finite_class_bound(n, K)
        cov["union"] += (p - h) <= true[k] <= (p + h)
        ho = (r.random(n) < true[k]).mean()
        s2 = math.sqrt(ho * (1 - ho) / n)
        cov["holdout"] += (ho - 1.96 * s2) <= true[k] <= (ho + 1.96 * s2)
    st = r"best of 1,000 classifiers, \ $n = 200$"
    rows = [
        Row(54, r"Wald interval on the training error", st, "coverage", 0.95, cov["naive"] / reps, reps),
        Row(54, r"Hoeffding $+$ union bound over the class", st, "coverage", 0.95, cov["union"] / reps, reps),
        Row(54, r"Wald interval on a fresh holdout", st, "coverage", 0.95, cov["holdout"] / reps, reps),
    ]
    for row in rows:
        row.mc_se = math.sqrt(row.achieved * (1 - row.achieved) / reps)
    save_rows(54, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows], "union_half": SL.finite_class_bound(n, K)}


ITEMS = {
    "shatter": compute_shatter, "erm": compute_erm, "rademacher": compute_rademacher, "boosting": compute_boosting,
    "pacbayes": compute_pacbayes, "stability": compute_stability, "sgd": compute_sgd, "bandits": compute_bandits, "online": compute_online, "surrogate": compute_surrogate,
    "interp": compute_interp, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
