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
        for u in small:
            if not small[u]:nodes[u].set_stroke(HEAD,width=3)
        dangling_caption=label(r"gold outline: no outgoing links; redistribute rank uniformly",
                               font_size=18,color=HEAD).move_to([-3.7,-3.25,0])
        if dangling_caption.width>6.0:dangling_caption.scale_to_fit_width(6.0)
        steps = VGroup(
            label(r"a surfer follows a random link with probability $d = 0.85$, \\ and jumps to a random page otherwise",
                  font_size=21, color=GREY_A),
            MathTex("r(v) = \\frac{1-d+dD}{n} + d \\sum_{u \\to v} \\frac{r(u)}{\\mathrm{outdeg}(u)}", font_size=30,
                    color=YES),
            label("$D$: rank on pages with no outgoing links; \\\\ redistributed uniformly to all $n$ pages", font_size=21, color=GREY_A),
            label(r"important pages are those linked from important pages: \\ circular, \ but well defined", font_size=21,
                  color=HEAD),
            label(r"the stationary distribution of a Markov chain \\ (\textit{AI, Built}, \ Part 5)", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        if steps.width > 6.0:
            steps.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "PageRank assigns a stationary probability in a specified random-surfer model. <bookmark "
            "mark='a'/> With probability zero point eight five, follow a uniformly chosen outgoing link; "
            "otherwise jump uniformly to any page. At a page with no outgoing links, distribute its rank "
            "uniformly too. <bookmark mark='b'/> The equation includes all three contributions: "
            "teleportation, linked incoming rank, and dangling-page rank. That last term is needed for "
            "the small graph drawn here. <bookmark mark='c'/> Circle sizes encode the computed stationary"
            " probabilities, not a direct measurement of human importance. <bookmark mark='d'/> For "
            "damping strictly below one and uniform teleportation on a nonempty finite graph, the "
            "stationary vector is unique and power iteration converges. It is a model with a mathematical"
            " guarantee, rather than a guarantee of ranking quality."
        ) as vo:
            self.play(FadeIn(head), Create(arrows), FadeIn(nodes))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]),FadeIn(dangling_caption))
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
        yl = label("$L_1$ iterate change, \\ log scale", font_size=17, color=GREY_B).next_to(ax, UP, buff=0.1
                                                                                             ).align_to(ax, LEFT)
        side = VGroup(
            label(r"start uniform; \\ apply the equation to every page; \\ repeat", font_size=21, color=GREY_A),
            label("$C_{k+1}\\le d C_k$ in $L_1$; \\ $0\\le d<1$ \\\\ dashed: first change $\\times d^{k-1}$", font_size=21, color=HEAD),
            label(rf"{len(res)} rounds to $10^{{-12}}$, \\ each one pass over the {words(d['m'])} links", font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        if side.width > 5.0:
            side.scale_to_fit_width(5.0).to_edge(RIGHT, buff=0.4)
        check=d['certificates'][0]
        fixed_point=VGroup(
            label(rf"checked stationarity residual: {check['stationarity_l1']:.2e}",font_size=18,color=YES),
            MathTex(r"\|r-r^*\|_1\le\frac{\|T(r)-r\|_1}{1-d}",font_size=27,color=HEAD),
        ).arrange(DOWN,buff=.16).move_to([4.0,-2.65,0])
        with self.voiceover(
            "Power iteration repeatedly applies the full surfer operator. <bookmark mark='a'/> Start with"
            " uniform rank, scan every link and redistribute dangling mass in each round. The green curve"
            " is the L1 change between successive vectors. <bookmark mark='b'/> Damping zero point eight "
            "five gives an L1 contraction bound: changes are at most zero point eight five times the "
            "preceding change. The dashed curve is a bound scaled from the first observed change, not an "
            "exact error trajectory. <bookmark mark='c'/> We check the final vector with a separate "
            "numerical operator, verify probability mass and compute its stationarity residual. Dividing "
            "that residual by one minus damping bounds distance to the stationary vector. A small iterate"
            " change is not itself proof that every pair of pages has a settled ordering."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(line))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ref), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]),FadeIn(fixed_point))
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
            "This ranking belongs to a synthetic graph. <bookmark mark='a'/> The reported overlap "
            "compares its top ten by PageRank with its top ten by incoming-link count. <bookmark "
            "mark='b'/> Preferential attachment makes old popular pages attractive to new links, so this "
            "generator naturally couples those two measures. It is not a measurement of today's web. "
            "<bookmark mark='c'/> PageRank weights links according to the linking page's rank, which "
            "differs from merely counting incoming links. <bookmark mark='d'/> That difference does not "
            "make the system immune to manipulation: link farms and other adversarial strategies require "
            "additional ranking signals and defenses, as Part 47 discusses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, s in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()
