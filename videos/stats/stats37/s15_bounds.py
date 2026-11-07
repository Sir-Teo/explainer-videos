from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class Bounds(VoiceoverScene):
    def construct(self):
        self.card()
        self.manski_idea()
        self.manski_numbers()
        self.lee_problem()
        self.lee_math()
        self.lee_numbers()
        self.law()

    def card(self):
        card = chapter_card(14, r"Bounds", r"When no design identifies the answer, \ say what the data rule out",
                            lit=(1990, 2009), part=PART)
        with self.voiceover("Chapter fourteen. Bounds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def manski_idea(self):
        rows = [
            cmath(r"E[Y]", r"=", r"p\, E[Y \mid \text{observed}] + (1 - p)\, E[Y \mid \text{missing}]", font_size=30),
            cmath(r"Y \in [0, 1]", r"\Rightarrow", r"E[Y \mid \text{missing}] \in [0, 1]", font_size=30),
            cmath(r"E[Y]", r"\in", r"[\,p\, \bar y_{\text{obs}},\ \ p\, \bar y_{\text{obs}} + 1 - p\,]", font_size=30),
            cmath(r"\text{width}", r"=", r"1 - p: \ \text{the share missing}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"the law of total probability"), why(r"the data say nothing about the missing"),
                why(r"Manski (1990): \ no missingness model; bounded outcomes"), why(r"never shrinks with $n$")]
        with self.voiceover(
            "<bookmark mark='a'/> Charles Manski's starting point, in 1990, was to ask what the data say with no "
            "assumptions at all. Suppose an outcome is missing for some people. Its mean is a mixture of the mean "
            "among those observed and among those missing. <bookmark mark='b'/> The data say nothing about the "
            "missing, except that a yes-or-no outcome lies between zero and one. <bookmark mark='c'/> So the mean "
            "lies in an interval: the worst case, where every missing person scored zero, and the best, where every "
            "one scored one. <bookmark mark='d'/> Its width is the share missing. It does not shrink as the sample "
            "grows; a smaller missing share or stronger justified assumptions can narrow it."
        ) as vo:
            intro=label('Bounded outcomes imply worst-case bounds without a missingness model',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def manski_numbers(self):
        d = load("bounds")
        m = d["manski"]
        A = axes([-0.3, 0.45], [0, 1], x_length=8.0, y_length=2.2, xlabel=r"effect of training on employment", ylabel=r"",
                 xticks=[-0.2, 0, 0.2, 0.4], yticks=[], xfmt=lambda v: f"{v:g}", center=[-1.0, -1.0, 0])
        ax = A.ax
        seg = Line(ax.c2p(m["lo"], 0.5), ax.c2p(m["hi"], 0.5), color=BANDC, stroke_width=10)
        tr = Dot(ax.c2p(d["truth_emp"], 0.5), radius=0.1, color=TRUEC)
        nv = Dot(ax.c2p(d["resp_naive"], 0.5), radius=0.07, color=MISSC)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"a training experiment, \ 4,000 workers; \ the follow-up survey reaches", font_size=24),
            label(rf"{100 * d['resp1']:.0f}\% of the trained and {100 * d['resp0']:.0f}\% of the others", font_size=24, color=MISSC),
            label(rf"plug-in bounds under random treatment: \ employment effect in [{m['lo']:.2f}, \ {m['hi']:.2f}]", font_size=24, color=BANDC),
            label(rf"the truth \ (gold): \ {d['truth_emp']:.3f}; \ respondents only \ (red): \ {d['resp_naive']:.3f}", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, 1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A seeded example: a randomized training programme for four thousand workers, with "
            "employment measured by a follow-up survey. <bookmark mark='b'/> The survey reaches " + str(round(100 * d["resp1"]))
            + " percent of the trained and " + str(round(100 * d["resp0"])) + " percent of the others. <bookmark mark='c'/> With no assumption about the people it missed, the "
            "effect on employment lies between minus " + say(-m["lo"], 2) + " and " + say(m["hi"], 2) + ": a width of a "
            "half, the two missing shares added. The data cannot even sign the effect. <bookmark mark='d'/> Here, as it "
            "happens, the respondents give nearly the right answer, but nothing in the data could have told us so."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(zero))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
                if m_ == "c":
                    self.play(Create(seg))
                if m_ == "d":
                    self.play(FadeIn(tr), FadeIn(nv))
        self.clear_scene()

    def lee_problem(self):
        d = load("bounds")
        rows = fit_rows(VGroup(
            label(r"a harder problem: \ the effect of training on wages", font_size=26, color=TAUC),
            label(rf"wages exist only for the employed: \ {100 * d['emp1']:.0f}\% of the trained, \ {100 * d['emp0']:.0f}\% of the others", font_size=26),
            label(r"training draws in marginal workers, \ who earn little", font_size=26, color=MISSC),
            label(rf"comparing employed wages: \ +{d['naive']:.2f} an hour; \ the effect on those always employed: \ +1.00", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A harder problem: the effect of training on wages. <bookmark mark='b'/> Wages exist only "
            "for people who are employed: " + str(round(100 * d["emp1"])) + " percent of the trained, "
            + str(round(100 * d["emp0"])) + " percent of the others. Randomization balanced the groups, but employment did "
            "not. <bookmark mark='c'/> Training draws marginal workers into jobs, and they earn little. <bookmark mark='d'/> "
            "So comparing the wages of the employed gives plus " + say(d["naive"], 2) + " dollars an hour, though for the "
            "workers who would be employed either way the effect is a full dollar. The comparison is not of like with like."
        ) as vo:
            self.add(seeded_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lee_math(self):
        rows = [
            cmath(r"\text{assume}", r":", r"\text{training never stops anyone working (monotonicity)}", font_size=30),
            cmath(r"p", r"=", r"\dfrac{P(\text{employed} \mid T{=}1) - P(\text{employed} \mid T{=}0)}{P(\text{employed} \mid T{=}1)}", font_size=30),
            cmath(r"\text{trim}", r":", r"\text{the top or bottom } p \text{ of the trained workers' wages}", font_size=30),
            cmath(r"\text{bounds}", r":", r"\text{the two trimmed means, \ minus the controls' mean}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"Lee (2009); random treatment and monotone selection"), why(r"the share of trained workers who are marginal"),
                why(r"they are somewhere in there"), why(r"for the always-employed")]
        with self.voiceover(
            "<bookmark mark='a'/> In this randomized experiment, David Lee's 2009 bounds additionally assume that "
            "training never stops anyone working, with consistent treatment and well-defined selection and wage "
            "outcomes. Then the employed trained workers are the always-employed plus some marginal workers, and the "
            "employed controls are the always-employed alone. <bookmark mark='b'/> The share of employed trained "
            "workers who are marginal is the difference in employment rates, divided by the trained rate. <bookmark "
            "mark='c'/> We do not know which ones they are. In the worst case they are the highest earners; in the "
            "best, the lowest. So trim that share from the top, and then from the bottom, of the trained workers' "
            "wages. <bookmark mark='d'/> The two trimmed means, minus the controls' mean, bound the effect for the "
            "always-employed."
        ) as vo:
            intro=label('Lee bounds require random assignment and monotone selection',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lee_numbers(self):
        d = load("bounds")
        lb = d["lee"]
        A = axes([-1.5, 2.0], [0, 1], x_length=8.0, y_length=2.2, xlabel=r"effect of training on hourly wages (\$)", ylabel=r"",
                 xticks=[-1, 0, 1, 2], yticks=[], center=[-1.0, -1.0, 0])
        ax = A.ax
        seg = Line(ax.c2p(lb["lo"], 0.5), ax.c2p(lb["hi"], 0.5), color=BANDC, stroke_width=10)
        tr = Dot(ax.c2p(1.0, 0.5), radius=0.1, color=TRUEC)
        nv = Dot(ax.c2p(d["naive"], 0.5), radius=0.07, color=MISSC)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(rf"trim {100 * lb['trim']:.1f}\% of the employed trained workers", font_size=24, color=TAUC),
            label(rf"plug-in Lee bounds: \ [{lb['lo']:.2f}, \ {lb['hi']:.2f}]", font_size=24, color=BANDC),
            label(r"the truth \ (gold) \ inside; \ the naive comparison \ (red) \ inside too, \ but by luck of where it fell", font_size=24, color=GREY_A),
            label(r"add assumptions \ (covariates, \ a ranking of who works) \ to narrow them", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, 1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the example, " + say(100 * lb["trim"], 1) + " percent of the employed trained workers "
            "are marginal. <bookmark mark='b'/> Trimming gives bounds from minus " + say(-lb["lo"], 2) + " to plus "
            + say(lb["hi"], 2) + " dollars an hour. <bookmark mark='c'/> The truth, one dollar, lies inside. They are wide, because the "
            "marginal workers are a large share and could be anywhere in the distribution. <bookmark mark='d'/> Valid"
            " covariate-conditional selection restrictions can sharpen population bounds, although finite-sample "
            "estimated bounds need not always narrow, and so do further assumptions about who is marginal; each "
            "assumption buys width."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(zero))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
                if m_ == "b":
                    self.play(Create(seg))
                if m_ == "c":
                    self.play(FadeIn(tr), FadeIn(nv))
        self.clear_scene()

    def law(self):
        rows = fit_rows(VGroup(
            label(r"Manski's law of decreasing credibility:", font_size=26, color=TAUC),
            label(r"the credibility of inference decreases with the strength of the assumptions maintained", font_size=26),
            label(r"every chapter of this part: \ a stronger assumption, \ a sharper answer, \ a smaller audience", font_size=26, color=MISSC),
            label(r"bounds show where the data end and the assumptions begin", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Manski summarized the trade in what he called the law of decreasing credibility: "
            "<bookmark mark='b'/> the credibility of inference decreases with the strength of the assumptions maintained. "
            "<bookmark mark='c'/> Every design in this part made that trade: a stronger assumption, a sharper answer, and "
            "fewer people who believe it. <bookmark mark='d'/> Bounds draw the line between what the data show and what the "
            "assumptions add, and that line is worth showing even when one goes beyond it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
