"""What every part's scenes share: the palette by name, numbers for narration, the furniture of a listening window,
and pictures that follow a clip.  A part's ``common.py`` does ``from explainer.music.kit import *`` and adds its own
``PART``, ``load`` and ``clip``."""

from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music.viz import HEAT

# one meaning per colour, for the whole series (explainer/music/palette.py)
TUNE = MC.TUNE      # the Tune, and whatever is sounding now
STR = MC.STRING     # strings and solid things that vibrate
RATIO = MC.RATIO    # ratios and lengths
FREQ = MC.FREQ      # frequency
TIME = MC.TIME      # time, periods
LEVEL = MC.LEVEL    # amplitude and level
FORCE = MC.FORCE    # forces, pressure
MASS = MC.MASS      # mass
RIGHT_C = MC.RIGHT  # the wave going right
LEFT_C = MC.LEFT    # the wave going left
NODE = MC.NODE      # nodes
GOOD = MC.SMOOTH    # agrees, coincides
BAD = MC.ROUGH      # false, clashes
HIST = MC.HUMAN     # people and dates
EAR = MC.EAR        # listening
LIMIT = MC.LIMIT    # the frontier
AIR = "#7DD3FC"     # air


def say(x, digits: int = 0) -> str:
    """A number for narration: ``130.8`` or ``1,200``."""
    return f"{x:,.{digits}f}"


def flat_name(name: str) -> str:
    """A note name for Tex: ``A#5`` is written as the flat it is heard as (B flat), ``C3`` stays."""
    sharp_to_flat = {"A#": r"B$\flat$", "D#": r"E$\flat$", "G#": r"A$\flat$", "C#": r"C$\sharp$", "F#": r"F$\sharp$"}
    for k, v in sharp_to_flat.items():
        if name.startswith(k):
            return v + name[len(k):]
    return name


def window(snd, text: str = r"listen", kind: str = "physical model", detail: str = "", corner=DL, tag_corner=UR,
           tag: bool = True):
    """The furniture of a listening window: the strip that fills as the clip plays, and what the sound is."""
    bar = listen_bar(snd, text).to_corner(corner, buff=0.35)
    snd.show(bar)
    if tag:
        snd.show(sound_tag(kind, detail, corner=tag_corner))
    return bar


def ring(at: float = 0.0, rate: float = 1.2, stop_at: float | None = None):
    """``fn(lens, t)`` for :meth:`SoundTracker.drive`: a blur that appears at clip time ``at`` and dies at ``rate``
    per second, gone before ``at`` and (if given) after ``stop_at``."""
    def fn(m, t):
        if t < at or (stop_at is not None and t >= stop_at):
            m.set_amp(0.0)
        else:
            m.set_amp(float(np.exp(-rate * (t - at))))
    return fn


def follow(env, rate: float = 100.0, t0: float = 0.0, lo: float = 0.0, hi: float = 1.0):
    """``fn(t) -> value`` that reads a stored envelope (``rate`` values a second, starting at clip time ``t0``) and
    maps it to ``lo..hi``: the level a picture should show at clip time ``t``."""
    env = np.asarray(env, dtype=float)

    def fn(t):
        i = (t - t0) * rate
        if i < 0 or i > len(env) - 1:
            return lo
        k = int(i)
        v = env[k] if k + 1 >= len(env) else env[k] * (1 - (i - k)) + env[k + 1] * (i - k)
        return lo + (hi - lo) * float(v)

    return fn


class Meter(VGroup):
    """A level meter: a bar that a clip's envelope drives.  ``snd.drive(meter, meter.follow(env))``."""

    def __init__(self, width: float = 0.5, height: float = 3.0, color=LEVEL, **kw):
        super().__init__(**kw)
        self.frame = Rectangle(width=width, height=height, stroke_color=GREY_C, stroke_width=1.5)
        self.bar = Rectangle(width=width - 0.08, height=0.02, stroke_width=0, fill_color=color, fill_opacity=0.9)
        self.bar.move_to(self.frame.get_bottom() + UP * 0.05)
        self.h = height - 0.08
        self.add(self.frame, self.bar)

    def set_level(self, v: float) -> "Meter":
        v = float(np.clip(v, 0.004, 1.0))
        self.bar.stretch_to_fit_height(self.h * v)
        self.bar.move_to(self.frame.get_bottom() + UP * (0.04 + self.h * v / 2))
        return self

    def follow(self, env, rate: float = 100.0, t0: float = 0.0):
        f = follow(env, rate, t0)
        return lambda m, t: m.set_level(f(t))


