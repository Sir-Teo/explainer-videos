"""Precompute every number in Part 62 of *Statistics, Built* ("Frontiers of Causal Inference").

    OMP_NUM_THREADS=1 python -m videos.stats.stats62.compute            # everything missing (a few minutes)
    python -m videos.stats.stats62.compute --force board

Results are cached in ``.cache/stats62/<name>.json``.  The NSW job-training data are the Museum's; everything else is a
seeded simulation.

Items:
    frontdoor    a hidden confounder of A and Y, a mediator M: naive, back-door-impossible, front-door estimates
    msm          NSW against PSID: the IPW estimate and its marginal-sensitivity bounds against the experiment
    proximal     two proxies of a hidden confounder: naive adjustment against proximal 2SLS (coverage)
    interference a random geometric network: exposure-based Hajek contrasts against the naive difference
    policy       empirical welfare maximization with AIPW scores: in-sample against cross-fitted policy values
    dtr          a two-stage SMART: Q-learning's regime against static regimes, valued from the true model
    discovery    random linear SEMs: the PC skeleton, varsortability, and what standardizing does to it
    fusion       a trial younger than its target: the trial ATE, the transported ATE, the target's truth
    surrogate    the surrogate index under its assumption and when the treatment bypasses the surrogates
    board        Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import causal as C
from explainer.stats.kit import frontier as F

CACHE = Cache("stats62")
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


def compute_frontdoor():
    r = rng(6201)
    n = 20000
    U = r.random(n) < 0.5
    A = r.random(n) < np.where(U, 0.8, 0.2)
    M = r.random(n) < np.where(A, 0.75, 0.25)
    Y = 2.0 * M + 3.0 * U + r.standard_normal(n)
    # truth: E[Y | do(a)] = 2 P(M = 1 | a) + 3 P(U = 1) -> ATE = 2 (0.75 - 0.25) = 1
    naive = float(Y[A].mean() - Y[~A].mean())
    fd = F.front_door(Y, A, M)
    g = C.DAG([("U", "A"), ("U", "Y"), ("A", "M"), ("M", "Y")])
    return {"n": n, "truth": 1.0, "naive": naive, "fd": fd["ate"], "frontdoor_ok": F.frontdoor_ok(g, "A", "Y", ["M"]),
            "backdoor_empty": g.backdoor_ok("A", "Y", [])}


def _nsw_psid():
    d = museum.nsw()
    m = (d["sample"] == "psid") | ((d["sample"] == "experiment") & (d["treat"] == 1))
    X = np.column_stack([d[k][m] for k in ("age", "educ", "black", "hisp", "married", "nodegree")] + [d["re74"][m] / 1e4, d["re75"][m] / 1e4])
    e = d["sample"] == "experiment"
    exp = float(d["re78"][e & (d["treat"] == 1)].mean() - d["re78"][e & (d["treat"] == 0)].mean())
    return X, d["treat"][m], d["re78"][m], exp


def compute_msm():
    X, t, y, exp = _nsw_psid()
    Z = (X - X.mean(0)) / X.std(0)
    Z = np.column_stack([Z, Z[:, 6] ** 2, Z[:, 7] ** 2, Z[:, 0] ** 2])
    ps = np.clip(C.propensity(Z, t), 0.01, 0.99)
    naive = float(y[t == 1].mean() - y[t == 0].mean())
    lams = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
    rows = []
    for lam in lams:
        b = F.msm_bounds(y, t, ps, lam)
        rows.append({"lam": lam, "lo": b["ate_lo"], "hi": b["ate_hi"]})
    return {"n1": int((t == 1).sum()), "n0": int((t == 0).sum()), "naive": naive, "ipw": rows[0]["lo"], "exp": exp, "rows": rows,
            "ps_t": ps[t == 1], "ps_c": ps[t == 0]}


def compute_proximal():
    r = rng(6202)
    reps, n = 600, 1000
    cn = cp = 0
    est_n, est_p = [], []
    for _ in range(reps):
        U = r.standard_normal(n)
        Z = U + r.standard_normal(n)
        W = U + r.standard_normal(n)
        A = (0.8 * U + r.standard_normal(n) > 0).astype(float)
        Y = 1.0 * A + 2 * U + r.standard_normal(n)
        o = F.ols_adjusted(Y, A, np.column_stack([Z, W]))
        p = F.proximal_2sls(Y, A, Z, W)
        cn += abs(o["effect"] - 1) < 1.96 * o["se"]
        cp += abs(p["effect"] - 1) < 1.96 * p["se"]
        est_n.append(o["effect"])
        est_p.append(p["effect"])
    return {"reps": reps, "n": n, "truth": 1.0, "cov_naive": cn / reps, "cov_prox": cp / reps, "est_naive": est_n, "est_prox": est_p,
            "mean_naive": float(np.mean(est_n)), "mean_prox": float(np.mean(est_p)), "sd_prox": float(np.std(est_p)), "sd_naive": float(np.std(est_n))}


def compute_interference():
    r = rng(6203)
    n, P = 400, 0.3
    pos = r.random((n, 2))
    D = np.sqrt(((pos[:, None] - pos[None]) ** 2).sum(-1))
    adj = ((D < 0.06) & (D > 0)).astype(int)
    pi = F.exposure_probs(adj, P, r, 4000)
    y0 = r.standard_normal(n)
    reps = 300
    out = {"direct": [], "spill": [], "naive": []}
    for _ in range(reps):
        z = (r.random(n) < P).astype(int)
        y = y0 + 2 * z + 1.0 * ((adj @ z) > 0) + 0.5 * r.standard_normal(n)
        h = F.exposure_hajek(y, z, adj, pi)
        out["direct"].append(h["direct"])
        out["spill"].append(h["spill"])
        out["naive"].append(float(y[z == 1].mean() - y[z == 0].mean()))
    z = (r.random(n) < P).astype(int)
    e = F.exposures(z, adj)
    edges = np.argwhere(np.triu(adj))
    return {"n": n, "p": P, "pos": pos, "edges": edges, "z": z, "exposure": e, "deg": float(adj.sum(1).mean()),
            "frac_isolated": float(np.mean(adj.sum(1) == 0)), "reps": reps, **{k: v for k, v in out.items()},
            "mean": {k: float(np.mean(v)) for k, v in out.items()}, "sd": {k: float(np.std(v)) for k, v in out.items()}}


def _policy_once(r, n):
    x = r.uniform(-1, 1, n)
    t = (r.random(n) < 0.5).astype(float)
    y = x + t * (0.25 * x - 0.1) + r.standard_normal(n)
    idx = r.permutation(n)
    A, B = idx[: n // 2], idx[n // 2:]
    G = np.zeros(n)
    for I, J in ((A, B), (B, A)):
        mu = {}
        for a in (0, 1):
            K = I[t[I] == a]
            mu[a] = np.polyfit(x[K], y[K], 1)
        G[J] = F.aipw_scores(y[J], t[J], np.polyval(mu[0], x[J]), np.polyval(mu[1], x[J]), 0.5)
    return x, G, A, B


def _true_value(rule):
    xs = np.linspace(-1, 1, 20001)
    return float(np.mean((0.25 * xs - 0.1) * F.apply_rule(xs, rule)))


def compute_policy():
    """The effect is tau(x) = 0.25 x - 0.1: treat only when x > 0.4.  The in-sample value of the rule EWM picks is
    optimistic (the winner's curse); learning on one half and evaluating on the other is honest."""
    r = rng(6204)
    reps, n = 800, 400
    cn = cs = 0
    gap_n, gap_s = [], []
    for _ in range(reps):
        x, G, A, B = _policy_once(r, n)
        rule = F.ewm_threshold(x, G)
        g = G * F.apply_rule(x, rule)
        est, se, tv = g.mean(), g.std(ddof=1) / math.sqrt(n), _true_value(rule)
        cn += abs(est - tv) < 1.96 * se
        gap_n.append(est - tv)
        ru = F.ewm_threshold(x[A], G[A])
        gg = G[B] * F.apply_rule(x[B], ru)
        e2, s2, t2 = gg.mean(), gg.std(ddof=1) / math.sqrt(len(B)), _true_value(ru)
        cs += abs(e2 - t2) < 1.96 * s2
        gap_s.append(e2 - t2)
    x, G, A, B = _policy_once(r, n)
    rule = F.ewm_threshold(x, G)
    best = float(np.mean(np.maximum(0.25 * np.linspace(-1, 1, 200001) - 0.1, 0)))
    return {"reps": reps, "n": n, "cov_naive": cn / reps, "cov_split": cs / reps, "gap_naive": float(np.mean(gap_n)),
            "gap_split": float(np.mean(gap_s)), "rule_c": rule["c"], "rule_s": rule["s"], "best": best, "x": x, "G": G,
            "true_cut": 0.4, "value_est": rule["value"], "value_true": _true_value(rule)}


def compute_dtr():
    r = rng(6205)

    def gen(n, policy=None):
        X1 = r.standard_normal(n)
        A1 = (r.random(n) < 0.5).astype(float) if policy is None else policy[0](X1).astype(float)
        X2 = 0.5 * X1 + 0.8 * A1 * (X1 > 0) - 0.4 * A1 + r.standard_normal(n)
        A2 = (r.random(n) < 0.5).astype(float) if policy is None else policy[1](X2).astype(float)
        Y = X2 + A2 * (X2 - 0.2) + 0.5 * A1 * X1 + r.standard_normal(n)
        return X1, A1, X2, A2, Y
    X1, A1, X2, A2, Y = gen(1000)
    q = F.q_learning(X1, A1, X2, A2, Y)
    vals = {}
    pol = {"Q-learning": (q["rule1"], q["rule2"]), "always treat": (lambda x: np.ones_like(x) > 0, lambda x: np.ones_like(x) > 0),
           "never treat": (lambda x: np.zeros_like(x) > 0, lambda x: np.zeros_like(x) > 0),
           "stage 2 only": (lambda x: np.zeros_like(x) > 0, lambda x: x > 0.2), "oracle": (lambda x: x > 0, lambda x: x > 0.2)}
    for k, p in pol.items():
        vals[k] = float(np.mean(gen(200000, p)[4]))
    return {"n": 1000, "b1": q["b1"], "b2": q["b2"], "values": vals}


def compute_discovery():
    r = rng(6206)
    rows = []
    for _ in range(30):
        s = F.random_linear_sem(10, 0.3, r, 2000)
        if not np.any(s["B"]):
            continue
        pc = F.pc_skeleton(s["X"], 0.01, 3)
        true = (s["B"] != 0) | (s["B"].T != 0)
        tp = int(np.sum(pc["adj"] & true) // 2)
        fp = int(np.sum(pc["adj"] & ~true) // 2)
        fn = int(np.sum(~pc["adj"] & true) // 2)
        Xs = (s["X"] - s["X"].mean(0)) / s["X"].std(0)
        rows.append({"edges": int(true.sum() // 2), "tp": tp, "fp": fp, "fn": fn, "vs": F.varsortability(s["X"], s["B"]),
                     "vs_std": F.varsortability(Xs, s["B"])})
    # faithfulness: a cancelling pair of paths X -> Y directly and X -> M -> Y
    n = 5000
    Xc = r.standard_normal(n)
    Mc = 1.0 * Xc + r.standard_normal(n)
    Yc = 1.0 * Xc - 1.0 * Mc + r.standard_normal(n)
    corr = float(np.corrcoef(Xc, Yc)[0, 1])
    return {"rows": rows, "vs": float(np.mean([q["vs"] for q in rows])), "vs_std": float(np.mean([q["vs_std"] for q in rows])),
            "recall": float(np.sum([q["tp"] for q in rows]) / np.sum([q["edges"] for q in rows])),
            "precision": float(np.sum([q["tp"] for q in rows]) / max(1, np.sum([q["tp"] + q["fp"] for q in rows]))), "cancel_corr": corr}


def compute_fusion():
    r = rng(6207)
    N = 20000
    age = r.uniform(20, 80, N)
    tau = 0.05 * (age - 20)  # the effect grows with age
    truth = float(tau.mean())
    reps = 200
    tr_est, tp_est, ess = [], [], []
    for _ in range(reps):
        sel = r.random(N) < 0.15 * np.exp(-(age - 20) / 15)  # a trial that recruits the young
        tr = np.flatnonzero(sel)
        z = r.random(len(tr)) < 0.5
        y = 1 + 0.02 * age[tr] + z * tau[tr] + r.standard_normal(len(tr))
        tr_est.append(float(y[z].mean() - y[~z].mean()))
        tg = r.choice(np.flatnonzero(~sel), 3000, replace=False)
        t = C.transport(y, z, age[tr][:, None], age[tg][:, None])
        tp_est.append(t["est"])
        ess.append(t["ess"])
    return {"n_trial": len(tr), "mean_age_trial": float(age[tr].mean()), "mean_age_target": float(age.mean()), "reps": reps,
            "trial": float(np.mean(tr_est)), "trial_sd": float(np.std(tr_est)), "transported": float(np.mean(tp_est)),
            "transported_sd": float(np.std(tp_est)), "ess": float(np.mean(ess)), "truth": truth, "tr_est": tr_est, "tp_est": tp_est}


def compute_surrogate():
    r = rng(6208)

    def world(n, t, bypass):
        S1 = 0.5 * t + r.standard_normal(n)
        S2 = 0.3 * t + 0.5 * S1 + r.standard_normal(n)
        Y = 2 * S1 + 1 * S2 + bypass * t + r.standard_normal(n)
        return np.column_stack([S1, S2]), Y
    out = {}
    for name, bypass in (("valid", 0.0), ("bypass", -1.0)):
        to = (r.random(5000) < 0.5).astype(float)  # observational sample with long-term outcomes (no treatment info used)
        So, Yo = world(5000, np.zeros(5000), bypass)
        te = (r.random(2000) < 0.5).astype(float)
        Se, Ye = world(2000, te, bypass)
        si = F.surrogate_index(So, Yo, Se, te)
        truth = 2 * 0.5 + 1 * (0.3 + 0.5 * 0.5) + bypass
        out[name] = {"est": si["effect"], "se": si["se"], "truth": truth}
        del to
    return out


def compute_board():
    p = load("proximal")
    q = load("policy")
    rows = [Row(62, r"OLS adjusting for both proxies", r"hidden confounder, \ $n = 1{,}000$", "coverage", 0.95, p["cov_naive"], p["reps"]),
            Row(62, r"proximal 2SLS", r"hidden confounder, \ $n = 1{,}000$", "coverage", 0.95, p["cov_prox"], p["reps"]),
            Row(62, r"policy value, \ learned and evaluated in-sample", r"EWM, \ AIPW scores, \ $n = 400$", "coverage", 0.95, q["cov_naive"], q["reps"]),
            Row(62, r"policy value, \ learned on one half, \ evaluated on the other", r"EWM, \ AIPW scores, \ $n = 400$", "coverage", 0.95, q["cov_split"], q["reps"])]
    save_rows(62, rows)
    return {"rows": [asdict(x) | {"verdict": x.verdict, "se": x.se} for x in rows]}


ITEMS = {
    "frontdoor": compute_frontdoor, "msm": compute_msm, "proximal": compute_proximal, "interference": compute_interference,
    "policy": compute_policy, "dtr": compute_dtr, "discovery": compute_discovery, "fusion": compute_fusion,
    "surrogate": compute_surrogate, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
