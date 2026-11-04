from __future__ import annotations

import numpy as np
from scipy import special, stats

from videos.stats.stats14.common import *  # noqa: F403


class Fitting(VoiceoverScene):
    def construct(self):
        self.card()
        self.likelihood()
        self.surface()
        self.newton()
        self.irls_path()
        self.deviance()

    def card(self):
        card = chapter_card(3, r"Fitting by maximum likelihood", r"Newton's method, \ dressed as weighted least squares", lit=(1922,), part=PART)
        with self.voiceover("Chapter three. Fitting by maximum likelihood."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def likelihood(self):
        rows = [
            cmath(r"L(\beta)", r"=", r"\prod_i p_i^{\,y_i}(1 - p_i)^{1 - y_i}", font_size=34),
            cmath(r"\ell(\beta)", r"=", r"\sum_i \big[y_i\,\eta_i - \log(1 + e^{\eta_i})\big]", font_size=34),
            cmath(r"\nabla \ell", r"=", r"X^\top(y - p) = 0", font_size=34),
            cmath(r"-\nabla^2 \ell", r"=", r"X^\top W X,\qquad W = \mathrm{diag}\big(p_i(1 - p_i)\big)", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"Part 9: \ the probability of the data"), why(r"$\eta_i = x_i^\top\beta$: \ concave in $\beta$"),
                why(r"the score: \ residuals orthogonal to the columns, \ as in Part 12"), why(r"the information: \ Part 9's Fisher information")]
        with self.voiceover(
            "There's no formula for the logistic coefficients. They come from Part 9's maximum likelihood. <bookmark mark='a'/> "
            "The likelihood is the product, over flights, of p for the flights with distress and one minus p for the others. "
            "<bookmark mark='b'/> Its logarithm simplifies to a sum of y times eta minus log of one plus e to the eta, a "
            "concave function of the coefficients, so it has a single maximum. <bookmark mark='c'/> At the maximum the score "
            "is zero: X transpose times the residuals, y minus p, vanishes. That's Part 12's normal equations, with the "
            "fitted probabilities in place of fitted values. But p depends on beta nonlinearly, so we can't solve it in one "
            "step. <bookmark mark='d'/> The curvature is X transpose W X, with weights p times one minus p: the Fisher "
            "information, whose inverse gives the standard errors."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def surface(self):
        d = load("challenger")
        T, Y = np.asarray(d["T"]), np.asarray(d["Y"])
        b0h, b1h = d["coef"]
        A = axes([-2, 30], [-0.5, 0.05], x_length=6.4, y_length=4.6, xlabel=r"$\beta_0$", ylabel=r"$\beta_1$", xticks=[0, 10, 20, 30],
                 yticks=[-0.4, -0.2, 0], center=[-2.4, -0.1, 0])
        ax = A.ax
        n = 46
        b0s = np.linspace(-2, 30, n + 1)
        b1s = np.linspace(-0.5, 0.05, n + 1)
        cells = VGroup()
        for i in range(n):
            for j in range(n):
                a, b = (b0s[i] + b0s[i + 1]) / 2, (b1s[j] + b1s[j + 1]) / 2
                eta = a + b * T
                ll = float(np.sum(Y * eta - np.log1p(np.exp(eta))))
                tval = float(np.clip((ll + 25) / 15, 0, 1))
                p0, p1 = ax.c2p(b0s[i], b1s[j]), ax.c2p(b0s[i + 1], b1s[j + 1])
                cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0,
                                    fill_color=interpolate_color(ManimColor("#14202B"), ManimColor(S.LIK), tval ** 2), fill_opacity=1).move_to((p0 + p1) / 2))
        top = Star(n=5, outer_radius=0.15, color=OBS, fill_opacity=1).move_to(ax.c2p(b0h, b1h))
        rows = fit_rows(VGroup(
            label(r"the log-likelihood over $(\beta_0, \beta_1)$", font_size=24),
            label(r"one ridge, \ one peak", font_size=24, color=S.LIK),
            label(r"the ridge: \ $\beta_0$ and $\beta_1$ trade off, \ since $T$ is far from 0", font_size=22),
            MathTex(rf"\hat\beta = ({b0h:.2f},\ {b1h:.3f})", font_size=30, color=OBS),
        ), 4.8, 0.38, [4.4, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is the log-likelihood as a landscape over the two coefficients, brighter where it's "
            "higher. <bookmark mark='b'/> It has one long ridge and a single peak. <bookmark mark='c'/> The ridge is "
            "diagonal because the temperatures are all far from zero: a bigger intercept can be traded for a steeper slope "
            "with almost the same fit. Centring temperature would round it out. <bookmark mark='d'/> The peak, the maximum "
            "likelihood estimate, is at fifteen point oh four and minus point two three two. How do we climb to it?"
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(top, scale=2), FadeIn(rows[3]))
        self.clear_scene()

    def newton(self):
        rows = [
            cmath(r"\beta^{(t+1)}", r"=", r"\beta^{(t)} + (X^\top W X)^{-1} X^\top (y - p)", font_size=32),
            cmath(r"z", r"=", r"X\beta^{(t)} + W^{-1}(y - p)", font_size=34),
            cmath(r"\beta^{(t+1)}", r"=", r"(X^\top W X)^{-1} X^\top W z", font_size=34),
            cmath(r"\text{iterate}", r":", r"\text{recompute } p,\ W,\ z;\ \text{refit}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"Newton's step: \ gradient over curvature"), why(r"the working response: \ a linearized $y$"),
                why(r"a weighted least squares fit! \ (Part 12)"), why(r"iteratively reweighted least squares (IRLS)")]
        with self.voiceover(
            "<bookmark mark='a'/> Use Newton's method: step by the gradient divided by the curvature. <bookmark mark='b'/> "
            "Now a little algebra. Define a working response z: the current linear predictor, plus the residuals divided by "
            "the weights. It's what y looks like on the log-odds scale, to first order. <bookmark mark='c'/> Then the Newton "
            "step is exactly a weighted least squares regression of z on X, with weights W: Part 12's machinery, reused. "
            "<bookmark mark='d'/> Recompute the probabilities, the weights and the working response, and fit again. "
            "Iteratively reweighted least squares, the algorithm inside every generalized linear model program since John "
            "Nelder and Robert Wedderburn's 1972 paper. Part 24 develops the theory."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def irls_path(self):
        d = load("challenger")
        T, Y = np.asarray(d["T"]), np.asarray(d["Y"])
        path = np.asarray(d["path"])
        ll = np.asarray(d["ll_path"])
        A = axes([25, 85], [-0.1, 1.15], x_length=6.0, y_length=3.8, xlabel=r"temperature, \ $^\circ$F", ylabel=r"$p$",
                 xticks=[30, 50, 70], yticks=[0, 0.5, 1], center=[-3.4, 0.5, 0])
        ax = A.ax
        xs = np.linspace(25, 85, 200)
        from videos.stats.stats14.s02_lpm import flights
        dots = flights(ax, T, Y, radius=0.06)
        tab = VGroup()
        head = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"step", r"$\beta_0$", r"$\beta_1$", r"$\ell$")])
        xs_col = [1.4, 2.8, 4.3, 5.8]
        for t, x in zip(head, xs_col):
            t.move_to([x, 2.6, 0])
        tab.add(head)
        lines = []
        for k in range(min(7, len(path))):
            r = VGroup(label(rf"{k}", font_size=22), label(rf"{path[k][0]:.3f}", font_size=22), label(rf"{path[k][1]:.4f}", font_size=22),
                       label(rf"{ll[k]:.3f}", font_size=22, color=S.LIK))
            for t, x in zip(r, xs_col):
                t.move_to([x, 2.0 - 0.5 * k, 0])
            lines.append(r)
        cur = curve(ax, xs, special.expit(path[0][0] + path[0][1] * xs), OBS, 4)
        foot = label(r"each step: \ one weighted least squares fit; \ the log-likelihood never falls", font_size=22, color=GREY_A).move_to([0, -3.1, 0])
        with self.voiceover(
            "Watch it work on the flights. <bookmark mark='a'/> Start from zero: every flight gets probability one half, a flat "
            "line. The log-likelihood is minus fifteen point nine. <bookmark mark='b'/> One weighted regression later, the curve "
            "already tilts the right way, and the log-likelihood jumps to minus ten point six. <bookmark mark='c'/> The next "
            "steps refine it: minus ten point one eight, minus ten point one five eight. <bookmark mark='d'/> By the fifth step "
            "the coefficients are fixed to five decimals, and they stop changing. Newton's method converges quadratically: "
            "near the answer, each step roughly doubles the number of correct digits."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(cur), FadeIn(lines[0]))
            for k, m_ in zip(range(1, 7), ["b", "c", None, "d", None, None]):
                if m_:
                    vo.wait_until(m_)
                new = curve(ax, xs, special.expit(path[k][0] + path[k][1] * xs), OBS, 4)
                self.play(Transform(cur, new), FadeIn(lines[k]), run_time=1.0)
            self.play(FadeIn(foot))
        self.clear_scene()

    def deviance(self):
        d = load("challenger")
        z = d["coef"][1] / d["se"][1]
        rows = [
            cmath(r"D", r"=", rf"-2\,\ell(\hat\beta) = {d['deviance']:.2f}\ \ \text{{(21 df)}}", font_size=32),
            cmath(r"D_0", r"=", rf"{d['null_dev']:.2f}\ \ \text{{(intercept only, 22 df)}}", font_size=32),
            cmath(r"D_0 - D", r"=", rf"{d['lr']:.2f}\ \sim\ \chi^2_1:\ \ p = {d['lr_p']:.4f}", font_size=32),
            cmath(r"\text{Wald}", r":", rf"z = {d['coef'][1]:.3f}/{d['se'][1]:.3f} = {z:.2f},\ \ p = {2 * stats.norm.sf(abs(z)):.3f}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the deviance: \ for 0/1 data, \ minus twice the log-likelihood"), why(r"a model with no temperature"),
                why(r"Part 10's likelihood-ratio test"), why(r"the coefficient over its SE: \ cruder")]
        with self.voiceover(
            "How good is the fit, and does temperature matter? <bookmark mark='a'/> The deviance, which for zero-one data is "
            "minus twice the maximized log-likelihood, is twenty point three. <bookmark mark='b'/> A model with no temperature "
            "at all, the same probability for every flight, has deviance twenty-eight point three. <bookmark mark='c'/> The "
            "drop, seven point nine five, is Part 10's likelihood-ratio statistic, approximately chi-squared with one degree of "
            "freedom: p of point zero zero five. <bookmark mark='d'/> The Wald test, the coefficient divided by its standard "
            "error, gives z of minus two point one four, p of point zero three: the same conclusion, less sharply, because "
            "the Wald test leans on a quadratic approximation that's poor with twenty-three flights. Deviances are to "
            "generalized linear models what sums of squares are to least squares."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
