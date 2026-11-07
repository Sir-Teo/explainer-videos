from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


class LMM(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.henderson()
        self.blup_formula()
        self.fit()
        self.picture()
        self.predict()

    def card(self):
        card = chapter_card(4, r"The linear mixed model", r"GLS, \ and predictions for each group", lit=(1982,), part=PART)
        with self.voiceover("Chapter four. The linear mixed model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"y", r"=", r"X\beta + Zb + \varepsilon", font_size=32),
            cmath(r"b \sim N(0, G)", r",", r"\ \varepsilon \sim N(0, R)", font_size=30),
            cmath(r"\mathrm{Var}\,y", r"=", r"V = ZGZ^\top + R", font_size=30),
            cmath(r"\hat\beta", r"=", r"(X^\top V^{-1} X)^{-1} X^\top V^{-1} y", font_size=30),
        ]
        rows[3][2].set_color(MODEL)
        whys = [why(r"fixed effects $\beta$, \ random effects $b$"), why(r"Laird \& Ware (1982)"),
                why(r"the random effects shape the covariance"), why(r"Part 23's GLS, \ with $V$ estimated")]
        intro = label('A working probability model states the assumptions behind shrinkage', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> In general a linear mixed model has fixed effects beta, with design X, and random "
            "effects b, with design Z. <bookmark mark='b'/> The random effects are normal with covariance G, and the "
            "errors normal with covariance R, independent of b, usually sigma squared times the identity: Nan Laird "
            "and James Ware's formulation of 1982. <bookmark mark='c'/> Averaging the random effects away, the data "
            "have covariance V, Z G Z transpose plus R. <bookmark mark='d'/> So the fixed effects are estimated by "
            "Part 23's generalized least squares with that V, once G and R have been estimated."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def henderson(self):
        rows = [
            cmath(r"\begin{pmatrix} X^\top R^{-1}X & X^\top R^{-1}Z \\ Z^\top R^{-1}X & Z^\top R^{-1}Z + G^{-1}\end{pmatrix}"
                  r"\begin{pmatrix}\hat\beta \\ \hat b\end{pmatrix}", r"=", r"\begin{pmatrix} X^\top R^{-1}y \\ Z^\top R^{-1}y\end{pmatrix}", font_size=26),
            cmath(r"\text{maximize}", r":", r"\log f(y \mid b)+\log f(b)\quad(\beta,b;\ G,R \text{ fixed})", font_size=30),
            cmath(r"G^{-1}", r":", r"\text{a ridge penalty on } b", font_size=30),
            cmath(r"\hat b", r"=", r"G Z^\top V^{-1}(y - X\hat\beta): \ \text{the BLUP}", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"Henderson's mixed-model equations (1950)"), why(r"a penalized least squares"),
                why(r"Part 19's ridge, \ with $\lambda$ from the data"), why(r"best linear unbiased prediction")]
        intro = label('Henderson solves for fixed effects and predictions at fixed covariance', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Charles Henderson, a dairy geneticist ranking bulls by their daughters' milk "
            "yields, found a neater route in 1950: the mixed-model equations. <bookmark mark='b'/> They come from "
            "maximizing the joint density over beta and b, holding G and R fixed. Estimate covariance parameters "
            "separately by marginal likelihood or REML, <bookmark mark='c'/> which is least squares with a ridge "
            "penalty G inverse on the random effects, Part 19's ridge with the penalty estimated from the data. "
            "<bookmark mark='d'/> Their solution gives the GLS estimate of beta and, for each group, the best linear "
            "unbiased predictor of its random effect, the BLUP."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def blup_formula(self):
        rows = [
            cmath(r"\text{random intercept}", r":", r"\hat u_g = \lambda_g\, (\bar y_g - \bar x_g^\top\hat\beta)", font_size=30),
            cmath(r"\lambda_g", r"=", r"\dfrac{\tau^2}{\tau^2 + \sigma^2/n_g}", font_size=32),
            cmath(r"\text{small } n_g", r":", r"\lambda_g \to 0: \ \text{back to the average school}", font_size=30),
            cmath(r"\text{large } n_g", r":", r"\lambda_g \to 1: \ \text{trust the school's own data}", font_size=30),
        ]
        rows[1][2].set_color(SHRUNK)
        whys = [why(r"each school's mean residual, \ shrunk"), why(r"signal over signal plus noise"),
                why(r"James--Stein, \ school by school"), why(r"partial pooling")]
        intro = label('Random-intercept predictions shrink each group residual mean', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For a random intercept, the BLUP is simply each school's mean residual, shrunk. "
            "<bookmark mark='b'/> The shrinkage factor is the between-school variance over itself plus the variance of a "
            "school mean: signal over signal plus noise. <bookmark mark='c'/> A school with few pupils is pulled almost all "
            "the way back to the average school, <bookmark mark='d'/> and a school with many keeps its own estimate. This is "
            "James–Stein again, with a shrinkage that differs by school according to how much data it has: partial pooling."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fit(self):
        d = load("blup")
        hdr = [r"", r"\textbf{programme}", r"\textbf{SE}", r"\textbf{SES}", r"\textbf{SE}"]
        body = [[r"OLS, \ pupils independent", f"{d['ols'][1]:.1f}", f"{d['ols_se'][1]:.1f}", f"{d['ols'][2]:.1f}", f"{d['ols_se'][2]:.2f}"],
                [r"mixed model, \ REML", f"{d['beta'][1]:.1f}", f"{d['se'][1]:.1f}", f"{d['beta'][2]:.1f}", f"{d['se'][2]:.2f}"]]
        t = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A, RAW, SHRUNK])
        t.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(rf"40 schools; \ $\hat\tau = {np.sqrt(d['G']):.0f}$, \ $\hat\sigma = {np.sqrt(d['sigma2']):.0f}$", font_size=22),
            label(r"the programme varies between schools: \ its SE triples", font_size=22, color=RES),
            label(r"SES varies within schools: \ its SE barely changes", font_size=22, color=HIT),
        ), 12.0, 0.25, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fit the World's forty sampled schools with the programme and home background as "
            "fixed effects and a random intercept for each school. <bookmark mark='b'/> The programme's coefficient "
            "has a standard error of twelve, against least squares' three point eight: <bookmark mark='c'/> the "
            "programme varies only between schools, so its information is in the forty schools, as Part 23 found with"
            " cluster-robust errors. <bookmark mark='d'/> Home background varies mostly within schools, and its "
            "standard error hardly changes. These model-based errors require suitable mean and covariance "
            "assumptions. This working mean omits school context; chapter nine investigates that omission."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(t[0]), FadeIn(t[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(t[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def picture(self):
        d = load("blup")
        raw, bl, tr = np.asarray(d["raw"]), np.asarray(d["blup"]), np.asarray(d["truth"])
        lo = float(np.floor(min(raw.min(), tr.min()) / 10) * 10)
        hi = float(np.ceil(max(raw.max(), tr.max()) / 10) * 10)
        P = ShrinkagePlot(raw, bl, tr, x_range=(lo, hi), width=10.4, center=[0.6, 0.3, 0], gap=1.6,
                          labels={"raw": "residual mean", "shrunk": "EBLUP", "truth": "realized deviations"},
                          ticks=list(np.arange(lo, hi + 1, 20)), fmt=lambda v: f"{v:.0f}", colors={"raw": RAW, "shrunk": SHRUNK, "truth": TRUE})
        rows = fit_rows(VGroup(
            label(rf"shrinkage $\lambda_g$: \ {d['shrink'][int(np.argmin(d['n_g']))]:.2f} for the smallest school, \ "
                  rf"{d['shrink'][int(np.argmax(d['n_g']))]:.2f} for the largest", font_size=22, color=SHRUNK),
            label(rf"one-fit MSE against centered school + context deviations: \ {d['mse_raw']:.0f} $\to$ {d['mse_blup']:.0f}", font_size=22, color=HIT),
        ), 12.0, 0.22, [0, -2.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Each school's mean residual, its empirical BLUP, and the centered realized "
            "school-plus-context deviation. With fifty to eighty-two pupils per school, the shrinkage factors are "
            "about point nine, so the BLUPs move only a little. <bookmark mark='b'/> Even so they are closer to the "
            "truth on average, a mean squared error of ninety-three against a hundred and one. Under the model, "
            "noisier group means can benefit more from shrinkage. An individual realized effect can still move in the"
            " wrong direction."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(P.lines), FadeIn(P.names), FadeIn(P.ticks), FadeIn(P.raw), FadeIn(P.truth))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a) for a in P.arrows], lag_ratio=0.02), LaggedStart(*[FadeIn(x) for x in P.shrunk], lag_ratio=0.02),
                      FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def predict(self):
        rows = [
            cmath(r"\text{a school in the data}", r":", r"x^\top\hat\beta + \hat u_g", font_size=30),
            cmath(r"\text{new pupil, new school}", r":", r"x^\top\hat\beta, \ \ \text{variance } \tau^2 + \sigma^2 + x^\top\mathrm{Var}(\hat\beta)x", font_size=28),
            cmath(r"\mathrm{Var}(\hat u_g - u_g)", r"=", r"(1 - \lambda_g)\,\tau^2 \quad(\beta,G,R \text{ known})", font_size=30),
            cmath(r"\text{BLUP}", r"\ne", r"\text{an estimate of a parameter}", font_size=30),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"its own BLUP"), why(r"only the population of schools"), why(r"less uncertain the more pupils"),
                why(r"`prediction': \ $u_g$ is random")]
        intro = label('Prediction uncertainty depends on what was estimated', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For a pupil in an observed school, add the school's empirical BLUP to the "
            "fixed-effect prediction. <bookmark mark='b'/> For a new pupil in an independent new school, prediction "
            "variance includes both school and pupil variation, plus fixed-effect uncertainty. A new school mean "
            "would instead average its pupil noise. <bookmark mark='c'/> The simple shrinkage error variance "
            "displayed assumes the fixed mean and variance components are known. Estimating beta adds uncertainty; "
            "estimating the variance components adds more. <bookmark mark='d'/> With estimated components these are "
            "empirical BLUPs. Their optimality relies on the stated mean and covariance assumptions."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
