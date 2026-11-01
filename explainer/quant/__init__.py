"""Shared instruments for *Quant, Built* (videos/quant/quant1 ... quant43).

    from explainer.quant import *

Everything *AI, Built* exports (``explainer.ai``: the lecture cards, ``cmath``/``morph``, ``LiveBars``,
``glow_dot``, ``axes``/``curve``/``band``, camera framing, ``payoff_card``-style set pieces) and the analysis series'
text helpers (``label``, ``note``, ``why``, ``ladder``, ``wrapped_label``) come with it, so the three series typeset
alike and share the Chinese on-screen-text machinery (``explainer/zh_text.py``, this series' table
``videos/quant/quant_text_zh.json``).  This module adds the devices of this series (videos/quant/SYLLABUS.md):

* :data:`ACTS`, :data:`PARTS` and :func:`series_map`: the forty-three parts in seven acts and a finale;
* the **timeline strip** (:func:`timeline`, 1900-2030): ideas in gold, crises in red, firms in blue;
* :func:`chapter_card` with that strip;
* the per-part set pieces :func:`crisis_card`, :func:`firm_card` and :func:`desk_question`;
* :func:`house_chart`, the org chart of **the House**, the series' own quant firm, with the desks built so far;
* :func:`payoff_card` over this series' parts ("where this comes back").

The visual instruments that draw finance (surfaces, path fans, the hedging ledger) are in :mod:`explainer.quant.viz`
and are exported here too; the series' library, the House, is :mod:`explainer.quant.house` (imported explicitly).
"""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F401,F403
from explainer.ai import zh  # noqa: F401
from explainer.ai.lecture import _card, _body  # noqa: F401
from explainer.analysis import label, note, wrapped_label  # noqa: F401
from explainer.style import QC  # noqa: F401
from explainer.quant.viz import *  # noqa: F401,F403,E402

SERIES_EN = "Quant, Built"
SERIES_ZH = "量化金融，从零搭建"
DISCLAIMER = r"An education in methods, not investment advice."

# ---------------------------------------------------------------------------
# The forty-three parts
# ---------------------------------------------------------------------------
ACTS = [
    (r"I.\ Markets and Money", (1, 3)),
    (r"II.\ The Toolkit", (4, 8)),
    (r"III.\ Derivatives (Q)", (9, 22)),
    (r"IV.\ Return Premia (P)", (23, 29)),
    (r"V.\ Portfolios and the Firm", (30, 34)),
    (r"VI.\ Microstructure", (35, 39)),
    (r"VII.\ The System", (40, 42)),
    (r"Finale", (43, 43)),
]
PARTS = {
    1: r"The Fair Game", 2: r"The Machinery of Markets", 3: r"Value, Accounting and the Firm",
    4: r"Martingales and Measure", 5: r"Stochastic Calculus", 6: r"Financial Econometrics",
    7: r"Time Series and Volatility", 8: r"Decisions and Control",
    9: r"No Arbitrage", 10: r"Black--Scholes--Merton", 11: r"Trading Options", 12: r"The Volatility Surface",
    13: r"Stochastic Volatility and Jumps", 14: r"Rough and Path-Dependent Volatility",
    15: r"Exotics and Structured Products", 16: r"Computing Prices", 17: r"Deep Pricing and Hedging",
    18: r"Money, Bonds and the Curve", 19: r"Term-Structure Models", 20: r"Credit",
    21: r"Counterparty Risk, XVA and Clearing", 22: r"FX, Commodities and the Basis",
    23: r"Risk and Return", 24: r"Factors", 25: r"The Factor Zoo", 26: r"Backtesting Without Fooling Yourself",
    27: r"Machine Learning for Returns", 28: r"Text, LLMs and Alternative Data",
    29: r"Alpha Mining and Automated Research",
    30: r"Portfolio Construction", 31: r"Risk Models, Costs and Trading Through Time",
    32: r"Systematic Macro and Alternative Premia", 33: r"Statistical Arbitrage", 34: r"Inside a Quant Firm",
    35: r"Who Trades With Whom", 36: r"The Limit Order Book", 37: r"Market Impact and Execution",
    38: r"Market Making, ETFs and the Speed Race", 39: r"Crypto and DeFi",
    40: r"Measuring Risk", 41: r"Leverage, Liquidity and Crises", 42: r"Machines in the Market",
    43: r"Can You Beat the Market?",
}
assert sorted(PARTS) == list(range(1, 44)) and sum(b - a + 1 for _, (a, b) in ACTS) == 43

