from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import alphas as A
from videos.quant.quant29.common import FORMULA, HURDLE, PART, RAND_C, fit_right, house_lab, load, sci


class Space(VoiceoverScene):
    def construct(self):
        s = load("space")
        self.card()
        self.recursion(s)
        self.growth(s)
        self.lab()
        self.redundancy(load("random"))
        self.question()

    def card(self):
        c = chapter_card(2, r"The search space", r"How many formulas are there?", part=PART)
        with self.voiceover("Chapter two. If signals are trees, how many trees are there to search?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def recursion(self, s):
        nf, nu, nt, nb, nw = len(s["fields"]), len(s["unary"]), len(s["ts"]), len(s["binary"]), len(s["windows"])
        rows = [cmath(r"N_1", r"=", rf"{nf}\ \text{{fields}}", font_size=34, colors={r"N_1": FORMULA}),
                cmath(r"N_d", r"=", rf"N_1 + {nu}\,N_{{d-1}} + {nt}\cdot{nw}\,N_{{d-1}} + ({nb} + {nw})\,N_{{d-1}}^2", font_size=32,
                      colors={r"N_d": FORMULA}),
                cmath(r"N_d", r"\approx", r"c\,N_{d-1}^2 \ \Rightarrow\ \log N_d \sim 2^d", font_size=34, colors={r"N_d": HURDLE})]
        whys = [why(r"a tree of depth one is a single field"),
                why(rf"a tree of depth at most $d$ is a field, or a one-argument operator ({nu} of them) on a smaller tree, "
                    rf"or a time-series operator ({nt}) with one of {nw} windows, or a two-argument one ({nb} arithmetic, "
                    r"and \texttt{corr} with a window) on two smaller trees"),
                why(r"the square term wins: the count is doubly exponential in depth")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Count them. <bookmark mark='a'/> A tree of depth one is a single field: six of them. <bookmark mark='b'/> "
            "A tree of depth d is a field, or an operator applied to smaller trees: one argument, or a time-series "
            "operator with one of four windows, or two arguments. <bookmark mark='c'/> The two-argument term squares "
            "the previous count, so the number of trees grows doubly exponentially with depth."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def growth(self, s):
        cnt = np.asarray(s["count"], float)
        lg = np.log10(cnt)
        g = axes([0.5, 6.5], [0, 60], x_length=7.4, y_length=4.4, xlabel=r"maximum depth of the tree",
                 ylabel=r"number of distinct formulas (log$_{10}$)", xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 20, 40, 60],
                 font_size=15).move_to(LEFT * 2.0 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.6, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.02), stroke_width=0,
                                  fill_color=FORMULA, fill_opacity=0.85).move_to([ax.c2p(k + 1, 0)[0],
                                                                                 (ax.c2p(0, 0)[1] + ax.c2p(0, v)[1]) / 2, 0])
                        for k, v in enumerate(lg)])
        tags = VGroup(*[MathTex(sci(v) if v >= 1e4 else f"{v:,.0f}".replace(",", "{,}"), font_size=18).next_to(b, UP, buff=0.08)
                        for v, b in zip(cnt, bars)])
        hours3 = cnt[2] / 100 / 3600
        years4 = cnt[3] / 100 / 3600 / 24 / 365.25
        side = wrapped_label(rf"at a hundred formulas a second, depth 3 takes about {hours3:.1f} hours; depth 4 about "
                             rf"{years4:,.0f} years. Search cannot be exhaustive: it must be guided, and every step it "
                             r"takes is a trial".replace(",", "{,}", 1), 3.6, 16, GREY_A).to_edge(RIGHT, buff=0.35)
        m3 = cnt[2] / 1e6
        e4 = int(np.floor(np.log10(cnt[3])))
        m4 = cnt[3] / 10 ** e4
        e6 = int(np.floor(np.log10(cnt[5])))
        fit_right(side)
        with self.voiceover(
            f"The numbers. <bookmark mark='a'/> Six formulas of depth one; {cnt[1]:,.0f} of depth two; about {m3:.0f} "
            f"million of depth three; about {m4:.0f} times ten to the {e4} of depth four. <bookmark mark='b'/> Depth six "
            f"gives around ten to the {e6}. No computer will ever evaluate them all. So search has to be guided: random, "
            "evolutionary, learned, or written by a language model. And every formula it evaluates is a trial, which "
            "Part twenty-six taught us to count."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:4]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(t_) for t_ in tags[:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[4], DOWN), GrowFromEdge(bars[5], DOWN), FadeIn(tags[4]), FadeIn(tags[5]),
                      FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Growing a random formula", A.random_tree, "if max_depth <= 1", 11, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "How does a miner draw a formula at random? This is the House's version of Koza's grow method. At each "
            "node, stop with probability three in ten and place a field; otherwise choose a kind of operator, a "
            "quarter of the time one with a single argument, a third of the time a time-series operator with a random "
            "window, sometimes a rolling correlation, otherwise arithmetic, and grow its arguments the same way, one "
            "level shallower. The probabilities are a prior: they decide which corners of the space the search visits "
            "most, long before any data is seen."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def redundancy(self, r):
        rng = np.random.default_rng(2929)                 # the same draws as Chapter 3
        trees = [A.random_tree(rng, 4) for _ in range(r["n"])]
        n_str = len(set(A.to_str(t) for t in trees))
        v = np.round(np.asarray(r["train"], float), 5)
        n_score = len(np.unique(v[np.isfinite(v)]))
        n_leaf = sum(1 for t in trees if A.depth(t) == 1)
        n_all = r["n"]
        bars = VGroup()
        vals = [(r"draws", n_all, GREY_B), (r"distinct formulas", n_str, FORMULA), (r"distinct scores", n_score, RAND_C)]
        for k, (t, n, col) in enumerate(vals):
            w = 7.6 * n / n_all
            bars.add(VGroup(label(t, font_size=20, color=col).move_to([-4.6, 1.4 - 1.1 * k, 0]),
                            Rectangle(width=w, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.8).move_to(
                                [-3.0 + w / 2, 1.4 - 1.1 * k, 0]).shift(RIGHT * 0.4),
                            MathTex(f"{n:,}".replace(",", "{,}"), font_size=26, color=col)))
            bars[-1][2].next_to(bars[-1][1], RIGHT, buff=0.2)
            bars[-1][0].align_to(np.array([-6.2, 0, 0]), LEFT)
        foot = wrapped_label(rf"{n_leaf:,} of the draws are a single field; \texttt{{rank(x)}} and $x$, or $x/y$ and "
                             r"\texttt{neg}$(y/x)$, are different trees with the same ranking of coins, so the same score"
                             .replace(",", "{,}", 1), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The space is also smaller than it looks. <bookmark mark='a'/> Of our ten thousand random draws, only "
            f"{n_str:,} are distinct formulas: the short ones come up again and again, and {n_leaf:,} of the draws are a "
            "single field. <bookmark mark='b'/> And many distinct formulas are the same signal in disguise. A rank of x "
            "orders the coins exactly as x does; x over y and minus y over x agree too. Counting distinct scores instead "
            f"of distinct strings leaves {n_score:,}. Even this simple fact matters for the trial counter: a search "
            "tries fewer different things than its count of formulas suggests."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[:2]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(bars[2]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a million machines each evaluate 100 formulas a second. How long to try every formula of "
                       r"depth 5?")
        with self.voiceover(
            "Pause and predict. A million machines each evaluate a hundred formulas a second. How long to try every "
            "formula of depth five?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
