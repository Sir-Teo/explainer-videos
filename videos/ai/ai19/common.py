"""Helpers shared by the scenes of Part 19 ("Inference")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401
from . import facts as F  # noqa: F401

PART = 19
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
FLOPC = C.COMPUTE  # arithmetic: FLOPs, the flat roof
BYTEC = C.DRAM  # memory: bytes moved, bandwidth
WEIGHTC = C.WEIGHTS  # the weights
KVC = C.KEY  # the key-value cache
PREFILLC = C.MODEL_Q  # prefill: the prompt read at once
DECODEC = C.TRUE_P  # decode: one token at a time
TARGETC = C.NEURAL  # the big model, p
DRAFTC = GREY_B  # the draft, q
EAGLEC = C.LATENT  # the EAGLE head
ACCEPTC = C.INTERVAL  # accepted
REJECTC = C.SURPRISE  # rejected, errors
LEVELC = C.BITS  # quantization levels, scales
ERRC = C.SURPRISE  # rounding error
RTNC = GREY_B  # round to nearest
GPTQC = C.PROB  # GPTQ
AWQC = C.HOT  # AWQ
SMOOTHC = C.EMBED  # SmoothQuant
ROTC = C.ENTROPY  # rotations (QuaRot)
LEARNC = C.RATIO  # learned rotations (SpinQuant)
STATICC, CONTC, CHUNKC, DISC = GREY_B, C.PROB, C.EMBED, C.ENTROPY  # batching policies
RESERVEC, CONTIGC, PAGEDC = C.SURPRISE, C.HOT, C.PROB  # memory policies
SIGNC, EXPC, MANC = C.SIGN_BIT, C.EXP_BIT, C.MAN_BIT  # bits of a float
COSTC = C.SCORE  # money
QUERYC, KEYC, VALUEC, ATTNC = C.QUERY, C.KEY, C.VALUE, C.ATTN

COLORS = {r"\alpha": ACCEPTC, r"p": TARGETC, r"q": DRAFTC, r"\Delta": LEVELC, r"H": C.MLP, r"B": DECODEC,
          r"\beta": BYTEC, r"P": FLOPC}


# ---------------------------------------------------------------------------
# Numbers as text
# ---------------------------------------------------------------------------
def fmt(x: float, digits: int = 2) -> str:
    """A number with sensible significant digits for narration and labels."""
    if x == 0:
        return "0"
    a = abs(x)
    if a >= 100:
        return f"{x:,.0f}"
    if a >= 10:
        return f"{x:.0f}" if digits <= 2 else f"{x:.1f}"
    if a >= 1:
        return f"{x:.1f}" if digits <= 2 else f"{x:.2f}"
    return f"{x:.{max(digits, int(-math.floor(math.log10(a))) + 1)}f}"


def tex_num(x: float, digits: int = 2) -> str:
    return fmt(x, digits).replace(",", "{,}")


def human_bytes(b: float) -> str:
    """Bytes as kB / MB / GB / TB text (decimal units), for labels."""
    for unit, k in (("TB", 1e12), ("GB", 1e9), ("MB", 1e6), ("kB", 1e3)):
        if b >= k:
            v = b / k
            return f"{v:.0f} {unit}" if v >= 10 else f"{v:.1f} {unit}"
    return f"{b:.0f} bytes"


def spoken_bytes(b: float) -> str:
    """Bytes for the narrator: '320 kilobytes', '1.3 gigabytes'."""
    for unit, k in (("terabytes", 1e12), ("gigabytes", 1e9), ("megabytes", 1e6), ("kilobytes", 1e3)):
        if b >= k:
            v = b / k
            return f"{v:.0f} {unit}" if v >= 10 else f"{v:.1f} {unit}"
    return f"{b:.0f} bytes"


def times(r: float) -> str:
    """A ratio for the narrator: '3.4 times', '12 times'."""
    return f"{r:.0f} times" if r >= 10 else f"{r:.1f} times"


# ---------------------------------------------------------------------------
# Boxes, chips, bars
# ---------------------------------------------------------------------------
def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, fill=0.1) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=fill)
    g = VGroup(box, t.move_to(box))
    g.box, g.text = box, t
    return g


def chip(text: str, size=0.46, color=GREY_B, font_size=24, fill=0.12, width=None) -> VGroup:
    """A token as a small box with its text (data: never translated)."""
    t = data_text(text, font=MONO, font_size=font_size, color=WHITE)
    w = width or max(size, t.width + 0.16)
    box = RoundedRectangle(width=w, height=size, corner_radius=0.06, stroke_color=color, stroke_width=1.8,
                           fill_color=color, fill_opacity=fill)
    return VGroup(box, t.move_to(box))


def token_chips(tokens, color=GREY_B, font_size=22, size=0.44, buff=0.06) -> VGroup:
    """A row of token chips; spaces shown as a middle dot."""
    g = VGroup(*[chip(t.replace(" ", "·").replace("\n", "↵"), size=size, color=color,
                      font_size=font_size) for t in tokens])
    return g.arrange(RIGHT, buff=buff)


def hbars(values, names, colors, width=5.0, row_h=0.46, font_size=22, lo=None, hi=None, fmt_v=None, name_w=None,
          bar_h=0.32) -> VGroup:
    """Horizontal bars, one per value, names on the left (Tex), values on the right; ``lo``..``hi`` is the axis."""
    lo = min(values) if lo is None else lo
    hi = max(values) if hi is None else hi
    fmt_v = fmt_v or (lambda v: f"{v:.3f}")
    rows = VGroup()
    for i, (v, nm, col) in enumerate(zip(values, names, colors)):
        y = -i * row_h
        w = max((v - lo) / max(hi - lo, 1e-12) * width, 0.02)
        bar = Rectangle(width=w, height=bar_h, stroke_width=0, fill_color=col, fill_opacity=0.85)
        bar.move_to([w / 2, y, 0])
        t = label(nm, font_size=font_size, color=col)
        if name_w and t.width > name_w:
            t.width = name_w
        t.move_to([-0.2, y, 0], aligned_edge=RIGHT)
        val = MathTex(fmt_v(v), font_size=font_size, color=col).next_to(bar, RIGHT, buff=0.12)
        r = VGroup(t, bar, val)
        r.name, r.bar, r.val = t, bar, val
        rows.add(r)
    return rows


def loglog(x_range, y_range, x_length=7.0, y_length=4.4, xlabel="", ylabel="", center=ORIGIN, font_size=20,
           xstep=1, ystep=1, xfmt=None, yfmt=None) -> VGroup:
    """Axes for log10 x and log10 y (ranges given as exponents), ticks at powers of ten."""
    def pow10(v):
        v = int(round(v))
        return {0: "1", 1: "10", 2: "100", 3: r"1{,}000", -1: "0.1", -2: "0.01"}.get(v, rf"10^{{{v}}}")

    xt = list(range(int(math.ceil(x_range[0])), int(math.floor(x_range[1])) + 1, xstep))
    yt = list(range(int(math.ceil(y_range[0])), int(math.floor(y_range[1])) + 1, ystep))
    return axes(x_range, y_range, x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel, xticks=xt,
                yticks=yt, xfmt=xfmt or pow10, yfmt=yfmt or pow10, font_size=font_size, center=center)


def bit_cells(bits: str, colors, cell=0.3, font_size=18) -> VGroup:
    """A bit string as boxes, coloured field by field (``colors`` one per bit)."""
    g = VGroup()
    for b, col in zip(bits, colors):
        sq = Rectangle(width=cell, height=cell * 1.2, stroke_color=col, stroke_width=1.4, fill_color=col,
                       fill_opacity=0.3)
        g.add(VGroup(sq, data_text(b, font=MONO, font_size=font_size, color=WHITE).move_to(sq)))
    return g.arrange(RIGHT, buff=0.0)


def take_away(text: str, color=WHITE, font_size=26) -> VGroup:
    """The chapter's takeaway: a line in a thin box, at the bottom of the frame."""
    t = label(text, font_size=font_size, color=color)
    if t.width > 12.4:
        t.width = 12.4
    box = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.3, corner_radius=0.12, stroke_color=color,
                           stroke_width=1.5, fill_color="#0B0F17", fill_opacity=0.9)
    return VGroup(box, t.move_to(box)).to_edge(DOWN, buff=0.3)
