"""Helpers shared by the scenes of Part 4 ("Calculus in Many Dimensions").

Part 4 draws maps of the plane: a square grid and its image under a map, small squares and the parallelograms the
derivative predicts, and level curves (``explainer.analysis.contours``).
"""

from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import polyline  # noqa: F401
from videos.analysis2.common import plain_axes  # noqa: F401

from .compute import load  # noqa: F401


def square_axes(x_range, y_range, unit, numbers=False, **kw) -> Axes:
    """Axes with the same scene length per unit on both axes (so circles stay round)."""
    return plain_axes(x_range, y_range, unit * (x_range[1] - x_range[0]), unit * (y_range[1] - y_range[0]),
                      numbers=numbers, **kw)


def mapped_grid(ax: Axes, F, xr, yr, n=9, color=GREY_C, stroke_width=1.5, samples=60) -> VGroup:
    """The images under F of the lines x = const and y = const of an n-by-n grid on xr x yr (F maps arrays of shape
    (..., 2) to the same shape; the identity gives the plain grid)."""
    g = VGroup()
    t = np.linspace(0, 1, samples)
    for c in np.linspace(0, 1, n):
        for line in (np.c_[xr[0] + (xr[1] - xr[0]) * t, np.full_like(t, yr[0] + (yr[1] - yr[0]) * c)],
                     np.c_[np.full_like(t, xr[0] + (xr[1] - xr[0]) * c), yr[0] + (yr[1] - yr[0]) * t]):
            q = F(line)
            g.add(VMobject(stroke_color=color, stroke_width=stroke_width).set_points_as_corners(
                [ax.c2p(a, b) for a, b in q]))
    return g


def line_through(ax: Axes, p, d, color, stroke_width=2.0, dashed=True):
    """The line through p with direction d, clipped to the axes' window."""
    (x0, x1), (y0, y1) = ax.x_range[:2], ax.y_range[:2]
    ts = []
    for lo, hi, pc, dc in ((x0, x1, p[0], d[0]), (y0, y1, p[1], d[1])):
        if abs(dc) > 1e-12:
            ts += [(lo - pc) / dc, (hi - pc) / dc]
    cands = sorted(t for t in ts if x0 - 1e-9 <= p[0] + t * d[0] <= x1 + 1e-9 and y0 - 1e-9 <= p[1] + t * d[1] <= y1 + 1e-9)
    a, b = np.asarray(p) + cands[0] * np.asarray(d), np.asarray(p) + cands[-1] * np.asarray(d)
    cls = DashedLine if dashed else Line
    return cls(ax.c2p(*a), ax.c2p(*b), color=color, stroke_width=stroke_width)


def heatmap(F, xr, yr, width, height, vmin, vmax, px=360, neg=C.SEQ, pos=C.CLOSED_SET, mid=BACKGROUND) -> ImageMobject:
    """F(X, Y) on xr x yr as an image (negative values toward ``neg``, positive toward ``pos``), sized width x
    height in scene units; place it with .move_to(ax.c2p(...))."""
    py = max(2, int(px * height / width))
    X, Y = np.meshgrid(np.linspace(xr[0], xr[1], px), np.linspace(yr[1], yr[0], py))
    with np.errstate(invalid="ignore", divide="ignore"):
        Z = np.nan_to_num(F(X, Y))
    t = np.clip((Z - vmin) / (vmax - vmin), 0, 1) * 2 - 1  # -1 .. 1
    c_neg, c_pos, c_mid = (np.array(ManimColor(c).to_rgb()) for c in (neg, pos, mid))
    a = np.abs(t)[..., None]
    rgb = np.where(t[..., None] < 0, c_mid + a * (c_neg - c_mid), c_mid + a * (c_pos - c_mid))
    img = ImageMobject((rgb * 255).astype(np.uint8))
    img.stretch_to_fit_width(width)
    img.stretch_to_fit_height(height)
    return img


def angle_ticks(ax: Axes, font_size=20, color=GREY_B, name=r"\theta") -> VGroup:
    """Labels 0, pi/2, pi, 3pi/2, 2pi under the bottom edge of an angle axis (outside the plot, so no curve runs
    through them), and the axis name at the right end of that row."""
    y0 = ax.y_range[0]
    texts = [r"0", r"\tfrac{\pi}{2}", r"\pi", r"\tfrac{3\pi}{2}", r"2\pi"]
    g = VGroup()
    for k, t in enumerate(texts):
        g.add(MathTex(t, font_size=font_size, color=color).next_to(ax.c2p(k * np.pi / 2, y0), DOWN, buff=0.12))
    g.add(MathTex(name, font_size=font_size + 4, color=color).next_to(g[-1], RIGHT, buff=0.25))
    return g
