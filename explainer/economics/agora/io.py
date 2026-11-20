"""Agora's industrial organization (Part 43): measuring market power without seeing costs.

* **Structure and performance** (:func:`scp`): industries that all play Cournot, differing only in how unequal
  their firms' costs are; concentration and margins rise together although conduct is the same everywhere
  (Demsetz's objection to Bain).
* **Conduct** (:func:`conduct`): Bresnahan's (1982) identification: with parallel shifts of demand a competitive
  industry with rising marginal cost and a monopoly with flat cost produce the same prices and quantities; a demand
  rotation tells them apart.
* **Discrete choice** (:func:`logit_shares`, :func:`nested_shares`, :func:`rc_shares`, :func:`jacobian`): plain,
  nested and random-coefficient logit market shares with an outside good, and their price derivatives.
* **Pricing and mergers** (:func:`bertrand`, :func:`costs_from_prices`, :func:`merger`): multi-product
  Bertrand-Nash prices for any ownership, marginal costs recovered from observed prices, and the prices after a
  merger.
* **Estimation** (:func:`island_cars`, :func:`logit_ols`, :func:`logit_iv`, :func:`blp`): a simulated car market
  with known demand, plain logit by OLS and by IV with characteristics of rivals' products as instruments, and the
  random-coefficient estimator of Berry, Levinsohn and Pakes (1995) with Berry's contraction.
* **Production** (:func:`island_plants`, :func:`acf`, :func:`dlw_markups`): plants whose labour responds to
  productivity the econometrician cannot see; OLS against Ackerberg, Caves and Frazer's two-step estimator; markups
  from production data (De Loecker and Warzynski 2012).
* **Entry** (:func:`entry_thresholds`, :func:`island_towns`): Bresnahan and Reiss's (1991) population thresholds
  for one, two, three firms, under Cournot and under collusion.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, minimize_scalar


# ---------------------------------------------------------------------------------------------------------------
# structure, conduct, performance


def cournot_hetero(a: float, b: float, costs) -> np.ndarray:
    """Cournot quantities with linear inverse demand P = a - b Q and constant unit costs; firms that would produce
    nothing drop out."""
    c = np.asarray(costs, float)
    active = np.ones(len(c), bool)
    for _ in range(len(c)):
        n = active.sum()
        q = np.where(active, (a - (n + 1) * c + c[active].sum()) / ((n + 1) * b), 0.0)
        neg = active & (q <= 0)
        if not neg.any():
            break
        active &= ~neg
    return np.maximum(q, 0.0)


def scp(n_ind: int = 300, n_firms: int = 5, a: float = 10.0, b: float = 1.0, c0: float = 4.0,
        max_spread: float = 0.6, seed: int = 0) -> dict:
    """Industries alike in demand and in conduct (Cournot) whose firms' costs differ by a spread drawn for each
    industry.  For each industry: the Herfindahl index (shares in percent squared), the industry's price-cost
    margin (profits over revenue), and, pooled, the correlation between the two and the within-industry relation
    between a firm's share and its margin."""
    rng = np.random.default_rng(seed)
    hhi, pcm, share_all, margin_all = [], [], [], []
    for _ in range(n_ind):
        spread = rng.uniform(0, max_spread)
        c = c0 * np.exp(spread * rng.standard_normal(n_firms))
        q = cournot_hetero(a, b, c)
        Q = q.sum()
        p = a - b * Q
        s = q / Q
        hhi.append(float(np.sum((100 * s) ** 2)))
        pcm.append(float(np.sum((p - c) * q) / (p * Q)))
        on = q > 0
        share_all += list(s[on])
        margin_all += list((p - c[on]) / p)
    hhi, pcm = np.array(hhi), np.array(pcm)
    return {"hhi": hhi.tolist(), "pcm": pcm.tolist(), "corr": float(np.corrcoef(hhi, pcm)[0, 1]),
            "slope": float(np.polyfit(hhi, pcm, 1)[0]), "share": share_all, "margin": margin_all,
            "within_corr": float(np.corrcoef(share_all, margin_all)[0, 1])}


