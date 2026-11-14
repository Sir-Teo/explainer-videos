"""Helpers shared by the scenes of Part 13 ("Intervals and Chords")."""

from __future__ import annotations

import numpy as np

from explainer.music.chordviz import Tonnetz, note_bars, partial_rows, tex  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.monochord import score as SC
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED, chain, keyboard, twelve  # noqa: F401
from explainer.music.staff import GrandStaff, Staff  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 13
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
MAJOR_C, MINOR_C, DIM_C, AUG_C = "#F5C542", "#7DD3FC", "#EF5350", "#A3E635"
KIND_COLOR = {"major": MAJOR_C, "minor": MINOR_C, "diminished": DIM_C, "augmented": AUG_C, "maj7": MAJOR_C, "7": "#FB923C", "m7": MINOR_C, "m7b5": DIM_C, "dim7": DIM_C}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def curve_from(g, xs, ys, color, stroke_width=3):
    return curve(g.ax, np.asarray(xs, dtype=float), np.asarray(ys, dtype=float), color, stroke_width=stroke_width)


def keys(lo: int = 48, hi: int = 84, width: float = 10.0, height: float = 1.7, lit=()):
    """A keyboard from MIDI key ``lo`` to ``hi`` (both white).  ``kb.key[m - 60]`` is key ``m``; ``kb.on(m)`` lights it."""
    kb = keyboard(lo - 60, hi - 60, width=width, height=height)
    kb.on = lambda m, c=GOLD: kb.light(int(m) - 60, c) if int(m) - 60 in kb.key else None       # noqa: E731
    for m in lit:
        kb.on(m)
    return kb


def light_chords(snd, kb, chords, times, end: float | None = None, color=GOLD, colors=None):
    """While a clip plays, light on ``kb`` the keys of whichever chord is sounding (``chords[k]`` from ``times[k]``)."""
    times = [float(t) for t in times]
    ends = times[1:] + [times[-1] + 3.0 if end is None else float(end)]

    def fn(_, t):
        kb.clear()
        for k, (ch, a, b) in enumerate(zip(chords, times, ends)):
            if a <= t < b:
                for m in ch:
                    kb.on(m, color if colors is None else colors[k])

    snd.drive(kb.key[min(kb.key)], fn)


def light_notes(snd, notes, times, hot=GOLD, base=WHITE, hold: float = 0.6, fade: float = 0.35):
    """Light the heads of staff notes (or any marks) at their times."""
    return flash(snd, [getattr(n, "ink", n) for n in notes], times, hot=hot, base=base, fade=fade, hold=hold)


def chord_row(items, width: float = 8.0, space: float = 0.2, clef: str = "treble", above=None, below=None, font_size: int = 26, above_color=WHITE, below_color=GREY_A,
              dur=SC.W, gap_above: float = 0.4, gap_below: float = 0.45, key: int = 0, **kw) -> VGroup:
    """Notes and chords in a row on a staff (``"C4"``, or ``["C4", "E4", "G4"]``), with a line of labels above
    and one below, each centred on its chord.  ``.staff``, ``.notes``, ``.above``, ``.below``."""
    st = Staff(SC.quick(items, dur=dur, clef=clef, key=key), width=width, space=space, show_time=False, carry=False, **kw)
    g = VGroup(st)
    g.staff, g.notes = st, st.notes
    top, bot = st.get_top()[1], st.get_bottom()[1]
    g.above, g.below = VGroup(), VGroup()
    if above is not None:
        g.above = VGroup(*[label(tex(t), font_size=font_size, color=above_color).move_to([n.x, top + gap_above, 0]) for n, t in zip(st.notes, above)])
        g.add(g.above)
    if below is not None:
        g.below = VGroup(*[label(tex(t), font_size=font_size, color=below_color).move_to([n.x, bot - gap_below, 0]) for n, t in zip(st.notes, below)])
        g.add(g.below)
    return g


def colour_chord(n, color):
    """Colour the heads of a staff chord (or note)."""
    n.ink.set_color(color)
    return n
