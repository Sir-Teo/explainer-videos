"""Agora's households (Part 22 of *Economics, Built*): how much to spend today.

* :func:`keynes`: Keynes's consumption function ``C = a + b Y``; the average propensity falls with income.
* :func:`pih`: Friedman's permanent income: with interest r, consume the annuity value of assets plus the present value
  of expected income; a transitory windfall raises consumption by only ``r / (1 + r)`` of itself a year.
* :func:`life_cycle`: Modigliani's life cycle with a working life and retirement, consumption from the Euler equation
  ``c' = (beta R)^(1/gamma) c`` and the lifetime budget; the hump of assets.
* :func:`buffer_stock`: Carroll's (1997) buffer-stock problem, normalized by permanent income, solved by the endogenous
  grid method: CRRA utility, permanent and transitory shocks, a small chance of a zero-income spell; the consumption
  function c(m), its target cash-on-hand and its marginal propensity to consume.
* :func:`simulate_mpc`: a population of such households at their ergodic distribution, and the average MPC out of a
  windfall of a month's income.
* :func:`hand_to_mouth`: Kaplan, Violante and Weidner's poor and wealthy hand-to-mouth on simulated households.
* :func:`friedman_cross_section`: Friedman's errors-in-variables answer to Kuznets's puzzle.
* :func:`rule_of_thumb`: Campbell and Mankiw's (1989) economy, where a share lam of income goes to households who spend
  it and the rest follows the random walk; lam recovered by instrumental variables.

numpy only.
"""

from __future__ import annotations

import numpy as np


def keynes(Y, a: float = 10.0, b: float = 0.8) -> dict:
    Y = np.asarray(Y, float)
    C = a + b * Y
    return {"Y": Y.tolist(), "C": C.tolist(), "apc": (C / Y).tolist(), "mpc": b}


def pih(windfall: float = 1.0, r: float = 0.03, horizon: float | None = None) -> dict:
    """A one-off windfall's effect on consumption a year: the annuity ``r/(1+r) w`` with an infinite horizon, or
    ``w r / (1 - (1+r)^-T)`` (times 1/(1+r)) over T years; and a permanent rise of the same size, spent in full."""
    if horizon is None:
        per_year = r / (1 + r) * windfall
    else:
        per_year = windfall * r / (1 + r) / (1 - (1 + r) ** -horizon)
    return {"windfall": windfall, "per_year": per_year, "share": per_year / windfall, "permanent": windfall}


def life_cycle(work: int = 40, retire: int = 20, income: float = 1.0, R: float = 1.02, beta: float = 1 / 1.02,
               gamma: float = 2.0, hump: bool = True) -> dict:
    """Consumption and assets from age 25: earnings (hump-shaped if ``hump``) for ``work`` years, then nothing for
    ``retire`` years; consumption grows at ``(beta R)^(1/gamma)`` and exhausts lifetime wealth."""
    T = work + retire
    t = np.arange(T)
    if hump:
        y = np.where(t < work, income * (0.7 + 0.6 * np.sin(np.pi * np.clip(t, 0, work) / work) ** 1.0), 0.0)
    else:
        y = np.where(t < work, income, 0.0)
    disc = R ** -t
    growth = (beta * R) ** (1 / gamma)
    path = growth ** t
    c0 = float(np.sum(y * disc) / np.sum(path * disc))
    c = c0 * path
    a = np.zeros(T + 1)
    for k in range(T):
        a[k + 1] = R * (a[k] + y[k] - c[k])
    return {"age": (25 + t).tolist(), "income": y.tolist(), "consumption": c.tolist(), "assets": a[:-1].tolist(),
            "peak_age": int(25 + int(np.argmax(a[:-1]))), "end_assets": float(a[-1])}


def _shocks(perm_sd: float, tran_sd: float, p_zero: float, n: int = 7):
    """Discrete equiprobable lognormal shocks with mean one (Gauss-Hermite would do as well), and a zero-income event
    with probability p_zero for the transitory shock."""
    q = (np.arange(n) + 0.5) / n
    from math import sqrt

    def lognorm(sd):
        if sd == 0:
            return np.ones(1), np.ones(1)
        z = np.sqrt(2) * _erfinv(2 * q - 1)
        x = np.exp(sd * z - sd ** 2 / 2)
        return x / x.mean(), np.full(n, 1 / n)
    psi, wp = lognorm(perm_sd)
    th, wt = lognorm(tran_sd)
    th = th / (1 - p_zero)          # keep the mean at one
    th = np.concatenate([[0.0], th]) if p_zero > 0 else th
    wt = np.concatenate([[p_zero], wt * (1 - p_zero)]) if p_zero > 0 else wt
    del sqrt
    return psi, wp, th, wt


