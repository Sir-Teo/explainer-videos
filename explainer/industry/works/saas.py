"""The Works' software company (Part 36): a subscription business run quarter by quarter, its cohorts, and a licence
business switching to subscriptions.

A subscription company's revenue is its annual recurring revenue (ARR) earned a quarter at a time.  Each year customers
who stay spend more (expansion) and some leave or cut back (churn); salespeople, once they have ramped up, bring in new
ARR, though each extra one finds the market a little more crowded; engineering builds a stock of product that, with a
lag, lowers churn and lifts expansion and the salespeople's productivity.  Customers pay a year in advance, so cash runs
ahead of revenue.  The software itself costs almost nothing to copy: the cost of revenue is hosting and support.  No manim.

    >>> y = Saas().run()
    >>> round(y["arr"][-1] / 1e6), round(100 * y["growth"][-1]), round(100 * y["op_margin"][4])
    (351, 17, 25)
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class Saas:
    """A subscription software company.  Money a year unless stated; the run is in quarters."""

    arr0: float = 200e6             # annual recurring revenue at the start
    gross_margin: float = 0.78      # after hosting, support and customer success
    churn: float = 0.08             # share of ARR lost each year to customers leaving or cutting back
    expansion: float = 0.10         # extra ARR each year from customers who stay
    reps0: float = 100.0            # ramped quota-carrying salespeople at the start
    productivity: float = 0.45e6    # new ARR a ramped salesperson brings in a year, at today's crowding
    ramp: int = 2                   # quarters before a new salesperson is productive
    rep_cost: float = 0.7e6         # sales and marketing cost per salesperson a year, with managers, engineers, marketing
    market: float = 300.0           # salespeople at which crowding has halved each one's productivity (from none)
    rnd0: float = 40e6              # engineering a year
    ga: float = 0.10                # general and administrative, share of revenue
    product_scale: float = 150e6    # extra product stock that lifts quality by 100%
    product_decay: float = 0.20     # yearly decay of the product stock (code ages, competitors catch up)
    churn_cut: float = 0.5          # churn falls by this times the quality lift
    expansion_lift: float = 0.6     # expansion rises by this times the quality lift
    sales_lift: float = 0.3         # productivity rises by this times the quality lift
    billing: float = 0.5            # deferred revenue as a share of ARR (annual billing in advance)
    quarters: int = 12

    def with_(self, **kw) -> "Saas":
        return replace(self, **kw)

    def _crowd(self, reps: float) -> float:
        return (1 + self.reps0 / self.market) / (1 + reps / self.market)

    def run(self, extra: float = 0.0, to_sales: float = 0.5, raise_at: int | None = None, rise: float = 0.10,
            churn_bump: float = 0.03, price_elast: float = 1.5, quarters: int | None = None, extra_years: int | None = None) -> dict:
        """Run the company.  ``extra`` a year of budget for ``extra_years`` years, a share ``to_sales`` of it spent hiring
        salespeople (at the start of each year) and the rest on engineering (every year of the run unless
        ``extra_years`` is given); an optional price rise of ``rise`` at quarter
        ``raise_at`` reprices renewals over the following four quarters, adds ``churn_bump`` to churn for a year and cuts
        new ARR by the price elasticity of new customers."""
        Q = self.quarters if quarters is None else quarters
        extra_years = Q if extra_years is None else extra_years
        arr = self.arr0
        hires: list = []                                  # (quarter hired, count)
        stock = 0.0
        out = {k: [] for k in ("arr", "revenue", "gross", "sm", "rnd", "ga", "op", "op_margin", "new", "churned",
                               "expanded", "reps", "growth", "cash", "deferred", "quality", "nrr")}
        hist_arr = [arr]
        for t in range(Q):
            year = t // 4
            if t % 4 == 0 and year < extra_years and extra > 0:
                hires.append((t, extra * to_sales / self.rep_cost))
            rnd_extra = extra * (1 - to_sales) if year < extra_years else 0.0
            stock = stock * (1 - self.product_decay) ** 0.25 + rnd_extra / 4
            q = stock / self.product_scale
            ramped = self.reps0 + sum(n for (h, n) in hires if t - h >= self.ramp)
            hired = sum(n for (h, n) in hires)
            reps = self.reps0 + hired
            price_q = 0.0
            churn = self.churn * (1 - self.churn_cut * q)
            if raise_at is not None and raise_at <= t < raise_at + 4:
                price_q = rise / 4
                churn += churn_bump
            unit = (1 + rise) ** (1 - price_elast) if (raise_at is not None and t >= raise_at) else 1.0
            new = ramped * self.productivity * (1 + self.sales_lift * q) * self._crowd(reps) * unit / 4
            churned = arr * churn / 4
            expanded = arr * self.expansion * (1 + self.expansion_lift * q) / 4 + arr * price_q
            start = arr
            arr = arr + new + expanded - churned
            revenue = (start + arr) / 2 / 4
            gross = self.gross_margin * revenue
            sm = reps * self.rep_cost / 4
            rnd = (self.rnd0 + rnd_extra) / 4
            ga = self.ga * revenue
            op = gross - sm - rnd - ga
            hist_arr.append(arr)
            growth = arr / hist_arr[-5] - 1 if len(hist_arr) >= 5 else (arr / hist_arr[0]) ** (4 / len(hist_arr[1:])) - 1
            cash = op + self.billing * (arr - start)
            for k, v in (("arr", arr), ("revenue", revenue), ("gross", gross), ("sm", sm), ("rnd", rnd), ("ga", ga),
                         ("op", op), ("op_margin", op / revenue), ("new", new), ("churned", churned), ("expanded", expanded),
                         ("reps", reps), ("growth", growth), ("cash", cash), ("deferred", self.billing * arr),
                         ("quality", q), ("nrr", 1 - churn + self.expansion * (1 + self.expansion_lift * q) + 4 * price_q)):
                out[k].append(v)
        out["cum_cash"] = float(np.sum(out["cash"]))
        return out

    def unit_economics(self) -> dict:
        """The first year at the start: CAC payback and the magic number."""
        y = self.run(quarters=4)
        sm = sum(y["sm"])
        new_arr = sum(y["new"]) + sum(y["expanded"])
        return dict(sm=sm, new=sum(y["new"]), expanded=sum(y["expanded"]), churned=sum(y["churned"]),
                    payback_months=12 * sm / (sum(y["new"]) * self.gross_margin),
                    magic=(y["arr"][-1] - self.arr0) / sm, new_arr=new_arr)


def cohorts(years: int = 8, new: float = 1.0, growth: float = 0.25, churn: float = 0.08, expansion: float = 0.10) -> np.ndarray:
    """ARR by cohort (rows, the year customers joined) and year (columns): each year a cohort ``growth`` larger than the
    last joins with ARR ``new``; afterwards every cohort's ARR changes by ``expansion - churn`` a year."""
    m = np.zeros((years, years))
    for c in range(years):
        first = new * (1 + growth) ** c
        for y in range(c, years):
            m[c, y] = first * (1 + expansion - churn) ** (y - c)
    return m


def j_curve(years: int = 10, switch: int = 3, units: float = 100.0, unit_growth: float = 0.06, licence: float = 3.0,
            maintenance: float = 0.2, subscription: float = 1.0, migrate: float = 0.35) -> dict:
    """Revenue of a software company selling perpetual licences (``licence`` up front and ``maintenance`` a year after)
    that switches in year ``switch`` to subscriptions at ``subscription`` a year; from then on new customers subscribe
    and a share ``migrate`` of the remaining licence owners converts each year.  Returns both paths."""
    lic_rev, sub_rev = [], []
    owners_l = owners_s = 0.0          # licence owners paying maintenance; subscribers
    base_owners = 0.0
    for y in range(years):
        n = units * (1 + unit_growth) ** y
        # the path that never switches
        lic_rev.append(n * licence + base_owners * maintenance)
        base_owners += n
        # the path that switches
        if y < switch:
            rev = n * licence + owners_l * maintenance
            owners_l += n
        else:
            moved = migrate * owners_l
            owners_l -= moved
            owners_s += moved + n
            rev = owners_l * maintenance + owners_s * subscription
        sub_rev.append(rev)
    return dict(licence=lic_rev, switched=sub_rev, switch=switch)
