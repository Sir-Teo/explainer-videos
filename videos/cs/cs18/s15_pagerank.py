from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class PageRank(VoiceoverScene):
    def construct(self):
        self.card()
        self.surfer()
        self.power()
        self.top()

    def card(self):
        card = chapter_card(14, r"PageRank", r"Which page matters most?", lit=(1998,),
                            extra=((1998, r"Brin and Page"),), part=PART)
        with self.voiceover("Chapter fourteen. PageRank."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def surfer(self):
        d = load("pagerank")
        head = label(r"A random surfer", font_size=34).to_edge(UP, buff=0.3)
        small = {int(k): v for k, v in d["small"].items()}
        rank = {int(k): v for k, v in d["small_rank"].items()}
        n = len(small)
        ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
        pos = {u: np.array([2.3 * np.cos(a) - 3.7, 2.1 * np.sin(a) - 0.4, 0]) for u, a in zip(range(n), ang)}
        mx = max(rank.values())
        nodes = VGroup(*[Circle(radius=0.12 + 0.45 * rank[u] / mx, color=DATA, fill_color=DATA,
                                fill_opacity=0.25 + 0.5 * rank[u] / mx).move_to(pos[u]) for u in range(n)])
        arrows = VGroup(*[Arrow(pos[u], pos[v], buff=0.3, stroke_width=1.4, color=GREY_B,
                                max_tip_length_to_length_ratio=0.1) for u in small for v in small[u]])
        steps = VGroup(
            label(r"a surfer follows a random link with probability $d = 0.85$, \\ and jumps to a random page otherwise",
                  font_size=21, color=GREY_A),
            MathTex(r"r(v) = \frac{1 - d}{n} + d \sum_{u \to v} \frac{r(u)}{\mathrm{outdeg}(u)}", font_size=34,
                    color=YES),
            label(r"a page's rank: \\ the fraction of time the surfer spends there", font_size=21, color=GREY_A),
            label(r"important pages are those linked from important pages: \\ circular, \ but well defined", font_size=21,
                  color=HEAD),
            label(r"the stationary distribution of a Markov chain \\ (\textit{AI, Built}, \ Part 5)", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        if steps.width > 6.0:
            steps.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "In 1998 Sergey Brin and Larry Page asked how to rank web pages by importance, using only the links. "
            "<bookmark mark='a'/> Imagine a surfer who, on each page, follows a random link with probability "
            "eighty-five percent, and otherwise jumps to a page chosen at random. <bookmark mark='b'/> A page's "
            "rank is the fraction of time this surfer spends on it in the long run, and it satisfies this equation: "
            "a small share from the random jumps, plus a share of the rank of every page that links to it, divided "
            "among that page's links. <bookmark mark='c'/> The circle sizes here are the ranks of a small web. "
            "<bookmark mark='d'/> Important pages are those linked from important pages: a circular definition, "
            "but a perfectly good one, because it describes the stationary distribution of a Markov chain, the "
            "object AI, Built's fifth part studied."
        ) as vo:
            self.play(FadeIn(head), Create(arrows), FadeIn(nodes))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3:]))
        self.wait(0.3)
        self.clear_scene()

    def power(self):
        d = load("pagerank")
        head = label(rf"Power iteration on {words(d['n'])} pages", font_size=34).to_edge(UP, buff=0.3)
        res = d["residuals"]
        ax = Axes(x_range=[0, len(res) + 2, 10], y_range=[-13, 1, 2], x_length=7.0, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        pts = [ax.c2p(i + 1, np.log10(r)) for i, r in enumerate(res)]
        line = VGroup(VMobject(color=YES, stroke_width=3).set_points_as_corners(pts),
                      *[Dot(p, radius=0.03, color=YES) for p in pts])
        ref = DashedLine(ax.c2p(1, np.log10(res[0])), ax.c2p(len(res), np.log10(res[0]) + (len(res) - 1) *
                                                               np.log10(0.85)), color=HEAD, stroke_width=2)
        xt = VGroup(*[label(str(v), font_size=15, color=GREY_B).next_to(ax.c2p(v, -13), DOWN, buff=0.1)
                      for v in (10, 20, 30, 40, 50)])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v, t in ((0, "1"), (-6, r"$10^{-6}$"), (-12, r"$10^{-12}$"))])
        xl = label(r"iteration", font_size=17, color=GREY_B).next_to(xt, DOWN, buff=0.1)
        yl = label(r"change in the rank vector, \ log scale", font_size=17, color=GREY_B).next_to(ax, UP, buff=0.1
                                                                                             ).align_to(ax, LEFT)
        side = VGroup(
            label(r"start uniform; \\ apply the equation to every page; \\ repeat", font_size=21, color=GREY_A),
            label(r"the error shrinks by a factor $d$ each round \\ (dashed: \ $0.85^k$)", font_size=21, color=HEAD),
            label(rf"{len(res)} rounds to $10^{{-12}}$, \\ each one pass over the {words(d['m'])} links", font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        if side.width > 5.0:
            side.scale_to_fit_width(5.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "How is the equation solved for billions of pages? <bookmark mark='a'/> Start with every page equal, "
            "apply the equation to every page at once, and repeat. Each round is one pass over the links. <bookmark "
            "mark='b'/> The jump probability guarantees convergence: the error shrinks by at least a factor of "
            "zero point eight five per round, the dashed line. <bookmark mark='c'/> On our synthetic web of twenty "
            "thousand pages, about fifty rounds bring the change below one part in a trillion, and in practice far "
            "fewer rounds are enough to fix the order."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(line), run_time=2)
            vo.wait_until("b")
            self.play(Create(ref), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    def top(self):
        d = load("pagerank")
        head = label(r"The top pages", font_size=34).to_edge(UP, buff=0.3)
        rows = [[str(u), f"{100 * r:.2f}\\%", words(deg)] for u, r, deg in d["top"][:8]]
        tab = grid_table([r"page", r"PageRank", r"incoming links"], rows, widths=[1.8, 2.6, 2.8], row_h=0.44,
                         font_size=20, colors=[[WHITE, YES, GREY_A]] * len(rows)).next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        side = VGroup(
            label(rf"{d['overlap_top10']} of the top ten by rank are in the top ten by links", font_size=21,
                  color=GREY_A),
            label(r"on this synthetic web, \ where links grow by popularity, \\ rank mostly follows in-degree", font_size=21,
                  color=GREY_A),
            label(r"on the real web it resisted cheap link counts: \\ a link from an important page is worth more",
                  font_size=21, color=YES),
            label(r"spam farms then learned to fake importance: \\ ranking became an adversarial game \ (Part 47)",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        if side.width > 6.0:
            side.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Which pages come out on top? <bookmark mark='a'/> On our synthetic web, nine of the ten highest-ranked "
            "pages are also among the ten with most incoming links. <bookmark mark='b'/> That is because the web was "
            "grown by popularity, so the oldest pages are both the most linked and the best linked. <bookmark "
            "mark='c'/> On the real web the difference mattered: counting links was easy to fool, but a link from an "
            "important page counts for more, which made the ranking hard to game. <bookmark mark='d'/> For a while. "
            "Link farms learned to manufacture importance, and search ranking became the adversarial game that "
            "Part 47 describes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, s in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()
