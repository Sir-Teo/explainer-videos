"""Helpers shared by the general-relativity scenes: text, rasters, a small orthographic 3D projector (spheres,
surfaces and point clouds drawn as ordinary 2D mobjects, so they mix freely with equations), spacetime diagrams
and clocks."""

from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as cm

from .compute import load  # noqa: F401

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


def corner_note(text: str, corner=DR) -> Tex:
    return note(text).to_corner(corner, buff=0.3)


def sci(x: float, digits=2) -> str:
    """3.57e-16 -> '3.57 \\times 10^{-16}' for MathTex."""
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10**e
    return rf"{m:.{digits}f} \times 10^{{{e}}}"


def num(x: float, digits=3, sign=False) -> str:
    s = f"{x:+.{digits}f}" if sign else f"{x:.{digits}f}"
    return s.replace("-", "{-}")


def color_parts(m: MathTex, colors: dict[int, str]) -> MathTex:
    for i, col in colors.items():
        m[i].set_color(col)
    return m


def why(text: str, target: Mobject, direction=RIGHT, color=GREY_A, font_size=26, buff=0.35) -> Tex:
    """A short grey justification placed next to a derivation step."""
    return label(text, color=color, font_size=font_size).next_to(target, direction, buff=buff)


def stack(*rows: MathTex, buff=0.42, align_index=1) -> VGroup:
    """Rows of a derivation, arranged downward with their ``align_index`` parts (usually '=') lined up."""
    g = VGroup(*rows).arrange(DOWN, buff=buff)
    x = rows[0][align_index].get_center()[0]
    for r in rows[1:]:
        r.shift((x - r[align_index].get_center()[0]) * RIGHT)
    return g


def ladder(scene, rows, whys, keep=4, top=2.9, buff=0.48, x=0.0, align_index=1):
    """Reveal derivation rows one at a time, keeping at most ``keep`` on screen (older rows scroll off the top).
    Returns a function step(i) that animates row i."""
    edge = 6.95
    for r, w in zip(rows, whys):
        r.shift((x - r[align_index].get_center()[0]) * RIGHT)
        # a row too wide for the frame once its '=' is aligned shrinks about that '=' (its note follows it)
        lo, hi = r.get_left()[0], r.get_right()[0]
        f = min(1.0, (edge - x) / (hi - x) if hi > edge else 1.0, (x + edge) / (x - lo) if lo < -edge else 1.0)
        if f < 1.0:
            below = w is not None and w.get_top()[1] < r.get_bottom()[1] - 0.01
            r.scale(f, about_point=np.array([x, r.get_y(), 0]))
            if w is not None:
                if below:
                    w.next_to(r, DOWN, buff=0.08).align_to(r, RIGHT)
                else:
                    w.next_to(r, RIGHT, buff=0.35)
                    w.set_x(min(w.get_x(), edge - 0.05 - w.width / 2))
    # each note keeps its vertical offset from its row (beside it: 0; below it: negative)
    offs = [0.0 if w is None else w.get_y() - r.get_y() for r, w in zip(rows, whys)]

    def step(i):
        anims = []
        shown = rows[max(0, i - keep + 1): i]
        if i >= keep:
            old = rows[i - keep]
            anims += [FadeOut(old, shift=UP * 0.3)]
            if whys[i - keep] is not None:
                anims += [FadeOut(whys[i - keep], shift=UP * 0.3)]
        # place: shown rows from top, then the new row
        y = top
        targets = []
        for r in list(shown) + [rows[i]]:
            targets.append(y - r.height / 2)
            y -= r.height + buff
        for r, ty in zip(shown, targets[:-1]):
            anims.append(r.animate.set_y(ty))
            j = rows.index(r)
            if whys[j] is not None:
                anims.append(whys[j].animate.set_y(ty + offs[j]))
        rows[i].set_y(targets[-1])
        if whys[i] is not None:
            whys[i].set_y(targets[-1] + offs[i])
        if anims:
            scene.play(*anims, run_time=0.7)
        if i == 0:
            scene.play(Write(rows[i]))
        else:
            scene.play(TransformMatchingTex(rows[i - 1].copy(), rows[i]), run_time=1.3)
        if whys[i] is not None:
            scene.play(FadeIn(whys[i]), run_time=0.5)

    return step


