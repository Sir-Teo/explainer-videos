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
    stability ridge regression: uniform stability and the generalization gap by lambda
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
        ex, dev = [], []
        for n in ns:
            e, d = [], []
            for _ in range(200):
                x, y = SL.threshold_data(n, r, eta=eta)
                t = SL.erm_threshold(x, y)
                e.append(float(SL.threshold_risk(t, eta=eta) - eta))
                d.append(SL.uniform_deviation_threshold(x, y, eta=eta))
            ex.append(float(np.mean(e)))
            dev.append(float(np.mean(d)))
        out[str(eta)] = {"excess": ex, "dev": dev}
    return {"ns": ns, "by_eta": out, "vc": [SL.vc_bound(n, 1) for n in ns], "rad": [SL.rademacher_vc_bound(n, 1) for n in ns]}


def compute_rademacher():
    r = rng(5403)
    ns = [25, 50, 100, 200, 400, 800]
    lin, linb, ker, kerb = [], [], [], []
    for n in ns:
        X = r.standard_normal((n, 10)) / math.sqrt(10)
        lin.append(SL.rademacher_linear(X, 1.0, r))
        linb.append(SL.rademacher_linear_bound(X, 1.0))
        K = SL.gaussian_kernel(X, 0.5)
        ker.append(SL.rademacher_kernel(K, 1.0, r))
        kerb.append(math.sqrt(np.trace(K)) / n)
    return {"ns": ns, "linear": lin, "linear_bound": linb, "kernel": ker, "kernel_bound": kerb}


def compute_boosting():
    X, y, names = museum.breast_cancer()
    X = np.asarray(X, float)
    y = np.where(np.asarray(y) == np.unique(y)[0], -1.0, 1.0)
    r = rng(5404)
    idx = r.permutation(len(y))
    tr, te = idx[:340], idx[340:]
    mu, sd = X[tr].mean(0), X[tr].std(0)
    Z = (X - mu) / sd
    out = SL.adaboost(Z[tr], y[tr], 400, Z[te], y[te])
    marg = {k: np.sort(v) for k, v in out["margins"].items()}
    return {"n_train": len(tr), "n_test": len(te), "train": out["train"], "test": out["test"], "margins": marg,
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
        rows.append({"lam": lam, "emp": er, "true": float(rho @ true), "kl": kl, "mcallester": b["mcallester"], "kl_bound": b["kl"]})
    best = int(np.argmin(emp))
    return {"n": n, "eta": eta, "rows": rows, "erm_emp": float(emp[best]), "erm_true": float(true[best]),
            "union": float(emp[best] + SL.finite_class_bound(n, 101))}


def compute_stability():
    r = rng(5406)
    n, p = 200, 50
    lams = [0.001, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0]
    beta = r.standard_normal(p) / math.sqrt(p)
    rows = []
    for lam in lams:
        st, gap = [], []
        for _ in range(10):
            X = r.standard_normal((n, p)) / math.sqrt(p)
            y = X @ beta + 0.5 * r.standard_normal(n)
            w = SL.ridge_fit(X, y, lam)
            Xt = r.standard_normal((2000, p)) / math.sqrt(p)
            yt = Xt @ beta + 0.5 * r.standard_normal(2000)
            gap.append(float(np.mean((yt - Xt @ w) ** 2) - np.mean((y - X @ w) ** 2)))
            st.append(SL.ridge_stability(X, y, lam)["stability"])
        rows.append({"lam": lam, "stability": float(np.mean(st)), "gap": float(np.mean(gap))})
    return {"n": n, "p": p, "rows": rows}


def compute_sgd():
    r = rng(5410)
    n, p, steps = 200, 10, 2000
    X = r.standard_normal((n, p))
    X /= np.maximum(1, np.linalg.norm(X, axis=1))[:, None]
    y = np.sign(X @ (np.ones(p) / math.sqrt(p)) + 0.3 * r.standard_normal(n))
    out = {"n": n, "p": p, "steps": steps}
    for lr in (0.2, 1.0):
        d = SL.sgd_divergence(X, y, steps, lr, r, reps=40)
        out[str(lr)] = {"div": d["divergence"][9::10], "bound": d["bound"][9::10]}
    out["t"] = list(range(10, steps + 1, 10))
    return out


def compute_bandits():
    r = rng(5411)
    mu, T, reps = [0.7, 0.5, 0.45, 0.4, 0.3], 50000, 10
    ts = np.unique(np.round(np.geomspace(10, T, 80)).astype(int))
    out = {"mu": mu, "T": T, "ts": ts}
    for a in ("ucb", "exp3", "greedy"):
        out[a] = np.mean([SL.bandit(mu, T, a, r)[ts - 1] for _ in range(reps)], axis=0)
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
    return {"T": T, "K": K, "ts": ts, "regret": reg, "bound": bound, "final": float(h["regret"][-1]), "final_bound": SL.hedge_bound(T, K)}


def compute_surrogate():
    th = np.linspace(-1, 1, 201)
    return {"theta": th, **{k: SL.psi_transform(th, k) for k in ("hinge", "logistic", "exponential", "squared")}}


def compute_interp():
    r = rng(5408)
    n = 100
    ps = [10, 25, 50, 70, 85, 92, 97, 100, 103, 110, 130, 160, 200, 300, 500, 1000]
    risk = [SL.min_norm_risk(n, p, r, reps=12, p_total=1000) for p in ps]
    benign = [{"n": m, **SL.benign_risk(m, r, reps=4)} for m in (50, 100, 200, 400)]
    short = SL.benign_risk(200, r, p_tail=400, tail_var=0.025, reps=4)
    return {"n": n, "ps": ps, "risk": risk, "benign": benign, "short_tail": short}


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
    save_rows(54, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows], "union_half": SL.finite_class_bound(n, K)}


ITEMS = {
    "shatter": compute_shatter, "erm": compute_erm, "rademacher": compute_rademacher, "boosting": compute_boosting,
    "pacbayes": compute_pacbayes, "stability": compute_stability, "sgd": compute_sgd, "bandits": compute_bandits, "online": compute_online, "surrogate": compute_surrogate,
    "interp": compute_interp, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
