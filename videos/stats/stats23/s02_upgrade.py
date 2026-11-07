from __future__ import annotations

from videos.stats.stats23.common import *  # noqa: F403


class Upgrade(VoiceoverScene):
    def construct(self):
        self.card()
        self.upgrade()
        self.assumptions()
        self.gauss_markov()
        self.map_()

    def card(self):
        card = chapter_card(1, r"Upgrade: \ what Part 12 assumed", r"Least squares without the fine print", part=PART)
        with self.voiceover("Chapter one. An upgrade of Part 12."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def upgrade(self):
        u = upgrade_card(12, r"$\hat\beta = (X^\top X)^{-1}X^\top y$ is BLUE, \ with $\mathrm{Var}\,\hat\beta = \sigma^2 (X^\top X)^{-1}$",
                         r"a true linear mean, \ equal and independent errors, \ exactly measured $X$, \ exact arithmetic",
                         r"each assumption dropped in turn, \ and the estimator and its SE repaired",
                         width=11.0, font_size=24).move_to([0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 12 derived least squares and proved the Gauss–Markov theorem: the least squares "
            "estimator is the best linear unbiased estimator, with variance sigma squared times X transpose X inverse. "
            "<bookmark mark='b'/> It assumed a lot: that the mean really is linear in the predictors, that the errors have "
            "equal variances and are independent, that the predictors are measured exactly, and, as Longley just showed, "
            "that the arithmetic is exact. <bookmark mark='c'/> This part drops each assumption in turn and repairs what "
            "breaks."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(u[0]), FadeIn(u[1][0]), FadeIn(u[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(u[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(u[1][1][2]))
        self.wait(1.0)
        self.clear_scene()

    def assumptions(self):
        rows = [
            cmath(r"y", r"=", r"X\beta + \varepsilon, \ \ E(\varepsilon \mid X) = 0", font_size=30),
            cmath(r"\mathrm{Var}(\varepsilon \mid X)", r"=", r"\sigma^2 I", font_size=30),
            cmath(r"\hat\beta - \beta", r"=", r"(X^\top X)^{-1} X^\top \varepsilon", font_size=30),
            cmath(r"\mathrm{Var}(\hat\beta \mid X)", r"=", r"(X^\top X)^{-1} X^\top \,\mathrm{Var}(\varepsilon \mid X)\, X (X^\top X)^{-1}", font_size=28),
        ]
        rows[3][2].set_color(OLS_C)
        whys = [why(r"the mean is linear: \ chapter six relaxes it"), why(r"equal, \ uncorrelated: \ chapters three to five"),
                why(r"the error the estimator inherits"), why(r"the sandwich, \ before any assumption on the middle")]
        intro = label('A full-rank linear mean and its error covariance determine OLS uncertainty', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Write the model as y equals X beta plus an error whose mean, given X, is zero. "
            "<bookmark mark='b'/> Part 12 added that the errors are uncorrelated with a common variance. "
            "<bookmark mark='c'/> The estimator's error is X transpose X inverse, X transpose, times the errors: it is "
            "linear in them. <bookmark mark='d'/> So its variance is a sandwich, with whatever the variance of the errors is "
            "in the middle. Every chapter of this part is about what goes in that middle, and what to do when we don't know."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gauss_markov(self):
        rows = [
            cmath(r"\tilde\beta", r"=", r"Ay, \ \ AX = I \ \ \text{(linear, unbiased)}", font_size=30),
            cmath(r"A", r"=", r"(X^\top X)^{-1}X^\top + D, \ \ DX = 0", font_size=30),
            cmath(r"\mathrm{Var}\,\tilde\beta", r"=", r"\sigma^2 (X^\top X)^{-1} + \sigma^2 DD^\top", font_size=30),
            cmath(r"\text{needs}", r":", r"\mathrm{Var}\,\varepsilon = \sigma^2 I", font_size=30),
        ]
        rows[2][2].set_color(OLS_C)
        whys = [why(r"any competitor"), why(r"write it as OLS plus a difference"),
                why(r"the cross terms vanish because $DX = 0$"), why(r"drop it and OLS can lose: \ chapter three")]
        intro = label('Gauss--Markov compares linear unbiased estimators under equal variances', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "A reminder of exactly where the assumptions enter. <bookmark mark='a'/> Take any other linear unbiased "
            "estimator, A y, with A X equal to the identity. <bookmark mark='b'/> Write A as least squares' matrix plus a "
            "difference D; unbiasedness forces D X to be zero. <bookmark mark='c'/> Its variance is least squares' variance "
            "plus sigma squared D D transpose, which can only add: the cross terms vanish because D X is zero. "
            "<bookmark mark='d'/> But that algebra used the error variance being sigma squared times the identity. Change "
            "the middle, and least squares need no longer win, which is where chapter three begins."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def map_(self):
        rows = fit_rows(VGroup(
            label(r"$\sigma^2 \Omega$, \ known shape: \ GLS, \ chapter three", font_size=24, color=GLS_C),
            label(r"$\mathrm{diag}(\sigma_i^2)$, \ unknown: \ HC standard errors, \ chapter four", font_size=24, color=OLS_C),
            label(r"blocks, \ one per cluster: \ cluster-robust SEs, \ chapter five", font_size=24, color=CLUSTER),
            label(r"a mean that is not linear: \ the best linear predictor, \ chapter six", font_size=24, color=TEAL),
            label(r"an $X$ measured with error: \ attenuation, \ chapter seven", font_size=24, color=NOISY),
            label(r"and the arithmetic: \ chapter ten", font_size=24, color=GREY_A),
        ), 12.4, 0.45, [0, 0, 0])
        intro = label('Different model departures require different repairs', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "The map. <bookmark mark='a'/> If the errors' covariance has a known shape, generalized least squares "
            "uses it. <bookmark mark='b'/> If each error has its own unknown variance, heteroskedasticity-consistent "
            "standard errors estimate the middle from the residuals. <bookmark mark='c'/> If errors are correlated "
            "within clusters, sum within clusters first. <bookmark mark='d'/> With finite second moments and a "
            "nonsingular predictor moment matrix, least squares can estimate the best linear predictor even when the "
            "mean is curved. <bookmark mark='e'/> Classical independent error in a single regressor attenuates its "
            "slope; with several regressors the direction of bias can vary. <bookmark mark='f'/> And the arithmetic "
            "needs care too."
        ) as vo:
            self.add(intro)
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
