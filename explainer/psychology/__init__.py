"""Shared instruments for *Psychology, Built* (videos/psychology/psych1 ... psych62): an undergraduate degree, the
graduate methods sequence, the practice, and a research tier.

    from explainer.psychology import *

The text helpers, derivation ladder and lecture cards are the other series' (``explainer.analysis``,
``explainer.ai``), so all the series typeset alike and share the Chinese on-screen text machinery (with this
series' own table, ``videos/psychology/psychology_text_zh.json``).  Here, the devices that hold this series together
(videos/psychology/README.md, "The devices"):

* the colours, :data:`P` (``explainer.psychology.style``): human data white, Psyche orange, the Pool grey-blue;
* :func:`chapter_card` with the **timeline strip**, 1780-2030, from Kant's objections to the reforms, and the
  **levels strip**: the scale the chapter works at and which of Marr's levels it answers;
* :func:`series_map`, the thirteen acts and sixty-two parts, with the current part lit;
* :func:`payoff_card`, "where this comes back", over this series' parts;
* tags for where a number comes from: :func:`historical_tag` (the Archive), :func:`published_tag`,
  :func:`simulated_tag` (the Pool), :func:`psyche_tag` (the model);
* the instruments of :mod:`explainer.psychology.viz` (exported here): the Homunculus, the On-you stage, the trial
  strip, stage bars, study and Ledger cards.

The parts of the series that do not draw, and so import without manim, are beside this file: Psyche
(:mod:`explainer.psychology.psyche`), the Pool (``pool``), the Battery (``battery``), the Ledger (``ledger``) and
the Archive (``archive``).
"""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F401,F403
from explainer.ai import zh  # noqa: F401
from explainer.analysis import label, note, wrapped_label  # noqa: F401
from explainer.psychology.style import P, STATUS_COLOR  # noqa: F401

SERIES_EN = "Psychology, Built"
SERIES_ZH = "心理学，从零搭建"

# ---------------------------------------------------------------------------
# Thirteen acts, sixty-two parts
# ---------------------------------------------------------------------------
ACTS = [
    (r"I.\ Asking a Mind a Question", (1, 4)),
    (r"II.\ The Wet Machine", (5, 10)),
    (r"III.\ Sensing", (11, 15)),
    (r"IV.\ Learning", (16, 17)),
    (r"V.\ Thinking", (18, 27)),
    (r"VI.\ Feeling and Wanting", (28, 29)),
    (r"VII.\ Growing", (30, 31)),
    (r"VIII.\ Differing", (32, 33)),
    (r"IX.\ Other People", (34, 38)),
    (r"X.\ When Minds Suffer", (39, 43)),
    (r"XI.\ The Graduate Toolkit", (44, 50)),
    (r"XII.\ Psychology at Work", (51, 57)),
    (r"XIII.\ The Frontier", (58, 62)),
]
PARTS = {
    1: r"Kant's Wager", 2: r"The Experiment", 3: r"The Measure", 4: r"The Evidence",
    5: r"The Neuron", 6: r"Synapses and Circuits", 7: r"The Brain", 8: r"Reading the Brain",
    9: r"Genes and Evolution", 10: r"Chemistry and Clocks",
    11: r"The Threshold", 12: r"Signal and Noise", 13: r"The Eye and the Code", 14: r"Seeing as Inference",
    15: r"The Other Senses",
    16: r"Conditioning", 17: r"Reward and Prediction",
    18: r"Attention", 19: r"Working Memory", 20: r"Memory I: Storing and Finding",
    21: r"Memory II: Forgetting and Inventing", 22: r"Concepts and Categories", 23: r"Language",
    24: r"Reasoning and Problem Solving", 25: r"Deciding in Time", 26: r"Judgment and Choice", 27: r"Consciousness",
    28: r"Motivation", 29: r"Emotion",
    30: r"The Infant Mind", 31: r"The Lifespan",
    32: r"Intelligence", 33: r"Personality",
    34: r"Social Influence", 35: r"Social Cognition", 36: r"Us and Them", 37: r"Bonds and Bargains",
    38: r"Culture and Morals",
    39: r"What Is a Disorder?", 40: r"Fear and Sadness", 41: r"Psychosis, Addiction and Development",
    42: r"Does Therapy Work?", 43: r"The Replication",
    44: r"Latent Variables", 45: r"Item Response Theory", 46: r"Scaling, Surveys and Choice",
    47: r"People over Time", 48: r"Modelling Behaviour", 49: r"Modelling the Brain's Data",
    50: r"The Weight of Evidence",
    51: r"Human Factors", 52: r"Designing for Minds", 53: r"People at Work", 54: r"The Science of Learning",
    55: r"Behaviour Change at Scale", 56: r"Psychology and Law", 57: r"Health and Care",
    58: r"The Efficient, Predictive Brain", 59: r"Computational Psychiatry", 60: r"Minds and Machines",
    61: r"The Next Psychology", 62: r"The Dissertation",
}
MILESTONES = {43: "the degree", 50: "the graduate toolkit", 57: "the practice", 62: "the dissertation"}
# which acts share a column of the series map
_MAP_COLUMNS = ((0, 1, 2), (3, 4, 5, 6), (7, 8, 9), (10, 11, 12))


