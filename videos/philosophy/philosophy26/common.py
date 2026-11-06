"""Helpers shared by the scenes of Part 26 ("The Quantum Puzzle")."""

from __future__ import annotations

import math  # noqa: F401

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import quantum as Q  # noqa: F401

from .compute import load  # noqa: F401

PART = 26
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
WAVE = "#6FB7FF"      # wavefunctions, amplitudes
ALICE = "#F2A65A"     # Alice, the first party, outcomes
BOB = "#F28EC2"       # Bob, the second party
CLASS = "#5EE6D0"     # classical bounds, local values
ABS = "#C3A6FF"       # formal machinery
PART_C = "#F2C14E"    # particles, detections
SPACE, MATTER, CURVE, TIME, LIGHT = WAVE, ALICE, BOB, CLASS, PART_C
LAW, CHANCE, ENT, DATA = WAVE, ALICE, BOB, PART_C


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            if m.width > 1.15 * width:  # break a long row into lines rather than shrink it out of legibility
                m = wrapped_label(t, width, font_size, c)
            else:
                m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)


def rows_table(rows, x_label=-6.4, x_text=-3.2, top=1.7, gap=0.42, label_size=22, text_size=21, width=9.6):
    g = VGroup()
    for a, b, c in rows:
        x = label(a, font_size=label_size, color=c)
        y = wrapped_label(b, width, text_size, WHITE)
        x.move_to([x_label + x.width / 2, top - x.height / 2, 0])
        y.move_to([x_text + y.width / 2, top - y.height / 2, 0])
        g.add(VGroup(x, y))
        top -= max(x.height, y.height) + gap
    return g


def series_plot(ax, ys, color, xs=None, width=3) -> VMobject:
    xs = xs if xs is not None else list(range(len(ys)))
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if y is not None]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


def fold(u, lo, hi):
    """Free motion in [lo, hi] with elastic walls: unfold the straight line and fold it back into the box."""
    span = hi - lo
    m = np.mod(u - lo, 2 * span)
    return lo + np.where(m < span, m, 2 * span - m)


def gas(n=40, box=(-3.0, 3.0, -2.0, 2.0), corner=0.22, seed=24, speed=1.0):
    """Initial positions (crowded into the lower-left corner) and velocities of a toy gas."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = box
    p = np.column_stack([x0 + (x1 - x0) * corner * rng.random(n), y0 + (y1 - y0) * corner * rng.random(n)])
    a = rng.random(n) * 2 * np.pi
    s = speed * (0.6 + 0.8 * rng.random(n))
    v = np.column_stack([s * np.cos(a), s * np.sin(a)])
    return p, v


def gas_at(p, v, t, box=(-3.0, 3.0, -2.0, 2.0)):
    x0, x1, y0, y1 = box
    q = p + v * t
    return np.column_stack([fold(q[:, 0], x0, x1), fold(q[:, 1], y0, y1)])


def tf(v, size=22) -> MathTex:
    return MathTex(r"\text{T}" if v else r"\text{F}", font_size=size, color=OK if v else BAD)


def mark(v, size=24) -> MathTex:
    return MathTex(r"\checkmark" if v else r"\times", font_size=size, color=OK if v else BAD)
