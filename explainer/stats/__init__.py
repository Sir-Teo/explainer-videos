"""Shared instruments for *Statistics, Built* (videos/stats/stats1 ... stats65), a degree from a first course to a PhD.

    from explainer.stats import *

The text helpers, derivation ladder and lecture cards are the other two series' (``explainer.analysis``,
``explainer.ai``), so all three typeset alike and share the Chinese on-screen text machinery (with this series' own
table, ``videos/stats/stats_text_zh.json``).  Here, the devices that hold this series together
(videos/stats/README.md, "The devices"):

* the colours, :data:`S` (``explainer.stats.style``): theta gold, theta-hat blue, the null grey, ...;
* :func:`chapter_card` with the **timeline strip**, 1650-2030, from Graunt to e-values;
* :func:`series_map` (the five stages and sixty-five parts) and :func:`transcript_card` (the degree so far);
* :func:`upgrade_card`, the Spiral: an earlier statement, what it assumed, and what this part proves;
* :func:`payoff_card`, "where this comes back", over this series' parts;
* tags: :func:`simulated_tag` (the World), :func:`historical_tag` (the Museum, with its source);
* the World (:mod:`explainer.stats.world`), the Coverage Board (:mod:`explainer.stats.board`), the Museum
  (:mod:`explainer.stats.museum`) and the statistics instruments (:mod:`explainer.stats.viz`).
"""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F401,F403
from explainer.ai import zh  # noqa: F401
from explainer.analysis import label, note, wrapped_label  # noqa: F401
from explainer.stats.style import S  # noqa: F401

SERIES_EN = "Statistics, Built"
SERIES_ZH = "统计学，从零搭建"

# ---------------------------------------------------------------------------
# The degree: five stages, sixty-five parts
# ---------------------------------------------------------------------------
STAGES = [
    (r"I.\ Bachelor's: Foundations", (1, 10)),
    (r"II.\ Bachelor's: Methods", (11, 20)),
    (r"III.\ Master's", (21, 42)),
    (r"IV.\ PhD Core", (43, 55)),
    (r"V.\ PhD Research", (56, 65)),
]
PARTS = {
    1: r"The Shape of Data", 2: r"Chance, Counted", 3: r"The Family of Distributions", 4: r"Matrices for Statistics",
    5: r"Many Variables at Once", 6: r"The Laws of Averages", 7: r"Randomness on Demand",
    8: r"From Sample to Population", 9: r"Estimation", 10: r"Significance",
    11: r"Honest Intervals", 12: r"Least Squares", 13: r"Experiments by Design", 14: r"Counts and Categories",
    15: r"First Bayes", 16: r"Without Assumptions", 17: r"Time Series", 18: r"Who Did You Ask?",
    19: r"Learning from Data", 20: r"The Analysis",
    21: r"Optimization for Statistics", 22: r"Likelihood in Depth", 23: r"The Linear Model in Depth",
    24: r"Generalized Linear Models", 25: r"Borrowing Strength", 26: r"Bayesian Data Analysis",
    27: r"Bayesian Computation", 28: r"Which Model?", 29: r"Smoothing", 30: r"Robust Statistics",
    31: r"Multivariate Analysis", 32: r"Sparsity", 33: r"Thousands of Questions", 34: r"Prediction with Guarantees",
    35: r"What If?", 36: r"Causes Without Experiments", 37: r"Natural Experiments", 38: r"Time Series in Depth",
    39: r"Space", 40: r"Time to Event", 41: r"What You Didn't See", 42: r"The Comprehensive Exam",
    43: r"Measure-Theoretic Probability", 44: r"Martingales and Brownian Motion", 45: r"The Theory of Estimation",
    46: r"The Theory of Testing", 47: r"Asymptotic Statistics", 48: r"Empirical Processes",
    49: r"Semiparametric Efficiency", 50: r"Minimax Theory", 51: r"High-Dimensional Probability",
    52: r"High-Dimensional Statistics", 53: r"Bayesian Asymptotics", 54: r"Statistical Learning Theory",
    55: r"The Qualifying Exam",
    56: r"Inference After Selection", 57: r"Distribution-Free Inference", 58: r"Anytime-Valid Inference",
    59: r"High-Dimensional Asymptotics", 60: r"Robustness and Shift", 61: r"Optimal Transport",
    62: r"Frontiers of Causal Inference", 63: r"Privacy and Fairness", 64: r"Statistics in the Age of AI",
    65: r"The Dissertation",
}
MILESTONES = {20: r"BSc", 42: r"MSc", 55: r"candidacy", 65: r"PhD"}


