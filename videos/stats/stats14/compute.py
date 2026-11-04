"""Precompute every number in Part 14 of *Statistics, Built* ("Counts and Categories").

    python -m videos.stats.stats14.compute            # everything missing (a few minutes)
    python -m videos.stats.stats14.compute --force board

Results are cached in ``.cache/stats14/<name>.json``.  The Challenger flights, the Berkeley admissions and Doll & Hill's
smokers are the Museum's; the screening condition, ages and towns are the World's (seed 1662); the clinic visits per
town are simulated on the World's towns.

Items:
    challenger  all 23 flights: least squares on 0/1, the logistic fit and its IRLS path, p at 31 F (Wald, profile)
    latent      the threshold picture: logit vs probit on the same flights
    rates       the World's screening condition by age band: Poisson regression with a log-population offset
    clinic      simulated clinic visits in the World's 200 towns: overdispersion, quasi-Poisson and sandwich SEs
    tables      Berkeley 1973: the pooled 2x2, the six departments, Cochran-Mantel-Haenszel; Doll & Hill 1950
    casecontrol the World's screening condition: a cohort fit vs a case-control fit (slopes agree, intercepts shift)
    scoring     a risk score from age: ROC, AUC, the Brier score, calibration; a miscalibrated rival
    board       Coverage Board rows: logistic Wald vs profile at n = 23; Poisson SEs under overdispersion
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import optimize, special, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import glm, ols
from explainer.stats.world import World

CACHE = Cache("stats14")
load = CACHE.load
W = World()
R_BOARD = 10_000
T = np.asarray(museum.CHALLENGER_TEMP, float)
K = np.asarray(museum.CHALLENGER_DISTRESS, float)
Y = (K > 0).astype(float)
XC = np.column_stack([np.ones(23), T])


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def compute_challenger():
    lp = ols.fit(XC, Y)
    f = glm.logistic(XC, Y)
    s = f.se()
    lo, eta, hi = glm.profile_ci(f, np.array([1.0, 31.0]))
    wl, wp, wh = (float(v[0]) for v in f.predict_ci(np.array([[1.0, 31.0]])))
    blo, bhat, bhi = glm.profile_coef_ci(f, 1)
    null = glm.logistic(XC[:, :1], Y)
    lr = 2 * (f.loglik - null.loglik)
    # the incidents-only chart: the seven flights with distress, count vs temperature
    inc = K > 0
    r_inc = float(np.corrcoef(T[inc], K[inc])[0, 1])
    b6 = glm.logistic(XC, K, n_trials=np.full(23, 6.0))
    p6 = float(b6.predict(np.array([1.0, 31.0])))
    path = [list(map(float, b)) for b in f.path]
    ll_path = [float(glm.Glm("binomial", np.asarray(b), XC, Y, np.ones(23), np.zeros(23)).loglik) for b in f.path]
    return nest({"T": T, "K": K, "Y": Y, "lp_coef": lp.coef, "lp_31": lp.coef[0] + 31 * lp.coef[1], "lp_85": lp.coef[0] + 85 * lp.coef[1],
                 "coef": f.coef, "se": s, "deviance": f.deviance, "null_dev": null.deviance, "lr": lr, "lr_p": stats.chi2.sf(lr, 1),
                 "p31": float(f.predict(np.array([1.0, 31.0]))), "p31_wald": [wl, wh], "p31_profile": [float(special.expit(lo)), float(special.expit(hi))],
                 "eta31": [lo, eta, hi], "p53": float(f.predict(np.array([1.0, 53.0]))), "p70": float(f.predict(np.array([1.0, 70.0]))),
                 "or10": float(np.exp(-10 * f.coef[1])), "or10_ci": np.exp(-10 * np.array([bhi, blo])), "slope_profile": [blo, bhi],
                 "slope_wald": f.wald_ci()[1], "r_incidents": r_inc, "b6_coef": b6.coef, "p6_31": p6, "p6_any": 1 - (1 - p6) ** 6,
                 "path": path, "ll_path": ll_path, "t50": float(-f.coef[0] / f.coef[1])})


def compute_latent():
    f = glm.logistic(XC, Y)
    # probit by Newton on the likelihood
    def negll(b):
        p = np.clip(stats.norm.cdf(XC @ b), 1e-12, 1 - 1e-12)
        return -np.sum(Y * np.log(p) + (1 - Y) * np.log(1 - p))
    pr = optimize.minimize(negll, f.coef / 1.7, method="BFGS").x
    xs = np.linspace(25, 85, 241)
    return nest({"logit": f.coef, "probit": pr, "ratio": f.coef / pr, "xs": xs, "p_logit": special.expit(f.coef[0] + f.coef[1] * xs),
                 "p_probit": stats.norm.cdf(pr[0] + pr[1] * xs), "probit_31": float(stats.norm.cdf(pr[0] + 31 * pr[1]))})


def compute_rates():
    s = W.screening
    age, adult, male = W.age.astype(int), W.adult, W.male
    edges = np.arange(18, 100, 6)
    rows = []
    for sex in (False, True):
        for lo in edges:
            m = adult & (age >= lo) & (age < lo + 6) & (male == sex)
            if m.sum() == 0:
                continue
            rows.append((lo + 2.5, float(sex), int(s["sick"][m].sum()), int(m.sum())))
    a = np.array(rows, float)
    X = np.column_stack([np.ones(len(a)), (a[:, 0] - 50) / 10, a[:, 1]])
    f = glm.poisson(X, a[:, 2], offset=np.log(a[:, 3]))
    return nest({"mid": a[:, 0], "male": a[:, 1], "cases": a[:, 2], "pop": a[:, 3], "coef": f.coef, "se": f.se(),
                 "rr10": float(np.exp(f.coef[1])), "rr10_ci": np.exp(f.wald_ci()[1]), "rr_male": float(np.exp(f.coef[2])),
                 "rr_male_ci": np.exp(f.wald_ci()[2]), "deviance": f.deviance, "df": len(a) - 3, "dispersion": f.pearson_dispersion,
                 "rate50": float(np.exp(f.coef[0]) * 1000)})


def clinic_sample(g, frailty_shape=None):
    """Monthly clinic visits in the World's 200 towns: rate per adult rises to the east; optional gamma frailty."""
    adults = np.bincount(W.town[W.adult], minlength=200).astype(float)
    east = W.towns["xy"][:, 0] / 5.0
    lam = adults * np.exp(np.log(0.02) + 0.25 * east)
    if frailty_shape is not None:
        lam = lam * g.gamma(frailty_shape, 1 / frailty_shape, 200)
    return g.poisson(lam), adults, east


