"""Monochord's rhythm engine (Part 11, *Rhythm and Meter*): time as a grid, and what a listener makes of it.

    meter_weights(groups)            a metre as nested groupings: how many levels each pulse of the bar belongs to
    onsets(pattern)                  "x..x..x." as positions
    syncopation(pattern, groups)     Longuet-Higgins and Lee's index (1984): notes on weak pulses before silent strong ones
    pulse(times, ...)                the beat a listener would tap: which period, and where it starts
    polyrhythm(a, b)                 a against b on their common grid
    compositions(n)                  every way to fill n pulses with beats of two and three
    swing(...)                       long-short eighths at a given ratio
    accelerando(...)                 clicks that speed up smoothly (rhythm into pitch)
    clicks(...)                      a click train as sound, band-limited
    reproduce / iterate              the telephone game on three-interval rhythms (Jacoby and McDermott's method, as a toy)

No manim.  Checked in ``tests/music/test_rhythm.py``.
"""

from __future__ import annotations

import math
from math import gcd

import numpy as np

from .audio import SR


# ---------------------------------------------------------------------------
# Metre: nested groupings
# ---------------------------------------------------------------------------
def meter_weights(groups) -> list[int]:
    """A bar as nested groupings, outermost first: (2, 2, 2, 2) is four-four down to sixteenths (the bar splits in
    two, each half in two, ...), (3, 2) is three-four down to eighths, (2, 3) is six-eight.  Returns, for every
    pulse of the bar, the number of levels of the metre on which it is a beat (Lerdahl and Jackendoff's dots): the
    downbeat has the most."""
    n = int(np.prod(groups))
    w = [0] * n
    step = n
    for k in range(len(groups) + 1):
        for i in range(0, n, step):
            w[i] += 1
        if k < len(groups):
            step //= groups[k]
    return w


def onsets(pattern: str) -> list[int]:
    """``"x..x..x."``: the positions of the notes (anything but ``.``, ``-`` or a space is a note)."""
    return [i for i, c in enumerate(pattern.replace(" ", "")) if c not in ".-"]


def syncopation(pattern: str, groups) -> int:
    """Longuet-Higgins and Lee's measure, on a pattern that repeats: wherever a note on a weak pulse is followed by
    silence on a stronger pulse (before the next note), add the difference of the two pulses' weights.  Zero for a
    rhythm that sounds every strong pulse it passes."""
    p = pattern.replace(" ", "")
    w = meter_weights(groups)
    n = len(p)
    if n != len(w):
        raise ValueError(f"the pattern has {n} pulses and the metre {len(w)}")
    notes = onsets(p)
    if not notes:
        return 0
    total = 0
    for k, a in enumerate(notes):
        b = notes[(k + 1) % len(notes)]
        span = (b - a) % n or n
        rests = [(a + j) % n for j in range(1, span)]             # the silent pulses before the next note
        if rests:
            strongest = max(w[r] for r in rests)
            if strongest > w[a]:
                total += strongest - w[a]
    return total


def rotate(pattern: str, k: int) -> str:
    p = pattern.replace(" ", "")
    return p[k % len(p):] + p[: k % len(p)]


# ---------------------------------------------------------------------------
# The pulse a listener finds
# ---------------------------------------------------------------------------
def resonance(period, preferred: float = 0.55, width: float = 1.0):
    """How readily a period is felt as a beat: a bump on a logarithmic axis centred near half a second (van Noorden
    and Moelants 1999; Parncutt 1994).  ``width`` is in octaves."""
    return np.exp(-0.5 * (np.log2(np.asarray(period, dtype=float) / preferred) / width) ** 2)


def pulse(times, weights=None, periods=None, sigma: float = 0.025, preferred: float = 0.55) -> dict:
    """The beat in a list of onset times.  For every candidate period and starting point a steady grid is laid over
    the onsets and scored by two fractions multiplied together: how many of the onsets fall on the grid, and how
    many of the grid's points have an onset.  (A grid that is too slow misses notes; one that is too fast is
    mostly empty.)  That is multiplied by how readily a period of that length is felt as a beat.  Returns the best
    period and phase, and the curve of scores against period."""
    t = np.asarray(times, dtype=float)
    a = np.ones(len(t)) if weights is None else np.asarray(weights, dtype=float)
    periods = np.geomspace(0.2, 2.4, 240) if periods is None else np.asarray(periods, dtype=float)
    def fit(T, step):
        best, where = 0.0, 0.0
        for phi in np.arange(0.0, T, step):
            grid = np.arange(t.min() + phi - T, t.max() + T, T)
            grid = grid[(grid >= t.min() - 1e-9) & (grid <= t.max() + 1e-9)]
            if len(grid) < 3:
                continue
            near = np.exp(-0.5 * ((t[None, :] - grid[:, None]) / sigma) ** 2)
            on_grid = float((near.max(axis=0) * a).sum() / a.sum())             # the share of the onsets that the grid explains
            filled = float(near.max(axis=1).mean())                             # the share of the grid that has an onset
            if on_grid * filled > best:
                best, where = on_grid * filled, float(phi)
        return best * float(resonance(T, preferred)), where

    scores = np.array([fit(T, 0.01)[0] for T in periods])
    k = int(np.argmax(scores))
    fine = np.linspace(0.97 * periods[k], 1.03 * periods[k], 61)                # the best period, looked at more closely
    best = max(((*fit(T, 0.005), T) for T in fine), key=lambda r: r[0])
    return {"period": float(best[2]), "phase": float(best[1]), "bpm": 60.0 / float(best[2]), "periods": periods, "scores": scores}


