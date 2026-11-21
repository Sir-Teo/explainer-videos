"""The core examination of Part 56: twelve problems of the kind every first-year PhD programme sets, four each in
micro, macro and econometrics, each solved twice: by the formula a candidate writes down, and by brute force (a grid,
a simulation, an optimizer), so the two can be checked against each other.

Micro: a consumer with a kinked budget (``kinked_budget``); an exchange economy with an externality
(``externality_box``); a first-price auction with a reserve (``reserve_auction``); a screening contract for two types
and a continuum (``screening``).  Macro: the Ramsey model with a tax on capital (``ramsey_tax``); a McCall worker
whose benefits expire (``mccall_expiring``); the three-equation model under discretion (``discretion``); an Aiyagari
household's interest rate (``aiyagari_gap``, over Part 52's ``hetero``).  Econometrics: a supply-and-demand system
and the Wald estimator (``supply_demand``); GMM for an Euler equation (``euler_gmm``, over Part 54's ``estimate``);
two-way fixed effects with staggered timing (``staggered_did``, over statkit's ``quasi``); a VAR with a long-run
restriction (``long_run_var``, over Part 55's ``macrometrics``).

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, minimize

# ---------------------------------------------------------------------------------------------------------------
# Micro 1: a consumer with a kinked budget


def kinked_budget(alpha: float = 0.4, m: float = 100.0, p1: float = 1.0, p2: float = 2.0, xbar: float = 20.0,
                  p2_new: float = 2.5) -> dict:
    """u = alpha ln x + (1 - alpha) ln y, with y the numeraire.  Good x costs p1 for the first ``xbar`` units and p2
    beyond (an increasing block tariff), so the budget is kinked at xbar.  On the second segment the consumer acts
    as if facing a straight budget at price p2 with virtual income m + (p2 - p1) xbar.

    Returns the demand (by segments, and by a brute-force search along the kinked budget), the Slutsky decomposition
    of a rise in p2 at the margin (the income effect falls only on the x - xbar units bought at p2), the change in
    demand when p2 rises to ``p2_new``, and its compensating variation against the Laspeyres approximation."""

    def demand(p2_, m_):
        x1 = alpha * m_ / p1
        if x1 <= xbar:
            return x1, "first segment"
        x2 = alpha * (m_ + (p2_ - p1) * xbar) / p2_
        if x2 >= xbar:
            return x2, "second segment"
        return xbar, "the kink"

    def cost(x, p2_):
        return p1 * np.minimum(x, xbar) + p2_ * np.maximum(x - xbar, 0.0)

    def util(p2_, m_):
        x_, _ = demand(p2_, m_)
        return alpha * np.log(x_) + (1 - alpha) * np.log(m_ - float(cost(x_, p2_)))

    xs = np.linspace(0.01, m / p1 - 0.01, 400001)
    y_ = m - cost(xs, p2)
    u_ = np.where(y_ > 0, alpha * np.log(xs) + (1 - alpha) * np.log(np.where(y_ > 0, y_, 1.0)), -np.inf)
    xb = float(xs[int(np.argmax(u_))])
    x, where = demand(p2, m)
    assert abs(x - xb) < 1e-3, (x, xb)
    y = m - float(cost(x, p2))
    mv = m + (p2 - p1) * xbar
    out = {"x": x, "y": y, "where": where, "x_brute": xb, "virtual_income": mv, "mrs": alpha / (1 - alpha) * y / x,
           "x_first": alpha * m / p1}
    if where == "second segment":
        dxdm = alpha / p2
        hicks = -alpha * mv / p2 ** 2 + x * dxdm          # dh/dp2: dx/dp2 at fixed virtual income, plus x dx/dm
        total = hicks - (x - xbar) * dxdm                  # virtual income rises by xbar dp2
        eps = 1e-6
        numeric = (demand(p2 + eps, m)[0] - demand(p2 - eps, m)[0]) / (2 * eps)
        assert abs(total - numeric) < 1e-5
        out.update({"dxdm": dxdm, "substitution": hicks, "income": -(x - xbar) * dxdm, "total": total,
                    "wrong_income": -x * dxdm, "wrong_total": hicks - x * dxdm})
    x_new, where_new = demand(p2_new, m)
    u0 = util(p2, m)
    cv = brentq(lambda extra: util(p2_new, m + extra) - u0, -10.0, 50.0)
    mv_new = m + (p2_new - p1) * xbar
    if where == "second segment" and demand(p2_new, m + cv)[1] == "second segment":
        assert abs(cv - (mv * (p2_new / p2) ** alpha - mv_new)) < 1e-8
    out.update({"p2_new": p2_new, "x_new": x_new, "where_new": where_new, "cv": cv,
                "laspeyres": (x - xbar) * (p2_new - p2), "wrong_laspeyres": x * (p2_new - p2), "alpha": alpha,
                "m": m, "p1": p1, "p2": p2, "xbar": xbar, "x_kink_alpha": demand(p2, m)[0]})
    # the same consumer with a smaller taste for x sits at the kink: alpha = 0.3
    out["kink_case"] = {"alpha": 0.3, "x_first": 0.3 * m / p1, "x_second": 0.3 * mv / p2,
                        "mrs": 0.3 / 0.7 * (m - p1 * xbar) / xbar}
    return out


# ---------------------------------------------------------------------------------------------------------------
# Micro 2: an exchange economy with an externality


def externality_box(a: float = 4.0, e: float = 0.5, X: float = 10.0, Y: float = 20.0) -> dict:
    """Two consumers with quasilinear utility, u_A = a ln x_A + y_A and u_B = a ln x_B + y_B - e x_A: A's
    consumption of good x harms B (smoke).  X units of x and Y of y in all, endowed equally.

    The competitive equilibrium ignores the harm: a / x_A = p = a / x_B, so x_A = x_B = X / 2.  The Pareto set has
    a / x_A - e = a / (X - x_A) (with quasilinear utility it is a vertical line in the box: one x_A, any split of y).
    A Pigouvian tax t = e on A's purchases, with the revenue returned lump sum, decentralizes it."""
    xa_eq = X / 2
    p_eq = a / xa_eq
    xa_po = brentq(lambda x: a / x - e - a / (X - x), 1e-6, X / 2)
    xb_po = X - xa_po
    p_t = a / xb_po
    t = a / xa_po - p_t
    assert abs(t - e) < 1e-9

    def welfare(xa):
        return a * np.log(xa) + a * np.log(X - xa) - e * xa + Y

    res = minimize(lambda v: -welfare(v[0]), [X / 3], bounds=[(1e-3, X - 1e-3)])
    assert abs(res.x[0] - xa_po) < 1e-4
    grid = np.linspace(0.5, X - 0.5, 200)
    return {"a": a, "e": e, "X": X, "Y": Y, "xa_eq": xa_eq, "p_eq": p_eq, "xa_po": xa_po, "xb_po": xb_po,
            "p_tax": p_t, "tax": t, "gain": welfare(xa_po) - welfare(xa_eq), "grid": grid.tolist(),
            "welfare": [welfare(x) for x in grid], "w_eq": welfare(xa_eq), "w_po": welfare(xa_po)}


