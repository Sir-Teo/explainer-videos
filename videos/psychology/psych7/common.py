"""Helpers shared by the scenes of Part 7 of *Psychology, Built* ("The Brain")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 7

# one meaning per colour, for this part
FRONTAL = "#F28FB8"
PARIETAL = "#7EC8F5"
TEMPORAL = "#5BD18B"
OCCIPITAL = "#B48EF0"
CEREBELLUM = "#F2A65A"
STEM = "#8FA3BF"
DEEP = "#E8D27A"  # structures under the surface
LESION = P.ERR  # damage
SPARED = "#5BD18B"  # a task that survives
MODEL = "#5BD18B"  # what Psyche computes
DATA = "#F2A65A"  # what was measured, a historical fact
VOLT = "#E8EDF2"  # neutral
THRESH = P.ACCENT
KANT = P.KANT

LOBES = {
    "frontal": (FRONTAL, [(-1.0, -0.05), (-0.95, 0.25), (-0.75, 0.5), (-0.45, 0.66), (-0.12, 0.72), (-0.05, 0.4),
                          (-0.12, 0.1), (-0.3, -0.05), (-0.55, -0.12), (-0.8, -0.18)]),
    "parietal": (PARIETAL, [(-0.12, 0.72), (0.2, 0.72), (0.5, 0.62), (0.68, 0.45), (0.6, 0.2), (0.4, 0.08), (0.1, 0.08),
                            (-0.12, 0.1), (-0.05, 0.4)]),
    "occipital": (OCCIPITAL, [(0.68, 0.45), (0.85, 0.25), (0.92, 0.0), (0.85, -0.2), (0.68, -0.3), (0.55, -0.15),
                              (0.5, 0.05), (0.6, 0.2)]),
    "temporal": (TEMPORAL, [(-0.55, -0.12), (-0.3, -0.05), (-0.12, 0.1), (0.1, 0.08), (0.4, 0.08), (0.5, 0.05),
                            (0.55, -0.15), (0.45, -0.33), (0.2, -0.42), (-0.1, -0.45), (-0.4, -0.4), (-0.58, -0.28)]),
}


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


def big_number(value: str, caption: str, color, font_size: int = 72, width: float = 4.2, cap_size: int = 26) -> VGroup:
    return VGroup(label(value, font_size=font_size, color=color), wrapped_label(caption, width, cap_size, GREY_A)).arrange(
        DOWN, buff=0.18)


def brain_side(width: float = 6.0, fill: float = 0.55, lit=None) -> VGroup:
    """The left hemisphere seen from the side, front to the left: four lobes, the cerebellum and the brainstem.
    ``.lobe[name]`` are the pieces; lobes not in ``lit`` (when given) are drawn dim."""
    k = width / 2.0

    def pts(seq):
        return [np.array([x * k, y * k, 0.0]) for x, y in seq]

    g = VGroup()
    g.lobe = {}
    stem = Polygon(*pts([(0.16, -0.4), (0.24, -0.86), (0.4, -0.86), (0.4, -0.42)]), color=STEM, stroke_width=3,
                   fill_color=STEM, fill_opacity=fill).round_corners(0.04 * k)
    cb = Ellipse(width=0.62 * k, height=0.36 * k, color=CEREBELLUM, stroke_width=3, fill_color=CEREBELLUM,
                 fill_opacity=fill).move_to([0.6 * k, -0.5 * k, 0])
    stripes = VGroup(*[Arc(radius=0.16 * k + 0.035 * k * i, start_angle=PI * 1.15, angle=PI * 0.7, color=BACKGROUND,
                           stroke_width=1.5).move_arc_center_to([0.6 * k, -0.36 * k, 0]) for i in range(4)])
    g.add(stem, cb, stripes)
    g.lobe["brainstem"], g.lobe["cerebellum"] = stem, VGroup(cb, stripes)
    for name, (col, seq) in LOBES.items():
        on = lit is None or name in lit
        piece = Polygon(*pts(seq), color=BACKGROUND, stroke_width=4, fill_color=col,
                        fill_opacity=fill if on else 0.12).round_corners(0.035 * k)
        g.add(piece)
        g.lobe[name] = piece
    g.k = k
    return g


def at(brain, x: float, y: float) -> np.ndarray:
    """A point in the coordinates of :func:`brain_side` (x from -1 at the front to 1 at the back)."""
    c = brain.lobe["parietal"].get_center() - np.array([0.21 * brain.k, 0.36 * brain.k, 0])
    return c + np.array([x * brain.k, y * brain.k, 0.0])


def brain_medial(width: float = 6.2, center=ORIGIN) -> VGroup:
    """One hemisphere cut down the middle, front to the left: the outline, the corpus callosum, the thalamus,
    the hypothalamus, the basal ganglia (dashed: deeper than the cut), the hippocampus and the amygdala.
    The pieces are attributes; ``.at(x, y)`` gives a point in the same coordinates as :func:`brain_side`."""
    k = width / 2.0
    c0 = np.asarray(center, float)

    def at_(x, y):
        return c0 + np.array([x * k, y * k, 0.0])

    outline = [(-1.0, -0.05), (-0.95, 0.25), (-0.75, 0.5), (-0.45, 0.66), (-0.12, 0.72), (0.2, 0.72), (0.5, 0.62),
               (0.68, 0.45), (0.85, 0.25), (0.92, 0.0), (0.85, -0.2), (0.68, -0.3), (0.45, -0.33), (0.2, -0.42),
               (-0.1, -0.45), (-0.4, -0.4), (-0.58, -0.28), (-0.8, -0.18)]
    g = VGroup()
    g.hemi = Polygon(*[at_(x, y) for x, y in outline], color=GREY_B, stroke_width=3, fill_color="#1A2130",
                     fill_opacity=1).round_corners(0.04 * k)
    g.stem = Polygon(at_(0.1, -0.2), at_(0.2, -0.86), at_(0.36, -0.86), at_(0.3, -0.2), color=STEM, stroke_width=3,
                     fill_color=STEM, fill_opacity=0.45).round_corners(0.025 * k)
    g.cb = Ellipse(width=0.62 * k, height=0.36 * k, color=CEREBELLUM, stroke_width=3, fill_color=CEREBELLUM,
                   fill_opacity=0.35).move_to(at_(0.6, -0.5))
    g.callosum = ArcBetweenPoints(at_(-0.45, 0.2), at_(0.4, 0.2), angle=-PI * 0.55, color=VOLT, stroke_width=12)
    g.thalamus = Ellipse(width=0.34 * k, height=0.2 * k, color=DEEP, stroke_width=3, fill_color=DEEP,
                         fill_opacity=0.6).move_to(at_(0.05, 0.08))
    g.hypothalamus = Dot(at_(-0.14, -0.06), radius=0.04 * k, color=LESION)
    g.basal = DashedVMobject(Ellipse(width=0.42 * k, height=0.26 * k, color=FRONTAL, stroke_width=3).move_to(
        at_(-0.25, 0.14)), num_dashes=28)
    g.hippocampus = ArcBetweenPoints(at_(-0.12, -0.24), at_(0.34, -0.16), angle=PI * 0.35, color=TEMPORAL,
                                     stroke_width=11)
    g.amygdala = Dot(at_(-0.22, -0.24), radius=0.042 * k, color=DATA)
    g.shell = VGroup(g.stem, g.cb, g.hemi)
    g.add(g.shell)
    g.at = at_
    return g


def lesion_mark(center, radius: float = 0.28, color=LESION) -> VGroup:
    """A lesion: a dark red blot with a ragged edge."""
    g = np.random.default_rng(int(abs(center[0] * 100) + abs(center[1] * 10)))
    n = 14
    pts = [np.asarray(center) + radius * (0.8 + 0.35 * g.random()) * np.array([np.cos(a), np.sin(a), 0])
           for a in np.linspace(0, TAU, n, endpoint=False)]
    return VGroup(VMobject(color=color, stroke_width=2, fill_color=color, fill_opacity=0.85).set_points_smoothly(
        pts + [pts[0]]))


def module_box(text: str, color=VOLT, width: float = 2.3, height: float = 0.8, font_size: int = 26) -> VGroup:
    """One box of a box-and-arrow diagram."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15, color=color, stroke_width=3,
                           fill_color="#111722", fill_opacity=1)
    t = wrapped_label(text, width - 0.3, font_size, color)
    if t.height > height - 0.15:
        t.scale_to_fit_height(height - 0.15)
    g = VGroup(box, t.move_to(box))
    g.box = box
    return g


