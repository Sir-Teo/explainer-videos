"""Agora's ideas (Part 21 of *Economics, Built*): growth from non-rival ideas, creative destruction and the direction
of technical change.

* :func:`replication`: why ideas bring increasing returns: doubling capital and labour doubles output for a given
  stock of ideas; doubling the ideas too more than doubles it.
* :func:`ak_path`: the AK model, ``Y = A K``, growing at ``s A - delta`` for ever.
* :func:`romer_bgp`, :func:`romer_path`: Romer's (1990) economy of expanding varieties: final output
  ``L_Y^(1-alpha) sum_i x_i^alpha``, monopolists who rent capital and price at a markup, researchers who add
  ``delta A`` ideas a year each; on the balanced path ``g = (alpha delta L - rho) / (alpha + theta)``, which rises with
  the size of the labour force (the scale effect).
* :func:`ah_research`, :func:`ah_ladder`: Aghion and Howitt's (1992) quality ladder: research labour n finds an
  innovation at rate ``lam n``; each multiplies productivity by gamma and destroys the incumbent's monopoly.  The
  decentralized research (risk-neutral households, as in their paper) against a planner with log utility; small steps
  bring too much research (business stealing), large ones too little (spillovers to the next innovator).
* :func:`semi_endogenous`: Jones's (1995) variant, ``A_dot = theta L_A^lam A^phi`` with ``phi < 1``: long-run growth
  ``lam n / (1 - phi)`` set by the growth of research labour, not its level.
* :func:`directed`: Acemoglu's (2002) directed technical change: the skill premium's response to the relative supply
  of skills, holding technology fixed and letting it respond.

numpy only.
"""

from __future__ import annotations

import numpy as np


def replication(K: float = 1.0, L: float = 1.0, A: float = 1.0, alpha: float = 1 / 3) -> dict:
    """Output ``A K^alpha L^(1-alpha)`` at the base point, with K and L doubled, and with K, L and A doubled."""
    def f(k, l, a):
        return a * k ** alpha * l ** (1 - alpha)
    base = f(K, L, A)
    return {"base": base, "double_KL": f(2 * K, 2 * L, A) / base, "double_KLA": f(2 * K, 2 * L, 2 * A) / base}


def ak_path(s: float = 0.2, A: float = 0.4, delta: float = 0.05, years: int = 60, k0: float = 1.0) -> dict:
    """``K' = K + s A K - delta K``: growth at ``s A - delta`` from the first year, with no steady state."""
    k = [k0]
    for _ in range(years):
        k.append(k[-1] * (1 + s * A - delta))
    return {"t": list(range(years + 1)), "K": k, "growth": s * A - delta}


# ---------------------------------------------------------------------------------------------------------------
# Romer (1990)

def romer_bgp(L: float = 1.0, delta: float = 0.06, alpha: float = 0.5, rho: float = 0.02, theta: float = 1.0) -> dict:
    """The balanced growth path.  Researchers earn the value of the ideas they find, ``delta A V`` with
    ``V = pi / r`` and ``pi = alpha (1 - alpha) Y / A``; equal to the final-goods wage ``(1 - alpha) Y / L_Y``, so
    ``L_Y = r / (alpha delta)``.  With ``g = delta L_A`` and ``r = rho + theta g``:
    ``g = (alpha delta L - rho) / (alpha + theta)``."""
    g = max(0.0, (alpha * delta * L - rho) / (alpha + theta))
    r = rho + theta * g
    LY = min(L, r / (alpha * delta))
    return {"g": g, "r": r, "L_Y": LY, "L_A": L - LY, "share_research": (L - LY) / L, "markup": 1 / alpha}


def romer_path(L: float = 1.0, delta: float = 0.06, alpha: float = 0.5, rho: float = 0.02, theta: float = 1.0,
               years: int = 80, A0: float = 1.0) -> dict:
    """Ideas and output on the balanced path, year by year: ``A' = A (1 + delta L_A)``; output per worker grows with
    A (capital per idea constant on the path)."""
    b = romer_bgp(L, delta, alpha, rho, theta)
    A = [A0]
    for _ in range(years):
        A.append(A[-1] * (1 + delta * b["L_A"]))
    return {"t": list(range(years + 1)), "A": A, **b}


def romer_scale(Ls, **kw) -> dict:
    """Balanced growth for each size of labour force: the scale effect."""
    return {"L": list(Ls), "g": [romer_bgp(L=float(L), **kw)["g"] for L in Ls]}


# ---------------------------------------------------------------------------------------------------------------
# Aghion and Howitt (1992)

