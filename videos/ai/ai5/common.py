"""Helpers shared by the scenes of Part 5 ("Randomness in Motion")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 5
MONO = "DejaVu Sans Mono"
DATA, MODEL = C.TRUE_P, C.MODEL_Q  # the data / the world (blue); a model, a proposal, a guess (orange)
NOISE = "#8B98A9"  # pure randomness
DRIFT = C.MODEL_Q  # the push in an SDE
SCORE = "#5BD17A"  # the score, grad log p
WALK = "#7FD3FF"  # random walkers


def normal_pdf(x, mu=0.0, s=1.0):
    return np.exp(-0.5 * ((np.asarray(x) - mu) / s) ** 2) / (s * math.sqrt(2 * math.pi))


def hist_shape(ax, edges, heights, color=DATA, opacity=0.55, stroke_width=2) -> VMobject:
    """A histogram as one filled outline (morphs smoothly into another histogram or a curve)."""
    pts = [ax.c2p(edges[0], 0)]
    for k, h in enumerate(heights):
        pts += [ax.c2p(edges[k], h), ax.c2p(edges[k + 1], h)]
    pts.append(ax.c2p(edges[-1], 0))
    return Polygon(*pts, color=color, stroke_width=stroke_width, fill_color=color, fill_opacity=opacity)


def curve(ax, xs, ys, color=WHITE, stroke_width=3) -> VMobject:
    return VMobject(color=color, stroke_width=stroke_width).set_points_smoothly([ax.c2p(x, y) for x, y in zip(xs, ys)])


def swarm(points, colors, radius=0.032, opacity=0.95) -> VGroup:
    """Particles as small dots; ``points`` is (n, 2)."""
    return VGroup(*[Dot([p[0], p[1], 0], radius=radius, color=c, fill_opacity=opacity, stroke_width=0)
                    for p, c in zip(points, colors)])


def follow(dots: VGroup, frames: np.ndarray, t: ValueTracker, scale=1.0, shift=ORIGIN):
    """Updater: put particle i at frames[t, i], interpolating between saved frames."""
    frames = np.asarray(frames) * scale
    off = np.asarray(shift)[:2]

    def upd(g):
        v = float(np.clip(t.get_value(), 0, len(frames) - 1))
        k = min(int(v), len(frames) - 2)
        a = v - k
        P = (1 - a) * frames[k] + a * frames[k + 1] + off
        for d, p in zip(g, P):
            d.move_to([p[0], p[1], 0])

    return upd


def ramp(values, c0=DATA, c1=C.BITS):
    lo, hi = float(np.min(values)), float(np.max(values))
    return [interpolate_color(ManimColor(c0), ManimColor(c1), (v - lo) / (hi - lo + 1e-12)) for v in values]


def printable(s: str) -> str:
    """GPT-2's samples, keeping only what a font can draw (it sometimes emits half of a multi-byte character)."""
    return " ".join("".join(c for c in s if c.isprintable() and ord(c) < 0x2000).split())


def density_picture(width=3.6, height=1.4, lo=0.3, hi=1.3) -> VGroup:
    """A jargon-card picture of a probability density: VGroup(axes, a coarse histogram of the standard bell, the
    bell, the area between ``lo`` and ``hi`` shaded, its label P), the last two hidden at first.  ``narrow_hist(pic)``
    is the same histogram with bars four times narrower, on the picture's axes wherever they now are."""
    ax = Axes(x_range=[-3, 3, 1], y_range=[0, 0.45, 0.1], x_length=width, y_length=height, tips=False,
              axis_config={"stroke_color": GREY_C, "include_ticks": False})
    ax.y_axis.set_stroke(opacity=0)
    edges = np.linspace(-3, 3, 7)
    hist = hist_shape(ax, edges, [float(normal_pdf((a + b) / 2)) for a, b in zip(edges, edges[1:])], color=DATA,
                      opacity=0.35, stroke_width=1.5)
    xs = np.linspace(-3, 3, 120)
    bell = curve(ax, xs, normal_pdf(xs), color=MODEL, stroke_width=3)
    xa = np.linspace(lo, hi, 40)
    shade = Polygon(ax.c2p(lo, 0), *[ax.c2p(x, float(normal_pdf(x))) for x in xa], ax.c2p(hi, 0), stroke_width=0,
                    fill_color=C.BITS, fill_opacity=0)
    p = MathTex(r"P", font_size=30, color=C.BITS).move_to(ax.c2p((lo + hi) / 2, 0.14)).set_opacity(0)
    return VGroup(ax, hist, bell, shade, p)


def narrow_hist(pic: VGroup) -> VMobject:
    ax = pic[0]
    edges = np.linspace(-3, 3, 25)
    return hist_shape(ax, edges, [float(normal_pdf((a + b) / 2)) for a, b in zip(edges, edges[1:])], color=DATA,
                      opacity=0.35, stroke_width=1.5)


HIST = C.HUMAN  # history: years, people