# ---------------------------------------------------------------------------------------------------------------
# Micro 3: a first-price auction with a reserve


def reserve_auction(n: int = 2, r: float = 0.5, draws: int = 400_000, seed: int = 56) -> dict:
    """n risk-neutral bidders with values uniform on [0, 1] and a reserve price r.  A bidder with value v >= r bids
    b(v) = v - (v^n - r^n) / (n v^(n-1)) (the expected highest rival value below v, with the reserve as the floor);
    one below r stays out.  Expected revenue n integral_r^1 (2v - 1) v^(n-1) dv, the same as a second-price auction
    with the same reserve (revenue equivalence), against (n - 1)/(n + 1) with none; checked by simulation."""
    rng = np.random.default_rng(seed)
    v = rng.random((draws, n))
    b = np.where(v >= r, v - (v ** n - r ** n) / (n * np.maximum(v, 1e-12) ** (n - 1)), -1.0)
    win = b.max(axis=1)
    rev_fp = float(np.where(win >= 0, win, 0.0).mean())
    vs = np.sort(v, axis=1)
    second = np.where(vs[:, -1] >= r, np.maximum(vs[:, -2], r), 0.0)
    rev_sp = float(second.mean())
    rev = 2 * n * (1 - r ** (n + 1)) / (n + 1) - (1 - r ** n)
    rev0 = (n - 1) / (n + 1)
    assert abs(rev_fp - rev) < 3e-3 and abs(rev_sp - rev) < 3e-3
    # the bid function is a best response: check one type's deviation payoff
    vv = 0.8
    bids = np.linspace(r, vv, 2001)
    # rivals use b(.), which is increasing on [r, 1]; P(rival bid < x) = P(rival value < b^{-1}(x))
    vgrid = np.linspace(r, 1, 20001)
    bgrid = vgrid - (vgrid ** n - r ** n) / (n * vgrid ** (n - 1))
    inv = np.interp(bids, bgrid, vgrid)
    payoff = (vv - bids) * inv ** (n - 1)
    b_star = vv - (vv ** n - r ** n) / (n * vv ** (n - 1))
    assert abs(bids[int(np.argmax(payoff))] - b_star) < 2e-3
    vgr = np.linspace(0, 1, 201)
    return {"n": n, "r": r, "v": vgr.tolist(),
            "bid": np.where(vgr >= r, vgr - (vgr ** n - r ** n) / (n * np.maximum(vgr, 1e-12) ** (n - 1)),
                            np.nan).tolist(),
            "bid0": ((n - 1) / n * vgr).tolist(), "rev": rev, "rev0": rev0, "rev_fp_sim": rev_fp,
            "rev_sp_sim": rev_sp, "p_no_sale": r ** n, "b_at_r": r, "b_08": b_star, "draws": draws,
            "dev_bids": bids.tolist(), "dev_payoff": payoff.tolist()}


