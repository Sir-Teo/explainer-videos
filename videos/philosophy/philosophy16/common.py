"""Helpers shared by the scenes of Part 16 ("Evidence by Numbers")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import stats as St  # noqa: F401

from .compute import load  # noqa: F401

PART = 16
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
NULLC = "#9AA5B8"     # the null hypothesis
ALTC = "#5EE6D0"      # the alternative
FISH = "#F2A65A"      # Fisher
NEYP = "#6FB7FF"      # Neyman and Pearson
BAYC = "#F28EC2"      # Bayes
SICK = "#E5534B"
WELL = "#3B4252"


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)


def rows_table(rows, x_label=-6.4, x_text=-3.2, top=1.7, gap=0.42, label_size=22, text_size=21, width=9.6):
    """Rows of (label, text, colour), laid out top-down with wrapped text; returns a VGroup of (label, text)."""
    g = VGroup()
    for a, b, c in rows:
        x = label(a, font_size=label_size, color=c)
        y = wrapped_label(b, width, text_size, WHITE)
        x.move_to([x_label + x.width / 2, top - x.height / 2, 0])
        y.move_to([x_text + y.width / 2, top - y.height / 2, 0])
        g.add(VGroup(x, y))
        top -= max(x.height, y.height) + gap
    return g


def series_plot(ax, ys, color, xs=None, width=3) -> VMobject:
    xs = xs if xs is not None else list(range(len(ys)))
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [ax.c2p(x, y) for x, y in zip(xs, ys)])


def hist_bars(ax, counts, color, total=None, width_frac=0.9) -> VGroup:
    """Bars for a histogram over 20 equal bins of [0, 1] (heights as densities)."""
    total = total or sum(counts)
    k = len(counts)
    g = VGroup()
    for i, c in enumerate(counts):
        dens = c / total * k
        lo, hi = i / k, (i + 1) / k
        w = (ax.c2p(hi, 0)[0] - ax.c2p(lo, 0)[0]) * width_frac
        h = ax.c2p(0, dens)[1] - ax.c2p(0, 0)[1]
        g.add(Rectangle(width=w, height=max(h, 0.001), stroke_width=0, fill_color=color, fill_opacity=0.8).move_to(
            [ax.c2p((lo + hi) / 2, 0)[0], ax.c2p(0, 0)[1] + h / 2, 0]))
    return g
