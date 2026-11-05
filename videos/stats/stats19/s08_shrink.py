from __future__ import annotations

import numpy as np

from videos.stats.stats19.common import *  # noqa: F403


class Shrinkage(VoiceoverScene):
    def construct(self):
        self.card()
        self.ridge()
        self.lasso()
        self.geometry()
        self.soft()
        self.paths()
        self.cv()

    def card(self):
        card = chapter_card(7, r"Ridge and the lasso, \ a first look", r"Shrink to predict better", lit=(1996,), part=PART)
        with self.voiceover("Chapter seven. Ridge and the lasso, a first look."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ridge(self):
        rows = [
            cmath(r"\hat\beta_{\text{ridge}}", r"=", r"\arg\min \|y - X\beta\|^2 + \lambda\|\beta\|_2^2", font_size=30),
            cmath(r"\ ", r"=", r"(X'X + \lambda I)^{-1} X'y", font_size=32),
            cmath(r"\lambda = 0", r":", r"\text{least squares};\ \ \lambda \to \infty: \ \beta \to 0", font_size=30),
            cmath(r"\text{the trade}", r":", r"\text{a little bias for a lot less variance}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"Hoerl \& Kennard (1970)"), why(r"always invertible, \ even with collinear $x$'s"),
                why(r"a dial from Part 12 to nothing"), why(r"chapter two, \ applied to coefficients")]
        with self.voiceover(
            "Linear models have their own dial. <bookmark mark='a'/> Ridge regression, proposed by Arthur Hoerl and Robert "
            "Kennard in 1970, minimizes the squared error plus lambda times the sum of squared coefficients. "
            "<bookmark mark='b'/> The solution adds lambda to the diagonal of X prime X before inverting, so it exists even "
            "when the predictors are nearly collinear and least squares falls apart. <bookmark mark='c'/> Lambda zero is Part "
            "12's least squares; as lambda grows, every coefficient shrinks toward zero. <bookmark mark='d'/> The shrinkage "
            "adds bias and removes variance, chapter two's trade, and with many predictors or noisy data the trade is usually "
            "favourable."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lasso(self):
        rows = [
            cmath(r"\hat\beta_{\text{lasso}}", r"=", r"\arg\min \tfrac{1}{2n}\|y - X\beta\|^2 + \lambda\|\beta\|_1", font_size=30),
            cmath(r"\|\beta\|_1", r"=", r"|\beta_1| + \cdots + |\beta_p|", font_size=32),
            cmath(r"\text{the difference}", r":", r"\text{many coefficients become exactly } 0", font_size=30),
            cmath(r"\text{so}", r":", r"\text{shrinkage and variable selection at once}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"Tibshirani (1996)"), why(r"absolute values instead of squares"), why(r"the corners of the next picture"),
                why(r"a sparse, \ readable model")]
        with self.voiceover(
            "<bookmark mark='a'/> Robert Tibshirani's lasso, of 1996, changes one thing: it penalizes the sum of the absolute "
            "values of the coefficients instead of their squares. <bookmark mark='b'/> The one-norm. <bookmark mark='c'/> The "
            "consequence is striking: as lambda grows, coefficients don't just shrink, many become exactly zero. "
            "<bookmark mark='d'/> So the lasso shrinks and selects variables at the same time, and produces a sparse model "
            "that can be read."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def geometry(self):
        ols = [2.0, 0.7]
        Q = [[1.0, 0.45], [0.45, 1.0]]
        g1 = L1Geometry(ols, Q=Q, center=[-3.3, -0.1, 0], unit=1.0, extent=2.6)
        g2 = L1Geometry(ols, Q=Q, center=[3.3, -0.1, 0], unit=1.0, extent=2.6)
        t = 1.2
        diamond = g1.ball(1, t, color=OBS)
        circle = g2.ball(2, t, color=S.CTRL)
        b1, b2 = g1.touch(1, t), g2.touch(2, t)
        c1 = g1.contour(g1.loss(b1), color=FIT)
        c2 = g2.contour(g2.loss(b2), color=FIT)
        c1b = VGroup(*[g1.contour(g1.loss(b1) * f, color=FIT, stroke_width=1.2) for f in (0.3, 0.6)])
        c2b = VGroup(*[g2.contour(g2.loss(b2) * f, color=FIT, stroke_width=1.2) for f in (0.3, 0.6)])
        d1 = Dot(g1.p(b1), radius=0.1, color=OBS)
        d2 = Dot(g2.p(b2), radius=0.1, color=S.CTRL)
        t1 = label(r"lasso: \ $|\beta_1| + |\beta_2| \le t$", font_size=22, color=OBS).next_to(g1, UP, buff=0.1)
        t2 = label(r"ridge: \ $\beta_1^2 + \beta_2^2 \le t^2$", font_size=22, color=S.CTRL).next_to(g2, UP, buff=0.1)
        r1 = MathTex(rf"\hat\beta = ({b1[0]:.2f},\ {abs(b1[1]):.2f})", font_size=24, color=OBS).next_to(g1, DOWN, buff=0.1)
        r2 = MathTex(rf"\hat\beta = ({b2[0]:.2f},\ {b2[1]:.2f})", font_size=24, color=S.CTRL).next_to(g2, DOWN, buff=0.1)
        with self.voiceover(
            "Why exact zeros? The picture explains it. <bookmark mark='a'/> In the plane of two coefficients, the least-squares "
            "estimate sits at the green dot, and the ellipses around it are contours of equal squared error. "
            "<bookmark mark='b'/> The lasso, in its equivalent constrained form, keeps the coefficients inside a diamond; ridge "
            "keeps them inside a circle. <bookmark mark='c'/> The solution is where the expanding ellipse first touches the "
            "region. <bookmark mark='d'/> For the circle, that's a smooth point where both coefficients are non-zero: shrunk, "
            "but both present. For the diamond, it's very often a corner, and at a corner one coefficient is exactly zero. "
            "<bookmark mark='e'/> Here the lasso keeps beta one and sets beta two to zero; ridge keeps a little of both. In many "
            "dimensions the diamond has many corners and edges, and the lasso lands on them constantly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(g2), Create(c1b), Create(c2b))
            vo.wait_until("b")
            self.play(DrawBorderThenFill(diamond), DrawBorderThenFill(circle), FadeIn(t1), FadeIn(t2))
            vo.wait_until("c")
            self.play(Create(c1), Create(c2))
            vo.wait_until("d")
            self.play(FadeIn(d1, scale=1.6), FadeIn(d2, scale=1.6))
            vo.wait_until("e")
            self.play(FadeIn(r1), FadeIn(r2))
        self.clear_scene()

    def soft(self):
        z = np.linspace(-3, 3, 200)
        lam = 1.0
        A = axes([-3, 3], [-3, 3], x_length=4.6, y_length=4.6, xlabel=r"least-squares $\hat\beta_j$", ylabel=r"shrunk",
                 xticks=[-2, 0, 2], yticks=[-2, 0, 2], center=[-3.6, 0.0, 0], font_size=18)
        ax = A.ax
        ident = polyline(ax, z, z, GREY_C, 2)
        soft = polyline(ax, z, np.sign(z) * np.maximum(np.abs(z) - lam, 0), OBS, 3.5)
        rid = polyline(ax, z, z / (1 + lam), S.CTRL, 3.5)
        rows = fit_rows(VGroup(
            label(r"orthonormal predictors:", font_size=22),
            MathTex(r"\text{lasso}: \ \text{sign}(\hat\beta)\,(|\hat\beta| - \lambda)_+", font_size=26, color=OBS),
            MathTex(r"\text{ridge}: \ \hat\beta / (1 + \lambda)", font_size=26, color=S.CTRL),
            label(r"the lasso zeroes small coefficients and shifts big ones by $\lambda$", font_size=20),
            label(r"ridge scales everything, \ zeroes nothing", font_size=20, color=GREY_A),
        ), 6.2, 0.4, [3.2, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> When the predictors are orthonormal, both rules act coefficient by coefficient, and their "
            "difference fits in one picture. <bookmark mark='b'/> The lasso soft-thresholds: any least-squares coefficient "
            "smaller than lambda becomes zero, and larger ones move toward zero by lambda. <bookmark mark='c'/> Ridge simply "
            "scales every coefficient by one over one plus lambda. <bookmark mark='d'/> So the lasso kills small effects and "
            "keeps large ones, slightly shrunk; <bookmark mark='e'/> ridge keeps everyone, all a little smaller."
        ) as vo:
            self.play(FadeIn(A), Create(ident))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(soft), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(rid), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def paths(self):
        d = load("lasso")
        lams = np.log10(np.asarray(d["lams"]))
        P = np.asarray(d["path"])
        R = np.asarray(d["ridge_path"])
        rl = np.log10(np.asarray(d["ridge_lams"]))
        true = np.asarray(d["true"])
        A = axes([lams.min(), lams.max()], [-2.6, 4.2], x_length=5.6, y_length=3.8, xlabel=r"$\log_{10}\lambda$",
                 ylabel=r"coefficients", yticks=[-2, 0, 2, 4], center=[-3.4, 0.4, 0], font_size=16)
        B = axes([rl.min(), rl.max()], [-2.6, 4.2], x_length=5.6, y_length=3.8, xlabel=r"$\log_{10}\lambda$",
                 ylabel=r"coefficients", yticks=[-2, 0, 2, 4], center=[3.4, 0.4, 0], font_size=16)
        cols = [OBS if t != 0 else GREY_C for t in true]
        la = VGroup(*[polyline(A.ax, lams, P[:, j], cols[j], 2.8 if true[j] else 1.4) for j in range(P.shape[1])])
        ra = VGroup(*[polyline(B.ax, rl, R[:, j], cols[j], 2.8 if true[j] else 1.4) for j in range(R.shape[1])])
        ta = label(r"lasso", font_size=24, color=OBS).next_to(A, UP, buff=0.1)
        tb = label(r"ridge", font_size=24, color=S.CTRL).next_to(B, UP, buff=0.1)
        foot = fit_rows(VGroup(
            label(r"20 predictors; \ 3 truly matter \ (gold); \ 17 are noise \ (grey)", font_size=22),
            label(r"lasso: \ coefficients enter one by one as $\lambda$ falls; \ ridge: \ all at once, \ never exactly zero", font_size=20,
                  color=GREY_A),
        ), 12.4, 0.2, [0, -2.6, 0])
        tag = simulated_tag(r"$n = 100$, \ $p = 20$", corner=UR)
        with self.voiceover(
            "<bookmark mark='a'/> Now a regression with twenty predictors, of which three really matter, in gold, and seventeen "
            "are noise, in grey. <bookmark mark='b'/> The lasso path traces every coefficient as lambda decreases from left to "
            "right. At the left, all are zero. As lambda falls, the three real effects enter first, one after another, and "
            "only later do the noise variables creep in. <bookmark mark='c'/> The ridge path, for comparison: every coefficient "
            "grows smoothly from zero together, and none is ever exactly zero."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(ta), LaggedStart(*[Create(c) for c in la], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(tb), LaggedStart(*[Create(c) for c in ra], lag_ratio=0.05), FadeIn(foot[1]), run_time=2.5)
        self.clear_scene()

    def cv(self):
        d = load("lasso")
        rows = [
            cmath(r"\text{10-fold CV over } \lambda", r":", r"\text{the minimum keeps}\ " + f"{d['nz_best']}" + r"\ \text{variables}", font_size=28),
            cmath(r"\text{one-SE rule}", r":", r"\text{keeps}\ " + f"{d['nz_one_se']}", font_size=30),
            cmath(r"\text{which}", r":", r"\text{exactly the three real effects}", font_size=30),
            cmath(r"\text{true}", r":", rf"({d['true'][0]:.2f},\ {d['true'][3]:.2f},\ {d['true'][7]:.2f});\ \ \hat\beta: ({d['b_one_se'][0]:.2f},\ {d['b_one_se'][3]:.2f},\ {d['b_one_se'][7]:.2f})",
                  font_size=26),
        ]
        rows[2][2].set_color(HIT)
        whys = [why(r"the most accurate predictor"), why(r"chapter three's rule, \ for $\lambda$"),
                why(r"selection, \ here, \ succeeded"), why(r"standardized scale: \ shrunk toward 0")]
        with self.voiceover(
            "<bookmark mark='a'/> Choose lambda by ten-fold cross-validation. The minimum keeps eight variables: the three real "
            "ones and five passengers, which help prediction a little by soaking up noise. <bookmark mark='b'/> The one-standard-"
            "error rule chooses a larger lambda, and keeps three. <bookmark mark='c'/> Exactly the three real effects. "
            "<bookmark mark='d'/> Their estimates are shrunk toward zero, the lasso's bias, which a refit by least squares on the "
            "selected variables would remove. Whether selection like this can be trusted in general, and what inference after it "
            "means, are questions for Parts 32 and 56."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