# ---------------------------------------------------------------------------------------------------------------
# Micro 4: screening, two types and a continuum


def screening(th_l: float = 1.0, th_h: float = 2.0, pi_h: float = 1 / 3, lo: float = 1.0, hi: float = 2.0) -> dict:
    """A seller offers quality q at cost q^2 / 2 to a buyer of type theta, who gets theta q - t.  Two types: the low
    type's participation and the high type's incentive constraint bind, q_H = theta_H (no distortion at the top) and
    q_L = theta_L - pi_H / (1 - pi_H) (theta_H - theta_L), with the high type's information rent (theta_H - theta_L)
    q_L.  A continuum uniform on [lo, hi]: q(theta) = theta - (1 - F) / f = 2 theta - hi, and t(theta) = theta q -
    integral_lo^theta q.  Both checked by brute force."""
    q_h = th_h
    q_l = max(th_l - pi_h / (1 - pi_h) * (th_h - th_l), 0.0)
    t_l = th_l * q_l
    rent = (th_h - th_l) * q_l
    t_h = th_h * q_h - rent
    profit = (1 - pi_h) * (t_l - q_l ** 2 / 2) + pi_h * (t_h - q_h ** 2 / 2)
    fb = (1 - pi_h) * th_l ** 2 / 2 + pi_h * th_h ** 2 / 2

    def neg(z):
        ql, qh = z
        tl = th_l * ql                                    # IR_L binds
        th = th_h * qh - (th_h - th_l) * ql               # IC_H binds
        return -((1 - pi_h) * (tl - ql ** 2 / 2) + pi_h * (th - qh ** 2 / 2))

    res = minimize(neg, [0.3, 1.5], bounds=[(0, 3), (0, 3)])
    assert abs(res.x[0] - q_l) < 1e-4 and abs(res.x[1] - q_h) < 1e-4
    # the unchecked constraints hold: IC_L and IR_H
    assert th_l * q_l - t_l >= th_l * q_h - t_h - 1e-9 and th_h * q_h - t_h >= -1e-9
    th = np.linspace(lo, hi, 201)
    virt = th - (hi - th)
    q = np.maximum(virt, 0.0)
    cum = np.concatenate([[0.0], np.cumsum((q[1:] + q[:-1]) / 2 * np.diff(th))])
    t = th * q - cum
    prof_c = float(np.trapezoid(t - q ** 2 / 2, th) / (hi - lo))
    fb_c = float(np.trapezoid(th ** 2 / 2, th) / (hi - lo))
    # incentive compatibility of the continuum menu: each type prefers its own item
    U = th[:, None] * q[None, :] - t[None, :]
    assert np.all(np.argmax(U, axis=1) >= np.arange(len(th)) - 1)
    return {"th_l": th_l, "th_h": th_h, "pi_h": pi_h, "q_l": q_l, "q_h": q_h, "t_l": t_l, "t_h": t_h, "rent": rent,
            "profit": profit, "first_best": fb, "q_l_fb": th_l, "theta": th.tolist(), "q": q.tolist(),
            "t": t.tolist(), "q_fb": th.tolist(), "profit_c": prof_c, "first_best_c": fb_c,
            "rent_c": (th * q - t).tolist()}


