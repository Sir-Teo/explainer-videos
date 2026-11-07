from __future__ import annotations

import numpy as np

from videos.stats.stats23.common import *  # noqa: F403


class Approx(VoiceoverScene):
    def construct(self):
        self.card()
        self.target()
        self.picture()
        self.depends()
        self.toy()
        self.bootstraps()
        self.lesson()

    def card(self):
        card = chapter_card(6, r"Models as approximations", r"What a wrong line estimates", lit=(2019,), part=PART)
        with self.voiceover("Chapter six. Models as approximations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def target(self):
        rows = [
            cmath(r"\mu(x)", r"=", r"E(y \mid x), \ \text{any shape}", font_size=30),
            cmath(r"\beta^*", r"=", r"\arg\min_b E\,(y - x^\top b)^2 = (E\,xx^\top)^{-1} E\,xy", font_size=30),
            cmath(r"\hat\beta", r"\to", r"\beta^*, \ \ \text{the best linear predictor}", font_size=30),
            cmath(r"y - x^\top\beta^*", r"=", r"\underbrace{\mu(x) - x^\top\beta^*}_{\text{nonlinearity}} + \underbrace{y - \mu(x)}_{\text{noise}}", font_size=28),
        ]
        rows[2][2].set_color(TEAL)
        whys = [why(r"the true regression function"), why(r"the population least squares line"),
                why(r"chapter ten of Part 22: \ a projection"), why(r"the nonlinearity acts like an error that depends on $x$")]
        intro = label('The population least-squares projection needs finite second moments', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Suppose the true mean of y given x has any shape at all. <bookmark mark='b'/> There"
            " is a unique best line when second moments exist and the predictor moment matrix is nonsingular: the "
            "population least-squares projection, beta star. <bookmark mark='c'/> Under suitable sampling and moment "
            "conditions least squares estimates it consistently, just as Part 22's maximum likelihood estimate "
            "converged to the closest wrong model. Andreas Buja and colleagues called this, in 2019, the view of "
            "models as approximations. <bookmark mark='d'/> The new twist is that the residual now contains the "
            "nonlinearity, the gap between the curve and the line, which is a function of x and doesn't average out "
            "at each x."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("blp")
        ages, means = np.asarray(d["ages"]), np.asarray(d["means"])
        ex = d["example"]
        A = axes([18, 76], [0, 130], x_length=8.0, y_length=4.4, xlabel=r"age", ylabel=r"income, \ thousands",
                 xticks=[20, 30, 40, 50, 60, 70], yticks=[0, 50, 100], center=[-1.6, 0.3, 0])
        ax = A.ax
        keep = np.asarray(ex["inc"]) < 130
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=GREY_B, fill_opacity=0.6)
                        for a, b in zip(np.asarray(ex["age"])[keep], np.asarray(ex["inc"])[keep])])
        mu = polyline(ax, ages, means, TRUE, 3.5)
        a, b = d["blp"]
        blp = Line(ax.c2p(18, a + 18 * b), ax.c2p(75, a + 75 * b), color=TEAL, stroke_width=4)
        rows = fit_rows(VGroup(
            label(r"grey: \ 200 of the World's adults", font_size=22, color=GREY_B),
            label(r"gold: \ the true mean income at each age", font_size=22, color=TRUE),
            label(rf"teal: \ the best line, \ ${b:.2f}$k per year", font_size=22, color=TEAL),
            label(r"a rise, \ a plateau, \ a drop at 67", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World's incomes against age, for adults up to seventy-five: a sample of two hundred. "
            "<bookmark mark='b'/> The true mean, computed from all the World's adults, rises steeply through the twenties, "
            "levels off, and drops at retirement. <bookmark mark='c'/> The best line through the whole population rises two "
            "hundred and seventy-four a year. <bookmark mark='d'/> It is a summary of a curve: not the effect of a year of "
            "age at any particular age."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(mu), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(blp), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def depends(self):
        d = load("blp")
        ages, means = np.asarray(d["ages"]), np.asarray(d["means"])
        A = axes([18, 76], [20, 70], x_length=8.0, y_length=4.4, xlabel=r"age", ylabel=r"mean income, \ thousands",
                 xticks=[20, 30, 40, 50, 60, 70], yticks=[30, 40, 50, 60], center=[-1.6, 0.3, 0])
        ax = A.ax
        mu = polyline(ax, ages, means, TRUE, 3.5)
        a, b = d["blp"]
        ay, by = d["blp_young"]
        l_all = Line(ax.c2p(18, a + 18 * b), ax.c2p(75, a + 75 * b), color=TEAL, stroke_width=4)
        l_young = Line(ax.c2p(18, ay + 18 * by), ax.c2p(40, ay + 40 * by), color=RED, stroke_width=4)
        rows = fit_rows(VGroup(
            label(rf"teal: \ all adults to 75: \ slope {b:.2f}", font_size=22, color=TEAL),
            label(rf"red: \ adults aged 18--40: \ slope {by:.2f}", font_size=22, color=RED),
            label(r"the same curve, \ a different $\beta^*$", font_size=22),
            label(r"$\beta^*$ depends on who is in the sample", font_size=22, color=RES),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the consequence. The best line for all adults has slope point two seven. "
            "<bookmark mark='b'/> Restrict to adults aged eighteen through forty and the best line has slope one "
            "point one five, four times steeper. <bookmark mark='c'/> The curve is the same; only the distribution of"
            " ages changed. <bookmark mark='d'/> When the model is wrong, what least squares estimates depends on the"
            " distribution of x, so random-design inference must account for the sampled predictor distribution, and "
            "a study of the young and a study of everyone are estimating different numbers."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), Create(mu))
            vo.wait_until("a")
            self.play(Create(l_all), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(l_young), FadeIn(rows[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def toy(self):
        d = load("blp")
        x, y = np.asarray(d["toy_x"]), np.asarray(d["toy_y"])
        A = axes([-3, 3], [-1, 9], x_length=6.0, y_length=4.4, xlabel=r"$x \sim N(0, 1)$", ylabel=r"$y$",
                 xticks=[-2, 0, 2], yticks=[0, 4, 8], center=[-3.0, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=GREY_B) for a, b in zip(x, y) if -3 < a < 3])
        gr = np.linspace(-2.9, 2.9, 100)
        cv = curve(ax, gr, gr ** 2, TRUE, 3)
        a, b = d["toy_fit"]
        line = Line(ax.c2p(-3, a - 3 * b), ax.c2p(3, a + 3 * b), color=TEAL, stroke_width=3.5)
        c = d["toy"]
        rows = fit_rows(VGroup(
            label(r"$y = x^2 + $ noise: \ $\beta^*$ slope $= 0$", font_size=22),
            label(r"the residual: \ $x^2 - 1 + 0.3Z$, \ $Z$ independent", font_size=22, color=GREY_A),
            label(rf"classical SE: \ covers {100 * c['classical']:.0f}\%", font_size=22, color=RES),
            label(rf"HC3 sandwich: \ covers {100 * c['HC3']:.0f}\%", font_size=22, color=HIT),
            label(r"projection residual second moments depend on $x$", font_size=22, color=TEAL),
        ), 5.0, 0.42, [3.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The standard errors change too. The plainest example: x standard normal, y equal to"
            " x squared plus a little noise. The best line is flat, slope zero. <bookmark mark='b'/> Its projection "
            "residual, x squared minus one plus independent noise with standard deviation point three, is largest "
            "exactly where x is far from zero, the points that drive the slope. <bookmark mark='c'/> The classical "
            "standard error ignores that, and its intervals cover the target sixty-one percent of the time in samples"
            " of a hundred. <bookmark mark='d'/> The sandwich covers ninety-four. <bookmark mark='e'/> With random "
            "predictors, the squared projection residual depends on x, even though the noise has constant conditional"
            " variance. The empirical-score sandwich accounts for both sources of variation under suitable moments. "
            "For the World's incomes the two kinds of standard error happen to agree, covering ninety-six percent, "
            "but nothing guaranteed that in advance."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots), Create(cv))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def bootstraps(self):
        rows = [
            cmath(r"\text{residual bootstrap}", r":", r"y^* = X\hat\beta + e^*, \ \ e^* \text{ resampled}", font_size=30),
            cmath(r"\text{pairs bootstrap}", r":", r"(x_i, y_i)^* \text{ resampled together}", font_size=30),
            cmath(r"\text{wild bootstrap}", r":", r"y_i^* = x_i^\top\hat\beta + w_i e_i", font_size=30),
            cmath(r"\text{which?}", r":", r"\text{pairs: iid random design, finite moments, regularity}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"assumes equal, \ exchangeable errors: \ the classical SE"), why(r"Freedman (1981): \ the sandwich"),
                why(r"fixed $X$, \ any variances: \ chapter four"), why(r"Buja et al.: \ it targets $\beta^*$")]
        intro = label('The resampling scheme must match the sampling target', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Part 16's bootstrap comes in three flavours for regression, and they answer different questions. "
            "<bookmark mark='a'/> The residual bootstrap keeps the fitted line and reshuffles residuals: it assumes "
            "the errors are interchangeable, and reproduces the classical standard error. <bookmark mark='b'/> The "
            "pairs bootstrap resamples whole observations, x and y together, as David Freedman analysed in 1981: it "
            "reproduces the sandwich. <bookmark mark='c'/> The wild bootstrap keeps each x and flips each residual: "
            "fixed predictors, a suitable mean model and uneven variances, under bootstrap regularity conditions. "
            "<bookmark mark='d'/> When the model may be wrong and the predictors were sampled, the pairs bootstrap "
            "can target beta star with iid sampling, adequate moments and a nonsingular design. Dependence or very "
            "heavy tails require further care."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"a linear model is a summary, \ even when it is wrong", font_size=24, color=TEAL),
            label(r"its target $\beta^*$ depends on the distribution of $x$", font_size=24),
            label(r"its honest SE is the sandwich; \ the pairs bootstrap agrees", font_size=24, color=HIT),
            label(r"a coefficient is not an effect without a causal argument: \ Parts 35--37", font_size=24, color=RES),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So a linear model is a useful summary even when it is wrong, <bookmark mark='b'/> but the "
            "thing it summarizes depends on who was sampled. <bookmark mark='c'/> Its honest standard error is the sandwich, "
            "and a bootstrap that resamples whole observations, x and y together, agrees with it. <bookmark mark='d'/> And a "
            "coefficient, right or wrong, is a description, not an effect; turning it into a causal claim needs the "
            "arguments of Parts 35 to 37."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
