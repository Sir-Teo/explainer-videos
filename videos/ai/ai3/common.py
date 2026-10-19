"""Helpers shared by the scenes of Part 3 ("Vectors That Mean Things").

* :func:`barcode`, a vector of hundreds of numbers drawn as a strip of colored ticks (one per coordinate);
* :func:`plane`, the 3Blue1Brown-style grid used by the linear-algebra chapters, and :func:`arrow`;
* :func:`unit_circle`, the circle whose image under a matrix is an ellipse.
"""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import CATEGORIES, VOWELS, load  # noqa: F401

MONO = "DejaVu Sans Mono"
CAT_COLORS = {"animals": "#F2A541", "colors": "#E85D75", "numbers": "#58A6FF", "places": "#5BD17A",
              "family": "#D4A5FF", "body": "#4FD1C5", "verbs": "#F7D154"}
I_COLOR, J_COLOR = "#7CE38B", "#FF6B8B"  # the two basis vectors: green for the first, red for the second


def barcode(v, width=11.0, height=0.55, vmax=None, pos="#F2A541", neg="#58A6FF") -> VGroup:
    """One thin bar per coordinate: up and warm for positive, down and cool for negative."""
    v = np.asarray(v, float)
    vmax = vmax or float(np.abs(v).max())
    n = len(v)
    w = width / n
    g = VGroup()
    for i, x in enumerate(v):
        h = max(abs(x) / vmax * height / 2, 0.004)
        r = Rectangle(width=w * 0.9, height=h, stroke_width=0, fill_color=pos if x > 0 else neg, fill_opacity=0.95)
        r.move_to([-width / 2 + (i + 0.5) * w, h / 2 if x > 0 else -h / 2, 0])
        g.add(r)
    g.add(Line([-width / 2, 0, 0], [width / 2, 0, 0], color=GREY_D, stroke_width=1))
    return g


def plane(x_range=(-8, 8), y_range=(-5, 5), faded=False) -> NumberPlane:
    return NumberPlane(x_range=[*x_range, 1], y_range=[*y_range, 1],
                       background_line_style={"stroke_color": BLUE_D, "stroke_width": 1.5,
                                              "stroke_opacity": 0.35 if faded else 0.7},
                       faded_line_ratio=1, axis_config={"stroke_color": GREY_B, "stroke_width": 2})


def arrow(end, color=YELLOW, start=ORIGIN, stroke_width=6) -> Arrow:
    return Arrow(np.asarray(start, float), np.asarray(end, float), buff=0, color=color, stroke_width=stroke_width,
                 max_tip_length_to_length_ratio=0.18, max_stroke_width_to_length_ratio=12)


def unit_circle(color=YELLOW, radius=1.0) -> Circle:
    return Circle(radius=radius, color=color, stroke_width=4)


def matrix_tex(M, color=WHITE, font_size=40, colors=None) -> MathTex:
    """A 2 x 2 matrix in brackets; with ``colors``, column j takes colors[j]."""
    m = Matrix([[f"{x:g}" for x in r] for r in np.asarray(M)], element_alignment_corner=ORIGIN,
               bracket_h_buff=0.15, v_buff=0.6, h_buff=0.9).scale(font_size / 48)
    m.set_color(color)
    if colors:
        for j, col in enumerate(m.get_columns()):
            col.set_color(colors[j])
    return m