# ---------------------------------------------------------------------------------------------------------------
# Macro 1: the Ramsey model with a tax on capital


def ramsey_tax(alpha: float = 1 / 3, delta: float = 0.05, rho: float = 0.03, theta: float = 2.0, tau: float = 0.25,
               dt: float = 0.02, T: float = 150.0) -> dict:
    """k_dot = k^alpha - delta k - c and c_dot / c = ((1 - tau)(alpha k^(alpha - 1) - delta) - rho) / theta: a tax
    tau on the return to capital net of depreciation, its revenue returned lump sum (so it leaves the resource
    constraint alone).  Before: tau = 0.  An unexpected, permanent tax: k cannot jump, c jumps onto the new saddle
    path and both fall to the new steady state.  Solved by shooting on c0 (bisection)."""

    def kss(t):
        return (alpha / (delta + rho / (1 - t))) ** (1 / (1 - alpha))

    k_old, k_new = kss(0.0), kss(tau)
    c_old = k_old ** alpha - delta * k_old
    c_new = k_new ** alpha - delta * k_new
    steps = int(T / dt)

    def shoot(c0):
        k, c = k_old, c0
        ks, cs = [k], [c]
        for _ in range(steps):
            kd = k ** alpha - delta * k - c
            cd = c * ((1 - tau) * (alpha * k ** (alpha - 1) - delta) - rho) / theta
            k, c = k + dt * kd, c + dt * cd
            ks.append(k)
            cs.append(c)
            if k < 0.6 * k_new:
                return ks, cs, "crash"           # consumed too much: capital runs down past the steady state
            if c < 0.6 * c_new or k > k_old * 1.05:
                return ks, cs, "over"            # consumed too little
            if abs(k - k_new) / k_new < 1e-5 and abs(c - c_new) / c_new < 1e-5:
                return ks, cs, "converge"
        return ks, cs, "crash" if k < k_new else "over"

    lo, hi = c_old * 0.9, k_old ** alpha * 1.2
    for _ in range(100):
        mid = (lo + hi) / 2
        how = shoot(mid)[2]
        if how == "crash":
            hi = mid
        else:
            lo = mid
    c0 = (lo + hi) / 2
    kp, cp, _ = shoot(c0)
    dist = [abs(k - k_new) / k_new + abs(c - c_new) / c_new for k, c in zip(kp, cp)]
    stop = int(np.argmin(dist)) + 1
    kp, cp = np.array(kp[:stop]), np.array(cp[:stop])
    assert c0 > c_old and c_new < c_old and k_new < k_old
    half = float(dt * np.argmax(kp - k_new < 0.5 * (k_old - k_new)))
    kg = np.linspace(0.2 * k_new, 1.6 * k_old, 300)
    return {"alpha": alpha, "delta": delta, "rho": rho, "theta": theta, "tau": tau, "k_old": k_old, "k_new": k_new,
            "c_old": c_old, "c_new": c_new, "c0": c0, "jump": c0 - c_old, "path_k": kp.tolist(),
            "path_c": cp.tolist(), "dt": dt, "half_life": half, "k_gold": (alpha / delta) ** (1 / (1 - alpha)),
            "kdot0_k": kg.tolist(), "kdot0_c": (kg ** alpha - delta * kg).tolist(),
            "r_old": alpha * k_old ** (alpha - 1) - delta, "r_new": alpha * k_new ** (alpha - 1) - delta}


# ---------------------------------------------------------------------------------------------------------------
# Macro 2: a McCall worker with benefits that expire


