from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats23.common import *  # noqa: F403


class Hetero(VoiceoverScene):
    def construct(self):
        self.card()
        self.ehw()
        self.testing()
        self.sources()
        self.scatter_()
        self.family()
        self.coverage()
        self.board()

    def card(self):
        card = chapter_card(4, r"Heteroskedasticity theory", r"Eicker, \ Huber, \ White, \ and small samples", lit=(1980,), part=PART)
        with self.voiceover("Chapter four. Heteroskedasticity theory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ehw(self):
        rows = [
            cmath(r"\mathrm{Var}(\varepsilon \mid X)", r"=", r"\mathrm{diag}(\sigma_1^2, \dots, \sigma_n^2)", font_size=30),
            cmath(r"\mathrm{Var}(\hat\beta)", r"=", r"(X^\top X)^{-1} \textstyle\sum_i \sigma_i^2 x_i x_i^\top (X^\top X)^{-1}", font_size=28),
            cmath(r"\text{HC0}", r":", r"\sigma_i^2 \to e_i^2", font_size=30),
            cmath(r"\text{why it works}", r":", r"\tfrac1n \textstyle\sum e_i^2 x_i x_i^\top \to E\,\sigma_i^2 x_i x_i^\top", font_size=30),
        ]
        rows[2][2].set_color(OLS_C)
        whys = [why(r"each error its own unknown variance"), why(r"chapter one's sandwich"),
                why(r"Eicker (1963), \ Huber (1967), \ White (1980)"), why(r"one $e_i^2$ is a bad guess; \ their average is not")]
        intro = label('Robust covariance estimates a weighted sum of variances', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Now suppose each error has its own variance, and we don't know any of them. "
            "<bookmark mark='b'/> The sandwich from chapter one has the sum of sigma i squared x i x i transpose in "
            "the middle. <bookmark mark='c'/> Friedhelm Eicker, Peter Huber and Halbert White each proposed replacing"
            " each unknown variance by that observation's squared residual: HC zero, Part 12's robust standard error."
            " <bookmark mark='d'/> One squared residual is a terrible estimate of one variance, but we never need the"
            " variances individually, only a weighted average of them, and under independent sampling, sufficient "
            "moments and controlled leverage, the weighted sum consistently estimates the covariance."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def testing(self):
        rows = [
            cmath(r"\text{studentized BP}", r":", r"\text{regress } e_i^2 \text{ on } x_i: \ nR^2 \sim \chi^2_{p-1}", font_size=30),
            cmath(r"\text{White's test}", r":", r"\text{add squares and cross-products of } x", font_size=30),
            cmath(r"\text{pre-testing}", r":", r"\text{choosing SEs by a test can distort inference}", font_size=28),
            cmath(r"\text{advice}", r":", r"\text{report robust SEs; \ model the variance if it matters}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"Koenker (1981): studentized BP"), why(r"White (1980)"), why(r"the test has low power when $n$ is small"),
                why(r"Part 30; \ and chapter three's WLS")]
        intro = label('Variance tests and robust standard errors need regularity conditions', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Should you test for heteroskedasticity first? The studentized Breusch–Pagan "
            "variant, associated with Koenker, regresses squared residuals on predictors. Under the null and suitable"
            " moment conditions, n times its R squared has an asymptotic chi-squared reference. <bookmark mark='b'/> "
            "White's version adds squares and products of the predictors. <bookmark mark='c'/> But testing first, and"
            " using the classical standard error when the test passes, works badly: in small samples, exactly where "
            "the classical formula fails, the test often lacks the power to notice. <bookmark mark='d'/> The modern "
            "habit is simpler: report robust standard errors routinely, and model the variance with weighted least "
            "squares only when efficiency matters."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sources(self):
        rows = [
            cmath(r"\text{averages}", r":", r"\mathrm{Var} = \sigma^2/m_i", font_size=30),
            cmath(r"\text{multiplicative}", r":", r"y = \mu(x)\, e^{\varepsilon} \Rightarrow \mathrm{SD} \propto \mu", font_size=30),
            cmath(r"\text{counts, \ proportions}", r":", r"\mathrm{Var} \text{ is a function of the mean}", font_size=30),
            cmath(r"\text{a missing interaction}", r":", r"\text{a slope that varies across people}", font_size=30),
        ]
        rows[1][2].set_color(OLS_C)
        whys = [why(r"chapter three's weights"), why(r"log the outcome: \ Part 12"), why(r"Part 24's variance functions"),
                why(r"random slopes: \ Part 25")]
        intro = label('Uneven conditional noise can arise through several mechanisms', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Where does uneven noise come from? <bookmark mark='a'/> Averages of unequal groups, as chapter three's "
            "weights assumed. <bookmark mark='b'/> Multiplicative errors, common in money and biology, make the "
            "spread grow with the mean; a log transform can stabilize multiplicative noise when its distribution is "
            "stable. The transformed mean is a different estimand. <bookmark mark='c'/> Counts and proportions have "
            "variances tied to their means, which Part 24 builds in. <bookmark mark='d'/> And a slope that differs "
            "from person to person, an interaction left out of the model, shows up as noise that grows with x: the "
            "random slopes of Part 25."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scatter_(self):
        d = load("hc")
        x, y, lev = np.asarray(d["x"]), np.asarray(d["y"]), np.asarray(d["lev"])
        A = axes([0, float(np.ceil(x.max()))], [float(np.floor(min(y.min(), 0))), float(np.ceil(y.max() + 1))], x_length=8.0,
                 y_length=4.4, xlabel=r"$x$", ylabel=r"$y$", xticks=list(range(0, int(np.ceil(x.max())) + 1)), yticks=[],
                 center=[-1.6, 0.3, 0])
        ax = A.ax
        r = 0.05 + 0.25 * lev / lev.max()
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=rr, color=OLS_C, fill_opacity=0.75) for a, b, rr in zip(x, y, r)])
        a, b = d["coef"]
        x1 = float(np.ceil(x.max()))
        line = Line(ax.c2p(0, a), ax.c2p(x1, a + b * x1), color=FIT, stroke_width=3)
        k = int(np.argmax(lev))
        rows = fit_rows(VGroup(
            label(rf"$n = {d['n']}$; \ $y = 1 + 2x + x\,\varepsilon$", font_size=22),
            label(r"the noise grows with $x$", font_size=22, color=RES),
            label(r"dot size: \ leverage $h_{ii}$", font_size=22, color=OLS_C),
            label(rf"largest: \ $h = {lev[k]:.2f}$ \ ($p/n = {d['p_over_n']:.2f}$)", font_size=22),
            label(r"its residual is shrunk towards zero", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Small samples are where it goes wrong. Thirty points, with noise proportional to x,"
            " and x skewed, so a few points sit far to the right. <bookmark mark='b'/> Those far points are both the "
            "noisiest and, <bookmark mark='c'/> drawn here by size, the ones with the most leverage. <bookmark "
            "mark='d'/> This sample's largest leverage is far above the average, p over n. <bookmark mark='e'/> A "
            "high-leverage point pulls the line towards itself, which can make its residual too small. In this "
            "experiment that damages HC zero most where uncertainty matters most; it is not a pointwise law for every"
            " heteroskedastic design."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots), Create(line))
            for k_, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k_]))
                if m_ == "d":
                    self.play(Indicate(dots[k], color=PATH))
        self.clear_scene()

    def family(self):
        rows = [
            cmath(r"E\, e_i^2", r"=", r"(1 - h_{ii})\sigma^2 \ \ \text{(homoskedastic case)}", font_size=30),
            cmath(r"\text{HC1}", r":", r"e_i^2 \cdot n/(n - p)", font_size=30),
            cmath(r"\text{HC2}", r":", r"e_i^2 / (1 - h_{ii})", font_size=30),
            cmath(r"\text{HC3}", r":", r"e_i^2 / (1 - h_{ii})^2 \ \approx \ \text{the jackknife}", font_size=30),
        ]
        rows[3][2].set_color(OLS_C)
        whys = [why(r"residuals are too small, \ most at high leverage"), why(r"a degrees-of-freedom fix"),
                why(r"unbiased if the errors were equal"), why(r"MacKinnon \& White (1985): \ small-sample experiments")]
        intro = label('Leverage corrections adjust residual-based covariance estimates', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Residuals are systematically too small: even with equal errors, the expected "
            "squared residual is one minus the leverage, times sigma squared. <bookmark mark='b'/> HC one inflates "
            "every residual by the same degrees-of-freedom factor. <bookmark mark='c'/> HC two divides each by one "
            "minus its own leverage, giving an unbiased covariance estimator under a correct linear mean with "
            "homoskedastic uncorrelated errors, not an exact confidence interval. <bookmark mark='d'/> HC three "
            "divides by the square, inflating the leverage correction further; MacKinnon and White found good "
            "small-sample performance in their experiments, and it is close to the jackknife variance of Part 16."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def coverage(self):
        d = load("hc")
        c = d["coverage"]
        items = [(r"classical", c["classical"], RES), (r"HC0", c["HC0"], OLS_C), (r"HC1", c["HC1"], OLS_C),
                 (r"HC2", c["HC2"], OLS_C), (r"HC3", c["HC3"], GLS_C), (r"wild bootstrap-$t$", c["wild"], HIT)]
        A = axes([0.6, 1.0], [0, 6.6], x_length=8.0, y_length=4.4, xlabel=r"coverage of the 95\% interval, \ $n = 30$",
                 xticks=[0.6, 0.7, 0.8, 0.9, 1.0], yticks=[], center=[0.8, 0.2, 0], xfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        nom = DashedLine(ax.c2p(0.95, 0), ax.c2p(0.95, 6.6), color=TRUE, stroke_width=2.5)
        bars, labs = VGroup(), VGroup()
        for k, (name, v, col) in enumerate(items):
            y = 6 - k
            bars.add(Line(ax.c2p(0.6, y), ax.c2p(v, y), color=col, stroke_width=14))
            labs.add(VGroup(label(name, font_size=22, color=col).next_to(ax.c2p(0.6, y), LEFT, buff=0.25),
                            label(rf"{100 * v:.1f}\%", font_size=22, color=col).next_to(ax.c2p(v, y), RIGHT, buff=0.15)))
        with self.voiceover(
            "<bookmark mark='a'/> Four thousand samples of thirty for the covariance formulas, and one thousand for "
            "the more expensive wild-bootstrap procedure. The classical interval covers the true slope seventy-six "
            "percent of the time. <bookmark mark='b'/> HC zero, eighty-two; HC one and HC two, a little better; "
            "<bookmark mark='c'/> HC three, ninety-one: the best of the formulas, still short. <bookmark mark='d'/> "
            "The wild bootstrap does better still. Fit the tested null, keep its restricted fitted values, multiply "
            "its residuals by random signs, refit, and compare studentized statistics. This retains estimated "
            "variance patterns; it does not reveal each unknown variance. It covers ninety-three."
        ) as vo:
            self.add(label(r"4,000 formula samples; 1,000 wild-bootstrap samples", font_size=22).move_to([0, 3.3, 0]))
            self.play(FadeIn(A), Create(nom))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], LEFT), FadeIn(labs[0]))
            vo.wait_until("b")
            for k in (1, 2, 3):
                self.play(GrowFromEdge(bars[k], LEFT), FadeIn(labs[k]), run_time=0.6)
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[4], LEFT), FadeIn(labs[4]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[5], LEFT), FadeIn(labs[5]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=23) if r.part == 23][5:8]
        b = coverage_board(rows, lit_part=23, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> To the Board, with a fresh thousand samples. HC zero: eighty-one percent, broken. "
            "<bookmark mark='b'/> HC three: ninety, closer but still broken at this sample size. <bookmark mark='c'/>"
            " The wild bootstrap-t: ninety-four, kept. In this experiment resampling outperforms the displayed "
            "covariance formulas. Its finite-sample performance still depends on the design and resampling method."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()