def act_of(part: int) -> int:
    """Index into ACTS of the act that holds ``part``."""
    return next(i for i, (_, (a, b)) in enumerate(ACTS) if a <= part <= b)


def series_map(current: int | None = None, done: int = 0, font_size=17, width=13.7, height=7.5) -> VGroup:
    """The thirteen acts in four columns, each part a row; done parts white, ``current`` lit and boxed, the rest
    dim.  Returns a VGroup with ``.part[n]`` (each row), ``.acts[i]`` (each act's block, with ``.head``) and
    ``.box``."""
    blocks = []
    for name, (a, b) in ACTS:
        head = label(name, font_size=font_size + 2, color=GREY_A)
        rows = VGroup()
        for p in range(a, b + 1):
            color = P.ACCENT if p == current else (WHITE if p <= done else GREY_C)
            rows.add(label(rf"{p}.\ {PARTS[p]}", font_size=font_size, color=color))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.085)
        block = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        block.head, block.rows = head, rows
        blocks.append(block)
    cols = VGroup(*[VGroup(*[blocks[i] for i in col]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
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
        g.box = SurroundingRectangle(g.part[current], color=P.ACCENT, buff=0.05, corner_radius=0.05,
                                     stroke_width=2)
        g.add(g.box)
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# The timeline strip, 1780-2030
# ---------------------------------------------------------------------------
TIMELINE = [
    (1786, r"Kant: no science of the soul"),
    (1834, r"Weber's fraction"),
    (1850, r"Helmholtz times the nerve; Fechner's morning"),
    (1860, r"Fechner's \emph{Elements}"),
    (1868, r"Donders' subtraction"),
    (1879, r"Wundt's laboratory"),
    (1884, r"Peirce and Jastrow randomize"),
    (1885, r"Ebbinghaus on memory"),
    (1890, r"James's \emph{Principles}"),
    (1898, r"Thorndike's puzzle box"),
    (1904, r"Spearman's $g$; Clever Hans"),
    (1905, r"Binet's scale"),
    (1913, r"Watson's manifesto"),
    (1927, r"Pavlov in English; Thurstone's law"),
    (1935, r"Stroop"),
    (1938, r"Skinner's \emph{Behavior of Organisms}"),
    (1946, r"Stevens's scales"),
    (1948, r"Tolman's maps; Shannon's information"),
    (1949, r"Hebb's rule"),
    (1951, r"Lashley on serial order"),
    (1952, r"Hick's law; Hodgkin and Huxley"),
    (1954, r"signal detection theory"),
    (1956, r"the cognitive revolution"),
    (1959, r"Chomsky reviews Skinner"),
    (1961, r"Milgram's obedience studies"),
    (1967, r"Neisser's \emph{Cognitive Psychology}"),
    (1969, r"Sternberg's additive factors"),
    (1972, r"Rescorla and Wagner"),
    (1974, r"heuristics and biases"),
    (1978, r"Ratcliff's diffusion model"),
    (1980, r"DSM-III"),
    (1982, r"Marr's \emph{Vision}"),
    (1986, r"parallel distributed processing"),
    (1990, r"the BOLD signal"),
    (1997, r"dopamine as prediction error"),
    (2011, r"the replication crisis"),
    (2015, r"a hundred replications"),
    (2018, r"Many Labs 2"),
]
T0, T1 = 1780, 2030


def timeline(lit=(), width=12.0, show_labels=True, font_size=18) -> VGroup:
    """The strip from 1780 to 2030; years in ``lit`` glow and get their names (kept apart and inside the frame, a
    faint leader tying each displaced label to its year).  ``lit`` may be a dict ``{year: name}`` to name the event
    this chapter means, where the table lists several for the year."""
    x0 = -width / 2

    def X(y):
        return x0 + width * (y - T0) / (T1 - T0)

    g = VGroup(Line([X(T0), 0, 0], [X(T1), 0, 0], color=GREY_D, stroke_width=2))
    for yr in (1800, 1850, 1900, 1950, 2000):
        g.add(Line([X(yr), -0.06, 0], [X(yr), 0.06, 0], color=GREY_D, stroke_width=1.5))
        g.add(Text(str(yr), font_size=14, color=GREY_D).next_to([X(yr), 0, 0], DOWN, buff=0.12))
    names = dict(TIMELINE)
    if isinstance(lit, dict):
        names.update(lit)
    labels, anchors, side = VGroup(), [], 1
    for yr in sorted(set(names)):
        on = yr in lit
        d = Dot([X(yr), 0, 0], radius=0.065 if on else 0.035, color=P.ACCENT if on else GREY_C)
        g.add(d)
        if on and show_labels:
            t = label(rf"{yr}\; {names[yr]}", font_size=font_size, color=P.ACCENT)
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
                             color=P.ACCENT, stroke_width=1, stroke_opacity=0.4))
    g.add(leaders, labels)
    g.labels, g.leaders = labels, leaders
    return g


# ---------------------------------------------------------------------------
# The levels strip
# ---------------------------------------------------------------------------
SCALES = ("molecule", "neuron", "circuit", "brain", "mind", "person", "group", "culture")
MARR = {"what": r"what is computed", "how": r"by what algorithm", "tissue": r"in what tissue"}


def levels_strip(scale=("mind",), marr=("how",), font_size=21, width=12.4) -> VGroup:
    """Where a chapter works: the scale ladder from molecule to culture with ``scale`` lit, and under it Marr's
    three levels with ``marr`` lit (keys of :data:`MARR`).  ``.scales`` and ``.marr`` map names to their labels."""
    top = VGroup()
    smap = {}
    for i, s in enumerate(SCALES):
        on = s in scale
        t = label(s, font_size=font_size, color=P.ACCENT if on else GREY_C)
        smap[s] = t
        top.add(t)
        if i < len(SCALES) - 1:
            top.add(MathTex(r"\cdot", font_size=font_size, color=GREY_D))
    top.arrange(RIGHT, buff=0.22)
    bottom = VGroup()
    mmap = {}
    for i, (k, text) in enumerate(MARR.items()):
        on = k in marr
        t = label(text, font_size=font_size - 1, color=P.ACCENT if on else GREY_C)
        mmap[k] = t
        bottom.add(t)
        if i < len(MARR) - 1:
            bottom.add(MathTex(r"\cdot", font_size=font_size, color=GREY_D))
    bottom.arrange(RIGHT, buff=0.3)
    g = VGroup(top, bottom).arrange(DOWN, buff=0.16)
    if g.width > width:
        g.width = width
    g.scales, g.marr = smap, mmap
    return g


def chapter_card(number, title: str, question: str = "", lit=(), part: int | None = None, scale=("mind",),
                 marr=("how",)) -> VGroup:
    """Chapter title, the question it answers, the levels strip and the timeline strip with this chapter's years
    lit.  ``scale`` and ``marr`` say where the chapter works (:func:`levels_strip`); pass ``scale=None`` to leave
    the levels strip off (the outro)."""
    if zh():
        head_text = (rf"第{part}部分 \textperiodcentered\ " if part else "") + f"第{number}章"
    else:
        head_text = (rf"Part {part} \textperiodcentered\ " if part else "") + f"Chapter {number}"
    head = label(head_text, font_size=28, color=GREY_B)
    t = label(title, font_size=54)
    g = VGroup(head, t)
    if question:
        g.add(wrapped_label(question, 11.5, font_size=30, color=GREY_A))
    g.arrange(DOWN, buff=0.3).shift(UP * 1.25)
    strip = timeline(lit=lit).to_edge(DOWN, buff=0.85)
    out = VGroup(g, strip)
    if scale is not None:
        lv = levels_strip(scale, marr)
        lv.move_to([0, (g.get_bottom()[1] + strip.get_top()[1]) / 2 - 0.05, 0])
        out.add(lv)
        out.levels = lv
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
        left = label(idea, font_size=font_size, color=P.ACCENT)
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


def historical_tag(source: str, corner=DL) -> Tex:
    """The Archive's tag: historical data, with its source."""
    return note(rf"historical data: {source}", color=P.ARCHIVE).to_corner(corner, buff=0.3)


def published_tag(source: str, corner=DL) -> Tex:
    """A published result, cited."""
    return note(rf"published: {source}", color=P.ARCHIVE).to_corner(corner, buff=0.3)


def simulated_tag(text=r"simulated: the Pool", corner=DR) -> Tex:
    """The Pool's tag: every number drawn from simulated participants says so."""
    return note(text, color=P.POOL).to_corner(corner, buff=0.3)


def psyche_tag(text=r"computed: Psyche (a model)", corner=DR) -> Tex:
    """The model's tag: what is plotted is Psyche's behaviour, not a person's."""
    return note(text, color=P.PSYCHE).to_corner(corner, buff=0.3)


from explainer.psychology.viz import *  # noqa: E402,F401,F403

# The parts that do not draw, by their own names.  ``ledger`` here is this series' Replication Ledger (the module),
# which replaces the analysis series' ``ledger()`` table that the star imports above bring along.
import explainer.psychology.archive as archive  # noqa: E402,F401
import explainer.psychology.battery as battery  # noqa: E402,F401
import explainer.psychology.ledger as ledger  # noqa: E402,F401,F811
import explainer.psychology.pool as pool  # noqa: E402,F401
