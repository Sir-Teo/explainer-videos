"""Helpers shared by the scenes of Part 8 ("Fitting and Generalizing").

* :func:`chapter`, the chapter card with its voiceover;
* :func:`log_axes`, axes over log10 ranges with powers of ten; :func:`pct_axes`, axes in percent;
* :func:`bars`, a histogram (or any bar chart) drawn on axes;
* :func:`bound_gap`, the vertical arrow between a measured value and its bound, with a label.
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 8
HIST = C.HUMAN  # history cards
TRAIN, TEST = GREY_B, C.BITS  # error on the examples it learned from; error on new ones
BIAS, VAR = C.TRUE_P, C.MODEL_Q
AUSTEN, DICKENS = "#E86F8A", "#58A6FF"
POS, NEG = "#58A6FF", "#E86F8A"  # the two labels of a binary problem
BOUND = C.INTERVAL  # a bound
MEAS = C.TRUE_P  # a measurement
BAYES = C.ADVANTAGE  # the Bayes rule, the best possible
PANEL = "#121722"


def curve(ax, xs, ys, color, stroke_width=4, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def chapter(scene, k: int, title: str, question: str, spoken: str, lit=()):
    card = chapter_card(k, title, question, lit=lit, part=PART)
    with scene.voiceover(spoken):
        scene.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
    scene.play(FadeOut(card))


def pw(v) -> str:
    v = float(v)
    if abs(v - round(v)) > 1e-9:
        return f"10^{{{v:g}}}"
    v = int(round(v))
    return "1" if v == 0 else ("10" if v == 1 else f"10^{{{v}}}")


def log_axes(xr, yr, x_length=6.0, y_length=3.8, xlabel="", ylabel="", center=ORIGIN, xstep=1, ystep=1,
             font_size=20, xticks=None, yticks=None, xfmt=None, yfmt=None):
    """Axes over log10 ranges, with ticks labelled as powers of ten (pass ``xfmt=str`` style formatters to change)."""
    xt = xticks if xticks is not None else list(range(int(math.ceil(xr[0])), int(math.floor(xr[1])) + 1, xstep))
    yt = yticks if yticks is not None else list(range(int(math.ceil(yr[0])), int(math.floor(yr[1])) + 1, ystep))
    return axes(list(xr), list(yr), x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel, xticks=xt,
                yticks=yt, xfmt=xfmt or pw, yfmt=yfmt or pw, font_size=font_size, center=center)


def pct_axes(xr, yr, yticks, x_length=6.0, y_length=3.8, xlabel="", ylabel="", center=ORIGIN, xticks=None,
             xfmt=None, font_size=20):
    """Axes whose y is a share, labelled in percent."""
    return axes(list(xr), list(yr), x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel,
                xticks=xticks, yticks=yticks, xfmt=xfmt, yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=font_size,
                center=center)


def bars(ax, xs, hs, width, color, opacity=0.75, stroke=0.0) -> VGroup:
    """Bars of height hs centred at xs (axis units), each ``width`` wide."""
    g = VGroup()
    y0 = ax.y_range[0] if not isinstance(ax, CornerAxes) else ax._off[1]
    for x, h in zip(xs, hs):
        if h <= y0:
            continue
        a, b = ax.c2p(x - width / 2, y0), ax.c2p(x + width / 2, h)
        r = Rectangle(width=max(b[0] - a[0], 0.004), height=max(b[1] - a[1], 0.002), stroke_width=stroke,
                      stroke_color=color, fill_color=color, fill_opacity=opacity)
        r.move_to([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0])
        g.add(r)
    return g


def bound_gap(top, bottom, text, color=BOUND, side=RIGHT, font_size=22):
    """A double arrow from ``bottom`` to ``top`` (points) with a label beside it."""
    a = DoubleArrow(bottom, top, buff=0, color=color, stroke_width=2.5, tip_length=0.14,
                    max_tip_length_to_length_ratio=0.3)
    t = label(text, font_size=font_size, color=color).next_to(a, side, buff=0.12)
    return VGroup(a, t)


def heat_strip(values, colors, cell=0.12, cols=56, buff=0.02, opacity=0.9) -> VGroup:
    """A grid of small squares, one per item, coloured by its value's key in ``colors``."""
    g = VGroup(*[Square(cell, stroke_width=0, fill_color=colors[v], fill_opacity=opacity) for v in values])
    return g.arrange_in_grid(cols=cols, buff=buff)
