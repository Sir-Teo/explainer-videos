"""Helpers shared by the scenes of Part 4 ("Arithmetic")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.gates import GATE_FILL, GATE_STROKE, ONE, WIRE, ZERO, gate, junction, wire  # noqa: F401

from .compute import load  # noqa: F401

PART = 4

DATA = C.CS_DATA  # operands, bits
CTRL = C.CS_CONTROL  # gates, control
HEAD = C.CS_HEAD  # the focus: the carry, the current digit
CODE = C.CS_CODE  # formulas as written
FUNC = C.CS_FUNC  # results
COST = C.CS_COST  # gate counts, delays
YES = C.CS_TRUE  # correct, 1
NO = C.CS_FALSE  # overflow, error, a bug
LIMIT = C.CS_LIMIT
INF = C.CS_INF
CLOCK = C.CS_CLOCK
HIST = C.HUMAN
BG = "#121722"

KIND_COLOR = {"ripple": NO, "carry-skip": LIMIT, "carry-select": CLOCK, "brent-kung": INF, "sklansky": CTRL,
              "kogge-stone": YES, "array": NO, "wallace": CTRL, "dadda": YES}


def fmt(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")


def say(n) -> str:
    return f"{int(n):,}"


def sci(x: float, digits: int = 2) -> str:
    """x as TeX scientific notation: 1.2 \\times 10^{-8}."""
    if x == 0:
        return "0"
    e = int(np.floor(np.log10(abs(x))))
    m = x / 10 ** e
    return rf"{m:.{digits - 1}f} \times 10^{{{e}}}"


def bit_cells(bits: str, cell=0.42, font_size=28, color=DATA, fill=BG, colors=None) -> VGroup:
    """A row of boxed bits, most significant on the left; ``g[i]`` is the box-and-digit of string position i."""
    g = VGroup()
    for i, b in enumerate(bits):
        col = colors[i] if colors else (color if b == "1" else GREY_B)
        box = Square(cell, stroke_color=GREY_D, stroke_width=1.5, fill_color=fill, fill_opacity=1)
        g.add(VGroup(box, MathTex(b, font_size=font_size, color=col)))
    g.arrange(RIGHT, buff=0.04)
    return g


def axis_plot(xs, ys, ax, color, width=3.0) -> VMobject:
    return VMobject(color=color, stroke_width=width).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
