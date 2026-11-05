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
        with self.voiceover("Chapter fourteen. The probabilistic method."):
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
            "Colour every edge of a complete graph red or blue. Frank Ramsey proved in 1930 that if the graph is "
            "big enough, some k vertices have all their edges the same colour, whatever you do. <bookmark mark='a'/> "
            "With four vertices, seventeen are not enough. On the left, a random colouring of the complete graph "
            f"on seventeen vertices: on average it has {d['k4_mean']:.0f} groups of four in a single colour. "
            "<bookmark mark='b'/> On the right, a clever colouring, blue exactly when the difference of the two "
            "vertices is a square modulo seventeen, has none at all. Eighteen vertices always contain one, so "
            "the Ramsey number R of four, four is eighteen. <bookmark mark='c'/> For five, nobody knows the answer: "
            "it is between forty-three and forty-six. For large k, clever colourings run out, but coins don't."
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
            label(r"nobody can \textbf{construct} such colourings: \\ the best explicit ones are far smaller",
                  font_size=20, color=WHITE),
            label(r"upper bound $4^k$ \ (Erd\H{o}s--Szekeres, 1935); \\ $(4 - \varepsilon)^k$ \ (Campos, Griffiths, "
                  r"Morris \\ and Sahasrabudhe, 2023)", font_size=20, color=LAM),
            label(r"the lower bound $\sqrt{2}^{\,k}$ has barely moved \\ since 1947", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(tab, RIGHT, buff=0.6)
        if side.get_right()[0] > 6.9:
            side.scale((6.9 - side.get_left()[0]) / side.width, about_edge=LEFT)
        with self.voiceover(
            "In 1947 Paul Erdős turned the question around. <bookmark mark='a'/> Colour each edge by a fair coin. A "
            "particular set of k vertices comes out all one colour with probability two times two to the minus k "
            "choose two. <bookmark mark='b'/> Add over all sets: if the expected number of one-colour sets is "
            "below one, then some colouring has none at all, because a random variable can't always be above its "
            "own average. <bookmark mark='c'/> The arithmetic works for n up to about two to the k over two. So "
            "the Ramsey number is at least that. <bookmark mark='d'/> Here is how far the count reaches for each "
            "k. The proof shows the colourings exist, and even that almost every colouring works, but it doesn't "
            "say how to write one down. <bookmark mark='e'/> Seventy-five years later, nobody can construct "
            "colourings anywhere near that good. <bookmark mark='f'/> The upper bound, four to the k, was "
            "improved for the first time in 2023, to four minus epsilon to the k, <bookmark mark='g'/> while the "
            "lower bound from coins has barely moved since 1947."
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
        tab = grid_table([r"variables", r"10-clauses", r"$d$", r"$e p (d + 1)$", r"failing at first",
                          r"resamplings"], rows, widths=[1.7, 1.8, 0.9, 1.9, 2.4, 2.0], row_h=0.38, font_size=18,
                         mono_cols=(), colors=[[GREY_A, GREY_A, LAM, YES, NO, HEAD]] * len(rows))
        tab.next_to(lines, DOWN, buff=0.35).set_x(0)
        with self.voiceover(
            "Sometimes the good outcome is very unlikely, and counting fails. <bookmark mark='a'/> Suppose there "
            "are many bad events, each of small probability p, and each one independent of all but d of the "
            "others. <bookmark mark='b'/> If e times p times d plus one is at most one, then with positive "
            "probability none of them happens. <bookmark mark='c'/> That is the Lovász local lemma, from Erdős and "
            "Lovász in 1975. The probability can be exponentially small, but it isn't zero, so the good outcome "
            "exists. <bookmark mark='d'/> For example, a k-SAT formula in which every clause shares variables with "
            "fewer than about two to the k over e others is always satisfiable. <bookmark mark='e'/> For thirty-five "
            "years the proof gave no way to find the assignment. Then in 2010 Robin Moser and Gábor Tardos showed "
            "that the most naive algorithm works: while some clause is false, give its variables fresh random "
            "values. <bookmark mark='f'/> We built 10-SAT formulas where each clause meets about three hundred "
            "others, inside the lemma's condition. Each needed only about as many resamplings as it had false "
            "clauses at the start, far inside the bound of m over d."
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
