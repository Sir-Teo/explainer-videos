"""Helpers shared by the scenes of Part 2 of *Economics, Built* ("The Scissors")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora.curves import Linear  # noqa: F401
from explainer.economics.agora.market import Market  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM, film_time, load  # noqa: F401

PART = 2
ASK = r"What sets a price?"  # the part's question, in the corner of every chapter card

# one meaning per colour, for this part (the series' E.* keep theirs)
WATER = "#6EC6FF"
DIAMOND = "#E6F1FF"
COFFEE = "#C08A5B"
ROBUSTA = "#8C6A4F"
STORM = "#8FA3B8"
TAX = "#E9A3C9"     # the wedge
CAP = "#F26D6D"     # a legal limit
ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color
CHIDI = island.CAST["chidi"].color
FILM_COLOR = {"oil": "#B0B7C3", "arabica": COFFEE, "cocoa": "#9C6B4E", "sugar": "#F2F2F2", "wheat": "#F2B84B",
              "copper": "#E07B53", "tin": "#9FB8D9", "gold": "#F6C453"}
FILM_NAME = {"oil": r"crude oil", "arabica": r"Arabica coffee", "cocoa": r"cocoa", "sugar": r"sugar",
             "wheat": r"wheat", "copper": r"copper", "tin": r"tin", "gold": r"gold"}


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("market",), horizon=("a year",),
         hold: float = 0.0):
    """The chapter card of this part, narrated, then cleared."""
    chapter(scene, PART, ASK, n, title, question, say, lit=lit, scale=scale, horizon=horizon, hold=hold)


def price_axes(q_max, p_range=(0, 6), x_length=6.2, y_length=4.4, qticks=None, pticks=None, qlabel=r"quantity",
               plabel=r"price", center=ORIGIN, font_size=20, money=True):
    """Quantity across, price up: the axes of every demand and supply picture."""
    from explainer.ai.viz import axes

    fmt = (lambda v: rf"\${v:.2f}" if v % 1 else rf"\${v:.0f}") if money else None
    return axes([0, q_max], list(p_range), x_length=x_length, y_length=y_length, xlabel=qlabel, ylabel=plabel,
                xticks=qticks, yticks=pticks, xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), yfmt=fmt,
                center=center, font_size=font_size)


def line_on(ax, q0, p0, q1, p1, color, width=4):
    """A straight segment between two (quantity, price) points on ``ax``."""
    return Line(ax.c2p(q0, p0), ax.c2p(q1, p1), color=color, stroke_width=width)


def drop_glyph(height: float = 1.0, color=WATER) -> VGroup:
    """A drop of water: a round bottom drawn up to a point."""
    r = height * 0.34
    body = VMobject(stroke_width=0, fill_color=color, fill_opacity=0.9)
    pts = [np.array([0, height * 0.62, 0])]
    arc = Arc(radius=r, start_angle=np.pi * 0.08, angle=-np.pi * 1.16, arc_center=[0, -height * 0.05, 0])
    body.set_points_as_corners([pts[0], *arc.get_points()[::4], pts[0]])
    body.make_smooth()
    shine = Arc(radius=r * 0.6, start_angle=np.pi * 0.95, angle=np.pi * 0.35, arc_center=[0, -height * 0.05, 0],
                stroke_color=WHITE, stroke_width=3, stroke_opacity=0.7)
    return VGroup(body, shine)


def gem_glyph(width: float = 1.1, color=DIAMOND) -> VGroup:
    """A cut diamond in profile: the table, the crown and the pavilion, with a few facet lines."""
    w, h = width, width * 0.8
    top = h * 0.32
    outline = Polygon([-w * 0.3, top, 0], [w * 0.3, top, 0], [w * 0.5, top * 0.35, 0], [0, -h * 0.62, 0],
                      [-w * 0.5, top * 0.35, 0], stroke_color=color, stroke_width=3, fill_color=color,
                      fill_opacity=0.18)
    facets = VGroup(Line([-w * 0.5, top * 0.35, 0], [w * 0.5, top * 0.35, 0]),
                    Line([-w * 0.3, top, 0], [-w * 0.12, top * 0.35, 0]), Line([w * 0.3, top, 0], [w * 0.12, top * 0.35, 0]),
                    Line([-w * 0.12, top * 0.35, 0], [0, -h * 0.62, 0]), Line([w * 0.12, top * 0.35, 0], [0, -h * 0.62, 0]))
    facets.set_stroke(color, 1.6, opacity=0.8)
    return VGroup(outline, facets)
