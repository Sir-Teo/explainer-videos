"""Shared instruments for *Economics, Built* (videos/economics/econ1 ... econ68): an undergraduate degree, the
first-year PhD core, the fields, the practice and a research tier.

    from explainer.economics import *

The text helpers, derivation ladder and lecture cards are the other series' (``explainer.analysis``,
``explainer.ai``), so the series typeset alike and share the Chinese on-screen text machinery (with this series'
own table, ``videos/economics/economics_text_zh.json``).  Here, the devices that hold this series together
(videos/economics/README.md, "The devices"):

* the colours, :data:`E` (``explainer.economics.style``): data white, Agora orange, the Island's truth dashed green,
  demand blue and supply amber, one colour for each of the five sectors;
* :func:`chapter_card` with the part's **question** in the corner, the **timeline strip** (1750-2030) and the
  **scale strip**: the level the chapter works at (person to world) and its horizon (a day to a century);
* :func:`series_map`, the twelve acts and sixty-eight parts, with the current part lit;
* :func:`payoff_card`, "where this comes back", over this series' parts;
* tags for where a number comes from: :func:`data_tag` (the Data Room, with source and vintage),
  :func:`published_tag`, :func:`island_tag` (simulated), :func:`agora_tag` (the model), :func:`illustrative_tag`;
* the instruments of :mod:`explainer.economics.viz` (exported here): the glyphs and the Island, the Play-it stage,
  traders' cards and the market cross, the Tableau, and the cards for a study, a dial, a fact, a call and the step
  from *is* to *ought*.

The parts of the series that do not draw, and so import without manim, are beside this file: Agora
(:mod:`explainer.economics.agora`), the Island (``island``), the Facts (``facts``), the Dials (``dials``), Called it?
(``calls``), the Data Room (``data``) and the score (``score``).
"""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F401,F403
from explainer.ai import zh  # noqa: F401
from explainer.analysis import label, note, wrapped_label  # noqa: F401
from explainer.economics.style import DESIGN_COLOR, DIAL_STATUS, E  # noqa: F401

SERIES_EN = "Economics, Built"
SERIES_ZH = "经济学，从零搭建"

# ---------------------------------------------------------------------------
# Twelve acts, sixty-eight parts
# ---------------------------------------------------------------------------
ACTS = [
    (r"I.\ The Question", (1, 4)),
    (r"II.\ Choosing", (5, 8)),
    (r"III.\ Markets", (9, 12)),
    (r"IV.\ Failure and Design", (13, 18)),
    (r"V.\ The Long Run", (19, 24)),
    (r"VI.\ Money and the Cycle", (25, 33)),
    (r"VII.\ The World Economy", (34, 37)),
    (r"VIII.\ Work and the State", (38, 42)),
    (r"IX.\ The Fields", (43, 50)),
    (r"X.\ The Graduate Core", (51, 56)),
    (r"XI.\ Economics at Work", (57, 62)),
    (r"XII.\ The Frontier", (63, 68)),
]
PARTS = {
    1: r"Who Feeds Paris?", 2: r"The Scissors", 3: r"The Measure", 4: r"The Evidence",
    5: r"What People Want", 6: r"Demand", 7: r"Time and Risk", 8: r"The Firm",
    9: r"The Invisible Hand, Proved", 10: r"The Price Maker", 11: r"Games", 12: r"Competition among the Few",
    13: r"Lemons and Signals", 14: r"Incentives", 15: r"Spillovers", 16: r"Auctions", 17: r"Markets by Design",
    18: r"Social Choice and Welfare",
    19: r"The Great Escape", 20: r"Growth I: Capital", 21: r"Growth II: Ideas and Institutions",
    22: r"Consumption and Saving", 23: r"Capital and Asset Prices", 24: r"Looking for Work",
    25: r"Money", 26: r"Banks and Runs", 27: r"The Keynesian Revolution", 28: r"Inflation and Expectations",
    29: r"The Cycle as Equilibrium", 30: r"Sticky Prices", 31: r"The Central Bank", 32: r"The Treasury",
    33: r"Crises",
    34: r"The Open Economy", 35: r"Trade I: Comparative Advantage", 36: r"Trade II: Scale, Firms and Gravity",
    37: r"Cities and Regions",
    38: r"Work and Wages", 39: r"The Wage Structure", 40: r"Inequality and Mobility", 41: r"Taxes",
    42: r"Social Insurance",
    43: r"Measuring Market Power", 44: r"Dynamics, Platforms and Antitrust", 45: r"Behavioural Economics",
    46: r"Development", 47: r"Political Economy", 48: r"Environment and Climate", 49: r"The Economic Approach",
    50: r"The Policy Memo",
    51: r"Computing Economies", 52: r"Many Agents", 53: r"Information and Persuasion", 54: r"Estimating Models",
    55: r"Identifying Macro", 56: r"The Core Exam",
    57: r"Reading the Economy in Real Time", 58: r"Scoring the Bill", 59: r"The Expert Witness", 60: r"The Price",
    61: r"Economics at the Platforms", 62: r"Inside the Firm",
    63: r"The Economy as a Network", 64: r"Machines that Learn", 65: r"The Economics of AI",
    66: r"Geoeconomics and Industrial Policy", 67: r"The Next Economics", 68: r"The Dissertation",
}
MILESTONES = {50: "the degree", 56: "the core exam", 62: "the practice", 68: "the dissertation"}
_MAP_COLUMNS = ((0, 1, 2, 3), (4, 5), (6, 7, 8), (9, 10, 11))


