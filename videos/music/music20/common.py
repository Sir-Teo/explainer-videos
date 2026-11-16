"""Helpers shared by the scenes of Part 20 ("Canon and Fugue")."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.music.chordviz import tex  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.melodyviz import columns, roll  # noqa: F401
from explainer.music.monochord import score as SC
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED, keyboard  # noqa: F401
from explainer.music.staff import GrandStaff, Staff  # noqa: F401

from .compute import BEAT, CACHE, CLIPS, load  # noqa: F401

PART = 20
clip = clip_loader(CACHE, CLIPS, item_aliases={"fugue": "exposition"})
WEAK = "#8A93A0"
DIM = "#3A4250"
VOICE_C = ("#F5C542", "#F472B6", "#7DD3FC", "#A3E635")             # first, second, third, fourth voice


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def voices_roll(lines, width: float = 11.0, height: float = 3.0, lo: float | None = None, hi: float | None = None, total: float | None = None,
                colors=VOICE_C, thick: float = 0.13, gap: float = 0.05, grid: float | None = 1.0) -> VGroup:
    """Lines of [midi, onset, duration] (beats) as bars, a colour to each voice, on one time axis; ``.notes[j][k]`` is
    voice j's k-th note, ``.x(t)``/``.y(p)`` map beats and pitches; faint lines mark every ``grid`` beats."""
    allp = [n[0] for ln in lines for n in ln]
    lo = min(allp) - 1.5 if lo is None else lo
    hi = max(allp) + 1.5 if hi is None else hi
    total = max(n[1] + n[2] for ln in lines for n in ln) if total is None else total
    frame = Rectangle(width=width, height=height, stroke_width=0, fill_opacity=0)
    g = VGroup(frame)
    g.frame, g.total = frame, total

    def x(t):
        return frame.get_left()[0] + width * float(t) / total

    def y(p):
        return frame.get_bottom()[1] + height * (float(p) - lo) / (hi - lo)

    g.x, g.y = x, y
    if grid:
        g.grid = VGroup(*[Line([x(t), y(lo), 0], [x(t), y(hi), 0], color=DIM, stroke_width=1.0, stroke_opacity=0.6)
                          for t in np.arange(0, total + 1e-9, grid * 2)])
        g.add(g.grid)
    g.notes = []
    for j, ln in enumerate(lines):
        col = colors[j % len(colors)]
        bars = []
        for p, a, d in ln:
            w = max(width * d / total - gap, 0.04)
            b = RoundedRectangle(width=w, height=thick, corner_radius=min(thick, w) / 2.2, stroke_width=0, fill_color=col, fill_opacity=1.0)
            b.move_to([x(a) + w / 2 + gap / 2, y(p), 0])
            g.add(b)
            bars.append(b)
        g.notes.append(bars)
    return g


def sing_voices(snd, g, lines, start: float = 0.0, beat: float = BEAT, hot=WHITE, colors=VOICE_C, fade: float = 0.3):
    """Light every note of every voice as it sounds (``start`` seconds into the clip; ``beat`` seconds a beat)."""
    for j, ln in enumerate(lines):
        if not ln:
            continue
        flash(snd, g.notes[j], [start + n[1] * beat for n in ln], hot=hot, base=colors[j % len(colors)], fade=fade, hold=0.15)


def cursor(snd, g, start: float, beat: float = BEAT, color=GREY_B):
    """A thin vertical line that moves along the roll with the sound."""
    ln = Line([g.x(0), g.frame.get_bottom()[1] - 0.1, 0], [g.x(0), g.frame.get_top()[1] + 0.1, 0], color=color, stroke_width=2, stroke_opacity=0.7)

    def upd(m, t):
        tb = min(max((t - start) / beat, 0.0), g.total)
        m.move_to([g.x(tb), m.get_center()[1], 0])

    snd.drive(ln, upd)
    return ln


def two_staff(upper, lower, width: float = 6.0, space: float = 0.15, key: int = 0, total: float | None = None) -> GrandStaff:
    """Two lines of [midi, onset, duration] (beats) on a grand staff, rests where a voice is silent."""
    total = total or max(max(n[1] + n[2] for n in ln) for ln in (upper, lower) if ln)

    def voice(ln, clef):
        ev, t = [], 0.0
        for p, a, d in ln:
            if a > t + 1e-9:
                ev.append(SC.Rest(Fraction(a - t).limit_denominator(16) / 4))
            ev.append(SC.Note(SC.Pitch.from_midi(int(p), flats=key < 0), Fraction(d).limit_denominator(16) / 4))
            t = a + d
        if t < total - 1e-9:
            ev.append(SC.Rest(Fraction(total - t).limit_denominator(16) / 4))
        return SC.Voice(ev, clef=clef)

    sc = SC.Score([voice(upper, "treble"), voice(lower, "treble" if min(n[0] for n in lower) >= 57 else "bass")], time=(int(round(total)), 4), key=key)
    return GrandStaff(sc, width=width, space=space, show_time=False, gap=9.5)


def one_staff(ln, width: float = 6.0, space: float = 0.16, key: int = 0, clef: str = "treble") -> Staff:
    total = max(n[1] + n[2] for n in ln)
    ev, t = [], 0.0
    for p, a, d in ln:
        if a > t + 1e-9:
            ev.append(SC.Rest(Fraction(a - t).limit_denominator(16) / 4))
        ev.append(SC.Note(SC.Pitch.from_midi(int(p), flats=key < 0), Fraction(d).limit_denominator(16) / 4))
        t = a + d
    sc = SC.Score([SC.Voice(ev, clef=clef)], time=(int(round(total)), 4), key=key)
    return Staff(sc, 0, width=width, space=space, show_time=False)
