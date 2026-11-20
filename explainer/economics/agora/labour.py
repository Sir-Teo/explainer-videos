"""Agora's labour, part I (Part 38): labour supply with income effects (the backward bend; Marshallian, Hicksian and
Frisch elasticities); participation; labour demand and a wage floor in a competitive market; monopsony with a minimum
wage; the border experiment run on the Island's restaurants under competition and under monopsony; least squares and
two-stage least squares for the return to schooling; Roy's model of sorting and Heckman's two-step correction.

numpy and scipy only.  Wages are dollars an hour; hours are a share of a week's available time unless stated.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, minimize
from scipy.stats import norm


# --- labour supply --------------------------------------------------------------------------------------------------
def hours(w: float, y: float = 0.2, gamma: float = 2.0, phi: float = 0.5, psi: float = 1.0) -> float:
    """Hours (a share of the available time) that maximize c^(1-gamma)/(1-gamma) - psi h^(1+1/phi)/(1+1/phi) with
    c = w h + y: the first-order condition w (w h + y)^(-gamma) = psi h^(1/phi).  ``phi`` is the Frisch elasticity;
    ``gamma`` > 1 makes the income effect strong enough to bend the curve back at high wages."""
    def foc(h):
        return w * (w * h + y) ** (-gamma) - psi * h ** (1 / phi)
    return float(brentq(foc, 1e-12, 50.0, xtol=1e-14))


def supply_elasticities(w: float, y: float = 0.2, gamma: float = 2.0, phi: float = 0.5, psi: float = 1.0) -> dict:
    """At wage ``w``: hours, the Marshallian (uncompensated) elasticity, the income effect w dh/dy, the Hicksian
    (compensated) elasticity by Slutsky, e_c = e_u - w dh/dy, and the Frisch elasticity (phi, holding the marginal
    utility of wealth fixed)."""
    h = hours(w, y, gamma, phi, psi)
    dw, dy = 1e-6 * w, 1e-6
    dh_dw = (hours(w + dw, y, gamma, phi, psi) - hours(w - dw, y, gamma, phi, psi)) / (2 * dw)
    dh_dy = (hours(w, y + dy, gamma, phi, psi) - hours(w, max(y - dy, 0.0), gamma, phi, psi)) / (2 * dy)
    e_u = w / h * dh_dw
    inc = w * dh_dy
    return {"h": h, "marshallian": e_u, "income_effect": inc, "hicksian": e_u - inc, "frisch": phi}


def participation(w, mu: float = np.log(12.0), sigma: float = 0.5):
    """The share who work at wage ``w`` when reservation wages are lognormal (median exp(mu))."""
    return norm.cdf((np.log(np.asarray(w, float)) - mu) / sigma)


# --- a competitive market with a wage floor ---------------------------------------------------------------------
def competitive(A: float = 100.0, eps_d: float = 0.5, B: float = 4.0, eps_s: float = 1.0) -> dict:
    """Demand A w^(-eps_d), supply B w^eps_s: the market wage and employment."""
    w = (A / B) ** (1 / (eps_d + eps_s))
    return {"w": float(w), "L": float(B * w ** eps_s)}


def floor_competitive(m, A: float = 100.0, eps_d: float = 0.5, B: float = 4.0, eps_s: float = 1.0):
    """Employment with a minimum wage ``m``: the wage is the larger of m and the market wage, and employment is the
    short side of the market there, min(demand, supply); a floor below the market wage does not bind."""
    w = np.maximum(np.asarray(m, float), competitive(A, eps_d, B, eps_s)["w"])
    return np.minimum(A * w ** (-eps_d), B * w ** eps_s)


# --- monopsony -------------------------------------------------------------------------------------------------------
def monopsony(a: float = 30.0, b: float = 0.3, eta: float = 3.0, B: float = 1.0) -> dict:
    """One employer facing labour supply L = B w^eta, with the value of the marginal worker a L^(-b).  It hires where
    the marginal cost of labour, w (1 + 1/eta), equals the marginal product; a competitive market would hire where
    the wage itself does.  Returns both wages and employments, and the markdown 1 - w / MRPL = 1 / (1 + eta)."""
    def mono(L):
        return (L / B) ** (1 / eta) * (1 + 1 / eta) - a * L ** (-b)

    def comp(L):
        return (L / B) ** (1 / eta) - a * L ** (-b)
    Lm = brentq(mono, 1e-9, 1e9)
    Lc = brentq(comp, 1e-9, 1e9)
    return {"w_m": float((Lm / B) ** (1 / eta)), "L_m": float(Lm), "mrpl_m": float(a * Lm ** (-b)),
            "w_c": float((Lc / B) ** (1 / eta)), "L_c": float(Lc), "markdown": 1 / (1 + eta)}


def floor_monopsony(m, a: float = 30.0, b: float = 0.3, eta: float = 3.0, B: float = 1.0):
    """Employment at a monopsonist under a minimum wage ``m``: below the monopsony wage the floor does not bind;
    between it and the competitive wage the firm hires everyone willing to work at m (employment rises); above the
    competitive wage it hires where the marginal product equals m (employment falls)."""
    M = monopsony(a, b, eta, B)
    m = np.asarray(m, float)
    supply = B * m ** eta
    demand = (a / m) ** (1 / b)
    out = np.where(m <= M["w_m"], M["L_m"], np.minimum(supply, demand))
    return out


# --- the border experiment on the Island ---------------------------------------------------------------------------
def border_experiment(regime: str = "competitive", n_treat: int = 331, n_ctrl: int = 79, m0: float = 4.25,
                      m1: float = 5.05, eps_d: float = 0.5, eta: float = 3.0, trend: float = -0.06,
                      noise: float = 0.25, seed: int = 0) -> dict:
    """Restaurants in a treated state (whose minimum rises from m0 to m1) and a control state, each with its own
    scale and wage-setting.  Under ``competitive`` a store pays the market wage (or the minimum) and hires on its
    demand curve with elasticity eps_d.  Under ``monopsony`` a store faces labour supply of elasticity ``eta`` and pays
    the monopsony wage, so a minimum between that and the competitive wage raises its hiring.  Both states share a
    common trend; each store's employment has multiplicative noise.  Returns the difference in differences of log
    employment and of log wages, their ratio (the own-wage elasticity), and the stores' data."""
    rng = np.random.default_rng(seed)
    n = n_treat + n_ctrl
    treat = np.r_[np.ones(n_treat, bool), np.zeros(n_ctrl, bool)]
    scale = np.exp(rng.normal(np.log(20.0), 0.35, n))
    # each store's competitive wage (its value of labour at its scale), around the old minimum
    wc = np.exp(rng.normal(np.log(4.6), 0.12, n))
    if regime == "competitive":
        w0 = np.maximum(wc, m0)
        w1 = np.where(treat, np.maximum(wc, m1), np.maximum(wc, m0))
        L0 = scale * (w0 / wc) ** (-eps_d)
        L1 = scale * (w1 / wc) ** (-eps_d)
    elif regime == "monopsony":
        wm = wc * eta / (1 + eta)                       # the monopsony wage, a markdown below the competitive one
        def emp(w):
            sup = scale * (w / wc) ** eta               # labour supply, normalized to `scale` at the competitive wage
            dem = scale * (w / wc) ** (-eps_d)
            return np.minimum(sup, dem)
        w0 = np.maximum(wm, m0)
        w1 = np.where(treat, np.maximum(wm, m1), np.maximum(wm, m0))
        L0, L1 = emp(w0), emp(w1)
    else:
        raise ValueError(regime)
    L0 = L0 * np.exp(rng.normal(0, noise, n))
    L1 = L1 * np.exp(trend + rng.normal(0, noise, n))
    dl = np.log(L1) - np.log(L0)
    dw = np.log(w1) - np.log(w0)
    did_l = float(dl[treat].mean() - dl[~treat].mean())
    did_w = float(dw[treat].mean() - dw[~treat].mean())
    se = float(np.sqrt(dl[treat].var(ddof=1) / n_treat + dl[~treat].var(ddof=1) / n_ctrl))
    return {"regime": regime, "did_emp": did_l, "did_wage": did_w, "owe": did_l / did_w, "se_emp": se,
            "treat": treat.tolist(), "L0": L0.tolist(), "L1": L1.tolist(), "w0": w0.tolist(), "w1": w1.tolist()}