def conduct(shifts=(0.0, 1.0, 2.0), rotations=(0.0, 0.5), a0: float = 10.0, a1: float = 1.0) -> dict:
    """Bresnahan (1982).  Demand Q = a0 + y - (a1 + z) P, where y shifts demand in parallel and z rotates it.
    Industry A is competitive (price = marginal cost) with marginal cost c + d Q; industry B is a monopoly with
    flat marginal cost c'.  Chosen so that, for parallel shifts, the two produce identical (P, Q).  Returns the
    equilibria of both for each (shift, rotation)."""
    # competitive with mc = 2 + Q / 2: P = 2 + Q/2.  Monopoly with flat mc c': MR = (a0 + y - 2Q)/a1 = c'.
    # For a1 = 1, z = 0: competitive Q = (a0 + y - 2)/1.5; monopoly Q = (a0 + y - c')/2.  Equal slopes in y need the
    # monopoly's mc to rise with Q too; instead match exactly by giving A the supply curve P = cA + dA Q with
    # dA = 1/a1 (the slope that makes a price-taker mimic a monopolist facing slope 1/a1) and cA = cB.
    cB = 2.0
    out = {"A": [], "B": []}
    for z in rotations:
        for y in shifts:
            slope = a1 + z
            # A: competitive, P = cB + Q / a1  (marginal cost rises with output)
            QA = (a0 + y - slope * cB) / (1 + slope / a1)
            PA = cB + QA / a1
            # B: monopoly, flat mc cB: MR = (a0 + y - 2Q)/slope = cB
            QB = (a0 + y - slope * cB) / 2
            PB = (a0 + y - QB) / slope
            out["A"].append({"y": y, "z": z, "P": PA, "Q": QA})
            out["B"].append({"y": y, "z": z, "P": PB, "Q": QB})
    return out


# ---------------------------------------------------------------------------------------------------------------
# discrete choice


def logit_shares(delta) -> np.ndarray:
    """Shares of J inside goods with mean utilities delta and an outside good with utility zero."""
    d = np.asarray(delta, float)
    m = max(d.max(), 0.0)
    e = np.exp(d - m)
    return e / (np.exp(-m) + e.sum())


def nested_shares(delta, nests, sigma: float) -> np.ndarray:
    """Nested logit shares: products in nests (labels), nesting parameter sigma in [0, 1), outside good alone."""
    d = np.asarray(delta, float)
    g = np.asarray(nests)
    out = np.zeros_like(d)
    labels = np.unique(g)
    D = {k: np.sum(np.exp(d[g == k] / (1 - sigma))) for k in labels}
    denom = 1.0 + sum(D[k] ** (1 - sigma) for k in labels)
    for k in labels:
        m = g == k
        out[m] = np.exp(d[m] / (1 - sigma)) / D[k] * D[k] ** (1 - sigma) / denom
    return out


def rc_shares(delta, x, nu, sigma: float) -> np.ndarray:
    """Random-coefficient logit: consumer i's utility from j is delta_j + sigma nu_i x_j; shares are the average
    over the draws nu."""
    d = np.asarray(delta, float)[None, :] + sigma * np.outer(nu, x)
    m = np.maximum(d.max(axis=1, keepdims=True), 0.0)
    e = np.exp(d - m)
    s = e / (np.exp(-m) + e.sum(axis=1, keepdims=True))
    return s.mean(axis=0)


