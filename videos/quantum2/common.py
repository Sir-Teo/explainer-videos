"""Helpers shared by the scenes of "Quantum Mechanics, Part 2".

Part 2 keeps Part 1's visual language exactly (``videos/quantum/common.py`` is re-exported here): a complex
amplitude is drawn with its **phase as hue** (0 red, pi/2 yellow-green, pi cyan, 3 pi/2 violet; constant lightness
in OKLCH) and its **size as height or brightness**; a phase wheel sits in a corner whenever phase colors are on
screen; position is blue, momentum orange, energy green, time teal, potentials grey, probabilities warm yellow,
i hbar and commutators lilac, classical things sepia.  Part 2 adds a few colors (``explainer/style.py``): the
action S rose, gauge fields lime, angular momentum light orange, perturbations pink, approximations magenta,
bosons sky blue, fermions soft red, environments slate, coherences violet, and Dirac's positive / negative
energies amber / blue.

New here:

* :func:`ladder` reveals a derivation one line at a time, keeping a few lines on screen and scrolling the rest
  away, each line with a grey note saying *why* it follows (the same helper as the relativity video).
* :func:`phasor_chain` draws complex numbers tip to tail, each arrow colored by its own phase (sums over paths).
* :func:`phase_img`, :func:`signed_img` and :func:`gold_img` turn computed arrays into images.
"""

from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum import colormap as qcm
from videos.quantum.common import (BlochSphere, Projector, Raster, WaveView, bar_chart, bloch_vector, boxed,  # noqa: F401
                                   complex_plane, corner_wheel, depth_sorted, energy_ladder, frames_at, glow, hue,
                                   image_on, label, level_line, line_3d, mtex, note, num, num_table, part_card,
                                   phase_wheel, phasor, place_whys, polyline, potential_fill, segments_3d, splat,
                                   stack, tagged, wave_axes, why, ylabel)

from .compute import ab_movie, load  # noqa: F401


def sci(x: float, digits=2) -> str:
    """3.57e-16 -> '3.57 \\times 10^{-16}' for MathTex."""
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10**e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    return rf"{m:.{digits}f} \times 10^{{{e}}}"


def fmt_int(n: int) -> str:
    return f"{int(n):,}".replace(",", "{,}")


# ---------------------------------------------------------------------------
# Derivations
# ---------------------------------------------------------------------------
def ladder(scene, rows, whys, keep=4, top=2.9, buff=0.48, x=0.0, align_index=1, edge=6.95):
    """Reveal derivation rows one at a time, keeping at most ``keep`` on screen (older rows scroll off the top).
    Each row's ``align_index`` part (usually '=') is lined up at ``x``.  Returns ``step(i)`` that animates row i:
    the first row is written, each later one grows out of a copy of the previous one (matching tex parts move into
    place), and its grey 'why' note fades in beside or below it."""
    for r, w in zip(rows, whys):
        r.shift((x - r[align_index].get_center()[0]) * RIGHT)
        lo, hi = r.get_left()[0], r.get_right()[0]
        f = min(1.0, (edge - x) / (hi - x) if hi > edge else 1.0, (x + edge) / (x - lo) if lo < -edge else 1.0)
        if f < 1.0:
            r.scale(f, about_point=np.array([x, r.get_y(), 0]))
        if w is not None:
            below = getattr(w, "below", False)
            if not below:
                w.next_to(r, RIGHT, buff=0.4)
                if w.get_right()[0] > edge:
                    below = True
            if below:  # under the row (clear of a box drawn around it), right-aligned with it or the frame edge
                w.next_to(r, DOWN, buff=0.28)
                w.set_x(min(r.get_right()[0], edge) - w.width / 2)
                w.set_x(max(w.get_x(), -edge + w.width / 2))
    offs = [0.0 if w is None else w.get_y() - r.get_y() for r, w in zip(rows, whys)]

    def step(i, run_time=1.3):
        anims = []
        shown = rows[max(0, i - keep + 1): i]
        if i >= keep:
            anims.append(FadeOut(rows[i - keep], shift=UP * 0.3))
            if whys[i - keep] is not None:
                anims.append(FadeOut(whys[i - keep], shift=UP * 0.3))
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
            scene.play(*anims, run_time=0.6)
        if i == 0:
            scene.play(Write(rows[i]), run_time=run_time)
        else:
            scene.play(TransformMatchingTex(rows[i - 1].copy(), rows[i]), run_time=run_time)
        if whys[i] is not None:
            scene.play(FadeIn(whys[i]), run_time=0.5)

    return step


