"""Helpers shared by the scenes of Part 62 of *Psychology, Built* ("The Dissertation")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 62

# one meaning per colour, for this part
PERSON = "#F2C14E"  # the individual: you, a participant, one node
CROWD = "#7EC8F5"  # the others, the group, the majority
AUTH = "#EF6F6C"  # authority, pressure, the wrong answer
MODEL = "#B39DDB"  # what Psyche computes
GOOD = "#5BD18B"  # help, dissent, the right answer
LOST = "#EF6F6C"
YOU = "#F2C14E"  # the viewer
OFF = "#3A3F48"  # not (yet) in, not adopted
G = "#F2C14E"
SYMP = "#7EC8F5"  # symptoms, the clinic
CARE = "#6F9BF2"  # care, help
DATA = P.ARCHIVE
KANT = P.KANT


def pct(x: float, digits: int = 0) -> str:
    return rf"{100 * x:.{digits}f}\%"


def spct(x: float) -> str:
    """A share as narration reads it: "45 percent"."""
    return f"{100 * x:.0f} percent"


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


def rows_of(items, width: float, font_size: int = 30, buff: float = 0.34) -> VGroup:
    """Lines of text, each (text, colour), wrapped to ``width`` and stacked."""
    return VGroup(*[wrapped_label(t, width, font_size, c) for t, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def bounds(ax):
    """The data range of an axis pair (corner axes store their ranges shifted to start at zero)."""
    ox, oy = getattr(ax, "_off", (0.0, 0.0))
    return (float(ax.x_range[0] + ox), float(ax.x_range[1] + ox)), (float(ax.y_range[0] + oy), float(ax.y_range[1] + oy))


def scatter(ax, x, y, color, radius: float = 0.04, opacity: float = 0.85) -> VGroup:
    (x0, x1), (y0, y1) = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1) & np.isfinite(x) & np.isfinite(y)
    return VGroup(*[Dot(ax.c2p(float(a), float(b)), radius=radius, color=color, fill_opacity=opacity)
                    for a, b in zip(x[keep], y[keep])])


def curve_in(ax, x, y, color, stroke_width=3, smooth=False):
    """A curve with the points outside the axes' x range left out."""
    (x0, x1), _ = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1)
    return curve(ax, x[keep], y[keep], color, stroke_width=stroke_width, smooth=smooth)


