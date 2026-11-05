"""Precompute every number in Part 25 of *Statistics, Built* ("Borrowing Strength: Shrinkage and Mixed Models").

    python -m videos.stats.stats25.compute            # everything missing (several minutes)
    python -m videos.stats.stats25.compute --force board

Results are cached in ``.cache/stats25/<name>.json``.  Efron and Morris's hitters are the Museum's; schools, towns and
incomes are the World's; the rest are seeded simulations.

Items:
    baseball    Efron & Morris: the MLE vs James-Stein vs the rest of the season
    risk        James-Stein's risk against |theta| for p = 10, with SURE
    winners     the winner's curse in 1,000 z-scores; Tweedie's correction with an NPMLE prior
    components  variance components and the ICC for the World's schools; the design effect
    blup        a random-intercept model for 40 schools: BLUPs against school means and the truth
    remlml      ML vs REML for the school variance with few schools
    boundary    the LR test of a zero variance: 50:50 chi-squared mixture
    growth      a longitudinal growth-curve example: random intercepts and slopes
    nested      pupils in schools in towns: a town variance at the boundary
    crossed     essays crossed with raters: each essay read by 2 of 8 raters; raw means vs a crossed model
    mundlak     random vs fixed effects when SES has a contextual effect: Hausman and Mundlak
    glmm        a random-intercept logistic model for passing: Laplace, AGQ, and marginal vs conditional
    league      the World's hospital league table: 60 hospitals' death rates, raw and shrunk by a GLMM
    smallarea   Fay-Herriot for town mean incomes: direct, synthetic and EBLUP against the truth
    meta        five studies: DerSimonian-Laird vs Hartung-Knapp
    rasch       a Rasch model as a GLMM
    board       Coverage Board rows
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import special, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import mixed as MX
from explainer.stats.kit import shrink as SH
from explainer.stats.kit import ols as O
from explainer.stats.world import World

CACHE = Cache("stats25")
load = CACHE.load
W = World()


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


def compute_baseball():
    names, h, ab, p = museum.efron_morris()
    y = h / 45
    x = np.sqrt(45) * np.arcsin(2 * y - 1)  # Efron & Morris's variance-stabilizing transform: unit variance
    js = SH.james_stein(x, 1.0)
    est = (np.sin(js["theta"] / np.sqrt(45)) + 1) / 2
    closer = int(np.sum(np.abs(est - p) < np.abs(y - p)))
    return nest({"names": names, "y": y, "p": p, "ab": ab, "js": est, "B": js["B"], "grand": float(y.mean()),
                 "sse_mle": float(np.sum((y - p) ** 2)), "sse_js": float(np.sum((est - p) ** 2)), "closer": closer,
                 "ratio": float(np.sum((y - p) ** 2) / np.sum((est - p) ** 2))})


def compute_risk():
    p = 10
    norms = np.linspace(0, 8, 33)
    g = rng(1961)
    out = {"norms": norms, "mle": [], "js": [], "js_plus": [], "sure": []}
    for r in norms:
        th = np.zeros(p)
        th[0] = r
        rr = SH.js_risk_exact(th, 1.0, R=8000, rng=g)
        out["mle"].append(rr["mle"])
        out["js"].append(rr["js"])
        out["js_plus"].append(rr["js_plus"])
        out["sure"].append(float(p - (p - 2) ** 2 / (p - 2 + r ** 2)))  # the bound E|X|^2 >= p + |theta|^2, Jensen
    out["p"] = p
    return nest(out)


def compute_winners():
    g = rng(2011)
    N = 1000
    theta = np.where(g.random(N) < 0.9, 0.0, g.normal(0, 3, N))
    z = theta + g.normal(size=N)
    top = np.argsort(-z)[:10]
    fit = SH.npmle(z, 1.0, grid=np.linspace(-10, 12, 441))
    return nest({"z": z, "theta": theta, "top": top, "z_top": z[top], "theta_top": theta[top], "tweedie_top": fit["post_mean"][top],
                 "mean_z_top": float(z[top].mean()), "mean_theta_top": float(theta[top].mean()),
                 "mean_tw_top": float(fit["post_mean"][top].mean()), "grid": fit["grid"], "w": fit["w"],
                 "null_share": float(fit["w"][np.abs(fit["grid"]) < 0.3].sum())})


def schools_df(pick=None):
    s = W.schools
    m = np.ones(len(s["school"]), bool) if pick is None else np.isin(s["school"], pick)
    sch = s["school"][m]
    return {"y": s["score"][m], "ses": s["ses"][m], "prog": s["programme"][sch].astype(float), "school": sch,
            "ses_school": s["ses_school"][sch], "u": s["u"][sch], "town": s["town"][sch]}


def compute_components():
    d = schools_df()
    f = MX.lmm(d["y"], np.ones((len(d["y"]), 1)), d["school"])
    icc_true = (100 * W.SCHOOL_SD) ** 2
    m_bar = len(d["y"]) / W.N_SCHOOLS
    sch, idx = np.unique(d["school"], return_inverse=True)
    means = np.bincount(idx, d["y"]) / np.bincount(idx)
    eg = np.flatnonzero(idx == 0)
    return nest({"means": means, "sizes": np.bincount(idx), "example": d["y"][idx < 6][:400], "example_school": idx[idx < 6][:400],
                 "G": f.G[0, 0], "sigma2": f.sigma2, "icc": f.icc, "n": len(d["y"]), "m_bar": m_bar,
                 "deff": 1 + (m_bar - 1) * f.icc, "neff": len(d["y"]) / (1 + (m_bar - 1) * f.icc),
                 "u_var_true": icc_true, "e_var_true": (100 * W.PUPIL_SD) ** 2})


def compute_blup():
    g = rng(2525)
    pick = np.sort(g.choice(W.N_SCHOOLS, 40, replace=False))
    d = schools_df(pick)
    X = np.column_stack([np.ones(len(d["y"])), d["prog"], d["ses"]])
    f = MX.lmm(d["y"], X, d["school"])
    ols = O.fit(X, d["y"])
    sch, idx = np.unique(d["school"], return_inverse=True)
    n_g = np.bincount(idx)
    resid_mean = np.bincount(idx, d["y"] - X @ f.beta) / n_g
    true_u = np.array([W.schools["u"][k] * 100 + 100 * W.SES_CONTEXT * W.schools["ses_school"][k] for k in sch])
    shrink = f.G[0, 0] / (f.G[0, 0] + f.sigma2 / n_g)
    return nest({"beta": f.beta, "se": f.se, "G": f.G[0, 0], "sigma2": f.sigma2, "ols": ols.coef, "ols_se": ols.se(),
                 "n_g": n_g, "raw": resid_mean, "blup": f.blup[:, 0], "truth": true_u - true_u.mean(), "shrink": shrink,
                 "mse_raw": float(np.mean((resid_mean - (true_u - true_u.mean())) ** 2)),
                 "mse_blup": float(np.mean((f.blup[:, 0] - (true_u - true_u.mean())) ** 2)), "loglik": f.loglik})


def compute_remlml():
    g = rng(1971)
    R = 300
    out = {}
    for G_ in (5, 10, 40):
        ml, rl = [], []
        for _ in range(R):
            m = 10
            groups = np.repeat(np.arange(G_), m)
            y = 0.5 * np.repeat(g.normal(size=G_), m) + g.normal(size=G_ * m) + np.repeat(g.normal(size=G_) > 0, m) * 0.3
            X = np.column_stack([np.ones(G_ * m), np.repeat(np.arange(G_) % 2, m)])
            ml.append(MX.lmm(y, X, groups, method="ML").G[0, 0])
            rl.append(MX.lmm(y, X, groups, method="REML").G[0, 0])
        out[str(G_)] = {"ml": float(np.mean(ml)), "reml": float(np.mean(rl)), "ml_zero": float(np.mean(np.asarray(ml) < 1e-6)),
                        "reml_zero": float(np.mean(np.asarray(rl) < 1e-6))}
    return nest({"by_G": out, "truth": 0.25 + 0.3 ** 2 / 4})


def compute_boundary():
    g = rng(1987)
    R = 1000
    lr = []
    for _ in range(R):
        G_, m = 20, 10
        groups = np.repeat(np.arange(G_), m)
        y = g.normal(size=G_ * m)
        X = np.ones((G_ * m, 1))
        f1 = MX.lmm(y, X, groups, method="ML")
        ll0 = float(np.sum(stats.norm.logpdf(y, y.mean(), y.std())))
        lr.append(max(2 * (f1.loglik - ll0), 0.0))
    lr = np.asarray(lr)
    return nest({"lr": lr, "zero_share": float(np.mean(lr < 1e-6)), "reject_chi1": float(np.mean(lr > 3.84)),
                 "reject_mix": float(np.mean(lr > 2.71)), "crit_mix": 2.71})


def compute_growth():
    """60 children measured at ages 4, 6, 8, 10, 12: the World's growth law plus child-specific intercepts and slopes."""
    g = rng(1982)
    n_ch, ages = 60, np.array([4.0, 6, 8, 10, 12])
    a0 = 106 + 5.5 * g.standard_normal(n_ch)
    b0 = 5.8 + 0.6 * g.standard_normal(n_ch)
    groups = np.repeat(np.arange(n_ch), len(ages))
    age = np.tile(ages, n_ch)
    y = a0[groups] + b0[groups] * (age - 8) + 1.2 * g.standard_normal(len(age))
    X = np.column_stack([np.ones(len(age)), age - 8])
    ri = MX.lmm(y, X, groups)
    rs = MX.lmm(y, X, groups, slopes=[1])
    lr = 2 * (rs.loglik - ri.loglik)
    return nest({"age": age, "y": y, "groups": groups, "ri": {"beta": ri.beta, "se": ri.se, "G": ri.G, "s2": ri.sigma2, "ll": ri.loglik},
                 "rs": {"beta": rs.beta, "se": rs.se, "G": rs.G, "s2": rs.sigma2, "ll": rs.loglik, "blup": rs.blup},
                 "lr": float(lr), "truth": {"int_sd": 5.5, "slope_sd": 0.6, "slope": 5.8, "e_sd": 1.2}, "ages": ages})


