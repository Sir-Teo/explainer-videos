"""Helpers shared by the quantum-mechanics scenes.

The visual language, kept the same in every scene:

* A complex amplitude psi is drawn with its **phase as hue** (``colormap.hue_rgb``: 0 red, pi/2 yellow-green,
  pi cyan, 3pi/2 violet) and its **size as height or brightness**.  A small phase wheel sits in a corner
  whenever phase colors are on screen.
* :class:`WaveView` draws a 1D wavefunction on Axes: a filled area whose height is |psi|^2 (or |psi|, or a
  signed real part) and whose color at each x is the phase of psi there, under a thin white outline.
* :class:`Projector` is a tiny orthographic 3D camera (azimuth / elevation) used for the complex helix
  (x, Re psi, Im psi) and the Bloch sphere.  Everything stays 2D Manim, so the narration-driven
  ``VoiceoverScene`` works unchanged.
* :class:`FieldMovie2D` plays back the double-slit simulation, phase-colored.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.ndimage import gaussian_filter

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as fcm

from . import colormap as qcm
from .compute import load, slit_frames  # noqa: F401

# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
WIDE_TEX = TEX_TEMPLATE.copy()
WIDE_TEX.add_to_preamble(r"\setlength{\textwidth}{40cm}")
MAX_TEXT_WIDTH = 13.6


def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    """A Tex label that never wraps on its own (line breaks are explicit) and shrinks to fit the frame."""
    kw.setdefault("tex_template", WIDE_TEX)
    t = Tex(text, color=color, font_size=font_size, **kw)
    if t.width > MAX_TEXT_WIDTH:
        t.width = MAX_TEXT_WIDTH
    return t


def note(text: str, font_size=22, color=GREY_B) -> Tex:
    """Small grey caption, e.g. a source line or 'simulated'."""
    return label(text, font_size=font_size, color=color)


def mtex(*tex: str, color=WHITE, font_size=36, **kw) -> MathTex:
    return MathTex(*tex, color=color, font_size=font_size, **kw)


def tagged(text: str, color=WHITE, font_size=28, opacity=0.85) -> Tex:
    t = label(text, color=color, font_size=font_size)
    t.add_background_rectangle(color=BACKGROUND, opacity=opacity, buff=0.06)
    return t


def boxed(mob: Mobject, color=YELLOW, buff=0.25, fill=0.0) -> VGroup:
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12, stroke_width=2.5)
    if fill:
        box.set_fill(color, opacity=fill)
    return VGroup(box, mob)


def part_card(number: int, title: str, subtitle: str = "") -> VGroup:
    num_ = label(rf"Part {number}", font_size=34, color=C.DIM)
    t = label(title, font_size=60)
    g = VGroup(num_, t)
    if subtitle:
        g.add(label(subtitle, font_size=32, color=GREY_A))
    return g.arrange(DOWN, buff=0.3)


def sim_tag(text=r"simulated", corner=DR) -> Tex:
    return note(text).to_corner(corner, buff=0.3)


def num(x: float, digits=3, sign=False) -> str:
    s = f"{x:+.{digits}f}" if sign else f"{x:.{digits}f}"
    return s.replace("-", "{-}")


def fmt_int(n: int) -> str:
    """12345678 -> '12{,}345{,}678' for MathTex."""
    return f"{int(n):,}".replace(",", "{,}")


def sci(x: float, digits=2) -> str:
    """3.5e-05 -> '3.5\\times 10^{-5}' for MathTex."""
    m, e = f"{x:.{digits - 1}e}".split("e")
    return rf"{m}\times 10^{{{int(e)}}}"


def stack(*lines: Mobject, buff=0.4, align=None) -> VGroup:
    """Stack derivation lines vertically; ``align``: index of the submobject (e.g. the '=') to line up."""
    g = VGroup(*lines).arrange(DOWN, buff=buff)
    if align is not None:
        x0 = lines[0][align].get_center()[0]
        for m in lines[1:]:
            m.shift((x0 - m[align].get_center()[0]) * RIGHT)
    return g


def why(mob: Mobject, text: str, color=GREY_B, font_size=24, direction=RIGHT, buff=0.3) -> Tex:
    """A small grey 'why this step' note next to a derivation line."""
    return label(text, font_size=font_size, color=color).next_to(mob, direction, buff=buff)


def place_whys(lines, whys, gap=0.45, right=6.9, left=-6.9):
    """Put each 'why' note in one column just right of the widest derivation line, at that line's height; if the
    column would leave the frame, slide the derivation left (never past ``left``) and shrink the notes if needed."""
    lines = [m for m in lines]
    xr = max(m.get_right()[0] for m in lines)
    wmax = max(w.width for w in whys)
    over = xr + gap + wmax - right
    if over > 0:
        room = min(m.get_left()[0] for m in lines) - left
        shift = min(over, max(room, 0))
        VGroup(*lines).shift(LEFT * shift)
        xr -= shift
        if over > shift:
            f = (right - xr - gap) / wmax
            for w in whys:
                w.scale(f)
    for m, w in zip(lines, whys):
        w.next_to(np.array([xr + gap, m.get_y(), 0]), RIGHT, buff=0)
    return whys


def num_table(header: list[str], rows: list[list[str]], font_size=30, col_colors=None, h_buff=0.55, v_buff=0.22):
    """A small table of MathTex cells: header row, a rule, then rows.  Returns a VGroup with .header, .rule,
    .rows (list of VGroups of cells) and .cols (list of VGroups, header included) for staged reveals."""
    cols = len(header)
    cells = [[MathTex(h, font_size=font_size, color=GREY_A) for h in header]]
    for r in rows:
        cells.append([MathTex(c, font_size=font_size, color=(col_colors[j] if col_colors else WHITE))
                      for j, c in enumerate(r)])
    widths = [max(cells[i][j].width for i in range(len(cells))) for j in range(cols)]
    xs = np.cumsum([0] + [w + h_buff for w in widths[:-1]])
    height = max(c.height for row in cells for c in row)
    grid = VGroup()
    for i, row in enumerate(cells):
        y = -i * (height + v_buff) - (0.15 if i else 0)
        for j, c in enumerate(row):
            c.move_to([xs[j] + widths[j] / 2, y, 0])
        grid.add(VGroup(*row))
    rule = Line([-0.1, -(height + v_buff) / 2 - 0.05, 0], [xs[-1] + widths[-1] + 0.1, -(height + v_buff) / 2 - 0.05, 0],
                color=GREY_D, stroke_width=1.5)
    t = VGroup(grid, rule)
    t.header, t.rule, t.rows = grid[0], rule, list(grid[1:])
    t.cols = [VGroup(*[grid[i][j] for i in range(len(cells))]) for j in range(cols)]
    return t


# ---------------------------------------------------------------------------
# Color
# ---------------------------------------------------------------------------
def hue(phase: float) -> ManimColor:
    """The phase color of a single complex number's argument."""
    return ManimColor.from_rgb(tuple(float(v) for v in qcm.hue_rgb(np.array([phase]))[0]))


