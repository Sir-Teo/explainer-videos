"""Pictures of scales (Part 12 and after): a keyboard, the octave as a circle, steps as a bar, a chain of fifths.

    keyboard(lo, hi, lit)        piano keys; ``.key[n]`` is the key n semitones above C
    octave_circle(points)        notes on a circle, one octave to the turn; ``.dots``, ``.at(pos)``
    twelve(notes)                the twelve notes as a clock, with a scale's notes joined; ``.dots[n]``
    step_bar(steps)              an octave cut into its steps, each coloured by its size
    chain(names, lit)            notes a fifth apart, in a row
    vector_bars(vector)          how often each interval occurs
"""

from __future__ import annotations

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, WHITE, BLACK, Circle, Dot, Line, Polygon, Rectangle, RoundedRectangle, VGroup

from explainer.analysis import label

GREY = "#8A93A0"
DIM = "#3A424E"
GOLD = "#F5C542"
BLUE = "#7DD3FC"
RED = "#EF5350"
NOTE_NAMES = ("C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B")
_BLACK = {1, 3, 6, 8, 10}


def keyboard(lo: int = 0, hi: int = 24, width: float = 10.0, height: float = 2.0, lit=None, color=GOLD) -> VGroup:
    """Piano keys from ``lo`` to ``hi`` semitones above C (both white).  ``lit``: semitones to colour.  ``.key[n]``
    is a key; ``.light(n, color)`` colours one."""
    whites = [n for n in range(lo, hi + 1) if n % 12 not in _BLACK]
    w = width / len(whites)
    g = VGroup()
    g.key = {}
    for i, n in enumerate(whites):
        k = Rectangle(width=w, height=height, stroke_color="#30363F", stroke_width=1.5, fill_color=WHITE, fill_opacity=0.95).move_to([(i + 0.5) * w - width / 2, 0, 0])
        g.add(k)
        g.key[n] = k
    for i, n in enumerate(whites[:-1]):
        if n + 1 <= hi and (n + 1) % 12 in _BLACK:
            k = Rectangle(width=0.6 * w, height=0.62 * height, stroke_color="#30363F", stroke_width=1.0, fill_color="#14181F", fill_opacity=1.0).move_to([(i + 1) * w - width / 2, 0.19 * height, 0])
            g.add(k)
            g.key[n + 1] = k
    g.base = {n: ("#14181F" if n % 12 in _BLACK else WHITE) for n in g.key}

    def light(n, c=color):
        g.key[n].set_fill(c, opacity=1.0)
        return g.key[n]

    def clear():
        for n, k in g.key.items():
            k.set_fill(g.base[n], opacity=1.0 if n % 12 in _BLACK else 0.95)

    g.light, g.clear = light, clear
    for n in lit or ():
        if n in g.key:
            light(n)
    return g


def octave_circle(points=(), radius: float = 1.8, color=GOLD, names=None, dot: float = 0.09, font_size: int = 22) -> VGroup:
    """Notes on a circle: once round is an octave, clockwise from the top.  ``points`` are in octaves (0 to 1)."""
    g = VGroup()
    ring = Circle(radius=radius, color=DIM, stroke_width=2)
    g.add(ring)

    def at(pos, r: float = 1.0):
        a = np.pi / 2 - 2 * np.pi * float(pos)
        return ring.get_center() + radius * r * np.array([np.cos(a), np.sin(a), 0.0])

    g.at = at
    g.dots = VGroup(*[Dot(at(p), radius=dot, color=color) for p in points])
    g.add(g.dots)
    g.names = VGroup()
    if names:
        for p, nm in zip(points, names):
            g.names.add(label(nm, font_size=font_size, color=WHITE).move_to(at(p, 1.22)))
        g.add(g.names)
    g.ring, g.radius = ring, radius
    return g


