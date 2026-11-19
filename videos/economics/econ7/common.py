"""Helpers shared by the scenes of Part 7 of *Economics, Built* ("Time and Risk")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import risk as rk  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 7
ASK = r"How do people choose when the pay-off comes later, or may not come at all?"

TODAY = "#F6C453"       # today's consumption, a budget line
LATER = "#7EC8F5"       # tomorrow's consumption, an indifference curve
SAFE = "#7BD88F"        # a sure thing
RISKY = "#F28C6F"       # a gamble
UTIL = "#C9A0FF"        # a utility function
EUL = "#5BD1C4"         # expected utility's indifference lines
FAN = "#F2A65A"         # lines that fan out (not expected utility)
AMBIG = "#E9A3C9"       # ambiguity
BIAS = E.MISS           # present bias
COINC = "#E8C07D"       # the coin
CHOICE = WHITE
PASS = E.TRUTH
WHO = {k: island.CAST[k].color for k in ("ana", "bo", "chidi", "dara")}


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("person",), horizon=("a year",),
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
        if not (np.isfinite(x) and np.isfinite(y)):
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


def triangle(center=ORIGIN, side=5.2, font_size=20, low=r"\$0", mid=r"\$1M", high=r"\$5M"):
    """The Marschak-Machina triangle: the chance of the worst outcome across, of the best up; the middle outcome
    gets the rest.  ``.p(pl, ph)`` maps chances to the screen."""
    o = np.array(center) + np.array([-side / 2, -side / 2, 0])

    def p(pl, ph):
        return o + np.array([side * pl, side * ph, 0])

    tri = Polygon(p(0, 0), p(1, 0), p(0, 1), stroke_color=GREY_B, stroke_width=2.5, fill_color=GREY_E,
                  fill_opacity=0.25)
    xl = label(rf"chance of {low}", font_size=font_size, color=GREY_A).next_to(p(0.5, 0), DOWN, buff=0.25)
    yl = label(rf"chance of {high}", font_size=font_size, color=GREY_A).rotate(PI / 2).next_to(p(0, 0.5), LEFT,
                                                                                               buff=0.25)
    corners = VGroup(label(rf"{mid} for sure", font_size=font_size - 2, color=GREY_B).next_to(p(0, 0), DL, buff=0.08),
                     label(rf"{low} for sure", font_size=font_size - 2, color=GREY_B).next_to(p(1, 0), DOWN, buff=0.08),
                     label(rf"{high} for sure", font_size=font_size - 2, color=GREY_B).next_to(p(0, 1), UP, buff=0.08))
    ticks = VGroup(*[MathTex(f"{v:g}", font_size=font_size - 4, color=GREY_C).next_to(p(v, 0), DOWN, buff=0.08)
                     for v in (0.5,)])
    g = VGroup(tri, xl, yl, corners, ticks)
    g.p, g.tri, g.side = p, tri, side
    return g


def tri_path(tr, pts, color=EUL, width=2.5, opacity=1.0):
    """A polyline in the triangle through (p_low, p_high) points."""
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    m.set_points_as_corners([tr.p(a, b) for a, b in pts])
    return m


def lottery_card(rows, title: str, color=RISKY, width=3.6, font_size=24) -> VGroup:
    """A lottery as a small card: a title and its (chance, prize) rows."""
    t = label(title, font_size=font_size + 4, color=color)
    body = VGroup(*[label(rf"{c} \ $\to$ \ {x}", font_size=font_size) for c, x in rows]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.12)
    inner = VGroup(t, body).arrange(DOWN, buff=0.2)
    box = RoundedRectangle(width=max(width, inner.width + 0.5), height=inner.height + 0.5, corner_radius=0.12,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.07)
    inner.move_to(box)
    g = VGroup(box, inner)
    g.box, g.title, g.body = box, t, body
    return g


def coin_glyph(r: float = 0.45, face: str = "H", color=COINC) -> VGroup:
    """A coin with a letter on its face."""
    disc = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25)
    rim = Circle(radius=r * 0.82, stroke_color=color, stroke_width=1.5, stroke_opacity=0.6)
    t = Text(face, font_size=int(48 * r / 0.45), color=color, weight=BOLD)
    return VGroup(disc, rim, t)


def tex_safe(s: str) -> str:
    """Plain text (a citation, a dial's sample) made safe for a Tex label."""
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def signed(x: float, digits: int = 2) -> str:
    """+0.34, -0.61, and 0.00 (never -0.00), for the screen."""
    v = round(x, digits)
    if v == 0:
        return f"{0.0:.{digits}f}"
    return ("$+$" if v > 0 else "$-$") + f"{abs(v):.{digits}f}"


def big(x: float) -> str:
    """1,300,000,000 -> 1.3 billion; 12,210,880 -> 12.2 million; 718,190 -> 718,190 (for the screen)."""
    if not np.isfinite(x):
        return r"any sum"
    if x >= 1e9:
        return rf"\${x / 1e9:.1f} billion"
    if x >= 1e7:
        return rf"\${x / 1e6:.1f} million"
    return rf"\${x:,.0f}".replace(",", "{,}")