def ah_research(lam: float = 1.0, gamma: float = 1.5, alpha: float = 0.5, rho: float = 0.05, L: float = 1.0) -> dict:
    """Research labour n, manufacturing x = L - n (one unit of labour makes one unit of the intermediate).  The
    monopolist prices at the markup 1/alpha, so its profit is ``(1 - alpha)/alpha * w x``.  A researcher earns lam
    times the value of the next patent, whose profits are gamma times larger and last until the next innovation:
    ``w = lam gamma pi / (r + lam n)``.  With risk-neutral households (r = rho), as in Aghion and Howitt:
    ``n = (lam gamma (1 - alpha) L - alpha rho) / (lam (alpha + gamma (1 - alpha)))``.  A planner with log utility
    maximizes ``(alpha ln x)/rho + lam n ln(gamma)/rho^2``: ``n* = L - alpha rho / (lam ln gamma)``.  Expected
    growth of log output is ``lam n ln gamma``."""
    n_dec = (lam * gamma * (1 - alpha) * L - alpha * rho) / (lam * (alpha + gamma * (1 - alpha)))
    n_dec = float(np.clip(n_dec, 0.0, L))
    n_star = float(np.clip(L - alpha * rho / (lam * np.log(gamma)), 0.0, L))
    return {"n_dec": n_dec, "n_star": n_star, "g_dec": lam * n_dec * np.log(gamma),
            "g_star": lam * n_star * np.log(gamma), "too_much": n_dec > n_star}


def ah_ladder(lam: float = 1.0, n: float = 0.3, gamma: float = 1.5, years: int = 60, seed: int = 0,
              dt: float = 0.05) -> dict:
    """A simulated quality ladder: innovations arrive as a Poisson process at rate ``lam n``; each multiplies
    productivity by gamma.  Returns the step path of log productivity, the arrival dates and the expected line."""
    rng = np.random.default_rng(seed)
    t, arrivals = 0.0, []
    while True:
        t += rng.exponential(1 / (lam * n))
        if t > years:
            break
        arrivals.append(t)
    grid = np.arange(0, years + dt / 2, dt)
    steps = np.searchsorted(np.array(arrivals), grid, side="right")
    return {"t": grid.tolist(), "logA": (steps * np.log(gamma)).tolist(), "arrivals": arrivals,
            "expected": (lam * n * np.log(gamma) * grid).tolist(), "rate": lam * n}


def ah_sectors(lam: float = 0.1, n: float = 0.25, gamma: float = 1.5, years: int = 120, sectors: int = 200,
               seed: int = 0, dt: float = 0.25) -> dict:
    """Many sectors, each on its own ladder: every sector's log productivity jumps by ln(gamma) at its own Poisson
    dates; the economy's average log productivity grows almost smoothly at ``lam n ln gamma``."""
    rng = np.random.default_rng(seed)
    grid = np.arange(0, years + dt / 2, dt)
    paths = np.zeros((sectors, len(grid)))
    for i in range(sectors):
        t, arr = 0.0, []
        while True:
            t += rng.exponential(1 / (lam * n))
            if t > years:
                break
            arr.append(t)
        paths[i] = np.searchsorted(np.array(arr), grid, side="right") * np.log(gamma)
    mean = paths.mean(axis=0)
    return {"t": grid.tolist(), "sectors": paths[:5].tolist(), "mean": mean.tolist(),
            "expected": (lam * n * np.log(gamma) * grid).tolist(), "growth": lam * n * np.log(gamma),
            "jumps_per_sector": float(paths[:, -1].mean() / np.log(gamma))}


# ---------------------------------------------------------------------------------------------------------------
# Jones (1995): semi-endogenous growth

def semi_endogenous(lam: float = 1.0, phi: float = 0.5, n: float = 0.01, theta: float = 0.02, years: int = 300,
                    A0: float = 1.0, LA0: float = 1.0) -> dict:
    """``A_dot = theta L_A^lam A^phi`` with research labour growing at n: idea growth converges to
    ``lam n / (1 - phi)``, whatever theta or the initial number of researchers; research productivity
    ``A_dot / (A L_A)`` falls along the way."""
    A, LA = A0, LA0
    gA, prod, t = [], [], []
    for k in range(years + 1):
        dA = theta * LA ** lam * A ** phi
        gA.append(dA / A)
        prod.append(dA / A / LA)
        t.append(k)
        A += dA
        LA *= 1 + n
    return {"t": t, "gA": gA, "research_productivity": prod, "long_run": lam * n / (1 - phi)}


# ---------------------------------------------------------------------------------------------------------------
# Acemoglu (2002): directed technical change

def directed(sigma: float, ratios) -> dict:
    """The skill premium ``w_H / w_L = (N_H/N_L)^((sigma-1)/sigma) (H/L)^(-1/sigma)``.  With technology fixed,
    more skilled workers lower it (slope -1/sigma in logs).  If the relative productivity of skill-complementing
    technology responds to the market for it, ``N_H/N_L`` proportional to ``(H/L)^(sigma - 1)``, the long-run slope
    is ``sigma - 2``: above 2, more skills raise the premium."""
    r = np.asarray(ratios, float)
    short = r ** (-1 / sigma)
    long_ = r ** (sigma - 2)
    return {"ratio": r.tolist(), "short": short.tolist(), "long": long_.tolist(), "short_slope": -1 / sigma,
            "long_slope": sigma - 2}