def phase_wheel(radius=0.42, n=72, labels=True, title=True) -> VGroup:
    """Legend: the phase of psi -> hue.  An annulus, with 0 (right), pi/2 (top), pi, 3pi/2 marked."""
    g = VGroup()
    for k in range(n):
        a0 = 2 * PI * k / n
        g.add(AnnularSector(inner_radius=radius * 0.58, outer_radius=radius, angle=2 * PI / n + 0.002, start_angle=a0,
                            fill_color=hue(a0 + PI / n), fill_opacity=1, stroke_width=0))
    out = VGroup(g)
    if labels:
        for ang, s in ((0, "0"), (PI / 2, r"\tfrac{\pi}{2}"), (PI, r"\pi"), (3 * PI / 2, r"\tfrac{3\pi}{2}")):
            out.add(MathTex(s, font_size=18, color=GREY_B).move_to(
                (radius + 0.17) * np.array([math.cos(ang), math.sin(ang), 0])))
    if title:
        out.add(MathTex(r"\arg\psi", font_size=22, color=GREY_B).next_to(g, DOWN, buff=0.27 if labels else 0.1))
    return out


def corner_wheel(corner=UR, buff=0.35, **kw) -> VGroup:
    return phase_wheel(**kw).to_corner(corner, buff=buff)


