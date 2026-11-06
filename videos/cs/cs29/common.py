"""Helpers shared by the scenes of Part 29 ("Secrets")."""

from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code, region  # noqa: F401
from videos.cs.cs16.common import big, value_bars, words  # noqa: F401

from .compute import load  # noqa: F401

PART = 29

DATA = C.CS_DATA
CTRL = C.CS_CONTROL
HEAD = C.CS_HEAD
CODE = C.CS_CODE
FUNC = C.CS_FUNC
COST = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
BG = "#121722"
LAM = "#9b8cd6"


def slots(occupied, w=0.26, h=0.42, color=DATA, empty=GREY_D):
    """A hash table as a row of slots, filled ones coloured; ``.cells``."""
    g = VGroup(*[Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=1.0,
                           fill_color=color if o else BG, fill_opacity=0.9 if o else 1.0) for o in occupied])
    g.arrange(RIGHT, buff=0.02)
    g.cells = g
    return g


def tree_layout(root_key, children, x0=0.0, dx=6.4, dy=0.9):
    """Positions for a binary tree given as {key: (left, right)}: in-order x, depth y."""
    pos, order = {}, []

    def walk(k, d):
        if k is None:
            return
        l, r = children.get(k, (None, None))
        walk(l, d + 1)
        order.append((k, d))
        walk(r, d + 1)
    walk(root_key, 0)
    n = len(order)
    for i, (k, d) in enumerate(order):
        pos[k] = np.array([x0 - dx / 2 + dx * (i + 0.5) / n, -d * dy, 0.0])
    return pos


def draw_tree(root_key, children, color=DATA, r=0.24, font=18, dx=6.4, dy=0.9, highlight=()):
    """A binary tree of labelled circles; returns (group, {key: node}, edges)."""
    pos = tree_layout(root_key, children, dx=dx, dy=dy)
    nodes, edges = {}, VGroup()
    for k, p in pos.items():
        c = Circle(radius=r, stroke_color=HEAD if k in highlight else color, stroke_width=2,
                   fill_color=BG, fill_opacity=1).move_to(p)
        t = mono(str(k), font, WHITE).move_to(p)
        nodes[k] = VGroup(c, t)
    for k, (l, rr) in children.items():
        for ch in (l, rr):
            if ch is not None and ch in pos and k in pos:
                edges.add(Line(pos[k], pos[ch], buff=r, color=GREY_B, stroke_width=1.6))
    g = VGroup(edges, *nodes.values())
    return g, nodes, edges


def bst_children(keys):
    """Insert keys into a plain BST; return (root, {key: (left, right)})."""
    root, ch = None, {}
    for k in keys:
        if root is None:
            root = k
            ch[k] = (None, None)
            continue
        n = root
        while True:
            l, r = ch[n]
            if k < n:
                if l is None:
                    ch[n] = (k, r)
                    break
                n = l
            else:
                if r is None:
                    ch[n] = (l, k)
                    break
                n = r
        ch[k] = (None, None)
    return root, ch


def gnode(label_, pos, color=DATA, r=0.26, font=18):
    c = Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(pos)
    return VGroup(c, mono(str(label_), font, WHITE).move_to(pos))


def draw_graph(pos, edges, directed=False, color=DATA, r=0.26, font=18, weights=None, edge_color=GREY_B):
    """Nodes at ``pos`` {name: (x, y)}; ``edges`` [(a, b)]; returns (group, nodes, edge dict)."""
    nodes = {k: gnode(k, [x, y, 0], color, r, font) for k, (x, y) in pos.items()}
    es = {}
    for a, b in edges:
        pa, pb = np.array([*pos[a], 0.0]), np.array([*pos[b], 0.0])
        if directed:
            e = Arrow(pa, pb, buff=r, stroke_width=2, color=edge_color, max_tip_length_to_length_ratio=0.12)
        else:
            e = Line(pa, pb, buff=r, stroke_width=2, color=edge_color)
        es[(a, b)] = e
    g = VGroup(*es.values(), *nodes.values())
    if weights:
        wl = VGroup()
        for (a, b), w in weights.items():
            mid = (np.array([*pos[a], 0.0]) + np.array([*pos[b], 0.0])) / 2
            wl.add(mono(str(w), font - 3, HEAD).move_to(mid + UP * 0.18))
        g.add(wl)
        g.weights = wl
    return g, nodes, es


