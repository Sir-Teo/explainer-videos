"""Helpers shared by the scenes of Part 6 of *Psychology, Built* ("Synapses and Circuits")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 6

# one meaning per colour, for this part
VOLT = "#E8EDF2"  # a membrane potential, a neutral trace
EXC = "#F28FB8"  # excitation: a synapse, a current, a unit that excites
INH = "#7EC8F5"  # inhibition
LEAK = "#8FA3BF"  # anything passive, a comparison line
MODEL = "#5BD18B"  # what the equations compute
DATA = "#F2A65A"  # what was measured, a historical fact
RULE = "#B48EF0"  # a learning rule, a weight
THRESH = P.ACCENT  # a threshold, the thing to look at
BAD = P.ERR
KANT = P.KANT


def r2(x: float) -> str:
    """A number to two places without the leading zero: ``.22``; ``1.00`` stays."""
    s = f"{x:.2f}"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s


def pct(x: float, digits: int = 0) -> str:
    return rf"{100 * x:.{digits}f}\%"


def keep_in_frame(mob, margin: float = 0.25):
    """Shift ``mob`` sideways so that it does not cross the left or right edge of the frame."""
    half = config.frame_width / 2 - margin
    if mob.get_left()[0] < -half:
        mob.shift(RIGHT * (-half - mob.get_left()[0]))
    if mob.get_right()[0] > half:
        mob.shift(LEFT * (mob.get_right()[0] - half))
    return mob


def big_number(value: str, caption: str, color, font_size: int = 72, width: float = 4.2, cap_size: int = 26) -> VGroup:
    """A number to remember, with one line under it saying what it is."""
    return VGroup(label(value, font_size=font_size, color=color), wrapped_label(caption, width, cap_size, GREY_A)).arrange(
        DOWN, buff=0.18)


def code_block(lines, font_size=24, width: float | None = None) -> VGroup:
    """A few lines of code on a dark panel (monospace through TeX)."""
    rows = VGroup(*[label(rf"\texttt{{{ln}}}", font_size=font_size, color=WHITE) for ln in lines])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    box = panel((width or rows.width + 0.8), rows.height + 0.6, color=P.PSYCHE)
    rows.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    g = VGroup(box, rows)
    g.rows = rows
    return g


def heart(height: float = 1.4, color=EXC) -> VMobject:
    """A heart, from the usual parametric curve."""
    t = np.linspace(0, 2 * np.pi, 120)
    pts = np.column_stack([16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t),
                           np.zeros_like(t)])
    h = VMobject(color=color, stroke_width=3, fill_color=color, fill_opacity=0.55).set_points_smoothly(list(pts))
    return h.scale_to_fit_height(height)


def unit(text: str = "", radius: float = 0.42, color=VOLT, font_size: int = 26) -> VGroup:
    """A neuron drawn as a circle, with an optional name inside."""
    c = Circle(radius=radius, color=color, stroke_width=3, fill_color="#111722", fill_opacity=1)
    g = VGroup(c)
    if text:
        g.add(label(text, font_size=font_size, color=color).move_to(c))
    return g


def excite(a, b, color=EXC, buff: float = 0.08, width: float = 4) -> Arrow:
    """An excitatory connection from ``a`` to ``b``: an arrow."""
    return Arrow(a, b, color=color, stroke_width=width, buff=buff, max_tip_length_to_length_ratio=0.18)


def inhibit(a, b, color=INH, buff: float = 0.1, width: float = 4) -> VGroup:
    """An inhibitory connection from ``a`` to ``b``: a line ending in a round knob."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = (b - a) / max(np.linalg.norm(b - a), 1e-9)
    end = b - d * (buff + 0.1)
    return VGroup(Line(a + d * buff, end, color=color, stroke_width=width),
                  Dot(end, radius=0.11, color=color))


def trace(ax, t, v, color, width: float = 3.5):
    """A curve on ``ax`` (a thin wrapper, so that scenes read as 'a trace')."""
    return curve(ax, t, v, color, stroke_width=width)


def picture(arr, height: float = 4.0, smooth: bool = False) -> ImageMobject:
    """A 2-D array of values in 0..1 as a grey image (0 black, 1 white)."""
    a = np.clip(np.asarray(arr, float), 0.0, 1.0)
    rgb = np.repeat((a * 255).astype(np.uint8)[:, :, None], 3, axis=2)
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.scale_to_fit_height(height)
    return img


def grey_strip(values, width: float = 6.0, height: float = 0.9, lo: float = 0.0, hi: float = 1.0) -> VGroup:
    """A row of grey bars, one per value (``lo`` black, ``hi`` white): a light pattern drawn as light."""
    v = np.asarray(values, float)
    w = width / len(v)
    g = VGroup()
    for i, x in enumerate(v):
        shade = float(np.clip((x - lo) / (hi - lo), 0, 1))
        col = ManimColor.from_rgb((shade, shade, shade))
        g.add(Rectangle(width=w * 1.02, height=height, stroke_width=0, fill_color=col, fill_opacity=1).move_to(
            [(i + 0.5) * w - width / 2, 0, 0]))
    return g


def light_strip(values, width: float = 6.0, height: float = 0.9, lo: float = 0.2, hi: float = 3.0,
                smooth: bool = False) -> ImageMobject:
    """A light pattern drawn as light: one grey level per value (``lo`` black, ``hi`` white), as an image, so
    that neighbouring levels meet without seams.  ``smooth`` interpolates between the values."""
    v = np.asarray(values, float)
    cols = np.interp(np.linspace(0, len(v) - 1, 8 * len(v)), np.arange(len(v)), v) if smooth else np.repeat(v, 8)
    img = picture(np.tile((cols - lo) / (hi - lo), (4, 1)), height=height, smooth=smooth)
    img.stretch_to_fit_width(width)
    img.stretch_to_fit_height(height)
    return img
