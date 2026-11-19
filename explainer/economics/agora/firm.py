"""The firm (Agora, Part 8): what to make, how, and why there is a firm at all.

**Technologies.**  :class:`CobbDouglas` (q = A K^a L^b), :class:`CES` (q = A [s K^rho + (1 - s) L^rho]^(nu / rho),
rho = (sigma - 1) / sigma) and :class:`Leontief` (q = min(K / a_K, L / a_L)), each with its output, marginal
products, technical rate of substitution, returns to scale, conditional factor demands and cost function in closed
form; :func:`shephard_errors` checks Shephard's lemma numerically, :func:`isoquant` draws an isoquant.

**Costs and supply.**  :class:`ShortRun` (capital fixed: total, variable, average and marginal cost, and the
envelope of short-run average costs that is the long-run curve), :func:`cd_supply` and :func:`cd_profit` (supply and
profit for decreasing returns, with Hotelling's lemma checked by :func:`hotelling_errors`), :func:`le_chatelier`
(short- and long-run supply elasticities), :class:`UCost` (a U-shaped cost F + c q + d q^2: the minimum of average
cost, the shutdown and break-even prices), and :func:`industry` (free entry: the long-run price and the number of
firms; with heterogeneous fixed costs, an upward-sloping long-run supply and the rents of the low-cost firms).

**Data.**  :func:`fit_cobb_douglas` (Cobb and Douglas's 1928 regression and its variants: unrestricted, constant
returns imposed, with a time trend, in growth rates).

**The boundary of the firm.**  :func:`hold_up` (relationship-specific investment under ex post bargaining against
integration), :func:`ghm` (Grossman-Hart-Moore: who should own the asset, for two parties' investments),
:func:`make_or_buy` (Williamson's comparison of market and hierarchy as asset specificity grows), and
:func:`hire` (the boatyard: hire while the last worker's marginal revenue product covers the wage).

Plain numpy and scipy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize_scalar


# ---------------------------------------------------------------------------------------------------------------
# technologies


@dataclass(frozen=True)
class CobbDouglas:
    """q = A K^a L^b; returns to scale a + b; elasticity of substitution 1."""
    A: float = 1.0
    a: float = 0.25
    b: float = 0.75

    def q(self, K, L):
        return self.A * np.asarray(K, float) ** self.a * np.asarray(L, float) ** self.b

    def mp(self, K, L):
        q = self.q(K, L)
        return self.a * q / np.asarray(K, float), self.b * q / np.asarray(L, float)

    def trs(self, K, L):
        """How much capital one more worker can replace, holding output fixed: MP_L / MP_K."""
        mk, ml = self.mp(K, L)
        return ml / mk

    @property
    def scale(self) -> float:
        return self.a + self.b

    def demand(self, w: float, r: float, q: float):
        """Conditional factor demands (K, L) that make q at least cost."""
        s = self.a + self.b
        ratio = (self.a / self.b) * (w / r)          # K / L at the optimum
        L = (q / (self.A * ratio ** self.a)) ** (1 / s)
        return ratio * L, L

    def cost(self, w: float, r: float, q: float) -> float:
        K, L = self.demand(w, r, q)
        return float(r * K + w * L)


@dataclass(frozen=True)
class CES:
    """q = A [s K^rho + (1 - s) L^rho]^(nu / rho), rho = (sigma - 1) / sigma: sigma is the elasticity of
    substitution (Arrow, Chenery, Minhas and Solow 1961); nu the returns to scale."""
    A: float = 1.0
    s: float = 0.3
    sigma: float = 0.5
    nu: float = 1.0

    @property
    def rho(self) -> float:
        return (self.sigma - 1) / self.sigma

    def q(self, K, L):
        K, L = np.asarray(K, float), np.asarray(L, float)
        if abs(self.sigma - 1) < 1e-9:
            return self.A * K ** (self.s * self.nu) * L ** ((1 - self.s) * self.nu)
        r = self.rho
        return self.A * (self.s * K ** r + (1 - self.s) * L ** r) ** (self.nu / r)

    def mp(self, K, L, h: float = 1e-6):
        K, L = np.asarray(K, float), np.asarray(L, float)
        return ((self.q(K * (1 + h), L) - self.q(K * (1 - h), L)) / (2 * h * K),
                (self.q(K, L * (1 + h)) - self.q(K, L * (1 - h))) / (2 * h * L))

    def trs(self, K, L):
        mk, ml = self.mp(K, L)
        return ml / mk

    @property
    def scale(self) -> float:
        return self.nu

    def demand(self, w: float, r: float, q: float):
        # the first-order condition gives K / L = ((s / (1 - s)) (w / r))^sigma
        ratio = ((self.s / (1 - self.s)) * (w / r)) ** self.sigma
        L = (q / float(self.q(ratio, 1.0))) ** (1 / self.nu)
        return ratio * L, L

    def cost(self, w: float, r: float, q: float) -> float:
        K, L = self.demand(w, r, q)
        return float(r * K + w * L)


@dataclass(frozen=True)
class Leontief:
    """q = min(K / aK, L / aL): no substitution at all (sigma = 0)."""
    aK: float = 1.0
    aL: float = 1.0

    def q(self, K, L):
        return np.minimum(np.asarray(K, float) / self.aK, np.asarray(L, float) / self.aL)

    @property
    def scale(self) -> float:
        return 1.0

    def demand(self, w: float, r: float, q: float):
        return self.aK * q, self.aL * q

    def cost(self, w: float, r: float, q: float) -> float:
        return float((r * self.aK + w * self.aL) * q)


def shephard_errors(tech, w: float, r: float, q: float, h: float = 1e-6) -> dict:
    """Shephard's lemma: the derivative of the cost function in each factor price is that factor's demand."""
    K, L = tech.demand(w, r, q)
    dcw = (tech.cost(w * (1 + h), r, q) - tech.cost(w * (1 - h), r, q)) / (2 * h * w)
    dcr = (tech.cost(w, r * (1 + h), q) - tech.cost(w, r * (1 - h), q)) / (2 * h * r)
    return {"L": abs(dcw - L) / L, "K": abs(dcr - K) / K}


def isoquant(tech, q: float, Ls):
    """The capital needed with each amount of labour to make q (NaN where q cannot be made)."""
    Ls = np.asarray(Ls, float)
    out = []
    for L in Ls:
        if isinstance(tech, Leontief):
            out.append(tech.aK * q if L / tech.aL >= q else np.nan)
            continue
        f = lambda lk: float(tech.q(np.exp(lk), L)) - q  # noqa: E731
        lo, hi = -30.0, 30.0
        if f(hi) < 0:
            out.append(np.nan)
            continue
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if f(mid) > 0:
                hi = mid
            else:
                lo = mid
        out.append(np.exp(0.5 * (lo + hi)))
    return np.array(out)


# ---------------------------------------------------------------------------------------------------------------
# costs, supply, the industry


@dataclass(frozen=True)
class ShortRun:
    """Cobb-Douglas with capital fixed at Kbar: total, variable, average and marginal cost."""
    tech: CobbDouglas
    Kbar: float
    w: float
    r: float

    def labour(self, q):
        t = self.tech
        return (np.asarray(q, float) / (t.A * self.Kbar ** t.a)) ** (1 / t.b)

    def vc(self, q):
        return self.w * self.labour(q)

    def tc(self, q):
        return self.r * self.Kbar + self.vc(q)

    def avc(self, q):
        return self.vc(q) / np.asarray(q, float)

    def atc(self, q):
        return self.tc(q) / np.asarray(q, float)

    def mc(self, q):
        return self.vc(q) / (self.tech.b * np.asarray(q, float))


def cd_supply(tech: CobbDouglas, p: float, w: float, r: float) -> float:
    """Long-run supply of a Cobb-Douglas firm with decreasing returns (a + b < 1): q maximizing p q - c(w, r, q).
    With c = k q^(1/s), price equals marginal cost at q = (p s / k)^(s / (1 - s))."""
    s = tech.a + tech.b
    assert s < 1, "supply is defined for decreasing returns"
    k = tech.cost(w, r, 1.0)
    return float((p * s / k) ** (s / (1 - s)))


def cd_profit(tech: CobbDouglas, p: float, w: float, r: float) -> float:
    q = cd_supply(tech, p, w, r)
    return float(p * q - tech.cost(w, r, q))


def hotelling_errors(tech: CobbDouglas, p: float, w: float, r: float, h: float = 1e-6) -> dict:
    """Hotelling's lemma: d profit / dp = supply, d profit / dw = -L, d profit / dr = -K."""
    q = cd_supply(tech, p, w, r)
    K, L = tech.demand(w, r, q)
    dp = (cd_profit(tech, p * (1 + h), w, r) - cd_profit(tech, p * (1 - h), w, r)) / (2 * h * p)
    dw = (cd_profit(tech, p, w * (1 + h), r) - cd_profit(tech, p, w * (1 - h), r)) / (2 * h * w)
    dr = (cd_profit(tech, p, w, r * (1 + h)) - cd_profit(tech, p, w, r * (1 - h))) / (2 * h * r)
    return {"q": abs(dp - q) / q, "L": abs(-dw - L) / L, "K": abs(-dr - K) / K}