# columns of the series map: the acts stacked so the columns come out about the same height
_MAP_COLUMNS = [(0, 1), (2,), (3, 4), (5, 6, 7)]


def series_map(current: int | None = None, done: int = 0, font_size=17, width=13.4, height=7.4) -> VGroup:
    """The seven acts and the finale in four columns; each part a row.  Parts up to ``done`` are white, ``current``
    is lit and boxed, the rest are dim.  ``g.part[p]`` is part p's row."""
    cols = VGroup()
    g = VGroup()
    g.part = {}
    for col_acts in _MAP_COLUMNS:
        col = VGroup()
        for ai in col_acts:
            act, (a, b) = ACTS[ai]
            head = label(act, font_size=font_size + 3, color=GREY_A)
            rows = VGroup()
            for p in range(a, b + 1):
                color = QC.IDEA if p == current else (WHITE if p <= done else GREY_C)
                row = label(rf"{p}.\ {PARTS[p]}", font_size=font_size, color=color)
                rows.add(row)
                g.part[p] = row
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
            col.add(VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18))
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        cols.add(col)
    cols.arrange(RIGHT, aligned_edge=UP, buff=0.55)
    if cols.width > width:
        cols.width = width
    if cols.height > height:
        cols.height = height
    g.add(cols)
    g.cols = cols
    if current is not None:
        box = SurroundingRectangle(g.part[current], color=QC.IDEA, buff=0.08, corner_radius=0.06, stroke_width=2)
        g.add(box)
        g.box = box
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# The timeline strip: ideas, crises, firms
# ---------------------------------------------------------------------------
IDEA, CRISIS, FIRM = "idea", "crisis", "firm"
TIMELINE = [
    (1900, r"Bachelier: \textit{Th\'eorie de la sp\'eculation}", IDEA),
    (1923, r"Wiener: Brownian motion", IDEA),
    (1929, r"the Crash", CRISIS),
    (1933, r"Cowles: can forecasters forecast?", IDEA),
    (1938, r"Macaulay: duration", IDEA),
    (1944, r"It\^o's stochastic integral", IDEA),
    (1952, r"Markowitz: portfolio selection", IDEA),
    (1956, r"Kelly's criterion", IDEA),
    (1958, r"Modigliani--Miller", IDEA),
    (1962, r"Thorp: \textit{Beat the Dealer}", IDEA),
    (1963, r"Mandelbrot: cotton prices", IDEA),
    (1964, r"Sharpe: the CAPM", IDEA),
    (1965, r"Samuelson: fair prices are random", IDEA),
    (1967, r"Thorp--Kassouf: \textit{Beat the Market}", IDEA),
    (1969, r"Merton's portfolio problem; Thorp's fund", IDEA),
    (1970, r"Fama: efficient markets", IDEA),
    (1973, r"Black--Scholes--Merton; the CBOE opens", IDEA),
    (1974, r"Merton: credit as an option", IDEA),
    (1976, r"Ross: arbitrage pricing", IDEA),
    (1977, r"Vasicek: the short rate", IDEA),
    (1979, r"binomial trees; Harrison--Kreps", IDEA),
    (1980, r"Grossman--Stiglitz", IDEA),
    (1981, r"Harrison--Pliska", IDEA),
    (1982, r"Engle: ARCH; Renaissance founded", FIRM),
    (1985, r"Kyle; Glosten--Milgrom; Leland", IDEA),
    (1987, r"Black Monday", CRISIS),
    (1988, r"D.\ E.\ Shaw founded", FIRM),
    (1990, r"Citadel founded", FIRM),
    (1992, r"Fama--French; HJM; Black Wednesday", IDEA),
    (1993, r"Heston; momentum", IDEA),
    (1994, r"Dupire; RiskMetrics; the bond massacre", IDEA),
    (1995, r"Barings", CRISIS),
    (1997, r"the Nobel; the LIBOR market model", IDEA),
    (1998, r"LTCM", CRISIS),
    (1999, r"coherent risk measures", IDEA),
    (2000, r"Jane Street founded; Almgren--Chriss; Li's copula", FIRM),
    (2001, r"Two Sigma founded; Longstaff--Schwartz", FIRM),
    (2002, r"SABR", IDEA),
    (2004, r"SVI; adaptive markets", IDEA),
    (2005, r"Reg NMS", IDEA),
    (2006, r"Amaranth", CRISIS),
    (2007, r"the quant quake", CRISIS),
    (2008, r"Lehman; the financial crisis", CRISIS),
    (2009, r"the momentum crash", CRISIS),
    (2010, r"the flash crash", CRISIS),
    (2012, r"Knight Capital; the London Whale", CRISIS),
    (2014, r"deflated Sharpe; SSVI", IDEA),
    (2015, r"the Swiss franc; China's crash", CRISIS),
    (2016, r"rough Bergomi; the factor zoo", IDEA),
    (2018, r"volatility is rough; Volmageddon", CRISIS),
    (2019, r"deep hedging; DeepLOB", IDEA),
    (2020, r"negative oil; the dash for cash", CRISIS),
    (2021, r"GameStop; Archegos", CRISIS),
    (2022, r"Terra; FTX; the gilt crisis", CRISIS),
    (2023, r"SVB", CRISIS),
    (2024, r"snowballs; the yen carry unwind", CRISIS),
    (2025, r"AI asset pricing models", IDEA),
]
T0, T1 = 1900, 2030
KIND_COLOR = {IDEA: QC.IDEA, CRISIS: QC.CRISIS, FIRM: QC.FIRM}
_YEARS = {y for y, _, _ in TIMELINE}


