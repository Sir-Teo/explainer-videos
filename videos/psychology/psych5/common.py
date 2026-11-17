"""Helpers shared by the scenes of Part 5 of *Psychology, Built* ("The Neuron")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 5

# one meaning per colour, for this part
VOLT = "#E8EDF2"  # the membrane potential
NA = "#F28FB8"  # sodium: its ions, its conductance, its current
K = "#7EC8F5"  # potassium
LEAK = "#8FA3BF"  # the leak, and anything passive
GATE = {"m": "#F2C14E", "h": "#B48EF0", "n": "#7EC8F5"}  # the three gates
THRESH = P.ACCENT  # a threshold, a stimulus, the thing to look at
MODEL = "#5BD18B"  # what the equations compute
DATA = "#F2A65A"  # what was measured
BAD = P.ERR
KANT = P.KANT


def r2(x: float) -> str:
    """A number to two places without the leading zero: ``.22``; ``1.00`` stays."""
    s = f"{x:.2f}"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s


def pct(x: float, digits: int = 0) -> str:
    return rf"{100 * x:.{digits}f}\%"


def mv(x: float, digits: int = 0) -> str:
    """A voltage in millivolts with its sign, as TeX: ``$-65$ mV``."""
    return rf"${x:+.{digits}f}$ mV".replace("+", "+").replace("-", "-")


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


def membrane(width: float = 9.0, y: float = 0.0, thickness: float = 0.5, color=LEAK) -> VGroup:
    """A strip of membrane seen edge on: two rows of lipid heads with their tails between."""
    n = int(width / 0.28)
    heads = VGroup()
    tails = VGroup()
    for i in range(n):
        x = -width / 2 + (i + 0.5) * width / n
        for s in (1, -1):
            heads.add(Circle(radius=0.085, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to(
                [x, y + s * thickness / 2, 0]))
            tails.add(Line([x, y + s * (thickness / 2 - 0.09), 0], [x, y + s * 0.03, 0], color=color, stroke_width=1.5,
                           stroke_opacity=0.6))
    g = VGroup(tails, heads)
    g.top, g.bottom = y + thickness / 2, y - thickness / 2
    return g


def channel(x: float, y: float = 0.0, color=K, height: float = 0.8, gap: float = 0.16, is_open: bool = True) -> VGroup:
    """A channel through the membrane at ``x``: two walls, with a bar across the pore when it is shut."""
    walls = VGroup(*[RoundedRectangle(width=0.16, height=height, corner_radius=0.06, stroke_width=0, fill_color=color,
                                      fill_opacity=0.95).move_to([x + s * (gap / 2 + 0.08), y, 0]) for s in (-1, 1)])
    g = VGroup(walls)
    if not is_open:
        g.add(Line([x - gap / 2, y, 0], [x + gap / 2, y, 0], color=color, stroke_width=6))
    return g


def ions(n: int, box, color, rng, radius: float = 0.07) -> VGroup:
    """``n`` ions scattered in the rectangle ``box`` = (x0, x1, y0, y1)."""
    x0, x1, y0, y1 = box
    pts = np.column_stack([rng.uniform(x0, x1, n), rng.uniform(y0, y1, n)])
    return VGroup(*[Dot([x, y, 0], radius=radius, color=color) for x, y in pts])


def neuron_drawing(scale: float = 1.0, color=VOLT) -> VGroup:
    """A neuron in outline: dendrites, cell body, axon, terminals.  Parts are attributes for labelling."""
    soma = Circle(radius=0.45, color=color, stroke_width=3, fill_color="#111722", fill_opacity=1)
    rng = np.random.default_rng(5)
    dend = VGroup()
    for ang in (2.2, 2.6, 3.0, 3.5, 3.9):
        base = 0.45 * np.array([np.cos(ang), np.sin(ang), 0])
        mid = base + 1.1 * np.array([np.cos(ang), np.sin(ang), 0])
        dend.add(Line(base, mid, color=color, stroke_width=3))
        for d in (-0.5, 0.45):
            tip = mid + 0.75 * np.array([np.cos(ang + d), np.sin(ang + d), 0]) * rng.uniform(0.8, 1.1)
            dend.add(Line(mid, tip, color=color, stroke_width=2))
    axon = Line([0.45, 0, 0], [4.6, 0, 0], color=color, stroke_width=3)
    hillock = Polygon([0.4, 0.18, 0], [0.4, -0.18, 0], [0.8, 0, 0], color=color, stroke_width=0, fill_color=color,
                      fill_opacity=1)
    term = VGroup()
    for d in (-0.5, 0.0, 0.5):
        end = np.array([4.6, 0, 0]) + 0.7 * np.array([np.cos(d), np.sin(d), 0])
        term.add(Line([4.6, 0, 0], end, color=color, stroke_width=2), Dot(end, radius=0.08, color=color))
    g = VGroup(dend, axon, hillock, term, soma).scale(scale)
    g.dend, g.axon, g.hillock, g.term, g.soma = dend, axon, hillock, term, soma
    return g


def raster(trains, x0: float, y0: float, width: float, row: float = 0.3, color=VOLT, t_end: float = 1.0,
           tick: float = 0.2) -> VGroup:
    """Spike trains as rows of ticks: time runs left to right over ``width``."""
    g = VGroup()
    for i, tr in enumerate(trains):
        y = y0 - i * row
        g.add(VGroup(*[Line([x0 + width * t / t_end, y - tick / 2, 0], [x0 + width * t / t_end, y + tick / 2, 0],
                            color=color, stroke_width=2) for t in tr]))
    return g
