"""The Works' season (Part 23): a fashion buyer orders a new style before anyone knows how well it will sell.

Demand for the style is uncertain (lognormal, with a known average).  An order placed early, months before the season,
from a distant factory, is cheap but must be placed on a poor forecast; an order placed late, from a factory nearby,
costs more a piece but is placed after the first weeks of selling have shown how the style is doing.  Pieces that sell
earn the full price; pieces left at the end of the season are cleared at a deep discount; customers who find the style
sold out are lost.  This is the newsvendor problem: the best order is the quantile of demand at the critical ratio
(price - cost) / (price - clearance price).

Three ways to buy (Run it): all early (far), all late (near), or a base early and a top-up late (chase), the way a
retailer with nearby factories can work.  The early forecast's error is split into what the first weeks reveal and what
stays unknown; expectations over the revealed part are taken by Gauss-Hermite quadrature, so every number is exact for
the model.  All numbers are this series' illustrations; Inditex's 58.3% gross margin in FY2025 is the anchor.  No manim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import norm


@dataclass(frozen=True)
class Season:
    price: float = 40.0        # full price, $
    clearance: float = 8.0     # what a leftover piece fetches in the end-of-season sale (80% off), $
    mean: float = 100_000.0    # average demand for the style, pieces
    cv_far: float = 0.6        # forecast error (standard deviation over the mean) months before the season
    cv_near: float = 0.2       # forecast error after the first weeks of selling
    cost_far: float = 12.0     # cost of a piece made far away and ordered early, landed, $
    cost_near: float = 16.0    # cost of a piece made nearby and ordered late, $
    nodes: int = 64            # quadrature nodes over what the first weeks reveal

    def sigmas(self) -> tuple[float, float, float]:
        """Log-scale standard deviations: early, late, and what the first weeks reveal."""
        sf = math.sqrt(math.log(1 + self.cv_far ** 2))
        sn = math.sqrt(math.log(1 + self.cv_near ** 2))
        return sf, sn, math.sqrt(sf ** 2 - sn ** 2)

    def mu0(self) -> float:
        return math.log(self.mean) - self.sigmas()[0] ** 2 / 2

    def ratio(self, cost: float) -> float:
        """The critical ratio: the chance of selling the last piece ordered at which ordering it breaks even."""
        return (self.price - cost) / (self.price - self.clearance)

    def best(self, cost: float, mu: float, sigma: float) -> float:
        """The best single order at ``cost`` when log demand is normal with mean ``mu`` and sd ``sigma``."""
        return math.exp(mu + sigma * norm.ppf(self.ratio(cost)))

    @staticmethod
    def sold(q, mu, sigma):
        """Expected pieces sold, E[min(D, q)], for lognormal D (vectorized over ``mu``)."""
        q = np.maximum(q, 1e-9)
        m = np.exp(mu + sigma ** 2 / 2)
        return m * norm.cdf((np.log(q) - mu - sigma ** 2) / sigma) + q * norm.sf((np.log(q) - mu) / sigma)

    def _nodes(self):
        x, w = np.polynomial.hermite_e.hermegauss(self.nodes)
        return x, w / w.sum()

    def _summary(self, q, sold, cost) -> dict:
        """Averages of an order policy: pieces ordered, sold at full price, cleared, demand lost, money."""
        q, sold, cost = (float(v) for v in (q, sold, cost))
        left = q - sold
        revenue = self.price * sold + self.clearance * left
        profit = revenue - cost
        return {"ordered": q, "sold": sold, "cleared": left, "lost": self.mean - sold, "revenue": revenue, "cost": cost,
                "profit": profit, "gm": profit / revenue, "sell_through": sold / q,
                "markdown": (self.price - self.clearance) * left / (self.price * q)}

    def far(self) -> dict:
        """Order everything early from the distant factory, on the early forecast."""
        sf, _, _ = self.sigmas()
        q = self.best(self.cost_far, self.mu0(), sf)
        return self._summary(q, self.sold(q, self.mu0(), sf), self.cost_far * q)

    def near(self) -> dict:
        """Order everything late from the nearby factory, after the first weeks: the order follows what they reveal."""
        _, sn, s1 = self.sigmas()
        x, w = self._nodes()
        mu = self.mu0() + s1 * x
        q = np.exp(mu + sn * norm.ppf(self.ratio(self.cost_near)))
        return self._summary(w @ q, w @ self.sold(q, mu, sn), self.cost_near * (w @ q))

    def chase_at(self, base: float) -> dict:
        """Order ``base`` pieces early, then top up late to the best level for what the first weeks showed."""
        _, sn, s1 = self.sigmas()
        x, w = self._nodes()
        mu = self.mu0() + s1 * x
        target = np.exp(mu + sn * norm.ppf(self.ratio(self.cost_near)))
        top = np.maximum(target - base, 0.0)
        q = base + top
        out = self._summary(w @ q, w @ self.sold(q, mu, sn), self.cost_far * base + self.cost_near * (w @ top))
        out.update(base=base, topped=float(w @ (top > 0)), top_up=float(w @ top))
        return out

    def chase(self) -> dict:
        """The chase with the best early base."""
        res = minimize_scalar(lambda b: -self.chase_at(b)["profit"], bounds=(0.0, 3 * self.mean), method="bounded",
                              options={"xatol": 1.0})
        return self.chase_at(float(res.x))

    def choices(self) -> dict:
        return {"far": self.far(), "near": self.near(), "chase": self.chase()}


def inventory_days(inventory: float, cost_of_sales: float) -> float:
    """How many days of the year's cost of sales sit in inventory at year end."""
    return 365 * inventory / cost_of_sales
