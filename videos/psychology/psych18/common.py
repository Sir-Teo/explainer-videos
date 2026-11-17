"""Helpers shared by the scenes of Part 18 of *Psychology, Built* ("Attention")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 18

# one meaning per colour, for this part
ATT = "#F2C14E"  # attention, the attended, the spotlight
TARGET = "#EF6F6C"  # the target, red items
DIST = "#5BD18B"  # distractors, green items
CUE = "#7EC8F5"  # a cue, the unattended ear
CONFLICT = "#F28FB8"  # conflict, the word pathway, interference
CONTROL = "#B39DDB"  # control, the normalization pool, capacity
MODEL = "#5BD18B"  # what Psyche computes
YOU = "#F2C14E"  # the viewer
DATA = P.ARCHIVE
BAD = P.ERR
KANT = P.KANT
GOOD = "#5BD18B"
INHIB = "#EF6F6C"


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


def log_axes(x_dec, y_dec, x_length=6.0, y_length=3.6, xlabel="", ylabel="", center=ORIGIN, font_size=20) -> VGroup:
    """Axes in decades: ``x_dec`` and ``y_dec`` are (lo, hi) powers of ten; tick labels read 10^k."""
    return axes(list(x_dec), list(y_dec), x_length=x_length, y_length=y_length,
                xticks=list(range(int(x_dec[0]), int(x_dec[1]) + 1)), yticks=list(range(int(y_dec[0]), int(y_dec[1]) + 1)),
                xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", xlabel=xlabel, ylabel=ylabel,
                center=center, font_size=font_size)


def picture(arr, height: float = 4.0, smooth: bool = False, lo: float = 0.0, hi: float = 1.0) -> ImageMobject:
    """A 2-D array as a grey image (``lo`` black, ``hi`` white), or an (h, w, 3) array as a colour image in [0, 1]."""
    a = np.asarray(arr, float)
    if a.ndim == 2:
        g = np.clip((a - lo) / (hi - lo), 0.0, 1.0)
        rgb = np.repeat((g * 255).astype(np.uint8)[:, :, None], 3, axis=2)
    else:
        rgb = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.scale_to_fit_height(height)
    return img


def swatch(rgb, side: float = 1.0, stroke=GREY_C) -> Square:
    """A colour patch from an sRGB triple in [0, 1]."""
    c = np.clip(np.asarray(rgb, float), 0, 1)
    return Square(side, stroke_color=stroke, stroke_width=1.5, fill_color=ManimColor.from_rgb(c), fill_opacity=1.0)


def frame_box(mob, color=GREY_C, buff: float = 0.0) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=2)


def share_bar(shares, colors, width: float = 6.0, height: float = 0.55, names=None, font_size: int = 26) -> VGroup:
    """One bar cut into shares (clipped at zero and rescaled to fill it), labelled where a share is wide enough."""
    v = np.clip(np.asarray(shares, float), 0, None)
    v = v / v.sum()
    parts, x = VGroup(), -width / 2
    for s, c in zip(v, colors):
        w = max(width * float(s), 1e-3)
        parts.add(Rectangle(width=w, height=height, stroke_width=0, fill_color=c, fill_opacity=0.9).move_to([x + w / 2, 0, 0]))
        x += w
    g = VGroup(parts)
    if names:
        labs = VGroup()
        for part, name, s in zip(parts, names, v):
            if s > 0.07 and name:
                labs.add(label(name, font_size=font_size, color=BLACK).move_to(part))
        g.add(labs)
    g.parts = parts
    return g


def curve_in(ax, x, y, color, stroke_width=3, smooth=False):
    """A curve with the points outside the axes' x range left out."""
    (x0, x1), _ = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1)
    return curve(ax, x[keep], y[keep], color, stroke_width=stroke_width, smooth=smooth)


def search_glyphs(arr, center, size: float = 3.6, letters: bool = False, glyph: float = 0.32) -> VGroup:
    """Draw a search display stored as rows (colour, orientation, shape, x, y) in a square of side ``size``: coloured
    bars (red or green, vertical or horizontal), or, with ``letters``, a T among Ls."""
    arr = np.asarray(arr, float)
    out = VGroup()
    for k, (col, ori, shp, x, y) in enumerate(arr):
        p = np.array([center[0] + (x - 0.5) * size, center[1] + (y - 0.5) * size, 0])
        c = TARGET if col > 0 else DIST
        if letters:
            g = glyph * 0.9
            if shp > 0:  # a T
                item = VGroup(Line(p + [-g / 2, g / 2, 0], p + [g / 2, g / 2, 0]), Line(p + [0, g / 2, 0], p + [0, -g / 2, 0]))
            else:  # an L, its foot offset so it is not a T
                item = VGroup(Line(p + [-g / 2, g / 2, 0], p + [-g / 2, -g / 2, 0]),
                              Line(p + [-g / 2, -g / 2, 0], p + [g / 2, -g / 2, 0]))
            item.set_stroke(WHITE, 5).rotate((k % 4) * PI / 2, about_point=p)
        else:
            w, h = (glyph * 0.28, glyph) if ori == 0 else (glyph, glyph * 0.28)
            item = Rectangle(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=1).move_to(p)
        out.add(item)
    return out
