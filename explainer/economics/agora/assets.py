"""Agora's asset prices and investment (Part 23 of *Economics, Built*): what a claim on the future is worth, and what
gets built.

* :func:`gordon`: the present value of a growing stream, ``D / (r - g)``, and its sensitivity to the discount rate.
* :func:`q_investment`: a firm with quadratic adjustment costs (Hayashi 1982): investment rises with marginal q, which
  equals average q; the path after a fall in the user cost of capital.
* :func:`option_to_wait`: irreversible investment when the project's value follows a geometric Brownian motion (McDonald
  and Siegel 1986; Dixit and Pindyck 1994): the threshold ``beta/(beta - 1)`` times the cost.
* :func:`mehra_prescott`: Mehra and Prescott's (1985) Lucas-tree economy with a two-state Markov chain for consumption
  growth: the risk-free rate, the return on equity and the premium for any patience and risk aversion; and
  :func:`mp_region`, the set of (risk-free rate, premium) pairs the model can produce.
* :func:`lognormal_tree`: the same with iid lognormal growth, in closed form.
* :func:`hj_bound`: Hansen and Jagannathan's (1991) bound: the volatility of the stochastic discount factor must exceed
  the Sharpe ratio; the risk aversion that power utility needs to reach it.
* :func:`disasters`: rare disasters (Rietz 1988; Barro 2006): a small yearly chance of a large fall in consumption.
* :func:`habit`: Campbell and Cochrane's (1999) surplus-consumption ratio and the price of risk it implies.
* :func:`ssw_market`: a stylized Smith-Suchanek-Williams (1988) laboratory market: a fifteen-period asset traded by
  fundamental traders and trend followers.

numpy only.
"""

from __future__ import annotations

import numpy as np


def gordon(D1: float, r: float, g: float) -> dict:
    """Price of a stream paying D1 next year and growing at g for ever, discounted at r > g; the percentage fall in
    price per point rise in r is 1/(r - g), the stream's duration."""
    if r <= g:
        raise ValueError("r must exceed g")
    P = D1 / (r - g)
    return {"price": P, "duration": 1 / (r - g), "price_up": D1 / (r + 0.01 - g),
            "fall_per_point": 1 - (r - g) / (r + 0.01 - g)}


def present_value(cash, r: float) -> float:
    cash = np.asarray(cash, float)
    return float(np.sum(cash / (1 + r) ** np.arange(1, len(cash) + 1)))


def user_cost(r: float, delta: float, inflation_k: float = 0.0, tax: float = 0.0, z: float = 0.0,
              p_k: float = 1.0) -> float:
    """Jorgenson's (1963) user cost of capital, ``p_K (r + delta - pi_K)(1 - tax z)/(1 - tax)``: the rental a firm
    must earn on a unit of capital to cover interest, depreciation and capital losses, after tax (z the present value
    of depreciation allowances per dollar)."""
    return p_k * (r + delta - inflation_k) * (1 - tax * z) / (1 - tax)


def q_investment(phi: float = 4.0, alpha: float = 0.33, r: float = 0.05, delta: float = 0.08, A0: float = 1.0,
                 A1: float = 1.2, years: int = 40, K0: float | None = None) -> dict:
    """Hayashi's firm: profit ``A K^alpha``, investment I with cost ``I + (phi/2) I^2 / K``.  With constant returns in
    the adjustment cost, ``I/K = (q - 1)/phi``, and q is the shadow value of a unit of capital, solved backward from the
    new steady state along the saddle path (forward shooting on the initial q).  At t = 0 productivity jumps from A0 to
    A1 (equivalently, the user cost falls); returns the paths of K, q and I/K."""
    def mpk(K, A):
        return alpha * A * K ** (alpha - 1)

    def steady(A):
        # in a steady state I/K = delta, q = 1 + phi delta, and r q = mpk + (phi/2) (I/K)^2 - delta q
        q = 1 + phi * delta
        target = (r + delta) * q - phi / 2 * delta ** 2
        return (target / (alpha * A)) ** (1 / (alpha - 1)), q
    Ks0, _ = steady(A0)
    Ks1, qs1 = steady(A1)
    K0 = Ks0 if K0 is None else K0

    def simulate(q0, T=years * 10, dt=0.1):
        K, q = K0, q0
        Ks, qs = [K], [q]
        for _ in range(T):
            ik = (q - 1) / phi
            dK = (ik - delta) * K
            dq = (r + delta) * q - mpk(K, A1) - phi / 2 * ik ** 2
            K, q = K + dt * dK, q + dt * dq
            Ks.append(K)
            qs.append(q)
            if not (0 < K < 50 * Ks1) or abs(q) > 50:
                break
        return np.array(Ks), np.array(qs)
    lo, hi = 1.0, 1 + 10 * phi
    for _ in range(80):
        mid = (lo + hi) / 2
        Ks, qs = simulate(mid)
        if Ks[-1] > Ks1 and qs[-1] > qs1 - 1e-9 or len(Ks) < years * 10 + 1 and Ks[-1] > Ks1:
            hi = mid
        else:
            lo = mid
    Ks, qs = simulate((lo + hi) / 2)
    n = min(len(Ks), years * 10 + 1)
    t = np.arange(n) * 0.1
    return {"t": t[::10].tolist(), "K": Ks[:n:10].tolist(), "q": qs[:n:10].tolist(),
            "ik": ((qs[:n:10] - 1) / phi).tolist(), "K_old": Ks0, "K_new": Ks1, "q_new": qs1, "q0": float(qs[0])}