def compute_clinic():
    g = rng(1898)
    y, adults, east = clinic_sample(g, frailty_shape=4.0)
    X = np.column_stack([np.ones(200), east])
    f = glm.poisson(X, y, offset=np.log(adults))
    return nest({"y": y, "adults": adults, "east": east, "coef": f.coef, "se": f.se(), "se_quasi": f.se("quasi"),
                 "se_sandwich": f.se("sandwich"), "dispersion": f.pearson_dispersion, "deviance": f.deviance, "df": 198,
                 "rate": y / adults * 1000, "fitted_rate": f.mu / adults * 1000})


def compute_tables():
    B = museum.BERKELEY
    ma = sum(v[0] for v in B.values())
    mr = sum(v[1] for v in B.values())
    fa = sum(v[2] for v in B.values())
    fr = sum(v[3] for v in B.values())
    pooled = glm.table2x2(ma, mr, fa, fr)
    depts = {k: {"men": v[0] / (v[0] + v[1]), "women": v[2] / (v[2] + v[3]), "n_men": v[0] + v[1], "n_women": v[2] + v[3],
                 "or": (v[0] * v[3]) / (v[1] * v[2])} for k, v in B.items()}
    c = glm.cmh([[[v[0], v[1]], [v[2], v[3]]] for v in B.values()])
    # logistic with department dummies: the women's coefficient
    rows = []
    for j, (k, v) in enumerate(B.items()):
        rows += [(j, 0, v[0], v[0] + v[1]), (j, 1, v[2], v[2] + v[3])]
    r = np.array(rows, float)
    Xd = np.column_stack([np.ones(len(r)), r[:, 1]] + [(r[:, 0] == j).astype(float) for j in range(1, 6)])
    fl = glm.logistic(Xd, r[:, 2], n_trials=r[:, 3])
    Xp = np.column_stack([np.ones(len(r)), r[:, 1]])
    fp = glm.logistic(Xp, r[:, 2], n_trials=r[:, 3])
    from statsmodels.stats.contingency_tables import StratifiedTable
    bd = StratifiedTable([np.array([[v[0], v[1]], [v[2], v[3]]], float) for v in B.values()]).test_equal_odds()
    bd5 = StratifiedTable([np.array([[v[0], v[1]], [v[2], v[3]]], float) for k, v in B.items() if k != "A"]).test_equal_odds()
    dept_admit = np.array([[v[0] + v[2], v[1] + v[3]] for v in B.values()])
    sex_dept = np.array([[v[0] + v[1] for v in B.values()], [v[2] + v[3] for v in B.values()]])
    c_da = stats.chi2_contingency(dept_admit, correction=False)
    c_sd = stats.chi2_contingency(sex_dept, correction=False)
    dh = museum.DOLL_HILL
    d = glm.table2x2(dh["cases_smokers"], dh["cases"] - dh["cases_smokers"], dh["controls_smokers"], dh["controls"] - dh["controls_smokers"])
    return nest({"pooled": pooled, "men_rate": ma / (ma + mr), "women_rate": fa / (fa + fr), "n_men": ma + mr, "n_women": fa + fr,
                 "depts": depts, "cmh": c, "logit_women_adj": fl.coef[1], "logit_women_adj_se": fl.se()[1],
                 "logit_women_pooled": fp.coef[1], "doll_hill": d, "bd": float(bd.statistic), "bd_p": float(bd.pvalue),
                 "bd5": float(bd5.statistic), "bd5_p": float(bd5.pvalue), "chi_dept_admit": float(c_da.statistic),
                 "chi_sex_dept": float(c_sd.statistic), "df_rxc": int(c_da.dof)})


