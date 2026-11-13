"""Helpers shared by the scenes of Part 6 ("Tuning")."""

from __future__ import annotations

import numpy as np

from explainer.music.kit import *  # noqa: F403

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 6
clip = clip_loader(CACHE, CLIPS)
PURE, WIDE, NARROW = GOOD, BAD, AIR
SHARP = {"C#": r"C$\sharp$", "F#": r"F$\sharp$", "G#": r"G$\sharp$", "Eb": r"E$\flat$", "Bb": r"B$\flat$", "D#": r"D$\sharp$", "A#": r"A$\sharp$",
         "E#": r"E$\sharp$", "B#": r"B$\sharp$", "Ab": r"A$\flat$"}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, links=("ear",), extra=extra, spoken=spoken)


def note_tex(name: str) -> str:
    return SHARP.get(name, name)


class FifthsCircle(VGroup):
    """The twelve notes round a circle, a fifth apart.  ``.dots[k]``, ``.names[k]`` and ``.edge(k)`` (the arc from
    note k to note k + 1) for colouring each fifth; ``.spoke(k)`` a line from the centre for a major third."""

    def __init__(self, radius: float = 1.9, names=("C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "Eb", "Bb", "F"), font_size: int = 24, **kw):
        super().__init__(**kw)
        self.r, self.keys = radius, names
        self.ring = Circle(radius=radius, color=GREY_D, stroke_width=1.5)
        self.dots = VGroup(*[Dot(self.at(k), radius=0.07, color=GREY_A) for k in range(12)])
        self.names = VGroup(*[label(note_tex(n), font_size=font_size, color=GREY_A).move_to(self.at(k, radius + 0.36)) for k, n in enumerate(names)])
        self.add(self.ring, self.dots, self.names)

    def at(self, k: float, radius: float | None = None) -> np.ndarray:
        r = self.r if radius is None else radius
        a = TAU * k / 12
        return self.ring.get_center() + r * np.array([np.sin(a), np.cos(a), 0.0])

    def edge(self, k: int, color=PURE, stroke_width: float = 6.0) -> VMobject:
        a0 = PI / 2 - TAU * k / 12
        return Arc(radius=self.r, start_angle=a0, angle=-TAU / 12, color=color, stroke_width=stroke_width).move_arc_center_to(self.ring.get_center())

    def index(self, name: str) -> int:
        return self.keys.index(name)


def error_color(err: float, scale: float = 22.0):
    """A colour for an interval's error in cents: green when pure, blue when narrow, red when wide."""
    x = float(np.clip(abs(err) / scale, 0, 1))
    return interpolate_color(ManimColor(PURE), ManimColor(WIDE if err > 0 else NARROW), x)


def key_bars(values, names, width: float = 6.0, height: float = 2.0, top: float = 45.0, color=None, font_size: int = 18) -> VGroup:
    """Bars for one number in each key (cents an interval is from pure), on a common scale; ``.bars`` and ``.base``."""
    slot = width / len(values)
    base = Line(LEFT * width / 2, RIGHT * width / 2, color=GREY_C, stroke_width=1.5)
    bars, labs = VGroup(), VGroup()
    for k, (v, n) in enumerate(zip(values, names)):
        h = max(abs(v) / top * height, 0.015)
        b = Rectangle(width=slot * 0.66, height=h, stroke_width=0, fill_color=color or error_color(v), fill_opacity=0.9)
        x = base.get_left() + RIGHT * slot * (k + 0.5)
        b.move_to(x + UP * (h / 2 if v >= 0 else -h / 2))
        bars.add(b)
        labs.add(label(note_tex(n), font_size=font_size, color=GREY_B).next_to(x, DOWN, buff=0.12 if v >= 0 else 0.12 + h))
    g = VGroup(base, bars, labs)
    g.base, g.bars, g.labels = base, bars, labs
    return g