# ---------------------------------------------------------------------------
# Redrawing
# ---------------------------------------------------------------------------
class Redraw(VGroup):
    """Like ``always_redraw``, but each frame *swaps in* the freshly built mobject instead of calling ``become``.
    ``become`` pairs old and new submobjects in family order, so when the family's size or nesting changes from
    frame to frame (curves split by visibility, markers appearing) mismatched pieces trade points and draw spikes."""

    def __init__(self, func):
        super().__init__()
        self.func = func
        self.submobjects = [func()]
        self.add_updater(Redraw._rebuild)

    @staticmethod
    def _rebuild(m):
        m.submobjects = [m.func()]


def redraw(func) -> Redraw:
    return Redraw(func)


# ---------------------------------------------------------------------------
# Curves and rasters
# ---------------------------------------------------------------------------
def polyline(ax: Axes, xs, ys, color=WHITE, stroke_width=3, **kw) -> VMobject:
    pts = ax.c2p(np.asarray(xs, float), np.asarray(ys, float)).T
    m = VMobject(color=color, stroke_width=stroke_width, **kw)
    m.set_points_as_corners(pts)
    return m


def screen_polyline(pts, color=WHITE, stroke_width=3, **kw) -> VMobject:
    m = VMobject(color=color, stroke_width=stroke_width, **kw)
    pts = np.asarray(pts, float)
    if pts.shape[1] == 2:
        pts = np.concatenate([pts, np.zeros((len(pts), 1))], 1)
    m.set_points_as_corners(pts)
    return m


class Raster(ImageMobject):
    """An image redrawn by ``draw(value) -> RGBA uint8`` whenever ``tracker`` changes value."""

    def __init__(self, draw, tracker, width: float, height: float, center=ORIGIN, alpha=1.0, **kw):
        self.draw = draw
        self.trackers = list(tracker) if isinstance(tracker, (list, tuple)) else [tracker]
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

    def fade(self, to: float = 1.0, **kwargs) -> Animation:
        start = self.alpha

        def upd(m, a):
            m.alpha = start + (to - start) * a
            m.refresh()

        return UpdateFromAlphaFunc(self, upd, suspend_mobject_updating=False, **kwargs)


def rgba(rgb, alpha=None) -> np.ndarray:
    rgb = np.clip(np.asarray(rgb, np.float32), 0, 1)
    if alpha is None:
        alpha = np.ones(rgb.shape[:2], np.float32)
    return cm.to_uint8(np.concatenate([rgb, np.asarray(alpha, np.float32)[..., None]], axis=2))


# ---------------------------------------------------------------------------
# Orthographic 3D
# ---------------------------------------------------------------------------
def rot(azimuth: float, elevation: float) -> np.ndarray:
    """World -> view rotation.  The view looks along -z_view; azimuth spins the world about its z axis, elevation
    tilts the world's z axis toward the viewer (elevation = 0: z is up on screen)."""
    ca, sa = math.cos(azimuth), math.sin(azimuth)
    ce, se = math.cos(elevation), math.sin(elevation)
    Rz = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    # map world (x, y, z) to view (X right, Y up, Z toward viewer): x -> X, z -> Y, -y -> Z, then tilt about X
    base = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)
    Rx = np.array([[1, 0, 0], [0, ce, -se], [0, se, ce]])
    return Rx @ base @ Rz


class View3D:
    """Projects world points to the screen: ``center + scale * (X, Y)``; ``depth`` > 0 is toward the viewer."""

    def __init__(self, center=ORIGIN, scale=2.5, azimuth=0.0, elevation=0.35):
        self.center = np.array(center, float)
        self.scale = scale
        self.az = ValueTracker(azimuth)
        self.el = ValueTracker(elevation)

    def R(self):
        return rot(self.az.get_value(), self.el.get_value())

    def view(self, P):
        P = np.atleast_2d(np.asarray(P, float))
        return P @ self.R().T

    def project(self, P):
        V = self.view(P)
        S = self.center + self.scale * np.stack([V[:, 0], V[:, 1], np.zeros(len(V))], 1)
        return S, V[:, 2]

    def point(self, P) -> np.ndarray:
        return self.project(P)[0][0]


def _split_by_visibility(S, vis):
    """Runs of consecutive points with the same visibility: [(points, visible)]."""
    runs, start = [], 0
    for i in range(1, len(S) + 1):
        if i == len(S) or vis[i] != vis[start]:
            seg = S[max(0, start - 1): i] if start > 0 else S[start:i]
            runs.append((seg, bool(vis[start])))
            start = i
    return runs