def compute_casecontrol():
    s = W.screening
    adults = np.flatnonzero(W.adult)
    age = W.age.astype(float)
    sick = s["sick"]
    g = rng(1950)
    cohort = g.choice(adults, 40_000, replace=False)
    Xc = np.column_stack([np.ones(len(cohort)), (age[cohort] - 50) / 10])
    fc = glm.logistic(Xc, sick[cohort].astype(float))
    cases = np.flatnonzero(sick)
    ctrl_pool = np.setdiff1d(adults, cases)
    cs = g.choice(cases, 400, replace=False)
    ct = g.choice(ctrl_pool, 400, replace=False)
    idx = np.r_[cs, ct]
    Xcc = np.column_stack([np.ones(len(idx)), (age[idx] - 50) / 10])
    ycc = np.r_[np.ones(400), np.zeros(400)]
    fcc = glm.logistic(Xcc, ycc)
    # the whole population, for the truth
    Xa = np.column_stack([np.ones(len(adults)), (age[adults] - 50) / 10])
    fa = glm.logistic(Xa, sick[adults].astype(float))
    shift = float(np.log((400 / len(cases)) / (400 / len(ctrl_pool))))
    return nest({"cohort_coef": fc.coef, "cohort_se": fc.se(), "cc_coef": fcc.coef, "cc_se": fcc.se(), "pop_coef": fa.coef,
                 "shift": shift, "n_cases": len(cases), "n_controls_pool": len(ctrl_pool), "cohort_cases": int(sick[cohort].sum()),
                 "cc_age_cases": age[cs], "cc_age_ctrl": age[ct], "prevalence": float(sick[adults].mean())})