def _erfinv(y):
    # Giles's single-precision approximation, refined by two Newton steps
    y = np.asarray(y, float)
    w = -np.log((1.0 - y) * (1.0 + y))
    x = np.where(w < 5.0,
                 np.polyval([2.81022636e-08, 3.43273939e-07, -3.5233877e-06, -4.39150654e-06, 0.00021858087,
                             -0.00125372503, -0.00417768164, 0.246640727, 1.50140941], w - 2.5) * y,
                 np.polyval([-0.000200214257, 0.000100950558, 0.00134934322, -0.00367342844, 0.00573950773,
                             -0.0076224613, 0.00943887047, 1.00167406, 2.83297682], np.sqrt(w) - 3.0) * y)
    from math import erf, pi
    for _ in range(2):
        err = np.vectorize(erf)(x) - y
        x = x - err / (2 / np.sqrt(pi) * np.exp(-x * x))
    return x


def buffer_stock(beta: float = 0.96, R: float = 1.03, gamma: float = 2.0, G: float = 1.02, perm_sd: float = 0.1,
                 tran_sd: float = 0.1, p_zero: float = 0.005, n_a: int = 200, a_max: float = 20.0,
                 tol: float = 1e-8, max_iter: int = 2000) -> dict:
    """Carroll's buffer-stock problem in cash-on-hand per unit of permanent income, m.  Each period the household
    consumes c and carries ``a = m - c`` (no borrowing); next period ``m' = R a / (G psi') + theta'``.  The Euler
    equation ``c^-gamma = beta R E[(G psi' c(m'))^-gamma]`` is solved by the endogenous grid method: fix a grid of a,
    compute the right side, invert for c, and set m = a + c.  Returns c(m) on a grid, the target m* where E[m'] = m,
    and the MPC c'(m)."""
    psi, wp, th, wt = _shocks(perm_sd, tran_sd, p_zero)
    a_grid = np.concatenate([[0.0], np.exp(np.linspace(np.log(1e-4), np.log(a_max), n_a - 1))])
    # start: consume everything (the last period of life)
    m_grid = a_grid.copy() + 1e-6
    c_grid = m_grid.copy()
    for it in range(max_iter):
        m_old, c_old = m_grid, c_grid
        rhs = np.zeros_like(a_grid)
        for p_, w_p in zip(psi, wp):
            for t_, w_t in zip(th, wt):
                m_next = R * a_grid / (G * p_) + t_
                c_next = np.interp(m_next, m_old, c_old, left=None, right=None)
                # beyond the grid, extrapolate linearly
                hi = m_next > m_old[-1]
                if hi.any():
                    slope = (c_old[-1] - c_old[-2]) / (m_old[-1] - m_old[-2])
                    c_next[hi] = c_old[-1] + slope * (m_next[hi] - m_old[-1])
                c_next = np.maximum(c_next, 1e-10)
                rhs += w_p * w_t * (G * p_ * c_next) ** -gamma
        c_new = (beta * R * rhs) ** (-1 / gamma)
        m_new = a_grid + c_new
        # the constrained region: below the first point, consume everything
        m_grid = np.concatenate([[0.0], m_new])
        c_grid = np.concatenate([[0.0], c_new])
        if it > 5 and np.max(np.abs(np.interp(m_old, m_grid, c_grid) - c_old)) < tol:
            break
    m = np.linspace(0.0, 6.0, 601)
    c = np.interp(m, m_grid, c_grid)
    mpc = np.gradient(c, m)
    # the target: E[m'] = m, with E[m'] = R (m - c) / G E[1/psi] + 1
    einv = float(np.sum(wp / psi))
    expected_next = R * (m - c) / G * einv + 1.0
    k = int(np.argmin(np.abs(expected_next - m)[1:])) + 1
    return {"m": m.tolist(), "c": c.tolist(), "mpc": mpc.tolist(), "target": float(m[k]), "c_target": float(c[k]),
            "iterations": it + 1, "m_grid": m_grid.tolist(), "c_grid": c_grid.tolist(),
            "params": {"beta": beta, "R": R, "gamma": gamma, "G": G, "perm_sd": perm_sd, "tran_sd": tran_sd,
                       "p_zero": p_zero},
            "impatience": float((R * beta) ** (1 / gamma) / G)}