def timeline(lit=(), width=12.4, show_labels=True, font_size=17) -> VGroup:
    """The strip from 1900 to 2030.  Every milestone is a small dot in its kind's colour (dim); years in ``lit``
    glow and get their names, alternating above and below the line."""
    unknown = set(lit) - _YEARS
    if unknown:
        raise KeyError(f"timeline years not in TIMELINE: {sorted(unknown)}")
    x0 = -width / 2

    def X(y):
        return x0 + width * (y - T0) / (T1 - T0)

    g = VGroup(Line([X(T0), 0, 0], [X(T1), 0, 0], color=GREY_D, stroke_width=2))
    for yr in range(1900, 2031, 20):
        g.add(Line([X(yr), -0.06, 0], [X(yr), 0.06, 0], color=GREY_D, stroke_width=1.5))
        g.add(Text(str(yr), font_size=13, color=GREY_D).next_to([X(yr), 0, 0], DOWN, buff=0.12))
    labels, leaders = VGroup(), VGroup()
    side = 1
    for yr, name, kind in TIMELINE:
        on = yr in lit
        col = KIND_COLOR[kind]
        d = Dot([X(yr), 0, 0], radius=0.07 if on else 0.035, color=col if on else interpolate_color(
            ManimColor(col), ManimColor(BACKGROUND), 0.55))
        g.add(d)
        if on:
            g.add(glow_dot(d.get_center(), color=col, radius=0.06, opacity=0.4))
        if on and show_labels:
            t = label(rf"{yr}\; {name}", font_size=font_size, color=col)
            t.next_to(d, UP if side > 0 else DOWN, buff=0.16 if side > 0 else 0.42)
            side = -side
            labels.add(t)
    for row in (1, -1):  # keep the lit labels apart and inside the frame
        same = sorted([t for t in labels if np.sign(t.get_y()) == row], key=lambda t: t.get_x())
        for a, b in zip(same, same[1:]):
            gap = b.get_left()[0] - a.get_right()[0]
            if gap < 0.2:
                b.shift(RIGHT * (0.2 - gap))
        for t in same:
            keep_in_frame(t, margin=0.25)
    for t in labels:
        yr = int(t.tex_string.split("\\;")[0])
        dot = np.array([X(yr), 0, 0])
        above = t.get_y() > 0
        leaders.add(Line(dot + (UP if above else DOWN) * 0.08, t.get_bottom() if above else t.get_top(),
                         color=GREY_C, stroke_width=1, stroke_opacity=0.5))
    g.add(leaders, labels)
    g.labels, g.leaders = labels, leaders
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
    g.arrange(DOWN, buff=0.3).shift(UP * 0.7)
    strip = timeline(lit=lit).to_edge(DOWN, buff=1.0)
    return VGroup(g, strip)


