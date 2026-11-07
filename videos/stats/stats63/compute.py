"""Precompute every number in Part 63 of *Statistics, Built* ("Privacy and Fairness").

    OMP_NUM_THREADS=1 python -m videos.stats.stats63.compute            # everything missing (a few minutes)
    python -m videos.stats.stats63.compute --force board

Results are cached in ``.cache/stats63/<name>.json``.  NHANES, the Wisconsin biopsies and ProPublica's COMPAS data are
the Museum's; everything else is exact arithmetic or a seeded simulation.

Items:
    unique     NHANES: how many adults a few published attributes single out
    mechanisms Laplace and Gaussian noise: classical against analytic Gaussian calibration
    tradeoff   trade-off curves of (eps, 0)-DP, the Laplace mechanism and 1-GDP, against a simulated membership attack
    accounting the eps of k Gaussian releases under basic, advanced, Renyi and zCDP accounting
    cost       the mean of bits under central and local DP, against n
    inference  a Laplace-noised proportion: naive against noise-aware intervals over a grid of n and eps
    census     a TopDown toy: noisy block counts projected to nonnegative counts with the right total
    dpsgd      noisy gradient descent for logistic regression on the biopsies: test accuracy against the privacy budget
    compas     ProPublica's COMPAS data: base rates, error rates and calibration by race; Chouldechova's identity
    multical   multicalibration of a COMPAS risk model across race, sex and age groups
    cfair      counterfactual fairness in a simulated policing model
    board      Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from . import checked as P

CACHE = Cache("stats63")
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


def compute_unique():
    d = museum.nhanes()
    sbp = np.nanmean(np.column_stack([d["sbp1"], d["sbp2"], d["sbp3"]]), axis=1)
    ok = np.isfinite(sbp) & np.isfinite(d["bmi"]) & np.isfinite(d["age"]) & np.isfinite(d["sex"])
    age, sex, bmi, s = d["age"][ok], d["sex"][ok], d["bmi"][ok], sbp[ok]
    combos = [("age", [age]), ("age, sex", [age, sex]), ("age, sex, BMI", [age, sex, np.round(bmi, 1)]),
              ("age, sex, BMI, blood pressure", [age, sex, np.round(bmi, 1), np.round(s)])]
    rows = []
    for name, cols in combos:
        keys = list(zip(*[c.tolist() for c in cols]))
        from collections import Counter
        cnt = Counter(keys)
        rows.append({"attrs": name, "unique": float(np.mean([cnt[k] == 1 for k in keys])), "classes": len(cnt)})
    return {"n": int(ok.sum()), "rows": rows}


def compute_mechanisms():
    eps = [0.1, 0.25, 0.5, 1.0, 2.0]
    delta = 1e-5
    return {"eps": eps, "delta": delta, "classic": [P.gaussian_sigma_classic(1, e, delta) for e in eps],
            "analytic": [P.gaussian_sigma_analytic(1, e, delta) for e in eps], "laplace_sd": [math.sqrt(2) / e for e in eps]}


def compute_tradeoff():
    r = rng(6301)
    a = np.linspace(0, 1, 201)
    m = P.membership_attack_roc(100, 0.01, 40000, r)
    return {"alpha": a, "dp1": P.tradeoff_eps_delta(a, 1.0), "lap1": P.tradeoff_laplace(a, 1.0), "gdp1": P.tradeoff_gaussian(a, 1.0),
            "attack_fpr": m["fpr"], "attack_fnr": 1 - m["tpr"], "mu": m["mu"]}


def compute_accounting():
    sigma, delta = 5.0, 1e-5
    ks = [1, 3, 10, 30, 100, 300, 1000]
    one = None
    # (eps, delta/k) for one release, by the exact Gaussian delta: find eps with delta_one = delta / (2k)
    from scipy import optimize
    out = {"ks": ks, "sigma": sigma, "delta": delta, "basic": [], "advanced": [], "rdp": [], "zcdp": []}
    for k in ks:
        d1 = delta / (2 * k)
        e_one = optimize.brentq(lambda e: P.gaussian_delta(sigma, 1, e) - d1, 1e-6, 50)
        out["basic"].append(k * e_one)
        out["advanced"].append(P.advanced_composition(e_one, k, delta / 2, d1)[0])
        out["rdp"].append(P.rdp_gaussian_eps(1, sigma, k, delta))
        out["zcdp"].append(P.zcdp_to_dp(k * P.zcdp_gaussian(1, sigma), delta))
        one = e_one if one is None else one
    out["census_rho"] = 2.63
    out["census_eps"] = P.zcdp_to_dp(2.63, 1e-10)
    return out


def compute_cost():
    r = rng(6302)
    ns = [100, 300, 1000, 3000, 10000]
    rows = []
    for n in ns:
        m = P.mean_mse_central_local(n, 1.0, 20000, r)
        rows.append({"n": n, **m, "sampling": 0.3 * 0.7 / n, "central_exact": 0.3 * 0.7 / n + 2 / n ** 2})
    return {"eps": 1.0, "p": 0.3, "rows": rows}


def compute_inference():
    r = rng(6303)
    grid = []
    for n in (100, 300, 1000, 3000):
        for eps in (0.1, 0.5, 1.0):
            cn = ca = 0
            reps = 1000
            for _ in range(reps):
                x = (r.random(n) < 0.3).astype(int)
                o = P.private_proportion(x, eps, r)
                cn += o["naive"][0] <= 0.3 <= o["naive"][1]
                ca += o["aware"][0] <= 0.3 <= o["aware"][1]
            grid.append({"n": n, "eps": eps, "naive": cn / reps, "aware": ca / reps, "reps": reps, "mcse_naive": math.sqrt((cn/reps)*(1-cn/reps)/reps), "mcse_aware": math.sqrt((ca/reps)*(1-ca/reps)/reps)})
    reps = 2000
    cn = ca = 0
    for _ in range(reps):
        x = (r.random(1000) < 0.3).astype(int)
        o = P.private_proportion(x, 0.1, r)
        cn += o["naive"][0] <= 0.3 <= o["naive"][1]
        ca += o["aware"][0] <= 0.3 <= o["aware"][1]
    return {"grid": grid, "board_n": 1000, "board_eps": 0.1, "board_reps": reps, "board_naive": cn / reps, "board_aware": ca / reps}


def compute_census():
    r = rng(6304)
    m = 400
    true = np.maximum(np.round(np.exp(r.normal(3.0, 1.4, m))), 0)
    total = true.sum()
    sigma = 4.0  # rounded continuous Gaussian; not a discrete Gaussian mechanism
    reps = 200
    post, raw = [], []
    for _ in range(reps):
        noisy = true + np.round(r.normal(0, sigma, m))
        raw.append(noisy)
        post.append(P.integer_total_projection(noisy, total))
    post, raw = np.array(post), np.array(raw)
    bins = [0, 5, 20, 100, 1e9]
    rows = []
    for lo, hi in zip(bins[:-1], bins[1:]):
        k = (true >= lo) & (true < hi)
        rows.append({"lo": lo, "hi": hi, "n": int(k.sum()), "bias_raw": float((raw[:, k] - true[k]).mean()),
                     "bias_post": float((post[:, k] - true[k]).mean()), "mcse_post": float((post[:, k]-true[k]).mean(1).std(ddof=1)/np.sqrt(reps))})
    return {"m": m, "sigma": sigma, "total": float(total), "rows": rows, "true": true, "post0": post[0], "raw0": raw[0],
            "neg_raw": float(np.mean(raw < 0)), "neg_post": float(np.mean(post < 0)), "max_total_error": float(np.max(abs(post.sum(1)-total))), "noise_law": "rounded continuous Gaussian; illustrative fixed-public-total projection", "reps": reps}


def compute_dpsgd():
    r=rng(6305);X,y,_=museum.breast_cancer();Z=P.fixed_features(X)
    splits=[r.permutation(len(y)) for _ in range(10)]
    out=[]
    for rho in [.003,.01,.03,.1,.3,1.,float('inf')]:
        acc=[]
        for o in splits:
            tr,te=o[:400],o[400:]
            w=P.dp_logistic_gd(Z[tr],y[tr],rho,60,1.,2.,r)['w']
            acc.append(float(np.mean(((Z[te]@w)>0)==y[te])))
        out.append(dict(rho=rho if math.isfinite(rho) else None,eps=P.zcdp_to_dp(rho,1e-5) if math.isfinite(rho) else None,acc=float(np.mean(acc)),sd=float(np.std(acc,ddof=1)),accuracy=acc))
    return dict(n_train=400,n_test=len(y)-400,rows=out,adjacency='fixed-size replace-one',sensitivity=2.,preprocessing='fixed public feature units; clipped pointwise; no fitted centering/scaling',release_scope='One model per budget. Accuracy and repeated fits are public-data diagnostics, not a jointly private release.')



def compute_compas():
    d = museum.compas()
    m = np.isin(d["race"], ["African-American", "Caucasian"])
    race = np.where(d["race"][m] == "African-American", "Black", "white")
    s, y = d["decile_score"][m], d["two_year_recid"][m]
    rates = P.group_rates(s, y, race, 5)
    cal = P.calibration_by_group(s, y, race, np.arange(1, 12))
    chk = {g: P.chouldechova_fpr(v["base"], v["ppv"], v["fnr"]) for g, v in rates.items()}
    return {"n": int(m.sum()), "rates": rates, "cal": cal, "chouldechova": chk, "n_all": len(d["age"])}


def _logit(X, y, iters=50, ridge=1e-3):
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w))
        g = X.T @ (p - y) + ridge * w
        H = (X * (p * (1 - p))[:, None]).T @ X + ridge * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w


def compute_multical():
    d = museum.compas()
    y = d["two_year_recid"].astype(float)
    X = np.column_stack([np.ones(len(y)), d["age"] / 10, np.log1p(d["priors_count"])])
    G = {"Black": d["race"] == "African-American", "white": d["race"] == "Caucasian", "women": d["sex"] == "Female", "under 25": d["age"] < 25}
    names = list(G)
    r = rng(6306)
    before, after, ins_b, ins_a = [], [], [], []
    per_b = {k: [] for k in names}
    per_a = {k: [] for k in names}
    hist = None
    for _ in range(20):
        o = r.permutation(len(y))
        tr, te = o[: len(y) // 2], o[len(y) // 2:]
        w = _logit(X[tr], y[tr])
        pred = 1 / (1 + np.exp(-X @ w))
        gtr, gte = [G[k][tr] for k in names], [G[k][te] for k in names]
        mc = P.multicalibrate(pred[tr], y[tr], gtr, alpha=0.02, n_bins=5, max_iter=300, min_n=100)
        hist = mc["history"] if hist is None else hist
        tp = P.apply_patches(pred[te], gte, mc["patches"], 5)
        before.append(P.weighted_calibration_gap(pred[te], y[te], gte))
        after.append(P.weighted_calibration_gap(tp, y[te], gte))
        ins_b.append(P.weighted_calibration_gap(pred[tr], y[tr], gtr))
        ins_a.append(P.weighted_calibration_gap(mc["pred"], y[tr], gtr))
        for k, g in zip(names, gte):
            per_b[k].append(P.weighted_calibration_gap(pred[te], y[te], [g]))
            per_a[k].append(P.weighted_calibration_gap(tp, y[te], [g]))
    return {"names": names, "splits": 20, "train_hist": hist, "metric_scope": "size-weighted mean absolute cell residual; not worst-cell multicalibration", "paired_gap_mcse": float(np.std(np.array(after)-before,ddof=1)/np.sqrt(20)), "split_before": before, "split_after": after, "before": float(np.mean(before)), "after": float(np.mean(after)),
            "in_before": float(np.mean(ins_b)), "in_after": float(np.mean(ins_a)),
            "per": {k: {"before": float(np.mean(per_b[k])), "after": float(np.mean(per_a[k])), "paired_gap_mcse": float(np.std(np.array(per_a[k])-per_b[k],ddof=1)/np.sqrt(20))} for k in names}}


def compute_cfair():
    r=rng(6317)
    def sample(n):
        A=(r.random(n)<.5).astype(float);U=r.standard_normal(n);noise=r.standard_normal(n)
        P=1.5+U+1.2*A+noise  # continuous prior-arrest measurement index, not a rounded count
        risk=1/(1+np.exp(-(-.5+.9*U)));Y=(r.random(n)<risk).astype(float)
        return A,U,noise,P,Y,risk
    at,ut,et,pt,yt,rt=sample(10000);A,U,e,priors,Y,risk=sample(20000)
    out={}
    for name,train,test,testcf in [('priors',pt,priors,1.5+U+1.2*(1-A)+e),('residual',pt-1.2*at,priors-1.2*A,1.5+U+e)]:
        w=_logit(np.column_stack([np.ones(len(train)),train]),yt)
        score=lambda z:1/(1+np.exp(-np.column_stack([np.ones(len(z)),z])@w))
        s=score(test);scf=score(testcf)
        out[name]=dict(gap=float(s[A==1].mean()-s[A==0].mean()),auc=_auc(s,Y),counterfactual_max_change=float(np.max(abs(s-scf))),counterfactual_mean_change=float(np.mean(abs(s-scf))))
    return dict(n=len(Y),n_train=len(yt),**out,true_gap=float(Y[A==1].mean()-Y[A==0].mean()),risk_gap=float(risk[A==1].mean()-risk[A==0].mean()),oracle_effect=1.2,model='continuous additive measurement index; independent train/test; oracle structural residual')



def _auc(s, y):
    from scipy.stats import rankdata
    rk = rankdata(s)
    n1 = y.sum()
    n0 = len(y) - n1
    return float((rk[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def compute_board():
    q = load("inference")
    rows = [Row(63, r"Wald interval on a DP-noised count", rf"Laplace, \ $\varepsilon = {q['board_eps']}$, \ $n = 1{{,}}000$", "coverage", 0.95, q["board_naive"], q["board_reps"]),
            Row(63, r"noise-aware interval", rf"Laplace, \ $\varepsilon = {q['board_eps']}$, \ $n = 1{{,}}000$", "coverage", 0.95, q["board_aware"], q["board_reps"])]
    save_rows(63, rows)
    return {"rows": [asdict(x) | {"verdict": x.verdict, "se": x.se} for x in rows]}


ITEMS = {
    "unique": compute_unique, "mechanisms": compute_mechanisms, "tradeoff": compute_tradeoff, "accounting": compute_accounting,
    "cost": compute_cost, "inference": compute_inference, "census": compute_census, "dpsgd": compute_dpsgd,
    "compas": compute_compas, "multical": compute_multical, "cfair": compute_cfair, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