def twelve(notes=(), radius: float = 1.5, color=GOLD, names: bool = True, polygon: bool = True, dot: float = 0.1, font_size: int = 20, tick=GREY) -> VGroup:
    """The twelve notes as a clock, C at the top; the notes of a scale are filled and joined."""
    g = VGroup()
    ring = Circle(radius=radius, color=DIM, stroke_width=2)
    g.add(ring)

    def at(n, r: float = 1.0):
        a = np.pi / 2 - 2 * np.pi * n / 12.0
        return ring.get_center() + radius * r * np.array([np.cos(a), np.sin(a), 0.0])

    g.at = at
    on = sorted(set(int(n) % 12 for n in notes))
    if polygon and len(on) >= 3:
        g.poly = Polygon(*[at(n) for n in on], color=color, stroke_width=2, fill_color=color, fill_opacity=0.1)
        g.add(g.poly)
    g.dots = {}
    for n in range(12):
        d = Dot(at(n), radius=dot if n in on else dot * 0.45, color=color if n in on else tick)
        g.add(d)
        g.dots[n] = d
    if names:
        g.names = VGroup(*[label(NOTE_NAMES[n], font_size=font_size, color=WHITE if n in on else GREY).move_to(at(n, 1.24)) for n in range(12)])
        g.add(g.names)
    g.ring, g.radius, g.on = ring, radius, on
    return g


def step_bar(steps, width: float = 9.0, height: float = 0.5, colors=(GOLD, BLUE, RED), show: bool = True, font_size: int = 20, fmt="{:.0f}") -> VGroup:
    """An octave as a bar cut into its steps; steps of the same size share a colour (the largest first), and each
    is labelled with its size."""
    s = np.asarray(steps, dtype=float)
    kinds = []
    for v in sorted(s, reverse=True):
        if not kinds or abs(kinds[-1] - v) > 0.01 * max(s):
            kinds.append(v)
    g = VGroup()
    g.cells = []
    x = -width / 2
    for v in s:
        w = width * v / s.sum()
        k = int(np.argmin([abs(v - q) for q in kinds]))
        r = Rectangle(width=max(w - 0.04, 0.02), height=height, stroke_width=0, fill_color=colors[min(k, len(colors) - 1)], fill_opacity=0.85).move_to([x + w / 2, 0, 0])
        cell = VGroup(r)
        if show and w > 0.42:
            cell.add(label(fmt.format(v), font_size=font_size, color=BLACK).move_to(r))
        g.add(cell)
        g.cells.append(cell)
        x += w
    g.kinds = kinds
    return g


def chain(names, lit=(), tonic: int | None = None, gap: float = 0.95, font_size: int = 30, color=GOLD) -> VGroup:
    """Notes a fifth apart, in a row, joined by short lines; those in ``lit`` are bright, ``tonic`` is ringed."""
    g = VGroup()
    g.cells = []
    for k, nm in enumerate(names):
        t = label(nm, font_size=font_size, color=color if k in lit else GREY).move_to([k * gap, 0, 0])
        cell = VGroup(t)
        if tonic == k:
            cell.add(Circle(radius=0.36, color=WHITE, stroke_width=2.5).move_to(t))
        g.add(cell)
        g.cells.append(cell)
        if k:
            g.add(Line([(k - 1) * gap + 0.3, 0, 0], [k * gap - 0.3, 0, 0], color=DIM, stroke_width=2))
    return g


def vector_bars(vector, width: float = 3.6, height: float = 1.6, color=GOLD, names=("m2", "M2", "m3", "M3", "P4", "tt"), font_size: int = 20, top: int | None = None) -> VGroup:
    """How many times each interval occurs in a scale: semitone, tone, minor third, major third, fourth (or fifth), tritone."""
    n = len(vector)
    top = top or max(max(vector), 1)
    g = VGroup()
    g.bars = []
    w = width / n
    for k, v in enumerate(vector):
        h = height * v / top
        b = Rectangle(width=0.62 * w, height=max(h, 0.02), stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([(k + 0.5) * w - width / 2, h / 2, 0])
        g.add(b, label(str(v), font_size=font_size, color=WHITE).move_to([(k + 0.5) * w - width / 2, h + 0.2, 0]),
              label(names[k], font_size=font_size - 2, color=GREY).move_to([(k + 0.5) * w - width / 2, -0.25, 0]))
        g.bars.append(b)
    return g
