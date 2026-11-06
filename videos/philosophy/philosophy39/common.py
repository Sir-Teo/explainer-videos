"""Helpers shared by the scenes of Part 39 ("The Arithmetic of Democracy")."""

from __future__ import annotations

import math  # noqa: F401

import numpy as np  # noqa: F401

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import vote as V  # noqa: F401

from .compute import load  # noqa: F401

PART = 39
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
VOTE = "#6FB7FF"      # ballots, voters
MAJ = "#5EE6D0"       # majority, Condorcet
SCORE = "#F2C14E"     # scoring rules, Borda
CYC = "#F28EC2"       # cycles, manipulation
TRUTH = "#C3A6FF"     # epistemic: juries, judgments
MACH = "#F2A65A"      # machines, AI
ALT = {"A": "#6FB7FF", "B": "#5EE6D0", "C": "#F2C14E", "D": "#F28EC2", "E": "#C3A6FF",
       "a": "#6FB7FF", "b": "#5EE6D0", "c": "#F2C14E", "x": "#6FB7FF", "y": "#5EE6D0", "z": "#F2C14E"}


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            if m.width > 1.15 * width:
                m = wrapped_label(t, width, font_size, c)
            else:
                m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)


def rows_table(rows, x_label=-6.4, x_text=-2.6, top=1.7, gap=0.45, label_size=22, text_size=21, width=8.8):
    g = VGroup()
    for a, b, c in rows:
        x = label(a, font_size=label_size, color=c)
        y = wrapped_label(b, width, text_size, WHITE)
        x.move_to([x_label + x.width / 2, top - x.height / 2, 0])
        y.move_to([x_text + y.width / 2, top - y.height / 2, 0])
        g.add(VGroup(x, y))
        top -= max(x.height, y.height) + gap
    return g


def mark(v, size=24):
    return MathTex(r"\checkmark" if v else r"\times", font_size=size, color=OK if v else BAD)


def ballot(ranking, count=None, font_size=22, w=0.9, h=0.42) -> VGroup:
    """A ballot as a column of coloured boxes, best on top, with its count above."""
    g = VGroup()
    for i, a in enumerate(ranking):
        box = Rectangle(width=w, height=h, stroke_width=1.2, stroke_color=ALT.get(a, WHITE), fill_color=ALT.get(a, WHITE),
                        fill_opacity=0.28)
        box.move_to([0, -i * (h + 0.06), 0])
        g.add(VGroup(box, label(a, font_size=font_size, color=WHITE).move_to(box)))
    if count is not None:
        g.add(label(str(count), font_size=font_size, color=GREY_A).next_to(g, UP, buff=0.14))
    return g
