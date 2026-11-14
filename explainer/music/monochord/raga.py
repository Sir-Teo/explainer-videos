"""Monochord's raga and tala (Part 34 of *Music, Built*).

    jawari_string(f0, seconds)       a string over a curved bridge (the tanpura's jawari), by finite differences with
                                     a one-sided contact; ``bridge=False`` gives the same string on a sharp bridge
    centroid_track(y)                spectral centroid over time: the jawari's rising-then-falling brightness
    SWARAS, SHRUTIS                  the twelve swaras and a common list of the twenty-two shrutis as just ratios
    THAATS                           Bhatkhande's ten thaats; ``thaat_space()`` the 32 scales they are drawn from
    melakarta(n), melakarta_number   Venkatamakhin's 72 parent scales, numbered as in Carnatic practice
    RAGAS                            ascent, descent and a characteristic phrase for a few ragas (as commonly taught)
    TALAS                            vibhag structure, clap/wave pattern and theka for a few talas
    tihai(cycle, start, phrase)      every way to place a phrase three times so that it lands on sam
    stroke(bol)                      tabla strokes by modal synthesis from Part 9's loaded membrane
    gamaka_contour(...)              a pitch contour with oscillation and glide, for synthesis
    pitch_histogram(contour)         a cents histogram folded to one octave, as computational raga analysis draws it
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

import numpy as np
from scipy.signal import resample_poly

from .audio import SR
from .instruments import percussion as PC

# ------------------------------------------------------------------------------------------------- the tanpura
def jawari_string(f0: float = 130.0, seconds: float = 3.0, n: int = 80, bridge: bool = True, depth: float = 0.008,
                  width: float = 0.03, pluck_at: float = 0.3, amp: float = 0.01, loss: float = 0.8, smooth: float = 0.004,
                  sr: int = SR) -> np.ndarray:
    """A string of unit length fixed at both ends, plucked, by the explicit finite-difference wave equation at the
    Courant limit (dt = dx / c).  With ``bridge`` a smooth curved obstacle, a parabola of the given ``depth`` over the
    first ``width`` of the string, stops it moving below the bridge surface (a one-sided contact: displacement is
    clamped to the surface and the velocity there set to zero), which is how the tanpura's flat bridge and its
    thread make the jawari.  ``smooth`` adds a loss that grows with frequency, as in a real string, so that without
    the bridge the tone dulls as it dies.  The output is the force on the far end, resampled to ``sr``."""
    dx = 1.0 / n
    rate = 2 * n * f0                                          # samples per second at dt = dx / c, c = 2 f0
    steps = int(seconds * rate)
    x = np.linspace(0, 1, n + 1)
    u = np.where(x < pluck_at, x / pluck_at, (1 - x) / (1 - pluck_at)) * amp
    u_prev = u.copy()
    surface = np.full(n + 1, -np.inf)
    if bridge:
        k = x <= width
        surface[k] = -depth * (1 - (x[k] / width)) ** 2       # rises from -depth at the nut end to 0 at the bridge edge
        surface[0] = 0.0
    out = np.empty(steps)
    damp = np.exp(-loss / rate)
    for t in range(steps):
        u_next = np.empty_like(u)
        u_next[1:-1] = (u[2:] + u[:-2] - u_prev[1:-1]) * damp
        u_next[1:-1] += smooth * (u_next[2:] + u_next[:-2] - 2 * u_next[1:-1])  # high wavenumbers lose more
        u_next[0] = u_next[-1] = 0.0
        if bridge:
            below = u_next < surface
            u_next[below] = surface[below]                     # the string cannot pass through the bridge
        out[t] = (u_next[-2] - u_next[-1]) / dx
        u_prev, u = u, u_next
    y = out - out.mean()
    # resample from rate to sr
    from math import gcd
    r = int(round(rate))
    g = gcd(r, sr)
    y = resample_poly(y, sr // g, r // g)
    return y / max(np.abs(y).max(), 1e-12)


def centroid_track(y: np.ndarray, sr: int = SR, frame: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """The spectral centroid (Hz) in frames of ``frame`` seconds."""
    n = int(frame * sr)
    ts, cs = [], []
    w = np.hanning(n)
    for i in range(0, len(y) - n, n // 2):
        seg = y[i:i + n] * w
        s = np.abs(np.fft.rfft(seg))
        f = np.fft.rfftfreq(n, 1 / sr)
        cs.append(float((s * f).sum() / max(s.sum(), 1e-12)))
        ts.append((i + n / 2) / sr)
    return np.array(ts), np.array(cs)


# ------------------------------------------------------------------------------------------------- swaras
SWARAS = [("Sa", 0), ("komal Re", 1), ("Re", 2), ("komal Ga", 3), ("Ga", 4), ("Ma", 5), ("tivra Ma", 6), ("Pa", 7),
          ("komal Dha", 8), ("Dha", 9), ("komal Ni", 10), ("Ni", 11)]
SARGAM = {0: "S", 1: "r", 2: "R", 3: "g", 4: "G", 5: "m", 6: "M", 7: "P", 8: "d", 9: "D", 10: "n", 11: "N"}

# A commonly quoted list of the 22 shrutis as just ratios (one of several modern reconstructions).
SHRUTIS = [Fraction(1), Fraction(256, 243), Fraction(16, 15), Fraction(10, 9), Fraction(9, 8), Fraction(32, 27), Fraction(6, 5),
           Fraction(5, 4), Fraction(81, 64), Fraction(4, 3), Fraction(27, 20), Fraction(45, 32), Fraction(729, 512), Fraction(3, 2),
           Fraction(128, 81), Fraction(8, 5), Fraction(5, 3), Fraction(27, 16), Fraction(16, 9), Fraction(9, 5), Fraction(15, 8),
           Fraction(243, 128)]


def cents(r) -> float:
    return 1200 * np.log2(float(r))


# ------------------------------------------------------------------------------------------------- thaats
THAATS = {
    "Bilawal": (0, 2, 4, 5, 7, 9, 11), "Khamaj": (0, 2, 4, 5, 7, 9, 10), "Kafi": (0, 2, 3, 5, 7, 9, 10),
    "Asavari": (0, 2, 3, 5, 7, 8, 10), "Bhairavi": (0, 1, 3, 5, 7, 8, 10), "Kalyan": (0, 2, 4, 6, 7, 9, 11),
    "Marwa": (0, 1, 4, 6, 7, 9, 11), "Purvi": (0, 1, 4, 6, 7, 8, 11), "Todi": (0, 1, 3, 6, 7, 8, 11), "Bhairav": (0, 1, 4, 5, 7, 8, 11),
}


def thaat_space() -> list[tuple]:
    """The 32 seven-note scales with Sa and Pa fixed and each of Re, Ga, Ma, Dha, Ni in one of its two forms."""
    out = []
    for re, ga, ma, dha, ni in product((1, 2), (3, 4), (5, 6), (8, 9), (10, 11)):
        out.append((0, re, ga, ma, 7, dha, ni))
    return out


def melakartas() -> list[tuple]:
    """Venkatamakhin's 72 parent scales in their traditional order (1 to 72)."""
    out = []
    for ma in (5, 6):
        for ri, ga in combinations((1, 2, 3, 4), 2):
            for dha, ni in combinations((8, 9, 10, 11), 2):
                out.append((0, ri, ga, ma, 7, dha, ni))
    return out


