"""Monochord's song studio (Part 40 of *Music, Built*): drum-machine voices from their circuits' principles,
sidechain ducking, sampling by slices, and measures of prosody and flow.

    kick808(f, decay)            a resonator struck by a pulse (the TR-808 bass drum's bridged-T network, as a damped
                                 oscillator whose pitch sags briefly after the strike) plus the strike's click
    snare808, clap808            two resonators and filtered noise; three bursts of noise and a tail
    hat808(open_)                six square-wave oscillators at inharmonic frequencies, high-passed, gated short or long
    PATTERNS                     step patterns (16 steps a bar) for rock, funk, disco, house and a trap-style beat
    sidechain(y, hits)           a compressor keyed by the kick: the pad's gain dips at each hit and recovers
    chop(y, n, order)            cut a recording into n equal slices and play them in a new order (sampling)
    prosody(syllables)           how often stressed syllables fall on strong positions of the bar, and unstressed ones on
                                 weak ones
    flow(syllables)              a rap verse's rhythm: syllables a beat, the share on beats, the gaps between accented
                                 syllables (twos and threes, after Ohriner), rhyme density and where rhymes fall
"""

from __future__ import annotations

from collections import Counter

import numpy as np
from scipy.signal import butter, sosfilt

from .audio import SR

HAT_HZ = (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)             # the six square-wave oscillators of the 808's metal sounds


def _env(n, decay, sr=SR):
    t = np.arange(n) / sr
    return np.exp(-t / decay)


def kick808(f: float = 52.0, decay: float = 0.45, seconds: float | None = None, bend: float = 0.6, click: float = 0.25,
            sr: int = SR) -> np.ndarray:
    """A struck resonator: a sine at ``f`` dying with time constant ``decay``, its frequency raised by ``bend`` at the
    instant of the strike and relaxing within 20 ms (the 808's trigger pulse briefly detunes its bridged-T network),
    plus a 1 ms click from the pulse itself."""
    seconds = seconds or max(0.3, 5 * decay)
    n = int(seconds * sr)
    t = np.arange(n) / sr
    freq = f * (1.0 + bend * np.exp(-t / 0.02))
    phase = 2 * np.pi * np.cumsum(freq) / sr
    y = np.sin(phase) * np.exp(-t / decay)
    k = int(0.001 * sr)
    y[:k] += click * np.hanning(2 * k)[:k][::-1] * 2
    y *= np.clip(t / 0.0005, 0, 1)
    return y / np.abs(y).max()


def snare808(seconds: float = 0.3, tone: float = 0.5, snappy: float = 0.6, seed: int = 0, sr: int = SR) -> np.ndarray:
    n = int(seconds * sr)
    t = np.arange(n) / sr
    body = 0.6 * np.sin(2 * np.pi * 238 * t) * np.exp(-t / 0.06) + 0.4 * np.sin(2 * np.pi * 476 * t) * np.exp(-t / 0.04)
    rng = np.random.default_rng(seed)
    nz = sosfilt(butter(2, 1800, btype="high", fs=sr, output="sos"), rng.standard_normal(n)) * np.exp(-t / 0.07)
    y = tone * body + snappy * nz / np.abs(nz).max()
    return y / np.abs(y).max()


def clap808(seed: int = 0, sr: int = SR) -> np.ndarray:
    n = int(0.35 * sr)
    t = np.arange(n) / sr
    rng = np.random.default_rng(seed)
    nz = sosfilt(butter(2, [700, 2400], btype="band", fs=sr, output="sos"), rng.standard_normal(n))
    env = np.zeros(n)
    for k, dt in enumerate((0.0, 0.011, 0.022)):
        i = int(dt * sr)
        env[i:] += np.exp(-(t[: n - i]) / 0.006)
    env += 0.5 * np.exp(-np.maximum(t - 0.025, 0) / 0.09) * (t > 0.025)
    y = nz * env
    return y / np.abs(y).max()


def hat808(open_: bool = False, sr: int = SR) -> np.ndarray:
    """Six square waves at fixed inharmonic frequencies, summed, high-passed, and gated: a short decay for closed, a
    long one for open."""
    seconds = 0.6 if open_ else 0.09
    n = int(seconds * sr)
    t = np.arange(n) / sr
    y = sum(np.sign(np.sin(2 * np.pi * f * t + 0.7 * k)) for k, f in enumerate(HAT_HZ))
    y = sosfilt(butter(4, 7000, btype="high", fs=sr, output="sos"), y)
    y = y * np.exp(-t / (0.18 if open_ else 0.022)) * np.clip(t / 0.0005, 0, 1)
    return y / np.abs(y).max()


def hat_spectrum(n: int = 1 << 15, sr: int = SR) -> tuple[np.ndarray, np.ndarray]:
    t = np.arange(n) / sr
    y = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in HAT_HZ)
    S = np.abs(np.fft.rfft(y * np.hanning(n))) / n
    return np.fft.rfftfreq(n, 1 / sr), S


