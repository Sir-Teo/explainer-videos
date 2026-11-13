"""Cueing: an observer who reads a questioner (videos/psychology/SYLLABUS.md, Part 2).

Clever Hans, as a mechanism.  The horse taps.  A questioner who knows the answer leans forward to count, and at the
right count relaxes: a slight upward jerk of the head, a millimetre or less (Pfungst 1907).  The horse stops when it
sees the jerk.  So the model has two parts,

* a **questioner**, who emits the cue at the right count when, and only when, the answer is known to him; and
* a **reader**, who detects a cue with a probability that falls with distance as a psychometric function,

      p(detect | distance D) = (1 - lapse) * Phi( log(D0 / D) / sigma ),

  because the visual angle of a fixed movement shrinks as 1 / D.  ``D0`` is the distance at which half the cues are
  seen, ``sigma`` the steepness on a log scale, and ``lapse`` the share of cues missed even at arm's length.

With no cue to read, the reader stops at some count of its own and is right at the rate ``guess``.

    from explainer.psychology.psyche.cueing import Reader, fit_hans
    hans = fit_hans()                              # the four numbers that reproduce Pfungst's table
    hans.p_correct(knows=True, sees=True, distance=0.4)

Four parameters and eight of Pfungst's conditions; the comparison is made in videos/psychology/psych2/compute.py.
Nothing here imports manim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
from scipy import optimize, stats

__all__ = ["Reader", "PFUNGST_CONDITIONS", "fit_hans", "simulate_session"]


@dataclass(frozen=True)
class Reader:
    """An observer of a questioner's involuntary cue."""

    d0: float = 4.0  # m: the distance at which half the cues are detected
    sigma: float = 0.08  # steepness of the fall with log distance
    lapse: float = 0.03  # cues missed at any distance
    guess: float = 0.07  # right by accident, with no cue to read

    def p_detect(self, distance) -> np.ndarray:
        """The probability of seeing the cue from ``distance`` metres."""
        d = np.asarray(distance, dtype=float)
        return (1 - self.lapse) * stats.norm.cdf(np.log(self.d0 / d) / self.sigma)

    def p_correct(self, knows: bool = True, sees: bool = True, distance: float = 0.4) -> float:
        """The probability of a right answer.  A cue exists only if the questioner ``knows`` the answer, and can
        be read only if the reader ``sees`` the questioner."""
        if not (knows and sees):
            return self.guess
        p = float(self.p_detect(distance))
        return p + (1 - p) * self.guess


# Pfungst's conditions (ch. II of the 1911 translation): (name, knows, sees, distance in m, tests, share correct).
# The usual distance was a quarter to half a metre.  The distance series is given in words, so its sample sizes
# are the 70 tests divided evenly, and its shares are read from "accurate up to 3.5 m", "a fall of 60 to 70%",
# "only one-third correct" and "no correct responses".
PFUNGST_CONDITIONS = (
    ("numerals, questioner knows", True, True, 0.4, 42, 0.98),
    ("numerals, questioner does not know", False, True, 0.4, 49, 0.08),
    ("blinders, questioner seen", True, True, 0.4, 56, 0.89),
    ("blinders, questioner not seen", True, False, 0.4, 35, 0.06),
    ("distance up to 3.5 m", True, True, 3.0, 18, 0.95),
    ("distance 3.5 to 4 m", True, True, 3.75, 18, 0.33),
    ("distance 4 to 4.5 m", True, True, 4.25, 17, 0.33),
    ("distance beyond 4.5 m", True, True, 5.0, 17, 0.0),
)


def _nll(theta, conditions) -> float:
    d0, sigma, lapse, guess = theta
    r = Reader(d0, sigma, lapse, guess)
    out = 0.0
    for _, knows, sees, dist, n, share in conditions:
        p = min(max(r.p_correct(knows, sees, dist), 1e-6), 1 - 1e-6)
        k = share * n
        out -= k * math.log(p) + (n - k) * math.log(1 - p)
    return out


def fit_hans(conditions=PFUNGST_CONDITIONS) -> Reader:
    """Maximum-likelihood values of the four parameters for Pfungst's eight conditions (binomial likelihood)."""
    best = None
    for d0 in (3.6, 3.9, 4.2):
        for sigma in (0.04, 0.1, 0.2):
            res = optimize.minimize(_nll, x0=(d0, sigma, 0.05, 0.07), args=(conditions,), method="L-BFGS-B",
                                    bounds=((2.0, 6.0), (0.01, 1.0), (0.001, 0.3), (0.001, 0.3)))
            if best is None or res.fun < best.fun:
                best = res
    return Reader(*map(float, best.x))


def simulate_session(reader: Reader, targets, knows: bool = True, sees: bool = True, distance: float = 0.4,
                     seed: int = 0, max_taps: int = 30) -> dict:
    """One sitting, tap by tap.  For each target number the reader taps until it sees the cue, which the
    questioner gives at the target count if he knows it; a missed cue, or no cue, lets the tapping run on to a
    count of the reader's own.  Returns the counts tapped and whether each was right."""
    rng = np.random.default_rng([1904, seed])
    targets = np.asarray(targets)
    p_cue = float(reader.p_detect(distance)) if (knows and sees) else 0.0
    # with no cue the horse stops at a habitual count: uniform over a range that makes ``guess`` the hit rate
    span = max(int(round(1 / reader.guess)), 2)
    tapped = np.empty(len(targets), dtype=int)
    for i, t in enumerate(targets):
        if rng.random() < p_cue:
            tapped[i] = t
        else:
            lo = max(1, int(t) - span // 2)
            tapped[i] = min(int(rng.integers(lo, lo + span)), max_taps)
    return {"targets": targets, "tapped": tapped, "correct": tapped == targets, "share": float((tapped == targets).mean())}


def with_distance(reader: Reader, d0: float) -> Reader:
    """The same reader with another half-detection distance (a sharper or a duller eye)."""
    return replace(reader, d0=d0)
