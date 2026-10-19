"""Helpers shared by the scenes of Part 14 ("The Language-Model Lineage")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14 import facts as F  # noqa: F401

from .compute import load  # noqa: F401

PART = 14
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
DECODER = "#FF9F45"  # decoder-only, causal, GPT-style: the lineage that won
ENCODER = "#B39DDB"  # encoder-only, masked, BERT-style (sees context on both sides)
ENCDEC = "#5CD0B3"  # encoder-decoder: the 2017 translation Transformer, T5
OPEN = "#5BD17A"  # open weights
CLOSED = "#FF6B8B"  # closed models
N_COL = C.PARAMS  # N, parameters
D_COL = C.DATA  # D, training tokens
C_COL = C.COMPUTE  # C, training compute
HUMAN = C.HUMAN  # human baselines
PRIOR = GREY_B  # earlier systems, prior state of the art
CONTEXT = C.CONTEXT  # in-context examples
ARCH_COLOR = {"decoder": DECODER, "encoder": ENCODER, "encdec": ENCDEC}
SIZE_COLORS = ["#FFE3BF", "#FFC27A", "#FF9F45", "#E8590C", "#B83A06"]  # our family, smallest to the base model

COLORS = {r"N": N_COL, r"D": D_COL, r"C": C_COL}


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------
def human(x: float, digits: int = 3) -> str:
    """175e9 -> '175B', 1.4e12 -> '1.4T', 65e6 -> '65M', 274080 -> '274k' (plain text, for labels)."""
    for unit, v in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if abs(x) >= v:
            y = x / v
            nd = max(0, digits - len(str(int(abs(y)))))
            s = f"{y:.{nd}f}"
            if "." in s:
                s = s.rstrip("0").rstrip(".")
            return s + unit
    return f"{x:g}"


def sci_tex(x: float, digits: int = 1) -> str:
    """3.14e23 -> '3.1 \\times 10^{23}' (MathTex)."""
    return sci(x, digits)


def month_year(d: str) -> str:
    y, m, _ = d.split("-")
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(m) - 1] + " " + y


def year_of(d: str) -> float:
    y, m, dd = (int(x) for x in d.split("-"))
    return y + (m - 1) / 12 + (dd - 1) / 365.25


# ---------------------------------------------------------------------------
# Small drawing helpers
# ---------------------------------------------------------------------------
def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, fill=0.1) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=fill)
    return VGroup(box, t.move_to(box))


def chip(text: str, color=GREY_B, font_size=22, height=0.46, fill=0.12, mono=True) -> VGroup:
    """A token in a rounded box (monospaced data text, never translated)."""
    t = data_text(text, font=MONO, font_size=font_size, color=WHITE) if mono else label(text, font_size=font_size)
    box = RoundedRectangle(width=max(t.width + 0.22, height), height=height, corner_radius=0.08, stroke_color=color,
                           stroke_width=1.8, fill_color=color, fill_opacity=fill)
    return VGroup(box, t.move_to(box))


def token_row(tokens, colors=None, font_size=22, buff=0.06) -> VGroup:
    colors = colors or [GREY_B] * len(tokens)
    return VGroup(*[chip(t, c, font_size=font_size) for t, c in zip(tokens, colors)]).arrange(RIGHT, buff=buff)


def said(text: str, chars: int = 46, font_size: int = 20, max_lines: int = 3, color=WHITE, box_color=GREY_B) -> VGroup:
    """Words a model (or a book) wrote: monospaced, wrapped, boxed, never translated."""
    import textwrap

    lines = textwrap.wrap(" ".join(text.split()), chars) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: chars - 3] + "..."
    t = data_text("\n".join(lines), font=MONO, font_size=font_size, color=color, line_spacing=0.8)
    box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.32, corner_radius=0.12, stroke_color=box_color,
                           stroke_width=2, fill_color=box_color, fill_opacity=0.07)
    return VGroup(box, t.move_to(box))


def stat(value: str, caption: str, color=WHITE, font_size=44, cap_size=20) -> VGroup:
    """A big number with a small caption under it."""
    v = label(value, font_size=font_size, color=color)
    c = label(caption, font_size=cap_size, color=GREY_A)
    return VGroup(v, c).arrange(DOWN, buff=0.12)


def bars_h(items, max_value, width=6.0, bar_h=0.34, gap=0.14, font_size=20, label_width=3.0, log=False,
           fmt=lambda v: f"{v:g}", lo=None):
    """Horizontal bars: (name, value, colour) rows; returns a VGroup of rows, each (name, bar, value)."""
    rows = VGroup()
    for i, (name, v, col) in enumerate(items):
        if log:
            lo_ = lo if lo is not None else 0.0
            w = max(width * (math.log10(v) - lo_) / (math.log10(max_value) - lo_), 0.02)
        else:
            w = max(width * v / max_value, 0.02)
        nm = label(name, font_size=font_size, color=GREY_A)
        if nm.width > label_width:
            nm.width = label_width
        bar = Rectangle(width=w, height=bar_h, stroke_width=0, fill_color=col, fill_opacity=0.9)
        y = -i * (bar_h + gap)
        bar.move_to([w / 2, y, 0])
        nm.move_to([-0.2 - nm.width / 2, y, 0])
        val = MathTex(fmt(v), font_size=font_size + 2, color=col).next_to(bar, RIGHT, buff=0.12)
        rows.add(VGroup(nm, bar, val))
    return rows


def arch_diagram(kind: str, scale: float = 1.0, label_on=True) -> VGroup:
    """A stack of blocks: 'encdec' (two stacks joined by cross-attention), 'encoder' or 'decoder'.  Arrows show what
    each position may look at: both ways (encoder) or only back (decoder).  schematic."""
    col = ARCH_COLOR[kind]

    def stack(color, n=3, w=1.5, h=0.42):
        g = VGroup(*[RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=2,
                                      fill_color=color, fill_opacity=0.18) for _ in range(n)])
        return g.arrange(UP, buff=0.12)

    g = VGroup()
    if kind == "encdec":
        enc, dec = stack(ENCODER), stack(DECODER)
        VGroup(enc, dec).arrange(RIGHT, buff=0.9)
        cross = VGroup(*[Arrow(enc[-1].get_right(), d.get_left(), buff=0.06, stroke_width=2, color=ENCDEC,
                               max_tip_length_to_length_ratio=0.15) for d in dec])
        g.add(enc, dec, cross)
        if label_on:
            g.add(label(r"encoder", font_size=18, color=ENCODER).next_to(enc, DOWN, buff=0.15),
                  label(r"decoder", font_size=18, color=DECODER).next_to(dec, DOWN, buff=0.15))
    else:
        s = stack(col)
        g.add(s)
        # five positions underneath, with the attention pattern of the last one
        dots = VGroup(*[Dot(radius=0.06, color=GREY_B) for _ in range(5)]).arrange(RIGHT, buff=0.24)
        dots.next_to(s, DOWN, buff=0.3)
        tgt = dots[2]
        arcs = VGroup()
        for j, d_ in enumerate(dots):
            if j == 2 or (kind == "decoder" and j > 2):
                continue
            arcs.add(ArcBetweenPoints(d_.get_top() + UP * 0.02, tgt.get_top() + UP * 0.02, angle=-PI / 2.2,
                                      color=col, stroke_width=2))
        g.add(dots, arcs)
        if label_on:
            g.add(label(r"looks both ways" if kind == "encoder" else r"looks back only", font_size=18,
                        color=col).next_to(dots, DOWN, buff=0.15))
    return g.scale(scale)


def config_card(c: dict, width=4.6, font_size=22, rows=("layers", "d", "heads", "ctx", "params", "tokens"),
                color=None) -> VGroup:
    """A model's published configuration as a card: name and date, then one row per field.  The rows keep their
    order and length from model to model, so one card can Transform into the next."""
    color = color or ARCH_COLOR.get(c["arch"], WHITE)
    names = {"layers": r"layers", "d": r"width $d$", "heads": r"heads", "ctx": r"context", "params": r"parameters",
             "tokens": r"training tokens", "active": r"active per token"}

    def val(k):
        v = c.get(k)
        if v is None:
            return r"--"
        if k == "layers" and c.get("layers_note"):
            return c["layers_note"]
        if k in ("params", "tokens", "active"):
            return human(v)
        if k == "ctx":
            return f"{v:,}".replace(",", "{,}")
        if k == "heads" and c.get("kv_heads") not in (None, c.get("heads")):
            return rf"{v}\ /\ {c['kv_heads']}\,\text{{kv}}"
        return f"{v:,}".replace(",", "{,}")

    head = VGroup(label(c["name"], font_size=font_size + 8, color=color),
                  label(month_year(c["date"]), font_size=font_size - 2, color=GREY_B)).arrange(DOWN, buff=0.08)
    body = VGroup()
    for k in rows:
        nm = label(names[k], font_size=font_size, color=GREY_A)
        v = MathTex(val(k), font_size=font_size + 4, color=WHITE)
        body.add(VGroup(nm, v))
    for r in body:
        r[0].move_to(ORIGIN, aligned_edge=LEFT)
        r[1].move_to([width - 0.7, 0, 0], aligned_edge=RIGHT)
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    for r in body:
        r[1].align_to(body, RIGHT)
    inner = VGroup(head, body).arrange(DOWN, buff=0.3)
    box = RoundedRectangle(width=width, height=inner.height + 0.5, corner_radius=0.16, stroke_color=color,
                           stroke_width=2.2, fill_color="#0B0F17", fill_opacity=0.95)
    g = VGroup(box, inner.move_to(box))
    g.box, g.head, g.body = box, head, body
    return g


def log_axes(x_range, y_range, x_length=10.0, y_length=5.0, xlabel="", ylabel="", center=ORIGIN, font_size=20,
             xticks=None, yticks=None, xfmt=None) -> VGroup:
    """Axes with a log10 y (y_range in powers of ten) and years on x."""
    return axes(x_range, y_range, x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel,
                xticks=xticks, yticks=yticks, xfmt=xfmt or (lambda v: f"{int(v)}"),
                yfmt=lambda v: rf"10^{{{int(v)}}}", font_size=font_size, center=center)


def take_away(text: str, color=C.BITS, font_size=30) -> VGroup:
    """The chapter's takeaway: a line of text in a soft band at the bottom of the frame."""
    t = label(text, font_size=font_size, color=color)
    band_ = RoundedRectangle(width=min(t.width + 0.8, 13.6), height=t.height + 0.4, corner_radius=0.14,
                             stroke_width=0, fill_color=color, fill_opacity=0.10)
    return VGroup(band_, t.move_to(band_)).to_edge(DOWN, buff=0.35)