def le_chatelier(tech: CobbDouglas) -> dict:
    """Supply elasticities of a Cobb-Douglas firm: short run (capital fixed) b / (1 - b), long run s / (1 - s): the
    long run responds more, because more inputs can adjust (Samuelson's Le Chatelier principle)."""
    s = tech.a + tech.b
    return {"short": tech.b / (1 - tech.b), "long": s / (1 - s)}


@dataclass(frozen=True)
class UCost:
    """A U-shaped cost: total cost F + c q + d q^2 (F avoidable in the long run, sunk in the short)."""
    F: float
    c: float
    d: float

    def tc(self, q):
        q = np.asarray(q, float)
        return self.F + self.c * q + self.d * q ** 2

    def atc(self, q):
        return self.tc(q) / np.asarray(q, float)

    def avc(self, q):
        return self.c + self.d * np.asarray(q, float)

    def mc(self, q):
        return self.c + 2 * self.d * np.asarray(q, float)

    @property
    def efficient_scale(self) -> float:
        return float(np.sqrt(self.F / self.d))

    @property
    def breakeven(self) -> float:
        """The lowest price at which the firm covers all its costs: the minimum of average total cost."""
        return float(self.c + 2 * np.sqrt(self.F * self.d))

    @property
    def shutdown(self) -> float:
        """The lowest price at which it keeps producing in the short run: the minimum of average variable cost."""
        return float(self.c)

    def supply(self, p: float, long_run: bool = True) -> float:
        floor = self.breakeven if long_run else self.shutdown
        return float((p - self.c) / (2 * self.d)) if p >= floor else 0.0


