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


# ===============================================================================================================
# Part 44 (io II): dynamics, platforms and antitrust
# ===============================================================================================================


# ---------------------------------------------------------------------------------------------------------------
# Rust (1987): when to rebuild a bus engine


def rust_panel(d: dict, groups=(1, 2, 3, 4), bin_miles: float = 5000.0, n_states: int = 90) -> dict:
    """Rust's states from his panel: for each bus-month, the mileage since the last replacement in bins of
    ``bin_miles`` (capped at n_states - 1), the decision (1 = rebuild the engine before next month), and the number
    of bins travelled to next month (from the old state, or from zero after a rebuild).  Also the mileage since the
    last replacement at each replacement."""
    g, bus, odo, rep = (np.asarray(d[c]) for c in ("group", "bus", "odometer", "replace"))
    xs, ds, dxs, at = [], [], [], []
    for gb in sorted({(a, b) for a, b in zip(g, bus) if a in groups}):
        idx = np.where((g == gb[0]) & (bus == gb[1]))[0]
        o, r = odo[idx].astype(float), rep[idx]
        base = 0.0
        for t in range(len(idx) - 1):
            m = o[t] - base
            x = min(int(m // bin_miles), n_states - 1)
            if r[t]:
                at.append(m + (o[t + 1] - o[t]) / 2)
                base = o[t] + (o[t + 1] - o[t]) / 2          # rebuilt during the month: about halfway
                x1 = min(int((o[t + 1] - base) // bin_miles), n_states - 1)
                dx = x1
            else:
                x1 = min(int((o[t + 1] - base) // bin_miles), n_states - 1)
                dx = x1 - x
            xs.append(x)
            ds.append(int(r[t]))
            dxs.append(int(max(dx, 0)))
    return {"x": np.array(xs), "d": np.array(ds), "dx": np.array(dxs), "at": np.array(at), "n_states": n_states,
            "bin": bin_miles}


def rust_transitions(dx, k: int = 3) -> np.ndarray:
    """The monthly probabilities of moving 0, 1, ..., k - 1 bins (the last pooling everything above)."""
    dx = np.minimum(np.asarray(dx), k - 1)
    return np.bincount(dx, minlength=k) / len(dx)


class Rust:
    """Harold Zurcher's problem.  Each month a bus in mileage state x either keeps its engine, paying the operating
    cost 0.001 theta1 x, or has it rebuilt for RC, which returns it to state 0; mileage then rises by j bins with
    probability p[j].  Choices carry independent extreme-value shocks, so the choice probabilities are logit in the
    two values.  ``ev`` solves the expected value function by contraction steps followed by Newton-Kantorovich
    steps, which keeps beta = 0.9999 fast."""

    def __init__(self, RC: float, theta1: float, p, beta: float = 0.9999, n: int = 90):
        self.RC, self.theta1, self.beta, self.n = float(RC), float(theta1), float(beta), int(n)
        self.p = np.asarray(p, float)
        P = np.zeros((n, n))
        for x in range(n):
            for j, pj in enumerate(self.p):
                P[x, min(x + j, n - 1)] += pj
        self.P = P
        self.x = np.arange(n)

    def cost(self):
        return 0.001 * self.theta1 * self.x

    def values(self, ev):
        v0 = -self.cost() + self.beta * ev
        v1 = -self.RC + self.beta * ev[0]
        return v0, v1

    def bellman(self, ev):
        v0, v1 = self.values(ev)
        m = np.maximum(v0, v1)
        logsum = m + np.log(np.exp(v0 - m) + np.exp(v1 - m))
        return self.P @ logsum

    def prob_replace(self, ev=None):
        ev = self.ev() if ev is None else ev
        v0, v1 = self.values(ev)
        return 1.0 / (1.0 + np.exp(v0 - v1))

    def ev(self, tol: float = 1e-12):
        ev = np.zeros(self.n)
        for _ in range(50):
            ev = self.bellman(ev)
        for _ in range(60):
            p1 = self.prob_replace(ev)
            J = self.beta * (self.P * (1 - p1)[None, :])      # d logsum(y) / d ev(y) = P0(y)
            J[:, 0] += self.beta * (self.P @ p1)               # and via ev(0), weight P1(y)
            F = ev - self.bellman(ev)
            step = np.linalg.solve(np.eye(self.n) - J, F)
            ev = ev - step
            if np.max(np.abs(step)) < tol:
                break
        return ev

    def loglik(self, x, d):
        p1 = self.prob_replace()
        p = np.where(np.asarray(d) == 1, p1[np.asarray(x)], 1 - p1[np.asarray(x)])
        return float(np.sum(np.log(np.maximum(p, 1e-300))))

    def average_cost(self, threshold: int) -> float:
        """Average monthly cost of the deterministic rule 'rebuild once mileage reaches ``threshold`` bins', in the
        same units as RC, from the stationary distribution of the chain it induces."""
        n = self.n
        Q = np.zeros((n, n))
        for x in range(n):
            src = 0 if x >= threshold else x
            for j, pj in enumerate(self.p):
                Q[x, min(src + j, n - 1)] += pj
        w, v = np.linalg.eig(Q.T)
        pi = np.real(v[:, np.argmin(np.abs(w - 1))])
        pi = pi / pi.sum()
        c = np.where(self.x >= threshold, self.RC, self.cost())
        return float(pi @ c)


def rust_nfxp(x, d, p, beta: float = 0.9999, start=(10.0, 2.0), n: int = 90) -> dict:
    """Rust's nested fixed point: maximize the likelihood of the decisions over (RC, theta1), solving the dynamic
    programme for every trial value."""
    from scipy.optimize import minimize

    def nll(th):
        if th[0] <= 0 or th[1] <= 0:
            return 1e10
        return -Rust(th[0], th[1], p, beta, n).loglik(x, d)
    r = minimize(nll, np.asarray(start, float), method="Nelder-Mead",
                 options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 2000})
    H = _num_hessian(nll, r.x)
    se = np.sqrt(np.diag(np.linalg.inv(H))) if np.all(np.linalg.eigvalsh(H) > 0) else np.full(2, np.nan)
    return {"RC": float(r.x[0]), "theta1": float(r.x[1]), "loglik": float(-r.fun), "se": se.tolist(),
            "evals": int(r.nfev)}


def _num_hessian(f, x, h: float = 1e-3):
    x = np.asarray(x, float)
    k = len(x)
    H = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            e_i, e_j = np.eye(k)[i] * h, np.eye(k)[j] * h
            H[i, j] = (f(x + e_i + e_j) - f(x + e_i - e_j) - f(x - e_i + e_j) + f(x - e_i - e_j)) / (4 * h * h)
    return (H + H.T) / 2


def rust_ccp(x, d, p, beta: float = 0.9999, n: int = 90, degree: int = 3) -> dict:
    """Hotz and Miller's conditional choice probabilities with Rust's renewal: estimate the probability of a
    rebuild at each mileage directly (a logit in a polynomial of mileage), then, because a rebuild resets every bus
    to the same state, v0(x) - v1 = -c(x) + RC + beta sum_j p_j [ln P1(j) - ln P1(x + j)], so (RC, theta1) come from
    one logit with a known offset; no dynamic programme is solved."""
    from scipy.optimize import minimize

    x = np.asarray(x)
    d = np.asarray(d)
    z = x / n
    B = np.column_stack([z ** k for k in range(degree + 1)])

    def nll1(b):
        e = B @ b
        return -np.sum(d * e - np.logaddexp(0, e))
    b = minimize(nll1, np.r_[-5.0, np.zeros(degree)], method="BFGS").x
    grid = np.arange(n) / n
    Bg = np.column_stack([grid ** k for k in range(degree + 1)])
    lp1 = -np.logaddexp(0, -(Bg @ b))                     # ln P1 on the grid
    pr = np.asarray(p, float)
    corr = np.array([sum(pj * (lp1[min(xx + j, n - 1)] - lp1[min(j, n - 1)]) for j, pj in enumerate(pr))
                     for xx in range(n)])

    def nll2(th):
        e = -th[0] + 0.001 * th[1] * x + beta * corr[x]       # v1 - v0
        return -np.sum(d * e - np.logaddexp(0, e))
    r = minimize(nll2, np.array([10.0, 2.0]), method="BFGS")
    return {"RC": float(r.x[0]), "theta1": float(r.x[1]), "p1_hat": np.exp(lp1).tolist()}


# ---------------------------------------------------------------------------------------------------------------
# dynamic oligopoly (Pakes and McGuire's version of Ericson and Pakes)


def pm_duopoly(K: int = 8, M: float = 5.0, a: float = 1.5, delta: float = 0.3, beta: float = 0.925,
               tol: float = 1e-9, max_iter: int = 5000) -> dict:
    """A symmetric Markov-perfect duopoly in qualities 0..K-1.  Each period a firm earns M times its logit share
    exp(w_i) / (1 + exp(w_i) + exp(w_j)), invests x at cost x so that its quality rises one step with probability
    a x / (1 + a x), and independently falls one step with probability delta.  Value and policy functions are found
    by iterating on the Bellman equation with the rival playing the current policy (Gauss-Jacobi)."""
    w = np.arange(K)
    pi = np.array([[M * np.exp(i) / (1 + np.exp(i) + np.exp(j)) for j in w] for i in w])
    V = pi / (1 - beta)
    X = np.zeros((K, K))

    def moves(xv):
        up = a * xv / (1 + a * xv)
        return up

    for it in range(max_iter):
        up_r = moves(X.T)                              # rival's chance of moving up, at (i, j) from j's view
        EV_up, EV_no = np.zeros((K, K)), np.zeros((K, K))
        for i in range(K):
            for j in range(K):
                def ev(ii):
                    tot = 0.0
                    for uj, pu in ((1, up_r[i, j]), (0, 1 - up_r[i, j])):
                        for dj, pd in ((1, delta), (0, 1 - delta)):
                            for di, pdi in ((1, delta), (0, 1 - delta)):
                                ni = min(max(ii - di, 0), K - 1)
                                nj = min(max(j + uj - dj, 0), K - 1)
                                tot += pu * pd * pdi * V[ni, nj]
                    return tot
                EV_up[i, j] = ev(min(i + 1, K - 1))
                EV_no[i, j] = ev(i)
        gain = beta * np.maximum(EV_up - EV_no, 0.0)
        Xn = np.maximum((np.sqrt(a * gain) - 1) / a, 0.0)
        up = moves(Xn)
        Vn = pi - Xn + beta * (up * EV_up + (1 - up) * EV_no)
        err = max(np.max(np.abs(Vn - V)), np.max(np.abs(Xn - X)))
        V, X = Vn, 0.5 * X + 0.5 * Xn
        if err < tol:
            break
    return {"V": V, "X": X, "pi": pi, "iterations": it + 1, "K": K, "a": a, "delta": delta, "beta": beta}


def pm_simulate(eq: dict, T: int = 2000, start=(0, 0), seed: int = 0) -> np.ndarray:
    """A path of the two qualities under the equilibrium policies."""
    rng = np.random.default_rng(seed)
    K, a, delta = eq["K"], eq["a"], eq["delta"]
    X = eq["X"]
    i, j = start
    out = np.zeros((T, 2), int)
    for t in range(T):
        xi, xj = X[i, j], X[j, i]
        ui = rng.random() < a * xi / (1 + a * xi)
        uj = rng.random() < a * xj / (1 + a * xj)
        di, dj = rng.random() < delta, rng.random() < delta
        i = min(max(i + ui - di, 0), K - 1)
        j = min(max(j + uj - dj, 0), K - 1)
        out[t] = (i, j)
    return out


# ---------------------------------------------------------------------------------------------------------------
# vertical relations, platforms, networks


def double_marginalization(a: float = 10.0, c: float = 2.0) -> dict:
    """Linear demand P = a - Q, a manufacturer with cost c and a retailer: integrated, the price is (a + c)/2;
    separated, the manufacturer charges w = (a + c)/2 and the retailer adds its own markup, (a + w)/2."""
    pi_int = (a - c) ** 2 / 4
    w = (a + c) / 2
    p_sep = (a + w) / 2
    q_sep = a - p_sep
    return {"p_int": (a + c) / 2, "q_int": (a - c) / 2, "profit_int": pi_int, "w": w, "p_sep": p_sep, "q_sep": q_sep,
            "profit_m": (w - c) * q_sep, "profit_r": (p_sep - w) * q_sep, "cs_int": ((a - c) / 2) ** 2 / 2,
            "cs_sep": q_sep ** 2 / 2}


def platform(a1: float, a2: float, alpha1: float, alpha2: float, c1: float = 0.0, c2: float = 0.0) -> dict:
    """A monopoly platform with two sides (Armstrong 2006, linear version): participation n1 = a1 + alpha1 n2 - p1
    and n2 = a2 + alpha2 n1 - p2, where alpha_i is what a member of side i gains from each member of the other side.
    The platform maximizes (p1 - c1) n1 + (p2 - c2) n2; each price equals cost plus a markup minus the value the
    side's members bring to the other side, alpha_j n_j."""
    A = np.array([[1.0, -alpha1], [-alpha2, 1.0]])
    Ai = np.linalg.inv(A)
    a = np.array([a1, a2])
    c = np.array([c1, c2])
    # profit (p - c)' Ai (a - p); FOC: Ai (a - p) - Ai' (p - c) = 0
    M = Ai + Ai.T
    p = np.linalg.solve(M, Ai @ a + Ai.T @ c)
    n = Ai @ (a - p)
    return {"p": p.tolist(), "n": n.tolist(), "profit": float((p - c) @ n),
            "subsidy": [float(alpha2 * n[1]), float(alpha1 * n[0])]}


def inferior_lockin(quality: float = 0.3, network: float = 0.05, adopters: int = 600, runs: int = 400,
                    seed: int = 0) -> dict:
    """Adopters arrive one at a time; each likes technology B better than A by ``quality`` on average (tastes are
    normal with sd 1), and gains ``network`` for every earlier adopter of the same technology.  A starts with a
    head start of 20 adopters (it came first).  Returns how often the inferior A ends up with most adopters."""
    rng = np.random.default_rng(seed)
    wins_a, paths = 0, []
    for r in range(runs):
        na, nb = 20, 0
        path = []
        for k in range(adopters):
            taste = rng.normal(quality, 1.0)                 # B's advantage for this adopter
            if taste + network * nb > network * na:
                nb += 1
            else:
                na += 1
            path.append(na / (na + nb))
        wins_a += na > nb
        if r < 12:
            paths.append(path)
    return {"share_a_wins": wins_a / runs, "paths": paths}


# ---------------------------------------------------------------------------------------------------------------
# competition and innovation


def arrow_replacement(a: float = 10.0, c: float = 4.0, c_new: float = 2.0) -> dict:
    """Arrow (1962): the gain from a process innovation lowering unit cost from c to c_new under linear demand
    P = a - Q, to a monopolist (its profit rises from pi_m(c) to pi_m(c_new)) and to an innovator in a competitive
    (Bertrand) industry, who earns the monopoly profit at the new cost if the innovation is drastic and otherwise
    undercuts at price c."""
    pim = lambda k: (a - k) ** 2 / 4   # noqa: E731
    drastic = (a + c_new) / 2 <= c
    comp = pim(c_new) if drastic else (c - c_new) * (a - c)
    return {"monopoly": pim(c_new) - pim(c), "competitive": comp, "planner": ((a - c_new) ** 2 - (a - c) ** 2) / 2,
            "drastic": bool(drastic)}


def step_by_step(delta: float, pi1: float = 1.0, r: float = 0.05, h: float = 0.1) -> dict:
    """Aghion, Bloom, Blundell, Griffith and Howitt's (2005) step-by-step industries, solved numerically.  An
    industry is either neck and neck (each firm earns (1 - delta) pi1: at delta = 0 they collude perfectly) or
    unlevelled (the leader earns pi1, the laggard nothing).  Firms choose Poisson innovation rates at cost n^2 / 2;
    a neck-and-neck innovator becomes the leader; a laggard who innovates (or imitates at rate h) catches up.
    ``delta`` is the intensity of competition.  Returns the innovation rates, the share of neck-and-neck
    industries in the steady state and aggregate innovation."""
    pi0 = (1 - delta) * pi1
    # values: V1 leader, V0 neck, Vm laggard; r V1 = pi1 + (nm + h)(V0 - V1)
    # r V0 = pi0 + n0 (V1 - V0) + n0' (Vm - V0) - n0^2/2, with n0 = V1 - V0 (symmetric: rival's rate n0 too)
    # r Vm = 0 + (nm + h)(V0 - Vm) - nm^2 / 2, nm = V0 - Vm
    from scipy.optimize import fsolve

    def eqs(v):
        V1, V0, Vm = v
        n0 = max(V1 - V0, 0.0)
        nm = max(V0 - Vm, 0.0)
        return [r * V1 - (pi1 + (nm + h) * (V0 - V1)),
                r * V0 - (pi0 + n0 * (V1 - V0) + n0 * (Vm - V0) - n0 ** 2 / 2),
                r * Vm - ((nm + h) * (V0 - Vm) - nm ** 2 / 2)]
    V1, V0, Vm = fsolve(eqs, [pi1 / r, pi0 / r, 0.0])
    n0 = max(V1 - V0, 0.0)
    nm = max(V0 - Vm, 0.0)
    mu1 = 2 * n0 / (2 * n0 + nm + h)          # share unlevelled: flows 2 n0 mu0 = (nm + h) mu1
    mu0 = 1 - mu1
    return {"n0": float(n0), "nm": float(nm), "mu0": float(mu0), "mu1": float(mu1),
            "innovation": float(2 * mu0 * n0 + mu1 * nm)}


def killer(pi_one: float = 100.0, pi_two: float = 110.0, pi_duo: float = 40.0, cost: float = 30.0) -> dict:
    """Cunningham, Ederer and Ma's logic in numbers: a start-up's drug competes with an incumbent's.  Developing it
    costs ``cost``.  Alone, the start-up earns the duopoly profit pi_duo; owned by the incumbent, the new drug adds
    only pi_two - pi_one, because it steals the incumbent's own sales."""
    return {"entrant_develops": pi_duo > cost, "incumbent_develops": pi_two - pi_one > cost,
            "entrant_gain": pi_duo - cost, "incumbent_gain": pi_two - pi_one - cost,
            "pay_up_to": (pi_one - pi_duo) + max(pi_duo - cost, 0.0)}


# ---------------------------------------------------------------------------------------------------------------
# algorithms that learn to collude (after Calvano, Calzolari, Denicolo and Pastorello 2020)


def logit_bertrand(prices, a=(2.0, 2.0), a0: float = 0.0, mu: float = 0.25, c=(1.0, 1.0)) -> tuple:
    """Two firms with logit demand q_i = e^((a_i - p_i)/mu) / (sum_j e^((a_j - p_j)/mu) + e^(a0/mu)); profits."""
    p = np.asarray(prices, float)
    a, c = np.asarray(a, float), np.asarray(c, float)
    e = np.exp((a - p) / mu)
    q = e / (e.sum() + np.exp(a0 / mu))
    return q, (p - c) * q


def logit_nash_monopoly(a=(2.0, 2.0), a0: float = 0.0, mu: float = 0.25, c=(1.0, 1.0)) -> tuple:
    from scipy.optimize import minimize, minimize_scalar

    p = np.array([1.5, 1.5])
    for _ in range(500):
        new = p.copy()
        for i in range(2):
            def neg(pi_, i=i):
                pp = new.copy()
                pp[i] = pi_
                return -logit_bertrand(pp, a, a0, mu, c)[1][i]
            new[i] = minimize_scalar(neg, bounds=(c[i], 5), method="bounded").x
        if np.max(np.abs(new - p)) < 1e-10:
            break
        p = new
    m = minimize(lambda q: -logit_bertrand(q, a, a0, mu, c)[1].sum(), np.array([1.9, 1.9]), method="Nelder-Mead",
                 options={"xatol": 1e-10, "fatol": 1e-12}).x
    return p, m


def q_learning(n_prices: int = 15, xi: float = 0.1, alpha: float = 0.15, beta: float = 4e-6, delta: float = 0.95,
               max_iter: int = 2_000_000, stable: int = 100_000, seed: int = 0) -> dict:
    """Two Q-learning price setters with one-period memory (the state is last period's pair of prices) in the
    logit Bertrand game, prices on a grid from the Nash price less xi times the Nash-monopoly gap to the monopoly
    price plus the same; exploration falls as exp(-beta t).  Stops when both greedy strategies have not changed for
    ``stable`` periods.  Returns the limit prices, the profit gain (0 at Nash, 1 at monopoly) and the strategies."""
    rng = np.random.default_rng(seed)
    pN, pM = logit_nash_monopoly()
    gap = pM[0] - pN[0]
    grid = np.linspace(pN[0] - xi * gap, pM[0] + xi * gap, n_prices)
    m = n_prices
    prof = np.zeros((m, m, 2))
    for i in range(m):
        for j in range(m):
            prof[i, j] = logit_bertrand([grid[i], grid[j]])[1]
    # initial Q: discounted payoff against a uniformly random rival
    Q = np.zeros((2, m * m, m))
    for k in range(2):
        for a_ in range(m):
            Q[k, :, a_] = (prof[a_, :, 0].mean() if k == 0 else prof[:, a_, 1].mean()) / (1 - delta)
    s = int(rng.integers(m * m))
    greedy = Q.argmax(axis=2)
    same = 0
    t = 0
    u = rng.random((2, 4096))
    acts = rng.integers(m, size=(2, 4096))
    for t in range(max_iter):
        if t % 4096 == 0 and t:
            u = rng.random((2, 4096))
            acts = rng.integers(m, size=(2, 4096))
        k_ = t % 4096
        eps = np.exp(-beta * t)
        a0 = acts[0, k_] if u[0, k_] < eps else int(Q[0, s].argmax())
        a1 = acts[1, k_] if u[1, k_] < eps else int(Q[1, s].argmax())
        s2 = a0 * m + a1
        r0, r1 = prof[a0, a1]
        Q[0, s, a0] += alpha * (r0 + delta * Q[0, s2].max() - Q[0, s, a0])
        Q[1, s, a1] += alpha * (r1 + delta * Q[1, s2].max() - Q[1, s, a1])
        g0, g1 = int(Q[0, s].argmax()), int(Q[1, s].argmax())
        if g0 == greedy[0, s] and g1 == greedy[1, s]:
            same += 1
        else:
            greedy[0, s], greedy[1, s] = g0, g1
            same = 0
        s = s2
        if same >= stable:
            break
    G = Q.argmax(axis=2)
    # play the greedy strategies from the last state until a cycle
    seen, path = {}, []
    st = s
    for k in range(200):
        if st in seen:
            break
        seen[st] = k
        a0, a1 = G[0, st], G[1, st]
        path.append((a0, a1))
        st = a0 * m + a1
    cyc = path[seen[st]:] if st in seen else path[-10:]
    pc = np.array([[grid[a0], grid[a1]] for a0, a1 in cyc])
    pf = np.array([prof[a0, a1] for a0, a1 in cyc])
    piN = logit_bertrand(pN)[1].mean()
    piM = logit_bertrand(pM)[1].mean()
    gain = (pf.mean() - piN) / (piM - piN)
    return {"grid": grid.tolist(), "nash": float(pN[0]), "monopoly": float(pM[0]), "iterations": t + 1,
            "prices": pc.mean(axis=0).tolist(), "gain": float(gain), "G": G, "cycle": [list(map(int, c)) for c in cyc],
            "state": int(st)}


def q_deviation(res: dict, periods: int = 15) -> dict:
    """Impulse response: from the converged cycle, firm 1 deviates once to its static best response to firm 2's
    price; both then follow their learned greedy strategies."""
    grid = np.array(res["grid"])
    m = len(grid)
    G = res["G"]
    a0, a1 = res["cycle"][0]
    prof = lambda i, j: logit_bertrand([grid[i], grid[j]])[1]   # noqa: E731
    br = int(np.argmax([prof(i, a1)[0] for i in range(m)]))
    path = [(a0, a1), (br, a1)]
    st = br * m + a1
    for _ in range(periods):
        b0, b1 = int(G[0, st]), int(G[1, st])
        path.append((b0, b1))
        st = b0 * m + b1
    return {"p1": [float(grid[p[0]]) for p in path], "p2": [float(grid[p[1]]) for p in path]}


# ---------------------------------------------------------------------------------------------------------------
# regulating a firm that knows more than you (Baron and Myerson 1982, two types)


def baron_myerson(a: float = 10.0, c_lo: float = 2.0, c_hi: float = 4.0, nu: float = 0.5, weight: float = 0.6) -> dict:
    """A regulator buys output from a firm whose unit cost is c_lo (probability nu) or c_hi, with demand P = a - q.
    It maximizes consumer surplus plus ``weight`` times the firm's profit, paying the transfers that make each type
    willing to report truthfully.  The low-cost type produces efficiently; the high-cost type's output is cut so as
    to shrink the low type's information rent."""
    q_lo = a - c_lo
    q_hi_full = a - c_hi
    # virtual cost: c_hi + nu/(1 - nu) (1 - weight) (c_hi - c_lo)
    virtual = c_hi + nu / (1 - nu) * (1 - weight) * (c_hi - c_lo)
    q_hi = max(a - virtual, 0.0)
    rent = (c_hi - c_lo) * q_hi
    return {"q_lo": q_lo, "q_hi": q_hi, "q_hi_full": q_hi_full, "p_hi": a - q_hi, "p_hi_full": c_hi,
            "virtual": virtual, "rent": rent, "rent_full": (c_hi - c_lo) * q_hi_full}