def stage_of(part: int) -> int:
    for i, (_, (a, b)) in enumerate(STAGES):
        if a <= part <= b:
            return i
    raise ValueError(part)


def series_map(current: int | None = None, done: int = 0, font_size=15, width=13.4, height=7.2) -> VGroup:
    """The five stages as five columns, each part a row; done parts white, ``current`` lit and boxed, the rest dim,
    milestones marked with a small diamond."""
    cols = VGroup()
    for name, (a, b) in STAGES:
        head = label(name, font_size=font_size + 3, color=S.ACCENT if a <= (current or 0) <= b else GREY_A)
        rows = VGroup()
        for p in range(a, b + 1):
            color = S.ACCENT if p == current else (WHITE if p <= done else GREY_C)
            t = label(rf"{p}.\ {PARTS[p]}", font_size=font_size, color=color)
            if p in MILESTONES:
                d = Square(0.09, stroke_width=0, fill_color=S.ACCENT, fill_opacity=1).rotate(PI / 4)
                t = VGroup(t, d.next_to(t, RIGHT, buff=0.1))
            rows.add(t)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        col = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        col.head, col.rows = head, rows
        cols.add(col)
    cols.arrange(RIGHT, aligned_edge=UP, buff=0.35)
    if cols.width > width:
        cols.width = width
    if cols.height > height:
        cols.height = height
    g = VGroup(cols)
    g.cols, g.part = cols, {}
    for col, (_, (a, b)) in zip(cols, STAGES):
        for p, row in zip(range(a, b + 1), col.rows):
            g.part[p] = row
    if current is not None:
        g.box = SurroundingRectangle(g.part[current], color=S.ACCENT, buff=0.06, corner_radius=0.05, stroke_width=2)
        g.add(g.box)
    return g.move_to(ORIGIN)


