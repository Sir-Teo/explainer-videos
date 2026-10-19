"""Helpers shared by the scenes of Part 6 ("Classical ML")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
AUSTEN, DICKENS = "#E86F8A", "#58A6FF"  # the two authors, in every picture
BOUNDARY = C.BITS  # a classifier's boundary
X_RANGE, Y_RANGE = (10, 90), (0, 24)  # the plotted rates: "the" and "not", per 1,000 words


def author_color(label: int) -> str:
    return AUSTEN if label == 0 else DICKENS


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


def page_dots(ax, X2, y, idx=None, radius=0.05, opacity=0.85, jitter=0.0, seed=0) -> VGroup:
    """One dot per page (rates are whole numbers per 1,000, so a little jitter keeps them from piling up)."""
    idx = np.arange(len(y)) if idx is None else idx
    g = np.random.default_rng(seed)
    out = VGroup()
    for i in idx:
        x, v = X2[i]
        if not (X_RANGE[0] <= x <= X_RANGE[1] and Y_RANGE[0] <= v <= Y_RANGE[1]):
            continue
        jx, jy = (g.uniform(-jitter, jitter, 2) if jitter else (0, 0))
        out.add(Dot(ax.c2p(x + jx, v + jy), radius=radius, color=author_color(int(y[i])), fill_opacity=opacity,
                    stroke_width=0))
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
    return Line(ax.c2p(*pts[0]), ax.c2p(*pts[-1]), color=color, stroke_width=stroke_width)