def mccall_expiring(beta: float = 0.95, b: float = 0.5, z: float = 0.1, D: int = 8, n_w: int = 501) -> dict:
    """Offers w uniform on [0, 1] each period; a job pays w for ever (value w / (1 - beta)).  An unemployed worker
    with d periods of benefit left gets b this period (d >= 1), or z once they have run out (d = 0, a stationary
    problem).  U_d = income_d + beta E max(w / (1 - beta), U_{d-1}), with U_0 its own fixed point.  The reservation
    wage w*_d = (1 - beta) U_d falls as exhaustion approaches, and the exit rate 1 - w*_d rises: the spike at
    exhaustion."""
    w = np.linspace(0, 1, n_w)
    W = w / (1 - beta)

    def emax(U):
        return float(np.trapezoid(np.maximum(W, U), w))

    U0 = brentq(lambda U: z + beta * emax(U) - U, 0.0, 1 / (1 - beta))
    U = [U0]
    for _ in range(D):
        U.append(b + beta * emax(U[-1]))
    U = np.array(U)
    res = (1 - beta) * U
    # the stationary benchmark: benefits for ever
    U_inf = brentq(lambda V: b + beta * emax(V) - V, 0.0, 1 / (1 - beta))
    # closed form for the expired state with uniform offers: w* = z + beta/(2(1-beta)) (1 - w*)^2
    w0 = brentq(lambda x: x - z - beta / (2 * (1 - beta)) * (1 - x) ** 2, 0.0, 1.0)
    assert abs(w0 - res[0]) < 2e-3
    assert np.all(np.diff(res) > 0)
    hazard = 1 - res                                     # chance of accepting this period's offer
    # survival from the start of a spell with D periods of benefit
    surv, s = [], 1.0
    for d in range(D, -1, -1):
        surv.append(s)
        s *= 1 - hazard[d]
    return {"beta": beta, "b": b, "z": z, "D": D, "res": res.tolist(), "hazard": hazard.tolist(),
            "res_inf": (1 - beta) * U_inf, "res_expired": float(res[0]), "res_full": float(res[-1]),
            "survival": surv}


# ---------------------------------------------------------------------------------------------------------------
# Macro 3: the three-equation model under discretion


def discretion(beta: float = 0.99, kappa: float = 0.1, lam: float = 0.25, xstar: float = 0.5, rho_u: float = 0.5,
               h: int = 12) -> dict:
    """Loss sum beta^t [pi^2 + lambda (x - x*)^2], Phillips curve pi = beta E pi' + kappa x + u, u AR(1).  Under
    discretion the bank takes expectations as given: kappa pi + lambda (x - x*) = 0 each period.  The inflation
    bias pi_bar = lambda kappa x* / (lambda (1 - beta) + kappa^2), which buys output of only x_bar = (1 - beta)
    pi_bar / kappa.  A cost shock: pi = lambda / (kappa^2 + lambda (1 - beta rho)) u and x = -kappa / (...) u.
    Under commitment (timeless), pi_t = (lambda / kappa)(x_{t-1} - x_t), solved here by undetermined coefficients
    on x_t = a x_{t-1} + c u_t, for the comparison."""
    pi_bar = lam * kappa * xstar / (lam * (1 - beta) + kappa ** 2)
    x_bar = (1 - beta) * pi_bar / kappa
    den = kappa ** 2 + lam * (1 - beta * rho_u)
    a_pi, a_x = lam / den, -kappa / den
    # check: the Phillips curve holds with E pi' = rho pi
    assert abs(a_pi - (beta * rho_u * a_pi + kappa * a_x + 1)) < 1e-12
    u = rho_u ** np.arange(h + 1)
    pi_d, x_d = a_pi * u, a_x * u
    # commitment: x_t = a x_{t-1} + c u_t, pi_t = (lam/kappa)(x_{t-1} - x_t)
    # Phillips: lam/kap (x_{t-1} - x_t) = beta lam/kap (x_t - E x_{t+1}) + kappa x_t + u_t
    # => beta a^2 - (1 + beta + kappa^2/lam) a + 1 = 0, the root inside the unit circle
    q = 1 + beta + kappa ** 2 / lam
    a = (q - np.sqrt(q * q - 4 * beta)) / (2 * beta)
    # coefficient on u: -lam/kap c = beta lam/kap (c - a c - c rho) + kappa c + 1
    c = -1.0 / (lam / kappa + beta * lam / kappa * (1 - a - rho_u) + kappa)
    x_c, pi_c = np.zeros(h + 1), np.zeros(h + 1)
    xprev = 0.0
    for t in range(h + 1):
        x_c[t] = a * xprev + c * u[t]
        pi_c[t] = lam / kappa * (xprev - x_c[t])
        xprev = x_c[t]
    # the Phillips curve holds along the commitment path (perfect foresight of the decaying shock)
    for t in range(h - 1):
        assert abs(pi_c[t] - (beta * pi_c[t + 1] + kappa * x_c[t] + u[t])) < 1e-9

    def loss(p, x):
        return float(np.sum(beta ** np.arange(len(p)) * (p ** 2 + lam * x ** 2)))
    return {"beta": beta, "kappa": kappa, "lam": lam, "xstar": xstar, "rho_u": rho_u, "pi_bar": pi_bar,
            "x_bar": x_bar, "a_pi": a_pi, "a_x": a_x, "pi_d": pi_d.tolist(), "x_d": x_d.tolist(),
            "pi_c": pi_c.tolist(), "x_c": x_c.tolist(), "loss_d": loss(pi_d, x_d), "loss_c": loss(pi_c, x_c),
            "a_commit": a, "lams": np.linspace(0.02, 1.0, 50).tolist(),
            "bias_by_lam": [lm * kappa * xstar / (lm * (1 - beta) + kappa ** 2) for lm in np.linspace(0.02, 1.0, 50)]}


