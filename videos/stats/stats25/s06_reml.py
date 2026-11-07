from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


class REML(VoiceoverScene):
    def construct(self):
        self.card()
        self.bias()
        self.reml()
        self.simulation()
        self.compare()

    def card(self):
        card = chapter_card(5, r"ML vs REML", r"Neyman--Scott, \ cured", lit=(1971,), part=PART)
        with self.voiceover("Chapter five. Maximum likelihood versus REML."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bias(self):
        rows = [
            cmath(r"\text{one sample}", r":", r"\hat\sigma^2_{ML} = \tfrac1n \textstyle\sum (y_i - \bar y)^2, \ \ E = \tfrac{n - 1}{n}\sigma^2", font_size=28),
            cmath(r"\text{regression}", r":", r"E\,\hat\sigma^2_{ML} = \tfrac{n - p}{n}\sigma^2", font_size=30),
            cmath(r"\text{mixed model}", r":", r"\text{profiling does not correct for fitted fixed effects}", font_size=28),
            cmath(r"\text{few groups}", r":", r"\text{the bias is large}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"the mean was estimated, \ not known"), why(r"$p$ degrees of freedom used"),
                why(r"Part 22's Neyman--Scott, \ in miniature"), why(r"the variance is learned from the groups")]
        intro = label('Fitting the mean can bias maximum-likelihood variance estimates', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Maximum likelihood can substantially underestimate variance after fitting a mean. "
            "For one sample, dividing by n instead of n minus one underestimates by a factor of n minus one over n, "
            "because the mean was estimated. <bookmark mark='b'/> In regression the factor is n minus p over n. "
            "<bookmark mark='c'/> In a mixed model, the maximum likelihood estimate of the group variance makes the "
            "same mistake: it profiles over the fixed effects without a degrees-of-freedom correction. This resembles"
            " the nuisance-parameter problem, though a fixed number of coefficients is not the growing-parameter "
            "Neyman–Scott setting. <bookmark mark='d'/> Since the group variance is learned from the groups, the bias"
            " can be large with few groups; boundaries can also bias REML."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def reml(self):
        rows = [
            cmath(r"K^\top y", r",", r"\ K^\top X=0,\ \mathrm{rank}(K)=n-p:\ \text{error contrasts}", font_size=30),
            cmath(r"K^\top y", r"\sim", r"N(0, K^\top V K): \ \text{free of } \beta", font_size=30),
            cmath(r"\ell_R", r"=", r"\ell(\hat\beta) - \tfrac12 \log\det(X^\top V^{-1} X)", font_size=30),
            cmath(r"\text{one sample}", r":", r"\ell_R \text{ gives } \tfrac{1}{n - 1}\textstyle\sum (y_i - \bar y)^2", font_size=30),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"combinations of $y$ that cancel the fixed effects"), why(r"Part 22's marginal likelihood idea"),
                why(r"Patterson \& Thompson (1971)"), why(r"the usual unbiased variance")]
        intro = label('Error contrasts remove the fixed-effect mean from the likelihood', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The cure is Part 22's: remove the nuisance parameters first. Take combinations of the data "
            "that cancel the fixed effects, error contrasts. <bookmark mark='b'/> Their distribution depends only on the "
            "variances. <bookmark mark='c'/> Its log likelihood, restricted maximum likelihood, is the ordinary log likelihood "
            "at the GLS estimate minus half the log determinant of X transpose V inverse X, as Desmond Patterson and Robin "
            "Thompson showed in 1971. <bookmark mark='d'/> For one sample it gives exactly the n minus one divisor."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def simulation(self):
        d = load("remlml")
        b = d["by_G"]
        Gs = ["5", "10", "40"]
        A = axes([0.5, 3.5], [0, 0.35], x_length=7.0, y_length=4.4, xlabel=r"number of groups, \ 10 per group",
                 ylabel=r"average estimate of $\tau^2$", xticks=[], yticks=[0, 0.1, 0.2, 0.3], center=[-2.0, 0.3, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(0.5, d["truth"]), ax.c2p(3.5, d["truth"]), color=TRUE, stroke_width=2.5)
        bars = VGroup()
        names = VGroup()
        for k, G_ in enumerate(Gs):
            x = k + 1
            for dx, key, col in ((-0.17, "ml", RES), (0.17, "reml", SHRUNK)):
                h = ax.c2p(0, b[G_][key])[1] - ax.c2p(0, 0)[1]
                bars.add(Rectangle(width=0.3, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(ax.c2p(x + dx, 0), aligned_edge=DOWN))
            names.add(label(G_, font_size=22, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.15))
        rows = fit_rows(VGroup(
            label(rf"gold: \ the truth, \ {d['truth']:.3f}", font_size=22, color=TRUE),
            label(rf"red: \ ML: \ {b['5']['ml']:.3f} with 5 groups", font_size=22, color=RES),
            label(rf"green: \ REML: \ {b['5']['reml']:.3f}", font_size=22, color=SHRUNK),
            label(rf"ML gives $\hat\tau^2 < 10^{-6}$ in {100 * b['5']['ml_zero']:.0f}\% of samples", font_size=22, color=RES),
            label(r"with 40 groups, \ they agree", font_size=22, color=GREY_A),
        ), 4.2, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three hundred seeded data sets at each group count compare ML and REML. This "
            "illustration uses a normal-plus-Bernoulli random-intercept mixture with the variance marked in gold, so "
            "the Gaussian likelihood is a working model. <bookmark mark='b'/> With five groups, ML averages about "
            "point one four three. <bookmark mark='c'/> REML averages point two eight nine, closer to the true point "
            "two seven two five in this experiment. REML is not exactly unbiased for every component, especially at a"
            " boundary. <bookmark mark='d'/> ML is numerically near zero in about twenty-eight percent of samples. "
            "<bookmark mark='e'/> With forty groups the averages nearly agree. Compare different fixed-effect "
            "specifications using ML, since their restricted likelihoods use different contrasts."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names), Create(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in bars[2:]], lag_ratio=0.2), FadeIn(rows[4]))
        self.clear_scene()

    def compare(self):
        rows = [
            cmath(r"\text{REML}", r":", r"\text{variance components; \ the default}", font_size=30),
            cmath(r"\text{ML}", r":", r"\text{LR tests of fixed effects; \ AIC across fixed parts}", font_size=30),
            cmath(r"\text{both}", r":", r"\text{the same } \hat\beta \text{ given the variances}", font_size=30),
            cmath(r"\text{Bayes}", r":", r"\text{integrate the fixed effects out, \ as REML does}", font_size=30),
        ]
        rows[0][2].set_color(SHRUNK)
        whys = [why(r"lme4's default"), why(r"REML likelihoods differ in their contrasts"), why(r"GLS either way"),
                why(r"REML is a flat-prior marginal likelihood: \ Part 26")]
        intro = label('Restricted likelihood comparisons require the same fixed-effect space', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> So: REML for variance components, the default in most software. <bookmark "
            "mark='b'/> Maximum likelihood when comparing models with different fixed effects, by likelihood ratio or"
            " AIC, because restricted likelihoods with different fixed effects are built from different contrasts. "
            "<bookmark mark='c'/> Given the variances, both give the same GLS estimates. <bookmark mark='d'/> And "
            "REML has a Bayesian reading: it is proportional, for fixed X and a fixed normalization, to integrating "
            "beta against a flat prior. Its arbitrary improper-prior constant prevents comparing different "
            "fixed-effect spaces."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
