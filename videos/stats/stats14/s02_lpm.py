from __future__ import annotations

import numpy as np

from videos.stats.stats14.common import *  # noqa: F403


def flights(ax, t, y, stack=0.05, radius=0.08):
    """The flights as dots at 0 (no distress) and 1 (distress), ties stacked."""
    seen = {}
    g = VGroup()
    for a, b in zip(t, y):
        j = seen.get((a, b), 0)
        seen[(a, b)] = j + 1
        g.add(Dot(ax.c2p(a, b + (-stack if b > 0.5 else stack) * j), radius=radius, color=EVENT if b > 0.5 else NOEVENT))
    return g


class LinearProbability(VoiceoverScene):
    def construct(self):
        self.card()
        self.binary()
        self.line()
        self.variance()
        self.economists()
        self.wanted()

    def card(self):
        card = chapter_card(1, r"Why not least squares?", r"A straight line through zeros and ones", part=PART)
        with self.voiceover("Chapter one. Why not least squares?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def binary(self):
        d = load("challenger")
        t, y = np.asarray(d["T"]), np.asarray(d["Y"])
        A = axes([25, 85], [-0.4, 1.9], x_length=8.0, y_length=4.0, xlabel=r"launch temperature, \ $^\circ$F", ylabel=r"distress?",
                 xticks=[30, 40, 50, 60, 70, 80], yticks=[0, 1], center=[-1.6, 0.7, 0])
        ax = A.ax
        dots = flights(ax, t, y)
        rows = fit_rows(VGroup(
            label(r"make the outcome yes or no: \ any O-ring distress", font_size=24),
            label(r"$y = 1$ for 7 flights, \ $y = 0$ for 16", font_size=24, color=EVENT),
            label(r"what we want: \ $P(y = 1 \mid \text{temperature})$", font_size=26, color=OBS),
        ), 12.4, 0.24, [0, -2.85, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Simplify the outcome to yes or no: did any O-ring on the flight show distress? "
            "<bookmark mark='b'/> Seven flights say yes, sixteen say no. Each dot now sits at zero or one, at its launch "
            "temperature. <bookmark mark='c'/> What we want is the probability of distress as a function of temperature, and "
            "especially its value far to the left, at thirty-one degrees."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.6) for d_ in dots], lag_ratio=0.06), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def line(self):
        d = load("challenger")
        t, y = np.asarray(d["T"]), np.asarray(d["Y"])
        a, b = d["lp_coef"]
        A = axes([25, 85], [-0.4, 1.9], x_length=8.0, y_length=4.4, xlabel=r"launch temperature, \ $^\circ$F", ylabel=r"$\hat p$",
                 xticks=[30, 40, 50, 60, 70, 80], yticks=[0, 0.5, 1, 1.5], center=[-2.2, 0.2, 0])
        ax = A.ax
        dots = flights(ax, t, y)
        ln = Line(ax.c2p(29, a + 29 * b), ax.c2p(85, a + 85 * b), color=FIT, stroke_width=4)
        one = DashedLine(ax.c2p(25, 1), ax.c2p(85, 1), color=GREY_C, stroke_width=1.5)
        zero = DashedLine(ax.c2p(25, 0), ax.c2p(85, 0), color=GREY_C, stroke_width=1.5)
        d31 = Dot(ax.c2p(31, a + 31 * b), radius=0.11, color=S.ACCENT)
        d85 = Dot(ax.c2p(85, a + 85 * b), radius=0.11, color=S.ACCENT)
        rows = fit_rows(VGroup(
            label(r"least squares on 0/1: \ the linear probability model", font_size=22),
            MathTex(rf"\hat p = {a:.2f} - {abs(b):.4f}\,T", font_size=30, color=FIT),
            MathTex(rf"\hat p(31) = {d['lp_31']:.2f}", font_size=30, color=RES),
            MathTex(rf"\hat p(85) = {d['lp_85']:.2f}", font_size=30, color=RES),
            label(r"probabilities above one and below zero", font_size=22, color=RES),
        ), 4.4, 0.36, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The obvious first try is Part 12's least squares, with the zeros and ones as the response. "
            "It's called the linear probability model. <bookmark mark='b'/> The fitted line falls by about four percentage "
            "points per degree. <bookmark mark='c'/> At thirty-one degrees it predicts a probability of one point seven five. "
            "<bookmark mark='d'/> At eighty-five, minus point two seven. <bookmark mark='e'/> A straight line can't respect the "
            "fact that probabilities live between zero and one. Near the middle of the data it's a fair summary; at the "
            "temperature that mattered, it's nonsense."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots), Create(one), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(d31, scale=2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(d85, scale=2), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def variance(self):
        rows = [
            cmath(r"y \mid x", r"\sim", r"\text{Bernoulli}(p(x))", font_size=34),
            cmath(r"\mathrm{Var}(y \mid x)", r"=", r"p(x)\,\big(1 - p(x)\big)", font_size=34),
            cmath(r"\text{residual}", r"\in", r"\{-\hat p(x),\ 1 - \hat p(x)\}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{heteroskedasticity, nonnormality, extrapolation}", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        rows[3][2].set_color(RES)
        whys = [why(r"a yes/no outcome"), why(r"the variance is tied to the mean"),
                why(r"only two values at each $x$"), why(r"normal-theory inference and global probability predictions need care")]
        intro = label('Binary outcomes have mean-dependent variance', font_size=36)
        with self.voiceover(
            "There are deeper problems too. <bookmark mark='a'/> A yes-or-no outcome is a Bernoulli variable, with probability "
            "p of x. <bookmark mark='b'/> Its variance is p times one minus p: tied to the mean, so it changes with x, largest "
            "at a half and vanishing near zero and one. <bookmark mark='c'/> The residuals at each x take only two values. "
            "<bookmark mark='d'/> When p varies, Bernoulli variance generally varies too; it can coincide at symmetric probabilities. The errors are nonnormal and unconstrained linear predictions can leave zero to one. The sandwich "
            "standard errors of Part 12 can patch the first problem, and economists still use the linear probability model "
            "for its simple coefficients. But for prediction, and especially for extrapolation, we need a different curve."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def wanted(self):
        xs = np.linspace(-6, 6, 241)
        A = axes([-6, 6], [0, 1], x_length=7.0, y_length=3.8, xlabel=r"$\eta = \beta_0 + \beta_1 x$", ylabel=r"$p$",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.5, 1], center=[-2.2, 0.0, 0])
        ax = A.ax
        cv = curve(ax, xs, 1 / (1 + np.exp(-xs)), OBS, 4)
        ln = Line(ax.c2p(-2, 0), ax.c2p(2, 1), color=FIT, stroke_width=2).set_opacity(0.6)
        rows = fit_rows(VGroup(
            label(r"wanted: \ a curve from 0 to 1", font_size=24),
            label(r"steep in the middle, \ flat at the ends", font_size=24),
            label(r"linear in $x$ on some transformed scale", font_size=24, color=OBS),
            MathTex(r"p = \frac{e^{\eta}}{1 + e^{\eta}}", font_size=36, color=OBS),
            label(r"the logistic curve", font_size=22, color=GREY_A),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What we want is a curve that runs from zero to one, <bookmark mark='b'/> rising steeply in "
            "the middle and flattening at both ends, where a probability can't go further. <bookmark mark='c'/> And to keep "
            "the convenience of regression, we'd like the curve to be linear in x on some transformed scale. "
            "<bookmark mark='d'/> The most popular answer is the logistic curve, e to the eta over one plus e to the eta. "
            "<bookmark mark='e'/> It was introduced by Pierre-François Verhulst in the 1840s, to describe population growth."
        ) as vo:
            self.play(FadeIn(A), Create(ln))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def economists(self):
        rows = [
            cmath(r"\hat p", r"=", r"\hat\beta_0 + \hat\beta_1 x", font_size=34),
            cmath(r"\hat\beta_1", r"=", r"\text{change in the fitted linear probability per unit of } x", font_size=32),
            cmath(r"\mathrm{SE}", r":", r"\text{HC3 sandwich (Part 12)}", font_size=32),
            cmath(r"\text{fine for}", r":", r"\text{average effects in the middle; \ not for } \hat p(31)", font_size=32),
        ]
        whys = [why(r"the linear probability model"), why(r"easy to read, \ the same at every $x$"),
                why(r"the heteroskedasticity is known, \ so fix it"), why(r"a summary, \ not a forecast")]
        intro = label('A linear probability model needs careful inference', font_size=36)
        with self.voiceover(
            "In fairness to the straight line: <bookmark mark='a'/> economists use the linear probability model all the time. "
            "<bookmark mark='b'/> Its coefficient is a change in the fitted linear probability per unit of x, easy to read and the same "
            "everywhere. <bookmark mark='c'/> The heteroskedasticity is known, so it can be handled with Part 12's sandwich "
            "standard errors. <bookmark mark='d'/> As a descriptive linear projection over a restricted range, the line "
            "is often close to the logistic curve's slope there. Its probability forecasts can fail badly at the edges, which "
            "is exactly where Challenger's question lay."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()
