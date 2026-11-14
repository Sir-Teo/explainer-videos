"""Helpers shared by the scenes of Part 18 ("Progressions")."""

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

PART = 18
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
DIM = "#3A4250"
VOICE_C = ("#F5C542", "#F472B6", "#A3E635", "#7DD3FC")             # soprano, alto, tenor, bass
FUNC_C = {"T": "#F5C542", "S": "#A3E635", "D": "#F472B6"}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def block_staff(chords, width: float = 6.0, space: float = 0.15, key: int = 0, beats: int = 2) -> GrandStaff:
    """Chords (S, A, T, B) on a grand staff: soprano and alto on the treble staff, tenor and bass on the bass staff."""
    def pitch(m):
        return SC.Pitch.from_midi(int(m), flats=key < 0)

    d = Fraction(beats, 4)
    up = SC.Voice([SC.Chord(tuple({pitch(c[0]), pitch(c[1])}), d) if c[0] != c[1] else SC.Note(pitch(c[0]), d) for c in chords], clef="treble")
    down = SC.Voice([SC.Chord(tuple({pitch(c[2]), pitch(c[3])}), d) if c[2] != c[3] else SC.Note(pitch(c[2]), d) for c in chords], clef="bass")
    sc = SC.Score([up, down], time=(len(chords) * beats, 4), key=key)
    return GrandStaff(sc, width=width, space=space, show_time=False, gap=9.5)


def chord_roll(chords, width: float = 10.0, height: float = 3.0, lo: float = 34, hi: float = 84, thick: float = 0.12, gap: float = 0.06) -> VGroup:
    """Chords (S, A, T, B) one after another as bars, a colour to each voice; ``.cols[k]`` is chord k's four bars."""
    n = len(chords)
    frame = Rectangle(width=width, height=height, stroke_width=0, fill_opacity=0)
    g = VGroup(frame)
    w = width / n
    g.cols = []
    for k, ch in enumerate(chords):
        col = VGroup()
        for j, p in enumerate(ch):
            r = RoundedRectangle(width=max(w - gap, 0.04), height=thick, corner_radius=thick / 2.2, stroke_width=0, fill_color=VOICE_C[j], fill_opacity=1.0)
            r.move_to([frame.get_left()[0] + w * (k + 0.5), frame.get_bottom()[1] + height * (p - lo) / (hi - lo), 0])
            col.add(r)
        g.add(col)
        g.cols.append(col)
    g.frame = frame
    g.xk = lambda k: frame.get_left()[0] + w * (k + 0.5)
    return g


def sing_chords(snd, g, times, start: float = 0.0, hot=WHITE, hold: float = 0.25, fade: float = 0.3):
    """Light chord k's four bars when it sounds."""
    for j in range(4):
        flash(snd, [col[j] for col in g.cols], [start + t for t in times], hot=hot, base=VOICE_C[j], fade=fade, hold=hold)


def line_roll(notes, width: float = 10.0, height: float = 2.0, lo: float = 34, hi: float = 60, color=VOICE_C[3]) -> VGroup:
    """A single line of notes, evenly spaced, as dots joined by a thin line."""
    n = len(notes)
    xs = np.linspace(-width / 2, width / 2, n)
    dots = VGroup(*[Dot([x, -height / 2 + height * (p - lo) / (hi - lo), 0], radius=0.08, color=color) for x, p in zip(xs, notes)])
    ln = VMobject(stroke_color=color, stroke_width=2, stroke_opacity=0.5).set_points_as_corners([d.get_center() for d in dots])
    g = VGroup(ln, dots)
    g.dots = dots
    return g
