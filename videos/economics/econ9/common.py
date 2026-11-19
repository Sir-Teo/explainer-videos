"""Helpers shared by the scenes of Part 9 of *Economics, Built* ("The Invisible Hand, Proved")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import ge  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 9
ASK = r"Can a whole economy of selfish traders reach a state nobody could improve on, and will it?"

ANA = island.CAST["ana"].color      # Ana, and her indifference curves
BO = island.CAST["bo"].color        # Bo
FRIDAY = island.CAST["friday"].color
CHIDI = island.CAST["chidi"].color
FISH = E.FISH
COCO = E.COCONUT
CC = "#F6C453"                      # the contract curve
CORE = "#7BD88F"                    # the core
PRICE = WHITE                       # a price line
LENS = "#C9A0FF"                    # the lens of mutual gains
TIMBER = "#8FD694"
PLAN = "#E9A3C9"                    # the planner
HOLD = E.MISS
GOODS3 = (FISH, "#F2A65A", TIMBER)   # fish, coconuts, timber on the price simplex


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("market",), horizon=("a year",),
         hold: float = 0.0):
    """The chapter card of this part, narrated, then cleared."""
    chapter(scene, PART, ASK, n, title, question, say, lit=lit, scale=scale, horizon=horizon, hold=hold)


def plane(x_range, y_range, center=ORIGIN, x_length=5.6, y_length=5.2, xticks=None, yticks=None, xlabel="",
          ylabel="", font_size=19, xfmt=None, yfmt=None):
    from explainer.ai.viz import axes

    return axes(list(x_range), list(y_range), x_length=x_length, y_length=y_length, xticks=xticks, yticks=yticks,
                xlabel=xlabel, ylabel=ylabel, font_size=font_size, center=center, xfmt=xfmt, yfmt=yfmt)


def path(ax, xs, ys, color=WHITE, width=3.0, xr=None, yr=None, smooth=True):
    """A curve through (x, y) on axes ``ax`` (a plane or a box), keeping the points inside the ranges given."""
    c2p = ax.c2p if hasattr(ax, "c2p") else ax.ax.c2p
    pts = []
    for x, y in zip(xs, ys):
        if not (np.isfinite(x) and np.isfinite(y)):
            continue
        if xr and not (xr[0] <= x <= xr[1]):
            continue
        if yr and not (yr[0] <= y <= yr[1]):
            continue
        pts.append(c2p(x, y))
    m = VMobject(stroke_color=color, stroke_width=width)
    if len(pts) > 3 and smooth:
        m.set_points_smoothly(pts)
    elif len(pts) > 1:
        m.set_points_as_corners(pts)
    return m


class Box(VGroup):
    """The Edgeworth box: Ana's origin at the bottom left, Bo's at the top right.  ``c2p(x, y)`` places Ana's
    bundle (x fish, y coconut bundles); Bo holds what is left.  Ticks on the left and bottom are Ana's, on the right
    and top Bo's."""

    def __init__(self, X, center=ORIGIN, width=6.0, height=5.4, ticks=2, font_size=17, labels=True):
        super().__init__()
        self.X = np.asarray(X, float)
        self.w, self.h = width, height
        self.frame = Rectangle(width=width, height=height, stroke_color=GREY_B, stroke_width=2).move_to(center)
        self.origin = self.frame.get_corner(DL)
        self.add(self.frame)
        self.ticks = VGroup()
        for v in np.arange(0, self.X[0] + 1e-9, ticks):
            x = self.c2p(v, 0)
            self.ticks.add(Line(x, x + UP * 0.08, color=GREY_B, stroke_width=1.5),
                           label(f"{v:g}", font_size=font_size - 3, color=GREY_B).next_to(x, DOWN, buff=0.08))
            xt = self.c2p(v, self.X[1])
            self.ticks.add(Line(xt, xt + DOWN * 0.08, color=GREY_B, stroke_width=1.5),
                           label(f"{self.X[0] - v:g}", font_size=font_size - 3, color=GREY_B).next_to(xt, UP,
                                                                                                    buff=0.08))
        for v in np.arange(0, self.X[1] + 1e-9, ticks):
            y = self.c2p(0, v)
            self.ticks.add(Line(y, y + RIGHT * 0.08, color=GREY_B, stroke_width=1.5),
                           label(f"{v:g}", font_size=font_size - 3, color=GREY_B).next_to(y, LEFT, buff=0.08))
            yr = self.c2p(self.X[0], v)
            self.ticks.add(Line(yr, yr + LEFT * 0.08, color=GREY_B, stroke_width=1.5),
                           label(f"{self.X[1] - v:g}", font_size=font_size - 3, color=GREY_B).next_to(yr, RIGHT,
                                                                                                    buff=0.08))
        self.add(self.ticks)
        self.names = VGroup()
        if labels:
            self.names.add(label(r"Ana", font_size=font_size + 3, color=ANA).next_to(self.frame.get_corner(DL),
                                                                                   DL, buff=0.2),
                           label(r"Bo", font_size=font_size + 3, color=BO).next_to(self.frame.get_corner(UR), UR,
                                                                                 buff=0.2),
                           label(r"fish \ $\rightarrow$", font_size=font_size, color=FISH).next_to(self.frame, DOWN,
                                                                                               buff=0.42),
                           label(r"$\leftarrow$ \ fish", font_size=font_size, color=FISH).next_to(self.frame, UP,
                                                                                              buff=0.42),
                           label(r"coconuts \ $\rightarrow$", font_size=font_size, color=COCO).rotate(PI / 2).next_to(
                               self.frame, LEFT, buff=0.5),
                           label(r"$\leftarrow$ \ coconuts", font_size=font_size, color=COCO).rotate(PI / 2).next_to(
                               self.frame, RIGHT, buff=0.5))
            self.add(self.names)

    def c2p(self, x, y):
        return self.origin + RIGHT * self.w * float(x) / self.X[0] + UP * self.h * float(y) / self.X[1]

    def clip(self, xs, ys):
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        ok = (xs >= 0) & (xs <= self.X[0]) & (ys >= 0) & (ys <= self.X[1])
        return xs[ok], ys[ok]

    def curve(self, xs, ys, color=WHITE, width=3.0):
        xs, ys = self.clip(xs, ys)
        return path(self, xs, ys, color=color, width=width)


