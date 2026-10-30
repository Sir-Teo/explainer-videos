"""Helpers shared by the scenes of Part 4 ("Change")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import BOWL_P0, bowl, bowl_grad, lag_f, load  # noqa: F401

PART = 4
MONO = "DejaVu Sans Mono"
HIST = C.HUMAN  # history cards
VALUE, GRAD = "#58A6FF", "#FF9F45"  # values flow forward (blue), gradients flow back (orange)
HESS = C.TRUE_P   # curvature, Hessians
CONS = C.BITS     # constraints, multipliers
FWD, BWD = VALUE, GRAD


class ComputeGraph(VGroup):
    """A computation graph drawn as circles and arrows: ``nodes`` is {name: (tex, position)}, ``edges`` a list of
    (from, to).  ``pulse(edge, color)`` is a glow travelling along an edge (values forward in blue, gradients back in
    orange); ``tag(name, tex, color, direction)`` writes a value beside a node."""

    def __init__(self, nodes: dict, edges: list, radius=0.4, font_size=32, colors: dict | None = None):
        super().__init__()
        colors = colors or {}
        self.node = {}
        for name, (tex, pos) in nodes.items():
            c = Circle(radius=radius, color=colors.get(name, GREY_B), stroke_width=3, fill_color=BACKGROUND,
                       fill_opacity=1).move_to(pos)
            self.node[name] = VGroup(c, MathTex(tex, font_size=font_size).move_to(c))
        self.edge = {}
        for a, b in edges:
            pa, pb = self.node[a].get_center(), self.node[b].get_center()
            d = (pb - pa) / np.linalg.norm(pb - pa)
            self.edge[(a, b)] = Arrow(pa + d * radius, pb - d * radius, buff=0.04, color=GREY_D, stroke_width=3,
                                      max_tip_length_to_length_ratio=0.15)
        self.add(*self.edge.values(), *self.node.values())

    def pulse(self, a, b, color=VALUE, backwards=False, width=8):
        e = self.edge[(a, b)]
        line = Line(e.get_end(), e.get_start()) if backwards else Line(e.get_start(), e.get_end())
        return ShowPassingFlash(line.set_stroke(color, width=width), time_width=0.6)

    def light(self, name, color):
        return self.node[name][0].animate.set_stroke(color, width=5)


def log_axes(xr, yr, x_length=6.0, y_length=3.8, xlabel="", ylabel="", center=ORIGIN, xstep=1, ystep=1,
             font_size=20, xticks=None, yticks=None):
    """Axes over log10 ranges, with ticks labelled as powers of ten."""
    xt = xticks if xticks is not None else list(range(int(math.ceil(xr[0])), int(math.floor(xr[1])) + 1, xstep))
    yt = yticks if yticks is not None else list(range(int(math.ceil(yr[0])), int(math.floor(yr[1])) + 1, ystep))
    pw = lambda v: "1" if v == 0 else ("10" if v == 1 else f"10^{{{int(v)}}}")  # noqa: E731
    return axes(list(xr), list(yr), x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel, xticks=xt,
                yticks=yt, xfmt=pw, yfmt=pw, font_size=font_size, center=center)


def matrix_heat(M, cell=0.42, pos=C.TRUE_P, neg=C.SURPRISE, numbers=False, fmt="{:.2f}", font_size=16, vmax=None):
    """A small signed matrix as coloured cells (blue positive, red negative), optionally with its entries."""
    M = np.asarray(M, float)
    vmax = vmax or max(float(np.abs(M).max()), 1e-12)
    bg = ManimColor("#121722")
    g = VGroup()
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = float(np.clip(M[i, j] / vmax, -1, 1))
            col = interpolate_color(bg, ManimColor(pos if v >= 0 else neg), abs(v) ** 0.7)
            sq = Square(side_length=cell, stroke_width=0.6, stroke_color=GREY_D, fill_color=col, fill_opacity=1)
            sq.move_to([j * cell, -i * cell, 0])
            cellg = VGroup(sq)
            if numbers:
                cellg.add(MathTex(fmt.format(M[i, j]).replace("-", "{-}"), font_size=font_size, color=WHITE).move_to(sq))
            g.add(cellg)
    return g.move_to(ORIGIN)


def bits_bar(sign, exp, man, unit=0.12, height=0.42, name="", font_size=22):
    """A number format's bit layout: sign (red), exponent (green), mantissa (blue), one cell per bit."""
    cells = VGroup()
    for k, (n, col) in enumerate(((sign, C.SIGN_BIT), (exp, C.EXP_BIT), (man, C.MAN_BIT))):
        for _ in range(n):
            cells.add(Rectangle(width=unit, height=height, stroke_width=0.8, stroke_color=BACKGROUND, fill_color=col,
                                fill_opacity=0.9))
    cells.arrange(RIGHT, buff=0)
    g = VGroup(cells)
    if name:
        g.add(label(name, font_size=font_size, color=GREY_A).next_to(cells, LEFT, buff=0.25))
    g.cells = cells
    return g


def _me(x: float):
    e = int(math.floor(math.log10(abs(x))))
    m = int(round(abs(x) / 10 ** e))
    if m == 10:
        m, e = 1, e + 1
    return m, e


def expo(x: float) -> int:
    """For narration of a small number as 'm times ten to the minus e': the e (positive)."""
    return -_me(x)[1]


def mant(x: float) -> int:
    """... and the m, one significant digit."""
    return _me(x)[0]
