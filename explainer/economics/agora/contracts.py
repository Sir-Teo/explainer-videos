"""Incentives when actions are hidden (Part 14): teams, the principal-agent problem, multitasking, tournaments,
efficiency wages, sharecropping and the ratchet.

**Teams.**  :func:`team` (Alchian and Demsetz 1972; Holmström 1982: n members share output equally, each chooses
effort; equilibrium effort against the efficient level, and the loss).

**The principal-agent problem.**  :func:`linear_agency` (Holmström and Milgrom 1987: output y = e + noise, a linear
wage alpha + beta y, a CARA agent with quadratic effort cost; the optimal share beta* = 1/(1 + r c sigma^2), effort,
the risk premium and the total surplus, against first best), :func:`share_curve` (beta* against noise and risk
aversion), :func:`two_outcome` (the discrete model: two effort levels, two outputs, the cheapest wage pair that meets
participation and incentive compatibility for a risk-averse agent with log utility), :func:`relative_performance`
(Holmström 1979's informativeness principle: pay on a second signal correlated with the noise, and the optimal
weight).

**Multitasking.**  :func:`multitask` (Holmström and Milgrom 1991: two tasks whose efforts are substitutes in cost,
only one measured; effort on each against the share paid on the measured one).

**Tournaments and careers.**  :func:`tournament` (Lazear and Rosen 1981: two workers, a prize spread, normal noise;
equilibrium effort against the spread), :func:`ratchet` (Weitzman 1980: next year's target set from this year's
output; effort with and without the ratchet).

**Efficiency wages.**  :func:`shapiro_stiglitz` (the no-shirking condition against labour demand: the equilibrium
wage and unemployment).

**Sharecropping.**  :func:`sharecrop` (a tenant's effort under a wage, a fixed rent and a crop share; the landlord's
best share when the tenant is risk averse and cannot bear a large loss).

Plain numpy and scipy.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, minimize_scalar


def team(n: int, a: float = 1.0, c: float = 1.0) -> dict:
    """n members each choose effort e_i at cost c e_i^2 / 2; output is a * sum(e) and is shared equally.  Each member
    gets a/n per unit of their own effort, so e = a/(n c); the efficient effort is a/c.  Surplus per member: a e - c e^2/2."""
    e_eq = a / (n * c)
    e_eff = a / c
    s_eq = a * e_eq - c * e_eq ** 2 / 2
    s_eff = a * e_eff - c * e_eff ** 2 / 2
    return {"n": n, "e_eq": float(e_eq), "e_eff": float(e_eff), "share": 1 / n, "surplus_eq": float(s_eq),
            "surplus_eff": float(s_eff), "lost": float(1 - s_eq / s_eff)}


def linear_agency(r: float = 2.0, c: float = 1.0, sigma: float = 0.5, value: float = 1.0, beta=None) -> dict:
    """Holmström and Milgrom's linear model: output y = e + eps, eps ~ N(0, sigma^2), each unit worth ``value`` to the
    principal; the agent has CARA utility with coefficient r and effort cost c e^2 / 2, and is paid alpha + beta y.
    The agent chooses e = beta value-free: e = beta / c.  Certainty equivalent: alpha + beta e - c e^2/2 -
    r beta^2 sigma^2 / 2.  With alpha set to meet the agent's outside option (0), the total surplus is
    value e - c e^2/2 - r beta^2 sigma^2/2, maximized at beta* = value / (1 + r c sigma^2)."""
    b_star = value / (1 + r * c * sigma ** 2)
    b = b_star if beta is None else beta
    e = b / c
    risk = r * b ** 2 * sigma ** 2 / 2
    surplus = value * e - c * e ** 2 / 2 - risk
    fb_e = value / c
    fb = value * fb_e - c * fb_e ** 2 / 2
    return {"beta_star": float(b_star), "beta": float(b), "effort": float(e), "risk_premium": float(risk),
            "surplus": float(surplus), "first_best_effort": float(fb_e), "first_best_surplus": float(fb),
            "agency_cost": float(fb - surplus)}


def share_curve(sigmas, rs=(0.5, 2.0, 8.0), c: float = 1.0) -> dict:
    """beta* = 1/(1 + r c sigma^2) for each risk aversion in ``rs`` against the noise sigma."""
    s = np.asarray(sigmas, float)
    return {"sigma": s, "curves": {r: 1 / (1 + r * c * s ** 2) for r in rs}}


def two_outcome(p_high: float = 0.8, p_low: float = 0.4, y_high: float = 100.0, y_low: float = 40.0,
                effort_cost: float = 0.3, reservation: float = 2.0) -> dict:
    """The discrete principal-agent problem with log utility: hard work costs ``effort_cost`` utils and makes the good
    outcome likely with p_high instead of p_low.  The principal pays w_H after a good outcome and w_L after a bad one.
    To get hard work it must meet participation, p_high ln w_H + (1 - p_high) ln w_L - cost >= reservation, and
    incentive compatibility, (p_high - p_low)(ln w_H - ln w_L) >= cost.  Both bind at the optimum, so
    ln w_L = reservation + cost - p_high cost / (p_high - p_low) and ln w_H = ln w_L + cost / (p_high - p_low).
    Compared with the flat wage that gets easy work, exp(reservation)."""
    d = effort_cost / (p_high - p_low)
    ln_wl = reservation + effort_cost - p_high * d
    ln_wh = ln_wl + d
    wl, wh = np.exp(ln_wl), np.exp(ln_wh)
    cost_hard = p_high * wh + (1 - p_high) * wl
    # first best: observable effort, a flat wage that pays for the effort
    fb_wage = np.exp(reservation + effort_cost)
    flat_easy = np.exp(reservation)
    out_hard = p_high * y_high + (1 - p_high) * y_low
    out_easy = p_low * y_high + (1 - p_low) * y_low
    return {"w_high": float(wh), "w_low": float(wl), "cost_hard": float(cost_hard), "fb_wage": float(fb_wage),
            "risk_cost": float(cost_hard - fb_wage), "flat_easy": float(flat_easy),
            "profit_hard": float(out_hard - cost_hard), "profit_easy": float(out_easy - flat_easy),
            "profit_fb": float(out_hard - fb_wage), "induce_hard": bool(out_hard - cost_hard > out_easy - flat_easy)}


def relative_performance(r: float = 2.0, c: float = 1.0, sigma_common: float = 0.4, sigma_own: float = 0.3) -> dict:
    """Output y = e + m + u, where m is a shock common to everyone (the weather, the market) and u the agent's own;
    the principal also sees z = m + v, a rival's or the industry's result (here v = 0 for a perfect reading of m, so
    z = m).  Paying on y - z removes m: the contract's noise falls from sigma_common^2 + sigma_own^2 to sigma_own^2,
    and the optimal share rises.  Holmström (1979): pay on every signal that tells you about effort, and only those."""
    var_y = sigma_common ** 2 + sigma_own ** 2
    b_y = 1 / (1 + r * c * var_y)
    b_rel = 1 / (1 + r * c * sigma_own ** 2)
    s_y = linear_agency(r, c, np.sqrt(var_y))["surplus"]
    s_rel = linear_agency(r, c, sigma_own)["surplus"]
    return {"beta_own": float(b_y), "beta_relative": float(b_rel), "surplus_own": float(s_y),
            "surplus_relative": float(s_rel), "var_own": float(var_y), "var_relative": float(sigma_own ** 2)}


def multitask(substitutability: float = 0.5, c: float = 1.0, base: float = 1.0, betas=None) -> dict:
    """Two tasks; effort cost c (e1^2 + e2^2 + 2 s e1 e2)/2 with s the substitutability (0: independent, near 1: the
    same hours); the agent also does task 2 out of habit or pride, as if paid ``base`` per unit up to... modelled as a
    constant marginal benefit ``base`` on each task (intrinsic motivation), and is paid beta per unit of task 1 only.
    First-order conditions: c (e1 + s e2) = base + beta, c (e2 + s e1) = base.  Returns both efforts against beta: as
    beta rises, task-1 effort rises and task-2 effort falls."""
    bs = np.linspace(0, 2, 81) if betas is None else np.asarray(betas, float)
    s = substitutability
    A = c * np.array([[1, s], [s, 1]])
    e1, e2 = [], []
    for b in bs:
        x = np.linalg.solve(A, np.array([base + b, base]))
        if x[1] < 0:                       # a corner: task 2 is dropped, and task 1 alone meets its condition
            x = np.array([(base + b) / c, 0.0])
        e1.append(float(x[0]))
        e2.append(float(x[1]))
    return {"beta": bs, "e1": np.array(e1), "e2": np.array(e2), "s": s}


def tournament(spread, sigma: float = 1.0, c: float = 1.0) -> dict:
    """Lazear and Rosen: two workers, output e_i + eps_i with eps ~ N(0, sigma^2); the winner gets the higher of two
    prizes.  The chance of winning rises with own effort at rate g(0), the density of eps_i - eps_j at zero, 1/(2 sigma
    sqrt(pi)), so each chooses e with c e = spread g(0): effort is proportional to the spread, and falls with noise.
    Returns effort for each spread."""
    sp = np.asarray(spread, float)
    g0 = 1 / (2 * sigma * np.sqrt(np.pi))
    return {"spread": sp, "effort": sp * g0 / c, "g0": float(g0)}


def ratchet(theta: float = 1.0, c: float = 1.0, delta: float = 0.9, bonus: float = 1.0) -> dict:
    """Weitzman's ratchet: a manager is paid a bonus per unit above a target; with a ratchet, next year's target is
    raised one for one with this year's output, so each extra unit today raises tomorrow's target by one and costs
    delta bonus tomorrow.  Without the ratchet effort is bonus / c; with it, (1 - delta) bonus / c."""
    e_free = bonus / c
    e_ratchet = (1 - delta) * bonus / c
    return {"effort_fixed_target": float(e_free), "effort_ratchet": float(e_ratchet), "delta": delta}


def shapiro_stiglitz(effort_cost: float = 1.0, detect: float = 0.5, quit_rate: float = 0.1, discount: float = 0.05,
                     labour: float = 100.0, demand_a: float = 6.0, demand_b: float = 0.04) -> dict:
    """Shapiro and Stiglitz (1984): a worker who shirks is caught with chance ``detect`` per period and fired; jobs
    end anyway at ``quit_rate``; unemployed workers find jobs at a rate a set by the flows.  The no-shirking wage is
    w = e + (e / q)(r + b / u), where u is the unemployment rate, b the separation rate, r the discount rate: the
    fewer the unemployed, the more a job must pay for its loss to be feared.  Labour demand: w = demand_a - demand_b L.
    Returns the no-shirking curve and the equilibrium wage, employment and unemployment rate."""
    Ls = np.linspace(1, labour - 1, 400)
    u = 1 - Ls / labour
    nsc = effort_cost + (effort_cost / detect) * (discount + quit_rate / u)
    dem = demand_a - demand_b * Ls
    f = lambda L: (effort_cost + (effort_cost / detect) * (discount + quit_rate / (1 - L / labour))) - (demand_a -
                                                                                                    demand_b * L)
    L_eq = float(brentq(f, 1, labour - 1e-6))
    w_eq = float(demand_a - demand_b * L_eq)
    return {"L": Ls, "nsc": nsc, "demand": dem, "L_eq": L_eq, "w_eq": w_eq, "u_eq": float(1 - L_eq / labour),
            "labour": labour, "full_employment_wage": float(demand_a - demand_b * labour)}


def sharecrop(a: float = 10.0, c: float = 1.0, r: float = 1.0, sigma: float = 8.0) -> dict:
    """A tenant farms land with output a e + noise (sd sigma) and effort cost c e^2 / 2, and keeps a share s of the
    crop (s = 0: a wage labourer; s = 1: a fixed rent).  With CARA risk aversion r, effort is s a / c and the
    tenant's risk premium r s^2 sigma^2 / 2.  The surplus-maximizing share s* = 1 / (1 + r c sigma^2 / a^2) is between
    the two: Marshall's inefficiency of sharecropping is the price of insuring the tenant (Stiglitz 1974)."""
    ss = np.linspace(0, 1, 101)
    e = ss * a / c
    surplus = a * e - c * e ** 2 / 2 - r * ss ** 2 * sigma ** 2 / 2
    s_star = 1 / (1 + r * c * sigma ** 2 / a ** 2)
    k = int(np.argmax(surplus))
    return {"s": ss, "effort": e, "surplus": surplus, "s_star": float(s_star), "s_grid_best": float(ss[k]),
            "surplus_wage": float(surplus[0]), "surplus_rent": float(surplus[-1]), "surplus_best": float(surplus[k])}
