"""A small kit for marking time (Part 11): each sound is one of Part 9's struck things, cut short.

    kick        a slack skin struck at its centre: the modes with no still diameter, which die at once
    tom         the same skin, tighter, struck off-centre
    woodblock   a short stiff bar: a free bar's partials (1 : 2.76 : 5.40), heavily damped
    clave       a smaller, harder bar
    hat         a cymbal's crowd of partials, stopped by a hand: here, a burst of filtered noise
    rim         a stick on a rim: one bright partial and its neighbour

All return mono arrays that peak at 1.  No manim.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt

from ..audio import SR
from . import percussion as P


def kick(seconds: float = 0.45, hz: float = 72.0, sr: int = SR) -> np.ndarray:
    """A bass drum: a skin's circular modes, falling a little in pitch as the blow relaxes, with the thud of the
    beater in front."""
    t = np.arange(int(seconds * sr)) / sr
    ratios, amps, dec = [1.0, 2.296, 3.600], [1.0, 0.35, 0.15], [11.0, 22.0, 34.0]
    y = np.zeros(len(t))
    for r, a, d in zip(ratios, amps, dec):
        f = hz * r * (1.0 + 0.45 * np.exp(-t / 0.035))                  # tension rises under the beater, then relaxes
        y += a * np.exp(-d * t) * np.sin(2 * np.pi * np.cumsum(f) / sr)
    rng = np.random.default_rng(1)
    click = rng.standard_normal(len(t)) * np.exp(-t / 0.004)
    y += 0.25 * sosfilt(butter(2, [900, 5000], btype="band", fs=sr, output="sos"), click)
    y *= np.clip(t / 0.001, 0.0, 1.0)
    return y / np.abs(y).max()


def tom(hz: float = 150.0, seconds: float = 0.5, sr: int = SR) -> np.ndarray:
    return P.drum(hz, seconds, at=0.5, damping=9.0, sr=sr)


def woodblock(hz: float = 950.0, seconds: float = 0.22, sr: int = SR) -> np.ndarray:
    f = [hz * r for r in P.UNIFORM_BAR]
    return P.modal(f, [1.0, 0.5, 0.28, 0.12], [30.0, 46.0, 70.0, 95.0], seconds, sr, attack=0.0008)


def clave(hz: float = 2350.0, seconds: float = 0.18, sr: int = SR) -> np.ndarray:
    return P.modal([hz, hz * 2.7565], [1.0, 0.18], [38.0, 70.0], seconds, sr, attack=0.0006)


def rim(hz: float = 1700.0, seconds: float = 0.12, sr: int = SR) -> np.ndarray:
    return P.modal([hz, hz * 1.52, hz * 2.9], [1.0, 0.6, 0.3], [55.0, 75.0, 100.0], seconds, sr, attack=0.0005)


def hat(seconds: float = 0.1, open_: bool = False, seed: int = 0, sr: int = SR) -> np.ndarray:
    """A closed hi-hat (or, with ``open_``, one left to ring): noise above six kilohertz, dying fast."""
    rng = np.random.default_rng(seed)
    n = int((0.5 if open_ else seconds) * sr)
    t = np.arange(n) / sr
    y = sosfilt(butter(4, 6000, btype="high", fs=sr, output="sos"), rng.standard_normal(n))
    y *= np.exp(-t * (9.0 if open_ else 55.0)) * np.clip(t / 0.0006, 0.0, 1.0)
    return y / np.abs(y).max()
