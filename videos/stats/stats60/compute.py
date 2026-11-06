"""Precompute every number in Part 60 of *Statistics, Built* ("Robustness and Distribution Shift").

    OMP_NUM_THREADS=1 python -m videos.stats.stats60.compute            # everything missing (a few minutes)
    python -m videos.stats.stats60.compute --force board

Results are cached in ``.cache/stats60/<name>.json``.  NHANES, Old Faithful and the Wisconsin biopsies are the Museum's;
everything else is a seeded simulation.

Items:
    depth     Tukey depth on Old Faithful, with and without planted outliers: the depth map, the Tukey median, the mean
    robust    robust means in R^d under contamination: mean, coordinatewise and geometric medians, the filter
    listdec   list-decodable estimation with 30% inliers
    heavy     median of means against the mean under heavy tails
    covshift  NHANES: a young-skewed sample, the population's mean pressure, unweighted against importance weighting
    labshift  the biopsies: a classifier trained at 37% malignant, deployed at 70%: classify-and-count against BBSE and EM
    dro       NHANES: the robust risk over chi-square and KL balls against the risk in each age group
    invariance  a structural model with environments: OLS, anchor regression and ICP
    transfer  Trans-Lasso against target-only and pooled lassos, for a similar and a dissimilar source
    detect    NHANES: MMD and classifier two-sample tests between the sample and the population
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
from explainer.stats.kit import shift as H

CACHE = Cache("stats60")
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


def _nhanes():
    d = museum.nhanes()
    sbp = np.nanmean(np.column_stack([d["sbp1"], d["sbp2"], d["sbp3"]]), axis=1)
    ok = np.isfinite(sbp) & np.isfinite(d["bmi"]) & np.isfinite(d["age"]) & np.isfinite(d["sex"])
    return {k: d[k][ok] for k in ("age", "sex", "bmi")} | {"sbp": sbp[ok]}


def compute_depth():
    e, w = museum.faithful()
    X = np.column_stack([e, w / 10.0])  # waiting in tens of minutes, so the axes are comparable
    tm = H.tukey_median_2d(X, 50)
    r = rng(6001)
    bad = np.column_stack([r.normal(5.5, 0.1, 30), r.normal(3.0, 0.2, 30)])  # 30 planted points: long eruptions, short waits
    Xc = np.vstack([X, bad])
    tmc = H.tukey_median_2d(Xc, 50)
    return {"X": X, "bad": bad, "median": tm["median"], "depth": tm["depth"], "grid": tm["grid"], "depth_grid": tm["depth_grid"],
            "mean": X.mean(0), "median_c": tmc["median"], "mean_c": Xc.mean(0), "coord_median_c": np.median(Xc, 0),
            "depth_grid_c": tmc["depth_grid"], "grid_c": tmc["grid"]}


def compute_robust():
    r = rng(6002)
    ds = [5, 10, 25, 50, 100, 200]
    rows = []
    for d in ds:
        e = [H.robust_mean_errors(2000, d, 0.1, r) for _ in range(4)]
        rows.append({"d": d, **{k: float(np.mean([x[k] for x in e])) for k in e[0]}})
    eps = [0.02, 0.05, 0.1, 0.15, 0.2]
    rows_e = []
    for ep in eps:
        e = [H.robust_mean_errors(2000, 100, ep, r) for _ in range(4)]
        rows_e.append({"eps": ep, **{k: float(np.mean([x[k] for x in e])) for k in e[0]}})
    return {"n": 2000, "eps": 0.1, "rows": rows, "d_fixed": 100, "rows_eps": rows_e}


def compute_listdec():
    r = rng(6003)
    inl = r.standard_normal((90, 2)) * 0.6 + np.array([1.0, 1.0])
    outs = [r.standard_normal((70, 2)) * 0.5 + c for c in (np.array([-3.0, 2.0]), np.array([3.5, -2.5]), np.array([-2.0, -3.0]))]
    X = np.vstack([inl] + outs)
    L = H.list_decode(X, 0.3, r)
    mu = np.array([1.0, 1.0])  # the inliers' population centre
    dist = np.linalg.norm(L - mu, axis=1)
    return {"X": X, "n_in": 90, "list": L, "truth": mu, "best": float(dist.min()), "mean": X.mean(0),
            "mean_err": float(np.linalg.norm(X.mean(0) - mu)),
            "oracle": float(np.linalg.norm(inl.mean(0) - mu))}


def compute_heavy():
    r = rng(6004)
    n, d, reps = 600, 20, 400
    em, eg = [], []
    for _ in range(reps):
        X = r.standard_t(2.5, (n, d))
        em.append(np.linalg.norm(X.mean(0)))
        eg.append(np.linalg.norm(H.median_of_means(X, 30, r)))
    em, eg = np.asarray(em), np.asarray(eg)
    qs = [0.5, 0.9, 0.99]
    return {"n": n, "d": d, "reps": reps, "df": 2.5, "k": 30, "mean_q": [float(np.quantile(em, q)) for q in qs],
            "mom_q": [float(np.quantile(eg, q)) for q in qs], "qs": qs, "mean_err": em, "mom_err": eg}


def _young_sample(f, n, r):
    """A sample of NHANES adults drawn with probability proportional to exp(-(age - 18)/20): the young are
    over-represented, as in an online panel."""
    pr = np.exp(-(f["age"] - 18) / 20.0)
    pr /= pr.sum()
    return r.choice(len(f["sbp"]), n, replace=False, p=pr)


def compute_covshift():
    f = _nhanes()
    N = len(f["sbp"])
    truth = float(f["sbp"].mean())
    r = rng(6005)
    reps, n = 400, 600
    cov_u = cov_w = 0
    est_u, est_w, ess = [], [], []
    Zall = np.column_stack([f["age"] / 10, (f["age"] / 10) ** 2, f["sex"] == 2, f["bmi"] / 10])
    for _ in range(reps):
        idx = _young_sample(f, n, r)
        y = f["sbp"][idx]
        cu = H.weighted_mean_ci(y, np.ones(n))
        ref = r.choice(N, 2000, replace=False)  # unlabelled draws from the population: covariates only
        wfun = H.logistic_density_ratio(Zall[idx], Zall[ref])
        wt = wfun(Zall[idx])
        cw = H.weighted_mean_ci(y, wt)
        cov_u += cu["lo"] <= truth <= cu["hi"]
        cov_w += cw["lo"] <= truth <= cw["hi"]
        est_u.append(cu["mean"])
        est_w.append(cw["mean"])
        ess.append(cw["ess"])
    idx = _young_sample(f, n, r)
    return {"N": N, "n": n, "reps": reps, "truth": truth, "cov_u": cov_u / reps, "cov_w": cov_w / reps, "mean_u": float(np.mean(est_u)),
            "mean_w": float(np.mean(est_w)), "sd_u": float(np.std(est_u)), "sd_w": float(np.std(est_w)), "ess": float(np.mean(ess)),
            "age_sample": f["age"][idx], "age_pop": f["age"][r.choice(N, 2000, replace=False)],
            "mean_age_sample": float(f["age"][idx].mean()), "mean_age_pop": float(f["age"].mean())}


def _logit_fit(X, y, lam=1e-2, iters=50):
    X1 = np.column_stack([np.ones(len(X)), X])
    b = np.zeros(X1.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(X1 @ b)))
        g = X1.T @ (y - p) - lam * np.r_[0, b[1:]]
        Hm = (X1 * (p * (1 - p))[:, None]).T @ X1 + lam * np.diag(np.r_[0, np.ones(len(b) - 1)])
        step = np.linalg.solve(Hm, g)
        b += step
        if np.max(np.abs(step)) < 1e-9:
            break
    return lambda Z: 1 / (1 + np.exp(-(np.column_stack([np.ones(len(Z)), Z]) @ b)))


def compute_labshift():
    X, y, names = museum.breast_cancer()
    Z = (X - X.mean(0)) / X.std(0)
    Z = Z[:, :10]  # the ten mean features
    r = rng(6006)
    reps = 300
    q_true = 0.70
    out = {"cc": [], "bbse": [], "em": [], "cc_cov": 0, "bbse_cov": 0}
    for _ in range(reps):
        o = r.permutation(len(y))
        tr, ca, rest = o[:250], o[250:400], o[400:]
        clf = _logit_fit(Z[tr], y[tr])
        # a target sample of 150 with 70% malignant, drawn from the held-out rest
        mal, ben = rest[y[rest] == 1], rest[y[rest] == 0]
        nt = 100
        k = int(q_true * nt)
        te = np.r_[r.choice(mal, k, replace=True), r.choice(ben, nt - k, replace=True)]
        pred_ca = (clf(Z[ca]) > 0.5).astype(int)
        pred_te = (clf(Z[te]) > 0.5).astype(int)
        cc = float(pred_te.mean())
        b = H.bbse_weights(pred_ca, y[ca], pred_te, 2)
        em = H.em_label_shift(np.column_stack([1 - clf(Z[te]), clf(Z[te])]), np.bincount(y[tr], minlength=2) / len(tr))
        # intervals by a bootstrap over the target and calibration sets
        bs_cc, bs_b = [], []
        for _ in range(100):
            i = r.choice(len(te), len(te))
            j = r.choice(len(ca), len(ca))
            bs_cc.append(pred_te[i].mean())
            bs_b.append(H.bbse_weights(pred_ca[j], y[ca][j], pred_te[i], 2)["q"][1])
        lo, hi = np.quantile(bs_cc, [0.025, 0.975])
        out["cc_cov"] += lo <= q_true <= hi
        lo, hi = np.quantile(bs_b, [0.025, 0.975])
        out["bbse_cov"] += lo <= q_true <= hi
        out["cc"].append(cc)
        out["bbse"].append(float(b["q"][1]))
        out["em"].append(float(em["q"][1]))
    return {"reps": reps, "q_true": q_true, "p_train": float(np.mean(y)), "cc_mean": float(np.mean(out["cc"])), "bbse_mean": float(np.mean(out["bbse"])),
            "em_mean": float(np.mean(out["em"])), "cc_sd": float(np.std(out["cc"])), "bbse_sd": float(np.std(out["bbse"])), "em_sd": float(np.std(out["em"])),
            "cc_cov": out["cc_cov"] / reps, "bbse_cov": out["bbse_cov"] / reps, "cc": out["cc"], "bbse": out["bbse"], "em": out["em"]}


def compute_dro():
    f = _nhanes()
    r = rng(6007)
    young = f["age"] < 40
    idx = np.flatnonzero(young)
    X = np.column_stack([np.ones(len(f["sbp"])), f["sex"] == 2, f["bmi"]])
    b = np.linalg.lstsq(X[idx], f["sbp"][idx], rcond=None)[0]
    loss = (f["sbp"] - X @ b) ** 2 / 100.0  # squared error in (10 mm Hg)^2
    train_loss = loss[idx]
    groups = [(18, 40), (40, 60), (60, 81)]
    grisk = [float(loss[(f["age"] >= a) & (f["age"] < c)].mean()) for a, c in groups]
    sub = r.choice(train_loss, 1500, replace=False)
    rhos = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0]
    return {"groups": [f"{a}--{c - 1}" for a, c in groups], "grisk": grisk, "rhos": rhos, "chi2": [H.dro_chi2(sub, rh) for rh in rhos],
            "kl": [H.dro_kl(sub, rh) for rh in rhos], "train": float(train_loss.mean())}


def compute_invariance():
    r = rng(6008)

    def env(n, shift, r):
        A = r.normal(shift, 1.0, n)  # an anchor: the environment's push on X1 and Y's hidden cause
        H_ = r.standard_normal(n)  # hidden confounder
        X1 = A + H_ + r.standard_normal(n)
        Y = 1.0 * X1 + 2 * H_ + r.standard_normal(n)
        X2 = Y + A + r.standard_normal(n)  # a child of Y, also pushed by A
        return np.column_stack([X1, X2]), Y, A
    Xtr, ytr, Atr = env(2000, 0.0, r)
    Xte, yte, Ate = env(2000, 3.0, r)
    out = {"gammas": [0, 1, 2, 5, 10, 50], "train": [], "test": [], "coef": []}
    for g in out["gammas"]:
        b = H.anchor_regression(np.column_stack([np.ones(len(ytr)), Xtr]), ytr, np.column_stack([np.ones(len(ytr)), Atr]), g if g > 0 else 1e-9)
        pred_tr = np.column_stack([np.ones(len(ytr)), Xtr]) @ b
        pred_te = np.column_stack([np.ones(len(yte)), Xte]) @ b
        out["train"].append(float(np.mean((ytr - pred_tr) ** 2)))
        out["test"].append(float(np.mean((yte - pred_te) ** 2)))
        out["coef"].append(b[1:])
    # ICP with three environments on a confounder-free model
    Xs, ys, es = [], [], []
    for e, s in enumerate([0.0, 1.5, -1.5]):
        n = 400
        X1 = r.normal(s, 1, n)
        Y = 1.5 * X1 + r.standard_normal(n)
        X2 = Y + r.normal(s, 1, n)
        Xs.append(np.column_stack([X1, X2]))
        ys.append(Y)
        es.append(np.full(n, e))
    ic = H.icp(np.vstack(Xs), np.concatenate(ys), np.concatenate(es))
    return {**out, "icp": ic}


def compute_transfer():
    r = rng(6010)
    p, s, ns, reps = 200, 10, 1000, 40
    nts = [50, 100, 200, 400]
    out = {"p": p, "s": s, "ns": ns, "reps": reps, "nts": nts, "k_diff": 5, "h": [0.15, 1.0]}
    for h in out["h"]:
        res = {"transfer": [], "pooled": [], "target": []}
        for nt in nts:
            E = {k: [] for k in res}
            for _ in range(reps):
                b = np.zeros(p)
                b[:s] = 0.5
                w = b.copy()
                idx = r.choice(p, 5, replace=False)
                w[idx] += h * r.choice([-1, 1], 5)
                Xs = r.standard_normal((ns, p))
                ys = Xs @ w + r.standard_normal(ns)
                Xt = r.standard_normal((nt, p))
                yt = Xt @ b + r.standard_normal(nt)
                o = H.trans_lasso(Xs, ys, Xt, yt)
                for k in E:
                    E[k].append(float(np.sum((o[k] - b) ** 2)))
            for k in res:
                res[k].append(float(np.mean(E[k])))
        out[f"h{h:g}"] = res
    return out


def compute_detect():
    f = _nhanes()
    r = rng(6009)
    Z = np.column_stack([f["age"] / 10, f["bmi"] / 5, f["sex"]])
    idx = _young_sample(f, 300, r)
    ref = r.choice(len(f["sbp"]), 300, replace=False)
    t_shift = H.mmd_test(Z[idx], Z[ref], r, 300)
    ref2 = r.choice(len(f["sbp"]), 300, replace=False)
    t_same = H.mmd_test(Z[ref2], Z[ref], r, 300)
    # a classifier two-sample test: held-out accuracy of a logistic classifier of sample against population
    Zs, Zp = Z[idx], Z[ref]
    tr = np.r_[np.arange(150)]
    clf = _logit_fit(np.vstack([Zs[:150], Zp[:150]]), np.r_[np.ones(150), np.zeros(150)])
    acc = float(np.mean(np.r_[clf(Zs[150:]) > 0.5, clf(Zp[150:]) <= 0.5]))
    p_acc = float(stats.binom.sf(int(acc * 300) - 1, 300, 0.5))
    del tr
    return {"mmd_shift": t_shift, "mmd_same": t_same, "acc": acc, "p_acc": p_acc}


def compute_board():
    c = load("covshift")
    l = load("labshift")
    rows = [Row(60, r"unweighted interval, \ shifted sample", r"NHANES pressure, \ young-skewed $n = 600$", "coverage", 0.95, c["cov_u"], c["reps"]),
            Row(60, r"importance-weighted interval", r"NHANES pressure, \ young-skewed $n = 600$", "coverage", 0.95, c["cov_w"], c["reps"]),
            Row(60, r"classify-and-count prevalence interval", r"biopsies, \ 37\% $\to$ 70\% malignant", "coverage", 0.95, l["cc_cov"], l["reps"]),
            Row(60, r"BBSE label-shift interval", r"biopsies, \ 37\% $\to$ 70\% malignant", "coverage", 0.95, l["bbse_cov"], l["reps"])]
    save_rows(60, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows]}


ITEMS = {
    "depth": compute_depth, "robust": compute_robust, "listdec": compute_listdec, "heavy": compute_heavy,
    "covshift": compute_covshift, "labshift": compute_labshift, "dro": compute_dro, "invariance": compute_invariance,
    "transfer": compute_transfer, "detect": compute_detect, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
