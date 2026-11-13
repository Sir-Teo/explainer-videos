"""The Tune: *Ah! vous dirai-je, maman* (anonymous, France, 18th century), carried through every part of the series.

The world sings it as *Twinkle, Twinkle, Little Star*; Mozart wrote twelve variations on it (K. 265).  It is in the
public domain everywhere.  Here it is as data: scale degrees of a major scale (1 = the tonic) and lengths in beats,
six phrases of eight beats.  A part turns the degrees into sound with whatever it has just built.
"""

from __future__ import annotations

from fractions import Fraction

# (degree, beats): phrases A A' B B A A'
_A = [(1, 1), (1, 1), (5, 1), (5, 1), (6, 1), (6, 1), (5, 2)]
_A2 = [(4, 1), (4, 1), (3, 1), (3, 1), (2, 1), (2, 1), (1, 2)]
_B = [(5, 1), (5, 1), (4, 1), (4, 1), (3, 1), (3, 1), (2, 2)]
PHRASES = [_A, _A2, _B, _B, _A, _A2]
TUNE = [note for phrase in PHRASES for note in phrase]
BEATS = sum(b for _, b in TUNE)  # 48

DEGREE_NAME = {1: "C", 2: "D", 3: "E", 4: "F", 5: "G", 6: "A", 7: "B"}
# The just major scale: the ratios of the monochord (Part 1).  Part 6 is about the alternatives.
DEGREE_RATIO = {1: Fraction(1), 2: Fraction(9, 8), 3: Fraction(5, 4), 4: Fraction(4, 3), 5: Fraction(3, 2),
                6: Fraction(5, 3), 7: Fraction(15, 8)}
WORDS = ("Twin-", "kle,", "twin-", "kle,", "lit-", "tle", "star,")  # the first phrase, for a first-time listener


def events(beat: float = 0.55, phrases=None) -> list[dict]:
    """The Tune as a list of notes: ``{"i", "degree", "name", "ratio", "t", "dur", "phrase"}`` with times in
    seconds at ``beat`` seconds to the beat."""
    out, t, i = [], 0.0, 0
    for p, phrase in enumerate(PHRASES if phrases is None else [PHRASES[k] for k in phrases]):
        for degree, beats in phrase:
            out.append({"i": i, "degree": degree, "name": DEGREE_NAME[degree], "ratio": DEGREE_RATIO[degree],
                        "t": t, "dur": beats * beat, "phrase": p})
            t += beats * beat
            i += 1
    return out
