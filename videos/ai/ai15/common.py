"""Helpers shared by the scenes of Part 15 ("Memory")."""

from __future__ import annotations

import numpy as np

import re

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import heat_image, signed_image  # noqa: F401

from .compute import CACHE, load  # noqa: F401

PART = 15
MONO = "DejaVu Sans Mono"
HIST = C.HUMAN  # history cards
Q, K, V, A = C.QUERY, C.KEY, C.VALUE, C.ATTN
STATE = C.EMBED  # the fixed-size memory
ADD, DECAY, DELTA = C.SURPRISE, C.TRUE_P, C.INTERVAL  # the three ways to write to it
GATED = C.BITS  # the gated delta rule
ATT = C.ATTN  # softmax attention
SSM_C = "#B39DDB"  # state-space models, Mamba
HYB = "#7FD3FF"  # hybrids
RET = C.NEURAL  # retrieval
# one colour and name per memory, for the whole part
MIX_C = {"softmax": ATT, "linear": ADD, "mamba2": SSM_C, "delta": DELTA, "gdn": GATED, "hybrid": HYB}
MIX_NAME = {"softmax": r"softmax attention", "linear": r"linear attention", "mamba2": r"Mamba-2-style SSM",
            "delta": r"delta rule", "gdn": r"gated delta rule", "hybrid": r"hybrid: \ gated delta $+$ attention"}
MIX_SHORT = {"softmax": r"softmax", "linear": r"linear", "mamba2": r"Mamba-2", "delta": r"delta", "gdn": r"gated delta",
             "hybrid": r"hybrid"}


def sci(x: float, digits: int = 0) -> str:
    """3.1e-15 as TeX: 3 \\times 10^{-15}."""
    m, e = f"{x:.{digits}e}".split("e")
    return rf"{m} \times 10^{{{int(e)}}}"


def fmt_int(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, fill=0.1, width=None) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    w = max(width or 0, t.width + 2 * pad)
    box = RoundedRectangle(width=w, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=fill)
    return VGroup(box, t.move_to(box))


def said(text: str, chars: int = 46, font_size: int = 20, max_lines: int = 3, color=WHITE, box_color=GREY_B) -> VGroup:
    """Words a model wrote (or a book): monospaced, wrapped, boxed, never translated."""
    import textwrap

    text = "".join(c if (c.isprintable() and c != "\ufffd") else "\u00b7" for c in text)  # bytes a model wrote, shown as dots
    lines = textwrap.wrap(" ".join(text.split()), chars) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: chars - 3] + "..."
    t = data_text("\n".join(lines), font=MONO, font_size=font_size, color=color, line_spacing=0.8)
    box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.32, corner_radius=0.12, stroke_color=box_color,
                           stroke_width=2, fill_color=box_color, fill_opacity=0.07)
    return VGroup(box, t.move_to(box))


def take_away(text: str, color=C.BITS, font_size=28) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    band_ = RoundedRectangle(width=min(t.width + 0.8, 13.6), height=t.height + 0.4, corner_radius=0.14,
                             stroke_width=0, fill_color=color, fill_opacity=0.10)
    return VGroup(band_, t.move_to(band_)).to_edge(DOWN, buff=0.4)


def stat(value: str, caption: str, color=WHITE, font_size=44, cap_size=20) -> VGroup:
    v = label(value, font_size=font_size, color=color)
    c = label(caption, font_size=cap_size, color=GREY_A)
    return VGroup(v, c).arrange(DOWN, buff=0.12)


