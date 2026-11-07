"""Precompute every number in Part 56 of *Statistics, Built* ("Inference After Selection").

    OMP_NUM_THREADS=1 python -m videos.stats.stats56.compute            # everything missing (a few minutes)
    python -m videos.stats.stats56.compute --force board

Results are cached in ``.cache/stats56/<name>.json``.  Stamey's prostate data, Singh's prostate microarray, the Wisconsin
breast cancer data, Old Faithful and Newcomb's passage times are the Museum's; the gene study is the World's; everything
else is exact arithmetic or a seeded simulation.

Items:
    hook      the World's gene study: the top genes' estimated effects against the truth and a replication
    winners   inference on the winner among K normals: naive, conditional, hybrid, projection, by gap and K
    posi      the PoSI constant against Bonferroni and Scheffe, by p, for orthogonal and correlated designs
    lasso     Stamey's prostate data: the lasso at a fixed lambda, naive and selective intervals
    carving   threshold selection with and without randomization: interval lengths and coverage
    fission   data fission and splitting for the selected largest mean: coverage and power
    knockoffs model-X knockoffs: FDR and power, and the supermartingale's stopped value
    conformal conformal selection on the breast cancer data and by simulation
    microarray inference on the top gene of the prostate microarray
    cluster   post-clustering tests: Old Faithful and Newcomb, and the null p-value histogram
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
from . import checked as Z
from explainer.stats.world import World

CACHE = Cache("stats56")
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


def _effects(x, group):
    a, b = x[group == 1], x[group == 0]
    sp = np.sqrt((a.var(0, ddof=1) + b.var(0, ddof=1)) / 2)
    d = (a.mean(0) - b.mean(0)) / sp
    t = d / math.sqrt(1 / len(a) + 1 / len(b))
    return d, t


def compute_hook():
    w = World()
    g = w.genes
    x, group, delta = g["x"], g["group"], g["delta"]
    d, t = _effects(x, group)
    top = np.argsort(-np.abs(t))[:20]
    # a replication: a fresh study of the same genes, same design and correlation
    r = rng(5601)
    m, n, B = x.shape[1], x.shape[0], World.GENE_BLOCK
    f = r.standard_normal((n, m // B))
    xr = math.sqrt(World.GENE_RHO) * np.repeat(f, B, axis=1) + math.sqrt(1 - World.GENE_RHO) * r.standard_normal((n, m))
    xr = xr + group[:, None] * delta[None, :]
    dr, _ = _effects(xr, group)
    s = np.sign(d[top])
    return {"top": top, "est": np.abs(d[top]), "true": s * delta[top], "rep": s * dr[top], "t": t[top],
            "mean_est": float(np.mean(np.abs(d[top]))), "mean_true": float(np.mean(s * delta[top])), "mean_rep": float(np.mean(s * dr[top])),
            "n_null_top": int(np.sum(delta[top] == 0)), "m": m}


def compute_winners():
    r = rng(5602)
    out = {}
    # (a) by the gap between the best and the rest: K = 10, mu = (gap, 0, ..., 0)
    gaps = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
    rows = []
    for gap in gaps:
        mu = np.zeros(10)
        mu[0] = gap
        c = {"naive": 0, "cond": 0, "hybrid": 0, "proj": 0}
        L = {"cond": [], "hybrid": [], "proj": []}
        bias = []
        reps = 1500
        for _ in range(reps):
            y = mu + r.standard_normal(10)
            w = Z.winner_conditional(y)
            h = Z.winner_hybrid(y)
            j = w["j"]
            c["naive"] += w["naive"][0] <= mu[j] <= w["naive"][1]
            c["cond"] += w["lo"] <= mu[j] <= w["hi"]
            c["hybrid"] += h["lo"] <= mu[j] <= h["hi"]
            c["proj"] += h["projection"][0] <= mu[j] <= h["projection"][1]
            L["cond"].append(w["hi"] - w["lo"])
            L["hybrid"].append(h["hi"] - h["lo"])
            L["proj"].append(h["projection"][1] - h["projection"][0])
            bias.append(y[j] - mu[j])
        rows.append({"gap": gap, **{k: v / reps for k, v in c.items()}, **{f"len_{k}": float(np.median(v)) for k, v in L.items()},
                     "bias": float(np.mean(bias)), "bias_mcse": Z.mcse(bias),
                     "coverage_mcse": {k: math.sqrt((v/reps)*(1-v/reps)/reps) for k,v in c.items()},
                     "lengths": L, "reps": reps})
    out["by_gap"] = rows
    # (b) the winner's curse by K, all nulls: E[max] and the naive coverage
    Ks = [1, 2, 5, 10, 20, 50, 100, 1000]
    curse = []
    for K in Ks:
        Y = r.standard_normal((4000, K))
        mx = Y.max(1)
        curse.append({"K": K, "bias": float(mx.mean()), "naive": float(np.mean(np.abs(mx) <= 1.96)),
                      "naive_exact": float(stats.norm.cdf(1.96)**K-stats.norm.cdf(-1.96)**K), "bias_mcse": Z.mcse(mx)})
    out["curse"] = curse
    # (c) one worked example
    mu = np.array([1.0] + [0.0] * 9)
    y = mu + rng(56021).standard_normal(10)
    w = Z.winner_conditional(y)
    h = Z.winner_hybrid(y)
    out["example"] = {"y": y, **{k: w[k] for k in ("j", "lo", "hi", "median_unbiased", "naive", "second")}, "hybrid": [h["lo"], h["hi"]], "proj": h["projection"]}
    return out


def compute_posi():
    r = rng(5603)
    n = 60
    rows = []
    for p in (2, 3, 4, 5, 6, 7, 8, 9, 10):
        Xo = np.linalg.qr(r.standard_normal((n, p)))[0]
        S = 0.5 * np.ones((p, p)) + 0.5 * np.eye(p)
        Xc = r.standard_normal((n, p)) @ np.linalg.cholesky(S).T
        po = Z.posi_constant(Xo, r, reps=4000)
        pc = Z.posi_constant(Xc, r, reps=4000)
        rows.append({"p": p, "orth": Z.max_z_quantile(p,.95), "orth_mc": po["K"], "orth_quantile_ci": po["quantile_ci"],
                     "corr_quantile_ci": pc["quantile_ci"], "corr_validation_coverage": pc["validation_coverage"],
                     "corr_validation_mcse": pc["validation_mcse"], "corr": pc["K"], "bonf": pc["bonferroni"], "scheffe": pc["scheffe"], "z": pc["z"], "n_contrasts": pc["n_contrasts"]})
    return {"n": n, "rows": rows}


def compute_lasso():
    X, y, tr, names = museum.prostate()
    Xs = (X - X.mean(0)) / X.std(0)
    yc = y - y.mean()
    n, p = Xs.shape
    beta_ols, res, *_ = np.linalg.lstsq(Xs, yc, rcond=None)
    sigma = float(math.sqrt(np.sum((yc - Xs @ beta_ols) ** 2) / (n - p - 1)))
    out = {"names": names, "n": n, "sigma": sigma, "fits": [], "historical_scope": "Gaussian working-model intervals with full-fit plug-in sigma, not exact known-variance coverage"}
    for lam in (20.0, 35.0):
        res = Z.lasso_selective_intervals(Xs, yc, lam, sigma=sigma)
        out["fits"].append({"lam": lam, "E": [names[j] for j in res["E"]], "intervals": [
            {"name": names[iv["j"]], "est": iv["est"], "lo": iv["lo"], "hi": iv["hi"], "naive": iv["naive"], "trunc": iv["trunc"]} for iv in res["intervals"]]})
    # The historical sigma is a plug-in approximation; the following simulation treats its value as known.
    r = rng(5604)
    cov_s = cov_n = cnt = 0
    lens_s, lens_n = [], []
    dataset_s, dataset_n, dataset_counts = [], [], []
    mu = Xs @ np.r_[0.6, np.zeros(p - 1)]  # only the log cancer volume matters; the lasso at lambda 12 lets noise in
    for _ in range(800):
        ys = mu + sigma * r.standard_normal(n)
        ys = ys - ys.mean()
        rs = Z.lasso_selective_intervals(Xs, ys, 12.0, sigma=sigma)
        hits_s = hits_n = 0
        dataset_counts.append(len(rs["E"]))
        if len(rs["E"]) == 0:
            dataset_s.append(0); dataset_n.append(0)
            continue
        target = np.linalg.pinv(Xs[:, rs["E"]]) @ mu
        for k, iv in enumerate(rs["intervals"]):
            cnt += 1
            hit_s = iv["lo"] <= target[k] <= iv["hi"]
            cov_s += hit_s; hits_s += hit_s
            hit_n = iv["naive"][0] <= target[k] <= iv["naive"][1]
            cov_n += hit_n; hits_n += hit_n
            lens_s.append(iv["hi"] - iv["lo"])
            lens_n.append(iv["naive"][1] - iv["naive"][0])
        dataset_s.append(hits_s); dataset_n.append(hits_n)
    out["sim_truth"] = "lcavol 0.6, the rest 0; lambda 12"
    out["sim"] = {"selective": cov_s / cnt, "naive": cov_n / cnt, "count": cnt, "len_s": float(np.median(lens_s)), "len_n": float(np.median(lens_n)),
                  "selective_mcse": Z.ratio_mcse(dataset_s,dataset_counts), "naive_mcse": Z.ratio_mcse(dataset_n,dataset_counts),
                  "dataset_selective_hits": dataset_s, "dataset_naive_hits": dataset_n, "dataset_counts": dataset_counts,
                  "lengths_selective": lens_s, "lengths_naive": lens_n, "reps": 800,
                  "scope": "coefficient-weighted coverage; dataset-clustered ratio Monte Carlo SE"}
    return out


def compute_carving():
    r = rng(5605)
    c = 2.0
    out = {"c": c, "rows": []}
    for gamma in (0.0, 0.25, 0.5, 1.0, 2.0):
        cov, lens, sel, residuals = 0, [], 0, []
        mu = 1.0
        reps = 1500
        for _ in range(reps):
            y = mu + r.standard_normal()
            w = r.normal(0, gamma) if gamma > 0 else 0.0
            if y + w <= c:
                continue
            sel += 1
            iv = Z.threshold_selective(y, c, gamma=gamma)
            cov += iv["lo"] <= mu <= iv["hi"]
            lens.append(iv["hi"] - iv["lo"])
            residuals.append(iv["pivot_residual"])
        out["rows"].append({"gamma": gamma, "coverage": cov / sel, "len": float(np.median(lens)), "selected": sel / reps, "n_selected": sel, "lengths": lens,
                             "coverage_mcse": math.sqrt((cov/sel)*(1-cov/sel)/sel), "max_pivot_residual": max(residuals), "reps": reps})
    ys = np.linspace(2.05, 4.0, 40)
    out["curve"] = {"y": ys, "hard": [Z.threshold_selective(v, c, gamma=0)["lo"] for v in ys],
                    "soft": [Z.threshold_selective(v, c, gamma=1.0)["lo"] for v in ys]}
    return out


def compute_fission():
    """Select the largest of K = 20 means, then infer it.  Full reuse (naive), splitting each observation's sample in
    half, and fission with tau = 1: coverage of the selected mean, and how often the truly largest is selected."""
    r = rng(5606)
    K, nrep = 20, 3000
    mu = np.zeros(K)
    mu[:3] = [2.0, 1.0, 0.5]
    sig = 1.0
    res = {k: {"cov": 0, "hit": 0, "len": []} for k in ("naive", "split", "fission")}
    z = 1.959963984540054
    for _ in range(nrep):
        # two independent halves, each N(mu, 2 sigma^2) so that the average is N(mu, sigma^2)
        a = mu + math.sqrt(2) * sig * r.standard_normal(K)
        b = mu + math.sqrt(2) * sig * r.standard_normal(K)
        x = (a + b) / 2
        j = int(np.argmax(x))
        res["naive"]["cov"] += abs(x[j] - mu[j]) <= z * sig
        res["naive"]["hit"] += j == 0
        res["naive"]["len"].append(2 * z * sig)
        j = int(np.argmax(a))
        res["split"]["cov"] += abs(b[j] - mu[j]) <= z * math.sqrt(2) * sig
        res["split"]["hit"] += j == 0
        res["split"]["len"].append(2 * z * math.sqrt(2) * sig)
        f, g = Z.fission_normal(x, sig, 1.0, r)
        j = int(np.argmax(f))
        res["fission"]["cov"] += abs(g[j] - mu[j]) <= z * math.sqrt(2) * sig
        res["fission"]["hit"] += j == 0
        res["fission"]["len"].append(2 * z * math.sqrt(2) * sig)
    out = {k: {"coverage": v["cov"] / nrep, "hit": v["hit"] / nrep, "len": float(np.mean(v["len"]))} for k, v in res.items()}
    # tau trades selection against inference
    taus = [0.25, 0.5, 1.0, 2.0, 4.0]
    trade = []
    for tau in taus:
        hit = 0
        for _ in range(2000):
            x = mu + sig * r.standard_normal(K)
            f, g = Z.fission_normal(x, sig, tau, r)
            hit += int(np.argmax(f)) == 0
        trade.append({"tau": tau, "hit": hit / 2000, "len": 2 * z * sig * math.sqrt(1 + 1 / tau ** 2)})
    # Poisson thinning on a count
    xp = r.poisson(8.0, 100000)
    a, b = Z.thin_poisson(xp, 0.5, r)
    return {"K": K, "mu": mu[:3], "methods": out, "trade": trade,
            "thin": {"corr": float(np.corrcoef(a, b)[0, 1]), "mean_a": float(a.mean()), "mean_b": float(b.mean())}}


def compute_knockoffs():
    from explainer.stats.kit import multiple as M

    r = rng(5607)
    n, p, k, q = 300, 100, 15, 0.1
    rho = 0.4
    Sigma = rho ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    Lc = np.linalg.cholesky(Sigma)
    fdp, power, ratio = [], [], []
    for _ in range(40):
        X = r.standard_normal((n, p)) @ Lc.T
        beta = np.zeros(p)
        idx = r.choice(p, k, replace=False)
        beta[idx] = 0.28 * r.choice([-1, 1], k)
        y = X @ beta + r.standard_normal(n)
        Xk = Z.gaussian_knockoffs(X, Sigma, r)
        W = Z.lasso_W(X, Xk, y, 0.05)
        T = M.knockoff_threshold(W, q, plus=True)
        sel = W >= T
        null = beta == 0
        fdp.append(np.sum(sel & null) / max(1, sel.sum()))
        power.append(np.sum(sel & ~null) / k)
        vplus = np.sum((W >= T) & null) if np.isfinite(T) else 0
        vminus = np.sum((W <= -T) & null) if np.isfinite(T) else 0
        ratio.append(vplus / (1 + vminus))
    return {"n": n, "p": p, "k": k, "q": q, "fdr": float(np.mean(fdp)), "power": float(np.mean(power)), "ratio": float(np.mean(ratio)),
            "fdp": fdp, "power_samples": power, "ratio_samples": ratio,
            "fdr_mcse": Z.mcse(fdp), "power_mcse": Z.mcse(power), "ratio_mcse": Z.mcse(ratio)}


def compute_conformal():
    X, y, names = museum.breast_cancer()
    r = rng(5608)
    n = len(y)
    out = {"n": int(n), "runs": []}
    fdps, pows, nsel = [], [], []
    for rep in range(50):
        o = r.permutation(n)
        tr, ca, te = o[:250], o[250:400], o[400:]
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        Xt = (X - mu) / sd
        from explainer.stats.kit.learn import logistic_ridge

        w = logistic_ridge(Xt[tr], y[tr], 1.0)
        score = lambda Z_: w[0] + Z_ @ w[1:]  # noqa: E731
        sel = Z.conformal_selection(score(Xt[ca]), y[ca], score(Xt[te]), c=0.5, q=0.1)["selected"]
        yt = y[te]
        fdps.append(np.sum(sel & (yt <= 0.5)) / max(1, sel.sum()))
        pows.append(np.sum(sel & (yt > 0.5)) / max(1, np.sum(yt > 0.5)))
        nsel.append(int(sel.sum()))
        out["runs"].append(dict(fdp=float(fdps[-1]), power=float(pows[-1]), n_selected=nsel[-1],
                                false_selected=int(np.sum(sel & (yt<=.5))), n_positive=int(np.sum(yt>.5))))
    out.update({"fdr": float(np.mean(fdps)), "power": float(np.mean(pows)), "nsel": float(np.mean(nsel)), "n_test": n - 400,
                "malignant_share": float(np.mean(y)), "fdp_mcse": Z.mcse(fdps), "power_mcse": Z.mcse(pows),
                "scope": "50 random splits conditional on this fixed dataset; not 50 independent clinical studies"})
    return out


def compute_microarray():
    t, z = museum.prostate_z()
    o = np.argsort(-z)
    w = Z.winner_conditional(z)
    h = Z.winner_hybrid(z)
    return {"m": len(z), "top": z[o[:5]], "j": w["j"], "z": w["y"], "second": w["second"], "cond": [w["lo"], w["hi"]],
            "median_unbiased": w["median_unbiased"], "naive": w["naive"], "hybrid": [h["lo"], h["hi"]], "proj": h["projection"]}


def compute_cluster():
    er, _ = museum.faithful()
    nw = museum.newcomb()
    nw = nw[nw > 0]
    out = {}
    for name, x in (("faithful", er), ("newcomb", nw)):
        s = float(np.std(x, ddof=1))
        res = Z.clustering_pvalues(x, sigma=s, grid=4001)
        out[name] = {"x": x, "sigma": s, "naive": res["naive"], "selective": res["selective"], "n": res["n"], "d": res["d"],
                     "selection_intervals": res["intervals"], "scope": "Gaussian working model with empirical scale; not a certified upper sigma or an exact historical p-value",
                     "cut": float((np.max(x[res["labels"] == 0]) + np.min(x[res["labels"] == 1])) / 2)}
    r = rng(5609)
    ps = [Z.clustering_pvalues(r.normal(0, 1, 40), grid=1001) for _ in range(1500)]
    out["null"] = {"selective": [q["selective"] for q in ps], "naive": [q["naive"] for q in ps]}
    return out


def compute_board():
    r = rng(5610)
    rows = []
    # winners: K = 10, one effect of 1
    mu = np.zeros(10)
    mu[0] = 1.0
    c = {"naive": 0, "cond": 0, "hybrid": 0}
    reps = 4000
    for _ in range(reps):
        y = mu + r.standard_normal(10)
        w = Z.winner_conditional(y)
        h = Z.winner_hybrid(y)
        j = w["j"]
        c["naive"] += w["naive"][0] <= mu[j] <= w["naive"][1]
        c["cond"] += w["lo"] <= mu[j] <= w["hi"]
        c["hybrid"] += h["lo"] <= mu[j] <= h["hi"]
    st = r"the largest of 10 means"
    rows += [Row(56, r"Wald interval for the winner", st, "coverage", 0.95, c["naive"] / reps, reps),
             Row(56, r"conditional interval (truncated normal)", st, "coverage", 0.95, c["cond"] / reps, reps),
             Row(56, r"hybrid interval (Andrews et al.)", st, "coverage", 0.95, c["hybrid"] / reps, reps)]
    lz = load("lasso")["sim"]
    rows += [Row(56, r"OLS intervals after the lasso", r"Stamey's design, \ fixed $\lambda$", "coverage", 0.95, lz["naive"], lz["reps"], mc_se=lz["naive_mcse"]),
             Row(56, r"selective intervals (polyhedral lemma)", r"Stamey's design, \ fixed $\lambda$", "coverage", 0.95, lz["selective"], lz["reps"], mc_se=lz["selective_mcse"]) ]
    fi = load("fission")["methods"]
    rows += [Row(56, r"data fission, \ $\tau = 1$", r"the largest of 20 means", "coverage", 0.95, fi["fission"]["coverage"], 3000)]
    for row in rows:
        if row.mc_se is None: row.mc_se=math.sqrt(row.achieved*(1-row.achieved)/row.reps)
    save_rows(56, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows]}


ITEMS = {
    "hook": compute_hook, "winners": compute_winners, "posi": compute_posi, "lasso": compute_lasso, "carving": compute_carving,
    "fission": compute_fission, "knockoffs": compute_knockoffs, "conformal": compute_conformal, "microarray": compute_microarray,
    "cluster": compute_cluster, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