def melakarta_number(scale) -> int:
    return melakartas().index(tuple(scale)) + 1


MELA_NAMES = {15: "Mayamalavagowla", 20: "Natabhairavi", 22: "Kharaharapriya", 28: "Harikambhoji", 29: "Dheerashankarabharanam",
              8: "Hanumatodi", 65: "Mechakalyani"}

# ------------------------------------------------------------------------------------------------- ragas
# Ascent, descent and a characteristic phrase (pakad), as commonly taught; octave marks: '.' below a note = lower
# octave, "'" after = upper.  Semitones relative to Sa; these are simplifications of living practice.
RAGAS = {
    "Yaman": {"thaat": "Kalyan", "aroha": [-1, 2, 4, 6, 9, 11, 12], "avaroha": [12, 11, 9, 7, 6, 4, 2, 0],
              "pakad": [-1, 2, 4, 2, 0, 7, 6, 4, 2, 0], "time": "early night"},
    "Bhupali": {"thaat": "Kalyan", "aroha": [0, 2, 4, 7, 9, 12], "avaroha": [12, 9, 7, 4, 2, 0],
                "pakad": [4, 2, 0, -3, 0, 2, 4, 7, 4, 2, 0], "time": "early night"},
    "Bilawal": {"thaat": "Bilawal", "aroha": [0, 2, 4, 5, 7, 9, 11, 12], "avaroha": [12, 11, 9, 7, 5, 4, 2, 0],
                "pakad": [4, 5, 7, 9, 7, 5, 4, 2, 0], "time": "morning"},
}

