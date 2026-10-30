"""Helpers shared by the scenes of Part 16 ("Sparsity")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401
from . import facts as F  # noqa: F401

PART = 16
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
ROUTER = C.ROUTER  # router scores, the choice of experts
EXPERTC = C.EXPERT  # experts (feed-forward networks)
SHAREDC = C.SHARED_EXPERT  # always-on shared experts
BALC = C.BALANCE  # balancing biases, loads
MOEC = C.INTERVAL  # our mixture of experts (the model)
DENSEC = GREY_B  # the dense model with the mixture's arithmetic
TOTALC = "#7FD3FF"  # the dense model with the mixture's parameters
HISTC = C.HUMAN  # history cards
GRADC = C.SURPRISE  # gradients
DROPC = C.SURPRISE  # dropped tokens
COMMC = C.COMM  # all-to-all traffic
WINC, BLOCKC, INDEXC, FULLC = C.LOCAL, C.BITS, C.INDEXER, C.GLOBAL  # attention patterns
TICKETC, REINITC, RANDC = C.INTERVAL, C.SURPRISE, GREY_B  # lottery tickets
EXPERT_COLORS = ["#58A6FF", "#F7D154", "#FF6B8B", "#5BD17A", "#D4A5FF", "#FF9F45", "#7FD3FF", "#E86F8A"]
MODES = [("none", r"no balancing", C.SURPRISE), ("aux", r"Switch's auxiliary loss", C.TRUE_P),
         ("moe", r"DeepSeek's loss-free bias", C.INTERVAL)]
MODE_NAME = {k: n for k, n, _ in MODES}
MODE_COLOR = {k: c for k, _, c in MODES}


def show(ch: str) -> str:
    """A character made visible: a space as a dot, a line break as an arrow."""
    return {" ": "·", "\n": "⏎"}.get(ch, ch)


def billions(v: float) -> str:
    return (f"{v / 1e12:.2f}".rstrip("0").rstrip(".") + r"\,\mathrm{T}") if v >= 1e12 else (
        f"{v / 1e9:,.1f}".rstrip("0").rstrip(".") + r"\,\mathrm{B}")


def spoken_b(v: float) -> str:
    """Parameters for the narrator: '671 billion', '1.6 trillion'."""
    if v >= 1e12:
        return f"{v / 1e12:.1f}".rstrip("0").rstrip(".") + " trillion"
    return f"{v / 1e9:.0f} billion" if v >= 10e9 else f"{v / 1e9:.1f}".rstrip("0").rstrip(".") + " billion"


def pct(x: float, digits=0) -> str:
    return f"{100 * x:.{digits}f}"


def ms(vals) -> tuple[float, float, float]:
    """Mean, min and max of a few seeds' numbers."""
    a = np.asarray(vals, float)
    return float(a.mean()), float(a.min()), float(a.max())


def seeds_tex(vals, digits=3) -> str:
    """'2.412 (2.401 to 2.420)' as TeX: the mean and the range over seeds."""
    m, lo, hi = ms(vals)
    return rf"{m:.{digits}f}\ \ ({lo:.{digits}f}\text{{--}}{hi:.{digits}f})"


def seed_curves(ax, arr, color, width=3, opacity=0.18, ys=None) -> VGroup:
    """Several seeds' curves (array seeds x points x 2) as a mean line over a band from the lowest to the highest."""
    a = np.asarray(arr, float)
    xs = a[0, :, 0]
    y = a[:, :, 1] if ys is None else ys
    lo, hi, mu = y.min(0), y.max(0), y.mean(0)
    return VGroup(band(ax, xs, lo, hi, color, opacity), curve(ax, xs, mu, color, width))