def curve3d(view: View3D, P, color=WHITE, stroke_width=3, back_opacity=0.18, sphere_r: float | None = 1.0,
            front_opacity=1.0) -> VGroup:
    """A 3D polyline projected now; the part hidden behind a sphere of radius ``sphere_r`` (centered at the origin)
    is drawn faint.  ``sphere_r=None``: depth only matters through ``back_opacity`` of points with depth < 0."""
    S, depth = view.project(P)
    if sphere_r is None:
        vis = np.ones(len(S), bool)
    else:
        V = view.view(P)
        # hidden if behind the sphere's silhouette: depth < 0 and inside the disk
        vis = (V[:, 2] >= -1e-9) | (V[:, 0] ** 2 + V[:, 1] ** 2 > sphere_r**2 * (1 + 1e-6))
    g = VGroup()
    for seg, v in _split_by_visibility(S, vis):
        if len(seg) < 2:
            continue
        m = VMobject(stroke_color=color, stroke_width=stroke_width if v else stroke_width * 0.7,
                     stroke_opacity=front_opacity if v else back_opacity)
        m.set_points_as_corners(seg)
        g.add(m)
    return g


def arrow3d(view: View3D, base, vec, color=C.VECTOR, stroke_width=5, tip=0.18, sphere_r=1.0, back_opacity=0.25):
    S, _ = view.project(np.array([base, np.asarray(base) + np.asarray(vec)]))
    V = view.view(np.asarray(base)[None])[0]
    hidden = sphere_r is not None and V[2] < 0 and V[0] ** 2 + V[1] ** 2 < sphere_r**2
    length = np.linalg.norm(S[1] - S[0])
    a = Arrow(S[0], S[1] if length > 1e-3 else S[0] + 1e-3 * RIGHT, buff=0, color=color, stroke_width=stroke_width,
              tip_length=min(tip, 0.45 * max(length, 1e-3)), max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=40)
    if hidden:
        a.set_opacity(back_opacity)
    return a


def sphere_points(th, ph, r=1.0):
    th, ph = np.asarray(th, float), np.asarray(ph, float)
    return r * np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], -1)


def latitude(th0, n=180, ph0=0.0, ph1=2 * np.pi):
    ph = np.linspace(ph0, ph1, n)
    return sphere_points(np.full_like(ph, th0), ph)


def meridian(ph0, n=120, th0=0.0, th1=np.pi):
    th = np.linspace(th0, th1, n)
    return sphere_points(th, np.full_like(th, ph0))


def great_arc(a, b, n=120):
    a, b = np.asarray(a, float), np.asarray(b, float)
    om = math.acos(np.clip(a @ b, -1, 1))
    t = np.linspace(0, 1, n)[:, None]
    if om < 1e-9:
        return np.repeat(a[None], n, 0)
    return (np.sin((1 - t) * om) * a + np.sin(t * om) * b) / math.sin(om)


def sphere_shading(px=420, base="#24384F", light=(-0.45, 0.55, 0.7), rim="#5B7A99") -> np.ndarray:
    """A shaded disk (RGBA) that looks like a lit sphere; it is the same from every direction."""
    y, x = np.mgrid[1:-1:px * 1j, -1:1:px * 1j]
    r2 = x * x + y * y
    inside = r2 <= 1
    z = np.sqrt(np.clip(1 - r2, 0, 1))
    L = np.array(light, float)
    L /= np.linalg.norm(L)
    lam = np.clip(x * L[0] + y * L[1] + z * L[2], 0, 1)
    b = np.array(ManimColor(base).to_rgb())
    rc = np.array(ManimColor(rim).to_rgb())
    shade = 0.45 + 0.75 * lam
    spec = np.clip(lam, 0, 1) ** 30 * 0.25
    rimw = np.clip((r2 - 0.85) / 0.15, 0, 1)[..., None] * 0.35
    rgb = b * shade[..., None] + spec[..., None] + rimw * (rc - b)
    a = inside.astype(np.float32) * np.clip((1 - r2) * 60, 0, 1)
    return rgba(rgb, a)


