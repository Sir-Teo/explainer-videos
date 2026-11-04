from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


class PSD(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.nearest()
        self.cholesky()
        self.loewner()
        self.linear()

    def card(self):
        card = chapter_card(5, r"Positive semidefinite matrices", r"The matrices that can be covariances", lit=(), part=PART)
        with self.voiceover("Chapter five. Positive semidefinite matrices."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        dfn = definition_card(r"Positive semidefinite", r"symmetric $A$ with $\mathbf u^\top A \mathbf u \ge 0$ for every "
                              r"$\mathbf u$; \ equivalently, \ every eigenvalue $\ge 0$; \ \emph{definite} if $> 0$",
                              color=EIG, width=7.0, font_size=24).to_edge(UP, buff=0.4)
        rows = [
            cmath(r"\mathrm{Var}(\mathbf u^\top \mathbf x)", r"=", r"\mathbf u^\top \Sigma\, \mathbf u", r"\ge", r"0",
                  font_size=36),
            cmath(r"\Sigma", r"=", r"Q \Lambda Q^\top", r"=", r"(Q\Lambda^{1/2} Q^\top)^2", font_size=36),
        ]
        whys = [why(r"a variance is never negative: \ every covariance matrix is PSD"),
                why(r"the symmetric square root $\Sigma^{1/2}$")]
        bad = VGroup(MathTex(r"\begin{pmatrix} 1 & 0.9 & -0.9 \\ 0.9 & 1 & 0.9 \\ -0.9 & 0.9 & 1 \end{pmatrix}", font_size=30),
                     label(r"looks like a correlation matrix; \ has a negative eigenvalue: \ impossible", font_size=22,
                           color=RES)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        ev = np.linalg.eigvalsh(np.array([[1, 0.9, -0.9], [0.9, 1, 0.9], [-0.9, 0.9, 1]]))
        evl = MathTex(rf"\lambda_{{\min}} = {ev.min():.2f}", font_size=26, color=RES).next_to(bad, RIGHT, buff=0.5)
        with self.voiceover(
            "Which symmetric matrices can be covariance matrices? <bookmark mark='a'/> Exactly the positive "
            "semidefinite ones: those whose quadratic form is never negative, which, by the spectral theorem, means "
            "every eigenvalue is at least zero. <bookmark mark='b'/> The reason is one line: the variance of any "
            "linear combination u transpose x is u transpose Sigma u, and a variance can't be negative. "
            "<bookmark mark='c'/> PSD matrices have square roots: take the square root of each eigenvalue in the "
            "spectral decomposition. <bookmark mark='d'/> And the condition has teeth. This matrix has ones on the "
            "diagonal and entries between minus one and one, so it looks like a correlation matrix. But it has a "
            "negative eigenvalue, so no three variables can have these correlations: the first two strongly "
            "positive, the second and third strongly positive, yet the first and third strongly negative."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dfn, shift=DOWN * 0.2))
            step = ladder(self, rows, whys, keep=2, top=1.4, x=-1.6, buff=0.6)
            vo.wait_until("b")
            step(0, transform=False)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(bad), FadeIn(evl))
        self.clear_scene()

    def cholesky(self):
        d = load("psd")
        z, x = np.asarray(d["z"]), np.asarray(d["x"])
        L = np.asarray(d["L"])
        c0 = np.array([-3.4, -0.4, 0])
        sc = 0.95
        dots = VGroup(*[Dot(c0 + sc * np.array([a, b, 0]), radius=0.025, color=SIM) for a, b in z])
        frame = VGroup(Line(c0 + LEFT * 3.2, c0 + RIGHT * 3.2, color=GREY_D), Line(c0 + DOWN * 3.2, c0 + UP * 3.2, color=GREY_D))
        rows = VGroup(
            MathTex(r"\Sigma = LL^\top", r",\quad L \text{ lower triangular}", font_size=34),
            MathTex(r"\Sigma = " + mat_tex(d["Sigma"], "{:.1f}"), r"\quad L = " + mat_tex(L, "{:.2f}"), font_size=30),
            MathTex(r"\mathbf z \sim N(\mathbf 0, I)", r"\ \Rightarrow\ ", r"L\mathbf z \sim N(\mathbf 0, LL^\top)", font_size=32),
            MathTex(rf"\text{{sample correlation: }} {d['corr']:.3f}", font_size=28, color=SIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.5, 0.6, 0])
        rows[0][0].set_color(EIG)
        for r in rows:
            if r.width > 6.6:
                r.width = 6.6
        hc = note(r"Andr\'e-Louis Cholesky, \ a French army geodesist (d.\ 1918); \ published 1924").to_corner(DR, buff=0.3)
        with self.voiceover(
            "A positive definite matrix also factors as L times L transpose, with L lower triangular: the Cholesky "
            "decomposition, named for a French army surveyor who devised it for map-making and was killed in the "
            "First World War. <bookmark mark='a'/> It's how a computer makes correlated random numbers. "
            "<bookmark mark='b'/> Start with independent standard normals: a round cloud. <bookmark mark='c'/> "
            "Multiply each point by L, here for a correlation of point eight. <bookmark mark='d'/> The cloud tilts "
            "and stretches into exactly the covariance we asked for: its sample correlation comes out at "
            f"{d['corr']:.2f}. Part 7 uses this to simulate any multivariate normal, and the World's families were "
            "built this way."
        ) as vo:
            self.play(FadeIn(frame), FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(dots, lag_ratio=0.002))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            self.play(*[dt.animate.move_to(c0 + sc * np.array([a, b, 0])) for dt, (a, b) in zip(dots, x)], run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def loewner(self):
        rows = VGroup(
            MathTex(r"A \succeq B", r"\iff", r"A - B \text{ is PSD}", font_size=36),
            label(r"a partial order: \ some pairs are not comparable", font_size=24, color=GREY_A),
            MathTex(r"\mathrm{Cov}(\hat\theta_1) \succeq \mathrm{Cov}(\hat\theta_2)", r"\iff",
                    r"\mathrm{Var}(\mathbf u^\top \hat\theta_1) \ge \mathrm{Var}(\mathbf u^\top \hat\theta_2)\ \ \forall\, \mathbf u",
                    font_size=30),
            label(r"``better in every direction'': \ Gauss--Markov (Part 12), \ Cram\'er--Rao (Part 45)", font_size=24,
                  color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.2, 0])
        with self.voiceover(
            "PSD matrices also give a way to compare matrices. <bookmark mark='a'/> Say A is at least B, in the "
            "Loewner order, when A minus B is positive semidefinite. <bookmark mark='b'/> It's only a partial order: "
            "for many pairs, neither is bigger. <bookmark mark='c'/> But when it holds between two estimators' "
            "covariance matrices, it means one is at least as precise as the other for every linear combination of "
            "the parameters at once. <bookmark mark='d'/> That's the sense in which least squares is best in Part "
            "12's Gauss–Markov theorem, and in which the Cramér–Rao bound of Part 45 is a floor."
        ) as vo:
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def linear(self):
        e = load("extras")["lin"]
        rows = [
            cmath(r"\mathrm{Cov}(A\mathbf x)", r"=", r"E[A(\mathbf x - \boldsymbol\mu)(\mathbf x - \boldsymbol\mu)^\top A^\top]", r"=",
                  r"A\Sigma A^\top", font_size=32),
        ]
        rows[0][4].set_color(EIG)
        whys = [why(r"linearity of expectation; \ $A\Sigma A^\top$ is PSD whenever $\Sigma$ is")]
        ex = VGroup(
            MathTex(r"A = \begin{pmatrix} \tfrac12 & \tfrac12 \\ 1 & -1 \end{pmatrix}", r":\quad", r"\text{(average, \ difference)}",
                    font_size=30),
            MathTex(r"A S A^\top = " + mat_tex(e["ASA"], "{:.1f}"), r"\qquad \text{direct: }" + mat_tex(e["emp"], "{:.1f}"),
                    font_size=30),
            label(r"average and difference of mid-parent and child: \ negatively correlated", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.8, 0])
        ex[1][0].set_color(EIG)
        ex[1][1].set_color(SIM)
        with self.voiceover(
            "One rule moves covariances through linear maps, and it's used constantly. <bookmark mark='a'/> The "
            "covariance of A x is A Sigma A transpose: expand the definition and pull the constant matrices out of "
            "the expectation. It's automatically positive semidefinite, as it must be. <bookmark mark='b'/> For "
            "example, turn each family's pair of heights into their average and their difference. "
            "<bookmark mark='c'/> The formula gives the new covariance matrix without touching the data, and "
            "computing it directly from the transformed data agrees to every digit. Part 5 builds the multivariate "
            "normal on this rule, and Part 12 uses it for the covariance of regression coefficients."
        ) as vo:
            step = ladder(self, rows, whys, keep=1, top=2.6, x=-0.6, buff=0.5, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            self.play(FadeIn(ex[0]))
            vo.wait_until("c")
            self.play(FadeIn(ex[1:]))
        self.clear_scene()

    def nearest(self):
        e = load("extras3")["nearcorr"]
        rows = VGroup(
            MathTex(r"\text{eigenvalues: }" + ", ".join(f"{v:.2f}" for v in e["bad_eig"]), font_size=30, color=RES),
            label(r"the nearest valid correlation matrix: \ clip the negative eigenvalues, \ restore the unit diagonal, \ repeat",
                  font_size=24, color=GREY_A),
            MathTex(r"\begin{pmatrix} 1 & 0.9 & -0.9 \\ 0.9 & 1 & 0.9 \\ -0.9 & 0.9 & 1 \end{pmatrix}", r"\ \longrightarrow\ ",
                    mat_tex(e["fixed"], "{:.2f}"), font_size=30),
            MathTex(r"\text{eigenvalues: }" + ", ".join(f"{abs(v):.2f}" for v in e["fixed_eig"]), font_size=30, color=FIT),
        ).arrange(DOWN, buff=0.35).move_to([0, 0.4, 0])
        rows[2][2].set_color(FIT)
        for r in rows:
            if r.width > 12.6:
                r.width = 12.6
        hc = note(r"N. Higham, \ ``Computing the nearest correlation matrix'' (2002): \ alternating projections").to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Matrices like that one appear in practice, when correlations are estimated from different subsets of "
            "the data, or by hand. <bookmark mark='a'/> Its eigenvalues are minus point eight, one point nine and "
            "one point nine. <bookmark mark='b'/> To repair it, find the nearest matrix that is a valid correlation "
            "matrix: alternately clip the negative eigenvalues to zero and put ones back on the diagonal, which "
            "converges, as Nicholas Higham showed in 2002. <bookmark mark='c'/> The answer here keeps the pattern of "
            "signs but shrinks every correlation to a half, and its eigenvalues are zero, one and a half, and one "
            "and a half: just barely valid. It's how risk managers and geneticists clean up estimated correlation "
            "matrices."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]), FadeIn(hc))
        self.clear_scene()
