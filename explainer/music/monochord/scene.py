"""Monochord's auditory scene (Part 45 of *Music, Built*): how one pressure wave becomes separate voices.

    erb_rate(f)                    Glasberg and Moore's ERB-number scale (Cams): the ear's frequency axis
    scale_illusion()               Deutsch's (1975) scale illusion: the notes each ear receives, and the two melodies
                                   pitch proximity predicts listeners hear
    link(dt, dcam, tau, width)     a model of sequential grouping: the strength with which one tone 'captures' the next,
                                   falling exponentially with time and with distance on the ERB scale
    streams(delta_st, trt, ...)    the competition model of ABA streaming: B joins A's stream if the A-B link beats the
                                   A-A link; the boundary in semitones against tone repetition time
    fit_boundary(points)           the model's two constants fitted to points on a published boundary
    interleave(a, b)               two melodies note by note in one line (Dowling's interleaved melodies)
    harmonic_complex(f0, ...)      a harmonic tone with one harmonic mistuned or started early
    pop_out(mistune)               the share of the mistuned harmonic's power outside the harmonic template
    continuity(gap, filler)        a glide with a gap left silent or filled with noise (Warren's continuity illusion)
    shepard(steps, ...)            Shepard tones: octave-spaced partials under a fixed bell-shaped envelope
    features(y, f0)                attack time, spectral centroid, odd/even ratio, spectral irregularity, decay
    timbre_space(features)         classical multidimensional scaling of standardised features

No manim here.  Checked in ``tests/music/test_scene.py``.
"""

from __future__ import annotations

import numpy as np

from .audio import SR


def erb_rate(f):
    """ERB-number (Cams) of frequency f in Hz (Glasberg and Moore 1990)."""
    return 21.4 * np.log10(1 + 0.00437 * np.asarray(f, float))


def hz(m):
    return 440.0 * 2 ** ((np.asarray(m, float) - 69) / 12.0)


# --------------------------------------------------------------------------------------------- the scale illusion
def scale_illusion(low: int = 60):
    """The ascending C major scale and the descending one played at once, successive tones switching ears (Deutsch
    1975).  Returns what each ear receives and the 'heard' melodies: the higher tone of each pair in one stream, the
    lower in the other (pitch proximity wins over ear of entry)."""
    up = [low + s for s in (0, 2, 4, 5, 7, 9, 11, 12)]
    down = up[::-1]
    right = [u if i % 2 == 0 else d for i, (u, d) in enumerate(zip(up, down))]
    left = [d if i % 2 == 0 else u for i, (u, d) in enumerate(zip(up, down))]
    high = [max(a, b) for a, b in zip(right, left)]
    lowm = [min(a, b) for a, b in zip(right, left)]
    return {"right": right, "left": left, "heard_high": high, "heard_low": lowm, "up": up, "down": down}


def leaps(seq) -> float:
    s = np.asarray(seq, float)
    return float(np.mean(np.abs(np.diff(s))))


# --------------------------------------------------------------------------------------------- streaming
def link(dt: float, dcam: float, tau: float = 0.25, width: float = 1.0) -> float:
    """How strongly a tone captures the next: exp(-dt / tau) * exp(-|dcam| / width)."""
    return float(np.exp(-dt / tau) * np.exp(-abs(dcam) / width))


def streams(delta_st: float, trt: float, f_a: float = 1000.0, tau: float = 0.25, width: float = 1.0) -> bool:
    """ABA- triplets with tone repetition time ``trt`` (onset to onset, s) and B ``delta_st`` semitones above A.  A's
    next A is 2 trt away at the same pitch; B is trt away at another pitch.  Two streams form if the A-A link beats
    the A-B link."""
    dcam = float(erb_rate(f_a * 2 ** (delta_st / 12.0)) - erb_rate(f_a))
    return link(2 * trt, 0.0, tau, width) > link(trt, dcam, tau, width)


def boundary(trt, f_a: float = 1000.0, tau: float = 0.25, width: float = 1.0) -> np.ndarray:
    """The model's boundary in semitones: two streams above it.  From exp(-2T/tau) = exp(-T/tau) exp(-d/w):
    d = w T / tau Cams, a straight line in T, converted to semitones at A's frequency."""
    trt = np.asarray(trt, float)
    dcam = width * trt / tau
    e = erb_rate(f_a) + dcam
    f_b = (10 ** (e / 21.4) - 1) / 0.00437
    return 12 * np.log2(f_b / f_a)


