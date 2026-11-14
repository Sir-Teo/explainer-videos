"""Pictures of rhythm (Part 11 and after): grids of pulses, necklaces, rows of ticks, stick notation.

    dot_grid(weights)           a metre as Lerdahl and Jackendoff draw it: a dot for every level on which a pulse is a beat
    pattern_row(pattern, xs)    a rhythm as a row of cells over a grid: filled where a note starts
    necklace(n, onsets)         a cycle as a circle of n pulses, with a hand that a sound can turn
    ticks(times, ...)           moments on a line of time, with a playhead
    sticks(parts)               the beat cut in parts, in stems and beams
    flash(snd, marks, times)    lights a mark at each time
"""

from __future__ import annotations

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, WHITE, Circle, Dot, Line, Polygon, RoundedRectangle, Square, VGroup, interpolate_color
from manim.utils.color import ManimColor

from explainer.analysis import label

GREY = "#8A93A0"
DIM = "#3A424E"
GOLD = "#F5C542"


def dot_grid(weights, width: float = 10.0, row: float = 0.26, radius: float = 0.06, color=GREY, strong=GOLD, top: int | None = None) -> VGroup:
    """Columns of dots: column i has ``weights[i]`` dots.  ``.cols[i]`` is a column, ``.xs[i]`` its x, and the
    columns with the most dots (``top`` or more, by default the maximum) are drawn in ``strong``."""
    n = len(weights)
    xs = np.linspace(-width / 2, width / 2, n, endpoint=False) + width / (2 * n)
    most = max(weights) if top is None else top
    g = VGroup()
    g.cols, g.xs = [], list(xs)
    for x, w in zip(xs, weights):
        col = VGroup(*[Dot([x, k * row, 0], radius=radius, color=strong if w >= most else color) for k in range(w)])
        g.add(col)
        g.cols.append(col)
    g.pitch = width / n
    return g


def pattern_row(pattern: str, xs, y: float = 0.0, size: float = 0.34, color=GOLD, empty=DIM) -> VGroup:
    """A rhythm over the columns of a grid: a filled cell where a note starts, an outline where it does not."""
    p = pattern.replace(" ", "")
    g = VGroup()
    g.cells, g.notes = [], []
    for x, c in zip(xs, p):
        on = c not in ".-"
        cell = Square(side_length=size, stroke_color=color if on else empty, stroke_width=2, fill_color=color, fill_opacity=0.9 if on else 0.0).move_to([x, y, 0])
        g.add(cell)
        g.cells.append(cell)
        if on:
            g.notes.append(cell)
    return g


def necklace(n: int, onsets=(), radius: float = 1.4, color=GOLD, tick=GREY, polygon: bool = True, dot: float = 0.1, start: float = np.pi / 2) -> VGroup:
    """A cycle of ``n`` pulses on a circle, clockwise from the top; the pulses in ``onsets`` are notes, joined by a
    polygon.  ``.hand`` is a line from the centre to the top; ``.turn(period, t0)`` gives a function for
    ``snd.drive`` that turns it once every ``period`` seconds.  ``.at(i)`` is the place of pulse i."""
    g = VGroup()
    ring = Circle(radius=radius, color=DIM, stroke_width=2)
    g.add(ring)

    def at(i):
        a = start - 2 * np.pi * i / n
        return ring.get_center() + radius * np.array([np.cos(a), np.sin(a), 0.0])

    g.at = at
    g.ticks = VGroup(*[Dot(at(i), radius=dot * 0.4, color=tick) for i in range(n)])
    g.add(g.ticks)
    pts = [at(i) for i in onsets]
    if polygon and len(pts) >= 3:
        g.poly = Polygon(*pts, color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.08)
        g.add(g.poly)
    elif polygon and len(pts) == 2:
        g.poly = Line(pts[0], pts[1], color=color, stroke_width=2.5)
        g.add(g.poly)
    g.dots = VGroup(*[Dot(p, radius=dot, color=color) for p in pts])
    g.add(g.dots)
    g.hand = Line(ring.get_center(), ring.get_center() + UP * radius * 0.92, color=WHITE, stroke_width=3)
    g.add(g.hand)
    g.ring, g.radius, g.n = ring, radius, n

    def turn(period: float, t0: float = 0.0, t1: float | None = None):
        def fn(m, t):
            u = (min(t, t1) if t1 is not None else t) - t0
            a = start - 2 * np.pi * max(u, 0.0) / period
            c = ring.get_center()
            return m.put_start_and_end_on(c, c + radius * 0.92 * np.array([np.cos(a), np.sin(a), 0.0]))
        return fn

    g.turn = turn
    return g


