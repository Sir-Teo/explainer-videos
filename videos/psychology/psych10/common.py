"""Helpers shared by the scenes of Part 10 of *Psychology, Built* ("Chemistry and Clocks")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 10

# one meaning per colour, for this part
CLOCKC = "#7EC8F5"  # the circadian rhythm
SLEEPC = "#B39DDB"  # sleep, and sleep pressure
LIGHTC = "#F2C14E"  # light
HORM = "#F28FB8"  # hormones
DRUG = "#5BD18B"  # a drug's direct effect, and what Psyche computes
OPP = "#F2A65A"  # the opposing process
REMC = "#4DD0C4"  # REM sleep
MODEL = "#5BD18B"
VOLT = "#E8EDF2"  # a neutral line
NOISE = "#8FA3BF"
DATA = P.ARCHIVE  # a published figure
BAD = P.ERR
THRESH = P.ACCENT
KANT = P.KANT


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


def clock_time(h: float) -> str:
    """A clock hour as text: 7.5 -> 7:30."""
    h = float(h) % 24
    m = int(round((h - int(h)) * 60))
    hh = int(h) + (1 if m == 60 else 0)
    return f"{hh % 24}:{m % 60:02d}"


def night_bands(ax, t0: float, t1: float, on: float = 7.0, off: float = 23.0, y0: float = 0.0, y1: float = 1.0,
                day: float = 24.0, color=NOISE, opacity: float = 0.14) -> VGroup:
    """Shaded bands on a time axis (hours) for the dark part of each day."""
    g = VGroup()
    k = int(t0 // day) - 1
    while k * day < t1:
        a, b = k * day + off, (k + 1) * day + on
        a, b = max(a, t0), min(b, t1)
        if b > a:
            p0, p1 = ax.c2p(a, y0), ax.c2p(b, y1)
            g.add(Rectangle(width=abs(p1[0] - p0[0]), height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=color,
                            fill_opacity=opacity).move_to((p0 + p1) / 2))
        k += 1
    return g


def loop_diagram(names, colors, center=ORIGIN, width: float = 9.0, font_size: int = 28, feedback: str = r"turns it down") -> VGroup:
    """Boxes in a row joined by arrows, with a return arrow from the last to the first: a feedback loop.
    ``.boxes``, ``.arrows`` and ``.back`` (the return path with its label)."""
    g = chain(names, colors, width=width, font_size=font_size, height=1.0)
    y = g.boxes.get_bottom()[1] - 0.6
    a, b = g.boxes[-1].get_bottom(), g.boxes[0].get_bottom()
    path = VMobject(color=BAD, stroke_width=4).set_points_as_corners([a, [a[0], y, 0], [b[0], y, 0], b + DOWN * 0.05])
    tip = Triangle(color=BAD, fill_color=BAD, fill_opacity=1).scale(0.1).move_to(b + DOWN * 0.12)
    lab = label(feedback, font_size=font_size - 2, color=BAD).next_to(path, DOWN, buff=0.1)
    out = VGroup(g, VGroup(path, tip, lab))
    out.boxes, out.arrows, out.back = g.boxes, g.arrows, out[1]
    out.move_to(center)
    return out


def clock_icon(radius: float = 0.45, color=CLOCKC, hour: float = 4.0) -> VGroup:
    """A clock face with its hands at ``hour``."""
    face = Circle(radius=radius, color=color, stroke_width=4)
    a = PI / 2 - TAU * (hour % 12) / 12
    b = PI / 2 - TAU * (hour % 1)
    hands = VGroup(Line(ORIGIN, 0.5 * radius * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=5),
                   Line(ORIGIN, 0.78 * radius * np.array([np.cos(b), np.sin(b), 0]), color=color, stroke_width=3))
    ticks = VGroup(*[Line(0.86 * radius * np.array([np.cos(k * TAU / 12), np.sin(k * TAU / 12), 0]),
                          radius * np.array([np.cos(k * TAU / 12), np.sin(k * TAU / 12), 0]), color=color, stroke_width=2)
                     for k in range(12)])
    return VGroup(face, ticks, hands)


def capsule(width: float = 0.9, height: float = 0.36, color=DRUG) -> VGroup:
    """A drug capsule: two halves."""
    body = RoundedRectangle(width=width, height=height, corner_radius=height / 2 - 0.001, color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.25)
    half = RoundedRectangle(width=width / 2, height=height, corner_radius=height / 2 - 0.001, stroke_width=0, fill_color=color,
                            fill_opacity=0.75).align_to(body, LEFT)
    return VGroup(body, half).rotate(25 * DEGREES)


def droplet(height: float = 0.7, color=HORM) -> VMobject:
    """A drop: a hormone in the blood."""
    t = np.linspace(0, TAU, 60)
    pts = [np.array([0.5 * np.sin(u) * np.sin(u / 2) ** 2 * 1.3, -np.cos(u) * 0.5, 0]) for u in t]
    m = VMobject(color=color, stroke_width=3, fill_color=color, fill_opacity=0.35).set_points_smoothly(pts + [pts[0]])
    m.scale_to_fit_height(height)
    return m


def spoken_time(h: float) -> tuple:
    """(hour, minute) of a clock hour, for narration written out by hand and checked against the model."""
    h = float(h) % 24
    m = int(round((h - int(h)) * 60))
    return (int(h) + (1 if m == 60 else 0)) % 24, m % 60


def sleep_bands(ax, t, asleep, y0: float, y1: float, color=SLEEPC, opacity: float = 0.16) -> VGroup:
    """Shaded bands over the stretches of a time axis where ``asleep`` is true."""
    t, a = np.asarray(t, float), np.asarray(asleep, bool)
    g, start = VGroup(), None
    for i in range(len(t)):
        if a[i] and start is None:
            start = t[i]
        if start is not None and (not a[i] or i == len(t) - 1):
            p0, p1 = ax.c2p(start, y0), ax.c2p(t[i], y1)
            if p1[0] > p0[0]:
                g.add(Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=color,
                                fill_opacity=opacity).move_to((p0 + p1) / 2))
            start = None
    return g


def hour_labels(ax, ticks, y0: float, font_size: int = 20) -> VGroup:
    """Clock-hour labels under a time axis in hours since a midnight (the axes helper prints each text only once,
    and a clock repeats)."""
    return VGroup(*[MathTex(f"{int(round(v)) % 24}{{:}}00", font_size=font_size, color=GREY_B).next_to(ax.c2p(v, y0), DOWN,
                                                                                                    buff=0.12)
                    for v in ticks])
