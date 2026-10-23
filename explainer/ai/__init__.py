"""Shared instruments for the AI series (videos/ai/ai1 ... ai30), *AI, Built*.

    from explainer.ai import *

The text helpers and the derivation ladder are the analysis series' (``explainer.analysis``: ``label``, ``note``,
``mtex``, ``why``, ``ladder``, ``boxed``, ``wrapped_label``, ...), so the two series typeset alike and share the
Chinese on-screen text machinery (``explainer/zh_text.py``, with this series' own table,
``videos/ai/ai_text_zh.json``).  Here, the devices that hold this series together:

* :func:`chapter_card` with the **timeline strip**, 1940-2030, the history of the ideas lit as the series reaches them;
* :func:`series_map`, the thirty-one parts in five acts and a finale, with the current part lit;
* :func:`scoreboard`, the series' running record: bits per character on one fixed passage, one row per model, filled
  in as the parts build the models (Part 1 computes the passage and the first rows, ``.cache/ai1/scoreboard.json``);
* :func:`payoff_card`, "where this comes back": an idea and the later parts that use it;
* :func:`reference_card`, the books and papers a part follows, and :func:`cite`, a source line on screen.

The visual instruments, and the series' visual language, are in :mod:`explainer.ai.viz` (exported here):
color-linked derivations (``cmath``, ``morph``), ``LiveBars``, ``glow_dot``, camera framing, loss surfaces. The
lecture's set pieces (objectives, definition and theorem cards, history cards, pause-and-predict, the problem set) are
in :mod:`explainer.ai.lecture`, also exported here.
"""

from __future__ import annotations

import os

import numpy as np

from explainer.analysis import *  # noqa: F401,F403
from explainer.analysis import _zh, label, note, wrapped_label  # noqa: F401
from explainer.ai.viz import *  # noqa: F401,F403
from explainer.ai.lecture import *  # noqa: F401,F403,E402
from explainer.ai.games import *  # noqa: F401,F403,E402

SERIES_EN = "AI, Built"
SERIES_ZH = "人工智能，从零搭建"


def zh() -> bool:
    return os.environ.get("EXPLAINER_LANG", "en") == "zh"


def data_text(s: str, **kw) -> Text:
    """Text that is data, words a model read or wrote: never translated, even when a word is in the table."""
    if zh() or os.environ.get("EXPLAINER_COLLECT_TEXT"):
        from explainer.zh_text import verbatim

        with verbatim():
            return Text(s, **kw)
    return Text(s, **kw)


# ---------------------------------------------------------------------------
# The thirty-one parts
# ---------------------------------------------------------------------------
ACTS = [
    (r"I.\ Foundations", (1, 5)),
    (r"II.\ Learning from Data", (6, 12)),
    (r"III.\ The Transformer Era", (13, 19)),
    (r"IV.\ Generation and Perception", (20, 25)),
    (r"V.\ Agency", (26, 29)),
    (r"Finale", (30, 31)),
]
PARTS = {
    1: r"The Guessing Game", 2: r"Thinking Machines", 3: r"Vectors That Mean Things", 4: r"Change",
    5: r"Randomness in Motion",
    6: r"Classical ML", 7: r"Statistical ML", 8: r"Fitting and Generalizing", 9: r"Networks",
    10: r"Seeing and Remembering", 11: r"Going Downhill", 12: r"The Mathematics of Scale",
    13: r"Attention as Geometry", 14: r"The Language-Model Lineage", 15: r"Memory", 16: r"Sparsity", 17: r"Silicon",
    18: r"Pretraining at Scale", 19: r"Inference",
    20: r"Four Ways to Generate", 21: r"Diffusion and Flow", 22: r"Images, Video and 3D",
    23: r"Every Sense Is a Token", 24: r"Learning Without Labels", 25: r"Symmetry and Science",
    26: r"Reinforcement Learning", 27: r"Post-Training and Alignment", 28: r"Reasoning", 29: r"Agents and Worlds",
    30: r"Inside the Model", 31: r"Can We Trust It?",
}


