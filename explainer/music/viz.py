"""Visual instruments of *Music, Built* (videos/music/SYLLABUS.md, section 4).  Each one draws a sound or the thing
that makes it, and each can be driven from a playing clip's clock (:meth:`explainer.music.sound.SoundTracker.drive`),
so the picture and the sound cannot drift apart.

* :class:`StringView`: a string between two supports, set from an array of displacements or filmed from a simulation;
* :class:`Lens`: the blur a vibrating string makes at full speed, an envelope that decays with the sound;
* :class:`Scope`: a triggered oscilloscope trace;
* :func:`partial_bars`: the partials of a tone as bars, coloured by the note each is nearest to;
* :class:`Spectrogram`: a clip's short-time spectrum with a playhead;
* :class:`MonochordView`: the instrument of Part 1, a string over a box with a movable bridge and a ruler.
"""

from __future__ import annotations

import numpy as np

from explainer.ai.viz import *  # noqa: F401,F403
from explainer.analysis import label, note  # noqa: F401
from explainer.music.monochord.audio import Clip
from explainer.music.monochord.dsp import stft_db
from explainer.music.palette import MC, harmonic_color, pc_color  # noqa: F401

__all__ = ["StringView", "Lens", "Scope", "partial_bars", "Spectrogram", "MonochordView", "heat_image", "HEAT",
           "ratio_tex", "playhead_fn"]

WOOD = "#7A5230"
WOOD_DARK = "#4A311C"


def ratio_tex(num: int, den: int) -> str:
    return rf"\tfrac{{{num}}}{{{den}}}"


