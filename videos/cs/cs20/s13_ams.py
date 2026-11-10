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
        with self.voiceover((
            'Chapter twelve. Sketching the second moment.'
        )):
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
            (
            "Counting distinct items and counting the stream's length are two cases of one family. <bookmark "
            "mark='a'/> The p-th frequency moment is the sum, over items, of each item's count to the power p. "
            "<bookmark mark='b'/> F zero is the number of distinct items, the last chapter. <bookmark mark='c'/> F "
            "one is the length of the stream, which one counter tracks. <bookmark mark='d'/> F two, the sum of the "
            "squared counts, measures how concentrated the stream is. <bookmark mark='e'/> It is the number of rows "
            'when a database joins a table with itself on that column, and it jumps when a network sees a flood of '
            "identical packets. <bookmark mark='f'/> For the novels it is a hundred and seventy-seven billion, and "
            'the word the contributes thirty percent of it on its own. Can we estimate F two without counting every '
            'word?'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(f))
            vo.wait_until("a")
            self.play(Indicate(f, color=YES))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.wait(0.3)
        self.clear_scene()

    def sketch(self):
        head = label(r"Alon, \ Matias and Szegedy: \ one random sign per item", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"consistent signs: \ $s_a=+1$, \ $s_b=-1$, \ $s_c=+1$; \ each arrival adds its sign",
                  font_size=20, color=WHITE),
            MathTex(r"Z=\sum_x s_xf_x,\qquad Z^2=F_2+\sum_{x\ne y}s_xs_yf_xf_y", font_size=31, color=LAM),
            MathTex(r"\mathbb E[Z^2]=F_2\quad\text{(unbiased pairwise-independent signs)}", font_size=29, color=YES),
            MathTex(r"\operatorname{Var}(Z^2)\le2F_2^2\quad\text{(4-wise independence)}", font_size=29, color=HEAD),
            label(r"average $k$ copies: \ relative SD $\le\sqrt{2/k}$; \ threshold + groups give confidence",
                  font_size=19, color=WHITE),
            label(r"Chebyshev for each mean; \ independent groups + Chernoff for the median", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.28)
        trace = grid_table([r"arrival", "a", "b", "a", "c", "b", "a"],
                           [[r"add sign", "+1", "-1", "+1", "+1", "-1", "+1"],
                            [r"counter $Z$", "1", "0", "1", "2", "1", "2"]],
                           widths=[2.1]+[1.05]*6, row_h=0.36, font_size=19, mono_cols=(),
                           colors=[[GREY_A]+[DATA,NO,DATA,YES,NO,DATA], [LAM]+[LAM]*6])
        trace.to_edge(DOWN, buff=0.85).set_x(0)
        witness = label(r"this sign choice: \ $Z^2=4$; \ truth $F_2=3^2+2^2+1^2=14$; \ all 8 signs: \ mean 14",
                        font_size=20, color=HEAD).to_edge(DOWN, buff=0.32)
        with self.voiceover(
            (
            "Alon, Matias and Szegedy gave a foundational streaming result in 1996. <bookmark mark='a'/> Assign "
            'every item a consistent random sign, plus or minus one. On each arrival add its sign to counter Z. In '
            'the worked six-arrival stream, the counter ends at two, so this one squared estimate is four; the true '
            "second moment is fourteen. <bookmark mark='b'/> Algebraically, Z squared is the sum of squared "
            "frequencies plus cross terms involving two different signs. <bookmark mark='c'/> Unbiased pairwise-"
            'independent signs make those cross terms vanish in expectation. Averaging over all eight sign '
            "assignments in this three-item example gives exactly fourteen. <bookmark mark='d'/> Four-wise "
            "independence gives variance at most twice F two squared. <bookmark mark='e'/> Averaging k independent "
            'counters gives relative standard deviation at most the square root of two divided by k. Chebyshev '
            'bounds a chosen error threshold; independent groups and their median amplify confidence. <bookmark '
            "mark='f'/> This is the median-of-means construction: a standard-error scale becomes a probability "
            'statement only after specifying the threshold and group count.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(trace), FadeIn(witness))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
                if mk == "a":
                    self.play(Indicate(VGroup(*trace.cells[2][1:]), color=LAM))
                if mk == "c":
                    self.play(Indicate(witness, color=YES))
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
        tab = grid_table([r"$k$", r"RMSE", r"$\sqrt{2/k}$", r"worst mean", r"worst median of 9"], rows,
                         widths=[0.9, 1.3, 1.4, 1.7, 2.3], row_h=0.42, font_size=18, mono_cols=(),
                         colors=[[GREY_A, YES, HEAD, NO, YES]] * len(rows)).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        note_ = label('40 trials per row; \\ modeled counters: $9k$ \\\\ exact input count vector stored separately', font_size=18, color=GREY_A
                      ).next_to(tab, DOWN, buff=0.3)
        with self.voiceover(
            (
            (
            "On the novels. <bookmark mark='a'/> The histogram contains four hundred single-counter squared "
            'estimates divided by the exact second moment. Individual estimates vary widely. Their empirical average'
            " is a finite statistic; unbiasedness refers to expectation over signs. <bookmark mark='b'/> Independent"
            " averages tighten the spread, consistent with the square-root scale. <bookmark mark='c'/> These "
            'experiments retain an exact frequency vector as input; the displayed counter budget excludes that '
            'vector. The table reports forty trials per configuration and the worst errors actually observed, '
            'including the median of nine groups. Those maxima are not future-error guarantees. The counters form '
            'linear random projections, so compatible unsquared counters for two streams can be added. Squared '
            'estimates themselves cannot simply be added.'
        )
        )
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
