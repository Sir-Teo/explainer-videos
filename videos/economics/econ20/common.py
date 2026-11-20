"""Helpers shared by the scenes of Part 20 of *Economics, Built* ("Growth I: Capital"): the chapter card, axes, curves
and colours."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import growth as gr  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 20
ASK = r"Can a country save its way to being rich?"

ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color
CRUSOE = island.CAST["crusoe"].color
DARA = island.CAST["dara"].color
FRIDAY = island.CAST["friday"].color
HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer
OUTPUT = "#7EC8F5"         # output, income per head
CAPITAL = "#F2C14E"        # capital
SAVE = "#F29E8E"           # saving, investment
BREAK = "#C9A0FF"          # break-even investment, depreciation
CONS = "#7BD88F"           # consumption
LABOUR = "#F2788F"         # labour, hours
HUMAN = "#9FB8F2"          # human capital, schooling
TFP = "#E8A0B4"            # the residual, TFP
RATE = "#7FD1B9"           # returns, interest rates
SOUTH = "#7EC8F5"          # South Korea
NORTH = "#F25F5C"          # North Korea
COUNTRY = {"USA": (r"United States", "#9FB8F2"), "GBR": (r"Britain", "#7EC8F5"), "JPN": (r"Japan", "#C9A0FF"),
           "KOR": (r"South Korea", "#F7D154"), "CHN": (r"China", "#F25F5C"), "IND": (r"India", "#F29E8E"),
           "BRA": (r"Brazil", "#7BD88F"), "NGA": (r"Nigeria", "#7FD1B9"), "SGP": (r"Singapore", "#E8A0B4"),
           "HKG": (r"Hong Kong", "#F2C14E"), "TWN": (r"Taiwan", "#9FE2BF"), "BWA": (r"Botswana", "#D4A373"),
           "DEU": (r"Germany", "#B8C0CC"), "ETH": (r"Ethiopia", "#E07A5F")}


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("nation",), horizon=("decades",),
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


def seg(ax, x0, y0, x1, y1, color=WHITE, width=3.0, dashed=False):
    a = ax.ax
    cls = DashedLine if dashed else Line
    return cls(a.c2p(x0, y0), a.c2p(x1, y1), color=color, stroke_width=width)


def dot(ax, x, y, color=WHITE, r=0.07):
    return Dot(ax.ax.c2p(x, y), radius=r, color=color)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def fmt(v, nd=1) -> str:
    v = float(v)
    return f"{v:.0f}" if abs(v - round(v)) < 1e-9 else f"{v:.{nd}f}"


def commas(v) -> str:
    """12345 -> '12{,}345' for TeX."""
    return f"{v:,.0f}".replace(",", "{,}")


def ordinal(n: int) -> str:
    """4 -> '4th', 43 -> '43rd', 111 -> '111th'."""
    n = int(n)
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def log_path(ax, xs, ys, color, width=3.0):
    """A curve on axes whose y range is in log10 units."""
    return path(ax, xs, [np.log10(v) if v and v > 0 else np.nan for v in ys], color=color, width=width, smooth=False)


def pc(v, nd=1) -> str:
    """0.0123 -> '1.2\\%' for TeX."""
    return f"{100 * v:.{nd}f}\\%"
