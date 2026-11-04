from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


class Calculus(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.logdet()
        self.hessian()
        self.mle()
        self.information()

    def card(self):
        card = chapter_card(10, r"Matrix calculus", r"Derivatives with respect to vectors and matrices", lit=(), part=PART)
        with self.voiceover("Chapter ten. Matrix calculus."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def rules(self):
        rows = [
            cmath(r"\frac{\partial}{\partial \mathbf x}\, \mathbf a^\top \mathbf x", r"=", r"\mathbf a", font_size=34),
            cmath(r"\frac{\partial}{\partial \mathbf x}\, \mathbf x^\top A \mathbf x", r"=", r"(A + A^\top)\,\mathbf x", r"=",
                  r"2A\mathbf x", r"\ \ (A \text{ symmetric})", font_size=32),
            cmath(r"\frac{\partial}{\partial \boldsymbol\beta}\, \|\mathbf y - X\boldsymbol\beta\|^2", r"=",
                  r"-2X^\top(\mathbf y - X\boldsymbol\beta)", font_size=32),
            cmath(r"\hat{\boldsymbol\beta}", r"=", r"(X^\top X)^{-1}X^\top \mathbf y", font_size=36),
        ]
        rows[3][0].set_color(FIT)
        whys = [why(r"$\sum_i a_i x_i$, \ term by term"), why(r"product rule on $\sum_{ij} x_i A_{ij} x_j$"),
                why(r"chain rule"), why(r"set to zero: \ chapter 2's normal equations")]
        with self.voiceover(
            "Statistics optimizes over vectors and matrices, so it needs their derivatives. "
            "<bookmark mark='a'/> The gradient of a linear function a transpose x is a, term by term. "
            "<bookmark mark='b'/> The gradient of a quadratic form x transpose A x is A plus A transpose times x, or "
            "two A x when A is symmetric: the matrix version of the derivative of a x squared. "
            "<bookmark mark='c'/> Apply both to the least-squares criterion, the squared length of y minus X beta. "
            "<bookmark mark='d'/> Set the gradient to zero, and the normal equations of chapter two fall out in "
            "three lines."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.55, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=False)
        self.clear_scene()

    def logdet(self):
        rows = [
            cmath(r"\log\det(\Sigma + \epsilon E)", r"=", r"\log\det\Sigma + \log\det(I + \epsilon\, \Sigma^{-1}E)", font_size=32),
            cmath(r"\log\det(\Sigma + \epsilon E)", r"=", r"\log\det\Sigma + \epsilon\operatorname{tr}(\Sigma^{-1}E) + O(\epsilon^2)",
                  font_size=32),
            cmath(r"\frac{\partial}{\partial \Sigma}\log\det\Sigma", r"=", r"\Sigma^{-1}", font_size=38),
            cmath(r"\frac{\partial}{\partial \Sigma}\operatorname{tr}(\Sigma^{-1}S)", r"=", r"-\Sigma^{-1} S\, \Sigma^{-1}",
                  font_size=34),
        ]
        rows[2][2].set_color(EIG)
        whys = [why(r"factor out $\Sigma$"), why(r"$\det(I + \epsilon E') = 1 + \epsilon \operatorname{tr} E' + \dots$"),
                why(r"read off the linear term"), why(r"$d(\Sigma^{-1}) = -\Sigma^{-1}(d\Sigma)\Sigma^{-1}$")]
        with self.voiceover(
            "Normal likelihoods need two derivatives with respect to a covariance matrix. <bookmark mark='a'/> "
            "Nudge Sigma by a small multiple of a direction E and factor Sigma out of the determinant. "
            "<bookmark mark='b'/> To first order, the determinant of the identity plus a small matrix is one plus "
            "its trace. <bookmark mark='c'/> So the gradient of log det Sigma is Sigma inverse, a beautiful "
            "identity. <bookmark mark='d'/> And differentiating an inverse, the matrix version of minus one over x "
            "squared, gives the derivative of the trace of Sigma inverse S."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.55, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=k == 1)
        self.clear_scene()

    def mle(self):
        d = load("mle")
        rows = [
            cmath(r"\ell(\Sigma)", r"=", r"-\frac n2 \log\det\Sigma - \frac n2\operatorname{tr}(\Sigma^{-1} S_n)", font_size=34),
            cmath(r"\frac{\partial \ell}{\partial \Sigma}", r"=", r"-\frac n2\Sigma^{-1} + \frac n2\Sigma^{-1}S_n\Sigma^{-1}",
                  r"=", r"0", font_size=32),
            cmath(r"\hat\Sigma", r"=", r"S_n", r"=", r"\frac1n\sum_i (\mathbf x_i - \bar{\mathbf x})(\mathbf x_i - \bar{\mathbf x})^\top",
                  font_size=32),
        ]
        rows[2][0].set_color(EIG)
        whys = [why(r"the normal log-likelihood, \ mean set to $\bar{\mathbf x}$"), why(r"the two rules"),
                why(r"divides by $n$: \ biased, \ like Part 1's")]
        nums = VGroup(MathTex(r"\hat\Sigma_{\text{MLE}} = " + mat_tex(d["S_mle"], "{:.2f}"), font_size=28),
                      MathTex(r"\tfrac{n}{n-1}\hat\Sigma = " + mat_tex(d["S_unb"], "{:.2f}"), font_size=28))
        nums.arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.45)
        tag = simulated_tag(r"simulated: 400 of the World's families", corner=UR)
        with self.voiceover(
            "With those two rules, the maximum likelihood estimate of a covariance matrix takes one line. "
            "<bookmark mark='a'/> The normal log-likelihood, with the mean already estimated, is minus n over two "
            "log det Sigma, minus n over two times the trace of Sigma inverse times the sample covariance. "
            "<bookmark mark='b'/> Differentiate and set to zero. <bookmark mark='c'/> The estimate is the sample "
            "covariance with divisor n. For four hundred families it's this matrix; the unbiased version, divisor n "
            "minus one, differs slightly, for the reason the hook gave. Part 22 does likelihood in full."
        ) as vo:
            self.play(FadeIn(tag))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            self.play(FadeIn(nums))
        self.clear_scene()

    def hessian(self):
        rows = [
            cmath(r"\nabla^2_{\boldsymbol\beta}\, \|\mathbf y - X\boldsymbol\beta\|^2", r"=", r"2X^\top X", font_size=36),
            cmath(r"\mathbf u^\top (2X^\top X)\mathbf u", r"=", r"2\|X\mathbf u\|^2", r"\ge", r"0", font_size=36),
            cmath(r"f(\boldsymbol\beta)", r"=", r"f(\hat{\boldsymbol\beta}) + (\boldsymbol\beta - \hat{\boldsymbol\beta})^\top X^\top X"
                  r"(\boldsymbol\beta - \hat{\boldsymbol\beta})", font_size=32),
        ]
        rows[0][2].set_color(EIG)
        whys = [why(r"the Hessian: \ differentiate the gradient"), why(r"PSD: \ the criterion is a convex bowl"),
                why(r"exactly quadratic: \ its level sets are chapter 4's ellipses")]
        take = label(r"a positive definite Hessian means a unique minimum, \ and Newton's method finds it in one step (Part 21)",
                     font_size=24, color=S.ACCENT).to_edge(DOWN, buff=0.5)
        if take.width > 13:
            take.width = 13
        with self.voiceover(
            "Is the solution of the normal equations really a minimum? <bookmark mark='a'/> Differentiate the "
            "gradient again: the Hessian of the least-squares criterion is two X transpose X. "
            "<bookmark mark='b'/> It's positive semidefinite, since u transpose X transpose X u is a squared length, "
            "and definite when X has full column rank. So the criterion is a convex bowl, and the solution is its "
            "unique bottom. <bookmark mark='c'/> In fact the criterion is exactly quadratic around the solution, "
            "with level sets that are ellipses shaped by X transpose X: the confidence ellipses of Part 12. "
            "<bookmark mark='d'/> For criteria that aren't quadratic, like logistic regression's, the Hessian drives "
            "Newton's method, in Part 21."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.4, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def information(self):
        rows = [
            cmath(r"\ell(\boldsymbol\mu)", r"=", r"-\frac12\sum_i (\mathbf x_i - \boldsymbol\mu)^\top \Sigma^{-1} (\mathbf x_i - \boldsymbol\mu)",
                  font_size=32),
            cmath(r"\nabla_{\boldsymbol\mu}\,\ell", r"=", r"n\,\Sigma^{-1}(\bar{\mathbf x} - \boldsymbol\mu)", font_size=34),
            cmath(r"-\nabla^2_{\boldsymbol\mu}\,\ell", r"=", r"n\,\Sigma^{-1}", font_size=36),
            cmath(r"\big(n\Sigma^{-1}\big)^{-1}", r"=", r"\frac{\Sigma}{n}", r"=", r"\mathrm{Cov}(\bar{\mathbf x})", font_size=36),
        ]
        rows[2][2].set_color(EIG)
        rows[3][4].set_color(EXACT)
        whys = [why(r"the normal log-likelihood in $\boldsymbol\mu$ (constants dropped)"), why(r"the score: \ chapter 10's rules"),
                why(r"the information: \ the curvature"), why(r"the inverse information is the estimator's covariance")]
        take = label(r"curvature of the log-likelihood $=$ precision: \ Fisher's idea, \ Parts 9 and 22", font_size=26,
                     color=S.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "One more application shows where all this is heading. <bookmark mark='a'/> The normal log-likelihood "
            "as a function of the mean. <bookmark mark='b'/> Its gradient, the score, is n Sigma inverse times x bar "
            "minus mu: zero exactly at the sample mean. <bookmark mark='c'/> Its negative Hessian, the curvature, is "
            "n Sigma inverse: Fisher called it the information. <bookmark mark='d'/> And the inverse of the "
            "information is Sigma over n, exactly the covariance of the sample mean. A sharply curved likelihood "
            "means a precise estimate. That's Fisher's great idea, and Parts 9 and 22 develop it in full."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.5, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=False)
            self.play(FadeIn(take))
        self.clear_scene()
