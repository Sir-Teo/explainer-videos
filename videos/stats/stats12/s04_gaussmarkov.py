from __future__ import annotations

import numpy as np

from videos.stats.stats12.common import *  # noqa: F403


class GaussMarkov(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.proof()
        self.rival()
        self.wls()
        self.limits()

    def card(self):
        card = chapter_card(3, r"Gauss--Markov", r"Why least squares is the best linear unbiased estimator", lit=(1821,), part=PART)
        with self.voiceover("Chapter three. The Gauss–Markov theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def statement(self):
        tc = theorem_card(r"Gauss--Markov", r"If $y = X\beta + \varepsilon$ with $E\varepsilon = 0$ and $\mathrm{Var}\,\varepsilon = \sigma^2 I$ \ "
                          r"(uncorrelated, \ equal variances, \ \emph{not necessarily normal}), \ then for any linear unbiased estimator "
                          r"$\tilde\beta = Cy$ \ and any vector $c$, \ $\mathrm{Var}(c^\top\tilde\beta) \ge \mathrm{Var}(c^\top\hat\beta)$.",
                          who=r"Gauss (1821); \ Markov (1912)", color=FIT, width=10.6,
                          font_size=26).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"BLUE: \ the \textbf{B}est \textbf{L}inear \textbf{U}nbiased \textbf{E}stimator", font_size=28, color=OBS),
            label(r"no normality needed: \ only means, \ variances, \ and no correlation between errors", font_size=24),
        ), 12.6, 0.34, [0, -1.7, 0])
        with self.voiceover(
            "Gauss's second justification, from 1821, needs no normal distribution at all. <bookmark mark='a'/> Suppose the "
            "errors have mean zero, are uncorrelated, and all have the same variance. Then among all estimators that are "
            "linear in y and unbiased, least squares has the smallest variance, for every coefficient and every linear "
            "combination of coefficients. Andrey Markov restated it in 1912, and it has carried both their names since the 1930s. "
            "<bookmark mark='b'/> Least squares is BLUE: the best linear unbiased estimator. <bookmark mark='c'/> And the "
            "conditions are mild: means, variances, and no correlation between the errors."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\tilde\beta = Cy,\quad C", r"=", r"(X^\top X)^{-1}X^\top + D", font_size=32),
            cmath(r"E\tilde\beta = \beta \ \forall\beta", r"\Rightarrow", r"DX = 0", font_size=32),
            cmath(r"\mathrm{Var}\,\tilde\beta", r"=", r"\sigma^2 CC^\top = \sigma^2\big((X^\top X)^{-1} + DD^\top\big)", font_size=32),
            cmath(r"\mathrm{Var}\,\tilde\beta - \mathrm{Var}\,\hat\beta", r"=", r"\sigma^2 DD^\top \succeq 0", font_size=34),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"any linear rule, \ written as OLS plus a difference $D$"), why(r"unbiased for every $\beta$: \ $CX = I$"),
                why(r"the cross terms vanish because $DX = 0$"), why(r"positive semidefinite (Part 4): \ OLS is never beaten")]
        with self.voiceover(
            "The proof is four lines of Part 4's matrix algebra. <bookmark mark='a'/> Write any linear estimator as C times y, "
            "and write C as the least squares matrix plus some difference D. <bookmark mark='b'/> Unbiasedness for every "
            "beta forces D times X to be zero. <bookmark mark='c'/> Its variance is sigma squared C C transpose, and when you "
            "multiply out, the cross terms vanish because D X is zero. <bookmark mark='d'/> So the rival's variance exceeds "
            "least squares' by sigma squared D D transpose, which is positive semidefinite. Every linear combination of the "
            "rival's coefficients has at least as much variance. Least squares is never beaten."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rival(self):
        d = load("gm")
        ed = np.asarray(d["edges"])
        A = axes([-0.5, 1.5], [0, 2.2], x_length=7.4, y_length=4.2, xlabel=r"estimated slope (truth 0.5), \ $n = 20$", ylabel=r"density",
                 xticks=[-0.5, 0, 0.5, 1, 1.5], yticks=[0, 1, 2], center=[-2.0, -0.3, 0])
        ax = A.ax
        h1 = hist_bars(ax, ed, np.minimum(np.asarray(d["h_ols"]), 2.2), color=FIT, opacity=0.6)
        h2 = hist_bars(ax, ed, np.minimum(np.asarray(d["h_end"]), 2.2), color=S.POST, opacity=0.5)
        tr = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 2.2), color=EXACT, stroke_width=2)
        leg = legend([(FIT, r"least squares"), (S.POST, r"the slope through the two end points")], font_size=22).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"both are linear in $y$ \ and unbiased", font_size=24),
            MathTex(rf"\text{{means: }} {d['mean_ols']:.3f},\ {d['mean_end']:.3f}", font_size=26),
            MathTex(rf"\text{{SDs: }} {d['sd_ols']:.3f}\ \text{{vs}}\ {d['sd_end']:.3f}", font_size=28, color=OBS),
            MathTex(rf"\text{{theory: }} {d['theory_ols']:.3f},\ {d['theory_end']:.3f}", font_size=24, color=GREY_A),
            label(r"the end-point rule throws away 18 points", font_size=22, color=GREY_A),
        ), 5.0, 0.32, [4.4, -0.3, 0])
        tag = simulated_tag(r"simulated: \ 20,000 samples, \ errors $N(0, 4)$", corner=DR)
        with self.voiceover(
            "Let's watch a rival lose. <bookmark mark='a'/> Twenty points, a true slope of a half, and a lazy rival: draw the "
            "line through the first and last points. It's linear in y, and it's unbiased. <bookmark mark='b'/> Over twenty "
            "thousand samples both centre on a half. <bookmark mark='c'/> But the end-point slope has a standard deviation of "
            "point three four, and least squares point two one, exactly as theory says. The rival wastes eighteen of the "
            "twenty points."
        ) as vo:
            self.play(FadeIn(A), Create(tr), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(leg), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(h2, lag_ratio=0.01), FadeIn(h1, lag_ratio=0.01), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"what Gauss--Markov does not say", font_size=30, color=OBS),
            label(r"``linear'': \ a nonlinear estimator can win, \ by far, \ when errors have heavy tails (LAD, \ Part 30)", font_size=24),
            label(r"``unbiased'': \ a biased one can win in MSE: \ ridge regression and James--Stein (Parts 25, 32)", font_size=24),
            label(r"``equal variances, \ uncorrelated'': \ otherwise generalized least squares (Aitken, 1935) is BLUE", font_size=24),
            label(r"and it says nothing about standard errors or tests: \ those need more (ch.~4, \ ch.~10)", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> It matters what the theorem doesn't say. <bookmark mark='b'/> It compares only linear "
            "estimators. With heavy-tailed errors a nonlinear estimator, like least absolute deviations, can be far better. "
            "<bookmark mark='c'/> It compares only unbiased ones. Biased estimators like ridge regression can have smaller "
            "mean squared error, Parts 25 and 32. <bookmark mark='d'/> It assumes equal variances and no correlation. When "
            "that fails, Alexander Aitken's generalized least squares, from 1935, is the best linear unbiased estimator "
            "instead. <bookmark mark='e'/> And it says nothing at all about standard errors or tests, which need more, as "
            "the next chapter and chapter ten show."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def wls(self):
        from explainer.stats.kit import ols as O
        g = np.random.Generator(np.random.PCG64(1935))
        n, R = 50, 6000
        x = np.sort(g.uniform(1, 5, n))
        sd = 0.5 * x
        bo, bw = [], []
        for _ in range(R):
            y = 1 + 0.5 * x + sd * g.normal(size=n)
            bo.append(O.fit(O.design(x), y).coef[1])
            w = 1 / sd
            bw.append(O.fit(O.design(x) * w[:, None], y * w).coef[1])
        rows = [
            cmath(r"\mathrm{Var}(\varepsilon_i) = \sigma_i^2", r"\Rightarrow", r"\text{divide row } i \text{ by } \sigma_i", font_size=32),
            cmath(r"\hat\beta_{\mathrm{WLS}}", r"=", r"(X^\top W X)^{-1}X^\top W y,\quad W = \mathrm{diag}(1/\sigma_i^2)", font_size=32),
            cmath(r"\mathrm{SD}(\hat\beta_1)", r":", rf"\text{{OLS }} {np.std(bo):.3f}\quad\text{{vs}}\quad\text{{WLS }} {np.std(bw):.3f}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the rescaled errors have equal variance: \ Gauss--Markov applies"), why(r"Aitken (1935): \ generalized least squares"),
                why(r"SD $\propto x$, \ 6,000 simulated samples of 50: \ both unbiased")]
        with self.voiceover(
            "What if the variances are unequal but known? <bookmark mark='a'/> Divide each row of the data by its error "
            "standard deviation. The rescaled errors all have variance one, so Gauss–Markov applies to the rescaled problem. "
            "<bookmark mark='b'/> That's weighted least squares, the simplest case of Alexander Aitken's generalized least "
            "squares: weight each observation by its inverse variance. <bookmark mark='c'/> In a simulation where the noise "
            "grows with x, both estimators are unbiased, but weighting cuts the slope's standard deviation by about a "
            "quarter. Noisy points should count for less."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
