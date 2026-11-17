"""The visual instruments of *Psychology, Built* (videos/psychology/SYLLABUS.md, §3), on top of
``explainer.ai.viz``.

* :func:`little_person`, :func:`gear`, :func:`head_outline`, :func:`butterfly`: the series' glyphs.
* :func:`homunculus_map`: the series map as an argument.  A head with a committee of little people inside, one per
  faculty; each part replaces one of them with a mechanism (a gear, with the part's number).  What is still a
  person at the end is the list of open problems.
* :func:`demo_stage`: the "On you" frame, for the demonstrations the viewer performs.
* :func:`trial_strip`: one trial of an experiment as a film strip (fixation, stimulus, response, feedback), the
  standard opening of every study.
* :func:`stage_bar`: a reaction time as consecutive stage durations, to scale.
* :func:`study_card`, :func:`status_chip`, :func:`ledger_card`, :func:`ledger_board`: a study with its design, N
  and effect; a finding with its replication record; the whole Ledger.
* :func:`pool_cloud`: the Pool as a field of dots.
* :func:`heading`, :func:`hist`, :func:`quote_card`: a line saying what the screen is about, a histogram on
  axes, a quotation with its source.
* :func:`wager_board`: Kant's three objections with the replies so far; every part ends by updating it.
* Diagrams for ideas that are not data, so a beat is a picture and not a list: :func:`point_cards` (key points as
  cards in a grid), :func:`flow_chain` (a mechanism or a sequence as boxes and arrows), :func:`quadrant` (a 2x2
  typology on two axes), :func:`pyramid` (a stacked hierarchy), :func:`rings` (nested contexts),
  :func:`theory_card` (a theory, its claim and what the record shows) and :func:`verdict_row` (claims beside
  their Ledger statuses).
"""

from __future__ import annotations

import math
import re

import numpy as np

from explainer.ai.viz import *  # noqa: F401,F403
from explainer.analysis import label, wrapped_label
from explainer.psychology.style import P, STATUS_COLOR

CARD_FILL = "#0B0F17"
PANEL_FILL = "#121722"

__all__ = ["care_card", "CARE_HELP", "little_person", "gear", "head_outline", "butterfly", "FACULTIES", "homunculus_map", "demo_stage",
           "countdown_ring", "trial_strip", "stage_bar", "study_card", "status_chip", "ledger_card", "ledger_board",
           "pool_cloud", "panel", "CARD_FILL", "PANEL_FILL", "heading", "hist", "quote_card", "OBJECTIONS",
           "wager_board", "point_cards", "flow_chain", "quadrant", "pyramid", "rings", "theory_card", "verdict_row"]


def panel(w, h, center=ORIGIN, color=GREY_D, fill=PANEL_FILL) -> RoundedRectangle:
    """A dark rounded panel to draw on."""
    return RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=color, stroke_width=1.5,
                            fill_color=fill, fill_opacity=1).move_to(center)


# ---------------------------------------------------------------------------
# Glyphs
# ---------------------------------------------------------------------------
def little_person(height: float = 0.6, color=None, fill: float = 0.9) -> VGroup:
    """A small figure: a round head on a domed body.  The homunculus, and anyone who stands for a person."""
    color = color or P.PERSON
    r = height * 0.24
    head = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=fill)
    bw = height * 0.74
    body = ArcBetweenPoints(RIGHT * bw / 2, LEFT * bw / 2, angle=PI, stroke_width=0, fill_color=color,
                            fill_opacity=fill)
    body.stretch_to_fit_height(height - 2 * r - height * 0.07)
    head.next_to(body, UP, buff=height * 0.07)
    g = VGroup(body, head)
    g.head, g.body = head, body
    return g.move_to(ORIGIN)


def gear(radius: float = 0.3, teeth: int = 8, color=None, fill: float = 0.9) -> VGroup:
    """A toothed wheel: a faculty that has been replaced by mechanism."""
    color = color or P.MECH
    r_out, r_in = radius, radius * 0.74
    pts = []
    for k in range(teeth):
        a = TAU * k / teeth
        w = TAU / teeth
        for frac, r in ((-0.30, r_in), (-0.18, r_out), (0.18, r_out), (0.30, r_in)):
            ang = a + frac * w
            pts.append([r * math.cos(ang), r * math.sin(ang), 0])
    body = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=fill)
    hole = Circle(radius=radius * 0.3, stroke_width=0, fill_color=CARD_FILL, fill_opacity=1)
    g = VGroup(body, hole)
    g.body, g.hole = body, hole
    return g


_HEAD = [  # a head in profile facing right, in units of its height, counter-clockwise from the nape
    (-0.20, -0.50), (-0.27, -0.34), (-0.41, -0.16), (-0.46, 0.05), (-0.42, 0.27), (-0.28, 0.43), (-0.06, 0.50),
    (0.16, 0.47), (0.32, 0.36), (0.39, 0.20), (0.39, 0.08), (0.41, 0.02), (0.50, -0.09), (0.40, -0.13),
    (0.41, -0.19), (0.37, -0.23), (0.40, -0.28), (0.36, -0.33), (0.36, -0.41), (0.27, -0.46), (0.12, -0.44),
    (0.07, -0.50),
]


