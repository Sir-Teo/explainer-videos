"""The Stack and the cost curve (SYLLABUS §2.1, Part 4): what one more unit costs, and what that does to price.

* :func:`unit_costs` splits a plant's cost per unit into the fixed part, which falls as output rises, and the variable
  part, which does not; :func:`break_even` is the output at which price covers both;
* :func:`stack` lines up an industry's producers from cheapest to dearest marginal cost, the industry's supply curve,
  and :func:`clear` finds the price where it meets demand: the marginal producer sets the price, and every cheaper one
  earns the difference (its rent);
* :func:`wright` fits Wright's law, cost = a x cumulative^(-b), and gives the learning rate, the fall in cost with
  each doubling of cumulative output;
* :func:`scale_cost` is the rule of thumb that a plant's capital cost grows as its capacity to a power below one.

No manim, no data: plain arithmetic that the scenes, the lab and the tests call.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def unit_costs(fixed: float, variable: float, output: float) -> dict:
    """Average fixed, variable and total cost per unit at ``output`` units a period."""
    afc = fixed / output if output > 0 else float("inf")
    return dict(fixed=afc, variable=variable, total=afc + variable, marginal=variable)


def break_even(fixed: float, variable: float, price: float) -> float:
    """Units a period at which revenue covers fixed and variable costs; infinite if price does not cover variable."""
    return fixed / (price - variable) if price > variable else float("inf")


def operating_leverage(fixed: float, variable: float, price: float, output: float) -> float:
    """Percent change in operating profit for a 1% change in volume (contribution over profit)."""
    contribution = (price - variable) * output
    profit = contribution - fixed
    return contribution / profit if profit != 0 else float("inf")


@dataclass(frozen=True)
class Block:
    name: str
    capacity: float      # units a period (e.g. gigawatts)
    marginal: float      # cost of one more unit (e.g. $ per megawatt-hour)


def stack(blocks: list[Block]) -> list[tuple[Block, float, float]]:
    """Blocks sorted by marginal cost, each with its start and end on the cumulative capacity axis."""
    out, x = [], 0.0
    for b in sorted(blocks, key=lambda b: b.marginal):
        out.append((b, x, x + b.capacity))
        x += b.capacity
    return out


def clear(blocks: list[Block], demand: float) -> dict:
    """The price at which the stack meets a fixed demand: the marginal cost of the last block needed. Rents are what
    each running block earns above its own marginal cost on its output."""
    st = stack(blocks)
    total = st[-1][2] if st else 0.0
    if demand > total:
        raise ValueError(f"demand {demand} exceeds capacity {total}")
    price, rents, running = 0.0, {}, {}
    for b, x0, x1 in st:
        used = max(0.0, min(x1, demand) - x0)
        if used > 0:
            price = b.marginal
            running[b.name] = used
    for b, x0, x1 in st:
        used = running.get(b.name, 0.0)
        rents[b.name] = used * (price - b.marginal)
    return dict(price=price, running=running, rents=rents)


def wright(cumulative: list[float], cost: list[float]) -> dict:
    """Least-squares fit of log cost on log cumulative output: cost = a * cumulative ** (-b). The learning rate is
    the fall in cost per doubling, 1 - 2 ** (-b)."""
    xs = [math.log(c) for c in cumulative]
    ys = [math.log(c) for c in cost]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    a = math.exp(my - slope * mx)
    b = -slope
    resid = [y - (math.log(a) - b * x) for x, y in zip(xs, ys)]
    r2 = 1 - sum(e * e for e in resid) / sum((y - my) ** 2 for y in ys)
    return dict(a=a, b=b, learning_rate=1 - 2 ** (-b), progress_ratio=2 ** (-b), r2=r2)


def wright_cost(a: float, b: float, cumulative: float) -> float:
    return a * cumulative ** (-b)


def scale_cost(cost0: float, capacity0: float, capacity: float, exponent: float = 0.6) -> float:
    """Capital cost of a plant of ``capacity`` from a known plant, cost growing as capacity ** exponent."""
    return cost0 * (capacity / capacity0) ** exponent
