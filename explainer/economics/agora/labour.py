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


# ======================================================================================================================
# Part II (Part 39): the wage structure
# ======================================================================================================================
# --- the canonical model: two skills and the race between education and technology ---------------------------------
def skill_premium(rel_supply, rel_tech, sigma: float):
    """The log college premium in the canonical model, with output (A_L L)^rho + (A_H H)^rho, rho = 1 - 1/sigma:
    ln(w_H/w_L) = (1 - 1/sigma) ln(A_H/A_L) - (1/sigma) ln(H/L).  Arguments are logs of H/L and A_H/A_L."""
    return (1 - 1 / sigma) * np.asarray(rel_tech, float) - np.asarray(rel_supply, float) / sigma


def implied_demand(log_premium, log_supply, sigma: float):
    """Katz and Murphy's relative demand index, D = ln(w_H/w_L) + ln(H/L)/sigma: the shift in relative demand that,
    with elasticity ``sigma``, reconciles the observed premium with the observed supply."""
    return np.asarray(log_premium, float) + np.asarray(log_supply, float) / sigma


def katz_murphy(log_premium, log_supply, years) -> dict:
    """Least squares of the log premium on a linear trend and log relative supply; sigma = -1/slope."""
    y = np.asarray(log_premium, float)
    t = np.asarray(years, float) - float(np.min(years))
    X = np.column_stack([np.ones_like(t), t, np.asarray(log_supply, float)])
    r = ols(y, X)
    return {"trend": r["b"][1], "slope": r["b"][2], "se_slope": r["se"][2], "sigma": -1 / r["b"][2],
            "corr_trend_supply": float(np.corrcoef(t, X[:, 2])[0, 1]), "n": r["n"]}


# --- tasks: a Ricardian assignment of three skills to a continuum of tasks (Acemoglu and Autor 2011) -----------------
def task_model(L: float = 1.0, M: float = 1.0, H: float = 1.0, beta=(0.0, 1.0, 2.0), auto=None) -> dict:
    """Tasks on [0, 1] combined Cobb-Douglas, so each task gets the same spending.  Low, middle and high skills have
    productivity exp(beta_k i) in task i, so higher skills have a comparative advantage in higher tasks.  Low skills do
    [0, I_L], middle (I_L, I_H), high [I_H, 1]; a band ``auto`` = (a, b) inside the middle range is done by machines.
    The thresholds solve w_k N_k = (spending on k's tasks) and, at each threshold, indifference between the two
    skills: ln w_M - ln w_L = (beta_M - beta_L) I_L and ln w_H - ln w_M = (beta_H - beta_M) I_H.  Returns the
    thresholds, relative wages and the share of output each group earns (machines earn the band's share)."""
    from scipy.optimize import fsolve  # noqa: PLC0415

    a, b = auto if auto else (0.5, 0.5)
    band = b - a

    def eqs(v):
        il, ih = v
        sl, sm, sh = il, (ih - il) - band, 1 - ih
        sm = max(sm, 1e-9)
        return [np.log(sm / M) - np.log(max(sl, 1e-9) / L) - (beta[1] - beta[0]) * il,
                np.log(max(sh, 1e-9) / H) - np.log(sm / M) - (beta[2] - beta[1]) * ih]

    il, ih = fsolve(eqs, [min(0.3, a - 0.05), max(0.7, b + 0.05)], xtol=1e-13)
    sl, sm, sh = il, (ih - il) - band, 1 - ih
    wl, wm, wh = sl / L, sm / M, sh / H
    return {"I_L": float(il), "I_H": float(ih), "share_L": float(sl), "share_M": float(sm), "share_H": float(sh),
            "share_K": float(band), "wM_wL": float(wm / wl), "wH_wM": float(wh / wm), "wH_wL": float(wh / wl),
            "lnw": [float(np.log(wl)), float(np.log(wm)), float(np.log(wh))]}