# ---------------------------------------------------------------------------
# Films of stored frames (a simulation shown slowed down)
# ---------------------------------------------------------------------------
def film(view, frames: np.ndarray, gain: float = 1.0, step: int = 1, loop: bool = False) -> ValueTracker:
    """Attach stored shapes to anything with ``set_shape`` (a StringView, a TubeView, a ParcelRow).  The returned
    tracker's value is the frame number (fractions interpolate)."""
    fr = frames[:, ::step] if step > 1 and (frames.shape[1] - 1) % step == 0 else frames
    n = len(fr)
    tr = ValueTracker(0.0)

    def upd(m):
        f = tr.get_value() % (n - 1) if loop else tr.get_value()
        f = min(max(f, 0.0), n - 1.000001)
        i = int(f)
        a = f - i
        view.set_shape(gain * ((1 - a) * fr[i] + a * fr[i + 1]))

    upd(view)
    view.add_updater(upd)
    return tr


DIVERGE = np.array([[0x4F, 0xC3, 0xF7], [0x1B, 0x4F, 0x72], [0x0E, 0x11, 0x17], [0x7A, 0x2E, 0x1F], [0xFF, 0x9B, 0x55]],
                   dtype=np.float64)   # rarefied (blue) ... rest (the background) ... compressed (orange)


def field_rgb(a: np.ndarray, scale: float, solid=None, wall=(0x8A, 0x93, 0xA0)) -> np.ndarray:
    """A pressure field as a picture: blue where the air is thinned, orange where it is squeezed, the background
    where it is at rest.  Row 0 of ``a`` is the bottom of the picture."""
    z = np.clip(np.asarray(a, dtype=np.float64)[::-1] / scale, -1.0, 1.0)
    z = np.sign(z) * np.abs(z) ** 0.7                       # lift the faint parts of the field
    z = (z + 1.0) * 0.5 * (len(DIVERGE) - 1)
    i = np.minimum(z.astype(int), len(DIVERGE) - 2)
    f = (z - i)[..., None]
    rgb = (DIVERGE[i] * (1 - f) + DIVERGE[i + 1] * f).astype(np.uint8)
    if solid is not None:
        rgb[np.asarray(solid, dtype=bool)[::-1]] = wall
    return rgb