def ergodic(bs: dict, n: int = 20000, periods: int = 400, seed: int = 0) -> np.ndarray:
    """Cash-on-hand m (per unit of permanent income) of n households drawing the shocks of :func:`buffer_stock`, run
    for ``periods`` years from m = 1: a draw from the ergodic distribution."""
    p = bs["params"]
    psi, wp, th, wt = _shocks(p["perm_sd"], p["tran_sd"], p["p_zero"])
    rng = np.random.default_rng(seed)
    mg, cg = np.array(bs["m_grid"]), np.array(bs["c_grid"])
    m = np.ones(n)
    for _ in range(periods):
        a = m - np.interp(m, mg, cg)
        ps = rng.choice(psi, size=n, p=wp)
        ts = rng.choice(th, size=n, p=wt)
        m = p["R"] * a / (p["G"] * ps) + ts
    return m


def mpc_of(bs: dict, m, windfall: float = 1 / 12) -> np.ndarray:
    """``(c(m + w) - c(m)) / w``: the share of a windfall w spent within the period."""
    mg, cg = np.array(bs["m_grid"]), np.array(bs["c_grid"])
    m = np.asarray(m, float)
    return (np.interp(m + windfall, mg, cg) - np.interp(m, mg, cg)) / windfall


def simulate_mpc(bs: dict, n: int = 20000, periods: int = 400, windfall: float = 1 / 12, seed: int = 0) -> dict:
    """Households drawing the same shocks as :func:`buffer_stock`, run to their ergodic distribution of m; the average
    of ``(c(m + w) - c(m)) / w`` for a windfall w (a month's income is 1/12 of a year's permanent income), and the
    share of households with less than a month of income left in cash after spending."""
    m = ergodic(bs, n, periods, seed)
    mg, cg = np.array(bs["m_grid"]), np.array(bs["c_grid"])
    mpc = mpc_of(bs, m, windfall)
    qs = np.percentile(m, np.arange(0, 101, 10))
    return {"mean_mpc": float(mpc.mean()), "median_m": float(np.median(m)),
            "mpc_by_decile": [float(mpc[(m >= lo) & (m <= hi)].mean()) for lo, hi in zip(qs[:-1], qs[1:])],
            "m_sample": np.sort(m)[:: max(1, n // 2000)].tolist(),
            "share_low": float(np.mean(m - np.interp(m, mg, cg) < 1 / 12))}


def hand_to_mouth(bs_renter: dict, bs_owner: dict, n: int = 20000, windfall: float = 1 / 12, own: float = 0.6,
                  median: float = 3.0, sd: float = 0.6, short: float = 0.25, seed: int = 0) -> dict:
    """The wealthy hand-to-mouth (Kaplan and Violante 2014; Kaplan, Violante and Weidner 2014), in a one-asset
    shortcut.  A share ``own`` of households hold illiquid wealth (a house, a pension; lognormal, the given median in
    years of income) that earns more than cash.  Each dollar they keep in cash forgoes that return, so on their cash
    they behave like a less patient household: ``bs_owner`` is the buffer-stock solution with ``beta R / R_h`` in
    place of ``beta``.  Renters solve ``bs_renter``.  The MPC out of a windfall then depends on liquid wealth, not net
    worth: owners, much richer, spend windfalls faster.  ``short`` is the liquid wealth (in years of income) below which
    a household counts as short of cash."""
    rng = np.random.default_rng(seed + 1)
    owns = rng.random(n) < own
    m = np.where(owns, ergodic(bs_owner, n, seed=seed), ergodic(bs_renter, n, seed=seed + 2))
    c = np.where(owns, np.interp(m, bs_owner["m_grid"], bs_owner["c_grid"]),
                 np.interp(m, bs_renter["m_grid"], bs_renter["c_grid"]))
    liquid = m - c
    illiquid = np.where(owns, median * np.exp(sd * rng.standard_normal(n)), 0.0)
    mpc = np.where(owns, mpc_of(bs_owner, m, windfall), mpc_of(bs_renter, m, windfall))
    net = liquid + illiquid
    low = liquid < short
    k = max(1, n // 1500)
    order = rng.permutation(n)[::k]
    return {"mpc_owners": float(mpc[owns].mean()), "mpc_renters": float(mpc[~owns].mean()), "mpc_all": float(mpc.mean()),
            "net_owners": float(np.median(net[owns])), "net_renters": float(np.median(net[~owns])),
            "liquid_owners": float(np.median(liquid[owns])), "liquid_renters": float(np.median(liquid[~owns])),
            "short_owners": float(low[owns].mean()), "short_renters": float(low[~owns].mean()),
            "mpc_short": float(mpc[low].mean()), "mpc_not_short": float(mpc[~low].mean()),
            "corr_liquid": float(np.corrcoef(np.log(liquid + 0.01), mpc)[0, 1]),
            "corr_net": float(np.corrcoef(np.log(net + 0.01), mpc)[0, 1]),
            "sample": {"net": net[order].tolist(), "liquid": liquid[order].tolist(), "mpc": mpc[order].tolist(),
                       "owns": owns[order].astype(int).tolist()}}


def friedman_cross_section(n: int = 10000, sd_perm: float = 0.5, sd_tran: float = 0.3, share: float = 0.9,
                           growth: float = 0.02, years: int = 60, seed: int = 0) -> dict:
    """Friedman's answer to Kuznets: every household consumes ``share`` of its permanent income, but measured income
    adds a transitory part.  Across households in one year, consumption regressed on measured income has a slope
    below ``share`` and a positive intercept (Keynes's function), and the average propensity falls with measured
    income; over time, as every permanent income grows, aggregate C/Y stays at ``share`` (Kuznets's long series).  In
    logs the cross-section slope is ``var(p) / (var(p) + var(t))``."""
    rng = np.random.default_rng(seed)
    p = rng.normal(0.0, sd_perm, n)
    t = rng.normal(-sd_tran ** 2 / 2, sd_tran, n)
    Y = np.exp(p + t)
    C = share * np.exp(p)
    b, a = np.polyfit(Y, C, 1)
    elast = float(np.polyfit(np.log(Y), np.log(C), 1)[0])
    qs = np.percentile(Y, np.arange(0, 101, 10))
    apc = [float(C[(Y >= lo) & (Y <= hi)].sum() / Y[(Y >= lo) & (Y <= hi)].sum()) for lo, hi in zip(qs[:-1], qs[1:])]
    mid = [float(np.median(Y[(Y >= lo) & (Y <= hi)])) for lo, hi in zip(qs[:-1], qs[1:])]
    # over time: aggregate C and Y, with fresh transitory draws each year
    agg = []
    for k in range(years + 1):
        tk = rng.normal(-sd_tran ** 2 / 2, sd_tran, n)
        g = (1 + growth) ** k
        agg.append((float(share * g * np.exp(p).sum()), float(g * np.exp(p + tk).sum())))
    order = rng.permutation(n)[:1500]
    return {"slope": float(b), "intercept": float(a), "elasticity": elast,
            "elasticity_theory": sd_perm ** 2 / (sd_perm ** 2 + sd_tran ** 2), "apc_by_decile": apc,
            "income_by_decile": mid, "apc_mean": float(C.sum() / Y.sum()),
            "years": list(range(years + 1)), "C": [c for c, _ in agg], "Y": [y for _, y in agg],
            "apc_time": [c / y for c, y in agg], "sample_Y": Y[order].tolist(), "sample_C": C[order].tolist()}


def rule_of_thumb(lam: float = 0.4, T: int = 240, mu: float = 0.005, phi: float = 0.5, sd: float = 0.01,
                  seed: int = 0) -> dict:
    """Aggregate log income growth ``dy_t = mu + phi (dy_{t-1} - mu) + e_t`` (predictable); a share lam of income goes
    to households who spend it, the rest to permanent-income households whose consumption follows a random walk with
    drift.  Consumption growth is ``dc_t = lam dy_t + (1 - lam) (mu + u_t)``.  OLS of dc on dy is biased by the
    correlation of e and u; instrumenting dy with dy_{t-2}, which forecasts it, recovers lam (Campbell and Mankiw)."""
    rng = np.random.default_rng(seed)
    dy = np.zeros(T)
    e = rng.normal(0, sd, T)
    for t in range(1, T):
        dy[t] = mu + phi * (dy[t - 1] - mu) + e[t]
    u = 0.6 * e + rng.normal(0, sd * 0.5, T)      # news about permanent income moves the forward-looking households
    dc = lam * dy + (1 - lam) * (mu + u)
    y_, x_, z_ = dc[3:], dy[3:], dy[1:-2]
    ols = float(np.polyfit(x_, y_, 1)[0])
    zc = z_ - z_.mean()
    iv = float(np.sum(zc * (y_ - y_.mean())) / np.sum(zc * (x_ - x_.mean())))
    first = float(np.polyfit(z_, x_, 1)[0])
    return {"lam": lam, "ols": ols, "iv": iv, "first_stage": first, "sd_dc": float(np.std(dc)),
            "sd_dy": float(np.std(dy)), "T": T}
