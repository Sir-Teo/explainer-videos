"""Helpers shared by the scenes of Part 12 ("Knowledge Among Many")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import epistemic as Ep  # noqa: F401

from .compute import load  # noqa: F401

PART = 12
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
AG = {"a": "#6FB7FF", "b": "#F2A65A", "c": "#C3A6FF", 0: "#6FB7FF", 1: "#F2A65A", 2: "#C3A6FF",
      "A": "#6FB7FF", "B": "#F2A65A"}
KNOW = "#5EE6D0"
COMMON = "#FFD166"
LOSS = "#F28EC2"


def mark(ok: bool, font_size=30) -> Mobject:
    return MathTex(r"\checkmark" if ok else r"\times", font_size=font_size, color=OK if ok else BAD)


class AgentGraph(VGroup):
    """An S5 model drawn: worlds as discs labelled inside, and for each agent a coloured edge between any two worlds
    it cannot tell apart (reflexive loops omitted). ``self.world[w]``, ``self.edge[(agent, u, v)]``."""

    def __init__(self, worlds, edges: dict, pos: dict, labels: dict | None = None, radius=0.36, font_size=22,
                 center=ORIGIN, offsets=None):
        super().__init__()
        c = np.asarray(center, float)
        self.pos = {w: c + np.asarray(pos[w], float) for w in worlds}
        self.world, self.edge = {}, {}
        es, ds = VGroup(), VGroup()
        offsets = offsets or {}
        for ag, pairs in edges.items():
            for u, v in pairs:
                u = tuple(u) if isinstance(u, list) else u
                v = tuple(v) if isinstance(v, list) else v
                a, b = self.pos[u], self.pos[v]
                off = offsets.get(ag, 0.0)
                d = b - a
                nrm = np.array([-d[1], d[0], 0]) / (np.linalg.norm(d) or 1)
                ln = Line(a + nrm * off, b + nrm * off, color=AG[ag], stroke_width=4)
                self.edge[(ag, u, v)] = ln
                es.add(ln)
        for w in worlds:
            disc = Circle(radius=radius, stroke_color=GREY_B, stroke_width=2.5, fill_color="#0B0F17",
                          fill_opacity=1).move_to(self.pos[w])
            t = MathTex((labels or {}).get(w, str(w)), font_size=font_size, color=WHITE).move_to(disc)
            g = VGroup(disc, t)
            self.world[w] = g
            ds.add(g)
        self.edges, self.discs = es, ds
        es.set_z_index(1)
        ds.set_z_index(3)
        self.add(es, ds)


def cube_points(scale=1.6, center=ORIGIN):
    """Positions of the eight worlds of three muddy children, as a cube in an oblique projection."""
    c = np.asarray(center, float)
    pts = {}
    for w in [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]:
        x, y, z = w
        p = np.array([x * 2.0 + z * 0.9, y * 2.0 + z * 0.75, 0]) * scale / 2
        pts[w] = c + p - np.array([1.45, 1.375, 0]) * scale / 2
    return pts


def muddy_cube(scale=1.7, center=ORIGIN, radius=0.3, font_size=20) -> AgentGraph:
    worlds = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    edges = {i: [(w, tuple(1 - w[j] if j == i else w[j] for j in range(3))) for w in worlds if w[i] == 0]
             for i in range(3)}
    pos = {w: p - np.asarray(center, float) for w, p in cube_points(scale, center).items()}
    labels = {w: "".join(map(str, w)) for w in worlds}
    return AgentGraph(worlds, edges, pos, labels, radius=radius, font_size=font_size, center=center)


def person(name: str, color=WHITE, font_size=22, scale=1.0, face=None) -> VGroup:
    head = Circle(radius=0.22 * scale, stroke_color=color, stroke_width=3)
    if face is not None:
        head.set_fill(face, opacity=0.8)
    body = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.55 * scale, color=color, stroke_width=3)
    arms = Line(LEFT * 0.3 * scale, RIGHT * 0.3 * scale, color=color, stroke_width=3).move_to(
        body.get_center() + UP * 0.1 * scale)
    legs = VGroup(Line(body.get_end(), body.get_end() + np.array([-0.22, -0.4, 0]) * scale, color=color,
                       stroke_width=3),
                  Line(body.get_end(), body.get_end() + np.array([0.22, -0.4, 0]) * scale, color=color,
                       stroke_width=3))
    fig = VGroup(head, body, arms, legs)
    if not name:
        g = VGroup(fig)
        g.fig, g.head, g.lab = fig, head, None
        return g
    lab = label(name, font_size=font_size, color=color).next_to(fig, DOWN, buff=0.12)
    g = VGroup(fig, lab)
    g.fig, g.head, g.lab = fig, head, lab
    return g


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
