"""Helpers shared by the scenes of Part 3 ("The Spectrum")."""

from __future__ import annotations

import numpy as np

from explainer.music.kit import *  # noqa: F403

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 3
clip = clip_loader(CACHE, CLIPS)


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, links=("air", "ear"), extra=extra, spoken=spoken)


def picture(a: np.ndarray, lo: float, hi: float, width: float, height: float) -> Group:
    """A stored time-frequency picture (row 0 the lowest frequency) with a thin frame; ``.playhead`` runs across it."""
    img = heat_image(np.asarray(a)[::-1], lo, hi, width, height)
    frame = Rectangle(width=width, height=height, stroke_color=GREY_D, stroke_width=1.2)
    head = Line(frame.get_corner(DL), frame.get_corner(UL), color=MC.PLAY, stroke_width=2).set_opacity(0)
    g = Group(img, frame, head)
    g.frame, g.playhead = frame, head
    return g


def sweep(g: Group, seconds: float):
    """``fn(mob, t)`` that moves a picture's playhead across it in ``seconds`` (for ``snd.drive``)."""
    x0, x1 = g.frame.get_left()[0], g.frame.get_right()[0]
    return lambda m, t: m.set_x(x0 + (x1 - x0) * float(np.clip(t / seconds, 0, 1)))


def ab_boxes(buff: float = 2.6, y: float = 0.1) -> VGroup:
    return VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.4, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2),
                           label(t, font_size=60, color=GREY_A)) for t in ("A", "B")]).arrange(RIGHT, buff=buff).shift(UP * y)


def glow_on(snd, box, t0: float, t1: float, env=None, rate: float = 100.0):
    """Light an A/B box while its sound plays (its edge follows the sound's envelope if one is given)."""
    box[1].set_color(EAR)
    glow = box[0].copy().set_stroke(EAR, width=5)
    snd.show(glow)
    f = follow(env, rate, t0) if env is not None else None
    snd.drive(glow, lambda m, t: m.set_stroke(opacity=(f(t) if f else 0.6 + 0.4 * np.sin(18 * t)) if t0 <= t < t1 else 0.0))
    return glow
