"""Tuning systems (Part 6, *Tuning*): where each one hides the comma.

Everything that can be exact is exact (``fractions.Fraction``): the commas, Pythagorean tuning, just intonation and
the comma pump.  Tempered systems are in cents.  A :class:`Tuning` is twelve pitch classes above C; it gives
frequencies, the sizes of its twelve fifths and twelve major thirds, and the beat rates a tuner would count.

Checked against Barbour's tables (*Tuning and Temperament*, 1951) in ``tests/music/test_tuning.py``.  No manim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

NAMES = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B")
FIFTHS_ORDER = ("Eb", "Bb", "F", "C", "G", "D", "A", "E", "B", "F#", "C#", "G#")     # the usual chain, wolf G#-Eb
PURE_FIFTH, PURE_THIRD, PURE_MINOR_THIRD = Fraction(3, 2), Fraction(5, 4), Fraction(6, 5)
PYTHAGOREAN_COMMA = Fraction(3 ** 12, 2 ** 19)          # twelve fifths against seven octaves: 23.46 cents
SYNTONIC_COMMA = Fraction(81, 80)                        # four fifths against a pure third and two octaves: 21.51
SCHISMA = PYTHAGOREAN_COMMA / SYNTONIC_COMMA             # 1.95 cents
DIESIS = Fraction(128, 125)                              # an octave against three pure thirds: 41.06


def cents(ratio) -> float:
    return 1200.0 * math.log2(float(ratio))


def fold(ratio: Fraction) -> Fraction:
    """A ratio brought into the octave [1, 2)."""
    r = Fraction(ratio)
    while r >= 2:
        r /= 2
    while r < 1:
        r *= 2
    return r


# ---------------------------------------------------------------------------
# A tuning: twelve pitch classes
# ---------------------------------------------------------------------------
@dataclass
class Tuning:
    name: str
    cents: tuple            # cents above C for C, C#, D, Eb, E, F, F#, G, G#, A, Bb, B
    ratios: tuple | None = None   # exact ratios, where the system has them

    def pc(self, name: str) -> float:
        return self.cents[NAMES.index(name)]

    def hz(self, name: str, octave: int = 4, a4: float = 440.0) -> float:
        """The frequency of a note, with the A above middle C at ``a4``."""
        c = self.pc(name) - self.pc("A") + 1200.0 * (octave - 4)
        return a4 * 2 ** (c / 1200.0)

    def interval(self, low: str, high: str) -> float:
        """The size in cents of the interval from ``low`` up to ``high`` (within an octave)."""
        return (self.pc(high) - self.pc(low)) % 1200.0

    def fifths(self) -> list[tuple[str, float]]:
        """The twelve fifths round the circle, C-G first: (lower note, size in cents)."""
        out, i = [], 0
        for _ in range(12):
            out.append((NAMES[i], self.interval(NAMES[i], NAMES[(i + 7) % 12])))
            i = (i + 7) % 12
        return out

    def thirds(self) -> list[tuple[str, float]]:
        """The twelve major thirds, in circle-of-fifths order of their lower note."""
        out, i = [], 0
        for _ in range(12):
            out.append((NAMES[i], self.interval(NAMES[i], NAMES[(i + 4) % 12])))
            i = (i + 7) % 12
        return out

    def triad_error(self, root: str) -> float:
        """How far the major triad on ``root`` is from pure: the root-mean-square error (cents) of its third and fifth."""
        i = NAMES.index(root)
        third = self.interval(root, NAMES[(i + 4) % 12]) - cents(PURE_THIRD)
        fifth = self.interval(root, NAMES[(i + 7) % 12]) - cents(PURE_FIFTH)
        return math.sqrt((third ** 2 + fifth ** 2) / 2)


def from_fifths(name: str, sizes: dict[str, float] | float) -> Tuning:
    """A tuning built along the chain Eb-Bb-F-C-G-D-A-E-B-F#-C#-G#, each fifth of the given size in cents (one
    number for all, or a size for the fifth above each named note)."""
    pos = {"C": 0.0}
    k = FIFTHS_ORDER.index("C")
    for j in range(k, len(FIFTHS_ORDER) - 1):                       # upwards from C
        low, high = FIFTHS_ORDER[j], FIFTHS_ORDER[j + 1]
        size = sizes if isinstance(sizes, (int, float)) else sizes.get(low, cents(PURE_FIFTH))
        pos[high] = (pos[low] + size) % 1200.0
    for j in range(k, 0, -1):                                       # downwards from C
        high, low = FIFTHS_ORDER[j], FIFTHS_ORDER[j - 1]
        size = sizes if isinstance(sizes, (int, float)) else sizes.get(low, cents(PURE_FIFTH))
        pos[low] = (pos[high] - size) % 1200.0
    return Tuning(name, tuple(pos[n] for n in NAMES))


def pythagorean() -> Tuning:
    """Eleven pure fifths, Eb to G#; the twelfth, G#-Eb, takes the whole comma."""
    exact = {"C": Fraction(1)}
    k = FIFTHS_ORDER.index("C")
    for j in range(k, 11):
        exact[FIFTHS_ORDER[j + 1]] = fold(exact[FIFTHS_ORDER[j]] * PURE_FIFTH)
    for j in range(k, 0, -1):
        exact[FIFTHS_ORDER[j - 1]] = fold(exact[FIFTHS_ORDER[j]] / PURE_FIFTH)
    return Tuning("Pythagorean", tuple(cents(exact[n]) for n in NAMES), tuple(exact[n] for n in NAMES))


