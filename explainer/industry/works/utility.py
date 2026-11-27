"""The Works' regulated water company (Part 14): a regulatory capital value (RCV) indexed to inflation, allowed revenue
set for five years at a time, and what gearing does to the shareholders' return when debt is cheap and when it is not.

This is a simplified version of the English model (Ofwat's price reviews): the parameters are this series'
illustrations, labelled as models on screen.  No manim here.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WaterCo:
    rcv: float = 10000.0           # £ million, the regulatory capital value
    real_wacc: float = 0.04        # allowed real return on the RCV
    run_off: float = 0.04          # share of the RCV recovered from customers each year (regulatory depreciation)
    opex: float = 600.0            # £ million a year
    capex: float = 900.0           # £ million a year, added to the RCV
    customers: float = 6.0         # million households

    def year(self, inflation: float = 0.02) -> dict:
        """One year: allowed revenue (real terms), the bill per household, and next year's RCV (nominal, indexed)."""
        ret = self.rcv * self.real_wacc
        dep = self.rcv * self.run_off
        revenue = self.opex + dep + ret
        nxt = (self.rcv - dep + self.capex) * (1 + inflation)
        return dict(revenue=revenue, bill=revenue / self.customers, ret=ret, dep=dep, next_rcv=nxt)


def equity_return(asset_return: float, gearing: float, debt_cost: float) -> float:
    """The return on the shareholders' slice when the RCV earns ``asset_return`` and ``gearing`` of it is debt costing
    ``debt_cost``: the leverage formula, r_E = r_A + (r_A - r_D) * D/E."""
    if gearing >= 1:
        return float("inf") if asset_return > debt_cost else float("-inf")
    return asset_return + (asset_return - debt_cost) * gearing / (1 - gearing)


def leverage_table(asset_return: float, gearings, debt_costs) -> dict:
    return {(g, d): equity_return(asset_return, g, d) for g in gearings for d in debt_costs}
