"""Helpers shared by the scenes of Part 1 ("One String")."""

from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music.monochord import Clip

from .compute import BETA, CACHE, CLIPS, IDEAL, STRING, load  # noqa: F401

PART = 1
clip = clip_loader(CACHE, CLIPS)

# one meaning per colour, for the whole part (the series' palette, explainer/music/palette.py)
TUNE = MC.TUNE      # the Tune, and whatever is sounding now
STR = MC.STRING     # the string
RATIO = MC.RATIO    # ratios and lengths
FREQ = MC.FREQ      # frequency
TIME = MC.TIME      # time, periods
LEVEL = MC.LEVEL    # amplitude and level
FORCE = MC.FORCE    # forces, tension
MASS = MC.MASS      # mass
RIGHT_C = MC.RIGHT  # the wave going right
LEFT_C = MC.LEFT    # the wave going left
NODE = MC.NODE      # nodes
GOOD = MC.SMOOTH    # agrees, coincides
BAD = MC.ROUGH      # false, clashes
HIST = MC.HUMAN     # people and dates
EAR = MC.EAR        # listening
LIMIT = MC.LIMIT    # the frontier


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
    """``fn(lens, t)`` for :meth:`SoundTracker.drive`: the blur of a string plucked at clip time ``at``, dying at
    ``rate`` per second, gone before ``at`` and (if given) after ``stop_at``."""
    def fn(m, t):
        if t < at or (stop_at is not None and t >= stop_at):
            m.set_amp(0.0)
        else:
            m.set_amp(float(np.exp(-rate * (t - at))))
    return fn


# ---------------------------------------------------------------------------
# Things from the legend
# ---------------------------------------------------------------------------
def anvil_shape(width=2.6, color="#7B8794") -> VGroup:
    """An anvil: a horn, a face, a waist and a foot."""
    pts = [[-1.3, 0.45, 0], [0.75, 0.45, 0], [0.75, 0.3, 0], [1.3, 0.3, 0], [0.75, 0.05, 0], [0.4, 0.0, 0],
           [0.25, -0.35, 0], [0.7, -0.6, 0], [0.7, -0.8, 0], [-0.7, -0.8, 0], [-0.7, -0.6, 0], [-0.25, -0.35, 0],
           [-0.4, 0.0, 0], [-0.9, 0.2, 0]]
    a = Polygon(*pts, stroke_color=GREY_A, stroke_width=2, fill_color=color, fill_opacity=0.9)
    return VGroup(a).scale(width / 2.6)


def hammer(weight: int, size=1.0, color=GREY_B) -> VGroup:
    """A smith's hammer whose head grows with its weight, the weight written on it."""
    w = 0.34 + 0.035 * weight
    head = RoundedRectangle(width=w * 1.5, height=w, corner_radius=0.05, stroke_color=GREY_A, stroke_width=1.5,
                            fill_color=color, fill_opacity=0.95)
    handle = Rectangle(width=0.1, height=1.25, stroke_width=0, fill_color="#9A6B3F", fill_opacity=1)
    handle.next_to(head, DOWN, buff=0)
    num = label(str(weight), font_size=30, color=BLACK).move_to(head)
    g = VGroup(handle, head, num).scale(size)
    g.head, g.num = head, num
    return g


def weight_block(n: int, unit=0.17, color=MASS) -> VGroup:
    """A hanging weight of ``n`` units, the number on it."""
    h = 0.42 + unit * n ** 0.5
    body = Polygon([-0.3, 0, 0], [0.3, 0, 0], [0.42, -h, 0], [-0.42, -h, 0], stroke_color=GREY_A, stroke_width=1.5,
                   fill_color=color, fill_opacity=0.9)
    hook = Line([0, 0.16, 0], [0, 0, 0], color=GREY_A, stroke_width=2)
    num = label(str(n), font_size=28, color=BLACK).move_to(body)
    g = VGroup(hook, body, num)
    g.num = num
    return g