def series_map(current: int | None = None, done: int = 0, font_size=20, width=13.2, height=7.4) -> VGroup:
    """The acts in a grid of three columns, two rows; each part a row.  Parts up to ``done`` are white, ``current``
    is lit and boxed, the rest are dim."""
    cols = VGroup()
    for act, (a, b) in ACTS:
        head = label(act, font_size=font_size + 4, color=GREY_A)
        rows = VGroup()
        for p in range(a, b + 1):
            color = C.BITS if p == current else (WHITE if p <= done else GREY_C)
            rows.add(label(rf"{p}.\ {PARTS[p]}", font_size=font_size, color=color))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        col = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        col.head, col.rows = head, rows
        cols.add(col)
    cols.arrange_in_grid(rows=2, cols=3, buff=(0.6, 0.45), cell_alignment=UL)
    if cols.width > width:
        cols.width = width
    if cols.height > height:
        cols.height = height
    g = VGroup(cols)
    g.cols = cols
    g.part = {}
    for col, (_, (a, b)) in zip(cols, ACTS):
        for p, row in zip(range(a, b + 1), col.rows):
            g.part[p] = row
    if current is not None:
        box = SurroundingRectangle(g.part[current], color=C.BITS, buff=0.1, corner_radius=0.08, stroke_width=2)
        g.add(box)
        g.box = box
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# The timeline strip
# ---------------------------------------------------------------------------
TIMELINE = [
    (1943, r"McCulloch--Pitts neurons"),
    (1948, r"Shannon: information theory"),
    (1949, r"Hebb's rule"),
    (1950, r"Turing's test; Shannon's chess"),
    (1951, r"Shannon's guessing game"),
    (1952, r"Huffman codes"),
    (1953, r"Markov chain Monte Carlo"),
    (1956, r"the Dartmouth workshop"),
    (1957, r"Bellman: dynamic programming"),
    (1958, r"the perceptron"),
    (1959, r"Samuel's checkers"),
    (1960, r"ADALINE"),
    (1962, r"DPLL"),
    (1964, r"kernel smoothers"),
    (1965, r"Moore's law"),
    (1966, r"ELIZA"),
    (1968, r"A* search"),
    (1969, r"\textit{Perceptrons}"),
    (1971, r"STRIPS"),
    (1972, r"Prolog"),
    (1973, r"the Lighthill report"),
    (1974, r"Dennard scaling"),
    (1976, r"arithmetic coding"),
    (1978, r"systolic arrays"),
    (1979, r"the bootstrap"),
    (1980, r"expert systems (XCON)"),
    (1982, r"Hopfield networks"),
    (1983, r"simulated annealing"),
    (1984, r"random projections"),
    (1985, r"IEEE 754 floating point"),
    (1986, r"backpropagation"),
    (1987, r"the Lisp-machine crash"),
    (1989, r"Q-learning"),
    (1990, r"latent semantic analysis"),
    (1991, r"vanishing gradients"),
    (1992, r"TD-Gammon"),
    (1994, r"MPI: collective communication"),
    (1995, r"support vector machines"),
    (1997, r"LSTM; Deep Blue"),
    (1998, r"LeNet-5; MNIST"),
    (1999, r"the GPU"),
    (2002, r"contrastive divergence"),
    (2003, r"a neural language model"),
    (2004, r"SIFT features"),
    (2005, r"multicore: the power wall"),
    (2006, r"Monte Carlo tree search"),
    (2007, r"CUDA"),
    (2008, r"Common Crawl"),
    (2009, r"ImageNet"),
    (2010, r"Glorot--Bengio initialization"),
    (2012, r"AlexNet"),
    (2013, r"word2vec; DQN"),
    (2014, r"Adam; GANs"),
    (2015, r"ResNet; diffusion"),
    (2016, r"AlphaGo"),
    (2017, r"the Transformer; AlphaZero"),
    (2018, r"GPT-1; BERT"),
    (2019, r"GPT-2; MuZero"),
    (2020, r"scaling laws; GPT-3"),
    (2021, r"Codex; instruction tuning"),
    (2022, r"Chinchilla; ChatGPT"),
    (2023, r"open weights; DPO"),
    (2024, r"reasoning models"),
    (2025, r"DeepSeek-R1"),
    (2026, r"agents"),
]
T0, T1 = 1940, 2030