def box_from(b: dict, center=ORIGIN, width=6.0, height=5.4, **kw) -> Box:
    return Box(b["X"], center=center, width=width, height=height, **kw)


def lens_region(box: Box, b: dict, color=LENS, opacity=0.22) -> VMobject:
    """The lens between Ana's and Bo's indifference curves through the endowment."""
    xs = np.asarray(b["xs"])
    ia, ib = np.asarray(b["ia"]), np.asarray(b["ib"])
    ok = ia < ib
    xs, ia, ib = xs[ok], ia[ok], ib[ok]
    pts = [box.c2p(x, y) for x, y in zip(xs, ia)] + [box.c2p(x, y) for x, y in zip(xs[::-1], ib[::-1])]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def price_line(box: Box, through, p: float, color=PRICE, width=2.5, dashed=False):
    """The budget line with slope -p (coconuts per fish) through Ana's bundle ``through``, clipped to the box."""
    x0, y0 = through
    X = box.X
    pts = []
    for x in np.linspace(0, X[0], 400):
        y = y0 - p * (x - x0)
        if 0 <= y <= X[1]:
            pts.append(box.c2p(x, y))
    cls = DashedLine if dashed else Line
    return cls(pts[0], pts[-1], color=color, stroke_width=width)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def signed(x: float, digits: int = 2) -> str:
    v = round(x, digits)
    if v == 0:
        return f"{0.0:.{digits}f}"
    return ("$+$" if v > 0 else "$-$") + f"{abs(v):.{digits}f}"


def parcel(width: float = 2.2) -> VGroup:
    """A Red Cross food parcel: a box with a red cross, its lid open."""
    body = Rectangle(width=width, height=width * 0.55, stroke_color="#C8B79A", stroke_width=2.5, fill_color="#8C7A5B",
                     fill_opacity=0.85)
    lid = Polygon(body.get_corner(UL), body.get_corner(UR), body.get_corner(UR) + UP * 0.25 + LEFT * 0.15,
                  body.get_corner(UL) + UP * 0.25 + RIGHT * 0.15, stroke_color="#C8B79A", stroke_width=2,
                  fill_color="#A08C68", fill_opacity=0.9)
    s = width * 0.13
    cross = VGroup(Rectangle(width=s * 3, height=s, stroke_width=0, fill_color="#D64545", fill_opacity=1),
                   Rectangle(width=s, height=s * 3, stroke_width=0, fill_color="#D64545", fill_opacity=1)
                   ).move_to(body.get_center())
    return VGroup(body, lid, cross)


def cigarette(length: float = 0.55) -> VGroup:
    paper = RoundedRectangle(width=length, height=length * 0.16, corner_radius=length * 0.07, stroke_width=0,
                             fill_color="#F2EEE6", fill_opacity=1)
    tip = Rectangle(width=length * 0.28, height=length * 0.16, stroke_width=0, fill_color="#D9A25F",
                    fill_opacity=1).align_to(paper, LEFT)
    return VGroup(paper, tip)


def tin(label_text: str, color="#9AA5B1", width: float = 0.8, font_size=15) -> VGroup:
    can = RoundedRectangle(width=width, height=width * 0.9, corner_radius=0.06, stroke_color=GREY_B, stroke_width=1.5,
                           fill_color=color, fill_opacity=0.85)
    band = Rectangle(width=width, height=width * 0.32, stroke_width=0, fill_color=WHITE, fill_opacity=0.85
                     ).move_to(can.get_center())
    t = label(label_text, font_size=font_size, color=BLACK).move_to(band.get_center())
    if t.width > width * 0.92:
        t.scale_to_fit_width(width * 0.92)
    return VGroup(can, band, t)
