"""Frequencies, ratios, cents and note names.

Pitch in this module is a frequency in hertz or an exact ratio (:class:`fractions.Fraction`); the tuning systems that
turn one into the other are Part 6's (:mod:`.tuning`, to come).  Note names follow scientific pitch notation: A4 is
440 Hz, C4 is middle C.
"""

from __future__ import annotations

import math
import re
from fractions import Fraction

A4 = 440.0
NAMES_SHARP = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
_STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_NAME = re.compile(r"^([A-Ga-g])([#b♯♭]*)(-?\d+)$")


def cents(ratio) -> float:
    """The size of a frequency ratio in cents (1200 to the octave)."""
    return 1200.0 * math.log2(float(ratio))


def ratio_from_cents(c: float) -> float:
    return 2.0 ** (c / 1200.0)


def midi_to_hz(m: float, a4: float = A4) -> float:
    """Twelve-tone equal temperament: MIDI note 69 is A4."""
    return a4 * 2.0 ** ((m - 69) / 12.0)


def hz_to_midi(f: float, a4: float = A4) -> float:
    return 69 + 12 * math.log2(f / a4)


def name_to_midi(name: str) -> int:
    m = _NAME.match(name)
    if not m:
        raise ValueError(f"not a note name: {name!r}")
    letter, acc, octave = m.group(1).upper(), m.group(2), int(m.group(3))
    shift = sum(1 if a in "#♯" else -1 for a in acc)
    return 12 * (octave + 1) + _STEP[letter] + shift


def name_to_hz(name: str, a4: float = A4) -> float:
    """Equal-tempered frequency of a named note: ``name_to_hz("C3")`` is 130.81 Hz."""
    return midi_to_hz(name_to_midi(name), a4)


def midi_to_name(m: int) -> str:
    return f"{NAMES_SHARP[int(m) % 12]}{int(m) // 12 - 1}"


def nearest_note(f: float, a4: float = A4) -> tuple[str, float]:
    """The nearest equal-tempered note and the deviation from it in cents."""
    m = hz_to_midi(f, a4)
    k = int(round(m))
    return midi_to_name(k), 100.0 * (m - k)


# The intervals of the monochord: string length kept / frequency ratio.  Names as the Greeks had them and as we do.
MONOCHORD = {
    "unison": Fraction(1, 1),
    "octave": Fraction(2, 1),      # diapason: half the string
    "fifth": Fraction(3, 2),       # diapente: two thirds
    "fourth": Fraction(4, 3),      # diatessaron: three quarters
    "tone": Fraction(9, 8),        # the difference of a fifth and a fourth
}

# The just major scale (Ptolemy's intense diatonic), as frequency ratios above the open string.
JUST_MAJOR = {
    "C": Fraction(1), "D": Fraction(9, 8), "E": Fraction(5, 4), "F": Fraction(4, 3),
    "G": Fraction(3, 2), "A": Fraction(5, 3), "B": Fraction(15, 8), "C'": Fraction(2),
}
