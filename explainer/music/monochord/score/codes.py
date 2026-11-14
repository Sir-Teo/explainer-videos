"""What a notation keeps, counted (Part 10).

    contour, count_contour, with_contour     neumes: up, down or the same, and how many tunes fit
    entropy, description_bits                how many bits a tune needs
    sizes                                    the bytes each encoding of a score takes
    gongche                                  the Tune in the characters of gongche notation
    binary_values, dotted                    durations: which sums of note values make a length
"""

from __future__ import annotations

import math
import zlib
from collections import Counter
from fractions import Fraction

import numpy as np

from . import Score, value, write


# ---------------------------------------------------------------------------
# Neumes: the contour of a melody
# ---------------------------------------------------------------------------
def contour(heights) -> list[int]:
    """+1 where the melody rises, -1 where it falls, 0 where it repeats: all that unheighted neumes record."""
    h = list(heights)
    return [(b > a) - (b < a) for a, b in zip(h, h[1:])]


def _ways(con, span: int) -> np.ndarray:
    """``ways[k][s]``: the number of ways to finish the melody from note ``k`` standing on step ``s``."""
    n = len(con) + 1
    ways = np.zeros((n, span), dtype=object)
    ways[-1, :] = 1
    for k in range(n - 2, -1, -1):
        for s in range(span):
            nxt = range(s + 1, span) if con[k] > 0 else range(0, s) if con[k] < 0 else (s,)
            ways[k, s] = sum(ways[k + 1, j] for j in nxt)
    return ways


def count_contour(con, span: int) -> int:
    """How many melodies on ``span`` steps of a scale have this contour."""
    return int(sum(_ways(con, span)[0]))


def with_contour(con, span: int, seed: int = 0) -> list[int]:
    """One of them, drawn so that each is equally likely (steps numbered from 0)."""
    rng = np.random.default_rng(seed)
    ways = _ways(con, span)

    def pick(options, k):
        w = np.array([float(ways[k, s]) for s in options])
        return int(options[rng.choice(len(options), p=w / w.sum())])

    out = [pick(list(range(span)), 0)]
    for k, c in enumerate(con):
        s = out[-1]
        options = list(range(s + 1, span)) if c > 0 else list(range(0, s)) if c < 0 else [s]
        out.append(pick(options, k + 1))
    return out


# ---------------------------------------------------------------------------
# Bits
# ---------------------------------------------------------------------------
def entropy(symbols) -> float:
    """Bits per symbol if each is coded by how often it occurs (Shannon's first-order entropy)."""
    c = Counter(symbols)
    n = sum(c.values())
    return -sum(v / n * math.log2(v / n) for v in c.values())


def description_bits(score: Score, voice: int = 0) -> dict:
    """Three counts of the bits in a voice: every note spelled out from a fixed menu; coded by frequency; and
    after a general-purpose compressor has found the repeats."""
    notes = [(e.pitch.name if not e.is_rest else "r", e.dur) for e in score.voices[voice].events]
    pitches = sorted({p for p, _ in notes})
    durs = sorted({d for _, d in notes})
    plain = len(notes) * (math.ceil(math.log2(len(pitches))) + math.ceil(math.log2(max(len(durs), 2))))
    h = entropy(notes)
    packed = bytes(pitches.index(p) * len(durs) + durs.index(d) for p, d in notes)
    return {"notes": len(notes), "pitches": len(pitches), "durations": len(durs), "plain_bits": plain, "entropy_bits_per_note": h,
            "entropy_bits": h * len(notes), "zlib_bits": 8 * len(zlib.compress(packed, 9)), "packed_bytes": len(packed)}


def sizes(score: Score) -> dict:
    """The bytes each of Monochord's writers needs for a score."""
    xml = write.musicxml(score).encode()
    out = {"MusicXML": len(xml), "MusicXML, zipped": len(zlib.compress(xml, 9)), "MEI": len(write.mei(score).encode()), "MIDI": len(write.midi(score)),
           "LilyPond": len(write.lilypond(score).encode()), "ABC": len(write.abc(score).encode()), "jianpu": len(write.jianpu(score).encode())}
    return out


# ---------------------------------------------------------------------------
# Gongche: the degrees of the scale as characters
# ---------------------------------------------------------------------------
GONGCHE = {-3: "合", -2: "四", -1: "一", 0: "上", 1: "尺", 2: "工", 3: "凡", 4: "六", 5: "五", 6: "乙"}      # steps above do
GONGCHE_NAMES = {"合": "he", "四": "si", "一": "yi", "上": "shang", "尺": "che", "工": "gong", "凡": "fan", "六": "liu", "五": "wu", "乙": "yi"}


def gongche(score: Score, voice: int = 0, tonic=None) -> list[str]:
    """The notes of a voice as gongche characters, with ``tonic`` (the first note by default) as 上."""
    notes = score.voices[voice].notes
    t = tonic or notes[0].pitch
    return [GONGCHE[n.pitch.diatonic - t.diatonic] for n in notes]


# ---------------------------------------------------------------------------
# Durations
# ---------------------------------------------------------------------------
def dotted(dots: int) -> Fraction:
    """How much longer ``dots`` dots make a note: 1, 3/2, 7/4, ... = 2 - 2^-dots."""
    return 2 - Fraction(1, 2 ** dots)


def binary_values(dur: Fraction, longest: Fraction = Fraction(1)) -> list[tuple[Fraction, int]]:
    """A length as tied notes, as few as possible: ``[(note value, dots), ...]``.  Runs of ones in the length's
    binary expansion become dotted notes (5/8 is a half tied to an eighth; 7/8 is a double-dotted half)."""
    dur = Fraction(dur)
    if dur.denominator & (dur.denominator - 1):
        raise ValueError(f"{dur} is not a sum of halvings of a whole note: it needs a tuplet")
    out = []
    v = Fraction(longest)
    while dur > 0:
        if v <= dur:
            dots = 0
            while dots < 2 and v * dotted(dots + 1) <= dur:
                dots += 1
            out.append((v, dots))
            dur -= v * dotted(dots)
        else:
            v /= 2
    return out


def value_name(v: Fraction, dots: int = 0) -> str:
    return ("double-dotted ", "dotted ", "")[2 - dots] + value(v)[0] if dots else value(v)[0]