def side_note(text: str, mob: Mobject, font_size=24, color=GREY_B, direction=RIGHT, buff=0.35) -> Tex:
    return label(text, font_size=font_size, color=color).next_to(mob, direction, buff=buff)


def color_tex(m: MathTex, colors: dict) -> MathTex:
    """Color sub-tex pieces of ``m`` by index: {index: color}."""
    for i, c in colors.items():
        m[i].set_color(c)
    return m


# ---------------------------------------------------------------------------
# Phasors
# ---------------------------------------------------------------------------
def phasor_chain(zs, origin=ORIGIN, unit=1.0, stroke_width=3.0, tips=True, tip_length=0.1, opacity=1.0) -> VGroup:
    """Complex numbers drawn tip to tail from ``origin``, each colored by its own phase.  With many small arrows
    (``tips=False``) the chain reads as a curve whose color shows the phase along it."""
    zs = np.asarray(zs, complex)
    pts = np.concatenate([[0], np.cumsum(zs)]) * unit
    g = VGroup()
    o = np.array(origin, float)
    for z, a, b in zip(zs, pts[:-1], pts[1:]):
        p0 = o + np.array([a.real, a.imag, 0])
        p1 = o + np.array([b.real, b.imag, 0])
        col = hue(np.angle(z))
        if tips and abs(b - a) > 1e-3:
            m = Arrow(p0, p1, buff=0, color=col, stroke_width=stroke_width, tip_length=min(tip_length, 0.4 * abs(b - a)),
                      max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=40)
        else:
            m = Line(p0, p1, color=col, stroke_width=stroke_width)
        m.set_opacity(opacity)
        g.add(m)
    return g


def chain_end(zs, origin=ORIGIN, unit=1.0) -> np.ndarray:
    s = complex(np.sum(zs)) * unit
    return np.array(origin, float) + np.array([s.real, s.imag, 0])


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------
def to_img(rgba: np.ndarray, height: float | None = None, width: float | None = None) -> ImageMobject:
    m = ImageMobject(rgba)
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    if height is not None:
        m.stretch_to_fit_height(height)
    if width is not None:
        m.stretch_to_fit_width(width)
    return m


def phase_rgba(psi, vmax=None, gamma=0.7, alpha=1.0) -> np.ndarray:
    """Complex array (rows = y top->bottom) -> RGBA uint8, hue = phase, brightness = |psi| / vmax."""
    return qcm.rgba(qcm.phase_rgb(psi, vmax=vmax, gamma=gamma, hot=0.0), alpha)


def phase_img(psi, height=None, width=None, vmax=None, gamma=0.7) -> ImageMobject:
    return to_img(phase_rgba(psi, vmax=vmax, gamma=gamma), height, width)


def signed_rgba(f, vmax=None, pos=C.WIGNER_POS, neg=C.WIGNER_NEG, gamma=0.85) -> np.ndarray:
    f = np.asarray(f, float)
    vmax = float(np.abs(f).max()) if vmax is None else vmax
    return qcm.rgba(qcm.real_rgb(f, vmax, pos=pos, neg=neg, gamma=gamma))


