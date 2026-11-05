"""Helpers shared by the scenes of Part 2 ("The Laws of Thought": propositional logic and SAT)."""

from __future__ import annotations

from explainer.philosophy.studio import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 2
ATOM = P.CLAIM       # atoms, propositional variables
CONN = P.RULE        # connectives and rules of inference
GOAL = P.CONCL       # conclusions, goals
OK = P.TRUE          # true, satisfied, valid
BAD = P.FALSE        # false, conflict, invalid
LEARN = "#9AD1FF"    # learned clauses
HIST = P.HIST
NAMES = "abcdefgh"


def lit_tex(l: int, names=NAMES) -> str:
    """A DIMACS literal (+3 / -3) as TeX over ``names``."""
    return (r"\lnot " if l < 0 else "") + names[abs(l) - 1]


def clause_math(c, names=NAMES, font_size=30, color=WHITE) -> MathTex:
    return MathTex(clause_tex(frozenset(c), list(names)), font_size=font_size, color=color)


def tag_box(text: str, color, font_size=22) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.2, corner_radius=0.08, stroke_color=color,
                           stroke_width=1.6, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))