# --- least squares and two-stage least squares ---------------------------------------------------------------------
def ols(y, X) -> dict:
    """Least squares with heteroskedasticity-robust (HC1) standard errors; X should include a constant."""
    y, X = np.asarray(y, float), np.asarray(X, float)
    n, k = X.shape
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    V = XtXi @ (X.T * e ** 2) @ X @ XtXi * n / (n - k)
    return {"b": b.tolist(), "se": np.sqrt(np.diag(V)).tolist(), "n": n, "r2": float(1 - e.var() / y.var())}


def tsls(y, X, Z) -> dict:
    """Two-stage least squares of y on X with instruments Z (both including the exogenous columns), with HC1 standard
    errors and the first-stage F statistic for the excluded instruments (taken as the columns of Z not in X)."""
    y, X, Z = (np.asarray(v, float) for v in (y, X, Z))
    n, k = X.shape
    PZ = Z @ np.linalg.solve(Z.T @ Z, Z.T @ X)
    b = np.linalg.solve(PZ.T @ X, PZ.T @ y)
    e = y - X @ b
    A = np.linalg.inv(PZ.T @ PZ)
    V = A @ (PZ.T * e ** 2) @ PZ @ A * n / (n - k)
    # first stage for the endogenous columns (those of X not in Z), F on the excluded instruments
    endo = [j for j in range(k) if not any(np.allclose(X[:, j], Z[:, i]) for i in range(Z.shape[1]))]
    excl = [i for i in range(Z.shape[1]) if not any(np.allclose(Z[:, i], X[:, j]) for j in range(k))]
    F = float("nan")
    if len(endo) == 1 and excl:
        x = X[:, endo[0]]
        full = ols(x, Z)
        keep = [i for i in range(Z.shape[1]) if i not in excl]
        rest = np.linalg.lstsq(Z[:, keep], x, rcond=None)[0]
        rss_r = np.sum((x - Z[:, keep] @ rest) ** 2)
        rss_u = np.sum((x - Z @ np.array(full["b"])) ** 2)
        F = float((rss_r - rss_u) / len(excl) / (rss_u / (n - Z.shape[1])))
    return {"b": b.tolist(), "se": np.sqrt(np.diag(V)).tolist(), "n": n, "first_stage_F": F}


