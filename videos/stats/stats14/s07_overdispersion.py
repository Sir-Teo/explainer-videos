from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats14.common import *  # noqa: F403


class Overdispersion(VoiceoverScene):
    def construct(self):
        self.card()
        self.towns()
        self.mean_variance()
        self.ses()
        self.remedies()
        self.board()

    def card(self):
        card = chapter_card(6, r"Overdispersion", r"When the counts vary more than Poisson allows", part=PART)
        with self.voiceover("Chapter six. Overdispersion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def towns(self):
        d = load("clinic")
        east, rate, adults = np.asarray(d["east"]), np.asarray(d["rate"]), np.asarray(d["adults"])
        fr = np.asarray(d["fitted_rate"])
        A = axes([-0.9, 1.0], [np.log(0.8), np.log(100)], x_length=7.2, y_length=4.4, xlabel=r"town's position, \ west $\to$ east",
                 ylabel=r"visits per 1{,}000 adults \ (log scale)", xticks=[-0.5, 0, 0.5], yticks=[np.log(1), np.log(10), np.log(100)],
                 center=[-2.2, 0.2, 0], yfmt=lambda v: f"{np.exp(v):.0f}")
        ax = A.ax
        big = adults > np.quantile(adults, 0.5)
        dots = VGroup(*[Dot(ax.c2p(e, np.log(r)), radius=0.05 + 0.05 * b_, color=S.WORLD if b_ else GREY_B, fill_opacity=0.85)
                        for e, r, b_ in zip(east, rate, big)])
        order = np.argsort(east)
        ln = VMobject(stroke_color=FIT, stroke_width=4).set_points_as_corners([ax.c2p(e, np.log(f_)) for e, f_ in zip(east[order], fr[order])])
        b0, b1 = d["coef"]
        rows = fit_rows(VGroup(
            label(r"one month's clinic visits in the World's 200 towns", font_size=22),
            label(r"offset: \ log adults in the town", font_size=22),
            MathTex(rf"\hat\beta_{{\text{{east}}}} = {b1:.3f}", font_size=28, color=FIT),
            label(r"big towns (green) scatter far more than Poisson noise allows", font_size=22, color=RES),
            label(r"towns differ in ways the model leaves out", font_size=22, color=GREY_A),
        ), 4.6, 0.34, [4.5, 0.2, 0])
        tag = simulated_tag(r"simulated visits, \ the World's towns", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> A second count: a month of clinic visits in each of the World's two hundred towns, simulated "
            "on the World's real town sizes. <bookmark mark='b'/> The model is the same: Poisson, with the log of the town's "
            "adults as the offset, and the town's east-west position as the predictor. <bookmark mark='c'/> The fitted slope "
            "is point two three on the log scale. <bookmark mark='d'/> But look at the big towns, in green. With tens of "
            "thousands of adults, Poisson noise in their rates should be tiny; instead they scatter by a factor of three or more. "
            "<bookmark mark='e'/> The towns differ in ways the model leaves out: doctors, habits, distance to the clinic. That "
            "extra variation is overdispersion."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dots, lag_ratio=0.01), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def mean_variance(self):
        d = load("clinic")
        y = np.asarray(d["y"], float)
        mu = np.asarray(d["fitted_rate"]) * np.asarray(d["adults"]) / 1000
        r2 = (y - mu) ** 2
        A = axes([0, 7.5], [-4, 14], x_length=7.0, y_length=4.4, xlabel=r"fitted mean $\hat\mu$ \ (log scale)", ylabel=r"$(y - \hat\mu)^2$ \ (log scale)",
                 xticks=[np.log(10), np.log(100), np.log(1000)], yticks=[0, np.log(100), np.log(10000), np.log(1e6)], center=[-2.4, 0.2, 0],
                 xfmt=lambda v: f"{np.exp(v):,.0f}", yfmt=lambda v: f"{np.exp(v):,.0f}")
        ax = A.ax
        keep = r2 > 0.02
        dots = VGroup(*[Dot(ax.c2p(np.log(m), np.log(v)), radius=0.05, color=S.WORLD, fill_opacity=0.8) for m, v in zip(mu[keep], r2[keep])])
        xs = np.linspace(np.log(3), 7.4, 100)
        l1 = curve(ax, xs, xs, NULLC, 3)
        l2 = curve(ax, xs, np.log(np.exp(xs) + np.exp(2 * xs) / 4), RES, 3)
        rows = fit_rows(VGroup(
            label(r"each town's squared residual against its fitted mean", font_size=22),
            label(r"grey: \ Poisson, \ variance $= \mu$", font_size=22, color=NULLC),
            label(r"red: \ variance $= \mu + \mu^2/4$", font_size=22, color=RES),
            MathTex(rf"\hat\phi = {d['dispersion']:.1f}", font_size=32, color=RES),
            label(r"the variance grows like $\mu^2$, \ not $\mu$", font_size=22, color=OBS),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Plot each town's squared residual against its fitted mean, both on log scales. "
            "<bookmark mark='b'/> If the counts were Poisson, the points would scatter around the grey line, variance equal to "
            "the mean. <bookmark mark='c'/> Instead they follow the red curve, mu plus mu squared over four, which is what the "
            "simulation built in: each town's rate multiplied by a random factor with a standard deviation of a half. "
            "<bookmark mark='d'/> The Pearson dispersion is twenty-two. <bookmark mark='e'/> For big towns, the variance grows "
            "like the square of the mean, so Poisson's assumption fails worst exactly where the data are most plentiful."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(dots, lag_ratio=0.01), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(l2), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def ses(self):
        d = load("clinic")
        rows = [
            cmath(r"\text{Poisson SE}", r"=", rf"{d['se'][1]:.3f}", font_size=34),
            cmath(r"\text{quasi-Poisson SE}", r"=", rf"\sqrt{{\hat\phi}}\times{d['se'][1]:.3f} = {d['se_quasi'][1]:.3f}", font_size=32),
            cmath(r"\text{sandwich SE}", r"=", rf"{d['se_sandwich'][1]:.3f}", font_size=34),
            cmath(r"\text{the same }\hat\beta", r"=", rf"{d['coef'][1]:.3f}", font_size=32),
        ]
        rows[0][2].set_color(RES)
        rows[2][2].set_color(HIT)
        whys = [why(r"assumes variance $= \mu$"), why(r"assumes variance $= \phi\mu$: \ Wedderburn (1974)"),
                why(r"Part 12's HC0: \ no variance model at all"), why(r"the estimate is fine; \ its uncertainty was not")]
        with self.voiceover(
            "What does it do to the inference? <bookmark mark='a'/> The Poisson standard error of the slope is point zero two "
            "one: it believes each big town is a nearly exact measurement. <bookmark mark='b'/> Robert Wedderburn's "
            "quasi-likelihood of 1974 keeps the estimating equations and scales the variance by the dispersion: the standard "
            "error grows by the square root of twenty-two, to point one oh. <bookmark mark='c'/> The sandwich standard error "
            "of Part 12 assumes nothing about the variance and gives point one eight, larger still, because here the variance "
            "isn't proportional to the mean. <bookmark mark='d'/> All three share the same estimate. Overdispersion leaves the "
            "coefficient usable and makes its Poisson standard error wrong by a factor of eight."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def remedies(self):
        rows = fit_rows(VGroup(
            label(r"quasi-Poisson: \ variance $\phi\mu$; \ a quick fix when the variance is roughly proportional", font_size=24),
            label(r"negative binomial: \ a gamma-mixed Poisson, \ variance $\mu + \mu^2/k$ \ (Greenwood \& Yule 1920)", font_size=24, color=S.ALT),
            label(r"sandwich standard errors: \ robust to any variance, \ with enough units", font_size=24, color=HIT),
            label(r"random effects: \ model the towns' differences directly \ (Part 25)", font_size=24, color=S.PRIOR),
            label(r"always check: \ dispersion, \ deviance on its df, \ residuals against fitted means", font_size=24, color=OBS),
        ), 12.4, 0.44, [0, 0, 0])
        with self.voiceover(
            "The remedies. <bookmark mark='a'/> Quasi-Poisson, a quick fix when the variance is roughly proportional to the mean. "
            "<bookmark mark='b'/> The negative binomial, a Poisson whose rate is itself gamma-distributed, with variance mu plus "
            "mu squared over k, exactly our simulation's structure; Major Greenwood and George Udny Yule used it in 1920 for "
            "accident counts among munitions workers. <bookmark mark='c'/> Sandwich standard errors, robust to any variance "
            "pattern when there are enough units. <bookmark mark='d'/> Or random effects, which model the towns' differences "
            "directly, Part 25. <bookmark mark='e'/> And always check before trusting a Poisson standard error: the dispersion, "
            "the deviance against its degrees of freedom, and the residuals against the fitted means."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=14) if r.part == 14]
        b = coverage_board(rows, lit_part=14, placeholders=0, font_size=19, row_h=0.52)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        rb = {(r.method, r.setting): r for r in rows}
        with self.voiceover(
            "The Coverage Board, with eight rows. First, the logistic intervals: twenty-three flights at the Challenger "
            "temperatures, simulated ten thousand times from the fitted curve. In about two percent of samples the zeros and "
            "ones are perfectly separated by temperature, and no finite estimate exists; those count as misses for Wald, while "
            "a profile interval still exists and is checked directly. <bookmark mark='a'/> For the slope, the Wald interval "
            "covers ninety-five point three percent: kept, even with the separated samples counted against it. The profile "
            "interval covers ninety-one point six: broken. <bookmark mark='b'/> For the probability at thirty-one degrees, the "
            "same pattern: Wald ninety-five point three, profile ninety-one point five. So at twenty-three flights it's the "
            "theoretically better interval that falls short, because the chi-squared calibration of the likelihood ratio is "
            "itself a large-sample result, while the Wald interval here is saved by being very wide. Small samples keep "
            "asymptotic theory honest, and Part 16's bootstrap and Part 22's corrections return to this. "
            "<bookmark mark='c'/> Then the Poisson rate ratio on the two hundred towns. With truly Poisson counts, the classical "
            "interval keeps its promise. <bookmark mark='d'/> With the towns' extra variation, it covers less than a fifth of "
            "the time. Quasi-Poisson repairs part of the damage, about two thirds; the sandwich covers about ninety-one percent: "
            "better, still short with two hundred towns. The right fix depends on getting the variance right, and Part 24 "
            "returns to it."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]), FadeIn(b.body[1]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[2]), FadeIn(b.body[3]))
            vo.wait_until("c")
            self.play(FadeIn(b.body[4]))
            vo.wait_until("d")
            self.play(FadeIn(b.body[5]), FadeIn(b.body[6]), FadeIn(b.body[7]))
        del rb
        self.wait(1.0)
        self.clear_scene()