def industry(demand_a: float, demand_b: float, F: float, c: float, d: float, fixed_costs=None) -> dict:
    """Free entry with linear demand Q = a - b p.  Identical firms (``fixed_costs`` None): price falls to the minimum
    of average cost and the number of firms is Q / q*.  With heterogeneous fixed costs (sorted, one per potential
    entrant), firms enter in order of cost until the next one would lose money; the price then exceeds the marginal
    entrant's break-even price by less than one firm's worth, and the earlier entrants earn rents."""
    if fixed_costs is None:
        u = UCost(F, c, d)
        p = u.breakeven
        Q = demand_a - demand_b * p
        return {"price": p, "q": u.efficient_scale, "Q": Q, "firms": Q / u.efficient_scale, "rents": 0.0}
    fc = np.sort(np.asarray(fixed_costs, float))
    best = None
    for n in range(1, len(fc) + 1):
        # n firms, each producing where p = MC: q = (p - c) / 2d; market: n (p - c) / 2d = a - b p
        p = (demand_a + n * c / (2 * d)) / (demand_b + n / (2 * d))
        q = (p - c) / (2 * d)
        profit = p * q - (c * q + d * q * q) - fc[:n]
        if profit[-1] < 0:
            break
        best = {"price": float(p), "q": float(q), "Q": float(n * q), "firms": n, "profits": profit,
                "rents": float(profit.sum())}
    return best


