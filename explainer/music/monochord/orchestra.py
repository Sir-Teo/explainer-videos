"""Monochord's orchestra (Part 41 of *Music, Built*): instruments resynthesised additively from spectra measured on the
series' own physical models, sections, blend, spacing, and a solver that matches a target spectrum.

    measure_profiles()        run Parts 7-8's physical models once (flute, clarinet, saxophone, trumpet soft and loud,
                              bowed string) and read the strengths of their first sixteen harmonics
    PROFILES                  those measurements, in dB (kept here so the film does not rerun the models), with a
                              celesta-like struck bar and a plucked string
    RANGES                    sounding ranges and transpositions of the orchestra's instruments (key numbers)
    note(name, m, seconds)    one note by additive synthesis: the measured harmonic strengths, an attack, vibrato
    section(name, m, n)       n players on one part: small random detunings, vibratos and onsets (the chorus effect)
    centroid(levels, f0)      the spectral centroid of a harmonic spectrum (brightness)
    fusion(parts)             the share of a combination's power that lies on one harmonic series (blend by harmonicity)
    voicing_roughness(keys)   Part 5's sensory roughness of a chord, voiced with each instrument's measured partials
    match(target, budget)     nonnegative least squares over (instrument, harmonic) candidates, then the best subset
                              of ``budget`` instruments: orchestration as search
"""

from __future__ import annotations

from itertools import combinations

import numpy as np
from scipy.optimize import nnls

from .audio import SR

H = 16                                                              # harmonics kept

# Measured once by measure_profiles() (dB re the strongest harmonic, harmonics 1..12, extended to 16 by the last slope).
_MEAS = {
    "flute": [0.0, -20.8, -11.5, -21.5, -17.5, -23.6, -24.5, -26.1, -29.3, -27.5, -35.9, -30.9],
    "clarinet": [0.0, -20.1, -1.9, -18.2, -4.3, -18.4, -7.0, -19.7, -9.9, -21.5, -13.0, -23.7],
    "saxophone": [0.0, -4.5, -11.8, -21.7, -18.0, -22.1, -31.2, -34.2, -36.6, -40.5, -35.4, -32.0],
    "trumpet p": [0.0, -18.9, -33.6, -48.5, -60.3, -65.3, -70.7, -69.0, -66.9, -68.9, -70.1, -65.6],
    "trumpet f": [0.0, -2.0, -5.9, -13.2, -13.6, -15.7, -20.8, -22.5, -25.0, -33.7, -41.2, -43.2],
    "violin": [0.0, -5.5, -10.4, -12.2, -13.4, -13.3, -13.3, -13.9, -14.1, -39.1, -18.4, -22.8],
}


def _extend(db, n=H):
    db = list(db)
    slope = (db[-1] - db[-4]) / 3.0 if len(db) >= 4 else -3.0
    while len(db) < n:
        db.append(db[-1] + min(slope, -1.0))
    return np.array(db[:n])


PROFILES = {k: _extend(v) for k, v in _MEAS.items()}
PROFILES["horn"] = np.minimum(PROFILES["trumpet p"] + 6.0, 0.0)          # the soft brass spectrum, a little fuller
PROFILES["piccolo"] = PROFILES["flute"] - 3.0 * np.arange(H)            # the flute's spectrum, thinner at the top
PROFILES["cello"] = PROFILES["violin"].copy()                           # the same bowed-string model, lower
CELESTA = [(1.0, 0.0), (2.756, -28.0), (5.404, -40.0)]                  # a struck bar: inharmonic partials (Part 9)
DECAY = {"celesta": 1.4, "harp": 1.8}


def measure_profiles(names=("flute", "clarinet", "saxophone", "trumpet p", "trumpet f", "violin")) -> dict:
    """Run the physical models (Parts 7-8) and read harmonics 1..12 in dB re the strongest (about ten seconds)."""
    from .instruments import strings as STR
    from .instruments import winds as W
    out = {}
    for name in names:
        if name == "flute":
            y, f0 = W.jet_tone(440.0, 1.0), 440.0
        elif name == "clarinet":
            y, f0 = W.reed_tone(W.clarinet(), seconds=1.0)["sound"], None
        elif name == "saxophone":
            y, f0 = W.reed_tone(W.saxophone(), seconds=1.0)["sound"], None
        elif name.startswith("trumpet"):
            y, f0 = W.lip_tone(W.trumpet(), 233.0, seconds=1.0, pressure=1.0 if name.endswith("p") else 1.6)["sound"], None
        else:
            y, f0 = STR.bowed_note(196.0, 1.0), 196.0
        y = np.asarray(y)[int(0.3 * SR): int(0.9 * SR)]
        S = np.abs(np.fft.rfft(y * np.hanning(len(y))))
        f = np.fft.rfftfreq(len(y), 1 / SR)
        if f0 is None:
            lo = f > 60
            f0 = f[lo][np.argmax(S[lo])]
        a = []
        for k in range(1, 13):
            i = int(np.argmin(np.abs(f - k * f0)))
            a.append(S[i - 3: i + 4].max())
        a = np.array(a) / max(a)
        out[name] = (20 * np.log10(a + 1e-6)).tolist()
    return out


