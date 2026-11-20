"""Agora's long run (Part 19 of *Economics, Built*): a Malthusian economy, its natural experiments, and a toy version of
unified growth theory.

* :func:`income`, :func:`steady_state`, :func:`simulate`: income per head ``y = A (X / L)^beta`` on fixed land X, and a
  population that grows when income is above subsistence, ``L' / L = lam * ln(y / ybar)``; a plague (a share of the
  people die) and an invention (A rises) can be scheduled.  The steady state has ``y = ybar`` whatever A is: technology
  buys people, not income.
* :func:`vital_rates`: births and deaths per 1,000 as functions of income, crossing at subsistence (the diagram).
* :func:`wage_elasticity`: the slope of log real wages on log population for a span of years, by OLS with
  heteroskedasticity-robust (HC1) and Newey-West standard errors (the Malthusian "labour demand curve").
* :func:`education_choice` and :func:`unified`: Galor and Weil's (2000) household, which chooses how much to educate
  each child when technology changes at rate g (human capital ``h = (e + rho tau) / (e + rho tau + g)`` is eroded by
  change), and a toy economy in which technology grows with population and education (a scale effect, as in Kremer
  1993), fertility responds to income below a cap that education lowers: a Malthusian era, a post-Malthusian take-off,
  a demographic transition and modern growth, from one set of equations.
* :func:`spatial_noise`: Kelly's (2019) warning about persistence studies: regress one spatially smooth random field
  on another, independent one, across sites, and count how often ordinary standard errors call the slope significant.
* :func:`cagr`: compound annual growth between two values.

numpy only.
"""

from __future__ import annotations

import numpy as np


def cagr(v0: float, v1: float, years: float) -> float:
    return float((v1 / v0) ** (1.0 / years) - 1.0)


# ---------------------------------------------------------------------------------------------------------------
# the Malthusian economy

def income(L, A: float = 1.0, X: float = 1.0, beta: float = 0.5):
    """Income per head with land X fixed and diminishing returns to labour: ``A (X / L)^beta``."""
    return A * (X / np.asarray(L, float)) ** beta


def steady_state(A: float = 1.0, X: float = 1.0, beta: float = 0.5, ybar: float = 1.0) -> float:
    """The population at which income per head is at subsistence: ``L* = X (A / ybar)^(1 / beta)``."""
    return float(X * (A / ybar) ** (1.0 / beta))


def simulate(years: int = 300, L0: float = 1.0, A: float = 1.0, X: float = 1.0, beta: float = 0.5,
             ybar: float = 1.0, lam: float = 0.02, plague: tuple | None = None, invention: tuple | None = None,
             start: int = 0) -> dict:
    """Run the economy year by year.  ``plague=(year, share)`` kills that share of the people at the start of that
    year; ``invention=(year, gain)`` multiplies A by ``1 + gain`` from that year on.  Returns years, population,
    income per head and A."""
    L, a = float(L0), float(A)
    ys, Ls, inc, As = [], [], [], []
    for k in range(years + 1):
        yr = start + k
        if plague and yr == plague[0]:
            L *= 1.0 - plague[1]
        if invention and yr == invention[0]:
            a *= 1.0 + invention[1]
        y = float(income(L, a, X, beta))
        ys.append(yr)
        Ls.append(L)
        inc.append(y)
        As.append(a)
        L *= float(np.exp(lam * np.log(y / ybar)))
    return {"year": ys, "L": Ls, "y": inc, "A": As, "L_star": steady_state(a, X, beta, ybar)}


def vital_rates(y, ybar: float = 1.0, birth: float = 38.0, death: float = 38.0, b1: float = 6.0, d1: float = 14.0):
    """Births and deaths per 1,000 a year as functions of income per head: births rise slowly with income, deaths fall
    faster; they cross at subsistence."""
    ly = np.log(np.asarray(y, float) / ybar)
    return birth + b1 * ly, death - d1 * ly


