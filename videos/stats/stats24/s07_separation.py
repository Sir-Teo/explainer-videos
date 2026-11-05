from __future__ import annotations

import numpy as np
from scipy import special

from videos.stats.stats24.common import *  # noqa: F403


class Separation(VoiceoverScene):
    def construct(self):
        self.card()
        self.picture()
        self.runaway()
        self.why_()
        self.firth()
        self.rare()
        self.practice()

    def card(self):
        card = chapter_card(6, r"Separation", r"When the likelihood has no top", lit=(1984, 1993), part=PART)
        with self.voiceover("Chapter six. Separation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def picture(self):
        d = load("separation")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        A = axes([-2.5, 2.5], [-0.1, 1.1], x_length=8.0, y_length=4.2, xlabel=r"$x$", ylabel=r"$y$",
                 xticks=[-2, -1, 0, 1, 2], yticks=[0, 1], center=[-1.6, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=RES if b else BLUE) for a, b in zip(x, y)])
        gap = DashedLine(ax.c2p(0.1, -0.1), ax.c2p(0.1, 1.1), color=PATH, stroke_width=2.5)
        gr = np.linspace(-2.5, 2.5, 200)
        curves = VGroup(*[curve(ax, gr, special.expit(b * (gr - 0.1)), interpolate_color(ManimColor(GREY_B), ManimColor(MODEL), k / 3), 3)
                          for k, b in enumerate((2, 6, 20, 80))])
        rows = fit_rows(VGroup(
            label(r"12 points: \ every $x < 0$ is a 0, \ every $x > 0$ a 1", font_size=22),
            label(r"a line separates them perfectly", font_size=22, color=PATH),
            label(r"steeper curves fit better, \ forever", font_size=22, color=MODEL),
            label(r"the MLE of the slope: \ $+\infty$", font_size=22, color=RES),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Twelve observations. Every one with x below zero is a zero, and every one above is a one. "
            "<bookmark mark='b'/> A vertical line separates the two outcomes perfectly. <bookmark mark='c'/> A logistic curve "
            "fits better the steeper it gets: each steeper curve gives every point a probability closer to its outcome. "
            "<bookmark mark='d'/> There is no best curve. The maximum likelihood estimate of the slope is infinite."
        ) as vo:
            self.play(FadeIn(A), LaggedStart(*[FadeIn(q, scale=0.5) for q in dots], lag_ratio=0.08))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(gap), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.5), FadeIn(rows[2]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def runaway(self):
        d = load("separation")
        s = np.asarray(d["slopes"])
        ll = np.asarray(d["loglik"])
        it = np.arange(1, len(s) + 1)
        A = axes([0, 25], [0, 120], x_length=6.0, y_length=4.2, xlabel=r"IRLS step", ylabel=r"slope",
                 xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 40, 80, 120], center=[-3.0, 0.3, 0])
        ax = A.ax
        pl = polyline(ax, it, s, MODEL, 3.5)
        B = axes([0, 25], [-3.5, 0.2], x_length=4.4, y_length=2.4, xlabel=r"step", ylabel=r"log likelihood",
                 xticks=[0, 10, 20], yticks=[-3, -2, -1, 0], center=[3.9, 1.4, 0], font_size=16)
        pl2 = polyline(B.ax, it, ll, PATH, 3)
        rows = fit_rows(VGroup(
            label(rf"slope after 25 steps: \ {s[-1]:.0f}, \ and climbing by 5 a step", font_size=22, color=MODEL),
            label(r"log likelihood: \ $\to 0$, \ never reaching it", font_size=22, color=PATH),
            label(r"software: \ ``fitted probabilities 0 or 1 occurred''", font_size=20, color=GREY_A),
            label(r"the reported SE: \ huge; \ the Wald test: \ useless", font_size=22, color=RES),
        ), 5.0, 0.35, [3.6, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Run IRLS anyway. The slope grows by five every step, a hundred and eight after "
            "twenty-five steps, and would keep going. <bookmark mark='b'/> The log likelihood creeps up towards zero, its "
            "ceiling, without reaching it. <bookmark mark='c'/> Software stops at its iteration limit and prints a warning "
            "that fitted probabilities of zero or one occurred. <bookmark mark='d'/> The standard error it reports is "
            "enormous, so the Wald test, Part 22's Hauck–Donner effect at its extreme, says the strongest possible effect is "
            "not significant."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(Create(pl), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(pl2), FadeIn(rows[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def why_(self):
        rows = [
            cmath(r"\text{complete separation}", r":", r"\exists\, b: \ x_i^\top b > 0 \iff y_i = 1", font_size=30),
            cmath(r"\ell(cb)", r"\uparrow", r"0 \ \text{as } c \to \infty", font_size=30),
            cmath(r"\text{quasi-complete}", r":", r"\text{separation with ties on the boundary}", font_size=30),
            cmath(r"\text{when}", r":", r"\text{small } n, \ \text{rare outcomes, \ many predictors, \ sparse categories}", font_size=28),
        ]
        rows[1][2].set_color(RES)
        whys = [why(r"Albert \& Anderson (1984)"), why(r"every probability tends to its outcome"),
                why(r"some coefficients still run away"), why(r"more common than one might hope")]
        with self.voiceover(
            "<bookmark mark='a'/> Adelin Albert and John Anderson characterized it in 1984. Complete separation means some "
            "direction in coefficient space puts every one on one side and every zero on the other. <bookmark mark='b'/> "
            "Scaling that direction up sends every fitted probability towards its own outcome, and the log likelihood up "
            "towards zero. <bookmark mark='c'/> Quasi-complete separation, with some ties on the boundary, sends just some "
            "coefficients to infinity. <bookmark mark='d'/> It happens far more often than one might hope: small samples, "
            "rare outcomes, many predictors, or a category in which everyone responded."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def firth(self):
        d = load("separation")
        rows = [
            cmath(r"\ell^*(\beta)", r"=", r"\ell(\beta) + \tfrac12 \log\det \mathcal I(\beta)", font_size=30),
            cmath(r"U^*", r"=", r"X^\top\big(y - p + h(\tfrac12 - p)\big)", font_size=30),
            cmath(r"\text{our data}", r":", rf"\hat\beta_1^{{\text{{Firth}}}} = {d['firth'][1]:.2f} \ \ (\mathrm{{SE}} \ {d['firth_se'][1]:.2f})", font_size=30),
            cmath(r"\text{bonus}", r":", r"O(1/n) \ \text{bias removed}", font_size=30),
        ]
        rows[0][2].set_color(HIT)
        whys = [why(r"Firth (1993): \ Jeffreys's prior as a penalty"), why(r"$h$: \ the hat values; \ half an observation each way"),
                why(r"finite, \ and sensible"), why(r"why it was invented")]
        with self.voiceover(
            "<bookmark mark='a'/> David Firth's cure, from 1993, adds half the log determinant of the information to the log "
            "likelihood. That's the logarithm of Jeffreys's prior from Part 22, used as a penalty. <bookmark mark='b'/> In "
            "the score equations it amounts to adding, for each observation, a fraction of a pseudo-observation split "
            "between the two outcomes, so no probability can be pushed all the way to zero or one. "
            "<bookmark mark='c'/> For our twelve points the slope is now finite, two point five five. "
            "<bookmark mark='d'/> Firth designed it to remove the leading term of the bias of maximum likelihood, which it "
            "also does when there is no separation; that it tames separation was a happy bonus."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rare(self):
        rows = [
            cmath(r"\text{rare events}", r":", r"\text{few 1s: \ MLE biased away from zero}", font_size=30),
            cmath(r"\text{bias}", r"\approx", r"O(1/(\text{number of events})), \ \text{not } O(1/n)", font_size=30),
            cmath(r"\text{case--control}", r":", r"\text{sample the 1s heavily; \ slopes still valid}", font_size=30),
            cmath(r"\text{intercept}", r":", r"\text{shift by } \log\{\text{sampling ratio}\}", font_size=30),
        ]
        rows[1][-1].set_color(RES)
        whys = [why(r"King \& Zeng (2001): \ wars, \ coups"), why(r"events, \ not people, \ set the precision"),
                why(r"Prentice \& Pyke (1979)"), why(r"only the constant knows the sampling")]
        with self.voiceover(
            "<bookmark mark='a'/> A milder relative of separation is rarity. With few ones, maximum likelihood "
            "overstates effects, as Gary King and Langche Zeng showed for rare political events. <bookmark mark='b'/> The "
            "bias shrinks with the number of events, not the number of observations: a million people with fifty cases "
            "is a small sample. Firth's correction helps here too. <bookmark mark='c'/> The flip side: for rare outcomes you "
            "can sample the cases heavily, a case–control design, and logistic slopes remain valid, as Ross Prentice and "
            "Ronald Pyke proved. <bookmark mark='d'/> Only the intercept changes, by the log of the sampling ratio."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def practice(self):
        d = load("separation")
        rows = fit_rows(VGroup(
            label(r"swap two points across the line, \ and the MLE exists:", font_size=24),
            label(rf"slope {d['overlap'][1]:.2f}, \ SE {d['overlap_se'][1]:.2f}", font_size=24, color=MODEL),
            label(r"under separation: \ Firth, \ profile-likelihood or exact intervals", font_size=24, color=HIT),
            label(r"or a weakly informative prior: \ Part 26", font_size=24, color=TEAL),
            label(r"never: \ drop the variable because its SE is huge", font_size=24, color=RES),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Separation is fragile. Move just two of the twelve points across the line <bookmark mark='b'/> "
            "and the maximum likelihood estimate exists, a slope of three point four five with a sizeable standard error. "
            "<bookmark mark='c'/> When it does happen, use Firth's estimate, profile-likelihood intervals, which are "
            "one-sided but informative, or exact conditional methods. <bookmark mark='d'/> A weakly informative prior, Part "
            "26, works too. <bookmark mark='e'/> What not to do is drop the variable because its standard error looked huge: "
            "it is the strongest predictor in the data."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
