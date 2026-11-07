from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403


class Ridge(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.derive()
        self.collinear()
        self.svd()
        self.shrink_bars()
        self.trace()
        self.prior()
        self.mse()
        self.never()

    def card(self):
        card = chapter_card(2, r"Ridge", r"Stability by shrinking", lit=(1970,), part=PART)
        with self.voiceover("Chapter two. Ridge regression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        rows = fit_rows(VGroup(
            label(r"1962: \ Arthur Hoerl, \ a chemical engineer at DuPont, \ fits response surfaces", font_size=24),
            label(r"his predictors are nearly collinear: \ least squares swings wildly", font_size=24, color=RES),
            label(r"he adds a small constant to the diagonal of $X^\top X$", font_size=24, color=RIDGE),
            label(r"1970, \ with Robert Kennard: \ `Ridge regression: \ biased estimation for nonorthogonal problems'", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Arthur Hoerl was a chemical engineer at DuPont in the early 1960s, fitting response "
            "surfaces to process data. <bookmark mark='b'/> His predictors were nearly collinear, and least-squares "
            "coefficients swung to absurd values with small changes in the data. <bookmark mark='c'/> His remedy was to add "
            "a small constant to the diagonal of X transpose X before inverting it. The name came from the ridge-shaped "
            "surfaces he had studied. <bookmark mark='d'/> With Robert Kennard he published the theory in Technometrics in "
            "1970: biased estimation for nonorthogonal problems."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\hat\beta_\lambda", r"=", r"\arg\min \ \|y - X\beta\|^2 + \lambda\|\beta\|^2", font_size=32),
            cmath(r"-2X^\top(y - X\beta) + 2\lambda\beta", r"=", r"0", font_size=30),
            cmath(r"\hat\beta_\lambda", r"=", r"(X^\top X + \lambda I)^{-1} X^\top y", font_size=32),
            cmath(r"\lambda > 0", r":", r"X^\top X + \lambda I \text{ is always invertible}", font_size=30),
        ]
        rows[2][-1].set_color(RIDGE)
        whys = [why(r"penalized least squares"), why(r"the gradient"), why(r"Hoerl \& Kennard's estimator"),
                why(r"even when $p > n$")]
        with self.voiceover(
            "<bookmark mark='a'/> In modern terms, ridge regression minimizes the residual sum of squares plus lambda times "
            "the squared length of beta, with the predictors standardized and the outcome centred. <bookmark mark='b'/> "
            "Setting the gradient to zero, <bookmark mark='c'/> the solution is X transpose X plus lambda times the "
            "identity, inverted, times X transpose y. <bookmark mark='d'/> For any positive lambda that matrix is "
            "invertible, even when there are more variables than observations: ridge always has a unique answer."
        ) as vo:
            intro=label('A positive quadratic penalty makes the ridge system invertible',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def collinear(self):
        d = load("ridge")
        nm, ols = d["names"], np.asarray(d["ols"])
        L, C = np.asarray(d["lams"]), np.asarray(d["coefs"])
        i10 = int(np.argmin(np.abs(L - 10)))
        hdr = [r"\textbf{per SD of}", r"\textbf{least squares}", r"\textbf{ridge, \ $\lambda = 10$}"]
        body = [[nm[j], f"{ols[j]:+.1f}", f"{d['coef_at10'][j]:+.1f}"] for j in (2, 3, 4, 5, 8)]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.3, colors=[GREY_A, None, None, RES, RES, None])
        for r in tb[1:]:
            r[2].set_color(RIDGE)
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(rf"442 patients; \ total cholesterol and LDL correlate {d['corr_tc_ldl']:.2f}", font_size=22),
            label(r"least squares: \ $-37.7$ and $+22.7$, \ a large contrast fitted to noise", font_size=22, color=RES),
            label(r"ridge: \ $-11.3$ and $+1.8$; \ the other coefficients barely move", font_size=22, color=RIDGE),
        ), 12.0, 0.22, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The diabetes data of Efron, Hastie, Johnstone and Tibshirani: four hundred and "
            "forty-two patients, ten baseline measurements, and a measure of disease progression a year later. Total "
            "cholesterol and LDL cholesterol correlate point nine. <bookmark mark='b'/> Least squares gives them "
            "coefficients of minus thirty-eight and plus twenty-three per standard deviation: a large contrast "
            "between two nearly identical measurements, sensitive to noise in that weakly identified contrast; these "
            "data alone do not establish the true coefficient values. <bookmark mark='c'/> Ridge with a modest lambda"
            " of ten brings them to minus eleven and almost two, while body-mass index and log triglycerides barely "
            "move."
        ) as vo:
            self.add(diabetes_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1:]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def svd(self):
        rows = [
            cmath(r"X", r"=", r"U D V^\top", font_size=34),
            cmath(r"X\hat\beta_\lambda", r"=", r"\textstyle\sum_j u_j \dfrac{d_j^2}{d_j^2 + \lambda} u_j^\top y", font_size=30),
            cmath(r"\mathrm{df}(\lambda)", r"=", r"\mathrm{tr}\, H_\lambda = \textstyle\sum_j \dfrac{d_j^2}{d_j^2 + \lambda}", font_size=30),
            cmath(r"\text{small } d_j", r":", r"\text{shrunk most: \ the unstable directions}", font_size=30),
        ]
        rows[1][-1].set_color(RIDGE)
        whys = [why(r"Part 4's decomposition"), why(r"each principal direction shrunk by its own factor"),
                why(r"effective degrees of freedom"), why(r"where least squares is noisiest")]
        with self.voiceover(
            "<bookmark mark='a'/> The singular value decomposition shows what ridge does. <bookmark mark='b'/> The "
            "fitted values are a sum over principal directions of the data, each projection shrunk by d squared over "
            "d squared plus lambda. Directions with large singular values, where the data vary a lot, are hardly "
            "touched. <bookmark mark='c'/> The trace of the hat matrix, the effective degrees of freedom, is the sum "
            "of those factors: it falls from the rank of X towards zero as lambda grows, equal to p here because the "
            "design has full column rank. <bookmark mark='d'/> The directions with small singular values are shrunk "
            "most, and they are exactly the ones where least squares is noisiest, since the variance of an estimate "
            "along direction j is sigma squared over d j squared."
        ) as vo:
            intro=label('Singular values determine how ridge shrinks fitted directions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def shrink_bars(self):
        d = load("ridge")
        dd = np.asarray(d["d"])
        f10, f1000 = np.asarray(d["shrink_at"]["10"]), np.asarray(d["shrink_at"]["1000"])
        A = axes([0.4, 10.6], [0, 1.1], x_length=7.4, y_length=4.2, xlabel=r"principal direction, \ largest $d_j$ first",
                 ylabel=r"shrinkage factor $d_j^2/(d_j^2 + \lambda)$", xticks=list(range(1, 11)), yticks=[0, 0.5, 1],
                 center=[-2.0, 0.3, 0])
        ax = A.ax
        b10 = bars_at(ax, np.arange(1, 11) - 0.18, f10, 0.34, RIDGE, 0.85)
        b1k = bars_at(ax, np.arange(1, 11) + 0.18, f1000, 0.34, ENET, 0.85)
        rows = fit_rows(VGroup(
            label(rf"singular values {dd[0]:.0f} down to {dd[-1]:.1f}: \ condition number {d['cond']:.0f}", font_size=22),
            label(r"teal: \ $\lambda = 10$, \ only the last direction shrinks much", font_size=22, color=RIDGE),
            label(r"orange: \ $\lambda = 1000$, \ everything shrinks", font_size=22, color=ENET),
            label(r"the last direction is roughly total cholesterol minus LDL", font_size=22, color=RES),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For the diabetes data the singular values run from forty-two down to about two, a "
            "condition number of twenty-two. <bookmark mark='b'/> With lambda ten, nine directions keep more than "
            "three quarters of their size and the last keeps barely a quarter. <bookmark mark='c'/> With lambda a "
            "thousand, everything shrinks a lot. <bookmark mark='d'/> That last, weakest direction is essentially the"
            " difference between total cholesterol and LDL: a contrast whose least-squares uncertainty is large."
        ) as vo:
            self.add(diabetes_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b10], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1k], lag_ratio=0.1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Indicate(VGroup(b10[-1], b1k[-1]), color=RES), FadeIn(rows[3]))
        self.clear_scene()

    def trace(self):
        d = load("ridge")
        df, C, nm = np.asarray(d["df"]), np.asarray(d["coefs"]), d["names"]
        A = axes([0, 10.4], [-42, 40], x_length=7.6, y_length=4.8, xlabel=r"effective degrees of freedom",
                 ylabel=r"coefficient per SD", xticks=[0, 2, 4, 6, 8, 10], yticks=[-40, -20, 0, 20, 40], center=[-2.0, 0.2, 0])
        ax = A.ax
        lines = VGroup(*[polyline(ax, df, C[:, j], PATHC[j], 2.5) for j in range(10)])
        tags = VGroup(*[label(nm[j], font_size=15, color=PATHC[j]).next_to(ax.c2p(df[0], C[0, j]), RIGHT, buff=0.08)
                        for j in (2, 4, 5, 8)])
        rows = fit_rows(VGroup(
            label(r"Hoerl and Kennard's ridge trace", font_size=22),
            label(r"right: \ least squares; \ left: \ everything shrunk to zero", font_size=22, color=GREY_A),
            label(r"the wild pair settles quickly; \ the rest shrink smoothly", font_size=22, color=RIDGE),
            label(r"individual coordinates can cross zero; no thresholded zero region", font_size=22, color=RES),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Hoerl and Kennard's ridge trace: every coefficient as lambda grows, plotted here "
            "against the effective degrees of freedom. <bookmark mark='b'/> At the right, ten degrees of freedom, "
            "least squares; at the left, everything shrunk to zero. <bookmark mark='c'/> The wild pair, total "
            "cholesterol and LDL, collapses towards zero almost at once; the others shrink smoothly and in "
            "proportion. <bookmark mark='d'/> And an individual coefficient can cross zero at a finite lambda. Ridge "
            "has no threshold that holds it at zero over a range, so its path does not generally perform variable "
            "selection."
        ) as vo:
            self.add(diabetes_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(tags), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def prior(self):
        rows = [
            cmath(r"\beta", r"\sim", r"N(0, \tau^2 I), \ \ y \mid \beta \sim N(X\beta, \sigma^2 I)", font_size=30),
            cmath(r"E(\beta \mid y)", r"=", r"(X^\top X + \tfrac{\sigma^2}{\tau^2} I)^{-1} X^\top y", font_size=30),
            cmath(r"\lambda", r"=", r"\sigma^2 / \tau^2", font_size=32),
            cmath(r"\text{also}", r":", r"\text{the posterior mode \ and median}", font_size=30),
        ]
        rows[1][-1].set_color(RIDGE)
        whys = [why(r"a normal prior, \ Part 26"), why(r"conjugate"), why(r"noise over signal"),
                why(r"a normal posterior: \ all three agree")]
        with self.voiceover(
            "<bookmark mark='a'/> Ridge is also Bayesian. Give the coefficients independent normal priors with variance tau "
            "squared. <bookmark mark='b'/> The posterior mean is exactly the ridge estimate, <bookmark mark='c'/> with "
            "lambda equal to the noise variance over the prior variance: the less you believe in large effects, the more you "
            "shrink. <bookmark mark='d'/> The posterior is normal, so its mean, median and mode all coincide. That will not "
            "be true for the lasso's prior in chapter eight."
        ) as vo:
            intro=label('A Gaussian coefficient prior gives a Gaussian posterior',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mse(self):
        rows = [
            cmath(r"\mathrm{bias}^2(\lambda)", r"=", r"\lambda^2 \beta^\top (X^\top X + \lambda I)^{-2} \beta", font_size=30),
            cmath(r"\mathrm{var}(\lambda)", r"=", r"\sigma^2 \textstyle\sum_j d_j^2 / (d_j^2 + \lambda)^2", font_size=30),
            cmath(r"\tfrac{d}{d\lambda} \mathrm{MSE} \big|_{\lambda = 0}", r"=", r"-2\sigma^2 \textstyle\sum_j d_j^{-4} < 0", font_size=28),
            cmath(r"\text{so}", r":", r"\text{some } \lambda > 0 \text{ always beats least squares}", font_size=30),
        ]
        rows[3][-1].set_color(RIDGE)
        whys = [why(r"grows from 0"), why(r"falls from $\sigma^2 \sum d_j^{-2}$"), why(r"the bias starts flat"),
                why(r"full column rank; $\sigma^2>0$; oracle $\lambda$ depends on $\beta$")]
        with self.voiceover(
            "<bookmark mark='a'/> Hoerl and Kennard proved something striking. The squared bias of ridge grows from "
            "zero like lambda squared, <bookmark mark='b'/> while the total variance falls from the least-squares "
            "value. <bookmark mark='c'/> At lambda equal to zero the bias term is flat but the variance is already "
            "falling, so the derivative of the mean squared error is negative. <bookmark mark='d'/> For a fixed "
            "full-column-rank design and positive noise variance, each true coefficient vector has some "
            "risk-improving positive lambda. That oracle choice depends on the unknown coefficients; this is not one "
            "fixed lambda that dominates least squares uniformly."
        ) as vo:
            intro=label('A small oracle ridge penalty can improve risk for a full-rank design',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def never(self):
        rows = fit_rows(VGroup(
            label(r"ridge: \ unique, \ stable, \ efficient for many small effects", font_size=26, color=RIDGE),
            label(r"generically dense: no automatic thresholded support selection", font_size=26, color=RES),
            label(r"with $p = 20{,}000$ genes, \ the model still has 20{,}000 terms", font_size=26),
            label(r"a convex separable penalty can select through a corner at zero", font_size=26, color=LASSO),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So ridge is unique, stable, and very good when there are many small effects. "
            "<bookmark mark='b'/> But it is generically dense, without a thresholded region of exact zeros. <bookmark"
            " mark='c'/> With twenty thousand genes the ridge model still has twenty thousand terms, and says nothing"
            " about which ones matter. <bookmark mark='d'/> For these separable convex penalties, a corner at zero "
            "permits a thresholded zero region. Hard constraints and nonconvex counting penalties provide other "
            "selection mechanisms. The next chapter finds the right one."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
