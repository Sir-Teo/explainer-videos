"""Helpers shared by the scenes of Part 15 ("Key")."""

from __future__ import annotations

import numpy as np

from explainer.music.chordviz import note_bars, tex  # noqa: F401
from explainer.music.keyviz import fifths_clock, key_meter, torus_map  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.melodyviz import columns, roll  # noqa: F401
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED, keyboard  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 15
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
TONIC_C, DOM_C, PRE_C = "#F5C542", "#EF5350", "#7DD3FC"
FUNC_C = {"tonic": TONIC_C, "dominant": DOM_C, "predominant": PRE_C}
NAMES12 = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def curve_from(g, xs, ys, color, stroke_width=3):
    return curve(g.ax, np.asarray(xs, dtype=float), np.asarray(ys, dtype=float), color, stroke_width=stroke_width)


def keys(lo: int = 36, hi: int = 84, width: float = 11.0, height: float = 1.5):
    """A keyboard from MIDI key ``lo`` to ``hi`` (both white).  ``kb.on(m, colour)`` lights key ``m``."""
    kb = keyboard(lo - 60, hi - 60, width=width, height=height)
    kb.on = lambda m, c=GOLD: kb.light(int(m) - 60, c) if int(m) - 60 in kb.key else None       # noqa: E731
    return kb


def light_chords(snd, kb, chords, times, end: float | None = None, color=GOLD, colors=None, melody=None, melody_times=None, melody_color=WHITE):
    """While a clip plays, light the keys of whichever chord is sounding (and, if given, of the melody note)."""
    times = [float(t) for t in times]
    ends = times[1:] + [times[-1] + 3.0 if end is None else float(end)]
    mt = [float(t) for t in (melody_times or [])]
    me = mt[1:] + [mt[-1] + 2.0] if mt else []

    def fn(_, t):
        kb.clear()
        for k, (ch, a, b) in enumerate(zip(chords, times, ends)):
            if a <= t < b:
                for m in ch:
                    kb.on(m, color if colors is None else colors[k])
        for m, a, b in zip(melody or [], mt, me):
            if a <= t < b:
                kb.on(m, melody_color)

    snd.drive(kb.key[min(kb.key)], fn)


def chips(names, colors=None, font_size: int = 36, buff: float = 0.9) -> VGroup:
    """Roman numerals in a row."""
    return VGroup(*[label(tex(n).replace("7", "$^7$"), font_size=font_size, color=WHITE if colors is None else colors[k]) for k, n in enumerate(names)]).arrange(RIGHT, buff=buff)


def sing(snd, r, times, hot=WHITE, base=None, hold: float = 0.3, fade: float = 0.35):
    return flash(snd, r.notes, times, hot=hot, base=base or r.notes[0].get_fill_color(), fade=fade, hold=hold)
