"""Helpers shared by the scenes of Part 23 ("Optimization")."""

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

PART = 23

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


class View3:
    """A hand-rolled 3D projection driven by ValueTrackers (azimuth ``th``, elevation ``ph``), as in Part 22's lifting
    map, so polytopes can be redrawn with always_redraw while the camera turns."""

    def __init__(self, origin=ORIGIN, scale=1.0, th=-0.6, ph=0.45, center=(0, 0, 0)):
        self.th = ValueTracker(th)
        self.ph = ValueTracker(ph)
        self.o = np.array(origin, dtype=float)
        self.s = scale
        self.c = np.array(center, dtype=float)

    def p(self, x, y=None, z=None):
        if y is None:
            x, y, z = x
        x, y, z = x - self.c[0], y - self.c[1], z - self.c[2]
        a, e = self.th.get_value(), self.ph.get_value()
        x1 = x * math.cos(a) - y * math.sin(a)
        y1 = x * math.sin(a) + y * math.cos(a)
        return self.o + self.s * np.array([x1, z * math.cos(e) + y1 * math.sin(e), 0.0])

    def depth(self, x, y, z):
        x, y, z = x - self.c[0], y - self.c[1], z - self.c[2]
        a, e = self.th.get_value(), self.ph.get_value()
        y1 = x * math.sin(a) + y * math.cos(a)
        return y1 * math.cos(e) - z * math.sin(e)

    def polytope(self, V, faces, color=DATA, opacity=0.18, edge_color=None, width=2.0):
        """Faces (triangles of a hull) drawn back to front; edges shared by coplanar triangles are hidden."""
        V = [tuple(v) for v in V]
        Vn = np.array(V)
        normals = []
        for f in faces:
            a, b, c = Vn[f[0]], Vn[f[1]], Vn[f[2]]
            nrm = np.cross(b - a, c - a)
            nrm = nrm / (np.linalg.norm(nrm) + 1e-12)
            normals.append(nrm)
        edges = {}
        for k, f in enumerate(faces):
            for u, v in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2])):
                edges.setdefault((min(u, v), max(u, v)), []).append(k)
        order = sorted(range(len(faces)), key=lambda k: -np.mean([self.depth(*V[i]) for i in faces[k]]))
        g = VGroup()
        for k in order:
            g.add(Polygon(*[self.p(V[i]) for i in faces[k]], stroke_width=0).set_fill(color, opacity))
        for (u, v), ks in edges.items():
            if len(ks) == 2 and abs(abs(np.dot(normals[ks[0]], normals[ks[1]])) - 1) < 1e-6:
                continue
            g.add(Line(self.p(V[u]), self.p(V[v]), color=edge_color or color, stroke_width=width))
        return g

    def axes(self, L=3.0, color=GREY_D):
        g = VGroup()
        for d, nm in ((np.array([L, 0, 0]), "x_1"), (np.array([0, L, 0]), "x_2"), (np.array([0, 0, L]), "x_3")):
            g.add(Arrow(self.p(0, 0, 0), self.p(*d), buff=0, color=color, stroke_width=2,
                        max_tip_length_to_length_ratio=0.06))
            g.add(MathTex(nm, font_size=24, color=GREY_B).move_to(self.p(*(d * 1.08))))
        return g