def compute_nested():
    d = schools_df()
    s = W.schools
    town_of_school = s["town"]
    X = np.ones((len(d["y"]), 1))
    f_s = MX.lmm(d["y"], X, d["school"])
    # town effect: fit to school means with known sampling variance (a quick two-level-from-means estimate)
    sch, idx = np.unique(d["school"], return_inverse=True)
    means = np.bincount(idx, d["y"]) / np.bincount(idx)
    tf = MX.lmm(means, np.ones((len(means), 1)), town_of_school[sch])
    n_towns = len(np.unique(town_of_school))
    return nest({"school_var": f_s.G[0, 0], "pupil_var": f_s.sigma2, "town_var": tf.G[0, 0], "school_resid_var": tf.sigma2,
                 "n_towns": n_towns, "n_schools": len(sch)})


def compute_crossed():
    g = rng(1955)
    E, R, k = 60, 8, 2
    quality = g.normal(0, 1.0, E)
    severity = g.normal(0, 0.6, R)
    essay = np.repeat(np.arange(E), k)
    rater = np.concatenate([g.choice(R, k, replace=False) for _ in range(E)])
    y = 5 + quality[essay] - severity[rater] + g.normal(0, 0.5, E * k)
    f = MX.vc_lmm(y, np.ones((E * k, 1)), {"essay": essay, "rater": rater})
    raw = np.bincount(essay, y) / k - 5
    fit_e = f["beta"][0] - 5 + f["blup"]["essay"]
    fe_only = MX.vc_lmm(y, np.ones((E * k, 1)), {"essay": essay})
    fit_e1 = fe_only["beta"][0] - 5 + fe_only["blup"]["essay"]
    mse = lambda a: float(np.mean((a - quality) ** 2))  # noqa: E731
    rc = lambda a: float(stats.spearmanr(a, quality)[0])  # noqa: E731
    return nest({"quality": quality, "severity": severity, "essay": essay, "rater": rater, "y": y, "raw": raw,
                 "crossed": fit_e, "essay_only": fit_e1, "sev_hat": -f["blup"]["rater"], "var": f["var"], "sigma2": f["sigma2"],
                 "var_essay_only": fe_only["var"], "sigma2_essay_only": fe_only["sigma2"],
                 "mse": {"raw": mse(raw), "essay_only": mse(fit_e1), "crossed": mse(fit_e)},
                 "rank": {"raw": rc(raw), "essay_only": rc(fit_e1), "crossed": rc(fit_e)}})


