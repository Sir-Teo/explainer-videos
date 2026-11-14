"""Helpers shared by the scenes of Part 14 ("Melody")."""

from __future__ import annotations

import numpy as np

from explainer.music.chordviz import tex  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.melodyviz import columns, dots_matrix, heat, roll  # noqa: F401
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED, keyboard  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 14
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
REAL_C, CHANCE_C = "#F5C542", "#7DD3FC"


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def curve_from(g, xs, ys, color, stroke_width=3):
    return curve(g.ax, np.asarray(xs, dtype=float), np.asarray(ys, dtype=float), color, stroke_width=stroke_width)


def sing(snd, r, times, hot=WHITE, base=None, hold: float = 0.3, fade: float = 0.35):
    """Light the bars of a roll as their notes sound."""
    return flash(snd, r.notes, times, hot=hot, base=base or r.notes[0].get_fill_color(), fade=fade, hold=hold)


def pair_bars(rows, width: float = 8.0, height: float = 2.4, colors=(REAL_C, CHANCE_C), fmt="{:.0f}", font_size: int = 24, top: float = 100.0, names=("the tunes", "by chance")) -> VGroup:
    """Groups of two bars side by side: ``rows`` is a list of (label, value 1, value 2).  ``.groups[k]`` holds the
    two bars and their numbers; ``.legend``."""
    g = VGroup(Line([-width / 2, 0, 0], [width / 2, 0, 0], color="#3A4250", stroke_width=2))
    g.groups = []
    w = width / len(rows)
    for k, (name, a, b) in enumerate(rows):
        x = (k + 0.5) * w - width / 2
        grp = VGroup()
        for j, (v, c) in enumerate(((a, colors[0]), (b, colors[1]))):
            h = max(height * v / top, 0.02)
            bar = Rectangle(width=0.26 * w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.9).move_to([x + (j - 0.5) * 0.3 * w, h / 2, 0])
            grp.add(VGroup(bar, label(fmt.format(v), font_size=font_size, color=WHITE).next_to(bar, UP, buff=0.08)))
        grp.add(label(name, font_size=font_size, color=GREY_A).move_to([x, -0.3, 0]))
        g.add(grp)
        g.groups.append(grp)
    g.legend = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.9), label(n, font_size=font_size - 2, color=GREY_A)).arrange(RIGHT, buff=0.12)
                        for c, n in zip(colors, names)]).arrange(RIGHT, buff=0.6)
    return g
