"""The House's expected-return framework (Part 23): what risk is paid, and how much.

* Mean-variance: the frontier by Lagrange (Markowitz 1952; Merton 1972), the global minimum-variance and tangency
  portfolios, the maximum Sharpe ratio; two assets in closed form.
* The CAPM: betas, the security market line, and its slope against the market's premium.
* The stochastic discount factor: Hansen-Jagannathan bounds for excess and gross returns; the CRRA consumption SDF,
  its moments, the risk aversion an equity premium implies, and the Euler-equation moments for GMM.
* Shiller (1981): the ex post rational price; the Campbell-Shiller (1988) decomposition of the dividend yield's
  variance into return and dividend-growth news.
* Limits to arbitrage: Shleifer and Vishny's (1997) performance-based arbitrage; inelastic markets (Gabaix and
  Koijen 2021): the multiplier.
* Bubbles (Greenwood, Shleifer and You 2019): industry run-ups and the crashes that follow.

Returns are per period (monthly or quarterly) unless annualised explicitly; ``Sigma`` is a covariance matrix.
"""

from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# Mean-variance
# ---------------------------------------------------------------------------


def frontier_constants(mu, Sigma) -> dict:
    """Merton's (1972) constants: A = 1'S^-1 mu, B = mu'S^-1 mu, C = 1'S^-1 1, D = BC - A^2."""
    mu = np.asarray(mu, float)
    Si = np.linalg.inv(np.asarray(Sigma, float))
    one = np.ones(len(mu))
    A, B, C = one @ Si @ mu, mu @ Si @ mu, one @ Si @ one
    return {"A": float(A), "B": float(B), "C": float(C), "D": float(B * C - A * A), "Si": Si}


def frontier_sigma(m, mu, Sigma):
    """The smallest volatility of a fully invested portfolio with mean ``m``: sqrt((C m^2 - 2 A m + B)/D)."""
    k = frontier_constants(mu, Sigma)
    m = np.asarray(m, float)
    return np.sqrt((k["C"] * m * m - 2 * k["A"] * m + k["B"]) / k["D"])


def frontier_weights(m, mu, Sigma):
    """The frontier portfolio with mean ``m``: w = S^-1 (lam mu + gam 1), lam = (C m - A)/D, gam = (B - A m)/D."""
    k = frontier_constants(mu, Sigma)
    lam = (k["C"] * m - k["A"]) / k["D"]
    gam = (k["B"] - k["A"] * m) / k["D"]
    return k["Si"] @ (lam * np.asarray(mu, float) + gam * np.ones(len(mu)))


def gmv(Sigma) -> dict:
    """The global minimum-variance portfolio: w = S^-1 1 / C, variance 1/C."""
    Si = np.linalg.inv(np.asarray(Sigma, float))
    one = np.ones(Si.shape[0])
    C = one @ Si @ one
    return {"w": Si @ one / C, "var": float(1 / C)}


def tangency(mu, Sigma, rf=0.0) -> dict:
    """The tangency portfolio, w proportional to S^-1 (mu - rf), normalised to sum to one; and the maximum Sharpe ratio
    sqrt((mu - rf)' S^-1 (mu - rf)), which any combination of the assets and cash can reach (Tobin's separation)."""
    ex = np.asarray(mu, float) - rf
    z = np.linalg.solve(np.asarray(Sigma, float), ex)
    w = z / z.sum()
    return {"w": w, "mean": float(w @ np.asarray(mu, float)), "sd": float(np.sqrt(w @ np.asarray(Sigma) @ w)),
            "sharpe": float(np.sqrt(ex @ z))}


def two_asset_gmv(s1, s2, rho) -> dict:
    """Two assets: the minimum-variance weight on the first, (s2^2 - rho s1 s2)/(s1^2 + s2^2 - 2 rho s1 s2), and its
    volatility."""
    c = rho * s1 * s2
    den = s1 * s1 + s2 * s2 - 2 * c
    if abs(den) < 1e-15:  # perfectly correlated with equal volatility: every mix has the same risk
        return {"w1": 0.5, "sd": float(s1)}
    w = (s2 * s2 - c) / den
    v = w * w * s1 * s1 + (1 - w) ** 2 * s2 * s2 + 2 * w * (1 - w) * c
    return {"w1": float(w), "sd": float(np.sqrt(v))}


# ---------------------------------------------------------------------------
# The CAPM
# ---------------------------------------------------------------------------


