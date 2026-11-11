from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, predict, show_card

ITEMS = [
    (r"Goyal, Welch, Zafirov (2024)", r"\textit{RFS} 37(11)", r"29 newer predictors and the original 17: over a third "
     r"fail even in sample, half the rest out of sample", 6),
    (r"Kelly, Malamud, Zhou (2024) vs.\ Nagel (2025)", r"\textit{JF} 79(1); NBER w34104", r"more parameters than "
     r"observations predicts the market; or is it volatility-timed momentum?", 6),
    (r"Lazarus, Lewis, Stock (2021)", r"\textit{Econometrica} 89(5)", r"the size--power frontier of HAR tests; with "
     r"LLSW (2018), the modern recipe", 2),
    (r"Andrews, Kitagawa, McCloskey (2024)", r"\textit{QJE} 139(1)", r"inference on winners: honest intervals for the "
     r"best of many", 13),
    (r"Roth, Sant'Anna, Bilinski, Poe (2023)", r"\textit{J.\ Econometrics} 235(2)", r"what's trending in "
     r"difference-in-differences; Baker--Larcker--Wang (2022) for finance", 14),
    (r"Chernozhukov et al.\ (2024); Maasoumi et al.\ (2024)", r"arXiv 2403.02467; \textit{JAE} 39(3)", r"an open "
     r"textbook of causal ML; automatic debiased ML to pick factors", 15),
    (r"Menkveld et al.; P\'erignon et al.\ (2024)", r"\textit{JF} 79(3); \textit{RFS} 37(11)", r"non-standard errors "
     r"and computational reproducibility", 17),
    (r"Glasserman and Lin (2023)", r"arXiv 2309.17322", r"look-ahead through a language model's training data; a "
     r"``distraction effect'' that is larger in sample", 17),
]


