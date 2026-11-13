"""Helpers shared by the scenes of Part 5 ("Consonance")."""

from __future__ import annotations

import numpy as np

from explainer.music.kit import *  # noqa: F403

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 5
clip = clip_loader(CACHE, CLIPS)
SMOOTH, ROUGH = GOOD, BAD


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, links=("ear",), extra=extra, spoken=spoken)


def ratio_axis(r_lo=1.0, r_hi=2.2, y_hi=1.0, x_length=10.0, y_length=3.2, ylabel=r"roughness", marks=((1, 1), (6, 5), (5, 4), (4, 3), (3, 2), (5, 3), (2, 1)),
               font_size=20) -> VGroup:
    """Axes whose x is an interval, laid out evenly in pitch (so an octave is the same width anywhere), with the
    just ratios marked along the bottom.  ``g.at(ratio, y)`` is the point for a ratio."""
    g = axes([np.log2(r_lo), np.log2(r_hi)], [0, y_hi], x_length=x_length, y_length=y_length, xlabel="", ylabel=ylabel, xticks=None, yticks=[],
             font_size=font_size)
    g.at = lambda r, y: g.ax.c2p(float(np.log2(r)), y)
    g.marks = VGroup()
    for p, q in marks:
        x = g.at(p / q, 0)
        g.marks.add(VGroup(Line(x, x + DOWN * 0.1, color=GREY_C, stroke_width=1.5),
                           MathTex(rf"{p}{{:}}{q}", font_size=font_size + 2, color=GREY_A).next_to(x, DOWN, buff=0.16)))
    g.add(g.marks)
    return g


def rcurve(g, ratios, values, color, stroke_width=3):
    return curve(g.ax, np.log2(np.asarray(ratios, dtype=float)), np.asarray(values, dtype=float), color, stroke_width=stroke_width)


def partial_lines(at, freqs, amps, unit: float, height: float = 1.0, color=TUNE, stroke_width: float = 4.0) -> VGroup:
    """Partials as upright lines on a frequency axis that starts at ``at``: ``unit`` is the length of 1 Hz."""
    return VGroup(*[Line(at + RIGHT * f * unit, at + RIGHT * f * unit + UP * height * a, color=color, stroke_width=stroke_width)
                    for f, a in zip(freqs, amps)])


def envelope_shape(box, fn, t: float, span: float, color=TUNE, n: int = 240) -> list:
    """Points of a filled envelope ``+-fn(time)`` inside ``box``, showing ``span`` seconds around ``t``."""
    xs = np.linspace(-0.5, 0.5, n)
    e = np.array([fn(t + x * span) for x in xs])
    w, h = box.width * 0.92, box.height * 0.4
    top = [box.get_center() + RIGHT * w * x + UP * h * v for x, v in zip(xs, e)]
    bot = [box.get_center() + RIGHT * w * x + DOWN * h * v for x, v in zip(xs[::-1], e[::-1])]
    return top + bot + top[:1]
