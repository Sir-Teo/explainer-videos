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

# The series' monochord: a metre-long steel string over a box, tuned to C3 when open.  The losses are chosen so the
# fundamental rings for several seconds and a 3 kHz partial for about a third of one (typical of a wire string on a
# wooden instrument: Fletcher & Rossing, *The Physics of Musical Instruments*, sec. 2.11-2.13); the stiffness is that
# of a 0.5 mm steel wire.
C3 = 130.8127826502993
MONOCHORD_STRING = String.tuned(C3, L=1.0, mu=0.00154, kappa=0.63, sigma0=0.55, sigma1=4.0e-4)

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


# ---------------------------------------------------------------------------
# The anvil of the legend (illustrative)
# ---------------------------------------------------------------------------
# A struck steel block rings at frequencies set by the block, whatever hits it.  The partial ratios below are those
# of a free bar (1 : 2.76 : 5.40 : 8.93), a stand-in for the low modes of an anvil's horn and body; only the claim
# "the same block gives the same pitches under every hammer" is physics, the particular numbers are not a measurement.
_ANVIL = ((1.0, 1.0, 5.0), (2.756, 0.7, 7.0), (5.404, 0.55, 10.0), (8.933, 0.4, 14.0), (13.34, 0.25, 20.0))


def anvil(hammer_mass: float = 1.0, base_hz: float = 880.0, seconds: float = 1.6, sr: int = SR) -> np.ndarray:
    """An illustrative anvil struck by a hammer of the given relative mass.  A heavier hammer stays in contact longer
    (Hertz: contact time grows as mass^(2/5)), so it excites the high modes less and hits harder; the pitches do not
    move."""
    n = int(round(seconds * sr))
    t = np.arange(n) / sr
    contact = 0.00025 * hammer_mass ** 0.4          # seconds
    y = np.zeros(n)
    for ratio, amp, decay in _ANVIL:
        f = base_hz * ratio
        # a half-sine force pulse of this duration has this much spectrum at f (first lobe)
        z = f * contact
        drive = abs(np.cos(np.pi * z) / (1 - 4 * z * z)) if abs(1 - 4 * z * z) > 1e-6 else np.pi / 4
        y += amp * drive * np.exp(-decay * t) * np.sin(2 * np.pi * f * t)
    y *= hammer_mass ** 0.6                         # a heavier hammer delivers more impulse
    k = max(2, int(contact * sr))
    y[:k] *= 0.5 - 0.5 * np.cos(np.pi * np.arange(k) / k)
    return y.astype(np.float32)
