"""Helpers shared by the scenes of Part 29 of *Psychology, Built* ("Emotion")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 29

# one meaning per colour, for this part
BODY = "#7EC8F5"  # the body: arousal, the viscera, interoception
PLEAS = "#5BD18B"  # pleasant feeling, valence up
UNPL = "#EF6F6C"  # unpleasant feeling, and what failed
FEAR = "#F28FB8"  # fear and the amygdala
COG = "#F2C14E"  # appraisal, labels, concepts
FACE = "#FF9F43"  # faces and expressions
MODEL = "#B39DDB"  # what Psyche computes
LOST = "#EF6F6C"
YOU = "#F2C14E"  # the viewer
DATA = P.ARCHIVE
BAD = P.ERR
KANT = P.KANT
GOOD = "#5BD18B"
WORD = COG


def pct(x: float, digits: int = 0) -> str:
    return rf"{100 * x:.{digits}f}\%"


def spct(x: float) -> str:
    """A share as narration reads it: "45 percent"."""
    return f"{100 * x:.0f} percent"


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


def word_chip(word: str, color=WORD, font_size=26, width=None) -> VGroup:
    """A word in a rounded box."""
    t = label(word, font_size=font_size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=width or t.width + 0.3, height=t.height + 0.25,
                           stroke_color=color, stroke_width=2, fill_color=BLACK, fill_opacity=0.6)
    return VGroup(box, t.move_to(box))


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


def face(valence: float, arousal: float, color=FACE, radius: float = 0.5, stroke: float = 3) -> VGroup:
    """A schematic face from two numbers in [-1, 1]: the mouth curves up with valence and opens with arousal; the
    eyes widen and the brows rise with arousal; with negative valence and high arousal the brows slant (anger when
    valence is lowest, fear otherwise).  The interactive draws the same faces from the same rule."""
    r = radius
    head = Circle(radius=r, color=color, stroke_width=stroke, fill_color=BLACK, fill_opacity=0.6)
    eye_h = 0.06 + 0.07 * (arousal + 1) / 2
    eyes = VGroup(*[Ellipse(width=0.12 * r / 0.5, height=eye_h * r / 0.5, color=color, fill_opacity=1,
                            stroke_width=0).move_to([dx * r, 0.18 * r, 0]) for dx in (-0.35, 0.35)])
    lift = 0.38 * r + 0.08 * r * arousal
    tilt = 0.0
    if valence < -0.2 and arousal > 0.2:
        tilt = 0.12 * r if valence < -0.75 else -0.12 * r  # anger: inner ends down; fear: inner ends up
    brows = VGroup(Line([-0.5 * r, lift, 0], [-0.18 * r, lift - tilt, 0], color=color, stroke_width=stroke),
                   Line([0.18 * r, lift - tilt, 0], [0.5 * r, lift, 0], color=color, stroke_width=stroke))
    w = 0.5 * r
    c = -0.28 * r * valence
    y0 = -0.38 * r
    top = VMobject(color=color, stroke_width=stroke).set_points_smoothly(
        [[-w, y0, 0], [0, y0 + c, 0], [w, y0, 0]])
    mouth = VGroup(top)
    opening = max(arousal, 0) * 0.16 * r
    if opening > 0.01:
        bottom = VMobject(color=color, stroke_width=stroke).set_points_smoothly(
            [[-w * 0.8, y0 - 0.02 * r, 0], [0, y0 + c - opening, 0], [w * 0.8, y0 - 0.02 * r, 0]])
        mouth.add(bottom)
    return VGroup(head, eyes, brows, mouth)
