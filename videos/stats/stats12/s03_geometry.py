from __future__ import annotations

import numpy as np

from videos.stats.stats12.common import *  # noqa: F403


class Geometry(VoiceoverScene):
    def construct(self):
        self.card()
        self.space()
        self.check()
        self.hat()
        self.qr()
        self.pythagoras()
        self.many_x()

    def card(self):
        card = chapter_card(2, r"Geometry", r"Least squares is a projection", part=PART)
        with self.voiceover("Chapter two. Geometry."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def space(self):
        x = np.array([1.0, 2.0, 4.0])
        y = np.array([1.5, 3.5, 3.0])
        X = np.column_stack([np.ones(3), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        yh = X @ b
        ns = NSpace(scale=0.48, center=[-2.6, 0.0, 0], angle=-0.65, tilt=0.35, axis_len=6.5,
                    axis_labels=[r"obs 1", r"obs 2", r"obs 3"])
        u1 = np.ones(3) / np.sqrt(3)
        xc = x - x.mean()
        u2 = xc / np.linalg.norm(xc)
        pl = ns.plane(u1, u2, extent=5.0, color=FIT, opacity=0.14)
        vy = ns.vector(y, color=DATA)
        vh = ns.vector(yh, color=FIT)
        res = ns.segment(yh, y, color=RES, stroke_width=4)
        ra = ns.right_angle(yh, (y - yh) / np.linalg.norm(y - yh), (yh - 0) / np.linalg.norm(yh), size=0.5)
        rows = fit_rows(VGroup(
            label(r"three observations: \ $y$ is one point in $\mathbb R^3$", font_size=24, color=DATA),
            label(r"every possible fit $a\mathbf 1 + b\,\mathbf x$: \ a plane, \ the column space of $X$", font_size=24, color=FIT),
            label(r"least squares: \ the closest point of the plane, \ $\hat y$", font_size=24, color=FIT),
            label(r"the residual $y - \hat y$ is perpendicular to the plane", font_size=24, color=RES),
            MathTex(r"X^\top(y - X\hat\beta) = 0", font_size=30, color=OBS),
            label(r"the normal equations say exactly this: \ ``normal'' means perpendicular", font_size=22, color=GREY_A),
        ), 5.0, 0.3, [4.3, 0.2, 0])
        heading = label(r"Least squares projects the response onto the model space", font_size=36).move_to([0, 3.3, 0])
        with self.voiceover(
            "Now the picture that explains everything, from Part 4. <bookmark mark='a'/> Take a dataset of just three "
            "observations. The three responses are one point, one vector, in three-dimensional space. "
            "<bookmark mark='b'/> Every possible fitted line, a times the ones vector plus b times the x vector, is a point "
            "in the plane spanned by those two vectors: the column space of X. <bookmark mark='c'/> Least squares picks the "
            "point of that plane closest to y, in ordinary distance, because the sum of squared residuals is the squared "
            "distance. <bookmark mark='d'/> The closest point is the foot of the perpendicular: the residual vector stands "
            "at right angles to the plane. <bookmark mark='e'/> That's what the normal equations say: X transpose times the "
            "residual is zero, the residual is orthogonal to every column. Normal, in normal equations, means perpendicular. "
            "Turn the picture to see the right angle."
        ) as vo:
            self.add(ns)
            self.play(FadeIn(ns.axes3), FadeIn(heading))
            vo.wait_until("a")
            self.add(vy)
            self.play(NSpace.reveal(vy), FadeIn(rows[0]))
            self.play(FadeOut(heading), run_time=0.25)
            vo.wait_until("b")
            self.add(pl)
            self.play(NSpace.reveal(pl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.add(vh)
            self.play(NSpace.reveal(vh), FadeIn(rows[2]))
            vo.wait_until("d")
            self.add(res, ra)
            self.play(NSpace.reveal(res, ra), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4:]))
            self.play(ns.turn(1.0, run_time=5.0))
            for m_ in (pl, vy, vh, res, ra):
                m_.clear_updaters()
        self.clear_scene()

    def hat(self):
        rows = [
            cmath(r"\hat y", r"=", r"X(X^\top X)^{-1}X^\top y = Hy", font_size=34),
            cmath(r"H^2 = H,\quad H^\top", r"=", r"H", r"\quad\text{a projection (Part 4)}", font_size=32),
            cmath(r"e", r"=", r"(I - H)\,y \ \perp\ \hat y", font_size=34),
            cmath(r"\mathrm{tr}\,H", r"=", r"p,\qquad \mathrm{tr}(I - H) = n - p", font_size=34),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"full column rank $X$; \ the hat matrix puts the hat on $y$"), why(r"eigenvalues 0 and 1 only"),
                why(r"the residual maker, \ also a projection"), why(r"degrees of freedom: \ the residuals live in $n - p$ dimensions")]
        intro = label('A matrix projects observations onto the fitted space', font_size=36)
        with self.voiceover(
            "In matrix form, <bookmark mark='a'/> the fitted values are a matrix H, the hat matrix, times y: it puts the hat "
            "on y. <bookmark mark='b'/> H is symmetric and idempotent, a projection, the object Part 4 opened with, so its "
            "eigenvalues are zero and one. <bookmark mark='c'/> One minus H makes the residuals, and it's also a projection, "
            "onto the space perpendicular to the columns. <bookmark mark='d'/> For full column rank X, the trace of H is the number of columns, p, including the intercept, so "
            "the residuals live in n minus p dimensions. That's why the variance estimate divides the residual sum of "
            "squares by n minus p, Part 8's n minus one, generalized."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def pythagoras(self):
        d = load("line")
        rows = [
            cmath(r"\|y - \bar y\mathbf 1\|^2", r"=", r"\|\hat y - \bar y\mathbf 1\|^2 + \|y - \hat y\|^2", font_size=34),
            cmath(r"\text{TSS}", r"=", r"\text{ESS} + \text{RSS}", font_size=34),
            cmath(r"R^2", r"=", r"\frac{\text{ESS}}{\text{TSS}} = \cos^2\angle(y - \bar y\mathbf 1,\ \hat y - \bar y\mathbf 1)", font_size=32),
            cmath(r"\text{our 30 families}", r":", rf"R^2 = {d['r2']:.3f} = r^2", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"a right angle: \ Pythagoras"), why(r"total = explained + residual"),
                why(r"the share explained: \ a squared cosine"), why(r"for one predictor, \ the squared correlation")]
        intro = label('An orthogonal decomposition gives the sums of squares', font_size=36)
        with self.voiceover(
            "And because there's a right angle, there's Pythagoras. <bookmark mark='a'/> Centre everything at the mean. "
            "The squared length of the data's deviation from its mean equals the squared length of the fitted values' "
            "deviation plus the squared length of the residual. <bookmark mark='b'/> In words: the total sum of squares is "
            "the explained sum of squares plus the residual sum of squares. <bookmark mark='c'/> R squared is the explained "
            "share, the squared cosine of the angle between the data and the fit. <bookmark mark='d'/> For our thirty "
            "families, point one eight: the squared correlation. Parents' heights explain under a fifth of the variation in "
            "these children's heights. Chapter four turns this Pythagoras into the F-test."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def qr(self):
        rows = [
            cmath(r"X", r"=", r"QR,\quad Q^\top Q = I,\ R \text{ upper triangular}", font_size=34),
            cmath(r"X^\top X\hat\beta = X^\top y", r"\iff", r"R\hat\beta = Q^\top y", font_size=34),
            cmath(r"H", r"=", r"QQ^\top,\qquad h_{ii} = \|q_i\|^2", font_size=34),
            cmath(r"\kappa(X^\top X)", r"=", r"\kappa(X)^2", r"\quad\text{why never to form } X^\top X", font_size=32),
        ]
        rows[1][2].set_color(FIT)
        whys = [why(r"Gram--Schmidt on the columns (Part 4): \ an orthonormal basis of the column space"),
                why(r"back-substitution: \ no inverse anywhere"), why(r"projection onto an orthonormal basis; \ leverages for free"),
                why(r"the condition number squares: \ digits lost twice over")]
        intro = label('Compute least squares with an orthogonal factorization', font_size=36)
        with self.voiceover(
            "How does a computer actually find the projection? <bookmark mark='a'/> It orthonormalizes the columns of X, "
            "Part 4's Gram–Schmidt, writing X as Q times R, where Q has orthonormal columns spanning the same plane and R is "
            "upper triangular. <bookmark mark='b'/> Then the normal equations become R beta-hat equals Q transpose y, solved by "
            "back-substitution, with no inverse anywhere. <bookmark mark='c'/> The hat matrix is just Q Q transpose, and each "
            "point's leverage is the squared length of its row of Q, for free. <bookmark mark='d'/> Forming X transpose X "
            "squares the condition number, so if X is nearly collinear you lose twice as many digits. That's why statkit, like "
            "many numerical routines, uses QR; SVD is another stable approach."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def check(self):
        from explainer.stats.kit import ols as O
        d = load("line")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        r = O.fit(O.design(x), y)
        rows = [
            cmath(r"\textstyle\sum_i e_i", r"=", rf"{r.resid.sum():.1e}".replace("e-", r"\times 10^{-") + "}", r"\quad e \perp \mathbf 1", font_size=32),
            cmath(r"\textstyle\sum_i x_i e_i", r"=", rf"{(x * r.resid).sum():.1e}".replace("e-", r"\times 10^{-") + "}", r"\quad e \perp \mathbf x", font_size=32),
            cmath(r"\textstyle\sum_i \hat y_i e_i", r"=", rf"{(r.fitted * r.resid).sum():.1e}".replace("e-", r"\times 10^{-") + "}", r"\quad e \perp \hat y", font_size=32),
        ]
        whys = [why(r"zero to machine precision"), why(r"the normal equations, \ checked"), why(r"so residuals vs fitted values must show no trend")]
        foot = label(r"a residual plot with a linear trend means a bug, \ not a finding", font_size=24, color=OBS).to_edge(DOWN, buff=0.8)
        intro = label('Check orthogonality on the thirty families', font_size=36)
        with self.voiceover(
            "You can check the right angle numerically on the thirty families. <bookmark mark='a'/> The residuals add up to zero, "
            "to fifteen decimal places: they're perpendicular to the ones vector. <bookmark mark='b'/> Their products with x add "
            "up to zero: perpendicular to x. <bookmark mark='c'/> And so they're perpendicular to every fitted value, which is a "
            "combination of the two. <bookmark mark='d'/> That's why a plot of residuals against fitted values can never show a "
            "linear trend from least squares itself. If yours does, something is wrong with the computation, not with the world."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.2, x=-0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def many_x(self):
        rows = fit_rows(VGroup(
            label(r"with $p$ independent columns, including the intercept, the picture is the same, \ one dimension up", font_size=28),
            label(r"the fit is a $p$-dimensional plane in $\mathbb R^n$; \ $\hat y$ is the foot of the perpendicular from $y$", font_size=24),
            label(r"every coefficient is a FWL slope (ch.~5): \ its predictor, \ cleaned of all the others", font_size=24, color=OBS),
            label(r"the residual space has $n - p$ dimensions: \ with rank $p$ close to $n$, \ almost nothing is left to estimate $\sigma$", font_size=24,
                  color=GREY_A),
            label(r"$p > n$, full row rank: \ interpolation; \ prediction needs further structure (Part 32)", font_size=24, color=MISS),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With many predictors, nothing in the picture changes except the dimension. "
            "<bookmark mark='b'/> The possible fits form a p-dimensional plane inside n-dimensional space, and the fitted values "
            "are the foot of the perpendicular from y. <bookmark mark='c'/> Each coefficient is a Frisch–Waugh–Lovell slope: the "
            "partial linear association after projecting out the others, as chapter five shows. <bookmark mark='d'/> The residuals "
            "live in the remaining n minus p dimensions, so as p approaches n there's little left over to estimate the noise. "
            "<bookmark mark='e'/> And when p exceeds n, a full-row-rank design spans the whole space and can interpolate the data. Prediction then needs further structure or regularization. That's the starting point of Part 32."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
