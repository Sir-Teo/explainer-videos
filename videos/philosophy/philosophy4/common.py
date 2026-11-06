"""Helpers shared by the scenes of Part 4 ("Necessity and Possibility": modal logics)."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import modal

from .compute import load  # noqa: F401

PART = 4
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
WORLD = "#5EE6D0"     # worlds
ACC = "#C3A6FF"       # the accessibility relation
PROP = "#FFD166"      # atomic propositions


def mf(s: str, font_size=38, color=WHITE) -> MathTex:
    """A modal formula (Reasoner syntax) as TeX."""
    return MathTex(modal.show(modal.parse(s), tex=True), font_size=font_size, color=color)


class WorldGraph(VGroup):
    """A Kripke model drawn: worlds as discs (name below, true atoms inside), accessibility as arrows, self-loops
    as small arcs above. ``self.world[w]``, ``self.arrow[(u, v)]``, ``self.inside[w]`` (the atom label)."""

    def __init__(self, worlds, R, V=None, pos=None, radius=0.42, names=None, color=ACC, font_size=26,
                 center=ORIGIN, scale_pos=1.0):
        super().__init__()
        V = V or {}
        n = len(worlds)
        if pos is None:
            pos = {w: np.array([2.2 * np.cos(PI / 2 - TAU * i / n), 2.2 * np.sin(PI / 2 - TAU * i / n), 0])
                   for i, w in enumerate(worlds)}
        c = np.asarray(center, float)
        self.pos = {w: c + scale_pos * np.asarray(pos[w], float) for w in worlds}
        self.world, self.inside, self.arrow, self.name = {}, {}, {}, {}
        discs, arrows = VGroup(), VGroup()
        for w in worlds:
            d = Circle(radius=radius, stroke_color=WORLD, stroke_width=2.5, fill_color="#0B0F17",
                       fill_opacity=1).move_to(self.pos[w])
            true = [a for a in sorted(V) if w in V[a]]
            txt = ",".join(true) if true else r"\cdot"
            ins = MathTex(txt, font_size=font_size, color=PROP if true else GREY_C).move_to(d)
            nm = MathTex(names[w] if names else rf"w_{{{w}}}", font_size=font_size - 4, color=GREY_A).next_to(
                d, DOWN, buff=0.1)
            g = VGroup(d, ins, nm)
            self.world[w], self.inside[w], self.name[w] = g, ins, nm
            discs.add(g)
        for u, v in sorted(R):
            if u == v:
                p = self.pos[u]
                a = Arc(radius=0.22, start_angle=-PI / 6, angle=4 * PI / 3, color=color, stroke_width=2.5).move_to(
                    p + UP * (radius + 0.15))
                a.add_tip(tip_length=0.12, tip_width=0.12)
            else:
                a = Arrow(self.pos[u], self.pos[v], buff=radius + 0.04, color=color, stroke_width=3,
                          max_tip_length_to_length_ratio=0.15, tip_length=0.22)
            self.arrow[(u, v)] = a
            arrows.add(a)
        self.discs, self.arrows = discs, arrows
        self.add(arrows, discs)

    def tag(self, w, ok: bool, font_size=26):
        """A coloured T/F tag beside world w."""
        return tv(ok, font_size).next_to(self.world[w][0], RIGHT, buff=0.12).shift(UP * 0.25)