# --- firms: a worker-firm economy and the two-way fixed-effects (AKM) model -------------------------------------------
def worker_firm_economy(n_workers: int = 20000, n_firms: int = 400, years: int = 6, sd_alpha: float = 0.40,
                        sd_psi: float = 0.15, sort: float = 0.3, move: float = 0.10, sd_e: float = 0.12,
                        seed: int = 0) -> dict:
    """Log wage y_it = alpha_i + psi_j(i,t) + e_it.  Firms' premiums psi_j are drawn once; each worker starts at a
    firm chosen with a tilt towards high-premium firms for high-alpha workers (``sort``); each year a share ``move``
    of workers moves to a new firm chosen the same way.  Returns the panel and the true variance decomposition."""
    rng = np.random.default_rng(seed)
    alpha = rng.normal(0, sd_alpha, n_workers)
    psi = rng.normal(0, sd_psi, n_firms)
    rank = np.argsort(np.argsort(psi)) / (n_firms - 1)          # firm's premium rank in [0, 1]
    z = (alpha - alpha.mean()) / alpha.std()

    def pick(zz):
        # a worker with standardized ability z draws a firm whose premium rank is near Phi(sort * z + noise)
        target = norm.cdf(sort * zz + np.sqrt(1 - sort ** 2) * rng.normal(size=zz.size))
        return np.clip(np.searchsorted(np.sort(rank), target), 0, n_firms - 1)
    order = np.argsort(rank)
    firm = np.empty((n_workers, years), int)
    firm[:, 0] = order[pick(z)]
    for t in range(1, years):
        firm[:, t] = firm[:, t - 1]
        mv = rng.random(n_workers) < move
        firm[mv, t] = order[pick(z[mv])]
    y = alpha[:, None] + psi[firm] + rng.normal(0, sd_e, (n_workers, years))
    a_obs, p_obs = np.repeat(alpha, years), psi[firm].ravel()
    tot = y.var()
    truth = {"var_y": float(tot), "var_alpha": float(a_obs.var()), "var_psi": float(p_obs.var()),
             "cov2": float(2 * np.cov(a_obs, p_obs)[0, 1]), "corr": float(np.corrcoef(a_obs, p_obs)[0, 1])}
    movers = int((firm != firm[:, :1]).any(axis=1).sum())
    return {"y": y, "firm": firm, "alpha": alpha, "psi": psi, "truth": truth, "movers": movers}


def akm(y, firm) -> dict:
    """The two-way fixed-effects model by sparse least squares (LSQR) on the panel: worker and firm dummies, one firm
    normalized to zero.  The firms must be connected by movers.  Returns the estimated effects and the plug-in variance
    decomposition (shares of the variance of y)."""
    from scipy.sparse import csr_matrix, hstack  # noqa: PLC0415
    from scipy.sparse.linalg import lsqr  # noqa: PLC0415

    y = np.asarray(y, float)
    n, T = y.shape
    J = int(firm.max()) + 1
    rows = np.arange(n * T)
    W = csr_matrix((np.ones(n * T), (rows, np.repeat(np.arange(n), T))), shape=(n * T, n))
    F = csr_matrix((np.ones(n * T), (rows, firm.ravel())), shape=(n * T, J))[:, 1:]
    X = hstack([W, F]).tocsr()
    sol = lsqr(X, y.ravel(), atol=1e-10, btol=1e-10, iter_lim=5000)[0]
    a_hat, p_hat = sol[:n], np.r_[0.0, sol[n:]]
    a_obs, p_obs = np.repeat(a_hat, T), p_hat[firm].ravel()
    tot = y.var()
    return {"alpha": a_hat, "psi": p_hat, "var_alpha": float(a_obs.var()), "var_psi": float(p_obs.var()),
            "cov2": float(2 * np.cov(a_obs, p_obs)[0, 1]), "corr": float(np.corrcoef(a_obs, p_obs)[0, 1]),
            "share_psi": float(p_obs.var() / tot), "share_alpha": float(a_obs.var() / tot),
            "share_cov": float(2 * np.cov(a_obs, p_obs)[0, 1] / tot)}


# --- superstars (Rosen 1981) ------------------------------------------------------------------------------------------
def superstars(n: int = 100000, sd_talent: float = 0.10, reach=(1.0, 3.0, 8.0), seed: int = 0) -> dict:
    """Talent q is lognormal with a small spread.  When one performer can serve a larger audience, earnings become a
    steeper function of talent: earnings proportional to q^k, with k the 'reach' of the technology (k = 1: earnings
    track talent).  Returns the top 1% share of talent and of earnings at each reach."""
    rng = np.random.default_rng(seed)
    q = np.exp(rng.normal(0, sd_talent, n))
    qs = np.sort(q)[::-1]
    top = n // 100
    out = {"talent_top1": float(qs[:top].sum() / qs.sum()), "reach": list(reach), "top1": [], "p99_p50": []}
    for k in reach:
        e = qs ** k
        out["top1"].append(float(e[:top].sum() / e.sum()))
        out["p99_p50"].append(float(np.percentile(e, 99) / np.percentile(e, 50)))
    return out


