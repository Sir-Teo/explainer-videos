"""Helpers for part 2 of the general-relativity video.  Everything from part 1's helpers (text, ladders, rasters,
the orthographic 3D projector, spacetime diagrams, clocks, the Schwarzschild black-hole shader) is re-exported, plus:
part cards, singularity zigzags, coordinate diagrams with clipping, surfaces of revolution, and a Kerr disk shader."""

from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import (  # noqa: F401
    BHShader, Clock, Globe, Raster, Redraw, View3D, arrow3d, boxed, color_parts, corner_note, curve3d, disk_texture,
    label, ladder, latitude, light_cone, meridian, mtex, note, num, page_thorne, polyline, redraw, rgba, sci,
    screen_polyline, sphere_points, st_axes, stack, stars_rgba, tagged, why)
from videos.relativity.compute import load as load1  # noqa: F401  (part 1's cache: bh80, bh20, gw, light, ...)

from . import spacetime as st
from .compute import load  # noqa: F401

FRAME_X, FRAME_Y = 7.1, 3.95  # half-extents of the visible frame, with a hair of margin


def clamp_x(m, edge=6.85):
    """Shift a mobject horizontally so it stays inside the frame."""
    lo, hi = m.get_left()[0], m.get_right()[0]
    if hi > edge:
        m.shift((edge - hi) * RIGHT)
    if lo < -edge:
        m.shift((-edge - lo) * RIGHT)
    return m


def under(rows, whys, x0, align_index=1, edge=6.85):
    """Line up the rows of a derivation on their '=' at x = x0, and put each note just below its row, centered on
    the row and kept inside the frame (part 1's ladder keeps these horizontal positions)."""
    for r, w in zip(rows, whys):
        r.shift((x0 - r[align_index].get_center()[0]) * RIGHT)
        if w is None:
            continue
        w.next_to(r, DOWN, buff=0.08)
        if w.width < r.width:
            w.align_to(r, RIGHT)
        lo, hi = w.get_left()[0], w.get_right()[0]
        if hi > edge:
            w.shift((edge - hi) * RIGHT)
        if lo < -edge:
            w.shift((-edge - lo) * RIGHT)


def part_card(numeral: str, title: str, subtitle: str = "") -> VGroup:
    num_ = label(rf"Part 2 \textperiodcentered\ {numeral}", font_size=34, color=C.DIM)
    t = label(title, font_size=60)
    g = VGroup(num_, t)
    if subtitle:
        g.add(label(subtitle, font_size=32, color=GREY_A))
    return g.arrange(DOWN, buff=0.3)


def zigzag(start, end, n=None, amp=0.06, color=None, stroke_width=3) -> VMobject:
    """A singularity: a zigzag line from start to end (screen points)."""
    start, end = np.asarray(start, float), np.asarray(end, float)
    d = end - start
    L = np.linalg.norm(d)
    n = n or max(4, int(L / 0.12))
    u = d / L
    perp = np.array([-u[1], u[0], 0])
    pts = [start + d * k / n + perp * amp * (1 if k % 2 else -1) * (0 < k < n) for k in range(n + 1)]
    m = VMobject(stroke_color=color or C.SINGULARITY, stroke_width=stroke_width)
    m.set_points_as_corners(pts)
    return m


def zigzag_curve(pts, amp=0.05, every=0.12, color=None, stroke_width=3) -> VMobject:
    """A zigzag that follows a curve given as screen points."""
    pts = np.asarray(pts, float)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    n = max(4, int(s[-1] / every))
    ss = np.linspace(0, s[-1], n + 1)
    P = np.stack([np.interp(ss, s, pts[:, i]) for i in range(3)], 1)
    T = np.gradient(P, axis=0)
    T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-12
    N = np.stack([-T[:, 1], T[:, 0], 0 * T[:, 0]], 1)
    sgn = np.array([(1 if k % 2 else -1) * (0 < k < n) for k in range(n + 1)])[:, None]
    m = VMobject(stroke_color=color or C.SINGULARITY, stroke_width=stroke_width)
    m.set_points_as_corners(P + N * amp * sgn)
    return m


