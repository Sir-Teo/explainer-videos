"""Helpers shared by the scenes of Part 14 ("Changing Your Mind")."""

from __future__ import annotations

import re

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import argue as G  # noqa: F401
from explainer.philosophy.reasoner import cond as C  # noqa: F401
from explainer.philosophy.reasoner import revision as R  # noqa: F401

from .compute import load  # noqa: F401

PART = 14
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
BEL = "#FFD166"       # current beliefs (the innermost sphere)
NEW = "#5EE6D0"       # the incoming information
GONE = "#F28EC2"      # given up
SPH = "#6C7A92"       # sphere outlines
IN_C, OUT_C, UND_C = "#5FD38D", "#F25C5C", "#9AA4B2"


def mark(ok: bool, font_size=30) -> Mobject:
    return MathTex(r"\checkmark" if ok else r"\times", font_size=font_size, color=OK if ok else BAD)


def wtex(w: str) -> str:
    """'~bm' -> '\\bar b m'."""
    out, i = [], 0
    while i < len(w):
        if w[i] == "~":
            m = re.match(r"[A-Za-z]", w[i + 1:])
            out.append(r"\bar{" + w[i + 1] + "}")
            i += 2
            del m
        else:
            out.append(w[i])
            i += 1
    return r"\,".join(out)


class SphereView(VGroup):
    """A ranking drawn as Grove's spheres: rank-k worlds on the k-th ring (rank 0 in the middle disc). ``dot[w]``,
    ``tag[w]``, ``ring[k]``, ``pos[w]``."""

    def __init__(self, rank: dict, center=ORIGIN, step=0.95, font_size=20, dot_r=0.11, angles=None, tags=True,
                 names=None, ring_labels=False):
        super().__init__()
        c = np.asarray(center, float)
        ranks = sorted(set(rank.values()))
        multi0 = sum(1 for v in rank.values() if v == ranks[0]) > 1
        r0 = step * (0.8 if multi0 else 0.55)
        self.radius = {k: r0 + step * i for i, k in enumerate(ranks)}
        self.ring, self.dot, self.tag, self.pos = {}, {}, {}, {}
        rings, dots, tg = VGroup(), VGroup(), VGroup()
        for k in ranks:
            r = Circle(radius=self.radius[k], stroke_color=SPH, stroke_width=2).move_to(c)
            if k == ranks[0]:
                r.set_fill(BEL, opacity=0.12).set_stroke(BEL, width=3)
            self.ring[k] = r
            rings.add(r)
        by = {}
        for w, k in rank.items():
            by.setdefault(k, []).append(w)
        for k, ws in by.items():
            inner = self.radius[k] - (step * 0.5 if k != ranks[0] else self.radius[k])
            rr = (self.radius[k] + inner) / 2 if k != ranks[0] else 0.0
            for i, w in enumerate(ws):
                if angles and w in angles:
                    a = angles[w]
                else:
                    a = PI / 2 + TAU * i / max(len(ws), 1) + 0.4 * (k % 2)
                if k == ranks[0] and len(ws) > 1:
                    rr0 = self.radius[k] * 0.5
                    pt = c + rr0 * np.array([np.cos(a), np.sin(a), 0])
                else:
                    pt = c + rr * np.array([np.cos(a), np.sin(a), 0])
                self.pos[w] = pt
                d = Dot(pt, radius=dot_r, color=WHITE)
                self.dot[w] = d
                dots.add(d)
                if tags:
                    t = MathTex(names[w] if names and w in names else wtex(w), font_size=font_size)
                    if k == ranks[0] and len(ws) > 1:      # inside the disc: label towards the middle, stacked
                        t.next_to(d, DOWN if np.sin(a) > -0.5 else UP, buff=0.06)
                        if t.width > rr0 * 1.6:
                            t.width = rr0 * 1.6
                    else:
                        t.next_to(d, DOWN, buff=0.06)
                    self.tag[w] = t
                    tg.add(t)
        self.rings, self.dots, self.tags = rings, dots, tg
        self.add(rings, dots, tg)
        if ring_labels:
            self.rlab = VGroup(*[MathTex(str(k), font_size=18, color=GREY_B).move_to(
                c + np.array([self.radius[k] - 0.15, 0.12, 0])) for k in ranks])
            self.add(self.rlab)

    def paint(self, ws, col) -> list:
        return [self.dot[w].animate.set_color(col) for w in ws if w in self.dot]

    def halo(self, ws, col=NEW) -> VGroup:
        return VGroup(*[Circle(radius=0.22, color=col, stroke_width=4).move_to(self.pos[w]) for w in ws])


class ArgGraph(VGroup):
    """A Dung framework drawn: arguments as discs, attacks as arrows; ``label(lab)`` colours by in/out/undec."""

    def __init__(self, args, attacks, pos: dict, names: dict | None = None, radius=0.38, font_size=22):
        super().__init__()
        self.node, self.pos = {}, {k: np.asarray(v, float) for k, v in pos.items()}
        nodes, arrows = VGroup(), VGroup()
        for a in args:
            disc = Circle(radius=radius, color=WHITE, fill_color="#16222F", fill_opacity=1, stroke_width=3).move_to(
                self.pos[a])
            t = label(names[a] if names and a in names else a, font_size=font_size).move_to(self.pos[a])
            g = VGroup(disc, t)
            self.node[a] = g
            nodes.add(g)
        for x, y in attacks:
            p, q = self.pos[x], self.pos[y]
            if (y, x) in set(map(tuple, attacks)):
                n = np.array([-(q - p)[1], (q - p)[0], 0])
                n = 0.12 * n / (np.linalg.norm(n) + 1e-9)
                arr = Arrow(p + n, q + n, buff=radius + 0.02, color=GREY_B, stroke_width=3,
                            max_tip_length_to_length_ratio=0.18)
            else:
                arr = Arrow(p, q, buff=radius + 0.02, color=GREY_B, stroke_width=3,
                            max_tip_length_to_length_ratio=0.18)
            arrows.add(arr)
        arrows.set_z_index(1)
        nodes.set_z_index(3)
        self.nodes, self.arrows = nodes, arrows
        self.add(arrows, nodes)

    def label_anims(self, lab: dict) -> list:
        col = {"in": IN_C, "out": OUT_C, "undec": UND_C}
        return [self.node[a][0].animate.set_stroke(col[v], width=5).set_fill(col[v], opacity=0.25)
                for a, v in lab.items()]


def caption(text: str, font_size=24, color=GREY_A, buff=0.4) -> Mobject:
    return label(text, font_size=font_size, color=color).to_edge(DOWN, buff=buff)


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