def compute_league():
    """The World's 60 hospitals: operations per year from 15 to about 900; true death rates vary modestly."""
    hb = W.hospitals
    H, n, p_true, d = W.N_HOSPITALS, hb["operations"], hb["p"], hb["deaths"]
    hosp = np.repeat(np.arange(H), n)
    y = np.concatenate([np.r_[np.ones(d[h]), np.zeros(n[h] - d[h])] for h in range(H)])
    f = MX.glmm_logit(y, np.ones((len(y), 1)), hosp, nagq=10)
    shrunk = special.expit(f["beta"][0] + np.asarray(f["modes"]))
    raw = d / n
    pbar = d.sum() / n.sum()
    worst10 = set(np.argsort(-p_true)[:10])
    top_raw = np.argsort(-raw)[:5]
    top_sh = np.argsort(-shrunk)[:5]
    out_99 = np.abs(raw - pbar) > 3.09 * np.sqrt(pbar * (1 - pbar) / n)
    return nest({"n": n, "d": d, "raw": raw, "shrunk": shrunk, "truth": p_true, "pbar": pbar, "sigma": f["sigma"],
                 "beta0": f["beta"][0], "top_raw": top_raw, "top_shrunk": top_sh,
                 "raw_hits": int(sum(h in worst10 for h in top_raw)), "shrunk_hits": int(sum(h in worst10 for h in top_sh)),
                 "raw_top_n": n[top_raw], "shrunk_top_n": n[top_sh], "n_out_99": int(out_99.sum()),
                 "mse_raw": float(np.mean((raw - p_true) ** 2)), "mse_shrunk": float(np.mean((shrunk - p_true) ** 2)),
                 "rank_raw": float(stats.spearmanr(raw, p_true)[0]), "rank_shrunk": float(stats.spearmanr(shrunk, p_true)[0])})