JUST = {"C": Fraction(1), "C#": Fraction(16, 15), "D": Fraction(9, 8), "Eb": Fraction(6, 5), "E": Fraction(5, 4), "F": Fraction(4, 3),
        "F#": Fraction(45, 32), "G": Fraction(3, 2), "G#": Fraction(8, 5), "A": Fraction(5, 3), "Bb": Fraction(9, 5), "B": Fraction(15, 8)}


def just() -> Tuning:
    """Just intonation on C: every note a ratio of small powers of 2, 3 and 5."""
    return Tuning("just intonation", tuple(cents(JUST[n]) for n in NAMES), tuple(JUST[n] for n in NAMES))


def meantone(fraction: Fraction = Fraction(1, 4)) -> Tuning:
    """Each fifth of the chain narrowed by ``fraction`` of the syntonic comma.  A quarter makes four fifths a pure
    major third; the leftover falls on G#-Eb, the wolf."""
    size = cents(PURE_FIFTH) - float(fraction) * cents(SYNTONIC_COMMA)
    f = Fraction(fraction)
    return from_fifths(f"{f.numerator}/{f.denominator}-comma meantone", size)


def werckmeister3() -> Tuning:
    """Werckmeister's third temperament (1691): C-G, G-D, D-A and B-F# each narrowed by a quarter of the Pythagorean
    comma; the other eight fifths pure.  Every key is usable and no two are alike."""
    narrow = cents(PURE_FIFTH) - cents(PYTHAGOREAN_COMMA) / 4
    return from_fifths("Werckmeister III", {"C": narrow, "G": narrow, "D": narrow, "B": narrow})


def equal(n: int = 12) -> Tuning:
    """n equal steps to the octave.  The twelve note names are placed along a chain of the system's best fifth."""
    fifth = round(n * math.log2(1.5))
    t = from_fifths(f"{n} equal", 1200.0 * fifth / n)
    return t


def equal_just(n: int) -> Tuning:
    """n equal steps, each of the twelve notes on the step nearest its ratio in just intonation: how a player with
    n keys to the octave would play in C.  (For 12, 19 and 31 this is the same as :func:`equal`; for 41 and 53 it
    finds the nearly pure thirds that a chain of fifths passes by.)"""
    return Tuning(f"{n} equal", tuple(1200.0 * step_of(n, JUST[name]) / n for name in NAMES))


def step_of(n: int, ratio) -> int:
    """The number of steps of ``n`` equal that best approximates a ratio."""
    return round(n * math.log2(float(ratio)))


def edo_errors(n: int) -> dict:
    """How far ``n`` equal's best fifth and best major third are from pure (cents, signed)."""
    return {"n": n, "fifth_steps": step_of(n, 1.5), "fifth_error": 1200.0 * step_of(n, 1.5) / n - cents(PURE_FIFTH),
            "third_steps": step_of(n, 1.25), "third_error": 1200.0 * step_of(n, 1.25) / n - cents(PURE_THIRD),
            "third_from_fifths_error": (4 * 1200.0 * step_of(n, 1.5) / n) % 1200.0 - cents(PURE_THIRD)}