# ---------------------------------------------------------------------------
# Counting
# ---------------------------------------------------------------------------
def polyrhythm(a: int, b: int) -> dict:
    """``a`` equal notes against ``b`` in the same time, on the grid that holds both."""
    n = a * b // gcd(a, b)
    pa, pb = [i * n // a for i in range(a)], [i * n // b for i in range(b)]
    both = sorted(set(pa) | set(pb))
    gaps = [(both[(k + 1) % len(both)] - both[k]) % n or n for k in range(len(both))]
    return {"grid": n, "a": pa, "b": pb, "composite": both, "gaps": gaps, "together": sorted(set(pa) & set(pb))}


def compositions(n: int, parts=(2, 3)) -> list[tuple[int, ...]]:
    """Every way to fill ``n`` pulses with beats of the given lengths, in order: 7 is 2+2+3, 2+3+2 or 3+2+2."""
    if n == 0:
        return [()]
    out = []
    for p in parts:
        if p <= n:
            out += [(p, *rest) for rest in compositions(n - p, parts)]
    return out


def swing(pairs: int, beat: float, ratio: float = 2.0) -> list[float]:
    """The times of ``pairs`` long-short pairs of eighth notes, a beat to the pair: ``ratio`` is long over short
    (1 is straight, 2 is the triplet feel)."""
    long = beat * ratio / (1.0 + ratio)
    return [t for k in range(pairs) for t in (k * beat, k * beat + long)]


def accelerando(rate0: float, rate1: float, seconds: float) -> np.ndarray:
    """Click times for a train that speeds up smoothly (its rate grows by equal ratios in equal times): click k
    falls where the running count of clicks reaches k."""
    g = math.log(rate1 / rate0) / seconds
    total = rate0 * (math.exp(g * seconds) - 1.0) / g
    k = np.arange(int(total) + 1)
    return np.log(1.0 + k * g / rate0) / g


def clicks(times, seconds: float | None = None, level=1.0, sr: int = SR, width: float = 0.0004) -> np.ndarray:
    """A click at each time: a narrow smooth bump, placed between samples exactly, so that a fast train has a true
    pitch.  ``level`` may be one number or one per click."""
    t = np.asarray(times, dtype=float)
    n = int(((seconds if seconds is not None else t.max() + 0.05)) * sr)
    y = np.zeros(n)
    lv = np.full(len(t), float(level)) if np.isscalar(level) else np.asarray(level, dtype=float)
    half = int(4 * width * sr) + 1
    for tk, a in zip(t, lv):
        c = tk * sr
        i0 = int(c) - half
        idx = np.arange(max(i0, 0), min(int(c) + half + 1, n))
        if len(idx):
            y[idx] += a * np.exp(-0.5 * ((idx - c) / (width * sr)) ** 2)
    return y


# ---------------------------------------------------------------------------
# The telephone game on rhythms
# ---------------------------------------------------------------------------
def simplex_point(ratio) -> np.ndarray:
    """A rhythm of three intervals as fractions of its length: 1:1:2 is (0.25, 0.25, 0.5)."""
    r = np.asarray(ratio, dtype=float)
    return r / r.sum()


INTEGER_RHYTHMS = [(1, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 2, 2), (2, 1, 2), (2, 2, 1), (1, 1, 3), (1, 3, 1), (3, 1, 1),
                   (1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1), (2, 3, 3), (3, 2, 3), (3, 3, 2)]


def reproduce(stimulus, peaks, weights, rng, spread: float = 0.02, hearing: float = 0.05, hand: float = 0.008) -> np.ndarray:
    """One listener taps back a rhythm.  The listener's expectations are bumps of width ``spread`` at ``peaks``
    (points of the simplex) with the given weights; what is heard is the stimulus blurred by ``hearing``; what is
    tapped is drawn from what the listener then believes (expectation times evidence), with a little noise from
    the hand."""
    s = np.asarray(stimulus, dtype=float)
    x = s + rng.normal(0.0, hearing, 3)
    x -= (x.sum() - 1.0) / 3.0                                   # stay on the simplex
    pk = np.asarray(peaks, dtype=float)
    w = np.asarray(weights, dtype=float)
    d2 = ((pk - x) ** 2).sum(axis=1)
    resp = w * np.exp(-0.5 * d2 / (spread ** 2 + hearing ** 2))
    if resp.sum() <= 0:
        resp = w
    k = rng.choice(len(pk), p=resp / resp.sum())
    shrink = hearing ** 2 / (spread ** 2 + hearing ** 2)         # how far the belief moves from what was heard to the peak
    mean = x + shrink * (pk[k] - x)
    sd = math.sqrt(spread ** 2 * hearing ** 2 / (spread ** 2 + hearing ** 2))
    r = mean + rng.normal(0.0, sd, 3) + rng.normal(0.0, hand, 3)
    r -= (r.sum() - 1.0) / 3.0
    r = np.clip(r, 0.08, None)
    return r / r.sum()


def iterate(seeds, peaks, weights, rounds: int = 5, seed: int = 0, **kw) -> np.ndarray:
    """The telephone game: every seed rhythm is tapped back, the tapping is played to the listener again, and so on.
    Returns an array (rounds + 1, number of seeds, 3)."""
    rng = np.random.default_rng(seed)
    out = [np.asarray(seeds, dtype=float)]
    for _ in range(rounds):
        out.append(np.array([reproduce(s, peaks, weights, rng, **kw) for s in out[-1]]))
    return np.array(out)


def nearest_ratio(points, peaks) -> np.ndarray:
    """For every rhythm, the index of the nearest peak and its distance."""
    p = np.asarray(points, dtype=float)
    pk = np.asarray(peaks, dtype=float)
    d = np.sqrt(((p[:, None, :] - pk[None, :, :]) ** 2).sum(axis=2))
    return np.stack([d.argmin(axis=1), d.min(axis=1)], axis=1)
