"""What every part's scenes share, from Part 2 on (Part 1 keeps its own copies in ``econ1/common.py``).

    from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis

* :func:`chapter`: the narrated chapter card, then a clean frame (``chapter(scene, PART, ASK, 3, title, ...)``);
* :func:`dollars`, :func:`pct`: numbers for the screen (TeX); :func:`money_words`, :func:`say_pct`: the same numbers
  for the narrator, written as they are spoken;
* :func:`year_axis`: axes for a time series, optionally on a log scale.
"""

from __future__ import annotations

from manim import ORIGIN

from explainer.ai.viz import axes
from explainer.economics import chapter_card


def chapter(scene, part: int, ask: str, n: int, title: str, question: str, say: str, lit=(), scale=("market",),
            horizon=("a year",), hold: float = 0.0):
    """The chapter card, narrated by ``say``, held ``hold`` seconds more, then cleared."""
    from manim import UP, FadeIn

    c = chapter_card(n, title, question, lit=lit, part=part, scale=scale, horizon=horizon, ask=ask)
    with scene.voiceover(say):
        scene.play(FadeIn(c, shift=UP * 0.2))
    if hold:
        scene.wait(hold)
    scene.clear_scene()


def dollars(x: float, digits: int = 2) -> str:
    """$2.25 for the screen (TeX)."""
    return rf"\${x:,.{digits}f}".replace(",", "{,}")


def pct(x: float, digits: int = 1, sign: bool = False) -> str:
    """0.255 -> 25.5\\% for the screen."""
    s = f"{100 * x:+.{digits}f}" if sign else f"{100 * x:.{digits}f}"
    return s.replace("-", "{-}") + r"\%"


def say_pct(x: float, digits: int = 1) -> str:
    """A share as words for the narrator: 0.0255 -> '2.6 percent', -0.026 -> 'minus 2.6 percent'."""
    v = round(100 * x, digits)
    s = f"{abs(v):.{digits}f}".rstrip("0").rstrip(".") if digits else f"{abs(v):.0f}"
    return ("minus " if v < 0 else "") + f"{s} percent"


def say_num(x: float, digits: int = 2) -> str:
    """A signed number for the narrator: -0.82 -> 'minus 0.82' (a bare hyphen can be dropped by the voice)."""
    return ("minus " if x < 0 else "") + f"{abs(x):.{digits}f}"


def money_words(x: float) -> str:
    """$2.21 -> '2 dollars 21'; $3.00 -> '3 dollars'; $0.40 -> '40 cents' (for the narrator)."""
    d = int(x)
    c = int(round((x - d) * 100))
    if c == 100:
        d, c = d + 1, 0
    if d == 0:
        return f"{c} cents"
    return f"{d} dollar{'s' if d != 1 else ''}" + (f" {c:02d}" if c else "")


def year_axis(x_range, y_range, x_length=11.0, y_length=4.8, xticks=None, yticks=None, xlabel="", ylabel="",
              log_y=False, yfmt=None, center=ORIGIN, font_size=20):
    """Axes for a time series.  ``log_y``: y_range and yticks in log10 units, labelled as numbers."""
    fmt = yfmt
    if log_y and fmt is None:
        def fmt(v):
            x = 10 ** v
            return f"{x:,.0f}".replace(",", "{,}") if x >= 1 else f"{x:g}"
    return axes(list(x_range), list(y_range), x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel,
                xticks=xticks, yticks=yticks, xfmt=lambda v: f"{v:.0f}", yfmt=fmt, center=center,
                font_size=font_size)
