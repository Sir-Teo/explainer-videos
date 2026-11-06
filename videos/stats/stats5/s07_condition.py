from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class Condition(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.proof()
        self.bivariate()
        self.galton()
        self.precision()

    def card(self):
        card = chapter_card(6, r"Conditioning a Gaussian", r"Where regression is born", lit=(1886,), part=PART)
        with self.voiceover("Chapter six. Conditioning a Gaussian."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        part = MathTex(r"\begin{pmatrix} \mathbf X_1 \\ \mathbf X_2 \end{pmatrix} \sim N\!\left(\begin{pmatrix} \boldsymbol\mu_1 \\ "
                       r"\boldsymbol\mu_2 \end{pmatrix},\ \begin{pmatrix} \Sigma_{11} & \Sigma_{12} \\ \Sigma_{21} & \Sigma_{22} "
                       r"\end{pmatrix}\right)", font_size=34).to_edge(UP, buff=0.5)
        th = theorem_card(r"Conditional normal", r"$\mathbf X_2 \mid \mathbf X_1 = \mathbf x_1 \ \sim\ N\big(\boldsymbol\mu_2 + "
                          r"\Sigma_{21}\Sigma_{11}^{-1}(\mathbf x_1 - \boldsymbol\mu_1),\ \ \Sigma_{22} - \Sigma_{21}\Sigma_{11}^{-1}\Sigma_{12}\big)$",
                          color=COND, width=10.6, font_size=26).move_to([0, 0.4, 0])
        notes = VGroup(label(r"$\Sigma\succ0$: the mean is affine in $\mathbf x_1$", font_size=26, color=COND),
                       label(r"the covariance: \ the Schur complement (Part 4), \ the same for every $\mathbf x_1$", font_size=26,
                             color=S.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.8)
        intro = label('Gaussian conditioning', font_size=36)
        with self.voiceover(
            "The slicer showed every slice of a Gaussian is a Gaussian of the same width, centred on a straight line. "
            "Here's the theorem. <bookmark mark='a'/> Split a multivariate normal vector with positive definite covariance into two blocks. "
            "<bookmark mark='b'/> Given the first block, the second is normal again. <bookmark mark='c'/> Its mean "
            "is linear in the observed value: the prior mean, plus a matrix times the surprise. And its covariance is "
            "the Schur complement from Part 4's chapter on block matrices, which doesn't depend on the observed value "
            "at all."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Write(part))
            vo.wait_until("b")
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(notes))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\mathbf W", r"=", r"\mathbf X_2 - \Sigma_{21}\Sigma_{11}^{-1}\mathbf X_1", font_size=34),
            cmath(r"\mathrm{Cov}(\mathbf W, \mathbf X_1)", r"=", r"\Sigma_{21} - \Sigma_{21}\Sigma_{11}^{-1}\Sigma_{11}", r"=", r"0", font_size=34),
            cmath(r"\mathbf X_2", r"=", r"\mathbf W + \Sigma_{21}\Sigma_{11}^{-1}\mathbf X_1", font_size=34),
            cmath(r"\mathrm{Cov}(\mathbf W)", r"=", r"\Sigma_{22} - \Sigma_{21}\Sigma_{11}^{-1}\Sigma_{12}", font_size=34),
        ]
        rows[3][2].set_color(S.ACCENT)
        whys = [why(r"remove the part of $\mathbf X_2$ predictable from $\mathbf X_1$"),
                why(r"uncorrelated, \ jointly normal: \ \emph{independent} (chapter 5)"),
                why(r"given $\mathbf X_1$, only $\mathbf W$ is random"), why(r"$\mathrm{Var}(\mathbf X_2 - B\mathbf X_1)$, expanded")]
        intro = label('Remove the predictable part', font_size=36)
        with self.voiceover(
            "The proof is a single trick. <bookmark mark='a'/> Subtract from X two the part that's linearly "
            "predictable from X one, and call the remainder W. <bookmark mark='b'/> W is uncorrelated with X one, and "
            "since they're jointly normal, chapter five says W is independent of X one. <bookmark mark='c'/> So X two "
            "is an independent normal W plus a linear function of X one. Given X one, only W is random: X two is "
            "normal, centred at the linear function. <bookmark mark='d'/> And its covariance is W's, the Schur "
            "complement."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-1.2, buff=0.55, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def bivariate(self):
        rows = [
            cmath(r"E[Y \mid X = x]", r"=", r"\mu_Y + \frac{\sigma_{XY}}{\sigma_X^2}(x - \mu_X)", r"=",
                  r"\mu_Y + \rho\,\frac{\sigma_Y}{\sigma_X}(x - \mu_X)", font_size=32),
            cmath(r"\mathrm{Var}(Y \mid X = x)", r"=", r"\sigma_Y^2 - \frac{\sigma_{XY}^2}{\sigma_X^2}", r"=", r"\sigma_Y^2 (1 - \rho^2)",
                  font_size=32),
            cmath(r"\frac{E[Y \mid x] - \mu_Y}{\sigma_Y}", r"=", r"\rho\, \frac{x - \mu_X}{\sigma_X}", font_size=36),
        ]
        rows[0][4].set_color(COND)
        rows[1][4].set_color(S.ACCENT)
        rows[2][2].set_color(COND)
        whys = [why(r"two variables: \ the regression line"), why(r"a fraction $1 - \rho^2$ of the variance is left"),
                why(r"in standard units: \ multiply by $\rho$")]
        intro = label('Regression in standard units', font_size=36)
        with self.voiceover(
            "With just two variables, the theorem is the regression line. <bookmark mark='a'/> The conditional mean of "
            "Y given x is mu Y plus rho times the ratio of standard deviations, times the deviation of x: a straight "
            "line with slope rho sigma Y over sigma X. <bookmark mark='b'/> The conditional variance is sigma Y "
            "squared times one minus rho squared: a fraction rho squared of the variance is explained. "
            "<bookmark mark='c'/> And in standard units, the prediction is simply rho times the standardized x. Since "
            "rho is between minus one and one, its magnitude is no larger than the standardized x, and is strictly smaller away from zero when the absolute correlation is below one. That one "
            "line is regression to the mean."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def galton(self):
        d = load("galton")
        rows = VGroup(
            MathTex(rf"\bar x = {d['mx']:.2f},\ \ s_x = {d['sx']:.2f};\quad \bar y = {d['my']:.2f},\ \ s_y = {d['sy']:.2f};\quad "
                    rf"r = {d['r']:.3f}", font_size=30),
            MathTex(rf"\text{{slope}} = r\,\frac{{s_y}}{{s_x}} = {d['r']:.3f} \times \frac{{{d['sy']:.2f}}}{{{d['sx']:.2f}}} = {d['b_yx']:.3f}",
                    font_size=32, color=COND),
            MathTex(rf"\text{{residual SD}} = s_y\sqrt{{1 - r^2}} = {d['sy'] * np.sqrt(1 - d['r'] ** 2):.2f}\ \text{{in}}", font_size=30,
                    color=S.ACCENT),
            label(r"Galton's ``two-thirds'', \ derived: \ and the children's spread is \emph{larger} than the mid-parents'",
                  font_size=24, color=GREY_A),
            label(r"(a mid-parent averages two people, \ so it varies less: \ $s_x < s_y$)", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.35).move_to([0, 0.2, 0])
        for r in rows:
            if r.width > 12.8:
                r.width = 12.8
        src = historical_tag(r"Galton (1886), 928 children")
        intro = label("Galton's fitted regression", font_size=36)
        with self.voiceover(
            "Put Galton's numbers in. <bookmark mark='a'/> The mid-parents average sixty-eight point three inches "
            f"with standard deviation {d['sx']:.2f}; the children sixty-eight point one with {d['sy']:.2f}; the "
            f"correlation is {d['r']:.2f}. <bookmark mark='b'/> The slope is r times the ratio of standard deviations: "
            f"{d['b_yx']:.2f}, Galton's two-thirds, now derived rather than observed. <bookmark mark='c'/> Around the "
            f"line, children still scatter with a standard deviation of {d['sy'] * np.sqrt(1 - d['r'] ** 2):.1f} inches. "
            "<bookmark mark='d'/> The slope is bigger than r because children vary more than mid-parents do: a "
            "mid-parent is an average of two people, and averages vary less, as Part 6 will make precise."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def precision(self):
        d = load("extras2")["chain"]
        R, K = np.asarray(d["R"]), np.asarray(d["K"])
        K = np.where(np.abs(K) < 1e-9, 0.0, K)

        def mat(M, hi=None, color=S.RESID):
            m = Matrix([[f"{v:.2f}" for v in r] for r in M], element_to_mobject=lambda s: MathTex(s, font_size=26),
                       h_buff=1.1, v_buff=0.6)
            if hi:
                for (i, j) in hi:
                    m.get_entries()[3 * i + j].set_color(color)
            return m
        nodes = VGroup(*[VGroup(Circle(radius=0.32, color=S.ACCENT, stroke_width=2.5), MathTex(t, font_size=30))
                         for t in ("X", "Y", "Z")]).arrange(RIGHT, buff=1.3).move_to([0, 2.6, 0])
        arrows = VGroup(Arrow(nodes[0].get_right(), nodes[1].get_left(), buff=0.08, color=GREY_B, stroke_width=3),
                        Arrow(nodes[1].get_right(), nodes[2].get_left(), buff=0.08, color=GREY_B, stroke_width=3))
        chain = label(r"$X\sim N(0,1)$; independent Gaussian noises: $Y=0.8X+\epsilon_Y$, $Z=0.7Y+\epsilon_Z$", font_size=22, color=GREY_B).next_to(nodes, DOWN, buff=0.2)
        mR = mat(R, hi=[(0, 2), (2, 0)], color=COND).scale(0.9).move_to([-3.4, -0.6, 0])
        mK = mat(K, hi=[(0, 2), (2, 0)], color=S.RESID).scale(0.9).move_to([3.4, -0.6, 0])
        tR = MathTex(r"\text{correlations } \Sigma", font_size=28, color=COND).next_to(mR, UP, buff=0.25)
        tK = MathTex(r"\text{precision } K = \Sigma^{-1}", font_size=28, color=S.RESID).next_to(mK, UP, buff=0.25)
        rule = MathTex(r"K_{ij} = 0", r"\iff", r"X_i \perp X_j \mid \text{the rest}", r"\qquad \rho_{ij \cdot \text{rest}} = "
                       r"-\frac{K_{ij}}{\sqrt{K_{ii}K_{jj}}}", font_size=28).to_edge(DOWN, buff=0.55)
        rule[0].set_color(S.RESID)
        intro = label('Conditional independence and precision', font_size=36)
        with self.voiceover(
            "The conditioning formula hides a beautiful fact about the inverse of the covariance matrix. "
            "<bookmark mark='a'/> Build a chain: Y is X times point eight plus noise; Z is Y times point seven plus "
            "noise. Z depends on X only through Y. <bookmark mark='b'/> In the correlation matrix, every entry is "
            f"non-zero: X and Z are correlated, {d['r13']:.2f}, through Y. <bookmark mark='c'/> Now invert it. The "
            "inverse, called the precision matrix, has an exact zero linking X and Z. <bookmark mark='d'/> That's "
            "the rule for a multivariate normal with positive definite covariance: a zero in the precision matrix means the two variables are "
            "independent given all the others, and the scaled entry, with a minus sign, is their partial "
            "correlation. Correlation shows every path of dependence; the precision matrix shows only the direct "
            "links. Arthur Dempster built covariance selection on this in 1972, and Part 31's graphical models "
            "draw the network straight from the zeros."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(nodes), GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(chain))
            vo.wait_until("b")
            self.play(FadeIn(mR), FadeIn(tR))
            vo.wait_until("c")
            self.play(TransformFromCopy(mR, mK), FadeIn(tK), run_time=1.5)
            self.play(*[Indicate(mK.get_entries()[k], color=S.RESID) for k in (2, 6)])
            vo.wait_until("d")
            self.play(FadeIn(rule))
        self.clear_scene()
