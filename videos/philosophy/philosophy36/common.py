"""Helpers shared by the scenes of Part 36 ("Weighing Lives")."""

from __future__ import annotations

import math  # noqa: F401

import numpy as np  # noqa: F401

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import population as Pop  # noqa: F401

from .compute import load  # noqa: F401

PART = 36
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
WELL = "#5EE6D0"      # welfare
POP = "#6FB7FF"       # population, numbers
FUT = "#C3A6FF"       # the future, time
RISK = "#F28EC2"      # risk, harm
MONEY = "#F2C14E"     # money, prices
INF = "#F2A65A"       # infinity, streams


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


def parfit_bars(groups, x0, base_y, unit_w=0.1, unit_h=0.2, color=WELL, gap=0.0, opacity=0.8):
    """Parfit's diagram: one block per group, width proportional to the number of people, height to welfare;
    blocks of one population side by side."""
    g = VGroup()
    x = x0
    for n, w in groups:
        wd, ht = unit_w * n, unit_h * abs(w)
        r = Rectangle(width=wd, height=max(ht, 0.02), stroke_width=1, stroke_color=color, fill_color=color,
                      fill_opacity=opacity)
        r.move_to([x + wd / 2, base_y + (ht / 2 if w >= 0 else -ht / 2), 0])
        g.add(r)
        x += wd + gap
    return g