def compute_scoring():
    s = W.screening
    adults = np.flatnonzero(W.adult)
    age = W.age.astype(float)
    g = rng(1997)
    tr = g.choice(adults, 50_000, replace=False)
    te = g.choice(np.setdiff1d(adults, tr), 50_000, replace=False)
    yt, ye = s["sick"][tr].astype(float), s["sick"][te].astype(float)
    Xtr = np.column_stack([np.ones(len(tr)), (age[tr] - 50) / 10])
    Xte = np.column_stack([np.ones(len(te)), (age[te] - 50) / 10])
    f = glm.logistic(Xtr, yt)
    p = f.predict(Xte)
    fpr, tpr, auc = glm.roc(p, ye)
    # a rival that ranks identically but overstates every risk fourfold in odds
    p_bad = special.expit(special.logit(p) + np.log(4))
    pred, obs, cnt = glm.calibration(p, ye, bins=10)
    pred_b, obs_b, _ = glm.calibration(p_bad, ye, bins=10)
    # a test that uses both screening results too
    both = (s["test_a"][te].astype(float) + s["test_b"][te].astype(float))
    p2_train = glm.logistic(np.column_stack([Xtr, s["test_a"][tr] + s["test_b"][tr]]), yt)
    p2 = p2_train.predict(np.column_stack([Xte, both]))
    f2, t2, auc2 = glm.roc(p2, ye)
    keep = np.linspace(0, len(fpr) - 1, 200).astype(int)
    keep2 = np.linspace(0, len(f2) - 1, 200).astype(int)
    return nest({"auc": auc, "brier": glm.brier(p, ye), "brier_bad": glm.brier(p_bad, ye), "brier_base": glm.brier(np.full_like(ye, ye.mean()), ye),
                 "fpr": fpr[keep], "tpr": tpr[keep], "auc_both": auc2, "fpr2": f2[keep2], "tpr2": t2[keep2], "brier_both": glm.brier(p2, ye),
                 "cal_pred": pred, "cal_obs": obs, "cal_n": cnt, "cal_pred_bad": pred_b, "cal_obs_bad": obs_b, "prevalence": float(ye.mean()),
                 "coef": f.coef})


# ---------------------------------------------------------------------------------------------------------------
# The Board
# ---------------------------------------------------------------------------------------------------------------
def _intercept_only(y, offset, start=0.0):
    """MLE of a with logit p = a + offset (1-D Newton); returns (a, loglik)."""
    ybar = np.clip(np.mean(y), 0.02, 0.98)
    a = float(np.log(ybar / (1 - ybar)) - np.mean(offset))  # a start on the right scale
    for _ in range(100):
        p = special.expit(a + offset)
        grad = np.sum(y - p)
        h = np.sum(p * (1 - p))
        step = float(np.clip(grad / max(h, 1e-12), -2.0, 2.0))
        a += step
        if abs(step) < 1e-10:
            break
    p = np.clip(special.expit(a + offset), 1e-15, 1 - 1e-15)
    return a, float(np.sum(y * np.log(p) + (1 - y) * np.log1p(-p)))


def _ll_eta31_fixed(y, e):
    """max over b of the log-likelihood with logit p = e + b (T - 31)."""
    b = -0.2
    for _ in range(200):
        p = special.expit(e + b * (T - 31))
        grad = np.sum((y - p) * (T - 31))
        h = np.sum(p * (1 - p) * (T - 31) ** 2)
        step = float(np.clip(grad / max(h, 1e-12), -0.1, 0.1))
        b += step
        if abs(step) < 1e-10:
            break
    p = np.clip(special.expit(e + b * (T - 31)), 1e-15, 1 - 1e-15)
    return float(np.sum(y * np.log(p) + (1 - y) * np.log1p(-p)))


