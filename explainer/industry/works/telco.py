"""The Works' telecoms: a spectrum auction run as an ascending clock, the value of a subscriber from what she pays, how
often she leaves and what she cost to win, and a tower whose return rises with every tenant.  Numpy only.

The auction: ``supply`` identical blocks of spectrum; each bidder has declining values for its first, second, third and
fourth block (billions of dollars).  The price rises by ``step`` while the blocks demanded exceed the supply; each bidder
demands the blocks it values at or above the price, up to a cap it chooses.  The auction ends at the first price where
demand does not exceed supply; every winner pays that price for each block (a uniform price).  Bidding for fewer blocks
than you value can end the auction lower: demand reduction.

The subscriber: an account pays ``arpa`` a month, ``margin`` of which is left after the cost of serving it; it leaves with
probability ``churn`` a month, so it stays 1 / churn months on average; winning it cost ``cac``.

The tower: built for ``build``; it costs ``opex`` a year to run (ground rent, power, upkeep) and earns ``rent`` a year
from each tenant.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class Auction:
    values: tuple = ((9.5, 9.0, 7.0, 6.5), (6.0, 4.5, 4.5, 2.0), (10.0, 7.0, 4.0, 1.5), (9.0, 7.5, 7.0, 3.5))
    names: tuple = ("you", "rival A", "rival B", "rival C")
    supply: int = 8
    step: float = 0.25

    def run(self, cap: int = 4, caps: tuple | None = None) -> dict:
        """The clock with bidder 0 capped at ``cap`` blocks (the rivals bid sincerely unless ``caps`` is given)."""
        caps = caps or (cap,) + (len(self.values[0]),) * (len(self.values) - 1)
        p, path = 0.0, []
        while True:
            d = [min(c, sum(1 for v in vals if v >= p - 1e-12)) for vals, c in zip(self.values, caps)]
            path.append((p, sum(d)))
            if sum(d) <= self.supply:
                break
            p = round(p + self.step, 6)
        won = d
        surplus = [sum(vals[:n]) - n * p for vals, n in zip(self.values, won)]
        return dict(price=p, won=won, surplus=surplus, revenue=p * sum(won), unsold=self.supply - sum(won), path=path)

    def but(self, **kw) -> "Auction":
        return replace(self, **kw)


@dataclass(frozen=True)
class Subscriber:
    arpa: float = 147.31        # $ a month (Verizon's Consumer postpaid ARPA, 2025)
    churn: float = 0.0092       # a month (Verizon's Consumer postpaid phone churn, 2025)
    margin: float = 0.45
    cac: float = 600.0

    def months(self) -> float:
        return 1.0 / self.churn

    def lifetime(self) -> float:
        """Margin over an account's expected life, less what it cost to win (no discounting)."""
        return self.arpa * self.margin / self.churn - self.cac

    def but(self, **kw) -> "Subscriber":
        return replace(self, **kw)


@dataclass(frozen=True)
class Tower:
    build: float = 300000.0
    opex: float = 20600.0       # $ a year: American Tower's U.S. & Canada segment operating expenses per site, 2025
    rent: float = 45000.0

    def cash(self, tenants: int) -> float:
        return tenants * self.rent - self.opex

    def yield_(self, tenants: int) -> float:
        """Cash a year over the cost of the tower."""
        return self.cash(tenants) / self.build

    def margin(self, tenants: int) -> float:
        return self.cash(tenants) / (tenants * self.rent) if tenants else float("-inf")

    def but(self, **kw) -> "Tower":
        return replace(self, **kw)


_ = field
