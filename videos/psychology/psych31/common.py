"""Helpers shared by the scenes of Part 31 of *Psychology, Built* ("The Lifespan")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 31

# one meaning per colour, for this part
AGE = "#7EC8F5"  # the age clock: growing older
PERIOD = "#F2C14E"  # the period clock: the year of testing
COHORT = "#B39DDB"  # the cohort clock: the year of birth
CHILD = "#FFB3C7"  # children
CARE = "#FF9F43"  # families, care and programmes
MODEL = "#B39DDB"  # what Psyche computes
TRUE = "#5BD18B"  # the true curve in a simulation
GOOD = "#5BD18B"
LOST = "#EF6F6C"
YOU = "#F2C14E"  # the viewer
DATA = P.ARCHIVE
KANT = P.KANT
OLD = "#E8A87C"  # later life


def pct(x: float, digits: int = 0) -> str:
    return rf"{100 * x:.{digits}f}\%"


def spct(x: float) -> str:
    """A share as narration reads it: "45 percent"."""
    return f"{100 * x:.0f} percent"


def num(n) -> str:
    """An integer with thousands separators that TeX sets without a gap."""
    return f"{int(n):,}".replace(",", "{,}")


def keep_in_frame(mob, margin: float = 0.25):
    half = config.frame_width / 2 - margin
    if mob.get_left()[0] < -half:
        mob.shift(RIGHT * (-half - mob.get_left()[0]))
    if mob.get_right()[0] > half:
        mob.shift(LEFT * (mob.get_right()[0] - half))
    return mob


def rows_of(items, width: float, font_size: int = 30, buff: float = 0.34) -> VGroup:
    """Lines of text, each (text, colour), wrapped to ``width`` and stacked."""
    return VGroup(*[wrapped_label(t, width, font_size, c) for t, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def bounds(ax):
    """The data range of an axis pair (corner axes store their ranges shifted to start at zero)."""
    ox, oy = getattr(ax, "_off", (0.0, 0.0))
    return (float(ax.x_range[0] + ox), float(ax.x_range[1] + ox)), (float(ax.y_range[0] + oy), float(ax.y_range[1] + oy))


def scatter(ax, x, y, color, radius: float = 0.04, opacity: float = 0.85) -> VGroup:
    (x0, x1), (y0, y1) = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1) & np.isfinite(x) & np.isfinite(y)
    return VGroup(*[Dot(ax.c2p(float(a), float(b)), radius=radius, color=color, fill_opacity=opacity)
                    for a, b in zip(x[keep], y[keep])])


def curve_in(ax, x, y, color, stroke_width=3, smooth=False):
    """A curve with the points outside the axes' x range left out."""
    (x0, x1), _ = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1)
    return curve(ax, x[keep], y[keep], color, stroke_width=stroke_width, smooth=smooth)


def bars(ax, xs, ys, color, width: float = 0.6, opacity: float = 0.85) -> VGroup:
    """Vertical bars from zero (or the axis floor) to ``ys`` at ``xs``, in data units."""
    (_, _), (y0, _) = bounds(ax)
    out = VGroup()
    colors = color if isinstance(color, (list, tuple)) else [color] * len(xs)
    for x, y, c in zip(xs, ys, colors):
        lo, hi = ax.c2p(float(x), max(y0, 0.0)), ax.c2p(float(x), float(y))
        w = abs(ax.c2p(float(x) + width / 2, 0)[0] - ax.c2p(float(x) - width / 2, 0)[0])
        out.add(Rectangle(width=w, height=max(abs(hi[1] - lo[1]), 1e-3), stroke_width=0, fill_color=c,
                          fill_opacity=opacity).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
    return out


def word_chip(word: str, color=AGE, font_size=26, width=None) -> VGroup:
    """A word in a rounded box."""
    t = label(word, font_size=font_size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=width or t.width + 0.3, height=t.height + 0.25,
                           stroke_color=color, stroke_width=2, fill_color=BLACK, fill_opacity=0.6)
    return VGroup(box, t.move_to(box))


def clock(text: str, color, radius: float = 0.55) -> VGroup:
    """A small clock face with a name under it: one of the three clocks."""
    face = Circle(radius=radius, color=color, stroke_width=4, fill_color=color, fill_opacity=0.12)
    hands = VGroup(Line(ORIGIN, UP * radius * 0.7, color=color, stroke_width=4),
                   Line(ORIGIN, RIGHT * radius * 0.5, color=color, stroke_width=4))
    ticks = VGroup(*[Line(UP * radius * 0.85, UP * radius, color=color, stroke_width=2).rotate(k * PI / 6,
                                                                                           about_point=ORIGIN)
                     for k in range(12)])
    name = label(text, font_size=24, color=color).next_to(face, DOWN, buff=0.15)
    return VGroup(VGroup(face, ticks, hands), name)


def person(height: float = 1.0, color=WHITE) -> VGroup:
    """A simple standing figure."""
    head = Circle(radius=0.14 * height, color=color, fill_color=color, fill_opacity=0.9, stroke_width=0)
    body = Line(ORIGIN, DOWN * 0.45 * height, color=color, stroke_width=4)
    arms = Line(LEFT * 0.2 * height, RIGHT * 0.2 * height, color=color, stroke_width=4).shift(DOWN * 0.15 * height)
    legs = VGroup(Line(DOWN * 0.45 * height, DOWN * 0.8 * height + LEFT * 0.15 * height, color=color, stroke_width=4),
                  Line(DOWN * 0.45 * height, DOWN * 0.8 * height + RIGHT * 0.15 * height, color=color, stroke_width=4))
    head.move_to(UP * 0.14 * height)
    return VGroup(head, body, arms, legs)