def ticks(times, t0: float, t1: float, width: float = 10.0, height: float = 0.5, color=GOLD, stroke_width: float = 3.0, levels=None) -> VGroup:
    """Marks on a line of time from ``t0`` to ``t1``.  ``.x_of(t)`` maps a time to an x; ``.marks`` are the marks;
    ``.head()`` is a playhead and ``.run(t_start)`` drives it.  ``levels`` (0..1 per mark) scales the marks."""
    g = VGroup()
    base = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=DIM, stroke_width=2)
    g.add(base)
    g.base = base

    def x_of(t):
        return base.get_left()[0] + base.width * (t - t0) / (t1 - t0)

    g.x_of = x_of
    g.marks = []
    for k, t in enumerate(times):
        h = height * (1.0 if levels is None else levels[k])
        m = Line([x_of(t), 0, 0], [x_of(t), h, 0], color=color, stroke_width=stroke_width)
        g.add(m)
        g.marks.append(m)

    def head(color=WHITE, extra: float = 0.15):
        return Line([base.get_left()[0], base.get_y() - extra, 0], [base.get_left()[0], base.get_y() + height + extra, 0], color=color, stroke_width=2.5)

    def run(start: float = 0.0, speed: float = 1.0):
        return lambda m, t: m.set_x(base.get_left()[0] + base.width * float(np.clip((start + speed * t - t0) / (t1 - t0), 0.0, 1.0)))

    g.head, g.run = head, run
    return g


def sticks(parts: int, width: float = 1.6, height: float = 0.8, color=WHITE, tuplet: bool | None = None) -> VGroup:
    """One beat cut into ``parts`` equal notes, in stems and beams (no heads: only the rhythm).  Two or three parts
    get one beam, four get two; three parts (or ``tuplet``) get a small 3."""
    g = VGroup()
    xs = np.linspace(-width / 2, width / 2, parts, endpoint=False) + (width / (2 * parts) if parts == 1 else 0.0)
    for x in xs:
        g.add(Line([x, 0, 0], [x, height, 0], color=color, stroke_width=4), Dot([x - 0.09, 0.02, 0], radius=0.11, color=color))
    if parts > 1:
        g.add(Line([xs[0], height, 0], [xs[-1], height, 0], color=color, stroke_width=8))
    if parts >= 4:
        g.add(Line([xs[0], height - 0.16, 0], [xs[-1], height - 0.16, 0], color=color, stroke_width=8))
    if tuplet or (tuplet is None and parts == 3):
        g.add(label("3", font_size=24, color=color).move_to([(xs[0] + xs[-1]) / 2, height + 0.28, 0]))
    g.xs = list(xs)
    return g


def flash(snd, marks, times, hot=GOLD, base=GREY, fade: float = 0.25, hold: float | None = None):
    """Light each mark at its time, fading back; if two marks share a mobject the later time wins.  The first mark
    carries the updater for all."""
    marks, times = list(marks), [float(t) for t in times]
    hot_c, base_c = ManimColor(hot), ManimColor(base)

    def fn(_, t):
        for m, t0 in zip(marks, times):
            dt = t - t0
            if dt < 0:
                continue
            w = float(np.exp(-dt / fade)) if hold is None or dt > hold else 1.0
            m.set_color(interpolate_color(base_c, hot_c, w))

    for m in marks:
        m.set_color(base_c)
    snd.drive(marks[0], fn)
    return marks
