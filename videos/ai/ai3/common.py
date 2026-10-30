"""Helpers shared by the scenes of Part 3 ("Vectors That Mean Things").

* :func:`barcode`, a vector of hundreds of numbers drawn as a strip of colored ticks (one per coordinate);
* :func:`plane`, the 3Blue1Brown-style grid used by the linear-algebra chapters, and :func:`arrow`;
* :func:`gray_image` and :func:`heat_image`, a matrix or a picture as an image;
* :func:`hist_bars`, a histogram drawn on axes; :func:`log_ticks`, powers of ten on a log axis;
* :func:`chapter`, the chapter card with its voiceover.
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import CATEGORIES, VOWELS, load  # noqa: F401

PART = 3
MONO = "DejaVu Sans Mono"
CAT_COLORS = {"animals": "#F2A541", "colors": "#E85D75", "numbers": "#58A6FF", "places": "#5BD17A",
              "family": "#D4A5FF", "body": "#4FD1C5", "verbs": "#F7D154"}
I_COLOR, J_COLOR = "#7CE38B", "#FF6B8B"  # the two basis vectors: green for the first, red for the second
VA, VB = C.TRUE_P, C.MODEL_Q  # two vectors a, b
HL = C.BITS  # what the sentence is about: a result, a highlight
HIST = C.HUMAN  # history cards
SIG = C.BITS  # singular values, stretches
UC, VC = C.TRUE_P, C.MODEL_Q  # U (output directions) and V (input directions)
TRAINED = C.SURPRISE  # trained weights
RANDOM = GREY_B  # random matrices
MPC = C.INTERVAL  # the Marchenko-Pastur law, predictions, bounds
GRAD = C.SCORE  # gradients
ERR = C.PENALTY
PANEL = "#121722"


def chapter(scene, k: int, title: str, question: str, spoken: str, lit=()):
    card = chapter_card(k, title, question, lit=lit, part=PART)
    with scene.voiceover(spoken):
        scene.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
    scene.play(FadeOut(card))


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


def mat2(M, font_size=40, cols=(I_COLOR, J_COLOR)) -> Matrix:
    m = Matrix([[f"{x:g}" for x in r] for r in np.asarray(M)], h_buff=0.9, v_buff=0.65, bracket_h_buff=0.12)
    m.scale(font_size / 48)
    if cols:
        for j, col in enumerate(m.get_columns()):
            col.set_color(cols[j % len(cols)])
    return m


def rot(a):
    return np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])


def gray_image(arr, width) -> ImageMobject:
    a = np.asarray(arr)
    if a.dtype != np.uint8:
        a = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    rgb = np.stack([a, a, a, np.full_like(a, 255)], -1)
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.scale_to_fit_width(width)
    return img


def heat_image(M, width, height, color=C.TRUE_P, gamma=0.6, vmax=None) -> ImageMobject:
    """A non-negative matrix as a picture: dark for 0, ``color`` for the largest entry."""
    M = np.asarray(M, float)
    v = np.clip(M / (vmax or max(M.max(), 1e-12)), 0, 1) ** gamma
    c = np.array(ManimColor(color).to_rgb())
    bg = np.array(ManimColor(PANEL).to_rgb())
    rgb = bg[None, None] * (1 - v[..., None]) + c[None, None] * v[..., None]
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def framed(img, color=GREY_D, sw=1.2) -> Group:
    return Group(img, SurroundingRectangle(img, buff=0, color=color, stroke_width=sw))


def hist_bars(ax, edges, counts, color, opacity=0.75, scale=1.0) -> VGroup:
    """Bars of a histogram on ``ax`` (x in data units, heights counts * scale)."""
    g = VGroup()
    for a, b, c in zip(edges[:-1], edges[1:], counts):
        h = float(c) * scale
        if h <= 0:
            continue
        p0, p1 = ax.c2p(a, 0), ax.c2p(b, h)
        g.add(Rectangle(width=max(p1[0] - p0[0], 0.005), height=max(p1[1] - p0[1], 0.002), stroke_width=0,
                        fill_color=color, fill_opacity=opacity).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
    return g


def pow10(e: int) -> str:
    return {0: "1", 1: "10"}.get(e, f"10^{{{e}}}")


def log_ticks(ax, axis: str, exps, font_size=20, y0=None, x0=None) -> VGroup:
    """Tick labels 10^e on a log10 axis (values are exponents)."""
    g = VGroup()
    for e in exps:
        t = MathTex(pow10(e), font_size=font_size, color=GREY_B)
        if axis == "x":
            t.next_to(ax.c2p(e, y0 if y0 is not None else ax.y_range[0]), DOWN, buff=0.12)
        else:
            t.next_to(ax.c2p(x0 if x0 is not None else ax.x_range[0], e), LEFT, buff=0.12)
        g.add(t)
    return g


def dots_on(ax, xs, ys, color, radius=0.05, opacity=1.0) -> VGroup:
    return VGroup(*[Dot(ax.c2p(x, y), radius=radius, color=color, fill_opacity=opacity) for x, y in zip(xs, ys)])


def era_strip(events, y0=-0.2, width=5.9, font_size=20, color=None) -> tuple:
    """Milestones evenly spaced on a line, alternating above and below: returns (axis, skeleton, marks)."""
    color = color or HIST
    n = len(events)
    xs = np.linspace(-width, width, n)
    axis = Line([-6.7, y0, 0], [6.7, y0, 0], color=GREY_C, stroke_width=3)
    marks, skel = [], VGroup()
    for i, ((yr, txt), x) in enumerate(zip(events, xs)):
        up = i % 2 == 0
        stem = Line([x, y0, 0], [x, y0 + (0.85 if up else -0.85), 0], color=color, stroke_width=2.5)
        dot = Dot([x, y0, 0], radius=0.08, color=color)
        yl = label(rf"{yr}", font_size=font_size + 8, color=color)
        t = label(txt, font_size=font_size, color=WHITE)
        words = VGroup(yl, t).arrange(DOWN, buff=0.06)
        words.next_to(stem.get_end(), UP if up else DOWN, buff=0.08)
        keep_in_frame(words, margin=0.12)
        marks.append(VGroup(stem, dot, words))
        skel.add(VGroup(stem.copy().set_stroke(GREY_D), Dot([x, y0, 0], radius=0.06, color=GREY_D),
                        yl.copy().set_color(GREY_D).move_to(yl)))
    return axis, skel, marks


def ex(x) -> int:
    """The power of ten nearest x (for narration: 'ten to the {ex(x)}')."""
    return int(round(math.log10(abs(float(x)))))


def seeds_text(vals, digits=3) -> str:
    """'0.912 (0.910 to 0.915)' as plain words for the narration: mean and the range over seeds."""
    v = np.asarray(vals, float)
    return f"{v.mean():.{digits}f}"
