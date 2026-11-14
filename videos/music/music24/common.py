"""Helpers shared by the scenes of Part 24 ("The Renaissance")."""

from __future__ import annotations

import numpy as np

from explainer.music.chordviz import tex  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.melodyviz import columns, roll  # noqa: F401
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 24
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
DIM = "#3A4250"
VOICE_C = [TUNE, BLUE, EAR, "#A3E635", GREY_B]
NAMES = {0: "C", 1: "C♯", 2: "D", 3: "E♭", 4: "E", 5: "F", 6: "F♯", 7: "G", 8: "G♯", 9: "A", 10: "B♭", 11: "B"}
LETTER = {0: "C", 1: r"C$\sharp$", 2: "D", 3: r"E$\flat$", 4: "E", 5: "F", 6: r"F$\sharp$", 7: "G", 8: r"G$\sharp$", 9: "A", 10: r"B$\flat$", 11: "B"}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def mroll(notes, width=10.0, height=1.8, lo=60, hi=86, color=TUNE, total=None, bar_h=0.13):
    """Notes [midi, onset, duration] as a roll on a time axis of ``total`` units (gaps kept)."""
    total = total or max(n[1] + n[2] for n in notes)
    frame = Rectangle(width=width, height=height, stroke_width=0, fill_opacity=0)
    g = VGroup(frame)
    g.frame, g.total, g.lo, g.hi = frame, total, lo, hi
    g.notes = []
    for p, a, d in notes:
        w = max(width * d / total - 0.04, 0.03)
        b = RoundedRectangle(width=w, height=bar_h, corner_radius=min(0.05, bar_h / 2.5), stroke_width=0, fill_color=color, fill_opacity=1.0)
        b.move_to([frame.get_left()[0] + width * a / total + w / 2 + 0.02, frame.get_bottom()[1] + height * (p - lo) / max(hi - lo, 1), 0])
        g.add(b)
        g.notes.append(b)
    return g


def voices_roll(voices, width=11.0, height=3.0, colors=None, total=None, lo=None, hi=None, bar_h=0.11):
    """Several voices in one frame, each its own colour; ``.parts[j].notes`` for flashing."""
    allp = [n[0] for v in voices for n in v]
    lo = lo if lo is not None else min(allp) - 1
    hi = hi if hi is not None else max(allp) + 1
    total = total or max(n[1] + n[2] for v in voices for n in v)
    colors = colors or VOICE_C
    g = VGroup()
    g.parts = []
    for j, v in enumerate(voices):
        r = mroll(v, width=width, height=height, lo=lo, hi=hi, color=colors[j % len(colors)], total=total, bar_h=bar_h)
        g.add(r)
        g.parts.append(r)
    g.frame = g.parts[0].frame
    g.total = total
    return g


def flash_voices(snd, g, voices, start, unit, hot=WHITE, colors=None):
    colors = colors or VOICE_C
    for j, v in enumerate(voices):
        flash(snd, g.parts[j].notes, [start + n[1] * unit for n in v], hot=hot, base=colors[j % len(colors)])


def cursor(snd, g, start, unit, color=WHITE):
    """A vertical line sweeping the roll in time with the sound."""
    fr = g.frame
    ln = Line(fr.get_corner(DL) + DOWN * 0.1, fr.get_corner(UL) + UP * 0.1, color=color, stroke_width=2, stroke_opacity=0.7)

    def upd(m, t):
        x = (t - start) / unit / g.total
        x = min(max(x, 0.0), 1.0)
        m.move_to([fr.get_left()[0] + fr.width * x, fr.get_center()[1], 0])

    snd.show(ln)
    snd.drive(ln, upd)
    return ln


def text_rows(items, font_size=25, buff=0.38, width=12.6):
    rows_ = VGroup(*[label(t, font_size=font_size, color=c_) for t, c_ in items]).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    rows_.scale_to_fit_width(min(rows_.width, width))
    return rows_.move_to(DOWN * 0.1)


def rows_scene(scene, head_text, items, script, font_size=25, buff=0.38, marks="bcdefg"):
    """A heading and rows revealed at bookmarks a, b, c ... (the first row with the heading)."""
    rows_ = text_rows(items, font_size=font_size, buff=buff)
    head = label(head_text, font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
    with scene.voiceover(script) as vo:
        scene.play(FadeIn(head), FadeIn(rows_[0]))
        for mark, r in zip(marks, rows_[1:]):
            vo.wait_until(mark)
            scene.play(FadeIn(r))
    scene.wait(0.4)
    scene.clear_scene()
