from __future__ import annotations

import numpy as np

from videos.stats.stats10.common import *  # noqa: F403


def cup(milk_first: bool | None, r=0.32):
    body = RoundedRectangle(width=r * 1.7, height=r * 1.5, corner_radius=0.08, stroke_color=GREY_B, stroke_width=2,
                            fill_color="#2a2118", fill_opacity=1)
    handle = Arc(radius=r * 0.35, start_angle=-PI / 2, angle=PI, color=GREY_B, stroke_width=2).next_to(body, RIGHT, buff=-0.02)
    g = VGroup(body, handle)
    if milk_first is not None:
        tag = Circle(radius=r * 0.28, stroke_width=0, fill_color="#F2EBDD" if milk_first else "#7A4E2A", fill_opacity=1).move_to(body)
        g.add(tag)
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.arbuthnot()
        self.years()
        self.tea()
        self.objectives()

    def arbuthnot(self):
        tl = timeline(lit=(1710,)).to_edge(UP, buff=0.35)
        hc = history_card(1710, r"John Arbuthnot, \ physician to Queen Anne", r"``An argument for divine providence, taken from the "
                          r"constant regularity observed in the births of both sexes'', \ \emph{Philosophical Transactions} 27",
                          color=DATA, width=8.6, font_size=24).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"London's christenings, \ 1629 to 1710: \ more boys than girls in every one of 82 years", font_size=26),
            label(r"if years were independent fair coins, \ the chance of 82 heads in a row:", font_size=26, color=GREY_A),
            MathTex(r"\big(\tfrac12\big)^{82} \approx 2.1 \times 10^{-25}", font_size=40, color=OBS),
        ), 12.6, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1710, John Arbuthnot, physician to Queen Anne, satirist and friend of Jonathan "
            "Swift, read a paper to the Royal Society with a theological title: an argument for divine providence, "
            "taken from the constant regularity in the births of both sexes. <bookmark mark='b'/> He had the London "
            "christening records for the eighty-two years from 1629 to 1710, and in every single year more boys had "
            "been christened than girls. <bookmark mark='c'/> Suppose, he said, that years are independent, each like a fair coin, "
            "equally likely to favour boys or girls. Then the chance of boys winning eighty-two years in a row is "
            "<bookmark mark='d'/> one half to the power eighty-two: about two in ten to the twenty-five. Chance can't "
            "explain it, he concluded; it must be art, by which he meant Providence."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def years(self):
        d = load("arbuthnot")
        yrs, sh = np.asarray(d["years"]), np.asarray(d["share"])
        A = axes([1629, 1710], [0.49, 0.54], x_length=10.0, y_length=3.4, xlabel=r"year", ylabel=r"share of christenings that were boys",
                 xticks=[1630, 1650, 1670, 1690, 1710], yticks=[0.49, 0.5, 0.51, 0.52, 0.53, 0.54], yfmt=lambda v: f"{v:.2f}",
                 center=[0, 0.6, 0])
        ax = A.ax
        half = DashedLine(ax.c2p(1629, 0.5), ax.c2p(1710, 0.5), color=GREY_B, stroke_width=2)
        hl = MathTex(r"\tfrac12", font_size=26, color=GREY_B).next_to(ax.c2p(1710, 0.5), RIGHT, buff=0.1)
        dots = VGroup(*[Dot(ax.c2p(y, s_), radius=0.05, color=DATA) for y, s_ in zip(yrs, sh)])
        signs = VGroup(*[MathTex("+", font_size=22, color=OBS) for _ in yrs]).arrange(RIGHT, buff=0.02)
        signs.width = 10.0
        signs.move_to([0, -1.8, 0])
        rows = fit_rows(VGroup(
            label(rf"in all: \ {d['males']:,} boys, \ {d['females']:,} girls, \ a ratio of {d['ratio']:.3f}", font_size=24),
            label(r"the first published significance test: \ a null hypothesis, \ a statistic, \ a tail probability", font_size=26,
                  color=OBS),
        ), 12.6, 0.28, [0, -2.75, 0])
        src = historical_tag(r"Arbuthnot (1710), \ via HistData", corner=UR)
        with self.voiceover(
            "Here are his data. <bookmark mark='a'/> Each dot is a year, and its height is the share of the year's "
            "christenings that were boys. The plague years, the Civil War and the Great Fire are all in there, and the "
            "numbers swing, from about fifty point three to fifty-three point six percent. <bookmark mark='b'/> But "
            "every dot is above one half. Eighty-two plus signs. <bookmark mark='c'/> Over the whole period, nearly "
            "four hundred and eighty-five thousand boys and four hundred and fifty-four thousand girls. "
            "<bookmark mark='d'/> Arbuthnot's argument has every ingredient of a modern significance test: a null "
            "hypothesis, that each year is a fair coin; a statistic, the number of years boys won; and the probability, "
            "under the null, of a result at least that extreme. His conclusion about Providence, we'll come back to."
        ) as vo:
            self.play(FadeIn(A), Create(half), FadeIn(hl), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt, scale=0.5) for dt in dots], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in signs], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def tea(self):
        d = load("tea")
        truth = [True, False, False, True, True, False, True, False]
        cups = VGroup(*[cup(None) for _ in truth]).arrange(RIGHT, buff=0.55).move_to([0, 2.0, 0])
        milk = VGroup(*[cup(t) for t in truth]).arrange(RIGHT, buff=0.55).move_to([0, 2.0, 0])
        hc = history_card(1935, r"R. A. Fisher, \ \emph{The Design of Experiments}, \ ch.~2",
                          r"a lady (Muriel Bristol, \ an algologist at Rothamsted) \ claims she can tell whether the milk or the tea "
                          r"was poured first", color=DATA, width=8.4, font_size=22).move_to([0, 0.2, 0])
        rows = fit_rows(VGroup(
            label(r"eight cups, \ four of each, \ in random order; \ she must pick the four milk-first cups", font_size=26),
            MathTex(r"\binom84 = 70 \text{ ways to choose; \ by guessing, \ all four right with probability } \tfrac{1}{70} \approx 1.4\%",
                    font_size=30, color=OBS),
            label(r"the story goes that she got them all right", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "Two centuries later, at the Rothamsted agricultural station in the 1920s, a colleague of Fisher's, the "
            "algologist Muriel Bristol, declined a cup of tea because the milk had been poured in after the tea. She "
            "said she could taste the difference. <bookmark mark='a'/> Fisher told the story in 1935, in the second "
            "chapter of The Design of Experiments, as the model of how to test such a claim. <bookmark mark='b'/> "
            "Prepare eight cups, four with the milk first and four with the tea first, and present them in random "
            "order. She must pick out the four milk-first cups. <bookmark mark='c'/> There are seventy ways to choose "
            "four cups out of eight. If she can't taste anything, each is equally likely, and she gets all four right "
            "with probability one in seventy, under one and a half percent. <bookmark mark='d'/> According to the "
            "story, told decades later by a witness, she got every cup right. But the design, not the result, was "
            "Fisher's point: the randomization itself creates the null distribution."
        ) as vo:
            self.play(FadeIn(cups))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), Transform(cups, milk))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 10", font_size=34, color=GREY_B), label(r"Significance", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Fisher's logic: \ a null, \ a statistic, \ a tail probability; \ exact tests that come from the design",
            r"the $p$-value: \ null calibration, \ and behavior under alternatives",
            r"Neyman and Pearson: \ two errors, \ size and power, \ the most powerful test, \ the likelihood ratio",
            r"the everyday tests: \ $z$, \ $t$, \ Welch, \ permutation, \ Pearson's $\chi^2$",
            r"power and sample size; \ peeking; \ what $p$-values are not; \ many tests at once",
        ], color=OBS, font_size=26)
        prereq = note(r"prerequisites: \ Parts 8 and 9").to_corner(DL, buff=0.3)
        built = note(r"built: \ the permutation machine; \ \texttt{statkit.tests}").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part ten: significance. <bookmark mark='b'/> We'll build Fisher's logic of the "
            "significance test and the exact tests that come from randomization; the p-value and its distribution; "
            "Jerzy Neyman and Egon Pearson's rival theory of two kinds of error, with its most powerful tests and the "
            "likelihood ratio; the everyday tests, from z and t to Welch and Pearson's chi-squared; and then the ways it "
            "all goes wrong: too little power, peeking at the data, misreading the p-value, and testing many things at "
            "once. Along the way we build a permutation machine, and a module of tests you can read line by line."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
