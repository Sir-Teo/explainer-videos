"""Pictures of chords (Part 13, *Intervals and Chords*): Euler's lattice of fifths and thirds, bars for the twelve
notes, and a chord's notes as rows of partials.

    net = Tonnetz(a=(-2, 3), b=(-1, 1))        # fifths to the right, major thirds up and to the right
    net.node[(a, b)], net.tri(a, b, "major")   # a note's disc; the triangle of a triad whose root is at (a, b)
    Tonnetz.walk(0, 0, "major", "PLPLPL")      # where the moves P, L and R carry a triangle
    note_bars(values, names)                   # twelve bars: a chord's root saliences, or a sound's chroma
"""

from __future__ import annotations

import numpy as np
from manim import DOWN, GREY, RIGHT, UP, WHITE, Circle, Line, Polygon, Rectangle, VGroup

from . import label
from .scaleviz import BLUE, GOLD

DIM = "#3A4250"
_ACC = {"♭": r"$\flat$", "♯": r"$\sharp$", "𝄫": r"$\flat\flat$", "𝄪": r"$\times$", "°": r"$^\circ$", "ø": r"$^{\varnothing}$"}


def tex(text: str) -> str:
    """A note or chord name for Tex: the accidental signs become maths."""
    for k, v in _ACC.items():
        text = text.replace(k, v)
    return text


class Tonnetz(VGroup):
    """Euler's lattice.  A step to the right is a fifth up, a step up and to the right a major third up; so a
    step up and to the left is a minor third down.  Every upward triangle is a major triad, every downward one a
    minor triad."""

    def __init__(self, a=(-2, 3), b=(-1, 1), dx: float = 1.3, names=None, font_size: int = 24, radius: float = 0.3, color=WHITE, edge=DIM, **kw):
        super().__init__(**kw)
        self.dx, self.radius = dx, radius
        self.node, self.text, self.coords = {}, {}, []
        self.edges = VGroup()
        pts = [(i, j) for j in range(b[0], b[1] + 1) for i in range(a[0], a[1] + 1)]
        have = set(pts)
        for (i, j) in pts:
            for di, dj in ((1, 0), (0, 1), (1, -1)):
                if (i + di, j + dj) in have:
                    self.edges.add(Line(self.xy(i, j), self.xy(i + di, j + dj), color=edge, stroke_width=2))
        self.add(self.edges)
        self.fills = VGroup()                               # triangles go under the discs
        self.add(self.fills)
        for (i, j) in pts:
            disc = Circle(radius=radius, stroke_color=edge, stroke_width=2, fill_color="#0B0E14", fill_opacity=1).move_to(self.xy(i, j))
            nm = names[(i, j)] if names else ""
            t = label(tex(nm), font_size=font_size, color=color).move_to(disc)
            cell = VGroup(disc, t)
            self.add(cell)
            self.node[(i, j)], self.text[(i, j)] = cell, t
            self.coords.append((i, j))

    def xy(self, i: float, j: float) -> np.ndarray:
        return np.array([self.dx * (i + 0.5 * j), self.dx * 0.866 * j, 0.0])

    def at(self, i: int, j: int) -> np.ndarray:
        """Where a note is now (after the lattice has been moved)."""
        return self.node[(i, j)].get_center()

    @staticmethod
    def corners(i: int, j: int, kind: str) -> list[tuple[int, int]]:
        """The three notes of the triad whose root is at (i, j): root, third, fifth."""
        return [(i, j), (i, j + 1), (i + 1, j)] if kind == "major" else [(i, j), (i + 1, j - 1), (i + 1, j)]

    def tri(self, i: int, j: int, kind: str = "major", color=GOLD, opacity: float = 0.45) -> Polygon:
        """A triad's triangle (not yet in the lattice: ``show`` adds it under the discs)."""
        return Polygon(*[self.at(*c) for c in self.corners(i, j, kind)], stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=opacity)

    def show(self, tri: Polygon) -> Polygon:
        self.fills.add(tri)
        return tri

    @staticmethod
    def move(i: int, j: int, kind: str, m: str) -> tuple[int, int, str]:
        """Where one of P, L, R carries the triangle of the triad rooted at (i, j): it flips over one edge."""
        if kind == "major":
            return {"P": (i, j, "minor"), "R": (i - 1, j + 1, "minor"), "L": (i, j + 1, "minor")}[m]
        return {"P": (i, j, "major"), "R": (i + 1, j - 1, "major"), "L": (i, j - 1, "major")}[m]

    @staticmethod
    def walk(i: int, j: int, kind: str, word: str) -> list[tuple[int, int, str]]:
        out = [(i, j, kind)]
        for m in word:
            out.append(Tonnetz.move(*out[-1], m))
        return out


def note_bars(values, names, width: float = 6.0, height: float = 1.8, color=GOLD, hot=(), hot_color=BLUE, fmt="{:.0f}", font_size: int = 20, top: float | None = None,
              show_values: bool = True) -> VGroup:
    """A bar for each of the twelve notes (or any row of names).  ``.bars[k]``, ``.names[k]``, ``.values[k]``."""
    v = np.asarray(values, dtype=float)
    n = len(v)
    top = top or max(float(v.max()), 1e-9)
    w = width / n
    g = VGroup(Line([-width / 2, 0, 0], [width / 2, 0, 0], color=DIM, stroke_width=2))
    g.bars, g.names, g.values = [], [], []
    for k in range(n):
        h = height * v[k] / top
        x = (k + 0.5) * w - width / 2
        b = Rectangle(width=0.62 * w, height=max(h, 0.015), stroke_width=0, fill_color=hot_color if k in hot else color, fill_opacity=0.9).move_to([x, max(h, 0.015) / 2, 0])
        nm = label(tex(names[k]), font_size=font_size, color=WHITE if k in hot else GREY).move_to([x, -0.26, 0])
        g.add(b, nm)
        g.bars.append(b)
        g.names.append(nm)
        if show_values:
            t = label(fmt.format(v[k]), font_size=font_size - 3, color=WHITE if k in hot else GREY).move_to([x, max(h, 0.015) + 0.17, 0])
            g.add(t)
            g.values.append(t)
    return g


def partial_rows(notes, names, n: int = 6, width: float = 9.0, f_lo: float = 100.0, f_hi: float = 2000.0, row: float = 0.45, colors=(GOLD, BLUE, "#EF5350", "#A3E635"),
                 font_size: int = 22, tick: float = 0.15) -> VGroup:
    """Each note's first ``n`` harmonics as ticks on a logarithmic frequency line, one row to a note: where rows
    line up, partials coincide; where ticks nearly touch, they beat.  ``.x(f)`` is a frequency's place."""
    g = VGroup()

    def x(f):
        return width * (np.log(f / f_lo) / np.log(f_hi / f_lo) - 0.5)

    g.x = x
    g.rows = []
    for k, (f0, nm) in enumerate(zip(notes, names)):
        y = -k * row
        c = colors[k % len(colors)]
        r = VGroup(Line([-width / 2, y, 0], [width / 2, y, 0], color=DIM, stroke_width=1.5), label(tex(nm), font_size=font_size, color=c).move_to([-width / 2 - 0.4, y, 0]))
        r.ticks = VGroup()
        for h in range(1, n + 1):
            f = f0 * h
            if f_lo <= f <= f_hi:
                r.ticks.add(Line([x(f), y - tick, 0], [x(f), y + tick, 0], color=c, stroke_width=max(5 - 0.3 * h, 2.5)))
        r.add(r.ticks)
        g.add(r)
        g.rows.append(r)
    return g
