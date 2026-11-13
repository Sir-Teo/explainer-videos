"""Helpers shared by the scenes of Part 7 ("Strings, Hammers and Bows")."""

from __future__ import annotations

import numpy as np

from explainer.music.kit import *  # noqa: F403

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 7
clip = clip_loader(CACHE, CLIPS)
WOOD = "#C8A06A"
FELT = "#E8DCC2"
PLUCK, STRUCK, BOWED = AIR, TUNE, EAR     # the three ways, one colour each


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, links=("string", "instrument"), extra=extra, spoken=spoken)


def helmholtz_points(a, b, tau: float, height: float = 0.6, n: int = 2) -> list:
    """The string in Helmholtz motion at phase ``tau`` (0 to 1) of its period: two straight lines from the ends ``a``
    (the bridge) and ``b`` (the nut) to a corner that runs round a parabola."""
    tau = tau % 1.0
    x = 2 * tau if tau < 0.5 else 2 * (1 - tau)
    y = 4 * height * x * (1 - x) * (1 if tau < 0.5 else -1)
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return [a, a + (b - a) * x + UP * y, b]


def helmholtz_y(x: float, tau: float, height: float = 0.6) -> float:
    """The displacement of the point at fraction ``x`` of the string in that motion."""
    tau = tau % 1.0
    xc = 2 * tau if tau < 0.5 else 2 * (1 - tau)
    yc = 4 * height * xc * (1 - xc) * (1 if tau < 0.5 else -1)
    if xc < 1e-9 or xc > 1 - 1e-9:
        return 0.0
    return yc * x / xc if x <= xc else yc * (1 - x) / (1 - xc)


def curve_from(g, xs, ys, color, stroke_width=3):
    return curve(g.ax, np.asarray(xs, dtype=float), np.asarray(ys, dtype=float), color, stroke_width=stroke_width)


def lane(names=("plucked", "struck", "bowed"), colors=(PLUCK, STRUCK, BOWED), width: float = 3.0, height: float = 0.9, buff: float = 0.5, font_size: int = 30) -> VGroup:
    """One box for each way of playing a string; ``pulse`` (kit) lights the one that is sounding."""
    return VGroup(*[VGroup(RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=c, stroke_width=2.5),
                           label(n, font_size=font_size, color=c)) for n, c in zip(names, colors)]).arrange(RIGHT, buff=buff)
