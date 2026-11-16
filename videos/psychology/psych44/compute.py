"""Precompute every number in Part 44 of *Psychology, Built* ("Latent Variables").

    python -m videos.psychology.psych44.compute            # everything missing (a few minutes)
    python -m videos.psychology.psych44.compute --force cutoffs

Results are cached in ``.cache/psych44/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.sem``), checked against lavaan's published results in ``tests/psychology/test_sem.py``.

Items:
    equivalent  1,000 simulated people from a chain X -> M -> Y (paths 0.5 and 0.6): the chi-square of the chain, the
                reversed chain, the fork and the collider fitted to the same data
    hs          Holzinger and Swineford's nine tests, 301 children: the correlation matrix; the three-factor CFA
                (loadings, factor correlations, chi-square, RMSEA, CFI, TLI, SRMR); the one-factor model
    invariance  the three-factor model in the two schools: configural, metric and scalar, with the latent mean
                differences
    cutoffs     200 samples of 301 from the fitted three-factor model, and 200 from the same model with one
                cross-loading of 0.4 left out: the distributions of RMSEA and CFI under each
    attenuation two latent traits correlated 0.5, three indicators each with standardized loadings 0.6, 500 people:
                the correlation of sum scores, and the latent correlation the CFA recovers
    omega       the reliability of each three-test sum from the loadings (omega) and the covariances (alpha), and a
                four-item set with loadings 0.9, 0.8, 0.3 and 0.2
    mediation   a randomized X, a mediator with an unmeasured confounder and no effect on Y: the indirect effect and
                its bootstrap interval, against a truth of zero
    panel       2,000 people, 4 waves, stable correlated traits and no cross effects: the cross-lagged regression
                against the same regression on within-person deviations
    network     a one-factor model with loadings 0.8, 0.7, 0.6, 0.5 and the network of partial correlations that
                implies exactly the same matrix
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import sem as E

CACHE = Cache("psych44")
load = CACHE.load

P3 = np.zeros((9, 3), int)
P3[0:3, 0] = 1
P3[3:6, 1] = 1
P3[6:9, 2] = 1


def compute_equivalent() -> dict:
    rng = np.random.default_rng(44)
    n = 1000
    X = rng.normal(0, 1, n)
    M = 0.5 * X + np.sqrt(1 - 0.25) * rng.normal(0, 1, n)
    Y = 0.6 * M + np.sqrt(1 - 0.36) * rng.normal(0, 1, n)
    R = np.corrcoef([X, M, Y])
    rxy, rxm, rmy = R[0, 2], R[0, 1], R[1, 2]
    partial = (rxy - rxm * rmy) / np.sqrt((1 - rxm ** 2) * (1 - rmy ** 2))
    t_chain = float(-n * np.log(1 - partial ** 2))
    t_coll = float(-n * np.log(1 - rxy ** 2))
    return {"R": R, "chain": t_chain, "reverse": t_chain, "fork": t_chain, "collider": t_coll, "n": n}


def compute_hs() -> dict:
    h = opendata.holzinger_1939()
    X = h["X"]
    n = len(X)
    S = np.cov(X.T, bias=True)
    r3 = E.fit_cfa(S, n, P3)
    r1 = E.fit_cfa(S, n, np.ones((9, 1), int))
    d = np.sqrt(np.diag(r3["Phi"]))
    std = r3["L"] * d[None, :] / np.sqrt(np.diag(r3["Sigma"]))[:, None]
    return {"R": np.corrcoef(X.T), "L": r3["L"], "std": std, "phi_cor": r3["Phi"] / np.outer(d, d),
            **{f"t3_{k}": r3[k] for k in ("T", "df", "rmsea", "cfi", "tli", "srmr", "T0", "df0")},
            **{f"t1_{k}": r1[k] for k in ("T", "df", "rmsea", "cfi", "tli", "srmr")}, "n": n}


def compute_invariance() -> dict:
    h = opendata.holzinger_1939()
    X, sch = h["X"], np.array(h["school"])
    gs = [X[sch == "Pasteur"], X[sch == "Grant-White"]]
    out = {"n_pasteur": len(gs[0]), "n_gw": len(gs[1])}
    for lev in ("configural", "metric", "scalar"):
        r = E.fit_multigroup(gs, P3, lev)
        out[f"{lev}_T"], out[f"{lev}_df"] = r["T"], r["df"]
        if lev == "scalar":
            out["kappa"] = r["kappa"][0]
    return out


def compute_cutoffs() -> dict:
    h = opendata.holzinger_1939()
    X = h["X"]
    n = len(X)
    fit = E.fit_cfa(np.cov(X.T, bias=True), n, P3)
    Sig_ok = fit["Sigma"]
    L = fit["L"].copy()
    L[8, 0] = 0.4 * np.sqrt(fit["Sigma"][8, 8] / fit["Phi"][0, 0])  # x9 also loads on the visual factor
    Sig_bad = E.cfa_implied(L, fit["Phi"], fit["theta"])
    rng = np.random.default_rng(44)
    out = {}
    for name, Sig in (("ok", Sig_ok), ("miss", Sig_bad)):
        rm, cf = [], []
        for _ in range(200):
            Z = rng.multivariate_normal(np.zeros(9), Sig, n)
            r = E.fit_cfa(np.cov(Z.T, bias=True), n, P3)
            rm.append(r["rmsea"])
            cf.append(r["cfi"])
        out[f"{name}_rmsea"], out[f"{name}_cfi"] = np.array(rm), np.array(cf)
    return out


def compute_attenuation() -> dict:
    rng = np.random.default_rng(44)
    n = 500
    F = rng.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], n)
    lam = 0.6
    X = np.column_stack([lam * F[:, j // 3] + np.sqrt(1 - lam ** 2) * rng.normal(0, 1, n) for j in range(6)])
    s1, s2 = X[:, :3].sum(1), X[:, 3:].sum(1)
    P = np.zeros((6, 2), int)
    P[:3, 0] = 1
    P[3:, 1] = 1
    r = E.fit_cfa(np.cov(X.T, bias=True), n, P)
    d = np.sqrt(np.diag(r["Phi"]))
    a1 = np.corrcoef(X[:, :3].T)
    k = 3
    rbar = a1[np.triu_indices(3, 1)].mean()
    alpha = k * rbar / (1 + (k - 1) * rbar)
    return {"sum_r": float(np.corrcoef(s1, s2)[0, 1]), "latent_r": float(r["Phi"][0, 1] / (d[0] * d[1])),
            "alpha": float(alpha), "true": 0.5}


def compute_omega() -> dict:
    """Reliability of each factor's three-test sum from the loadings (McDonald's omega) and from the covariances
    (Cronbach's alpha), on Holzinger and Swineford's data; and a congeneric set whose loadings differ widely."""
    h = opendata.holzinger_1939()
    X = h["X"]
    n = len(X)
    S = np.cov(X.T, bias=True)
    r = E.fit_cfa(S, n, P3)
    out = {"omega": [], "alpha": []}
    for f in range(3):
        idx = np.arange(3 * f, 3 * f + 3)
        lam = r["L"][idx, f] * np.sqrt(r["Phi"][f, f])
        th = r["theta"][idx]
        out["omega"].append(float(lam.sum() ** 2 / (lam.sum() ** 2 + th.sum())))
        C = S[np.ix_(idx, idx)]
        out["alpha"].append(float(3 / 2 * (1 - np.trace(C) / C.sum())))
    lam = np.array([0.9, 0.8, 0.3, 0.2])
    R = np.outer(lam, lam)
    np.fill_diagonal(R, 1)
    out["cong_alpha"] = float(4 / 3 * (1 - 4 / R.sum()))
    out["cong_omega"] = float(lam.sum() ** 2 / (lam.sum() ** 2 + (1 - lam ** 2).sum()))
    out["cong_lam"] = lam
    return out


def compute_mediation() -> dict:
    return E.mediation(seed=44)


def compute_network() -> dict:
    f = E.factor_as_network([0.8, 0.7, 0.6, 0.5])
    return {"R": f["R"], "partial": f["partial"], "max_err": float(np.abs(f["R"] - f["reproduced"]).max())}


def compute_panel() -> dict:
    """Hamaker, Kuiper and Grasman's trap: stable person differences in two traits, correlated, and no
    within-person cross-lagged effect at all.  The cross-lagged panel regression finds one; the same regression on
    within-person deviations (which Psyche knows, and the random-intercept model estimates) does not."""
    rng = np.random.default_rng(44)
    n, waves = 2000, 4
    B = rng.multivariate_normal([0, 0], [[1, 0.6], [0.6, 1]], n)
    wx = np.zeros((n, waves))
    wy = np.zeros((n, waves))
    wx[:, 0], wy[:, 0] = rng.normal(0, 1, n), rng.normal(0, 1, n)
    for t in range(1, waves):
        wx[:, t] = 0.3 * wx[:, t - 1] + np.sqrt(1 - 0.09) * rng.normal(0, 1, n)
        wy[:, t] = 0.3 * wy[:, t - 1] + np.sqrt(1 - 0.09) * rng.normal(0, 1, n)
    x, y = B[:, [0]] + wx, B[:, [1]] + wy

    def lag(a, b, c):
        X = np.column_stack([np.ones(n * (waves - 1)), a[:, :-1].ravel(), b[:, :-1].ravel()])
        coef = np.linalg.lstsq(X, c[:, 1:].ravel(), rcond=None)[0]
        res = c[:, 1:].ravel() - X @ coef
        se = np.sqrt(np.diag(res.var() * np.linalg.inv(X.T @ X)))
        return float(coef[2]), float(se[2])

    cl, cl_se = lag(y, x, y)  # y_{t+1} on y_t and x_t
    wl, wl_se = lag(wy, wx, wy)
    return {"clpm": cl, "clpm_se": cl_se, "within": wl, "within_se": wl_se, "n": n, "waves": waves,
            "trait_r": 0.6, "auto": 0.3}


ITEMS = {"panel": compute_panel, "equivalent": compute_equivalent, "hs": compute_hs, "invariance": compute_invariance,
         "cutoffs": compute_cutoffs, "attenuation": compute_attenuation, "omega": compute_omega, "mediation": compute_mediation,
         "network": compute_network}

if __name__ == "__main__":
    CACHE.main(ITEMS)