class RCMarket:
    """One market of a random-coefficient logit: consumer i's utility from j is base_j - alpha_i p_j, with
    alpha_i = alpha - sigma nu_i, plus an outside good worth zero.  Shares, their exact price derivatives, and
    Bertrand-Nash prices by Morrow and Skerlos's (2011) zeta-markup iteration."""

    def __init__(self, base, alpha: float, sigma: float, nu):
        self.base = np.asarray(base, float)
        self.ai = alpha - sigma * np.asarray(nu, float)     # each consumer's price sensitivity

    def individual(self, p):
        u = self.base[None, :] - self.ai[:, None] * np.asarray(p, float)[None, :]
        m = np.maximum(u.max(axis=1, keepdims=True), 0.0)
        e = np.exp(u - m)
        return e / (np.exp(-m) + e.sum(axis=1, keepdims=True))

    def shares(self, p):
        return self.individual(p).mean(axis=0)

    def jac(self, p):
        """J[j, k] = ds_k / dp_j."""
        si = self.individual(p)
        a = self.ai[:, None]
        G = (a * si).T @ si / len(self.ai)                  # mean of alpha_i s_ij s_ik
        L = np.mean(a * si, axis=0)                          # mean of alpha_i s_ij
        return G - np.diag(L)

    def bertrand(self, mc, owner, p0=None, tol: float = 1e-11, max_iter: int = 2000):
        mc = np.asarray(mc, float)
        own = np.asarray(owner)
        O = (own[:, None] == own[None, :]).astype(float)
        p = mc * 1.2 if p0 is None else np.asarray(p0, float).copy()
        for _ in range(max_iter):
            si = self.individual(p)
            a = self.ai[:, None]
            L = np.mean(a * si, axis=0)
            G = (a * si).T @ si / len(self.ai)
            s = si.mean(axis=0)
            zeta = ((O * G) @ (p - mc) + s) / L
            new = mc + zeta
            if np.max(np.abs(new - p)) < tol:
                return new
            p = new
        return p


def jacobian(share_fn, prices, h: float = 1e-6) -> np.ndarray:
    """ds_k/dp_j by central differences: rows j (the price changed), columns k (the share)."""
    p = np.asarray(prices, float)
    J = len(p)
    out = np.zeros((J, J))
    for j in range(J):
        up, dn = p.copy(), p.copy()
        up[j] += h
        dn[j] -= h
        out[j] = (share_fn(up) - share_fn(dn)) / (2 * h)
    return out


def elasticities(share_fn, prices) -> np.ndarray:
    """E[j, k]: the percent change in k's share for a 1% rise in j's price."""
    p = np.asarray(prices, float)
    s = share_fn(p)
    return jacobian(share_fn, p) * p[:, None] / s[None, :]


# ---------------------------------------------------------------------------------------------------------------
# pricing and mergers


def bertrand(share_fn, mc, owner, p0=None, tol: float = 1e-11, max_iter: int = 5000) -> np.ndarray:
    """Multi-product Bertrand-Nash prices: p = mc - (Omega * dS/dp')^{-1} s, where Omega[j, k] = 1 when j and k have
    the same owner; found by damped iteration on the first-order conditions."""
    mc = np.asarray(mc, float)
    own = np.asarray(owner)
    O = (own[:, None] == own[None, :]).astype(float)
    p = mc * 1.3 if p0 is None else np.asarray(p0, float).copy()
    for _ in range(max_iter):
        s = share_fn(p)
        Jm = jacobian(share_fn, p)          # J[j, k] = ds_k/dp_j
        A = O * Jm                          # firm's derivative of its own goods' shares
        markup = -np.linalg.solve(A, s)
        new = mc + markup
        if np.max(np.abs(new - p)) < tol:
            return new
        p = 0.5 * p + 0.5 * new
    return p


def costs_from_prices(share_fn, prices, owner) -> np.ndarray:
    """Marginal costs that make observed prices a Bertrand-Nash equilibrium for the given ownership."""
    p = np.asarray(prices, float)
    own = np.asarray(owner)
    O = (own[:, None] == own[None, :]).astype(float)
    return p + np.linalg.solve(O * jacobian(share_fn, p), share_fn(p))


def merger(share_fn, prices, owner, merging, tol: float = 1e-10) -> dict:
    """Simulate a merger: recover costs from pre-merger prices, give the ``merging`` products one owner, and solve
    for the new equilibrium.  Returns costs, prices before and after, the percent changes, the share-weighted price
    change, and the change in the Herfindahl index (shares of inside sales, in percent squared)."""
    p0 = np.asarray(prices, float)
    own = np.asarray(owner).copy()
    mc = costs_from_prices(share_fn, p0, own)
    new_owner = own.copy()
    tgt = own[merging[0]]
    for j in merging:
        new_owner[own == own[j]] = tgt
    p1 = bertrand(share_fn, mc, new_owner, p0=p0, tol=tol)
    s0, s1 = share_fn(p0), share_fn(p1)
    w = s0 / s0.sum()

    def hhi(owner_, s):
        ss = s / s.sum()
        return float(sum((100 * ss[owner_ == o].sum()) ** 2 for o in np.unique(owner_)))
    return {"mc": mc.tolist(), "p0": p0.tolist(), "p1": p1.tolist(), "dp": ((p1 / p0 - 1)).tolist(),
            "avg": float(np.sum(w * (p1 / p0 - 1))), "s0": s0.tolist(), "s1": s1.tolist(),
            "dhhi": hhi(new_owner, s0) - hhi(own, s0), "hhi0": hhi(own, s0)}