def capm_betas(R_ex, m_ex) -> dict:
    """Time-series regressions of each asset's excess return on the market's: alphas, betas, and residual variances.
    ``R_ex`` [T, N]; ``m_ex`` [T]."""
    R = np.asarray(R_ex, float)
    m = np.asarray(m_ex, float)
    X = np.c_[np.ones(len(m)), m]
    coef, *_ = np.linalg.lstsq(X, R, rcond=None)
    resid = R - X @ coef
    return {"alpha": coef[0], "beta": coef[1], "resid_var": resid.var(0, ddof=2)}


def sml(betas, means) -> dict:
    """The cross-sectional line of average excess returns on betas: the CAPM says intercept 0 and slope equal to
    the market's average excess return."""
    b = np.asarray(betas, float)
    X = np.c_[np.ones(len(b)), b]
    coef, *_ = np.linalg.lstsq(X, np.asarray(means, float), rcond=None)
    return {"intercept": float(coef[0]), "slope": float(coef[1])}


# ---------------------------------------------------------------------------
# The stochastic discount factor
# ---------------------------------------------------------------------------


def hj_excess(mu_ex, Sigma_ex) -> float:
    """Hansen and Jagannathan (1991) with excess returns: any SDF that prices them has sigma(m)/E(m) >= the
    largest Sharpe ratio they can form, sqrt(mu' S^-1 mu)."""
    mu = np.asarray(mu_ex, float)
    return float(np.sqrt(mu @ np.linalg.solve(np.asarray(Sigma_ex, float), mu)))


def hj_gross(mu_gross, Sigma_gross, Em) -> np.ndarray:
    """The bound with gross returns, for each mean of the SDF ``Em``: the smallest sigma(m) among SDFs that price
    every return (E[mR] = 1): sigma^2 >= (1 - Em mu)' S^-1 (1 - Em mu)."""
    mu = np.asarray(mu_gross, float)
    Si = np.linalg.inv(np.asarray(Sigma_gross, float))
    out = []
    for e in np.atleast_1d(Em):
        g = np.ones(len(mu)) - e * mu
        out.append(np.sqrt(g @ Si @ g))
    return np.array(out)


def crra_sdf(growth, gamma, beta=1.0):
    """The consumption SDF of power utility: m = beta (C_{t+1}/C_t)^(-gamma); ``growth`` gross."""
    return beta * np.asarray(growth, float) ** (-gamma)


def sdf_ratio(growth, gamma, beta=1.0) -> float:
    """sigma(m)/E(m) for the CRRA SDF at risk aversion ``gamma``: what the HJ bound must be compared with."""
    m = crra_sdf(growth, gamma, beta)
    return float(m.std() / m.mean())


def implied_gamma(premium, cov_c_r) -> float:
    """Lognormal CCAPM: E[r - rf] + var(r)/2 = gamma cov(dc, r); here simply the premium over the covariance."""
    return float(premium / cov_c_r)


def euler_moments(growth, R_gross, Z=None):
    """The moment function for GMM: e_t(theta) = (beta g_{t+1}^{-gamma} R_{t+1} - 1) (x) z_t, theta = (beta, gamma).
    ``R_gross`` [T, N]; instruments ``Z`` [T, K] (a constant if None). Returns f(theta) -> [T, N*K]."""
    g = np.asarray(growth, float)
    R = np.atleast_2d(np.asarray(R_gross, float).T).T
    Z = np.ones((len(g), 1)) if Z is None else np.atleast_2d(np.asarray(Z, float).T).T

    def f(theta):
        b, gm = theta
        u = b * g[:, None] ** (-gm) * R - 1.0
        return np.concatenate([u * Z[:, [k]] for k in range(Z.shape[1])], axis=1)
    return f


# ---------------------------------------------------------------------------
# Excess volatility and the Campbell-Shiller identity
# ---------------------------------------------------------------------------


def ex_post_rational(div, r, terminal):
    """Shiller's p*: the present value, at a constant rate ``r`` per period, of the dividends that were actually
    paid, p*_t = (p*_{t+1} + d_{t+1})/(1 + r), started from ``terminal`` at the end of the sample."""
    d = np.asarray(div, float)
    p = np.empty(len(d))
    p[-1] = terminal
    for t in range(len(d) - 2, -1, -1):
        p[t] = (p[t + 1] + d[t + 1]) / (1 + r)
    return p


