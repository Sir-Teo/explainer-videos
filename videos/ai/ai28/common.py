"""Helpers shared by the scenes of Part 28 ("Reasoning")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 28
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
DIRECT = C.MODEL_Q  # answering at once
CHAIN = C.WORK_TOK  # tokens of thought: the chain, the scratchpad
FILLER = GREY_B  # filler tokens: positions without meaning
RIGHT_C, WRONG_C = C.REWARD, C.PENALTY  # a right answer (or step), a wrong one
POLICY = C.RL_POLICY  # the model being trained, pi_theta
REF = C.REFERENCE  # the starting (reference) model
OLD = C.OLD_POLICY  # pi_old, the model that sampled the batch
RATIO = C.RATIO  # importance ratios rho
ADV = C.ADVANTAGE  # advantages A
KLC = C.KL  # KL divergence, the leash
ENT = C.ENTROPY  # entropy
LEN = C.LENGTH  # length: steps of thought, tokens
VOTE = C.TRUE_P  # majority vote
PASS = C.BITS  # pass@k: any of k right (an oracle checker)
ORM_C = C.ATTN  # the outcome reward model
PRM_C = C.NEURAL  # the process reward model
SEARCH = C.BITS  # search: beams, trees
LEAN = C.INTERVAL  # formal proof: Lean's kernel says yes

# the think-or-answer task (think.py): tokens as they are drawn
T_PAD, T_EQ, T_THINK, T_ANS, T_END, T_V0 = 10, 11, 12, 13, 14, 15


def chip(text: str, size=0.46, color=GREY_B, font_size=28, fill=0.12, width=None) -> VGroup:
    """A rounded box with a short monospace text in it (data: never translated)."""
    box = RoundedRectangle(width=width or size, height=size, corner_radius=0.08, stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=fill)
    t = data_text(text, font=MONO, font_size=font_size, color=WHITE).move_to(box)
    if t.width > box.width - 0.08:
        t.width = box.width - 0.08
    return VGroup(box, t)


def bit_row(bits, size=0.46, buff=0.08, color=GREY_B, font_size=28) -> VGroup:
    return VGroup(*[chip(str(int(b)), size, color, font_size) for b in bits]).arrange(RIGHT, buff=buff)


def mark(ok: bool, font_size=30) -> MathTex:
    return MathTex(r"\checkmark" if ok else r"\times", font_size=font_size, color=RIGHT_C if ok else WRONG_C)


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def hit_image(R, width, height) -> ImageMobject:
    """A boolean matrix as a picture: green where right, dark red where wrong."""
    R = np.asarray(R, bool)
    g, r = np.array(ManimColor(RIGHT_C).to_rgb()), np.array(ManimColor(WRONG_C).to_rgb()) * 0.45
    rgb = np.where(R[..., None], g, r)
    img = ImageMobject((np.concatenate([rgb, np.ones(R.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def heat(Z, width, height, color=CHAIN, vmax=None, low="#141A24") -> ImageMobject:
    """A non-negative matrix as a picture, dark to ``color`` (rows top to bottom as given)."""
    Z = np.asarray(Z, float)
    t = np.clip(Z / (vmax or max(Z.max(), 1e-9)), 0, 1)[..., None]
    a, b = np.array(ManimColor(low).to_rgb()), np.array(ManimColor(color).to_rgb())
    rgb = a + (b - a) * t
    img = ImageMobject((np.concatenate([rgb, np.ones(Z.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def healthy(o, v):
    """Which runs of objective v (in the ``objectives`` item) did not collapse: those that end at least as accurate as
    they started. If every run collapsed, all of them (so a plot still has something to show)."""
    C = np.asarray(o[f"{v}_curves"])
    ok = C[:, -1, 1] >= C[:, 0, 1]
    return ok if ok.any() else np.ones_like(ok, bool)


def seeds_plot(ax, xs, Y, color, width=3.5, opacity=0.2):
    """The mean over seeds (rows of Y) as a line, and the lowest-to-highest band."""
    Y = np.asarray(Y, float)
    return VGroup(band(ax, xs, Y.min(0), Y.max(0), color, opacity=opacity), curve(ax, xs, Y.mean(0), color, width))


def solution_chips(tokens, size=0.42, font_size=20, steps_ok=None, answer_ok=None, show_question=True) -> VGroup:
    """A think-or-answer solution as a row of chips: the digits, '=', THINK, the running totals, ANS, the answer.
    ``steps_ok`` colours each step right or wrong; ``answer_ok`` the answer."""
    t = [int(v) for v in np.asarray(tokens) if v >= 0]
    row = VGroup()
    i = 0
    if show_question:
        for v in t[:10]:
            if v < 10:
                row.add(chip(str(v), size, GREY_B, font_size))
    k = 0
    phase = 0
    for v in t[10:]:
        if v == T_EQ:
            row.add(chip("=", size, GREY_C, font_size, fill=0.0))
        elif v == T_THINK:
            row.add(chip("think", size, CHAIN, font_size - 4, width=size * 2.2, fill=0.25))
            phase = 1
        elif v == T_ANS:
            row.add(chip("ans", size, DIRECT, font_size - 4, width=size * 1.8, fill=0.25))
            phase = 2
        elif v >= T_V0:
            val = str(v - T_V0)
            if phase == 1:
                ok = None if steps_ok is None or k >= len(steps_ok) else bool(steps_ok[k])
                col = CHAIN if ok is None else (RIGHT_C if ok else WRONG_C)
                row.add(chip(val, size, col, font_size, width=size * 1.25, fill=0.18))
                k += 1
            else:
                col = WHITE if answer_ok is None else (RIGHT_C if answer_ok else WRONG_C)
                row.add(chip(val, size, col, font_size, width=size * 1.25, fill=0.3))
                break
        i += 1
    return row.arrange(RIGHT, buff=0.06)


def tile_frame(caption, color, TW=3.0, TH=2.0):
    box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D, stroke_width=1.5,
                           fill_color="#121722", fill_opacity=1)
    return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)


def pct(x: float) -> str:
    """A share as spoken: 'about 37 percent'."""
    return f"{100 * float(x):.0f}"


def spread_txt(vals) -> str:
    """'from 71 to 78 percent' over seeds, or one number when they agree."""
    v = [100 * float(x) for x in vals]
    lo, hi = min(v), max(v)
    return f"{lo:.0f} percent" if round(lo) == round(hi) else f"from {lo:.0f} to {hi:.0f} percent"
