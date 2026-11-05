from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats24.common import *  # noqa: F403


class Quasi(VoiceoverScene):
    def construct(self):
        self.card()
        self.overdispersion()
        self.quasi()
        self.estimates()
        self.shape()
        self.binomial_od()
        self.board()

    def card(self):
        card = chapter_card(7, r"Quasi-likelihood", r"Only a mean and a variance", lit=(1974,), part=PART)
        with self.voiceover("Chapter seven. Quasi-likelihood and overdispersion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def overdispersion(self):
        d = load("visits")
        rows = [
            cmath(r"\text{Poisson}", r":", r"\mathrm{Var}\,y = \mu", font_size=30),
            cmath(r"\text{the visits}", r":", rf"\bar y = {d['mean']:.2f}, \ s^2 = {d['var']:.2f}", font_size=30),
            cmath(r"\text{causes}", r":", r"\text{people differ beyond the covariates; \ contagion; \ clustering}", font_size=28),
            cmath(r"\text{consequence}", r":", r"\text{estimates fine, \ SEs too small}", font_size=30),
        ]
        rows[1][2].set_color(RES)
        whys = [why(r"one parameter fixes both"), why(r"five times the mean"),
                why(r"unobserved heterogeneity"), why(r"Part 22's sandwich chapter")]
        with self.voiceover(
            "<bookmark mark='a'/> A Poisson model ties the variance to the mean. <bookmark mark='b'/> The World's doctor "
            "visits have a mean of two point one three and a variance of ten point three, five times as big. "
            "<bookmark mark='c'/> Counts are usually overdispersed like this: people differ in ways the covariates don't "
            "capture, one event makes another likelier, events cluster. <bookmark mark='d'/> As Part 22 found, the Poisson "
            "estimates of the mean structure stay sensible, but its standard errors are too small."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def quasi(self):
        rows = [
            cmath(r"\text{assume only}", r":", r"E\,y = \mu(\beta), \ \ \mathrm{Var}\,y = \phi V(\mu)", font_size=30),
            cmath(r"Q(\mu; y)", r"=", r"\textstyle\int_y^\mu \dfrac{y - t}{\phi V(t)}\, dt", font_size=30),
            cmath(r"\text{maximizing } Q", r"=", r"\text{the GLM score equations}", font_size=30),
            cmath(r"\mathrm{Cov}\,\hat\beta", r"=", r"\hat\phi\,(X^\top W X)^{-1}", font_size=30),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"Wedderburn (1974)"), why(r"the quasi-likelihood: \ behaves like a log likelihood"),
                why(r"the same IRLS, \ the same $\hat\beta$"), why(r"SEs scaled by $\sqrt{\hat\phi}$")]
        with self.voiceover(
            "<bookmark mark='a'/> Robert Wedderburn's 1974 quasi-likelihood, which Part 22 met briefly, assumes only a mean "
            "model and a variance that is phi times a known function of the mean. <bookmark mark='b'/> The integral of the "
            "standardized residual behaves just like a log likelihood: its derivative has mean zero, and its variance equals "
            "minus its expected curvature. <bookmark mark='c'/> Maximizing it gives exactly the GLM score equations, so the "
            "same IRLS, the same estimates. <bookmark mark='d'/> Only the covariance changes: multiply by the estimated "
            "dispersion."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def estimates(self):
        d = load("visits")
        p, nb = d["poisson"], d["nb"]
        names = d["names"]
        hdr = [r"", r"\textbf{Poisson} $\hat\beta$", r"\textbf{SE model}", r"\textbf{quasi}", r"\textbf{sandwich}", r"\textbf{NB} $\hat\beta$", r"\textbf{NB SE}"]
        body = []
        q = np.sqrt(p["phi"])
        for j in range(1, 5):
            body.append([names[j], f"{p['coef'][j]:.3f}", f"{p['se'][j]:.3f}", f"{q * p['se'][j]:.3f}", f"{p['se_sand'][j]:.3f}",
                         f"{nb['coef'][j]:.3f}", f"{nb['se'][j]:.3f}"])
        t = table_rows([hdr] + body, font_size=22, col_buff=0.45, row_buff=0.3, colors=[GREY_A, None, None, None, None])
        t.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"$\hat\phi = {p['phi']:.2f}$: \ quasi SEs $= \sqrt{{\hat\phi}} = {q:.2f}$ times the Poisson's", font_size=22, color=PATH),
            label(r"the estimates barely move; \ the SEs nearly double", font_size=22, color=RES),
        ), 12.0, 0.25, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The doctor visits, four covariates. <bookmark mark='b'/> The Poisson model's standard "
            "errors, <bookmark mark='c'/> then quasi-Poisson's, all multiplied by the square root of three point three six, one "
            "point eight three. <bookmark mark='d'/> The sandwich's are similar but not uniformly scaled: the diagnosis of "
            "high blood pressure gets the biggest increase. <bookmark mark='e'/> A negative binomial model, chapter eight, "
            "gives almost the same coefficients with standard errors close to the sandwich's."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(t[0]), *[FadeIn(VGroup(*r[:2])) for r in t[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(r[2]) for r in t[1:]])
            vo.wait_until("c")
            self.play(*[FadeIn(r[3]) for r in t[1:]], FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(*[FadeIn(r[4]) for r in t[1:]])
            vo.wait_until("e")
            self.play(*[FadeIn(VGroup(*r[5:])) for r in t[1:]], FadeIn(foot[1]))
        self.clear_scene()

    def shape(self):
        rows = [
            cmath(r"\text{quasi-Poisson}", r":", r"\mathrm{Var} = \phi\mu", font_size=30),
            cmath(r"\text{negative binomial}", r":", r"\mathrm{Var} = \mu + \mu^2/k", font_size=30),
            cmath(r"\text{the difference}", r":", r"\text{weights: \ } \mu \ \text{vs} \ \mu/(1 + \mu/k)", font_size=30),
            cmath(r"\text{sandwich}", r":", r"\text{no variance model at all}", font_size=30),
        ]
        rows[1][2].set_color(NBC)
        whys = [why(r"a constant multiple"), why(r"grows faster: \ heterogeneity"),
                why(r"Ver Hoef \& Boveng (2007)"), why(r"honest for any shape, \ if $n$ is large")]
        with self.voiceover(
            "<bookmark mark='a'/> But quasi-Poisson makes an assumption of its own: the variance is a constant multiple of "
            "the mean. <bookmark mark='b'/> Heterogeneity between people produces something else, the negative binomial's "
            "mu plus mu squared over k, which grows faster for large means. <bookmark mark='c'/> The two weight the "
            "observations differently, the quasi-Poisson giving big counts more weight, as Jay Ver Hoef and Peter Boveng "
            "pointed out. <bookmark mark='d'/> The sandwich assumes no variance shape at all."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def binomial_od(self):
        rows = [
            cmath(r"\text{beta-binomial}", r":", r"p_i \sim \text{Beta}: \ \mathrm{Var} = np(1 - p)\{1 + (n - 1)\rho\}", font_size=28),
            cmath(r"\text{beetles, logit}", r":", rf"\hat\phi = {load('extras')['bliss_phi']['logit']:.2f}", font_size=30),
            cmath(r"\text{beetles, cloglog}", r":", rf"\hat\phi = {load('extras')['bliss_phi']['cloglog']:.2f}", font_size=30),
            cmath(r"\text{lesson}", r":", r"\text{a wrong mean looks like overdispersion}", font_size=30),
        ]
        rows[3][-1].set_color(RES)
        whys = [why(r"litters, \ batches, \ classrooms: \ Williams (1982)"), why(r"apparently overdispersed"), why(r"not at all"), why(r"fix the mean before the variance")]
        with self.voiceover(
            "<bookmark mark='a'/> Proportions can be overdispersed too. If each batch of beetles had its own death rate, "
            "drawn from a beta distribution, counts would follow a beta-binomial, with the binomial variance inflated by one "
            "plus n minus one times an intraclass correlation. <bookmark mark='b'/> Bliss's beetles under the logit link "
            "give a Pearson dispersion of one point six seven, apparently overdispersed. <bookmark mark='c'/> Under the "
            "complementary log-log it's point five five. <bookmark mark='d'/> The extra variation was the wrong curve, "
            "not extra noise. A misspecified mean shows up as overdispersion, so fix the mean before reaching for the "
            "variance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=24) if r.part == 24][:3]
        b = coverage_board(rows, lit_part=24, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> The Board: a thousand samples of five hundred adults, and the coefficient on a diagnosis of "
            "high blood pressure. The target is the World's own Poisson fit, the projection of Part 22. Poisson standard "
            "errors cover it sixty-four percent of the time: broken. <bookmark mark='b'/> Quasi-Poisson: ninety, closer but "
            "still broken, because a constant multiple is the wrong shape for these data. <bookmark mark='c'/> The sandwich: "
            "ninety-four, kept."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()
