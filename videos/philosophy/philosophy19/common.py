"""Helpers shared by the scenes of Part 19 ("Life")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import evo as Ev  # noqa: F401

from .compute import load  # noqa: F401

PART = 19
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
GENE = "#5EE6D0"      # genes and replicators
ORG = "#F2A65A"       # organisms
GROUP = "#6FB7FF"     # groups
ALT = "#F28EC2"       # altruists, cooperators
SELF = "#9AA5B8"      # selfish types, defectors


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)


def rows_table(rows, x_label=-6.4, x_text=-3.2, top=1.7, gap=0.42, label_size=22, text_size=21, width=9.6):
    g = VGroup()
    for a, b, c in rows:
        x = label(a, font_size=label_size, color=c)
        y = wrapped_label(b, width, text_size, WHITE)
        x.move_to([x_label + x.width / 2, top - x.height / 2, 0])
        y.move_to([x_text + y.width / 2, top - y.height / 2, 0])
        g.add(VGroup(x, y))
        top -= max(x.height, y.height) + gap
    return g


def series_plot(ax, ys, color, xs=None, width=3) -> VMobject:
    xs = xs if xs is not None else list(range(len(ys)))
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [ax.c2p(x, y) for x, y in zip(xs, ys)])


class Simplex(VGroup):
    """An equilateral triangle for three-strategy frequencies; ``p2c(x)`` maps (x1, x2, x3) to the plane."""

    def __init__(self, names, center=ORIGIN, side=4.0, colors=(WHITE, WHITE, WHITE), font_size=20):
        super().__init__()
        h = side * np.sqrt(3) / 2
        c = np.array(center, float)
        self.v = [c + np.array([0, 2 * h / 3, 0]), c + np.array([-side / 2, -h / 3, 0]),
                  c + np.array([side / 2, -h / 3, 0])]
        self.tri = Polygon(*self.v, color=GREY_B, stroke_width=2.5)
        self.add(self.tri)
        offs = [UP * 0.3, DL * 0.3, DR * 0.3]
        self.names = VGroup(*[label(n, font_size=font_size, color=col).move_to(p + o)
                              for n, p, o, col in zip(names, self.v, offs, colors)])
        self.add(self.names)

    def p2c(self, x):
        x = np.array(x, float)
        return x[0] * self.v[0] + x[1] * self.v[1] + x[2] * self.v[2]

    def path(self, traj, color, width=2.5) -> VMobject:
        return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([self.p2c(x) for x in traj])


def field_rgba(arr, color=GENE, scale: float = 1.0) -> np.ndarray:
    """A 2D array in [0, scale] as an upscaled RGBA pixel array, dark to ``color``."""
    a = np.clip(np.array(arr, float) / scale, 0, 1)
    rgb = np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)], float)
    bg = np.array([12, 16, 22], float)
    img = (bg[None, None, :] * (1 - a[..., None]) + rgb[None, None, :] * a[..., None]).astype(np.uint8)
    rep = max(1, int(round(480 / a.shape[0])))
    img = np.kron(img, np.ones((rep, rep, 1), dtype=np.uint8))
    return np.concatenate([img, np.full(img.shape[:2] + (1,), 255, np.uint8)], axis=2)


def field_image(arr, size: float, color=GENE, scale: float = 1.0) -> ImageMobject:
    """A 2D array in [0, scale] as an image, dark to ``color``."""
    m = ImageMobject(field_rgba(arr, color, scale))
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    m.height = size
    return m
