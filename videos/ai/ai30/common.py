"""Helpers shared by the scenes of Part 30 ("Inside the Model").

Part 16 imports ``show`` from here: keep it.
"""

from __future__ import annotations

import textwrap

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import heat_image, signed_image  # noqa: F401

from .compute import load  # noqa: F401

PART = 30
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
RESID = C.QUERY  # the residual stream's raw numbers
FEAT = C.BITS  # a dictionary's features (latents)
NEURON = C.NEURAL  # the model's own neurons
PROBE = C.TRUE_P  # probes, lenses: reading out
CAUSE = C.SURPRISE  # interventions: patching, ablation, steering
CTRL = GREY_B  # controls and baselines
BASEM = GREY_B  # the base model
CHAT = C.ASSISTANT  # the chat fine-tune
FEATURE_COLORS = [C.TRUE_P, C.BITS, C.INTERVAL, C.SURPRISE, C.NEURAL, C.MODEL_Q]


def show(ch: str) -> str:
    return {" ": "·", "\n": "⏎"}.get(ch, ch)


def show_tok(t: str) -> str:
    """A token of the novels model, made visible: spaces as dots, line breaks as arrows."""
    return t.replace(" ", "·").replace("\n", "⏎")


def context_line(ctx: str, width: float, font_size=20, color=FEAT, at: int = -2) -> VGroup:
    """A window of text, one glyph per character, with the character at ``at`` lit (where the unit fired)."""
    n = len(ctx)
    step = width / n
    i_hot = at % n
    g = VGroup()
    for i, ch in enumerate(ctx):
        hot = i == i_hot
        t = data_text(show(ch), font=MONO, font_size=font_size, color=WHITE if hot else (GREY_B if i < i_hot else GREY_D))
        t.move_to([-width / 2 + step * (i + 0.5), 0, 0])
        if hot:
            g.add(Rectangle(width=step * 1.05, height=font_size / 48 * 0.75, stroke_width=0, fill_color=color,
                            fill_opacity=0.55).move_to(t))
        g.add(t)
    return g


def arrow2d(origin, vec, color, scale=1.0, stroke_width=5) -> Arrow:
    end = origin + scale * np.array([vec[0], vec[1], 0.0])
    return Arrow(origin, end, buff=0, stroke_width=stroke_width, color=color, max_tip_length_to_length_ratio=0.15,
                 max_stroke_width_to_length_ratio=12)


def vec_bars(v, width, height, color, signed=True, floor=0.004) -> VGroup:
    """A vector as a row of thin bars (up for positive, down for negative), ``width`` wide and ``height`` tall at most."""
    v = np.asarray(v, float)
    top = max(np.abs(v).max(), 1e-9)
    w = width / len(v)
    g = VGroup()
    for i, x in enumerate(v):
        h = max(abs(x) / top * height / (2 if signed else 1), floor)
        r = Rectangle(width=w * 0.8, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9 if abs(x) > 1e-9 else 0.2)
        r.move_to([-width / 2 + w * (i + 0.5), (h / 2) * (1 if x >= 0 else -1), 0])
        g.add(r)
    return g


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def model_text(text: str, chars: int = 48, font_size: int = 20, max_lines: int = 3, color=GREY_A, box=None) -> VGroup:
    """Words a model read or wrote: monospaced, wrapped, never translated."""
    lines = textwrap.wrap(" ".join(text.split()), chars) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: chars - 3] + "..."
    t = data_text("\n".join(lines), font=MONO, font_size=font_size, color=color, line_spacing=0.8)
    if box is None:
        return VGroup(t)
    r = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.35, corner_radius=0.12, stroke_color=box,
                         stroke_width=2, fill_color=box, fill_opacity=0.06)
    return VGroup(r, t.move_to(r))


def bars(values, width, height, colors, vmax=None, gap=0.25, base_y=0.0) -> VGroup:
    """Vertical bars side by side, bottoms on ``base_y``; ``colors`` a colour or a list."""
    vals = np.asarray(values, float)
    vmax = vmax or max(float(np.nanmax(np.abs(vals))), 1e-9)
    n = len(vals)
    w = width / n
    g = VGroup()
    for i, v in enumerate(vals):
        col = colors[i] if isinstance(colors, (list, tuple)) else colors
        h = max(abs(v) / vmax * height, 0.01) if np.isfinite(v) else 0.01
        r = Rectangle(width=w * (1 - gap), height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
        r.move_to([-width / 2 + w * (i + 0.5), base_y + (h / 2 if v >= 0 else -h / 2), 0])
        g.add(r)
    return g


def grid_image(M, width, height, cmap="signed", vmax=None, pos=None, neg=None):
    """A matrix as an image: ``signed`` (blue-white-red style around zero, from the part's colours) or heat."""
    M = np.asarray(M, float)
    if cmap == "signed":
        return signed_image(M, width, height, pos=pos or C.TRUE_P, neg=neg or C.SURPRISE)
    return heat_image(M, width, height, color=pos or FEAT, gamma=0.7)


def heads_grid(vals, color, cell=0.62, fmt="{:.2f}", vmax=None, font_size=20, labels=True) -> VGroup:
    """A layers x heads table of numbers, each cell shaded by its value."""
    vals = np.asarray(vals, float)
    vmax = vmax or max(float(np.nanmax(np.abs(vals))), 1e-9)
    L, H = vals.shape
    g = VGroup()
    cells = VGroup()
    for l_ in range(L):
        for h in range(H):
            v = vals[l_, h]
            sq = Square(cell, stroke_color=GREY_D, stroke_width=1, fill_color=color,
                        fill_opacity=0.05 + 0.85 * min(abs(v) / vmax, 1)).move_to([h * cell, -l_ * cell, 0])
            t = MathTex(fmt.format(v), font_size=font_size, color=WHITE).move_to(sq)
            cells.add(VGroup(sq, t))
    g.add(cells)
    if labels:
        for h in range(H):
            g.add(MathTex(rf"h_{h + 1}", font_size=font_size, color=GREY_B).next_to(cells[h], UP, buff=0.1))
        for l_ in range(L):
            g.add(label(rf"layer ${l_ + 1}$", font_size=font_size - 2, color=GREY_B).next_to(cells[l_ * H], LEFT, buff=0.15))
    g.cells = cells
    return g


def spread_bar(ax, x, vals, color, width=0.12):
    """The spread of several seeds at one x: a thin line from min to max, a dot at the mean."""
    vals = [v for v in vals if np.isfinite(v)]
    if not vals:
        return VGroup()
    lo, hi, mu = min(vals), max(vals), float(np.mean(vals))
    return VGroup(Line(ax.c2p(x, lo), ax.c2p(x, hi), color=color, stroke_width=3),
                  Line(ax.c2p(x, lo) + LEFT * width / 2, ax.c2p(x, lo) + RIGHT * width / 2, color=color, stroke_width=2),
                  Line(ax.c2p(x, hi) + LEFT * width / 2, ax.c2p(x, hi) + RIGHT * width / 2, color=color, stroke_width=2),
                  Dot(ax.c2p(x, mu), radius=0.06, color=color))


def ticks(lo, hi, n=4) -> list:
    """A few round tick values inside [lo, hi]."""
    raw = (hi - lo) / n
    step = 10 ** np.floor(np.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * step:
            step *= m
            break
    return [float(round(v, 9)) + 0.0 for v in np.arange(np.ceil(lo / step) * step, hi + 1e-9, step)]


def num_words(n: int) -> str:
    """Small whole numbers in words, for narration ("three seeds")."""
    w = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
    return w[n] if 0 <= n < len(w) else str(n)
