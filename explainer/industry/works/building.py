"""The Works' building (Part 26): a commercial building valued as its income divided by a rate, a loan against it that
must be refinanced, and a development priced the same way.

The building.  ``sqft`` square feet let at ``rent`` dollars a square foot a year, ``occupancy`` of it let; its operating
costs (``costs``, $ million a year: taxes, insurance, cleaning, energy, management) are mostly fixed, so they are paid
whether the space is let or not.  Net operating income is the rent roll less the costs, and the value is that income
divided by the capitalization rate ``cap``, the yield a buyer demands.

The loan.  ``principal`` ($ million) at ``rate``, interest only, due at maturity.  To repay it the owner refinances:
a lender lends the least of ``ltv`` of the value, the amount whose interest the income covers ``dscr`` times, and the
amount that gives the lender a ``debt_yield`` (income over loan).  The gap between the old loan and the new is what
the owner must put in.  Its choices: pay the gap, hand the building to the lender, or ask the lender to extend.

The development.  Build at a cost, earn a stabilized income: the yield on cost over the cap rate, less one, is the
developer's margin.

All numbers are this series' illustrations, anchored on BXP's 86.7% office occupancy at the end of 2025, Prologis's rent
increases of about 50% on renewal in 2025, Realty Income's 7.3% yield on what it bought in 2025, the Federal Reserve's
average capitalization rate of 6.79% since 2001, and Prologis's 6.7% stabilized yield and 25.4% margin.  No manim.
"""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Building:
    sqft: float = 400_000.0
    rent: float = 50.0          # $ a square foot a year, on the space let
    occupancy: float = 0.95
    costs: float = 9.0          # $ million a year, mostly fixed
    cap: float = 0.05

    def rent_roll(self) -> float:
        """Rent collected, $ million a year."""
        return self.sqft * self.rent * self.occupancy / 1e6

    def noi(self) -> float:
        """Net operating income, $ million a year."""
        return self.rent_roll() - self.costs

    def value(self) -> float:
        """$ million: income over the capitalization rate."""
        return self.noi() / self.cap

    def but(self, **kw) -> "Building":
        return replace(self, **kw)


@dataclass(frozen=True)
class Loan:
    principal: float = 130.0    # $ million
    rate: float = 0.04

    def interest(self) -> float:
        return self.principal * self.rate


def refinance(b: Building, rate: float, ltv: float = 0.60, dscr: float = 1.25, debt_yield: float = 0.10) -> dict:
    """The largest new loan a lender offers against ``b`` at ``rate``, by each of its three tests, and which binds."""
    tests = {"ltv": ltv * b.value(), "dscr": b.noi() / (dscr * rate), "debt_yield": b.noi() / debt_yield}
    tests = {k: max(0.0, v) for k, v in tests.items()}
    binds = min(tests, key=tests.get)
    return dict(tests=tests, binds=binds, loan=tests[binds])


def maturity(b: Building, old: Loan, rate: float, equity: float, **kw) -> dict:
    """What happens when ``old`` falls due on ``b``: the new loan, the gap to fill, and the three choices.

    ``equity`` is what the owner put in at the start.  Paying the gap leaves the owner a building worth ``b.value()``
    with the new loan on it, having paid in the gap; handing over the keys loses the owner its equity and the lender
    the difference between the loan and the building's value; extending leaves both waiting."""
    r = refinance(b, rate, **kw)
    gap = max(0.0, old.principal - r["loan"])
    cash_out = max(0.0, r["loan"] - old.principal)
    v = b.value()
    return dict(value=v, new_loan=r["loan"], binds=r["binds"], tests=r["tests"], gap=gap, cash_out=cash_out,
                owner_equity=v - old.principal, ltv_now=old.principal / v if v > 0 else float("inf"),
                pay_in=dict(owner_cash=gap, owner_left=v - r["loan"], lender_loss=0.0),
                keys=dict(owner_cash=0.0, owner_loss=equity, lender_loss=max(0.0, old.principal - v)),
                extend=dict(owner_cash=0.0, interest_cover=b.noi() / old.interest() if old.interest() else float("inf")))


def value_at(noi: float, cap: float) -> float:
    return noi / cap


def rate_move(cap: float, move: float = 0.01) -> float:
    """The change in value when the capitalization rate rises by ``move`` with income unchanged."""
    return cap / (cap + move) - 1


def dev_margin(yield_on_cost: float, cap: float) -> float:
    """A development's margin: its stabilized value (income over the cap rate) over its cost, less one."""
    return yield_on_cost / cap - 1


def implied_cap(yield_on_cost: float, margin: float) -> float:
    """The cap rate implied by a reported stabilized yield and development margin."""
    return yield_on_cost / (1 + margin)


# The Run it pair: the same purchase in 2019, an office and a warehouse, and what each looks like in 2026.
OFFICE_2019 = Building()
OFFICE_2026 = Building(rent=48.0, occupancy=0.65, costs=9.5, cap=0.075)
SHED_2019 = Building(sqft=1_000_000, rent=11.0, occupancy=0.97, costs=0.67, cap=0.045)
SHED_2026 = Building(sqft=1_000_000, rent=16.5, occupancy=0.95, costs=0.75, cap=0.055)


def run_it() -> dict:
    """The two buildings bought in 2019 with 65% loans at 4% that fall due in 2026, refinanced at 7%."""
    out = {}
    for name, b0, b1 in (("office", OFFICE_2019, OFFICE_2026), ("warehouse", SHED_2019, SHED_2026)):
        loan = Loan(principal=round(0.65 * b0.value(), 1), rate=0.04)
        eq = b0.value() - loan.principal
        out[name] = dict(then=dict(rent_roll=b0.rent_roll(), noi=b0.noi(), value=b0.value(), cap=b0.cap, occupancy=b0.occupancy,
                                   rent=b0.rent, costs=b0.costs, cash_yield=(b0.noi() - loan.interest()) / eq),
                         now=dict(rent_roll=b1.rent_roll(), noi=b1.noi(), value=b1.value(), cap=b1.cap, occupancy=b1.occupancy,
                                  rent=b1.rent, costs=b1.costs),
                         loan=loan.principal, equity=eq, at=maturity(b1, loan, 0.07, eq))
    return out
