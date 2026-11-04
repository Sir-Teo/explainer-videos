from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


class Trace(VoiceoverScene):
    def construct(self):
        self.card()
        self.cyclic()
        self.expectation()
        self.mse()
        self.rank()
        self.genvar()

    def card(self):
        card = chapter_card(3, r"Trace tricks", r"The sum of the diagonal, \ and why it is so useful", lit=(), part=PART)
        with self.voiceover("Chapter three. Trace tricks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def cyclic(self):
        d = load("trace")
        rows = [
            cmath(r"\operatorname{tr}(AB)", r"=", r"\sum_i (AB)_{ii}", r"=", r"\sum_i \sum_j A_{ij} B_{ji}", font_size=34),
            cmath(r"\operatorname{tr}(AB)", r"=", r"\sum_j \sum_i B_{ji} A_{ij}", r"=", r"\operatorname{tr}(BA)", font_size=34),
            cmath(r"\operatorname{tr}(ABC)", r"=", r"\operatorname{tr}(CAB)", r"=", r"\operatorname{tr}(BCA)", font_size=34),
            cmath(r"\mathbf x^\top A \mathbf x", r"=", r"\operatorname{tr}(\mathbf x^\top A \mathbf x)", r"=",
                  r"\operatorname{tr}(A\, \mathbf x \mathbf x^\top)", font_size=34),
        ]
        rows[1][4].set_color(EIG)
        rows[3][4].set_color(EIG)
        whys = [why(r"definition"), why(r"swap the order of summation"), why(r"cycle, \ but do not shuffle"),
                why(r"a number is its own trace")]
        chk = MathTex(rf"B_{{3\times5}}, C_{{5\times3}}:\ \operatorname{{tr}}(BC) = {d['trBC']:.6f},\ \operatorname{{tr}}(CB) = "
                      rf"{d['trCB']:.6f}", font_size=24, color=SIM).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The trace, the sum of a matrix's diagonal, looks too simple to matter. It matters because of one "
            "identity. <bookmark mark='a'/> The trace of A B is a double sum of A i j times B j i. "
            "<bookmark mark='b'/> Swap the order of summation and it's the trace of B A, even when A and B are "
            "different shapes and A B is tiny while B A is big. <bookmark mark='c'/> So you can cycle the factors "
            "of a product inside a trace, though you can't shuffle them. <bookmark mark='d'/> And the trick that "
            "statisticians use daily: a quadratic form, x transpose A x, is a single number, so it's its own trace, "
            "and cycling turns it into the trace of A times x x transpose, a matrix we can take expectations of."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.4, buff=0.55)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=k in (1,))
                if m == "b":
                    self.play(FadeIn(chk))
        self.clear_scene()

    def expectation(self):
        d = load("trace")
        rows = [
            cmath(r"E[\mathbf x^\top A \mathbf x]", r"=", r"E \operatorname{tr}(A\,\mathbf x \mathbf x^\top)", r"=",
                  r"\operatorname{tr}(A\, E[\mathbf x \mathbf x^\top])", font_size=34),
            cmath(r"E[\mathbf x \mathbf x^\top]", r"=", r"\Sigma + \boldsymbol\mu \boldsymbol\mu^\top", font_size=34),
            cmath(r"E[\mathbf x^\top A \mathbf x]", r"=", r"\operatorname{tr}(A\Sigma) + \boldsymbol\mu^\top A \boldsymbol\mu",
                  font_size=38),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"trace and expectation are both linear"), why(r"the covariance, \ plus the mean's outer product"),
                why(r"no normality needed")]
        chk = VGroup(MathTex(rf"\operatorname{{tr}}(A\Sigma) + \boldsymbol\mu^\top A\boldsymbol\mu = {d['trAS']:.3f} + "
                             rf"{d['muAmu']:.3f} = {d['exact']:.3f}", font_size=28, color=EXACT),
                     MathTex(rf"\text{{Monte Carlo, 200{{,}}000 draws: }} {d['mc']:.3f}", font_size=28, color=SIM))
        chk.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        use = label(r"with $A = I - H$: \ $E\,\mathrm{RSS} = \sigma^2 \operatorname{tr}(I - H) = (n - p)\sigma^2$", font_size=26,
                    color=S.ACCENT).next_to(chk, UP, buff=0.4)
        with self.voiceover(
            "Here's that trick earning its keep. <bookmark mark='a'/> The expectation of a quadratic form is the "
            "expectation of a trace, and since trace and expectation are both linear, they swap. "
            "<bookmark mark='b'/> The expected outer product of x is its covariance matrix plus the mean's outer "
            "product. <bookmark mark='c'/> So the expected quadratic form is the trace of A Sigma plus mu transpose "
            "A mu, for any distribution with a covariance, normal or not. A Monte Carlo check with two hundred "
            "thousand draws agrees to the second decimal. <bookmark mark='d'/> Put A equal to I minus H and Sigma "
            "equal to sigma squared times the identity, and out comes the hook's result: the expected residual sum "
            "of squares is n minus p times sigma squared."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.55)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            self.play(FadeIn(chk))
            vo.wait_until("d")
            self.play(FadeIn(use))
        self.clear_scene()

    def rank(self):
        rows = VGroup(
            MathTex(r"P = Q\,\Lambda\,Q^\top,\quad \Lambda = \operatorname{diag}(1, \dots, 1, 0, \dots, 0)", font_size=32),
            MathTex(r"\operatorname{tr} P = \operatorname{tr}(\Lambda Q^\top Q) = \operatorname{tr}\Lambda = \operatorname{rank} P",
                    font_size=32, color=EIG),
            MathTex(r"\operatorname{tr} H = \operatorname{tr}\big((X^\top X)^{-1} X^\top X\big) = \operatorname{tr} I_p = p",
                    font_size=32, color=FIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.4, 0])
        take = label(r"cycling the trace turns an $n \times n$ question into a $p \times p$ one", font_size=28,
                     color=S.ACCENT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "One more use. <bookmark mark='a'/> A projection can be diagonalized, with its eigenvalues, ones and "
            "zeros, on the diagonal. <bookmark mark='b'/> Cycle the orthogonal factors around, and the trace of the "
            "projection is the trace of the diagonal: the number of ones, which is its rank. "
            "<bookmark mark='c'/> And for the hat matrix there's an even quicker route. Cycle X to the end, and the "
            "trace of an n by n matrix becomes the trace of the p by p identity: p. Cycling the trace turns big "
            "questions into small ones."
        ) as vo:
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            self.play(FadeIn(take))
        self.clear_scene()

    def genvar(self):
        e = load("extras")["genvar"]
        rows = VGroup(
            MathTex(r"\operatorname{tr}\Sigma = \sum_k \lambda_k", r"\quad", r"\text{total variance}", font_size=34),
            MathTex(r"\det\Sigma = \prod_k \lambda_k", r"\quad", r"\text{generalized variance (Wilks 1932)}", font_size=34),
            MathTex(r"\|A\|_F^2 = \sum_{ij} A_{ij}^2 = \operatorname{tr}(A^\top A)", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 1.2, 0])
        for r in rows[:2]:
            r[2].set_color(GREY_B)
        nums = VGroup(MathTex(rf"\text{{families: }}\ \operatorname{{tr}} S = {e['tr']:.1f} = {e['sum']:.1f}", font_size=30, color=SIM),
                      MathTex(rf"\det S = {e['det']:.0f} = {e['prod']:.0f}", font_size=30, color=SIM)).arrange(DOWN, buff=0.2)
        nums.move_to([0, -1.2, 0])
        geo = label(r"$\det\Sigma$: \ the squared volume of the ellipse, \ up to a constant", font_size=24, color=S.ACCENT)
        geo.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Two numbers summarize a whole covariance matrix, and both come from its eigenvalues. "
            "<bookmark mark='a'/> The trace is the sum of the eigenvalues, so the trace of a covariance matrix is "
            "the total variance, summed over all directions. <bookmark mark='b'/> The determinant is their product, "
            "which Samuel Wilks called the generalized variance: it measures the volume of the cloud's ellipse. "
            "<bookmark mark='c'/> And the trace also gives the Frobenius norm, the matrix version of a sum of "
            "squares, which chapter six used to measure the error of an approximation. <bookmark mark='d'/> For the "
            "four hundred families, both identities check exactly."
        ) as vo:
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(nums), FadeIn(geo))
        self.clear_scene()

    def mse(self):
        rows = [
            cmath(r"E\,\|\hat{\boldsymbol\theta} - \boldsymbol\theta\|^2", r"=", r"E\operatorname{tr}\big[(\hat{\boldsymbol\theta} - \boldsymbol\theta)"
                  r"(\hat{\boldsymbol\theta} - \boldsymbol\theta)^\top\big]", font_size=32),
            cmath(r"E\,\|\hat{\boldsymbol\theta} - \boldsymbol\theta\|^2", r"=", r"\operatorname{tr}\,\mathrm{Cov}(\hat{\boldsymbol\theta})",
                  r"+", r"\|E\hat{\boldsymbol\theta} - \boldsymbol\theta\|^2", font_size=34),
        ]
        rows[1][2].set_color(SIM)
        rows[1][4].set_color(RES)
        whys = [why(r"a squared length is a trace"), why(r"the previous identity, \ with $\boldsymbol\mu = E\hat{\boldsymbol\theta} - "
                                                          r"\boldsymbol\theta$")]
        cap = VGroup(label(r"mean squared error \ $=$ \ total variance \ $+$ \ squared bias", font_size=28, color=S.ACCENT),
                     label(r"the bias--variance trade-off: \ Parts 9, 19 and 25", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.2)
        cap.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The same identity splits the error of any estimator. <bookmark mark='a'/> Let theta hat estimate a vector "
            "of parameters theta. Its expected squared error is the expected trace of an outer product. "
            "<bookmark mark='b'/> Apply the quadratic-form identity with the estimator's mean in place of mu, and it "
            "splits in two: the total variance of the estimator, plus its squared bias. <bookmark mark='c'/> Mean "
            "squared error is variance plus bias squared. Accepting a little bias to remove a lot of variance is the "
            "bias–variance trade-off, and it's behind ridge regression, shrinkage and most of modern statistics."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.4, buff=0.7, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(cap, shift=UP * 0.2))
        self.clear_scene()