# ---------------------------------------------------------------------------
# Raster images driven by trackers (fills, fields, particle clouds)
# ---------------------------------------------------------------------------
class Raster(ImageMobject):
    """An image redrawn by ``draw(value) -> RGBA uint8`` whenever its tracker(s) change value.

    Fades go through :meth:`fade` (the alpha is applied on top of whatever ``draw`` returns), so playback
    keeps running during them.  ``clear_scene`` removes the updater before fading it out.
    """

    def __init__(self, draw, tracker, width: float, height: float, center=ORIGIN, alpha=1.0, **kw):
        self.draw = draw
        self.trackers = list(tracker) if isinstance(tracker, (list, tuple)) else [tracker]
        self.tracker = self.trackers[0]
        self.alpha = alpha
        self._v = self._values()
        super().__init__(self._render(self._v), **kw)
        self.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        self.stretch_to_fit_width(width).stretch_to_fit_height(height).move_to(center)
        self.add_updater(Raster._tick)

    def _values(self):
        return tuple(t.get_value() for t in self.trackers)

    def _render(self, v):
        img = self.draw(v[0] if len(v) == 1 else v)
        if self.alpha < 1:
            img = img.copy()
            img[..., 3] = (img[..., 3] * self.alpha).astype(np.uint8)
        return img

    def refresh(self):
        self._v = self._values()
        self.pixel_array = self._render(self._v)
        return self

    @staticmethod
    def _tick(m):
        if m._values() != m._v:
            m.refresh()

    def fade_to(self, to: float = 1.0, **kwargs) -> Animation:
        start = self.alpha

        def upd(m, a):
            m.alpha = start + (to - start) * a
            m.refresh()

        return UpdateFromAlphaFunc(self, upd, suspend_mobject_updating=False, **kwargs)


def image_on(ax: Axes, rgba: np.ndarray, x_range, y_range) -> ImageMobject:
    """A static image covering the data rectangle x_range x y_range of ``ax``."""
    img = ImageMobject(rgba)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    p0, p1 = ax.c2p(x_range[0], y_range[0]), ax.c2p(x_range[1], y_range[1])
    img.stretch_to_fit_width(abs(p1[0] - p0[0])).stretch_to_fit_height(abs(p1[1] - p0[1])).move_to((p0 + p1) / 2)
    return img


def splat(xs, ys, extent, shape, sigma=1.3, weights=None) -> np.ndarray:
    """Deposit points bilinearly into a (H, W) grid and blur; one isolated point peaks at 1."""
    H, W = shape
    x0, x1, y0, y1 = extent
    px = (np.asarray(xs, float) - x0) / (x1 - x0) * (W - 1)
    py = (y1 - np.asarray(ys, float)) / (y1 - y0) * (H - 1)
    w = np.ones_like(px) if weights is None else np.asarray(weights, float)
    ok = (px >= 0) & (px < W - 1) & (py >= 0) & (py < H - 1)
    px, py, w = px[ok], py[ok], w[ok]
    ix, iy = px.astype(int), py.astype(int)
    fx, fy = px - ix, py - iy
    img = np.zeros((H, W))
    np.add.at(img, (iy, ix), w * (1 - fx) * (1 - fy))
    np.add.at(img, (iy, ix + 1), w * fx * (1 - fy))
    np.add.at(img, (iy + 1, ix), w * (1 - fx) * fy)
    np.add.at(img, (iy + 1, ix + 1), w * fx * fy)
    return gaussian_filter(img, sigma) * (2 * np.pi * sigma * sigma)


def glow(intensity, color, gain=1.6, white=0.55, alpha=1.0) -> np.ndarray:
    """Intensity -> RGBA uint8: the color fades in with intensity and turns whiter where points pile up."""
    a = 1 - np.exp(-gain * intensity)
    hot = np.clip((intensity - 1.0) / 6.0, 0, 1)[..., None] * white
    c = np.array(ManimColor(color).to_rgb(), dtype=np.float32)
    rgb = c + (1 - c) * hot
    return fcm.to_uint8(np.concatenate([rgb, (a * alpha)[..., None]], axis=2))


