"""Helpers shared by the scenes of Part 1 of *Psychology, Built* ("Kant's Wager")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 1

# one meaning per colour, for this part (the series' P.HUMAN / P.PSYCHE / P.POOL keep theirs)
SENSE = P.SIGNAL  # sensing: the signal reaches the brain and is detected
DISC = "#B48EF0"  # telling one stimulus from another
CHOOSE = "#F28FB8"  # choosing a response
RESPOND = P.RESP  # making the response
GONOGO = "#9BD86B"  # the decision to respond or not (Wundt's objection)
PROGRAM = "#E3B98A"  # programming a response that could not be prepared
STAGE_COLOR = {"sense": SENSE, "discriminate": DISC, "choose": CHOOSE, "respond": RESPOND, "go or no-go": GONOGO,
               "program": PROGRAM}
# Donders' three methods take the colour of the stage each one adds
METHOD = {"a": "#9FD8F0", "c": DISC, "b": CHOOSE}
NERVE = "#F2D16B"
MUSCLE = "#E8736B"
KANT = P.KANT  # Kant's objections


def stages_of(rows) -> list:
    """``[(name, ms), ...]`` from the cache to the ``(name, ms, color)`` triples :func:`stage_bar` takes."""
    return [(name, ms, STAGE_COLOR[name]) for name, ms in rows]


def rt_axes(x_range, y_max, x_length=9.0, y_length=3.6, center=ORIGIN, xticks=None, xlabel=r"reaction time (ms)"):
    """Axes for reaction-time densities: time in ms along x, no numbers on y (a density's height is not read)."""
    return axes(list(x_range), [0, y_max], x_length=x_length, y_length=y_length, xlabel=xlabel, xticks=xticks,
                center=center)


BOX = "#05070B"


def black_box(w=3.0, h=2.0) -> VGroup:
    """Stimulus in, response out, and a box nobody may open.  ``.box``, ``.inp``, ``.out``."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=GREY_A, stroke_width=3,
                           fill_color=BOX, fill_opacity=1)
    inp = Arrow(box.get_left() + LEFT * 2.4, box.get_left(), buff=0.08, color=P.STIM, stroke_width=5)
    out = Arrow(box.get_right(), box.get_right() + RIGHT * 2.4, buff=0.08, color=P.RESP, stroke_width=5)
    s = label(r"stimulus", font_size=30, color=P.STIM).next_to(inp, UP, buff=0.12)
    r = label(r"response", font_size=30, color=P.RESP).next_to(out, UP, buff=0.12)
    g = VGroup(box, inp, out, s, r)
    g.box, g.inp, g.out = box, inp, out
    return g