def timeline(lit=(), width=12.0, show_labels=True, font_size=18) -> VGroup:
    """The strip from 1940 to 2030; years in ``lit`` glow and get their names."""
    x0 = -width / 2

    def X(y):
        return x0 + width * (y - T0) / (T1 - T0)

    g = VGroup(Line([X(T0), 0, 0], [X(T1), 0, 0], color=GREY_D, stroke_width=2))
    for yr in (1950, 1970, 1990, 2010, 2030):
        g.add(Line([X(yr), -0.06, 0], [X(yr), 0.06, 0], color=GREY_D, stroke_width=1.5))
        g.add(Text(str(yr), font_size=14, color=GREY_D).next_to([X(yr), 0, 0], DOWN, buff=0.12))
    labels = VGroup()
    side = 1
    for yr, name in TIMELINE:
        on = yr in lit
        d = Dot([X(yr), 0, 0], radius=0.065 if on else 0.04, color=C.BITS if on else GREY_C)
        g.add(d)
        if on and show_labels:
            t = label(rf"{yr}\; {name}", font_size=font_size, color=C.BITS)
            t.next_to(d, UP if side > 0 else DOWN, buff=0.14 if side > 0 else 0.4)
            side = -side
            labels.add(t)
    # keep the lit labels apart and inside the frame
    for row in (1, -1):
        same = sorted([t for t in labels if np.sign(t.get_y()) == row], key=lambda t: t.get_x())
        for a, b in zip(same, same[1:]):  # left to right: no overlaps
            gap = b.get_left()[0] - a.get_right()[0]
            if gap < 0.2:
                b.shift(RIGHT * (0.2 - gap))
        if same and same[-1].get_right()[0] > 6.9:  # the last one back inside, pushing its neighbours left
            same[-1].shift(LEFT * (same[-1].get_right()[0] - 6.9))
            for i in range(len(same) - 2, -1, -1):
                gap = same[i + 1].get_left()[0] - same[i].get_right()[0]
                if gap < 0.2:
                    same[i].shift(LEFT * (0.2 - gap))
        if same and same[0].get_left()[0] < -6.9:
            same[0].shift(RIGHT * (-6.9 - same[0].get_left()[0]))
    g.add(labels)
    g.labels = labels
    return g


def chapter_card(number, title: str, question: str = "", lit=(), part: int | None = None) -> VGroup:
    """Chapter title, the question it answers, and the timeline strip with this chapter's years lit."""
    if zh():
        head_text = (rf"第{part}部分 \textperiodcentered\ " if part else "") + f"第{number}章"
    else:
        head_text = (rf"Part {part} \textperiodcentered\ " if part else "") + f"Chapter {number}"
    head = label(head_text, font_size=28, color=GREY_B)
    t = label(title, font_size=54)
    g = VGroup(head, t)
    if question:
        g.add(label(question, font_size=30, color=GREY_A))
    g.arrange(DOWN, buff=0.3).shift(UP * 0.6)
    strip = timeline(lit=lit).to_edge(DOWN, buff=0.9)
    return VGroup(g, strip)


# ---------------------------------------------------------------------------
# The scoreboard
# ---------------------------------------------------------------------------
KIND_COLOR = {"baseline": GREY_B, "count": C.COUNTING, "compressor": C.COMPRESSOR, "lm": C.NEURAL,
              "human": C.HUMAN}


def scoreboard(rows: list[dict], shown: int | None = None, highlight=(), max_bits=8.0, bar_width=6.4,
               row_h=0.42, font_size=22, label_width=4.4, title=True) -> VGroup:
    """One row per model: its name, a bar as long as its bits per character, and the number.  ``rows`` are dicts
    with ``label``, ``bits`` and ``kind`` (baseline, count, compressor, lm, human); a human row may give ``lo`` and
    ``hi`` instead of ``bits`` and is drawn as a band, and a row with neither is one a later part will fill (a dim
    question mark).  Only the first ``shown`` rows are filled (the rest are dim placeholders).  Returns a VGroup with ``.rows`` (each with ``.name``, ``.bar``, ``.value``) and ``.axis``."""
    shown = len(rows) if shown is None else shown
    x0 = -bar_width / 2 + label_width / 2 + 0.3
    scale = bar_width / max_bits
    g = VGroup()
    out = VGroup()
    for i, r in enumerate(rows):
        y = -i * row_h
        on = i < shown
        color = KIND_COLOR.get(r.get("kind", "count"), WHITE)
        name = label(r["label"], font_size=font_size, color=(WHITE if on else GREY_D))
        if name.width > label_width:
            name.width = label_width
        name.move_to([x0 - 0.25 - name.width / 2, y, 0])
        if "bits" not in r and "lo" not in r:  # a row a later part will fill: its name and a question mark
            bar = VectorizedPoint([x0, y, 0])
            value = MathTex(r"?", font_size=font_size + 2, color=GREY_D).move_to([x0 + 0.25, y, 0])
        elif "bits" in r:
            w = max(r["bits"] * scale, 0.02)
            bar = Rectangle(width=w, height=row_h * 0.62, stroke_width=0, fill_color=color,
                            fill_opacity=0.9 if on else 0.0).move_to([x0 + w / 2, y, 0])
            value = MathTex(f"{r['bits']:.2f}", font_size=font_size + 2, color=(color if on else GREY_D))
            value.next_to(bar, RIGHT, buff=0.15)
        else:
            a, b = r["lo"] * scale, r["hi"] * scale
            bar = Rectangle(width=b - a, height=row_h * 0.62, stroke_width=2, stroke_color=color,
                            fill_color=color, fill_opacity=0.35 if on else 0.0)
            bar.move_to([x0 + (a + b) / 2, y, 0])
            if not on:
                bar.set_stroke(opacity=0)
            value = MathTex(f"{r['lo']:.1f}\\text{{--}}{r['hi']:.1f}", font_size=font_size + 2,
                            color=(color if on else GREY_D)).next_to(bar, RIGHT, buff=0.15)
        if not on:
            value.set_opacity(0)
        row = VGroup(name, bar, value)
        row.name, row.bar, row.value, row.data = name, bar, value, r
        if i in highlight:
            hl = Rectangle(width=label_width + bar_width + 1.6, height=row_h * 0.95, stroke_width=0,
                           fill_color=C.BITS, fill_opacity=0.10).move_to([x0 + (bar_width - label_width) / 2 + 0.3, y, 0])
            row.add_to_back(hl)
        out.add(row)
    top = 0.45
    bottom = -(len(rows) - 1) * row_h - 0.35
    axis = VGroup(Line([x0, top, 0], [x0, bottom, 0], color=GREY_C, stroke_width=1.5))
    for b in range(0, int(max_bits) + 1, 2):
        x = x0 + b * scale
        axis.add(Line([x, bottom, 0], [x, bottom - 0.08, 0], color=GREY_C, stroke_width=1.5))
        axis.add(MathTex(str(b), font_size=20, color=GREY_B).move_to([x, bottom - 0.28, 0]))
    unit = label(r"bits per character", font_size=20, color=GREY_B)
    unit.move_to([x0 + bar_width / 2, bottom - 0.65, 0])
    axis.add(unit)
    g.add(axis, out)
    g.rows, g.axis, g.unit = out, axis, unit
    g.x0, g.unit_len = x0, scale  # x of 0 bits, and the length of one bit
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# Payoffs and references
# ---------------------------------------------------------------------------
def payoff_card(items, font_size=24, title=r"Where this comes back") -> VGroup:
    """``items``: (idea, [part numbers]).  Each row: the idea, an arrow, the parts that use it (by number and name)."""
    head = label(title, font_size=font_size + 12)
    rows = VGroup()
    for idea, parts in items:
        left = label(idea, font_size=font_size, color=C.BITS)
        right = label(r",\ ".join(rf"{p}\ \textit{{{PARTS[p]}}}" for p in parts), font_size=font_size - 2, color=GREY_A)
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