def act_of(part: int) -> int:
    """Index into ACTS of the act that holds ``part``."""
    return next(i for i, (_, (a, b)) in enumerate(ACTS) if a <= part <= b)


def series_map(current: int | None = None, done: int = 0, font_size=15, width=13.7, height=7.4) -> VGroup:
    """The twelve acts in four columns, each part a row; done parts white, ``current`` lit and boxed, the rest dim.
    Returns a VGroup with ``.part[n]`` (each row), ``.acts[i]`` (each act's block, with ``.head``) and ``.box``."""
    blocks = []
    for name, (a, b) in ACTS:
        head = label(name, font_size=font_size + 2, color=GREY_A)
        rows = VGroup()
        for p in range(a, b + 1):
            color = E.ACCENT if p == current else (WHITE if p <= done else GREY_C)
            rows.add(label(rf"{p}.\ {PARTS[p]}", font_size=font_size, color=color))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.075)
        block = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        block.head, block.rows = head, rows
        blocks.append(block)
    cols = VGroup(*[VGroup(*[blocks[i] for i in col]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
                    for col in _MAP_COLUMNS])
    cols.arrange(RIGHT, buff=0.45, aligned_edge=UP)
    if cols.width > width:
        cols.width = width
    if cols.height > height:
        cols.height = height
    g = VGroup(cols)
    g.cols, g.acts, g.part = cols, blocks, {}
    for block, (_, (a, b)) in zip(blocks, ACTS):
        for p, row in zip(range(a, b + 1), block.rows):
            g.part[p] = row
    if current is not None:
        g.box = SurroundingRectangle(g.part[current], color=E.ACCENT, buff=0.05, corner_radius=0.05,
                                     stroke_width=2)
        g.add(g.box)
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# The timeline strip, 1750-2030
# ---------------------------------------------------------------------------
TIMELINE = [
    (1758, r"Quesnay's \emph{Tableau}"),
    (1776, r"\emph{The Wealth of Nations}"),
    (1798, r"Malthus's \emph{Essay}"),
    (1817, r"Ricardo's \emph{Principles}"),
    (1838, r"Cournot"),
    (1845, r"Bastiat's \emph{Sophisms}"),
    (1848, r"Mill's \emph{Principles}; the \emph{Manifesto}"),
    (1867, r"Marx's \emph{Capital}"),
    (1871, r"the marginal revolution"),
    (1874, r"Walras's \emph{Elements}"),
    (1890, r"Marshall's \emph{Principles}"),
    (1920, r"Pigou on welfare"),
    (1929, r"the crash"),
    (1934, r"Kuznets's national income"),
    (1936, r"Keynes's \emph{General Theory}"),
    (1937, r"Coase: why firms exist"),
    (1944, r"von Neumann and Morgenstern; Haavelmo"),
    (1945, r"Hayek on knowledge"),
    (1948, r"Chamberlin's classroom market"),
    (1949, r"Phillips's machine"),
    (1950, r"Nash equilibrium"),
    (1954, r"Arrow and Debreu"),
    (1956, r"Solow's growth model"),
    (1958, r"the Phillips curve"),
    (1962, r"Smith's double auction"),
    (1968, r"Friedman's natural rate"),
    (1970, r"Akerlof's lemons"),
    (1976, r"the Lucas critique"),
    (1979, r"Volcker"),
    (1982, r"Kydland and Prescott"),
    (1990, r"Romer's ideas"),
    (1994, r"Card and Krueger"),
    (2008, r"the financial crisis"),
    (2020, r"the pandemic"),
]
T0, T1 = 1750, 2030


def timeline(lit=(), width=12.0, show_labels=True, font_size=18) -> VGroup:
    """The strip from 1750 to 2030; years in ``lit`` glow and get their names (kept apart and inside the frame, a
    faint leader tying each displaced label to its year).  ``lit`` may be a dict ``{year: name}`` to name the event
    this chapter means."""
    x0 = -width / 2

    def X(y):
        return x0 + width * (y - T0) / (T1 - T0)

    g = VGroup(Line([X(T0), 0, 0], [X(T1), 0, 0], color=GREY_D, stroke_width=2))
    for yr in (1750, 1800, 1850, 1900, 1950, 2000):
        g.add(Line([X(yr), -0.06, 0], [X(yr), 0.06, 0], color=GREY_D, stroke_width=1.5))
        g.add(Text(str(yr), font_size=14, color=GREY_D).next_to([X(yr), 0, 0], DOWN, buff=0.12))
    names = dict(TIMELINE)
    if isinstance(lit, dict):
        names.update(lit)
    labels, anchors, side = VGroup(), [], 1
    for yr in sorted(set(names)):
        on = yr in lit
        d = Dot([X(yr), 0, 0], radius=0.065 if on else 0.035, color=E.ACCENT if on else GREY_C)
        g.add(d)
        if on and show_labels:
            t = label(rf"{yr}\; {names[yr]}", font_size=font_size, color=E.ACCENT)
            t.next_to(d, UP if side > 0 else DOWN, buff=0.14 if side > 0 else 0.4)
            side = -side
            labels.add(t)
            anchors.append(d)
    for row in (1, -1):
        same = sorted([t for t in labels if np.sign(t.get_y()) == row], key=lambda t: t.get_x())
        for a, b in zip(same, same[1:]):
            gap = b.get_left()[0] - a.get_right()[0]
            if gap < 0.2:
                b.shift(RIGHT * (0.2 - gap))
        if same and same[-1].get_right()[0] > 6.9:
            same[-1].shift(LEFT * (same[-1].get_right()[0] - 6.9))
            for i in range(len(same) - 2, -1, -1):
                gap = same[i + 1].get_left()[0] - same[i].get_right()[0]
                if gap < 0.2:
                    same[i].shift(LEFT * (0.2 - gap))
        if same and same[0].get_left()[0] < -6.9:
            same[0].shift(RIGHT * (-6.9 - same[0].get_left()[0]))
    leaders = VGroup()
    for t, d in zip(labels, anchors):
        if abs(t.get_x() - d.get_x()) > 0.1:
            above = t.get_y() > 0
            leaders.add(Line(d.get_top() if above else d.get_bottom(), t.get_bottom() if above else t.get_top(),
                             color=E.ACCENT, stroke_width=1, stroke_opacity=0.4))
    g.add(leaders, labels)
    g.labels, g.leaders = labels, leaders
    return g


# ---------------------------------------------------------------------------
# The scale strip
# ---------------------------------------------------------------------------
SCALES = ("person", "household", "firm", "market", "city", "nation", "world")
HORIZONS = ("a day", "a year", "a decade", "a century")


def scale_strip(scale=("market",), horizon=("a year",), font_size=21, width=12.4) -> VGroup:
    """Where a chapter works: the ladder from one person to the world with ``scale`` lit, and under it the horizon
    with ``horizon`` lit.  ``.scales`` and ``.horizons`` map names to their labels."""

    def row(names, on, size):
        g, m = VGroup(), {}
        for i, s in enumerate(names):
            t = label(s, font_size=size, color=E.ACCENT if s in on else GREY_C)
            m[s] = t
            g.add(t)
            if i < len(names) - 1:
                g.add(MathTex(r"\cdot", font_size=size, color=GREY_D))
        return g.arrange(RIGHT, buff=0.22), m

    top, smap = row(SCALES, scale, font_size)
    bottom, hmap = row(HORIZONS, horizon, font_size - 1)
    g = VGroup(top, bottom).arrange(DOWN, buff=0.16)
    if g.width > width:
        g.width = width
    g.scales, g.horizons = smap, hmap
    return g


def chapter_card(number, title: str, question: str = "", lit=(), part: int | None = None, scale=("market",),
                 horizon=("a year",), ask: str = "") -> VGroup:
    """Chapter title, the question it answers, the scale strip and the timeline strip with this chapter's years lit.
    ``ask`` is the part's own question, kept in the top corner of every chapter card (the series' rule: one question,
    kept in view).  Pass ``scale=None`` to leave the scale strip off."""
    if zh():
        head_text = (rf"第{part}部分 \textperiodcentered\ " if part else "") + f"第{number}章"
    else:
        head_text = (rf"Part {part} \textperiodcentered\ " if part else "") + f"Chapter {number}"
    head = label(head_text, font_size=28, color=GREY_B)
    t = label(title, font_size=54)
    g = VGroup(head, t)
    if question:
        g.add(wrapped_label(question, 11.5, font_size=30, color=GREY_A))
    g.arrange(DOWN, buff=0.3).shift(UP * 1.2)
    strip = timeline(lit=lit).to_edge(DOWN, buff=0.85)
    out = VGroup(g, strip)
    if scale is not None:
        lv = scale_strip(scale, horizon)
        lv.move_to([0, (g.get_bottom()[1] + strip.get_top()[1]) / 2 - 0.05, 0])
        out.add(lv)
        out.levels = lv
    if ask:
        corner = VGroup(Dot(radius=0.05, color=E.ACCENT), label(ask, font_size=22, color=E.ACCENT))
        corner.arrange(RIGHT, buff=0.14).to_corner(UR, buff=0.4)
        out.add(corner)
        out.ask = corner
    out.title, out.strip = g, strip
    return out


# ---------------------------------------------------------------------------
# Payoffs and tags
# ---------------------------------------------------------------------------
def payoff_card(items, font_size=24, title=r"Where this comes back") -> VGroup:
    """``items``: (idea, [part numbers]).  Each row: the idea, an arrow, the parts that use it (number and name)."""
    head = label(title, font_size=font_size + 12)
    rows = VGroup()
    for idea, parts in items:
        left = label(idea, font_size=font_size, color=E.ACCENT)
        right = label(r",\ ".join(rf"{p}\ \textit{{{PARTS[p]}}}" for p in parts), font_size=font_size - 2,
                      color=GREY_A)
        rows.add(VGroup(left, right))
    lw = max(r[0].width for r in rows)
    for r in rows:
        r[0].align_to(ORIGIN, LEFT)
        arrow = MathTex(r"\longrightarrow", font_size=font_size + 4, color=GREY_C)
        r.insert(1, arrow)
        arrow.next_to(ORIGIN, RIGHT, buff=0).shift(RIGHT * (lw + 0.3))
        r[2].next_to(arrow, RIGHT, buff=0.3)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    for r in rows:
        r[1].set_y(r[0].get_y())
        r[2].set_y(r[0].get_y())
    g = VGroup(head, rows).arrange(DOWN, buff=0.5)
    if g.width > 13.4:
        g.width = 13.4
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)