def fit_boundary(points, f_a: float = 1000.0) -> dict:
    """Fit k = width / tau (Cams a second, the only combination that matters) to (trt, semitones) points by least
    squares, with tau = 1."""
    pts = np.asarray(points, float)
    best = None
    for k in np.linspace(1.0, 60.0, 5901):
        pred = boundary(pts[:, 0], f_a, tau=1.0, width=k)
        err = float(np.sqrt(np.mean((pred - pts[:, 1]) ** 2)))
        if best is None or err < best[1]:
            best = (k, err)
    return {"k": float(best[0]), "rms_st": best[1]}


# Approximate points read from the temporal coherence boundary in van Noorden (1975) as reproduced in Bregman (1990):
# (tone repetition time in seconds, interval in semitones above which two streams are always heard).  Read from a
# figure; good to about a semitone.
VAN_NOORDEN_TCB = [(0.06, 4.0), (0.08, 5.5), (0.10, 7.0), (0.12, 8.5), (0.15, 11.0)]
VAN_NOORDEN_FB = 1.5       # the fission boundary: below about this many semitones, one stream is always heard


def aba(delta_st: float, trt: float, cycles: int = 8, f_a: float = 500.0, dur: float = 0.05, sr: int = SR) -> np.ndarray:
    """ABA- triplets: A, B, A, silence, repeated."""
    n = int((4 * trt * cycles + 0.2) * sr)
    out = np.zeros(n)
    t = np.arange(int(dur * sr)) / sr
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.5
    tone = {k: env * np.sin(2 * np.pi * f * t) for k, f in (("A", f_a), ("B", f_a * 2 ** (delta_st / 12.0)))}
    for c in range(cycles):
        for j, k in enumerate("ABA"):
            i0 = int((4 * c + j) * trt * sr)
            out[i0:i0 + len(t)] += tone[k]
    return out / np.abs(out).max()


# --------------------------------------------------------------------------------------------- interleaving
def interleave(a, b):
    """Two melodies (lists of key numbers, equal length) alternated note by note."""
    out = []
    for x, y in zip(a, b):
        out += [x, y]
    return out


def crossings(a, b) -> int:
    """How many times two interleaved melodies cross in pitch: the more crossings, the harder to hear them apart."""
    d = np.sign(np.asarray(a, float) - np.asarray(b, float))
    d = d[d != 0]
    return int(np.sum(d[1:] != d[:-1]))


# --------------------------------------------------------------------------------------------- simultaneous grouping
def harmonic_complex(f0: float = 200.0, n: int = 10, seconds: float = 1.2, mistune: float = 0.0, which: int = 4,
                     lead: float = 0.0, sr: int = SR) -> np.ndarray:
    """Harmonics 1..n of f0 with equal amplitude; harmonic ``which`` mistuned by ``mistune`` (a fraction, 0.03 = 3%)
    or started ``lead`` seconds early."""
    total = seconds + lead
    t = np.arange(int(total * sr)) / sr
    y = np.zeros_like(t)
    for k in range(1, n + 1):
        f = k * f0 * (1 + (mistune if k == which else 0.0))
        start = 0.0 if k == which else lead
        env = np.clip((t - start) / 0.02, 0, 1) * np.clip((total - t) / 0.05, 0, 1)
        y += env * np.sin(2 * np.pi * f * t)
    return y / np.abs(y).max()


def pop_out(mistune: float, which: int = 4, cents_window: float = 20.0) -> float:
    """How far the mistuned harmonic lies from the template's nearest harmonic, in cents, beyond the window within
    which the ear still counts it as part of the series (a crude stand-in for the ~1-3% threshold measured by Moore,
    Glasberg and Peters 1986)."""
    c = abs(1200 * np.log2(1 + mistune))
    return float(max(0.0, c - cents_window))


# --------------------------------------------------------------------------------------------- continuity
def continuity(gap: float = 0.15, filler: str = "silence", seconds: float = 1.6, f_lo: float = 500.0, f_hi: float = 1500.0,
               sr: int = SR, seed: int = 0) -> np.ndarray:
    """A rising glide with a gap in the middle, left silent or filled with louder broadband noise."""
    t = np.arange(int(seconds * sr)) / sr
    f = f_lo * (f_hi / f_lo) ** (t / seconds)
    y = 0.5 * np.sin(2 * np.pi * np.cumsum(f) / sr)
    g0, g1 = seconds / 2 - gap / 2, seconds / 2 + gap / 2
    mask = (t >= g0) & (t < g1)
    y[mask] = 0.0
    if filler == "noise":
        rng = np.random.default_rng(seed)
        y[mask] = 0.9 * rng.uniform(-1, 1, mask.sum())
    ramp = np.clip(t / 0.02, 0, 1) * np.clip((seconds - t) / 0.02, 0, 1)
    return y * ramp


