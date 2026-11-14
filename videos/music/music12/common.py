"""Helpers shared by the scenes of Part 12 ("Scales and Modes")."""

from __future__ import annotations

import numpy as np

from explainer.music.kit import *  # noqa: F403
from explainer.music.monochord import score as SC
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, NOTE_NAMES, chain, keyboard, octave_circle, step_bar, twelve, vector_bars  # noqa: F401
from explainer.music.staff import Staff  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 12
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
LONG = "#F5C542"      # the larger step
SHORT = "#7DD3FC"     # the smaller


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def curve_from(g, xs, ys, color, stroke_width=3):
    return curve(g.ax, np.asarray(xs, dtype=float), np.asarray(ys, dtype=float), color, stroke_width=stroke_width)


def play_keys(snd, kb, notes, times, color=GOLD, hold: float = 0.28):
    """Light the keys of ``kb`` in turn as their notes sound (a key may be struck more than once)."""
    notes, times = list(notes), [float(t) for t in times]

    def fn(_, t):
        kb.clear()
        for n, t0 in zip(notes, times):
            if t0 <= t < t0 + hold and n in kb.key:
                kb.light(n, color)

    snd.drive(kb.key[min(kb.key)], fn)


def scale_staff(semitones, names=None, width: float = 6.0, space: float = 0.2, base: str = "C4", **kw) -> Staff:
    """A scale on a staff: ``semitones`` above ``base``, spelled with the letters in order (``names`` gives them
    otherwise, as ``["C4", "Db4", ...]``)."""
    if names is None:
        b = SC.Pitch.parse(base)
        names = []
        for k, s in enumerate(semitones):
            p = b.up(k, int(s))
            names.append(p.name)
    notes = [SC.Note(SC.Pitch.parse(n), SC.Q) for n in names]
    return Staff(SC.Score([SC.Voice(notes)], time=(len(notes), 4)), width=width, space=space, show_time=False, **kw)
