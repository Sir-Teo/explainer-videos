"""Helpers shared by the scenes of Part 28 ("Meaning in Use")."""

from __future__ import annotations

import math  # noqa: F401

import numpy as np  # noqa: F401

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import pragmatics as G  # noqa: F401

from .compute import load  # noqa: F401

PART = 28
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
WORD = "#6FB7FF"      # words, signals, utterances
USE = "#F2A65A"       # uses, speakers, acts
RULE_C = "#C3A6FF"    # rules, functions, interpretations
WORLD = "#5EE6D0"     # states, worlds, referents
HEAR = "#F28EC2"      # listeners, receivers
TRUTH = "#F2C14E"     # truth values, probabilities


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            if m.width > 1.15 * width:  # break a long row into lines rather than shrink it out of legibility
                m = wrapped_label(t, width, font_size, c)
            else:
                m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)


def rows_table(rows, x_label=-6.4, x_text=-3.2, top=1.7, gap=0.42, label_size=22, text_size=21, width=9.6):
    g = VGroup()
    for a, b, c in rows:
        x = label(a, font_size=label_size, color=c)
        y = wrapped_label(b, width, text_size, WHITE)
        x.move_to([x_label + x.width / 2, top - x.height / 2, 0])
        y.move_to([x_text + y.width / 2, top - y.height / 2, 0])
        g.add(VGroup(x, y))
        top -= max(x.height, y.height) + gap
    return g


def tv(v, size=24):
    """A truth value as a coloured symbol: T, F, or a gap."""
    if v is None:
        return MathTex(r"\text{---}", font_size=size, color=GREY_B)
    return MathTex(r"\text{T}" if v else r"\text{F}", font_size=size, color=OK if v else BAD)