def measured_pitch(y: np.ndarray, start: float = 0.05, length: float = 0.2, sr: int = SR) -> float:
    a, b = int(start * sr), int((start + length) * sr)
    seg = y[a:b] * np.hanning(b - a)
    S = np.abs(np.fft.rfft(seg, 1 << 17))
    f = np.fft.rfftfreq(1 << 17, 1 / sr)
    lo = f > 20
    return float(f[lo][np.argmax(S[lo])])


# ------------------------------------------------------------------------------------------------- patterns
PATTERNS = {   # 16 steps a bar: kick, snare (or clap), closed hat, open hat
    "rock": {"kick": [0, 8, 10], "snare": [4, 12], "hat": list(range(0, 16, 2)), "open": []},
    "funk": {"kick": [0, 3, 10], "snare": [4, 7, 12, 15], "hat": list(range(16)), "open": [], "ghost": [7, 15]},
    "disco": {"kick": [0, 4, 8, 12], "snare": [4, 12], "hat": [0, 4, 8, 12], "open": [2, 6, 10, 14]},
    "house": {"kick": [0, 4, 8, 12], "snare": [4, 12], "hat": [], "open": [2, 6, 10, 14]},
    "trap": {"kick": [0, 7, 10], "snare": [8], "hat": list(range(16)), "open": []},
}
TEMPO = {"rock": 112, "funk": 100, "disco": 120, "house": 124, "trap": 140}


def backbeat_share(p: dict) -> float:
    """The share of snare hits on beats 2 and 4 (steps 4 and 12)."""
    s = p["snare"]
    return sum(1 for x in s if x in (4, 12)) / len(s)


# ------------------------------------------------------------------------------------------------- production
def sidechain(y: np.ndarray, hits, depth_db: float = 12.0, attack: float = 0.005, release: float = 0.18, sr: int = SR) -> tuple[np.ndarray, np.ndarray]:
    """Duck ``y`` by ``depth_db`` at each hit time, recovering exponentially: a compressor keyed by the kick."""
    n = len(y)
    g_db = np.zeros(n)
    t = np.arange(n) / sr
    for h in hits:
        i = int(h * sr)
        if i >= n:
            continue
        tt = t[i:] - h
        shape = np.where(tt < attack, tt / attack, np.exp(-(tt - attack) / release))
        g_db[i:] = np.minimum(g_db[i:], -depth_db * shape)
    g = 10 ** (g_db / 20)
    return y * g, g


def chop(y: np.ndarray, n: int, order, slice_len: float | None = None, sr: int = SR) -> tuple[np.ndarray, list]:
    """Cut ``y`` into ``n`` equal slices and concatenate them in ``order`` (indices; None for a rest), each trimmed or
    padded to ``slice_len`` seconds, with 3 ms fades to avoid clicks."""
    L = len(y) // n
    out_len = int((slice_len or L / sr) * sr)
    f = int(0.003 * sr)
    pieces = []
    for k in order:
        p = np.zeros(out_len)
        if k is not None:
            s = y[k * L: k * L + min(L, out_len)].copy()
            s[:f] *= np.linspace(0, 1, f)
            s[-f:] *= np.linspace(1, 0, f)
            p[: len(s)] = s
        pieces.append(p)
    return np.concatenate(pieces), [(k * L / sr if k is not None else None) for k in order]


# ------------------------------------------------------------------------------------------------- prosody and flow
WEIGHT16 = [4, 0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0]       # metrical weight of each sixteenth in 4/4


def prosody(syllables) -> dict:
    """syllables: [(text, stressed: bool, step)] with steps in sixteenths from the bar line.  Stressed syllables should
    take the strong positions (weight >= 2: beats); the score is the share of syllables whose stress agrees with the
    position's strength."""
    agree = []
    for _, st, step in syllables:
        strong = WEIGHT16[step % 16] >= 2
        agree.append(st == strong)
    stressed = [s for s in syllables if s[1]]
    return {"agree": float(np.mean(agree)), "stressed_on_beats": float(np.mean([WEIGHT16[s[2] % 16] >= 2 for s in stressed])) if stressed else 0.0,
            "n": len(syllables)}


def flow(syllables, bars: int) -> dict:
    """syllables: [(text, accent: bool, step, rhyme or None)] in sixteenths from the first bar line.  Returns the
    density (syllables a beat), the share on the beat, the gaps between accented syllables in sixteenths (Ohriner's
    groupings: mostly twos and threes), the share of syllables that rhyme, and the steps where rhymes land."""
    steps = [s[2] for s in syllables]
    acc = [s[2] for s in syllables if s[1]]
    gaps = [b - a for a, b in zip(acc, acc[1:])]
    rhymes = [s for s in syllables if s[3]]
    groups = Counter(rhymes_class for _, _, _, rhymes_class in rhymes)
    return {"syllables": len(syllables), "per_beat": len(syllables) / (4 * bars), "on_beat": float(np.mean([x % 4 == 0 for x in steps])),
            "gaps": gaps, "gap_counts": dict(Counter(gaps)), "rhyme_share": len(rhymes) / len(syllables),
            "rhyme_steps": [s[2] % 16 for s in rhymes], "rhyme_classes": dict(groups),
            "end_of_bar_rhymes": sum(1 for s in rhymes if s[2] % 16 >= 12)}