def cs_rho(dp_mean) -> float:
    """The Campbell-Shiller linearisation constant rho = 1/(1 + exp(mean log d/p))."""
    return float(1 / (1 + np.exp(dp_mean)))


def cs_decomposition(dp, r, dg, horizon=15) -> dict:
    """Campbell-Shiller (1988): dp_t ~ sum rho^j (r_{t+1+j} - dg_{t+1+j}) + const, so var(dp) splits into the
    coefficient of dp on discounted future returns, b_r, and on discounted future dividend growth, b_d, with
    b_r - b_d ~ 1. Estimated by direct long-horizon regressions (annual data). Returns b_r, b_d and rho."""
    dp, r, dg = (np.asarray(v, float) for v in (dp, r, dg))
    rho = cs_rho(dp.mean())
    T = len(dp)
    sr, sd = [], []
    for t in range(T - horizon):
        w = rho ** np.arange(horizon)
        sr.append(w @ r[t + 1:t + 1 + horizon])
        sd.append(w @ dg[t + 1:t + 1 + horizon])
    sr, sd = np.array(sr), np.array(sd)
    x = dp[:T - horizon] - dp[:T - horizon].mean()
    br = float(x @ (sr - sr.mean()) / (x @ x))
    bd = float(x @ (sd - sd.mean()) / (x @ x))
    return {"b_r": br, "b_d": bd, "rho": rho, "n": int(len(x))}


# ---------------------------------------------------------------------------
# Limits to arbitrage and inelastic markets
# ---------------------------------------------------------------------------


def shleifer_vishny(V=1.0, S1=0.2, S2=0.3, F1=0.1, a=1.0) -> dict:
    """Shleifer and Vishny (1997): noise traders push the price down by S_t; arbitrageurs with funds F_t buy. If
    their investors withdraw after losses (F2 = F1 + a F1 (p2/p1 - 1), a > 1 'performance-based'), then when the
    shock deepens the price falls further than the shock alone implies: p2 = (V - S2 + F1 (1 - a)) / (1 - a F1/p1)."""
    p1 = V - S1 + F1
    p2 = (V - S2 + F1 * (1 - a)) / (1 - a * F1 / p1)
    F2 = F1 + a * F1 * (p2 / p1 - 1)
    return {"p1": float(p1), "p2": float(p2), "F2": float(F2), "no_withdrawal_p2": float(V - S2 + F1)}


def gk_multiplier(zeta) -> float:
    """Gabaix and Koijen (2021): with a market-wide demand elasticity zeta, a flow of f percent of the market's value
    into equities moves prices by f/zeta percent; their estimate zeta of about 0.2 gives a multiplier of about 5."""
    return float(1 / zeta)


# ---------------------------------------------------------------------------
# Bubbles
# ---------------------------------------------------------------------------


def run_ups(R, Rm, months=24, threshold=1.0, crash=0.4, horizon=24) -> dict:
    """Greenwood, Shleifer and You (2019): an industry 'run-up' is a raw and market-adjusted return above
    ``threshold`` (100%) over ``months``; record each first episode, and whether the industry then fell by ``crash``
    (40%) from its peak within ``horizon`` months. ``R`` [T, N] monthly simple returns, ``Rm`` [T] the market's."""
    R = np.asarray(R, float)
    Rm = np.asarray(Rm, float)
    lr, lm = np.log1p(R), np.log1p(Rm)
    cr, cm = np.nancumsum(lr, 0), np.cumsum(lm)
    T, N = R.shape
    events = []
    for j in range(N):
        last = -10 ** 9
        for t in range(months, T - 1):
            raw = np.exp(cr[t, j] - cr[t - months, j]) - 1
            rel = np.exp((cr[t, j] - cr[t - months, j]) - (cm[t] - cm[t - months])) - 1
            if raw > threshold and rel > threshold and t - last > months:
                last = t
                level = np.exp(cr[t:t + horizon + 1, j] - cr[t, j])
                peak = np.maximum.accumulate(level)
                dd = 1 - level / peak
                fwd = float(np.exp(cr[min(t + horizon, T - 1), j] - cr[t, j]) - 1)
                events.append({"j": j, "t": t, "raw": float(raw), "rel": float(rel),
                               "crash": bool(dd.max() >= crash), "next": fwd})
    n = len(events)
    return {"events": events, "n": n, "p_crash": float(np.mean([e["crash"] for e in events])) if n else np.nan,
            "mean_next": float(np.mean([e["next"] for e in events])) if n else np.nan}