# ---------------------------------------------------------------------------
# 1D wavefunctions
# ---------------------------------------------------------------------------
def wave_axes(x_range, y_range, x_length=11.0, y_length=3.2, y_axis=False, **kw) -> Axes:
    """Axes for wave plots.  The y axis is hidden by default: Manim draws it through x = 0, which would cut a
    vertical line through the middle of a symmetric plot.  Label the vertical quantity with :func:`ylabel`."""
    cfg = {"stroke_color": GREY_B, "stroke_width": 2, "include_ticks": False}
    ax = Axes(x_range=list(x_range) + ([1] if len(x_range) == 2 else []),
              y_range=list(y_range) + ([1] if len(y_range) == 2 else []), x_length=x_length, y_length=y_length,
              tips=False, axis_config=cfg, **kw)
    if not y_axis:
        ax.y_axis.set_stroke(opacity=0)
    return ax


def ylabel(ax: Axes, tex: str, color=WHITE, font_size=30) -> MathTex:
    """The label of a wave plot's vertical quantity, at the top-left corner of the plotting area."""
    return MathTex(tex, font_size=font_size, color=color).next_to(ax.c2p(ax.x_range[0], ax.y_range[1]), RIGHT, buff=0.1)


def polyline(ax: Axes, xs, ys, color=WHITE, stroke_width=3, **kw) -> VMobject:
    pts = ax.c2p(np.asarray(xs, float), np.asarray(ys, float)).T
    m = VMobject(color=color, stroke_width=stroke_width, **kw)
    m.set_points_as_corners(pts)
    return m


def _fill_rgba(vals_px, phases, H, opacity, base_px, mags=None):
    """Columns filled from ``base_px`` (pixel height of the baseline above the bottom) to ``vals_px``; the color of
    each column is the hue of its phase.  Antialiased at the edge."""
    W = len(vals_px)
    lo = np.minimum(vals_px, base_px)[None, :]
    hi = np.maximum(vals_px, base_px)[None, :]
    yb = (H - 1 - np.arange(H))[:, None].astype(np.float32)  # pixel row r spans heights [yb, yb + 1]
    cov = np.clip(np.minimum(yb + 1, hi) - np.maximum(yb, lo), 0, 1)
    col = qcm.hue_rgb(phases)  # (W, 3)
    rgb = np.broadcast_to(col[None, :, :], (H, W, 3))
    a = cov * opacity
    if mags is not None:
        a = a * mags[None, :]
    return np.concatenate([fcm.to_uint8(rgb), fcm.to_uint8(a)[..., None]], axis=2)


class WaveView(Group):
    """A 1D wavefunction on ``ax``: a phase-colored fill under the curve plus a white outline.

    ``mode``: "density" (height |psi|^2 * scale), "abs" (|psi| * scale) or "real" (signed Re psi * scale,
    filled from the baseline).  The fill's hue at each x is arg psi(x).  ``base`` lifts the baseline (to stand the
    wave on an energy level).  Call :meth:`set_psi` to redraw, or use :meth:`follow` to drive it from a tracker.
    """

    def __init__(self, ax: Axes, x, psi, mode="density", scale=1.0, base=0.0, opacity=0.85, px_per_unit=None,
                 outline=True, outline_color=WHITE, outline_width=2.2, x_window=None):
        super().__init__()
        if px_per_unit is None:  # match the output resolution (60 px/unit at 480p, 135 at 1080p)
            px_per_unit = config.pixel_width / config.frame_width
        self.ax, self.x, self.mode, self.yscale, self.base = ax, np.asarray(x, float), mode, scale, base
        self.opacity = opacity
        x0, x1 = (self.x[0], self.x[-1]) if x_window is None else x_window
        self.x0, self.x1 = x0, x1
        y0, y1 = ax.y_range[0], ax.y_range[1]
        self.y0, self.y1 = y0, y1
        p0, p1 = ax.c2p(x0, y0), ax.c2p(x1, y1)
        self.W = max(16, int(abs(p1[0] - p0[0]) * px_per_unit))
        self.H = max(16, int(abs(p1[1] - p0[1]) * px_per_unit))
        self.xs_px = np.linspace(x0, x1, self.W)
        self.img = ImageMobject(np.zeros((self.H, self.W, 4), np.uint8))
        self.img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        self.img.stretch_to_fit_width(abs(p1[0] - p0[0])).stretch_to_fit_height(abs(p1[1] - p0[1]))
        self.img.move_to((p0 + p1) / 2)
        self.outline_on = outline
        self.line = VMobject(stroke_color=outline_color, stroke_width=outline_width)
        self.add(self.img)
        if outline:
            self.add(self.line)
        self.alpha = 1.0
        self.set_psi(psi)

    def heights(self, psi):
        if self.mode == "density":
            return self.base + self.yscale * np.abs(psi) ** 2
        if self.mode == "abs":
            return self.base + self.yscale * np.abs(psi)
        return self.base + self.yscale * np.real(psi)

    def set_psi(self, psi):
        psi = np.asarray(psi)
        self.psi = psi
        h = self.heights(psi)
        hp = np.interp(self.xs_px, self.x, h)
        re = np.interp(self.xs_px, self.x, np.real(psi))
        im = np.interp(self.xs_px, self.x, np.imag(psi))
        ph = np.arctan2(im, re)
        to_px = (self.H - 1) / (self.y1 - self.y0)
        vals = np.clip((hp - self.y0) * to_px, -2, self.H + 2)
        base_px = (self.base - self.y0) * to_px
        rgba = _fill_rgba(vals, ph, self.H, self.opacity * self.alpha, base_px)
        self.img.pixel_array = rgba
        if self.outline_on:
            keep = (self.x >= self.x0) & (self.x <= self.x1)
            xs, hs = self.x[keep], np.clip(h[keep], self.y0, self.y1)
            if len(xs) > 1500:
                idx = np.linspace(0, len(xs) - 1, 1500).astype(int)
                xs, hs = xs[idx], hs[idx]
            self.line.set_points_as_corners(self.ax.c2p(xs, hs).T)
            self.line.set_stroke(opacity=self.alpha)
        return self

    def follow(self, tracker: ValueTracker, psi_at):
        """Redraw from ``psi_at(t)`` whenever ``tracker`` changes."""
        self._t = None

        def upd(m):
            t = tracker.get_value()
            if t != m._t:
                m._t = t
                m.set_psi(psi_at(t))

        self.add_updater(upd)
        return self

    def fade_to(self, to=1.0, **kw) -> Animation:
        start = self.alpha

        def upd(m, a):
            m.alpha = start + (to - start) * a
            m.set_psi(m.psi)

        return UpdateFromAlphaFunc(self, upd, suspend_mobject_updating=False, **kw)