def part_title(part: int, subtitle: str = "") -> VGroup:
    """The part's title card: series name, part number and title, and an optional subtitle."""
    s = label(SERIES_ZH if zh() else SERIES_EN, font_size=30, color=QC.HOUSE)
    n = label((rf"第{part}部分" if zh() else rf"Part {part}"), font_size=30, color=GREY_B)
    t = label(PARTS[part], font_size=64)
    g = VGroup(VGroup(s, n).arrange(RIGHT, buff=0.4), t)
    if subtitle:
        g.add(label(subtitle, font_size=30, color=GREY_A))
    return g.arrange(DOWN, buff=0.35)


# ---------------------------------------------------------------------------
# The per-part set pieces: crisis files, firm files, desk questions
# ---------------------------------------------------------------------------
def crisis_card(date: str, name: str, body="", stats=(), width: float = 6.6, font_size=24) -> VGroup:
    """A crisis file: the date in red, the event, a line or two of what happened, and measured numbers as large
    figures with captions (``stats``: (figure, caption) pairs, the figure as math).  ``card.stats`` are the figures."""
    tag = label(r"Crisis file", font_size=font_size - 6, color=QC.CRISIS)
    d = label(date, font_size=font_size - 2, color=GREY_B)
    nm = label(name, font_size=font_size + 8, color=WHITE)
    head = VGroup(VGroup(tag, d).arrange(RIGHT, buff=0.3, aligned_edge=DOWN), nm).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
    parts = VGroup()
    if body:
        parts.add(_body(body, width - 0.8, font_size - 2, GREY_A))
    figs = VGroup()
    for fig, cap in stats:
        f = MathTex(fig, font_size=font_size + 14, color=QC.CRISIS)
        c = wrapped_label(cap, 2.6, font_size - 6, GREY_B)
        figs.add(VGroup(f, c).arrange(DOWN, buff=0.08))
    if len(figs):
        figs.arrange(RIGHT, buff=0.5, aligned_edge=UP)
        if figs.width > width - 0.8:
            figs.width = width - 0.8
        parts.add(figs)
    body_m = parts.arrange(DOWN, aligned_edge=LEFT, buff=0.22) if len(parts) else VectorizedPoint()
    card = _card(head, body_m, QC.CRISIS, width)
    card.stats = figs
    return card


def firm_card(name: str, what: str, numbers=(), source: str = "", width: float = 6.2, font_size=23) -> VGroup:
    """A firm file: the firm, what it does and how it earns, a few disclosed numbers (``numbers``: (figure,
    caption)), and the public source the numbers come from."""
    tag = label(r"Firm file", font_size=font_size - 6, color=QC.FIRM)
    nm = label(name, font_size=font_size + 8, color=WHITE)
    head = VGroup(tag, nm).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    parts = VGroup(_body(what, width - 0.8, font_size - 2, GREY_A))
    figs = VGroup()
    for fig, cap in numbers:
        figs.add(VGroup(MathTex(fig, font_size=font_size + 10, color=QC.FIRM),
                        wrapped_label(cap, 2.4, font_size - 6, GREY_B)).arrange(DOWN, buff=0.08))
    if len(figs):
        figs.arrange(RIGHT, buff=0.45, aligned_edge=UP)
        if figs.width > width - 0.8:
            figs.width = width - 0.8
        parts.add(figs)
    if source:
        parts.add(label(source, font_size=font_size - 8, color=GREY_C))
    parts.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    return _card(head, parts, QC.FIRM, width)


