"""Helpers shared by the scenes of Part 23 ("God and the Philosophers")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import theism as Th  # noqa: F401

from .compute import load  # noqa: F401

PART = 23
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
DIV = "#F2C14E"       # God, the divine attributes
ARG = "#6FB7FF"       # arguments, premises, worlds
NAT = "#5EE6D0"       # nature, the world, evidence
HUM = "#F28EC2"       # persons, believers, freedom
ABS = "#C3A6FF"       # modal and logical machinery
WARM = "#F2A65A"      # the actual, chances, wagers
WORLD, NAME = ARG, WARM


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


def island(center, w=2.2, h=1.3, name=None, color=WORLD, font_size=20, seed=0) -> VGroup:
    """A world drawn as an island: a wobbly closed curve with a soft fill, and its name above it. ``.shape`` and
    ``.name``."""
    rng = np.random.default_rng(seed)
    c = np.array(list(center) + [0.0] * (3 - len(center)), float)
    ts = np.linspace(0, 2 * PI, 9)[:-1]
    rs = 1 + 0.12 * rng.standard_normal(len(ts))
    pts = [c + np.array([w / 2 * r * np.cos(t), h / 2 * r * np.sin(t), 0]) for r, t in zip(rs, ts)]
    shape = VMobject(stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.12)
    shape.set_points_smoothly(pts + [pts[0]])
    g = VGroup(shape)
    g.shape = shape
    g.name = None
    if name:
        g.name = label(name, font_size=font_size, color=color).next_to(shape, UP, buff=0.1)
        g.add(g.name)
    return g


def person(pos, color=NAME, name=None, font_size=16, r=0.16) -> VGroup:
    """A dot with a name under it."""
    pos = np.array(list(pos) + [0.0] * (3 - len(pos)), float)
    d = Dot(pos, radius=r, color=color)
    g = VGroup(d)
    g.dot = d
    if name:
        g.add(label(name, font_size=font_size, color=color).next_to(d, DOWN, buff=0.08))
    return g


def tf(v, size=22) -> MathTex:
    return MathTex(r"\text{T}" if v else r"\text{F}", font_size=size, color=OK if v else BAD)


def mark(v, size=24) -> MathTex:
    return MathTex(r"\checkmark" if v else r"\times", font_size=size, color=OK if v else BAD)