def hung_string(n: int, width=4.6, color=STR) -> VGroup:
    """A string fixed at the left, over a pulley at the right, with a weight of ``n`` units hanging from it."""
    a, b = np.array([-width / 2, 0, 0]), np.array([width / 2, 0, 0])
    post = Polygon(a + [-0.12, -0.3, 0], a + [0.12, -0.3, 0], a, stroke_width=0, fill_color=GREY_A, fill_opacity=1)
    wheel = Circle(radius=0.16, stroke_color=GREY_A, stroke_width=2).move_to(b + [0.0, -0.16, 0])
    s = Line(a, b, color=color, stroke_width=3.5)
    drop = Line(b + [0.16, -0.16, 0], b + [0.16, -0.7, 0], color=color, stroke_width=3.5)
    w = weight_block(n).next_to(drop, DOWN, buff=0).shift(DOWN * 0.0)
    g = VGroup(post, wheel, s, drop, w)
    g.string, g.weight, g.a, g.b = s, w, a, b
    return g


def hung_lens(h: VGroup, amp=0.16, color=TUNE) -> Lens:
    return Lens(h.string.get_start(), h.string.get_end(), amp=amp, color=color)


# ---------------------------------------------------------------------------
# Two strings side by side
# ---------------------------------------------------------------------------
class PairView(VGroup):
    """Two monochords, one above the other: the open string and the string stopped at ``stop``.  ``play(snd)`` makes
    them ring on a clip's events ``a`` (the open string), ``b`` (the stopped one) and ``both``."""

    def __init__(self, stop: float, width: float = 8.6, gap: float = 0.75, ruler: bool = False, **kw):
        super().__init__(**kw)
        self.top = MonochordView(width=width, ruler=ruler)
        self.bottom = MonochordView(width=width, stop=stop, ruler=ruler)
        VGroup(self.top, self.bottom).arrange(DOWN, buff=gap)
        self.stop = stop
        self.add(self.top, self.bottom)

    def lenses(self, amp: float = 0.17) -> tuple[Lens, Lens]:
        return self.top.lens(1.0, amp=amp, color=STR), self.bottom.lens(self.stop, amp=amp, color=TUNE)

    def play(self, scene, snd, events=("a", "b", "both"), rate: float = 1.6, prefix: str = ""):
        a, b, both = (snd.time_of(prefix + e) for e in events)
        la, lb = self.lenses()
        scene.add(la, lb)
        snd.show(la, lb)

        def fa(m, t):
            m.set_amp(float(np.exp(-rate * (t - a))) if a <= t < b else
                      (float(np.exp(-rate * (t - both))) if t >= both else 0.0))

        def fb(m, t):
            m.set_amp(float(np.exp(-rate * (t - b))) if b <= t < both else
                      (float(np.exp(-rate * (t - both))) if t >= both else 0.0))

        snd.drive(la, fa)
        snd.drive(lb, fb)
        return la, lb


# ---------------------------------------------------------------------------
# Filming a simulation that makes no sound of its own (slow motion under narration)
# ---------------------------------------------------------------------------
def film(view: StringView, frames: np.ndarray, gain: float = 1.0, step: int = 2, loop: bool = False) -> ValueTracker:
    """Attach stored shapes to a StringView.  The returned tracker's value is the frame number (fractions
    interpolate): ``self.play(tr.animate.set_value(120), rate_func=linear, run_time=6)`` plays the film.  With
    ``loop`` the frames are one period (the last equals the first) and the film goes round."""
    fr = frames[:, ::step] if (frames.shape[1] - 1) % step == 0 else frames
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
    view.film_updater = upd
    return tr


def film_many(pairs, gain: float = 1.0, step: int = 1, loop: bool = False) -> ValueTracker:
    """One tracker for several StringViews: ``pairs`` is ``[(view, frames), ...]`` with equally many frames each."""
    tr = ValueTracker(0.0)
    for view, frames in pairs:
        fr = frames[:, ::step] if (frames.shape[1] - 1) % step == 0 else frames
        n = len(fr)

        def upd(m, view=view, fr=fr, n=n):
            f = tr.get_value() % (n - 1) if loop else tr.get_value()
            f = min(max(f, 0.0), n - 1.000001)
            i = int(f)
            a = f - i
            view.set_shape(gain * ((1 - a) * fr[i] + a * fr[i + 1]))

        upd(view)
        view.add_updater(upd)
    return tr