# --- compensating differentials: the hedonic wage locus (Rosen 1974) --------------------------------------------------
def hedonic(n: int = 60, seed: int = 0, r_max: float = 1.0) -> dict:
    """Workers dislike risk r at rate d_i (utility w - d_i r); a firm finds safety costly at rate k_j, so reducing risk
    from r_max costs k_j (r_max - r)^2 / 2.  In a match, the worker's marginal distaste equals the firm's marginal cost
    of safety: d_i = k_j (r_max - r).  Workers who mind risk least sort into firms for which safety is dearest.  The
    wage locus w(r) has slope d at each job's r: it is the envelope of the workers' indifference lines."""
    rng = np.random.default_rng(seed)
    d = np.sort(np.exp(rng.normal(np.log(1.0), 0.35, n)))       # ascending distaste
    k = np.sort(np.exp(rng.normal(np.log(2.0), 0.35, n)))[::-1]  # descending cost of safety
    r = np.clip(r_max - d / k, 0.0, r_max)
    o = np.argsort(r)
    r, d_at = r[o], d[o]
    w = np.r_[0.0, np.cumsum(0.5 * (d_at[1:] + d_at[:-1]) * np.diff(r))]
    slope = np.polyfit(r, w, 1)[0]
    return {"r": r.tolist(), "w": w.tolist(), "d": d_at.tolist(), "slope_ols": float(slope),
            "mean_d": float(d.mean())}


