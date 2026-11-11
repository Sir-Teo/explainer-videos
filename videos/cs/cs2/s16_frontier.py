from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import (ADV, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, LIMIT, NO, PART, YES, fmt, load, say)

RED, BLUE = NO, DATA


def ring(n, r=1.6):
    return [np.array([r * np.cos(np.pi / 2 - 2 * np.pi * k / n), r * np.sin(np.pi / 2 - 2 * np.pi * k / n), 0])
            for k in range(n)]


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): Ramsey numbers, from the pigeonhole principle to the 2023
    exponential improvement, and the open problem of building what the probabilistic method proves exists."""

    def construct(self):
        self.card()
        self.party()
        self.paley()
        self.bounds()
        self.breakthrough()
        self.explicit()

    def card(self):
        card = chapter_card(15, r"Frontier: \ order in chaos", r"How big must a party be?", lit=(1930, 1947, 2023),
                            part=PART, extra=((1930, r"Ramsey's theorem"), (1947, r"Erd\H{o}s: the probabilistic method"),
                                              (2023, r"$R(k) < (4 - \varepsilon)^k$")))
        with self.voiceover("Chapter fifteen. Frontier: order in chaos."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def party(self):
        r = load("ramsey")
        head = label(r"Three friends or three strangers", font_size=36).to_edge(UP, buff=0.3)
        p5 = ring(5)
        k5 = VGroup(*[Line(p5[a], p5[b], color=RED if (b - a) % 5 in (1, 4) else BLUE, stroke_width=4)
                      for a in range(5) for b in range(a + 1, 5)])
        d5 = VGroup(*[Dot(p, radius=0.09, color=WHITE) for p in p5])
        g5 = VGroup(k5, d5).move_to(LEFT * 4.0 + DOWN * 0.2)
        l5 = label(r"five people: \ no three all friends \ (red), \\ no three all strangers \ (blue)", font_size=20,
                   color=GREY_A).next_to(g5, DOWN, buff=0.3)
        p6 = [p + RIGHT * 2.6 + DOWN * 0.2 for p in ring(6)]
        v = p6[0]
        spokes = VGroup(*[Line(v, p6[k], color=RED if k in (1, 2, 4) else BLUE, stroke_width=4) for k in range(1, 6)])
        d6 = VGroup(*[Dot(p, radius=0.09, color=WHITE) for p in p6])
        steps = VGroup(
            label(r"five edges at one person, \ two colours: \ three share a colour \ (pigeonhole)", font_size=20,
                  color=CTRL),
            label(r"if any two of those three are red, \ a red triangle; \ if none are, \ a blue one", font_size=20,
                  color=CTRL),
            label(rf"checked: \ all $2^{{15}} = 32{{,}}768$ colourings of six people: \ {fmt(r['good6'])} escape",
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35).shift(RIGHT * 1.6)
        tri = VGroup(Line(p6[1], p6[2], color=BLUE, stroke_width=4), Line(p6[2], p6[4], color=BLUE, stroke_width=4),
                     Line(p6[1], p6[4], color=BLUE, stroke_width=4))
        res = MathTex(r"R(3, 3) = 6", font_size=44, color=HEAD).move_to(RIGHT * 2.6 + UP * 2.4)
        with self.voiceover(
            "Part 2's pigeons lead straight to an open frontier. Among any six people, either three all know each "
            "other or three are all strangers; five people are not enough. <bookmark mark='a'/> Here are five, with "
            "friendship in red and strangers in blue: the red pentagon and the blue star contain no triangle of either "
            "colour. <bookmark mark='b'/> With six, pick one person. Five edges, two colours: by the pigeonhole "
            "principle, three of them share a colour, say red. <bookmark mark='c'/> If any two of those three people "
            "are friends, they make a red triangle with the first; if no two are, the three of them are a blue "
            "triangle. <bookmark mark='d'/> A computer agrees: of all thirty-two thousand ways to colour six people's "
            "relationships, not one escapes. Frank Ramsey proved in 1930 that this happens for any size: for every k "
            "there is a number R of k, a party size where k mutual friends or k mutual strangers are forced. Complete "
            "disorder is impossible."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(k5), FadeIn(d5), FadeIn(l5), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(d6), Create(spokes), FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), Create(tri))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), Write(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paley(self):
        r = load("ramsey")
        head = label(r"Seventeen people, \ and no four", font_size=36).to_edge(UP, buff=0.3)
        pts = ring(17, 2.4)
        red = {tuple(e) for e in r["paley17_edges"]}
        lines = VGroup(*[Line(pts[a], pts[b], color=RED if (a, b) in red else BLUE, stroke_width=1.4,
                              stroke_opacity=0.75) for a in range(17) for b in range(a + 1, 17)])
        dots = VGroup(*[Dot(p, radius=0.07, color=WHITE) for p in pts])
        g = VGroup(lines, dots).move_to(LEFT * 2.6 + DOWN * 0.3)
        side = VGroup(
            label(r"the Paley graph: \ $i$ and $j$ are friends \\ when $i - j$ is a square modulo 17", font_size=22,
                  color=GREY_A),
            label(rf"largest group of friends: \ {r['paley17_omega']}; \\ of strangers: \ {r['paley17_alpha']} \ "
                  r"(checked)", font_size=22, color=YES),
            MathTex(r"R(4,4) > 17", font_size=40, color=HEAD),
            label(r"and every colouring of 18 people has four: \\ $R(4,4) = 18$ \ (Greenwood and Gleason, \ 1955)",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.8 + DOWN * 0.2)
        with self.voiceover(
            "For four, the answer is eighteen. <bookmark mark='a'/> The colouring that shows seventeen is not enough "
            "comes from number theory: seat seventeen people in a circle and make two of them friends when the "
            "difference of their seats is a perfect square modulo seventeen. <bookmark mark='b'/> The largest group of "
            "mutual friends has three people, and so has the largest group of strangers: our program checked every "
            "group of four. <bookmark mark='c'/> And in 1955 Greenwood and Gleason proved that eighteen people always "
            "contain four. After that the exact values stop. For five, the answer is known only to lie between "
            "forty-three and forty-six."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dots), Create(lines), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            self.play(Write(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bounds(self):
        head = label(r"Two bounds, \ seventy-five years apart", font_size=36).to_edge(UP, buff=0.3)
        up = VGroup(
            label(r"upper \ (Erd\H{o}s and Szekeres, \ 1935): \ induction", font_size=22, color=YES),
            MathTex(r"R(k, \ell) \le R(k - 1, \ell) + R(k, \ell - 1) \ \Rightarrow\ R(k) \le \binom{2k - 2}{k - 1} < 4^k",
                    font_size=32, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(UP * 1.6)
        low = VGroup(
            label(r"lower \ (Erd\H{o}s, \ 1947): \ colour every edge by a coin toss \ (Part 2's linearity of "
                  r"expectation)", font_size=22, color=DATA),
            MathTex(r"\mathbb{E}[\#\text{ one-colour } K_k] = \binom{n}{k}\, 2^{\,1 - \binom{k}{2}} < 1"
                    r"\ \text{ when } n = 2^{k/2}", font_size=32, color=DATA),
            label(r"an average below one means some colouring has none: \ $R(k) > 2^{k/2}$", font_size=22,
                  color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(DOWN * 0.5)
        gap = MathTex(r"\sqrt{2}^{\,k} \ < \ R(k) \ < \ 4^k", font_size=48, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "For large k, two bounds from Paul Erdős have stood for most of a century. <bookmark mark='a'/> The upper "
            "one, with George Szekeres in 1935, is an induction of the kind Part 2 taught: R of k and l is at most R of "
            "k minus one and l, plus R of k and l minus one, which solves to a binomial coefficient, less than four to "
            "the k. <bookmark mark='b'/> The lower one, from 1947, founded the probabilistic method. Colour every "
            "relationship by tossing a coin, and count the expected number of one-colour groups of k, by linearity of "
            "expectation. Below two to the k over two people, that expectation is less than one, so some colouring has "
            "no such group at all. <bookmark mark='c'/> So R of k lies between root two to the k and four to the k: "
            "an exponential gap, and for seventy-five years nobody could move either end by an exponential factor."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(up[0]), Write(up[1]))
            vo.wait_until("b")
            self.play(FadeIn(low[0]), Write(low[1]))
            self.play(FadeIn(low[2]))
            vo.wait_until("c")
            self.play(Write(gap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def breakthrough(self):
        head = label(r"2023: \ the upper bound moves", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"1935", font_size=24, color=HIST), MathTex(r"R(k) < 4^k", font_size=36)),
            VGroup(label(r"2009", font_size=24, color=HIST), MathTex(r"R(k) < 4^{k}\, k^{-c \log k / \log\log k}",
                                                                    font_size=36)),
            VGroup(label(r"2023", font_size=24, color=HIST), MathTex(r"R(k) < (4 - 2^{-7})^{k}", font_size=36,
                                                                    color=HEAD)),
            VGroup(label(r"2024", font_size=24, color=HIST), MathTex(r"R(k) < 3.8^{\,k + o(k)}", font_size=36,
                                                                    color=HEAD)),
        )
        for k, r in enumerate(rows):
            r[1].scale(0.85)
            r[0].move_to([-5.6, 1.8 - 0.75 * k, 0])
            r[1].move_to([-4.9, 1.8 - 0.75 * k, 0], aligned_edge=LEFT)
        who = VGroup(
            label(r"Thomason \ (1988), \ Conlon \ (2009): \ savings smaller than any exponential", font_size=20,
                  color=GREY_B),
            label(r"Campos, Griffiths, Morris and Sahasrabudhe: \\ the first exponential improvement, \ by a `book' "
                  r"algorithm", font_size=20, color=YES),
            label(r"Gupta, Ndiaye, Norin and Wei: \ the same argument, \ optimised", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        small = VGroup(
            label(r"exact values: \ $R(3) = 6$, \ $R(4) = 18$; \ \ $43 \le R(5) \le 46$ \ (the 46: Angeltveit and McKay, "
                  r"2024, \ by computer)", font_size=20, color=GREY_A),
            label(r"Erd\H{o}s: \ if aliens demanded $R(5)$, \ we should set every computer to work; \ for $R(6)$, \ we "
                  r"should fight", font_size=20, color=HIST),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Then, in 2023, the upper end moved. <bookmark mark='a'/> For decades the only progress shaved off factors "
            "smaller than any exponential: Andrew Thomason in 1988, David Conlon in 2009. <bookmark mark='b'/> In March 2023 Marcelo "
            "Campos, Simon Griffiths, Robert Morris and Julian Sahasrabudhe proved that R of k is less than four minus "
            "a small epsilon, all to the k, the first exponential improvement since 1935, with a new way of growing "
            "a structure they called a book. <bookmark mark='c'/> A year later Gupta, Ndiaye, Norin and Wei sharpened "
            "the same argument to three point eight to the k. The lower bound has not moved by an exponential factor "
            "since 1947. <bookmark mark='d'/> And the small cases remain brutally hard: the five-person number is between "
            "forty-three and forty-six, the forty-six proved in 2024 with linear programming and a large computer "
            "search. Erdős liked to say that if aliens demanded R of five on pain of destroying the Earth, we should "
            "set every computer to work on it; if they asked for R of six, we should try to destroy the aliens."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(who[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(who[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), FadeIn(who[2]))
            vo.wait_until("d")
            self.play(FadeIn(small[0]))
            self.play(FadeIn(small[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def explicit(self):
        r = load("ramsey")
        head = label(r"Proved to exist, \ but where?", font_size=36).to_edge(UP, buff=0.3)
        pal = r["paley"]
        ax = Axes(x_range=[0, 400, 100], y_range=[0, 20, 5], x_length=6.0, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16, "include_numbers": True}).move_to(LEFT * 2.6 + DOWN * 0.4)
        xl = note(r"prime $q$", font_size=18).next_to(ax, DOWN, buff=0.3)
        yl = note(r"largest group of friends in the Paley graph", font_size=18).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(p["q"], p["omega"]), radius=0.05, color=HEAD) for p in pal])
        qs = np.linspace(5, 400, 80)
        rnd = VMobject(color=DATA, stroke_width=2.5).set_points_as_corners([ax.c2p(q, 2 * np.log2(q)) for q in qs])
        sq = VMobject(color=GREY_B, stroke_width=2).set_points_as_corners([ax.c2p(q, np.sqrt(q)) for q in qs])
        lr = label(r"$2 \log_2 q$: \ a random colouring", font_size=18, color=DATA).next_to(ax.c2p(400, 2 * np.log2(400)),
                                                                                        DOWN, buff=0.15).shift(LEFT * 0.9)
        ls = label(r"$\sqrt{q}$: \ what can be proved", font_size=18, color=GREY_B).next_to(ax.c2p(290, np.sqrt(290)),
                                                                                         UP + LEFT, buff=0.1)
        side = VGroup(
            label(r"the probabilistic method proves good colourings exist \\ without saying where any of them is",
                  font_size=20, color=GREY_A),
            label(r"an \textit{explicit} colouring, \ built by a rule, \\ as good as a random one: \ open since 1947",
                  font_size=20, color=LIMIT),
            label(r"Paley graphs look random: \ their cliques grow \\ like $\log q$ in every case computed, \ but the "
                  r"best \\ proved bound is about $\sqrt{q}$", font_size=20, color=HEAD),
            label(r"the same question drives randomness extractors \\ and pseudorandomness \ (Parts 20, 27)",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "The lower bound hides a deeper open problem. <bookmark mark='a'/> Erdős's argument proves that good "
            "colourings exist, colourings of two to the k over two people with no large one-colour group, without "
            "saying where a single one of them is. <bookmark mark='b'/> Nobody knows how to build one by a rule that "
            "matches a random colouring: this has been open since 1947. <bookmark mark='c'/> Paley graphs are the "
            "natural candidate. We computed the largest group of friends in every Paley graph up to four hundred "
            "people: it grows like the logarithm, as a random colouring's would, nine at most here. But the best bound "
            "anyone can prove is of the order of the square root, near twenty at four hundred, far from the truth. "
            "<bookmark mark='d'/> Building order-free structures on purpose is the same problem as extracting good "
            "randomness from bad sources, which Parts 20 and 27 take up. It is the research problem of this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), Create(rnd), FadeIn(lr), Create(sq),
                      FadeIn(ls), run_time=2.5)
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()
