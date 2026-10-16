"""Helpers shared by the scenes of Part 2 ("Limits: Sequences, Series, Continuity and the Derivative").

Part 2 reuses Part 1's helpers (the zoomable Window with its rational ruler, pinned labels, interval endpoints)
and the series' instruments from ``explainer/analysis``, including the epsilon-delta game boards.
"""

from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis1.common import SQRT2, Window, endpoint, interval_bar, pin, polyline  # noqa: F401

from .compute import load  # noqa: F401


def plain_axes(x_range, y_range, x_length, y_length, numbers=False, font_size=22, **kw) -> Axes:
    cfg = {"stroke_color": GREY_C, "include_numbers": numbers, "font_size": font_size}
    cfg.update(kw.pop("axis_config", {}))
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length, tips=False, axis_config=cfg, **kw)


def hop(start, end, color, up=True, stroke_width=3, tip=0.14) -> VMobject:
    """A curved arrow above (or below) a number line from one point to another."""
    ang = (-TAU / 5 if end[0] > start[0] else TAU / 5) * (1 if up else -1)
    return CurvedArrow(np.asarray(start) + UP * 0.08 * (1 if up else -1), np.asarray(end) + UP * 0.08 * (1 if up else -1),
                       angle=ang, color=color, stroke_width=stroke_width, tip_length=tip)


def sum_plot(ax: Axes, sums, color=C.SEQ, stroke_width=2.5, k0=1) -> VMobject:
    """Partial sums s_k against k as a polyline on ``ax`` (k starting at k0)."""
    k = np.arange(k0, k0 + len(sums))
    return polyline(ax, k, sums, color=color, stroke_width=stroke_width)


def runs_in_range(ax, x, y, lo, hi, color, stroke_width=3) -> VGroup:
    """The graph of y over x, drawn only where it lies within [lo, hi] (pieces that leave the axes are cut, not
    flattened against the edge)."""
    ok = (y > lo) & (y < hi)
    g, start = VGroup(), None
    for i in range(len(x) + 1):
        if i < len(x) and ok[i]:
            start = i if start is None else start
        elif start is not None:
            if i - start > 1:
                g.add(polyline(ax, x[start:i], y[start:i], color=color, stroke_width=stroke_width))
            start = None
    return g


def magnifier_above(src_ax, x_window, y_window, height=1.6, gap=0.3, color=GREY_B, tag=None) -> tuple:
    """A vertical magnifier: the window x_window × y_window of ``src_ax`` redrawn directly above itself, just as wide,
    so only heights are magnified (for small bars and thin boxes near a baseline). The guides run straight up from the
    source frame to the inset. Returns ``(inset_ax, decor)`` like ``magnifier``: draw on ``inset_ax`` with the
    source's coordinates."""
    x0, x1 = x_window
    y0, y1 = y_window
    p0, p1 = src_ax.c2p(x0, y0), src_ax.c2p(x1, y1)
    width = p1[0] - p0[0]
    src = Rectangle(width=width, height=max(p1[1] - p0[1], 0.04), color=color, stroke_width=2).move_to((p0 + p1) / 2)
    center = np.array([(p0[0] + p1[0]) / 2, src.get_top()[1] + gap + height / 2, 0.0])
    inset = Axes(x_range=[x0, x1, x1 - x0], y_range=[y0, y1, y1 - y0], x_length=width, y_length=height, tips=False,
                 axis_config={"stroke_opacity": 0, "include_ticks": False}).move_to(center)
    dst = Rectangle(width=width, height=height, color=color, stroke_width=2).move_to(center)
    dst.set_fill(BACKGROUND, opacity=1.0)
    guides = VGroup(*[DashedLine(src.get_corner(a), dst.get_corner(b), color=color, stroke_width=1.5, dash_length=0.08)
                      for a, b in ((UL, DL), (UR, DR))])
    k = height / max(p1[1] - p0[1], 1e-9)
    tag = tag if tag is not None else rf"\text{{heights}} \times {k:.0f}"
    t = MathTex(tag, font_size=24, color=color).next_to(dst, UP, buff=0.08).align_to(dst, LEFT)
    decor = VGroup(src, guides, dst, t)
    decor.src, decor.guides, decor.frame, decor.tag = src, guides, dst, t
    return inset, decor


def board_box(board, eps_color=C.EPS, delta_color=C.DELTA) -> VMobject:
    """The game as a box of fixed size: the rectangle (a - delta, a + delta) x (f(a) - eps, f(a) + eps) of a
    ``FunctionBoard``, its top and bottom in the epsilon colour and its sides in the delta colour, clipped to the axes.
    (Used with ``board.piece()``, which colours the graph green inside the box and red where it leaves through the top
    or bottom.)"""

    def draw():
        A = board.ax
        a, d, e, L = board.a.get_value(), board.delta.get_value(), board.eps.get_value(), board.L
        x0, x1 = max(a - d, A.x_range[0]), min(a + d, A.x_range[1])
        y0, y1 = max(L - e, A.y_range[0]), min(L + e, A.y_range[1])
        p00, p11 = A.c2p(x0, y0), A.c2p(x1, y1)
        fill = Rectangle(width=max(0.004, p11[0] - p00[0]), height=max(0.004, p11[1] - p00[1]), stroke_width=0,
                         fill_color=eps_color, fill_opacity=0.14).move_to((p00 + p11) / 2)
        p01, p10 = A.c2p(x0, y1), A.c2p(x1, y0)
        return VGroup(fill, Line(p01, p11, color=eps_color, stroke_width=3), Line(p00, p10, color=eps_color, stroke_width=3),
                      Line(p00, p01, color=delta_color, stroke_width=3), Line(p10, p11, color=delta_color, stroke_width=3))

    return always_redraw(draw)