def frames_at(ts, frames):
    """psi(t) from stored frames at times ``ts``: the nearest stored frame (frames are dense enough that this is
    smooth), so phases are never blended (blending two phases would dim the amplitude)."""
    ts = np.asarray(ts)

    def f(t):
        k = int(np.clip(np.round(np.interp(t, ts, np.arange(len(ts)))), 0, len(ts) - 1))
        return frames[k]

    return f


def potential_fill(ax: Axes, xs, V, color=C.POTENTIAL, opacity=0.22, stroke_width=2.5, y_min=None) -> VGroup:
    """V(x) as an outlined, lightly filled region down to the bottom of the axes."""
    xs, V = np.asarray(xs, float), np.asarray(V, float)
    y0 = ax.y_range[0] if y_min is None else y_min
    Vc = np.clip(V, y0, ax.y_range[1])
    pts = [ax.c2p(xs[0], y0)] + list(ax.c2p(xs, Vc).T) + [ax.c2p(xs[-1], y0)]
    area = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)
    edge = VMobject(stroke_color=color, stroke_width=stroke_width)
    edge.set_points_as_corners(ax.c2p(xs, Vc).T)
    return VGroup(area, edge)


def level_line(ax: Axes, E, x0, x1, color=C.ENERGY, stroke_width=2, dashed=False) -> Line:
    cls = DashedLine if dashed else Line
    return cls(ax.c2p(x0, E), ax.c2p(x1, E), color=color, stroke_width=stroke_width)


def phasor(z: complex, origin=ORIGIN, unit=1.0, stroke_width=4, tip=0.16, color=None) -> Arrow:
    """An arrow for a complex number: length |z| * unit, direction arg z, colored by its phase."""
    end = np.array(origin) + unit * np.array([z.real, z.imag, 0.0])
    c = hue(np.angle(z)) if color is None else color
    return Arrow(origin, end, buff=0, color=c, stroke_width=stroke_width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12)


