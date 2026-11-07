"""Precompute every number in Part 33 of *Statistics, Built* ("Thousands of Questions").

    python -m videos.stats.stats33.compute            # everything missing (a few minutes)
    python -m videos.stats.stats33.compute --force board

Results are cached in ``.cache/stats33/<name>.json``.  The prostate z-values are the Museum's (Singh et al. 2002);
the gene study is the World's; the rest are seeded simulations.

Items:
    salmon      a 'brain' of pure-noise voxels: what p < .001 uncorrected finds, and what corrections find
    genes       the World's 5,000-gene study: uncorrected, Bonferroni, Holm, Westfall--Young, BH, BY, Storey
    fdp         the spread of BH's false discovery proportion, independent vs equicorrelated tests
    prostate    Efron's local fdr on the prostate data, theoretical and empirical null
    knock       model-X knockoffs vs a naive lasso, FDR and power
    phack       Simmons, Nelson & Simonsohn's researcher degrees of freedom
    pub         a literature filtered by significance: the funnel, Egger's test, PET
    pcurve      p-curves for no effect and real effects
    fcr         intervals for BH-selected effects: unadjusted vs FCR-adjusted
    board       Coverage Board rows: FDR of BH (independent, dependent), BY, no correction; FCR
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import ndimage, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import multiple as MT
from explainer.stats.kit import sparse as SP
from explainer.stats.world import World

CACHE = Cache("stats33")
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


def fish_mask(H: int = 96, W: int = 192) -> np.ndarray:
    """A fish-shaped region of voxels: an elliptical body and a triangular tail."""
    yy, xx = np.mgrid[0:H, 0:W]
    body = ((xx - 0.42 * W) / (0.37 * W)) ** 2 + ((yy - H / 2) / (0.35 * H)) ** 2 <= 1
    tail = (xx >= 0.77 * W) & (xx <= 0.98 * W) & (np.abs(yy - H / 2) <= (xx - 0.75 * W) * 0.85)
    return body | tail


def compute_salmon():
    g = rng(2009)
    mask = fish_mask()
    n_scans = 15  # illustrative independent Gaussian contrast images; not the original fMRI design
    data = np.array([ndimage.gaussian_filter(g.standard_normal(mask.shape), 1.5) for _ in range(n_scans)])
    t = data.mean(0) / (data.std(0, ddof=1) / math.sqrt(n_scans))
    p = 2 * stats.t.sf(np.abs(t), n_scans - 1)
    pv = p[mask]
    act = (p < 0.001) & mask
    lab, nlab = ndimage.label(act)
    sizes = ndimage.sum(act, lab, range(1, nlab + 1)) if nlab else np.array([])
    clusters = int(np.sum(sizes >= 3)) if nlab else 0
    # a bigger 'brain': how many voxels light up by chance at p < .001 out of 130,000
    big = 130_000
    exp_fp = big * 0.001
    bonf = int(np.sum(pv < 0.05 / mask.sum()))
    bhk = MT.bh(pv, 0.05)["k"]
    act01 = (p < 0.01) & mask
    lab01, n01 = ndimage.label(act01)
    return nest({"mask": mask.astype(int), "n_vox": int(mask.sum()), "active01": act01.astype(int),
                 "n_active01": int(act01.sum()), "clusters01": int(n01),
                 "active": act.astype(int), "n_active": int(act.sum()), "n_05": int(np.sum(pv < 0.05)), "clusters3": clusters,
                 "expected": mask.sum() * 0.001, "big": big, "big_expected": exp_fp, "bonf": bonf, "bh": bhk})


def gene_tests():
    w = World()
    gd = w.genes
    x, grp = gd["x"], gd["group"].astype(bool)
    a, b = x[grp], x[~grp]
    r = stats.ttest_ind(a, b)
    return gd, r.statistic, r.pvalue


def compute_genes():
    gd, t, p = gene_tests()
    nn = gd["nonnull"]
    m = len(p)

    def summary(rej):
        rej = np.asarray(rej, bool)
        R, V = int(rej.sum()), int((rej & ~nn).sum())
        return {"R": R, "V": V, "S": R - V, "fdp": V / max(R, 1), "power": float((rej & nn).sum() / nn.sum())}

    res = {"uncorrected": summary(p < 0.05), "bonferroni": summary(MT.adjust(p, "bonferroni") < 0.05),
           "holm": summary(MT.adjust(p, "holm") < 0.05), "bh05": summary(MT.bh(p, 0.05)["reject"]),
           "bh10": summary(MT.bh(p, 0.1)["reject"]), "by10": summary(MT.bh(p, 0.1, by=True)["reject"])}
    wy = MT.westfall_young(gd["x"], gd["group"].astype(bool), B=1000, rng=rng(1993))
    res["westfall_young"] = summary(wy["adj"] < 0.05)
    pi0 = MT.storey_pi0(p)
    qv = MT.qvalues(p, pi0)
    res["storey10"] = summary(qv <= 0.1)
    hist = np.histogram(p, np.linspace(0, 1, 21))[0]
    sp = np.sort(p)
    return nest({"m": m, "m1": int(nn.sum()), "res": res, "pi0": pi0, "hist": hist, "p_sorted": sp[:400],
                 "k_bh10": MT.bh(p, 0.1)["k"], "bh10_thr": MT.bh(p, 0.1)["threshold"], "p_all": p,
                 "nonnull_sorted": nn[np.argsort(p)][:400], "min_p": float(sp[0]),
                 "bonf_thr": 0.05 / m, "t": t})


def compute_fdp():
    out = {}
    for rho in (0.0, 0.5):
        r = MT.fdp_sim(1000, 0.9, 2.5, rho, 0.1, 2000, rng(int(rho * 10) + 7))
        out[str(rho)] = {"fdp": r["fdp"], "fdr": r["fdr"], "power": r["power"], "p_gt": r["p_fdp_gt_2q"],
                         "p_zero": r["p_zero"], "R_mean": float(np.mean(r["R"])), "R_sd": float(np.std(r["R"])),
                         "R": r["R"]}
    rb = MT.fdp_sim(1000, 0.9, 2.5, 0.5, 0.1, 2000, rng(99), method="by")
    out["by"] = {"fdr": rb["fdr"], "power": rb["power"]}
    return nest(out)


def compute_prostate():
    t, z = museum.prostate_z()
    lt = MT.locfdr(z, null="theoretical")
    le = MT.locfdr(z, null="empirical")
    p = 2 * stats.norm.sf(np.abs(z))
    fdr_t = lt["fdr_at"](z)
    fdr_e = le["fdr_at"](z)
    return nest({"N": len(z), "mids": lt["mids"], "counts": lt["counts"], "f": lt["f"], "width": lt["width"],
                 "f0_theo": lt["f0"], "f0_emp": le["f0"], "pi0_t": lt["pi0"], "pi0_e": le["pi0"], "delta0": le["delta0"],
                 "sigma0": le["sigma0"], "fdr_t": lt["fdr"], "fdr_e": le["fdr"],
                 "n_fdr20_t": int(np.sum(fdr_t < 0.2)), "n_fdr20_e": int(np.sum(fdr_e < 0.2)),
                 "bh10": MT.bh(p, 0.1)["k"], "bonf": int(np.sum(p < 0.05 / len(p))), "zmax": float(z.max()),
                 "zmin": float(z.min()), "n_z3": int(np.sum(np.abs(z) > 3)), "exp_z3": float(len(z) * 2 * stats.norm.sf(3)),
                 "sd": float(z.std())})


def mean_mc_se(values):
    """Monte Carlo SE across independent simulated studies, including empty lists."""
    return float(np.std(values, ddof=1) / math.sqrt(len(values)))


def fold_scaled_cv(X, y, lams, K=5, rng=None):
    """Fit every centering/scaling transform using its training fold only."""
    order = rng.permutation(len(y))
    folds = np.array_split(order, K)
    errors = []
    for test in folds:
        train = np.setdiff1d(order, test)
        A, b, xm, scale, ym = SP.standardize(X[train], y[train])
        path = SP.lasso_path(A, b, lams=lams)
        prediction = (X[test] - xm) / scale @ path["coefs"].T + ym
        errors.append(np.mean((y[test, None] - prediction) ** 2, axis=0))
    means = np.average(errors, axis=0, weights=[len(f) for f in folds])
    return {"lam_min": float(lams[np.argmin(means)]), "mse": means, "folds": folds}


def compute_knock():
    g = rng(2015)
    n, p, k = 400, 150, 20
    rho = 0.5
    S = rho ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    L = np.linalg.cholesky(S)
    amp = 0.35
    q = 0.1
    stats_ = {"knockoff": [], "lasso_cv": [], "pow_k": [], "pow_l": []}
    demo = None
    for rep in range(20):
        X = g.standard_normal((n, p)) @ L.T
        beta = np.zeros(p)
        idx = g.choice(p, k, replace=False)
        beta[idx] = amp * g.choice([-1.0, 1.0], k)
        y = X @ beta + g.standard_normal(n)
        Xk = MT.gaussian_knockoffs(X, S, g)
        lam = 0.6 * math.sqrt(2 * math.log(2 * p) / n)
        W = MT.lasso_W(X, Xk, y, lam)
        thr = MT.knockoff_threshold(W, q)
        sel = np.flatnonzero(W >= thr)
        true = beta != 0
        stats_["knockoff"].append(np.mean(~true[sel]) if len(sel) else 0.0)
        stats_["pow_k"].append(np.mean(true[sel].sum() / k))
        Xs, ys, *_ = SP.standardize(X, y)
        lams = np.geomspace(2.0, 0.01, 25)  # fixed without inspecting validation outcomes
        cv = fold_scaled_cv(X, y, lams, K=5, rng=g)
        b = SP.lasso_cd(Xs, ys, cv["lam_min"])
        sl = np.flatnonzero(b)
        stats_["lasso_cv"].append(np.mean(~true[sl]) if len(sl) else 0.0)
        stats_["pow_l"].append(true[sl].sum() / k)
        if rep == 0:
            demo = {"W": W, "true": true, "thr": thr, "n_sel": len(sel), "false_sel": int(np.sum(~true[sel])),
                    "lasso_sel": len(sl), "lasso_false": int(np.sum(~true[sl]))}
    return nest({"n": n, "p": p, "k": k, "q": q, "fdr_knock": float(np.mean(stats_["knockoff"])),
                 "pow_knock": float(np.mean(stats_["pow_k"])), "fdr_lasso": float(np.mean(stats_["lasso_cv"])),
                 "pow_lasso": float(np.mean(stats_["pow_l"])), "demo": demo, "reps": 20,
                 "replicates": stats_, "mc_se": {k: mean_mc_se(v) for k, v in stats_.items()}})


def compute_phack():
    r = MT.phack(5000, rng(2011))
    return nest(r)


def compute_stopping():
    """Optional stopping with no effect: a two-group study checked after every 10 subjects per group, from 10 to 100,
    stopping at the first p < .05.  One trajectory, and the chance of ever 'succeeding'."""
    g = rng(64)
    looks = np.arange(10, 101, 10)
    traj = None
    hits = 0
    reps = 4000
    for r in range(reps):
        a, b = g.standard_normal(100), g.standard_normal(100)
        ps = [stats.ttest_ind(a[:k], b[:k]).pvalue for k in looks]
        if r < 200 and traj is None and min(ps) < 0.05 and np.argmin(ps) >= 4:
            traj = ps
        hits += min(ps) < 0.05
    return nest({"looks": looks, "traj": traj, "p_ever": hits / reps, "reps": reps})


def compute_pub():
    g = rng(1997)
    s = MT.publication_sim(800, 0.2, g, publish_null=0.1)
    pub = s["published"]
    e_all = MT.egger(s["est"], s["se"])
    e_pub = MT.egger(s["est"][pub], s["se"][pub])
    w = 1 / s["se"] ** 2
    fe_all = float(np.sum(w * s["est"]) / np.sum(w))
    fe_pub = float(np.sum(w[pub] * s["est"][pub]) / np.sum(w[pub]))
    return nest({"est": s["est"], "se": s["se"], "pub": pub, "n_pub": int(pub.sum()), "k": len(pub), "truth": 0.2,
                 "fe_all": fe_all, "fe_pub": fe_pub, "egger_all": e_all, "egger_pub": e_pub,
                 "share_sig_pub": float(np.mean(s["p"][pub] < 0.05))})


def compute_pcurve():
    """p-curves (Simonsohn, Nelson & Simmons 2014): the distribution of significant two-sided p-values in bins of
    0.01, exactly, for a two-sample z-test with n = 30 per group and standardized effect 0 (flat), 0.3 and 0.7."""
    edges = np.array([0.0, 0.01, 0.02, 0.03, 0.04, 0.05])
    out = {}
    for d in (0.0, 0.3, 0.7):
        ncp = d * math.sqrt(30 / 2)
        zc = stats.norm.isf(edges / 2)
        tail = stats.norm.sf(zc - ncp) + stats.norm.cdf(-zc - ncp)  # P(|Z| > z_c) = P(p < edge)
        tail[0] = 0.0
        probs = np.diff(tail) / tail[-1]
        out[str(d)] = {"probs": probs, "power": float(tail[-1]), "below_025": float(
            (stats.norm.sf(stats.norm.isf(0.0125) - ncp) + stats.norm.cdf(-stats.norm.isf(0.0125) - ncp)) / tail[-1])}
    grid = np.linspace(0.0005, 0.0495, 99)
    return nest({"edges": edges, "curves": out, "grid": grid, "null": MT.pcurve_density(0.0, 30, grid),
                 "small": MT.pcurve_density(0.3, 30, grid), "large": MT.pcurve_density(0.7, 30, grid)})


def _fcr_rep(g, m=1000, m1=100, q=0.1, alpha=0.1):
    mu = np.zeros(m)
    mu[:m1] = g.normal(2.5, 0.5, m1)
    x = mu + g.standard_normal(m)
    p = 2 * stats.norm.sf(np.abs(x))
    sel = MT.bh(p, q)["reject"]
    R = int(sel.sum())
    zu = stats.norm.ppf(1 - alpha / 2)
    if R == 0:
        return 1.0, 1.0, 0, 0.0  # noncoverage/(R or 1) is zero for an empty family
    unadj = np.abs(x[sel] - mu[sel]) <= zu
    adj = MT.fcr_intervals(x, np.ones(m), sel, alpha)
    adjc = (adj["lo"][sel] <= mu[sel]) & (mu[sel] <= adj["hi"][sel])
    return float(np.mean(unadj)), float(np.mean(adjc)), R, adj["z"]


def compute_fcr():
    g = rng(2005)
    out = [_fcr_rep(g) for _ in range(400)]
    return nest({"unadj": float(np.mean([o[0] for o in out])), "adj": float(np.mean([o[1] for o in out])),
                 "R_mean": float(np.mean([o[2] for o in out])), "z_adj": float(np.mean([o[3] for o in out if o[2]])),
                 "zero_selections": sum(o[2] == 0 for o in out), "replicates": out,
                 "z_unadj": float(stats.norm.ppf(0.95))})


def compute_board():
    reps = 1000
    q = 0.1
    rows = []
    r_ind = MT.fdp_sim(1000, 0.9, 2.5, 0.0, q, reps, rng(1))
    r_dep = MT.fdp_sim(1000, 0.9, 2.5, 0.5, q, reps, rng(2))
    r_by = MT.fdp_sim(1000, 0.9, 2.5, 0.5, q, reps, rng(3), method="by")
    # no correction: reject every p < q
    g = rng(4)
    fdp_none = []
    for _ in range(reps):
        z = MT.equicorrelated_z(1000, 0.0, g)
        z[900:] += 2.5
        pv = stats.norm.sf(z)
        rej = pv < q
        fdp_none.append(rej[:900].sum() / max(rej.sum(), 1))
    rows.append(Row(33, r"no correction \ (each $p < 0.1$)", r"$m = 1000$, \ 90\% null, \ independent", "size", q,
                    float(np.mean(fdp_none)), reps, extra="FDR", mc_se=mean_mc_se(fdp_none)))
    rows.append(Row(33, r"Benjamini--Hochberg, \ $q = 0.1$", r"$m = 1000$, \ 90\% null, \ independent", "size", q, r_ind["fdr"], reps, extra="FDR", mc_se=mean_mc_se(r_ind["fdp"])))
    rows.append(Row(33, r"Benjamini--Hochberg, \ $q = 0.1$", r"$m = 1000$, \ equicorrelated $\rho = 0.5$", "size", q, r_dep["fdr"], reps, extra="FDR", mc_se=mean_mc_se(r_dep["fdp"])))
    rows.append(Row(33, r"Benjamini--Yekutieli, \ $q = 0.1$", r"$m = 1000$, \ equicorrelated $\rho = 0.5$", "size", q, r_by["fdr"], reps, extra="FDR", mc_se=mean_mc_se(r_by["fdp"])))
    g = rng(5)
    fc = [_fcr_rep(g) for _ in range(reps)]
    rows.append(Row(33, r"unadjusted 90\% CIs, \ BH-selected", r"$m = 1000$, \ 100 real effects", "coverage", 0.9,
                    float(np.mean([o[0] for o in fc])), len(fc), extra="1-FCR", mc_se=mean_mc_se([o[0] for o in fc])))
    rows.append(Row(33, r"FCR-adjusted CIs, \ BH-selected", r"$m = 1000$, \ 100 real effects", "coverage", 0.9,
                    float(np.mean([o[1] for o in fc])), len(fc), extra="1-FCR", mc_se=mean_mc_se([o[1] for o in fc])))
    save_rows(33, rows)
    return nest({"q": q, "reps": reps, "fdr_ind": r_ind["fdr"], "fdr_dep": r_dep["fdr"], "fdr_by": r_by["fdr"],
                 "fdr_none": float(np.mean(fdp_none)), "pow_ind": r_ind["power"], "pow_dep": r_dep["power"],
                 "pow_by": r_by["power"], "fdp_replicates": {"none": fdp_none, "ind": r_ind["fdp"],
                 "dep": r_dep["fdp"], "by": r_by["fdp"]}, "fcr_replicates": fc, "rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


ITEMS = {
    "salmon": compute_salmon, "genes": compute_genes, "fdp": compute_fdp, "prostate": compute_prostate,
    "knock": compute_knock, "phack": compute_phack, "stopping": compute_stopping, "pub": compute_pub, "pcurve": compute_pcurve, "fcr": compute_fcr,
    "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
