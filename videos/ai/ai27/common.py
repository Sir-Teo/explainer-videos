"""Helpers shared by the scenes of Part 27 ("Post-Training and Alignment")."""

from __future__ import annotations

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 27
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
USER = C.USER  # the person's turn
ASSIST = C.ASSISTANT  # the model's answer
BASE = GREY_B  # the base (pretrained) model
POLICY = C.RL_POLICY  # the model being tuned, pi_theta
REF = C.REFERENCE  # the reference model pi_ref
REWARD = C.REWARD  # reward, the preferred answer
PENALTY = C.PENALTY  # the rejected answer, a failure
KLC = C.KL  # KL divergence, the leash
PROXY = C.MODEL_Q  # the learned reward model (a proxy)
GOLD = C.SCORE  # the true taste the proxy stands in for
ADAPT = C.MLP  # adapters, task vectors


def bubble(text: str, who: str = "user", width: float = 5.6, font_size: int = 24) -> VGroup:
    """A chat turn: a rounded box, the speaker's colour on its edge."""
    col = USER if who == "user" else ASSIST
    t = label(text, font_size=font_size, color=WHITE)
    if t.width > width - 0.4:
        t.width = width - 0.4
    box = RoundedRectangle(width=max(t.width + 0.4, 1.2), height=t.height + 0.35, corner_radius=0.15,
                           stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.08)
    return VGroup(box, t.move_to(box))


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def said(text: str, who: str = "assistant", chars: int = 44, font_size: int = 20, max_lines: int = 4) -> VGroup:
    """A chat turn holding words a model (or a person in the data) actually wrote: monospaced, wrapped, never
    translated, never read as LaTeX."""
    import textwrap

    col = USER if who == "user" else ASSIST
    lines = textwrap.wrap(" ".join(text.split()), chars) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: chars - 3] + "..."
    t = data_text("\n".join(lines), font=MONO, font_size=font_size, color=WHITE, line_spacing=0.8)
    box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.35, corner_radius=0.15, stroke_color=col,
                           stroke_width=2.5, fill_color=col, fill_opacity=0.08)
    return VGroup(box, t.move_to(box))
