"""Helpers shared by the scenes of Part 1 of *Economics, Built* ("Who Feeds Paris?")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora.market import Market  # noqa: F401

from .compute import film_time, load  # noqa: F401

PART = 1
ASK = r"Who feeds Paris?"  # the part's question, in the corner of every chapter card

# one meaning per colour, for this part (the series' E.* keep theirs)
CRUSOE = island.CAST["crusoe"].color
FRIDAY = island.CAST["friday"].color
NIGHT = "#0A0F1A"
LAMP = "#F6D58A"
WINE, CLOTH = "#B5486B", "#7FA6D9"
TIN = "#B9C3CF"
FINE = E.TREAT
REGION_COLOR = {
    "Western Europe": "#5DADEC",
    "Western Offshoots": "#7EC8F5",
    "Eastern Europe": "#B48EF0",
    "Latin America": "#F2B84B",
    "East Asia": "#F26D6D",
    "South and South East Asia": "#FF9F5A",
    "Middle East and North Africa": "#E9A3C9",
    "Sub Saharan Africa": "#7BD88F",
}
REGION_SHORT = {
    "Western Europe": r"Western Europe", "Western Offshoots": r"US, Canada, Australia, NZ",
    "Eastern Europe": r"Eastern Europe", "Latin America": r"Latin America", "East Asia": r"East Asia",
    "South and South East Asia": r"South and South-East Asia", "Middle East and North Africa": r"Middle East, N. Africa",
    "Sub Saharan Africa": r"Sub-Saharan Africa",
}


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("market",), horizon=("a year",)):
    """The chapter card, narrated, then cleared."""
    c = chapter_card(n, title, question, lit=lit, part=PART, scale=scale, horizon=horizon, ask=ASK)
    with scene.voiceover(say):
        scene.play(FadeIn(c, shift=UP * 0.2))
    scene.clear_scene()


def dollars(x: float, digits: int = 2) -> str:
    return rf"\${x:.{digits}f}"


def pct(x: float, digits: int = 1, sign: bool = False) -> str:
    s = f"{100 * x:+.{digits}f}" if sign else f"{100 * x:.{digits}f}"
    return s.replace("-", "{-}") + r"\%"


def say_pct(x: float, digits: int = 1) -> str:
    """A share as words for the narrator: 0.0255 -> '2.6 percent', -0.026 -> 'minus 2.6 percent'."""
    v = round(100 * x, digits)
    s = f"{abs(v):.{digits}f}".rstrip("0").rstrip(".") if digits else f"{abs(v):.0f}"
    return ("minus " if v < 0 else "") + f"{s} percent"


def money_words(x: float) -> str:
    """$2.21 -> '2 dollars 21' for the narrator."""
    d = int(x)
    c = int(round((x - d) * 100))
    if c == 100:
        d, c = d + 1, 0
    return f"{d} dollars" + (f" {c:02d}" if c else "")


def year_axis(x_range, y_range, x_length=11.0, y_length=4.8, xticks=None, yticks=None, xlabel="", ylabel="",
              log_y=False, yfmt=None, center=ORIGIN, font_size=20):
    """Axes for a time series.  ``log_y``: y_range and yticks in log10 units, labelled as numbers."""
    fmt = yfmt
    if log_y and fmt is None:
        def fmt(v):
            x = 10 ** v
            return f"{x:,.0f}".replace(",", "{,}")
    return axes(list(x_range), list(y_range), x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel,
                xticks=xticks, yticks=yticks, xfmt=lambda v: f"{v:.0f}", yfmt=fmt, center=center,
                font_size=font_size)
