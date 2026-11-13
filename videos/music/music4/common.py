"""Helpers shared by the scenes of Part 4 ("The Ear")."""

from __future__ import annotations

import numpy as np

from explainer.music.kit import *  # noqa: F403

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 4
clip = clip_loader(CACHE, CLIPS)
BONE = "#E8DCC2"      # the ear's solid parts
FLUID = "#5B8DEF"     # the fluid of the inner ear


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, links=("ear",), extra=extra, spoken=spoken)


# ---------------------------------------------------------------------------
# Frequency on a logarithmic axis
# ---------------------------------------------------------------------------
def hz_name(f: float) -> str:
    return rf"{f / 1000:g}\,\mathrm{{k}}" if f >= 1000 else f"{f:g}"


def faxes(f_lo, f_hi, y_range, x_length=8.0, y_length=3.4, ylabel="", yticks=None, fticks=(100, 1000, 10000),
          xlabel=r"frequency (Hz)", font_size=20, yfmt=None) -> VGroup:
    """Axes whose x is frequency on a logarithmic scale.  ``g.fx(f)`` is the x-coordinate (in axis units) of f."""
    g = axes([np.log10(f_lo), np.log10(f_hi)], y_range, x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel,
             xticks=[float(np.log10(f)) for f in fticks], yticks=yticks, xfmt=lambda v: hz_name(float(round(10 ** v, 6))),
             yfmt=yfmt, font_size=font_size)
    g.fx = lambda f: float(np.log10(f))
    g.at = lambda f, y: g.ax.c2p(float(np.log10(f)), y)
    return g


def fcurve(g, f, y, color, stroke_width=3):
    return curve(g.ax, np.log10(np.asarray(f, dtype=float)), np.asarray(y, dtype=float), color, stroke_width=stroke_width)


# ---------------------------------------------------------------------------
# Pictures of stored data with a playhead (as in Part 3)
# ---------------------------------------------------------------------------
def picture(a: np.ndarray, lo: float, hi: float, width: float, height: float) -> Group:
    """A stored time-frequency picture (row 0 the lowest frequency) with a thin frame; ``.playhead`` runs across it."""
    img = heat_image(np.asarray(a)[::-1], lo, hi, width, height)
    frame = Rectangle(width=width, height=height, stroke_color=GREY_D, stroke_width=1.2)
    head = Line(frame.get_corner(DL), frame.get_corner(UL), color=MC.PLAY, stroke_width=2).set_opacity(0)
    g = Group(img, frame, head)
    g.frame, g.playhead = frame, head
    return g


def sweep(g, seconds: float):
    """``fn(mob, t)`` that moves a picture's playhead across it in ``seconds`` (for ``snd.drive``)."""
    x0, x1 = g.frame.get_left()[0], g.frame.get_right()[0]
    return lambda m, t: m.set_x(x0 + (x1 - x0) * float(np.clip(t / seconds, 0, 1)))


def boxes(names=("A", "B"), buff: float = 1.2, width: float = 2.4, height: float = 1.3, font_size: int = 54) -> VGroup:
    """Boxes that stand for the sounds of an ear question; ``pulse`` lights one while its sound plays."""
    return VGroup(*[VGroup(RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2),
                           label(t, font_size=font_size, color=GREY_A)) for t in names]).arrange(RIGHT, buff=buff)


def pulse(snd, mob, t0: float, t1: float, rate: float = 18.0, color=None, buff: float = 0.1):
    """Light a frame around ``mob`` between clip times ``t0`` and ``t1`` (it flickers, so the picture is never still)."""
    glow = SurroundingRectangle(mob, color=color or EAR, buff=buff, stroke_width=4, corner_radius=0.12)
    snd.show(glow)
    snd.drive(glow, lambda m, t: m.set_stroke(opacity=(0.6 + 0.4 * np.sin(rate * t)) if t0 <= t < t1 else 0.0))
    return glow


