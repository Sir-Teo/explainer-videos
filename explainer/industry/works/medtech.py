"""The Works' device maker (Part 21): a surgical robot sold to hospitals, or placed in them for a fee per operation, with
instruments that wear out and a service contract; and what one robot costs a hospital over five years.

The ranges are Intuitive Surgical's (Form 10-K 2025): a da Vinci system sells for $0.7m to $3.1m, instruments and
accessories bring $900 to $3,700 an operation, service contracts $95,000 to $225,000 a year, and the average system did
about 300 operations in 2025.  The hospitals, their gain per operation and the maker's costs are this series'
illustrations.  No manim here.
"""

from __future__ import annotations

from dataclasses import dataclass, field


def _volumes(lo: float = 50.0, hi: float = 550.0, n: int = 101) -> tuple:
    return tuple(lo + (hi - lo) * i / (n - 1) for i in range(n))


@dataclass(frozen=True)
class Market:
    """Hospitals that would do ``volumes`` robotic operations a year each.  A hospital gains ``value`` an operation (the
    payment it receives above what the open or keyhole operation would have cost it) and pays ``instrument`` for the
    instruments each uses; a bought robot also carries a service contract.  The maker builds a robot for
    ``machine_cost``, instruments for ``instrument_cost`` an operation and services one for ``service_cost`` a year.  All
    flows last ``life`` years and are discounted at ``rate``."""
    volumes: tuple = field(default_factory=_volumes)
    value: float = 4000.0
    instrument: float = 1800.0
    instrument_cost: float = 550.0
    machine_cost: float = 0.9e6
    service: float = 160e3
    service_cost: float = 60e3
    life: int = 7
    rate: float = 0.08

    def annuity(self) -> float:
        return (1 - (1 + self.rate) ** -self.life) / self.rate

    def sell(self, price: float = 2.0e6) -> dict:
        """Sell each robot for ``price`` with a service contract: a hospital buys if its discounted gain covers the
        price."""
        a = self.annuity()
        per, buyers, ops = [], 0, 0.0
        for n in self.volumes:
            buys = a * (n * (self.value - self.instrument) - self.service) >= price
            v = price - self.machine_cost + a * (n * (self.instrument - self.instrument_cost) + self.service - self.service_cost)
            per.append(v if buys else 0.0)
            buyers += buys
            ops += n if buys else 0.0
        threshold = (price / a + self.service) / (self.value - self.instrument)
        return {"buyers": buyers, "value": sum(per), "ops": ops, "threshold": threshold, "per": per}

    def place(self, fee: float = 1000.0) -> dict:
        """Place each robot free, service included, and charge ``fee`` an operation on top of the instruments: a hospital
        takes one if each operation still gains it something."""
        a = self.annuity()
        per, takers, ops = [], 0, 0.0
        takes = self.value - self.instrument - fee >= 0
        for n in self.volumes:
            v = -self.machine_cost + a * (n * (self.instrument + fee - self.instrument_cost) - self.service_cost)
            per.append(v if takes else 0.0)
            takers += takes
            ops += n if takes else 0.0
        breakeven = (self.machine_cost / a + self.service_cost) / (self.instrument + fee - self.instrument_cost)
        return {"takers": takers, "value": sum(per), "ops": ops, "breakeven": breakeven, "per": per,
                "losers": sum(1 for v in per if v < 0)}

    def fee_to_match(self, price: float = 2.0e6) -> float:
        """The fee an operation at which placing earns the maker as much as selling at ``price``."""
        lo, hi, target = 0.0, self.value - self.instrument, self.sell(price)["value"]
        if self.place(hi)["value"] < target:
            return float("nan")
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if self.place(mid)["value"] < target else (lo, mid)
        return (lo + hi) / 2


def hospital_spend(system: float = 1.9e6, service: float = 160e3, per_op: float = 1825.0, ops: int = 300,
                   years: int = 5) -> dict:
    """What one robot costs a hospital over ``years``: the system (with its first year of service), service for the
    remaining years, and instruments for ``ops`` operations a year."""
    parts = {"system": system, "service": service * (years - 1), "instruments": per_op * ops * years}
    total = sum(parts.values())
    return {"parts": parts, "total": total, "shares": {k: v / total for k, v in parts.items()},
            "per_op": total / (ops * years)}