def transcript_card(done: int, current: int | None = None, width=12.6) -> VGroup:
    """The degree's transcript: one cell per part along five stage bars; finished parts filled, the current one lit,
    the four milestones (BSc, MSc, candidacy, PhD) labelled under their cells."""
    n = len(PARTS)
    cell = width / n
    g = VGroup()
    title = label(r"Transcript", font_size=30, color=GREY_A)
    cells, stage_labels, marks = VGroup(), VGroup(), VGroup()
    x0 = -width / 2
    for p in range(1, n + 1):
        x = x0 + (p - 0.5) * cell
        on = p <= done
        color = S.ACCENT if p == current else (WHITE if on else GREY_D)
        r = Rectangle(width=cell * 0.82, height=0.42, stroke_color=color, stroke_width=1.2,
                      fill_color=color, fill_opacity=0.85 if (on or p == current) else 0.0).move_to([x, 0, 0])
        cells.add(r)
        if p in MILESTONES:
            m = label(MILESTONES[p], font_size=17, color=S.ACCENT if p <= done else GREY_B)
            m.next_to(r, DOWN, buff=0.2)
            tick = Line(r.get_bottom(), r.get_bottom() + DOWN * 0.12, color=GREY_B, stroke_width=1.5)
            marks.add(VGroup(tick, m))
    for name, (a, b) in STAGES:
        left, right = cells[a - 1].get_left()[0], cells[b - 1].get_right()[0]
        br = Line([left, 0.36, 0], [right, 0.36, 0], color=GREY_B, stroke_width=1.5)
        t = label(name.split(r".\ ")[1], font_size=16, color=GREY_A).next_to(br, UP, buff=0.1)
        if t.width > right - left - 0.05:
            t.width = right - left - 0.05
        stage_labels.add(VGroup(br, t))
    body = VGroup(stage_labels, cells, marks)
    g.add(title, body)
    title.next_to(body, UP, buff=0.35)
    g.cells, g.marks, g.title = cells, marks, title
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# The timeline strip, 1650-2030
# ---------------------------------------------------------------------------
TIMELINE = [
    (1654, r"Pascal and Fermat"),
    (1662, r"Graunt's \emph{Bills}"),
    (1693, r"Halley's life table"),
    (1710, r"Arbuthnot's test"),
    (1713, r"Bernoulli's law"),
    (1733, r"de Moivre's curve"),
    (1738, r"St Petersburg"),
    (1763, r"Bayes"),
    (1774, r"Laplace's inverse probability"),
    (1777, r"Buffon's needle"),
    (1786, r"Playfair's charts"),
    (1802, r"Laplace's census"),
    (1801, r"Ceres"),
    (1805, r"least squares"),
    (1821, r"Gauss--Markov"),
    (1810, r"Laplace's CLT"),
    (1835, r"Quetelet's average man"),
    (1858, r"Nightingale's rose"),
    (1867, r"Chebyshev's inequality"),
    (1869, r"Minard's map"),
    (1882, r"Newcomb's speed of light"),
    (1884, r"Peirce and Jastrow"),
    (1886, r"Galton's regression"),
    (1889, r"Bertrand's paradox"),
    (1898, r"the law of small numbers"),
    (1901, r"Pearson's principal axes"),
    (1904, r"Spearman's $g$"),
    (1894, r"Pearson's moments"),
    (1900, r"Pearson's $\chi^2$"),
    (1907, r"vox populi"),
    (1908, r"Student's $t$"),
    (1915, r"Fisher's geometry"),
    (1918, r"variance components"),
    (1919, r"Fisher at Rothamsted"),
    (1922, r"Fisher's likelihood"),
    (1926, r"nonsense correlations; Sturges's rule"),
    (1927, r"Wilson's interval"),
    (1928, r"extreme values; Wishart"),
    (1929, r"Hubble's law"),
    (1931, r"de Finetti's theorem; Hotelling's $T^2$"),
    (1933, r"Neyman--Pearson; Kolmogorov; principal components"),
    (1934, r"Cochran; Neyman's sampling"),
    (1936, r"the \emph{Literary Digest}; Fisher's irises; Mahalanobis; canonical correlation"),
    (1935, r"Fisher's \emph{Design}; Aitken's GLS; Bliss's probits"),
    (1937, r"confidence intervals"),
    (1939, r"Jeffreys's \emph{Theory}; Dantzig's homework"),
    (1943, r"the German tanks"),
    (1945, r"sequential tests; ranks; Rao's metric"),
    (1946, r"Cram\'er--Rao; Jeffreys's prior"),
    (1947, r"Mann--Whitney; the simplex"),
    (1948, r"Neyman--Scott"),
    (1949, r"Lehmer's generator; Wald's consistency"),
    (1950, r"Doll and Hill"),
    (1951, r"a state of sin; Robbins--Monro"),
    (1952, r"classical scaling"),
    (1953, r"MCMC"),
    (1956, r"Stein's paradox; Robbins's empirical Bayes; kernel densities"),
    (1957, r"Lindley's paradox; Lloyd's $k$-means"),
    (1958, r"Kaplan--Meier"),
    (1959, r"Mantel--Haenszel"),
    (1960, r"the Kalman filter; Tukey's contamination"),
    (1961, r"James--Stein; the curse of dimensionality"),
    (1962, r"the likelihood principle"),
    (1963, r"Hodges--Lehmann"),
    (1964, r"the \emph{Federalist} decided; Nadaraya--Watson; Huber"),
    (1970, r"Box--Jenkins; Hastings; the representer theorem; ridge"),
    (1971, r"NHANES; REML; breakdown"),
    (1967, r"Huber's sandwich; Longley; Reinsch's spline; Marchenko--Pastur"),
    (1972, r"Cox; GLMs"),
    (1973, r"Anscombe's quartet; the Dirichlet process; AIC"),
    (1974, r"Rubin's causal model; cross-validation; influence functions; the Shepp--Logan phantom"),
    (1975, r"Berkeley admissions; pseudo-likelihood; Efron--Morris"),
    (1977, r"Tukey's \emph{EDA}; EM"),
    (1978, r"quantile regression; Hausman; BIC; MDL"),
    (1979, r"the bootstrap; Fay--Herriot; GCV; LOESS"),
    (1980, r"White's robust SEs; proportional odds"),
    (1981, r"the eight schools; Silverman's mode test"),
    (1982, r"the M-competition; Laird--Ware"),
    (1983, r"Freedman's paradox"),
    (1984, r"separation; predictive checks; prequential"),
    (1986, r"Challenger; Moulton's factor; GEE; optimism"),
    (1987, r"Hamiltonian Monte Carlo"),
    (1988, r"INTERSALT"),
    (1990, r"the Gibbs sampler; GAMs"),
    (1994, r"wavelet shrinkage"),
    (1991, r"Sheather--Jones"),
    (1992, r"seven shuffles; zero inflation"),
    (1993, r"Firth's correction; particle filters"),
    (1995, r"false discovery rate; Bayes factors"),
    (1996, r"the lasso; coupling from the past; Bai--Saranadasa"),
    (1999, r"variational inference; BMA"),
    (2001, r"the two cultures; SCAD"),
    (2002, r"selection bias in CV; ABC"),
    (2003, r"Neal's funnel"),
    (2004, r"least angle regression"),
    (2005, r"conformal prediction; the elastic net"),
    (2006, r"weakly informative priors; compressed sensing"),
    (2007, r"proper scoring rules"),
    (2008, r"the wild cluster bootstrap; the graphical lasso"),
    (2009, r"FISTA; INLA; singular learning theory"),
    (2010, r"WAIC; the horseshoe; MCP; SoftImpute"),
    (2013, r"CUPED; PoSI"),
    (2014, r"NUTS; the debiased lasso; double selection"),
    (2016, r"the ASA on $p$-values"),
    (2017, r"same stats, different graphs; Stan"),
    (2018, r"double machine learning; robust bias correction"),
    (2019, r"models as approximations"),
    (2020, r"Bayesian workflow; best subset vs lasso"),
    (2023, r"e-values; PPI"),
]
T0, T1 = 1650, 2030