def desk_question(question: str, answer_hint: str = "", width: float = 8.4, font_size=28) -> VGroup:
    """A desk question: an interview-style problem, posed on screen (the full solution is in the part's README).
    Drawn with a small terminal glyph so it reads as the trading desk, not the lecture."""
    color = QC.HOUSE
    glyph = VGroup(RoundedRectangle(width=0.5, height=0.36, corner_radius=0.05, stroke_color=color, stroke_width=2),
                   MathTex(r">\!\_", font_size=20, color=color))
    glyph[1].move_to(glyph[0])
    tag = label(r"Desk question", font_size=font_size - 6, color=color)
    head = VGroup(glyph, tag).arrange(RIGHT, buff=0.2)
    parts = VGroup(_body(question, width - 0.8, font_size))
    if answer_hint:
        parts.add(_body(answer_hint, width - 0.8, font_size - 6, GREY_B))
        parts.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    return _card(head, parts, color, width, accent=False)


# ---------------------------------------------------------------------------
# The House: the series' own quant firm, desk by desk
# ---------------------------------------------------------------------------
DESKS = {  # key: (name, first part that builds it)
    "data": (r"Data \& technology", 1),
    "treasury": (r"Treasury \& funding", 2),
    "vol": (r"Volatility desk", 10),
    "rates": (r"Rates desk", 18),
    "credit": (r"Credit \& XVA", 20),
    "macro": (r"Macro desk", 22),
    "research": (r"Research", 23),
    "portfolio": (r"Portfolio \& risk", 30),
    "compliance": (r"Compliance", 34),
    "execution": (r"Execution", 37),
    "mm": (r"Market making", 38),
    "digital": (r"Digital assets", 39),
}
# the chart's layout: data across the top, the desks that trade in the middle, the control functions below
_HOUSE_ROWS = [("data",), ("vol", "rates", "credit", "macro", "digital"), ("research", "portfolio", "execution", "mm"),
               ("treasury", "compliance")]
_HOUSE_FLOWS = [("research", "portfolio"), ("portfolio", "execution")]


def house_chart(part: int, lit=(), width=12.6, font_size=20) -> VGroup:
    """The House's org chart as of ``part``: desks built by then are filled in the House colour, desks the part
    builds or extends (``lit``) glow, the rest are dashed outlines of what is to come.  ``g.desk[key]`` is a desk's
    box."""
    g = VGroup()
    g.desk = {}
    rows = VGroup()
    for keys in _HOUSE_ROWS:
        row = VGroup()
        n = len(keys)
        bw = (width - 0.3 * (n - 1)) / n if n > 1 else width
        for k in keys:
            name, first = DESKS[k]
            built = first <= part
            on = k in lit
            col = QC.HOUSE if (built or on) else GREY_D
            box = RoundedRectangle(width=bw, height=0.95, corner_radius=0.12, stroke_color=col,
                                   stroke_width=3 if on else 1.6, fill_color=col,
                                   fill_opacity=0.28 if on else (0.12 if built else 0.0))
            if not (built or on):
                box = DashedVMobject(box, num_dashes=60, dashed_ratio=0.5)
            t = label(name, font_size=font_size, color=WHITE if (built or on) else GREY_C)
            if t.width > bw - 0.3:
                t.width = bw - 0.3
            desk = VGroup(box, t.move_to(box))
            if on:
                desk.add_to_back(SurroundingRectangle(box, buff=0.06, corner_radius=0.16, color=QC.HOUSE,
                                                      stroke_width=8, stroke_opacity=0.25))
            g.desk[k] = desk
            row.add(desk)
        row.arrange(RIGHT, buff=0.3)
        rows.add(row)
    rows.arrange(DOWN, buff=0.45)
    g.add(rows)
    flows = VGroup()
    for a, b in _HOUSE_FLOWS:
        flows.add(Arrow(g.desk[a].get_right(), g.desk[b].get_left(), buff=0.04, stroke_width=3, color=GREY_B,
                        max_tip_length_to_length_ratio=0.5, tip_length=0.14))
    g.add(flows)
    title = label(r"The House", font_size=font_size + 12, color=QC.HOUSE).next_to(rows, UP, buff=0.35)
    g.add(title)
    g.rows, g.flows, g.title = rows, flows, title
    return g.move_to(ORIGIN)


def payoff_card(items, font_size=24, title=r"Where this comes back") -> VGroup:
    """``items``: (idea, [part numbers]).  Each row: the idea, an arrow, the parts that use it (number and name)."""
    head = label(title, font_size=font_size + 12)
    rows = VGroup()
    for idea, parts in items:
        left = label(idea, font_size=font_size, color=QC.IDEA)
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
