"""Helpers shared by the scenes of Part 12 of *Psychology, Built* ("Signal and Noise")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 12

# one meaning per colour, for this part
NOISEC = "#8FA3BF"  # the noise distribution, blanks
SIGNALC = "#F2A65A"  # the signal distribution, targets
CRIT = P.ACCENT  # the criterion
HIT = "#5BD18B"  # hits and correct rejections
MISS = P.ERR  # misses
FA = "#F28FB8"  # false alarms
MODEL = "#5BD18B"  # a fitted curve, and what Psyche computes
ROCC = "#7EC8F5"  # ROC curves
YOU = "#F2C14E"  # the viewer
DATA = P.ARCHIVE  # a published figure
BAD = P.ERR
THRESH = P.ACCENT
KANT = P.KANT
RIVAL = "#B39DDB"  # rival models


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


def log_axes(x_dec, y_dec, x_length=6.0, y_length=3.6, xlabel="", ylabel="", center=ORIGIN, font_size=20) -> VGroup:
    """Axes in decades: ``x_dec`` and ``y_dec`` are (lo, hi) powers of ten; tick labels read 10^k."""
    return axes(list(x_dec), list(y_dec), x_length=x_length, y_length=y_length,
                xticks=list(range(int(x_dec[0]), int(x_dec[1]) + 1)), yticks=list(range(int(y_dec[0]), int(y_dec[1]) + 1)),
                xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", xlabel=xlabel, ylabel=ylabel,
                center=center, font_size=font_size)


def gauss_pair(ax, d: float, sigma_s: float = 1.0, x0: float = -3.5, x1: float = 5.5, fill: bool = True,
               scale: float = 1.0) -> VGroup:
    """The noise and signal densities on ``ax``: ``.noise`` and ``.signal`` (curves), ``.fills`` (areas)."""
    from scipy import stats
    x = np.linspace(x0, x1, 300)
    yn = scale * stats.norm.pdf(x)
    ys = scale * stats.norm.pdf(x, d, sigma_s)
    noise = curve(ax, x, yn, NOISEC, stroke_width=4)
    signal = curve(ax, x, ys, SIGNALC, stroke_width=4)
    g = VGroup(noise, signal)
    g.noise, g.signal, g.x, g.yn, g.ys = noise, signal, x, yn, ys
    return g


def area_under(ax, x, y, lo: float, hi: float, color, opacity: float = 0.35) -> VGroup:
    """A filled region under a sampled curve between ``lo`` and ``hi``."""
    keep = (x >= lo) & (x <= hi)
    if keep.sum() < 2:
        return VGroup()
    xs, ys = x[keep], y[keep]
    pts = [ax.c2p(float(xs[0]), 0)] + [ax.c2p(float(a), float(b)) for a, b in zip(xs, ys)] + [ax.c2p(float(xs[-1]), 0)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def outcome_table(values=None, font_size: int = 26, width: float = 6.0) -> VGroup:
    """The two-by-two of detection: rows signal / noise, columns yes / no.  ``values`` fills the four cells
    (hit, miss, false alarm, correct rejection); ``.cells[i]``."""
    names = [("hit", HIT), ("miss", MISS), ("false alarm", FA), ("correct rejection", HIT)]
    cw, ch = width / 2, 0.9
    cells = VGroup()
    for i, (name, col) in enumerate(names):
        r, c = divmod(i, 2)
        box = Rectangle(width=cw, height=ch, stroke_color=GREY_C, stroke_width=2, fill_color=col, fill_opacity=0.12)
        box.move_to([c * cw, -r * ch, 0])
        txt = name if values is None else rf"{name}: \ {values[i]}"
        cells.add(VGroup(box, label(txt, font_size=font_size, color=col).move_to(box)))
    head = VGroup(label(r"said ``yes''", font_size=font_size - 2, color=GREY_A).next_to(cells[0], UP, buff=0.15),
                  label(r"said ``no''", font_size=font_size - 2, color=GREY_A).next_to(cells[1], UP, buff=0.15))
    side = VGroup(label(r"signal", font_size=font_size - 2, color=SIGNALC).next_to(cells[0], LEFT, buff=0.2),
                  label(r"noise", font_size=font_size - 2, color=NOISEC).next_to(cells[2], LEFT, buff=0.2))
    g = VGroup(cells, head, side)
    g.cells = cells
    return g