def compute_mundlak():
    d = schools_df()  # all 400 schools: a contextual effect needs many schools to be seen
    sch, idx = np.unique(d["school"], return_inverse=True)
    ses_bar = (np.bincount(idx, d["ses"]) / np.bincount(idx))[idx]
    X = np.column_stack([np.ones(len(d["y"])), d["ses"]])
    re = MX.lmm(d["y"], X, d["school"])
    # fixed effects: within transformation
    yw = d["y"] - (np.bincount(idx, d["y"]) / np.bincount(idx))[idx]
    xw = d["ses"] - ses_bar
    fe = O.fit(xw[:, None], yw)
    fe_se = float(np.sqrt(fe.rss / (len(yw) - len(sch) - 1) / np.sum(xw ** 2)))
    mk = MX.lmm(d["y"], np.column_stack([X, ses_bar]), d["school"])
    H = float((fe.coef[0] - re.beta[1]) ** 2 / max(fe_se ** 2 - re.se[1] ** 2, 1e-12))
    mx = np.bincount(idx, d["ses"]) / np.bincount(idx)
    my = np.bincount(idx, d["y"]) / np.bincount(idx)
    between = np.polyfit(mx, my, 1)
    g = rng(78)
    show = np.sort(g.choice(len(sch), 6, replace=False))
    pupils = [{"ses": d["ses"][idx == k], "y": d["y"][idx == k]} for k in show]
    return nest({"school_ses": mx, "school_y": my, "between": between, "show": show, "pupils": pupils,
                 "re": re.beta[1], "re_se": re.se[1], "fe": float(fe.coef[0]), "fe_se": fe_se, "mundlak_within": mk.beta[1],
                 "mundlak_context": mk.beta[2], "mundlak_se": mk.se, "hausman": H, "p_hausman": float(stats.chi2.sf(H, 1)),
                 "truth_within": 100 * W.SES_SLOPE, "truth_context": 100 * W.SES_CONTEXT})


def compute_glmm():
    g = rng(2405)  # the same 40 schools as Part 24's GEE chapter
    s = W.schools
    pick = np.sort(g.choice(W.N_SCHOOLS, 40, replace=False))
    m = np.isin(s["school"], pick)
    sch = s["school"][m]
    X = np.column_stack([np.ones(m.sum()), s["programme"][sch].astype(float), s["ses"][m]])
    y = (s["score"][m] > 550).astype(float)
    lap = MX.glmm_logit(y, X, sch, nagq=1)
    agq = MX.glmm_logit(y, X, sch, nagq=10)
    from explainer.stats.kit import glm as Gm
    marg = Gm.gee_logistic(X, y, sch, "exchangeable")
    ratio = float(agq["beta"][1] / marg["coef"][1])
    approx = float(np.sqrt(1 + 0.346 * agq["sigma"] ** 2))
    return nest({"laplace": lap, "agq": agq, "gee": marg["coef"], "ratio": ratio, "approx": approx})


