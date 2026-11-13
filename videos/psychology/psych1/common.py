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
KANT = "#C9B8FF"  # Kant's objections


def heading(text: str, font_size=36, color=WHITE) -> Tex:
    """A line at the top of the frame saying what the screen is about."""
    return label(text, font_size=font_size, color=color).to_edge(UP, buff=0.4)


def hist(ax, edges, dens, color, opacity=0.55) -> VGroup:
    """A histogram on ``ax`` from bin ``edges`` and densities ``dens``."""
    g = VGroup()
    y0 = ax.c2p(0, 0)[1]
    for a, b, d in zip(edges[:-1], edges[1:], dens):
        if d <= 0:
            continue
        p0, p1 = ax.c2p(a, 0), ax.c2p(b, d)
        g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - y0, 0.005), stroke_color=BACKGROUND, stroke_width=1,
                        fill_color=color, fill_opacity=opacity).move_to([(p0[0] + p1[0]) / 2, (y0 + p1[1]) / 2, 0]))
    return g


def stages_of(rows) -> list:
    """``[(name, ms), ...]`` from the cache to the ``(name, ms, color)`` triples :func:`stage_bar` takes."""
    return [(name, ms, STAGE_COLOR[name]) for name, ms in rows]


def quote_card(text: str, who: str, width: float = 8.0, font_size=28, color=None) -> VGroup:
    """A quotation with its source, on a card."""
    color = color or P.ARCHIVE
    body = wrapped_label(text, width - 0.9, font_size, WHITE)
    src = label(who, font_size=font_size - 8, color=color)
    inner = VGroup(body, src).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    box = RoundedRectangle(width=width, height=inner.height + 0.7, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.8, fill_color=CARD_FILL, fill_opacity=0.95)
    bar = Rectangle(width=0.07, height=box.height - 0.3, stroke_width=0, fill_color=color, fill_opacity=1)
    bar.move_to(box.get_left() + RIGHT * 0.14)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.42)
    g = VGroup(box, bar, inner)
    g.body, g.src = body, src
    return g


OBJECTIONS = [
    (r"No mathematics", r"a thought has no length and no weight: nothing to put a number on"),
    (r"No experiment", r"the mind's contents cannot be taken apart and recombined at will"),
    (r"The observer disturbs", r"watching a mental state changes the state"),
]


def wager_board(replies=(None, None, None), font_size=30, width=13.0) -> VGroup:
    """Kant's three objections, each with the reply so far: ``replies`` holds a ``(text, color)`` per objection, or
    None for none yet.  ``.rows[i]`` has ``.objection`` and ``.reply``."""
    head = label(r"Kant's wager, 1786", font_size=font_size + 10, color=KANT)
    rows = VGroup()
    for i, ((title, _), rep) in enumerate(zip(OBJECTIONS, replies)):
        num = label(rf"{i + 1}", font_size=font_size + 8, color=KANT)
        obj = label(title, font_size=font_size + 4, color=WHITE)
        left = VGroup(num, obj).arrange(RIGHT, buff=0.3)
        if rep is None:
            reply = label(r"no reply yet", font_size=font_size - 2, color=GREY_C)
        else:
            reply = wrapped_label(rep[0], width - 6.0, font_size - 4, rep[1])
        row = VGroup(left, reply)
        row.objection, row.reply = left, reply
        rows.add(row)
    for r in rows:
        r.objection.move_to(ORIGIN, aligned_edge=LEFT)
        r.reply.move_to([5.6, 0, 0], aligned_edge=LEFT)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
    for r in rows:
        r.reply.align_to(r.objection, UP)
    g = VGroup(head, rows).arrange(DOWN, buff=0.5)
    if g.width > width:
        g.width = width
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)


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