# ---------------------------------------------------------------------------------------------------------------
# Cobb and Douglas's regression


def fit_cobb_douglas(Y, K, L, how: str = "unrestricted", years=None) -> dict:
    """OLS on logs.  ``how``: "unrestricted" (log Y on log L and log K), "crs" (log(Y/L) on log(K/L), as Cobb and
    Douglas fitted it in 1928), "trend" (adds a linear time trend), "growth" (first differences)."""
    y, k, l = (np.log(np.asarray(v, float)) for v in (Y, K, L))
    n = len(y)
    t = np.arange(n, dtype=float) if years is None else np.asarray(years, float) - years[0]
    if how == "unrestricted":
        X, Yv, names = np.c_[np.ones(n), l, k], y, ("const", "labour", "capital")
    elif how == "crs":
        X, Yv, names = np.c_[np.ones(n), k - l], y - l, ("const", "capital")
    elif how == "trend":
        X, Yv, names = np.c_[np.ones(n), t, l, k], y, ("const", "trend", "labour", "capital")
    elif how == "growth":
        X, Yv, names = np.c_[np.ones(n - 1), np.diff(l), np.diff(k)], np.diff(y), ("const", "labour", "capital")
    else:
        raise ValueError(how)
    b = np.linalg.lstsq(X, Yv, rcond=None)[0]
    e = Yv - X @ b
    dof = len(Yv) - X.shape[1]
    se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * (e @ e) / dof)
    r2 = 1 - (e @ e) / ((Yv - Yv.mean()) @ (Yv - Yv.mean()))
    out = {nm: float(v) for nm, v in zip(names, b)}
    out.update({f"se_{nm}": float(s) for nm, s in zip(names, se)})
    out.update({"r2": float(r2), "fitted": X @ b, "resid": e})
    if how == "crs":
        out["labour"] = 1 - out["capital"]
    return out


# ---------------------------------------------------------------------------------------------------------------
# the boundary of the firm


def hold_up(V: float, theta: float) -> dict:
    """A supplier can invest i in an asset worth 2 V sqrt(i) only inside the relationship.  Integrated (or with a
    complete contract) it invests the first best, V^2; dealing at arm's length, it is paid a share theta of the
    surplus after the investment is sunk, and invests (theta V)^2.  Returns both investments and the surplus lost."""
    first = V ** 2
    held = (theta * V) ** 2

    def surplus(i):
        return 2 * V * np.sqrt(i) - i

    return {"first_best": first, "held_up": held, "surplus_first": surplus(first), "surplus_held": surplus(held),
            "loss": surplus(first) - surplus(held)}


def ghm(va: float, vb: float, oa: float, ob: float, cost: float = 1.0) -> dict:
    """Grossman-Hart-Moore with two parties A and B and one asset.  Each invests e (cost e^2 / 2 * cost); inside the
    relationship investment adds va e_A + vb e_B to the joint value, split 50-50 ex post.  The owner of the asset
    keeps an outside option worth a share of its own investment's value (``oa`` for A owning, ``ob`` for B), the
    non-owner none.  Ex post each gets its outside option plus half the gain over the two options, so its marginal
    return to investing is (v + o) / 2 if it owns and v / 2 if not.  Returns investments and surplus under A-ownership,
    B-ownership and non-integration (each owning nothing specific: both v / 2)."""

    def run(ma, mb):
        ea, eb = ma / cost, mb / cost
        return {"eA": ea, "eB": eb, "surplus": va * ea + vb * eb - cost * (ea ** 2 + eb ** 2) / 2}

    out = {"A owns": run((va + oa * va) / 2, vb / 2), "B owns": run(va / 2, (vb + ob * vb) / 2),
           "apart": run(va / 2, vb / 2), "first best": run(va, vb)}
    out["best"] = max(("A owns", "B owns", "apart"), key=lambda k: out[k]["surplus"])
    return out