def hbars(items, max_value, width=5.0, bar_h=0.34, gap=0.16, font_size=20, label_width=3.2, fmt=lambda v: f"{v:g}",
          spread=None) -> VGroup:
    """Horizontal bars: items (label TeX, value, colour); ``spread``: (lo, hi) per item, drawn as a whisker."""
    rows = VGroup()
    for i, (t, v, c_) in enumerate(items):
        y = -i * (bar_h + gap)
        nm = label(t, font_size=font_size, color=c_)
        if nm.width > label_width:
            nm.width = label_width
        nm.move_to([-0.15 - nm.width / 2, y, 0])
        w = max(width * v / max_value, 0.02)
        bar = Rectangle(width=w, height=bar_h, stroke_width=0, fill_color=c_, fill_opacity=0.85).move_to([w / 2, y, 0])
        val = MathTex(fmt(v), font_size=font_size + 2, color=c_).next_to(bar, RIGHT, buff=0.12)
        row = VGroup(nm, bar, val)
        if spread is not None:
            lo, hi = spread[i]
            wl = Line([width * lo / max_value, y, 0], [width * hi / max_value, y, 0], color=WHITE, stroke_width=2)
            row.add(wl)
            val.next_to([max(w, width * hi / max_value), y, 0], RIGHT, buff=0.12)
        row.name, row.bar, row.value = nm, bar, val
        rows.add(row)
    return rows


