"""Precompute every number in Part 57 of *Statistics, Built* ("Distribution-Free Inference").

    OMP_NUM_THREADS=1 python -m videos.stats.stats57.compute            # everything missing (a few minutes)
    python -m videos.stats.stats57.compute --force board

Results are cached in ``.cache/stats57/<name>.json``.  NHANES and the Wisconsin breast cancer data are the Museum's;
everything else is exact arithmetic or a seeded simulation.

Items:
    bs        the Bahadur-Savage family: the t-interval's coverage against the bound, by eps
    lemma     the quantile lemma: exact coverage by n; the Beta law of coverage given the calibration set
    full      full against split conformal for ridge: coverage and length
    local     conditional coverage by bins of x for split conformal on heteroscedastic data
    nhanes    NHANES systolic pressure: coverage by age, sex and race group for marginal, Mondrian and conditional
    drift     a drifting series: split against nonexchangeable (weighted) conformal over time
    outliers  conformal outlier detection with BH on the breast cancer data
    risk      conformal risk control of a false negative rate
    aci       adaptive conformal inference on the drifting series, by gamma
    pvals     the outlier example's conformal p-values for inliers and outliers, one split
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
from explainer.stats.kit import conformal as CF
from . import checked as F

CACHE = Cache("stats57")
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


def compute_bs():
    r = rng(5701)
    n = 50
    eps = [0.3, 0.1, 0.05, 0.03, 0.02, 0.01, 0.005, 0.003, 0.001]
    rows = [{"eps": e, "atom": 3.0 / e, **F.bahadur_savage_coverage(n, e), "sim": F.bahadur_savage_sim(n, e, r, reps=4000)} for e in eps]
    return {"n": n, "rows": rows}


def compute_lemma():
    r = rng(5702)
    ns = [4, 10, 14, 25, 33, 50, 101, 250]
    rows = [{"n": n, **F.quantile_lemma_coverage(n, 0.1)} for n in ns]
    # the coverage given one calibration set, over many calibration sets of n = 100
    n = 100
    k = math.ceil((n + 1) * 0.9)
    cond = []
    for _ in range(4000):
        s = r.standard_normal(n)
        q = np.sort(s)[k - 1]
        cond.append(stats.norm.cdf(q))  # P(test <= q | calibration)
    law = F.conformal_coverage_law(n, 0.1)
    return {"rows": rows, "n": n, "cond": cond, "law": law, "mean": float(np.mean(cond)), "below85": float(np.mean(np.asarray(cond) < 0.85))}


def compute_full():
    r = rng(5703)
    n, p, reps = 40, 5, 200
    beta = np.array([1.0, -0.5, 0.25, 0.0, 0.0])
    res = {k: {"cov": 0, "len": []} for k in ("full", "split")}
    grid = np.linspace(-10, 10, 801)
    for _ in range(reps):
        X = r.standard_normal((n, p))
        y = X @ beta + r.standard_normal(n)
        x0 = r.standard_normal(p)
        y0 = x0 @ beta + r.standard_normal()
        fc = F.full_conformal_ridge(X, y, x0, 1.0, 0.1, grid=grid)
        res["full"]["cov"] += any(lo<=y0<=hi for lo,hi in fc["intervals"])
        res["full"]["len"].append(fc["length"])
        tr, ca = np.arange(n // 2), np.arange(n // 2, n)
        pred = lambda Z: F.ridge_fit_predict(X[tr], y[tr], Z, 1.0)  # noqa: E731
        sc = CF.split_conformal(pred(X[ca]), y[ca], pred(x0[None, :]), 0.1)
        res["split"]["cov"] += sc["lo"][0] <= y0 <= sc["hi"][0]
        res["split"]["len"].append(sc["hi"][0] - sc["lo"][0])
    return {"n": n, "p": p, "reps": reps, **{k: {"coverage": v["cov"] / reps, "len": float(np.median(v["len"])), "lengths": v["len"], "coverage_mcse": math.sqrt((v["cov"]/reps)*(1-v["cov"]/reps)/reps)} for k, v in res.items()}}


def compute_local():
    r = rng(5704)
    n = 4000
    x = r.uniform(0, 1, n)
    y = np.sin(2 * math.pi * x) + (0.1 + 1.2 * x ** 2) * r.standard_normal(n)
    tr, ca, te = np.arange(0, 1000), np.arange(1000, 2000), np.arange(2000, n)
    # fit the mean by a cubic polynomial
    Z = np.column_stack([np.ones(n), x, x ** 2, x ** 3, np.sin(2 * math.pi * x)])
    b = np.linalg.lstsq(Z[tr], y[tr], rcond=None)[0]
    m = Z @ b
    q = CF.conformal_quantile(np.abs(y[ca] - m[ca]), 0.1)
    cov = np.abs(y[te] - m[te]) <= q
    bins = np.linspace(0, 1, 11)
    bc = F.binned_coverage(x[te], cov, bins)
    # locally weighted: scale by a fitted spread
    zs = np.column_stack([np.ones(n), x, x ** 2])
    a = np.linalg.lstsq(zs[tr], np.abs(y[tr] - m[tr]), rcond=None)[0]
    sd = np.maximum(zs @ a, 0.05)
    q2 = CF.conformal_quantile(np.abs(y[ca] - m[ca]) / sd[ca], 0.1)
    cov2 = np.abs(y[te] - m[te]) <= q2 * sd[te]
    bc2 = F.binned_coverage(x[te], cov2, bins)
    return {"mid": bc["mid"], "plain": bc["coverage"], "scaled": bc2["coverage"], "marg_plain": float(cov.mean()), "marg_scaled": float(cov2.mean())}


def _nhanes_frame():
    d = museum.nhanes()
    readings = np.column_stack([d["sbp1"], d["sbp2"], d["sbp3"]])
    count = np.isfinite(readings).sum(1)
    sbp = np.divide(np.nansum(readings, axis=1), count, out=np.full(len(count), np.nan), where=count>0)
    ok = np.isfinite(sbp) & np.isfinite(d["bmi"]) & np.isfinite(d["age"]) & np.isfinite(d["sex"]) & np.isfinite(d["race"])
    return {k: d[k][ok] for k in ("age", "sex", "race", "bmi")} | {"sbp": sbp[ok]}


def compute_nhanes():
    f = _nhanes_frame()
    n = len(f["sbp"])
    age, sex, race, bmi, y = f["age"], f["sex"], f["race"], f["bmi"], f["sbp"]
    X = np.column_stack([np.ones(n), age, age ** 2 / 100, sex == 2, bmi])
    agegrp = np.digitize(age, [30, 45, 60, 70])  # 0: 18-29, 1: 30-44, 2: 45-59, 3: 60-69, 4: 70+
    r = rng(5705)
    reps = 8
    names = ["18-29", "30-44", "45-59", "60-69", "70+", "men", "women", "race 3", "race 4", "race 6"]

    def gmask(idx):
        a, s, rc = agegrp[idx], sex[idx], race[idx]
        cols = [a == k for k in range(5)] + [s == 1, s == 2, rc == 3, rc == 4, rc == 6]
        return np.column_stack(cols).astype(float)

    out = {m: {g: [] for g in names} for m in ("marginal", "mondrian", "gcc")}
    marg = {m: [] for m in out}
    for _ in range(reps):
        o = r.permutation(n)
        tr, ca, te = o[: n // 2], o[n // 2: n // 2 + 1200], o[n // 2 + 1200:]
        b = np.linalg.lstsq(X[tr], y[tr], rcond=None)[0]
        res_ca = np.abs(y[ca] - X[ca] @ b)
        res_te = np.abs(y[te] - X[te] @ b)
        Gc, Gt = gmask(ca), gmask(te)
        q = CF.conformal_quantile(res_ca, 0.1)
        cm = res_te <= q
        qa = CF.mondrian_quantiles(res_ca, agegrp[ca], 0.1)
        cmo = res_te <= np.array([qa[a] for a in agegrp[te]])
        # conditional calibration over the overlapping groups (age, sex, race): one threshold per distinct pattern
        pats, inv = np.unique(Gt, axis=0, return_inverse=True)
        thr = np.array([F.gcc_group_threshold(res_ca, np.column_stack([np.ones(len(ca)), Gc]), np.r_[1.0, pt], 0.1) for pt in pats])
        cg = res_te <= thr[inv.ravel()]
        for k, gname in enumerate(names):
            msk = Gt[:, k] > 0
            out["marginal"][gname].append(float(cm[msk].mean()))
            out["mondrian"][gname].append(float(cmo[msk].mean()))
            out["gcc"][gname].append(float(cg[msk].mean()))
        marg["marginal"].append(float(cm.mean()))
        marg["mondrian"].append(float(cmo.mean()))
        marg["gcc"].append(float(cg.mean()))
    summary = {m: {g: float(np.mean(v)) for g, v in out[m].items()} for m in out}
    counts = {g: int(c) for g, c in zip(names, gmask(np.arange(n)).sum(0))}
    return {"n": n, "groups": names, "summary": summary, "overall": {m: float(np.mean(v)) for m, v in marg.items()}, "counts": counts,
            "q_overall": float(q), "reps": reps, "split_coverages": out,
            "split_mcse": {m:{g:F.mcse(v) for g,v in out[m].items()} for m in out},
            "basis_columns": 11, "basis_rank": int(np.linalg.matrix_rank(np.column_stack([np.ones(n), gmask(np.arange(n))]))),
            "scope": "random splits conditional on the complete-case survey extract; ignores population survey weights/clustering; not independent national cohorts"}


def _roll(v, w=100):
    """A centred rolling mean that averages only the points that exist (no zero padding at the ends)."""
    v = np.asarray(v, float)
    k = np.ones(w)
    return np.convolve(v, k, mode="same") / np.convolve(np.ones_like(v), k, mode="same")


def compute_drift():
    r = rng(5706)
    T = 2000
    t = np.arange(T)
    sigma = np.where(t < 1000, 1.0, 2.5)  # a changepoint in the noise level at t = 1000
    y = sigma * r.standard_normal(T)
    window = 300
    rho = 0.99
    split_cov, nex_cov, split_thr, nex_thr = [], [], [], []
    for k in range(window, T):
        past = np.abs(y[k - window:k])
        qs = CF.conformal_quantile(past, 0.1)
        w = rho ** np.arange(window, 0, -1)
        qn = F.nexcp_threshold(past, w, 0.1)
        split_cov.append(abs(y[k]) <= qs)
        nex_cov.append(abs(y[k]) <= qn)
        split_thr.append(qs)
        nex_thr.append(qn)
    sc, nc = np.asarray(split_cov, float), np.asarray(nex_cov, float)
    tt = t[window:]

    def roll(v, w=100):
        return _roll(v, w)

    after = tt >= 1000
    paths=[]
    for rep in range(40):
        yy=sigma*rng(570600+rep).standard_normal(T)
        hits_s=[];hits_w=[]
        for k in range(1000,1300):
            past=np.abs(yy[k-window:k]);order=np.argsort(past);ordered=past[order]
            qs=ordered[math.ceil((window+1)*.9)-1]
            cumulative=np.cumsum((rho**np.arange(window,0,-1))[order])/(np.sum(rho**np.arange(window,0,-1))+1)
            index=np.searchsorted(cumulative,.9);qw=ordered[index] if index<window else np.inf
            hits_s.append(abs(yy[k])<=qs);hits_w.append(abs(yy[k])<=qw)
        paths.append([float(np.mean(hits_s)),float(np.mean(hits_w))])
    path_array=np.array(paths)
    board=dict(split=float(path_array[:,0].mean()),weighted=float(path_array[:,1].mean()),reps=40,
               split_mcse=F.mcse(path_array[:,0]),weighted_mcse=F.mcse(path_array[:,1]),coverage_samples=paths,
               scope="40 independent paths; coverage averaged over 300 temporally dependent post-change steps per path")
    pair_tv=4/math.pi*math.atan(2.5)-1
    weights=rho**np.arange(window,0,-1)
    tv_bound=dict(pair_tv=pair_tv,equal_stale_weight=250/301,weighted_stale_weight=float(weights[:250].sum()/(weights.sum()+1)),
                  equal_lower=.9-pair_tv*250/301,weighted_lower=.9-pair_tv*float(weights[:250].sum()/(weights.sum()+1)))
    return {"board":board, "tv_bound":tv_bound, "t": tt[::10], "split_roll": roll(sc)[::10], "nex_roll": roll(nc)[::10], "split_thr": np.asarray(split_thr)[::10],
            "nex_thr": np.asarray(nex_thr)[::10], "split_after": float(sc[after][:300].mean()), "nex_after": float(nc[after][:300].mean()),
            "split_all": float(sc.mean()), "nex_all": float(nc.mean()), "rho": rho, "window": window}


def _benign_split(X, ben, r):
    """150 benign biopsies fit the score (the distance from their centre, in their standardized units), 157 more are
    the reference set, and the remaining 50 are test inliers."""
    b = r.permutation(ben)
    tr, ca, ti = b[:150], b[150:307], b[307:]
    mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
    score = lambda idx: np.sum(((X[idx] - mu) / sd) ** 2, axis=1)  # noqa: E731
    return tr, ca, ti, score


def compute_outliers():
    X, y, names = museum.breast_cancer()
    r = rng(5707)
    ben, mal = np.flatnonzero(y == 0), np.flatnonzero(y == 1)
    from explainer.stats.kit.multiple import bh

    fdps, pows, zero = [], [], 0
    for _ in range(50):
        tr, ca, test_in, score = _benign_split(X, ben, r)
        test_out = r.choice(mal, 40, replace=False)
        te = np.r_[test_in, test_out]
        is_out = np.r_[np.zeros(len(test_in)), np.ones(len(test_out))].astype(bool)
        p = F.outlier_pvalues(score(ca), score(te))
        rej = np.asarray(bh(p, 0.1)["reject"], bool)
        zero += int(rej.sum() == 0)
        fdps.append(float(np.sum(rej & ~is_out) / max(1, rej.sum())))
        pows.append(float(np.sum(rej & is_out) / is_out.sum()))
    return {"fdr": float(np.mean(fdps)), "power": float(np.mean(pows)), "n_test_in": int(len(ben) - 307), "n_test_out": 40,
            "n_ref": 157, "n_fit": 150, "zero": zero, "fdp_samples": fdps, "power_samples": pows, "fdr_mcse": F.mcse(fdps), "power_mcse": F.mcse(pows),
            "scope": "50 random splits conditional on one fixed biopsy dataset"}


def compute_risk():
    """Multilabel screening: each unit has 20 candidate labels, a few of them true; a model scores them; predict the
    set {k: score_k >= 1 - lam}; control the false negative rate (fraction of true labels missed) at alpha = 0.1."""
    r = rng(5708)

    def draw(n):
        truth = r.random((n, 20)) < 0.15
        score = 1 / (1 + np.exp(-(1.6 * truth - 0.8 + 0.9 * r.standard_normal((n, 20)))))
        return truth, score

    lams = np.linspace(0, 1, 201)
    tc, sc = draw(500)

    def fnr(truth, score, lam):
        pred = score >= 1 - lam
        miss = np.sum(truth & ~pred, axis=1)
        tot = np.maximum(np.sum(truth, axis=1), 1)
        return np.where(np.sum(truth, axis=1) > 0, miss / tot, 0.0)

    L = np.column_stack([fnr(tc, sc, l) for l in lams])
    lh = F.conformal_risk_control(L, lams, 0.1)
    tt, st = draw(20000)
    test_fnr = float(np.mean(fnr(tt, st, lh)))
    size = float(np.mean(np.sum(st >= 1 - lh, axis=1)))
    # repeat over calibration sets for the guarantee in expectation
    reps = []
    for _ in range(200):
        tc2, sc2 = draw(500)
        L2 = np.column_stack([fnr(tc2, sc2, l) for l in lams])
        l2 = F.conformal_risk_control(L2, lams, 0.1)
        t3, s3 = draw(2000)
        reps.append(float(np.mean(fnr(t3, s3, l2))))
    return {"lam": lh, "test_fnr": test_fnr, "set_size": size, "mean_fnr": float(np.mean(reps)), "curve_lam": lams[::5],
            "curve_risk": L.mean(0)[::5], "risk_samples": reps, "risk_mcse": F.mcse(reps),
            "test_fnr_mcse": F.mcse(fnr(tt, st, lh)), "calibration_corrected_risk": float((fnr(tc,sc,lh).sum()+1)/(len(tc)+1))}


def compute_aci():
    r = rng(5706)
    T = 2000
    t = np.arange(T)
    sigma = np.where(t < 1000, 1.0, 2.5)
    y = sigma * r.standard_normal(T)
    out = {"gammas": [0.0, 0.005, 0.02]}
    for g in out["gammas"]:
        res = F.aci(np.abs(y), alpha=0.1, gamma=g, window=300, warm=300)
        e = res["err"]
        roll = _roll(1 - e, 100)
        out[str(g)] = {"roll": roll[::10], "alpha_t": res["alpha_t"][::10], "miss": float(e.mean()),
                       "after": float(1 - e[700:1000].mean()), "errors": e, "levels": res["alpha_t"],
                       "alpha_final": res["alpha_final"], "infinite_sets": res["infinite_sets"], "empty_sets": res["empty_sets"]}
    out["t"] = np.arange(300, T)[::10]
    return out


def compute_pvals():
    """The outlier example's conformal p-values, pooled over 20 random splits (50 benign and 40 malignant tests each)."""
    X, y, names = museum.breast_cancer()
    r = rng(5712)
    ben, mal = np.flatnonzero(y == 0), np.flatnonzero(y == 1)
    pin, pout = [], []
    for _ in range(20):
        tr, ca, ti, score = _benign_split(X, ben, r)
        to = r.choice(mal, 40, replace=False)
        pin.append(F.outlier_pvalues(score(ca), score(ti)))
        pout.append(F.outlier_pvalues(score(ca), score(to)))
    return {"inlier": np.concatenate(pin), "outlier": np.concatenate(pout), "n_ref": 157, "splits": 20}