# ---------------------------------------------------------------------------------------------------------------
# Macro 4: why an Aiyagari economy's interest rate lies below the rate of time preference


def aiyagari_gap(rs=None, **kw) -> dict:
    """Part 52's Aiyagari economy: the capital households supply at each interest rate (with the wage firms pay
    at that rate) and the capital firms demand.  Supply explodes as r approaches the rate of time preference
    1/beta - 1 (with income risk and a borrowing limit, beta (1 + r) >= 1 makes the marginal utility a
    supermartingale bounded below, so assets drift without bound), so the curves cross below it."""
    from . import hetero

    eq = hetero.aiyagari(**kw)
    rho = 1 / eq["beta"] - 1
    if rs is None:
        rs = np.concatenate([np.linspace(-0.01, rho - 0.006, 9), rho - np.array([0.004, 0.002, 0.001])])
    sup = hetero.capital_supply(rs, beta=eq["beta"], gamma=eq["gamma"], **{k: v for k, v in kw.items()
                                                                           if k not in ("beta", "gamma")})
    assert eq["r"] < rho
    return {"r": eq["r"], "rho": rho, "K": eq["K"], "gap": rho - eq["r"], "beta": eq["beta"], "gamma": eq["gamma"],
            "rs": [s["r"] for s in sup], "supply": [s["supply"] for s in sup], "demand": [s["demand"] for s in sup],
            "K_rep": hetero.capital_demand(rho, 0.36, 0.08)}


# ---------------------------------------------------------------------------------------------------------------
# Metrics 1: a supply-and-demand system, the order and rank conditions, the Wald estimator


