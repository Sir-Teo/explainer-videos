"""What every *Industry, Built* scene shares: text in the series' face, the cards, the stamps, money formatting.

    from explainer.industry.kit import *

* :func:`T` is all on-screen text (Inter, the series' face); :func:`money` and :func:`say_money` give the same amount
  for the screen and for the narrator;
* :func:`part_title` opens a film; :func:`chapter` is the narrated chapter card, with the five questions along its
  foot and the ones this chapter answers lit;
* :func:`source` and :func:`as_of` stamp a frame with where its figures come from and the date they describe; every
  frame with a market figure carries both (SYLLABUS §1, item 7).
"""

from __future__ import annotations

from manim import (DL, DOWN, DR, LEFT, ORIGIN, RIGHT, UL, UP, UR, BOLD, NORMAL, Circle, FadeIn, Line,
                   RoundedRectangle, Text, VGroup, config)

from explainer.industry import PARTS, QUESTION_SHORT, QUESTIONS, SERIES_EN, act_of
from explainer.industry.style import BACKGROUND, FONT, FONT_DISPLAY, I, REGION, REGION_NAME

config.background_color = BACKGROUND

__all__ = ["T", "TB", "money", "money_short", "say_money", "say_bn", "pct", "say_pct", "part_title", "chapter",
           "source", "as_of", "estimate_tag", "pill", "I", "REGION", "REGION_NAME", "FONT", "question_strip",
           "big_number", "caption", "PARTS"]


def T(text: str, size: float = 28, color: str = I.TEXT, weight=NORMAL, font: str = FONT, **kw) -> Text:
    """On-screen text in the series' face.  ``size`` is a font size in manim's units (body text 24-32)."""
    return Text(text, font=font, font_size=size, color=color, weight=weight, **kw)


def TB(text: str, size: float = 28, color: str = I.TEXT, **kw) -> Text:
    return T(text, size, color, weight=BOLD, **kw)


def money(x: float, digits: int = 0) -> str:
    """$1,099 / $0.11 / -$600 for the screen."""
    s = f"${abs(x):,.{digits}f}"
    return ("-" if x < 0 else "") + s


def money_short(x_bn: float, digits: int = 1) -> str:
    """$254.1bn for amounts given in billions."""
    return f"${x_bn:,.{digits}f}bn"


def say_money(x: float) -> str:
    """For the narrator: 1099 -> '1,099 dollars'; 0.11 -> '11 cents'; 3.70 -> '3 dollars 70'."""
    if abs(x) < 1:
        return f"{round(abs(x) * 100):d} cents"
    d = int(round(abs(x) * 100)) // 100
    c = int(round(abs(x) * 100)) % 100
    words = f"{d:,} dollar{'s' if d != 1 else ''}" + (f" {c:02d}" if c else "")
    return ("minus " if x < 0 else "") + words


def say_bn(x_bn: float, digits: int = 1) -> str:
    """For the narrator: 254.098 -> '254.1 billion dollars'."""
    v = f"{x_bn:,.{digits}f}".rstrip("0").rstrip(".") if digits else f"{x_bn:,.0f}"
    return f"{v} billion dollars"


def pct(x: float, digits: int = 0, sign: bool = False) -> str:
    s = f"{100 * x:+.{digits}f}" if sign else f"{100 * x:.{digits}f}"
    return s + "%"


def say_pct(x: float, digits: int = 0) -> str:
    v = round(100 * x, digits)
    s = f"{abs(v):.{digits}f}" if digits else f"{abs(v):.0f}"
    return ("minus " if v < 0 else "") + f"{s} percent"


def caption(text: str, size: float = 22, color: str = I.DIM) -> Text:
    return T(text, size, color)


def big_number(text: str, size: float = 96, color: str = I.MONEY) -> Text:
    return Text(text, font=FONT_DISPLAY, font_size=size, color=color, weight=BOLD)


def pill(text: str, color: str = I.TEXT, region: str | None = None, size: float = 20, fill: str = I.PANEL,
         pad=(0.22, 0.12), stroke: str | None = None) -> VGroup:
    """A company's name in a rounded tag, with a dot in its region's colour when ``region`` is given."""
    t = T(text, size, color)
    parts = [t]
    if region:
        d = Circle(radius=0.07 * size / 20, fill_color=REGION[region], fill_opacity=1, stroke_width=0)
        d.next_to(t, LEFT, buff=0.1)
        parts.insert(0, d)
    g = VGroup(*parts)
    box = RoundedRectangle(corner_radius=0.12, width=g.width + 2 * pad[0], height=g.height + 2 * pad[1],
                           fill_color=fill, fill_opacity=1, stroke_color=stroke or I.EDGE, stroke_width=1.2)
    box.move_to(g)
    return VGroup(box, g)