def compute_smallarea():
    """Mean adult income in each of the World's 200 towns, from a survey of 2,000 adults: most towns get a handful."""
    ad = np.flatnonzero(W.adult)
    town = W.town[ad]
    inc = W.income[ad] / 1000
    truth = np.array([inc[town == t].mean() for t in range(200)])
    size = np.bincount(town, minlength=200)
    g = rng(1979)
    samp = g.choice(len(ad), 2000, replace=False)
    st, si = town[samp], inc[samp]
    n_t = np.bincount(st, minlength=200)
    ok = n_t >= 2
    direct = np.array([si[st == t].mean() if n_t[t] > 0 else np.nan for t in range(200)])
    var_within = np.array([si[st == t].var(ddof=1) if n_t[t] > 1 else np.nan for t in range(200)])
    pooled_var = float(np.nanmean(var_within))
    D = pooled_var / np.maximum(n_t, 1)
    region = W.towns["region"]
    Xr = np.column_stack([np.ones(200)] + [(region == r).astype(float) for r in range(1, 10)])
    fh = SH.fay_herriot(direct[ok], D[ok], Xr[ok])
    eblup = np.full(200, np.nan)
    eblup[ok] = fh["eblup"]
    synth = Xr @ fh["beta"]
    mse = lambda est: float(np.nanmean((est[ok] - truth[ok]) ** 2))  # noqa: E731
    return nest({"truth": truth, "direct": direct, "eblup": eblup, "synthetic": synth, "n_t": n_t, "ok": ok, "A": fh["A"],
                 "gamma": fh["gamma"], "mse_direct": mse(direct), "mse_eblup": mse(eblup), "mse_synth": mse(synth),
                 "towns_used": int(ok.sum()), "size": size})


def meta_sample(k, g, tau=0.15, mu=0.3):
    n = g.integers(40, 400, k)
    v = 4 / n
    th = mu + tau * g.normal(size=k)
    return th + np.sqrt(v) * g.normal(size=k), v


def compute_meta():
    g = rng(1986)
    y, v = meta_sample(5, g)
    m = SH.meta(y, v)
    return nest({"y": y, "v": v, "res": m, "truth": 0.3, "tau": 0.15})


def compute_rasch():
    g = rng(1960)
    P, I = 200, 15
    ability = g.normal(0, 1.0, P)
    diff = np.linspace(-1.8, 1.8, I)
    person = np.repeat(np.arange(P), I)
    item = np.tile(np.arange(I), P)
    y = (g.random(P * I) < special.expit(ability[person] - diff[item])).astype(float)
    X = np.column_stack([np.eye(I)[item]])  # one column per item: -difficulty
    fit = MX.glmm_logit(y, X, person, nagq=1)
    return nest({"diff_true": diff, "diff_hat": -np.asarray(fit["beta"]), "se": fit["se"], "sigma": fit["sigma"],
                 "ability_true": ability, "ability_hat": fit["modes"], "P": P, "I": I,
                 "raw_score": np.bincount(person, y)})


def compute_board():
    g = rng(2526)
    R = 1000
    # (1, 2) meta-analysis of 5 studies: DL z interval vs Hartung-Knapp t interval
    dl = hk = 0
    for _ in range(R):
        y, v = meta_sample(5, g)
        m = SH.meta(y, v)
        dl += m["ci_dl"][0] <= 0.3 <= m["ci_dl"][1]
        hk += m["ci_hk"][0] <= 0.3 <= m["ci_hk"][1]
    # (3, 4) a between-school treatment effect with 8 schools: normal vs Satterthwaite t
    R2 = 400
    zc = st = 0
    for _ in range(R2):
        G_, m = 8, 25
        groups = np.repeat(np.arange(G_), m)
        trt = np.repeat(np.arange(G_) % 2, m).astype(float)
        y = 0.4 * trt + 0.5 * np.repeat(g.normal(size=G_), m) + g.normal(size=G_ * m)
        X = np.column_stack([np.ones(G_ * m), trt])
        f = MX.lmm(y, X, groups)
        zc += abs(f.beta[1] - 0.4) <= 1.96 * f.se[1]
        d = MX.satterthwaite(f, [0, 1])
        st += abs(f.beta[1] - 0.4) <= stats.t.ppf(0.975, d["df"]) * f.se[1]
    rows = [
        Row(25, r"DerSimonian--Laird, \ $z$", r"5 studies, \ $\tau = 0.15$", "coverage", 0.95, dl / R, R),
        Row(25, r"Hartung--Knapp, \ $t_4$", r"5 studies, \ $\tau = 0.15$", "coverage", 0.95, hk / R, R),
        Row(25, r"mixed model, \ $z$ interval", r"8 schools, \ effect between schools", "coverage", 0.95, zc / R2, R2),
        Row(25, r"mixed model, \ Satterthwaite $t$", r"8 schools, \ effect between schools", "coverage", 0.95, st / R2, R2),
    ]
    save_rows(25, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "baseball": compute_baseball, "risk": compute_risk, "winners": compute_winners, "components": compute_components,
    "blup": compute_blup, "remlml": compute_remlml, "boundary": compute_boundary, "growth": compute_growth,
    "nested": compute_nested, "crossed": compute_crossed, "league": compute_league, "mundlak": compute_mundlak, "glmm": compute_glmm, "smallarea": compute_smallarea,
    "meta": compute_meta, "rasch": compute_rasch, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
