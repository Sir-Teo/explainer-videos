"""Helpers shared by the scenes of Part 10 ("Parallel Machines")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs9.common import size_label  # noqa: F401

from .compute import load  # noqa: F401

PART = 10

DATA = C.CS_DATA
CTRL = C.CS_CONTROL
HEAD = C.CS_HEAD
CODE = C.CS_CODE
FUNC = C.CS_FUNC
COST = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
LIMIT = C.CS_LIMIT
INF = C.CS_INF
CLOCK = C.CS_CLOCK
HIST = C.HUMAN
BG = "#121722"

# MESI states: Modified (dirty, the only copy), Exclusive (clean, the only copy), Shared, Invalid
STATE_COLOR = {"M": NO, "E": CTRL, "S": DATA, "I": GREY_D}
STATE_NAME = {"M": "Modified", "E": "Exclusive", "S": "Shared", "I": "Invalid"}
CORE_COLORS = [DATA, CTRL, YES, FUNC]


def core_box(k: int, w=1.6, h=0.9, color=None, font_size=22):
    """A processor core: a rounded box with its name."""
    c = color or CORE_COLORS[k % 4]
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=c, stroke_width=2.4, fill_color=BG,
                         fill_opacity=1)
    t = label(rf"core {k}", font_size=font_size, color=c).move_to(r)
    g = VGroup(r, t)
    g.box = r
    return g


class CacheLine(VGroup):
    """One line in a private cache: a state letter in a coloured cell and a value; ``set(state, value)`` returns
    the animation to a new state."""

    def __init__(self, state="I", value="", w=1.6, h=0.5, font_size=20):
        super().__init__()
        self.w, self.h, self.fs = w, h, font_size
        self.cell = Rectangle(width=w, height=h, stroke_color=STATE_COLOR[state], stroke_width=2,
                              fill_color=STATE_COLOR[state], fill_opacity=0.25 if state != "I" else 0.05)
        self.letter = Text(state, font="DejaVu Sans Mono", font_size=font_size, color=STATE_COLOR[state],
                           weight=BOLD).move_to(self.cell.get_left() + RIGHT * 0.25)
        self.val = Text(value or ".", font="DejaVu Sans Mono", font_size=font_size - 2, color=WHITE).move_to(
            self.cell.get_center() + RIGHT * 0.25)
        if not value:
            self.val.set_opacity(0)
        self.add(self.cell, self.letter, self.val)
        self.state, self.value = state, value

    def make(self, state, value=None):
        new = CacheLine(state, value if value is not None else self.value, self.w, self.h, self.fs)
        new.move_to(self)
        return new

    def set(self, state, value=None):
        new = self.make(state, value)
        anims = [Transform(self.cell, new.cell), Transform(self.letter, new.letter), Transform(self.val, new.val)]
        self.state, self.value = state, new.value
        return anims


def timeline(ops, color, x0, y0, dx=1.6, font_size=20):
    """A thread's program as a row of boxes (one per operation), left to right."""
    g = VGroup()
    for k, op in enumerate(ops):
        b = RoundedRectangle(width=dx - 0.15, height=0.55, corner_radius=0.08, stroke_color=color, stroke_width=2,
                             fill_color=BG, fill_opacity=1).move_to([x0 + k * dx, y0, 0])
        t = Text(op, font="DejaVu Sans Mono", font_size=font_size, color=WHITE).move_to(b)
        if t.width > b.width - 0.1:
            t.width = b.width - 0.1
        g.add(VGroup(b, t))
    return g


def wire_diagram(n, layers, x0=-5.0, y0=2.2, dy=0.55, dx=0.55, color=GREY_B, comp_color=DATA, gap=0.35):
    """A sorting network: ``n`` horizontal wires, comparators as vertical bars with dots, layer by layer.
    Returns a VGroup with ``.wires``, ``.comps`` (a VGroup per layer) and ``.x(layer)``."""
    g = VGroup()
    total = sum(len(_sublayers(l)) for l in layers)
    width = total * dx + (len(layers) + 1) * gap
    g.wires = VGroup(*[Line([x0, y0 - i * dy, 0], [x0 + width, y0 - i * dy, 0], color=color, stroke_width=2)
                       for i in range(n)])
    g.comps = VGroup()
    x = x0 + gap
    for l in layers:
        grp = VGroup()
        for sub in _sublayers(l):
            x += dx / 2
            for i, j in sub:
                a, b = [x, y0 - i * dy, 0], [x, y0 - j * dy, 0]
                grp.add(VGroup(Line(a, b, color=comp_color, stroke_width=3), Dot(a, radius=0.07, color=comp_color),
                               Dot(b, radius=0.07, color=comp_color)))
            x += dx / 2
        x += gap
        g.comps.add(grp)
    g.add(g.wires, g.comps)
    return g


def _sublayers(layer):
    """Comparators of one layer that overlap visually are drawn side by side."""
    subs = []
    for i, j in sorted(layer, key=lambda c: c[1] - c[0]):
        for s in subs:
            if all(j < a or i > b for a, b in s):
                s.append((i, j))
                break
        else:
            subs.append([(i, j)])
    return subs