def option_to_wait(r: float = 0.04, mu: float = 0.0, sigma: float = 0.2, cost: float = 1.0) -> dict:
    """A project worth V, following dV = mu V dt + sigma V dW, can be built once at cost I.  The value of waiting is
    ``A V^b`` with ``b`` the positive root of ``sigma^2 b(b-1)/2 + mu b - r = 0``; invest when ``V >= b/(b-1) I``
    (the NPV rule says ``V >= I``)."""
    a = 0.5 - mu / sigma ** 2
    b = a + np.sqrt(a * a + 2 * r / sigma ** 2)
    threshold = b / (b - 1) * cost
    return {"beta": float(b), "threshold": float(threshold), "multiple": float(threshold / cost)}


def mehra_prescott(beta: float, gamma: float, mu: float = 0.018, delta: float = 0.036, phi: float = 0.43) -> dict | None:
    """Mehra and Prescott's (1985) economy: consumption (the dividend) grows by ``1 + mu + delta`` or ``1 + mu -
    delta``, persisting with probability phi.  Equity is the claim to consumption.  Returns the average risk-free rate,
    equity return and premium (net, a year), or None if the price is infinite."""
    lam = np.array([1 + mu + delta, 1 + mu - delta])
    P = np.array([[phi, 1 - phi], [1 - phi, phi]])
    A = beta * P * lam[None, :] ** (1 - gamma)
    if np.max(np.abs(np.linalg.eigvals(A))) >= 1:
        return None
    w = np.linalg.solve(np.eye(2) - A, A @ np.ones(2))
    if np.any(w <= 0):
        return None
    Re = lam[None, :] * (w[None, :] + 1) / w[:, None]
    ERe = (P * Re).sum(axis=1)
    Rf = 1 / (beta * (P * lam[None, :] ** (-gamma)).sum(axis=1))
    pi = np.array([0.5, 0.5])
    re, rf = float(pi @ ERe) - 1, float(pi @ Rf) - 1
    return {"rf": rf, "re": re, "premium": re - rf, "pd": w.tolist()}


def mp_region(gammas, betas, **kw) -> dict:
    pts = []
    for g in gammas:
        for b in betas:
            m = mehra_prescott(b, g, **kw)
            if m is not None:
                pts.append((float(g), float(b), m["rf"], m["premium"]))
    return {"points": pts}


def lognormal_tree(beta: float, gamma: float, g: float = 0.02, sd: float = 0.036) -> dict:
    """iid lognormal consumption growth (log mean g, sd): risk-free rate ``-ln beta + gamma g - gamma^2 sd^2/2`` (log),
    and the claim to consumption's log premium ``gamma sd^2``."""
    rf = -np.log(beta) + gamma * g - gamma ** 2 * sd ** 2 / 2
    prem = gamma * sd ** 2
    return {"rf": float(np.exp(rf) - 1), "premium": float(prem)}


def hj_bound(sharpe: float, sd_g: float, gammas) -> dict:
    """The Hansen-Jagannathan bound ``sigma(m)/E(m) >= |E(R - Rf)| / sigma(R - Rf)``; with power utility and lognormal
    growth, ``sigma(m)/E(m) = sqrt(exp(gamma^2 sd^2) - 1)``; the smallest gamma that meets the bound."""
    gammas = np.asarray(gammas, float)
    ratio = np.sqrt(np.exp(gammas ** 2 * sd_g ** 2) - 1)
    need = float(np.sqrt(np.log(1 + sharpe ** 2)) / sd_g)
    return {"gamma": gammas.tolist(), "ratio": ratio.tolist(), "needed_gamma": need, "sharpe": sharpe}


