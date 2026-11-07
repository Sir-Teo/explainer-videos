from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats19.common import *  # noqa: F403


class CrossValidation(VoiceoverScene):
    def construct(self):
        self.card()
        self.recap()
        self.curve()
        self.one_se()
        self.honest()
        self.board()
        self.loo()

    def card(self):
        card = chapter_card(3, r"Cross-validation", r"Estimating the U from one training set", part=PART)
        with self.voiceover("Chapter three. Cross-validation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def recap(self):
        rows = [
            cmath(r"\text{split the data into } K \text{ folds}", r":", r"\text{fit on } K - 1,\ \text{predict the one left out}", font_size=28),
            cmath(r"\text{CV}(\theta)", r"=", r"\tfrac1n \textstyle\sum_i L\big(y_i, \hat f^{(-k(i))}_\theta(x_i)\big)", font_size=30),
            cmath(r"\mathrm{SE}", r"=", r"\text{SD of the } K \text{ fold errors} / \sqrt K", font_size=30),
            cmath(r"\text{choose}", r":", r"\theta \text{ minimizing CV: \ the tuning parameter}", font_size=30),
        ]
        rows[3][2].set_color(CVC)
        whys = [why(r"Part 16, \ chapter ten"), why(r"for each setting $\theta$ of the dial"), why(r"a rough measure of its noise"),
                why(r"$k$ for neighbours, \ degree for polynomials, \ $\lambda$ for the lasso")]
        intro = label('Repeat the full fitting procedure inside each fold', font_size=36)
        with self.voiceover(
            "Part 16 introduced cross-validation; here it does its main job. <bookmark mark='a'/> Split the data into K folds; "
            "fit on all but one and predict the one left out, in turn. <bookmark mark='b'/> Do that for every setting of the "
            "dial, theta, and average the prediction losses. <bookmark mark='c'/> The spread of the K fold errors gives a rough "
            "standard error. <bookmark mark='d'/> Then choose the setting with the smallest cross-validated error. That's how "
            "nearly every tuning parameter in machine learning is chosen."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def curve(self):
        d = load("cv")
        ks = np.asarray(d["ks"], float)
        cv, se, te = np.asarray(d["cv"]), np.asarray(d["se"]), np.asarray(d["test"])
        A = axes([0, 41], [0.08, 0.3], x_length=8.6, y_length=4.4, xlabel=r"$k$", ylabel=r"mean squared error",
                 xticks=[1, 10, 20, 30, 40], yticks=[0.1, 0.15, 0.2, 0.25, 0.3], center=[-1.4, 0.3, 0])
        ax = A.ax
        bars = VGroup(*[Line(ax.c2p(k, max(0.08, m - s)), ax.c2p(k, min(0.3, m + s)), color=CVC, stroke_width=1.8, stroke_opacity=0.6)
                        for k, m, s in zip(ks, cv, se)])
        ccv = polyline(ax, ks, cv, CVC, 3.5)
        cte = polyline(ax, ks, te, TEST, 3)
        rows = fit_rows(VGroup(
            label(r"one training set of 100", font_size=22),
            label(r"blue: \ 10-fold CV, \ $\pm 1$ SE", font_size=22, color=CVC),
            label(r"red: \ test error on 4,000 new cases \ (4,000 new points)", font_size=22, color=TEST),
            MathTex(rf"\text{{CV's choice}}: k = {d['best_k']}", font_size=26, color=CVC),
            MathTex(rf"\text{{the truth's}}: k = {d['test_argmin']}", font_size=26, color=TEST),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's cross-validation choosing k for nearest neighbours, from a single training set of a "
            "hundred. <bookmark mark='b'/> The ten-fold CV error, with bars of one standard error, has the U shape: high for k "
            "equal to one, falling, then rising as the rule gets too stiff. <bookmark mark='c'/> Because this is a simulation, we "
            "can also draw test error on 4,000 new cases of each rule, on four thousand new points. CV tracks it well. "
            "<bookmark mark='d'/> CV's minimum is at k equals eight. <bookmark mark='e'/> The truth's is at seven. From a single "
            "training set of a hundred, cross-validation found nearly the best rule."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ccv), FadeIn(bars), FadeIn(rows[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(cte), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def one_se(self):
        d = load("cv")
        rows = [
            cmath(r"\text{the CV curve is noisy}", r":", r"\text{its minimum is uncertain}", font_size=30),
            cmath(r"\text{one-SE rule}", r":", r"\text{the simplest model within 1 SE of the minimum}", font_size=30),
            cmath(r"\text{here}", r":", rf"k = {d['one_se_k']}\ \text{{instead of}}\ {d['best_k']}", font_size=30),
            cmath(r"\text{true test errors}", r":", rf"{d['test_one_se']:.3f}\ \text{{vs}}\ {d['test_best']:.3f}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"its SE bars overlap widely"), why(r"Breiman, \ Friedman, \ Olshen \& Stone (1984)"),
                why(r"$k$ larger means simpler, \ smoother"), why(r"this time, \ the rule cost accuracy")]
        intro = label('The one-SE rule trades observed fit for simplicity', font_size=36)
        with self.voiceover(
            "<bookmark mark='a'/> But the CV curve is itself noisy, and near its bottom it's nearly flat, so its minimum is "
            "uncertain. <bookmark mark='b'/> A common convention, from the authors of the CART book in 1984, is the one-"
            "standard-error rule: choose the simplest model whose CV error is within one standard error of the minimum. "
            "<bookmark mark='c'/> Here that's k equals seventeen, a smoother rule than CV's choice of eight. "
            "<bookmark mark='d'/> And here it costs accuracy: test error on 4,000 new casess are point one four one against point one "
            "one nine. The rule protects against chasing noise in the CV curve, and buys simplicity; it doesn't promise a "
            "lower error, and on any one dataset it can be worse."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def honest(self):
        rows = [
            cmath(r"\text{CV estimates}", r":", r"\text{the error of the procedure, \ averaged over training sets}", font_size=28),
            cmath(r"\text{distinguish}", r":", r"\text{average procedure risk and a particular full-data fit}", font_size=28),
            cmath(r"\text{the fold SE}", r":", r"\text{ignores that folds share data}", font_size=28),
            cmath(r"\text{so}", r":", r"\text{CV} \pm 2\,\text{SE can be too narrow}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"Bates, \ Hastie \& Tibshirani (2023)"), why(r"a subtle but real difference"),
                why(r"the $K$ fold errors are correlated"), why(r"the Board checks it")]
        intro = label('Distinguish average procedure risk from a particular fit', font_size=36)
        with self.voiceover(
            "What exactly does cross-validation estimate? <bookmark mark='a'/> Stephen Bates, Trevor Hastie and "
            "Robert Tibshirani studied the difference between average procedure risk and the conditional risk of a "
            "particular fit. Their exact independence result concerns homoskedastic Gaussian least squares, not every"
            " learner. In general, K-fold CV evaluates fits trained on only K minus one folds, <bookmark mark='b'/> "
            "so its target also differs from a rule trained on the entire observed sample. <bookmark mark='c'/> And "
            "the usual standard error, the spread of the fold errors, treats the folds as independent, though they "
            "share most of their training data. <bookmark mark='d'/> Ignoring that dependence can make CV intervals "
            "too narrow, as the next simulation checks."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=19) if r.part == 19]
        b = coverage_board(rows, lit_part=19, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> The Board: two thousand training sets of a hundred, each with ten-fold CV and an "
            "interval of plus or minus one point nine six fold standard errors, checked against test error on 4,000 "
            "new cases of the rule fitted to that training set. Coverage ninety point one five percent against the "
            "exact population risk: broken, modestly. Bates and colleagues propose a specialized nested procedure to "
            "estimate uncertainty, with improved coverage in their examples. Ordinary nested tuning, discussed later,"
            " is a different use of an outer loop and is not an automatic confidence-interval repair."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
        self.wait(1.0)
        self.clear_scene()

    def loo(self):
        rows = fit_rows(VGroup(
            label(r"$K = n$: \ leave-one-out; \ nearly unbiased, \ variable, \ cheap for linear smoothers", font_size=24),
            label(r"$K = 5$ or $10$: \ the usual choice", font_size=24, color=CVC),
            label(r"folds must respect the structure: \ blocks of time (Part 17), \ whole clusters (Part 18)", font_size=24, color=RES),
            label(r"every choice made with the data goes inside the loop: \ chapter ten", font_size=24, color=OBS),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With one fold per observation, cross-validation is leave-one-out: often with small "
            "training-size bias, with variance that depends on the learner, and for linear smoothers computable from "
            "a single fit, as Part 16 showed. <bookmark mark='b'/> Five or ten folds are the usual compromise. "
            "<bookmark mark='c'/> The folds must respect the data's structure: blocks of time, as in Part 17's "
            "rolling origins; whole clusters, as in Part 18's towns. <bookmark mark='d'/> And every choice made with "
            "the data, including which variables to use, has to be repeated inside each fold, or the estimate leaks. "
            "Chapter ten shows how badly."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