# ---------------------------------------------------------------------------
# Why twelve: continued fractions
# ---------------------------------------------------------------------------
def continued_fraction(x: float, terms: int = 10) -> list[int]:
    out = []
    for _ in range(terms):
        a = math.floor(x)
        out.append(a)
        if x - a < 1e-12:
            break
        x = 1.0 / (x - a)
    return out


def convergents(cf: list[int]) -> list[Fraction]:
    """The best rational approximations given by a continued fraction."""
    out = []
    h0, h1, k0, k1 = 1, cf[0], 0, 1
    out.append(Fraction(h1, k1))
    for a in cf[1:]:
        h0, h1 = h1, a * h1 + h0
        k0, k1 = k1, a * k1 + k0
        out.append(Fraction(h1, k1))
    return out


def root12_of_2(digits: int = 24) -> str:
    """The twelfth root of two to ``digits`` decimal places, by integer arithmetic (Newton's method on big integers)."""
    scale = 10 ** (digits + 4)
    target = 2 * scale ** 12
    x = int(1.0594630943592953 * scale)
    for _ in range(60):
        x_new = (11 * x + target // x ** 11) // 12
        if x_new == x:
            break
        x = x_new
    s = str(x)[: digits + 1]
    return s[0] + "." + s[1:]


# ---------------------------------------------------------------------------
# Beats: what a tuner counts
# ---------------------------------------------------------------------------
def beat_rate(low_hz: float, high_hz: float, p: int, q: int) -> float:
    """The beats a second between two notes that are nearly p:q (high:low): partial q of the upper against partial
    p of the lower.  Positive if the interval is wide."""
    return q * high_hz - p * low_hz


def tuner_table(t: Tuning, a4: float = 440.0) -> list[dict]:
    """The beat rates of the fifths, fourths and thirds a tuner uses to set a temperament in the octave F3 to F4."""
    seq = [("A", 3, "E", 4, 3, 2, "fifth"), ("A", 3, "D", 4, 4, 3, "fourth"), ("F", 3, "C", 4, 3, 2, "fifth"), ("G", 3, "D", 4, 3, 2, "fifth"),
           ("F", 3, "A", 3, 5, 4, "major third"), ("C", 4, "E", 4, 5, 4, "major third"), ("G", 3, "B", 3, 5, 4, "major third")]
    out = []
    for lo, lo_oct, hi, hi_oct, p, q, kind in seq:
        a, b = t.hz(lo, lo_oct, a4), t.hz(hi, hi_oct, a4)
        out.append({"low": f"{lo}{lo_oct}", "high": f"{hi}{hi_oct}", "kind": kind, "low_hz": a, "high_hz": b, "beats": beat_rate(a, b, p, q)})
    return out


# ---------------------------------------------------------------------------
# The comma pump
# ---------------------------------------------------------------------------
TRIADS = {"major": (Fraction(1), PURE_THIRD, PURE_FIFTH), "minor": (Fraction(1), PURE_MINOR_THIRD, PURE_FIFTH)}
PUMP = (("C", "major"), ("A", "minor"), ("D", "minor"), ("G", "major"), ("C", "major"))     # I vi ii V I


def comma_pump(rounds: int = 1, progression=PUMP) -> list[dict]:
    """A progression sung in pure triads, each chord keeping the pitch of the notes it shares with the one before.
    Returns the chords with the exact ratio of every note to the starting C.  After I-vi-ii-V-I the tonic comes
    back a syntonic comma (80/81) below where it began."""
    def pcs(root, quality):
        i = NAMES.index(root)
        return [NAMES[i], NAMES[(i + (4 if quality == "major" else 3)) % 12], NAMES[(i + 7) % 12]]

    chords = []
    held: dict[str, Fraction] = {}
    for r in range(rounds):
        steps = progression if r == 0 else progression[1:]
        for root, quality in steps:
            names = pcs(root, quality)
            shape = dict(zip(names, TRIADS[quality]))
            common = [n for n in names if n in held]
            if not chords:
                base = Fraction(1)                                  # the first chord: its root is the reference
            else:
                n0 = common[0]
                base = held[n0] / shape[n0]
                if len(common) > 1:                                 # shared notes must agree, or the triad is not pure
                    assert all(held[n] == fold(base * shape[n]) or fold(held[n]) == fold(base * shape[n]) for n in common)
            notes = {n: fold(base * shape[n]) for n in names}
            held = notes
            chords.append({"root": root, "quality": quality, "notes": notes, "root_ratio": notes[root], "root_cents": cents(notes[root]) % 1200.0})
    return chords


def pump_drift(rounds: int = 1) -> float:
    """How far (cents, negative is flat) the tonic has moved after ``rounds`` times round I-vi-ii-V-I."""
    if rounds <= 0:
        return 0.0
    chords = comma_pump(rounds)
    last = chords[-1]["root_ratio"]
    c = cents(last)                                       # one round's drift, folded: the pump repeats exactly
    one = c - 1200.0 if c > 600 else c
    return one if rounds == 1 else rounds * pump_drift(1)


# ---------------------------------------------------------------------------
# The piano's stretched octaves
# ---------------------------------------------------------------------------
def stiff_partial(f1: float, n: int, b: float) -> float:
    """Partial n of a stiff string whose first partial is f1: n f0 sqrt(1 + B n^2), with f0 = f1 / sqrt(1 + B)."""
    return f1 * n * math.sqrt((1 + b * n * n) / (1 + b))


def stretched_octave(b_low: float, b_high: float | None = None, m: int = 1) -> float:
    """How wide (cents above 1200) an octave must be to be beatless when partial 2m of the lower string is matched
    to partial m of the upper (m = 1 is the 2:1 octave of the treble, 2 the 4:2 of the middle, 3 the 6:3 of the
    bass); the strings have inharmonicities ``b_low`` and ``b_high``."""
    b_high = b_low if b_high is None else b_high
    return cents(stiff_partial(1.0, 2 * m, b_low) / (2.0 * stiff_partial(1.0, m, b_high)))


def piano_b(key: int) -> float:
    """A model of a grand piano's inharmonicity by key (1 = A0, 49 = A4, 88 = C8): least in the tenor, a little
    larger in the wound bass strings, a hundred times larger at the top (after the measurements summarised by
    Fletcher and Rossing, *The Physics of Musical Instruments*, ch. 12)."""
    if key >= 25:
        return 10 ** (-4.0 + 2.2 * (key - 25) / 63.0)      # 0.0001 at C3, 0.016 at C8
    return 10 ** (-4.0 + 0.6 * (25 - key) / 24.0)          # 0.0004 at A0


def octave_weights(key: int) -> tuple[float, float, float]:
    """How a tuner judges the octave above this key: by the 6:3 partials in the bass, 4:2 in the middle and 2:1 in
    the treble, passing gradually from one to the next.  Returns the weights of (2:1, 4:2, 6:3)."""
    w3 = min(max((34 - key) / 12.0, 0.0), 1.0)
    w1 = min(max((key - 46) / 12.0, 0.0), 1.0)
    return w1, 1.0 - w1 - w3, w3


def tuner_octave(b_low: float, b_high: float, key: int) -> float:
    """The stretch (cents) of the octave above ``key`` as a tuner sets it."""
    return sum(w * stretched_octave(b_low, b_high, m) for m, w in zip((1, 2, 3), octave_weights(key)))


def railsback(b_of_key=piano_b, lo: int = 1, hi: int = 88, reference: int = 49) -> list[float]:
    """The deviation from equal temperament (cents) of each key of a piano on which every octave is beatless, the
    stretch of each octave shared evenly among its twelve steps, with the A above middle C (key 49) left where it
    is.  This is the shape of Railsback's curve (1938): flat in the bass, sharp in the treble."""
    def step(k: int) -> float:                           # the stretch of the semitone above key k
        return tuner_octave(b_of_key(k), b_of_key(k + 12), k) / 12.0

    dev = {reference: 0.0}
    for k in range(reference + 1, hi + 1):
        dev[k] = dev[k - 1] + step(k - 7)                # the octave centred on this step
    for k in range(reference - 1, lo - 1, -1):
        dev[k] = dev[k + 1] - step(k - 6)
    return [dev[k] for k in range(lo, hi + 1)]