def wage_elasticity(years, population, wages, first: int, last: int, lags: int = 10) -> dict:
    """OLS of ln(real wage) on ln(population) over [first, last], with HC1 and Newey-West (``lags``) standard errors
    for the slope."""
    yv = np.asarray(years)
    keep = (yv >= first) & (yv <= last) & np.isfinite(np.asarray(population, float)) & \
        np.isfinite(np.asarray(wages, float))
    x = np.log(np.asarray(population, float)[keep])
    y = np.log(np.asarray(wages, float)[keep])
    n = len(x)
    Xm = np.column_stack([np.ones(n), x])
    beta, *_ = np.linalg.lstsq(Xm, y, rcond=None)
    u = y - Xm @ beta
    XtXi = np.linalg.inv(Xm.T @ Xm)
    meat = (Xm * u[:, None]).T @ (Xm * u[:, None])
    hc1 = XtXi @ meat @ XtXi * n / (n - 2)
    S = meat.copy()
    for l in range(1, lags + 1):
        w = 1.0 - l / (lags + 1)
        G = (Xm[l:] * u[l:, None]).T @ (Xm[:-l] * u[:-l, None])
        S += w * (G + G.T)
    nw = XtXi @ S @ XtXi * n / (n - 2)
    r2 = 1.0 - float(u @ u) / float(((y - y.mean()) ** 2).sum())

    def nw_se(L):
        S_ = meat.copy()
        for l in range(1, L + 1):
            G_ = (Xm[l:] * u[l:, None]).T @ (Xm[:-l] * u[:-l, None])
            S_ += (1.0 - l / (L + 1)) * (G_ + G_.T)
        return float(np.sqrt((XtXi @ S_ @ XtXi * n / (n - 2))[1, 1]))
    rho1 = float(np.corrcoef(u[1:], u[:-1])[0, 1])
    return {"slope": float(beta[1]), "intercept": float(beta[0]), "se_hc1": float(np.sqrt(hc1[1, 1])),
            "se_nw": float(np.sqrt(nw[1, 1])), "r2": r2, "n": n, "first": first, "last": last,
            "residuals": u.tolist(), "years": yv[keep].tolist(), "rho1": rho1,
            "se_by_lag": {str(L): nw_se(L) for L in (0, 5, 10, 20, 40)}}


# ---------------------------------------------------------------------------------------------------------------
# unified growth: Galor and Weil's household, and a toy economy

def education_choice(g: float, tau: float = 0.15, rho: float = 0.5, grid: int = 4001) -> float:
    """The education per child that maximizes the human capital of the next generation per unit of child-rearing
    time, ``h(e, g) / (tau + e)`` with ``h = (e + rho tau) / (e + rho tau + g)``: zero while technology changes
    slowly, rising once g passes a threshold (change makes education pay)."""
    es = np.linspace(0.0, 1.0, grid)
    v = (es + rho * tau) / ((tau + es) * (es + rho * tau + g))
    return float(es[int(np.argmax(v))])


def threshold(tau: float = 0.15, rho: float = 0.5) -> float:
    """The rate of technological change above which parents begin to educate: where the derivative of
    ``ln h(e, g) - ln(tau + e)`` at e = 0 turns positive, ``g_hat = rho^2 tau / (1 - rho)``; found here numerically, on
    the same grid as :func:`education_choice`."""
    gs = np.linspace(0.0, 0.5, 5001)
    for g in gs:
        if education_choice(float(g), tau, rho, grid=8001) > 0:
            return float(g)
    return float("nan")