RANGES = {   # sounding ranges (key numbers) and written-to-sounding transposition in semitones
    "piccolo": (74, 108, 12), "flute": (60, 96, 0), "oboe": (58, 91, 0), "clarinet": (50, 94, -2), "saxophone": (49, 81, -14),
    "bassoon": (34, 75, 0), "horn": (35, 77, -7), "trumpet": (52, 82, -2), "trombone": (40, 77, 0), "tuba": (26, 65, 0),
    "violin": (55, 103, 0), "viola": (48, 88, 0), "cello": (36, 81, 0), "double bass": (28, 67, -12), "celesta": (60, 108, 12),
    "harp": (23, 104, 0),
}


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def levels(name: str) -> np.ndarray:
    """Linear amplitudes of the first H harmonics."""
    return 10 ** (PROFILES[name] / 20.0)


def note(name: str, m: float, seconds: float, sr: int = SR, vibrato: float | None = None, attack: float | None = None,
         detune_cents: float = 0.0, phase_seed: int = 0) -> np.ndarray:
    """One note: harmonics of hz(m) with the instrument's measured strengths, an attack shaped by the family (winds and
    bowed strings swell in; the celesta and harp are struck and decay), and vibrato for the strings and flutes."""
    f0 = hz(m) * 2 ** (detune_cents / 1200.0)
    n = int(seconds * sr)
    t = np.arange(n) / sr
    rng = np.random.default_rng(phase_seed)
    if name in ("celesta",):
        y = sum(10 ** (db / 20) * np.sin(2 * np.pi * f0 * r * t + rng.uniform(0, 6.28)) * np.exp(-t * (DECAY["celesta"] * (1 + 3 * k)))
                for k, (r, db) in enumerate(CELESTA))
        y *= np.clip(t / 0.001, 0, 1)
        return y / np.abs(y).max()
    vib = vibrato if vibrato is not None else (5.5 if name in ("violin", "cello", "flute", "piccolo", "voice a") else 0.0)
    depth = 0.004 if vib else 0.0
    ph_mod = 2 * np.pi * np.cumsum(1.0 + depth * np.sin(2 * np.pi * vib * t + rng.uniform(0, 6.28)) * np.clip((t - 0.2) / 0.3, 0, 1)) / sr
    lv = levels(name)
    y = np.zeros(n)
    for k in range(H):
        fk = f0 * (k + 1)
        if fk > 0.45 * sr:
            break
        y += lv[k] * np.sin(fk * ph_mod + rng.uniform(0, 6.28))
    a = attack if attack is not None else {"trumpet p": 0.03, "trumpet f": 0.02, "horn": 0.05, "harp": 0.003}.get(name, 0.06)
    env = np.clip(t / a, 0, 1) * np.clip((seconds - t) / 0.08, 0, 1)
    if name == "harp":
        env = np.clip(t / 0.003, 0, 1) * np.exp(-t * DECAY["harp"])
    y *= env
    return y / max(np.abs(y).max(), 1e-12)


def section(name: str, m: float, seconds: float, players: int = 8, cents_sd: float = 6.0, onset_ms_sd: float = 15.0,
            seed: int = 0, sr: int = SR) -> np.ndarray:
    """``players`` copies of a note, each with its own small detuning, vibrato phase and onset: a section. Returned
    unnormalised (the sum), so its level can be compared with one player's."""
    rng = np.random.default_rng(seed)
    n = int(seconds * sr)
    out = np.zeros(n + int(0.1 * sr))
    for p in range(players):
        y = note(name, m, seconds, sr, detune_cents=float(rng.normal(0, cents_sd)), phase_seed=seed * 100 + p,
                 vibrato=5.0 + rng.normal(0, 0.4) if name in ("violin", "cello", "flute") else None)
        i = int(abs(rng.normal(0, onset_ms_sd / 1000.0)) * sr)
        out[i:i + n] += y
    return out[:n]


def rms_db(y: np.ndarray) -> float:
    return float(20 * np.log10(np.sqrt(np.mean(y ** 2)) + 1e-12))


def centroid(lv: np.ndarray, f0: float) -> float:
    p = np.asarray(lv) ** 2
    f = f0 * np.arange(1, len(p) + 1)
    return float((f * p).sum() / p.sum())


def partials(name: str, m: float, gain: float = 1.0) -> list[tuple[float, float]]:
    if name == "celesta":
        return [(hz(m) * r, gain * 10 ** (db / 20)) for r, db in CELESTA]
    lv = levels(name)
    return [(hz(m) * (k + 1), gain * lv[k]) for k in range(H)]


