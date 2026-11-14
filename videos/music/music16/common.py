"""Helpers shared by the scenes of Part 16 ("Two Voices")."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.music.chordviz import note_bars, tex  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.melodyviz import columns, roll  # noqa: F401
from explainer.music.monochord import score as SC
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED, keyboard  # noqa: F401
from explainer.music.staff import GrandStaff, Staff  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 16
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
UP_C, CF_C = "#F5C542", "#7DD3FC"
DIM = "#3A4250"
MOTION_C = {"parallel": "#EF5350", "similar": "#FB923C", "contrary": "#A3E635", "oblique": "#7DD3FC"}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def curve_from(g, xs, ys, color, stroke_width=3):
    return curve(g.ax, np.asarray(xs, dtype=float), np.asarray(ys, dtype=float), color, stroke_width=stroke_width)


def duet(voices, colors=(UP_C, CF_C), width: float = 11.0, height: float = 3.0, lo: float | None = None, hi: float | None = None, total: float | None = None,
         thick: float = 0.14, gap: float = 0.06, bar: float | None = None) -> VGroup:
    """Several voices, each a list of (pitch, start beat, beats), as bars on one pair of axes: time to the right,
    pitch up.  ``.notes[j][k]`` is voice j's k-th note; ``.x(beat)``, ``.y(pitch)``.  ``bar`` draws faint barlines."""
    allp = [e[0] for v in voices for e in v]
    lo = min(allp) - 1.5 if lo is None else lo
    hi = max(allp) + 1.5 if hi is None else hi
    total = max(e[1] + e[2] for v in voices for e in v) if total is None else total
    frame = Rectangle(width=width, height=height, stroke_width=0, fill_opacity=0)
    g = VGroup(frame)

    def x(t):
        return frame.get_left()[0] + width * float(t) / total

    def y(p):
        return frame.get_bottom()[1] + height * (float(p) - lo) / (hi - lo)

    g.x, g.y, g.frame = x, y, frame
    if bar:
        g.add(*[Line([x(b), y(lo), 0], [x(b), y(hi), 0], color=DIM, stroke_width=1) for b in np.arange(bar, total, bar)])
    g.notes = []
    for j, v in enumerate(voices):
        row = []
        for p, a, d in v:
            w = max(width * d / total - gap, 0.04)
            r = RoundedRectangle(width=w, height=thick, corner_radius=min(thick, w) / 2.2, stroke_width=0, fill_color=colors[j % len(colors)], fill_opacity=1.0)
            r.move_to([x(a) + w / 2 + gap / 2, y(p), 0])
            g.add(r)
            row.append(r)
        g.notes.append(row)
    return g


def sing_voice(snd, notes, times, base, hot=WHITE, hold: float = 0.25, fade: float = 0.3):
    return flash(snd, notes, times, hot=hot, base=base, fade=fade, hold=hold)


def staff_pair(upper, lower, width: float = 11.0, space: float = 0.16, lower_clef: str = "treble"):
    """Two voices on two staves, bar for bar (a bar is four beats, a whole note)."""
    def voice(events, clef):
        out, t = [], Fraction(0)
        for p, a, d in events:
            a, d = Fraction(a).limit_denominator(8) / 4, Fraction(d).limit_denominator(8) / 4
            if a > t:
                out.append(SC.Rest(a - t))
            out.append(SC.Note(SC.Pitch.from_midi(int(p), flats=False) if int(p) % 12 != 1 else SC.Pitch.from_midi(int(p)), d))
            t = a + d
        return SC.Voice(out, clef=clef)

    sc = SC.Score([voice(upper, "treble"), voice(lower, lower_clef)], time=(4, 4))
    return GrandStaff(sc, width=width, space=space, show_time=False, gap=9.5)


NAMES = {48: "C3", 50: "D3", 52: "E3", 53: "F3", 55: "G3", 57: "A3", 59: "B3", 60: "C4", 62: "D4", 64: "E4", 65: "F4", 67: "G4", 69: "A4", 71: "B4", 72: "C5", 73: "C♯5",
         74: "D5", 76: "E5", 77: "F5", 79: "G5", 81: "A5", 83: "B5", 84: "C6"}
