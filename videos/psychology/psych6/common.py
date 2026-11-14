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
