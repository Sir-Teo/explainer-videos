"""Helpers shared by the scenes of Part 29 ("Agents and Worlds")."""

from __future__ import annotations

import textwrap

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 29
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
AGENT = C.RL_POLICY  # the agent, its policy, the learner
EXPERT = C.EXPERT  # the expert, the demonstrator
WORLD = C.ENVIRONMENT  # the environment, reality
BELIEF = C.TRUE_P  # beliefs, the posterior
OBS = C.OBSERVED  # observations
TOOL = C.MLP  # tools and their results
MODEL = C.LATENT  # a learned world model, its latent state, imagination
REWARD = C.REWARD
FAIL = C.PENALTY  # an error, off the road, a fall
GOOD = C.INTERVAL  # a step that went right
HIST = C.HUMAN  # history cards
CLAIM = GREY_B  # a company's own claim


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, fill=0.1) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=fill)
    return VGroup(box, t.move_to(box))


def trace_box(lines, chars=44, font_size=18, width=None, max_lines=14, color=GREY_B) -> VGroup:
    """An agent's trace (lines its loop actually printed): monospaced, never translated, coloured by kind."""
    colours = {"Thought": GREY_A, "Action": AGENT, "Observation": TOOL, "Answer": REWARD}
    rows = VGroup()
    for ln in lines[:max_lines]:
        kind = ln.split(":")[0]
        col = colours.get(kind, GREY_A)
        if "error" in ln:
            col = FAIL
        for k, piece in enumerate(textwrap.wrap(ln, chars) or [""]):
            rows.add(data_text(("  " if k else "") + piece, font=MONO, font_size=font_size, color=col))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    if width and rows.width > width - 0.4:
        rows.width = width - 0.4
    box = RoundedRectangle(width=(width or rows.width + 0.4), height=rows.height + 0.35, corner_radius=0.12,
                           stroke_color=color, stroke_width=1.6, fill_color="#0B0F17", fill_opacity=0.95)
    rows.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.2)
    g = VGroup(box, rows)
    g.rows = rows
    return g


def gray(a, size, color=None, height=None) -> ImageMobject:
    """A picture (values 0..1) tinted with ``color``, scaled to ``size`` wide, pixels kept sharp."""
    a = np.clip(np.asarray(a, float), 0, 1)
    tint = np.array(ManimColor(color or WHITE).to_rgb())
    base = np.array(ManimColor("#10141C").to_rgb())
    rgb = base[None, None] * (1 - a[..., None]) + a[..., None] * tint[None, None]
    rgba = np.concatenate([rgb, np.ones(a.shape + (1,))], -1)
    img = ImageMobject((rgba * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.stretch_to_fit_width(size)
    return img.stretch_to_fit_height(height or size * a.shape[0] / a.shape[1])


def framed(img, color=GREY_D, buff=0.04):
    return Group(img, SurroundingRectangle(img, color=color, buff=buff, stroke_width=1.5))


def score_bar(value, vmax, width, color, height=0.32) -> VGroup:
    """A horizontal bar for a published score (0..vmax), drawn to ``width`` at vmax."""
    back = Rectangle(width=width, height=height, stroke_width=1, stroke_color=GREY_D, fill_opacity=0)
    w = max(width * value / vmax, 0.02)
    bar = Rectangle(width=w, height=height, stroke_width=0, fill_color=color, fill_opacity=0.85)
    bar.align_to(back, LEFT)
    return VGroup(back, bar)


def spread_band(ax, xs, Y, color, opacity=0.18):
    """min-max band over seeds (rows of Y) and the mean as a curve."""
    Y = np.asarray(Y, float)
    return VGroup(band(ax, xs, Y.min(0), Y.max(0), color, opacity), curve(ax, xs, Y.mean(0), color, 3.5))


def years_label(y: float) -> str:
    """Years since 2019 (as in the METR fit) to a calendar year with a decimal."""
    return f"{2019 + y:.1f}"
