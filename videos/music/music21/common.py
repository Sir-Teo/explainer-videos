"""Helpers shared by the scenes of Part 21 ("Form")."""

from __future__ import annotations

import numpy as np

from explainer.music.chordviz import tex  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.melodyviz import columns, roll  # noqa: F401
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED  # noqa: F401

from .compute import BEAT, CACHE, CLIPS, load  # noqa: F401

PART = 21
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
DIM = "#3A4250"
SEC_C = {"A": "#F5C542", "B": "#F472B6", "C": "#7DD3FC", "D": "#A3E635", "A1": "#E8A23A", "A2": "#C77B3F", "A'": "#E8A23A"}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def ssm_image(S, size: float = 4.0, lo=(14, 17, 23), hi=(245, 197, 66)) -> ImageMobject:
    """A self-similarity matrix as a picture: dark where moments differ, gold where they are alike; time runs down
    and to the right, the first moment at the top left."""
    S = np.asarray(S, dtype=float)
    lo_, hi_ = np.percentile(S, 5), np.percentile(S, 99)          # stretch the contrast for the eye
    a = np.clip((S - lo_) / (hi_ - lo_ + 1e-9), 0.0, 1.0) ** 1.5
    rgb = np.zeros(S.shape + (3,), dtype=np.uint8)
    for k in range(3):
        rgb[..., k] = (lo[k] + (hi[k] - lo[k]) * a).astype(np.uint8)
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.height = size
    return img


def strip(starts, names, total: float, width: float = 4.0, height: float = 0.32, colors=None, font_size: int = 18) -> VGroup:
    """Sections as coloured blocks along a time axis of ``total`` beats."""
    colors = colors or SEC_C
    g = VGroup()
    edges = list(starts) + [total]
    for k, n in enumerate(names):
        a, b = edges[k], edges[k + 1]
        w = width * (b - a) / total
        r = Rectangle(width=max(w - 0.03, 0.02), height=height, stroke_width=0, fill_color=colors.get(n.split(":")[0].split(" ")[0], GREY_B), fill_opacity=0.85)
        r.move_to([-width / 2 + width * a / total + w / 2, 0, 0])
        t = label(n, font_size=font_size, color=BLACK).move_to(r)
        if t.width > r.width - 0.05:
            t.scale_to_fit_width(max(r.width - 0.05, 0.05))
        g.add(VGroup(r, t))
    return g


def curve(values, width: float = 6.0, height: float = 1.2, color=TUNE) -> VGroup:
    """A curve of values in [0, 1], left to right."""
    v = np.asarray(values, dtype=float)
    xs = np.linspace(-width / 2, width / 2, len(v))
    pts = [np.array([x, -height / 2 + height * y, 0]) for x, y in zip(xs, v)]
    ln = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners(pts)
    base = Line([-width / 2, -height / 2, 0], [width / 2, -height / 2, 0], color=DIM, stroke_width=1.5)
    g = VGroup(base, ln)
    g.x = lambda i: -width / 2 + width * i / (len(v) - 1) + g.get_center()[0] - 0.0
    return g


def tick(g, i, n, color=EAR, height: float = 1.4):
    """A vertical mark at index i of n along a curve ``g`` (built by ``curve``)."""
    x = g[0].get_left()[0] + g[0].width * i / (n - 1)
    return Line([x, g[0].get_y() - 0.1, 0], [x, g[0].get_y() + height, 0], color=color, stroke_width=2.5)


def diag_cursor(snd, img, beats: int, beat: float, start: float = 0.0, color=WHITE):
    """A ring that travels down the diagonal of a self-similarity picture with the sound: the moment now playing."""
    r = Circle(radius=0.12, color=color, stroke_width=3)
    size = img.height

    def upd(m, t):
        b = min(max((t - start) / beat, 0.0), beats)
        m.move_to([img.get_left()[0] + size * b / beats, img.get_top()[1] - size * b / beats, 0])

    snd.drive(r, upd)
    return r
