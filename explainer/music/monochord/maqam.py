"""Monochord's maqam (Part 35 of *Music, Built*): a maqam engine in cents.

    AJNAS                        the common ajnas (tetrachords and trichords) of Arabic theory, in cents, as usually
                                 taught on the 24-step grid (a 'quarter tone' = 50 cents)
    MAQAMAT                      maqamat as a lower jins on the tonic and an upper jins on the ghammaz
    maqam_scale(name)            the scale in cents above the tonic, one octave
    farabi_ratios()              al-Fārābī's and Zalzal's neutral intervals as ratios
    safi_17()                    Ṣafī al-Dīn's seventeen-tone Pythagorean gamut, by a chain of fourths
    edo_error(cents, n)          the nearest step of n equal divisions and its error
    AEU                          Turkish Arel–Ezgi–Uzdilek theory in Holdrian commas (1/53 octave)
    turkish_rast()               the Turkish Rast scale in commas and cents
    oud(hz, seconds)             a plucked string at an exact pitch (Karplus–Strong at four times the rate, retuned)
    darbuka(stroke)              dum, tek and ka on a goblet drum, from Part 9's membrane
    IQAAT                        rhythmic cycles: maqsum, baladi, samai thaqil, aksak
"""

from __future__ import annotations

from fractions import Fraction
from math import log2

import numpy as np

from .audio import SR
from .instruments import percussion as PC
from .instruments import strings as STR

# ------------------------------------------------------------------------------------------------- ajnas and maqamat
AJNAS = {
    "Rast": [0, 200, 350, 500],
    "Bayati": [0, 150, 300, 500],
    "Hijaz": [0, 100, 400, 500],
    "Saba": [0, 150, 300, 400],
    "Nahawand": [0, 200, 300, 500],
    "Kurd": [0, 100, 300, 500],
    "Ajam": [0, 200, 400, 500],
    "Sikah": [0, 150, 350],
}

# name: (lower jins, upper jins, ghammaz in cents where the upper jins starts)
MAQAMAT = {
    "Rast": ("Rast", "Rast", 700),
    "Bayati": ("Bayati", "Nahawand", 500),
    "Hijaz": ("Hijaz", "Nahawand", 500),
    "Saba": ("Saba", "Hijaz", 300),
    "Nahawand": ("Nahawand", "Hijaz", 700),
    "Kurd": ("Kurd", "Nahawand", 500),
    "Ajam": ("Ajam", "Ajam", 700),
}


def maqam_scale(name: str, octave: bool = True) -> list[float]:
    """Lower jins from the tonic, upper jins from the ghammaz, filled to the octave (Saba is the exception: it does
    not close at the octave, and its scale is returned as the two ajnas joined)."""
    lo, hi, g = MAQAMAT[name]
    notes = sorted(set(AJNAS[lo] + [g + c for c in AJNAS[hi]]))
    if name != "Saba" and octave:
        notes = [c for c in notes if c <= 1200]
        if 1200 not in notes:
            notes.append(1200)
    return [float(c) for c in notes]


def cents(r) -> float:
    return 1200 * log2(float(r))


def farabi_ratios() -> dict:
    """Neutral intervals from the medieval sources: Zalzal's wusta (neutral third) 27/22, and al-Fārābī's neutral
    second 12/11, against the Pythagorean and just thirds."""
    rs = {"Zalzal's neutral third 27/22": Fraction(27, 22), "neutral second 12/11": Fraction(12, 11),
          "Pythagorean minor third 32/27": Fraction(32, 27), "just minor third 6/5": Fraction(6, 5),
          "just major third 5/4": Fraction(5, 4), "Pythagorean major third 81/64": Fraction(81, 64)}
    return {k: cents(v) for k, v in rs.items()}


def safi_17() -> list[float]:
    """Ṣafī al-Dīn al-Urmawī's seventeen notes (13th century): a chain of pure fourths (and the octave), which
    divides each whole tone into limma, limma, comma: 90, 90, 24 cents."""
    pts = sorted(((k * cents(Fraction(4, 3))) % 1200) for k in range(17))
    return [float(round(p, 1)) for p in pts]


def edo_error(c: float, n: int) -> tuple[int, float]:
    k = round(c * n / 1200)
    return k, k * 1200 / n - c


# ------------------------------------------------------------------------------------------------- Turkish theory
COMMA = 1200 / 53
AEU = {"koma": 1, "bakiye": 4, "küçük mücennep": 5, "büyük mücennep": 8, "tanini": 9}


def turkish_rast() -> dict:
    """Rast in Arel–Ezgi–Uzdilek theory: steps of 9, 8, 5, 9, 9, 8, 5 commas (tanini, büyük mücennep, küçük mücennep...)."""
    steps = [9, 8, 5, 9, 9, 8, 5]
    pos = np.cumsum([0] + steps)
    return {"steps": steps, "commas": pos.tolist(), "cents": (pos * COMMA).tolist()}


# ------------------------------------------------------------------------------------------------- sounds
_OUD = None


def _body():
    global _OUD
    if _OUD is None:
        _OUD = STR.guitar_body()
    return _OUD


def oud(hz: float, seconds: float = 1.2, sr: int = SR, seed: int = 0, stretch: float = 0.5) -> np.ndarray:
    """A plucked gut string at an exact pitch: Karplus–Strong at four times the output rate (so the integer delay
    is fine), then read back at the rate that puts the pitch exactly at ``hz``, and through Part 7's guitar body."""
    hi = 4 * sr
    actual = STR.ks_pitch(hz, hi)
    y = STR.karplus_strong(hz, seconds * hz / actual + 0.05, sr=hi, seed=seed, stretch=stretch)
    t_in = np.arange(len(y)) / (hi * hz / actual)                  # the samples' times if the pitch were exactly hz
    t_out = np.arange(int(seconds * sr)) / sr
    out = np.interp(t_out, t_in, y)
    out = np.asarray(_body().play(out))
    n = len(t_out)
    out = out[:n] * np.minimum(1, (seconds - t_out[: len(out[:n])]) / 0.05)
    return out / max(np.abs(out).max(), 1e-12)


def darbuka(stroke: str, seconds: float = 0.5, sr: int = SR) -> np.ndarray:
    """dum: the centre of the head, low and ringing; tek: the rim, high and short; ka: tek with the other hand, softer."""
    if stroke == "dum":
        y = PC.drum(110.0, seconds=seconds, at=0.15, damping=7.0)
    else:
        y = PC.drum(420.0, seconds=seconds * 0.5, at=0.9, damping=25.0)
        if stroke == "ka":
            y = y * 0.6
    return y / np.abs(y).max()


# ------------------------------------------------------------------------------------------------- rhythm
IQAAT = {
    "maqsum": {"beats": 8, "strokes": ["dum", "tek", None, "tek", "dum", None, "tek", None]},
    "baladi": {"beats": 8, "strokes": ["dum", "dum", None, "tek", "dum", None, "tek", None]},
    "samai thaqil": {"beats": 10, "strokes": ["dum", None, None, "tek", None, "dum", "dum", "tek", None, None]},
    "aksak": {"beats": 9, "strokes": ["dum", None, "tek", None, "dum", None, "tek", "tek", None]},
}