def bars(ax, xs, ys, color, width: float = 0.6, opacity: float = 0.85) -> VGroup:
    """Vertical bars from zero (or the axis floor) to ``ys`` at ``xs``, in data units."""
    (_, _), (y0, _) = bounds(ax)
    out = VGroup()
    colors = color if isinstance(color, (list, tuple)) else [color] * len(xs)
    for x, y, c in zip(xs, ys, colors):
        lo, hi = ax.c2p(float(x), max(y0, 0.0)), ax.c2p(float(x), float(y))
        w = abs(ax.c2p(float(x) + width / 2, 0)[0] - ax.c2p(float(x) - width / 2, 0)[0])
        out.add(Rectangle(width=w, height=max(abs(hi[1] - lo[1]), 1e-3), stroke_width=0, fill_color=c,
                          fill_opacity=opacity).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
    return out


def word_chip(word: str, color=CROWD, font_size=26, width=None) -> VGroup:
    """A word in a rounded box."""
    t = label(word, font_size=font_size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=width or t.width + 0.3, height=t.height + 0.25,
                           stroke_color=color, stroke_width=2, fill_color=BLACK, fill_opacity=0.6)
    return VGroup(box, t.move_to(box))




def heatmap(R, names=None, cell: float = 0.55, font_size: int = 16, values: bool = True, lo: float = 0.0,
            hi: float = 1.0, name_color=GREY_A) -> VGroup:
    """A correlation matrix as coloured squares (dark for 0, gold for 1, red below 0), with optional values and
    names on the left and top.  Returns VGroup(cells, labels) with ``.cells`` indexed [i][j]."""
    R = np.asarray(R, float)
    p = len(R)
    cells = VGroup()
    grid = []
    for i in range(p):
        row = []
        for j in range(p):
            r = float(R[i, j])
            if r >= 0:
                t = min(1.0, (r - lo) / (hi - lo))
                col = interpolate_color(ManimColor("#14181F"), ManimColor(G), t)
            else:
                col = interpolate_color(ManimColor("#14181F"), ManimColor(LOST), min(1.0, -r / 0.3))
            sq = Square(side_length=cell, stroke_width=1, stroke_color=BLACK, fill_color=col, fill_opacity=1)
            sq.move_to([j * cell, -i * cell, 0])
            g_ = VGroup(sq)
            if values and i != j:
                g_.add(label(f"{r:.2f}".replace("0.", ".", 1) if r >= 0 else f"{r:.2f}".replace("-0.", "-.", 1),
                             font_size=font_size, color=BLACK if r > 0.55 else WHITE).move_to(sq))
            cells.add(g_)
            row.append(g_)
        grid.append(row)
    labels = VGroup()
    if names:
        for i, nm in enumerate(names):
            labels.add(label(nm, font_size=font_size + 2, color=name_color).next_to(grid[i][0], LEFT, buff=0.12))
    out = VGroup(cells, labels)
    out.cells = grid
    return out


def area_under(ax, x, y, color, opacity: float = 0.5) -> Polygon:
    """The region between a curve, given as points, and y = 0, as a filled polygon."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    pts = [ax.c2p(float(x[0]), 0.0)] + [ax.c2p(float(a), float(b)) for a, b in zip(x, y)] + [ax.c2p(float(x[-1]), 0.0)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


BACKGROUND = config.background_color
THRESH = "#F2C14E"  # voxels a rule declares active
BAD = "#EF6F6C"  # false positives

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


# ----------------------------------------------------------------------------------------------------------------
# Section helpers: a chapter card, a column of lines revealed by bookmarks, and labelled chips
# ----------------------------------------------------------------------------------------------------------------
NUMS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen")


def card_section(scene, n: int, title: str, question: str, scale=("person",), marr=("what",)):
    card = chapter_card(n, title, question, lit=(), part=PART, scale=scale, marr=marr)
    plain = title.replace("\\ ", " ").replace("\\", "")
    with scene.voiceover(f"Chapter {NUMS[n - 1]}. {plain}."):
        scene.play(FadeIn(card, shift=UP * 0.2))
    scene.clear_scene()


def rows_section(scene, title: str, items, narration: str, width: float = 12.4, font_size: int = 22,
                 buff: float = 0.42, tag=None, extra=None):
    """A heading and lines revealed one per bookmark (a, b, c, ...); ``extra`` mobjects appear with the heading."""
    head = heading(title)
    rows = rows_of(items, width, font_size, buff).move_to([0, -0.3, 0])
    with scene.voiceover(narration) as vo:
        scene.play(FadeIn(head), *([FadeIn(tag)] if tag is not None else []), *([FadeIn(extra)] if extra else []))
        for m, r in zip("abcdefgh", rows):
            vo.wait_until(m)
            scene.play(FadeIn(r, shift=RIGHT * 0.15))
    scene.clear_scene()


def chips_section(scene, title: str, items, narration: str, chip_w: float = 3.8, text_w: float = 8.2,
                  font_size: int = 21, buff: float = 0.42, foot=None, tag=None):
    """A heading and (name, explanation, colour) rows revealed one per bookmark; an optional footer line."""
    head = heading(title)
    rows = VGroup()
    for name, what, col in items:
        rows.add(VGroup(word_chip(name, col, font_size, width=chip_w), wrapped_label(what, text_w, font_size - 1, WHITE))
                 .arrange(RIGHT, buff=0.4))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff).move_to([0, 0.1 if foot else -0.2, 0])
    f = wrapped_label(foot, 12.0, 21, YOU).to_edge(DOWN, buff=0.6) if foot else None
    with scene.voiceover(narration) as vo:
        scene.play(FadeIn(head), *([FadeIn(tag)] if tag is not None else []))
        for m, r in zip("abcdefgh", rows):
            vo.wait_until(m)
            scene.play(FadeIn(r, shift=RIGHT * 0.15))
        if f is not None:
            scene.play(FadeIn(f))
    scene.clear_scene()
