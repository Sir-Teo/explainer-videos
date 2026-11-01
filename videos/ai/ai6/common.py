"""Helpers shared by the scenes of Part 6 ("Classical ML").

* :func:`chapter`, the chapter card with its voiceover;
* :func:`page_plane`, :func:`page_dots`, :func:`region_image`: the two plotted rates, the pages as dots, a classifier's
  regions as a picture;
* :func:`plot`, axes with ticks for a measured curve; :func:`spread`, a band of spread; :func:`log_ticks`;
* :func:`era_strip`, milestones evenly spaced on a line;
* :func:`bars`, a small bar chart; :func:`readout`, a label and a live number.
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 6
MONO = "DejaVu Sans Mono"
AUSTEN, DICKENS = "#E86F8A", "#58A6FF"  # the two authors, in every picture
BOUNDARY = C.BITS  # a classifier's boundary
HL = C.BITS  # a result, a highlight
HIST = C.HUMAN  # history cards
FIT = C.MODEL_Q  # a fitted model
DATA = C.TRUE_P  # data
ERR = C.SURPRISE  # residuals, errors
BAD = C.PENALTY
GOOD = C.REWARD
PANEL = "#121722"
X_RANGE, Y_RANGE = (10, 90), (0, 24)  # the plotted rates: "the" and "not", per 1,000 words


def chapter(scene, k: int, title: str, question: str, spoken: str, lit=()):
    card = chapter_card(k, title, question, lit=lit, part=PART)
    with scene.voiceover(spoken):
        scene.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
    scene.play(FadeOut(card))


def author_color(label_: int) -> str:
    return AUSTEN if label_ == 0 else DICKENS


def mix(v):
    return interpolate_color(ManimColor(AUSTEN), ManimColor(DICKENS), float(np.clip(v, 0, 1)))


def page_plane(x_length=7.0, y_length=4.6, center=ORIGIN, labels=True) -> VGroup:
    """Axes for the two plotted rates, with their names."""
    ax = Axes(x_range=[*X_RANGE, 10], y_range=[*Y_RANGE, 4], x_length=x_length, y_length=y_length, tips=False,
              axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
    ax.move_to(center)
    g = VGroup(ax)
    if labels:
        g.add(label(r"``the'' per $1{,}000$ words", font_size=22, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.15),
              label(r"``not''", font_size=22, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1))
    return g


def page_dots(ax, X2, y, idx=None, radius=0.05, opacity=0.85, jitter=0.0, seed=0, sizes=None) -> VGroup:
    """One dot per page (rates are whole numbers per 1,000, so a little jitter keeps them from piling up)."""
    idx = np.arange(len(y)) if idx is None else idx
    g = np.random.default_rng(seed)
    out = VGroup()
    for k, i in enumerate(idx):
        x, v = X2[i]
        jx, jy = (g.uniform(-jitter, jitter, 2) if jitter else (0, 0))
        if not (X_RANGE[0] <= x <= X_RANGE[1] and Y_RANGE[0] <= v <= Y_RANGE[1]):
            continue
        r = radius if sizes is None else float(sizes[k])
        d = Dot(ax.c2p(x + jx, v + jy), radius=r, color=author_color(int(y[i])), fill_opacity=opacity, stroke_width=0)
        d.page = int(i)
        out.add(d)
    return out


def region_image(values, xs, ys, ax, lo=0.0, hi=1.0, opacity=0.35) -> ImageMobject:
    """A decision region as a picture: values near ``lo`` tinted Austen, near ``hi`` Dickens, cropped to the axes."""
    v = np.clip((np.asarray(values) - lo) / (hi - lo), 0, 1)
    ca, cd = np.array(ManimColor(AUSTEN).to_rgb()), np.array(ManimColor(DICKENS).to_rgb())
    bg = np.array(ManimColor("#0B0F17").to_rgb())
    rgb = (1 - v)[..., None] * ca + v[..., None] * cd
    rgb = (1 - opacity) * bg + opacity * rgb
    img_arr = (np.concatenate([rgb, np.ones(v.shape + (1,))], -1)[::-1] * 255).astype(np.uint8)
    img = ImageMobject(img_arr)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    p0, p1 = ax.c2p(xs[0], ys[0]), ax.c2p(xs[-1], ys[-1])
    img.stretch_to_fit_width(p1[0] - p0[0]).stretch_to_fit_height(p1[1] - p0[1])
    img.move_to((p0 + p1) / 2)
    return img


def crop_to_axes(img_values, xs, ys):
    """Restrict a grid of values (rows: ys, columns: xs) to the plotted ranges."""
    xs, ys = np.asarray(xs), np.asarray(ys)
    cx = (xs >= X_RANGE[0]) & (xs <= X_RANGE[1])
    cy = (ys >= Y_RANGE[0]) & (ys <= Y_RANGE[1])
    return np.asarray(img_values)[np.ix_(cy, cx)], xs[cx], ys[cy]


def regions(ax, values, xs, ys, lo=0.0, hi=1.0, opacity=0.42):
    v, xs_, ys_ = crop_to_axes(values, xs, ys)
    return region_image(v, xs_, ys_, ax, lo=lo, hi=hi, opacity=opacity)


def line_in_box(ax, w, b, color=BOUNDARY, stroke_width=4) -> Line:
    """The line w . x + b = 0, clipped to the plotted box."""
    pts = []
    (x0, x1), (y0, y1) = X_RANGE, Y_RANGE
    if abs(w[1]) > 1e-12:
        for x in (x0, x1):
            y = -(b + w[0] * x) / w[1]
            if y0 <= y <= y1:
                pts.append((x, y))
    if abs(w[0]) > 1e-12:
        for y in (y0, y1):
            x = -(b + w[1] * y) / w[0]
            if x0 <= x <= x1:
                pts.append((x, y))
    pts = sorted(set(pts))[:2]
    if len(pts) < 2:
        return VMobject()
    return Line(ax.c2p(*pts[0]), ax.c2p(*pts[-1]), color=color, stroke_width=stroke_width)


def plot(x_range, y_range, x_length=6.0, y_length=3.6, xlabel="", ylabel="", xticks=None, yticks=None, xfmt=None,
         yfmt=None, center=ORIGIN, font_size=20) -> VGroup:
    """Axes with a few tick labels and names (the series' ``axes``); ``.ax`` is the Axes."""
    return axes(x_range, y_range, x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel, xticks=xticks,
                yticks=yticks, xfmt=xfmt, yfmt=yfmt, center=center, font_size=font_size)


def pct(v) -> str:
    return rf"{100 * v:.0f}\%"


def pow10(e: int) -> str:
    return {0: "1", 1: "10"}.get(e, f"10^{{{e}}}")


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


def hbars(rows, width=4.0, lo=0.0, hi=1.0, bar_h=0.3, font_size=22, gap=0.16, fmt=None, name_width=3.4) -> VGroup:
    """Horizontal bars: rows of (name, value, color); the value written at the bar's end."""
    fmt = fmt or (lambda v: rf"{100 * v:.1f}\%")
    g = VGroup()
    for name, v, col in rows:
        nm = label(name, font_size=font_size, color=GREY_A)
        if nm.width > name_width:
            nm.scale_to_fit_width(name_width)
        L = max(width * (v - lo) / (hi - lo), 0.02)
        bar = Rectangle(width=L, height=bar_h, stroke_width=0, fill_color=col, fill_opacity=0.85)
        val = MathTex(fmt(v), font_size=font_size, color=col)
        row = VGroup(nm, bar, val)
        nm.move_to(ORIGIN, aligned_edge=RIGHT)
        bar.move_to([0.2 + L / 2, 0, 0])
        val.next_to(bar, RIGHT, buff=0.12)
        g.add(row)
    g.arrange(DOWN, buff=gap, aligned_edge=LEFT)
    if len(g):
        x0 = g[0][1].get_left()[0]
        for r in g:
            r.shift((x0 - r[1].get_left()[0]) * RIGHT)
    for r in g:  # names flush right against the bars' common start
        x0 = r[1].get_left()[0]
        r[0].next_to([x0, r[1].get_y(), 0], LEFT, buff=0.2)
    return g


def pic_frame(mob, width, height, color=GREY_D) -> VGroup:
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=color, stroke_width=1.2,
                           fill_color=PANEL, fill_opacity=0.9)
    return VGroup(box, mob.move_to(box))


def soft_threshold(z, t):
    return math.copysign(max(abs(z) - t, 0.0), z)


def sci_tex(x, digits=1) -> str:
    """1.8e-15 as TeX: 1.8\\times 10^{-15}."""
    if x == 0:
        return "0"
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    return rf"{m:.{digits}f}\times 10^{{{e}}}"


def side_ladder(scene, rows, whys, center_x: float, half_width: float, **kw):
    """The series' ``ladder`` in a column of the frame: the rows (and their reasons) fit within ``half_width`` of
    ``center_x``.  The shared ladder only bounds rows symmetrically about the centre of the frame, so lay them out
    there and slide them across (``step`` only ever moves rows up and down)."""
    kw.pop("x", None)
    step = ladder(scene, rows, whys, x=0.0, edge=half_width, **kw)
    for r, w in zip(rows, whys):
        r.shift(RIGHT * center_x)
        if w is not None:
            w.shift(RIGHT * center_x)
    return step