# --------------------------------------------------------------------------------------------- pitch
def shepard(steps: int = 25, step_st: float = 1.0, tone: float = 0.35, gap: float = 0.05, base: float = 20.0,
            octaves: int = 9, centre: float = 6.0, sigma: float = 1.6, sr: int = SR) -> np.ndarray:
    """Shepard tones: every partial an octave apart, their loudness set by a bell over log frequency that never
    moves, so each step up sounds higher but the sequence never leaves its range."""
    out = []
    t = np.arange(int(tone * sr)) / sr
    env = np.clip(t / 0.02, 0, 1) * np.clip((tone - t) / 0.03, 0, 1)
    for s in range(steps):
        pc = (s * step_st / 12.0) % 1.0
        y = np.zeros_like(t)
        for o in range(octaves):
            x = o + pc
            amp = np.exp(-((x - centre) ** 2) / (2 * sigma ** 2))
            y += amp * np.sin(2 * np.pi * base * 2 ** x * t)
        out += [y * env, np.zeros(int(gap * sr))]
    y = np.concatenate(out)
    return y / np.abs(y).max()


# --------------------------------------------------------------------------------------------- timbre
def features(y, f0: float, sr: int = SR) -> dict:
    """Attack time (10% to 90% of the envelope's peak), spectral centroid (Hz) and its ratio to f0, odd-to-even
    harmonic power ratio (dB), spectral irregularity (mean |difference| of neighbouring harmonic levels, dB), and
    the decay (dB a second after the peak)."""
    y = np.asarray(y, float)
    if y.ndim == 2:
        y = y.mean(axis=1)
    env = np.abs(y)
    k = int(0.005 * sr)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    pk = int(np.argmax(env))
    a10 = int(np.argmax(env >= 0.1 * env[pk]))
    a90 = int(np.argmax(env >= 0.9 * env[pk]))
    attack = max(a90 - a10, 1) / sr
    seg = y[pk: pk + int(0.4 * sr)] if len(y) - pk > int(0.4 * sr) else y[-int(0.4 * sr):]
    S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
    f = np.fft.rfftfreq(len(seg), 1 / sr)
    cent = float((f * S).sum() / S.sum())
    lv = []
    for h in range(1, 13):
        i = int(np.argmin(np.abs(f - h * f0)))
        lv.append(S[max(i - 3, 0): i + 4].max())
    lv = np.array(lv) + 1e-12
    db = np.maximum(10 * np.log10(lv / lv.max()), -60.0)            # a floor: below -60 dB counts as absent
    odd = lv[0::2].sum()
    even = lv[1::2].sum()
    last = len(env) - 1 - int(0.15 * sr)                           # stay clear of the note's release
    i1 = max(min(pk + int(0.4 * sr), last), pk + 1)
    decay = float(20 * np.log10((env[i1] + 1e-9) / (env[pk] + 1e-9)) / max((i1 - pk) / sr, 1e-3))
    oe = float(np.clip(10 * np.log10(odd / even), -40.0, 40.0))
    return {"attack_ms": 1000 * attack, "centroid": cent, "brightness": cent / f0, "odd_even_db": oe,
            "irregularity_db": float(np.mean(np.abs(np.diff(db)))), "decay_db_s": decay}


FEATURE_KEYS = ("attack_ms", "brightness", "odd_even_db", "irregularity_db", "decay_db_s")


def timbre_space(feats: dict, keys=FEATURE_KEYS, log_attack: bool = True) -> dict:
    """Classical multidimensional scaling on standardised features: coordinates in two dimensions, the
    share of variance each dimension carries, and each feature's correlation with each dimension."""
    names = list(feats)
    X = np.array([[np.log10(feats[n][k]) if (k == "attack_ms" and log_attack) else feats[n][k] for k in keys] for n in names], float)
    Z = (X - X.mean(0)) / (X.std(0) + 1e-12)
    D2 = ((Z[:, None, :] - Z[None, :, :]) ** 2).sum(-1)
    n = len(names)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ D2 @ J
    w, V = np.linalg.eigh(B)
    order = np.argsort(w)[::-1]
    w, V = w[order], V[:, order]
    coords = V[:, :2] * np.sqrt(np.maximum(w[:2], 0))
    share = (np.maximum(w, 0) / np.maximum(w, 0).sum())[:2]
    corr = {k: [float(np.corrcoef(Z[:, j], coords[:, d])[0, 1]) for d in range(2)] for j, k in enumerate(keys)}
    return {"names": names, "coords": coords.tolist(), "share": share.tolist(), "corr": corr}
