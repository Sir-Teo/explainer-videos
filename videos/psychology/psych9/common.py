"""Helpers shared by the scenes of Part 9 of *Psychology, Built* ("Genes and Evolution")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 9

# one meaning per colour, for this part
GENE = "#5BD18B"  # additive genes (A), and what is inherited
HOME = "#F2A65A"  # the environment a family shares (C)
OWN = "#8FA3BF"  # everything else (E): what makes twins in one home differ
MZC = "#7EC8F5"  # identical twins
DZC = "#F28FB8"  # fraternal twins
VOLT = "#E8EDF2"  # a neutral line
MODEL = "#5BD18B"  # what Psyche computes
DATA = P.ARCHIVE  # a published figure
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


def twin_pair(color, identical: bool = True, height: float = 0.75) -> VGroup:
    """Two little people: the same shade if identical, two shades if fraternal."""
    a = little_person(height, color)
    b = little_person(height, color if identical else interpolate_color(ManimColor(color), ManimColor(WHITE), 0.45))
    return VGroup(a, b).arrange(RIGHT, buff=0.12)


def path_diagram(width: float = 9.0, share_a: str = r"1 \ or \ $\tfrac12$", font_size: int = 28) -> VGroup:
    """The twin design as a path diagram: each twin's score (a square) is caused by additive genes A, the shared
    home C and everything else E (circles); the curved lines say how alike the two twins' causes are.
    ``.twins``, ``.latents`` (A1, C1, E1, A2, C2, E2), ``.arrows``, ``.links`` (A-A, C-C) and ``.link_labels``."""
    half = width / 2
    xs = {"A1": -half + 0.6, "C1": -half * 0.48, "E1": -0.75, "E2": 0.75, "C2": half * 0.48, "A2": half - 0.6}
    cols = {"A": GENE, "C": HOME, "E": OWN}
    latents = VGroup()
    for name, x in xs.items():
        c = cols[name[0]]
        circ = Circle(radius=0.42, color=c, stroke_width=3, fill_color=c, fill_opacity=0.15).move_to([x, 1.2, 0])
        latents.add(VGroup(circ, label(name[0], font_size=font_size + 2, color=c).move_to(circ)))
    twins = VGroup()
    for x, name in ((-half * 0.48, r"twin 1"), (half * 0.48, r"twin 2")):
        box = Square(side_length=1.05, color=VOLT, stroke_width=3, fill_color=PANEL_FILL, fill_opacity=1).move_to([x, -1.1, 0])
        twins.add(VGroup(box, label(name, font_size=font_size - 4, color=VOLT).move_to(box)))
    arrows = VGroup()
    for i, name in enumerate(xs):
        target = twins[0] if name.endswith("1") else twins[1]
        arrows.add(Arrow(latents[i][0].get_bottom(), target[0].get_top() + RIGHT * 0.3 * (list(xs).index(name) % 3 - 1) * (
            1 if name.endswith("1") else -1), buff=0.06, color=cols[name[0]], stroke_width=3, max_tip_length_to_length_ratio=0.12))
    a_link = ArcBetweenPoints(latents[0][0].get_top(), latents[5][0].get_top(), angle=-PI / 2.6, color=GENE, stroke_width=3)
    c_link = ArcBetweenPoints(latents[1][0].get_top(), latents[4][0].get_top(), angle=-PI / 2.6, color=HOME, stroke_width=3)
    a_lab = label(share_a, font_size=font_size, color=GENE).next_to(a_link, UP, buff=0.08)
    c_lab = label(r"1", font_size=font_size, color=HOME).next_to(c_link.point_from_proportion(0.5), DOWN, buff=0.1)
    g = VGroup(latents, twins, arrows, a_link, c_link, a_lab, c_lab)
    g.latents, g.twins, g.arrows, g.links, g.link_labels = latents, twins, arrows, VGroup(a_link, c_link), VGroup(a_lab, c_lab)
    return g