# ---------------------------------------------------------------------------------------------------------------
# estimation


def island_cars(T: int = 40, firms: int = 6, per_firm: int = 4, alpha: float = 0.6, sigma: float = 0.15,
                beta=(-4.0, 1.5, 1.0), gamma=(1.2, 0.3, 0.2), gamma_w: float = 0.5, sd_xi: float = 0.8,
                sd_omega: float = 0.15, ns: int = 300, seed: int = 0) -> dict:
    """A car market for T years: firms x per_firm models a year, each with two characteristics (size, power) and an
    unobserved quality xi that buyers see.  Utility of i for j: beta_0 + beta_1 size + beta_2 power - alpha p_j +
    sigma nu_i p_j + xi_j (a random coefficient on price, so price-sensitive and insensitive buyers differ).
    Marginal cost exp(gamma_0 + gamma_1 size + gamma_2 power + gamma_w w + omega), where w is an observed cost
    shifter (the price of the steel and labour the plant buys) and omega, unobserved, is correlated with xi (better
    cars cost more to build); prices are Bertrand-Nash.  Returns the products' data and the true elasticities."""
    rng = np.random.default_rng(seed)
    J = firms * per_firm
    nu = rng.standard_normal(ns)
    rows = []
    true_own = []
    for t in range(T):
        size = rng.uniform(0.5, 2.0, J)
        power = rng.uniform(0.5, 2.0, J)
        xi = sd_xi * rng.standard_normal(J)
        omega = sd_omega * rng.standard_normal(J) + 0.3 * xi
        w = 0.4 * rng.standard_normal(J)
        mc = np.exp(gamma[0] + gamma[1] * size + gamma[2] * power + gamma_w * w + omega)
        owner = np.repeat(np.arange(firms), per_firm)
        base = beta[0] + beta[1] * size + beta[2] * power + xi
        mk = RCMarket(base, alpha, sigma, nu)
        p = mk.bertrand(mc, owner)
        s = mk.shares(p)
        E = mk.jac(p) * p[:, None] / s[None, :]
        true_own += list(np.diag(E))
        for j in range(J):
            rows.append((t, owner[j], size[j], power[j], p[j], s[j], xi[j], mc[j], w[j]))
    arr = np.array(rows)
    return {"t": arr[:, 0].astype(int), "firm": arr[:, 1].astype(int), "size": arr[:, 2], "power": arr[:, 3],
            "price": arr[:, 4], "share": arr[:, 5], "xi": arr[:, 6], "mc": arr[:, 7], "w": arr[:, 8], "nu": nu,
            "true_own": np.array(true_own), "alpha": alpha, "sigma": sigma, "beta": beta, "J": J, "T": T}


def blp_instruments(t, firm, X) -> np.ndarray:
    """BLP's instruments: for each product, the sums of each characteristic over the firm's other products and over
    rivals' products in the same market."""
    t, firm = np.asarray(t), np.asarray(firm)
    X = np.asarray(X, float)
    Z = np.zeros((len(t), 2 * X.shape[1]))
    for m in np.unique(t):
        idx = np.where(t == m)[0]
        for i in idx:
            same = idx[(firm[idx] == firm[i]) & (idx != i)]
            other = idx[firm[idx] != firm[i]]
            Z[i, :X.shape[1]] = X[same].sum(axis=0)
            Z[i, X.shape[1]:] = X[other].sum(axis=0)
    return Z


def diff_instruments(t, X) -> np.ndarray:
    """Gandhi and Houde's differentiation instruments: for each product and characteristic, the sum over the other
    products in its market of the squared difference in that characteristic (how crowded its neighbourhood is)."""
    t = np.asarray(t)
    X = np.asarray(X, float)
    Z = np.zeros_like(X)
    for m in np.unique(t):
        idx = np.where(t == m)[0]
        for c in range(X.shape[1]):
            d = X[idx, c][:, None] - X[idx, c][None, :]
            Z[idx, c] = np.sum(d ** 2, axis=1)
    return Z