def timeline(lit=(), width=12.0, show_labels=True, font_size=18) -> VGroup:
    """The strip from 1650 to 2030; years in ``lit`` glow and get their names (kept apart and inside the frame,
    a faint leader tying each displaced label to its year)."""
    x0 = -width / 2

    def X(y):
        return x0 + width * (y - T0) / (T1 - T0)

    g = VGroup(Line([X(T0), 0, 0], [X(T1), 0, 0], color=GREY_D, stroke_width=2))
    for yr in (1700, 1800, 1900, 2000):
        g.add(Line([X(yr), -0.06, 0], [X(yr), 0.06, 0], color=GREY_D, stroke_width=1.5))
        g.add(Text(str(yr), font_size=14, color=GREY_D).next_to([X(yr), 0, 0], DOWN, buff=0.12))
    labels, anchors, side = VGroup(), [], 1
    for yr, name in TIMELINE:
        on = yr in lit
        d = Dot([X(yr), 0, 0], radius=0.065 if on else 0.035, color=S.ACCENT if on else GREY_C)
        g.add(d)
        if on and show_labels:
            t = label(rf"{yr}\; {name}", font_size=font_size, color=S.ACCENT)
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
                             color=S.ACCENT, stroke_width=1, stroke_opacity=0.4))
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
        g.add(wrapped_label(question, 11.5, font_size=30, color=GREY_A))
    g.arrange(DOWN, buff=0.3).shift(UP * 0.6)
    strip = timeline(lit=lit).to_edge(DOWN, buff=0.9)
    return VGroup(g, strip)


# ---------------------------------------------------------------------------
# The Spiral, payoffs, tags
# ---------------------------------------------------------------------------
def upgrade_card(part: int, said: str, assumed: str, now: str, width=9.6, font_size=24) -> VGroup:
    """The Spiral: what Part ``part`` said, what it quietly assumed, and what this part will prove."""
    rows = VGroup()
    for tag, body, color in ((rf"Part {part} said", said, GREY_A), (r"It assumed", assumed, S.RESID),
                             (r"Now", now, S.ACCENT)):
        t = label(tag, font_size=font_size - 4, color=color)
        b = wrapped_label(body, width - 2.6, font_size, WHITE)
        rows.add(VGroup(t, b))
    tw = max(r[0].width for r in rows)
    for r in rows:
        r[1].next_to(r[0], RIGHT, buff=0.35).align_to(r[0], UP)
        r[0].shift(LEFT * (tw - r[0].width) * 0)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    for r in rows:
        r[1].set_x(rows.get_left()[0] + tw + 0.35 + r[1].width / 2)
    head = label(r"Upgrade", font_size=font_size - 2, color=S.ACCENT)
    inner = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    box = RoundedRectangle(width=max(width, inner.width + 0.6), height=inner.height + 0.6, corner_radius=0.14,
                           stroke_color=S.ACCENT, stroke_width=1.8, fill_color="#0B0F17", fill_opacity=0.94)
    inner.move_to(box)
    return VGroup(box, inner)


def payoff_card(items, font_size=24, title=r"Where this comes back") -> VGroup:
    """``items``: (idea, [part numbers]).  Each row: the idea, an arrow, the parts that use it (number and name)."""
    head = label(title, font_size=font_size + 12)
    rows = VGroup()
    for idea, parts in items:
        left = label(idea, font_size=font_size, color=S.ACCENT)
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


def simulated_tag(text=r"simulated: the World", corner=DR) -> Tex:
    """The World's tag: every number drawn from the simulated population says so."""
    return note(text, color=S.WORLD).to_corner(corner, buff=0.3)


def historical_tag(source: str, corner=DL) -> Tex:
    """The Museum's tag: historical data, with its source."""
    return note(rf"historical data: {source}", color=S.MUSEUM).to_corner(corner, buff=0.3)


from explainer.stats.viz import *  # noqa: E402,F401,F403
from explainer.stats.board import Row, coverage_board, load_all, save_rows, verdict  # noqa: E402,F401