def supply_demand(n: int = 2000, a: float = 10.0, b: float = 1.0, c: float = 2.0, d: float = 1.0, e: float = -2.0,
                  sd_d: float = 1.0, sd_s: float = 1.0, p_storm: float = 0.3, seed: int = 56) -> dict:
    """Demand q = a - b p + u_d; supply q = c + d p + e w + u_s, with w = 1 in a storm (it cuts supply, e < 0).  The
    demand equation excludes w, which moves supply only: one excluded instrument for one endogenous regressor,
    exactly identified (order), as long as e != 0 (rank).  The supply curve excludes nothing and is not identified.
    The Wald estimator of the demand slope: the ratio of the storm's effect on quantity to its effect on price."""
    rng = np.random.default_rng(seed)
    w = (rng.random(n) < p_storm).astype(float)
    ud, us = sd_d * rng.standard_normal(n), sd_s * rng.standard_normal(n)
    p = (a - c - e * w + ud - us) / (b + d)
    q = a - b * p + ud
    X = np.column_stack([np.ones(n), p])
    ols = np.linalg.lstsq(X, q, rcond=None)[0][1]
    dq = q[w == 1].mean() - q[w == 0].mean()
    dp = p[w == 1].mean() - p[w == 0].mean()
    wald = dq / dp
    # its probability limit for OLS: cov(q, p) / var(p)
    var_p = (e ** 2 * p_storm * (1 - p_storm) + sd_d ** 2 + sd_s ** 2) / (b + d) ** 2
    cov_qp = (-b * (e ** 2 * p_storm * (1 - p_storm) + sd_d ** 2 + sd_s ** 2) / (b + d) + sd_d ** 2) / (b + d)
    plim_ols = cov_qp / var_p
    # delta-method standard error of the Wald ratio (two-sample means)
    z = w == 1
    se = abs(1 / dp) * np.sqrt(np.var(q[z] + b * p[z]) / z.sum() + np.var(q[~z] + b * p[~z]) / (~z).sum())
    return {"n": n, "a": a, "b": b, "c": c, "d": d, "e": e, "p_storm": p_storm, "ols": float(ols),
            "plim_ols": float(plim_ols), "wald": float(wald), "se_wald": float(se), "dq": float(dq),
            "dp": float(dp), "p": p[:400].tolist(), "q": q[:400].tolist(), "w": w[:400].tolist(),
            "means": {"p0": float(p[w == 0].mean()), "q0": float(q[w == 0].mean()), "p1": float(p[w == 1].mean()),
                      "q1": float(q[w == 1].mean())}}


# ---------------------------------------------------------------------------------------------------------------
# Metrics 2: GMM for an Euler equation


def euler_gmm(T: int = 2000, beta: float = 0.97, gamma: float = 3.0, seed: int = 56) -> dict:
    """Part 54's Hansen-Singleton set-up: two assets, instruments a constant, lagged consumption growth and both
    lagged returns, so 8 moment conditions for 2 parameters.  First step with the identity, second with the
    inverse covariance; the J statistic is chi-square with 8 - 2 = 6 degrees of freedom."""
    from . import estimate

    dat = estimate.euler_data(T=T, beta=beta, gamma=gamma, seed=seed)
    f = estimate.euler_moments(dat)
    one = estimate.gmm(f, [0.95, 2.0], two_step=False)
    two = estimate.gmm(f, [0.95, 2.0], two_step=True)
    m = f(np.array([beta, gamma])).shape[1]
    return {"T": T, "beta": beta, "gamma": gamma, "m": m, "k": 2, "df": m - 2, "one": one, "two": two}


# ---------------------------------------------------------------------------------------------------------------
# Metrics 3: two-way fixed effects with staggered timing


def staggered_did(T: int = 10, g_early: int = 3, g_late: int = 7, slope: float = 1.0, n_each: int = 1,
                  never: bool = True) -> dict:
    """Two groups adopt a policy at different dates and its effect grows with time since adoption: tau(e) = slope
    (e + 1) for e = t - g >= 0.  No noise, so every number is exact.  The two-way fixed-effects coefficient, its
    Goodman-Bacon decomposition into 2x2 comparisons (one of which uses the already-treated early group as a
    control, so its growing effect enters with a minus sign), the true average effect on the treated, and the
    imputation (Borusyak, Jaravel and Spiess) or Callaway-Sant'Anna estimate, which recover it."""
    from explainer.stats.kit import quasi

    times = np.arange(1, T + 1)
    G = [g_early] * n_each + [g_late] * n_each + ([np.inf] * n_each if never else [])
    G = np.array(G, float)
    N = len(G)
    unit = np.arange(N)[:, None] * 0.5
    time = 0.3 * times[None, :]
    D = (times[None, :] >= G[:, None]).astype(float)
    E = np.where(D > 0, times[None, :] - G[:, None], -1)
    tau = np.where(D > 0, slope * (E + 1), 0.0)
    Y = unit + time + tau
    tw = quasi.twfe(Y, D)["beta"]
    parts = quasi.bacon(Y, G, times)
    att = float(tau[D > 0].mean())
    imp = quasi.imputation(Y, G, times)
    assert abs(imp["att"] - att) < 1e-6
    assert abs(sum(p["w"] * p["est"] for p in parts) - tw) < 1e-9
    # the TWFE weights on each treated cell: beta = sum w_it tau_it with w = Dd_it / sum Dd^2
    Dd = D - D.mean(1, keepdims=True) - D.mean(0, keepdims=True) + D.mean()
    wcell = Dd / np.sum(Dd * D)
    assert abs(np.sum(wcell * tau) - tw) < 1e-9
    return {"T": T, "times": times.tolist(), "G": [float(g) if np.isfinite(g) else None for g in G],
            "Y": Y.tolist(), "D": D.tolist(), "tau": tau.tolist(), "twfe": tw, "att": att,
            "imputation": float(imp["att"]),
            "bacon": [{**p, "c": (None if not np.isfinite(p["c"]) else float(p["c"]))} for p in parts],
            "weights": (wcell * D).tolist(), "neg_weight_cells": int(np.sum((wcell < -1e-12) & (D > 0)))}