def head_outline(height: float = 6.0, color=GREY_B, fill=PANEL_FILL, stroke_width=2.5) -> VMobject:
    """A head in profile, facing right: the room the homunculus lives in.  ``.inside`` is the centre of the
    cranium, where things can be drawn."""
    pts = [np.array([x * height, y * height, 0.0]) for x, y in _HEAD]
    m = VMobject(stroke_color=color, stroke_width=stroke_width, fill_color=fill, fill_opacity=1)
    m.set_points_smoothly(pts + [pts[0]])
    m.inside = np.array([-0.045 * height, 0.13 * height, 0.0])
    return m


def butterfly(height: float = 0.9, color=None) -> VGroup:
    """Psyche's mark: *psyche* is Greek for breath, for the soul, and for a butterfly."""
    color = color or P.PSYCHE
    h = height
    wings = VGroup()
    for sx in (-1, 1):
        up = Ellipse(width=0.62 * h, height=0.42 * h, stroke_width=0, fill_color=color, fill_opacity=0.9)
        up.rotate(sx * 0.6).move_to([sx * 0.33 * h, 0.17 * h, 0])
        lo = Ellipse(width=0.42 * h, height=0.32 * h, stroke_width=0, fill_color=color, fill_opacity=0.6)
        lo.rotate(-sx * 0.5).move_to([sx * 0.24 * h, -0.2 * h, 0])
        wings.add(up, lo)
    body = Line([0, -0.32 * h, 0], [0, 0.3 * h, 0], color=WHITE, stroke_width=3)
    feelers = VGroup(*[Line([0, 0.3 * h, 0], [sx * 0.12 * h, 0.47 * h, 0], color=WHITE, stroke_width=1.5)
                       for sx in (-1, 1)])
    return VGroup(wings, body, feelers)


# ---------------------------------------------------------------------------
# The Homunculus
# ---------------------------------------------------------------------------
# (key, what the little person does, the part that replaces it with a mechanism), in rows of five
FACULTIES = [
    ("reacts", "reacts", 1), ("detects", "detects", 12), ("sees", "sees", 14), ("hears", "hears", 15),
    ("attends", "attends", 18),
    ("learns", "learns", 16), ("predicts", "predicts", 17), ("holds", "holds in mind", 19),
    ("remembers", "remembers", 20), ("kinds", "knows kinds", 22),
    ("speaks", "speaks", 23), ("reasons", "reasons", 24), ("decides", "decides", 25), ("chooses", "chooses", 26),
    ("aware", "is aware", 27),
    ("wants", "wants", 28), ("feels", "feels", 29), ("grows", "grows", 30), ("minds", "reads minds", 35),
    ("suffers", "suffers", 39),
]


def homunculus_map(done=(), height: float = 7.0, whole: bool = False, font_size=15) -> VGroup:
    """The series map as an argument.  A head in profile; inside, either one large little person (``whole``: the
    explanation that explains nothing) or the committee of twenty, one per faculty.  A faculty in ``done`` (its key,
    or any part number at or after which it counts as built) is drawn as a gear with its part number; the others
    are still little people.

    Returns a VGroup with ``.head``, ``.token[key]`` (the figure or gear), ``.name[key]`` (its label) and, when
    ``whole``, ``.person``."""
    head = head_outline(height)
    g = VGroup(head)
    g.head, g.token, g.name = head, {}, {}
    c = head.inside
    if whole:
        person = little_person(height * 0.3, color=P.PERSON).move_to(c + DOWN * 0.02 * height)
        g.add(person)
        g.person = person
        return g
    built = set()
    for item in done if not isinstance(done, int) else ():
        built.add(item)
    upto = done if isinstance(done, int) else 0
    cw, chh = 0.132 * height, 0.105 * height
    for i, (key, text, part) in enumerate(FACULTIES):
        row, col = divmod(i, 5)
        pos = c + np.array([(col - 2) * cw, (1.5 - row) * chh + 0.012 * height, 0.0])
        if key in built or part <= upto:
            tok = gear(0.026 * height, color=P.MECH)
            num = MathTex(str(part), font_size=font_size - 2, color=P.MECH).next_to(tok, RIGHT, buff=0.04)
            tok = VGroup(tok, num)
            tok.move_to(pos + UP * 0.012 * height)
            lab = label(text, font_size=font_size, color=P.MECH)
        else:
            tok = little_person(0.05 * height, color=P.PERSON).move_to(pos + UP * 0.012 * height)
            lab = label(text, font_size=font_size, color=GREY_B)
        if lab.width > cw * 0.96:
            lab.width = cw * 0.96
        lab.move_to(pos + DOWN * 0.034 * height)
        g.add(tok, lab)
        g.token[key], g.name[key] = tok, lab
    return g