def complex_plane(radius=1.5, font_size=24, label_axes=True) -> VGroup:
    """Small complex-plane axes (Re, Im) with a unit circle."""
    ax = VGroup(Line(LEFT * radius, RIGHT * radius, color=GREY_C, stroke_width=1.5),
                Line(DOWN * radius, UP * radius, color=GREY_C, stroke_width=1.5))
    g = VGroup(ax)
    if label_axes:
        g.add(MathTex(r"\mathrm{Re}", font_size=font_size, color=GREY_B).next_to(ax[0], RIGHT, buff=0.08),
              MathTex(r"\mathrm{Im}", font_size=font_size, color=GREY_B).next_to(ax[1], UP, buff=0.08))
    return g


# ---------------------------------------------------------------------------
# A tiny 3D camera (orthographic, with depth cues) for helices and spheres
# ---------------------------------------------------------------------------
class Projector:
    """Maps 3D points to the screen.  World axes: X to the right, Y up, Z toward the viewer.  ``az`` turns the
    world about the vertical (Y) axis, ``el`` then tilts it about the horizontal (X) axis.  Trackers make both
    animatable; :meth:`depth` (positive = nearer the viewer) drives opacity cues."""

    def __init__(self, az=0.0, el=0.0, scale=1.0, center=ORIGIN):
        self.az = ValueTracker(az)
        self.el = ValueTracker(el)
        self.scale = scale
        self.center = np.array(center, dtype=float)

    def _rot(self):
        a, e = self.az.get_value(), self.el.get_value()
        ca, sa, ce, se = math.cos(a), math.sin(a), math.cos(e), math.sin(e)
        Ry = np.array([[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]])
        Rx = np.array([[1, 0, 0], [0, ce, -se], [0, se, ce]])
        return Rx @ Ry

    def rotated(self, P):
        P = np.atleast_2d(np.asarray(P, float))
        return P @ self._rot().T

    def __call__(self, P):
        Q = self.rotated(P)
        out = np.zeros_like(Q)
        out[:, 0], out[:, 1] = Q[:, 0] * self.scale, Q[:, 1] * self.scale
        return out + self.center

    def depth(self, P):
        return self.rotated(P)[:, 2]

    def point(self, p):
        return self(np.array([p]))[0]


def segments_3d(proj: Projector, P, colors, stroke_width=3.0, depth_range=1.0, min_opacity=0.25, opacity=1.0) -> VGroup:
    """A 3D polyline drawn as short segments, each with its own color; farther segments are fainter and thinner."""
    S = proj(P)
    d = proj.depth(P)
    g = VGroup()
    for i in range(len(P) - 1):
        dm = 0.5 * (d[i] + d[i + 1])
        f = np.clip(0.5 + 0.5 * dm / max(depth_range, 1e-9), 0, 1)
        op = opacity * (min_opacity + (1 - min_opacity) * f)
        seg = Line(S[i], S[i + 1], stroke_width=stroke_width * (0.65 + 0.35 * f), color=colors[i])
        seg.set_stroke(opacity=op)
        seg.depth = dm
        g.add(seg)
    return g


def depth_sorted(*groups) -> VGroup:
    """Merge segment groups from :func:`segments_3d` into one, ordered back to front, so nearer pieces cover
    farther ones (e.g. an axis passing behind half of a helix and in front of the other half)."""
    segs = [m for g in groups for m in g.submobjects]
    segs.sort(key=lambda m: getattr(m, "depth", 0.0))
    return VGroup(*segs)


def line_3d(proj: Projector, a, b, color=GREY_B, n=24, **kw) -> VGroup:
    """A straight 3D segment split into ``n`` pieces (so it can be depth-sorted against other geometry)."""
    P = np.linspace(np.asarray(a, float), np.asarray(b, float), n + 1)
    return segments_3d(proj, P, [color] * n, **kw)


def helix_points(x, psi, x_unit=1.0, amp_unit=1.0, x_center=0.0):
    """World points (X = x, Y = Re psi, Z = Im psi) for the complex-helix picture of psi(x)."""
    x = np.asarray(x, float)
    return np.stack([(x - x_center) * x_unit, np.real(psi) * amp_unit, np.imag(psi) * amp_unit], axis=1)


