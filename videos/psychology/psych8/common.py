"""Helpers shared by the scenes of Part 8 of *Psychology, Built* ("Reading the Brain")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 8

# one meaning per colour, for this part
VOLT = "#E8EDF2"  # a recorded trace, neutral
SPIKE = "#F2C14E"  # spikes, single cells
EEGC = "#7EC8F5"  # potentials on the scalp
BLOOD = "#F28FB8"  # the BOLD signal
MODEL = "#5BD18B"  # what Psyche computes, a fitted line
DATA = "#F2A65A"  # what was measured, a historical fact
NOISE = "#8FA3BF"  # noise, and things that are not there
BAD = P.ERR  # a false positive, a mistake
THRESH = P.ACCENT
KANT = P.KANT


def r2(x: float) -> str:
    s = f"{x:.2f}"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s


def pct(x: float, digits: int = 0) -> str:
    return rf"{100 * x:.{digits}f}\%"


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


_HOT = np.array([[0.04, 0.05, 0.08], [0.55, 0.10, 0.10], [0.95, 0.45, 0.12], [1.0, 0.86, 0.35], [1.0, 1.0, 0.92]])


def _rgb(a: np.ndarray, anchors: np.ndarray) -> np.ndarray:
    """Values in [0, 1] to colours along a ramp of anchor colours."""
    x = np.clip(a, 0, 1) * (len(anchors) - 1)
    i = np.minimum(x.astype(int), len(anchors) - 2)
    f = (x - i)[..., None]
    return anchors[i] * (1 - f) + anchors[i + 1] * f


def heat(arr, height: float = 3.6, lo: float = 0.0, hi: float = 1.0, mask=None, center=ORIGIN, grey: bool = False,
         smooth: bool = False) -> Group:
    """A 2-D array as an image on a dark-to-hot ramp (or grey), with the brain's outline when ``mask`` is given:
    voxels outside the mask take the background colour.  Row 0 of the array is drawn at the bottom."""
    a = (np.asarray(arr, float) - lo) / (hi - lo)
    ramp = np.array([[0.04, 0.05, 0.08], [1.0, 1.0, 1.0]]) if grey else _HOT
    rgb = _rgb(a, ramp)
    if mask is not None:
        base = np.array(ManimColor(BACKGROUND).to_rgb())
        rgb = np.where(np.asarray(mask, bool)[..., None], rgb, base[None, None, :])
    img = ImageMobject((rgb[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.scale_to_fit_height(height).move_to(center)
    g = Group(img)
    if mask is not None:
        g.add(Ellipse(width=0.92 * height, height=0.96 * height, color=GREY_B, stroke_width=2).move_to(center))
    return g


def hits_map(hit, brain_mask, truth=None, height: float = 3.0, center=ORIGIN, color=THRESH) -> Group:
    """The voxels a rule declares active: true ones in ``color``, false ones in red, on the slice's outline."""
    n = np.asarray(hit).shape[0]
    base = np.array(ManimColor(BACKGROUND).to_rgb())
    inside = np.array([0.07, 0.09, 0.13])
    rgb = np.where(np.asarray(brain_mask, bool)[..., None], inside[None, None, :], base[None, None, :])
    good = np.asarray(hit, bool) & (np.asarray(truth) > 0 if truth is not None else True)
    bad = np.asarray(hit, bool) & ~good
    rgb = np.where(good[..., None], np.array(ManimColor(color).to_rgb())[None, None, :], rgb)
    rgb = np.where(bad[..., None], np.array(ManimColor(BAD).to_rgb())[None, None, :], rgb)
    img = ImageMobject((rgb[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.scale_to_fit_height(height).move_to(center)
    g = Group(img, Ellipse(width=0.92 * height, height=0.96 * height, color=GREY_B, stroke_width=2).move_to(center))
    g.unit = height / n
    return g


def fish(width: float = 3.0, color=DATA) -> VGroup:
    """A salmon, schematically."""
    body = Ellipse(width=width * 0.78, height=width * 0.26, color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
    tail = Polygon([width * 0.36, 0, 0], [width * 0.52, width * 0.13, 0], [width * 0.47, 0, 0], [width * 0.52, -width * 0.13, 0],
                   color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
    fin = Polygon([-width * 0.05, width * 0.12, 0], [width * 0.08, width * 0.2, 0], [width * 0.14, width * 0.11, 0], color=color,
                  stroke_width=3, fill_color=color, fill_opacity=0.25)
    eye = Dot([-width * 0.29, width * 0.03, 0], radius=width * 0.016, color=color)
    g = VGroup(body, tail, fin, eye)
    g.head = np.array([-width * 0.27, 0.0, 0.0])  # where its brain is, relative to the centre
    return g


def scanner(width: float = 4.2) -> VGroup:
    """An MRI scanner seen from the end: the magnet's ring and the bed."""
    outer = Circle(radius=width / 2, color=GREY_B, stroke_width=4, fill_color="#141B28", fill_opacity=1)
    bore = Circle(radius=width * 0.27, color=GREY_B, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1)
    bed = Line([-width * 0.25, -width * 0.12, 0], [width * 0.25, -width * 0.12, 0], color=GREY_B, stroke_width=5)
    g = VGroup(outer, bore, bed)
    g.bore = bore
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
