"""Helpers shared by the scenes of Part 56 of *Economics, Built* ("The Core Exam"): the chapter card, axes, curves
and colours, and the exam's own furniture: the question paper, the pause, derivation rows with their margin reasons,
and the card of the mistakes that cost marks."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import exam  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, TRUTH, film_time, load  # noqa: F401

PART = 56
ASK = r"Can you do it with the book closed?"

HOLD = E.MISS              # caveats
GAIN = "#7BD88F"
LOSS = "#F25F5C"
TRUTHC = "#FFFFFF"         # the planted truth
EST = "#F2C14E"            # estimates
DATA = "#7EC8F5"           # data
MODEL = "#C9A0FF"          # models
THEORY = "#7FD1B9"         # formulas
OUT = "#7EC8F5"            # output
INFL = "#F2A65A"           # inflation and prices
RATE = "#E8A0B4"           # the policy rate
SUPPLY = "#7FD1B9"
DEMAND = "#F2C14E"
MONEY = "#E8A0B4"
ERR = "#F25F5C"
GRID = "#9AA3B2"
RECESS = "#3A3F4B"
CHIP = ("#7FD1B9", "#F2C14E", "#E8A0B4", "#C9A0FF")
MICRO, MACRO, METRICS = "#7EC8F5", "#F2A65A", "#C9A0FF"
FIELD = {"micro": MICRO, "macro": MACRO, "metrics": METRICS}
PAPER = "#10151F"


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


def exam_paper(number: int, field: str, title: str, lines, marks: int = 25, width: float = 12.2,
               font_size: int = 22) -> VGroup:
    """A question as it appears on the paper: a header (question number, field, marks), the statement and its
    lettered parts.  ``lines`` are Tex strings; parts start with (a), (b), ...  Returns the card with ``.head``,
    ``.rows`` and ``.box``."""
    col = FIELD[field]
    head = VGroup(label(rf"Question {number}", font_size=font_size + 4, color=col),
                  label(rf"{field.capitalize() if field != 'metrics' else 'Econometrics'} \ $\cdot$ \ {title}",
                        font_size=font_size, color=GREY_A),
                  label(rf"{marks} marks", font_size=font_size - 2, color=GREY_B)).arrange(RIGHT, buff=0.5)
    rows = VGroup(*[wrapped_label(t, width - 0.8, font_size, WHITE) for t in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.22)
    body = VGroup(head, Line(LEFT, RIGHT, color=col, stroke_width=1.5).set_width(width - 0.6), rows).arrange(
        DOWN, aligned_edge=LEFT, buff=0.25)
    head.align_to(body, LEFT)
    box = RoundedRectangle(width=width, height=body.height + 0.6, corner_radius=0.15, stroke_color=col,
                           stroke_width=2, fill_color=PAPER, fill_opacity=0.96)
    body.move_to(box)
    g = VGroup(box, body)
    if g.height > 6.8:
        g.scale_to_fit_height(6.8)
    g.head, g.rows, g.box = head, rows, box
    return g


def pause(scene, seconds: float = 8.0, where=DOWN * 3.3, text=r"pause, \ and try it"):
    """The exam's Play it: a ring that empties while the viewer works."""
    ring = countdown().scale(0.55).move_to(where + RIGHT * 1.2)
    msg = label(text, font_size=22, color=E.ACCENT).next_to(ring, LEFT, buff=0.3)
    scene.play(FadeIn(ring), FadeIn(msg))
    scene.add(ring[1])
    scene.play(ring.t.animate.set_value(0.0), run_time=seconds, rate_func=linear)
    scene.play(FadeOut(ring), FadeOut(msg))


def steps(rows, math_size: int = 30, reason_size: int = 18, buff: float = 0.32, reason_x: float = 3.4,
          left_x: float = -6.4, width: float = 9.6) -> VGroup:
    """Derivation rows: each is (math, reason[, color]); the math (MathTex) on the left, the margin reason in grey
    at a fixed column on the right.  Returns a VGroup of rows, each VGroup(math, reason)."""
    g = VGroup()
    for r in rows:
        math, why = r[0], r[1]
        col = r[2] if len(r) > 2 else WHITE
        m = MathTex(math, font_size=math_size, color=col)
        if m.width > width:
            m.width = width
        w = wrapped_label(why, 6.9 - reason_x, reason_size, GREY_B)
        g.add(VGroup(m, w))
    g.arrange(DOWN, buff=buff)
    for row in g:
        row[0].align_to(np.array([left_x, 0, 0]), LEFT)
        row[1].move_to([reason_x + row[1].width / 2, row[0].get_center()[1], 0])
    return g


def marks_card(items, title=r"where marks are lost", width: float = 12.4, font_size: int = 21) -> VGroup:
    """The mistakes that cost marks: a red-ruled card with one line per mistake."""
    head = label(title, font_size=font_size + 6, color=ERR)
    rows = VGroup()
    for t in items:
        x = label(r"$\times$", font_size=font_size + 2, color=ERR)
        w = wrapped_label(t, width - 1.4, font_size, WHITE)
        rows.add(VGroup(x, w).arrange(RIGHT, buff=0.25, aligned_edge=UP))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    box = RoundedRectangle(width=width, height=body.height + 0.6, corner_radius=0.15, stroke_color=ERR,
                           stroke_width=2, fill_color=PAPER, fill_opacity=0.96)
    body.move_to(box)
    g = VGroup(box, body)
    g.head, g.rows, g.box = head, rows, box
    return g


def answer_box(mob, color=GAIN, buff: float = 0.15) -> SurroundingRectangle:
    """The box a grader looks for around the final answer."""
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=2.5, corner_radius=0.08)



def part_tag(n: int, letter: str, field: str) -> Tex:
    """A small reminder in the corner of which question and part is being solved."""
    return label(rf"Question {n}\,({letter})", font_size=22, color=FIELD[field]).to_corner(UL, buff=0.35)


def say_tex(x: float, digits: int = 2) -> str:
    """A number for on-screen math (inside $...$ or MathTex, where a minus sign is a minus)."""
    return f"{x:.{digits}f}"