def signed_img(f, height=None, width=None, vmax=None, pos=C.WIGNER_POS, neg=C.WIGNER_NEG, gamma=0.85) -> ImageMobject:
    return to_img(signed_rgba(f, vmax, pos, neg, gamma), height, width)


def gold_rgba(d, vmax=None, gamma=0.6, color=C.BORN) -> np.ndarray:
    d = np.asarray(d, float)
    vmax = float(d.max()) if vmax is None else vmax
    t = np.clip(d / max(vmax, 1e-30), 0, 1) ** gamma
    c = qcm.hex_rgb(ManimColor(color).to_hex())
    return qcm.rgba(qcm.BG + t[..., None] * (c - qcm.BG))


def gold_img(d, height=None, width=None, vmax=None, gamma=0.6, color=C.BORN) -> ImageMobject:
    return to_img(gold_rgba(d, vmax, gamma, color), height, width)


def sphere_img(key: str, height=1.6) -> ImageMobject:
    """A precomputed function-on-a-sphere render (compute item ``symmetry``, keys ``Y_l_m``)."""
    return to_img(load("symmetry")[key], height=height, width=height)


def framed(mob: Mobject, color=GREY_C, buff=0.04, stroke_width=1.5) -> Rectangle:
    return Rectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff, stroke_color=color,
                     stroke_width=stroke_width).move_to(mob)


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
def plain_axes(x_range, y_range, x_length, y_length, ticks=False, **kw) -> Axes:
    cfg = {"stroke_color": GREY_B, "stroke_width": 2, "include_ticks": ticks, "tip_length": 0.15}
    cfg.update(kw.pop("axis_config", {}))
    return Axes(x_range=list(x_range), y_range=list(y_range), x_length=x_length, y_length=y_length, tips=False,
                axis_config=cfg, **kw)


def tick_labels(ax: Axes, xs=(), ys=(), font_size=22, fmt=None, color=GREY_B) -> VGroup:
    """Small numeric labels under the x axis / left of the y axis at the given values (strings via ``fmt``)."""
    g = VGroup()
    f = fmt or (lambda v: f"{v:g}")
    for v in xs:
        p = ax.c2p(v, ax.y_range[0])
        g.add(Line(p, p + UP * 0.08, color=color, stroke_width=1.5),
              MathTex(f(v), font_size=font_size, color=color).next_to(p, DOWN, buff=0.08))
    for v in ys:
        p = ax.c2p(ax.x_range[0], v)
        g.add(Line(p, p + RIGHT * 0.08, color=color, stroke_width=1.5),
              MathTex(f(v), font_size=font_size, color=color).next_to(p, LEFT, buff=0.08))
    return g


def curve(ax: Axes, xs, ys, color=WHITE, stroke_width=3, **kw) -> VMobject:
    return polyline(ax, xs, ys, color=color, stroke_width=stroke_width, **kw)


def dots(ax: Axes, xs, ys, color=WHITE, radius=0.05, **kw) -> VGroup:
    return VGroup(*[Dot(ax.c2p(x, y), radius=radius, color=color, **kw) for x, y in zip(xs, ys)])


def lframe(ax: Axes, color=GREY_B, stroke_width=2) -> VGroup:
    """Hide the axes Manim draws through the origin and return an L-shaped frame along the bottom and left edges of
    the plotting area instead (for log scales, where the origin is in the middle of the plot).  frame[0] is the
    bottom edge, frame[1] the left edge: put the axis labels at their ends."""
    ax.x_axis.set_stroke(opacity=0)
    ax.y_axis.set_stroke(opacity=0)
    x0, x1 = ax.x_range[0], ax.x_range[1]
    y0, y1 = ax.y_range[0], ax.y_range[1]
    return VGroup(Line(ax.c2p(x0, y0), ax.c2p(x1, y0), color=color, stroke_width=stroke_width),
                  Line(ax.c2p(x0, y0), ax.c2p(x0, y1), color=color, stroke_width=stroke_width))
