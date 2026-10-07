"""Helpers shared by the Navier–Stokes scenes."""

from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as cm

from .simulate import load

# ---------------------------------------------------------------------------
# The equation, built from indexable, consistently colored parts.
# ---------------------------------------------------------------------------
NS_TEX = [
    r"\rho",  # 0
    r"\Big(",  # 1
    r"{\partial \vu \over \partial t}",  # 2
    r"+",  # 3
    r"(\vu \cdot \nabla)\vu",  # 4
    r"\Big)",  # 5
    r"=",  # 6
    r"-\nabla p",  # 7
    r"+",  # 8
    r"\mu \nabla^2 \vu",  # 9
    r"+",  # 10
    r"\vf",  # 11
]
I_RHO, I_DT, I_ADV, I_EQ, I_P, I_VISC, I_F = 0, 2, 4, 6, 7, 9, 11
NS_COLORS = {I_RHO: C.DENSITY, I_DT: C.TIME, I_ADV: C.ADVECT, I_P: C.PRESSURE, I_VISC: C.VISCOUS, I_F: C.FORCE}


def ns_equation(font_size=48) -> MathTex:
    eq = MathTex(*NS_TEX, font_size=font_size)
    for i, col in NS_COLORS.items():
        eq[i].set_color(col)
    return eq


def div_free(font_size=48) -> MathTex:
    eq = MathTex(r"\nabla \cdot \vu", r"=", r"0", font_size=font_size)
    eq[0].set_color(C.DIVERGENCE)
    return eq


def ns_system(font_size=48, buff=0.45) -> VGroup:
    return VGroup(ns_equation(font_size), div_free(font_size)).arrange(DOWN, buff=buff)


def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    return Tex(text, color=color, font_size=font_size, **kw)


def caption_box(mob: Mobject, color=WHITE, buff=0.18) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, stroke_width=2)


# ---------------------------------------------------------------------------
# Playing back precomputed simulations
# ---------------------------------------------------------------------------
class FieldMovie(ImageMobject):
    """An image whose pixels advance through precomputed simulation frames.

    Time advances in its own updater, so it keeps playing during any other
    animation. Use :meth:`fade` (not FadeIn) to change its opacity without
    freezing playback.
    """

    def __init__(self, render_frame, n_frames, fps=30, loop=True, start=0, rate=1.0, alpha=1.0, **kwargs):
        self.render_frame = render_frame
        self.n_frames = n_frames
        self.fps = fps
        self.loop = loop
        self.t = start / fps
        self.rate = rate
        self.alpha = alpha
        self._k = start
        super().__init__(self._rgba(start), **kwargs)
        self.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        self.add_updater(FieldMovie._tick)

    def _rgba(self, k):
        rgb = self.render_frame(k)
        a = np.full(rgb.shape[:2] + (1,), int(255 * self.alpha), np.uint8)
        return np.concatenate([rgb, a], axis=2)

    def frame_index(self) -> int:
        k = int(self.t * self.fps)
        return k % self.n_frames if self.loop else min(k, self.n_frames - 1)

    def set_alpha(self, alpha: float):
        self.alpha = float(np.clip(alpha, 0, 1))
        self.pixel_array[:, :, 3] = int(255 * self.alpha)
        return self

    @staticmethod
    def _tick(mob, dt):
        mob.t += dt * mob.rate
        k = mob.frame_index()
        if k != mob._k:
            mob._k = k
            mob.pixel_array = mob._rgba(k)

    def fade(self, to: float = 1.0, **kwargs) -> Animation:
        start = self.alpha

        def upd(m, a):
            m.set_alpha(start + (to - start) * a)

        return UpdateFromAlphaFunc(self, upd, suspend_mobject_updating=False, **kwargs)


CROP_INLET = 6  # lattice columns hidden at the inlet (boundary artifacts)


def cylinder_movie(name: str, mode: str = "vorticity", width: float = 13.5, vmax: float = 4.0, **kwargs) -> FieldMovie:
    data = load(name)
    vort, dye, solid = data["vorticity"], data["dye"], data["solid"][:, CROP_INLET:][::-1]

    def render(k):
        w = vort[k][:, CROP_INLET:][::-1]
        if mode == "dye":
            rgb = cm.dye_overlay(dye[k][:, CROP_INLET:][::-1], w, vmax)
        else:
            rgb = cm.diverging(w, vmax, gamma=0.9)
        return cm.to_uint8(cm.solid_mask(rgb, solid))

    movie = FieldMovie(render, len(vort), **kwargs)
    movie.width = width
    return movie


def cylinder_geometry(movie: FieldMovie, name: str) -> tuple[np.ndarray, float]:
    """Scene-space center and radius of the cylinder inside ``movie``."""
    data = load(name)
    ny, nx = data["solid"].shape
    nx -= CROP_INLET
    cx, cy = data["center"]
    scale = movie.width / nx
    x = movie.get_left()[0] + (cx - CROP_INLET + 0.5) * scale
    y = movie.get_bottom()[1] + (cy + 0.5) * scale
    return np.array([x, y, 0.0]), float(data["diameter"]) / 2 * scale


