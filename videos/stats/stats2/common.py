"""Helpers shared by the scenes of Part 2 of *Statistics, Built* ("Chance, Counted")."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats.prob import Dist, coin, die, faces, shuffles  # noqa: F401

from .compute import load  # noqa: F401

PART = 2

# one meaning per colour, for this part (the series' S.TRUTH / S.EST keep theirs: an exact probability is the
# model's truth, gold; a simulated frequency is an estimate of it, blue)
EXACT = S.TRUTH
SIM = S.EST
EVENT = S.ACCENT  # the outcomes in an event
PA, PB = "#F28FB8", "#7EC8F5"  # the two players of 1654
SICK = "#F26D6D"  # has the condition
WELL = "#5C6B7A"  # does not
POS = S.ACCENT  # tested positive
CAR, GOAT = S.TRUTH, GREY_B
CELL = "#1A2230"  # an outcome cell, unlit


def frac(fr, display=False) -> str:
    """[a, b] or Fraction -> TeX fraction."""
    f = Fraction(*fr) if isinstance(fr, (list, tuple)) else Fraction(fr)
    if f.denominator == 1:
        return str(f.numerator)
    cmd = r"\dfrac" if display else r"\tfrac"
    return rf"{cmd}{{{f.numerator}}}{{{f.denominator}}}"


def fval(fr) -> float:
    f = Fraction(*fr) if isinstance(fr, (list, tuple)) else Fraction(fr)
    return float(f)


def exact_sim(exact_tex: str, exact_value: float, sim_value: float, n: int, font_size=30, digits=4) -> VGroup:
    """The part's two-line check: the exact answer (gold) above the simulated frequency (blue)."""
    top = MathTex(r"\text{exact}\quad", exact_tex, rf"= {exact_value:.{digits}f}", font_size=font_size, color=EXACT)
    bot = MathTex(rf"\text{{simulated, {fmt_int(n)} runs}}\quad {sim_value:.{digits}f}", font_size=font_size - 2,
                  color=SIM)
    return VGroup(top, bot).arrange(DOWN, aligned_edge=LEFT, buff=0.2)


def outcome_grid(size=0.62, buff=0.06, dice_size=0.22, show_dice=True) -> VGroup:
    """The 36 outcomes of two dice, first die across (1-6, left to right), second die down (1-6, top to bottom).
    ``grid.cell[(i, j)]`` is the square for first die i, second die j."""
    g = VGroup()
    cell = {}
    for j in range(1, 7):
        for i in range(1, 7):
            sq = Square(side_length=size, stroke_color=GREY_D, stroke_width=1.2, fill_color=CELL, fill_opacity=1)
            sq.move_to([(i - 3.5) * (size + buff), (3.5 - j) * (size + buff), 0])
            if show_dice:
                pair = VGroup(die_face(i, dice_size), die_face(j, dice_size)).arrange(RIGHT, buff=0.03).move_to(sq)
                c = VGroup(sq, pair)
            else:
                c = VGroup(sq)
            cell[(i, j)] = c
            g.add(c)
    g.cell = cell
    return g


def light(grid, pred, color=EVENT, opacity=0.55):
    """Animations that fill the cells of the outcomes satisfying ``pred(i, j)``."""
    return [grid.cell[k][0].animate.set_fill(color, opacity=opacity) for k in grid.cell if pred(*k)]


def door(number: int, w=1.5, h=2.4, color="#7A4E2D") -> VGroup:
    body = RoundedRectangle(width=w, height=h, corner_radius=0.08, fill_color=color, fill_opacity=1,
                            stroke_color="#C9A27E", stroke_width=2)
    knob = Dot(body.get_right() + LEFT * 0.22, radius=0.05, color="#E8C872")
    num = MathTex(str(number), font_size=48, color="#F3E6D0").move_to(body.get_center() + UP * 0.55)
    g = VGroup(body, knob, num)
    g.body, g.num = body, num
    return g


def prize(kind: str, font_size=30) -> VGroup:
    if kind == "car":
        return label(r"car", font_size=font_size, color=CAR)
    return label(r"goat", font_size=font_size, color=GOAT)


def money(v: float) -> str:
    """A whole number for narration: 13983816 -> '13,983,816'."""
    return f"{v:,.0f}"