class Globe(Group):
    """A sphere of radius ``radius`` (screen units) seen through a View3D.  The body is a static shaded image;
    grid lines and curves are 3D polylines re-projected whenever the view changes (use ``always_redraw``)."""

    def __init__(self, view: View3D, radius: float | None = None, grid=True, n_lat=5, n_lon=12, grid_color=GREY_C,
                 grid_opacity=0.35):
        super().__init__()
        self.view = view
        r = radius or view.scale
        self.body = ImageMobject(sphere_shading()).set_width(2 * r).move_to(view.center)
        self.outline = Circle(radius=r, color=GREY_B, stroke_width=1.5).move_to(view.center)
        self.add(self.body, self.outline)
        self.gridlines = None
        if grid:
            lats = [latitude(t) for t in np.linspace(0, np.pi, n_lat + 2)[1:-1]]
            lons = [meridian(p) for p in np.linspace(0, 2 * np.pi, n_lon, endpoint=False)]

            def make():
                g = VGroup()
                for P in lats + lons:
                    for m in curve3d(view, P, color=grid_color, stroke_width=1.2, back_opacity=0.0):
                        m.set_stroke(opacity=grid_opacity if m.get_stroke_opacity() > 0 else 0)
                        g.add(m)
                return g

            self.gridlines = redraw(make)
            self.add(self.gridlines)

    def curve(self, P, **kw) -> VGroup:
        return redraw(lambda: curve3d(self.view, P, **kw))


# ---------------------------------------------------------------------------
# Spacetime diagrams: x to the right, ct up; light rays at 45 degrees
# ---------------------------------------------------------------------------
def st_axes(x_range=(-3, 3), t_range=(0, 4), unit=1.0, x_label="x", t_label="ct", labels=True) -> VGroup:
    ax = Axes(x_range=[*x_range, 1], y_range=[*t_range, 1], x_length=(x_range[1] - x_range[0]) * unit,
              y_length=(t_range[1] - t_range[0]) * unit, tips=False,
              axis_config={"stroke_color": GREY_B, "stroke_width": 2, "include_ticks": False})
    g = VGroup(ax)
    if labels:
        g.add(MathTex(x_label, font_size=30).next_to(ax.x_axis.get_end(), RIGHT, buff=0.12))
        g.add(MathTex(t_label, font_size=30, color=C.PROPER_TIME).next_to(ax.y_axis.get_end(), UP, buff=0.12))
    g.ax = ax
    return g


def light_cone(ax: Axes, x0, t0, length=1.5, color=C.LIGHT, opacity=0.18, up=True) -> VGroup:
    s = 1 if up else -1
    tip = ax.c2p(x0, t0)
    a, b = ax.c2p(x0 - length, t0 + s * length), ax.c2p(x0 + length, t0 + s * length)
    fill = Polygon(tip, a, b, stroke_width=0, fill_color=color, fill_opacity=opacity)
    edges = VGroup(Line(tip, a, color=color, stroke_width=2), Line(tip, b, color=color, stroke_width=2))
    return VGroup(fill, edges)


# ---------------------------------------------------------------------------
# Clocks
# ---------------------------------------------------------------------------
class Clock(VGroup):
    """A small clock face whose hand angle follows ``tracker`` (one turn per ``period`` units of its value)."""

    def __init__(self, tracker: ValueTracker, radius=0.35, color=C.PROPER_TIME, period=1.0):
        super().__init__()
        self.tracker, self.period = tracker, period
        self.face = Circle(radius=radius, stroke_color=color, stroke_width=3, fill_color=BACKGROUND, fill_opacity=0.9)
        ticks = VGroup(*[Line(radius * 0.78 * np.array([math.sin(a), math.cos(a), 0]),
                              radius * 0.95 * np.array([math.sin(a), math.cos(a), 0]), color=color, stroke_width=2)
                         for a in np.linspace(0, 2 * np.pi, 12, endpoint=False)])
        self.add(self.face, ticks)
        self.r = radius

        def hand():
            a = 2 * np.pi * self.tracker.get_value() / self.period
            c0 = self.face.get_center()
            return Line(c0, c0 + 0.8 * self.r * np.array([math.sin(a), math.cos(a), 0]), color=WHITE, stroke_width=3)

        self.hand = redraw(hand)
        self.add(self.hand)