class BlochSphere(VGroup):
    """A Bloch sphere drawn through a :class:`Projector`: outline, equator, a meridian, axes and pole labels.
    World mapping: Bloch z -> screen up (Y), Bloch x -> toward the viewer (Z), Bloch y -> right (X)."""

    def __init__(self, proj: Projector, radius=2.0, labels=True, font_size=30):
        super().__init__()
        self.proj, self.r = proj, radius
        self.labels_on, self.fs = labels, font_size
        self._build()

    @staticmethod
    def world(v):
        """Bloch vector (x, y, z) -> world (X, Y, Z)."""
        v = np.atleast_2d(v)
        return np.stack([v[:, 1], v[:, 2], v[:, 0]], axis=1)

    def bloch_to_screen(self, v):
        return self.proj(self.world(np.asarray(v, float) * self.r))

    def _build(self):
        self.submobjects = []
        r, proj = self.r, self.proj
        t = np.linspace(0, 2 * PI, 121)
        outline = Circle(radius=r * proj.scale, color=GREY_B, stroke_width=2).move_to(proj.center)
        circ = lambda pts: segments_3d(proj, pts, [GREY_C] * (len(pts) - 1), stroke_width=1.6, depth_range=r,  # noqa: E731
                                       min_opacity=0.15)
        eq = circ(self.world(np.stack([np.cos(t), np.sin(t), 0 * t], 1) * r))
        mer = circ(self.world(np.stack([np.sin(t), 0 * t, np.cos(t)], 1) * r))
        axes = VGroup()
        for v, lab, col in (([0, 0, 1], r"\ket{\uparrow}", C.SPIN_UP), ([0, 0, -1], r"\ket{\downarrow}", C.SPIN_DOWN),
                            ([1, 0, 0], r"\ket{+x}", GREY_A), ([0, 1, 0], r"\ket{+y}", GREY_A)):
            p0, p1 = self.bloch_to_screen([0, 0, 0])[0], self.bloch_to_screen(v)[0]
            axes.add(DashedLine(p0, p1, color=GREY_C, stroke_width=1.5, dash_length=0.08))
            if self.labels_on:
                d = p1 - p0
                n = d / max(np.linalg.norm(d), 1e-6)
                axes.add(MathTex(lab, font_size=self.fs, color=col).move_to(p1 + n * 0.42))
        self.add(outline, eq, mer, axes)

    def redraw(self):
        self._build()
        return self

    def arrow(self, v, color=C.BLOCH, stroke_width=6) -> Arrow:
        p0, p1 = self.bloch_to_screen([0, 0, 0])[0], self.bloch_to_screen(v)[0]
        return Arrow(p0, p1, buff=0, color=color, stroke_width=stroke_width, tip_length=0.22,
                     max_tip_length_to_length_ratio=0.3)


def bloch_vector(theta, phi):
    return np.array([math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)])


