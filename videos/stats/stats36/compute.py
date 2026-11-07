"""Precompute every number in Part 36 of *Statistics, Built* ("Causes Without Experiments").

    OMP_NUM_THREADS=1 python -m videos.stats.stats36.compute            # everything missing (about ten minutes)
    python -m videos.stats.stats36.compute --force board

Results are cached in ``.cache/stats36/<name>.json``.  The NSW data (LaLonde 1986; Dehejia & Wahba 1999) are the
Museum's; the observational study, the clinic and the trial are the World's; the rest are seeded simulations.

Items:
    lalonde     the NSW experiment vs the PSID comparison group: covariates, naive and adjusted estimates
    simpson     the World's clinic resolved by the back-door formula
    colliders   Berkson's bias, M-bias and a mediator, by simulation
    frontdoor   the front-door formula recovering an effect with an unmeasured confounder
    obs         the World's observational study: naive, g-computation, matching, subclassification, IPW, AIPW; balance
    kang        Kang & Schafer's (2007) simulation: IPW, outcome regression and AIPW when models are wrong
    dml         nonlinear confounding: OLS vs AIPW with forests, with and without cross-fitting
    cate        heterogeneous effects in the World's trial: T-, X- and DR-learners and a causal forest vs the truth
    sens        an unmeasured confounder: the bias, Cinelli-Hazlett's robustness value, E-values; Rosenbaum's Gamma on NSW
    smoking     Doll & Hill's numbers; Cornfield's inequality and the E-value
    msm         a two-period treatment with time-varying confounding: naive vs IPW-MSM vs the g-formula
    lalonde2    LaLonde revisited: propensity scores, overlap, ATT estimators and a placebo test
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from functools import lru_cache
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import causal as CA
from explainer.stats.kit import conformal as CF
from explainer.stats.world import World

CACHE = Cache("stats36")
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


def ols_fit(X, y):
    D = np.column_stack([np.ones(len(X)), X])
    return np.linalg.lstsq(D, y, rcond=None)[0]


def ols_pred(b, X):
    return np.column_stack([np.ones(len(X)), X]) @ b


def ols_effect(y, t, X):
    """OLS of y on t and X: coefficient, conventional SE, t statistic and residual df."""
    D = np.column_stack([np.ones(len(y)), t.astype(float), X])
    b = np.linalg.lstsq(D, y, rcond=None)[0]
    e = y - D @ b
    dof = len(y) - D.shape[1]
    V = (e @ e / dof) * np.linalg.inv(D.T @ D)
    se = math.sqrt(V[1, 1])
    return float(b[1]), se, float(b[1] / se), dof


# ------------------------------------------------------------------------------------------------- the World's study


@lru_cache(maxsize=1)
def observational_pool():
    """Reuse the fixed World population; each study still draws fresh patients and assignments."""
    return World().trial


def obs_sample(g, n=3000, frailty=0.0):
    """n patients from the World's eligible pool; doctors prescribe with log-odds (base - 152)/6 + 0.04 (age - 65) +
    0.03 (bmi - 28), plus ``frailty`` times an unmeasured frailty u ~ N(0, 1), which also raises the untreated
    pressure by 3u mm Hg."""
    t = observational_pool()
    k = g.choice(len(t["pool"]), n, replace=False)
    base, age, bmi, fem = t["base_pool"][k], t["age_pool"][k], t["bmi_pool"][k], t["female_pool"][k].astype(float)
    u = g.standard_normal(n)
    y0 = t["y0_pool"][k] + 3.0 * frailty * u
    tau = t["tau_pool"][k]
    lo = (base - 152) / 6 + 0.04 * (age - 65) + 0.03 * (bmi - 28) + 0.8 * frailty * u
    e = 1 / (1 + np.exp(-lo))
    z = g.random(n) < e
    y = np.where(z, y0 + tau, y0)
    X = np.column_stack([base, age, bmi, fem])
    return {"X": X, "t": z, "y": y, "e": e, "tau": tau, "u": u, "ate": float(tau.mean()), "att": float(tau[z].mean())}


def obs_estimates(s):
    X, t, y = s["X"], s["t"], s["y"]
    ps = CA.propensity(X, t)
    b1, b0 = ols_fit(X[t], y[t]), ols_fit(X[~t], y[~t])
    mu1, mu0 = ols_pred(b1, X), ols_pred(b0, X)
    return {"naive": CA.diff_means(y, t), "gcomp": float(np.mean(mu1 - mu0)), "ipw": CA.ipw(y, t, ps),
            "aipw": CA.aipw(y, t, mu0, mu1, ps), "match_att": CA.ps_match(y, t, ps)["est"],
            "subclass": CA.subclassify(y, t, ps, 5)["est"], "ps": ps}


# ------------------------------------------------------------------------------------------------- items


def compute_lalonde():
    d = museum.nsw()
    e, p, tr = d["sample"] == "experiment", d["sample"] == "psid", d["treat"] == 1
    cov = ["age", "educ", "black", "hisp", "married", "nodegree", "re74", "re75"]
    means = {k: {"treated": float(d[k][e & tr].mean()), "exp_control": float(d[k][e & ~tr].mean()),
                 "psid": float(d[k][p].mean())} for k in cov}
    exp = CA.diff_means(d["re78"][e], tr[e], alpha=0.05)
    naive = CA.diff_means(np.r_[d["re78"][e & tr], d["re78"][p]], np.r_[np.ones((e & tr).sum(), bool), np.zeros(p.sum(), bool)], alpha=0.05)
    m = (e & tr) | p
    X = np.column_stack([d[k][m] for k in cov])
    est, se, _, _ = ols_effect(d["re78"][m], tr[m], X)
    return nest({"means": means, "exp": exp, "naive": naive, "ols": {"est": est, "se": se},
                 "n": {"treated": int((e & tr).sum()), "exp_control": int((e & ~tr).sum()), "psid": int(p.sum())}})


def compute_simpson():
    c = World().clinic
    sev, t, r = c["severe"], c["treated"], c["recovered"]
    out = {"overall": {"t": float(r[t].mean()), "c": float(r[~t].mean())}}
    for name, m in (("mild", ~sev), ("severe", sev)):
        out[name] = {"t": float(r[m & t].mean()), "c": float(r[m & ~t].mean()), "share": float(m.mean()),
                     "treated_share": float(t[m].mean())}
    adj = sum(out[k]["share"] * (out[k]["t"] - out[k]["c"]) for k in ("mild", "severe"))
    out["adjusted"] = float(adj)
    out["naive"] = out["overall"]["t"] - out["overall"]["c"]
    return nest(out)


def compute_colliders():
    g = rng(361)
    n = 200_000
    # Berkson: two independent diseases; admitted if either is severe enough
    a, b = g.standard_normal(n), g.standard_normal(n)
    adm = (a > 1.0) | (b > 1.0)
    berk = {"all": float(np.corrcoef(a, b)[0, 1]), "admitted": float(np.corrcoef(a[adm], b[adm])[0, 1]),
            "share": float(adm.mean())}
    # M-bias: T <- A -> M <- B -> Y, T -> Y with effect 1
    A, B = g.standard_normal(n), g.standard_normal(n)
    M = A + B + g.standard_normal(n)
    T = (A + g.standard_normal(n) > 0).astype(float)
    Y = 1.0 * T + 2 * B + g.standard_normal(n)
    unadj = ols_effect(Y, T.astype(bool), np.zeros((n, 0)))[0]
    adjM = ols_effect(Y, T.astype(bool), M[:, None])[0]
    adjMA = ols_effect(Y, T.astype(bool), np.column_stack([M, A]))[0]
    # a mediator: T -> M2 -> Y, total effect 1 + 0.5*2 = 2
    T2 = (g.random(n) < 0.5).astype(float)
    M2 = 0.5 * T2 + g.standard_normal(n)
    Y2 = 1.0 * T2 + 2.0 * M2 + g.standard_normal(n)
    tot = ols_effect(Y2, T2.astype(bool), np.zeros((n, 0)))[0]
    direct = ols_effect(Y2, T2.astype(bool), M2[:, None])[0]
    return nest({"berkson": berk, "mbias": {"truth": 1.0, "unadjusted": unadj, "adjust_M": adjM, "adjust_M_A": adjMA},
                 "mediator": {"total_truth": 2.0, "total": tot, "adjusted": direct}})


def compute_frontdoor():
    """Smoking T, tar M, cancer Y, with an unmeasured genotype U -> T and U -> Y; T affects Y only through M."""
    g = rng(362)
    n = 400_000
    U = g.random(n) < 0.3
    T = g.random(n) < np.where(U, 0.8, 0.2)
    M = g.random(n) < np.where(T, 0.9, 0.05)
    Y = g.random(n) < 0.05 + 0.15 * M + 0.2 * U
    naive = float(Y[T].mean() - Y[~T].mean())
    # truth: P(Y | do(T)) = sum_m P(m | T) E[Y | m] with U at its marginal
    def do(tv):
        pm = 0.9 if tv else 0.05
        return float(0.05 + 0.15 * pm + 0.2 * 0.3)
    truth = do(True) - do(False)
    # front-door: sum_m P(m|t) sum_t' P(Y|m,t') P(t')
    pt = T.mean()
    def fd(tv):
        s = 0.0
        for m in (False, True):
            pm = np.mean(M[T == tv] == m)
            inner = sum(np.mean(Y[(M == m) & (T == t2)]) * (pt if t2 else 1 - pt) for t2 in (False, True))
            s += pm * inner
        return float(s)
    front = fd(True) - fd(False)
    return nest({"naive": naive, "truth": truth, "front": front})


def compute_obs():
    g = rng(363)
    s = obs_sample(g, 3000)
    r = obs_estimates(s)
    X, t = s["X"], s["t"]
    names = ["baseline pressure", "age", "BMI", "female"]
    ps = r["ps"]
    w = np.where(t, 1 / ps, 1 / (1 - ps))
    bal = [{"name": nm, "before": CA.smd(X[:, j], t), "after": CA.smd(X[:, j], t, w)} for j, nm in enumerate(names)]
    h1 = np.histogram(ps[t], bins=20, range=(0, 1))[0]
    h0 = np.histogram(ps[~t], bins=20, range=(0, 1))[0]
    return nest({"ate": s["ate"], "att": s["att"], "share": float(t.mean()), "naive": r["naive"], "gcomp": r["gcomp"],
                 "ipw": r["ipw"], "aipw": {k: v for k, v in r["aipw"].items() if k != "psi"}, "match_att": r["match_att"],
                 "subclass": r["subclass"], "balance": bal, "h_t": h1, "h_c": h0})


def _ks(g, n=1000):
    Z = g.standard_normal((n, 4))
    y = 210 + 27.4 * Z[:, 0] + 13.7 * (Z[:, 1] + Z[:, 2] + Z[:, 3]) + g.standard_normal(n)
    pi = 1 / (1 + np.exp(-(-Z[:, 0] + 0.5 * Z[:, 1] - 0.25 * Z[:, 2] - 0.1 * Z[:, 3])))
    r = g.random(n) < pi  # observed
    X = np.column_stack([np.exp(Z[:, 0] / 2), Z[:, 1] / (1 + np.exp(Z[:, 0])) + 10, (Z[:, 0] * Z[:, 2] / 25 + 0.6) ** 3,
                         (Z[:, 1] + Z[:, 3] + 20) ** 2])
    return Z, X, y, r


def _ks_estimates(Z, X, y, r):
    """Estimates of E[Y] (= 210) with Y observed when r; 'right' models use Z, 'wrong' use X."""
    out = {}
    for name, F in (("right", Z), ("wrong", X)):
        F2 = (F - F.mean(0)) / F.std(0)
        out[f"ps_{name}"] = np.clip(CA.propensity(F2, r), 1e-6, 1)
        b = ols_fit(F2[r], y[r])
        out[f"or_{name}"] = ols_pred(b, F2)
    n = len(y)
    res = {}
    for ps_n in ("right", "wrong"):
        e = out[f"ps_{ps_n}"]
        w = r / e
        res[f"ipw_{ps_n}"] = float(np.sum(w * y) / np.sum(w))
        for or_n in ("right", "wrong"):
            m = out[f"or_{or_n}"]
            psi = m + r * (y - m) / e
            res[f"aipw_{ps_n}_{or_n}"] = (float(psi.mean()), float(psi.std(ddof=1) / math.sqrt(n)))
    for or_n in ("right", "wrong"):
        res[f"or_{or_n}"] = float(out[f"or_{or_n}"].mean())
    res["max_w_wrong"] = float((1 / out["ps_wrong"][r]).max())
    return res


def compute_kang():
    g = rng(364)
    reps = 1000
    keys = ["ipw_right", "ipw_wrong", "or_right", "or_wrong"]
    akeys = ["aipw_right_right", "aipw_right_wrong", "aipw_wrong_right", "aipw_wrong_wrong"]
    vals = {k: [] for k in keys + akeys}
    cover = {k: [] for k in akeys}
    maxw = []
    q = stats.norm.ppf(0.95)
    for _ in range(reps):
        Z, X, y, r = _ks(g)
        e = _ks_estimates(Z, X, y, r)
        for k in keys:
            vals[k].append(e[k])
        for k in akeys:
            est, se = e[k]
            vals[k].append(est)
            cover[k].append(abs(est - 210) <= q * se)
        maxw.append(e["max_w_wrong"])
    out = {k: {"bias": float(np.mean(v) - 210), "rmse": float(np.sqrt(np.mean((np.array(v) - 210) ** 2))),
               "sd": float(np.std(v))} for k, v in vals.items()}
    for k in akeys:
        out[k]["cover"] = float(np.mean(cover[k]))
    out["median_max_weight"] = float(np.median(maxw))
    out["max_max_weight"] = float(np.max(maxw))
    out["reps"] = reps
    return nest(out)


def _dml_data(g, n=1000):
    X = g.random((n, 5))
    lo = 2 * np.sin(np.pi * X[:, 0] * X[:, 1]) + 4 * (X[:, 2] - 0.5) ** 2 - 1.2
    e = 1 / (1 + np.exp(-lo))
    t = g.random(n) < e
    mu0 = 10 * np.sin(np.pi * X[:, 0] * X[:, 1]) + 20 * (X[:, 2] - 0.5) ** 2 + 10 * X[:, 3]
    tau = 2 + 2 * X[:, 4]
    y = mu0 + t * tau + g.standard_normal(n)
    return X, t, y, float(tau.mean())


def _forest_reg(g):
    def f(Xtr, ytr, Xte):
        return CF.Forest(Xtr, ytr, B=60, mtry=3, min_leaf=5, rng=g).predict(Xte)
    return f


def _forest_prob(g):
    def f(Xtr, ttr, Xte):
        return CF.Forest(Xtr, ttr, B=60, mtry=3, min_leaf=10, rng=g).predict(Xte)
    return f


def _dml_rep(g):
    X, t, y, sample_ate = _dml_data(g)
    ate = 3.0  # superpopulation ATE, matching the score's influence-function SE
    q = stats.norm.ppf(0.95)
    o = ols_effect(y, t, X)
    ols_hit = abs(o[0] - ate) <= q * o[1]
    r = CA.dml_ate(y, t, X, _forest_reg(g), _forest_prob(g), K=2, rng=g)
    dml_hit = r["lo"] <= ate <= r["hi"]
    # the same AIPW with forests fitted to all the data (no cross-fitting)
    fr, fp = _forest_reg(g), _forest_prob(g)
    mu1, mu0 = fr(X[t], y[t], X), fr(X[~t], y[~t], X)
    e = np.clip(fp(X, t.astype(float), X), 0.01, 0.99)
    a = CA.aipw(y, t, mu0, mu1, e)
    nocf_hit = a["lo"] <= ate <= a["hi"]
    return (o[0], ols_hit), (r["est"], dml_hit, r["se"]), (a["est"], nocf_hit, a["se"]), ate


def compute_dml():
    g = rng(365)
    reps = 150
    res = [_dml_rep(g) for _ in range(reps)]
    ate = float(np.mean([r[3] for r in res]))
    o = np.array([r[0][0] for r in res])
    dm = np.array([r[1][0] for r in res])
    nc = np.array([r[2][0] for r in res])
    return nest({"reps": reps, "ate": ate, "target": "superpopulation ATE = 3",
                 "replicates": [{"ols_est":r[0][0],"ols_hit":r[0][1],"dml_est":r[1][0],"dml_hit":r[1][1],
                                 "dml_se":r[1][2],"nocf_est":r[2][0],"nocf_hit":r[2][1],"nocf_se":r[2][2]} for r in res],
                 "ols": {"bias": float(o.mean() - ate), "cover": float(np.mean([r[0][1] for r in res]))},
                 "dml": {"bias": float(dm.mean() - ate), "sd": float(dm.std()), "mean_se": float(np.mean([r[1][2] for r in res])),
                         "cover": float(np.mean([r[1][1] for r in res]))},
                 "nocf": {"bias": float(nc.mean() - ate), "sd": float(nc.std()), "mean_se": float(np.mean([r[2][2] for r in res])),
                          "cover": float(np.mean([r[2][1] for r in res]))}})


def compute_cate():
    t = World().trial
    g = rng(366)
    X = np.column_stack([t["base"], t["age"], t["bmi"], t["female"].astype(float)])
    z = np.zeros(len(X), bool)
    z[g.choice(len(X), len(X) // 2, replace=False)] = True
    y = np.where(z, t["y1"], t["y0"])
    # Hold out all trial participants. The benchmark uses latent true pressure;
    # learners only observe noisy recorded pressure, so this is a structural
    # effect benchmark, not exactly the CATE given their recorded covariates.
    eligible = np.setdiff1d(np.arange(len(t["pool"])), t["pos"])
    k = g.choice(eligible, 2000, replace=False)
    Xg = np.column_stack([t["base_pool"][k], t["age_pool"][k], t["bmi_pool"][k], t["female_pool"][k].astype(float)])
    truth = -(9 + 0.3 * (t["sbp_pool"][k] - 150) + 0.08 * (t["age_pool"][k] - 60))
    fr = _forest_reg(g)
    preds = {"T-learner": CA.t_learner(X, y, z, Xg, fr), "X-learner": CA.x_learner(X, y, z, Xg, fr, 0.5),
             "DR-learner": CA.dr_learner(X, y, z, Xg, fr, 0.5, rng=g),
             "causal forest": CA.CausalForest(X, y, z.astype(float), B=200, min_leaf=40, rng=g).predict(Xg)}
    # a linear model with interactions, which happens to be the right shape
    D = np.column_stack([X, z, X * z[:, None]])
    b = np.linalg.lstsq(np.column_stack([np.ones(len(D)), D]), y, rcond=None)[0]
    preds["linear, interacted"] = Xg @ b[6:10] + b[5]
    ate = float(np.mean(y[z]) - np.mean(y[~z]))
    out = {"rmse_const": float(np.sqrt(np.mean((truth - ate) ** 2))), "sd_truth": float(truth.std()), "ate": ate,
           "test_training_overlap": int(np.intersect1d(k,t["pos"]).size),
           "benchmark": "latent systematic effect; learners see noisy recorded pressure"}
    out["learners"] = {}
    for k_, p in preds.items():
        dec = np.quantile(p, np.linspace(0, 1, 11))
        bins = np.clip(np.searchsorted(dec, p, side="right") - 1, 0, 9)
        out["learners"][k_] = {"rmse": float(np.sqrt(np.mean((p - truth) ** 2))), "corr": float(np.corrcoef(p, truth)[0, 1]),
                               "dec_pred": [float(p[bins == b_].mean()) for b_ in range(10)],
                               "dec_true": [float(truth[bins == b_].mean()) for b_ in range(10)]}
    return nest(out)


def disjoint_ps_pairs(t, ps, caliper_sd=0.2):
    """Outcome-blind minimum-distance pairing, without reused controls.

    Enforce a logit-score caliper after assignment; unmatched treated units are
    omitted, so the matched sample, rather than the full ATT, is the target.
    """
    from scipy.optimize import linear_sum_assignment
    t, ps = np.asarray(t, bool), np.clip(np.asarray(ps, float),1e-12,1-1e-12)
    logit = np.log(ps/(1-ps))
    treated, control = np.flatnonzero(t), np.flatnonzero(~t)
    distance = np.abs(logit[treated,None]-logit[control][None,:])
    i,j=linear_sum_assignment(distance)
    keep=distance[i,j] <= caliper_sd*logit.std(ddof=1)
    return treated[i[keep]],control[j[keep]]


def signed_rank_bound(d, gamma):
    """Exact one-sided worst-case signed-rank tail for disjoint pairs.

    At the extremal assignment probabilities all positive-rank signs have
    probability Gamma/(1+Gamma). Doubled ranks handle average-rank ties.
    """
    d=np.asarray(d,float);d=d[d!=0]
    if not len(d):return 1.0
    ranks=np.rint(2*stats.rankdata(np.abs(d))).astype(int)
    observed=int(ranks[d>0].sum())
    p=gamma/(1+gamma)
    probabilities=np.array([1.0])
    for rank in ranks:
        updated=np.zeros(len(probabilities)+rank)
        updated[:len(probabilities)]+=(1-p)*probabilities
        updated[rank:]+=p*probabilities
        probabilities=updated
    return float(probabilities[observed:].sum())


def compute_sens():
    g = rng(367)
    s = obs_sample(g, 3000, frailty=1.0)
    est, se, tstat, dof = ols_effect(s["y"], s["t"], s["X"])
    rv = CA.robustness_value(tstat, dof)
    rv_sig = CA.robustness_value(tstat, dof, alpha=0.05)
    # the unmeasured confounder's actual partial R^2 with treatment and with outcome (given X)
    def pr2(y_, extra):
        D0 = np.column_stack([np.ones(len(y_)), extra])
        e0 = y_ - D0 @ np.linalg.lstsq(D0, y_, rcond=None)[0]
        D1 = np.column_stack([D0, s["u"]])
        e1 = y_ - D1 @ np.linalg.lstsq(D1, y_, rcond=None)[0]
        return float(1 - (e1 @ e1) / (e0 @ e0))
    r2_tu = pr2(s["t"].astype(float), s["X"])
    r2_yu = pr2(s["y"], np.column_stack([s["X"], s["t"].astype(float)]))
    # with u measured
    est_u = ols_effect(s["y"], s["t"], np.column_stack([s["X"], s["u"]]))[0]
    # Rosenbaum on the World's study: treated patients matched to controls on the measured covariates' propensity
    psw = CA.propensity(s["X"], s["t"])
    tw,cw = disjoint_ps_pairs(s["t"], psw)
    dw = -(s["y"][tw]-s["y"][cw])  # pressure reduction, independent disjoint pairs
    gw = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0]
    rbw = {str(gm): signed_rank_bound(dw, gm) for gm in gw}
    gstar = next((gm for gm in np.arange(1.0, 20.0, 0.1) if signed_rank_bound(dw, gm) > 0.05), None)
    # and on NSW: PSID controls matched to the treated on the propensity score
    d = museum.nsw()
    e_, p_, tr = d["sample"] == "experiment", d["sample"] == "psid", d["treat"] == 1
    m = (e_ & tr) | p_
    Xn = nsw_design(d, m)
    ps = CA.propensity(Xn, tr[m], ridge=1e-3)
    tn,cn = disjoint_ps_pairs(tr[m],ps)
    diffs = d["re78"][m][tn] - d["re78"][m][cn]
    gam = [1.0, 1.1, 1.2, 1.3, 1.5, 2.0]
    rb = {str(gm): signed_rank_bound(diffs, gm) for gm in gam}
    return nest({"ate": s["ate"], "est": est, "se": se, "t": tstat, "dof": dof, "rv": rv, "rv_sig": rv_sig,
                 "r2_tu": r2_tu, "r2_yu": r2_yu, "est_with_u": est_u, "rosen": rb, "match_att": float(diffs.mean()),
                 "rosen_world": rbw, "gamma_star": float(gstar) if gstar else None, "world_match": float(-dw.mean()),
                 "world_pairs": len(tw), "nsw_pairs": len(tn), "reused_controls": 0,
                 "caliper_logit_sd": 0.2,
                 "pair_mean": float(diffs.mean())})


def nsw_design(d, m):
    """Dehejia & Wahba's propensity covariates: age, age^2, education, education^2, black, hispanic, married, no
    degree, re74, re75, zero-earnings indicators, standardized."""
    cols = [d["age"], d["age"] ** 2, d["educ"], d["educ"] ** 2, d["black"], d["hisp"], d["married"], d["nodegree"],
            d["re74"] / 1000, d["re75"] / 1000, (d["re74"] == 0).astype(float), (d["re75"] == 0).astype(float)]
    X = np.column_stack([c[m] for c in cols]).astype(float)
    return (X - X.mean(0)) / X.std(0)


def compute_smoking():
    return nest({"cases_smokers": 647, "cases": 649, "controls_smokers": 622, "controls": 649, "rr": 9.0,
                 "e_value_9": CA.e_value(9.0), "cornfield": CA.cornfield_ratio(9.0),
                 "odds_ratio": float((647 * 27) / (2 * 622))})


def compute_msm():
    """Two periods: A0 (random), L1 (a health measure worsened by low A0 and raising A1), A1, Y.  Y = 10 - 2 A0 - 2 A1
    + 3 L1 + noise; L1 = 1 - A0 + U + noise with U unmeasured, U also raising Y.  The joint effect of always vs never
    treating is E[Y(1,1)] - E[Y(0,0)] = -4 - 3 (since A0 lowers L1 by 1, which lowers Y by 3) = -7."""
    g = rng(368)
    n = 200_000
    U = g.standard_normal(n)
    A0 = (g.random(n) < 0.5).astype(float)
    L1 = 1 - A0 + 0.7 * U + 0.5 * g.standard_normal(n)
    p1 = 1 / (1 + np.exp(-(-0.5 + 1.2 * L1)))
    A1 = (g.random(n) < p1).astype(float)
    Y = 10 - 2 * A0 - 2 * A1 + 3 * L1 + 2 * U + g.standard_normal(n)
    truth = -7.0
    # naive: regress Y on A0, A1 (no adjustment): confounded for A1
    D = np.column_stack([np.ones(n), A0, A1])
    b = np.linalg.lstsq(D, Y, rcond=None)[0]
    naive = float(b[1] + b[2])
    # adjust for L1: blocks A0's effect through L1 and opens A0 -> L1 <- U -> Y
    D2 = np.column_stack([np.ones(n), A0, A1, L1])
    b2 = np.linalg.lstsq(D2, Y, rcond=None)[0]
    adj = float(b2[1] + b2[2])
    # IPW MSM with stabilized weights
    ph = 1 / (1 + np.exp(-CA.logit_fit(L1[:, None], A1) @ np.vstack([np.ones(n), L1])))
    pa1 = np.where(A1 == 1, ph, 1 - ph)
    marg = np.where(A1 == 1, A1.mean(), 1 - A1.mean())
    sw = marg / pa1
    W = np.sqrt(sw)
    bm = np.linalg.lstsq(D * W[:, None], Y * W, rcond=None)[0]
    msm = float(bm[1] + bm[2])
    # g-formula: E[Y(a0,a1)] = sum over L1 of E[Y | a0, L1, a1] f(L1 | a0)  (linear models, Monte Carlo over L1)
    def gform(a0, a1):
        Lm = np.linalg.lstsq(np.column_stack([np.ones(n), A0]), L1, rcond=None)[0]
        Ym = b2
        l1 = Lm[0] + Lm[1] * a0 + (L1 - (Lm[0] + Lm[1] * A0))  # residual resampling
        return float(np.mean(Ym[0] + Ym[1] * a0 + Ym[2] * a1 + Ym[3] * l1))
    gf = gform(1, 1) - gform(0, 0)
    return nest({"truth": truth, "naive": naive, "adjusted": adj, "msm": msm, "gformula": gf,
                 "sw_mean": float(sw.mean()), "sw_max": float(sw.max())})


def compute_lalonde2():
    d = museum.nsw()
    e_, p_, tr = d["sample"] == "experiment", d["sample"] == "psid", d["treat"] == 1
    m = (e_ & tr) | p_
    y, t = d["re78"][m], tr[m]
    X = nsw_design(d, m)
    ps = CA.propensity(X, t, ridge=1e-3)
    h1 = np.histogram(ps[t], bins=20, range=(0, 1))[0]
    h0 = np.histogram(ps[~t], bins=20, range=(0, 1))[0]
    # overlap: drop controls below the smallest treated score and treated above the largest control score
    lo, hi = ps[t].min(), ps[~t].max()
    keep = (ps >= lo) & (ps <= hi)
    Xr = np.column_stack([d[k][m] for k in ("age", "educ", "black", "hisp", "married", "nodegree", "re74", "re75")]).astype(float)
    b0 = ols_fit(Xr[~t], y[~t])
    reg_att = float(np.mean(y[t] - ols_pred(b0, Xr[t])))
    out = {"exp": float(d["re78"][e_ & tr].mean() - d["re78"][e_ & ~tr].mean()), "naive": float(y[t].mean() - y[~t].mean()),
           "ols": ols_effect(y, t, Xr)[0], "reg_att": reg_att, "match": CA.ps_match(y, t, ps)["est"],
           "ipw_att": CA.ipw(y, t, np.clip(ps, 1e-4, 1 - 1e-4), "att")["est"],
           "subclass": CA.subclassify(y[keep], t[keep], ps[keep], 5, "att")["est"],
           "ipw_att_overlap": CA.ipw(y[keep], t[keep], np.clip(ps[keep], 1e-4, 1 - 1e-4), "att")["est"],
           "n_kept_controls": int((keep & ~t).sum()), "n_controls": int((~t).sum()),
           "share_controls_below_01": float(np.mean(ps[~t] < 0.1)), "share_treated_above_05": float(np.mean(ps[t] > 0.5)),
           "h_t": h1, "h_c": h0}
    # placebo: 1975 earnings as the outcome, with 1974 earnings among the covariates (Imbens & Xu 2024)
    Xp = X[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]]  # drop re75 and its zero indicator
    psp = CA.propensity(Xp, t, ridge=1e-3)
    out["placebo_psid"] = CA.ps_match(d["re75"][m], t, psp)["est"]
    out["placebo_exp"] = float(d["re75"][e_ & tr].mean() - d["re75"][e_ & ~tr].mean())
    return nest(out)


def compute_board():
    rows = []
    g = rng(370)
    reps = 500
    cn, ci, ca, cu = [], [], [], []
    q = stats.norm.ppf(0.95)
    for _ in range(reps):
        s = obs_sample(g, 2000)
        r = obs_estimates(s)
        ate = s["ate"]
        cn.append(r["naive"]["lo"] <= ate <= r["naive"]["hi"])
        ci.append(r["ipw"]["lo"] <= ate <= r["ipw"]["hi"])
        ca.append(r["aipw"]["lo"] <= ate <= r["aipw"]["hi"])
        su = obs_sample(g, 2000, frailty=1.0)
        est, se, _, _ = ols_effect(su["y"], su["t"], su["X"])
        cu.append(abs(est - su["ate"]) <= q * se)
    rows.append(Row(36, r"naive difference in means", r"World: \ doctors choose, \ $n = 2{,}000$", "coverage", 0.9, float(np.mean(cn)), reps))
    rows.append(Row(36, r"IPW, \ logistic propensity", r"World: \ doctors choose, \ $n = 2{,}000$", "coverage", 0.9, float(np.mean(ci)), reps))
    rows.append(Row(36, r"AIPW, \ both models fitted", r"World: \ doctors choose, \ $n = 2{,}000$", "coverage", 0.9, float(np.mean(ca)), reps))
    rows.append(Row(36, r"regression adjustment, \ unmeasured frailty", r"World: \ doctors also see frailty", "coverage", 0.9, float(np.mean(cu)), reps))
    ks = load("kang")
    rows.append(Row(36, r"AIPW, \ PS right, \ outcome wrong", r"Kang \& Schafer (2007), \ $n = 1{,}000$", "coverage", 0.9,
                    ks["aipw_right_wrong"]["cover"], ks["reps"]))
    rows.append(Row(36, r"AIPW, \ both models wrong", r"Kang \& Schafer (2007), \ $n = 1{,}000$", "coverage", 0.9,
                    ks["aipw_wrong_wrong"]["cover"], ks["reps"]))
    dm = load("dml")
    rows.append(Row(36, r"OLS adjustment, \ linear", r"nonlinear confounding, \ $n = 1{,}000$", "coverage", 0.9, dm["ols"]["cover"], dm["reps"]))
    rows.append(Row(36, r"AIPW with forests, \ no cross-fitting", r"nonlinear confounding, \ $n = 1{,}000$", "coverage", 0.9, dm["nocf"]["cover"], dm["reps"]))
    rows.append(Row(36, r"DML: \ forests, \ cross-fitted", r"nonlinear confounding, \ $n = 1{,}000$", "coverage", 0.9, dm["dml"]["cover"], dm["reps"]))
    save_rows(36, rows)
    return nest({"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


ITEMS = {
    "lalonde": compute_lalonde, "simpson": compute_simpson, "colliders": compute_colliders, "frontdoor": compute_frontdoor,
    "obs": compute_obs, "kang": compute_kang, "dml": compute_dml, "cate": compute_cate, "sens": compute_sens,
    "smoking": compute_smoking, "msm": compute_msm, "lalonde2": compute_lalonde2, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