class Chart:
    """A coordinate diagram: world (x, y) -> screen center + scale * (x - x0, y - y0), with curves clipped to a
    screen box (so infinite coordinate lines can be drawn and morphed)."""

    def __init__(self, center=ORIGIN, scale=1.0, origin=(0.0, 0.0), box=(-FRAME_X, FRAME_X, -FRAME_Y, FRAME_Y)):
        self.center = np.array(center, float)
        self.scale = scale
        self.origin = np.array(origin, float)
        self.box = box

    def p(self, x, y) -> np.ndarray:
        x, y = np.asarray(x, float), np.asarray(y, float)
        return np.stack([self.center[0] + self.scale * (x - self.origin[0]),
                         self.center[1] + self.scale * (y - self.origin[1]), np.zeros(np.broadcast(x, y).shape)], -1)

    def curve(self, x, y, color=WHITE, stroke_width=2.5, opacity=1.0, clip=True) -> VGroup:
        return clipped(self.p(x, y), color=color, stroke_width=stroke_width, opacity=opacity,
                       box=self.box if clip else None)


def clipped(P, color=WHITE, stroke_width=2.5, opacity=1.0, box=(-FRAME_X, FRAME_X, -FRAME_Y, FRAME_Y)) -> VGroup:
    """A polyline split into the runs of points that are finite and inside ``box``."""
    P = np.asarray(P, float)
    ok = np.all(np.isfinite(P), axis=1)
    if box is not None:
        x0, x1, y0, y1 = box
        ok &= (P[:, 0] >= x0) & (P[:, 0] <= x1) & (P[:, 1] >= y0) & (P[:, 1] <= y1)
    g = VGroup()
    i, n = 0, len(P)
    while i < n:
        if not ok[i]:
            i += 1
            continue
        j = i
        while j < n and ok[j]:
            j += 1
        if j - i >= 2:
            m = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity)
            m.set_points_as_corners(P[i:j])
            g.add(m)
        i = j
    return g


def revolution(view: View3D, rho, z, n_rings=9, n_spokes=24, color=C.METRIC, stroke_width=1.6, highlight=None,
               ring_idx=None, back_opacity=0.25, z_scale=1.0) -> VGroup:
    """Wireframe of a surface of revolution about the vertical axis: radius rho(s), height z(s) (arrays)."""
    rho, z = np.asarray(rho, float), np.asarray(z, float) * z_scale
    g = VGroup()
    idx = ring_idx if ring_idx is not None else np.linspace(0, len(rho) - 1, n_rings).round().astype(int)
    a = np.linspace(0, 2 * np.pi, 120)
    for k in idx:
        P = np.stack([rho[k] * np.cos(a), rho[k] * np.sin(a), np.full_like(a, z[k])], 1)
        g.add(curve3d(view, P, color=color, stroke_width=stroke_width, sphere_r=None, back_opacity=1.0))
    for ang in np.linspace(0, 2 * np.pi, n_spokes, endpoint=False):
        P = np.stack([rho * math.cos(ang), rho * math.sin(ang), z], 1)
        g.add(curve3d(view, P, color=color, stroke_width=stroke_width * 0.8, sphere_r=None, back_opacity=1.0))
    return g


def spheroid(view: View3D, R_eq, R_pol, color, n_lat=7, n_lon=14, stroke_width=1.6, opacity=1.0,
             back_opacity=0.18) -> VGroup:
    """Wireframe of an axisymmetric surface given by its equatorial radius R_eq(theta) and height R_pol(theta)
    (callables of the polar angle), drawn with its far side faint."""
    g = VGroup()
    th = np.linspace(0, np.pi, 90)
    rho, z = R_eq(th), R_pol(th)
    for ph in np.linspace(0, 2 * np.pi, n_lon, endpoint=False):
        P = np.stack([rho * math.cos(ph), rho * math.sin(ph), z], 1)
        g.add(_depth_curve(view, P, color, stroke_width, opacity, back_opacity))
    for t0 in np.linspace(0, np.pi, n_lat + 2)[1:-1]:
        a = np.linspace(0, 2 * np.pi, 120)
        P = np.stack([R_eq(t0) * np.cos(a), R_eq(t0) * np.sin(a), np.full_like(a, R_pol(t0))], 1)
        g.add(_depth_curve(view, P, color, stroke_width, opacity, back_opacity))
    return g


def _depth_curve(view, P, color, stroke_width, opacity, back_opacity):
    """Front half (depth >= 0) solid, back half faint."""
    S, depth = view.project(P)
    g = VGroup()
    front = depth >= 0
    start = 0
    for i in range(1, len(S) + 1):
        if i == len(S) or front[i] != front[start]:
            seg = S[max(0, start - 1): i] if start > 0 else S[start:i]
            if len(seg) >= 2:
                m = VMobject(stroke_color=color, stroke_width=stroke_width if front[start] else stroke_width * 0.7,
                             stroke_opacity=opacity if front[start] else back_opacity)
                m.set_points_as_corners(seg)
                g.add(m)
            start = i
    return g


