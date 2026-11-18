from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Ams(WatchScene):
    def construct(self):
        self.card()
        self.moments()
        self.sketch()

    def card(self):
        self.chapter(12, r"Sketching the second moment", r"How skewed is a stream?", lit=(1996,), extra=((1996, r"Alon, Matias and Szegedy"),), part=PART, said='Chapter twelve. Sketching the second moment.')

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
        self.ask(r"Give each item a random sign; sum them; square. \\ The expected value is...",
                 [r"the number of distinct items", r"$\sum_i f_i^2$, the second moment"], 1,
                 say="Give every item a random sign, add up the signed stream, and square it. What's the expected value?",
                 reveal="The second frequency moment: cross terms cancel in expectation.")
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