def _tsls(y, X, Z):
    """Two-stage least squares of y on X with instruments Z (X and Z include the exogenous columns)."""
    PZ = Z @ np.linalg.pinv(Z.T @ Z) @ Z.T
    b = np.linalg.solve(X.T @ PZ @ X, X.T @ PZ @ y)
    return b


def logit_ols(share, outshr, price, X) -> dict:
    """Plain logit by OLS: ln s_j - ln s_0 = X beta - alpha p + xi."""
    y = np.log(share) - np.log(outshr)
    Xf = np.column_stack([np.ones(len(y)), X, price])
    b = np.linalg.lstsq(Xf, y, rcond=None)[0]
    return {"coef": b.tolist(), "alpha": float(-b[-1])}


def logit_iv(share, outshr, price, X, Z) -> dict:
    """Plain logit by two-stage least squares, price instrumented by Z (the exogenous X are their own instruments).
    Returns the coefficients, alpha and the first stage's F statistic."""
    y = np.log(share) - np.log(outshr)
    n = len(y)
    Xf = np.column_stack([np.ones(n), X, price])
    Zf = np.column_stack([np.ones(n), X, Z])
    b = _tsls(y, Xf, Zf)
    # first stage F for the excluded instruments
    Xr = np.column_stack([np.ones(n), X])
    rr = price - Xr @ np.linalg.lstsq(Xr, price, rcond=None)[0]
    ru = price - Zf @ np.linalg.lstsq(Zf, price, rcond=None)[0]
    q = Z.shape[1]
    F = ((rr @ rr - ru @ ru) / q) / ((ru @ ru) / (n - Zf.shape[1]))
    return {"coef": b.tolist(), "alpha": float(-b[-1]), "F": float(F)}


def contraction(share, t, x_rc, nu, sigma: float, delta0=None, tol: float = 1e-12, max_iter: int = 5000):
    """Berry's contraction: delta <- delta + ln s - ln s_hat(delta), market by market."""
    share = np.asarray(share, float)
    t = np.asarray(t)
    delta = np.log(share) if delta0 is None else np.array(delta0, float)
    for m in np.unique(t):
        idx = t == m
        d = delta[idx]
        for _ in range(max_iter):
            new = d + np.log(share[idx]) - np.log(rc_shares(d, x_rc[idx], nu, sigma))
            if np.max(np.abs(new - d)) < tol:
                d = new
                break
            d = new
        delta[idx] = d
    return delta


def blp(share, t, price, X, Z, nu, bounds=(0.0, 1.5)) -> dict:
    """The BLP estimator with one random coefficient, on price: for each sigma, invert shares by the contraction,
    run 2SLS of delta on (1, X, price) with instruments (1, X, Z), and evaluate the GMM objective xi' Z W Z' xi with
    W = (Z'Z)^{-1}; minimize over sigma."""
    n = len(share)
    Xf = np.column_stack([np.ones(n), X, price])
    Zf = np.column_stack([np.ones(n), X, Z])
    W = np.linalg.pinv(Zf.T @ Zf)
    cache = {}

    def obj(sig):
        delta = contraction(share, t, price, nu, sig, delta0=cache.get("d"))
        cache["d"] = delta
        b = _tsls(delta, Xf, Zf)
        xi = delta - Xf @ b
        g = Zf.T @ xi
        cache[round(float(sig), 6)] = (b, delta)
        return float(g @ W @ g) / n
    r = minimize_scalar(obj, bounds=bounds, method="bounded", options={"xatol": 1e-4})
    sig = float(r.x)
    obj(sig)
    b, delta = cache[round(sig, 6)]
    return {"sigma": sig, "alpha": float(-b[-1]), "coef": b.tolist(), "delta": delta, "objective": float(r.fun)}


def own_elasticities_logit(alpha: float, price, share) -> np.ndarray:
    """Plain logit own-price elasticities: -alpha p (1 - s)."""
    return -alpha * np.asarray(price) * (1 - np.asarray(share))