def unified(generations: int = 42, tau: float = 0.15, gamma: float = 0.2, kappa: float = 0.8, alpha: float = 0.6,
            rho: float = 0.5, phi: float = 0.075, a: float = 0.5, gmax: float = 1.0, start: int = 1000,
            years_per: int = 25) -> dict:
    """A toy unified growth economy, one step a generation.  Income per head ``y = (A / L)^alpha (h / h0)^(1 -
    alpha)``; children per adult ``n = min(y^kappa, gamma / (tau + e))`` (below the cap, a Malthusian response to
    income; at the cap, the time cost of children and their education binds); technology grows at
    ``g = min(gmax, phi (e + a) L)`` (more people, more ideas; educated people, more again); parents choose e from g.
    Returns each generation's year, population, technology, income, fertility, education and g, with the regimes
    marked: 'Malthusian' (education zero, income near subsistence), 'post-Malthusian' (income and population both
    rising), 'modern' (education positive and fertility falling to replacement)."""
    L, A, e = 1.0, 1.0, 0.0
    g = min(gmax, phi * a * L)
    h0 = rho * tau / (rho * tau + g)
    rows = []
    for t in range(generations):
        h = (e + rho * tau) / (e + rho * tau + g)
        y = (A / L) ** alpha * (h / h0) ** (1 - alpha)
        e_next = education_choice(g, tau, rho)
        n = min(y ** kappa, gamma / (tau + e_next))
        rows.append({"year": start + years_per * t, "L": L, "A": A, "y": y, "n": n, "e": e_next, "g": g})
        L, A = L * n, A * (1 + g)
        g = min(gmax, phi * (e_next + a) * L)
        e = e_next
    peak = int(np.argmax([r["n"] for r in rows]))
    for k, r in enumerate(rows):
        if r["e"] <= 1e-9 and r["y"] < 1.06:
            r["regime"] = "Malthusian"
        elif k <= peak:
            r["regime"] = "post-Malthusian"
        else:
            r["regime"] = "modern"
    return {"rows": rows, "peak_year": rows[peak]["year"], "peak_n": rows[peak]["n"],
            "takeoff_year": next(r["year"] for r in rows if r["regime"] != "Malthusian"),
            "params": {"tau": tau, "gamma": gamma, "kappa": kappa, "alpha": alpha, "rho": rho, "phi": phi, "a": a}}


def quantity_quality(gs=(0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8), tau: float = 0.15, gamma: float = 0.2,
                     rho: float = 0.5) -> list:
    """Becker and Lewis's trade-off in Galor and Weil's form: as technology changes faster, parents educate each child
    more and, since each child then costs more time, have fewer: ``n = gamma / (tau + e)``."""
    out = []
    for g in gs:
        e = education_choice(float(g), tau, rho)
        out.append({"g": float(g), "e": e, "n": gamma / (tau + e)})
    return out


# ---------------------------------------------------------------------------------------------------------------
# persistence regressions and spatial noise

def spatial_noise(n_sites: int = 300, length: float = 0.25, reps: int = 400, seed: int = 2019) -> dict:
    """Draw ``n_sites`` places uniformly in the unit square; for each repetition draw two independent Gaussian fields
    with exponential covariance ``exp(-d / length)`` and regress one on the other by OLS.  Returns the share of
    repetitions with |t| > 1.96 using ordinary (iid) standard errors (5% if the errors were independent), the same for
    a field with no spatial correlation, and the median |t|."""
    rng = np.random.default_rng(seed)
    xy = rng.uniform(0, 1, (n_sites, 2))
    d = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
    out = {}
    for name, ell in (("smooth", length), ("independent", 0.0)):
        if ell > 0:
            C = np.exp(-d / ell)
            Lc = np.linalg.cholesky(C + 1e-9 * np.eye(n_sites))
        ts = []
        for _ in range(reps):
            if ell > 0:
                x, y = Lc @ rng.standard_normal(n_sites), Lc @ rng.standard_normal(n_sites)
            else:
                x, y = rng.standard_normal(n_sites), rng.standard_normal(n_sites)
            X = np.column_stack([np.ones(n_sites), x])
            b, *_ = np.linalg.lstsq(X, y, rcond=None)
            u = y - X @ b
            s2 = float(u @ u) / (n_sites - 2)
            se = float(np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1]))
            ts.append(b[1] / se)
        ts = np.abs(np.array(ts))
        out[name] = {"reject": float((ts > 1.96).mean()), "median_t": float(np.median(ts))}
    return {**out, "n_sites": n_sites, "length": length, "reps": reps}
