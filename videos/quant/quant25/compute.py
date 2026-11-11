"""Every number in Part 25 (The Factor Zoo), computed and cached in .cache/quant25/.

    python -m videos.quant.quant25.compute [items] [--force]

The zoo is Chen and Zimmermann's Open Source Asset Pricing release 2024.10: 212 published predictors, each as its
original paper's long-short portfolio, monthly (percent). Research uses data to December 2020; the hold-out (2021-01
to 2023-12, the release's end) is read once, in ``envelope``, for the two strategies registered there.

* ``zoo``        each predictor's publication year, original t, reproduced t in the original sample, post-publication
                 t (to 2020); the count by year; Bonferroni's hurdle as the count grows; Harvey, Liu and Zhu's t > 3;
* ``noise``      the best t-statistic among n strategies of pure noise;
* ``mtest``      Bonferroni, Holm and Benjamini-Hochberg discoveries among the predictors, in sample and after
                 publication;
* ``shrink``     empirical-Bayes shrinkage of the t's against the decay seen after publication; by data category;
* ``kns``        Kozak, Nagel and Santosh's shrinkage SDF on 154 predictors complete since 1973: the cross-validated
                 path, the chosen shrinkage, the SDF portfolio;
* ``pca``        PCA and RP-PCA of the zoo: variance, and the out-of-sample Sharpe ratio of K components;
* ``fgx``        Feng, Giglio and Xiu's double selection: do recent factors add to the older zoo?
* ``weak``       a simulation: Fama-MacBeth premia of strong and weak factors;
* ``models``     every subset of nine classic factors ranked by the squared Sharpe ratio, in and out of sample;
* ``envelope``   the shrinkage SDF and the zoo's equal-weight portfolio, registered and opened on 2021-23.
"""

from __future__ import annotations

import inspect
import itertools
import json

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import econ as E, factors as FA, pit, track, zoo as Z
from videos.quant.quant3.compute import _osap, _osap_matrix

CACHE = Cache("quant25")
load = pit.counted(CACHE.load, 25)
END = 202012
START = 197301


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _int(s):
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return None


