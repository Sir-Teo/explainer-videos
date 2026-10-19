"""Helpers shared by the scenes of Part 9 ("Networks")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 9
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
CLS_A, CLS_B = "#E86F8A", "#58A6FF"  # the two classes (spirals, perceptron points, XOR)
HINGE = C.MODEL_Q  # a ReLU's bend, hinges, pieces
NEURON = "#7FD3FF"  # units
WEIGHT = C.BITS  # weights w
FWD = C.ACTS  # the forward pass: values
BWD = C.GRADS  # the backward pass: gradients, deltas
RES = C.BITS  # the residual stream
NORM = C.INTERVAL  # normalization
PLAIN = C.SURPRISE  # plain stacks, things that fail
ORDER, CRIT, CHAOS = "#58A6FF", C.BITS, "#FF6B8B"  # the ordered phase, the edge, the chaotic phase
GATE = C.CONTEXT  # gates
KANC = "#5CD0B3"  # Kolmogorov-Arnold networks
HIST = C.HUMAN  # history cards

PANEL_FILL = "#121722"


def rgb_of(c) -> np.ndarray:
    return np.array(ManimColor(c).to_rgb())


def region_image(prob, regions, xs, width, height, boundary=True) -> ImageMobject:
    """Decision regions as a picture: tinted by the probability of class B, with the network's linear pieces drawn
    as thin light lines where the activation pattern changes."""
    p = np.asarray(prob)
    ca, cb = rgb_of(CLS_A), rgb_of(CLS_B)
    bg = rgb_of("#0B0F17")
    rgb = (1 - p)[..., None] * ca + p[..., None] * cb
    rgb = 0.55 * bg + 0.45 * rgb
    if boundary:
        r = np.asarray(regions)
        edge = np.zeros(r.shape, bool)
        edge[1:, :] |= r[1:, :] != r[:-1, :]
        edge[:, 1:] |= r[:, 1:] != r[:, :-1]
        rgb[edge] = 0.6 * rgb[edge] + 0.4 * np.array([0.92, 0.92, 0.95])
    img = ImageMobject((np.concatenate([rgb, np.ones(p.shape + (1,))], -1)[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def patch_image(regions, width, height, seed=0) -> ImageMobject:
    """Linear pieces, each its own colour."""
    r = np.asarray(regions)
    _, inv = np.unique(r, return_inverse=True)
    inv = inv.reshape(r.shape)
    hue = (inv * 0.61803 + seed * 0.1) % 1.0
    rgb = np.stack([0.32 + 0.3 * np.sin(2 * math.pi * hue), 0.38 + 0.28 * np.sin(2 * math.pi * (hue + 0.33)),
                    0.52 + 0.28 * np.sin(2 * math.pi * (hue + 0.66))], -1)
    img = ImageMobject((np.concatenate([rgb, np.ones(r.shape + (1,))], -1)[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def two_tone(mask, width, height, a=CLS_A, b=CLS_B, strength=0.45) -> ImageMobject:
    """A 0/1 array (rows bottom to top) as two tints over the background."""
    m = np.asarray(mask, float)
    bg = rgb_of("#0B0F17")
    rgb = (1 - m)[..., None] * rgb_of(a) + m[..., None] * rgb_of(b)
    rgb = (1 - strength) * bg + strength * rgb
    img = ImageMobject((np.concatenate([rgb, np.ones(m.shape + (1,))], -1)[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def heat(Z, lo, hi, width, height, colors=("#1B2A6B", "#2E6FB0", "#3FB8AF", "#F2D16B", "#F28C5B")) -> ImageMobject:
    """A 2-D array (rows bottom to top) through a colour scale from ``lo`` to ``hi``."""
    t = np.clip((np.asarray(Z, float) - lo) / (hi - lo), 0, 1)
    stops = np.array([rgb_of(c) for c in colors])
    x = t * (len(stops) - 1)
    i = np.minimum(x.astype(int), len(stops) - 2)
    f = (x - i)[..., None]
    rgb = stops[i] * (1 - f) + stops[i + 1] * f
    img = ImageMobject((np.concatenate([rgb, np.ones(t.shape + (1,))], -1)[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def panel(width, height, center=ORIGIN, color=GREY_D) -> RoundedRectangle:
    return RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color=color, stroke_width=1.5,
                            fill_color=PANEL_FILL, fill_opacity=1).move_to(center)


def unit_circle(tex=r"\Sigma", radius=0.42, color=NEURON, font_size=34) -> VGroup:
    c = Circle(radius=radius, color=color, stroke_width=3.5, fill_color=PANEL_FILL, fill_opacity=1)
    return VGroup(c, MathTex(tex, font_size=font_size).move_to(c))


def network(widths, x0=-4.0, x1=4.0, height=4.4, center=ORIGIN, radius=0.2, color=NEURON, edge_color=GREY_D,
            edge_width=1.4) -> VGroup:
    """Layers of circles joined by every edge. ``net.layers[i]`` are the circles of layer i, ``net.edges[i]`` the
    edges from layer i to i + 1 (row-major: from each unit of layer i to each of layer i + 1)."""
    L = len(widths)
    xs = np.linspace(x0, x1, L)
    layers = VGroup()
    for x, w in zip(xs, widths):
        ys = np.linspace(height / 2, -height / 2, w) if w > 1 else np.array([0.0])
        layers.add(VGroup(*[Circle(radius=radius, color=color, stroke_width=2.5, fill_color=PANEL_FILL,
                                   fill_opacity=1).move_to([x, y, 0]) for y in ys]))
    edges = VGroup()
    for a, b in zip(layers, layers[1:]):
        edges.add(VGroup(*[Line(u.get_center(), v.get_center(), buff=radius, stroke_width=edge_width,
                                color=edge_color) for u in a for v in b]))
    g = VGroup(edges, layers)
    g.layers, g.edges = layers, edges
    return g.move_to(center)


def log_axes(x_range, y_range, x_length, y_length, center, xlabel="", ylabel="", xticks=(), yticks=(),
             font_size=20) -> VGroup:
    """Axes in log10 units, with ticks labelled 10^k."""
    return axes(x_range, y_range, x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel,
                xticks=list(xticks), yticks=list(yticks), xfmt=lambda v: rf"10^{{{int(v)}}}",
                yfmt=lambda v: rf"10^{{{int(v)}}}", center=center, font_size=font_size)


def words(n: int) -> str:
    """Small numbers in words, for narration."""
    w = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
    return w[n] if 0 <= n < len(w) else f"{n:,}"