def compute_board():
    """Logistic rows: a profile-likelihood interval covers the truth exactly when the likelihood-ratio statistic at the
    truth is below chi2_1(0.95), which works for every sample, separated or not (the supremum of the log-likelihood is
    0 under separation, and the profile interval is then one-sided).  A Wald interval needs a finite estimate: under
    separation there is none, and the sample counts as a miss."""
    g = rng(14_000)
    f0 = glm.logistic(XC, Y)
    a0, b0 = f0.coef
    eta31 = a0 + 31 * b0
    crit = stats.chi2.ppf(0.95, 1)
    hits = {"b_w": 0, "b_p": 0, "e_w": 0, "e_p": 0}
    sep = 0
    for _ in range(R_BOARD):
        y = (g.random(23) < special.expit(a0 + b0 * T)).astype(float)
        separated = (y.sum() in (0, 23) or np.max(T[y == 1]) < np.min(T[y == 0]) or np.min(T[y == 1]) > np.max(T[y == 0]))
        f = None
        if not separated:
            f = glm.logistic(XC, y)
            se = f.se()
            if not np.all(np.isfinite(se)) or se[1] > 5 or not np.all(np.isfinite(f.coef)):
                separated, f = True, None
        ll_sup = 0.0 if separated else f.loglik
        sep += separated
        # profile: the LR test at the truth
        hits["b_p"] += 2 * (ll_sup - _intercept_only(y, b0 * T)[1]) <= crit
        hits["e_p"] += 2 * (ll_sup - _ll_eta31_fixed(y, eta31)) <= crit
        if f is not None:
            z = 1.959964
            hits["b_w"] += abs(f.coef[1] - b0) <= z * se[1]
            x31 = np.array([1.0, 31.0])
            hits["e_w"] += abs(float(x31 @ f.coef) - eta31) <= z * float(np.sqrt(x31 @ f.cov() @ x31))
    res = {k: v / R_BOARD for k, v in hits.items()}
    # Poisson rate ratios on the World's towns
    pc = {"pois": 0, "nb_c": 0, "nb_q": 0, "nb_s": 0}
    for _ in range(R_BOARD):
        for kind in ("pois", "nb"):
            y, adults, east = clinic_sample(g, None if kind == "pois" else 4.0)
            X = np.column_stack([np.ones(200), east])
            f = glm.poisson(X, y, offset=np.log(adults))
            if kind == "pois":
                pc["pois"] += abs(f.coef[1] - 0.25) <= 1.959964 * f.se()[1]
            else:
                pc["nb_c"] += abs(f.coef[1] - 0.25) <= 1.959964 * f.se()[1]
                pc["nb_q"] += abs(f.coef[1] - 0.25) <= 1.959964 * f.se("quasi")[1]
                pc["nb_s"] += abs(f.coef[1] - 0.25) <= 1.959964 * f.se("sandwich")[1]
    pc = {k: v / R_BOARD for k, v in pc.items()}
    chal = r"Challenger temperatures, \ $n = 23$"
    over = r"200 towns, \ gamma frailty"
    rows = [
        Row(14, r"logistic slope, \ Wald", chal, "coverage", 0.95, res["b_w"], R_BOARD, extra=f"{sep} separated samples: no estimate"),
        Row(14, r"logistic slope, \ profile likelihood", chal, "coverage", 0.95, res["b_p"], R_BOARD),
        Row(14, r"$p$ at 31$^\circ$F, \ Wald (logit scale)", chal, "coverage", 0.95, res["e_w"], R_BOARD),
        Row(14, r"$p$ at 31$^\circ$F, \ profile likelihood", chal, "coverage", 0.95, res["e_p"], R_BOARD),
        Row(14, r"Poisson rate ratio, \ classical SE", r"200 towns, \ Poisson counts", "coverage", 0.95, pc["pois"], R_BOARD),
        Row(14, r"Poisson rate ratio, \ classical SE", over, "coverage", 0.95, pc["nb_c"], R_BOARD),
        Row(14, r"Poisson rate ratio, \ quasi-Poisson SE", over, "coverage", 0.95, pc["nb_q"], R_BOARD),
        Row(14, r"Poisson rate ratio, \ sandwich SE", over, "coverage", 0.95, pc["nb_s"], R_BOARD),
    ]
    save_rows(14, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "separated": sep}


ITEMS = {
    "challenger": compute_challenger, "latent": compute_latent, "rates": compute_rates, "clinic": compute_clinic,
    "tables": compute_tables, "casecontrol": compute_casecontrol, "scoring": compute_scoring, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
