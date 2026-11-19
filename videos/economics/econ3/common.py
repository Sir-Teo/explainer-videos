"""Helpers shared by the scenes of Part 3 of *Economics, Built* ("The Measure")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 3
ASK = r"How do you put a number on an economy?"  # the part's question, in the corner of every chapter card

# one meaning per colour, for this part (the series' E.* keep theirs)
IND_COLOR = {"fishing": E.FISH, "coconut grove": E.COCONUT, "boatyard": "#E07B53", "ferry": "#9FB8F2"}
IND_NAME = {"fishing": r"fishing", "coconut grove": r"coconut grove", "boatyard": r"boatyard", "ferry": r"ferry"}
WAGES = E.HOUSEHOLDS
PROFITS = E.FIRMS
TAXES = E.GOVERNMENT
USE_COLOR = {"C": E.HOUSEHOLDS, "I": E.BANKS, "G": E.GOVERNMENT, "X": E.WORLD, "M": E.WORLD}
USE_NAME = {"C": r"consumption", "I": r"investment", "G": r"government", "X": r"exports", "M": r"imports"}
LASP = "#F28C6F"      # Laspeyres: the old basket
PAAS = "#6FC3F2"      # Paasche: the new basket
FISHER = E.ACCENT     # Fisher's ideal index
TRUE = E.TRUTH        # the true cost of living (the Island's, known)
UNPAID = "#C9A0FF"    # work the accounts leave out
STORM_C = "#8FA3B8"   # a stormy season on the Island
DARA = island.CAST["dara"].color
BO = island.CAST["bo"].color
KUZ = "#E8D5A8"       # the 1934 report's paper


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("nation",), horizon=("a year",),
         hold: float = 0.0):
    """The chapter card of this part, narrated, then cleared."""
    chapter(scene, PART, ASK, n, title, question, say, lit=lit, scale=scale, horizon=horizon, hold=hold)


def tn(x_billions: float, digits: int = 2) -> str:
    """$30.86 trillion for the screen, from billions."""
    return rf"\${x_billions / 1000:,.{digits}f}" + r"\ \text{trillion}"


def say_tn(x_billions: float, digits: int = 1) -> str:
    """'30.9 trillion dollars' for the narrator."""
    return f"{x_billions / 1000:.{digits}f} trillion dollars"


def bn(x_millions: float, digits: int = 1) -> str:
    """$83.0 billion for the screen, from millions."""
    return rf"\${x_millions / 1000:,.{digits}f}" + r"\ \text{bn}"


def band(x0: float, y0a: float, y0b: float, x1: float, y1a: float, y1b: float, color, opacity: float = 0.55,
         bend: float = 0.5) -> VMobject:
    """A Sankey ribbon from the vertical span [y0a, y0b] at x0 to [y1a, y1b] at x1 (top edges first)."""
    c = bend * (x1 - x0)
    top = CubicBezier([x0, y0a, 0], [x0 + c, y0a, 0], [x1 - c, y1a, 0], [x1, y1a, 0])
    bot = CubicBezier([x1, y1b, 0], [x1 - c, y1b, 0], [x0 + c, y0b, 0], [x0, y0b, 0])
    shape = VMobject(stroke_width=0, fill_color=color, fill_opacity=opacity)
    pts = list(top.get_points()) + [np.array([x1, y1a, 0]), np.array([x1, y1b, 0])]
    shape.set_points_as_corners([top.point_from_proportion(t) for t in np.linspace(0, 1, 30)]
                                + [bot.point_from_proportion(t) for t in np.linspace(0, 1, 30)]
                                + [top.point_from_proportion(0)])
    del pts
    return shape


def stack_column(x: float, values, colors, labels, total_height: float, top: float, width: float = 0.5,
                 font_size=20, side=RIGHT, gap: float = 0.05, scale: float | None = None):
    """A column of stacked blocks, top-down, heights proportional to ``values``; returns the VGroup with ``.spans``
    (each block's (top, bottom) y) for the ribbons, and ``.blocks``, ``.texts``."""
    k = scale if scale is not None else (total_height - gap * (len(values) - 1)) / float(sum(values))
    g = VGroup()
    spans, blocks, texts = [], VGroup(), VGroup()
    y = top
    for v, c, t in zip(values, colors, labels):
        h = v * k
        r = Rectangle(width=width, height=max(h, 0.01), stroke_width=0, fill_color=c, fill_opacity=0.9)
        r.move_to([x, y - h / 2, 0])
        spans.append((y, y - h))
        blocks.add(r)
        if t:
            tx = label(t, font_size=font_size, color=c)
            tx.next_to(r, side, buff=0.12)
            texts.add(tx)
        y -= h + gap
    g.add(blocks, texts)
    g.spans, g.blocks, g.texts, g.k = spans, blocks, texts, k
    return g


def flag(text: str, color, font_size=22) -> VGroup:
    """A small rounded label with a coloured outline, for picking out one point on a chart."""
    t = label(text, font_size=font_size, color=color)
    box = SurroundingRectangle(t, buff=0.08, corner_radius=0.08, stroke_color=color, stroke_width=1.5,
                               fill_color=BACKGROUND, fill_opacity=0.85)
    return VGroup(box, t)


def meter_glyph(r: float = 0.6, value: float = 0.62, color=E.ACCENT, stroke_width: float = 4) -> VGroup:
    """A gauge: an arc with ticks and a needle at ``value`` (0 = left, 1 = right).  The Part's emblem: a meter on
    every pipe."""
    arc = Arc(radius=r, start_angle=PI * 0.95, angle=-PI * 0.9, stroke_color=color, stroke_width=stroke_width)
    ticks = VGroup()
    for k in range(7):
        a = PI * 0.95 - PI * 0.9 * k / 6
        u = np.array([np.cos(a), np.sin(a), 0])
        ticks.add(Line(u * r * 0.78, u * r * 0.95, stroke_color=color, stroke_width=stroke_width * 0.6))
    a = PI * 0.95 - PI * 0.9 * value
    needle = Line(ORIGIN, np.array([np.cos(a), np.sin(a), 0]) * r * 0.82, stroke_color=WHITE,
                  stroke_width=stroke_width * 0.9)
    hub = Dot(ORIGIN, radius=r * 0.09, color=WHITE)
    g = VGroup(arc, ticks, needle, hub)
    g.arc, g.ticks, g.needle, g.hub = arc, ticks, needle, hub
    return g


def report_cover(width: float = 3.4, font_size=22) -> VGroup:
    """The 1934 report as a printed cover: the Senate document number, the title, the date."""
    h = width * 1.32
    page = Rectangle(width=width, height=h, stroke_color=GREY_B, stroke_width=1.5, fill_color=KUZ, fill_opacity=0.95)
    ink = "#2B2B2B"
    top = VGroup(label(r"73d Congress, 2d Session", font_size=font_size - 8, color=ink),
                 label(r"Senate Document No.\ 124", font_size=font_size - 6, color=ink)).arrange(DOWN, buff=0.06)
    title = label(r"NATIONAL INCOME, \\ 1929--32", font_size=font_size + 6, color=ink)
    mid = VGroup(label(r"Letter from the Acting Secretary", font_size=font_size - 9, color=ink),
                 label(r"of Commerce", font_size=font_size - 9, color=ink)).arrange(DOWN, buff=0.04)
    date = label(r"January 4, 1934", font_size=font_size - 7, color=ink)
    body = VGroup(top, title, mid, date).arrange(DOWN, buff=0.32)
    if body.width > width - 0.4:
        body.width = width - 0.4
    body.move_to(page)
    rule = Line(LEFT * (width / 2 - 0.3), RIGHT * (width / 2 - 0.3), stroke_color=ink, stroke_width=1.2)
    rule.next_to(title, DOWN, buff=0.16)
    g = VGroup(page, body, rule)
    g.page = page
    return g