def data_tag(source: str, corner=DL, font_size=20) -> Tex:
    """The Data Room's tag: data, with source and vintage."""
    return note(rf"data: {source}", font_size=font_size, color=E.SOURCE).to_corner(corner, buff=0.3)


def published_tag(source: str, corner=DL, font_size=20) -> Tex:
    """A published result or a passage, cited."""
    return note(rf"published: {source}", font_size=font_size, color=E.SOURCE).to_corner(corner, buff=0.3)


def island_tag(text=r"simulated: the Island", corner=DR, font_size=20) -> Tex:
    """The Island's tag: every number drawn from the simulated world says so."""
    return note(text, font_size=font_size, color=E.ISLAND).to_corner(corner, buff=0.3)


def agora_tag(text=r"computed: Agora (a model)", corner=DR, font_size=20) -> Tex:
    """The model's tag: what is plotted is Agora's behaviour, not the world's."""
    return note(text, font_size=font_size, color=E.AGORA).to_corner(corner, buff=0.3)


def illustrative_tag(text=r"illustrative numbers", corner=DR, font_size=20) -> Tex:
    return note(text, font_size=font_size, color=GREY_B).to_corner(corner, buff=0.3)


from explainer.economics.viz import *  # noqa: E402,F401,F403

# The parts of the series that do not draw, by their own names
import explainer.economics.calls as calls  # noqa: E402,F401
import explainer.economics.data as data  # noqa: E402,F401
import explainer.economics.dials as dials  # noqa: E402,F401
import explainer.economics.facts as facts  # noqa: E402,F401
import explainer.economics.island as island  # noqa: E402,F401
from explainer.economics.data import tables  # noqa: E402,F401