# ---------------------------------------------------------------------------------------------------------------
# Metrics 4: a VAR with a long-run restriction


def long_run_var(T: int = 400, seed: int = 56, reps: int = 200) -> dict:
    """Blanchard and Quah's bivariate VAR: output growth and unemployment, y_t = A y_{t-1} + B eps_t, with a supply
    shock that moves output's level for ever and a demand shock that does not.  The long-run impact matrix
    C(1) B = (I - A)^{-1} B has a zero above the diagonal; Sigma = B B' and that zero pin B down: C(1) B is the
    Cholesky factor of C(1) Sigma C(1)'.  In population, then from simulated samples."""
    # A planted so that a demand shock that lifts growth by 0.5 and cuts unemployment by 0.3 on impact leaves the
    # level of output unchanged in the long run: row 1 of (I - A)^{-1} is orthogonal to that column
    a22, a11, a21 = 0.8, 0.2, -0.1
    a12 = (1 - a22) * 0.5 / 0.3
    A = np.array([[a11, a12], [a21, a22]])
    B = np.array([[0.8, 0.5], [-0.1, -0.3]])
    C1 = np.linalg.inv(np.eye(2) - A)
    L = C1 @ B
    assert abs(L[0, 1]) < 1e-12 and np.max(np.abs(np.linalg.eigvals(A))) < 1

    def identify(C1_, S_):
        Lc = np.linalg.cholesky(C1_ @ S_ @ C1_.T)
        Bc = np.linalg.solve(C1_, Lc)
        if Bc[1, 1] > 0:                                  # sign: the demand shock lowers unemployment on impact
            Bc[:, 1] *= -1
        if Bc[0, 0] < 0:
            Bc[:, 0] *= -1
        return Bc

    Sigma = B @ B.T
    Bh = identify(C1, Sigma)
    assert np.allclose(Bh, B, atol=1e-10)
    rng = np.random.default_rng(seed)
    est = []
    for r in range(reps):
        y = np.zeros((T + 50, 2))
        for t in range(1, T + 50):
            y[t] = A @ y[t - 1] + B @ rng.standard_normal(2)
        y = y[50:]
        X, Yv = np.column_stack([np.ones(T - 1), y[:-1]]), y[1:]
        coef = np.linalg.lstsq(X, Yv, rcond=None)[0]
        Ah = coef[1:].T
        U = Yv - X @ coef
        S = U.T @ U / (len(U) - 3)
        est.append(identify(np.linalg.inv(np.eye(2) - Ah), S))
    est = np.array(est)
    # responses of output's level (cumulated growth) and unemployment to each shock
    h = 20
    resp = np.zeros((h + 1, 2, 2))
    M = np.eye(2)
    for k in range(h + 1):
        resp[k] = M @ B
        M = A @ M
    level = np.cumsum(resp[:, 0, :], axis=0)
    return {"A": A.tolist(), "B": B.tolist(), "Sigma": Sigma.tolist(), "C1": C1.tolist(), "L": L.tolist(),
            "B_est_mean": est.mean(0).tolist(), "B_est_sd": est.std(0).tolist(), "reps": reps, "T": T,
            "level_supply": level[:, 0].tolist(), "level_demand": level[:, 1].tolist(),
            "u_supply": resp[:, 1, 0].tolist(), "u_demand": resp[:, 1, 1].tolist(),
            "n_free": 4, "n_cov": 3}
