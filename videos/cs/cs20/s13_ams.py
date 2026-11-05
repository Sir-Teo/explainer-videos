from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Ams(VoiceoverScene):
    def construct(self):
        self.card()
        self.moments()
        self.sketch()
        self.measured()

    def card(self):
        card = chapter_card(12, r"Sketching the second moment", r"How skewed is a stream?", lit=(1996,),
                            extra=((1996, r"Alon, Matias and Szegedy"),), part=PART)
        with self.voiceover("Chapter twelve. Sketching the second moment."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def moments(self):
        d = load("ams")
        head = label(r"Frequency moments", font_size=36).to_edge(UP, buff=0.35)
        f = MathTex(r"F_p = \sum_x f_x^{\,p}", font_size=44, color=YES).next_to(head, DOWN, buff=0.5)
        rows = VGroup(
            label(r"$F_0$: \ the number of distinct items \ (the last chapter)", font_size=24, color=DATA),
            label(r"$F_1$: \ the length of the stream \ (one counter)", font_size=24, color=GREY_A),
            label(r"$F_2$: \ the sum of squared counts: \ how concentrated the stream is", font_size=24, color=LAM),
            label(r"a database's join of a table with itself has $F_2$ rows; \ a network sees $F_2$ jump in an "
                  r"attack", font_size=20, color=GREY_A),
            label(rf"the novels: \ $F_2 = {d['f2']:,}$".replace(",", "{,}") +
                  rf"; \ the word \textit{{the}} alone is {d['the'] * 100:.0f}\% of it", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(f, DOWN, buff=0.5)
        with self.voiceover(
            "Counting distinct items and counting the stream's length are two cases of one family. <bookmark "
            "mark='a'/> The p-th frequency moment is the sum, over items, of each item's count to the power p. "
            "<bookmark mark='b'/> F zero is the number of distinct items, the last chapter. <bookmark mark='c'/> F "
            "one is the length of the stream, which one counter tracks. <bookmark mark='d'/> F two, the sum of the "
            "squared counts, measures how concentrated the stream is. <bookmark mark='e'/> It is the number of rows "
            "when a database joins a table with itself on that column, and it jumps when a network sees a flood "
            "of identical packets. <bookmark mark='f'/> For the novels it is a hundred and seventy-seven billion, "
            "and the word the contributes thirty percent of it on its own. Can we estimate F two without counting "
            "every word?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(f))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.wait(0.3)
        self.clear_scene()

    def sketch(self):
        head = label(r"Alon, \ Matias and Szegedy: \ one random sign per item", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"give each item a random sign $s_x = \pm 1$; \ keep one number, \ $Z$, \ adding $s_x$ for every "
                  r"arrival of $x$", font_size=21, color=WHITE),
            MathTex(r"Z = \sum_x s_x f_x \qquad Z^2 = \sum_x f_x^2 + \sum_{x \ne y} s_x s_y\, f_x f_y", font_size=34,
                    color=LAM),
            MathTex(r"\mathbb{E}[s_x s_y] = 0 \;\Longrightarrow\; \mathbb{E}[Z^2] = F_2", font_size=36, color=YES),
            MathTex(r"\operatorname{Var}[Z^2] \le 2F_2^2 \quad \text{(needs only 4-wise independent signs)}",
                    font_size=32, color=HEAD),
            label(r"average $k$ copies: \ error $\sqrt{2/k}$; \ then the median of a few averages: \ confidence",
                  font_size=21, color=WHITE),
            label(r"the median of means: \ Chebyshev for each mean, \ Chernoff for the median", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Noga Alon, Yossi Matias and Mario Szegedy showed how in 1996, in the paper that started the theory of "
            "streaming. <bookmark mark='a'/> Give every item a random sign, plus or minus one, and keep a single "
            "number Z: each time an item arrives, add its sign. <bookmark mark='b'/> At the end, Z is the sum of "
            "each item's sign times its count. Square it. You get the squared counts, which is F two, plus cross "
            "terms, each a product of two different signs. <bookmark mark='c'/> Independent signs multiply to zero "
            "on average, so the expected value of Z squared is exactly F two. <bookmark mark='d'/> Its variance is "
            "at most twice F two squared, and that calculation needs only four-wise independent signs, which a "
            "small hash function supplies. <bookmark mark='e'/> Averaging k copies brings the relative error down "
            "to root two over k, and the median of a few such averages makes large errors exponentially unlikely. "
            "<bookmark mark='f'/> The median of means is a trick worth remembering: Chebyshev's inequality for "
            "each mean, a Chernoff bound for the median."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("ams")
        head = label(r"Measured on the novels", font_size=34).to_edge(UP, buff=0.35)
        one = np.array(d["single"])
        hist, edges = np.histogram(one, bins=24, range=(0, 4))
        top = hist.max()
        bars = VGroup(*[Rectangle(width=0.2, height=max(2.2 * h / top, 0.02), stroke_width=0, fill_color=LAM,
                                  fill_opacity=0.85) for h in hist])
        for i, b in enumerate(bars):
            b.move_to([-6.2 + i * 0.23, -0.3 + b.height / 2, 0])
        ax = Line([-6.35, -0.3, 0], [-6.35 + 24 * 0.23, -0.3, 0], color=GREY_C)
        mean_x = -6.2 + (1.0 / (4 / 24)) * 0.23 - 0.115
        mean = DashedLine([mean_x, -0.3, 0], [mean_x, 2.1, 0], color=HEAD)
        ticks = VGroup(*[label(str(v), font_size=16, color=GREY_B).move_to([-6.2 + (v / (4 / 24)) * 0.23 - 0.115,
                                                                            -0.55, 0]) for v in (0, 1, 2, 3, 4)])
        cap = label(rf"400 single estimates $Z^2 / F_2$ \ ({int((one > 4).sum())} beyond 4 not shown): \ mean "
                    rf"{d['single_mean']:.2f}", font_size=19,
                    color=GREY_A).next_to(ax, DOWN, buff=0.45)
        rows = [[str(r["k"]), f"{r['rmse_mean'] * 100:.0f}\\%", f"{r['theory'] * 100:.0f}\\%",
                 f"{r['worst_mean'] * 100:.0f}\\%", f"{r['worst_median9'] * 100:.0f}\\%"] for r in d["rows"]]
        tab = grid_table([r"$k$", r"error", r"$\sqrt{2/k}$", r"worst mean", r"worst median of 9"], rows,
                         widths=[0.9, 1.3, 1.4, 1.7, 2.3], row_h=0.42, font_size=18, mono_cols=(),
                         colors=[[GREY_A, YES, HEAD, NO, YES]] * len(rows)).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        note_ = label(r"40 trials per row; \ memory: \ $9k$ numbers", font_size=18, color=GREY_A
                      ).next_to(tab, DOWN, buff=0.3)
        with self.voiceover(
            "On the novels. <bookmark mark='a'/> One copy of the sketch is wild: here are four hundred single "
            "estimates of F two, each divided by the truth. They scatter from nearly zero to several times too "
            "big, now and then ten times, but their average is right. <bookmark mark='b'/> Averaging k copies tightens them as "
            "predicted, about root two over k. <bookmark mark='c'/> And the median of nine averages cuts off the "
            "occasional bad average. With sixty-four copies in each of nine groups, the worst of forty trials was "
            "off by seventeen percent, from fewer than six hundred numbers. Each copy of Z is a dot product of the "
            "count vector with random signs, a random projection, the Johnson–Lindenstrauss idea from the AI "
            "series, and because it is linear, sketches of two streams simply add."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), Create(mean), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r[:3])) for r in tab.cells[1:]], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*r[3:])) for r in tab.cells[1:]], lag_ratio=0.25), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
