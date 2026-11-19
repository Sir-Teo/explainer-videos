"""Helpers shared by the scenes of Part 11 of *Economics, Built* ("Games"): the chapter card, axes, and the two
pictures game theory draws over and over, the payoff matrix and the game tree."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import games as gm  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 11
ASK = r"What happens when my best choice depends on yours, and yours on mine?"

ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color
ROWC = ANA                 # the row player
COLC = BO                  # the column player
COOP = "#7BD88F"           # cooperate
DEFECT = E.MISS            # defect
EQ = E.ACCENT              # an equilibrium
HOLD = E.MISS              # caveats
LEVEL = "#C9A0FF"          # levels of thinking
US = "#7EC8F5"             # the United States' stockpile
USSR = "#F29E8E"           # the Soviet Union's, then Russia's


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("person", "market"), horizon=("a day",),
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


def fmt(v) -> str:
    v = float(v)
    return f"{v:.0f}" if abs(v - round(v)) < 1e-9 else f"{v:.2f}".rstrip("0").rstrip(".")


def matrix(A, B, rows, cols, row_name=r"Ana", col_name=r"Bo", cell_w: float = 2.0, cell_h: float = 0.95,
           font_size=26, row_color=ROWC, col_color=COLC, highlight=(), labels_size=None) -> VGroup:
    """A payoff matrix: the row player's payoff (left, in her colour) and the column player's (right, in his) in each
    cell.  ``.cells[i][j]`` is a cell's box, ``.pay[i][j]`` its two numbers; ``highlight`` cells get a gold frame
    (``.frames``)."""
    A, B = np.asarray(A, float), np.asarray(B, float)
    m, n = A.shape
    ls = labels_size or font_size - 4
    g = VGroup()
    cells, pay = [], []
    grid = VGroup()
    for i in range(m):
        crow, prow = [], []
        for j in range(n):
            box = Rectangle(width=cell_w, height=cell_h, stroke_color=GREY_C, stroke_width=1.5, fill_opacity=0)
            box.move_to(RIGHT * j * cell_w + DOWN * i * cell_h)
            a = MathTex(fmt(A[i, j]), font_size=font_size, color=row_color)
            b = MathTex(fmt(B[i, j]), font_size=font_size, color=col_color)
            c = MathTex(",", font_size=font_size, color=GREY_B)
            num = VGroup(a, c, b).arrange(RIGHT, buff=0.1, aligned_edge=DOWN).move_to(box)
            grid.add(box)
            crow.append(box)
            prow.append(num)
        cells.append(crow)
        pay.append(prow)
    g.add(grid, *[p for row in pay for p in row])
    rl = VGroup(*[label(r, font_size=ls, color=row_color).next_to(cells[i][0], LEFT, buff=0.2)
                  for i, r in enumerate(rows)])
    cl = VGroup(*[label(c, font_size=ls, color=col_color).next_to(cells[0][j], UP, buff=0.15)
                  for j, c in enumerate(cols)])
    rn = label(row_name, font_size=ls, color=row_color).next_to(rl, LEFT, buff=0.25)
    cn = label(col_name, font_size=ls, color=col_color).next_to(cl, UP, buff=0.12)
    g.add(rl, cl, rn, cn)
    frames = VGroup(*[SurroundingRectangle(cells[i][j], color=EQ, stroke_width=4, buff=0.0) for i, j in highlight])
    g.add(frames)
    g.cells, g.pay, g.frames, g.row_labels, g.col_labels = cells, pay, frames, rl, cl
    g.center()
    return g


def frame_cell(mat, i, j, color=EQ, width=4.0) -> Mobject:
    return SurroundingRectangle(mat.cells[i][j], color=color, stroke_width=width, buff=0.0)


def tree_node(pos, color=WHITE, r=0.11) -> Dot:
    return Dot(pos, radius=r, color=color)


def tree_edge(a, b, text: str = "", color=GREY_B, font_size=20, side=LEFT, width=3.0) -> VGroup:
    ln = Line(a, b, color=color, stroke_width=width)
    g = VGroup(ln)
    if text:
        g.add(label(text, font_size=font_size, color=color).next_to(ln.point_from_proportion(0.5), side, buff=0.1))
    return g


def payoff_leaf(pos, pay, colors=(ROWC, COLC), font_size=22) -> VGroup:
    a = MathTex(fmt(pay[0]), font_size=font_size, color=colors[0])
    b = MathTex(fmt(pay[1]), font_size=font_size, color=colors[1])
    return VGroup(MathTex(r"(", font_size=font_size, color=GREY_B), a, MathTex(",", font_size=font_size, color=GREY_B),
                  b, MathTex(r")", font_size=font_size, color=GREY_B)).arrange(RIGHT, buff=0.05).move_to(pos)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s
