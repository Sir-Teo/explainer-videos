"""Pictures of melodies (Part 14, *Melody*): a tune as bars in time and pitch, and small charts.

    r = roll(pitches, beats)          # each note a bar: left to right is time, bottom to top is pitch
    r.notes[k], r.x(beat), r.y(pitch) # a note's bar; where a moment and a pitch are (after the picture has moved)
    columns(values, labels)           # a bar chart; .bars[k]
    dots_matrix(matrix)               # a square of dots where a matrix is not zero (a tune against itself)
    heat(matrix)                      # a grid of cells shaded by value (where each degree goes)
"""

from __future__ import annotations

import numpy as np
from manim import DOWN, GREY, LEFT, RIGHT, UP, WHITE, Dot, Line, Rectangle, RoundedRectangle, Square, VGroup

from . import label
from .scaleviz import BLUE, GOLD

DIM = "#3A4250"


def roll(pitches, beats=None, width: float = 9.0, height: float = 2.4, color=GOLD, lo: float | None = None, hi: float | None = None, lines=(0, 12),
         thick: float = 0.15, phrase_ends=(), gap: float = 0.08) -> VGroup:
    """A melody as bars.  ``lines`` are pitches drawn as faint horizontal lines (the tonic and its octave)."""
    pitches = list(pitches)
    beats = [1.0] * len(pitches) if beats is None else list(beats)
    on = np.concatenate([[0.0], np.cumsum(beats)])
    total = float(on[-1])
    lo = min(pitches) - 1.0 if lo is None else lo
    hi = max(pitches) + 1.0 if hi is None else hi
    frame = Rectangle(width=width, height=height, stroke_width=0, fill_opacity=0)
    g = VGroup(frame)
    g.frame, g.lo, g.hi, g.total = frame, lo, hi, total

    def x(t):
        return frame.get_left()[0] + frame.width * float(t) / total

    def y(p):
        return frame.get_bottom()[1] + frame.height * (float(p) - lo) / (hi - lo)

    g.x, g.y = x, y
    g.guides = VGroup(*[Line([x(0), y(p), 0], [x(total), y(p), 0], color=DIM, stroke_width=1.5) for p in lines if lo <= p <= hi])
    g.add(g.guides)
    g.breaks = VGroup(*[Line([x(on[e]), y(lo), 0], [x(on[e]), y(hi), 0], color=DIM, stroke_width=1.5) for e in phrase_ends if 0 < e < len(pitches)])
    g.add(g.breaks)
    g.notes = []
    for k, p in enumerate(pitches):
        w = max(width * beats[k] / total - gap, 0.05)
        bar = RoundedRectangle(width=w, height=thick, corner_radius=min(thick, w) / 2.2, stroke_width=0, fill_color=color, fill_opacity=1.0)
        bar.move_to([x(on[k]) + w / 2 + gap / 2, y(p), 0])
        g.add(bar)
        g.notes.append(bar)
    g.onsets = on[:-1].tolist()
    return g


def columns(values, labels=None, width: float = 6.0, height: float = 2.0, color=GOLD, hot=(), hot_color=BLUE, fmt=None, font_size: int = 20, top: float | None = None,
            bar: float = 0.62, label_every: int = 1) -> VGroup:
    """A bar chart.  ``.bars[k]``, ``.labels[k]`` (``None`` where a label was left out), ``.values[k]``."""
    v = np.asarray(values, dtype=float)
    n = len(v)
    top = top or max(float(v.max()), 1e-9)
    w = width / n
    g = VGroup(Line([-width / 2, 0, 0], [width / 2, 0, 0], color=DIM, stroke_width=2))
    g.bars, g.labels, g.values = [], [], []
    for k in range(n):
        h = max(height * v[k] / top, 0.012)
        xk = (k + 0.5) * w - width / 2
        b = Rectangle(width=bar * w, height=h, stroke_width=0, fill_color=hot_color if k in hot else color, fill_opacity=0.9).move_to([xk, h / 2, 0])
        g.add(b)
        g.bars.append(b)
        if labels is not None and k % label_every == 0:
            t = label(str(labels[k]), font_size=font_size, color=WHITE if k in hot else GREY).move_to([xk, -0.26, 0])
            g.add(t)
            g.labels.append(t)
        else:
            g.labels.append(None)
        if fmt is not None:
            t = label(fmt.format(v[k]), font_size=font_size - 2, color=WHITE if k in hot else GREY).move_to([xk, h + 0.18, 0])
            g.add(t)
            g.values.append(t)
    return g


def dots_matrix(matrix, size: float = 4.0, color=GOLD, radius: float | None = None, breaks=()) -> VGroup:
    """A dot wherever ``matrix[i][j]`` is not zero; row 0 is at the top.  ``breaks``: indices to rule lines at."""
    m = np.asarray(matrix)
    n = m.shape[0]
    cell = size / n
    g = VGroup(Square(size, stroke_color=DIM, stroke_width=1.5))
    for e in breaks:
        if 0 < e < n:
            g.add(Line([-size / 2 + e * cell, -size / 2, 0], [-size / 2 + e * cell, size / 2, 0], color=DIM, stroke_width=1),
                  Line([-size / 2, size / 2 - e * cell, 0], [size / 2, size / 2 - e * cell, 0], color=DIM, stroke_width=1))
    g.dots = VGroup(*[Dot([-size / 2 + (j + 0.5) * cell, size / 2 - (i + 0.5) * cell, 0], radius=radius or 0.36 * cell, color=color)
                      for i in range(n) for j in range(n) if m[i, j]])
    g.add(g.dots)
    return g


def heat(matrix, size: float = 3.6, color=GOLD, rows=None, cols=None, font_size: int = 22, top: float | None = None) -> VGroup:
    """A grid of cells, each as bright as its value.  ``.cell[(i, j)]``."""
    m = np.asarray(matrix, dtype=float)
    n, k = m.shape
    c = size / max(n, k)
    top = top or float(m.max())
    g = VGroup()
    g.cell = {}
    for i in range(n):
        for j in range(k):
            sq = Square(c * 0.94, stroke_width=0, fill_color=color, fill_opacity=0.06 + 0.94 * min(m[i, j] / top, 1.0)).move_to([(j + 0.5) * c - k * c / 2, n * c / 2 - (i + 0.5) * c, 0])
            g.add(sq)
            g.cell[(i, j)] = sq
    if rows:
        g.add(*[label(str(r), font_size=font_size, color=GREY).move_to([-k * c / 2 - 0.28, n * c / 2 - (i + 0.5) * c, 0]) for i, r in enumerate(rows)])
    if cols:
        g.add(*[label(str(r), font_size=font_size, color=GREY).move_to([(j + 0.5) * c - k * c / 2, n * c / 2 + 0.26, 0]) for j, r in enumerate(cols)])
    return g
