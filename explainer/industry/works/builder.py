"""The Works' builder (Part 25): a homebuilder that must secure land three years before it can sell the homes on it, and
a mortgage.

The land.  A home sells today for ``price``; its lot costs ``lot``, the house ``build``, and selling and overhead take
``overhead`` of the sale price.  In ``years`` years, when the home is sold, prices are either up ``boom`` or down ``bust``
(with probability ``p_bust``).  The builder can own the lot now (paying for it and carrying it at ``carry`` a year) or
option it: put down a ``deposit`` now and buy the lot at delivery for its price grown at ``escalator`` a year, the land
banker's return, or walk away in a bust and lose only the deposit.  Owning earns more per home if prices rise and loses
if they fall; the option costs more in a boom but caps the loss, and ties up a fraction of the money.

The mortgage.  ``payment`` is the level monthly payment on a fixed-rate loan; ``balance`` the amount still owed.

All numbers are this series' illustrations; D.R. Horton's 77% and Lennar's 98% of lots controlled through contracts and
options, and NVR's lot purchase agreements, are the anchors.  No manim.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LandDeal:
    price: float = 400.0       # a home's price today, $ thousand
    lot: float = 100.0         # the finished lot, $ thousand
    build: float = 220.0       # sticks and bricks, $ thousand
    overhead: float = 0.08     # selling, commissions and overhead, a share of the sale price
    years: int = 3
    carry: float = 0.07        # the cost of the money tied up in an owned lot, a year
    escalator: float = 0.12    # what the land banker charges, a year, on the optioned lot's price
    deposit: float = 10.0      # the option deposit, $ thousand
    boom: float = 0.08         # prices at delivery in the good case
    bust: float = -0.15        # prices at delivery in the bad case
    p_bust: float = 0.4

    def sale(self, state: str) -> float:
        return self.price * (1 + (self.boom if state == "boom" else self.bust))

    def own(self, state: str) -> float:
        """Profit per home ($ thousand) if the lot is bought now and the home built and sold in ``years``."""
        s = self.sale(state)
        lot_cost = self.lot * (1 + self.carry) ** self.years
        return s - lot_cost - self.build - self.overhead * s

    def option(self, state: str) -> float:
        """Profit per home if the lot is optioned: in a boom the builder takes the lot at the escalated price; in a bust
        it walks away and loses the deposit."""
        s = self.sale(state)
        take = self.lot * (1 + self.escalator) ** self.years
        built = s - take - self.build - self.overhead * s
        return built if state == "boom" else max(built, -self.deposit)

    def capital(self, how: str) -> float:
        """Money tied up per home today ($ thousand)."""
        return self.lot if how == "own" else self.deposit

    def expected(self, how: str) -> float:
        f = self.own if how == "own" else self.option
        return (1 - self.p_bust) * f("boom") + self.p_bust * f("bust")

    def table(self) -> dict:
        out = {}
        for how in ("own", "option"):
            f = self.own if how == "own" else self.option
            out[how] = {"boom": f("boom"), "bust": f("bust"), "expected": self.expected(how), "capital": self.capital(how),
                        "return": self.expected(how) / self.capital(how)}
        return out

    def breakeven_bust(self) -> float:
        """The chance of a bust at which owning and optioning earn the same on average."""
        a = self.own("boom") - self.option("boom")
        b = self.option("bust") - self.own("bust")
        return a / (a + b)


def payment(principal: float, rate: float, years: int = 30) -> float:
    """The level monthly payment on a fixed-rate loan (rate a year, as a fraction)."""
    r, n = rate / 12, 12 * years
    return principal * r / (1 - (1 + r) ** -n) if r else principal / n


def balance(principal: float, rate: float, months: int, years: int = 30) -> float:
    """What is still owed after ``months`` level payments."""
    r = rate / 12
    p = payment(principal, rate, years)
    return principal * (1 + r) ** months - p * ((1 + r) ** months - 1) / r if r else principal - p * months