def logit_markups(alpha: float, price, share, t, firm) -> np.ndarray:
    """Plain logit Bertrand markups (p - mc)/p for multi-product firms, market by market."""
    price, share = np.asarray(price, float), np.asarray(share, float)
    t, firm = np.asarray(t), np.asarray(firm)
    out = np.zeros(len(price))
    for m in np.unique(t):
        idx = np.where(t == m)[0]
        s, p = share[idx], price[idx]
        # ds_k/dp_j = -alpha s_j (1 - s_j) on the diagonal, alpha s_j s_k off it
        Jm = alpha * np.outer(s, s)
        np.fill_diagonal(Jm, -alpha * s * (1 - s))
        O = (firm[idx][:, None] == firm[idx][None, :]).astype(float)
        mk = -np.linalg.solve(O * Jm, s)
        out[idx] = mk / p
    return out


def logit_surplus(delta, alpha: float) -> float:
    """Expected consumer surplus per buyer under plain logit with an outside good: ln(1 + sum exp delta) / alpha."""
    d = np.asarray(delta, float)
    return float(np.log1p(np.sum(np.exp(d))) / alpha)


def nested_surplus(delta, nests, sigma: float, alpha: float) -> float:
    """The same for nested logit: ln(1 + sum over nests of D_g^(1 - sigma)) / alpha."""
    d = np.asarray(delta, float)
    g = np.asarray(nests)
    tot = sum(np.sum(np.exp(d[g == k] / (1 - sigma))) ** (1 - sigma) for k in np.unique(g))
    return float(np.log1p(tot) / alpha)


def implied_margins(share_fn, prices, owners: dict) -> dict:
    """Nevo's (2001) test.  For each assumed ownership (a name and an owner vector), the marginal costs that make the
    observed prices an equilibrium, and the implied price-cost margins (p - mc) / p.  Comparing them with margins
    measured some other way says which conduct fits."""
    p = np.asarray(prices, float)
    out = {}
    for name, own in owners.items():
        mc = costs_from_prices(share_fn, p, np.asarray(own))
        out[name] = ((p - mc) / p).tolist()
    return out


def cmcr(share_fn, prices, owner, merging) -> np.ndarray:
    """Werden's (1996) compensating marginal-cost reductions: the cut in each merging product's marginal cost (as a
    share of its pre-merger cost) that keeps every price where it was after the merger."""
    p = np.asarray(prices, float)
    own = np.asarray(owner).copy()
    mc0 = costs_from_prices(share_fn, p, own)
    new = own.copy()
    tgt = own[merging[0]]
    for j in merging:
        new[own == own[j]] = tgt
    mc1 = costs_from_prices(share_fn, p, new)
    return (mc0 - mc1) / mc0


def contraction_trace(share, x_rc, nu, sigma: float, iters: int = 60) -> dict:
    """Berry's contraction in one market, step by step: the largest change in delta at each iteration, starting from
    ln s_j - ln s_0 (the plain-logit answer)."""
    share = np.asarray(share, float)
    s0 = 1 - share.sum()
    d = np.log(share) - np.log(s0)
    steps, path = [], [d.copy()]
    for _ in range(iters):
        new = d + np.log(share) - np.log(rc_shares(d, x_rc, nu, sigma))
        steps.append(float(np.max(np.abs(new - d))))
        d = new
        path.append(d.copy())
    return {"steps": steps, "delta": d.tolist(), "start": path[0].tolist(),
            "path": [q.tolist() for q in path[:12]]}


# ---------------------------------------------------------------------------------------------------------------
# production