class FieldView(Group):
    """A film of a field in a plane (frames of pressure, row 0 at the bottom, covering ``extent`` metres).
    ``.tracker`` is the frame number; ``.point(x, y)`` is where a point in metres falls on the screen."""

    def __init__(self, frames: np.ndarray, extent: tuple[float, float], width: float = 7.0, scale: float | None = None,
                 solid=None, loop: bool = False, frame: bool = True, **kw):
        super().__init__(**kw)
        self.frames = np.asarray(frames)
        self.vmax = float(scale if scale is not None else np.percentile(np.abs(self.frames), 99.7) or 1.0)
        self.solid = solid
        self.extent = extent
        self.loop = loop
        self.image = ImageMobject(field_rgb(self.frames[0], self.vmax, solid))
        self.image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        self.image.width = width
        self.image.stretch_to_fit_height(width * extent[1] / extent[0])
        self.add(self.image)
        if frame:
            self.border = Rectangle(width=self.image.width, height=self.image.height, stroke_color=GREY_D,
                                    stroke_width=1.2).move_to(self.image)
            self.add(self.border)
        self.tracker = ValueTracker(0.0)
        self._shown = 0
        self.image.add_updater(self._update)

    def _update(self, m):
        n = len(self.frames)
        f = self.tracker.get_value()
        i = int(f) % n if self.loop else int(min(max(f, 0), n - 1))
        if i != self._shown:
            m.pixel_array[:, :, :3] = field_rgb(self.frames[i], self.vmax, self.solid)
            self._shown = i

    def point(self, x: float, y: float) -> np.ndarray:
        c, w, h = self.image.get_center(), self.image.width, self.image.height
        return c + np.array([(x / self.extent[0] - 0.5) * w, (y / self.extent[1] - 0.5) * h, 0.0])

    def start(self, fps: float = 6.0) -> "FieldView":
        """Let the film run by itself at ``fps`` frames a second from now on (slow motion under narration)."""
        self.stop()
        self._auto = lambda m, dt: m.increment_value(dt * fps)
        self.tracker.add_updater(self._auto)
        if self.tracker not in self.submobjects:
            self.add(self.tracker)
        return self

    def stop(self) -> "FieldView":
        if getattr(self, "_auto", None) is not None:
            self.tracker.remove_updater(self._auto)
            self._auto = None
        return self

    def run(self, seconds: float, to: float | None = None):
        """An animation that plays the film to frame ``to`` (the last by default) in ``seconds``."""
        return self.tracker.animate(run_time=seconds, rate_func=linear).set_value(len(self.frames) - 1 if to is None else to)


class ParcelRow(VGroup):
    """A row of parcels of air seen from the side: dots that slide along the row.  ``set_shape(xi)`` moves each dot
    by its displacement (in the units of ``gain`` screen units per unit)."""

    def __init__(self, n: int = 60, width: float = 10.0, rows: int = 5, gap: float = 0.16, color=AIR, radius=0.035,
                 gain: float = 1.0, **kw):
        super().__init__(**kw)
        self.n, self.width, self.rows, self.gain = n, width, rows, gain
        self.x0 = np.linspace(-width / 2, width / 2, n)
        self.dots = VGroup(*[Dot(radius=radius, color=color) for _ in range(n * rows)])
        self.ys = (np.arange(rows) - (rows - 1) / 2) * gap
        self.add(self.dots)
        self.origin = ORIGIN.copy()
        self.set_shape(np.zeros(n))

    def set_shape(self, xi) -> "ParcelRow":
        xi = np.asarray(xi, dtype=float)
        if len(xi) != self.n:
            xi = np.interp(np.linspace(0, 1, self.n), np.linspace(0, 1, len(xi)), xi)
        base = getattr(self, "_base", self.origin)
        k = 0
        for r in range(self.rows):
            for i in range(self.n):
                self.dots[k].move_to(base + np.array([self.x0[i] + self.gain * xi[i], self.ys[r], 0.0]))
                k += 1
        return self

    def place(self, point) -> "ParcelRow":
        """Put the row's rest position at ``point`` (use this, not ``move_to``: the dots are redrawn from it)."""
        self._base = np.array(point, dtype=float)
        return self.set_shape(np.zeros(self.n))

    def x(self, frac: float) -> np.ndarray:
        base = getattr(self, "_base", self.origin)
        return base + np.array([-self.width / 2 + frac * self.width, 0.0, 0.0])


