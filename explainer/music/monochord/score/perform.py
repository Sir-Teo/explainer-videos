"""From the page to a performance (Part 10): what a player adds that no notation of the Tune records.

``deadpan`` plays exactly what is written.  ``expressive`` applies four rules taken from the study of real
performances:

    phrasing      each phrase speeds up into its middle and slows at its end (Todd 1985, 1992)
    dynamics      "the faster, the louder": level follows the tempo (Todd 1992)
    final ritard  the last phrase slows like a runner coming to a stop (Friberg and Sundberg 1999)
    touch         a repeated note is detached from the one before; the first beat of a bar is a little stronger;
                  and no two notes are placed exactly (a few milliseconds of motor noise)

Both return a list of notes ``{"t", "dur", "hz", "db", "midi", "page_t", "page_dur"}``.  No manim, no sound.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from . import Pitch, Score


def deadpan(score: Score, voice: int = 0, hz=None, gate: float = 1.0) -> list[dict]:
    out = []
    for n in score.performed(voice, hz):
        out.append({"t": n["t"], "dur": n["dur"] * gate, "hz": n["hz"], "db": 0.0, "midi": n["midi"], "page_t": n["t"], "page_dur": n["dur"]})
    return out


def ritard_tempo(x, final: float = 0.45, q: float = 3.0):
    """Friberg and Sundberg's final ritardando: tempo (as a fraction of the tempo before it) at position ``x`` in
    0..1 through the ritard, ending at ``final``.  q = 3 fitted their measurements of performances best."""
    x = np.clip(np.asarray(x, dtype=float), 0.0, 1.0)
    return (1.0 + (final ** q - 1.0) * x) ** (1.0 / q)


def tempo_curve(score: Score, phrases, depth: float = 0.12, ritard: Fraction = Fraction(1), final: float = 0.5, steps: int = 96) -> tuple[np.ndarray, np.ndarray]:
    """Tempo (1 is the written tempo) at ``steps`` points to the whole note through the piece."""
    total = score.length
    x = np.arange(int(total * steps) + 1) / steps
    tempo = np.ones(len(x))
    for a, b in phrases:
        m = (x >= float(a)) & (x <= float(b))
        u = (x[m] - float(a)) / float(b - a)
        tempo[m] = 1.0 + depth * (1.0 - (2.0 * u - 1.0) ** 2) - depth * 0.55          # an arch: slow, fast, slow
    start = float(total - ritard)
    m = x >= start
    tempo[m] *= ritard_tempo((x[m] - start) / float(ritard), final)
    return x, tempo


def expressive(score: Score, voice: int = 0, phrases=None, depth: float = 0.12, final: float = 0.5, ritard: Fraction = Fraction(1), loud: float = 28.0,
               accent: float = 1.2, detach: float = 0.72, legato: float = 0.97, jitter: float = 0.008, seed: int = 4, hz=None) -> list[dict]:
    """The page, played by the rules above.  ``phrases`` is a list of (start, end) in whole notes; by default every
    two bars.  ``loud`` is the decibels of level per unit of tempo; ``jitter`` the motor noise in seconds."""
    rng = np.random.default_rng(seed)
    if phrases is None:
        two = 2 * score.bar
        phrases = [(k * two, (k + 1) * two) for k in range(int(score.length / two))]
    x, tempo = tempo_curve(score, phrases, depth, ritard, final)
    # time: integrate the written beat over the tempo
    clock = np.concatenate([[0.0], np.cumsum(np.diff(x) / (0.5 * (tempo[1:] + tempo[:-1])))]) * score.seconds(1)
    at = lambda w: float(np.interp(float(w), x, clock))                      # noqa: E731
    out, prev = [], None
    t = Fraction(0)
    for e in score.voices[voice].events:
        if not e.is_rest:
            t0, t1 = at(t), at(t + e.dur)
            repeated_next = False
            idx = score.voices[voice].events.index(e)
            later = [f for f in score.voices[voice].events[idx + 1: idx + 2] if not f.is_rest]
            repeated_next = bool(later) and later[0].pitch == e.pitch
            level = loud * (float(np.interp(float(t), x, tempo)) - 1.0)
            if t % score.bar == 0:
                level += accent
            if prev is not None and prev == e.pitch:
                level -= 0.8                                                 # the second of a pair is an echo
            start = t0 + (rng.normal(0.0, jitter) if t > 0 else 0.0)
            out.append({"t": start, "dur": (t1 - t0) * (detach if repeated_next else legato), "hz": (hz or Pitch.hz)(e.pitch), "db": level, "midi": e.pitch.midi,
                        "page_t": score.seconds(t), "page_dur": score.seconds(e.dur)})
            prev = e.pitch
        t += e.dur
    mean = float(np.mean([n["db"] for n in out]))
    for n in out:
        n["db"] -= mean
    return out


def deviations(notes) -> dict:
    """How far a performance is from its page: milliseconds early or late against a steady beat fitted to it, the
    spread of its levels, and its length against the page's."""
    page = np.array([n["page_t"] for n in notes])
    real = np.array([n["t"] for n in notes])
    slope, shift = np.polyfit(page, real, 1)
    ms = 1000.0 * (real - (slope * page + shift))
    db = np.array([n["db"] for n in notes])
    return {"ms": ms.tolist(), "largest_ms": float(np.abs(ms).max()), "rms_ms": float(np.sqrt(np.mean(ms ** 2))), "db_range": float(db.max() - db.min()),
            "stretch": float((real[-1] + notes[-1]["dur"]) / (page[-1] + notes[-1]["page_dur"]))}