def island_plants(n: int = 1500, T: int = 10, bl: float = 0.6, bk: float = 0.3, rho: float = 0.8,
                  sd_eta: float = 0.2, sd_eps: float = 0.1, sd_lerr: float = 0.15, delta: float = 0.1,
                  seed: int = 0) -> dict:
    """Plants with value added y = bl l + bk k + omega + eps.  Productivity omega follows an AR(1) the plant sees and
    the econometrician does not.  Capital is chosen a year ahead (investment rises with omega); labour is chosen
    with omega in view, with an idiosyncratic shift (a wage or adjustment shock); materials, the proxy, are a
    function of (omega, k, l): m = omega + 0.5 k + 0.5 l.  Returns a panel."""
    rng = np.random.default_rng(seed)
    omega = rng.normal(0, sd_eta / np.sqrt(1 - rho ** 2), n)
    k = rng.normal(1.0, 0.5, n)
    rows = []
    for t in range(T):
        lerr = sd_lerr * rng.standard_normal(n)
        l = (np.log(bl) + omega + bk * k) / (1 - bl) * 0.6 + lerr
        m = omega + 0.5 * k + 0.5 * l
        eps = sd_eps * rng.standard_normal(n)
        y = bl * l + bk * k + omega + eps
        for i in range(n):
            rows.append((i, t, y[i], l[i], k[i], m[i], omega[i]))
        inv = 0.5 * omega + rng.normal(0, 0.1, n)
        k = np.log((1 - delta) * np.exp(k) + np.exp(inv + k - 1.5))
        omega = rho * omega + sd_eta * rng.standard_normal(n)
    a = np.array(rows)
    return {"i": a[:, 0].astype(int), "t": a[:, 1].astype(int), "y": a[:, 2], "l": a[:, 3], "k": a[:, 4],
            "m": a[:, 5], "omega": a[:, 6], "bl": bl, "bk": bk}


def _poly(*cols, degree: int = 2):
    """A full polynomial basis of the given degree in the columns (with a constant)."""
    from itertools import combinations_with_replacement
    X = [np.ones(len(cols[0]))]
    for d in range(1, degree + 1):
        for comb in combinations_with_replacement(range(len(cols)), d):
            X.append(np.prod([cols[c] for c in comb], axis=0))
    return np.column_stack(X)


def acf(P: dict, degree: int = 2) -> dict:
    """Ackerberg, Caves and Frazer (2015): stage one regresses y on a polynomial in (l, k, m) to purge eps; stage two
    finds (bl, bk) such that the innovation in omega, after an AR(1) on last year's omega, is uncorrelated with this
    year's capital and last year's labour.  Returns OLS and ACF estimates."""
    y, l, k, m, i, t = (np.asarray(P[c]) for c in ("y", "l", "k", "m", "i", "t"))
    Xo = np.column_stack([np.ones(len(y)), l, k])
    ols = np.linalg.lstsq(Xo, y, rcond=None)[0]
    B = _poly(l, k, m, degree=degree)
    phi = B @ np.linalg.lstsq(B, y, rcond=None)[0]
    # lags
    order = np.lexsort((t, i))
    i_, t_ = i[order], t[order]
    has_lag = np.r_[False, (i_[1:] == i_[:-1]) & (t_[1:] == t_[:-1] + 1)]
    cur = order[has_lag]
    lag = order[np.where(has_lag)[0] - 1]

    def moments(b):
        w = phi - b[0] * l - b[1] * k
        wc, wl = w[cur], w[lag]
        rho = np.polyfit(wl, wc, 1)
        xi = wc - np.polyval(rho, wl)
        return np.array([np.mean(xi * k[cur]), np.mean(xi * l[lag]), np.mean(xi * k[lag])])
    # the moments also vanish where omega loses all persistence, so search a grid of sensible elasticities first
    grid = [(a, c) for a in np.linspace(0.05, 1.0, 39) for c in np.linspace(0.0, 0.8, 33)]
    start = min(grid, key=lambda b: float(np.sum(moments(b) ** 2)))
    from scipy.optimize import least_squares
    r = least_squares(moments, x0=list(start), bounds=([0.0, 0.0], [1.0, 1.0]), xtol=1e-12, ftol=1e-12)
    return {"ols": {"bl": float(ols[1]), "bk": float(ols[2])}, "acf": {"bl": float(r.x[0]), "bk": float(r.x[1])},
            "true": {"bl": P["bl"], "bk": P["bk"]}}