# --- Roy's model and Heckman's correction --------------------------------------------------------------------------
def roy(n: int = 20000, mu: tuple = (2.6, 2.5), sd: tuple = (0.4, 0.6), rho: float = 0.3, cost_sd: float = 0.3,
        seed: int = 0) -> dict:
    """Roy (1951): each person has a log wage in two occupations (fishing and the boatyard, say), jointly normal, and
    a cost of choosing the second, drawn independently; each chooses the larger net wage.  The observed wages are
    selected: those in each occupation are better at it than the average person would be."""
    rng = np.random.default_rng(seed)
    cov = np.array([[sd[0] ** 2, rho * sd[0] * sd[1]], [rho * sd[0] * sd[1], sd[1] ** 2]])
    w = rng.multivariate_normal(mu, cov, n)
    z = rng.normal(0, cost_sd, n)                       # the cost of the second occupation (observed: a shifter)
    second = w[:, 1] - z > w[:, 0]
    return {"w1": w[:, 0].tolist(), "w2": w[:, 1].tolist(), "z": z.tolist(), "second": second.tolist(),
            "share_second": float(second.mean()), "mean1_all": float(w[:, 0].mean()),
            "mean1_obs": float(w[~second, 0].mean()), "mean2_all": float(w[:, 1].mean()),
            "mean2_obs": float(w[second, 1].mean())}


def probit(d, Z) -> np.ndarray:
    """Maximum-likelihood probit coefficients of a 0/1 outcome on Z (with a constant column)."""
    d, Z = np.asarray(d, float), np.asarray(Z, float)

    def nll(g):
        p = np.clip(norm.cdf(Z @ g), 1e-12, 1 - 1e-12)
        return -np.sum(d * np.log(p) + (1 - d) * np.log(1 - p))

    def grad(g):
        xb = Z @ g
        p = np.clip(norm.cdf(xb), 1e-12, 1 - 1e-12)
        phi = norm.pdf(xb)
        return -Z.T @ (phi * (d / p - (1 - d) / (1 - p)))
    r = minimize(nll, np.zeros(Z.shape[1]), jac=grad, method="BFGS", options={"gtol": 1e-9, "maxiter": 1000})
    return r.x


def heckman_two_step(y, X, d, Z) -> dict:
    """Heckman (1979): a probit of selection d on Z, the inverse Mills ratio for the selected, then least squares of
    y on X and the ratio among the selected.  Returns the corrected coefficients, the naive ones, and the ratio's
    coefficient (the covariance of the outcome's error with selection)."""
    y, X, d, Z = (np.asarray(v, float) for v in (y, X, d, Z))
    g = probit(d, Z)
    xb = Z @ g
    imr = norm.pdf(xb) / np.clip(norm.cdf(xb), 1e-12, None)
    s = d > 0.5
    naive = ols(y[s], X[s])
    corr = ols(y[s], np.column_stack([X[s], imr[s]]))
    return {"probit": g.tolist(), "naive": naive["b"], "corrected": corr["b"][:-1], "lambda": corr["b"][-1],
            "n_selected": int(s.sum())}