def make_or_buy(k, market=(1.0, 2.0), hierarchy=(1.6, 0.5)):
    """Williamson's heuristic (1985): governance cost of buying in the market m0 + m1 k and of making in a hierarchy
    h0 + h1 k, for asset specificity k; the market is cheaper for standard inputs, the firm for specific ones.
    Returns both costs and the switch point."""
    k = np.asarray(k, float)
    m0, m1 = market
    h0, h1 = hierarchy
    return {"market": m0 + m1 * k, "hierarchy": h0 + h1 * k, "switch": (h0 - m0) / (m1 - h1)}


def hire(p: float, w: float, tech: CobbDouglas, K: float, max_workers: int = 30) -> dict:
    """The boatyard: with capital K fixed, each worker adds a marginal product; hire while p times it covers the
    wage.  Returns the schedule of marginal products, the number hired and the profit at each head count."""
    n = np.arange(0, max_workers + 1)
    out = tech.q(K, n.astype(float))
    mp = np.diff(out)
    hired = int(np.sum(p * mp >= w)) if np.all(np.diff(mp) <= 1e-12) else int(np.argmax(p * out - w * n))
    profit = p * out - w * n
    return {"workers": n, "output": out, "mp": mp, "hired": hired, "profit": profit,
            "best": int(np.argmax(profit))}


def best_scale(cost_fn, qs):
    """The output that minimizes average cost along a grid (for curves drawn on screen)."""
    qs = np.asarray(qs, float)
    ac = np.array([cost_fn(q) / q for q in qs])
    i = int(np.argmin(ac))
    res = minimize_scalar(lambda q: cost_fn(q) / q, bounds=(qs[max(i - 1, 0)], qs[min(i + 1, len(qs) - 1)]),
                          method="bounded")
    return float(res.x)


def selection(yards: int, months: int, elasticity: float, noise: float, mutation: float, seed: int,
              cost: float = 1.0, fixed: float = None, scale: float = 100.0) -> dict:
    """Alchian (1950): firms that never maximize anything, run through survival.  Each yard prices at cost times
    (1 + markup), its markup fixed by habit and drawn uniform on 0-100% at the start.  Each month it sells
    scale * p^elasticity * exp(noise * shock) and earns (p - cost) q - fixed; the profit-maximizing markup is
    1 / (-elasticity - 1).  A yard with three losing months in a row closes and is replaced by a copy of a profitable
    yard, chosen in proportion to its profit (newcomers imitate success), its markup varied by ``mutation``.  Returns the markups month by
    month, closures, and the optimum."""
    rng = np.random.default_rng(seed)
    best = 1.0 / (-elasticity - 1.0)
    if fixed is None:
        # set so that a yard at the optimum earns a modest profit and one far from it loses money
        p_best = cost * (1 + best)
        fixed = 0.9 * (p_best - cost) * scale * p_best ** elasticity
    m = rng.uniform(0.0, 1.0, yards)
    losing = np.zeros(yards, int)
    history, closures = [m.copy()], []
    for _ in range(months):
        p = cost * (1 + m)
        q = scale * p ** elasticity * np.exp(noise * rng.standard_normal(yards))
        profit = (p - cost) * q - fixed
        losing = np.where(profit < 0, losing + 1, 0)
        dead = np.where(losing >= 3)[0]
        alive = np.where(profit >= 0)[0]
        if len(dead) and len(alive):
            parents = rng.choice(alive, size=len(dead), p=profit[alive] / profit[alive].sum())
            m[dead] = np.clip(m[parents] + mutation * rng.standard_normal(len(dead)), 0.0, 2.0)
            losing[dead] = 0
        closures.append(len(dead))
        history.append(m.copy())
    return {"markups": np.array(history), "closures": np.array(closures), "best": best, "fixed": fixed}