def question_strip(lit=(), size: float = 17, width: float = 12.6) -> VGroup:
    """The five questions in a row; those in ``lit`` (keys of :data:`QUESTIONS`) are lit gold."""
    cells = VGroup()
    for k, _ in QUESTIONS:
        on = k in lit
        dot = Circle(radius=0.07, fill_color=I.ACCENT if on else I.FAINT, fill_opacity=1, stroke_width=0)
        t = T(QUESTION_SHORT[k], size, I.TEXT if on else I.FAINT)
        cells.add(VGroup(dot, t).arrange(RIGHT, buff=0.12))
    cells.arrange(RIGHT, buff=0.55)
    if cells.width > width:
        cells.scale_to_fit_width(width)
    return cells


def part_title(part: int, question: str, subtitle: str = "") -> VGroup:
    """The film's title card: series, act, part number and name, and the question the part answers."""
    act = act_of(part)
    series = T(SERIES_EN.upper(), 22, I.DIM).set_opacity(0.9)
    actl = T(f"Act {act[0]} · {act[1]}", 22, I.DIM)
    top = VGroup(series, actl).arrange(RIGHT, buff=0.5)
    num = T(f"Part {part}", 34, I.ACCENT, weight=BOLD)
    name = Text(PARTS[part], font=FONT_DISPLAY, font_size=86, color=I.TEXT, weight=BOLD)
    if name.width > 12.5:
        name.scale_to_fit_width(12.5)
    rule = Line(LEFT * 3.2, RIGHT * 3.2, color=I.ACCENT, stroke_width=2)
    q = T(question, 30, I.TEXT, slant="ITALIC")
    if q.width > 12.2:
        q.scale_to_fit_width(12.2)
    g = VGroup(top, num, name, rule, q).arrange(DOWN, buff=0.36)
    if subtitle:
        g.add(T(subtitle, 22, I.DIM).next_to(g, DOWN, buff=0.3))
    return g.move_to(ORIGIN)


def chapter(scene, part: int, n: int, title: str, question: str, say: str, lit=(), hold: float = 0.0):
    """The narrated chapter card: number, title, the chapter's own question, the five questions with ``lit`` lit."""
    corner = T(f"Part {part} · {PARTS[part]}", 18, I.FAINT).to_corner(UL, buff=0.35)
    num = T(f"Chapter {n}" if isinstance(n, int) else str(n), 28, I.ACCENT, weight=BOLD)
    ttl = Text(title, font=FONT_DISPLAY, font_size=66, color=I.TEXT, weight=BOLD)
    if ttl.width > 12.4:
        ttl.scale_to_fit_width(12.4)
    q = T(question, 28, I.DIM, slant="ITALIC")
    if q.width > 12.0:
        q.scale_to_fit_width(12.0)
    body = VGroup(num, ttl, q).arrange(DOWN, buff=0.38).move_to(UP * 0.35)
    strip = question_strip(lit).to_edge(DOWN, buff=0.55)
    card = VGroup(corner, body, strip)
    with scene.voiceover(say):
        scene.play(FadeIn(card, shift=UP * 0.15))
    if hold:
        scene.wait(hold)
    scene.clear_scene()


def source(text: str, corner=DL, size: float = 15) -> Text:
    """Where the figures on screen come from, small and grey, in a corner."""
    t = T("Source: " + text if not text.lower().startswith(("source", "computed", "estimate", "illustrative"))
          else text, size, I.FAINT)
    if t.width > 9.0:
        t.scale_to_fit_width(9.0)
    return t.to_corner(corner, buff=0.28)


def as_of(text: str, corner=UR, size: float = 16) -> VGroup:
    """The date the figures describe, as a small boxed stamp."""
    t = T(text, size, I.ACCENT)
    box = RoundedRectangle(corner_radius=0.08, width=t.width + 0.3, height=t.height + 0.18, stroke_color=I.ACCENT,
                           stroke_width=1, fill_opacity=0)
    box.move_to(t)
    return VGroup(box, t).to_corner(corner, buff=0.28)


def estimate_tag(text: str = "estimate: this film's model, with its range", corner=DR, size: float = 15) -> Text:
    return T(text, size, I.CHANNEL).to_corner(corner, buff=0.28)
