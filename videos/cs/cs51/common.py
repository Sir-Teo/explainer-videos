"""Helpers shared by the scenes of Part 51 ("Light and Pixels")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs31.common import BG, DATA, HEAD, KERN, LAM, NO, YES  # noqa: F401
from videos.cs.cs37.common import axes, trace  # noqa: F401
from videos.cs.cs40.common import code_block, module_box  # noqa: F401

from .compute import load  # noqa: F401

PART = 51


def tag_box(text: str, color=DATA, size=18, w=None, h=0.5):
    """A DOM node or a token drawn as a rounded box with monospace text."""
    t = mono(text, size=size, color=color)
    box = RoundedRectangle(width=w or t.width + 0.35, height=h, corner_radius=0.08, stroke_color=color,
                           stroke_width=1.6, fill_color=BG, fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


def timeline_bar(x0: float, x1: float, y: float, color, h=0.32, scale=1.0, label_text=None, size=14):
    """A span of time on a horizontal timeline (x in scene units), optionally labelled inside."""
    r = Rectangle(width=max(0.02, (x1 - x0) * scale), height=h, stroke_width=0, fill_color=color, fill_opacity=0.85)
    r.move_to([x0 * scale + (x1 - x0) * scale / 2, y, 0])
    if label_text:
        t = label(label_text, font_size=size, color=BLACK)
        if t.width < r.width - 0.05:
            t.move_to(r)
            return VGroup(r, t)
    return VGroup(r)


def image(arr, height: float = 3.0, nearest: bool = True):
    """An ImageMobject from a cached uint8 array (H x W x 3 or H x W), with a thin frame."""
    import numpy as np
    a = np.asarray(arr)
    if a.ndim == 2:
        a = np.stack([a] * 3, axis=-1)
    if a.shape[-1] == 3:
        a = np.concatenate([a, np.full(a.shape[:2] + (1,), 255, np.uint8)], axis=-1)
    img = ImageMobject(a.astype(np.uint8))
    if nearest:
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.height = height
    return Group(img, SurroundingRectangle(img, buff=0.0, color=GREY_D, stroke_width=1.2))


# A side view of the series' box (illustrative): the open front on the left, the back wall on the right, the floor,
# the ceiling with its light, a mirror ball and a matte ball.  Scene units of the left part of the frame.
X0, X1, Y0, Y1 = -5.6, -1.0, -2.7, 1.9
LX0, LX1 = -3.875, -2.725
EYE = np.array([-6.5, -0.4])
SPH = [(np.array([-3.3, -1.95]), 0.75, "mirror"), (np.array([-1.75, -2.2]), 0.5, "diffuse")]


def hit(o, d):
    """Nearest hit t > 0 of the ray o + t d (d unit) in the side view: (t, kind, normal) or None (it leaves through
    the open front)."""
    best = None
    for c, r, kind in SPH:
        oc = o - c
        b = d @ oc
        disc = b * b - (oc @ oc - r * r)
        if disc < 0:
            continue
        for t in (-b - math.sqrt(disc), -b + math.sqrt(disc)):
            if t > 1e-6:
                if best is None or t < best[0]:
                    best = (t, kind, (o + t * d - c) / r)
                break
    for axis, val, nrm, lo, hi, kind in ((1, Y0, (0, 1), X0, X1, "floor"), (1, Y1, (0, -1), X0, X1, "ceiling"),
                                         (0, X1, (-1, 0), Y0, Y1, "back")):
        if abs(d[axis]) < 1e-12:
            continue
        t = (val - o[axis]) / d[axis]
        if t <= 1e-6:
            continue
        p = o + t * d
        if lo - 1e-9 <= p[1 - axis] <= hi + 1e-9 and (best is None or t < best[0]):
            k2 = "light" if kind == "ceiling" and LX0 <= p[0] <= LX1 else kind
            best = (t, k2, np.array(nrm, float))
    return best


def end_of(o, d):
    """Where a ray ends: its hit point, or the box's open front."""
    h = hit(o, d)
    if h is not None:
        return o + h[0] * d, h
    t = (X0 - 0.3 - o[0]) / d[0] if d[0] < 0 else 3.0
    return o + t * d, None


def cos_dir(n, u):
    """A 2D cosine-weighted direction about the normal n: sin(angle) = 2u - 1."""
    a = math.asin(2 * u - 1)
    t = np.array([n[1], -n[0]])
    return math.cos(a) * n + math.sin(a) * t


def random_path(o, d, rng, max_b=6):
    """A path: diffuse bounces in cosine-weighted directions, mirror bounces exact, until it reaches the light."""
    pts, kinds = [o], []
    for _ in range(max_b):
        h = hit(o, d)
        if h is None:
            pts.append(end_of(o, d)[0])
            kinds.append("out")
            break
        t, kind, n = h
        p = o + t * d
        pts.append(p)
        kinds.append(kind)
        if kind == "light":
            break
        d = d - 2 * (d @ n) * n if kind == "mirror" else cos_dir(n, rng.random())
        o = p + 1e-6 * n
    return pts, kinds


def P(v):
    return np.array([v[0], v[1], 0.0])


def box2d(eye=True):
    """The side view: walls, light, balls, eye."""
    walls = VGroup(Line(P((X0, Y0)), P((X1, Y0)), color=GREY_B, stroke_width=3),
                   Line(P((X0, Y1)), P((X1, Y1)), color=GREY_B, stroke_width=3),
                   Line(P((X1, Y0)), P((X1, Y1)), color=GREY_B, stroke_width=3))
    light = Line(P((LX0, Y1 - 0.02)), P((LX1, Y1 - 0.02)), color=HEAD, stroke_width=9)
    balls = VGroup(Circle(radius=SPH[0][1], color=GREY_A, stroke_width=2.5, fill_color=GREY_A,
                          fill_opacity=0.15).move_to(P(SPH[0][0])),
                   Circle(radius=SPH[1][1], color=WHITE, stroke_width=2.5, fill_color=GREY_B,
                          fill_opacity=0.35).move_to(P(SPH[1][0])))
    names = VGroup(label(r"mirror", font_size=16, color=GREY_A).move_to(P(SPH[0][0])),
                   label(r"light", font_size=16, color=HEAD).next_to(light, UP, buff=0.08),
                   label(r"open front", font_size=16, color=GREY_C).rotate(PI / 2).move_to(P((X0 - 0.15, 0.6))))
    g = VGroup(walls, light, balls, names)
    if eye:
        g.add(Dot(P(EYE), radius=0.09, color=WHITE), label(r"eye", font_size=16, color=GREY_A).next_to(
            P(EYE), DOWN, buff=0.12))
    return g


def path_mob(pts, color=WHITE, width=3, dots=True):
    g = VGroup(*[Line(P(a), P(b), color=color, stroke_width=width) for a, b in zip(pts, pts[1:])])
    if dots:
        g.add(*[Dot(P(p), radius=0.06, color=color) for p in pts[1:-1]])
    return g


def to_linear(u8):
    """Undo the cached images' display transform (sRGB, then Reinhard x / (1 + x)) to get radiance back."""
    s = np.asarray(u8, float) / 255.0
    x = np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)
    x = np.clip(x, 0, 0.9995)
    return x / (1 - x)


def to_display(L):
    """Radiance to 8-bit sRGB with the same Reinhard curve as the instrument (path.to_srgb8)."""
    x = L / (1 + L)
    s = np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)
    return np.round(np.clip(s, 0, 1) * 255).astype(np.uint8)