def curve(ax, xs, ys, color, stroke_width=3, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def gib(n_bytes: float) -> str:
    """A byte count in the unit that reads best (KiB, MiB, GiB, TiB), as TeX."""
    for unit, p in (("TiB", 40), ("GiB", 30), ("MiB", 20), ("KiB", 10)):
        if n_bytes >= 2 ** p:
            v = n_bytes / 2 ** p
            return (f"{v:,.0f}" if v >= 100 else f"{v:.1f}" if v >= 10 else f"{v:.2f}").replace(",", "{,}") + rf"\,\mathrm{{{unit}}}"
    return f"{n_bytes:.0f}" + r"\,\mathrm{B}"


def grid_matrix(M, size, color=STATE, gamma=0.6) -> VGroup:
    """A small matrix as a grid of squares, brightness by |entry|."""
    M = np.asarray(M, float)
    n, m = M.shape
    top = max(np.abs(M).max(), 1e-9)
    cell = size / max(n, m)
    g = VGroup()
    for i in range(n):
        for j in range(m):
            g.add(Square(cell, stroke_width=0.5, stroke_color=GREY_D, fill_color=color,
                         fill_opacity=float(0.08 + 0.85 * (abs(M[i, j]) / top) ** gamma))
                  .move_to([j * cell, -i * cell, 0]))
    return g.center()


def vec_column(vals, cell=0.22, color=K) -> VGroup:
    v = np.asarray(vals, float)
    top = max(np.abs(v).max(), 1e-9)
    return VGroup(*[Square(cell, stroke_width=0.6, stroke_color=GREY_D, fill_color=color,
                           fill_opacity=float(0.15 + 0.75 * abs(x) / top)) for x in v]).arrange(DOWN, buff=0)


def gqa_picture(n_q=8, groups=2) -> VGroup:
    """A jargon-card picture of grouped-query attention: VGroup(query heads, their key-value pairs, the links).  Each
    query head starts with a key and value of its own; ``gqa_shared(pic)`` is the same pairs and links once every
    group of query heads shares one pair (the group's pairs stacked into one), wherever the picture now is."""
    gap = 0.42
    qs = VGroup(*[Circle(radius=0.13, stroke_color=Q, stroke_width=2, fill_color=Q, fill_opacity=0.6) for _ in range(n_q)])
    qs.arrange(RIGHT, buff=gap - 0.26)
    per = n_q // groups
    for gi in range(1, groups):  # a little air between groups
        qs[gi * per:].shift(RIGHT * 0.25)

    def pair():
        return VGroup(Square(0.17, stroke_width=0, fill_color=K, fill_opacity=0.9),
                      Square(0.17, stroke_width=0, fill_color=V, fill_opacity=0.9)).arrange(RIGHT, buff=0.03)

    kvs = VGroup(*[pair().next_to(q_, DOWN, buff=0.75) for q_ in qs])
    links = VGroup(*[Line(q_.get_bottom(), p_.get_top(), color=GREY_B, stroke_width=1.5) for q_, p_ in zip(qs, kvs)])
    return VGroup(qs, kvs, links)


def gqa_shared(pic: VGroup, groups=2) -> VGroup:
    qs, kvs, _ = pic
    per = len(qs) // groups
    new_kv, new_links = VGroup(), VGroup()
    for i, (q_, p_) in enumerate(zip(qs, kvs)):
        gi = i // per
        x = VGroup(*qs[gi * per:(gi + 1) * per]).get_x()
        p2 = p_.copy().move_to([x, p_.get_y(), 0])
        new_kv.add(p2)
        new_links.add(Line(q_.get_bottom(), p2.get_top(), color=GREY_B, stroke_width=1.5))
    return VGroup(new_kv, new_links)


def ttt_picture(seed=0) -> VGroup:
    """A jargon-card picture of test-time training: VGroup(the text streaming in, an arrow, the memory as a small
    network's weights, its name).  ``ttt_step(pic, k)`` is the weights after reading the k-th token: they change as
    the model reads."""
    toks = VGroup(*[Square(0.2, stroke_width=1, stroke_color=GREY_B, fill_color=C.TOKEN, fill_opacity=0.25) for _ in range(6)])
    toks.arrange(RIGHT, buff=0.06)
    arrow = Arrow(LEFT * 0.35, RIGHT * 0.35, buff=0, color=GREY_B, stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
    w = _ttt_weights(seed)
    net = VGroup(w, label(r"the memory: \\ a network's weights", font_size=18, color=STATE).next_to(w, DOWN, buff=0.1))
    return VGroup(toks, arrow, net).arrange(RIGHT, buff=0.25)


def _ttt_weights(seed):
    g = np.random.default_rng(100 + seed)
    return VGroup(*[Square(0.17, stroke_width=0.6, stroke_color=GREY_D, fill_color=STATE, fill_opacity=float(o))
                    for o in g.uniform(0.1, 0.95, 24)]).arrange_in_grid(4, 6, buff=0.02)


def ttt_step(pic: VGroup, k: int) -> tuple[VGroup, VGroup]:
    """(the weights after token k, the tokens with the first k read), rebuilt where the picture now is."""
    toks, _, net = pic
    w = _ttt_weights(k).replace(net[0])
    t2 = toks.copy()
    for i, t_ in enumerate(t2):
        t_.set_fill(C.BITS if i < k else C.TOKEN, opacity=0.85 if i == k - 1 else 0.5 if i < k else 0.25)
    return w, t2


def signed_grid(M, size, top=None, pos=C.TRUE_P, neg=C.SURPRISE) -> VGroup:
    """A small signed matrix as squares: blue for positive, red for negative, brightness by size, on a common
    scale ``top`` (so the steps of an animation compare)."""
    M = np.asarray(M, float)
    n, m = M.shape
    top = top or max(float(np.abs(M).max()), 1e-9)
    cell = size / max(n, m)
    g = VGroup()
    for i in range(n):
        for j in range(m):
            x = float(np.clip(M[i, j] / top, -1, 1))
            g.add(Square(cell, stroke_width=0.5, stroke_color=GREY_D, fill_color=pos if x >= 0 else neg,
                         fill_opacity=0.06 + 0.88 * abs(x) ** 0.7).move_to([j * cell, -i * cell, 0]))
    return g.center()


def signed_column(v, cell=0.24, top=None, pos=C.TRUE_P, neg=C.SURPRISE) -> VGroup:
    return signed_grid(np.asarray(v, float)[:, None], cell * len(v), top, pos, neg)


def bits_grid(x, side=10, size=2.4, on=WHITE, off="#1B2230") -> VGroup:
    """A +1/-1 pattern as a side x side picture of squares."""
    cell = size / side
    g = VGroup()
    for i in range(side):
        for j in range(side):
            g.add(Square(cell * 0.94, stroke_width=0, fill_color=on if x[i * side + j] > 0 else off, fill_opacity=1)
                  .move_to([j * cell, -i * cell, 0]))
    return g.center()


def heat_fixed(M, width, height, color, vmax=1.0, gamma=0.6) -> ImageMobject:
    """A matrix as a picture on a fixed scale: dark for 0, ``color`` at ``vmax`` (so small values look small)."""
    M = np.asarray(M, float)
    v = np.clip(M / vmax, 0, 1) ** gamma
    c = np.array(ManimColor(color).to_rgb())
    bg = np.array(ManimColor("#121722").to_rgb())
    rgb = bg[None, None] * (1 - v[..., None]) + c[None, None] * v[..., None]
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)
