from __future__ import annotations

import itertools
import math
import random

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


def k_n(n, radius, center, colors=None):
    pts = [np.array([center[0] + radius * math.cos(math.pi / 2 + 2 * math.pi * i / n),
                     center[1] + radius * math.sin(math.pi / 2 + 2 * math.pi * i / n), 0]) for i in range(n)]
    edges = VGroup()
    for i, j in itertools.combinations(range(n), 2):
        c = colors[(i, j)] if colors else GREY_B
        edges.add(Line(pts[i], pts[j], stroke_width=1.6, color=c))
    dots = VGroup(*[Dot(p, radius=0.06, color=WHITE) for p in pts])
    return VGroup(edges, dots), pts


class ProbMethod(VoiceoverScene):
    def construct(self):
        self.card()
        self.ramsey()
        self.table()
        self.lll()

    def card(self):
        card = chapter_card(14, r"The probabilistic method", r"Can you prove something exists without finding it?",
                            lit=(1947, 2010), extra=((1947, r"Erd\H{o}s on Ramsey"), (2010, r"Moser--Tardos")),
                            part=PART)
        with self.voiceover((
            'Chapter fourteen. The probabilistic method.'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ramsey(self):
        d = load("probmethod")
        head = label(r"Colour every edge red or blue", font_size=34).to_edge(UP, buff=0.35)
        rng = random.Random(5)
        n = 17
        qr = {(x * x) % 17 for x in range(1, 17)}
        paley = {(i, j): (DATA if ((j - i) % 17) in qr else NO) for i, j in itertools.combinations(range(n), 2)}
        rand = {(i, j): (DATA if rng.random() < 0.5 else NO) for i, j in itertools.combinations(range(n), 2)}
        g1, _ = k_n(n, 1.7, (-3.4, -0.6), rand)
        g2, _ = k_n(n, 1.7, (3.4, -0.6), paley)
        c1 = label(rf"a random colouring of $K_{{17}}$: \ {d['k4_mean']:.0f} one-colour $K_4$'s on average",
                   font_size=19, color=GREY_A).next_to(g1, DOWN, buff=0.3)
        c2 = label(r"the Paley colouring: \ blue when $j - i$ is a square mod 17: \ none", font_size=19, color=YES
                   ).next_to(g2, DOWN, buff=0.3)
        q = label(r"Ramsey: \ every colouring of a big enough $K_n$ has a one-colour $K_k$. \ How big is big enough?",
                  font_size=21, color=WHITE).next_to(head, DOWN, buff=0.25)
        with self.voiceover(
            (
            f'Colour every edge of a complete graph red or blue. Frank Ramsey proved in 1930 that if the graph is big'
            f" enough, some k vertices have all their edges the same colour, whatever you do. <bookmark mark='a'/> "
            f'With four vertices, seventeen are not enough. On the left, a random colouring of the complete graph on '
            f'seventeen vertices: on average it has '
            f"{d['k4_mean']:.0f}"
            f" groups of four in a single colour. <bookmark mark='b'/> On the right, a clever colouring, blue exactly"
            f' when the difference of the two vertices is a square modulo seventeen, has none at all. Eighteen '
            f"vertices always contain one, so the Ramsey number R of four, four is eighteen. <bookmark mark='c'/> "
            f'Larger diagonal Ramsey numbers pose much harder questions. For growing k, random colorings provide a '
            f'powerful existence proof.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(q))
            vo.wait_until("a")
            self.play(Create(g1[0]), FadeIn(g1[1]), FadeIn(c1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(g2[0]), FadeIn(g2[1]), FadeIn(c2), run_time=2.0)
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        d = load("probmethod")
        head = label(r"Erd\H{o}s (1947): \ count, \ don't construct", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"colour each edge of $K_n$ by a fair coin; \ a given $k$-set is one colour with probability "
                  r"$2 \cdot 2^{-\binom{k}{2}}$", font_size=21, color=WHITE),
            MathTex(r"\mathbb{E}[\#\text{one-colour } K_k] = \binom{n}{k}\, 2^{1 - \binom{k}{2}} < 1 "
                    r"\quad\Longrightarrow\quad \text{some colouring has none}", font_size=32, color=YES),
            MathTex(r"n = \lfloor 2^{k/2} \rfloor \text{ works for } k \ge 3: \qquad R(k, k) > 2^{k/2}", font_size=32,
                    color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.4)
        sel = [r for r in d["ramsey"] if r["k"] in (4, 6, 8, 10, 12, 16, 20)]
        rows = [[str(r["k"]), words(r["floor"]), words(r["n"])] for r in sel]
        tab = grid_table([r"$k$", r"$2^{k/2}$", r"largest $n$ with $\mathbb{E} < 1$"], rows, widths=[1.0, 1.8, 4.0],
                         row_h=0.36, font_size=19, mono_cols=(), colors=[[GREY_A, HEAD, YES]] * len(rows))
        tab.next_to(lines, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        side = VGroup(
            label(r"explicit constructions matching the random \\ asymptotic scale remain open",
                  font_size=20, color=WHITE),
            label(r"selected upper bounds: \ $(4-\varepsilon)^k$ (2023); \\ $3.8^{k+o(k)}$ (2024 preprint, revised 2026)", font_size=20, color=LAM),
            label(r"dated source reports; \ no complete record survey; \\ upper and lower exponential scales still differ", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(tab, RIGHT, buff=0.6)
        if side.get_right()[0] > 6.9:
            side.scale((6.9 - side.get_left()[0]) / side.width, about_edge=LEFT)
        with self.voiceover(
            (
            "In 1947 Erdős reversed the question. <bookmark mark='a'/> Color each edge independently by a fair coin."
            ' A particular set of k vertices is monochromatic with probability two to the one minus k choose two. '
            "<bookmark mark='b'/> Summing over all sets gives the expected number of bad cliques. If it is below "
            'one, some coloring has none, because an integer-valued nonnegative count cannot always be at least one.'
            " <bookmark mark='c'/> This yields an exponential lower bound on the Ramsey number, of scale two to the "
            "k over two. <bookmark mark='d'/> The table gives the finite values certified by this expectation "
            'calculation. Expectation below one proves existence; it alone does not imply almost every coloring '
            "works. <bookmark mark='e'/> Explicit constructions matching the random asymptotic scale remain a major "
            "challenge. <bookmark mark='f'/> Campos, Griffiths, Morris and Sahasrabudhe reported a base below four "
            'in 2023. A selected 2024 preprint by Gupta, Ndiaye, Norin and Wei, revised in 2026, reports base 3.8 '
            'with a lower-order exponent. These are dated source claims, not a complete latest-record survey. '
            "<bookmark mark='g'/> The exponential gap between upper and lower bounds remains large."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2))
            for mk, s_ in zip("efg", side):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.wait(0.3)
        self.clear_scene()

    def lll(self):
        d = load("probmethod")
        head = label(r"When bad events are rare and local", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"bad events $A_1, \dots, A_m$, \ each of probability $\le p$, \ each independent of all but $d$ "
                  r"others", font_size=21, color=WHITE),
            MathTex(r"e\,p\,(d + 1) \le 1 \quad\Longrightarrow\quad \Pr[\text{no } A_i \text{ happens}] > 0",
                    font_size=36, color=YES),
            label(r"the Lov\'asz local lemma \ (Erd\H{o}s and Lov\'asz, 1975): \ the probability may be "
                  r"exponentially small, \ but it isn't zero", font_size=20, color=GREY_A),
            label(r"$k$-SAT: \ a clause fails with $p = 2^{-k}$; \ if each clause shares variables with at most "
                  r"$2^k/e - 1$ others, \ the formula is satisfiable", font_size=21, color=LAM),
            label(r"Moser and Tardos (2010): \ while some clause fails, \ re-randomize its variables; \ expected "
                  r"resamplings $\le m/d$", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.26).next_to(head, DOWN, buff=0.35)
        rows = [[words(r["n"]), words(r["m"]), str(r["d"]), f"{r['lll']:.2f}", str(r["initial_bad"]),
                 str(r["resamplings"])] for r in d["mt"]]
        tab = grid_table([r"variables", r"10-clauses", r"$d$ bound", r"$e p (d + 1)$", r"failing at first",
                          r"resamplings"], rows, widths=[1.7, 1.8, 0.9, 1.9, 2.4, 2.0], row_h=0.38, font_size=18,
                         mono_cols=(), colors=[[GREY_A, GREY_A, LAM, YES, NO, HEAD]] * len(rows))
        tab.next_to(lines, DOWN, buff=0.35).set_x(0)
        with self.voiceover(
            (
            "Sometimes existence needs a dependency argument. <bookmark mark='a'/> Suppose each bad event has "
            'probability at most p, and is independent of the collection outside its dependency neighborhood, of '
            "degree at most d. <bookmark mark='b'/> The symmetric local lemma gives positive probability of no bad "
            "event when e times p times d plus one is at most one. <bookmark mark='c'/> This is the Lovász local "
            "lemma of Erdős and Lovász. Positive probability need not be large. <bookmark mark='d'/> For k-SAT under"
            ' independent fair variable assignments, each clause fails with probability at most two to the minus k '
            "when it contains k distinct variables. Shared variables define a dependency graph. <bookmark mark='e'/>"
            " Moser and Tardos' 2010 variable-model algorithm resamples all variables of a currently false clause. "
            'Under the criterion it has an expected resampling bound; exhausting our execution budget would not '
            "prove unsatisfiability. <bookmark mark='f'/> Each table row starts the algorithm from exactly the "
            'assignment used to count its initial false clauses. The reported d is a safe dependency-degree upper '
            "bound; steps and final assignments are checked. The comparison m over d is a theorem's expectation "
            'bound under the criterion, not a per-run maximum.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()