def square_movie(name: str, key: str, vmax: float, side: float = 6.0, mode: str = "diverging", dye_key=None, **kwargs):
    data = load(name)
    frames = data[key]
    dyes = data[dye_key] if dye_key else None

    def render(k):
        if mode == "dye":
            c = np.asarray(dyes[k], dtype=np.float32)
            w = np.asarray(frames[k], dtype=np.float32)
            base = cm.sequential(c, 0, 1, low=BACKGROUND, high="#2C6E91")
            glow = cm.diverging(w, vmax)
            rgb = 0.55 * base + 0.6 * glow
        else:
            rgb = cm.diverging(frames[k], vmax)
        return cm.to_uint8(rgb[::-1])

    movie = FieldMovie(render, len(frames), **kwargs)
    movie.height = side
    return movie


def frame_rect(mob: Mobject, color=GREY_C, stroke_width=1.5) -> Rectangle:
    return Rectangle(width=mob.width, height=mob.height, color=color, stroke_width=stroke_width).move_to(mob)


# ---------------------------------------------------------------------------
# Static scalar fields (e.g. pressure) as images
# ---------------------------------------------------------------------------
def heatmap(fn, x_range, y_range, resolution=200, colormap=None, opacity=1.0) -> ImageMobject:
    """Image of ``fn(x, y)`` (vectorized) covering the given scene rectangle."""
    (x0, x1), (y0, y1) = x_range, y_range
    ny = resolution
    nx = int(round(resolution * (x1 - x0) / (y1 - y0)))
    xs = np.linspace(x0, x1, nx)
    ys = np.linspace(y1, y0, ny)
    X, Y = np.meshgrid(xs, ys)
    Z = fn(X, Y)
    colormap = colormap or (lambda z: cm.sequential(z, Z.min(), Z.max(), mid="#4A2A5E"))
    rgb = cm.to_uint8(colormap(Z))
    a = np.full(rgb.shape[:2] + (1,), int(255 * opacity), np.uint8)
    img = ImageMobject(np.concatenate([rgb, a], axis=2))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    img.stretch_to_fit_width(x1 - x0).stretch_to_fit_height(y1 - y0)
    img.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    return img


def pressure_colormap(vmin, vmax):
    """Dark = low pressure, bright red = high pressure (red is the pressure color)."""
    return lambda z: cm.sequential(z, vmin, vmax, low="#0B0E16", mid="#5C1F2B", high="#F0624D")


# ---------------------------------------------------------------------------
# Small reusable mobjects
# ---------------------------------------------------------------------------
def parcel(side=0.5, color=C.VELOCITY) -> Square:
    return Square(side, color=WHITE, stroke_width=2.5, fill_color=color, fill_opacity=0.35)


def vector_arrow(start, vec, color=C.VELOCITY, scale=1.0, **kw) -> Arrow:
    start = np.array(start, dtype=float)
    vec = np.array(vec, dtype=float) * scale
    return Arrow(start, start + vec, buff=0, color=color, stroke_width=kw.pop("stroke_width", 5),
                 max_tip_length_to_length_ratio=kw.pop("tip_ratio", 0.3), **kw)


def chapter_title(number: int, text: str) -> VGroup:
    num = Tex(f"Part {number}", font_size=32, color=C.DIM)
    title = Tex(text, font_size=60)
    return VGroup(num, title).arrange(DOWN, buff=0.25)


# ---------------------------------------------------------------------------
# "Word equation" used as the roadmap: rho * accel = pressure + viscous + external
# ---------------------------------------------------------------------------
TEMPLATE_TEX = [
    r"\rho",
    r"\cdot",
    r"\text{acceleration}",
    r"\;=\;",
    r"\text{pressure}",
    r"\;+\;",
    r"\text{viscosity}",
    r"\;+\;",
    r"\text{external}",
]
T_RHO, T_ACC, T_EQ, T_P, T_VISC, T_F = 0, 2, 3, 4, 6, 8
TEMPLATE_COLORS = {T_RHO: C.DENSITY, T_ACC: WHITE, T_P: C.PRESSURE, T_VISC: C.VISCOUS, T_F: C.FORCE}


def template_equation(font_size=40, boxes=True) -> VGroup:
    eq = MathTex(*TEMPLATE_TEX, font_size=font_size)
    for i, col in TEMPLATE_COLORS.items():
        eq[i].set_color(col)
    group = VGroup(eq)
    if boxes:
        for i in (T_ACC, T_P, T_VISC, T_F):
            col = TEMPLATE_COLORS[i] if i != T_ACC else GREY_B
            group.add(SurroundingRectangle(eq[i], color=col, buff=0.1, corner_radius=0.06, stroke_width=2))
    return group


def move_movie(movie: "FieldMovie", center=None, width=None, **kwargs) -> Animation:
    """Move/resize a FieldMovie without pausing its playback (unlike ``.animate``)."""
    c0, w0 = movie.get_center().copy(), movie.width
    c1 = c0 if center is None else np.array(center, dtype=float)
    w1 = w0 if width is None else width

    def upd(m, a):
        m.width = w0 + (w1 - w0) * a
        m.move_to(c0 + (c1 - c0) * a)

    return UpdateFromAlphaFunc(movie, upd, suspend_mobject_updating=False, **kwargs)