def fit(P, center=ORIGIN, w=6.0, h=4.0):
    """Map data points into a w x h screen box centred at ``center``, keeping the aspect ratio.  Returns f(p) -> point
    and the scale."""
    P = np.asarray(P, dtype=float)
    lo, hi = P.min(0), P.max(0)
    span = np.maximum(hi - lo, 1e-9)
    s = min(w / span[0], h / span[1])
    c = (lo + hi) / 2
    cx, cy = float(center[0]), float(center[1])

    def f(p):
        return np.array([cx + (p[0] - c[0]) * s, cy + (p[1] - c[1]) * s, 0.0])
    return f, s


def dots(P, f, color=DATA, r=0.05):
    return VGroup(*[Dot(f(p), radius=r, color=color) for p in P])


def poly_mob(P, f, color=DATA, width=2.5, fill=None, opacity=0.0):
    m = Polygon(*[f(p) for p in P], color=color, stroke_width=width)
    if fill is not None:
        m.set_fill(fill, opacity)
    return m


def cells_row(values, w=0.5, h=0.5, color=DATA, font=20, fill=0.0, labels=True):
    """An array drawn as a row of boxes with its values; ``.boxes``, ``.vals``."""
    boxes = VGroup(*[Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=1.2).set_fill(color, fill)
                     for _ in values]).arrange(RIGHT, buff=0)
    vals = VGroup(*[mono(str(v), font, WHITE).move_to(b) for v, b in zip(values, boxes)])
    g = VGroup(boxes, vals)
    g.boxes, g.vals = boxes, vals
    if labels:
        idx = VGroup(*[mono(str(i), 14, GREY_C).next_to(b, DOWN, buff=0.06) for i, b in enumerate(boxes)])
        g.add(idx)
        g.idx = idx
    return g


def log_axes(x_range, y_range, x_length=6.0, y_length=3.6, x_label=None, y_label=None):
    """Axes whose coordinates are log10 values, with labels 10^k (both axes)."""
    ax = Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
              axis_config={"color": GREY_D, "include_numbers": False})
    xt = VGroup(*[MathTex(rf"10^{{{int(k)}}}", font_size=18, color=GREY_B).next_to(ax.c2p(k, y_range[0]), DOWN,
                                                                               buff=0.12)
                  for k in np.arange(x_range[0], x_range[1] + 1e-9, x_range[2])])
    yt = VGroup(*[MathTex(rf"10^{{{int(k)}}}", font_size=18, color=GREY_B).next_to(ax.c2p(x_range[0], k), LEFT,
                                                                               buff=0.12)
                  for k in np.arange(y_range[0], y_range[1] + 1e-9, y_range[2])])
    g = VGroup(ax, xt, yt)
    if x_label:
        g.add(label(x_label, font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.12))
    if y_label:
        g.add(label(y_label, font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT))
    g.ax = ax
    return g


def curve(ax, xs, ys, color, width=3.0, dots=True):
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys)]
    g = VGroup(VMobject(color=color, stroke_width=width).set_points_as_corners(pts))
    if dots:
        g.add(*[Dot(p, radius=0.04, color=color) for p in pts])
    return g


def fit_right(m, right=6.9):
    """Shrink ``m`` (keeping its left edge) so that it ends at ``right``."""
    left = m.get_left()[0]
    if m.get_right()[0] > right:
        m.width = right - left
        m.shift(RIGHT * (left - m.get_left()[0]))
    return m


def qr_grid(matrix, side=4.6, light="#e8e8e8", dark="#121212"):
    """A QR matrix as squares on a light quiet zone; ``.cells[y][x]``."""
    n = len(matrix)
    s = side / (n + 4)
    zone = Square(side_length=side, stroke_width=0, fill_color=light, fill_opacity=1)
    cells = []
    g = VGroup(zone)
    for y in range(n):
        row = []
        for x in range(n):
            col = dark if matrix[y][x] else light
            sq = Square(side_length=s, stroke_width=1.2, stroke_color=col, fill_color=col, fill_opacity=1)
            sq.move_to(zone.get_corner(UL) + RIGHT * s * (x + 2.5) + DOWN * s * (y + 2.5))
            row.append(sq)
            g.add(sq)
        cells.append(row)
    g.cells = cells
    g.step = s
    return g