# ------------------------------------------------------------------------------------------------- talas
TALAS = {
    "Teentaal": {"beats": 16, "vibhags": [4, 4, 4, 4], "marks": ["X", "2", "0", "3"],
                 "theka": ["dha", "dhin", "dhin", "dha", "dha", "dhin", "dhin", "dha", "dha", "tin", "tin", "ta", "ta", "dhin", "dhin", "dha"]},
    "Jhaptaal": {"beats": 10, "vibhags": [2, 3, 2, 3], "marks": ["X", "2", "0", "3"],
                 "theka": ["dhi", "na", "dhi", "dhi", "na", "ti", "na", "dhi", "dhi", "na"]},
    "Rupak": {"beats": 7, "vibhags": [3, 2, 2], "marks": ["0", "1", "2"],
              "theka": ["tin", "tin", "na", "dhi", "na", "dhi", "na"]},
    "Ektaal": {"beats": 12, "vibhags": [2, 2, 2, 2, 2, 2], "marks": ["X", "0", "2", "0", "3", "4"],
               "theka": ["dhin", "dhin", "dhage", "tirakita", "tu", "na", "kat", "ta", "dhage", "tirakita", "dhi", "na"]},
    "Adi": {"beats": 8, "vibhags": [4, 2, 2], "marks": ["laghu", "drutam", "drutam"], "theka": []},
}


