from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import EST_C, PART, REAL_C, TRUE_C, era_strip, fit_right, load


class Hook(VoiceoverScene):
    def construct(self):
        m = load("michaud")
        r = load("rolling")
        self.title_card()
        self.promise(m)
        self.act(r)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Portfolio Construction")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty. Portfolio construction: how to turn estimates into weights, why the optimizer turns errors into "
            "conviction, and what to do about it."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def promise(self, m):
        pts = np.asarray(m["sims"]["60"]["pts"], float)
        med = np.median(pts, axis=0)
        left = VGroup(label(r"what the optimizer promised", font_size=24, color=EST_C),
                      MathTex(rf"{100 * med[3]:.1f}\%\ \text{{a month at}}\ {100 * med[2]:.1f}\%\ \text{{volatility}}",
                              font_size=34, color=EST_C)).arrange(DOWN, buff=0.3)
        right = VGroup(label(r"true model performance", font_size=24, color=REAL_C),
                       MathTex(rf"{100 * med[1]:.2f}\%\ \text{{a month at}}\ {100 * med[0]:.1f}\%\ \text{{volatility}}",
                               font_size=34, color=REAL_C)).arrange(DOWN, buff=0.3)
        g = VGroup(left, right).arrange(DOWN, buff=1.0).move_to(UP * 0.3)
        foot = wrapped_label(r"the median of 300 optimizers, each given five years of returns simulated from the 49 US "
                             r"industries' own means and covariance (Chapter 1)", 11.0, 17, GREY_A).to_edge(DOWN, buff=0.6)
        ratio = med[0] / med[2]
        with self.voiceover(
            f"""In a controlled simulation, declare the forty-nine industries' research-period moments to be the population truth. Give each optimizer sixty independent Gaussian observations and target one percent monthly excess return. <bookmark mark='a'/> Across {m['reps']} draws, median reported volatility is {100 * med[2]:.1f} percent a month. <bookmark mark='b'/> Evaluate those same weights under the stipulated moments: median expected excess return is {100 * med[1]:.2f} percent at {100 * med[0]:.1f} percent volatility, about {ratio:.0f} times the reported risk. These are componentwise medians, not one portfolio, and population-model evaluations rather than historical deliveries."""
        ) as vo:
            self.play(FadeIn(foot), FadeIn(left, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(left, color=EST_C, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self, r):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. This part opens the fifth act: portfolios, strategies and the firm. The fourth act asked "
            "which signals are real; this one asks how to hold them. Part twenty-nine ended on a theorem about estimated "
            "means; this part is about estimated covariances, and about the rules that try to need neither."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1952, r"Markowitz", I), (1956, r"Kelly", I), (1967, r"Marchenko--Pastur", I), (1972, r"Merton's frontier", I),
                   (1989, r"Michaud: error maximisation", I), (1991, r"Cover; Black--Litterman", I),
                   (1999, r"RMT cleaning", I), (2000, r"CVaR as an LP", I), (2003, r"constraints as shrinkage", I),
                   (2004, r"Ledoit--Wolf", I), (2009, r"1/N", I), (2016, r"HRP", I), (2020, r"nonlinear shrinkage", I)]
        strip = era_strip(entries, y0=1948, y1=2026, font_size=12).move_to(DOWN * 0.3)
        head = label(r"Seventy years of optimizing with estimates", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 8), (8, 13)]
        with self.voiceover(
            "Harry Markowitz posed the problem in 1952; John Kelly asked the long-run question in 1956; the mathematics of "
            "random matrices arrived in 1967, and Robert Merton drew the frontier in closed form in 1972. "
            "<bookmark mark='a'/> Then the reckoning: Richard Michaud's error maximisation, Cover's universal portfolio, "
            "Black and Litterman's market prior, and physicists cleaning correlation matrices. <bookmark mark='b'/> And "
            "the modern answers: risk as a linear program, constraints understood as shrinkage, Ledoit and Wolf's "
            "estimators, the humbling contest against one over N, hierarchical risk parity, and nonlinear shrinkage."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk in zip(groups, [None, "a", "b"]):
                if mk:
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Error maximisation, and the contest against 1/N",
            r"Covariance in high dimension: Marchenko--Pastur and cleaning",
            r"Shrinkage: Ledoit and Wolf, linear and nonlinear; constraints as shrinkage",
            r"Black--Litterman; risk parity and HRP; robust optimisation and CVaR",
            r"Kelly, Cover's universal portfolio, Fernholz's diversity weights; entropy pooling",
            r"End-to-end portfolios; evaluation protocol and fixed arithmetic",
            r"For the researcher: why the optimizer underestimates its own risk, exactly",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: why optimizers maximise errors, and how one over N embarrasses them; what random matrix theory says "
            "about a covariance matrix; shrinkage, and why constraints are shrinkage in disguise; Black-Litterman, risk "
            "parity and its hierarchical cousin; robust optimisation and tail risk; growth, from Kelly to Cover and "
            "Fernholz; views on whole distributions; a network that learns weights directly; evaluation protocol and fixed arithmetic, with sealed strategy results excluded; and the optimizer's risk illusion under a stated model."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("portfolio",))
        with self.voiceover(
            "In the House, the portfolio desk gets its optimizer: estimators that know their own noise, allocation rules "
            "that need fewer estimates, and a rule for what any optimized portfolio must report about itself."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