# ---------------------------------------------------------------------------
# The double-slit movie
# ---------------------------------------------------------------------------
class FieldMovie2D(ImageMobject):
    """Plays the double-slit simulation: frame k of ``slit_frames()`` (t = 4 k), phase-colored, brightness from |psi|.
    Driven by ``tracker`` (simulation time).  Right of the slit plate the brightness is boosted by ``boost`` so the
    transmitted wave (a tenth of the probability) is visible; scenes say so on screen."""

    def __init__(self, tracker: ValueTracker, width: float, boost: float = 3.0, vmax: float | None = None,
                 gamma=0.6, alpha=1.0, stride=1, mode="phase"):
        from .compute import FRAME_SCALE, SLIT
        self.frames = slit_frames()
        self.tracker, self.boost, self.gamma, self.alpha, self.stride, self.mode = tracker, boost, gamma, alpha, stride, mode
        p = SLIT
        self.x0, self.x1 = p["crop_x"]
        self.y0, self.y1 = p["crop_y"]
        self.wall_col = int(p["wall"][1] - self.x0)
        f0 = self._psi(0)
        self.vmax = float(np.abs(f0).max()) if vmax is None else vmax
        self._k = -1
        super().__init__(self._rgba(0))
        self.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        self.stretch_to_fit_width(width)
        self.stretch_to_fit_height(width * (self.y1 - self.y0) / (self.x1 - self.x0))
        self.add_updater(FieldMovie2D._tick)
        self.frame_scale = FRAME_SCALE

    def _psi(self, k):
        from .compute import FRAME_SCALE
        f = np.asarray(self.frames[k, :: self.stride, :: self.stride], dtype=np.float32)
        return (f[..., 0] + 1j * f[..., 1])[::-1] / FRAME_SCALE  # row 0 = top = largest y

    def _rgba(self, k):
        psi = self._psi(k)
        gain = np.ones(psi.shape[1], np.float32)
        gain[self.wall_col // self.stride:] = self.boost
        psi = psi * gain[None, :]
        if self.mode == "density":
            rho = np.abs(psi) ** 2 / self.vmax**2
            t = np.clip(rho, 0, 1) ** (self.gamma * 0.5)
            c = np.array(ManimColor(C.BORN).to_rgb(), np.float32)
            rgb = qcm.BG + t[..., None] * (c - qcm.BG)
        else:
            rgb = qcm.phase_rgb(psi, vmax=self.vmax, gamma=self.gamma, hot=0.0)
        return qcm.rgba(rgb, self.alpha)

    def frame_index(self):
        return int(np.clip(round(self.tracker.get_value() / 4.0), 0, len(self.frames) - 1))

    @staticmethod
    def _tick(m):
        k = m.frame_index()
        if k != m._k:
            m._k = k
            m.pixel_array = m._rgba(k)

    def refresh(self):
        self._k = -1
        FieldMovie2D._tick(self)
        return self

    def fade_to(self, to=1.0, **kw) -> Animation:
        start = self.alpha

        def upd(m, a):
            m.alpha = start + (to - start) * a
            m.refresh()

        return UpdateFromAlphaFunc(self, upd, suspend_mobject_updating=False, **kw)

    def sim_to_screen(self, x, y):
        """Scene point of simulation coordinates (x, y)."""
        c = self.get_center()
        w, h = self.width, self.height
        u = (x - self.x0) / (self.x1 - self.x0) - 0.5
        v = (y - self.y0) / (self.y1 - self.y0) - 0.5
        return c + np.array([u * w, v * h, 0])


def orbital_image(key: str, height=2.2, gain=2.5) -> ImageMobject:
    """A precomputed hydrogen render (compute.py, item "hydrogen"), tone-mapped to its own brightness."""
    from .compute import tone
    h = load("hydrogen")
    col, acc = h[f"{key}_col"], h[f"{key}_acc"]
    img = ImageMobject(tone(col, acc, gain / np.percentile(acc, 99.5)))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    img.height = height
    return img


# ---------------------------------------------------------------------------
# Small composite pieces
# ---------------------------------------------------------------------------
def energy_ladder(ax: Axes, energies, x0, x1, color=C.ENERGY, labels=None, font_size=26) -> VGroup:
    g = VGroup()
    for i, E in enumerate(energies):
        ln = Line(ax.c2p(x0, E), ax.c2p(x1, E), color=color, stroke_width=2.5)
        g.add(ln)
        if labels is not None:
            g.add(MathTex(labels[i], font_size=font_size, color=color).next_to(ln, RIGHT, buff=0.15))
    return g


def bar_chart(ax: Axes, xs, hs, width=0.7, color=C.BORN, opacity=0.75, stroke_width=0) -> VGroup:
    g = VGroup()
    for x, h in zip(xs, hs):
        p0, p1 = ax.c2p(x - width / 2, 0), ax.c2p(x + width / 2, h)
        r = Rectangle(width=abs(p1[0] - p0[0]), height=max(abs(p1[1] - p0[1]), 1e-3), stroke_width=stroke_width,
                      fill_color=color, fill_opacity=opacity, stroke_color=color)
        r.move_to((p0 + p1) / 2)
        g.add(r)
    return g


def spectrum_color(lam_nm: float) -> ManimColor:
    """Approximate sRGB of a visible wavelength (for drawing spectral lines)."""
    lam = lam_nm
    if 380 <= lam < 440:
        r, g, b = -(lam - 440) / 60, 0.0, 1.0
    elif lam < 490:
        r, g, b = 0.0, (lam - 440) / 50, 1.0
    elif lam < 510:
        r, g, b = 0.0, 1.0, -(lam - 510) / 20
    elif lam < 580:
        r, g, b = (lam - 510) / 70, 1.0, 0.0
    elif lam < 645:
        r, g, b = 1.0, -(lam - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    f = 0.3 + 0.7 * (lam - 380) / 40 if lam < 420 else (0.3 + 0.7 * (780 - lam) / 80 if lam > 700 else 1.0)
    return ManimColor.from_rgb(tuple(float(min(1.0, (c * f) ** 0.8)) for c in (r, g, b)))  # floats: 0..1 scale
