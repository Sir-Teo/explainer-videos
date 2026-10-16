"""Helpers shared by the scenes of Part 4 ("Randomness in Motion")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

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
