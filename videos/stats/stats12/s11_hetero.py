from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats12.common import *  # noqa: F403


class Hetero(VoiceoverScene):
    def construct(self):
        self.card()
        self.funnel()
        self.why_wrong()
        self.sandwich()
        self.log_fix()
        self.board()
        self.advice()

    def card(self):
        card = chapter_card(10, r"Uneven noise", r"When the classical standard errors lie", lit=(1980,), part=PART)
        with self.voiceover("Chapter ten. Uneven noise."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def funnel(self):
        d = load("hetero")
        age, inc = np.asarray(d["age"]), np.asarray(d["inc"])
        A = axes([18, 67], [0, 150], x_length=6.4, y_length=4.6, xlabel=r"age", ylabel=r"income (thousands)", xticks=[20, 30, 40, 50, 60],
                 yticks=[0, 50, 100, 150], center=[-2.8, -0.3, 0])
        ax = A.ax
        keep = inc < 150
        pts = scatter(ax, age[keep], inc[keep], radius=0.04, opacity=0.6)
        ln = fit_line(ax, d["coef"][0], d["coef"][1], 18, 67)
        rows = fit_rows(VGroup(
            label(r"the World's working-age adults: \ the spread of incomes grows with their level", font_size=22),
            label(r"heteroskedasticity: \ $\mathrm{Var}(\varepsilon_i)$ depends on $x_i$", font_size=24, color=OBS),
            MathTex(rf"\hat\beta_{{\text{{age}}}} = {d['coef'][1]:.2f}\ \text{{thousand per year}}", font_size=26, color=FIT),
            MathTex(rf"\text{{classical SE}}\ {d['se'][1]:.3f},\quad \text{{HC3}}\ {d['hc3'][1]:.3f}", font_size=26),
            label(r"close here; \ chapter 9's funnel is mild", font_size=22, color=GREY_A),
        ), 5.4, 0.32, [3.9, -0.2, 0])
        tag = simulated_tag(r"the World: \ 400 adults under 67", corner=DR)
        with self.voiceover(
            "Gauss–Markov and the classical standard errors assume every observation has the same error variance. "
            "<bookmark mark='a'/> Real data often don't. Here are four hundred of the World's working-age adults: income against "
            "age. The spread of incomes grows with their level, a funnel. <bookmark mark='b'/> Unequal variances are called "
            "heteroskedasticity. <bookmark mark='c'/> Least squares still estimates the slope without bias, about seven hundred "
            "a year. <bookmark mark='d'/> Here the classical standard error and a robust one, which we'll build in a moment, "
            "happen to agree. But they don't always."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.003), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def why_wrong(self):
        d = load("hetsim")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        A = axes([0, 6], [-10, 16], x_length=6.0, y_length=4.6, xlabel=r"$x \sim$ Exponential", ylabel=r"$y = 1 + x + x\,\varepsilon$", xticks=[0, 2, 4, 6],
                 yticks=[-10, 0, 10], center=[-3.0, -0.3, 0])
        ax = A.ax
        keep = (x < 6) & (y > -10) & (y < 16)
        pts = scatter(ax, x[keep], y[keep], radius=0.04, opacity=0.7)
        ln = fit_line(ax, d["coef"][0], d["coef"][1], 0, 6)
        rows = fit_rows(VGroup(
            label(r"the worst case: \ the noise is largest exactly where $x$ is extreme", font_size=24),
            label(r"those points have the most leverage on the slope", font_size=24, color=OBS),
            MathTex(rf"\text{{classical SE}}\ {d['se'][1]:.3f}\quad\text{{vs}}\quad\text{{HC3}}\ {d['hc3'][1]:.3f}", font_size=28),
            label(r"the classical formula assumes their noise is average: \ it is 2.8 times too small", font_size=22, color=MISS),
        ), 5.4, 0.34, [3.9, -0.3, 0])
        tag = simulated_tag(r"simulated: \ 200 points", corner=DR)
        with self.voiceover(
            "When do they disagree? <bookmark mark='a'/> When the noise is biggest exactly where x is extreme. Here's a "
            "simulated case: a skewed x, and errors whose spread is proportional to x. <bookmark mark='b'/> The extreme x's "
            "have the most leverage on the slope, and they're also the noisiest points. <bookmark mark='c'/> The classical "
            "formula pretends their noise is average, and reports a standard error of point zero nine five. The robust "
            "standard error is point two seven: nearly three times larger. <bookmark mark='d'/> Intervals built on the "
            "classical one would be far too narrow."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.005), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def sandwich(self):
        rows = [
            cmath(r"\mathrm{Var}\,\hat\beta", r"=", r"(X^\top X)^{-1}X^\top\,\Sigma\,X\,(X^\top X)^{-1}", font_size=34),
            cmath(r"\Sigma = \sigma^2 I", r"\Rightarrow", r"\sigma^2(X^\top X)^{-1}", r"\quad\text{the classical formula}", font_size=32),
            cmath(r"\widehat{\mathrm{Var}}_{\mathrm{HC0}}", r"=", r"(X^\top X)^{-1}\Big(\sum_i e_i^2\,x_i x_i^\top\Big)(X^\top X)^{-1}", font_size=32),
            cmath(r"\mathrm{HC3}", r":", r"e_i^2 \to \frac{e_i^2}{(1 - h_{ii})^2}", font_size=34),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"exact, \ for any error covariance $\Sigma$: \ a sandwich"), why(r"only if every variance is equal"),
                why(r"White (1980): \ estimate the meat with squared residuals"), why(r"MacKinnon \& White (1985): \ inflate high-leverage residuals")]
        with self.voiceover(
            "<bookmark mark='a'/> The exact variance of beta-hat, for any error covariance, is a sandwich: X transpose X inverse "
            "on both sides, and X transpose Sigma X in the middle. <bookmark mark='b'/> If every variance is equal, the middle "
            "collapses and you get the classical formula. <bookmark mark='c'/> Halbert White's insight, in 1980, published "
            "in what became one of the most cited papers in economics: you can't estimate each error variance, but you don't "
            "need to. Estimate the middle of the sandwich with the squared residuals, and the result is consistent whatever "
            "the pattern of variances. <bookmark mark='d'/> James MacKinnon and White's HC3 version divides each squared "
            "residual by one minus its leverage, squared, because high-leverage points have deceptively small residuals, "
            "as chapter nine showed. It behaves best in small samples."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=12) if r.part == 12]
        b = coverage_board(rows, lit_part=12, placeholders=0, font_size=20, row_h=0.6)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "The Coverage Board settles it, with the ninety-five percent interval for the slope. <bookmark mark='a'/> On the "
            "World's families, where the noise is even, classical and HC3 intervals both keep the promise: ninety-five point "
            "three and ninety-five point two. <bookmark mark='b'/> In the funnel-shaped simulation with fifty points, the "
            "classical interval covers only sixty percent. HC3 covers ninety. Better, but still broken. "
            "<bookmark mark='c'/> With five hundred points, the classical interval gets worse, fifty-five percent, because its "
            "error doesn't shrink with more data: it's the wrong formula. HC3 climbs to ninety-four. Robust standard errors are "
            "large-sample tools, and in small samples with extreme leverage even they fall short."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]), FadeIn(b.body[1]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[2]), FadeIn(b.body[3]))
            vo.wait_until("c")
            self.play(FadeIn(b.body[4]), FadeIn(b.body[5]))
        self.wait(1.0)
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"in practice", font_size=30, color=OBS),
            label(r"plot residuals against fitted values: \ a funnel is visible", font_size=24),
            label(r"report HC3 standard errors by default; \ when they agree with the classical ones, \ nothing is lost", font_size=24),
            label(r"a transformation (log income) often removes the funnel, \ and changes the question to a proportional one", font_size=24,
                  color=GREY_A),
            label(r"if the variance pattern is known, \ weight by it: \ weighted least squares, \ BLUE again", font_size=24, color=GREY_A),
            label(r"correlated errors (clusters, \ time) need other sandwiches: \ Parts 17 and 23", font_size=24, color=GREY_A),
        ), 12.6, 0.4, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In practice: <bookmark mark='b'/> plot the residuals against the fitted values, where a "
            "funnel is easy to see. <bookmark mark='c'/> Report HC3 standard errors by default; when the noise is even they "
            "agree with the classical ones and nothing is lost. <bookmark mark='d'/> A transformation, like taking logs of "
            "incomes, often removes the funnel, and changes the question to one about proportional effects. "
            "<bookmark mark='e'/> If you know how the variance changes, weight each observation by the inverse of its "
            "variance: weighted least squares is the best linear unbiased estimator again. <bookmark mark='f'/> And when errors "
            "are correlated, in clusters or over time, different sandwiches are needed, in Parts 17 and 23."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def log_fix(self):
        d = load("hetero")
        rows = fit_rows(VGroup(
            label(r"the World's incomes on the log scale", font_size=28),
            MathTex(rf"\widehat{{\beta}}_{{\text{{age}}}}\ \text{{on log income}}:\ \ \text{{classical SE}}\ {d['log_se'][1]:.4f},\ \ \text{{HC3}}\ {d['log_hc3'][1]:.4f}",
                    font_size=30),
            label(r"logs turn multiplicative noise into additive noise of constant size", font_size=24, color=OBS),
            label(r"the coefficient now means a percentage: \ about 1.5\% more income per year of age, \ on average, \ under 67", font_size=24,
                  color=GREY_A),
            label(r"choose the scale for the question first; \ fix the standard errors second", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Incomes are a natural case for logs. <bookmark mark='b'/> On the log scale, the classical and "
            "robust standard errors for the age slope agree closely. <bookmark mark='c'/> Taking logs turns noise that grows in "
            "proportion to the level into noise of roughly constant size. <bookmark mark='d'/> And the coefficient changes "
            "meaning, to a percentage change per year of age. <bookmark mark='e'/> Choose the scale for the question first, and "
            "fix the standard errors second."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