# ---------------------------------------------------------------------------
# The Kerr black hole image (compute.trace_kerr data): disk + lensed stars
# ---------------------------------------------------------------------------
_PT_SCHW_MAX = float(st.page_thorne_kerr(np.linspace(6.0001, 26, 6000), 1e-9).max())


def disk_texture_M(r, phi, t, a=0.0, seed=3):
    """Part 1's streaky gas texture, in units of M, wound up by the Kerr Keplerian shear Omega = 1/(r^1.5 + a)."""
    rr = np.random.default_rng(seed)
    om = 1 / (np.maximum(r, 1.0) ** 1.5 + a)
    ph = phi - om * t
    lr = np.log(np.maximum(r / 2, 1e-3))
    v = np.zeros_like(r)
    for k in range(7):
        m = int(rr.integers(2, 9))
        amp = rr.uniform(6, 22)
        v += np.sin(m * ph + amp * lr + rr.uniform(0, 2 * np.pi)) / (k + 1.5)
    return 1 + 0.32 * v


class KerrShader:
    """RGBA image of a precomputed Kerr ray trace at disk time t (in M), shaded like part 1's: Page-Thorne flux for
    this spin times g^4 (Doppler and gravitational shift).  A spinning hole's inner disk is about a hundred times
    brighter than a non-spinning one's peak, so the brightness is compressed with a gamma, (F g^4)^gamma, and the
    color temperature uses the flux relative to this disk's own peak.  Colors are illustrative, as in part 1."""

    def __init__(self, d, exposure=0.55, stars=True, gamma=0.5, tscale=1.0):
        a = float(d["a"])
        H, W = d["captured"].shape
        base = np.zeros((H, W, 3), np.float32)
        ok = np.isfinite(d["hit_r"])
        if stars:
            s = stars_rgba(d["dir"])
            s[d["captured"]] = 0
            s[ok] = 0
            base += s[..., None] * np.array([0.85, 0.9, 1.0], np.float32)
        rr, pp, g = d["hit_r"][ok], d["hit_phi"][ok], d["g"][ok]
        F = st.page_thorne_kerr(rr, max(a, 1e-9))
        F_own = F / float(st.page_thorne_kerr(np.linspace(st.isco(a) + 1e-4, 26, 6000), max(a, 1e-9)).max())
        fade = np.clip((26.0 - rr) / 6.0, 0, 1)
        self.amp = exposure * (F / _PT_SCHW_MAX * g**4) ** gamma * fade
        temp = np.clip(tscale * g * F_own ** 0.25, 0, 2)
        self.col = np.stack([np.clip(0.55 + 0.6 * temp, 0, 1), np.clip(0.18 + 0.75 * temp ** 1.5, 0, 1),
                             np.clip(0.02 + 0.6 * temp ** 3, 0, 1)], -1).astype(np.float32)
        self.idx, self.rr, self.pp, self.a = np.nonzero(ok), rr, pp, a
        base[d["captured"]] = 0
        self.base = base

    def __call__(self, t=0.0):
        img = self.base.copy()
        v = 1 - np.exp(-2.2 * self.amp * disk_texture_M(self.rr, self.pp, t, self.a))
        img[self.idx] = self.col * v[:, None]
        return rgba(np.clip(img, 0, 1))


def bh_screen_scale(width_units: float, W=1280, fov_deg=36.0, r0=100.0) -> float:
    """Screen units per M of the image-plane coordinates (alpha, beta) for a ray-traced image shown ``width_units``
    wide.  A ray through screen offset X (in tan units) has alpha = r0 X / sqrt(1 - 2/r0) (the camera's lapse), to
    first order in X."""
    return width_units / (2 * math.tan(math.radians(fov_deg) / 2) * r0) * math.sqrt(1 - 2 / r0)


def shadow_outline(a, incl_deg, center, scale, color=WHITE, stroke_width=2.5, n=600) -> VMobject:
    """Bardeen's analytic shadow edge drawn over an image (alpha to the right, beta up), ``scale`` screen units per M."""
    al, be = st.shadow_curve(a, math.radians(incl_deg), n)
    P = np.stack([center[0] + scale * al, center[1] + scale * be, np.zeros_like(al)], 1)
    m = VMobject(stroke_color=color, stroke_width=stroke_width)
    m.set_points_as_corners([*P, P[0]])
    return m
