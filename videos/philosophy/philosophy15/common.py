"""Helpers shared by the scenes of Part 15 ("The Problem of Induction")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import induction as I  # noqa: F401

from .compute import load  # noqa: F401

PART = 15
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
PAST = "#FFD166"      # what has been observed
FUT = "#5EE6D0"       # projections into the future
GREENC = "#5FD38D"
BLUEC = "#6FB7FF"
A_C, B_C, C_C = "#F2A65A", "#6FB7FF", "#F28EC2"
RAVEN = "#20242C"     # a black bird, a black swan


def mark(ok: bool, font_size=30) -> Mobject:
    return MathTex(r"\checkmark" if ok else r"\times", font_size=font_size, color=OK if ok else BAD)


def emerald(color, size=0.32) -> VMobject:
    """A small cut gem."""
    pts = [UP * 0.5, RIGHT * 0.45 + UP * 0.15, RIGHT * 0.3 + DOWN * 0.5, LEFT * 0.3 + DOWN * 0.5,
           LEFT * 0.45 + UP * 0.15]
    g = Polygon(*[p * size * 2 for p in pts], stroke_color=WHITE, stroke_width=1.5, fill_color=color, fill_opacity=0.85)
    return g


def caption(text: str, font_size=24, color=GREY_A, buff=0.4) -> Mobject:
    return label(text, font_size=font_size, color=color).to_edge(DOWN, buff=buff)


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)


def series_plot(ax, ys, color, xs=None, width=3) -> VMobject:
    xs = xs if xs is not None else list(range(len(ys)))
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [ax.c2p(x, y) for x, y in zip(xs, ys)])