def load_image(L, width, height, E=None, fair=None) -> ImageMobject:
    """Expert loads over training as a picture: rows = experts, columns = time; bright = busy (1 = a fair share)."""
    L = np.asarray(L, float).T  # expert, time
    E = E or L.shape[0]
    v = np.clip(L * E / 3.0, 0, 1) ** 0.7  # 3x a fair share or more: full brightness
    hot = np.array(ManimColor(C.BITS).to_rgb())
    bg = np.array(ManimColor("#121722").to_rgb())
    rgb = bg[None, None] * (1 - v[..., None]) + hot[None, None] * v[..., None]
    img = ImageMobject((np.concatenate([rgb, np.ones(v.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def heat(Z, width=4.0, height=3.0, color=C.KEY, gamma=0.6, bg="#121722", vmax=None) -> ImageMobject:
    """A non-negative 2-D array as a picture, rows top to bottom, from the background colour (0) to ``color``."""
    Z = np.asarray(Z, float)
    t = np.clip(Z / max(vmax or Z.max(), 1e-12), 0, 1) ** gamma
    a, b = np.array(ManimColor(bg).to_rgb()), np.array(ManimColor(color).to_rgb())
    rgb = a + (b - a) * t[..., None]
    img = ImageMobject((np.concatenate([rgb, np.ones(Z.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def take_away(text: str, color=WHITE, font_size=26) -> VGroup:
    """The chapter's takeaway: a line in a thin box, at the bottom of the frame."""
    t = label(text, font_size=font_size, color=color)
    if t.width > 12.4:
        t.width = 12.4
    box = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.3, corner_radius=0.12, stroke_color=color,
                           stroke_width=1.5, fill_color="#0B0F17", fill_opacity=0.95)
    return VGroup(box, t.move_to(box)).to_edge(DOWN, buff=0.3)


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, fill=0.1) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=fill)
    g = VGroup(box, t.move_to(box))
    g.box, g.text = box, t
    return g


def hbars(values, names, colors, width=5.0, row_h=0.5, font_size=22, lo=None, hi=None, fmt_v=None, bar_h=0.34,
          name_w=None) -> VGroup:
    """Horizontal bars, names on the left, values on the right; ``lo``..``hi`` is the axis."""
    lo = min(values) if lo is None else lo
    hi = max(values) if hi is None else hi
    fmt_v = fmt_v or (lambda v: f"{v:.3f}")
    rows = VGroup()
    for i, (v, nm, col) in enumerate(zip(values, names, colors)):
        y = -i * row_h
        w = max((v - lo) / max(hi - lo, 1e-12) * width, 0.02)
        bar = Rectangle(width=w, height=bar_h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([w / 2, y, 0])
        t = label(nm, font_size=font_size, color=col)
        if name_w and t.width > name_w:
            t.width = name_w
        t.move_to([-0.2, y, 0], aligned_edge=RIGHT)
        val = MathTex(fmt_v(v), font_size=font_size, color=col).next_to(bar, RIGHT, buff=0.12)
        r = VGroup(t, bar, val)
        r.name, r.bar, r.val = t, bar, val
        rows.add(r)
    return rows


def expert_row(n, lit=(), size=0.32, color=EXPERTC, buff=0.08, shared=0) -> VGroup:
    """A row of ``n`` expert boxes, the ``lit`` ones filled; ``shared`` always-on ones first, in their colour."""
    boxes = VGroup()
    for i in range(shared):
        boxes.add(Square(size, stroke_color=SHAREDC, stroke_width=1.6, fill_color=SHAREDC, fill_opacity=0.85))
    for i in range(n):
        boxes.add(Square(size, stroke_color=color, stroke_width=1.2, fill_color=color,
                         fill_opacity=0.85 if i in lit else 0.06))
    return boxes.arrange(RIGHT, buff=buff)


SIG_SCORES = np.array([0.6, 0.1, -0.4, 0.3])  # illustrative router scores for four experts


def gate_picture() -> VGroup:
    """Softmax against sigmoid gates: VGroup(softmax panel, sigmoid panel), each VGroup(bars, base, name, room).
    ``gate_bars(pic, boost)`` rebuilds both panels' bars with expert 1's score raised by ``boost``: under the softmax
    the others shrink (they compete), under the sigmoid they stay put (each its own)."""
    parts = VGroup()
    for name in (r"softmax: \ they compete", r"sigmoid: \ each its own"):
        base = Line(LEFT * 0.95, RIGHT * 0.95, color=GREY_C, stroke_width=1.5)
        parts.add(VGroup(Rectangle(width=1.9, height=1.0, stroke_width=0, fill_opacity=0).next_to(base, UP, buff=0), base,
                         label(name, font_size=18, color=GREY_A).next_to(base, DOWN, buff=0.1)))
    parts.arrange(RIGHT, buff=0.7)
    bars = gate_bars(VGroup(*[VGroup(VGroup(), p_[1]) for p_ in parts]), 0.0)
    return VGroup(*[VGroup(b_, p_[1], p_[2], p_[0]) for b_, p_ in zip(bars, parts)])


def gate_bars(pic: VGroup, boost: float) -> tuple[VGroup, VGroup]:
    s = SIG_SCORES.copy()
    s[0] += boost
    soft = np.exp(s) / np.exp(s).sum()
    sig = 1 / (1 + np.exp(-s))
    out = []
    for panel, vals in zip(pic, (soft, sig)):
        base = panel[1]
        unit = base.get_length() / 2.2
        x0 = base.get_left()[0] + 0.25 * unit
        out.append(VGroup(*[Rectangle(width=0.3 * unit, height=max(1.2 * unit * float(v), 0.01), stroke_width=0,
                                      fill_color=EXPERT_COLORS[i], fill_opacity=0.9)
                            .move_to([x0 + (0.15 + 0.5 * i) * unit, base.get_y() + 0.6 * unit * float(v), 0])
                            for i, v in enumerate(vals)]))
    return tuple(out)


def card_intro(scene, k, title, question, lit=()):
    """The chapter card: 'Chapter k. Title.'"""
    card = chapter_card(k, title, question, lit=lit, part=PART)
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
             10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen"}
    return card, words[k]


def ticks_log2(ax, vals, y, font_size=20):
    return VGroup(*[MathTex(str(v), font_size=font_size, color=GREY_B).next_to(ax.c2p(math.log2(v), y), DOWN, buff=0.1)
                    for v in vals])