def disasters(beta: float, gamma: float, g: float = 0.025, sd: float = 0.02, p: float = 0.017,
              sizes=(0.15, 0.25, 0.35, 0.50, 0.65), weights=(0.35, 0.25, 0.20, 0.12, 0.08), leverage: float = 1.0) -> dict:
    """Consumption growth ``exp(g + sd z)`` times ``(1 - b)`` in a disaster year (probability p, size b drawn from
    ``sizes``).  Equity pays consumption to the power ``leverage``.  Closed forms for iid growth: the risk-free rate,
    the equity return and the premium, a year (net)."""
    sizes, weights = np.asarray(sizes, float), np.asarray(weights, float)
    weights = weights / weights.sum()

    def E(power):
        # E[G^power] for G = exp(g + sd z) (1-b)^{disaster}
        normal = np.exp(power * g + power ** 2 * sd ** 2 / 2)
        return normal * (1 - p + p * np.sum(weights * (1 - sizes) ** power))
    Rf = 1 / (beta * E(-gamma))
    x = beta * E(leverage - gamma)
    if x >= 1:
        return None
    pd = x / (1 - x)
    Re = E(leverage) * (1 + pd) / pd
    return {"rf": float(Rf - 1), "re": float(Re - 1), "premium": float(Re - Rf), "mean_size": float(np.sum(weights * sizes))}


def habit(gamma: float = 2.0, phi: float = 0.87, g: float = 0.0189, sd: float = 0.015, years: int = 100,
          seed: int = 0) -> dict:
    """Campbell and Cochrane's (1999) surplus-consumption ratio S = (C - X)/C, with log s following
    ``s' = (1 - phi) s_bar + phi s + lambda(s)(dc - g)``, ``S_bar = sd sqrt(gamma/(1 - phi))``,
    ``lambda(s) = sqrt(1 - 2(s - s_bar))/S_bar - 1`` up to ``s_max``.  The conditional price of risk (the maximum
    Sharpe ratio) is ``gamma sd (1 + lambda(s))``: high when consumption is close to habit."""
    rng = np.random.default_rng(seed)
    Sbar = sd * np.sqrt(gamma / (1 - phi))
    sbar = np.log(Sbar)
    smax = sbar + (1 - Sbar ** 2) / 2

    def lam(s):
        return np.where(s <= smax, np.sqrt(np.maximum(1 - 2 * (s - sbar), 0)) / Sbar - 1, 0.0)
    s = sbar
    S, price, dc = [], [], []
    for _ in range(years):
        e = rng.normal(0, sd)
        s = (1 - phi) * sbar + phi * s + float(lam(s)) * e
        s = min(s, smax)
        S.append(float(np.exp(s)))
        price.append(float(gamma * sd * (1 + lam(s))))
        dc.append(g + e)
    return {"S": S, "price_of_risk": price, "dc": dc, "Sbar": float(Sbar), "smax": float(np.exp(smax)),
            "steady_price": float(gamma * sd / Sbar), "local_rra": [gamma / x for x in S]}


def ssw_market(periods: int = 15, dividends=(0.0, 0.08, 0.28, 0.60), share_trend: float = 0.7, n: int = 12,
               k: float = 0.9, start: float = 0.55, noise: float = 0.08, seed: int = 0) -> dict:
    """A stylized version of Smith, Suchanek and Williams's (1988) market: an asset paying one of ``dividends`` with
    equal chances each period for ``periods`` periods, so its fundamental value falls in a straight line to zero.  Each
    period every trader bids: fundamental traders bid the value, trend followers (a share ``share_trend``) bid last
    price plus ``k`` times its last change; the price is the median bid.  The first price is ``start`` times the value.
    An illustration of how extrapolation can carry a price above value and back, not a fit to their data."""
    rng = np.random.default_rng(seed)
    ed = float(np.mean(dividends))
    fv = [ed * (periods - t) for t in range(periods)]
    prices = [fv[0] * start]
    trend = rng.random(n) < share_trend
    for t in range(1, periods):
        change = prices[-1] - (prices[-2] if t > 1 else fv[0] * start * 0.8)
        bids = [max(prices[-1] + k * change + rng.normal(0, noise), 0.0) if trend[i]
                else max(fv[t] + rng.normal(0, noise), 0.0) for i in range(n)]
        prices.append(float(np.median(bids)))
    return {"fv": fv, "price": prices, "expected_dividend": ed, "trend_followers": int(trend.sum()), "n": n}
