"""Helpers shared by the scenes of Part 22 ("Analysis")."""

from __future__ import annotations

import numpy as np

from explainer.music.chordviz import tex  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.melodyviz import columns, roll  # noqa: F401
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED  # noqa: F401

from .compute import BEAT, CACHE, CLIPS, load  # noqa: F401

PART = 22
clip = clip_loader(CACHE, CLIPS, item_aliases={"grammar": "progressions", "parsing": "progressions", "recursion": "progressions", "reduction": "kinds"})
WEAK = "#8A93A0"
DIM = "#3A4250"
REGION_C = {"TR": "#F5C542", "DR": "#F472B6", "SR": "#A3E635"}
NAMES = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B"}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def mroll(notes, width=10.0, height=1.8, lo=60, hi=86, color=TUNE, total=None):
    """Notes [midi, onset, beats] as a roll on a time axis of ``total`` beats (gaps kept)."""
    total = total or max(n[1] + n[2] for n in notes)
    frame = Rectangle(width=width, height=height, stroke_width=0, fill_opacity=0)
    g = VGroup(frame)
    g.frame, g.total = frame, total
    g.notes = []
    for p, a, d in notes:
        w = max(width * d / total - 0.05, 0.04)
        b = RoundedRectangle(width=w, height=0.13, corner_radius=0.05, stroke_width=0, fill_color=color, fill_opacity=1.0)
        b.move_to([frame.get_left()[0] + width * a / total + w / 2 + 0.025, frame.get_bottom()[1] + height * (p - lo) / (hi - lo), 0])
        g.add(b)
        g.notes.append(b)
    return g


def tree_mob(tree, width: float = 8.0, level_h: float = 0.75, font_size: int = 22):
    """A parse tree (nested [label, child, child] or [label, leaf]) drawn top-down; leaves evenly spaced at the bottom."""
    leaves = []

    def collect(t):
        if isinstance(t, str):
            leaves.append(t)
            return
        if len(t) == 2 and isinstance(t[1], str):
            leaves.append(t[1])
            return
        for c in t[1:]:
            collect(c)

    collect(tree)
    n = len(leaves)
    xs = [(-width / 2 + width * (k + 0.5) / n) for k in range(n)]

    def depth(t):
        if isinstance(t, str) or (len(t) == 2 and isinstance(t[1], str)):
            return 1
        return 1 + max(depth(c) for c in t[1:])

    D = depth(tree)
    g = VGroup()
    g.leaves = []
    counter = [0]

    def draw(t, lev):
        """Returns (x, y, mobject) for this node."""
        y = (D - lev) * level_h
        if len(t) == 2 and isinstance(t[1], str):
            x = xs[counter[0]]
            counter[0] += 1
            leaf_y = 0.0
            nl = label(t[0], font_size=font_size - 6, color=REGION_C.get(t[0], GREY_B)).move_to([x, y, 0])
            lf = label(tex(t[1]), font_size=font_size, color=WHITE).move_to([x, leaf_y - 0.1, 0])
            ln = Line([x, y - 0.18, 0], [x, leaf_y + 0.15, 0], color=DIM, stroke_width=1.5)
            g.add(ln, nl, lf)
            g.leaves.append(lf)
            return x, y
        pts = [draw(c, lev + 1) for c in t[1:]]
        x = sum(p[0] for p in pts) / len(pts)
        nl = label(t[0], font_size=font_size - 4, color=REGION_C.get(t[0], GREY_B)).move_to([x, y, 0])
        g.add(nl)
        for (cx, cy) in pts:
            g.add(Line([x, y - 0.15, 0], [cx, cy + 0.15, 0], color=GREY_B, stroke_width=1.8))
        return x, y

    draw(tree, 0)
    return g


def chord_strip(names, font_size: int = 30, buff: float = 0.45, color=GREY_A):
    """Roman numerals in a row, one label per chord, to be flashed as the chords sound."""
    return VGroup(*[label(tex(n), font_size=font_size, color=color) for n in names]).arrange(RIGHT, buff=buff)


def chord_times(start: float, names, beat: float):
    return [start + k * beat for k in range(len(names))]
