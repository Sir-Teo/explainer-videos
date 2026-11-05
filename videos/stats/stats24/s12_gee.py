from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats24.common import *  # noqa: F403


class GEE(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.equations()
        self.results()
        self.marginal()
        self.working()
        self.board()

    def card(self):
        card = chapter_card(11, r"GEE", r"Clustered outcomes, \ honest standard errors", lit=(1986,), part=PART)
        with self.voiceover("Chapter eleven. Generalized estimating equations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        d = load("gee")
        rows = [
            cmath(r"y_{gi}", r"=", r"[\text{score} > 550], \ \ \text{pupil } i \text{ in school } g", font_size=30),
            cmath(r"\text{logit } P(y = 1)", r"=", r"\beta_0 + \beta_1 \text{programme} + \beta_2 \text{SES}", font_size=30),
            cmath(r"\text{iid SE of } \hat\beta_1", r"=", rf"{d['naive']['se'][1]:.3f}", font_size=30),
            cmath(r"\text{but}", r":", r"\text{pupils in a school share teachers, \ intake, \ the programme}", font_size=28),
        ]
        rows[2][2].set_color(RES)
        whys = [why(rf"{d['n']:,} pupils in 40 of the World's schools; \ {100 * d['mean_y']:.0f}\% pass"), why(r"Part 23's programme, \ now yes-or-no"),
                why(r"as if every pupil were independent"), why(r"Part 23, \ chapter five: \ clusters")]
        with self.voiceover(
            "<bookmark mark='a'/> Part 23's schools again, with a yes-or-no outcome: did the pupil score above five hundred "
            "and fifty? Thirty-two percent did, in a sample of forty schools. <bookmark mark='b'/> A logistic regression on "
            "the tutoring programme and home background. <bookmark mark='c'/> Fitted as if every pupil were independent, the "
            "programme's coefficient has a standard error of point oh nine four. <bookmark mark='d'/> But pupils in the "
            "same school share teachers, intake, and the programme itself, so as Part 23 showed for least squares, that "
            "standard error is too small."
        ) as vo:
            self.add(simulated_tag())
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def equations(self):
        rows = [
            cmath(r"\textstyle\sum_g D_g^\top V_g^{-1} (y_g - \mu_g)", r"=", r"0", font_size=30),
            cmath(r"V_g", r"=", r"A_g^{1/2} R(\alpha) A_g^{1/2}, \ \ A_g = \mathrm{diag}\{\mu(1 - \mu)\}", font_size=30),
            cmath(r"R(\alpha)", r":", r"\text{independence, \ exchangeable, \ AR(1), \ unstructured}", font_size=28),
            cmath(r"\mathrm{Cov}\,\hat\beta", r"=", r"B^{-1}\Big(\textstyle\sum_g D_g^\top V_g^{-1} r_g r_g^\top V_g^{-1} D_g\Big) B^{-1}", font_size=28),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"Liang \& Zeger (1986): \ a GLM score, \ cluster by cluster"), why(r"a working covariance"),
                why(r"a guess at the within-cluster correlation"), why(r"the sandwich: \ right even if $R$ is wrong")]
        with self.voiceover(
            "<bookmark mark='a'/> Kung-Yee Liang and Scott Zeger's generalized estimating equations, from 1986, write a GLM "
            "score cluster by cluster: derivatives of the mean, times an inverse covariance, times the residuals. "
            "<bookmark mark='b'/> The covariance is a working guess: the binomial variances combined with <bookmark mark='c'/> "
            "a working correlation within each cluster, independence, exchangeable, autoregressive or unstructured. "
            "<bookmark mark='d'/> The standard errors come from a sandwich that sums each cluster's residual products, Part "
            "23's cluster-robust idea. The estimates are consistent and the sandwich honest even when the working "
            "correlation is wrong; a good guess only buys efficiency."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def results(self):
        d = load("gee")
        hdr = [r"\textbf{fit}", r"$\hat\beta_1$", r"\textbf{model SE}", r"\textbf{robust SE}"]
        body = [[r"logistic, \ iid", f"{d['naive']['coef'][1]:.3f}", f"{d['naive']['se'][1]:.3f}", r"---"],
                [r"GEE, \ independence", f"{d['ind']['coef'][1]:.3f}", f"{d['ind']['se_model'][1]:.3f}", f"{d['ind']['se_robust'][1]:.3f}"],
                [rf"GEE, \ exchangeable ($\hat\alpha = {d['ex']['alpha']:.3f}$)", f"{d['ex']['coef'][1]:.3f}", f"{d['ex']['se_model'][1]:.3f}",
                 f"{d['ex']['se_robust'][1]:.3f}"]]
        t = table_rows([hdr] + body, font_size=26, col_buff=0.7, row_buff=0.32, colors=[GREY_A, RES, BLUE, HIT])
        t.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"the World's marginal coefficient: \ {d['truth']:.3f}", font_size=22, color=TRUE),
            label(r"independence GEE: \ the same estimate as logistic, \ an honest SE", font_size=22),
            label(r"the robust SE is 2.4 times the naive", font_size=22, color=RES),
        ), 12.0, 0.25, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three fits. <bookmark mark='b'/> GEE with an independence working correlation reproduces "
            "the logistic estimate exactly, point four five three, but its robust standard error is point two two eight, "
            "two point four times the naive one. <bookmark mark='c'/> With an exchangeable correlation, estimated at point "
            "oh nine between pupils of one school, the estimate moves to point four oh five and the model-based and robust "
            "errors agree, a sign the working correlation is about right. <bookmark mark='d'/> The target is the "
            "World's own marginal coefficient, point three nine two, computed from every pupil."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(t[0]), FadeIn(t[1]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(t[2]), FadeIn(foot[1]), FadeIn(foot[2]))
            vo.wait_until("c")
            self.play(FadeIn(t[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
        self.clear_scene()

    def marginal(self):
        rows = [
            cmath(r"\text{marginal}", r":", r"\text{logit } P(y = 1 \mid x) = x^\top\beta^{M}", font_size=30),
            cmath(r"\text{conditional}", r":", r"\text{logit } P(y = 1 \mid x, u_g) = x^\top\beta^{C} + u_g", font_size=30),
            cmath(r"\beta^{M}", r"\approx", r"\beta^{C} / \sqrt{1 + 0.346\,\sigma_u^2}", font_size=30),
            cmath(r"\text{which?}", r":", r"\text{policy for a population, \ or the effect for one school}", font_size=28),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"population-averaged: \ GEE"), why(r"school-specific: \ Part 25's mixed models"),
                why(r"Zeger, \ Liang \& Albert (1988): \ marginal is smaller"), why(r"different questions, \ both legitimate")]
        with self.voiceover(
            "<bookmark mark='a'/> GEE estimates a marginal, population-averaged effect: how the pass rate changes across "
            "all pupils when schools adopt the programme. <bookmark mark='b'/> A mixed model, Part 25, estimates a "
            "conditional effect: the change within one school, holding its own effect fixed. <bookmark mark='c'/> For a "
            "logistic link they differ: averaging over school effects flattens the curve, so the marginal coefficient is "
            "smaller, roughly the conditional one divided by the square root of one plus point three four six times the "
            "school-effect variance, as Scott Zeger, Kung-Yee Liang and Paul Albert showed. <bookmark mark='d'/> Neither is "
            "wrong. A minister choosing a policy wants the first; a head teacher wants the second. For a linear model, and "
            "only there, they coincide."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def working(self):
        rows = [
            cmath(r"\text{right } R", r":", r"\text{efficient; \ model and robust SEs agree}", font_size=30),
            cmath(r"\text{wrong } R", r":", r"\text{still consistent; \ robust SE still honest}", font_size=30),
            cmath(r"\text{few clusters}", r":", r"\text{the sandwich is biased down: \ Mancl \& DeRouen (2001)}", font_size=28),
            cmath(r"\text{time-varying } x", r":", r"\text{non-independence } R \text{ needs care: \ Pepe \& Anderson (1994)}", font_size=28),
        ]
        rows[1][-1].set_color(HIT)
        whys = [why(r"like GLS: \ Part 23, \ chapter three"), why(r"the whole point of GEE"),
                why(r"Part 23's few-cluster problem, \ again"), why(r"when past covariates matter")]
        with self.voiceover(
            "<bookmark mark='a'/> How much does the working correlation matter? If it's right, GEE is efficient, like "
            "generalized least squares, and the model-based and robust standard errors agree, as they did here. "
            "<bookmark mark='b'/> If it's wrong, the estimates are still consistent and the robust standard errors still "
            "honest; only efficiency is lost. <bookmark mark='c'/> With few clusters the sandwich is biased downwards, the "
            "few-cluster problem of Part 23; Lloyd Mancl and Timothy DeRouen's correction helps. <bookmark mark='d'/> And "
            "with covariates that change over time, a non-independence working correlation can bias the estimates unless "
            "the model conditions on everything that matters, as Margaret Pepe and Garnet Anderson showed."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=24) if r.part == 24][3:6]
        b = coverage_board(rows, lit_part=24, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> The Board: five hundred samples of forty schools, against the World's marginal "
            "coefficient. Logistic regression with the iid standard error: fifty-five percent, broken. "
            "<bookmark mark='b'/> GEE with independence and the robust standard error: ninety-five, kept. "
            "<bookmark mark='c'/> GEE with an exchangeable working correlation: ninety-five, kept."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()
