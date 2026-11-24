"""The cycle: capacity that takes years to build, ordered by firms that look at today's price (Part 6).

Four small machines, each with a property the tests check:

* :func:`cobweb` is Ezekiel's model.  Farmers decide what to raise from this year's price; the crop arrives next
  year and sells for whatever clears the market.  With linear curves the path spirals in when supply is less
  responsive than demand (``d * b < 1``), cycles for ever when they are equal, and spirals out otherwise.
* :func:`fleet` is a shipping market.  Each year owners order ships in proportion to how far today's freight rate is
  above the cost of running one; ships arrive ``lead`` years later and last ``life`` years.  Demand grows steadily.
  The longer the lead time, the larger the swings, though demand never falls.
* :func:`bullwhip` passes a shop's sales up a chain of tiers.  Each tier forecasts with a moving average and orders
  enough to restore a stock of ``cover`` periods of its forecast.  The variance of orders grows at every tier.
* :func:`leverage` splits costs into fixed and variable and shows how a fall in revenue becomes a larger fall in
  operating profit.
"""

from __future__ import annotations

import numpy as np


def cobweb(a: float, b: float, c: float, d: float, p0: float, n: int = 12) -> tuple[np.ndarray, np.ndarray]:
    """Demand ``p = a - b q``; supply ``q_t = c + d p_{t-1}``.  Returns prices ``p_0..p_n`` and quantities
    ``q_1..q_n`` (``q[0]`` is the quantity that ``p_0`` called forth, sold at ``p_1``)."""
    p = [p0]
    q = []
    for _ in range(n):
        qt = c + d * p[-1]
        q.append(qt)
        p.append(a - b * qt)
    return np.array(p), np.array(q)


def cobweb_eq(a: float, b: float, c: float, d: float) -> tuple[float, float]:
    """The price and quantity at which the curves cross."""
    p = (a - b * c) / (1 + b * d)
    return p, c + d * p


def fleet(years: int = 40, lead: int = 3, life: int = 25, growth: float = 0.03, cost: float = 1.0,
          k: float = 0.25, elasticity: float = 0.5, fleet0: float = 100.0, order_cap: float = 0.4,
          shock: dict | None = None) -> dict:
    """A shipping market, year by year.

    Demand for ships grows by ``growth`` a year (``shock`` maps a year to a one-off proportional change in demand).
    The freight rate clears the market: ``rate = cost * (demand / fleet) ** (1 / elasticity)``, so a fleet 10% short
    of demand raises the rate by about 20% when ``elasticity`` is 0.5.  Owners order ``k * (rate / cost - 1)`` of the
    fleet each year (never less than zero, never more than ``order_cap``), looking only at today's rate.  Orders are
    delivered ``lead`` years later; a ship is scrapped after ``life`` years (the starting fleet is spread evenly over
    ages).  Returns arrays: demand, fleet, rate, orders (ordered that year), deliveries, orderbook (ordered, not yet
    delivered, as a share of the fleet)."""
    assert lead >= 1, "a ship ordered this year cannot sail this year"
    shock = shock or {}
    dem = np.zeros(years)
    flt = np.zeros(years)
    rate = np.zeros(years)
    orders = np.zeros(years)
    deliv = np.zeros(years)
    book = np.zeros(years)
    scrap_old = fleet0 / life  # the starting fleet retires evenly
    d = fleet0
    f = fleet0
    for t in range(years):
        d = d * (1 + growth) * (1 + shock.get(t, 0.0))
        deliv[t] = orders[t - lead] if t >= lead else fleet0 * growth  # before any orders arrive: replacement pace
        retire = orders[t - lead - life] if t - lead - life >= 0 else scrap_old
        f = f + deliv[t] - retire
        dem[t], flt[t] = d, f
        rate[t] = cost * (d / f) ** (1 / elasticity)
        orders[t] = f * min(max(k * (rate[t] / cost - 1) + growth, 0.0), order_cap)
        pending = orders[max(0, t - lead + 1):t + 1].sum()
        book[t] = pending / f
    return dict(demand=dem, fleet=flt, rate=rate, orders=orders, deliveries=deliv, orderbook=book)


def swing(x: np.ndarray, burn: int = 10) -> float:
    """Peak-to-trough range of a series after a burn-in, as a ratio of its mean (how big the cycle is)."""
    y = np.asarray(x)[burn:]
    return float((y.max() - y.min()) / y.mean())


def bullwhip(sales: np.ndarray, tiers: int = 4, window: int = 4, cover: float = 2.0) -> np.ndarray:
    """Orders placed by each tier of a chain, the first tier being the shop that sees ``sales``.

    Each tier forecasts next period's demand as the mean of the last ``window`` orders it received and orders
    ``demand + (target - stock)`` where the target stock is ``cover`` periods of the forecast; the stock adjusts by
    what came in less what went out (no lead time, unlimited supply upstream).  Returns an array of shape
    ``(tiers + 1, n)``: row 0 is the sales, row ``i`` the orders tier ``i`` places upstream."""
    sales = np.asarray(sales, dtype=float)
    n = len(sales)
    out = np.zeros((tiers + 1, n))
    out[0] = sales
    for i in range(1, tiers + 1):
        incoming = out[i - 1]
        stock = cover * incoming[:window].mean()
        for t in range(n):
            hist = incoming[max(0, t - window + 1):t + 1]
            fc = hist.mean()
            target = cover * fc
            stock -= incoming[t]
            o = max(incoming[t] + (target - stock), 0.0)
            stock += o
            out[i, t] = o
    return out


def leverage(revenue0: float, revenue1: float, fixed: float, variable_share: float) -> dict:
    """Operating profit before and after a change in revenue when ``fixed`` costs stay and variable costs are a
    constant share of revenue.  Returns both profits and the ratio of the profit change to the revenue change."""
    p0 = revenue0 * (1 - variable_share) - fixed
    p1 = revenue1 * (1 - variable_share) - fixed
    dr = revenue1 / revenue0 - 1
    dp = (p1 - p0) / abs(p0) if p0 else float("nan")
    return dict(profit0=p0, profit1=p1, revenue_change=dr, profit_change=dp,
                degree=dp / dr if dr else float("nan"))