# ---------------------------------------------------------------------------
# The ray-traced black hole: shade the precomputed light paths (compute.trace_bh) into an image
# ---------------------------------------------------------------------------
def page_thorne(r):
    """Page-Thorne flux of a thin disk around a Schwarzschild hole, r in units of r_s (r* = r/M = 2r);
    zero at the ISCO (r = 3 r_s), peaked near r* = 9.55."""
    rs = 2 * np.asarray(r, float)
    s3, s6 = math.sqrt(3), math.sqrt(6)
    with np.errstate(invalid="ignore", divide="ignore"):
        L = np.log(((np.sqrt(rs) + s3) * (s6 - s3)) / ((np.sqrt(rs) - s3) * (s6 + s3)))
        F = (np.sqrt(rs) - s6 + (s3 / 2) * L) / ((rs - 3) * rs**2.5)
    return np.nan_to_num(np.where(rs > 6, F, 0.0))


_PT_MAX = float(page_thorne(np.linspace(3.01, 13, 4000)).max())


def disk_texture(r, phi, t, seed=3):
    """Streaky 'turbulent' gas texture in (ln r, phi - Omega t): Keplerian shear winds it up."""
    rr = np.random.default_rng(seed)
    om = np.sqrt(0.5 / np.maximum(r, 1.0) ** 3)
    ph = phi - om * t
    lr = np.log(np.maximum(r, 1e-3))
    v = np.zeros_like(r)
    for k in range(7):
        m = int(rr.integers(2, 9))
        a = rr.uniform(6, 22)
        v += np.sin(m * ph + a * lr + rr.uniform(0, 2 * np.pi)) / (k + 1.5)
    return 1 + 0.32 * v


def stars_rgba(dirs, density=0.0016, seed=11):
    """A sparse star field looked up by escape direction (unit vectors), so it is lensed by the hole."""
    n = 700  # cubic cells of ~1/700 rad: a star covers a couple of pixels
    q = np.floor(np.asarray(dirs, np.float64) * n).astype(np.int64)
    h = (q[..., 0] * 73856093) ^ (q[..., 1] * 19349663) ^ (q[..., 2] * 83492791) ^ seed
    h = np.abs(h)
    u = (h % 100003) / 100003.0
    return (u < density).astype(np.float32) * (0.45 + 0.55 * ((h // 7) % 97) / 97.0)


def shade_bh(d, t=0.0, exposure=1.0, stars=True):
    """RGBA image of the precomputed black hole ``d`` (a compute.load('bh80') dict) at disk time t."""
    return BHShader(d, exposure=exposure, stars=stars)(t)


class BHShader:
    """``shade_bh`` with everything but the moving texture precomputed: call it with the disk time t."""

    def __init__(self, d, exposure=1.0, stars=True):
        from .compute import R_IN, R_OUT

        H, W = d["captured"].shape
        self.H, self.W = H, W
        base = np.zeros((H, W, 3), np.float32)
        if stars:
            s = stars_rgba(d["dir"])
            s[d["captured"]] = 0
            base += s[..., None] * np.array([0.85, 0.9, 1.0], np.float32)
        filled = np.zeros((H, W), bool)
        self.layers = []
        for k in range(2):
            r = d["cross_r"][k]
            ok = np.isfinite(r) & (r > R_IN) & (r < R_OUT) & ~filled
            if not ok.any():
                continue
            rr, pp, g = r[ok], d["cross_phi"][k][ok], d["g"][k][ok]
            F = page_thorne(rr) / _PT_MAX
            fade = np.clip((R_OUT - rr) / 3.0, 0, 1)
            amp = exposure * F * g**4 * fade
            temp = np.clip(g * (F ** 0.25), 0, 2)
            col = np.stack([np.clip(0.55 + 0.6 * temp, 0, 1), np.clip(0.18 + 0.75 * temp ** 1.5, 0, 1),
                            np.clip(0.02 + 0.6 * temp ** 3, 0, 1)], -1).astype(np.float32)
            self.layers.append((np.nonzero(ok), rr, pp, amp, col))
            filled |= ok
        base[d["captured"]] = 0
        self.base = base

    def __call__(self, t=0.0):
        img = self.base.copy()
        for idx, rr, pp, amp, col in self.layers:
            v = 1 - np.exp(-2.2 * amp * disk_texture(rr, pp, t))
            img[idx] = col * v[:, None]
        return rgba(np.clip(img, 0, 1))