def tihai(cycle: int, start: int, phrase_lengths=range(1, 33), gaps=range(0, 17), sub: int = 1) -> list[dict]:
    """Every tihai: a phrase of ``p`` units played three times with gaps of ``g`` units between, its first stroke on
    beat ``start`` (beats numbered from 1, sam being beat 1) and its last stroke exactly on a sam, counting in units of
    1/``sub`` of a beat.  With positions counted from 0 at sam, the first stroke is at s = (start - 1) * sub and the
    last at s + 3p + 2g - 1, which must be a multiple of the cycle: (start - 1) * sub + 3p + 2g - 1 = 0 (mod cycle * sub)."""
    n = cycle * sub
    s0 = (start - 1) * sub
    out = []
    for p in phrase_lengths:
        for g in gaps:
            end = s0 + 3 * p + 2 * g - 1
            if end % n == 0 and end > s0:
                out.append({"p": p, "g": g, "span": 3 * p + 2 * g, "end": end, "cycles": end // n})
    return out


# ------------------------------------------------------------------------------------------------- strokes
_RATIOS = None


def _tabla_ratios():
    global _RATIOS
    if _RATIOS is None:
        _RATIOS = [r["ratio"] for r in PC.tabla_modes(0.4, 9.0, 6)]
    return _RATIOS


def _dayan(f, seconds, damped=False, sr=SR):
    rat = _tabla_ratios()
    amps = [1.0, 0.8, 0.6, 0.45, 0.3, 0.2]
    decays = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0] if not damped else [25.0, 30.0, 35.0, 40.0, 45.0, 50.0]
    return PC.modal([f * r for r in rat], amps, decays, seconds, sr)


def _bayan(f, seconds, sr=SR):
    t = np.arange(int(seconds * sr)) / sr
    glide = f * (1 + 0.25 * np.exp(-t * 6))                      # a low skin, pressed by the heel: the pitch slides
    ph = 2 * np.pi * np.cumsum(glide) / sr
    y = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.exp(-2.5 * t) * np.clip(t / 0.003, 0, 1)
    return y / np.abs(y).max()


def stroke(bol: str, f_dayan: float = 262.0, f_bayan: float = 80.0, seconds: float = 0.6, sr: int = SR) -> np.ndarray:
    """A tabla stroke: na/ta (dayan, rim), tin (dayan, open), dhin/dha (dayan with bayan), ge (bayan), ka/kat (bayan,
    damped), tirakita (four quick damped strokes); each normalized to peak 1."""
    b = bol.lower()
    if b == "tirakita":
        out = np.zeros(int(seconds * sr))
        for i in range(4):
            s = _dayan(f_dayan, 0.12, damped=True, sr=sr) * (0.8 if i % 2 else 1.0)
            k = int(i * seconds / 4 * sr)
            out[k:k + len(s)] += s[: len(out) - k]
        return out / np.abs(out).max()
    if b in ("na", "ta", "ti", "tu"):
        y = _dayan(f_dayan, seconds, damped=(b == "ti"), sr=sr)
    elif b == "tin":
        y = _dayan(f_dayan, seconds, sr=sr) * 0.8
    elif b in ("dha", "dhin", "dhi", "dhage"):
        y = _dayan(f_dayan, seconds, sr=sr) + 0.9 * _bayan(f_bayan, seconds, sr=sr)
    elif b in ("ge", "ga"):
        y = _bayan(f_bayan, seconds, sr=sr)
    elif b in ("ka", "kat", "ke"):
        y = _bayan(f_bayan, seconds, sr=sr) * np.exp(-np.arange(int(seconds * sr)) / sr * 30)
    else:
        y = _dayan(f_dayan, seconds, sr=sr)
    return y / np.abs(y).max()


# ------------------------------------------------------------------------------------------------- gamaka
def gamaka_contour(notes, rate: int = 200, glide: float = 0.12, shake=None) -> np.ndarray:
    """A pitch contour (semitones, sampled at ``rate`` per second) through notes [(pitch, seconds), ...], gliding
    for ``glide`` seconds into each note (meend); ``shake`` maps a note index to (depth in semitones, cycles per
    second) for an oscillation (andolan)."""
    shake = shake or {}
    out = []
    prev = notes[0][0]
    for i, (p, d) in enumerate(notes):
        n = max(int(d * rate), 1)
        t = np.arange(n) / rate
        g = min(glide, d * 0.5)
        x = np.where(t < g, prev + (p - prev) * (0.5 - 0.5 * np.cos(np.pi * t / max(g, 1e-9))), p)
        if i in shake:
            depth, cps = shake[i]
            x = x + depth * 0.5 * (1 - np.cos(2 * np.pi * cps * t)) * (t >= g)
        out.append(x)
        prev = p
    return np.concatenate(out)


def voice_from_contour(contour, base_hz: float, rate: int = 200, sr: int = SR, partials: int = 8, rolloff: float = 0.65) -> np.ndarray:
    """A bowed-string-like additive tone following a contour of semitones above ``base_hz``."""
    t = np.arange(len(contour)) / rate
    ts = np.arange(int(len(contour) / rate * sr)) / sr
    m = np.interp(ts, t, contour)
    f = base_hz * 2 ** (m / 12)
    ph = 2 * np.pi * np.cumsum(f) / sr
    y = sum((rolloff ** k) * np.sin((k + 1) * ph) for k in range(partials))
    env = np.minimum(1, ts / 0.05) * np.minimum(1, (ts[-1] - ts) / 0.2)
    return y * env / partials


def pitch_histogram(contour, bins: int = 120) -> tuple[np.ndarray, np.ndarray]:
    """A histogram of pitch (cents above Sa, folded to one octave) from a contour in semitones."""
    c = (np.asarray(contour) * 100.0) % 1200.0
    h, e = np.histogram(c, bins=bins, range=(0, 1200))
    return (e[:-1] + e[1:]) / 2, h
