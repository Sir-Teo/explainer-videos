"""Helpers shared by the scenes of Part 8 ("Pipes, Reeds and Voices")."""

from __future__ import annotations

import numpy as np

from explainer.music.kit import *  # noqa: F403

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 8
clip = clip_loader(CACHE, CLIPS)
REED = "#E8B04A"        # cane
BRASS = "#F2C84B"
VOICE = EAR
FLUTE, CLAR, SAX, TPT, SING = AIR, REED, "#F08A5D", BRASS, EAR     # the five players, one colour each
PLAYERS = {"flute": FLUTE, "clarinet": CLAR, "saxophone": SAX, "trumpet": TPT, "voice": SING}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, links=("air", "instrument"), extra=extra, spoken=spoken)


def curve_from(g, xs, ys, color, stroke_width=3):
    return curve(g.ax, np.asarray(xs, dtype=float), np.asarray(ys, dtype=float), color, stroke_width=stroke_width)


def lane(names, colors, width: float = 2.3, height: float = 0.9, buff: float = 0.25, font_size: int = 26) -> VGroup:
    """One box for each player; ``pulse`` (kit) lights the one that is sounding."""
    return VGroup(*[VGroup(RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=c, stroke_width=2.5),
                           label(n, font_size=font_size, color=c)) for n, c in zip(names, colors)]).arrange(RIGHT, buff=buff)


def standing(n: int, closed: bool, pts: int = 80) -> np.ndarray:
    """The pressure along a pipe in its n-th mode (n = 1, 2, 3 ...): zero at an open end, greatest at a closed one.
    The pipe is open at the right; at the left it is open, or closed."""
    x = np.linspace(0, 1, pts)
    return np.cos((2 * n - 1) * np.pi * x / 2) if closed else np.sin(n * np.pi * x)


def pipe_mode(n: int, closed: bool, width: float = 4.6, bore: float = 0.5, color=AIR) -> VGroup:
    """A pipe with the envelope of one standing wave of pressure drawn inside it."""
    tv = TubeView(width=width, bore=bore, left="closed" if closed else "open", right="open", color=color, scale=0.2)
    sh = standing(n, closed)
    up = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners([tv.p(f, v) for f, v in zip(np.linspace(0, 1, len(sh)), sh)])
    dn = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners([tv.p(f, -v) for f, v in zip(np.linspace(0, 1, len(sh)), sh)])
    tv.curve.set_stroke(opacity=0)
    return VGroup(tv, up, dn)


def bore_shape(xs, rs, width: float = 9.0, height: float = 1.6, color=BRASS, stroke_width=3) -> VGroup:
    """An instrument's bore in section: radius against distance, mirrored about the axis (the radius is exaggerated)."""
    xs, rs = np.asarray(xs, dtype=float), np.asarray(rs, dtype=float)
    sx, sy = width / xs.max(), 0.5 * height / rs.max()
    top = VMobject(stroke_color=color, stroke_width=stroke_width).set_points_as_corners([np.array([x * sx - width / 2, r * sy, 0]) for x, r in zip(xs, rs)])
    bot = VMobject(stroke_color=color, stroke_width=stroke_width).set_points_as_corners([np.array([x * sx - width / 2, -r * sy, 0]) for x, r in zip(xs, rs)])
    return VGroup(top, bot)


def harmonic_bars(db, count: int = 10, width: float = 4.2, height: float = 1.8, color=AIR, floor_db: float = -40.0, font_size: int = 16) -> VGroup:
    return partial_bars(list(db)[:count], width=width, height=height, db=True, floor_db=floor_db, colors=[color] * count, font_size=font_size)