# --- discrimination --------------------------------------------------------------------------------------------------
def becker(share_minority: float, share_unprejudiced: float, d_scale: float = 0.15, n: int = 10000,
           seed: int = 0) -> dict:
    """Becker (1957): each employer hires the same number of workers; an employer with taste d acts as if a minority
    worker cost w_m (1 + d).  Prejudice d is zero for a share of employers and exponential (mean ``d_scale``) for the
    rest.  Minority workers go first to the least prejudiced; the market gap w_maj/w_min - 1 is the taste of the
    marginal employer who must hire them.  If unprejudiced employers can absorb every minority worker, the gap is
    zero."""
    rng = np.random.default_rng(seed)
    d = np.where(rng.random(n) < share_unprejudiced, 0.0, rng.exponential(d_scale, n))
    ds = np.sort(d)
    k = int(np.ceil(share_minority * n)) - 1
    gap = float(ds[max(k, 0)])
    return {"gap": gap, "d_sorted": ds[:: max(n // 400, 1)].tolist(), "share_minority": share_minority,
            "share_unprejudiced": share_unprejudiced}


def phelps(signal, mu=(0.0, 0.0), sd_q: float = 1.0, sd_noise=(0.5, 1.0)) -> dict:
    """Statistical discrimination (Phelps 1972): an employer sees a test score s = q + e and pays expected
    productivity, E[q | s] = (1 - lam) mu_g + lam s with lam = sd_q^2 / (sd_q^2 + sd_e^2).  A noisier score for one
    group flattens its pay line: equal scores, unequal pay, though nobody's tastes enter."""
    s = np.asarray(signal, float)
    out = {}
    for g, (m, se) in enumerate(zip(mu, sd_noise)):
        lam = sd_q ** 2 / (sd_q ** 2 + se ** 2)
        out[g] = {"lam": lam, "pay": ((1 - lam) * m + lam * s).tolist()}
    return out


def oaxaca(y_a, X_a, y_b, X_b) -> dict:
    """The Oaxaca-Blinder decomposition of mean(y_a) - mean(y_b), with group b's coefficients as the reference:
    explained = (xbar_a - xbar_b) beta_b, unexplained = xbar_a (beta_a - beta_b).  X includes a constant."""
    ra, rb = ols(y_a, X_a), ols(y_b, X_b)
    ba, bb = np.array(ra["b"]), np.array(rb["b"])
    xa, xb = np.asarray(X_a, float).mean(0), np.asarray(X_b, float).mean(0)
    gap = float(np.mean(y_a) - np.mean(y_b))
    explained = float((xa - xb) @ bb)
    return {"gap": gap, "explained": explained, "unexplained": gap - explained,
            "by_variable": ((xa - xb) * bb).tolist(),
            "beta_a": ba.tolist(), "beta_b": bb.tolist()}


def within(y, X, ids) -> dict:
    """The fixed-effects (within) estimator: demean y and X by ``ids`` and run least squares (no constant); the
    standard errors are clustered by id."""
    y, X, ids = np.asarray(y, float), np.asarray(X, float), np.asarray(ids)
    u, inv = np.unique(ids, return_inverse=True)
    cnt = np.bincount(inv)

    def demean(v):
        return v - (np.bincount(inv, weights=v) / cnt)[inv]
    yd = demean(y)
    Xd = np.column_stack([demean(X[:, j]) for j in range(X.shape[1])])
    b = np.linalg.lstsq(Xd, yd, rcond=None)[0]
    e = yd - Xd @ b
    A = np.linalg.inv(Xd.T @ Xd)
    S = np.zeros((X.shape[1], X.shape[1]))
    for g in range(len(u)):
        sc = Xd[inv == g].T @ e[inv == g]
        S += np.outer(sc, sc)
    G, n, k = len(u), len(y), X.shape[1]
    V = A @ S @ A * G / (G - 1) * (n - 1) / (n - k - G)
    return {"b": b.tolist(), "se": np.sqrt(np.diag(V)).tolist(), "n": n, "groups": G}


# --- the child penalty: an event study around the first birth ---------------------------------------------------------
def child_penalty(n: int = 6000, penalty=(0.0, -0.30, -0.25, -0.22, -0.20), seed: int = 0) -> dict:
    """Simulated earnings of mothers and fathers from five years before to ten years after the first child, with
    common age and year profiles; mothers' earnings fall by the planted ``penalty`` path (years 0, 1, 2, 5, 10, linear
    between), fathers' do not.  The event study regresses log earnings on event-time dummies (year -1 omitted) with
    age and calendar-year controls, separately by sex, and reports the penalty as in Kleven, Landais and Sogaard:
    the gap between women's and men's event-time effects, relative to the counterfactual."""
    rng = np.random.default_rng(seed)
    ev = np.arange(-5, 11)
    knots_t, knots_v = [0, 1, 2, 5, 10], list(penalty)
    planted = np.where(ev < 0, 0.0, np.interp(ev, knots_t, knots_v))
    out = {"event": ev.tolist(), "planted": planted.tolist()}
    res = {}
    for sex in ("men", "women"):
        age0 = rng.integers(20, 41, n)                     # age at first birth
        year0 = rng.integers(1985, 2016, n)
        rows_y, rows_e, rows_age, rows_year = [], [], [], []
        person = rng.normal(0, 0.4, n)
        for i in range(n):
            age = age0[i] + ev
            yr = year0[i] + ev
            base = 10 + person[i] + 0.06 * (age - 25) - 0.0012 * (age - 25) ** 2 + 0.01 * (yr - 2000)
            eff = planted if sex == "women" else 0.0
            rows_y.append(base + eff + rng.normal(0, 0.15, ev.size))
            rows_e.append(ev)
            rows_age.append(age)
            rows_year.append(yr)
        y = np.concatenate(rows_y)
        e = np.concatenate(rows_e)
        age = np.concatenate(rows_age)
        yr = np.concatenate(rows_year)
        D = np.column_stack([(e == k).astype(float) for k in ev if k != -1])
        A = np.column_stack([(age == a).astype(float) for a in np.unique(age)[1:]])
        Y = np.column_stack([(yr == t).astype(float) for t in np.unique(yr)[1:]])
        X = np.column_stack([np.ones_like(y), D, A, Y])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        coefs = np.insert(b[1:1 + D.shape[1]], list(ev).index(-1), 0.0)
        res[sex] = coefs.tolist()
    out["men"], out["women"] = res["men"], res["women"]
    out["penalty"] = (np.array(res["women"]) - np.array(res["men"])).tolist()
    out["long_run"] = float(np.mean(out["penalty"][-5:]))
    return out


# --- robots across commuting zones (Acemoglu and Restrepo 2020) --------------------------------------------------------
ROBOT_INDUSTRIES = (("cars", 8.0), ("electronics", 3.0), ("metals", 3.0), ("plastics", 2.0), ("food", 0.5),
                    ("services", 0.0))


def robot_zones(n_zones: int = 300, beta: float = -0.20, manuf_trend: float = -3.0, noise: float = 0.5,
                industries=ROBOT_INDUSTRIES, seed: int = 0) -> dict:
    """Zones differ in their mix of industries; each industry adopts robots at its own national rate (robots per
    thousand workers), so a zone's exposure is its employment-weighted average.  The change in a zone's
    employment-to-population ratio (percentage points) is ``beta`` times exposure, plus a decline common to all
    manufacturing (``manuf_trend`` points per unit of manufacturing share: trade, offshoring) and noise.  Exposure
    and the manufacturing share are correlated, so a regression that omits the share overstates the robots' effect;
    controlling for it recovers ``beta``."""
    rng = np.random.default_rng(seed)
    names = [n for n, _ in industries]
    dr = np.array([d for _, d in industries])
    conc = np.array([0.6, 0.6, 0.8, 0.8, 1.0, 6.0])
    shares = rng.dirichlet(conc, n_zones)
    expo = shares @ dr
    manuf = shares[:, :5].sum(1)
    demp = beta * expo + manuf_trend * manuf + rng.normal(0, noise, n_zones)
    one = np.ones(n_zones)
    naive = ols(demp, np.column_stack([one, expo]))
    ctrl = ols(demp, np.column_stack([one, expo, manuf]))
    return {"names": names, "robots": dr.tolist(), "exposure": expo.tolist(), "manuf": manuf.tolist(),
            "demp": demp.tolist(), "naive": naive["b"][1], "naive_se": naive["se"][1], "ctrl": ctrl["b"][1],
            "ctrl_se": ctrl["se"][1], "beta": beta, "corr": float(np.corrcoef(expo, manuf)[0, 1])}