class TubeView(VGroup):
    """A pipe seen in section, with the pressure inside drawn as a curve about its axis.  ``left``/``right`` are
    ``"open"`` or ``"closed"``; ``set_shape(p)`` takes the pressure along the pipe."""

    def __init__(self, width: float = 8.0, bore: float = 0.9, left: str = "open", right: str = "open", color=AIR,
                 scale: float = 0.36, wall=GREY_B, **kw):
        super().__init__(**kw)
        a, b = np.array([-width / 2, 0, 0]), np.array([width / 2, 0, 0])
        up = UP * bore / 2
        self.walls = VGroup(Line(a + up, b + up, color=wall, stroke_width=5), Line(a - up, b - up, color=wall, stroke_width=5))
        self.caps = VGroup()
        if left == "closed":
            self.caps.add(Line(a + up, a - up, color=wall, stroke_width=5))
        if right == "closed":
            self.caps.add(Line(b + up, b - up, color=wall, stroke_width=5))
        self.curve = VMobject(stroke_color=color, stroke_width=3.5)
        self.a, self.b, self.scale_, self.width_ = a, b, scale, width
        self.add(self.walls, self.caps, self.curve)
        self.set_shape(np.zeros(2))

    def p(self, frac: float, v: float = 0.0) -> np.ndarray:
        shift = self.walls.get_center()
        return shift + np.array([-self.width_ / 2 + frac * self.width_, self.scale_ * v, 0.0])

    def set_shape(self, v) -> "TubeView":
        v = np.asarray(v, dtype=float)
        fr = np.linspace(0, 1, len(v))
        self.curve.set_points_as_corners([self.p(f, u) for f, u in zip(fr, v)])
        return self

    def lens(self, shape, amp: float = 0.36, color=None, opacity: float = 0.3) -> Lens:
        """The blur of a standing wave of the given shape (pressure along the pipe) at full speed."""
        return Lens(self.p(0.0), self.p(1.0), amp=amp, color=color or AIR, opacity=opacity, shape=np.abs(shape),
                    n=max(48, len(shape)))


class Trace(VMobject):
    """A curve between two points whose height is set from data: ``set_shape(v)`` (so that :func:`film` can run a
    stored simulation through it)."""

    def __init__(self, start, end, scale: float = 1.0, color=AIR, stroke_width: float = 3.0, **kw):
        super().__init__(stroke_color=color, stroke_width=stroke_width, **kw)
        self.a, self.b, self.gain = np.array(start, dtype=float), np.array(end, dtype=float), scale
        self.set_shape(np.zeros(2))

    def set_shape(self, v) -> "Trace":
        v = np.asarray(v, dtype=float)
        fr = np.linspace(0, 1, len(v))
        self.set_points_as_corners([self.a + (self.b - self.a) * f + UP * self.gain * u for f, u in zip(fr, v)])
        return self


def bottle_shape(height: float = 3.0, body_w: float = 1.3, neck_w: float = 0.42, neck_h: float = 0.9, fill: float = 0.0,
                 glass="#9FB8AD", water="#3B82F6") -> VGroup:
    """A bottle in outline with water up to the fraction ``fill`` of its body.  ``.mouth`` is the top of the neck,
    ``.air`` the part of the body that is air (where its note comes from)."""
    bh = height - neck_h
    sh = 0.28                                           # the shoulder
    pts = [[-body_w / 2, 0, 0], [body_w / 2, 0, 0], [body_w / 2, bh - sh, 0], [neck_w / 2, bh, 0],
           [neck_w / 2, height, 0], [-neck_w / 2, height, 0], [-neck_w / 2, bh, 0], [-body_w / 2, bh - sh, 0]]
    outline = Polygon(*pts, stroke_color=glass, stroke_width=3, fill_color=glass, fill_opacity=0.06)
    g = VGroup(outline)
    if fill > 0:
        wh = max(0.02, min(fill, 1.0) * (bh - sh))
        g.add_to_back(Rectangle(width=body_w - 0.06, height=wh, stroke_width=0, fill_color=water, fill_opacity=0.55
                                ).move_to([0, wh / 2 + 0.02, 0]))
    g.shift(DOWN * height / 2)
    g.mouth = np.array([0.0, height / 2, 0.0])
    g.outline = outline
    return g


NUMBER_WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
                "seventeen eighteen nineteen twenty").split()


def open_chapter(scene, number: int, title: str, question: str, lit=(), part: int | None = None, links=None,
                 extra=(), spoken: str | None = None) -> None:
    """Show a chapter's card under its spoken title (``"Chapter three. A wave on a string."``) and take it away."""
    card = chapter_card(number, title, question, lit=lit, part=part, links=links, extra=extra)
    words = spoken or plain_title(title)
    with scene.voiceover(f"Chapter {NUMBER_WORDS[number]}. {words}."):
        scene.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
    scene.play(FadeOut(card))


