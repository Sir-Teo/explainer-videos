from __future__ import annotations

import numpy as np

from videos.stats.stats35.common import *  # noqa: F403


class Blocks(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.estimator()
        self.compare()
        self.pairs()
        self.rerand()
        self.lesson()

    def card(self):
        card = chapter_card(6, r"Blocking and pairing", r"Randomize within similar units", lit=(1935,), part=PART)
        with self.voiceover("Chapter six. Blocking and pairing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        d = load("blocks")
        rows = fit_rows(VGroup(
            label(r"Part 13: \ block on the soil gradient; \ here: \ block on the baseline pressure", font_size=26),
            label(rf"baseline predicts $Y(0)$: \ correlation {d['corr_base_y0']:.2f}", font_size=26, color=Y0C),
            label(r"sort the 2,000 by baseline; \ ten blocks of 200; \ randomize 100 and 100 within each", font_size=26),
            label(r"between-block imbalance is removed; \ within-block imbalance remains", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 13 blocked a field trial on the soil gradient. The same idea works for patients. "
            "<bookmark mark='b'/> A patient's baseline pressure strongly predicts their pressure twelve weeks later, with "
            "correlation " + say(d["corr_base_y0"]) + ". <bookmark mark='c'/> So sort the two thousand patients by baseline, "
            "cut them into ten blocks of two hundred, and randomize a hundred to each arm within every block. <bookmark "
            "mark='d'/> Then the arms cannot differ much in baseline by bad luck, because every block is split exactly in "
            "half."
        ) as vo:
            self.add(trial_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def estimator(self):
        rows = [
            cmath(r"\hat\tau_{\rm block}", r"=", r"\textstyle\sum_b \frac{n_b}{n}\, \hat\tau_b", font_size=32),
            cmath(r"\mathrm{Var}", r"=", r"\textstyle\sum_b \big(\frac{n_b}{n}\big)^2 \mathrm{Var}\,\hat\tau_b", font_size=32),
            cmath(r"\text{gain}", r":", r"\text{only within-block variation remains}", font_size=32),
            cmath(r"\text{roughly}", r":", r"\mathrm{Var} \times (1 - R^2_{\rm block})", font_size=32),
        ]
        rows[0][-1].set_color(BANDC)
        whys = [why(r"a weighted average of block estimates"), why(r"independent randomizations"),
                why(r"between-block differences cancel"), why(r"$R^2$ of the outcome on the blocks")]
        with self.voiceover(
            "<bookmark mark='a'/> The blocked estimate is the average of the ten within-block differences, weighted by the "
            "blocks' sizes. <bookmark mark='b'/> Its variance is the weighted sum of the blocks' Neyman variances, since "
            "each block is randomized separately. <bookmark mark='c'/> The differences between blocks, the high-pressure "
            "patients against the low, no longer enter at all. <bookmark mark='d'/> Roughly, the variance shrinks by the "
            "share of the outcome's variation that the blocks explain."
        ) as vo:
            intro=label('Independent block assignments permit weighted estimation',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        d = load("blocks")
        names = [("complete", r"complete randomization", GREY_B), ("blocked", r"10 blocks by baseline", BANDC),
                 ("paired", r"1,000 matched pairs", TAUC)]
        A = axes([0, 3], [0, 0.5], x_length=6.4, y_length=4.2, xlabel=r"", ylabel=r"SD of $\hat\tau$ (mm Hg)",
                 xticks=[], yticks=[0, 0.25, 0.5], center=[-2.6, 0.3, 0])
        ax = A.ax
        bars = VGroup(*[bars_at(ax, [k + 0.5], [d[n]["sd"]], 0.6, c) for k, (n, _, c) in enumerate(names)])
        labs = VGroup(*[label(t, font_size=18, color=c).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.2) for k, (_, t, c) in enumerate(names)])
        nums = VGroup(*[label(rf"{d[n]['sd']:.3f}", font_size=20, color=c).next_to(b, UP, buff=0.08) for b, (n, _, c) in zip(bars, names)])
        side = fit_rows(VGroup(
            label(r"1,500 randomizations of each design", font_size=22),
            label(rf"blocking: \ variance $\times$ {(d['blocked']['sd'] / d['complete']['sd']) ** 2:.2f}", font_size=22, color=BANDC),
            label(rf"pairing: \ $\times$ {(d['paired']['sd'] / d['complete']['sd']) ** 2:.2f}", font_size=22, color=TAUC),
            label(r"all unbiased: \ means " + rf"{d['complete']['mean']:.2f}, \ {d['blocked']['mean']:.2f}, \ {d['paired']['mean']:.2f}", font_size=20, color=GREY_A),
        ), 4.6, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fifteen hundred randomizations of each design on the World's patients. <bookmark "
            "mark='b'/> Complete randomization: a standard deviation of " + say(d["complete"]["sd"], 3) + ". Ten blocks: "
            + say(d["blocked"]["sd"], 3) + ", <bookmark mark='c'/> which is a variance cut by two fifths, as if the trial had been sixty percent "
            "larger. <bookmark mark='d'/> Pairing the sorted patients two by two gains a little more. All three are "
            "unbiased; these baseline blocks improve precision in this example before any outcome is seen."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(A), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), FadeIn(nums[:2]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(nums[2]), FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def pairs(self):
        rows = [
            cmath(r"\hat\tau_{\rm pair}", r"=", r"\tfrac1J \textstyle\sum_j d_j, \ \ d_j = Y_{j,\rm treated} - Y_{j,\rm control}", font_size=28),
            cmath(r"\widehat{\mathrm{Var}}", r"=", r"\tfrac{1}{J(J-1)} \textstyle\sum_j (d_j - \bar d)^2", font_size=30),
            cmath(r"\text{conservative}", r":", r"\text{by the variance of the pairs' true effects}", font_size=30),
            cmath(r"\text{a pair}", r":", r"\text{one treated, \ one control: \ no within-pair variance}", font_size=28),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"Imai (2008)"), why(r"from the spread of the pair differences"),
                why(r"Neyman again"), why(r"so it cannot be estimated pair by pair")]
        with self.voiceover(
            "<bookmark mark='a'/> In a matched-pair design, the estimate is the average of the within-pair "
            "differences. <bookmark mark='b'/> Its variance is estimated from the spread of those differences. "
            "<bookmark mark='c'/> As Kosuke Imai showed in 2008, this is again conservative, by the variation in the "
            "pairs' true average effects. <bookmark mark='d'/> With one treated and one control unit per pair, there "
            "is no way to estimate the variance within a pair, Small blocks of four or more allow separate within-arm"
            " variance estimates; matched pairs instead use variation across pair differences."
        ) as vo:
            intro=label('Matched-pair variance is estimated across pairs',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rerand(self):
        rows = fit_rows(VGroup(
            label(r"rerandomization: \ draw again until the arms balance on the covariates", font_size=26),
            label(r"Morgan \& Rubin (2012): \ accept only if the Mahalanobis imbalance is small", font_size=26, color=GREY_A),
            label(r"valid if the analysis respects the rule \ (Li, \ Ding \& Rubin 2018)", font_size=26, color=BANDC),
            label(r"blocking for continuous covariates, \ in effect", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A related design is rerandomization: draw the assignment, check the balance of the "
            "covariates, and if it is poor, draw again. <bookmark mark='b'/> Kari Lock Morgan and Rubin formalized it in "
            "2012, accepting only draws whose Mahalanobis imbalance is below a threshold. <bookmark mark='c'/> Xinran Li, "
            "Ding and Rubin worked out its asymptotic theory in 2018: valid, and more precise, provided the analysis takes "
            "the acceptance rule into account. <bookmark mark='d'/> It is blocking for continuous covariates, in effect."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"`block what you can, \ randomize what you cannot'", font_size=28, color=BANDC),
            label(r"Box, \ Hunter \& Hunter (1978)", font_size=22, color=GREY_A),
            label(r"next: \ adjusting for covariates after the fact, \ instead of before", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The rule of thumb is old: block what you can, and randomize what you cannot, <bookmark "
            "mark='b'/> in the words of George Box, William Hunter and Stuart Hunter. <bookmark mark='c'/> But often the "
            "covariates are only used after the trial, in the analysis. Is that as good?"
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
