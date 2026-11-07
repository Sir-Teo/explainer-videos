from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403


class Lasso(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.kkt()
        self.lam_max()
        self.orthonormal()
        self.thresholds()
        self.geometry()
        self.facts()
        self.bias()

    def card(self):
        card = chapter_card(4, r"The lasso", r"Shrinkage and selection in one convex problem", lit=(1996,), part=PART)
        with self.voiceover("Chapter four. The lasso."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        rows = fit_rows(VGroup(
            label(r"Breiman's nonnegative garrote (1995): \ shrink least squares by factors $c_j \ge 0$, \ $\sum c_j \le t$", font_size=24),
            label(r"Tibshirani (1996): \ bound $\sum_j |\beta_j|$ directly", font_size=24, color=LASSO),
            label(r"`least absolute shrinkage and selection operator'", font_size=24, color=GREY_A),
            label(r"slow to catch on: \ no fast algorithm until 2002--2007", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Leo Breiman's nonnegative garrote of 1995 shrank each least-squares coefficient by a "
            "nonnegative factor, with the factors constrained to a budget. <bookmark mark='b'/> Robert Tibshirani, then at "
            "Toronto, simplified the idea in 1996: put the budget directly on the sum of absolute values of the "
            "coefficients. <bookmark mark='c'/> He called it the lasso, the least absolute shrinkage and selection operator. "
            "<bookmark mark='d'/> It caught on slowly, because it needed quadratic programming for every value of the "
            "budget. Only when fast path algorithms arrived, between 2002 and 2007, did it become the workhorse it is now."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def kkt(self):
        rows = [
            cmath(r"\partial |b|", r"=", r"\{\mathrm{sign}(b)\} \ (b \ne 0), \ \ [-1, 1] \ (b = 0)", font_size=30),
            cmath(r"0", r"\in", r"-\tfrac1n X^\top(y - X\hat\beta) + \lambda\, \partial\|\hat\beta\|_1", font_size=30),
            cmath(r"\hat\beta_j \ne 0", r":", r"\tfrac1n x_j^\top(y - X\hat\beta) = \lambda\, \mathrm{sign}(\hat\beta_j)", font_size=30),
            cmath(r"\hat\beta_j = 0", r":", r"\big|\tfrac1n x_j^\top(y - X\hat\beta)\big| \le \lambda", font_size=30),
        ]
        rows[3][-1].set_color(LASSO)
        whys = [why(r"the subgradient: \ Part 21"), why(r"optimality for a convex function"),
                why(r"active: \ correlation pinned at $\pm\lambda$"), why(r"inactive: \ correlation below $\lambda$")]
        with self.voiceover(
            "<bookmark mark='a'/> The absolute value has no derivative at zero, but it has a subgradient: the sign "
            "where it is smooth, and anything between minus one and one at the kink. <bookmark mark='b'/> A convex "
            "function is minimized where zero is in its subdifferential, Part 21's condition. <bookmark mark='c'/> "
            "Read off for each coordinate: if a coefficient is nonzero, the correlation of its variable with the "
            "residual is pinned at exactly plus or minus lambda. <bookmark mark='d'/> If it is zero, that correlation"
            " is at most lambda in size. Every active variable is equally correlated with what remains; every "
            "inactive one has no larger absolute residual inner product; equality can occur at a knot."
        ) as vo:
            intro=label('Subgradient conditions distinguish zero and nonzero lasso coefficients',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lam_max(self):
        rows = [
            cmath(r"\hat\beta = 0", r"\iff", r"\tfrac1n \|X^\top y\|_\infty \le \lambda", font_size=32),
            cmath(r"\lambda_{\max}", r"=", r"\max_j \tfrac1n |x_j^\top y|", font_size=32),
            cmath(r"\lambda \downarrow", r":", r"\text{variables enter as their correlation reaches } \lambda", font_size=30),
            cmath(r"\text{diabetes}", r":", r"\text{BMI first, \ then log triglycerides}", font_size=30),
        ]
        rows[1][-1].set_color(LASSO)
        whys = [why(r"KKT at $\beta = 0$"), why(r"where the path begins"), why(r"the path: \ chapter five"),
                why(r"the largest correlations with the outcome")]
        with self.voiceover(
            "<bookmark mark='a'/> Two consequences. Setting beta to zero in the conditions, the lasso returns all "
            "zeros exactly when every variable's correlation with the outcome is at most lambda. <bookmark mark='b'/>"
            " So the path starts at lambda max, the largest of those correlations. <bookmark mark='c'/> As lambda "
            "decreases, under generic non-tied conditions, variables enter at successive knots, each when its "
            "correlation with the current residual catches up. <bookmark mark='d'/> For the diabetes data, body-mass "
            "index enters first, then log triglycerides."
        ) as vo:
            intro=label('The largest residual inner product determines the all-zero threshold',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def orthonormal(self):
        rows = [
            cmath(r"X^\top X = nI", r":", r"\tfrac1{2n}\|y - X\beta\|^2 = \text{const} + \tfrac12 \textstyle\sum_j (\beta_j - z_j)^2", font_size=28),
            cmath(r"\min_b", r"", r"\tfrac12 (b - z)^2 + \lambda |b|", font_size=32),
            cmath(r"\hat b", r"=", r"\mathrm{sign}(z)(|z| - \lambda)_+", font_size=32),
            cmath(r"\text{ridge}", r":", r"z / (1 + \lambda); \ \ \text{subset}: \ z\, \mathbf 1\{|z| > \sqrt{2\lambda}\}", font_size=28),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"$z_j = x_j^\top y / n$: \ separable"), why(r"one coordinate at a time"),
                why(r"soft thresholding"), why(r"proportional shrinkage; \ hard thresholding")]
        with self.voiceover(
            "<bookmark mark='a'/> With orthonormal columns the problem separates into one small problem per coefficient, "
            "where z j is the least-squares estimate. <bookmark mark='b'/> Minimize a half the squared distance to z plus "
            "lambda times the absolute value. <bookmark mark='c'/> The answer is soft thresholding: move z towards zero by "
            "lambda, and stop at zero. <bookmark mark='d'/> Ridge instead divides by one plus lambda, shrinking in "
            "proportion; best subset keeps or kills, hard thresholding at root two lambda."
        ) as vo:
            intro=label('Orthogonal columns separate the lasso into scalar threshold problems',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def thresholds(self):
        z = np.linspace(-4, 4, 401)
        A = axes([-4, 4], [-4, 4], x_length=5.8, y_length=5.0, xlabel=r"least-squares estimate $z$", ylabel=r"penalized estimate",
                 xticks=[-4, -2, 0, 2, 4], yticks=[-4, -2, 0, 2, 4], center=[-2.6, 0.0, 0])
        ax = A.ax
        idl = DashedLine(ax.c2p(-4, -4), ax.c2p(4, 4), color=GREY_D, stroke_width=1.5)
        lam = 1.0
        ridge = curve(ax, z, z / 2, RIDGE, 3)
        soft = curve(ax, z, np.sign(z) * np.maximum(np.abs(z) - lam, 0), LASSO, 3.5)
        t = np.sqrt(2 * lam)
        hard = VGroup(curve(ax, z[z < -t], z[z < -t], RES, 3), Line(ax.c2p(-t, 0), ax.c2p(t, 0), color=RES, stroke_width=3),
                      curve(ax, z[z > t], z[z > t], RES, 3))
        rows = fit_rows(VGroup(
            label(r"$\lambda = 1$, \ orthonormal design", font_size=22),
            label(r"ridge: halves the estimate; zero only at $z=0$", font_size=22, color=RIDGE),
            label(r"subset: \ keep or kill at $\sqrt2$", font_size=22, color=RES),
            label(r"lasso: \ zero inside $\pm\lambda$, \ shifted by $\lambda$ outside", font_size=22, color=LASSO),
            label(r"continuous, \ sparse; \ but large effects are biased by $\lambda$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The three rules side by side, with lambda one. <bookmark mark='b'/> Ridge halves "
            "every estimate and is zero exactly when that scalar estimate is zero, without a thresholded interval. "
            "<bookmark mark='c'/> Best subset keeps an estimate untouched or kills it, with a jump at root two: "
            "unstable, since a tiny change in the data can flip a variable in or out. <bookmark mark='d'/> The lasso "
            "is zero inside a band of half-width lambda and shifted towards zero by lambda outside it. <bookmark "
            "mark='e'/> It is continuous and sparse at once, the compromise; its price is that even large effects are"
            " shrunk by lambda, a bias that chapter six's penalties repair."
        ) as vo:
            self.play(FadeIn(A), Create(idl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ridge), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(hard), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(soft), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def geometry(self):
        ols = np.array([2.2, 0.5])
        Q = np.array([[1.0, 0.3], [0.3, 1.0]])
        g = L1Geometry(ols, Q=Q, center=[-2.6, 0.0, 0], unit=1.15, extent=3.0)
        tl = 1.5
        t1 = g.touch(1, tl)
        t2 = g.touch(2, tl)
        dia = g.ball(1, tl, color=LASSO)
        disc = g.ball(2, tl, color=RIDGE, fill=0.08)
        c1 = g.contour(g.loss(t1), color=S.FIT)
        c2 = g.contour(g.loss(t2), color=GREY_B)
        p1 = Dot(g.p(t1), radius=0.09, color=LASSO)
        p2 = Dot(g.p(t2), radius=0.09, color=RIDGE)
        rows = fit_rows(VGroup(
            label(r"least squares at the dot; \ ellipses of equal loss", font_size=22, color=S.FIT),
            label(rf"lasso: \ budget $|\beta_1| + |\beta_2| \le {tl}$", font_size=22, color=LASSO),
            label(rf"first touch at a corner: \ $({t1[0]:.2f}, {t1[1]:.2f})$", font_size=22, color=LASSO),
            label(rf"ridge disc: \ touches at $({t2[0]:.2f}, {t2[1]:.2f})$, \ both nonzero", font_size=22, color=RIDGE),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 19's picture, now with correlated predictors. The dot is the least-squares estimate "
            "and the ellipses are contours of the loss. <bookmark mark='b'/> The lasso's constraint is the diamond. "
            "<bookmark mark='c'/> Grow the ellipses from the dot until they first touch it: they touch at the corner on the "
            "horizontal axis, so the second coefficient is exactly zero. <bookmark mark='d'/> The ridge disc of the same "
            "radius is touched at a point where both coefficients are nonzero. Corners make zeros."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(DrawBorderThenFill(dia), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(p1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(DrawBorderThenFill(disc), Create(c2), FadeIn(p2), FadeIn(rows[3]))
        self.clear_scene()

    def facts(self):
        rows = [
            cmath(r"X\hat\beta", r":", r"\text{unique, \ even when } \hat\beta \text{ is not}", font_size=30),
            cmath(r"\text{generic } X", r":", r"\hat\beta \text{ unique, \ at most } \min(n, p) \text{ nonzero}", font_size=30),
            cmath(r"\mathrm{df}(X\hat\beta_\lambda)", r"=", r"E\, \#\{j : \hat\beta_j \ne 0\}", font_size=32),
            cmath(r"\text{so}", r":", r"C_p, \ \text{AIC and SURE use the count of nonzeros}", font_size=30),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"strict convexity in the fit"), why(r"Tibshirani (2013)"), why(r"Gaussian fixed-design, fixed $\lambda$; general position"),
                why(r"Part 28's criteria")]
        with self.voiceover(
            "<bookmark mark='a'/> A few facts about the solution. The fitted values are always unique, since the loss"
            " is strictly convex in them, even when the coefficients are not. <bookmark mark='b'/> For a design in "
            "general position the coefficients are unique too, and at most min of n and p are nonzero: this support "
            "bound uses general position. With duplicate columns, nonunique coefficient solutions can have more "
            "nonzeros. <bookmark mark='c'/> And, beautifully, under fixed design, Gaussian noise and a fixed penalty,"
            " the fit degrees of freedom equal the expected active-set rank, or the expected nonzero count in general"
            " position, a result of Hui Zou, Trevor Hastie and Robert Tibshirani from Stein's lemma. <bookmark "
            "mark='d'/> The nonzero count can estimate degrees of freedom in that fixed-penalty setting, adding one "
            "for an unpenalized intercept. Choosing the penalty from the data introduces further tuning complexity."
        ) as vo:
            intro=label('Lasso degrees of freedom require a specified design and fixed penalty',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bias(self):
        rows = fit_rows(VGroup(
            label(r"the lasso does two jobs with one $\lambda$: \ select, \ and shrink", font_size=26),
            label(r"large $\lambda$ to remove noise variables shrinks the real effects too", font_size=26, color=RES),
            label(r"small $\lambda$ to keep the effects lets noise variables in", font_size=26, color=RES),
            label(r"fixes: \ refit (relaxed lasso), \ reweight (adaptive), \ or bend the penalty (MCP, SCAD)", font_size=26, color=LASSO),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lasso does two jobs with one tuning parameter: it selects variables and it "
            "shrinks their coefficients. <bookmark mark='b'/> A lambda large enough to remove every noise variable "
            "also biases the real effects; the simple shift by lambda is specific to orthonormal coordinates. "
            "<bookmark mark='c'/> A lambda small enough to leave the real effects nearly unbiased lets noise "
            "variables in. <bookmark mark='d'/> The fixes separate the jobs: refit the selected variables with a "
            "smaller penalty, the relaxed lasso; reweight the penalty by a first estimate, the adaptive lasso; or "
            "bend the penalty so that large coefficients are not penalized at all. Chapter six."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
