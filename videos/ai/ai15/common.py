"""Helpers shared by the scenes of Part 15 ("Memory")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
Q, K, V, A = C.QUERY, C.KEY, C.VALUE, C.ATTN
STATE = C.EMBED  # the fixed-size memory
ADD, DECAY, DELTA = C.SURPRISE, C.TRUE_P, C.INTERVAL  # the three ways to write to it


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
