from __future__ import annotations

import itertools

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import MART, P_C, PART, Q_C, load


class Measure(VoiceoverScene):
    def construct(self):
        m = load("measure")
        self.card()
        self.table()
        self.equivalence()
        self.paths(m)

    def card(self):
        c = chapter_card(6, r"Change of measure", r"What if the coin were different?", part=PART)
        with self.voiceover("Chapter six. Change of measure."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def table(self):
        outs = ["".join(o) for o in itertools.product("HT", repeat=3)]
        head = VGroup(*[label(t, font_size=22, color=c) for t, c in
                        [(r"world", GREY_B), (r"$P$: fair coin", P_C), (r"$Q$: heads 60\%", Q_C),
                         (r"$L = dQ/dP$", MART)]])
        rows = []
        for o in outs:
            h = o.count("H")
            p, q = 0.125, 0.6 ** h * 0.4 ** (3 - h)
            rows.append([MathTex(o, font_size=28), MathTex(r"0.125", font_size=28, color=P_C),
                         MathTex(f"{q:.3f}", font_size=28, color=Q_C), MathTex(f"{q / p:.3f}", font_size=28, color=MART)])
        cells = [*head] + [c for r in rows for c in r]
        grid = VGroup(*cells).arrange_in_grid(rows=9, cols=4, buff=(0.7, 0.14), col_alignments="cccc")
        grid.scale_to_fit_height(5.6).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        side = VGroup(
            MathTex(r"L(\omega) = \frac{Q(\omega)}{P(\omega)}", font_size=40, color=MART),
            MathTex(r"\mathbb{E}_Q[X] = \mathbb{E}_P[L\,X]", font_size=40),
            MathTex(r"\mathbb{E}_P[L] = 1", font_size=40),
            wrapped_label(r"the Radon--Nikodym derivative: reweight each world, and one probability becomes another",
                          4.6, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "The same worlds can carry different probabilities. Toss a coin three times. Under P the coin is fair, "
            "and each of the eight worlds has probability one eighth. Under Q the coin lands heads sixty percent of "
            "the time, and the worlds with more heads are more likely. <bookmark mark='a'/> Divide one by the other, "
            "world by world. This ratio, L, is the Radon-Nikodym derivative of Q with respect to P. "
            "<bookmark mark='b'/> It converts one into the other: any expectation under Q is an expectation under P "
            "of the variable reweighted by L. And because Q's probabilities add up to one, L averages to one under P. "
            "This is the whole of the change of measure. In Part nine the second measure will be the one in which "
            "every asset earns the riskless rate, and prices will be expectations under it."
        ) as vo:
            self.play(FadeIn(VGroup(*cells[:4])), LaggedStart(*[FadeIn(VGroup(*r[:3])) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in rows], lag_ratio=0.15), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def equivalence(self):
        d = definition_card(r"Equivalent measures",
                            r"$P$ and $Q$ are equivalent if they agree on which events are impossible: $P(A) = 0$ exactly "
                            r"when $Q(A) = 0$. Then $dQ/dP$ exists and is positive. They may disagree on everything "
                            r"else: how likely each possible thing is.", width=9.4, color=Q_C,
                            font_size=25).to_edge(UP, buff=0.7)
        ex = VGroup(
            VGroup(label(r"equivalent", font_size=24, color=MART),
                   label(r"fair coin and a 60\% coin: any sequence possible under one is possible under the other",
                         font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"not equivalent", font_size=24, color=QC.LOSS),
                   label(r"fair coin and a two-headed coin: ``a tail appears'' is likely under one, impossible under "
                         r"the other", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            wrapped_label(r"why it matters: an arbitrage, a sure profit with no possible loss, is a statement about "
                          r"which events are possible; so it looks the same under every equivalent measure (Part 9).",
                          11.0, 23, Q_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(d, DOWN, buff=0.6)
        with self.voiceover(
            "Two measures are equivalent when they agree on what is impossible, even if they disagree about how "
            "likely everything else is. <bookmark mark='a'/> A fair coin and a sixty-percent coin are equivalent: "
            "any sequence that can happen under one can happen under the other. A fair coin and a two-headed coin "
            "are not: seeing a tail is likely under the first and impossible under the second, and no reweighting "
            "can turn one into the other. <bookmark mark='b'/> This is why finance can price under a convenient "
            "measure. An arbitrage, a profit with no possible loss, is a statement only about what is possible, so "
            "it is the same under every equivalent measure."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(ex[0]))
            self.play(FadeIn(ex[1]))
            vo.wait_until("b")
            self.play(FadeIn(ex[2]))
        self.wait(0.4)
        self.clear_scene()

    def paths(self, m):
        n = m["n"]
        k = np.arange(n + 1)
        g = axes([0, n], [-6, 6], x_length=7.4, y_length=4.6, xlabel=r"tosses", ylabel=r"$L_n = dQ/dP$ on the first $n$ "
                 r"tosses (log scale)", xticks=[0, 100, 200, 300], yticks=[-6, -3, 0, 3, 6],
                 yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        pp = VGroup(*[curve(ax, k, np.clip(np.asarray(p), -6, 6), P_C, stroke_width=1.5).set_stroke(opacity=0.6)
                      for p in m["paths_p"]])
        qq = VGroup(*[curve(ax, k, np.clip(np.asarray(p), -6, 6), Q_C, stroke_width=1.5).set_stroke(opacity=0.6)
                      for p in m["paths_q"]])
        med = curve(ax, k, np.log10(np.asarray(m["median_p"])), WHITE, stroke_width=3.5)
        one = DashedLine(ax.c2p(0, 0), ax.c2p(n, 0), color=GREY_B, stroke_width=2)
        side = VGroup(
            label(r"if the coin is fair ($P$):", font_size=22, color=P_C),
            MathTex(r"\mathbb{E}_P[L_n] = 1 \text{ for every } n", font_size=30),
            MathTex(rf"\text{{median after {n}: }} {m['median_end_p']:.3f}", font_size=30, color=WHITE),
            label(rf"{100 * m['frac_below_001']:.0f}\% of paths end below 0.01", font_size=22, color=GREY_A),
            label(r"if the coin is the 60\% one ($Q$):", font_size=22, color=Q_C),
            label(rf"{100 * m['frac_q_above_100']:.0f}\% of paths end above 100", font_size=22, color=GREY_A),
            wrapped_label(r"$L$ is the wealth of a gambler betting that the coin is $Q$: a fair game if it isn't, a "
                          r"fortune if it is. Testing by betting is a change of measure.", 4.6, 21, MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now follow L as the tosses go on, say for three hundred. Under the fair coin, L is a martingale with "
            "mean one: we built it to average one. <bookmark mark='a'/> Yet look at the paths. Almost all of them "
            "sink toward zero. The median after three hundred tosses is about two thousandths, and two thirds of "
            "the paths end below a hundredth. The mean stays at one only because of a few paths that soar, so rare "
            "that two thousand simulated paths average under a half. A nonnegative martingale must converge, and "
            "this one converges to zero. <bookmark mark='b'/> If the coin really is the sixty-percent one, the same "
            "L grows: two thirds of the paths end above a hundred. <bookmark mark='c'/> Read L as the wealth of a "
            "gambler who bets, toss by toss, that the coin is Q. If it isn't, the gambler is playing a fair game and "
            "almost surely goes broke. If it is, the gambler gets rich. That is the idea behind testing by betting, "
            "in chapter eight."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(side[:2]))
            self.play(LaggedStart(*[Create(p) for p in pp], lag_ratio=0.05, run_time=4))
            vo.wait_until("a")
            self.play(Create(med), FadeIn(side[2:4]))
            vo.wait_until("b")
            self.play(pp.animate.set_stroke(opacity=0.15), LaggedStart(*[Create(p) for p in qq], lag_ratio=0.05,
                                                                       run_time=4), FadeIn(side[4:6]))
            vo.wait_until("c")
            self.play(FadeIn(side[6]))
        self.wait(0.4)
        self.clear_scene()
