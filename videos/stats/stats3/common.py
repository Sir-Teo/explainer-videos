"""Helpers shared by the scenes of Part 3 of *Statistics, Built* ("The Family of Distributions")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import load  # noqa: F401

PART = 3

EXACT = S.TRUTH  # a pmf or density from the formula
SIM = S.EST  # simulated frequencies
DATA = S.MUSEUM  # historical counts
DISC, CONT = FamilyTree.D_COL, FamilyTree.C_COL

# the arrows each chapter derives (the family tree is lit cumulatively, chapter by chapter)
CHAPTER_EDGES = {
    1: ["sum_bern"], 2: ["rare"], 3: ["first", "sum_geo"], 4: ["hyper_bin"], 5: ["gaps", "sum_exp", "geo_exp"],
    6: ["demoivre", "pois_norm"], 7: ["neglog", "box_muller", "exp_log", "pareto"],
    8: ["squares", "gamma_chi", "student", "ratio", "t1", "tinf"], 9: ["order", "gamma_beta"], 10: [], 11: [],
    12: ["gp", "mix_p"], 13: [],
}


def edges_before(chapter: int) -> list:
    return [e for c in range(1, chapter) for e in CHAPTER_EDGES.get(c, [])]


def money(v: float) -> str:
    return f"{v:,.0f}"


def pmf_bars(ax, ks, ps, color, width=0.7, opacity=0.85) -> VGroup:
    return VGroup(*[Rectangle(width=(ax.c2p(width, 0)[0] - ax.c2p(0, 0)[0]),
                              height=max(ax.c2p(0, p)[1] - ax.c2p(0, 0)[1], 0.002), stroke_width=0,
                              fill_color=color, fill_opacity=opacity).move_to(ax.c2p(k, p / 2))
                    for k, p in zip(ks, ps)])


def pmf_dots(ax, ks, ps, color, radius=0.06) -> VGroup:
    return VGroup(*[Dot(ax.c2p(k, p), radius=radius, color=color) for k, p in zip(ks, ps)])


class TreeMixin:
    """The family tree at a chapter's end: earlier arrows lit, this chapter's arrows lighting up."""

    def tree_update(self, chapter: int, narration: str, scale=0.92):
        ft = FamilyTree().scale(scale)
        before = edges_before(chapter)
        nodes = {n for e in before for n in FAMILY_EDGES[e][:2]}
        ft.lit_state(nodes=nodes, edges=before)
        head = label(r"The family tree", font_size=26, color=GREY_B).to_corner(UL, buff=0.25)
        with self.voiceover(narration) as vo:
            self.play(FadeIn(ft), FadeIn(head))
            new = CHAPTER_EDGES.get(chapter, [])
            if new:
                vo.wait_until("t")
                self.play(*ft.light_edges(*new), run_time=1.6)
        self.wait(0.5)
        self.clear_scene()
