from __future__ import annotations

import numpy as np

from videos.stats.stats14.common import *  # noqa: F403
from videos.stats.stats14.s02_lpm import flights


class Logistic(VoiceoverScene):
    def construct(self):
        self.card()
        self.odds()
        self.odds_table()
        self.fit_curve()
        self.odds_ratio()
        self.latent()
        self.probit()
        self.canonical()

    def card(self):
        card = chapter_card(2, r"Logistic regression", r"Linear in the log-odds", part=PART)
        with self.voiceover("Chapter two. Logistic regression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def odds(self):
        rows = [
            cmath(r"\text{odds}", r"=", r"\frac{p}{1 - p}\ \in (0, \infty)", font_size=34),
            cmath(r"\text{logit}(p)", r"=", r"\log\frac{p}{1 - p}\ \in (-\infty, \infty)", font_size=34),
            cmath(r"\text{logit}\,p(x)", r"=", r"\beta_0 + \beta_1 x", font_size=36),
            cmath(r"p(x)", r"=", r"\frac{1}{1 + e^{-(\beta_0 + \beta_1 x)}}", font_size=34),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"a gambler's scale: \ ``4 to 1''"), why(r"stretched to the whole line"),
                why(r"the model: \ linear on the logit scale"), why(r"inverted: \ the logistic curve")]
        with self.voiceover(
            "<bookmark mark='a'/> Start from the odds: p over one minus p. A probability of point eight is odds of four to one. "
            "Odds run from zero to infinity. <bookmark mark='b'/> Take the logarithm, and the log-odds, or logit, run over the "
            "whole real line, with a probability of one half at zero. <bookmark mark='c'/> Now regression can do its usual "
            "thing: model the log-odds as a straight line in x. <bookmark mark='d'/> Inverting gives the probability: the "
            "logistic curve. That's logistic regression, popularized for medical data by Joseph Berkson in 1944, and given its "
            "modern form by David Cox in 1958."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def odds_table(self):
        ps = [0.1, 0.2, 0.5, 0.8, 0.9, 0.99, 0.9996]
        tab = table_rows([[r"$p$", r"odds", r"log-odds"]] + [[rf"{p:g}", (rf"{p / (1 - p):,.0f}" if p / (1 - p) >= 100 else rf"{p / (1 - p):.3g}"), rf"{np.log(p / (1 - p)):+.2f}"] for p in ps],
                         font_size=26, col_buff=1.0, row_buff=0.18, colors=[GREY_B] + [None] * 7).move_to([-2.8, 0.2, 0])
        rows = fit_rows(VGroup(
            label(r"near $p = 0.5$, \ logit is nearly linear in $p$", font_size=24),
            label(r"near 0 or 1, \ it stretches: \ 0.99 to 0.9996 is a step of 3.2", font_size=24, color=OBS),
            label(r"odds multiply: \ a factor of 10 in odds is $+2.3$ in log-odds", font_size=24),
        ), 5.0, 0.36, [3.9, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A few values. Between point two and point eight, the log-odds behave much like the "
            "probability itself, stretched out. <bookmark mark='b'/> Near zero or one they stretch enormously: going from "
            "point nine nine to point nine nine nine six, the Challenger number we'll meet, is a step of three point two on "
            "the log-odds scale. <bookmark mark='c'/> And since logs turn products into sums, adding a constant to the "
            "log-odds multiplies the odds: two point three is a factor of ten."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab, lag_ratio=0.05), FadeIn(rows[0]))
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def fit_curve(self):
        d = load("challenger")
        t, y = np.asarray(d["T"]), np.asarray(d["Y"])
        b0, b1 = d["coef"]
        A = axes([25, 85], [-0.1, 1.15], x_length=8.0, y_length=4.0, xlabel=r"launch temperature, \ $^\circ$F", ylabel=r"$P(\text{distress})$",
                 xticks=[30, 40, 50, 60, 70, 80], yticks=[0, 0.5, 1], center=[-2.0, 0.75, 0])
        ax = A.ax
        dots = flights(ax, t, y)
        xs = np.linspace(25, 85, 241)
        cv = curve(ax, xs, 1 / (1 + np.exp(-(b0 + b1 * xs))), OBS, 4)
        half = DashedLine(ax.c2p(d["t50"], 0), ax.c2p(d["t50"], 0.5), color=GREY_B, stroke_width=2)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{logit}}\,\hat p = {b0:.2f} - {abs(b1):.3f}\,T", font_size=30, color=OBS),
            MathTex(rf"\hat p = 0.5\ \text{{at}}\ {d['t50']:.1f}^\circ\text{{F}}", font_size=28),
            MathTex(rf"\hat p(70) = {d['p70']:.2f},\quad \hat p(53) = {d['p53']:.2f}", font_size=28),
            label(r"fitted by maximum likelihood: \ next chapter", font_size=22, color=GREY_A),
        ), 12.4, 0.22, [0, -2.85, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the logistic curve fitted to all twenty-three flights: logit p equals fifteen point "
            "oh four minus point two three two times the temperature. <bookmark mark='b'/> It crosses one half at about "
            "sixty-five degrees, between the warm flights and the cold ones. <bookmark mark='c'/> At seventy degrees it gives a "
            "twenty-three percent chance of distress; at fifty-three, the coldest flight, ninety-four percent. "
            "<bookmark mark='d'/> We'll see how it was fitted in a moment, and what it says at thirty-one degrees after that."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(half), FadeIn(rows[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def odds_ratio(self):
        d = load("challenger")
        b1 = d["coef"][1]
        lo, hi = d["or10_ci"]
        rows = [
            cmath(r"\text{logit}\,p(x + 1) - \text{logit}\,p(x)", r"=", r"\beta_1", font_size=32),
            cmath(r"\frac{\text{odds}(x + 1)}{\text{odds}(x)}", r"=", r"e^{\beta_1}", font_size=32),
            cmath(r"\text{10}^\circ\text{F colder}", r":", rf"e^{{-10\hat\beta_1}} = e^{{{-10 * b1:.2f}}} = {d['or10']:.1f}", font_size=32),
            cmath(r"95\%\ \text{(profile)}", r":", rf"[{lo:.1f},\ {hi:.0f}]", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the slope: \ change in log-odds per degree"), why(r"so $e^{\beta_1}$ is an odds ratio, \ the same at every $x$"),
                why(r"the odds of distress multiply by ten"), why(r"23 flights: \ wide, \ and lopsided")]
        with self.voiceover(
            "How do you read the coefficient? <bookmark mark='a'/> The slope is the change in log-odds for each degree. "
            "<bookmark mark='b'/> So e to the slope is an odds ratio: the factor by which the odds change per degree, the same "
            "at every temperature, though the change in probability isn't. <bookmark mark='c'/> Ten degrees colder, the odds "
            "of distress are multiplied by about ten. <bookmark mark='d'/> With only twenty-three flights the uncertainty is "
            "large: the profile-likelihood interval, which we'll build in chapter four, runs from about two to about a hundred "
            "and seventy. But it excludes one: colder was worse."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def latent(self):
        A = axes([-6, 6], [0, 0.3], x_length=8.0, y_length=3.0, xlabel=r"latent strain $y^*$", ylabel=r"", xticks=[-4, -2, 0, 2, 4],
                 yticks=[], center=[-1.0, 0.8, 0])
        ax = A.ax
        eta = ValueTracker(-1.5)
        xs = np.linspace(-6, 6, 241)

        def dens():
            e = eta.get_value()
            z = xs - e
            f = np.exp(-z) / (1 + np.exp(-z)) ** 2
            grp = VGroup(curve(ax, xs, f, GREY_A, 3))
            right = xs >= 0
            grp.add(shade(ax, xs[right], f[right], EVENT, 0.5))
            return grp

        pic = always_redraw(dens)
        thr = DashedLine(ax.c2p(0, 0), ax.c2p(0, 0.3), color=S.ACCENT, stroke_width=3)
        tl = label(r"failure threshold", font_size=20, color=S.ACCENT).next_to(thr, UP, buff=0.08)
        readout = always_redraw(lambda: MathTex(rf"\eta = {eta.get_value():+.1f}:\ \ P(y^* > 0) = {1 / (1 + np.exp(-eta.get_value())):.2f}",
                                                font_size=30, color=EVENT).move_to([4.6, 1.6, 0]))
        rows = fit_rows(VGroup(
            label(r"imagine a hidden strain on the seal: \ $y^* = \beta_0 + \beta_1 x + \varepsilon$", font_size=24),
            label(r"the seal fails when $y^* > 0$", font_size=24, color=EVENT),
            label(r"logistic noise $\varepsilon$ \ $\Rightarrow$ \ $P(y = 1) = $ the logistic curve", font_size=24, color=OBS),
            label(r"normal noise \ $\Rightarrow$ \ $\Phi(\eta)$: \ the probit model (Bliss 1934)", font_size=24, color=S.ALT),
        ), 12.4, 0.26, [0, -2.2, 0])
        with self.voiceover(
            "A second way to see the model. <bookmark mark='a'/> Imagine a hidden strain on the seal, y star, which is a "
            "straight line in temperature plus random noise. <bookmark mark='b'/> The seal shows distress when the strain "
            "crosses a threshold, zero. <bookmark mark='c'/> If the noise has the logistic distribution, the probability "
            "of crossing is exactly the logistic curve of eta. As the temperature drops, eta rises, the whole distribution "
            "slides right, and more of it lies past the threshold. <bookmark mark='d'/> If the noise is normal instead, the "
            "probability is the normal CDF of eta: the probit model, which Chester Bliss introduced in 1934 for the doses "
            "that kill insects."
        ) as vo:
            self.add(pic)
            self.play(FadeIn(A), Create(thr), FadeIn(tl), FadeIn(readout))
            self.add(readout)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            self.play(eta.animate.set_value(2.5), run_time=4.0)
            self.play(eta.animate.set_value(0.0), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            pic.clear_updaters()
            readout.clear_updaters()
        self.clear_scene()

    def probit(self):
        d = load("latent")
        t = np.asarray(load("challenger")["T"])
        y = np.asarray(load("challenger")["Y"])
        xs = np.asarray(d["xs"])
        A = axes([25, 85], [-0.1, 1.15], x_length=7.4, y_length=4.2, xlabel=r"launch temperature, \ $^\circ$F", ylabel=r"$P(\text{distress})$",
                 xticks=[30, 40, 50, 60, 70, 80], yticks=[0, 0.5, 1], center=[-2.4, 0.2, 0])
        ax = A.ax
        dots = flights(ax, t, y)
        c1 = curve(ax, xs, np.asarray(d["p_logit"]), OBS, 4)
        c2 = DashedVMobject(curve(ax, xs, np.asarray(d["p_probit"]), S.ALT, 4), num_dashes=60)
        rows = fit_rows(VGroup(
            label(r"logit (gold) \ and probit (teal), \ both fitted", font_size=24),
            MathTex(rf"\hat\beta_{{\text{{logit}}}} / \hat\beta_{{\text{{probit}}}} = {d['ratio'][1]:.2f}", font_size=28),
            label(r"the logistic SD is $\pi/\sqrt3 = 1.81$; \ the curves are matched near the middle", font_size=22, color=GREY_A),
            label(r"indistinguishable where the data are", font_size=24, color=OBS),
            MathTex(rf"\text{{at }}31^\circ\text{{F:}}\ \ {load('challenger')['p31']:.4f}\ \text{{vs}}\ {d['probit_31']:.6f}", font_size=26),
            label(r"the tails come from the model, \ not the data", font_size=22, color=RES),
        ), 4.6, 0.32, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fit both models to the flights. <bookmark mark='b'/> The logit coefficients are about one "
            "point seven times the probit ones, <bookmark mark='c'/> because the logistic distribution is more spread out than "
            "the standard normal; its standard deviation is pi over root three. <bookmark mark='d'/> Where the data are, the two "
            "curves are indistinguishable. <bookmark mark='e'/> At thirty-one degrees, both say distress is nearly certain, "
            "but the logit model leaves four chances in ten thousand of no distress, and the probit about two in a million. "
            "<bookmark mark='f'/> That difference comes entirely from the assumed shape of the tail. The data can't "
            "tell the two apart, which is the first warning about extrapolating."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def canonical(self):
        rows = [
            cmath(r"f(y \mid p)", r"=", r"p^y(1 - p)^{1 - y} = \exp\Big\{y\log\frac{p}{1 - p} + \log(1 - p)\Big\}", font_size=30),
            cmath(r"\theta", r"=", r"\log\frac{p}{1 - p}", font_size=34),
            cmath(r"\text{Poisson}", r":", r"\frac{\mu^y e^{-\mu}}{y!} = \exp\{y\log\mu - \mu - \log y!\}\ \Rightarrow\ \theta = \log\mu", font_size=30),
            cmath(r"\text{canonical link}", r":", r"\theta = x^\top\beta \ \Rightarrow\ \text{score } X^\top(y - \mu)", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"the Bernoulli as an exponential family (Part 3)"), why(r"its natural parameter is the logit"),
                why(r"the natural parameter is the log"), why(r"Nelder \& Wedderburn (1972); \ theory in Part 24")]
        with self.voiceover(
            "Why the logit, of all transformations? <bookmark mark='a'/> Write the Bernoulli distribution in Part 3's "
            "exponential-family form. <bookmark mark='b'/> The quantity multiplying y, its natural parameter, is exactly the "
            "log-odds. <bookmark mark='c'/> Do the same for the Poisson, and the natural parameter is the log of the mean, "
            "which is why Poisson regression will use logs. <bookmark mark='d'/> Setting the natural parameter equal to a linear "
            "predictor is called using the canonical link, and it makes the score equations take the simple form X transpose "
            "times y minus the mean. This is the unifying idea of generalized linear models, which Part 24 develops."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
