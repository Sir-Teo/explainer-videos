"""A four-part choir from Part 8's source-filter voice: each part one continuous voice (folds, then the formants of
a vowel), so that its notes join legato, with a little vibrato and a short glide between notes, as singers do.

    y = sing([(67, 0.0, 0.6), (69, 0.6, 0.6)], "soprano")    # (key number, start s, seconds)
"""

from __future__ import annotations

import numpy as np

from ..audio import SR
from .winds import VOWELS, formant_filter, glottal_pulse

# formants scaled from Peterson and Barney's men (women's and children's tracts are shorter), and how open each part's
# folds are (a lighter, breathier source higher up)
PARTS = {"soprano": {"scale": 1.17, "oq": 0.68, "breath": 0.02}, "alto": {"scale": 1.12, "oq": 0.64, "breath": 0.018},
         "tenor": {"scale": 1.03, "oq": 0.58, "breath": 0.012}, "bass": {"scale": 0.96, "oq": 0.55, "breath": 0.01}}


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def sing(notes, part: str = "soprano", vowel: str = "a", sr: int = SR, glide: float = 0.035, vibrato: float = 5.4, depth: float = 0.004,
         tail: float = 0.4, seed: int = 0) -> np.ndarray:
    """One part, its notes as (key number, start in seconds, seconds); rests where there are no notes."""
    p = PARTS[part]
    end = max(a + d for _, a, d in notes) + tail
    n = int(end * sr)
    f0 = np.zeros(n)
    amp = np.zeros(n)
    notes = sorted(notes, key=lambda x: x[1])
    for k, (m, a, d) in enumerate(notes):
        i0, i1 = int(a * sr), min(int((a + d) * sr), n)
        f0[i0:i1] = hz(m)
        joined = k > 0 and abs(notes[k - 1][1] + notes[k - 1][2] - a) < 1e-3
        att = int((0.02 if joined else 0.06) * sr)
        rel = int(0.05 * sr)
        env = np.ones(i1 - i0)
        env[:att] = np.linspace(0.75 if joined else 0.0, 1.0, min(att, len(env)))[: len(env[:att])]
        nxt = notes[k + 1] if k + 1 < len(notes) else None
        if nxt is None or abs(a + d - nxt[1]) > 1e-3:
            env[-rel:] = np.linspace(1.0, 0.0, min(rel, len(env)))[: len(env[-rel:])]
        amp[i0:i1] = env
    # fill rests with the neighbouring pitch so the source never stops abruptly, and glide between notes
    last = hz(notes[0][0])
    for i in range(n):
        if f0[i] == 0:
            f0[i] = last
        else:
            last = f0[i]
    g = max(int(glide * sr), 1)
    kernel = np.ones(g) / g
    f0 = np.convolve(np.pad(f0, (g // 2, g - g // 2 - 1), mode="edge"), kernel, mode="valid")
    t = np.arange(n) / sr
    rng = np.random.default_rng(seed)
    f0 = f0 * (1 + depth * np.sin(2 * np.pi * (vibrato + 0.3 * rng.standard_normal()) * t + rng.uniform(0, 6.3)))
    src = glottal_pulse(f0, end, sr, open_quotient=p["oq"], breath=p["breath"], seed=seed)
    formants = [f * p["scale"] for f in VOWELS[vowel]]
    y = formant_filter(src, formants + [3500.0 * p["scale"], 4500.0 * p["scale"]], None, sr)
    y = np.diff(y, prepend=y[0]) * amp[: len(y)]
    return y / max(np.abs(y).max(), 1e-12)


def chorale(voices, beat: float, sr: int = SR, vowel: str = "a", gains=(0.0, -2.0, -2.0, -1.0), seed: int = 0) -> np.ndarray:
    """Four parts, each a list of (key number, start beat, beats), sung together; ``gains`` in dB."""
    parts = ("soprano", "alto", "tenor", "bass")
    outs = []
    for j, v in enumerate(voices):
        notes = [(m, a * beat, d * beat) for m, a, d in v]
        outs.append(sing(notes, parts[j], vowel, sr, seed=seed + j) * 10 ** (gains[j] / 20))
    n = max(len(o) for o in outs)
    y = np.zeros(n)
    for o in outs:
        y[: len(o)] += o
    return y / max(np.abs(y).max(), 1e-12)
