"""Agora's many agents (Part 52): economies with a distribution of households and firms.

* **Aggregation** (:func:`gorman_demand`): when a redistribution leaves aggregate demand unchanged (common, linear
  Engel curves) and when it does not.
* **Aiyagari's economy** (:func:`household`, :func:`young_step`, :func:`stationary`, :func:`aiyagari`): households
  facing uninsurable income risk and a borrowing limit, solved by the endogenous grid method; the stationary
  distribution by Young's lottery method; the interest rate that clears the capital market, found by bisection;
  wealth Gini, top shares, the share at the limit, marginal propensities to consume (:func:`mpcs`); permanent
  differences in patience (:func:`aiyagari_types`); a table over persistence, risk and risk aversion
  (:func:`aiyagari_table`); a simulated population (:func:`simulate`).
* **Krusell and Smith** (:func:`krusell_smith`): aggregate productivity shocks, households who forecast capital with
  a log-linear rule, the rule updated from a simulated panel until it settles; its R-squared and Den Haan's dynamic
  forecast error.
* **Huggett in continuous time** (:func:`huggett_ct`): the bond market cleared with the HJB and Kolmogorov forward
  equations of Agora's solver.
* **Sequence-space Jacobians** (:func:`jacobians`): the fake-news algorithm of Auclert, Bardóczy, Rognlie and Straub
  for the Jacobians of aggregate consumption with respect to the paths of the interest rate and of income, checked
  against brute force (:func:`jacobian_column_brute`); **a one-asset HANK** (:func:`hank_rate_cut`,
  :func:`hank_multiplier`): the direct and indirect effects of a rate cut, and the spending multiplier.
* **Firms** (:func:`hopenhayn`): Hopenhayn's industry with entry, exit and a stationary size distribution.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np

from . import solve as S


# ---------------------------------------------------------------------------------------------------------------
# aggregation


def gorman_demand(incomes, a, b, transfer: float, donor: int, recipient: int) -> dict:
    """Demand c_i = a_i + b_i m_i for each household; a transfer of ``transfer`` from ``donor`` to ``recipient``.
    Aggregate demand is unchanged when the slopes b are equal (Gorman's condition), and moves by
    (b_recipient - b_donor) x transfer otherwise."""
    m = np.asarray(incomes, float).copy()
    a, b = np.asarray(a, float), np.asarray(b, float)
    before = float(np.sum(a + b * m))
    m[donor] -= transfer
    m[recipient] += transfer
    after = float(np.sum(a + b * m))
    return {"before": before, "after": after, "change": after - before}


# ---------------------------------------------------------------------------------------------------------------
# Aiyagari


def asset_grid(n: int = 200, a_min: float = 0.0, a_max: float = 200.0, curve: float = 3.0) -> np.ndarray:
    x = np.linspace(0, 1, n)
    return a_min + (a_max - a_min) * x ** curve


def income_chain(rho: float, sigma: float, n: int = 7) -> tuple:
    """A Rouwenhorst chain for log efficiency with persistence rho and innovation s.d. sigma, normalized to mean
    one: (efficiency levels, transition matrix, stationary distribution)."""
    z, P = S.rouwenhorst(n, rho, sigma)
    e = np.exp(z)
    pi = np.linalg.matrix_power(P, 2000)[0]
    e = e / (pi @ e)
    return e, P, pi


def household(r: float, w: float, beta: float, gamma: float, e, P, a, a_min: float = 0.0, c0=None,
              tol: float = 1e-10, max_iter: int = 10000) -> dict:
    """The household's consumption and savings rules on the asset grid ``a`` for each efficiency state, by the
    endogenous grid method: a' = (1 + r) a + w e - c >= a_min."""
    R = 1.0 + r
    y = w * np.asarray(e)
    c = (R * a[:, None] + y[None, :] - a_min) * 0.5 + 1e-8 if c0 is None else c0.copy()
    for it in range(max_iter):
        emu = S.up(c, gamma) @ P.T
        c_end = S.up_inv(beta * R * emu, gamma)
        a_end = (c_end + a[:, None] - y[None, :]) / R
        cn = np.empty_like(c)
        for s in range(len(y)):
            cn[:, s] = np.interp(a, a_end[:, s], c_end[:, s])
            bind = a < a_end[0, s]
            cn[bind, s] = R * a[bind] + y[s] - a_min
        d = np.max(np.abs(cn - c))
        c = cn
        if d < tol:
            break
    ap = np.maximum(R * a[:, None] + y[None, :] - c, a_min)
    return {"c": c, "ap": ap, "iters": it + 1}


def young_step(D, ap, a, P):
    """One step of the distribution under the savings rule ``ap`` by Young's (2010) lottery: each household's
    savings are split between the two grid points around them, then income moves by P."""
    n_a, n_e = D.shape
    idx = np.clip(np.searchsorted(a, ap, side="right") - 1, 0, n_a - 2)
    w_hi = np.clip((ap - a[idx]) / (a[idx + 1] - a[idx]), 0.0, 1.0)
    Dn = np.zeros_like(D)
    for s in range(n_e):
        np.add.at(Dn[:, s], idx[:, s], D[:, s] * (1 - w_hi[:, s]))
        np.add.at(Dn[:, s], idx[:, s] + 1, D[:, s] * w_hi[:, s])
    return Dn @ P


def stationary(ap, a, P, pi, tol: float = 1e-12, max_iter: int = 20000, D0=None):
    D = np.outer(np.full(len(a), 1.0 / len(a)), pi) if D0 is None else D0
    for _ in range(max_iter):
        Dn = young_step(D, ap, a, P)
        if np.max(np.abs(Dn - D)) < tol:
            return Dn
        D = Dn
    return D


def firm(K: float, alpha: float = 0.36, delta: float = 0.08, L: float = 1.0) -> dict:
    return {"r": alpha * (K / L) ** (alpha - 1) - delta, "w": (1 - alpha) * (K / L) ** alpha}


def capital_demand(r: float, alpha: float = 0.36, delta: float = 0.08, L: float = 1.0) -> float:
    return L * (alpha / (r + delta)) ** (1 / (1 - alpha))


def gini(x, w) -> float:
    """The Gini coefficient of values ``x`` with weights ``w``."""
    x, w = np.asarray(x, float).ravel(), np.asarray(w, float).ravel()
    o = np.argsort(x)
    x, w = x[o], w[o] / w.sum()
    cx = np.cumsum(w * x)
    if cx[-1] <= 0:
        return 0.0
    L = cx / cx[-1]
    Lp = np.concatenate([[0.0], L[:-1]])
    return float(1 - np.sum(w * (L + Lp)))


def top_share(x, w, q: float) -> float:
    """The share of the total held by the top fraction ``q``."""
    x, w = np.asarray(x, float).ravel(), np.asarray(w, float).ravel()
    o = np.argsort(x)[::-1]
    x, w = x[o], w[o] / w.sum()
    cw = np.cumsum(w)
    k = np.searchsorted(cw, q)
    part = np.sum(x[:k] * w[:k]) + (q - (cw[k - 1] if k > 0 else 0.0)) * x[min(k, len(x) - 1)]
    return float(part / np.sum(x * w))


def mpcs(c, a, R, windfall: float) -> np.ndarray:
    """The marginal propensity to consume out of a windfall at each grid point: (c(a + x/R) - c(a)) / x, the windfall
    arriving as cash on hand."""
    out = np.empty_like(c)
    for s in range(c.shape[1]):
        out[:, s] = (np.interp(a + windfall / R, a, c[:, s]) - c[:, s]) / windfall
    return out


def aiyagari(beta: float = 0.96, gamma: float = 3.0, rho: float = 0.9, sigma: float = 0.2, n_e: int = 7,
             alpha: float = 0.36, delta: float = 0.08, a_min: float = 0.0, n_a: int = 300, a_max: float = 250.0,
             tol: float = 1e-6, windfall: float = 0.05) -> dict:
    """Aiyagari's (1994) economy in steady state: the interest rate that makes the capital households supply equal
    the capital firms demand, the wage, the distribution and its statistics."""
    e, P, pi = income_chain(rho, sigma, n_e)
    a = asset_grid(n_a, a_min, a_max)
    lo, hi = -delta + 1e-4, 1 / beta - 1 - 1e-6
    c0 = None
    D = None
    for _ in range(60):
        r = 0.5 * (lo + hi)
        K = capital_demand(r, alpha, delta)
        w = firm(K, alpha, delta)["w"]
        h = household(r, w, beta, gamma, e, P, a, a_min, c0=c0)
        c0 = h["c"]
        D = stationary(h["ap"], a, P, pi, D0=D)
        A = float(np.sum(D * a[:, None]))
        if A > K:
            hi = r
        else:
            lo = r
        if hi - lo < tol:
            break
    r = 0.5 * (lo + hi)
    K = capital_demand(r, alpha, delta)
    w = firm(K, alpha, delta)["w"]
    h = household(r, w, beta, gamma, e, P, a, a_min, c0=c0)
    D = stationary(h["ap"], a, P, pi, D0=D)
    wealth = np.repeat(a[:, None], n_e, axis=1)
    m = mpcs(h["c"], a, 1 + r, windfall * w)
    return {"r": r, "K": K, "w": w, "Y": K ** alpha, "saving_rate": delta * K / K ** alpha, "a": a, "e": e,
            "P": P, "pi": pi, "c": h["c"], "ap": h["ap"], "D": D, "A": float(np.sum(D * wealth)),
            "gini": gini(wealth, D), "top1": top_share(wealth, D, 0.01), "top10": top_share(wealth, D, 0.10),
            "at_limit": float(D[0].sum()), "mpc": m, "mean_mpc": float(np.sum(D * m)), "rho_time": 1 / beta - 1,
            "beta": beta, "gamma": gamma}


def aiyagari_types(betas=(0.94, 0.96, 0.98), shares=(1 / 3, 1 / 3, 1 / 3), **kw) -> dict:
    """The same economy with permanent differences in patience: each type's own savings at a common interest rate,
    which clears the capital market for the total."""
    alpha, delta = kw.get("alpha", 0.36), kw.get("delta", 0.08)
    gamma, rho, sigma, n_e = kw.get("gamma", 3.0), kw.get("rho", 0.9), kw.get("sigma", 0.2), kw.get("n_e", 7)
    e, P, pi = income_chain(rho, sigma, n_e)
    a = asset_grid(kw.get("n_a", 300), 0.0, kw.get("a_max", 400.0))
    lo, hi = -delta + 1e-4, 1 / max(betas) - 1 - 1e-6
    for _ in range(60):
        r = 0.5 * (lo + hi)
        K = capital_demand(r, alpha, delta)
        w = firm(K, alpha, delta)["w"]
        Ds = []
        A = 0.0
        for b, sh in zip(betas, shares):
            h = household(r, w, b, gamma, e, P, a)
            Dt = stationary(h["ap"], a, P, pi)
            Ds.append(sh * Dt)
            A += sh * float(np.sum(Dt * a[:, None]))
        if A > K:
            hi = r
        else:
            lo = r
        if hi - lo < 1e-6:
            break
    D = np.concatenate(Ds, axis=1)
    wealth = np.repeat(a[:, None], D.shape[1], axis=1)
    return {"r": r, "K": K, "gini": gini(wealth, D), "top1": top_share(wealth, D, 0.01),
            "top10": top_share(wealth, D, 0.10), "at_limit": float(D[0].sum()), "a": a,
            "D_by_type": [Dt.sum(axis=1) for Dt in Ds]}


def aiyagari_table(rhos=(0.0, 0.3, 0.6, 0.9), sigmas=(0.2, 0.4), gammas=(1.0, 3.0, 5.0), **kw) -> list:
    """The equilibrium interest rate (percent) over persistence, the s.d. of log income and risk aversion, as in
    Aiyagari's (1994) Table II (recomputed here, with Rouwenhorst's chain)."""
    rows = []
    for sg in sigmas:
        for rh in rhos:
            for gm in gammas:
                res = aiyagari(rho=rh, sigma=sg * np.sqrt(1 - rh ** 2), gamma=gm, **kw)
                rows.append({"sigma": sg, "rho": rh, "gamma": gm, "r": 100 * res["r"],
                             "saving_rate": 100 * res["saving_rate"]})
    return rows


def simulate(res: dict, n: int = 100000, T: int = 400, seed: int = 0, keep: int = 5) -> dict:
    """A population of ``n`` households following the Aiyagari rules from equal wealth: the final cross-section of
    wealth and income state, and the paths of ``keep`` households."""
    rng = np.random.default_rng(seed)
    a, ap, P, e = res["a"], res["ap"], res["P"], res["e"]
    cum = np.cumsum(P, axis=1)
    s = rng.choice(len(e), size=n, p=res["pi"])
    k = np.full(n, float(np.sum(res["D"] * a[:, None])))
    paths = np.zeros((T, keep))
    for t in range(T):
        nxt = np.empty(n)
        for j in range(len(e)):
            sel = s == j
            nxt[sel] = np.interp(k[sel], a, ap[:, j])
        k = nxt
        u = rng.random(n)
        s = (u[:, None] > cum[s]).sum(axis=1)
        paths[t] = k[:keep]
    return {"wealth": k, "state": s, "paths": paths}


# ---------------------------------------------------------------------------------------------------------------
# Huggett in continuous time


def huggett_ct(rho: float = 0.05, gamma: float = 2.0, z=(0.1, 0.2), lam=(1.2, 1.2), a_min: float = -0.15,
               a_max: float = 5.0, n: int = 500) -> dict:
    """The interest rate at which households' bond holdings sum to zero (Huggett 1993), with the household of
    Agora's solver (Achdou et al. 2022)."""
    lo, hi = 0.0, rho - 1e-4
    for _ in range(40):
        r = 0.5 * (lo + hi)
        res = S.hjb_household(rho=rho, r=r, gamma=gamma, z=z, lam=lam, a_min=a_min, a_max=a_max, n=n)
        a = np.array(res["a"])
        g = np.array(res["g"])
        B = float((a[:, None] * g).sum() * (a[1] - a[0]))
        if B > 0:
            hi = r
        else:
            lo = r
        if hi - lo < 1e-6:
            break
    return {"r": r, "B": B, "a": res["a"], "g": res["g"], "s": res["s"], "c": res["c"]}


# ---------------------------------------------------------------------------------------------------------------
# a general household: state-specific returns and incomes


def household_general(R, y, beta: float, gamma: float, P, a, a_min: float = 0.0, c0=None, tol: float = 1e-10,
                      max_iter: int = 20000) -> dict:
    """The endogenous grid method when the gross return ``R`` and income ``y`` differ by state (a Markov chain with
    transition matrix ``P``): a' = R_s a + y_s - c >= a_min."""
    R, y = np.asarray(R, float), np.asarray(y, float)
    c = 0.5 * (R[None, :] * a[:, None] + y[None, :] - a_min) + 1e-8 if c0 is None else c0.copy()
    for it in range(max_iter):
        emu = (S.up(c, gamma) * R[None, :]) @ P.T
        c_end = S.up_inv(beta * emu, gamma)
        a_end = (c_end + a[:, None] - y[None, :]) / R[None, :]
        cn = np.empty_like(c)
        for s in range(len(y)):
            cn[:, s] = np.interp(a, a_end[:, s], c_end[:, s])
            bind = a < a_end[0, s]
            cn[bind, s] = R[s] * a[bind] + y[s] - a_min
        d = np.max(np.abs(cn - c) / np.maximum(1.0, np.abs(c)))
        c = cn
        if d < tol:
            break
    ap = np.maximum(R[None, :] * a[:, None] + y[None, :] - c, a_min)
    return {"c": c, "ap": ap, "iters": it + 1}


def aiyagari_returns(r: float, w: float, beta: float = 0.96, gamma: float = 3.0, rho: float = 0.9,
                     sigma: float = 0.2, n_e: int = 7, premium: float = 0.06, p_up: float = 0.02,
                     p_down: float = 0.2, n_a: int = 400, a_max: float = 3000.0) -> dict:
    """Aiyagari's households at a given interest rate and wage, with a second, persistent risk: in the "business"
    state, entered with probability ``p_up`` a year and left with probability ``p_down``, wealth earns ``premium``
    more (after Benhabib, Bisin and Zhu 2011, 2015). Returns the distribution's top shares and its Pareto tail."""
    e, Pe, pie = income_chain(rho, sigma, n_e)
    Pb = np.array([[1 - p_up, p_up], [p_down, 1 - p_down]])
    P = np.kron(Pb, Pe)
    R = np.concatenate([np.full(n_e, 1 + r), np.full(n_e, 1 + r + premium)])
    y = np.concatenate([w * e, w * e])
    a = asset_grid(n_a, 0.0, a_max, curve=4.0)
    h = household_general(R, y, beta, gamma, P, a)
    pi = np.kron(np.array([p_down, p_up]) / (p_up + p_down), pie)
    D = stationary(h["ap"], a, P, pi)
    wealth = np.repeat(a[:, None], D.shape[1], axis=1)
    out = {"a": a, "D": D, "A": float(np.sum(D * wealth)), "gini": gini(wealth, D),
           "top1": top_share(wealth, D, 0.01), "top10": top_share(wealth, D, 0.10),
           "business_share": p_up / (p_up + p_down), "upper_mass": float(D[-1].sum())}
    out["pareto"] = pareto_tail(a, D.sum(axis=1))
    return out


def pareto_tail(a, mass, q_lo: float = 0.01, q_hi: float = 0.001) -> dict:
    """The slope of log(share richer than a) against log(a) between the top ``q_lo`` and the top ``q_hi``: minus
    the Pareto exponent of the tail."""
    a, mass = np.asarray(a, float), np.asarray(mass, float) / np.sum(mass)
    tail = 1 - np.cumsum(mass) + mass
    sel = (tail <= q_lo) & (tail >= q_hi) & (a > 0)
    if sel.sum() < 3:
        return {"alpha": float("nan"), "points": int(sel.sum())}
    b = np.polyfit(np.log(a[sel]), np.log(tail[sel]), 1)
    return {"alpha": float(-b[0]), "points": int(sel.sum()), "log_a": np.log(a[sel]).tolist(),
            "log_tail": np.log(tail[sel]).tolist()}


def pareto_from_shares(top1: float, top10: float) -> float:
    """The Pareto exponent alpha implied by two top shares: S(p) = p^(1 - 1/alpha)."""
    return float(1.0 / (1.0 - np.log(top1 / top10) / np.log(0.1)))


# ---------------------------------------------------------------------------------------------------------------
# Krusell and Smith (1998), in the calibration of Den Haan, Judd and Juillard (2010)


def ks_chain(u=(0.10, 0.04), dur_z: float = 8.0, dur_u=(2.5, 1.5)) -> tuple:
    """The aggregate chain (bad, good) and the employment chain conditional on the aggregate transition, built as
    Krusell and Smith did: spells of bad and good times of ``dur_z`` quarters on average, unemployment spells of
    ``dur_u`` quarters, and unemployment rates ``u`` that hold exactly in every period."""
    pzz = 1 - 1 / dur_z
    Pz = np.array([[pzz, 1 - pzz], [1 - pzz, pzz]])
    p00 = np.empty((2, 2))
    p00[0, 0] = 1 - 1 / dur_u[0]
    p00[1, 1] = 1 - 1 / dur_u[1]
    p00[0, 1] = 0.75 * p00[1, 1]
    p00[1, 0] = 1.25 * p00[0, 0]
    Pe = np.zeros((2, 2, 2, 2))
    for z in range(2):
        for zp in range(2):
            Pe[z, zp, 0, 0] = p00[z, zp]
            Pe[z, zp, 0, 1] = 1 - p00[z, zp]
            p10 = (u[zp] - u[z] * p00[z, zp]) / (1 - u[z])
            Pe[z, zp, 1, 0] = p10
            Pe[z, zp, 1, 1] = 1 - p10
    return Pz, Pe


def krusell_smith(beta: float = 0.99, gamma: float = 1.0, alpha: float = 0.36, delta: float = 0.025,
                  dz: float = 0.01, u=(0.10, 0.04), mu: float = 0.15, l_bar: float = 1 / 0.9, n_a: int = 100,
                  a_max: float = 250.0, K_grid=(30.0, 34.0, 38.0, 42.0, 46.0, 50.0), T: int = 1100, burn: int = 100,
                  seed: int = 0, damp: float = 0.3, tol: float = 1e-6, max_rounds: int = 60,
                  inner_tol: float = 1e-8) -> dict:
    """Households who face unemployment risk and aggregate productivity shocks and forecast next quarter's capital
    from this quarter's with a log-linear rule for each aggregate state, log K' = b0 + b1 log K. The rule is
    guessed, the households' problem solved by the endogenous grid method on (assets, K), the economy simulated by
    moving the whole distribution (no sampling error), the rule re-estimated, until it settles. Returns the rule,
    its R-squared, Den Haan's (2010) dynamic forecast errors and the simulated path."""
    Pz, Pe = ks_chain(u, 8.0, (2.5, 1.5))
    zs = np.array([1 - dz, 1 + dz])
    u = np.asarray(u, float)
    L = l_bar * (1 - u)
    tau = mu * u / (l_bar * (1 - u))
    a = asset_grid(n_a, 0.0, a_max, curve=3.0)
    Kg = np.asarray(K_grid, float)
    nK = len(Kg)

    def prices(K, z):
        r = alpha * zs[z] * (K / L[z]) ** (alpha - 1) - delta
        w = (1 - alpha) * zs[z] * (K / L[z]) ** alpha
        return r, w

    def income(w, z):
        return np.array([mu * w, (1 - tau[z]) * w * l_bar])

    rng = np.random.default_rng(seed)
    zpath = np.empty(T, int)
    zpath[0] = 1
    for t in range(1, T):
        zpath[t] = zpath[t - 1] if rng.random() < Pz[zpath[t - 1], zpath[t - 1]] else 1 - zpath[t - 1]

    b = np.array([[0.0, 1.0], [0.0, 1.0]])
    c = np.empty((n_a, nK, 4))
    for i, K in enumerate(Kg):
        for z in range(2):
            r, w = prices(K, z)
            yv = income(w, z)
            for e in range(2):
                c[:, i, 2 * z + e] = 0.1 * (1 + r) * a + yv[e]
    history = []
    for rnd in range(max_rounds):
        # households, given the rule
        Kp = np.exp(b[:, 0][None, :] + b[:, 1][None, :] * np.log(Kg)[:, None])  # (nK, z)
        for it in range(5000):
            cn = np.empty_like(c)
            for i, K in enumerate(Kg):
                for z in range(2):
                    kp = Kp[i, z]
                    j = int(np.clip(np.searchsorted(Kg, kp) - 1, 0, nK - 2))
                    th = (kp - Kg[j]) / (Kg[j + 1] - Kg[j])
                    r, w = prices(K, z)
                    yv = income(w, z)
                    emu = np.zeros((n_a, 2))
                    for zp in range(2):
                        rp, _ = prices(kp, zp)
                        cnext = (1 - th) * c[:, j, 2 * zp:2 * zp + 2] + th * c[:, j + 1, 2 * zp:2 * zp + 2]
                        cnext = np.maximum(cnext, 1e-10)
                        emu += Pz[z, zp] * (1 + rp) * (S.up(cnext, gamma) @ Pe[z, zp].T)
                    c_end = S.up_inv(beta * emu, gamma)
                    for e in range(2):
                        a_end = (c_end[:, e] + a - yv[e]) / (1 + r)
                        col = np.interp(a, a_end, c_end[:, e])
                        bind = a < a_end[0]
                        col[bind] = (1 + r) * a[bind] + yv[e]
                        cn[:, i, 2 * z + e] = col
            d = np.max(np.abs(cn - c))
            c = cn
            if d < inner_tol:
                break
        ap = np.empty_like(c)
        for i, K in enumerate(Kg):
            for z in range(2):
                r, w = prices(K, z)
                yv = income(w, z)
                for e in range(2):
                    ap[:, i, 2 * z + e] = np.maximum((1 + r) * a + yv[e] - c[:, i, 2 * z + e], 0.0)
        # the economy, moving the whole distribution
        D = np.zeros((n_a, 2))
        k0 = int(np.searchsorted(a, 40.0))
        D[k0, 0], D[k0, 1] = u[zpath[0]], 1 - u[zpath[0]]
        Kt = np.empty(T)
        for t in range(T):
            K = float(np.sum(D * a[:, None]))
            Kt[t] = K
            if t == T - 1:
                break
            z = zpath[t]
            j = int(np.clip(np.searchsorted(Kg, K) - 1, 0, nK - 2))
            th = (K - Kg[j]) / (Kg[j + 1] - Kg[j])
            pol = (1 - th) * ap[:, j, 2 * z:2 * z + 2] + th * ap[:, j + 1, 2 * z:2 * z + 2]
            idx = np.clip(np.searchsorted(a, pol, side="right") - 1, 0, n_a - 2)
            wh = np.clip((pol - a[idx]) / (a[idx + 1] - a[idx]), 0.0, 1.0)
            Dn = np.zeros_like(D)
            for e in range(2):
                np.add.at(Dn[:, e], idx[:, e], D[:, e] * (1 - wh[:, e]))
                np.add.at(Dn[:, e], idx[:, e] + 1, D[:, e] * wh[:, e])
            D = Dn @ Pe[z, zpath[t + 1]]
        # the rule, re-estimated
        bn = np.empty((2, 2))
        r2 = np.empty(2)
        x, xn, zz = np.log(Kt[burn:-1]), np.log(Kt[burn + 1:]), zpath[burn:-1]
        for z in range(2):
            sel = zz == z
            X = np.column_stack([np.ones(sel.sum()), x[sel]])
            coef, *_ = np.linalg.lstsq(X, xn[sel], rcond=None)
            bn[z] = coef
            res = xn[sel] - X @ coef
            r2[z] = 1 - res.var() / xn[sel].var()
        diff = float(np.max(np.abs(bn - b)))
        history.append({"round": rnd, "b": bn.tolist(), "r2": r2.tolist(), "diff": diff})
        b = damp * bn + (1 - damp) * b
        if diff < tol:
            b = bn
            break
    # Den Haan's dynamic forecast: the rule alone, run on the shocks
    Kh = np.empty(T)
    Kh[burn] = Kt[burn]
    for t in range(burn, T - 1):
        z = zpath[t]
        Kh[t + 1] = np.exp(b[z, 0] + b[z, 1] * np.log(Kh[t]))
    err = 100 * np.abs(np.log(Kh[burn:]) - np.log(Kt[burn:]))
    one = 100 * np.abs(np.log(Kt[burn + 1:]) - (b[zpath[burn:-1], 0] + b[zpath[burn:-1], 1] * np.log(Kt[burn:-1])))
    # who holds the capital, and how they save
    i_mid = int(np.argmin(np.abs(Kg - Kt[burn:].mean())))
    mps = np.gradient(ap[:, i_mid, 3], a)
    wealth_share_rich = None
    m = D.sum(axis=1)
    cw = np.cumsum(m)
    half = int(np.searchsorted(cw, 0.5))
    wealth_share_rich = float(np.sum(m[half:] * a[half:]) / np.sum(m * a))
    return {"b": b.tolist(), "r2": r2.tolist(), "rounds": len(history), "history": history, "K": Kt.tolist(),
            "K_rule": Kh.tolist(), "z": zpath.tolist(), "burn": burn, "dh_max": float(err.max()),
            "dh_mean": float(err.mean()), "one_step_max": float(one.max()), "a": a, "ap_mid": ap[:, i_mid, 3],
            "mps": mps, "D_last": D, "rich_half_share": wealth_share_rich, "K_mean": float(Kt[burn:].mean())}


# ---------------------------------------------------------------------------------------------------------------
# sequence-space Jacobians (Auclert, Bardoczy, Rognlie and Straub 2021) and a one-asset HANK


def _egm_step(c_next, r_next: float, r_now: float, Z_now: float, beta: float, gamma: float, e, P, a,
              a_min: float = 0.0):
    """One backward step: tomorrow's consumption rule and returns, today's return and income -> today's rules.
    Timing: c_t + a_t = (1 + r_t) a_{t-1} + Z_t e_t and u'(c_t) = beta E[(1 + r_{t+1}) u'(c_{t+1})]."""
    emu = (1 + r_next) * (S.up(c_next, gamma) @ P.T)
    c_end = S.up_inv(beta * emu, gamma)
    y = Z_now * np.asarray(e)
    a_end = (c_end + a[:, None] - y[None, :]) / (1 + r_now)
    c = np.empty_like(c_next)
    for s in range(len(y)):
        c[:, s] = np.interp(a, a_end[:, s], c_end[:, s])
        bind = a < a_end[0, s]
        c[bind, s] = (1 + r_now) * a[bind] + y[s] - a_min
    ap = (1 + r_now) * a[:, None] + y[None, :] - c
    return c, np.maximum(ap, a_min)


def _lottery(ap, a):
    idx = np.clip(np.searchsorted(a, ap, side="right") - 1, 0, len(a) - 2)
    w = np.clip((ap - a[idx]) / (a[idx + 1] - a[idx]), 0.0, 1.0)
    return idx, w


def _forward(D, idx, w, P):
    Dn = np.zeros_like(D)
    for s in range(D.shape[1]):
        np.add.at(Dn[:, s], idx[:, s], D[:, s] * (1 - w[:, s]))
        np.add.at(Dn[:, s], idx[:, s] + 1, D[:, s] * w[:, s])
    return Dn @ P


def _expect(X, idx, w, P):
    Y = X @ P.T
    cols = np.arange(X.shape[1])[None, :]
    return (1 - w) * Y[idx, cols] + w * Y[idx + 1, cols]


def hank_steady_state(target_A: float, r: float = 0.005, gamma: float = 1.0, rho_e: float = 0.966,
                      sd_e: float = 0.5, n_e: int = 7, n_a: int = 400, a_min: float = 0.0) -> dict:
    """A one-asset household block in steady state: output 1 a quarter, government bonds ``target_A`` (all the
    households' wealth), taxes r x B, after-tax income Z = 1 - r B, and the discount factor that makes households
    hold exactly the bonds."""
    e, P, pi = income_chain(rho_e, sd_e * np.sqrt(1 - rho_e ** 2), n_e)
    a = asset_grid(n_a, a_min, max(60.0, 25.0 * target_A), curve=3.0)
    Z = 1.0 - r * target_A
    lo, hi = 0.80, 1 / (1 + r) - 1e-7
    c = None
    for _ in range(60):
        beta = 0.5 * (lo + hi)
        h = household_general(np.full(n_e, 1 + r), Z * e, beta, gamma, P, a, a_min, c0=c)
        c = h["c"]
        D = stationary(h["ap"], a, P, pi)
        A = float(np.sum(D * h["ap"]))
        if A > target_A:
            hi = beta
        else:
            lo = beta
        if hi - lo < 1e-10:
            break
    h = household_general(np.full(n_e, 1 + r), Z * e, beta, gamma, P, a, a_min, c0=c, tol=1e-12)
    D = stationary(h["ap"], a, P, pi, tol=1e-14)
    m = mpcs(h["c"], a, 1 + r, 0.01)
    return {"beta": beta, "r": r, "Z": Z, "B": target_A, "gamma": gamma, "e": e, "P": P, "pi": pi, "a": a,
            "a_min": a_min, "c": h["c"], "ap": h["ap"], "D": D, "A": float(np.sum(D * h["ap"])),
            "C": float(np.sum(D * h["c"])), "mpc": m, "mean_mpc": float(np.sum(D * m)),
            "at_limit": float(D[0].sum())}


def jacobians(ss: dict, T: int = 300, h: float = 1e-4) -> dict:
    """The Jacobians of aggregate consumption C and assets A with respect to the paths of the return r and of
    after-tax income Z, T x T each, by the fake-news algorithm: one backward pass per input for the effect of
    news at each horizon on today's rules, expectation vectors for how a change in tomorrow's distribution
    shows up later, and a cumulative sum."""
    a, e, P, beta, gamma = ss["a"], ss["e"], ss["P"], ss["beta"], ss["gamma"]
    r, Z, D, c_ss, ap_ss = ss["r"], ss["Z"], ss["D"], ss["c"], ss["ap"]
    idx, w = _lottery(ap_ss, a)
    D1_ss = _forward(D, idx, w, P)
    outs = {"C": c_ss, "A": ap_ss}
    E = {}
    for o, base in outs.items():
        Ev = np.empty((T - 1,) + base.shape)
        Ev[0] = base
        for t in range(1, T - 1):
            Ev[t] = _expect(Ev[t - 1], idx, w, P)
        E[o] = Ev.reshape(T - 1, -1)
    J = {}
    for inp in ("r", "Z"):
        Ycur = {o: np.empty(T) for o in outs}
        Dcur = np.empty((T, D.size))
        cprev = None
        for u in range(T):
            if u == 0:
                c_u, ap_u = (_egm_step(c_ss, r, r + h, Z, beta, gamma, e, P, a, ss["a_min"]) if inp == "r" else
                             _egm_step(c_ss, r, r, Z + h, beta, gamma, e, P, a, ss["a_min"]))
            elif u == 1 and inp == "r":
                c_u, ap_u = _egm_step(cprev, r + h, r, Z, beta, gamma, e, P, a, ss["a_min"])
            else:
                c_u, ap_u = _egm_step(cprev, r, r, Z, beta, gamma, e, P, a, ss["a_min"])
            cprev = c_u
            Ycur["C"][u] = np.sum(D * (c_u - c_ss)) / h
            Ycur["A"][u] = np.sum(D * (ap_u - ap_ss)) / h
            i2, w2 = _lottery(ap_u, a)
            Dcur[u] = ((_forward(D, i2, w2, P) - D1_ss) / h).ravel()
        for o in outs:
            F = np.empty((T, T))
            F[0] = Ycur[o]
            F[1:] = E[o] @ Dcur.T
            Jo = F.copy()
            for t in range(1, T):
                Jo[t, 1:] += Jo[t - 1, :-1]
            J[(o, inp)] = Jo
    return {"J": J, "T": T}


def jacobian_column_brute(ss: dict, inp: str, s: int, T: int = 300, h: float = 1e-4) -> dict:
    """The same Jacobian column by brute force: shock the input at date s, solve every rule backward from T and move
    the distribution forward."""
    a, e, P, beta, gamma = ss["a"], ss["e"], ss["P"], ss["beta"], ss["gamma"]
    r, Z = ss["r"], ss["Z"]
    rp = np.full(T + 1, r)
    Zp = np.full(T, Z)
    if inp == "r":
        rp[s] += h
    else:
        Zp[s] += h
    cs, aps = [None] * T, [None] * T
    c = ss["c"]
    for t in range(T - 1, -1, -1):
        c, ap = _egm_step(c, rp[t + 1], rp[t], Zp[t], beta, gamma, e, P, a, ss["a_min"])
        cs[t], aps[t] = c, ap
    D = ss["D"]
    dC, dA = np.empty(T), np.empty(T)
    for t in range(T):
        dC[t] = (np.sum(D * cs[t]) - ss["C"]) / h
        dA[t] = (np.sum(D * aps[t]) - ss["A"]) / h
        i2, w2 = _lottery(aps[t], a)
        D = _forward(D, i2, w2, P)
    return {"C": dC, "A": dA}


def hank_rate_cut(ss: dict, jac: dict, size: float = -0.0025, persistence: float = 0.7) -> dict:
    """A cut in the real rate announced at date 0, first paid on assets at date 1, in a one-asset economy whose
    output is set by demand. Debt stays constant, so taxes fall with the interest bill (dT = B dr). Asset-market
    clearing (dA = 0) pins down after-tax income; output is income plus taxes. The consumption response is split
    into the direct effect of the rates (incomes held fixed) and the indirect effect through incomes (Kaplan, Moll
    and Violante 2018)."""
    J, T = jac["J"], jac["T"]
    dr = np.zeros(T)
    dr[1:] = size * persistence ** np.arange(T - 1)
    dT = ss["B"] * dr
    dZ = -np.linalg.solve(J[("A", "Z")], J[("A", "r")] @ dr)
    dY = dZ + dT
    direct = J[("C", "r")] @ dr
    indirect = J[("C", "Z")] @ dZ
    dC = direct + indirect
    return {"dr": dr, "dY": dY, "dC": dC, "direct": direct, "indirect": indirect, "dZ": dZ,
            "goods_residual": float(np.max(np.abs(dC - dY))),
            "direct_share_impact": float(direct[0] / dC[0]) if abs(dC[0]) > 0 else float("nan"),
            "direct_share_year": float(direct[:4].sum() / dC[:4].sum())}


def hank_multiplier(ss: dict, jac: dict, rho_g: float = 0.8, phi: float = 0.1, financing: str = "deficit") -> dict:
    """Government purchases dG = 0.01 rho_g^t with the real rate fixed. Balanced-budget: taxes rise with spending.
    Deficit: taxes follow debt, dT_t = phi dB_{t-1}. The discounted cumulative multiplier and the path of output."""
    J, T, r = jac["J"], jac["T"], ss["r"]
    dG = 0.01 * rho_g ** np.arange(T)
    dT, dB = np.zeros(T), np.zeros(T)
    if financing == "balanced":
        dT = dG.copy()
    else:
        for t in range(T):
            prev = dB[t - 1] if t > 0 else 0.0
            dT[t] = phi * prev
            dB[t] = (1 + r) * prev + dG[t] - dT[t]
    dZ = np.linalg.solve(J[("A", "Z")], dB)
    dY = dZ + dT
    dC = J[("C", "Z")] @ dZ
    q = (1 + r) ** -np.arange(T)
    return {"dG": dG, "dY": dY, "dC": dC, "dT": dT, "dB": dB, "multiplier": float(q @ dY / (q @ dG)),
            "impact": float(dY[0] / dG[0]), "goods_residual": float(np.max(np.abs(dY - dC - dG)))}


def impc(jac: dict, years: int = 6) -> np.ndarray:
    """Intertemporal MPCs: the share of a one-off income at date 0 spent in each year (four quarters) after."""
    col = jac["J"][("C", "Z")][:, 0]
    return np.array([col[4 * k:4 * k + 4].sum() for k in range(years)])


def ra_rate_cut(r: float, B: float, dr) -> dict:
    """The same rate cut for a representative household with log utility (beta (1 + r) = 1) holding the debt B.
    Total: with debt constant and output set by demand, consumption follows the Euler equation alone,
    dC_t = -sum_{k > t} dr_k / (1 + r). Direct: incomes held fixed, the Euler equation and the budget give
    dC_0 = (rB - 1)/(1 + r) sum_k q_k dr_k, then the same slope."""
    dr = np.asarray(dr, float)
    T = len(dr)
    q = (1 + r) ** -np.arange(T)
    tail = np.concatenate([np.cumsum(dr[::-1])[::-1][1:], [0.0]])
    total = -tail / (1 + r)
    c0 = (r * B - 1) / (1 + r) * np.sum(q * dr)
    direct = c0 + np.concatenate([[0.0], np.cumsum(dr[1:])]) / (1 + r)
    return {"dC": total, "direct": direct, "indirect": total - direct,
            "direct_share_impact": float(direct[0] / total[0]),
            "direct_share_year": float(direct[:4].sum() / total[:4].sum())}


# ---------------------------------------------------------------------------------------------------------------
# firms: Hopenhayn (1992), and lumpy investment


def hopenhayn(c_e: float = 40.0, c_f: float = 20.0, theta: float = 0.64, beta: float = 0.95, rho: float = 0.9,
              sigma: float = 0.2, n: int = 41, entrant_shift: float = 1.0, demand: float = 100.0) -> dict:
    """Hopenhayn's competitive industry in steady state. Firms with productivity phi (a Rouwenhorst chain in logs)
    hire labour at wage 1 to make phi n^theta, pay a fixed cost c_f each period they produce, and after producing
    decide whether to stay. Entrants pay c_e, then draw phi from a distribution ``entrant_shift`` standard
    deviations below the incumbents'. Free entry pins the price, demand (expenditure ``demand``) the mass of
    entrants. Returns the price, the exit threshold, entry and exit rates, the size distribution and how a
    cohort survives and grows with age."""
    zg, P = S.rouwenhorst(n, rho, sigma)
    phi = np.exp(zg)
    sd = sigma / np.sqrt(1 - rho ** 2)
    nu = np.exp(-0.5 * ((zg + entrant_shift * sd) / sd) ** 2)
    nu /= nu.sum()

    def solve_v(p):
        nl = (theta * p * phi) ** (1 / (1 - theta))
        prof = p * phi * nl ** theta - nl - c_f
        v = prof.copy()
        for _ in range(5000):
            cont = P @ v
            vn = prof + beta * np.maximum(cont, 0.0)
            if np.max(np.abs(vn - v)) < 1e-10:
                v = vn
                break
            v = vn
        return v, nl, prof, (P @ v) > 0

    lo, hi = 1e-3, 1e3
    for _ in range(200):
        p = np.sqrt(lo * hi)
        v, nl, prof, stay = solve_v(p)
        if nu @ v - c_e > 0:
            hi = p
        else:
            lo = p
        if hi / lo < 1 + 1e-12:
            break
    p = np.sqrt(lo * hi)
    v, nl, prof, stay = solve_v(p)
    A = (P * stay[:, None]).T
    mu_hat = np.linalg.solve(np.eye(n) - A, nu)
    q = phi * nl ** theta
    M = demand / (p * (mu_hat @ q))
    mu = M * mu_hat
    firms = float(mu.sum())
    exits = float(mu @ (~stay))
    cohort = [nu.copy()]
    for _ in range(40):
        cohort.append(A @ cohort[-1])
    surv = np.array([cz.sum() for cz in cohort])
    size_age = np.array([(cz @ nl) / max(cz.sum(), 1e-300) for cz in cohort])
    emp = mu * nl
    order = np.argsort(nl)
    cum_firms = np.cumsum(mu[order]) / firms
    cum_emp = np.cumsum(emp[order]) / emp.sum()
    big = nl >= np.percentile(np.repeat(nl, np.maximum((mu / mu.sum() * 1e5).astype(int), 0)), 90)
    thr = phi[stay].min() if stay.any() else float("nan")
    return {"p": float(p), "M": float(M), "firms": firms, "entry_rate": float(M / firms), "exit_rate": exits / firms,
            "phi": phi, "n_l": nl, "mu": mu, "stay": stay, "threshold": float(thr), "survival": surv,
            "size_by_age": size_age, "mean_size": float(emp.sum() / firms),
            "entrant_size": float(nu @ nl), "productivity": float((mu @ phi) / firms),
            "output_weighted_productivity": float((mu @ (phi * q)) / (mu @ q)),
            "employment": float(emp.sum()), "cum_firms": cum_firms, "cum_emp": cum_emp,
            "emp_share_big": float(emp[big].sum() / emp.sum()), "nu": nu}


def lumpy_plants(n: int = 20000, T: int = 120, delta: float = 0.1, band: float = 0.25, rho: float = 0.8,
                 sigma: float = 0.15, shock_at: int = 80, shock: float = 0.1, seed: int = 0) -> dict:
    """A sketch of (S,s) investment: each plant's desired log capital follows its own productivity; capital
    depreciates, and a plant invests only when its gap from the target exceeds ``band`` (a fixed cost of adjusting),
    then jumps to the target. Returns plant-level investment rates (mostly zero, sometimes large) and the smooth
    aggregate, with a common shock to desired capital at ``shock_at``. Not Khan and Thomas's model: a picture of
    why lumps can vanish in the sum."""
    rng = np.random.default_rng(seed)
    x = rng.normal(0, sigma / np.sqrt(1 - rho ** 2), n)
    k = x + rng.uniform(-band, band, n)
    plants = np.zeros((T, 5))
    agg = np.zeros(T)
    share_adj = np.zeros(T)
    common = 0.0
    for t in range(T):
        if t == shock_at:
            common = shock
        x = rho * x + rng.normal(0, sigma, n)
        k = k + np.log(1 - delta)
        target = x + common
        gap = target - k
        adj = np.abs(gap) > band
        inv = np.where(adj, np.exp(target) - np.exp(k), 0.0)
        rate = inv / np.exp(k)
        k = np.where(adj, target, k)
        plants[t] = rate[:5]
        agg[t] = inv.sum() / np.exp(k).sum()
        share_adj[t] = adj.mean()
    return {"plants": plants, "aggregate": agg, "share_adjusting": share_adj, "shock_at": shock_at}


__all__ = ["gorman_demand", "asset_grid", "income_chain", "household", "young_step", "stationary", "firm",
           "capital_demand", "gini", "top_share", "mpcs", "aiyagari", "aiyagari_types", "aiyagari_table", "simulate",
           "huggett_ct", "household_general", "aiyagari_returns", "pareto_tail", "pareto_from_shares", "ks_chain",
           "krusell_smith", "hank_steady_state", "jacobians", "jacobian_column_brute", "hank_rate_cut",
           "hank_multiplier", "impc", "ra_rate_cut", "hopenhayn", "lumpy_plants"]