def reference_card(books, papers, font_size=21, width=13.2) -> VGroup:
    """Two blocks: the books (each a Tex line) and the papers, left-aligned, wrapped to ``width``."""
    bh = label(r"Books", font_size=font_size + 7, color=GREY_A)
    ph = label(r"Papers", font_size=font_size + 7, color=GREY_A)
    bl = VGroup(*[wrapped_label(b, width - 0.4, font_size) for b in books]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    pl = VGroup(*[wrapped_label(p, width - 0.4, font_size - 1, GREY_A) for p in papers]).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.1)
    g = VGroup(bh, bl, ph, pl).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    g[2].shift(DOWN * 0.15)
    g[3].shift(DOWN * 0.15)
    if g.height > 7.4:
        g.height = 7.4
    return g.move_to(ORIGIN)


def cite(text: str, corner=DL, font_size=20) -> Tex:
    """A source line in a corner of the frame, e.g. ``cite(r"Shannon (1948)")``."""
    return note(text, font_size=font_size).to_corner(corner, buff=0.3)


def gloss(term: str, plain: str, picture: Mobject | None = None, corner=DR, width: float = 4.6,
          color=None) -> VGroup:
    """A jargon card for a term's first appearance: the term, what it means in plain words, and a small picture of
    it (any mobject, scaled to fit). Put it in a free corner, FadeIn when the narration names the term."""
    color = color or C.BITS
    t = label(term, font_size=24, color=color)
    p = label(plain, font_size=18, color=GREY_A)
    body = VGroup(t, p).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    if picture is not None:
        pic = picture.copy() if hasattr(picture, "copy") else picture
        if pic.width > max(width - 0.4, VGroup(t, p).width):
            pic.scale_to_fit_width(max(width - 0.4, VGroup(t, p).width))
        if pic.height > 1.6:
            pic.scale_to_fit_height(1.6)
        body.add(pic)
        body.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        pic.set_x(body.get_x())
    if body.width > 6.6:  # the box grows to the text rather than shrinking it, up to about half the frame
        body.scale_to_fit_width(6.6)
    box = RoundedRectangle(width=max(body.width + 0.36, 2.0), height=body.height + 0.3, corner_radius=0.12,
                           stroke_color=color, stroke_width=1.5, fill_color="#0B0F17", fill_opacity=0.92)
    card = VGroup(box, body.move_to(box))
    return card.to_corner(corner, buff=0.3)