def plain_title(title: str) -> str:
    from explainer.music.sound import plain

    return plain(title).rstrip(".?!")


# ---------------------------------------------------------------------------
# Shared by the parts from Part 4 on: frequency on a logarithmic axis, pictures with a playhead, boxes for the
# sounds of an ear question, a card for a demonstration
# ---------------------------------------------------------------------------
def hz_name(f: float) -> str:
    """A frequency for an axis: ``500``, ``1\\,k``, ``4.186\\,k`` (math mode)."""
    return rf"{f / 1000:g}\,\mathrm{{k}}" if f >= 1000 else f"{f:g}"


def faxes(f_lo, f_hi, y_range, x_length=8.0, y_length=3.4, ylabel="", yticks=None, fticks=(100, 1000, 10000),
          xlabel=r"frequency (Hz)", font_size=20, yfmt=None) -> VGroup:
    """Axes whose x is frequency on a logarithmic scale.  ``g.at(f, y)`` is the point for frequency f."""
    g = axes([np.log10(f_lo), np.log10(f_hi)], y_range, x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel,
             xticks=[float(np.log10(f)) for f in fticks], yticks=yticks, xfmt=lambda v: hz_name(float(round(10 ** v, 6))),
             yfmt=yfmt, font_size=font_size)
    g.at = lambda f, y: g.ax.c2p(float(np.log10(f)), y)
    return g


def fcurve(g, f, y, color, stroke_width=3):
    """A curve on :func:`faxes`."""
    return curve(g.ax, np.log10(np.asarray(f, dtype=float)), np.asarray(y, dtype=float), color, stroke_width=stroke_width)


def picture(a: np.ndarray, lo: float, hi: float, width: float, height: float) -> Group:
    """A stored picture of data (row 0 the lowest) with a thin frame; ``.playhead`` runs across it."""
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
    """Boxes that stand for the sounds of an ear question; :func:`pulse` lights one while its sound plays."""
    return VGroup(*[VGroup(RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2),
                           label(t, font_size=font_size, color=GREY_A)) for t in names]).arrange(RIGHT, buff=buff)


def pulse(snd, mob, t0: float, t1: float, rate: float = 18.0, color=None, buff: float = 0.1):
    """Light a frame around ``mob`` between clip times ``t0`` and ``t1`` (it flickers, so the picture is never still)."""
    glow = SurroundingRectangle(mob, color=color or EAR, buff=buff, stroke_width=4, corner_radius=0.12)
    snd.show(glow)
    snd.drive(glow, lambda m, t: m.set_stroke(opacity=(0.6 + 0.4 * np.sin(rate * t)) if t0 <= t < t1 else 0.0))
    return glow


def listen_note(text: str, color=None, width: float = 8.0, font_size=28) -> VGroup:
    """What to listen for in a demonstration (not one of a part's pause-and-listen questions: nothing to commit to,
    only something to notice)."""
    from explainer.ai.lecture import _body, _card

    color = color or EAR
    head = VGroup(speaker_icon(0.2, color), label(r"Listen for this", font_size=font_size - 6, color=color)).arrange(RIGHT, buff=0.18)
    return _card(head, _body(text, width - 0.8, font_size), color, width, accent=False)


def rows_card(rows, left: float = -6.2, text_left: float = -3.6, top: float = 2.1, step: float = 1.35, name_size: int = 30,
              text_size: int = 24, color=None) -> VGroup:
    """Rows of (name, text): the name at the left, what it means beside it.  ``.rows[i]`` is a row."""
    out = VGroup()
    for k, (name, text) in enumerate(rows):
        r = VGroup(label(name, font_size=name_size, color=color or TUNE), label(text, font_size=text_size, color=GREY_A))
        r[0].move_to(RIGHT * left, aligned_edge=LEFT)
        r[1].move_to(RIGHT * text_left, aligned_edge=LEFT)
        r.shift(UP * (top - step * k))
        out.add(r)
    return out
