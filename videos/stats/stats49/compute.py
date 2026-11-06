"""Precompute every number in Part 49 of *Statistics, Built* ("Semiparametric Efficiency").

    OMP_NUM_THREADS=1 python -m videos.stats.stats49.compute            # everything missing (a few minutes)
    python -m videos.stats.stats49.compute --force board

Results are cached in ``.cache/stats49/<name>.json``.  The NSW job-training data are the Museum's; the survey and the
observational sample are the World's; everything else is exact arithmetic or a seeded simulation.

Items:
    hook      adaptive estimation of a symmetric centre: n Var of the mean, median, Hodges-Lehmann and Stone's
              adaptive estimator under five laws, against 1/I; the adaptive estimator's efficiency by n
    geometry  a 2 x 2 table under independence: the gradient, its projection, coordinates for the picture, simulation
    bounds    one-dimensional submodels in the tangent plane: their information bounds by angle, the least favourable
    ate       the ATE's efficiency bound in a smooth world, against IPW's variance, by quadrature and simulation
    onestep   plug-in, one-step and TMLE with nuisances off by n^-0.3: bias, SD and coverage by n
    nsw       the NSW experiment: difference in means, one-step and TMLE; the PSID comparison: ATT by one-step
    dr        double robustness: the one-step's bias with each working model right or wrong
    rates     the product-rate experiment: root-n bias by n for five (a, b); cross-fitting against reuse with k-NN
    mar       the World's survey: mean log income under MAR by complete cases, IPW, regression and AIPW
    intsq     the integrated squared density: plug-in, one-step and U-statistic by bandwidth
    board     Coverage Board rows (the World test)
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import integrate, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import causal as CA
from explainer.stats.kit import learn as LK
from explainer.stats.kit import semipar as SP
from explainer.stats.world import World

CACHE = Cache("stats49")
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


LAWS = ["normal", "logistic", "laplace", "t3", "mixture"]


# ---------------------------------------------------------------------------------------------------------------
def compute_hook():
    r = rng(49011)
    n, reps = 400, 4000
    out = {"n": n, "reps": reps, "laws": LAWS, "rows": []}
    for law in LAWS:
        m, md, hl, ad = [], [], [], []
        for _ in range(reps):
            x = SP.draw_symmetric(law, r, n)
            m.append(x.mean())
            md.append(np.median(x))
            hl.append(SP.hodges_lehmann(x))
            ad.append(SP.adaptive_location(x)["est"])
        bound = 1 / SP.fisher_location(law)
        out["rows"].append({"law": law, "bound": bound, "mean": n * np.var(m), "median": n * np.var(md), "hl": n * np.var(hl),
                            "adaptive": n * np.var(ad)})
    by_n = []
    for nn, rr in ((100, 4000), (400, 4000), (1600, 3000)):
        ad = [SP.adaptive_location(SP.draw_symmetric("t3", r, nn))["est"] for _ in range(rr)]
        by_n.append({"n": nn, "eff": (1 / SP.fisher_location("t3")) / (nn * np.var(ad)), "reps": rr})
    out["by_n"] = by_n
    return out


def compute_geometry():
    p1, p2 = np.array([0.3, 0.7]), np.array([0.6, 0.4])
    P = np.outer(p1, p2).ravel()
    T = SP.independence_scores(2, 2)
    phi = SP.gradient_discrete(lambda q: q[0], P)
    eff = SP.project(P, phi, T)
    B = SP.l2_basis(P, list(T) + [np.eye(4)[0]])
    r = rng(4902)
    n, reps = 400, 20000
    cells = r.choice(4, size=(reps, n), p=P)
    cell = (cells == 0).mean(axis=1)
    x1 = (cells <= 1).mean(axis=1)  # X1 = first row: cells 0, 1
    x2 = np.isin(cells, [0, 2]).mean(axis=1)  # X2 = first column: cells 0, 2
    prod = x1 * x2
    # pathwise derivatives along three submodels of independence, against <phi, s> and <phi*, s>
    paths = []
    for name, s in (("row", T[0]), ("column", T[2]), ("both", T[0] + 2 * T[3])):
        s = SP.center(P, s)

        def psi_t(t, s=s):
            q1 = np.array([P.reshape(2, 2)[0].sum(), P.reshape(2, 2)[1].sum()])
            q2 = np.array([P.reshape(2, 2)[:, 0].sum(), P.reshape(2, 2)[:, 1].sum()])
            pt = P * (1 + t * s)
            # project the moved law back onto independence: product of its margins (first order the same)
            m1 = np.array([pt[:2].sum(), pt[2:].sum()])
            m2 = np.array([pt[0] + pt[2], pt[1] + pt[3]])
            return float(m1[0] * m2[0])

        der = (psi_t(1e-6) - psi_t(-1e-6)) / 2e-6
        paths.append({"name": name, "deriv": der, "ip_phi": SP.inner(P, phi, s), "ip_eff": SP.inner(P, eff, s)})
    # three models, one estimand: nonparametric, independence, independence with the column margin known
    q1 = 0.6
    p1 = 0.3
    bound_known = q1 ** 2 * p1 * (1 - p1)
    return {"P": P, "phi": phi, "eff": eff, "bound_np": SP.bound(P, phi), "bound": SP.bound(P, eff), "paths": paths,
            "bound_known": bound_known,
            "c_phi": SP.coords(P, phi, B), "c_eff": SP.coords(P, eff, B), "sim_cell": n * cell.var(), "sim_prod": n * prod.var(),
            "n": n, "reps": reps}


def compute_bounds():
    g = load("geometry")
    c = np.asarray(g["c_eff"])[:2]
    ang = np.linspace(0, np.pi, 181)
    s = np.stack([np.cos(ang), np.sin(ang)], axis=1)
    info = (s @ c) ** 2  # the bound along submodel s: <phi*, s>^2 / <s, s>
    best = float(np.arctan2(c[1], c[0]) % np.pi)
    return {"ang": ang, "bound": info, "best": best, "max": float(np.sum(c ** 2))}


def ate_world_moments():
    """E[(mu1 - mu0 - psi)^2 + 1/e + 1/(1 - e)] for SP.rate_world, by quadrature: the efficiency bound."""
    def integrand(x2, x1):
        e = 0.2 + 0.6 * x1
        cate = 1 + x2
        return (cate - 1.5) ** 2 + 1 / e + 1 / (1 - e)

    b = integrate.dblquad(integrand, 0, 1, 0, 1)[0]

    def ipw2(x2, x1):  # Horvitz-Thompson: E[Y1^2/e + Y0^2/(1 - e)] - psi^2
        e = 0.2 + 0.6 * x1
        m0 = math.sin(2 * math.pi * x2) + x1
        m1 = m0 + 1 + x2
        return (m1 ** 2 + 1) / e + (m0 ** 2 + 1) / (1 - e)

    ht = integrate.dblquad(ipw2, 0, 1, 0, 1)[0] - 1.5 ** 2
    return b, ht


def compute_ate():
    bound, ht = ate_world_moments()
    r = rng(4903)
    n, reps = 1000, 2000
    os_, ip, hj = [], [], []
    for _ in range(reps):
        w = SP.rate_world(n, r)
        os_.append(SP.ate_one_step(w["y"], w["t"], w["mu0"], w["mu1"], w["e"])["est"])
        hj.append(SP.ate_ipw(w["y"], w["t"], w["e"])["est"])
        ip.append(float(np.mean(w["t"] * w["y"] / w["e"] - (1 - w["t"]) * w["y"] / (1 - w["e"]))))
    return {"bound": bound, "ht": ht, "n": n, "reps": reps, "sim_os": n * np.var(os_), "sim_ht": n * np.var(ip), "sim_hajek": n * np.var(hj)}


def compute_onestep():
    r = rng(4904)
    out = {"ns": [250, 1000, 4000, 16000], "rows": []}
    for n in out["ns"]:
        reps = 600 if n <= 4000 else 200
        pl, os_, tm, cpl, cos, ctm = [], [], [], [], [], []
        for _ in range(reps):
            w = SP.rate_world(n, r)
            k = SP.corrupt(w, 0.3, 0.3)
            a = SP.ate_one_step(w["y"], w["t"], k["mu0"], k["mu1"], k["e"])
            b = SP.ate_tmle(w["y"], w["t"], k["mu0"], k["mu1"], k["e"])
            pl.append(a["plugin"])
            os_.append(a["est"])
            tm.append(b["est"])
            cpl.append(abs(a["plugin"] - 1.5) <= 1.645 * a["se"])
            cos.append(a["lo"] <= 1.5 <= a["hi"])
            ctm.append(b["lo"] <= 1.5 <= b["hi"])
        f = lambda v: math.sqrt(n) * (np.mean(v) - 1.5)  # noqa: E731
        out["rows"].append({"n": n, "reps": reps, "rb_plugin": f(pl), "rb_os": f(os_), "rb_tmle": f(tm),
                            "sd_os": math.sqrt(n) * np.std(os_), "cov_plugin": np.mean(cpl), "cov_os": np.mean(cos), "cov_tmle": np.mean(ctm)})
        if n == 1000:
            out["err_plugin"], out["err_os"] = (np.array(pl) - 1.5).tolist(), (np.array(os_) - 1.5).tolist()
    return out


def compute_nsw():
    d = museum.nsw()
    out = {}
    ex = d["sample"] == "experiment"
    X = np.column_stack([d["age"], d["educ"], d["black"], d["hisp"], d["married"], d["nodegree"], d["re74"] / 1000, d["re75"] / 1000])
    y = d["re78"]
    t = d["treat"].astype(float)
    Xe, ye, te = X[ex], y[ex], t[ex]
    n = len(ye)
    dm = CA.diff_means(ye, te.astype(bool), alpha=0.05)
    e = np.full(n, te.mean())

    def ols(Xa, ya, Xb):
        A = np.column_stack([np.ones(len(Xa)), Xa])
        b = np.linalg.lstsq(A, ya, rcond=None)[0]
        return np.column_stack([np.ones(len(Xb)), Xb]) @ b

    mu1, mu0 = ols(Xe[te == 1], ye[te == 1], Xe), ols(Xe[te == 0], ye[te == 0], Xe)
    os_ = SP.ate_one_step(ye, te, mu0, mu1, e, alpha=0.05)
    tm = SP.ate_tmle(ye, te, mu0, mu1, e, alpha=0.05)
    out["experiment"] = {"n": n, "n1": int(te.sum()), "dm": dm["est"], "dm_se": dm["se"], "os": os_["est"], "os_se": os_["se"],
                         "tmle": tm["est"], "tmle_se": tm["se"]}
    # the observational comparison: NSW treated against the PSID men
    ob = (d["sample"] == "psid") | (ex & (d["treat"] == 1))
    Xo, yo, to = X[ob], y[ob], t[ob]
    ps = np.clip(CA.propensity(np.column_stack([Xo, Xo[:, 0] ** 2, Xo[:, 6] ** 2, Xo[:, 7] ** 2]), to.astype(bool)), 0.01, 0.99)
    mu0o = ols(Xo[to == 0], yo[to == 0], Xo)
    att = SP.att_one_step(yo, to, mu0o, ps, alpha=0.05)
    naive = float(yo[to == 1].mean() - yo[to == 0].mean())
    reg = float(np.mean(yo[to == 1] - mu0o[to == 1]))
    out["psid"] = {"n0": int((to == 0).sum()), "n1": int(to.sum()), "naive": naive, "reg": reg, "att": att["est"], "att_se": att["se"],
                   "benchmark": dm["est"]}
    return out


def compute_dr():
    r = rng(4905)
    n, reps = 2000, 400
    cells = {}
    for om in ("right", "wrong"):
        for pm in ("right", "wrong"):
            b, pl, ip = [], [], []
            for _ in range(reps):
                w = SP.rate_world(n, r)
                if om == "right":
                    mu0, mu1 = w["mu0"], w["mu1"]
                else:  # an outcome model that ignores X: the arm means
                    mu0 = np.full(n, w["y"][w["t"] == 0].mean())
                    mu1 = np.full(n, w["y"][w["t"] == 1].mean())
                e = w["e"] if pm == "right" else np.full(n, w["t"].mean())
                a = SP.ate_one_step(w["y"], w["t"], mu0, mu1, e)
                b.append(a["est"] - 1.5)
                pl.append(a["plugin"] - 1.5)
                ip.append(SP.ate_ipw(w["y"], w["t"], e)["est"] - 1.5)
            cells[f"{om}_{pm}"] = {"bias": float(np.mean(b)), "se": float(np.std(b) / math.sqrt(reps)), "sd": float(np.std(b)),
                                   "plugin": float(np.mean(pl)), "ipw": float(np.mean(ip))}
    return {"n": n, "reps": reps, "cells": cells}


def compute_rates():
    r = rng(4906)
    ab = [(0.5, 0.5), (0.25, 0.25), (0.375, 0.125), (0.125, 0.125), (0.0, 0.0)]
    ns = [250, 1000, 4000, 16000]
    lines = {}
    for a, b in ab:
        vals = []
        for n in ns:
            reps = 300 if n <= 4000 else 120
            out = []
            for _ in range(reps):
                w = SP.rate_world(n, r)
                k = SP.corrupt(w, a, b)
                out.append(SP.ate_one_step(w["y"], w["t"], k["mu0"], k["mu1"], k["e"])["est"] - 1.5)
            vals.append(math.sqrt(n) * float(np.mean(out)))
        lines[f"{a}_{b}"] = vals
    # cross-fitting against reusing the data, with 5-NN nuisances
    reps, n = 200, 600
    res = {"reuse": [], "cross": []}
    for _ in range(reps):
        w = SP.rate_world(n, r)
        X, t, y = w["X"], w["t"], w["y"]
        for mode in ("reuse", "cross"):
            mu0, mu1, e = np.zeros(n), np.zeros(n), np.zeros(n)
            folds = r.permutation(np.arange(n) % 2) if mode == "cross" else np.zeros(n, int)
            for kf in (0, 1) if mode == "cross" else (0,):
                te = folds == kf
                tr = ~te if mode == "cross" else np.ones(n, bool)
                m1, m0 = tr & (t == 1), tr & (t == 0)
                mu1[te] = LK.knn_predict(X[m1], y[m1], X[te], 5)
                mu0[te] = LK.knn_predict(X[m0], y[m0], X[te], 5)
                e[te] = np.clip(LK.knn_predict(X[tr], t[tr], X[te], 25), 0.05, 0.95)
            a = SP.ate_one_step(y, t, mu0, mu1, e)
            res[mode].append((a["est"] - 1.5, a["lo"] <= 1.5 <= a["hi"], a["se"]))
    cf = {m: {"bias": float(np.mean([v[0] for v in res[m]])), "sd": float(np.std([v[0] for v in res[m]])),
              "se": float(np.mean([v[2] for v in res[m]])), "cover": float(np.mean([v[1] for v in res[m]]))} for m in res}
    return {"ns": ns, "ab": ab, "lines": lines, "cf": cf, "cf_n": n, "cf_reps": reps}


def compute_mar():
    m = World().missing
    li = m["log_income"]
    miss = m["mar"]
    R = (~miss).astype(float)
    region = m["region"]
    regs = np.unique(region)
    Xr = np.column_stack([m["age"]] + [(region == g).astype(float) for g in regs[1:]])
    truth = float(li.mean())
    e_true = 1 - m["p_mar"]
    e_hat = CA.propensity(Xr, R.astype(bool))
    # regression of log income on age, age^2, sex and region among respondents
    Xo = np.column_stack([np.ones(len(li)), m["age"], m["age"] ** 2 / 100, m["male"].astype(float)] + [(region == g).astype(float) for g in regs[1:]])
    b = np.linalg.lstsq(Xo[R == 1], li[R == 1], rcond=None)[0]
    m_hat = Xo @ b
    Xw = np.column_stack([np.ones(len(li)), m["male"].astype(float)])  # a wrong outcome model: sex only
    bw = np.linalg.lstsq(Xw[R == 1], li[R == 1], rcond=None)[0]
    m_wrong = Xw @ bw
    est = SP.mar_mean(li, R, Xr, e_hat, m_hat, alpha=0.1)
    est_true = SP.mar_mean(li, R, Xr, e_true, m_hat, alpha=0.1)
    wrong_om = SP.mar_mean(li, R, Xr, e_hat, m_wrong, alpha=0.1)
    wrong_ps = SP.mar_mean(li, R, Xr, np.full(len(li), R.mean()), m_hat, alpha=0.1)
    return {"n": len(li), "n_obs": int(R.sum()), "truth": truth, "est": est, "true_e": est_true, "wrong_om": wrong_om, "wrong_ps": wrong_ps,
            "regions": len(regs)}


def compute_intsq():
    r = rng(4907)
    psi = SP.int_sq_normal()
    n, reps = 400, 600
    hs = [0.05, 0.1, 0.2, 0.3, 0.45, 0.6]
    rows = []
    for h in hs:
        v = [SP.int_sq_estimates(r.standard_normal(n), h, r) for _ in range(reps)]
        row = {"h": h}
        for k in ("plugin", "one_step", "ustat"):
            a = np.array([x[k] for x in v])
            row[k] = {"rbias": math.sqrt(n) * (a.mean() - psi), "sd": math.sqrt(n) * a.std()}
        rows.append(row)
    # the efficient variance: 4 Var f(X) = 4 (int f^3 - (int f^2)^2)
    f3 = 1 / (2 * math.pi * math.sqrt(3))
    return {"psi": psi, "n": n, "reps": reps, "rows": rows, "eff_sd": math.sqrt(4 * (f3 - psi ** 2))}


# ------------------------------------------------------------------------------------------------- the board
def obs_sample(g, n=2000):
    """n patients from the World's eligible pool (Part 36's observational world, with gentler doctors): the drug is
    prescribed with log-odds (base - 152)/12 + 0.02 (age - 65) + 0.02 (bmi - 28), so propensities run from about 0.2
    to 0.98 rather than to 0.9997."""
    t = World().trial
    k = g.choice(len(t["pool"]), n, replace=False)
    base, age, bmi, fem = t["base_pool"][k], t["age_pool"][k], t["bmi_pool"][k], t["female_pool"][k].astype(float)
    y0 = t["y0_pool"][k]
    tau = t["tau_pool"][k]
    lo = (base - 152) / 12 + 0.02 * (age - 65) + 0.02 * (bmi - 28)
    e = 1 / (1 + np.exp(-lo))
    z = (g.random(n) < e).astype(float)
    y = np.where(z == 1, y0 + tau, y0)
    X = np.column_stack([base, age, bmi, fem])
    return {"X": X, "t": z, "y": y, "e": e, "ate": float(tau.mean())}


def nuisances(X, t, y, folds, k_out=15, k_ps=40):
    """Cross-fitted k-NN outcome regressions on standardized X, with two propensities: logistic and k-NN."""
    n = len(y)
    Z = (X - X.mean(axis=0)) / X.std(axis=0)
    mu0, mu1, el, ek = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
    for kf in np.unique(folds):
        te = folds == kf
        tr = ~te
        m1, m0 = tr & (t == 1), tr & (t == 0)
        mu1[te] = LK.knn_predict(Z[m1], y[m1], Z[te], k_out)
        mu0[te] = LK.knn_predict(Z[m0], y[m0], Z[te], k_out)
        w = CA.logit_fit(np.column_stack([np.ones(tr.sum()), Z[tr]]), t[tr])
        el[te] = np.clip(CA.logit_predict(w, np.column_stack([np.ones(te.sum()), Z[te]])), 0.02, 0.98)
        ek[te] = np.clip(LK.knn_predict(Z[tr], t[tr], Z[te], k_ps), 0.02, 0.98)
    return mu0, mu1, el, ek


def compute_board():
    g = rng(4910)
    reps, n = 300, 2000
    hit = {k: [] for k in ("plugin", "ipw", "os", "tmle", "os_knn")}
    bias = {k: [] for k in hit}
    q = stats.norm.ppf(0.95)
    for _ in range(reps):
        s = obs_sample(g, n)
        X, t, y, ate = s["X"], s["t"], s["y"], s["ate"]
        folds = g.permutation(np.arange(n) % 2)
        mu0, mu1, el, ek = nuisances(X, t, y, folds)
        a = SP.ate_one_step(y, t, mu0, mu1, el)
        b = SP.ate_tmle(y, t, mu0, mu1, el)
        ip = SP.ate_ipw(y, t, el)
        c = SP.ate_one_step(y, t, mu0, mu1, ek)
        hit["plugin"].append(abs(a["plugin"] - ate) <= q * a["se"])
        hit["ipw"].append(ip["lo"] <= ate <= ip["hi"])
        hit["os"].append(a["lo"] <= ate <= a["hi"])
        hit["tmle"].append(b["lo"] <= ate <= b["hi"])
        hit["os_knn"].append(c["lo"] <= ate <= c["hi"])
        for k, v in (("plugin", a["plugin"]), ("ipw", ip["est"]), ("os", a["est"]), ("tmle", b["est"]), ("os_knn", c["est"])):
            bias[k].append(v - ate)
    setting = r"World: \ doctors choose, \ $n = 2{,}000$"
    names = {"plugin": r"plug-in, \ $k$-NN outcome models", "ipw": r"IPW, \ logistic propensity", "os": r"one-step, \ $k$-NN $+$ logistic, \ cross-fitted",
             "tmle": r"TMLE, \ $k$-NN $+$ logistic, \ cross-fitted", "os_knn": r"one-step, \ $k$-NN for both"}
    rows = [Row(49, names[k], setting, "coverage", 0.9, float(np.mean(v)), reps) for k, v in hit.items()]
    save_rows(49, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows],
            "bias": {k: float(np.mean(v)) for k, v in bias.items()}, "sd": {k: float(np.std(v)) for k, v in bias.items()}}


ITEMS = {
    "hook": compute_hook, "geometry": compute_geometry, "bounds": compute_bounds, "ate": compute_ate, "onestep": compute_onestep,
    "nsw": compute_nsw, "dr": compute_dr, "rates": compute_rates, "mar": compute_mar, "intsq": compute_intsq, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
