"""An exact probability engine on finite spaces: the build of Part 2 ("Chance, Counted").

    from explainer.stats.prob import Dist, coin, die
    three = die() ** 3                        # three dice: 216 equally likely ordered rolls
    three.map(sum).P(10), three.map(sum).P(9) # Fraction(1, 8), Fraction(25, 216): Galileo's answer
    (die() ** 4).P(lambda r: 6 in r)          # Fraction(671, 1296): de Mere's first bet
    die().given(lambda x: x > 3).E()          # Fraction(5, 1)

A :class:`Dist` is a finite probability space whose outcomes carry exact rational probabilities (``fractions.Fraction``):
Kolmogorov's axioms with Omega finite, where every subset is an event and additivity is a sum.  The operations are the
ones the part introduces, in order:

* ``P(event)``: an event is a predicate, a set of outcomes or a single outcome;
* ``given(event)``: conditioning, the slice renormalized (chapter 5);
* ``map(f)``: the distribution of the random variable ``f`` (chapter 10), its push-forward;
* ``E(f)``, ``var(f)``, ``moment(k)`` (chapters 11-12);
* ``*`` and ``**``: independent product spaces, outcomes as tuples (chapter 9); ``+`` and ``iid_sum``: the
  distribution of a sum of independent variables, by convolution;
* ``then(kernel)``: a two-stage experiment, a tree whose second stage depends on the first (chapter 5);
* ``pgf()``: the probability generating function's coefficients (chapter 13);
* ``sample(n, rng)``: draws, so every exact answer can be checked against simulation.

Nothing here is approximate: a probability printed on screen as a fraction is the exact value of the model.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import permutations, product
from typing import Callable, Hashable, Iterable

import numpy as np


def _as_event(event) -> Callable:
    if callable(event):
        return event
    if isinstance(event, (set, frozenset)):
        return lambda w: w in event
    return lambda w: w == event


class Dist:
    """A finite probability space: outcome -> Fraction, the weights summing to one (they are normalized on
    construction, so weights may be any nonnegative numbers, e.g. counts)."""

    def __init__(self, weights: dict):
        w = {k: Fraction(v) for k, v in weights.items() if Fraction(v) != 0}
        if any(v < 0 for v in w.values()):
            raise ValueError("probabilities must be nonnegative")
        total = sum(w.values(), Fraction(0))
        if total == 0:
            raise ValueError("an empty space: the event conditioned on has probability zero")
        self.p = {k: v / total for k, v in w.items()}

    # ---------------------------------------------------------------- building spaces
    @classmethod
    def uniform(cls, outcomes: Iterable[Hashable]) -> "Dist":
        """Equally likely outcomes: Cardano's and Laplace's classical probability, favourable over possible."""
        return cls({o: 1 for o in outcomes})

    def __mul__(self, other: "Dist") -> "Dist":
        """Independent product: (a, b) with probability p(a) q(b).  Tuples are flattened, so d * d * d has
        outcomes (x, y, z)."""
        out = {}
        for a, pa in self.p.items():
            for b, pb in other.p.items():
                ta = a if isinstance(a, tuple) and getattr(self, "_flat", False) else (a,)
                tb = b if isinstance(b, tuple) and getattr(other, "_flat", False) else (b,)
                out[ta + tb] = pa * pb
        d = Dist(out)
        d._flat = True
        return d

    def __pow__(self, n: int) -> "Dist":
        """n independent copies, outcomes as n-tuples."""
        if n < 1:
            raise ValueError("need n >= 1")
        d = Dist({(o,): p for o, p in self.p.items()})
        d._flat = True
        for _ in range(n - 1):
            d = d * self
        return d

    def __add__(self, other: "Dist") -> "Dist":
        """The distribution of X + Y for independent X ~ self, Y ~ other (convolution), without listing pairs."""
        out = defaultdict(Fraction)
        for a, pa in self.p.items():
            for b, pb in other.p.items():
                out[a + b] += pa * pb
        return Dist(dict(out))

    def iid_sum(self, n: int) -> "Dist":
        """The distribution of X_1 + ... + X_n, independent copies of self: n - 1 convolutions, so 24 throws of two
        dice need 24 small steps, not 36^24 outcomes."""
        d = self
        for _ in range(n - 1):
            d = d + self
        return d

    def then(self, kernel: Callable[[Hashable], "Dist"]) -> "Dist":
        """A two-stage experiment: draw a, then b from ``kernel(a)``; outcomes (a, b), probability p(a) q(b | a).
        This is the multiplication rule, P(A and B) = P(A) P(B | A), as a tree."""
        out = {}
        for a, pa in self.p.items():
            for b, pb in kernel(a).p.items():
                out[(a, b)] = out.get((a, b), 0) + pa * pb
        return Dist(out)

    # ---------------------------------------------------------------- probability
    def P(self, event) -> Fraction:
        """The probability of an event: the sum of its outcomes' probabilities (finite additivity)."""
        e = _as_event(event)
        return sum((p for o, p in self.p.items() if e(o)), Fraction(0))

    def given(self, event) -> "Dist":
        """Conditioning on an event of positive probability: keep its outcomes, rescale by 1 / P(event)."""
        e = _as_event(event)
        return Dist({o: p for o, p in self.p.items() if e(o)})

    def map(self, f: Callable) -> "Dist":
        """The distribution of the random variable f: P(f = v) = P({w : f(w) = v})."""
        out = defaultdict(Fraction)
        for o, p in self.p.items():
            out[f(o)] += p
        return Dist(dict(out))

    # ---------------------------------------------------------------- moments
    def E(self, f: Callable | None = None) -> Fraction:
        """Expectation, sum of f(w) p(w) (the law of the unconscious statistician when f is given)."""
        f = f or (lambda w: w)
        return sum((Fraction(f(o)) * p for o, p in self.p.items()), Fraction(0))

    def var(self, f: Callable | None = None) -> Fraction:
        f = f or (lambda w: w)
        m = self.E(f)
        return self.E(lambda w: (Fraction(f(w)) - m) ** 2)

    def moment(self, k: int, f: Callable | None = None) -> Fraction:
        f = f or (lambda w: w)
        return self.E(lambda w: Fraction(f(w)) ** k)

    def cdf(self, x) -> Fraction:
        return self.P(lambda w: w <= x)

    def pgf(self) -> list[Fraction]:
        """Coefficients of G(s) = E s^X for a variable with values in 0, 1, 2, ...: c[k] = P(X = k)."""
        if not all(isinstance(o, int) and o >= 0 for o in self.p):
            raise ValueError("a pgf needs values in 0, 1, 2, ...")
        c = [Fraction(0)] * (max(self.p) + 1)
        for o, p in self.p.items():
            c[o] = p
        return c

    # ---------------------------------------------------------------- the check
    def sample(self, n: int, rng: np.random.Generator) -> list:
        """n independent draws (for checking an exact answer against simulated frequencies)."""
        outs = list(self.p)
        probs = np.array([float(self.p[o]) for o in outs])
        idx = rng.choice(len(outs), size=n, p=probs / probs.sum())
        return [outs[i] for i in idx]

    # ---------------------------------------------------------------- display
    def items(self):
        try:
            return sorted(self.p.items())
        except TypeError:
            return sorted(self.p.items(), key=lambda kv: repr(kv[0]))

    def support(self) -> list:
        return [o for o, _ in self.items()]

    def __len__(self) -> int:
        return len(self.p)

    def __repr__(self) -> str:
        body = ", ".join(f"{o!r}: {p}" for o, p in self.items()[:8])
        more = ", ..." if len(self.p) > 8 else ""
        return f"Dist({{{body}{more}}})"


# ---------------------------------------------------------------- common spaces
def coin(p=Fraction(1, 2), heads="H", tails="T") -> Dist:
    return Dist({heads: Fraction(p), tails: 1 - Fraction(p)})


def die(sides=6) -> Dist:
    return Dist.uniform(range(1, sides + 1))


def faces(values: Iterable[int]) -> Dist:
    """A die with the given faces (repeats allowed): Sicherman's dice are faces([1, 2, 2, 3, 3, 4]) and
    faces([1, 3, 4, 5, 6, 8])."""
    out = defaultdict(int)
    for v in values:
        out[v] += 1
    return Dist(dict(out))


def shuffles(n: int) -> Dist:
    """A uniformly random permutation of 0..n-1 (the hat-check problem)."""
    return Dist.uniform(permutations(range(n)))


def convolve(a: list, b: list) -> list:
    """Polynomial product of two coefficient lists: the pgf of a sum of independent variables."""
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += Fraction(x) * Fraction(y)
    return out


def all_tuples(values, n) -> list:
    return list(product(values, repeat=n))
