"""The plucked string as sound, and the pure tone.

The sound of a string instrument is not the string's displacement: a string moves almost no air.  What reaches the
soundboard is the force the string exerts on its bridge, ``T du/dx`` at the end, and that is what :func:`plucked`
returns, computed as a sum of the string's modes (:mod:`..physics.string`).  The sum is band-limited by construction
(modes above 18 kHz are left out), so there is nothing to alias.

No soundboard is modelled yet: these are the forces a board would be driven by, played as they are.  Part 7 adds the
body.
"""

from __future__ import annotations

import numpy as np

from ..audio import SR, Clip, mix
from ..physics.string import String, pluck_modes

# The series' monochord: a metre of 0.5 mm steel wire over a box, tuned to C3 when open (a tension of about 105 N,
# the weight of eleven kilograms).  The stiffness is that wire's (E = 200 GPa).  The losses are chosen so that the
# fundamental takes about seven seconds to fall by 60 dB and a partial at 3 kHz under half a second, which is how
# a wire string on a wooden box behaves: its brightness fades long before its pitch does (Fletcher & Rossing, *The
# Physics of Musical Instruments*, sec. 2.11-2.13, 5.5).
C3 = 130.8127826502993
MONOCHORD_STRING = String.tuned(C3, L=1.0, mu=0.00154, kappa=0.63, sigma0=0.9, sigma1=3.0e-3)

F_MAX = 18_000.0


def _plectrum(n: np.ndarray, width: float, L: float) -> np.ndarray:
    """A plectrum or finger of finite width rounds the corner of the pluck: each mode is scaled by
    ``sin(z) / z`` with ``z = n pi width / 2L``."""
    z = n * np.pi * width / (2 * L)
    return np.where(z < 1e-9, 1.0, np.sin(z) / np.maximum(z, 1e-9))


def pluck_partials(string: String, beta: float, width: float = 0.004, f_max: float = F_MAX) -> dict:
    """The modes a pluck at ``beta`` excites, as heard at the bridge: ``n``, ``hz``, ``decay`` (1/s) and the force
    amplitude ``force`` (relative to the first)."""
    n_max = 1
    while string.mode_freq(n_max + 1) < f_max and n_max < 400:
        n_max += 1
    n = np.arange(1, n_max + 1, dtype=np.float64)
    a = pluck_modes(n_max, beta) * _plectrum(n, width, string.L)
    force = a * n  # T du/dx at the end: mode n contributes a_n (n pi / L) T
    ref = abs(force[0]) if abs(force[0]) > 1e-12 else np.abs(force).max()
    return {"n": n, "hz": string.mode_freq(n), "decay": string.mode_decay(n), "force": force / ref}


def plucked(f1: float | None = None, seconds: float = 3.0, beta: float = 0.18, string: String | None = None,
            width: float = 0.004, stop: float = 1.0, release: float | None = None, sr: int = SR,
            only=None) -> np.ndarray:
    """The bridge force of a plucked string, peak 1.

    ``string`` defaults to the monochord's; ``stop`` is the fraction of it left to vibrate (a movable bridge at that
    point: the same wire and tension, a shorter length), and ``f1`` instead re-tunes the tension.  ``beta`` is the
    plucking point as a fraction of the sounding length.  ``release`` (seconds) damps the string from that moment
    (a finger laid on it).  ``only`` keeps just those mode numbers."""
    s = string or MONOCHORD_STRING
    if stop != 1.0:
        s = s.with_(L=s.L * stop)
    if f1 is not None:
        s = s.with_(T=s.mu * (2 * s.L * f1) ** 2)
    p = pluck_partials(s, beta, width)
    keep = np.ones(len(p["n"]), bool) if only is None else np.isin(p["n"], np.asarray(only))
    n_samp = int(round(seconds * sr))
    t = np.arange(n_samp) / sr
    y = np.zeros(n_samp)
    w = 2 * np.pi * p["hz"]
    for i in np.flatnonzero(keep):  # one mode at a time keeps the memory flat for long notes
        y += p["force"][i] * np.exp(-p["decay"][i] * t) * np.cos(w[i] * t)
    if release is not None:
        k = int(round(release * sr))
        if k < n_samp:
            y[k:] *= np.exp(-(t[k:] - t[k]) / 0.035)
    peak = np.abs(y).max()
    return (y / peak if peak > 0 else y).astype(np.float32)


def released(shape, seconds: float = 3.0, string: String | None = None, sr: int = SR, f_max: float = F_MAX) -> np.ndarray:
    """The bridge force of a string let go from rest in any shape: ``shape`` is a function on [0, 1] (the fraction
    of the length) that vanishes at both ends.  Its sine coefficients are found numerically; the rest is as for a
    pluck.  Peak 1."""
    from ..physics.string import sine_coefficients

    s = string or MONOCHORD_STRING
    n_max = 1
    while s.mode_freq(n_max + 1) < f_max and n_max < 400:
        n_max += 1
    x = np.linspace(0.0, 1.0, 4001)
    a = sine_coefficients(np.asarray(shape(x), dtype=np.float64) * np.sin(np.pi * x) ** 0, n_max)
    n = np.arange(1, n_max + 1, dtype=np.float64)
    force = a * n
    t = np.arange(int(round(seconds * sr))) / sr
    y = np.zeros(len(t))
    w, dec = 2 * np.pi * s.mode_freq(n), s.mode_decay(n)
    for i in range(n_max):
        if abs(force[i]) > 1e-9 * np.abs(force).max():
            y += force[i] * np.exp(-dec[i] * t) * np.cos(w[i] * t)
    peak = np.abs(y).max()
    return (y / peak if peak > 0 else y).astype(np.float32)


def pure_tone(hz: float, seconds: float, decay: float = 0.0, attack: float = 0.012, sr: int = SR) -> np.ndarray:
    """A single sinusoid with a short raised-cosine attack and an exponential decay (1/s), peak 1."""
    n = int(round(seconds * sr))
    t = np.arange(n) / sr
    y = np.sin(2 * np.pi * hz * t) * np.exp(-decay * t)
    k = max(2, int(attack * sr))
    y[:k] *= 0.5 - 0.5 * np.cos(np.pi * np.arange(k) / k)
    return y.astype(np.float32)


def two_strings(ratio: float, f1: float = C3, seconds: float = 4.0, beta: float = 0.18, stagger: float = 0.0,
                level: float = -18.0) -> Clip:
    """Two monochord strings sounded together, the second ``ratio`` times the first in frequency."""
    a = Clip(plucked(f1, seconds, beta))
    b = Clip(plucked(f1 * ratio, seconds - stagger, beta))
    return mix([(a, 0.0, 0.0, -0.35), (b, stagger, 0.0, 0.35)]).fade(0.002, 0.15).at_lufs(level)
