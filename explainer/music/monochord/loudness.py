"""Loudness and true peak after ITU-R BS.1770-4 (the meter of EBU R 128).

The series needs a meter from its first part, to set the level of every example and to check its own masters; Part 57
derives it on screen.  ``tests/music/test_loudness.py`` checks it against ffmpeg's ``ebur128`` filter, which shares
none of this code.

    integrated(clip)      # LUFS, gated
    true_peak_db(clip)    # dBTP, by 4x oversampling
"""

from __future__ import annotations

import numpy as np
from scipy.signal import lfilter, resample_poly

from .audio import Clip

# K-weighting at 48 kHz (BS.1770-4, Annex 1): a high shelf (the head), then a high-pass (the RLB curve).
_SHELF_B = (1.53512485958697, -2.69169618940638, 1.19839281085285)
_SHELF_A = (1.0, -1.69065929318241, 0.73248077421585)
_HP_B = (1.0, -2.0, 1.0)
_HP_A = (1.0, -1.99004745483398, 0.99007225036621)

BLOCK = 0.4  # seconds
OVERLAP = 0.75
ABS_GATE = -70.0  # LUFS
REL_GATE = -10.0  # LU below the ungated level


def k_weight(y: np.ndarray, sr: int = 48_000) -> np.ndarray:
    if sr != 48_000:
        raise ValueError("the K-weighting coefficients here are for 48 kHz")
    y = lfilter(_SHELF_B, _SHELF_A, y.astype(np.float64), axis=0)
    return lfilter(_HP_B, _HP_A, y, axis=0)


def block_power(clip: Clip) -> np.ndarray:
    """Mean square of the K-weighted signal in 400 ms blocks with 75% overlap, summed over channels (L and R both
    have weight 1).  A mono clip is one channel, which equals its constant-power stereo placement."""
    z = k_weight(clip.y if clip.channels == 2 else clip.y[:, None], clip.sr) ** 2
    n = int(round(BLOCK * clip.sr))
    hop = int(round(n * (1 - OVERLAP)))
    if z.shape[0] < n:
        return np.zeros(0)
    c = np.concatenate([np.zeros((1, z.shape[1])), np.cumsum(z, axis=0)])
    starts = np.arange(0, z.shape[0] - n + 1, hop)
    return ((c[starts + n] - c[starts]) / n).sum(axis=1)


def _lufs(power) -> float:
    return -0.691 + 10 * np.log10(power) if power > 0 else -np.inf


def integrated(clip: Clip) -> float:
    """Integrated loudness in LUFS, with the absolute (-70 LUFS) and relative (-10 LU) gates.  ``-inf`` for silence
    and for clips shorter than one block."""
    p = block_power(clip)
    if p.size == 0:
        # shorter than a block: the ungated level of what there is
        z = k_weight(clip.y if clip.channels == 2 else clip.y[:, None], clip.sr) ** 2
        return _lufs(float(z.mean(axis=0).sum())) if z.size else -np.inf
    keep = p[p > 10 ** ((ABS_GATE + 0.691) / 10)]
    if keep.size == 0:
        return -np.inf
    rel = _lufs(float(keep.mean())) + REL_GATE
    keep = keep[keep > 10 ** ((rel + 0.691) / 10)]
    return _lufs(float(keep.mean())) if keep.size else -np.inf


def momentary_max(clip: Clip) -> float:
    """The loudest 400 ms block, in LUFS."""
    p = block_power(clip)
    return _lufs(float(p.max())) if p.size else integrated(clip)


def true_peak_db(clip: Clip, oversample: int = 4) -> float:
    """The peak of the signal between its samples, in dBTP (0 = full scale), by polyphase oversampling."""
    if clip.n == 0:
        return -np.inf
    up = resample_poly(clip.y.astype(np.float64), oversample, 1, axis=0)
    peak = max(float(np.abs(up).max()), clip.peak)
    return 20 * np.log10(peak) if peak > 0 else -np.inf