def dlw_markups(theta_m: float, mu, rng_seed: int = 0, n: int = 2000) -> dict:
    """De Loecker and Warzynski (2012): with a flexible input whose output elasticity is theta_m, a cost-minimizing
    firm's markup is theta_m over the input's share of revenue.  Plants with markups ``mu`` (an array or a
    distribution's draws) spend theta_m / mu of revenue on the input; recovering mu needs theta_m."""
    mu = np.asarray(mu, float)
    share = theta_m / mu
    return {"share": share.tolist(), "mu_hat": (theta_m / share).tolist(),
            "mu_wrong": ((theta_m * 1.15) / share).tolist()}


# ---------------------------------------------------------------------------------------------------------------
# entry


def entry_thresholds(n_max: int = 5, F: float = 1.0, margin: float = 1.0, mode: str = "cournot") -> dict:
    """Population needed for N firms to break even when each pays a fixed cost F and the market's variable profit
    per head is shared: under Cournot with linear demand, per-firm profit per head is margin^2 / (N + 1)^2; under
    collusion the monopoly profit per head, margin^2 / 4, is split N ways.  Returns S_N, the per-firm thresholds
    S_N / N, and their ratios s_{N+1} / s_N (one means competition no longer intensifies)."""
    N = np.arange(1, n_max + 1)
    if mode == "cournot":
        per = margin ** 2 / (N + 1) ** 2
    else:
        per = margin ** 2 / 4 / N
    S = F / per
    s = S / N
    return {"N": N.tolist(), "S": S.tolist(), "per_firm": s.tolist(), "ratio": (s[1:] / s[:-1]).tolist()}


def island_towns(n: int = 400, F: float = 1.0, margin: float = 1.0, sd: float = 0.25, seed: int = 0,
                 margins=None, n_max: int = 8) -> dict:
    """Towns of different populations (thousands, log-uniform 0.5 to 40) and the number of firms that enter, each town
    with its own fixed-cost shock.  By default the thresholds are Cournot's; with ``margins`` (the market's variable
    profit per head when 1, 2, ... firms compete) the N-firm threshold is S_N = N F / margins[N - 1]."""
    rng = np.random.default_rng(seed)
    pop = np.exp(rng.uniform(np.log(0.5), np.log(40), n))
    shock = np.exp(sd * rng.standard_normal(n))
    if margins is None:
        th = np.array(entry_thresholds(n_max, F, margin)["S"])
    else:
        m = np.asarray(margins, float)
        th = np.arange(1, len(m) + 1) * F / m
    nfirms = np.array([int(np.sum(p >= th * f)) for p, f in zip(pop, shock)])
    return {"pop": pop.tolist(), "n": nfirms.tolist(), "thresholds": th.tolist(), "sd": sd}


def ordered_thresholds(pop, n, n_max: int | None = None) -> dict:
    """Bresnahan and Reiss's estimator, in its simplest form: N firms enter where ln(pop) - ln(S_N) exceeds a normal
    shock with standard deviation sd, so P(N >= k) = Phi((ln pop - ln S_k) / sd), an ordered probit in ln(pop).
    Returns the estimated S_k, the per-firm thresholds S_k / k, their ratios and sd."""
    from scipy.optimize import minimize
    from scipy.stats import norm

    lp = np.log(np.asarray(pop, float))
    n = np.asarray(n, int)
    K = int(n_max or n.max())
    n = np.minimum(n, K)

    def unpack(th):
        cuts = np.cumsum(np.r_[th[0], np.exp(th[1:K])])
        return cuts, np.exp(th[K])

    def nll(th):
        cuts, sd = unpack(th)
        c = np.r_[-np.inf, cuts, np.inf]
        hi = norm.cdf((lp - c[n]) / sd)           # P(N >= n)
        lo = norm.cdf((lp - c[n + 1]) / sd)       # P(N >= n + 1)
        return -np.sum(np.log(np.maximum(hi - lo, 1e-300)))
    start = np.r_[np.log(np.quantile(np.exp(lp), 0.2)), np.full(K - 1, np.log(0.5)), np.log(0.3)]
    r = minimize(nll, start, method="BFGS")
    cuts, sd = unpack(r.x)
    S = np.exp(cuts)
    per = S / np.arange(1, K + 1)
    return {"S": S.tolist(), "per_firm": per.tolist(), "ratio": (per[1:] / per[:-1]).tolist(), "sd": float(sd)}


def root(f, lo, hi):
    return float(brentq(f, lo, hi))
