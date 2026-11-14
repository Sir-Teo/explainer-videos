"""Helpers shared by the scenes of Part 17 ("Four Voices")."""

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

PART = 17
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
DIM = "#3A4250"
VOICE_C = ("#F5C542", "#F472B6", "#A3E635", "#7DD3FC")             # soprano, alto, tenor, bass
VOICE_NAMES = ("soprano", "alto", "tenor", "bass")
TICKS = 24


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def choir_roll(voices, width: float = 11.0, height: float = 3.2, lo: float | None = None, hi: float | None = None, total: float | None = None,
               thick: float = 0.11, gap: float = 0.04, colors=VOICE_C, bars: list | None = None, which=(0, 1, 2, 3)) -> VGroup:
    """Four voices (rows of (key, onset tick, duration ticks, fermata)) as bars: time to the right, pitch up.
    ``.notes[j][k]`` is voice j's k-th note; ``.x(tick)``, ``.y(key)``; fermata notes carry a small arc above."""
    vs = [[tuple(n) for n in voices[j]] for j in which]
    base = min(o for v in vs for _, o, _, _ in v)
    allp = [n[0] for v in vs for n in v]
    lo = min(allp) - 1.5 if lo is None else lo
    hi = max(allp) + 1.5 if hi is None else hi
    total = max(o + d for v in vs for _, o, d, _ in v) - base if total is None else total
    frame = Rectangle(width=width, height=height, stroke_width=0, fill_opacity=0)
    g = VGroup(frame)

    def x(t):
        return frame.get_left()[0] + width * float(t - base) / total

    def y(p):
        return frame.get_bottom()[1] + height * (float(p) - lo) / (hi - lo)

    g.x, g.y, g.frame, g.base, g.which = x, y, frame, base, tuple(which)
    if bars:
        g.add(*[Line([x(b), y(lo), 0], [x(b), y(hi), 0], color=DIM, stroke_width=1) for b in bars if base < b < base + total])
    g.notes = []
    marks = VGroup()
    for j, v in zip(which, vs):
        row = []
        for p, o, d, f in v:
            w = max(width * d / total - gap, 0.03)
            r = RoundedRectangle(width=w, height=thick, corner_radius=min(thick, w) / 2.2, stroke_width=0, fill_color=colors[j], fill_opacity=1.0)
            r.move_to([x(o) + w / 2 + gap / 2, y(p), 0])
            g.add(r)
            row.append(r)
            if f and j == which[0]:
                marks.add(Arc(radius=0.09, start_angle=0, angle=PI, color=GREY_B, stroke_width=2).next_to(r, UP, buff=0.06))
        g.notes.append(row)
    g.add(marks)
    return g


def sing_roll(snd, g, times, start: float = 0.0, hot=WHITE, hold: float = 0.2, fade: float = 0.3):
    """Light each voice's notes as they sound; ``times`` are the clip's start times per voice, ``start`` the clip's
    offset in the sound."""
    for j, nts in enumerate(g.notes):
        flash(snd, nts, [start + t for t in times[j]], hot=hot, base=VOICE_C[g.which[j]], fade=fade, hold=hold)


def block_staff(chords, width: float = 6.0, space: float = 0.15, key: int = 0, beats: int = 2) -> GrandStaff:
    """Chords (S, A, T, B) on a grand staff: soprano and alto on the treble staff, tenor and bass on the bass staff,
    each chord ``beats`` quarter notes long."""
    def pitch(m):
        return SC.Pitch.from_midi(int(m), flats=key < 0)

    d = Fraction(beats, 4)
    up = SC.Voice([SC.Chord(tuple({pitch(c[0]), pitch(c[1])}), d) if c[0] != c[1] else SC.Note(pitch(c[0]), d) for c in chords], clef="treble")
    down = SC.Voice([SC.Chord(tuple({pitch(c[2]), pitch(c[3])}), d) if c[2] != c[3] else SC.Note(pitch(c[2]), d) for c in chords], clef="bass")
    sc = SC.Score([up, down], time=(len(chords) * beats, 4), key=key)
    return GrandStaff(sc, width=width, space=space, show_time=False, gap=9.5)


def name(m: int, flats: bool = False) -> str:
    sharp = ("C", r"C$\sharp$", "D", r"D$\sharp$", "E", "F", r"F$\sharp$", "G", r"G$\sharp$", "A", r"A$\sharp$", "B")
    flat = ("C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"G$\flat$", "G", r"A$\flat$", "A", r"B$\flat$", "B")
    return (flat if flats else sharp)[int(m) % 12] + str(int(m) // 12 - 1)