def bit_row(bits, size=0.42, on=DATA, off=BG, font=22, labels=None):
    """Bits as boxed digits; ``.boxes``, ``.digits``."""
    boxes = VGroup(*[Square(side_length=size, stroke_color=GREY_B, stroke_width=1.5,
                            fill_color=on if b else off, fill_opacity=0.35 if b else 1) for b in bits])
    boxes.arrange(RIGHT, buff=0.05)
    digits = VGroup(*[mono(str(b), font, WHITE).move_to(bx) for b, bx in zip(bits, boxes)])
    g = VGroup(boxes, digits)
    g.boxes, g.digits = boxes, digits
    if labels:
        g.labels = VGroup(*[label(t, font_size=14, color=GREY_A).next_to(bx, UP, buff=0.06)
                            for t, bx in zip(labels, boxes)])
        g.add(g.labels)
    return g



def state_grid(hexs, cell=0.52, font=17, color=DATA, fill=0.18):
    """The AES state: 16 bytes in a 4 x 4 grid, column by column; ``.cells[r][c]``, ``.vals[r][c]``."""
    b = bytes.fromhex(hexs) if isinstance(hexs, str) else bytes(hexs)
    cells = [[None] * 4 for _ in range(4)]
    vals = [[None] * 4 for _ in range(4)]
    g = VGroup()
    for c in range(4):
        for r in range(4):
            sq = Square(side_length=cell, stroke_color=GREY_B, stroke_width=1.2, fill_color=color,
                        fill_opacity=fill).move_to([c * cell, -r * cell, 0])
            t = mono(f"{b[4 * c + r]:02x}", font, WHITE).move_to(sq)
            cells[r][c], vals[r][c] = sq, t
            g.add(sq, t)
    g.center()
    g.cells, g.vals = cells, vals
    return g


def pixel_image(vals, w, h, height=3.0):
    """Grey bytes as an image, scaled up without smoothing."""
    a = np.array(vals, dtype=np.uint8).reshape(h, w)
    img = ImageMobject(np.stack([a, a, a, np.full_like(a, 255)], axis=-1))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.height = height
    return img


def letter_bars(freq, width=5.6, height=2.0, color=DATA, top=0.14, font=13):
    """26 bars, A to Z, of letter frequencies; ``.bars``, ``.letters``."""
    A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    bw = width / 26
    bars = VGroup(*[Rectangle(width=bw * 0.78, height=max(height * freq.get(c, 0) / top, 0.01), stroke_width=0,
                              fill_color=color, fill_opacity=0.9) for c in A])
    for i, b in enumerate(bars):
        b.move_to([-width / 2 + bw * (i + 0.5), 0, 0], aligned_edge=DOWN)
    letters = VGroup(*[mono(c, font, GREY_A).move_to([-width / 2 + bw * (i + 0.5), -0.15, 0]) for i, c in enumerate(A)])
    base = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=GREY_D, stroke_width=1.5)
    g = VGroup(base, bars, letters)
    g.bars, g.letters = bars, letters
    return g


def flow_box(text, color=DATA, w=1.5, h=0.7, font=20):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, label(text, font_size=font, color=WHITE).move_to(r))


def block_image(vals, w, h, height=3.0):
    """Ciphertext drawn block by block: each 16-byte block painted in the colour given by its own first three bytes,
    so equal blocks show as equal colours."""
    a = np.array(vals, dtype=np.uint8).reshape(h, w)
    rgb = np.zeros((h, w, 4), dtype=np.uint8)
    rgb[..., 3] = 255
    for r in range(h):
        for j in range(0, w, 16):
            rgb[r, j:j + 16, :3] = a[r, j:j + 3]
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.height = height
    return img
