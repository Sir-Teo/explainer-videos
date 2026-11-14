"""Helpers shared by the scenes of Part 11 of *Psychology, Built* ("The Threshold")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 11

# one meaning per colour, for this part
STD = "#9AA4B2"  # the standard stimulus
CMP = "#E8EDF2"  # the comparison
WEBERC = "#7EC8F5"  # Weber: the just noticeable difference
FECHC = "#B39DDB"  # Fechner: the scale of sensation
STEVC = "#F28FB8"  # Stevens: numbers and the power law
MODEL = "#5BD18B"  # a fitted curve, and what Psyche computes
YOU = "#F2C14E"  # the viewer
DATA = P.ARCHIVE  # a published figure
BAD = P.ERR
THRESH = P.ACCENT
KANT = P.KANT
NOISE = "#8FA3BF"


def r2(x: float) -> str:
    s = f"{x:.2f}"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s


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


def big_number(value: str, caption: str, color, font_size: int = 72, width: float = 4.2, cap_size: int = 28) -> VGroup:
    return VGroup(label(value, font_size=font_size, color=color), wrapped_label(caption, width, cap_size, GREY_A)).arrange(
        DOWN, buff=0.18)


def rows_of(items, width: float, font_size: int = 30, buff: float = 0.34) -> VGroup:
    """Lines of text, each (text, colour), wrapped to ``width`` and stacked."""
    return VGroup(*[wrapped_label(t, width, font_size, c) for t, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def scatter(ax, x, y, color, radius: float = 0.035, opacity: float = 0.75) -> VGroup:
    """Points on axes, clipped to the axes' range."""
    (x0, x1), (y0, y1) = bounds(ax)
    keep = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
    return VGroup(*[Dot(ax.c2p(float(a), float(b)), radius=radius, color=color, fill_opacity=opacity)
                    for a, b in zip(np.asarray(x)[keep], np.asarray(y)[keep])])


def bounds(ax):
    """The data range of an axis pair (corner axes store their ranges shifted to start at zero)."""
    ox, oy = getattr(ax, "_off", (0.0, 0.0))
    return (float(ax.x_range[0] + ox), float(ax.x_range[1] + ox)), (float(ax.y_range[0] + oy), float(ax.y_range[1] + oy))


def share_bar(shares, colors, width: float = 6.0, height: float = 0.55, names=None, font_size: int = 26) -> VGroup:
    """One bar cut into shares (they are clipped at zero and rescaled to fill it).  ``.parts[i]``."""
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
        for part, name, c, s in zip(parts, names, colors, v):
            if s > 0.07:
                labs.add(label(name, font_size=font_size, color=BLACK).move_to(part))
        g.add(labs)
    g.parts = parts
    return g


def chain(names, colors=None, width: float = 12.6, font_size: int = 24, height: float = 0.9) -> VGroup:
    """A row of boxes joined by arrows: the measurement chain.  ``.boxes[i]`` and ``.arrows[i]``."""
    n = len(names)
    w = (width - 0.45 * (n - 1)) / n
    boxes = VGroup()
    for i, name in enumerate(names):
        col = colors[i] if colors else VOLT
        box = RoundedRectangle(width=w, height=height, corner_radius=0.12, color=col, stroke_width=2.5,
                               fill_color=col, fill_opacity=0.1)
        boxes.add(VGroup(box, wrapped_label(name, w - 0.15, font_size, col).move_to(box)))
    boxes.arrange(RIGHT, buff=0.45)
    arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.04, color=GREY_B, stroke_width=3,
                            max_tip_length_to_length_ratio=0.45) for i in range(n - 1)])
    g = VGroup(boxes, arrows)
    g.boxes, g.arrows = boxes, arrows
    return g


def patch_pair(left: float, right: float, size: float = 1.6, gap: float = 0.5, base: float = 100.0) -> VGroup:
    """Two grey patches side by side whose brightness stands for intensities around ``base``."""
    def grey(v):
        g = int(np.clip(70 + (v - base) * 2.2 + 40, 20, 235))
        return f"#{g:02x}{g:02x}{g:02x}"
    a = Square(side_length=size, stroke_width=0, fill_color=grey(left), fill_opacity=1)
    b = Square(side_length=size, stroke_width=0, fill_color=grey(right), fill_opacity=1)
    g = VGroup(a, b).arrange(RIGHT, buff=gap)
    frame = SurroundingRectangle(g, buff=0.35, color=GREY_D, stroke_width=2, corner_radius=0.1)
    out = VGroup(frame, g)
    out.left, out.right = a, b
    return out


def log_axes(x_dec, y_dec, x_length=6.0, y_length=3.6, xlabel="", ylabel="", center=ORIGIN, font_size=20) -> VGroup:
    """Axes in decades: ``x_dec`` and ``y_dec`` are (lo, hi) powers of ten; tick labels read 10^k."""
    return axes(list(x_dec), list(y_dec), x_length=x_length, y_length=y_length,
                xticks=list(range(int(x_dec[0]), int(x_dec[1]) + 1)), yticks=list(range(int(y_dec[0]), int(y_dec[1]) + 1)),
                xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", xlabel=xlabel, ylabel=ylabel,
                center=center, font_size=font_size)