# ---------------------------------------------------------------------------
# Strings
# ---------------------------------------------------------------------------
class StringView(VGroup):
    """A string stretched between two supports, ``width`` wide.  ``set_shape(u)`` draws displacements ``u`` (any
    number of samples from one end to the other, in units of ``scale`` scene units)."""

    def __init__(self, width: float = 10.0, scale: float = 1.0, color=MC.STRING, stroke_width: float = 4.0,
                 supports: bool = True, **kw):
        super().__init__(**kw)
        self.scale_u = scale
        self.axis = Line(LEFT * width / 2, RIGHT * width / 2, stroke_width=0, stroke_opacity=0)
        self.curve = VMobject(stroke_color=color, stroke_width=stroke_width)
        self.curve.set_points_as_corners([self.axis.get_start(), self.axis.get_end()])
        self.add(self.axis, self.curve)
        self.posts = VGroup()
        if supports:
            for p in (self.axis.get_start(), self.axis.get_end()):
                self.posts.add(Triangle(stroke_width=0, fill_color=GREY_B, fill_opacity=1).scale(0.13)
                               .move_to(p + DOWN * 0.1))
            self.add(self.posts)

    def p(self, frac: float, u: float = 0.0) -> np.ndarray:
        """The scene point at fraction ``frac`` of the length, displaced by ``u``."""
        a, b = self.axis.get_start(), self.axis.get_end()
        up = np.array([-(b - a)[1], (b - a)[0], 0.0])
        up = up / max(np.linalg.norm(up), 1e-9)
        return a + (b - a) * frac + up * u * self.scale_u

    def set_shape(self, u, lo: float = 0.0, hi: float = 1.0) -> "StringView":
        u = np.asarray(u, dtype=np.float64)
        a, b = self.axis.get_start(), self.axis.get_end()
        up = np.array([-(b - a)[1], (b - a)[0], 0.0])
        up = up / max(np.linalg.norm(up), 1e-9)
        f = np.linspace(lo, hi, len(u))
        pts = a[None, :] + (b - a)[None, :] * f[:, None] + up[None, :] * (u * self.scale_u)[:, None]
        if lo > 0:
            pts = np.vstack([a[None, :], pts])
        if hi < 1:
            pts = np.vstack([pts, b[None, :]])
        self.curve.set_points_as_corners(pts)
        return self

    def film(self, snaps: np.ndarray, dt: float, slow: float = 1.0, gain: float = 1.0, loop: bool = False,
             max_points: int = 240):
        """A function ``fn(mob, t)`` that draws the simulation's shape at clip time ``t``: ``snaps`` are shapes
        ``dt`` seconds apart, shown ``slow`` times slower than they happened (so ``slow=200`` turns 110 Hz into a
        motion the eye can follow).  Shapes between stored frames are interpolated."""
        step = max(1, snaps.shape[1] // max_points)
        frames = snaps[:, ::step] if (snaps.shape[1] - 1) % step == 0 else snaps
        n = len(frames)

        def fn(m, t):
            f = max(t, 0.0) / slow / dt
            if loop:
                f = f % (n - 1)
            f = min(f, n - 1.000001)
            i = int(f)
            a = f - i
            self.set_shape(gain * ((1 - a) * frames[i] + a * frames[i + 1]))

        return fn


class Lens(VMobject):
    """What a string looks like at full speed: a blur between its extreme positions.  ``set_amp(a)`` scales the
    envelope; drive it with the clip so that it shrinks as the sound dies."""

    def __init__(self, start, end, amp: float = 0.25, color=MC.STRING, opacity: float = 0.28, shape=None, n: int = 48,
                 **kw):
        super().__init__(stroke_width=1.5, stroke_color=color, stroke_opacity=0.7, fill_color=color,
                         fill_opacity=opacity, **kw)
        self.a, self.b = np.array(start, dtype=float), np.array(end, dtype=float)
        x = np.linspace(0, 1, n)
        self.env = np.sin(np.pi * x) if shape is None else np.interp(x, np.linspace(0, 1, len(shape)), shape)
        self.x = x
        self.amp0 = amp
        self.set_amp(1.0)

    def set_amp(self, a: float) -> "Lens":
        d = self.b - self.a
        up = np.array([-d[1], d[0], 0.0])
        up = up / max(np.linalg.norm(up), 1e-9)
        base = self.a[None, :] + d[None, :] * self.x[:, None]
        top = base + up[None, :] * (self.env * self.amp0 * max(a, 1e-3))[:, None]
        bot = base - up[None, :] * (self.env * self.amp0 * max(a, 1e-3))[:, None]
        self.set_points_as_corners(np.vstack([top, bot[::-1], top[:1]]))
        return self

    def decay(self, rate: float, floor: float = 0.0):
        """``fn(mob, t)``: the envelope shrinking as ``exp(-rate t)``."""
        return lambda m, t: m.set_amp(max(float(np.exp(-rate * max(t, 0.0))), floor))


# ---------------------------------------------------------------------------
# Waveforms
# ---------------------------------------------------------------------------
class Scope(VGroup):
    """An oscilloscope: a frame and a trace.  ``set_wave(y)`` draws samples in [-1, 1]; ``follow(clip, window)``
    gives a function for :meth:`SoundTracker.drive` that shows the clip around the playhead, triggered on a rising
    zero crossing so that a steady tone stands still."""

    def __init__(self, width: float = 5.0, height: float = 2.0, color=MC.LEVEL, stroke_width: float = 2.5,
                 frame: bool = True, **kw):
        super().__init__(**kw)
        self.w, self.h = width, height
        self.box = Rectangle(width=width, height=height, stroke_color=GREY_D, stroke_width=1.2,
                             fill_color="#0B0F17", fill_opacity=0.6 if frame else 0)
        self.zero = Line(LEFT * width / 2, RIGHT * width / 2, color=GREY_D, stroke_width=1)
        self.trace = VMobject(stroke_color=color, stroke_width=stroke_width)
        self.trace.set_points_as_corners([LEFT * width / 2, RIGHT * width / 2])
        self.add(self.box, self.zero, self.trace)

    def set_wave(self, y, gain: float = 1.0) -> "Scope":
        y = np.clip(np.asarray(y, dtype=np.float64) * gain, -1.0, 1.0)
        if len(y) > 600:
            y = y[:: len(y) // 600]
        left, right = self.box.get_left(), self.box.get_right()
        up = self.box.get_top() - self.box.get_center()
        x = np.linspace(0, 1, len(y))
        pts = left[None, :] + (right - left)[None, :] * x[:, None] + up[None, :] * (y * 0.92)[:, None]
        self.trace.set_points_as_corners(pts)
        return self

    def follow(self, clip: Clip, window: float = 0.03, gain: float | None = None, trigger: bool = True):
        y = clip.mono.astype(np.float64)
        sr = clip.sr
        g = gain if gain is not None else 0.95 / max(float(np.abs(y).max()), 1e-9)
        n = int(window * sr)

        def fn(m, t):
            i = int(np.clip(t, 0, clip.duration) * sr)
            if trigger:
                seg = y[i:i + n]
                z = np.flatnonzero((seg[:-1] <= 0) & (seg[1:] > 0)) if len(seg) > 1 else np.zeros(0, int)
                if z.size:
                    i += int(z[0])
            w = y[i:i + n]
            if len(w) < n:
                w = np.concatenate([w, np.zeros(n - len(w))])
            self.set_wave(w, g)

        return fn


# ---------------------------------------------------------------------------
# Partials
# ---------------------------------------------------------------------------
def partial_bars(values, width: float = 6.0, height: float = 2.6, db: bool = True, floor_db: float = -48.0,
                 root_pc: int = 0, numbers: bool = True, font_size: int = 20, colors=None, first: int = 1) -> VGroup:
    """Bars for partials ``first``, ``first + 1``, ...: ``values`` are levels in dB relative to the strongest
    (``db=True``; the floor is the baseline) or linear amplitudes.  Each bar takes the colour of the note it is
    nearest to (:func:`harmonic_color`), so the chord inside a tone can be seen.  ``.bars``, ``.numbers``, ``.base``;
    ``.top(i)`` is the top of bar i."""
    v = np.asarray(values, dtype=np.float64)
    if db:
        frac = np.clip((v - floor_db) / (0.0 - floor_db), 0.0, 1.0)
    else:
        frac = np.clip(np.abs(v) / max(np.abs(v).max(), 1e-12), 0.0, 1.0)
    n = len(v)
    slot = width / n
    base = Line(LEFT * width / 2, RIGHT * width / 2, color=GREY_C, stroke_width=2)
    bars, nums = VGroup(), VGroup()
    for i in range(n):
        col = (colors[i] if colors is not None else harmonic_color(first + i, root_pc))
        h = max(frac[i] * height, 0.012)
        b = Rectangle(width=slot * 0.62, height=h, stroke_width=0, fill_color=col, fill_opacity=0.95)
        b.move_to(base.get_left() + RIGHT * (slot * (i + 0.5)) + UP * h / 2)
        bars.add(b)
        if numbers:
            nums.add(label(str(first + i), font_size=font_size, color=GREY_B).next_to(
                base.get_left() + RIGHT * (slot * (i + 0.5)), DOWN, buff=0.12))
    g = VGroup(base, bars, nums)
    g.base, g.bars, g.numbers, g.frac, g.bar_height = base, bars, nums, frac, height
    return g


# ---------------------------------------------------------------------------
# Images of data
# ---------------------------------------------------------------------------
# A dark heat map that starts at the frame's background: quiet is invisible, loud is bright.
HEAT = np.array([[0x0E, 0x11, 0x17], [0x24, 0x1B, 0x4A], [0x5B, 0x1F, 0x7A], [0xA8, 0x2E, 0x77], [0xE3, 0x55, 0x55],
                 [0xF9, 0x9B, 0x45], [0xFC, 0xE0, 0x8A], [0xFF, 0xFF, 0xE8]], dtype=np.float64)


def heat_image(a: np.ndarray, lo: float, hi: float, width: float | None = None, height: float | None = None,
               smooth: bool = True) -> ImageMobject:
    """A 2-D array as a picture (row 0 at the top), values from ``lo`` (background) to ``hi`` (brightest)."""
    z = np.clip((np.asarray(a, dtype=np.float64) - lo) / (hi - lo), 0.0, 1.0) * (len(HEAT) - 1)
    i = np.minimum(z.astype(int), len(HEAT) - 2)
    f = (z - i)[..., None]
    rgb = (HEAT[i] * (1 - f) + HEAT[i + 1] * f).astype(np.uint8)
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear" if smooth else "nearest"])
    if width is not None and height is not None:
        img.stretch_to_fit_width(width)
        img.stretch_to_fit_height(height)
    elif width is not None:
        img.width = width
    elif height is not None:
        img.height = height
    return img


class Spectrogram(Group):
    """A clip's spectrogram: time runs right, frequency up, brightness is level.  ``.x_of(t)``, ``.y_of(hz)`` give
    scene coordinates; ``.playhead`` is a vertical line and ``.follow()`` the function that moves it with the clip.
    ``marks``: frequencies to tick on the left edge (``[(hz, tex)]``)."""

    def __init__(self, clip: Clip, width: float = 8.0, height: float = 3.2, fmax: float = 4000.0, fmin: float = 0.0,
                 n_fft: int = 4096, hop: int = 480, db_range=(-66.0, -6.0), marks=(), font_size: int = 18,
                 seconds: bool = True, **kw):
        super().__init__(**kw)
        t, f, S = stft_db(clip.mono, clip.sr, n_fft, hop)
        keep = (f >= fmin) & (f <= fmax)
        S = S[keep] - S.max()
        self.duration, self.fmin, self.fmax = clip.duration, fmin, fmax
        self.image = heat_image(S[::-1], db_range[0], db_range[1], width, height)
        self.frame = Rectangle(width=width, height=height, stroke_color=GREY_D, stroke_width=1.2)
        self.add(self.image, self.frame)
        self.ticks = VGroup()
        for hz, tex in marks:
            y = self.y_of(hz)
            self.ticks.add(Line(self.frame.get_left() + UP * 0, self.frame.get_left() + LEFT * 0.1, color=GREY_C,
                                stroke_width=1.5).set_y(y))
            self.ticks.add(label(tex, font_size=font_size, color=GREY_B).next_to(
                [self.frame.get_left()[0] - 0.1, y, 0], LEFT, buff=0.08))
        if seconds:
            for s in range(0, int(clip.duration) + 1):
                x = self.x_of(s)
                self.ticks.add(Line([x, self.frame.get_bottom()[1], 0], [x, self.frame.get_bottom()[1] - 0.08, 0],
                                    color=GREY_C, stroke_width=1.5))
            self.ticks.add(label(r"seconds", font_size=font_size - 2, color=GREY_B).next_to(self.frame, DOWN, buff=0.14))
        self.add(self.ticks)
        self.playhead = Line(self.frame.get_corner(DL), self.frame.get_corner(UL), color=MC.PLAY, stroke_width=2)
        self.add(self.playhead)

    def x_of(self, t: float) -> float:
        return float(self.frame.get_left()[0] + self.frame.width * np.clip(t / max(self.duration, 1e-9), 0, 1))

    def y_of(self, hz: float) -> float:
        return float(self.frame.get_bottom()[1] + self.frame.height * (hz - self.fmin) / (self.fmax - self.fmin))

    def follow(self):
        return lambda m, t: m.set_x(self.x_of(t))


def playhead_fn(x0: float, x1: float, duration: float):
    """``fn(mob, t)`` moving a mobject from x0 to x1 over ``duration`` seconds of a clip."""
    return lambda m, t: m.set_x(x0 + (x1 - x0) * float(np.clip(t / max(duration, 1e-9), 0, 1)))


# ---------------------------------------------------------------------------
# The monochord
# ---------------------------------------------------------------------------
class MonochordView(VGroup):
    """The monochord: one string over a sound box, fixed at both ends, with a movable bridge under it and a ruler.

    The sounding part is the stretch from the left end to the movable bridge; ``stop`` is its length as a fraction
    of the whole (1 = open string).  ``.x(frac)`` is the point on the string at that fraction; ``.movable`` the
    bridge; ``.move_bridge(frac)`` an animation; ``.lens(frac)`` the blur of the sounding part; ``.mark(frac, tex)``
    a tick with a fraction under the ruler."""

    def __init__(self, width: float = 10.5, stop: float = 1.0, ruler: bool = True, divisions: int = 12, **kw):
        super().__init__(**kw)
        self.width_ = width
        box = RoundedRectangle(width=width + 0.9, height=0.9, corner_radius=0.12, stroke_color=WOOD_DARK,
                               stroke_width=2, fill_color=WOOD, fill_opacity=0.75)
        hole = Circle(radius=0.16, stroke_width=0, fill_color="#0B0F17", fill_opacity=0.9).move_to(
            box.get_center() + RIGHT * width * 0.32)
        y = box.get_top()[1] + 0.34
        self.axis = Line([-width / 2, y, 0], [width / 2, y, 0], stroke_width=0, stroke_opacity=0)
        self.string = Line(self.axis.get_start(), self.axis.get_end(), color=MC.STRING, stroke_width=3.5)
        ends = VGroup(*[Polygon(p + DOWN * 0.34 + LEFT * 0.12, p + DOWN * 0.34 + RIGHT * 0.12, p, stroke_width=0,
                                fill_color=GREY_A, fill_opacity=1)
                        for p in (self.axis.get_start(), self.axis.get_end())])
        self.movable = Polygon(DOWN * 0.34 + LEFT * 0.14, DOWN * 0.34 + RIGHT * 0.14, ORIGIN, stroke_width=0,
                               fill_color=MC.RATIO, fill_opacity=1)
        self.movable.shift(self.x(stop))
        self.box = VGroup(box, hole)
        self.add(self.box, self.axis, self.string, ends)
        self.ruler = VGroup()
        if ruler:
            y0 = box.get_bottom()[1] - 0.16
            self.ruler.add(Line([-width / 2, y0, 0], [width / 2, y0, 0], color=GREY_C, stroke_width=1.5))
            for i in range(divisions + 1):
                x = -width / 2 + width * i / divisions
                self.ruler.add(Line([x, y0, 0], [x, y0 - (0.14 if i % (divisions // 2) == 0 else 0.08), 0],
                                    color=GREY_C, stroke_width=1.5))
            self.add(self.ruler)
        self.add(self.movable)
        self.stop = stop
        if stop >= 1.0:
            self.movable.set_opacity(0)

    def x(self, frac: float) -> np.ndarray:
        a, b = self.axis.get_start(), self.axis.get_end()
        return a + (b - a) * frac

    def ruler_y(self) -> float:
        return float(self.ruler[0].get_y()) if len(self.ruler) else float(self.box.get_bottom()[1])

    def set_stop(self, frac: float) -> "MonochordView":
        self.movable.set_opacity(1 if frac < 1.0 else 0)
        self.movable.shift(self.x(frac) - self.movable.get_vertices()[2])
        self.stop = frac
        return self

    def move_bridge(self, frac: float):
        """An animation moving the bridge to ``frac`` (it appears if the string was open)."""
        target = self.movable.copy().set_opacity(1 if frac < 1.0 else 0)
        target.shift(self.x(frac) - target.get_vertices()[2])
        self.stop = frac
        return Transform(self.movable, target)

    def sounding(self, frac: float | None = None, color=MC.TUNE, stroke_width: float = 5.5) -> Line:
        frac = self.stop if frac is None else frac
        return Line(self.x(0), self.x(frac), color=color, stroke_width=stroke_width)

    def lens(self, frac: float | None = None, amp: float = 0.2, color=MC.TUNE, lo: float = 0.0) -> Lens:
        frac = self.stop if frac is None else frac
        return Lens(self.x(lo), self.x(frac), amp=amp, color=color)

    def mark(self, frac: float, tex: str, color=MC.RATIO, font_size: int = 30) -> VGroup:
        x = self.x(frac)[0]
        y0 = self.ruler_y()
        tick = Line([x, y0 + 0.02, 0], [x, y0 - 0.2, 0], color=color, stroke_width=2.5)
        t = MathTex(tex, font_size=font_size, color=color).next_to(tick, DOWN, buff=0.1)
        return VGroup(tick, t)

    def brace(self, lo: float, hi: float, tex: str, color=MC.RATIO, font_size: int = 30, up: bool = True) -> VGroup:
        a, b = self.x(lo), self.x(hi)
        ln = Line(a, b)
        br = Brace(ln, UP if up else DOWN, buff=0.42 if up else 0.5, color=color)
        t = MathTex(tex, font_size=font_size, color=color).next_to(br, UP if up else DOWN, buff=0.08)
        return VGroup(br, t)
