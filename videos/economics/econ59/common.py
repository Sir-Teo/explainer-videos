"""Helpers shared by the scenes of Part 59 of *Economics, Built* ("The Expert Witness"): the chapter card, axes,
curves, the Island's map of towns, and colours."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import merger  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, TRUTH, film_time, load  # noqa: F401

PART = 59
ASK = r"How is economics used to decide a merger, and what survives cross-examination?"

HOLD = E.MISS              # caveats
TRUTHC = "#FFFFFF"         # the planted truth
GRID = "#9AA3B2"
RECESS = "#3A3F4B"
ALDER = "#7EC8F5"          # Alder, the chain in every town
BIRCH = "#F2C14E"          # Birch
CEDAR = "#7FD1B9"          # Cedar
SHOPS = "#9AA3B2"          # the corner shops
GOV = "#E8A0B4"            # the agency, the plaintiff
DEF = "#C9A0FF"            # the defence
CARTEL = "#F25F5C"         # cartels and harm
SAVE = "#7BD88F"           # savings, efficiencies
WORK = "#F2A65A"           # workers
REG = "#9FB8F2"            # regulators
SIM = "#F2A65A"            # simulations
COST = "#F25F5C"
GAIN = "#7BD88F"
FARE = "#7EC8F5"           # airline fares


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("world",), horizon=("a century",),
         hold: float = 0.0):
    """The chapter card of this part, narrated, then cleared."""
    chapter(scene, PART, ASK, n, title, question, say, lit=lit, scale=scale, horizon=horizon, hold=hold)


def plane(x_range, y_range, center=ORIGIN, x_length=5.6, y_length=5.2, xticks=None, yticks=None, xlabel="",
          ylabel="", font_size=19, xfmt=None, yfmt=None):
    from explainer.ai.viz import axes

    return axes(list(x_range), list(y_range), x_length=x_length, y_length=y_length, xticks=xticks, yticks=yticks,
                xlabel=xlabel, ylabel=ylabel, font_size=font_size, center=center, xfmt=xfmt, yfmt=yfmt)


def path(ax, xs, ys, color=WHITE, width=3.0, xr=None, yr=None, smooth=True):
    """A curve through (x, y) on axes ``ax``, keeping the points inside the ranges given."""
    a = ax.ax
    pts = []
    for x, y in zip(xs, ys):
        if x is None or y is None or not (np.isfinite(x) and np.isfinite(y)):
            continue
        if xr and not (xr[0] <= x <= xr[1]):
            continue
        if yr and not (yr[0] <= y <= yr[1]):
            continue
        pts.append(a.c2p(x, y))
    m = VMobject(stroke_color=color, stroke_width=width)
    if len(pts) > 3 and smooth:
        m.set_points_smoothly(pts)
    elif len(pts) > 1:
        m.set_points_as_corners(pts)
    return m


def band(ax, xs, lo, hi, color, opacity=0.18, yr=None):
    """A shaded band between ``lo`` and ``hi``, clipped to ``yr`` when given."""
    a = ax.ax
    if yr is not None:
        lo, hi = np.clip(lo, *yr), np.clip(hi, *yr)
    up = [a.c2p(x, y) for x, y in zip(xs, hi)]
    dn = [a.c2p(x, y) for x, y in zip(xs, lo)][::-1]
    return Polygon(*up, *dn, stroke_width=0, fill_color=color, fill_opacity=opacity)


def seg(ax, x0, y0, x1, y1, color=WHITE, width=3.0, dashed=False):
    a = ax.ax
    cls = DashedLine if dashed else Line
    return cls(a.c2p(x0, y0), a.c2p(x1, y1), color=color, stroke_width=width)


def dot(ax, x, y, color=WHITE, r=0.07):
    return Dot(ax.ax.c2p(x, y), radius=r, color=color)


def shade(ax, spans, y0, y1, color=RECESS, opacity=0.55):
    """Bands over the x-intervals ``spans``, from y0 to y1."""
    g = VGroup()
    for a, b in spans:
        p0, p1 = ax.ax.c2p(a, y0), ax.ax.c2p(b, y1)
        if p1[0] - p0[0] < 0.02:
            p1 = p0 + np.array([0.02, p1[1] - p0[1], 0])
        g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=color, fill_opacity=opacity,
                        stroke_width=0).move_to((p0 + p1) / 2))
    return g


def vline(ax, x, y0, y1, color=GREY_B, width=2.0):
    return DashedLine(ax.ax.c2p(x, y0), ax.ax.c2p(x, y1), color=color, stroke_width=width)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def presence_color(birch: bool, cedar: bool):
    """The colour of a town on the map: who is there besides Alder."""
    if birch and cedar:
        return WHITE
    if birch:
        return BIRCH
    if cedar:
        return CEDAR
    return ALDER


def island_map(T, width: float = 8.0, height: float = 4.4, radius: float = 0.07, outline: bool = True):
    """The Island's sixty towns as dots on an outline, coloured by which superstores are there; bigger towns larger.
    Returns a group with ``.dots`` (in town order) and ``.coast``."""
    x, y, size = np.array(T["x"]), np.array(T["y"]), np.array(T["size"])
    sx, sy = width / 12.4, height / 6.0
    coast = Ellipse(width=width, height=height, stroke_color=GREY_C, stroke_width=2, fill_color="#162330",
                    fill_opacity=0.9)
    dots = VGroup()
    for k in range(len(x)):
        r = radius * (1.0 + 0.35 * float(np.clip(size[k], -1.5, 2.0)))
        dots.add(Dot([x[k] * sx, y[k] * sy, 0], radius=max(r, 0.035),
                     color=presence_color(bool(T["birch"][k]), bool(T["cedar"][k]))))
    g = VGroup(coast, dots) if outline else VGroup(dots)
    g.dots, g.coast = dots, coast
    return g


def legend_rows(items, font_size=17):
    """A key: [(colour, text)] as dots with labels, stacked."""
    rows = VGroup()
    for col, txt in items:
        rows.add(VGroup(Dot(radius=0.07, color=col), label(txt, font_size=font_size, color=col)).arrange(
            RIGHT, buff=0.15))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