def card(who, venue, what, ch, width=6.3):
    head = VGroup(label(who, font_size=19, color=WHITE), label(venue, font_size=15, color=GREY_B)).arrange(
        DOWN, aligned_edge=LEFT, buff=0.05)
    body = wrapped_label(what, width - 1.3, 16, GREY_A)
    txt = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    badge = VGroup(Circle(radius=0.26, color=QC.IDEA, stroke_width=2).set_fill(QC.IDEA, 0.15),
                   MathTex(str(ch), font_size=24, color=QC.IDEA))
    badge[1].move_to(badge[0])
    row = VGroup(badge, txt).arrange(RIGHT, buff=0.2, aligned_edge=UP)
    box = RoundedRectangle(width=width, height=row.height + 0.25, corner_radius=0.1, stroke_color=GREY_D,
                           stroke_width=1.2, fill_color="#10161E", fill_opacity=1)
    box.move_to(row)
    row.align_to(box, LEFT).shift(RIGHT * 0.12)
    return VGroup(box, row)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.sweep()
        self.complexity()

    def card(self):
        c = chapter_card(18, r"The frontier, 2023--2026", r"What is changing in how we measure?", part=PART)
        with self.voiceover("Chapter eighteen. The frontier, 2023 to 2026."):
            show_card(self, c)
        self.play(FadeOut(c))

    def sweep(self):
        cards = VGroup(*[card(*it) for it in ITEMS])
        grid = VGroup(VGroup(*cards[0::2]).arrange(DOWN, buff=0.18, aligned_edge=LEFT),
                      VGroup(*cards[1::2]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)).arrange(RIGHT, buff=0.25,
                                                                                               aligned_edge=UP)
        if grid.height > 7.4:
            grid.scale_to_fit_height(7.4)
        if grid.width > 13.4:
            grid.scale_to_fit_width(13.4)
        grid.move_to(ORIGIN)
        hint = label(r"the circle: the chapter each paper extends", font_size=17, color=QC.IDEA).to_corner(DR, buff=0.12)
        with self.voiceover(
            "The frontier, paper by paper, each tied to the chapter it extends. Amit Goyal, Ivo Welch and Athanasse "
            "Zafirov's 2024 look at equity premium prediction: most new predictors fail. <bookmark mark='a'/> Bryan "
            "Kelly, Semyon Malamud and Kangying Zhou's virtue of complexity, and Stefan Nagel's reply: an open debate, "
            "next. <bookmark mark='b'/> Eben Lazarus, Daniel Lewis and James Stock's size-power frontier for "
            "heteroskedasticity- and autocorrelation-robust tests, the theory behind chapter two's recommendations. "
            "<bookmark mark='c'/> Isaiah Andrews, Toru Kitagawa and Adam McCloskey's inference on winners: once you "
            "pick the best of many strategies, its estimate is biased upward, and they show how to correct the "
            "estimate and its interval. <bookmark mark='d'/> Jonathan Roth, Pedro Sant'Anna, Alyssa Bilinski and "
            "John Poe's survey of the new difference-in-differences. <bookmark mark='e'/> An open textbook on causal "
            "machine learning by Chernozhukov and coauthors, and Esfandiar Maasoumi and coauthors' automatic debiased "
            "machine learning for choosing factors. <bookmark mark='f'/> The measurement of researchers themselves: "
            "non-standard errors and reproducibility. <bookmark mark='g'/> And a new channel of look-ahead. Paul "
            "Glasserman and Caden Lin asked whether a language model's sentiment scores on old headlines are "
            "contaminated by what the model learned about what happened next. Anonymising the company names, they "
            "found the larger effect in sample was distraction, general knowledge about the company getting in the "
            "way, rather than look-ahead. Part twenty-eight measures it."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2), FadeIn(hint))
            for i, mk in enumerate("abcdefg", 1):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def complexity(self):
        g1 = axes([0, 10], [0, 1], x_length=5.2, y_length=3.2, xlabel=r"model complexity (parameters / observations)",
                  ylabel=r"out-of-sample performance", xticks=[0, 1, 10], yticks=[], font_size=14)
        g2 = axes([0, 10], [-1, 1], x_length=5.2, y_length=3.2, xlabel=r"same method, data with reversals",
                  ylabel=r"performance", xticks=[], yticks=[0], font_size=14)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).shift(UP * 0.35)  # room underneath for the question
        xs = np.linspace(0.05, 10, 80)
        up = curve(g1.ax, xs, 0.15 + 0.6 * (1 - np.exp(-xs / 2)), GOOD, stroke_width=3.5)
        down = curve(g2.ax, xs, -0.1 - 0.5 * (1 - np.exp(-xs / 2)), BAD, stroke_width=3.5)
        t1 = label(r"Kelly--Malamud--Zhou (2024): ``the virtue of complexity''", font_size=19, color=GOOD).next_to(
            g1, UP, buff=0.15)
        t2 = label(r"Nagel (2025): ``seemingly virtuous complexity''", font_size=19, color=BAD).next_to(g2, UP, buff=0.15)
        tag = label(r"schematic, not a reproduction", font_size=16, color=GREY_C).to_edge(DOWN, buff=0.7)
        q = predict(r"A model with more parameters than months of data forecasts the market. What simple strategy "
                    r"might it secretly be?", width=11.0).to_edge(DOWN, buff=0.1)
        with self.voiceover(
            "The debate, in a picture. Kelly, Malamud and Zhou showed in 2024 that predicting the market with thousands "
            "of random nonlinear features of a few predictors, far more parameters than observations, did better out of "
            "sample as complexity grew, against the textbook intuition of chapter six. <bookmark mark='a'/> Nagel replied "
            "in 2025: with short training windows, such a forecast becomes a weighted average of recent returns, "
            "weighted by how similar today's predictors are to the past's, and since similarity falls when predictors "
            "are volatile, it is a volatility-timed momentum strategy. On artificial data where returns reverse instead, "
            "the same machine builds the same momentum bet, and loses. Both sides are on the record; the question is "
            "open, and Part twenty-seven returns to it. <bookmark mark='b'/> Pause and predict: what simple strategy "
            "might a model with more parameters than months be? Momentum, if Nagel is right."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(t1), Create(up), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g2), FadeIn(t2), Create(down))
            vo.wait_until("b")
            self.play(FadeOut(tag), FadeIn(q))
        self.wait(0.4)
        self.clear_scene()