def fusion(parts, f0: float, cents: float = 15.0) -> float:
    """parts: [(instrument, key number, gain)].  The share of the combination's power that lies within ``cents`` of a
    harmonic of ``f0``: 1 means every partial belongs to one harmonic series."""
    tot, on = 0.0, 0.0
    for name, m, g in parts:
        for f, a in partials(name, m, g):
            p = a * a
            tot += p
            k = max(1, round(f / f0))
            if abs(1200 * np.log2(f / (k * f0))) <= cents:
                on += p
    return on / tot


def _pair_roughness(f1, f2, a1, a2):
    s = 0.24 / (0.0207 * min(f1, f2) + 18.96)
    d = abs(f2 - f1)
    return a1 * a2 * (np.exp(-3.5 * s * d) - np.exp(-5.75 * s * d))


def voicing_roughness(notes, name: str = "violin") -> float:
    """Part 5's sensory roughness (Plomp-Levelt, Sethares's parametrisation) of a chord whose notes all have the
    instrument's measured partials."""
    ps = []
    for m in notes:
        ps += partials(name, m)
    r = 0.0
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            r += _pair_roughness(ps[i][0], ps[j][0], ps[i][1], ps[j][1])
    return float(r)


# ------------------------------------------------------------------------------------------------- matching
ERB_EDGES = np.geomspace(80.0, 8000.0, 33)


def band_power(parts) -> np.ndarray:
    """Power in 32 log-spaced bands from 80 Hz to 8 kHz, for [(frequency, amplitude)]."""
    out = np.zeros(len(ERB_EDGES) - 1)
    for f, a in parts:
        i = np.searchsorted(ERB_EDGES, f) - 1
        if 0 <= i < len(out):
            out[i] += a * a
    return out


def vowel_target(formants=(730.0, 1090.0, 2440.0), f0: float = 130.81, bw=(80.0, 90.0, 120.0)) -> list[tuple[float, float]]:
    """A sung vowel's harmonic spectrum: a source falling 12 dB an octave shaped by three formant resonances."""
    out = []
    for k in range(1, 61):
        f = f0 * k
        if f > 8000:
            break
        src = k ** -1.0
        env = 1.0
        for F, B in zip(formants, bw):
            env *= 1.0 / np.sqrt((1 - (f / F) ** 2) ** 2 + (f * B / F ** 2) ** 2)
        out.append((f, src * env))
    m = max(a for _, a in out)
    return [(f, a / m) for f, a in out]


def match(target, f0: float, instruments=("flute", "piccolo", "clarinet", "saxophone", "trumpet f", "horn", "violin", "cello"),
          harmonics=(1, 2, 3, 4, 5, 6, 8), budget: int = 4) -> dict:
    """Candidates are (instrument, playing the k-th harmonic of f0, within its range).  Their band powers form the
    columns of A; the target's band power is b.  Nonnegative least squares picks gains; then every subset of
    ``budget`` candidates among the best is refitted, and the best subset kept.  The error is the relative distance in
    log band power (dB), the measure the ear cares about more than raw power."""
    tb = band_power(target)
    cands = []
    for name in instruments:
        base = "trumpet" if name.startswith("trumpet") else name
        lo, hi, _ = RANGES.get(base, (0, 127, 0))
        for k in harmonics:
            m = int(round(69 + 12 * np.log2(f0 * k / 440.0)))         # players play tempered notes
            if lo <= m <= hi:
                cands.append((name, float(m), k))
    A = np.array([band_power(partials(n, m)) for n, m, _ in cands]).T
    w, _ = nnls(A, tb)
    order = np.argsort(-w)[: max(budget + 4, 8)]

    def err(idx):
        sub = A[:, idx]
        ww, _ = nnls(sub, tb)
        approx = sub @ ww
        mask = tb > tb.max() * 1e-4
        e = np.sqrt(np.mean((10 * np.log10(approx[mask] + 1e-9) - 10 * np.log10(tb[mask] + 1e-9)) ** 2))
        return e, ww

    best = None
    for r in range(1, budget + 1):
        for comb in combinations([int(i) for i in order if w[i] > 0] or list(order[:budget]), r):
            e, ww = err(list(comb))
            if best is None or e < best[0] - 1e-9 or (abs(e - best[0]) < 1e-9 and len(comb) < len(best[1])):
                if r == budget or best is None or e < best[0]:
                    best = (e, comb, ww)
    by_size = {}
    for r in range(1, budget + 1):
        es = []
        for comb in combinations([int(i) for i in order if w[i] > 0] or list(order[:budget]), r):
            es.append((err(list(comb))[0], comb))
        by_size[r] = min(es)[0] if es else None
    e, comb, ww = best
    chosen = [{"instrument": cands[i][0], "key": cands[i][1], "harmonic": cands[i][2], "gain": float(g)} for i, g in zip(comb, ww)]
    return {"chosen": chosen, "error_db": float(e), "error_by_size": by_size, "candidates": len(cands), "target_bands": tb.tolist()}
