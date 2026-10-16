"""Helpers shared by the scenes of Part 7 ("Complex Analysis").

Part 7 draws complex functions by domain coloring (``explainer.analysis.complexplot``: hue = arg f, brightness = |f|
with rings at powers of 2), maps of grids under holomorphic functions, and contours with their winding numbers.
"""

from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis1.common import polyline  # noqa: F401
from videos.analysis.analysis2.common import plain_axes  # noqa: F401
from videos.analysis.analysis4.common import heatmap, square_axes  # noqa: F401

from .compute import load, trap  # noqa: F401


def cplot(ax: Axes, F, xr, yr, px=720, rings=True, mask=None) -> ImageMobject:
    """The domain coloring of F on the rectangle xr x yr, sized and placed on the axes ax."""
    p0, p1 = ax.c2p(xr[0], yr[0]), ax.c2p(xr[1], yr[1])
    img = domain_image(F, xr, yr, p1[0] - p0[0], p1[1] - p0[1], px=px, rings=rings, mask=mask)
    return img.move_to((p0 + p1) / 2)


def cplot_fine(ax: Axes, F, xr, yr, px=960, ss=3, rings=True, mask=None) -> ImageMobject:
    """Like ``cplot``, but each pixel is the average of ss x ss samples (computed a band of rows at a time), so
    rings and phases that turn faster than a pixel blend to their mean instead of aliasing into speckle; ``mask``
    gets the same treatment, so its edge is anti-aliased. For essential singularities (Hook, Beurling)."""
    if config.dry_run:  # layout checks never look at the pixels: same size and place, a quarter of the work
        px, ss = max(64, px // 4), 1
    p0, p1 = ax.c2p(xr[0], yr[0]), ax.c2p(xr[1], yr[1])
    w, h = p1[0] - p0[0], p1[1] - p0[1]
    py = max(2, int(px * h / w))
    xs = xr[0] + (np.arange(px * ss) + 0.5) / (px * ss) * (xr[1] - xr[0])
    ys = yr[1] - (np.arange(py * ss) + 0.5) / (py * ss) * (yr[1] - yr[0])
    out = np.zeros((py, px, 4))
    band = 32
    for r0 in range(0, py, band):
        r1 = min(py, r0 + band)
        X, Y = np.meshgrid(xs, ys[r0 * ss:r1 * ss])
        Z = X + 1j * Y
        with np.errstate(all="ignore"):
            rgb = domain_rgb(F(Z), rings=rings)
        a = np.ones(Z.shape) if mask is None else mask(Z).astype(float)
        nr = r1 - r0
        A = a.reshape(nr, ss, px, ss).sum(axis=(1, 3))
        RGB = (rgb * a[..., None]).reshape(nr, ss, px, ss, 3).sum(axis=(1, 3))
        out[r0:r1, :, :3] = RGB / np.maximum(A, 1e-12)[..., None]
        out[r0:r1, :, 3] = A / ss**2
    img = ImageMobject((np.clip(out, 0, 1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    img.stretch_to_fit_width(w)
    img.stretch_to_fit_height(h)
    return img.move_to((p0 + p1) / 2)


def zcurve(ax: Axes, z, color, stroke_width=3.0, closed=False) -> VMobject:
    """A polyline through the complex points z on ax."""
    z = np.asarray(z)
    pts = [ax.c2p(w.real, w.imag) for w in z]
    if closed:
        pts.append(pts[0])
    return VMobject(stroke_color=color, stroke_width=stroke_width).set_points_as_corners(pts)


def zgrid(ax: Axes, F, xr, yr, n=9, color=GREY_B, stroke_width=1.6, samples=80, colors=None) -> VGroup:
    """Images under F (complex -> complex, vectorized) of the lines x = const and y = const of an n x n grid on
    xr x yr; with ``colors`` = (horizontal, vertical) the two families get their own colors."""
    g = VGroup()
    t = np.linspace(0, 1, samples)
    ch, cv = colors if colors else (color, color)
    for c in np.linspace(0, 1, n):
        horiz = xr[0] + (xr[1] - xr[0]) * t + 1j * (yr[0] + (yr[1] - yr[0]) * c)
        vert = xr[0] + (xr[1] - xr[0]) * c + 1j * (yr[0] + (yr[1] - yr[0]) * t)
        g.add(zcurve(ax, F(horiz), ch, stroke_width))
        g.add(zcurve(ax, F(vert), cv, stroke_width))
    return g


def phase_wheel(radius=0.45, n=72) -> VGroup:
    """The legend: a ring colored by arg, with 0 (red) on the right."""
    g = VGroup()
    for k in range(n):
        a0, a1 = 2 * np.pi * k / n, 2 * np.pi * (k + 1) / n
        col = ManimColor(tuple(float(c) for c in hue_rgb(np.array((a0 + a1) / 2))))
        g.add(AnnularSector(inner_radius=radius * 0.6, outer_radius=radius, angle=a1 - a0, start_angle=a0,
                            fill_color=col, fill_opacity=1, stroke_width=0))
    lab = VGroup(MathTex(r"0", font_size=18).next_to(g, RIGHT, buff=0.06),
                 MathTex(r"\pi", font_size=18).next_to(g, LEFT, buff=0.06),
                 MathTex(r"\tfrac{\pi}{2}", font_size=18).next_to(g, UP, buff=0.04))
    t = label(r"$\arg f$", font_size=20, color=GREY_B).next_to(g, DOWN, buff=0.06)
    return VGroup(g, lab, t)
