from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import arbitrage as A
from explainer.quant.house import trees
from explainer.quant.viz import binomial_tree
from videos.quant.quant9.common import ALT, ARB, CALL, FWD, PART, PUT, Q_C, load, tbar


class Tree(VoiceoverScene):
    def construct(self):
        self.card()
        self.fold()
        self.incomplete(load("incomplete"))

    def card(self):
        c = chapter_card(3, r"The tree, completeness, and super-replication", r"When does a price follow from "
                         r"no arbitrage alone?", lit=(1979,), part=PART)
        with self.voiceover("Chapter three. The binomial tree, completeness, and super-replication."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fold(self):
        out = trees.crr(100.0, 100.0, 1.0, 0.25, 0.0, N=4, cp=1, keep=5)
        layers = out["layers"]
        g = binomial_tree(layers, dx=1.9, dy=0.62, node_r=0.32, font_size=19, show=("values",))
        g.to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        eq = VGroup(
            MathTex(r"q = \frac{e^{r\Delta t} - d}{u - d}", font_size=36, color=Q_C),
            MathTex(r"V = e^{-r\Delta t}\big(q\,V_u + (1 - q)\,V_d\big)", font_size=34),
            wrapped_label(r"two states, two assets (stock and bond): any payoff is replicated, so its price is "
                          r"forced; the tree folds back from the payoff at expiry (Cox, Ross and Rubinstein 1979)",
                          4.4, 20, GREY_A),
            wrapped_label(rf"a call: $K = 100$, $\sigma = 25\%$, one year, four steps: {out['price']:.2f}. Part 10 "
                          r"lets the steps go to infinity", 4.4, 20, CALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        n_last = max(int(k) for k in layers)
        with self.voiceover(
            "In 1979 John Cox, Stephen Ross and Mark Rubinstein made the theorem concrete. Let the stock move up or "
            "down each step: two states, two assets. Then any payoff can be built from the stock and the bond, so "
            "its price is forced, and the risk-neutral probability is fixed by the size of the moves alone. "
            "<bookmark mark='a'/> Start from the payoff at expiry and fold the tree back: each node is the "
            "discounted risk-neutral average of the two after it. <bookmark mark='b'/> Four steps price a call at "
            f"{out['price']:.2f}; Part ten lets the steps go to infinity, and the tree becomes Black and Scholes."
        ) as vo:
            self.play(FadeIn(g.edges), FadeIn(eq[0]), FadeIn(eq[2]))
            vo.wait_until("a")
            for n in range(n_last, -1, -1):
                self.play(FadeIn(g.nodes[n]), run_time=0.7)
            self.play(FadeIn(eq[1]))
            vo.wait_until("b")
            self.play(FadeIn(eq[3]), Indicate(g.nodes[0], color=CALL))
        self.wait(0.4)
        self.clear_scene()

    def incomplete(self, inc):
        rows = inc["rows"]
        g = axes([0, len(rows)], [0, 0.22], x_length=6.6, y_length=4.2, ylabel=r"no-arbitrage prices of an "
                 r"at-the-money call", xticks=[], yticks=[0, 0.05, 0.1, 0.15, 0.2], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        labs = VGroup()
        for i, r_ in enumerate(rows):
            lo, hi = max(r_["lower"], 0.0), r_["upper"]
            if hi - lo < 1e-6:
                bars.add(Dot(ax.c2p(i + 0.5, lo), radius=0.08, color=CALL))
            else:
                bars.add(tbar(ax, i + 0.5, hi, ALT, width=0.45, lo=lo).set_fill(opacity=0.55))
            labs.add(label(f"{r_['states']}", font_size=19, color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.1))
        xl = label(r"states tomorrow", font_size=18, color=GREY_B).next_to(labs, DOWN, buff=0.15)
        bsl = DashedLine(ax.c2p(0, inc["bs"]), ax.c2p(len(rows), inc["bs"]), color=CALL, stroke_width=2)
        bsll = wrapped_label(rf"dashed: one model's price inside the interval (Black--Scholes at 20\% vol): "
                             rf"{inc['bs']:.3f}; the dot: two states, where the price is forced", 4.4, 19, CALL)
        side = VGroup(
            MathTex(r"\overline{p} = \min_\theta\ \theta\cdot p\ \ \text{s.t.}\ \ D^\top\theta \ge X", font_size=30,
                    color=ALT),
            MathTex(r"\underline{p} = \max_\theta\ \theta\cdot p\ \ \text{s.t.}\ \ D^\top\theta \le X", font_size=30,
                    color=ALT),
            wrapped_label(r"with three or more states and two assets, the market is incomplete: no arbitrage only "
                          r"gives an interval, the cost of the cheapest hedge that always covers the payoff and the "
                          r"value of the richest one it always covers", 4.4, 20, GREY_A),
            wrapped_label(r"the interval never shrinks as states are added; trading the call itself, or choosing a "
                          r"model, picks a price inside it", 4.4, 20, Q_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        bsll.next_to(side, DOWN, buff=0.25).align_to(side, LEFT)
        with self.voiceover(
            "That works because the tree has exactly two branches. Give the stock three possible outcomes tomorrow, "
            "with still only the stock and the bond to trade, and the market is incomplete: a call can no longer "
            "be replicated. <bookmark mark='a'/> No arbitrage then gives only an interval. Its top is the cost of "
            "the cheapest portfolio whose payoff is always at least the call's: super-replication, a linear program. "
            "Its bottom is the richest portfolio the call always beats. <bookmark mark='b'/> With two states the "
            "interval is a single point. With three it opens, and adding more states never closes it. A model, "
            "like Black and Scholes, picks one price inside; so does trading the option itself, which makes the "
            "market complete again. That is why options exist: they complete the market."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(xl), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.3), run_time=2.5)
            self.play(Create(bsl), FadeIn(bsll), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