def heat_image(f, x_range, y_range, w=400, h=300) -> ImageMobject:
    """A density f(X, Y) on a grid as a picture, dark blue (0) to warm yellow (its maximum).  Part 7 uses it too
    (imported from ``videos.ai.ai5.s08_mcmc``, which re-exports it)."""
    xs = np.linspace(*x_range, w)
    ys = np.linspace(*y_range, h)[::-1]
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    Z = (Z / Z.max()) ** 0.8
    stops = [np.array(ManimColor(c).to_rgb()) for c in ("#0B0F17", "#1B2A6B", "#2E6FB0", "#3FB8AF", "#F2D16B")]
    k = np.clip(Z * (len(stops) - 1), 0, len(stops) - 1 - 1e-9)
    i = k.astype(int)
    a = (k - i)[..., None]
    rgb = (1 - a) * np.array(stops)[i] + a * np.array(stops)[np.minimum(i + 1, len(stops) - 1)]
    img = ImageMobject((np.concatenate([rgb, np.ones_like(a)], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    return img


def era_strip(events, y0=-0.2, color=None, font_size=21):
    """'How we got here': milestones evenly spaced along a line, alternately above and below (not to scale).
    Returns (axis, marks, skeleton): fade the skeleton in first, then each mark as the narration reaches it."""
    color = color or HIST
    n = len(events)
    xs = np.linspace(-5.9, 5.9, n)
    axis = Line([-6.6, y0, 0], [6.6, y0, 0], color=GREY_C, stroke_width=3)
    marks, skel = [], VGroup()
    for i, ((yr, txt), x) in enumerate(zip(events, xs)):
        up = i % 2 == 0
        stem = Line([x, y0, 0], [x, y0 + (0.9 if up else -0.9), 0], color=color, stroke_width=2.5)
        dot = Dot([x, y0, 0], radius=0.08, color=color)
        yl = label(str(yr), font_size=30, color=color)
        t = label(txt, font_size=font_size, color=WHITE)
        words = VGroup(yl, t).arrange(DOWN, buff=0.06)
        words.next_to(stem.get_end(), UP if up else DOWN, buff=0.08)
        keep_in_frame(words, margin=0.12)
        marks.append(VGroup(stem, dot, words))
        skel.add(VGroup(stem.copy().set_stroke(GREY_D), Dot([x, y0, 0], radius=0.06, color=GREY_D),
                        yl.copy().set_color(GREY_D).move_to(yl)))
    return axis, marks, skel


def surface_from_grid(axes, gx, gy, Z, zmax, colors=("#1B2A6B", "#2E6FB0", "#3FB8AF", "#F2D16B", "#F28C5B"),
                      opacity=0.85, resolution=None):
    """A density given on a grid (Z[j, i] at gx[i], gy[j]) as a 3D surface over ``axes`` (bilinear in between),
    coloured by height."""
    from scipy.interpolate import RegularGridInterpolator

    f = RegularGridInterpolator((gy, gx), np.asarray(Z), bounds_error=False, fill_value=0.0)
    res = resolution or (len(gx) - 1, len(gy) - 1)
    surf = Surface(lambda u, v: axes.c2p(u, v, float(f([[v, u]])[0])), u_range=[gx[0], gx[-1]],
                   v_range=[gy[0], gy[-1]], resolution=res, fill_opacity=opacity, stroke_width=0.3,
                   stroke_color="#0E1117", checkerboard_colors=False)
    surf.set_fill_by_value(axes=axes, colorscale=[(ManimColor(c), zmax * k / (len(colors) - 1))
                                                   for k, c in enumerate(colors)], axis=2)
    return surf


class ParticleFlow(VGroup):
    """Particles moving in the plane (``frames``: (T, n, 2) saved positions), drawn as dots on the floor of 3D
    ``axes`` (or on 2D axes), with a time tracker ``flow.t`` (in saved frames) that moves them, interpolating
    between frames.  ``flow.density(k)`` would be the surface; the scene keeps those separately."""

    def __init__(self, axes, frames, colors=None, radius=0.03, opacity=0.9, z=0.0):
        super().__init__()
        self.ax, self.frames, self.z = axes, np.asarray(frames, float), z
        n = self.frames.shape[1]
        colors = colors or [WALK] * n
        self.t = ValueTracker(0.0)
        self.dots = VGroup(*[Dot(radius=radius, color=c, fill_opacity=opacity, stroke_width=0) for c in colors])
        self.add(self.dots)
        self._place()

    def _place(self):
        v = float(np.clip(self.t.get_value(), 0, len(self.frames) - 1))
        k = min(int(v), len(self.frames) - 2)
        a = v - k
        P = (1 - a) * self.frames[k] + a * self.frames[k + 1]
        for d, p in zip(self.dots, P):
            d.move_to(self.ax.c2p(p[0], p[1], self.z) if len(self.ax.c2p(0, 0)) == 3 and hasattr(self.ax, "z_axis")
                      else self.ax.c2p(p[0], p[1]))

    def start(self):
        self.dots.add_updater(lambda m: self._place())
        return self

    def stop(self):
        self.dots.clear_updaters()
        return self