def compute_board():
    r = rng(5709)
    rows = []
    bs = [x for x in load("bs")["rows"] if x["eps"] == 0.003][0]
    rows.append(Row(57, r"$t$-interval for the mean", r"Bahadur--Savage mixture, \ $n = 50$", "coverage", 0.95, bs["sim"], 4000))
    # split conformal on the same family (prediction of a new draw): exact
    hits = 0
    reps = 4000
    for _ in range(reps):
        s = r.standard_normal(51)
        atom = r.random(51) < 0.003
        s[atom] = 1000.0
        q = CF.conformal_quantile(np.abs(s[:50]), 0.05)
        hits += abs(s[50]) <= q
    rows.append(Row(57, r"split conformal prediction interval", r"Bahadur--Savage mixture, \ $n = 50$", "coverage", 0.95, hits / reps, reps))
    nh = load("nhanes")
    n_te = nh["n"] - nh["n"] // 2 - 1200
    reps_n = nh["reps"]  # Independent random splits conditional on this fixed extract, not test people.  # test points aged 70+, over the splits
    rows.append(Row(57, r"marginal split conformal, \ ages 70+", r"NHANES systolic pressure", "coverage", 0.90, nh["summary"]["marginal"]["70+"], reps_n, mc_se=nh["split_mcse"]["marginal"]["70+"]))
    rows.append(Row(57, r"group-conditional conformal, \ ages 70+", r"NHANES systolic pressure", "coverage", 0.90, nh["summary"]["gcc"]["70+"], reps_n, mc_se=nh["split_mcse"]["gcc"]["70+"]))
    dr = load("drift")
    rows.append(Row(57, r"split conformal after a changepoint", r"noise SD 1 $\to$ 2.5, \ 300 steps after", "coverage", 0.90, dr["board"]["split"], dr["board"]["reps"], mc_se=dr["board"]["split_mcse"]))
    rows.append(Row(57, r"weighted (nonexchangeable) conformal", r"noise SD 1 $\to$ 2.5, \ 300 steps after", "coverage", 0.90, dr["board"]["weighted"], dr["board"]["reps"], mc_se=dr["board"]["weighted_mcse"]))
    for row in rows:
        if row.mc_se is None: row.mc_se=math.sqrt(row.achieved*(1-row.achieved)/row.reps)
    save_rows(57, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows]}


ITEMS = {
    "bs": compute_bs, "lemma": compute_lemma, "full": compute_full, "local": compute_local, "nhanes": compute_nhanes,
    "drift": compute_drift, "outliers": compute_outliers, "risk": compute_risk, "aci": compute_aci, "pvals": compute_pvals,
    "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
