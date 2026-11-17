"""Helpers shared by the scenes of Part 19 of *Psychology, Built* ("Working Memory")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 19

# one meaning per colour, for this part
MEM = "#F2C14E"  # what is held in mind; the bump; the remembered item
LOOP = "#7EC8F5"  # the phonological loop, verbal material, resources
SKETCH = "#5BD18B"  # the visuospatial sketchpad
EXEC = "#B39DDB"  # the central executive, control, chunks
LOST = "#EF6F6C"  # forgetting, guesses, interference, swaps
SLOT = "#F28FB8"  # the slot models
MODEL = "#5BD18B"  # what Psyche computes, and the variable-precision model
YOU = "#F2C14E"  # the viewer
DATA = P.ARCHIVE
BAD = P.ERR
KANT = P.KANT
GOOD = "#5BD18B"


def pct(x: float, digits: int = 0) -> str:
    return rf"{100 * x:.{digits}f}\%"


def num(n) -> str:
    """An integer with thousands separators that TeX sets without a gap."""
    return f"{int(n):,}".replace(",", "{,}")


def keep_in_frame(mob, margin: float = 0.25):
    half = config.frame_width / 2 - margin
    if mob.get_left()[0] < -half:
        mob.shift(RIGHT * (-half - mob.get_left()[0]))
    if mob.get_right()[0] > half:
        mob.shift(LEFT * (mob.get_right()[0] - half))
    return mob


def rows_of(items, width: float, font_size: int = 30, buff: float = 0.34) -> VGroup:
    """Lines of text, each (text, colour), wrapped to ``width`` and stacked."""
    return VGroup(*[wrapped_label(t, width, font_size, c) for t, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def bounds(ax):
    """The data range of an axis pair (corner axes store their ranges shifted to start at zero)."""
    ox, oy = getattr(ax, "_off", (0.0, 0.0))
    return (float(ax.x_range[0] + ox), float(ax.x_range[1] + ox)), (float(ax.y_range[0] + oy), float(ax.y_range[1] + oy))


def scatter(ax, x, y, color, radius: float = 0.04, opacity: float = 0.85) -> VGroup:
    (x0, x1), (y0, y1) = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
    return VGroup(*[Dot(ax.c2p(float(a), float(b)), radius=radius, color=color, fill_opacity=opacity)
                    for a, b in zip(x[keep], y[keep])])


def curve_in(ax, x, y, color, stroke_width=3, smooth=False):
    """A curve with the points outside the axes' x range left out."""
    (x0, x1), _ = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1)
    return curve(ax, x[keep], y[keep], color, stroke_width=stroke_width, smooth=smooth)


def frame_box(mob, color=GREY_C, buff: float = 0.0) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=2)


def hue(angle: float) -> str:
    """The colour at ``angle`` (radians) on the report wheel: a hue circle at fixed lightness."""
    import colorsys

    h = (float(angle) % (2 * np.pi)) / (2 * np.pi)
    r, g, b = colorsys.hls_to_rgb(h, 0.6, 0.65)
    return ManimColor.from_rgb((r, g, b))


def wheel(radius: float = 1.4, width: float = 0.28, n: int = 90) -> VGroup:
    """A colour wheel for continuous report: ``n`` annular sectors."""
    out = VGroup()
    for k in range(n):
        a0 = 2 * np.pi * k / n
        out.add(AnnularSector(inner_radius=radius - width, outer_radius=radius, angle=2 * np.pi / n + 0.002,
                              start_angle=a0, fill_color=hue(a0 + np.pi / n), fill_opacity=1, stroke_width=0))
    return out


def digits_row(text: str, font_size: int = 60, color=WHITE, buff: float = 0.35) -> VGroup:
    """A row of digits or letters, each its own mobject."""
    return VGroup(*[label(ch, font_size=font_size, color=color) for ch in text]).arrange(RIGHT, buff=buff)


def bars(ax, xs, ys, color, width: float = 0.6, opacity: float = 0.85) -> VGroup:
    """Vertical bars from zero (or the axis floor) to ``ys`` at ``xs``, in data units."""
    (_, _), (y0, _) = bounds(ax)
    out = VGroup()
    for x, y in zip(xs, ys):
        lo, hi = ax.c2p(float(x), max(y0, 0.0)), ax.c2p(float(x), float(y))
        w = abs(ax.c2p(float(x) + width / 2, 0)[0] - ax.c2p(float(x) - width / 2, 0)[0])
        out.add(Rectangle(width=w, height=max(hi[1] - lo[1], 1e-3), stroke_width=0, fill_color=color,
                          fill_opacity=opacity).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
    return out
