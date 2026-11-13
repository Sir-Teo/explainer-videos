"""What every part's ``compute.py`` needs: a store for its clips, a way to level and label them, and the Tune as a
sequence of notes to be played by whatever the part has built.  No manim here."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from . import tune
from .audio import EXAMPLE_LEVEL, SR, Clip, ClipStore, mix
from .instruments.plucked import C3, plucked
from .loudness import momentary_max, true_peak_db


def saver(clips: ClipStore, level: float = EXAMPLE_LEVEL, kind: str = "physical model"):
    """``save(name, clip, kind=..., level=..., **more)``: level a clip (loudest 400 ms), label it, store it, and
    return what a part's JSON keeps about it."""

    def save(name: str, clip: Clip, kind: str = kind, level: float | None = level, ceiling: float = -2.5,
             **more) -> dict:
        c = clip if level is None else clip.at_level(level)
        over = true_peak_db(c) - ceiling
        if over > 0:                     # a short, sharp sound: its peaks set its level, not its loudness
            c = c.gain(-over)
        c = c.label(kind, **more)
        clips.save(name, c)
        return {"name": name, "seconds": c.duration, "level": momentary_max(c), "true_peak_db": true_peak_db(c),
                "events": c.events}

    return save


def string_note(stop: float = 1.0, seconds: float = 2.0, beta: float = 0.11, release: float | None = None, **kw) -> Clip:
    """One pluck of Part 1's monochord with its bridge at ``stop`` (the series' reference sound)."""
    return Clip(plucked(seconds=seconds, stop=stop, beta=beta, release=release, **kw)).fade(0.002, 0.04)


def play_tune(voice, beat: float = 0.55, phrases=None, tail: float = 1.5, tonic: float = C3, ratios=None,
              accent: float = -1.5, pan=None) -> Clip:
    """The Tune, each note made by ``voice(hz, seconds, note) -> Clip`` (``note`` is the event: degree, name, ratio,
    phrase, index).  ``ratios`` maps a degree to its ratio above the tonic (the just scale of Part 1 by default).
    The clip carries events ``n0, n1, ...`` and ``phrase0, ...`` and a list of notes for the picture."""
    ev = tune.events(beat, phrases)
    placed, notes, events = [], [], {}
    for k, e in enumerate(ev):
        ratio = Fraction(e["ratio"]) if ratios is None else ratios[e["degree"]]
        hz = tonic * float(ratio)
        last = k == len(ev) - 1
        c = voice(hz, e["dur"] + (tail if last else 0.0), {**e, "index": k, "last": last})
        row = (c, e["t"], 0.0 if k % 2 == 0 else accent)
        placed.append(row if pan is None else (*row, pan(e)))
        events[f"n{k}"] = e["t"]
        notes.append({"t": e["t"], "dur": e["dur"], "hz": hz, "name": e["name"], "degree": e["degree"],
                      "ratio": [Fraction(ratio).limit_denominator(1000).numerator,
                                Fraction(ratio).limit_denominator(1000).denominator],
                      "phrase": e["phrase"]})
    end = ev[-1]["t"] + ev[-1]["dur"]
    c = mix(placed, duration=max(end, max(row[1] + row[0].duration for row in placed)))   # never shorter than the bar
    events.update({f"phrase{p}": min(n["t"] for n in notes if n["phrase"] == p) for p in {n["phrase"] for n in notes}})
    events["end"] = ev[-1]["t"] + ev[-1]["dur"]
    return Clip(c.y, SR, events, notes)


def envelope(clip: Clip, rate: int = 100, window: float = 0.03) -> np.ndarray:
    """The loudness of a clip over time, ``rate`` values a second, scaled so that its largest value is 1: what a
    picture follows while the clip plays."""
    y = np.asarray(clip.mono, dtype=np.float64)
    w = max(1, int(window * clip.sr))
    e = np.sqrt(np.convolve(y * y, np.ones(w) / w, mode="same"))[:: clip.sr // rate]
    return e / max(float(e.max()), 1e-12)


def resample(y: np.ndarray, sr_in: float, sr_out: int = SR) -> np.ndarray:
    """A signal at another sample rate (polyphase, band-limited)."""
    from scipy.signal import resample_poly

    g = np.gcd(int(round(sr_in)), int(sr_out))
    return resample_poly(np.asarray(y, dtype=np.float64), int(sr_out) // g, int(round(sr_in)) // g)