# ---------------------------------------------------------------------------
# The cochlea, unrolled
# ---------------------------------------------------------------------------
class Cochlea(VGroup):
    """The basilar membrane laid out straight: the base (narrow, stiff) on the left, the apex (wide, slack) on the
    right.  ``p(mm, v)`` is the point ``mm`` from the base, lifted by ``v``; ``wave`` is a :class:`Trace` along it and
    ``lens(env)`` a blur between a wave's extremes."""

    def __init__(self, width: float = 10.0, length_mm: float = 35.0, scale: float = 0.9, ticks=(0, 5, 10, 15, 20, 25, 30, 35),
                 names: bool = True, **kw):
        super().__init__(**kw)
        self.w, self.length, self.gain = width, length_mm, scale
        a, b = LEFT * width / 2, RIGHT * width / 2
        self.membrane = Polygon(a + UP * 0.05, b + UP * 0.2, b + DOWN * 0.2, a + DOWN * 0.05, stroke_width=0, fill_color=BONE, fill_opacity=0.28)
        self.mid = Line(a, b, color=GREY_C, stroke_width=1.2)
        self.add(self.membrane, self.mid)
        self.marks = VGroup()
        for mm in ticks:
            x = a + RIGHT * width * mm / length_mm
            self.marks.add(Line(x + DOWN * 0.95, x + DOWN * 1.05, color=GREY_C, stroke_width=1.5),
                           label(str(mm), font_size=18, color=GREY_B).next_to(x + DOWN * 1.05, DOWN, buff=0.08))
        self.axis = Line(a + DOWN * 1.0, b + DOWN * 1.0, color=GREY_D, stroke_width=1.2)
        self.unit = label(r"mm from the base", font_size=20, color=GREY_B).next_to(self.axis, DOWN, buff=0.42)
        self.add(self.axis, self.marks, self.unit)
        if names:
            self.base = VGroup(label(r"base", font_size=24, color=GREY_A), label(r"narrow, \ stiff", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.05)
            self.apex = VGroup(label(r"apex", font_size=24, color=GREY_A), label(r"wide, \ slack", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.05)
            self.base.next_to(a, LEFT, buff=0.25)
            self.apex.next_to(b, RIGHT, buff=0.25)
            self.add(self.base, self.apex)

    def p(self, mm: float, v: float = 0.0) -> np.ndarray:
        return self.mid.get_start() + (self.mid.get_end() - self.mid.get_start()) * (mm / self.length) + UP * self.gain * v

    def trace(self, color=TUNE, stroke_width: float = 3.0) -> Trace:
        return Trace(self.mid.get_start(), self.mid.get_end(), scale=self.gain, color=color, stroke_width=stroke_width)

    def lens(self, env, color=TUNE, opacity: float = 0.3) -> Lens:
        return Lens(self.mid.get_start(), self.mid.get_end(), amp=self.gain, color=color, opacity=opacity, shape=np.asarray(env), n=200)

    def pin(self, mm: float, text: str, color=FREQ, font_size: int = 22, up: float = 1.15) -> VGroup:
        tip = self.p(mm)
        t = label(text, font_size=font_size, color=color).move_to(tip + UP * (up + 0.22))
        return VGroup(Line(tip + UP * up, tip + UP * 0.25, color=color, stroke_width=1.5), t)


def ear_diagram() -> VGroup:
    """A schematic of the ear in section: the canal, the eardrum, three bones, the oval window, the coiled cochlea.
    ``.canal``, ``.drum``, ``.bones``, ``.window``, ``.cochlea`` and ``.pinna``."""
    pinna = ArcBetweenPoints(LEFT * 4.9 + UP * 1.2, LEFT * 4.9 + DOWN * 1.2, angle=-PI * 0.9, color=BONE, stroke_width=5)
    top = Line(LEFT * 4.6 + UP * 0.32, LEFT * 1.6 + UP * 0.32, color=BONE, stroke_width=4)
    bot = Line(LEFT * 4.6 + DOWN * 0.32, LEFT * 1.6 + DOWN * 0.32, color=BONE, stroke_width=4)
    air = Rectangle(width=3.0, height=0.64, stroke_width=0, fill_color=AIR, fill_opacity=0.12).move_to(LEFT * 3.1)
    canal = VGroup(air, top, bot)
    drum = Line(LEFT * 1.6 + UP * 0.5, LEFT * 1.45 + DOWN * 0.5, color=FORCE, stroke_width=7)
    hammer = Line(LEFT * 1.5, LEFT * 0.7 + UP * 0.55, color=BONE, stroke_width=7)
    anvil = Line(LEFT * 0.7 + UP * 0.55, LEFT * 0.2 + UP * 0.05, color=BONE, stroke_width=7)
    pivot = Dot(LEFT * 0.7 + UP * 0.55, radius=0.07, color=GREY_B)
    stirrup = VGroup(Line(LEFT * 0.2 + UP * 0.05, RIGHT * 0.35 + UP * 0.05, color=BONE, stroke_width=6),
                     Line(RIGHT * 0.35 + UP * 0.22, RIGHT * 0.35 + DOWN * 0.12, color=FORCE, stroke_width=7))
    bones = VGroup(hammer, anvil, pivot, stirrup)
    th = np.linspace(0, 2.6 * TAU, 160)
    r = 1.25 * np.exp(-0.11 * th)
    centre = RIGHT * 1.9 + UP * 0.05
    spiral = VMobject(stroke_color=FLUID, stroke_width=9, stroke_opacity=0.85)
    spiral.set_points_smoothly([centre + r_ * np.array([-np.cos(t), -np.sin(t), 0]) for r_, t in zip(r, th)])
    g = VGroup(pinna, canal, drum, bones, spiral)
    g.pinna, g.canal, g.drum, g.bones, g.window, g.cochlea = pinna, canal, drum, bones, stirrup[1], spiral
    return g


def run(tracker, fps: float = 8.0):
    """Let a film's frame counter run by itself (so a looping film plays through a whole narration)."""
    tracker.add_updater(lambda m, dt: m.increment_value(dt * fps))
    return tracker


def halt(tracker):
    tracker.clear_updaters()
    return tracker


def listen_note(text: str, color=None, width: float = 8.0, font_size=28) -> VGroup:
    """What to listen for in a demonstration (not one of the part's pause-and-listen questions: nothing to commit to,
    only something to notice)."""
    from explainer.ai.lecture import _body, _card

    color = color or EAR
    head = VGroup(speaker_icon(0.2, color), label(r"Listen for this", font_size=font_size - 6, color=color)).arrange(RIGHT, buff=0.18)
    return _card(head, _body(text, width - 0.8, font_size), color, width, accent=False)
