"""The Works' drug company (Part 20): a candidate's road through the clinical phases, with BIO's phase success rates and
durations and illustrative costs; the cost of one approved drug once the failures and the years are counted; a drug's
revenue from launch to its patent cliff; and the Run it decision, whether to pay for Phase III once Phase II has shown
how big the market will be.

The success rates and durations are BIO, Informa and QLS's *Clinical Development Success Rates 2011-2020* (2021); the
costs, the peak sales and the erosion after the cliff are this series' illustrations, set beside the filings (Pfizer's
Lipitor, Merck's Keytruda, Lilly's tirzepatide) and the FDA's study of generic prices.  No manim here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# (name, years, cost in $m, probability of passing to the next stage)
PHASES = (("Phase I", 2.3, 25.0, 0.520), ("Phase II", 3.6, 60.0, 0.289), ("Phase III", 3.3, 250.0, 0.578),
          ("FDA review", 1.3, 5.0, 0.906))
# the brand's revenue in the years after generic entry, as a share of its last year of exclusivity (illustrative; the
# FDA finds generic prices 39% below the brand with one generic maker and more than 95% below with six or more)
CLIFF = (0.40, 0.12, 0.06, 0.04, 0.03)


def reach(phases=PHASES) -> list[float]:
    """The probability that a candidate entering Phase I reaches each stage, and finally approval."""
    out, p = [], 1.0
    for _, _, _, q in phases:
        out.append(p)
        p *= q
    out.append(p)
    return out


def cost_per_approval(phases=PHASES, rate: float = 0.105) -> dict:
    """Expected spending per candidate, and per approved drug: out of pocket, and capitalized to the day of approval at
    ``rate`` a year (each stage's cost spent at its start)."""
    r = reach(phases)
    spend = sum(c * p for (_, _, c, _), p in zip(phases, r))
    total_years = sum(y for _, y, _, _ in phases)
    cap, t = 0.0, 0.0
    for (_, y, c, _), p in zip(phases, r):
        cap += c * p * (1 + rate) ** (total_years - t)
        t += y
    return {"p_approval": r[-1], "spend": spend, "per_approval": spend / r[-1], "capitalized": cap / r[-1],
            "years": total_years, "reach": r}


@dataclass(frozen=True)
class Drug:
    """An approved drug's sales: a ramp to ``peak`` ($m a year) over ``ramp`` years, flat until exclusivity ends
    ``exclusivity`` years after launch, then the ``cliff``; ``margin`` of sales left after making and selling it."""
    peak: float = 2000.0
    ramp: int = 6
    exclusivity: int = 12
    margin: float = 0.6
    cliff: tuple = CLIFF
    rate: float = 0.105

    def sales(self, years: int = 20) -> list[float]:
        out = []
        for t in range(years):
            if t < self.exclusivity:
                out.append(self.peak * min(1.0, (t + 1) / self.ramp))
            else:
                k = t - self.exclusivity
                out.append(self.peak * (self.cliff[k] if k < len(self.cliff) else self.cliff[-1]))
        return out

    def npv(self, years: int = 20) -> float:
        return sum(s * self.margin / (1 + self.rate) ** (t + 1) for t, s in enumerate(self.sales(years)))


@dataclass(frozen=True)
class Option:
    """Run it: a candidate has passed Phase II, and the trial has shown whether its market is big or small.  Phase III
    costs ``phases[2]`` and succeeds with its probability; then review.  Is it worth paying for Phase III?"""
    big: Drug = field(default_factory=lambda: Drug(peak=3000.0))
    small: Drug = field(default_factory=lambda: Drug(peak=150.0))
    p_big: float = 0.3
    phases: tuple = PHASES

    def continue_value(self, drug: Drug) -> float:
        _, y3, c3, q3 = self.phases[2]
        _, y4, c4, q4 = self.phases[3]
        disc = (1 + drug.rate) ** (y3 + y4)
        return -c3 - q3 * c4 / (1 + drug.rate) ** y3 + q3 * q4 * drug.npv() / disc

    def summary(self) -> dict:
        vb, vs = self.continue_value(self.big), self.continue_value(self.small)
        commit = self.p_big * vb + (1 - self.p_big) * vs
        flexible = self.p_big * max(vb, 0.0) + (1 - self.p_big) * max(vs, 0.0)
        return {"big": vb, "small": vs, "commit": commit, "flexible": flexible, "option": flexible - commit,
                "npv_big": self.big.npv(), "npv_small": self.small.npv()}
