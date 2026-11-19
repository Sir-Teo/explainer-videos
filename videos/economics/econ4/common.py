"""Helpers shared by the scenes of Part 4 of *Economics, Built* ("The Evidence")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 4
ASK = r"When can data answer an economic question?"

FEAST = "#F2B84B"      # a feast day: demand moves
STORM = "#8FA3B8"      # a storm: supply moves
ORDINARY = GREY_B
OLSC = "#C9A0FF"       # the least-squares line: what the cloud says
IVC = "#5BD1C4"        # an instrument's estimate
EXP = "#7BD88F"        # an experiment
NONEXP = "#F26D6D"     # a non-experimental estimate
DARA = island.CAST["dara"].color


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("market",), horizon=("a year",),
         hold: float = 0.0):
    """The chapter card of this part, narrated, then cleared."""
    chapter(scene, PART, ASK, n, title, question, say, lit=lit, scale=scale, horizon=horizon, hold=hold)


def fish_axes(center=ORIGIN, x_length=6.6, y_length=4.6, font_size=20):
    """Quantity across, price up, for the Island's fish season."""
    from explainer.ai.viz import axes

    return axes([120, 300], [1.8, 4.4], x_length=x_length, y_length=y_length, xticks=[150, 200, 250, 300],
                yticks=[2, 2.5, 3, 3.5, 4], xlabel=r"fish sold that day", ylabel=r"price, dollars",
                yfmt=lambda v: rf"\${v:.2f}", font_size=font_size, center=center)


def line_qp(ax, slope: float, q0: float, p0: float, color, p_range=(1.9, 4.3), width=4, dashed=False):
    """The line q = q0 + slope (p - p0) drawn on fish axes (quantity across, price up), clipped to the frame."""
    a = ax.ax
    pts = []
    for p in np.linspace(p_range[0], p_range[1], 60):
        q = q0 + slope * (p - p0)
        if 120 <= q <= 300:
            pts.append(a.c2p(q, p))
    ln = VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)
    out = DashedVMobject(ln, num_dashes=28) if dashed else ln
    out.ends = (np.array(pts[0]), np.array(pts[-1]))  # a dashed line has no points of its own
    return out


def day_dots(ax, s, radius=0.045):
    """One dot per day, coloured by what happened that day."""
    a = ax.ax
    dots = VGroup()
    for p, q, f, st in zip(s["p"], s["q"], s["feast"], s["storm"]):
        c = FEAST if f and not st else STORM if st and not f else "#E07B53" if f and st else ORDINARY
        dots.add(Dot(a.c2p(q, p), radius=radius, color=c, fill_opacity=0.8))
    return dots


def magnifier(r: float = 0.6, color=E.ACCENT) -> VGroup:
    """A lens over a few dots: the part's emblem."""
    ring = Circle(radius=r, stroke_color=color, stroke_width=6)
    handle = Line(ring.point_at_angle(-PI / 4), ring.point_at_angle(-PI / 4) + np.array([0.55, -0.55, 0]) * r,
                  stroke_color=color, stroke_width=9)
    rng = np.random.default_rng(4)
    dots = VGroup(*[Dot(np.array([rng.uniform(-0.6, 0.6), rng.uniform(-0.6, 0.6), 0]) * r, radius=0.05 * r / 0.6,
                        color=WHITE) for _ in range(9)])
    g = VGroup(ring, handle, dots)
    g.ring, g.handle, g.dots = ring, handle, dots
    return g