# ---------------------------------------------------------------------------
# On you
# ---------------------------------------------------------------------------
def demo_stage(width: float = 9.0, height: float = 5.0, tag: str = r"On you", center=ORIGIN) -> VGroup:
    """The frame for a demonstration the viewer performs: a bordered stage with the series' accent and a tag.
    ``.box`` is the stage (draw at ``stage.box.get_center()``), ``.tag`` the label."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.2, stroke_color=P.ACCENT, stroke_width=3,
                           fill_color="#05070B", fill_opacity=1)
    icon = little_person(0.34, color=P.ACCENT)
    t = label(tag, font_size=26, color=P.ACCENT)
    tg = VGroup(icon, t).arrange(RIGHT, buff=0.14)
    plate = RoundedRectangle(width=tg.width + 0.4, height=tg.height + 0.22, corner_radius=0.1, stroke_color=P.ACCENT,
                             stroke_width=2, fill_color=BACKGROUND, fill_opacity=1)
    plate.move_to(box.get_corner(UL) + RIGHT * (plate.width / 2 + 0.35))
    tg.move_to(plate)
    g = VGroup(box, plate, tg).move_to(center)
    g.box, g.tag = box, VGroup(plate, tg)
    return g


def countdown_ring(radius: float = 0.45, color=None) -> VGroup:
    """A ring that empties: ``ring.arc`` is redrawn from ``ring.t`` (a ValueTracker going from 1 to 0)."""
    color = color or P.ACCENT
    t = ValueTracker(1.0)
    back = Circle(radius=radius, stroke_color=GREY_D, stroke_width=5)
    arc = always_redraw(lambda: Arc(radius=radius, start_angle=PI / 2, angle=-TAU * max(t.get_value(), 1e-3),
                                    stroke_color=color, stroke_width=5).move_arc_center_to(back.get_center()))
    g = VGroup(back, arc)
    g.t, g.arc = t, arc
    return g


# ---------------------------------------------------------------------------
# An experiment, drawn
# ---------------------------------------------------------------------------
def trial_strip(frames, frame_w: float = 2.3, frame_h: float = 1.5, buff: float = 0.55, font_size=20) -> VGroup:
    """One trial as a film strip.  ``frames`` is a list of ``(caption, content, duration)``: the caption under the
    frame, what the participant sees in it (a mobject, scaled to fit, or None for a blank screen) and how long it
    lasts (a Tex string, or "").  Returns a VGroup with ``.frames`` (each with ``.screen``, ``.content``,
    ``.caption``, ``.time``) and ``.arrows``."""
    cells = VGroup()
    for caption, content, duration in frames:
        screen = RoundedRectangle(width=frame_w, height=frame_h, corner_radius=0.08, stroke_color=GREY_B,
                                  stroke_width=2, fill_color="#05070B", fill_opacity=1)
        cell = VGroup(screen)
        if content is not None:
            if content.width > frame_w * 0.84:
                content.scale_to_fit_width(frame_w * 0.84)
            if content.height > frame_h * 0.8:
                content.scale_to_fit_height(frame_h * 0.8)
            content.move_to(screen)
            cell.add(content)
        cap = label(caption, font_size=font_size, color=GREY_A).next_to(screen, DOWN, buff=0.14)
        if cap.width > frame_w + buff * 0.7:
            cap.width = frame_w + buff * 0.7
        cell.add(cap)
        tm = label(duration, font_size=font_size - 2, color=P.ACCENT) if duration else VectorizedPoint()
        tm.next_to(screen, UP, buff=0.12)
        cell.add(tm)
        cell.screen, cell.content, cell.caption, cell.time = screen, content, cap, tm
        cells.add(cell)
    for i, cell in enumerate(cells):
        cell.shift(RIGHT * i * (frame_w + buff) - cell.screen.get_center())
    arrows = VGroup(*[Arrow(a.screen.get_right(), b.screen.get_left(), buff=0.08, color=GREY_C, stroke_width=3,
                            max_tip_length_to_length_ratio=0.3) for a, b in zip(cells, cells[1:])])
    g = VGroup(cells, arrows).move_to(ORIGIN)
    g.frames, g.arrows = cells, arrows
    return g


def stage_bar(stages, unit: float = 0.02, height: float = 0.6, font_size=22, show_ms: bool = True,
              names_above: bool = True) -> VGroup:
    """A reaction time as its stages laid end to end, to scale: ``stages`` is a list of ``(name, ms, color)`` and
    ``unit`` the length of one millisecond.  Returns a VGroup with ``.cells`` (rectangles), ``.names``, ``.ms``
    (the numbers inside or under each cell) and ``.x0`` / ``.end`` (the left and right ends, for alignment)."""
    cells, names, nums = VGroup(), VGroup(), VGroup()
    x = 0.0
    for name, ms, color in stages:
        w = max(ms * unit, 0.02)
        r = Rectangle(width=w, height=height, stroke_color=BACKGROUND, stroke_width=2, fill_color=color,
                      fill_opacity=0.85).move_to([x + w / 2, 0, 0])
        cells.add(r)
        nm = label(name, font_size=font_size, color=color)
        nm.next_to(r, UP if names_above else DOWN, buff=0.12)
        names.add(nm)
        if show_ms:
            n = MathTex(f"{ms:.0f}", font_size=font_size + 2, color=WHITE)
            if n.width > w - 0.08:
                n.next_to(r, DOWN if names_above else UP, buff=0.1).set_color(color)
            else:
                n.move_to(r)
            nums.add(n)
        x += w
    g = VGroup(cells, names, nums)
    g.cells, g.names, g.ms = cells, names, nums
    g.unit = unit
    return g


# ---------------------------------------------------------------------------
# Studies and the Ledger
# ---------------------------------------------------------------------------
def status_chip(status: str, font_size=20) -> VGroup:
    """A Ledger status as a coloured chip."""
    color = STATUS_COLOR[status]
    t = label(status, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 0.34, height=t.height + 0.2, corner_radius=0.09, stroke_color=color,
                           stroke_width=1.6, fill_color=color, fill_opacity=0.12)
    t.move_to(box)
    return VGroup(box, t)


def _marker(filled: bool, color, r=0.075) -> Circle:
    return Circle(radius=r, stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=1.0 if filled else 0.0)


def study_card(title: str, who: str, rows, status: str | None = None, width: float = 6.2, font_size=22,
               color=None) -> VGroup:
    """A study at a glance: its name, who ran it and when, then ``rows`` of ``(field, value)`` (always the design,
    the sample and what was found; the effect with its interval where there is one), and its Ledger status."""
    color = color or P.ARCHIVE
    head = VGroup(label(r"Study", font_size=font_size - 6, color=color), label(title, font_size=font_size + 4),
                  label(who, font_size=font_size - 4, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    body = VGroup()
    fw = max(label(f, font_size=font_size - 4).width for f, _ in rows) + 0.3
    for f, v in rows:
        a = label(f, font_size=font_size - 4, color=color)
        b = wrapped_label(v, width - fw - 0.9, font_size - 2, WHITE)
        b.next_to(a, RIGHT, buff=0).align_to(a, UP).shift(RIGHT * (fw - a.width))
        body.add(VGroup(a, b))
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    if status:
        chip = status_chip(status, font_size - 4)
        inner.add(chip)
        inner.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    box = RoundedRectangle(width=max(width, inner.width + 0.6), height=inner.height + 0.56, corner_radius=0.14,
                           stroke_color=color, stroke_width=1.8, fill_color=CARD_FILL, fill_opacity=0.95)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.3)
    g = VGroup(box, inner)
    g.box, g.head, g.rows = box, head, body
    return g


def _tex(text: str) -> str:
    """Ledger rows are plain prose (they also go to the README and the site): escape what LaTeX would misread."""
    return re.sub(r"(?<!\\)([%&#])", r"\\\1", text)


def _study_line(s, filled: bool, color, width, font_size) -> VGroup:
    mk = _marker(filled, color)
    who = label(rf"{_tex(s.who)} ({s.year})", font_size=font_size, color=color)
    what = wrapped_label(_tex(s.found or s.design), width - 0.6, font_size - 1, GREY_A)
    txt = VGroup(who, what).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
    row = VGroup(mk, txt).arrange(RIGHT, buff=0.2, aligned_edge=UP)
    mk.align_to(who, UP).shift(DOWN * 0.04)
    return row


def ledger_card(f, width: float = 9.6, font_size=22, max_record: int | None = None) -> VGroup:
    """One row of the Replication Ledger as a card: the claim, the original study (a hollow marker), what happened
    when it was run again (filled markers), the status, and the note.  ``f`` is an
    :class:`explainer.psychology.ledger.Finding`.  ``.status``, ``.claim``, ``.original``, ``.record`` (a VGroup of
    lines) and ``.note`` can be revealed one at a time."""
    color = STATUS_COLOR[f.status]
    tag = label(r"The Ledger", font_size=font_size - 5, color=P.ACCENT)
    chip = status_chip(f.status, font_size - 3)
    top = VGroup(tag, chip).arrange(RIGHT, buff=0.3)
    claim = wrapped_label(_tex(f.claim), width - 0.7, font_size + 1, WHITE)
    orig = _study_line(f.original, False, P.ARCHIVE, width - 0.7, font_size - 2)
    rec = VGroup(*[_study_line(s, True, color, width - 0.7, font_size - 2)
                   for s in f.record[: max_record if max_record is not None else len(f.record)]])
    rec.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    parts = [top, claim, orig]
    if len(rec):
        parts.append(rec)
    nt = None
    if f.note:
        nt = wrapped_label(_tex(f.note), width - 0.7, font_size - 3, GREY_B)
        parts.append(nt)
    inner = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    box = RoundedRectangle(width=width, height=inner.height + 0.6, corner_radius=0.14, stroke_color=color,
                           stroke_width=2, fill_color=CARD_FILL, fill_opacity=0.96)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    chip.align_to(box, RIGHT).shift(LEFT * 0.35)
    g = VGroup(box, inner)
    g.box, g.tag, g.status, g.claim, g.original, g.record, g.note = box, tag, chip, claim, orig, rec, nt
    if g.height > 7.4:
        g.height = 7.4
    return g


def ledger_board(findings, font_size=22, width: float = 12.8, title: str = r"The Replication Ledger") -> VGroup:
    """The Ledger as a board: one line per finding with its short title, the original study and its status.
    ``.rows`` holds the lines (each with ``.title``, ``.who``, ``.chip``), ``.head`` the title."""
    head = label(title, font_size=font_size + 12)
    rows = VGroup()
    for f in findings:
        t = label(f.title, font_size=font_size, color=WHITE)
        who = label(rf"{f.original.who}, {f.original.year}", font_size=font_size - 3, color=GREY_B)
        chip = status_chip(f.status, font_size - 4)
        row = VGroup(t, who, chip)
        row.title, row.who, row.chip = t, who, chip
        rows.add(row)
    tw = max(r.title.width for r in rows)
    ww = max(r.who.width for r in rows)
    for r in rows:
        r.title.move_to(ORIGIN, aligned_edge=LEFT)
        r.who.move_to([tw + 0.6, 0, 0], aligned_edge=LEFT)
        r.chip.move_to([tw + ww + 1.2, 0, 0], aligned_edge=LEFT)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    if rows.width > width:
        rows.width = width
    g = VGroup(head, rows).arrange(DOWN, buff=0.55)
    if g.height > 7.3:
        g.height = 7.3
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# The Pool
# ---------------------------------------------------------------------------
def pool_cloud(n: int = 600, width: float = 9.0, height: float = 4.2, seed: int = 0, radius: float = 0.035,
               color=None) -> VGroup:
    """The Pool as a field of ``n`` dots (people), scattered evenly with a little jitter."""
    color = color or P.POOL
    rng = np.random.default_rng(seed)
    cols = int(math.ceil(math.sqrt(n * width / height)))
    rows = int(math.ceil(n / cols))
    dx, dy = width / cols, height / rows
    dots = VGroup()
    for k in range(n):
        r, c = divmod(k, cols)
        x = -width / 2 + (c + 0.5) * dx + rng.uniform(-0.3, 0.3) * dx
        y = -height / 2 + (r + 0.5) * dy + rng.uniform(-0.3, 0.3) * dy
        dots.add(Dot([x, y, 0], radius=radius, color=color, fill_opacity=0.85))
    return dots


# ---------------------------------------------------------------------------
# Headings, histograms, quotations, and the wager board
# ---------------------------------------------------------------------------
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


#: where help is found, shown on the care card (SYLLABUS 1.2): emergency services first, then two national lines
#: and an international directory of helplines
CARE_HELP = [
    (r"in danger now", r"call your local emergency number"),
    (r"United States", r"call or text 988, \ the Suicide and Crisis Lifeline"),
    (r"UK and Ireland", r"Samaritans, \ 116 123"),
    (r"anywhere else", r"findahelpline.com lists free, \ confidential helplines by country"),
]


def care_card(width: float = 12.6, font_size=24, color=None) -> VGroup:
    """The card that opens each part about suffering (Parts 39-42, 57, 59): education, not diagnosis or treatment,
    and where help is found.  Returns VGroup(box, head, body, help) with ``.rows`` for the help lines."""
    color = color or "#6F9BF2"
    head = label(r"Before we start", font_size=font_size + 10, color=color)
    body = wrapped_label(r"This part is education, \ not diagnosis or treatment. \ If any of it touches your own "
                         r"life, \ talk to a doctor, \ a counsellor or someone you trust.", width - 1.2, font_size,
                         WHITE)
    rows = VGroup()
    for who, how in CARE_HELP:
        rows.add(VGroup(label(who, font_size=font_size - 3, color=color),
                        wrapped_label(how, width - 5.2, font_size - 3, GREY_A)).arrange(RIGHT, buff=0.35))
    for r in rows:
        r[1].align_to(rows[0][0].get_left() + RIGHT * 3.4, LEFT)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    for r in rows:
        r[1].move_to([rows.get_left()[0] + 3.4, r[0].get_center()[1], 0], aligned_edge=LEFT)
    inner = VGroup(head, body, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    box = RoundedRectangle(width=width, height=inner.height + 0.9, corner_radius=0.16, stroke_color=color,
                           stroke_width=2, fill_color=CARD_FILL, fill_opacity=0.97)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.55)
    g = VGroup(box, head, body, rows)
    g.box, g.head, g.body, g.rows = box, head, body, rows
    return g


OBJECTIONS = [
    (r"No mathematics", r"a thought has no length and no weight: nothing to put a number on"),
    (r"No experiment", r"the mind's contents cannot be taken apart and recombined at will"),
    (r"The observer disturbs", r"watching a mental state changes the state"),
]


def wager_board(replies=(None, None, None), font_size=30, width=13.0) -> VGroup:
    """Kant's three objections, each with the reply so far: ``replies`` holds a ``(text, color)`` per objection, or
    None for none yet.  ``.rows[i]`` has ``.objection`` and ``.reply``."""
    head = label(r"Kant's wager, 1786", font_size=font_size + 10, color=P.KANT)
    rows = VGroup()
    for i, ((title, _), rep) in enumerate(zip(OBJECTIONS, replies)):
        num = label(rf"{i + 1}", font_size=font_size + 8, color=P.KANT)
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



# ---------------------------------------------------------------------------
# Diagrams for ideas (not data): cards, chains, typologies, hierarchies, nested contexts, theories and verdicts
# ---------------------------------------------------------------------------
def _accent_card(w: float, h: float, color, fill_opacity: float = 0.96) -> VGroup:
    box = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color, stroke_width=1.8,
                           fill_color=CARD_FILL, fill_opacity=fill_opacity)
    bar = Rectangle(width=0.08, height=max(h - 0.3, 0.1), stroke_width=0, fill_color=color, fill_opacity=1)
    bar.move_to(box.get_left() + RIGHT * 0.14)
    return VGroup(box, bar)


def point_cards(items, width: float = 12.6, cols: int | None = None, font_size=24, buff: float = 0.3,
                max_height: float = 5.9) -> VGroup:
    """Key points as a grid of cards: ``items`` is a list of ``(title, body, color)`` (``body`` may be "" or a
    mobject).  Each card has a coloured bar, its title in the colour and its body in white; cards in a row share a
    height.  ``cols`` defaults to 1 for one item, 2 for two or four, else 3.  Returns a VGroup whose ``.cards[i]``
    has ``.box``, ``.title`` and ``.body``, centred at the origin; reveal the cards one at a time."""
    n = len(items)
    cols = cols or (1 if n == 1 else 2 if n in (2, 4) else 3)
    cw = (width - buff * (cols - 1)) / cols
    inners = []
    for title, body, color in items:
        t = wrapped_label(title, cw - 0.75, font_size + 2, color)
        parts = [t]
        if isinstance(body, Mobject):
            if body.width > cw - 0.75:
                body.width = cw - 0.75
            parts.append(body)
        elif body:
            parts.append(wrapped_label(body, cw - 0.75, font_size, WHITE))
        inner = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        inner.title, inner.body, inner.accent = t, (parts[1] if len(parts) > 1 else None), color
        inners.append(inner)
    rows = [inners[i:i + cols] for i in range(0, n, cols)]
    cards = VGroup()
    y = 0.0
    for row in rows:
        h = max(x.height for x in row) + 0.5
        for j, inner in enumerate(row):
            frame = _accent_card(cw, h, inner.accent)
            frame.move_to([j * (cw + buff) + cw / 2, y - h / 2, 0])
            inner.move_to(frame).align_to(frame[0], LEFT).shift(RIGHT * 0.36)
            c = VGroup(frame, inner)
            c.box, c.title, c.body = frame, inner.title, inner.body
            cards.add(c)
        y -= h + buff
    if len(rows) > 1 and len(rows[-1]) < cols:  # centre a short last row
        last = VGroup(*cards[-len(rows[-1]):])
        last.set_x(cards[0].get_left()[0] + (cols * cw + (cols - 1) * buff) / 2)
    g = VGroup(*cards)
    if g.height > max_height:
        g.height = max_height
    g.move_to(ORIGIN)
    g.cards = cards
    return g


def flow_chain(steps, direction=RIGHT, box_w: float = 2.5, box_h: float = 1.1, buff: float = 0.55, font_size=22,
               notes=None, note_size=18) -> VGroup:
    """A mechanism or a sequence: ``steps`` is a list of ``(text, color)`` drawn as boxes joined by arrows, left to
    right (or down, ``direction=DOWN``).  ``notes`` (optional, one string or "" per step) go under each box (beside
    it when vertical).  Returns a VGroup with ``.boxes`` (each with ``.text``), ``.arrows`` and ``.notes``."""
    boxes = VGroup()
    for text, color in steps:
        t = wrapped_label(text, box_w - 0.3, font_size, WHITE)
        if t.height > box_h - 0.2:
            t.height = box_h - 0.2
        r = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.12, stroke_color=color, stroke_width=2.2,
                             fill_color=color, fill_opacity=0.14)
        b = VGroup(r, t.move_to(r))
        b.rect, b.text = r, t
        boxes.add(b)
    boxes.arrange(direction, buff=buff)
    arrows = VGroup(*[Arrow(a.get_edge_center(direction), b.get_edge_center(-direction), buff=0.06,
                            color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.35)
                      for a, b in zip(boxes, boxes[1:])])
    ns = VGroup()
    for b, nt in zip(boxes, notes or [""] * len(steps)):
        if nt:
            if np.allclose(direction, DOWN) or np.allclose(direction, UP):
                m = wrapped_label(nt, 4.2, note_size, GREY_A).next_to(b, RIGHT, buff=0.25)
            else:
                m = wrapped_label(nt, box_w + buff * 0.6, note_size, GREY_A).next_to(b, DOWN, buff=0.18)
            ns.add(m)
        else:
            ns.add(VectorizedPoint(b.get_bottom()))
    g = VGroup(boxes, arrows, ns)
    if g.width > 13.4:
        g.width = 13.4
    g.boxes, g.arrows, g.notes = boxes, arrows, ns
    return g.move_to(ORIGIN)


def quadrant(cells, xlabel: str, ylabel: str, x_ends=(r"low", r"high"), y_ends=(r"low", r"high"),
             size: float = 5.6, font_size=22) -> VGroup:
    """A 2x2 typology on two axes: ``cells`` lists ``(title, body, color)`` for the top-left, top-right,
    bottom-left and bottom-right cells (x grows to the right, y upward).  Returns a VGroup with ``.cells`` (each with
    ``.title``, ``.body``), ``.axes`` (the two axis labels and their ends)."""
    s = size / 2
    out = VGroup()
    cells_g = VGroup()
    centres = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
    for (title, body, color), (cx, cy) in zip(cells, centres):
        sq = RoundedRectangle(width=s - 0.08, height=s - 0.08, corner_radius=0.12, stroke_color=color,
                              stroke_width=2, fill_color=color, fill_opacity=0.12).move_to([cx * s / 2, cy * s / 2, 0])
        t = wrapped_label(title, s - 0.45, font_size + 2, color)
        parts = [t]
        if body:
            parts.append(wrapped_label(body, s - 0.45, font_size - 3, WHITE))
        inner = VGroup(*parts).arrange(DOWN, buff=0.14)
        if inner.height > s - 0.35:
            inner.height = s - 0.35
        inner.move_to(sq)
        c = VGroup(sq, inner)
        c.box, c.title, c.body = sq, t, (parts[1] if len(parts) > 1 else None)
        cells_g.add(c)
    xa = Arrow([-s, -s - 0.25, 0], [s, -s - 0.25, 0], buff=0, color=GREY_B, stroke_width=2.5,
               max_tip_length_to_length_ratio=0.04)
    ya = Arrow([-s - 0.25, -s, 0], [-s - 0.25, s, 0], buff=0, color=GREY_B, stroke_width=2.5,
               max_tip_length_to_length_ratio=0.04)
    xl = label(xlabel, font_size=font_size, color=GREY_A).next_to(xa, DOWN, buff=0.12)
    yl = label(ylabel, font_size=font_size, color=GREY_A).rotate(PI / 2).next_to(ya, LEFT, buff=0.12)
    xe = VGroup(label(x_ends[0], font_size=font_size - 4, color=GREY_C).next_to(xa.get_start(), DOWN, buff=0.12),
                label(x_ends[1], font_size=font_size - 4, color=GREY_C).next_to(xa.get_end(), DOWN, buff=0.12))
    ye = VGroup(label(y_ends[0], font_size=font_size - 4, color=GREY_C).rotate(PI / 2)
                .next_to(ya.get_start(), LEFT, buff=0.12),
                label(y_ends[1], font_size=font_size - 4, color=GREY_C).rotate(PI / 2)
                .next_to(ya.get_end(), LEFT, buff=0.12))
    xe[0].align_to(xa, LEFT)
    xe[1].align_to(xa, RIGHT)
    ye[0].align_to(ya, DOWN)
    ye[1].align_to(ya, UP)
    axes_g = VGroup(xa, ya, xl, yl, xe, ye)
    out.add(axes_g, cells_g)
    out.cells, out.axes = cells_g, axes_g
    return out.move_to(ORIGIN)


def pyramid(levels, width: float = 7.0, height: float = 5.2, font_size=24, gap: float = 0.08) -> VGroup:
    """A stacked hierarchy: ``levels`` lists ``(text, color)`` from the base to the top, drawn as the bands of a
    triangle.  Returns a VGroup with ``.layers`` (each with ``.shape`` and ``.text``), base first."""
    n = len(levels)
    hb = (height - gap * (n - 1)) / n
    layers = VGroup()
    for i, (text, color) in enumerate(levels):
        y0 = -height / 2 + i * (hb + gap)
        y1 = y0 + hb
        w0 = width * (1 - (y0 + height / 2) / height)
        w1 = width * (1 - (y1 + height / 2) / height)
        if i == n - 1:
            w1 = 0.0
        shape = Polygon([-w0 / 2, y0, 0], [w0 / 2, y0, 0], [w1 / 2, y1, 0], [-w1 / 2, y1, 0], stroke_color=color,
                        stroke_width=2, fill_color=color, fill_opacity=0.22)
        t = label(text, font_size=font_size, color=WHITE)
        room = (w0 + w1) / 2 - 0.3 if i < n - 1 else w0 * 0.55
        lead = None
        if t.width > room and room / t.width < 0.75:  # too narrow to read: label beside the band, with a leader
            t.set_color(color)
            mid = np.array([(w0 + w1) / 4 + 0.05, y0 + hb * 0.45, 0])
            t.next_to(mid, RIGHT, buff=0.55)
            lead = Line(mid, t.get_left() + LEFT * 0.08, color=color, stroke_width=1.5)
        else:
            if t.width > room:
                t.width = room
            t.move_to([0, y0 + hb * (0.5 if i < n - 1 else 0.36), 0])
        layer = VGroup(shape, t) if lead is None else VGroup(shape, lead, t)
        layer.shape, layer.text = shape, t
        layers.add(layer)
    g = VGroup(*layers)
    g.layers = layers
    return g.move_to(ORIGIN)


def rings(levels, radius: float = 3.2, font_size=21, centre=None) -> VGroup:
    """Nested contexts (a person inside a family inside a community ...): ``levels`` lists ``(text, color)`` from
    the innermost ring out; each label sits at the top of its band.  ``centre`` is a mobject for the middle (a little
    person by default).  Returns a VGroup with ``.rings`` (each with ``.shape``, ``.text``) and ``.centre``."""
    n = len(levels)
    r0 = radius * 0.26
    step = (radius - r0) / n
    rs = VGroup()
    for i, (text, color) in enumerate(levels):
        r_in, r_out = r0 + i * step, r0 + (i + 1) * step
        shape = Annulus(inner_radius=r_in, outer_radius=r_out, stroke_color=color, stroke_width=1.5,
                        fill_color=color, fill_opacity=0.10 + 0.05 * (n - i) / n)
        t = label(text, font_size=font_size, color=color)
        if t.width > 2 * r_out * 0.8:
            t.width = 2 * r_out * 0.8
        t.move_to([0, (r_in + r_out) / 2, 0])
        ring = VGroup(shape, t)
        ring.shape, ring.text = shape, t
        rs.add(ring)
    c = centre if centre is not None else little_person(r0 * 1.2, color=P.ACCENT)
    disc = Circle(radius=r0 - 0.02, stroke_width=0, fill_color=CARD_FILL, fill_opacity=1)
    c.move_to(ORIGIN)
    g = VGroup(*reversed(rs), disc, c)
    g.rings, g.centre = rs, VGroup(disc, c)
    return g


def theory_card(name: str, who: str, claim: str, verdict: str, status: str, width: float = 6.4, font_size=22,
                color=None) -> VGroup:
    """A theory as the textbooks state it, and what the record shows: its name and author, the claim, a verdict
    line, and a chip in the Ledger's colours (``status`` is a key of ``STATUS_COLOR``).  ``.claim``, ``.verdict``
    and ``.status`` can be revealed one at a time."""
    color = color or P.KANT
    tag = label(r"Theory", font_size=font_size - 6, color=color)
    nm = wrapped_label(name, width - 0.8, font_size + 6, WHITE)
    by = label(who, font_size=font_size - 4, color=GREY_B)
    cl = wrapped_label(claim, width - 0.8, font_size, GREY_A)
    sc = STATUS_COLOR[status]
    ve = wrapped_label(verdict, width - 0.8, font_size - 1, sc)
    chip = status_chip(status, font_size - 4)
    inner = VGroup(tag, nm, by, cl, ve, chip).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    inner[3].shift(DOWN * 0.08)
    inner[4:].shift(DOWN * 0.2)
    frame = _accent_card(width, inner.height + 0.6, color)
    inner.move_to(frame).align_to(frame[0], LEFT).shift(RIGHT * 0.38)
    g = VGroup(frame, inner)
    g.box, g.name, g.claim, g.verdict, g.status = frame, VGroup(tag, nm, by), cl, ve, chip
    return g


def verdict_row(items, width: float = 12.6, font_size=22) -> VGroup:
    """Claims beside their verdicts: ``items`` lists ``(claim, status)``, drawn as lines with a status chip at the
    right, the way the Ledger board reads.  Returns a VGroup with ``.rows`` (each with ``.claim``, ``.chip``)."""
    rows = VGroup()
    chips = [status_chip(st, font_size - 4) for _, st in items]
    cw = max(c.width for c in chips)
    for (claim, st), chip in zip(items, chips):
        mk = _marker(True, STATUS_COLOR[st])
        t = wrapped_label(claim, width - cw - 1.0, font_size, WHITE)
        r = VGroup(mk, t).arrange(RIGHT, buff=0.22, aligned_edge=UP)
        mk.align_to(t, UP).shift(DOWN * 0.05)
        row = VGroup(r, chip)
        chip.move_to([width / 2 - cw / 2, r.get_center()[1], 0])
        r.move_to([-width / 2, r.get_center()[1], 0], aligned_edge=LEFT)
        row.claim, row.chip = r, chip
        rows.add(row)
    rows.arrange(DOWN, buff=0.32)
    for row in rows:
        row.claim.set_x(-width / 2 + row.claim.width / 2)
        row.chip.set_x(width / 2 - cw / 2)
    g = VGroup(*rows)
    g.rows = rows
    return g.move_to(ORIGIN)