def _flt(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def _records():
    ym, names, R = _osap_matrix()
    _, doc = _osap()
    y = ym // 100
    recs = []
    for j, c in enumerate(names):
        d = doc.get(c)
        if not d:
            continue
        s0, s1, py = _int(d["SampleStartYear"]), _int(d["SampleEndYear"]), _int(d["Year"])
        if None in (s0, s1, py):
            continue
        x = R[:, j]
        ins = x[(y >= s0) & (y <= s1) & np.isfinite(x)]
        post = x[(y > py) & (ym <= END) & np.isfinite(x)]
        if len(ins) < 24:
            continue
        recs.append({"name": c, "year": py, "s0": s0, "s1": s1, "cat": d["Cat.Data"], "econ": d["Cat.Economic"],
                     "t_op": _flt(d["T-Stat"]), "t_in": Z.tstat(ins), "mean_in": float(ins.mean()),
                     "t_post": Z.tstat(post) if len(post) >= 24 else None,
                     "mean_post": float(post.mean()) if len(post) >= 24 else None, "n_post": int(len(post)),
                     "clear": d["Predictability in OP"] == "1_clear", "j": j})
    return ym, names, R, recs


def compute_zoo() -> dict:
    _, _, _, recs = _records()
    years = np.arange(1970, 2017)
    count = np.array([sum(r_["year"] <= yy for r_ in recs) for yy in years])
    return _json({"recs": [{k: v for k, v in r_.items() if k != "j"} for r_ in recs], "years": years, "count": count,
                  "hurdle": Z.bonferroni_t(np.maximum(count, 1)), "n": len(recs),
                  "share_t3": float(np.mean([r_["t_in"] > 3 for r_ in recs])),
                  "share_t2": float(np.mean([r_["t_in"] > 1.96 for r_ in recs]))})


def compute_noise() -> dict:
    ns = [1, 5, 10, 20, 50, 100, 200, 500, 1000]
    out = [dict(Z.noise_max_t(n, 240, 3000, seed=n), n=n) for n in ns]
    a200 = Z.noise_max_t(200, 240, 4000, seed=7, absolute=True)
    rng = np.random.default_rng(25)
    ex = rng.standard_normal((240, 200)) * 0.04
    ts = ex.mean(0) / ex.std(0, ddof=1) * np.sqrt(240)
    return _json({"ns": ns, "rows": out, "abs200": a200, "example_t": ts, "example_best": float(ts.max())})


def compute_mtest() -> dict:
    _, _, _, recs = _records()
    t_in = np.array([r_["t_in"] for r_ in recs])
    p_in = 2 * stats.norm.sf(np.abs(t_in))
    post = [r_ for r_ in recs if r_["t_post"] is not None]
    t_po = np.array([r_["t_post"] for r_ in post])
    p_po = 2 * stats.norm.sf(np.abs(t_po))
    p_po1 = stats.norm.sf(t_po)  # one-sided: the published sign

    def disc(p):
        return {"raw": int((p < 0.05).sum()), "bonferroni": int(E.bonferroni(p).sum()), "holm": int(E.holm(p).sum()),
                "bh": int(E.benjamini_hochberg(p, 0.05).sum()), "n": int(len(p))}
    return _json({"in": disc(p_in), "post": disc(p_po1), "post_two": disc(p_po), "t_in": t_in, "t_post": t_po,
                  "hurdle_bonf": float(Z.bonferroni_t(len(p_in))),
                  "bh_cut_post": float(np.sort(p_po1)[max(E.benjamini_hochberg(p_po1, 0.05).sum() - 1, 0)])})


def compute_shrink() -> dict:
    _, _, _, recs = _records()
    t_in = np.array([r_["t_in"] for r_ in recs])
    eb = Z.eb_shrink(t_in)
    post = [r_ for r_ in recs if r_["mean_post"] is not None]
    mi = np.array([r_["mean_in"] for r_ in post])
    mp = np.array([r_["mean_post"] for r_ in post])
    slope = float(np.polyfit(mi, mp, 1)[0])
    ratio = float(mp.mean() / mi.mean())
    cats = {}
    for c in sorted(set(r_["cat"] for r_ in post)):
        q = [r_ for r_ in post if r_["cat"] == c]
        if len(q) >= 6:
            cats[c] = {"n": len(q), "ratio": float(np.mean([r_["mean_post"] for r_ in q]) / np.mean([r_["mean_in"] for r_ in q]))}
    clear = [r_ for r_ in post if r_["clear"]]
    likely = [r_ for r_ in post if not r_["clear"]]
    return _json({"eb": {k: v for k, v in eb.items() if k != "post"}, "slope": slope, "ratio": ratio,
                  "mean_in": float(mi.mean()), "mean_post": float(mp.mean()), "n": len(post), "cats": cats,
                  "mi": mi, "mp": mp,
                  "clear_ratio": float(np.mean([r_["mean_post"] for r_ in clear]) / np.mean([r_["mean_in"] for r_ in clear])),
                  "likely_ratio": float(np.mean([r_["mean_post"] for r_ in likely]) / np.mean([r_["mean_in"] for r_ in likely]))})


def _panel(start=START, end=END):
    ym, names, R, recs = _records()
    keep = [r_ for r_ in recs if np.isfinite(R[(ym >= start) & (ym <= 202312), r_["j"]]).all()]
    m = (ym >= start) & (ym <= end)
    F = R[m][:, [r_["j"] for r_ in keep]] / 100
    return ym[m], F, keep


KAPPAS = np.geomspace(0.01, 1.0, 20)  # root expected squared Sharpe ratio, per month: 0.035 to 3.5 a year


def compute_kns() -> dict:
    d, F, keep = _panel()
    T = len(F)
    S = np.cov(F.T)
    gam = [Z.kns_kappa_gamma(S, T, k) for k in KAPPAS]
    cv = Z.kns_cv(F, gam, folds=3)
    jb = int(np.argmax(cv["r2"]))
    b = Z.kns_b(F.mean(0), S, gam[jb])
    sdf = F @ b
    sdf = sdf / sdf.std() * 0.10 / np.sqrt(12)  # scaled to 10% a year
    # unpenalised tangency, and the in-sample R^2 along the path
    r2_in = [1 - np.sum((F.mean(0) - S @ Z.kns_b(F.mean(0), S, g)) ** 2) / np.sum(F.mean(0) ** 2) for g in gam]
    # a sharp out-of-sample check inside the research window: fit 1973-2000, hold 2001-2020
    a = d <= 200012
    Sa = np.cov(F[a].T)
    ba = Z.kns_b(F[a].mean(0), Sa, Z.kns_kappa_gamma(Sa, int(a.sum()), KAPPAS[jb]))
    b0 = Z.kns_b(F[a].mean(0), Sa, 1e-10 * np.trace(Sa))
    ew = F.mean(1)
    pc = Z.pca(F)

    def scaled(w):  # a portfolio scaled to 10% a year on the fitting window, then held
        k = 0.10 / np.sqrt(12) / (F[a] @ w).std()
        return F[a] @ w * k, F[~a] @ w * k
    ki, ko = scaled(ba)
    ti, to = scaled(b0)
    ei, eo = scaled(np.ones(F.shape[1]))
    mu_b, S_b = F[~a].mean(0), np.cov(F[~a].T)
    split = {"kns_in": FA.stats(ki), "kns_oos": FA.stats(ko), "tan_in": FA.stats(ti), "tan_oos": FA.stats(to),
             "ew_in": FA.stats(ei), "ew_oos": FA.stats(eo), "r2_kns_oos": Z._r2(mu_b, S_b, ba),
             "r2_tan_oos": Z._r2(mu_b, S_b, b0)}
    return _json({"kappas": KAPPAS * np.sqrt(12), "r2_cv": cv["r2"], "r2_in": r2_in, "best_kappa": KAPPAS[jb] * np.sqrt(12),
                  "N": F.shape[1], "T": T, "names": [r_["name"] for r_ in keep],
                  "b_top": sorted(zip([r_["name"] for r_ in keep], b * np.sqrt(np.diag(S))), key=lambda z: -abs(z[1]))[:10],
                  "sdf_stats": FA.stats(sdf), "ew_stats": FA.stats(ew),
                  "split": split,
                  "pc_loadings_share": float(np.sum((pc["V"].T @ b) [:5] ** 2) / np.sum((pc["V"].T @ b) ** 2))})


def compute_pca() -> dict:
    d, F, keep = _panel()
    pc = Z.pca(F)
    a = d <= 200012
    out = {"share": pc["share"][:20], "cum": np.cumsum(pc["share"])[:20], "K": list(range(1, 11)), "pca": [], "rp": []}
    Fa, Fb = F[a], F[~a]
    for K in range(1, 11):
        for nm, V in (("pca", Z.pca(Fa)["V"]), ("rp", Z.rp_pca(Fa, 10.0)["V"])):
            W = V[:, :K]
            fa, fb = Fa @ W, Fb @ W
            w = np.linalg.solve(np.atleast_2d(np.cov(fa.T)), fa.mean(0))
            pin, pout = fa @ w, fb @ w
            # cross-sectional fit out of sample: alphas of the test portfolios on the K factors
            X = np.c_[np.ones(len(fb)), fb]
            coef = np.linalg.lstsq(X, Fb, rcond=None)[0]
            rms = float(np.sqrt(np.mean(coef[0] ** 2)) * 12 * 100)
            out[nm].append({"sr_in": float(pin.mean() / pin.std() * np.sqrt(12)),
                            "sr_out": float(pout.mean() / pout.std() * np.sqrt(12)), "rms_alpha": rms})
    rms0 = float(np.sqrt(np.mean(Fb.mean(0) ** 2)) * 12 * 100)
    out["rms_none"] = rms0
    out["N"] = F.shape[1]
    return _json(out)


def compute_fgx() -> dict:
    d, F, keep = _panel()
    yrs = np.array([r_["year"] for r_ in keep])
    old = np.flatnonzero(yrs <= 2003)
    new = np.flatnonzero(yrs >= 2011)
    res = []
    for g in new:
        others = np.setdiff1d(np.arange(F.shape[1]), np.r_[old, g])
        R = F[:, others]
        H = F[:, old]
        T, N = R.shape
        Rc = R - R.mean(0)
        CH = Rc.T @ (H - H.mean(0)) / (T - 1)
        mu = R.mean(0)
        lam = float(np.std(mu) * np.sqrt(2 * np.log(H.shape[1]) / N))
        lam2 = float(np.std(Rc.T @ (F[:, g] - F[:, g].mean()) / (T - 1)) * np.sqrt(2 * np.log(H.shape[1]) / N))
        ds = Z.double_selection(R, F[:, g], H, lam, lam2)
        # the naive test: g alone
        Cg = Rc.T @ (F[:, g] - F[:, g].mean()) / (T - 1)
        X = np.c_[np.ones(N), Cg]
        coef = np.linalg.lstsq(X, mu, rcond=None)[0]
        e = mu - X @ coef
        XtX = np.linalg.inv(X.T @ X)
        Vv = XtX @ (X.T * e ** 2) @ X @ XtX
        res.append({"name": keep[g]["name"], "year": int(yrs[g]), "t_ds": ds["t"], "t_naive": float(coef[1] / np.sqrt(Vv[1, 1])),
                    "t_mean": Z.tstat(F[:, g]), "selected": len(ds["selected"])})
    return _json({"rows": res, "n_old": int(len(old)), "n_new": int(len(new)),
                  "sig_naive": int(sum(abs(r_["t_naive"]) > 1.96 for r_ in res)),
                  "sig_ds": int(sum(abs(r_["t_ds"]) > 1.96 for r_ in res)),
                  "sig_mean": int(sum(r_["t_mean"] > 1.96 for r_ in res))})


def compute_weak() -> dict:
    rng = np.random.default_rng(2025)
    N, T, lam, sims = 50, 480, 0.005, 400
    out = {}
    for nm, s in (("strong", 1.0), ("weak", 0.05)):
        est = []
        for _ in range(sims):
            beta = s * rng.normal(1.0, 0.5, N)
            f = lam + 0.04 * rng.standard_normal(T)
            R = np.outer(f, beta) + 0.05 * rng.standard_normal((T, N))
            tp = E.two_pass(R, f[:, None], shanken=False)
            est.append(tp["lambda"][1])
        est = np.array(est)
        out[nm] = {"est": est, "median": float(np.median(est)), "p10": float(np.percentile(est, 10)),
                   "p90": float(np.percentile(est, 90))}
    out["true"] = lam
    return _json(out)


def compute_models() -> dict:
    f = data.ken_french_monthly("F-F_Research_Data_5_Factors_2x3_CSV.zip", "ff5_monthly", "2025-12")
    m = data.ken_french_monthly("F-F_Momentum_Factor_CSV.zip", "mom_monthly", "2025-12")
    q = data.q_factors("2025-12")
    d = f["date"][(f["date"] >= 196701) & (f["date"] <= END)]

    def on(dd, x):
        idx = {int(a): i for i, a in enumerate(dd)}
        return np.array([x[idx[int(a)]] for a in d])
    cols = {"MKT": on(f["date"], f["returns"][:, 0]), "SMB": on(f["date"], f["returns"][:, 1]),
            "HML": on(f["date"], f["returns"][:, 2]), "RMW": on(f["date"], f["returns"][:, 3]),
            "CMA": on(f["date"], f["returns"][:, 4]), "UMD": on(m["date"], m["returns"][:, 0]),
            "ME": on(q["date"], q["R_ME"]), "IA": on(q["date"], q["R_IA"]), "ROE": on(q["date"], q["R_ROE"]),
            "EG": on(q["date"], q["R_EG"])}
    names = list(cols)
    X = np.c_[tuple(cols[k] for k in names)]
    a = d <= 199312
    rows = []
    for k in range(1, 7):
        for sub in itertools.combinations(range(len(names)), k):
            if 0 not in sub:
                continue  # every model keeps the market
            Fa, Fb = X[a][:, sub], X[~a][:, sub]
            w = np.linalg.solve(np.atleast_2d(np.cov(Fa.T)), Fa.mean(0))
            po = Fb @ w
            rows.append({"model": [names[i] for i in sub], "sh2_in": Z.max_sh2(Fa) * 12, "sh2_full": Z.max_sh2(X[:, sub]) * 12,
                         "sr_out": float(po.mean() / po.std() * np.sqrt(12))})
    rows.sort(key=lambda r_: -r_["sh2_in"])
    named = {"CAPM": ["MKT"], "FF3": ["MKT", "SMB", "HML"], "Carhart": ["MKT", "SMB", "HML", "UMD"],
             "FF5": ["MKT", "SMB", "HML", "RMW", "CMA"], "FF6": ["MKT", "SMB", "HML", "RMW", "CMA", "UMD"],
             "q4": ["MKT", "ME", "IA", "ROE"], "q5": ["MKT", "ME", "IA", "ROE", "EG"]}
    nm = {k: next(r_ for r_ in rows if r_["model"] == v) for k, v in named.items()}
    by_out = sorted(rows, key=lambda r_: -r_["sr_out"])
    return _json({"top_in": rows[:8], "top_out": by_out[:8], "named": nm, "n_models": len(rows),
                  "all": [[r_["sh2_in"], r_["sr_out"]] for r_ in rows],
                  "rank_corr": float(stats.spearmanr([r_["sh2_in"] for r_ in rows], [r_["sr_out"] for r_ in rows])[0])})


# ---------------------------------------------------------------------------
# The hold-out
# ---------------------------------------------------------------------------
def _sdf_weights():
    d, F, keep = _panel()
    S = np.cov(F.T)
    gam = [Z.kns_kappa_gamma(S, len(F), k) for k in KAPPAS]
    cv = Z.kns_cv(F, gam, folds=3)
    b = Z.kns_b(F.mean(0), S, cv["best"])
    scale = 0.10 / np.sqrt(12) / (F @ b).std()
    return [r_["j"] for r_ in keep], b * scale


def compute_envelope() -> dict:
    ym, names, R = _osap_matrix()
    cols, w = _sdf_weights()
    code = inspect.getsource(_sdf_weights) + inspect.getsource(Z.kns_cv) + inspect.getsource(Z.kns_b) + \
        inspect.getsource(_panel) + repr(KAPPAS.tolist())
    rule = {"universe": "OSAP 2024.10 predictors complete 1973-2023 (154)", "fit": "1973-01 to 2020-12",
            "kappa_grid": len(KAPPAS), "folds": 3, "scale": "10% a year in sample", "cost_per_year": 0.02}
    reg = {"kns_sdf_part25": pit.register("kns_sdf_part25", code, rule, trials=len(KAPPAS)),
           "zoo_equal_weight_part25": pit.register("zoo_equal_weight_part25", code, dict(rule, weights="equal"), trials=1)}
    stamp = ym * 100 + 1
    allv = np.nan_to_num(R, nan=-999)
    out = {}
    for strat, ww in (("kns_sdf_part25", w), ("zoo_equal_weight_part25", None)):
        hd, hv = pit.open_envelope(strat, "osap/2024.10/PredictorLSretWide", stamp, allv)
        H = hv[:, cols] / 100
        m_res = (ym >= START) & (ym <= END)
        Fr = R[m_res][:, cols] / 100
        if ww is None:
            res, hold = Fr.mean(1), H.mean(1)
            cost = 0.01
        else:
            res, hold = Fr @ ww, H @ ww
            cost = 0.02
        row = track.record(strat, 25, res, hold, cost, note=json.dumps(rule))
        out[strat] = dict(row, holdout_cum=FA.cumulative(hold), holdout_dates=hd // 100)
    return _json({"rows": out, "registered": reg, "trials": pit.trials_so_far()})


def compute_discovery_theory() -> dict:
    """The research chapter: how many anomalies are real?  Benjamini and Hochberg's step-up rule controls the false
    discovery rate at pi0 q under independence; Storey (2002) estimates the share of true nulls pi0 from the flat
    right side of the p-value histogram, pi0(lambda) = #{p > lambda}/(m(1 - lambda)); Efron's two-group model gives each
    hypothesis a local false discovery rate lfdr(z) = pi0 phi(z)/f(z).  Checked by simulation; then applied to the 208
    anomalies' post-publication t-statistics, which, unlike the in-sample ones, were not selected for significance."""
    from scipy.stats import gaussian_kde
    rng = np.random.default_rng(2525)
    m = 208
    sims = []
    for pi0 in (0.3, 0.5, 0.8):
        fdr, pis, power = [], [], []
        for _ in range(400):
            null = rng.random(m) < pi0
            mu = np.where(null, 0.0, rng.gamma(2.0, 1.0, m))
            t = mu + rng.standard_normal(m)
            p = stats.norm.sf(t)
            o = np.argsort(p)
            k = np.where(p[o] <= 0.10 * np.arange(1, m + 1) / m)[0]
            rej = np.zeros(m, bool)
            if len(k):
                rej[o[: k.max() + 1]] = True
            fdr.append(float((rej & null).sum() / max(rej.sum(), 1)))
            power.append(float((rej & ~null).sum() / max((~null).sum(), 1)))
            pis.append(float(np.mean(p > 0.5) / 0.5))
        sims.append({"pi0": pi0, "fdr": float(np.mean(fdr)), "fdr_bound": 0.10 * pi0, "pi0_hat": float(np.mean(pis)),
                     "pi0_hat_sd": float(np.std(pis)), "power": float(np.mean(power))})
    _, _, _, recs = _records()
    post = [r_ for r_ in recs if r_["t_post"] is not None]
    tp = np.array([r_["t_post"] for r_ in post])
    ti = np.array([r_["t_in"] for r_ in recs])
    p_post = stats.norm.sf(tp)                    # one-sided, in the published direction
    p_in = stats.norm.sf(ti)
    lams = np.linspace(0.05, 0.9, 18)
    pi0_curve = [float(min(1.0, np.mean(p_post > l_) / (1 - l_))) for l_ in lams]
    pi0 = float(min(1.0, np.mean(p_post > 0.5) / 0.5))
    pi0_in = float(min(1.0, np.mean(p_in > 0.5) / 0.5))
    # Efron's local fdr with a kernel estimate of the mixture density
    kde = gaussian_kde(tp)
    lfdr = np.minimum(1.0, pi0 * stats.norm.pdf(tp) / kde(tp))
    zz = np.linspace(-4, 7, 221)
    names = [r_["name"] for r_ in post]
    order = np.argsort(lfdr)
    # BH at 10% with and without the pi0 adjustment
    o = np.argsort(p_post)
    k1 = np.where(p_post[o] <= 0.10 * np.arange(1, len(tp) + 1) / len(tp))[0]
    k2 = np.where(p_post[o] <= 0.10 / max(pi0, 1e-9) * np.arange(1, len(tp) + 1) / len(tp))[0]
    out = {"sims": sims, "m": int(len(tp)), "t_post": tp, "t_in": ti, "p_post_hist": np.histogram(p_post, bins=20, range=(0, 1))[0],
           "p_in_hist": np.histogram(p_in, bins=20, range=(0, 1))[0], "lams": lams, "pi0_curve": pi0_curve, "pi0": pi0,
           "pi0_in": pi0_in, "density_z": zz, "density_f": kde(zz), "density_null": pi0 * stats.norm.pdf(zz),
           "lfdr": lfdr, "n_lfdr_02": int(np.sum(lfdr < 0.2)), "expected_true": float(np.sum(1 - lfdr)),
           "bh10": int(k1.max() + 1) if len(k1) else 0, "storey_bh10": int(k2.max() + 1) if len(k2) else 0,
           "best": [{"name": names[i], "t_post": float(tp[i]), "lfdr": float(lfdr[i])} for i in order[:8]]}
    return _json(out)


ITEMS = {"discovery_theory": compute_discovery_theory, "zoo": compute_zoo, "noise": compute_noise, "mtest": compute_mtest, "shrink": compute_shrink,
         "kns": compute_kns, "pca": compute_pca, "fgx": compute_fgx, "weak": compute_weak, "models": compute_models,
         "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
