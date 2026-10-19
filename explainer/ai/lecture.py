"""The lecture's set pieces for *AI, Built*: what a part will cover, definitions and theorems as cards, the history of
an idea, a pause to predict, and the problem set at the end (videos/ai/SYLLABUS.md, "The standard every part meets").

    card = definition_card(r"Markov decision process", r"states $S$, actions $A$, ...")
    self.play(FadeIn(card, shift=UP * 0.2))

Every card is a VGroup with ``.box`` (the outline) and ``.body``; text goes through ``label``/``wrapped_label``, so the
Chinese build translates it from the series' table like any other on-screen string.
"""

from __future__ import annotations

from explainer.analysis import label, wrapped_label
from explainer.ai.viz import *  # noqa: F401,F403

CARD_FILL = "#0B0F17"


def _card(head: Mobject, body: Mobject, color, width: float | None, pad=0.3, accent=True) -> VGroup:
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    w = max(inner.width + 2 * pad, width or 0)
    box = RoundedRectangle(width=w, height=inner.height + 2 * pad, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.8, fill_color=CARD_FILL, fill_opacity=0.94)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * pad)
    g = VGroup(box)
    if accent:  # a bar down the left edge, the card's colour
        bar = Rectangle(width=0.07, height=box.height - 0.28, stroke_width=0, fill_color=color, fill_opacity=1)
        bar.move_to(box.get_left() + RIGHT * 0.12)
        inner.shift(RIGHT * 0.08)
        g.add(bar)
    g.add(inner)
    g.box, g.head, g.body = box, head, body
    return g


def _body(body, width, font_size, color=WHITE) -> Mobject:
    if isinstance(body, Mobject):
        if body.width > width:
            body.width = width
        return body
    return wrapped_label(body, width, font_size, color)


def definition_card(term: str, body, color=None, width: float = 6.4, font_size=24, kind=r"Definition") -> VGroup:
    """A boxed definition: a small coloured tag (``kind``), the term, and what it means (Tex text, or any mobject)."""
    color = color or C.BITS
    tag = label(kind, font_size=font_size - 6, color=color)
    name = label(term, font_size=font_size + 6, color=WHITE)
    head = VGroup(tag, name).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    return _card(head, _body(body, width - 0.8, font_size, GREY_A), color, width)


def theorem_card(name: str, statement, who: str = "", color=None, width: float = 7.2, font_size=24,
                 kind=r"Theorem") -> VGroup:
    """A theorem (or lemma, algorithm): the tag and name on one line, who proved it and when, the statement."""
    color = color or C.TRUE_P
    tag = label(kind, font_size=font_size - 4, color=color)
    nm = label(name, font_size=font_size + 2, color=WHITE)
    row = VGroup(tag, nm).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
    head = VGroup(row)
    if who:
        head.add(label(who, font_size=font_size - 6, color=GREY_B))
        head.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    return _card(head, _body(statement, width - 0.8, font_size), color, width)


def history_card(year, who: str, what: str, color=None, width: float = 5.2, font_size=22) -> VGroup:
    """A moment in the field's history: the year large, who, and what happened."""
    color = color or C.HUMAN
    yr = label(str(year), font_size=font_size + 18, color=color)
    w = wrapped_label(who, width - 0.8, font_size, WHITE)
    head = VGroup(yr, w).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    return _card(head, _body(what, width - 0.8, font_size - 2, GREY_A), color, width)


def pause_card(question: str, color=None, width: float = 8.0, font_size=28) -> VGroup:
    """'Pause and predict': a question to answer before the next sentence answers it."""
    color = color or C.ADVANTAGE
    icon = VGroup(*[RoundedRectangle(width=0.1, height=0.34, corner_radius=0.03, stroke_width=0, fill_color=color,
                                     fill_opacity=1) for _ in range(2)]).arrange(RIGHT, buff=0.08)
    tag = label(r"Pause and predict", font_size=font_size - 6, color=color)
    head = VGroup(icon, tag).arrange(RIGHT, buff=0.18)
    return _card(head, _body(question, width - 0.8, font_size), color, width, accent=False)


def objectives_card(items, title=r"In this part", color=None, font_size=26, width=11.6) -> VGroup:
    """What the part will cover: a title and numbered lines."""
    color = color or C.BITS
    head = label(title, font_size=font_size + 12)
    rows = VGroup()
    for i, it in enumerate(items, 1):
        dot = VGroup(Circle(radius=0.2, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.15),
                     label(str(i), font_size=font_size - 6, color=color))
        dot[1].move_to(dot[0])
        txt = wrapped_label(it, width - 1.0, font_size, WHITE)
        rows.add(VGroup(dot, txt).arrange(RIGHT, buff=0.3, aligned_edge=UP))
        dot.align_to(txt, UP).shift(DOWN * 0.02)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
    g = VGroup(head, rows).arrange(DOWN, buff=0.5)
    rows.align_to(g, LEFT)
    head.set_x(0)
    if g.height > 7.2:
        g.height = 7.2
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)


def problem_set(problems, font_size=22, width=13.0, title=r"Problems") -> VGroup:
    """The part's problems: numbered statements (Tex), full width, shrunk to fit the frame if there are many.
    Solutions live in the part's README."""
    head = label(title, font_size=font_size + 14)
    rows = VGroup()
    for i, p in enumerate(problems, 1):
        n = label(rf"{i}.", font_size=font_size, color=C.BITS)
        t = wrapped_label(p, width - 0.8, font_size, WHITE)
        rows.add(VGroup(n, t).arrange(RIGHT, buff=0.2, aligned_edge=UP))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    g = VGroup(head, rows).arrange(DOWN, buff=0.45)
    head.set_x(0)
    if g.height > 7.3:
        g.height = 7.3
    if g.width > 13.6:
        g.width = 13.6
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)