def link(a, b, color=GREY_B, width: float = 4) -> Arrow:
    return Arrow(a, b, color=color, stroke_width=width, buff=0.08, max_tip_length_to_length_ratio=0.15)


def score_bar(value: float, color, width: float = 1.6, height: float = 0.32) -> VGroup:
    """A task's score from 0 to 1 as a filled bar."""
    back = Rectangle(width=width, height=height, color=GREY_D, stroke_width=2)
    fill = Rectangle(width=max(width * value, 0.001), height=height, stroke_width=0, fill_color=color, fill_opacity=0.9)
    fill.align_to(back, LEFT)
    return VGroup(back, fill)


def picture(arr, height: float = 4.0, smooth: bool = False, lo: float = 0.0, hi: float = 1.0, tint=None) -> ImageMobject:
    """A 2-D array as an image: grey from ``lo`` (black) to ``hi`` (white), or shades of ``tint``."""
    a = np.clip((np.asarray(arr, float) - lo) / (hi - lo), 0.0, 1.0)
    if tint is None:
        rgb = np.repeat((a * 255).astype(np.uint8)[:, :, None], 3, axis=2)
    else:
        col = np.array(ManimColor(tint).to_rgb())
        base = np.array(ManimColor(BACKGROUND).to_rgb())
        rgb = ((base[None, None, :] * (1 - a[..., None]) + col[None, None, :] * a[..., None]) * 255).astype(np.uint8)
    img = ImageMobject(rgb[::-1])  # row 0 of the array at the bottom, as on a plot
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.scale_to_fit_height(height)
    return img
