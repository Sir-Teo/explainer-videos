"""Precompute every number in Part 41 of *Statistics, Built* ("What You Didn't See").

    OMP_NUM_THREADS=1 python -m videos.stats.stats41.compute            # everything missing (about ten minutes)
    python -m videos.stats.stats41.compute --force board

Results are cached in ``.cache/stats41/<name>.json``.  New York's air quality, NHANES and Mroz's women are the
Museum's; the survey sample with its three masks, the election and the opt-in poll are the World's; the rest are seeded
simulations.

Items:
    wald        a stylized version of Wald's bombers: hits by area on all planes, on the returners, and Wald's estimate
    mech        the World's income under MCAR, MAR and MNAR masks: complete cases, EM, MI and IPW against the truth
    sins        mean imputation's shrunken SD and correlation; LOCF in a seeded trial with dropout
    em          New York's ozone: complete cases vs EM, the EM path and its likelihood
    mice        New York's ozone regression by chained equations and Rubin's rules; NHANES's missing pressures
    weight      IPW and AIPW for the World's MAR mask; misspecified models and double robustness
    heckman     Mroz's women: OLS, Heckman's two steps, ML
    tipping     delta-adjusted MI on the World's MNAR mask
    mrp         an opt-in poll of the World: raw, raked and MRP estimates of the election, overall and by region
    meas        NHANES's two sodium recalls: reliability, attenuation, regression calibration, SIMEX; a seeded truth
    misclass    a seeded case-control study with misclassified exposure: observed, corrected, differential
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import mi as MI
from explainer.stats.world import World

CACHE = Cache("stats41")
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


def eff_reps(per_rep, nominal=0.9) -> int:
    v = np.var(np.asarray(per_rep, float), ddof=1) / len(per_rep)
    return int(round(nominal * (1 - nominal) / max(v, 1e-12)))


def compute_wald():
    """Planes take hits uniformly over their surface; the chance a hit downs a plane depends on where it lands.
    The returners show few engine hits, because engine hits are the ones that kill."""
    g = rng(4101)
    areas = ["engines", "fuselage", "fuel system", "wings and tail"]
    share = np.array([0.15, 0.35, 0.10, 0.40])  # of surface
    kill = np.array([0.40, 0.05, 0.25, 0.04])  # chance one hit there downs the plane
    n = 2000
    hits = g.poisson(4.0, n)
    where = [g.choice(4, h, p=share) for h in hits]
    counts = np.array([np.bincount(w, minlength=4) for w in where])
    survive = np.array([np.prod((1 - kill) ** c) for c in counts]) > g.random(n)
    all_hits = counts.sum(0)
    ret_hits = counts[survive].sum(0)
    # Wald's logic: expected hits by area among all planes vs among returners
    expect = share * counts[survive].sum() / share.sum()
    return nest({"areas": areas, "share": share, "kill": kill, "n": n, "returned": int(survive.sum()), "all_hits": all_hits,
                 "ret_hits": ret_hits, "expected_if_harmless": expect, "ret_share": ret_hits / ret_hits.sum(),
                 "deficit": 1 - ret_hits / expect, "deficit_scope": "relative area-normalized share deficit, not per-hit kill probability", "expected_return_share": share * (1-kill) / np.sum(share*(1-kill))})


def compute_mech():
    W = World()
    m = W.missing
    li, age, male, region, bmi = m["log_income"], m["age"], m["male"].astype(float), m["region"], m["bmi"]
    truth = float(li.mean())
    R = (region[:, None] == np.arange(10)[None, :]).astype(float)[:, 1:]
    X = np.column_stack([age / 10, (age / 10) ** 2, male, bmi, R])
    out = {"truth": truth, "n": len(li)}
    g = rng(4102)
    for k in ("mcar", "mar", "mnar"):
        miss = m[k]
        yo = np.where(miss, np.nan, li)
        cc = float(np.nanmean(yo))
        se_cc = float(np.nanstd(yo, ddof=1) / math.sqrt((~miss).sum()))
        ests, vs = [], []
        for _ in range(20):
            yy = MI.impute_norm(yo, X, g, "proper")
            ests.append(yy.mean())
            vs.append(yy.var(ddof=1) / len(yy))
        r = MI.rubin(ests, vs, df_complete=len(li) - 1)
        rm = MI.response_model((~miss).astype(float), X)
        ipw = MI.ipw_mean(li, (~miss).astype(float), rm["p"])
        ipw_true = MI.ipw_mean(li, (~miss).astype(float), 1 - m["p_" + k])
        out[k] = {"rate": float(miss.mean()), "cc": cc, "cc_se": se_cc, "mi": r["est"], "mi_ci": r["ci"], "mi_fmi": r["fmi"],
                  "ipw": ipw["est"], "ipw_se": ipw["se"], "ipw_true_p": ipw_true["est"],
                  "miss_age": float(age[miss].mean()), "obs_age": float(age[~miss].mean()),
                  "miss_inc": float(li[miss].mean()), "obs_inc": float(li[~miss].mean())}
    # a grid for the mask picture: 24 respondents x 6 variables
    pick = np.arange(24)
    out["grid"] = {"age": age[pick], "income": li[pick], "mcar": m["mcar"][pick], "mar": m["mar"][pick], "mnar": m["mnar"][pick],
                   "sbp_miss": m["sbp_miss"][pick]}
    out["corr_age_income"] = float(np.corrcoef(age, li)[0, 1])
    return nest(out)


def compute_sins():
    W = World()
    m = W.missing
    li, age = m["log_income"], m["age"]
    miss = m["mcar"]
    yo = np.where(miss, np.nan, li)
    mean_imp = np.where(miss, np.nanmean(yo), li)
    g = rng(4103)
    X = np.column_stack([age / 10, m["male"].astype(float), m["bmi"]])
    reg_imp = MI.impute_norm(yo, X, g, "mean")
    prop = MI.impute_norm(yo, X, g, "proper")
    stat = lambda y: {"sd": float(np.std(y, ddof=1)), "corr": float(np.corrcoef(y, age)[0, 1]), "mean": float(np.mean(y))}  # noqa: E731
    tab = {"truth": stat(li), "cc": {"sd": float(np.nanstd(yo, ddof=1)), "corr": float(np.corrcoef(yo[~miss], age[~miss])[0, 1]), "mean": float(np.nanmean(yo))},
           "mean_imp": stat(mean_imp), "reg_imp": stat(reg_imp), "proper": stat(prop)}
    # LOCF: a seeded trial; symptom scores worsen by 2 a month on placebo and 1 on drug; the worse drop out
    n, T = 300, 6
    arm = np.repeat([0, 1], n // 2)
    slope = np.where(arm == 1, 1.0, 2.0)
    u = g.normal(0, 3, n)
    Y = 20 + u[:, None] + slope[:, None] * np.arange(T)[None, :] + g.normal(0, 2, (n, T))
    drop = np.full(n, T)
    for i in range(n):
        for t in range(1, T):
            if g.random() < 1 / (1 + np.exp(-(-3.5 + 0.12 * (Y[i, t - 1] - 25)))) * (1.6 if arm[i] == 1 else 1.0):
                drop[i] = t
                break
    Yobs = np.where(np.arange(T)[None, :] < drop[:, None], Y, np.nan)
    locf = np.array([np.where(np.isnan(r), r[~np.isnan(r)][-1], r) for r in Yobs])
    true_diff = float(Y[arm == 1, -1].mean() - Y[arm == 0, -1].mean())
    locf_diff = float(locf[arm == 1, -1].mean() - locf[arm == 0, -1].mean())
    cc_last = Yobs[:, -1]
    cc_diff = float(np.nanmean(cc_last[arm == 1]) - np.nanmean(cc_last[arm == 0]))
    # MAR-based: impute month by month from the previous month and arm (sequential regression)
    ests = []
    for _ in range(20):
        Z = Yobs.copy()
        for t in range(1, T):
            Z[:, t] = MI.impute_norm(Z[:, t], np.column_stack([Z[:, t - 1], arm]), g, "proper")
        ests.append(Z[arm == 1, -1].mean() - Z[arm == 0, -1].mean())
    means = {"true": [Y[arm == a].mean(0) for a in (0, 1)], "locf": [locf[arm == a].mean(0) for a in (0, 1)],
             "obs": [np.nanmean(Yobs[arm == a], 0) for a in (0, 1)]}
    return nest({"tab": tab, "rate": float(miss.mean()), "locf": {"true": true_diff, "locf": locf_diff, "cc": cc_diff,
                 "mi": float(np.mean(ests)), "completed": [float((drop[arm == a] == T).mean()) for a in (0, 1)], "means": means}})


def compute_em():
    a = museum.airquality(complete=False)
    X = np.column_stack([a["ozone"], a["solar"], a["wind"], a["temp"]])
    cc = X[~np.isnan(X).any(1)]
    e = MI.em_mvn(X)
    path_oz = [float(p[0][0]) for p in e["path"]]
    # a bivariate picture: ozone vs temperature, observed and EM's conditional means for the missing ozone
    mu, S = e["mu"], e["S"]
    miss = np.isnan(a["ozone"])
    o = [1, 2, 3]
    fills = []
    for i in np.flatnonzero(miss):
        row = X[i]
        ob = [j for j in o if not np.isnan(row[j])]
        B = S[np.ix_([0], ob)] @ np.linalg.inv(S[np.ix_(ob, ob)])
        fills.append(float((mu[0] + B @ (row[ob] - mu[ob]))[0]))
    return nest({"n": len(X), "n_miss_oz": int(miss.sum()), "n_miss_solar": int(np.isnan(a["solar"]).sum()), "n_cc": len(cc),
                 "cc_mean": float(cc[:, 0].mean()), "observed_ozone_mean": float(np.nanmean(a["ozone"])), "em_mean": float(mu[0]), "path": path_oz, "ll": e["ll"], "iters": e["iters"],
                 "temp": a["temp"], "ozone": a["ozone"], "miss": miss, "fills": fills,
                 "temp_miss_mean": float(a["temp"][miss].mean()), "temp_obs_mean": float(a["temp"][~miss].mean()),
                 "S": S, "mu": mu})


def ols(Xd, y):
    b = np.linalg.lstsq(Xd, y, rcond=None)[0]
    e = y - Xd @ b
    s2 = e @ e / (len(y) - Xd.shape[1])
    V = s2 * np.linalg.inv(Xd.T @ Xd)
    return b, V


def compute_mice():
    a = museum.airquality(complete=False)
    D = np.column_stack([np.log(a["ozone"]), a["solar"], a["wind"], a["temp"]])
    g = rng(4104)
    imps = MI.mice(D, m=20, iters=10, rng=g, methods={0: "pmm", 1: "pmm"})
    names = ["intercept", "solar radiation", "wind", "temperature"]
    ests, vs = [], []
    for Y in imps:
        Xd = np.column_stack([np.ones(len(Y)), Y[:, 1], Y[:, 2], Y[:, 3]])
        b, V = ols(Xd, Y[:, 0])
        ests.append(b)
        vs.append(np.diag(V))
    ests, vs = np.array(ests), np.array(vs)
    pooled = [MI.rubin(ests[:, j], vs[:, j], df_complete=len(D) - 4) for j in range(4)]
    cc = ~np.isnan(D).any(1)
    bcc, Vcc = ols(np.column_stack([np.ones(cc.sum()), D[cc, 1], D[cc, 2], D[cc, 3]]), D[cc, 0])
    # the m estimates of the temperature coefficient (for the picture)
    temp_draws = ests[:, 3]
    # NHANES: who is missing a blood pressure?
    nh = museum.nhanes()
    sbp = np.nanmean(np.column_stack([nh["sbp1"], nh["sbp2"], nh["sbp3"]]), 1)
    ms = np.isnan(sbp)
    age = nh["age"]
    bands = [(18, 30), (30, 45), (45, 60), (60, 75), (75, 81)]
    miss_by_age = [float(ms[(age >= lo) & (age < hi)].mean()) for lo, hi in bands]
    return nest({"names": names, "mi": [{"est": p["est"], "se": p["se"], "fmi": p["fmi"], "df": p["df"], "B": p["B"], "W": p["W"]} for p in pooled],
                 "cc": {"est": bcc, "se": np.sqrt(np.diag(Vcc))}, "n": len(D), "n_cc": int(cc.sum()), "temp_draws": temp_draws,
                 "nhanes": {"n": len(sbp), "miss_rate": float(ms.mean()), "bands": bands, "miss_by_age": miss_by_age}})


def compute_weight():
    W = World()
    m = W.missing
    li, age, male, region, bmi = m["log_income"], m["age"], m["male"].astype(float), m["region"], m["bmi"]
    R = (region[:, None] == np.arange(10)[None, :]).astype(float)[:, 1:]
    miss = m["mar"]
    r = (~miss).astype(float)
    truth = float(li.mean())
    X_right = np.column_stack([age, np.isin(region, [3, 8]).astype(float)])
    X_wrong = np.column_stack([bmi])
    p_right = MI.response_model(r, X_right)["p"]
    p_wrong = MI.response_model(r, X_wrong)["p"]
    D_out = np.column_stack([np.ones(len(li)), age / 10, (age / 10) ** 2, male, bmi, R])
    b = np.linalg.lstsq(D_out[r == 1], li[r == 1], rcond=None)[0]
    m_right = D_out @ b
    m_wrong = np.full(len(li), float(li[r == 1].mean()))
    res = {"truth": truth, "cc": float(li[r == 1].mean()),
           "ipw_right": MI.ipw_mean(li, r, p_right), "ipw_wrong": MI.ipw_mean(li, r, p_wrong),
           "aipw_rr": MI.aipw_mean(li, r, p_right, m_right), "aipw_rw": MI.aipw_mean(li, r, p_right, m_wrong),
           "aipw_wr": MI.aipw_mean(li, r, p_wrong, m_right), "aipw_ww": MI.aipw_mean(li, r, p_wrong, m_wrong)}
    # weights: the largest and the effective sample size
    w = r / p_right
    ess = float(w.sum() ** 2 / (w ** 2).sum())
    return nest(res | {"ess": ess, "max_w": float(w.max()), "n_obs": int(r.sum())})


def compute_heckman():
    d = museum._table("mroz87.csv")
    lfp = d["lfp"].astype(int)
    w = lfp == 1
    lw = np.where(w, np.log(np.where(d["wage"] > 0, d["wage"], 1.0)), np.nan)
    X = np.column_stack([d["educ"], d["exper"], d["exper"] ** 2])
    Z = np.column_stack([d["age"], d["kids5"], d["kids618"], d["educ"], d["exper"], d["exper"] ** 2, d["nwifeinc"]])
    b, V = ols(np.column_stack([np.ones(w.sum()), X[w]]), lw[w])
    two = MI.heckman_twostep(np.nan_to_num(lw), X, lfp, Z)
    mle = MI.heckman_mle(np.nan_to_num(lw), X, lfp, Z)
    return nest({"n": len(lfp), "n_work": int(w.sum()), "ols": {"beta": b, "se": np.sqrt(np.diag(V))},
                 "two": {"beta": two["beta"], "se": two["se"], "rho": two["rho"], "sigma": two["sigma"], "bl": two["beta_lambda"]},
                 "mle": {"beta": mle["beta"], "rho": mle["rho"], "sigma": mle["sigma"], "se": mle["se"]},
                 "gamma": two["gamma"], "mean_wage": float(d["wage"][w].mean()), "kids5_rate": [float(lfp[d["kids5"] == k].mean()) for k in (0, 1, 2)]})


def delta_curve(completions, missing, deltas):
    """Vary the sensitivity assumption using the same completed datasets at every delta."""
    completions = np.asarray(completions, float)
    rows = []
    for delta in deltas:
        shifted = completions + float(delta) * np.asarray(missing, bool)[None, :]
        estimates = shifted.mean(axis=1)
        variances = shifted.var(axis=1, ddof=1) / shifted.shape[1]
        pooled = MI.rubin(estimates, variances, df_complete=shifted.shape[1]-1)
        rows.append(dict(delta=float(delta), est=pooled['est'], lo=pooled['ci'][0], hi=pooled['ci'][1]))
    return rows


def compute_tipping():
    W = World()
    m = W.missing
    li, age, male, region, bmi = m["log_income"], m["age"], m["male"].astype(float), m["region"], m["bmi"]
    R = (region[:, None] == np.arange(10)[None, :]).astype(float)[:, 1:]
    X = np.column_stack([age / 10, (age / 10) ** 2, male, bmi, R])
    miss = m["mnar"]
    yo = np.where(miss, np.nan, li)
    g = rng(4105)
    completions = np.asarray([MI.impute_norm(yo, X, g, "proper") for _ in range(20)])
    deltas = np.round(np.arange(0, 1.01, .1), 2)
    rows = delta_curve(completions, miss, deltas)
    true_shift = float((li.mean() - completions.mean()) / miss.mean())
    return nest(dict(rows=rows, truth=float(li.mean()), true_delta=true_shift, rate=float(miss.mean()),
                     base_estimates=completions.mean(axis=1), imputations=len(completions),
                     delta_scope="oracle aggregate mean-matching shift, not an identified conditional departure"))


def optin_sample(W, g, n=3000):
    """A self-selected online poll: the young, men, two regions and the well-off join far more often."""
    ad = np.flatnonzero(W.adult)
    a = W.age[ad].astype(float)
    li = np.log(W.income[ad])
    z = -0.045 * (a - 45) + 0.6 * W.male[ad] + 0.7 * np.isin(W.region[ad], [0, 7]) + 0.5 * (li - li.mean()) / li.std()
    p = np.exp(z)
    p = p / p.sum()
    idx = g.choice(ad, n, replace=False, p=p)
    return idx


def cells(W, idx):
    a = W.age[idx]
    ab = np.digitize(a, [30, 40, 50, 60, 70])
    li = np.log(W.income[idx])
    q = np.quantile(np.log(W.income[W.adult]), [0.2, 0.4, 0.6, 0.8])
    ib = np.digitize(li, q)
    return ab, W.male[idx].astype(int), W.region[idx], ib


MRP_GRID = (.1, .3, .6)


def mrp_factors(ab, sx, rg, ib):
    return [ab, sx, rg, ib, ab * 2 + sx]


def compute_mrp():
    W = World()
    vote = W.survey["vote_blue"]
    ad = np.flatnonzero(W.adult)
    truth = float(vote[ad].mean())
    g = rng(4106)
    idx = optin_sample(W, g)
    y = vote[idx].astype(float)
    ab, sx, rg, ib = cells(W, idx)
    fit = MI.mrp_fit(y, mrp_factors(ab, sx, rg, ib), grid=MRP_GRID)
    # population cells
    pab, psx, prg, pib = cells(W, ad)
    key = ((pab * 2 + psx) * 10 + prg) * 5 + pib
    uk, counts = np.unique(key, return_counts=True)
    cab = (uk // 5 // 10) // 2
    csx = (uk // 5 // 10) % 2
    crg = (uk // 5) % 10
    cib = uk % 5
    pc, draws = MI.mrp_predict(fit, mrp_factors(cab, csx, crg, cib), draws=400, rng=g)
    est = float(np.sum(pc * counts) / counts.sum())
    dist = (draws * counts[:, None]).sum(0) / counts.sum()
    # raking on age band, sex, region, income band
    from explainer.stats.kit import survey as SVY
    margins = [ab, sx, rg, ib]
    targets = [{c: float(np.mean(v == c)) for c in range(k)} for v, k in zip([pab, psx, prg, pib], [6, 2, 10, 5])]
    wr, _ = SVY.rake(margins, targets)
    raked = float(np.sum(wr * y) / np.sum(wr))
    by_region = {"truth": [float(vote[ad][prg == r].mean()) for r in range(10)],
                 "raw": [float(y[rg == r].mean()) if (rg == r).any() else None for r in range(10)],
                 "mrp": [float(np.sum((pc * counts)[crg == r]) / counts[crg == r].sum()) for r in range(10)],
                 "n": [int((rg == r).sum()) for r in range(10)]}
    comp = {"sample_young": float((ab == 0).mean()), "pop_young": float((pab == 0).mean()),
            "sample_male": float(sx.mean()), "pop_male": float(psx.mean())}
    return nest({"truth": truth, "raw": float(y.mean()), "raw_se": float(y.std() / math.sqrt(len(y))), "raked": raked, "mrp": est,
                 "mrp_ci": [float(np.quantile(dist, 0.05)), float(np.quantile(dist, 0.95))], "taus": fit["taus"], "n": len(y),
                 "by_region": by_region, "comp": comp, "hyperparameter_grid": MRP_GRID, "includes_age_sex_factor": True, "interval_scope": "normal approximation at mode, conditional on fitted group spreads"})


def compute_meas():
    nh = museum.nhanes()
    ok = np.isfinite(nh["na1"]) & np.isfinite(nh["na2"]) & np.isfinite(nh["sbp1"]) & (nh["bp_meds"] != 1)
    sbp = np.nanmean(np.column_stack([nh["sbp1"], nh["sbp2"], nh["sbp3"]]), 1)[ok]
    w1, w2 = nh["na1"][ok] / 1000, nh["na2"][ok] / 1000
    age, sex = nh["age"][ok], nh["sex"][ok]
    rel = float(np.corrcoef(w1, w2)[0, 1])
    Z = np.column_stack([age, age ** 2, (sex == 2).astype(float)])
    b1, V1 = ols(np.column_stack([np.ones(len(w1)), w1, Z]), sbp)
    wbar = (w1 + w2) / 2
    b2, V2 = ols(np.column_stack([np.ones(len(w1)), wbar, Z]), sbp)
    from explainer.stats.kit import capstone as CAP
    rc = CAP.regression_calibration(w1, w2, Z)
    b3, V3 = ols(np.column_stack([np.ones(len(w1)), rc["xhat"], Z]), sbp)
    su2 = float(np.var(w1 - w2, ddof=1) / 2)
    sx = MI.simex(w1, sbp, su2, Z=Z, B=100, rng=rng(4107))
    # a seeded truth: x the usual intake, w = x + error, y = 2 x + noise
    g = rng(4108)
    n = 20000
    x = g.normal(3.4, 0.8, n)
    v1, v2 = x + g.normal(0, 1.0, n), x + g.normal(0, 1.0, n)
    y = 110 + 2.0 * x + g.normal(0, 10, n)
    naive = float(ols(np.column_stack([np.ones(n), v1]), y)[0][1])
    rcs = CAP.regression_calibration(v1, v2)
    rcb = float(ols(np.column_stack([np.ones(n), rcs["xhat"]]), y)[0][1])
    sxs = MI.simex(v1, y, float(np.var(v1 - v2, ddof=1) / 2), B=100, rng=g)
    lam_theory = 0.8 ** 2 / (0.8 ** 2 + 1.0)
    return nest({"n": int(ok.sum()), "rel": rel, "corr_w1w2": rel, "naive": {"b": b1[1], "se": math.sqrt(V1[1, 1])},
                 "mean2": {"b": b2[1], "se": math.sqrt(V2[1, 1])}, "rc": {"b": b3[1], "lam": rc["lam"]}, "simex": sx,
                 "su2": su2, "var_w": float(np.var(w1, ddof=1)), "unrecorded_bp_medication_status": int(np.isnan(nh["bp_meds"][ok]).sum()), "analysis_scope": "unweighted complete cases not recorded as taking prescribed antihypertensives; missing medication fields include structural skips",
                 "seeded": {"naive": naive, "rc": rcb, "simex": sxs, "truth": 2.0, "lam_theory": lam_theory, "lam_rc": rcs["lam"]}})


def compute_misclass():
    """A case-control study of an exposure with true OR 2.5, exposure recalled with sensitivity 0.8, specificity 0.9
    by everyone (nondifferential), or with sensitivity 0.9 by cases and 0.7 by controls (differential recall)."""
    g = rng(4109)
    n = 1000
    p0 = 0.25
    odds1 = 2.5 * p0 / (1 - p0)
    p1 = odds1 / (1 + odds1)
    e_case = g.random(n) < p1
    e_ctl = g.random(n) < p0

    def recall(e, se, sp):
        return np.where(e, g.random(len(e)) < se, g.random(len(e)) < 1 - sp)

    tbl = lambda ec, et: (ec.sum(), n - ec.sum(), et.sum(), n - et.sum())  # noqa: E731
    true = tbl(e_case, e_ctl)
    nd = tbl(recall(e_case, 0.8, 0.9), recall(e_ctl, 0.8, 0.9))
    dif = tbl(recall(e_case, 0.9, 0.9), recall(e_ctl, 0.7, 0.9))
    orr = lambda t: t[0] * t[3] / (t[1] * t[2])  # noqa: E731
    corr = MI.misclass_correct(*nd, 0.8, 0.9)
    # the expected attenuation curve: OR observed vs sensitivity at sp 0.9
    ses = np.linspace(0.5, 1.0, 26)

    def exp_or(se, sp):
        a = se * p1 + (1 - sp) * (1 - p1)
        c = se * p0 + (1 - sp) * (1 - p0)
        return (a / (1 - a)) / (c / (1 - c))

    return nest({"true_or": orr(true), "nd_or": orr(nd), "dif_or": orr(dif), "corr_or": corr["or_corrected"], "true": true, "nd": nd,
                 "dif": dif, "ses": ses, "exp_or": [exp_or(s, 0.9) for s in ses], "exp_or_sp1": [exp_or(s, 1.0) for s in ses], "or_param": 2.5})


def compute_board():
    g = rng(4110)
    from scipy import stats as st
    z = st.norm.ppf(0.95)
    reps = 1000
    cc_mean, cc_slope, single, multi, aipw, = [], [], [], [], []
    for _ in range(reps):
        n = 300
        x = g.standard_normal(n)
        y = 1.0 + 0.6 * x + 0.8 * g.standard_normal(n)
        miss = MI.mask("mar", n, 0.4, g, driver=x, strength=2.0)["miss"]
        yo = np.where(miss, np.nan, y)
        k = ~miss
        se = yo[k].std(ddof=1) / math.sqrt(k.sum())
        cc_mean.append(abs(yo[k].mean() - 1.0) <= z * se)
        b, V = ols(np.column_stack([np.ones(k.sum()), x[k]]), y[k])
        cc_slope.append(abs(b[1] - 0.6) <= z * math.sqrt(V[1, 1]))
        ys = MI.impute_norm(yo, x, g, "mean")
        single.append(abs(ys.mean() - 1.0) <= z * ys.std(ddof=1) / math.sqrt(n))
        ests, vs = [], []
        for _ in range(10):
            yy = MI.impute_norm(yo, x, g, "proper")
            ests.append(yy.mean())
            vs.append(yy.var(ddof=1) / n)
        r = MI.rubin(ests, vs, df_complete=n - 1, level=0.90)
        multi.append(r["ci"][0] <= 1.0 <= r["ci"][1])
        rr = (~miss).astype(float)
        p = MI.response_model(rr, x)["p"]
        a = MI.aipw_mean(y, rr, p, np.polyval(np.polyfit(x[k], y[k], 1), x))
        aipw.append(abs(a["est"] - 1.0) <= z * a["se"])
    # MRP vs the raw opt-in poll: 200 polls of the World
    W = World()
    vote = W.survey["vote_blue"]
    ad = np.flatnonzero(W.adult)
    truth = float(vote[ad].mean())
    pab, psx, prg, pib = cells(W, ad)
    key = ((pab * 2 + psx) * 10 + prg) * 5 + pib
    uk, counts = np.unique(key, return_counts=True)
    cab, csx, crg, cib = (uk // 5 // 10) // 2, (uk // 5 // 10) % 2, (uk // 5) % 10, uk % 5
    raw_c, mrp_c = [], []
    for _ in range(200):
        idx = optin_sample(W, g, n=1500)
        y = vote[idx].astype(float)
        ab, sx, rg, ib = cells(W, idx)
        raw_c.append(abs(y.mean() - truth) <= z * y.std() / math.sqrt(len(y)))
        fit = MI.mrp_fit(y, mrp_factors(ab, sx, rg, ib), grid=MRP_GRID)
        pc, dr = MI.mrp_predict(fit, mrp_factors(cab, csx, crg, cib), draws=300, rng=g)
        dist = (dr * counts[:, None]).sum(0) / counts.sum()
        mrp_c.append(np.quantile(dist, 0.05) <= truth <= np.quantile(dist, 0.95))
    # Measurement error: naive slope vs calibration, including both-stage bootstrap uncertainty.
    me_n, me_rc = [], []
    for _ in range(reps):
        n = 500
        x = g.normal(0, 1, n)
        v1, v2 = x + g.normal(0, 0.8, n), x + g.normal(0, 0.8, n)
        y = 2.0 * x + g.normal(0, 1.5, n)
        b, V = ols(np.column_stack([np.ones(n), v1]), y)
        me_n.append(abs(b[1] - 2.0) <= z * math.sqrt(V[1, 1]))
        from explainer.stats.kit import capstone as CAP
        rc = CAP.regression_calibration(v1, v2)
        b2, V2 = ols(np.column_stack([np.ones(n), rc["xhat"]]), y)
        # Resample complete triples and refit both stages; 199 bootstrap draws per dataset.
        bs = []
        for _ in range(199):
            i = g.integers(0, n, n)
            rcb = CAP.regression_calibration(v1[i], v2[i])
            bs.append(ols(np.column_stack([np.ones(n), rcb["xhat"]]), y[i])[0][1])
        me_rc.append(abs(b2[1] - 2.0) <= z * np.std(bs, ddof=1))
    rows = [
        Row(41, r"complete-case mean", r"$y$ missing at random given $x$ \ (40\%), \ $n = 300$", "coverage", 0.9, float(np.mean(cc_mean)), reps),
        Row(41, r"complete-case regression slope", r"same: \ missingness depends on $x$ only", "coverage", 0.9, float(np.mean(cc_slope)), reps),
        Row(41, r"single regression imputation, \ naive SE", r"same", "coverage", 0.9, float(np.mean(single)), reps),
        Row(41, r"multiple imputation \ ($m = 10$), \ Rubin's rules", r"same", "coverage", 0.9, float(np.mean(multi)), reps),
        Row(41, r"AIPW mean, \ influence-function SE", r"same", "coverage", 0.9, float(np.mean(aipw)), reps),
        Row(41, r"opt-in poll, \ raw share", r"the World's election, \ a self-selected sample of 1,500", "coverage", 0.9, float(np.mean(raw_c)), len(raw_c)),
        Row(41, r"MRP, \ 90\% posterior interval", r"same", "coverage", 0.9, float(np.mean(mrp_c)), len(mrp_c)),
        Row(41, r"OLS slope on an error-prone $w$", r"reliability 0.61, \ $n = 500$", "coverage", 0.9, float(np.mean(me_n)), reps),
        Row(41, r"regression calibration, \ bootstrap SE", r"same, \ with a replicate", "coverage", 0.9, float(np.mean(me_rc)), reps),
    ]
    save_rows(41, rows)
    return nest({"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "mrp_hyperparameter_grid": MRP_GRID, "mrp_includes_age_sex_factor": True, "calibration_bootstrap_reps": 199})


ITEMS = {
    "wald": compute_wald, "mech": compute_mech, "sins": compute_sins, "em": compute_em, "mice": compute_mice,
    "weight": compute_weight, "heckman": compute_heckman, "tipping": compute_tipping, "mrp": compute_mrp,
    "meas": compute_meas, "misclass": compute_misclass, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
